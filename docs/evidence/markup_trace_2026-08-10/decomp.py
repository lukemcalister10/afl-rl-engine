"""READ-ONLY decomposition of the year-0 -> year-1 re-pricing, per position.
Mirrors measure_g6.py's fold exactly, then re-computes raw_ev's internals with instrumentation.
"""
import os, sys, io, contextlib, json, hashlib
import numpy as np

WORKDIR = os.environ['RL_WORKDIR']
sys.path.insert(0, os.environ.get('RL_VENDOR', '/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0, '.')
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
G = {'__name__': '_s6_decomp'}
with contextlib.redirect_stdout(io.StringIO()): exec(src, G)

MA=G['MA']; cp=G['cp']; PR=G['PR']
delisted=G['delisted']; nseas_pro=G['nseas_pro']; bestlvl=G['bestlvl']
v0_start=G['v0_start']; entry_anchor=G['entry_anchor']; _sitout_cls=G['_sitout_cls']
_fEy=G['_fEy']; _prod_path=G['_prod_path']; _fa_year=G['_fa_year']
_form_anchor_clock=G['_form_anchor_clock']
b6=G['b6']; price6=G['price6']; par_pole=G['par_pole']; recover=G['recover']
iso_eff=G['iso_eff']; iso_corr=G['iso_corr']; eff_ten=G['eff_ten']; _expgate=G['_expgate']
_uncomp_prod=G['_uncomp_prod']; _v0_uncapped=G['_v0_uncapped']; _v0_raw=G['_v0_raw']
ev=G['ev']; _ev_m3=G['_ev_m3']; floor_frac=G['floor_frac']
_POLE=G['_POLE']

SCALE={'MID':1.19,'SF':0.93,'KPF':0.95,'SD':1.08,'KPD':1.05,'RUCK':1.13}

def raw_ev_parts(p, Y):
    """Byte-mirror of raw_ev (:451-466) with every term exposed."""
    _bb=b6(p,Y); pr_pre=price6(p,_bb,Y); pr=_uncomp_prod(pr_pre,p,Y,_bb)
    pos=MA.gfut(p); pk=MA.effpk(p)
    with _form_anchor_clock():
        T=min(max(PR.tenure(p,_fa_year(Y)),1),6)
        et=min(max(eff_ten(p,_fa_year(Y), PR.tenure(p,_fa_year(Y))),1),6)
        po,par=par_pole(pos,pk,T); a=MA.age(p)
        wage=0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))
        tfade=float(np.interp(et,[1,2,3,4,5,6],[1.00,0.76,0.40,0.16,0.05,0.05]))
        expgate=_expgate(p,Y)
        w=wage*tfade*expgate
    perf=cp._lvl_wt(p,Y)
    rec=recover(perf,par)
    gap=max(0.0,po-pr)
    return dict(pr=float(pr), pos=pos, pk=int(pk), T=int(T), et=float(et), po=float(po),
                pole_unscaled=float(po/SCALE.get(pos,1.0)), par=float(par), age=a,
                wage=float(wage), tfade=float(tfade), expgate=float(expgate), w=float(w),
                perf=float(perf), rec=float(rec), gap=float(gap),
                raw=float(pr+w*rec*gap), pole_credit=float(w*rec*gap))

def _min_tenure(p):
    if p.get('type')=='ND' and not p.get('_pickless'):
        pk=MA.effpk(p)
        if pk<=20: return 4
        if pk<=40: return 3
    return 2
def _debut_year(p):
    C=p.get('year')
    if C is None: return None
    return C if p.get('type')=='MSD' else C+1
def _listed_through(p,lastscore):
    LL=p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d=_debut_year(p)
    return max((d+_min_tenure(p)-1) if d is not None else 0, lastscore)

def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
FORCE={'thomas-boyd','paddy-mccartin'}
players=[p for p in MA.data if eligible(p) and p.get('key') not in FORCE]

TARGET=json.load(open(os.environ['RL_S6']))
LEG={(r['key'],r['C']):r for r in TARGET
     if r['nd'] and r['pk']<=64 and 2004<=r['C']<=2022 and r['N']==1}
years=sorted(set(C+1 for (_k,C) in LEG))

OUT=[]
for Y in years:
    saved={}
    for p in players:
        if (p.get('year') or 9999)>Y: continue
        lastscore=max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)]=(p['scoring'],p.get('_retired'),p.get('_last_listed'))
        p['scoring']=[r for r in p['scoring'] if r['year']<=Y]
        eff_last=_listed_through(p,lastscore)
        p['_retired']=False
        p['_last_listed']=eff_last if (eff_last is not None and eff_last<Y) else None
    MA.BASE_REF=Y; MA.AGE_REF=Y; MA._pe_clear()
    for p in players:
        C=p.get('year')
        if C is None or C+1!=Y: continue
        if (p.get('key'),C) not in LEG: continue
        try:
            if delisted(p): continue
            if nseas_pro(p,Y)<1: continue
            # --- measure_g6.py's exact call sequence, so `e` reproduces s6_rows byte-for-byte ---
            fe=_fEy(Y,p)
            with _form_anchor_clock(): el=PR.tenure(p,_fa_year(Y))
            _par=PR.par_at_p(p,MA.gfut(p),min(MA.effpk(p),cp.KMAX),min(max(el,1),6),_fa_year(Y))
            _pr=bestlvl(p,Y)/max(1,_par)
            with contextlib.redirect_stdout(io.StringIO()):
                e1=_prod_path(p,Y)
            # --- instrumentation (after; cannot move `e`) ---
            with contextlib.redirect_stdout(io.StringIO()):
                A1=raw_ev_parts(p,Y)
                iso1=iso_eff(p,Y)
                ev1=float(_ev_m3(p,Y))
                evf=float(ev(p,Y))
                # ---- the year-ZERO leg, exactly as _v0_uncapped builds it
                Y0=cp.debutyr(p)-1
                gcm,gq=G['cm'],G['q97m']
                G['cm'],G['q97m']=G['_V0_CM'],G['_V0_Q97']
                try:
                    A0=raw_ev_parts(p,Y0)
                    iso0=iso_eff(p,Y0)
                finally:
                    G['cm'],G['q97m']=gcm,gq
                v0u=float(_v0_uncapped(p)); v0r=float(_v0_raw(p)); v0=float(v0_start(p))
        except Exception as ex:
            print('SKIP',p.get('key'),repr(ex)); continue
        r=LEG[(p.get('key'),C)]
        OUT.append(dict(key=p['key'], C=C, Y=Y, pos=A1['pos'], pk=A1['pk'],
                        age=r['age'], sa=r['sa'], gcum=r['gcum'],
                        s6_price=r['price'], s6_v0=r['v0'], s6_e=r['e'], s6_F=r['F'],
                        y0={**A0,'iso':float(iso0)}, y1={**A1,'iso':float(iso1)},
                        v0u=v0u, v0r=v0r, v0=v0, e1=float(e1), ev_m3=ev1, ev_full=evf,
                        floor1=float(floor_frac(1)*entry_anchor(p))))
    for p in players:
        if id(p) in saved: p['scoring'],p['_retired'],p['_last_listed']=saved[id(p)]
    MA._pe_clear()

json.dump(OUT, open(os.environ['RL_OUT'],'w'))
print('rows', len(OUT))
# sanity: reproduce s6 v0 and e
dv=[abs(x['v0']-x['s6_v0']) for x in OUT]; de=[abs(x['e1']-x['s6_e']) for x in OUT]
print('max |v0 - s6_v0| = %.6f   max |e1 - s6_e| = %.6f' % (max(dv), max(de)))
