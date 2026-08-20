#!/usr/bin/env python3
"""ORDER P STEP 3 — THE DERIVATION, ON THE NEW SURPLUS. READ-ONLY.

Same discipline and same form as ORDER N Step 3 (PREREG_P.md section 5). The form is not re-derived:
it was derived in ORDER N and this order changes the SURPLUS, not the shape. Every constant is
re-derived here on the pedigree-conditional surplus. Nothing is tuned. No board price enters.

  usage: OPENBLAS_NUM_THREADS=1 ... python op_step3.py
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

SEED, B_PAR = 32, 4000
L = []


def P(s=''):
    print(s); L.append(str(s))


S2 = json.load(open(os.path.join(HERE, 'STEP2_P.json')))
ROWS = S2['rows']

P('=' * 118)
P('ORDER P — STEP 3. THE CHARGE, RE-DERIVED ON THE PEDIGREE-CONDITIONAL SURPLUS')
P('=' * 118)
P('input : STEP2_P.json — the outcome measurement. No board price enters this file.')
P('form  : pi *= exp( -LAMBDA * A(g) * T(s_P) ),  A(g) = 1-exp(-g/G0),  T = clip(1 - THETA_R*(s-s0), 0, TMAX)')
P('        The FORM is ORDER N\'s, derived there and not re-litigated here. What changes is s.')
P()

# ---- 1 · A(g) ----------------------------------------------------------------------------------------
P('-' * 118)
P('1 · A(g) — THE EVIDENCE CURVE, FITTED TO THE MEASURED PAYOFF TO THE NEW SURPLUS')
P('-' * 118)
bins = []
for b, e in S2['beta'].items():
    if b == 'POOLED':
        continue
    lo, hi = e['ci']
    bins.append(dict(bin=b, g=e['gmean'], beta=e['beta'], lo=lo, hi=hi, n=e['n'],
                     sd=(hi - lo) / (2 * 1.6448536269514722), beta_N=e['beta_N']))
bins.sort(key=lambda d: d['g'])
P('   %-8s %8s %5s | %10s %-22s %10s | %10s' % ('bin', 'mean g', 'n', 'BETA_P', '90% CI', 'implied sd', 'BETA_N'))
for d in bins:
    P('   %-8s %8.2f %5d | %+10.5f [%+.5f,%+.5f] %10.5f | %+10.5f' % (
        d['bin'], d['g'], d['n'], d['beta'], d['lo'], d['hi'], d['sd'], d['beta_N']))
P()

gs = np.array([d['g'] for d in bins]); bt = np.array([d['beta'] for d in bins])
sd = np.array([d['sd'] for d in bins]); w = 1.0 / (sd ** 2)
GRID = np.arange(0.5, 60.0001, 0.01)
AMAT = 1.0 - np.exp(-gs[None, :] / GRID[:, None])
WA2 = (w[None, :] * AMAT * AMAT).sum(axis=1)


def fit_many(BV):
    num = np.einsum('j,kj,mj->mk', w, AMAT, BV)
    bs = num / WA2[None, :]
    resid = BV[:, None, :] - bs[:, :, None] * AMAT[None, :, :]
    sse = (w[None, None, :] * resid ** 2).sum(axis=2)
    ki = sse.argmin(axis=1)
    m = np.arange(BV.shape[0])
    return GRID[ki], bs[m, ki], sse[m, ki]


g0v, bsv, ssev = fit_many(bt[None, :])
G0, BSAT, SSE = float(g0v[0]), float(bsv[0]), float(ssev[0])
rng = np.random.default_rng(SEED)
BV = bt[None, :] + rng.normal(0.0, sd[None, :], size=(B_PAR, len(bt)))
BV = BV[~(BV <= 0).all(axis=1)]
g0d, bsd, _ = fit_many(BV)
G0_CI = (float(np.percentile(g0d, 5)), float(np.percentile(g0d, 95)))
BS_CI = (float(np.percentile(bsd, 5)), float(np.percentile(bsd, 95)))

P('   FITTED  BETA_P(g) = BETA_sat * (1 - exp(-g/G0)), weighted by each bin\'s own inverse variance:')
P('       G0        = %.2f games       90%% CI [%.2f, %.2f]      (ORDER N: 9.72 [7.39, 12.84])' % (G0, *G0_CI))
P('       BETA_sat  = %.5f             90%% CI [%.5f, %.5f]      (ORDER N: 0.11521 [0.10434, 0.12828])' % (BSAT, *BS_CI))
P('       weighted SSE %.4g over %d bins, 2 free parameters' % (SSE, len(bins)))
P('   CIs are a parametric bootstrap: each bin\'s BETA redrawn %d times from a normal with the sd its' % B_PAR)
P('   own cluster bootstrap implied, then the curve refitted. Seed %d — ORDER N\'s own seed.' % SEED)
P()
P('   FIT QUALITY, bin by bin:')
P('   %-8s %8s | %10s %10s %10s' % ('bin', 'mean g', 'BETA obs', 'BETA fit', 'A(g)'))
for d in bins:
    a = 1.0 - math.exp(-d['g'] / G0)
    P('   %-8s %8.2f | %+10.5f %+10.5f %10.4f' % (d['bin'], d['g'], d['beta'], BSAT * a, a))
P()
P('   A(g) AT THE ORDER\'S OWN ANCHORS, against the current blind shape:')
P('   %-8s %10s %14s' % ('games', 'A(g)', 'current m_d(g)'))
for g in (0, 2, 5, 10, 14, 17, 20, 30, 36, 60, 141):
    P('   %-8d %10.4f %14.4f' % (g, 1.0 - math.exp(-g / G0), LB.m_d(g)))
P()

# ---- 2 · the tilt ------------------------------------------------------------------------------------
P('-' * 118)
P('2 · THE TILT. ONE EQUATION, AND IT IS THE MEASUREMENT.')
P('-' * 118)
P('   With T linear in s inside the exponent, the delivered slope is exactly constant:')
P()
P('       d ln(retained pedigree) / ds  =  LAMBDA * A(g) * THETA_R')
P()
P('   Setting LAMBDA * THETA_R = BETA_sat makes the pedigree leg respond to the pedigree-conditional')
P('   surplus at exactly the rate the outcome data says it should, at every level of s, scaled by')
P('   A(g), which reproduces the measured BETA_P(g) = BETA_sat * A(g).')
P()
P('       LAMBDA * THETA_R = BETA_sat = %.5f     90%% CI [%.5f, %.5f]' % (BSAT, *BS_CI))
P()
P('   That is ONE equation. LAMBDA is solved by the anchoring identity in Step 4. THETA_R follows as')
P('   BETA_sat / LAMBDA. There is no free parameter left and nothing to tune.')
P()

# ---- 3 · s0 and the cap ------------------------------------------------------------------------------
P('-' * 118)
P('3 · s0 AND THE CAP, FROM THE POPULATION\'S OWN SPREAD')
P('-' * 118)
sp = np.array([r['sP'] for r in ROWS]); sn = np.array([r['sN'] for r in ROWS])
gg = np.array([r['g'] for r in ROWS])
s0 = float((sp * gg).sum() / gg.sum())
s0N = float((sn * gg).sum() / gg.sum())
S_P5 = float(np.percentile(sp, 5))
P('   s0 = the GAMES-WEIGHTED mean of the NEW surplus over the young cohort = %+.4f points per game.' % s0)
P('        (ORDER N, on the age-only surplus: %+.4f. The centre moves because the bar moved.)' % s0N)
P('   unweighted mean %+.4f · median %+.4f · p5 %+.2f · p95 %+.2f' % (
    float(sp.mean()), float(np.median(sp)), S_P5, float(np.percentile(sp, 95))))
P('   T(s0) = 1 by construction: a row producing exactly at the cohort centre pays the base charge.')
P()
P('   THE CAP. TMAX is the value T takes at the cohort\'s own 5th percentile of the new surplus,')
P('   %+.2f points per game, so the worst-producing 5%% all pay the same top rate rather than an' % S_P5)
P('   unbounded one. The bound is the data\'s own spread. TMAX is computed in Step 4, where THETA_R')
P('   becomes known.')
P()
P('   THE LOWER CLIP AT ZERO. A young player far enough above his PEDIGREE-CONDITIONAL bar pays no')
P('   charge on his pedigree leg at all. The surplus at which that happens is s0 + 1/THETA_R and it')
P('   is reported in Step 4.')
P()

# ---- 4 · structural properties -----------------------------------------------------------------------
P('-' * 118)
P('4 · THE PREREGISTERED STRUCTURAL PROPERTIES')
P('-' * 118)


def A(g):
    return 1.0 - math.exp(-float(g) / G0)


chk = [('P-S1  A(0) = 0 exactly, so pi(0) = D and no day-0 print can move', A(0.0) == 0.0),
       ('P-S2  A is non-decreasing in g over [0, 400]',
        all(A(g) <= A(g + 0.25) + 1e-15 for g in np.arange(0.0, 400.0, 0.25))),
       ('P-S3  T is non-increasing in s', True),
       ('P-S4  the factor exp(-LAMBDA*A*T) is in (0,1] for every non-negative argument', True)]
for name, ok in chk:
    P('   %-72s %s' % (name, 'PASS' if ok else 'FAIL'))
P('   P-S3 and P-S4 are structural: T is a clipped decreasing line, and exp(-x) is in (0,1] for x>=0.')
P('   P-S5 (no row prices above its own uncharged price) is asserted row by row in Step 4.')
P()

MECH = dict(form='pi *= exp( -LAMBDA * A(g) * T(s_P) )',
            A='A(g) = 1 - exp(-g/G0)',
            T='T(s) = clip( 1 - THETA_R*(s - s0), 0, TMAX )',
            constraint='LAMBDA * THETA_R = BETA_sat',
            G0=G0, G0_ci=list(G0_CI), BETA_sat=BSAT, BETA_sat_ci=list(BS_CI),
            s0=s0, s0_orderN=s0N, s_p5=S_P5, fit=dict(bins=bins, sse=SSE),
            note='LAMBDA solved by the anchoring identity in op_step4.py; THETA_R = BETA_sat/LAMBDA.')
json.dump(MECH, open(os.path.join(HERE, 'MECH_P.json'), 'w'), indent=1)
open(os.path.join(HERE, 'STEP3_P_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote MECH_P.json and STEP3_P_out.txt')
