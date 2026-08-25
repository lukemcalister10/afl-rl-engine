#!/usr/bin/env python3
"""THE SCALED NET — prereg prediction in the ADOPTED candidate world (board 543bf900).
Owner rulings 2026-08-25: D2 position-scaled ramp (knots 40-45 x posbar/77.1, smoothstep);
D3 mature-agers (entry age >=22) EXCLUDED; scope = no banked level, >=1 career game, tenure 1-4
(entry-year convention), active. Lift = lambda(c) * max(0, cf - v). Read-only; writes the
prediction JSON only.

USAGE (the candidate world; wsF seeded FROM root_final with fv_provenance/config_manifest/boot_guard/
LTI_REGISTER.md copied in — see register v854):
  cd /home/user/arm2_norec/wsF/rl_after && \
  env RL_CONFIG_MODE=gate RL_REPO=/home/user/arm2_norec/root_final \
      RL_FV=/home/user/arm2_norec/root_final/engine/forward_valuation \
      RL_CM_PKL=/home/user/arm2_norec/root_final/data/cm_400.pkl \
      RL_Q97M_PKL=/home/user/arm2_norec/root_final/data/q97m.pkl \
      PYTHONPATH=/home/user/arm2_norec/wsF/rl_after:/home/claude/rl_vendor \
      OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
      /root/rl_venv312/bin/python3 /home/user/seam_fix/predict_net.py"""
import contextlib, io, json, os, sys
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; evf=g['ev']; F=1.0524; Y=2026
bars={k:(v-3.0) for k,v in MA.REPL.items()}
def lam(c,pos):
    s=bars.get(pos,77.1)/77.1
    lo,hi=40.0*s,45.0*s
    if c<=lo: return 0.0
    if c>=hi: return 1.0
    t=(c-lo)/(hi-lo); return 3*t*t-2*t*t*t
rows=[]
for p in MA.data:
    if p.get('_retired'): continue
    sc=[x for x in (p.get('scoring') or []) if x.get('year',0)<=Y]
    gtot=sum(x.get('games',0) for x in sc)
    if gtot<1 or any(x.get('games',0)>=6 for x in sc): continue
    ten=Y-int(p.get('year') or Y)+1
    if ten>4: continue
    by=p.get('_by'); ea=(int(p.get('year'))-int(by)) if by and p.get('year') else None
    if ea is not None and ea>=22: continue                     # D3: mature-agers excluded
    c=sum(x['avg']*x['games'] for x in sc)/gtot
    pos=MA.GRP.get(MA.gfut(p) if hasattr(MA,'gfut') else p.get('pos')) or MA.GRP.get(p.get('pos'))
    v=evf(p,Y)/F
    s0=p['scoring']; p['scoring']=[]
    try: cf=evf(p,Y)/F
    finally: p['scoring']=s0
    L=lam(c,pos)
    lift=round(L*max(0.0,cf-v))
    if lift>0:
        rows.append({'key':p.get('key'),'player':p.get('player'),'pos':pos,'tenure':ten,'games':int(gtot),
                     'cameo':round(c,1),'v':round(v),'cf':round(cf),'lambda':round(L,3),'lift':lift,'new':round(v)+lift})
rows.sort(key=lambda r:-r['lift'])
tot=sum(r['lift'] for r in rows)
json.dump({'world':'root_final (board 543bf900)','rulings':'D2 scaled, D3 mature excluded, scope t1-4 no-banked-level',
           'movers':rows,'total_lift':tot}, open('/home/user/seam_fix/NET_PREDICTION.json','w'), indent=1)
print('NET PREDICTION on the candidate world: %d movers, total +%d' % (len(rows),tot))
for r in rows: print('  %-24s %-4s t%d c=%5.1f  %4d -> %4d (+%d, lam %.2f)' % (r['player'],r['pos'],r['tenure'],r['cameo'],r['v'],r['new'],r['lift'],r['lambda']))
