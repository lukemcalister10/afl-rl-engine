"""Prove whether channels 2a (unpl_eq) and 2b (pedestal) consume the swapped curve.
Recomputes the SAME expressions rl_model.value() uses, from module-level helpers, and reports
which branch each player takes. Run once per installed curve; compare the two dumps."""
import os,io,contextlib,json,sys
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
NAMES=json.load(open(sys.argv[1]))          # list of player keys
out={'curve_payload_in_use':None,'AGE_REF':MA.AGE_REF,'PROD_GATE':MA.PROD_GATE,
     'P_HOOK_is_none':MA.P_HOOK is None,'players':{}}
import hashlib
out['curve_payload_in_use']=hashlib.md5(json.dumps({str(k):int(MA._PVC2M[k]) for k in range(1,65)},sort_keys=True).encode()).hexdigest()[:8]
byk={p.get('key'):p for p in MA.data if p.get('key')}
for k in NAMES:
    p=byk.get(k)
    if p is None: out['players'][k]={'error':'not in store'}; continue
    ep=MA.effpk(p); decu=MA.los_decay(p)
    pvc=float(MA._PVC2M[min(ep,70)])
    unpl_eq=pvc*decu*MA.debut_factor(p)
    ln=MA.level_now(p)
    g=MA.gfut(p)
    rec={'ep':int(ep),'PVC2M_at_ep':pvc,'los_decay':round(decu,6),
         'debut_factor':round(MA.debut_factor(p),6),'unpl_eq':round(unpl_eq,4),
         'level_now':ln,'_unplayed':bool(p.get('_unplayed')),'_pedonly':bool(p.get('_pedonly')),
         'debut':MA.debut(p),'seasons':MA.seasons(p),'games':p.get('games'),'gfut':g}
    # which branch value() takes
    if p.get('_unplayed') and (MA.debut(p)>MA.AGE_REF or p.get('_pedonly')):
        rec['branch']='A: pure pedigree -> round(unpl_eq)'
    elif ln is None:
        rec['branch']='B: 0-game in window -> round(unpl_eq * Pz)'
    else:
        rec['branch']='C: production path (pedestal competes with prod_full)'
        try:
            relative=MA.clamp((MA.peak_est(p)/max(MA.basepk_c(g,ep),40.0))**2.2,0.40,3.0)
            decay=max(0.0,1-(MA.seasons(p)-1)/4.5)
            Pz=None if MA.P_HOOK is None else MA.P_HOOK(p)
            decay_eff=decay if Pz is None else min(decay,Pz)
            rec['pedestal']=round(pvc*relative*1.0*decay_eff,4)
            rec['prod_v']=round(MA.val(MA.player_raw(p,'bal')),4)
            rec['prod_floor']=round(MA.prod_floor(p,'bal'),4)
            rec['prod_full']=round(max(rec['prod_v'],rec['prod_floor']),4)
            rec['pedestal_binds']=rec['pedestal']>rec['prod_full']
        except Exception as e:
            rec['pedestal_error']=str(e)
    try:
        with contextlib.redirect_stdout(io.StringIO()): rec['value_bal']=MA.value(p,'bal')
    except Exception as e: rec['value_error']=str(e)
    out['players'][k]=rec
print(json.dumps(out,indent=1))
