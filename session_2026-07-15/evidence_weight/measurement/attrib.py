# ATTRIBUTION probe: dump the internal level terms that the four regimes consume, for key players.
# Lo=cp._lvl_eff_orig (exposure-shrunk baseline)  Lc=_lvlcurr (recency current)  par=_par_prior (pedigree)
# n=_nqual  E=cp._exposure  core=_coreM1 (live level pre-infer)  games=career games
import os, io, contextlib, sys
os.environ['PYTHONHASHSEED']='0'
for k,v in dict(RL_GAMMA='0.85',RL_PICK1='3000',RL_RUCK_TAX='0.25',RL_RECENCY_DECAY='0.72',
                RL_PRIOR_TREES='400',PAR_RAMPS='22').items(): os.environ.setdefault(k,v)
WS='/home/claude/rl_workspace/rl_after'
os.environ.setdefault('RL_REPO','/home/user/afl-rl-engine')
sys.path.insert(0,'/home/claude/rl_vendor'); sys.path.insert(0,WS); os.chdir(WS)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(os.path.join(WS,'_merged_recover.py')).read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; F=1.0524
_nqual=g['_nqual']; PROVEN_N=g['PROVEN_N']; _lvlcurr=g['_lvlcurr']; _par_prior=g['_par_prior']
_coreM1=g['_coreM1']; _lvl_eff_orig=cp._lvl_eff_orig
def _games(p,Y=2026): return sum(x['games'] for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y)
def find(nm):
    c=[p for p in MA.data if nm.lower()==p['player'].lower() and MA.GRP.get(p.get('pos'))]
    if not c: c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
NAMES=['Elijah Tsatas','Sam Berry','Harley Reid','Ryley Sanders','Marcus Bontempelli','Kieren Briggs',
       'Jamarra Ugle-Hagan','Bailey Smith','Nick Daicos','Max Gawn','Sam Darcy']
print(f"{'player':22}{'pos':8}{'age':>4}{'n':>3}{'gms':>4}{'E':>7}{'Lo':>7}{'Lc':>7}{'par':>7}{'core':>7}{'num':>7}")
for nm in NAMES:
    p=find(nm)
    if not p: print(f"{nm:22} NOT FOUND"); continue
    Y=2026
    Lo=_lvl_eff_orig(p,Y); Lc=_lvlcurr(p,Y); par=_par_prior(p,Y); core=_coreM1(p,Y)
    n=_nqual(p,Y); E=cp._exposure(p,Y); a=cp._age_asof(p,Y); num=int(round(ev(p,Y)/F))
    print(f"{p['player'][:21]:22}{MA.gfut(p):8}{a:4.0f}{n:3}{_games(p):4}{E:7.1f}{Lo:7.1f}{Lc:7.1f}{par:7.1f}{core:7.1f}{num:7}")
    sc=[(x['year'],x['games'],round(x['avg'],1)) for x in p['scoring'] if x['games']>0]
    print(f"    scoring: {sc}")
