"""Print the #336 reference tables + guard under whatever channel dials are in the environment."""
import sys, os, json
sys.path.insert(0,'/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
import engine_load
g = engine_load.load()
MA = g['MA']
out = {}
out['A2_GUARD_breaches'] = len(MA._A2_GUARD)
out['A2_GUARD_cells'] = [[x[0], x[1], round(MA.BASEPK_EST[x],4), round(MA.BASEPK_REG[x],4),
                          round(MA.BASEPK_EST[x]-MA.BASEPK_REG[x],4)] for x in MA._A2_GUARD]
out['NB'] = MA.NB
gs = sorted(set(MA.GRP.values()))
out['BASEPK_REG'] = {gg: [round(MA.BASEPK_REG[(gg,b)],4) for b in range(MA.NB)] for gg in gs}
out['BASEPK_EST'] = {gg: [round(MA.BASEPK_EST[(gg,b)],4) for b in range(MA.NB)] for gg in gs}
out['POOL'] = [round(MA.POOL[b],4) for b in range(MA.NB)]
out['POOL_COND336'] = [round(MA.POOL_COND336[b],4) for b in range(MA.NB)]
out['A3_D'] = MA._dbpk_336('MID',3)
# par surface probe
PR = g['PR']
out['par'] = {f"{p}_{t}": round(float(PR.par_at('MID',p,t)),4) for p in (1,7,30,60) for t in (1,4)}
out['par_KPD'] = {f"{p}_{t}": round(float(PR.par_at('KPD',p,t)),4) for p in (7,40) for t in (1,4)}
# monotone in pick check on BASEPK_REG
nonmono = [(gg,b) for gg in gs for b in range(1,MA.NB) if MA.BASEPK_REG[(gg,b)] > MA.BASEPK_REG[(gg,b-1)]+1e-9]
out['BASEPK_REG_nonmono'] = len(nonmono)
print(json.dumps(out, indent=1))
