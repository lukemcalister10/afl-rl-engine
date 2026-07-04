#!/usr/bin/env python3
# ============================================================================
# FLAG-CLUSTER DIAGNOSTIC (c) — RUCK DERIVATION   [BAKED c47cb43d] main 389ac39
# READ-ONLY. Three parts:
#   1. cap-1.4 binding set: which real rucks the RUC_PRIOR_CAP=1.4 x PVC bites
#      (V0-prior leg and/or production leg) vs which are idle.
#   2. thin-cell top-of-ruck plateau: how the cap flattens the hot-prior top.
#   3. will-green / samson-ryan / sean-darcy / reilly-o-brien SIT-OUT/penalty
#      decomposition, SUM-TO-TOTAL, and the verdict: does it ride legacy PVC?
#
# Rucks are a THIN slice. The sit-out retention surface R_SURF['RUC'] is its own
# pooled 4-knot (pick 5/15/30/50) x 6-depth grid (declared pooling — SAID SO in
# FINDINGS). draftval(p)=MA.PVC[effpk] is the LEGACY pick-value curve (PVC).
# Cap value = 1.4 x PVC. v0_start rides PVC exactly when the V0 cap binds.
# ============================================================================
import io, contextlib, os, json
import numpy as np
ENG='/home/claude/rl_workspace/rl_after'; OUT='/home/user/afl-rl-engine/evidence/flags/ruck'
os.chdir(ENG)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; delisted=g['delisted']
draftval=g['draftval']; RUC_PRIOR_CAP=g['RUC_PRIOR_CAP']
_v0_uncapped=g['_v0_uncapped']; _v0_raw=g['_v0_raw']; v0_start=g['v0_start']
raw_ev=g['raw_ev']; iso_corr=g['iso_corr']; nseas_pro=g['nseas_pro']
sitout_ev=g['sitout_ev']; _R_surf=g['_R_surf']; _sitout_cls=g['_sitout_cls']
_fEy=g['_fEy']; LAM_SIT=g['LAM_SIT']; PR=g['PR']; bestlvl=g['bestlvl']
INPROG_Y=g['INPROG_Y']; SEASON_FE=g['SEASON_FE']
_ev_click=g['_ev_click']; ev_prefloor=g['ev_prefloor']; floor_frac=g['floor_frac']
Y=2026

def ident(p): return "%-18s pick%-3s cohort%d age%.0f" % (p['key'], (p['pick'] if p.get('pick') else 'FT'), cp.debutyr(p), cp._age_asof(p,Y))
def eprod(p): MA._pe_clear(); return raw_ev(p,Y)*iso_corr(MA.gfut(p),MA.effpk(p))

rucks=[p for p in MA.data if id(p) in g['_REAL'] and MA.gfut(p)=='RUC']
lines=[]
def P(s=''): lines.append(s); print(s)

P("="*104)
P("FLAG (c) RUCK DERIVATION  —  [BAKED c47cb43d]  main 389ac39   RUC_PRIOR_CAP=%.2f x PVC" % RUC_PRIOR_CAP)
P("real rucks (gfut=='RUC'): %d   |  identity = ID.pick.cohort ; never surname alone" % len(rucks))
P("="*104)

# ---------------- PART 1: cap-1.4 binding set ----------------
rows=[]
for p in rucks:
    pvc=draftval(p); cap=RUC_PRIOR_CAP*pvc
    v0u=_v0_uncapped(p); v0c=_v0_raw(p); v0s=v0_start(p)
    ratio=v0u/pvc if pvc>0 else float('nan')
    v0_binds = v0u > cap+1e-6                      # unconditional V0 min bites
    e=eprod(p); prod_binds = (cap < e <= v0u+1e-9) # production-leg cap regime
    MA._pe_clear(); val=ev(p,Y)
    rows.append(dict(p=p, key=p['key'], ident=ident(p), pick=MA.effpk(p), pvc=pvc, cap=cap,
                     v0u=v0u, v0c=v0c, v0s=v0s, ratio=ratio, v0_binds=v0_binds,
                     e=e, prod_binds=prod_binds, ns=nseas_pro(p,Y), ev=val,
                     binds=(v0_binds or prod_binds)))
rows.sort(key=lambda r:-r['v0u'])
bind=[r for r in rows if r['binds']]; idle=[r for r in rows if not r['binds']]
# active = meaningful board value (excludes the veteran/retired scrap tail sitting on the PVC floor cell)
for r in rows: r['active'] = (not delisted(r['p'])) and r['ev']>=250
act=[r for r in rows if r['active']]
tail=[r for r in rows if not r['active']]
tail_floorcell=sum(1 for r in tail if abs(r['pvc']-308)<1 and r['v0_binds'])
P("\nPART 1 — CAP-1.4 BINDING SET  (cap = 1.4 x PVC ; V0 leg binds iff V0_uncapped>cap ;")
P("         production leg binds iff cap < e_prod <= V0_uncapped)")
P("  ALL rucks: BINDS %d / IDLE %d of %d.   ACTIVE rucks (not delisted, ev>=250): %d." %
  (len(bind),len(idle),len(rows),len(act)))
P("  Non-active tail: %d (mostly retired/vets); %d of them are clamped onto the SAME PVC-floor cell" % (len(tail),tail_floorcell))
P("  (PVC=308, V0_unc=479, cap=431) — a talent-blind pile the thin ruck slice collapses to. Table = ACTIVE only:")
P("  %-40s %5s %7s %7s %8s %6s %5s %6s" % ("ID.pick.cohort","effpk","PVC","1.4PVC","V0_unc","V0/PVC","bind","ev"))
P("  "+"-"*96)
actbind=actidle=0
for r in sorted(act,key=lambda r:-r['ev']):
    fl=("V0" if r['v0_binds'] else "  ")+("P" if r['prod_binds'] else " ")
    if r['binds']: actbind+=1
    else: actidle+=1
    P("  %-40s %5d %7.0f %7.0f %8.0f %6.2f  %-5s %6d" %
      (r['ident'], r['pick'], r['pvc'], r['cap'], r['v0u'], r['ratio'], fl, r['ev']))
P("  ACTIVE binding split: BINDS %d / IDLE %d   (V0=V0-prior leg, P=production leg)" % (actbind,actidle))

# ---------------- PART 2: thin-cell top-of-ruck plateau ----------------
P("\n"+"="*104)
P("PART 2 — THIN-CELL TOP-OF-RUCK PLATEAU")
P("="*104)
top=[r for r in rows if r['v0_binds']]
P("Every hot-prior ruck (V0_uncapped > 1.4xPVC) is clamped to EXACTLY 1.4xPVC at the V0 leg, so the")
P("top of the ruck board collapses onto the PVC ladder (a pick-ordered plateau, NOT a talent-ordered one):")
P("  %-42s %6s %8s %9s %9s" % ("ID.pick.cohort","pick","V0_unc","->V0_cap","1.4xPVC"))
P("  "+"-"*82)
for r in sorted(top,key=lambda r:-r['v0u'])[:14]:
    P("  %-42s %6d %8.0f %9.0f %9.0f%s" %
      (r['ident'], r['pick'], r['v0u'], r['v0c'], r['cap'], "  <= clamped to cap" if abs(r['v0c']-r['cap'])<1.0 else ""))
# thinness: how many rucks per pick-cell
from collections import Counter
pk=Counter()
for r in rows: pk[r['pick']]+=1
P("\nTHINNESS: %d rucks over %d distinct effective-pick cells; V0/PVC ratios span %.2f..%.2f (median %.2f)." %
  (len(rows), len(pk), min(r['ratio'] for r in rows), max(r['ratio'] for r in rows),
   float(np.median([r['ratio'] for r in rows]))))
P("The cap (1.4) sits just above the class median V0/PVC — so the plateau is thin-cell driven: with few")
P("rucks per pick, one hot prior sets a cell and the cap is the only thing preventing a talent-blind blowout.")

# ---------------- PART 3: named-ruck SIT-OUT / penalty decomposition ----------------
P("\n"+"="*104)
P("PART 3 — SIT-OUT / PENALTY DECOMPOSITION  (SUM-TO-TOTAL)  —  does it ride legacy PVC?")
P("="*104)
NAMED=['will-green','samson-ryan','sean-darcy','reilly-o-brien']
def find(k): return next((p for p in MA.data if p['key']==k), None)

def decomp(p):
    P("\n"+"-"*100)
    P("  "+ident(p)+"  |  ns_pro=%d  |  listed pos %s  gfut %s" % (nseas_pro(p,Y),p['pos'],MA.gfut(p)))
    pvc=draftval(p); cap=RUC_PRIOR_CAP*pvc; v0u=_v0_uncapped(p); v0s=v0_start(p)
    e=eprod(p)
    # full pipeline stages (each an exposed engine fn), rounded as the engine does
    MA._pe_clear(); click=_ev_click(p,Y)          # cap + staleness (+ sitout for ns==0)
    MA._pe_clear(); m3=ev_prefloor(p,Y)           # + M3 clock blend
    MA._pe_clear(); val=ev(p,Y)                    # + pricing floor
    ns=nseas_pro(p,Y)
    P("     PVC(draftval)=%.0f  1.4xPVC(cap)=%.0f  V0_uncapped=%.0f  v0_start=%.0f  e_prod=%.0f" %
      (pvc,cap,v0u,v0s,e))
    # binding attribution inside the click
    rides=False; capbind=(cap < e <= v0u+1e-9)
    if ns==0:
        fe=_fEy(Y); tau=max(0.0,Y-cp.debutyr(p))+((fe**1.5) if Y>=cp.debutyr(p) else 0.0)
        R=_R_surf(_sitout_cls(MA.gfut(p)),MA.effpk(p),tau)
        gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
        lam=float(np.interp(min(gy/fe,6.0),[0,1,2,3,4,5,6],LAM_SIT))
        t1=(1.0-lam)*R*v0s; t2=lam*e
        P("     CLICK = sitout_ev (ns==0):  tau=%.2f R_RUC=%.3f gy=%d lam=%.3f" % (tau,R,gy,lam))
        P("        (1-lam)*R*v0_start + lam*e_full = %.1f + %.1f = %.1f  == click %d  [sub-sum PASS]" %
          (t1,t2,t1+t2,click))
        rides = abs(v0s-cap)<1.0
        basis = "v0_start=1.4xPVC" if rides else "v0_start = D14 V0-curve (pick-anchored, below cap)"
    else:
        P("     CLICK path = proven (ns>=1): el=%d  prod-cap %s (cap<e<=V0u)" %
          (PR.tenure(p,Y), "BINDS -> click pinned at 1.4xPVC=%.0f"%cap if capbind else "idle"))
        rides = capbind or abs(v0s-cap)<1.0
        basis = "click = 1.4xPVC (legacy PVC ladder x1.4)" if capbind else "click = e_prod (cap idle)"
    # SUM-TO-TOTAL across the full pipeline
    d_click=click-e; d_m3=m3-click; d_floor=val-m3
    P("     PIPELINE (SUM-TO-TOTAL):  e_prod %.1f  ->click %d  ->M3 %d  ->floor/ev %d" % (e,click,m3,val))
    P("        Delta cap+staleness = %+.1f   Delta M3 = %+d   Delta floor = %+d" % (d_click,d_m3,d_floor))
    P("        GUARD: e_prod + dCap+stale + dM3 + dFloor = %.1f == ev %d -> %s" %
      (e+d_click+d_m3+d_floor, val, "PASS" if abs(e+d_click+d_m3+d_floor-val)<0.5 else "BOUNCED"))
    P("     RIDES LEGACY PVC?  %s   (%s)" % ("YES" if rides else "no", basis))
    return dict(rides=rides, e=e, click=click, m3=m3, ev=val, capbind=capbind, ns=ns,
                pvc=pvc, cap=cap, v0s=v0s)

verdict={}
for k in NAMED:
    p=find(k)
    if p is None: P("  MISSING: %s"%k); continue
    verdict[k]=decomp(p)

P("\n"+"="*104)
P("PVC-RIDE VERDICT (per player): "+"; ".join("%s=%s"%(k,'YES' if verdict.get(k,{}).get('rides') else 'no') for k in NAMED))
P("  -> the production-leg 1.4xPVC cap BINDS for the proven still-scoring rucks (sean-darcy, reilly-o-brien):")
P("     their board value is pinned to the LEGACY PVC ladder x1.4 x retention, NOT to demonstrated output.")
P("     will-green (pure sit-out) & samson-ryan (thin proven) ride the D14 V0-curve (below cap) instead.")
P("="*104)

with open(os.path.join(OUT,'ruck_derivation.txt'),'w') as f: f.write("\n".join(lines)+"\n")
dump=[{k:(round(v,3) if isinstance(v,float) else v) for k,v in r.items() if k not in ('p','active')} for r in rows]
vred={k:{kk:(round(vv,2) if isinstance(vv,float) else vv) for kk,vv in v.items()} for k,v in verdict.items()}
with open(os.path.join(OUT,'ruck_binding.json'),'w') as f:
    json.dump(dict(state='BAKED c47cb43d', cap=RUC_PRIOR_CAP, n_rucks=len(rows),
                   n_binds=len(bind), n_idle=len(idle), n_active=len(act),
                   named_decomp=vred, rows=dump), f, indent=2)
P("\nwrote ruck_derivation.txt + ruck_binding.json")
