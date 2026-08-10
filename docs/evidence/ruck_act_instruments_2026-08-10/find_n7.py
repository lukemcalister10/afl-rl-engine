import json, itertools
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
IN=json.load(open(SP+"ruck_instr_main.json")); rows=IN['rows']
D=json.load(open("/home/user/afl-rl-engine/data/rl_build/rl_app_data.json"))
ACT={a['key']:a for a in D['active']}
ru=[r for r in rows if r['pos']=='RUCK' and r['key'] in ACT]
def rep(name, sub):
    if not sub: return
    sp=sum(x['price'] for x in sub); sv=sum(x['v0s'] for x in sub); su=sum(x['v0u'] for x in sub)
    print("%-52s n=%2d  p/v0s=%.4f  p/v0u=%.4f  v0s/v0u=%.4f" % (name,len(sub),sp/sv,sp/su,sv/su))
defs={}
defs['C in 2023-25 (all)']=[r for r in ru if r['C'] and 2023<=r['C']<=2025]
defs['C in 2023-25 games>0']=[r for r in ru if r['C'] and 2023<=r['C']<=2025 and r['games_total']>0]
defs['C in 2023-25 ND only']=[r for r in ru if r['C'] and 2023<=r['C']<=2025 and r['epk']<65]
defs['C in 2023-25 ND games>0']=[r for r in ru if r['C'] and 2023<=r['C']<=2025 and r['epk']<65 and r['games_total']>0]
defs['C in 2023-25 nseas>=1']=[r for r in ru if r['C'] and 2023<=r['C']<=2025 and r['nseas']>=1]
defs['C in 2024-26 (all)']=[r for r in ru if r['C'] and 2024<=r['C']<=2026]
defs['C in 2024-26 games>0']=[r for r in ru if r['C'] and 2024<=r['C']<=2026 and r['games_total']>0]
defs['last_year>=2024 & C>=2022']=[r for r in ru if r['C'] and r['C']>=2022 and (r['last_year'] or 0)>=2024]
defs['C in 2023-25 pool only']=[r for r in ru if r['C'] and 2023<=r['C']<=2025 and r['epk']==65]
for k,v in defs.items(): rep(k,v)
print()
print("all live rucks C>=2022 enumerated:")
for r in sorted([x for x in ru if x['C'] and x['C']>=2022], key=lambda z:-z['price']):
    print("  %-24s C=%s epk=%3d g=%3.0f nseas=%d price=%8.1f v0s=%8.1f v0u=%8.1f" % (
        r['key'],r['C'],r['epk'],r['games_total'],r['nseas'],r['price'],r['v0s'],r['v0u']))
