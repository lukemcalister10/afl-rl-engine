#!/usr/bin/env python3
"""ARM 1 — V3, THE FULL-POPULATION LEVEL-AXIS CENSUS, at the READ SITE.

WHAT IS COUNTED
  For EVERY row on the board (not three archetypes — that is how a 23%-of-steps defect stayed invisible
  for five weeks), the level feature (index 9 in both cp._feat and _feat_infer) is swept across a
  DECLARED grid spanning the model's own level range, and the six-leg band's price6 weighted mean
  (WQ6 = [0.18]*5 + [0.10], normalised — the engine's own weights) is checked for DESCENDING steps.

TWO CENSUSES FROM ONE SWEEP, because reporting only the first would be dishonest:
  RAW        the band straight off the forests — sort of the five quantile predictions, then
             max(q97m, b[4]) — i.e. _o44_rows6, the engine's own expression. This is what the FIT
             delivers. The ratchet is not applied.
  READ SITE  the same surface under ORDER 44 VARIANT A, the shipped read-site ratchet
             (RL_O44_LVLMONO='ratchet', code default, absent from the manifest so gate mode leaves it
             standing): the componentwise running maximum over every piece of the step surface at or
             below the row's level. This is what a PLAYER is actually priced from, and it is the census
             the directive requires at ZERO.
  The read-site figure is zero BY CONSTRUCTION (a running maximum over a nested family is
  non-decreasing). Measuring it is still the point: it proves the construction survives the real fit
  and the real feature rows, and it is the standing falsifier if it ever does not.

LIMITATION, STATED IN THE SAME BREATH (study B I-18 / packet F2's open half): this census is measured
at the BAND, not through the true ev(). Band monotonicity is necessary for law 3, not sufficient — the
engine composes the band with the pole, the ISO correction, the taper and the projection lens before a
player has a price. The ev() sweep remains OWED.

Usage: run from the engine workspace with the candidate root bound.
       python3 level_census_v3.py [--step 0.25] [--lo 40] [--hi 120] [--json OUT]
"""
import argparse, contextlib, io, json, os, sys
import numpy as np


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument('--step', type=float, default=0.25)
    ap.add_argument('--lo', type=float, default=40.0)
    ap.add_argument('--hi', type=float, default=120.0)
    ap.add_argument('--json')
    a = ap.parse_args(argv[1:])

    sys.path.insert(0, os.environ['RL_REPO'])
    import config_manifest
    config_manifest.enforce('gate')

    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, cp = g['MA'], g['cp']
    rows6, WQ6 = g['_o44_rows6'], g['WQ6']
    LVL = g['_O44_LVL']
    XS = g['_o44_xs']()
    print('ORDER 44 dial          : %r  (read-site ratchet)' % g['_O44_RAW'])
    print('level feature index    : %d' % LVL)
    print("model's own knot set   : %d knots, range %.4f - %.4f"
          % (len(XS), XS[1], XS[-2]))          # [0] and [-1] are the declared window edges
    grid = np.arange(a.lo, a.hi + 1e-9, a.step)
    print('DECLARED GRID          : %.1f -> %.1f step %.2f  (%d points/row)'
          % (a.lo, a.hi, a.step, len(grid)))

    players = [p for p in MA.data if MA.GRP.get(p.get('pos'))]
    board = [p for p in players if not p.get('_retired')]
    print('board rows             : %d  (of %d mapped store rows)' % (len(board), len(players)))

    raw_steps = raw_neg = 0
    ratchet_steps = ratchet_neg = 0
    raw_worst = 0.0
    ratchet_worst = 0.0
    raw_rows_with_drop = 0
    ratchet_rows_with_drop = 0
    worst_row = None
    n = 0
    for p in board:
        f = np.asarray(cp._feat(p, 2026), dtype=float)
        F = np.repeat(f[None, :], len(grid), axis=0)
        F[:, LVL] = grid
        B = rows6(F)                                 # (len(grid), 6) — the engine's own band expression
        w_raw = B @ WQ6
        w_rat = (np.maximum.accumulate(B, axis=0)) @ WQ6
        for w, tag in ((w_raw, 'raw'), (w_rat, 'rat')):
            d = np.diff(w)
            neg = int((d < 0).sum())
            if tag == 'raw':
                raw_steps += len(d); raw_neg += neg
                if neg:
                    raw_rows_with_drop += 1
                mn = float(d.min()) if len(d) else 0.0
                base = float(np.abs(w).max()) or 1.0
                if mn / base * 100.0 < raw_worst:
                    raw_worst = mn / base * 100.0
                    worst_row = p['player']
            else:
                ratchet_steps += len(d); ratchet_neg += neg
                if neg:
                    ratchet_rows_with_drop += 1
                mn = float(d.min()) if len(d) else 0.0
                base = float(np.abs(w).max()) or 1.0
                ratchet_worst = min(ratchet_worst, mn / base * 100.0)
        n += 1
        if n % 200 == 0:
            print('  ... %d rows' % n, flush=True)

    res = {
        'grid': {'lo': a.lo, 'hi': a.hi, 'step': a.step, 'points_per_row': len(grid)},
        'knots_in_model': int(len(XS)), 'board_rows': len(board),
        'raw': {'steps': raw_steps, 'negative': raw_neg,
                'pct_negative': 100.0 * raw_neg / raw_steps if raw_steps else 0.0,
                'rows_with_a_drop': raw_rows_with_drop,
                'pct_rows_with_a_drop': 100.0 * raw_rows_with_drop / len(board),
                'worst_step_pct': raw_worst, 'worst_row': worst_row},
        'read_site_ratchet': {'steps': ratchet_steps, 'negative': ratchet_neg,
                              'pct_negative': 100.0 * ratchet_neg / ratchet_steps if ratchet_steps else 0.0,
                              'rows_with_a_drop': ratchet_rows_with_drop,
                              'worst_step_pct': ratchet_worst},
    }
    print('\n================ V3 LEVEL CENSUS — CANDIDATE ================')
    print('RAW BAND (what the fit delivers, ratchet NOT applied)')
    print('  steps                : %d' % raw_steps)
    print('  descending steps     : %d  (%.4f%%)' % (raw_neg, res['raw']['pct_negative']))
    print('  rows with a drop     : %d of %d (%.2f%%)'
          % (raw_rows_with_drop, len(board), res['raw']['pct_rows_with_a_drop']))
    print('  worst step           : %.4f%% of the row\'s band mean  (%s)' % (raw_worst, worst_row))
    print('READ SITE (ORDER 44 ratchet ON — what a player is priced from)')
    print('  steps                : %d' % ratchet_steps)
    print('  descending steps     : %d  (%.6f%%)   <== the directive\'s ZERO'
          % (ratchet_neg, res['read_site_ratchet']['pct_negative']))
    print('  rows with a drop     : %d' % ratchet_rows_with_drop)
    print('  worst step           : %.6f%%' % ratchet_worst)
    print('VERDICT                : %s' % ('PASS — zero descending steps at the read site, over every '
                                           'board row' if ratchet_neg == 0 else
                                           'FAIL — falsifier FA6 fired'))
    if a.json:
        json.dump(res, open(a.json, 'w'), indent=1, sort_keys=True)
    return 0 if ratchet_neg == 0 else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
