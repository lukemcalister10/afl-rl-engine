#!/usr/bin/env python3
"""LEG B SEGMENT-4 — λ PRE-GATE DIAGNOSTIC (decision support for the HALT, NOT a lever pulled).
The v1.2 law (games×recency, d=0.5) measured λ=0.8086 < 0.95 (HALT). d is the memo's owner-tunable
checkpoint lever. This sweeps λ_ρ(d) and two horizon variants so the owner can rule at the checkpoint.
Same PINNED frozen fit_beta harness + same sample law as rho_axis_v12.py. Writes NOTHING to store/engine/board."""
import io,contextlib,sys,math,json
import numpy as np
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; delisted=g['delisted']; _isreal=g['_isreal']
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
POP=[]
for p in MA.data:
    if not _isreal(p) or delisted(p) or p.get('_retired'): continue
    if MA.gfut(p) not in REPL or MA.age(p) is None: continue
    POP.append(p)
def rho_gxr(p,pos,d,cap=None):
    """games×recency over all games>0 seasons; cap=None all seasons, cap=k -> only the k most-recent games>0 seasons."""
    rows=[(x['year'],x['avg'],x.get('games',0) or 0) for x in p['scoring'] if (x.get('games',0) or 0)>0]
    if not rows: return None
    rows.sort()
    if cap is not None: rows=rows[-cap:]
    num=0.0; den=0.0
    for yr,av,gm in rows:
        u=gm*(d**(YNOW-yr)); num+=u*(av-REPL[pos]); den+=u
    return None if den<=0.0 else num/den
def measure(rho_fn):
    O=[];R=[]
    for p in POP:
        a=MA.age(p)
        if a is None or a<27: continue
        pos=MA.gfut(p)
        rows=sorted([(x['year'],x['avg']) for x in p['scoring'] if x.get('games',0)>0 and x.get('avg',0)>0])
        if not rows: continue
        o=sum(a2 for _,a2 in rows[-2:])/len(rows[-2:])-REPL[pos]
        r=rho_fn(p,pos); ln=MA.level_now(p)
        if o>0 and r and r>0 and ln and ln>0: O.append(o); R.append(r)
    b,lo,hi=fit_beta(O,R); return b,lo,hi,len(O)
out={'gate':0.95,'sweep_all_seasons':{},'horizon_cap_recent2':{},'horizon_cap_recent3':{}}
sys.stderr.write("=== λ_ρ(d) — games×recency, ALL games>0 seasons (the v1.2 law; d=0.5 is THE construction) ===\n")
for d in (0.30,0.40,0.50,0.60,0.72):
    b,lo,hi,n=measure(lambda p,pos,dd=d: rho_gxr(p,pos,dd))
    out['sweep_all_seasons']['d=%.2f'%d]={'lambda':round(b,4),'ci':[round(lo,4),round(hi,4)],'n':n}
    sys.stderr.write("  d=%.2f : λ=%.4f CI=[%.4f,%.4f] n=%d %s\n"%(d,b,lo,hi,n,'>=gate' if b>=0.95 else '< gate'))
sys.stderr.write("=== λ_ρ(d) — games×recency, RECENT-2 games>0 seasons only (horizon-capped) ===\n")
for d in (0.30,0.50,0.72):
    b,lo,hi,n=measure(lambda p,pos,dd=d: rho_gxr(p,pos,dd,cap=2))
    out['horizon_cap_recent2']['d=%.2f'%d]={'lambda':round(b,4),'ci':[round(lo,4),round(hi,4)],'n':n}
    sys.stderr.write("  d=%.2f cap2 : λ=%.4f CI=[%.4f,%.4f] n=%d %s\n"%(d,b,lo,hi,n,'>=gate' if b>=0.95 else '< gate'))
sys.stderr.write("=== λ_ρ(d) — games×recency, RECENT-3 games>0 seasons only ===\n")
for d in (0.50,0.72):
    b,lo,hi,n=measure(lambda p,pos,dd=d: rho_gxr(p,pos,dd,cap=3))
    out['horizon_cap_recent3']['d=%.2f'%d]={'lambda':round(b,4),'ci':[round(lo,4),round(hi,4)],'n':n}
    sys.stderr.write("  d=%.2f cap3 : λ=%.4f CI=[%.4f,%.4f] n=%d %s\n"%(d,b,lo,hi,n,'>=gate' if b>=0.95 else '< gate'))
print(json.dumps(out,indent=1))
