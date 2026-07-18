import json, statistics as st
SP="/tmp/claude-0/-home-user-afl-rl-engine/d9439600-3e14-5c64-8f57-bbe5bcf65036/scratchpad"
W=json.load(open(SP+"/board_v210.json"))
A=W['active']; LP=W['lensPicks']
b1=json.load(open(SP+"/board_minus1_2025.json"))['rows']
b2=json.load(open(SP+"/board_minus2_2024.json"))['rows']
bn=json.load(open(SP+"/board_now_2026.json"))['rows']
def S(rows,k): return sum((r.get(k) or 0) for r in rows)
out={}

# ---------- Totals (single-run, same 804 roster) ----------
Sv,SvP1,SvP2,SvM1,SvM2=[round(S(A,k)) for k in ('v','vP1','vP2','vM1','vM2')]
out['totals_singlerun']=dict(now=Sv,fwd1=SvP1,fwd2=SvP2,back1=SvM1,back2=SvM2,n=len(A))

# ---------- JOB 1: BACKTEST ----------
# (A) composition-controlled: identical roster, fwd vs back one-year rate
fwd_rate = SvP1/Sv - 1                      # now -> +1
back_rate = Sv/SvM1 - 1                     # -1 -> now (realized, engine backward lens)
# calibrated expectation: apply the engine's own realized backward one-year rate forward
pred_fwd_if_symmetric = round(Sv*(Sv/SvM1))
undershoot_A = round(pred_fwd_if_symmetric - SvP1)
out['job1_backtestA_controlled']=dict(
   roster_now=Sv, fwd1_modeled=SvP1, fwd_rate_pct=round(100*fwd_rate,1),
   back1_state=SvM1, back_rate_realized_pct=round(100*back_rate,1),
   calibrated_fwd1_if_symmetric=pred_fwd_if_symmetric,
   undershoot_vs_symmetric=undershoot_A, undershoot_pct=round(100*undershoot_A/Sv,1))

# (B) F2 actual boards: project -1 forward one year via smoothed fwd ratio r(exp), reproduce now.
NOW=2026
# build smoothed one-year fwd ratio by experience (years since draft) from the single run
from collections import defaultdict
buckets=defaultdict(list)
for r in A:
    dy=r.get('draft_year') or r.get('yr')
    # workspace uses 'draft' as category; derive exp from age proxy: use 'age'
    pass
# workspace rows carry 'age'; build ratio vP1/v by age (smoothed, 1-yr, clipped)
rat_by_age=defaultdict(list)
for r in A:
    if (r.get('v') or 0)>50 and r.get('age'):
        rat_by_age[r['age']].append((r['vP1'] or 0)/r['v'])
# smoothed ratio: median per age, then fill gaps by nearest
ages=sorted(rat_by_age)
ratmed={a:st.median(rat_by_age[a]) for a in ages}
def ratio_for_age(a):
    if a in ratmed: return ratmed[a]
    ka=min(ratmed, key=lambda x:abs(x-a)); return ratmed[ka]
# map F2 players to an age: use workspace age where key matches; else estimate age=NOW-draft_year+18.5
wage={r['key']:r['age'] for r in A if r.get('key')}
def est_age(row, asof):
    if row['key'] in wage: return wage[row['key']]-(NOW-asof)
    return (asof-(row.get('draft_year') or asof))+18.5
def backtest(src_rows, src_year):
    pred=0
    for row in src_rows:
        a=est_age(row, src_year)
        pred+= (row['v'] or 0)*ratio_for_age(round(a))
    return round(pred)
pred_now = backtest(b1,2025)             # -1 -> now
pred_m1  = backtest(b2,2024)             # -2 -> -1
actual_now=752427; actual_m1=771152
out['job1_backtestB_F2boards']=dict(
  minus1_total=round(S(b1,'v')), pred_now=pred_now, actual_now=actual_now,
  err_now=pred_now-actual_now, err_now_pct=round(100*(pred_now-actual_now)/actual_now,1),
  minus2_total=round(S(b2,'v')), pred_minus1=pred_m1, actual_minus1=actual_m1,
  err_m1=pred_m1-actual_m1, err_m1_pct=round(100*(pred_m1-actual_m1)/actual_m1,1))

# ---------- JOB 2: now->+1 DECOMPOSITION by cohort ----------
def cohort(a):
    if a is None: return 'unknown'
    if a<=23: return 'developing(<=23)'
    if a<=27: return 'mid(24-27)'
    return 'veteran(>=28)'
coh=defaultdict(lambda: dict(n=0, dnow=0, dfwd=0, delta=0, dv=[]))
for r in A:
    c=cohort(r.get('age')); d=(r.get('vP1') or 0)-(r.get('v') or 0)
    coh[c]['n']+=1; coh[c]['dnow']+=(r.get('v') or 0); coh[c]['dfwd']+=(r.get('vP1') or 0)
    coh[c]['delta']+=d; coh[c]['dv'].append(d)
out['job2_decomp']={}
for c,x in coh.items():
    out['job2_decomp'][c]=dict(n=x['n'], now=round(x['dnow']), fwd1=round(x['dfwd']),
        signed_delta=round(x['delta']), mean_delta=round(x['delta']/x['n']),
        pct=round(100*x['delta']/x['dnow'],1) if x['dnow'] else None)
# exits + phantom (filed F1 authoritative; single-run corroboration)
out['job2_exits_phantom']=dict(
  phantom_intake_plus1_singlerun=round(sum(p['v'] for p in LP if p['lens']==1)),
  F1_filed_phantom_net_plus1=80480, F1_filed_draft=43266, F1_filed_free=69552,
  F1_filed_exits_refilled=366, F1_filed_residual=32338)

# ---------- JOB 3: PEDIGREE-PREMIUM CARRY ----------
young=[r for r in A if (r.get('age') or 99)<=23]
# high-pick low-games young
def games(r): return r.get('g') or r.get('cg') or 0
hp_lg=[r for r in young if (r.get('pk') or 999)<=20 and games(r)<=40]
pedanchored=[r for r in A if r.get('pedOnly')]
def prem(rows):
    return dict(n=len(rows), now=round(S(rows,'v')), fwd1=round(S(rows,'vP1')),
      premium_lost=round(S(rows,'v')-S(rows,'vP1')),
      mean_pct=round(100*(S(rows,'v')-S(rows,'vP1'))/S(rows,'v'),1) if S(rows,'v') else None)
out['job3_pedigree']=dict(
  young_le23=prem(young),
  young_highpick_lowgames=prem(hp_lg),
  pedOnly_rows=prem(pedanchored),
  examples=[dict(name=r['name'],age=r['age'],pk=r['pk'],g=games(r),v=round(r['v']),vP1=round(r['vP1']),lost=round(r['v']-r['vP1'])) 
            for r in sorted(hp_lg,key=lambda r:r['v']-r['vP1'],reverse=True)[:12]])
# share of job2 developing decline explained by these
dev_decline=-coh['developing(<=23)']['delta']
out['job3_pedigree']['share_of_developing_decline']=dict(
  developing_decline=round(dev_decline),
  highpick_lowgames_lost=round(S(hp_lg,'v')-S(hp_lg,'vP1')),
  pct=round(100*(S(hp_lg,'v')-S(hp_lg,'vP1'))/dev_decline,1) if dev_decline else None)

# ---------- JOB 4: DISTRIBUTED RETIREMENT ----------
# empirical P(exit|age) from F2 actual boards, pooled -2->-1 and -1->now
def keyset(rows): return {r['key'] for r in rows}
kb2,kb1,kbn=keyset(b2),keyset(b1),keyset(bn)
haz=defaultdict(lambda:[0,0])  # age -> [exited, total]
for rows,nxt,asof in [(b2,kb1,2024),(b1,kbn,2025)]:
    for r in rows:
        a=round(est_age(r,asof))
        haz[a][1]+=1
        if r['key'] not in nxt: haz[a][0]+=1
# smoothed P(retire|age): only age-eligible (age>=26); simple isotonic-ish via cumulative
def p_ret(a):
    # pooled hazard in +/-1 age window
    ex=tot=0
    for aa in (a-1,a,a+1):
        ex+=haz[aa][0]; tot+=haz[aa][1]
    p= ex/tot if tot else 0.0
    return p if a>=26 else min(p,0.02)   # floor youth near zero (age-eligible steer)
# distributed liability on the single-run now roster (age-eligible cohort)
elig=[r for r in A if (r.get('age') or 0)>=26]
dist_liab=sum(p_ret(r['age'])*(r['v'] or 0) for r in elig)
dist_liab2=sum(min(1.0,2*p_ret(r['age']))*(r['v'] or 0) for r in elig)  # +2 horizon ~ 2yr cumulative
# discrete rule replica: exit if vP1 < X=207
X=207
disc_exit=[r for r in A if (r.get('vP1') or 0)<X]
disc_removed=round(S(disc_exit,'v'))
out['job4_distributed_retirement']=dict(
  construction="P(retire|age) = pooled empirical exit hazard from F2 -2/-1/now, +/-1yr smoothed, age>=26 eligible; per-player haircut = P*v; no named exits",
  eligible_n=len(elig),
  distributed_liability_plus1=round(dist_liab),
  distributed_liability_plus2=round(dist_liab2),
  discrete_exit_rule_X=X, discrete_exits_n=len(disc_exit), discrete_removed_value=disc_removed,
  F1_filed_exits_plus1=366, F1_filed_residual_plus1=32338,
  diff_discrete_minus_distributed_plus1=round(disc_removed-dist_liab))
# show hazard curve
out['job4_distributed_retirement']['hazard_by_age']={a:round(haz[a][0]/haz[a][1],3) for a in sorted(haz) if haz[a][1]>=5}

json.dump(out, open(SP+"/findings.json","w"), indent=1)
print(json.dumps(out,indent=1))
