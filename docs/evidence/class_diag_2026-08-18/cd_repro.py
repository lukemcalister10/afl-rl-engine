#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART E FIRST. Reproduce op_class.py's marks off the same matrices, then open
the instrument up: exactly which rows sit in the year-0 denominator and the year-1 numerator for
each class, and whether 2015 is counted differently from any other class.
"""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

BOARDS = [('O35FINAL', 'landing candidate 1f176444'),
          ('OKRULED', 'ORDER K f3101883'),
          ('PBUILT', 'ORDER P 374d4e44')]
M = {t: L.load(t) for t, _ in BOARDS}
marks = {}
for t, _ in BOARDS:
    marks[t], wend = L.class_marks(M[t])

P('=' * 110)
P('E1 — INSTRUMENT REPRODUCTION. My arithmetic against op_class.py\'s published CLASS_P_out.txt.')
P('=' * 110)
PUB_K = {2006:0.8562,2007:1.0579,2008:1.0713,2009:1.0063,2010:1.0432,2011:1.1359,2012:1.1363,
         2013:1.0673,2014:1.0535,2015:1.0300,2016:1.1060}
PUB_P = {2006:0.8230,2007:1.0155,2008:1.0378,2009:1.0263,2010:1.0680,2011:1.1570,2012:1.1595,
         2013:1.0901,2014:1.0760,2015:1.0158,2016:1.2047}
P('  draft class  cohort   ORDER K mine/published      ORDER P mine/published')
worst = 0.0
for y in L.W2:
    a, b = marks['OKRULED'][y], marks['PBUILT'][y]
    da, db = abs(a - PUB_K[y]), abs(b - PUB_P[y])
    worst = max(worst, da, db)
    P('  %-12d %-7d %8.4f / %.4f  d=%.5f   %8.4f / %.4f  d=%.5f' % (y - 1, y, a, PUB_K[y], da, b, PUB_P[y], db))
P('  worst absolute disagreement over 22 published class marks: %.6f' % worst)
P('  -> %s' % ('REPRODUCED' if worst < 5e-5 else 'THE INSTRUMENT DISAGREES'))
w2k = sum(marks['OKRULED'][y] for y in L.W2) / 11.0
w2p = sum(marks['PBUILT'][y] for y in L.W2) / 11.0
P('  W2 mark  ORDER K %.4f (published 1.0513)   ORDER P %.4f (published 1.0613)' % (w2k, w2p))
P('  matrix last year with a price (wend) = %d' % wend)
P()

P('=' * 110)
P('E2 — THE DENOMINATOR AND THE NUMERATOR, CLASS BY CLASS. Is 2015 counted differently?')
P('=' * 110)
P('  cols: rows = eligible rows in the class (cohort readable, v0>0).')
P('        scored = rows that entered BOTH sums.  excluded = rows dropped by the pre-window rule.')
P('        zeroed = scored rows whose year-1 price is exactly 0 (ended or null), kept in the denominator.')
P('        sumv0 / sumv1 are the two sums the mark divides.')
P()
P('  %-6s %-6s %6s %7s %8s %7s %12s %12s %9s' %
  ('class', 'cohort', 'rows', 'scored', 'excluded', 'zeroed', 'sum v0 (K)', 'sum v1 (K)', 'mark K'))
per, _ = L.rowset(M['OKRULED'])
E2 = {}
for y in L.ALLC:
    pop = per.get(y, [])
    sc = exc = zer = 0
    s0 = s1 = 0.0
    for r in pop:
        v1 = L.year1_price(r, y, wend)
        if v1 is None:
            exc += 1; continue
        sc += 1; s0 += float(r['v0']); s1 += v1
        if v1 == 0.0:
            zer += 1
    E2[y] = dict(rows=len(pop), scored=sc, excluded=exc, zeroed=zer, sumv0=s0, sumv1=s1)
    tag = '  <== registered W2 basis' if y in L.W2 else ''
    P('  %-6s %-6d %6d %7d %8d %7d %12.1f %12.1f %9.4f%s' %
      (y - 1, y, len(pop), sc, exc, zer, s0, s1, (s1 / s0) if s0 else float('nan'), tag))
P()
P('  the same denominator on the ORDER P matrix (v0 must be identical — day-0 prices did not move):')
perP, _ = L.rowset(M['PBUILT'])
mx = 0.0
for y in L.ALLC:
    s0 = sum(float(r['v0']) for r in perP.get(y, []) if L.year1_price(r, y, wend) is not None)
    mx = max(mx, abs(s0 - E2[y]['sumv0']))
P('  worst difference in any class year-0 denominator, ORDER K vs ORDER P: %.6f' % mx)
P('  worst difference in scored-row COUNT: %d' %
  max(abs(sum(1 for r in perP.get(y, []) if L.year1_price(r, y, wend) is not None) - E2[y]['scored'])
      for y in L.ALLC))
P()

# composition of every class, for part C/D
P('=' * 110)
P('E3 — CLASS COMPOSITION. Size, route mix, pick mix, entry-age mix, share who played year 1.')
P('=' * 110)
P('  %-6s %5s %5s %5s %6s %6s %7s %8s %8s %8s %8s' %
  ('class', 'rows', 'ND', 'pool', 'p1-10', 'p1-20', 'played1', 'meanv0', 'maxv0', 'top1sh', 'top5sh'))
COMP = {}
for y in L.ALLC:
    pop = [r for r in per.get(y, []) if L.year1_price(r, y, wend) is not None]
    nd = [r for r in pop if r.get('type') == 'ND']
    p10 = sum(1 for r in nd if (r.get('pick') or 99) <= 10)
    p20 = sum(1 for r in nd if (r.get('pick') or 99) <= 20)
    pl1 = sum(1 for r in pop if L.season_of(r, y))
    v0s = sorted((float(r['v0']) for r in pop), reverse=True)
    tot = sum(v0s)
    COMP[y] = dict(rows=len(pop), nd=len(nd), pool=len(pop) - len(nd), p10=p10, p20=p20,
                   played1=pl1, played1_sh=pl1 / len(pop), meanv0=tot / len(pop), maxv0=v0s[0],
                   top1sh=v0s[0] / tot, top5sh=sum(v0s[:5]) / tot, sumv0=tot)
    P('  %-6s %5d %5d %5d %6d %6d %6.1f%% %8.1f %8.1f %7.1f%% %7.1f%%' %
      (y - 1, len(pop), len(nd), len(pop) - len(nd), p10, p20, 100 * pl1 / len(pop),
       tot / len(pop), v0s[0], 100 * v0s[0] / tot, 100 * sum(v0s[:5]) / tot))

json.dump(dict(marks={k: {str(a): b for a, b in v.items()} for k, v in marks.items()},
               E2={str(k): v for k, v in E2.items()},
               COMP={str(k): v for k, v in COMP.items()}, wend=wend),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CD_REPRO.json'), 'w'),
          indent=1, default=float)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CD_REPRO_out.txt'), 'w').write('\n'.join(OUT) + '\n')
