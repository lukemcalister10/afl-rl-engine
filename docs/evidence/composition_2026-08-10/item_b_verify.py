"""ITEM B WIRING VERIFICATION — conservation shown, not asserted, on the LIVE pool population.

Checks, on the patched engine:
  1. pool Sigma entry_anchor is held EXACTLY (C5 level-preserving);
  2. the age-unknown cell is its own cell (factor exactly 1.0 x renormaliser, never absorbed);
  3. the curve is CONTINUOUS in draft age (no integer cliff) — sampled on a half-year grid;
  4. NON-POOL rows are byte-untouched (the ND path never reads _b_factor);
  5. the movers, by age band, with the redistribution shown.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # re-runnable FROM THE TREE
import numpy as np
from engine_load import load
g = load()
MA = g['MA']; cp = g['cp']
entry_anchor = g['entry_anchor']
pool = [p for p in MA.data if g['_isreal'](p) and p.get('_pool')]
nd = [p for p in MA.data if g['_isreal'](p) and not p.get('_pool')]
PL_F = g['_PL_F']

print("live pool population: n=%d   non-pool: n=%d" % (len(pool), len(nd)))
print("C5 renormaliser K = %.10f  (re-derived from THIS roster, not stored)" % g['_b_renorm']())

# 1. conservation
before = sum(float(MA.pool_level(p)) * PL_F for p in pool)
after = sum(float(entry_anchor(p)) for p in pool)
print("\n1. CONSERVATION (pool Sigma entry_anchor)")
print("   before (age-blind) = %.6f" % before)
print("   after  (age-shaped)= %.6f" % after)
print("   delta              = %.9f   (%.3e relative)" % (after - before, abs(after - before) / before))
assert abs(after - before) / before < 1e-12, "C5 CONSERVATION BROKEN"
print("   PASS — held exactly.")

# 2. age-unknown its own cell
unk = [p for p in pool if g['_b_age'](p) is None]
print("\n2. AGE-UNKNOWN CELL: n=%d" % len(unk))
if unk:
    f = g['_b_factor'](unk[0]); print("   factor = %.10f == K (shape 1.0, never absorbed): %s"
                                      % (f, abs(f - g['_b_renorm']()) < 1e-12))
else:
    print("   empty on this store (the 302-birthdate write closed it) — the rule is still coded.")

# 3. continuity
print("\n3. CONTINUITY IN DRAFT AGE (no integer cliff)")
grid = [17.0, 17.5, 18.0, 18.25, 18.5, 18.75, 19.0, 19.5, 20.0, 20.25, 20.5, 20.75, 21.0, 21.5, 22.0, 26.0]
vals = [g['_b_shape'](a) for a in grid]
print("   " + " · ".join("%.2f:%.4f" % (a, v) for a, v in zip(grid, vals)))
jumps = [abs(vals[i + 1] - vals[i]) for i in range(len(vals) - 1)]
print("   largest step on the grid = %.4f (a cliff would show as a jump at an integer)" % max(jumps))

# 4. non-pool untouched
print("\n4. NON-POOL ROWS UNTOUCHED")
bad = [p['key'] for p in nd[:400] if float(entry_anchor(p)) != float(g['v0_start'](p))]
print("   checked 400 non-pool rows; entry_anchor != v0_start on %d of them  %s"
      % (len(bad), "PASS" if not bad else "FAIL " + str(bad[:5])))

# 5. movers by band
print("\n5. THE REDISTRIBUTION, BY BAND")
def band(a):
    if a is None: return 'age-unknown'
    return '<=18' if a <= 18 else ('19-20' if a <= 20 else '21+')
agg = {}
for p in pool:
    b = band(g['_b_age'](p))
    b0 = float(MA.pool_level(p)) * PL_F
    b1 = float(entry_anchor(p))
    d = agg.setdefault(b, [0, 0.0, 0.0])
    d[0] += 1; d[1] += b0; d[2] += b1
print("   %-13s %6s %14s %14s %12s %9s" % ("band", "n", "before", "after", "delta", "x"))
tot = 0.0
for b in ('<=18', '19-20', '21+', 'age-unknown'):
    if b not in agg: continue
    n, b0, b1 = agg[b]; tot += b1 - b0
    print("   %-13s %6d %14.1f %14.1f %+12.1f %9.4f" % (b, n, b0, b1, b1 - b0, b1 / b0 if b0 else 0))
print("   %-13s %6s %14s %14s %+12.6f" % ("TOTAL", "", "", "", tot))
frac = sum(abs(agg[b][2] - agg[b][1]) for b in agg) / 2.0 / before
print("   share of pool year-0 value redistributed = %.1f%%" % (100 * frac))
