#!/usr/bin/env python3
# F2 empirical: engine ev vs book-path (double-v7) ev, divergent panel. READ-ONLY.
import io,contextlib,json,numpy as np
# ---- CLEAN engine ----
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']
def find(nm,yr=None,pk=None):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))
       and (yr is None or p.get('year')==yr) and (pk is None or p.get('pick')==pk)]
    return c[0] if c else None
PANEL=[('Josh Ward',2021,None),('Christian Petracca',2014,2),('Nick Daicos',2021,4),
       ('Harry Sheezel',2022,3),('Harley Reid',2023,None),('Marcus Bontempelli',2013,None)]
clean={}
with contextlib.redirect_stdout(io.StringIO()):
    for nm,yr,pk in PANEL:
        p=find(nm,yr,pk); clean[nm]=(ev(p,2026),id(p)) if p else (None,None)

# ---- BOOK-PATH: apply the s4_matrix_M1v7 injection to the SAME namespace ----
# replicate lines 24-58 of s4_matrix_M1v7.py: define book _v7 (cB+asc) and rebind g['b6']
cp=g['cp']; b6_orig=g['b6']; _lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; PROVEN_N=g['PROVEN_N']
DOWN_TOL=g['DOWN_TOL']; _agemult=g['_agemult']; _par_prior=g['_par_prior']; _upS=g['_upS']; _eo=g['_eo']
TOL_M1=5.0; G_ADQ=12; WIN=2; S_M1=0.46; GCAP=17.0
def _radq(p,Y,Lo): return any(x['games']>=G_ADQ and x['avg']>Lo for x in p['scoring'] if Y-WIN<x['year']<=Y and (cp.debutyr(p)-1)<x['year'])
def _coreM1(p,Y):
    Lo=cp._lvl_eff_orig(p,Y); n=_nqual(p,Y)
    if n==0: return Lo
    Lc=_lvlcurr(p,Y)
    if n>=PROVEN_N:
        if Lc>=Lo: return (Lo+S_M1*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo
        drop=Lo-Lc
        if drop<=DOWN_TOL: return Lo
        sw=float(np.clip((drop-DOWN_TOL)/5,0,1)); return (1-sw)*Lo+sw*Lc*_agemult(cp._age_asof(p,Y))
    c=n/PROVEN_N; return c*Lc+(1-c)*_par_prior(p,Y)
def _inferM1(p,Y):
    L0=_coreM1(p,Y); eo=_eo(p,Y)
    if eo<=0: return L0
    avs=[x['avg'] for x in p['scoring'] if x.get('games',0)>=6 and (cp.debutyr(p)-1)<x['year']<=Y]
    if not avs: return L0
    bar=MA.REPL.get(MA.gfut(p),0.0)-3.0; N=Y-cp.debutyr(p)+1
    return (1-eo)*L0+eo*min(L0,max(_upS(max(avs)-bar,N),_lvlcurr(p,Y)))
def _effs(p,Y): return sum(min(x['games']/GCAP,1.0) for x in p['scoring'] if x['games']>=6 and (cp.debutyr(p)-1)<x['year']<=Y)
def _v7book(bb,p,Y):
    bb=list(bb); m=bb[2]; a=cp._age_asof(p,Y); cB=0.47*float(np.clip((_effs(p,Y)-1)/3,0,1))
    asc=float(np.interp(a,[20,22,24,27],[1.0,0.76,0.58,0.40]))
    bb[3]=m+(1-cB)*(bb[3]-m); bb[4]=m+(1-cB)*(bb[4]-m); bb[5]=m+asc*(bb[5]-m); return bb
_REAL_book=set(id(p) for p in MA.data if MA.GRP.get(p.get('pos')))
def _b6fix(p,Y=2026):
    bb=b6_orig(p,Y)   # b6_orig already = engine's v7-wrapped b6 (asc once). This wraps AGAIN.
    if id(p) in _REAL_book:
        try: return _v7book(bb,p,Y)
        except Exception: return bb
    return bb
cp._lvl_eff=_inferM1; g['b6']=_b6fix
book={}
with contextlib.redirect_stdout(io.StringIO()):
    for nm,yr,pk in PANEL:
        p=find(nm,yr,pk); book[nm]=ev(p,2026) if p else None

print("=== F2 EMPIRICAL: engine ev(2026) vs book-path (double-v7) ev(2026) ===")
print("%-24s %8s %8s %8s"%('player','engine','book','pct'))
out={}
for nm,yr,pk in PANEL:
    e=clean[nm][0]; b=book[nm]
    pc=(b-e)/e*100 if (e and b) else None
    print("%-24s %8s %8s %+7.1f%%"%(nm, e, b, pc if pc is not None else 0))
    out[nm]={'engine':e,'book':b,'pct':pc}
json.dump(out,open('/home/user/afl-rl-engine/evidence/f1_probe/f2_result.json','w'),indent=2)
print("\nwrote f2_result.json")
