#!/usr/bin/env python3
"""ARM 2 — THE PINBALL MONITOR, against study A section 5.1's baseline AND ARM 1's filed zero point.

THE PROTOCOL IS STUDY A'S, UNCHANGED, AND THAT IS THE POINT (docs/proposals/rebake_study_A/05_candidates.py):
  * rolling-origin split by DEBUT YEAR, whole careers held out (a row-random split would leak a player's
    own future into his own training rows):
        fold 1  train debut <= 2012   test debut 2013-2015
        fold 2  train debut <= 2015   test debut 2016-2018
        fold 3  train debut <= 2018   test debut 2019-2021
  * six legs Q6 = [.10,.30,.50,.70,.90,.97]
  * the engine's own two crossing repairs applied identically (np.sort over the five;
    band[5] = max(q97, band[4])) and INSTRUMENTED — the repair rates are a real reading, not decoration:
    study A's design (f) was caught partly BY them (11.6% sort repairs against 5.2%).
  * pinball per leg, unweighted mean of the six; folds pooled by unweighted mean

  NOTE THAT THIS IS A DIFFERENT SPLIT FROM THE SELECTION'S. The selection (tools/rebake/select_arm2.py)
  splits by AS-OF YEAR on three walk-forward origins; this splits by DEBUT YEAR holding whole careers
  out. They answer different questions and the second one was never used to choose anything — which is
  exactly why it is a fair monitor of a model selected on the first.

THE THREE ARMS, ON IDENTICAL FOLDS AND IDENTICAL ROWS:
  incumbent   GradientBoostingRegressor quantile, 400/4/0.05/25 (200 for .97) — study A's design (a)
  arm2        the exact-monotone construction at the OUT-OF-SAMPLE-SELECTED settings, with the age hill
              and the window-anchored recency weight
  arm2_nowt   the same, with the weight off — so the weight's contribution is separable here too

TWO FEATURE VARIANTS, and the reason is a real wrinkle ARM 1 filed:
  'plain'  cp._feat with the ORIGINAL cp._lvl_eff — what study A measured, the only variant comparable
           to its 3.9703.
  'par'    cp._feat with cp._lvl_eff rebound to par_redesign.lvl_par — what the SHIPPED cm_400 actually
           trains on. ARM 1 filed 3.9788 as the PAR-centred zero point for the design arms; that is the
           number this arm is measured against, and it is the honest comparison.
"""
import argparse, collections, contextlib, importlib.util, io, json, os, sys, time

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

Q6 = [0.10, 0.30, 0.50, 0.70, 0.90, 0.97]
NTREES = {0.10: 400, 0.30: 400, 0.50: 400, 0.70: 400, 0.90: 400, 0.97: 200}
BASELINE_A = 3.9703        # study A section 5.1, design (a), PLAIN feature
BASELINE_PAR = 3.9788      # ARM 1's filed PAR-centred zero point (register v834)


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
    X, y, cls, debut, yr = [], [], [], [], []
    for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
        if cp.debutyr(p) > CUT or not (p.get('pick') or p.get('_ft')):
            continue
        d0 = cp.debutyr(p) - 1
        last = max([x['year'] for x in p['scoring']] + [d0])
        for Y in range(d0, min(last, CAP) + 1):
            if fo is not None and d0 < Y < fo:          # T1
                continue
            X.append(cp._feat(p, Y)); y.append(cp.fwd_best3_from(p, Y, CAP))
            cls.append(entry_class(p, MA)); debut.append(cp.debutyr(p)); yr.append(Y)
    return (np.array(X, float), np.array(y, float), np.array(cls), np.array(debut, int),
            np.array(yr, int), fo)


def run(variant, cp, MA, PR, EM, SEL, arm):
    """arm in {'incumbent','arm2','arm2_nowt'} — identical folds, identical rows, identical repairs."""
    X, y, cls, debut, yr, fo = build_design(cp, MA, PR, variant)
    S = SEL['SELECTION']
    if arm != 'incumbent':
        X = EM.apply_age_hill(X, S['a_star'])
    print('\n=== %s / %s : design %r ===' % (arm, variant, X.shape))
    folds = [((debut <= a), (debut >= b) & (debut <= c))
             for a, b, c in ((2012, 2013, 2015), (2015, 2016, 2018), (2018, 2019, 2021))]
    agg = collections.defaultdict(list)
    out = {'design_shape': list(X.shape), 'folds': [], 'arm': arm}
    for i, (tr, te) in enumerate(folds, 1):
        t0 = time.time()
        if arm == 'incumbent':
            M = {q: GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=NTREES[q],
                                              max_depth=4, learning_rate=0.05, min_samples_leaf=25,
                                              random_state=0).fit(X[tr], y[tr]) for q in Q6}
        else:
            hl = None if arm == 'arm2_nowt' else S['recency_halflife_years']
            # the weight is anchored to the END OF THIS FOLD'S TRAINING WINDOW — the same M-60 rule the
            # selection used, applied to this split's own definition of "the end of the window".
            anchor = int(yr[tr].max())
            w = EM.recency_weight(yr[tr], hl, anchor)
            M = {q: EM.make_estimator(q, X.shape[1], True, S['hyperparameters'])
                 .fit(X[tr], y[tr], sample_weight=w) for q in Q6}
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
        agg['ns'].append(f['sort_repair_pct']); agg['nc'].append(f['ceil_repair_pct'])
        out['folds'].append(f)
        print('  fold %d  n_tr=%5d n_te=%5d  %5.1fs  pinball %.4f  covErr %.4f  sortfix %.1f%% '
              'ceilfix %.1f%%' % (i, tr.sum(), te.sum(), f['fit_s'], f['pinball_mean'],
                                  f['cov_abs_err'], f['sort_repair_pct'], f['ceil_repair_pct']),
              flush=True)
    out['pooled_pinball'] = round(float(np.mean(agg['pb'])), 5)
    out['pooled_cov_abs_err'] = round(float(np.mean(agg['cov'])), 5)
    out['pooled_sort_repair_pct'] = round(float(np.mean(agg['ns'])), 3)
    out['pooled_ceil_repair_pct'] = round(float(np.mean(agg['nc'])), 3)
    out['by_class'] = {k[4:]: round(float(np.mean(v)), 5) for k, v in agg.items() if k.startswith('pbc_')}
    print('  POOLED pinball %.4f   covErr %.4f   sortfix %.2f%%  ceilfix %.2f%%'
          % (out['pooled_pinball'], out['pooled_cov_abs_err'], out['pooled_sort_repair_pct'],
             out['pooled_ceil_repair_pct']))
    print('  by population: ' + '  '.join('%s %.4f' % (k, v) for k, v in sorted(out['by_class'].items())))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--selection', required=True)
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])
    root = os.environ['RL_REPO']
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path.insert(0, root)
    import config_manifest
    config_manifest.enforce('gate')
    sys.path.insert(0, fv)
    import exact_monotone as EM
    EM.selftest_or_halt()
    sys.path.insert(0, '.')
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA
    PR = _L('PR_pb2', os.path.join(fv, 'par_redesign.py'))
    cp = PR.cp
    SEL = json.load(open(a.selection))
    import hashlib
    res = {'baseline_study_A_5_1_design_a_PLAIN': BASELINE_A,
           'baseline_ARM1_filed_PAR_centred': BASELINE_PAR,
           'selection': SEL['SELECTION'],
           'store_md5': hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()}
    orig_lvl = cp._lvl_eff
    for variant in ('plain', 'par'):
        for arm in ('incumbent', 'arm2', 'arm2_nowt'):
            cp._lvl_eff = orig_lvl
            res['%s_%s' % (variant, arm)] = run(variant, cp, MA, PR, EM, SEL, arm)
    cp._lvl_eff = orig_lvl

    p_inc, p_a2 = res['par_incumbent']['pooled_pinball'], res['par_arm2']['pooled_pinball']
    pl_inc, pl_a2 = res['plain_incumbent']['pooled_pinball'], res['plain_arm2']['pooled_pinball']
    res['verdicts'] = {
        'PAR_vs_ARM1_zero_point_3_9788': {
            'arm2': p_a2, 'zero_point': BASELINE_PAR,
            'delta': round(p_a2 - BASELINE_PAR, 5),
            'delta_pct': round(100.0 * (p_a2 - BASELINE_PAR) / BASELINE_PAR, 3),
            'verdict': 'BEATS' if p_a2 < BASELINE_PAR else 'WORSE'},
        'PAR_vs_incumbent_same_folds': {
            'arm2': p_a2, 'incumbent': p_inc, 'delta': round(p_a2 - p_inc, 5),
            'delta_pct': round(100.0 * (p_a2 - p_inc) / p_inc, 3),
            'verdict': 'BEATS' if p_a2 < p_inc else 'WORSE — prereg falsifier FB2'},
        'PLAIN_vs_study_A_3_9703': {
            'arm2': pl_a2, 'baseline': BASELINE_A,
            'delta_pct': round(100.0 * (pl_a2 - BASELINE_A) / BASELINE_A, 3)},
        'PLAIN_vs_incumbent_same_folds': {
            'arm2': pl_a2, 'incumbent': pl_inc,
            'delta_pct': round(100.0 * (pl_a2 - pl_inc) / pl_inc, 3)},
        'per_horizon_vs_incumbent_PAR': [
            {'fold': i + 1,
             'incumbent': res['par_incumbent']['folds'][i]['pinball_mean'],
             'arm2': res['par_arm2']['folds'][i]['pinball_mean'],
             'arm2_better': res['par_arm2']['folds'][i]['pinball_mean']
                            < res['par_incumbent']['folds'][i]['pinball_mean']}
            for i in range(3)],
        'recency_weight_contribution_PAR_pct': round(
            100.0 * (res['par_arm2_nowt']['pooled_pinball'] - p_a2)
            / res['par_arm2_nowt']['pooled_pinball'], 3),
    }
    res['verdicts']['FB2_fires'] = not all(f['arm2_better'] for f in
                                           res['verdicts']['per_horizon_vs_incumbent_PAR'])
    print('\n================ PINBALL MONITOR — ARM 2 ================')
    print('  study A 5.1 design (a), PLAIN            : %.4f' % BASELINE_A)
    print('  ARM 1 filed PAR-centred zero point       : %.4f' % BASELINE_PAR)
    print('  ARM 2, PAR-centred (the shipped feature) : %.4f  (%+.3f%% vs the zero point)'
          % (p_a2, res['verdicts']['PAR_vs_ARM1_zero_point_3_9788']['delta_pct']))
    print('  incumbent, PAR-centred, SAME folds       : %.4f  (ARM 2 is %+.3f%% on it)'
          % (p_inc, res['verdicts']['PAR_vs_incumbent_same_folds']['delta_pct']))
    print('  ARM 2, PLAIN feature                     : %.4f  (%+.3f%% vs 3.9703)'
          % (pl_a2, res['verdicts']['PLAIN_vs_study_A_3_9703']['delta_pct']))
    print('  recency weight worth                     : %.3f%%'
          % res['verdicts']['recency_weight_contribution_PAR_pct'])
    print('  FB2 (worse than incumbent at ANY horizon): %s'
          % ('FIRES' if res['verdicts']['FB2_fires'] else 'does not fire'))
    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
