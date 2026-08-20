"""ORDER E — engine loader (read-only, in-process). Mirrors o34_probe.py staging exactly."""
import os, sys, io, json, contextlib

ROOT = os.environ.get('RL_ROOT') or '/home/user/afl-rl-engine/.claude/worktrees/agent-a8f9b3afd299527e3'
os.environ.update(PYTHONHASHSEED='0', RL_REPO=ROOT,
                  OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1',
                  NUMEXPR_NUM_THREADS='1', VECLIB_MAXIMUM_THREADS='1',
                  RL_V0SURF_PKL=os.path.join(ROOT, 'data', 'v0surf.pkl'),
                  RL_GAMMA='1.0', RL_PICK1='3000', RL_RUCK_TAX='0.25', RL_RECENCY_DECAY='0.72',
                  RL_PRIOR_TREES='400', PAR_RAMPS='22',
                  RL_FV=os.path.join(ROOT, 'engine', 'forward_valuation'))
os.environ.setdefault('RL_O32', '1')          # the repaired Candidate 32 lane (implies RL_O31)


def load():
    sys.path[:0] = [ROOT, ROOT + '/vendor', ROOT + '/engine/forward_valuation', ROOT + '/engine/rl_after']
    os.chdir(ROOT + '/engine/rl_after')
    NSE = {}
    with contextlib.redirect_stdout(io.StringIO()):
        import rl_model as MA
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], NSE)
    MA = NSE.get('MA', MA)
    return MA, NSE


def price(G, p, Y=2026):
    with contextlib.redirect_stdout(io.StringIO()):
        return float(G['ev'](p, Y))
