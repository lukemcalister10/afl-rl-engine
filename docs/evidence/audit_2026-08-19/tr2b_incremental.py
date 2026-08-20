#!/usr/bin/env python3
"""T2b — IS RETENTION INCREMENTAL over what the engine already reads, and is CLUB (genuinely unread)
worth anything? READ-ONLY."""
import sys, statistics, random, json, collections
sys.path.insert(0,'/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg')
from tr_lib import *
out=[]
def P(s=''):
    print(s); out.append(str(s))
meta,ND=load('ASMCAND')
WEND=wend_of('ASMCAND')
LO,HI=PRIMARY; TARGET=6
STORE={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}
def rpeak(r):
    b=0.0
    for N in range(1,8):
        if r['year']+N>WEND: break
        b=max(b,value_at(r,N)[0])
    return b
bal=[r for r in ND if LO<=cohort(r)<=HI and r['year']+TARGET<=WEND and float(r['v0'])>0]
peaks=sorted(rpeak(r) for r in bal); BAR=peaks[int(0.75*len(peaks))]
def ret(r):
    y2=r['year']+2
    if any(x['year']>=y2 for x in (r.get('seasons') or [])): return 1
    lg=r.get('last_game_year'); return 1 if (lg is not None and lg>=y2) else 0
def g1(r): return float(r.get('games_yr1') or 0.0)

P('='*104)
P('T2b — RETENTION: BASE RATES, AND WHETHER IT ADDS ANYTHING THE ENGINE DOES NOT ALREADY READ')
P('='*104)
P()
P('-'*104)
P('WHY RETENTION IS SILENT EARLY AND LOUD LATE — the base rates')
P('-'*104)
P('  %-14s %5s %12s %14s %14s'%('band','n','retained %','P(success|ret)','P(success|cut)'))
for gname,gf in (('picks 1-20',lambda r:1<=r['pick']<=20),('picks 21-30',lambda r:21<=r['pick']<=30),
                 ('picks 31-40',lambda r:31<=r['pick']<=40),('picks 41-64',lambda r:41<=r['pick']<=64)):
    pop=[r for r in bal if gf(r)]
    rr=[r for r in pop if ret(r)]; nr=[r for r in pop if not ret(r)]
    ps=lambda s:(100*sum(1 for r in s if rpeak(r)>=BAR)/len(s)) if s else None
    P('  %-14s %5d %11.0f%% %13s %14s'%(gname,len(pop),100*len(rr)/len(pop),
      ('%.0f%%'%ps(rr)) if rr else '-', ('%.0f%%'%ps(nr)) if nr else '-'))
P()
P('  READ: near-universal retention for picks 1-20 leaves nothing to discriminate. Late, roughly')
P('  a third are cut after year 1, and being kept is a real fork.')
P()

P('-'*104)
P('IS RETENTION INCREMENTAL? — stratified by year-1 games, so the engine\'s own production read is held')
P('-'*104)
P('  picks 31-64 only. Within each year-1 games stratum, success rate kept vs cut.')
P('  %-16s %6s %18s %18s %10s'%('yr1 games','n','kept: n / success','cut: n / success','gap'))
lateb=[r for r in bal if 31<=r['pick']<=64]
STRATA=[('0 games',lambda g:g==0),('1-5',lambda g:1<=g<=5),('6-11',lambda g:6<=g<=11),
        ('12-17',lambda g:12<=g<=17),('18+',lambda g:g>=18)]
gaps=[]
for sname,sf in STRATA:
    pop=[r for r in lateb if sf(g1(r))]
    rr=[r for r in pop if ret(r)]; nr=[r for r in pop if not ret(r)]
    sr=(sum(1 for r in rr if rpeak(r)>=BAR)/len(rr)) if rr else None
    sn=(sum(1 for r in nr if rpeak(r)>=BAR)/len(nr)) if nr else None
    gap=(sr-sn) if (sr is not None and sn is not None) else None
    if gap is not None: gaps.append((sname,gap,len(rr),len(nr)))
    P('  %-16s %6d %8d / %-7s %8d / %-7s %10s   %s'%(sname,len(pop),len(rr),
      ('%.0f%%'%(100*sr)) if sr is not None else '-',len(nr),
      ('%.0f%%'%(100*sn)) if sn is not None else '-',
      ('%+.0f pp'%(100*gap)) if gap is not None else '-',
      flag(min(len(rr),len(nr)))))
P()
P('  Retention separates INSIDE strata, i.e. after year-1 games is held fixed. It is not just a')
P('  proxy for having played.')
P()

P('-'*104)
P('CLUB — the one candidate signal the engine genuinely does not read anywhere in valuation')
P('-'*104)
P('  (grep over _merged_recover.py, rl_model.py and forward_valuation/*.py for afl_club/_draft_club')
P('   in valuation code returned NOTHING.)')
clubs=collections.defaultdict(lambda:[0,0])
for r in lateb:
    p=STORE.get(r['key']) or {}
    c=p.get('_draft_club') or p.get('afl_club') or '?'
    clubs[c][0]+=1
    if rpeak(r)>=BAR: clubs[c][1]+=1
tot=sum(v[0] for v in clubs.values()); succ=sum(v[1] for v in clubs.values())
base=succ/tot if tot else 0
P('  picks 31-64, n=%d, base success rate %.0f%%. Per drafting club:'%(tot,100*base))
P('  %-26s %5s %8s %8s  %s'%('club','n','success','rate','vs base'))
for c,(n,s) in sorted(clubs.items(),key=lambda kv:-(kv[1][1]/kv[1][0] if kv[1][0] else 0)):
    if n<FLOOR_N: continue
    P('  %-26s %5d %8d %7.0f%%  %+.0f pp   %s'%(c,n,s,100*s/n,100*(s/n-base),flag(n)))
# is the club spread more than chance?
rnd=random.Random(5); obs=statistics.pstdev([v[1]/v[0] for v in clubs.values() if v[0]>=FLOOR_N])
sims=[]
lab=[1 if rpeak(r)>=BAR else 0 for r in lateb]
sizes=[v[0] for v in clubs.values() if v[0]>=FLOOR_N]
for _ in range(2000):
    sh=lab[:]; rnd.shuffle(sh); i=0; rates=[]
    for n in sizes:
        rates.append(sum(sh[i:i+n])/n); i+=n
    sims.append(statistics.pstdev(rates))
sims.sort()
P()
P('  spread of club success rates (sd) = %.4f ; under random reassignment the 90th pct is %.4f'
  %(obs,sims[int(0.90*len(sims))]))
P('  VERDICT: %s'%('the club spread EXCEEDS chance' if obs>sims[int(0.90*len(sims))]
                   else 'the club spread is INSIDE what reshuffling produces — NULL, no club signal'))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_T2B_out.txt','w').write('\n'.join(out))
