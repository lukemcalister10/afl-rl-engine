#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — shared loaders. READ-ONLY. No engine import, no board build, no store write.

Everything here reads the BUILT walk-forward matrices that ORDER P BUILD produced and that
op_class.py scored. The class-mark arithmetic below is a line-for-line restatement of
docs/evidence/order_p_build_2026-08-18/op_class.py so that any number this diagnostic prints can be
checked against that file's own published output.
"""
import json, math, os, collections

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
W2 = list(range(2006, 2017))          # cohort years == DRAFT classes 2005-2015. THE REGISTERED BASIS
ALLC = list(range(2005, 2022))
RAIL, FLOOR = 1.14, 1.03

# the S4 house ruler's flat bars, and the C3 age deltas, both copied out of ORDER N's on_lib.py.
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))
LAST_REAL_SEASON = 2025


def load(tag):
    return json.load(open(os.path.join(SP, 'per_entrant_%s.json' % tag)))['recs']


def cohort(r):
    y = r.get('year')
    return None if y is None else (y if r.get('type') == 'MSD' else y + 1)


def year1_price(r, y, wend):
    """op_class.py's own value semantics, verbatim. Returns None when the row is EXCLUDED
    (pre-window / after the matrix ends), else the year-1 price with ended/null scored 0."""
    yrs = r.get('yrs') or []
    vp = r.get('vpath') or []
    if y > wend:
        return None
    if not yrs:
        return 0.0
    if y < yrs[0]:
        return None
    if y > yrs[-1]:
        return 0.0
    i = yrs.index(y)
    return 0.0 if vp[i] is None else float(vp[i])


def rowset(R):
    """the eligible set and the per-class row lists, exactly as op_class.py forms them."""
    wend = max(y for r in R for y, v in zip(r.get('yrs') or [], r.get('vpath') or []) if v is not None)
    elig = [r for r in R if cohort(r) is not None and (r.get('v0') or 0) > 0]
    per = collections.defaultdict(list)
    for r in elig:
        per[cohort(r)].append(r)
    return per, wend


def class_marks(R):
    per, wend = rowset(R)
    out = {}
    for y in ALLC:
        num = den = 0.0
        n = 0
        for r in per.get(y, []):
            v1 = year1_price(r, y, wend)
            if v1 is None:
                continue
            num += v1
            den += float(r['v0'])
            n += 1
        out[y] = (num / den) if (den > 0 and n >= 5) else None
    return out, wend


# ---- realised outcomes, straight off the store rows carried in the matrix ---------------------------
def age_at(r, year):
    ad = r.get('age_draft')
    return None if ad is None else int(ad) + (int(year) - int(r['year']))


def bar_flat(pos):
    return BARS.get(pos)


def season_of(r, year):
    for s in r.get('seasons') or []:
        if s.get('year') == year and (s.get('games') or 0) > 0:
            return s
    return None


# ---- the age bar, out of the S1 C3 surface (same numbers ORDER N's on_lib.py asserts) ---------------
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def _find(name, *rel):
    """the file as it sits in the repo, or a local copy beside this script."""
    for c in [os.path.join(REPO, r, name) for r in rel] + [os.path.join(HERE, name)]:
        if os.path.exists(c):
            return c
    raise IOError('cannot find %s' % name)


_S1 = json.load(open(_find('CONSTRUCTIONS_S1.json', 'docs/evidence/order32_s1_2026-08-17')))
GATE_DELTA = {'TALL': {}, 'SMALL': {}}
for _k, _v in _S1['C3meta'].items():
    if _k.startswith('('):
        _c, _a = _k.strip('()').replace("'", '').split(',')
        GATE_DELTA[_c.strip()][int(_a)] = float(_v['delta'])
assert all(abs(_S1['bars_flat'][k] - BARS[k]) < 1e-9 for k in BARS)


def age_bar(pos, age):
    b = BARS.get(pos)
    if b is None:
        return None
    if age is None or age >= 24:
        return b
    return b - GATE_DELTA['TALL' if pos in TALLPOS else 'SMALL'][max(18, min(23, int(age)))]


# ---- the pedigree premium PG(ln v0, class), read off the surface the engine was wired with ----------
_PS = json.load(open(_find('PREMIUM_SURFACE.json', 'docs/evidence/order_p_build_2026-08-18')))


def premium(v0, pos):
    cls = 'TALL' if pos in TALLPOS else 'SMALL'
    g = _PS[cls]
    lo, hi, ys = float(g['lo']), float(g['hi']), [float(z) for z in g['y']]
    x = math.log(max(1e-9, float(v0)))
    n = len(ys)
    if x <= lo:
        return ys[0]
    if x >= hi:
        return ys[-1]
    t = (x - lo) / (hi - lo) * (n - 1)
    i = int(t)
    if i >= n - 1:
        return ys[-1]
    f = t - i
    return ys[i] * (1 - f) + ys[i + 1] * f


def ped_bar(pos, age, v0):
    b = age_bar(pos, age)
    return None if b is None else b + premium(v0, pos)


def surplus(r, upto, bar_fn):
    """games-weighted mean of (season avg - bar) over every played season up to and including `upto`.
    None when nothing is readable — reported as a null, never as a zero."""
    num = den = 0.0
    for s in r.get('seasons') or []:
        if s['year'] > upto or (s.get('games') or 0) <= 0 or s['year'] > LAST_REAL_SEASON:
            continue
        if s.get('avg') is None or s.get('bar') not in BARS:
            return None
        b = bar_fn(s['bar'], age_at(r, s['year']), float(r.get('v0') or 0.0))
        if b is None:
            return None
        g = float(s['games'])
        num += g * (float(s['avg']) - b)
        den += g
    return None if den <= 0 else num / den
