"""STUDY B / M7 — CAN LAW 3 BE MADE STRUCTURAL?

M5 measured that HistGBR's monotonic_cst is only APPROXIMATE under loss='quantile'. This script
locates the mechanism, proves it, and prices the one construction that makes the constraint EXACT.

MECHANISM (read out of the pinned sklearn 1.8.0 source):
  sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py:962
      if not self._loss.differentiable:  _update_leaves_values(...)
  PinballLoss.differentiable = False, so after the grower has enforced the monotone bounds every leaf
  value is OVERWRITTEN with the empirical quantile of that leaf's residuals. The overwrite does not
  respect the bounds. Under squared_error there is no overwrite and the constraint is exact.

ARMS
  A  GradientBoostingRegressor(loss='quantile')                 the incumbent, no constraint possible
  C  HistGBR(loss='quantile', monotonic_cst)                    the prereg's "FIX 1", as written
  F  HistGBR(loss=<pinball, line search disabled>, monotonic_cst)  law 3 BY CONSTRUCTION
  G  F + a signed AGE constraint (-1)
READ-ONLY; writes only into scratch.
"""
import json, os, sys, time
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn._loss.loss import PinballLoss

SC = os.path.dirname(os.path.abspath(__file__))
X = np.load(os.path.join(SC, 'X_cm.npy'))
y = np.load(os.path.join(SC, 'y_cm.npy'))
META = json.load(open(os.path.join(SC, 'meta_cm.json')))
YEAR = np.array([m[2] for m in META])
Q = [0.10, 0.30, 0.50, 0.70, 0.90]
LVL, AGE = 9, 10
CST_L = [0] * 11; CST_L[LVL] = 1
CST_LA = list(CST_L); CST_LA[AGE] = -1
GRID = np.arange(42.0, 118.01, 0.25)
W6 = np.full(5, 0.2)
RNG = np.random.default_rng(0)


class GradOnlyPinball(PinballLoss):
    """PinballLoss with the post-hoc leaf line search DISABLED.

    `differentiable = True` is what stops gradient_boosting.py calling _update_leaves_values, so the
    grower's monotone-constrained leaf values survive into the predictor. The fit becomes plain
    gradient boosting on the pinball loss (hessians are already fixed at 1 by PinballLoss itself),
    which needs a larger learning rate and more iterations to reach the same fit.
    NOTE: this subclasses a PRIVATE sklearn module (sklearn._loss). See the study's risk register.
    """
    differentiable = True
    need_update_leaves_values = False


def pinball(yt, yp, q):
    d = yt - yp
    return float(np.mean(np.maximum(q * d, (q - 1) * d)))


def fit(kind, Xtr, ytr, cst=None, w=None):
    out = {}
    for q in Q:
        if kind == 'gbr':
            m = GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400, max_depth=4,
                                          learning_rate=0.05, min_samples_leaf=25, random_state=0)
        elif kind == 'hist':
            m = HistGradientBoostingRegressor(loss='quantile', quantile=q, max_iter=400, max_depth=4,
                                              learning_rate=0.05, min_samples_leaf=25,
                                              monotonic_cst=cst, early_stopping=False, random_state=0)
        else:   # gradonly
            m = HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), max_iter=1200,
                                              max_depth=4, learning_rate=2.0, min_samples_leaf=25,
                                              monotonic_cst=cst, early_stopping=False, random_state=0)
        m.fit(Xtr, ytr, sample_weight=w)
        out[q] = m
    return out


def band(fam, F):
    return np.sort(np.column_stack([fam[q].predict(F) for q in Q]), axis=1)


def law3(fam, idx):
    rows = neg = tot = 0; worst = 0.0; worstpct = 0.0
    for i in idx:
        F = np.repeat(X[i][None, :], GRID.size, axis=0); F[:, LVL] = GRID
        w = band(fam, F) @ W6
        d = np.diff(w); tot += d.size
        n = int((d < -1e-9).sum()); neg += n
        if n:
            rows += 1
            worst = min(worst, float(d.min()))
            worstpct = min(worstpct, float((d / np.maximum(w[:-1], 1e-9)).min()))
    return {'rows_sampled': len(idx), 'rows_with_a_down_step': rows,
            'pct_rows_violating': round(100.0 * rows / len(idx), 2),
            'pct_steps_negative': round(100.0 * neg / max(tot, 1), 4),
            'worst_step_pct_of_band': round(100.0 * worstpct, 4)}


ARMS = {'A_gbr_incumbent': ('gbr', None),
        'C_histgbr_quantile_cst_prereg_FIX1': ('hist', CST_L),
        'F_gradonly_pinball_cst_LEVEL': ('gradonly', CST_L),
        'G_gradonly_pinball_cst_LEVEL_and_AGEDOWN': ('gradonly', CST_LA),
        'F0_gradonly_pinball_NO_cst_control': ('gradonly', None)}

R = {'_doc': __doc__, 'design_rows': int(X.shape[0])}
SAMPLE = RNG.choice(X.shape[0], 200, replace=False)
THIN = np.where(X[:, 7] < 12.0)[0]
THIN_S = RNG.choice(THIN, 200, replace=False)

R['arms'] = {}
FIT = {}
for name, (kind, cst) in ARMS.items():
    t0 = time.time()
    fam = fit(kind, X, y)  if False else fit(kind, X, y, cst=cst)
    dt = time.time() - t0
    FIT[name] = fam
    R['arms'][name] = {
        'fit_seconds_5_quantiles': round(dt, 2),
        'insample_pinball': {str(q): round(pinball(y, fam[q].predict(X), q), 4) for q in Q},
        'insample_pinball_mean': round(float(np.mean([pinball(y, fam[q].predict(X), q) for q in Q])), 4),
        'law3_all_rows': law3(fam, SAMPLE),
        'law3_thin_evidence_rows': law3(fam, THIN_S)}
    print('done', name, round(dt, 1), 's', file=sys.stderr)

# ---- walk-forward, the honest out-of-sample read ----
WF = {}
for name, (kind, cst) in ARMS.items():
    rows = {}
    for T in (2014, 2017, 2020):
        tr = YEAR <= T; te = (YEAR > T) & (YEAR <= T + 3)
        fam = fit(kind, X[tr], y[tr], cst=cst)
        rows[str(T)] = {'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                        'pinball_mean': round(float(np.mean([pinball(y[te], fam[q].predict(X[te]), q) for q in Q])), 4)}
    WF[name] = rows
    print('wf', name, file=sys.stderr)
R['walk_forward'] = WF

# ---- the AGE question, measured on the constrained family ----
AG = np.arange(18.0, 34.01, 0.5)
def age_pd(fam, idx):
    C = []
    for i in idx:
        F = np.repeat(X[i][None, :], AG.size, axis=0); F[:, AGE] = AG
        C.append(band(fam, F) @ W6)
    C = np.array(C); mean = C.mean(0); d = np.diff(C, 1)
    return {'grid': [float(a) for a in AG],
            'mean_curve': [round(float(v), 3) for v in mean],
            'argmax_age': float(AG[int(np.argmax(mean))]),
            'rise_to_peak': round(float(mean.max() - mean[0]), 3),
            'fall_from_peak': round(float(mean.max() - mean[-1]), 3),
            'pct_rows_monotone_nonincreasing': round(100.0 * float((d <= 1e-9).all(1).mean()), 2),
            'pct_rows_monotone_nondecreasing': round(100.0 * float((d >= -1e-9).all(1).mean()), 2),
            'pct_rows_single_peaked': round(100.0 * float(np.mean([
                (np.argmax(c) not in (0, len(c) - 1)) for c in C])), 2)}
R['age_shape'] = {'F_gradonly_level_only': age_pd(FIT['F_gradonly_pinball_cst_LEVEL'], SAMPLE),
                  'F0_unconstrained_control': age_pd(FIT['F0_gradonly_pinball_NO_cst_control'], SAMPLE)}
for tag, m in (('tenure_le_3', X[:, 8] <= 3), ('tenure_ge_8', X[:, 8] >= 8)):
    s = RNG.choice(np.where(m)[0], 150, replace=False)
    R['age_shape'][f'F0_unconstrained__{tag}'] = age_pd(FIT['F0_gradonly_pinball_NO_cst_control'], s)

json.dump(R, open(os.path.join(SC, 'm7_out.json'), 'w'), indent=1, sort_keys=True, default=str)
print('WROTE m7_out.json', file=sys.stderr)
