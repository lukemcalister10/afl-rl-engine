"""SURVIVAL HAZARD on the forward lenses — owner ruling SURVIVAL_H2_2026-10-14 (D-H = "H2").

THE RULE: retirement/exit risk on the +1 and +2 lens values is probability-based survival, spread across
each age cohort by risk, SUM-PRESERVING within each integer-age band:

    vP_k' = round( vP_k * S_k(age, games) / Sbar_k(age) ),      k in {1, 2}
    Sbar_k(age) = sum(vP_k * S_k) / sum(vP_k)   over ALL active rows at that integer age  (value-weighted)

so a cohort's lens total is unchanged (to rounding) and the charge is carried by the thin-evidence / old
rows inside it, the lift by the proven ones. The present value v and the -1/-2 lenses are never touched;
retired/back rows and phantom picks are never touched. Applied at the EXPORT layer (rl_export.py), never
inside ev().

S_k is the fitted age x evidence additive-logit survival (S1 = listed one season on, S2 = two seasons on),
replicated EXACTLY from the owner's scratch calibration (scratchpad/hazard/hazard_final_v2.py):
  * design  [1, min(age,24)-24, (age-24)+, (age-29)+, (age-33)+, band6-20, band21-50, band51-100, band100+]
    (hazard_final_v2.py lines 24-29; the base band is 1-5 career games);
  * monotone in evidence (line 36): S = min over band midpoints m >= g of S_raw(age, m), with S_raw(age, g);
  * a 0-game row takes the intake-cohort 'ever plays' rate ever0[type|tenure] as S2, sqrt as S1 (lines 58-62).
The calibration lives in data/survival_hazard.json under the repo root (RL_REPO / CLAUDE_PROJECT_DIR, the
same resolution season_read.py uses) and the engine HALTS if it is absent — there is no fallback.

CAP_LIFT below is the ONE switch for the measurement variant (multiplier capped at 1.0, no lifts). It is a
module constant, not an environment flag: the engine no longer takes kill-switches
(docs/evidence/engine_chain_hardwired_single_reader_2026-10-14/NOTE.md).
"""
import os, json, math, hashlib
from season_read import repo_root

#: THE cap switch. None = take data/survival_hazard.json's `cap_lift` (the recorded ruling default, false =
#: pure H2, lifts allowed). Flip to True for a no-lift measurement build (multiplier = min(1, S/Sbar)); the
#: board's `survivalHazard.cap_lift` reports the value IN EFFECT. Under the cap the per-age sums are NOT
#: preserved (the total can only fall) and the conservation assert is relaxed to "after <= before".
CAP_LIFT = None

HAZARD_REL = ('data', 'survival_hazard.json')
RULING = 'SURVIVAL_H2_2026-10-14'
LENSES = ((1, 'S1'), (2, 'S2'))


class SurvivalHazardError(RuntimeError):
    pass


def hazard_path():
    return os.path.join(repo_root(), *HAZARD_REL)


def load(path=None):
    """The calibration document + its md5. Halts (raises) when the file is absent, unreadable or malformed."""
    p = path or hazard_path()
    try:
        raw = open(p, 'rb').read()
    except OSError as e:
        raise SurvivalHazardError('survival hazard: cannot read %s (%s) — the forward lenses are not priced '
                                  'without the %s calibration; no fallback' % (p, e, RULING)) from e
    try:
        doc = json.loads(raw.decode('utf-8'))
    except ValueError as e:
        raise SurvivalHazardError('survival hazard: %s is not JSON (%s)' % (p, e)) from e
    for k in ('coef', 'ever0', 'ever0_default', 'cap_lift', 'band_midpoints', 'ruling'):
        if k not in doc:
            raise SurvivalHazardError('survival hazard: %s carries no %r' % (p, k))
    for _, nm in LENSES:
        c = doc['coef'].get(nm)
        if not isinstance(c, list) or len(c) != 9 or not all(math.isfinite(float(x)) for x in c):
            raise SurvivalHazardError('survival hazard: %s coef.%s is not a finite 9-vector' % (p, nm))
    if doc['ruling'] != RULING:
        raise SurvivalHazardError('survival hazard: %s carries ruling %r, the engine implements %r'
                                  % (p, doc['ruling'], RULING))
    doc['_path'] = p
    doc['_md5'] = hashlib.md5(raw).hexdigest()
    return doc


# ---- the fitted survival --------------------------------------------------------------------------------
BANDS = ((1, 5), (6, 20), (21, 50), (51, 100), (101, None))


def band_index(games):
    """0..4 for games >= 1 (bands 1-5, 6-20, 21-50, 51-100, 101+). hazard_final_v2.py line 14 (bi)."""
    g = int(games)
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= g and (hi is None or g <= hi):
            return i
    raise SurvivalHazardError('survival hazard: games=%r has no evidence band' % (games,))


def features(age, games):
    """The 9-column design row (hazard_final_v2.py lines 24-29); games >= 1."""
    a = float(age); b = band_index(games)
    return [1.0, min(a, 24.0) - 24.0, max(0.0, a - 24.0), max(0.0, a - 29.0), max(0.0, a - 33.0)] + \
           [1.0 if b == i else 0.0 for i in range(1, 5)]


def survival_raw(age, games, coef):
    z = sum(x * float(c) for x, c in zip(features(age, max(1, int(games))), coef))
    return 1.0 / (1.0 + math.exp(-z))


def survival(age, games, coef, midpoints=(3, 12, 35, 75, 180)):
    """S(age, g) for g >= 1, monotone in evidence (hazard_final_v2.py line 36): a thinner band can never
    beat a thicker one at the same age."""
    g = max(1, int(games))
    s = survival_raw(age, g, coef)
    if g <= max(midpoints):
        s = min(s, min(survival_raw(age, m, coef) for m in midpoints if m >= g))
    return s


def survival0(ty, yr, k, ever0, default, base_year):
    """The 0-game row: intake-cohort 'ever plays' rate by (type, tenure) as S2, sqrt of it as S1
    (hazard_final_v2.py lines 58-62; tenure = clamp(base_year - year (+1 for MSD), 1, 2))."""
    ten = max(1, min(2, (base_year - int(yr)) if ty != 'MSD' else (base_year - int(yr) + 1)))
    s2 = float(ever0.get('%s|%d' % (ty, ten), default))
    return math.sqrt(s2) if k == 1 else s2


def survival_of(row, k, doc, base_year):
    """S_k for one row {age, games, ty, yr}; halts when age/games cannot be formed."""
    age, games = row.get('age'), row.get('games')
    key = row.get('key', '?')
    if not isinstance(age, (int, float)) or isinstance(age, bool) or not math.isfinite(age) or int(age) != age or age < 15:
        raise SurvivalHazardError('survival hazard: %s has no usable age (%r); refusing to price the lens' % (key, age))
    if not isinstance(games, (int, float)) or isinstance(games, bool) or not math.isfinite(games) or int(games) != games or games < 0:
        raise SurvivalHazardError('survival hazard: %s has no usable career games (%r); refusing to price the lens' % (key, games))
    if int(games) == 0:
        ty, yr = row.get('ty'), row.get('yr')
        if not ty or not isinstance(yr, int) or isinstance(yr, bool):
            raise SurvivalHazardError('survival hazard: 0-game row %s has no usable type/year (%r, %r)' % (key, ty, yr))
        return survival0(ty, yr, k, doc['ever0'], doc['ever0_default'], base_year)
    return survival(int(age), int(games), doc['coef']['S%d' % k], tuple(doc['band_midpoints']))


# ---- the sum-preserving relative application ----------------------------------------------------------
def apply(rows, doc, base_year, cap_lift=None):
    """rows: list of dicts {key, age, games, ty, yr, vP1, vP2} (the ACTIVE board rows). Returns
    (per_key, report): per_key[key] = {S1, S2, age, games, m1, m2, vP1, vP2} with the NEW rounded lens
    values; report = the board-level `survivalHazard` block. Pure: never mutates `rows`.
    cap_lift None -> the module constant CAP_LIFT, itself None -> the document's cap_lift."""
    cap = CAP_LIFT if cap_lift is None else cap_lift
    if cap is None:
        cap = bool(doc['cap_lift'])
    cap = bool(cap)
    per = {}
    for r in rows:
        if r['key'] in per:
            raise SurvivalHazardError('survival hazard: duplicate active key %r' % r['key'])
        per[r['key']] = {'age': int(r['age']) if isinstance(r.get('age'), (int, float)) else r.get('age'),
                         'games': r.get('games')}
        for k, nm in LENSES:
            per[r['key']][nm] = survival_of(r, k, doc, base_year)
    sbar = {}; totals = {}
    for k, nm in LENSES:
        fld = 'vP%d' % k
        num = {}; den = {}; n_age = {}
        for r in rows:
            v = r.get(fld)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
                raise SurvivalHazardError('survival hazard: %s has no %s (%r)' % (r['key'], fld, v))
            a = per[r['key']]['age']
            num[a] = num.get(a, 0.0) + v * per[r['key']][nm]
            den[a] = den.get(a, 0.0) + v
            n_age[a] = n_age.get(a, 0) + 1
        # Sbar_k(age): value-weighted mean of S_k over the active rows at that age (hazard_part2.py [f]:
        # sum(p[fld]*S)/max(1,sum(p[fld]))). An age whose lens sum is 0 has nothing to redistribute: m=1.
        sb = {a: (num[a] / den[a] if den[a] > 0 else None) for a in num}
        sbar['S%d' % k] = {str(a): {'sbar': (round(sb[a], 6) if sb[a] is not None else None), 'n': n_age[a],
                                    'lens_sum': int(round(den[a]))} for a in sorted(num)}
        before = 0; after = 0
        for r in rows:
            v = r[fld]; a = per[r['key']]['age']; s = per[r['key']][nm]
            m = 1.0 if sb[a] is None else s / sb[a]
            if cap and m > 1.0:
                m = 1.0
            nv = int(round(v * m))
            per[r['key']]['m%d' % k] = round(m, 6)
            per[r['key']][fld] = nv
            before += v; after += nv
        totals['+%d' % k] = {'field': fld, 'before': int(round(before)), 'after': after, 'delta': after - int(round(before))}
    n = len(rows)
    for lbl, t in totals.items():
        if cap:
            if t['after'] > t['before']:
                raise SurvivalHazardError('survival hazard: cap_lift=True but the %s total ROSE %d -> %d' % (lbl, t['before'], t['after']))
        elif abs(t['delta']) > 0.5 * max(1, n):
            raise SurvivalHazardError('survival hazard: %s total NOT preserved %d -> %d (delta %+d exceeds the '
                                      'rounding bound %.1f on %d rows)' % (lbl, t['before'], t['after'], t['delta'], 0.5 * n, n))
    report = {'ruling': doc['ruling'], 'source': os.path.relpath(doc['_path'], repo_root()) if doc.get('_path') else None,
              'source_md5': doc.get('_md5'), 'cap_lift': cap, 'cap_lift_recorded': bool(doc['cap_lift']),
              'base_year': base_year, 'nActive': n, 'design': doc.get('design'),
              'sbar_by_age': sbar, 'totals': totals,
              'law': 'vP_k = round(vP_k x S_k(age,games) / Sbar_k(age)); Sbar_k(age) = value-weighted mean of S_k over '
                     'the active rows at that integer age (sum-preserving per age band; cap_lift caps the multiplier at 1.0)',
              'untouched': 'v, vM1, vM2, back rows, phantom picks', 'applied_at': 'export layer (rl_export.py), not ev()'}
    return per, report
