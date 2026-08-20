#!/usr/bin/env python3
# =====================================================================================================
# ORDER B BUILD -- THE OUTPUT-CONDITIONAL TERMINAL FADE FIT (PREREG_B_BUILD.md section 2; rules fixed
# there BEFORE this ran). Offline, read-only. Evidence base: the rebuilt W5 rows (per_entrant_O31FFINAL,
# md5 asserted) with the W5 tier cuts; machinery: the derivation's delta-space replica (b2_fit.py),
# carried -- the replica supplies COUNTERFACTUAL RATIOS only (C-REP rule).
#   family      r(a,s) = 0.14 + A * phi(a) * G(s);  phi = clip((a-27)/4, 0, 1);  G = exp(-s/s0)
#   surplus     s = max(0, L - REPL[bar]), L = trailing-2 level
#   loss        survivor-view anchored-B over tier x age cells (star/mid/role x 27..31), target 1,
#               weights = inverse variance of the published W5 survivor tier CIs
#   constraints full-view predicted B >= B_pt/CI_hi for every tier x age AND position x age cell
#   grid        A in 0..0.60 step .02;  s0 in {2,3,4,5,6,8,10,13,16,20,25,32,40,50,64}
#   ident       PASS iff 90% CI of A excludes 0 AND 90% CI of G(s_bar_star) < 0.5
#   seed 35, cluster bootstrap by player, B=500, 90% CIs
# =====================================================================================================
import json, math, os, hashlib, collections
import numpy as np

SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
HERE = os.path.dirname(os.path.abspath(__file__))
CAND_P = SP + '/per_entrant_O31FFINAL.json'
SEED = 35
B_BOOT = 500
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
# the MANDATED ladder (owner ruling B-1; PREREG section 1) -- pinned, not refit
RHO0, GG, PA_T = 0.030, 0.025, 27


def ladder_of(rho0, g, n=12):
    f, out = 1.0, []
    for j in range(1, n + 1):
        f *= (1.0 - min(0.60, max(0.0, rho0 + g * (j - 1))))
        out.append(f)
    return out


LAD = ladder_of(RHO0, GG)
A_GRID = [round(x, 2) for x in np.arange(0.0, 0.601, 0.02)]
S0_GRID = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 13.0, 16.0, 20.0, 25.0, 32.0, 40.0, 50.0, 64.0]

# W5 published tier CIs for weights + floors
W5R = json.load(open(os.path.join(os.path.dirname(HERE), 'order33_w5_2026-08-17', 'RESULTS_W5.json')))
W_SURV, FLOOR_FULL = {}, {}
for tr in ('star', 'mid', 'role'):
    for a_s, c in W5R['tiers']['tier:%s|survivor' % tr]['cells'].items():
        if isinstance(c, dict) and c.get('B_ci'):
            sd = (c['B_ci'][1] - c['B_ci'][0]) / 3.29
            W_SURV[(tr, int(a_s))] = 1.0 / sd ** 2
    for a_s, c in W5R['tiers']['tier:%s|full' % tr]['cells'].items():
        if isinstance(c, dict) and c.get('B_ci'):
            FLOOR_FULL[('tier:' + tr, int(a_s))] = c['B'] / c['B_ci'][1]
for gname, store, key in (('ALL', 'bias', 'ALL|full'), ('TALL', 'positions', 'pos:TALL|full'),
                          ('SMALL', 'positions', 'pos:SMALL|full'), ('RUCK', 'positions', 'pos:RUCK|full')):
    for a_s, c in W5R[store][key]['cells'].items():
        if isinstance(c, dict) and c.get('B') and c.get('B_ci'):
            FLOOR_FULL[(gname, int(a_s))] = c['B'] / c['B_ci'][1]
STAR_CI = {int(a): c['B_ci'] for a, c in W5R['tiers']['tier:star|survivor']['cells'].items()}
STAR_PT = {int(a): c['B'] for a, c in W5R['tiers']['tier:star|survivor']['cells'].items()}


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
        return {'RD': 'RD', 'MSD': 'MSD'}.get(r['type'], 'OTHERPOOL')
    return None


m5 = md5f(CAND_P)
assert m5.startswith('d97f1aee'), 'HALT md5 ' + m5
A = json.load(open(CAND_P))
recs = A['recs']

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
        num = den = 0.0
        for t in (Y, Y - 1):
            g2 = SGM[k].get(t, 0)
            if g2 >= 4:
                w = min(g2, 22)
                num += w * SAV[k][t]; den += w
        L = num / den if den > 0 else None
        rows.append(dict(key=k, age=a, Y=Y, mark=float(m), R=dvrest(k, Y), pos=pg, bar=bar,
                         surv=any(t > Y for t in SV[k]),
                         t2=SV[k].get(Y, 0.0) + SV[k].get(Y - 1, 0.0), L=L))
print('rebuilt primary rows %d (W5: 3218)' % len(rows))
assert len(rows) == 3218, 'HALT row count'

# tiers: terciles within age cell by t2 (W5 construction, carried)
for a in AGES:
    cell = [r for r in rows if r['age'] == a]
    if not cell:
        continue
    t2 = np.array([r['t2'] for r in cell])
    q1, q2 = np.percentile(t2, [100 / 3, 200 / 3])
    for r in cell:
        r['tier'] = 'role' if r['t2'] <= q1 else ('mid' if r['t2'] <= q2 else 'star')

# surplus
for x in rows:
    x['s'] = max(0.0, x['L'] - REPL[x['bar']]) if (x['L'] is not None and x['bar'] in REPL) else None
n_noL = sum(1 for x in rows if x['s'] is None)
print('rows with no trailing-2 L (ratio held 1.0, disclosed): %d' % n_noL)

# control: reproduce the published tier profile (survivor view) before any correction
def anchored_B_masked(mask_rows, marks=None):
    mk = (lambda x: marks[id(x)]) if marks else (lambda x: x['mark'])
    anc = [x for x in mask_rows if x['age'] in ANCHOR_AGES]
    if len(anc) < 20:
        return None, {}
    anc_ratio = np.mean([mk(x) for x in anc]) / np.mean([x['R'] for x in anc])
    prof = {}
    for a in TEST_AGES:
        cell = [x for x in mask_rows if x['age'] == a]
        if len(cell) < 20:
            continue
        Rm = np.mean([x['R'] for x in cell])
        if Rm <= 0:
            continue
        prof[a] = (np.mean([mk(x) for x in cell]) / Rm) / anc_ratio
    return float(anc_ratio), prof


for tr in ('star', 'mid', 'role'):
    _, pf = anchored_B_masked([x for x in rows if x.get('tier') == tr and x['surv']])
    pub = {int(a): c['B'] for a, c in W5R['tiers']['tier:%s|survivor' % tr]['cells'].items()}
    ok = all(abs(pf[a] - pub[a]) < 0.02 for a in pf)
    print('C-TIER %s|surv: ' % tr + ' '.join('%d:%.2f(pub %.2f)' % (a, pf[a], pub[a]) for a in sorted(pf)) +
          ('  PASS' if ok else '  MISMATCH'))
    assert ok, 'HALT C-TIER'

# ---- replica ----------------------------------------------------------------------------------------


def frac_engine(a, pa):
    return DELTAS[max(-8, min(14, int(round(a - pa))))]


def frac_tall(a, pa_star=PA_T, ladder=LAD):
    j = int(round(a - pa_star))
    if j <= 0:
        return DELTAS[max(-8, j)]
    if j <= len(ladder):
        return ladder[j - 1]
    lr = ladder[-1] / ladder[-2]
    f = ladder[-1]
    for _ in range(j - len(ladder)):
        f *= lr
    return f


def replica_mark(bar, a, L, r, tall):
    fracfn = frac_tall if tall else frac_engine
    pa = PA_T if tall else PEAK_AGE[bar]
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
    if bar in ('KPF', 'KPD'):
        prod *= 1.05
    runway = min(max((25 - a) / 6.0, 0), 1)
    elite = min(max((lp / PEAK[bar] - 0.97) / 0.30, 0), 1)
    return prod * (1 + runway * elite * PMAX)


def phi(a):
    return min(max((a - 27.0) / 4.0, 0.0), 1.0)


ROWS_L = [x for x in rows if x['s'] is not None and x['bar'] in BARS]
# base replica at flat 0.14 WITH the mandated ladder (talls) -- the fade fits the residual after it
REP_BASE = {}
for x in ROWS_L:
    REP_BASE[id(x)] = replica_mark(x['bar'], x['age'], x['L'], 0.14, x['pos'] == 'TALL')

# per-row corrected-mark matrix over the grid ---------------------------------------------------------
GRID = [(Av, s0) for Av in A_GRID for s0 in S0_GRID]
NG = len(GRID)
N = len(rows)
MARKS = np.zeros((NG, N))
row_arr = rows
for j, x in enumerate(row_arr):
    MARKS[:, j] = x['mark']
for gi, (Av, s0) in enumerate(GRID):
    for j, x in enumerate(row_arr):
        if x['s'] is None or REP_BASE.get(id(x), 0.0) <= 0:
            continue
        if x['pos'] == 'TALL':
            base_new = replica_mark(x['bar'], x['age'], x['L'], 0.14, True)  # ladder in base too
        else:
            base_new = REP_BASE[id(x)]
        r_eff = 0.14 + Av * phi(x['age']) * math.exp(-x['s'] / s0)
        if r_eff == 0.14:
            m_new = base_new
        else:
            m_new = replica_mark(x['bar'], x['age'], x['L'], r_eff, x['pos'] == 'TALL')
        MARKS[gi, j] = x['mark'] * (m_new / REP_BASE[id(x)]) if REP_BASE[id(x)] > 0 else x['mark']
    if gi % 50 == 0:
        print('  grid %d/%d' % (gi, NG))
# NOTE: for tall rows the base ratio (ladder at 0.14) is NOT 1.0 -- the ladder correction rides along in
# every grid point including A=0; the anchored instrument is invariant to the flat s* renorm (stated).

MK = np.array([x['mark'] for x in row_arr])
RR = np.array([x['R'] for x in row_arr])
AGE_A = np.array([x['age'] for x in row_arr])
SURV = np.array([bool(x['surv']) for x in row_arr])
TIER = np.array([x.get('tier') or '' for x in row_arr])
POS = np.array([x['pos'] or '' for x in row_arr])
IS_ANC = np.isin(AGE_A, list(ANCHOR_AGES))
players = sorted({x['key'] for x in row_arr})
pl_ix = {k: i for i, k in enumerate(players)}
PL = np.array([pl_ix[x['key']] for x in row_arr])


FLOOR_AGES = (28, 29, 30, 31)
# FLOOR SCOPE CLARIFICATION (disclosed, matches the derivation's own feasible() exactly): floors bind at
# ages 28-31 only -- phi(27)=0, the fade cannot act at 27, and the 27 cells carry pre-existing
# under-mark calls (SMALL|27 B=.885 CI_hi=.971 -> B_pt/CI_hi=.912 > B_pt) that a zero correction
# already "breaches"; b2_fit.py's feasible() checked {28,29,30,31} for the same reason. Additionally the
# effective floor is min(floor, B_at_zero_fade): a cell already under its formula floor with NO fade must
# not be cut further, but its pre-existing level is not held against the candidate.


def profiles(w):
    """per grid point: survivor tier loss + full-view floor feasibility. w = row weights (multiplicity)."""
    loss = np.zeros(NG)
    feas = np.ones(NG, bool)
    GI0 = GRID.index((0.0, S0_GRID[0]))
    for tr in ('star', 'mid', 'role'):
        tm = (TIER == tr)
        # survivor view
        anc = tm & IS_ANC & SURV
        wa = w * anc
        swa = wa.sum()
        if swa < 20:
            return None, None
        Ranc = (wa * RR).sum() / swa
        anc_vec = (MARKS[:, wa > 0] @ wa[wa > 0]) / swa / Ranc
        for a in TEST_AGES:
            cm = tm & (AGE_A == a) & SURV
            wc = w * cm
            swc = wc.sum()
            if swc < 20:
                continue
            Rc = (wc * RR).sum() / swc
            if Rc <= 0:
                continue
            Bv = ((MARKS[:, wc > 0] @ wc[wc > 0]) / swc / Rc) / anc_vec
            wt = W_SURV.get((tr, a), 0.0)
            loss += wt * (Bv - 1.0) ** 2
        # full view floors
        ancf = tm & IS_ANC
        waf = w * ancf
        Rancf = (waf * RR).sum() / waf.sum()
        ancf_vec = (MARKS[:, waf > 0] @ waf[waf > 0]) / waf.sum() / Rancf
        for a in FLOOR_AGES:
            cmf = tm & (AGE_A == a)
            wcf = w * cmf
            if wcf.sum() < 20:
                continue
            Rcf = (wcf * RR).sum() / wcf.sum()
            if Rcf <= 0:
                continue
            Bf = ((MARKS[:, wcf > 0] @ wcf[wcf > 0]) / wcf.sum() / Rcf) / ancf_vec
            fl = FLOOR_FULL.get(('tier:' + tr, a))
            if fl:
                feas &= (Bf >= min(fl, float(Bf[GI0])) - 1e-9)
    for gname, msel in (('ALL', np.ones(N, bool)), ('TALL', POS == 'TALL'),
                        ('SMALL', POS == 'SMALL'), ('RUCK', POS == 'RUCK')):
        ancf = msel & IS_ANC
        waf = w * ancf
        if waf.sum() < 20:
            continue
        Rancf = (waf * RR).sum() / waf.sum()
        ancf_vec = (MARKS[:, waf > 0] @ waf[waf > 0]) / waf.sum() / Rancf
        for a in FLOOR_AGES:
            cmf = msel & (AGE_A == a)
            wcf = w * cmf
            if wcf.sum() < 20:
                continue
            Rcf = (wcf * RR).sum() / wcf.sum()
            if Rcf <= 0:
                continue
            Bf = ((MARKS[:, wcf > 0] @ wcf[wcf > 0]) / wcf.sum() / Rcf) / ancf_vec
            fl = FLOOR_FULL.get((gname, a))
            if fl:
                feas &= (Bf >= min(fl, float(Bf[GI0])) - 1e-9)
    return loss, feas


W1 = np.ones(N)
loss0, feas0 = profiles(W1)
order = np.argsort(loss0)
best_gi = next(gi for gi in order if feas0[gi])
A_FIT, S0_FIT = GRID[best_gi]
print('\nFIT: A=%.2f s0=%.1f  loss=%.3f  (feasible %d of %d grid points)' % (
    A_FIT, S0_FIT, loss0[best_gi], int(feas0.sum()), NG))
print('  unconstrained best: A=%.2f s0=%.1f loss=%.3f feasible=%s' % (
    GRID[order[0]][0], GRID[order[0]][1], loss0[order[0]], bool(feas0[order[0]])))

# star-tier mean surplus at 28-31 (identification quantity)
star_s = [x['s'] for x in row_arr if x.get('tier') == 'star' and 28 <= x['age'] <= 31 and x['s'] is not None]
S_STAR_MEAN = float(np.mean(star_s))
print('  mean star-tier surplus (28-31): %.2f  -> G at fit = %.3f' % (S_STAR_MEAN, math.exp(-S_STAR_MEAN / S0_FIT)))

# tier profiles at the fit
def tier_profile_at(gi, view):
    out = {}
    for tr in ('star', 'mid', 'role'):
        sel = [x for x in row_arr if x.get('tier') == tr and (view == 'full' or x['surv'])]
        marks = {id(x): MARKS[gi, j] for j, x in enumerate(row_arr)}
        _, pf = anchored_B_masked(sel, marks)
        out[tr] = {a: round(v, 4) for a, v in pf.items()}
    return out


PROF_FIT_S = tier_profile_at(best_gi, 'survivor')
PROF_FIT_F = tier_profile_at(best_gi, 'full')
PROF_0_S = tier_profile_at(GRID.index((0.0, S0_GRID[0])), 'survivor')   # A=0: ladder-only reference
for tr in ('star', 'mid', 'role'):
    print('  %s|surv B: ladder-only ' % tr +
          ' '.join('%d:%.2f' % (a, PROF_0_S[tr][a]) for a in sorted(PROF_0_S[tr])) +
          '  -> with fade ' + ' '.join('%d:%.2f' % (a, PROF_FIT_S[tr][a]) for a in sorted(PROF_FIT_S[tr])))

# star gate (prereg): fitted star B inside published CI and within .05 of the measured point
STAR_GATE = {}
star_ok = True
for a in TEST_AGES:
    b_new = PROF_FIT_S['star'].get(a)
    ok = (b_new is not None and STAR_CI[a][0] <= b_new <= STAR_CI[a][1] and abs(b_new - STAR_PT[a]) <= 0.05)
    STAR_GATE[a] = dict(B_new=b_new, B_meas=STAR_PT[a], ci=STAR_CI[a], passes=bool(ok))
    star_ok &= ok
print('  STAR GATE: %s' % ('PASS' if star_ok else 'FAIL') +
      '  ' + ' '.join('%d:%.3f(meas %.3f)' % (a, STAR_GATE[a]['B_new'], STAR_PT[a]) for a in TEST_AGES))

# ---- bootstrap --------------------------------------------------------------------------------------
RNG = np.random.default_rng(SEED)
boot_A, boot_s0, boot_G = [], [], []
nfail = 0
for b in range(B_BOOT):
    cnt = np.bincount(RNG.integers(0, len(players), size=len(players)), minlength=len(players))
    w = cnt[PL].astype(float)
    res = profiles(w)
    if res[0] is None:
        nfail += 1
        continue
    lb, fb = res
    orderb = np.argsort(lb)
    gib = next((gi for gi in orderb if fb[gi]), None)
    if gib is None:
        nfail += 1
        continue
    Ab, s0b = GRID[gib]
    boot_A.append(Ab); boot_s0.append(s0b)
    boot_G.append(math.exp(-S_STAR_MEAN / s0b) if Ab > 0 else 0.0)
A_CI = [float(np.percentile(boot_A, 5)), float(np.percentile(boot_A, 95))]
S0_CI = [float(np.percentile(boot_s0, 5)), float(np.percentile(boot_s0, 95))]
G_CI = [float(np.percentile(boot_G, 5)), float(np.percentile(boot_G, 95))]
print('  boot (%d ok, %d failed draws): A CI [%.2f, %.2f]  s0 CI [%.1f, %.1f]  G(star) CI [%.3f, %.3f]'
      % (len(boot_A), nfail, A_CI[0], A_CI[1], S0_CI[0], S0_CI[1], G_CI[0], G_CI[1]))

IDENT_A = A_CI[0] > 0.0
IDENT_G = G_CI[1] < 0.5
IDENTIFIED = IDENT_A and IDENT_G
print('  IDENTIFICATION: A-CI excludes 0: %s;  G(star) CI below 0.5: %s  ==> %s'
      % (IDENT_A, IDENT_G, 'FITTED (conditional fade wired)' if IDENTIFIED else 'FAILED -> FALLBACK (flat hazard knots)'))

# effective rates at the fit, for the packet table
RATE_TABLE = {}
for a in (27, 28, 29, 30, 31, 32):
    RATE_TABLE[a] = {s: round(0.14 + A_FIT * phi(a) * math.exp(-s / S0_FIT), 4)
                     for s in (0, 2, 5, 10, 15, 20, 30)}
print('\n  effective rate r(a,s):')
for a in RATE_TABLE:
    print('   age %d: ' % a + '  '.join('s=%d:%.3f' % (s, v) for s, v in RATE_TABLE[a].items()))

# ALL / tier step closure (survivor-linked pairs, delta-space)
by_player_rows = collections.defaultdict(dict)
for x in rows:
    by_player_rows[x['key']][x['age']] = x
pairs = []
for k, d in by_player_rows.items():
    for a in range(26, 31):
        if a in d and (a + 1) in d and d[a + 1]['Y'] == d[a]['Y'] + 1:
            if d[a]['s'] is not None and d[a + 1]['s'] is not None:
                pairs.append((d[a], d[a + 1]))


def rep_at(x, Av, s0):
    r_eff = 0.14 + Av * phi(x['age']) * math.exp(-x['s'] / s0)
    return replica_mark(x['bar'], x['age'], x['L'], r_eff, x['pos'] == 'TALL')


STEPS = {}
for a in (27, 28, 29, 30):
    P2 = [(x0, x1) for x0, x1 in pairs if x0['age'] == a]
    if len(P2) < 20:
        continue
    eng = np.mean([x1['mark'] for _, x1 in P2]) / np.mean([x0['mark'] for x0, _ in P2])
    rel = np.mean([x1['R'] for _, x1 in P2]) / np.mean([x0['R'] for x0, _ in P2])
    f0 = np.mean([REP_BASE[id(x0)] for x0, _ in P2]); f1 = np.mean([REP_BASE[id(x1)] for _, x1 in P2])
    n0 = np.mean([rep_at(x0, A_FIT, S0_FIT) for x0, _ in P2])
    n1 = np.mean([rep_at(x1, A_FIT, S0_FIT) for _, x1 in P2])
    new = eng * (n1 / n0) / (f1 / f0)
    STEPS[a] = dict(n=len(P2), step='%d->%d' % (a, a + 1), engine=round(float(eng), 4),
                    new=round(float(new), 4), realized=round(float(rel), 4))
    print('  step %d->%d n=%d engine %.4f -> new %.4f  realized %.4f' % (a, a + 1, len(P2), eng, new, rel))

OUT = dict(meta=dict(prereg='PREREG_B_BUILD.md section 2 (pushed first, commit a6c6ec3)',
                     input=dict(path=CAND_P, md5=m5), seed=SEED, B_boot=B_BOOT,
                     rows=len(rows), rows_no_L=n_noL, grid=dict(A=A_GRID, s0=S0_GRID)),
           fit=dict(A=A_FIT, s0=S0_FIT, A_ci=A_CI, s0_ci=S0_CI,
                    star_mean_surplus=round(S_STAR_MEAN, 2),
                    G_at_star=round(math.exp(-S_STAR_MEAN / S0_FIT), 4), G_star_ci=G_CI,
                    identified=bool(IDENTIFIED), ident_A=bool(IDENT_A), ident_G=bool(IDENT_G),
                    n_feasible_grid=int(feas0.sum()),
                    unconstrained=dict(A=GRID[order[0]][0], s0=GRID[order[0]][1])),
           tier_B_ladder_only_surv=PROF_0_S, tier_B_fit_surv=PROF_FIT_S, tier_B_fit_full=PROF_FIT_F,
           star_gate={str(a): v for a, v in STAR_GATE.items()}, star_gate_pass=bool(star_ok),
           rate_table={str(a): v for a, v in RATE_TABLE.items()},
           steps=STEPS)
with open(os.path.join(HERE, 'RESULTS_B_FADE_FIT.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_FADE_FIT.json')
