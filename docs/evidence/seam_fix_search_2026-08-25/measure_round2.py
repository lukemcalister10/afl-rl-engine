#!/usr/bin/env python3
"""SEAM ROUND 2 — the owner-directed measurements (2026-08-25):
M1 pedigree-ordering census (the Burton-Oliver class)
M2 key-position forgiveness (do weak KP cameos resolve better than weak non-KP cameos?)
M3 mature-age flags on the live no-banked-level population
M4 tenure-5+ scope split (mature-age vs ordinary draftees)
Read-only; one engine load."""
import contextlib, io, json, os, sys
import numpy as np
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; evf=g['ev']; F=1.0524; Y=2026
OUT={}

def entry_age(p):
    by=p.get('_by'); yr=p.get('year')
    if not by or not yr: return None
    return int(yr)-int(by)

# live no-banked-level population with cur/cf (recompute; matches scope_census)
live=[]
for p in MA.data:
    if p.get('_retired'): continue
    sc=[x for x in (p.get('scoring') or []) if x.get('year',0)<=Y]
    gtot=sum(x.get('games',0) for x in sc)
    if gtot<1 or any(x.get('games',0)>=6 for x in sc): continue
    c=sum(x['avg']*x['games'] for x in sc)/gtot
    v=evf(p,Y)/F
    s0=p['scoring']; p['scoring']=[]
    try: vcf=evf(p,Y)/F
    finally: p['scoring']=s0
    live.append({'key':p.get('key'),'player':p.get('player') or p.get('name'),
                 'pos':MA.GRP.get(p.get('pos')),'pick':p.get('pick'),'stream':p.get('draft_stream') or p.get('type'),
                 'tenure':Y-int(p.get('year') or Y)+1,'entry_age':entry_age(p),
                 'games':int(gtot),'cameo':round(c,1),'cur':round(v),'cf':round(vcf)})

# M1 — pedigree ordering: same tenure, comparable evidence, materially better pedigree (cf), lower price
pairs=[]
for a in live:
    for b in live:
        if a['key']>=b['key']: continue
        A,B=(a,b) if a['cf']>=b['cf'] else (b,a)          # A = better pedigree
        if A['tenure']!=B['tenure']: continue
        if abs(A['cameo']-B['cameo'])>4 or abs(A['games']-B['games'])>3: continue
        if A['cf'] < 1.5*B['cf']: continue                # materially better pedigree
        if A['cur'] < B['cur']:                           # ...priced BELOW
            pairs.append({'better_pedigree':A['player'],'A_cf':A['cf'],'A_cur':A['cur'],'A_cameo':A['cameo'],'A_g':A['games'],'A_pos':A['pos'],
                          'worse_pedigree':B['player'],'B_cf':B['cf'],'B_cur':B['cur'],'B_cameo':B['cameo'],'B_g':B['games'],'B_pos':B['pos'],
                          'tenure':A['tenure'],'same_pos':A['pos']==B['pos'],'gap':B['cur']-A['cur']})
pairs.sort(key=lambda x:-x['gap'])
OUT['M1_pedigree_pairs']={'n':len(pairs),'n_same_pos':sum(1 for x in pairs if x['same_pos']),'pairs':pairs}

# M2 — historical: weak-cameo resolution by KP vs non-KP (as-of tenure states, resolved cohorts)
def tbp(p):
    a=sorted([x['avg'] for x in p['scoring'] if x['games']>=6],reverse=True)[:3]
    return float(np.mean(a)) if a else 0.0
KP={'KPF','KPD','RUCK'}
cells={}
for p in MA.data:
    grp=MA.GRP.get(p.get('pos'))
    if not grp: continue
    try: d=MA.debut(p)
    except Exception: d=None
    if not d or not (2006<=d<=2021): continue
    sc=sorted([x for x in (p.get('scoring') or [])],key=lambda x:x['year'])
    for t in (2,3,4):
        w=[x for x in sc if d<=x['year']<d+t]
        gtot=sum(x['games'] for x in w)
        if gtot<1 or gtot>8 or any(x['games']>=6 for x in w): continue
        c=sum(x['avg']*x['games'] for x in w)/gtot
        band='<35' if c<35 else ('35-45' if c<45 else '45+')
        kp='KP' if grp in KP else 'nonKP'
        cells.setdefault((t,kp,band),[]).append(tbp(p))
OUT['M2_kp_forgiveness']={'%d|%s|%s'%k: {'n':len(v),'mean_best3':round(float(np.mean(v)),1),
    'p70':round(float(np.mean([1 if x>=70 else 0 for x in v])),2),
    'bust0':round(float(np.mean([1 if x==0 else 0 for x in v])),2)} for k,v in sorted(cells.items())}

# M3 — mature-age flags on the live population
OUT['M3_mature_age']=[r for r in live if (r['entry_age'] or 0)>=22]

# M4 — tenure 5+ split
t5=[r for r in live if r['tenure']>4]
OUT['M4_t5plus']={'ordinary_draftee':[r for r in t5 if (r['entry_age'] or 99)<22],
                  'mature_age':[r for r in t5 if (r['entry_age'] or 0)>=22]}

# positional effective bars (REPL - 3), for the KP-scaled knot proposal
try:
    repl=dict(MA.REPL)
    OUT['bars_repl_minus3']={k:(float(v)-3.0) for k,v in repl.items()} if isinstance(repl,dict) else str(type(repl))
except Exception as e:
    OUT['bars_repl_minus3']='ERR %s'%e
json.dump(OUT, open('/home/user/seam_fix/round2.json','w'), indent=1)
print('M1 pedigree pairs:', OUT['M1_pedigree_pairs']['n'], '(same-pos:', OUT['M1_pedigree_pairs']['n_same_pos'],')')
for x in pairs[:10]:
    print('  t%d %-20s (cf %4d, now %4d, %4.1f avg/%dg %s)  <  %-20s (cf %4d, now %4d, %4.1f avg/%dg %s)  gap %d' %
          (x['tenure'],x['better_pedigree'],x['A_cf'],x['A_cur'],x['A_cameo'],x['A_g'],x['A_pos'],
           x['worse_pedigree'],x['B_cf'],x['B_cur'],x['B_cameo'],x['B_g'],x['B_pos'],x['gap']))
print('M2 cells:')
for k,v in OUT['M2_kp_forgiveness'].items():
    print('  %-12s n=%3d  mean best-3 %5.1f  P(70+) %.2f  P(bust) %.2f' % (k,v['n'],v['mean_best3'],v['p70'],v['bust0']))
print('M3 mature-age live rows:', [(r['player'],r['entry_age'],r['tenure']) for r in OUT['M3_mature_age']])
print('M4 t5+ ordinary:', [(r['player'],r['cameo'],r['cur'],r['cf']) for r in OUT['M4_t5plus']['ordinary_draftee']])
print('M4 t5+ mature :', [(r['player'],r['cameo'],r['cur'],r['cf']) for r in OUT['M4_t5plus']['mature_age']])
