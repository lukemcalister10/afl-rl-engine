import json
from collections import defaultdict
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
IN=json.load(open(SP+"ruck_instr_main.json")); rows=IN['rows']; F=IN['meta']['pl_factor']
D=json.load(open("/home/user/afl-rl-engine/data/rl_build/rl_app_data.json"))
ACT={a['key']:a for a in D['active']}
print("engine=%s store=%s v0surf=%s factor=%s" % (IN['meta']['engine_md5'][:8],IN['meta']['store_md5'][:8],IN['meta']['v0surf_sig'][:8],F))
print("RUCCEIL grid: lo=%.1f hi=%.1f refpk=%s head=%s" % (IN['meta']['ruccei_meta']['grid_lo'],IN['meta']['ruccei_meta']['grid_hi'],IN['meta']['ruccei_meta']['refpk'],IN['meta']['ruccei_meta']['head']))
ru=[r for r in rows if r['pos']=='RUCK']
live=[r for r in ru if r['key'] in ACT]
print("\nRUCK records priced=%d ; ON THE LIVE BOARD (active list)=%d" % (len(ru),len(live)))

print("\n=== D1f  LIVE-BOARD RUCK ROSTER — ceiling state at Y=2026 (engine currency; board = engine/1.0524) ===")
print("%-26s %4s %4s %4s %5s %6s %8s %9s %9s %9s %9s %8s %8s %5s %s" % (
  "key","C","N","epk","ageY","games","bestlvl","e","ceiling","v0u","v0s","price","price_nc","bind","board_v"))
tb=0.0
for r in sorted(live,key=lambda x:-x['price']):
    N=(2026-(r['C'] or 0))
    b=r['price_nc']-r['price']; tb+=b
    print("%-26s %4s %4s %4d %5s %6.0f %8.2f %9.1f %9.1f %9.1f %9.1f %8.1f %8.1f %5s %6s" % (
      r['key'],r['C'],N,r['epk'],("%.0f"%r['age_asof']) if r['age_asof'] is not None else "?",
      r['games_total'],r['bestlvl'],r['e'],r['cpv'],r['v0u'],r['v0s'],r['price'],r['price_nc'],r['bind'],
      ACT[r['key']].get('v')))
print("TOTAL live-board ceiling bite (engine currency) = %.1f  (board currency %.1f)" % (tb,tb/F))

print("\n=== D1g  LIVE BOARD, CAREER YEARS 1-3 (classes 2023-2025) ===")
c3=[r for r in live if r['C'] and 2023<=r['C']<=2025]
sp=sum(r['price'] for r in c3); sv=sum(r['v0s'] for r in c3); svu=sum(r['v0u'] for r in c3)
print("n=%d  Sprice=%.1f  Sv0_start=%.1f  R=Sprice/Sv0=%.4f   Sv0_uncapped=%.1f  prod=Sprice/Sv0u=%.4f  surface lift Sv0/Sv0u=%.4f"
      % (len(c3),sp,sv,sp/sv,svu,sp/svu,sv/svu))
for r in sorted(c3,key=lambda x:-x['price']):
    print("   %-26s C=%s epk=%3d g=%3.0f price=%8.1f v0s=%8.1f v0u=%8.1f R=%.3f bind=%s board=%s" % (
      r['key'],r['C'],r['epk'],r['games_total'],r['price'],r['v0s'],r['v0u'],r['price']/r['v0s'],r['bind'],ACT[r['key']].get('v')))

print("\n=== D1h  ALL LIVE positions: cohort re-anchoring R=Sprice/Sv0 for classes 2023-2025 ===")
d=defaultdict(lambda:[0,0.0,0.0,0.0])
for r in rows:
    if r['key'] not in ACT: continue
    if not (r['C'] and 2023<=r['C']<=2025): continue
    a=d[r['pos']]; a[0]+=1; a[1]+=r['price']; a[2]+=r['v0s']; a[3]+=r['v0u']
tot=[0,0.0,0.0,0.0]
for pos,(n,p,v,vu) in sorted(d.items()):
    tot[0]+=n; tot[1]+=p; tot[2]+=v; tot[3]+=vu
    print("  %-5s n=%3d  R=%.4f  prod=%.4f  surface_lift=%.4f" % (pos,n,p/v,p/vu,v/vu))
print("  %-5s n=%3d  R=%.4f  prod=%.4f  surface_lift=%.4f" % ("ALL",tot[0],tot[1]/tot[2],tot[1]/tot[3],tot[2]/tot[3]))
