#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PARTS C and D. Decompose every class's year-0->1 mark move into rows.

The mark is sum(year-1 price) / sum(year-0 price). The year-0 sum is bit-identical on both boards
(proved in CD_REPRO_out.txt), so a class's move is exactly the sum of its rows' year-1 price moves
divided by that one shared denominator. Every row's contribution is therefore additive and exact.

Each row also carries the two charges, recomputed from the published constants, so the ORDER K and
ORDER P charge on a named row can be read beside its price move.
"""
import sys, os, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

G0 = 9.8900000000000077
LAMBDA = 0.17438330365754029
THETA_R = 0.65743851737411818
S0 = -2.4527208914690739
TMAX = 21.123281548845981
ETA, GAMMA_D = 0.50, 14.0


def A(g):
    return 1.0 - math.exp(-g / G0)


def T(s):
    return max(0.0, min(TMAX, 1.0 - THETA_R * (s - S0)))


def chargeK(g):
    return max(0.0, 1.0 - ETA * ((g / GAMMA_D) * math.exp(1.0 - g / GAMMA_D)))


def chargeP(g, s):
    return math.exp(-LAMBDA * A(g) * T(s))


K = {r['key']: r for r in L.load('OKRULED')}
Pm = {r['key']: r for r in L.load('PBUILT')}
perK, wend = L.rowset(list(K.values()))

ROWS = collections.defaultdict(list)
for y in L.ALLC:
    for r in perK.get(y, []):
        v1k = L.year1_price(r, y, wend)
        if v1k is None:
            continue
        rp = Pm[r['key']]
        v1p = L.year1_price(rp, y, wend)
        cg = sum(float(s['games']) for s in r['seasons'] if s['year'] <= y and (s.get('games') or 0) > 0)
        g1 = float((L.season_of(r, y) or {}).get('games') or 0.0)
        avg1 = (L.season_of(r, y) or {}).get('avg')
        age = L.age_at(r, y)
        sa = L.surplus(r, y, lambda p, a, v: L.age_bar(p, a))
        sp = L.surplus(r, y, L.ped_bar)
        ROWS[y].append(dict(key=r['key'], player=r['player'], typ=r['type'], pick=r.get('pick'),
                            pos=r.get('pos'), v0=float(r['v0']), age_draft=r.get('age_draft'),
                            age=age, cg=cg, g1=g1, avg1=avg1, sa=sa, sp=sp,
                            v1k=v1k, v1p=v1p, d=v1p - v1k,
                            cK=chargeK(cg), cP=(chargeP(cg, sp) if (sp is not None and age is not None and age < 24) else None)))

DEN = {y: sum(x['v0'] for x in ROWS[y]) for y in ROWS}
MOVE = {y: sum(x['d'] for x in ROWS[y]) / DEN[y] for y in ROWS}

P('=' * 118)
P('C1 — CONCENTRATION. How much of each class\'s move comes from its biggest movers?')
P('=' * 118)
P('  move = sum of row year-1 price moves / the class year-0 denominator (shared, bit-identical).')
P('  shares are of the NET move. movers = rows whose year-1 price moved by more than 0.05 points.')
P()
P('  %-6s %8s %6s %7s %8s %8s %8s %8s %8s' %
  ('class', 'move', 'rows', 'movers', 'top1', 'top3', 'top5', 'top10', 'grosspos'))
CONC = {}
for y in L.W2:
    rs = sorted(ROWS[y], key=lambda z: -abs(z['d']))
    mv = [x for x in rs if abs(x['d']) > 0.05]
    net = sum(x['d'] for x in rs)
    pos = sum(x['d'] for x in rs if x['d'] > 0)
    def sh(k):
        return sum(x['d'] for x in rs[:k]) / net if net else float('nan')
    CONC[y] = dict(move=MOVE[y], rows=len(rs), movers=len(mv), top1=sh(1), top3=sh(3), top5=sh(5),
                   top10=sh(10), grosspos=pos / DEN[y])
    P('  %-6d %+8.4f %6d %7d %7.1f%% %7.1f%% %7.1f%% %7.1f%% %+8.4f' %
      (y - 1, MOVE[y], len(rs), len(mv), 100 * sh(1), 100 * sh(3), 100 * sh(5), 100 * sh(10), pos / DEN[y]))
P()

P('=' * 118)
P('C2 — THE ROWS THAT DRIVE EACH BREACH CLASS, AND THE 2013 CONTROL. Top 8 movers by |price move|.')
P('=' * 118)
for y in (2016, 2012, 2011, 2014):
    P()
    P('  DRAFT CLASS %d (cohort %d)  ORDER K %.4f -> ORDER P %.4f  move %+.4f   denominator %.1f'
      % (y - 1, y, sum(x['v1k'] for x in ROWS[y]) / DEN[y], sum(x['v1p'] for x in ROWS[y]) / DEN[y],
         MOVE[y], DEN[y]))
    P('  %-24s %-4s %4s %5s %7s %4s %5s %6s %7s %7s %9s %9s %8s %7s %6s %6s' %
      ('player', 'type', 'pick', 'pos', 'v0', 'g1', 'ppg1', 'age', 'surpAGE', 'surpPED',
       'v1 ORDER K', 'v1 ORDER P', 'move', 'shr', 'chgK', 'chgP'))
    rs = sorted(ROWS[y], key=lambda z: -abs(z['d']))
    net = sum(x['d'] for x in rs)
    for x in rs[:8]:
        P('  %-24s %-4s %4s %5s %7.1f %4.0f %5s %6s %7s %7s %9.1f %9.1f %+8.1f %6.1f%% %6s %6s' %
          (x['player'][:24], x['typ'], (x['pick'] if x['pick'] is not None else '-'), x['pos'] or '-',
           x['v0'], x['g1'], ('%.1f' % x['avg1']) if x['avg1'] is not None else 'n/a',
           x['age'] if x['age'] is not None else 'n/a',
           ('%+.2f' % x['sa']) if x['sa'] is not None else 'null',
           ('%+.2f' % x['sp']) if x['sp'] is not None else 'null',
           x['v1k'], x['v1p'], x['d'], 100 * x['d'] / net if net else float('nan'),
           '%.3f' % x['cK'], ('%.3f' % x['cP']) if x['cP'] is not None else 'n/a'))
    other = sum(z['d'] for z in rs[8:])
    P('  ... the other %d rows contribute %+.1f points in total = %.1f%% of the move'
      % (len(rs) - 8, other, 100 * other / net if net else float('nan')))

json.dump(dict(move={str(k): v for k, v in MOVE.items()},
               den={str(k): v for k, v in DEN.items()},
               conc={str(k): v for k, v in CONC.items()},
               rows={str(k): v for k, v in ROWS.items()}),
          open(os.path.join(HERE, 'CD_DECOMP.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CD_DECOMP_out.txt'), 'w').write('\n'.join(OUT) + '\n')
