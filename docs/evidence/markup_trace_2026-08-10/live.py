import os,sys,io,contextlib,json
import numpy as np
WORKDIR=os.environ['RL_WORKDIR']; sys.path.insert(0,os.environ.get('RL_VENDOR','/home/claude/rl_vendor'))
os.chdir(WORKDIR); sys.path.insert(0,'.')
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
G={'__name__':'_live'}
with contextlib.redirect_stdout(io.StringIO()): exec(src,G)
MA=G['MA']; cp=G['cp']; PR=G['PR']
ev=G['ev']; v0_start=G['v0_start']; _v0_uncapped=G['_v0_uncapped']; _v0_raw=G['_v0_raw']
_isreal=G['_isreal']; delisted=G['delisted']; nseas_pro=G['nseas_pro']
_prod_path=G['_prod_path']; _expgate=G['_expgate']; par_pole=G['par_pole']
eff_ten=G['eff_ten']; recover=G['recover']; iso_eff=G['iso_eff']
_fa_year=G['_fa_year']; _form_anchor_clock=G['_form_anchor_clock']
b6=G['b6']; price6=G['price6']; _uncomp_prod=G['_uncomp_prod']
SCALE={'MID':1.19,'SF':0.93,'KPF':0.95,'SD':1.08,'KPD':1.05,'RUCK':1.13}
Y=2026
rows=[]
for p in MA.data:
    if not _isreal(p): continue
    C=p.get('year')
    if C is None or not (2021<=C<=2025): continue
    if p.get('type')!='ND' or p.get('pick') is None: continue
    if delisted(p) or p.get('_retired'): continue
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            pos=MA.gfut(p); pk=int(MA.effpk(p))
            v0=float(v0_start(p)); v0u=float(_v0_uncapped(p)); v0r=float(_v0_raw(p))
            price=float(ev(p,Y)); e=float(_prod_path(p,Y))
            ns=nseas_pro(p,Y)
            g=sum(x['games'] for x in p['scoring'])
            sa=[(x['year'],x['games'],x['avg']) for x in p['scoring']]
            ag=cp._age_asof(p,C)
            eg=_expgate(p,Y)
            with _form_anchor_clock():
                T=min(max(PR.tenure(p,_fa_year(Y)),1),6)
                po,par=par_pole(pos,pk,T)
                et=min(max(eff_ten(p,_fa_year(Y),PR.tenure(p,_fa_year(Y))),1),6)
            a=MA.age(p); wage=0.0 if pos=='RUCK' else float(np.clip(1-((a or 21)-20)/6,0,1))
            tf=float(np.interp(et,[1,2,3,4,5,6],[1.00,0.76,0.40,0.16,0.05,0.05]))
            _bb=b6(p,Y); pr=_uncomp_prod(price6(p,_bb,Y),p,Y,_bb)
            perf=cp._lvl_wt(p,Y); rec=recover(perf,par); w=wage*tf*eg
            pole=w*rec*max(0.0,po-pr)
    except Exception as ex:
        continue
    rows.append(dict(key=p['key'],name=p.get('player'),C=C,N=Y-C,pos=pos,pk=pk,age=ag,
                     v0=v0,v0u=v0u,v0r=v0r,price=price,e=e,ns=ns,games=g,seasons=sa,
                     m=(v0/v0u if v0u>0 else None),prod=(price/v0u if v0u>0 else None),
                     pole=float(pole),pr=float(pr),iso=float(iso_eff(p,Y))))
json.dump(rows,open(os.environ['RL_OUT'],'w'))
print('live rows',len(rows))
