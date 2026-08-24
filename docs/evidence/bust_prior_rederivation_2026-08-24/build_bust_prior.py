#!/usr/bin/env python3
"""build_bust_prior — the recovered producer, first-class: FAITHFUL and MODERNIZED constructions.

FAITHFUL = the verbatim June construction (owner-recovered bustprior.py), current store + current
position vocabulary: peak_ib = best-3 of >=6-game seasons else 0 · debut 2006-2020 · isotonic
(decreasing) on effpk · pool + per-position blend w = min(n/200, 1) * 0.6 · picks 1-70, 2dp.

MODERNIZED = the same estimand, consistent with today's laws:
  - cohorts debut 2006-2021 (the band's current resolved-career rule);
  - SMOOTH over pick (L-SMOOTH): isotonic at integer picks -> 5-point centered moving average ->
    non-increasing re-projection (PAVA), so the curve is monotone AND has no plateau cliffs;
  - MEASURED credibility: w_pos = n_pos / (n_pos + K), K selected by 5-fold player-split CV on the
    blended prior's squared error (grid declared below) — no hard 0.6 ceiling;
  - T1 note: the fabricated-zeros rule does not touch this construction (only >=6-game seasons
    aggregate; a fabricated 0-game season never enters peak_ib) — stated, not silently assumed.

Runs read-only against the engine (census-script loading pattern). Writes tables to --out.
"""
import argparse, contextlib, io, json, os, sys
import numpy as np
from sklearn.isotonic import IsotonicRegression

sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest
config_manifest.enforce('gate')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA = g['MA']

POS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
K_GRID = [50, 100, 200, 400, 800]

def best(ss, n):
    a = sorted([x['avg'] for x in ss if x['games'] >= 6], reverse=True)[:n]
    return float(np.mean(a)) if a else None

def peak_ib(p):
    return best(p['scoring'], 3) or 0.0

def pop(lo, hi):
    return [p for p in MA.data if MA.GRP.get(p['pos']) and lo <= MA.debut(p) <= hi]

def fit_iso(players):
    if len(players) < 5:
        return None
    xs = np.array([MA.effpk(p) for p in players]); ys = np.array([peak_ib(p) for p in players])
    return IsotonicRegression(increasing=False, out_of_bounds='clip').fit(xs, ys)

def faithful_table(train):
    pool = fit_iso(train)
    pf = {pos: fit_iso([p for p in train if MA.GRP[p['pos']] == pos]) for pos in POS}
    nc = {pos: sum(1 for p in train if MA.GRP[p['pos']] == pos) for pos in POS}
    def bp(pos, pk):
        pv = pool.predict([pk])[0]
        f = pf[pos]
        if f is None: return pv
        w = min(nc[pos] / 200.0, 1.0) * 0.6
        return w * f.predict([pk])[0] + (1 - w) * pv
    return {pos: {str(pk): round(float(bp(pos, pk)), 2) for pk in range(1, 71)} for pos in POS}, nc

def smooth_curve(iso, picks):
    y = iso.predict(picks.astype(float))
    k = np.ones(5) / 5.0
    ypad = np.concatenate([[y[0]] * 2, y, [y[-1]] * 2])
    ysm = np.convolve(ypad, k, mode='valid')
    proj = IsotonicRegression(increasing=False).fit(picks, ysm)     # re-project monotone
    return proj.predict(picks.astype(float))

def modern_table(train):
    picks = np.arange(1, 71)
    pool_iso = fit_iso(train)
    pool_s = smooth_curve(pool_iso, picks)
    pos_s, nc = {}, {}
    for pos in POS:
        pl = [p for p in train if MA.GRP[p['pos']] == pos]
        nc[pos] = len(pl)
        f = fit_iso(pl)
        pos_s[pos] = smooth_curve(f, picks) if f is not None else pool_s
    # measured credibility K by 5-fold player-split CV on blended squared error
    rng = np.random.RandomState(0)
    order = rng.permutation(len(train))
    folds = np.array_split(order, 5)
    def cv_err(K):
        err, n = 0.0, 0
        for i in range(5):
            te = [train[j] for j in folds[i]]
            tr = [train[j] for f2 in folds[:i] + folds[i+1:] for j in f2]
            pool_i = fit_iso(tr)
            for pos in POS:
                pl_tr = [p for p in tr if MA.GRP[p['pos']] == pos]
                f = fit_iso(pl_tr)
                w = len(pl_tr) / (len(pl_tr) + float(K))
                for p in te:
                    if MA.GRP[p['pos']] != pos: continue
                    pk = min(MA.effpk(p), 70)
                    pv = pool_i.predict([pk])[0]
                    pred = w * (f.predict([pk])[0] if f is not None else pv) + (1 - w) * pv
                    err += (pred - peak_ib(p)) ** 2; n += 1
        return err / n
    errs = {K: cv_err(K) for K in K_GRID}
    Kbest = min(errs, key=errs.get)
    tbl = {}
    for pos in POS:
        w = nc[pos] / (nc[pos] + float(Kbest))
        tbl[pos] = {str(int(pk)): round(float(w * pos_s[pos][i] + (1 - w) * pool_s[i]), 2)
                    for i, pk in enumerate(picks)}
    return tbl, nc, Kbest, errs

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', required=True)
    a = ap.parse_args()
    frozen = json.load(open(os.path.join(os.environ['RL_REPO'], 'engine/rl_after/bust_prior_table.json')))
    faith, nc_f = faithful_table(pop(2006, 2020))
    modern, nc_m, Kbest, errs = modern_table(pop(2006, 2021))
    def dev(a_, b_):
        d = [abs(a_[pos][str(pk)] - b_[pos][str(pk)]) for pos in POS for pk in range(1, 71)]
        return float(np.mean(d)), float(np.max(d))
    out = {'frozen_md5_note': 'engine/rl_after/bust_prior_table.json as committed',
           'faithful': faith, 'modern': modern,
           'faithful_counts': nc_f, 'modern_counts': nc_m,
           'modern_K_selected': Kbest, 'modern_K_cv_errors': errs,
           'dev_faithful_vs_frozen': dev(faith, frozen),
           'dev_modern_vs_frozen': dev(modern, frozen),
           'dev_modern_vs_faithful': dev(modern, faith)}
    json.dump(out, open(a.out, 'w'), indent=1)
    print('K selected:', Kbest, '| cv errs:', {k: round(v, 1) for k, v in errs.items()})
    print('mean/max |dev| faithful-vs-frozen:', out['dev_faithful_vs_frozen'])
    print('mean/max |dev| modern-vs-frozen  :', out['dev_modern_vs_frozen'])
    print('mean/max |dev| modern-vs-faithful:', out['dev_modern_vs_faithful'])
    for pos in POS:
        w = nc_m[pos] / (nc_m[pos] + float(Kbest))
        print('  %-5s n=%3d  modern w=%.2f  (faithful w=%.2f)  p1 %6.1f/%6.1f/%6.1f  p40 %5.1f/%5.1f/%5.1f (frozen/faithful/modern)'
              % (pos, nc_m[pos], w, min(nc_f[pos]/200.0, 1.0)*0.6,
                 frozen[pos]['1'], faith[pos]['1'], modern[pos]['1'],
                 frozen[pos]['40'], faith[pos]['40'], modern[pos]['40']))
    print('wrote', a.out)

main()
