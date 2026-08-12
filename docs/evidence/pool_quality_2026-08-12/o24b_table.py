#!/usr/bin/env python3
"""ORDER 24B STEP 6 -- THE TABLE. The deliverable.

SEVEN price columns per pool player -- pre_act / live / pr469 / a025 / a050 / a100 / psi -- the
separation assertion on the psi board (raised BEFORE anything is written), the Q_TABLE for every
currently-playing pool row, and the numbers that score the pre-registration.

The pathway and is_pool definitions are CARRIED VERBATIM from ORDER 24's o24_table.py, which carried
them from ORDER 23's o23_consequence.py, so all three tables partition the board the same way.

The q, par and depth reported in Q_TABLE.md are computed by CALLING THE ENGINE'S OWN `_pr_q`,
`_pr_par`, `_pr_depth` and `_pr_phi` on the store records -- never re-implemented here, so the table
cannot drift from what the board was priced on.

ATTRIBUTION: the psi column differs from a100 by EXACTLY ONE lever -- the quality condition q on the
premium leg, and the U'' re-derivation that condition forces.

  usage: o24b_table.py <outdir>
"""
import sys, json, os, hashlib, io, contextlib, shutil, collections

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
          ('a025',    SP + '/o24/board_a0.25.json', '322df660ccce6c017ded341403b7215f'),
          ('a050',    SP + '/o24/board_a0.50.json', '87214d5653e0fb8e48b804f1a890b6bc'),
          ('a100',    SP + '/o24/board_a1.00.json', 'ca3544d8df9272db191a67001a1bb9e4'),
          ('psi',     SP + '/o24b/board_psi.json', None)]
COLS = [b[0] for b in BOARDS]
VARCOLS = ['pre_act', 'pr469', 'a025', 'a050', 'a100', 'psi']

NAMED = ['mani-liddy', 'robert-hansen', 'nicholas-martin', 'marcus-herbert', 'jai-newcombe',
         'harrison-ramm', 'luker-kentfield', 'vigo-visentini']
NAMED_WHY = {
    'mani-liddy': 'NAMED (order) — ORDER 24 defect case: MSD 2025 pick 15, 0 games 2026. phi=0, so psi cannot reach him: 168 EXACT is the test.',
    'robert-hansen': 'NAMED (order) — the second ORDER 24 defect case, same mechanism, same phi=0 test',
    'nicholas-martin': 'NAMED (order) — established SSP career, 0 games 2026: phi=0, evidence-faded anchor',
    'marcus-herbert': 'NAMED (order) — healthy currently-playing pool rookie, 8 games 2026 (phi=1, anchor share exactly 0)',
    'jai-newcombe': 'NAMED (order) — established MSD star, 21 games 2026 (phi=1, anchor share exactly 0)',
    'harrison-ramm': 'NAMED (order) — THE ORDER 24B DEFECT CASE: MSD, 4 games 2026 at 28.75, collected the full MSD premium 406 -> 620',
    'luker-kentfield': 'NAMED (order) — MSD, 3 games 2026 at 32.33, the second quality-blind lift',
    'vigo-visentini': 'NAMED (order) — RD ruck, 1 game 2026 at 84.00: quality ABOVE par, earned a fraction. The row the clip is for.',
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


P("=" * 130)
P("ORDER 24B -- THE TABLE")
P("=" * 130)
B, MD5 = {}, {}
for lab, path, exp in BOARDS:
    m = md5(path)
    MD5[lab] = m
    if exp is not None:
        assert m == exp, "BOARD PIN FAILED: %s is %s, expected %s" % (lab, m, exp)
    D = json.load(open(path))
    B[lab] = {r.get('key') or r.get('name'): r for r in D['active']}
    B[lab + '@back'] = {r.get('key') or r.get('name'): r for r in D.get('back', [])}
    P("  %-8s %-30s md5 %s   active rows %d%s"
      % (lab, os.path.basename(path), m, len(B[lab]), '   [PINNED]' if exp else ''))
P()
P("  CAVEAT (verbatim, carried on every artifact of this order):")
P("    %s" % CAVEAT)
P()

live = B['live']
keys = sorted(live)

# ---- THE SEPARATION LAW -- asserted BEFORE any table is written ---------------------------------
P("=" * 130)
P("THE SEPARATION LAW -- every ND (national) row identical to the live board 1dbd1480")
P("=" * 130)
nd_keys = [k for k in keys if not is_pool(live[k])]
pool_keys = [k for k in keys if is_pool(live[k])]
P("  national rows on the live board (ty==ND, pick<=64): %d    pool rows: %d"
  % (len(nd_keys), len(pool_keys)))
SEP, hard_fail = {}, []
for lab in ['a100', 'psi']:
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
assert not hard_fail, ("SEPARATION LAW BREACHED on %s -- HARD FAILURE, build stops, nothing written"
                       % hard_fail)
P("  ASSERTED: 0 ND movers on the psi board. Nothing below is written until this line is reached.")
for lab in ['a100', 'psi']:
    bl, bv = B['live@back'], B[lab + '@back']
    mv = [k for k in bl if k in bv and val(bl[k]) != val(bv[k])]
    P("  %-6s delisted `back` rows moved: %-4d  of which non-pool: %d"
      % (lab, len(mv), sum(1 for k in mv if not is_pool(bl[k]))))
P()

# ---- THE ENGINE'S OWN q / par / phi, called not re-implemented ----------------------------------
STAGE = SP + '/eng_stage_o24b_tbl/rl_after'
shutil.rmtree(SP + '/eng_stage_o24b_tbl', ignore_errors=True)
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(os.path.join(ROOT, 'LTI_REGISTER.md'), STAGE)
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT)
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA = G['MA']
_pr_q, _pr_par, _pr_phi, _pr_depth = G['_pr_q'], G['_pr_par'], G['_pr_phi'], G['_pr_depth']
_pr_pathway, _pr_U = G['_pr_pathway'], G['_pr_U']
REC = {p.get('key'): p for p in MA.data if p.get('key')}
PSISURF = json.load(open(HERE + '/SURFACE_psi.json'))
U2 = PSISURF['uplift']
U1 = json.load(open(ROOT + '/docs/evidence/pool_dial_2026-08-12/SURFACE_a1.00.json'))['uplift']
Y = 2026

# ---- pool totals --------------------------------------------------------------------------------
P("=" * 130)
P("POOL TOTALS AND MOVER COUNTS (pool rows only, %d rows)" % len(pool_keys))
P("=" * 130)
P("  %-8s %14s %14s %10s %8s %6s %6s %10s %10s" %
  ('board', 'pool total', 'vs live', 'vs live %', 'moved', 'up', 'down', 'vs pr469', 'vs a100'))
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
    m469 = sum(1 for k in pool_keys if k in B[lab] and val(B['pr469'][k]) != val(B[lab][k]))
    m100 = sum(1 for k in pool_keys if k in B[lab] and val(B['a100'][k]) != val(B[lab][k]))
    TOT[lab] = dict(pool_total=tot, delta_vs_live=tot - base, moved_vs_live=mv, up=up, down=dn,
                    moved_vs_pr469=m469, moved_vs_a100=m100)
    P("  %-8s %14s %14s %9.3f%% %8d %6d %6d %10d %10d"
      % (lab, format(round(tot), ','), format(round(tot - base), ','),
         100.0 * (tot - base) / base, mv, up, dn, m469, m100))
P()

# ---- the psi cell structure: who CAN move -------------------------------------------------------
FE = float(json.load(open(ROOT + '/data/rl_build/rl_app_data.json'))['SEASON_PROG'])
grp = collections.defaultdict(list)
for k in pool_keys:
    p = REC.get(k)
    if not p: continue
    ph = float(_pr_phi(p, Y))
    grp['full' if ph >= 1.0 else ('partial' if ph > 0 else 'sit')].append(k)
P("  THE psi CELL STRUCTURE -- only rows with 0 < phi < 1 can move a100 -> psi:")
for g in ['full', 'partial', 'sit']:
    ks = grp[g]
    P("    %-8s n=%-4d   moved a100 -> psi: %d"
      % (g, len(ks), sum(1 for k in ks if val(B['a100'][k]) != val(B['psi'][k]))))
outside = [k for k in pool_keys if val(B['a100'][k]) != val(B['psi'][k]) and k not in grp['partial']]
P("    movers OUTSIDE the partial cell (must be 0 by construction): %d %s"
  % (len(outside), outside[:10]))
P()

# ---- Q_TABLE: every currently-playing pool row --------------------------------------------------
QROWS = []
for k in pool_keys:
    p = REC.get(k)
    if not p: continue
    ph = float(_pr_phi(p, Y))
    if ph <= 0: continue
    yr = [x for x in p['scoring'] if x['year'] == Y]
    gy = sum(x['games'] for x in yr)
    av = (sum(float(x.get('avg') or 0.0) * x['games'] for x in yr) / gy) if gy > 0 else None
    pw = _pr_pathway(p)
    QROWS.append(dict(key=k, name=live[k].get('name'), pathway=pathway(live[k]), engine_pathway=pw,
                      games=gy, avg=(round(av, 2) if av else None), depth=int(_pr_depth(p, Y)),
                      par=round(float(_pr_par(p, Y)), 4), q=round(float(_pr_q(p, Y)), 6),
                      phi=round(ph, 6), psi_weight=round(ph * float(_pr_q(p, Y)), 6),
                      U_a100=(U1.get(pw) if pw else None), U_psi=(U2.get(pw) if pw else None),
                      a100=round(val(B['a100'][k])), psi=round(val(B['psi'][k])),
                      d_psi=round(val(B['psi'][k]) - val(B['a100'][k]))))
QROWS.sort(key=lambda r: (-abs(r['d_psi']), r['key']))
P("=" * 130)
P("Q_TABLE -- every currently-playing pool row (%d rows), q = clip(avg / par(pathway, depth), 0, 1)"
  % len(QROWS))
P("=" * 130)
P("  %-26s %-6s %4s %7s %2s %8s %7s %7s %7s %7s %6s"
  % ('player', 'path', 'g26', 'avg26', 'd', 'par', 'q', 'phi', 'a100', 'psi', 'delta'))
for r in QROWS[:60]:
    P("  %-26s %-6s %4g %7s %2d %8.2f %7.4f %7.4f %7d %7d %+6d"
      % (r['key'], r['pathway'], r['games'], ('%.2f' % r['avg']) if r['avg'] else 'NONE',
         r['depth'], r['par'], r['q'], r['phi'], r['a100'], r['psi'], r['d_psi']))
P("  ... (%d rows in total; the full set is in Q_TABLE.md)" % len(QROWS))
P()
P("  q == 1.0 (at or above par, the clip binds): %d rows" % sum(1 for r in QROWS if r['q'] >= 1.0))
P("  q == 0.0 (games played, no usable average): %d rows" % sum(1 for r in QROWS if r['q'] <= 0.0))
P()

# ---- THE TABLE ----------------------------------------------------------------------------------
def material(k):
    a = val(live[k])
    for lab in VARCOLS:
        if k not in B[lab]: continue
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
    p = REC.get(k)
    row = dict(key=k, name=r.get('name'), pathway=pathway(r), pos=r.get('gf'), club=r.get('club'),
               pick=r.get('pk'), draft_year=r.get('yr'), named=(k in NAMED), material=inc)
    for lab in COLS:
        row[lab] = (round(val(B[lab][k])) if k in B[lab] else None)
    for lab in VARCOLS:
        row['d_' + lab] = (row[lab] - row['live']) if row[lab] is not None else None
        row['pct_' + lab] = (100.0 * (row[lab] - row['live']) / row['live']
                             if row[lab] is not None and row['live'] else None)
    row['d_psi_vs_a100'] = (row['psi'] - row['a100']
                            if row['psi'] is not None and row['a100'] is not None else None)
    row['maxabs'] = max(abs(row['d_' + l]) for l in VARCOLS if row['d_' + l] is not None)
    if p:
        row['games_2026'] = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
        row['qual_seasons_pre2026'] = sum(1 for x in p['scoring']
                                          if x['year'] < Y and x['games'] >= 6)
        row['phi'] = round(float(_pr_phi(p, Y)), 6)
        row['q'] = round(float(_pr_q(p, Y)), 6)
        row['par'] = round(float(_pr_par(p, Y)), 4)
        row['depth'] = int(_pr_depth(p, Y))
        yr = [x for x in p['scoring'] if x['year'] == Y]
        g = sum(x['games'] for x in yr)
        row['avg_2026'] = (round(sum(float(x.get('avg') or 0.0) * x['games'] for x in yr) / g, 2)
                           if g > 0 else None)
    ROWS.append(row)
ROWS.sort(key=lambda r: -r['maxabs'])

mat_psi = [r for r in ROWS if r['d_psi'] is not None and
           (abs(r['d_psi']) >= 20 or (r['live'] and abs(r['d_psi']) / r['live'] >= 0.10))]
P("=" * 130)
P("THE TABLE: %d rows (%d material, %d named-only). Material against LIVE on the psi column: %d"
  % (len(ROWS), sum(1 for r in ROWS if r['material']),
     sum(1 for r in ROWS if not r['material']), len(mat_psi)))
P("=" * 130)
P("  %-24s %-6s %4s %7s %7s %7s %7s %7s %7s %7s %7s" %
  ('player', 'path', 'g26', 'pre_act', 'live', 'pr469', 'a025', 'a050', 'a100', 'psi', 'psi-a100'))
for r in ROWS[:45]:
    P("  %-24s %-6s %4s %7s %7s %7s %7s %7s %7s %7s %+7s%s" %
      (r['key'], r['pathway'], r.get('games_2026'), r['pre_act'], r['live'], r['pr469'],
       r['a025'], r['a050'], r['a100'], r['psi'], r['d_psi_vs_a100'],
       '  <-- NAMED' if r['named'] else ''))
P()
P("  THE EIGHT NAMED ROWS")
for k in NAMED:
    r = next((x for x in ROWS if x['key'] == k), None)
    if r is None:
        P("    %-20s ABSENT from the pool row set" % k); continue
    P("    %-18s pre_act %6s live %6s pr469 %6s a025 %6s a050 %6s a100 %6s psi %6s  (g26=%s avg=%s d=%s par=%s q=%s phi=%s)"
      % (k, r['pre_act'], r['live'], r['pr469'], r['a025'], r['a050'], r['a100'], r['psi'],
         r.get('games_2026'), r.get('avg_2026'), r.get('depth'), r.get('par'), r.get('q'), r.get('phi')))
P()

# ---- top movers a100 -> psi ---------------------------------------------------------------------
MOV = [r for r in ROWS if r['d_psi_vs_a100']]
P("  TOP MOVERS a100 -> psi, DOWN (%d rows fell):" % sum(1 for r in MOV if r['d_psi_vs_a100'] < 0))
for r in sorted(MOV, key=lambda r: r['d_psi_vs_a100'])[:15]:
    P("    %-24s %-6s a100 %6d -> psi %6d  %+6d  (avg %s vs par %s, q=%.4f, phi=%.4f)"
      % (r['key'], r['pathway'], r['a100'], r['psi'], r['d_psi_vs_a100'],
         r.get('avg_2026'), r.get('par'), r.get('q', 0), r.get('phi', 0)))
P("  TOP MOVERS a100 -> psi, UP (%d rows rose):" % sum(1 for r in MOV if r['d_psi_vs_a100'] > 0))
for r in sorted(MOV, key=lambda r: -r['d_psi_vs_a100'])[:15]:
    P("    %-24s %-6s a100 %6d -> psi %6d  %+6d  (avg %s vs par %s, q=%.4f, phi=%.4f)"
      % (r['key'], r['pathway'], r['a100'], r['psi'], r['d_psi_vs_a100'],
         r.get('avg_2026'), r.get('par'), r.get('q', 0), r.get('phi', 0)))
P()

json.dump(dict(caveat=CAVEAT, board_md5=MD5, separation=SEP, totals=TOT,
               cells={g: sorted(ks) for g, ks in grp.items()},
               n_rows=len(ROWS), n_material=sum(1 for r in ROWS if r['material']),
               n_material_psi=len(mat_psi), named=NAMED, named_why=NAMED_WHY,
               uplift_a100=U1, uplift_psi=U2, q_rows=QROWS, rows=ROWS),
          open(os.path.join(OUT, 'MOVERS_TABLE_PSI.json'), 'w'), indent=1, default=float)
P("  wrote %s" % os.path.join(OUT, 'MOVERS_TABLE_PSI.json'))
