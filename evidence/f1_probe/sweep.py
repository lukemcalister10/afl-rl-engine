#!/usr/bin/env python3
# Full gated-vs-shipped sweep + Petracca position + population/retirement + pick-60. READ-ONLY.
import io,contextlib,json,statistics
REPO="/home/user/afl-rl-engine"
SHIP=json.load(open(REPO+"/data/rl_build/rl_app_data.json"))
SHIP_ACT={r['key']:r for r in SHIP['active']}
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; REAL=g['_REAL']
players=MA.players   # the 805 active list, module instance (ids in _REAL)

# ---- GATED sweep: ev on module players (id in _REAL -> all layers on) ----
gated={}
with contextlib.redirect_stdout(io.StringIO()):
    for p in players:
        gated[p['key']]=ev(p,2026)

# match keys
common=[k for k in gated if k in SHIP_ACT]
diffs=[]; pct=[]
for k in common:
    gv=gated[k]; sv=SHIP_ACT[k]['v']
    if gv is None or sv is None: continue
    if gv!=sv:
        diffs.append((k,gv,sv,sv-gv, (sv-gv)/gv*100 if gv else 0))
        pct.append((sv-gv)/gv*100 if gv else 0)
print("=== FULL GATED-vs-SHIPPED SWEEP (active board, ev year 2026) ===")
print("matched keys:",len(common),"/ shipped active:",len(SHIP_ACT),"/ engine players:",len(players))
print("DIFFERING values:",len(diffs),"of",len(common),"= %.1f%%"%(100*len(diffs)/len(common)))
if pct:
    posd=[x for x in pct if x>0]
    print("median divergence (shipped vs gated) over differing: %.1f%%"%statistics.median(pct))
    print("median divergence (shipped OVER gated, differing): +%.1f%%"%statistics.median([x for x in pct]))
    print("shipped HIGHER than gated:",sum(1 for x in pct if x>0),"  shipped LOWER:",sum(1 for x in pct if x<0))
    print("mean abs divergence: %.1f%%"%statistics.mean([abs(x) for x in pct]))
# top over-values
diffs.sort(key=lambda r:-abs(r[3]))
print("\nTop 12 by absolute divergence (key, gated, shipped, delta, pct):")
for k,gv,sv,dl,pc in diffs[:12]:
    print("  %-26s gated=%6s shipped=%6s  %+6d  %+6.1f%%"%(k,gv,sv,dl,pc))

# ---- Petracca position deep ----
print("\n=== PETRACCA POSITION (frozen draft-group vs current) ===")
petr=[p for p in players if 'petracca' in p['player'].lower() and p.get('year')==2014][0]
print("raw p['pos'] (current de-DPP position) =",petr.get('pos'))
print("gfut(p) (forward-looking group)        =",MA.gfut(petr))
print("bnow(p) (board-now group)              =",g['bnow'](petr))
print("gf field source=gfut, grp field source=bnow(p)")
print("frozen draft group p.get('_grp')       =",petr.get('_grp'))
print("shipped: gf=%s grp=%s fut=%s"%(SHIP_ACT['christian-petracca']['gf'],SHIP_ACT['christian-petracca']['grp'],SHIP_ACT['christian-petracca']['fut']))

# ---- Population / retirement ----
print("\n=== POPULATION / RETIREMENT ===")
retired_ship=[r for r in SHIP['active'] if r.get('v') and (r.get('bk') or False)]
# retirement flags on engine
delisted=g.get('delisted')
n_retired_flag=sum(1 for p in players if p.get('_retired'))
n_delisted=sum(1 for p in players if delisted and delisted(p)) if delisted else None
print("engine active players:",len(players))
print("shipped active rows:",len(SHIP['active']))
print("engine players with _retired flag:",n_retired_flag)
print("engine players delisted() True:",n_delisted)
# shipped rows with nonzero v that are delisted/retired in engine
key2p={p['key']:p for p in players}
ship_retired_nonzero=[]
for r in SHIP['active']:
    p=key2p.get(r['key'])
    if p is not None and delisted and delisted(p) and r.get('v') and r['v']>50:
        ship_retired_nonzero.append((r['key'],r['v']))
print("shipped active rows that are delisted() in engine but carry v>50:",len(ship_retired_nonzero))
for k,v in ship_retired_nonzero[:15]: print("   ",k,"v=",v)

# ---- Pick-60 draftval ----
print("\n=== PICK-60 DRAFTVAL ===")
PVC=MA.PVC
print("PVC has key 60?",60 in PVC," PVC[60]=",PVC.get(60))
print("max PVC pick key:",max(PVC))
shipped_picks=SHIP.get('picks')
print("shipped picks table length:",len(shipped_picks),"-> last entry:",shipped_picks[-1])
print("shipped PVC dict has '60'?", '60' in SHIP['PVC']," value:",SHIP['PVC'].get('60'))
# how engine derives draftval at pick 60
import numpy as np
cp=g['cp']
print("engine draftval mechanism: PVC[min(effpk,KMAX)]; KMAX=",cp.KMAX)
print("PVC[60] (gated pick-60 draft value)=",PVC.get(min(60,cp.KMAX)))

json.dump({'differing':len(diffs),'common':len(common),'median_pct':statistics.median(pct) if pct else None,
           'shipped_active':len(SHIP['active']),'engine_players':len(players),
           'ship_retired_nonzero':len(ship_retired_nonzero)},
          open(REPO+"/evidence/f1_probe/sweep_result.json","w"),indent=2)
print("\nwrote sweep_result.json")
