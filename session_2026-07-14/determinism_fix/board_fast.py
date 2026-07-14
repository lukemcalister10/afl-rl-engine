#!/usr/bin/env python3
"""FAST 2026-only board under a summation-order regime. Same modes as board_variants.
Board value = round(ev(p,2026)/F). Representative for the order-sensitivity comparison."""
import os, sys, io, contextlib, math
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
MODE=sys.argv[1]; OUT=sys.argv[2]
import numpy as np
import sklearn, sklearn.isotonic, sklearn.ensemble  # noqa
try:
    import scipy.stats  # noqa
except Exception: pass
_odot=np.dot; _osum=np.sum; _omean=np.mean; _oavg=np.average
def _is1df(a):
    try:
        aa=np.asarray(a); return aa.ndim==1 and aa.dtype.kind=='f' and aa.size>=2
    except Exception: return False
if MODE=='rev_dot':
    def wd(a,b,*r,**k):
        if _is1df(a) and _is1df(b) and np.asarray(a).shape==np.asarray(b).shape:
            return _odot(np.asarray(a)[::-1],np.asarray(b)[::-1],*r,**k)
        return _odot(a,b,*r,**k)
    np.dot=wd
elif MODE=='rev_sums':
    np.sum   =lambda a,*r,**k:(_osum(np.asarray(a)[::-1],*r,**k)  if (not r and not k.get('axis') and _is1df(a)) else _osum(a,*r,**k))
    np.mean  =lambda a,*r,**k:(_omean(np.asarray(a)[::-1],*r,**k) if (not r and not k.get('axis') and _is1df(a)) else _omean(a,*r,**k))
    np.average=lambda a,*r,**k:(_oavg(np.asarray(a)[::-1],*r,**k) if (not r and not k.get('axis') and _is1df(a)) else _oavg(a,*r,**k))
elif MODE=='rev_both':
    def wd(a,b,*r,**k):
        if _is1df(a) and _is1df(b) and np.asarray(a).shape==np.asarray(b).shape:
            return _odot(np.asarray(a)[::-1],np.asarray(b)[::-1],*r,**k)
        return _odot(a,b,*r,**k)
    np.dot=wd
    np.sum   =lambda a,*r,**k:(_osum(np.asarray(a)[::-1],*r,**k)  if (not r and not k.get('axis') and _is1df(a)) else _osum(a,*r,**k))
    np.mean  =lambda a,*r,**k:(_omean(np.asarray(a)[::-1],*r,**k) if (not r and not k.get('axis') and _is1df(a)) else _omean(a,*r,**k))
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; F=1.0524
with open(OUT,'w') as f, contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        f.write("%s\t%d\n"%(p['key'], int(round(ev(p,2026)/F))))
sys.stderr.write("mode=%s done\n"%MODE)
