import json,statistics as st
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
LEGsurf=A(d,lambda x:x['v0u'])/A(d,lambda x:x['v0'])
LEGprod=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['v0u'])
print("leg surf = v0u/v0 = %.4f    leg prod = price/v0u = %.4f    (n=%d, yarran v0u=0 dropped)"%(LEGsurf,LEGprod,len(d)))
print()
print(f"{'pos':6s} {'n':>4s} {'mkup':>6s} {'F1':>6s} {'honest':>6s} | {'surf':>6s} {'x_surf':>7s} {'pts_surf':>9s} | {'prod':>6s} {'x_prod':>7s} {'pts_prod':>9s} | {'excess':>9s}")
for pos in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if x['pos']==pos]; n=len(r)
    P=A(r,lambda x:x['s6_price']); V=A(r,lambda x:x['v0']); U=A(r,lambda x:x['v0u']); F=A(r,lambda x:x['s6_F'])
    surf=U/V; prod=P/U; mk=P/V; f1=F/P
    xs=surf/LEGsurf; xp=prod/LEGprod
    pts_s=P*(1-1/xs); pts_p=P*(1/xs)*(1-1/xp)
    print(f"{pos:6s} {n:4d} {mk:6.3f} {f1:6.3f} {mk*f1:6.3f} | {surf:6.3f} {xs:7.3f} {pts_s:9.0f} | {prod:6.3f} {xp:7.3f} {pts_p:9.0f} | {P-F:9.0f}")
print()
print("x_surf = the position's year-0 lens factor relative to the leg's; x_prod = its production re-pricing relative to the leg's.")
print("pts_surf = points of the position's year-1 book that exist only because its year-0 lens factor differs from the leg average.")
