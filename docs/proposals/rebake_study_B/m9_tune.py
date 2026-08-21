"""STUDY B / M9 — OUT-OF-SAMPLE SELECTION FOR THE CONSTRAINED ARM, THEN THE THREE DATA-DESIGN QUESTIONS.

M7 showed the exactly-constrained arm (grad-only pinball + monotonic_cst) is law-3 clean by construction but
OVERFITS at the settings used to demonstrate the mechanism. Removing the leaf line search makes every boosting
step bounded (|gradient| <= 1, hessian == 1), so the incumbent's learning rate and iteration count do not
transfer. This selects them on the WALK-FORWARD score alone.

SELECTION RULE, DECLARED BEFORE THE RUN: lowest MEAN walk-forward pinball over the three splits
(train as-of year <= T, score T+1..T+3, for T in 2014/2017/2020). In-sample loss is reported and never used
to choose.

Then, at the selected settings, the three questions the owner asked:
  (1) the AGE shape          — raw age vs a peak reparameterisation that makes single-peakedness structural
  (2) the POOL arm           — leave as-is / add an arm feature / delete the pool rows
  (3) WEIGHTING vs DELETION  — recency weights against dropping old cohorts

READ-ONLY. Writes only into scratch.
"""
import json, os, sys, time, itertools
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn._loss.loss import PinballLoss

SC = os.path.dirname(os.path.abspath(__file__))
X = np.load(os.path.join(SC, 'X_cm.npy'))
y = np.load(os.path.join(SC, 'y_cm.npy'))
META = json.load(open(os.path.join(SC, 'meta_cm.json')))
YEAR = np.array([m[2] for m in META])
POOL = np.array([bool(m[4]) for m in META], dtype=float)
Q = [0.10, 0.30, 0.50, 0.70, 0.90]
LVL, AGE = 9, 10
SPLITS = (2014, 2017, 2020)
GRID = np.arange(42.0, 118.01, 0.25)
AGRID = np.arange(18.0, 34.01, 0.5)
W6 = np.full(5, 0.2)
RNG = np.random.default_rng(0)


class GradOnlyPinball(PinballLoss):
    """Pinball loss with the post-hoc leaf line search DISABLED.

    gradient_boosting.py:962 calls _update_leaves_values only when `loss.differentiable` is False, and that
    call overwrites every leaf with the empirical quantile of its residuals — discarding the monotone bounds
    the grower just enforced. Setting differentiable=True keeps the constrained leaf values, at the cost of a
    slower-converging fit (hence the selection below).
    NOTE: subclasses the PRIVATE module sklearn._loss. See the study's risk register (D1).
    """
    differentiable = True
    need_update_leaves_values = False


def pinball(yt, yp, q):
    d = yt - yp
    return float(np.mean(np.maximum(q * d, (q - 1) * d)))


def fam(Xtr, ytr, cst, lr, it, msl=25, w=None):
    return {q: HistGradientBoostingRegressor(loss=GradOnlyPinball(quantile=q), max_iter=it, max_depth=4,
                                             learning_rate=lr, min_samples_leaf=msl, monotonic_cst=cst,
                                             early_stopping=False, random_state=0
                                             ).fit(Xtr, ytr, sample_weight=w) for q in Q}


def wf(Xs, cst, lr, it, msl=25, w=None, trmask=None, temask=None):
    per = {}
    for T in SPLITS:
        tr = (YEAR <= T) if trmask is None else ((YEAR <= T) & trmask)
        te = (YEAR > T) & (YEAR <= T + 3)
        if temask is not None:
            te = te & temask
        f = fam(Xs[tr], y[tr], cst, lr, it, msl, w=(None if w is None else w[tr]))
        per[str(T)] = round(float(np.mean([pinball(y[te], f[q].predict(Xs[te]), q) for q in Q])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    return per


def band(f, F):
    return np.sort(np.column_stack([f[q].predict(F) for q in Q]), axis=1)


CST = [0] * 11; CST[LVL] = 1
R = {'_doc': __doc__, 'selection_rule': 'lowest MEAN walk-forward pinball; in-sample never used to choose'}

# ---- incumbent baseline on the same splits ----
per = {}
for T in SPLITS:
    tr = YEAR <= T; te = (YEAR > T) & (YEAR <= T + 3)
    f = {q: GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400, max_depth=4,
                                      learning_rate=0.05, min_samples_leaf=25,
                                      random_state=0).fit(X[tr], y[tr]) for q in Q}
    per[str(T)] = round(float(np.mean([pinball(y[te], f[q].predict(X[te]), q) for q in Q])), 4)
per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
R['incumbent_gbr_quantile'] = per
print('baseline', per, file=sys.stderr)

# ---- (0) hyperparameter selection ----
grid = {}
for lr, it in itertools.product((0.3, 0.6, 1.0), (400, 800)):
    t0 = time.time()
    grid[f'lr{lr}_it{it}'] = wf(X, CST, lr, it)
    print('grid lr%s it%s %s  %.0fs' % (lr, it, grid[f'lr{lr}_it{it}']['mean'], time.time() - t0), file=sys.stderr)
R['selection_grid'] = grid
best = min(grid, key=lambda k: grid[k]['mean'])
LR = float(best.split('_')[0][2:]); IT = int(best.split('_')[1][2:])
R['selected'] = {'key': best, 'learning_rate': LR, 'max_iter': IT, 'walk_forward': grid[best]}

t0 = time.time()
F_SEL = fam(X, y, CST, LR, IT)
R['selected']['fit_seconds_5_quantiles'] = round(time.time() - t0, 2)
R['selected']['insample_pinball_mean'] = round(float(np.mean([pinball(y, F_SEL[q].predict(X), q) for q in Q])), 4)

# law-3 census on EVERY design row at the selected settings
rows = neg = tot = 0; worst = 0.0
G2 = np.arange(42.0, 118.01, 1.0)
for i in range(X.shape[0]):
    F = np.repeat(X[i][None, :], G2.size, axis=0); F[:, LVL] = G2
    d = np.diff(band(F_SEL, F) @ W6); tot += d.size
    n = int((d < -1e-9).sum()); neg += n
    if n:
        rows += 1; worst = min(worst, float(d.min()))
R['selected']['law3_EVERY_design_row'] = {'rows': int(X.shape[0]), 'rows_violating': rows,
                                          'steps': tot, 'negative_steps': neg, 'worst_step': worst}
print('selected', best, R['selected']['law3_EVERY_design_row'], file=sys.stderr)

# ---- (1) THE AGE SHAPE ----
ASTAR = 22.0
Xa = np.column_stack([X, np.maximum(0.0, ASTAR - X[:, AGE]), np.maximum(0.0, X[:, AGE] - ASTAR)])
Xa = Xa[:, [i for i in range(11) if i != AGE] + [11, 12]]     # raw age removed; u,v appended
cst_peak = [0] * 12; cst_peak[LVL] = 1; cst_peak[10] = -1; cst_peak[11] = -1
cst_lvl12 = [0] * 12; cst_lvl12[LVL] = 1
cst_agedown11 = list(CST); cst_agedown11[AGE] = -1

S = RNG.choice(X.shape[0], 200, replace=False)
def age_curve(f, Xs, idx, peak):
    C = []
    for i in idx:
        F = np.repeat(Xs[i][None, :], AGRID.size, axis=0)
        if peak:
            F[:, 10] = np.maximum(0.0, ASTAR - AGRID); F[:, 11] = np.maximum(0.0, AGRID - ASTAR)
        else:
            F[:, AGE] = AGRID
        C.append(band(f, F) @ W6)
    C = np.array(C); sp = 0
    for c in C:
        d = np.diff(c); up = np.where(d > 1e-9)[0]; dn = np.where(d < -1e-9)[0]
        if len(up) == 0 or len(dn) == 0 or up.max() < dn.min():
            sp += 1
    m = C.mean(0)
    return {'pct_rows_single_peaked_or_monotone': round(100.0 * sp / len(C), 2),
            'mean_curve_argmax_age': float(AGRID[int(np.argmax(m))]),
            'mean_curve_at_18_22_26_30_34': [round(float(m[i]), 2) for i in (0, 8, 16, 24, 32)]}

fpeak = fam(Xa, y, cst_peak, LR, IT)
fpeak_free = fam(Xa, y, cst_lvl12, LR, IT)
R['age_design'] = {
    'a_star': ASTAR,
    'construction': 'raw age REPLACED by u=max(0,a*-age) and v=max(0,age-a*), both constrained -1',
    'walk_forward_raw_age_level_only': grid[best],
    'walk_forward_raw_age_plus_agedown': wf(X, cst_agedown11, LR, IT),
    'walk_forward_peakfeatures_constrained': wf(Xa, cst_peak, LR, IT),
    'walk_forward_peakfeatures_unconstrained_age': wf(Xa, cst_lvl12, LR, IT),
    'single_peak_check_constrained': age_curve(fpeak, Xa, S, True),
    'single_peak_check_unconstrained': age_curve(fpeak_free, Xa, S, True),
    'single_peak_check_raw_age_selected_model': age_curve(F_SEL, X, S, False),
}
# level monotonicity must survive the reparameterisation
rows = neg = tot = 0
for i in S:
    F = np.repeat(Xa[i][None, :], GRID.size, axis=0); F[:, LVL] = GRID
    d = np.diff(band(fpeak, F) @ W6); tot += d.size
    n = int((d < -1e-9).sum()); neg += n; rows += 1 if n else 0
R['age_design']['law3_still_exact_under_reparameterisation'] = {
    'rows_sampled': len(S), 'rows_violating': rows, 'negative_steps': neg, 'steps': tot}
print('age done', file=sys.stderr)

# ---- (2) THE POOL ARM ----
Xp = np.column_stack([X, POOL])
cstp = list(CST) + [0]
nat = POOL == 0
poolm = POOL == 1
R['pool_design'] = {
    'rows_pool': int(POOL.sum()), 'rows_national': int(nat.sum()),
    'scored_on_ALL_rows': {
        'A_as_is_no_arm_feature': grid[best],
        'B_add_is_pool_feature': wf(Xp, cstp, LR, IT),
        'C_delete_pool_rows': wf(X, CST, LR, IT, trmask=nat)},
    'scored_on_POOL_rows_only': {
        'A_as_is_no_arm_feature': wf(X, CST, LR, IT, temask=poolm),
        'B_add_is_pool_feature': wf(Xp, cstp, LR, IT, temask=poolm),
        'C_delete_pool_rows': wf(X, CST, LR, IT, trmask=nat, temask=poolm)},
    'scored_on_NATIONAL_rows_only': {
        'A_as_is_no_arm_feature': wf(X, CST, LR, IT, temask=nat),
        'B_add_is_pool_feature': wf(Xp, cstp, LR, IT, temask=nat),
        'C_delete_pool_rows': wf(X, CST, LR, IT, trmask=nat, temask=nat)},
}
print('pool done', file=sys.stderr)

# ---- (3) WEIGHTING vs DELETION ----
W = {'uniform_all_rows': grid[best]}
for tag, hl in (('recency_halflife_4y', 4.0), ('recency_halflife_6y', 6.0), ('recency_halflife_10y', 10.0)):
    W[tag] = wf(X, CST, LR, IT, w=0.5 ** ((YEAR.max() - YEAR) / hl))
for tag, lo in (('DELETE_pre2010', 2010), ('DELETE_pre2014', 2014)):
    W[tag] = wf(X, CST, LR, IT, trmask=(YEAR >= lo))
    W[tag]['n_train_at_T2020'] = int(((YEAR <= 2020) & (YEAR >= lo)).sum())
W['uniform_all_rows'] = dict(W['uniform_all_rows'])
W['uniform_all_rows']['n_train_at_T2020'] = int((YEAR <= 2020).sum())
R['weighting_vs_deletion'] = W

json.dump(R, open(os.path.join(SC, 'm9_out.json'), 'w'), indent=1, sort_keys=True, default=str)
print('WROTE m9_out.json', file=sys.stderr)
