#!/usr/bin/env python3
"""ORDER B — the R-VETLEAN trade-off frontier, published (PREREG_B_A1 empty-set branch)."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'bb_vetlean_fit.py')).read().split('B0 = b_off')[0])
B0 = b_off(ladder_of(0.030, 0.025))
res = []
for r0 in RHO_GRID:
    for g in G_GRID:
        Bo = b_off(ladder_of(r0, g))
        Bh = {a: B_CAL[a] * Bo[a] / B0[a] for a in TEST_AGES}
        res.append((r0, g, Bh))
front = [(min(b.values()), r0, g, b) for r0, g, b in res if max(b.values()) <= 1.15]
front.sort(key=lambda t: -t[0])
print('top frontier (all cells <= 1.15), by min cell:')
for m, r0, g, b in front[:8]:
    print('  rho0=%.3f g=%.4f min=%.3f  ' % (r0, g, m) + ' '.join('%d:%.3f' % (a, b[a]) for a in TEST_AGES))
ok945 = [(max(b.values()), r0, g, b) for r0, g, b in res if min(b.values()) >= 0.945]
ok945.sort(key=lambda t: t[0])
print('\npoints reaching floor 0.945 everywhere (ceiling ignored), by max cell:')
for m, r0, g, b in ok945[:6]:
    print('  rho0=%.3f g=%.4f max=%.3f  ' % (r0, g, m) + ' '.join('%d:%.3f' % (a, b[a]) for a in TEST_AGES))
if not ok945:
    print('  (none anywhere in the CI box)')
json.dump(dict(frontier=[dict(min_cell=round(m, 4), rho0=r0, g=g,
                              cells={str(a): round(b[a], 4) for a in TEST_AGES}) for m, r0, g, b in front[:8]],
               floor_everywhere=[dict(max_cell=round(m, 4), rho0=r0, g=g,
                                      cells={str(a): round(b[a], 4) for a in TEST_AGES}) for m, r0, g, b in ok945[:6]]),
          open(os.path.join(HERE, 'VETLEAN_TRADEOFF.json'), 'w'), indent=1)
print('wrote VETLEAN_TRADEOFF.json')
