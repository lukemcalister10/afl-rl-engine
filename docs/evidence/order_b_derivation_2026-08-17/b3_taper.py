#!/usr/bin/env python3
# =====================================================================================================
# ORDER B DERIVATION -- b3: the v7 age-taper RE-DERIVED AS A QUANTILE OBJECT (PREREG_B.md Object 4).
# Data: W6's 9,877-vantage ground-truth table. For each age band, exceedance(asc') of realized forward
# best-3 over the tapered ceiling b5' = m + asc'*(b5_raw - m); the taper median m is recovered exactly
# per vantage where asc<0.999. Fitted asc*(band) = the asc' in (0,1] hitting the 3% target; boundary
# solution asc*=1 for every band = the derived object is RETIREMENT.
# =====================================================================================================
import csv, json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
W6CSV = os.path.join(os.path.dirname(HERE), 'order33_w6_2026-08-17', 'W6_VANTAGES.csv')
SEED = 34
TARGET = 0.03

rows = []
with open(W6CSV) as f:
    for r in csv.DictReader(f):
        rows.append(dict(key=r['key'], Y=int(r['Y']), age=float(r['age']), pos=r['pos'],
                         games=int(r['games']), peak_fwd=float(r['peak_fwd']),
                         pred_raw=float(r['pred_raw']), b5_raw=float(r['b5_raw']),
                         b5_tap=float(r['b5_tap']), asc=float(r['asc'])))
print('vantages %d' % len(rows))

# recover the taper median m where invertible; asc'=1 evaluation never needs m
for r in rows:
    if r['asc'] < 0.999:
        r['m'] = (r['b5_tap'] - r['asc'] * r['b5_raw']) / (1.0 - r['asc'])
    else:
        r['m'] = None

BANDS = [('<=19', lambda a: a <= 19), ('20-21', lambda a: 20 <= a <= 21), ('22-23', lambda a: 22 <= a <= 23),
         ('24-26', lambda a: 24 <= a <= 26), ('27+', lambda a: a >= 27)]


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((c - h) / d, (c + h) / d)


def exceed(sel, asc_p):
    """exceedance of realized peak over the ceiling at candidate asc'. asc'=1 uses b5_raw directly."""
    k = n = 0
    for r in sel:
        if abs(asc_p - 1.0) < 1e-9:
            ceil = r['b5_raw']
        else:
            if r['m'] is None:      # taper inert at this age in v7; candidate asc'<1 not evaluable
                continue
            ceil = r['m'] + asc_p * (r['b5_raw'] - r['m'])
        n += 1
        if r['peak_fwd'] > ceil:
            k += 1
    return k, n


OUT = dict(meta=dict(input=W6CSV, n=len(rows), target=TARGET), bands={})
ASC_GRID = [round(x, 2) for x in np.arange(0.40, 1.001, 0.05)]
print('\nband        n     v7-as-priced   asc\'=1 (retire)   fitted asc* in (0,1]')
for name, fn in BANDS:
    sel = [r for r in rows if fn(r['age'])]
    k_now = sum(1 for r in sel if r['peak_fwd'] > r['b5_tap'])
    n_now = len(sel)
    e_now = k_now / n_now if n_now else float('nan')
    k1, n1 = exceed(sel, 1.0)
    e1 = k1 / n1 if n1 else float('nan')
    lo1, hi1 = wilson(k1, n1)
    # exceedance is monotone nonincreasing in asc' (ceiling rises with asc' when b5_raw>m);
    # the fitted asc* is the smallest asc' in (0,1] with exceedance <= target, else the boundary 1.0
    grid = {}
    inv = [r for r in sel if r['m'] is not None]
    for a_p in ASC_GRID:
        kk, nn = exceed(sel, a_p)
        grid[a_p] = round(kk / nn, 4) if nn else None
    fitted = None
    for a_p in ASC_GRID:
        if grid[a_p] is not None and grid[a_p] <= TARGET:
            fitted = a_p
            break
    boundary = fitted is None or fitted >= 1.0
    asc_star = 1.0 if boundary else fitted
    OUT['bands'][name] = dict(n=n_now, n_invertible=len(inv),
                              exceed_v7=round(e_now, 4),
                              exceed_asc1=round(e1, 4), exceed_asc1_wilson=[round(lo1, 4), round(hi1, 4)],
                              grid=grid, asc_star=asc_star, boundary_solution=bool(boundary),
                              residual_above_target=round(max(0.0, e1 - TARGET), 4))
    print('%-8s %6d   %6.2f%%        %5.2f%% [%.2f,%.2f]   asc*=%.2f%s' % (
        name, n_now, 100 * e_now, 100 * e1, 100 * lo1, 100 * hi1, asc_star,
        ' (BOUNDARY — no taper in (0,1] is calibrated)' if boundary else ''))

# sensitivity: <=2016 window
sel16 = [r for r in rows if r['Y'] <= 2016]
k, n = exceed(sel16, 1.0)
OUT['sensitivity_le2016'] = dict(n=n, exceed_asc1=round(k / n, 4))
print('\nsensitivity <=2016: asc\'=1 exceedance %.2f%% (n=%d)' % (100 * k / n, n))

# RUCK cut (the owner's suspicion)
selr = [r for r in rows if r['pos'] == 'RUCK']
k_nowr = sum(1 for r in selr if r['peak_fwd'] > r['b5_tap'])
k1r, n1r = exceed(selr, 1.0)
OUT['ruck'] = dict(n=len(selr), exceed_v7=round(k_nowr / len(selr), 4), exceed_asc1=round(k1r / n1r, 4))
print('RUCK: v7 %.2f%% -> asc\'=1 %.2f%%' % (100 * k_nowr / len(selr), 100 * k1r / n1r))

with open(os.path.join(HERE, 'RESULTS_B_TAPER.json'), 'w') as f:
    json.dump(OUT, f, indent=1)
print('\nwrote RESULTS_B_TAPER.json')
