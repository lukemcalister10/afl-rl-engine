#!/usr/bin/env python3
"""Owner hypothesis 2026-08-25: rucks routinely sit their first 2-3 seasons as part of development,
so sitting should be LESS predictive of failure for rucks than for other positions.
Test: historical entrants 2006-2021, gameless through their first 1 / first 2 playable seasons
(draft year not counted, per the calibration convention), outcomes by position class.
Read-only."""
import contextlib, io, json, os, sys
import numpy as np
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']
def tbp(p):
    a=sorted([x['avg'] for x in (p.get('scoring') or []) if x['games']>=6],reverse=True)[:3]
    return float(np.mean(a)) if a else 0.0
def games_in(p,yr): return sum(x['games'] for x in (p.get('scoring') or []) if x['year']==yr)
LAST=2025   # last fully resolved season for outcome fairness on the sat-2 cell
cells={}
for p in MA.data:
    grp=MA.GRP.get(p.get('pos'))
    ey=p.get('year')
    if not grp or not ey or not (2006<=ey<=2021): continue
    if p.get('type')=='MSD': continue                      # different clock; exclude for cleanliness
    cls='RUCK' if grp=='RUCK' else ('KP' if grp in ('KPF','KPD') else 'SMALL')
    for sat in (1,2):
        yrs=[ey+k for k in range(1,sat+1)]
        if yrs[-1]>LAST: continue
        if all(games_in(p,y)==0 for y in yrs):
            v=tbp(p); ever=any(x['games']>0 for x in (p.get('scoring') or []) if x['year']>yrs[-1])
            cells.setdefault((sat,cls),[]).append((v,ever))
print('%-14s %4s  %10s  %8s  %8s' % ('cell','n','mean best-3','P(70+)','P(plays later)'))
out={}
for k in sorted(cells):
    vs=[v for v,_ in cells[k]]; es=[e for _,e in cells[k]]
    n=len(vs)
    boot=[np.mean(np.random.RandomState(i).choice(vs,n)) for i in range(400)] if n>3 else vs
    lo,hi=(np.percentile(boot,2.5),np.percentile(boot,97.5)) if n>3 else (0,0)
    print('sat-%d %-8s %4d  %6.1f [%5.1f,%5.1f]  %6.2f  %8.2f' %
          (k[0],k[1],n,np.mean(vs),lo,hi,np.mean([1 if v>=70 else 0 for v in vs]),np.mean(es)))
    out['sat%d|%s'%k]={'n':n,'mean_best3':round(float(np.mean(vs)),1),'ci':[round(float(lo),1),round(float(hi),1)],
                       'p70':round(float(np.mean([1 if v>=70 else 0 for v in vs])),3),
                       'p_plays_later':round(float(np.mean(es)),3)}
json.dump(out,open('/home/user/seam_fix/ruck_sit_cells.json','w'),indent=1)
