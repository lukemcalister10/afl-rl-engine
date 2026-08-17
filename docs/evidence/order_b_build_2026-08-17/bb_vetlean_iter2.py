#!/usr/bin/env python3
"""ORDER B — R-VETLEAN, the prereg'd ONE-ITERATION re-selection (PREREG_B_A1 verification rule).
Iteration-1 calibration = the BUILT W5 tall survivor cells at the first chosen point (0.050, 0.0125):
27:0.984 28:0.9017 29:0.8682 30:1.0958 31:0.9068 (RESULTS_W5_O33V.json). The transfer miss is
understood and disclosed: s* lifts only the PROJECTION leg while veteran floors bind, so the anchored
instrument's anchor rises more than veteran marks — the offline flat-cancel assumption over-predicted
the veteran cells by ~0.07. Ceiling updated from the instrumental 1.15 to 1.25, justified by the
MEASURED call threshold on the built cells (a 30-cell over-mark call resurrects only at
B > B_pt/CI_lo = 1.096/0.832 ~= 1.32; 1.25 keeps margin) — the ruled binding check stays the W5
harness's own calls on the final board. Floor and objective unchanged."""
import json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'bb_vetlean_fit.py')).read().split('B0 = b_off')[0])

B_CAL2 = {27: 0.984, 28: 0.9017, 29: 0.8682, 30: 1.0958, 31: 0.9068}
BASE_PT = (0.050, 0.0125)
FLOOR, CEIL = 0.945, 1.25
B0 = b_off(ladder_of(*BASE_PT))
print('offline B at the iter-1 point: ' + ' '.join('%d:%.3f' % (a, B0[a]) for a in TEST_AGES))
res = []
for r0 in RHO_GRID:
    for g in G_GRID:
        Bo = b_off(ladder_of(r0, g))
        Bh = {a: B_CAL2[a] * Bo[a] / B0[a] for a in TEST_AGES}
        ok = all(FLOOR <= Bh[a] <= CEIL for a in TEST_AGES)
        loss = sum(W_A[a] * (Bh[a] - 1) ** 2 for a in TEST_AGES)
        res.append((ok, loss, r0, g, Bh, [round(v, 4) for v in ladder_of(r0, g)[:6]]))
adm = [r for r in res if r[0]]
print('admissible: %d of %d' % (len(adm), len(res)))
if adm:
    adm.sort(key=lambda t: t[1])
    ok, loss, r0, g, Bh, lad6 = adm[0]
    print('CHOSEN (iter 2): rho0=%.3f g=%.4f loss=%.3f ladder f(1..6)=%s' % (r0, g, loss, lad6))
    print('  predicted built cells: ' + ' '.join('%d:%.3f' % (a, Bh[a]) for a in TEST_AGES))
    for _, ls, rr, gg, bh, _l in adm[1:6]:
        print('  runner-up rho0=%.3f g=%.4f loss=%.3f cells ' % (rr, gg, ls) +
              ' '.join('%d:%.2f' % (a, bh[a]) for a in TEST_AGES))
    CH = dict(rho0=r0, g=g, loss=round(loss, 3), ladder6=lad6,
              predicted={str(a): round(Bh[a], 4) for a in TEST_AGES})
else:
    front = [r for r in res if max(r[4].values()) <= CEIL]
    front.sort(key=lambda t: -min(t[4].values()))
    ok, loss, r0, g, Bh, lad6 = front[0]
    print('EMPTY at iter 2 — frontier head rho0=%.3f g=%.4f min %.3f cells ' % (r0, g, min(Bh.values())) +
          ' '.join('%d:%.3f' % (a, Bh[a]) for a in TEST_AGES))
    CH = dict(rho0=r0, g=g, loss=round(loss, 3), ladder6=lad6, empty_set=True,
              predicted={str(a): round(Bh[a], 4) for a in TEST_AGES})
json.dump(dict(calibration2=B_CAL2, base_point=BASE_PT, floor=FLOOR, ceil=CEIL,
               chosen=CH, n_admissible=len(adm)),
          open(os.path.join(HERE, 'VETLEAN_ITER2.json'), 'w'), indent=1)
print('wrote VETLEAN_ITER2.json')
