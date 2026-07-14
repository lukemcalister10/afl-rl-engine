#!/usr/bin/env python3
"""PART 1 BISECT — fingerprint every BLAS-routed np.dot/np.matmul during a full board build.
Usage:  OPENBLAS_CORETYPE=<kernel> python3 bisect_dot.py <outfile>
Records, per call, in deterministic call order:
    seq  callsite(file:line)  input_fp  output_fp
input_fp  = sha1( float64 bytes of a  ++ float64 bytes of b )
output_fp = sha1( float64 bytes of the result )
Because OPENBLAS_CORETYPE changes ONLY OpenBLAS (numpy's own SIMD reductions are untouched),
any divergence between two runs of this script MUST first surface as a np.dot whose inputs are
bit-identical but whose output differs — that is the culprit reduction."""
import os, sys, io, contextlib, hashlib, traceback
WS = '/home/claude/rl_workspace/rl_after'
sys.path.insert(0, WS); sys.path.insert(0, '/home/claude/rl_vendor')
os.chdir(WS)
OUT = sys.argv[1]
import numpy as np

_sha1 = hashlib.sha1
def _fp(*arrs):
    h = _sha1()
    for a in arrs:
        af = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
        h.update(af.tobytes())
    return h.hexdigest()[:16]

def _callsite():
    # nearest engine frame: the engine is exec'd from a string so its frames are '<string>'
    for fr in reversed(traceback.extract_stack()[:-2]):
        if fr.filename == '<string>':
            return "_merged_recover.py:%d" % fr.lineno
        base = os.path.basename(fr.filename)
        if base not in ('bisect_dot.py',) and ('rl_after' in fr.filename or 'forward_valuation' in fr.filename):
            return "%s:%d" % (base, fr.lineno)
    return "?"

log = []
_odot = np.dot
_omat = np.matmul
def _wrap(orig):
    def w(a, b, *rest, **kw):
        r = orig(a, b, *rest, **kw)
        try:
            log.append((_callsite(), _fp(a, b), _fp(r)))
        except Exception:
            log.append((_callsite(), "ERR", "ERR"))
        return r
    return w
np.dot = _wrap(_odot)
np.matmul = _wrap(_omat)

# ---- full board build path: engine load (incl _build_v0_curve + ISO guard) then ev() as-of sequence ----
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
LOAD_N = len(log)
MA = g['MA']; ev = g['ev']
raw_evs = {}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        v = ev(p, 2026); ev(p, 2024); ev(p, 2025); ev(p, 2027); ev(p, 2028)  # export's as-of sequence
        raw_evs[p['key']] = v
# write fingerprint log
with open(OUT, 'w') as f:
    f.write("# kernel=%s  total_dot=%d  load_dot=%d\n" % (os.environ.get('OPENBLAS_CORETYPE', 'native'), len(log), LOAD_N))
    for i, (site, ifp, ofp) in enumerate(log):
        f.write("%d\t%s\t%s\t%s\n" % (i, site, ifp, ofp))
# write per-player raw ev (float64 hex) for B3
import struct
with open(OUT + ".ev", 'w') as f:
    for k in sorted(raw_evs):
        f.write("%s\t%s\t%.17g\n" % (k, struct.pack('>d', raw_evs[k]).hex(), raw_evs[k]))
print("wrote %s : %d dot calls (%d at load), %d players" % (OUT, len(log), LOAD_N, len(raw_evs)))
