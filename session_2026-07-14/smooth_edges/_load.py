# Shared loader: exec the engine, expose ev, MA, and internal fns.
import io,contextlib,os,sys
os.environ.setdefault('PYTHONHASHSEED','0'); os.environ.setdefault('RL_GAMMA','0.85')
os.environ.setdefault('RL_PICK1','3000'); os.environ.setdefault('RL_RUCK_TAX','0.25')
os.environ.setdefault('RL_RECENCY_DECAY','0.72'); os.environ.setdefault('RL_PRIOR_TREES','400')
os.environ.setdefault('PAR_RAMPS','22')
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,WS)
os.chdir(WS)
G={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
def find(nm):
    c=[p for p in G['MA'].data if nm.lower() in p['player'].lower() and G['MA'].GRP.get(p.get('pos'))]
    return c[0] if c else None
