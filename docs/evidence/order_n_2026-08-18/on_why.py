#!/usr/bin/env python3
"""ORDER N — WHY THE CONFLICT EXISTS. READ-ONLY.

The rails do not overlap, and the reason is one fact about the population rather than anything about
the mechanism. This file measures that fact.

  usage: OPENBLAS_NUM_THREADS=1 ... python on_why.py
"""
import json, math, os, sys
import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import on_lib as LB                                                          # noqa: E402
L = []


def P(s=''):
    print(s); L.append(str(s))


def spear(x, y):
    rx, ry = rankdata(x), rankdata(y)
    rx = rx - rx.mean(); ry = ry - ry.mean()
    d = math.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else float('nan')


M = json.load(open(os.path.join(HERE, 'MECH_N.json')))
S2 = json.load(open(os.path.join(HERE, 'STEP2_N.json')))
ZERO = M['s0'] + 1.0 / M['variantB']['THETA_R_frontier'] if 'variantB' in M else None
ZERO_ANCHOR = M['s0'] + M['LAMBDA'] / M['BETA_sat']

P('=' * 118)
P('ORDER N — WHY THE TWO RAILS DO NOT OVERLAP')
P('=' * 118)
P()
P('THE SHORT VERSION. The young players who are ABOVE their age bar are, very largely, the young')
P('players taken at the TOP of the draft. So a charge that relieves over-performers relieves the top')
P('of the draft, and the top of the draft is exactly where the +14%% buy rail has almost no headroom.')
P('The conflict is between the owner\'s fix and the no-arbitrage rail, and it runs through one')
P('population fact. Here is the fact.')
P()

MK = LB.load_matrix('OKRULED')
LED = LB.load_ledger()

# ---- pick vs surplus on the historical vantage cohort ------------------------------------------------
rows = S2['rows']
nd = [r for r in rows if r.get('pick')]
P('-' * 118)
P('1 · PICK AGAINST PERFORMANCE SURPLUS, on the %d vantage rows of the Step 2 cohort with a draft pick' % len(nd))
P('-' * 118)
pk = np.array([float(r['pick']) for r in nd]); ps = np.array([r['ps'] for r in nd])
P('   Spearman(pick, surplus) = %+.4f      (negative means earlier picks produce further above their bar)'
  % spear(pk, ps))
P()
P('   %-12s %6s | %9s %9s %9s | %11s' % ('pick band', 'rows', 'PS p25', 'PS median', 'PS p75', 'share at or'))
P('   %-12s %6s | %9s %9s %9s | %11s' % ('', '', '', '', '', 'past +%.2f' % ZERO_ANCHOR))
for lo, hi, lab in ((1, 10, '1-10'), (11, 20, '11-20'), (21, 40, '21-40'), (41, 64, '41-64'), (65, 999, 'pool/none')):
    s = [r for r in nd if lo <= int(r['pick']) <= hi]
    if len(s) < 10:
        continue
    a = np.array([r['ps'] for r in s])
    P('   %-12s %6d | %+9.2f %+9.2f %+9.2f | %10.1f%%' % (
        lab, len(s), np.percentile(a, 25), np.median(a), np.percentile(a, 75),
        100 * float((a >= ZERO_ANCHOR).mean())))
allps = np.array([r['ps'] for r in nd])
P('   %-12s %6d | %+9.2f %+9.2f %+9.2f | %10.1f%%' % (
    'ALL', len(nd), np.percentile(allps, 25), np.median(allps), np.percentile(allps, 75),
    100 * float((allps >= ZERO_ANCHOR).mean())))
P()
P('   A pick 1-10 row is roughly %.1f times as likely to sit past the zero point as a pick 41-64 row.' % (
    (float((np.array([r['ps'] for r in nd if int(r['pick']) <= 10]) >= ZERO_ANCHOR).mean()) + 1e-9) /
    (float((np.array([r['ps'] for r in nd if 41 <= int(r['pick']) <= 64]) >= ZERO_ANCHOR).mean()) + 1e-9)))
P()

# ---- the same on the year-1 vantage only, which is what the band table reads --------------------------
P('-' * 118)
P('2 · THE SAME AT THE YEAR-1 VANTAGE ONLY — the exact rows the year-0 -> year-1 band table reads')
P('-' * 118)
y1 = [r for r in nd if r['N'] == 1]
P('   %-12s %6s | %9s %9s | %11s | %-11s' % ('pick band', 'rows', 'PS median', 'mean g', 'share past 0-pt', 'window'))
for wname, lo_y, hi_y in (('PRIMARY', 2005, 2023), ('MODERN', 2019, 2023)):
    for lo, hi, lab in ((1, 10, '1-10'), (11, 20, '11-20'), (21, 40, '21-40'), (41, 64, '41-64')):
        s = [r for r in y1 if lo <= int(r['pick']) <= hi and lo_y <= r['Y'] <= hi_y]
        if len(s) < 8:
            continue
        a = np.array([r['ps'] for r in s])
        P('   %-12s %6d | %+9.2f %9.1f | %10.1f%% | %-11s' % (
            lab, len(s), np.median(a), np.mean([r['g'] for r in s]),
            100 * float((a >= ZERO_ANCHOR).mean()), wname))
    P()

P('-' * 118)
P('3 · THE HEADROOM THAT WAS ALREADY GONE')
P('-' * 118)
BR = json.load(open(os.path.join(HERE, 'BANDS_N.json')))
P('   %-14s %-24s %-24s' % ('board', 'picks 1-10 PRIMARY', 'picks 1-10 MODERN'))
for tag, nm in (('OKRULED', 'ORDER K'), ('O35FINAL', 'landing'), ('O31FFINAL', 'candidate 31'),
                ('MMIN031', 'dose 0, eta 0.31'), ('M0ETA0', 'eta = 0')):
    a = BR['nd'][tag]['PRIMARY|ALLCOH|picks 1-10']['apprec01']
    b = BR['nd'][tag]['MODERN|ALLCOH|picks 1-10']['apprec01']
    P('   %-14s %+9.2f%%  headroom %+6.2f  %+9.2f%%  headroom %+6.2f' % (
        nm, 100 * a, 100 * (0.14 - a), 100 * b, 100 * (0.14 - b)))
P()
P('   ORDER K has %.2f points of headroom on the modern picks 1-10 cell and %.2f on the primary one.'
  % (100 * (0.14 - BR['nd']['OKRULED']['MODERN|ALLCOH|picks 1-10']['apprec01']),
     100 * (0.14 - BR['nd']['OKRULED']['PRIMARY|ALLCOH|picks 1-10']['apprec01'])))
P('   ORDER M flagged this in its own words: "Anything that lifts the top of the draft has less')
P('   headroom than the primary table suggests." This order is the thing that lifts the top of the draft.')
P('   The modern cell carries n = %d rows at year 1.'
  % BR['nd']['OKRULED']['MODERN|ALLCOH|picks 1-10']['n_included'][1])
P()

open(os.path.join(HERE, 'WHY_N_out.txt'), 'w').write('\n'.join(L) + '\n')
print('\nwrote WHY_N_out.txt')
