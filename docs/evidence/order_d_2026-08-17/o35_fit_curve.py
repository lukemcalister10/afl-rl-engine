#!/usr/bin/env python3
"""ORDER D — D1/D2: THE PICK-CURVE FIT AND THE REDISTRIBUTION CONSTANT (PREREG_D.md, pushed first).

Plain words: we measure, player by player, how much a year-one sit raises the odds of a
five-year washout, and how that penalty changes with draft pick — as a SMOOTH line in log(pick),
never a band. Then we solve the one constant that makes the new pick-shaped fade average out to
exactly the ruled fade over the sitter population (the curve redistributes; it does not change
the total).
"""
import os, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
BARS = {'KPD': 65.4, 'KPF': 63.8, 'MID': 77.1, 'RUCK': 75.5, 'SD': 75.3, 'SF': 67.9}
D2 = 0.5582775239783688      # the ruled depth-2 fade (31-F row, re-derived at deviation 0.0)

A = json.load(open(SP + '/per_entrant_O32RFINAL.json'))
FM = {'paddy-mccartin', 'thomas-boyd'}
ROWS = []
for r in A['recs']:
    if r['key'] in FM or not (r.get('teaches_curve') and r['type'] == 'ND'):
        continue
    if not (2005 <= r['year'] <= 2020) or not r.get('pick') or not (1 <= r['pick'] <= 64):
        continue
    sdv = 0.0
    for s in r['seasons']:
        if r['year'] < s['year'] <= r['year'] + 5 and s.get('bar') in BARS:
            sdv += float(s['games']) * max(0.0, float(s['avg']) - BARS[s['bar']])
    ROWS.append(dict(key=r['key'], pick=int(r['pick']), g1=int(r.get('games_yr1') or 0),
                     w=1.0 if sdv <= 0.0 else 0.0))
SAT = [r for r in ROWS if r['g1'] == 0]
CTL = [r for r in ROWS if r['g1'] >= 11]
print('population: %d ND entrants 2005-2020; sitters %d, played-11+ controls %d'
      % (len(ROWS), len(SAT), len(CTL)))

def logistic_fit(rows):
    """IRLS logistic: y ~ 1 + ln(pick) + SAT + SAT*ln(pick). Returns beta[4]."""
    X = np.array([[1.0, math.log(r['pick']), (1.0 if r['g1'] == 0 else 0.0),
                   (math.log(r['pick']) if r['g1'] == 0 else 0.0)] for r in rows])
    y = np.array([r['w'] for r in rows])
    b = np.zeros(4)
    for _ in range(60):
        eta = X @ b
        mu = 1.0 / (1.0 + np.exp(-eta))
        Wd = np.clip(mu * (1 - mu), 1e-9, None)
        z = eta + (y - mu) / Wd
        XtW = X.T * Wd
        b_new = np.linalg.solve(XtW @ X + 1e-9 * np.eye(4), XtW @ z)
        if np.max(np.abs(b_new - b)) < 1e-10:
            b = b_new; break
        b = b_new
    return b

FITROWS = SAT + CTL
b = logistic_fit(FITROWS)
G0, G1 = float(b[2]), float(b[3])
print('primary fit (SAT vs played-11+): s(p) = %.4f %+.4f * ln(pick)' % (G0, G1))
for p in (1, 7, 10, 16, 20, 30, 40, 50, 64):
    print('  s(%2d) = %.4f' % (p, G0 + G1 * math.log(p)))

# bootstrap (player rows are independent players; B=1000 seed 35)
RNG = np.random.default_rng(35)
BB = []
arr = FITROWS
for _ in range(1000):
    idx = RNG.integers(0, len(arr), len(arr))
    try:
        bb = logistic_fit([arr[i] for i in idx])
        BB.append([bb[2], bb[3]])
    except Exception:
        continue
BB = np.array(BB)
ci0 = [float(np.percentile(BB[:, 0], 5)), float(np.percentile(BB[:, 0], 95))]
ci1 = [float(np.percentile(BB[:, 1], 5)), float(np.percentile(BB[:, 1], 95))]
print('bootstrap 90%% CI: gamma0 [%.3f, %.3f]  gamma1 [%.3f, %.3f]  (B=%d ok)' % (*ci0, *ci1, len(BB)))
sh = float(np.mean(BB[:, 1] < 0))
print('share of bootstrap draws with gamma1 < 0 (the ruled direction): %.1f%%' % (100 * sh))

# secondary spec: SAT vs ALL played
b2 = logistic_fit([r for r in ROWS])
print('secondary (SAT vs all played): s(p) = %.4f %+.4f * ln(pick)' % (b2[2], b2[3]))

def s_of(p):
    return G0 + G1 * math.log(max(1, min(64, p)))

# ---- the redistribution constant: mean over sitters of D2^kappa = D2, kappa=clip(s/snorm,.5,2) ----
def kap(p, snorm):
    return float(np.clip(s_of(p) / snorm, 0.5, 2.0))

def ident(snorm):
    return float(np.mean([D2 ** kap(r['pick'], snorm) for r in SAT])) - D2

lo, hi = 0.05, 20.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    # mean fade rises as snorm rises (kappa falls); ident increasing in snorm
    if ident(mid) < 0:
        lo = mid
    else:
        hi = mid
SNORM = 0.5 * (lo + hi)
print('redistribution constant s_norm = %.6f ; identity residual %.2e (target 0 at depth 2)'
      % (SNORM, ident(SNORM)))
KT = {p: kap(p, SNORM) for p in (1, 5, 7, 10, 16, 19, 20, 21, 30, 40, 50, 53, 64)}
print('kappa(pick):', {p: round(v, 4) for p, v in KT.items()})
d3 = 0.2747857941376827; d4 = 0.3972708510774922
print('reported (not pinned): pooled depth-3 fade %.4f vs ruled %.4f ; depth-4 %.4f vs ruled %.4f'
      % (float(np.mean([d3 ** kap(r['pick'], SNORM) for r in SAT])), d3,
         float(np.mean([d4 ** kap(r['pick'], SNORM) for r in SAT])), d4))
supp = {}
for name, plo, phi in (('1-10', 1, 10), ('11-20', 11, 20), ('21-30', 21, 30), ('31-40', 31, 40), ('41-64', 41, 64)):
    supp[name] = sum(1 for r in SAT if plo <= r['pick'] <= phi)
print('sitter data support by region:', supp, '(the early end of the curve leans on the trend — n=17 top-10 sitters)')

json.dump(dict(order='ORDER D — the pick-curve sitter fade (R-PICKFADE)',
               family='logit P(washout5) = a + b*ln(pick) + (g0 + g1*ln(pick))*SAT; SAT vs played-11+',
               gamma0=G0, gamma1=G1, ci_gamma0=ci0, ci_gamma1=ci1,
               boot_share_gamma1_negative=sh,
               secondary_all_played=dict(gamma0=float(b2[2]), gamma1=float(b2[3])),
               s_norm=SNORM, clip=[0.5, 2.0], kappa_table={str(p): v for p, v in KT.items()},
               identity='mean over fitted sitters of D(2)^kappa(pick) == D(2), pinned; depth 3/4 reported',
               n=dict(rows=len(ROWS), sat=len(SAT), ctl=len(CTL)), support_sat=supp,
               d2=D2),
          open(os.path.join(HERE, 'O35_CURVE.json'), 'w'), indent=1, sort_keys=True)
print('written: O35_CURVE.json')
