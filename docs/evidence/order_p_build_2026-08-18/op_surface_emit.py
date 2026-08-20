#!/usr/bin/env python3
"""ORDER P BUILD — emit the PEDIGREE PREMIUM surface as an engine literal, and prove it.

The surface is NOT re-fitted here. It is rebuilt by ORDER P's own `op_lib.Premium` from ORDER P's own
population (`op_lib.season_rows` over the ORDER K matrix `per_entrant_OKRULED.json`), at the
preregistered bandwidth 0.40 with the monotonicity guard on, and then written out as the constant
block the engine carries.

Two grids, one per class, 121 nodes each over the 1st-99th percentile of ln(v0). The engine
interpolates linearly between nodes and HOLDS FLAT outside, exactly as `Premium.at` does.

  usage: OPENBLAS_NUM_THREADS=1 ... python3 op_surface_emit.py
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(REPO, 'docs/evidence/order_p_2026-08-18'))
import op_lib as PB                                                          # noqa: E402
LB = PB.LB

MK = LB.load_matrix('OKRULED')
ROWS = PB.season_rows(MK)
PG = PB.Premium(ROWS, h=PB.H_PRIMARY, iso=True)

out = dict(n_rows=len(ROWS), n_players=len(set(r['key'] for r in ROWS)),
           n_games=sum(r['games'] for r in ROWS), h=PB.H_PRIMARY, iso=True, grid_n=PB.GRID_N,
           source='op_lib.Premium over op_lib.season_rows(per_entrant_OKRULED.json)')
for cls in ('TALL', 'SMALL'):
    gx, gy = PG.grid[cls]
    out[cls] = dict(lo=float(gx[0]), hi=float(gx[-1]), y=[float(v) for v in gy],
                    raw=[float(v) for v in PG.raw[cls]], ess=[float(v) for v in PG.ess[cls]],
                    n=PG.n[cls], v0_lo=math.exp(float(gx[0])), v0_hi=math.exp(float(gx[-1])))
json.dump(out, open(os.path.join(HERE, 'PREMIUM_SURFACE.json'), 'w'), indent=1)

# ---- the engine literal ---------------------------------------------------------------------------
def emit(cls):
    gx, gy = PG.grid[cls]
    body = ',\n     '.join(','.join('%.17g' % float(v) for v in gy[i:i + 6]) for i in range(0, len(gy), 6))
    return "    '%s':(%.17g,%.17g,(\n     %s)),\n" % (cls, float(gx[0]), float(gx[-1]), body)


lit = 'O37_PG_GRID={\n' + emit('TALL') + emit('SMALL') + '}\n'
open(os.path.join(HERE, 'O37_PG_GRID.py.txt'), 'w').write(lit)

print('season rows %d · players %d · games %.0f' % (out['n_rows'], out['n_players'], out['n_games']))
for cls in ('TALL', 'SMALL'):
    d = out[cls]
    print('%-6s nodes %d  ln v0 [%.6f, %.6f]  v0 [%.1f, %.1f]  rows %d'
          % (cls, len(d['y']), d['lo'], d['hi'], d['v0_lo'], d['v0_hi'], d['n']))
print('wrote PREMIUM_SURFACE.json and O37_PG_GRID.py.txt (%d bytes)' % len(lit))

# ---- the packet's own printed table, reproduced --------------------------------------------------
print('\nPACKET_P section 3 table, reproduced from this surface:')
print('   %8s %10s %10s' % ('v0', 'SMALL', 'TALL'))
for v0 in (100, 200, 300, 450, 600, 900, 1200, 1700, 2400, 3200):
    print('   %8d %+10.2f %+10.2f' % (v0, PG.at_v0(v0, 'SMALL'), PG.at_v0(v0, 'TALL')))
