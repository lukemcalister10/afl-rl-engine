#!/usr/bin/env python3
"""#306 L-A — THE ACCEPTANCE, MEASURED ON THE ARTIFACT.  (N30 / Acceptance 7.)

THIS IS NOT THE DESIGN SIMULATION.  `anchored_construction_sim.py` modelled the construction on
committed matrix rows.  THIS loads the engine on the board path, reads the FROZEN SURFACE ARTIFACT the
refit actually produced, and measures N30's two limbs on the values `v0_start` actually returns.

  limb 1  AGGREGATE-NEUTRAL against the anchor to a stated tolerance   (|SUM v0 / SUM anchor - 1| <= tol)
  limb 2  NO BAND EXCEEDS ITS STATED BOUND                             (every band ratio within [1/B, B])

Both limbs are BORN FAILING on the pre-#306 artifact and that is their non-vacuity proof -- so this
runs BOTH lanes in one act and reports them side by side:

  BEFORE  RL_V0_ANCHORED=0  -- the pre-#306 free fit, the declared A/B control
  AFTER   RL_V0_ANCHORED=1  -- the anchored construction (default)

Run from the workspace rl_after with RL_REPO set, behind the preboot assert, on a box whose N35
fit-path assert has passed.  Each lane runs in its OWN fresh process (the engine builds the surface at
import and caches it), so the two are not contaminated by each other.

    python3 la_acceptance.py            # driver: spawns both lanes, writes la_acceptance.json
    python3 la_acceptance.py --lane 0|1 # one lane, prints JSON to stdout (used by the driver)

POPULATION: the FIT population -- `teaches_curve`-equivalent rows, i.e. the engine's own `real` set
(type ND, not pool, picks 1-64).  NOT the G-Y0 gate's ~1,326-row set; the gate prints its own figure.
Nothing here is a gated G-Y0 and nothing here is a predicted one (Acceptance 4).
"""
import json, os, subprocess, sys

BANDS = [(1, 10), (11, 20), (21, 30), (31, 45), (46, 64)]


def run_lane(anchored):
    os.environ['RL_V0_ANCHORED'] = '1' if anchored else '0'
    os.environ['RL_V0SURF_REFIT'] = '1'          # DECLARED refit: fit here, never load a stale freeze
    import io, contextlib
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, v0_start, META = g['MA'], g['v0_start'], g['_V0CURVE_META']
    _isreal, _ageR = g['_isreal'], g['_ageR']
    PVC = g['_PVC0'] if '_PVC0' in g else MA.PVC
    A = {int(k): float(v) for k, v in PVC.items()}

    real = [p for p in MA.data if _isreal(p) and p.get('type') == 'ND'
            and p.get('pick') is not None and not MA.is_pool(p)
            and 1 <= int(p.get('pick')) <= 64]
    rows = [(int(p.get('pick')), MA.gfut(p), _ageR(p), float(v0_start(p))) for p in real]

    sv = sum(v for _, _, _, v in rows); sa = sum(A[pk] for pk, _, _, _ in rows)
    out = {'lane': 'anchored' if anchored else 'free_fit_pre_306',
           'v0surf_sig': META.get('_v0surf_sig', '')[:12],
           'rows': len(rows), 'aggregate_ratio': sv / sa,
           'aggregate_gap_pct': 100 * (sv / sa - 1), 'by_band': {}}
    for lo, hi in BANDS:
        b = [r for r in rows if lo <= r[0] <= hi]
        bv = sum(v for _, _, _, v in b); ba = sum(A[pk] for pk, _, _, _ in b)
        out['by_band']['%d-%d' % (lo, hi)] = {'rows': len(b), 'ratio': bv / ba,
                                              'gap_pct': 100 * (bv / ba - 1)}
    if '_la' in META:
        la = META['_la']
        out['la'] = {'B': la['B'], 'tol': la['tol'], 'mincell': la['mincell'],
                     'neutrality_solved': la['neutrality'], 'lens': la['lens'],
                     'rows_per_cell': la['rows'], 'bound_binds': la['bound_binds']}
    return out


def main():
    if '--lane' in sys.argv:
        print(json.dumps(run_lane(sys.argv[sys.argv.index('--lane') + 1] == '1')))
        return 0

    here = os.path.dirname(os.path.abspath(__file__))
    res = {}
    for lane, name in ((0, 'before'), (1, 'after')):
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', str(lane)],
                           capture_output=True, text=True, cwd=os.getcwd())
        if p.returncode != 0:
            raise SystemExit('HALT: lane %d failed.\n%s' % (lane, p.stderr[-3000:]))
        res[name] = json.loads(p.stdout.strip().splitlines()[-1])

    B = res['after'].get('la', {}).get('B', 2.0)
    tol = res['after'].get('la', {}).get('tol', 0.005)
    verdict = {}
    for name in ('before', 'after'):
        r = res[name]
        l1 = abs(r['aggregate_ratio'] - 1.0) <= tol
        worst = max(abs(v['ratio'] - 1.0) for v in r['by_band'].values())
        l2 = all((1.0 / B) <= v['ratio'] <= B for v in r['by_band'].values())
        verdict[name] = {'limb1_aggregate_neutral': l1, 'limb2_bands_within_bound': l2,
                         'ACCEPTANCE_7': l1 and l2, 'worst_band_deviation': worst}
    out = {'what': 'N30 / Acceptance 7 measured ON THE ARTIFACT, both lanes, fresh process each',
           'POPULATION': 'FIT population (engine `real` set, type ND, not pool, picks 1-64). '
                         'NOT the G-Y0 gate population. Nothing here is a gated or predicted G-Y0.',
           'constants': {'B': B, 'tolerance': tol}, 'lanes': res, 'verdict': verdict}
    with open(os.path.join(here, 'la_acceptance.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')

    print(out['POPULATION'] + '\n')
    print('%-10s %10s   %s' % ('band', 'BEFORE', 'AFTER'))
    for k in ('1-10', '11-20', '21-30', '31-45', '46-64'):
        print('  %-8s %+9.3f%%   %+9.3f%%' % (k, res['before']['by_band'][k]['gap_pct'],
                                              res['after']['by_band'][k]['gap_pct']))
    print('  %-8s %+9.4f%%   %+9.4f%%   <- aggregate, N30 limb 1'
          % ('TOTAL', res['before']['aggregate_gap_pct'], res['after']['aggregate_gap_pct']))
    print('\nrows %d / %d   sig before %s  after %s'
          % (res['before']['rows'], res['after']['rows'],
             res['before']['v0surf_sig'], res['after']['v0surf_sig']))
    print('\nACCEPTANCE 7 (B=%.2f, tol=%.1f%%)' % (B, 100 * tol))
    for name in ('before', 'after'):
        v = verdict[name]
        print('  %-7s limb1 aggregate-neutral %-5s   limb2 bands-in-bound %-5s   ACCEPTANCE %s'
              % (name.upper(), v['limb1_aggregate_neutral'], v['limb2_bands_within_bound'],
                 'PASS' if v['ACCEPTANCE_7'] else 'FAIL'))
    if 'la' in res['after']:
        la = res['after']['la']
        print('\nTHE LENS AS BUILT   neutrality solved to %.12f' % la['neutrality_solved'])
        for k in sorted(la['lens']):
            flag = '  <- bound binds' if k in la['bound_binds'] else ''
            print('  %-14s m %6.4f   rows %4d%s' % (k, la['lens'][k], la['rows_per_cell'].get(k, 0), flag))
    print('\nwrote la_acceptance.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
