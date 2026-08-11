"""ORDER 4 STEP 1 — THE DISCRIMINATING HONESTY TEST. Measurement only; wires nothing.

Tests the suspicion that exposure-weighting the par sample is survivor bias by another door. The
decision rule was fixed in PREREG_ORDER4.md BEFORE this grid was computed.

Four estimators on the IDENTICAL par-cohort row set that par_build.gather() collects:
  (i)   as-built      every ever-establisher's played season (g>=1), EQUAL weight
  (ii)  exposure      the SAME sample, weight min(g,18)                -- nothing dropped
  (iii) survivors     seasons with g>=6, EQUAL weight                  -- the pre-#336 sample
  (iv)  discriminator seasons with g>=6, weight min(g,18)              -- isolates the added rows
"""
import sys, os, json, collections
sys.path.insert(0, '/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
sys.path.insert(0, '/home/user/afl-rl-engine/engine/forward_valuation')
import numpy as np
import engine_load
g_ = engine_load.load()
MA = g_['MA']
import importlib
pb = importlib.import_module('par_build'); CP = pb.CP

CAP = 18.0
pool = [p for p in MA.data if MA.GRP.get(p.get('pos'))
        and (p.get('pick') or p.get('_ft')) and pb.DRAFT_LO <= pb.draftyr(p) <= pb.DRAFT_HI]
rows = []   # (band, T, games, lvl, tw, established)
for p in pool:
    pk = min(MA.effpk(p), CP.KMAX); d0 = pb.draftyr(p); b = MA.bandof(MA.effpk(p))
    est = pb._ever_established_338(p)
    for T in range(1, pb.TEN_MAX + 1):
        Y = d0 + T; r = pb.season_row(p, Y); gm = r['games'] if r else 0
        if gm <= 0: continue
        if pb.season_pos(r) is None: continue
        sr = CP._season_rows(p, Y)
        tw = sum(gg * CP._swt(yr, Y) for yr, gg, _ in sr)
        rows.append((b, T, float(gm), float(CP._lvl_wt(p, Y)), float(tw), est))
print(f"par-cohort played observations: {len(rows)}   ever-establisher rows: {sum(1 for r in rows if r[5])}")

def est(sel, wfn):
    v = [(r[3], wfn(r)) for r in rows if sel(r)]
    if not v: return None, 0, 0.0
    W = sum(x[1] for x in v)
    return (sum(x[0]*x[1] for x in v)/W if W > 0 else None), len(v), W

S_I   = lambda r: r[5] and r[2] >= 1        # as-built sample
S_III = lambda r: r[2] >= 6                 # survivors sample
W_EQ  = lambda r: 1.0
W_EXP = lambda r: min(r[2], CAP)
W_UNC = lambda r: r[2]                      # uncapped, so the cap is not doing hidden work
W_TW  = lambda r: r[4]                      # the exposure actually behind the target

BANDS = sorted(set(r[0] for r in rows))
def cell(selT, selB=None):
    def mk(base):
        return lambda r: base(r) and selT(r) and (selB is None or r[0] == selB)
    a = est(mk(S_I),   W_EQ)[0]; b = est(mk(S_I),   W_EXP)[0]
    c = est(mk(S_III), W_EQ)[0]; d = est(mk(S_III), W_EXP)[0]
    return a, b, c, d

OUT = {'cells': [], 'pooled': []}
print("\n" + "="*112)
print("CRITERION A — POOLED BY TENURE.  R = |(ii)-(iii)| / |(iii)-(i)|;  R < 0.10 == 'coincides'")
print("="*112)
print(f"  {'T':>2} {'n(i)':>6} {'n(iii)':>7} {'(i) built':>10} {'(ii) exp':>9} {'(iii) surv':>11} {'(iv) disc':>10}"
      f" {'gap%':>7} {'R':>7} {'verdict':>12}")
for T in range(1, 7):
    sT = (lambda t: (lambda r: r[1] == t))(T)
    a, b, c, d = cell(sT)
    ni = est(lambda r: S_I(r) and r[1]==T, W_EQ)[1]; niii = est(lambda r: S_III(r) and r[1]==T, W_EQ)[1]
    gap = abs(c - a); R = abs(b - c)/gap if gap > 0 else float('nan')
    info = gap/c > 0.01
    verdict = ('COINCIDES' if R < 0.10 else 'DIVERGES') if info else 'uninformative'
    print(f"  {T:2} {ni:6} {niii:7} {a:10.2f} {b:9.2f} {c:11.2f} {d:10.2f} {100*gap/c:6.2f}% {R:7.3f} {verdict:>12}")
    OUT['pooled'].append(dict(T=T, n_i=ni, n_iii=niii, built=a, exp=b, surv=c, disc=d, gap=gap, R=R,
                              informative=info, verdict=verdict))

print("\n" + "="*112)
print("CRITERION A — THE FULL GRID, TENURE x BAND")
print("="*112)
print(f"  {'band':>6} {'T':>2} {'n(i)':>5} {'n(iii)':>6} {'(i)':>8} {'(ii)':>8} {'(iii)':>8} {'(iv)':>8} {'gap%':>7} {'R':>7} {'verdict':>13}")
ncoin = ndiv = nuninf = 0
for b_ in BANDS:
    for T in range(1, 7):
        sT = (lambda t: (lambda r: r[1] == t))(T)
        a, bb, c, d = cell(sT, b_)
        if a is None or c is None: continue
        ni = est(lambda r: S_I(r) and r[1]==T and r[0]==b_, W_EQ)[1]
        niii = est(lambda r: S_III(r) and r[1]==T and r[0]==b_, W_EQ)[1]
        if niii < 4 or ni < 4: continue
        gap = abs(c - a); R = abs(bb - c)/gap if gap > 0 else float('nan')
        info = gap/c > 0.01
        if not info: v = 'uninformative'; nuninf += 1
        elif R < 0.10: v = 'COINCIDES'; ncoin += 1
        else: v = 'DIVERGES'; ndiv += 1
        lbl = '%d-%d' % tuple(MA.BANDS[b_])
        print(f"  {lbl:>6} {T:2} {ni:5} {niii:6} {a:8.2f} {bb:8.2f} {c:8.2f} {d:8.2f} {100*gap/c:6.2f}% {R:7.3f} {v:>13}")
        OUT['cells'].append(dict(band=lbl, T=T, n_i=ni, n_iii=niii, built=a, exp=bb, surv=c, disc=d,
                                 gap=gap, R=R, informative=info, verdict=v))
print(f"\n  INFORMATIVE CELLS: {ncoin+ndiv}   COINCIDES {ncoin}   DIVERGES {ndiv}   (uninformative, excluded: {nuninf})")

print("\n" + "="*112)
print("CRITERION B — THE MECHANISM TEST. Do the sub-6-game rows still carry weight?")
print("="*112)
print(f"  {'T':>2} {'sub6 rows':>10} {'count share':>12} {'wt share EQUAL':>15} {'wt share EXP':>13}"
      f" {'wt share UNCAP':>15} {'wt share TW':>12}")
for T in range(1, 7):
    sel = lambda r: S_I(r) and r[1] == T
    sub = lambda r: sel(r) and r[2] < 6
    tot = {n: est(sel, w)[2] for n, w in (('eq',W_EQ),('exp',W_EXP),('unc',W_UNC),('tw',W_TW))}
    s = {n: est(sub, w)[2] for n, w in (('eq',W_EQ),('exp',W_EXP),('unc',W_UNC),('tw',W_TW))}
    n_sub = est(sub, W_EQ)[1]
    print(f"  {T:2} {n_sub:10} {100*s['eq']/tot['eq']:11.1f}% {100*s['eq']/tot['eq']:14.1f}%"
          f" {100*s['exp']/tot['exp']:12.1f}% {100*s['unc']/tot['unc']:14.1f}% {100*s['tw']/tot['tw']:11.1f}%")
selA = lambda r: S_I(r); subA = lambda r: S_I(r) and r[2] < 6
tA = {n: est(selA, w)[2] for n, w in (('eq',W_EQ),('exp',W_EXP),('unc',W_UNC),('tw',W_TW))}
sA = {n: est(subA, w)[2] for n, w in (('eq',W_EQ),('exp',W_EXP),('unc',W_UNC),('tw',W_TW))}
pooled_wt = 100*sA['exp']/tA['exp']
print(f"  {'ALL':>2} {est(subA,W_EQ)[1]:10} {100*sA['eq']/tA['eq']:11.1f}% {100*sA['eq']/tA['eq']:14.1f}%"
      f" {pooled_wt:12.1f}% {100*sA['unc']/tA['unc']:14.1f}% {100*sA['tw']/tA['tw']:11.1f}%")
print(f"\n  CRITERION B FIRES (design dead) if the pooled EXP weight share is under 2.0%. It is {pooled_wt:.1f}%.")

print("\n" + "="*112)
print("CRITERION C — THE DISCRIMINATOR.  |(ii)-(iv)| as a % of (iv): what the added rows do")
print("="*112)
print(f"  {'T':>2} {'(ii) exp all':>13} {'(iv) exp surv-only':>19} {'diff %':>9} {'fires?':>8}")
cfire = True
for T in range(1, 7):
    sT = (lambda t: (lambda r: r[1] == t))(T)
    a, b, c, d = cell(sT)
    diff = 100*(b-d)/d
    f = abs(diff) < 0.5
    cfire = cfire and f
    print(f"  {T:2} {b:13.2f} {d:19.2f} {diff:8.2f}% {'yes' if f else 'no':>8}")
print(f"\n  CRITERION C FIRES (design dead) only if EVERY tenure is within 0.5%: {cfire}")

print("\n" + "="*112)
print("THE ALTERNATIVE WEIGHT (target-precision), reported so the choice is not hidden")
print("="*112)
print(f"  {'T':>2} {'(i) equal':>10} {'exp min(g,18)':>14} {'exp uncapped':>13} {'exp = sum g*rec':>16} {'(iii) surv':>11}")
for T in range(1, 7):
    sT = lambda r: S_I(r) and r[1] == T
    a = est(sT, W_EQ)[0]; b = est(sT, W_EXP)[0]; u = est(sT, W_UNC)[0]; t = est(sT, W_TW)[0]
    c = est(lambda r: S_III(r) and r[1] == T, W_EQ)[0]
    print(f"  {T:2} {a:10.2f} {b:14.2f} {u:13.2f} {t:16.2f} {c:11.2f}")
json.dump(OUT, open('/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb/XW_HONESTY.json','w'), indent=1)
