#!/usr/bin/env python3
"""ORDER 33 W1 -- NAMED ROWS: what the proposed deep curve does to the CURRENT BOARD's mid-career
rows (PREREG_W1.md s7). Inputs: the seat brief's cand31.json (per-row g/beta/v0/rho/Phi/cand of the
candidate board). Repricing is the law's own algebra:

    price_new = price + rho(g) * Phi(g,s) * (beta_new(g) - beta_old(g)) * v0        (non-pool rows)

beta_old is CROSS-CHECKED against the row's own carried `beta` field (must agree to <1e-9 -- the
row's beta IS the wired curve read at its g) before any repriced number is reported.
"""
import os, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'

WIRED = [(2.5, 0.2878886216033701), (10.5, 0.2878886216033701), (25.5, 0.21772876584106796),
         (53.0, 0.14155152291809878), (85.5, 0.023849021706229417)]
PROP = [(2.5, 0.2878886216033701), (10.5, 0.2878886216033701), (25.5, 0.21772876584106796),
        (53.0, 0.21772876584106796), (85.5, 0.015157500325177839)]

def loglin(pts, g):
    g = max(1e-9, float(g))
    if g <= pts[0][0]: return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0.0 or y1 <= 0.0: return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]

D = json.load(open(os.path.join(SP, 'cand31.json')))
ROWS = D['rows']
OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

P('ORDER 33 W1 -- the proposed curve on the CURRENT BOARD (cand31.json, %d rows)' % len(ROWS))
mism = 0
tab = []
for r in ROWS:
    if r.get('pool'):
        continue
    g = float(r['g'])
    b_old = loglin(WIRED, g)
    if abs(b_old - float(r['beta'])) > 1e-9:
        mism += 1; continue
    b_new = loglin(PROP, g)
    d = r['rho'] * r['Phi'] * (b_new - b_old) * r['v0']
    tab.append(dict(key=r['key'], name=r['name'], pos=r['pos'], pick=r.get('pick'), age=r['age'],
                    g=g, rho=r['rho'], Phi=r['Phi'], v0=r['v0'], beta_old=b_old, beta_new=b_new,
                    cand=r['cand'], cand_new=r['cand'] + d, delta=d,
                    pct=(100.0 * d / r['cand']) if r['cand'] else None))
P('  beta cross-check: %d non-pool rows, %d beta-field mismatches (must be 0)' % (len(tab), mism))
assert mism == 0, 'row beta fields disagree with the wired curve'

mid = [t for t in tab if 40 <= t['g'] <= 90]
up = [t for t in tab if t['delta'] > 0.5]
dn = [t for t in tab if t['delta'] < -0.5]
P('  rows moved up >0.5pt: %d   down >0.5pt: %d   unmoved (g<=25.5 or beta unchanged): %d'
  % (len(up), len(dn), len(tab) - len(up) - len(dn)))
P('')
P('  40 <= g <= 90 board rows (%d), by delta:' % len(mid))
P('  %-26s %-4s %4s %5s %6s %6s %8s %8s %8s %8s %7s' %
  ('name', 'pos', 'pick', 'g', 'b_old', 'b_new', 'v0', 'cand', 'cand_W1', 'delta', 'pct'))
for t in sorted(mid, key=lambda x: -x['delta']):
    P('  %-26s %-4s %4s %5.0f %6.3f %6.3f %8.0f %8.0f %8.0f %+8.1f %+6.1f%%' %
      (t['name'][:26], t['pos'], t['pick'] or '-', t['g'], t['beta_old'], t['beta_new'],
       t['v0'], t['cand'], t['cand_new'], t['delta'], t['pct'] or 0))

json.dump(dict(order='ORDER 33 W1 named rows', proposed=PROP, wired=WIRED,
               n_rows=len(tab), n_mid=len(mid), rows=tab),
          open(os.path.join(HERE, 'NAMED_ROWS_W1.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'NAMED_ROWS_W1_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('\nwritten: NAMED_ROWS_W1.json / NAMED_ROWS_W1_out.txt')
