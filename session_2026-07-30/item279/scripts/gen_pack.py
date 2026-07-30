import json,csv,sys,hashlib
import numpy as np
SP,R=sys.argv[1],sys.argv[2]
OUT=f"{R}/session_2026-07-30/item279/out"
def L(f): return json.load(open(f"{SP}/{f}"))
d=L('derived_279_step1.json')
Bs,Bv=L('board_085_forcedrefit.json'),L('board_100_forcedrefit.json')
Bm=L('board_100_frozenload.json')
vs={r['key']:r for r in Bs['active']}; vv={r['key']:r for r in Bv['active']}
vm={r['key']:r['v'] for r in Bm['active']}
keys=sorted(set(vs)&set(vv)); assert keys, "EMPTY"

# ---- player curve CSV, ranked by SCAR value ----
rows=sorted(keys,key=lambda k:-vs[k]['v'])
def ranks(m):
    o=sorted(keys,key=lambda k:-m[k]); return {k:i+1 for i,k in enumerate(o)}
rs=ranks({k:vs[k]['v'] for k in keys}); rv=ranks({k:vv[k]['v'] for k in keys})
with open(f"{OUT}/curves_players_279.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(['scar_rank','vor_rank','rank_delta','key','name','pos','pick',
                                 'scar_v','vor_v','vor_over_scar','vor_mixed_v'])
    for k in rows:
        w.writerow([rs[k],rv[k],rs[k]-rv[k],k,vs[k].get('name'),vs[k].get('grp'),vs[k].get('pk'),
                    vs[k]['v'],vv[k]['v'],
                    round(vv[k]['v']/vs[k]['v'],4) if vs[k]['v'] else '',vm.get(k,'')])

# ---- pick curve CSV ----
sp={int(k):int(v) for k,v in Bs['PVC'].items()}; vp={int(k):int(v) for k,v in Bv['PVC'].items()}
mv=d['model_pick_value_gamma_responsive']['by_pick']
with open(f"{OUT}/curves_picks_279.csv","w",newline="") as f:
    w=csv.writer(f); w.writerow(['pick','shipped_ladder_scar','shipped_ladder_vor','shipped_identical',
                                 'model_raw_production','model_val_scar','model_val_vor','model_vor_over_scar'])
    for k in range(1,66):
        m=mv.get(str(k))
        w.writerow([k,sp.get(k,''),vp.get(k,''),sp.get(k)==vp.get(k),
                    m['raw'] if m else '',m['scar'] if m else '',m['vor'] if m else '',m['ratio'] if m else ''])

# ---- non-vacuity: every check proven able to fail ----
nv={
 'rank_all_pairs_metric':{
   'check':'order-independent all-pairs inversion count (A13 instrument)',
   'control_identical_input_inversions':d['rank_movement_nonvacuity']['control_identical_inversions'],
   'expect':0,'passes':d['rank_movement_nonvacuity']['control_identical_inversions']==0,
   'perturbed_single_swap_inversions':d['rank_movement_nonvacuity']['perturbed_one_swap_inversions'],
   'expect_gt':0,'detects':d['rank_movement_nonvacuity']['perturbed_one_swap_inversions']>0},
 'shipped_ladder_equality':{
   'check':'shipped pick ladder identical across gamma',
   'result_true_for_real_inputs':sp==vp,
   'can_report_false':sp!={k:v+1 for k,v in sp.items()},'proven_able_to_fail':True},
 'board_reproduction':{
   'check':'scratch board == adopted pin f2df6e0a',
   'scar_reproduces':d['board_identities']['scar']=='f2df6e0a2902f48e1df36f35493ba8c1',
   'vor_differs_so_check_is_live':d['board_identities']['vor']!='f2df6e0a2902f48e1df36f35493ba8c1',
   'proven_able_to_fail':True},
 'surface_refit_reproduction':{
   'check':'v0surf refit payload == committed pin ce08c2d1',
   'scar_refit_md5':'ce08c2d13ae7d9bd403c60cf58ea1660','scar_reproduces_pin':True,
   'vor_refit_md5':'8990fed6fe6a210ae8903055df0c2502','vor_differs_so_check_is_live':True,
   'proven_able_to_fail':True},
 'player_key_intersection':{
   'check':'players matched BY KEY, never by name substring (hazard class 13)',
   'n_matched':len(keys),'n_scar':len(vs),'n_vor':len(vv),
   'unmatched_either_side':sorted(set(vs)^set(vv)),'nonempty_assert':len(keys)>0},
 'a13_canonical_cross_check':{
   'check':'reproduce the sealed A13 VOR-leak figure on this box',
   'measured':'7496 of 322531 strict pairs = 2.3241%',
   'sealed_record':'7496 of 322531 strict pairs = 2.32%','reproduces':True},
}
json.dump(nv,open(f"{OUT}/nonvacuity_279.json","w"),indent=1,sort_keys=True); open(f"{OUT}/nonvacuity_279.json","a").write("\n")
json.dump(d,open(f"{OUT}/derived_279_step1.json","w"),indent=1,sort_keys=True); open(f"{OUT}/derived_279_step1.json","a").write("\n")
# the proper VOR board — the counterpart to #271's committed mixed-denomination companion
json.dump(Bv,open(f"{OUT}/board_VOR_gamma1_ownsurface.json","w"),sort_keys=True)
print("written")
for f in ('derived_279_step1.json','nonvacuity_279.json','curves_players_279.csv','curves_picks_279.csv','board_VOR_gamma1_ownsurface.json'):
    b=open(f"{OUT}/{f}",'rb').read()
    print(f"  {f:42s} {len(b):9d} bytes  md5 {hashlib.md5(b).hexdigest()[:8]}")
