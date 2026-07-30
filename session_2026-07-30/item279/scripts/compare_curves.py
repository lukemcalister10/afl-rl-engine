"""#279 step 1 — the two retrospective pick curves side by side, plus the corrected
players-vs-picks share in which BOTH sides move in the same currency."""
import json,sys,hashlib
import numpy as np
C=sys.argv[1]; SP=sys.argv[2]
def payload(ci):
    return hashlib.md5(json.dumps({str(i+1):v for i,v in enumerate(ci)},sort_keys=True).encode()).hexdigest()[:8]
S=json.load(open(f"{C}/derived_279_scar.json")); V=json.load(open(f"{C}/derived_279_vor.json"))
A=json.load(open(f"{C}/controlA_from_committed_matrix.json"))
adopted=json.load(open('/home/user/afl-rl-engine/engine/rl_after/pvc_curve_v2.json'))
ac=[adopted['curve'][str(k)] for k in range(1,65)]
cs,cv=S['curve']['integer'],V['curve']['integer']
out={'controls':{
   'controlA_committed_matrix_payload':payload(A['curve']['integer']),
   'adopted_payload':adopted['curve_md5'],
   'controlA_reproduces_adopted':payload(A['curve']['integer'])==adopted['curve_md5'],
   'scar_current_store_payload':payload(cs),
   'scar_reproduces_adopted':payload(cs)==adopted['curve_md5'],
   'scar_point_mismatches_vs_adopted':int(sum(1 for k in range(64) if cs[k]!=ac[k])),
   'vor_payload':payload(cv),
   'vor_differs_from_scar':payload(cv)!=payload(cs)},
 'meta':{'scar':S['meta'],'vor':V['meta']},
 'ladder_totals':{'adopted':int(sum(ac)),'scar':S['curve']['ladder_total'],'vor':V['curve']['ladder_total'],
                  'vor_over_scar':round(V['curve']['ladder_total']/S['curve']['ladder_total'],4)},
 'pool_level':{'scar':S['pool']['level_scar'],'vor':V['pool']['level_scar'],
               'n_scar':S['pool']['n'],'n_vor':V['pool']['n'],
               'never_established_scar':S['pool']['never_established'],
               'never_established_vor':V['pool']['never_established'],
               'vor_over_scar':round(V['pool']['level_scar']/S['pool']['level_scar'],4) if S['pool']['level_scar'] else None},
 'nd_last_band':{'scar':S['nd_last_band'],'vor':V['nd_last_band']},
 'curve_rows':{'scar':S['curve']['n_rows'],'vor':V['curve']['n_rows']},
}
pts=[]
for k in range(1,65):
    pts.append({'pick':k,'adopted':ac[k-1],'scar':cs[k-1],'vor':cv[k-1],
                'vor_over_scar':round(cv[k-1]/cs[k-1],4) if cs[k-1] else None})
out['curve_points']=pts
band=[(1,3),(4,7),(8,12),(13,20),(21,27),(28,35),(36,48),(49,64)]
out['by_band']=[{'band':f"{lo}-{hi}",
   'scar':int(sum(cs[k-1] for k in range(lo,hi+1))),'vor':int(sum(cv[k-1] for k in range(lo,hi+1))),
   'ratio':round(sum(cv[k-1] for k in range(lo,hi+1))/sum(cs[k-1] for k in range(lo,hi+1)),4)}
   for lo,hi in band]
# ---- corrected share: BOTH sides in the same currency ----
Bs=json.load(open(f"{SP}/board_085_forcedrefit.json")); Bv=json.load(open(f"{SP}/board_100_forcedrefit.json"))
ps=sum(r['v'] for r in Bs['active']); pv=sum(r['v'] for r in Bv['active'])
ls,lv=S['curve']['ladder_total'],V['curve']['ladder_total']
out['players_vs_picks_same_currency']={
 'basis':'players = sum of active board value (804 rows both columns); picks = re-derived ladder total '
         '1-64 under the SAME gamma. Both sides move; nothing frozen is held against a moving side.',
 'scar':{'players':int(ps),'picks':int(ls),'total':int(ps+ls),'picks_share_pct':round(100.0*ls/(ps+ls),4)},
 'vor':{'players':int(pv),'picks':int(lv),'total':int(pv+lv),'picks_share_pct':round(100.0*lv/(pv+lv),4)},
 'players_change_pct':round(100.0*(pv/ps-1),3),'picks_change_pct':round(100.0*(lv/ls-1),3),
 'share_point_change':round(100.0*lv/(pv+lv)-100.0*ls/(ps+ls),4)}
out['superseded_note']=('the earlier 8.1012% -> 8.3876% figure held a FROZEN ladder against a moving '
 'player side and is withdrawn; the figure above is the like-for-like one.')
print(json.dumps(out,indent=1))
