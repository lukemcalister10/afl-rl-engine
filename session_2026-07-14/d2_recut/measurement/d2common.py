# D2 re-cut — shared event / control construction.
# Reuses the PRIOR job's definitions VERBATIM (d2_measure.py / d2_refine.py) so the effect
# reproduces (-3.42 SC [-4.84,-1.95]; young -4.94, prime -1.07), then adds the gap-year
# bookkeeping that R3 (recency charge) and R4 (phantom rows) need.
# Board of record: store b0c39d78 (asserted by harness against /tmp/bor_ws).
import harness as H, numpy as np
MA=H.MA; cp=H.cp
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]

def timeline(p):
    d0=cp.debutyr(p)
    rows={x['year']:x for x in p['scoring'] if (d0-1)<x['year']}
    yrs=[x['year'] for x in p['scoring'] if (d0-1)<x['year'] and x['games']>0]
    if not yrs: return None
    tl=[]
    for y in range(min(yrs),max(yrs)+1):
        r=rows.get(y)
        tl.append((y,r['games'],r['avg']) if (r and r['games']>0) else (y,0,None))
    return tl

def age_at(p,year):
    a=cp._age_asof(p,2026)
    return (a-(2026-year)) if a is not None else None

def build_events():
    """collapse-from-established-base events, VERBATIM prior logic (+ gap_year/missed_years)."""
    events=[]
    for p in priced:
        tl=timeline(p)
        if not tl or len(tl)<3: continue
        for i,(y,gm,av) in enumerate(tl):
            prior=[(yy,g2,a2) for (yy,g2,a2) in tl[:i] if g2>=10]
            if len(prior)<2: continue
            base=np.median([g2 for _,g2,_ in prior[-3:]])
            if base<14: continue
            collapsed=(gm==0) or (gm<=0.4*base)
            if not collapsed: continue
            pre_avg=np.mean([a2 for _,_,a2 in prior[-2:]])
            ret=next(((yy,g2,a2) for (yy,g2,a2) in tl[i+1:] if g2>=10),None)
            last_played=prior[-1][0]
            events.append(dict(p=p,player=p['player'],pos=p.get('pos'),year=y,
                typ='absent' if gm==0 else 'reduced', base=base, pre_avg=pre_avg,
                age_pre=age_at(p,last_played), last_played=last_played, ret=ret,
                gap_k=(ret[0]-last_played) if ret else None))
    return events

def build_control():
    """continuous (no-absence) transitions, VERBATIM prior logic."""
    control=[]
    for p in priced:
        tl=timeline(p)
        if not tl: continue
        pl=[(y,gm,av) for (y,gm,av) in tl if gm>=10]
        for a in range(len(pl)):
            for b in range(a+1,len(pl)):
                ya,_,ava=pl[a]; yb,_,avb=pl[b]; k=yb-ya
                if not(1<=k<=4): continue
                span=[yy for (yy,gm,av) in tl if ya<yy<yb]
                if any(next((g2 for (y2,g2,a2) in tl if y2==yy),0)<10 for yy in span): continue
                ag=age_at(p,ya)
                if ag is not None: control.append((ag,k,avb-ava))
    return np.array(control)

def make_expected(control):
    def expected(age,k):
        m=(np.abs(control[:,0]-age)<=1.5)&(control[:,1]==k)
        return np.mean(control[m,2]) if m.sum()>=5 else np.nan
    return expected

def build_control_lvl():
    """continuous transitions WITH the starting level: (age, k, start_avg, davg)."""
    out=[]
    for p in priced:
        tl=timeline(p)
        if not tl: continue
        pl=[(y,gm,av) for (y,gm,av) in tl if gm>=10]
        for a in range(len(pl)):
            for b in range(a+1,len(pl)):
                ya,_,ava=pl[a]; yb,_,avb=pl[b]; k=yb-ya
                if not(1<=k<=4): continue
                span=[yy for (yy,gm,av) in tl if ya<yy<yb]
                if any(next((g2 for (y2,g2,a2) in tl if y2==yy),0)<10 for yy in span): continue
                ag=age_at(p,ya)
                if ag is not None: out.append((ag,k,ava,avb-ava))
    return np.array(out)

def fit_ctrl_model(cl):
    """Δavg ~ age + age^2 + start_avg + C(k). Returns predict(age,k,start).
    This is the mean-reversion counterfactual: a matched non-absent player at the SAME age AND level."""
    ks=sorted(set(int(x) for x in cl[:,1]))
    def design(age,k,start):
        row=[1.0,age,age*age,start]+[1.0 if int(k)==kk else 0.0 for kk in ks[1:]]
        return row
    X=np.array([design(a,k,s) for a,k,s,_ in cl]); y=cl[:,3]
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None)
    def predict(age,k,start): return float(np.dot(design(age,k,start),beta))
    return predict

def effect_rows(events,expected,ctrl_predict=None):
    """returner events with a matched control -> dict per event.
    effect     = age-only diff-in-diff (prior D2 construction, reproduces -3.42).
    effect_adj = age AND level matched (nets mean-reversion) when ctrl_predict is given."""
    out=[]
    for e in events:
        if e['ret'] is None or e['age_pre'] is None: continue
        ex=expected(e['age_pre'],e['gap_k'])
        if np.isnan(ex): continue
        raw_d=e['ret'][2]-e['pre_avg']
        rec=dict(player=e['player'],pos=e['pos'],age_pre=e['age_pre'],
            pre_avg=e['pre_avg'],gap_k=e['gap_k'],typ=e['typ'],effect=raw_d-ex,p=e['p'],
            last_played=e['last_played'],ret=e['ret'],raw_d=raw_d)
        if ctrl_predict is not None:
            rec['effect_adj']=raw_d-ctrl_predict(e['age_pre'],e['gap_k'],e['pre_avg'])
        out.append(rec)
    return out

def gap_players():
    """players with a true mid-career calendar gap after an established base (the R3/R4 population).
    Returns list of dict(p, player, pos, gaps=[years], last_played, ret_year, pre_avg, age_pre, base)."""
    out=[]
    for p in priced:
        tl=timeline(p)
        if not tl or len(tl)<3: continue
        ymap={y:(gm,av) for (y,gm,av) in tl}
        for i,(y,gm,av) in enumerate(tl):
            if gm!=0: continue                          # a true gap year (absent row)
            prior=[(yy,g2,a2) for (yy,g2,a2) in tl[:i] if g2>=10]
            if len(prior)<2: continue
            base=np.median([g2 for _,g2,_ in prior[-3:]])
            if base<14: continue
            # contiguous run of gap years starting here
            gaps=[y]; j=i+1
            while j<len(tl) and tl[j][1]==0: gaps.append(tl[j][0]); j+=1
            ret=next(((yy,g2,a2) for (yy,g2,a2) in tl[i+1:] if g2>=10),None)
            last_played=prior[-1][0]
            out.append(dict(p=p,player=p['player'],pos=p.get('pos'),gaps=gaps,
                last_played=last_played,ret=ret,base=base,
                pre_avg=np.mean([a2 for _,_,a2 in prior[-2:]]),age_pre=age_at(p,last_played)))
            break   # first mid-career gap per player
    return out

if __name__=='__main__':
    ev=build_events(); ctrl=build_control(); exp=make_expected(ctrl)
    rows=effect_rows(ev,exp); gaps=gap_players()
    print(f"events={len(ev)} control={len(ctrl)} matched-effect-rows={len(rows)} gap-players={len(gaps)}")
    print(f"mean effect={np.mean([r['effect'] for r in rows]):+.2f} (expect -3.42)")
