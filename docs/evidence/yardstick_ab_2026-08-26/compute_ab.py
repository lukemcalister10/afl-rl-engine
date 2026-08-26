# FIRST-CUT A-vs-B derivation (owner sitting 2026-08-26). The packet's filed version follows the
# prereg'd derivation; the resolution convention is the owner's packet word. Run from repo root.
import json, statistics as st

SRC='/home/user/arm2_norec/noarb_sp_o45/per_entrant_ARM2CAND.json'
d=json.load(open(SRC))
recs=[r for r in d['recs'] if r['type']=='ND' and r.get('pick') and 2006<=r['year']<=2016 and r['pick']<=64]

R=0.14           # balanced-lens per-annum rate, dial 14 (rl_model LENS['bal'])
def grace(r): return 1 if (r.get('age_draft') or 18)<=19 else 0   # grace-A, entry age >19 => none

rows=[]
for r in recs:
    g=grace(r); vp=r['vpath']
    disc=lambda s: (1.0+R)**max(0, s-1-g)          # s=1 debut season == k=0 (never discounted); grace frees s=2
    b_exit=max(vp[i]/disc(i+1) for i in range(len(vp)))
    b_peak=max(vp)
    b_y3=(vp[2]/disc(3)) if len(vp)>=3 else 0.0
    s_star=max(range(len(vp)), key=lambda i: vp[i]/disc(i+1))+1
    rows.append(dict(key=r['key'],player=r['player'],pick=r['pick'],year=r['year'],pos=r['pos'],
                     v0=r['v0'],b_exit=round(b_exit,1),b_peak=b_peak,b_y3=round(b_y3,1),
                     s_star=s_star,games=r['games_total'],
                     active=not (r['retired_now'] or r['delisted'])))

def mean(xs): return sum(xs)/len(xs)
per_pick=[]
for p in range(1,65):
    g=[x for x in rows if x['pick']==p]
    if not g: continue
    per_pick.append(dict(pick=p,n=len(g),n_active=sum(1 for x in g if x['active']),
                         A=round(mean([x['v0'] for x in g]),1),
                         B=round(mean([x['b_exit'] for x in g]),1),
                         B_raw=round(mean([x['b_peak'] for x in g]),1),
                         B_y3=round(mean([x['b_y3'] for x in g]),1),
                         med_B=round(st.median([x['b_exit'] for x in g]),1)))

# position x band table
BANDS=[(1,5),(6,11),(12,20),(21,30),(31,40),(41,64)]
pos_bands=[]
for pos in ['MID','SD','SF','KPD','KPF','RUCK','ALL']:
    for lo,hi in BANDS:
        g=[x for x in rows if lo<=x['pick']<=hi and (pos=='ALL' or x['pos']==pos)]
        if len(g)<4: 
            pos_bands.append(dict(pos=pos,band=f'{lo}-{hi}',n=len(g),A=None,B=None,ratio=None)); continue
        A=mean([x['v0'] for x in g]); B=mean([x['b_exit'] for x in g])
        pos_bands.append(dict(pos=pos,band=f'{lo}-{hi}',n=len(g),A=round(A,1),B=round(B,1),ratio=round(B/A,3)))

tot_A=sum(x['v0'] for x in rows); tot_B=sum(x['b_exit'] for x in rows)
out=dict(meta=dict(source=SRC, src_meta={k:d['meta'][k] for k in ('store_md5','engine_head','n_records')},
                   cohorts='ND 2006-2016, picks 1-64', n=len(rows),
                   n_active=sum(1 for x in rows if x['active']),
                   rate=R, grace='grace-A: 1 free future season, entry age<=19 (board convention, ruling #334)',
                   conventions=dict(B='discounted best-exit: max over career seasons s of board value / 1.14^max(0,s-1-grace)',
                                    B_raw='raw career-peak board value, undiscounted',
                                    B_y3='season-3 board value discounted to day 0; careers shorter than 3 seasons count 0')),
         totals=dict(A=round(tot_A), B=round(tot_B), ratio=round(tot_B/tot_A,3)),
         per_pick=per_pick, pos_bands=pos_bands, players=rows)
json.dump(out, open('docs/evidence/yardstick_ab_2026-08-26/ab_curves.json','w'))
print('n',len(rows),'active',out['meta']['n_active'])
print('TOTALS  A',out['totals']['A'],' B',out['totals']['B'],' B/A',out['totals']['ratio'])
print('pick  n  A      B      B/A    Braw   By3')
for x in per_pick:
    print(f"{x['pick']:>4} {x['n']:>3} {x['A']:>7.0f} {x['B']:>7.0f} {x['B']/x['A']:>5.2f} {x['B_raw']:>7.0f} {x['B_y3']:>7.0f}")
print()
for pb in pos_bands:
    if pb['pos'] in ('ALL','SD','MID') and pb['ratio'] is not None:
        print(pb['pos'], pb['band'], 'n',pb['n'], 'A',pb['A'],'B',pb['B'],'B/A',pb['ratio'])
