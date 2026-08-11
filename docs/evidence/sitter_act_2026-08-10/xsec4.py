import json, statistics as st, random
random.seed(11)
G=1.0939
d=json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/matrix.json'))['recs']
S=[r for r in d if r['type']=='ND' and 2004<=r['year']<=2022 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]
def vp(r,i): return float(r['vpath'][i]) if len(r['vpath'])>i else 0.0
for r in S: r['_g2']=r['games_by'].get('2',0)
def kpp(r): return r['pos'] in ('KPD','KPF','RUCK')

def Fh(rows,base,hor):
    return sum(vp(r,hor)/G**(hor-base) for r in rows)/sum(vp(r,base) for r in rows)
def boot(rows,fn,B=8000):
    n=len(rows);out=[]
    for _ in range(B):
        sam=[rows[random.randrange(n)] for _ in range(n)]
        out.append(fn(sam))
    out.sort();return fn(rows),out[int(.025*B)],out[int(.975*B)-1]
def effn(rows,base):
    ws=[vp(r,base) for r in rows];s=sum(ws);return s*s/sum(w*w for w in ws)

print('=== HORIZON CHECK: is the 2018-22 shortfall a maturity artifact? (F from the year-1 price to horizon h)')
print('    only entry years with the horizon elapsed by 2026 are included in each column')
for lab,f in [('2004-2017',lambda r:r['year']<2018),('2018-2022',lambda r:r['year']>=2018)]:
    for hor in [1,2,3,4,5]:
        rs=[r for r in S if f(r) and r['year']+1+hor<=2026]
        if len(rs)<20: continue
        print(f"  {lab}  h=yr{hor+1}  n={len(rs):>3}  F={Fh(rs,0,hor):.3f}")

print()
print('=== F BY ENTRY YEAR (year-1 price -> discounted year-4)')
for y in range(2004,2023):
    rs=[r for r in S if r['year']==y]
    print(f"  {y}  n={len(rs):>3}  F={Fh(rs,0,3):.3f}  playyr2={sum(1 for r in rs if r['_g2']>0)/len(rs):.2f}  never={sum(1 for r in rs if r['games_total']==0)/len(rs):.2f}")

print()
print('=== THE YEAR-2 EVALUATION (base = price at end of year 2 = vpath[1]; outcome = discounted year-4)')
def F2(rows): return Fh(rows,1,3)
for lab,rs in [('ALL sitters',S),
               ('played yr2',[r for r in S if r['_g2']>0]),
               ('sat yr2 again',[r for r in S if r['_g2']==0]),
               ('KPP played yr2',[r for r in S if kpp(r) and r['_g2']>0]),
               ('KPP sat yr2',[r for r in S if kpp(r) and r['_g2']==0]),
               ('SMALL played yr2',[r for r in S if not kpp(r) and r['_g2']>0]),
               ('SMALL sat yr2',[r for r in S if not kpp(r) and r['_g2']==0])]:
    pt,lo,hi=boot(rs,F2)
    e=effn(rs,1); clear='CLEAR' if (lo>1 or hi<1) else '.'
    print(f"  {lab:<18} n={len(rs):>4} effn={e:>6.1f} F2={pt:.3f} CI[{lo:.3f},{hi:.3f}] {clear}{'  F8' if clear=='CLEAR' and e>=35 else ''}")
# what the clock charges between yr1 and yr2 for each
for lab,rs in [('played yr2',[r for r in S if r['_g2']>0]),('sat yr2 again',[r for r in S if r['_g2']==0])]:
    print(f"  {lab:<18} clock move yr1->yr2 = {sum(vp(r,1) for r in rs)/sum(vp(r,0) for r in rs):.3f}x   realized(disc yr4 from yr2 price) = {F2(rs):.3f}")

print()
print('=== VALUE MOVEMENT, historic cohort (mass = year-1 price at the year-1 evaluation)')
tot=sum(vp(r,0) for r in S)
print(f"  total year-1 mass of the 496 sitters = {tot:,.0f}")
for lab,rs in [('KPP',[r for r in S if kpp(r)]),('SMALL',[r for r in S if not kpp(r)])]:
    m=sum(vp(r,0) for r in rs); F=Fh(rs,0,3)
    print(f"  {lab:<6} mass={m:,.0f} ({m/tot:.0%})  F={F:.3f}  move={m*(F-1):+,.0f} ({(F-1):+.1%} of the cell)")
print(f"  net = {sum(sum(vp(r,0) for r in rs)*(Fh(rs,0,3)-1) for rs in [[r for r in S if kpp(r)],[r for r in S if not kpp(r)]]):+,.0f} ({sum(sum(vp(r,0) for r in rs)*(Fh(rs,0,3)-1) for rs in [[r for r in S if kpp(r)],[r for r in S if not kpp(r)]])/tot:+.1%} of mass) -- gross reallocation = {sum(abs(sum(vp(r,0) for r in rs)*(Fh(rs,0,3)-1)) for rs in [[r for r in S if kpp(r)],[r for r in S if not kpp(r)]]):,.0f}")
print()
print('  year-2 conditioned split (mass = price at end of year 2):')
tot2=sum(vp(r,1) for r in S)
for lab,rs in [('played yr2',[r for r in S if r['_g2']>0]),('sat yr2 again',[r for r in S if r['_g2']==0])]:
    m=sum(vp(r,1) for r in rs); F=F2(rs)
    print(f"  {lab:<16} mass={m:,.0f} ({m/tot2:.0%})  F2={F:.3f}  move={m*(F-1):+,.0f} ({(F-1):+.1%})")
mv=[(sum(vp(r,1) for r in rs))*(F2(rs)-1) for rs in [[r for r in S if r['_g2']>0],[r for r in S if r['_g2']==0]]]
print(f"  net={sum(mv):+,.0f} ({sum(mv)/tot2:+.1%})  gross reallocation={sum(abs(x) for x in mv):,.0f} ({sum(abs(x) for x in mv)/tot2:.1%} of the year-2 mass)")
