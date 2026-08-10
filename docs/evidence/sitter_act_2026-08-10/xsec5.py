import json, statistics as st, random
random.seed(3)
G=1.0939
d=json.load(open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/matrix.json'))['recs']
S=[r for r in d if r['type']=='ND' and 2004<=r['year']<=2022 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]
def vp(r,i): return float(r['vpath'][i]) if len(r['vpath'])>i else 0.0
def kpp(r): return r['pos'] in ('KPD','KPF','RUCK')
def F(rows): return sum(vp(r,3)/G**3 for r in rows)/sum(vp(r,0) for r in rows)
def boot(rows,fn,B=8000):
    n=len(rows);out=[]
    for _ in range(B):
        out.append(fn([rows[random.randrange(n)] for _ in range(n)]))
    out.sort();return fn(rows),out[int(.025*B)],out[int(.975*B)-1]
def effn(rows):
    ws=[vp(r,0) for r in rows];s=sum(ws);return s*s/sum(w*w for w in ws)

print('=== ERA, maturity-clean sub-window (6+ seasons elapsed for every entrant)')
for lab,f in [('2004-2017',lambda r:r['year']<2018),('2018-2020',lambda r:2018<=r['year']<=2020),('2021-2022',lambda r:r['year']>=2021)]:
    rs=[r for r in S if f(r)]
    pt,lo,hi=boot(rs,F)
    print(f"  {lab:<12} n={len(rs):>4} effn={effn(rs):>6.1f} F={pt:.3f} CI[{lo:.3f},{hi:.3f}] never={sum(1 for r in rs if r['games_total']==0)/len(rs):.2f}")

print()
print('=== LIVE EXPOSURE: today\'s year-1 sitters still inside the clock (ND pick 1-64, entry 2023-2025, zero games in year 1)')
L=[r for r in d if r['type']=='ND' and 2023<=r['year']<=2025 and r.get('pick') and 1<=r['pick']<=64 and r['games_yr1']==0]
print(f"  n={len(L)}   current board mass (cur) = {sum(r['cur'] for r in L):,.0f}")
for lab,f in [('KPP',kpp),('SMALL',lambda r:not kpp(r))]:
    rs=[r for r in L if f(r)]
    m=sum(r['cur'] for r in rs)
    print(f"  {lab:<6} n={len(rs):>3} cur mass={m:,.0f}")
print()
print('  by entry year x position:')
for y in [2023,2024,2025]:
    rs=[r for r in L if r['year']==y]
    if not rs: continue
    k=[r for r in rs if kpp(r)]; s=[r for r in rs if not kpp(r)]
    print(f"   {y}: n={len(rs):>3}  KPP n={len(k)} cur={sum(x['cur'] for x in k):,.0f}   SMALL n={len(s)} cur={sum(x['cur'] for x in s):,.0f}")
print()
print('  the largest live exposures (top 15 by current price):')
for r in sorted(L,key=lambda r:-r['cur'])[:15]:
    g2=r['games_by'].get('2',0)
    print(f"   {r['player']:<24} pk{r['pick']:<3} {r['year']} {r['pos']:<5} cur={r['cur']:>5}  v0={r['v0']:>6.0f}  yr2 games={g2:>3}  total={r['games_total']}")
print()
print('=== DIRECTIONAL MOVEMENT ON THE LIVE BOOK (applying the measured cell factors as a pure scaling of the sit-charge)')
KPP_F, SM_F = F([r for r in S if kpp(r)]), F([r for r in S if not kpp(r)])
mk=sum(r['cur'] for r in L if kpp(r)); ms=sum(r['cur'] for r in L if not kpp(r))
print(f"  KPP   factor {KPP_F:.3f}  live mass {mk:,.0f}  ->  {mk*(KPP_F-1):+,.0f}")
print(f"  SMALL factor {SM_F:.3f}  live mass {ms:,.0f}  ->  {ms*(SM_F-1):+,.0f}")
print(f"  net {mk*(KPP_F-1)+ms*(SM_F-1):+,.0f} on a live sitter book of {mk+ms:,.0f} ({(mk*(KPP_F-1)+ms*(SM_F-1))/(mk+ms):+.1%}); gross reallocation {abs(mk*(KPP_F-1))+abs(ms*(SM_F-1)):,.0f} ({(abs(mk*(KPP_F-1))+abs(ms*(SM_F-1)))/(mk+ms):.1%})")
print()
print('  as a share of the whole 2026 board:')
board=sum(r['cur'] for r in d)
print(f"   whole-matrix current mass = {board:,.0f}; live sitter book = {(mk+ms)/board:.2%} of it; gross reallocation = {(abs(mk*(KPP_F-1))+abs(ms*(SM_F-1)))/board:.3%} of the board")
print()
print('=== SECOND-SIT LIVE SET (entry 2023-2024 who sat year 1 AND year 2) -- the F8-clear over-price')
S2=[r for r in L if r['year']<=2024 and r['games_by'].get('2',0)==0]
print(f"  n={len(S2)} cur mass={sum(r['cur'] for r in S2):,.0f}")
sm2=[r for r in S2 if not kpp(r)]
print(f"  of which SMALL (the F8-clear cell, F2=0.654): n={len(sm2)} cur mass={sum(r['cur'] for r in sm2):,.0f} -> {sum(r['cur'] for r in sm2)*(0.654-1):+,.0f}")
for r in sorted(S2,key=lambda r:-r['cur'])[:12]:
    print(f"   {r['player']:<24} pk{r['pick']:<3} {r['year']} {r['pos']:<5} cur={r['cur']:>5} total games={r['games_total']}")
