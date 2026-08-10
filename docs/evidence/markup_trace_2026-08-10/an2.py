import json,statistics as st
d=json.load(open('decomp_b.json'))
def A(rows,f): return sum(f(x) for x in rows)
def cell(lbl,r):
    if len(r)<1: return
    n=len(r)
    P=A(r,lambda x:x['s6_price']); V=A(r,lambda x:x['v0']); U=A(r,lambda x:x['v0u'])
    E=A(r,lambda x:x['e1']); F=A(r,lambda x:x['s6_F'])
    pr0=A(r,lambda x:x['y0']['pr']*x['y0']['iso']); pr1=A(r,lambda x:x['y1']['pr']*x['y1']['iso'])
    C1=A(r,lambda x:x['y1']['pole_credit']*x['y1']['iso'])
    print(f"{lbl:14s} {n:4d} | mk {P/V:6.3f} = surf {U/V:6.3f} x prod {P/U:6.3f} | prodsplit: band {pr1/pr0:6.3f} pole+ {1+C1/pr1:6.3f} other {(P/U)/((pr1/pr0)*(1+C1/pr1)):6.3f} | F1 {F/P:6.3f}")
print("markup = (v0_uncapped/v0_shipped) x (price/v0_uncapped);  band = pr1*iso1 / pr0*iso0")
cell('LEG',d)
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']: cell(p,[x for x in d if x['pos']==p])
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    for lbl,f in [('y<=18',lambda x:x['age'] is not None and x['age']<=18),('m19+',lambda x:x['age'] is not None and x['age']>=19),('unk',lambda x:x['age'] is None)]:
        cell(p+' '+lbl,[x for x in d if x['pos']==p and f(x)])
print()
print("pole credit distribution (share of year-1 price)")
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if x['pos']==p]
    sh=sorted(x['y1']['pole_credit']*x['y1']['iso']/max(x['s6_price'],1) for x in r)
    nz=[s for s in sh if s>0.001]
    print(f"  {p:5s} n={len(r):3d}  n_with_credit={len(nz):3d}  max_share={sh[-1]:.3f}  aggregate_share={A(r,lambda x:x['y1']['pole_credit']*x['y1']['iso'])/A(r,lambda x:x['s6_price']):.4f}")
