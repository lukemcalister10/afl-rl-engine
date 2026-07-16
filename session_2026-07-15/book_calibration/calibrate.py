#!/usr/bin/env python3
"""WALK-FORWARD BOOK CALIBRATION — priced vs realised, by cohort (READ-ONLY, AGE-CONDITIONED).

The pooled output->price map is confounded by age/runway: at the same realised output (~45), cur spans
2707 (Gawn, 35) to 9252 (Jackson, 25). cur is a runway-discounted STOCK of future value; realised
current output is a FLOW. So the calibration is AGE-CONDITIONED throughout (PLAN cohort grid =
draftclass x age/tenure x position). The compression (item 131) is a PROVEN-player, current-state
phenomenon (English/Briggs both late-20s; rucks carry wage=0, so age is neutralized for that pair).

Instruments:
 A. Age-conditioned output->price map + signed mispricing m (under-priced +), within age band.
 B. Peak (age-neutral) map: sustained peak output vs peak price.
 C. iso pick-band residual within age x position (item 132 mid-round trough).
 D. Young walk-forward (item 130): unconditional (incl busts) AND conditional (star-track), direct.

Base 9be07b8e (store b1fd0bce, engine fc7045d6, rl_model f79fc740, config c2d233ae, N=2649).
Method fixed by PLAN.md before these numbers. Under-priced = positive.
"""
import json, os, math, statistics, csv
import numpy as np

HERE=os.path.dirname(os.path.abspath(__file__)); OUT=os.path.join(HERE,'out')
REPL={'MID':80.1,'GEN_DEF':78.3,'RUC':78.5,'KEY_DEF':68.4,'GEN_FWD':70.9,'KEY_FWD':66.8}
ROOKIE={'MSD','SSP','UNR','IRE','PDA','PDN','PDS','PSD'}
NOW=2026; NMIN=12; rng=np.random.default_rng(0)
book=json.load(open(os.path.join(OUT,'BASE_BOOK_gate_seal-asserted.json')))
board=json.load(open(os.path.join(OUT,'board_cand_canonical.json')))
age_by_key={k:v.get('age') for k,v in board.items() if isinstance(v,dict) and v.get('age') is not None}
recs=[r for ik,r in book.items() if not ik.startswith('__')]

def delivered(r): return [(y,p) for y,p in zip(r.get('yrs') or [],r.get('Ppath') or []) if p and p>0]
def pickband(pk,pl):
    if pl or pk is None: return 'rookie/pickless'
    return '01-06' if pk<=6 else '07-12' if pk<=12 else '13-20' if pk<=20 else '21-34' if pk<=34 else '35-50' if pk<=50 else '51-70'
def ageband(a): return None if a is None else '<=22' if a<=22 else '23-26' if a<=26 else '>=27'
def gmean(xs): return math.exp(sum(math.log(x) for x in xs)/len(xs))
def boot_ci_mean(vals,nb=1000):
    if len(vals)<3: return (None,None)
    v=np.array(vals); return tuple(np.percentile([v[rng.integers(0,len(v),len(v))].mean() for _ in range(nb)],[2.5,97.5]))
def fit_beta(sub,nb=1000):
    if len(sub)<8: return None,None,None
    x=np.array([math.log(p['o']) for p in sub]); y=np.array([math.log(p['p']) for p in sub])
    b1,b0=np.polyfit(x,y,1); bs=[]
    for _ in range(nb):
        i=rng.integers(0,len(sub),len(sub))
        try: bb,_=np.polyfit(x[i],y[i],1); bs.append(bb)
        except Exception: pass
    return b1,b0,tuple(np.percentile(bs,[2.5,97.5]))

# ---------- per-player ----------
players=[]
for r in recs:
    pos=r.get('pos')
    if pos not in REPL: continue
    d=delivered(r); key=r.get('key'); age=age_by_key.get(key)
    tenure=(NOW-r['year']) if r.get('year') else None
    age_est=False
    if age is None and tenure is not None: age=18+tenure; age_est=True
    V=r.get('Vpath') or []
    rec=dict(player=r['player'],key=key,pos=pos,type=r.get('type'),pick=r.get('pick'),
             pickless=bool(r.get('pickless')),year=r.get('year'),tenure=tenure,age=age,age_est=age_est,
             cur=r.get('cur'),anchor=r.get('anchor'),draftval=r.get('draftval'),n_deliv=len(d),
             rookie=(r.get('type') in ROOKIE))
    if d:
        by=sorted(d); outs=[p for _,p in d]; rl=REPL[pos]
        rec['o_recent2']=sum(p for _,p in by[-2:])/len(by[-2:])-rl
        rec['o_top3']=sum(sorted(outs,reverse=True)[:3])/len(sorted(outs,reverse=True)[:3])-rl
        rec['o_peak']=max(outs)-rl
        rec['p_peak']=max([v for v in V if v is not None],default=None)
    rec['o']=rec.get('o_recent2'); rec['p']=rec['cur']
    players.append(rec)
contrib=[p for p in players if p.get('o') and p['o']>0 and p['p'] and p['p']>0 and p['age'] is not None]
print(f"pos-eligible={len(players)} delivered>=1={sum(1 for p in players if p['n_deliv'])} contributors(o>0,age)={len(contrib)}")

# ---------- A. AGE-CONDITIONED map + signed mispricing m ----------
bands=['<=22','23-26','>=27']
band_base={}
for b in bands:
    sub=[p for p in contrib if ageband(p['age'])==b]
    if sub: band_base[b]=(gmean([p['o'] for p in sub]),gmean([p['p'] for p in sub]),len(sub))
# m within age band (baselines per band -> runway-neutral)
for p in contrib:
    b=ageband(p['age']); ob,pb,_=band_base[b]
    p['m']=math.log(p['o']/ob)-math.log(p['p']/pb)          # under-priced +

print("\nAGE-BANDED elasticity beta (beta<1 => top compressed WITHIN band):")
band_beta={}
for b in bands:
    sub=[p for p in contrib if ageband(p['age'])==b]
    be,al,ci=fit_beta(sub); band_beta[b]=(be,al,ci,len(sub))
    if be is not None: print(f"  age {b:6s} n={len(sub):4d} beta={be:.3f} CI[{ci[0]:.3f},{ci[1]:.3f}]")
# residual vs the WITHIN-BAND fit (isolates position/pick effects from age & level)
for p in contrib:
    be,al,ci,n=band_beta[ageband(p['age'])]
    p['resid_band']=(math.log(p['p'])-(al+be*math.log(p['o']))) if be is not None else None

# proven-band deciles (the item-131 regime: age>=27, minimal runway confound)
proven=sorted([p for p in contrib if p['age']>=27],key=lambda p:p['o'])
print(f"\nPROVEN band (age>=27) n={len(proven)} — output->price by quintile (price should keep pace):")
ob,pb,_=band_base['>=27']
dec_rows=[]
Q=5
for d in range(Q):
    lo=int(d*len(proven)/Q); hi=int((d+1)*len(proven)/Q); ps=proven[lo:hi]
    if not ps: continue
    row=dict(band='>=27',quantile=f"Q{d+1}",n=len(ps),out_lo=round(ps[0]['o'],1),out_hi=round(ps[-1]['o'],1),
             output_mult=round(gmean([p['o'] for p in ps])/ob,3),price_mult=round(gmean([p['p'] for p in ps])/pb,3),
             mean_m=round(statistics.mean([p['m'] for p in ps]),3))
    dec_rows.append(row); print(f"  Q{d+1} n={len(ps):2d} out={row['out_lo']:.0f}..{row['out_hi']:.0f} omul={row['output_mult']:.2f} pmul={row['price_mult']:.2f} m={row['mean_m']:+.2f}")

# ---------- B. PEAK (age-neutral) map ----------
peakpop=[p for p in players if p.get('o_top3') and p['o_top3']>0 and p.get('p_peak') and p['p_peak']>0]
pk=[{'o':p['o_top3'],'p':p['p_peak'],'pos':p['pos']} for p in peakpop]
bpk,apk,cipk=fit_beta(pk)
print(f"\nPEAK map (age-neutral: sustained-peak output vs peak price) n={len(pk)} beta={bpk:.3f} CI[{cipk[0]:.3f},{cipk[1]:.3f}]")

# ---------- signed mispricing SURFACE (age-conditioned m) ----------
def cell_rows(groupfn,label):
    cells={}
    for p in contrib:
        g=groupfn(p)
        if g is not None: cells.setdefault(g,[]).append(p)
    rows=[]
    for g,ps in sorted(cells.items(),key=lambda kv:str(kv[0])):
        ms=[p['m'] for p in ps]; lo,hi=boot_ci_mean(ms)
        rows.append(dict(axis=label,cohort=str(g),n=len(ps),
            mean_priced=round(statistics.mean([p['p'] for p in ps]),0),
            mean_realised_out=round(statistics.mean([p['o'] for p in ps]),2),
            signed_mispricing_m=round(statistics.mean(ms),3),
            m_ci_lo=round(lo,3) if lo is not None else None,m_ci_hi=round(hi,3) if hi is not None else None,
            verdict=('UNDER' if lo and lo>0 else 'OVER' if hi and hi<0 else 'fair/uncertain'),
            support=('firm' if len(ps)>=30 else 'indicative' if len(ps)>=NMIN else 'POOLED/withheld')))
    return rows
surface=[]
surface+=cell_rows(lambda p:(p['pos'],ageband(p['age'])),'position x ageband')
surface+=cell_rows(lambda p:ageband(p['age']),'ageband')
surface+=cell_rows(lambda p:p['pos'],'position (all ages, note runway-mixed)')
surface+=cell_rows(lambda p:(ageband(p['age']),pickband(p['pick'],p['pickless'])),'ageband x pickband')
surface+=cell_rows(lambda p:('rookie' if p['rookie'] else 'drafted',ageband(p['age'])),'type x ageband')
with open(os.path.join(OUT,'cohort_calibration.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(surface[0].keys())); w.writeheader(); w.writerows(surface)
print(f"\ncohort_calibration.csv: {len(surface)} cells")
with open(os.path.join(OUT,'output_price_map.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(dec_rows[0].keys())); w.writeheader(); w.writerows(dec_rows)
    f.write('\n# age-banded elasticity beta (log price ~ log realised-output); beta<1 => top compressed within band\n')
    for b in bands:
        be,al,ci,n=band_beta[b]
        if be is not None: f.write(f'# age {b},beta={be:.3f},CI=[{ci[0]:.3f}:{ci[1]:.3f}],n={n}\n')
    f.write(f'# PEAK(age-neutral),beta={bpk:.3f},CI=[{cipk[0]:.3f}:{cipk[1]:.3f}],n={len(pk)}\n')

# ---------- C. iso pick-band residual within age x position (item 132) ----------
iso_rows=[]
for pos in ('RUC','MID','GEN_DEF','GEN_FWD','KEY_DEF','KEY_FWD'):
    for pb_ in ('01-06','07-12','13-20','21-34','35-50','51-70'):
        ps=[p for p in contrib if p['pos']==pos and pickband(p['pick'],p['pickless'])==pb_ and p.get('resid_band') is not None]
        if not ps: continue
        rs=[p['resid_band'] for p in ps]; lo,hi=boot_ci_mean(rs)
        iso_rows.append(dict(pos=pos,pickband=pb_,n=len(ps),
            mean_resid=round(statistics.mean(rs),3),ci_lo=round(lo,3) if lo is not None else None,
            ci_hi=round(hi,3) if hi is not None else None,
            note=('OVER(+)' if lo and lo>0 else 'UNDER(-)' if hi and hi<0 else '~fair'),
            support=('firm' if len(ps)>=30 else 'indicative' if len(ps)>=NMIN else 'thin')))
with open(os.path.join(OUT,'iso_pickband_residual.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(iso_rows[0].keys())); w.writeheader(); w.writerows(iso_rows)
# resid_band sign: + = priced ABOVE the within-band level map = over; - = below = under-priced

# ---------- D. Young walk-forward (item 130) ----------
matured=[p for p in players if p.get('year') and p['year']<=2021]
# unconditional: anchor (young Yr1 price) vs realised mature value (cur), incl busts (o_top3 may be None/neg)
young_rows=[]
for pb_ in ('01-06','07-12','13-20','21-34','35-50','51-70','rookie/pickless'):
    ps=[p for p in matured if pickband(p['pick'],p['pickless'])==pb_ and p.get('anchor') and p['anchor']>0]
    if len(ps)<NMIN:
        if not ps: continue
    # UNCONDITIONAL (busts kept): median mature cur / young anchor -> pedigree anchor vs realised value
    grow=[p['cur']/p['anchor'] for p in ps if p.get('cur') and p['cur']>0]
    # star-track subset: those who realised above replacement (o_top3>0)
    stars=[p for p in ps if p.get('o_top3') and p['o_top3']>0]
    # the book's OWN recognized growth: peak price / young anchor (retirement-clean; both are book prices)
    star_peakgrow=[p['p_peak']/p['anchor'] for p in stars if p.get('p_peak') and p.get('anchor') and p['anchor']>0]
    # realised-implied fair (peak output through the age-neutral peak map) / young anchor: >1 => under-priced young
    def fair_peak(o): return math.exp(apk+bpk*math.log(o)) if o and o>0 else None
    upr=[fair_peak(p['o_top3'])/p['anchor'] for p in stars if p.get('anchor') and p['anchor']>0 and p.get('o_top3') and p['o_top3']>0]
    young_rows.append(dict(pickband=pb_,n=len(ps),n_star=len(stars),
        uncond_median_cur_over_anchor=round(statistics.median(grow),2) if grow else None,
        star_median_peakprice_over_anchor=round(statistics.median(star_peakgrow),2) if star_peakgrow else None,
        star_median_realisedfair_over_youngprice=round(statistics.median(upr),2) if upr else None,
        support=('firm' if len(ps)>=30 else 'indicative' if len(ps)>=NMIN else 'thin')))
with open(os.path.join(OUT,'young_cohort_walkforward.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(young_rows[0].keys())); w.writeheader(); w.writerows(young_rows)
print("young walk-forward (matured C<=2021): cur/anchor growth; star = realised o_top3>0")
for r in young_rows: print(f"  {r['pickband']:16s} n={r['n']:3d} star={r['n_star']:3d} uncond cur/anchor={r['uncond_median_cur_over_anchor']} star peak/anchor={r['star_median_peakprice_over_anchor']} realisedfair/youngprice={r['star_median_realisedfair_over_youngprice']}")

# ---------- worked rows + named pairwise ----------
by_name={p['player']:p for p in players}
named=['Timothy English','Kieren Briggs','Ryley Sanders','Marcus Bontempelli','Jai Newcombe']
worked=[]
for nm in named:
    p=by_name.get(nm)
    if not p: worked.append(dict(kind='named',who=nm,note='NOT FOUND')); continue
    worked.append(dict(kind='named',who=nm,pos=p['pos'],age=p['age'],pick=p['pick'],type=p['type'],
        realised_o_recent2=round(p['o'],1) if p.get('o') is not None else None,
        realised_o_top3=round(p['o_top3'],1) if p.get('o_top3') is not None else None,
        price_cur=p['cur'],price_peak=p.get('p_peak'),anchor=p.get('anchor'),
        m_in_band=round(p.get('m'),3) if p.get('m') is not None else None,
        resid_band=round(p.get('resid_band'),3) if p.get('resid_band') is not None else None))
# top under/over cohorts among firm/indicative age-conditioned cells with CI excluding 0
firm=[r for r in surface if r['axis'] in ('position x ageband','ageband x pickband') and r['support'] in ('firm','indicative') and r['m_ci_lo'] is not None]
under=sorted([r for r in firm if r['verdict']=='UNDER'],key=lambda r:-r['signed_mispricing_m'])[:5]
over=sorted([r for r in firm if r['verdict']=='OVER'],key=lambda r:r['signed_mispricing_m'])[:5]
def examples(axis,cohort):
    ps=[p for p in contrib if (f"('{p['pos']}', '{ageband(p['age'])}')"==cohort) or (f"('{ageband(p['age'])}', '{pickband(p['pick'],p['pickless'])}')"==cohort)]
    return [(p['player'],round(p['m'],2)) for p in sorted(ps,key=lambda p:-p['m'])[:4]]
for r in under: worked.append(dict(kind='top-under',who=r['cohort'],axis=r['axis'],n=r['n'],m=r['signed_mispricing_m'],ci=[r['m_ci_lo'],r['m_ci_hi']],examples=str(examples(r['axis'],r['cohort']))))
for r in over: worked.append(dict(kind='top-over',who=r['cohort'],axis=r['axis'],n=r['n'],m=r['signed_mispricing_m'],ci=[r['m_ci_lo'],r['m_ci_hi']],examples=str(examples(r['axis'],r['cohort']))))
ak=[]
for w_ in worked:
    for k in w_:
        if k not in ak: ak.append(k)
with open(os.path.join(OUT,'worked_rows.csv'),'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ak); w.writeheader(); w.writerows(worked)

# English/Briggs pairwise (register anchor)
E,B=by_name['Timothy English'],by_name['Kieren Briggs']
print(f"\nENGLISH/BRIGGS pairwise: o_recent2 {E['o']:.1f}/{B['o']:.1f}={E['o']/B['o']:.2f}x  cur {E['cur']}/{B['cur']}={E['cur']/B['cur']:.2f}x  (item131: output 2.99x -> price 2.14x)")
print(f"  peak: o_top3 {E['o_top3']:.1f}/{B['o_top3']:.1f}={E['o_top3']/B['o_top3']:.2f}x  peakprice {E['p_peak']}/{B['p_peak']}={E['p_peak']/B['p_peak']:.2f}x")

summary=dict(base='9be07b8e',n_players=len(recs),contributors=len(contrib),
    band_beta={b:(round(v[0],3) if v[0] else None,[round(v[2][0],3),round(v[2][1],3)] if v[2] else None,v[3]) for b,v in band_beta.items()},
    peak_beta=[round(bpk,3),[round(cipk[0],3),round(cipk[1],3)],len(pk)],
    proven_quintiles=dec_rows,
    named={nm:worked[i] for i,nm in enumerate(named) if 'note' not in worked[i]},
    iso=iso_rows,young=young_rows,
    top_under=[dict(cohort=r['cohort'],axis=r['axis'],n=r['n'],m=r['signed_mispricing_m'],ci=[r['m_ci_lo'],r['m_ci_hi']],examples=examples(r['axis'],r['cohort'])) for r in under],
    top_over=[dict(cohort=r['cohort'],axis=r['axis'],n=r['n'],m=r['signed_mispricing_m'],ci=[r['m_ci_lo'],r['m_ci_hi']],examples=examples(r['axis'],r['cohort'])) for r in over],
    englishbriggs=dict(o_ratio_recent2=round(E['o']/B['o'],2),cur_ratio=round(E['cur']/B['cur'],2),
        o_ratio_peak=round(E['o_top3']/B['o_top3'],2),peakprice_ratio=round(E['p_peak']/B['p_peak'],2)),
    subreplacement=dict(never_delivered=sum(1 for p in players if p['n_deliv']==0),
        below_repl_recent=sum(1 for p in players if p.get('o') is not None and p['o']<=0)))
json.dump(summary,open(os.path.join(OUT,'_summary.json'),'w'),indent=2)
print("\n_summary.json + CSVs written. DONE.")
