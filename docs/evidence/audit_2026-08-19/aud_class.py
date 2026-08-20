#!/usr/bin/env python3
"""INDEPENDENT AUDIT · A4 — THE YEAR-1 CLASS MARK, re-derived on the REGISTERED W2 BASIS.

The estimand, written from the register's own words and NOT copied from as_class.py:
  registered basis = DRAFT classes 2005-2015, ENTRY_FLOOR 2005; on the cohort clock (cohort =
  draft year + 1, except MSD where cohort = draft year) that is cohort years 2006-2016.
  A class's mark = (sum of its rows' year-1 prices) / (sum of its rows' year-0 prices);
  year 0 is v0, year 1 is the vpath cell at the cohort year; ended/null counts as 0 and STAYS in
  the denominator; rows whose path starts after the cohort year are excluded, never scored zero.
  The overall mark is the unweighted average of the class marks in the window.

The instrument is VALIDATED first: it must reproduce ORDER K's published W2 1.0513 and cohort-clock
1.0324 off ORDER K's own matrix before any candidate number is quoted."""
import json, os, hashlib

SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
out=[]
def P(s=''):
    print(s); out.append(str(s))

W2=list(range(2006,2017))       # DRAFT 2005-2015 on the cohort clock — THE REGISTERED BASIS
COH=list(range(2005,2016))      # DRAFT 2004-2014 — the cohort clock, NOT the rail
ALL=list(range(2005,2022))
FLOOR,RAIL=1.03,1.14

def cohort(r):
    y=r.get('year')
    return None if y is None else (y if r.get('type')=='MSD' else y+1)

def marks(path):
    D=json.load(open(path)); R=D['recs']
    wend=max(y for r in R for y,v in zip(r.get('yrs') or [],r.get('vpath') or []) if v is not None)
    elig=[r for r in R if cohort(r) is not None and (r.get('v0') or 0)>0]
    per={}
    for y in ALL:
        num=den=0.0; n=0
        for r in elig:
            if cohort(r)!=y: continue
            yrs=r.get('yrs') or []; vp=r.get('vpath') or []
            if y>wend: continue
            if not yrs: v1=0.0
            elif y<yrs[0]: continue          # path starts later — excluded, not zeroed
            elif y>yrs[-1]: v1=0.0           # ended — zero, stays in the denominator
            else:
                i=yrs.index(y); v1=0.0 if vp[i] is None else float(vp[i])
            num+=v1; den+=float(r['v0']); n+=1
        per[y]=(num/den) if (den>0 and n>=5) else None
    def avg(ws):
        v=[per[y] for y in ws if per.get(y) is not None]
        return (sum(v)/len(v),len(v))
    w2,nw2=avg(W2); ch,nch=avg(COH)
    return dict(per=per,w2=w2,n_w2=nw2,coh=ch,n_coh=nch)

P('='*100)
P('INDEPENDENT AUDIT · A4 — THE YEAR-1 CLASS MARK RE-DERIVED')
P('='*100)
P()
CAND=SP+'/per_entrant_ASMCAND.json'
K=SP+'/per_entrant_OKRULED.json'
Pb=SP+'/per_entrant_PBUILT.json'
P('  matrices read (md5 / mtime):')
for lbl,p in (('ASMCAND',CAND),('OKRULED',K),('PBUILT',Pb)):
    if os.path.exists(p):
        import time
        P('    %-9s %s  %s'%(lbl,hashlib.md5(open(p,'rb').read()).hexdigest()[:12],
                              time.strftime('%Y-%m-%d %H:%M',time.gmtime(os.path.getmtime(p)))))
    else: P('    %-9s MISSING'%lbl)
P()
P('-'*100)
P('INSTRUMENT VALIDATION — reproduce ORDER K\'s published marks off ORDER K\'s own matrix')
P('-'*100)
mk=marks(K)
P('  ORDER K  W2 %.4f   (published 1.0513, diff %+.5f)'%(mk['w2'],mk['w2']-1.0513))
P('  ORDER K  cohort clock %.4f   (published 1.0324, diff %+.5f)'%(mk['coh'],mk['coh']-1.0324))
ok=max(abs(mk['w2']-1.0513),abs(mk['coh']-1.0324))<5e-4
P('  -> %s'%('VALIDATED — the instrument is the published one'if ok else '*** THE INSTRUMENT DISAGREES — nothing below is quotable ***'))
P()
if os.path.exists(Pb):
    mp=marks(Pb)
    P('  control ORDER P  W2 %.4f  (published 1.0613, diff %+.5f)'%(mp['w2'],mp['w2']-1.0613))
    P()
P('-'*100)
P('THE CANDIDATE, ON THE REGISTERED W2 BASIS (DRAFT 2005-2015, ENTRY_FLOOR 2005)')
P('-'*100)
mc=marks(CAND)
P('  CANDIDATE  W2 mark        %.4f      (PUBLISHED 1.0671, diff %+.5f)'%(mc['w2'],mc['w2']-1.0671))
P('  CANDIDATE  cohort clock   %.4f      (published 1.0423, diff %+.5f)'%(mc['coh'],mc['coh']-1.0423))
P('  classes averaged: %d of %d in the window'%(mc['n_w2'],len(W2)))
P('  acceptance gate [%.2f, %.2f) : %s'%(FLOOR,RAIL,'INSIDE — PASSES' if FLOOR<=mc['w2']<RAIL else '*** BREACH ***'))
P()
P('  PER-CLASS, and the breaches named:')
P('    %-7s %9s %9s   %s'%('cohort','candidate','ORDER K','over the 1.14 rail?'))
for y in W2:
    v=mc['per'].get(y); kv=mk['per'].get(y)
    P('    %-7s %9s %9s   %s'%(y,'%.4f'%v if v else '-','%.4f'%kv if kv else '-',
                               'BREACH' if (v and v>=RAIL) else ''))
P()
mx=max((v,y) for y,v in mc['per'].items() if v is not None)
P('  max class over ALL cohorts: %.4f at %d'%(mx[0],mx[1]))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/auditpkg/AUD_CLASS_out.txt','w').write('\n'.join(out))
