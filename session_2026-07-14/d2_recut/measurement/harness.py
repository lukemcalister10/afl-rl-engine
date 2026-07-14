import os, io, contextlib, sys
os.environ['PYTHONHASHSEED']='0'; os.environ.setdefault('RL_GAMMA','0.85')
os.environ.setdefault('RL_PICK1','3000'); os.environ.setdefault('RL_RUCK_TAX','0.25')
os.environ.setdefault('RL_RECENCY_DECAY','0.72'); os.environ.setdefault('RL_PRIOR_TREES','400')
os.environ.setdefault('PAR_RAMPS','22')
BOR='/tmp/bor_ws'
sys.path.insert(0, '/home/claude/rl_vendor'); sys.path.insert(0, BOR)
os.chdir(BOR)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
    exec(src, g)
# expose
MA=g['MA']; ev=g['ev']; cp=g['cp']; PR=g['PR']
def get(name): return g[name]
