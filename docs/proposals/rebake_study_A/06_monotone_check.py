"""Is the residual descending-step count on the constrained designs REAL, or float noise?

Measures, per leg and on the WQ6 band mean, the SIZE of every negative step on the level sweep.
A constraint that works leaves violations at the 1e-13 relative scale (summation order); a
constraint that does not leaves violations you can see in a price.
"""
import os, pickle, json
import numpy as np

S = os.environ['STUDY']
Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
WQ6 = np.array([0.18] * 5 + [0.10])
WQ6 = WQ6 / WQ6.sum()
LVL = 9


class Fitted:                      # unpickling stub, same identity as 05_candidates.Fitted
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


import __main__
__main__.Fitted = Fitted

F = pickle.load(open(os.path.join(S, 'out', 'full_fits.pkl'), 'rb'))
d = np.load(os.path.join(S, 'out', 'design.npz'), allow_pickle=True)
ispool = d['ispool'].astype(bool)
GRID = np.linspace(40.0, 120.0, 401)
res = {}
for nm, f in F.items():
    M = f.M
    leg_abs, leg_rel, band_rel, band_abs = [], [], [], []
    for i in range(0, M.shape[0], 45):
        base = np.repeat(M[i][None, :], len(GRID), axis=0)
        base[:, LVL] = GRID
        raw = f.predict(base, np.repeat(ispool[i], len(GRID)))
        for j in range(6):
            col = raw[:, j]
            dj = np.diff(col)
            neg = dj[dj < 0]
            if len(neg):
                rng = max(col.max() - col.min(), 1e-9)
                leg_abs.extend(np.abs(neg).tolist())
                leg_rel.extend((np.abs(neg) / rng).tolist())
        P = np.sort(raw[:, :5], axis=1)
        B = np.column_stack([P, np.maximum(raw[:, 5], P[:, 4])])
        v = B @ WQ6
        dv = np.diff(v)
        neg = dv[dv < 0]
        if len(neg):
            band_abs.extend(np.abs(neg).tolist())
            band_rel.extend((np.abs(neg) / max(v.max() - v.min(), 1e-9)).tolist())

    def st(a):
        a = np.array(a) if len(a) else np.array([0.0])
        return dict(n=int(len(a)) if len(a) else 0, max=float(a.max()),
                    median=float(np.median(a)), p99=float(np.percentile(a, 99)))
    res[nm] = dict(per_leg_abs=st(leg_abs), per_leg_rel=st(leg_rel),
                   band_abs=st(band_abs), band_rel=st(band_rel))
    print('%-16s per-leg neg: n=%7d max_abs=%.3e max_rel=%.3e | band neg: n=%7d max_abs=%.3e max_rel=%.3e'
          % (nm, res[nm]['per_leg_abs']['n'], res[nm]['per_leg_abs']['max'],
             res[nm]['per_leg_rel']['max'], res[nm]['band_abs']['n'],
             res[nm]['band_abs']['max'], res[nm]['band_rel']['max']))

json.dump(res, open(os.path.join(S, 'out', 'monotone_check.json'), 'w'), indent=1)
print('\nwrote out/monotone_check.json')
