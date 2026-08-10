import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
rows=json.load(open(SP+"s6_rows.json"))
leg=[r for r in rows if r['nd'] and 1<=r['pk']<=64 and 2004<=r['C']<=2022 and r['N']==1]
ru=[r for r in leg if r['pos']=='RUCK']
print("THE 11 (ND 1-64, classes 2004-2022, N=1, RUCK)")
print("%-22s %4s %4s %5s %5s %5s %4s %9s %9s %8s %9s %9s" % ("key","C","pk","gcum","sa","age","el","e","price","e-price","v0","F"))
tot_e=tot_p=0.0
for r in sorted(ru,key=lambda x:-x['price']):
    print("%-22s %4d %4d %5.1f %5.1f %5s %4.1f %9.1f %9.1f %8.1f %9.1f %9.1f" % (
      r['key'],r['C'],r['pk'],r['gcum'],r['sa'],r['age'],r['el'],r['e'],r['price'],r['e']-r['price'],r['v0'],r['F']))
    tot_e+=r['e']; tot_p+=r['price']
print("TOTAL e=%.1f price=%.1f  gap=%.1f" % (tot_e,tot_p,tot_e-tot_p))
print()
# same for every position on the leg: how often does price < e (something binds)?
from collections import defaultdict
d=defaultdict(lambda:[0,0,0.0])
for r in leg:
    d[r['pos']][0]+=1
    if r['price'] < r['e']-0.75: d[r['pos']][1]+=1; d[r['pos']][2]+=r['e']-r['price']
print("%-6s %5s %8s %12s" % ("pos","n","n_cut","pts_cut"))
for pos,(n,nc,pc) in sorted(d.items()):
    print("%-6s %5d %8d %12.1f" % (pos,n,nc,pc))
