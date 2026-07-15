# Boot the (candidate) workspace engine under a given RL_CAPT combo and dump per-player ev/num/lvl/age + the
# captaincy credit at the current-year level (both the ruled and the retired saturating value, for attribution).
# usage: RL_CAPT=.. python3 dump.py <out.json>
# RL_CAPT default ON (in-code); caller sets RL_CAPT=0 for the base (retired saturating) ablation. Model vars are
# the pinned gate values (setdefault, so an explicit ablation env still wins). Currency = num-SCAR = round(ev/1.0524).
import os, io, contextlib, sys, json
os.environ['PYTHONHASHSEED']='0'
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22').items():
    os.environ.setdefault(k,v)
out=os.path.abspath(sys.argv[1])   # resolve BEFORE the chdir(WS) below
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
        # captaincy credit at the current-year level under BOTH curves (attribution; capt_prem itself follows RL_CAPT)
        cr_ruled=MA._capt_ruled(float(lvl)); cr_sat=MA._capt_saturating(float(lvl)); cr_live=MA.capt_prem(float(lvl))
        rows[k]=dict(player=p['player'], pos=MA.gfut(p), ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), age=cp._age_asof(p,2026),
                     cr_ruled=float(cr_ruled), cr_sat=float(cr_sat), cr_live=float(cr_live))
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
print(f"DUMP {os.path.basename(out)}: {len(rows)} players  RL_CAPT={os.environ.get('RL_CAPT','1')}")
