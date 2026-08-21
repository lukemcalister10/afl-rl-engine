"""RATCHET COST AND MINT, OUT OF SAMPLE. 10_ratchet_and_coverage.py measured the ratchet on a
FULL-DATA fit, so its absolute pinball is in-sample. Here the surface is refitted on fold-3's
TRAINING careers only (debut <= 2018) and the ratchet is measured on the HELD-OUT careers
(debut 2019-2021), which is the honest version of the same number."""
import json, os, time, collections
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
S=os.environ['STUDY']; OUT=os.path.join(S,'out')
Q6=[0.10,0.30,0.50,0.70,0.90,0.97]; WQ6=np.array([0.18]*5+[0.10]); WQ6/=WQ6.sum(); LVL=9
NT={0.10:400,0.30:400,0.50:400,0.70:400,0.90:400,0.97:200}
d=np.load(os.path.join(OUT,'design.npz'),allow_pickle=True)
X=d['X'].astype(float); y=d['y'].astype(float); ispool=d['ispool'].astype(bool); debut=d['debut'].astype(int)
tr=debut<=2018; te=(debut>=2019)&(debut<=2021); idx=np.where(te)[0]
def mono(nf): c=[0]*nf; c[LVL]=1; return c
def guarded(B):
    P=np.sort(B[:,:5],axis=1); return np.column_stack([P,np.maximum(B[:,5],P[:,4])])
def pinball(yt,qh,q):
    e=yt-qh; return float(np.mean(np.maximum(q*e,(q-1)*e)))
res={}
for nm,mk in (('a_status_quo',lambda q: GradientBoostingRegressor(loss='quantile',alpha=q,n_estimators=NT[q],max_depth=4,learning_rate=0.05,min_samples_leaf=25,random_state=0)),
              ('b_mono',lambda q: HistGradientBoostingRegressor(loss='quantile',quantile=q,max_iter=NT[q],max_depth=4,learning_rate=0.05,min_samples_leaf=25,random_state=0,early_stopping=False,monotonic_cst=mono(X.shape[1])))):
    t0=time.time(); M={q:mk(q).fit(X[tr],y[tr]) for q in Q6}
    def pred(F): return np.column_stack([M[q].predict(F) for q in Q6])
    raw=guarded(pred(X[idx]))
    kn=set()
    for q in Q6:
        m=M[q]
        if hasattr(m,'_bin_mapper'): kn.update(float(x)+1e-9 for x in np.asarray(m._bin_mapper.bin_thresholds_[LVL]))
        else:
            for e in np.asarray(m.estimators_).ravel():
                t=e.tree_; kn.update(float(v)+1e-9 for v in t.threshold[t.feature==LVL])
    kn=np.array(sorted(x for x in kn if 40.0<=x<=120.0)); kn=np.concatenate([[40.0],kn,[120.0]])
    out=np.zeros_like(raw)
    for r,i in enumerate(idx):
        f=X[i]; sel=kn[kn<=float(f[LVL])]
        if sel.size==0: out[r]=raw[r]; continue
        G=np.repeat(f[None,:],sel.size,axis=0); G[:,LVL]=sel
        out[r]=np.maximum.accumulate(guarded(pred(G)),axis=0)[-1]
    pr=float(np.mean([pinball(y[idx],raw[:,j],q) for j,q in enumerate(Q6)]))
    pt=float(np.mean([pinball(y[idx],out[:,j],q) for j,q in enumerate(Q6)]))
    mr=float(np.mean(raw@WQ6)); mt=float(np.mean(out@WQ6))
    mv=int((np.abs(out-raw).max(axis=1)>1e-9).sum())
    # per-population mint
    cls=d['cls'].astype(str)[idx]; bym={}
    for c in sorted(set(cls)):
        s=cls==c
        if s.sum()<25: continue
        bym[c]=round(100*float((np.mean(out[s]@WQ6)-np.mean(raw[s]@WQ6))/np.mean(raw[s]@WQ6)),4)
    res[nm]=dict(pinball_raw=round(pr,5),pinball_ratchet=round(pt,5),
                 cost_pct=round(100*(pt-pr)/pr,3), mean_band_raw=round(mr,4),
                 mean_band_ratchet=round(mt,4), mint_pct=round(100*(mt-mr)/mr,4),
                 rows_moved=mv, rows_moved_pct=round(100.0*mv/len(idx),2),
                 mint_by_population_pct=bym, n_knots=len(kn), fit_s=round(time.time()-t0,1))
    print('%-14s OOS pinball %.4f -> %.4f (%+.3f%%)   band mean %.3f -> %.3f  MINT %+.4f%%   %d/%d rows moved'
          %(nm,pr,pt,res[nm]['cost_pct'],mr,mt,res[nm]['mint_pct'],mv,len(idx)),flush=True)
    print('    mint by population:',bym,flush=True)
json.dump(res,open(os.path.join(OUT,'ratchet_oos.json'),'w'),indent=1)
print('wrote out/ratchet_oos.json')
