#!/usr/bin/env python3
"""Instrument EVERY sklearn .fit / .fit_transform during a full engine load, capturing the
call-site (file:line), the estimator, and input shape. Enumerates the runtime-fit census (P2)."""
import os, sys, io, contextlib, traceback, json, collections
WS = os.environ.get('RL_WS', '/home/claude/rl_workspace/rl_after')
sys.path.insert(0, WS); sys.path.insert(0, '/home/claude/rl_vendor')
os.chdir(WS)

records = []
def _caller():
    # the exec'd engine is '<string>' frames whose linenos == _merged_recover.py line numbers.
    # Return the nearest engine frame AND the name of the enclosing engine function.
    frames = traceback.extract_stack()[:-2]
    eng_frames = [fr for fr in frames if (fr.filename == '<string>' or 'rl_after' in fr.filename or 'forward_valuation' in fr.filename)
                  and fr.name not in ('_wrap','_patched_fit','_patched_ft')]
    if not eng_frames:
        fr = frames[-1]; return f"{os.path.basename(fr.filename)}:{fr.lineno}", fr.name, fr.line
    innermost = eng_frames[-1]      # where the fit is literally called (e.g. _iso_dec)
    # find nearest DISTINCT enclosing caller for context
    caller = None
    for fr in reversed(eng_frames[:-1]):
        if fr.name != innermost.name:
            caller = fr; break
    site = f"_merged_recover.py:{innermost.lineno}" if innermost.filename == '<string>' else f"{os.path.basename(innermost.filename)}:{innermost.lineno}"
    ctx = f"{innermost.name} <- {caller.name}:{caller.lineno}" if caller else innermost.name
    return site, ctx, (innermost.line or '')

import sklearn.isotonic as _iso
import sklearn.ensemble as _ens
_orig_iso_fit = _iso.IsotonicRegression.fit
_orig_iso_ft  = _iso.IsotonicRegression.fit_transform
def _patched_fit(self, X, y=None, **kw):
    site, ctx, src = _caller()
    n = len(X) if hasattr(X,'__len__') else '?'
    records.append(('IsotonicRegression.fit', site, ctx, n,
                    dict(increasing=getattr(self,'increasing',None), oob=getattr(self,'out_of_bounds',None))))
    return _orig_iso_fit(self, X, y, **kw)
def _patched_ft(self, X, y=None, **kw):
    site, ctx, src = _caller()
    n = len(X) if hasattr(X,'__len__') else '?'
    records.append(('IsotonicRegression.fit_transform', site, ctx, n,
                    dict(increasing=getattr(self,'increasing',None))))
    return _orig_iso_ft(self, X, y, **kw)
_iso.IsotonicRegression.fit = _patched_fit
_iso.IsotonicRegression.fit_transform = _patched_ft

# also catch GBR / RF fits (should be ZERO now — q97m + cm are loaded, not fitted)
for _cls in ('GradientBoostingRegressor','RandomForestRegressor','GradientBoostingClassifier','RandomForestClassifier'):
    _k = getattr(_ens, _cls, None)
    if _k is None: continue
    _of = _k.fit
    def _mk(orig, name):
        def _w(self, X, y=None, **kw):
            site, src = _caller()
            n = len(X) if hasattr(X,'__len__') else '?'
            records.append((name+'.fit', site, src.strip() if src else '', n, {}))
            return orig(self, X, y, **kw)
        return _w
    setattr(_k, 'fit', _mk(_of, _cls))

# load the engine exactly as a build does (exec up to the AFTER banner)
eng = os.path.join(WS, '_merged_recover.py')
g = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(eng).read().split('print("=== AFTER')[0], g)

# report
print("TOTAL runtime .fit/.fit_transform calls during engine load:", len(records))
bykind = collections.Counter(r[0] for r in records)
print("by estimator:", dict(bykind))
bysite = collections.Counter(r[1] for r in records)
print("\nBY CALL SITE (site : count : source):")
for site, c in sorted(bysite.items(), key=lambda kv:(-kv[1], kv[0])):
    ex = next(r for r in records if r[1]==site)
    print(f"  {site:28s} x{c:3d}  {ex[2][:80]}")
# dump full records for the table
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else '.', 'fit_census_raw.json'),'w') as f:
    json.dump([{'kind':r[0],'site':r[1],'src':r[2],'n_in':r[3],'params':r[4]} for r in records], f, indent=1)
print("\nwrote fit_census_raw.json")
