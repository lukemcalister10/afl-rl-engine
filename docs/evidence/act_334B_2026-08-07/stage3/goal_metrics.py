"""334 stage B / stage 3 STEP 9 — GOAL METRICS from the FINAL board + the FINAL matrix."""
import os, sys, json, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = json.load(open(os.path.join(HERE, 'board_STAGE3_6c9f8d3a.json')))
MATRIX = os.path.join(HERE, 'per_entrant_338_stage3.json')
spec = importlib.util.spec_from_file_location('harness_pvc', os.path.join(HERE, 'harness_pvc_REPINNED_pass3.py'))
H = importlib.util.module_from_spec(spec); sys.modules['harness_pvc'] = H; spec.loader.exec_module(H)
meta, ND = H.load_matrix(MATRIX)

# ---------------- 1. TOP-END RATIO -------------------------------------------------------------
act = [p for p in BOARD['active'] if p.get('v') is not None]
top = max(act, key=lambda p: p['v'])
print('TOP-END RATIO')
print('  max active display value = %d  (%s, %s)' % (top['v'], top.get('name') or top['key'], top.get('club')))
print('  ratio to the numeraire (pick 1 = 3000) = %d / 3000 = %.6f' % (top['v'], top['v'] / 3000.0))
print('  runner-up: %s' % ', '.join('%s %d' % (p.get('name') or p['key'], p['v'])
                                    for p in sorted(act, key=lambda p: -p['v'])[1:4]))

# ---------------- 2. PER-ENTRY-YEAR TABLE ------------------------------------------------------
# For N = 0..5: mean value at the PEAK year / mean value at year N, over entrants whose window
# covers BOTH years. Whole cohort. Denominators printed.
PEAK = 4


def val(r, n):
    if n == 0:
        return float(r['v0'])
    vp = r.get('vpath') or []
    if n - 1 < len(vp):
        v = vp[n - 1]
        return float(v) if v is not None else 0.0
    return 0.0


def covers(r, n):
    return (int(r['year']) + n) <= 2026


print('\nPER-ENTRY-YEAR TABLE — mean value at the PEAK year (%d) / mean value at year N' % PEAK)
print('whole cohort, busts at 0 in every denominator, entrants whose window covers BOTH years')
print('  %2s  %8s  %12s  %12s  %10s' % ('N', 'n(both)', 'mean_yr%d' % PEAK, 'mean_yrN', 'ratio'))
for N in range(0, 6):
    pop = [r for r in ND if covers(r, N) and covers(r, PEAK)]
    a = float(np.mean([val(r, PEAK) for r in pop]))
    b = float(np.mean([val(r, N) for r in pop]))
    print('  %2d  %8d  %12.4f  %12.4f  %10.6f' % (N, len(pop), a, b, a / b))

# ---------------- 3. YEAR-OVER-YEAR INCREMENTS + THE FRONT-LOADED ASSERT ------------------------
print('\nYEAR-OVER-YEAR INCREMENTS of the final whole-cohort path (ratio to year 0, same-set means)')
path = []
for n in range(0, 8):
    inc = [r for r in ND if covers(r, n)]
    m = float(np.mean([val(r, n) for r in inc]))
    m0 = float(np.mean([val(r, 0) for r in inc]))
    path.append((n, len(inc), m, m0, m / m0))
for n, ni, m, m0, rt in path:
    print('   yr %d  n=%4d  mean %9.4f  ratio %.6f' % (n, ni, m, m0 and rt))
print('  increments (ratio units):')
incs = {}
for i in range(1, len(path)):
    d = path[i][4] - path[i - 1][4]
    incs[(path[i - 1][0], path[i][0])] = d
    print('    yr%d -> yr%d : %+0.6f' % (path[i - 1][0], path[i][0], d))
a12, a34 = incs[(1, 2)], incs[(3, 4)]
ok = a12 > a34
print('  FRONT-LOADED ASSERT  (yr1->2 increment STRICTLY exceeds yr3->4): %+0.6f > %+0.6f  -> %s'
      % (a12, a34, 'PASS' if ok else 'FAIL'))
assert ok, 'front-loaded assert FAILED'
