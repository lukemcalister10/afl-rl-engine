#!/usr/bin/env python3
"""item-221 diagnostic, ONE engine load: build V_ref_b once (s-independent), then measure the frozen-estimator
beta for OFF + each grid s by flipping the live _L2S. Prints one line per s to stderr."""
import io,contextlib,sys,os,math
import numpy as np
REPL={'MID':80.1,'GEN_DEF':78.3,'RUC':78.5,'KEY_DEF':68.4,'GEN_FWD':70.9,'KEY_FWD':66.8}
rng=np.random.default_rng(0)
def fit_beta(sub,nb=1000):
    if len(sub)<8: return None,None,None
    x=np.array([math.log(p['o']) for p in sub]); y=np.array([math.log(p['p']) for p in sub])
    b1,b0=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(sub),len(sub))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    return b1,b0,tuple(np.percentile(bs,[2.5,97.5]))
# load with L2 flag SET (to force V_ref_b construction), then vary _L2S live
os.environ['RL_UNCOMP_L2_S']='0.55'
g={}
with contextlib.redirect_stdout(io.StringIO()) as _b: exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; find=g['find']; delisted=g['delisted']; _isreal=g['_isreal']
# the module namespace g holds _L2S / _L2_LREF / _L2_VREFB / raw_ev (all in the exec dict)
for L in _b.getvalue().splitlines():
    if 'V_ref_b' in L or 'DIAGNOSTIC' in L: sys.stderr.write(L+'\n')
def measure(sval):
    g['_L2S']=sval                                              # flip the live blend strength (V_ref_b already built, s-independent)
    sub=[]
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
        with contextlib.redirect_stdout(io.StringIO()): pr=ev(p)
        if o>0 and pr and pr>0: sub.append({'o':o,'p':float(pr)})
    b1,b0,ci=fit_beta(sub)
    lbl='OFF' if sval is None else '%.2f'%sval
    if b1 is None: sys.stderr.write("s=%-5s beta=NA n=%d\n"%(lbl,len(sub))); return
    sys.stderr.write("s=%-5s beta=%.4f CI=[%.4f,%.4f] width=%.4f n=%d | pt>=0.85:%s CI_1.0:%s width<=0.35:%s n>=120:%s\n"
        %(lbl,b1,ci[0],ci[1],ci[1]-ci[0],len(sub),b1>=0.85,ci[0]<=1.0<=ci[1],(ci[1]-ci[0])<=0.35,len(sub)>=120))
measure(None)                                                  # OFF = beta_c
for s in (0.45,0.50,0.55,0.60): measure(s)
