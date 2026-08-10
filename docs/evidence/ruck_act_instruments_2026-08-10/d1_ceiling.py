import json
from collections import defaultdict
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
IN=json.load(open(SP+"ruck_instr_branch.json")); rows=IN['rows']
s6=json.load(open(SP+"s6_rows.json"))
nd={(r['key'],r['C'],r['Y']):(r['nd'],r['pk'],r['is_pool']) for r in s6}
for r in rows:
    t=nd.get((r['key'],r['C'],r['Y']))
    r['nd_flag']=bool(t[0]) if t else None
    r['pool_flag']=bool(t[2]) if t else None

print("=== D1a  CEILING BINDING — TEACHING LEG, ALL EVALUATION YEARS (branch basis) ===")
print("population: every RUCK established-leg row measure_g6 kept (classes 2004-2022), n=%d" % len(rows))
tot=defaultdict(lambda:[0,0,0.0,0.0])
for r in rows:
    seg='ND 1-64' if (r['nd_flag'] and 1<=r['pk']<=64) else 'pool/other'
    bite=r['price_nc']-r['price']
    tot[seg][0]+=1
    if r['bind']: tot[seg][1]+=1; tot[seg][2]+=bite
    tot[seg][3]+=r['price']
print("%-12s %6s %8s %14s %14s" % ("segment","n","n_bind","bite_pts","Sprice"))
for k,(n,nb,b,sp) in sorted(tot.items()):
    print("%-12s %6d %8d %14.1f %14.1f" % (k,n,nb,b,sp))

print()
print("=== D1b  EVERY BINDING ROW, ND 1-64 leg (classes 2004-2022) ===")
bd=[r for r in rows if r['bind'] and r['nd_flag'] and 1<=r['pk']<=64]
print("%-22s %4s %4s %2s %4s %6s %6s %5s %6s %9s %9s %9s %9s %9s %8s %s" % (
  "key","C","Y","N","pk","gcum","sa","agD","agY","e","ceiling","v0u","price","price_nc","bite","fallback"))
bysum=defaultdict(float); bycnt=defaultdict(int)
for r in sorted(bd,key=lambda x:(x['key'],x['Y'])):
    bite=r['price_nc']-r['price']
    bysum[r['key']]+=bite; bycnt[r['key']]+=1
    print("%-22s %4d %4d %2d %4d %6.1f %6.1f %5s %6s %9.1f %9.1f %9.1f %9.1f %9.1f %8.1f %s" % (
      r['key'],r['C'],r['Y'],r['N'],r['pk'],r['gcum'],r['sa'],r['age'],
      ("%.1f"%r['age_asof']) if r['age_asof'] is not None else "None",
      r['e'],r['cpv'],r['v0u'],r['price'],r['price_nc'],bite,
      "PRIOR-CAP" if r['no_production'] else "prod-ceil"))
print("\nper-player total bite (ND 1-64, all evaluation years):")
for k in sorted(bysum,key=lambda z:-bysum[z]):
    print("  %-24s rows=%d  bite=%.1f" % (k,bycnt[k],bysum[k]))
print("  TOTAL bite = %.1f over %d rows / %d players" % (sum(bysum.values()),len(bd),len(bysum)))

print()
print("=== D1c  EVERY BINDING ROW, POOL/OTHER rucks (classes 2004-2022) ===")
bp=[r for r in rows if r['bind'] and not (r['nd_flag'] and 1<=r['pk']<=64)]
bysum2=defaultdict(float); bycnt2=defaultdict(int)
for r in bp: bysum2[r['key']]+=r['price_nc']-r['price']; bycnt2[r['key']]+=1
for k in sorted(bysum2,key=lambda z:-bysum2[z]):
    print("  %-24s rows=%d  bite=%.1f" % (k,bycnt2[k],bysum2[k]))
print("  TOTAL pool/other bite = %.1f over %d rows / %d players" % (sum(bysum2.values()),len(bp),len(bysum2)))

print()
print("=== D1d  BINDING BY EVALUATION YEAR N (ND 1-64) ===")
byN=defaultdict(lambda:[0,0,0.0,0.0,0.0])
for r in rows:
    if not (r['nd_flag'] and 1<=r['pk']<=64): continue
    a=byN[r['N']]; a[0]+=1; a[3]+=r['price']; a[4]+=r['price_nc']
    if r['bind']: a[1]+=1; a[2]+=r['price_nc']-r['price']
print("%3s %6s %7s %12s %12s %12s %8s" % ("N","n","n_bind","bite","Sprice","Sprice_nc","bite%"))
for N in sorted(byN):
    n,nb,b,sp,spn=byN[N]
    print("%3d %6d %7d %12.1f %12.1f %12.1f %7.2f%%" % (N,n,nb,b,sp,spn,100.0*b/sp if sp else 0))

print()
print("=== D1e  THE 11 (N=1, ND 1-64) — full ceiling arithmetic ===")
e11=[r for r in rows if r['N']==1 and r['nd_flag'] and 1<=r['pk']<=64]
print("n=%d" % len(e11))
hdr=("key","C","pk","gcum","sa","agD","bestlvl","e","ceiling","v0u","v0s","price","price_nc","bite","bind")
print("%-22s %4s %4s %5s %6s %4s %8s %9s %9s %9s %9s %8s %9s %8s %5s" % hdr)
for r in sorted(e11,key=lambda x:-x['price']):
    print("%-22s %4d %4d %5.1f %6.1f %4s %8.2f %9.1f %9.1f %9.1f %9.1f %8.1f %9.1f %8.1f %5s" % (
      r['key'],r['C'],r['pk'],r['gcum'],r['sa'],r['age'],r['bestlvl'],r['e'],r['cpv'],r['v0u'],r['v0s'],
      r['price'],r['price_nc'],r['price_nc']-r['price'],r['bind']))
sp=sum(r['price'] for r in e11); spn=sum(r['price_nc'] for r in e11)
print("Sprice=%.1f  Sprice_nocap=%.1f  bite=%.1f (%.2f%% of the no-cap book)" % (sp,spn,spn-sp,100*(spn-sp)/spn))
json.dump(rows,open(SP+"ruck_rows_enriched.json","w"))
