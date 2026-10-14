"""SURVIVAL HAZARD on the forward lenses — owner ruling SURVIVAL_H2_2026-10-14 (D-H = "H2"), capped; fix plan F1.

THE RULE: retirement/exit risk on the +1 and +2 lens values is probability-based survival, spread across each
age cohort by EVIDENCE, with the multiplier CAPPED at 1.0 (owner ruling 2026-10-14: nobody rises for survival):

    vP_k' = round( vP_k * m_k ),   m_k(i) = min(1, S_k(age_i, g_i) / R_k(age_i)),      k in {1, 2}, CHARGED rows
    R_k(age_i) = sum_j w_j * S_k(age_i, g_j)   over the charged rows j of i's cohort,  w_j = vP_k(j) / sum vP_k

R_k is the cohort's evidence mix priced AT ROW i's OWN AGE: a row is charged only for carrying thinner evidence
than its cohort, never for being older than its cohort-mates. For a single-age cohort R_k is the value-weighted
mean of S_k over the cohort (the first act's Sbar); in the pooled veteran cohort it keeps a 37-year-old from
being charged against 33-year-olds' age.

CHARGED rows are the active rows with career games >= 1. A 0-game (never-played) row is EXCLUDED from the charge
and from R (m = 1) and carries NO fitted S (S1/S2 = null): its vP is a pick-curve expectation that already
averages over busts, and its listing outcome is not observable before the 2024/2025 list facts, so no S is
published for it. COHORTS are integer ages, with every age >= 33 pooled into one veteran cohort, and any age with
fewer than 5 charged rows joined to the nearest larger cohort below it (the lowest age with no cohort below
joins the first cohort above). Because the multiplier is capped the lens totals can only FALL — the application
is NOT sum-preserving. The present value v and the -1/-2 lenses are never touched; retired/back rows and phantom
picks are never touched. Applied at the EXPORT layer (rl_export.py), never inside ev().

S_k is the fitted age x evidence additive-logit survival on the TRUE listing outcome (fix plan F1), PLAYED rows:
    S_k(age, evidence) = P(on an AFL list at the END of season Y+k | listed at the END of base season Y with
                           career games >= 1, age at Y, career games through Y)
fitted by engine/rl_after/ingestion/fit_survival_hazard.py from the store's own history (the `_last_listed` list
facts of the AFL 2024/2025 list changes, active rows listed through 2026, the last played season as a proxy for
older retirees — the JSON's `outcome` states it exactly). Design (9 columns, data/survival_hazard.json `design`):
    [1, min(age,24)-24, (age-24)+, (age-29)+, (age-33)+, band6-20, band21-50, band51-100, band101+]
  * the reference band is 1-5 career games; 0-game records are NOT in the fit (they leaked into the age slopes);
  * monotone in evidence: S = min over band midpoints m >= g of S_raw(age, m), with S_raw(age, g) — a thinner
    band can never beat a thicker one at the same age.
The calibration lives in data/survival_hazard.json under the repo root (RL_REPO / CLAUDE_PROJECT_DIR, the
same resolution season_read.py uses) and the engine HALTS if it is absent — there is no fallback.

CAP_LIFT below is the ONE switch for the measurement variant. It is a module constant, not an environment
flag: the engine no longer takes kill-switches (docs/evidence/engine_chain_hardwired_single_reader_2026-10-14/
NOTE.md). The shipped default is the document's cap_lift (true).
"""
import os, json, math, hashlib
from season_read import repo_root

#: THE cap switch. None = take data/survival_hazard.json's `cap_lift` (true: the shipped capped rule). Flip to
#: False for a pure-H2 measurement build (multiplier S/R uncapped; sum-preserving to rounding within each
#: single-age cohort, not within a pooled cohort); the board's `survivalHazard.cap_lift` reports the value IN EFFECT.
CAP_LIFT = None

HAZARD_REL = ('data', 'survival_hazard.json')
RULING = 'SURVIVAL_H2_2026-10-14'
LENSES = ((1, 'S1'), (2, 'S2'))
N_COEF = 9
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
    """0..4 for games >= 1 (bands 1-5, 6-20, 21-50, 51-100, 101+)."""
    g = int(games)
    for i, (lo, hi) in enumerate(BANDS):
        if lo <= g and (hi is None or g <= hi):
            return i
    raise SurvivalHazardError('survival hazard: games=%r has no evidence band' % (games,))


def features(age, games):
    """The 9-column design row (fit_survival_hazard.py `design`); games >= 1."""
    a = float(age); b = band_index(games)
    return [1.0, min(a, 24.0) - 24.0, max(0.0, a - 24.0), max(0.0, a - 29.0), max(0.0, a - 33.0)] + \
           [1.0 if b == i else 0.0 for i in range(1, 5)]


def survival_raw(age, games, coef):
    z = sum(x * float(c) for x, c in zip(features(age, max(1, int(games))), coef))
    return 1.0 / (1.0 + math.exp(-z))


def survival(age, games, coef, midpoints=(3, 12, 35, 75, 180)):
    """S(age, g) for g >= 1, monotone in evidence: a thinner band can never beat a thicker one at the same age
    (min over the band midpoints m >= g)."""
    g = max(1, int(games))
    s = survival_raw(age, g, coef)
    if g <= max(midpoints):
        s = min(s, min(survival_raw(age, m, coef) for m in midpoints if m >= g))
    return s


def _check_row(row):
    age, games = row.get('age'), row.get('games')
    key = row.get('key', '?')
    if not isinstance(age, (int, float)) or isinstance(age, bool) or not math.isfinite(age) or int(age) != age or age < 15:
        raise SurvivalHazardError('survival hazard: %s has no usable age (%r); refusing to price the lens' % (key, age))
    if not isinstance(games, (int, float)) or isinstance(games, bool) or not math.isfinite(games) or int(games) != games or games < 0:
        raise SurvivalHazardError('survival hazard: %s has no usable career games (%r); refusing to price the lens' % (key, games))
    return int(age), int(games)


def survival_of(row, k, doc, base_year=None):
    """S_k for one row {age, games}; None for a 0-game row (no fitted S is published for it); halts when
    age/games cannot be formed."""
    age, games = _check_row(row)
    if games == 0:
        return None
    return survival(age, games, doc['coef']['S%d' % k], tuple(doc['band_midpoints']))


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
    """rows: list of dicts {key, age, games, vP1, vP2} (the ACTIVE board rows; ty/yr tolerated, unused). Returns
    (per_key, report): per_key[key] = {S1, S2, age, games, cohort, charged, ref1, ref2, m1, m2, vP1, vP2} with
    the NEW rounded lens values (S/ref None and m=1 on a 0-game row); report = the board-level `survivalHazard`
    block. Pure: never mutates `rows`. cap_lift None -> the module constant CAP_LIFT, itself None -> the
    document's cap_lift."""
    cap = CAP_LIFT if cap_lift is None else cap_lift
    if cap is None:
        cap = bool(doc['cap_lift'])
    cap = bool(cap)
    per = {}
    for r in rows:
        if r['key'] in per:
            raise SurvivalHazardError('survival hazard: duplicate active key %r' % r['key'])
        age, games = _check_row(r)
        per[r['key']] = {'age': age, 'games': games, 'charged': games >= 1}
        for k, nm in LENSES:
            per[r['key']][nm] = survival_of(r, k, doc)
    charged_count = {}
    for r in rows:
        if per[r['key']]['charged']:
            a = per[r['key']]['age']; charged_count[a] = charged_count.get(a, 0) + 1
    coh = cohorts_of(charged_count)
    members = {}
    for r in rows:
        c = coh.get(per[r['key']]['age'])
        per[r['key']]['cohort'] = c
        if per[r['key']]['charged']:
            members.setdefault(c, []).append(r)
    cohorts = {}; totals = {}
    for k, nm in LENSES:
        fld = 'vP%d' % k
        for r in rows:
            v = r.get(fld)
            if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v):
                raise SurvivalHazardError('survival hazard: %s has no %s (%r)' % (r['key'], fld, v))
        coef = doc['coef'][nm]; mids = tuple(doc['band_midpoints'])
        # R_k(age) per cohort: the cohort's evidence mix priced at that age (w_j = vP_j / sum vP over the
        # cohort's charged rows). For a single-age cohort this is the value-weighted mean of the rows' own S_k.
        ref = {}; cinfo = {}
        for c, mem in members.items():
            den = sum(float(r[fld]) for r in mem)
            ages = sorted(set(per[r['key']]['age'] for r in mem))
            ref[c] = {}
            for a in ages:
                ref[c][a] = (sum(float(r[fld]) * survival(a, per[r['key']]['games'], coef, mids) for r in mem) / den) if den > 0 else None
            own = (sum(float(r[fld]) * per[r['key']][nm] for r in mem) / den) if den > 0 else None
            n_z = sum(1 for r in rows if not per[r['key']]['charged'] and per[r['key']]['cohort'] == c)
            cinfo[c] = {'sbar': (round(own, 6) if own is not None else None),
                        'ref_by_age': {str(a): (round(x, 6) if x is not None else None) for a, x in ref[c].items()},
                        'n_charged': len(mem), 'n_zero_game': n_z, 'ages': ages, 'lens_sum': int(round(den))}
        cohorts[nm] = {c: cinfo[c] for c in sorted(cinfo, key=lambda c: cinfo[c]['ages'][0])}
        before = 0; after = 0; single_delta = 0
        for r in rows:
            v = r[fld]; p = per[r['key']]; c = p['cohort']
            rv = ref[c][p['age']] if (p['charged'] and c in ref) else None
            if rv is not None and rv > 0:
                m = p[nm] / rv
                if cap and m > 1.0:
                    m = 1.0
            else:
                m = 1.0
            nv = int(round(v * m))
            p['ref%d' % k] = (round(rv, 6) if rv is not None else None)
            p['m%d' % k] = round(m, 6)
            p[fld] = nv
            before += v; after += nv
            if p['charged'] and len(cinfo[c]['ages']) == 1:
                single_delta += nv - v
        totals['+%d' % k] = {'field': fld, 'before': int(round(before)), 'after': after, 'delta': after - int(round(before)),
                             'single_age_cohorts_delta': int(round(single_delta))}
    n = len(rows); n_charged = sum(1 for r in rows if per[r['key']]['charged'])
    n_single = sum(1 for r in rows if per[r['key']]['charged'] and len(cohorts['S1'][per[r['key']]['cohort']]['ages']) == 1)
    for lbl, t in totals.items():
        if cap:
            if t['after'] > t['before']:
                raise SurvivalHazardError('survival hazard: cap_lift=True but the %s total ROSE %d -> %d' % (lbl, t['before'], t['after']))
        elif abs(t['single_age_cohorts_delta']) > 0.5 * max(1, n_single):
            raise SurvivalHazardError('survival hazard: %s NOT preserved over the single-age cohorts (delta %+d exceeds the '
                                      'rounding bound %.1f on %d charged rows)' % (lbl, t['single_age_cohorts_delta'], 0.5 * n_single, n_single))
    report = {'ruling': doc['ruling'], 'source': os.path.relpath(doc['_path'], repo_root()) if doc.get('_path') else None,
              'source_md5': doc.get('_md5'), 'cap_lift': cap, 'cap_lift_recorded': bool(doc['cap_lift']),
              'base_year': base_year, 'nActive': n, 'nCharged': n_charged, 'nZeroGame': n - n_charged,
              'design': doc.get('design'), 'outcome': doc.get('outcome'),
              'cohort_of_age': {str(a): c for a, c in sorted(coh.items())}, 'sbar_by_cohort': cohorts, 'totals': totals,
              'law': ('vP_k = round(vP_k x min(1, S_k(age_i,g_i) / R_k(age_i))) over the charged rows (games >= 1); R_k(age_i) = '
                      'sum_j w_j S_k(age_i, g_j) over the charged rows j of i\'s cohort, w_j = vP_j / sum vP (the cohort\'s evidence '
                      'mix at the row\'s own age; = the value-weighted mean of S_k for a single-age cohort). Cohorts: integer ages, '
                      '>= %d pooled, < %d charged rows joins the cohort below; 0-game rows carry no S and are not charged; the cap '
                      'means the totals can only fall (not sum-preserving)' % (POOL_FROM, MIN_CHARGED)) if cap else
                     ('vP_k = round(vP_k x S_k(age_i,g_i) / R_k(age_i)) over the charged rows (pure H2 measurement variant: '
                      'sum-preserving to rounding within each single-age cohort)'),
              'untouched': 'v, vM1, vM2, 0-game active rows, back rows, phantom picks', 'applied_at': 'export layer (rl_export.py), not ev()'}
    return per, report
