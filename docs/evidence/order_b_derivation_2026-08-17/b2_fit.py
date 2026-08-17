#!/usr/bin/env python3
# =====================================================================================================
# ORDER B DERIVATION -- b2: the CLOSURE FIT (PREREG_B.md Objects 1-3 verification + Object 2 fit).
# Read-only. Rebuilds the W5 vantage rows exactly (construction copied from w5_veteran_mark.py),
# validates a replica of proj_from_peak against the engine's own measured step declines (C-REP), then:
#   C-W5  : reproduce published W5 anchors/B cells (control)
#   FIT-1 : tall post-peak ladder (peak age + rho0 + growth g), fitted so the replica-corrected marks
#           close the W5 TALL remaining-value bias (survivor view primary; full view guarded)
#   FIT-2 : age-dynamic terminal discount knots r(28..31), r(<=27)=0.14 pinned, solved on the residual
#           survivor-linked rate gaps subject to per-position level-B CI floors (no over-correction)
#   CHECKS: RUCK keep-verdict, rank preservation, young-end reach, x1.05 premium analytics
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'
SEED = 34
B_BOOT = 500          # bootstrap for fitted-parameter CIs (fit is re-run per draw; heavier than a mean)
FM = {'paddy-mccartin', 'thomas-boyd'}
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
REPL = {'MID': 80.1, 'SD': 78.3, 'RUCK': 78.5, 'KPD': 68.4, 'SF': 70.9, 'KPF': 66.8}
PEAK = {'MID': 92, 'RUCK': 92, 'SD': 78, 'KPD': 70, 'SF': 70, 'KPF': 72}
PEAK_AGE = {'MID': 25, 'RUCK': 27, 'SD': 26, 'KPD': 27, 'SF': 25, 'KPF': 27}
DELTAS = {-8: .58, -7: .62, -6: .68, -5: .74, -4: .80, -3: .86, -2: .92, -1: .97, 0: 1.0, 1: .99, 2: .98,
          3: .96, 4: .94, 5: .91, 6: .88, 7: .84, 8: .79, 9: .73, 10: .66, 11: .58, 12: .50, 13: .42, 14: .34}
PMAX = 0.25
S_SH = 3.0
LCAPT_BAR, LCAPT_M, LCAPT_W, LCAPT_G = 105.0, 109.5, 1.85, 1.00
LAST_REAL_SEASON = 2025
ENTRY_FLOOR = 2005
VANTAGE_LAST = 2021
AGES = list(range(23, 32))
TEST_AGES = [27, 28, 29, 30, 31]
ANCHOR_AGES = {23, 24, 25, 26}
POSG = {'KPD': 'TALL', 'KPF': 'TALL', 'MID': 'SMALL', 'SD': 'SMALL', 'SF': 'SMALL', 'RUCK': 'RUCK'}

# W5 published targets (RESULTS_W5.json) used as controls + fit weights
W5_TALL_SURV_B = {27: 1.21, 28: 1.28, 29: 1.33, 30: 1.66, 31: 1.41}
W5_REALIZED_STEP = {26: 0.8023, 27: 0.7478, 28: 0.6980, 29: 0.6622, 30: 0.6317}
W5_REALIZED_STEP_CI = {26: [0.777, 0.8263], 27: [0.7136, 0.7791], 28: [0.6503, 0.7395],
                       29: [0.6015, 0.7131], 30: [0.5557, 0.6925]}
W5_ENGINE_STEP = {26: 0.8118, 27: 0.8087, 28: 0.7574, 29: 0.7636, 30: 0.7854}
# over-correction floors from the published W5 full-view cells: a correction is too big when the
# corrected point would be CALLED under-marked at 90%, i.e. floor(g,a) = B_pt / B_ci_hi (relative CI).
W5R = json.load(open(os.path.join(os.path.dirname(HERE), 'order33_w5_2026-08-17', 'RESULTS_W5.json')))
B_FLOOR = {}
for gname, store, key in (('ALL', 'bias', 'ALL|full'), ('TALL', 'positions', 'pos:TALL|full'),
                          ('SMALL', 'positions', 'pos:SMALL|full'), ('RUCK', 'positions', 'pos:RUCK|full')):
    for a_s, cell in W5R[store][key]['cells'].items():
        if isinstance(cell, dict) and cell.get('B') and cell.get('B_ci'):
            B_FLOOR[(gname, int(a_s))] = round(cell['B'] / cell['B_ci'][1], 4)


def md5f(p):
    h = hashlib.md5()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


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


def arm_of(r):
    if r.get('teaches_curve') and r['type'] == 'ND':
        return 'ND'
    if r.get('is_pool'):
        t = r['type']
        if t == 'RD':
            return 'RD'
        if t == 'MSD':
            return 'MSD'
        return 'OTHERPOOL'
    return None


m5 = md5f(CAND_P)
assert m5.startswith('d97f1aee'), 'HALT md5 ' + m5
A = json.load(open(CAND_P))
recs = A['recs']

# ---- W5 rows, rebuilt verbatim ----------------------------------------------------------------------
SV, SBAR, SGM, SAV = {}, {}, {}, {}
for r in recs:
    d, bb, gg2, av = {}, {}, {}, {}
    for s in r['seasons']:
        if s['year'] > LAST_REAL_SEASON:
            continue
        g = s.get('bar')
        if g not in BARS:
            continue
        d[s['year']] = w_sqrt(s['games']) * season_raw(s['avg'], g)
        bb[s['year']] = g
        gg2[s['year']] = s['games']
        av[s['year']] = s['avg']
    SV[r['key']] = d; SBAR[r['key']] = bb; SGM[r['key']] = gg2; SAV[r['key']] = av


def dvrest(k, Y):
    return sum((1.14 ** -(t - Y)) * v for t, v in SV[k].items() if t > Y)


rows = []
for r in recs:
    k = r['key']
    if k in FM or arm_of(r) is None or r['year'] < ENTRY_FLOOR:
        continue
    lg = r.get('last_game_year')
    complete = (r['retired_now'] or r['delisted']) and (lg is not None and lg <= LAST_REAL_SEASON) \
        and not any(s['year'] > LAST_REAL_SEASON for s in r['seasons'])
    if not complete:
        continue
    for i, Y in enumerate(r['yrs']):
        if Y > VANTAGE_LAST:
            continue
        a = r['age_draft'] + (Y - r['year'])
        if a not in AGES:
            continue
        m = r['vpath'][i]
        if m is None:
            continue
        bar = SBAR[k].get(Y)
        pg = POSG.get(bar if bar is not None else r.get('pos'), None)
        # trailing-2 level for the replica
        num = den = 0.0
        for t in (Y, Y - 1):
            g2 = SGM[k].get(t, 0)
            if g2 >= 4:
                w = min(g2, 22)
                num += w * SAV[k][t]; den += w
        L = num / den if den > 0 else None
        rows.append(dict(key=k, age=a, Y=Y, mark=float(m), R=dvrest(k, Y), pos=pg, bar=bar,
                         surv=any(t > Y for t in SV[k]), L=L))
print('rebuilt primary rows %d (W5: 3218)' % len(rows))
assert len(rows) == 3218, 'HALT: row count mismatch vs W5'

# ---- C-W5: reproduce published anchors + TALL B ------------------------------------------------------


def anchored_B(rr, view, marks=None):
    sel = [x for x in rr if (view == 'full' or x['surv'])]
    mk = (lambda x: marks[id(x)]) if marks else (lambda x: x['mark'])
    anc = [x for x in sel if x['age'] in ANCHOR_AGES]
    if len(anc) < 20:
        return None, {}
    anc_ratio = np.mean([mk(x) for x in anc]) / np.mean([x['R'] for x in anc])
    prof = {}
    for a in TEST_AGES:
        cell = [x for x in sel if x['age'] == a]
        if len(cell) < 20:
            continue
        Rm = np.mean([x['R'] for x in cell])
        if Rm <= 0:
            continue
        prof[a] = (np.mean([mk(x) for x in cell]) / Rm) / anc_ratio
    return float(anc_ratio), prof


ancA, profA = anchored_B(rows, 'full')
ancT, profT = anchored_B([x for x in rows if x['pos'] == 'TALL'], 'full')
ancTs, profTs = anchored_B([x for x in rows if x['pos'] == 'TALL'], 'survivor')
print('C-W5: ALL|full anchor %.4f (pub 2.8800)  TALL|full anchor %.4f (pub 2.4213)' % (ancA, ancT))
print('  TALL|full B: ' + ' '.join('%d:%.2f' % (a, profA and profT[a]) for a in sorted(profT)))
print('  TALL|surv B: ' + ' '.join('%d:%.2f' % (a, profTs[a]) for a in sorted(profTs)))
assert abs(ancA - 2.8800) < 0.005 and abs(ancT - 2.4213) < 0.005, 'HALT C-W5 anchor mismatch'
assert abs(profT[30] - 1.76) < 0.02 and abs(profT[28] - 1.29) < 0.02, 'HALT C-W5 TALL B mismatch'
print('C-W5 PASS')

# ---- replica ----------------------------------------------------------------------------------------


def frac_engine(a, pa):
    return DELTAS[max(-8, min(14, int(round(a - pa))))]


def frac_new(a, pa_star, ladder):
    """ladder: list of post-peak fractions f(1), f(2), ...; pre-peak reuses shared DELTAS shape."""
    j = int(round(a - pa_star))
    if j <= 0:
        return DELTAS[max(-8, j)]
    if j <= len(ladder):
        return ladder[j - 1]
    # tail rule: hold last annual ratio flat
    lr = ladder[-1] / (ladder[-2] if len(ladder) > 1 else 1.0)
    f = ladder[-1]
    for _ in range(j - len(ladder)):
        f *= lr
    return f


def replica_mark(bar, a, L, r, fracfn, pa, tall_prem=True):
    """offline proj_from_peak (bal lens), level anchored to trailing-2 form on the curve."""
    f_a = fracfn(a, pa)
    if f_a < 1e-6:
        return 0.0
    lp = L / f_a
    cl = L
    prod = 0.0
    for k in range(18):
        ag = a + k
        fv = fracfn(ag, pa)
        if ag > 38 or fv < 0.42:
            break
        lev = lp * fv
        if ag <= pa or k == 0:
            lev = max(lev, cl)
        base = lev + capt_prem(lev)
        prod += posval(base - REPL[bar]) * 21 / (1.0 + r) ** k
    if bar in ('KPF', 'KPD') and tall_prem:
        prod *= 1.05
    runway = min(max((25 - a) / 6.0, 0), 1)
    elite = min(max((lp / PEAK[bar] - 0.97) / 0.30, 0), 1)
    prod *= (1 + runway * elite * PMAX)
    return prod


ROWS_L = [x for x in rows if x['L'] is not None and x['bar'] in BARS]
print('replica-able rows %d of %d (no trailing-2 level: %d, disclosed)'
      % (len(ROWS_L), len(rows), len(rows) - len(ROWS_L)))

# C-REP: replica survivor-linked step declines at flat 14% vs engine measured
by_player_rows = collections.defaultdict(dict)
for x in rows:
    by_player_rows[x['key']][x['age']] = x
pairs = []
for k, d in by_player_rows.items():
    for a in range(23, 31):
        if a in d and (a + 1) in d and d[a + 1]['Y'] == d[a]['Y'] + 1:
            if d[a]['L'] is not None and d[a + 1]['L'] is not None and d[a]['bar'] in BARS and d[a + 1]['bar'] in BARS:
                pairs.append((d[a], d[a + 1]))
print('replica pairs %d' % len(pairs))


def rep_old(x, r=0.14):
    return replica_mark(x['bar'], x['age'], x['L'], r, frac_engine, PEAK_AGE[x['bar']])


CREP = {}
for a in range(26, 31):
    P2 = [(x0, x1) for x0, x1 in pairs if x0['age'] == a]
    if len(P2) < 20:
        continue
    eng = np.mean([x1['mark'] for _, x1 in P2]) / np.mean([x0['mark'] for x0, _ in P2])
    rep = np.mean([rep_old(x1) for _, x1 in P2]) / np.mean([rep_old(x0) for x0, _ in P2])
    CREP[a] = dict(n=len(P2), engine=round(float(eng), 4), replica=round(float(rep), 4),
                   w5_engine=W5_ENGINE_STEP[a], gap_pp=round(100 * (rep - eng), 1))
    print('C-REP %d->%d n=%d engine %.4f replica %.4f gap %.1fpp' % (a, a + 1, len(P2), eng, rep, 100 * (rep - eng)))
CREP_PASS = all(abs(v['replica'] - v['engine']) <= 0.03 for v in CREP.values())
print('C-REP %s' % ('PASS (±3pp)' if CREP_PASS else 'FAIL — replica unfit, fallback per prereg'))

# ---- FIT-1: tall ladder -----------------------------------------------------------------------------
# family: decline rate at post-peak step j: rho_j = rho0 + g*(j-1), f(j) = prod_{i<=j}(1-rho_i), floors at >=0.05/yr
# grid: pa* in {25,26,27}; rho0 in 0..0.20 step .01; g in 0..0.06 step .005


def ladder_of(rho0, g, n=12):
    f, out = 1.0, []
    for j in range(1, n + 1):
        rho = min(0.60, max(0.0, rho0 + g * (j - 1)))
        f *= (1.0 - rho)
        out.append(f)
    return out


PA_GRID = [25, 26, 27]
RHO_GRID = [round(x, 3) for x in np.arange(0.0, 0.201, 0.01)]
G_GRID = [round(x, 3) for x in np.arange(0.0, 0.061, 0.005)]

TALL_ROWS = [x for x in ROWS_L if x['pos'] == 'TALL']
OTHER_ROWS = [x for x in ROWS_L if x['pos'] != 'TALL']

# precompute per tall row: M_old and M_new(pa,rho0,g) ratio
M_old_tall = {id(x): rep_old(x) for x in TALL_ROWS}


def tall_ratio_map(pa, rho0, g):
    lad = ladder_of(rho0, g)
    out = {}
    for x in TALL_ROWS:
        mo = M_old_tall[id(x)]
        out[id(x)] = (replica_mark(x['bar'], x['age'], x['L'], 0.14, lambda a, p: frac_new(a, pa, lad), pa) / mo
                      if mo > 0 else 1.0)
    return out


def tall_loss(ratio_map, rr=None):
    rr = rr if rr is not None else rows
    marks = {}
    for x in rr:
        marks[id(x)] = x['mark'] * ratio_map.get(id(x), 1.0)
    _, profS = anchored_B([x for x in rr if x['pos'] == 'TALL'], 'survivor', marks)
    _, profF = anchored_B([x for x in rr if x['pos'] == 'TALL'], 'full', marks)
    # weights: inverse variance from W5 survivor CIs (approx from full CIs widths)
    W = {27: 1 / 0.13 ** 2, 28: 1 / 0.14 ** 2, 29: 1 / 0.20 ** 2, 30: 1 / 0.39 ** 2, 31: 1 / 0.61 ** 2}
    loss = sum(W[a] * (profS.get(a, 1.0) - 1.0) ** 2 for a in TEST_AGES)
    # guard: full-view over-correction below the relative-CI floor
    pen = sum(100.0 * max(0.0, B_FLOOR[('TALL', a)] - profF[a]) ** 2
              for a in (28, 29, 30, 31) if a in profF and ('TALL', a) in B_FLOOR)
    return loss + pen, profS, profF


best = None
for pa in PA_GRID:
    for rho0 in RHO_GRID:
        for g in G_GRID:
            rm = tall_ratio_map(pa, rho0, g)
            ls, pS, pF = tall_loss(rm)
            if best is None or ls < best[0]:
                best = (ls, pa, rho0, g, pS, pF)
LS, PA_F, RHO_F, G_F, PS_F, PF_F = best
LAD_F = ladder_of(RHO_F, G_F)
print('\nFIT-1 TALL: pa*=%d rho0=%.3f g=%.3f loss=%.3f' % (PA_F, RHO_F, G_F, LS))
print('  ladder f(1..8): ' + ' '.join('%.3f' % v for v in LAD_F[:8]))
print('  implied TALL surv B: ' + ' '.join('%d:%.2f' % (a, PS_F[a]) for a in sorted(PS_F)))
print('  implied TALL full B: ' + ' '.join('%d:%.2f' % (a, PF_F[a]) for a in sorted(PF_F)))

# bootstrap the fit (cluster by TALL player), coarse grid around the optimum; survivor-view loss
# (vectorized: per-param corrected-mark arrays; per-draw masked means via row multiplicity weights)
tall_all = [x for x in rows if x['pos'] == 'TALL']
t_players = sorted({x['key'] for x in tall_all})
t_pl_ix = {k: i for i, k in enumerate(t_players)}
T_mark = np.array([x['mark'] for x in tall_all])
T_R = np.array([x['R'] for x in tall_all])
T_age = np.array([x['age'] for x in tall_all])
T_surv = np.array([x['surv'] for x in tall_all])
T_pl = np.array([t_pl_ix[x['key']] for x in tall_all])
T_anchor = np.isin(T_age, list(ANCHOR_AGES)) & T_surv
RNG = np.random.default_rng(SEED)
RED = [(pa, round(r0, 3), round(gg, 3)) for pa in PA_GRID
       for r0 in np.arange(max(0, RHO_F - 0.05), RHO_F + 0.051, 0.01)
       for gg in np.arange(max(0, G_F - 0.02), G_F + 0.021, 0.005)]
RED_MARKS = {}
for p in RED:
    rm = tall_ratio_map(*p)
    RED_MARKS[p] = T_mark * np.array([rm.get(id(x), 1.0) for x in tall_all])
WT = {27: 1 / 0.13 ** 2, 28: 1 / 0.14 ** 2, 29: 1 / 0.20 ** 2, 30: 1 / 0.39 ** 2, 31: 1 / 0.61 ** 2}
boot_params = []
for b in range(B_BOOT):
    cnt = np.bincount(RNG.integers(0, len(t_players), size=len(t_players)), minlength=len(t_players))
    w = cnt[T_pl].astype(float)
    wa = w * T_anchor
    if wa.sum() < 20:
        continue
    Ranc = (wa * T_R).sum() / wa.sum()
    bb = None
    for p in RED:
        mk = RED_MARKS[p]
        anc = ((wa * mk).sum() / wa.sum()) / Ranc if Ranc > 0 else np.nan
        loss = 0.0
        ok = True
        for a in TEST_AGES:
            wcell = w * (T_age == a) * T_surv
            if wcell.sum() < 20:
                continue
            Rc = (wcell * T_R).sum() / wcell.sum()
            if Rc <= 0 or not np.isfinite(anc):
                ok = False
                break
            Bv = ((wcell * mk).sum() / wcell.sum() / Rc) / anc
            loss += WT[a] * (Bv - 1.0) ** 2
        if ok and (bb is None or loss < bb[0]):
            bb = (loss, p)
    if bb:
        boot_params.append(bb[1])
pa_bs = [p[0] for p in boot_params]; r0_bs = [p[1] for p in boot_params]; g_bs = [p[2] for p in boot_params]
lad_bs = np.array([ladder_of(r0, g)[:8] for _, r0, g in boot_params])
lad_ci = np.percentile(lad_bs, [5, 95], axis=0)
print('  boot: pa* CI [%d,%d]  rho0 CI [%.3f,%.3f]  g CI [%.3f,%.3f]' % (
    np.percentile(pa_bs, 5), np.percentile(pa_bs, 95), np.percentile(r0_bs, 5), np.percentile(r0_bs, 95),
    np.percentile(g_bs, 5), np.percentile(g_bs, 95)))

# RUCK keep-check: does the fitted tall family beat the engine curve for RUCK? (guard — expect NO)
RUCK_ROWS = [x for x in ROWS_L if x['pos'] == 'RUCK']
M_old_ruck = {id(x): rep_old(x) for x in RUCK_ROWS}
_, profR_now = anchored_B([x for x in rows if x['pos'] == 'RUCK'], 'full')
rm_ruck = {}
lad = LAD_F
for x in RUCK_ROWS:
    mo = M_old_ruck[id(x)]
    rm_ruck[id(x)] = (replica_mark(x['bar'], x['age'], x['L'], 0.14, lambda a, p: frac_new(a, PA_F, lad), PA_F) / mo
                      if mo > 0 else 1.0)
marks_r = {id(x): x['mark'] * rm_ruck.get(id(x), 1.0) for x in rows}
_, profR_new = anchored_B([x for x in rows if x['pos'] == 'RUCK'], 'full', marks_r)
print('  RUCK check: B now ' + ' '.join('%d:%.2f' % (a, profR_now[a]) for a in sorted(profR_now)) +
      ' | with-tall-ladder ' + ' '.join('%d:%.2f' % (a, profR_new[a]) for a in sorted(profR_new)))

# ---- FIT-2: discount knots --------------------------------------------------------------------------
# precompute per replica-pair-row marks at rate grid, WITH the fitted tall ladder for talls
R_GRID = [round(x, 3) for x in np.arange(0.14, 0.341, 0.005)]
RATIO_TALL = tall_ratio_map(PA_F, RHO_F, G_F)


def rep_new(x, r):
    if x['pos'] == 'TALL':
        return replica_mark(x['bar'], x['age'], x['L'], r, lambda a, p: frac_new(a, PA_F, LAD_F), PA_F)
    return replica_mark(x['bar'], x['age'], x['L'], r, frac_engine, PEAK_AGE[x['bar']])


PAIR_M = {}
for x0, x1 in pairs:
    for x in (x0, x1):
        if id(x) not in PAIR_M:
            PAIR_M[id(x)] = np.array([rep_new(x, r) for r in R_GRID])

# per-age stacked arrays for the pairs (vectorized): replica M at every rate, engine marks, realized R
STEP_ARR = {}
for a in (26, 27, 28, 29, 30):
    P2 = [(x0, x1) for x0, x1 in pairs if x0['age'] == a]
    if len(P2) < 20:
        continue
    STEP_ARR[a] = dict(n=len(P2),
                       M0=np.stack([PAIR_M[id(x0)] for x0, _ in P2]),     # n x nR
                       M1=np.stack([PAIR_M[id(x1)] for _, x1 in P2]),
                       R0=np.array([x0['R'] for x0, _ in P2]),
                       R1=np.array([x1['R'] for _, x1 in P2]),
                       E0=np.array([x0['mark'] for x0, _ in P2]),
                       E1=np.array([x1['mark'] for _, x1 in P2]),
                       keys=[x0['key'] for x0, _ in P2])
NR = len(R_GRID)


def _rix(r):
    return min(range(NR), key=lambda i: abs(R_GRID[i] - r))


IX14 = _rix(0.14)

# subset-consistent measured targets (same pair set for engine, replica and realized)
SUB = {}
for a, S in STEP_ARR.items():
    SUB[a] = dict(eng=float(S['E1'].mean() / S['E0'].mean()),
                  realized=float(S['R1'].mean() / S['R0'].mean()),
                  rep_flat=float(S['M1'][:, IX14].mean() / S['M0'][:, IX14].mean()))
    print('  subset step %d->%d: engine %.4f realized %.4f (W5 full-set: %.4f / %.4f)' % (
        a, a + 1, SUB[a]['eng'], SUB[a]['realized'], W5_ENGINE_STEP[a], W5_REALIZED_STEP[a]))

# DELTA-SPACE step prediction (C-REP failed at +-3pp, so the replica is used ONLY for the
# counterfactual RATIO, never its absolute step level — disclosed deviation handling per prereg):
#   new_step(a; r_a, r_a1) = eng_step(a) * [rep_step(a; r_a, r_a1) / rep_step(a; .14, .14)]
STEP_SD = {a: (W5_REALIZED_STEP_CI[a][1] - W5_REALIZED_STEP_CI[a][0]) / 3.29 for a in (27, 28, 29, 30)}


def new_step(a, i_a, i_a1, S=None, w=None):
    S = S or STEP_ARR[a]
    if w is None:
        m0f, m1f = S['M0'][:, IX14].mean(), S['M1'][:, IX14].mean()
        m0, m1 = S['M0'][:, i_a].mean(), S['M1'][:, i_a1].mean()
        eng = S['E1'].mean() / S['E0'].mean()
    else:
        sw = w.sum()
        m0f, m1f = (w * S['M0'][:, IX14]).sum() / sw, (w * S['M1'][:, IX14]).sum() / sw
        m0, m1 = (w * S['M0'][:, i_a]).sum() / sw, (w * S['M1'][:, i_a1]).sum() / sw
        eng = (w * S['E1']).sum() / (w * S['E0']).sum()
    return eng * (m1 / m0) / (m1f / m0f)


# level tables: B_new(g, a; r) as a function of the age-a rate alone (anchors fixed at 0.14)
ALL_ROWS_L = ROWS_L
M_LVL, REP_OLD = {}, {}
for x in ALL_ROWS_L:
    M_LVL[id(x)] = np.array([rep_new(x, r) for r in R_GRID])
    REP_OLD[id(x)] = rep_old(x)
GDEF = (('ALL', lambda x: True), ('TALL', lambda x: x['pos'] == 'TALL'),
        ('SMALL', lambda x: x['pos'] == 'SMALL'), ('RUCK', lambda x: x['pos'] == 'RUCK'))
B_TABLE = {}       # (g, a) -> vector over R_GRID of full-view anchored B
ANCH = {}
for gname, fn in GDEF:
    sel = [x for x in rows if fn(x)]
    anc_rows = [x for x in sel if x['age'] in ANCHOR_AGES]
    # anchor marks carry the tall-ladder fix at 0.14 (rate never touches <=27)
    anc_m = np.mean([x['mark'] * ((M_LVL[id(x)][IX14] / REP_OLD[id(x)]) if id(x) in M_LVL and REP_OLD[id(x)] > 0 else 1.0)
                     for x in anc_rows])
    anc_R = np.mean([x['R'] for x in anc_rows])
    ANCH[gname] = anc_m / anc_R
    for a in TEST_AGES:
        cell = [x for x in sel if x['age'] == a]
        if len(cell) < 20:
            continue
        Rm = np.mean([x['R'] for x in cell])
        vec = np.zeros(NR)
        for i in range(NR):
            mm = np.mean([x['mark'] * ((M_LVL[id(x)][i] / REP_OLD[id(x)]) if id(x) in M_LVL and REP_OLD[id(x)] > 0 else 1.0)
                          for x in cell])
            vec[i] = (mm / Rm) / ANCH[gname]
        B_TABLE[(gname, a)] = vec


def feasible(i28, i29, i30, i31):
    ii = {28: i28, 29: i29, 30: i30, 31: i31}
    for (gname, a), floor in B_FLOOR.items():
        if a in ii and (gname, a) in B_TABLE:
            if B_TABLE[(gname, a)][ii[a]] < floor - 1e-9:
                return False
    return True


def wls_loss(i28, i29, i30, i31, arrs=None, weights=None, targets=None):
    ii = {27: IX14, 28: i28, 29: i29, 30: i30, 31: i31}
    loss = 0.0
    for a in (27, 28, 29, 30):
        S = (arrs or STEP_ARR)[a]
        w = weights.get(a) if weights else None
        tgt = targets[a] if targets else SUB[a]['realized']
        ns = new_step(a, ii[a], ii[a + 1], S, w)
        loss += ((ns - tgt) / STEP_SD[a]) ** 2
    return loss


# grid search: monotone knot 4-tuples (step .01); precomputed mean-vectors make each eval O(1)
UV0 = {a: STEP_ARR[a]['M0'].mean(axis=0) for a in (27, 28, 29, 30)}
UV1 = {a: STEP_ARR[a]['M1'].mean(axis=0) for a in (27, 28, 29, 30)}
UENG = {a: SUB[a]['eng'] for a in (27, 28, 29, 30)}


def fast_loss(i28, i29, i30, i31):
    ii = {27: IX14, 28: i28, 29: i29, 30: i30, 31: i31}
    ls = 0.0
    for a in (27, 28, 29, 30):
        ns = UENG[a] * (UV1[a][ii[a + 1]] / UV0[a][ii[a]]) / (UV1[a][IX14] / UV0[a][IX14])
        ls += ((ns - SUB[a]['realized']) / STEP_SD[a]) ** 2
    return ls


CAND_IX = list(range(0, NR, 2))          # 0.14, 0.15, ... step .01
best_u, best_c = None, None
for i28 in CAND_IX:
    for i29 in CAND_IX:
        if i29 < i28:
            continue
        for i30 in CAND_IX:
            if i30 < i29:
                continue
            for i31 in CAND_IX:
                if i31 < i30:
                    continue
                ls = fast_loss(i28, i29, i30, i31)
                if best_u is None or ls < best_u[0]:
                    best_u = (ls, i28, i29, i30, i31)
                if feasible(i28, i29, i30, i31):
                    if best_c is None or ls < best_c[0]:
                        best_c = (ls, i28, i29, i30, i31)
KNOTS_RAW = {a: R_GRID[i] for a, i in zip((28, 29, 30, 31), best_u[1:])}
KNOTS_F = {a: R_GRID[i] for a, i in zip((28, 29, 30, 31), best_c[1:])}
KNOTS_F[27] = 0.14
KNOTS_RAW[27] = 0.14
print('\nFIT-2 unconstrained WLS knots: %s (loss %.2f)' % (KNOTS_RAW, best_u[0]))
print('FIT-2 CONSTRAINED WLS knots:   %s (loss %.2f)' % (KNOTS_F, best_c[0]))


def rate_of(a, knots):
    if a <= 27:
        return 0.14
    return knots.get(min(a, 31), knots[31])


IIF = {a: _rix(rate_of(a, KNOTS_F)) for a in (27, 28, 29, 30, 31)}
FINAL_STEPS = {}
for a in (26, 27, 28, 29, 30):
    i_a = IIF.get(a, IX14); i_a1 = IIF.get(a + 1, IX14)
    ns = new_step(a, i_a, i_a1)
    FINAL_STEPS[a] = dict(step='%d->%d' % (a, a + 1), new=round(float(ns), 4),
                          engine_old=round(SUB[a]['eng'], 4), realized=round(SUB[a]['realized'], 4),
                          realized_ci_w5=W5_REALIZED_STEP_CI[a])
    print('  step %d->%d: engine %.4f -> new %.4f  realized %.4f' % (a, a + 1, SUB[a]['eng'], ns, SUB[a]['realized']))


def level_B_with(knots):
    marks = {}
    for x in rows:
        if id(x) in M_LVL and REP_OLD[id(x)] > 0:
            newm = float(M_LVL[id(x)][_rix(rate_of(x['age'], knots))])
            marks[id(x)] = x['mark'] * newm / REP_OLD[id(x)]
        else:
            marks[id(x)] = x['mark']
    out = {}
    for gname, fn in GDEF:
        _, pf = anchored_B([x for x in rows if fn(x)], 'full', marks)
        out[gname] = pf
    return out, marks


profF, marksF = level_B_with(KNOTS_F)
for gname in ('ALL', 'TALL', 'SMALL', 'RUCK'):
    pf = profF[gname]
    print('  final full B %s: ' % gname + ' '.join('%d:%.2f' % (a, pf[a]) for a in sorted(pf)) +
          '   floors: ' + ' '.join('%d:%.2f' % (a, B_FLOOR.get((gname, a), float('nan'))) for a in sorted(pf)))

# bootstrap knots (cluster by player over pairs; targets + engine + replica means re-drawn; floors fixed)
pair_players = sorted({x0['key'] for x0, _ in pairs})
pp_ix = {k: i for i, k in enumerate(pair_players)}
for a in STEP_ARR:
    STEP_ARR[a]['pl'] = np.array([pp_ix[k] for k in STEP_ARR[a]['keys']])
COARSE = list(range(0, NR, 4))            # step .02 for the bootstrap solve
FEAS_C = [(i28, i29, i30, i31) for i28 in COARSE for i29 in COARSE if i29 >= i28
          for i30 in COARSE if i30 >= i29 for i31 in COARSE if i31 >= i30]
FEAS_C = [t for t in FEAS_C if feasible(*t)]
knot_bs = {28: [], 29: [], 30: [], 31: []}
for b in range(B_BOOT):
    cnt = np.bincount(RNG.integers(0, len(pair_players), size=len(pair_players)), minlength=len(pair_players))
    wts, tgs, okd = {}, {}, True
    for a in (27, 28, 29, 30):
        S = STEP_ARR.get(a)
        w = cnt[S['pl']].astype(float) if S is not None else None
        if S is None or w.sum() < 20:
            okd = False
            break
        m0 = (w * S['R0']).sum() / w.sum()
        if m0 <= 0:
            okd = False
            break
        tgs[a] = (w * S['R1']).sum() / w.sum() / m0
        wts[a] = w
    if not okd:
        continue
    # precompute weighted mean-vectors over the rate grid for this draw
    V0, V1, ENG = {}, {}, {}
    for a in (27, 28, 29, 30):
        S = STEP_ARR[a]; w = wts[a]; sw = w.sum()
        V0[a] = (w @ S['M0']) / sw
        V1[a] = (w @ S['M1']) / sw
        ENG[a] = (w * S['E1']).sum() / (w * S['E0']).sum()
    bb = None
    for t in FEAS_C:
        ii = {27: IX14, 28: t[0], 29: t[1], 30: t[2], 31: t[3]}
        ls = 0.0
        for a in (27, 28, 29, 30):
            ns = ENG[a] * (V1[a][ii[a + 1]] / V0[a][ii[a]]) / (V1[a][IX14] / V0[a][IX14])
            ls += ((ns - tgs[a]) / STEP_SD[a]) ** 2
        if bb is None or ls < bb[0]:
            bb = (ls, t)
    if bb:
        for a, i in zip((28, 29, 30, 31), bb[1]):
            knot_bs[a].append(R_GRID[i])
KNOT_CI = {a: [round(float(np.percentile(v, 5)), 3), round(float(np.percentile(v, 95)), 3)]
           for a, v in knot_bs.items() if len(v) > 50}
print('  knot CIs (constrained WLS, cluster bootstrap): %s' % KNOT_CI)

# hazard cross-check
EXITS = {27: 0.1293, 28: 0.1289, 29: 0.2009, 30: 0.2216, 31: 0.2358}
HAZ = {a: round(0.14 + (EXITS[a] - 0.13), 3) for a in EXITS}
print('  hazard-arithmetic reference r(a)=0.14+dh: %s' % HAZ)

# ---- rank preservation ------------------------------------------------------------------------------
from scipy.stats import rankdata


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


RANK = {}
for a in TEST_AGES:
    cell = [x for x in rows if x['age'] == a]
    old = spear(np.array([x['mark'] for x in cell]), np.array([x['R'] for x in cell]))
    new = spear(np.array([marksF[id(x)] for x in cell]), np.array([x['R'] for x in cell]))
    RANK[a] = dict(n=len(cell), rho_old=round(old, 4), rho_new=round(new, 4))
    print('  rank age %d: old %.3f new %.3f' % (a, old, new))

# ---- young-end reach + premium analytics ------------------------------------------------------------
YOUNG = {}
print('  young/veteran reach grid (KPF): ladder-only ratio | +discount ratio, by level')
for a in list(range(20, 32)):
    row = {}
    for L in (60.0, 70.0, 80.0, 90.0, 100.0):
        mo = replica_mark('KPF', a, L, 0.14, frac_engine, 27)
        m_lad = replica_mark('KPF', a, L, 0.14, lambda aa, p: frac_new(aa, PA_F, LAD_F), PA_F)
        m_all = replica_mark('KPF', a, L, rate_of(a, KNOTS_F), lambda aa, p: frac_new(aa, PA_F, LAD_F), PA_F)
        row[L] = dict(ladder_only=round(m_lad / mo, 4), combined=round(m_all / mo, 4))
    YOUNG[a] = row
    print('   age %d: ' % a + '  '.join('L%.0f %.2f|%.2f' % (L, row[L]['ladder_only'], row[L]['combined'])
                                        for L in sorted(row)))
# discount-only reach on non-tall veterans (MID), by level
YOUNG_MID = {}
for a in (28, 29, 30, 31, 32):
    row = {}
    for L in (80.0, 90.0, 100.0, 110.0):
        mo = replica_mark('MID', a, L, 0.14, frac_engine, PEAK_AGE['MID'])
        mn = replica_mark('MID', a, L, rate_of(a, KNOTS_F), frac_engine, PEAK_AGE['MID'])
        row[L] = round(mn / mo, 4)
    YOUNG_MID[a] = row
    print('   MID age %d discount-only: ' % a + '  '.join('L%.0f %.3f' % (L, row[L]) for L in sorted(row)))

# premium: anchored-B invariance shown numerically
marks_noprem = {}
for x in rows:
    marks_noprem[id(x)] = x['mark'] * (1 / 1.05 if x['pos'] == 'TALL' else 1.0)
_, prof_np = anchored_B([x for x in rows if x['pos'] == 'TALL'], 'full', marks_noprem)
print('  premium-off TALL full B (should equal with-premium): ' +
      ' '.join('%d:%.4f' % (a, prof_np[a]) for a in sorted(prof_np)))

OUT = dict(meta=dict(input=dict(path=CAND_P, md5=m5), seed=SEED, B_boot=B_BOOT,
                     rows=len(rows), replica_rows=len(ROWS_L), pairs=len(pairs)),
           controls=dict(c_w5=dict(anchor_all=round(ancA, 4), anchor_tall=round(ancT, 4),
                                   tall_full_B={a: round(v, 4) for a, v in profT.items()},
                                   passed=True),
                         c_rep=dict(steps=CREP, passed=CREP_PASS)),
           fit1_tall=dict(family='rho_j = rho0 + g*(j-1); f(j)=prod(1-rho_i); pre-peak keeps shared DELTAS',
                          peak_age=PA_F, rho0=RHO_F, g=G_F,
                          ladder={j + 1: round(v, 4) for j, v in enumerate(LAD_F[:10])},
                          ladder_ci_5=[round(float(v), 4) for v in lad_ci[0]],
                          ladder_ci_95=[round(float(v), 4) for v in lad_ci[1]],
                          peak_age_ci=[int(np.percentile(pa_bs, 5)), int(np.percentile(pa_bs, 95))],
                          rho0_ci=[round(float(np.percentile(r0_bs, 5)), 3), round(float(np.percentile(r0_bs, 95)), 3)],
                          g_ci=[round(float(np.percentile(g_bs, 5)), 3), round(float(np.percentile(g_bs, 95)), 3)],
                          implied_tall_surv_B={a: round(v, 4) for a, v in PS_F.items()},
                          implied_tall_full_B={a: round(v, 4) for a, v in PF_F.items()},
                          ruck_check=dict(now={a: round(v, 4) for a, v in profR_now.items()},
                                          with_tall_ladder={a: round(v, 4) for a, v in profR_new.items()})),
           fit2_discount=dict(knots_unconstrained=KNOTS_RAW, knots_constrained=KNOTS_F,
                              knot_ci=KNOT_CI, hazard_reference=HAZ,
                              subset_steps=SUB, steps_final=FINAL_STEPS,
                              floors={'%s|%d' % k: v for k, v in B_FLOOR.items()},
                              level_B_final={g: {a: round(v, 4) for a, v in p.items()} for g, p in profF.items()},
                              delta_space_note='C-REP failed +-3pp; replica used only for counterfactual ratios'),
           rank_preservation=RANK,
           young_end_reach=YOUNG, discount_reach_mid=YOUNG_MID,
           premium=dict(anchored_invariance_B={a: round(v, 4) for a, v in prof_np.items()},
                        prime_anchors=dict(TALL=2.4213, SMALL=3.0843, RUCK=2.6385, ALL=2.88),
                        removal_effect_flat=-0.0476))
with open(os.path.join(HERE, 'RESULTS_B_FIT.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_FIT.json')
