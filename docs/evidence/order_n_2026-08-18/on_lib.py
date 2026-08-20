#!/usr/bin/env python3
"""ORDER N — the shared constructions. READ-ONLY. No engine import, no board build, no store write.

Everything in here is fixed by PREREG_N.md sections 2.1, 2.2, 2.3, 2.4 and 2.5. Nothing is fitted
here. The two objects this file owns are:

  bar(pos, age)   -- the engine's own o32_gate_bar, read from the S1 C3 surface and ASSERTED against
                     the engine source's O32_GATE_DELTA literal (falsifier N2).
  PS(rec, Y)      -- performance surplus: games-weighted mean of (season avg - bar) over seasons up
                     to and including Y.

and it re-exports the house delivered-value ruler, copied byte-for-byte out of
docs/evidence/order32_s4_2026-08-17/s4_shootout.py and md5-asserted (falsifier N3).
"""
import json, math, os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

S1_PATH = os.path.join(REPO, 'docs/evidence/order32_s1_2026-08-17/CONSTRUCTIONS_S1.json')
S4_PATH = os.path.join(REPO, 'docs/evidence/order32_s4_2026-08-17/s4_shootout.py')
S4_COPY = os.path.join(HERE, 's4_shootout_COPY.py')
S4_MD5 = '241842f61ddd3c486f04f201a7efcce9'
ENGINE = os.path.join(REPO, 'engine/rl_after/_merged_recover.py')
LEDGER = os.path.join(REPO, 'docs/ledgers/ORDER_K_MOVERS.json')

TALLPOS = frozenset(('KPD', 'KPF', 'RUCK'))

# ---- the house ruler, byte-for-byte out of s4_shootout.py -------------------------------------------
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
FM = {'paddy-mccartin', 'thomas-boyd'}
DISC = 1.14


def softplus(x):
    return math.log1p(math.exp(x)) if x < 30.0 else x


def capt_prem(lev):
    c = LCAPT_G * LCAPT_W * (softplus((lev - LCAPT_M) / LCAPT_W) - softplus((LCAPT_BAR - LCAPT_M) / LCAPT_W))
    return c if c > 0.0 else 0.0


def posval(x):
    return S_SH * math.log(1 + math.exp(min(x / S_SH, 40.0)))


def season_raw(X, g):
    return posval(X + capt_prem(X) - BARS[g]) * 21.0


def w_sqrt(g):
    return min(1.0, math.sqrt(max(0.0, g) / 10.0))


# ---- the engine's own age bar -----------------------------------------------------------------------
def _load_delta():
    """C3 deltas out of CONSTRUCTIONS_S1.json, then ASSERTED against the engine source literal."""
    D = json.load(open(S1_PATH))
    delta = {'TALL': {}, 'SMALL': {}}
    for k, v in D['C3meta'].items():
        if not k.startswith('('):
            continue
        cls, age = k.strip('()').replace("'", '').split(',')
        delta[cls.strip()][int(age)] = float(v['delta'])
    flat = dict(D['bars_flat'])
    # falsifier N2: the engine's own literal
    src = open(ENGINE, 'r').read()
    m = re.search(r"O32_GATE_DELTA=\{(.*?)\}\}", src, re.S)
    assert m, 'N2 FIRED: cannot find O32_GATE_DELTA in the engine source'
    blob = 'dict(' + m.group(0).split('=', 1)[1].replace("'TALL'", 'TALL=').replace("'SMALL'", 'SMALL=') \
        .replace('{TALL=', 'TALL=dict_(').replace(',SMALL=', '),SMALL=dict_(').rstrip('}') + '))'
    # simpler and safer: eval the literal directly
    lit = m.group(0).split('=', 1)[1]
    eng = eval(lit, {'__builtins__': {}}, {})
    for cls in ('TALL', 'SMALL'):
        for a in range(18, 24):
            assert abs(eng[cls][a] - delta[cls][a]) < 1e-9, \
                'N2 FIRED: C3 delta %s|%d %.12f != engine %.12f' % (cls, a, delta[cls][a], eng[cls][a])
    return delta, flat, eng


GATE_DELTA, BARS_FLAT, _ENG_DELTA = _load_delta()
assert set(BARS_FLAT) == set(BARS) and all(abs(BARS_FLAT[k] - BARS[k]) < 1e-9 for k in BARS), \
    'N2 FIRED: S1 bars_flat != the S4 ruler BARS'


def bar(pos, age):
    """o32_gate_bar, reproduced. Flat at/from 24; C3 class-pooled offset below; <=18 takes the 18 column."""
    b = BARS_FLAT.get(pos)
    if b is None:
        return None
    if age is None or age >= 24:
        return b
    return b - GATE_DELTA['TALL' if pos in TALLPOS else 'SMALL'][max(18, min(23, int(age)))]


def check_s4_copy():
    h = hashlib.md5(open(S4_COPY, 'rb').read()).hexdigest()
    assert h == S4_MD5, 'N3 FIRED: S4 ruler copy md5 %s != %s' % (h, S4_MD5)
    h2 = hashlib.md5(open(S4_PATH, 'rb').read()).hexdigest()
    assert h2 == S4_MD5, 'N3 FIRED: S4 ruler source md5 moved'
    return h


# ---- matrices ---------------------------------------------------------------------------------------
def load_matrix(tag):
    D = json.load(open(os.path.join(SP, 'per_entrant_%s.json' % tag)))
    return {r['key']: r for r in D['recs']}


def age_at(rec, year):
    ad = rec.get('age_draft')
    if ad is None:
        return None
    return int(ad) + (int(year) - int(rec['year']))


def seasons_upto(rec, Y):
    return [s for s in rec['seasons'] if s['year'] <= Y and (s.get('games') or 0) > 0]


def career_games(rec, Y):
    return sum(float(s['games']) for s in seasons_upto(rec, Y))


def perf_surplus(rec, Y):
    """PREREG N 2.2. None when no played season up to Y, or when any season lacks a bar/age."""
    ss = seasons_upto(rec, Y)
    if not ss:
        return None
    num = den = 0.0
    for s in ss:
        a = age_at(rec, s['year'])
        b = bar(s.get('bar'), a)
        if b is None or s.get('avg') is None:
            return None
        g = float(s['games'])
        num += g * (float(s['avg']) - b)
        den += g
    return num / den if den > 0 else None


def season_values(rec):
    """SV[year] on the house ruler. Right-censored at LAST_REAL_SEASON exactly as s4_shootout does."""
    d = {}
    for s in rec['seasons']:
        if s['year'] > LAST_REAL_SEASON:
            continue
        g = s.get('bar')
        if g not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * season_raw(s['avg'], g)
    return d


def dv1(sv, Y):
    return sv.get(Y + 1, 0.0)


def dvrest(sv, Y):
    return sum((DISC ** -(t - Y)) * v for t, v in sv.items() if t > Y)


# ---- the eta charge ---------------------------------------------------------------------------------
GAMMA_D = 14.0
ETA_K = 0.50            # ORDER K's ruled eta


def m_d(g):
    g = float(g)
    return (g / GAMMA_D) * math.exp(1.0 - g / GAMMA_D)


def eta_charge(g, eta=ETA_K):
    return max(0.0, eta * m_d(g))


# ---- games bins -------------------------------------------------------------------------------------
G_BINS_1 = [(1, 4), (5, 9), (10, 15), (16, 24), (25, 39), (40, 60)]
G_BINS_2 = [(1, 3), (4, 7), (8, 12), (13, 17), (18, 24), (25, 39), (40, 60)]


def binof(g, bins):
    """Bins are stated on integer games but games can be fractional (an in-progress season), so the
    upper edge is half-open at hi+1. Every g in [bins[0][0], bins[-1][1]+1) lands in exactly one bin."""
    for lo, hi in bins:
        if lo <= g < hi + 1:
            return '%d-%d' % (lo, hi)
    return None


def band_of(pick):
    if pick is None:
        return '41+/pool'
    p = int(pick)
    if p <= 10: return '1-10'
    if p <= 20: return '11-20'
    if p <= 40: return '21-40'
    return '41+/pool'


def load_ledger():
    return json.load(open(LEDGER))
