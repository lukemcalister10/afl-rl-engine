#!/usr/bin/env python3
# =====================================================================================================
# ORDER 31-F  --  F1: THE POSITIONAL v0 HEAD FIX (thin-sample shrink at all six curve heads)
# =====================================================================================================
# THE DEFECT.  nd_v0.posv is posv_g(p) = relat_g(p) * curve(p).  ORDER 30B Step 1 made it monotone with
# weighted PAVA.  Where relat_g(p) is estimated on almost no data it is noise, and PAVA pools that noise
# BACKWARD ONTO THE HEAD: RUCK pick 1 went 1,967.7 -> 3,477.2 because picks 2/3/4 (effective n 2.8/3.5/4.3)
# read 4,221 / 4,423 / 3,790.
#
# THE RULE (PREREG_31F §1.2, declared before this file ran).  At every one of the 384 cells, symmetrically:
#
#     w_gp        =  n_gp / (n_gp + K)                       K = 15, THIS PROJECT'S OWN K_SHRINK
#     relat'_g(p) =  w_gp * relat_g(p) + (1 - w_gp) * 1.0    K-toward-the-ALL-IN RELATIVITY
#     relat"_g(p) =  relat'_g(p) / sum_h share_h(p) relat'_h(p)          per-pick renormalisation
#     posv*_g(p)  =  relat"_g(p) * curve(p)
#
# n_gp is the LL ESTIMATOR'S OWN EFFECTIVE n (o26b_loclin.kernel_loclin), the same call the surface itself
# is built with.  The target is 1.0 -- the all-in curve's own relativity, which is the exact null of "this
# pick carries no position-specific evidence" AND the centroid of the reconciliation identity
# sum_g share_g(p) relat_g(p) = 1.  The renormalisation restores that identity EXACTLY, so the shrink
# CANNOT move the all-in ladder, the pooled head H, or the numeraire s.
#
# posv* is then fed through the COMMITTED o30b_v0refit.py PIPELINE, LIFTED BY SOURCE TEXT AND EXEC'D
# VERBATIM (PAVA -> floor 100 -> the -1 ordering tiebreak -> one conservation scalar).  The lifted text is
# md5'd and printed so the reuse is auditable.  NO STAGE IS ALTERED.
#
# READS   engine/rl_after/pvc_curve_v2.json            (md5-pinned at entry)
#         docs/evidence/one_machinery_2026-08-14/V0REFIT30B.json   (posv_in = the PRE-monotone surface)
#         docs/evidence/grace_adoption_2026-08-13/inputs/          (the ORDER-28 ND fit population)
# WRITES  HEADFIX_31F.json / HEADFIX_31F_out.txt
#         engine/rl_after/pvc_curve_v2.json            (only with --write)
# =====================================================================================================
import json, hashlib, os, sys, collections
from collections import OrderedDict

ROOT = os.environ.get('RL_ROOT', '/home/user/afl-rl-engine/.claude/worktrees/agent-a8ab36345dce038ee')
ART = os.path.join(ROOT, 'engine/rl_after/pvc_curve_v2.json')
EVID = os.path.join(ROOT, 'docs/evidence/candidate_31f')
REFIT30B = os.path.join(ROOT, 'docs/evidence/one_machinery_2026-08-14/V0REFIT30B.json')
REFIT_SRC = os.path.join(ROOT, 'docs/evidence/one_machinery_2026-08-14/o30b_v0refit.py')
O28 = os.path.join(ROOT, 'docs/evidence/grace_adoption_2026-08-13')
ART_MD5_IN = '06146b00daf2043487f58a8b9f842a1e'          # the land/order-29 tip's artifact, asserted below
K_SHRINK = 15
FLOOR = 100.0
WRITE = ('--write' in sys.argv)

_OUT = []
def P(s=''):
    print(s); _OUT.append(s)

md5f = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()

got = md5f(ART)
P('ORDER 31-F  F1 -- THE POSITIONAL v0 HEAD FIX (thin-sample shrink, all six heads)')
P('  artifact engine/rl_after/pvc_curve_v2.json  md5 %s' % got)
if os.environ.get('O31F_PIN', '1') != '0' and got != ART_MD5_IN:
    raise SystemExit('PIN FAILED: artifact md5 %s != expected %s' % (got, ART_MD5_IN))
P('  PIN HELD')

J = json.load(open(ART), object_pairs_hook=OrderedDict)
POS = list(J['nd_v0']['positions'])
share = {g: {int(k): float(v) for k, v in J['nd_v0']['share'][g].items()} for g in POS}
curve = {int(k): float(v) for k, v in J['curve'].items()}
PICKS = list(range(1, 65))
CURVE_TOT = sum(curve[p] for p in PICKS)
shipped = {g: {int(k): float(v) for k, v in J['nd_v0']['posv'][g].items()} for g in POS}

# ---- the PRE-monotone surface the shrink acts on -------------------------------------------------
R30 = json.load(open(REFIT30B))
posv_raw = {g: {int(k): float(v) for k, v in R30['posv_in'][g].items()} for g in POS}
assert {g: {p: round(R30['posv_out'][g][str(p)], 6) for p in PICKS} for g in POS} == \
       {g: {p: round(shipped[g][p], 6) for p in PICKS} for g in POS}, \
    'V0REFIT30B.posv_out is not what the artifact ships -- the lineage is broken'
P('  lineage HELD: V0REFIT30B.posv_out == the shipped nd_v0.posv')

# ---- the estimator's OWN effective n --------------------------------------------------------------
sys.path.insert(0, os.path.join(O28, 'inputs'))
import harness_pvc_REPINNED_pass3 as HP
import o26b_loclin as LL
L2 = json.load(open(os.path.join(O28, 'inputs/LAYER2.json')))
L1 = json.load(open(os.path.join(O28, 'inputs/layer1_player_seasons.json')))
E = {e['key']: e for e in L1['entries']}; ATTR = L2['attribution']; GA = L2['grace_a']
nd = [dict(key=k, pick=ATTR[k]['pick'], value=GA[k]['total'], pos=E[k]['position_group'])
      for k in L2['fit_nd_keys']]
posrows = {g: [r for r in nd if r['pos'] == g] for g in POS}
hard_n = collections.Counter((r['pos'], r['pick']) for r in nd)
effn = {}
for g in POS:
    nm = min(HP.NMIN, max(8.0, len(posrows[g]) / 4.0))
    _v, _e, _d = LL.kernel_loclin(posrows[g], PICKS, nm, HP.HMIN, HP.HMAX)
    effn[g] = {p: float(_e[i]) for i, p in enumerate(PICKS)}
P('  ND fit population %d rows; per-position rows %s'
  % (len(nd), ' '.join('%s %d' % (g, len(posrows[g])) for g in POS)))

# ---- THE SHRINK ------------------------------------------------------------------------------------
relat = {g: {p: posv_raw[g][p] / curve[p] for p in PICKS} for g in POS}
recon_pre = max(abs(sum(share[g][p] * relat[g][p] for g in POS) - 1.0) for p in PICKS)
P('  the pre-shrink reconciliation identity sum_g share_g(p) relat_g(p) == 1 holds to %.3e' % recon_pre)

w = {g: {p: effn[g][p] / (effn[g][p] + K_SHRINK) for p in PICKS} for g in POS}
rel1 = {g: {p: w[g][p] * relat[g][p] + (1.0 - w[g][p]) * 1.0 for p in PICKS} for g in POS}
nrm = {p: sum(share[g][p] * rel1[g][p] for g in POS) for p in PICKS}
rel2 = {g: {p: rel1[g][p] / nrm[p] for p in PICKS} for g in POS}
posv = {g: {p: rel2[g][p] * curve[p] for p in PICKS} for g in POS}       # <-- the pipeline's INPUT
recon_post = max(abs(sum(share[g][p] * rel2[g][p] for g in POS) - 1.0) for p in PICKS)
P('  the post-shrink reconciliation identity is restored EXACTLY to %.3e' % recon_post)
assert recon_post < 1e-12

P('')
P('THE SHRINK, AT THE HEAD (picks 1-6) -- credibility weight w, raw relativity, shrunk relativity')
for g in POS:
    P('  %-5s  ' % g + '  '.join('p%d n%.1f w%.2f %.3f->%.3f'
                                 % (p, effn[g][p], w[g][p], relat[g][p], rel2[g][p]) for p in range(1, 5)))
P('')
P('THE SHRINK, POSITION BY POSITION -- share-weighted mean |w| and the cells it barely moves')
P('  %-6s %6s %8s %8s %8s %10s' % ('pos', 'rows', 'min_w', 'mean_w', 'max_w', 'cells_w<0.5'))
for g in POS:
    ws = [w[g][p] for p in PICKS]
    P('  %-6s %6d %8.4f %8.4f %8.4f %10d'
      % (g, len(posrows[g]), min(ws), sum(ws) / 64.0, max(ws), sum(1 for x in ws if x < 0.5)))
P('')

# =====================================================================================================
# THE COMMITTED 30B STEP-1 PIPELINE, LIFTED BY SOURCE TEXT AND EXEC'D VERBATIM.
# =====================================================================================================
_src = open(REFIT_SRC).read()
_blk = _src.split("# ---- 1. weighted PAVA, non-increasing ")[1]
_blk = '# ---- 1. weighted PAVA, non-increasing ' + _blk.split('# ---- OUTPUT ')[0]
P('PIPELINE LIFT -- o30b_v0refit.py stages 1..4 + the residual disclosure, exec\'d VERBATIM')
P('  lifted text md5 %s   (%d lines)' % (hashlib.md5(_blk.encode()).hexdigest(), _blk.count('\n')))
P('')

def ascents_of(tab):
    return [p for p in PICKS[1:] if tab[p] > tab[p - 1] + 1e-12]
asc_in = {g: ascents_of(posv[g]) for g in POS}
NS = dict(PICKS=PICKS, POS=POS, posv=posv, share=share, curve=curve, CURVE_TOT=CURVE_TOT,
          FLOOR=FLOOR, P=P, ascents_of=ascents_of, asc_in=asc_in, json=json, collections=collections)
exec(_blk, NS)
fin = NS['fin']; LAM = NS['LAM']; resid = NS['resid']; sw_fin = NS['sw_fin']
TB_LOG = NS['TB_LOG']; JOIN_SHIFTS = NS['JOIN_SHIFTS']; mx = NS['mx']

# ---- THE RULED PROPERTIES, RE-ASSERTED --------------------------------------------------------------
BAD = []
for g in POS:
    if ascents_of(fin[g]): BAD.append('%s: monotonicity broken' % g)
    if fin[g][64] < FLOOR - 1e-9: BAD.append('%s: floor 100 breached at pick 64 (%.4f)' % (g, fin[g][64]))
    if min(fin[g].values()) < FLOOR - 1e-9: BAD.append('%s: a cell is below the floor' % g)
if abs(sw_fin - CURVE_TOT) > 1e-6: BAD.append('conservation drift %.3e' % abs(sw_fin - CURVE_TOT))
mxres = max(abs(resid[p]['ratio'] - 1.0) for p in PICKS)
P('THE RULED PROPERTIES, RE-ASSERTED AFTER THE HEAD FIX')
P('  per-position monotonicity (ascents==0) ... %s' % ('PASS' if not any(ascents_of(fin[g]) for g in POS) else 'FAIL'))
P('  floor 100 at pick 64, all six ........... %s' % ('PASS' if all(fin[g][64] >= FLOOR - 1e-9 for g in POS) else 'FAIL'))
P('  conservation |drift| .................... %.3e  %s' % (abs(sw_fin - CURVE_TOT),
                                                            'EXACT' if abs(sw_fin - CURVE_TOT) < 1e-6 else 'FAIL'))
P('  per-pick reconciliation max|ratio-1| .... %.4f at pick %d   (PRINTED IN FULL ABOVE, NOT ABSORBED)'
  % (mxres, mx))
P('  lambda (the one published conservation scalar) = %.12f' % LAM)
if BAD:
    raise SystemExit('ORDER 31-F HALT: the head fix broke a ruled property -- %s' % BAD)
P('')

# ---- THE HEAD, BEFORE AND AFTER ---------------------------------------------------------------------
P('THE HEAD FIX -- posv AT PICK 1, SHIPPED vs HEAD-FIXED (prereg F2/F3/F4/F5)')
P('  %-6s %8s %12s %12s %12s %10s' % ('pos', 'eff_n(1)', 'raw', 'SHIPPED', 'HEAD-FIXED', 'rel_move'))
head_moves = {}
for g in POS:
    d = fin[g][1] - shipped[g][1]
    head_moves[g] = d
    P('  %-6s %8.2f %12.1f %12.1f %12.1f %+9.1f%%'
      % (g, effn[g][1], posv_raw[g][1], shipped[g][1], fin[g][1], 100.0 * d / shipped[g][1]))
P('  LARGEST |head move| : %s' % max(POS, key=lambda g: abs(head_moves[g])))
P('  SMALLEST relative head move : %s'
  % min(POS, key=lambda g: abs(head_moves[g]) / shipped[g][1]))
P('')
P('THE WHOLE SURFACE, SHIPPED -> HEAD-FIXED')
SHOW = [1, 2, 3, 4, 5, 7, 10, 13, 16, 19, 20, 24, 25, 30, 35, 40, 42, 47, 52, 56, 60, 64]
for g in POS:
    P('  %-5s  ' % g + ' '.join('%d:%.0f->%.0f' % (p, shipped[g][p], fin[g][p]) for p in SHOW))
P('')
moves = sorted(((abs(fin[g][p] - shipped[g][p]), g, p) for g in POS for p in PICKS), reverse=True)
P('  TWENTY LARGEST CELL MOVES vs THE SHIPPED SURFACE')
P('  %-6s %5s %7s %11s %11s %11s' % ('pos', 'pick', 'eff_n', 'shipped', 'head-fixed', 'delta'))
for _, g, p in moves[:20]:
    P('  %-6s %5d %7.2f %11.1f %11.1f %+11.1f' % (g, p, effn[g][p], shipped[g][p], fin[g][p],
                                                  fin[g][p] - shipped[g][p]))
P('')

DOC = OrderedDict([
    ('_doc',
     'ORDER 31-F F1 -- THE POSITIONAL v0 HEAD FIX. A THIN-SAMPLE SHRINK applied SYMMETRICALLY at all six '
     'positional curve heads BEFORE the ORDER-30B monotone pipeline, curing the head inflation that the '
     'monotone enforcement created by pooling unmeasured cells backward onto pick 1 (the known case: RUCK '
     '1,967.7 -> 3,477.2 on effective n of 1.7-4.3). THE RULE, declared in PREREG_31F.md before it ran: '
     'w_gp = n_gp/(n_gp+K) with K=15 (this project\'s own K_SHRINK) and n_gp the LL estimator\'s OWN '
     'effective n; relat\' = w*relat + (1-w)*1.0, i.e. K-TOWARD-THE-ALL-IN-RELATIVITY; then the per-pick '
     'renormalisation relat" = relat\'/sum_h share_h relat\'_h, which restores the reconciliation identity '
     'EXACTLY and therefore CANNOT move the all-in ladder, the pooled head H, or the numeraire s. The '
     'shrunk surface is then fed through the COMMITTED o30b_v0refit.py pipeline, LIFTED BY SOURCE TEXT AND '
     'EXEC\'D VERBATIM: weighted PAVA -> floor 100 -> the -1 ordering tiebreak -> one conservation scalar. '
     'Floor-100 tail, per-position monotonicity and EXACT conservation all survive; the per-pick '
     'reconciliation residual is PRINTED IN FULL, not absorbed.'),
    ('supersedes', 'nd_v0.monotone_refit_30b (ORDER 30B STEP 1) -- its output is the SHIPPED surface this '
                   'fix replaces; its pipeline is re-used verbatim on the shrunk input'),
    ('rule', OrderedDict([('K', K_SHRINK), ('K_source', 'DERIVE.json::pool.K -- the project\'s own K_SHRINK'),
                          ('n', 'o26b_loclin.kernel_loclin effective n, per position, per pick'),
                          ('target', 'the all-in relativity 1.0'),
                          ('renormalisation', 'per pick, against nd_v0.share'),
                          ('pipeline', 'o30b_v0refit.py stages 1-4, lifted by source text'),
                          ('pipeline_text_md5', hashlib.md5(_blk.encode()).hexdigest())])),
    ('construction', ['thin_sample_shrink_K15_toward_all_in_relativity', 'per_pick_renormalisation',
                      'weighted_pava_non_increasing', 'floor_100_lower_bound',
                      'minus_one_per_pick_ordering_tiebreak', 'one_conservation_scalar']),
    ('floor', FLOOR), ('lambda', LAM),
    ('conservation', OrderedDict([('target_sum_curve_1_64', CURVE_TOT),
                                  ('achieved_share_weighted_total', sw_fin),
                                  ('abs_drift', abs(sw_fin - CURVE_TOT)), ('verdict', 'EXACT')])),
    ('effective_n', {g: {str(p): effn[g][p] for p in PICKS} for g in POS}),
    ('hard_cohort_n', {g: {str(p): hard_n[(g, p)] for p in PICKS} for g in POS}),
    ('credibility_w', {g: {str(p): w[g][p] for p in PICKS} for g in POS}),
    ('ascents_after_total', 0),
    ('per_pick_reconciliation', {str(p): {'mix': resid[p]['mix'], 'curve': resid[p]['curve'],
                                          'ratio': resid[p]['ratio']} for p in PICKS}),
    ('per_pick_max_abs_ratio_minus_1', mxres), ('per_pick_max_at_pick', mx),
    ('head_pick1', {g: {'raw': posv_raw[g][1], 'shipped': shipped[g][1], 'head_fixed': fin[g][1],
                        'eff_n': effn[g][1]} for g in POS}),
    ('tiebreak_blocks', TB_LOG), ('join_shifts', JOIN_SHIFTS),
])

REPORT = dict(order='ORDER 31-F F1 -- the head fix', artifact_md5_in=got, K=K_SHRINK, lam=LAM,
              curve_total=CURVE_TOT, share_weighted_total_out=sw_fin,
              effective_n={g: {str(p): effn[g][p] for p in PICKS} for g in POS},
              credibility_w={g: {str(p): w[g][p] for p in PICKS} for g in POS},
              posv_raw={g: {str(p): posv_raw[g][p] for p in PICKS} for g in POS},
              posv_shipped={g: {str(p): shipped[g][p] for p in PICKS} for g in POS},
              posv_headfixed={g: {str(p): fin[g][p] for p in PICKS} for g in POS},
              per_pick_residual={str(p): resid[p]['ratio'] for p in PICKS},
              per_pick_max_abs_ratio_minus_1=mxres, per_pick_max_at=mx,
              head_moves=head_moves, pipeline_text_md5=hashlib.md5(_blk.encode()).hexdigest())
json.dump(REPORT, open(os.path.join(EVID, 'HEADFIX_31F.json'), 'w'), indent=1, sort_keys=True)

if WRITE:
    for g in J['nd_v0']['posv']:
        for k in J['nd_v0']['posv'][g]:
            J['nd_v0']['posv'][g][k] = fin[g][int(k)]
    J['nd_v0']['ascents'] = OrderedDict((g, []) for g in J['nd_v0']['ascents'])
    J['nd_v0']['head_shrink_31f'] = DOC
    J['nd_v0']['reconciliation'] = OrderedDict([
        ('identity', 'sum_g share_g(p) * posv_g(p) == curve(p)  for every pick 1..64'),
        ('status', 'SUPERSEDED AT THE PER-PICK LEVEL BY ORDER 31-F F1 -- see head_shrink_31f'),
        ('population_identity', 'sum over picks 1..64 IS exact (the conservation scalar)'),
        ('per_pick_max_abs_ratio_minus_1', mxres), ('at_pick', mx),
        ('prior_order30b_reading', {'max_abs_ratio_minus_1': 0.18531788138640548, 'at_pick': 63}),
        ('prior_order29_reading', {'max_abs_ratio_minus_1': 2.220446049250313e-16, 'at_pick': 1})])
    J['nd_v0']['ruck_floor_63_64'] = OrderedDict([
        ('_doc', 'RETIRED BY ORDER 30B STEP 1, RE-STAMPED BY ORDER 31-F F1.'),
        ('retired_by', 'ORDER 30B STEP 1'), ('posv_63', fin['RUCK'][63]), ('posv_64', fin['RUCK'][64])])
    with open(ART, 'w') as fh:
        json.dump(J, fh, indent=1)
    P('WROTE %s   new md5 %s' % (ART, md5f(ART)))
else:
    P('DRY RUN -- nothing written (pass --write to re-stamp the artifact)')

open(os.path.join(EVID, 'HEADFIX_31F_out.txt'), 'w').write('\n'.join(_OUT) + '\n')
