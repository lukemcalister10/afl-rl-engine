# Boot the workspace engine under RL_ISOFADE and dump per-player ev/num/lvl/age + projection margin.
# usage: RL_ISOFADE=0|1 python3 dump.py <out.json>   (default ON as in-code)
# Model vars = pinned gate values (setdefault, so an explicit ablation env still wins). Currency = num = round(ev/1.0524).
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
MA=g['MA']; cp=g['cp']; ev=g['ev']; _lvlcurr=g['_lvlcurr']; _par_prior=g['_par_prior']
_ev_qual=g['_ev_qual']; iso_eff=g['iso_eff']; raw_ev=g['raw_ev']; F=1.0524; Y=2026
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows={}
for p in priced:
    k=p.get('key')
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            v=ev(p,Y); lvl=cp._lvl_eff(p,Y); Lc=_lvlcurr(p,Y); par=_par_prior(p,Y)
            gf=MA.gfut(p); bar=MA.REPL.get(gf,0.0)-3.0; Eq=_ev_qual(p,Y); iso=iso_eff(p,Y); rawe=raw_ev(p,Y)
        rows[k]=dict(player=p['player'], pos=gf, ev=float(v), num=int(round(v/F)),
                     lvl=float(lvl), Lc=float(Lc), par=float(par), bar=float(bar), rawev=repr(float(rawe)),
                     age=cp._age_asof(p,Y), effpk=int(MA.effpk(p)), Eq=round(float(Eq),3), iso=repr(float(iso)),
                     pormargin=round(float(Lc-par),2))   # demonstrated recency level minus pedigree par projection; rawev/iso = full-precision repr for byte-identity decomposition
    except Exception as e:
        rows[k]=dict(player=p['player'], error=repr(e))
json.dump(rows, open(out,'w'))
print(f"DUMP {os.path.basename(out)}: {len(rows)} players  RL_ISOFADE={os.environ.get('RL_ISOFADE','1')}")
