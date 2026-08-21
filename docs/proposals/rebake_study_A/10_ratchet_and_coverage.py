"""TWO MEASUREMENTS THE OWNER'S DECISIONS NEED.

(1) COVERAGE DIRECTION. Are the band's quantiles too high or too low, and by how much? This is the
    calibration question D6 never names, and it turns out to be a bigger miss than anything the
    monotonicity act touches.

(2) WHAT THE RATCHET COSTS AND WHAT IT MINTS. The ORDER-44 running-max projection is the only
    construction measured here that reaches EXACTLY zero descending steps. It is one-sided: it can
    only raise. Scope D7 asks whether the pool total moves and by how much. This measures it on
    held-out careers — the pinball cost of the projection and the mean lift it mints — for a
    CONSTRAINED surface (where the residual violations are small) and for the UNCONSTRAINED one
    (where they are not).
"""
import json, os, pickle, time
import numpy as np

S = os.environ['STUDY']
OUT = os.path.join(S, 'out')
Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
WQ6 = np.array([0.18] * 5 + [0.10])
WQ6 = WQ6 / WQ6.sum()
LVL = 9


class Fitted:
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
FULL = pickle.load(open(os.path.join(OUT, 'full_fits.pkl'), 'rb'))
H = json.load(open(os.path.join(OUT, 'candidates_holdout.json')))
d = np.load(os.path.join(OUT, 'design.npz'), allow_pickle=True)
X = d['X'].astype(float)
y = d['y'].astype(float)
cls = d['cls'].astype(str)
ispool = d['ispool'].astype(bool)
debut = d['debut'].astype(int)

ORDER = ['a_status_quo', 'b_mono', 'c_unified', 'c1_entryonly', 'd_weighted', 'e_heads', 'f_delete']

# ---------------------------------------------------------------- (1) coverage direction
print('=' * 108)
print('COVERAGE — observed fraction of held-out careers landing BELOW each quantile (nominal in brackets)')
print('=' * 108)
print('%-14s' % 'design' + ''.join(' %11s' % ('q%.2f[%.2f]' % (q, q)) for q in Q6))
print('-' * 108)
cov = {}
for nm in ORDER:
    v = [float(np.mean([f['coverage']['%.2f' % q] for f in H[nm]['folds']])) for q in Q6]
    cov[nm] = [round(x, 4) for x in v]
    print('%-14s' % nm + ''.join(' %11.3f' % x for x in v))
print()
print('SIGNED ERROR (observed - nominal); positive = the quantile sits TOO HIGH, negative = TOO LOW')
print('%-14s' % 'design' + ''.join(' %11s' % ('q%.2f' % q) for q in Q6))
print('-' * 108)
for nm in ORDER:
    print('%-14s' % nm + ''.join(' %+11.3f' % (cov[nm][j] - q) for j, q in enumerate(Q6)))

# ---------------------------------------------------------------- (2) ratchet cost + mint
def guarded(B):
    P = np.sort(B[:, :5], axis=1)
    return np.column_stack([P, np.maximum(B[:, 5], P[:, 4])])


def knots_of(F, pool):
    models = F.models if F.models is not None else F.heads[pool]
    kn = set()
    for q in Q6:
        m = models[q]
        if hasattr(m, '_bin_mapper'):
            kn.update(float(x) + 1e-9 for x in np.asarray(m._bin_mapper.bin_thresholds_[LVL]))
        else:
            for e in np.asarray(m.estimators_).ravel():
                t = e.tree_
                kn.update(float(v) + 1e-9 for v in t.threshold[t.feature == LVL])
    kn = np.array(sorted(x for x in kn if 40.0 <= x <= 120.0))
    return np.concatenate([[40.0], kn, [120.0]]) if len(kn) else np.array([40.0, 120.0])


def pinball(yt, qh, q):
    e = yt - qh
    return float(np.mean(np.maximum(q * e, (q - 1) * e)))


te = (debut >= 2019) & (debut <= 2021)          # fold-3 test set — the newest resolved careers
idx = np.where(te)[0]
print()
print('=' * 108)
print('THE RATCHET — cost and mint, on %d held-out rows (debut 2019-2021)' % len(idx))
print('=' * 108)
print('%-16s %10s %10s %10s %10s %10s %10s' %
      ('design', 'pinball', '+ratchet', 'cost %', 'mean band', '+ratchet', 'MINT %'))
print('-' * 108)
rat = {}
for nm in ('a_status_quo', 'b_mono', 'c1_entryonly'):
    F = FULL[nm]
    M = F.M
    t0 = time.time()
    raw = guarded(F.predict(M[idx], ispool[idx]))
    KN = {False: knots_of(F, False), True: knots_of(F, True)}
    out = np.zeros_like(raw)
    for r, i in enumerate(idx):
        f = M[i]
        lvl = float(f[LVL])
        xs = KN[bool(ispool[i])]
        sel = xs[xs <= lvl]
        if sel.size == 0:
            out[r] = raw[r]
            continue
        G = np.repeat(f[None, :], sel.size, axis=0)
        G[:, LVL] = sel
        out[r] = np.maximum.accumulate(
            guarded(F.predict(G, np.repeat(ispool[i], sel.size))), axis=0)[-1]
    pb_raw = float(np.mean([pinball(y[idx], raw[:, j], q) for j, q in enumerate(Q6)]))
    pb_rat = float(np.mean([pinball(y[idx], out[:, j], q) for j, q in enumerate(Q6)]))
    m_raw = float(np.mean(raw @ WQ6))
    m_rat = float(np.mean(out @ WQ6))
    moved = int((np.abs(out - raw).max(axis=1) > 1e-9).sum())
    rat[nm] = dict(pinball_raw=round(pb_raw, 5), pinball_ratchet=round(pb_rat, 5),
                   pinball_cost_pct=round(100 * (pb_rat - pb_raw) / pb_raw, 3),
                   mean_band_raw=round(m_raw, 4), mean_band_ratchet=round(m_rat, 4),
                   mint_pct=round(100 * (m_rat - m_raw) / m_raw, 4),
                   rows_moved=moved, rows_moved_pct=round(100.0 * moved / len(idx), 2),
                   n_knots=int(len(KN[False])), seconds=round(time.time() - t0, 1))
    print('%-16s %10.4f %10.4f %+9.2f%% %10.3f %10.3f %+9.3f%%   (%d of %d rows moved, %.0fs)' %
          (nm, pb_raw, pb_rat, rat[nm]['pinball_cost_pct'], m_raw, m_rat, rat[nm]['mint_pct'],
           moved, len(idx), rat[nm]['seconds']))

json.dump({'coverage': cov, 'ratchet': rat},
          open(os.path.join(OUT, 'ratchet_and_coverage.json'), 'w'), indent=1)
print('\nwrote out/ratchet_and_coverage.json')
