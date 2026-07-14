# R2 — SMOOTH CURVE IN AGE (CORE rule 7). Replace the 3 rigid bins with a local-linear kernel
# smoother of the return-from-absence effect against age_pre, evaluated 18..34 with a bootstrap
# ribbon. Test for the U-shape. Uses the MEAN-REVERSION-ADJUSTED effect (age+level matched, R1[G])
# as primary, with the age-only effect shown alongside for continuity with the prior D2.
# Board of record: store b0c39d78.
import d2common as D, numpy as np
np.random.seed(0)
ev=D.build_events(); ctrl=D.build_control(); exp=D.make_expected(ctrl)
cl=D.build_control_lvl(); pred=D.fit_ctrl_model(cl)
rows=D.effect_rows(ev,exp,ctrl_predict=pred)
age=np.array([r['age_pre'] for r in rows])
eff_raw=np.array([r['effect'] for r in rows])       # age-only DiD (prior)
eff_adj=np.array([r['effect_adj'] for r in rows])   # age+level matched (mean-reversion netted)
n=len(rows)
GRID=np.arange(18,35)
BW=2.5   # kernel bandwidth in years (declared); n=167 in the young decade supports ~2-3yr resolution

def nw(xq, x, y, bw):
    """local-LINEAR (degree-1) kernel regression at xq; Gaussian kernel, bandwidth bw."""
    w=np.exp(-0.5*((x-xq)/bw)**2)
    sw=w.sum()
    if sw< 3: return np.nan
    # weighted linear fit
    W=np.diag(w); X=np.column_stack([np.ones(len(x)),x-xq])
    try:
        beta=np.linalg.solve(X.T@W@X, X.T@W@y)
        return beta[0]   # intercept = fit at xq
    except np.linalg.LinAlgError:
        return np.sum(w*y)/sw

def curve_ci(x,y,grid,bw,B=2000):
    base=np.array([nw(g,x,y,bw) for g in grid])
    boots=np.empty((B,len(grid)))
    for b in range(B):
        s=np.random.randint(0,len(x),len(x))
        boots[b]=[nw(g,x[s],y[s],bw) for g in grid]
    lo=np.nanpercentile(boots,2.5,axis=0); hi=np.nanpercentile(boots,97.5,axis=0)
    return base,lo,hi

print(f"=== R2 · smooth age curve · n={n} returner events · board b0c39d78 ===")
print(f"kernel: Gaussian local-linear, bandwidth {BW}y (declared). Grid 18..34.\n")
# effective sample support at each grid age (sum of kernel weights ~ effective n)
def eff_n(g): return float(np.exp(-0.5*((age-g)/BW)**2).sum())

for label,y in [('AGE-ONLY DiD (prior D2 construction)',eff_raw),
                ('MEAN-REVERSION-ADJUSTED (age+level matched)',eff_adj)]:
    base,lo,hi=curve_ci(age,y,GRID,BW)
    print(f"--- {label} ---")
    print(f"  age :  effect  [ 95% ribbon ]   eff_n")
    for i,g in enumerate(GRID):
        en=eff_n(g)
        flag=''
        if en<8: flag=' (thin — pooled/deweighted)'
        print(f"   {g:2d} : {base[i]:+6.2f}  [{lo[i]:+6.2f},{hi[i]:+6.2f}]  {en:5.1f}{flag}")
    # U-shape test: is there an interior minimum (prime) with young & old both more negative?
    valid=~np.isnan(base)
    gmin=GRID[valid][np.argmin(base[valid])]
    print(f"  minimum (least penalty) at age {gmin};  young(≤22) mean {np.nanmean(base[GRID<=22]):+.2f}"
          f"  prime(25-28) {np.nanmean(base[(GRID>=25)&(GRID<=28)]):+.2f}  old(≥30) {np.nanmean(base[GRID>=30]):+.2f}")
    print()

# raw scatter counts per integer age (honesty: where the data actually is)
print("raw n at each integer age_pre (support):")
u,c=np.unique(np.round(age).astype(int),return_counts=True)
print("  "+"  ".join(f"{a}:{ct}" for a,ct in zip(u,c)))
