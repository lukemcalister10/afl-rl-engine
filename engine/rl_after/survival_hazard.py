"""SURVIVAL HAZARD on the forward lenses — owner ruling SURVIVAL_H2_2026-10-14 (D-H = "H2"), capped; fix plan F1.

THE RULE: retirement/exit risk on the +1 and +2 lens values is probability-based survival, spread across each
age cohort by risk, with the multiplier CAPPED at 1.0 (owner ruling 2026-10-14: nobody rises for survival):

    vP_k' = round( vP_k * min(1, S_k(age, games) / Sbar_k(cohort)) ),      k in {1, 2}, CHARGED rows only
    Sbar_k(cohort) = sum(vP_k * S_k) / sum(vP_k)   over the charged rows of the cohort  (value-weighted)

CHARGED rows are the active rows with career games >= 1. A 0-game (never-played) row reports its fitted S but is
EXCLUDED from the charge and from Sbar (m = 1): its vP is a pick-curve expectation that already averages over
busts, so charging it again would count the bust risk twice. COHORTS are integer ages, with every age >= 33
pooled into one veteran cohort, and any age with fewer than 5 charged rows joined to the nearest larger cohort
below it (the lowest age with no cohort below joins the first cohort above). Because the multiplier is capped
the lens totals can only FALL — the application is NOT sum-preserving: a cohort's proven rows keep their value
and its thin-evidence rows are charged. The present value v and the -1/-2 lenses are never touched; retired/back
rows and phantom picks are never touched. Applied at the EXPORT layer (rl_export.py), never inside ev().

S_k is the fitted age x evidence additive-logit survival on the TRUE listing outcome (fix plan F1):
    S_k(age, evidence) = P(on an AFL list at the END of season Y+k | listed at the END of base season Y,
                           age at Y, career games through Y)
fitted by engine/rl_after/ingestion/fit_survival_hazard.py from the store's own history (the `_last_listed` list
facts of the AFL 2024/2025 list changes, active rows listed through 2026, the last played season as a proxy for
older retirees, the #338 minimum tenure for never-played retirees without a list fact — the JSON's `outcome`
states it exactly). Design (11 columns, data/survival_hazard.json `design`):
    [1, min(age,24)-24, (age-24)+, (age-29)+, (age-33)+, band0, band0 x (tenure>=2),
     band6-20, band21-50, band51-100, band101+]
  * the reference band is 1-5 career games; the 0-game band is its OWN evidence band with a tenure term
    (1st listed season vs 2nd+), fitted on the same outcome — it replaces the former ever0 intake table;
  * monotone in evidence among the PLAYED bands: S = min over band midpoints m >= g of S_raw(age, m), with
    S_raw(age, g); the 0-game band is NOT clamped under the 1-5 band (a first-year never-played rookie is a
    contract regime of his own and measures ABOVE the 1-5 band; his S is reported, never applied).
The calibration lives in data/survival_hazard.json under the repo root (RL_REPO / CLAUDE_PROJECT_DIR, the
same resolution season_read.py uses) and the engine HALTS if it is absent — there is no fallback.

CAP_LIFT below is the ONE switch for the measurement variant. It is a module constant, not an environment
flag: the engine no longer takes kill-switches (docs/evidence/engine_chain_hardwired_single_reader_2026-10-14/
NOTE.md). The shipped default is the document's cap_lift (true).
"""
import os, json, math, hashlib
from season_read import repo_root

#: THE cap switch. None = take data/survival_hazard.json's `cap_lift` (true: the shipped capped rule). Flip to
#: False for a pure-H2 measurement build (multiplier S/Sbar uncapped, sum-preserving per cohort over the charged
#: rows); the board's `survivalHazard.cap_lift` reports the value IN EFFECT.
CAP_LIFT = None

HAZARD_REL = ('data', 'survival_hazard.json')
RULING = 'SURVIVAL_H2_2026-10-14'
LENSES = ((1, 'S1'), (2, 'S2'))
N_COEF = 11
POOL_FROM = 33          # integer ages >= POOL_FROM form one veteran cohort
MIN_CHARGED = 5         # an age with fewer charged rows joins the nearest larger cohort below it


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
    for k in ('coef', 'cap_lift', 'band_midpoints', 'ruling', 'design', 'outcome'):
        if k not in doc:
            raise SurvivalHazardError('survival hazard: %s carries no %r' % (p, k))
    for _, nm in LENSES:
        c = doc['coef'].get(nm)
        if not isinstance(c, list) or len(c) != N_COEF or not all(math.isfinite(float(x)) for x in c):
            raise SurvivalHazardError('survival hazard: %s coef.%s is not a finite %d-vector' % (p, nm, N_COEF))
    if doc['ruling'] != RULING:
        raise SurvivalHazardError('survival hazard: %s carries ruling %r, the engine implements %r'
                                  % (p, doc['ruling'], RULING))
    doc['_path'] = p
    doc['_md5'] = hashlib.md5(raw).hexdigest()
    return doc


# ---- the fitted survival --------------------------------------------------------------------------------
BANDS = ((1, 5), (6, 20), (21, 50), (51, 100), (101, None))


def band_index(games):
    """0 for 0 games; 1..5 for the played bands 1-5, 6-20, 21-50, 51-100, 101+."""
    g = int(games)
    if g == 0:
        return 0
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= g and (hi is None or g <= hi):
            return i + 1
    raise SurvivalHazardError('survival hazard: games=%r has no evidence band' % (games,))


def features(age, games, tenure=1):
    """The 11-column design row (fit_survival_hazard.py `design`)."""
    a = float(age); b = band_index(games)
    return [1.0, min(a, 24.0) - 24.0, max(0.0, a - 24.0), max(0.0, a - 29.0), max(0.0, a - 33.0),
            1.0 if b == 0 else 0.0, 1.0 if (b == 0 and int(tenure) >= 2) else 0.0] + \
           [1.0 if b == i else 0.0 for i in range(2, 6)]


def survival_raw(age, games, coef, tenure=1):
    z = sum(x * float(c) for x, c in zip(features(age, int(games), tenure), coef))
    return 1.0 / (1.0 + math.exp(-z))


def survival(age, games, coef, midpoints=(3, 12, 35, 75, 180), tenure=1):
    """S(age, g). Played bands (g >= 1) are monotone in evidence: a thinner band can never beat a thicker one
    at the same age (min over the band midpoints m >= g). The 0-game band is its own fitted value by tenure."""
    g = int(games)
    s = survival_raw(age, g, coef, tenure)
    if g == 0:
        return s
    if g <= max(midpoints):
        s = min(s, min(survival_raw(age, m, coef) for m in midpoints if m >= g))
    return s


def tenure_of(ty, yr, base_year):
    """Seasons on a list through the base season: base_year - debut + 1, debut = draft year + 1 (MSD: draft
    year; rl_model.py:171). Floored at 1."""
    debut = int(yr) if ty == 'MSD' else int(yr) + 1
    return max(1, base_year - debut + 1)


def survival_of(row, k, doc, base_year):
    """S_k for one row {age, games, ty, yr}; halts when age/games (or, for a 0-game row, type/year) cannot be formed."""
    age, games = row.get('age'), row.get('games')
    key = row.get('key', '?')
    if not isinstance(age, (int, float)) or isinstance(age, bool) or not math.isfinite(age) or int(age) != age or age < 15:
        raise SurvivalHazardError('survival hazard: %s has no usable age (%r); refusing to price the lens' % (key, age))
    if not isinstance(games, (int, float)) or isinstance(games, bool) or not math.isfinite(games) or int(games) != games or games < 0:
        raise SurvivalHazardError('survival hazard: %s has no usable career games (%r); refusing to price the lens' % (key, games))
    tenure = 1
    if int(games) == 0:
        ty, yr = row.get('ty'), row.get('yr')
        if not ty or not isinstance(yr, int) or isinstance(yr, bool):
            raise SurvivalHazardError('survival hazard: 0-game row %s has no usable type/year (%r, %r)' % (key, ty, yr))
        tenure = tenure_of(ty, yr, base_year)
    return survival(int(age), int(games), doc['coef']['S%d' % k], tuple(doc['band_midpoints']), tenure)


# ---- the cohorts ----------------------------------------------------------------------------------------
def cohorts_of(charged_count, pool_from=POOL_FROM, min_charged=MIN_CHARGED):
    """charged_count: {age: n charged rows}. Returns {age: cohort label}. Integer-age cohorts; ages >= pool_from
    pooled into one; an age with fewer than min_charged charged rows joins the nearest larger cohort below it
    (an age with nothing below joins the first cohort above; a thin veteran pool joins the cohort below it)."""
    ages = sorted(a for a, n in charged_count.items() if n > 0)
    groups = []; pending = []
    for a in ages:
        if a >= pool_from:
            break
        if charged_count[a] >= min_charged:
            groups.append(pending + [a]); pending = []
        elif groups:
            groups[-1].append(a)
        else:
            pending.append(a)
    vets = [a for a in ages if a >= pool_from]
    if vets:
        if sum(charged_count[a] for a in vets) >= min_charged or not groups:
            groups.append(pending + vets); pending = []
        else:
            groups[-1].extend(vets)
    if pending:
        if groups:
            groups[0] = pending + groups[0]
        else:
            groups.append(pending)
    out = {}
    for g in groups:
        lo, hi = min(g), max(g)
        label = ('%d+' % lo) if hi >= pool_from else (('%d' % lo) if lo == hi else ('%d-%d' % (lo, hi)))
        for a in g:
            out[a] = label
    return out


# ---- the capped relative application --------------------------------------------------------------------
def apply(rows, doc, base_year, cap_lift=None):
    """rows: list of dicts {key, age, games, ty, yr, vP1, vP2} (the ACTIVE board rows). Returns
    (per_key, report): per_key[key] = {S1, S2, age, games, cohort, charged, m1, m2, vP1, vP2} with the NEW
    rounded lens values; report = the board-level `survivalHazard` block. Pure: never mutates `rows`.
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
        per[r['key']]['charged'] = int(r['games']) >= 1
    charged_count = {}
    for r in rows:
        if per[r['key']]['charged']:
            a = per[r['key']]['age']; charged_count[a] = charged_count.get(a, 0) + 1
    coh = cohorts_of(charged_count)
    for r in rows:
        per[r['key']]['cohort'] = coh.get(per[r['key']]['age'])
    sbar = {}; totals = {}
    for k, nm in LENSES:
        fld = 'vP%d' % k
        num = {}; den = {}; n_c = {}; n_z = {}; ages = {}
        for r in rows:
            v = r.get(fld)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
                raise SurvivalHazardError('survival hazard: %s has no %s (%r)' % (r['key'], fld, v))
            c = per[r['key']]['cohort']
            if not per[r['key']]['charged'] or c is None:
                continue
            num[c] = num.get(c, 0.0) + v * per[r['key']][nm]
            den[c] = den.get(c, 0.0) + v
            n_c[c] = n_c.get(c, 0) + 1
            ages.setdefault(c, set()).add(per[r['key']]['age'])
        for r in rows:
            if not per[r['key']]['charged']:
                c = coh.get(per[r['key']]['age'])
                if c is not None:
                    n_z[c] = n_z.get(c, 0) + 1
        # Sbar_k(cohort): value-weighted mean of S_k over the CHARGED rows of the cohort. A cohort whose lens
        # sum is 0 has nothing to redistribute: m=1.
        sb = {c: (num[c] / den[c] if den[c] > 0 else None) for c in num}
        sbar['S%d' % k] = {c: {'sbar': (round(sb[c], 6) if sb[c] is not None else None), 'n_charged': n_c[c],
                               'n_zero_game': n_z.get(c, 0), 'ages': sorted(ages[c]), 'lens_sum': int(round(den[c]))}
                           for c in sorted(num, key=lambda c: min(ages[c]))}
        before = 0; after = 0; charge = 0
        for r in rows:
            v = r[fld]; s = per[r['key']][nm]; c = per[r['key']]['cohort']
            if per[r['key']]['charged'] and c is not None and sb.get(c) is not None:
                m = s / sb[c]
                if cap and m > 1.0:
                    m = 1.0
            else:
                m = 1.0
            nv = int(round(v * m))
            per[r['key']]['m%d' % k] = round(m, 6)
            per[r['key']][fld] = nv
            before += v; after += nv
        totals['+%d' % k] = {'field': fld, 'before': int(round(before)), 'after': after, 'delta': after - int(round(before))}
    n = len(rows); n_charged = sum(1 for r in rows if per[r['key']]['charged'])
    for lbl, t in totals.items():
        if cap:
            if t['after'] > t['before']:
                raise SurvivalHazardError('survival hazard: cap_lift=True but the %s total ROSE %d -> %d' % (lbl, t['before'], t['after']))
        elif abs(t['delta']) > 0.5 * max(1, n_charged):
            raise SurvivalHazardError('survival hazard: %s total NOT preserved %d -> %d (delta %+d exceeds the '
                                      'rounding bound %.1f on %d charged rows)' % (lbl, t['before'], t['after'], t['delta'], 0.5 * n_charged, n_charged))
    report = {'ruling': doc['ruling'], 'source': os.path.relpath(doc['_path'], repo_root()) if doc.get('_path') else None,
              'source_md5': doc.get('_md5'), 'cap_lift': cap, 'cap_lift_recorded': bool(doc['cap_lift']),
              'base_year': base_year, 'nActive': n, 'nCharged': n_charged, 'nZeroGame': n - n_charged,
              'design': doc.get('design'), 'outcome': doc.get('outcome'),
              'cohort_of_age': {str(a): c for a, c in sorted(coh.items())}, 'sbar_by_cohort': sbar, 'totals': totals,
              'law': ('vP_k = round(vP_k x min(1, S_k(age,games) / Sbar_k(cohort))) over the charged rows (games >= 1); '
                      'Sbar_k(cohort) = value-weighted mean of S_k over the charged rows of the cohort (integer ages, >= %d '
                      'pooled, < %d charged rows joins the cohort below); 0-game rows report S and are not charged; the cap '
                      'means the totals can only fall (not sum-preserving)' % (POOL_FROM, MIN_CHARGED)) if cap else
                     ('vP_k = round(vP_k x S_k(age,games) / Sbar_k(cohort)) over the charged rows (pure H2 measurement '
                      'variant: sum-preserving per cohort to rounding)'),
              'untouched': 'v, vM1, vM2, 0-game active rows, back rows, phantom picks', 'applied_at': 'export layer (rl_export.py), not ev()'}
    return per, report
