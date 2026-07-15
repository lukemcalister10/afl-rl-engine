# Attribute the EVW move for named players: decompose core (base vs new) + ev/num under RL_EVW 0/1.
import os, io, contextlib, sys, math
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
Lo_f=cp._lvl_eff_orig; _lvlcurr=g['_lvlcurr']; _par=g['_par_prior']; _est=g['_est']
_ev_qual=g['_ev_qual']; _ev_rec=g['_ev_rec']; _ev_est=g['_ev_est']; _ev_pw=g['_ev_pw']; _nqual=g['_nqual']
def find(nm):
    c=[p for p in MA.data if nm.lower()==p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
Y=2026
print(f"{'player':20}{'n':>2}{'E_q':>6}{'Lo':>7}{'Lc':>7}{'par':>7}{'est':>7}{'rec':>6}{'estw':>6}{'pw':>6}{'coreB':>7}{'coreN':>7}")
for nm in ['Josh Ward','Jack Ginnivan','Nathan Ward','Tristan Xerri','Sam Berry','Elijah Tsatas']:
    p=find(nm)
    if not p: print(f"{nm} NOT FOUND"); continue
    Lo=Lo_f(p,Y); Lc=_lvlcurr(p,Y); par=_par(p,Y); est=_est(p,Y,Lo,Lc)
    Eq=_ev_qual(p,Y); rec=_ev_rec(Eq); estw=_ev_est(Eq); pw=_ev_pw(Eq)
    # base core (four regimes): reproduce via nqual
    n=_nqual(p,Y)
    if n==0: coreB=Lo
    elif n>=4: coreB=est
    else: coreB=(n/4.0)*Lc+(1-n/4.0)*par
    Lrec=Lo+rec*(Lc-Lo); prod=(1-estw)*Lrec+estw*est; coreN=(1-pw)*prod+pw*par
    print(f"{p['player'][:19]:20}{n:2}{Eq:6.2f}{Lo:7.1f}{Lc:7.1f}{par:7.1f}{est:7.1f}{rec:6.2f}{estw:6.2f}{pw:6.2f}{coreB:7.1f}{coreN:7.1f}")
    print(f"     scoring: {[(x['year'],x['games'],round(x['avg'],1)) for x in p['scoring'] if x['games']>0]}")
