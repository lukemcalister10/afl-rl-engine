import os, io, contextlib, sys, numpy as np
os.environ.setdefault('PYTHONHASHSEED','0')
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22').items(): os.environ.setdefault(k,v)
WS='/home/claude/rl_workspace/rl_after'
os.environ['RL_REPO']=os.environ.get('RL_REPO','/home/user/afl-rl-engine')
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,WS); os.chdir(WS)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; F=1.0524
_abs_gap=g['_abs_gap']; preabs=g['_lvl_eff_preabs']; abscur=cp._lvl_eff
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
for nm in ['bailey smith','buller','wilmot']:
    p=find(nm)
    if not p: print(nm,'NOT FOUND'); continue
    gi=_abs_gap(p,2026)
    v=ev(p,2026); lvl=abscur(p,2026)
    # abs off
    cp._lvl_eff=preabs
    try: v_off=ev(p,2026); lvl_off=preabs(p,2026)
    finally: cp._lvl_eff=abscur
    d0=cp.debutyr(p)
    gpost = sum(x['games'] for x in p['scoring'] if x['games']>0 and gi and x['year']>=gi['ret'] and (d0-1)<x['year']<=2026) if gi else None
    print("="*70)
    print(f"{p['player']}  pos={MA.gfut(p)} age={cp._age_asof(p,2026)}")
    print(f"  scoring: {[(x['year'],x['games'],round(x['avg'],1)) for x in p['scoring'] if x['games']>0]}")
    print(f"  gap: {gi}")
    print(f"  gpost(games since ret): {gpost}")
    print(f"  num(abs ON) ={int(round(v/F))}  lvl={lvl:.2f}")
    print(f"  num(abs OFF)={int(round(v_off/F))}  lvl={lvl_off:.2f}   => absence delta SCAR = {int(round(v/F))-int(round(v_off/F))}")
