#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART B, ROBUSTNESS. Leave one class out.

2015 is the outlier. If ORDER P only beats ORDER K because of 2015, that is worth knowing and is
reported here rather than left inside an average.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

M = {t: L.class_marks(L.load(t))[0] for t in ('OKRULED', 'PBUILT')}
MEAS = {int(k): v for k, v in json.load(open(os.path.join(HERE, 'CD_OUTCOMES.json')))['meas'].items()}
KEYS = ['surp_per_row', 'prod_per_row', 'games_per_row', 'surp_ppg', 'ppg', 'share_above',
        'share_played', 'career_games_per_row', 'share_100']
NICE = dict(zip(KEYS, ['yr1 surplus/row', 'yr1 production/row', 'yr1 games/row', 'yr1 surplus ppg',
                       'yr1 ppg', 'share above bar', 'share played', 'career games/row', 'share 100g']))


def rk(a):
    a = np.asarray(a, float); o = a.argsort(); r = np.empty(len(a)); r[o] = np.arange(1., len(a) + 1)
    for v in set(a):
        m = a == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def pe(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if a.std() == 0 or b.std() == 0:
        return float('nan')
    return float(np.corrcoef(a, b)[0, 1])


def sp(a, b):
    return pe(rk(a), rk(b))


P('=' * 118)
P('B-ROBUST — LEAVE ONE CLASS OUT. Spearman of each board\'s mark against realised year-1')
P('    PRODUCTION PER ROW, with one class removed at a time.')
P('=' * 118)
P('  %-14s %10s %10s %10s' % ('dropped', 'ORDER K', 'ORDER P', 'P minus K'))
LOO = {}
for drop in [None] + L.W2:
    ys = [y for y in L.W2 if y != drop]
    x = [MEAS[y]['prod_per_row'] for y in ys]
    a = sp([M['OKRULED'][y] for y in ys], x)
    b = sp([M['PBUILT'][y] for y in ys], x)
    LOO[drop] = (a, b)
    P('  %-14s %10.3f %10.3f %+10.3f' % ('none' if drop is None else str(drop - 1), a, b, b - a))
P()
P('=' * 118)
P('B-ROBUST-2 — the same, all nine measures, with the 2015 class REMOVED (n = 10).')
P('=' * 118)
P('  %-24s %10s %10s %10s %10s %10s %10s' %
  ('measure', 'K spear', 'P spear', 'd spear', 'K pear', 'P pear', 'd pear'))
ys = [y for y in L.W2 if y != 2016]
ns = npn = 0
for k in KEYS:
    x = [MEAS[y][k] for y in ys]
    ak = sp([M['OKRULED'][y] for y in ys], x); ap = sp([M['PBUILT'][y] for y in ys], x)
    bk = pe([M['OKRULED'][y] for y in ys], x); bp = pe([M['PBUILT'][y] for y in ys], x)
    ns += (ap > ak); npn += (bp > bk)
    P('  %-24s %10.3f %10.3f %+10.3f %10.3f %10.3f %+10.3f' % (NICE[k], ak, ap, ap - ak, bk, bp, bp - bk))
P('  with 2015 dropped, ORDER P still correlates more strongly on %d of 9 (Spearman), %d of 9 (Pearson).'
  % (ns, npn))
P()
P('=' * 118)
P('B-ROBUST-3 — RANK AGREEMENT. Where each class sits on the board, and where it sits on outcomes.')
P('=' * 118)
prod = [MEAS[y]['prod_per_row'] for y in L.W2]
surp = [MEAS[y]['surp_per_row'] for y in L.W2]
mk = [M['OKRULED'][y] for y in L.W2]
mp = [M['PBUILT'][y] for y in L.W2]
def ord_(v, rev=True):
    return {y: i + 1 for i, y in enumerate(sorted(L.W2, key=lambda z: -v[L.W2.index(z)]))}
rprod, rsurp, rK, rP = ord_(prod), ord_(surp), ord_(mk), ord_(mp)
P('  %-8s %10s %10s %12s %12s' % ('class', 'rank K', 'rank P', 'rank prod/row', 'rank surp/row'))
for y in L.W2:
    P('  %-8d %10d %10d %12d %12d' % (y - 1, rK[y], rP[y], rprod[y], rsurp[y]))
P()
P('  sum of |rank(board) - rank(production)| over the eleven classes:')
P('    ORDER K %d   ORDER P %d   (lower is better)' %
  (sum(abs(rK[y] - rprod[y]) for y in L.W2), sum(abs(rP[y] - rprod[y]) for y in L.W2)))
P('  sum of |rank(board) - rank(surplus)|:')
P('    ORDER K %d   ORDER P %d' %
  (sum(abs(rK[y] - rsurp[y]) for y in L.W2), sum(abs(rP[y] - rsurp[y]) for y in L.W2)))

open(os.path.join(HERE, 'CD_LOO_out.txt'), 'w').write('\n'.join(OUT) + '\n')
