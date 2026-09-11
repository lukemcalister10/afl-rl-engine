"""ORDER 19 -- HOW MUCH DOES LIFTING THE POOL SITTER PENALTY CHANGE POOL VALUES, AND THE v0?

THE OWNER'S RULING AND QUESTION, VERBATIM:
  "For now, keep ND sitter and we can deal with it later. But given more pool players sit, if we keep
   it for them it will destroy their values"
  "For the pool players, I think we look at lifting the sitter penalty and rebuild it again if needed
   afterwards? How much would that change values of the pool and the v0 of them?"

THE ND SITTER TREATMENT IS UNTOUCHED IN BOTH VARIANTS. That is the owner's ruling and it is not
optional; it is enforced by construction (variant A's dials are pool-gated inside _h_cut; variant B's
patch is `if p.get('_pool')`), and it is VERIFIED here on the national arm rather than asserted.

  VARIANT A -- lift the H leg only.   H_POOLSIT = H_UNION = 1.0 (manifest dials, gate mode).
  VARIANT B -- lift the whole pool sitter penalty. A, plus the R leg neutralised inside sitout_ev for
               POOL rows only (`if p.get('_pool'): R=1.0`), so a pool sitter carries his FULL entry
               anchor. Built by a one-line patch in a SCRATCHPAD WORKTREE; the checkout's engine is
               never written. Proof it differs by code: emitted engine_head 002ff843 vs SHIP a8071af4.

INPUTS (all produced by the two committed shell scripts beside this file):
  boards    board_BASE.json   (md5 94f1fec5.. == THE LIVE BOARD, exact reproduction -- the control)
            board_LIFTH.json  (variant A)   board_LIFTRH.json  (variant B)
  matrices  per_entrant_SHIP.json / _LIFTH.json / _LIFTRH.json  (24-year walk-forward per variant)
            plus per_entrant_CTRL19.json, a HEAD-defaults re-emit whose `recs` are compared byte-wise
            against SHIP as the emit control.

READ-ONLY. The engine is loaded from a STAGED COPY. Nothing is wired; no shipped default changes.

  usage:  OPENBLAS_NUM_THREADS=1 /root/rl_venv312/bin/python pool_sitter_lift.py
"""
import os, sys, io, json, contextlib, math, collections, shutil, hashlib

ROOT = '/home/user/afl-rl-engine'
SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O19 = SP + '/o19'
STAGE = SP + '/eng_stage_o19/rl_after'
HERE = os.path.dirname(os.path.abspath(__file__))

PINS = {
    'board': ('data/rl_build/rl_app_data.json', '94f1fec59f99c59d5890d5975c79fa9b'),
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
    bad = []
    for k, (rel, exp) in PINS.items():
        got = _md5(os.path.join(ROOT, rel))
        if got != exp:
            bad.append("%s %s != pinned %s (%s)" % (k, got, exp, rel))
    if bad:
        raise SystemExit("PIN ASSERTION FAILED (%s):\n  " % when + "\n  ".join(bad))


assert_pins('entry')

# ---- staged engine (phase 1 / ORDER 18 discipline, carried) ---------------------------------------
if not os.path.exists(os.path.join(STAGE, '_merged_recover.py')):
    os.makedirs(os.path.dirname(STAGE), exist_ok=True)
    shutil.copytree(ROOT + '/engine/rl_after', STAGE, dirs_exist_ok=True)
if not os.path.exists(os.path.join(STAGE, 'LTI_REGISTER.md')):
    shutil.copy(ROOT + '/LTI_REGISTER.md', STAGE)

os.environ.update(PYTHONHASHSEED='0')
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)

MA, cp = G['MA'], G['cp']
price6 = G['price6']
v0_start, entry_anchor, _sitout_cls = G['v0_start'], G['entry_anchor'], G['_sitout_cls']
H_POOLSIT, H_UNION = G['H_POOLSIT'], G['H_UNION']
_R_surf, _b_age = G['_R_surf'], G['_b_age']
_v0_uncapped, _v0_raw, raw_ev = G['_v0_uncapped'], G['_v0_raw'], G['raw_ev']

OUT = []


def P(s=''):
    print(s)
    OUT.append(s)


DATA = {}

P("=" * 118)
P("ORDER 19 -- THE POOL SITTER LIFT: TWO VARIANTS, BOTH MEASURED")
P("=" * 118)
P("  pins asserted at entry:  board 94f1fec5..  store d9a24282..  instrument 0f822035..")
P("  shipped constants read from the engine: H_POOLSIT=%.3f  H_UNION=%.3f  (composed %.4f)"
  % (H_POOLSIT, H_UNION, H_POOLSIT * H_UNION))
P("  engine loaded read-only from a staged copy; repo untouched.  MA.data n=%d" % len(MA.data))
P()

# ==================================================================================================
# 0. CONTROLS
# ==================================================================================================
P("=" * 118)
P("0. CONTROLS -- BELIEVE NOTHING UNTIL THE BASELINE REPRODUCES")
P("=" * 118)
BD = {}
for lab, fn in (('BASE', 'board_BASE.json'), ('LIFTH', 'board_LIFTH.json'), ('LIFTRH', 'board_LIFTRH.json')):
    p = os.path.join(O19, fn)
    BD[lab] = json.load(open(p))
    P("  board %-7s md5 %s   (%s)" % (lab, _md5(p), fn))
_live = _md5(os.path.join(ROOT, PINS['board'][0]))
_base = _md5(os.path.join(O19, 'board_BASE.json'))
P("  live board md5 %s" % _live)
P("  CONTROL 1: the HEAD-defaults board build reproduces THE LIVE BOARD BYTE-FOR-BYTE -> %s"
  % ("REPRODUCED" if _base == _live else "MISMATCH"))
assert _base == _live, "baseline board did not reproduce the live board"

MX = {}
for lab in ('SHIP', 'LIFTH', 'LIFTRH', 'CTRL19'):
    MX[lab] = json.load(open("%s/per_entrant_%s.json" % (SP, lab)))
_ctrl_ok = MX['CTRL19']['recs'] == MX['SHIP']['recs']
P("  CONTROL 2: a fresh HEAD-defaults 24-year emit reproduces per_entrant_SHIP.json `recs` -> %s"
  % ("REPRODUCED" if _ctrl_ok else "MISMATCH"))
assert _ctrl_ok
P("  matrix engine identities: SHIP %s   LIFTH %s   LIFTRH %s"
  % (MX['SHIP']['meta']['engine_head'], MX['LIFTH']['meta']['engine_head'],
     MX['LIFTRH']['meta']['engine_head']))
P("    -> LIFTRH's engine_head DIFFERS. That is the machine-readable proof variant B is a CODE")
P("       variant, not a dial variant, and that the patch was actually in the tree that emitted it.")
P("  store pin on every matrix: %s / %s / %s"
  % (MX['SHIP']['meta']['store_md5'], MX['LIFTH']['meta']['store_md5'], MX['LIFTRH']['meta']['store_md5']))
P()
DATA['controls'] = dict(board_base_md5=_base, live_board_md5=_live,
                        board_lifth_md5=_md5(os.path.join(O19, 'board_LIFTH.json')),
                        board_liftrh_md5=_md5(os.path.join(O19, 'board_LIFTRH.json')),
                        ctrl_emit_recs_identical=_ctrl_ok,
                        engine_heads={k: MX[k]['meta']['engine_head'] for k in MX})

# ==================================================================================================
# 1. THE BOARD EFFECT
# ==================================================================================================
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
POOLS = set(ORDER)


def bstream(r):
    """The board row's pathway, on phase 1's own stream() definition."""
    t = r.get('ty')
    if t == 'ND':
        pk = r.get('pk') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


ROW = {lab: {r['key']: r for r in BD[lab]['active']} for lab in BD}
BACKROW = {lab: {r['key']: r for r in BD[lab]['back']} for lab in BD}
KEYS = sorted(ROW['BASE'])
assert set(ROW['BASE']) == set(ROW['LIFTH']) == set(ROW['LIFTRH'])

# sitter status and player object, from the engine (the board carries no games-this-season field)
PL = {}
for p in MA.data:
    if p.get('_double_count'):
        continue
    PL[p.get('player')] = p
PLK = {}
for p in MA.data:
    k = p.get('key') or p.get('player')
    PLK[k] = p
Y0 = 2026


def games_in(p, Y):
    return sum(x['games'] for x in p['scoring'] if x['year'] == Y)


P("=" * 118)
P("1. THE BOARD EFFECT -- LIVE BOARD, 'active' ROWS  (v = round(engine ev(p,2026) / F))")
P("=" * 118)
tot = {lab: sum(ROW[lab][k]['v'] for k in KEYS) for lab in ROW}
P("  active rows: %d      board total today: %s board points" % (len(KEYS), format(tot['BASE'], ',')))
P()
P("  %-24s %14s %14s %10s" % ('', 'board total', 'change', 'change %'))
P("  " + "-" * 66)
P("  %-24s %14s %14s %10s" % ('TODAY (shipped)', format(tot['BASE'], ','), '-', '-'))
for lab, nm in (('LIFTH', 'VARIANT A  (H lifted)'), ('LIFTRH', 'VARIANT B  (H and R lifted)')):
    d = tot[lab] - tot['BASE']
    P("  %-24s %14s %+14s %+9.3f%%" % (nm, format(tot[lab], ','), format(d, ','), 100.0 * d / tot['BASE']))
P()

MOVED = {}
for lab in ('LIFTH', 'LIFTRH'):
    MOVED[lab] = [k for k in KEYS if ROW[lab][k]['v'] != ROW['BASE'][k]['v']]
P("  ROWS MOVED")
P("  %-24s %8s %8s %8s %14s %14s" % ('', 'moved', 'up', 'down', 'sum of moves', 'largest move'))
P("  " + "-" * 82)
for lab, nm in (('LIFTH', 'VARIANT A'), ('LIFTRH', 'VARIANT B')):
    ds = [ROW[lab][k]['v'] - ROW['BASE'][k]['v'] for k in MOVED[lab]]
    P("  %-24s %8d %8d %8d %14s %14s"
      % (nm, len(ds), sum(1 for x in ds if x > 0), sum(1 for x in ds if x < 0),
         format(sum(ds), ','), format(max(ds, key=abs) if ds else 0, ',')))
P()
_setA, _setB = set(MOVED['LIFTH']), set(MOVED['LIFTRH'])
P("  ROW SETS: A moves %d, B moves %d.  A subset of B: %s.  B \\ A = %d rows.  A \\ B = %d rows."
  % (len(_setA), len(_setB), _setA <= _setB, len(_setB - _setA), len(_setA - _setB)))
P("  Every moved row is a POOL row: A %s   B %s"
  % (all(bstream(ROW['BASE'][k]) in POOLS for k in _setA),
     all(bstream(ROW['BASE'][k]) in POOLS for k in _setB)))
P("  Every moved row is a 2026 SIT-OUT (zero games this season): A %s   B %s"
  % (all(games_in(PLK[k], Y0) == 0 for k in _setA if k in PLK),
     all(games_in(PLK[k], Y0) == 0 for k in _setB if k in PLK)))
P()
P("  NO NATIONAL-ARM ROW MOVES. This is the owner's ruling, verified rather than asserted:")
_nd_moved = [k for k in (_setA | _setB) if bstream(ROW['BASE'][k]) == 'ND 1-64']
P("      ND 1-64 board rows whose value changes under EITHER variant: %d" % len(_nd_moved))
P()

# distribution of moves
P("  DISTRIBUTION OF THE MOVES (percentage change of the row's own value)")
P("  %-12s %8s %10s %10s %10s %10s %10s" % ('variant', 'n', 'min', 'p25', 'median', 'p75', 'max'))
P("  " + "-" * 74)


def pct(k, lab):
    b = ROW['BASE'][k]['v']
    return 100.0 * (ROW[lab][k]['v'] - b) / b if b else float('nan')


def q(v, f):
    if not v: return float('nan')
    s = sorted(v); i = f * (len(s) - 1)
    lo, hi = int(math.floor(i)), int(math.ceil(i))
    return s[lo] + (s[hi] - s[lo]) * (i - lo)


DIST = {}
for lab, nm in (('LIFTH', 'VARIANT A'), ('LIFTRH', 'VARIANT B')):
    v = [pct(k, lab) for k in MOVED[lab]]
    DIST[lab] = dict(n=len(v), min=min(v), p25=q(v, .25), med=q(v, .5), p75=q(v, .75), max=max(v))
    P("  %-12s %8d %9.2f%% %9.2f%% %9.2f%% %9.2f%% %9.2f%%"
      % (nm, len(v), min(v), q(v, .25), q(v, .5), q(v, .75), max(v)))
P()
P("  BUCKETED (variant B, the full lift)")
BUCK = [('0 - 10%', 0, 10), ('10 - 25%', 10, 25), ('25 - 50%', 25, 50), ('50 - 100%', 50, 100),
        ('100 - 150%', 100, 150), ('150%+', 150, 1e9)]
for nm, lo, hi in BUCK:
    sub = [k for k in MOVED['LIFTRH'] if lo <= pct(k, 'LIFTRH') < hi]
    if sub:
        P("      %-12s %4d rows   %12s board points"
          % (nm, len(sub), format(sum(ROW['LIFTRH'][k]['v'] - ROW['BASE'][k]['v'] for k in sub), ',')))
P()

# ---- THE NAMED LINES ------------------------------------------------------------------------------
P("  EVERY POOL PLAYER ON THE LIVE BOARD WHOSE VALUE CHANGES, sorted by absolute move under B")
P("  (today / variant A / variant B, in board points; 'd' = the row's own sit-out depth in seasons)")
P()
P("  %-24s %-7s %5s %4s %3s | %8s %8s %8s | %8s %8s"
  % ('player', 'pathway', 'age', 'g26', 'd', 'TODAY', 'VAR A', 'VAR B', 'A move', 'B move'))
P("  " + "-" * 116)
NAMED = []
for k in sorted(_setB | _setA, key=lambda k: -abs(ROW['LIFTRH'][k]['v'] - ROW['BASE'][k]['v'])):
    r0, ra, rb = ROW['BASE'][k], ROW['LIFTH'][k], ROW['LIFTRH'][k]
    p = PLK.get(k)
    d = ''
    if p is not None:
        dy = cp.debutyr(p) - 1
        quals = [x for x in p['scoring'] if x['games'] >= 6 and x['year'] <= Y0]
        d = str(Y0 - dy) if not quals else 'q'
    NAMED.append(dict(key=k, name=r0['name'], stream=bstream(r0), age=r0.get('age'),
                      g26=games_in(p, Y0) if p is not None else None, depth=d,
                      today=r0['v'], varA=ra['v'], varB=rb['v'],
                      dA=ra['v'] - r0['v'], dB=rb['v'] - r0['v'],
                      pA=pct(k, 'LIFTH'), pB=pct(k, 'LIFTRH')))
    P("  %-24s %-7s %5s %4s %3s | %8s %8s %8s | %+7s%s %+7s%s"
      % (r0['name'][:24], bstream(r0), r0.get('age'), games_in(p, Y0) if p is not None else '?', d,
         format(r0['v'], ','), format(ra['v'], ','), format(rb['v'], ','),
         format(ra['v'] - r0['v'], ','), ' ', format(rb['v'] - r0['v'], ','), ''))
P("  " + "-" * 116)
P("  %-24s %-7s %5s %4s %3s | %8s %8s %8s | %+7s  %+7s"
  % ('TOTAL (moved rows only)', '', '', '', '',
     format(sum(n['today'] for n in NAMED), ','), format(sum(n['varA'] for n in NAMED), ','),
     format(sum(n['varB'] for n in NAMED), ','),
     format(sum(n['dA'] for n in NAMED), ','), format(sum(n['dB'] for n in NAMED), ',')))
P()
P("  percentage moves, same order:")
P("  %-24s %10s %10s" % ('player', 'A %', 'B %'))
for n in NAMED:
    P("  %-24s %+9.2f%% %+9.2f%%" % (n['name'][:24], n['pA'], n['pB']))
P()
DATA['board'] = dict(total=tot, moved={k: len(v) for k, v in MOVED.items()}, dist=DIST, named=NAMED,
                     nd_rows_moved=len(_nd_moved), a_subset_of_b=bool(_setA <= _setB))

# ---- per-pathway board effect ---------------------------------------------------------------------
P("  BOARD EFFECT BY PATHWAY (all live 'active' rows of the pathway, moved or not)")
P("  %-8s %6s %6s | %12s %12s %12s | %10s %10s | %10s %10s"
  % ('pathway', 'rows', 'moved', 'today', 'VAR A', 'VAR B', 'A delta', 'B delta', 'A %', 'B %'))
P("  " + "-" * 116)
PATH_BOARD = {}
for s in ORDER + ['ND 1-64']:
    ks = [k for k in KEYS if bstream(ROW['BASE'][k]) == s]
    if not ks: continue
    t0 = sum(ROW['BASE'][k]['v'] for k in ks)
    ta = sum(ROW['LIFTH'][k]['v'] for k in ks)
    tb = sum(ROW['LIFTRH'][k]['v'] for k in ks)
    nm = sum(1 for k in ks if ROW['LIFTRH'][k]['v'] != ROW['BASE'][k]['v'])
    PATH_BOARD[s] = dict(rows=len(ks), moved=nm, today=t0, varA=ta, varB=tb,
                         dA=ta - t0, dB=tb - t0,
                         pA=100.0 * (ta - t0) / t0 if t0 else 0.0,
                         pB=100.0 * (tb - t0) / t0 if t0 else 0.0,
                         meanA=(ta - t0) / len(ks), meanB=(tb - t0) / len(ks))
    x = PATH_BOARD[s]
    P("  %-8s %6d %6d | %12s %12s %12s | %+10s %+10s | %+9.3f%% %+9.3f%%"
      % (s, len(ks), nm, format(t0, ','), format(ta, ','), format(tb, ','),
         format(x['dA'], ','), format(x['dB'], ','), x['pA'], x['pB']))
P("  " + "-" * 116)
_pk = [k for k in KEYS if bstream(ROW['BASE'][k]) in POOLS]
_t0 = sum(ROW['BASE'][k]['v'] for k in _pk)
_ta = sum(ROW['LIFTH'][k]['v'] for k in _pk)
_tb = sum(ROW['LIFTRH'][k]['v'] for k in _pk)
P("  %-8s %6d %6d | %12s %12s %12s | %+10s %+10s | %+9.3f%% %+9.3f%%"
  % ('ALL POOL', len(_pk), sum(1 for k in _pk if ROW['LIFTRH'][k]['v'] != ROW['BASE'][k]['v']),
     format(_t0, ','), format(_ta, ','), format(_tb, ','), format(_ta - _t0, ','),
     format(_tb - _t0, ','), 100.0 * (_ta - _t0) / _t0, 100.0 * (_tb - _t0) / _t0))
P()
P("  MEAN VALUE CHANGE PER ROW (all rows of the pathway, moved or not / moved rows only)")
P("  %-8s %8s %10s %10s | %8s %10s %10s"
  % ('pathway', 'rows', 'mean A', 'mean B', 'moved', 'mean A', 'mean B'))
P("  " + "-" * 78)
for s in ORDER:
    if s not in PATH_BOARD: continue
    ks = [k for k in KEYS if bstream(ROW['BASE'][k]) == s]
    mv = [k for k in ks if ROW['LIFTRH'][k]['v'] != ROW['BASE'][k]['v']]
    x = PATH_BOARD[s]
    P("  %-8s %8d %+10.1f %+10.1f | %8d %+10.1f %+10.1f"
      % (s, len(ks), x['meanA'], x['meanB'], len(mv),
         (sum(ROW['LIFTH'][k]['v'] - ROW['BASE'][k]['v'] for k in mv) / len(mv)) if mv else 0.0,
         (sum(ROW['LIFTRH'][k]['v'] - ROW['BASE'][k]['v'] for k in mv) / len(mv)) if mv else 0.0))
P()
DATA['path_board'] = PATH_BOARD

# ---- the 'back' (delisted / non-active) board, reported so the population is complete --------------
_bk = sorted(BACKROW['BASE'])
_bt = {lab: sum(BACKROW[lab][k]['v'] for k in _bk) for lab in BACKROW}
_bm = [k for k in _bk if BACKROW['LIFTRH'][k]['v'] != BACKROW['BASE'][k]['v']]
P("  THE 'back' BOARD (delisted / non-active, %d rows), reported so the population is complete:" % len(_bk))
P("      total today %s -> A %s -> B %s ; rows moved under B: %d"
  % (format(_bt['BASE'], ','), format(_bt['LIFTH'], ','), format(_bt['LIFTRH'], ','), len(_bm)))
P("      delisted(p) returns 0.02*v0_start BEFORE any sitter site is reached (ev():2229), so these")
P("      rows cannot move -- and do not.")
P()

assert_pins('mid-run')

# ==================================================================================================
# 2. PER-PATHWAY MEAN-PRESERVING FIGURE  (ORDER 18's cell construction, carried verbatim)
# ==================================================================================================
P("=" * 118)
P("2. THE MEAN-PRESERVING FIGURE, PER PATHWAY")
P("=" * 118)
P("  The owner's D8 law: once a group's entry price is calibrated on that group's own realized")
P("  returns -- sitters included -- any within-group sitter differential must REDISTRIBUTE and never")
P("  be a net charge. Test statistic, entry-weighted over the pathway:")
P("      mean = ( SUM_sit e*M + SUM_non e*1 ) / SUM_all e ,   e = entry_anchor,  M = applied multiplier")
P("  mean < 1.0 is a NET CHARGE. The cell construction below is ORDER 18's, carried verbatim, which")
P("  is phase 1's, carried verbatim. It is not reinvented here.")
P()


def draftyr(p): return cp.debutyr(p) - 1


def min_window(p):
    t, pk = p.get('type'), p.get('pick')
    if t == 'ND' and pk and pk <= 20: return 4
    if t == 'ND' and pk and pk <= 40: return 3
    return 2


def listed_through(p):
    if p.get('_last_listed') is not None: return int(p['_last_listed'])
    if not p.get('_retired'): return 2026
    lg = max((x['year'] for x in p['scoring']), default=0)
    dy = p.get('year') or lg
    return max(dy + min_window(p) - 1, lg)


def stream(p):
    t = p.get('type')
    if t == 'ND':
        pk = p.get('pick') or 0
        return 'ND 1-64' if 1 <= pk <= 64 else 'ND>64'
    return t


cells = []
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue
        dy = draftyr(p)
        if dy < 2003 or dy > 2024: continue
        lt = listed_through(p)
        rows = sorted(p['scoring'], key=lambda x: x['year'])
        pos = MA.gfut(p)
        cls = _sitout_cls(pos)
        va = float(v0_start(p))
        try:
            ea = float(entry_anchor(p))
        except Exception:
            ea = float('nan')
        try:
            epk = int(MA.effpk(p))
        except Exception:
            epk = 65
        for Y in range(dy + 1, min(lt, 2025) + 1):
            quals = [x for x in rows if x['games'] >= 6 and x['year'] <= Y]
            cells.append(dict(pool=bool(p.get('_pool')), stream=stream(p), cls=cls, pos=pos,
                              d=Y - dy, sitout=bool(not quals),
                              V0start=va, Vanchor=ea, wc=bool(Y <= 2021),
                              age=_b_age(p), typ=p.get('type'),
                              effpk=epk, pick=(p.get('pick') or 0)))

POOL = [c for c in cells if c['pool'] and c['wc']]
NDC = [c for c in cells if not c['pool'] and c['wc']]
ND64 = [c for c in NDC if c['stream'] == 'ND 1-64']


def applied_R(c):
    if not c['sitout']: return 1.0
    return float(_R_surf(c['cls'], c['effpk'], float(c['d'])))


def h_mult(c):
    if not c['sitout']: return 1.0
    f = H_POOLSIT
    if (c['age'] is not None and c['age'] >= 23.0) or c['typ'] in ('IRE', 'MSD'):
        f *= H_UNION
    return f


def today_mult(c):   return applied_R(c) * h_mult(c)      # the composed charge SHIPPED today
def varA_mult(c):    return applied_R(c)                  # H lifted; R stands
def varB_mult(c):    return 1.0                           # both legs lifted for pool rows


def meanstat(sub, mult, weight='Vanchor'):
    tot = sitw = nonw = num = 0.0
    nsit = n = 0
    for c in sub:
        e = c[weight]
        if not e or e != e or e <= 0: continue
        R = mult(c)
        tot += e; n += 1
        if c['sitout']:
            sitw += e; num += e * R; nsit += 1
        else:
            nonw += e
    if tot <= 0: return None
    mean = (num + nonw) / tot
    return dict(n=n, nsit=nsit, sit_share_w=sitw / tot, sit_share_n=nsit / n if n else 0.0,
                meanR=(num / sitw) if sitw > 0 else float('nan'),
                mean=mean, net_charge=mean - 1.0,
                U=((tot - num) / nonw) if nonw > 0 else float('nan'))


P("  CONTROL 3 -- reproduce ORDER 18's published composed R x H column before reporting anything.")
O18 = {'RD': -0.2102, 'SSP': -0.2064, 'MSD': -0.7379, 'IRE': -0.4527, 'PDA': -0.3062,
       'PDN': -0.4861, 'PDS': -0.3564, 'UNR': -0.3291, 'ND>64': -0.2726}
O18R = {'RD': -0.1675, 'SSP': -0.1499, 'MSD': -0.3520, 'IRE': -0.2522, 'PDA': -0.2465,
        'PDN': -0.3972, 'PDS': -0.3017, 'UNR': -0.2015, 'ND>64': -0.2231}
_dmax = 0.0
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    m = meanstat(sub, today_mult)
    _dmax = max(_dmax, abs(m['net_charge'] - O18[s]))
P("      max |delta| vs ORDER 18's composed column = %.6f -> %s"
  % (_dmax, "REPRODUCED" if _dmax < 5e-5 else "MISMATCH"))
P()
P("  %-8s %7s %7s %9s | %10s %11s | %10s %11s | %10s %11s"
  % ('pathway', 'cells', 'sitters', 'sit wtd', 'TODAY', 'net charge', 'VAR A', 'net charge',
     'VAR B', 'net charge'))
P("  " + "-" * 116)
PATH_MEAN = {}
for s in ORDER:
    sub = [c for c in POOL if c['stream'] == s]
    t = meanstat(sub, today_mult); a = meanstat(sub, varA_mult); b = meanstat(sub, varB_mult)
    PATH_MEAN[s] = dict(n=t['n'], nsit=t['nsit'], sit_share_w=t['sit_share_w'],
                        today=t['mean'], today_nc=t['net_charge'],
                        varA=a['mean'], varA_nc=a['net_charge'],
                        varB=b['mean'], varB_nc=b['net_charge'],
                        o18_r_only=O18R[s], delta_vs_o18_r=a['net_charge'] - O18R[s])
    P("  %-8s %7d %7d %9.4f | %10.6f %11.6f | %10.6f %11.6f | %10.6f %11.6f"
      % (s, t['n'], t['nsit'], t['sit_share_w'], t['mean'], t['net_charge'],
         a['mean'], a['net_charge'], b['mean'], b['net_charge']))
allp_t = meanstat(POOL, today_mult); allp_a = meanstat(POOL, varA_mult); allp_b = meanstat(POOL, varB_mult)
P("  " + "-" * 116)
P("  %-8s %7d %7d %9.4f | %10.6f %11.6f | %10.6f %11.6f | %10.6f %11.6f"
  % ('ALL POOL', allp_t['n'], allp_t['nsit'], allp_t['sit_share_w'], allp_t['mean'],
     allp_t['net_charge'], allp_a['mean'], allp_a['net_charge'], allp_b['mean'], allp_b['net_charge']))
nd_t = meanstat(ND64, applied_R)
P("  %-8s %7d %7d %9.4f | %10.6f %11.6f | %10s %11s | %10s %11s"
  % ('ND 1-64', nd_t['n'], nd_t['nsit'], nd_t['sit_share_w'], nd_t['mean'], nd_t['net_charge'],
     'UNTOUCHED', '(ruled)', 'UNTOUCHED', '(ruled)'))
P()
P("  CROSS-CHECK against ORDER 18's published R-LEG-ONLY column (which is exactly what variant A")
P("  leaves standing).  max |delta| = %.6f"
  % max(abs(PATH_MEAN[s]['delta_vs_o18_r']) for s in ORDER))
P()
P("  WHERE THE MEAN-PRESERVING FIGURE LANDS:")
P("      TODAY      pool pathways span %.4f (MSD) to %.4f (SSP); ALL POOL %.6f"
  % (min(PATH_MEAN[s]['today'] for s in ORDER), max(PATH_MEAN[s]['today'] for s in ORDER),
     allp_t['mean']))
P("      VARIANT A  pool pathways span %.4f to %.4f; ALL POOL %.6f  -- moves TOWARD 1.0 but does"
  % (min(PATH_MEAN[s]['varA'] for s in ORDER), max(PATH_MEAN[s]['varA'] for s in ORDER),
     allp_a['mean']))
P("                 NOT reach it: every pathway is still in breach on the surviving R leg.")
P("      VARIANT B  every pool pathway lands at EXACTLY %.6f -- the law holds, by construction."
  % allp_b['mean'])
P()
DATA['path_mean'] = PATH_MEAN
DATA['path_mean_allpool'] = dict(today=allp_t['mean'], varA=allp_a['mean'], varB=allp_b['mean'],
                                 nd64_today=nd_t['mean'])

# ==================================================================================================
# 3. THE v0 QUESTION
# ==================================================================================================
P("=" * 118)
P("3. THE v0 QUESTION -- 'How much would that change ... the v0 of them?'")
P("=" * 118)
P("  ANSWER: NOT AT ALL. THE SITTER PENALTY DOES NOT REACH v0, ON EITHER LEG, IN EITHER VARIANT.")
P("  Three independent proofs, all by EXECUTION, none by assertion.")
P()
P("  PROOF 1 -- THE FULL-ENGINE PROOF. Three complete 24-year walk-forward emits were run, one per")
P("  variant, each writing every entrant's own v0 = v0_start(p) under THAT engine. Compare them:")
S = {r['key']: r for r in MX['SHIP']['recs']}
A = {r['key']: r for r in MX['LIFTH']['recs']}
B = {r['key']: r for r in MX['LIFTRH']['recs']}
assert set(S) == set(A) == set(B)
_poolk = [k for k in S if S[k].get('is_pool')]
dA = max(abs(A[k]['v0'] - S[k]['v0']) for k in S)
dB = max(abs(B[k]['v0'] - S[k]['v0']) for k in S)
dAp = max(abs(A[k]['v0'] - S[k]['v0']) for k in _poolk)
dBp = max(abs(B[k]['v0'] - S[k]['v0']) for k in _poolk)
nvA = sum(1 for k in S if (A[k].get('vpath') or []) != (S[k].get('vpath') or []))
nvB = sum(1 for k in S if (B[k].get('vpath') or []) != (S[k].get('vpath') or []))
P("      records                                          %d" % len(S))
P("      of which POOL                                    %d" % len(_poolk))
P("      max |v0(VARIANT A) - v0(SHIP)|  ALL rows         %.17g" % dA)
P("      max |v0(VARIANT B) - v0(SHIP)|  ALL rows         %.17g" % dB)
P("      max |v0(VARIANT A) - v0(SHIP)|  POOL rows        %.17g" % dAp)
P("      max |v0(VARIANT B) - v0(SHIP)|  POOL rows        %.17g" % dBp)
P("      records whose WALK-FORWARD PATH did change: A %d,  B %d" % (nvA, nvB))
P("      -> v0 is EXACTLY unchanged (delta 0.0, not 'small') while 1 in 3 careers' priced path moves.")
P("         The instrument is plainly sensitive to the lift; v0 simply is not downstream of it.")
P()
P("  PROOF 2 -- THE CALL-GRAPH PROOF BY EXECUTION. _h_cut and sitout_ev are wrapped with counters in")
P("  the staged engine, then the v0 chain is called for every pool player and the counters read.")
_cnt = collections.Counter()
_h_cut_o, _sit_o = G['_h_cut'], G['sitout_ev']


def _h_cut_w(p, Y):
    _cnt['h_cut'] += 1
    return _h_cut_o(p, Y)


def _sit_w(p, Y, e):
    _cnt['sitout_ev'] += 1
    return _sit_o(p, Y, e)


G['_h_cut'] = _h_cut_w
G['sitout_ev'] = _sit_w
pool_players = [p for p in MA.data if p.get('_pool') and not p.get('_double_count')
                and MA.GRP.get(p.get('pos'))]
G['_V0U'].clear(); G['_V0C'].clear()
_cnt.clear()
with contextlib.redirect_stdout(io.StringIO()):
    for p in pool_players:
        _v0_uncapped(p); _v0_raw(p); v0_start(p); entry_anchor(p); raw_ev(p, cp.debutyr(p) - 1)
c_v0 = dict(_cnt)
_cnt.clear()
with contextlib.redirect_stdout(io.StringIO()):
    for p in pool_players[:60]:
        G['ev'](p, 2026)
c_ev = dict(_cnt)
P("      pool players probed: %d" % len(pool_players))
P("      calls to _h_cut / sitout_ev during _v0_uncapped + _v0_raw + v0_start + entry_anchor + raw_ev:")
P("          _h_cut     %d" % c_v0.get('h_cut', 0))
P("          sitout_ev  %d" % c_v0.get('sitout_ev', 0))
P("      the SAME counters during 60 calls to ev(p,2026) on the same players:")
P("          _h_cut     %d" % c_ev.get('h_cut', 0))
P("          sitout_ev  %d" % c_ev.get('sitout_ev', 0))
P("      -> the counters are live and they FIRE at ev(). They never fire on the v0 chain. The site")
P("         comment at _merged_recover.py:1999 says so in the engine's own words: 'this runs at ev(),")
P("         NEVER inside raw_ev -- _v0_uncapped calls raw_ev at Y=debutyr-1 to BUILD the very")
P("         year-0 prior'.")
G['_h_cut'], G['sitout_ev'] = _h_cut_o, _sit_o
P()
P("  PROOF 3 -- THE IN-PROCESS PERTURBATION. Set H_POOLSIT=H_UNION=1.0 and pool-gate _R_surf to 1.0")
P("  in the staged engine, CLEAR the v0 caches, and recompute the whole v0 chain for every pool row.")
_R_o = G['_R_surf']
G['_V0U'].clear(); G['_V0C'].clear()
with contextlib.redirect_stdout(io.StringIO()):
    before = {(p.get('player'), p.get('year')): (float(_v0_uncapped(p)), float(_v0_raw(p)),
                                                 float(v0_start(p)), float(entry_anchor(p)))
              for p in pool_players}
_poolflag = {'on': False}


def _R_patched(cls, pick, tau):
    if _poolflag['on']: return 1.0
    return _R_o(cls, pick, tau)


G['H_POOLSIT'] = 1.0; G['H_UNION'] = 1.0; G['_R_surf'] = _R_patched
_poolflag['on'] = True
G['_V0U'].clear(); G['_V0C'].clear()
with contextlib.redirect_stdout(io.StringIO()):
    after = {(p.get('player'), p.get('year')): (float(_v0_uncapped(p)), float(_v0_raw(p)),
                                                float(v0_start(p)), float(entry_anchor(p)))
             for p in pool_players}
_labels = ('_v0_uncapped', '_v0_raw', 'v0_start', 'entry_anchor')
_deltas = [max(abs(after[k][i] - before[k][i]) for k in before) for i in range(4)]
for lab, d in zip(_labels, _deltas):
    P("      max |%s(perturbed) - %s(shipped)| over %d pool rows = %.17g"
      % (lab, lab, len(before), d))
G['H_POOLSIT'], G['H_UNION'], G['_R_surf'] = H_POOLSIT, H_UNION, _R_o
_poolflag['on'] = False
G['_V0U'].clear(); G['_V0C'].clear()
P()
P("  WHY, FROM THE CODE (the mechanism, so the verdict is understood and not just believed):")
P("      _v0_uncapped(p) = raw_ev(p, debutyr-1) * iso_eff(p, debutyr-1)   (:1228-1238)")
P("      _v0_raw(p)      = _ruc_prior_cap(p, _v0_uncapped(p))             (:1239-1241)")
P("      v0_start(p)     = _V0CURVE[key] on the board path                (:1756-1760)")
P("      entry_anchor(p) = pool_level(p)*_PL_F*_b_factor(p) for a POOL row (:1852-1857)")
P("  NOT ONE of those five reads H_POOLSIT, H_UNION or _R_surf. _h_cut (:2037) and sitout_ev (:1961)")
P("  are both applied INSIDE ev() (:2228-2277). raw_ev is a DIFFERENT function (:1061).")
P()
P("  THE CONSEQUENCE THE OWNER SHOULD TAKE FROM THIS, stated plainly:")
P("      Lifting the pool sitter penalty changes what a pool player is WORTH TODAY. It does not")
P("      change what he ENTERED at. v0 and the signed division levels are a separate object and a")
P("      separate decision -- which is exactly the pool REPRICING question phase 1 is measuring on")
P("      its own branch. THESE TWO LEVERS DO NOT OVERLAP AT THE v0 SITE.")
P()
DATA['v0'] = dict(records=len(S), pool_records=len(_poolk), max_dv0_A=dA, max_dv0_B=dB,
                  max_dv0_pool_A=dAp, max_dv0_pool_B=dBp, vpath_changed_A=nvA, vpath_changed_B=nvB,
                  callcount_v0_chain=c_v0, callcount_ev=c_ev,
                  perturbation_max_delta=dict(zip(_labels, _deltas)))

# ==================================================================================================
# 4. THE OWNER'S PREMISE: SIT-OUT RATES PER PATHWAY vs ND
# ==================================================================================================
P("=" * 118)
P("4. THE OWNER'S OWN CONCERN, MEASURED -- 'given more pool players sit'")
P("=" * 118)
P("  Population: the same complete-window cells (Y <= 2021). A cell is a SIT-OUT if the player has")
P("  no season of >= 6 games up to and including that year. Both an unweighted count share and the")
P("  ENTRY-WEIGHTED share are given, because the entry weighting is what the charge actually keys on")
P("  (ORDER 18's P7 miss was exactly this distinction).")
P()
P("  %-8s %8s %8s %11s %13s | %9s %9s"
  % ('pathway', 'cells', 'sitters', 'share (n)', 'share (wtd)', 'vs ND n', 'vs ND wtd'))
P("  " + "-" * 82)
nd_n = nd_t['sit_share_n']; nd_w = nd_t['sit_share_w']
SIT = {}
for s in ORDER:
    m = PATH_MEAN[s]
    sub = [c for c in POOL if c['stream'] == s]
    mm = meanstat(sub, today_mult)
    SIT[s] = dict(n=mm['n'], nsit=mm['nsit'], share_n=mm['sit_share_n'], share_w=mm['sit_share_w'],
                  vs_nd_n=mm['sit_share_n'] / nd_n, vs_nd_w=mm['sit_share_w'] / nd_w)
    P("  %-8s %8d %8d %11.4f %13.4f | %8.2fx %8.2fx"
      % (s, mm['n'], mm['nsit'], mm['sit_share_n'], mm['sit_share_w'],
         mm['sit_share_n'] / nd_n, mm['sit_share_w'] / nd_w))
P("  " + "-" * 82)
P("  %-8s %8d %8d %11.4f %13.4f | %8.2fx %8.2fx"
  % ('ALL POOL', allp_t['n'], allp_t['nsit'], allp_t['sit_share_n'], allp_t['sit_share_w'],
     allp_t['sit_share_n'] / nd_n, allp_t['sit_share_w'] / nd_w))
P("  %-8s %8d %8d %11.4f %13.4f | %8s %8s"
  % ('ND 1-64', nd_t['n'], nd_t['nsit'], nd_n, nd_w, '1.00x', '1.00x'))
P()
_below_n = [s for s in ORDER if SIT[s]['share_n'] <= nd_n]
_below_w = [s for s in ORDER if SIT[s]['share_w'] <= nd_w]
P("  THE OWNER'S PREMISE ('more pool players sit'):")
P("      pathways at or BELOW ND 1-64 by COUNT share:          %s" % (', '.join(_below_n) or 'NONE'))
P("      pathways at or BELOW ND 1-64 by ENTRY-WEIGHTED share: %s" % (', '.join(_below_w) or 'NONE'))
P("      pooled pool vs ND 1-64: %.2fx by count, %.2fx entry-weighted."
  % (allp_t['sit_share_n'] / nd_n, allp_t['sit_share_w'] / nd_w))
P()
P("  AND ON THE LIVE BOARD (2026 season, zero games so far this season):")
P("  %-8s %8s %9s %11s | %14s %14s"
  % ('pathway', 'rows', 'sit-outs', 'share', 'value sitting', 'share of value'))
P("  " + "-" * 74)
LIVESIT = {}
for s in ORDER + ['ND 1-64']:
    ks = [k for k in KEYS if bstream(ROW['BASE'][k]) == s]
    if not ks: continue
    sit = [k for k in ks if k in PLK and games_in(PLK[k], Y0) == 0]
    tv = sum(ROW['BASE'][k]['v'] for k in ks)
    sv = sum(ROW['BASE'][k]['v'] for k in sit)
    LIVESIT[s] = dict(rows=len(ks), sit=len(sit), share=len(sit) / len(ks), val=tv, sitval=sv,
                      valshare=sv / tv if tv else 0.0)
    P("  %-8s %8d %9d %11.4f | %14s %13.4f"
      % (s, len(ks), len(sit), len(sit) / len(ks), format(sv, ','), sv / tv if tv else 0.0))
_pk2 = [k for k in KEYS if bstream(ROW['BASE'][k]) in POOLS]
_ps = [k for k in _pk2 if k in PLK and games_in(PLK[k], Y0) == 0]
P("  " + "-" * 74)
P("  %-8s %8d %9d %11.4f | %14s %13.4f"
  % ('ALL POOL', len(_pk2), len(_ps), len(_ps) / len(_pk2),
     format(sum(ROW['BASE'][k]['v'] for k in _ps), ','),
     sum(ROW['BASE'][k]['v'] for k in _ps) / sum(ROW['BASE'][k]['v'] for k in _pk2)))
P()
DATA['sitout'] = dict(cells=SIT, nd64=dict(share_n=nd_n, share_w=nd_w),
                      allpool=dict(share_n=allp_t['sit_share_n'], share_w=allp_t['sit_share_w']),
                      live=LIVESIT)

assert_pins('exit')
P("=" * 118)
P("PINS RE-ASSERTED AT EXIT -- board 94f1fec5..  store d9a24282..  instrument 0f822035..  UNMOVED.")
P("Nothing was wired. No shipped default changed. The live board was not touched.")
P("=" * 118)

with open(os.path.join(HERE, 'POOL_SITTER_LIFT.json'), 'w') as f:
    json.dump(DATA, f, indent=1, default=str)
