import json
L=[x for x in json.load(open('live.json')) if x['v0u'] and x['v0u']>0 and 2023<=x['C']<=2025]
def A(r,f): return sum(f(x) for x in r)
mbar=A(L,lambda x:x['v0'])/A(L,lambda x:x['v0u'])
print("LIVE young ND cohort (classes 2023-2025, career years 1-3), n=%d.  cohort mean lens factor m_bar=%.4f"%(len(L),mbar))
print("cohort book: v0 %.0f  price %.0f  markup %.3f"%(A(L,lambda x:x['v0']),A(L,lambda x:x['price']),A(L,lambda x:x['price'])/A(L,lambda x:x['v0'])))
print()
print(f"{'pos':6s} {'n':>4s} {'m':>6s} {'markup':>7s} {'lens-exposed pts':>17s}")
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in L if x['pos']==p]
    if not r: continue
    m=A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u'])
    print(f"{p:6s} {len(r):4d} {m:6.3f} {A(r,lambda x:x['price'])/A(r,lambda x:x['v0']):7.3f} {A(r,lambda x:x['price']*(1-x['m']/mbar)):17.0f}")
print()
print("=== EVERY live year-1-3 ND player priced above 1.8x his own year-0 anchor ===")
print(f"{'name':24s}{'pos':5s}{'C':>5s}{'N':>2s}{'pk':>4s}{'ag':>3s}{'v0':>6s}{'v0u':>6s}{'m':>6s}{'price':>7s}{'mkup':>6s}{'prod':>6s}{'lens_pts':>9s}{'lens%':>6s}{'pole':>6s}")
big=[x for x in L if x['price']/x['v0']>1.8]
for x in sorted(big,key=lambda z:-(z['price']*(1-z['m']/mbar))):
    lp=x['price']*(1-x['m']/mbar)
    print(f"{(x['name'] or x['key'])[:23]:24s}{x['pos']:5s}{x['C']:5d}{x['N']:2d}{x['pk']:4d}{(x['age'] or 0):3d}{x['v0']:6.0f}{x['v0u']:6.0f}{x['m']:6.3f}{x['price']:7.0f}{x['price']/x['v0']:6.2f}{x['prod']:6.2f}{lp:9.0f}{100*lp/x['price']:5.0f}%{x['pole']:6.0f}")
print()
print("total live prices in that group = %.0f ; lens-exposed points = %.0f (%.0f%%)"%(
    A(big,lambda x:x['price']), A(big,lambda x:x['price']*(1-x['m']/mbar)),
    100*A(big,lambda x:x['price']*(1-x['m']/mbar))/A(big,lambda x:x['price'])))
