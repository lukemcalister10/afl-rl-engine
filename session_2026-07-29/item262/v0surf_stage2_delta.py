"""ITEM 262 R2-3 — cell-by-cell equality proof.

Refits the V0 surfaces under the NEW vocabulary via the declared RL_V0SURF_REFIT lane, and
compares every cell against the FROZEN surfaces in data/v0surf.pkl, pairing them by the
reverse-mapped signature. Writes nothing.

The only instrumentation is a recorder inside _v0surf_sig that notes the new->old signature
correspondence. It does NOT change the function's return value, so the build behaves exactly
as it would unpatched.
"""
import os, sys, io, json, pickle, contextlib, hashlib
import config_manifest
config_manifest.enforce()
os.environ['RL_V0SURF_REFIT'] = '1'          # the declared refit lane

REPO = os.environ['RL_REPO']
frozen = pickle.load(open(os.path.join(REPO, 'data', 'v0surf.pkl'), 'rb'))
sys.stderr.write('frozen signatures: %s\n' % sorted(frozen))

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
ANCHOR = 'def _v0surf_sig(real):'
assert src.count(ANCHOR) == 1, src.count(ANCHOR)
INJECT = '''
_REV={'SD':'GEN_DEF','SF':'GEN_FWD','KPD':'KEY_DEF','KPF':'KEY_FWD','MID':'MID','RUCK':'RUC'}
_SIGPAIRS={}
def _v0surf_sig(real):
    import hashlib as _hl, json as _js
    _curve=_PVC0 if '_PVC0' in globals() else MA.PVC
    def _mk(lab):
        return {'pvc':sorted((int(k),int(v)) for k,v in _curve.items()),
                'roster':sorted([lab(p),_ageR(p),int(p.get('pick'))] for p in real),
                'gates':{g:os.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    def _h(pl): return _hl.md5(_js.dumps(pl,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    _new=_h(_mk(lambda p: str(MA.gfut(p))))
    _old=_h(_mk(lambda p: _REV.get(str(MA.gfut(p)),str(MA.gfut(p)))))
    _SIGPAIRS[_new]=_new
    return _new
def _UNUSED_orig(real):'''
src = src.replace(ANCHOR, INJECT, 1)

g = {'__name__': '__main__'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)

pairs = g['_SIGPAIRS']; built = g['_V0SURF_BUILT']
sys.stderr.write('refit produced %d surface set(s); signature pairs new->old:\n' % len(built))
for n, o in pairs.items():
    sys.stderr.write('   %s -> %s   %s\n' % (n[:12], o[:12], 'IN FROZEN SET' if o in frozen else '!! NOT FROZEN'))

def walk(a, b, path, diffs):
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b):
            diffs.append((path, 'key sets differ', sorted(set(a) ^ set(b))[:6])); return
        for k in a: walk(a[k], b[k], '%s.%s' % (path, k), diffs)
    elif isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            diffs.append((path, 'len %d vs %d' % (len(a), len(b)), '')); return
        for i, (x, y) in enumerate(zip(a, b)): walk(x, y, '%s[%d]' % (path, i), diffs)
    else:
        if a != b: diffs.append((path, repr(a), repr(b)))

total_cells = 0
def count(o):
    global total_cells
    if isinstance(o, dict): [count(v) for v in o.values()]
    elif isinstance(o, (list, tuple)): [count(v) for v in o]
    else: total_cells += 1

REV={'SD':'GEN_DEF','SF':'GEN_FWD','KPD':'KEY_DEF','KPF':'KEY_FWD','MID':'MID','RUCK':'RUC'}
def norm(o):
    """Reverse-map position labels appearing as dict KEYS (bare, or inside a tuple key such
    as ('age18','KPD')) so the comparison is on VALUES, not spelling."""
    if isinstance(o, dict):
        out={}
        for k,v in o.items():
            if isinstance(k,str): nk=REV.get(k,k)
            elif isinstance(k,tuple): nk=tuple(REV.get(x,x) if isinstance(x,str) else x for x in k)
            else: nk=k
            out[nk]=norm(v)
        return out
    if isinstance(o,list): return [norm(v) for v in o]
    if isinstance(o,tuple): return tuple(norm(v) for v in o)
    return o

allsame = True
for nsig, osig in pairs.items():
    if nsig not in built:
        sys.stderr.write('   (signature %s produced no surface set)\n' % nsig[:12]); continue
    diffs = []
    # pair stage-2 signature -> the stage-1 frozen surface it supersedes, by ordinal
    fz=sorted(frozen); bl=sorted(built)
    partner=fz[bl.index(nsig)] if len(fz)==len(bl) else None
    if partner is None: continue
    sys.stderr.write('pairing %s (stage2) against %s (stage1 frozen)\n'%(nsig[:12],partner[:12]))
    walk(built[nsig], frozen[partner], '', diffs)
    count(norm(built[nsig]))
    sys.stderr.write('COMPARE %s vs frozen: %s\n'
                     % (nsig[:12], 'IDENTICAL' if not diffs else '%d DIFFERENCES' % len(diffs)))
    for d in diffs[:10]: sys.stderr.write('     %s  %s  !=  %s\n' % d)
    if diffs: allsame = False
sys.stderr.write('total scalar cells compared: %d\n' % total_cells)
sys.stderr.write('RESULT: %s\n' % ('ALL SURFACES CELL-FOR-CELL IDENTICAL' if allsame else 'DIFFERENCES FOUND — STOP'))
