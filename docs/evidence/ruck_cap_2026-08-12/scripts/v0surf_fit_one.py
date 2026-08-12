"""ORDER 20C — ONE declared V0-surface refit, at ONE cap, in ONE process, dumped to a pickle.

Drives the COMMITTED refit entry point (`session_2026-07-18/legf6/scripts/refit_v0surf.py`, imported;
`_engine_surfaces()` called) — no fitting logic is re-implemented here. One process per fit is
deliberate: the engine head is not re-entrant (two `exec`s in one interpreter blow the recursion limit
inside `_inferM1`/`_lvl_eff_abs`), and a fit that shares module state with a previous fit is not a
clean reading.

Nothing is baked: `--bake` needs `RL_BAKE_V0SURF=1`, never set on this lane.

Usage: RC_TREE=<tree> RC_CAP=<value> RC_OUT=<dump.pkl> python3 v0surf_fit_one.py
"""
import os, sys, io, pickle, contextlib, importlib.util

TREE = os.environ['RC_TREE']
CAP = os.environ['RC_CAP']
OUT = os.environ['RC_OUT']

sys.path.insert(0, TREE + '/vendor')
sys.path.insert(0, TREE)
os.chdir(TREE + '/engine/rl_after')
sys.path.insert(0, '.')
os.environ['RL_RUC_PRIOR_CAP'] = CAP

spec = importlib.util.spec_from_file_location(
    'refit_v0surf', TREE + '/session_2026-07-18/legf6/scripts/refit_v0surf.py')
RV = importlib.util.module_from_spec(spec)
spec.loader.exec_module(RV)

with contextlib.redirect_stdout(io.StringIO()):
    sig, built = RV._engine_surfaces()

with open(OUT, 'wb') as f:
    pickle.dump({'cap': CAP, 'shipped_sig': sig, 'built': built}, f)
print("FIT cap=%s  shipped_sig=%s  keys=%s -> %s" % (CAP, sig[:12], sorted(built), OUT))
