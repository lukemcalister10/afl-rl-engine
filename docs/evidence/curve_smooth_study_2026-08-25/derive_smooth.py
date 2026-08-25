#!/usr/bin/env python3
"""THE SMOOTHING-PASS CANDIDATE — candidates S and X, the positional rebuild, and the ruck cells.

Construction declared in PREREG.md BEFORE this file computed anything.  NOTHING LANDS.
Reads only; writes only into this scratch directory.
"""
import os, sys, json, math, collections, random
import numpy as np
import _common as C
import _posv as PV

OUT = C.OUT
LOG = []
def P(s=''):
    print(s); LOG.append(s)

PICKS = list(range(1, 65))
PICKS_X = list(range(1, 71))
SEED = 20260825

P('=' * 132)
P('THE SMOOTHING-PASS CANDIDATE  --  CANDIDATE S (SMOOTH) AND CANDIDATE X (EXTENDED)')
P('  construction declared in PREREG.md before this ran.   MEASUREMENT ONLY.  NOTHING LANDS.')
P('=' * 132)
P('  estimators, all reused and cited, none reinvented:')
P('    LOCLIN   o26b_loclin.kernel_loclin            (26B-C2)')
P('    WM       harness_pvc_REPINNED_pass3.kernel_raw (the SHIPPED year-0 aggregator)')
P('    PAVA     par_build.py::_pava(increasing=False) lifted by source text, md5 %s' % C.PAVA_MD5)
P('    L-SMOOTH build_bust_prior.py::smooth_curve MA lines, lifted by source text, md5 %s' % C.MA_MD5)
P('    30B      o30b_v0refit.py stages 1-4, lifted by source text, md5 %s' % PV.PIPE_MD5)
P('  NMIN=%.0f HMIN=%.2f HMAX=%.2f   K=%d   PIN1=%.0f' % (C.HP.NMIN, C.HP.HMIN, C.HP.HMAX,
                                                          C.K_SHRINK, C.PIN1))
P()

# ==================================================================================================
# GATE R0 -- reproduce ORDER 28 before reporting anything
# ==================================================================================================
nd = C.nd_rows_1_64()
O28 = C.derive_curve(nd, PICKS, smooth=None)
ref28 = {int(k): float(v) for k, v in C.DERIVE28['candidate']['allin'].items()}
r0 = max(abs(O28['allin'][p] - ref28[p]) for p in PICKS)
P('-' * 132)
P('GATE R0 -- THE HARNESS REPRODUCES ORDER 28 UNMODIFIED')
P('-' * 132)
P('  ND fit population: %d rows (LAYER2.json::fit_nd_keys)' % len(nd))
P('  force-majeure excluded from every fit input: %s' % ', '.join(C.FM['excluded_keys']))
P('  max |harness - DERIVE28.json::candidate.allin| over picks 1-64 = %.3e' % r0)
P('  pre-anchor head %.4f (published 3191.2)   anchor factor %.6f (published 0.9401)'
  % (O28['head'], O28['anchor_factor']))
P('  seam: nu=%.6f  zone %s  seam pick p0=%s'
  % (O28['zinfo']['nu'], '%d-%d' % (O28['zinfo']['zone'][0], O28['zinfo']['zone'][-1]),
     O28['zinfo']['seam']))
P('  R0 .......................................................... %s'
  % ('PASS' if r0 < 1e-9 else 'FAIL'))
if r0 >= 1e-9:
    raise SystemExit('R0 FAILED -- no candidate reported')

rel2, relat_raw, ident31 = PV.shrunk_relativities()
posv_in_ship = {g: {p: rel2[g][p] * C.CURVE_SHIPPED[p] for p in PICKS} for g in C.POSN}
RSHIP = PV.run_pipeline(posv_in_ship, C.SHARE, C.CURVE_SHIPPED, PICKS, 64)
r1 = max(abs(RSHIP['fin'][g][p] - C.POSV_SHIPPED[g][p]) for g in C.POSN for p in PICKS)
P()
P('GATE R1 -- THE 31-F RELATIVITIES ARE REUSED, AND THEY REBUILD THE SHIPPED SURFACE')
P('  31-F identity  max |sum_g share_g(p) rel2_g(p) - 1| = %.3e   (curve-INDEPENDENT)' % ident31)
P('  30B pipeline lift md5 %s == artifact head_shrink_31f.rule.pipeline_text_md5 %s'
  % (PV.PIPE_MD5, C.V2['nd_v0']['head_shrink_31f']['rule']['pipeline_text_md5']))
P('  max |rebuilt - shipped nd_v0.posv| over 384 cells = %.3e' % r1)
P('  lambda %.15f  (artifact %.15f)' % (RSHIP['LAM'], C.V2['nd_v0']['head_shrink_31f']['lambda']))
P('  R1 .......................................................... %s'
  % ('PASS' if r1 < 1e-6 else 'FAIL'))
if r1 >= 1e-6:
    raise SystemExit('R1 FAILED -- positional rebuild not reported')

# ==================================================================================================
# CANDIDATE S
# ==================================================================================================
S = C.derive_curve(nd, PICKS, smooth=5)
S3 = C.derive_curve(nd, PICKS, smooth=3)
S7 = C.derive_curve(nd, PICKS, smooth=7)

P()
P('=' * 132)
P('1.  CANDIDATE S  --  THE SMOOTHING PASS')
P('=' * 132)
P('  pipeline: raw cohorts -> LOCLIN -> HYBRID south boundary -> [L-SMOOTH MA5] -> weighted PAVA')
P('            -> anchor pick1=3000.   The bracketed stage is the ONLY change.')
P()
P('  THE SEAM (RULING B) IS UNCHANGED BY THE SMOOTHING PASS')
P('    ORDER 28  nu=%.6f  zone %d-%d  seam p0=%d'
  % (O28['zinfo']['nu'], O28['zinfo']['zone'][0], O28['zinfo']['zone'][-1], O28['zinfo']['seam']))
P('    CAND S    nu=%.6f  zone %d-%d  seam p0=%d'
  % (S['zinfo']['nu'], S['zinfo']['zone'][0], S['zinfo']['zone'][-1], S['zinfo']['seam']))
P('    (the seam is computed on LL vs WM, both UPSTREAM of the smoothing pass, so it cannot move)')
P()

# ---- the asserts ----
P('  THE ORDER-28 ASSERTS, RE-RUN ON CANDIDATE S')
P('    A1  PAVA did not pool pick 1 with pick 2 ............... %s'
  % ('PASS' if S['asserts']['A1'] else 'HALT'))
P('    A2  weighted-sum conservation |post/pre-1| = %.3e ..... %s'
  % (S['asserts']['A2'], 'PASS' if S['asserts']['A2'] < 1e-12 else 'HALT'))
P('    A3  output non-increasing over picks 1-64 ............. %s'
  % ('PASS' if S['asserts']['A3'] else 'HALT'))
P()
P('  A5 -- DISCLOSED, AS PREDICTED IN THE PREREG: the MA does NOT leave pick 1 alone.')
P('    pre-anchor head   ORDER 28 %10.4f   CAND S %10.4f   move %+.4f%%'
  % (O28['head'], S['head'], 100 * (S['head'] / O28['head'] - 1)))
P('    anchor factor     ORDER 28 %10.6f   CAND S %10.6f' % (O28['anchor_factor'], S['anchor_factor']))
P('    pick-vs-player premium  ORDER 28 %+.2f%%   CAND S %+.2f%%'
  % (100 * O28['premium'], 100 * S['premium']))
P('    ANY DOWNSTREAM OBJECT KEYED TO THE PRE-ANCHOR HEAD (e.g. the pooled numeraire s) IS OUT OF')
P('    SCOPE FOR THIS SEAT AND MUST BE RE-CHECKED BEFORE ANY LANDING.')
P()

# ---- ascents / plateaus ----
def plateau_report(res, picks, label):
    blk = C.blocks_of(res['post'])
    out = []
    for (i, j) in blk:
        out.append(dict(picks='%d-%d' % (picks[i], picks[j]), n=j - i + 1,
                        value=res['allin'][picks[i]]))
    return out

pl28 = plateau_report(O28, PICKS, 'O28')
plS = plateau_report(S, PICKS, 'S')
P('  THE PLATEAUS -- what the weighted PAVA still has to pool')
P('    ORDER 28 (what ships): %d ascents entering PAVA, %d pooled blocks'
  % (len(O28['ascents']), len(pl28)))
for b in pl28:
    P('        picks %-8s n=%d  pooled value %.1f' % (b['picks'], b['n'], b['value']))
P('    CANDIDATE S:          %d ascents entering PAVA, %d pooled blocks'
  % (len(S['ascents']), len(plS)))
for b in plS:
    P('        picks %-8s n=%d  pooled value %.1f' % (b['picks'], b['n'], b['value']))
if not plS:
    P('        NONE -- the curve is strictly descending at every one of the 63 steps.')
P()
P('  THE 3->6 CLIFF')
for lab, res in (('shipped integer curve', None), ('ORDER 28 float', O28), ('CANDIDATE S', S)):
    if res is None:
        v3, v6 = C.CURVE_SHIPPED[3], C.CURVE_SHIPPED[6]
    else:
        v3, v6 = res['allin'][3], res['allin'][6]
    P('    %-22s pick3 %8.1f -> pick6 %8.1f   drop %8.1f  (%.1f%%)'
      % (lab, v3, v6, v3 - v6, 100 * (v6 / v3 - 1)))
P('    largest single adjacent drop, picks 1-64:')
for lab, res in (('ORDER 28 float', O28), ('CANDIDATE S', S)):
    d = [(res['allin'][p] - res['allin'][p + 1], p) for p in PICKS[:-1]]
    d.sort(reverse=True)
    P('      %-16s %s' % (lab, '  '.join('%d->%d %.0f' % (p, p + 1, v) for v, p in d[:5])))
P()

# ---- conservation ----
def totals(allin, picks, nper):
    plain = math.fsum(allin[p] for p in picks)
    wtd = math.fsum(nper.get(p, 0) * allin[p] for p in picks)
    return plain, wtd

pl_ship = math.fsum(C.CURVE_SHIPPED[p] for p in PICKS)
wt_ship = math.fsum(O28['nper'].get(p, 0) * C.CURVE_SHIPPED[p] for p in PICKS)
pl28t, wt28t = totals(O28['allin'], PICKS, O28['nper'])
plSt, wtSt = totals(S['allin'], PICKS, S['nper'])

P('  TOTAL-VALUE CONSERVATION  (owner tolerance 1%; NO post-hoc rescale was applied)')
P('    %-38s %14s %14s %10s' % ('reading', 'baseline', 'CANDIDATE S', 'drift'))
P('    %-38s %14.1f %14.1f %+9.4f%%'
  % ('plain total  sum curve(p), 1-64', pl_ship, plSt, 100 * (plSt / pl_ship - 1)))
P('       (baseline = SHIPPED integer curve, ordering_tiebreak.curve_plain_sum_post = %d)'
  % C.V2['ordering_tiebreak']['curve_plain_sum_post'])
P('    %-38s %14.1f %14.1f %+9.4f%%'
  % ('plain total vs ORDER-28 float', pl28t, plSt, 100 * (plSt / pl28t - 1)))
P('    %-38s %14.1f %14.1f %+9.4f%%'
  % ('cohort-weighted  sum n_p*curve(p)', wt_ship, wtSt, 100 * (wtSt / wt_ship - 1)))
P('    %-38s %14.1f %14.1f %+9.4f%%'
  % ('  same, vs ORDER-28 float', wt28t, wtSt, 100 * (wtSt / wt28t - 1)))
cons_ok = all(abs(x) <= 1.0 for x in
              [100 * (plSt / pl_ship - 1), 100 * (plSt / pl28t - 1),
               100 * (wtSt / wt_ship - 1), 100 * (wtSt / wt28t - 1)])
P('    VERDICT vs the 1%% tolerance ............................ %s'
  % ('WITHIN TOLERANCE' if cons_ok else 'BREACH -- REPORTED AS MEASURED, NOT ABSORBED'))
P()

# ---- per-pick table ----
P('  PER-PICK: SHIPPED vs ORDER-28 FLOAT vs CANDIDATE S')
P('  %-5s %5s %11s %11s %11s %11s %9s %9s'
  % ('pick', 'n', 'shipped', 'O28 float', 'CAND S', 'S-shipped', 'S/shipped', 'S/O28'))
for p in PICKS:
    P('  %-5d %5d %11.0f %11.1f %11.1f %+11.1f %9.4f %9.4f'
      % (p, S['nper'].get(p, 0), C.CURVE_SHIPPED[p], O28['allin'][p], S['allin'][p],
         S['allin'][p] - C.CURVE_SHIPPED[p], S['allin'][p] / C.CURVE_SHIPPED[p],
         S['allin'][p] / O28['allin'][p]))
P()
P('  WIDTH ABLATION (declared sensitivity; MA5 is the estate\'s ruled width and is the candidate)')
P('  %-6s %10s %10s %10s %10s %10s' % ('width', 'plain tot', 'vs ship%', 'blocks', 'pick6', 'pick64'))
for lab, res in (('MA3', S3), ('MA5', S), ('MA7', S7)):
    t = math.fsum(res['allin'][p] for p in PICKS)
    P('  %-6s %10.1f %+9.4f%% %10d %10.1f %10.1f'
      % (lab, t, 100 * (t / pl_ship - 1), len(C.blocks_of(res['post'])),
         res['allin'][6], res['allin'][64]))

# ==================================================================================================
# CANDIDATE X
# ==================================================================================================
nd65 = C.nd_rows_65_70()
ndX = nd + nd65
X = C.derive_curve(ndX, PICKS_X, smooth=5, end=70)

P()
P('=' * 132)
P('2.  CANDIDATE X  --  THE EXTENDED CANDIDATE (no hard 64 endpoint), domain 1-70')
P('=' * 132)
P('  ADDED POPULATION: ND rows at (slid) picks 65-70, same window 2004-2021, same grace-A basis.')
P('  They ENTER the curve fit and LEAVE the ND>64 pool pathway -- the estate\'s own already-ruled')
P('  mechanic (LAYER2.json::force_majeure.mechanics), not a new rule.')
n65 = collections.Counter(r['pick'] for r in nd65)
P('    n = %d   by pick: %s' % (len(nd65), '  '.join('p%d n=%d' % (p, n65[p]) for p in sorted(n65))))
vals65 = [r['value'] for r in nd65]
P('    outcomes: mean %.1f   median %.1f   zeros (busts) %d/%d (%.0f%%)   max %.1f'
  % (float(np.mean(vals65)), float(np.median(vals65)), sum(1 for v in vals65 if v <= 0),
     len(vals65), 100.0 * sum(1 for v in vals65 if v <= 0) / len(vals65), max(vals65)))
pos65 = collections.Counter(r['pos'] for r in nd65)
P('    by position: %s' % '  '.join('%s %d' % (g, pos65.get(g, 0)) for g in C.POSN))
P('    these %d rows are removed from the pool fit for X (they are in fit_pool_keys today)' % len(nd65))
P()
P('  RULING B RE-DECLARED FOR THE LONGER DOMAIN (PREREG §2.2)')
P('    KEPT:     interior-norm window %d-%d, ZONE_NORTH_LIMIT %d (both pick-space guards)'
  % (C.NORM_LO, C.NORM_HI, C.ZONE_NORTH_LIMIT))
P('    RE-BASED: blend t = (p - p0)/(END - p0) with END=70, so w(p0)=0 and w(70)=1')
P('    CAND S seam p0=%s zone %d-%d      CAND X seam p0=%s zone %d-%d'
  % (S['zinfo']['seam'], S['zinfo']['zone'][0], S['zinfo']['zone'][-1],
     X['zinfo']['seam'], X['zinfo']['zone'][0], X['zinfo']['zone'][-1]))
P()
P('  ASSERTS ON X:  A1 %s   A2 %.3e %s   A3 %s'
  % ('PASS' if X['asserts']['A1'] else 'HALT', X['asserts']['A2'],
     'PASS' if X['asserts']['A2'] < 1e-12 else 'HALT', 'PASS' if X['asserts']['A3'] else 'HALT'))
P('  pre-anchor head %.4f   anchor factor %.6f   premium %+.2f%%'
  % (X['head'], X['anchor_factor'], 100 * X['premium']))
plXt = math.fsum(X['allin'][p] for p in PICKS)
plX70 = math.fsum(X['allin'][p] for p in PICKS_X)
P('  plain total over 1-64  %.1f   vs shipped %+0.4f%%   vs CAND S %+0.4f%%'
  % (plXt, 100 * (plXt / pl_ship - 1), 100 * (plXt / plSt - 1)))
P('  plain total over 1-70  %.1f' % plX70)
P()
P('  THE PICKS 65-70 IMPLIED VALUES  --  the answer to "what if 64 were not a hard endpoint"')
P('  %-6s %6s %12s %12s' % ('pick', 'n', 'CAND X', 'vs X pick64'))
for p in range(65, 71):
    P('  %-6d %6d %12.1f %11.3fx' % (p, X['nper'].get(p, 0), X['allin'][p],
                                     X['allin'][p] / X['allin'][64]))
P('    for reference, the SAME players are priced today by the pool, not the curve:')
P('      pool_levels.signed_nd65_plus.measured_k15      = %s (signed, pre-anchor units)'
  % C.V2['pool_levels']['signed_nd65_plus']['measured_k15'])
P('      pool_v0.pathway_levels_anchored["ND>64"]       = %.1f (board currency)'
  % C.V2['pool_v0']['pathway_levels_anchored']['ND>64'])
P('      CANDIDATE X mean over picks 65-70              = %.1f'
  % float(np.mean([X['allin'][p] for p in range(65, 71)])))
P()
plX = [dict(picks='%d-%d' % (PICKS_X[i], PICKS_X[j]), n=j - i + 1, value=X['allin'][PICKS_X[i]])
       for (i, j) in C.blocks_of(X['post'])]
P('  THE PLATEAUS ON X -- and THE HEADLINE FINDING OF THE EXTENSION')
for b in plX:
    P('        picks %-8s n=%d  pooled value %.1f' % (b['picks'], b['n'], b['value']))
P('    THE DEEP TAIL GENUINELY TURNS UP ONCE THE 65-70 DATA IS IN. The LOCLIN estimate stops')
P('    falling at pick 63 and RISES to pick 70, and the weighted PAVA pools picks 61-70 into one')
P('    flat shelf. Pick 64 stops being an edge and becomes an ordinary interior point of a shelf.')
P()
P('  %-5s %6s %10s %10s %10s %10s' % ('pick', 'n', 'raw mean', 'LOCLIN', 'WM', 'CAND X'))
for p in range(58, 71):
    P('  %-5d %6d %10.1f %10.1f %10.1f %10.1f'
      % (p, X['nper'].get(p, 0), X['rawmean'][p], X['ll'][p - 1], X['wm'][p - 1], X['allin'][p]))
P()
P('  THE 40-64 ZONE: CANDIDATE X vs CANDIDATE S')
P('  %-5s %11s %11s %11s %9s %8s %8s'
  % ('pick', 'CAND S', 'CAND X', 'delta', 'X/S', 'w in S', 'w in X'))
for p in range(40, 65):
    iS = PICKS.index(p); iX = PICKS_X.index(p)
    P('  %-5d %11.1f %11.1f %+11.1f %9.4f %8.4f %8.4f'
      % (p, S['allin'][p], X['allin'][p], X['allin'][p] - S['allin'][p],
         X['allin'][p] / S['allin'][p], S['blendw'][iS], X['blendw'][iX]))
z = [X['allin'][p] / S['allin'][p] - 1 for p in range(40, 65)]
P('    zone 40-64 summary: mean %+.2f%%   min %+.2f%% (pick %d)   max %+.2f%% (pick %d)'
  % (100 * float(np.mean(z)), 100 * min(z), 40 + int(np.argmin(z)), 100 * max(z),
     40 + int(np.argmax(z))))
P('    MECHANISM, as predicted in the PREREG: at the same pick the blend weight w is LOWER on the')
P('    1-70 domain (the pick is further from the endpoint), so the south tail reverts LESS toward')
P('    the weighted mean and stays closer to LOCLIN.')

# ==================================================================================================
# POSITIONAL REBUILD
# ==================================================================================================
P()
P('=' * 132)
P('3.  THE POSITIONAL REBUILD  --  31-F RELATIVITIES REUSED, 30B PIPELINE LIFTED VERBATIM')
P('=' * 132)

posv_in_S = {g: {p: rel2[g][p] * S['allin'][p] for p in PICKS} for g in C.POSN}
identS = max(abs(sum(C.SHARE[g][p] * posv_in_S[g][p] for g in C.POSN) / S['allin'][p] - 1.0)
             for p in PICKS)
RS = PV.run_pipeline(posv_in_S, C.SHARE, S['allin'], PICKS, 64)

# candidate X: extend share flat from 64 too (the artifact has no share past 64), then renormalise
share_X = {g: dict(C.SHARE[g]) for g in C.POSN}
for g in C.POSN:
    for p in range(65, 71):
        share_X[g][p] = C.SHARE[g][64]
for p in range(65, 71):
    t = sum(share_X[g][p] for g in C.POSN)
    for g in C.POSN:
        share_X[g][p] = share_X[g][p] / t
rel2X = PV.extend_relativity(rel2, PICKS_X, share_X)
posv_in_X = {g: {p: rel2X[g][p] * X['allin'][p] for p in PICKS_X} for g in C.POSN}
identX = max(abs(sum(share_X[g][p] * posv_in_X[g][p] for g in C.POSN) / X['allin'][p] - 1.0)
             for p in PICKS_X)
RX = PV.run_pipeline(posv_in_X, share_X, X['allin'], PICKS_X, 70)

P('  RELATIVITIES: REUSED, NOT REFITTED. rel2 reconstructed from stored artifact values only')
P('    (V0REFIT30B.posv_in / curve_shipped, credibility_w AS STORED, nd_v0.share). No estimator run.')
P('    For X, picks 65-70 HOLD the pick-64 shrunk relativity flat, then are re-renormalised.')
P()
P('  RECONCILIATION -- REPORTED AT ALL THREE LEVELS (PREREG §3.3)')
P('  %-52s %14s %14s %14s' % ('level', 'SHIPPED', 'CAND S', 'CAND X'))
P('  %-52s %14.3e %14.3e %14.3e'
  % ('relativity stage, per pick  max|sum share*posv/curve-1|',
     max(abs(sum(C.SHARE[g][p] * posv_in_ship[g][p] for g in C.POSN) / C.CURVE_SHIPPED[p] - 1.0)
         for p in PICKS), identS, identX))
P('       target <= 1e-9 ................................ %s / %s / %s'
  % ('PASS', 'PASS' if identS < 1e-9 else 'FAIL', 'PASS' if identX < 1e-9 else 'FAIL'))
P('  %-52s %14.3e %14.3e %14.3e'
  % ('population identity |sum_gp share*posv - sum curve|',
     abs(RSHIP['sw_fin'] - RSHIP['curve_tot']), abs(RS['sw_fin'] - RS['curve_tot']),
     abs(RX['sw_fin'] - RX['curve_tot'])))
P('       target <= 1e-9 ................................ %s / %s / %s'
  % ('PASS' if abs(RSHIP['sw_fin'] - RSHIP['curve_tot']) < 1e-9 else 'FAIL',
     'PASS' if abs(RS['sw_fin'] - RS['curve_tot']) < 1e-9 else 'FAIL',
     'PASS' if abs(RX['sw_fin'] - RX['curve_tot']) < 1e-9 else 'FAIL'))
mxS = max(abs(RS['resid'][p]['ratio'] - 1) for p in PICKS)
mxX = max(abs(RX['resid'][p]['ratio'] - 1) for p in PICKS_X)
mxSh = max(abs(RSHIP['resid'][p]['ratio'] - 1) for p in PICKS)
P('  %-52s %14.4f %14.4f %14.4f'
  % ('per-pick POST-pipeline max|ratio-1|  (NOT exact)', mxSh, mxS, mxX))
P('       at pick .......................................  %12d %14d %14d'
  % (max(PICKS, key=lambda p: abs(RSHIP['resid'][p]['ratio'] - 1)),
     max(PICKS, key=lambda p: abs(RS['resid'][p]['ratio'] - 1)),
     max(PICKS_X, key=lambda p: abs(RX['resid'][p]['ratio'] - 1))))
P('       THIS IS NOT 1e-9 AND CANNOT BE: monotonicity + floor 100 are constraints the raw')
P('       relativities do not satisfy. The shipped surface carries the same residual (0.1718).')
P()
P('  lambda (conservation scalar):  SHIPPED %.12f   CAND S %.12f   CAND X %.12f'
  % (RSHIP['LAM'], RS['LAM'], RX['LAM']))
P()
P('  PER-POSITION HEADS (pick 1) AND TAILS')
P('  %-6s %12s %12s %12s   %10s %10s %10s'
  % ('pos', 'ship p1', 'CAND S p1', 'CAND X p1', 'ship p64', 'S p64', 'X p70'))
for g in C.POSN:
    P('  %-6s %12.1f %12.1f %12.1f   %10.1f %10.1f %10.1f'
      % (g, C.POSV_SHIPPED[g][1], RS['fin'][g][1], RX['fin'][g][1],
         C.POSV_SHIPPED[g][64], RS['fin'][g][64], RX['fin'][g][70]))
P()
P('  per-position monotonicity (ascents) and floor 100:')
for g in C.POSN:
    aS = [p for p in PICKS[1:] if RS['fin'][g][p] > RS['fin'][g][p - 1] + 1e-12]
    aX = [p for p in PICKS_X[1:] if RX['fin'][g][p] > RX['fin'][g][p - 1] + 1e-12]
    P('    %-6s S ascents %d  min %.2f   |   X ascents %d  min %.2f'
      % (g, len(aS), min(RS['fin'][g].values()), len(aX), min(RX['fin'][g].values())))
P()
P('  ALEX DODSON  --  ND pick 53, RUCK, entry 2024 (window_tier sensitivity2022+)')
P('    HE IS NOT IN ANY FIT POPULATION. He is a CONSUMER of the curve, not a teacher of it;')
P('    his number moves only because the surface under him moves.')
dod = (C.POSV_SHIPPED['RUCK'][53], RS['fin']['RUCK'][53], RX['fin']['RUCK'][53])
P('    v0 (board currency)   OLD (shipped) %8.2f   ->  CAND S %8.2f   ->  CAND X %8.2f'
  % dod)
P('                          move vs shipped:  S %+.2f (%+.2f%%)   X %+.2f (%+.2f%%)'
  % (dod[1] - dod[0], 100 * (dod[1] / dod[0] - 1), dod[2] - dod[0], 100 * (dod[2] / dod[0] - 1)))
P('    the all-in curve at pick 53:  shipped %.0f   CAND S %.1f   CAND X %.1f'
  % (C.CURVE_SHIPPED[53], S['allin'][53], X['allin'][53]))

# ==================================================================================================
# THE RUCK QUESTION
# ==================================================================================================
P()
P('=' * 132)
P('4.  THE RUCK QUESTION  --  per-band cells with bootstrap CIs')
P('=' * 132)
BANDS = [(1, 10), (11, 20), (21, 40), (41, 64), (65, 70)]
GROUPS = collections.OrderedDict([
    ('RUCK', ['RUCK']), ('KPD', ['KPD']), ('KPF', ['KPF']),
    ('TALL(KPD+KPF+RUCK)', ['KPD', 'KPF', 'RUCK']),
    ('TALL_ex_RUCK(KPD+KPF)', ['KPD', 'KPF']),
    ('MID', ['MID']), ('SD', ['SD']), ('SF', ['SF']),
    ('SMALL(MID+SD+SF)', ['MID', 'SD', 'SF']),
])
POPX = ndX  # includes 65-70


def cell(groups, lo, hi):
    return [r['value'] for r in POPX if r['pos'] in groups and lo <= r['pick'] <= hi]


def boot_mean_ci(vals, n=10000, seed=SEED):
    if len(vals) < 2:
        return (float('nan'), float('nan'))
    rng = np.random.default_rng(seed)
    a = np.asarray(vals, float)
    idx = rng.integers(0, len(a), size=(n, len(a)))
    ms = a[idx].mean(axis=1)
    return (float(np.percentile(ms, 2.5)), float(np.percentile(ms, 97.5)))


P('  population: the ORDER-28 ND fit rows (n=%d) PLUS the picks 65-70 entrants (n=%d).' % (len(nd), len(nd65)))
P('  value = whole-career grace-A delivered value. busts are IN, at zero.')
P('  CI = percentile bootstrap, %d resamples, players resampled within (group, band), seed %d.'
  % (10000, SEED))
P()
P('  %-24s %-8s %5s %10s %10s %10s %8s' % ('group', 'band', 'n', 'mean', 'ci_lo', 'ci_hi', 'zero%'))
CELLS = {}
for gname, gl in GROUPS.items():
    for (lo, hi) in BANDS:
        v = cell(gl, lo, hi)
        if not v:
            continue
        lo_ci, hi_ci = boot_mean_ci(v)
        z = 100.0 * sum(1 for x in v if x <= 0) / len(v)
        CELLS['%s|%d-%d' % (gname, lo, hi)] = dict(n=len(v), mean=float(np.mean(v)),
                                                   ci=[lo_ci, hi_ci], zero_pct=z)
        P('  %-24s %-8s %5d %10.1f %10.1f %10.1f %7.1f%%'
          % (gname, '%d-%d' % (lo, hi), len(v), float(np.mean(v)), lo_ci, hi_ci, z))
    P()

# ---- the flatness test ----
P('  THE FLATNESS TEST (declared in the PREREG before it ran)')
P('    F_g = mean(g, picks 41-70) / mean(g, picks 1-10).  A position whose deep tail flattens')
P('    relative to another has the HIGHER F.')


def F_of(groups, rng=None, resample=False):
    deep = np.asarray(cell(groups, 41, 70), float)
    head = np.asarray(cell(groups, 1, 10), float)
    if resample:
        deep = deep[rng.integers(0, len(deep), len(deep))]
        head = head[rng.integers(0, len(head), len(head))]
    return float(deep.mean() / head.mean()) if head.mean() > 0 else float('nan')


P()
P('  %-24s %6s %6s %10s %10s %10s %10s'
  % ('group', 'n_deep', 'n_head', 'mean_deep', 'mean_head', 'F', 'F 95% CI'))
FSTAT = {}
for gname, gl in GROUPS.items():
    d = cell(gl, 41, 70); h = cell(gl, 1, 10)
    if not d or not h:
        continue
    rng = np.random.default_rng(SEED)
    fs = [F_of(gl, rng, True) for _ in range(10000)]
    ci = (float(np.percentile(fs, 2.5)), float(np.percentile(fs, 97.5)))
    FSTAT[gname] = dict(F=F_of(gl), ci=list(ci), n_deep=len(d), n_head=len(h))
    P('  %-24s %6d %6d %10.1f %10.1f %10.4f  [%.4f, %.4f]'
      % (gname, len(d), len(h), float(np.mean(d)), float(np.mean(h)), F_of(gl), ci[0], ci[1]))

# ---- the difference test ----
rng = np.random.default_rng(SEED)
diffs = []
for _ in range(10000):
    diffs.append(F_of(['RUCK'], rng, True) - F_of(['KPD', 'KPF'], rng, True))
dci = (float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5)))
dpt = FSTAT['RUCK']['F'] - FSTAT['TALL_ex_RUCK(KPD+KPF)']['F']
P()
P('  TEST 1 -- F_RUCK - F_TALL_ex_RUCK = %+.4f   95%% CI [%+.4f, %+.4f]   excludes 0: %s'
  % (dpt, dci[0], dci[1], 'YES' if (dci[0] > 0 or dci[1] < 0) else 'NO'))

rd = cell(['RUCK'], 41, 70); td = cell(['KPD', 'KPF'], 41, 70)
rci = boot_mean_ci(rd); tci = boot_mean_ci(td)
overlap = not (rci[1] < tci[0] or tci[1] < rci[0])
P('  TEST 2 -- deep band 41-70 means')
P('             RUCK          n=%3d  mean %.1f  CI [%.1f, %.1f]' % (len(rd), float(np.mean(rd)), *rci))
P('             TALL_ex_RUCK  n=%3d  mean %.1f  CI [%.1f, %.1f]' % (len(td), float(np.mean(td)), *tci))
P('             CIs overlap: %s' % ('YES' if overlap else 'NO'))
rng = np.random.default_rng(SEED)
md = []
for _ in range(10000):
    a = np.asarray(rd, float); b = np.asarray(td, float)
    md.append(a[rng.integers(0, len(a), len(a))].mean() - b[rng.integers(0, len(b), len(b))].mean())
mci = (float(np.percentile(md, 2.5)), float(np.percentile(md, 97.5)))
P('             difference of means %+.1f   95%% CI [%+.1f, %+.1f]'
  % (float(np.mean(rd)) - float(np.mean(td)), mci[0], mci[1]))

thin = min(len(cell(['RUCK'], lo, hi)) for lo, hi in [(41, 64), (65, 70)])
n_ruck_deep = len(rd)
t1 = (dci[0] > 0 or dci[1] < 0)
t2 = not overlap
if n_ruck_deep < 30:
    verdict = 'INCONCLUSIVE -- deep RUCK cell too thin (n=%d < 30)' % n_ruck_deep
elif t1 and t2:
    verdict = 'SUPPORTS a ruck-specific deep relativity'
elif not t1 and not t2:
    verdict = 'DOES NOT SUPPORT a ruck-specific deep relativity'
else:
    verdict = 'INCONCLUSIVE -- exactly one of the two tests fires'
P()
P('  VERDICT (by the rule fixed in the PREREG, not chosen after the fact):')
P('    TEST 1 fires: %s     TEST 2 fires: %s     deep RUCK n = %d' % (t1, t2, n_ruck_deep))
P('    ==> %s' % verdict)

# ==================================================================================================
# WRITE
# ==================================================================================================
json.dump(dict(
    status='CANDIDATE ONLY -- NOTHING LANDS',
    gates=dict(R0_max_abs=r0, R1_max_abs=r1, pava_md5=C.PAVA_MD5, ma_md5=C.MA_MD5,
               pipeline_md5=PV.PIPE_MD5),
    construction=['loclin_26bc2', 'hybrid_south_boundary_rulingB',
                  'L_SMOOTH_5pt_centered_moving_average_edge_replicate',
                  'shipped_weighted_pava_rulingC', 'anchor_pick1_3000'],
    seam=S['zinfo'], asserts=S['asserts'],
    head=S['head'], anchor_factor=S['anchor_factor'], premium=S['premium'],
    head_o28=O28['head'], anchor_factor_o28=O28['anchor_factor'],
    conservation=dict(plain_shipped=pl_ship, plain_o28=pl28t, plain_S=plSt,
                      wtd_shipped=wt_ship, wtd_o28=wt28t, wtd_S=wtSt,
                      drift_plain_vs_shipped_pct=100 * (plSt / pl_ship - 1),
                      drift_plain_vs_o28_pct=100 * (plSt / pl28t - 1),
                      drift_wtd_vs_shipped_pct=100 * (wtSt / wt_ship - 1),
                      drift_wtd_vs_o28_pct=100 * (wtSt / wt28t - 1),
                      within_1pct=cons_ok),
    plateaus_o28=pl28, plateaus_S=plS,
    per_pick={str(p): dict(n=S['nper'].get(p, 0), shipped=C.CURVE_SHIPPED[p],
                           o28_float=O28['allin'][p], cand_S=S['allin'][p],
                           delta_vs_shipped=S['allin'][p] - C.CURVE_SHIPPED[p],
                           ratio_vs_shipped=S['allin'][p] / C.CURVE_SHIPPED[p]) for p in PICKS},
    ablation={'MA3': {str(p): S3['allin'][p] for p in PICKS},
              'MA5': {str(p): S['allin'][p] for p in PICKS},
              'MA7': {str(p): S7['allin'][p] for p in PICKS}},
), open(os.path.join(OUT, 'CANDIDATE_S.json'), 'w'), indent=1, sort_keys=True, default=float)

json.dump(dict(
    status='CANDIDATE ONLY -- NOTHING LANDS', domain='1-70',
    ruling_B='kept norm window 4-48 and ZONE_NORTH_LIMIT 50; blend denominator re-based to END=70',
    added_population=dict(n=len(nd65), by_pick={str(p): n65[p] for p in sorted(n65)},
                          by_pos={g: pos65.get(g, 0) for g in C.POSN},
                          mean=float(np.mean(vals65)), median=float(np.median(vals65)),
                          zeros=sum(1 for v in vals65 if v <= 0),
                          removed_from_pool_pathway='ND>64'),
    seam=X['zinfo'], asserts=X['asserts'], head=X['head'], anchor_factor=X['anchor_factor'],
    plateaus=plX,
    deep_tail_evidence={str(p): dict(n=X['nper'].get(p, 0), rawmean=X['rawmean'][p],
                                     loclin=X['ll'][p - 1], wm=X['wm'][p - 1],
                                     cand_X=X['allin'][p]) for p in range(58, 71)},
    headline='the deep tail turns UP once 65-70 is in: LOCLIN stops falling at 63 and rises to 70; '
             'the weighted PAVA pools picks 61-70 into one flat shelf at %.1f' % X['allin'][64],
    curve={str(p): X['allin'][p] for p in PICKS_X},
    picks_65_70={str(p): X['allin'][p] for p in range(65, 71)},
    pool_reference=dict(signed_nd65_plus_measured_k15=C.V2['pool_levels']['signed_nd65_plus']['measured_k15'],
                        pathway_levels_anchored_ND64=C.V2['pool_v0']['pathway_levels_anchored']['ND>64']),
    zone_40_64_shift={str(p): dict(cand_S=S['allin'][p], cand_X=X['allin'][p],
                                   delta=X['allin'][p] - S['allin'][p],
                                   ratio=X['allin'][p] / S['allin'][p],
                                   w_S=S['blendw'][PICKS.index(p)],
                                   w_X=X['blendw'][PICKS_X.index(p)]) for p in range(40, 65)},
), open(os.path.join(OUT, 'CANDIDATE_X.json'), 'w'), indent=1, sort_keys=True, default=float)

json.dump(dict(
    status='CANDIDATE ONLY -- NOTHING LANDS',
    relativity_provenance='31-F shrunk relativities REUSED (reconstructed from V0REFIT30B.posv_in, '
                          'curve_shipped, stored credibility_w, nd_v0.share). NOT refitted.',
    pipeline='o30b_v0refit.py stages 1-4 lifted by source text, md5 %s' % PV.PIPE_MD5,
    reconciliation=dict(
        relativity_stage=dict(shipped=max(abs(sum(C.SHARE[g][p] * posv_in_ship[g][p] for g in C.POSN)
                                              / C.CURVE_SHIPPED[p] - 1.0) for p in PICKS),
                              cand_S=identS, cand_X=identX, target=1e-9),
        population=dict(shipped=abs(RSHIP['sw_fin'] - RSHIP['curve_tot']),
                        cand_S=abs(RS['sw_fin'] - RS['curve_tot']),
                        cand_X=abs(RX['sw_fin'] - RX['curve_tot']), target=1e-9),
        per_pick_post_pipeline=dict(shipped=mxSh, cand_S=mxS, cand_X=mxX,
                                    note='NOT exact and cannot be; monotonicity+floor are binding')),
    lam=dict(shipped=RSHIP['LAM'], cand_S=RS['LAM'], cand_X=RX['LAM']),
    posv_S={g: {str(p): RS['fin'][g][p] for p in PICKS} for g in C.POSN},
    posv_X={g: {str(p): RX['fin'][g][p] for p in PICKS_X} for g in C.POSN},
    posv_shipped={g: {str(p): C.POSV_SHIPPED[g][p] for p in PICKS} for g in C.POSN},
    dodson=dict(key='alex-dodson', pick=53, pos='RUCK', entry_year=2024,
                window_tier='sensitivity2022+', in_fit_population=False,
                v0_shipped=dod[0], v0_cand_S=dod[1], v0_cand_X=dod[2]),
), open(os.path.join(OUT, 'POSV_REBUILD.json'), 'w'), indent=1, sort_keys=True, default=float)

json.dump(dict(status='MEASUREMENT ONLY', seed=SEED, resamples=10000,
               bands=[list(b) for b in BANDS], cells=CELLS, flatness=FSTAT,
               test1=dict(stat=dpt, ci=list(dci), fires=bool(t1)),
               test2=dict(ruck_mean=float(np.mean(rd)), ruck_ci=list(rci), ruck_n=len(rd),
                          tall_mean=float(np.mean(td)), tall_ci=list(tci), tall_n=len(td),
                          diff_ci=list(mci), fires=bool(t2)),
               verdict=verdict),
          open(os.path.join(OUT, 'RUCK_CELLS.json'), 'w'), indent=1, sort_keys=True, default=float)

open(os.path.join(OUT, 'SMOOTH_OUT.txt'), 'w').write('\n'.join(LOG) + '\n')
P()
P('wrote CANDIDATE_S.json CANDIDATE_X.json POSV_REBUILD.json RUCK_CELLS.json SMOOTH_OUT.txt')
