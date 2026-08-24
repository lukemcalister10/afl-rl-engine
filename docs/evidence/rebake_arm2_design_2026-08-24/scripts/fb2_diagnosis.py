#!/usr/bin/env python3
"""ARM 2 — FB2 FIRED. THIS IS THE DIAGNOSIS, NOT A DEFENCE.

WHAT HAPPENED
  Two out-of-sample protocols disagree IN SIGN about the same model:
    * study B's WALK-FORWARD BY AS-OF YEAR (train YEAR<=T, score T+1..T+3; T=2014/2017/2020) — the
      protocol v831 D1 pointed the bake at, and the one this arm's settings were SELECTED on:
          ARM 2  3.9058   incumbent  3.9211      ARM 2 is 0.39% BETTER
    * study A section 5.1's ROLLING-ORIGIN BY DEBUT YEAR, whole careers held out — the standing pinball
      monitor, and the protocol ARM 1's filed zero point 3.9788 came from:
          ARM 2  4.0563   incumbent  3.9788      ARM 2 is 1.95% WORSE, at ALL THREE horizons
  Prereg falsifier FB2 is written against the second one. It has FIRED. The prereg's instruction is
  "report and stop", and this arm does — but a bare "it fired" leaves the owner nothing to rule on, so
  this script asks the two questions that decide what it MEANS.

QUESTION 1 — DO THE TWO PROTOCOLS HOLD OUT THE SAME THING? (they do not, and the difference is leakage)
  Study A holds out WHOLE CAREERS: a test player has NO training row. Its own docstring says why — "a
  row-random split would leak a player's own future into his own training rows".
  Study B's as-of-year split does not hold out players at all: a player drafted in 2010 contributes rows
  Y=2010..2014 to TRAIN at T=2014 and rows Y=2015..2017 to TEST. His own earlier rows teach the model
  about him. THIS SCRIPT MEASURES THAT OVERLAP DIRECTLY — what share of study B's test rows belong to a
  player who also has training rows in the same split. If it is large, then the settings were selected on
  a protocol with within-player leakage, and study A's verdict is the one that describes a fresh player.

QUESTION 2 — IS IT THE CONSTRUCTION OR THE SETTINGS?
  The declared stage-1 grid and the declared a* grid are re-scored UNDER STUDY A'S PROTOCOL. If some
  declared point beats the incumbent there, then the exact arm is fine and the SELECTION PROTOCOL was
  the defect. If NO point on the declared grid beats it, the exact construction genuinely costs accuracy
  on fresh players and that is the finding to bring back.
  NOTHING IS RE-SELECTED HERE. This is a diagnosis run AFTER the candidate was built and filed; the
  candidate's settings stay what the declared, prereg'd rule chose. Re-selecting on the protocol that
  embarrassed the first selection would be exactly the post-hoc move P9 exists to prevent.
"""
import argparse, contextlib, importlib.util, io, json, os, sys, time

import numpy as np
from sklearn.ensemble import GradientBoostingRegressor

Q5 = [0.10, 0.30, 0.50, 0.70, 0.90]
SPLITS_B = (2014, 2017, 2020)
FOLDS_A = ((2012, 2013, 2015), (2015, 2016, 2018), (2018, 2019, 2021))


def _L(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    sys.modules[n] = m
    with contextlib.redirect_stdout(io.StringIO()):
        s.loader.exec_module(m)
    return m


def pinball(yt, yp, q):
    d = np.asarray(yt, float) - np.asarray(yp, float)
    return float(np.mean(np.maximum(q * d, (q - 1.0) * d)))


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
    PR = _L('PR_fb2', os.path.join(fv, 'par_redesign.py'))
    cp = PR.cp
    cp._lvl_eff = PR.lvl_par                      # PAR-CENTRED — what cm_400 trains on
    SEL = json.load(open(a.selection))
    S = SEL['SELECTION']

    fo = cp.first_observable_season()
    X, y, yr, debut, pid = [], [], [], [], []
    for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
        if cp.debutyr(p) > 2021 or not (p.get('pick') or p.get('_ft')):
            continue
        d0 = cp.debutyr(p) - 1
        last = max([x['year'] for x in p['scoring']] + [d0])
        for Y in range(d0, min(last, 2026) + 1):
            if fo is not None and d0 < Y < fo:
                continue
            X.append(cp._feat(p, Y)); y.append(cp.fwd_best3_from(p, Y, 2026))
            yr.append(Y); debut.append(cp.debutyr(p)); pid.append(p['player'])
    X = np.array(X, float); y = np.array(y, float)
    yr = np.array(yr, int); debut = np.array(debut, int); pid = np.array(pid)
    R = {'design_shape': list(X.shape)}
    print('design %r  PAR-centred' % (X.shape,))

    # ---------------------------------------------------------------- QUESTION 1: the overlap
    print('\n=== Q1 — WITHIN-PLAYER OVERLAP IN THE SELECTION PROTOCOL (study B, as-of year) ===')
    ov = {}
    for T in SPLITS_B:
        tr = yr <= T
        te = (yr > T) & (yr <= T + 3)
        trp = set(pid[tr])
        share = float(np.mean([pid[i] in trp for i in np.where(te)[0]])) if te.sum() else 0.0
        ov['T%d' % T] = {'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                         'test_rows_whose_player_is_also_in_train_pct': round(100.0 * share, 2),
                         'test_players': len(set(pid[te])),
                         'test_players_also_in_train': len(set(pid[te]) & trp)}
        print('  T=%d  test rows %5d  of which the player ALSO has training rows: %6.2f%%   '
              '(%d of %d test players)'
              % (T, te.sum(), 100.0 * share, ov['T%d' % T]['test_players_also_in_train'],
                 ov['T%d' % T]['test_players']))
    print('\n  study A, for contrast — whole careers held out by DEBUT YEAR:')
    ova = {}
    for i, (aa, b, c) in enumerate(FOLDS_A, 1):
        tr = debut <= aa
        te = (debut >= b) & (debut <= c)
        trp = set(pid[tr])
        share = float(np.mean([pid[j] in trp for j in np.where(te)[0]])) if te.sum() else 0.0
        ova['fold%d' % i] = {'n_train': int(tr.sum()), 'n_test': int(te.sum()),
                             'test_rows_whose_player_is_also_in_train_pct': round(100.0 * share, 2)}
        print('  fold %d  test rows %5d  of which the player ALSO has training rows: %6.2f%%'
              % (i, te.sum(), 100.0 * share))
    R['overlap_selection_protocol_studyB'] = ov
    R['overlap_monitor_protocol_studyA'] = ova

    # ---------------------------------------------------------------- QUESTION 2: the grid under study A
    print('\n=== Q2 — THE DECLARED GRIDS, RE-SCORED UNDER STUDY A\'S PROTOCOL (diagnosis, NOT a re-selection) ===')

    def wf_A(Xs, hp, agehill, halflife):
        per = []
        for aa, b, c in FOLDS_A:
            tr = debut <= aa
            te = (debut >= b) & (debut <= c)
            w = EM.recency_weight(yr[tr], halflife, int(yr[tr].max())) if halflife else None
            per.append(float(np.mean([
                pinball(y[te], EM.make_estimator(q, Xs.shape[1], agehill, hp)
                        .fit(Xs[tr], y[tr], sample_weight=w).predict(Xs[te]), q) for q in Q5])))
        return [round(v, 4) for v in per], round(float(np.mean(per)), 4)

    inc = []
    for aa, b, c in FOLDS_A:
        tr = debut <= aa
        te = (debut >= b) & (debut <= c)
        inc.append(float(np.mean([
            pinball(y[te], GradientBoostingRegressor(loss='quantile', alpha=q, n_estimators=400,
                                                     max_depth=4, learning_rate=0.05,
                                                     min_samples_leaf=25, random_state=0)
                    .fit(X[tr], y[tr]).predict(X[te]), q) for q in Q5])))
    INC = round(float(np.mean(inc)), 4)
    R['incumbent_under_studyA_5legs'] = {'folds': [round(v, 4) for v in inc], 'mean': INC}
    print('  incumbent (5 legs, study A folds)     : %.4f  %s' % (INC, [round(v, 4) for v in inc]))

    Xa = EM.apply_age_hill(X, S['a_star'])
    grid = {}
    for lr in SEL['declared_grids']['stage1_learning_rate']:
        for it in SEL['declared_grids']['stage1_max_iter']:
            hp = dict(SEL['declared_grids']['stage1_fixed'], learning_rate=lr, max_iter=it)
            t0 = time.time()
            folds, mean = wf_A(Xa, hp, True, None)
            grid['lr%s_it%d' % (lr, it)] = {'folds': folds, 'mean': mean,
                                            'beats_incumbent': mean < INC}
            print('    lr=%-4s it=%-5d  mean %.4f  %s  (%.0fs)'
                  % (lr, it, mean, 'BEATS' if mean < INC else '', time.time() - t0), flush=True)
    R['stage1_grid_under_studyA'] = grid
    best = min(grid, key=lambda k: grid[k]['mean'])
    R['best_declared_point_under_studyA'] = {'key': best, **grid[best]}

    # the level-only arm (no age hill) — separates the constraint from the reparameterisation
    lo = {}
    for lr in (0.6, 1.0):
        for it in (800, 1600):
            hp = dict(SEL['declared_grids']['stage1_fixed'], learning_rate=lr, max_iter=it)
            folds, mean = wf_A(X, hp, False, None)
            lo['lr%s_it%d' % (lr, it)] = {'folds': folds, 'mean': mean, 'beats_incumbent': mean < INC}
            print('    LEVEL-ONLY (no age hill) lr=%-4s it=%-5d  mean %.4f  %s'
                  % (lr, it, mean, 'BEATS' if mean < INC else ''), flush=True)
    R['level_only_arm_under_studyA'] = lo

    # the selected point WITH the weight, so the weight's cost here is separable
    folds, mean = wf_A(Xa, S['hyperparameters'], True, S['recency_halflife_years'])
    R['selected_point_with_weight_under_studyA'] = {'folds': folds, 'mean': mean}
    folds0, mean0 = wf_A(Xa, S['hyperparameters'], True, None)
    R['selected_point_no_weight_under_studyA'] = {'folds': folds0, 'mean': mean0}
    print('  selected point, weight ON             : %.4f' % mean)
    print('  selected point, weight OFF            : %.4f' % mean0)
    print('  => the recency weight costs %+.3f%% under study A\'s protocol'
          % (100.0 * (mean - mean0) / mean0))

    anyb = any(v['beats_incumbent'] for v in list(grid.values()) + list(lo.values()))
    R['VERDICT'] = (
        'THE SETTINGS, NOT THE CONSTRUCTION — at least one DECLARED grid point beats the incumbent under '
        'study A\'s protocol, so the exact arm can fit fresh players at least as well; the selection '
        'protocol chose the wrong point on it.' if anyb else
        'THE CONSTRUCTION — NO point on the declared grid beats the incumbent under study A\'s '
        'whole-career protocol. The exact-monotone arm costs measurable accuracy on players the model '
        'has never seen, and that is the finding to bring back. It does NOT invalidate the law-3 result '
        '(V3 is zero either way); it prices it.')
    print('\nVERDICT: %s' % R['VERDICT'])
    if a.json:
        json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
