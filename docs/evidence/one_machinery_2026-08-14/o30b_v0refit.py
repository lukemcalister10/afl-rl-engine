#!/usr/bin/env python3
# =====================================================================================================
# ORDER 30B  --  STEP 1: THE POSITIONAL v0 RE-FIT
# =====================================================================================================
# Cures A2 (RUCK 63/64 = 0, SF 64 = 18, MID 64 = 57) and the 107 published ascents, by the construction
# PREREG_30B §1 declared BEFORE this file existed in runnable form:
#
#   1. weighted PAVA, non-increasing in pick, weights = the artifact's own share_g(p)
#   2. FLOOR max(.,100) -- ruling 3, a lower bound, so pick 64 >= 100 per position and the approach to
#      it is monotone by construction
#   3. the -1-per-pick ORDERING TIEBREAK on every flat run of length >= 2 -- the same law as the all-in
#      curve (ordering_tiebreak.convention). Above the floor: centred on the block's weighted-mean index
#      so the block's weighted sum is preserved EXACTLY. On the floor plateau: anchored v(64) = 100 and
#      v(p) = 100 + (64-p), because a descending spread there would put pick 64 BELOW the ruled floor.
#   4. CONSERVATION: one scalar lambda on the above-floor part, v' = 100 + lambda*(v-100), chosen so the
#      share-weighted grand total equals sum_p curve(p) EXACTLY. lambda preserves both the monotone order
#      and the floor. NO SLASH -- it is a conservation scalar and it is published.
#
# The PER-PICK reconciliation residual vs the all-in curve is DISCLOSED in full, never hidden: the
# population identity (sum over picks) is exact, the per-pick one is not, and that is the price of
# monotonicity.
#
# READS  engine/rl_after/pvc_curve_v2.json      (pinned by md5 at entry)
# WRITES engine/rl_after/pvc_curve_v2.json      (nd_v0.posv re-stamped + a monotone_refit_30b block)
#        V0REFIT30B.json / V0REFIT30B_out.txt   (the full disclosure)
# =====================================================================================================
import json, hashlib, os, sys, collections
from collections import OrderedDict

ROOT = os.environ.get('RL_ROOT', '/home/user/afl-rl-engine/.claude/worktrees/agent-ac6abd0494353e85f')
ART = os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')
EVID = os.path.join(ROOT, 'docs/evidence/one_machinery_2026-08-14')
ART_MD5_IN = '911774bc92de0630199a4cc0c6bfac42'
FLOOR = 100.0
WRITE = ('--write' in sys.argv)

_OUT = []
def P(s=''):
    print(s)
    _OUT.append(s)

def md5f(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

got = md5f(ART)
P('ORDER 30B STEP 1 -- THE POSITIONAL v0 RE-FIT')
P('  artifact %s  md5 %s' % ('engine/rl_after/pvc_curve_v2.json', got))
if got != ART_MD5_IN:
    raise SystemExit('PIN FAILED: artifact md5 %s != expected %s' % (got, ART_MD5_IN))
P('  PIN HELD (%s)' % ART_MD5_IN)
P('')

# KEY ORDER IS PRESERVED ON PURPOSE: the artifact ships with its own (non-sorted) key order and a
# re-serialisation with sort_keys would produce a 1,796-line reordering diff that no reviewer can read.
# The written diff must show THE CHANGE and nothing else.
J = json.load(open(ART), object_pairs_hook=OrderedDict)
POS = list(J['nd_v0']['positions'])
posv = {g: {int(k): float(v) for k, v in J['nd_v0']['posv'][g].items()} for g in POS}
share = {g: {int(k): float(v) for k, v in J['nd_v0']['share'][g].items()} for g in POS}
curve = {int(k): float(v) for k, v in J['curve'].items()}
PICKS = list(range(1, 65))
CURVE_TOT = sum(curve[p] for p in PICKS)

# ---- entry disclosure ---------------------------------------------------------------------------
def ascents_of(tab):
    return [p for p in PICKS[1:] if tab[p] > tab[p - 1] + 1e-12]

P('ENTRY STATE (what the re-fit is fixing)')
P('  all-in curve  pick1 %.1f  pick64 %.1f  sum(1..64) %.1f' % (curve[1], curve[64], CURVE_TOT))
P('  %-6s %9s %9s %9s %9s %8s %9s' % ('pos', 'p1', 'p32', 'p63', 'p64', 'ascents', 'min'))
asc_in = {}
for g in POS:
    a = ascents_of(posv[g]); asc_in[g] = a
    P('  %-6s %9.2f %9.2f %9.2f %9.2f %8d %9.2f'
      % (g, posv[g][1], posv[g][32], posv[g][63], posv[g][64], len(a), min(posv[g].values())))
P('  TOTAL ASCENTS %d' % sum(len(a) for a in asc_in.values()))
sw_in = sum(share[g][p] * posv[g][p] for g in POS for p in PICKS)
mx_in = max(abs(sum(share[g][p] * posv[g][p] for g in POS) / curve[p] - 1.0) for p in PICKS)
P('  share-weighted total %.6f  (curve total %.6f)   per-pick max|ratio-1| %.3e' % (sw_in, CURVE_TOT, mx_in))
P('  A2 cells: RUCK63 %.2f  RUCK64 %.2f  SF64 %.2f  MID64 %.2f'
  % (posv['RUCK'][63], posv['RUCK'][64], posv['SF'][64], posv['MID'][64]))
P('')

# ---- 1. weighted PAVA, non-increasing -----------------------------------------------------------
def pava_ni(vals, wts):
    """Weighted isotonic (non-increasing) regression, pool-adjacent-violators. Returns (fitted, blocks)
    where blocks is the list of index-lists that were pooled. The weighted sum is preserved EXACTLY
    inside every block, hence globally."""
    blocks = [[i] for i in range(len(vals))]
    bv = list(vals); bw = list(wts)
    i = 0
    while i < len(blocks) - 1:
        if bv[i] < bv[i + 1] - 1e-15:                      # violation of non-increasing
            w = bw[i] + bw[i + 1]
            v = (bv[i] * bw[i] + bv[i + 1] * bw[i + 1]) / w if w > 0 else (bv[i] + bv[i + 1]) / 2.0
            blocks[i] = blocks[i] + blocks[i + 1]; bv[i] = v; bw[i] = w
            del blocks[i + 1]; del bv[i + 1]; del bw[i + 1]
            if i > 0:
                i -= 1
        else:
            i += 1
    out = [None] * len(vals)
    for bi, blk in enumerate(blocks):
        for j in blk:
            out[j] = bv[bi]
    return out, blocks

STAGE = {}
pava = {}; blocks_of = {}
for g in POS:
    v = [posv[g][p] for p in PICKS]
    w = [share[g][p] for p in PICKS]
    f, blks = pava_ni(v, w)
    pava[g] = {PICKS[i]: f[i] for i in range(len(PICKS))}
    blocks_of[g] = [[PICKS[i] for i in b] for b in blks]

P('STAGE 1 -- WEIGHTED PAVA (non-increasing, weights = share_g(p))')
P('  %-6s %9s %9s %9s %8s %8s' % ('pos', 'p1', 'p32', 'p64', 'blocks', 'pooled'))
for g in POS:
    nb = sum(1 for b in blocks_of[g] if len(b) > 1)
    npooled = sum(len(b) for b in blocks_of[g] if len(b) > 1)
    P('  %-6s %9.2f %9.2f %9.2f %8d %8d' % (g, pava[g][1], pava[g][32], pava[g][64], nb, npooled))
    assert not ascents_of(pava[g]), 'PAVA left an ascent in %s' % g
sw_pava = sum(share[g][p] * pava[g][p] for g in POS for p in PICKS)
P('  share-weighted total after PAVA %.6f   drift vs curve total %.3e (PAVA conserves by construction)'
  % (sw_pava, sw_pava - CURVE_TOT))
P('')

# ---- 2. FLOOR 100 -------------------------------------------------------------------------------
flo = {g: {p: max(pava[g][p], FLOOR) for p in PICKS} for g in POS}
lift = {g: sum(share[g][p] * (flo[g][p] - pava[g][p]) for p in PICKS) for g in POS}
P('STAGE 2 -- FLOOR 100 AT PICK 64 PER POSITION (ruling 3), applied as the lower bound max(.,100)')
P('  %-6s %8s %10s %12s' % ('pos', 'n_lifted', 'first_pick', 'weighted_lift'))
for g in POS:
    lifted = [p for p in PICKS if flo[g][p] > pava[g][p] + 1e-12]
    P('  %-6s %8d %10s %12.4f' % (g, len(lifted), (lifted[0] if lifted else '-'), lift[g]))
    assert flo[g][64] >= FLOOR - 1e-9, 'floor missed at 64 for %s' % g
    assert not ascents_of(flo[g]), 'floor broke monotonicity in %s' % g
P('  TOTAL weighted lift %.4f board points (share-weighted)' % sum(lift.values()))
P('')

# ---- 3. the -1-per-pick ORDERING TIEBREAK -------------------------------------------------------
def flat_runs(tab):
    runs = []; i = 0
    while i < len(PICKS):
        j = i
        while j + 1 < len(PICKS) and abs(tab[PICKS[j + 1]] - tab[PICKS[i]]) <= 1e-12:
            j += 1
        if j > i:
            runs.append(PICKS[i:j + 1])
        i = j + 1
    return runs

tb = {g: dict(flo[g]) for g in POS}
TB_LOG = {g: [] for g in POS}
for g in POS:
    for run in flat_runs(flo[g]):
        val = flo[g][run[0]]
        ws = [share[g][p] for p in run]
        if abs(val - FLOOR) <= 1e-12:
            # THE FLOOR PLATEAU: anchor v(64)=100 and ascend by +1 per pick going shallower, so the
            # ruled floor is never breached. (These runs always terminate at pick 64 by construction.)
            for p in run:
                tb[g][p] = FLOOR + float(64 - p)
            TB_LOG[g].append(dict(picks='%d-%d' % (run[0], run[-1]), n=len(run), kind='floor_anchor',
                                  pooled_value=val,
                                  values=[round(tb[g][p], 6) for p in run],
                                  weighted_sum_pre=sum(share[g][p] * val for p in run),
                                  weighted_sum_post=sum(share[g][p] * tb[g][p] for p in run)))
        else:
            # ABOVE THE FLOOR: centre on the block's weighted-mean index so the block's weighted sum is
            # preserved EXACTLY while every pick descends by exactly 1 board point.
            W = sum(ws)
            c = (sum(share[g][p] * (p - run[0]) for p in run) / W) if W > 0 else (len(run) - 1) / 2.0
            for p in run:
                tb[g][p] = val + (c - (p - run[0]))
            TB_LOG[g].append(dict(picks='%d-%d' % (run[0], run[-1]), n=len(run), kind='weighted_centre',
                                  pooled_value=val,
                                  values=[round(tb[g][p], 6) for p in run],
                                  weighted_sum_pre=sum(share[g][p] * val for p in run),
                                  weighted_sum_post=sum(share[g][p] * tb[g][p] for p in run)))

# join guard: after spreading, a block join can go non-strict. Shift the SHALLOWER block up minimally.
JOIN_SHIFTS = {g: [] for g in POS}
for g in POS:
    for _ in range(200):
        bad = [p for p in PICKS[:-1] if tb[g][p] <= tb[g][p + 1] + 1e-12]
        if not bad:
            break
        p = bad[0]
        need = tb[g][p + 1] + 1.0 - tb[g][p]
        for q in PICKS:
            if q <= p:
                tb[g][q] += need
        JOIN_SHIFTS[g].append(dict(at_pick=p, shift=round(need, 6)))
    assert not ascents_of(tb[g]), 'tiebreak left an ascent in %s' % g
    assert all(tb[g][p] > tb[g][p + 1] + 1e-12 for p in PICKS[:-1]), 'tiebreak not strict in %s' % g
    assert tb[g][64] >= FLOOR - 1e-9, 'tiebreak broke the floor at 64 in %s' % g

P('STAGE 3 -- THE -1-PER-PICK ORDERING TIEBREAK (the same law as the all-in curve)')
P('  %-6s %7s %7s %10s %12s' % ('pos', 'runs', 'floorruns', 'joinshifts', 'weighted_drift'))
for g in POS:
    d = sum(share[g][p] * (tb[g][p] - flo[g][p]) for p in PICKS)
    P('  %-6s %7d %7d %10d %12.6f'
      % (g, len(TB_LOG[g]), sum(1 for b in TB_LOG[g] if b['kind'] == 'floor_anchor'),
         len(JOIN_SHIFTS[g]), d))
sw_tb = sum(share[g][p] * tb[g][p] for g in POS for p in PICKS)
P('  share-weighted total after tiebreak %.6f  (floor+tiebreak lift %.4f over curve total)'
  % (sw_tb, sw_tb - CURVE_TOT))
P('')

# ---- 4. CONSERVATION ----------------------------------------------------------------------------
# sum_gp share*(FLOOR + L*(v-FLOOR)) = CURVE_TOT  ->  L = (CURVE_TOT - sum share*FLOOR)/sum share*(v-FLOOR)
A = sum(share[g][p] * FLOOR for g in POS for p in PICKS)
Bx = sum(share[g][p] * (tb[g][p] - FLOOR) for g in POS for p in PICKS)
LAM = (CURVE_TOT - A) / Bx
fin = {g: {p: FLOOR + LAM * (tb[g][p] - FLOOR) for p in PICKS} for g in POS}
sw_fin = sum(share[g][p] * fin[g][p] for g in POS for p in PICKS)
P('STAGE 4 -- CONSERVATION (one published scalar, NO SLASH)')
P('  lambda = %.12f   (applied to the ABOVE-FLOOR part only: v\' = 100 + lambda*(v-100))' % LAM)
P('  share-weighted grand total %.9f   target %.9f   |drift| %.3e' % (sw_fin, CURVE_TOT, abs(sw_fin - CURVE_TOT)))
for g in POS:
    assert not ascents_of(fin[g]), 'conservation broke monotonicity in %s' % g
    assert fin[g][64] >= FLOOR - 1e-9, 'conservation broke the floor at 64 in %s' % g
P('  monotone + floor re-asserted AFTER conservation on all six positions: PASS')
P('')

# ---- THE DISCLOSED PER-PICK RECONCILIATION RESIDUAL ----------------------------------------------
resid = {}
for p in PICKS:
    s = sum(share[g][p] * fin[g][p] for g in POS)
    resid[p] = dict(mix=s, curve=curve[p], ratio=s / curve[p], abs=s - curve[p])
mx = max(PICKS, key=lambda p: abs(resid[p]['ratio'] - 1.0))
P('THE PER-PICK RECONCILIATION RESIDUAL -- DISCLOSED, NOT HIDDEN')
P('  The POPULATION identity (sum over picks) is EXACT by construction (lambda). The PER-PICK identity')
P('  sum_g share_g(p)*posv_g(p) == curve(p) is NOT preserved -- monotonicity and the floor are')
P('  constraints the raw relativities did not satisfy. The whole residual vector is published.')
P('  max |ratio-1| = %.4f at pick %d (mix %.2f vs curve %.2f)'
  % (abs(resid[mx]['ratio'] - 1.0), mx, resid[mx]['mix'], resid[mx]['curve']))
P('  %5s %10s %10s %8s   |  %5s %10s %10s %8s' % ('pick', 'mix', 'curve', 'ratio', 'pick', 'mix', 'curve', 'ratio'))
for i in range(32):
    a, b = PICKS[i], PICKS[i + 32]
    P('  %5d %10.2f %10.2f %8.4f   |  %5d %10.2f %10.2f %8.4f'
      % (a, resid[a]['mix'], resid[a]['curve'], resid[a]['ratio'],
         b, resid[b]['mix'], resid[b]['curve'], resid[b]['ratio']))
band = lambda lo, hi: max(abs(resid[p]['ratio'] - 1.0) for p in PICKS if lo <= p <= hi)
P('  max|ratio-1| by band:  1-20 %.4f   21-40 %.4f   41-54 %.4f   55-64 %.4f'
  % (band(1, 20), band(21, 40), band(41, 54), band(55, 64)))
P('')

# ---- THE CELL MOVES -----------------------------------------------------------------------------
P('THE RE-FIT, POSITION BY POSITION')
P('  %-6s %9s %9s %9s %9s %8s %9s %9s' % ('pos', 'p1', 'p32', 'p63', 'p64', 'ascents', 'min', 'max_move'))
for g in POS:
    mm = max(abs(fin[g][p] - posv[g][p]) for p in PICKS)
    P('  %-6s %9.2f %9.2f %9.2f %9.2f %8d %9.2f %9.2f'
      % (g, fin[g][1], fin[g][32], fin[g][63], fin[g][64], len(ascents_of(fin[g])), min(fin[g].values()), mm))
P('')
moves = sorted(((abs(fin[g][p] - posv[g][p]), g, p) for g in POS for p in PICKS), reverse=True)
P('  TWENTY LARGEST CELL MOVES')
P('  %-6s %5s %11s %11s %11s' % ('pos', 'pick', 'old', 'new', 'delta'))
for _, g, p in moves[:20]:
    P('  %-6s %5d %11.2f %11.2f %+11.2f' % (g, p, posv[g][p], fin[g][p], fin[g][p] - posv[g][p]))
P('')
P('  THE A2 CELLS, CURED')
for g, p in (('RUCK', 63), ('RUCK', 64), ('SF', 64), ('MID', 64)):
    P('    %-5s %2d   %8.2f  ->  %8.2f' % (g, p, posv[g][p], fin[g][p]))
P('')

# ---- OUTPUT -------------------------------------------------------------------------------------
DOC = {
    '_doc': ('ORDER 30B STEP 1 -- THE POSITIONAL v0 RE-FIT. Per position: weighted PAVA (weights = this '
             'artifact\'s own share_g(p)) -> FLOOR 100 (owner ruling 3, applied as the lower bound '
             'max(.,100) so pick 64 is >= 100 and the approach to it is monotone BY CONSTRUCTION) -> the '
             '-1-per-pick ORDERING TIEBREAK (the same law as the all-in curve; above the floor the block '
             'is centred on its weighted-mean index so the block weighted sum is preserved exactly, on '
             'the floor plateau it is anchored at v(64)=100 and ascends +1 per pick going shallower so '
             'the ruled floor is never breached) -> ONE PUBLISHED CONSERVATION SCALAR lambda on the '
             'above-floor part. PER-POSITION MONOTONICITY IS NOW ENFORCED: `ascents` is empty and stays '
             'empty. A2 IS CURED: no cell is below 100 anywhere. The PER-PICK reconciliation identity is '
             'NO LONGER exact -- it cannot be, because the raw relativities were not monotone -- and the '
             'FULL residual vector is published here rather than summarised away. The POPULATION identity '
             '(sum over picks 1..64) IS exact.'),
    'construction': ['weighted_pava_non_increasing', 'floor_100_lower_bound',
                     'minus_one_per_pick_ordering_tiebreak', 'one_conservation_scalar'],
    'floor': FLOOR,
    'lambda': LAM,
    'weights': 'nd_v0.share (this artifact)',
    'conservation': {'target_sum_curve_1_64': CURVE_TOT, 'achieved_share_weighted_total': sw_fin,
                     'abs_drift': abs(sw_fin - CURVE_TOT), 'verdict': 'EXACT'},
    'ascents_before': {g: asc_in[g] for g in POS},
    'ascents_before_total': sum(len(a) for a in asc_in.values()),
    'ascents_after_total': 0,
    'floor_weighted_lift': sum(lift.values()),
    'tiebreak_blocks': TB_LOG,
    'join_shifts': JOIN_SHIFTS,
    'per_pick_reconciliation': {str(p): {'mix': resid[p]['mix'], 'curve': resid[p]['curve'],
                                         'ratio': resid[p]['ratio']} for p in PICKS},
    'per_pick_max_abs_ratio_minus_1': abs(resid[mx]['ratio'] - 1.0),
    'per_pick_max_at_pick': mx,
    'supersedes': {'ruck_floor_63_64': J['nd_v0'].get('ruck_floor_63_64'),
                   'note': 'the zero floor at RUCK 63/64 (A2) is REPLACED by the ruled 100 floor'},
}

REPORT = dict(
    artifact_md5_in=ART_MD5_IN, floor=FLOOR, lam=LAM,
    curve_total=CURVE_TOT, share_weighted_total_in=sw_in, share_weighted_total_out=sw_fin,
    ascents_in={g: len(asc_in[g]) for g in POS}, ascents_out={g: 0 for g in POS},
    per_pick_residual={str(p): resid[p]['ratio'] for p in PICKS},
    per_pick_max_abs_ratio_minus_1=abs(resid[mx]['ratio'] - 1.0), per_pick_max_at=mx,
    posv_in={g: {str(p): posv[g][p] for p in PICKS} for g in POS},
    posv_out={g: {str(p): fin[g][p] for p in PICKS} for g in POS},
    a2_cells={'RUCK63': [posv['RUCK'][63], fin['RUCK'][63]], 'RUCK64': [posv['RUCK'][64], fin['RUCK'][64]],
              'SF64': [posv['SF'][64], fin['SF'][64]], 'MID64': [posv['MID'][64], fin['MID'][64]]},
    tiebreak_blocks=TB_LOG, join_shifts=JOIN_SHIFTS,
)
json.dump(REPORT, open(os.path.join(EVID, 'V0REFIT30B.json'), 'w'), indent=1, sort_keys=True)

if WRITE:
    for g in J['nd_v0']['posv']:                       # mutate IN PLACE: key order preserved exactly
        for k in J['nd_v0']['posv'][g]:
            J['nd_v0']['posv'][g][k] = fin[g][int(k)]
    J['nd_v0']['ascents'] = OrderedDict((g, []) for g in J['nd_v0']['ascents'])
    J['nd_v0']['monotone_refit_30b'] = DOC
    J['nd_v0']['ruck_floor_63_64'] = {
        '_doc': 'RETIRED BY ORDER 30B STEP 1. The zero floor at RUCK 63/64 was A2. Owner ruling 3 '
                'replaces it with a FLOOR OF 100 at pick 64 for EVERY position. See monotone_refit_30b.',
        'retired_by': 'ORDER 30B STEP 1', 'posv_63': fin['RUCK'][63], 'posv_64': fin['RUCK'][64]}
    J['nd_v0']['reconciliation'] = {
        'identity': 'sum_g share_g(p) * posv_g(p) == curve(p)  for every pick 1..64',
        'status': 'SUPERSEDED AT THE PER-PICK LEVEL BY ORDER 30B STEP 1 -- see monotone_refit_30b',
        'population_identity': 'sum over picks 1..64 IS exact (the conservation scalar)',
        'per_pick_max_abs_ratio_minus_1': abs(resid[mx]['ratio'] - 1.0), 'at_pick': mx,
        'prior_order29_reading': {'max_abs_ratio_minus_1': 2.220446049250313e-16, 'at_pick': 1}}
    J['nd_v0']['_doc'] = (J['nd_v0']['_doc'].replace(
        'PER-POSITION MONOTONICITY IS NOT ENFORCED (owner lean): ascents are published as data in '
        '`ascents`.',
        'PER-POSITION MONOTONICITY IS ENFORCED (ORDER 30B STEP 1, owner ruling 3): weighted PAVA + floor '
        '100 + the -1 ordering tiebreak + one conservation scalar; `ascents` is empty by construction and '
        'the per-pick reconciliation residual is published in `monotone_refit_30b`.'))
    with open(ART, 'w') as fh:
        json.dump(J, fh, indent=1)
    P('WROTE %s  new md5 %s' % (ART, md5f(ART)))
else:
    P('DRY RUN -- nothing written (pass --write to re-stamp the artifact)')

open(os.path.join(EVID, 'V0REFIT30B_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
