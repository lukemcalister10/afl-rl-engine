"""CANDIDATE DESIGNS — specified, fitted and MEASURED on held-out careers.

Six designs (a)-(f) (plus one law-safe variant of c), each fitted on the SAME population
(04_dataset_audit.py's design.npz) and scored on the SAME held-out folds.

SPLIT.  Rolling-origin by DEBUT YEAR, whole careers held out.  A player contributes many rows (one
per as-of season), so a row-random split would leak his own future into his own training rows; a
career-level split cannot.  Debut year is also the time axis the production board extrapolates
along, so this split asks the question the board actually asks.

    fold 1   train debut <= 2012    test debut 2013-2015
    fold 2   train debut <= 2015    test debut 2016-2018
    fold 3   train debut <= 2018    test debut 2019-2021

METRICS.  Pinball loss (the proper scoring rule for a quantile — lower is better) and coverage
(what fraction of held-out careers land below the quantile; nominal = alpha), overall and per
population.  Then, on a FULL-DATA fit: monotonicity violations and smoothness along the level axis,
and the four staircase victims' bands as spot exhibits.

Single-threaded.  READ-ONLY on the repo; writes only into the scratch dir.
"""
import json, os, sys, time, collections, pickle
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor

S = os.environ['STUDY']
OUT = os.path.join(S, 'out')
RNG = 0
Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
WQ6 = np.array([0.18] * 5 + [0.10])
WQ6 = WQ6 / WQ6.sum()
LVL = 9
NTREES = {0.10: 400, 0.30: 400, 0.50: 400, 0.70: 400, 0.90: 400, 0.97: 200}   # as shipped

d = np.load(os.path.join(OUT, 'design.npz'), allow_pickle=True)
X = d['X'].astype(float)
y = d['y'].astype(float)
cls = d['cls'].astype(str)
ispool = d['ispool'].astype(bool)
debut = d['debut'].astype(int)
ptype = d['ptype'].astype(str)
player = d['player'].astype(str)
key = d['key'].astype(str)
N, NF = X.shape
print('design matrix %r; debut %d..%d' % (X.shape, debut.min(), debut.max()), flush=True)

# ------------------------------------------------------------------ extended features (design c)
ETYPES = ['ND', 'RD', 'PSD', 'MSD', 'OTHER']
LASTND = {int(k): v for k, v in
          json.load(open('/home/user/afl-rl-engine/engine/rl_after/national_draft_last_pick.json'))
          ['last_national_pick'].items()}
STORE = {p['key']: p for p in
         json.load(open('/home/user/afl-rl-engine/engine/rl_after/rl_model_data.json'))}


def etype(t):
    return t if t in ('ND', 'RD', 'PSD', 'MSD') else 'OTHER'


def unified_ordinal(k):
    """ONE talent ordinal across every entry mechanism — the owner's continuum. A national pick is
    itself; a rookie/pre-season selection chains onto that year's national END (the store's own
    _NDC convention); a pickless mechanism has NO ordinal and is left MISSING (NaN), which
    HistGradientBoostingRegressor handles natively — the tree then learns that row from its
    entry-type flag rather than from a number somebody invented for it."""
    p = STORE.get(k)
    if p is None:
        return np.nan
    t, pk, sp, yr = p.get('type'), p.get('pick'), p.get('stream_pick'), p.get('year')
    if t == 'ND' and pk:
        return float(pk)
    if t in ('RD', 'PSD') and sp:
        return float(LASTND.get(int(yr), 64) + int(sp))
    return np.nan


EXTRA = np.column_stack(
    [np.array([[1.0 if etype(t) == e else 0.0 for e in ETYPES] for t in ptype]),
     ispool.astype(float).reshape(-1, 1),
     np.array([unified_ordinal(k) for k in key]).reshape(-1, 1)])
XC = np.hstack([X, EXTRA])
print('extended matrix %r  (%d entry flags + is_pool + unified ordinal; %d rows carry no ordinal)'
      % (XC.shape, len(ETYPES), int(np.isnan(EXTRA[:, -1]).sum())), flush=True)

MATRIX = {'base': X, 'ext': XC, 'ext_noord': XC[:, :-1]}


# ------------------------------------------------------------------ estimators
def mono_cst(nf):
    c = [0] * nf
    c[LVL] = 1
    return c


def fit_gbr(Xtr, ytr, q, w, mono):
    m = GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=NTREES[q], max_depth=4,
                                  learning_rate=0.05, min_samples_leaf=25, random_state=RNG)
    m.fit(Xtr, ytr, sample_weight=w)
    return m


def fit_hgb(Xtr, ytr, q, w, mono):
    m = HistGradientBoostingRegressor(
        loss='quantile', quantile=q, max_iter=NTREES[q], max_depth=4, learning_rate=0.05,
        min_samples_leaf=25, random_state=RNG, early_stopping=False,
        monotonic_cst=mono_cst(Xtr.shape[1]) if mono else None)
    m.fit(Xtr, ytr, sample_weight=w)
    return m


# ------------------------------------------------------------------ the designs
DESIGNS = {
    'a_status_quo': dict(
        label='(a) STATUS QUO refit - classic GBR, no constraint, current store',
        matrix='base', est='gbr', mono=False, weight=None, tfilter=None, heads=None),
    'b_mono': dict(
        label='(b) modern estimator + monotone-in-level only',
        matrix='base', est='hgb', mono=True, weight=None, tfilter=None, heads=None),
    'c_unified': dict(
        label='(c) b + entry type, pool flag and a unified draft ordinal AS FEATURES',
        matrix='ext', est='hgb', mono=True, weight=None, tfilter=None, heads=None),
    'c1_entryonly': dict(
        label='(c1) b + entry type and pool flag only (no ordinal past 64 - law-4 safe)',
        matrix='ext_noord', est='hgb', mono=True, weight=None, tfilter=None, heads=None),
    'd_weighted': dict(
        label='(d) b + population-relevance sample weighting (class-balanced, gamma=0.5)',
        matrix='base', est='hgb', mono=True, weight='class', tfilter=None, heads=None),
    'e_heads': dict(
        label='(e) separate heads - one model for national (ND 1-64), one for pool',
        matrix='base', est='hgb', mono=True, weight=None, tfilter=None, heads='pool'),
    'f_delete': dict(
        label='(f) DELETION - pool careers dropped from training (the scope\'s old option)',
        matrix='base', est='hgb', mono=True, weight=None, tfilter='national_only', heads=None),
}
ORDER = ['a_status_quo', 'b_mono', 'c_unified', 'c1_entryonly', 'd_weighted', 'e_heads', 'f_delete']


def w_class_balanced(sel, gamma=0.5):
    """(d) POPULATION-RELEVANCE WEIGHTING - and it is ARBITRARY, stated plainly.
    w_i = (n / n_class(i))^gamma with gamma=0.5. gamma=0 is unweighted; gamma=1 makes every
    population count equally regardless of how much of it there is. gamma=0.5 is a HALFWAY POINT
    NOBODY DERIVED - it is a dial, and this study reports what it buys and what it costs rather
    than pretending it fell out of anything."""
    c = collections.Counter(cls[sel])
    n = int(sel.sum())
    return np.array([(n / c[x]) ** gamma for x in cls[sel]])


class Fitted:
    """A fitted design. predict(Mrows, pool_flags) -> (n,6) in the design's OWN feature space."""

    def __init__(self, name, tr_sel):
        D = DESIGNS[name]
        self.name = name
        self.D = D
        self.M = MATRIX[D['matrix']]
        est = fit_gbr if D['est'] == 'gbr' else fit_hgb
        if D['heads'] == 'pool':
            self.heads = {}
            for arm in (False, True):
                sel = tr_sel & (ispool == arm)
                self.heads[arm] = {q: est(self.M[sel], y[sel], q, None, D['mono']) for q in Q6}
                self.__dict__['n_%s' % arm] = int(sel.sum())
            self.models = None
        else:
            sel = tr_sel.copy()
            if D['tfilter'] == 'national_only':
                sel = sel & (~ispool)
            w = w_class_balanced(sel) if D['weight'] == 'class' else None
            self.models = {q: est(self.M[sel], y[sel], q, w, D['mono']) for q in Q6}
            self.heads = None
            self.n_train = int(sel.sum())

    def predict(self, Mrows, pool_flags=None):
        Mrows = np.atleast_2d(Mrows)
        if self.heads is None:
            return np.column_stack([self.models[q].predict(Mrows) for q in Q6])
        out = np.zeros((len(Mrows), 6))
        pf = np.asarray(pool_flags, dtype=bool)
        for arm in (False, True):
            m = pf == arm
            if m.any():
                out[m] = np.column_stack([self.heads[arm][q].predict(Mrows[m]) for q in Q6])
        return out

    def predict_idx(self, idx):
        return self.predict(self.M[idx], ispool[idx])


# ------------------------------------------------------------------ metrics
def pinball(yt, qhat, q):
    e = yt - qhat
    return float(np.mean(np.maximum(q * e, (q - 1) * e)))


def guarded(B):
    """The engine's own two crossing repairs, applied identically to every design so the comparison
    is like-for-like - and INSTRUMENTED, which the scope's section 3.3 asks for and nobody has done:
      conditional_prior.py:167   np.sort over the five quantiles
      _merged_recover.py:372     band[5] = max(q97, band[4])"""
    P = np.sort(B[:, :5], axis=1)
    n_sort = int((np.abs(P - B[:, :5]) > 1e-12).any(axis=1).sum())
    top = np.maximum(B[:, 5], P[:, 4])
    n_ceil = int((B[:, 5] < P[:, 4] - 1e-12).sum())
    return np.column_stack([P, top]), n_sort, n_ceil


def evaluate(name, folds):
    rec = dict(design=name, label=DESIGNS[name]['label'], folds=[])
    agg = collections.defaultdict(list)
    for fi, (tr_sel, te_sel) in enumerate(folds, 1):
        t = time.time()
        F = Fitted(name, tr_sel)
        idx = np.where(te_sel)[0]
        B, n_sort, n_ceil = guarded(F.predict_idx(idx))
        yt = y[idx]
        f = dict(fold=fi, n_train=int(tr_sel.sum()), n_test=len(idx),
                 fit_s=round(time.time() - t, 1),
                 sort_repairs=n_sort, sort_repair_pct=round(100.0 * n_sort / len(idx), 2),
                 ceil_repairs=n_ceil, ceil_repair_pct=round(100.0 * n_ceil / len(idx), 2),
                 pinball={}, coverage={})
        for j, q in enumerate(Q6):
            pl = pinball(yt, B[:, j], q)
            cv = float(np.mean(yt <= B[:, j]))
            f['pinball']['%.2f' % q] = round(pl, 5)
            f['coverage']['%.2f' % q] = round(cv, 4)
            agg['pb_%.2f' % q].append(pl)
            agg['cv_%.2f' % q].append(cv)
        f['pinball_mean'] = round(float(np.mean(list(f['pinball'].values()))), 5)
        f['cov_abs_err'] = round(float(np.mean(
            [abs(f['coverage']['%.2f' % q] - q) for q in Q6])), 4)
        agg['pb_mean'].append(f['pinball_mean'])
        agg['cov_abs_err'].append(f['cov_abs_err'])
        f['by_class'] = {}
        for c in sorted(set(cls[idx])):
            m = cls[idx] == c
            if m.sum() < 25:
                continue
            pbs = [pinball(yt[m], B[m, j], q) for j, q in enumerate(Q6)]
            cvs = [float(np.mean(yt[m] <= B[m, j])) for j in range(6)]
            f['by_class'][c] = dict(
                n=int(m.sum()), pinball_mean=round(float(np.mean(pbs)), 5),
                cov_abs_err=round(float(np.mean(np.abs(np.array(cvs) - Q6))), 4),
                coverage={'%.2f' % q: round(cvs[j], 3) for j, q in enumerate(Q6)})
            agg['pbc_' + c].append(float(np.mean(pbs)))
            agg['cvc_' + c].append(float(np.mean(np.abs(np.array(cvs) - Q6))))
        rec['folds'].append(f)
        print('   fold %d  n_tr=%5d n_te=%5d  %5.1fs  pinball %.4f  covErr %.4f  sortfix %.1f%% ceilfix %.1f%%'
              % (fi, tr_sel.sum(), len(idx), f['fit_s'], f['pinball_mean'], f['cov_abs_err'],
                 f['sort_repair_pct'], f['ceil_repair_pct']), flush=True)
    rec['pooled'] = {k: round(float(np.mean(v)), 5) for k, v in agg.items()}
    return rec


# ------------------------------------------------------------------ folds + held-out evaluation
FOLDS = []
for tr_max, lo, hi in ((2012, 2013, 2015), (2015, 2016, 2018), (2018, 2019, 2021)):
    FOLDS.append(((debut <= tr_max), (debut >= lo) & (debut <= hi)))
for i, (a, b) in enumerate(FOLDS, 1):
    print('fold %d: train %5d rows (debut<=%d), test %5d rows'
          % (i, a.sum(), (2012, 2015, 2018)[i - 1], b.sum()))

results = {}
for nm in ORDER:
    print('\n=== %s' % DESIGNS[nm]['label'], flush=True)
    results[nm] = evaluate(nm, FOLDS)
json.dump(results, open(os.path.join(OUT, 'candidates_holdout.json'), 'w'), indent=1, default=str)
print('\nwrote out/candidates_holdout.json', flush=True)

# ------------------------------------------------------------------ FULL-DATA fits + surface tests
ALL = np.ones(N, dtype=bool)
FULL = {}
for nm in ORDER:
    t = time.time()
    FULL[nm] = Fitted(nm, ALL)
    print('full fit %-16s %5.1fs' % (nm, time.time() - t), flush=True)

rs = np.random.RandomState(0)
samp = []
for c in sorted(set(cls)):
    ix = np.where((cls == c) & (debut >= 2014))[0]
    if len(ix) < 10:
        ix = np.where(cls == c)[0]
    samp.extend(rs.choice(ix, size=min(50, len(ix)), replace=False).tolist())
samp = np.array(sorted(set(samp)))
GRID = np.linspace(40.0, 120.0, 401)
print('\nsurface sweep: %d rows x %d level points (40..120)' % (len(samp), len(GRID)), flush=True)

surface = {}
for nm in ORDER:
    F = FULL[nm]
    M = F.M
    neg_steps = tot_steps = rows_neg = 0
    negvar_pct = []
    plateau_counts = []
    worst_drop_pct = 0.0
    worst_row = None
    for i in samp:
        base = np.repeat(M[i][None, :], len(GRID), axis=0)
        base[:, LVL] = GRID
        B, _, _ = guarded(F.predict(base, np.repeat(ispool[i], len(GRID))))
        v = B @ WQ6                                  # the band's weighted mean = what price6 reads
        dv = np.diff(v)
        neg = dv < -1e-9
        neg_steps += int(neg.sum())
        tot_steps += int((np.abs(dv) > 1e-9).sum())
        if neg.any():
            rows_neg += 1
        rng = max(v.max() - v.min(), 1e-9)
        negvar_pct.append(100.0 * float(-dv[neg].sum()) / rng if neg.any() else 0.0)
        plateau_counts.append(int((np.abs(dv) > 1e-9).sum()) + 1)
        # worst peak-to-trough fall anywhere on the sweep, as % of the running max
        runmax = np.maximum.accumulate(v)
        drop = float(np.max((runmax - v) / np.maximum(runmax, 1e-9))) * 100.0
        if drop > worst_drop_pct:
            worst_drop_pct = drop
            worst_row = player[i]
    surface[nm] = dict(
        label=DESIGNS[nm]['label'],
        rows_swept=len(samp),
        rows_with_a_descending_step=rows_neg,
        rows_with_a_descending_step_pct=round(100.0 * rows_neg / len(samp), 2),
        descending_steps=neg_steps, total_steps=tot_steps,
        descending_step_pct=round(100.0 * neg_steps / max(tot_steps, 1), 3),
        mean_negative_variation_pct_of_range=round(float(np.mean(negvar_pct)), 4),
        max_negative_variation_pct_of_range=round(float(np.max(negvar_pct)), 4),
        mean_distinct_steps_per_row=round(float(np.mean(plateau_counts)), 1),
        worst_peak_to_trough_drop_pct=round(worst_drop_pct, 2),
        worst_row=worst_row)
    print('%-16s desc-steps %6d/%6d (%5.2f%%)  rows-with-a-drop %3d/%3d  worst fall %6.2f%%  steps/row %6.1f'
          % (nm, neg_steps, tot_steps, surface[nm]['descending_step_pct'], rows_neg, len(samp),
             worst_drop_pct, surface[nm]['mean_distinct_steps_per_row']), flush=True)

json.dump(surface, open(os.path.join(OUT, 'candidates_surface.json'), 'w'), indent=1, default=str)
print('wrote out/candidates_surface.json', flush=True)

# ------------------------------------------------------------------ spot exhibits: the four victims
VICTIMS = ['Max Kondogiannis', 'Josh Dolan', 'Charlie West', 'Will Hayes']
exhibit = {}
for nm_p in VICTIMS:
    ix = np.where(player == nm_p)[0]
    if len(ix) == 0:
        exhibit[nm_p] = 'NOT A TRAINING ROW (debut after the 2021 resolved cut) - swept as a '
        continue
for nm_p in VICTIMS:
    exhibit.setdefault(nm_p, {})
json.dump({'note': 'see 06_victims.py - the victims post-date the resolved cut so their feature '
                   'rows are built from the live store, not from the training matrix'},
          open(os.path.join(OUT, 'victims_placeholder.json'), 'w'), indent=1)

with open(os.path.join(OUT, 'full_fits.pkl'), 'wb') as fh:
    pickle.dump({nm: FULL[nm] for nm in ORDER}, fh)
print('wrote out/full_fits.pkl')
