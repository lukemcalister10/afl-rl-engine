"""#279 step 4 — signature probe. Prints this build's v0surf config signature.

Runs the engine with RL_V0SURF_REFIT=1 (the declared refit lane) so the FROZEN-SIGNATURE HALT is bypassed
and the signature can be read for any env, including configs whose surface is not in the pickle.
Mirrors refit_v0surf.py's _engine_surfaces() exactly: exec _merged_recover.py from the workspace rl_after
and read _V0CURVE_META['_v0surf_sig'].
"""
import os, sys, io, json, contextlib

os.environ['RL_V0SURF_REFIT'] = '1'
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
sig = g['_V0CURVE_META']['_v0surf_sig']
built = sorted((g.get('_V0SURF_BUILT') or {}).keys())
print(json.dumps({
    'signature': sig,
    'all_built_signatures': built,
    'RL_GAMMA': os.environ.get('RL_GAMMA', '<unset>'),
    'RL_PICK1': os.environ.get('RL_PICK1', '<unset>'),
    'RL_RUCK_TAX': os.environ.get('RL_RUCK_TAX', '<unset>'),
}))
