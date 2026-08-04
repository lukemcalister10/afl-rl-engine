#!/usr/bin/env python3
"""#306 L-A — THE ANCHORED CONSTRUCTION, SIMULATED ON COMMITTED ROWS.

WHAT THIS IS, AND WHAT IT IS NOT
  This is a DESIGN SIMULATION, not an engine fit and not an acceptance run.  It takes the committed
  pass-0 matrix rows and shows what the proposed construction does to the band shape, so the design
  arrives MEASURED rather than argued.  The engine's own fit will differ in detail -- it fits the lens
  from `_v0_raw` (the pre-curve model estimate), whereas this fits it from the current surface's own
  output, the best cell-level proxy the committed evidence supplies.  **The acceptance is measured on
  the ARTIFACT the engine produces, never here.**  Nothing below is a gated G-Y0 and nothing below is
  an expectation.

THE CONSTRUCTION UNDER TEST

    v0*(pos, age, pick)  =  anchor(pick)  x  m(pos, age)

  anchor(pick) -- the installed pick curve.  THE SKELETON.  `pick` enters the surface through the
    anchor and through NOTHING ELSE, so the surface cannot leave the curve's shape.  This is the
    structural difference from today's `_build_v0_curve`, which fits `_v0_raw` over log(pick) and
    never references the curve at all.

  m(pos, age)  -- THE LENS.  A function of position and draft age ONLY.  Making m independent of pick
    is the whole of "constrained by construction": today's lens drifts 0.94 -> 1.65 with pick depth,
    which is not modulation around an anchor, it is re-shaping the anchor.

  BOUNDED BY CONSTRUCTION -- m is carried as m = B**t with t in [-1, 1], so m lies in [1/B, B]
    IDENTICALLY.  The artifact cannot represent a lens outside the band; no clipping step is applied
    to a finished surface, because no out-of-band surface can be built in the first place.

  AGGREGATE-NEUTRAL BY CONSTRUCTION -- the neutrality scalar is solved INSIDE the estimator, against
    the constraint  SUM anchor*m == SUM anchor  over the fit population.  Where the bound binds, the
    BOUND WINS and neutrality is met to a stated tolerance -- which is exactly N30's wording.

    python3 anchored_construction_sim.py
"""
import json, hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
MATRIX = os.path.join(REPO, 'docs/evidence/rehearsal_290_2026-07-31/L6_convergence/pass0_matrix.json')
CURVE  = os.path.join(REPO, 'engine/rl_after/pvc_curve_v2.json')
MATRIX_MD5, CURVE_PAYLOAD = '9c4bca53b738452739c353d94fe99928', 'e69a3f38'

BANDS = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]
BOUND = 2.0          # the STATED bound, fixed at design time: m in [0.50, 2.00]
TOL   = 0.005        # the STATED aggregate tolerance: |ratio - 1| <= 0.5%
MINCELL = 25         # below this a (pos,age-group) cell pools into its position's all-age cell


def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()


def payload_md5(c):
    return hashlib.md5(json.dumps({str(k): int(round(v)) for k, v in c.items()},
                                  sort_keys=True).encode()).hexdigest()[:8]


def agegrp(a):
    if a is None: return 'na'
    a = int(a)
    return '<=17' if a <= 17 else ('18' if a == 18 else ('19-20' if a <= 20 else '21+'))


def main():
    got = md5(MATRIX)
    if got != MATRIX_MD5:
        raise SystemExit('HALT: pass0_matrix.json is %s, pinned %s.' % (got, MATRIX_MD5))
    curve = json.load(open(CURVE))['curve']
    gotp = payload_md5(curve)
    if gotp != CURVE_PAYLOAD:
        raise SystemExit('HALT: installed curve payload %s, expected %s — reconstruct the substrate.'
                         % (gotp, CURVE_PAYLOAD))
    C = {int(k): float(v) for k, v in curve.items()}
    recs = json.load(open(MATRIX))['recs']
    teach = [r for r in recs if r.get('teaches_curve') and r.get('v0') is not None
             and r.get('pick') is not None and 1 <= r['pick'] <= 64]
    for r in teach:
        r['_a'] = C[r['pick']]; r['_cell'] = (r.get('pos'), agegrp(r.get('age_draft')))

    # ---- pool thin cells into the position's all-age cell, so no cell is fitted on noise
    cnt = {}
    for r in teach: cnt[r['_cell']] = cnt.get(r['_cell'], 0) + 1
    for r in teach:
        if cnt[r['_cell']] < MINCELL: r['_cell'] = (r.get('pos'), 'ALL')

    cells = sorted({r['_cell'] for r in teach}, key=lambda c: (str(c[0]), str(c[1])))
    SA = {c: sum(r['_a'] for r in teach if r['_cell'] == c) for c in cells}
    SV = {c: sum(r['v0'] for r in teach if r['_cell'] == c) for c in cells}
    raw = {c: (SV[c] / SA[c]) for c in cells}                 # the cell's unconstrained lens

    # ---- solve the neutrality scalar INSIDE the bound. Where the bound binds, the bound wins.
    TA = sum(SA[c] for c in cells)
    s, hist = 1.0, []
    for _ in range(200):
        m = {c: min(BOUND, max(1.0 / BOUND, s * raw[c])) for c in cells}
        tot = sum(SA[c] * m[c] for c in cells)
        hist.append(tot / TA)
        if abs(tot / TA - 1.0) <= 1e-12: break
        s *= TA / tot
    m = {c: min(BOUND, max(1.0 / BOUND, s * raw[c])) for c in cells}
    achieved = sum(SA[c] * m[c] for c in cells) / TA
    bound_binds = [c for c in cells if abs(m[c] - BOUND) < 1e-9 or abs(m[c] - 1.0 / BOUND) < 1e-9]

    out = {'what': 'DESIGN SIMULATION of v0* = anchor(pick) x m(pos,age) on committed pass-0 rows',
           'NOT_AN_ACCEPTANCE_RUN': 'the engine fits m from _v0_raw; acceptance is measured on the '
                                    'artifact, never here. Nothing here is a gated G-Y0.',
           'POPULATION_WARNING': 'FIT population (teaches_curve, picks 1-64) — NOT the gate\'s set.',
           'design_constants': {'bound_B': BOUND, 'm_range': [1.0 / BOUND, BOUND],
                                'aggregate_tolerance': TOL, 'min_cell': MINCELL},
           'anchor_curve_payload': gotp, 'matrix_md5': got, 'rows': len(teach), 'cells': len(cells),
           'neutrality': {'achieved_ratio': round(achieved, 8),
                          'within_tolerance': abs(achieved - 1.0) <= TOL,
                          'cells_where_bound_binds': [list(c) for c in bound_binds]}}

    # ---- BOTH DIRECTIONS: every band, before and after. L-A requirement 3.
    rows = []
    for lo, hi in BANDS:
        b = [r for r in teach if lo <= r['pick'] <= hi]
        sa = sum(r['_a'] for r in b)
        before = sum(r['v0'] for r in b) / sa
        after = sum(r['_a'] * m[r['_cell']] for r in b) / sa
        rows.append({'band': '%d-%d' % (lo, hi), 'rows': len(b),
                     'before_ratio': round(before, 6), 'before_gap_pct': round(100 * (before - 1), 3),
                     'after_ratio': round(after, 6), 'after_gap_pct': round(100 * (after - 1), 3),
                     'move_pp': round(100 * (after - before), 3)})
    out['by_band'] = rows
    out['lens'] = {'%s|%s' % (c[0], c[1]): {'rows': cnt.get(c, sum(1 for r in teach if r['_cell'] == c)),
                                            'raw': round(raw[c], 4), 'm': round(m[c], 4)} for c in cells}

    # ---- the pool's structural coherence under the construction (SHAPE only; the LEVEL is #207's)
    pool = [r for r in recs if r.get('is_pool') and r.get('v0') is not None]
    if pool:
        anchor65 = C[64] * (C[64] / C[63]) if 63 in C else C[64]
        worst = BOUND * anchor65
        out['pool_coherence_by_construction'] = {
            'n': len(pool), 'curve_64': C[64], 'implied_anchor_65': round(anchor65, 2),
            'worst_case_pool_value_at_bound_B': round(worst, 2),
            'holds_below_curve64_for_all_m': worst <= C[64],
            'max_B_that_would_guarantee_it': round(C[64] / anchor65, 4),
            'today_mean_pool_v0': round(sum(r['v0'] for r in pool) / len(pool), 2),
            'reading': 'With the pool anchored at index 65 and the curve strictly decreasing, the pool '
                       'sits below the last national band FOR EVERY lens value iff B <= curve[64]/anchor(65). '
                       'That is a provable property of the construction, not a check applied afterwards. '
                       'The pool LEVEL stays out of scope (ITEM 412 / #207) — this constrains coherence only.'}

    # ---- L-A requirement 4: the bust inversion, CHECKED under the construction (never depended on).
    # Under v0* = anchor(pick) x m(pos,age), two pool entrants in the SAME cell take the SAME value
    # whatever their games played -- so a WITHIN-CELL inversion is structurally impossible. It can only
    # survive ACROSS cells, if never-played entrants concentrate in high-m cells. That is measurable.
    if pool:
        for r in pool:
            r['_cell'] = (r.get('pos'), agegrp(r.get('age_draft')))
            if r['_cell'] not in m: r['_cell'] = (r.get('pos'), 'ALL')
        mat = [r for r in pool if (r.get('age_draft') or 0) >= 19] or pool
        nev = [r for r in mat if not (r.get('games_total') or 0)]
        pld = [r for r in mat if (r.get('games_total') or 0) > 0]
        if nev and pld:
            def mean(x): return sum(x) / len(x)
            lens_only_n = mean([m.get(r['_cell'], 1.0) for r in nev])
            lens_only_p = mean([m.get(r['_cell'], 1.0) for r in pld])
            out['bust_inversion_under_construction'] = {
                'today': {'never_played_mean_v0': round(mean([r['v0'] for r in nev]), 1), 'n_never': len(nev),
                          'played_mean_v0': round(mean([r['v0'] for r in pld]), 1), 'n_played': len(pld),
                          'inverted': mean([r['v0'] for r in nev]) > mean([r['v0'] for r in pld])},
                'under_construction_lens_only': {
                    'never_played_mean_m': round(lens_only_n, 4),
                    'played_mean_m': round(lens_only_p, 4),
                    'residual_inversion_ratio': round(lens_only_n / lens_only_p, 4),
                    'inverted': lens_only_n > lens_only_p},
                'reading': 'Within a cell the inversion is structurally impossible under this construction '
                           '(same anchor, same lens, games played is not an input). What remains is the '
                           'across-cell residual shown here — the construction is CHECKED against it and '
                           'does not DEPEND on it.'}

    with open(os.path.join(HERE, 'anchored_construction_sim.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print(out['NOT_AN_ACCEPTANCE_RUN'] + '\n')
    print('construction   v0* = anchor(pick) x m(pos,age)      B = %.2f  ->  m in [%.2f, %.2f]   tol %.1f%%'
          % (BOUND, 1 / BOUND, BOUND, 100 * TOL))
    print('cells %d (min %d rows, thin cells pooled to position)   teaching rows %d\n' % (len(cells), MINCELL, len(teach)))
    print('BOTH DIRECTIONS      rows      BEFORE          AFTER          move')
    for r in rows:
        print('  %-8s %9d   %+8.2f%%      %+8.2f%%     %+8.2f pp'
              % (r['band'], r['rows'], r['before_gap_pct'], r['after_gap_pct'], r['move_pp']))
    n = out['neutrality']
    print('\nAGGREGATE NEUTRALITY  achieved %.8f   |1-ratio| = %.2e   within %.1f%% tolerance: %s'
          % (n['achieved_ratio'], abs(n['achieved_ratio'] - 1), 100 * TOL, n['within_tolerance']))
    print('  cells where the bound binds: %s' % (n['cells_where_bound_binds'] or 'none'))
    print('\nTHE LENS (raw -> bounded, neutralised)')
    for k, v in sorted(out['lens'].items()):
        flag = '  <- bound binds' if abs(v['m'] - BOUND) < 1e-9 or abs(v['m'] - 1 / BOUND) < 1e-9 else ''
        print('  %-12s raw %6.3f   m %6.3f%s' % (k, v['raw'], v['m'], flag))
    if 'pool_coherence_by_construction' in out:
        p = out['pool_coherence_by_construction']
        print('\nPOOL COHERENCE BY CONSTRUCTION')
        print('  curve[64] %.0f | implied anchor(65) %.2f | worst case at B=%.2f -> %.2f'
              % (p['curve_64'], p['implied_anchor_65'], BOUND, p['worst_case_pool_value_at_bound_B']))
        print('  holds for EVERY lens value at B=%.2f: %s   (guaranteed iff B <= %.4f)'
              % (BOUND, p['holds_below_curve64_for_all_m'], p['max_B_that_would_guarantee_it']))
        print('  today the pool mean is %.2f against curve[64] %.0f' % (p['today_mean_pool_v0'], p['curve_64']))
    if 'bust_inversion_under_construction' in out:
        b = out['bust_inversion_under_construction']
        print('\nBUST INVERSION (L-A requirement 4)')
        print('  today            never-played %.1f (n=%d)  vs  played %.1f (n=%d)   inverted: %s'
              % (b['today']['never_played_mean_v0'], b['today']['n_never'],
                 b['today']['played_mean_v0'], b['today']['n_played'], b['today']['inverted']))
        u = b['under_construction_lens_only']
        print('  under construction  mean lens m  never %.4f  vs  played %.4f   ratio %.4f   inverted: %s'
              % (u['never_played_mean_m'], u['played_mean_m'], u['residual_inversion_ratio'], u['inverted']))
        print('  within-cell inversion is structurally impossible (games played is not an input)')
    print('\nwrote anchored_construction_sim.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
