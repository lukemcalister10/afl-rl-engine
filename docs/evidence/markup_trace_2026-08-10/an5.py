import json,statistics as st
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
LS=A(d,lambda x:x['v0u'])/A(d,lambda x:x['v0']); LP=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['v0u']); LM=LS*LP
def line(lbl,r):
    if len(r)<1: return
    n=len(r); P=A(r,lambda x:x['s6_price']); V=A(r,lambda x:x['v0']); U=A(r,lambda x:x['v0u']); F=A(r,lambda x:x['s6_F'])
    surf=U/V; prod=P/U; mk=P/V; f1=F/P
    xs=surf/LS; xp=prod/LP
    ps=P*(1-1/xs); pp=P/xs*(1-1/xp); pb=V*LM-F
    print(f"{lbl:14s} {n:4d} {mk:6.3f} {f1:6.3f} {mk*f1:6.3f} {P-F:9.0f} {(P-F)/n:7.0f} | {surf:6.3f} {xs:6.3f} {ps:9.0f} | {prod:6.3f} {xp:6.3f} {pp:8.0f} | {pb:9.0f}  chk {ps+pp+pb-(P-F):8.1f}")
print("leg surf %.4f  leg prod %.4f  leg markup %.4f"%(LS,LP,LM))
print(f"{'cell':14s} {'n':>4s} {'mkup':>6s} {'F1':>6s} {'honest':>6s} {'excess':>9s} {'exc/pl':>7s} | {'surf':>6s} {'xS':>6s} {'ptsSURF':>9s} | {'prod':>6s} {'xP':>6s} {'ptsPROD':>8s} | {'ptsBASE':>9s}")
line('LEG',d)
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']: line(p,[x for x in d if x['pos']==p])
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    for lbl,f in [('y<=18',lambda x:x['age'] is not None and x['age']<=18),('m19+',lambda x:x['age'] is not None and x['age']>=19),('unk',lambda x:x['age'] is None)]:
        line(p+' '+lbl,[x for x in d if x['pos']==p and f(x)])
print()
print("=== the year-0 lens factor m = v0_shipped / v0_uncapped, by position x pick band (n) ===")
print(f"{'pos':6s} " + ' '.join(f'{b:>14s}' for b in ['pk1-10','pk11-20','pk21-40','pk41-64']))
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    out=[]
    for lo,hi in [(1,10),(11,20),(21,40),(41,64)]:
        r=[x for x in d if x['pos']==p and lo<=x['pk']<=hi]
        out.append(f"{(A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u'])):.3f}({len(r)})" if r else '   -   ')
    print(f"{p:6s} " + ' '.join(f'{o:>14s}' for o in out))
