#!/usr/bin/env python3
"""ARM 1 — THE PINBALL MONITOR, against study A §5.1's baseline table.

THE PROTOCOL IS STUDY A'S, NOT A NEW ONE (docs/proposals/rebake_study_A/05_candidates.py):
  * rolling-origin split by DEBUT YEAR, whole careers held out (a row-random split would leak a
    player's own future into his own training rows):
        fold 1  train debut <= 2012   test debut 2013-2015
        fold 2  train debut <= 2015   test debut 2016-2018
        fold 3  train debut <= 2018   test debut 2019-2021
  * six legs Q6 = [.10,.30,.50,.70,.90,.97], trees as shipped {400 x5, 200 for .97}
  * the engine's own two crossing repairs applied identically (np.sort over the five;
    band[5] = max(q97, band[4])) and instrumented
  * pinball per leg, then the unweighted mean of the six; folds pooled by unweighted mean
  * design (a) STATUS QUO — classic GradientBoostingRegressor, no constraint. §5.1 baseline: 3.9703

TWO FEATURE VARIANTS ARE REPORTED, and the reason is a real wrinkle in the baseline:
  'plain'    cp._feat with the ORIGINAL cp._lvl_eff — this is what study A measured, so it is the
             only variant COMPARABLE to the 3.9703 number.
  'par'      cp._feat with cp._lvl_eff rebound to par_redesign.lvl_par — this is what the SHIPPED
             cm_400 is actually trained on (par_redesign.retrain()). Study A's own 08_victims.py
             flags the same caveat. Its number is NOT comparable to 3.9703 and is reported as its
             own zero point for future arms.

Run with cwd = the engine workspace and RL_REPO/RL_FV bound to the root under test.
"""
import argparse, collections, contextlib, importlib.util, io, json, os, sys, time
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
NTREES = {0.10: 400, 0.30: 400, 0.50: 400, 0.70: 400, 0.90: 400, 0.97: 200}
BASELINE_A = 3.9703          # study A §5.1, design (a) status quo, pooled over the three folds


def _L(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    with contextlib.redirect_stdout(io.StringIO()):
        s.loader.exec_module(m)
    return m


def entry_class(p, MA):
    t, pk = p.get('type'), p.get('pick') or 0
    if t == 'ND':
        return ('ND-early' if 1 <= pk <= 18 else 'ND-mid' if 19 <= pk <= 40
                else 'ND-late' if 41 <= pk <= 64 else 'ND-pool')
    return 'RD/PSD' if t in ('RD', 'PSD') else 'SSP/other'


def pinball(yt, qh, q):
    e = yt - qh
    return float(np.mean(np.maximum(q * e, (q - 1) * e)))


def guarded(B):
    P = np.sort(B[:, :5], axis=1)
    n_sort = int((np.abs(P - B[:, :5]) > 1e-12).any(axis=1).sum())
    top = np.maximum(B[:, 5], P[:, 4])
    n_ceil = int((B[:, 5] < P[:, 4] - 1e-12).sum())
    return np.column_stack([P, top]), n_sort, n_ceil


def build_design(cp, MA, PR, variant):
    if variant == 'par':
        cp._lvl_eff = PR.lvl_par
    CAP, CUT = 2026, 2021
    fo = cp.first_observable_season()
    X, y, cls, debut = [], [], [], []
    for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
        if cp.debutyr(p) > CUT or not (p.get('pick') or p.get('_ft')):
            continue
        d0 = cp.debutyr(p) - 1
        last = max([x['year'] for x in p['scoring']] + [d0])
        for Y in range(d0, min(last, CAP) + 1):
            if fo is not None and d0 < Y < fo:          # T1
                continue
            X.append(cp._feat(p, Y)); y.append(cp.fwd_best3_from(p, Y, CAP))
            cls.append(entry_class(p, MA)); debut.append(cp.debutyr(p))
    return (np.array(X, float), np.array(y, float), np.array(cls), np.array(debut, int), fo)


def run(variant, cp, MA, PR):
    X, y, cls, debut, fo = build_design(cp, MA, PR, variant)
    print('\n=== variant %r : design %r, first_observable=%r ===' % (variant, X.shape, fo))
    folds = [((debut <= a), (debut >= b) & (debut <= c))
             for a, b, c in ((2012, 2013, 2015), (2015, 2016, 2018), (2018, 2019, 2021))]
    agg = collections.defaultdict(list)
    out = {'design_shape': list(X.shape), 'folds': []}
    for i, (tr, te) in enumerate(folds, 1):
        t0 = time.time()
        M = {q: GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=NTREES[q],
                                          max_depth=4, learning_rate=0.05, min_samples_leaf=25,
                                          random_state=0).fit(X[tr], y[tr]) for q in Q6}
        B, ns, nc = guarded(np.column_stack([M[q].predict(X[te]) for q in Q6]))
        yt = y[te]
        pbs = [pinball(yt, B[:, j], q) for j, q in enumerate(Q6)]
        cvs = [float(np.mean(yt <= B[:, j])) for j in range(6)]
        f = {'fold': i, 'n_train': int(tr.sum()), 'n_test': int(te.sum()),
             'pinball': {('%.2f' % q): round(pbs[j], 5) for j, q in enumerate(Q6)},
             'coverage': {('%.2f' % q): round(cvs[j], 4) for j, q in enumerate(Q6)},
             'pinball_mean': round(float(np.mean(pbs)), 5),
             'cov_abs_err': round(float(np.mean(np.abs(np.array(cvs) - Q6))), 4),
             'sort_repair_pct': round(100.0 * ns / max(int(te.sum()), 1), 2),
             'ceil_repair_pct': round(100.0 * nc / max(int(te.sum()), 1), 2),
             'fit_s': round(time.time() - t0, 1)}
        for c in sorted(set(cls[te])):
            m = cls[te] == c
            if m.sum() < 25:
                continue
            agg['pbc_' + c].append(float(np.mean([pinball(yt[m], B[m, j], q)
                                                  for j, q in enumerate(Q6)])))
        agg['pb'].append(f['pinball_mean']); agg['cov'].append(f['cov_abs_err'])
        out['folds'].append(f)
        print('  fold %d  n_tr=%5d n_te=%5d  %5.1fs  pinball %.4f  covErr %.4f  sortfix %.1f%% '
              'ceilfix %.1f%%' % (i, tr.sum(), te.sum(), f['fit_s'], f['pinball_mean'],
                                  f['cov_abs_err'], f['sort_repair_pct'], f['ceil_repair_pct']),
              flush=True)
    out['pooled_pinball'] = round(float(np.mean(agg['pb'])), 5)
    out['pooled_cov_abs_err'] = round(float(np.mean(agg['cov'])), 5)
    out['by_class'] = {k[4:]: round(float(np.mean(v)), 5) for k, v in agg.items() if k.startswith('pbc_')}
    print('  POOLED pinball %.4f   covErr %.4f' % (out['pooled_pinball'], out['pooled_cov_abs_err']))
    print('  by population: ' + '  '.join('%s %.4f' % (k, v) for k, v in sorted(out['by_class'].items())))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])
    root = os.environ['RL_REPO']
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path.insert(0, root)
    import config_manifest
    config_manifest.enforce('gate')
    sys.path.insert(0, '.')
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA
    PR = _L('PR_pb', os.path.join(fv, 'par_redesign.py'))
    cp = PR.cp
    res = {'baseline_study_A_5_1_design_a': BASELINE_A,
           'store_md5': __import__('hashlib').md5(open('rl_model_data.json', 'rb').read()).hexdigest()}
    res['plain'] = run('plain', cp, MA, PR)
    res['par_centred'] = run('par', cp, MA, PR)
    d = res['plain']['pooled_pinball'] - BASELINE_A
    print('\n================ PINBALL MONITOR ================')
    print('  study A §5.1 design (a) baseline : %.4f' % BASELINE_A)
    print('  ARM 1, same protocol, current store, PLAIN feature : %.4f  (%+.4f, %+.2f%%)'
          % (res['plain']['pooled_pinball'], d, 100.0 * d / BASELINE_A))
    print('  ARM 1, PAR-CENTRED feature (what cm_400 actually trains on) : %.4f'
          % res['par_centred']['pooled_pinball'])
    print('  (the PAR number is NOT comparable to 3.9703 — different feature 9 — and is filed as its')
    print('   own zero point for the design arms.)')
    res['delta_vs_baseline'] = round(d, 5)
    res['delta_pct_vs_baseline'] = round(100.0 * d / BASELINE_A, 3)
    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
