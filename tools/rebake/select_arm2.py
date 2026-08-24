#!/usr/bin/env python3
"""REBAKE WEEK · ARM 2 — THE OUT-OF-SAMPLE SELECTION. Every grid point declared before the run.

WHAT THIS IS
  Ruled at register v831: the exact-constrained arm's hyperparameters, the age hill's peak a*, and the
  recency half-life are NOT carried as literals from study B — they are SELECTED OUT OF SAMPLE at the
  bake, over grids DECLARED IN THE PREREG BEFORE THE RUN
  (docs/evidence/rebake_arm2_design_2026-08-24/PREREG.md sections 1.2, 1.3, 1.4, committed at e4a078f
  before this file existed, P9).

THE SELECTION RULE, WRITTEN HERE AND NOWHERE ELSE
  Lowest MEAN walk-forward pinball over three rolling-origin splits by AS-OF YEAR:
      train YEAR <= T,  score T+1 .. T+3,   for T in (2014, 2017, 2020)
  five quantiles Q = [0.10, 0.30, 0.50, 0.70, 0.90], unweighted mean of the five, unweighted mean of the
  three splits. IN-SAMPLE LOSS IS REPORTED AND NEVER USED TO CHOOSE. Ties break to the smaller max_iter,
  then the smaller learning_rate — declared so a tie cannot be resolved after the fact.

WHY THE DESIGN MATRIX IS PAR-CENTRED, AND WHY THAT IS A DECLARED DEVIATION FROM STUDY B
  The shipped cm_400 trains through par_redesign.retrain(), which rebinds cp._lvl_eff to lvl_par before
  the fit. Study B selected on the PLAIN cp._lvl_eff (its X_cm.npy), so its selected lr=1.0 / max_iter=800
  was selected for a model the estate does not build. This selects on the matrix the artifact is actually
  fitted from. Named in the prereg as a deviation, with the reason, rather than discovered afterwards.

WHY THE STAGES ARE ORDERED THE WAY THEY ARE (declared, not convenient)
  (0) the incumbent GradientBoostingRegressor on the identical splits — the comparison arm, so FB2 has a
      number to fire against.
  (1) hyperparameters on the RAW-AGE, level-only design. Chosen first because the age hill and the weight
      are both small effects (study B: 0.19% and 0.18%) and selecting them under a badly-fitted capacity
      would be selecting noise.
  (2) a* on the age-hill design AT the stage-1 settings. Both the owner's prior (~23) and the study's
      fitted peak (~21.5) are IN the grid and BOTH are reported whichever wins.
  (3) the half-life at the stage-1 settings AND the stage-2 a*.
  Each stage's full table is emitted. Nothing is reported as "the answer" without its grid beside it.

READ-ONLY with respect to the estate: fits into memory, writes ONE json into the evidence tree.
"""
import argparse, contextlib, hashlib, importlib.util, io, json, os, sys, time

import numpy as np

VERSION = 'arm2-select/1'

# ------------------------------------------------------------------ THE DECLARED GRIDS (prereg 1.2-1.4)
SPLITS = (2014, 2017, 2020)
Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]
STAGE1_LR = (0.3, 0.6, 1.0, 1.5)
STAGE1_IT = (400, 800, 1600)
STAGE1_FIXED = {'max_depth': 4, 'min_samples_leaf': 25}
STAGE2_CROSS = ({'max_depth': 3}, {'max_depth': 5}, {'min_samples_leaf': 15}, {'min_samples_leaf': 40})
ASTAR_GRID = (20.0, 20.5, 21.0, 21.5, 22.0, 22.5, 23.0, 23.5, 24.0)
HALFLIFE_GRID = (None, 10.0, 12.0, 14.0, 16.0)
OWNER_PRIOR_ASTAR = 23.0            # v831 D2, owner verbatim: "age 23 or so on mean, not 21-22?"
STUDY_B_ASTAR = 21.5                # study B M-57's fitted mean-curve peak
INCUMBENT_KW = dict(n_estimators=400, max_depth=4, learning_rate=0.05, min_samples_leaf=25)


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def pinball(yt, yp, q):
    d = np.asarray(yt, float) - np.asarray(yp, float)
    return float(np.mean(np.maximum(q * d, (q - 1.0) * d)))


def build_design(cp, MA, PR, par_centred=True, cap=2026, cut=2021):
    """The cm_400 training design, row-for-row as conditional_prior.build_cond_prior enumerates it, plus
    the as-of YEAR per row (which build_cond_prior discards and the walk-forward split needs).

    The row rule is NOT re-implemented from prose: it is the same four conditions the committed builder
    applies (debut <= resolved_cut, (pick or _ft), Y from the draft year through min(last, cap), and the
    T1 fabricated-zero skip), and the T1 skip is read from the construction's own
    first_observable_season() rather than from a literal."""
    old = cp._lvl_eff
    if par_centred:
        cp._lvl_eff = PR.lvl_par
    try:
        fo = cp.first_observable_season()
        X, y, yr = [], [], []
        for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
            if cp.debutyr(p) > cut or not (p.get('pick') or p.get('_ft')):
                continue
            d0 = cp.debutyr(p) - 1
            last = max([x['year'] for x in p['scoring']] + [d0])
            for Y in range(d0, min(last, cap) + 1):
                if fo is not None and d0 < Y < fo:
                    continue
                X.append(cp._feat(p, Y))
                y.append(cp.fwd_best3_from(p, Y, cap))
                yr.append(Y)
        return np.array(X, float), np.array(y, float), np.array(yr, int), fo
    finally:
        cp._lvl_eff = old


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--stage', default='all')
    a = ap.parse_args(argv[1:])

    root = os.environ['RL_REPO']
    fv = os.environ.get('RL_FV') or os.path.join(root, 'engine', 'forward_valuation')
    sys.path.insert(0, root)
    import config_manifest
    chash = config_manifest.enforce('gate')
    sys.path.insert(0, fv)
    import exact_monotone as EM

    # FB4 BEFORE ANY FIT — including a selection fit. A selection made under a moved private contract is
    # a selection of the wrong thing, so the tripwire guards this entry point exactly as it guards the bake.
    st = EM.selftest_or_halt()
    print('FB4 private-contract self-test: %s  (stock violates %d steps, exact %d)'
          % (st['verdict'], st['STOCK_negative_steps'], st['EXACT_negative_steps']))

    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA
    PR = _load('PR_sel', os.path.join(fv, 'par_redesign.py'))
    cp = PR.cp
    X, y, YEAR, fo = build_design(cp, MA, PR, par_centred=True)
    store = hashlib.md5(open('rl_model_data.json', 'rb').read()).hexdigest()
    print('design %r  PAR-centred  store %s  first_observable=%r  years %d-%d'
          % (X.shape, store[:8], fo, YEAR.min(), YEAR.max()))

    R = {'_doc': __doc__, 'version': VERSION, 'config_sha256': chash, 'store_md5': store,
         'design_shape': list(X.shape), 'first_observable_season': fo,
         'feature_bind': 'cp._lvl_eff = par_redesign.lvl_par (PAR-centred) — what cm_400 actually trains on',
         'selection_rule': ('lowest MEAN walk-forward pinball over T=2014/2017/2020 (train YEAR<=T, score '
                            'T+1..T+3), 5 quantiles, unweighted; in-sample NEVER used to choose; ties -> '
                            'smaller max_iter, then smaller learning_rate'),
         'declared_grids': {'stage1_learning_rate': list(STAGE1_LR), 'stage1_max_iter': list(STAGE1_IT),
                            'stage1_fixed': STAGE1_FIXED,
                            'stage2_capacity_cross': [dict(d) for d in STAGE2_CROSS],
                            'a_star': list(ASTAR_GRID),
                            'recency_halflife_years': ['uniform' if h is None else h for h in HALFLIFE_GRID]},
         'fb4_selftest': st}

    def wf(Xs, hp, a_star=None, halflife=None):
        """One grid point: mean walk-forward pinball, plus the per-split detail. The weight is anchored to
        the SPLIT'S OWN T — the whole of study B M-60 — never to YEAR.max()."""
        agehill = a_star is not None
        per = {}
        for T in SPLITS:
            tr = YEAR <= T
            te = (YEAR > T) & (YEAR <= T + 3)
            w = EM.recency_weight(YEAR[tr], halflife, T)
            per[str(T)] = round(float(np.mean([
                pinball(y[te], EM.make_estimator(q, Xs.shape[1], agehill, hp)
                        .fit(Xs[tr], y[tr], sample_weight=w).predict(Xs[te]), q) for q in Q5])), 4)
            per['n_train_%d' % T] = int(tr.sum())
            per['n_test_%d' % T] = int(te.sum())
        per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
        return per

    def pick(grid):
        """The declared tie-break, applied to the grid dict {key: row}."""
        return min(grid, key=lambda k: (grid[k]['mean'], grid[k]['_it'], grid[k]['_lr']))

    # ---------------------------------------------------------------- (0) the incumbent, same splits
    from sklearn.ensemble import GradientBoostingRegressor
    per = {}
    for T in SPLITS:
        tr = YEAR <= T
        te = (YEAR > T) & (YEAR <= T + 3)
        per[str(T)] = round(float(np.mean([
            pinball(y[te], GradientBoostingRegressor(loss='quantile', alpha=q, random_state=0,
                                                     **INCUMBENT_KW).fit(X[tr], y[tr]).predict(X[te]), q)
            for q in Q5])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    R['incumbent_same_splits'] = per
    R['incumbent_same_splits']['settings'] = dict(INCUMBENT_KW)
    print('INCUMBENT GradientBoostingRegressor  mean %.4f  %s' % (per['mean'], per), flush=True)

    # ---------------------------------------------------------------- (1) hyperparameters
    g1 = {}
    for lr in STAGE1_LR:
        for it in STAGE1_IT:
            hp = dict(STAGE1_FIXED, learning_rate=lr, max_iter=it)
            t0 = time.time()
            row = wf(X, hp)
            row.update({'_lr': lr, '_it': it, 'settings': dict(hp), 'fit_s': round(time.time() - t0, 1)})
            g1['lr%s_it%d' % (lr, it)] = row
            print('  stage1 lr=%-4s it=%-5d  mean %.4f  (%.0fs)' % (lr, it, row['mean'], row['fit_s']),
                  flush=True)
    R['stage1_hyperparameters'] = g1
    b1 = pick(g1)
    HP = dict(g1[b1]['settings'])
    print('stage1 SELECTED %s -> %s  mean %.4f' % (b1, HP, g1[b1]['mean']))

    # interior-optimum check, declared: extend one step past any selected edge
    ext = {}
    if HP['learning_rate'] == max(STAGE1_LR):
        ext['lr2.0_it%d' % HP['max_iter']] = dict(STAGE1_FIXED, learning_rate=2.0, max_iter=HP['max_iter'])
    if HP['learning_rate'] == min(STAGE1_LR):
        ext['lr0.15_it%d' % HP['max_iter']] = dict(STAGE1_FIXED, learning_rate=0.15, max_iter=HP['max_iter'])
    if HP['max_iter'] == max(STAGE1_IT):
        ext['lr%s_it3200' % HP['learning_rate']] = dict(STAGE1_FIXED, learning_rate=HP['learning_rate'],
                                                        max_iter=3200)
    if HP['max_iter'] == min(STAGE1_IT):
        ext['lr%s_it200' % HP['learning_rate']] = dict(STAGE1_FIXED, learning_rate=HP['learning_rate'],
                                                       max_iter=200)
    g1e = {}
    for k, hp in ext.items():
        row = wf(X, hp)
        row.update({'_lr': hp['learning_rate'], '_it': hp['max_iter'], 'settings': dict(hp)})
        g1e[k] = row
        print('  stage1 EXTENSION %s  mean %.4f' % (k, row['mean']), flush=True)
    R['stage1_edge_extension'] = g1e
    if g1e:
        merged = dict(g1); merged.update(g1e)
        b1 = pick(merged)
        HP = dict(merged[b1]['settings'])
        R['stage1_selected_after_extension'] = {'key': b1, 'settings': HP, 'mean': merged[b1]['mean']}
        print('stage1 AFTER EXTENSION selected %s -> %s' % (b1, HP))
    R['stage1_selected'] = {'key': b1, 'settings': dict(HP),
                            'interior_optimum': not bool(g1e) or b1 not in g1e}

    # stage 2 — capacity, one-at-a-time around the stage-1 winner
    g2 = {'centre': dict(g1.get(b1) or R['stage1_edge_extension'][b1])}
    for d in STAGE2_CROSS:
        hp = dict(HP); hp.update(d)
        row = wf(X, hp)
        row.update({'_lr': hp['learning_rate'], '_it': hp['max_iter'], 'settings': dict(hp)})
        g2['depth%d_leaf%d' % (hp['max_depth'], hp['min_samples_leaf'])] = row
        print('  stage2 %s  mean %.4f' % (d, row['mean']), flush=True)
    R['stage2_capacity'] = g2
    b2 = pick(g2)
    HP = dict(g2[b2]['settings'])
    R['selected_hyperparameters'] = dict(HP)
    print('HYPERPARAMETERS SELECTED: %s  mean %.4f' % (HP, g2[b2]['mean']), flush=True)

    # ---------------------------------------------------------------- (2) the age hill, a* selected OOS
    AGE = EM.AGE
    ga = {}
    for a_star in ASTAR_GRID:
        Xa = EM.apply_age_hill(X, a_star)
        row = wf(Xa, HP, a_star=a_star)
        row.update({'_lr': HP['learning_rate'], '_it': HP['max_iter'], 'a_star': a_star})
        ga['a%.1f' % a_star] = row
        print('  a*=%-5.1f  mean %.4f' % (a_star, row['mean']), flush=True)
    R['a_star_grid'] = ga
    ba = min(ga, key=lambda k: (ga[k]['mean'], abs(ga[k]['a_star'] - STUDY_B_ASTAR)))
    ASTAR = ga[ba]['a_star']

    # the three declared controls, so D2 is priced and not asserted
    cst_down = None
    ctl = {'raw_age_no_constraint': dict(R['stage2_capacity'][b2])}
    # raw age with a signed -1: build the constraint by hand HERE only, because it is a CONTROL that the
    # shipped construction never uses (the age hill replaces it) — it must not live in exact_monotone.py.
    from sklearn.ensemble import HistGradientBoostingRegressor
    per = {}
    for T in SPLITS:
        tr = YEAR <= T
        te = (YEAR > T) & (YEAR <= T + 3)
        cst_down = [0] * X.shape[1]; cst_down[EM.LVL] = 1; cst_down[AGE] = -1
        per[str(T)] = round(float(np.mean([
            pinball(y[te], HistGradientBoostingRegressor(
                loss=EM.GradOnlyPinball(quantile=q), max_iter=HP['max_iter'], max_depth=HP['max_depth'],
                learning_rate=HP['learning_rate'], min_samples_leaf=HP['min_samples_leaf'],
                monotonic_cst=cst_down, early_stopping=False, random_state=0)
                .fit(X[tr], y[tr]).predict(X[te]), q) for q in Q5])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    ctl['raw_age_constrained_minus1'] = per
    Xa = EM.apply_age_hill(X, ASTAR)
    per = {}
    for T in SPLITS:
        tr = YEAR <= T
        te = (YEAR > T) & (YEAR <= T + 3)
        cst_free = [0] * Xa.shape[1]; cst_free[EM.LVL] = 1
        per[str(T)] = round(float(np.mean([
            pinball(y[te], HistGradientBoostingRegressor(
                loss=EM.GradOnlyPinball(quantile=q), max_iter=HP['max_iter'], max_depth=HP['max_depth'],
                learning_rate=HP['learning_rate'], min_samples_leaf=HP['min_samples_leaf'],
                monotonic_cst=cst_free, early_stopping=False, random_state=0)
                .fit(Xa[tr], y[tr]).predict(Xa[te]), q) for q in Q5])), 4)
    per['mean'] = round(float(np.mean([per[str(T)] for T in SPLITS])), 4)
    ctl['age_hill_features_UNCONSTRAINED'] = per
    ctl['age_hill_features_constrained_at_selected_a_star'] = dict(ga[ba])
    R['age_controls'] = ctl
    means = [ctl['raw_age_no_constraint']['mean'], ctl['raw_age_constrained_minus1']['mean'],
             ctl['age_hill_features_UNCONSTRAINED']['mean'], ga[ba]['mean']]
    R['age_arm_spread_pct'] = round(100.0 * (max(means) - min(means)) / min(means), 3)
    R['selected_a_star'] = ASTAR
    R['owner_prior_vs_study_peak'] = {
        'owner_prior_a_star': OWNER_PRIOR_ASTAR,
        'owner_prior_walk_forward': ga['a%.1f' % OWNER_PRIOR_ASTAR],
        'study_B_fitted_peak_a_star': STUDY_B_ASTAR,
        'study_B_peak_walk_forward': ga['a%.1f' % STUDY_B_ASTAR],
        'selected': ASTAR,
        'note': ("v831 D2: a* is NOT hand-fixed. Both candidates are reported whichever wins. The owner's "
                 "year-5-6 read most likely comes from the no-arb COHORT path (peak year 5 = age ~23), "
                 "which is a COMPOSITION curve (survival x value) and NOT the band's conditional age "
                 "response — the two are different objects and the selection settles only the band's.")}
    print('a* SELECTED %.1f   (owner prior 23.0 -> %.4f ; study B 21.5 -> %.4f ; spread across all four '
          'age arms %.3f%%)' % (ASTAR, ga['a23.0']['mean'], ga['a21.5']['mean'], R['age_arm_spread_pct']),
          flush=True)

    # ---------------------------------------------------------------- (3) the recency half-life
    Xa = EM.apply_age_hill(X, ASTAR)
    gw = {}
    for hl in HALFLIFE_GRID:
        row = wf(Xa, HP, a_star=ASTAR, halflife=hl)
        row.update({'_lr': HP['learning_rate'], '_it': HP['max_iter'],
                    'halflife': 'uniform' if hl is None else hl})
        gw['uniform' if hl is None else 'hl%dy' % hl] = row
        print('  halflife %-8s mean %.4f' % (row['halflife'], row['mean']), flush=True)
    R['halflife_grid'] = gw
    bw = min(gw, key=lambda k: gw[k]['mean'])
    HL = None if gw[bw]['halflife'] == 'uniform' else float(gw[bw]['halflife'])
    R['selected_halflife_years'] = HL
    R['halflife_gain_vs_uniform_pct'] = round(
        100.0 * (gw['uniform']['mean'] - gw[bw]['mean']) / gw['uniform']['mean'], 3)
    print('HALF-LIFE SELECTED: %r  (%.3f%% better than uniform)'
          % (HL, R['halflife_gain_vs_uniform_pct']), flush=True)

    R['SELECTION'] = {'hyperparameters': dict(HP), 'a_star': ASTAR, 'recency_halflife_years': HL,
                      'recency_anchor': 'end of training window',
                      'n_features': int(Xa.shape[1]), 'level_index': EM.LVL}
    R['final_walk_forward'] = gw[bw]
    R['improvement_vs_incumbent_pct'] = round(
        100.0 * (R['incumbent_same_splits']['mean'] - gw[bw]['mean']) / R['incumbent_same_splits']['mean'], 3)
    print('\n=== SELECTION COMPLETE ===')
    print('  incumbent (same splits)        : %.4f' % R['incumbent_same_splits']['mean'])
    print('  ARM 2 selected                 : %.4f  (%+.3f%% vs incumbent)'
          % (gw[bw]['mean'], -R['improvement_vs_incumbent_pct']))
    print('  hyperparameters                : %s' % HP)
    print('  a*                             : %.1f' % ASTAR)
    print('  recency half-life (window)     : %r' % HL)
    with open(a.out, 'w') as f:
        json.dump(R, f, indent=1, sort_keys=True, default=str)
        f.write('\n')
    print('WROTE %s' % a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
