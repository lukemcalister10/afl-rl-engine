#!/usr/bin/env python3
"""ORDER 33 W1 -- CONTROL: the 31-F beta derivation RERUN WHOLE, outputs repointed to this seat.

The instrument is `o30bm_measure.py` (the 30B-M panel harness), executed with the SAME four
character-level substitutions ORDER 31-F used (`o31f_rederive_beta.py`), except the two OUTPUT paths
and the scratch staging land in THIS seat's locations so nothing committed is overwritten. The five
band coefficients must reproduce docs/evidence/candidate_31f/BETA_31F.json at deviation 0, or the
seat STOPS (PREREG_W1.md P1).

READ-ONLY on the repo: writes only into docs/evidence/order33_w1_2026-08-17/ and the scratchpad.
"""
import os, sys, json, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')
SPW1 = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o33w1'
os.makedirs(SPW1, exist_ok=True)

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
assert HARNESS_MD5 == 'e910fe6482ab7b05a92f18c173667073', 'harness moved: %s' % HARNESS_MD5

SUBS = [
    ("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
     "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
    ("POSV = V0ART['posv_out']",
     "POSV = V0ART['posv_headfixed']"),
    ("OUT_JSON = os.path.join(HERE, 'PERSISTENCE_TABLE.json')",
     "OUT_JSON = os.path.join(ROOT, 'docs', 'evidence', 'order33_w1_2026-08-17', 'PERSISTENCE_W1CTRL.json')"),
    ("OUT_TXT = os.path.join(HERE, 'MEASURE_out.txt')",
     "OUT_TXT = os.path.join(ROOT, 'docs', 'evidence', 'order33_w1_2026-08-17', 'MEASURE_W1CTRL_out.txt')"),
    ("SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'",
     "SP = %r" % SPW1),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique / not found: %r' % a[:60]
    _run = _run.replace(a, b)
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(str(s)); print(s)

P('ORDER 33 W1 CONTROL -- the 31-F beta derivation rerun whole')
P('  instrument     %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s' % HARNESS_MD5)
P('  as-run md5     %s' % RUN_MD5)
for a, b in SUBS:
    P('    SUB  %-78s ->  %s' % (a[:78], b[:96]))
P('')

_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), {'__name__': '__main__', '__file__': SRC})
open(os.path.join(HERE, 'MEASURE_W1CTRL_console.txt'), 'w').write(_buf.getvalue())
P('  harness ran clean; console MEASURE_W1CTRL_console.txt (%d lines)' % _buf.getvalue().count('\n'))

NEW = json.load(open(os.path.join(HERE, 'PERSISTENCE_W1CTRL.json')))
REF = json.load(open(os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'BETA_31F.json')))
ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
NBF = NEW['q1_persistence']['band_fits']
RBF = REF['band_fits_31f']
P('')
P('P1 CHECK: the five band coefficients against BETA_31F.json')
P('  %-8s %8s %14s %14s %12s' % ('band', 'n', 'BETA_31F', 'W1 CONTROL', 'deviation'))
worst = 0.0
DEV = {}
for nm in ORDER:
    d = float(NBF[nm]['beta_v0']) - float(RBF[nm]['beta_v0'])
    DEV[nm] = d
    worst = max(worst, abs(d))
    P('  %-8s %8d %14.10f %14.10f %+12.3e'
      % (nm, NBF[nm]['n'], float(RBF[nm]['beta_v0']), float(NBF[nm]['beta_v0']), d))
P('  max |deviation| = %.3e   n identical: %s   clusters identical: %s'
  % (worst, all(NBF[nm]['n'] == RBF[nm]['n'] for nm in ORDER),
     all(NBF[nm]['n_clusters'] == RBF[nm]['n_clusters'] for nm in ORDER)))
VERDICT = 'PASS' if worst == 0.0 else ('PASS (fp-noise <1e-12)' if worst < 1e-12 else 'FAIL')
P('  P1 VERDICT: %s' % VERDICT)

json.dump(dict(order='ORDER 33 W1 CONTROL', instrument=os.path.relpath(SRC, ROOT),
               instrument_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               deviations=DEV, max_abs_deviation=worst, verdict=VERDICT),
          open(os.path.join(HERE, 'CONTROL_W1.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'CONTROL_W1_out.txt'), 'w').write('\n'.join(OUT) + '\n')
if VERDICT == 'FAIL':
    raise SystemExit('ORDER 33 W1 STOP: control did not reproduce BETA_31F (max dev %.3e)' % worst)
print('written: CONTROL_W1.json / CONTROL_W1_out.txt / PERSISTENCE_W1CTRL.json')
