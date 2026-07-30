import json, math, hashlib, itertools, sys
import numpy as np
SP=sys.argv[1]
def L(f): return json.load(open(f"{SP}/{f}"))
def md5(f): return hashlib.md5(open(f"{SP}/{f}",'rb').read()).hexdigest()

B={'scar':L('board_085_forcedrefit.json'),'scar_frozen':L('board_085_frozenload.json'),
   'vor':L('board_100_forcedrefit.json'),'vor_mixed':L('board_100_frozenload.json')}
M={k:md5({'scar':'board_085_forcedrefit.json','scar_frozen':'board_085_frozenload.json',
          'vor':'board_100_forcedrefit.json','vor_mixed':'board_100_frozenload.json'}[k]) for k in B}
out={'board_identities':M,'gammas':{k:B[k]['GAMMA'] for k in B},'scales':{k:B[k]['SCALE'] for k in B}}

# ---------- players, matched BY KEY (never by name/substring: hazard class 13) ----------
def vmap(b): return {r['key']:r['v'] for r in b['active']}
vs,vv = vmap(B['scar']), vmap(B['vor'])
vm = vmap(B['vor_mixed'])
keys=sorted(set(vs)&set(vv))
assert len(keys)>0, "EMPTY player intersection"
out['players']={'n_scar':len(vs),'n_vor':len(vv),'n_matched':len(keys),
                'unmatched_scar':sorted(set(vs)-set(vv)),'unmatched_vor':sorted(set(vv)-set(vs))}
a=np.array([vs[k] for k in keys],float); b=np.array([vv[k] for k in keys],float)
def stats(x): 
    return {'sum':int(x.sum()),'mean':round(float(x.mean()),1),'median':round(float(np.median(x)),1),
            'p90':round(float(np.percentile(x,90)),1),'p10':round(float(np.percentile(x,10)),1),
            'max':int(x.max()),'min':int(x.min())}
out['players']['scar']=stats(a); out['players']['vor']=stats(b)
out['players']['total_ratio_vor_over_scar']=round(float(b.sum()/a.sum()),4)

# decile curve by SCAR rank
order=np.argsort(-a); ad,bd=a[order],b[order]
dec=[]
for i in range(10):
    lo,hi=int(i*len(ad)/10),int((i+1)*len(ad)/10)
    dec.append({'decile':i+1,'n':hi-lo,'scar_mean':round(float(ad[lo:hi].mean()),1),
                'vor_mean':round(float(bd[lo:hi].mean()),1),
                'ratio':round(float(bd[lo:hi].sum()/ad[lo:hi].sum()),4)})
out['players']['deciles_by_scar_rank']=dec
kk=[keys[i] for i in order[:20]]
out['players']['top20_by_scar']=[{'key':k,'scar':int(vs[k]),'vor':int(vv[k]),
                                 'ratio':round(vv[k]/vs[k],4)} for k in kk]

# ---------- rank movement: ORDER-INDEPENDENT ALL-PAIRS (A13 instrument note) ----------
def allpairs(x,y):
    """count over ALL i<j pairs; denominator = pairs STRICTLY ordered in x."""
    dx=x[:,None]-x[None,:]; dy=y[:,None]-y[None,:]
    iu=np.triu_indices(len(x),1)
    dx,dy=dx[iu],dy[iu]
    strict=dx!=0
    n_strict=int(strict.sum())
    inv=int(((dx>0)&(dy<0)).sum()+((dx<0)&(dy>0)).sum())
    tie_collapse=int((strict&(dy==0)).sum())
    return {'n_pairs_total':int(len(dx)),'n_pairs_strict_in_first':n_strict,
            'inversions':inv,'inversion_pct':round(100.0*inv/n_strict,4) if n_strict else None,
            'tie_collapses':tie_collapse,
            'tie_collapse_pct':round(100.0*tie_collapse/n_strict,4) if n_strict else None}
out['rank_movement_scar_vs_vor']=allpairs(a,b)
# NON-VACUITY: identical input must give 0; a deliberate perturbation must give >0
ctrl=allpairs(a,a.copy())
pert=a.copy(); i1,i2=int(order[0]),int(order[len(order)//2]); pert[i1],pert[i2]=pert[i2],pert[i1]
pv=allpairs(a,pert)
out['rank_movement_nonvacuity']={
  'control_identical_inversions':ctrl['inversions'],
  'control_passes(expect 0)':ctrl['inversions']==0,
  'perturbed_one_swap_inversions':pv['inversions'],
  'perturbed_detects(expect >0)':pv['inversions']>0}
assert ctrl['inversions']==0 and pv['inversions']>0, "rank metric is VACUOUS"

# ---------- pick curves ----------
sp={int(k):int(v) for k,v in B['scar']['PVC'].items()}
vp={int(k):int(v) for k,v in B['vor']['PVC'].items()}
out['shipped_pick_ladder']={'identical_under_both_gamma':sp==vp,
  'n_points':len(sp),'sample':{str(k):sp[k] for k in (1,2,3,10,24,40,57,64,65)},
  'ladder_sum_1_64':int(sum(sp[k] for k in range(1,65))),
  'why':'board ships the frozen adopted curve (L7 repoint, pvc_curve_v2.json); gamma cannot reach it'}
# non-vacuity for the ladder-equality check: it must be able to report False
out['shipped_pick_ladder']['nonvacuity_check_can_fail']= (sp != {k:v+1 for k,v in sp.items()})

pa=L('pickval_0.85.json'); pb=L('pickval_1.0.json')
pr={}
for k in map(str,range(1,65)):
    pr[k]={'raw':round(pa['picks'][k]['raw'],4),'scar':pa['picks'][k]['val'],'vor':pb['picks'][k]['val'],
           'ratio':round(pb['picks'][k]['val']/pa['picks'][k]['val'],4) if pa['picks'][k]['val'] else None}
out['model_pick_value_gamma_responsive']={
  'note':'val(pick_raw(k)) in board currency, BEFORE the frozen-ladder repoint. Band-resolved (8 bands), so picks inside a band share a value.',
  'raw_production_identical_across_gamma':all(abs(pa['picks'][k]['raw']-pb['picks'][k]['raw'])<1e-12 for k in pa['picks']),
  'by_pick':pr,'pool':{'scar':pa['pool'],'vor':pb['pool']}}

# ---------- conservation yardstick (S-3 shape) under each ----------
def cons(b):
    lc=b['lensConservation']['+1']; dt=b['draftAssetTotals']['+1']
    tot=lc['picks']+lc['players']
    return {'lensYear':lc['lensYear'],'nPicks':lc['nPicks'],'nPlayers':lc['nPlayers'],
            'picks_face':lc['picks'],'players_sum':lc['players'],'total':tot,
            'picks_share_pct':round(100.0*lc['picks']/tot,4),
            'entrant_layer_pvc':dt['f5_entrant_layer_pvc'],'visible_1_64':dt['visible_1_64']}
out['conservation']={'scar':cons(B['scar']),'vor':cons(B['vor']),
  'reading':'the pick ladder is frozen, so under VOR the player pool shrinks against an unchanged ladder and picks become dearer AS A CLASS'}

# ---------- what the own-surface bake is worth ----------
km=sorted(set(vs)&set(vm))
am=np.array([vv[k] for k in km],float); bm=np.array([vm[k] for k in km],float)
diff=int((am!=bm).sum())
out['own_surface_bake_effect']={
  'vor_own_surface_board':M['vor'],'vor_loaded_scar_surface_board':M['vor_mixed'],
  'boards_differ':M['vor']!=M['vor_mixed'],
  'n_matched':len(km),'n_players_whose_value_changes':diff,
  'pct_players_changed':round(100.0*diff/len(km),2),
  'max_abs_delta':int(np.abs(am-bm).max()),'sum_own':int(am.sum()),'sum_mixed':int(bm.sum()),
  'rank_movement_own_vs_mixed':allpairs(am,bm)}
# the 0.85 symmetry proof
out['forced_refit_symmetry']={'scar_forced_refit':M['scar'],'scar_frozen_load':M['scar_frozen'],
  'identical':M['scar']==M['scar_frozen'],
  'meaning':'forcing the own-bake lane is not itself an artifact at 0.85'}
print(json.dumps(out,indent=1,sort_keys=True))
