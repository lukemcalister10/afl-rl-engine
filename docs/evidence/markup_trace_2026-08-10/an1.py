import json,statistics as st
d=json.load(open('decomp_b.json'))
def S(rows,f): return sum(f(x) for x in rows)
hdr=f"{'pos':6s} {'n':>4s} | {'pr0':>7s} {'C0':>7s} {'poleSh0':>7s} | {'pr1':>7s} {'C1':>7s} {'poleSh1':>7s} | {'pr1/pr0':>7s} {'C1/C0':>6s} {'iso0':>5s} {'iso1':>5s} {'v0u/v0':>6s} {'mkup':>6s}"
print(hdr)
for pos in ['MID','SD','SF','KPF','KPD','RUCK','ALL']:
    r=[x for x in d if pos=='ALL' or x['pos']==pos]
    n=len(r)
    pr0=S(r,lambda x:x['y0']['pr']); C0=S(r,lambda x:x['y0']['pole_credit'])
    pr1=S(r,lambda x:x['y1']['pr']); C1=S(r,lambda x:x['y1']['pole_credit'])
    iso0=S(r,lambda x:x['y0']['iso']*x['y0']['raw'])/S(r,lambda x:x['y0']['raw'])
    iso1=S(r,lambda x:x['y1']['iso']*x['y1']['raw'])/S(r,lambda x:x['y1']['raw'])
    v0u=S(r,lambda x:x['v0u']); v0=S(r,lambda x:x['v0'])
    mk=S(r,lambda x:x['s6_price'])/v0
    print(f"{pos:6s} {n:4d} | {pr0/n:7.0f} {C0/n:7.0f} {C0/(pr0+C0):7.3f} | {pr1/n:7.0f} {C1/n:7.0f} {C1/(pr1+C1):7.3f} | {pr1/pr0:7.3f} {C1/max(C0,1e-9):6.3f} {iso0:5.3f} {iso1:5.3f} {v0u/v0:6.3f} {mk:6.3f}")
print()
print("mean component values (unweighted) — the pole machinery")
h2=f"{'pos':6s} {'n':>4s} | {'wage':>5s} {'tf0':>5s} {'eg0':>5s} {'w0':>5s} {'rec0':>5s} | {'tf1':>5s} {'eg1':>5s} {'w1':>5s} {'rec1':>5s} | {'perf1':>6s} {'par1':>6s} {'p/par':>6s} | {'po0/pr0':>7s} {'po1/pr1':>7s}"
print(h2)
for pos in ['MID','SD','SF','KPF','KPD','RUCK']:
    r=[x for x in d if x['pos']==pos]; n=len(r)
    m=lambda f: st.mean(f(x) for x in r)
    print(f"{pos:6s} {n:4d} | {m(lambda x:x['y0']['wage']):5.3f} {m(lambda x:x['y0']['tfade']):5.3f} {m(lambda x:x['y0']['expgate']):5.3f} {m(lambda x:x['y0']['w']):5.3f} {m(lambda x:x['y0']['rec']):5.3f} | {m(lambda x:x['y1']['tfade']):5.3f} {m(lambda x:x['y1']['expgate']):5.3f} {m(lambda x:x['y1']['w']):5.3f} {m(lambda x:x['y1']['rec']):5.3f} | {m(lambda x:x['y1']['perf']):6.1f} {m(lambda x:x['y1']['par']):6.1f} {m(lambda x:x['y1']['perf']/x['y1']['par']):6.3f} | {m(lambda x:x['y0']['po']/x['y0']['pr']):7.3f} {m(lambda x:x['y1']['po']/x['y1']['pr']):7.3f}")
