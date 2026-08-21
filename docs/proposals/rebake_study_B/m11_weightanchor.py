"""STUDY B / M11 — a robustness check on the recency-weighting result.

M55 weighted rows by 0.5 ** ((YEAR.max() - YEAR)/halflife) with YEAR.max() = 2026, the GLOBAL last as-of
year. On the T=2014 walk-forward split that means every training row is already far down the decay curve,
which could be responsible for the result rather than the weighting idea itself. This re-runs the comparison
with the half-life anchored to the END OF EACH TRAINING WINDOW instead, which is the construction a real
rebake would use. If the answer flips, M55 is an artefact of the anchor. READ-ONLY.
"""
import json, os, sys
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn._loss.loss import PinballLoss

SC = os.path.dirname(os.path.abspath(__file__))
X = np.load(os.path.join(SC, 'X_cm.npy'))
y = np.load(os.path.join(SC, 'y_cm.npy'))
YEAR = np.array([m[2] for m in json.load(open(os.path.join(SC, 'meta_cm.json')))])
Q = [0.10, 0.30, 0.50, 0.70, 0.90]
CST = [0] * 11; CST[9] = 1
SPLITS = (2014, 2017, 2020)
LR, IT = 1.0, 800


class GradOnlyPinball(PinballLoss):
    differentiable = True
    need_update_leaves_values = False


def pinball(yt, yp, q):
    d = yt - yp
    return float(np.mean(np.maximum(q * d, (q - 1) * d)))


def wf(halflife, anchor):
    """anchor='global' -> decay measured from 2026; anchor='window' -> from the split's own last year T."""
    per = {}
    for T in SPLITS:
        tr = YEAR <= T; te = (YEAR > T) & (YEAR <= T + 3)
        if halflife is None:
            w = None
        else:
            ref = YEAR.max() if anchor == 'global' else T
            w = (0.5 ** ((ref - YEAR) / halflife))[tr]
        f = {q: HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), max_iter=IT, max_depth=4,
                                              learning_rate=LR, min_samples_leaf=25, monotonic_cst=CST,
                                              early_stopping=False, random_state=0
                                              ).fit(X[tr], y[tr], sample_weight=w) for q in Q}
        per[str(T)] = round(float(np.mean([pinball(y[te], f[q].predict(X[te]), q) for q in Q])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    return per


R = {'_doc': __doc__, 'uniform': wf(None, None)}
print('uniform', R['uniform'], file=sys.stderr)
for hl in (6.0, 10.0, 16.0):
    for anchor in ('global', 'window'):
        k = f'halflife_{int(hl)}y_anchor_{anchor}'
        R[k] = wf(hl, anchor)
        print(k, R[k]['mean'], file=sys.stderr)
json.dump(R, open(os.path.join(SC, 'm11_out.json'), 'w'), indent=1, sort_keys=True)
print('WROTE m11_out.json', file=sys.stderr)
