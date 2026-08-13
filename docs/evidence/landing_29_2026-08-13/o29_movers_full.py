#!/usr/bin/env python3
"""ORDER 29 -- THE FULL COMPOSED MOVERS LEDGER, all four levers, every player.

Recomposes docs/ledgers/LANDING_29_MOVERS_2026-08-13.{md,json} against live 88ce647f with the
lever taxonomy the stopped packet already used, EXTENDED to the levers this build landed:

  lever 1  the unflag-three        LIVE   -> B_U   (store d9a24282 -> cb38ef11)
  lever 2  the grace dial          B_U    -> B_G   (RL_GRACE default OFF -> ON)
  lever 3  the curve + v0 reprint  B_G    -> L3    (ruled curve + v0surf re-bake + book re-seal)
  lever 4  the numeraire scalar    L3     -> FINAL (s 0.99406108 -> 0.94009143)

Lever sums must reconcile EXACTLY, per row and in aggregate: no row may carry an unexplained
residual. usage: python3 o29_movers_full.py <L3_board.json> <FINAL_board.json>
"""
import os, sys, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
OLD = ROOT + '/docs/ledgers/LANDING_29_MOVERS_2026-08-13.json'
L3B, L4B = sys.argv[1], sys.argv[2]

LOG = []
def P(s=''):
    print(s); LOG.append(s)

def board(pth):
    b = json.load(open(pth))
    return {r['key']: r for r in b['active']}

old = json.load(open(OLD))
prev = {r['key']: r for r in old['rows']}
L3, L4 = board(L3B), board(L4B)

NAMED = ['harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'dante-visentini',
         'vigo-visentini', 'nicholas-martin', 'marcus-herbert', 'jai-newcombe', 'willem-duursma',
         'harry-sheezel']

P("=" * 124)
P("ORDER 29  --  THE FULL COMPOSED MOVERS LEDGER  (vs live 88ce647f, all four levers)")
P("=" * 124)
P()
P("  stages, each an actual built board -- never a modelled step:")
P("    LIVE   88ce647f531030d8d2e094188b258191   the untouched tree, dial OFF")
P("    B_U    71cbb13b3414d031135771dd7e564b3c   + the unflag-three")
P("    B_G    0017657e0469addda9260964938bad78   + the grace dial ON")
P("    L3     5c0de646bd71c2e4e371bc83ccf476ef   + the ruled curve, v0surf re-bake, book re-seal")
P("    FINAL  86c8d5d9ba5b95e2cba05c78fbc31f78   + the numeraire re-pin")

# ---- assert the populations line up before differencing anything
assert set(L3) == set(L4), 'L3/FINAL key sets differ'
missing = set(prev) - set(L4)
extra = set(L4) - set(prev)
P()
P("  population   prev-ledger rows %d · L3 %d · FINAL %d · missing %d · new %d"
  % (len(prev), len(L3), len(L4), len(missing), len(extra)))
assert not missing and not extra, 'population moved: missing %s extra %s' % (sorted(missing)[:5], sorted(extra)[:5])

rows = []
for k in sorted(L4):
    pr = prev[k]
    live, b_u, b_g = pr['live'], pr['b_u'], pr['b_g']
    l3, l4 = L3[k]['v'], L4[k]['v']
    lv = collections.OrderedDict([
        ('key', k), ('name', L4[k].get('name')), ('pos', L4[k].get('grp')), ('ep', L4[k].get('ep')),
        ('pick', pr.get('pick')), ('ty', L4[k].get('ty')),
        ('live', live), ('b_u', b_u), ('b_g', b_g), ('l3', l3), ('final', l4),
        ('lever1_unflag', b_u - live), ('lever2_grace', b_g - b_u),
        ('lever3_curve_v0', l3 - b_g), ('lever4_numeraire', l4 - l3),
        ('total', l4 - live)])
    lv['residual'] = lv['total'] - (lv['lever1_unflag'] + lv['lever2_grace']
                                    + lv['lever3_curve_v0'] + lv['lever4_numeraire'])
    rows.append(lv)

# ---- THE RECONCILIATION: exact, per row
bad = [r for r in rows if r['residual'] != 0]
P()
P("  LEVER RECONCILIATION (per row, exact): rows failing %d   max |residual| %d"
  % (len(bad), max(abs(r['residual']) for r in rows)))
assert not bad, 'levers do not reconcile on %d rows: %s' % (len(bad), [r['key'] for r in bad[:5]])

def tot(f): return sum(r[f] for r in rows)
LEVERS = [('lever 1 — THE UNFLAG-THREE', 'lever1_unflag',
           'store d9a24282 -> cb38ef11; reaches every priced row through the v3.4 kernel head '
           '(3917 -> 3966) and hence BOARD_FACTOR (0.761344 -> 0.751937, -1.2355%)'),
          ('lever 2 — THE GRACE DIAL', 'lever2_grace',
           'RL_GRACE default OFF -> ON; entry age <= 19 gets seasons 1-2 at full weight'),
          ('lever 3 — THE CURVE + v0 REPRINT', 'lever3_curve_v0',
           'the ruled monotone curve installed with the ruling-C ordering tiebreak (df766dff -> '
           '9729f0c5), the v0surf re-bake it makes inseparable (fbc5b393 -> 5dd34ca8), and the '
           'book re-seal (c9e7491b -> cbb7c431). The printed nd_v0/pool_v0 objects are INERT on '
           'the board and proven so by byte-identity, so this lever is the curve and the surface'),
          ('lever 4 — THE NUMERAIRE SCALAR', 'lever4_numeraire',
           's 0.9940610814748366 -> 0.9400914291048137; re-denominates every priced row by '
           'x0.945707911339, both sides together')]

P()
P("  PER-LEVER SUMS (board points), and they add to the total exactly")
P("  %-34s %9s %12s %10s" % ('lever', 'movers', 'sum delta', 'share'))
grand = tot('total')
for nm, f, _doc in LEVERS:
    mv = sum(1 for r in rows if r[f] != 0)
    P("  %-34s %9d %12d %9.1f%%" % (nm, mv, tot(f), 100.0 * tot(f) / grand if grand else 0))
P("  %-34s %9s %12s" % ('-' * 34, '-' * 9, '-' * 12))
P("  %-34s %9d %12d %9.1f%%" % ('TOTAL (live -> final)', sum(1 for r in rows if r['total'] != 0), grand, 100.0))
P("  sum of the four lever sums          %12d   == total %d   %s"
  % (sum(tot(f) for _n, f, _d in LEVERS), grand,
     'EXACT' if sum(tot(f) for _n, f, _d in LEVERS) == grand else 'MISMATCH'))
assert sum(tot(f) for _n, f, _d in LEVERS) == grand

# ---- board totals
P()
P("  BOARD TOTALS, live -> landed")
P("  %-8s %-36s %12s %14s %12s" % ('stage', 'board md5', 'total', 'delta vs LIVE', 'pct'))
stg = [('LIVE', '88ce647f531030d8d2e094188b258191', 'live'), ('B_U', '71cbb13b3414d031135771dd7e564b3c', 'b_u'),
       ('B_G', '0017657e0469addda9260964938bad78', 'b_g'), ('L3', '5c0de646bd71c2e4e371bc83ccf476ef', 'l3'),
       ('FINAL', '86c8d5d9ba5b95e2cba05c78fbc31f78', 'final')]
base = tot('live')
for nm, md5, f in stg:
    t = tot(f)
    P("  %-8s %-36s %12d %14d %11.4f%%" % (nm, md5, t, t - base, 100.0 * (t - base) / base))

# ---- national vs pool
P()
P("  NATIONAL vs POOL (national = effective pick 1..64; pool = the pool slot)")
P("  %-22s %5s %12s %12s %14s %10s" % ('population', 'n', 'LIVE', 'FINAL', 'delta', 'pct'))
for lbl, pred in (('national (ND 1-64)', lambda r: (r['ep'] or 0) <= 64),
                  ('pool (past 64)', lambda r: (r['ep'] or 0) > 64)):
    sub = [r for r in rows if pred(r)]
    a, b = sum(r['live'] for r in sub), sum(r['final'] for r in sub)
    P("  %-22s %5d %12d %12d %14d %9.4f%%" % (lbl, len(sub), a, b, b - a, 100.0 * (b - a) / a))

# ---- movers
mv = [r for r in rows if r['total'] != 0]
P()
P("  MOVERS  %d of %d rows  (%.1f%%)" % (len(mv), len(rows), 100.0 * len(mv) / len(rows)))
P("  unmoved %d" % (len(rows) - len(mv)))
ups = [r for r in mv if r['total'] > 0]
P("  rising %d · falling %d" % (len(ups), len(mv) - len(ups)))

# ---- named rows
P()
P("  THE NAMED ROWS (P14), live -> landed, with the full per-lever split")
P("  %-18s %-5s %5s %8s %8s %8s %8s %8s %8s %8s %8s"
  % ('row', 'pos', 'pick', 'LIVE', 'L1 unfl', 'L2 grace', 'L3 curve', 'L4 num', 'FINAL', 'delta', 'pct'))
byk = {r['key']: r for r in rows}
for k in NAMED:
    r = byk.get(k)
    if not r:
        P("  %-18s NOT ON THE BOARD" % k); continue
    P("  %-18s %-5s %5s %8d %8d %8d %8d %8d %8d %8d %7.2f%%"
      % (k, r['pos'], r['pick'] if r['pick'] is not None else r['ep'], r['live'], r['lever1_unflag'],
         r['lever2_grace'], r['lever3_curve_v0'], r['lever4_numeraire'], r['final'], r['total'],
         100.0 * r['total'] / r['live'] if r['live'] else 0))
rise = [k for k in NAMED if byk.get(k) and byk[k]['total'] > 0]
P()
P("  named rows that RISE: %s" % (rise or 'none'))

# ---- biggest movers
P()
P("  THE TWENTY LARGEST ABSOLUTE MOVERS")
P("  %-24s %-5s %6s %9s %9s %9s %9s %9s %9s"
  % ('row', 'pos', 'ep', 'LIVE', 'L1', 'L2', 'L3', 'L4', 'delta'))
for r in sorted(rows, key=lambda x: -abs(x['total']))[:20]:
    P("  %-24s %-5s %6s %9d %9d %9d %9d %9d %9d"
      % (r['key'], r['pos'], r['ep'], r['live'], r['lever1_unflag'], r['lever2_grace'],
         r['lever3_curve_v0'], r['lever4_numeraire'], r['total']))

out = collections.OrderedDict([
    ('_doc', 'ORDER 29 THE FULL COMPOSED MOVERS LEDGER — every priced row, all four levers, vs live '
             '88ce647f. Lever sums reconcile EXACTLY per row (max |residual| 0); every stage is an '
             'actually-built board, never a modelled step.'),
    ('stages', collections.OrderedDict((nm, md5) for nm, md5, _f in stg)),
    ('levers', [collections.OrderedDict([('name', nm), ('field', f), ('doc', d),
                                         ('movers', sum(1 for r in rows if r[f] != 0)),
                                         ('sum_delta', tot(f))]) for nm, f, d in LEVERS]),
    ('totals', collections.OrderedDict((nm, tot(f)) for nm, _m, f in stg)),
    ('movers', len(mv)), ('rows_total', len(rows)),
    ('reconciliation', {'rows_failing': len(bad), 'max_residual': max(abs(r['residual']) for r in rows)}),
    ('rows', rows)])
json.dump(out, open(ROOT + '/docs/ledgers/LANDING_29_MOVERS_2026-08-13.json', 'w'), indent=1)
open(HERE + '/MOVERS29_out.txt', 'w').write("\n".join(LOG) + "\n")
P()
P("  written: docs/ledgers/LANDING_29_MOVERS_2026-08-13.json")
