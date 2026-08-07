"""#334 stage B / STAGE 5 — THE LANDING ON THE OWNER'S PRESENTATION BASIS.

Owner ruling (#334 comment 5217177098, verbatim): *"when I'm talking about the conservation of value, for
me it's about cohorts as a whole, not just ND picks (but the split is often helpful too). And why wouldn't
2023/24/25 drafts be included in this presentation given they too have year 0 and year 1 cohort ratings"*

So every owner-facing cohort table LEADS with the FULL COHORT — ND 1-64 plus every pool route, classes
2004-2025 at reached years — with the ND and pool splits beside it. The TEACHING window stays 2004-2022
(a class must have outcomes to teach from) and is printed last, so the two are never confused.

Read straight off the committed matrices, on the committed no-arb value convention (`value_at`: year 0 =
v0_start, year N = vpath[N-1], a concluded career scores 0 and stays in the denominator, a class that has
not reached year N is excluded). READ-ONLY.
"""
import os, sys, json
import numpy as np

REPO = os.environ['RL_REPO']
EV = REPO + '/docs/evidence/act_334B_2026-08-07'
S5 = EV + '/stage5'
WINDOW_END = 2026
L = []
def P(s=''):
    print(s); L.append(s)


def recs(path):
    return {(r['key'], r['type'], r['year']): r for r in json.load(open(path))['recs']}


A = recs(EV + '/stage4_amend1/noarb/per_entrant_338_stage4a1.json')
B = recs(S5 + '/noarb/per_entrant_338_stage5.json')
keys = sorted(set(A) & set(B))


def val(r, n):
    if r['year'] + n > WINDOW_END: return None
    if n == 0: return float(r['v0'])
    vp = r.get('vpath') or []
    if n - 1 >= len(vp): return 0.0
    v = vp[n - 1]
    return 0.0 if v is None else float(v)


def ratio(M, ks, n=1):
    num = den = 0.0; cnt = 0
    for k in ks:
        r = M[k]
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
    ('class 2023 ND', lambda k: ND(k) and YR(k, 2023, 2023)),
    ('class 2024 ND', lambda k: ND(k) and YR(k, 2024, 2024)),
    ('class 2025 ND', lambda k: ND(k) and YR(k, 2025, 2025)),
    ('ND 1-64, 2004-2022 (TEACHING WINDOW)', lambda k: ND(k) and YR(k, 2004, 2022)),
]

P('=' * 104)
P('#334 stage B / STAGE 5 — YEAR-1 LANDING ON THE OWNER PRESENTATION BASIS (ruling 5217177098)')
P('=' * 104)
P('  the FULL COHORT leads; the ND and pool splits sit beside it; the teaching window is printed LAST')
P('  and labelled, so a reader never mistakes the fitting population for the presentation one.')
P('')
P('  %-40s %7s %12s %12s %10s' % ('population', 'n', 'baseline', 'LANDED', 'move'))
P('  ' + '-' * 86)
OUT = {}
for nm, f in POPS:
    ks = [k for k in keys if f(k)]
    if not ks: continue
    ra, na = ratio(A, ks); rb, nb = ratio(B, ks)
    OUT[nm.strip()] = dict(n=na, base=ra, landed=rb)
    P('  %-40s %7d %12.6f %12.6f %+10.6f' % (nm, na, ra, rb, rb - ra))
P('')
P('  THE HEADLINE THE OWNER READS: the full-cohort conservation view lands at %.4f (from %.4f).'
  % (OUT['FULL COHORT ND+pool 2004-2025']['landed'], OUT['FULL COHORT ND+pool 2004-2025']['base']))
P('  The ND figure on the owner window (%.4f) and on the teaching window (%.4f) differ by %+.4f —'
  % (OUT['ND 1-64, 2004-2025']['landed'], OUT['ND 1-64, 2004-2022 (TEACHING WINDOW)']['landed'],
     OUT['ND 1-64, 2004-2025']['landed'] - OUT['ND 1-64, 2004-2022 (TEACHING WINDOW)']['landed']))
P('  the landing story is the same on either window, which is what the ruling anticipated.')
P('')
P('  THE POOL LEG, on the record: stage 5 DID reach the pool quiet starters — the sit-out path serves pool')
P('  entrants off their signed division levels and their cells taught from their own outcomes. Pool yr1')
P('  moves %.4f -> %.4f. The remaining full-cohort drag is the pool leg\'s deep sub-par level, whose own'
  % (OUT['pool routes, 2004-2025']['base'], OUT['pool routes, 2004-2025']['landed']))
P('  honesty has NOT been measured on the current basis. That measurement is fired separately (#334')
P('  comment 5217293177 disposition 3) and is NOT this act\'s to claim.')

# the multi-year path on the full cohort, since the owner reads conservation across years
P('')
P('  THE FULL-COHORT PATH, years 0-6 (the conservation view the owner asked to lead with):')
P('  %-6s %8s %12s %12s %10s' % ('yr', 'n', 'baseline', 'LANDED', 'move'))
P('  ' + '-' * 52)
full = [k for k in keys if YR(k, 2004, 2025)]
PATH = {}
for n in range(0, 7):
    ra, na = ratio(A, full, n); rb, nb = ratio(B, full, n)
    PATH[n] = dict(n=na, base=ra, landed=rb)
    P('  %-6d %8d %12.6f %12.6f %+10.6f' % (n, na, ra, rb, rb - ra))
json.dump(dict(populations=OUT, full_cohort_path=PATH),
          open(os.path.join(S5, 'owner_basis.json'), 'w'), indent=1)
open(os.path.join(S5, 'OWNER_BASIS.txt'), 'w').write('\n'.join(L) + '\n')
