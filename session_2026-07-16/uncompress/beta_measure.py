#!/usr/bin/env python3
"""LEG B — FROZEN beta estimator (PLAN §7 / acceptance leg_b.beta_proven27), applied to the engine's
CURRENT price under the un-compress map at RL_UNCOMP_S (or map-off if unset => beta_c).

FROZEN (declared in the directive/PLAN before build; identical at every grid point):
  beta   = OLS slope of ln(price) on ln(realised-output)   [np.polyfit(ln o, ln p, 1)]
  sample = proven-27+ contributors: age>=27, o>0, p>0       [memo: item-131 low-runway-confound regime]
  o      = mean of the last-2 realised season avgs - REPL[pos]  (the calibrate.py o_recent2 construction)
  p      = the engine's current price ev(p) (numeraire-invariant: a scale on p shifts the intercept, not beta)
  weight = unweighted log-log OLS
  CI     = 1000-sample bootstrap percentile (seed 0, verbatim from calibrate.py:40)
Precision gates: max CI width 0.35, min effective n 120.  Prints one line: s beta ci_lo ci_hi n width.
"""
import io,contextlib,sys,os,math
import numpy as np
REPL={'MID':80.1,'GEN_DEF':78.3,'RUC':78.5,'KEY_DEF':68.4,'GEN_FWD':70.9,'KEY_FWD':66.8}
rng=np.random.default_rng(0)
def fit_beta(sub,nb=1000):                                      # VERBATIM from session_2026-07-15/book_calibration/calibrate.py:40
    if len(sub)<8: return None,None,None
    x=np.array([math.log(p['o']) for p in sub]); y=np.array([math.log(p['p']) for p in sub])
    b1,b0=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(sub),len(sub))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    return b1,b0,tuple(np.percentile(bs,[2.5,97.5]))
def main():
    g={}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA=g['MA']; ev=g['ev']; MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()
    age=MA.age; gfut=MA.gfut; delisted=g['delisted']; _isreal=g['_isreal']
    sub=[]; c_age=c_pos=c_rows=c_o=c_p=0
    for p in MA.data:
        MA.BASE_REF=MA.AGE_REF=2026                              # force the present clock before each read (module load / an ev() call can leave it at a historical V0-build year)
        if not _isreal(p) or delisted(p) or p.get('_retired'): continue
        a=age(p)
        if a is None or a<27: continue                          # proven-27+ (memo item-131 regime)
        c_age+=1
        pos=gfut(p)
        if pos not in REPL: continue
        c_pos+=1
        rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>0 and x.get('avg',0)>0])
        if not rows: continue
        c_rows+=1
        o=sum(v for _,v in rows[-2:])/len(rows[-2:])-REPL[pos]   # o_recent2 above replacement
        with contextlib.redirect_stdout(io.StringIO()): pr=ev(p)
        if o>0: c_o+=1
        if pr and pr>0: c_p+=1
        if o>0 and pr and pr>0: sub.append({'o':o,'p':float(pr)})
    _ages=sorted(age(p) for p in MA.data if _isreal(p) and not delisted(p) and not p.get('_retired') and age(p) is not None)
    sys.stderr.write("DIAG AGE_REF=%s BASE_REF=%s | ages n=%d min=%s max=%s | age>=27:%d pos:%d rows:%d o>0:%d p>0:%d -> sub:%d\n"
        %(MA.AGE_REF,MA.BASE_REF,len(_ages),_ages[0] if _ages else None,_ages[-1] if _ages else None,c_age,c_pos,c_rows,c_o,c_p,len(sub)))
    b1,b0,ci=fit_beta(sub)
    s=os.environ.get('RL_UNCOMP_S','OFF')
    if b1 is None:
        sys.stderr.write("s=%s  beta=NA (n=%d < 8)\n"%(s,len(sub))); return
    width=ci[1]-ci[0]
    sys.stderr.write("s=%-5s beta=%.4f  CI=[%.4f,%.4f] width=%.4f  n=%d  | pt>=0.85:%s  CI_contains_1.0:%s  width<=0.35:%s  n>=120:%s\n"
        %(s,b1,ci[0],ci[1],width,len(sub), b1>=0.85, ci[0]<=1.0<=ci[1], width<=0.35, len(sub)>=120))
if __name__=='__main__': main()
