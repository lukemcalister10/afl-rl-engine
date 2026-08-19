#!/usr/bin/env python3
"""T4 — IS THE YEAR-1 MARK BLIND TO THE LATE-BAND WINNERS, OR IS THE TROUGH A MIX EFFECT?
The decisive decomposition. READ-ONLY."""
import sys, statistics, random
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

P('='*104)
P('T4 — THE DECISIVE DECOMPOSITION')
P('='*104)
P()
P('-'*104)
P('(a) DOES THE YEAR-1 MARK MISS THE EVENTUAL WINNERS IN THE LATE BANDS?')
P('-'*104)
P('  %-12s %5s %8s %14s %14s %14s'%('band','n','succ %','yr1 mark: WIN','yr1 mark: BUST','ratio win/bust'))
for gname,gf in (('picks 1-20',lambda r:1<=r['pick']<=20),('picks 21-30',lambda r:21<=r['pick']<=30),
                 ('picks 31-40',lambda r:31<=r['pick']<=40),('picks 41-64',lambda r:41<=r['pick']<=64)):
    pop=[r for r in bal if gf(r)]
    m0=statistics.mean([float(r['v0']) for r in pop])
    w=[r for r in pop if rpeak(r)>=BAR]; b=[r for r in pop if rpeak(r)<BAR]
    mw=statistics.mean([value_at(r,1)[0] for r in w])/m0 if w else None
    mb=statistics.mean([value_at(r,1)[0] for r in b])/m0 if b else None
    P('  %-12s %5d %7.0f%% %14s %14s %14s'%(gname,len(pop),100*len(w)/len(pop),
      '%.3f'%mw if mw else '-','%.3f'%mb if mb else '-',
      '%.2f'%(mw/mb) if (mw and mb) else '-'))
P()
P('  READ: the year-1 mark marks the eventual late-band winners UP HARDER than the early-band')
P('  winners, and the win/bust ratio is WIDER late, not narrower. The mark is not blind to them.')
P()

P('-'*104)
P('(b) THEN WHY IS THE BAND MEAN BELOW 1.0? — the mix decomposition')
P('-'*104)
P('  the band year-1 mark = (winners\' value share) + (busts\' value share), both over mean v0')
P('  %-12s %14s %14s %10s'%('band','winners add','busts add','= mark'))
for gname,gf in (('picks 1-20',lambda r:1<=r['pick']<=20),('picks 31-40',lambda r:31<=r['pick']<=40),
                 ('picks 41-64',lambda r:41<=r['pick']<=64)):
    pop=[r for r in bal if gf(r)]
    n=len(pop); tot0=sum(float(r['v0']) for r in pop)
    w=[r for r in pop if rpeak(r)>=BAR]; b=[r for r in pop if rpeak(r)<BAR]
    cw=sum(value_at(r,1)[0] for r in w)/tot0
    cb=sum(value_at(r,1)[0] for r in b)/tot0
    P('  %-12s %14.3f %14.3f %10.3f'%(gname,cw,cb,cw+cb))
P()
P('-'*104)
P('(c) THE COUNTERFACTUAL THAT SEPARATES MIX FROM MISPRICING')
P('-'*104)
P('  If the late band had the EARLY band\'s success RATE but kept its own per-group year-1 marks,')
P('  what would its year-1 mark be?')
e=[r for r in bal if 1<=r['pick']<=20]
rate_e=sum(1 for r in e if rpeak(r)>=BAR)/len(e)
for gname,gf in (('picks 31-40',lambda r:31<=r['pick']<=40),('picks 41-64',lambda r:41<=r['pick']<=64)):
    pop=[r for r in bal if gf(r)]
    m0=statistics.mean([float(r['v0']) for r in pop])
    w=[r for r in pop if rpeak(r)>=BAR]; b=[r for r in pop if rpeak(r)<BAR]
    mw=statistics.mean([value_at(r,1)[0] for r in w])/m0; mb=statistics.mean([value_at(r,1)[0] for r in b])/m0
    act=(len(w)*mw+len(b)*mb)/len(pop)
    cf=rate_e*mw+(1-rate_e)*mb
    P('  %-12s actual mark %.3f (%+.1f%%)   at the 1-20 success rate of %.0f%%: %.3f (%+.1f%%)'
      %(gname,act,100*(act-1),100*rate_e,cf,100*(cf-1)))
P()
P('  THE WHOLE TROUGH IS MIX. Hold the per-group marks fixed and give the late band the early')
P('  band\'s hit rate, and the trough turns into a gain. Nothing about the PRICING of a late-band')
P('  row is wrong; there are simply far fewer winners among them.')
P()

P('-'*104)
P('(d) THE SHAPE — why the mean recovers by year 6 anyway')
P('-'*104)
P('  %-12s %5s %10s %10s %10s %10s %10s'%('band','n','mean pk/v0','median','p90','p99','max'))
for gname,gf in (('picks 1-20',lambda r:1<=r['pick']<=20),('picks 21-30',lambda r:21<=r['pick']<=30),
                 ('picks 31-40',lambda r:31<=r['pick']<=40),('picks 41-64',lambda r:41<=r['pick']<=64)):
    pop=[r for r in bal if gf(r)]
    rs=sorted(rpeak(r)/float(r['v0']) for r in pop)
    q=lambda p: rs[min(len(rs)-1,int(p*len(rs)))]
    P('  %-12s %5d %10.2f %10.2f %10.2f %10.2f %10.2f'
      %(gname,len(rs),statistics.mean(rs),q(0.50),q(0.90),q(0.99),rs[-1]))
P()
P('  The late bands are OPTION-SHAPED: a median late-band row peaks near or below its entry price,')
P('  while the top percentile multiplies it many times over. The mean is a poor description of the')
P('  typical row — which is exactly the caveat the board already carries in its standing box for')
P('  the deep cell ("about half deliver almost nothing and a few deliver a lot").')
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_T4_out.txt','w').write('\n'.join(out))
