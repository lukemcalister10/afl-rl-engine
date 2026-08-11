"""PROBE 3AX, pass 4 (READ-ONLY): the remaining reportables for every specification."""
import json
import numpy as np

S = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
src = open(S + '/probe3ax3.py').read()
exec(src.split("print('=' * 122)")[0])

SEAM = {0.25: 1.014493, 0.5: 1.925722, 0.75: 2.753623, 1.0: 3.768116}
BASE_LANDING = 0.990805
LIFT1 = 1.071991 - BASE_LANDING
band = [x for x in Y1 if 20 <= x['pk'] <= 33]
spb = sum(x['price'] for x in band)
med0 = float(np.median([x['F'] / x['price'] for x in Y1]))
frac0 = float(np.mean([1.0 if x['F'] > x['price'] else 0.0 for x in Y1]))
MEAS = {}
for cn, f, bound in GATES:
    sub = [x for x in Y1 if f(x)]
    MEAS[cn] = sum(x['F'] for x in sub) / sum(x['price'] for x in sub) - 1.0

print('=' * 126)
print('MEASURED value of each gate cell (what "already priced" means numerically):')
for cn in MEAS: print('   %-34s measured residual %+0.5f   (bound on movement %s)' %
                      (cn, MEAS[cn], [b for c, f, b in GATES if c == cn][0]))
print('   uncorrected year-1 median F\' = %.4f ; fraction out-earning the uncorrected price = %.3f'
      % (med0, frac0))
print('=' * 126)
print('%-50s %9s %9s %8s %10s %9s %9s %9s' %
      ('surface', 'bandlift', 'seamW2%', 'W_max', 'yr1 land', "medF'@Wm", 'frac@Wm', 'seam@Wm'))
print('-' * 126)
ref_band = None
OUT = {}
for nm, bf, gts in SPECS:
    d, dg = build(bf, gts)
    g = {}
    for cn, f, bound in GATES:
        sub = [x for x in Y1 if f(x)]
        sp = sum(x['price'] for x in sub)
        v1 = sum(x['price'] * d(x, 1.0) for x in sub) / sp
        g[cn] = (v1, bound / abs(v1) if abs(v1) > 1e-12 else 9.9)
    wmax = min(v[1] for v in g.values())
    bl = sum(x['price'] * d(x, 1.0) for x in band) / spb
    if ref_band is None: ref_band = bl
    r = bl / ref_band
    ys = np.array([SEAM[W] * r for W in (0.25, 0.5, 0.75, 1.0)])
    ws = np.array([0.25, 0.5, 0.75, 1.0])
    w2 = float(np.interp(2.0, ys, ws)) if ys[-1] >= 2.0 else 9.9
    seam_at = float(np.interp(wmax, ws, ys))
    newp = [x['price'] * (1.0 + d(x, wmax)) for x in Y1]
    medc = float(np.median([Y1[i]['F'] / newp[i] for i in range(len(Y1))]))
    fr = float(np.mean([1.0 if Y1[i]['F'] > newp[i] else 0.0 for i in range(len(Y1))]))
    print('%-50s %9.5f %9.4f %8.4f %10.6f %9.4f %9.3f %9.4f' %
          (nm, bl, w2, wmax, BASE_LANDING + LIFT1 * wmax, medc, fr, seam_at))
    OUT[nm] = dict(g={k: v[0] for k, v in g.items()}, wmax=wmax, bandlift=bl, seamW2=w2,
                   med=medc, frac=fr, seam_at=seam_at)

print('\nTAUGHT vs MEASURED at the two REGISTERED zero cells, at W=1 (how well each surface holds them):')
print('%-50s %22s %22s' % ('surface', 'picks1-10 x topT sa', 'picks1-20 x aboveMed sa'))
print('%-50s %22s %22s' % ('', 'measured %+0.5f' % MEAS['picks 1-10 x TOP-TERCILE sa'],
                           'measured %+0.5f' % MEAS['picks 1-20 x ABOVE-MEDIAN sa']))
for nm in OUT:
    print('%-50s %22s %22s' % (nm, '%+0.5f' % OUT[nm]['g']['picks 1-10 x TOP-TERCILE sa'],
                               '%+0.5f' % OUT[nm]['g']['picks 1-20 x ABOVE-MEDIAN sa']))
json.dump(OUT, open(S + '/probe3ax4.json', 'w'), indent=1)
