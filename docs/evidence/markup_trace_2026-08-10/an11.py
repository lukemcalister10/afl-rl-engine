import json
ALL=[x for x in json.load(open('live.json')) if 2023<=x['C']<=2025]
DEG=[x for x in ALL if not x['v0u'] or x['v0u']<50]
L=[x for x in ALL if x['v0u'] and x['v0u']>=50]
def A(r,f): return sum(f(x) for x in r)
R=A(L,lambda x:x['v0'])/A(L,lambda x:x['v0u'])
print("LIVE classes 2023-25 (career years 1-3): n=%d, %d dropped for a degenerate raw year-0 value (<50 pts; mature entrants)."%(len(L),len(DEG)))
print("cohort re-anchoring factor R_bar = v0_shipped/v0_raw = %.4f ; cohort markup = %.3f"%(R,A(L,lambda x:x['price'])/A(L,lambda x:x['v0'])))
print()
print(f"{'pos':6s} {'n':>4s} {'R':>6s} {'markup':>7s} {'book v0':>9s} {'book price':>11s}")
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in L if x['pos']==p]
    if not r: continue
    print(f"{p:6s} {len(r):4d} {A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u']):6.3f} {A(r,lambda x:x['price'])/A(r,lambda x:x['v0']):7.3f} {A(r,lambda x:x['v0']):9.0f} {A(r,lambda x:x['price']):11.0f}")
print()
print("=== live year-1-3 ND players priced above 1.8x their own year-0 anchor (n=%d) ==="%len([x for x in L if x['price']/x['v0']>1.8]))
print("re-anchor exposure = price x (1 - R_i/R_bar) = the points that exist only because his year-0 anchor")
print("was re-anchored harder than the cohort average, with nothing re-anchoring his year-1 price.")
print()
print(f"{'name':23s}{'pos':5s}{'C':>5s}{'N':>2s}{'pk':>4s}{'ag':>3s}{'v0':>6s}{'v0raw':>7s}{'R':>6s}{'price':>7s}{'mkup':>6s}{'prod':>6s}{'reanch':>8s}{'%':>5s}{'pole':>6s}")
big=sorted([x for x in L if x['price']/x['v0']>1.8],key=lambda z:-z['price']*(1-z['m']/R))
for x in big:
    lp=x['price']*(1-x['m']/R)
    print(f"{(x['name'] or x['key'])[:22]:23s}{x['pos']:5s}{x['C']:5d}{x['N']:2d}{int(x['pk']):4d}{int(x['age'] or 0):3d}{x['v0']:6.0f}{x['v0u']:7.0f}{x['m']:6.3f}{x['price']:7.0f}{x['price']/x['v0']:6.2f}{x['prod']:6.2f}{lp:8.0f}{100*lp/x['price']:4.0f}%{x['pole']:6.0f}")
print()
print("group totals: price %.0f | re-anchor-exposed %.0f (%.0f%%) | pole-credit-exposed %.0f (%.1f%%)"%(
  A(big,lambda x:x['price']),A(big,lambda x:x['price']*(1-x['m']/R)),
  100*A(big,lambda x:x['price']*(1-x['m']/R))/A(big,lambda x:x['price']),
  A(big,lambda x:x['pole']*x['iso']),100*A(big,lambda x:x['pole']*x['iso'])/A(big,lambda x:x['price'])))
print()
print("=== the named cases ===")
for k in ['connor-o-sullivan','harry-dean','finn-o-sullivan','sullivan-robey']:
    x=[z for z in ALL if z['key']==k]
    if not x: continue
    x=x[0]; lp=x['price']*(1-x['m']/R)
    print(f"  {x['name']:20s} {x['pos']} pk{int(x['pk'])} class {x['C']}  v0_raw {x['v0u']:.0f} -> v0_shipped {x['v0']:.0f} (R={x['m']:.3f})  price {x['price']:.0f}  markup {x['price']/x['v0']:.2f}x  production {x['prod']:.2f}x  re-anchor-exposed {lp:.0f} ({100*lp/x['price']:.0f}%)  pole {x['pole']*x['iso']:.0f}")
