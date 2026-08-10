import json
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
print("=== KILL THE PEDIGREE POLE ENTIRELY (upper bound: subtract the whole year-1 pole credit) ===")
print(f"{'pos':6s} {'n':>4s} {'markup':>7s} {'markup_nopole':>14s} {'delta':>7s}")
for pos in ['MID','SD','SF','KPF','KPD','RUCK','LEG']:
    r=[x for x in d if pos=='LEG' or x['pos']==pos]
    V=A(r,lambda x:x['v0']); P=A(r,lambda x:x['s6_price']); C=A(r,lambda x:x['y1']['pole_credit']*x['y1']['iso'])
    print(f"{pos:6s} {len(r):4d} {P/V:7.3f} {(P-C)/V:14.3f} {(P-C)/V-P/V:7.3f}")
print()
print("=== the 35 established KPDs, year 1 ===")
print(f"{'key':26s}{'pk':>4s}{'age':>4s}{'sa':>6s}{'g':>4s}{'v0u':>7s}{'v0':>7s}{'m':>6s}{'price':>7s}{'F':>7s}{'mkup':>6s}{'F1':>6s}{'pole':>6s}{'band0':>7s}{'band1':>7s}")
for x in sorted([z for z in d if z['pos']=='KPD'],key=lambda z:z['pk']):
    m=x['v0']/x['v0u']
    print(f"{x['key']:26s}{x['pk']:4d}{(x['age'] or 0):4d}{x['sa']:6.1f}{x['gcum']:4.0f}{x['v0u']:7.0f}{x['v0']:7.0f}{m:6.3f}{x['s6_price']:7.0f}{x['s6_F']:7.0f}{x['s6_price']/x['v0']:6.2f}{x['s6_F']/x['s6_price']:6.2f}{x['y1']['pole_credit']:6.0f}{x['y0']['pr']*x['y0']['iso']:7.0f}{x['y1']['pr']*x['y1']['iso']:7.0f}")
