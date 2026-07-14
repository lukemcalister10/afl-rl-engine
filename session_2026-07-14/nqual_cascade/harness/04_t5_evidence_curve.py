"""T5: MEASURE how well the record predicts future output vs the pedigree, as a function of evidence.
Walk-forward, leak-free. record=_lvlcurr(p,Y) (<=Y only); pedigree=_par_prior(p,Y); future=realised avg over Y+1..Y+3.
Evidence axis = nqual(p,Y) and games-so-far. Cluster-bootstrap over players. READ-ONLY. store b0c39d78/board 81e48293."""
import io,contextlib,json,numpy as np
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; PROVEN_N=g['PROVEN_N']
_nqual=g['_nqual']; _lvlcurr=g['_lvlcurr']; _par_prior=g['_par_prior']
rng=np.random.default_rng(0)
FWD_LO,FWD_HI=1,3            # forward window Y+1..Y+3
DATA_CAP=2025               # last fully-resolved season (2026 in-progress -> excluded from forward)
YMIN=2010                  # as-of years to sweep
pool=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
def games_through(p,Y): return sum(x['games'] for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y)
def fwd_real(p,Y):
    qs=[x['avg'] for x in p['scoring'] if x['games']>=6 and Y+FWD_LO<=x['year']<=min(Y+FWD_HI,DATA_CAP)]
    return float(np.mean(qs)) if qs else None    # None => no qualifying forward season (bust/left) -> excluded from prediction fit
rows=[]
for p in pool:
    d=cp.debutyr(p)
    for Y in range(max(YMIN,d),DATA_CAP-FWD_LO+1):     # need at least Y+1<=2025
        R=_lvlcurr(p,Y)
        if R<=0: continue                              # hasn't produced yet -> record undefined
        if games_through(p,Y)<=0: continue
        Fo=fwd_real(p,Y)
        if Fo is None: continue
        n=_nqual(p,Y)
        rows.append((p['key'],n,games_through(p,Y),R,_par_prior(p,Y),Fo))
rows=np.array([(r[1],r[2],r[3],r[4],r[5]) for r in rows],dtype=float)
keys=[r[0] for r in [(x[0],) for x in [(rr,) for rr in []]]]  # placeholder
keys=[r for r in []]
# rebuild keys list properly
keys=[]; data=[]
for p in pool:
    d=cp.debutyr(p)
    for Y in range(max(YMIN,d),DATA_CAP-FWD_LO+1):
        R=_lvlcurr(p,Y)
        if R<=0 or games_through(p,Y)<=0: continue
        Fo=fwd_real(p,Y)
        if Fo is None: continue
        keys.append(p['key']); data.append((_nqual(p,Y),games_through(p,Y),R,_par_prior(p,Y),Fo))
D=np.array(data,float); K=np.array(keys)
n_arr,gm_arr,R_arr,P_arr,F_arr=D[:,0],D[:,1],D[:,2],D[:,3],D[:,4]
print('rows=%d  players=%d  as-of years %d..%d  fwd=+%d..+%d'%(len(D),len(set(keys)),YMIN,DATA_CAP-FWD_LO,FWD_LO,FWD_HI))

def wstar(R,P,F):
    """optimal record weight w in F ~ w*R+(1-w)*P  (closed form, unclipped then report)."""
    x=R-P; y=F-P; d=np.dot(x,x)
    return float(np.dot(x,y)/d) if d>1e-9 else np.nan
def corr(a,b):
    if len(a)<3 or np.std(a)<1e-9 or np.std(b)<1e-9: return np.nan
    return float(np.corrcoef(a,b)[0,1])
def rmse(pred,F): return float(np.sqrt(np.mean((pred-F)**2)))

# cluster bootstrap over players
uniq=np.array(sorted(set(keys)))
key2idx={}
for i,k in enumerate(keys): key2idx.setdefault(k,[]).append(i)
def boot_w(mask,B=400):
    idx_all=np.where(mask)[0]
    ks=np.array(sorted(set(K[idx_all])))
    ws=[]
    for _ in range(B):
        samp=rng.choice(ks,size=len(ks),replace=True)
        ii=np.concatenate([[i for i in key2idx[k] if mask[i]] for k in samp]) if len(ks) else np.array([],int)
        if len(ii)<8: ws.append(np.nan); continue
        ws.append(wstar(R_arr[ii],P_arr[ii],F_arr[ii]))
    ws=np.array([w for w in ws if not np.isnan(w)])
    return (np.nanpercentile(ws,2.5),np.nanpercentile(ws,97.5)) if len(ws)>20 else (np.nan,np.nan)

print('\n=== EVIDENCE AXIS = nqual (seasons with >=10 games) ===')
print('%3s %6s %6s | %7s %7s | %7s %8s %8s | %s'%('n','rows','plyrs','corrR','corrP','w*_rec','engine_c','ped_wt*','ped_wt* 95%CI'))
for nb in [0,1,2,3,4,5,'6+']:
    if nb=='6+': m=n_arr>=6
    else: m=n_arr==nb
    if m.sum()<8:
        print('%3s %6d  (thin)'%(str(nb),m.sum())); continue
    R,P,F=R_arr[m],P_arr[m],F_arr[m]
    w=wstar(R,P,F); cR=corr(R,F); cP=corr(P,F)
    lo,hi=boot_w(m)
    ec = (nb/PROVEN_N if isinstance(nb,int) and nb<PROVEN_N else (0.0 if nb==0 else 1.0)) if isinstance(nb,int) else 1.0
    # engine record weight: n==0 -> uses Lo(no par blend, treat rec wt ~ 1 effectively? mark NA); 1..3 -> n/4; >=4 -> 1.0
    ecs = 'NA(Lo)' if nb==0 else ('%.2f'%(nb/PROVEN_N) if (isinstance(nb,int) and nb<4) else '1.00')
    print('%3s %6d %6d | %+6.3f %+6.3f | %6.3f  %6s  %6.3f  [%+.2f,%+.2f]'%(
        str(nb),m.sum(),len(set(K[m])),cR,cP,w,ecs,1-w,1-hi,1-lo))

print('\n=== EVIDENCE AXIS = games-so-far (R98.4: games decide trust) ===')
print('%10s %6s | %6s %6s | %6s %8s'%('games','rows','corrR','corrP','w*_rec','ped_wt*'))
bins=[(1,20),(21,40),(41,70),(71,110),(111,160),(161,9999)]
for a,b in bins:
    m=(gm_arr>=a)&(gm_arr<=b)
    if m.sum()<8: print('%10s %6d (thin)'%('%d-%d'%(a,b),m.sum())); continue
    R,P,F=R_arr[m],P_arr[m],F_arr[m]
    print('%10s %6d | %+5.3f %+5.3f | %5.3f   %5.3f'%('%d-%d'%(a,b),m.sum(),corr(R,F),corr(P,F),wstar(R,P,F),1-wstar(R,P,F)))

print('\n=== record-only vs pedigree-only vs blend RMSE (all rows) ===')
print('pedigree-only RMSE=%.2f  record-only RMSE=%.2f  best-static-blend RMSE=%.2f (w*=%.3f)'%(
    rmse(P_arr,F_arr),rmse(R_arr,F_arr),rmse(wstar(R_arr,P_arr,F_arr)*R_arr+(1-wstar(R_arr,P_arr,F_arr))*P_arr,F_arr),wstar(R_arr,P_arr,F_arr)))
# crossover: smallest n where corrR>corrP and where w*>0.5
print('\n=== crossovers ===')
for nb in range(0,7):
    m=n_arr==nb if nb<6 else n_arr>=6
    if m.sum()<8: continue
    R,P,F=R_arr[m],P_arr[m],F_arr[m]
    print('  n=%d: corrR=%.3f corrP=%.3f record_wins=%s ; w*=%.3f record_dominant(>0.5)=%s'%(
        nb,corr(R,F),corr(P,F),corr(R,F)>corr(P,F),wstar(R,P,F),wstar(R,P,F)>0.5))
