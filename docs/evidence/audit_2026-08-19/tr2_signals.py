#!/usr/bin/env python3
"""T2 + T3 — THE EARLY-SIGNAL AUDIT, and the across-band comparison that tests the owner's
'unique to that cohort' claim. READ-ONLY.

ESTIMAND. Within a band group, take every row observed for at least TARGET years. Call a row a
SUCCESS if its realized peak value clears an ABSOLUTE, BAND-INDEPENDENT bar (the top quartile of the
whole ND teaching population's realized peaks) — the bar is absolute on purpose: the question is who
BECOMES valuable, and a within-band bar would define the answer into existence.

For each YEAR-1 OBSERVABLE, the separation statistic is the AUC: the probability that a randomly
drawn success scores higher than a randomly drawn non-success. 0.50 = no information. CIs are a
2,000-draw bootstrap over rows (one row = one player here, so the row IS the cluster)."""
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

def realized_peak(r):
    best=0.0
    for N in range(1,8):
        if r['year']+N>WEND: break
        v,_=value_at(r,N)
        best=max(best,v)
    return best

bal=[r for r in ND if LO<=cohort(r)<=HI and r['year']+TARGET<=WEND and float(r['v0'])>0]
peaks=sorted(realized_peak(r) for r in bal)
BAR=peaks[int(0.75*len(peaks))]
P('='*104)
P('T2 / T3 — THE EARLY-SIGNAL AUDIT')
P('='*104)
P('  balanced rows (>= %d observed years, PRIMARY): %d'%(TARGET,len(bal)))
P('  SUCCESS bar = top quartile of realized peak over ALL of them = %.0f board points (absolute,'%BAR)
P('  band-independent). %d of %d rows clear it.'%(sum(1 for r in bal if realized_peak(r)>=BAR),len(bal)))
P()

def yr1_avg(r):
    y=r['year']+1
    s=[x for x in (r.get('seasons') or []) if x['year']==y and x.get('games')]
    return float(s[0]['avg']) if s else None
def yr1_games(r):
    return float(r.get('games_yr1') or 0.0)
def retained_y2(r):
    """still on a list for year 2: he has a year-2 season row, or his last game is year 2 or later."""
    y2=r['year']+2
    if any(x['year']>=y2 for x in (r.get('seasons') or [])): return 1.0
    lg=r.get('last_game_year')
    return 1.0 if (lg is not None and lg>=y2) else 0.0
def entry_age(r):
    a=r.get('age_draft')
    return float(a) if a is not None else None

SIGNALS=[
 ('games in year 1',            yr1_games,                       'engine READS it (rho31, A(g), the F1 credit curve, every games bar)'),
 ('average when played, yr 1',  yr1_avg,                         'engine READS it (the level, the gate bar, the surplus)'),
 ('total output yr1 (g x avg)', lambda r:(yr1_games(r)*(yr1_avg(r) or 0.0)) if yr1_games(r) else 0.0,
                                                                 'engine READS both factors'),
 ('entry age (younger=better)', lambda r:(-entry_age(r)) if entry_age(r) is not None else None,
                                                                 'engine READS it (age-referenced gate bar, mature-entry discount)'),
 ('RETAINED into year 2',       retained_y2,                     'PARTIALLY read — see the reconciliation note'),
]

def auc(sig,succ):
    pairs=[(s,y) for s,y in zip(sig,succ) if s is not None]
    a=[s for s,y in pairs if y]; b=[s for s,y in pairs if not y]
    if not a or not b: return None
    n=0; t=0
    for x in a:
        for y in b:
            t+=1
            n+= 1 if x>y else (0.5 if x==y else 0)
    return n/t
def auc_ci(sig,succ,B=2000,seed=11):
    idx=[i for i in range(len(sig)) if sig[i] is not None]
    if not idx: return (None,None,None)
    rnd=random.Random(seed); vals=[]
    for _ in range(B):
        s=[idx[rnd.randrange(len(idx))] for _ in range(len(idx))]
        a=auc([sig[i] for i in s],[succ[i] for i in s])
        if a is not None: vals.append(a)
    vals.sort()
    return (auc(sig,succ), vals[int(0.05*len(vals))], vals[int(0.95*len(vals))-1]) if vals else (None,None,None)

GROUPS=[('picks 1-20', lambda r:1<=r['pick']<=20),
        ('picks 21-30',lambda r:21<=r['pick']<=30),
        ('picks 31-64',lambda r:31<=r['pick']<=64),
        ('  of which 31-40',lambda r:31<=r['pick']<=40),
        ('  of which 41-64',lambda r:41<=r['pick']<=64)]

P('-'*104)
P('SEPARATION AT YEAR 1, BY BAND GROUP (AUC; 0.50 = the observable says nothing)')
P('-'*104)
store_auc={}
for gname,gf in GROUPS:
    pop=[r for r in bal if gf(r)]
    succ=[1 if realized_peak(r)>=BAR else 0 for r in pop]
    ns=sum(succ)
    P('  %-18s n=%-4d successes=%-3d (%.0f%%)   %s'%(gname,len(pop),ns,100*ns/len(pop) if pop else 0,flag(min(ns,len(pop)-ns))))
    for sname,sf,_ in SIGNALS:
        sig=[sf(r) for r in pop]
        a,lo,hi=auc_ci(sig,succ)
        if a is None: P('     %-28s  n/a'%sname); continue
        sep='INFORMATIVE' if (lo is not None and lo>0.5) else ('none' if (lo is not None and lo<=0.5<=hi) else 'INVERSE')
        store_auc[(gname,sname)]=(a,lo,hi)
        P('     %-28s AUC %.3f  90%% CI [%.3f, %.3f]   %s'%(sname,a,lo,hi,sep))
    P()

P('-'*104)
P('T3 — THE TEST OF THE OWNER\'S CLAIM: is the early-signal deficit LARGER for late picks?')
P('-'*104)
P('  %-28s %14s %14s %14s'%('signal','picks 1-20','picks 21-30','picks 31-64'))
for sname,_,_ in SIGNALS:
    row=[]
    for g in ('picks 1-20','picks 21-30','picks 31-64'):
        v=store_auc.get((g,sname))
        row.append('%.3f'%v[0] if v else '-')
    P('  %-28s %14s %14s %14s'%(sname,row[0],row[1],row[2]))
P()
P('  (AUC closer to 0.50 = the year-1 observable carries LESS information about who becomes')
P('  valuable. The owner predicts the late-pick column sits closer to 0.50.)')
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/trpkg/TROUGH_T2T3_out.txt','w').write('\n'.join(out))
