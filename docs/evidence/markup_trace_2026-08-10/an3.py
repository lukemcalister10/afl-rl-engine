import json,statistics as st
d=json.load(open('decomp_b.json'))
def A(r,f): return sum(f(x) for x in r)
print("=== COUNTERFACTUAL: carry the year-0 lens multiplier m = v0/v0_uncapped into the year-1 price ===")
print(f"{'pos':6s} {'n':>4s} | {'excess_now':>11s} {'exc/pl':>8s} | {'excess_lens':>11s} {'exc/pl':>8s} | {'removed%':>8s} | {'m(lens)':>7s}")
tot=[0,0]
for pos in ['MID','SD','SF','KPF','KPD','RUCK','LEG']:
    r=[x for x in d if pos=='LEG' or x['pos']==pos]; n=len(r)
    ex=A(r,lambda x:x['s6_price']-x['s6_F'])
    exl=A(r,lambda x:x['e1']*(x['v0']/x['v0u'])-x['s6_F'])
    m=A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u'])
    rem=(1-abs(exl)/max(abs(ex),1e-9))*100
    print(f"{pos:6s} {n:4d} | {ex:11.0f} {ex/n:8.0f} | {exl:11.0f} {exl/n:8.0f} | {rem:7.1f}% | {m:7.3f}")
print()
print("=== the pole gap: po/pr at year 1 (why KPF/RUCK get zero pole credit) ===")
for pos in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if x['pos']==pos]
    v=sorted(x['y1']['po']/x['y1']['pr'] for x in r)
    print(f"  {pos:5s} n={len(r):3d} median po/pr = {st.median(v):6.3f}  p90 = {v[int(.9*len(v))]:7.3f}  frac>1 = {sum(1 for z in v if z>1)/len(v):.2f}   mean _SCALE-stripped po/pr = {st.mean(x['y1']['pole_unscaled']/x['y1']['pr'] for x in r):6.3f}")
print()
print("=== RUCK: where the year-1 price is cut ===")
for x in [z for z in d if z['pos']=='RUCK']:
    print("  %-22s pk%-3d e1=%7.0f price=%6.0f v0=%6.0f v0u=%6.0f  F=%7.0f  cut=%6.0f" % (x['key'],x['pk'],x['e1'],x['s6_price'],x['v0'],x['v0u'],x['s6_F'],x['s6_price']-x['e1']))
print()
print("=== B5 floor bind (price = 0.45*v0) ===")
for pos in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if x['pos']==pos]
    b=[x for x in r if x['s6_price']>x['e1']+0.6]
    print(f"  {pos:5s} floor-bound {len(b):3d}/{len(r):3d}   lift = {A(b,lambda x:x['s6_price']-x['e1']):7.0f}")
