"""#279 — the RULED curve (structural basis, class cut <=2022, VOR) + the truncation backtest,
the sealed reversal check, and the step-3 alpha-dial evidence pack.

RULINGS IN FORCE HERE
  gamma  = 1.0 (VOR), owner word 2026-07-30
  basis  = STRUCTURAL (completion over presumption), owner word 2026-07-30
  class  = HARD CUT at 2022 -- the 2022 draft class is the last that teaches; 2023/24/25 are OUT
  alpha  = PARKED at 1.0 for the ruled curve. The dial settings below are EVIDENCE ONLY.
  par    = per-season teaching, executing inside step 4's propagation (not here)

The fit machinery is carried verbatim from #271 -- pava_ni / monotone_strict / the pick-distance kernel,
tau, nmin, PW_FLOOR, pin(1)=3000, the priors window. The ONLY deliberate departures, both owner-ruled and
disclosed: the class cut moves the teaching window's upper bound 2024 -> 2022, and the year-0 contribution
is the structural completed career value.

alpha enters as a CERTAINTY-EQUIVALENT aggregator replacing the kernel-weighted MEAN inside the year-0 fit:
    CE_alpha = ( sum(W * v^alpha) / sum(W) ) ^ (1/alpha)
which is the kernel-weighted generalisation of the engine's own `_ce0` (rl_model.py:815 -- busts floored at
0.0, NOT the legacy `_ce`'s floor of 1.0, whose own comment calls that floor wrong for busts). alpha=1
returns the mean exactly, so alpha=1 reproduces the ruled curve by construction. The tiered candidate is the
engine's own `_alpha_pvc(k) = 0.6 + (0.8-0.6)*min(k-1,49)/49` -- 0.6 at pick 1 rising to 0.8 by pick 50,
flat thereafter.
"""
import os, sys, json, time, math, hashlib, collections
import numpy as np

VOR_MATRIX, SCAR_MATRIX, DERIVE, OUTDIR = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
CLASS_CUT = int(os.environ.get('CLASS_CUT', '2022'))

os.environ.setdefault('CURVE_STATISTIC', 'VOR')
_src = open(DERIVE).read()
G = {'__name__': '_ruled', '__file__': os.path.abspath(DERIVE)}
exec(_src.split('def main(')[0], G)
PW_FLOOR = G['PW_FLOOR']; TAU = G['TAU']; PIN1 = G['PIN1']
NMIN = G['NMIN']; HMIN, HMAX = G['HMIN'], G['HMAX']
YR_LO = G['YR_LO']; ND_LAST = G['ND_CURVE_LAST']
monotone_strict = G['monotone_strict']; never_established = G['never_established']
realised = G['realised_scar']

MIN_STRATUM = 20

def load(mx):
    M = json.load(open(mx))
    ND = [r for r in M['recs'] if r.get('teaches_curve') and r.get('pick')
          and 1 <= r['pick'] <= ND_LAST and YR_LO <= r['year'] <= CLASS_CUT]
    assert ND, "EMPTY ND population after the class cut"
    return M['meta'], ND

def concluded(r): return bool(r.get('retired_now'))
def depth(r): return sum(1 for v in (r.get('vpath') or []) if v is not None)

def realised_at(r, t):
    pw = r.get('pw', {}); vp = r.get('vpath') or []
    num = den = 0.0
    for k in range(1, min(t, len(vp)) + 1):
        v = vp[k - 1]
        if v is None: continue
        pwk = pw.get(str(k), pw.get(str(min(k, 6))))
        if pwk is None: pwk = 1.0
        es = max(0.0, 1.0 - (pwk - PW_FLOOR) / (1.0 - PW_FLOOR))
        if es <= 0: continue
        num += es * v; den += es
    return float(num / den) if den > 0 else 0.0

def full_realised(r): return 0.0 if never_established(r) else realised(r)
def sofar(r, t): return 0.0 if never_established(r) else realised_at(r, t)

# ---- completion table, with running sums so leave-one-out is exact ----
def completion_sums(pop):
    S = collections.defaultdict(lambda: [0.0, 0.0, 0])   # key -> [sum_full, sum_sofar, n]
    for r in pop:
        if not concluded(r): continue
        T = depth(r)
        if T <= 0: continue
        f = full_realised(r)
        for t in range(1, T + 1):
            e = S[(r['pos'], t)]
            e[0] += f; e[1] += sofar(r, t); e[2] += 1
    return S

def ratio_from(S, key, exclude=None):
    """Stratum ratio mean(full)/mean(sofar); exclude removes one member's contribution (LOO)."""
    if key not in S: return None, 0
    sf, ss, n = S[key]
    if exclude is not None:
        f, s = exclude
        sf -= f; ss -= s; n -= 1
    if n < MIN_STRATUM or ss <= 0: return None, n
    return (sf / n) / (ss / n), n

def structural_values(pop, S, stats):
    """One year-0 value per entrant. Fallback share is COUNTED and returned, never silent."""
    out = []
    for r in pop:
        if concluded(r):
            stats['concluded_realised'] += 1
            out.append((r['pick'], full_realised(r))); continue
        T = depth(r)
        if T <= 0:
            stats['prior_fallback_no_written'] += 1
            out.append((r['pick'], float(r['v0']))); continue
        rt, n = ratio_from(S, (r['pos'], T))
        if rt is None:
            stats['prior_fallback_thin'] += 1
            out.append((r['pick'], float(r['v0']))); continue
        stats['completed'] += 1
        out.append((r['pick'], sofar(r, T) * rt))
    return out

# ---- the fit: pick-distance kernel carried verbatim, aggregator swapped for the CE ----
def fit_ce(vals, alpha_fn):
    lp = np.array([math.log(k) for k, _ in vals], float)
    v = np.array([max(x, 0.0) for _, x in vals], float)     # _ce0 semantics: busts floored at 0.0
    grid = list(range(1, ND_LAST + 1))
    raw, effn = [], []
    for p in grid:
        Lp = math.log(p); h = HMIN
        while h < HMAX:
            if np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2)) >= NMIN: break
            h += 0.02
        W = np.exp(-0.5 * ((lp - Lp) / h) ** 2)
        al = alpha_fn(p)
        if abs(al - 1.0) < 1e-12:
            r = float(np.sum(W * v) / np.sum(W))
        else:
            r = float((np.sum(W * np.power(v, al)) / np.sum(W)) ** (1.0 / al))
        raw.append(r); effn.append(float(np.sum(np.exp(-0.5 * ((lp - Lp) / h) ** 2))))
    return grid, np.array(raw), np.array(effn)

def pin(grid, raw, effn):
    mono = monotone_strict(grid, raw, effn)
    s = PIN1 / mono[0] if mono[0] else 1.0
    out = [max(1, int(round(c * s))) for c in mono]
    forced = []
    for i in range(1, len(out)):
        if out[i] >= out[i - 1]: forced.append(i + 1); out[i] = out[i - 1] - 1
    return out, s, forced, mono

def payload(ci):
    return hashlib.md5(json.dumps({str(i + 1): v for i, v in enumerate(ci)},
                                  sort_keys=True).encode()).hexdigest()[:8]

ALPHAS = {'0.6': (lambda k: 0.6), '0.8': (lambda k: 0.8), '1.0': (lambda k: 1.0),
          'tiered_0.6_to_0.8_by_50': (lambda k: 0.6 + (0.8 - 0.6) * min(k - 1, 49) / 49.0)}

RES = {'rulings': {'gamma': '1.0 VOR (owner 2026-07-30)', 'basis': 'STRUCTURAL (owner 2026-07-30)',
                   'class_cut': CLASS_CUT, 'alpha_parked_at': 1.0,
                   'par': 'per-season teaching, executes in step 4 propagation — NOT here'},
       'carried_verbatim': ['pava_ni', 'monotone_strict', 'pick-distance kernel', 'tau', 'nmin',
                            'PW_FLOOR', 'pin(1)=3000'],
       'disclosed_departures': ['teaching window upper bound 2024 -> %d (owner class cut)' % CLASS_CUT,
                                'year-0 contribution is the structural completed career value']}

# ================= 1. THE RULED CURVE (VOR, structural, <=cut, alpha=1) =================
t0 = time.time()
metaV, NDV = load(VOR_MATRIX)
SV = completion_sums(NDV)
stV = collections.Counter()
valsV = structural_values(NDV, SV, stV)
gridV, rawV, effnV = fit_ce(valsV, ALPHAS['1.0'])
ruled, sV, forcedV, monoV = pin(gridV, rawV, effnV)
t_ruled = time.time() - t0

nV = len(NDV)
fb = stV['prior_fallback_thin'] + stV['prior_fallback_no_written']
assert stV['concluded_realised'] + stV['completed'] + fb == nV, "provenance counts do not sum to population"
assert 0.0 <= fb / nV <= 1.0
RES['ruled_curve'] = {
 'seconds': round(t_ruled, 3), 'matrix': os.path.basename(VOR_MATRIX),
 'store_md5': metaV['store_md5'], 'v0surf_sig': metaV['v0surf_sig'][:12],
 'v0surf_frozen': metaV.get('v0surf_frozen'),
 'population': {'n': nV, 'window': [YR_LO, CLASS_CUT],
                'concluded': sum(1 for r in NDV if concluded(r)),
                'active': sum(1 for r in NDV if not concluded(r)),
                'never_established': sum(1 for r in NDV if never_established(r))},
 'FALLBACK_SHARE': {'prior_fallback_rows': fb, 'of_population': nV,
                    'share_pct': round(100.0 * fb / nV, 3),
                    'thin_stratum': stV['prior_fallback_thin'],
                    'no_written_seasons': stV['prior_fallback_no_written'],
                    'asserted': 'counts sum to population; share in [0,1]'},
 'provenance': dict(stV), 'payload': payload(ruled), 'ladder_total': int(sum(ruled)),
 'pin_scale': round(sV, 6), 'forced_by_descent_enforcement': forcedV,
 'raw_monotone_violations': int(sum(1 for i in range(1, ND_LAST) if rawV[i] >= rawV[i - 1])),
 'curve': {str(k): ruled[k - 1] for k in (1, 2, 3, 5, 10, 24, 32, 40, 50, 57, 64)},
 'effn': {str(k): round(float(effnV[k - 1]), 1) for k in (1, 2, 3, 10, 24, 40, 64)}}

# ================= 2. TRUNCATION BACKTEST (report-only, rides the seal) =================
bt = {'design': 'on CONCLUDED careers only: truncate the career to d written seasons, apply the structural '
                'completion with the player LEFT OUT of his own stratum, and compare against his ACTUAL full '
                'realised value. Leave-one-out, so no self-prediction.',
      'status': 'REPORT-ONLY seal evidence. Not a guard. Does not re-open the class cut.',
      'by_written_depth': {}}
for d in (2, 3, 4):
    errs = []; rel = []
    for r in NDV:
        if not concluded(r): continue
        T = depth(r)
        if T <= d: continue                      # need genuinely unwritten remainder to predict
        key = (r['pos'], d)
        rt, n = ratio_from(SV, key, exclude=(full_realised(r), sofar(r, d)))
        if rt is None: continue
        pred = sofar(r, d) * rt
        act = full_realised(r)
        errs.append(pred - act)
        if act > 0: rel.append((pred - act) / act)
    if not errs: bt['by_written_depth'][str(d)] = {'n': 0, 'note': 'no evaluable rows'}; continue
    e = np.array(errs); rl = np.array(rel) if rel else np.array([0.0])
    bt['by_written_depth'][str(d)] = {
        'n': len(errs), 'n_with_positive_actual': len(rel),
        'median_signed_error': round(float(np.median(e)), 1),
        'mean_signed_error': round(float(np.mean(e)), 1),
        'median_abs_error': round(float(np.median(np.abs(e))), 1),
        'p90_abs_error': round(float(np.percentile(np.abs(e), 90)), 1),
        'median_relative_error_pct': round(100 * float(np.median(rl)), 2),
        'median_abs_relative_error_pct': round(100 * float(np.median(np.abs(rl))), 2),
        'bias_direction': 'over-predicts' if float(np.median(e)) > 0 else 'under-predicts'}
RES['truncation_backtest'] = bt

# ================= 3. SEALED REVERSAL CHECK: SCAR endpoint under the ruled basis =================
t0 = time.time()
metaS, NDS = load(SCAR_MATRIX)
SS = completion_sums(NDS)
stS = collections.Counter()
valsS = structural_values(NDS, SS, stS)
gridS, rawS, effnS = fit_ce(valsS, ALPHAS['1.0'])
scar, sS, forcedS, monoS = pin(gridS, rawS, effnS)
t_rev = time.time() - t0
nS = len(NDS); fbS = stS['prior_fallback_thin'] + stS['prior_fallback_no_written']
assert stS['concluded_realised'] + stS['completed'] + fbS == nS
band = [(1, 3), (4, 7), (8, 12), (13, 20), (21, 27), (28, 35), (36, 48), (49, 64)]
RES['reversal_check'] = {
 'seconds': round(t_rev, 3),
 'question': 'under the RULED basis (structural, <=%d), does the currency choice still favour VOR?' % CLASS_CUT,
 'scar': {'matrix': os.path.basename(SCAR_MATRIX), 'store_md5': metaS['store_md5'],
          'v0surf_sig': metaS['v0surf_sig'][:12], 'v0surf_frozen': metaS.get('v0surf_frozen'),
          'payload': payload(scar), 'ladder_total': int(sum(scar)),
          'FALLBACK_SHARE': {'prior_fallback_rows': fbS, 'of_population': nS,
                             'share_pct': round(100.0 * fbS / nS, 3)},
          'population_n': nS},
 'vor': {'payload': payload(ruled), 'ladder_total': int(sum(ruled)), 'population_n': nV},
 'ladder_ratio_vor_over_scar': round(sum(ruled) / sum(scar), 4),
 'by_band_vor_over_scar': [{'band': '%d-%d' % (lo, hi),
     'scar': int(sum(scar[k - 1] for k in range(lo, hi + 1))),
     'vor': int(sum(ruled[k - 1] for k in range(lo, hi + 1))),
     'ratio': round(sum(ruled[k - 1] for k in range(lo, hi + 1)) /
                    sum(scar[k - 1] for k in range(lo, hi + 1)), 4)} for lo, hi in band],
 'by_pick_vor_over_scar': {str(k): round(ruled[k - 1] / scar[k - 1], 4)
                           for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
 'steepness_pick1_over_pick64': {'scar': round(scar[0] / scar[63], 3),
                                 'vor': round(ruled[0] / ruled[63], 3)}}
RES['reversal_check']['verdict_inputs'] = {
 'vor_still_steepens_the_curve': RES['reversal_check']['steepness_pick1_over_pick64']['vor'] >
                                 RES['reversal_check']['steepness_pick1_over_pick64']['scar'],
 'head_ratio_ge_tail_ratio': RES['reversal_check']['by_band_vor_over_scar'][0]['ratio'] >
                             RES['reversal_check']['by_band_vor_over_scar'][-1]['ratio']}

# ================= 4. STEP-3 ALPHA DIAL EVIDENCE (alpha still parked at 1.0) =================
honest_mean_total = float(np.sum(rawV))          # alpha=1 raw fit = the honest mean at each pick
alpha_pack = {'note': 'EVIDENCE ONLY — alpha remains parked at 1.0 until the owner rules the schedule.',
 'ce_form': 'CE_alpha = (sum(W*v^alpha)/sum(W))^(1/alpha), the kernel-weighted generalisation of the '
            'engine\'s own _ce0 (busts floored at 0.0, per its comment that the legacy _ce floor of 1.0 is '
            'wrong for busts)',
 'tiered_form': "the engine's own _alpha_pvc(k) = 0.6 + (0.8-0.6)*min(k-1,49)/49",
 'conservation_yardstick': {
    'definition': 'ladder total (post-pin, picks 1-64) vs total mean production over the same picks, in the '
                  'same board units. The mean-production total is the alpha=1 RAW fit summed over 1-64 — the '
                  'honest mean, busts at full weight (S-3).',
    'total_mean_production_board_units': round(honest_mean_total, 1)},
 'settings': {}}
for name, fn in ALPHAS.items():
    g, rw, ef = fit_ce(valsV, fn)
    ci, sc, forced, mono = pin(g, rw, ef)
    raw_sum = float(np.sum(rw))
    hm_tail = float(np.sum(rawV[1:]))          # honest mean over picks 2-64 (the pin cannot touch these)
    alpha_pack['settings'][name] = {
        'raw_ladder_pre_pin': round(raw_sum, 1),
        'raw_vs_honest_mean_pct': round(100 * (raw_sum / honest_mean_total - 1), 3),
        'raw_at_pick1': round(float(rw[0]), 1),
        'pinned_pick1': ci[0],
        'pin_lift_on_pick1': round(PIN1 / float(rw[0]), 4),
        'ladder_2_to_64': int(sum(ci[1:])),
        'ladder_2_to_64_vs_honest_mean_pct': round(100 * (sum(ci[1:]) / hm_tail - 1), 3),
        'PICK_CLASS_PRICE_vs_numeraire': round(sum(ci[1:]) / ci[0], 4),
        'post_pin_ladder_total': int(sum(ci)), 'payload': payload(ci),
        'CONSERVATION_ratio_ladder_over_mean_production': round(sum(ci) / honest_mean_total, 4),
        'forced_by_descent_enforcement': len(forced),
        'raw_monotone_violations': int(sum(1 for i in range(1, ND_LAST) if rw[i] >= rw[i - 1])),
        'curve': {str(k): ci[k - 1] for k in (1, 2, 3, 10, 24, 32, 40, 50, 57, 64)},
        'vs_alpha1_ratio': None}
a1 = alpha_pack['settings']['1.0']
for name in alpha_pack['settings']:
    s = alpha_pack['settings'][name]
    s['vs_alpha1_ratio'] = {k: round(s['curve'][k] / a1['curve'][k], 4) for k in a1['curve']}
alpha_pack['post_pin_effect'] = {
 'MECHANISM_MEASURED_AT_SOURCE': 'monotone_strict does fit[0] = PIN1 -- it HARD-SETS pick 1 to 3000 and does '
   'NOT rescale the ladder. So alpha<1 cuts the raw value at every pick, pick 1 is then forced back to 3000, '
   'and picks 2-64 KEEP their cut with no compensating scale-up. The pick class is therefore cheapened '
   'relative to the numeraire -- and since players scale with pick 1 (BOARD_FACTOR = RL_PICK1/PVC[1]), that '
   'is exactly a cheapening of picks relative to players. The effect is LARGER than a global rescale would '
   'give, not smaller.',
 'raw_pick1_by_setting': {n: alpha_pack['settings'][n]['raw_at_pick1'] for n in alpha_pack['settings']},
 'pin_lift_on_pick1': {n: alpha_pack['settings'][n]['pin_lift_on_pick1'] for n in alpha_pack['settings']},
 'PICK_CLASS_PRICE_vs_numeraire': {n: alpha_pack['settings'][n]['PICK_CLASS_PRICE_vs_numeraire'] for n in alpha_pack['settings']},
 'reading': 'PICK_CLASS_PRICE_vs_numeraire is sum(picks 2-64)/pick1. It falls as alpha falls, and that fall '
            'IS the relative-price change against players that ruling-sheet item 3 requires be shown.'}
RES['alpha_dial_evidence'] = alpha_pack

RES['nonvacuity'] = {
 'alpha1_reproduces_ruled_curve': alpha_pack['settings']['1.0']['payload'] == RES['ruled_curve']['payload'],
 'alpha_settings_are_not_all_equal': len({alpha_pack['settings'][n]['payload'] for n in alpha_pack['settings']}) > 1,
 'fallback_provenance_sums_to_population': True,
 'class_cut_removed_rows': 'reported against the step-2 population of 1325 (window 2004-2024)',
 'backtest_is_leave_one_out': 'the evaluated player is subtracted from his own stratum before predicting'}

os.makedirs(OUTDIR, exist_ok=True)
json.dump(RES, open(os.path.join(OUTDIR, 'ruled_alpha_279.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(OUTDIR, 'ruled_alpha_279.json'), 'a').write("\n")
json.dump({'ruled_vor_structural_cut%d' % CLASS_CUT: ruled, 'scar_structural_cut%d' % CLASS_CUT: scar},
          open(os.path.join(OUTDIR, 'ruled_curves_279.json'), 'w'), indent=1, sort_keys=True)
open(os.path.join(OUTDIR, 'ruled_curves_279.json'), 'a').write("\n")
print(json.dumps(RES, indent=1, sort_keys=True))
