#!/usr/bin/env python3
"""ORDER 31-F  --  F1(d): THE 30B-C STALL COEFFICIENTS (Phi), RE-DERIVED ON THE HEAD-FIXED v0s.

The brief names four re-derivations (fade, beta, the rho backbone, printed-day-0).  Phi is NOT among
them, and there is a real argument that it need not move: Phi is the RATIO beta_stall/beta_pooled, and
both numerator and denominator are coefficients on the SAME moved regressor, so to first order the ratio
is invariant.  THE SEAT DID NOT RELY ON THAT ARGUMENT.  The ratio is re-measured, because "to first
order" is not a measurement and the whole point of R1 is that a measurement travels with its ruler.

`o30bc_circ.py` is run WHOLE with THREE character-level substitutions, each printed:
    SRC = open(MEASURE).read()   ->  the same text with the head-fixed v0 surface substituted in
    OUT_JSON / OUT_TXT           ->  docs/evidence/candidate_31f/
The 30B-M harness's own md5 pin is left in place and still asserts against the UNMODIFIED file on disk.
"""
import os, sys, json, math, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'one_machinery_2026-08-14', 'circularity', 'o30bc_circ.py')

V0SUB = [("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
          "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
         ("POSV = V0ART['posv_out']", "POSV = V0ART['posv_headfixed']")]
_v0expr = ('open(MEASURE).read()' +
           ''.join('.replace(%r, %r)' % (a, b) for a, b in V0SUB))

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()
SUBS = [
    ('SRC = open(MEASURE).read()', 'SRC = ' + _v0expr),
    ("OUT_JSON = os.path.join(HERE, 'CIRCULARITY.json')",
     "OUT_JSON = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'CIRCULARITY_31F.json')"),
    ("OUT_TXT = os.path.join(HERE, 'CIRC_out.txt')",
     "OUT_TXT = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'CIRC_31F_out.txt')"),
    # The harness's BAND COEFFICIENT CONTROL asserts its panel reproduces the 30B-M run's band betas to
    # 1e-9. That is a SAME-RULER control and it MUST be re-pointed at the 31-F run of the same harness,
    # or it would be asserting that a moved regressor did not move the coefficient. Re-pointed, the
    # control still binds exactly as hard: it proves this harness's panel IS the 30B-M panel.
    ("PTABLEP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')",
     "PTABLEP = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'PERSISTENCE_31F.json')"),
]
_run = _txt
for a, b in SUBS:
    assert _run.count(a) == 1, 'substitution target not unique: %r' % a[:60]
    _run = _run.replace(a, b)
RUN_MD5 = hashlib.md5(_run.encode()).hexdigest()

OUT = []
def P(s=''):
    OUT.append(s); print(s)

P('ORDER 31-F  F1(d) -- THE 30B-C STALL COEFFICIENTS, RE-DERIVED ON THE HEAD-FIXED v0 SURFACE')
P('  instrument     %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s' % HARNESS_MD5)
P('  as-run md5     %s' % RUN_MD5)
for a, b in SUBS:
    P('    SUB  %-52s ->  %s' % (a[:52], b[:110]))
P('')

_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    exec(compile(_run, SRC, 'exec'), {'__name__': '__main__', '__file__': SRC})
open(os.path.join(HERE, 'CIRC_31F_console.txt'), 'w').write(_buf.getvalue())
P('  harness ran clean; full console CIRC_31F_console.txt (%d lines)' % _buf.getvalue().count('\n'))
P('')

NEW = json.load(open(os.path.join(HERE, 'CIRCULARITY_31F.json')))
OLD = json.load(open(os.path.join(EV, 'one_machinery_2026-08-14', 'circularity', 'CIRCULARITY.json')))
BETA = json.load(open(os.path.join(HERE, 'BETA_31F.json')))
ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
MIDS = [2.5, 10.5, 25.5, 53.0, 85.5]

P('THE STALL COHORT\'S OWN COEFFICIENT ON v0, BAND BY BAND')
P('  %-8s %6s %14s %14s %12s' % ('band', 'mid', 'COMMITTED', '31-F HEAD-FIX', 'drift'))
NS, OS_ = {}, {}
for nm, m in zip(ORDER, MIDS):
    o = OLD['beta_stall_by_band'].get(nm); n = NEW['beta_stall_by_band'].get(nm)
    ov = float(o['beta_v0']) if isinstance(o, dict) else None
    nv = float(n['beta_v0']) if isinstance(n, dict) else None
    OS_[m] = ov; NS[m] = nv
    P('  %-8s %6.1f %14s %14s %12s'
      % (nm, m, ('%.7f' % ov) if ov is not None else 'NO SIGNAL',
         ('%.7f' % nv) if nv is not None else 'NO SIGNAL',
         ('%+.7f' % (nv - ov)) if (ov is not None and nv is not None) else '--'))
P('')

# ---- rebuild PhiStall by the SAME rule o31_fit.py uses (zero-floor, monotone, ratio to beta_mono) ----
def mono_dec(points):
    out, cur = [], None
    for g, y in points:
        cur = y if cur is None else min(cur, y)
        out.append((g, cur))
    return out

def loglin(pts, g):
    g = max(1e-9, float(g))
    if g <= pts[0][0]: return pts[0][1]
    if g >= pts[-1][0]: return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0.0 or y1 <= 0.0: return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]

BETA_MONO = [(m, b) for m, b in BETA['monotone_points']]
STALL_RAW = [(m, NS[m] if NS[m] is not None else 0.0) for m in MIDS]
STALL_FLOORED = [(m, max(0.0, b)) for m, b in STALL_RAW]
STALL_MONO = mono_dec(STALL_FLOORED)
def bmono(g): return loglin(BETA_MONO, g)
def bstall(g): return loglin(STALL_MONO, g)
PHI_RAW = []
for m in MIDS:
    p = bmono(m)
    PHI_RAW.append((m, 1.0 if p <= 0.0 else min(1.0, max(0.0, bstall(m) / p))))
PHI_PTS = mono_dec(PHI_RAW)

OLD_PHI = [(2.5, 0.5834702550962193), (10.5, 0.28802290519477386), (25.5, 0.28802290519477386),
           (53.0, 0.0), (85.5, 0.0)]
P('PhiStall = beta_stall / beta_mono, ZERO-FLOORED THEN MADE NON-INCREASING (o31_fit.py\'s own rule)')
P('  %6s %14s %14s %14s %12s' % ('mid', 'beta_mono 31-F', 'beta_stall 31-F', 'PhiStall 31-F', 'COMMITTED'))
for (m, ph), (_, oph) in zip(PHI_PTS, OLD_PHI):
    P('  %6.1f %14.7f %14.7f %14.7f %12.7f' % (m, bmono(m), bstall(m), ph, oph))
P('')
P('  THE RATIO-INVARIANCE ARGUMENT, TESTED RATHER THAN ASSUMED:')
P('    max |PhiStall_31F - PhiStall_committed| = %.7f'
  % max(abs(ph - oph) for (_, ph), (_, oph) in zip(PHI_PTS, OLD_PHI)))
P('    the ratio moved by %s than the coefficients themselves did (max |beta_stall| drift %.7f)'
  % ('LESS' if max(abs(ph - oph) for (_, ph), (_, oph) in zip(PHI_PTS, OLD_PHI)) <
     max(abs(NS[m] - OS_[m]) for m in MIDS if NS[m] is not None and OS_[m] is not None) else 'MORE',
     max(abs(NS[m] - OS_[m]) for m in MIDS if NS[m] is not None and OS_[m] is not None)))
P('')

json.dump(dict(order='ORDER 31-F F1(d) -- Phi re-derived on head-fixed v0',
               instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5, as_run_md5=RUN_MD5,
               substitutions=[{'from': a, 'to': b} for a, b in SUBS],
               beta_stall_committed={str(m): OS_[m] for m in MIDS},
               beta_stall_31f={str(m): NS[m] for m in MIDS},
               beta_stall_floored=[[m, b] for m, b in STALL_FLOORED],
               beta_stall_monotone=[[m, b] for m, b in STALL_MONO],
               phistall_committed=[[m, b] for m, b in OLD_PHI],
               phistall_31f=[[m, b] for m, b in PHI_PTS]),
          open(os.path.join(HERE, 'PHI_31F.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE, 'PHI_31F_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: PHI_31F.json / PHI_31F_out.txt / CIRCULARITY_31F.json')
