# INDEPENDENT re-derivation of R_SIT + LAM_SIT from raw scoring histories.
# Own harvest, own kernel/isotonic. Estimator (from spec): sit-out cell = no qualifying (>=6g)
# season through Y; r=O/V0, O=price6 of best fwd qualifying era-adj level in (Y,Y+4] busts=0,
# V0=raw_ev(draftyr)*iso. R_SIT=M_SIT/NORM ("0.76 form"); LAM from d1 g0..5 + graduated 6-9.
import io, contextlib, json, numpy as np
OUT=open('/tmp/claude-0/-home-user-afl-rl-engine/a62bb32e-b9ba-53aa-805e-a08c12f3bf5a/scratchpad/rederive_out.txt','w')
def P(*a): print(*a, file=OUT)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; PR=g['PR']; cp=g['cp']; era=g['era']; REF=g['REF']
raw_ev=g['raw_ev']; iso_corr=g['iso_corr']; price6=g['price6']; CLS=g['_sitout_cls']
R_SIT_WIRED=g['R_SIT']; LAM_WIRED=g['LAM_SIT']

def draftyr(p): return cp.debutyr(p)-1
def min_window(p):
    t,pk=p.get('type'),p.get('pick')
    if t=='ND' and pk and pk<=20: return 4
    if t=='ND' and pk and pk<=40: return 3
    return 2
def listed_through(p):
    if p.get('_last_listed') is not None: return int(p['_last_listed'])
    if not p.get('_retired'): return 2026
    lg=max((x['year'] for x in p['scoring']),default=0); dy=p.get('year') or lg
    return max(dy+min_window(p)-1,lg)
def V0(p):
    with contextlib.redirect_stdout(io.StringIO()):
        return raw_ev(p,draftyr(p))*iso_corr(MA.gfut(p),MA.effpk(p))
def outO(p,Y):
    fwd=[x for x in p['scoring'] if x['games']>=6 and Y<x['year']<=Y+4]
    if not fwd: return 0.0
    L=max(x['avg']*REF/era.get(x['year'],REF) for x in fwd)
    with contextlib.redirect_stdout(io.StringIO()):
        return price6(p,[L]*6,Y)

# ---- HARVEST ----
sit=[]      # sit-out cells: dict(cls,d,gY,r,q)
grad=[]     # graduated depth-1 boundary (6-9 g)
normr={c:{d:[] for d in range(1,7)} for c in ('nonKPP','KPP','RUC')}   # all still-listed r by depth
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.data:
        if p.get('_double_count') or not MA.GRP.get(p.get('pos')): continue
        if not (p.get('pick') or p.get('_ft')): continue
        dy=draftyr(p)
        if dy<2003 or dy>2024: continue
        lt=listed_through(p); pos=MA.gfut(p); cls=CLS(pos); v0=V0(p)
        if v0<=0: continue
        rows=sorted(p['scoring'],key=lambda x:x['year'])
        # NORM: all still-listed at depth d (complete window Y<=2021)
        for d in range(1,7):
            Y=dy+d
            if Y>min(lt,2021): continue
            normr[cls][d].append(min(outO(p,Y)/v0,2.0))
        for Y in range(dy+1,min(lt,2025)+1):
            if Y>2021: continue   # complete-window only
            quals=[x for x in rows if x['games']>=6 and x['year']<=Y]
            yrow=[x for x in rows if x['year']==Y]; gY=yrow[0]['games'] if yrow else 0
            avgY=(yrow[0]['avg']*REF/era.get(Y,REF)) if yrow else 0.0
            q=avgY/max(1.0,MA.REPL.get(pos,1.0)); d=Y-dy
            r=min(outO(p,Y)/v0,2.0)
            if not quals:
                sit.append(dict(cls=cls,d=min(d,7),gY=gY,r=r,q=q))
            elif d==1 and len(quals)==1 and quals[0]['year']==Y and 6<=gY<=9:
                grad.append(dict(cls=cls,d=1,gY=gY,r=r,q=q))
P("HARVEST: sit-out cells=%d  graduated=%d"%(len(sit),len(grad)))
from collections import Counter
P("  by depth:",dict(sorted(Counter(c['d'] for c in sit).items())))
P("  by cls:",dict(Counter(c['cls'] for c in sit)))

# ---- KERNEL (gaussian over depth, bw grown to eff-n>=35) ----
def ksm(pts,grid,minn=35):
    out={}
    for x0 in grid:
        bw=0.5
        while True:
            w=np.array([np.exp(-0.5*((c-x0)/bw)**2) for c,_ in pts])
            effn=w.sum()**2/(w**2).sum() if w.sum()>0 else 0
            if effn>=min(minn,len(pts)*0.9) or bw>4.0: break
            bw+=0.25
        vals=np.array([v for _,v in pts])
        out[x0]=float((w*vals).sum()/w.sum())
    return out
DG=[1,2,3,4,5,6]
z=[c for c in sit if c['gY']==0]
# M_SIT (zero-game sit-out realization, kernel over depth)
M={}
for cls in ('nonKPP','KPP'):
    M[cls]=[ksm([(c['d'],c['r']) for c in z if c['cls']==cls],DG)[d] for d in DG]
pts_kr=[(c['d'],c['r']) for c in z if c['cls'] in ('KPP','RUC')]
smkr=ksm(pts_kr,DG)
ruc12=[c['r'] for c in z if c['cls']=='RUC' and c['d']<=2]
kpp12=[c['r'] for c in z if c['cls'] in ('KPP','RUC') and c['d']<=2]
scale=np.mean(ruc12)/np.mean(kpp12)
M['RUC']=[smkr[d]*scale for d in DG]
# NORM
NORM={cls:[float(np.mean(normr[cls][d])) for d in DG] for cls in ('nonKPP','KPP','RUC')}
# R_SIT = M/NORM, 3pt smooth, clip [0.05,1.0]
def sm3(a):
    o=[]
    for i in range(len(a)):
        lo=a[max(0,i-1)]; hi=a[min(len(a)-1,i+1)]; o.append(0.25*lo+0.5*a[i]+0.25*hi)
    return o
R={}
for cls in ('nonKPP','KPP','RUC'):
    ratio=[m/n for m,n in zip(M[cls],NORM[cls])]
    R[cls]=[round(float(np.clip(v,0.05,1.0)),3) for v in sm3(ratio)]
P("\n== RE-DERIVED R_SIT (mine) vs WIRED ==")
P("  RUC pooled-KPP scale = %.3f (n_ruc_d12=%d)"%(scale,len(ruc12)))
for cls in ('nonKPP','KPP','RUC'):
    mine=R[cls]; wired=R_SIT_WIRED[cls]
    dmax=max(abs(a-b) for a,b in zip(mine,wired))
    P("  %-7s NORM=%s"%(cls,[round(x,3) for x in NORM[cls]]))
    P("          M_SIT=%s"%[round(x,3) for x in M[cls]])
    P("          MINE =%s"%mine)
    P("          WIRED=%s   maxΔ=%.3f  %s"%(wired,dmax,'PASS(<=0.05)' if dmax<=0.05 else 'OVER-TOL'))

# ---- LAMBDA ----
d1=[c for c in sit if c['d']==1]
allg=d1+grad
mg_raw={}
for gg in range(0,10):
    v=[c['r'] for c in allg if c['gY']==gg]
    if v: mg_raw[gg]=(float(np.mean(v)),len(v))
smg=ksm([(c['gY'],c['r']) for c in allg],list(range(0,10)))
mg=[smg[gg] for gg in range(0,10)]
mono=np.maximum.accumulate(mg)
m0,m6=mono[0],mono[6]
lam=[round(float(np.clip((v-m0)/(m6-m0),0,1)),3) for v in mono[:7]]
P("\n== RE-DERIVED LAMBDA (mine) vs WIRED ==")
P("  raw m(g): "+" ".join("g%d:%.3f(n%d)"%(gg,a,n) for gg,(a,n) in sorted(mg_raw.items())))
P("  MINE =%s"%lam)
P("  WIRED=%s"%LAM_WIRED)
dmax=max(abs(a-b) for a,b in zip(lam,LAM_WIRED))
P("  maxΔ=%.3f  %s"%(dmax,'PASS(<=0.10)' if dmax<=0.10 else 'OVER-TOL'))
# evidence-axis test
def kendall(x,y):
    x,y=np.asarray(x,float),np.asarray(y,float); n=len(x); s=0
    for i in range(n): s+=np.sum(np.sign((x[i+1:]-x[i])*(y[i+1:]-y[i])))
    return 2.0*s/(n*(n-1)) if n>1 else 0.0
d1p=[c for c in d1 if c['gY']>=1]
P("  evidence-axis tau within played d1 (n=%d): g=%.3f q=%.3f gxq=%.3f"%(
    len(d1p),kendall([c['gY'] for c in d1p],[c['r'] for c in d1p]),
    kendall([c['q'] for c in d1p],[c['r'] for c in d1p]),
    kendall([c['gY']*c['q'] for c in d1p],[c['r'] for c in d1p])))
OUT.close(); print("done")
