"""L1 — YOUNG-GDEF TRANSITION CREDIT: derive the transition-anchored expected-rerating replacement for
the GEN_DEF rows of ycred_table.json (the v2.6 L1c family; engine formula/code UNTOUCHED).

OWNER DIAGNOSIS (canonical, directive 2026-07-11): established GDEFs price FAIRLY; young GDEFs are NOT
priced as a genuine chance of becoming the established GDEFs already on this board. MECHANISM: per
young-GDEF cell, STRENGTHEN the credit by the measured TERMINAL-EXPECTATION GAP — the difference
between the transition expectation (chance x the board's own demonstrated established-GDEF outcomes)
and the engine's own expected value at the establishment horizon, discounted at the board's live lens:
    R_new(T, pick, row) = R_shipped(T, pick, row)
                        + DF_T * max(0, E_term_T(pick) - VD_T(pick)) / V1_T(pick)
    E_term_T(pick) = P_T(pick) * PRIZE_T(pick) + (1 - P_T(pick)) * WASH_T(pick)
Additive, non-negative: strengthen, never weaken; the sat/played row structure is preserved; the
engine's clip R >= 0 and phi fade are untouched. WHY the gap (not a ratio): the credit multiplies the
engine's CURRENT full-path price e; the engine's path already carries the interim years AND its own
(near-empty-sample-extrapolated) terminal view VD — the honest correction is exactly the measured
terminal difference, PV'd. A terminal-only/V1 ratio was prototyped and REJECTED as structurally biased
(it compares a terminal-only expectation against a full-path price; census carries the prototype).
All quantities measured on the CREDIT-OFF (RL_YOUNG=0) walk-forward as-of matrix regenerated on THIS
candidate (store 04f38dad) + the pinned store:
  P_T(pick)     = probability a GDEF ND/RD entrant ESTABLISHES — cumulative career games >= G0=46
                  (the credit's own evidence-complete boundary) within the first 6 seasons — measured
                  attrition-inclusive on classes with a FULLY OBSERVABLE window (C+6 <= T), kernel-
                  smoothed on log-pick (EFFN=35 adaptive bandwidth, the D14/derive_ycred convention).
  PRIZE_T(pick) = the DEMONSTRATED outcome anchor: the as-of-T board's OWN established GDEFs (cpos
                  GEN_DEF, ND, picked, cum games >= 46 by T, ACTIVE at T, age at T <= 26 — the
                  just-matured state a transition lands on), their as-of-T engine values, smoothed by
                  a FIXED-BANDWIDTH 0.6 log-pick Gaussian kernel — THE SUITE'S OWN pick-matching
                  convention (the A6 gate kernel, bw 0.6 log-pick) — then projected MONOTONE
                  NON-INCREASING in pick (PAVA, draft-market coherence). DECLARED CHOICE, both
                  alternatives prototyped and committed as sensitivity: (a) adaptive EFFN kernels
                  (6/8/12) dilute the near-empty top-pick anchor toward the all-pick mean (~2100 at
                  pick 2 vs demonstrated 5187/3598 at picks 4/10), defeating the ruled anchor;
                  (b) isotonic-on-raw-points carries a one-player CLIFF at picks 4->5
                  (ash 5187 vs braeden-campbell ~900), violating the binding continuity law. The
                  fixed-0.6 kernel keeps the demonstrated top-end local (ash/campbell/blakey all
                  weighted at top picks) while staying continuous on the pick axis.
  WASH_T(pick)  = the measured washout residual: non-establishers' value at C+6 (0 if the path ended —
                  attrition included), EFFN=35 kernel. Measured ~0-70.
  VD_T(pick)    = the engine's OWN expected value at the establishment horizon: kernel class-sum mean
                  of Vpath[Dmed-1] over the fully-observable pool, attrition-inclusive (ended path
                  contributes 0) — what the credit-off engine already believes a year-1 entrant
                  becomes by year Dmed.
  DF_T          = (1 + 0.15)^(-Dmed_T): the prize arrives Dmed_T years out (measured median
                  years-to-establishment), discounted at the board's OWN live lens LENS['bal']=0.15 —
                  NO lens change; the lens is read, not written. DF=1 sensitivity committed (the
                  owner's undiscounted no-arbitrage lens; informs, not shipped).
  V1_T(pick)    = the cell's year-1-anchor kernel mean on the credit-off matrix (classes C+2 <= T,
                  Vpath[0]) — the per-cell-dollar normalizer the multiplicative credit needs.
                  Cross-year currency comparability verified (era means 371/448/440/454 at picks
                  15-60 — stable).

TRAILING / LEAK-FREE (auditor: assert by code reading): table_T reads ONLY data visible at T —
P-pool classes C+6 <= T; V1-pool classes C+2 <= T; PRIZE/WASH from as-of-<=T matrix values (the
walk-forward matrix prices year Y with scoring truncated <= Y, so Vpath[i] at calendar year C+1+i is
as-of that year); Dmed from the T-visible establishers. Years T < T_FIRST (< 2 observable classes or
< 3 prize members) keep the SHIPPED rows byte-identical — declared conservatism, same law as the
L1c pre-2007 zero-credit rule.

HARD CONSTRAINTS (enforced + asserted here):
  - ONLY GEN_DEF rows move; every other (year x pos x sat/played) cell asserted BYTE-IDENTICAL.
  - Replacement bars untouched (no REPL edit anywhere in this lever).
  - Established-GDEF prices untouched BY CONSTRUCTION: the engine consults this table only through
    _ycred_mult, which returns 1.0 for g >= G0=46 (evidence complete) — code-read assertion; a named
    zero-mover check on the established set rides the L1-only board artifact.
  - No blanket young multiplier: GEN_DEF-cell-only, pick-conditioned, evidence-fading (phi unchanged).
  - Raise-only vs shipped (max), and the engine's own clip R >= 0 still applies.

Ships: engine/rl_after/ycred_table.json (GEN_DEF rows replaced for T >= T_FIRST) +
       session_2026-07-11/chapter_levers/out/ycred_gdef_transition_census.json (every measured
       quantity, pools, sensitivity) — sizes come OUT of the measurement; no number targeted.
Usage: python3 derive_ycred_gdef_transition.py <s4_matrix_youngoff.json>
"""
import json, os, sys, statistics
import numpy as np

HERE = '/home/user/afl-rl-engine'
OUT = f'{HERE}/session_2026-07-11/chapter_levers/out'
MAT = sys.argv[1]

sys.path.insert(0, HERE)
import boot_guard
boot_guard.assert_boot('derive_ycred_gdef_transition', store_path=f'{HERE}/engine/rl_after/rl_model_data.json')

mat = json.load(open(MAT))
meta = mat.get('__meta__', {})
assert meta.get('store_md5', '')[:8] == '04f38dad', f"credit-off matrix store {meta.get('store_md5')} != candidate 04f38dad"
store = {p['key']: p for p in json.load(open(f'{HERE}/engine/rl_after/rl_model_data.json')) if p.get('key')}
recs = [v for k, v in mat.items() if not k.startswith('__')]

G0 = 46.0; WINDOW = 6; LENS_BAL = 0.15
EFFN, H0, HMAX = 35.0, 0.18, 2.6          # derive_ycred / D14 convention
EFFN_PRIZE = 8.0                           # small-pool locality target (declared; sensitivity below)
GRIDPK = list(range(1, 91)); LGRID = np.log(np.array(GRIDPK, dtype=float))

def _by(k):
    p = store.get(k); return p.get('_by') if p else None

def cumg_to(key, C, yr):
    p = store.get(key)
    return sum(x.get('games', 0) for x in (p.get('scoring') or []) if C + 1 <= x['year'] <= yr) if p else 0

def est_year(v):
    """career-year k (1..WINDOW) at which cumulative games first reach G0, else None (washout)."""
    C = v['year']
    for k in range(1, WINDOW + 1):
        if cumg_to(v['key'], C, C + k) >= G0:
            return k
    return None

def lp_of(pk): return float(np.log(min(max(pk, 1), 90)))

def kern_curve(pts, vals, effn=EFFN):
    """adaptive-bandwidth Gaussian kernel mean of vals over log-pick pts, on the grid."""
    lx = np.asarray(pts, dtype=float); a = np.asarray(vals, dtype=float)
    grid = []; mineff = 1e9
    for lg in LGRID:
        h = H0
        while True:
            w = np.exp(-0.5 * ((lx - lg) / h) ** 2); sw = w.sum()
            eff = (sw * sw) / float(np.sum(w * w)) if sw > 0 else 0.0
            if eff >= effn or h >= HMAX:
                break
            h *= 1.15
        mineff = min(mineff, eff)
        grid.append(float(np.dot(w, a) / sw) if sw > 0 else 0.0)
    return np.array(grid), mineff

def pava_noninc(y):
    """isotonic NON-INCREASING projection (PAVA) — draft-market coherence for the prize curve."""
    y = list(-np.asarray(y, dtype=float))    # solve non-decreasing on the negation
    n = len(y)
    vals = []; ws = []
    for v in y:
        vals.append(v); ws.append(1.0)
        while len(vals) >= 2 and vals[-2] > vals[-1]:
            v2, w2 = vals.pop(), ws.pop(); v1, w1 = vals.pop(), ws.pop()
            vals.append((v1 * w1 + v2 * w2) / (w1 + w2)); ws.append(w1 + w2)
    res = []
    for v, w in zip(vals, ws):
        res.extend([v] * int(round(w)))
    return -np.asarray(res[:n])

# ---- pools per trailing year T ----
gdent = [v for v in recs if v['cpos'] == 'GEN_DEF' and v['incurve'] and not v.get('pickless')
         and v.get('pick') and v.get('year') and v['year'] >= 2004]
EY = {v['key']: est_year(v) for v in gdent}

shipped = json.load(open(f'{HERE}/engine/rl_after/ycred_table.json'))
newtab = json.loads(json.dumps(shipped))    # deep copy
census = {'doc': __doc__, 'pools': {}, 'rows': {}, 'sensitivity': {}, 'T_first': None}

for T in sorted(int(t) for t in shipped['table']):
    tab_T = newtab['table'][str(T)]
    # P-pool: fully observable windows
    ppool = [v for v in gdent if v['year'] + WINDOW <= T]
    # prize pool: as-of-T active established ND GEN_DEF age<=26 (as-of-T values)
    prize = []
    for v in recs:
        if v['cpos'] != 'GEN_DEF' or v.get('pickless') or not v.get('pick') or v.get('type') != 'ND' or v.get('year') is None:
            continue
        b = _by(v['key'])
        if not b or T - b > 26 or T not in v.get('yrs', []):
            continue
        if cumg_to(v['key'], v['year'], T) < G0:
            continue
        val = v['Vpath'][v['yrs'].index(T)]
        if val:
            prize.append((lp_of(v['pick']), float(val), v['key']))
    if len({v['year'] for v in ppool}) < 2 or len(prize) < 3:
        continue                                             # keep shipped rows (declared conservatism)
    if census['T_first'] is None:
        census['T_first'] = T
    v1pool = [v for v in gdent if v['year'] + 2 <= T and len(v['Vpath']) > 0 and v['Vpath'][0]]
    wash = [(lp_of(v['pick']), float(v['Vpath'][WINDOW - 1]) if len(v['Vpath']) > WINDOW - 1 and v['Vpath'][WINDOW - 1] else 0.0)
            for v in ppool if not EY[v['key']]]
    dm = statistics.median([EY[v['key']] for v in ppool if EY[v['key']]])
    DF = (1.0 + LENS_BAL) ** (-dm)

    Pg, effP = kern_curve([lp_of(v['pick']) for v in ppool], [1.0 if EY[v['key']] else 0.0 for v in ppool])
    Pg = np.clip(Pg, 0.0, 1.0)
    V1g, effV = kern_curve([lp_of(v['pick']) for v in v1pool], [float(v['Vpath'][0]) for v in v1pool])
    Wg, _ = kern_curve([a for a, _ in wash], [b for _, b in wash]) if wash else (np.zeros(len(GRIDPK)), 0)
    di = max(1, int(dm))
    VDg, _ = kern_curve([lp_of(v['pick']) for v in ppool],
                        [float(v['Vpath'][di-1]) if len(v['Vpath']) > di-1 and v['Vpath'][di-1] else 0.0 for v in ppool])
    # PRIZE (ships): fixed-bw 0.6 log-pick kernel (the A6 convention) + PAVA; variants = sensitivity
    plx = np.array([a for a, _, _ in prize]); pv = np.array([b for _, b, _ in prize])
    PR_raw = []
    for lg in LGRID:
        w = np.exp(-0.5 * ((plx - lg) / 0.6) ** 2)
        PR_raw.append(float(np.dot(w, pv) / w.sum()))
    PR = pava_noninc(PR_raw)
    prz_sorted = sorted(prize, key=lambda t: t[0])
    iso_vals = pava_noninc([b for _, b, _ in prz_sorted])
    iso_lp = np.array([a for a, _, _ in prz_sorted])
    PR_isoraw = np.interp(LGRID, iso_lp, iso_vals, left=float(iso_vals[0]), right=float(iso_vals[-1]))
    PRg = {}
    for effp in (6.0, EFFN_PRIZE, 12.0):
        g, _ = kern_curve([a for a, _, _ in prize], [b for _, b, _ in prize], effn=effp)
        PRg[effp] = pava_noninc(g)
    Eterm = Pg * PR + (1.0 - Pg) * Wg
    gap = np.maximum(Eterm - VDg, 0.0) * DF / np.maximum(V1g, 1e-9)
    old0 = np.array(tab_T['GEN_DEF']['0'], dtype=float); old1 = np.array(tab_T['GEN_DEF']['1'], dtype=float)
    tab_T['GEN_DEF']['0'] = [round(float(x), 4) for x in old0 + gap]
    tab_T['GEN_DEF']['1'] = [round(float(x), 4) for x in old1 + gap]

    census['pools'][T] = dict(n_P=len(ppool), n_classes=len({v['year'] for v in ppool}), n_prize=len(prize),
                              n_V1=len(v1pool), n_wash=len(wash), Dmed=dm, DF=round(DF, 4),
                              prize_members=[k for _, _, k in sorted(prize, key=lambda t: -t[1])] if T == 2026 else len(prize))
    reps = {pk: dict(P=round(float(Pg[pk-1]), 3), prize=round(float(PR[pk-1])), V1=round(float(V1g[pk-1])),
                     VD=round(float(VDg[pk-1])), wash=round(float(Wg[pk-1])), Eterm=round(float(Eterm[pk-1])),
                     gap_credit=round(float(gap[pk-1]), 3),
                     R_shipped_played=round(float(old0[pk-1]), 3), R_shipped_sat=round(float(old1[pk-1]), 3),
                     R_new_played=round(float(old0[pk-1] + gap[pk-1]), 3), R_new_sat=round(float(old1[pk-1] + gap[pk-1]), 3))
            for pk in (1, 2, 3, 5, 8, 12, 21, 30, 50, 70)}
    census['rows'][T] = reps
    if T == 2026:
        census['sensitivity'] = {
            **{f'prize_kernel_adaptive_EFFN={int(e)}': {pk: round(float(PRg[e][pk-1])) for pk in (2, 5, 8, 21, 50)} for e in PRg},
            'prize_fixedbw06_pava_SHIPPED': {pk: round(float(PR[pk-1])) for pk in (2, 5, 8, 21, 50)},
            'prize_isotonic_on_raw_REJECTED_cliff': {pk: round(float(PR_isoraw[pk-1])) for pk in (2, 5, 8, 21, 50)},
            'gap_credit_undiscounted_DF1': {pk: round(float(np.maximum(Eterm[pk-1]-VDg[pk-1], 0.0)/max(V1g[pk-1], 1e-9)), 3) for pk in (2, 5, 8, 21, 50)},
        }
        census['establishment_rate_overall'] = round(sum(1 for v in ppool if EY[v['key']]) / max(1, len(ppool)), 3)

# ---- byte-identity assertion: nothing but GEN_DEF rows moved ----
for T in shipped['table']:
    for pos in shipped['table'][T]:
        if pos == 'GEN_DEF':
            continue
        assert json.dumps(shipped['table'][T][pos], sort_keys=True) == json.dumps(newtab['table'][T][pos], sort_keys=True), \
            f'NON-GEN_DEF CELL MOVED: {T}/{pos} — HALT'
for k in shipped:
    if k != 'table':
        assert json.dumps(shipped[k], sort_keys=True) == json.dumps(newtab[k], sort_keys=True), f'top-level {k} moved'
changed = sum(1 for T in shipped['table']
              if json.dumps(shipped['table'][T]['GEN_DEF']) != json.dumps(newtab['table'][T]['GEN_DEF']))
newtab['doc'] = shipped.get('doc', '') + (' || GEN_DEF rows REPLACED by the transition-anchored expected-rerating '
    '(chapter-lever L1, 2026-07-11): R_new = max(R_transition, R_shipped); derivation + census: '
    'session_2026-07-11/chapter_levers/ (derive_ycred_gdef_transition.py). All other cells byte-identical.')

json.dump(newtab, open(f'{HERE}/engine/rl_after/ycred_table.json', 'w'))
json.dump(census, open(f'{OUT}/ycred_gdef_transition_census.json', 'w'), indent=1)
print(f"T_first={census['T_first']}  GEN_DEF row-years changed: {changed}/{len(shipped['table'])}")
r26 = census['rows'][2026]
print(f"{'pick':>4} {'P':>5} {'prize':>6} {'VD':>6} {'V1':>6} {'gap+':>6} {'R_sat':>12} {'R_played':>15}")
for pk in (1, 2, 3, 5, 8, 12, 21, 30, 50, 70):
    r = r26[pk]
    print(f"{pk:>4} {r['P']:5.2f} {r['prize']:6d} {r['VD']:6d} {r['V1']:6d} {r['gap_credit']:+6.2f} "
          f"{r['R_shipped_sat']:+5.2f}->{r['R_new_sat']:+5.2f} {r['R_shipped_played']:+6.2f}->{r['R_new_played']:+5.2f}")
print('sensitivity (prize at EFFN 6/8/12):', json.dumps(census['sensitivity']))
print(f"wrote engine/rl_after/ycred_table.json + {OUT}/ycred_gdef_transition_census.json")
