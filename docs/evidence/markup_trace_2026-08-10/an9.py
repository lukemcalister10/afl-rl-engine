import json
D=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
d=[x for x in D if x['age'] is not None and x['age']<=18]
k=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['s6_price']*(x['v0']/x['v0u']))
pbar=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['v0u'])
print("YOUNG LEG ONLY (draft age <=18, n=%d).  book-conserving lens-carry constant k=%.4f ; leg prod %.4f"%(len(d),k,pbar))
print(f"{'pos':6s} {'n':>4s} {'m':>6s} {'mkup':>6s} {'F1':>6s} {'E_now':>8s} {'E_lenscarry':>12s} {'closed%':>8s}")
for p in ['ALL','MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if p=='ALL' or x['pos']==p]
    if not r: continue
    E=A(r,lambda x:x['s6_price']-x['s6_F']); EB=A(r,lambda x:k*x['s6_price']*(x['v0']/x['v0u'])-x['s6_F'])
    m=A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u']); P=A(r,lambda x:x['s6_price']); V=A(r,lambda x:x['v0']); F=A(r,lambda x:x['s6_F'])
    print(f"{p:6s} {len(r):4d} {m:6.3f} {P/V:6.3f} {F/P:6.3f} {E:8.0f} {EB:12.0f} {(1-abs(EB)/max(abs(E),1e-9))*100:7.1f}%")
print()
print("=== B5 pricing floor (price = 0.45 x v0_start) bind count on the leg ===")
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in D if x['pos']==p]
    b=[x for x in r if x['s6_price']>x['e1']+0.6]
    print(f"  {p:5s} {len(b):3d}/{len(r):3d} floor-bound, total lift {A(b,lambda x:x['s6_price']-x['e1']):7.0f}")
print()
print("=== RUCK: v0_uncapped -> v0_raw (ruck prior cap) -> v0_start (lens), and the year-1 production cap ===")
print(f"{'key':24s}{'pk':>4s}{'v0u':>7s}{'v0r':>7s}{'v0':>7s}{'e_prod':>8s}{'price':>7s}{'F':>7s}{'cap cut':>8s}")
for x in sorted([z for z in D if z['pos']=='RUCK'],key=lambda z:z['pk']):
    print(f"{x['key']:24s}{x['pk']:4d}{x['v0u']:7.0f}{x['v0r']:7.0f}{x['v0']:7.0f}{x['e1']:8.0f}{x['s6_price']:7.0f}{x['s6_F']:7.0f}{x['s6_price']-x['e1']:8.0f}")
