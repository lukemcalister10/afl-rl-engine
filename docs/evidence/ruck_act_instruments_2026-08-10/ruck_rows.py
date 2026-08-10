import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
rows=json.load(open(SP+"s6_rows.json"))
ru=[r for r in rows if r['pos']=='RUCK']
print("ALL RUCK established-leg rows in s6_rows.json: n=%d" % len(ru))
print("%-24s %4s %4s %2s %4s %6s %6s %6s %9s %9s %9s %9s %8s %6s" % (
  "key","C","Y","N","pk","gcum","sa","age","e","price","v0","A","F","nd"))
for r in sorted(ru,key=lambda x:(x['key'],x['Y'])):
    print("%-24s %4d %4d %2d %4d %6.1f %6.1f %6s %9.1f %9.1f %9.1f %9.1f %8.1f %6s pool=%s" % (
      r['key'],r['C'],r['Y'],r['N'],r['pk'],r['gcum'],r['sa'],r['age'],r['e'],r['price'],r['v0'],r['A'],r['F'],r['nd'],r['is_pool']))
