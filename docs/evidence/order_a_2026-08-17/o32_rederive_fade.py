#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — M6b-4(a): THE SITTER FADE ROW, RE-RUN WHOLE UNDER THE NEW DEFINITIONS.

The 30A-2 instrument (`o30a2_recut.py`, the o31f_rederive_fade.py lineage) is run WHOLE with exactly
one character-level substitution (its output directory, printed below). PREREG_32 P-D0 states the
prediction: the instrument's depth-N cells condition on GAMELESS histories (seasons 1..N-1 with zero
games), a population on which the Candidate 32 definitions — G*=2 played credit, delivered-season
reset, age-referenced gate bars — coincide exactly with the Candidate 31 definitions (no played
season to credit, no delivered season to reset, no AVG leg reached). Running the lineage whole under
the new definitions is therefore expected to REPRODUCE the 31-F row at deviation 0.0; this script
MEASURES that rather than assuming it, and HALTS with the moved row (PREREG_32 F4) if it moves.
"""
import os, sys, json, hashlib, io, contextlib

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

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

P('ORDER A / CANDIDATE 32 — THE SITTER FADE, RE-RUN WHOLE (30A-2 lineage) UNDER THE NEW DEFINITIONS')
P('  instrument      %s' % os.path.relpath(SRC, ROOT))
P('  committed md5   %s' % HARNESS_MD5)
P('  as-run md5      %s' % hashlib.md5(_run.encode()).hexdigest())
P('  THE ONLY EDIT   %r -> %r    (output directory only; no estimator touched)' % (_OLD, _NEW))
P('  artifact        engine/rl_after/pvc_curve_v2.json md5 %s (head-fixed, the Candidate 31/32 surface)'
  % hashlib.md5(open(os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json'), 'rb').read()).hexdigest())
P('')

NS = {'__name__': '__main__', '__file__': SRC}
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), NS)
open(os.path.join(HERE, 'RECUT30A2_32_console.txt'), 'w').write(_buf.getvalue())
P('  instrument ran clean; console RECUT30A2_32_console.txt (%d lines)' % _buf.getvalue().count('\n'))

NEWT = json.load(open(os.path.join(HERE, 'SITTER_DISCOUNT_TABLE_2.json')))
F31 = json.load(open(os.path.join(EV, 'candidate_31f', 'FADE_31F.json')))
LB = 'L-B outcome-blind floor'
W31 = {int(k): v for k, v in F31['wired'].items()}

NEW = {}
P('')
P('THE ROW, AGAINST THE CANDIDATE-31 (31-F) WIRED ROW:')
DEV = 0.0
for N in (2, 3, 4):
    n = NEWT['T1']['D'][LB].get(str(N))
    NEW[N] = n
    d = abs(n - W31[N])
    DEV = max(DEV, d)
    P('  D(%d) = %.16f    31-F %.16f    dev %.3e   (n=%d)'
      % (N, n, W31[N], d, NEWT['T1']['surfaces'][LB][str(N)]['n']))
P('  RAW(1) normaliser  31-F %.6f -> %.6f' % (F31['raw1_31f'], NEWT['T1']['raw1']))
P('')
P('PREREG_32 P-D0 verdict: %s (max deviation %.3e)'
  % ('HELD — the row reproduces at deviation 0.0; the D row does NOT move and every printed day-0 '
     'price is therefore unmoved by construction' if DEV == 0.0 else
     'FAILED — the row MOVED (F4): the moved row wires at stage 4 and the day-0 delta is reported', DEV))

json.dump(dict(order='ORDER A / Candidate 32 — fade row re-run whole under the new definitions',
               instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5,
               only_edit={'from': _OLD, 'to': _NEW},
               wired_31f={str(k): v for k, v in W31.items()},
               rederived_32={str(k): v for k, v in NEW.items()},
               max_deviation=DEV, p_d0_held=bool(DEV == 0.0),
               population_note='depth-N cells condition on gameless histories; the new '
                               'credit/reset/bar definitions coincide with the old on that population'),
          open(os.path.join(HERE, 'FADE_32.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'FADE_32_out.txt'), 'w').write('\n'.join(OUT) + '\n')
if DEV != 0.0:
    sys.exit('ORDER A F4: the fade row moved — see FADE_32.json')
print('written: FADE_32.json / FADE_32_out.txt')
