# R3 — WHAT THE RECENCY DECAY ALREADY CHARGES FOR ABSENCE, vs the measured truth (R1/R2).
# The engine has no absence lever, but a year-gap ages the player's demonstrated seasons an extra
# k years of decay inside _lvlcurr (ld^(Y-yr), ld=0.40 KEY / 0.35 GEN / 0.225 MR). We isolate that
# charge by REMOVING the gap (shift pre-gap seasons forward by the gap length so the record is
# contiguous) and re-pricing. charge = actual - nogap, in LEVEL points and in SCAR (via ev()).
# Compared per player against the mean-reversion-adjusted truth (R2 smooth age curve).
# Board of record: store b0c39d78. Deep-copies only; nothing written.
import harness as H, d2common as D, numpy as np, copy
MA=H.MA; cp=H.cp; ev=H.ev; g=H.g
_lvlcurr=g['_lvlcurr']

def shift_out_gap(p, gaps):
    """return a deep copy with the pre-gap seasons slid forward by len(gaps) (gap filled, contiguous)."""
    q=copy.deepcopy(p); gmin=min(gaps); glen=len(gaps)
    for x in q['scoring']:
        if x['year']<gmin: x['year']=x['year']+glen
    return q

def charges(p, gaps, Y):
    q=shift_out_gap(p,gaps)
    lv_a=_lvlcurr(p,Y); lv_n=_lvlcurr(q,Y)
    sc_a=ev(p,Y);      sc_n=ev(q,Y)
    return dict(lvl_actual=lv_a, lvl_nogap=lv_n, lvl_charge=lv_a-lv_n,
                scar_actual=sc_a, scar_nogap=sc_n, scar_charge=sc_a-sc_n)

# ---- R2 mean-reversion-adjusted smooth age curve = the 'truth' the charge is compared to ----
ev_=D.build_events(); ctrl=D.build_control(); exp=D.make_expected(ctrl)
cl=D.build_control_lvl(); pred=D.fit_ctrl_model(cl)
rows=D.effect_rows(ev_,exp,ctrl_predict=pred)
tage=np.array([r['age_pre'] for r in rows]); tadj=np.array([r['effect_adj'] for r in rows])
traw=np.array([r['effect'] for r in rows])   # age-only DiD truth (prior D2 / directive framing)
BW=2.5
def _sm(age,y):
    if age is None: return np.nan
    w=np.exp(-0.5*((tage-age)/BW)**2)
    return float(np.sum(w*y)/w.sum())
def truth(age): return _sm(age,tadj)        # PRIMARY: mean-reversion-adjusted (age+level matched)
def truth_ageonly(age): return _sm(age,traw) # the prior/directive age-only truth (prime ~ -1)

# ---- validate on Jamarra ----
J=next(p for p in MA.data if 'ugle-hagan' in p['player'].lower())
print("=== R3 validation · Jamarra Ugle-Hagan (KFWD, gap 2025) · board b0c39d78 ===")
print("  scoring:", [(x['year'],x['games'],round(x['avg'],1)) for x in J['scoring']])
c=charges(J,[2025],2026)
print(f"  _lvlcurr actual(gap)={c['lvl_actual']:.2f}  nogap={c['lvl_nogap']:.2f}  RECENCY CHARGE={c['lvl_charge']:+.2f} lvl-pts")
print(f"  ev()     actual={c['scar_actual']:.0f}  nogap={c['scar_nogap']:.0f}  RECENCY CHARGE={c['scar_charge']:+.0f} SCAR")
print(f"  truth (R2 adj curve @ age {D.age_at(J,2024):.0f}) = {truth(D.age_at(J,2024)):+.2f} lvl-pts\n")

# ---- full gap population, at Y=return-year (charge-at-return, comparable to truth timing) and Y=2026 ----
gaps_pop=D.gap_players()
recs=[]
for gp in gaps_pop:
    p=gp['p']; gaps=gp['gaps']; age=gp['age_pre']
    Yret=gp['ret'][0] if gp['ret'] else 2026
    cR=charges(p,gaps,Yret); c26=charges(p,gaps,2026)
    recs.append(dict(player=gp['player'],pos=gp['pos'],age=age,glen=len(gaps),
        ret=bool(gp['ret']), Yret=Yret,
        lvl_R=cR['lvl_charge'], scar_R=cR['scar_charge'],
        lvl_26=c26['lvl_charge'], scar_26=c26['scar_charge'],
        truth=truth(age), truth_ao=truth_ageonly(age)))
recs=[r for r in recs if r['age'] is not None]
A=np.array([r['age'] for r in recs]); LR=np.array([r['lvl_R'] for r in recs])
L26=np.array([r['lvl_26'] for r in recs]); TR_=np.array([r['truth'] for r in recs])
SR=np.array([r['scar_R'] for r in recs])
print(f"=== recency charge across {len(recs)} gap players (established-base absences) ===")
print(f"  LEVEL charge @ return-year : mean {LR.mean():+.2f}  median {np.median(LR):+.2f} lvl-pts")
print(f"  LEVEL charge @ 2026 (board): mean {L26.mean():+.2f}  median {np.median(L26):+.2f} lvl-pts  (transience: decays as player re-establishes)")
print(f"  measured TRUTH  (R2 adj)   : mean {TR_.mean():+.2f} lvl-pts")
print(f"  SCAR charge @ return-year  : mean {SR.mean():+.0f}  median {np.median(SR):+.0f} SCAR")

TAO=np.array([r['truth_ao'] for r in recs])
print("\n=== UNDER / OVER / RIGHT — recency LEVEL charge (at return) vs truth, by age ===")
print("  (charge - truth < 0 => engine docks MORE than truth => OVER; > 0 => UNDER)")
print("  Two truths shown: [adj] mean-reversion-adjusted (R1[G], primary) · [ao] age-only (prior D2/directive framing)")
for lo,hi,lab in [(18,23,'18-22 (dev trough)'),(23,25,'23-24'),(25,29,'25-28 prime'),(29,45,'29+ older')]:
    m=(A>=lo)&(A<hi)
    if m.sum()>=3:
        ch=LR[m].mean(); tr=TR_[m].mean(); tao=TAO[m].mean()
        def vd(e): return 'OVER' if e<-0.5 else ('UNDER' if e>0.5 else 'RIGHT')
        print(f"  {lab:18} n={m.sum():3d}  charge={ch:+.2f}  |  [adj] truth={tr:+.2f} err={ch-tr:+.2f} {vd(ch-tr):5}  |  [ao] truth={tao:+.2f} err={ch-tao:+.2f} {vd(ch-tao):5}")
print(f"  ALL                n={len(recs):3d}  charge={LR.mean():+.2f}  |  [adj] truth={TR_.mean():+.2f} err={LR.mean()-TR_.mean():+.2f}  |  [ao] truth={TAO.mean():+.2f} err={LR.mean()-TAO.mean():+.2f}")

# does the error vary with age? regress (charge - truth) on age
err_i=LR-TR_
X=np.column_stack([np.ones(len(A)),A]); b,_,_,_=np.linalg.lstsq(X,err_i,rcond=None)
np.random.seed(0)
bs=[np.linalg.lstsq(np.column_stack([np.ones(len(A)),A[s]]),err_i[s],rcond=None)[0][1]
    for s in (np.random.randint(0,len(A),len(A)) for _ in range(3000))]
print(f"\n  error-vs-age slope = {b[1]:+.3f} lvl-pts/yr  95%CI[{np.percentile(bs,2.5):+.3f},{np.percentile(bs,97.5):+.3f}]")
