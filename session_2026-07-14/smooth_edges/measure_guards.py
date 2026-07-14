import sys; sys.path.insert(0,'/tmp/smooth')
import load; sys.path.insert(0,'/tmp/smooth')
import overlay, io, contextlib, copy, numpy as np, json
G=load.G; MA=G['MA']; ev=G['ev']; cp=G['cp']; F=1.0524
def num_p(p): return round(ev(p)/F)
def byname(nm):
    c=[p for p in MA.data if p['player']==nm]
    return c[0] if c else None
def bykey(k):
    c=[p for p in MA.data if p.get('key')==k]
    return c[0] if c else None

# ---- walk-forward cohort (G-COHORT) ----
def draft_year(p): return p.get('year')
def cum_games(p,Y): return sum(x.get('games',0) for x in p['scoring'] if x['year']<=Y)
def value_asof(p,t):
    D=draft_year(p); Yt=D+t; q=copy.deepcopy(p)
    q['scoring']=[x for x in q['scoring'] if x['year']<=Yt]; q['_pos_now']=None; q['_fut']=[]
    MA.BASE_REF=MA.AGE_REF=Yt; MA._pe_clear()
    if cum_games(p,Yt)==0 and t>=3: return 0.0
    with contextlib.redirect_stdout(io.StringIO()): return float(ev(q,Yt))
CLASSES=list(range(2014,2021))
by_class={Y:[p for p in MA.data if p.get('type')=='ND' and p.get('pick') and draft_year(p)==Y] for Y in CLASSES}
def cohort_gate():
    cs={Y:{} for Y in CLASSES}
    for Y in CLASSES:
        for t in range(1,7):
            if Y+t<=2026: cs[Y][t]=sum(value_asof(p,t) for p in by_class[Y])
    avg={t:float(np.mean([cs[Y][t] for Y in CLASSES if t in cs[Y]])) for t in range(1,7)}
    denom=min(avg[1],avg[2]); ratios={t:avg[t]/denom for t in (4,5,6)}
    MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()   # restore
    return {'avg':{t:round(avg[t],1) for t in avg},'denom':round(denom,1),
            'ratios':{t:round(ratios[t]*100,1) for t in (4,5,6)},'breach':any(ratios[t]>1.30 for t in (4,5,6))}
def gy0_chain():
    # y0->y1->y2 shape over in-curve ND classes 2014-2020 (walk-forward)
    y1=float(np.mean([cs for Y in CLASSES for cs in [value_asof(p,1) for p in by_class[Y]] ]))
    # simpler: mean per-player t1 and t2
    t1=[value_asof(p,1) for Y in CLASSES for p in by_class[Y] if Y+1<=2026]
    t2=[value_asof(p,2) for Y in CLASSES for p in by_class[Y] if Y+2<=2026]
    MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()
    return {'y1_mean':round(float(np.mean(t1)),1),'y2_mean':round(float(np.mean(t2)),1),'y2_gt_y1':float(np.mean(t2))>float(np.mean(t1))}

# ---- G-FLOOR (B5) ----
B5={1:0.45,2:0.35,3:0.28,4:0.21,5:0.13,6:0.09}
def draftval(p):
    try: return MA.PVC[min(p['pick'],99)]
    except Exception: return None
def floor_breaches():
    out=[]
    for p in MA.data:
        if not G['_isreal'](p): continue
        if p.get('type')!='ND' or not p.get('pick') or p.get('_retired'): continue
        yis=2026-int(p['year'])
        if yis<1: continue
        dv=draftval(p)
        if dv is None: continue
        fl=B5.get(yis,0.05)*dv
        if ev(p,2026)<fl: out.append((p['player'],round(ev(p)/F),round(fl/F)))
    return out

# ---- G-CONVEX young band aggregates (numeraire) ----
def convex_bands():
    bands={'<=21':(0,21),'22-24':(22,24),'25-26':(25,26)}
    agg={}
    for nm,(lo,hi) in bands.items():
        s=0
        for p in MA.data:
            if not G['_isreal'](p): continue
            a=cp._age_asof(p,2026)
            if a is None: continue
            if lo<=a<=hi: s+=num_p(p)
        agg[nm]=s
    return agg

NAMED={'bont':'Marcus Bontempelli','reid':'Harley Reid','sanders':'Ryley Sanders',
       'duursma':'Willem Duursma','zeke':'Zeke Uwland','butters':'Zak Butters','holmes':'Max Holmes'}
def named_vals():
    d={}
    for k,nm in NAMED.items():
        p=byname(nm); d[k]=num_p(p) if p else None
    return d

def run(label):
    r={'label':label}
    r['named']=named_vals()
    r['floor_breaches']=floor_breaches()
    r['convex']=convex_bands()
    r['cohort']=cohort_gate()
    r['gy0']=gy0_chain()
    return r

RES={}
for name,cfg in [('BASE',{'f1':False,'f2':False,'f3':False}),('F1+F2+F3',{'f1':True,'f2':True,'f3':True})]:
    overlay.apply(G,cfg)
    RES[name]=run(name)
    print('done',name)
overlay.apply(G,{'f1':False,'f2':False,'f3':False})
json.dump(RES,open('/tmp/smooth/guards.json','w'),indent=1)
print('GUARDS_DONE')
