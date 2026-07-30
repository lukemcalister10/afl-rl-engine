"""ITEM 271 STAGE A, Q-E instrument — READ-ONLY diagnostic.

Reverses the 62 deferred edits at PAYLOAD level: each edited player's label is put back to
his pre-edit `gfut` at the exact point it enters the v0surf fingerprint, the signature is
recomputed, and it must reproduce the landed frozen signature EXACTLY. If anything other
than those labels moved -- the pick curve, the gate set, roster membership, an age or a pick
-- the equality fails, which is what makes this check non-vacuous.

Writes NO artifact: it raises SystemExit inside _v0surf_sig, before the surface is consulted
or any board is produced. The signature function in the repo is NOT modified -- the patch
lives only in this process's in-memory copy of the source.

Run from the workspace rl_after with RL_REPO set:
    RL_V0SURF_REFIT=1 python3 <repo>/session_2026-07-29/item271/v0surf_reverse_map_stageA.py
"""
import sys, os, io, json, contextlib
import config_manifest
config_manifest.enforce()

OLD_GFUT = json.load(open(os.environ['RL_OLD_GFUT']))
EXPECT   = os.environ['RL_EXPECT_SIG']

src = open('_merged_recover.py').read().split('print("=== AFTER')[0]

ANCHOR = """def _v0surf_sig(real):"""
if src.count(ANCHOR) != 1:
    raise SystemExit('HALT: expected exactly 1 _v0surf_sig definition, found %d' % src.count(ANCHOR))

INJECT = '''
import json as _json0, os as _os0
_OLDG=_json0.load(open(_os0.environ['RL_OLD_GFUT']))
_EXPECT=_os0.environ['RL_EXPECT_SIG']
def _v0surf_sig(real):
    import hashlib as _hl, json as _js, sys as _sys
    _curve=_PVC0 if '_PVC0' in globals() else MA.PVC
    def _mk(lab):
        return {'pvc':sorted((int(k),int(v)) for k,v in _curve.items()),
                'roster':sorted([lab(p),_ageR(p),int(p.get('pick'))] for p in real),
                'gates':{g:_os0.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    def _h(pl): return _hl.md5(_js.dumps(pl,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    def _rev(p):
        k=p.get('key')
        return _OLDG.get(k, str(MA.gfut(p))) if k in _OLDG else str(MA.gfut(p))
    _new=_mk(lambda p: str(MA.gfut(p)))
    _old=_mk(_rev)
    w=_sys.stderr.write
    # who in the fingerprint sample actually moved
    _movers=[p for p in real if p.get('key') in _OLDG and _OLDG[p['key']]!=str(MA.gfut(p))]
    w('DIAG roster rows (denominator)   : %d\\n'%len(_new['roster']))
    w('DIAG edited players IN sample    : %d\\n'%sum(1 for p in real if p.get('key') in _EDITED))
    w('DIAG label movers IN sample      : %d\\n'%len(_movers))
    for _p in sorted(_movers,key=lambda q:q.get('key') or ''):
        w('     %-24s %s -> %s  (pick %s)\\n'%(_p.get('key'),_OLDG[_p['key']],str(MA.gfut(_p)),int(_p.get('pick'))))
    w('DIAG pvc entries                 : %d\\n'%len(_new['pvc']))
    w('DIAG gates                       : %d\\n'%len(_new['gates']))
    # the two payloads must differ ONLY in the label field
    _sn=[[_OLDG.get(r[0],r[0])]+r[1:] for r in _new['roster']]
    w('DIAG signature (with the 62)     : %s\\n'%_h(_new))
    w('DIAG signature (62 reversed)     : %s\\n'%_h(_old))
    w('DIAG expected prior signature    : %s\\n'%_EXPECT)
    w('DIAG REVERSED REPRODUCES PRIOR   : %s\\n'%(_h(_old)==_EXPECT))
    w('DIAG reversed IS in frozen set   : %s\\n'%(_h(_old) in (_V0SURF if isinstance(_V0SURF,dict) else {})))
    w('DIAG new sig IS in frozen set    : %s\\n'%(_h(_new) in (_V0SURF if isinstance(_V0SURF,dict) else {})))
    raise SystemExit('DIAGNOSTIC COMPLETE - no artifact written')
'''

src = src.replace(ANCHOR, INJECT + '\ndef _UNUSED_orig_v0surf_sig(real):', 1)

g = {'__name__': '__main__', '_EDITED': set(OLD_GFUT)}
# _EDITED must be visible inside the exec'd module namespace
src = "_EDITED=set(__import__('json').load(open(__import__('os').environ['RL_EDITED_KEYS'])))\n" + src
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, g)
except SystemExit as e:
    sys.stderr.write('exit: %s\n' % e)
