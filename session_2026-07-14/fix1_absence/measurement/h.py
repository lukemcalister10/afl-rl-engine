import os, io, contextlib, sys
os.environ['PYTHONHASHSEED']='0'
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22').items(): os.environ.setdefault(k,v)
SP=os.path.dirname(os.path.abspath(__file__))
BOR=os.path.join(SP,'bor_ws')
os.environ['RL_Q97M_PKL']=os.path.join(BOR,'q97m.pkl')
os.environ['RL_REPO']=BOR
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,BOR); os.chdir(BOR)
def boot():
    g={}
    with contextlib.redirect_stdout(io.StringIO()):
        src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
        exec(src,g)
    return g
