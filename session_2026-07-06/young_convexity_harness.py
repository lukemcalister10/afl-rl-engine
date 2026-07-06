"""Young-player convexity audit v2 — READ-ONLY. Matched draft/zero-evidence conditioning + SCAR-gap metric.
Writes nothing to the repo."""
import io,contextlib,os,sys,json,copy
import numpy as np
os.chdir('/home/claude/rl_workspace/rl_after'); sys.path.insert(0,'/home/claude/rl_vendor')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; dp=g['dp']; PR=g['PR']
ev=g['ev']; b6=g['b6']; synth=g['synth']; raw_ev=g['raw_ev']
WQ6=np.asarray(g['WQ6']); delisted=g['delisted']; _nqual=g['_nqual']
V=lambda p,L: float(dp.v_at_peak(p,float(L),'bal'))
SCALE=dp.SCALE_DIST
SCR='/tmp/claude-0/-home-user-afl-rl-engine/0783ac9f-47fd-5a10-9e9c-a70a3aeff701/scratchpad/'

def chrono_age(p):
    by=p.get('_by');  y=p.get('year')
    return 2026-int(by) if by else ((2026-(int(y)+18)) if y else None)
def band_of(a):
    if a is None: return None
    return '<=21' if a<=21 else ('22-24' if a<=24 else ('25-26' if a<=26 else '27+'))
ALLB=['1-3','4-10','11-20','21-40','41-70']
def pick_bucket(pk):
    pk=pk or 60
    for lo,hi,lab in [(1,3,'1-3'),(4,10,'4-10'),(11,20,'11-20'),(21,40,'21-40'),(41,70,'41-70')]:
        if lo<=pk<=hi: return lab
    return '41-70'
PKMID={'1-3':2,'4-10':7,'11-20':15,'21-40':30,'41-70':55}

def gaps(vmap, levels, weights=None):
    """E[V(L)], V(E[L]), gap=E-Vm, ratio=E/Vm-1 (None if Vm~0), meanL."""
    L=np.asarray(levels,float)
    w=np.ones(len(L)) if weights is None else np.asarray(weights,float)
    w=w/w.sum()
    E=float(np.dot(w,[V(vmap,x) for x in L])); mL=float(np.dot(w,L)); Vm=V(vmap,mL)
    return E,Vm,E-Vm,(E/Vm-1 if Vm>1.0 else None),mL

# ---- zero-evidence draft reference player per (pos,pick): current young age ~20, NO scoring evidence ----
def draft_ref(pos,pk):
    r=copy.deepcopy(synth(pk,50.0,pos,1)); r['scoring']=[]; r['_by']=2006; r['dob']='2006-03-01'
    r['year']=2025; r.pop('_eff',None)   # draft 2025 -> debut 2026, age 20 in 2026
    return r

# ============================================================================
# STEP 2 — CURRENT engine premium, per player, by band, SEGMENTED proven/unproven
# ============================================================================
players=[p for p in MA.data if MA.GRP.get(p.get('pos')) and p.get('key') and not delisted(p)]
rows=[]
for p in players:
    a=chrono_age(p); bnd=band_of(a)
    if bnd is None: continue
    bb=[float(x) for x in b6(p)]
    E=float(SCALE*np.dot(WQ6,[V(p,L) for L in bb])); mL=float(np.dot(WQ6,bb)); Vm=float(SCALE*V(p,mL))
    nq=_nqual(p,2026)
    rows.append(dict(player=p['player'],pos=MA.gfut(p),age=a,band=bnd,pick=p.get('pick'),
        ev=ev(p),vpt=p.get('_vpt'),cvx=p.get('_cvx'),nqual=nq,proven=nq>=4,
        E=round(E,1),Vm=round(Vm,1),gap=round(E-Vm,1),ratio=(round(E/Vm-1,4) if Vm>1 else None)))

def vw(vals,wts):
    v=np.asarray(vals,float); w=np.asarray(wts,float); m=(w>0)&np.isfinite(v)
    return float(np.dot(v[m],w[m])/w[m].sum()) if w[m].sum()>0 else float('nan')

print("="*72); print("STEP 2 — CURRENT ENGINE PREMIUM BY BAND (segmented proven vs unproven)"); print("="*72)
cur={}
for bnd in ['<=21','22-24','25-26','27+']:
    br=[r for r in rows if r['band']==bnd]
    if not br: continue
    for seg,ss in [('ALL',br),('unproven(nq<4)',[r for r in br if not r['proven']]),('proven(nq>=4)',[r for r in br if r['proven']])]:
        if not ss: continue
        totev=sum(r['ev'] for r in ss)
        cr=[r for r in ss if r['cvx'] is not None and r['vpt']]
        cvxp=vw([r['cvx']-1 for r in cr],[r['vpt'] for r in cr]) if cr else float('nan')
        rr=[r for r in ss if r['ratio'] is not None]
        ratiop=vw([r['ratio'] for r in rr],[r['ev'] for r in rr]) if rr else float('nan')
        totgap=sum(r['gap'] for r in ss)
        atcap=sum(1 for r in cr if abs(r['cvx']-1.25)<1e-6); excl=len(ss)-len(cr)
        if seg=='ALL': cur[bnd]=dict(n=len(ss),totev=round(totev),cvxp=round(cvxp,4) if cvxp==cvxp else None,
            ratiop=round(ratiop,4) if ratiop==ratiop else None,totgap=round(totgap),atcap=atcap,excl=excl)
        print(f"  {bnd:6s} {seg:16s} n={len(ss):3d} totEV={totev:6.0f} | _cvx prem(vw)={100*cvxp:+5.2f}% [def {len(cr)},excl {excl},cap {atcap}] "
              f"| fwd-band E[v]/v(mean)-1 (vw)={(str(round(100*ratiop,1))+'%') if ratiop==ratiop else 'n/a':>7s} totgap={totgap:7.0f}")

# ============================================================================
# STEP 3 — MATCHED DRAFT-STATE: engine draft band vs empirical outcomes, same value map
# ============================================================================
print("\n"+"="*72); print("STEP 3 — DRAFT-STATE MATCHED: engine band vs empirical forward outcomes"); print("="*72)
MINN=20
resolved=[p for p in MA.data if p.get('key') and p.get('type')=='ND' and p.get('pick') and cp.debutyr(p)<=2020 and MA.GRP.get(p.get('pos'))]
def outcomes(pos,buckets):
    o=[]
    for p in resolved:
        if MA.gfut(p)==pos and pick_bucket(p.get('pick')) in buckets:
            v=cp.fwd_best3_from(p,cp.debutyr(p)-1,2026)
            if v is not None: o.append(float(v))
    return o
def gather(pos,pb):
    idx=ALLB.index(pb)
    for span in range(len(ALLB)):
        bs=ALLB[max(0,idx-span):min(len(ALLB),idx+span+1)]; o=outcomes(pos,bs)
        if len(o)>=MINN: return o,bs,('exact' if span==0 else 'pooled')
    return outcomes(pos,ALLB),ALLB,'all'

# cohorts present on the young board
young=[r for r in rows if r['band'] in ('<=21','22-24','25-26')]
cohorts={}
for r in young: cohorts.setdefault((r['pos'],pick_bucket(r['pick'])),[]).append(r)

impl={}
print(f"resolved pool {len(resolved)}  (engine draft-band vs empirical, both via zero-evidence draft ref; gaps in SCAR)")
print(f"  {'cohort':16s} {'nE':>3s} {'bust':>4s} {'empμ':>5s} {'engμ':>5s} | {'impl_gap':>8s} {'eng_gap':>8s} {'short':>7s} | {'impl_E':>7s} {'eng_E':>7s} curN curEV")
for (pos,pb),rs in sorted(cohorts.items()):
    emp,used,how=gather(pos,pb)
    if len(emp)<12:
        impl[(pos,pb)]=dict(note='thin',n_emp=len(emp)); continue
    emp=np.asarray(emp,float)
    ref=draft_ref(pos,PKMID[pb])
    iE,iVm,iGap,iRat,iMu=gaps(ref,emp)                        # implied (empirical outcomes)
    bb=[float(x) for x in b6(ref,cp.debutyr(ref)-1)]          # engine DRAFT band, same ref
    eE,eVm,eGap,eRat,eMu=gaps(ref,bb,WQ6)                     # engine (its band)
    short=iGap-eGap
    bust=float((emp<1e-6).mean())
    impl[(pos,pb)]=dict(n_emp=int(len(emp)),how=how,bust=round(bust,3),emp_mu=round(iMu,1),eng_mu=round(eMu,1),
        impl_gap=round(iGap,1),eng_gap=round(eGap,1),short_gap=round(short,1),
        impl_E=round(iE,1),eng_E=round(eE,1),eng_band=[round(x,1) for x in bb],
        n_cur=len(rs),ev_cur=sum(r['ev'] for r in rs))
    print(f"  {pos+' '+pb:16s} {len(emp):3d} {bust:4.2f} {iMu:5.0f} {eMu:5.0f} | {iGap:8.0f} {eGap:8.0f} {short:+7.0f} | {iE:7.0f} {eE:7.0f} {len(rs):4d} {sum(r['ev'] for r in rs):6.0f} ({how})")

# ============================================================================
# STEP 4/5 — shortfall direction by band, flags
# ============================================================================
print("\n"+"="*72); print("STEP 4 — net shortfall direction (draft-state), value-weighted by current cohort EV"); print("="*72)
for bnd in ['<=21','22-24','25-26','ALL-young']:
    num=den=0.0
    for (pos,pb),d in impl.items():
        if 'short_gap' not in d: continue
        rs=[r for r in cohorts[(pos,pb)] if (bnd=='ALL-young' or r['band']==bnd)]
        if not rs: continue
        w=sum(r['ev'] for r in rs); num+=d['short_gap']*w; den+=w
    if den>0:
        print(f"  {bnd:10s} value-weighted shortfall (implied-engine, draft-state) = {num/den:+.0f} SCAR/player-equiv  (EVw={den:.0f})")

print("\n"+"="*72); print("STEP 5 — FLAGS (|engine-implied| large; FOR OWNER RULING, not applied)"); print("="*72)
under=[]; over=[]
for (pos,pb),d in sorted(impl.items()):
    if 'short_gap' not in d: continue
    if d['impl_E']<50 and d['eng_E']<50: continue   # both negligible
    rel=d['short_gap']/max(1.0,d['eng_E'])
    rec=dict(pos=pos,pb=pb,short=d['short_gap'],eng_E=d['eng_E'],impl_E=d['impl_E'],rel=round(rel,3),bust=d['bust'],n_cur=d['n_cur'],ev_cur=d['ev_cur'])
    if rel>0.15: under.append(rec)
    elif rel<-0.15: over.append(rec)
print("UNDER-priced (implied > engine; candidate RAISE):")
for r in sorted(under,key=lambda z:-z['short']): print(f"  {r['pos']:8s} pk{r['pb']:6s} short={r['short']:+.0f} SCAR ({100*r['rel']:+.0f}% of eng) bust={r['bust']} curN={r['n_cur']} curEV={r['ev_cur']}")
if not under: print("  (none)")
print("OVER-priced (engine > implied; FLAG for owner ruling, NOT applied):")
for r in sorted(over,key=lambda z:z['short']): print(f"  {r['pos']:8s} pk{r['pb']:6s} short={r['short']:+.0f} SCAR ({100*r['rel']:+.0f}% of eng) bust={r['bust']} curN={r['n_cur']} curEV={r['ev_cur']}")
if not over: print("  (none)")

json.dump(dict(current=cur,rows=rows,implied={f"{k[0]}|{k[1]}":v for k,v in impl.items()},
    under=under,over=over,consts=dict(CVX_CAP=MA.CVX_CAP,PMAX=MA.PMAX,PRESENT_VAR=MA.PRESENT_VAR)),
    open(SCR+'audit_out2.json','w'),indent=1,default=str)
print("\nJSON -> audit_out2.json")
