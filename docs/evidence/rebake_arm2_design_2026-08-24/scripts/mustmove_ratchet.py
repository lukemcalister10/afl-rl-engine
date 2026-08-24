#!/usr/bin/env python3
"""ARM 2 — THE RATCHET MUST-MOVE PROOF (PREREG_STAIRCASE.md section 8; study B section 4.3).

WHAT IS OWED, VERBATIM, AND BY WHOM
  PREREG_STAIRCASE.md section 8 bound its own scaffolding's removal in advance: "its removal is a rebake
  MUST-MOVE PROOF: the rebake is not complete until this dial and its code are gone from
  _merged_recover.py and the board built without them reproduces the monotone behaviour from the
  constrained forests alone." This script is that proof, and it is deliberately three separate legs,
  because "the code is gone" and "the code was doing nothing" are different claims and only the second
  one justifies the first.

LEG 1 — M-52, RUN IN ANGER RATHER THAN QUOTED.
  The shipped knot reader was:
      for _e in np.asarray(_m.estimators_).ravel():
  Study B M-52 says HistGradientBoostingRegressor has no estimators_, and the supervisor verified it by
  reading _merged_recover.py:488. This leg EXECUTES the shipped expression against the candidate band and
  records the exception. It is the difference between "the studies agree the ratchet cannot ride through
  the estimator swap" and "we tried it and here is the traceback".

LEG 2 — THE MEASURED NO-OP, ON EVERY BOARD ROW.
  The ratchet is generalised to the new estimator's OWN split thresholds — read off _predictors[i][j].nodes
  where is_leaf is false and feature_idx == the level index, which is the exact analogue of the shipped
  reader's walk over tree_.threshold[tree_.feature == LVL]. FOUR LINES, and they live HERE, in the
  evidence tree, never in the shipped engine: writing them into _merged_recover.py would be exactly the
  "rewrite of the whole knot walker against the new estimator's own private internals" the comparison
  paper's F1 rejected as the more expensive of the two internal-API dependencies.
  Then, for every board row: the raw band, and the ratcheted band (componentwise running maximum over
  every knot at or below the row's level, the shipped construction). THE DIRECTIVE'S CLAIM IS THAT THESE
  ARE IDENTICAL — "the read-site ratchet finds nothing to fix on any row (a measured no-op)".
  This is a real falsifier: if the fit were only approximately monotone, the ratchet would find work, and
  the maximum absolute difference would be non-zero. On the INCUMBENT artifacts the same measurement
  returns a large number, and that control is run too so the instrument is proven able to see a
  difference. A no-op measured by an instrument that cannot detect work is not a measurement.

LEG 3 — BOARD (b) == BOARD (c).
  Done by the caller, not here: board (c) is the candidate, built by the branch's engine with the block
  deleted; board (b) is built by a SCRATCH engine copy with the block restored and _o44_xs generalised
  (scripts/make_ratchet_engine.py). Leg 2 is what makes leg 3's outcome predictable rather than lucky.

Usage: run from the engine workspace with the candidate root bound.
"""
import argparse, contextlib, io, json, os, sys, traceback

import numpy as np


def hist_level_knots(model, lvl):
    """The generalised knot reader — the exact analogue of the shipped tree_.threshold walk.

    Shipped (GradientBoostingRegressor):
        for e in np.asarray(m.estimators_).ravel():
            t = e.tree_;  thresholds where t.feature == LVL
    Here (HistGradientBoostingRegressor): the boosting rounds live in m._predictors, each round a list of
    one predictor per output; each predictor's `nodes` record array carries feature_idx / num_threshold /
    is_leaf. Split nodes on the level feature are the pieces of the step surface on that axis."""
    s = set()
    for rnd in model._predictors:
        for pr in rnd:
            nd = pr.nodes
            sel = (~nd['is_leaf'].astype(bool)) & (nd['feature_idx'] == lvl)
            s.update(float(v) for v in nd['num_threshold'][sel])
    return s


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--json')
    ap.add_argument('--lo', type=float, default=40.0)
    ap.add_argument('--hi', type=float, default=120.0)
    ap.add_argument('--eps', type=float, default=1e-9)
    a = ap.parse_args(argv[1:])

    sys.path.insert(0, os.environ['RL_REPO'])
    import config_manifest
    config_manifest.enforce('gate')
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, cp, cm, q97m, WQ6 = g['MA'], g['cp'], g['cm'], g['q97m'], g['WQ6']
    spec = g['_SPEC_CM']
    LVL = spec['level_index']
    R = {'construction': spec['construction'], 'level_index': LVL,
         'estimator': type(cm[cp.Q[0]]).__name__}

    # ---------------------------------------------------------------- LEG 1: M-52, executed
    print('=== LEG 1 — M-52: the SHIPPED knot reader against the design estimator ===')
    try:
        for _m in [cm[q] for q in cp.Q] + [q97m]:
            for _e in np.asarray(_m.estimators_).ravel():
                pass
        R['M52'] = {'raised': False,
                    'verdict': 'NOT REPRODUCED — the design estimator DOES expose estimators_. The '
                               'must-move is then NOT forced by M-52 and the retirement needs re-arguing.'}
        print('  UNEXPECTED: estimators_ is present. M-52 does not reproduce.')
    except Exception as e:
        R['M52'] = {'raised': True, 'exception': '%s: %s' % (type(e).__name__, e),
                    'shipped_expression': "for _e in np.asarray(_m.estimators_).ravel():  "
                                          "(_merged_recover.py:488, ORDER 44 _o44_xs)",
                    'verdict': 'REPRODUCED — the shipped read-site ratchet CANNOT LOAD against the design '
                               'estimator. "New estimator + ratchet retained" is not a configuration that '
                               'exists; the retirement is FORCED, not chosen.'}
        print('  %s: %s' % (type(e).__name__, e))
        print('  => the shipped ratchet cannot load. The retirement is FORCED (study B M-52).')

    # ---------------------------------------------------------------- LEG 2: the measured no-op
    print('\n=== LEG 2 — THE MEASURED NO-OP, every board row, ratchet generalised to the new estimator ===')
    knots = set()
    for m in [cm[q] for q in cp.Q] + [q97m]:
        knots |= hist_level_knots(m, LVL)
    XS = np.concatenate([[a.lo], np.array(sorted(knots), dtype=float) + a.eps, [a.hi]])
    XS = np.unique(XS[(XS >= a.lo) & (XS <= a.hi)])
    print('  generalised knot set : %d knots, range %.4f - %.4f' % (len(XS), XS[1], XS[-2]))
    R['generalised_knots'] = {'n': int(len(XS)), 'lo': float(XS[1]), 'hi': float(XS[-2]),
                              'source': '_predictors[i][j].nodes where not is_leaf and feature_idx == %d'
                                        % LVL,
                              'shipped_incumbent_knots_for_comparison': 2464}

    def rows6(F):
        P = np.sort(np.column_stack([np.asarray(cm[q].predict(F), dtype=float) for q in cp.Q]), axis=1)
        return np.column_stack([P, np.maximum(np.asarray(q97m.predict(F), dtype=float), P[:, 4])])

    board = [p for p in MA.data if MA.GRP.get(p.get('pos')) and not p.get('_retired')]
    worst = 0.0
    worst_row = None
    moved = 0
    worst_leg = 0.0
    for n, p in enumerate(board, 1):
        f = np.asarray(cp._feat(p, 2026), dtype=float)
        raw = rows6(f[None, :])[0]
        lvl = float(f[LVL])
        xs = XS[XS <= lvl]
        if xs.size == 0:
            xs = np.array([lvl], dtype=float)
        F = np.repeat(f[None, :], xs.size, axis=0)
        F[:, LVL] = xs
        rat = np.maximum.accumulate(rows6(F), axis=0)[-1]
        d = float(abs(float(rat @ WQ6) - float(raw @ WQ6)))
        dl = float(np.abs(rat - raw).max())
        if d > 0.0:
            moved += 1
        if d > worst:
            worst, worst_row = d, p['player']
        worst_leg = max(worst_leg, dl)
        if n % 200 == 0:
            print('  ... %d rows' % n, flush=True)
    R['no_op_on_candidate'] = {'board_rows': len(board), 'rows_the_ratchet_would_move': moved,
                               'max_abs_band_mean_delta': worst, 'max_abs_any_leg_delta': worst_leg,
                               'worst_row': worst_row,
                               'verdict': 'MEASURED NO-OP' if moved == 0 else 'NOT A NO-OP — FB3'}
    print('  rows the ratchet would move : %d of %d' % (moved, len(board)))
    print('  max |band-mean change|      : %.12f' % worst)
    print('  max |any-leg change|        : %.12f' % worst_leg)
    print('  VERDICT                     : %s' % R['no_op_on_candidate']['verdict'])

    # ---- the CONTROL: the same instrument on the INCUMBENT artifacts must find a LOT of work.
    print('\n=== LEG 2 CONTROL — the same instrument on the SHIPPED artifacts (non-vacuity) ===')
    import pickle
    root = os.environ['RL_REPO']
    ctl = {}
    try:
        icm = pickle.load(open(os.environ['RL_CTL_CM'], 'rb'))
        iq = pickle.load(open(os.environ['RL_CTL_Q97M'], 'rb'))
        iknots = set()
        for m in [icm[q] for q in cp.Q] + [iq]:
            for e in np.asarray(m.estimators_).ravel():
                t = e.tree_
                iknots.update(float(v) for v in t.threshold[t.feature == LVL])
        IXS = np.concatenate([[a.lo], np.array(sorted(iknots), dtype=float) + a.eps, [a.hi]])
        IXS = np.unique(IXS[(IXS >= a.lo) & (IXS <= a.hi)])

        def irows6(F):
            P = np.sort(np.column_stack([np.asarray(icm[q].predict(F), dtype=float) for q in cp.Q]), axis=1)
            return np.column_stack([P, np.maximum(np.asarray(iq.predict(F), dtype=float), P[:, 4])])

        # the incumbent's 11-feature vector: rebuild it WITHOUT the age hill, by unbinding the design
        old = cp.bind_design(None)
        imoved = 0
        iworst = 0.0
        try:
            for p in board:
                f = np.asarray(cp._feat(p, 2026), dtype=float)
                raw = irows6(f[None, :])[0]
                lvl = float(f[LVL])
                xs = IXS[IXS <= lvl]
                if xs.size == 0:
                    xs = np.array([lvl], dtype=float)
                F = np.repeat(f[None, :], xs.size, axis=0)
                F[:, LVL] = xs
                rat = np.maximum.accumulate(irows6(F), axis=0)[-1]
                d = float(abs(float(rat @ WQ6) - float(raw @ WQ6)))
                if d > 0.0:
                    imoved += 1
                iworst = max(iworst, d)
        finally:
            cp.bind_design(old)
        ctl = {'knots': int(len(IXS)), 'rows_the_ratchet_moves': imoved, 'board_rows': len(board),
               'max_abs_band_mean_delta': iworst,
               'verdict': ('INSTRUMENT PROVEN ABLE TO SEE WORK' if imoved > 0 else
                           'VACUOUS — the instrument found nothing on the SHIPPED artifacts either, so '
                           'the no-op above proves nothing')}
        print('  shipped knots               : %d' % ctl['knots'])
        print('  rows the ratchet MOVES      : %d of %d' % (imoved, len(board)))
        print('  max |band-mean change|      : %.6f' % iworst)
        print('  VERDICT                     : %s' % ctl['verdict'])
    except Exception as e:
        ctl = {'error': '%s: %s' % (type(e).__name__, e), 'trace': traceback.format_exc()[-800:]}
        print('  CONTROL NOT RUN: %s' % e)
    R['no_op_control_on_shipped_artifacts'] = ctl

    if a.json:
        json.dump(R, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0 if R['no_op_on_candidate']['rows_the_ratchet_would_move'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
