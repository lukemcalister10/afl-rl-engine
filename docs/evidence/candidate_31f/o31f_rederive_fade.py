#!/usr/bin/env python3
"""ORDER 31-F  --  F1(b): THE SITTER FADE AND THE R1 CUMULATIVE BACKBONE, RE-DERIVED AGAINST THE
HEAD-FIXED v0s.  READ-ONLY (it writes only into docs/evidence/candidate_31f/).

R1 RULER DISCIPLINE: the measurement travels with its ruler.  The ruled row
D(2)/D(3)/D(4+) = 0.5502 / 0.2628 / 0.3460 and the cumulative backbone B(<=0/2/5/10) were both measured
with `v0` = the PRE-head-fix positional surface.  F1 moved that surface, so both are re-measured on it.

THE INSTRUMENT IS NOT RE-IMPLEMENTED AND NOT SLICED.  `o30a2_recut.py` is run WHOLE, with EXACTLY ONE
character-level substitution, printed and md5'd below:

    OUTD = HERE      ->      OUTD = <docs/evidence/candidate_31f>

so that the committed 30A-2 outputs are not overwritten.  Every estimator, every population rule, every
listing reading, every control and every prereg score is the committed instrument's own, byte for byte.
The ONLY substantive input that differs from the committed run is
`engine/rl_after/pvc_curve_v2.json::nd_v0.posv` -- the object under test.

THE OWNER'S RULINGS ARE APPLIED UNCHANGED (#334 c.5292534855): the wired row is the L-B outcome-blind
floor; the depth-4 > depth-3 kink is SELECTION and is kept unsmoothed; the deep end HOLDS FLAT at the
depth-4 value.
"""
import os, sys, json, math, hashlib, collections, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'sitter_fade_2026-08-14', 'o30a2_recut.py')

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
_OLD = "OUTD = HERE"
assert _txt.count(_OLD) == 1, 'the OUTD line is not unique -- refusing to substitute blindly'
_NEW = "OUTD = %r" % HERE
_run = _txt.replace(_OLD, _NEW)
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(s); print(s)

P('ORDER 31-F  F1(b) -- THE SITTER FADE + THE R1 BACKBONE, RE-DERIVED ON THE HEAD-FIXED v0 SURFACE')
P('  instrument      %s' % os.path.relpath(SRC, ROOT))
P('  committed md5   %s' % HARNESS_MD5)
P('  as-run md5      %s' % RUN_MD5)
P('  THE ONLY EDIT   %r  ->  %r     (output directory only; no estimator touched)' % (_OLD, _NEW))
P('  artifact        engine/rl_after/pvc_curve_v2.json  md5 %s   <-- HEAD-FIXED (F1)'
  % hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json'), 'rb').read()).hexdigest())
P('')

NS = {'__name__': '__main__', '__file__': SRC}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), NS)
open(os.path.join(HERE, 'RECUT30A2_31F_console.txt'), 'w').write(_buf.getvalue())
P('  instrument ran clean; its full console is RECUT30A2_31F_console.txt (%d lines)'
  % _buf.getvalue().count('\n'))
P('')

NEWT = json.load(open(os.path.join(HERE, 'SITTER_DISCOUNT_TABLE_2.json')))
OLDT = json.load(open(os.path.join(EV, 'sitter_fade_2026-08-14', 'SITTER_DISCOUNT_TABLE_2.json')))
R1T = json.load(open(os.path.join(EV, 'one_machinery_2026-08-14', 'FADE30B_TABLE.json')))
LB = 'L-B outcome-blind floor'
UN = 'UNCONDITIONAL (ORDER 30A)'

# =====================================================================================================
# THE FADE ROW
# =====================================================================================================
RULED = {2: 0.5501935857356868, 3: 0.26278629823610156, 4: 0.3460004697526451}
P('THE FADE, THREE RULERS SIDE BY SIDE  (D = mean(V_from_N/v0) / RAW(1), L-B outcome-blind floor)')
P('  %-6s %7s %14s %14s %14s %12s' % ('depth', 'n', '29B v0s', 'R1 / 30B v0s', '31-F HEAD-FIXED', 'drift vs R1'))
NEW, DRIFT = {}, {}
for N in ('1', '2', '3', '4', '5', '6'):
    o = OLDT['T1']['D'][LB].get(N); r = R1T['T1']['D'][LB].get(N); n = NEWT['T1']['D'][LB].get(N)
    nn = NEWT['T1']['surfaces'][LB][N].get('n', 0)
    if n is None:
        continue
    NEW[int(N)] = n
    if r is not None:
        DRIFT[int(N)] = n - r
    P('  %-6s %7d %14s %14s %14.7f %+12.7f'
      % (N, nn, ('%.7f' % o) if o is not None else '--', ('%.7f' % r) if r is not None else '--',
         n, (n - r) if r is not None else float('nan')))
P('  RAW(1) normaliser   R1 %.6f  ->  31-F %.6f   (%+.3f%%)'
  % (R1T['T1']['raw1'], NEWT['T1']['raw1'], 100.0 * (NEWT['T1']['raw1'] / R1T['T1']['raw1'] - 1.0)))
P('')

WIRED = {1: 1.0, 2: NEW[2], 3: NEW[3], 4: NEW[4]}
FLAT_FROM = 4
P('THE WIRED ROW, BY THE OWNER\'S OWN RULES (#334 c.5292534855 -- no new rule is made here)')
for N in (2, 3, 4):
    P('  D(%d) = %.16f      ruled %.16f      drift %+.7f' % (N, WIRED[N], RULED[N], WIRED[N] - RULED[N]))
P('  D(%d+) HOLDS FLAT at %.16f   -- the amendment that retired extrapolation through a selection kink'
  % (FLAT_FROM, WIRED[4]))
KINK = WIRED[4] > WIRED[3]
BAD = [ 'D(%d)=%.6f is not a usable fade' % (N, WIRED[N]) for N in (2, 3, 4) if not (0.0 < WIRED[N] <= 1.0) ]
if WIRED[2] >= 1.0: BAD.append('depth 2 is no longer a fade')
P('')
P('THE RULED PROPERTIES (prereg F10 -- THE STOP CONDITION)')
P('  0 < D <= 1 at every wired depth ............ %s' % ('PASS' if not BAD else 'FAIL %s' % BAD))
P('  depth 2 is still a fade .................... %s' % ('PASS' if WIRED[2] < 1.0 else 'FAIL'))
P('  the ruled depth-4 > depth-3 kink SURVIVES .. %s' % ('YES' if KINK else 'NO'))
P('  max |drift| vs the ruled row ............... %.7f' % max(abs(WIRED[N] - RULED[N]) for N in (2, 3, 4)))
if BAD:
    raise SystemExit('ORDER 31-F STOP: the re-derived fade broke a ruled property -- %s' % BAD)
P('')

# =====================================================================================================
# THE R1 CUMULATIVE BACKBONE  (BLEND30B.json::backbone, sourced FADE30B_DRIFT.json::backbone_r1)
# =====================================================================================================
ocum = R1T['T4']['cumulative_leq']; ncum = NEWT['T4']['cumulative_leq']
BB_R1 = {k: ocum['2|<=%s' % k]['D'] for k in ('0', '2', '5', '10')}
BB_NEW = {k: ncum['2|<=%s' % k]['D'] for k in ('0', '2', '5', '10')}
P('THE R1 CUMULATIVE BACKBONE  B(<= k games by depth 2), RE-DERIVED  (the object rho is calibrated on)')
P('  %-10s %7s %14s %14s %12s' % ('<= games', 'n', 'R1 / 30B v0s', '31-F HEAD-FIXED', 'drift'))
for k in ('0', '2', '5', '10'):
    P('  %-10s %7d %14.7f %14.7f %+12.7f'
      % ('<= ' + k, ncum['2|<=%s' % k]['n'], BB_R1[k], BB_NEW[k], BB_NEW[k] - BB_R1[k]))
P('  THE BACKBONE\'S OWN COHERENCE: B(<=0) must equal D(2) exactly (the RAW(1) normalisation)')
P('    B(<=0) %.16f    D(2) %.16f    |diff| %.3e'
  % (BB_NEW['0'], WIRED[2], abs(BB_NEW['0'] - WIRED[2])))
assert abs(BB_NEW['0'] - WIRED[2]) < 1e-9, 'the backbone/fade normalisation split apart'
P('')

json.dump(dict(order='ORDER 31-F F1(b) -- fade + backbone re-derived on head-fixed v0',
               instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
               only_edit={'from': _OLD, 'to': _NEW},
               ruled=RULED, r1={str(k): R1T['T1']['D'][LB].get(str(k)) for k in (1, 2, 3, 4, 5, 6)},
               rederived={str(k): v for k, v in NEW.items()},
               drift_vs_r1={str(k): v for k, v in DRIFT.items()},
               drift_vs_ruled={str(k): WIRED[k] - RULED[k] for k in (2, 3, 4)},
               wired={str(k): v for k, v in WIRED.items()}, flat_from=FLAT_FROM, kink_survives=KINK,
               raw1_r1=R1T['T1']['raw1'], raw1_31f=NEWT['T1']['raw1'],
               backbone_r1=BB_R1, backbone_31f=BB_NEW,
               cells={str(N): NEWT['T1']['surfaces'][LB].get(str(N)) for N in (1, 2, 3, 4, 5, 6)}),
          open(os.path.join(HERE, 'FADE_31F.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'FADE_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: FADE_31F.json / FADE_31F_out.txt / SITTER_DISCOUNT_TABLE_2.json (31-F copy)')
