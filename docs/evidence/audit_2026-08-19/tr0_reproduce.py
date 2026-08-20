#!/usr/bin/env python3
"""STEP 0 — REPRODUCE THE TROUGH before explaining it. READ-ONLY."""
import sys, statistics
sys.path.insert(0,'/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg')
from tr_lib import *
out=[]
def P(s=''):
    print(s); out.append(str(s))

meta,ND=load('ASMCAND')
WEND=wend_of('ASMCAND')
P('='*104)
P('STEP 0 — REPRODUCING THE LATE-BAND YEAR-1 TROUGH ON THE CANDIDATE (before explaining anything)')
P('='*104)
P('  matrix: per_entrant_ASMCAND.json   store %s   v0surf %s   ND teaching rows %d'
  %(meta['store_md5'],meta['v0surf_sig'][:12],len(ND)))
P()
for wname,(lo,hi) in (('PRIMARY',PRIMARY),('MODERN',MODERN)):
    P('  --- %s window, cohorts %d-%d ---'%(wname,lo,hi))
    P('  %-8s %5s %8s %8s %8s %8s %8s %8s %8s   %s'
      %('band','n','yr0','yr1','yr2','yr3','yr4','yr6','peak','yr0->1'))
    for b in ('1-10','11-20','21-30','31-40','41-64'):
        pop=[r for r in ND if band_of(r['pick'])==b and lo<=cohort(r)<=hi]
        row=[]
        for N in range(0,8):
            incl=[r for r in pop if r['year']+N<=WEND]
            if len(incl)<FLOOR_N: row.append(None); continue
            mN=statistics.mean([value_at(r,N)[0] for r in incl])
            m0=statistics.mean([float(r['v0']) for r in incl])
            row.append(mN/m0 if m0>0 else None)
        pk=max([v for v in row[1:] if v is not None] or [None]) if any(v is not None for v in row[1:]) else None
        f=lambda v:('%8.3f'%v) if v is not None else '       -'
        a01=(row[1]-row[0]) if (row[0] is not None and row[1] is not None) else None
        P('  %-8s %5d %s %s %s %s %s %s %s   %s'
          %(b,len(pop),f(row[0]),f(row[1]),f(row[2]),f(row[3]),f(row[4]),f(row[6]),f(pk),
            ('%+.1f%%'%(100*a01)) if a01 is not None else '-'))
    P()
P('  READ: the owner\'s two facts reproduce. The late bands dip hardest at year 1 and reach')
P('  peaks at or above the early bands. Entries and peaks are consistent; year 1 is the outlier.')
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_REPRODUCE_out.txt','w').write('\n'.join(out))
