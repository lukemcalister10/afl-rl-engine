#!/usr/bin/env python3
"""item-221 explanatory: the frozen estimator's beta for the un-compress TARGET AXES vs realised output o,
over the same proven-27+ sample. Shows why any blend toward t=V_ref_b*rho (rho=level_now/L_ref) compresses:
the target's own elasticity vs o (= the w->1 limit of beta) is BELOW beta_c."""
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
g={}
with contextlib.redirect_stdout(io.StringIO()): exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; delisted=g['delisted']; _isreal=g['_isreal']; price6=g['price6']; b6=g['b6']
O=[];EVv=[];PR=[];LN=[]
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
    ln=MA.level_now(p)
    with contextlib.redirect_stdout(io.StringIO()):
        e=ev(p); pr=price6(p,b6(p,2026),2026)
    if o>0 and e and e>0 and pr and pr>0 and ln and ln>0:
        O.append(o); EVv.append(float(e)); PR.append(float(pr)); LN.append(float(ln))
n=len(O)
for lbl,y in (('ev (=beta_c)',EVv),('price6 (production)',PR),('level_now (rho axis)',LN)):
    b,lo,hi=fit_beta(O,y)
    sys.stderr.write("beta[ %-22s vs o ] = %.4f  CI=[%.4f,%.4f]  n=%d\n"%(lbl,b,lo,hi,n))
