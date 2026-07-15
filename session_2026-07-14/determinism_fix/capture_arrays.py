#!/usr/bin/env python3
"""Capture the actual (a,b) operands hitting np.dot at each of the 3 sites (206, 910, 926),
plus the operands of the numpy reductions w.sum() / np.sum(w*w) in the NW smoother, so each
can be replayed in isolation under different kernels. Run NATIVE (operands are the same object
identities regardless of kernel; we only need one capture)."""
import os, sys, io, contextlib, pickle
WS='/home/claude/rl_workspace/rl_after'
sys.path.insert(0,WS); sys.path.insert(0,'/home/claude/rl_vendor'); os.chdir(WS)
import numpy as np, traceback
cap={'206':[], '910':[], '926':[]}
def site():
    for fr in reversed(traceback.extract_stack()[:-2]):
        if fr.filename=='<string>': return str(fr.lineno)
    return '?'
_od=np.dot
def w(a,b,*r,**k):
    res=_od(a,b,*r,**k); s=site()
    if s in cap and len(cap[s])<40:
        cap[s].append((np.ascontiguousarray(np.asarray(a,dtype=np.float64)).copy(),
                        np.ascontiguousarray(np.asarray(b,dtype=np.float64)).copy()))
    return res
np.dot=w
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
# a few player ev() to exercise 206 on real players too
MA=g['MA']; ev=g['ev']
with contextlib.redirect_stdout(io.StringIO()):
    for p in MA.players[:60]: ev(p,2026)
with open('/tmp/dot_operands.pkl','wb') as f:
    pickle.dump({k:v for k,v in cap.items()}, f)
print("captured operand sets:", {k:len(v) for k,v in cap.items()})
for k,v in cap.items():
    if v:
        a,b=v[0]; print("  site %s: first operand shapes a=%s b=%s"%(k,a.shape,b.shape))
