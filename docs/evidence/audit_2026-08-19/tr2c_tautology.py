#!/usr/bin/env python3
"""T2c — THE HONESTY TEST ON RETENTION. Being cut TERMINATES the value path (value_at returns 0 for
'ended'), so 'retained -> becomes valuable' is partly a mechanic, not a discovery. This file asks
whether year-1 retention still carries information AMONG ROWS THAT ALL SURVIVED FURTHER.
READ-ONLY."""
import sys, statistics, random, json
sys.path.insert(0,'/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg')
from tr_lib import *
out=[]
def P(s=''):
    print(s); out.append(str(s))
meta,ND=load('ASMCAND')
WEND=wend_of('ASMCAND')
LO,HI=PRIMARY; TARGET=6
def rpeak(r):
    b=0.0
    for N in range(1,8):
        if r['year']+N>WEND: break
        b=max(b,value_at(r,N)[0])
    return b
bal=[r for r in ND if LO<=cohort(r)<=HI and r['year']+TARGET<=WEND and float(r['v0'])>0]
peaks=sorted(rpeak(r) for r in bal); BAR=peaks[int(0.75*len(peaks))]
def survives_to(r,N):
    y=r['year']+N
    if any(x['year']>=y for x in (r.get('seasons') or [])): return True
    lg=r.get('last_game_year'); return bool(lg is not None and lg>=y)
def ret(r): return 1 if survives_to(r,2) else 0

P('='*104)
P('T2c — IS RETENTION A DISCOVERY OR A MECHANIC?')
P('='*104)
P('  A cut row\'s path ENDS, and the standing instrument scores an ended path as 0. So "retained')
P('  predicts value" is guaranteed in part by construction. The honest question: among rows that')
P('  ALL survived to year k, does year-1 retention still separate?')
P()
late=[r for r in bal if 31<=r['pick']<=64]
early=[r for r in bal if 1<=r['pick']<=20]
def auc(sig,succ):
    pr=[(s,y) for s,y in zip(sig,succ) if s is not None]
    a=[s for s,y in pr if y]; b=[s for s,y in pr if not y]
    if not a or not b: return None
    n=t=0
    for x in a:
        for y in b:
            t+=1; n+= 1 if x>y else (0.5 if x==y else 0)
    return n/t
for gname,pop in (('picks 31-64',late),('picks 1-20',early)):
    P('  --- %s ---'%gname)
    P('    %-32s %6s %8s %10s %10s'%('conditioning','n','kept %','AUC(ret)','note'))
    for k,lbl in ((0,'no conditioning (all rows)'),(3,'survived to year 3'),(4,'survived to year 4'),
                  (5,'survived to year 5')):
        sub=[r for r in pop if (k==0 or survives_to(r,k))]
        if len(sub)<FLOOR_N: continue
        sig=[ret(r) for r in sub]; succ=[1 if rpeak(r)>=BAR else 0 for r in sub]
        kept=100*sum(sig)/len(sig)
        a=auc(sig,succ)
        note=''
        if kept>=99.5: note='EVERYONE kept -> no contrast left'
        P('    %-32s %6d %7.0f%% %10s   %s'%(lbl,len(sub),kept,('%.3f'%a) if a is not None else 'n/a',note))
    P()
P('  READ: once you condition on surviving a few years, the year-1 retention flag has no contrast')
P('  left — essentially every survivor was retained. THE SEPARATION IN T2 IS THE TERMINATION')
P('  MECHANIC, NOT AN INDEPENDENT EARLY SIGNAL. Reported as a NULL rather than banked.')
P()

P('-'*104)
P('SO WHAT IS LEFT? — the production signals, and how much of the trough they could ever close')
P('-'*104)
P('  The year-1 mark is a PRICE, and the standing instrument compares mean(v_yr1)/mean(v_yr0).')
P('  The late-band trough is -11.0%% (31-40) and -7.4%% (41-64) on PRIMARY.')
P()
for gname,pop in (('picks 1-20',early),('picks 31-64',late)):
    succ=[r for r in pop if rpeak(r)>=BAR]; fail=[r for r in pop if rpeak(r)<BAR]
    m0=statistics.mean([float(r['v0']) for r in pop])
    P('  %-12s n=%-4d successes=%-3d (%.0f%%)'%(gname,len(pop),len(succ),100*len(succ)/len(pop)))
    P('     mean yr1/v0  successes %.3f   non-successes %.3f'
      %(statistics.mean([value_at(r,1)[0] for r in succ])/m0,
        statistics.mean([value_at(r,1)[0] for r in fail])/m0))
    P('     mean peak/v0 successes %.3f   non-successes %.3f'
      %(statistics.mean([rpeak(r) for r in succ])/m0,
        statistics.mean([rpeak(r) for r in fail])/m0))
    zero1=sum(1 for r in pop if value_at(r,1)[0]==0.0)
    P('     rows priced ZERO at year 1: %d (%.0f%%)'%(zero1,100*zero1/len(pop)))
    P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_T2C_out.txt','w').write('\n'.join(out))
