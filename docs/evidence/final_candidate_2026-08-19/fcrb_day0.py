#!/usr/bin/env python3
"""DAY-0 REFERENCE REGENERATION on the final candidate `daa16812` — ORDER K's generator, re-pointed.

AUTHORITY. Register v763 bake item ("sitter print reference regeneration if day-0 moved — disclose as
Orders D/K did"), pulled forward by the register v769 supervisor ruling. The disclosure that must be
pushed BEFORE this file is run is REBASE_DAY0.md, in this directory.

WHAT THIS IS. `docs/evidence/order_k_2026-08-18/ok_day0.py`, carried with FOUR declared changes and no
others: (1) the board path points at THIS seat's FC_CAND staging, (2) the dial line is the final
candidate's, (3) the output name, (4) THE ASSERTION BLOCK — new, and the whole point of this file.

WHY A REGENERATION IS LAWFUL HERE, STATED BEFORE THE CODE. A day-0 price for a man who has never
played IS his entry value multiplied by the sitting fade, `round(day0_v0(p) * D(c_u))`. RL_O42 re-keys
the availability layer onto the owner's annotation sheet, and the availability fraction feeds the
UNPLAYED CLOCK c_u through `_fEy`. So the printed day-0 of a wired entrant who is annotated on the
sheet moves BY CONSTRUCTION the moment the sheet is the injury truth. What does NOT move is
`derived_v0`, the raw entry object the walk-forward matrix writes as its year-0 column. This is the
same shape of regeneration ORDER D's pick-curve fade and ORDER K's tall/small factor each required.

THE ASSERTIONS, ALL HARD, ALL PRINTED. Against `order_k_2026-08-18/DAY0_K.json`:
  A1  every one of the 89 rows is present in both files, same key set.
  A2  `derived_v0` is BIT-IDENTICAL on 89 of 89 — the matrix year-0 column does not move.
  A3  EXACTLY THREE rows move on `printed`, and they are exactly sam-allen, ollie-murphy,
      kobe-mcdonald. A fourth mover, or a named row that fails to move, HALTS.
  A4  each mover's new printed integer equals the value the emit guard itself diagnosed
      (428 / 200 / 37), and each mover's derived_v0 equals the guard's own `_mb`.
  A5  every moved row is annotated injured=Y on the pinned owner sheet. An unannotated mover HALTS.
  A6  the 86 non-movers are byte-identical on EVERY field, not just `printed`.
  A7  the identity on the WRITTEN board holds 89 of 89 at tolerance 0 (ORDER K's own check).

READ-ONLY on the engine and on the store. No board is rebuilt here.
"""
import os, sys, json, io, csv, re, contextlib, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SP = os.environ.get('RL_SCRATCH',
                    '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/fc')
TAG = os.environ.get('FCRB_TAG', 'FC_CAND')
BOARDP = os.path.join(SP, 'bb_%s' % TAG, 'rl_after', 'rl_app_data.json')
OUTNAME = os.environ.get('FCRB_OUT', 'DAY0_FC.json')
REF = os.path.join(ROOT, 'docs/evidence/order_k_2026-08-18/DAY0_K.json')

OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

# ---- THE CANDIDATE'S OWN DIAL LINE, character for character off build_FC.sh (KLINE + $S + RL_O42) --
KLINE = dict(RL_O31='1', RL_O32='1', RL_O36='1', RL_O36_LAM_S1='0.40', RL_O36_TALL='1',
             RL_O36_FLOORFIX='1', RL_O36_KAPPA='0.20', RL_O36_GAMMA='8.0', RL_O36_ETA='0.50',
             RL_O36_GAMMA_D='14.0', RL_O36_LAMBDA='1.08')
SLINE = dict(RL_O37='1', RL_O38A='1', RL_O38B1='1', RL_O39_BETASAT='0.105',
             RL_O40_CAPFORM='smooth', RL_O40_CAPPCT='15', RL_O40_RECW='0.47', RL_O40_PGMAT='1',
             RL_O41_SDOFF='2.98', RL_O41_CREDIT='1', RL_O41_RESET='1', RL_O41_INJ='1',
             RL_O41_R3='1', RL_O41_RAMP='1', RL_O41_BREAK='unwind', RL_O41_UNWIND='7')
O42 = {} if os.environ.get('FCRB_NO_O42') else dict(RL_O42='1')

# CLEAR-LIST: every dial build_FC.sh clears with `env -u`, cleared here too, so an unset dial cannot
# leak in from the calling shell and silently price a line nobody ruled.
for _k in ('RL_O35', 'RL_O38B2', 'RL_O39_TMAXPCT', 'RL_O40_LAMBDA', 'RL_O41_CREDITFORM', 'RL_AVAIL',
           'RL_O42'):
    os.environ.pop(_k, None)

ENV = dict(PYTHONHASHSEED='0', RL_REPO=ROOT,
           OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
           NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
           RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
           RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
           RL_PRIOR_TREES='400', PAR_RAMPS='22',
           RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
ENV.update(KLINE); ENV.update(SLINE); ENV.update(O42)
os.environ.update(ENV)

P('=' * 118)
P('DAY-0 PRINT REFERENCE — REGENERATED ON THE FINAL CANDIDATE  (tag %s)' % TAG)
P('=' * 118)
P('  authority : register v763 bake item, pulled forward by the v769 supervisor ruling')
P('  disclosure: docs/evidence/final_candidate_2026-08-19/REBASE_DAY0.md — pushed BEFORE this run')
P('  precedent : ORDER D (pick-curve fade) and ORDER K (tall/small factor) each regenerated this file')
P('  generator : ok_day0.py carried; board path, dial line, output name, and the ASSERTION BLOCK')
P('  engine    : %s' % hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/_merged_recover.py'),
                                        'rb').read()).hexdigest()[:32])
P('  v0surf    : %s   (RL_V0SURF_PKL bound EXPLICITLY — register v767 footgun)'
  % hashlib.md5(open(os.path.join(ROOT, 'data/v0surf.pkl'), 'rb').read()).hexdigest()[:32])
P('  sheet     : %s' % hashlib.md5(open(os.path.join(
    ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv'), 'rb').read()).hexdigest()[:32])
P('  dial line : %s' % ' '.join('%s=%s' % (k, ENV[k]) for k in sorted(list(KLINE) + list(SLINE) + list(O42))))
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
        D = float(o31_D(p, Y)); cu = float(o31_cu(p, Y))
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
NAMED = ('sam-allen', 'ollie-murphy', 'kobe-mcdonald')
# the values the ORDER 31-F guard itself diagnosed when it halted (EMIT_FCCAND_out.txt):
#   (key, reference printed, the printed integer THIS law forms, the raw entry object)
GUARD = {'sam-allen':     (450, 428, 791.8152857422534),
         'ollie-murphy':  (196, 200, 398.35828513161437),
         'kobe-mcdonald': (40,  37,  87.02989219418069)}
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
    HALT.append('A3 a row NOT named by the guard moved: %s' % _extra)
    P('      *** UNNAMED MOVER(S): %s ***' % _extra)
if _missing:
    HALT.append('A3 a NAMED row failed to move: %s' % _missing)
    P('      *** NAMED ROW DID NOT MOVE: %s ***' % _missing)
if not _extra and not _missing:
    P('      exactly the three rows the guard named, no more and no fewer.')

# A4 each mover matches the guard's own diagnosed values -----------------------------------------------
P('  A4  each mover against the guard\'s OWN halt output:')
P('      %-16s %10s %10s %10s   %22s %22s   %s'
  % ('key', 'old print', 'new print', 'guard', 'old derived_v0', 'new derived_v0', 'verdict'))
for k in NAMED:
    if k not in BY or k not in RBY:
        P('      %-16s ROW ABSENT' % k); HALT.append('A4 %s absent' % k); continue
    _op, _gp, _gv = GUARD[k]
    n, o = BY[k], RBY[k]
    ok = (o['printed'] == _op and n['printed'] == _gp
          and n['derived_v0'] == _gv and o['derived_v0'] == _gv)
    P('      %-16s %10d %10d %10d   %22.13f %22.13f   %s'
      % (k, o['printed'], n['printed'], _gp, o['derived_v0'], n['derived_v0'],
         'MATCHES THE GUARD' if ok else '*** DOES NOT MATCH ***'))
    if not ok:
        HALT.append('A4 %s does not reproduce the guard\'s diagnosed values' % k)

# A5 every mover is annotated injured=Y on the pinned sheet ---------------------------------------------
def _n2(n): return re.sub(r'[^a-z0-9]+', '-', str(n).strip().lower().replace('’', "'")).strip('-')
_sheet = list(csv.DictReader(open(os.path.join(ROOT, 'docs/owner_annotations/SITTER_2026_v1.csv'))))
_SY = {_n2(r['player']): r for r in _sheet if (r.get('injured') or '').strip().upper() == 'Y'}
_wired_annot = sorted(set(_common) & set(_SY))
P('  A5  sheet          : %d rows, %d annotated injured=Y; %d of the %d wired entrants are annotated'
  % (len(_sheet), len(_SY), len(_wired_annot), len(_common)))
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

P('-' * 118)
if HALT:
    P('*** HALT — %d ASSERTION(S) FAILED. NO REFERENCE IS WRITTEN. ***' % len(HALT))
    for h in HALT: P('      %s' % h)
    open(os.path.join(HERE, 'REBASE_DAY0_out.txt'), 'w').write('\n'.join(OUT) + '\n')
    raise SystemExit(1)
P('ALL SEVEN ASSERTIONS PASS. %d of %d rows byte-identical to the old reference; only %s move, '
  'every one of them sheet-annotated, each to the value the guard itself diagnosed.'
  % (len(_common) - len(_mv), len(_common), ', '.join(sorted(_mv))))
P()

DOC = dict(label='FINAL CANDIDATE — the day-0 reference regenerated on board %s (%s)'
                 % (TAG, BOARD_MD5[:8]),
           board='FINAL CANDIDATE %s' % TAG, board_md5=BOARD_MD5,
           law='printed = round(day0_v0(p) * D(c_u)) — the ONE LAW at g=0, where rho(0)=0 and '
               'pi(0,c,s) == D(c) exactly',
           regeneration_reason='RL_O42=1 makes the owner annotation sheet the single source of injury '
                               'truth; the availability fraction feeds the UNPLAYED CLOCK c_u through '
                               '_fEy, so the SITTER FADE D(c_u) of a sheet-annotated wired entrant '
                               'moves by construction. derived_v0 is bit-identical on 89 of 89 — the '
                               'matrix year-0 column does not move. Same shape as ORDER D and ORDER K.',
           authority='register v763 bake item, pulled forward by the register v769 supervisor ruling; '
                     'disclosed at docs/evidence/final_candidate_2026-08-19/REBASE_DAY0.md',
           supersedes='docs/evidence/order_k_2026-08-18/DAY0_K.json (board %s)' % R['board_md5'],
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
