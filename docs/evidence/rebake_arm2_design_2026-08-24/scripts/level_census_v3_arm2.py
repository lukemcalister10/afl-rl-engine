#!/usr/bin/env python3
"""ARM 2 — V3, THE FULL-POPULATION LEVEL-AXIS CENSUS, AT RAW. Plus V4, the age-shape census.

WHY THIS SCRIPT IS DIFFERENT FROM ARM 1'S, AND WHY THAT DIFFERENCE IS THE WHOLE ARM
  ARM 1's census read the same surface twice: RAW (the band straight off the forests) and READ SITE (the
  same surface under ORDER 44's running maximum). It had to, because the two numbers were 25.49% and 0 —
  the fit was violating law 3 on a quarter of all steps and a read-site operator was hiding it.
  ARM 2 retires that operator. There is no second surface any more: RAW *is* the read site. The number
  the directive requires at ZERO is therefore a number about THE FIT, and it cannot be produced by an
  operator applied afterwards. This script measures it, and it measures it on every board row.

  Both censuses are still PRINTED, with the read-site figure derived the only way it now can be — from
  the same rows — so the pair is unambiguous and nobody reads a zero that came from a ratchet.

THE BAND EXPRESSION IS THE ENGINE'S OWN, not a re-implementation: sort of the five quantile predictions,
then max(q97m, b[4]) — what _b6_core emits now that ORDER 44's dispatch is gone.

V4 — THE AGE-SHAPE CENSUS (study B section 4.2, gate V4). With the age hill bound, sweep age across a
declared grid on every board row and count rows whose band mean is SINGLE-PEAKED (rises then falls, with
monotone in either direction as the degenerate cases). The construction claims 100% BY CONSTRUCTION; a
census that measured 99.8% would mean the claim is false, so this is a real falsifier and not a lap of
honour. Study B measured 7.0% single-peaked WITHOUT the reparameterisation on the same kind of sample.

LIMITATION, STATED IN THE SAME BREATH (study B I-18 / packet F2's open half, carried from ARM 1 unchanged
because ARM 2 does not close it either): this census is measured at the BAND, not through the true ev().
Band monotonicity is necessary for law 3, not sufficient — the engine composes the band with the pole, the
ISO correction, the taper and the projection lens before a player has a price. The ev() sweep is STILL OWED.

Usage: run from the engine workspace with the candidate root bound.
"""
import argparse, contextlib, io, json, os, sys

import numpy as np


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--step', type=float, default=0.25)
    ap.add_argument('--lo', type=float, default=40.0)
    ap.add_argument('--hi', type=float, default=120.0)
    ap.add_argument('--age-lo', type=float, default=18.0)
    ap.add_argument('--age-hi', type=float, default=34.0)
    ap.add_argument('--age-step', type=float, default=0.5)
    ap.add_argument('--full-design', action='store_true',
                    help='ALSO census every TRAINING row (study B M-54 replication), not just the board')
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])

    sys.path.insert(0, os.environ['RL_REPO'])
    import config_manifest
    config_manifest.enforce('gate')

    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, cp, cm, q97m = g['MA'], g['cp'], g['cm'], g['q97m']
    WQ6 = g['WQ6']
    EM = g['_EM']
    spec = g['_SPEC_CM']
    LVL = spec['level_index'] if spec else EM.LVL

    def rows6(F):
        """The engine's own band expression, verbatim (_b6_core, ORDER 44 retired)."""
        P = np.sort(np.column_stack([np.asarray(cm[q].predict(F), dtype=float) for q in cp.Q]), axis=1)
        return np.column_stack([P, np.maximum(np.asarray(q97m.predict(F), dtype=float), P[:, 4])])

    print('construction           : %s' % (spec['construction'] if spec else 'INCUMBENT (no design spec)'))
    print('estimator              : %s' % type(cm[cp.Q[0]]).__name__)
    print('monotonic_cst          : %r' % (spec['monotonic_cst'] if spec else None))
    print('level feature index    : %d   (features %d)'
          % (LVL, spec['n_features'] if spec else cm[cp.Q[0]].n_features_in_))
    print('read-site ratchet      : RETIRED — RAW is the read site')
    grid = np.arange(a.lo, a.hi + 1e-9, a.step)
    print('DECLARED GRID          : %.1f -> %.1f step %.2f  (%d points/row)'
          % (a.lo, a.hi, a.step, len(grid)))

    players = [p for p in MA.data if MA.GRP.get(p.get('pos'))]
    board = [p for p in players if not p.get('_retired')]
    print('board rows             : %d  (of %d mapped store rows)' % (len(board), len(players)))

    steps = neg = rows_with_drop = 0
    worst = 0.0
    worst_row = None
    for n, p in enumerate(board, 1):
        f = np.asarray(cp._feat(p, 2026), dtype=float)
        F = np.repeat(f[None, :], len(grid), axis=0)
        F[:, LVL] = grid
        w = rows6(F) @ WQ6
        d = np.diff(w)
        k = int((d < -1e-12).sum())
        steps += len(d)
        neg += k
        if k:
            rows_with_drop += 1
        base = float(np.abs(w).max()) or 1.0
        mn = float(d.min()) if len(d) else 0.0
        if mn / base * 100.0 < worst:
            worst = mn / base * 100.0
            worst_row = p['player']
        if n % 200 == 0:
            print('  ... %d rows' % n, flush=True)

    res = {'grid': {'lo': a.lo, 'hi': a.hi, 'step': a.step, 'points_per_row': len(grid)},
           'board_rows': len(board), 'construction': spec,
           'raw': {'steps': steps, 'negative': neg,
                   'pct_negative': 100.0 * neg / steps if steps else 0.0,
                   'rows_with_a_drop': rows_with_drop, 'worst_step_pct': worst, 'worst_row': worst_row},
           'read_site': {'note': 'IDENTICAL to raw — the ORDER 44 ratchet is retired; there is no second '
                                 'surface. The zero below is a property of the FIT.',
                         'steps': steps, 'negative': neg,
                         'pct_negative': 100.0 * neg / steps if steps else 0.0}}

    print('\n================ V3 LEVEL CENSUS — ARM 2 CANDIDATE ================')
    print('RAW BAND — straight off the forests, no read-site operator anywhere')
    print('  steps                : %d' % steps)
    print('  descending steps     : %d  (%.6f%%)   <== the directive\'s ZERO, AT RAW' % (neg, res['raw']['pct_negative']))
    print('  rows with a drop     : %d of %d' % (rows_with_drop, len(board)))
    print('  worst step           : %.6f%% of the row\'s band mean  (%s)' % (worst, worst_row))
    print('READ SITE              : the same number — the ratchet is gone (%d)' % neg)
    print('VERDICT                : %s' % ('PASS — zero descending steps AT RAW, over every board row'
                                           if neg == 0 else 'FAIL — prereg falsifier FB1 has FIRED'))

    # ---------------------------------------------------------------- V4, the age-shape census
    if spec and spec.get('age_hill'):
        a_star = spec['age_hill']['a_star']
        ui, vi = spec['age_hill']['u_index'], spec['age_hill']['v_index']
        ages = np.arange(a.age_lo, a.age_hi + 1e-9, a.age_step)
        single = 0
        curves = []
        for p in board:
            f = np.asarray(cp._feat(p, 2026), dtype=float)
            F = np.repeat(f[None, :], ages.size, axis=0)
            F[:, ui] = np.maximum(0.0, a_star - ages)
            F[:, vi] = np.maximum(0.0, ages - a_star)
            c = rows6(F) @ WQ6
            curves.append(c)
            d = np.diff(c)
            up = np.where(d > 1e-12)[0]
            dn = np.where(d < -1e-12)[0]
            if len(up) == 0 or len(dn) == 0 or up.max() < dn.min():
                single += 1
        C = np.array(curves)
        mean_curve = C.mean(0)
        res['V4_age_shape'] = {
            'a_star': a_star,
            'grid': {'lo': a.age_lo, 'hi': a.age_hi, 'step': a.age_step, 'points': int(ages.size)},
            'rows': len(board), 'rows_single_peaked_or_monotone': single,
            'pct_single_peaked': round(100.0 * single / len(board), 4),
            'mean_curve_argmax_age': float(ages[int(np.argmax(mean_curve))]),
            'mean_curve': {('%.1f' % ages[i]): round(float(mean_curve[i]), 3)
                           for i in range(0, ages.size, max(1, int(round(2.0 / a.age_step))))},
            'verdict': 'PASS' if single == len(board) else 'FAIL',
        }
        print('\n================ V4 AGE-SHAPE CENSUS ================')
        print('  a*                   : %.1f  (SELECTED out of sample on the declared grid)' % a_star)
        print('  age grid             : %.1f -> %.1f step %.2f' % (a.age_lo, a.age_hi, a.age_step))
        print('  single-peaked rows   : %d of %d  (%.4f%%)' % (single, len(board),
                                                               res['V4_age_shape']['pct_single_peaked']))
        print('  mean curve peaks at  : age %.1f' % res['V4_age_shape']['mean_curve_argmax_age'])
        print('  mean curve           : %s' % res['V4_age_shape']['mean_curve'])
        print('  VERDICT              : %s' % res['V4_age_shape']['verdict'])

    # ------------------------------------------- the full-design census (study B M-54 replication)
    if a.full_design:
        print('\n================ V3 ON EVERY TRAINING ROW (study B M-54 replication) ================')
        fo = cp.first_observable_season()
        g2 = np.arange(a.lo, a.hi + 1e-9, 1.0)
        tsteps = tneg = tworst_rows = 0
        tworst = 0.0
        nrow = 0
        for p in [q for q in MA.data if MA.GRP.get(q['pos'])]:
            if cp.debutyr(p) > 2021 or not (p.get('pick') or p.get('_ft')):
                continue
            d0 = cp.debutyr(p) - 1
            last = max([x['year'] for x in p['scoring']] + [d0])
            for Y in range(d0, min(last, 2026) + 1):
                if fo is not None and d0 < Y < fo:
                    continue
                f = np.asarray(cp._feat(p, Y), dtype=float)
                F = np.repeat(f[None, :], g2.size, axis=0)
                F[:, LVL] = g2
                d = np.diff(rows6(F) @ WQ6)
                k = int((d < -1e-12).sum())
                tsteps += len(d); tneg += k; nrow += 1
                if k:
                    tworst_rows += 1
                    tworst = min(tworst, float(d.min()))
                if nrow % 2000 == 0:
                    print('  ... %d design rows' % nrow, flush=True)
        res['full_design_census'] = {'rows': nrow, 'steps': tsteps, 'negative': tneg,
                                     'rows_violating': tworst_rows, 'worst_step': tworst,
                                     'grid_step': 1.0}
        print('  %d rows · %d steps · %d negative steps · worst step %.9f'
              % (nrow, tsteps, tneg, tworst))
        print('  (study B M-54, for comparison: 13,220 rows · 1,004,720 steps · 0 negative · worst 0.000000)')

    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, sort_keys=True, default=str)
    return 0 if neg == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
