#!/usr/bin/env python3
"""ORDER 44 — THE INSTRUMENT CHECK, RUN BEFORE THE ENGINE EDIT WAS COMMITTED AND BEFORE ANY BUILD.

Reads the pinned forests directly (cm_400.pkl 34faa865, data/q97m.pkl cfdc7321) and reproduces the
monotoniser's arithmetic standalone. This is the measurement that FALSIFIED the prereg's declared
0.5 level grid (30 negative steps, worst -0.47 on the band's weighted mean) and that establishes the
exact-knot construction is non-decreasing at a resolution 25x finer than one round-23 score point.
No engine load, no build, no write to the repo.
"""
import pickle, numpy as np, sys
cm=pickle.load(open('/home/claude/cm_400.pkl','rb')); q97=pickle.load(open('data/q97m.pkl','rb'))
Q=[0.10,0.30,0.50,0.70,0.90]; LVLI=9; LO,HI,EPS=40.0,120.0,1e-9
ks=set()
for m in [cm[q] for q in Q]+[q97]:
    for e in np.asarray(m.estimators_).ravel():
        t=e.tree_; ks.update(float(v) for v in t.threshold[t.feature==LVLI])
K=np.array(sorted(ks))
XS=np.unique(np.concatenate([[LO],K+EPS,[HI]]))
print('KNOT CENSUS  n=%d  range %.4f..%.4f  min gap %.3e (EPS=%g cannot skip a piece: %s)'
      %(len(K),K[0],K[-1],np.diff(K).min(),EPS,np.diff(K).min()>1e-7))
GRID=np.arange(LO,HI+1e-9,0.5)
def rows6(F):
    P=np.sort(np.column_stack([np.asarray(cm[q].predict(F),float) for q in Q]),axis=1)
    return np.column_stack([P,np.maximum(np.asarray(q97.predict(F),float),P[:,4])])
def mid(x,y):
    n=len(y);mx=[];my=[];i=0
    while i<n:
        j=i
        while j+1<n and y[j+1]==y[i]: j+=1
        mx.append(0.5*(x[i]+x[j])); my.append(float(y[i])); i=j+1
    return mx,my
def band(f,lvl,mode):
    f=f.copy(); f[LVLI]=lvl
    if mode=='raw': return rows6(f[None,:])[0]
    if mode=='grid-ratchet(THE PREREG ERROR)':
        xs=np.append(GRID[GRID<=lvl],lvl)
        F=np.repeat(f[None,:],xs.size,axis=0); F[:,LVLI]=xs
        return np.maximum.accumulate(rows6(F),axis=0)[-1]
    if mode=='ratchet':
        xs=XS[XS<=lvl]
        if xs.size==0: xs=np.array([lvl])
        F=np.repeat(f[None,:],xs.size,axis=0); F[:,LVLI]=xs
        return np.maximum.accumulate(rows6(F),axis=0)[-1]
    F=np.repeat(f[None,:],XS.size,axis=0); F[:,LVLI]=XS
    R=np.maximum.accumulate(rows6(F),axis=0)
    return np.sort(np.array([np.interp(min(max(lvl,LO),HI),*mid(XS,R[:,i])) for i in range(6)],float))
W=np.array([0.18]*5+[0.10]); W/=W.sum()
ROWS=[('MID pick40 age22',0,40.0,10.0,3.0,22.0),('KPD pick8 age21',3,8.0,8.0,2.0,21.0),
      ('SF pick55 age24',2,55.0,14.0,5.0,24.0)]
bad=0
for lab,g,pk,ex,tn,ag in ROWS:
    f=np.zeros(11); f[g]=1.0; f[6]=np.log(pk); f[7]=ex; f[8]=tn; f[10]=ag
    for lo,hi,st in ((44.0,58.0,0.05),(46.0,50.0,0.002)):
        L=np.arange(lo,hi+1e-9,st)
        for mode in ('raw','grid-ratchet(THE PREREG ERROR)','ratchet','smooth'):
            B=np.array([band(f,l,mode) for l in L]); pr=B@W; d=np.diff(pr)
            neg=int((d<-1e-9).sum()); flat=int((np.abs(d)<=1e-12).sum())
            print('%-18s %5.1f-%4.1f@%.3f %-30s legmin %+.6f  proxy min step %+.8f  NEG %3d  FLAT %4d'
                  %(lab,lo,hi,st,mode,np.diff(B,axis=0).min(),d.min(),neg,flat))
            if mode=='ratchet' and neg: bad+=1
            if mode=='smooth' and (neg or flat): bad+=1
print()
print('VERDICT: %s  (variant A must show NEG 0; variant B must show NEG 0 and FLAT 0)'
      %('PASS' if not bad else '*** FAIL: %d ***'%bad))
sys.exit(1 if bad else 0)
