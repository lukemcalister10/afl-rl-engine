#!/usr/bin/env python3
"""Form-conditioned aging measurement (T3, read-only). Re-derives everything from the committed store at
base 9be07b8e (store b1fd0bce). Follows PLAN.md.

LEVEL BASIS (PLAN refinement, declared): the demonstrated level is the engine's own recency-weighted
current level Lc = _lvlcurr replica (VALIDATED: Heeney@2025 = 109.5, exactly the engine's stated 'playing
109.5', item 128). Both the conditioning (sustained flat-or-rising) and the decline event use Lc, so a
single-season spike cannot masquerade as 'rising' and then mean-revert (the naive single-season cut, which
inverts the sign via regression-to-the-mean, is reported as a caveat in the FINDING).

Age convention matches the engine (_age_at: age = year - _by). No engine import; all re-derived.
"""
import json, os, math, statistics as st, csv, hashlib, random
from collections import defaultdict, Counter
random.seed(12345)

HERE=os.path.dirname(os.path.abspath(__file__))
OUT=HERE
BASE_COMMIT="9be07b8e5939eeade71106ef1eaee112df183441"   # chapter final head (STRICT)
STORE_PATH_IN_REPO="engine/rl_after/rl_model_data.json"
STORE_MD5="b1fd0bced30baa838325814c39d43233"             # Guard 5 pin

def load_store_bytes():
    """Read the base store from a local byte-copy if present, else from git history (self-contained,
    reproducible from the permanent base commit). md5 is asserted either way."""
    import subprocess, hashlib
    local=os.path.join(HERE,"base_store_rl_model_data.json")
    if os.path.exists(local):
        b=open(local,'rb').read()
    else:
        repo=os.path.abspath(os.path.join(HERE,"..",".."))
        b=subprocess.check_output(["git","-C",repo,"show",f"{BASE_COMMIT}:{STORE_PATH_IN_REPO}"])
    md5=hashlib.md5(b).hexdigest()
    assert md5==STORE_MD5, f"STORE MISMATCH {md5} != {STORE_MD5}"
    return b, md5
LAST_COMPLETE=2025            # 2026 is partial (mid-July 2026); transitions need t+1<=2025
AGES=list(range(29,37))

# ---- engine age-path constants (overlay only) ----
import numpy as np
AGEMULT_X=[20,22,25,28,30,32,34,37]; AGEMULT_Y=[0.92,0.89,0.85,0.79,0.73,0.68,0.62,0.55]
def agemult(a): return float(np.clip(np.interp(a,AGEMULT_X,AGEMULT_Y),0.53,0.95))
SAGE_X=[20,21,22,23,24,25,26,27,28,29,30,31]
SAGE_Y=[0.915376,0.860795,0.789170,0.700837,0.599107,0.489589,0.377802,0.265858,0.150620,0.3793,0.0,0.0]
def s_age(a): return float(np.clip(np.interp(a,SAGE_X,SAGE_Y),0.0,1.0))
REPL={'MID':80.1,'GDEF':78.3,'RUC':78.5,'KDEF':68.4,'GFWD':70.9,'KFWD':66.8,'DEF':78.3}
LDECAY={'KEY':0.40,'GEN':0.35,'MR':0.225}
def ldg(pos):
    if pos in ('KFWD','KDEF'): return 'KEY'
    if pos in ('GFWD','GDEF','DEF'): return 'GEN'
    return 'MR'   # MID, RUC

_STORE_BYTES,_STORE_MD5=load_store_bytes()
players=json.loads(_STORE_BYTES)
def by(p): return p.get('_by')
def pos_of(p): return p.get('future_position') or p.get('present_position') or p.get('drafted_position')
def repl_for(p): return REPL.get(pos_of(p),75.0)
def wg(g): return g*g/(g+5.8)
def age_of(p,y):
    b=by(p); return (y-b) if b is not None else None
def all_years(p): return sorted({x['year'] for x in (p.get('scoring') or [])})
def still_active(p):
    ay=all_years(p); return bool(p.get('_has26')) or (ay and max(ay)>=2026)

def lvlcurr(p,Y):
    """engine _lvlcurr replica (validated). recency-weighted demonstrated CURRENT level through Y."""
    ld=LDECAY[ldg(pos_of(p))]
    rows=[(x['year'],x['games'],x['avg']) for x in p['scoring'] if x['games']>0 and x['year']<=Y]
    tw=sum(wg(g)*ld**(Y-yr) for yr,g,_ in rows)
    return (sum(wg(g)*ld**(Y-yr)*a for yr,g,a in rows)/tw) if tw>0 else None

def banked(p,Y,gq):
    """transparent banked record: games-weighted mean of qualifying seasons <=Y (NO recency decay).
    Declared re-derivation of the engine's Lo; runs a few pts below _lvl_eff_orig (includes early years)."""
    rows=[(x['games'],x['avg']) for x in p['scoring'] if x['games']>=gq and x['year']<=Y]
    tw=sum(wg(g) for g,_ in rows); return (sum(wg(g)*a for g,a in rows)/tw) if tw>0 else None

def qual_years(p,gq): return sorted({x['year'] for x in (p.get('scoring') or []) if x['games']>=gq})
def raw_avg(p,y):
    for x in p['scoring']:
        if x['year']==y and x['games']>0: return x['avg']
    return None

def pct(xs,q):
    xs=sorted(xs); k=(len(xs)-1)*q/100.0; f=math.floor(k); c=math.ceil(k)
    return xs[int(k)] if f==c else xs[f]*(c-k)+xs[c]*(k-f)
def rnd(x): return round(x,4) if isinstance(x,(int,float)) else x

# ============================ PANEL ============================
def build_panel(gq=8, eps=3.0, min_prior=3, rule='trail2', relband=False):
    recs=[]
    for p in players:
        qy=qual_years(p,gq)
        if len(qy)<min_prior+1: continue
        for i in range(min_prior,len(qy)):
            t=qy[i]
            if t>LAST_COMPLETE-1: continue
            a=age_of(p,t)
            if a is None or a<AGES[0] or a>AGES[-1]: continue
            Lc=lvlcurr(p,t); Lp1=lvlcurr(p,t-1); Lp2=lvlcurr(p,t-2)
            if Lc is None or Lp1 is None: continue
            if Lp2 is None: Lp2=Lp1
            e=(0.04*Lc if relband else eps)
            if rule=='trail2':   rising_ok = Lc>=max(Lp1,Lp2)-e
            elif rule=='last':   rising_ok = Lc>=Lp1-e
            elif rule=='peak':   rising_ok = Lc>=max(lvlcurr(p,qy[j]) for j in range(i))-e
            elif rule=='strict': rising_ok = Lc>=Lp1+e
            is_rising = Lc>Lp1+e
            nxt=t+1; has_next = nxt in qy; later=any(y>nxt for y in qy)
            Lo=banked(p,t,gq); lift=(Lc-Lo) if Lo is not None else None
            if has_next:
                Lcn=lvlcurr(p,nxt); dL=Lcn-Lc
                outcome='DECLINE' if dL<-e else 'CONTINUE'
                fwd_raw=raw_avg(p,nxt)
                sfrac=((fwd_raw-Lo)/(Lc-Lo)) if (Lo is not None and lift and lift>2.0 and fwd_raw is not None) else None
            elif later:
                outcome='GAP'; dL=None; sfrac=None; fwd_raw=None
            else:
                outcome='CENSOR_ACTIVE' if still_active(p) else 'EXIT'; dL=None; sfrac=None; fwd_raw=None
            recs.append(dict(player=p['player'],key=p.get('key'),pos=pos_of(p),year=t,age=a,Lc=Lc,Lo=Lo,
                             lift=lift,dL=dL,fwd_raw=fwd_raw,sfrac=sfrac,outcome=outcome,
                             rising_ok=rising_ok,is_rising=is_rising,
                             elite=(Lo is not None and Lc>=repl_for(p)+15)))
    return recs

def by_age(recs, conditioned=True):
    B=defaultdict(Counter); DL=defaultdict(list); SF=defaultdict(list); ELx=defaultdict(int)
    for r in recs:
        if conditioned and not r['rising_ok']: continue
        B[r['age']][r['outcome']]+=1
        if r['dL'] is not None: DL[r['age']].append(r['dL'])
        if r['sfrac'] is not None: SF[r['age']].append(r['sfrac'])
        if r['outcome']=='EXIT' and r['elite']: ELx[r['age']]+=1
    out={}
    for a in AGES:
        b=B[a]; cont=b['CONTINUE']; dec=b['DECLINE']; ex=b['EXIT']; gap=b['GAP']; cen=b['CENSOR_ACTIVE']
        played=cont+dec; up=cont+dec+ex; d=DL[a]; sf=SF[a]
        out[a]=dict(n_continue=cont,n_decline=dec,n_exit=ex,n_gap=gap,n_censor=cen,
                    n_elite_exit=ELx[a],n_played=played,
                    h_lower=(dec/played if played else None),
                    h_upper=((dec+ex)/up if up else None),
                    dL_mean=(st.mean(d) if d else None),dL_median=(st.median(d) if d else None),
                    dL_p10=(pct(d,10) if len(d)>=5 else None),dL_p90=(pct(d,90) if len(d)>=5 else None),
                    dL_p25=(pct(d,25) if len(d)>=5 else None),dL_p75=(pct(d,75) if len(d)>=5 else None),
                    s_mean=(st.mean(sf) if sf else None),n_lift=len(sf),dls=d)
    return out

def gsmooth(ages,vals,ns,h=1.5):
    pts=[(a,v,n) for a,v,n in zip(ages,vals,ns) if v is not None and n>0]; out={}
    for a in ages:
        num=den=0.0
        for aj,vj,nj in pts:
            w=math.exp(-0.5*((a-aj)/h)**2)*nj; num+=w*vj; den+=w
        out[a]=num/den if den>0 else None
    return out

def boot_ci(recs,conditioned,age,kind,reps=1000):
    byp=defaultdict(list)
    for r in recs:
        if conditioned and not r['rising_ok']: continue
        if r['age']!=age: continue
        byp[r['key']].append(r)
    keys=list(byp)
    if len(keys)<4: return (None,None)
    est=[]
    for _ in range(reps):
        flat=[r for _ in keys for r in byp[keys[random.randrange(len(keys))]]]
        cont=sum(1 for r in flat if r['outcome']=='CONTINUE'); dec=sum(1 for r in flat if r['outcome']=='DECLINE')
        ex=sum(1 for r in flat if r['outcome']=='EXIT')
        if kind=='h_lower': d=cont+dec; est.append(dec/d if d else float('nan'))
        elif kind=='h_upper': d=cont+dec+ex; est.append((dec+ex)/d if d else float('nan'))
        elif kind=='dL_mean':
            dl=[r['dL'] for r in flat if r['dL'] is not None]; est.append(st.mean(dl) if dl else float('nan'))
    est=[e for e in est if e==e]
    if len(est)<50: return (None,None)
    est.sort(); return (round(est[int(.025*len(est))],4),round(est[int(.975*len(est))],4))

def pool(d,aset):
    cont=sum(d[a]['n_continue'] for a in aset); dec=sum(d[a]['n_decline'] for a in aset)
    ex=sum(d[a]['n_exit'] for a in aset); elx=sum(d[a]['n_elite_exit'] for a in aset)
    dls=[x for a in aset for x in d[a]['dls']]; sfn=sum(d[a]['n_lift'] for a in aset)
    sfvals=[]
    return dict(n_played=cont+dec,n_continue=cont,n_decline=dec,n_exit=ex,n_elite_exit=elx,
               h_lower=rnd(dec/(cont+dec) if cont+dec else None),
               h_upper=rnd((dec+ex)/(cont+dec+ex) if cont+dec+ex else None),
               dL_mean=rnd(st.mean(dls) if dls else None),dL_median=rnd(st.median(dls) if dls else None),
               dL_p25=rnd(pct(dls,25) if len(dls)>=5 else None),dL_p75=rnd(pct(dls,75) if len(dls)>=5 else None),
               n_lift=sfn)

# ============================ MAIN ============================
def main():
    md5=_STORE_MD5
    print("store md5:",md5,"OK")
    summary={'store_md5':md5,'base':'9be07b8e','level_basis':'lvlcurr recency-weighted (validated Heeney 109.5)'}

    GQ,EPS,MINP,RULE=8,3.0,3,'trail2'
    recs=build_panel(GQ,EPS,MINP,RULE)
    cond=by_age(recs,True); unc=by_age(recs,False)
    ages=AGES
    def col(d,k): return [d[a][k] for a in ages]
    sm={
      'cond_hlo':gsmooth(ages,col(cond,'h_lower'),col(cond,'n_played')),
      'unc_hlo':gsmooth(ages,col(unc,'h_lower'),col(unc,'n_played')),
      'cond_hup':gsmooth(ages,col(cond,'h_upper'),[cond[a]['n_played']+cond[a]['n_exit'] for a in ages]),
      'unc_hup':gsmooth(ages,col(unc,'h_upper'),[unc[a]['n_played']+unc[a]['n_exit'] for a in ages]),
      'cond_dl':gsmooth(ages,col(cond,'dL_mean'),col(cond,'n_played')),
      'unc_dl':gsmooth(ages,col(unc,'dL_mean'),col(unc,'n_played')),
      'cond_s':gsmooth(ages,col(cond,'s_mean'),col(cond,'n_lift')),
    }

    # CSV 1: hazard/Δ by age
    with open(os.path.join(OUT,'hazard_by_age.csv'),'w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['age','set','n_played','n_continue','n_decline','n_exit','n_gap','n_censor_active','n_elite_exit',
                    'h_lower','h_lower_ci_lo','h_lower_ci_hi','h_lower_smoothed','h_upper','h_upper_smoothed',
                    'dL_mean','dL_mean_ci_lo','dL_mean_ci_hi','dL_mean_smoothed','dL_median','dL_p25','dL_p75',
                    'engine_agemult','engine_s_age'])
        for a in ages:
            for lab,d in [('conditioned',cond),('unconditioned',unc)]:
                r=d[a]; cf=(lab=='conditioned')
                ci=boot_ci(recs,cf,a,'h_lower'); cid=boot_ci(recs,cf,a,'dL_mean')
                w.writerow([a,lab,r['n_played'],r['n_continue'],r['n_decline'],r['n_exit'],r['n_gap'],r['n_censor'],
                    r['n_elite_exit'],rnd(r['h_lower']),ci[0],ci[1],
                    rnd(sm['cond_hlo' if cf else 'unc_hlo'][a]),rnd(r['h_upper']),
                    rnd(sm['cond_hup' if cf else 'unc_hup'][a]),
                    rnd(r['dL_mean']),cid[0],cid[1],rnd(sm['cond_dl' if cf else 'unc_dl'][a]),
                    rnd(r['dL_median']),rnd(r['dL_p25']),rnd(r['dL_p75']),
                    round(agemult(a),3),round(s_age(a),4)])

    summary['by_age']={'conditioned':{a:{k:rnd(v) for k,v in cond[a].items() if k!='dls'} for a in ages},
                       'unconditioned':{a:{k:rnd(v) for k,v in unc[a].items() if k!='dls'} for a in ages}}
    summary['smoothed']={k:{a:rnd(v[a]) for a in ages} for k,v in sm.items()}
    summary['pooled']={}
    for nm,aset in [('age29',[29]),('30-32',[30,31,32]),('33-36',[33,34,35,36]),('30plus',list(range(30,37))),('29-36',AGES)]:
        summary['pooled'][nm]={'conditioned':pool(cond,aset),'unconditioned':pool(unc,aset)}

    # CSV 2: sensitivity on 30+ pooled
    with open(os.path.join(OUT,'sensitivity.csv'),'w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['variant','value','cond30_n','cond30_h_lower','cond30_h_upper','cond30_dL_mean',
                    'unc30_h_lower','unc30_dL_mean','delta_h_lower(cond-unc)'])
        rows=[('primary','trail2/eps3/gq8/mp3')]+[('rule','last'),('rule','peak'),('rule','strict'),
              ('eps',2.0),('eps',5.0),('eps','rel4pct'),('gq',6),('gq',10),('min_prior',2),('min_prior',4)]
        summary['sensitivity']={}
        for vk,vv in rows:
            gq,eps,minp,rule,rel=GQ,EPS,MINP,RULE,False
            if vk=='rule': rule=vv
            elif vk=='eps': rel=(vv=='rel4pct'); eps=(EPS if rel else vv)
            elif vk=='gq': gq=vv
            elif vk=='min_prior': minp=vv
            rc=build_panel(gq,eps,minp,rule,rel); c=by_age(rc,True); u=by_age(rc,False)
            cp=pool(c,list(range(30,37))); up=pool(u,list(range(30,37)))
            dh=(cp['h_lower']-up['h_lower']) if (cp['h_lower'] is not None and up['h_lower'] is not None) else None
            w.writerow([vk,vv,cp['n_played'],cp['h_lower'],cp['h_upper'],cp['dL_mean'],up['h_lower'],up['dL_mean'],rnd(dh)])
            summary['sensitivity'][f'{vk}={vv}']={'cond30':cp,'unc30':up,'delta_h':rnd(dh)}

    # CSV 3: worked examples
    named={'gawn':'max-gawn','bontempelli':'marcus-bontempelli','english':'timothy-english',
           'heeney':'isaac-heeney','dale':'bailey-dale'}
    with open(os.path.join(OUT,'worked_examples.csv'),'w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['player','pos','_by','season','age','games','raw_avg','Lc_demonstrated','qualifying',
                    'flat_or_rising_here','cond_h_lower_smoothed','cond_dL_mean_smoothed','engine_s_age','note'])
        summary['worked']={}
        for short,key in named.items():
            p=[x for x in players if x.get('key')==key]
            if not p: summary['worked'][short]='NOT FOUND'; continue
            p=p[0]; summary['worked'][short]=p['player']; qy=set(qual_years(p,GQ)); traj=[]
            for x in sorted(p['scoring'],key=lambda z:z['year']):
                yr=x['year']; a=age_of(p,yr); q=x['games']>=GQ; Lc=lvlcurr(p,yr)
                partial=(yr==2026)
                fr=''
                if q and yr<=LAST_COMPLETE-1 and a in AGES:
                    qys=sorted(qy);
                    if yr in qys and qys.index(yr)>=MINP:
                        Lp1=lvlcurr(p,yr-1); Lp2=lvlcurr(p,yr-2) or Lp1
                        fr='RISING' if Lc>Lp1+EPS else ('FLAT/UP' if Lc>=max(Lp1,Lp2)-EPS else 'declining')
                hlo=sm['cond_hlo'].get(a) if a in AGES else None
                dlm=sm['cond_dl'].get(a) if a in AGES else None
                note='partial 2026 (right-censored; so-far only)' if partial else ('below qual bar' if not q else '')
                w.writerow([p['player'],pos_of(p),by(p),yr,a,x['games'],x['avg'],rnd(Lc),int(q),fr,
                            rnd(hlo),rnd(dlm),rnd(s_age(a) if a is not None else None),note])
                traj.append(dict(year=yr,age=a,raw=x['avg'],Lc=rnd(Lc),games=x['games'],qual=q,fr=fr,partial=partial))
            summary['worked'][short+'_traj']=traj

    summary['engine']={'agemult':{a:round(agemult(a),3) for a in ages},
                       's_age':{a:round(s_age(a),4) for a in ages}}
    json.dump(summary,open(os.path.join(OUT,'summary.json'),'w'),indent=1,default=str)
    print("WROTE hazard_by_age.csv sensitivity.csv worked_examples.csv summary.json")

if __name__=='__main__': main()
