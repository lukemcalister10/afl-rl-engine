import sys, json, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h, numpy as np
out=sys.argv[1]
g=h.boot()
MA=g['MA']; cp=g['cp']; ev=g['ev']
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
F=1.0524
rows={}
for p in priced:
    k=p.get('key')
    try:
        v=ev(p,2026); lvl=cp._lvl_eff(p,2026)
        gi=g['_abs_gap'](p,2026) if '_abs_gap' in g else None
        rows[k]=dict(player=p['player'], pos=MA.gfut(p), ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), age=cp._age_asof(p,2026),
                     gap=(dict(age_pre=gi['age_pre'],ret=gi['ret'],last=gi['last'],npost=gi['npost']) if gi else None),
                     scoring=[(x['year'],x['games'],round(x['avg'],1)) for x in p['scoring'] if x['games']>0])
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
print("DUMP %s: %d players  DAMP=%s ABSENCE=%s"%(out,len(rows),os.environ.get('RL_DAMP'),os.environ.get('RL_ABSENCE')))
