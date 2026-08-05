"""#279 step 4 — G3 follow-up. Does a config that leaves the SIGNATURE unchanged nevertheless change the
FITTED SURFACE? If yes, the signature has a blind spot for that config; if no, the signature is correctly
invariant. Measured, not reasoned — the G3 probe already disproved the 'RL_PICK1 is transitive' reading.

Prints: the signature, a content hash of the three fitted surfaces, and the _PVC0 head the signature reads.
"""
import os, sys, io, json, hashlib, contextlib

os.environ['RL_V0SURF_REFIT'] = '1'
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)

META = g['_V0CURVE_META']
sig = META['_v0surf_sig']
built = g.get('_V0SURF_BUILT') or {}
s = built.get(sig) or {}

def canon(o):
    if isinstance(o, dict):  return {str(k): canon(v) for k, v in sorted(o.items(), key=lambda kv: str(kv[0]))}
    if isinstance(o, (list, tuple)): return [canon(x) for x in o]
    if isinstance(o, float): return round(o, 10)
    try:    return canon(o.tolist())
    except Exception: return o

def h(o): return hashlib.md5(json.dumps(canon(o), sort_keys=True).encode()).hexdigest()[:16]

# the pick curve the signature actually reads
curve = g.get('_PVC0') if '_PVC0' in g else None
MA = g.get('MA')
pvc_live = getattr(MA, 'PVC', None) if MA is not None else None

print(json.dumps({
    'RL_GAMMA': os.environ.get('RL_GAMMA', '<unset>'),
    'RL_PICK1': os.environ.get('RL_PICK1', '<unset>'),
    'signature': sig,
    'surface_c18_hash':  h(s.get('c18')),
    'surface_surfN_hash': h(s.get('surfN')),
    'surface_surfR_hash': h(s.get('surfR')),
    '_PVC0_head': [curve.get(k) for k in (1, 2, 3, 64)] if isinstance(curve, dict) else None,
    'MA_PVC_head': [pvc_live.get(k) for k in (1, 2, 3, 64)] if isinstance(pvc_live, dict) else None,
}))
