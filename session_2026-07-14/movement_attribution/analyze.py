#!/usr/bin/env python3
"""Analysis over census_data.json: M1 ranking, M2 denied-credit, M3 eo/English test, M4 thin-hot-sample.
Reads the base decomposition; re-loads the engine ONLY to price M2 hypothetical credits + M4 counterfactuals."""
import io,contextlib,json,copy,numpy as np
D=json.load(open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/census_data.json'))
rows=D['rows']; NB=D['NB']
def f(x): return 0.0 if x is None else x

# ---------- quick distributions ----------
from collections import Counter
bc=Counter(r['branch'] for r in rows)
print('BRANCH COUNTS:',dict(bc))
prov=[r for r in rows if r['n']>=4]
risers=[r for r in prov if r['branch']=='rising']
print('proven=%d risers=%d  (rising among proven)'%(len(prov),len(risers)))
# risers with improvement>0
imp_pos=[r for r in risers if r['improvement']>1e-9]
print('risers with improvement>0:',len(imp_pos))
tol_denied=[r for r in imp_pos if not r['passes_tol']]   # 0<imp<5
radq_denied=[r for r in imp_pos if r['passes_tol'] and not r['passes_radq']]  # imp>=5, radq fail
credited=[r for r in imp_pos if r['passes_tol'] and r['passes_radq']]         # got (possibly sage=0) credit
print('  denied-by-TOL(0<imp<5):',len(tol_denied))
print('  denied-by-radq(imp>=5,radq fail):',len(radq_denied))
print('  passed-both-gates:',len(credited))
# 4.0-4.9 near miss
neartol=[r for r in tol_denied if 4.0<=r['improvement']<5.0]
print('  TOL near-miss 4.0-4.9:',len(neartol))
# radq 10/11 games near miss
radq_1011=[r for r in radq_denied if r['best_recent_games'] in (10,11)]
print('  radq denied on 10 or 11 games:',len(radq_1011))
# 30+ zero credit (passed gates but sage=0 -> granted ~0)
zero30=[r for r in credited if r['age'] is not None and r['age']>=30 and r['sage']<=1e-9]
print('  age30+ passed gates but sage=0 (zero credit):',len(zero30))
# eo distribution
eos=[r['eo'] for r in rows]
print('eo: n_at_1.0=%d  n>=0.99=%d  n>=0.95=%d  n==0=%d  mean=%.3f'%(
    sum(1 for e in eos if e>=0.999),sum(1 for e in eos if e>=0.99),
    sum(1 for e in eos if e>=0.95),sum(1 for e in eos if e<=1e-9),float(np.mean(eos))))
# eo drag: players where eo actually pulled down (eo_lvl<0)
eo_bit=[r for r in rows if r['eo_lvl']<-1e-6]
print('players eo actually dragged (eo_lvl<0):',len(eo_bit))
