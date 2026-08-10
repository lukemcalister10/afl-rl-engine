import json
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
mbar=A(d,lambda x:x['v0'])/A(d,lambda x:x['v0u'])          # leg-average year-0 lens factor
pbar=A(d,lambda x:x['s6_price'])/A(d,lambda x:x['v0u'])    # leg-average production re-pricing
print("leg lens factor m_bar = %.4f ; leg production re-pricing prod_bar = %.4f ; leg markup %.4f"%(mbar,pbar,pbar/mbar))
print()
print("PER-PLAYER counterfactuals, summed. E = sum(price - F).")
print(f"{'cell':14s} {'n':>4s} {'E_now':>9s} | {'E_lens=leg':>11s} {'closed':>8s} | {'E_prod=leg':>11s} {'closed':>8s}")
def line(lbl,r):
    if not r: return
    E=A(r,lambda x:x['s6_price']-x['s6_F'])
    EL=A(r,lambda x:x['s6_price']*(x['v0']/x['v0u'])/mbar-x['s6_F'])
    EP=A(r,lambda x:x['v0u']*pbar-x['s6_F'])
    print(f"{lbl:14s} {len(r):4d} {E:9.0f} | {EL:11.0f} {(E-EL):8.0f} | {EP:11.0f} {(E-EP):8.0f}")
line('LEG',d)
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']: line(p,[x for x in d if x['pos']==p])
print()
for p in ['MID','SD','SF','KPF','KPD','RUCK']:
    for lbl,f in [(' y<=18',lambda x:x['age'] is not None and x['age']<=18),(' m19+',lambda x:x['age'] is not None and x['age']>=19),(' unk',lambda x:x['age'] is None)]:
        line(p+lbl,[x for x in d if x['pos']==p and f(x)])
print()
print("=== biggest single excesses on the leg (price - F), with their two factors ===")
print(f"{'key':26s}{'pos':6s}{'pk':>4s}{'sa':>6s}{'g':>4s}{'v0':>7s}{'price':>7s}{'F':>7s}{'excess':>8s}{'m':>6s}{'m/mbar':>7s}{'prod':>7s}{'p/pbar':>7s}")
for x in sorted(d,key=lambda z:-(z['s6_price']-z['s6_F']))[:18]:
    m=x['v0']/x['v0u']; pr=x['s6_price']/x['v0u']
    print(f"{x['key']:26s}{x['pos']:6s}{x['pk']:4d}{x['sa']:6.1f}{x['gcum']:4.0f}{x['v0']:7.0f}{x['s6_price']:7.0f}{x['s6_F']:7.0f}{x['s6_price']-x['s6_F']:8.0f}{m:6.2f}{m/mbar:7.2f}{pr:7.2f}{pr/pbar:7.2f}")
