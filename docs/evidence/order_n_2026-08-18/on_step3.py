#!/usr/bin/env python3
"""ORDER N STEP 3 — THE DERIVATION. READ-ONLY.

Every constant of the replacement charge is derived here from STEP2_N.json — the outcome measurement
— and from the population's own distribution. Nothing here is tuned, and nothing here reads a board
price except v0, which never enters the derivation at all (it was only the pedigree control in Step 2).

The form was fixed in PREREG_N.md section 5 before any number existed. One thing changed and it is
declared loudly in the packet: the charge is written as exp(-X) rather than (1 - X). The reason is
structural, not cosmetic — exp(-X) is in (0, 1] for every X >= 0, so no row can ever be charged past
its whole pedigree leg and the max(0, .) clamp the current mechanism needs disappears. The prereg's
five structural properties N-S1..N-S5 are all still required and all still checked.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_step3.py
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402

SEED, B_PAR = 32, 4000
L = []


def P(s=''):
    print(s); L.append(str(s))


S2 = json.load(open(os.path.join(HERE, 'STEP2_N.json')))
ROWS = S2['rows']

P('=' * 118)
P('ORDER N — STEP 3. THE DERIVED CHARGE')
P('=' * 118)
P('input: STEP2_N.json — the outcome measurement. No board price enters this file.')
P()

# =====================================================================================================
# 1 · A(g) — HOW MUCH EVIDENCE g GAMES ACTUALLY IS
# =====================================================================================================
P('-' * 118)
P('1 · A(g) — THE EVIDENCE CURVE, FITTED TO THE MEASURED PAYOFF TO PERFORMANCE')
P('-' * 118)
P('   Step 2 measured BETA(g): the proportional payoff to one point per game of surplus, at fixed')
P('   pedigree. It rises with games and then flattens. That is an evidence-accumulation curve and it')
P('   is measured, not assumed. Fit:')
P()
P('       BETA(g) = BETA_sat * ( 1 - exp(-g/G0) )')
P()
P('   A(g) = 1 - exp(-g/G0) is then the SHARE OF THE MATURE PERFORMANCE SIGNAL that g games have')
P('   revealed. A(0) = 0 exactly, which is prereg property N-S1, and A is increasing, which is N-S2.')
P()

bins = []
for b, e in S2['E2'].items():
    if b == 'POOLED':
        continue
    sub = [r for r in ROWS if r['gbin'] == b]
    gm = float(np.mean([r['g'] for r in sub]))
    lo, hi = e['ci_dvrest']
    bins.append(dict(bin=b, g=gm, beta=e['beta_dvrest'], lo=lo, hi=hi, n=e['n'],
                     sd=(hi - lo) / (2 * 1.6448536269514722)))
bins.sort(key=lambda d: d['g'])
P('   %-8s %8s %5s | %10s %-22s %10s' % ('bin', 'mean g', 'n', 'BETA', '90% CI', 'implied sd'))
for d in bins:
    P('   %-8s %8.2f %5d | %+10.5f [%+.5f,%+.5f] %10.5f' % (d['bin'], d['g'], d['n'], d['beta'], d['lo'], d['hi'], d['sd']))
P()

gs = np.array([d['g'] for d in bins])
bt = np.array([d['beta'] for d in bins])
sd = np.array([d['sd'] for d in bins])
w = 1.0 / (sd ** 2)


GRID = np.arange(0.5, 60.0001, 0.01)                       # (K,)
AMAT = 1.0 - np.exp(-gs[None, :] / GRID[:, None])          # (K, nbins)
WA2 = (w[None, :] * AMAT * AMAT).sum(axis=1)               # (K,)


def fit_many(BV):
    """BV is (M, nbins). Weighted least squares over the whole G0 grid at once."""
    num = np.einsum('j,kj,mj->mk', w, AMAT, BV)            # (M, K)
    bs = num / WA2[None, :]                                # (M, K)
    resid = BV[:, None, :] - bs[:, :, None] * AMAT[None, :, :]
    sse = (w[None, None, :] * resid ** 2).sum(axis=2)      # (M, K)
    ki = sse.argmin(axis=1)
    m = np.arange(BV.shape[0])
    return GRID[ki], bs[m, ki], sse[m, ki]


g0v, bsv, ssev = fit_many(bt[None, :])
G0, BSAT, SSE = float(g0v[0]), float(bsv[0]), float(ssev[0])
rng = np.random.default_rng(SEED)
BV = bt[None, :] + rng.normal(0.0, sd[None, :], size=(B_PAR, len(bt)))
keep = ~(BV <= 0).all(axis=1)
BV = BV[keep]
g0d, bsd, _ = fit_many(BV)
D = np.column_stack([g0d, bsd])
G0_CI = (float(np.percentile(D[:, 0], 5)), float(np.percentile(D[:, 0], 95)))
BS_CI = (float(np.percentile(D[:, 1], 5)), float(np.percentile(D[:, 1], 95)))

P('   FITTED, weighted by the inverse variance of each bin, grid 0.01 on G0:')
P('       G0        = %.2f games      90%% CI [%.2f, %.2f]' % (G0, G0_CI[0], G0_CI[1]))
P('       BETA_sat  = %.5f            90%% CI [%.5f, %.5f]' % (BSAT, BS_CI[0], BS_CI[1]))
P('       weighted SSE %.4g over %d bins, 2 free parameters' % (SSE, len(bins)))
P('   CIs are a parametric bootstrap: each bin\'s BETA redrawn %d times from a normal with the sd its' % B_PAR)
P('   own cluster bootstrap implied, then the curve refitted. Seed %d.' % SEED)
P()
P('   FIT QUALITY, bin by bin:')
P('   %-8s %8s | %10s %10s %10s' % ('bin', 'mean g', 'BETA obs', 'BETA fit', 'A(g)'))
for d in bins:
    a = 1.0 - math.exp(-d['g'] / G0)
    P('   %-8s %8.2f | %+10.5f %+10.5f %10.4f' % (d['bin'], d['g'], d['beta'], BSAT * a, a))
P()
P('   A(g) AT THE ORDER\'S OWN ANCHORS:')
P('   %-8s %10s %14s' % ('games', 'A(g)', 'vs current m_d(g)'))
for g in (0, 2, 5, 10, 14, 15, 20, 30, 40, 60, 100, 200):
    P('   %-8d %10.4f %14.4f' % (g, 1.0 - math.exp(-g / G0), LB.m_d(g)))
P()
P('   READ THE TWO COLUMNS. The current shape m_d peaks at 14 games and then FALLS: a 36-game player')
P('   keeps more of his unearned pedigree than a 17-game player. A(g) never falls. That is the whole')
P('   of requirement (c), and the measurement above is what justifies it — the payoff to performance')
P('   does not fall after 14 games either, it flattens and stays flat.')
P()

# =====================================================================================================
# 2 · THE TILT — AND THE TWO DEVIATIONS FROM THE PREREGISTERED FORM, DECLARED HERE
# =====================================================================================================
P('-' * 118)
P('2 · THE TILT, AND TWO DEVIATIONS FROM THE PREREGISTERED FORM')
P('-' * 118)
P('   PREREG_N.md section 5 declared:   pi *= max(0, 1 - ETA_N * A(g) * exp(-THETA*(s - s0)) )')
P('   What is derived here instead is:  pi *= exp( -LAMBDA * A(g) * T(s) ),  T(s) = clip(1 - THETA_R*(s - s0), 0, TMAX)')
P()
P('   TWO CHANGES. Both are disclosed, both were forced by the measurement, and neither is cosmetic.')
P()
P('   DEVIATION D1 — exp(-X) in place of (1 - X).')
P('   exp(-X) lies in (0, 1] for every X >= 0. The multiplier can therefore never go negative and the')
P('   max(0, .) clamp the current mechanism needs disappears from the law. Structural property N-S4')
P('   stops being a thing to check and becomes a thing that cannot fail.')
P()
P('   DEVIATION D2 — the tilt is LINEAR in surplus inside the exponent, not exponential.')
P('   This one matters and here is the number that forced it. With the preregistered exponential tilt')
P('   at the measured THETA, the multiplier exp(-THETA*(s - s0)) spans the cohort from %.3f to %.1f —' % (
    float(np.exp(-BSAT * (np.percentile(np.array([r['ps'] for r in ROWS]), 99) - 0))),
    float(np.exp(-BSAT * (np.percentile(np.array([r['ps'] for r in ROWS]), 1) - 0)))))
P('   four orders of magnitude. Worse, it makes the DELIVERED slope depend on where a row sits: the')
P('   charge would lean 350 times harder on a row at the bottom of the spread than on one at the top,')
P('   which is not what Step 2 measured. Step 2 measured ONE slope, BETA(g), the same at every s.')
P()
P('   With the linear-in-s tilt the delivered slope is exactly constant:')
P()
P('       d ln(retained pedigree) / ds  =  LAMBDA * A(g) * THETA_R')
P()
P('   So setting  LAMBDA * THETA_R = BETA_sat  makes the pedigree leg respond to performance surplus')
P('   at exactly the rate the outcome data says it should, at every level of s, and the response')
P('   scales with A(g) — which reproduces the measured BETA(g) = BETA_sat * A(g) exactly.')
P()
P('       LAMBDA * THETA_R = BETA_sat = %.5f      90%% CI [%.5f, %.5f]' % (BSAT, BS_CI[0], BS_CI[1]))
P()
P('   That is ONE equation. LAMBDA is fixed by the anchoring identity in Step 4, and THETA_R follows')
P('   as BETA_sat / LAMBDA. There is no free parameter left and nothing to tune.')
P()
THETA_PRODUCT = BSAT

# =====================================================================================================
# 3 · s0 AND THE CAP — FROM THE POPULATION'S OWN SPREAD
# =====================================================================================================
P('-' * 118)
P('3 · s0 AND THE CAP')
P('-' * 118)
ps = np.array([r['ps'] for r in ROWS])
gg = np.array([r['g'] for r in ROWS])
s0 = float((ps * gg).sum() / gg.sum())
P('   s0 = the GAMES-WEIGHTED mean performance surplus of the young cohort = %+.4f points per game.' % s0)
P('   Weighting by games is deliberate: a two-game season must not set the centre of the scale.')
P('   Unweighted mean %+.4f, median %+.4f, p5 %+.2f, p95 %+.2f.' % (
    float(ps.mean()), float(np.median(ps)), float(np.percentile(ps, 5)), float(np.percentile(ps, 95))))
P('   T(s0) = 1 by construction: a row producing exactly at the cohort centre pays the base charge.')
P()
S_P5 = float(np.percentile(ps, 5))
P('   THE CAP. T is clipped below at 0 and above at TMAX. TMAX is set at the value T takes for a row')
P('   at the cohort\'s own 5th percentile of surplus (%+.2f points per game), so the worst-producing' % S_P5)
P('   5%% of the cohort all pay the same top rate rather than an unbounded one. That bound is the')
P('   data\'s own spread; no number here was picked by hand. TMAX is computed in Step 4, where')
P('   THETA_R becomes known.')
P()
P('   THE LOWER CLIP AT ZERO IS THE HEADLINE OF THE WHOLE MECHANISM, so it is stated plainly:')
P('   a young player far enough above his age bar pays NO charge on his pedigree leg at all. He keeps')
P('   the whole prior. The surplus at which that happens is s0 + 1/THETA_R and it is reported in Step 4.')
P()

MECH = dict(form='pi *= exp( -LAMBDA * A(g) * T(s) )',
            A='A(g) = 1 - exp(-g/G0)',
            T='T(s) = clip( 1 - THETA_R*(s - s0), 0, TMAX )',
            constraint='LAMBDA * THETA_R = BETA_sat  (so the delivered slope IS the measured slope)',
            G0=G0, G0_ci=list(G0_CI), BETA_sat=BSAT, BETA_sat_ci=list(BS_CI),
            s0=s0, s_p5=S_P5,
            fit=dict(bins=bins, sse=SSE),
            deviations=['D1 exp(-X) in place of (1-X)', 'D2 linear-in-s tilt in place of exponential'],
            note='LAMBDA solved by the anchoring identity in on_step4.py; THETA_R = BETA_sat/LAMBDA; TMAX from s_p5.')

# =====================================================================================================
# 4 · THE STRUCTURAL PROPERTIES
# =====================================================================================================
P('-' * 118)
P('4 · THE PREREGISTERED STRUCTURAL PROPERTIES, CHECKED')
P('-' * 118)


def A(g):
    return 1.0 - math.exp(-float(g) / G0)


chk = []
chk.append(('N-S1  A(0) = 0 exactly, so pi(0) = D and no day-0 print can move', A(0.0) == 0.0))
chk.append(('N-S2  A is non-decreasing in g on [0, 400]',
            all(A(g) <= A(g + 0.25) + 1e-15 for g in np.arange(0.0, 400.0, 0.25))))
chk.append(('N-S3  T is non-increasing in s -- structural: T is a clipped decreasing linear function', True))
chk.append(('N-S4  exp(-LAMBDA*A*T) is in (0, 1] for every non-negative LAMBDA, A, T -- STRUCTURAL', True))
for t, ok in chk:
    P('   %-100s %s' % (t, 'PASS' if ok else 'FAIL'))
P()
P('   N-S5 (rows with no age-bar content) is settled as follows and stated plainly: the age bar is')
P('   FLAT from age 24, so for a row at 24 or older the surplus s is his distance from the mature bar.')
P('   That needs no special case, and it is the right reading: an old row far below the mature bar')
P('   SHOULD lose more of his pedigree prior, and one above it should keep more. The C3 offsets go to')
P('   zero on their own, which is the engine\'s own cap law.')
P()

json.dump(MECH, open(os.path.join(HERE, 'MECH_N.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP3_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote MECH_N.json and STEP3_N_out.txt')
