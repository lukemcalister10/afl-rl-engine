"""STUDY B / M5 — THE ESTIMATOR BAKE-OFF.

On the design matrix rebuilt from the CURRENT store (M2: 13,220 x 11), compare:
  A  the incumbent construction : GradientBoostingRegressor(loss='quantile'), no shape constraint
  B  the modern unconstrained   : HistGradientBoostingRegressor(loss='quantile'), no shape constraint
  C  the modern level-monotone  : HistGBR + monotonic_cst[+1] on the LEVEL feature (index 9)
  D  C + a signed AGE constraint (-1 on feature 10), the owner's "should age get direction?"

Measured on each: pinball loss (in-sample + walk-forward by as-of year), and a LAW-3 CENSUS —
how often a rising level buys a falling band on real rows.

READ-ONLY: reads only the scratch design matrix and the pinned pickles; writes only into scratch.
"""
import json, os, sys, time, pickle, hashlib
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor

SC = os.path.dirname(os.path.abspath(__file__))
X = np.load(os.path.join(SC, 'X_cm.npy'))
y = np.load(os.path.join(SC, 'y_cm.npy'))
META = json.load(open(os.path.join(SC, 'meta_cm.json')))
YEAR = np.array([m[2] for m in META])
ISPOOL = np.array([bool(m[4]) for m in META])
Q = [0.10, 0.30, 0.50, 0.70, 0.90]
LVL, AGE = 9, 10
FN = ['oh_MID', 'oh_SD', 'oh_SF', 'oh_KPD', 'oh_KPF', 'oh_RUCK',
      'log_effpk', 'exposure', 'tenure', 'level', 'age']
RNG = np.random.default_rng(0)
R = {'design': {'rows': int(X.shape[0]), 'features': int(X.shape[1]), 'feature_names': FN}}


def pinball(yt, yp, q):
    d = yt - yp
    return float(np.mean(np.maximum(q * d, (q - 1) * d)))


def fit_family(kind, Xtr, ytr, cst=None, seed=0, weight=None):
    out = {}
    for q in Q:
        if kind == 'gbr':
            m = GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400, max_depth=4,
                                          learning_rate=0.05, min_samples_leaf=25, random_state=seed)
        else:
            m = HistGradientBoostingRegressor(loss='quantile', quantile=q, max_iter=400, max_depth=4,
                                              learning_rate=0.05, min_samples_leaf=25,
                                              monotonic_cst=cst, early_stopping=False,
                                              random_state=seed)
        m.fit(Xtr, ytr, sample_weight=weight)
        out[q] = m
    return out


def band(models, F):
    return np.sort(np.column_stack([models[q].predict(F) for q in Q]), axis=1)


CST_LVL = [0] * 11; CST_LVL[LVL] = 1
CST_LVL_AGEDOWN = list(CST_LVL); CST_LVL_AGEDOWN[AGE] = -1
CST_LVL_AGEUP = list(CST_LVL); CST_LVL_AGEUP[AGE] = 1

ARMS = {
    'A_gbr_classic_unconstrained': ('gbr', None),
    'B_histgbr_unconstrained': ('hist', None),
    'C_histgbr_level_monotone': ('hist', CST_LVL),
    'D_histgbr_level_mono_age_down': ('hist', CST_LVL_AGEDOWN),
    'E_histgbr_level_mono_age_up': ('hist', CST_LVL_AGEUP),
}

# ---------------- 1. in-sample fit + fit cost ----------------
FITTED = {}
R['arms'] = {}
CACHE = os.path.join(SC, '_fitcache.pkl')
_cache = pickle.load(open(CACHE, 'rb')) if os.path.exists(CACHE) else {}
for name, (kind, cst) in ARMS.items():
    t0 = time.time()
    if name in _cache:
        fam, dt = _cache[name]
    else:
        fam = fit_family(kind, X, y, cst=cst)
        dt = time.time() - t0
        _cache[name] = (fam, dt)
        pickle.dump(_cache, open(CACHE, 'wb'))
    FITTED[name] = fam
    R['arms'][name] = {'estimator': 'GradientBoostingRegressor' if kind == 'gbr' else 'HistGradientBoostingRegressor',
                       'monotonic_cst': cst, 'fit_seconds_5_quantiles': round(dt, 2),
                       'insample_pinball': {str(q): pinball(y, fam[q].predict(X), q) for q in Q}}
    print('fitted', name, round(dt, 1), 's', file=sys.stderr)

# ---------------- 2. walk-forward by as-of year ----------------
# Train on rows whose as-of year <= T, score rows with as-of year in (T, T+3]. This is the
# design-relevant split: the model must price a player from evidence available at the time.
WF = {}
for name, (kind, cst) in ARMS.items():
    rows = {}
    if ('wf', name) in _cache:
        WF[name] = _cache[('wf', name)]
        print('walkforward cached', name, file=sys.stderr)
        continue
    for T in (2014, 2017, 2020):
        tr = YEAR <= T
        te = (YEAR > T) & (YEAR <= T + 3)
        if te.sum() < 50:
            continue
        fam = fit_family(kind, X[tr], y[tr], cst=cst)
        rows[str(T)] = {'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                        'pinball': {str(q): pinball(y[te], fam[q].predict(X[te]), q) for q in Q}}
        rows[str(T)]['pinball_mean'] = float(np.mean(list(rows[str(T)]['pinball'].values())))
    WF[name] = rows
    _cache[('wf', name)] = rows
    pickle.dump(_cache, open(CACHE, 'wb'))
    print('walkforward', name, file=sys.stderr)
R['walk_forward'] = WF

# ---------------- 3. THE LAW-3 CENSUS ----------------
# For a sample of real rows, sweep the LEVEL feature upward over the observed level range and count
# how often the band's weighted mean FALLS while the level RISES. That is the defect the ratchet patches.
WQ6 = np.array([0.18] * 5); WQ6 = WQ6 / WQ6.sum()
GRID = np.arange(42.0, 118.01, 0.25)

def law3(models_predict, sample_idx):
    viol_rows = 0; steps = 0; neg_steps = 0; worst = 0.0; worst_pct = 0.0
    for i in sample_idx:
        F = np.repeat(X[i][None, :], GRID.size, axis=0)
        F[:, LVL] = GRID
        B = models_predict(F)
        w = B @ WQ6
        d = np.diff(w)
        steps += d.size
        nn = int((d < -1e-9).sum())
        neg_steps += nn
        if nn:
            viol_rows += 1
            worst = min(worst, float(d.min()))
            base = w[:-1]
            pct = float((d / np.maximum(base, 1e-9)).min())
            worst_pct = min(worst_pct, pct)
    return {'rows_sampled': len(sample_idx), 'rows_with_a_down_step': viol_rows,
            'pct_rows_violating': round(100.0 * viol_rows / max(len(sample_idx), 1), 2),
            'total_steps': steps, 'negative_steps': neg_steps,
            'pct_steps_negative': round(100.0 * neg_steps / max(steps, 1), 3),
            'worst_single_step_value': round(worst, 4),
            'worst_single_step_pct': round(100.0 * worst_pct, 3)}

SAMPLE = RNG.choice(X.shape[0], size=200, replace=False)
# thin-evidence subset: the population the register named (low recency-weighted exposure)
THIN = np.where(X[:, 7] < 12.0)[0]
THIN_SAMPLE = RNG.choice(THIN, size=min(200, THIN.size), replace=False)
R['law3_thin_population'] = {'rows_with_exposure_lt_12': int(THIN.size),
                             'pct_of_design': round(100.0 * THIN.size / X.shape[0], 2)}

# 3a. the PINNED shipped artifacts, read as they are
sys.path.insert(0, '/home/claude/rl_workspace/rl_after')
CM = pickle.load(open('/home/user/afl-rl-engine/data/cm_400.pkl', 'rb'))
Q97 = pickle.load(open('/home/user/afl-rl-engine/data/q97m.pkl', 'rb'))
def pinned_band(F):
    return np.sort(np.column_stack([CM[q].predict(F) for q in Q]), axis=1)
R['law3'] = {'PINNED_cm_400_shipped': {'all_rows': law3(pinned_band, SAMPLE),
                                       'thin_evidence_rows': law3(pinned_band, THIN_SAMPLE)}}
for name in ARMS:
    fam = FITTED[name]
    f = (lambda fam: (lambda F: band(fam, F)))(fam)
    R['law3'][name] = {'all_rows': law3(f, SAMPLE), 'thin_evidence_rows': law3(f, THIN_SAMPLE)}
    print('law3', name, file=sys.stderr)

# ---------------- 4. WHAT THE DATA SAYS ABOUT AGE ----------------
# (a) marginal: realised forward best-3 by age bucket
buck = {}
for lo in range(18, 34, 2):
    m = (X[:, AGE] >= lo) & (X[:, AGE] < lo + 2)
    if m.sum() >= 30:
        buck[f'{lo}-{lo+1}'] = {'n': int(m.sum()), 'mean_target': round(float(y[m].mean()), 2),
                                'median_target': round(float(np.median(y[m])), 2),
                                'mean_level': round(float(X[m, LVL].mean()), 2)}
R['age_marginal_by_bucket'] = buck

# (b) conditional partial dependence: hold everything else at the row's own values, sweep AGE
AGRID = np.arange(18.0, 34.01, 0.5)
def age_pd(models_predict, idx):
    curves = []
    for i in idx:
        F = np.repeat(X[i][None, :], AGRID.size, axis=0)
        F[:, AGE] = AGRID
        curves.append(models_predict(F) @ WQ6)
    Cv = np.array(curves)
    mean = Cv.mean(axis=0)
    d = np.diff(Cv, axis=1)
    return {'age_grid': [float(a) for a in AGRID],
            'mean_band_weighted_mean': [round(float(v), 3) for v in mean],
            'mean_curve_argmax_age': float(AGRID[int(np.argmax(mean))]),
            'mean_curve_total_rise': round(float(mean.max() - mean[0]), 3),
            'mean_curve_total_fall_from_peak': round(float(mean.max() - mean[-1]), 3),
            'pct_row_steps_negative': round(100.0 * float((d < 0).mean()), 2),
            'pct_rows_monotone_nonincreasing': round(100.0 * float((d <= 1e-9).all(axis=1).mean()), 2),
            'pct_rows_monotone_nondecreasing': round(100.0 * float((d >= -1e-9).all(axis=1).mean()), 2)}

R['age_partial_dependence'] = {
    'PINNED_cm_400_shipped': age_pd(pinned_band, SAMPLE),
    'B_histgbr_unconstrained': age_pd(lambda F: band(FITTED['B_histgbr_unconstrained'], F), SAMPLE),
}
# (c) the same, split by tenure — is the sign of age different for young vs old careers?
for tag, m in (('tenure_le_3', X[:, 8] <= 3), ('tenure_ge_8', X[:, 8] >= 8)):
    idx = np.where(m)[0]
    if idx.size > 40:
        s = RNG.choice(idx, size=min(150, idx.size), replace=False)
        R['age_partial_dependence'][f'PINNED_cm_400__{tag}'] = age_pd(pinned_band, s)

# ---------------- 5. POOL ARM ----------------
R['pool_arm'] = {
    'pool_rows': int(ISPOOL.sum()), 'national_rows': int((~ISPOOL).sum()),
    'pool_pct_of_design': round(100.0 * float(ISPOOL.mean()), 2),
    'pool_target_mean': round(float(y[ISPOOL].mean()), 2),
    'national_target_mean': round(float(y[~ISPOOL].mean()), 2),
    'pool_target_zero_pct': round(100.0 * float((y[ISPOOL] == 0).mean()), 2),
    'national_target_zero_pct': round(100.0 * float((y[~ISPOOL] == 0).mean()), 2),
}
# what happens to national-arm accuracy if the pool rows are DELETED from training?
famA_all = FITTED['A_gbr_classic_unconstrained']
famA_natonly = fit_family('gbr', X[~ISPOOL], y[~ISPOOL])
R['pool_arm']['deletion_experiment'] = {
    '_doc': 'Refit arm A on NATIONAL rows only; score on the national rows. If deleting the pool '
            'sets costs national accuracy, the pool rows are carrying signal, not noise.',
    'national_pinball_trained_on_all': {str(q): pinball(y[~ISPOOL], famA_all[q].predict(X[~ISPOOL]), q) for q in Q},
    'national_pinball_trained_on_national_only': {str(q): pinball(y[~ISPOOL], famA_natonly[q].predict(X[~ISPOOL]), q) for q in Q},
}

# ---------------- 6. RECENCY / ERA WEIGHTING ----------------
# Does weighting toward recent as-of years beat deleting old ones?
HALF = {}
for tag, w in (('uniform', np.ones(len(y))),
               ('halflife_6y', 0.5 ** ((YEAR.max() - YEAR) / 6.0)),
               ('halflife_10y', 0.5 ** ((YEAR.max() - YEAR) / 10.0))):
    tr = YEAR <= 2020
    te = (YEAR > 2020)
    fam = fit_family('hist', X[tr], y[tr], cst=CST_LVL, weight=w[tr])
    HALF[tag] = {'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                 'pinball': {str(q): pinball(y[te], fam[q].predict(X[te]), q) for q in Q}}
    HALF[tag]['pinball_mean'] = float(np.mean(list(HALF[tag]['pinball'].values())))
# the deletion counterfactual: train only on the recent half
tr_recent = (YEAR <= 2020) & (YEAR >= 2014)
fam = fit_family('hist', X[tr_recent], y[tr_recent], cst=CST_LVL)
te = YEAR > 2020
HALF['DELETE_pre2014_half_the_data'] = {
    'n_train': int(tr_recent.sum()), 'n_test': int(te.sum()),
    'pinball': {str(q): pinball(y[te], fam[q].predict(X[te]), q) for q in Q}}
HALF['DELETE_pre2014_half_the_data']['pinball_mean'] = float(
    np.mean(list(HALF['DELETE_pre2014_half_the_data']['pinball'].values())))
R['weighting_vs_deletion'] = HALF

json.dump(R, open(os.path.join(SC, 'm5_out.json'), 'w'), indent=1, sort_keys=True, default=str)
print('WROTE m5_out.json', file=sys.stderr)
