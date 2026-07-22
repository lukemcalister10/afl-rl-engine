#!/usr/bin/env python3
"""LEG B SEGMENT-4 — KERNEL-FAMILY λ ROUND (supervisor item 243; FINDINGS ONLY, nothing selected).
Same PINNED frozen fit_beta + same sample law as rho_axis_v12.py (measure.py::measure3 @2b76d37).
The ρ construction generalises to a per-game recency kernel K(b), b=years-back=2026−year:
    ρ_num(p,pos) = Σ_s games_s·K(b_s)·(avg_s−REPL[pos]) / Σ_s games_s·K(b_s)   over ALL games>0 seasons.
(v1.2 was K(b)=0.5^b.) Candidates measured this round:
  - geometric  K(b)=d^b            d ∈ {0.10,0.15,0.20,0.25}
  - gaussian   K(b)=exp(−(b/h)^2)  h ∈ {0.8,1.0,1.3}
  - soft-shoulder logistic K(b)=1/(1+exp((b−1.5)/0.5))   (full-ish ≤1yr, falloff center 1.5, width 0.5)
Per-candidate ASSERTIONS (both must hold — else the candidate is flagged): (A) positive weight for EVERY
played game in the store (no exclusion); (B) per-game weight K(b) strictly non-increasing in years-back
(L-RECENCY). Reports λ(point·CI·n) + Sam Darcy & Darcy Moore ρ per shape. Writes NOTHING to store/engine/board."""
import io,contextlib,sys,math,json
import numpy as np
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; delisted=g['delisted']; _isreal=g['_isreal']; _nqual=g['_nqual']; eng_rho_out=g['rho_out']
PROVEN_N=g.get('PROVEN_N', getattr(MA,'PROVEN_N',4))
MA.BASE_REF=MA.AGE_REF=2026
REPL=dict(MA.REPL); YNOW=2026

def fit_beta(x_,y_,nb=1000):
    rng=np.random.default_rng(0)
    x=np.array([math.log(v) for v in x_]); y=np.array([math.log(v) for v in y_])
    b1,_=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(x),len(x))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    lo,hi=np.percentile(bs,[2.5,97.5]); return b1,lo,hi

# ---- kernels K(b), b = years-back ----
def geom(d):  return (lambda b: d**b)
def gauss(h): return (lambda b: math.exp(-(b/h)**2))
def soft():   return (lambda b: 1.0/(1.0+math.exp((b-1.5)/0.5)))
KERNELS=[('geom d=0.10',geom(0.10)),('geom d=0.15',geom(0.15)),('geom d=0.20',geom(0.20)),('geom d=0.25',geom(0.25)),
         ('gauss h=0.8',gauss(0.8)),('gauss h=1.0',gauss(1.0)),('gauss h=1.3',gauss(1.3)),
         ('soft-shoulder 1.5/0.5',soft()),
         ('[anchor] geom d=0.50 (v1.2 law)',geom(0.50)),('[anchor] floor6 recent-2 (v1.1)',None)]

def rho_num_K(p,pos,K):
    num=0.0; den=0.0
    for x in p['scoring']:
        gm=x.get('games',0) or 0
        if gm<=0: continue
        u=gm*K(YNOW-x['year']); num+=u*(x['avg']-REPL[pos]); den+=u
    return None if den<=0.0 else num/den
def rho_floor6(p,pos):   # the v1.1 anchor (recent-2 of games>=6)
    rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>=6 and x.get('avg',0)>0])
    if not rows: return None
    return sum(a for _,a in rows[-2:])/len(rows[-2:])-REPL[pos]

# observed years-back on ALL played store games (for the assertions)
BS=sorted({YNOW-x['year'] for p in MA.data for x in (p.get('scoring') or []) if (x.get('games',0) or 0)>0})
def assert_kernel(K):
    kb=[K(b) for b in BS]
    posA=all(v>0.0 for v in kb)                                   # (A) positive weight for every played game
    monoB=all(kb[i]>=kb[i+1]-1e-15 for i in range(len(kb)-1))     # (B) non-increasing in years-back
    strict=all(kb[i]>kb[i+1] for i in range(len(kb)-1))
    return posA,monoB,strict,min(kb)

# named players
def findp(sub,pos=None):
    hits=[p for p in MA.data if p['player'].strip().lower()==sub.lower() and (pos is None or MA.gfut(p)==pos)]
    return hits[0] if hits else None
SAM=findp('Sam Darcy'); MOORE=findp('Darcy Moore','KEY_DEF')

# proven pop for RHO_DEN[pos] (reference-build population)
PROVEN={}
for p in MA.data:
    if not (_isreal(p) and not delisted(p) and not p.get('_retired')): continue
    if _nqual(p,2026)<PROVEN_N: continue
    pos=MA.gfut(p)
    if pos in REPL: PROVEN.setdefault(pos,[]).append(p)

# λ sample (proven-27+, o = recent-2 games>0 avg above REPL)
POP=[p for p in MA.data if _isreal(p) and not delisted(p) and not p.get('_retired')
     and MA.gfut(p) in REPL and MA.age(p) is not None]
def sample_o():
    S=[]
    for p in POP:
        a=MA.age(p)
        if a is None or a<27: continue
        pos=MA.gfut(p)
        rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>0 and x.get('avg',0)>0])
        if not rows: continue
        o=sum(a2 for _,a2 in rows[-2:])/len(rows[-2:])-REPL[pos]
        ln=MA.level_now(p)
        if o>0 and ln and ln>0: S.append((p,pos,o))
    return S
SMP=sample_o()

def rho_den(rho_fn):
    d={}
    for pos,ps in PROVEN.items():
        vals=[rho_fn(p,pos) for p in ps]; vals=[v for v in vals if v and v>0.0]
        if vals: d[pos]=float(np.median(vals))
    return d

res=[]; hdr="%-32s  %8s  %-18s  %4s   %-6s  %-24s  %-24s"%(
    'kernel K(b)','λ','CI','n','asserts','Sam Darcy KEY_FWD','Darcy Moore KEY_DEF')
sys.stderr.write(hdr+"\n"+"-"*len(hdr)+"\n")
for lbl,K in KERNELS:
    if K is None: rho_fn=rho_floor6; posA=monoB=strict=True; mink=float('nan')
    else:
        rho_fn=lambda p,pos,K=K: rho_num_K(p,pos,K); posA,monoB,strict,mink=assert_kernel(K)
    O=[];R=[]
    for p,pos,o in SMP:
        r=rho_fn(p,pos)
        if r and r>0: O.append(o); R.append(r)
    b1,lo,hi=fit_beta(O,R)
    RD=rho_den(rho_fn)
    def named(pl,pos):
        if pl is None: return (None,None)
        rn=rho_fn(pl,pos); den=RD.get(pos)
        return (round(rn,2) if rn is not None else None,
                round(rn/den,3) if (rn is not None and den) else None)
    sam_rn,sam_r=named(SAM,'KEY_FWD'); mr_rn,mr_r=named(MOORE,'KEY_DEF')
    ab='%s%s'%('P' if posA else 'x','R' if monoB else 'x')
    row={'kernel':lbl,'lambda':round(b1,4),'ci':[round(lo,4),round(hi,4)],'n':len(O),
         'assert_positive':bool(posA),'assert_Lrecency_nonincreasing':bool(monoB),'strictly_decreasing':bool(strict),
         'min_pergame_weight':(None if mink!=mink else float('%.3g'%mink)),
         'sam_darcy':{'rho_num':sam_rn,'rho':sam_r},'darcy_moore':{'rho_num':mr_rn,'rho':mr_r},
         'rho_den':{k:round(v,2) for k,v in RD.items()}}
    res.append(row)
    gate='>=0.95' if b1>=0.95 else '<0.95'
    sys.stderr.write("%-32s  %7.4f  [%.3f,%.3f]  %4d   %-6s  ρnum=%-7s ρ=%-8s  ρnum=%-7s ρ=%-8s  %s\n"%(
        lbl,b1,lo,hi,len(O),ab+('/'+('str' if strict else 'flat') if K is not None else ''),
        sam_rn,sam_r,mr_rn,mr_r,gate))
sys.stderr.write("\nasserts key: P=positive weight every played game, R=L-RECENCY non-increasing, str=strictly decreasing.\n")
sys.stderr.write("Sam Darcy   scoring (yr,g,avg): %s\n"%[(x['year'],x.get('games',0),round(x.get('avg',0),1)) for x in sorted(SAM['scoring'],key=lambda r:r['year']) if (x.get('games',0) or 0)>0])
sys.stderr.write("Darcy Moore scoring (yr,g,avg): %s\n"%[(x['year'],x.get('games',0),round(x.get('avg',0),1)) for x in sorted(MOORE['scoring'],key=lambda r:r['year']) if (x.get('games',0) or 0)>0])
print(json.dumps({'gate':0.95,'sample_n':len(SMP),'years_back_observed':[BS[0],BS[-1]],'proven_pop':{k:len(v) for k,v in PROVEN.items()},'candidates':res},indent=1))
