#!/usr/bin/env python3
"""ORDER 25 -- THE SEPARATION ASSERTIONS, RUN BEFORE ANYTHING IS WRITTEN.

The owner's separation law (#334 comment 5255810874) in its measurable form: THE NATIONAL ARM DOES
NOT MOVE WHEN THE POOL IS REPRICED. This file asserts it on the board bytes and RAISES on a breach,
and it is run BEFORE the landing tree is touched -- so a breach stops the act rather than being
discovered after the pins have moved.

The pathway and is_pool definitions are CARRIED VERBATIM from ORDER 24B's o24b_table.py, which
carried them from ORDER 24's o24_table.py. They are the ENGINE's own classification read off the
board's `ty` and `pk` fields, so "national" here means exactly what it means everywhere else in this
chain: `ty == 'ND'` with pick <= 64. A pool ND>64 row is POOL and is expected to move.

  usage: o25_separation.py <landed_board.json> <live_board.json> <out.json> [label=path ...]
"""
import sys, json, hashlib, os

P = print
LANDED, LIVE, OUTJS = sys.argv[1], sys.argv[2], sys.argv[3]
EXTRA = [a.split('=', 1) for a in sys.argv[4:]]

TYMAP = {'National': 'ND', 'Rookie': 'RD', 'Mid-Season': 'MSD', 'Pre-Season': 'SSP',
         'Supplemental': 'SSP', 'Irish': 'IRE', 'Academy': 'PDA', 'Unrestricted': 'UNR'}
POOLSET = {'RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64'}


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


def pathway(r):
    t = r.get('ty') or TYMAP.get(r.get('draft')) or r.get('draft')
    if t == 'ND':
        return 'ND>64' if (r.get('pk') or 0) > 64 else 'ND 1-64'
    return t


def is_pool(r):
    return pathway(r) in POOLSET


def val(r):
    v = r.get('v')
    return int(v) if v is not None else 0


def load(p):
    D = json.load(open(p))
    return ({r.get('key') or r.get('name'): r for r in D['active']},
            {r.get('key') or r.get('name'): r for r in D.get('back', [])})


BOARDS = [('live', LIVE)] + [(k, v) for k, v in EXTRA] + [('landed', LANDED)]
B, BK, MD5 = {}, {}, {}
P("=" * 122)
P("ORDER 25 -- SEPARATION, BOARD TOTALS AND THE NAMED ROWS")
P("=" * 122)
for lab, path in BOARDS:
    B[lab], BK[lab] = load(path)
    MD5[lab] = md5(path)
    P("  %-10s %-34s md5 %s   active %d" % (lab, os.path.basename(path), MD5[lab], len(B[lab])))
P()

live = B['live']; landed = B['landed']
keys = sorted(live)
nd_keys = [k for k in keys if not is_pool(live[k])]
pool_keys = [k for k in keys if is_pool(live[k])]

# ---- THE SEPARATION LAW -- HARD ASSERT ----------------------------------------------------------
P("=" * 122)
P("THE SEPARATION LAW -- every national row (ty==ND, pick <= 64) identical to live %s" % MD5['live'])
P("=" * 122)
P("  national rows on the live board: %d    pool rows: %d" % (len(nd_keys), len(pool_keys)))
P()
P("  %-10s %12s %12s %14s %16s %16s" %
  ('board', 'ND movers', 'ND absent', 'ND value', 'pool value', 'total (active)'))
SEP = {}
for lab, _ in BOARDS:
    bl = B[lab]
    mv = [k for k in nd_keys if k in bl and val(bl[k]) != val(live[k])]
    ab = [k for k in nd_keys if k not in bl]
    ndv = sum(val(bl[k]) for k in nd_keys if k in bl)
    plv = sum(val(bl[k]) for k in pool_keys if k in bl)
    tot = sum(val(r) for r in bl.values())
    SEP[lab] = dict(nd_movers=len(mv), nd_absent=len(ab), nd_value=ndv, pool_value=plv, total=tot,
                    nd_mover_keys=mv[:50])
    P("  %-10s %12d %12d %14s %16s %16s"
      % (lab, len(mv), len(ab), format(ndv, ','), format(plv, ','), format(tot, ',')))
P()
bad = SEP['landed']
assert bad['nd_movers'] == 0 and bad['nd_absent'] == 0 and bad['nd_value'] == SEP['live']['nd_value'], \
    ("SEPARATION FAILED on the landed board: %d ND movers, %d absent, ND value %s vs %s"
     % (bad['nd_movers'], bad['nd_absent'], bad['nd_value'], SEP['live']['nd_value']))
P("  *** ASSERTED: 0 NATIONAL MOVERS, 0 ABSENT, NATIONAL BOARD VALUE IDENTICAL (%s). ***"
  % format(SEP['live']['nd_value'], ','))
P("  Nothing below this line is written until that assertion is reached. HARD FAILURE otherwise.")
P()

# ---- the delisted `back` rows, disclosed exactly as ORDER 24B disclosed them --------------------
bkl, bkv = BK['landed'], BK['live']
bkmov = [k for k in sorted(bkv) if k in bkl and val(bkl[k]) != val(bkv[k])]
bknonpool = [k for k in bkmov if not is_pool(bkv[k])]
P("  DELISTED (`back`) ROWS: %d moved, of which NON-POOL %d" % (len(bkmov), len(bknonpool)))
assert not bknonpool, "a non-pool delisted row moved: %s" % bknonpool[:5]
P()

# ---- TOTALS -------------------------------------------------------------------------------------
P("=" * 122)
P("BOARD TOTALS -- live vs landed, pool and national split")
P("=" * 122)
lv, ld = SEP['live'], SEP['landed']
P("  %-22s %14s %14s %14s %10s" % ('quantity', 'live', 'landed', 'delta', 'pct'))
for nm, a, b in (('TOTAL (active)', lv['total'], ld['total']),
                 ('pool', lv['pool_value'], ld['pool_value']),
                 ('national (ND 1-64)', lv['nd_value'], ld['nd_value'])):
    P("  %-22s %14s %14s %14s %9.3f%%"
      % (nm, format(a, ','), format(b, ','), format(b - a, ','), 100.0 * (b / a - 1) if a else 0.0))
P()

# ---- MOVERS -------------------------------------------------------------------------------------
allmov = [(k, val(live[k]), val(landed[k])) for k in keys
          if k in landed and val(live[k]) != val(landed[k])]
P("  ROWS MOVED vs live: %d   (up %d, down %d)   pool %d   non-pool %d"
  % (len(allmov), sum(1 for _, a, b in allmov if b > a), sum(1 for _, a, b in allmov if b < a),
     sum(1 for k, _, _ in allmov if is_pool(live[k])),
     sum(1 for k, _, _ in allmov if not is_pool(live[k]))))
P()
P("  TOP 15 MOVERS UP")
P("    %-30s %8s %8s %9s %9s %8s" % ('player', 'live', 'landed', 'delta', 'pct', 'pathway'))
for k, a, b in sorted(allmov, key=lambda t: -(t[2] - t[1]))[:15]:
    P("    %-30s %8d %8d %+9d %8.2f%% %8s" % (k, a, b, b - a, 100.0 * (b / a - 1) if a else 0.0,
                                              pathway(live[k])))
P("  TOP 15 MOVERS DOWN")
P("    %-30s %8s %8s %9s %9s %8s" % ('player', 'live', 'landed', 'delta', 'pct', 'pathway'))
for k, a, b in sorted(allmov, key=lambda t: (t[2] - t[1]))[:15]:
    P("    %-30s %8d %8d %+9d %8.2f%% %8s" % (k, a, b, b - a, 100.0 * (b / a - 1) if a else 0.0,
                                              pathway(live[k])))
P()

# ---- THE NAMED ROWS -----------------------------------------------------------------------------
NAMED = ['harrison-ramm', 'luker-kentfield', 'mani-liddy', 'robert-hansen', 'vigo-visentini',
         'marcus-herbert', 'jai-newcombe', 'nicholas-martin']
P("=" * 122)
P("THE NAMED ROWS (the pre-registered test names)")
P("=" * 122)
P("  %-22s %8s" % ('player', 'pathway') + "".join("%12s" % lab for lab, _ in BOARDS))
for n in NAMED:
    pw = pathway(live[n]) if n in live else '?'
    P("  %-22s %8s" % (n, pw) + "".join("%12s" % (val(B[lab][n]) if n in B[lab] else '-')
                                        for lab, _ in BOARDS))
P()

json.dump(dict(md5=MD5, separation=SEP, movers=len(allmov),
               movers_detail=[dict(key=k, live=a, landed=b, delta=b - a, pathway=pathway(live[k]))
                              for k, a, b in allmov],
               named={n: {lab: (val(B[lab][n]) if n in B[lab] else None) for lab, _ in BOARDS}
                      for n in NAMED},
               back_movers=len(bkmov), back_movers_nonpool=len(bknonpool)),
          open(OUTJS, 'w'), indent=1)
P("  wrote %s" % OUTJS)
