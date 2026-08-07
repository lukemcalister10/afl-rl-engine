"""#334 stage B / STAGE 6 — THE FOUR-RUNG LANDING ON THE OWNER'S PRESENTATION BASIS.

Owner ruling (#334 comment 5217177098, verbatim): *"when I'm talking about the conservation of value, for
me it's about cohorts as a whole, not just ND picks (but the split is often helpful too). And why wouldn't
2023/24/25 drafts be included in this presentation given they too have year 0 and year 1 cohort ratings"*

So the table LEADS with the FULL COHORT (ND 1-64 + every pool route, classes 2004-2025 at reached years),
with the ND and pool splits beside it, and the TEACHING window (2004-2022) printed LAST and labelled.

Addendum 1 F4 (basis honesty) is discharged in the printed text: the owner's [1.04, 1.13] range BINDS on
the instrument it was ruled on — ND 1-64, teaching window — and the full-cohort figure is printed beside
it precisely so the basis question can go to the owner rather than being resolved by this seat.

Read straight off the committed matrices on the committed no-arb value convention. READ-ONLY.
"""
import os, sys, json, hashlib
import numpy as np

REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S6 = EV + '/stage6'
WINDOW_END = 2026
RUNGS = ['0.25', '0.5', '0.75', '1.0']
L = []
def P(s=''):
    print(s); L.append(s)

def recs(path):
    return {(r['key'], r['type'], r['year']): r for r in json.load(open(path))['recs']}

def md5(p): return hashlib.md5(open(p, 'rb').read()).hexdigest()

BASE_PATH = EV + '/stage5/noarb/per_entrant_338_stage5.json'
S4_PATH = EV + '/stage4_amend1/noarb/per_entrant_338_stage4a1.json'
S4 = recs(S4_PATH)                      # the pre-stage-5 baseline, for the sequence view
A = recs(BASE_PATH)                     # the stage-5 LANDED matrix = stage 6's baseline
M = {W: recs(S6 + '/noarb/per_entrant_338_rung%s.json' % W) for W in RUNGS}
keys = sorted(set(A) & set(S4) & set.intersection(*[set(M[W]) for W in RUNGS]))

def val(r, n):
    if r['year'] + n > WINDOW_END: return None
    if n == 0: return float(r['v0'])
    vp = r.get('vpath') or []
    if n - 1 >= len(vp): return 0.0
    v = vp[n - 1]
    return 0.0 if v is None else float(v)

def ratio(MM, ks, n=1):
    num = den = 0.0; cnt = 0
    for k in ks:
        r = MM[k]
        a, b = val(r, n), val(r, 0)
        if a is None or b is None or b <= 0: continue
        num += a; den += b; cnt += 1
    return (num / den if den else float('nan')), cnt

ND = lambda k: (A[k]['type'] == 'ND' and A[k].get('pick') and 1 <= A[k]['pick'] <= 64)
POOL = lambda k: not ND(k)
YR = lambda k, lo, hi: lo <= A[k]['year'] <= hi

POPS = [
    ('FULL COHORT ND+pool 2004-2025', lambda k: YR(k, 2004, 2025)),
    ('  ND 1-64, 2004-2025', lambda k: ND(k) and YR(k, 2004, 2025)),
    ('  pool routes, 2004-2025', lambda k: POOL(k) and YR(k, 2004, 2025)),
    ('ND 1-64, 2004-2022 (TEACHING WINDOW)', lambda k: ND(k) and YR(k, 2004, 2022)),
    ('  ND picks 1-20, 2004-2022', lambda k: ND(k) and YR(k, 2004, 2022) and A[k]['pick'] <= 20),
    ('  ND picks 21-64, 2004-2022', lambda k: ND(k) and YR(k, 2004, 2022) and A[k]['pick'] >= 21),
    ('class 2023 ND', lambda k: ND(k) and YR(k, 2023, 2023)),
    ('class 2024 ND', lambda k: ND(k) and YR(k, 2024, 2024)),
    ('class 2025 ND', lambda k: ND(k) and YR(k, 2025, 2025)),
]

P('=' * 118)
P('#334 stage B / STAGE 6 — THE FOUR-RUNG YEAR-1 LANDING, OWNER PRESENTATION BASIS (ruling 5217177098)')
P('=' * 118)
P('  The FULL COHORT leads. The teaching window is printed LAST and labelled. NO RUNG IS RECOMMENDED —')
P('  the four are symmetric candidates and the intensity ruling is the owner\'s (Addendum 1 F9/F10).')
P('')
P('  matrices: stage-4a1 %s | stage-5 LANDED %s' % (md5(S4_PATH)[:8], md5(BASE_PATH)[:8]))
for W in RUNGS:
    P('            rung %-5s %s' % (W, md5(S6 + '/noarb/per_entrant_338_rung%s.json' % W)[:8]))
P('')
P('  %-40s %6s %10s %10s %10s %10s %10s %10s' %
  ('population (year 1)', 'n', 'pre-s5', 's5 LANDED', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
P('  ' + '-' * 112)
OUT = {}
for nm, f in POPS:
    ks = [k for k in keys if f(k)]
    if not ks: continue
    r0, n0 = ratio(S4, ks); ra, na = ratio(A, ks)
    rr = [ratio(M[W], ks)[0] for W in RUNGS]
    OUT[nm.strip()] = dict(n=na, pre_stage5=r0, stage5=ra,
                           rungs={W: rr[i] for i, W in enumerate(RUNGS)})
    P('  %-40s %6d %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f'
      % (nm, na, r0, ra, rr[0], rr[1], rr[2], rr[3]))
P('')
tw = OUT['ND 1-64, 2004-2022 (TEACHING WINDOW)']
fc = OUT['FULL COHORT ND+pool 2004-2025']
P('  THE RANGE THE OWNER RULED, [1.04, 1.13], BINDS ON THE INSTRUMENT IT WAS RULED ON — ND 1-64, teaching')
P('  window (Addendum 1 F4). Distance to the 1.04 floor at each rung, on that instrument:')
for i, W in enumerate(RUNGS):
    v = tw['rungs'][W]
    P('     rung %-5s  %.6f   %s 1.04 by %+.6f   %s'
      % (W, v, 'above' if v >= 1.04 else 'below', v - 1.04,
         'INSIDE [1.04, 1.13]' if 1.04 <= v <= 1.13 else 'OUTSIDE the range'))
P('')
P('  ON THE FULL-COHORT BASIS the sequence does NOT reach 1.04 at any rung (%.4f .. %.4f). That is the'
  % (min(fc['rungs'].values()), max(fc['rungs'].values())))
P('  line Addendum 1 F4 required printed explicitly: the pool leg is 45%% of the cohort and takes ZERO')
P('  from stage 6 by construction (the declared pick taper zeroes the pool index effpk 65), because the')
P('  pool treatment is stage 7 on its own measurement (#334 comment 5217529020). THE BASIS QUESTION IS')
P('  THE OWNER\'S, at the side-by-side — this seat does not resolve it.')

P('')
P('  THE FULL-COHORT PATH, years 0-6 (the conservation view the owner asked to lead with):')
P('  %-4s %7s %10s %10s %10s %10s %10s %10s' %
  ('yr', 'n', 'pre-s5', 's5', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
P('  ' + '-' * 76)
full = [k for k in keys if YR(k, 2004, 2025)]
PATH = {}
for n in range(0, 7):
    r0, n0 = ratio(S4, full, n); ra, na = ratio(A, full, n)
    rr = [ratio(M[W], full, n)[0] for W in RUNGS]
    PATH[n] = dict(n=na, pre_stage5=r0, stage5=ra, rungs={W: rr[i] for i, W in enumerate(RUNGS)})
    P('  %-4d %7d %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f' % (n, na, r0, ra, rr[0], rr[1], rr[2], rr[3]))

P('')
P('  THE TEACHING-WINDOW PATH, ND 1-64 years 0-6:')
P('  %-4s %7s %10s %10s %10s %10s %10s %10s' %
  ('yr', 'n', 'pre-s5', 's5', 'rung .25', 'rung .50', 'rung .75', 'rung 1.0'))
P('  ' + '-' * 76)
nd = [k for k in keys if ND(k) and YR(k, 2004, 2022)]
NDPATH = {}
for n in range(0, 7):
    r0, _ = ratio(S4, nd, n); ra, na = ratio(A, nd, n)
    rr = [ratio(M[W], nd, n)[0] for W in RUNGS]
    NDPATH[n] = dict(n=na, pre_stage5=r0, stage5=ra, rungs={W: rr[i] for i, W in enumerate(RUNGS)})
    P('  %-4d %7d %10.6f %10.6f %10.6f %10.6f %10.6f %10.6f' % (n, na, r0, ra, rr[0], rr[1], rr[2], rr[3]))

json.dump(dict(populations=OUT, full_cohort_path=PATH, teaching_window_path=NDPATH),
          open(os.path.join(S6, 'owner_basis.json'), 'w'), indent=1)
open(os.path.join(S6, 'OWNER_BASIS.txt'), 'w').write('\n'.join(L) + '\n')
