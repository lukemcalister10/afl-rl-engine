#!/usr/bin/env python3
"""ORDER B — R-VETLEAN re-tune (PREREG_B_A1.md rules, fixed before this ran).
Grid over the fitted CI box (rho0 0..0.08 step .005; g .010...045 step .0025). For each candidate
ladder: offline survivor anchored B for talls (delta-space replica ratios, C-REP rule), then the
calibrated prediction B_hat(a) = B_cal(a) * B_off(a; cand) / B_off(a; 0.030,0.025).
Admissible: every cell 27..31 in [0.945, 1.15]. Objective: min sum W_a (B_hat-1)^2 (b2 weights).
Publishes the chosen point vs the original fit point with both cell tables."""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
exec(open(os.path.join(HERE, 'bb_fade_fit.py')).read().split('# control: reproduce')[0])

B_CAL = {27: 1.0152, 28: 0.934, 29: 0.8552, 30: 1.0241, 31: 0.8358}   # RESULTS_W5_O33CAL.json tall|survivor
W_A = {27: 1 / 0.13 ** 2, 28: 1 / 0.14 ** 2, 29: 1 / 0.20 ** 2, 30: 1 / 0.39 ** 2, 31: 1 / 0.61 ** 2}  # b2 weights
FLOOR, CEIL = 0.945, 1.15
RHO_GRID = [round(x, 3) for x in np.arange(0.0, 0.0801, 0.005)]
G_GRID = [round(x, 4) for x in np.arange(0.010, 0.04501, 0.0025)]


def ladder_of(rho0, g, n=14):
    f, out = 1.0, []
    for j in range(1, n + 1):
        f *= (1.0 - min(0.60, max(0.0, rho0 + g * (j - 1))))
        out.append(f)
    return out


def frac_engine(a, pa):
    return DELTAS[max(-8, min(14, int(round(a - pa))))]


def make_frac_tall(lad):
    def f(a, pa_star=27):
        j = int(round(a - pa_star))
        if j <= 0:
            return DELTAS[max(-8, j)]
        if j <= len(lad):
            return lad[j - 1]
        lr = lad[-1] / lad[-2]
        v = lad[-1]
        for _ in range(j - len(lad)):
            v *= lr
        return v
    return f


def replica_mark(bar, a, L, fracfn, pa):
    f_a = fracfn(a, pa)
    if f_a < 1e-6:
        return 0.0
    lp = L / f_a
    cl = L
    prod = 0.0
    for k in range(18):
        ag = a + k
        fv = fracfn(ag, pa)
        if ag > 38 or fv < 0.42:
            break
        lev = lp * fv
        if ag <= pa or k == 0:
            lev = max(lev, cl)
        base = lev + capt_prem(lev)
        prod += posval(base - REPL[bar]) * 21 / 1.14 ** k
    if bar in ('KPF', 'KPD'):
        prod *= 1.05
    runway = min(max((25 - a) / 6.0, 0), 1)
    elite = min(max((lp / PEAK[bar] - 0.97) / 0.30, 0), 1)
    return prod * (1 + runway * elite * PMAX)


TALL = [x for x in rows if x['pos'] == 'TALL']
for x in TALL:
    x['repM'] = (replica_mark(x['bar'], x['age'], x['L'], frac_engine, PEAK_AGE[x['bar']])
                 if (x['L'] is not None and x['bar'] in BARS) else None)


def b_off(lad):
    ft = make_frac_tall(lad)
    marks = {}
    for x in TALL:
        if x['repM']:
            mn = replica_mark(x['bar'], x['age'], x['L'], ft, 27)
            marks[id(x)] = x['mark'] * mn / x['repM']
        else:
            marks[id(x)] = x['mark']
    sel = [x for x in TALL if x['surv']]
    anc = [x for x in sel if x['age'] in ANCHOR_AGES]
    anc_r = np.mean([marks[id(x)] for x in anc]) / np.mean([x['R'] for x in anc])
    out = {}
    for a in TEST_AGES:
        cell = [x for x in sel if x['age'] == a]
        Rm = np.mean([x['R'] for x in cell])
        out[a] = (np.mean([marks[id(x)] for x in cell]) / Rm) / anc_r
    return out


B0 = b_off(ladder_of(0.030, 0.025))
print('offline B at the original fit point: ' + ' '.join('%d:%.3f' % (a, B0[a]) for a in TEST_AGES))
results = []
for r0 in RHO_GRID:
    for g in G_GRID:
        lad = ladder_of(r0, g)
        Bo = b_off(lad)
        Bh = {a: B_CAL[a] * Bo[a] / B0[a] for a in TEST_AGES}
        ok = all(FLOOR <= Bh[a] <= CEIL for a in TEST_AGES)
        loss = sum(W_A[a] * (Bh[a] - 1) ** 2 for a in TEST_AGES)
        results.append((ok, loss, r0, g, Bh, [round(v, 4) for v in lad[:6]]))
adm = [r for r in results if r[0]]
print('admissible points: %d of %d' % (len(adm), len(results)))
if adm:
    adm.sort(key=lambda t: t[1])
    ok, loss, r0, g, Bh, lad6 = adm[0]
    print('CHOSEN: rho0=%.3f g=%.4f  loss=%.3f  ladder f(1..6)=%s' % (r0, g, loss, lad6))
    print('  predicted built cells: ' + ' '.join('%d:%.3f' % (a, Bh[a]) for a in TEST_AGES))
    for _, ls, rr, gg, bh, ld in adm[1:6]:
        print('  runner-up rho0=%.3f g=%.4f loss=%.3f cells ' % (rr, gg, ls) +
              ' '.join('%d:%.2f' % (a, bh[a]) for a in TEST_AGES))
    CHOSEN = dict(rho0=r0, g=g, loss=round(loss, 3), ladder6=lad6,
                  predicted={str(a): round(Bh[a], 4) for a in TEST_AGES})
else:
    # trade-off frontier: max the min cell subject to no cell > CEIL
    frontier = [r for r in results if all(v <= CEIL for v in r[4].values())]
    frontier.sort(key=lambda t: -min(t[4].values()))
    ok, loss, r0, g, Bh, lad6 = frontier[0]
    print('ADMISSIBLE SET EMPTY — trade-off frontier head: rho0=%.3f g=%.4f min-cell %.3f cells ' % (
        r0, g, min(Bh.values())) + ' '.join('%d:%.3f' % (a, Bh[a]) for a in TEST_AGES))
    CHOSEN = dict(rho0=r0, g=g, loss=round(loss, 3), ladder6=lad6, empty_set=True,
                  predicted={str(a): round(Bh[a], 4) for a in TEST_AGES})
json.dump(dict(calibration=B_CAL, floor=FLOOR, ceil=CEIL,
               offline_B_original={str(a): round(B0[a], 4) for a in TEST_AGES},
               chosen=CHOSEN,
               n_admissible=len(adm), n_grid=len(results)),
          open(os.path.join(HERE, 'VETLEAN_FIT.json'), 'w'), indent=1)
print('wrote VETLEAN_FIT.json')
