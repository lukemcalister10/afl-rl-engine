import json
SP="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
s6=json.load(open(SP+"s6_rows.json"))
IN=json.load(open(SP+"ruck_instr_branch.json"))
rows=IN['rows']
s6r={(r['key'],r['C'],r['Y']):r for r in s6 if r['pos']=='RUCK'}
print("s6 RUCK rows=%d  instr rows=%d" % (len(s6r),len(rows)))
miss=0; maxde=0.0; maxdv=0.0; nexact_e=0; nexact_v=0
for r in rows:
    k=(r['key'],r['C'],r['Y'])
    q=s6r.get(k)
    if q is None: miss+=1; continue
    de=abs(q['e']-r['e']); dv=abs(q['v0']-r['v0s'])
    maxde=max(maxde,de); maxdv=max(maxdv,dv)
    if de==0.0: nexact_e+=1
    if dv==0.0: nexact_v+=1
print("unmatched=%d  max|de|=%.10g  max|dv0|=%.10g  e byte-exact %d/%d  v0 byte-exact %d/%d"
      % (miss,maxde,maxdv,nexact_e,len(rows),nexact_v,len(rows)))
# price reproduction vs the frozen matrix price carried in s6_rows
maxdp=0.0; nexact_p=0
for r in rows:
    q=s6r.get((r['key'],r['C'],r['Y']))
    if q is None: continue
    dp=abs(q['price']-r['price'])
    maxdp=max(maxdp,dp)
    if dp==0.0: nexact_p+=1
print("price (re-run ev vs FROZEN stage4a1 matrix price): max|dp|=%.6g  exact %d/%d" % (maxdp,nexact_p,len(rows)))
