#!/usr/bin/env python3
"""#306 L-A — ACCEPTANCE ON THE ARTIFACT, PER-PICK AND BAND-FREE.  (Approval clause 2.)

Loads the engine on the board path in a FRESH PROCESS per lane, reads the values `v0_start` actually
returns, and measures the acceptance AT EVERY PICK.  No bands anywhere -- the presentation law binds
this file as it binds the model.

  LIMB 1  LOCAL NEUTRALITY AT EVERY PICK: the kernel-weighted ratio SUM w*v0 / SUM w*anchor sits
          within tolerance of 1.0 at each of the 64 picks -- totals preserved in the neighbourhood,
          never by inflating the class.
  LIMB 2  BOUNDS HELD: no realised per-pick position line leaves [1/B, B].

  BEFORE  RL_V0_LENS=0 -- the pre-#306 free fit, the declared A/B control (born failing).
  AFTER   RL_V0_LENS=1 -- the anchored lens field.

  The basis's inherited completion optimism is printed with every result and travels in the JSON.

    python3 la_acceptance_perpick.py            # driver
    python3 la_acceptance_perpick.py --lane 0|1 # one lane
"""
import json, math, os, subprocess, sys

HP, TOLQ = 0.35, 0.005
PICKS = list(range(1, 65))


def lane(anchored):
    os.environ['RL_V0_LENS'] = '1' if anchored else '0'
    os.environ['RL_V0SURF_REFIT'] = '1'
    import io, contextlib
    g = {}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA, v0s, META = g['MA'], g['v0_start'], g['_V0CURVE_META']
    _isreal, _ageR = g['_isreal'], g['_ageR']
    PVC = g['_PVC0'] if '_PVC0' in g else MA.PVC
    A = {int(k): float(v) for k, v in PVC.items()}
    rows = [(int(p.get('pick')), MA.gfut(p), _ageR(p), float(v0s(p)))
            for p in MA.data if _isreal(p) and p.get('type') == 'ND' and p.get('pick') is not None
            and not MA.is_pool(p) and 1 <= int(p.get('pick')) <= 64]
    POS = sorted({r[1] for r in rows})
    per, lines = {}, {p: {} for p in POS}
    for pk in PICKS:
        lp = math.log(pk); n = d = 0.0
        pn = {p: [0.0, 0.0] for p in POS}
        for (q, po, ag, v) in rows:
            w = math.exp(-0.5 * ((math.log(q) - lp) / HP) ** 2)
            if w < 1e-12: continue
            n += w * v; d += w * A[q]
            pn[po][0] += w * v; pn[po][1] += w * A[q]
        per[pk] = (n / d) if d > 0 else None
        for p in POS:
            lines[p][pk] = (pn[p][0] / pn[p][1]) if pn[p][1] > 0 else None
    return {'lane': 'anchored_lens' if anchored else 'free_fit_pre_306',
            'sig': META.get('_v0surf_sig', '')[:12], 'rows': len(rows), 'positions': POS,
            'neutrality_per_pick': per, 'lines_per_pick': lines,
            'basis': META.get('_lens_basis'), 'la': META.get('_la')}


def main():
    if '--lane' in sys.argv:
        print(json.dumps(lane(sys.argv[sys.argv.index('--lane') + 1] == '1'))); return 0
    here = os.path.dirname(os.path.abspath(__file__)); res = {}
    for i, nm in ((0, 'before'), (1, 'after')):
        p = subprocess.run([sys.executable, os.path.abspath(__file__), '--lane', str(i)],
                           capture_output=True, text=True, cwd=os.getcwd())
        if p.returncode != 0:
            raise SystemExit('HALT lane %d:\n%s' % (i, p.stderr[-3000:]))
        res[nm] = json.loads(p.stdout.strip().splitlines()[-1])
    B = (res['after'].get('la') or {}).get('B', 2.0)
    v = {}
    for nm in ('before', 'after'):
        r = res[nm]
        nv = [x for x in r['neutrality_per_pick'].values() if x is not None]
        worst = max(abs(x - 1) for x in nv)
        off = [pk for pk, x in r['neutrality_per_pick'].items() if x is not None and abs(x - 1) > TOLQ]
        oob = [(p, pk) for p in r['positions'] for pk, x in r['lines_per_pick'][p].items()
               if x is not None and not (1.0 / B <= x <= B)]
        v[nm] = {'limb1_local_neutrality_every_pick': not off, 'worst_deviation': worst,
                 'picks_out_of_tolerance': off[:20], 'n_picks_out': len(off),
                 'limb2_bounds_held': not oob, 'n_lines_out_of_bound': len(oob),
                 'ACCEPTANCE': (not off) and (not oob)}
    out = {'what': 'L-A acceptance ON THE ARTIFACT, per-pick, band-free (approval clause 2)',
           'PRESENTATION': 'per-pick only; no bands in this file or in the model',
           'OPTIMISM_CARRIED': (res['after'].get('basis') or {}).get('OPTIMISM'),
           'tolerance': TOLQ, 'B': B, 'lanes': res, 'verdict': v}
    with open(os.path.join(here, 'la_acceptance_perpick.json'), 'w') as f:
        json.dump(out, f, indent=1, sort_keys=True); f.write('\n')
    print('OPTIMISM CARRIED: %s\n' % out['OPTIMISM_CARRIED'])
    bas = res['after'].get('basis') or {}
    print('basis input: %s md5 %s · %d rows · %s' % (bas.get('file'), (bas.get('md5') or '')[:8],
                                                     bas.get('rows', 0), (bas.get('provenance') or {}).get('counts')))
    print('\nPER-PICK NEUTRALITY (ratio of realised v0 to the anchor in each pick neighbourhood)')
    print('  pick    BEFORE     AFTER        pick    BEFORE     AFTER')
    for i in range(32):
        a, b = PICKS[i], PICKS[i + 32]
        print('  %4d  %8.4f  %8.4f        %4d  %8.4f  %8.4f'
              % (a, res['before']['neutrality_per_pick'][str(a)], res['after']['neutrality_per_pick'][str(a)],
                 b, res['before']['neutrality_per_pick'][str(b)], res['after']['neutrality_per_pick'][str(b)]))
    for nm in ('before', 'after'):
        d = v[nm]
        print('\n%-7s limb1 neutrality-at-every-pick %-5s (worst dev %.4f, %d picks out) · '
              'limb2 bounds-held %-5s (%d lines out) -> ACCEPTANCE %s'
              % (nm.upper(), d['limb1_local_neutrality_every_pick'], d['worst_deviation'],
                 d['n_picks_out'], d['limb2_bounds_held'], d['n_lines_out_of_bound'],
                 'PASS' if d['ACCEPTANCE'] else 'FAIL'))
    print('\nwrote la_acceptance_perpick.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
