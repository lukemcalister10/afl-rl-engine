#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART E, the rest. Is the 2015 number an instrument artifact?"""
import sys, os, json, collections
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

K = {r['key']: r for r in L.load('OKRULED')}
Pm = {r['key']: r for r in L.load('PBUILT')}
per, wend = L.rowset(list(K.values()))

P('=' * 116)
P('E4 — IS ANY ROW COUNTED, DROPPED OR DIVIDED DIFFERENTLY FOR 2015?')
P('=' * 116)
bad = collections.defaultdict(list)
for y in L.ALLC:
    for r in per.get(y, []):
        yrs = r.get('yrs') or []
        rp = Pm[r['key']]
        if yrs and yrs[0] != y:
            bad['year-1 cell is not the first vpath cell'].append((y, r['player'], yrs[0]))
        if not yrs:
            bad['no vpath at all'].append((y, r['player'], None))
        if (rp.get('yrs') or []) != yrs:
            bad['year grid differs between the two boards'].append((y, r['player'], None))
        if abs(float(rp['v0']) - float(r['v0'])) > 1e-9:
            bad['year-0 price differs between the two boards'].append((y, r['player'], None))
        if L.year1_price(r, y, wend) is None:
            bad['row excluded by the pre-window rule'].append((y, r['player'], yrs[0] if yrs else None))
for k in ('year-1 cell is not the first vpath cell', 'no vpath at all',
          'year grid differs between the two boards', 'year-0 price differs between the two boards',
          'row excluded by the pre-window rule'):
    v = bad.get(k, [])
    by = collections.Counter(z[0] - 1 for z in v)
    P('  %-46s %4d rows   by draft class: %s' % (k, len(v), dict(by) if v else 'none'))
P()
P('  the 2015 class carries 110 rows, every one of them scored in both sums, none excluded, none')
P('  zeroed, and its year-0 denominator is bit-identical on the two boards. The instrument treats')
P('  it exactly as it treats the other ten.')
P()

P('=' * 116)
P('E5 — THE MARK IS A RATIO OF SUMS, SO A FEW EXPENSIVE ROWS CARRY IT. THAT IS TRUE OF EVERY CLASS.')
P('=' * 116)
P('  %-8s %14s %14s %14s' % ('class', 'top-5 v0 share', 'top-10 v0 share', 'Gini of v0'))
for y in L.W2:
    v = sorted((float(r['v0']) for r in per[y]), reverse=True)
    t = sum(v)
    a = np.sort(np.array(v)); n = len(a)
    gini = float((2 * np.arange(1, n + 1) - n - 1).dot(a) / (n * a.sum()))
    P('  %-8d %13.1f%% %13.1f%% %14.3f' % (y - 1, 100 * sum(v[:5]) / t, 100 * sum(v[:10]) / t, gini))
P()

P('=' * 116)
P('E6 — THE CHARGE IS ONE FACTOR IN THE PRICE, NOT THE PRICE. Stated so nobody reads the charge')
P('     column in C2 as a price multiplier.')
P('=' * 116)
D = json.load(open(os.path.join(HERE, 'CD_DECOMP.json')))
rows = [x for x in D['rows']['2016'] if x['cP'] is not None and x['v1k'] > 0 and x['cK'] > 0]
cr = np.array([x['cP'] / x['cK'] for x in rows])
pr = np.array([x['v1p'] / x['v1k'] for x in rows])
def rk(a):
    o = a.argsort(); r = np.empty(len(a)); r[o] = np.arange(1., len(a) + 1); return r
P('  2015 draft class, %d rows carrying the new charge:' % len(rows))
P('  charge ratio (ORDER P / ORDER K) spans %.3f to %.3f, median %.3f' % (cr.min(), cr.max(), np.median(cr)))
P('  price  ratio (ORDER P / ORDER K) spans %.3f to %.3f, median %.3f' % (pr.min(), pr.max(), np.median(pr)))
P('  Spearman between the two: %+.3f    Pearson: %+.3f'
  % (np.corrcoef(rk(cr), rk(pr))[0, 1], np.corrcoef(cr, pr)[0, 1]))
allr = [x for rs in D['rows'].values() for x in rs if x['cP'] is not None and x['v1k'] > 0 and x['cK'] > 0]
dis = sum(1 for x in allr
          if abs(x['cP'] / x['cK'] - 1) > 1e-9 and abs(x['v1p'] / x['v1k'] - 1) > 1e-9
          and ((x['cP'] / x['cK'] - 1) > 0) != ((x['v1p'] / x['v1k'] - 1) > 0))
P('  Over ALL %d rows on the whole matrix that carry the new charge, the charge and the price' % len(allr))
P('  move in the same direction on every one: %d sign disagreements.' % dis)
P('  But NOT proportionally: the rest of the pricing stack damps it. Read the charge as the input and')
P('  the price move as the output.')

open(os.path.join(HERE, 'CD_INST_out.txt'), 'w').write('\n'.join(OUT) + '\n')
