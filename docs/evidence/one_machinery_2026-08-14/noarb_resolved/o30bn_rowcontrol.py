#!/usr/bin/env python3
"""ORDER 30B-N STEP 2 CONTROL -- does the ev()-LEVEL WIRING reproduce the DERIVED resolved board?

RESOLVED_ALLROWS.json is derived, not built: o30br_allrows.py composes committed artifacts and never
runs the engine. This harness asks whether the wired law, priced through ev() on a real build, lands on
the same 804 rows. It is the calibration control for everything that follows.

TWO COMPARISONS, AND THE FIRST IS THE REAL ONE.

  A. UNROUNDED, engine-loaded (THE CONTROL). The engine is loaded IN THE RESOLVED LANE and ev(p,2026) is
     called per row, so the comparison is float-vs-float in BOARD currency (ev/_PL_F). No print rounding
     enters it at all. This is the comparison the prereg's P3 bands were written for.

  B. PRINTED BOARD (a disclosure, NOT the control). The written board carries INTEGERS while the derived
     board carries one decimal, so every row can differ by up to 0.5 for that reason alone. PREREG_30BN
     P3a/P3b/P3c were tabled against the unrounded quantity; scoring them on the printed integers would
     charge the wiring for the board's own print precision. Both are reported; the scored one is A.

THE TOLERANCE IS PRE-STATED (PREREG_30BN.md P3) AND ITS SOURCE IS NAMED: the derived board's production
column is recovered by INVERTING THE WEIGHT BLEND ON THE ROUNDED PRINTED PREVIEW PRICE
(o30bp_movers.py:52, `prod = (v_printed - sigma*v0)/(1-sigma)`), so it carries a rounding residue of up
to 0.5/(1-sigma) board points. The wiring consumes the TRUE unrounded production leg. The two therefore
CANNOT agree to zero, and the prereg bands the disagreement per lane BEFORE this ran:

  sitter (89) + thin (99)  production does NOT enter the lane  -> EXACTLY ZERO, tolerance 0.05.
                                                                  A move here is a WIRING ERROR.
  bridge (44)              residue <= t*0.5/(1-sigma(g)), g 11-15 -> <= 1.2
  deep   (572)             residue <= 0.5/(1-sigma(g)), g >= 16   -> <= 1.0
  max |delta| over 804     <= 1.2 ; count(|delta| > 1.5) == 0 ; total within +-150 of 715228.6

env:   RL_O30B_RESOLVED=1  STAGE=<staged rl_after>  RL_REPO=<worktree>
usage: o30bn_rowcontrol.py <resolved_board.json> [out.json]
"""
import os, sys, io, json, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, '..', 'resolution')

BOARD = sys.argv[1]
OUTP = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'ROWCONTROL_30BN.json')

assert os.environ.get('RL_O30B_RESOLVED') == '1', 'this harness must run IN the resolved lane'
STAGE = os.environ['STAGE']
ROOT = os.environ['RL_REPO']
sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', STAGE]
_cwd = os.getcwd()
os.chdir(STAGE)
G = {}
_boot = io.StringIO()
with contextlib.redirect_stdout(_boot):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
os.chdir(_cwd)
BOOT = _boot.getvalue()
MA = G['MA']
ev = G['ev']
_PL_F = G['_PL_F']
pv_games = G['pv_games']
fade30b_of = G['fade30b_of']
fade30b_clock = G['fade30b_clock']
beta30bn = G['beta30bn']
b_lift30bn = G['b_lift30bn']
Y = 2026

# ---- THE EFFECTIVE PRODUCTION LEG, AT BETTER PRECISION THAN THE DERIVED BOARD'S ---------------------
# The derived board recovers production by inverting the weight blend on the PRINTED INTEGER preview
# price, so its production column carries the board's print rounding (+-0.5 board) ON TOP of the blend
# site's round() in engine currency (+-0.5/_PL_F). Reading the preview lane's UNROUNDED ev() removes the
# print rounding and leaves only the latter, which is a strictly better production leg.
#
# WHY AN INVERSION AT ALL, rather than capturing `e` at the blend site: ev() is an M3 interpolation of
# TWO evaluations (click and pin), so the blend is called more than once per row and no single `e` is
# the one that produced the price. Both readings are AFFINE in production with a games-only slope, so
# the interpolation commutes with the blend and an EFFECTIVE production leg is well defined --
# P_eff = (ev_preview - sigma*v0) / (1 - sigma) -- which is exactly the object the derived board is
# reaching for, recovered here at higher precision.
import math as _m

PREV = json.load(open(os.environ['PREVIEW_EV']))

AR = json.load(open(os.path.join(RES, 'RESOLVED_ALLROWS.json')))
B = json.load(open(BOARD))
BV = {r['key']: r for r in B['active']}
DER = {r['key']: r for r in AR['rows']}
BYK = {p['key']: p for p in MA.data if p.get('key')}

rows = []
for k, d in DER.items():
    if k not in BV or k not in BYK:
        continue
    p = BYK[k]
    unr = float(ev(p, Y)) / _PL_F              # BOARD currency -- the engine's own answer
    g = pv_games(p, Y)
    D = fade30b_of(p, Y)
    c = fade30b_clock(p, Y)
    v0 = float(G['day0_v0'](p) or 0.0)
    # THE SAME RESOLUTION ARITHMETIC, but fed the effective production leg recovered from the PREVIEW
    # lane's UNROUNDED ev() instead of the derived board's print-rounded one. Board currency throughout.
    Pb = None
    _pv = PREV.get(k)
    if _pv is not None and _pv['sigma'] < 1.0:
        Pb = (_pv['ev_board'] - _pv['sigma'] * v0) / (1.0 - _pv['sigma'])
    if d['lane'] == 'sitter':
        rec = v0 * D
    elif d['lane'] == 'thin':
        rec = v0 * D * b_lift30bn(g, c)
    elif Pb is None:
        rec = None
    elif d['lane'] == 'bridge':
        t10 = v0 * D * b_lift30bn(10.0, c)
        d16 = Pb + beta30bn(16.0) * v0
        t = (_m.log1p(g) - _m.log1p(10.0)) / (_m.log1p(16.0) - _m.log1p(10.0))
        rec = t10 + t * (d16 - t10)
    else:
        rec = Pb + beta30bn(g) * v0
    rows.append(dict(key=k, name=d['name'], pathway=d['pathway'], pool=d['pool'], lane=d['lane'],
                     derived=d['resolved'], unrounded=unr, printed=float(BV[k]['v']),
                     delta=unr - d['resolved'], delta_printed=float(BV[k]['v']) - d['resolved'],
                     recomputed=rec, prod_engine=Pb,
                     d_law=(None if rec is None else unr - rec),
                     d_prodcol=(None if rec is None else rec - d['resolved']),
                     games=g, fade_D=D, clock=c))

by_lane = {}
for r in rows:
    L = by_lane.setdefault(r['lane'], dict(n=0, maxabs=0.0, maxkey=None, sd=0.0, su=0.0, sp=0.0))
    L['n'] += 1
    L['sd'] += r['derived']
    L['su'] += r['unrounded']
    L['sp'] += r['printed']
    if abs(r['delta']) > L['maxabs']:
        L['maxabs'], L['maxkey'] = abs(r['delta']), r['key']

tot_der = sum(r['derived'] for r in rows)
tot_unr = sum(r['unrounded'] for r in rows)
tot_prn = sum(r['printed'] for r in rows)
mx = max(rows, key=lambda r: abs(r['delta']))
over = [r for r in rows if abs(r['delta']) > 1.5]
moved = [r for r in rows if r['lane'] in ('sitter', 'thin') and abs(r['delta']) > 0.05]

P = print
P('=' * 112)
P('ORDER 30B-N -- ROW CONTROL: THE WIRED LAW vs THE DERIVED RESOLVED BOARD')
P('=' * 112)
P('  built board : %s' % BOARD)
P('  derived     : resolution/RESOLVED_ALLROWS.json  (control_total %.1f)' % AR['control_total'])
P('  compared    : %d rows' % len(rows))
for _l in BOOT.splitlines():
    if 'ORDER 30B-N' in _l or 'ORDER 30B-P STEP-3' in _l:
        P('  DIAL PRINT  : %s' % _l.strip()[:150])
P('')
P('A. THE CONTROL -- UNROUNDED ev()/_PL_F vs the derived board (no print rounding in this comparison)')
P('  %-8s %5s %12s %12s %10s %10s  %s'
  % ('lane', 'n', 'derived', 'wired', 'delta', 'max|d|', 'worst row'))
for L in ('sitter', 'thin', 'bridge', 'deep'):
    if L not in by_lane:
        continue
    d = by_lane[L]
    P('  %-8s %5d %12.1f %12.1f %+10.2f %10.5f  %s'
      % (L, d['n'], d['sd'], d['su'], d['su'] - d['sd'], d['maxabs'], d['maxkey']))
P('  %-8s %5d %12.1f %12.1f %+10.2f' % ('TOTAL', len(rows), tot_der, tot_unr, tot_unr - tot_der))
P('')
P('  max |delta| any row      : %.5f  (%s, lane %s, g=%.1f)' % (abs(mx['delta']), mx['key'], mx['lane'], mx['games']))
P('  rows with |delta| > 1.5  : %d   %s' % (len(over), [r['key'] for r in over[:8]]))
P('  sitter/thin rows moved   : %d   %s' % (len(moved), [(r['key'], round(r['delta'], 4)) for r in moved[:6]]))
P('  book total wired         : %.1f' % tot_unr)
P('  book total derived       : %.1f' % tot_der)
P('  total delta              : %+.2f  (%.5f%%)' % (tot_unr - tot_der, 100 * (tot_unr / tot_der - 1)))
P('')
P('B. DISCLOSURE -- the PRINTED integer board vs the derived board (print rounding, NOT scored)')
P('  printed total %.1f   derived %.1f   delta %+.1f   max|d| %.2f'
  % (tot_prn, tot_der, tot_prn - tot_der, max(abs(r['delta_printed']) for r in rows)))
P('  Every row can differ by up to 0.5 here for print precision alone; that is why A is the control.')
P('')
P('C. THE DECOMPOSITION -- WHERE DOES delta ACTUALLY COME FROM? (the question P3 exists to answer)')
P('   d_law     = engine ev()  MINUS the resolution arithmetic fed the ENGINE\'S OWN production leg.')
P('               This is the WIRING TEST. It is bounded by the blend site\'s own round() in ENGINE')
P('               currency, 0.5/_PL_F = %.4f board pts, which the preview lane has always carried.' % (0.5 / _PL_F))
P('   d_prodcol = that same arithmetic MINUS the derived board. This is the DERIVED BOARD\'S OWN')
P('               production-column artifact and has nothing to do with this seat\'s wiring.')
have = [r for r in rows if r['d_law'] is not None]
P('')
P('  %-8s %5s %12s %12s %12s %12s' % ('lane', 'n', 'max|d_law|', 'max|d_prod|', 'sum d_law', 'sum d_prod'))
for L in ('sitter', 'thin', 'bridge', 'deep'):
    sub = [r for r in have if r['lane'] == L]
    if not sub:
        continue
    P('  %-8s %5d %12.5f %12.5f %+12.2f %+12.2f'
      % (L, len(sub), max(abs(r['d_law']) for r in sub), max(abs(r['d_prodcol']) for r in sub),
         sum(r['d_law'] for r in sub), sum(r['d_prodcol'] for r in sub)))
P('  %-8s %5d %12.5f %12.5f %+12.2f %+12.2f'
  % ('ALL', len(have), max(abs(r['d_law']) for r in have), max(abs(r['d_prodcol']) for r in have),
     sum(r['d_law'] for r in have), sum(r['d_prodcol'] for r in have)))
_wr = [r for r in have if abs(r['d_law']) > 0.5 / _PL_F + 1e-6]
P('')
P('  rows where |d_law| EXCEEDS the blend-site round bound: %d   %s'
  % (len(_wr), [(r['key'], round(r['d_law'], 4)) for r in _wr[:6]]))
P('  -> THAT count is the real wiring test. 0 means the wired law IS the resolution arithmetic,')
P('     evaluated on the engine\'s own production leg, to the last representable digit.')
P('')
verdicts = {
    'P3a_sitter_thin_exact': len(moved) == 0,
    'P3b_max_delta_le_1p2': abs(mx['delta']) <= 1.2,
    'P3c_no_row_over_1p5': len(over) == 0,
    'P3d_total_within_150': abs(tot_unr - tot_der) <= 150.0,
    'P3e_715229_class': abs(tot_unr - 715228.6) < 500.0,
    # The band P3a/P3b/P3c SHOULD have carried. Reported beside them, never instead of them.
    'P3f_law_within_blendsite_round': len(_wr) == 0,
}
for k, v in verdicts.items():
    P('  %-24s %s' % (k, 'HELD' if v else 'BREACHED'))
P('')
P('  P3 VERDICT: %s' % ('HELD' if all(verdicts.values()) else 'BREACHED'))

json.dump(dict(board=BOARD, derived_total=tot_der, wired_total=tot_unr, printed_total=tot_prn,
               max_abs_delta=abs(mx['delta']), max_row=mx['key'], over_1p5=[r['key'] for r in over],
               sitter_thin_moved=[r['key'] for r in moved],
               by_lane={k: dict(n=v['n'], derived=v['sd'], wired=v['su'], printed=v['sp'],
                                maxabs=v['maxabs'], maxkey=v['maxkey']) for k, v in by_lane.items()},
               verdicts=verdicts, rows=rows), open(OUTP, 'w'), indent=1, sort_keys=True)
P('  wrote %s' % OUTP)
