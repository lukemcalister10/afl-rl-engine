#!/usr/bin/env python3
"""Decisive not-localised test. Build the board (round(ev/F) for all players) under different
summation-ORDER regimes, holding CPU/kernel fixed. A different valid order (reversed) is exactly
what a different SIMD width (AVX512 vs AVX2) produces. Modes:
  native     : numpy default everywhere (== e6a8e6ef)
  rev_sums   : np.dot NATIVE, but np.sum/np.mean/np.average/np.std computed on REVERSED input
               (isolates the numpy-reduction-order contribution, np.dot held constant)
  rev_dot    : only np.dot on reversed input (isolates the np.dot contribution)
  fsum_all   : np.dot + np.sum + np.mean + np.average -> correctly-rounded fsum (order-independent)
Usage: python3 board_variants.py <mode> <outfile>"""
import os, sys, io, contextlib, math, struct
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
MODE=sys.argv[1]; OUT=sys.argv[2]
import numpy as np
# Pre-import the heavy libs (sklearn/scipy) BEFORE patching so import-time internals are untouched;
# the patch then only affects the engine's RUNTIME reductions.
import sklearn, sklearn.isotonic, sklearn.ensemble  # noqa
try:
    import scipy.stats  # noqa
except Exception: pass
_odot=np.dot; _osum=np.sum; _omean=np.mean; _oavg=np.average; _ostd=np.std
def _is1df(a):
    try:
        aa=np.asarray(a)
        return aa.ndim==1 and aa.dtype.kind=='f'
    except Exception: return False
def _rev(a):
    try: return np.asarray(a)[::-1]
    except Exception: return a
if MODE=='rev_sums':
    np.sum   =lambda a,*r,**k:(_osum(np.asarray(a)[::-1],*r,**k)  if (not r and not k.get('axis') and _is1df(a)) else _osum(a,*r,**k))
    np.mean  =lambda a,*r,**k:(_omean(np.asarray(a)[::-1],*r,**k) if (not r and not k.get('axis') and _is1df(a)) else _omean(a,*r,**k))
    np.average=lambda a,*r,**k:(_oavg(np.asarray(a)[::-1],*r,**k) if (not r and not k.get('axis') and _is1df(a)) else _oavg(a,*r,**k))
elif MODE=='rev_dot':
    def wd(a,b,*r,**k):
        try:
            aa=np.asarray(a); bb=np.asarray(b)
            if aa.ndim==1 and bb.ndim==1 and aa.shape==bb.shape:
                return _odot(aa[::-1],bb[::-1],*r,**k)
        except Exception: pass
        return _odot(a,b,*r,**k)
    np.dot=wd
elif MODE=='fsum_all':
    def fd(a,b,*r,**k):
        try:
            aa=np.asarray(a,dtype=np.float64).ravel(); bb=np.asarray(b,dtype=np.float64).ravel()
            if aa.shape==bb.shape and aa.ndim==1:
                return math.fsum(float(x)*float(y) for x,y in zip(aa,bb))
        except Exception: pass
        return _odot(a,b,*r,**k)
    def fs(a,*r,**k):
        if not r and not k.get('axis') and _is1df(a):
            try:
                el=np.asarray(a,dtype=np.float64).ravel(); return np.float64(math.fsum(float(x) for x in el))
            except Exception: pass
        return _osum(a,*r,**k)
    def fm(a,*r,**k):
        if not r and not k.get('axis') and _is1df(a):
            try:
                el=np.asarray(a,dtype=np.float64).ravel()
                if len(el): return np.float64(math.fsum(float(x) for x in el)/len(el))
            except Exception: pass
        return _omean(a,*r,**k)
    def fa(a,*r,**k):
        return _oavg(a,*r,**k)
    np.dot=fd; np.sum=fs; np.mean=fm
# build
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; F=1.0524
board={}
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        v=ev(p,2026); ev(p,2024); ev(p,2025); ev(p,2027); ev(p,2028)
        board[p['key']]=int(round(v/F))
with open(OUT,'w') as f:
    for k in sorted(board): f.write("%s\t%d\n"%(k,board[k]))
print("mode=%s wrote %d players"%(MODE,len(board)))
