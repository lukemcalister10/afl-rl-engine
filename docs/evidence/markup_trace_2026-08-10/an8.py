import json
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
mbar=A(d,lambda x:x['v0'])/A(d,lambda x:x['v0u']); pbar=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['v0u'])
k=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['s6_price']*(x['v0']/x['v0u']))   # conserve the leg book exactly
print("CF-A  'give every player the LEG production re-pricing on his own raw year-0 value':  price = v0_uncapped x %.4f"%pbar)
print("CF-B  'carry the year-0 lens multiplier m into the year-1 price, leg book conserved':  price = %.4f x price x m"%k)
print()
print(f"{'cell':14s} {'n':>4s} {'m_pos':>6s} {'E_now':>9s} {'CF-A':>9s} {'CF-B':>9s} | {'A closes':>9s} {'B closes':>9s}")
def line(lbl,r):
    if not r: return
    E=A(r,lambda x:x['s6_price']-x['s6_F'])
    EA=A(r,lambda x:x['v0u']*pbar-x['s6_F'])
    EB=A(r,lambda x:k*x['s6_price']*(x['v0']/x['v0u'])-x['s6_F'])
    m=A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u'])
    print(f"{lbl:14s} {len(r):4d} {m:6.3f} {E:9.0f} {EA:9.0f} {EB:9.0f} | {E-EA:9.0f} {E-EB:9.0f}")
line('LEG',d)
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']: line(p,[x for x in d if x['pos']==p])
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    for lbl,f in [(' y<=18',lambda x:x['age'] is not None and x['age']<=18),(' m19+',lambda x:x['age'] is not None and x['age']>=19),(' unk',lambda x:x['age'] is None)]:
        line(p+lbl,[x for x in d if x['pos']==p and f(x)])
