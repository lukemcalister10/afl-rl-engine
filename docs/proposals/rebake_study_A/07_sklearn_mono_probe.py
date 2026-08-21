"""IS sklearn's monotonic constraint EXACT?  This decides whether the scope's acceptance bar
D6.1 ("zero descending steps on the level axis") is met BY CONSTRUCTION by design (b), or whether
it still needs a read-site ratchet on top.

Isolated synthetic probe, pinned library (sklearn 1.8.0), single-threaded, no engine, no store.
"""
import numpy as np, json, os
from sklearn.ensemble import HistGradientBoostingRegressor

S = os.environ.get('STUDY', '.')
rs = np.random.RandomState(0)
out = {'sklearn': __import__('sklearn').__version__}

# --- case 1: clean continuous feature, quantile loss, constraint on feature 0 ------------------
n, p = 4000, 4
X = rs.uniform(0, 100, size=(n, p))
y = 0.5 * X[:, 0] + 3 * np.sin(X[:, 1] / 8) + rs.normal(0, 8, n)
cst = [1] + [0] * (p - 1)
G = np.linspace(0, 100, 4001)


def probe(model, Xtrain, label, nprobe=60):
    tot = neg = 0
    worst = 0.0
    for i in range(nprobe):
        b = np.repeat(Xtrain[i][None, :], len(G), axis=0)
        b[:, 0] = G
        v = model.predict(b)
        dv = np.diff(v)
        neg += int((dv < -1e-12).sum())
        tot += len(dv)
        worst = min(worst, float(dv.min()))
    return dict(case=label, neg_steps=neg, steps=tot, worst_step=worst)


rows = []
for loss, kw in (('quantile', dict(loss='quantile', quantile=0.5)),
                 ('quantile', dict(loss='quantile', quantile=0.9)),
                 ('squared_error', dict(loss='squared_error'))):
    m = HistGradientBoostingRegressor(max_iter=400, max_depth=4, learning_rate=0.05,
                                      min_samples_leaf=25, random_state=0,
                                      early_stopping=False, monotonic_cst=cst, **kw)
    m.fit(X, y)
    r = probe(m, X, 'clean/%s/%s' % (loss, kw.get('quantile', '-')))
    rows.append(r)
    print(r)

# --- case 2: the REAL shape — a feature with a large point mass at 0 (draft-year rows) ---------
X2 = X.copy()
mass = rs.rand(n) < 0.25
X2[mass, 0] = 0.0
y2 = np.where(mass, rs.normal(30, 15, n), 0.5 * X2[:, 0] + rs.normal(0, 8, n))
for q in (0.5, 0.9):
    m = HistGradientBoostingRegressor(loss='quantile', quantile=q, max_iter=400, max_depth=4,
                                      learning_rate=0.05, min_samples_leaf=25, random_state=0,
                                      early_stopping=False, monotonic_cst=cst)
    m.fit(X2, y2)
    r = probe(m, X2, 'pointmass-at-0/quantile/%s' % q)
    rows.append(r)
    print(r)

# --- case 3: does changing max_bins / depth / iterations remove it? -----------------------------
for mb in (64, 128, 255):
    m = HistGradientBoostingRegressor(loss='quantile', quantile=0.5, max_iter=400, max_depth=4,
                                      learning_rate=0.05, min_samples_leaf=25, random_state=0,
                                      early_stopping=False, monotonic_cst=cst, max_bins=mb)
    m.fit(X2, y2)
    r = probe(m, X2, 'pointmass/max_bins=%d' % mb)
    rows.append(r)
    print(r)
for it in (50, 100):
    m = HistGradientBoostingRegressor(loss='quantile', quantile=0.5, max_iter=it, max_depth=4,
                                      learning_rate=0.05, min_samples_leaf=25, random_state=0,
                                      early_stopping=False, monotonic_cst=cst)
    m.fit(X2, y2)
    r = probe(m, X2, 'pointmass/max_iter=%d' % it)
    rows.append(r)
    print(r)

# --- case 4: is the violation AT a bin boundary? ------------------------------------------------
m = HistGradientBoostingRegressor(loss='quantile', quantile=0.5, max_iter=400, max_depth=4,
                                  learning_rate=0.05, min_samples_leaf=25, random_state=0,
                                  early_stopping=False, monotonic_cst=cst)
m.fit(X2, y2)
th = np.asarray(m._bin_mapper.bin_thresholds_[0])
b = np.repeat(X2[0][None, :], len(G), axis=0)
b[:, 0] = G
v = m.predict(b)
dv = np.diff(v)
bad = np.where(dv < -1e-12)[0]
det = []
for j in bad[:10]:
    lo, hi = G[j], G[j + 1]
    near = th[(th >= lo - 1e-9) & (th <= hi + 1e-9)]
    det.append(dict(lo=float(lo), hi=float(hi), step=float(dv[j]),
                    bin_threshold_inside=[float(x) for x in near]))
out['bin_boundary_detail'] = det
out['cases'] = rows
print('\nviolations sit at a bin threshold:',
      all(d['bin_threshold_inside'] for d in det) if det else 'no violations')

# --- case 5: EXACTNESS ON THE BINNED GRID — evaluate only at bin midpoints ---------------------
mid = np.concatenate([[th[0] - 1.0], (th[:-1] + th[1:]) / 2.0, [th[-1] + 1.0]])
b = np.repeat(X2[0][None, :], len(mid), axis=0)
b[:, 0] = mid
v = m.predict(b)
out['bin_midpoint_grid'] = dict(n=len(mid), neg_steps=int((np.diff(v) < -1e-12).sum()),
                                worst=float(np.diff(v).min()))
print('on the BIN-MIDPOINT grid:', out['bin_midpoint_grid'])

json.dump(out, open(os.path.join(S, 'out', 'sklearn_mono_probe.json'), 'w'), indent=1)
print('\nwrote out/sklearn_mono_probe.json')
