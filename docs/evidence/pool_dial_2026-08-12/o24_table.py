#!/usr/bin/env python3
"""ORDER 24 -- THE DIAL TABLE. The deliverable.

Six price columns per pool player -- pre_act / live / pr469 / a025 / a050 / a100 -- the separation
assertions on every alpha board, and the numbers that score the pre-registration.

The pathway and is_pool definitions are CARRIED VERBATIM from
docs/evidence/pool_landing_2026-08-12/o23_consequence.py:88-105 so this table and ORDER 23's ledger
partition the board the same way.

ATTRIBUTION: the alpha columns differ from `pr469` by EXACTLY ONE lever -- the current-state delivery
fix plus the dial (and the U' re-derivation the fix forces). pr469's own three-lever ledger against
live already exists at docs/ledgers/POOL_UPDATE_MOVERS_2026-08-12.json and is not re-derived here.

  usage: o24_table.py <outdir>
"""
import sys, json, os, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '../../..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
OUT = sys.argv[1]
P = print

CAVEAT = ("levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; "
          "re-trued at landing")

BOARDS = [('pre_act', SP + '/board_pre_act.json', '94f1fec59f99c59d5890d5975c79fa9b'),
          ('live',    SP + '/board_live.json',    '1dbd1480a34c7823f330273211cbb76a'),
          ('pr469',   ROOT + '/data/rl_build/rl_app_data.json', '665311ca72576df6ff0bbf6dfd007739'),
          ('a025',    SP + '/o24/board_a0.25.json', None),
          ('a050',    SP + '/o24/board_a0.50.json', None),
          ('a100',    SP + '/o24/board_a1.00.json', None)]
COLS = [b[0] for b in BOARDS]
ALPHACOLS = ['a025', 'a050', 'a100']

NAMED = ['mani-liddy', 'robert-hansen', 'nicholas-martin', 'marcus-herbert', 'jai-newcombe']
NAMED_WHY = {
    'mani-liddy': 'NAMED (order) — the defect case: MSD 2025 pick 15, 9 games 2025, 0 games 2026',
    'robert-hansen': 'NAMED (order) — the second defect case, same mechanism',
    'nicholas-martin': 'NAMED (order) — established SSP career, 0 games 2026: same cell, evidence-faded anchor',
    'marcus-herbert': 'NAMED (build) — healthy currently-playing pool rookie: MSD 2026 pick 13, 8 games 2026 (phi=1)',
    'jai-newcombe': 'NAMED (build) — established multi-season MSD star: highest live-board MSD value, 6 qualifying seasons, 21 games 2026',
}


def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()


TYMAP = {'National': 'ND', 'Rookie': 'RD', 'Mid-Season': 'MSD', 'Pre-Season': 'SSP',
         'Supplemental': 'SSP', 'Irish': 'IRE', 'Academy': 'PDA', 'Unrestricted': 'UNR'}


def pathway(r):
    t = r.get('ty') or TYMAP.get(r.get('draft')) or r.get('draft')
    if t == 'ND':
        return 'ND>64' if (r.get('pk') or 0) > 64 else 'ND 1-64'
    return t


POOLSET = {'RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64'}


def is_pool(r):
    return pathway(r) in POOLSET


def val(r):
    v = r.get('v')
    return float(v) if v is not None else 0.0


P("=" * 122)
P("ORDER 24 -- THE DIAL TABLE")
P("=" * 122)
B = {}
MD5 = {}
for lab, path, exp in BOARDS:
    m = md5(path)
    MD5[lab] = m
    if exp is not None:
        assert m == exp, "BOARD PIN FAILED: %s is %s, expected %s" % (lab, m, exp)
    D = json.load(open(path))
    B[lab] = {r.get('key') or r.get('name'): r for r in D['active']}
    B[lab + '@back'] = {r.get('key') or r.get('name'): r for r in D.get('back', [])}
    P("  %-8s %-34s md5 %s   active rows %d" % (lab, os.path.basename(path), m, len(B[lab])))
P()
P("  CAVEAT (verbatim, carried on every artifact of this order):")
P("    %s" % CAVEAT)
P()

live = B['live']
keys = sorted(live)
missing = {lab: sorted(set(keys) - set(B[lab])) for lab in COLS}
for lab in COLS:
    if missing[lab]:
        P("  NOTE: %s is missing %d of live's active keys (%s...) -- those rows are reported as "
          "absent, never as zero." % (lab, len(missing[lab]), ', '.join(missing[lab][:5])))

# ---- STEP 5: THE SEPARATION LAW ----------------------------------------------------------------
P("=" * 122)
P("THE SEPARATION LAW -- every ND (national) row identical to the live board 1dbd1480")
P("=" * 122)
SEP = {}
hard_fail = []
nd_keys = [k for k in keys if not is_pool(live[k])]
P("  national rows on the live board (ty==ND, pick<=64): %d    pool rows: %d"
  % (len(nd_keys), len(keys) - len(nd_keys)))
for lab in ALPHACOLS:
    moved = [k for k in nd_keys if k in B[lab] and val(live[k]) != val(B[lab][k])]
    absent = [k for k in nd_keys if k not in B[lab]]
    nd_live = sum(val(live[k]) for k in nd_keys)
    nd_var = sum(val(B[lab][k]) for k in nd_keys if k in B[lab])
    SEP[lab] = dict(nd_rows=len(nd_keys), nd_movers=len(moved), nd_absent=len(absent),
                    nd_value_live=nd_live, nd_value=nd_var, names=moved[:10])
    P("  %-6s ND movers: %-4d   ND absent: %-3d   ND board value %s -> %s"
      % (lab, len(moved), len(absent), format(round(nd_live), ','), format(round(nd_var), ',')))
    if moved or absent:
        hard_fail.append(lab)
assert not hard_fail, ("SEPARATION LAW BREACHED on %s -- HARD FAILURE, build stops" % hard_fail)
P("  ASSERTED: 0 ND movers on all three alpha boards.")
P()

# the delisted `back` list, checked separately (ORDER 23 convention)
for lab in ALPHACOLS:
    bl = B['live@back']; bv = B[lab + '@back']
    mv = [k for k in bl if k in bv and val(bl[k]) != val(bv[k])]
    ndmv = [k for k in mv if not is_pool(bl[k])]
    P("  %-6s delisted `back` rows moved: %-4d  of which non-pool: %d" % (lab, len(mv), len(ndmv)))
P()

# ---- pool totals -------------------------------------------------------------------------------
pool_keys = [k for k in keys if is_pool(live[k])]
P("=" * 122)
P("POOL TOTALS AND MOVER COUNTS (pool rows only, %d rows)" % len(pool_keys))
P("=" * 122)
P("  %-8s %14s %14s %9s %8s %6s %6s   %s" %
  ('board', 'pool total', 'vs live', 'vs live %', 'moved', 'up', 'down', 'moved vs pr469'))
TOT = {}
base = sum(val(live[k]) for k in pool_keys)
for lab in COLS:
    tot = sum(val(B[lab][k]) for k in pool_keys if k in B[lab])
    mv = up = dn = 0
    for k in pool_keys:
        if k not in B[lab]: continue
        a, b = val(live[k]), val(B[lab][k])
        if a != b:
            mv += 1; up += (b > a); dn += (b < a)
    mv469 = sum(1 for k in pool_keys
                if k in B[lab] and k in B['pr469'] and val(B['pr469'][k]) != val(B[lab][k]))
    TOT[lab] = dict(pool_total=tot, delta_vs_live=tot - base, moved_vs_live=mv, up=up, down=dn,
                    moved_vs_pr469=mv469)
    P("  %-8s %14s %14s %8.3f%% %8d %6d %6d   %d"
      % (lab, format(round(tot), ','), format(round(tot - base), ','),
         100.0 * (tot - base) / base, mv, up, dn, mv469))
P()

# ---- STEP 6: THE TABLE -------------------------------------------------------------------------
def material(k):
    a = val(live[k])
    for lab in COLS:
        if lab == 'live' or k not in B[lab]: continue
        d = val(B[lab][k]) - a
        if abs(d) >= 20.0 or (a > 0 and abs(d) / a >= 0.10):
            return True
    return False


ROWS = []
for k in pool_keys:
    inc = material(k)
    if not inc and k not in NAMED:
        continue
    r = live[k]
    a = val(r)
    row = dict(key=k, name=r.get('name'), pathway=pathway(r), pos=r.get('gf'), club=r.get('club'),
               pick=r.get('pk'), draft_year=r.get('yr'),
               games_2026=None, named=(k in NAMED), material=inc)
    for lab in COLS:
        row[lab] = (round(val(B[lab][k])) if k in B[lab] else None)
    row['d_pre_act'] = (row['pre_act'] - row['live']) if row['pre_act'] is not None else None
    for lab in ['pr469'] + ALPHACOLS:
        row['d_' + lab] = (row[lab] - row['live']) if row[lab] is not None else None
        row['pct_' + lab] = (100.0 * (row[lab] - row['live']) / row['live']
                             if row[lab] is not None and row['live'] else None)
    row['maxabs'] = max(abs(row['d_' + l]) for l in ['pr469'] + ALPHACOLS
                        if row['d_' + l] is not None)
    if row['d_pre_act'] is not None:
        row['maxabs'] = max(row['maxabs'], abs(row['d_pre_act']))
    ROWS.append(row)

# 2026 games from the store, for reading the table
STORE = {p['key']: p for p in json.load(open(ROOT + '/engine/rl_after/rl_model_data.json'))}
for row in ROWS:
    p = STORE.get(row['key'])
    if p:
        row['games_2026'] = sum(x['games'] for x in p['scoring'] if x['year'] == 2026)
        row['qual_seasons_pre2026'] = sum(1 for x in p['scoring']
                                          if x['year'] < 2026 and x['games'] >= 6)

ROWS.sort(key=lambda r: -r['maxabs'])
P("=" * 122)
P("THE TABLE: %d rows (%d material, %d named-only)"
  % (len(ROWS), sum(1 for r in ROWS if r['material']),
     sum(1 for r in ROWS if not r['material'])))
P("=" * 122)
mat_alpha = [r for r in ROWS
             if any(r['d_' + l] is not None and
                    (abs(r['d_' + l]) >= 20 or (r['live'] and abs(r['d_' + l]) / r['live'] >= 0.10))
                    for l in ALPHACOLS)]
P("  material against LIVE on at least one ALPHA column: %d rows" % len(mat_alpha))
P()
P("  %-24s %-7s %4s %7s %7s %7s %7s %7s %7s" %
  ('player', 'path', 'g26', 'pre_act', 'live', 'pr469', 'a025', 'a050', 'a100'))
for r in ROWS[:40]:
    P("  %-24s %-7s %4s %7s %7s %7s %7s %7s %7s%s" %
      (r['key'], r['pathway'], r['games_2026'], r['pre_act'], r['live'], r['pr469'],
       r['a025'], r['a050'], r['a100'], '  <-- NAMED' if r['named'] else ''))
P()
P("  THE NAMED FIVE")
for k in NAMED:
    r = next((x for x in ROWS if x['key'] == k), None)
    if r is None:
        P("    %-20s ABSENT from the pool row set" % k); continue
    P("    %-20s pre_act %6s  live %6s  pr469 %6s  a025 %6s  a050 %6s  a100 %6s   (g26=%s, qual seasons pre-2026=%s)"
      % (k, r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'], r['a100'],
         r['games_2026'], r.get('qual_seasons_pre2026')))
P()

# ---- prereg scoring inputs ---------------------------------------------------------------------
P("=" * 122)
P("PRE-REGISTRATION SCORING INPUTS")
P("=" * 122)


def cell(k):
    p = STORE.get(k)
    if not p: return None
    gy = sum(x['games'] for x in p['scoring'] if x['year'] == 2026)
    nq = sum(1 for x in p['scoring'] if x['year'] < 2026 and x['games'] >= 6)
    fe = 1.0 if (live[k].get('lti_reg') or {}).get('out') else json.load(
        open(SP + '/board_live.json'))['SEASON_PROG']
    return gy, nq, fe


FE = json.load(open(ROOT + '/data/rl_build/rl_app_data.json'))['SEASON_PROG']
grp = {'full': [], 'partial': [], 'sit_qual': [], 'sit_never': []}
for k in pool_keys:
    p = STORE.get(k)
    if not p: continue
    fe = 1.0 if (live[k].get('lti_reg') or {}).get('out') else FE
    gy = sum(x['games'] for x in p['scoring'] if x['year'] == 2026)
    nq = sum(1 for x in p['scoring'] if x['year'] < 2026 and x['games'] >= 6)
    if gy >= 6.0 * fe: grp['full'].append(k)
    elif gy > 0: grp['partial'].append(k)
    elif nq >= 1: grp['sit_qual'].append(k)
    else: grp['sit_never'].append(k)
for g, ks in grp.items():
    moved = {lab: sum(1 for k in ks if val(B['pr469'][k]) != val(B[lab][k])) for lab in ALPHACOLS}
    P("  %-10s n=%-4d  moved vs pr469: a025 %-4d  a050 %-4d  a100 %-4d"
      % (g, len(ks), moved['a025'], moved['a050'], moved['a100']))
P()
P("  P5 (full participants byte-identical to pr469 at every alpha): %s"
  % ('HELD' if all(val(B['pr469'][k]) == val(B[l][k]) for k in grp['full'] for l in ALPHACOLS)
     else 'BREACHED'))
P("  P6 (never-qualified current sitters byte-identical to pr469 at alpha=1.0): %s"
  % ('HELD' if all(val(B['pr469'][k]) == val(B['a100'][k]) for k in grp['sit_never'])
     else 'BREACHED'))
P("  pool rows moving pr469 -> a100: %d" % TOT['a100']['moved_vs_pr469'])
P()

json.dump(dict(caveat=CAVEAT, board_md5=MD5, separation=SEP, totals=TOT,
               cells={g: sorted(ks) for g, ks in grp.items()},
               n_rows=len(ROWS), n_material=sum(1 for r in ROWS if r['material']),
               n_material_alpha=len(mat_alpha), named=NAMED, named_why=NAMED_WHY,
               rows=ROWS),
          open(os.path.join(OUT, 'MOVERS_TABLE.json'), 'w'), indent=1, default=float)
P("  wrote %s" % os.path.join(OUT, 'MOVERS_TABLE.json'))
