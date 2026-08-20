#!/usr/bin/env python3
"""T1 — WHO CARRIES THE RECOVERY. Is the late-band year-1 -> peak appreciation BROAD (many modest
recoveries) or CONCENTRATED (a few late-bloomer stars)? READ-ONLY.
BALANCED PANEL: only rows OBSERVED at both year 1 and the comparison year are used, so the
comparison is not contaminated by censoring. The censoring is reported, never hidden."""
import sys, statistics
sys.path.insert(0,'/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg')
from tr_lib import *
out=[]
def P(s=''):
    print(s); out.append(str(s))
meta,ND=load('ASMCAND')
WEND=wend_of('ASMCAND')
LO,HI=PRIMARY
TARGET=6

P('='*104)
P('T1 — WHO CARRIES THE LATE-BAND RECOVERY')
P('='*104)
P('  PRIMARY window %d-%d. BALANCED PANEL: a row counts only if year 1 AND year %d are both'%(LO,HI,TARGET))
P('  observed (cohort year + %d <= %d), so censoring cannot manufacture the result.'%(TARGET,HI))
P()
res={}
for b in ('1-10','11-20','21-30','31-40','41-64'):
    pop=[r for r in ND if band_of(r['pick'])==b and LO<=cohort(r)<=HI]
    bal=[r for r in pop if r['year']+TARGET<=WEND and float(r['v0'])>0]
    cens=len(pop)-len(bal)
    if len(bal)<FLOOR_N: continue
    rows=[]
    for r in bal:
        v0=float(r['v0']); v1=value_at(r,1)[0]; vT=value_at(r,TARGET)[0]
        rows.append(dict(key=r['key'],name=r.get('player'),pick=r['pick'],v0=v0,v1=v1,vT=vT,
                         gain=vT-v1,pos=r.get('pos'),typ=r.get('type'),yr=r['year']))
    m0=statistics.mean([x['v0'] for x in rows])
    tot=sum(x['gain'] for x in rows)
    rows.sort(key=lambda x:-x['gain'])
    pos_gain=sum(x['gain'] for x in rows if x['gain']>0)
    n=len(rows)
    top5=sum(x['gain'] for x in rows[:max(1,round(n*0.05))])
    top10=sum(x['gain'] for x in rows[:max(1,round(n*0.10))])
    top20=sum(x['gain'] for x in rows[:max(1,round(n*0.20))])
    nup=sum(1 for x in rows if x['gain']>0)
    res[b]=dict(rows=rows,n=n,cens=cens,m0=m0,tot=tot,nup=nup,
                s5=top5/tot if tot else None,s10=top10/tot if tot else None,s20=top20/tot if tot else None)
    P('  BAND %-6s  n(balanced)=%-4d censored=%-4d  %s'%(b,n,cens,flag(n)))
    P('     mean yr1/v0 = %.3f   mean yr%d/v0 = %.3f   band gain = %+.1f%% of entry'
      %(statistics.mean([x['v1'] for x in rows])/m0,TARGET,
        statistics.mean([x['vT'] for x in rows])/m0,100*(tot/n)/m0))
    P('     rows that GAINED from yr1 to yr%d: %d of %d (%.0f%%)'%(TARGET,nup,n,100*nup/n))
    P('     share of the TOTAL band gain carried by the top  5%% of rows: %s'
      %('%.0f%%'%(100*res[b]['s5']) if tot else 'n/a'))
    P('     share carried by the top 10%%: %s   top 20%%: %s'
      %('%.0f%%'%(100*res[b]['s10']) if tot else 'n/a','%.0f%%'%(100*res[b]['s20']) if tot else 'n/a'))
    P()

P('-'*104)
P('CONCENTRATION, SIDE BY SIDE — is the late-band recovery broader or narrower than the early bands?')
P('-'*104)
P('  %-8s %5s %10s %10s %10s %10s'%('band','n','% rows up','top5% share','top10% share','top20% share'))
for b in ('1-10','11-20','21-30','31-40','41-64'):
    if b not in res: continue
    d=res[b]
    P('  %-8s %5d %9.0f%% %10s %11s %11s'%(b,d['n'],100*d['nup']/d['n'],
      '%.0f%%'%(100*d['s5']) if d['s5'] is not None else '-',
      '%.0f%%'%(100*d['s10']) if d['s10'] is not None else '-',
      '%.0f%%'%(100*d['s20']) if d['s20'] is not None else '-'))
P()
P('-'*104)
P('THE HISTORICAL EXEMPLARS — ILLUSTRATION ONLY, never a gate and never a target')
P('-'*104)
for b in ('31-40','41-64'):
    if b not in res: continue
    P('  band %s — the ten largest yr1->yr%d gains:'%(b,TARGET))
    P('    %-26s %4s %5s %8s %8s %8s %7s'%('player','pick','draft','v0','yr1','yr%d'%TARGET,'gain'))
    for x in res[b]['rows'][:10]:
        P('    %-26s %4d %5d %8.0f %8.0f %8.0f %+7.0f'%(x['name'],x['pick'],x['yr'],x['v0'],x['v1'],x['vT'],x['gain']))
    P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_T1_out.txt','w').write('\n'.join(out))
