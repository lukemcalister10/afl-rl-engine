#!/usr/bin/env python3
"""ORDER A / CANDIDATE 32 — M6b-2: THE 30B-C STALL COEFFICIENTS (Phi), RE-DERIVED UNDER THE
AGE-REFERENCED GATE BARS (S1 construction C3), ON THE HEAD-FIXED v0 SURFACE.

Lineage discipline = docs/evidence/candidate_31f/o31f_rederive_phi.py, carried: `o30bc_circ.py` is
run WHOLE with character-level substitutions, each printed and md5'd. The 31-F substitutions (the
head-fixed v0 surface and the re-pointed same-ruler controls) are CARRIED VERBATIM; this act adds
exactly ONE substantive substitution — the DELIVERED predicate's AVG leg reads the age-referenced
bar `O32_AGEBAR(pos, season_year - birth_year)` instead of the flat `BARS[pos]`. The games leg
(>= 10.0) is untouched: S1's order re-references only the AVG leg.

TWO RUNS, in this order:
  CONTROL  Δ≡0 (O32_AGEBAR == BARS at every age): must reproduce CIRCULARITY_31F.json's
           beta_stall_by_band at deviation 0.0 — proves the substitution machinery is inert
           (PREREG_32 F3; a failure HALTS the order).
  REAL     Δ = the S1 C3 class-pooled development offsets (PREREG_32 M1 constants), cap law
           structural (Δ >= 0, flat from age 24, ages <= 18 take the age-18 column).

PhiStall is then rebuilt by o31_fit.py's OWN rule (zero-floor, monotone non-increasing, ratio to
the UNCHANGED 31-F monotone beta — R-W1: beta does not move — clip [0,1], monotone), exactly as
o31f_rederive_phi.py did. Output: PHI_32.json (the stage-4 Phi row), CIRCULARITY_32.json,
CIRCULARITY_32_CTRL.json, consoles.
"""
import os, sys, json, math, hashlib, io, contextlib

HERE = os.path.dirname(os.path.abspath(__file__))
EV = os.path.dirname(HERE)
ROOT = os.path.dirname(os.path.dirname(EV))
SRC = os.path.join(EV, 'one_machinery_2026-08-14', 'circularity', 'o30bc_circ.py')

# ---- the S1 C3 offsets (PREREG_32 M1; CONSTRUCTIONS_S1.json) --------------------------------------
TALL = {'KPD', 'KPF', 'RUCK'}
D_TALL = {18: 22.334475609756097, 19: 20.55500752464971, 20: 16.306362402208926,
          21: 11.588672690048071, 22: 7.826894964594814, 23: 6.439783302063788}
D_SMALL = {18: 20.080511089352214, 19: 20.080511089352214, 20: 14.306977484301457,
           21: 11.265167414136857, 22: 6.761247284555768, 23: 4.584052475875439}

C3 = json.load(open(os.path.join(EV, 'order32_s1_2026-08-17', 'CONSTRUCTIONS_S1.json')))
FLAT = C3['bars_flat']
# construction-time assert: the transcribed deltas reproduce the S1 C3 table cell-for-cell
for key, bar in C3['C3'].items():
    pos, a = key.split('|'); a = int(a)
    dl = (D_TALL if pos in TALL else D_SMALL)[a]
    assert abs((FLAT[pos] - dl) - bar) < 1e-6, 'C3 transcription broken at %s: %r vs %r' % (key, FLAT[pos] - dl, bar)
print('C3 transcription verified against CONSTRUCTIONS_S1.json: all %d cells to 1e-6' % len(C3['C3']))


def agebar_real(pos, age):
    """bar(pos, age): flat minus the class-pooled development gap; cap law structural."""
    if age is None or age >= 24:
        return FLAT[pos]
    a = max(18, min(23, int(age)))
    return FLAT[pos] - (D_TALL if pos in TALL else D_SMALL)[a]


def agebar_ctrl(pos, age):
    return FLAT[pos]


# ---- the substitutions ----------------------------------------------------------------------------
V0SUB = [("V0P = os.path.join(ROOT, 'docs', 'evidence', 'one_machinery_2026-08-14', 'V0REFIT30B.json')",
          "V0P = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'HEADFIX_31F.json')"),
         ("POSV = V0ART['posv_out']", "POSV = V0ART['posv_headfixed']")]
_v0expr = ('open(MEASURE).read()' + ''.join('.replace(%r, %r)' % (a, b) for a, b in V0SUB))

OLD_DEL = "        DELIVERED[(k, s['year'])] = bool(float(s['games']) >= 10.0 and float(s['avg']) >= BARS[pos])"
NEW_DEL = ("        DELIVERED[(k, s['year'])] = bool(float(s['games']) >= 10.0 and "
           "float(s['avg']) >= O32_AGEBAR(pos, s['year'] - e['birth_year']))")

_txt = open(SRC).read()
HARNESS_MD5 = hashlib.md5(_txt.encode()).hexdigest()


def build_run(tag):
    subs = [
        ('SRC = open(MEASURE).read()', 'SRC = ' + _v0expr),
        ("OUT_JSON = os.path.join(HERE, 'CIRCULARITY.json')",
         "OUT_JSON = %r" % os.path.join(HERE_A, 'CIRCULARITY_32%s.json' % tag)),
        ("OUT_TXT = os.path.join(HERE, 'CIRC_out.txt')",
         "OUT_TXT = %r" % os.path.join(HERE_A, 'CIRC_32%s_out.txt' % tag)),
        ("PTABLEP = os.path.join(ROOT, 'docs', 'evidence', 'pedigree_persistence_2026-08-14', 'PERSISTENCE_TABLE.json')",
         "PTABLEP = os.path.join(ROOT, 'docs', 'evidence', 'candidate_31f', 'PERSISTENCE_31F.json')"),
        (OLD_DEL, NEW_DEL),
    ]
    run = _txt
    for a, b in subs:
        assert run.count(a) == 1, 'substitution target not unique: %r' % a[:60]
        run = run.replace(a, b)
    return run, subs


HERE_A = HERE
OUT = []


def P(s=''):
    OUT.append(str(s)); print(s)


P('ORDER A / CANDIDATE 32 — Phi RE-DERIVED UNDER THE AGE-REFERENCED GATE BARS')
P('  instrument     %s' % os.path.relpath(SRC, ROOT))
P('  committed md5  %s' % HARNESS_MD5)

# THE TWO HARNESS RUNS MUST BE SEPARATE PROCESSES: _merged_recover.py's load-time patching of the
# level chain (cp._lvl_eff et al.) is not idempotent inside one interpreter — a second exec captures
# the first exec's patched function as its "original" and the level chain recurses. Mode dispatch:
#   run_ctrl / run_real  execute the harness once each (called as subprocesses by the default mode).
MODE = sys.argv[1] if len(sys.argv) > 1 else 'all'
if MODE in ('run_ctrl', 'run_real'):
    tag = '_CTRL' if MODE == 'run_ctrl' else ''
    fn = agebar_ctrl if MODE == 'run_ctrl' else agebar_real
    run, subs = build_run(tag)
    print('RUN %s  (as-run md5 %s)' % ('CONTROL Δ≡0' if tag else 'REAL C3 offsets',
                                       hashlib.md5(run.encode()).hexdigest()))
    for a, b in subs:
        print('    SUB  %-58s ->  %s' % (a.strip()[:58], b.strip()[:120]))
    NS = {'__name__': '__main__', '__file__': SRC, 'O32_AGEBAR': fn}
    _buf = io.StringIO()
    with contextlib.redirect_stdout(_buf):
        exec(compile(run, SRC, 'exec'), NS)
    open(os.path.join(HERE_A, 'CIRC_32%s_console.txt' % tag), 'w').write(_buf.getvalue())
    print('  harness ran clean; console CIRC_32%s_console.txt (%d lines)' % (tag, _buf.getvalue().count('\n')))
    sys.exit(0)

import subprocess
RESULTS = {}
for mode, tag in (('run_ctrl', '_CTRL'), ('run_real', '')):
    P('')
    r = subprocess.run([sys.executable, os.path.abspath(__file__), mode],
                       capture_output=True, text=True, cwd=HERE)
    P(r.stdout.rstrip())
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-4000:])
        raise SystemExit('ORDER A HALT: the %s harness run failed (rc=%d)' % (mode, r.returncode))
    RESULTS[tag] = json.load(open(os.path.join(HERE_A, 'CIRCULARITY_32%s.json' % tag)))

REF = json.load(open(os.path.join(EV, 'candidate_31f', 'CIRCULARITY_31F.json')))
ORDER = ['0-5', '6-15', '16-35', '36-70', '71+']
MIDS = [2.5, 10.5, 25.5, 53.0, 85.5]


def bs(d, nm):
    v = d['beta_stall_by_band'].get(nm)
    return float(v['beta_v0']) if isinstance(v, dict) else None


P('')
P('CONTROL — the Δ≡0 run against CIRCULARITY_31F.json (deviation must be 0.0):')
CTRL_OK = True
for nm in ORDER:
    a, b = bs(RESULTS['_CTRL'], nm), bs(REF, nm)
    dev = (abs(a - b) if (a is not None and b is not None) else (0.0 if a == b else float('nan')))
    if not (dev == 0.0):
        CTRL_OK = False
    P('  %-6s ctrl %-14s 31F %-14s dev %s' % (nm, a, b, dev))
if not CTRL_OK:
    raise SystemExit('ORDER A HALT (PREREG_32 F3): the Δ≡0 control did not reproduce '
                     'CIRCULARITY_31F beta_stall at deviation 0 — the substitution machinery is not inert.')
P('  CONTROL PASS: deviation 0.0 at every band.')

# ---- PhiStall rebuilt by o31_fit.py's rule, against the UNCHANGED 31-F monotone beta (R-W1) -------
BETA = json.load(open(os.path.join(EV, 'candidate_31f', 'BETA_31F.json')))


def mono_dec(points):
    out, cur = [], None
    for g, y in points:
        cur = y if cur is None else min(cur, y)
        out.append((g, cur))
    return out


def loglin(pts, g):
    g = max(1e-9, float(g))
    if g <= pts[0][0]:
        return pts[0][1]
    if g >= pts[-1][0]:
        return pts[-1][1]
    for i in range(1, len(pts)):
        g0, y0 = pts[i - 1]; g1, y1 = pts[i]
        if g0 <= g <= g1:
            t = (math.log(g) - math.log(g0)) / (math.log(g1) - math.log(g0))
            if y0 <= 0.0 or y1 <= 0.0:
                return y0 + t * (y1 - y0)
            return math.exp(math.log(y0) + t * (math.log(y1) - math.log(y0)))
    return pts[-1][1]


BETA_MONO = [(m, b) for m, b in BETA['monotone_points']]
NS_ = {m: bs(RESULTS[''], m2) for m, m2 in zip(MIDS, ORDER)}
STALL_FLOORED = [(m, max(0.0, NS_[m] if NS_[m] is not None else 0.0)) for m in MIDS]
STALL_MONO = mono_dec(STALL_FLOORED)


def bmono(g):
    return loglin(BETA_MONO, g)


def bstall(g):
    return loglin(STALL_MONO, g)


PHI_RAW = []
for m in MIDS:
    p = bmono(m)
    PHI_RAW.append((m, 1.0 if p <= 0.0 else min(1.0, max(0.0, bstall(m) / p))))
PHI_PTS = mono_dec(PHI_RAW)

OLD_PHI = [(2.5, 0.5792926948039687), (10.5, 0.298245232115451), (25.5, 0.298245232115451),
           (53.0, 0.0), (85.5, 0.0)]
P('')
P('PhiStall UNDER THE AGE-REFERENCED BARS (zero-floored, monotone, ratio to the UNCHANGED 31-F beta):')
P('  %6s %16s %16s %16s %14s' % ('mid', 'beta_stall_32', 'PhiStall_32', 'PhiStall_31F', 'drift'))
for (m, ph), (_, oph) in zip(PHI_PTS, OLD_PHI):
    P('  %6.1f %16.7f %16.7f %16.7f %+14.7f' % (m, bstall(m), ph, oph, ph - oph))

json.dump(dict(order='ORDER A / Candidate 32 — Phi re-derived under the age-referenced gate bars',
               instrument=os.path.relpath(SRC, ROOT), instrument_md5=HARNESS_MD5,
               control_dev0=CTRL_OK,
               beta_stall_31f={str(m): bs(REF, nm) for m, nm in zip(MIDS, ORDER)},
               beta_stall_32={str(m): NS_[m] for m in MIDS},
               beta_stall_floored=[[m, b] for m, b in STALL_FLOORED],
               beta_stall_monotone=[[m, b] for m, b in STALL_MONO],
               phistall_31f=[[m, b] for m, b in OLD_PHI],
               phistall_32=[[m, b] for m, b in PHI_PTS],
               beta_unchanged='R-W1: the denominator is BETA_31F monotone_points, untouched'),
          open(os.path.join(HERE_A, 'PHI_32.json'), 'w'), indent=1, sort_keys=True, default=float)
open(os.path.join(HERE_A, 'PHI_32_out.txt'), 'w').write('\n'.join(OUT) + '\n')
print('written: PHI_32.json / PHI_32_out.txt / CIRCULARITY_32.json / CIRCULARITY_32_CTRL.json')
