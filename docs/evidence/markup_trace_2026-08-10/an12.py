import json
ALL=[x for x in json.load(open('live.json')) if 2023<=x['C']<=2025]
L=[x for x in ALL if x['v0u'] and x['v0u']>=50]
def A(r,f): return sum(f(x) for x in r)
R=A(L,lambda x:x['v0'])/A(L,lambda x:x['v0u'])
print("whole live young cohort re-anchor exposure, by position (R_bar=%.4f):"%R)
print(f"{'pos':6s} {'n':>4s} {'R':>6s} {'book price':>11s} {'reanch pts':>11s} {'%of book':>9s} {'pole pts':>9s}")
for p in ['MID','SD','SF','KPF','KPD','RUCK','ALL']:
    r=[x for x in L if p=='ALL' or x['pos']==p]
    P=A(r,lambda x:x['price']); E=A(r,lambda x:x['price']*(1-x['m']/R)); PO=A(r,lambda x:x['pole']*x['iso'])
    print(f"{p:6s} {len(r):4d} {A(r,lambda x:x['v0'])/A(r,lambda x:x['v0u']):6.3f} {P:11.0f} {E:11.0f} {100*E/P:8.1f}% {PO:9.0f}")
print()
print("=== every live KPD in career years 1-3 ===")
print(f"{'name':23s}{'C':>5s}{'N':>2s}{'pk':>4s}{'v0':>6s}{'v0raw':>7s}{'R':>6s}{'price':>7s}{'mkup':>6s}{'prod':>6s}{'reanch':>8s}{'%':>5s}")
for x in sorted([z for z in L if z['pos']=='KPD'],key=lambda z:-z['price']):
    lp=x['price']*(1-x['m']/R)
    print(f"{(x['name'])[:22]:23s}{x['C']:5d}{x['N']:2d}{int(x['pk']):4d}{x['v0']:6.0f}{x['v0u']:7.0f}{x['m']:6.3f}{x['price']:7.0f}{x['price']/x['v0']:6.2f}{x['prod']:6.2f}{lp:8.0f}{100*lp/max(x['price'],1):4.0f}%")
