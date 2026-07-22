#!/usr/bin/env python3
"""LEG B SEGMENT-4 — THE λ PRE-GATE (directive step 0). Measure λ_ρ of the v1.2 games×recency ρ
construction (memo §2.1 ⟪v1.2⟫ WEIGHT-DON'T-GATE) with the PINNED frozen fit_beta harness, same
sample law as session_2026-07-16/qualifying_diag/scripts/measure.py::measure3 (produced m3_lambda.json).

FROZEN (byte-identical to the pinned harness):
  - fit_beta: OLS log-log slope + 1000-boot percentile CI, np.random.default_rng(0) fresh per fit.
  - POP: real / not delisted / not _retired / gfut in REPL / age not None.
  - proven-27+ sample; o = recent-2 games>0 avg above REPL[pos] (the estimator's o-construction).
  - per-variant gate: o>0 and rho>0 and level_now>0.
NEW variant only: v12_gxr = games×recency ρ_num (the LAW). floor6/floor10 are re-run to PROVE the
harness reproduces the pinned m3_lambda.json (floor6=0.9942 n=114, floor10=0.8957 n=112) on this store.
CROSS-CHECK: v12_gxr rho == engine rho_out(p,pos) for every sampled player (harness formula == shipped code).
Writes NOTHING to store/engine/board/docs. Engine loaded exactly as the pinned harness (exec _merged_recover.py)."""
import io,contextlib,sys,math,json
import numpy as np

# ---- load the engine (v1.2), exactly as the pinned harness ----
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; delisted=g['delisted']; _isreal=g['_isreal']
eng_rho_out=g['rho_out']                     # the SHIPPED v1.2 rho_out (for the cross-check)
MA.BASE_REF=MA.AGE_REF=2026
REPL=dict(MA.REPL)
DECAY=float(MA.UNCOMP_DECAY)                  # =0.5, declared next to Δ=6.0 (rl_model.py)
YNOW=2026

def fit_beta(x_,y_,nb=1000):
    rng=np.random.default_rng(0)             # fresh per fit -> mutually comparable variants; point est is rng-independent
    x=np.array([math.log(v) for v in x_]); y=np.array([math.log(v) for v in y_])
    b1,_=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(x),len(x))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    lo,hi=np.percentile(bs,[2.5,97.5]); return b1,lo,hi

# ---- population (measure.py POP) ----
POP=[]
for p in MA.data:
    if not _isreal(p) or delisted(p) or p.get('_retired'): continue
    pos=MA.gfut(p)
    if pos not in REPL: continue
    if MA.age(p) is None: continue
    POP.append(p)

# ---- rho constructions ----
def rho_floor(p,pos,F):                       # v1.1 family: recent-2 QUALIFYING-season avg above REPL (games>=F)
    rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>=F and x.get('avg',0)>0])
    if not rows: return None
    return sum(a for _,a in rows[-2:])/len(rows[-2:])-REPL[pos]

def rho_v12(p,pos):                            # THE LAW (memo §2.1 ⟪v1.2⟫): games×recency, ALL games>0, no exclusion
    num=0.0; den=0.0
    for x in p['scoring']:
        gm=x.get('games',0) or 0
        if gm<=0: continue
        u=gm*(DECAY**(YNOW-x['year']))
        num+=u*(x['avg']-REPL[pos]); den+=u
    if den<=0.0: return None
    return num/den

VARIANTS=[('floor10 (v1.1, games>=10)',lambda p,pos:rho_floor(p,pos,10),0.8957,112),
          ('floor6  (v1.1, games>=6)', lambda p,pos:rho_floor(p,pos,6), 0.9942,114),
          ('v12_gxr (THE LAW: games×recency d=%.2f)'%DECAY, rho_v12, None,None)]

res={}; xchk_max=0.0; xchk_n=0
for lbl,rho_fn,exp_l,exp_n in VARIANTS:
    O=[];R=[]
    for p in POP:
        a=MA.age(p)
        if a is None or a<27: continue
        pos=MA.gfut(p)
        rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>0 and x.get('avg',0)>0])
        if not rows: continue
        o=sum(a2 for _,a2 in rows[-2:])/len(rows[-2:])-REPL[pos]
        r=rho_fn(p,pos); ln=MA.level_now(p)
        if o>0 and r and r>0 and ln and ln>0:
            O.append(o); R.append(r)
            if rho_fn is rho_v12:              # cross-check the LAW variant against the SHIPPED engine rho_out
                er=eng_rho_out(p,pos)
                if er is not None:
                    xchk_max=max(xchk_max,abs(er-r)); xchk_n+=1
    b,lo,hi=fit_beta(O,R)
    res[lbl]={'lambda':round(b,4),'ci':[round(lo,4),round(hi,4)],'n':len(O),'expect':exp_l,'expect_n':exp_n}
    tag=''
    if exp_l is not None:
        tag=('  REPRO-OK' if (abs(b-exp_l)<5e-4 and len(O)==exp_n) else '  <<< REPRO MISMATCH (exp %.4f n=%d)'%(exp_l,exp_n))
    sys.stderr.write("lambda[ %-42s vs o ] = %.4f  CI=[%.4f,%.4f]  n=%d%s\n"%(lbl,b,lo,hi,len(O),tag))

sys.stderr.write("\nCROSS-CHECK  v12 harness rho_v12 == engine rho_out : max|Δ|=%.3e over n=%d sampled players  %s\n"
                 %(xchk_max, xchk_n, 'IDENTICAL' if xchk_max<1e-9 else 'DIVERGENT <<<'))
v12=[v for k,v in res.items() if k.startswith('v12_gxr')][0]
GATE=0.95
verdict='PROCEED' if v12['lambda']>=GATE else 'HALT'
sys.stderr.write("\nλ PRE-GATE (memo §2.1 step 0): λ_v12 = %.4f  vs gate %.2f  ->  %s\n"%(v12['lambda'],GATE,verdict))
print(json.dumps({'gate':GATE,'verdict':verdict,'lambda_v12':v12['lambda'],'ci_v12':v12['ci'],'n_v12':v12['n'],
                  'decay_d':DECAY,'ynow':YNOW,'xcheck_max_abs':xchk_max,'xcheck_n':xchk_n,
                  'reproduced':res,'population':len(POP)},indent=1,default=str))
