"""THE SHARPENED PREDICTION TEST.

The claim: the piecewise-constant lookup in the chain is the CONDITIONAL-PRIOR BAND — the five frozen
GradientBoostingRegressor quantile models `cm` (+ `q97m`), read at `cp._feat(p,Y)[9]` (the level feature)
by `cond_prior_band` (conditional_prior.py:164-167) via `_b6_core` (_merged_recover.py:370-372).

A GBR is a sum of regression trees: its output is piecewise-constant, and its breakpoints in the level
feature are exactly the tree split thresholds on feature 9.

PREDICTION, made from the band model ALONE (no ev() call): on the originating seat's own grid
(Dolan, games fixed at 10, average 46.00 -> 53.40 step 0.2) the price is bit-identical across a grid
step IFF that step contains NO band breakpoint, and moves IFF it contains one.
Breakpoints located by bisection on the band vector, in AVERAGE units.
"""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']
Y = 2026; F = 1.052329
QK = sorted(cm.keys())

p = next(x for x in MA.data if x['player'] == 'Josh Dolan')
saved = copy.deepcopy(p['scoring'])
row = next(x for x in p['scoring'] if x['year'] == Y)


def L_of(avg):
    row['games'] = 10; row['avg'] = float(avg)
    return float(cp._feat(p, Y)[9])


def band_of_L(feat, L):
    f = list(feat); f[9] = float(L)
    a = np.array([f])
    b = np.sort(np.array([float(cm[q].predict(a)[0]) for q in QK]))
    return tuple(list(b) + [max(float(q97m.predict(a)[0]), float(b[4]))])


row['games'] = 10; row['avg'] = 49.88
feat0 = [float(x) for x in cp._feat(p, Y)]
# 1. the level input is linear in the average (the originating seat's point 2)
xs = [46.0, 48.0, 50.0, 52.0, 53.4]
print('avg -> level feature (cp._feat[9]):')
for a in xs:
    print('   avg %6.2f  L=%.8f' % (a, L_of(a)))
d = (L_of(53.4) - L_of(46.0)) / (53.4 - 46.0)
print('   dL/davg = %.8f  (linear check: mid residual %.2e)'
      % (d, L_of(49.7) - (L_of(46.0) + d * 3.7)))


def band_of_avg(avg):
    return band_of_L(feat0, L_of(avg))


# 2. locate EVERY band breakpoint in [46.0, 53.4] by scan + bisection, in AVERAGE units
lo, hi, step = 46.0, 53.4, 0.005
grid = np.arange(lo, hi + 1e-9, step)
prev = band_of_avg(grid[0]); bps = []
for a in grid[1:]:
    b = band_of_avg(a)
    if b != prev:
        x0, x1 = a - step, a
        for _ in range(60):
            m = 0.5 * (x0 + x1)
            if band_of_avg(m) == prev:
                x0 = m
            else:
                x1 = m
        bps.append((0.5 * (x0 + x1), prev, b))
        prev = b
print()
print('BAND BREAKPOINTS in [46.00, 53.40] (average units), n=%d:' % len(bps))
for a, b0, b1 in bps:
    print('   avg* = %.9f   dband = %s' % (a, ' '.join('%+.3f' % (y - x) for x, y in zip(b0, b1))))

# 3. THE PREDICTION on the originating seat's 0.2 grid
GRID = [round(46.0 + 0.2 * i, 2) for i in range(38)]
pred_change = []
for i in range(len(GRID) - 1):
    n = sum(1 for a, _, _ in bps if GRID[i] < a <= GRID[i + 1])
    pred_change.append(n)
print()
print('PREDICTION — grid steps that must move (breakpoint inside) vs must be bit-identical:')
print('   RISERS/FALLERS predicted at: %s'
      % ', '.join('%.1f->%.1f (%d bp)' % (GRID[i], GRID[i + 1], pred_change[i])
                  for i in range(len(GRID) - 1) if pred_change[i]))
print('   BIT-IDENTICAL predicted at:  %s'
      % ', '.join('%.1f->%.1f' % (GRID[i], GRID[i + 1])
                  for i in range(len(GRID) - 1) if not pred_change[i]))

# 4. CONFIRMATION — the true ev() on the same grid
vals = []
for a in GRID:
    row['games'] = 10; row['avg'] = float(a)
    vals.append(ev(p, Y) / F)
p['scoring'] = saved
print('   restore check: %.10f (shipped 247.185...)' % (ev(p, Y) / F))

print()
print('CONFIRMATION (true ev(), board currency, full precision):')
ok = bad = 0
for i in range(len(GRID) - 1):
    same = (vals[i + 1] == vals[i])
    predicted_same = (pred_change[i] == 0)
    hit = (same == predicted_same)
    ok += hit; bad += (not hit)
    print('   %6.2f -> %6.2f   %.10f -> %.10f   %+8.3f   predicted %-14s actual %-14s %s'
          % (GRID[i], GRID[i + 1], vals[i], vals[i + 1], vals[i + 1] - vals[i],
             'BIT-IDENTICAL' if predicted_same else 'MOVES(%d bp)' % pred_change[i],
             'BIT-IDENTICAL' if same else 'MOVES', 'ok' if hit else '*** MISS ***'))
print('PREDICTION SCORE: %d/%d grid steps correct, %d misses' % (ok, ok + bad, bad))
json.dump({'bps': [(a, list(b0), list(b1)) for a, b0, b1 in bps], 'grid': GRID, 'vals': vals,
           'pred_change': pred_change}, open(OUTBASE + '.json', 'w'), indent=1, default=str)
