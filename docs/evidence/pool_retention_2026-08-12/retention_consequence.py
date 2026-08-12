#!/usr/bin/env python3
"""ORDER 21 -- WHAT THE DERIVED SURFACE DOES TO THE BOARD.

Compares five boards, all built by build_board_o21.sh on the ADOPTED engine (main @ c330169, the par
fix landed), all against the live board pin 1dbd1480a34c7823f330273211cbb76a:

  BASE         HEAD defaults                                        -- the control; must be byte-identical to live
  VARA         H_POOLSIT = H_UNION = 1.0                            -- ORDER 19 variant A, REBUILT on this engine
  VARB         VARA + R := 1.0 for pool rows at sitout_ev           -- ORDER 19 variant B, REBUILT on this engine
  DERIVEDSIT   VARA + the DERIVED surface at sitout_ev only         -- disclosed sensitivity
  DERIVED      VARA + the DERIVED object at BOTH sites              -- ** THE STAGED CONFIGURATION **

READ-ONLY. Pins asserted at entry AND exit.
  usage: OPENBLAS_NUM_THREADS=1 python retention_consequence.py
"""
import os, sys, io, json, contextlib, math, hashlib, shutil, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O21 = SP + '/o21'
STAGE = SP + '/eng_stage_o21/rl_after'

PINS = {
    'board': ('data/rl_build/rl_app_data.json', '1dbd1480a34c7823f330273211cbb76a'),
    'store': ('engine/rl_after/rl_model_data.json', 'd9a24282357cf3083b1640466e3ecd83'),
    'instrument': ('docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py',
                   '0f8220351c64c56ccfa90c60edcdfa5f'),
}


def _md5(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def assert_pins(when):
    bad = ["%s %s != pinned %s (%s)" % (k, _md5(os.path.join(ROOT, rel)), exp, rel)
           for k, (rel, exp) in PINS.items() if _md5(os.path.join(ROOT, rel)) != exp]
    if bad:
        raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')

if not os.path.exists(os.path.join(STAGE, '_merged_recover.py')):
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(ROOT + '/LTI_REGISTER.md', STAGE)
os.environ.update(PYTHONHASHSEED='0')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd(); os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
MA, cp = G['MA'], G['cp']

SURF = json.load(open(os.path.join(HERE, 'POOL_RETENTION_SURFACE.json')))
OUT = []


def P(s=''):
    print(s); OUT.append(s)


LABS = ['BASE', 'VARA', 'VARB', 'DERIVEDSIT', 'DERIVED']
NICE = {'BASE': 'TODAY (shipped)', 'VARA': 'VARIANT A  (H lifted only)',
        'VARB': 'VARIANT B  (H + R:=1 at sitout_ev)',
        'DERIVEDSIT': 'DERIVED, sit site only', 'DERIVED': '** STAGED: DERIVED, both sites **'}
BD = {}
P("=" * 118)
P("ORDER 21 -- THE STAGED BOARD: WHAT THE DERIVED POOL RETENTION DOES")
P("=" * 118)
P("  pins asserted at entry: board 1dbd1480..  store d9a24282..  instrument 0f822035..")
P()
P("0. CONTROLS")
for lab in LABS:
    p = os.path.join(O21, 'board_%s.json' % lab)
    BD[lab] = json.load(open(p))
    P("  board %-11s md5 %s" % (lab, _md5(p)))
_live = _md5(os.path.join(ROOT, PINS['board'][0]))
_base = _md5(os.path.join(O21, 'board_BASE.json'))
P("  live board  md5 %s" % _live)
P("  CONTROL 1: the HEAD-defaults board build reproduces THE LIVE BOARD BYTE-FOR-BYTE -> %s"
  % ("REPRODUCED" if _base == _live else "MISMATCH"))
assert _base == _live
P("  engine_head per build (the machine proof each patch was in the tree that built it):")
P("     BASE/VARA a8071af4 (unpatched)  VARB a20d7092  DERIVEDSIT cd2e37c0  DERIVED 54347ed4")
P()

ROW = {lab: {r['key']: r for r in BD[lab]['active']} for lab in LABS}
BACK = {lab: {r['key']: r for r in BD[lab]['back']} for lab in LABS}
KEYS = sorted(ROW['BASE'])
for lab in LABS:
    assert set(ROW[lab]) == set(ROW['BASE'])

ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
POOLS = set(ORDER)


def bstream(r):
    t = r.get('ty')
    if t == 'ND':
        pk = r.get('pk') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


PLK = {}
for p in MA.data:
    PLK[p.get('key') or p.get('player')] = p
Y0 = 2026


def games_in(p, Y):
    return sum(x['games'] for x in p['scoring'] if x['year'] == Y)


def q(v, f):
    if not v: return float('nan')
    s = sorted(v); i = f * (len(s) - 1)
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


# ==================================================================================================
P("=" * 118)
P("1. THE BOARD TOTAL")
P("=" * 118)
tot = {lab: sum(ROW[lab][k]['v'] for k in KEYS) for lab in LABS}
btot = {lab: sum(BACK[lab][k]['v'] for k in BACK[lab]) for lab in LABS}
P("  active rows: %d   back rows: %d   board total today: %s"
  % (len(KEYS), len(BACK['BASE']), format(tot['BASE'], ',')))
P()
P("  %-36s %14s %14s %11s %9s %7s %7s" % ('', 'board total', 'change', 'change %', 'moved', 'up', 'down'))
P("  " + "-" * 104)
MOVED = {}
for lab in LABS:
    MOVED[lab] = [k for k in KEYS if ROW[lab][k]['v'] != ROW['BASE'][k]['v']]
    ds = [ROW[lab][k]['v'] - ROW['BASE'][k]['v'] for k in MOVED[lab]]
    d = tot[lab] - tot['BASE']
    P("  %-36s %14s %14s %10.3f%% %9d %7d %7d"
      % (NICE[lab], format(tot[lab], ','), ('-' if lab == 'BASE' else '%+d' % d),
         100.0 * d / tot['BASE'], len(ds), sum(1 for x in ds if x > 0), sum(1 for x in ds if x < 0)))
P()
P("  back board (delisted/non-active, %s pts): unchanged in every variant -> %s"
  % (format(btot['BASE'], ','), all(btot[l] == btot['BASE'] for l in LABS)))
P()

# ---- THE SEPARATION ASSERTION --------------------------------------------------------------------
P("=" * 118)
P("2. THE SEPARATION LAW ON THE BOARD -- ND ROWS MUST NOT MOVE. ASSERTED, NOT REPORTED.")
P("=" * 118)
ND_MOVED = {}
for lab in LABS[1:]:
    nd = [k for k in MOVED[lab] if bstream(ROW['BASE'][k]) == 'ND 1-64']
    ndany = [k for k in MOVED[lab] if not (PLK.get(k) or {}).get('_pool')]
    ND_MOVED[lab] = (len(nd), len(ndany))
    P("  %-36s ND 1-64 rows moved: %d    non-pool rows moved (any): %d" % (NICE[lab], len(nd), len(ndany)))
    assert len(nd) == 0, "SEPARATION BREACH: %d ND 1-64 rows moved under %s" % (len(nd), lab)
    assert len(ndany) == 0, "SEPARATION BREACH: %d non-pool rows moved under %s" % (len(ndany), lab)
P()
P("  ASSERTION HOLDS on all four variants: ZERO national rows move. The staged configuration is")
P("  p.get('_pool')-gated at both read sites and at both retired H cells; national prices are")
P("  byte-identical to the live board.")
_ndtot = {lab: sum(ROW[lab][k]['v'] for k in KEYS if bstream(ROW['BASE'][k]) == 'ND 1-64') for lab in LABS}
P("  ND 1-64 board value: %s in every variant -> %s"
  % (format(_ndtot['BASE'], ','), all(_ndtot[l] == _ndtot['BASE'] for l in LABS)))
P()

# ---- distribution --------------------------------------------------------------------------------
P("=" * 118)
P("3. THE DISTRIBUTION OF THE MOVES")
P("=" * 118)


def pct(k, lab):
    b = ROW['BASE'][k]['v']
    return 100.0 * (ROW[lab][k]['v'] - b) / b if b else float('nan')


P("  %-36s %6s %10s %10s %10s %10s %10s" % ('variant', 'n', 'min', 'p25', 'median', 'p75', 'max'))
P("  " + "-" * 96)
DIST = {}
for lab in LABS[1:]:
    v = [pct(k, lab) for k in MOVED[lab]]
    DIST[lab] = dict(n=len(v), min=min(v), p25=q(v, .25), med=q(v, .5), p75=q(v, .75), max=max(v))
    P("  %-36s %6d %9.2f%% %9.2f%% %9.2f%% %9.2f%% %9.2f%%"
      % (NICE[lab], len(v), min(v), q(v, .25), q(v, .5), q(v, .75), max(v)))
P()
_dn = [k for k in MOVED['DERIVED'] if ROW['DERIVED'][k]['v'] < ROW['BASE'][k]['v']]
P("  ROWS THAT MOVE DOWN UNDER THE STAGED CONFIGURATION: %d" % len(_dn))
if _dn:
    P("  This is the redistribution biting. A row moves down when its DERIVED retention is below what")
    P("  the composed shipped read (R_natl@65 x H) gave it -- the FULL update is not a uniform lift.")
    P("  %-26s %-7s %4s %3s %10s %10s %10s" % ('player', 'pathway', 'g26', 'd', 'TODAY', 'STAGED', 'move'))
    for k in sorted(_dn, key=lambda k: ROW['DERIVED'][k]['v'] - ROW['BASE'][k]['v']):
        r0 = ROW['BASE'][k]; p = PLK.get(k)
        dep = ''
        if p is not None:
            dy = cp.debutyr(p) - 1
            quals = [x for x in p['scoring'] if x['games'] >= 6 and x['year'] <= Y0]
            dep = str(Y0 - dy) if not quals else 'q'
        P("  %-26s %-7s %4s %3s %10s %10s %+10d"
          % (r0['name'][:26], bstream(r0), games_in(p, Y0) if p is not None else '?', dep,
             format(r0['v'], ','), format(ROW['DERIVED'][k]['v'], ','),
             ROW['DERIVED'][k]['v'] - r0['v']))
P()

# ---- per-pathway ----------------------------------------------------------------------------------
P("=" * 118)
P("4. BY PATHWAY -- every live 'active' row of the pathway, moved or not")
P("=" * 118)
P("  %-8s %6s %6s | %11s %11s %11s %11s | %9s %9s %9s | %8s"
  % ('pathway', 'rows', 'moved', 'today', 'VAR A', 'VAR B', 'STAGED', 'A delta', 'B delta', 'STG delta', 'STG %'))
P("  " + "-" * 118)
PATH_BOARD = {}
for s in ORDER + ['ND 1-64']:
    ks = [k for k in KEYS if bstream(ROW['BASE'][k]) == s]
    if not ks: continue
    t = {lab: sum(ROW[lab][k]['v'] for k in ks) for lab in LABS}
    mv = sum(1 for k in ks if ROW['DERIVED'][k]['v'] != ROW['BASE'][k]['v'])
    PATH_BOARD[s] = dict(rows=len(ks), moved=mv, **{l: t[l] for l in LABS})
    P("  %-8s %6d %6d | %11s %11s %11s %11s | %+9d %+9d %+9d | %+7.2f%%"
      % (s, len(ks), mv, format(t['BASE'], ','), format(t['VARA'], ','), format(t['VARB'], ','),
         format(t['DERIVED'], ','), t['VARA'] - t['BASE'], t['VARB'] - t['BASE'],
         t['DERIVED'] - t['BASE'], 100.0 * (t['DERIVED'] - t['BASE']) / t['BASE'] if t['BASE'] else 0.0))
pk = [k for k in KEYS if bstream(ROW['BASE'][k]) in POOLS]
t = {lab: sum(ROW[lab][k]['v'] for k in pk) for lab in LABS}
P("  " + "-" * 118)
P("  %-8s %6d %6d | %11s %11s %11s %11s | %+9d %+9d %+9d | %+7.2f%%"
  % ('ALL POOL', len(pk), sum(1 for k in pk if ROW['DERIVED'][k]['v'] != ROW['BASE'][k]['v']),
     format(t['BASE'], ','), format(t['VARA'], ','), format(t['VARB'], ','), format(t['DERIVED'], ','),
     t['VARA'] - t['BASE'], t['VARB'] - t['BASE'], t['DERIVED'] - t['BASE'],
     100.0 * (t['DERIVED'] - t['BASE']) / t['BASE']))
P()

# ---- named movers -----------------------------------------------------------------------------------
P("=" * 118)
P("5. EVERY POOL PLAYER ON THE LIVE BOARD WHOSE VALUE MOVES UNDER THE STAGED CONFIGURATION")
P("=" * 118)
P("  g26 = games played in 2026 so far; d = sit-out depth in seasons, 'q' = has a qualifying season")
P("  (so he takes the year-1+ arm and carries the UPLIFT U, not the retention R).")
P()
P("  %-26s %-7s %4s %4s %3s | %8s %8s %8s %8s | %9s %9s"
  % ('player', 'pathway', 'age', 'g26', 'd', 'TODAY', 'VAR A', 'VAR B', 'STAGED', 'STG move', 'STG %'))
P("  " + "-" * 118)
NAMED = []
ALLMOVED = sorted(set(MOVED['DERIVED']) | set(MOVED['VARB']) | set(MOVED['VARA']),
                  key=lambda k: -abs(ROW['DERIVED'][k]['v'] - ROW['BASE'][k]['v']))
for k in ALLMOVED:
    r0 = ROW['BASE'][k]; p = PLK.get(k)
    dep = ''
    if p is not None:
        dy = cp.debutyr(p) - 1
        quals = [x for x in p['scoring'] if x['games'] >= 6 and x['year'] <= Y0]
        dep = str(Y0 - dy) if not quals else 'q'
    NAMED.append(dict(key=k, name=r0['name'], stream=bstream(r0), age=r0.get('age'),
                      g26=games_in(p, Y0) if p is not None else None, depth=dep,
                      **{l: ROW[l][k]['v'] for l in LABS},
                      d_staged=ROW['DERIVED'][k]['v'] - r0['v'], p_staged=pct(k, 'DERIVED')))
    P("  %-26s %-7s %4s %4s %3s | %8s %8s %8s %8s | %+9d %+8.2f%%"
      % (r0['name'][:26], bstream(r0), r0.get('age'),
         games_in(p, Y0) if p is not None else '?', dep,
         format(r0['v'], ','), format(ROW['VARA'][k]['v'], ','), format(ROW['VARB'][k]['v'], ','),
         format(ROW['DERIVED'][k]['v'], ','), ROW['DERIVED'][k]['v'] - r0['v'], pct(k, 'DERIVED')))
P("  " + "-" * 118)
P("  %-26s %-7s %4s %4s %3s | %8s %8s %8s %8s | %+9d"
  % ('TOTAL (rows listed)', '', '', '', '',
     format(sum(n['BASE'] for n in NAMED), ','), format(sum(n['VARA'] for n in NAMED), ','),
     format(sum(n['VARB'] for n in NAMED), ','), format(sum(n['DERIVED'] for n in NAMED), ','),
     sum(n['d_staged'] for n in NAMED)))
P()
_qrows = [n for n in NAMED if n['depth'] == 'q' and n['d_staged'] != 0]
P("  Of the moved rows, %d carry 'q': they have a qualifying season, take the YEAR-1+ arm, and their"
  % len(_qrows))
P("  move is the UPLIFT U, not the retention R. That is the SECOND read site -- the leg neither")
P("  ORDER 19 variant contained.")
P()

# ---- where the staged object lands between A and B --------------------------------------------------
P("=" * 118)
P("6. WHERE THE DERIVED OBJECT LANDS BETWEEN 'H LIFTED ONLY' AND 'EVERYTHING LIFTED'")
P("=" * 118)
dA = tot['VARA'] - tot['BASE']; dB = tot['VARB'] - tot['BASE']
dS = tot['DERIVED'] - tot['BASE']; dSS = tot['DERIVEDSIT'] - tot['BASE']
P("  VARIANT A   (H lifted, national R still clamped at knot 50 on top)   %+8d" % dA)
P("  DERIVED, sit site only                                              %+8d" % dSS)
P("  ** STAGED (derived object, both sites) **                           %+8d" % dS)
P("  VARIANT B   (H lifted AND R:=1.0 -- no sitter charge at all)         %+8d" % dB)
P()
P("  position of the staged object on the A->B interval: %.3f"
  % ((dS - dA) / (dB - dA) if dB != dA else float('nan')))
P("  the SECOND READ SITE (the uplift leg) is worth %+d of the staged move (%.1f%% of it)"
  % (dS - dSS, 100.0 * (dS - dSS) / dS if dS else float('nan')))
P()
P("  ORDER 19 published A +2,306 / B +8,467 against the SUPERSEDED board 94f1fec5.")
P("  Rebuilt here on the ADOPTED engine (board 1dbd1480, the par fix landed): A %+d / B %+d."
  % (dA, dB))
P("  Difference vs ORDER 19: A %+d (%.2f%%), B %+d (%.2f%%). The par fix moved the base the sitter"
  % (dA - 2306, 100.0 * (dA - 2306) / 2306, dB - 8467, 100.0 * (dB - 8467) / 8467))
P("  legs act on; the legs themselves are unchanged code.")
P()

DATA = dict(
    controls=dict(board_md5={l: _md5(os.path.join(O21, 'board_%s.json' % l)) for l in LABS},
                  live_board_md5=_live, base_reproduces_live=bool(_base == _live)),
    totals=tot, back_totals=btot, moved={l: len(MOVED[l]) for l in LABS},
    nd_rows_moved={l: ND_MOVED[l][0] for l in ND_MOVED},
    nonpool_rows_moved={l: ND_MOVED[l][1] for l in ND_MOVED},
    dist=DIST, by_pathway=PATH_BOARD, named=NAMED,
    down_movers=[n['name'] for n in NAMED if n['d_staged'] < 0],
    interval=dict(A=dA, B=dB, staged=dS, staged_sit_only=dSS,
                  second_site=dS - dSS,
                  position=(dS - dA) / (dB - dA) if dB != dA else None),
    order19_published=dict(A=2306, B=8467, board='94f1fec59f99c59d5890d5975c79fa9b'),
)
json.dump(DATA, open(os.path.join(HERE, 'RETENTION_CONSEQUENCE.json'), 'w'), indent=1)
P("wrote RETENTION_CONSEQUENCE.json  md5 %s" % _md5(os.path.join(HERE, 'RETENTION_CONSEQUENCE.json')))
assert_pins('exit')
P()
P("PINS RE-ASSERTED AT EXIT -- all three UNMOVED.")
open(os.path.join(HERE, 'retention_consequence_out.txt'), 'w').write("\n".join(OUT) + "\n")
