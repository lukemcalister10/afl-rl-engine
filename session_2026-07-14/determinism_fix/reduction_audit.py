#!/usr/bin/env python3
"""Audit EVERY numpy summation-reduction on the board path against a correctly-rounded fsum
reference. A reduction whose numpy result != fsum on real data is ORDER-SENSITIVE -> it is a
potential cross-chip mover (AVX512 vs AVX2). One that always equals fsum is chip-safe.
Tally per call-site (file:line) how many calls are order-sensitive."""
import os, sys, io, contextlib, math, struct, collections, traceback
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
import numpy as np
def bits(x): return struct.pack('>d',float(x)).hex()
def site():
    for fr in reversed(traceback.extract_stack()[:-3]):
        if fr.filename=='<string>': return "_merged_recover.py:%d"%fr.lineno
        b=os.path.basename(fr.filename)
        if b not in ('reduction_audit.py',) and ('rl_after' in fr.filename or 'forward_valuation' in fr.filename):
            return "%s:%d"%(b,fr.lineno)
    return "?"
tot=collections.Counter(); bad=collections.Counter()
def flat(x):
    a=np.asarray(x,dtype=np.float64).ravel()
    return [float(v) for v in a]
def rec_sum(npval, elems):
    s=site(); tot[s]+=1
    if bits(npval)!=bits(math.fsum(elems)): bad[s]+=1
_odot=np.dot; _osum=np.sum; _omean=np.mean; _oavg=np.average
def w_dot(a,b,*r,**k):
    res=_odot(a,b,*r,**k)
    try:
        if np.ndim(res)==0:
            aa=np.asarray(a,dtype=np.float64).ravel(); bb=np.asarray(b,dtype=np.float64).ravel()
            if aa.shape==bb.shape: rec_sum(res,[float(x)*float(y) for x,y in zip(aa,bb)])
    except Exception: pass
    return res
def w_sum(a,*r,**k):
    res=_osum(a,*r,**k)
    try:
        if np.ndim(res)==0: rec_sum(res, flat(a))
    except Exception: pass
    return res
def w_mean(a,*r,**k):
    res=_omean(a,*r,**k)
    try:
        el=flat(a)
        if np.ndim(res)==0 and el: rec_sum(res*len(el), el)   # mean == sum/n; test the sum part
    except Exception: pass
    return res
np.dot=w_dot; np.sum=w_sum; np.mean=w_mean
# also ndarray.sum / .mean (used as w.sum(), vy.mean())
_ndsum=np.ndarray.sum; _ndmean=np.ndarray.mean
# ndarray methods can't be monkeypatched directly; wrap via subclass is heavy. Instead catch the common
# w.sum() by noting numpy routes ndarray.sum through np.add.reduce; we approximate by auditing np.sum only.
# (w.sum() at :906/:921 -> we AUDIT it explicitly below by patching the engine's call is not possible; but
#  np.sum(w*w) IS captured. For w.sum() we rely on the isolate test already done.)

g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players:
        ev(p,2026); ev(p,2024); ev(p,2025); ev(p,2027); ev(p,2028)
print("=== ORDER-SENSITIVE REDUCTIONS ON THE BOARD PATH (numpy result != correctly-rounded fsum) ===")
print("%-40s %10s %14s"%("callsite","calls","order-sensitive"))
for s in sorted(tot, key=lambda z:-bad[z]):
    if tot[s]==0: continue
    flag=" <== ORDER-SENSITIVE" if bad[s]>0 else ""
    print("  %-40s %8d %10d%s"%(s,tot[s],bad[s],flag))
print("\nDISTINCT order-sensitive call-sites:", sum(1 for s in bad if bad[s]>0))
