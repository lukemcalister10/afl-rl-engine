"""Year-1 mover census and the Mraz line, per round-3 arm.

Population and filter are the harness loader's own (teaches_curve, pick 1-64, class 2004-2022),
matching the canonical table's denominator exactly. A "mover" is a row whose year-1 as-of price
vpath[0] differs from the FULL build's. FULL-SEASON movers are the ones ITEM A never reached: rows
with games_yr1 >= 6, where the built-A saturation pins the anchor share to exactly 0.
"""
import json, sys, statistics
SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
def load(L):
    d=json.load(open(f"{SP}/per_entrant_{L}.json"))
    return {r['key']: r for r in d['recs']}
F=load('FULL')
POP=[k for k,r in F.items() if r.get('teaches_curve') and r.get('pick') and 1<=r['pick']<=64
     and r.get('year') and 2004<=r['year']<=2022]
print(f"population (harness filter) n = {len(POP)}")
print(f"{'arm':8} {'yr1 movers':>10} {'>=6g':>6} {'1-5g':>6} {'0g':>5} {'up':>5} {'down':>5} {'med %':>8} {'Mraz':>7}")
MRAZ='noah-mraz'   # ND 2024 pick 35; class 2024 is OUTSIDE the 2004-2022 teaching cut, so he is in the matrix but not in the ratio population
allk=set(F)
for L in ['IDENT5','AGSATF','AGSATD','V5','C336P','C336E','C336C']:
    A=load(L)
    mv=[]; 
    for k in POP:
        a,b=F[k], A.get(k)
        if b is None: continue
        va = a['vpath'][0] if a.get('vpath') else None
        vb = b['vpath'][0] if b.get('vpath') else None
        if va is None or vb is None: continue
        if abs(va-vb)>1e-9: mv.append((k, va, vb, F[k].get('games_yr1') or 0))
    g6=sum(1 for m in mv if m[3]>=6); g15=sum(1 for m in mv if 1<=m[3]<=5); g0=sum(1 for m in mv if m[3]==0)
    up=sum(1 for m in mv if m[2]>m[1]); dn=len(mv)-up
    pct=[100*(m[2]/m[1]-1) for m in mv if m[1]>0]
    mz=A.get(MRAZ); mzf=F.get(MRAZ)
    mzs = f"{mz['cur']:.0f}" if mz and mz.get('cur') is not None else "n/a"
    print(f"{L:8} {len(mv):10} {g6:6} {g15:6} {g0:5} {up:5} {dn:5} "
          f"{statistics.median(pct) if pct else 0:7.2f}% {mzs:>7}")
mzf=F.get(MRAZ)
print("\nMRAZ (%s) — pick %s, class %s, in the ratio population: %s"
      % (MRAZ, mzf.get('pick'), mzf.get('year'), MRAZ in POP))
print("  the matrix column is his as-of-2026 engine valuation `cur`; the ladder-currency board line is")
print("  reported separately in MENU.txt from board builds (PVC0[35] = 561.0, the frozen pick-35 ruler).")
print("  %-8s %9s" % ('arm','cur'))
for L in ['FULL','IDENT5','AGSATF','AGSATD','V5','C336P','C336E','C336C']:
    A=load(L); print("  %-8s %9.1f" % (L, A[MRAZ]['cur']))
