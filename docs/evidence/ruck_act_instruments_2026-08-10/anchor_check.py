import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
rows=json.load(open(SP+"s6_rows.json"))

leg=[r for r in rows if r['nd'] and 1<=r['pk']<=64 and 2004<=r['C']<=2022 and r['N']==1]
print("leg n:", len(leg))
sp=sum(r['price'] for r in leg); sv=sum(r['v0'] for r in leg); sF=sum(r['F'] for r in leg)
print("leg  markup Sprice/Sv0 = %.4f" % (sp/sv))
print("leg  F1 SF/Sprice      = %.4f" % (sF/sp))
ru=[r for r in leg if r['pos']=='RUCK']
print("ruck n:", len(ru))
sp2=sum(r['price'] for r in ru); sv2=sum(r['v0'] for r in ru); sF2=sum(r['F'] for r in ru)
print("ruck markup = %.4f" % (sp2/sv2))
print("ruck F1     = %.4f" % (sF2/sp2))
print()
# per-position table
from collections import defaultdict
d=defaultdict(list)
for r in leg: d[r['pos']].append(r)
for pos,rs in sorted(d.items(), key=lambda kv:-len(kv[1])):
    a=sum(x['price'] for x in rs); b=sum(x['v0'] for x in rs); c=sum(x['F'] for x in rs)
    print("%-6s n=%3d markup=%.3f F1=%.3f" % (pos,len(rs),a/b,c/a))
print()
for r in sorted(ru, key=lambda x:-x['price']):
    print("%-24s C=%d pk=%3d g=%5.1f sa=%5.1f age=%s v0=%8.1f price=%8.1f F=%9.1f" % (
        r['key'], r['C'], r['pk'], r['gcum'], r['sa'], r['age'], r['v0'], r['price'], r['F']))
