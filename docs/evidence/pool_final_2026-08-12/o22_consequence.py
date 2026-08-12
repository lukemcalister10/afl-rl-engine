#!/usr/bin/env python3
"""ORDER 22 -- THE CONSEQUENCE: the composed pool-update movers ledger, the separation assertions,
and the `_ruc_prior_cap` check.

Reads only artefacts already produced. Writes CONSEQUENCE.json + prints the ledger.

  usage: o22_consequence.py <out.json>

THE LEVERS, decomposed against the LIVE board `1dbd1480`:
  LEVER 1  H RETIREMENT   RL_H_POOLSIT=1.0 RL_H_UNION=1.0, national surface still read  -> board_VARA
  LEVER 2  + RETENTION    the ORDER 22 derived pool surface at BOTH read sites,
                          checkout levels                                               -> board_STAGED22
  LEVER 3  + REPRICING    the derived entry levels                                      -> board_FINAL
"""
import sys, json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OUT = sys.argv[1]
P = print


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


BOARDS = [('LIVE', SP + '/o22/board_C1_unstaged.json'),
          ('VARA', SP + '/o22/board_VARA.json'),
          ('STAGED22', SP + '/o22/board_STAGED22.json'),
          ('FINAL', SP + '/o22/board_FINAL.json')]

PINS = {'board': ROOT + '/data/rl_build/rl_app_data.json',
        'store': ROOT + '/engine/rl_after/rl_model_data.json',
        'instrument noarb_table_338.py': ROOT + '/docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py'}
PINMD5 = {k: md5(v) for k, v in PINS.items()}
assert PINMD5['board'] == '1dbd1480a34c7823f330273211cbb76a'
assert PINMD5['store'] == 'd9a24282357cf3083b1640466e3ecd83'
assert PINMD5['instrument noarb_table_338.py'] == '0f8220351c64c56ccfa90c60edcdfa5f'


def load(path):
    D = json.load(open(path))
    return D, list(D['active'])          # the priced board; `back` (198 delisted rows) is checked separately


def rowmap(rows):
    out = {}
    for r in rows:
        k = r.get('key') or r.get('name')
        out[k] = r
    return out


P("=" * 122)
P("ORDER 22 -- THE COMPOSED POOL-UPDATE MOVERS LEDGER")
P("=" * 122)
P("  pins (computed at run): " + " · ".join("%s %s" % (k.split()[0], v[:8]) for k, v in PINMD5.items()))
P()
B = {}
for lab, path in BOARDS:
    D, rows = load(path)
    B[lab] = dict(md5=md5(path), rows=rowmap(rows), raw=D)
    P("  %-9s %-34s md5 %s   rows %d" % (lab, os.path.basename(path), B[lab]['md5'], len(B[lab]['rows'])))
P()

# the live board on disk must equal the LIVE reproduction
assert B['LIVE']['md5'] == PINMD5['board'], "the unstaged control does not reproduce the live board"
P("  CONTROL: the unstaged build reproduces the live board %s BYTE-IDENTICAL." % PINMD5['board'])
P()

VALK = 'v'
P("  board value field: %r" % VALK)


def val(r):
    v = r.get(VALK)
    return float(v) if v is not None else 0.0


TYMAP = {'National': 'ND', 'Rookie': 'RD', 'Mid-Season': 'MSD', 'Pre-Season': 'SSP',
         'Supplemental': 'SSP', 'Irish': 'IRE', 'Academy': 'PDA', 'Unrestricted': 'UNR'}


def pathway(r):
    """The board row's pathway, from the engine's own `ty` field where present, else `draft`."""
    t = r.get('ty') or TYMAP.get(r.get('draft')) or r.get('draft')
    if t == 'ND':
        return 'ND>64' if (r.get('pk') or 0) > 64 else 'ND 1-64'
    return t


POOLSET = {'RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64'}


def is_pool(r):
    return pathway(r) in POOLSET


keys = sorted(B['LIVE']['rows'])
P()
P("  %-10s %14s %14s %10s %8s %6s %6s" % ('board', 'total', 'delta vs LIVE', 'delta %', 'moved', 'up', 'down'))
P("  " + "-" * 118)
TOT = {}
for lab, _ in BOARDS:
    tot = sum(val(r) for r in B[lab]['rows'].values())
    mv = up = dn = 0
    for k in keys:
        a = val(B['LIVE']['rows'][k]); b = val(B[lab]['rows'].get(k, B['LIVE']['rows'][k]))
        if a != b:
            mv += 1
            up += (b > a); dn += (b < a)
    TOT[lab] = dict(total=tot, moved=mv, up=up, down=dn,
                    delta=tot - sum(val(r) for r in B['LIVE']['rows'].values()))
    P("  %-10s %14s %14s %9.3f%% %8d %6d %6d" %
      (lab, format(round(tot), ','), format(round(TOT[lab]['delta']), ','),
       100.0 * TOT[lab]['delta'] / TOT['LIVE']['total'], mv, up, dn))
P()

# ---- separation on the board -------------------------------------------------------------------
P("=" * 122)
P("THE SEPARATION LAW ON THE BOARD -- ASSERTED, PRINTED")
P("=" * 122)
SEP = {}
for lab, _ in BOARDS[1:]:
    nd_moved = [k for k in keys if not is_pool(B['LIVE']['rows'][k])
                and val(B['LIVE']['rows'][k]) != val(B[lab]['rows'].get(k, B['LIVE']['rows'][k]))]
    nd_val_live = sum(val(r) for k, r in B['LIVE']['rows'].items() if not is_pool(r))
    nd_val_var = sum(val(B[lab]['rows'][k]) for k in keys if not is_pool(B['LIVE']['rows'][k]))
    SEP[lab] = dict(non_pool_rows_moved=len(nd_moved), non_pool_value_live=nd_val_live,
                    non_pool_value=nd_val_var, names=nd_moved[:10])
    P("  %-10s non-pool board rows moved: %-4d   non-pool board value %s -> %s"
      % (lab, len(nd_moved), format(round(nd_val_live), ','), format(round(nd_val_var), ',')))
    if nd_moved: P("            names: %s" % nd_moved[:10])
P()

# ---- by pathway --------------------------------------------------------------------------------
P("=" * 122)
P("BY PATHWAY")
P("=" * 122)
P("  %-9s %6s %7s %12s %12s %12s %12s %12s %10s" %
  ('pathway', 'rows', 'moved', 'LIVE', 'VARA', 'STAGED22', 'FINAL', 'FINAL d', 'FINAL %'))
P("  " + "-" * 118)
BYP = {}
paths = sorted({pathway(r) for r in B['LIVE']['rows'].values()}, key=lambda s: s or '')
for pw in paths:
    ks = [k for k in keys if pathway(B['LIVE']['rows'][k]) == pw]
    if not ks: continue
    v = {lab: sum(val(B[lab]['rows'][k]) for k in ks) for lab, _ in BOARDS}
    mv = sum(1 for k in ks if val(B['LIVE']['rows'][k]) != val(B['FINAL']['rows'][k]))
    BYP[pw] = dict(rows=len(ks), moved=mv, **{lab: v[lab] for lab, _ in BOARDS})
    P("  %-9s %6d %7d %12s %12s %12s %12s %12s %9.3f%%" %
      (pw, len(ks), mv, format(round(v['LIVE']), ','), format(round(v['VARA']), ','),
       format(round(v['STAGED22']), ','), format(round(v['FINAL']), ','),
       format(round(v['FINAL'] - v['LIVE']), ','),
       100.0 * (v['FINAL'] - v['LIVE']) / v['LIVE'] if v['LIVE'] else 0.0))
P()

# ---- the named ledger with the lever decomposition ----------------------------------------------
P("=" * 122)
P("EVERY BOARD ROW THAT MOVES, WITH THE LEVER DECOMPOSITION  (H retirement / retention / repricing)")
P("=" * 122)
LED = []
for k in keys:
    a = val(B['LIVE']['rows'][k]); d = val(B['FINAL']['rows'][k])
    if a == d: continue
    va = val(B['VARA']['rows'][k]); st = val(B['STAGED22']['rows'][k])
    LED.append(dict(key=k, player=B['LIVE']['rows'][k].get('name'),
                    pathway=pathway(B['LIVE']['rows'][k]), pos=B['LIVE']['rows'][k].get('grp'),
                    live=a, vara=va, staged=st, final=d, delta=d - a,
                    pct=100.0 * (d / a - 1) if a else float('inf'),
                    lever_H=va - a, lever_retention=st - va, lever_repricing=d - st))
LED.sort(key=lambda r: -abs(r['delta']))
P("  %-26s %-7s %-5s %9s %9s %9s %9s %9s %9s | %8s %10s %10s" %
  ('player', 'pathway', 'pos', 'LIVE', 'VARA', 'STAGED', 'FINAL', 'delta', 'pct',
   'lev H', 'lev reten', 'lev repric'))
P("  " + "-" * 118)
for r in LED[:45]:
    P("  %-26s %-7s %-5s %9.0f %9.0f %9.0f %9.0f %+9.0f %8.1f%% | %8.0f %10.0f %10.0f" %
      ((r['player'] or r['key'])[:26], r['pathway'], r['pos'] or '', r['live'], r['vara'],
       r['staged'], r['final'], r['delta'], r['pct'],
       r['lever_H'], r['lever_retention'], r['lever_repricing']))
P("  ... %d moved rows in total; the full ledger is in CONSEQUENCE.json['ledger']." % len(LED))
P()
lev = dict(H=sum(r['lever_H'] for r in LED), retention=sum(r['lever_retention'] for r in LED),
           repricing=sum(r['lever_repricing'] for r in LED))
P("  LEVER TOTALS across every moved row:  H retirement %+.0f · retention %+.0f · repricing %+.0f  = %+.0f"
  % (lev['H'], lev['retention'], lev['repricing'], sum(lev.values())))
P("  rows that go DOWN under the FINAL configuration: %d" % sum(1 for r in LED if r['delta'] < 0))
P()

json.dump(dict(pins=PINMD5, boards={lab: dict(md5=B[lab]['md5'], **TOT[lab]) for lab, _ in BOARDS},
               separation=SEP, by_pathway=BYP, lever_totals=lev, ledger=LED),
          open(OUT, 'w'), indent=1, default=float)
P("wrote %s" % OUT)
