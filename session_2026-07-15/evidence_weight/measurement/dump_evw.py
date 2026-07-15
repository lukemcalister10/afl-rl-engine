# Boot the workspace engine and dump per-player {ev,num,lvl,age + evidence fields} for the EVW ablation.
# Evidence fields (games/nqual/proven_n-status/exposure) explain each mover per the directive.
# usage: python3 dump_evw.py <out.json>   (RL_EVW read from ambient env; default ON in-engine)
import os, io, contextlib, sys, json
os.environ['PYTHONHASHSEED']='0'
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22').items():
    os.environ.setdefault(k,v)
out=sys.argv[1]
WS='/home/claude/rl_workspace/rl_after'
os.environ.setdefault('RL_REPO','/home/user/afl-rl-engine')
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,WS); os.chdir(WS)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(WS,'_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; F=1.0524
_nqual=g['_nqual']; PROVEN_N=g['PROVEN_N']
def _games(p,Y=2026): return sum(x['games'] for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y)
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows={}
for p in priced:
    k=p.get('key')
    try:
        v=ev(p,2026); lvl=cp._lvl_eff(p,2026)
        rows[k]=dict(player=p['player'], pos=MA.gfut(p), ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), age=round(cp._age_asof(p,2026),1),
                     nqual=int(_nqual(p,2026)), games=int(_games(p)),
                     expo=round(float(cp._exposure(p,2026)),2),
                     proven=bool(_nqual(p,2026)>=PROVEN_N))
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
ok=sum(1 for r in rows.values() if 'error' not in r)
print(f"DUMP {out}: {len(rows)} players ({ok} ok)  EVW={os.environ.get('RL_EVW','(default ON)')}")
