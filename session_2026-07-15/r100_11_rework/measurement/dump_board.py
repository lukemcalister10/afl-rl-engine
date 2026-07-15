# Boot a given engine file and dump per-player ev/num/lvl/gap for the ablation.
# usage: python3 dump_board.py <engine_path> <out.json>
import os, io, contextlib, sys, json
os.environ['PYTHONHASHSEED']='0'
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22',RL_DAMP='1',RL_ABSENCE='1').items():
    os.environ.setdefault(k,v)
eng_path=sys.argv[1]; out=sys.argv[2]
WS='/home/claude/rl_workspace/rl_after'
os.environ.setdefault('RL_REPO','/home/user/afl-rl-engine')
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,WS); os.chdir(WS)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(eng_path).read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; F=1.0524
_abs_gap=g.get('_abs_gap')
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows={}
for p in priced:
    k=p.get('key')
    try:
        v=ev(p,2026); lvl=cp._lvl_eff(p,2026)
        gi=_abs_gap(p,2026) if _abs_gap else None
        rows[k]=dict(player=p['player'], pos=MA.gfut(p), ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), age=cp._age_asof(p,2026),
                     gap=(dict(age_pre=gi['age_pre'],ret=gi['ret'],last=gi['last'],
                               npost=gi['npost'],gpost=gi.get('gpost')) if gi else None))
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
print(f"DUMP {out}: {len(rows)} players  engine={os.path.basename(eng_path)}  ABSENCE={os.environ.get('RL_ABSENCE')} DAMP={os.environ.get('RL_DAMP')}")
