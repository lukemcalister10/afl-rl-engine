#!/usr/bin/env python3
"""v1.1 CONFIRM (seg-3): elasticity of the NEW rho axis vs realised output o, proven-27+, frozen estimator.
rho numerator (v1.1 memo 2.1) = recent-2 QUALIFYING-season avg points above REPL[pos]; qualifying = games>=FLOOR.
Contrast against level_now (v1.0 axis, lambda~0.124). Expect the v1.1 axis lambda ~ 1 (why the re-wire raises beta)."""
import io,contextlib,sys,math
import numpy as np
REPL={'MID':80.1,'GEN_DEF':78.3,'RUC':78.5,'KEY_DEF':68.4,'GEN_FWD':70.9,'KEY_FWD':66.8}
rng=np.random.default_rng(0)
def fit_beta(x_,y_,nb=1000):
    x=np.array([math.log(v) for v in x_]); y=np.array([math.log(v) for v in y_])
    b1,_=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(x),len(x))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    lo,hi=np.percentile(bs,[2.5,97.5]); return b1,lo,hi
def rho_num(p,pos,floor):
    rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>=floor and x.get('avg',0)>0])
    if not rows: return None
    return sum(v for _,v in rows[-2:])/len(rows[-2:]) - REPL[pos]
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; delisted=g['delisted']; _isreal=g['_isreal']
# o (estimator) = recent-2 games>0 avg above REPL, EXACTLY as calibrate.py / the s-dial estimator
O=[];RHO10=[];RHO6=[];LN=[]
for p in MA.data:
    MA.BASE_REF=MA.AGE_REF=2026
    if not _isreal(p) or delisted(p) or p.get('_retired'): continue
    a=MA.age(p)
    if a is None or a<27: continue
    pos=MA.gfut(p)
    if pos not in REPL: continue
    rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>0 and x.get('avg',0)>0])
    if not rows: continue
    o=sum(v for _,v in rows[-2:])/len(rows[-2:])-REPL[pos]
    r10=rho_num(p,pos,10); r6=rho_num(p,pos,6); ln=MA.level_now(p)
    if o>0 and r10 and r10>0 and r6 and r6>0 and ln and ln>0:
        O.append(o); RHO10.append(r10); RHO6.append(r6); LN.append(float(ln))
n=len(O)
for lbl,y in (('rho_v1.1 num (games>=10)',RHO10),('rho num (games>=6)',RHO6),('level_now (v1.0 axis)',LN)):
    b,lo,hi=fit_beta(O,y)
    sys.stderr.write("lambda[ %-26s vs o ] = %.4f  CI=[%.4f,%.4f]  n=%d\n"%(lbl,b,lo,hi,n))
