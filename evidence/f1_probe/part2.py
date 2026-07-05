import io,contextlib,json
REPO="/home/user/afl-rl-engine"
SHIP=json.load(open(REPO+"/data/rl_build/rl_app_data.json"))
SHIP_ACT={r['key']:r for r in SHIP['active']}
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; players=MA.players; delisted=g.get('delisted')

print("=== PETRACCA POSITION ===")
petr=[p for p in players if 'petracca' in p['player'].lower() and p.get('year')==2014][0]
print("current de-DPP p['pos']   =",petr.get('pos'))
print("gfut (forward group)      =",MA.gfut(petr))
print("bnow (board-now group)    =",MA.bnow(petr))
print("frozen draft group _grp   =",petr.get('_grp'))
print("futblend                  =",[[gg,round(w,3)] for gg,w in MA.futblend(petr)])
print("shipped gf/grp/fut        =",SHIP_ACT['christian-petracca']['gf'],"/",SHIP_ACT['christian-petracca']['grp'],"/",SHIP_ACT['christian-petracca']['fut'])

print("\n=== POPULATION / RETIREMENT ===")
print("engine active players:",len(players),"  shipped active rows:",len(SHIP['active']))
n_ret=sum(1 for p in players if p.get('_retired'))
n_del=sum(1 for p in players if delisted and delisted(p))
print("engine _retired flag:",n_ret,"  engine delisted() True:",n_del)
key2p={p['key']:p for p in players}
# shipped rows delisted in engine but nonzero shipped value
nz=[(r['key'],r['v']) for r in SHIP['active'] if key2p.get(r['key']) and delisted and delisted(key2p[r['key']]) and (r.get('v') or 0)>50]
print("shipped active delisted-but-v>50:",len(nz))
for k,v in nz[:20]: print("   ",k,"v=",v," gated ev=", None)
# injured named players by key (Conway, King)
for nm in ['conway','king']:
    for p in players:
        if nm in p['player'].lower():
            print("  injured-check:",p['key'],p['player'],"yr",p.get('year'),"pk",p.get('pick'),"retired?",p.get('_retired'),"delisted?",delisted(p) if delisted else "n/a","shipped_v?",SHIP_ACT.get(p['key'],{}).get('v'))

print("\n=== PICK-60 DRAFTVAL ===")
PVC=MA.PVC; cp=g['cp']
print("PVC[60]=",PVC.get(60)," KMAX=",cp.KMAX," draftval mech=PVC[min(effpk,KMAX)]")
print("gated pick-60 draftval:",PVC.get(min(60,cp.KMAX)))
print("shipped PVC['60']=",SHIP['PVC'].get('60'),"  shipped picks table len=",len(SHIP['picks']),"(stops at pick",SHIP['picks'][-1]['n'],")")
# does shipped book use pick 60 anywhere? picks table only 1..30
print("shipped picks n range:",SHIP['picks'][0]['n'],"..",SHIP['picks'][-1]['n'])
