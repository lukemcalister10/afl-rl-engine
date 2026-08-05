#!/usr/bin/env python3
"""#306 LANDING — why the #323 corrected store cannot ride the converged surface.

Reads the engine's OWN signature function (`_v0surf_sig` in `_merged_recover.py`) on whichever
store is currently installed, prints the signature, says whether `data/v0surf.pkl` holds a fitted
surface under it, and prints each leg of the signature payload separately so the moving leg is
named rather than guessed.

Run from the workspace rl_after, single-thread, RL_REPO set. One argument: a label for the run.
"""
import contextlib, hashlib, io, json, os, pickle, sys

label = sys.argv[1] if len(sys.argv) > 1 else 'run'
repo = os.environ.get('RL_REPO') or '/home/user/afl-rl-engine'

g = {}
halted = False
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
except SystemExit:
    # The frozen-signature HALT is the very condition this probe exists to describe: the engine
    # refuses to continue when no fitted surface matches. Everything the signature reads (MA, the
    # roster sample, the pick curve) is already built by then, so the measurement below still holds.
    halted = True

MA = g['MA']
real = MA._curve_sample('v0_kernel', 0,
                        [p for p in MA.data if g['_isreal'](p) and p.get('type') == 'ND'
                         and p.get('pick') is not None and not MA.is_pool(p)])
curve = g.get('_PVC0', MA.PVC)
gates = {k: os.environ.get(k, d) for k, d in sorted(g['_V0SURF_GATES'].items())}
legs = {
    'pvc': sorted((int(k), int(v)) for k, v in curve.items()),
    'roster': sorted([str(MA.gfut(p)), g['_ageR'](p), int(p.get('pick'))] for p in real),
    'gates': gates,
}


def h(o):
    return hashlib.md5(json.dumps(o, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


sig = h(legs)
store = hashlib.md5(open(os.path.join(repo, 'engine/rl_after/rl_model_data.json'), 'rb').read()).hexdigest()
with open(os.path.join(repo, 'data/v0surf.pkl'), 'rb') as f:
    frozen = pickle.load(f)
frozen_keys = sorted(frozen) if isinstance(frozen, dict) else []

print(json.dumps({
    'label': label,
    'engine_halted_on_frozen_signature': halted,
    'installed_store_md5': store,
    'v0surf_signature': sig,
    'signature_in_frozen_pickle': sig in frozen_keys,
    'frozen_signatures': frozen_keys,
    'leg_hashes': {k: h(v) for k, v in legs.items()},
    'roster_rows': len(legs['roster']),
    'pvc_entries': len(legs['pvc']),
}, indent=2, sort_keys=True))
