"""SPOT EXHIBITS — the four staircase victims, under every candidate design and under the SHIPPED
frozen forest, plus the decisive test of whether the estate's own ORDER-44 ratchet closes the
residual gap that sklearn's quantile constraint leaves open.

The four are the diagnosis's own named rows (WORKINGS_TROUGH.md 4.1 and the isotonic table):
Max Kondogiannis, Josh Dolan, Charlie West, Will Hayes. They debuted after the 2021 resolved cut,
so they are NOT training rows — they are exactly the population the band extrapolates onto.

CAVEAT, stated in the output: the SHIPPED cm_400 was trained with cp._lvl_eff rebound to the
par-centred PR.lvl_par (wire_redesign.build / par_redesign.retrain), while every candidate here is
trained on cp._feat's own _lvl_eff. So the shipped forest's LEVEL COORDINATE is not the same
coordinate as the candidates'. The level SWEEP is still a fair comparison of surface ROUGHNESS —
it is the same comparison the diagnosis made — but the absolute band values are not comparable
across that boundary, and are not compared here.

READ-ONLY.
"""
import io, contextlib, json, os, sys, pickle, time
import numpy as np

S = os.environ['STUDY']
OUT = os.path.join(S, 'out')
Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
Q5 = Q6[:5]
WQ6 = np.array([0.18] * 5 + [0.10])
WQ6 = WQ6 / WQ6.sum()
LVL = 9
ORDER = ['a_status_quo', 'b_mono', 'c_unified', 'c1_entryonly', 'd_weighted', 'e_heads', 'f_delete']


class Fitted:                      # unpickling stub
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

# ---- engine, for the victims' real feature vectors -------------------------------------------
sys.path.insert(0, '.')
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
import importlib.util


def _L(n, p):
    sp = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(sp)
    with contextlib.redirect_stdout(io.StringIO()):
        sp.loader.exec_module(m)
    return m


FV = os.path.join(os.environ['RL_REPO'], 'engine', 'forward_valuation')
cp = _L('cp', os.path.join(FV, 'conditional_prior.py'))

SHIPPED_CM = pickle.load(open(os.path.join(os.environ['RL_REPO'], 'data', 'cm_400.pkl'), 'rb'))
SHIPPED_Q97 = pickle.load(open(os.path.join(os.environ['RL_REPO'], 'data', 'q97m.pkl'), 'rb'))

ETYPES = ['ND', 'RD', 'PSD', 'MSD', 'OTHER']
LASTND = {int(k): v for k, v in
          json.load(open(os.path.join(os.environ['RL_REPO'], 'engine', 'rl_after',
                                      'national_draft_last_pick.json')))['last_national_pick'].items()}


def ext_row(p, f11):
    t = p.get('type')
    e = t if t in ('ND', 'RD', 'PSD', 'MSD') else 'OTHER'
    oh = [1.0 if e == x else 0.0 for x in ETYPES]
    pool = 1.0 if MA.is_pool(p) else 0.0
    pk, sp, yr = p.get('pick'), p.get('stream_pick'), p.get('year')
    if t == 'ND' and pk:
        ordn = float(pk)
    elif t in ('RD', 'PSD') and sp:
        ordn = float(LASTND.get(int(yr), 64) + int(sp))
    else:
        ordn = np.nan
    return np.array(list(f11) + oh + [pool, ordn], dtype=float)


def guarded(B):
    P = np.sort(B[:, :5], axis=1)
    return np.column_stack([P, np.maximum(B[:, 5], P[:, 4])])


def shipped_band(F):
    P = np.column_stack([SHIPPED_CM[q].predict(F) for q in Q5])
    return guarded(np.column_stack([P, SHIPPED_Q97.predict(F)]))


# ---- the ORDER-44 ratchet, reproduced here on an ARBITRARY surface ----------------------------
def ratchet(predict_fn, f, lo=40.0, hi=120.0, knots=None):
    """The estate's own construction (_merged_recover._o44_band): the componentwise running maximum
    over every PIECE of the step surface at or below this row's level. Nested in lvl, therefore
    EXACTLY non-decreasing by construction, with no free parameter. Applied here to a CANDIDATE
    surface to answer the one question the constrained fit cannot answer for itself."""
    xs = knots
    lvl = float(f[LVL])
    sel = xs[xs <= lvl]
    if sel.size == 0:
        sel = np.array([lvl])
    F = np.repeat(f[None, :], sel.size, axis=0)
    F[:, LVL] = sel
    return np.maximum.accumulate(guarded(predict_fn(F)), axis=0)[-1]


VICTIMS = ['Max Kondogiannis', 'Josh Dolan', 'Charlie West', 'Will Hayes']
GRID = np.linspace(40.0, 120.0, 801)
res = {'_caveat': __doc__.split('CAVEAT, stated in the output:')[1].split('READ-ONLY')[0].strip()}

for nm in VICTIMS:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        res[nm] = 'NOT IN STORE'
        continue
    f11 = np.array(cp._feat(p, 2026), dtype=float)
    fext = ext_row(p, f11)
    pool = bool(MA.is_pool(p))
    r = dict(player=nm, type=p.get('type'), pick=p.get('pick'), pos=MA.gfut(p),
             is_pool=pool, level_feature=round(float(f11[LVL]), 4),
             exposure=round(float(f11[7]), 3), tenure=float(f11[8]),
             age=round(float(f11[10]), 2), designs={})

    def sweep_stats(pf, M0, label):
        F = np.repeat(M0[None, :], len(GRID), axis=0)
        F[:, LVL] = GRID
        B = guarded(pf(F))
        v = B @ WQ6
        dv = np.diff(v)
        neg = dv < -1e-9
        runmax = np.maximum.accumulate(v)
        drop = float(np.max((runmax - v) / np.maximum(runmax, 1e-9))) * 100.0
        at = np.interp(M0[LVL], GRID, v)
        return dict(band_at_own_level=[round(float(x), 2) for x in
                                       B[np.argmin(np.abs(GRID - M0[LVL]))]],
                    weighted_mean_at_own_level=round(float(at), 3),
                    descending_steps=int(neg.sum()), total_steps=int((np.abs(dv) > 1e-9).sum()),
                    worst_peak_to_trough_drop_pct=round(drop, 3),
                    worst_single_step=round(float(dv.min()), 4))

    r['designs']['SHIPPED_cm400'] = sweep_stats(shipped_band, f11, 'shipped')
    for dn in ORDER:
        F = FULL[dn]
        M0 = fext if F.M.shape[1] == 18 else (fext[:17] if F.M.shape[1] == 17 else f11)

        def pf(Frows, _F=F, _pool=pool):
            return _F.predict(Frows, np.repeat(_pool, len(Frows)))
        r['designs'][dn] = sweep_stats(pf, M0, dn)

    # ---- the ratchet on top of design (b) and design (c1) ----
    for dn in ('b_mono', 'c1_entryonly', 'a_status_quo'):
        F = FULL[dn]
        M0 = fext[:17] if F.M.shape[1] == 17 else (fext if F.M.shape[1] == 18 else f11)

        def pf(Frows, _F=F, _pool=pool):
            return _F.predict(Frows, np.repeat(_pool, len(Frows)))
        # knots: for a HistGBR the pieces are the bin edges of the level feature across all six
        # models; for the classic GBR they are the tree split thresholds, as ORDER 44 reads them.
        kn = set()
        models = F.models if F.models is not None else F.heads[pool]
        for q in Q6:
            m = models[q]
            if hasattr(m, '_bin_mapper'):
                kn.update(float(x) + 1e-9 for x in np.asarray(m._bin_mapper.bin_thresholds_[LVL]))
            else:
                for e in np.asarray(m.estimators_).ravel():
                    t = e.tree_
                    kn.update(float(v) + 1e-9 for v in t.threshold[t.feature == LVL])
        kn = np.array(sorted(x for x in kn if 40.0 <= x <= 120.0))
        kn = np.concatenate([[40.0], kn, [120.0]])
        vals = []
        for L in GRID:
            g = M0.copy()
            g[LVL] = L
            vals.append(ratchet(pf, g, knots=kn) @ WQ6)
        vals = np.array(vals)
        dv = np.diff(vals)
        r['designs']['%s+RATCHET' % dn] = dict(
            descending_steps=int((dv < -1e-9).sum()),
            worst_single_step=round(float(dv.min()), 6),
            weighted_mean_at_own_level=round(float(np.interp(M0[LVL], GRID, vals)), 3),
            n_knots=len(kn))
    res[nm] = r
    print('%-18s lvl=%7.3f pool=%s' % (nm, f11[LVL], pool), flush=True)
    for k, v in r['designs'].items():
        if 'total_steps' in v:
            print('    %-22s desc %4d/%4d  worst fall %6.3f%%  band-mean %8.3f'
                  % (k, v['descending_steps'], v['total_steps'],
                     v['worst_peak_to_trough_drop_pct'], v['weighted_mean_at_own_level']))
        else:
            print('    %-22s desc %4d  worst step %.2e  band-mean %8.3f  (knots %d)'
                  % (k, v['descending_steps'], v['worst_single_step'],
                     v['weighted_mean_at_own_level'], v['n_knots']))
    print(flush=True)

json.dump(res, open(os.path.join(OUT, 'victims.json'), 'w'), indent=1, default=str)
print('wrote out/victims.json')
