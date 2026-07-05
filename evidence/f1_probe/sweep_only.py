import io,contextlib,json,statistics
REPO="/home/user/afl-rl-engine"
SHIP=json.load(open(REPO+"/data/rl_build/rl_app_data.json"))
SHIP_ACT={r['key']:r for r in SHIP['active']}
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; players=MA.players
gated={}
with contextlib.redirect_stdout(io.StringIO()):
    for p in players: gated[p['key']]=ev(p,2026)
common=[k for k in gated if k in SHIP_ACT]
pct=[]; diffs=[]
for k in common:
    gv=gated[k]; sv=SHIP_ACT[k]['v']
    if gv is None or sv is None: continue
    if gv!=sv:
        diffs.append((k,gv,sv,sv-gv,(sv-gv)/gv*100 if gv else 0)); pct.append((sv-gv)/gv*100 if gv else 0)
res={'matched':len(common),'shipped_active':len(SHIP_ACT),'engine_players':len(players),
     'differing':len(diffs),'differing_pct':round(100*len(diffs)/len(common),1),
     'median_divergence_pct':round(statistics.median(pct),1),
     'shipped_higher':sum(1 for x in pct if x>0),'shipped_lower':sum(1 for x in pct if x<0),
     'review_claim':{'differing':537,'total':805,'pct':66.7,'median':12.5}}
diffs.sort(key=lambda r:-abs(r[3]))
res['top12']=[{'key':k,'gated':gv,'shipped':sv,'delta':dl,'pct':round(pc,1)} for k,gv,sv,dl,pc in diffs[:12]]
json.dump(res,open(REPO+"/evidence/f1_probe/sweep_result.json","w"),indent=2)
print(json.dumps(res,indent=2))
