#!/usr/bin/env python3
"""DAY-0 REFERENCE REGENERATION on the PARITY BOARD `a05fe951` — fcrb_day0.py carried, re-keyed.

AUTHORITY. Register v763 bake item ("sitter print reference regeneration if day-0 moved — disclose as
Orders D/K did"), pulled forward by the register v769 supervisor ruling, STOPPED by the v771 owner
parity ruling, re-measured at SIX rows by v773 (falsifier D7-F8 FIRED), and ordered on `a05fe951` by
the v774 owner completion word. The disclosure that must be pushed BEFORE this file is run is
REBASE_DAY0_AMENDED.md, in this directory. It SUPERSEDES REBASE_DAY0.md at d5c37da on the record.

WHAT THIS IS. `fcrb_day0.py` (itself ORDER K's `ok_day0.py` carried), carried again with FOUR declared
changes and no others: (1) the board tag points at THIS seat's CP_CAND staging, (2) the dial line adds
RL_O43=1 — the parity guard, (3) the output name DAY0_CP.json, (4) THE ASSERTION BLOCK re-keyed to the
SIX rows, plus TWO NEW assertions A8 (every mover moves UP) and A9 (the two restored rows hold).

WHY A REGENERATION IS LAWFUL HERE, STATED BEFORE THE CODE. A day-0 price for a man who has never
played IS his entry value multiplied by the sitting fade, `round(day0_v0(p) * D(c_u))`. RL_O42 re-keys
the availability layer onto the owner's annotation sheet, and the availability fraction feeds the
UNPLAYED CLOCK c_u through `_fEy`. RL_O43 then takes a per-row max against the healthy counterpart;
at g=0 the one law collapses to v = v0 * D(c_u) exactly, so a max on the VALUE is identically a max on
the FADE. So the printed day-0 of an annotated wired entrant moves BY CONSTRUCTION. What does NOT move
is `derived_v0`, the raw entry object the walk-forward matrix writes as its year-0 column. This is the
same shape of regeneration ORDER D's pick-curve fade and ORDER K's tall/small factor each required.

THE ASSERTIONS, ALL HARD, ALL PRINTED. Against `order_k_2026-08-18/DAY0_K.json`:
  A1  every one of the 89 rows is present in both files, same key set.
  A2  `derived_v0` is BIT-IDENTICAL on 89 of 89 — the matrix year-0 column does not move.
  A3  EXACTLY SIX rows move on `printed`, and they are exactly harley-barker, blake-thredgold,
      max-king-syd, liam-hetherton, ollie-murphy, noah-chamberlain. A SEVENTH mover, or a named row
      that fails to move, HALTS.
  A4  each mover's old AND new printed integers equal the values the D7 parity harness published
      (481->504 · 372->381 · 129->138 · 66->70 · 196->200 · 37->40).
  A5  every moved row is annotated injured=Y on the pinned owner sheet. An unannotated mover HALTS.
  A6  the 83 non-movers are byte-identical on EVERY field, not just `printed`.
  A7  the identity on the WRITTEN board holds 89 of 89 at tolerance 0 (ORDER K's own check).
  A8  NEW — every moved row moves UP, strictly. RL_O43 is a max; a fall HALTS.
  A9  NEW — sam-allen and kobe-mcdonald are BYTE-IDENTICAL to the frozen reference (450 / 40); the
      parity guard restores them exactly, which is why the count is six and not eight.

READ-ONLY on the engine and on the store. No board is rebuilt here. NO ENGINE EDIT.
"""
import os, sys, json, io, csv, re, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = os.environ.get('RL_SCRATCH',
                    '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/fc')
TAG = os.environ.get('FCRB_TAG', 'CP_CAND')
BOARDP = os.path.join(SP, 'bb_%s' % TAG, 'rl_after', 'rl_app_data.json')
OUTNAME = os.environ.get('FCRB_OUT', 'DAY0_CP.json')
REF = os.path.join(ROOT, 'docs/evidence/order_k_2026-08-18/DAY0_K.json')

OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

# ---- THE CANDIDATE'S OWN DIAL LINE, character for character off build_D7.sh (KLINE + $S + O42 + O43)
KLINE = dict(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1='0.40', RL_O36_TALL='1',
             RL_O36_FLOORFIX='1', RL_O36_KAPPA='0.20', RL_O36_GAMMA='8.0', RL_O36_ETA='0.50',
             RL_O36_GAMMA_D='14.0', RL_O36_LAMBDA='1.08')
SLINE = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
             RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
             RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
             RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7')
O42 = {} if os.environ.get('FCRB_NO_O42') else dict(RL_O42='1')
# THE PARITY GUARD. RL_O43=1 is the ONE dial ORDER D7 added; without it this file would read the
# SUPERSEDED board daa16812 while the reference it writes claims to be a05fe951.
O43 = {} if os.environ.get('FCRB_NO_O43') else dict(RL_O43='1')

# CLEAR-LIST: every dial build_D7.sh clears with `env -u`, cleared here too, so an unset dial cannot
# leak in from the calling shell and silently price a line nobody ruled.
for _k in ('RL_O35', 'RL_O38B2', 'RL_O39_TMAXPCT', 'RL_O40_LAMBDA', 'RL_O41_CREDITFORM', 'RL_AVAIL',
           'RL_O42', 'RL_O43'):
    os.environ.pop(_k, None)

ENV = dict(PYTHONHASHSEED='0', RL_REPO=ROOT,
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
           RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
           RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
           RL_PRIOR_TREES='400', PAR_RAMPS='22',
           RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
ENV.update(KLINE); ENV.update(SLINE); ENV.update(O42); ENV.update(O43)
os.environ.update(ENV)

P('=' * 118)
P('DAY-0 PRINT REFERENCE — REGENERATED ON THE PARITY BOARD a05fe951  (tag %s)' % TAG)
P('=' * 118)
P('  authority : v763 bake item -> v769 pull-forward -> v771 parity ruling (the STOP) ->')
P('              v773 six-row finding (D7-F8 FIRED) -> v774 owner completion word on a05fe951')
P('  disclosure: docs/evidence/final_candidate_2026-08-19/REBASE_DAY0_AMENDED.md — pushed BEFORE this run')
P('  supersedes: REBASE_DAY0.md at d5c37da (three rows, superseded board daa16812) — NOT deleted')
P('  precedent : ORDER D (pick-curve fade) and ORDER K (tall/small factor) each regenerated this file')
P('  generator : ok_day0.py carried; board path, dial line, output name, and the ASSERTION BLOCK')
P('  engine    : %s' % hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'),
                                        'rb').read()).hexdigest()[:32])
P('  v0surf    : %s   (RL_V0SURF_PKL bound EXPLICITLY — register v767 footgun)'
  % hashlib.md5(open(os.path.join(ROOT, 'data/v0surf.pkl'), 'rb').read()).hexdigest()[:32])
P('  sheet     : %s' % hashlib.md5(open(os.path.join(
    ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv'), 'rb').read()).hexdigest()[:32])
P('  dial line : %s' % ' '.join('%s=%s' % (k, ENV[k])
                             for k in sorted(list(KLINE) + list(SLINE) + list(O42) + list(O43))))
P('  U0 = 7 return games — OWNER-RULED, DATA-SUPPORTED')
P('  board     : %s' % BOARDP)
if not os.path.exists(BOARDP):
    raise SystemExit('HALT: the candidate board is absent at %s. Build it first (build_FC.sh).' % BOARDP)

sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
_cwd = os.getcwd(); os.chdir(ROOT + '/engine/rl_after')
NSE = {}
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
os.chdir(_cwd)
MA = NSE.get('MA', MA)
entry_derived = NSE['_entry29b_derived']; o31_D = NSE['o31_D']; o31_cu = NSE['o31_cu']

# ---- INSTRUMENT FIX 1, DISCLOSED: THE CARRIED GENERATOR PRE-DATES THE D7 SECOND WIRING SITE. -------
# ok_day0.py / fcrb_day0.py form the day-0 price as `d0 * o31_D(p,Y)` — the LIVE (injury) fade. Under
# RL_O43 the engine's OWN day-0 predicate `_entry30b_price` no longer does that: it multiplies by the
# fade ratio `_dh/_dl` out of `_D7_DFADE`, so the price is formed on the HEALTHY fade wherever the
# healthy counterpart wins (engine `_merged_recover.py`, the "SECOND WIRING SITE" block). A generator
# that keeps the old formula measures a DIFFERENT LAW from the one the board was written with, and its
# A7/A6 columns then disagree with a board that is in fact self-consistent — which is exactly what the
# first run of this file showed (A7 read 82 of 89, and the 7 "mismatches" were the rows where the
# healthy fade won). THE FIX IS TO READ THE ENGINE'S OWN RATIO, character for character as the engine
# applies it — NOT to relax the assertion, and NOT to touch the engine.
_D7_DFADE = NSE.get('_D7_DFADE') or {}
def _fade_guarded(p, Y):
    """The sitter fade the BOARD actually formed the price with, under RL_O43."""
    _d = float(o31_D(p, Y))
    if int(Y) != 2026:
        return _d
    _pr = _D7_DFADE.get(p.get('key'))
    if not _pr:
        return _d
    _dl, _dh = _pr
    return _d * (_dh / _dl) if (_dl > 0.0 and _dh > _dl) else _d
# THE ENGINE'S OWN RESOLUTION of the owner sheet's names to store keys, used for A5 instead of a naive
# re-normalisation of the sheet (INSTRUMENT FIX 2, below).
_AVAIL_KEYS = set(NSE.get('_AVAIL_STATE') or {})
BOARD_MD5 = hashlib.md5(open(BOARDP, 'rb').read()).hexdigest()
ROWS = {r['key']: r for r in json.load(open(BOARDP))['active']}
Y = MA.BASE_REF
P('  board md5 : %s   BASE_REF %d' % (BOARD_MD5, Y))
P()

# ---- ORDER K's generator body, verbatim in shape --------------------------------------------------
out, mism = [], []
nND = nPOOL = 0
for p in MA.data:
    with contextlib.redirect_stdout(io.StringIO()):
        d0 = entry_derived(p, Y)
    if d0 is None:
        continue
    k = p.get('key') or MA.slug(p['player'])
    with contextlib.redirect_stdout(io.StringIO()):
        D = _fade_guarded(p, Y); cu = float(o31_cu(p, Y))
    price = float(d0) * D
    printed = ROWS[k]['v'] if k in ROWS else None
    if printed is None or int(round(price)) != int(printed):
        mism.append((k, printed, price))
    if p.get('_pool'): nPOOL += 1
    else: nND += 1
    out.append(dict(key=k, ty=p.get('type'), pos=MA.gfut(p), pick=p.get('pick'),
                    cell=('%s|%s' % (p.get('type'), MA.gfut(p))) if p.get('_pool') else None,
                    printed=int(printed) if printed is not None else None,
                    derived_v0=float(d0), fade_D=D, day0_price=price))
BY = {r['key']: r for r in out}

# ================= THE ASSERTION BLOCK — NEW IN THIS FILE, HARD, AND PRINTED =======================
# THE SIX ROWS, off the D7 parity harness's OWN raw output
# (docs/evidence/parity_2026-08-19/PARITY_TABLE_out.txt at 9b93fba, the D7-F8 block), as
#   key : (printed on the frozen reference, printed on the priced board a05fe951)
GUARD = {'harley-barker':    (481, 504),
         'blake-thredgold':  (372, 381),
         'max-king-syd':     (129, 138),
         'liam-hetherton':   (66,  70),
         'ollie-murphy':     (196, 200),
         'noah-chamberlain': (37,  40)}
NAMED = tuple(sorted(GUARD))
# THE TWO ROWS THE PARITY GUARD RESTORES EXACTLY — they moved on the SUPERSEDED board daa16812
# (450->428, 40->37) and must NOT move here. This is why the count is six and not eight (A9).
RESTORED = {'sam-allen': 450, 'kobe-mcdonald': 40}
FIELDS = ('key', 'ty', 'pos', 'pick', 'cell', 'printed', 'derived_v0', 'fade_D', 'day0_price')

R = json.load(open(REF))
RBY = {r['key']: r for r in R['rows']}
P('ASSERTIONS AGAINST THE OLD REFERENCE  %s  (board %s, %s)'
  % (os.path.relpath(REF, ROOT), R['board_md5'][:8], R['identity_all']))
P('-' * 118)
HALT = []

# A7 (ORDER K's own identity check on the WRITTEN board) --------------------------------------------
P('  A7  printed-day-0 identity on the WRITTEN board %s : %d of %d at tolerance 0  (ND %d, pool %d)'
  % (BOARD_MD5[:8], len(out) - len(mism), len(out), nND, nPOOL))
if mism:
    P('      MISMATCHES: %s' % mism[:10]); HALT.append('A7 the identity does not hold on the written board')

# A1 same key set ------------------------------------------------------------------------------------
_only_new = sorted(set(BY) - set(RBY)); _only_old = sorted(set(RBY) - set(BY))
P('  A1  key set        : new %d rows, old %d rows, symmetric difference %d'
  % (len(BY), len(RBY), len(_only_new) + len(_only_old)))
if _only_new or _only_old:
    P('      only-new %s   only-old %s' % (_only_new[:8], _only_old[:8]))
    HALT.append('A1 the wired-entrant population changed')

_common = sorted(set(BY) & set(RBY))

# A2 derived_v0 bit-identical ------------------------------------------------------------------------
_dv = [k for k in _common if BY[k]['derived_v0'] != RBY[k]['derived_v0']]
P('  A2  derived_v0     : BIT-IDENTICAL on %d of %d  — the matrix year-0 column does not move'
  % (len(_common) - len(_dv), len(_common)))
if _dv:
    for k in _dv[:10]:
        P('      %-20s %.13f -> %.13f' % (k, RBY[k]['derived_v0'], BY[k]['derived_v0']))
    HALT.append('A2 %d rows moved on derived_v0 — this is NOT a fade-only regeneration' % len(_dv))

# A3 exactly the three named rows move on printed -----------------------------------------------------
_mv = [k for k in _common if BY[k]['printed'] != RBY[k]['printed']]
P('  A3  printed movers : %d  %s' % (len(_mv), sorted(_mv)))
_extra = sorted(set(_mv) - set(NAMED)); _missing = sorted(set(NAMED) - set(_mv))
if _extra:
    HALT.append('A3 a row NOT named by the D7 harness moved (a SEVENTH mover): %s' % _extra)
    P('      *** UNNAMED MOVER(S): %s ***' % _extra)
if _missing:
    HALT.append('A3 a NAMED row failed to move: %s' % _missing)
    P('      *** NAMED ROW DID NOT MOVE: %s ***' % _missing)
if not _extra and not _missing:
    P('      exactly the SIX rows the D7 parity harness named, no more and no fewer.')

# A4 each mover matches the D7 parity harness's published values ---------------------------------------
P('  A4  each mover against the D7 parity harness\'s OWN raw output (PARITY_TABLE_out.txt):')
P('      %-18s %10s %10s %10s %10s   %22s   %s'
  % ('key', 'old print', 'new print', 'D7 old', 'D7 new', 'derived_v0 (unmoved)', 'verdict'))
for k in NAMED:
    if k not in BY or k not in RBY:
        P('      %-18s ROW ABSENT' % k); HALT.append('A4 %s absent' % k); continue
    _op, _np = GUARD[k]
    n, o = BY[k], RBY[k]
    ok = (o['printed'] == _op and n['printed'] == _np and n['derived_v0'] == o['derived_v0'])
    P('      %-18s %10d %10d %10d %10d   %22.13f   %s'
      % (k, o['printed'], n['printed'], _op, _np, n['derived_v0'],
         'MATCHES THE D7 TABLE' if ok else '*** DOES NOT MATCH ***'))
    if not ok:
        HALT.append('A4 %s does not reproduce the D7 parity harness\'s published values' % k)

# A5 every mover is annotated injured=Y on the pinned sheet ---------------------------------------------
# INSTRUMENT FIX 2, DISCLOSED: THE MEMBERSHIP JOIN IS READ OFF THE ENGINE, NOT OFF A NAIVE NORMALISER.
# fcrb_day0.py tested membership by re-normalising the sheet's `player` column and comparing to the
# engine key. That mis-maps exactly the rows PACKET_D7.md §4.2 already caught and disclosed:
#     sheet "Maxwell King" (Sydney) -> naive `maxwell-king` -> ENGINE KEY `max-king-syd`
#     sheet "Max King"     (St K)   -> naive `max-king`     -> ENGINE KEY `max-king-stk`
#     sheet "Elliott Himmelberg"    -> naive `elliott-...`  -> ENGINE KEY `elliot-himmelberg` (one t)
# On the first run of this file that artifact made A5 fire on `max-king-syd`, a row that IS annotated
# injured=Y (sheet line 126). THE ROW WAS NEVER UNANNOTATED; THE JOIN WAS WRONG. The fix reads the
# annotated set out of the engine's OWN `_AVAIL_STATE`, which the ORDER 42 builder constructs by
# matching the normalised sheet name against BOTH the record's `key` AND its `player` field, and which
# it ASSERTS is a 37 -> 37 distinct-single-record correspondence (it halts on a miss, a duplicate or an
# ambiguity). This is STRICTLY STRONGER than the naive test, not weaker: it is the same set the engine
# itself refuses to build if it cannot resolve exactly.
def _n2(n): return re.sub(r'[^a-z0-9]+', '-', str(n).strip().lower().replace('’', "'")).strip('-')
_sheet = list(csv.DictReader(open(os.path.join(ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv'))))
_SY_naive = {_n2(r['player']): r for r in _sheet if (r.get('injured') or '').strip().upper() == 'Y'}
_SY = _AVAIL_KEYS                       # the ENGINE's resolution of those same annotated rows
if len(_SY) != len(_SY_naive):
    P('      NOTE: the engine resolves %d annotated keys; the naive sheet normaliser yields %d names. '
      'The difference is the disclosed join artifact (PACKET_D7 §4.2); the ENGINE is authoritative.'
      % (len(_SY), len(_SY_naive)))
_wired_annot = sorted(set(_common) & set(_SY))
P('  A5  sheet          : %d rows, %d annotated injured=Y (engine-resolved to %d store keys); '
  '%d of the %d wired entrants are annotated'
  % (len(_sheet), len(_SY_naive), len(_SY), len(_wired_annot), len(_common)))
P('      annotated wired entrants: %s' % _wired_annot)
_unannot = [k for k in _mv if k not in _SY]
if _unannot:
    P('      *** MOVED BUT NOT SHEET-ANNOTATED: %s ***' % _unannot)
    HALT.append('A5 a moved row is not annotated on the owner sheet: %s' % _unannot)
else:
    P('      every moved row is annotated injured=Y. %d annotated wired entrants did NOT move: %s'
      % (len(_wired_annot) - len(_mv), sorted(set(_wired_annot) - set(_mv))))

# A6 the non-movers are byte-identical on EVERY field --------------------------------------------------
_bad6 = []
for k in _common:
    if k in _mv: continue
    for f in FIELDS:
        if BY[k].get(f) != RBY[k].get(f):
            _bad6.append((k, f, RBY[k].get(f), BY[k].get(f)))
P('  A6  non-movers     : %d of %d rows BYTE-IDENTICAL on every field %s'
  % (len(_common) - len(_mv) - len({b[0] for b in _bad6}), len(_common) - len(_mv), list(FIELDS)))
if _bad6:
    for b in _bad6[:12]: P('      %-20s %-12s %r -> %r' % b)
    HALT.append('A6 %d non-mover field(s) moved' % len(_bad6))

# A8 EVERY MOVER MOVES UP -- NEW ------------------------------------------------------------------------
# RL_O43 is a per-row max. It CANNOT lower a row. A downward mover would mean the dial is not what the
# encoding claims, and that is a build-failing finding, not a note.
_down = [(k, RBY[k]['printed'], BY[k]['printed']) for k in _mv if BY[k]['printed'] <= RBY[k]['printed']]
P('  A8  direction      : %d of %d movers move strictly UP  (RL_O43 is a max — it can only RAISE)'
  % (len(_mv) - len(_down), len(_mv)))
for k in sorted(_mv):
    P('      %-18s %6d -> %-6d  %+d  %s'
      % (k, RBY[k]['printed'], BY[k]['printed'], BY[k]['printed'] - RBY[k]['printed'],
         'UP' if BY[k]['printed'] > RBY[k]['printed'] else '*** NOT UP ***'))
if _down:
    P('      *** DOWNWARD OR FLAT MOVER(S): %s ***' % _down)
    HALT.append('A8 a moved row did not move UP: %s — RL_O43 is a max and cannot lower a row' % _down)

# A9 THE TWO RESTORED ROWS HOLD -- NEW -------------------------------------------------------------------
# sam-allen and kobe-mcdonald moved DOWN on the superseded board daa16812 (450->428, 40->37). The parity
# guard restores them EXACTLY. If either moves here the count is not six and the amendment is wrong.
P('  A9  parity-restored rows (moved on the SUPERSEDED board daa16812, must NOT move here):')
for k, _want in sorted(RESTORED.items()):
    if k not in BY or k not in RBY:
        P('      %-18s ROW ABSENT' % k); HALT.append('A9 %s absent' % k); continue
    o, n = RBY[k]['printed'], BY[k]['printed']
    ok = (o == n == _want)
    P('      %-18s frozen %6d | priced %6d | expected %6d   %s'
      % (k, o, n, _want, 'RESTORES EXACTLY' if ok else '*** DOES NOT RESTORE ***'))
    if not ok:
        HALT.append('A9 %s does not restore to the frozen print (%d -> %d, expected %d)'
                    % (k, o, n, _want))

P('-' * 118)
if HALT:
    P('*** HALT — %d ASSERTION(S) FAILED. NO REFERENCE IS WRITTEN. ***' % len(HALT))
    for h in HALT: P('      %s' % h)
    open(os.path.join(HERE, 'REBASE_DAY0_AMENDED_out.txt'), 'w').write('\n'.join(OUT) + '\n')
    raise SystemExit(1)
P('ALL NINE ASSERTIONS PASS. %d of %d rows byte-identical to the ORDER K reference; exactly %d move '
  '(%s), every one sheet-annotated injured=Y, every one UP, each to the value the D7 parity harness '
  'itself published; sam-allen and kobe-mcdonald restore exactly.'
  % (len(_common) - len(_mv), len(_common), len(_mv), ', '.join(sorted(_mv))))
P()

DOC = dict(label='PARITY BOARD — the day-0 reference regenerated on board %s (%s)'
                 % (TAG, BOARD_MD5[:8]),
           board='PARITY BOARD %s' % TAG, board_md5=BOARD_MD5,
           law='printed = round(day0_v0(p) * D(c_u)) — the ONE LAW at g=0, where rho(0)=0 and '
               'pi(0,c,s) == D(c) exactly',
           regeneration_reason='RL_O42=1 makes the owner annotation sheet the single source of injury '
                               'truth; the availability fraction feeds the UNPLAYED CLOCK c_u through '
                               '_fEy. RL_O43=1, the parity guard, then takes a per-row max against the '
                               'healthy counterpart; at g=0 a max on the VALUE is identically a max on '
                               'the FADE. So the SITTER FADE D(c_u) of a sheet-annotated wired entrant '
                               'moves by construction, and can only move UP. derived_v0 is '
                               'bit-identical on 89 of 89 — the matrix year-0 column does not move. '
                               'Same shape as ORDER D and ORDER K.',
           authority='register v763 bake item -> v769 pull-forward -> v771 parity ruling (the STOP) -> '
                     'v773 six-row finding (D7-F8 FIRED) -> v774 owner completion word on a05fe951; '
                     'disclosed at docs/evidence/final_candidate_2026-08-19/REBASE_DAY0_AMENDED.md, '
                     'which SUPERSEDES the stale three-row REBASE_DAY0.md at d5c37da on the record',
           supersedes='docs/evidence/order_k_2026-08-18/DAY0_K.json (board %s)' % R['board_md5'],
           supersedes_disclosure='docs/evidence/final_candidate_2026-08-19/REBASE_DAY0.md at d5c37da '
                                 '(three rows, superseded board daa16812, NEVER ACTED ON) — kept as '
                                 'filed history, not deleted',
           direction='every mover moves UP — RL_O43 is a per-row max and cannot lower a row (A8)',
           parity_restored={k: dict(frozen=RBY[k]['printed'], priced=BY[k]['printed'])
                            for k in sorted(RESTORED) if k in BY and k in RBY},
           movers=[dict(key=k, printed_old=RBY[k]['printed'], printed_new=BY[k]['printed'],
                        fade_D_old=RBY[k]['fade_D'], fade_D_new=BY[k]['fade_D'],
                        derived_v0=BY[k]['derived_v0'], sheet_injured='Y') for k in sorted(_mv)],
           n_byte_identical=len(_common) - len(_mv),
           base_ref=Y, n_fresh_nd=nND, n_pool=nPOOL, n_wired=len(out),
           identity_all='%d of %d at tolerance 0' % (len(out) - len(mism), len(out)),
           mismatches=mism, rows=out)
json.dump(DOC, open(os.path.join(HERE, OUTNAME), 'w'), indent=1, sort_keys=True)
P('PRINTED DAY-0 IDENTITY: %d of %d at tolerance 0 (ND %d, pool %d) on board %s'
  % (len(out) - len(mism), len(out), nND, nPOOL, BOARD_MD5[:12]))
P('%s written  (md5 %s)' % (OUTNAME, hashlib.md5(open(os.path.join(HERE, OUTNAME), 'rb').read()).hexdigest()[:12]))
open(os.path.join(HERE, 'REBASE_DAY0_out.txt'), 'w').write('\n'.join(OUT) + '\n')
