# Boot the (improver) workspace engine under a given switch combo and dump per-player ev/num/lvl/age.
# usage: RL_EO2=.. RL_LSYM=.. RL_SAGE29=.. python3 dump.py <out.json>
# Switches default ON (as in-code); the caller sets them to 0 for ablations. Model vars are the pinned gate
# values (setdefault, so an explicit ablation env still wins). Analysis currency = num-SCAR = round(ev/1.0524).
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
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows={}
for p in priced:
    k=p.get('key')
    try:
        v=ev(p,2026); lvl=cp._lvl_eff(p,2026)
        rows[k]=dict(player=p['player'], pos=MA.gfut(p), ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), age=cp._age_asof(p,2026))
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
sw=dict(EO2=os.environ.get('RL_EO2','1'),LSYM=os.environ.get('RL_LSYM','1'),SAGE29=os.environ.get('RL_SAGE29','1'))
print(f"DUMP {os.path.basename(out)}: {len(rows)} players  switches={sw}")
