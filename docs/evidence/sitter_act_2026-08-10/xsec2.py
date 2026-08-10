import json, statistics as st, random
random.seed(20260810)
DF = 1.0939**3
d = json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/matrix.json'))['recs']
S = [r for r in d if r['type']=='ND' and 2004<=r['year']<=2022 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]
def v4(r): return float(r['vpath'][3]) if len(r['vpath'])>=4 else 0.0
for r in S:
    r['_w']=float(r['vpath'][0]); r['_o']=v4(r)/DF; r['_v0']=float(r['v0'])
    r['_g2']=r['games_by'].get('2',0); r['_np']=(r['games_total']==0)

def band(r):
    p=r['pick']
    return '1-12' if p<=12 else '13-20' if p<=20 else '21-27' if p<=27 else '28-35' if p<=35 else '36-48' if p<=48 else '49-64'
def kpp(r): return r['pos'] in ('KPD','KPF','RUCK')
def eff_n(ws):
    s=sum(ws); return (s*s)/sum(w*w for w in ws)

def bootstat(rows, f, B=10000):
    n=len(rows); pt=f(rows); out=[]
    for _ in range(B):
        sam=[rows[random.randrange(n)] for _ in range(n)]
        out.append(f(sam))
    out.sort(); return pt, out[int(.025*B)], out[int(.975*B)-1]

def F(rows): return sum(r['_o'] for r in rows)/sum(r['_w'] for r in rows)
def Fv0(rows): return sum(r['_o'] for r in rows)/sum(r['_v0'] for r in rows)
def Rch(rows): return sum(r['_w'] for r in rows)/sum(r['_v0'] for r in rows)

print('=== CLOCK CHARGE vs REALIZED, by cell (R_charged = yr1 price / v0 ; R_real = discounted yr4 / v0 ; F = R_real/R_charged)')
def line(name, rows):
    if not rows: return
    print(f"{name:<20} n={len(rows):>4} effn={eff_n([r['_w'] for r in rows]):>6.1f}  R_ch={Rch(rows):.3f}  R_real={Fv0(rows):.3f}  F={F(rows):.3f}")
cells=[('ALL',S)]
for p in ['KPD','KPF','RUCK','MID','SD','SF']: cells.append((p,[r for r in S if r['pos']==p]))
for b in ['1-12','13-20','21-27','28-35','36-48','49-64']: cells.append((b,[r for r in S if band(r)==b]))
cells.append(('KPP',[r for r in S if kpp(r)])); cells.append(('SMALL',[r for r in S if not kpp(r)]))
cells.append(('play yr2',[r for r in S if r['_g2']>0])); cells.append(('sit yr2',[r for r in S if r['_g2']==0]))
for n_,rs in cells: line(n_,rs)

print()
print('=== CONTRASTS (bootstrap on the RATIO of two cells\' F; CI clear of 1 = the cells really differ)')
def contrast(nA, A, nB, B_, B=10000):
    pt = F(A)/F(B_); out=[]
    nA_,nB_=len(A),len(B_)
    for _ in range(B):
        a=[A[random.randrange(nA_)] for _ in range(nA_)]
        b=[B_[random.randrange(nB_)] for _ in range(nB_)]
        out.append(F(a)/F(b))
    out.sort()
    lo,hi=out[int(.025*B)],out[int(.975*B)-1]
    print(f"{nA} / {nB:<28} ratio={pt:.3f}  CI[{lo:.3f},{hi:.3f}]  {'CLEAR' if (lo>1 or hi<1) else 'straddles'}")
KPPs=[r for r in S if kpp(r)]; SM=[r for r in S if not kpp(r)]
contrast('KPP','',0,0) if False else None
contrast('KPP', KPPs, 'SMALL', SM)
contrast('KPF', [r for r in S if r['pos']=='KPF'], 'SMALL', SM)
contrast('RUCK', [r for r in S if r['pos']=='RUCK'], 'SMALL', SM)
contrast('KPD', [r for r in S if r['pos']=='KPD'], 'SMALL', SM)
contrast('play-yr2', [r for r in S if r['_g2']>0], 'sit-yr2', [r for r in S if r['_g2']==0])
contrast('picks1-20', [r for r in S if r['pick']<=20], 'picks21-64', [r for r in S if r['pick']>20])
contrast('picks1-35', [r for r in S if r['pick']<=35], 'picks36-64', [r for r in S if r['pick']>35])
contrast('2018-2022', [r for r in S if r['year']>=2018], '2004-2017', [r for r in S if r['year']<2018])
contrast('age17', [r for r in S if r.get('age_draft')==17], 'age18', [r for r in S if r.get('age_draft')==18])

print()
print('=== TAIL CONCENTRATION: share of realized (discounted) value from the top-k players in each cell')
for n_,rs in [('ALL',S),('KPP',KPPs),('SMALL',SM),('49-64',[r for r in S if band(r)=='49-64']),
              ('1-20',[r for r in S if r['pick']<=20]),('sit yr2',[r for r in S if r['_g2']==0]),
              ('play yr2',[r for r in S if r['_g2']>0])]:
    o=sorted((r['_o'] for r in rs), reverse=True); tot=sum(o)
    k5=max(1,int(round(.05*len(o)))); k10=max(1,int(round(.10*len(o))))
    zero=sum(1 for x in o if x==0)/len(o)
    print(f"{n_:<12} n={len(rs):>4} top5%={sum(o[:k5])/tot:.2f} top10%={sum(o[:k10])/tot:.2f}  zero-at-yr4 share of players={zero:.2f}")

print()
print('=== POSITION x YEAR-2 (the interaction: who recovers after a second sit)')
for p,lab in [(lambda r: kpp(r),'KPP'),(lambda r: not kpp(r),'SMALL')]:
    for g,glab in [(lambda r: r['_g2']>0,'play yr2'),(lambda r: r['_g2']==0,'sit yr2')]:
        rs=[r for r in S if p(r) and g(r)]
        pt,lo,hi=bootstat(rs,F)
        print(f"{lab:<6}{glab:<10} n={len(rs):>4} effn={eff_n([r['_w'] for r in rs]):>6.1f} F={pt:.3f} CI[{lo:.3f},{hi:.3f}] never={sum(r['_np'] for r in rs)/len(rs):.2f} play2rate")

print()
print('=== YEAR-2 RETURN RATE by year-1-observable cell (is year-2 play itself predictable at year 1?)')
for lab,f in [('KPD',lambda r:r['pos']=='KPD'),('KPF',lambda r:r['pos']=='KPF'),('RUCK',lambda r:r['pos']=='RUCK'),
              ('MID',lambda r:r['pos']=='MID'),('SD',lambda r:r['pos']=='SD'),('SF',lambda r:r['pos']=='SF'),
              ('pick1-12',lambda r:r['pick']<=12),('pick13-20',lambda r:13<=r['pick']<=20),('pick21-35',lambda r:21<=r['pick']<=35),
              ('pick36-48',lambda r:36<=r['pick']<=48),('pick49-64',lambda r:r['pick']>=49),
              ('age17',lambda r:r.get('age_draft')==17),('age18',lambda r:r.get('age_draft')==18),('age19+',lambda r:(r.get('age_draft') or 0)>=19)]:
    rs=[r for r in S if f(r)]
    print(f"{lab:<10} n={len(rs):>4} play-yr2={sum(1 for r in rs if r['_g2']>0)/len(rs):.2f}  never-play={sum(r['_np'] for r in rs)/len(rs):.2f}  median peak/v0={st.median(r['peak']/r['v0'] for r in rs):.2f}")
