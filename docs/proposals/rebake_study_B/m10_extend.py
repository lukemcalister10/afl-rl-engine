"""STUDY B / M10 — extend the selection grid upward.

M9's grid was still improving at its top corner (lr 1.0, 800 iterations), so the selected point may be a
boundary of the grid rather than an optimum. This extends the search and re-prices the exact-constraint arm
against the incumbent on the same walk-forward splits. Same declared selection rule: lowest MEAN walk-forward
pinball. READ-ONLY.
"""
import json, os, sys, time, itertools
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn._loss.loss import PinballLoss

SC = os.path.dirname(os.path.abspath(__file__))
X = np.load(os.path.join(SC, 'X_cm.npy'))
y = np.load(os.path.join(SC, 'y_cm.npy'))
META = json.load(open(os.path.join(SC, 'meta_cm.json')))
YEAR = np.array([m[2] for m in META])
Q = [0.10, 0.30, 0.50, 0.70, 0.90]
LVL = 9
SPLITS = (2014, 2017, 2020)
CST = [0] * 11; CST[LVL] = 1
W6 = np.full(5, 0.2)


class GradOnlyPinball(PinballLoss):
    differentiable = True
    need_update_leaves_values = False


def pinball(yt, yp, q):
    d = yt - yp
    return float(np.mean(np.maximum(q * d, (q - 1) * d)))


def fam(Xtr, ytr, lr, it, msl=25):
    return {q: HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), max_iter=it, max_depth=4,
                                             learning_rate=lr, min_samples_leaf=msl, monotonic_cst=CST,
                                             early_stopping=False, random_state=0).fit(Xtr, ytr) for q in Q}


def wf(lr, it, msl=25):
    per = {}
    for T in SPLITS:
        tr = YEAR <= T; te = (YEAR > T) & (YEAR <= T + 3)
        f = fam(X[tr], y[tr], lr, it, msl)
        per[str(T)] = round(float(np.mean([pinball(y[te], f[q].predict(X[te]), q) for q in Q])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    return per


R = {'_doc': __doc__, 'incumbent_walk_forward_mean': 3.9267}
g = {}
for lr, it, msl in [(1.0, 1600, 25), (1.5, 800, 25), (1.5, 1600, 25), (2.0, 1600, 25),
                    (1.0, 3200, 25), (1.0, 1600, 60), (1.5, 1600, 60)]:
    t0 = time.time()
    g[f'lr{lr}_it{it}_msl{msl}'] = wf(lr, it, msl)
    print('lr%s it%s msl%s -> %s  (%.0fs)' % (lr, it, msl, g[f'lr{lr}_it{it}_msl{msl}']['mean'],
                                              time.time() - t0), file=sys.stderr)
R['extended_grid'] = g
best = min(g, key=lambda k: g[k]['mean'])
R['best_extended'] = {'key': best, 'walk_forward': g[best]}

lr = float(best.split('_')[0][2:]); it = int(best.split('_')[1][2:]); msl = int(best.split('_')[2][3:])
t0 = time.time()
F = fam(X, y, lr, it, msl)
R['best_extended']['fit_seconds_5_quantiles'] = round(time.time() - t0, 2)
R['best_extended']['insample_pinball_mean'] = round(
    float(np.mean([pinball(y, F[q].predict(X), q) for q in Q])), 4)

G2 = np.arange(42.0, 118.01, 1.0)
rows = neg = tot = 0; worst = 0.0
for i in range(X.shape[0]):
    A = np.repeat(X[i][None, :], G2.size, axis=0); A[:, LVL] = G2
    B = np.sort(np.column_stack([F[q].predict(A) for q in Q]), axis=1) @ W6
    d = np.diff(B); tot += d.size
    n = int((d < -1e-9).sum()); neg += n
    if n:
        rows += 1; worst = min(worst, float(d.min()))
R['best_extended']['law3_EVERY_design_row'] = {'rows': int(X.shape[0]), 'rows_violating': rows,
                                               'steps': tot, 'negative_steps': neg, 'worst_step': worst}
json.dump(R, open(os.path.join(SC, 'm10_out.json'), 'w'), indent=1, sort_keys=True, default=str)
print('WROTE m10_out.json', file=sys.stderr)
