import json, statistics as st, random
random.seed(7)
DF=1.0939**3
d=json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/matrix.json'))['recs']
S=[r for r in d if r['type']=='ND' and 2004<=r['year']<=2022 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]
def v4(r): return float(r['vpath'][3]) if len(r['vpath'])>=4 else 0.0
for r in S:
    r['_w']=float(r['vpath'][0]); r['_o']=v4(r)/DF
    r['_g2']=r['games_by'].get('2',0)
    s2=[s for s in r['seasons'] if s['year']==r['year']+2]
    r['_a2']=s2[0]['avg'] if s2 else 0.0
def F(rows): return sum(r['_o'] for r in rows)/sum(r['_w'] for r in rows)
def effn(rows):
    ws=[r['_w'] for r in rows]; s=sum(ws); return s*s/sum(w*w for w in ws)
def boot(rows,B=10000):
    n=len(rows); out=[]
    for _ in range(B):
        sam=[rows[random.randrange(n)] for _ in range(n)]
        out.append(F(sam))
    out.sort(); return F(rows),out[int(.025*B)],out[int(.975*B)-1]
def pr(lab,rows):
    if len(rows)<5: print(f'{lab:<22} n={len(rows)} too thin'); return
    pt,lo,hi=boot(rows)
    clear='CLEAR' if (lo>1 or hi<1) else '.'
    f8='F8' if (clear=='CLEAR' and effn(rows)>=35) else ''
    print(f"{lab:<22} n={len(rows):>4} effn={effn(rows):>6.1f} F={pt:.3f} CI[{lo:.3f},{hi:.3f}] {clear:<6}{f8}")

print('=== YEAR-2 DOSE RESPONSE (games played in year 2)')
for lab,f in [('yr2 = 0 games',lambda r:r['_g2']==0),('yr2 1-5',lambda r:1<=r['_g2']<=5),
              ('yr2 6-11',lambda r:6<=r['_g2']<=11),('yr2 12-17',lambda r:12<=r['_g2']<=17),
              ('yr2 18+',lambda r:r['_g2']>=18)]:
    pr(lab,[r for r in S if f(r)])
print()
print('=== YEAR-2 QUALITY (season average, among those who played yr2)')
P=[r for r in S if r['_g2']>0]
q=sorted(r['_a2'] for r in P); t1,t2=q[len(q)//3],q[2*len(q)//3]
print(f'  tercile cuts on yr2 avg: {t1:.1f} / {t2:.1f}')
for lab,f in [('yr2 avg low',lambda r:r['_a2']<t1),('yr2 avg mid',lambda r:t1<=r['_a2']<t2),('yr2 avg high',lambda r:r['_a2']>=t2)]:
    pr(lab,[r for r in P if f(r)])
print()
print('=== VOLUME vs QUALITY horse race (the owner hypothesis: does "whether" beat "how well"?)')
med_g=st.median(r['_g2'] for r in P); med_a=st.median(r['_a2'] for r in P)
print(f'  median yr2 games among players={med_g:.0f}, median yr2 avg={med_a:.1f}')
for lab,f in [('few games, low avg',lambda r:r['_g2']<=med_g and r['_a2']<med_a),
              ('few games, high avg',lambda r:r['_g2']<=med_g and r['_a2']>=med_a),
              ('many games, low avg',lambda r:r['_g2']>med_g and r['_a2']<med_a),
              ('many games, high avg',lambda r:r['_g2']>med_g and r['_a2']>=med_a)]:
    pr(lab,[r for r in P if f(r)])
print()
print('=== ERA ROBUSTNESS (trim the top realized outcomes)')
for lab,f in [('2004-2017',lambda r:r['year']<2018),('2018-2022',lambda r:r['year']>=2018)]:
    rs=[r for r in S if f(r)]
    rs_s=sorted(rs,key=lambda r:-r['_o'])
    print(f"{lab}: full F={F(rs):.3f}  drop-top1={F(rs_s[1:]):.3f}  drop-top3={F(rs_s[3:]):.3f}  drop-top5%={F(rs_s[max(1,len(rs)//20):]):.3f}")
    print("    top realized: "+', '.join('%s(pk%d,%d,%.1fx)'%(r['player'],r['pick'],r['year'],r['_o']/r['_w']) for r in rs_s[:4]))
print()
print('=== 2018-2022 BREAKDOWN')
def band(r):
    p=r['pick']; return '1-20' if p<=20 else '21-35' if p<=35 else '36-48' if p<=48 else '49-64'
for b in ['1-20','21-35','36-48','49-64']:
    pr('2018-22 '+b,[r for r in S if r['year']>=2018 and band(r)==b])
for b in ['1-20','21-35','36-48','49-64']:
    pr('2004-17 '+b,[r for r in S if r['year']<2018 and band(r)==b])
