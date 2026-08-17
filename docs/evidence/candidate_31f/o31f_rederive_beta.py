#!/usr/bin/env python3
"""ORDER 31-F  --  F1(c): THE PERSISTENCE beta, RE-DERIVED AGAINST THE HEAD-FIXED v0s.  READ-ONLY.

R1 RULER DISCIPLINE.  The wired beta curve
    2.5 -> 0.2968 · 10.5 -> 0.3623 · 25.5 -> 0.2233 · 53.0 -> 0.1531 · 85.5 -> 0.0201
is `PERSISTENCE_TABLE.json::q1_persistence.band_fits[*].beta_v0`, the ORDER 30B-M panel regression's
coefficient ON v0.  It was estimated with v0 = the PRE-head-fix positional surface.  F1 moved that
surface, and a regression coefficient on a moved regressor moves.  So the panel is re-run.

THE HARNESS IS RUN WHOLE, NOT SLICED AND NOT RE-IMPLEMENTED.  `o30bm_measure.py` is executed with FOUR
character-level substitutions, each printed and each confined to a PATH or an OUTPUT LOCATION:

    V0P            -> docs/evidence/candidate_31f/HEADFIX_31F.json    (the head-fixed surface)
    POSV           -> V0ART['posv_headfixed']                          (that file's key for the surface)
    OUT_JSON/TXT   -> docs/evidence/candidate_31f/                     (do not overwrite the committed run)
    SP             -> .../scratchpad/o31f                              (this seat's own staging)

NO ESTIMATOR, NO POPULATION RULE, NO BAND, NO CLUSTER RULE AND NO CONTROL IS TOUCHED.
"""
import os, sys, json, math, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'pedigree_persistence_2026-08-14', 'o30bm_measure.py')
SP31F = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o31f'

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()

SUBS = [
    ("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
     "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
    ("POSV = V0ART['posv_out']",
     "POSV = V0ART['posv_headfixed']"),
    ("OUT_JSON = os.path.join(HERE, 'PERSISTENCE_TABLE.json')",
     "OUT_JSON = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'PERSISTENCE_31F.json')"),
    ("OUT_TXT = os.path.join(HERE, 'MEASURE_out.txt')",
     "OUT_TXT = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'MEASURE_31F_out.txt')"),
    ("SP = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'",
     "SP = %r" % SP31F),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique / not found: %r' % a[:60]
    _run = _run.replace(a, b)
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(s); print(s)

P('ORDER 31-F  F1(c) -- THE PERSISTENCE beta, RE-DERIVED ON THE HEAD-FIXED v0 SURFACE')
P('  instrument     %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s' % HARNESS_MD5)
P('  as-run md5     %s' % RUN_MD5)
for a, b in SUBS:
    P('    SUB  %-78s ->  %s' % (a[:78], b[:96]))
P('')

_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), {'__name__': '__main__', '__file__': SRC})
open(os.path.join(HERE, 'MEASURE_31F_console.txt'), 'w').write(_buf.getvalue())
P('  harness ran clean; full console MEASURE_31F_console.txt (%d lines)' % _buf.getvalue().count('\n'))
P('')

NEWP = json.load(open(os.path.join(HERE, 'PERSISTENCE_31F.json')))
OLDP = json.load(open(os.path.join(EV, 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')))
MIDS = {'0-5': 2.5, '6-15': 10.5, '16-35': 25.5, '36-70': 53.0, '71+': 85.5}
ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
WIRED_OLD = {2.5: 0.2968279384332228, 10.5: 0.362259307264279, 25.5: 0.22329587551741345,
             53.0: 0.15314862603013868, 85.5: 0.020068021140596692}

NBF = NEWP['q1_persistence']['band_fits']
OBF = OLDP['q1_persistence']['band_fits']
P('THE PANEL COEFFICIENT ON v0, BAND BY BAND  (beta_v0; the object the one law wires as beta)')
P('  %-8s %6s %8s %14s %14s %12s %9s %9s'
  % ('band', 'mid', 'n', 'COMMITTED', '31-F HEAD-FIX', 'drift', 't old', 't new'))
NEWPTS, DRIFT = [], {}
for nm in ORDER:
    o = OBF[nm]; n = NBF[nm]
    d = float(n['beta_v0']) - float(o['beta_v0'])
    DRIFT[MIDS[nm]] = d
    NEWPTS.append((MIDS[nm], float(n['beta_v0'])))
    P('  %-8s %6.1f %8d %14.7f %14.7f %+12.7f %9.2f %9.2f'
      % (nm, MIDS[nm], n['n'], float(o['beta_v0']), float(n['beta_v0']), d,
         float(o['t_v0']), float(n['t_v0'])))
P('')
P('  the wired points are the SAME OBJECT the committed READING.json carries, re-measured:')
P('    committed  ' + ' '.join('%.4f' % WIRED_OLD[m] for m, _ in NEWPTS))
P('    31-F       ' + ' '.join('%.4f' % b for _, b in NEWPTS))
P('    max |drift| %.7f' % max(abs(v) for v in DRIFT.values()))
P('')

# ---- the brief's DEEP-beta CI, re-read on the moved ruler -------------------------------------------
d71 = NBF['71+']
P('THE DEEP-beta CAVEAT, RE-READ (the owed word: the 71+ coefficient\'s interval spans zero)')
P('  71+ : beta_v0 %.6f   se %.6f   t %.3f   n %d   clusters %d'
  % (float(d71['beta_v0']), float(d71['se_v0']), float(d71['t_v0']), d71['n'], d71['n_clusters']))
P('  sigma %.4f   90%% CI %s' % (100 * float(d71.get('sigma', 0)), d71.get('sigma_ci90')))
P('')

MONO = []
_cur = None
for m, b in NEWPTS:
    _cur = b if _cur is None else min(_cur, b)
    MONO.append((m, _cur))
P('THE MONOTONE NON-INCREASING PROJECTION (the brief\'s "pi decays in g" -- unchanged rule)')
P('    measured  ' + ' '.join('%.4f' % b for _, b in NEWPTS))
P('    monotone  ' + ' '.join('%.4f' % b for _, b in MONO))
_del = [(m, b0, b1) for (m, b0), (_, b1) in zip(NEWPTS, MONO) if abs(b0 - b1) > 1e-12]
P('    DELETED BY THE PROJECTION: %s'
  % (', '.join('g=%.1f  %.4f -> %.4f' % (m, b0, b1) for m, b0, b1 in _del) if _del else 'nothing'))
P('')

BAD = [ 'beta(%.1f) = %.6f is negative' % (m, b) for m, b in MONO if b < -1e-12 ]
P('THE RULED PROPERTIES')
P('  beta non-negative at every knot ............ %s' % ('PASS' if not BAD else 'FAIL %s' % BAD))
P('  the monotone projection is non-increasing .. %s'
  % ('PASS' if all(MONO[i][1] >= MONO[i + 1][1] - 1e-15 for i in range(len(MONO) - 1)) else 'FAIL'))
if BAD:
    raise SystemExit('ORDER 31-F STOP: the re-derived beta broke a ruled property -- %s' % BAD)

json.dump(dict(order='ORDER 31-F F1(c) -- beta re-derived on head-fixed v0',
               instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               committed_points=[[m, WIRED_OLD[m]] for m, _ in NEWPTS],
               rederived_points=[[m, b] for m, b in NEWPTS],
               monotone_points=[[m, b] for m, b in MONO],
               drift={str(k): v for k, v in DRIFT.items()},
               band_fits_31f={nm: NBF[nm] for nm in ORDER},
               band_fits_committed={nm: OBF[nm] for nm in ORDER},
               deep_beta_ci={'band': '71+', 'beta_v0': float(d71['beta_v0']), 'se': float(d71['se_v0']),
                             't': float(d71['t_v0']), 'sigma_ci90': d71.get('sigma_ci90')}),
          open(os.path.join(HERE, 'BETA_31F.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'BETA_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: BETA_31F.json / BETA_31F_out.txt / PERSISTENCE_31F.json')
