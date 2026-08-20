#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART D. Why the 2015 draft class and not the others.

Everything here is v0-WEIGHTED, because the class mark is a ratio of sums: a row's influence on the
mark is its year-0 price, not its head count.
"""
import sys, os, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

D = json.load(open(os.path.join(HERE, 'CD_DECOMP.json')))
ROWS = {int(k): v for k, v in D['rows'].items()}
DEN = {int(k): v for k, v in D['den'].items()}
MOVE = {int(k): v for k, v in D['move'].items()}

P('=' * 124)
P('D1 — UP AND DOWN, SEPARATELY. The net move hides which side changed.')
P('=' * 124)
P('  gross up   = sum of the year-1 price RISES over the class denominator')
P('  gross down = sum of the year-1 price FALLS over the same denominator')
P()
P('  %-6s %9s %10s %10s %10s %8s %8s' %
  ('class', 'net move', 'gross up', 'gross down', 'up/|down|', 'n up', 'n down'))
S = {}
for y in L.W2:
    rs = ROWS[y]
    up = sum(x['d'] for x in rs if x['d'] > 0) / DEN[y]
    dn = sum(x['d'] for x in rs if x['d'] < 0) / DEN[y]
    nu = sum(1 for x in rs if x['d'] > 0.05); nd = sum(1 for x in rs if x['d'] < -0.05)
    S[y] = dict(up=up, dn=dn, nu=nu, nd=nd)
    P('  %-6d %+9.4f %+10.4f %+10.4f %10s %8d %8d' %
      (y - 1, MOVE[y], up, dn, ('%.2f' % (up / abs(dn))) if dn else 'inf', nu, nd))
P()
P('  READ: 2015 is not the class with the biggest RISE. It is the class with almost no FALL.')
P()

P('=' * 124)
P('D2 — WHERE THE CLASS SITS AGAINST THE TWO BARS, v0-WEIGHTED.')
P('=' * 124)
P('  surpAGE = games-weighted (season average - S1 age bar) to the year-1 season.')
P('  surpPED = the same against the age bar PLUS the measured pedigree premium PG(ln v0, class).')
P('  the ORDER P charge is a falling function of surpPED, so a class whose PRICE-WEIGHT sits above')
P('  its pedigree bar is relieved and a class whose price-weight sits below it is charged harder.')
P()
P('  %-6s %10s %10s %10s %10s %10s %10s' %
  ('class', 'w-surpAGE', 'w-surpPED', 'w-shr PED+', 'w-shr AGE+', 'w-chargeK', 'w-chargeP'))
W = {}
for y in L.W2:
    rs = [x for x in ROWS[y] if x['sp'] is not None and x['age'] is not None and x['age'] < 24]
    tot = sum(x['v0'] for x in rs)
    wa = sum(x['v0'] * x['sa'] for x in rs) / tot
    wp = sum(x['v0'] * x['sp'] for x in rs) / tot
    sp_ = sum(x['v0'] for x in rs if x['sp'] > 0) / tot
    sa_ = sum(x['v0'] for x in rs if x['sa'] > 0) / tot
    ck = sum(x['v0'] * x['cK'] for x in rs) / tot
    cp = sum(x['v0'] * x['cP'] for x in rs) / tot
    W[y] = dict(wa=wa, wp=wp, sp=sp_, sa=sa_, ck=ck, cp=cp, cov=tot / DEN[y], n=len(rs))
    P('  %-6d %+10.2f %+10.2f %9.1f%% %9.1f%% %10.3f %10.3f' % (y - 1, wa, wp, 100 * sp_, 100 * sa_, ck, cp))
P()
P('  coverage: share of the class year-0 denominator these rows carry (the rest have no readable')
P('  surplus or were 24+ at the year priced, and keep the OLD charge unchanged):')
P('  ' + '  '.join('%d %.0f%%' % (y - 1, 100 * W[y]['cov']) for y in L.W2))
P()

P('=' * 124)
P('D3 — THE ROWS THE NEW CHARGE MOST RELIEVES: near the OLD charge\'s worst point AND above the')
P('     pedigree bar. The old charge bottoms out at exactly 14 career games.')
P('=' * 124)
P('  v0-weighted share of each class in each cell. "8-24 g" = career games at the year-1 season.')
P()
P('  %-6s %12s %12s %12s %12s %12s' %
  ('class', '8-24g & PED+', '8-24g & PED-', '<8g', '>24g', 'no s / 24+'))
for y in L.W2:
    tot = DEN[y]
    a = b = c = d = e = 0.0
    for x in ROWS[y]:
        if x['sp'] is None or x['age'] is None or x['age'] >= 24:
            e += x['v0']; continue
        if x['cg'] < 8:
            c += x['v0']
        elif x['cg'] > 24:
            d += x['v0']
        elif x['sp'] > 0:
            a += x['v0']
        else:
            b += x['v0']
    P('  %-6d %11.1f%% %11.1f%% %11.1f%% %11.1f%% %11.1f%%'
      % (y - 1, 100 * a / tot, 100 * b / tot, 100 * c / tot, 100 * d / tot, 100 * e / tot))
P()

P('=' * 124)
P('D4 — THE EXPENSIVE END. Rows with v0 >= 1000, which carry most of the denominator.')
P('=' * 124)
P('  %-6s %5s %9s %10s %11s %11s %12s' %
  ('class', 'n>=1k', 'shr den', 'w-surpPED', 'shr PED+', 'move share', 'mean g yr1'))
for y in L.W2:
    rs = [x for x in ROWS[y] if x['v0'] >= 1000]
    tot = sum(x['v0'] for x in rs)
    have = [x for x in rs if x['sp'] is not None]
    wp = sum(x['v0'] * x['sp'] for x in have) / sum(x['v0'] for x in have) if have else float('nan')
    sp_ = sum(x['v0'] for x in have if x['sp'] > 0) / sum(x['v0'] for x in have) if have else float('nan')
    ms = sum(x['d'] for x in rs) / DEN[y]
    P('  %-6d %5d %8.1f%% %+10.2f %10.1f%% %+11.4f %12.2f'
      % (y - 1, len(rs), 100 * tot / DEN[y], wp, 100 * sp_, ms, sum(x['g1'] for x in rs) / len(rs)))
P()
P('  ... and the same rows\' share of the class NET move:')
for y in L.W2:
    rs = [x for x in ROWS[y] if x['v0'] >= 1000]
    ms = sum(x['d'] for x in rs) / DEN[y]
    P('    %d: %+0.4f of %+0.4f = %.0f%%' % (y - 1, ms, MOVE[y], 100 * ms / MOVE[y] if MOVE[y] else float('nan')))
P()

P('=' * 124)
P('D5 — DATA-ARTIFACT SWEEP on the same eleven classes.')
P('=' * 124)
P('  %-6s %6s %8s %9s %10s %10s %9s %9s' %
  ('class', 'rows', 'no age', 'no v0', 'no seas', 'yr1 gap', 'age!=18/19', 'null s_P'))
for y in L.W2:
    rs = ROWS[y]
    noage = sum(1 for x in rs if x['age'] is None)
    nos = sum(1 for x in rs if x['g1'] == 0)
    odd = sum(1 for x in rs if x['age'] is not None and x['age'] not in (18, 19))
    nul = sum(1 for x in rs if x['sp'] is None)
    P('  %-6d %6d %8d %9d %10s %10d %9d %9d'
      % (y - 1, len(rs), noage, 0, 'n/a', nos, odd, nul))
P()
P('  entry-age mix (age at the year-1 season), v0-weighted share:')
P('  %-6s' % 'class' + ''.join('%8s' % ('age %d' % a) for a in (18, 19, 20, 21, 22, 23)) + '%8s' % '24+')
for y in L.W2:
    tot = DEN[y]
    sh = collections.defaultdict(float)
    for x in ROWS[y]:
        a = x['age']
        sh['24+' if (a is None or a >= 24) else a] += x['v0']
    P('  %-6d' % (y - 1) + ''.join('%7.1f%%' % (100 * sh[a] / tot) for a in (18, 19, 20, 21, 22, 23))
      + '%7.1f%%' % (100 * sh['24+'] / tot))

json.dump(dict(S={str(k): v for k, v in S.items()}, W={str(k): v for k, v in W.items()}),
          open(os.path.join(HERE, 'CD_WHY.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CD_WHY_out.txt'), 'w').write('\n'.join(OUT) + '\n')

# ---- D6, appended: the top of the draft, class by class -------------------------------------------
O2 = []
def Q(s=''):
    print(s); O2.append(str(s))

Q()
Q('=' * 124)
Q('D6 — THE TOP TEN PICKS OF EACH CLASS. The rows the mark weights most.')
Q('=' * 124)
Q('  %-6s %5s %8s %9s %10s %10s %9s %10s' %
  ('class', 'n1-10', 'played1', 'mean g1', 'mean ppg1', 'mn surpAGE', 'mn surpPED', 'move share'))
for y in L.W2:
    rs = [x for x in ROWS[y] if x['typ'] == 'ND' and (x['pick'] or 99) <= 10]
    pl = [x for x in rs if x['g1'] > 0]
    have = [x for x in rs if x['sp'] is not None]
    ms = sum(x['d'] for x in rs) / DEN[y]
    Q('  %-6d %5d %7.0f%% %9.2f %10s %10s %9s %+10.4f'
      % (y - 1, len(rs), 100 * len(pl) / len(rs), sum(x['g1'] for x in rs) / len(rs),
         ('%.1f' % (sum(x['g1'] * x['avg1'] for x in pl) / sum(x['g1'] for x in pl))) if pl else 'n/a',
         ('%+.2f' % (sum(x['sa'] for x in have) / len(have))) if have else 'n/a',
         ('%+.2f' % (sum(x['sp'] for x in have) / len(have))) if have else 'n/a', ms))
open(os.path.join(HERE, 'CD_WHY_out.txt'), 'a').write('\n'.join(O2) + '\n')
