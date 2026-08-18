#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART B, the apples-to-apples version.

The class mark is a RATIO OF SUMS, so an expensive row counts more than a cheap one. Part A's
outcome measures are per-row and unweighted. This file repeats the decisive test with the outcome
measures weighted by the same year-0 price that weights the mark.
"""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

K = L.load('OKRULED')
M = {t: L.class_marks(L.load(t))[0] for t in ('OKRULED', 'PBUILT', 'O35FINAL')}
per, wend = L.rowset(K)

W = {}
for y in L.W2:
    pop = [r for r in per[y] if L.year1_price(r, y, wend) is not None]
    den = sum(float(r['v0']) for r in pop)
    g = pr = su = pl = 0.0
    for r in pop:
        v0 = float(r['v0']); s = L.season_of(r, y)
        if not s or s.get('avg') is None or s.get('bar') not in L.BARS:
            continue
        b = L.age_bar(s['bar'], L.age_at(r, y))
        gg = float(s['games'])
        g += v0 * gg; pr += v0 * gg * float(s['avg']); su += v0 * gg * (float(s['avg']) - b); pl += v0
    W[y] = dict(wgames=g / den, wprod=pr / den, wsurp=su / den, wplayed=pl / den)

def rk(a):
    a = np.asarray(a, float); o = a.argsort(); r = np.empty(len(a)); r[o] = np.arange(1., len(a) + 1)
    for v in set(a):
        m = a == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r
def pe(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float('nan') if a.std() == 0 or b.std() == 0 else float(np.corrcoef(a, b)[0, 1])
def sp(a, b):
    return pe(rk(a), rk(b))

rng = np.random.default_rng(20260818)
def _pr(A, B):
    A = A - A.mean(1, keepdims=True); B = B - B.mean(1, keepdims=True)
    n = (A * B).sum(1); d = np.sqrt((A * A).sum(1) * (B * B).sum(1))
    o = np.full(len(n), np.nan); m = d > 0; o[m] = n[m] / d[m]; return o
def _rr(A):
    o = A.argsort(1, kind='stable'); n = A.shape[1]; r = np.empty(A.shape)
    np.put_along_axis(r, o, np.tile(np.arange(1., n + 1), (A.shape[0], 1)), 1); return r
def bootd(a1, a2, b, kind):
    n = len(b); idx = rng.integers(0, n, size=(20000, n))
    A1 = np.asarray(a1, float)[idx]; A2 = np.asarray(a2, float)[idx]; B = np.asarray(b, float)[idx]
    if kind == 's':
        A1, A2, B = _rr(A1), _rr(A2), _rr(B)
    d = _pr(A1, B) - _pr(A2, B); d = d[np.isfinite(d)]
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)), float((d > 0).mean())

P('=' * 122)
P('B-WEIGHTED — the same test, with the realised measures weighted by year-0 price, the same weight')
P('    the class mark itself uses. n = 11 classes, CIs over 20,000 bootstrap resamples of classes.')
P('=' * 122)
P()
P('  the weighted measures themselves:')
P('  %-6s %12s %12s %12s %12s %10s %10s' %
  ('class', 'w games', 'w production', 'w surplus', 'w played', 'mark K', 'mark P'))
for y in L.W2:
    P('  %-6d %12.2f %12.1f %+12.1f %11.1f%% %10.4f %10.4f'
      % (y - 1, W[y]['wgames'], W[y]['wprod'], W[y]['wsurp'], 100 * W[y]['wplayed'],
         M['OKRULED'][y], M['PBUILT'][y]))
P()
for k, nice in (('wprod', 'price-weighted year-1 production'), ('wsurp', 'price-weighted year-1 surplus'),
                ('wgames', 'price-weighted year-1 games'), ('wplayed', 'price-weighted share who played')):
    x = [W[y][k] for y in L.W2]
    P('  ---- %s ----' % nice)
    for t, lab in (('OKRULED', 'ORDER K'), ('PBUILT', 'ORDER P'), ('O35FINAL', 'landing cand')):
        P('  %-14s Spearman %+.3f   Pearson %+.3f' % (lab, sp([M[t][y] for y in L.W2], x),
                                                      pe([M[t][y] for y in L.W2], x)))
    a, b, pr = bootd([M['PBUILT'][y] for y in L.W2], [M['OKRULED'][y] for y in L.W2], x, 's')
    c, d, pr2 = bootd([M['PBUILT'][y] for y in L.W2], [M['OKRULED'][y] for y in L.W2], x, 'p')
    P('  P minus K   Spearman %+.3f [%+.3f, %+.3f] P>K %.0f%%   Pearson %+.3f [%+.3f, %+.3f] P>K %.0f%%'
      % (sp([M['PBUILT'][y] for y in L.W2], x) - sp([M['OKRULED'][y] for y in L.W2], x), a, b, 100 * pr,
         pe([M['PBUILT'][y] for y in L.W2], x) - pe([M['OKRULED'][y] for y in L.W2], x), c, d, 100 * pr2))
    ys = [y for y in L.W2 if y != 2016]
    xs = [W[y][k] for y in ys]
    P('  with the 2015 class DROPPED (n=10): K %+.3f  P %+.3f  d %+.3f (Spearman)'
      % (sp([M['OKRULED'][y] for y in ys], xs), sp([M['PBUILT'][y] for y in ys], xs),
         sp([M['PBUILT'][y] for y in ys], xs) - sp([M['OKRULED'][y] for y in ys], xs)))
    P()

open(os.path.join(HERE, 'CD_WCORR_out.txt'), 'w').write('\n'.join(OUT) + '\n')
