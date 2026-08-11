import io, contextlib, os, sys, json, hashlib
import engine_load
ROOT = engine_load.ROOT; RA = engine_load.RA
os.chdir(RA)
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(src, '_merged_recover.py', 'exec'), g)
except SystemExit as e:
    print('HALT caught')
except BaseException as e:
    print('ERR', type(e).__name__, e)
MA = g.get('MA')
print('has MA', MA is not None, 'has _isreal', '_isreal' in g, 'has _PVC0', '_PVC0' in g)
_isreal = g['_isreal']; _ageR = g['_ageR']; GATES = g['_V0SURF_GATES']
_curve = g['_PVC0'] if '_PVC0' in g else MA.PVC
real = MA._curve_sample('v0_kernel', 0,
        [p for p in MA.data if _isreal(p) and p.get('type') == 'ND' and p.get('pick') is not None
         and not MA.is_pool(p)])
pvc = sorted((int(k), int(v)) for k, v in _curve.items())
roster = sorted([str(MA.gfut(p)), _ageR(p), int(p.get('pick'))] for p in real)
gates = {k: os.environ.get(k, d) for k, d in sorted(GATES.items())}
def h(o): return hashlib.md5(json.dumps(o, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
print('n_real', len(real))
print('pvc leg  ', h(pvc))
print('roster leg', h(roster))
print('gates leg ', h(gates))
print('gates', gates)
print('full', h({'pvc': pvc, 'roster': roster, 'gates': gates}))
import collections
print('age hist', collections.Counter(a for _, a, _ in roster))
print('pvc head', pvc[:5], 'pool', [x for x in pvc if x[0] >= 64][:3])
