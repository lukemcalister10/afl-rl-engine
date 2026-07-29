"""ITEM 262 R2-3 — READ-ONLY diagnostic. Reverse-maps the new position labels back to the
old spelling at the point they enter the v0surf fingerprint, recomputes, and compares to the
frozen set. Writes NO artifact: it raises SystemExit inside _v0surf_sig, before the surface
is consulted or any board is produced. The signature function in the repo is NOT modified —
the patch lives only in this process's in-memory copy of the source."""
import sys, os, io, contextlib, re
import config_manifest
config_manifest.enforce()

src = open('_merged_recover.py').read()
src = src.split('print("=== AFTER')[0]

ANCHOR = """def _v0surf_sig(real):"""
if src.count(ANCHOR) != 1:
    raise SystemExit('HALT: expected exactly 1 _v0surf_sig definition, found %d' % src.count(ANCHOR))

INJECT = '''
_REV={'SD':'GEN_DEF','SF':'GEN_FWD','KPD':'KEY_DEF','KPF':'KEY_FWD','MID':'MID','RUCK':'RUC'}
def _v0surf_sig(real):
    import hashlib as _hl, json as _js, sys as _sys
    _curve=_PVC0 if '_PVC0' in globals() else MA.PVC
    def _mk(lab):
        return {'pvc':sorted((int(k),int(v)) for k,v in _curve.items()),
                'roster':sorted([lab(p),_ageR(p),int(p.get('pick'))] for p in real),
                'gates':{g:os.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    def _h(pl): return _hl.md5(_js.dumps(pl,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    _new=_mk(lambda p: str(MA.gfut(p)))
    _old=_mk(lambda p: _REV.get(str(MA.gfut(p)),str(MA.gfut(p))))
    w=_sys.stderr.write
    w('DIAG roster rows            : %d\\n'%len(_new['roster']))
    w('DIAG pvc entries            : %d\\n'%len(_new['pvc']))
    w('DIAG gates                  : %d\\n'%len(_new['gates']))
    w('DIAG labels seen (new)      : %s\\n'%sorted({r[0] for r in _new['roster']}))
    w('DIAG labels seen (reversed) : %s\\n'%sorted({r[0] for r in _old['roster']}))
    # the two payloads must differ ONLY in the label field
    _sn=[[_REV.get(r[0],r[0])]+r[1:] for r in _new['roster']]
    w('DIAG roster identical after reverse-map: %s\\n'%(sorted(_sn)==sorted(_old['roster'])))
    w('DIAG pvc identical  : %s\\n'%(_new['pvc']==_old['pvc']))
    w('DIAG gates identical: %s\\n'%(_new['gates']==_old['gates']))
    w('DIAG signature (new vocabulary)  : %s\\n'%_h(_new))
    w('DIAG signature (reverse-mapped)  : %s\\n'%_h(_old))
    w('DIAG frozen set                  : %s\\n'%(sorted(_V0SURF.keys()) if isinstance(_V0SURF,dict) else repr(_V0SURF)))
    w('DIAG reverse-mapped IS frozen    : %s\\n'%(_h(_old) in (_V0SURF if isinstance(_V0SURF,dict) else {})))
    raise SystemExit('DIAGNOSTIC COMPLETE - no artifact written')
'''
src = src.replace(ANCHOR, INJECT + '\ndef _UNUSED_orig_v0surf_sig(real):', 1)

g = {'__name__': '__main__'}
try:
    with contextlib.redirect_stdout(io.StringIO()):
        exec(src, g)
except SystemExit as e:
    sys.stderr.write('exit: %s\n' % e)
