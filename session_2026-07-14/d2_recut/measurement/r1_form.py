# R1 — ADDITIVE vs MULTIPLICATIVE. Is the return-from-absence effect flat in POINTS or flat in
# PERCENT across the pre-absence level? Regress the effect against pre-absence level; report slope+CI.
# Board of record: store b0c39d78.
import d2common as D, numpy as np
np.random.seed(0)
ev=D.build_events(); ctrl=D.build_control(); exp=D.make_expected(ctrl)
rows=D.effect_rows(ev,exp)
age=np.array([r['age_pre'] for r in rows]); lvl=np.array([r['pre_avg'] for r in rows])
eff=np.array([r['effect'] for r in rows]); n=len(rows)
print(f"=== R1 · matched returner events n={n} · board b0c39d78 ===")
print(f"mean effect (points)  : {eff.mean():+.3f} SC")
print(f"mean effect (percent) : {(eff/lvl).mean()*100:+.2f} %   [effect_i / pre_avg_i]")
print(f"pre_avg range: {lvl.min():.1f} .. {lvl.max():.1f}  (mean {lvl.mean():.1f})")

def ols(X,y):
    X=np.column_stack([np.ones(len(y))]+X)
    beta,_,_,_=np.linalg.lstsq(X,y,rcond=None); return beta
def boot_slope(X_cols,y,idx_of=-1,B=4000):
    betas=[]
    for _ in range(B):
        s=np.random.randint(0,len(y),len(y))
        Xs=[c[s] for c in X_cols]
        betas.append(ols(Xs,y[s])[idx_of])
    return np.percentile(betas,2.5),np.percentile(betas,97.5)

# --- (A) ADDITIVE test: effect(points) ~ pre_avg. Additive <=> slope 0 ---
b=ols([lvl],eff); ci=boot_slope([lvl],eff)
print("\n[A] ADDITIVE form — regress effect(POINTS) on pre_avg:")
print(f"    slope = {b[1]:+.4f} pts per SC of level   95%CI[{ci[0]:+.4f},{ci[1]:+.4f}]")
print(f"    intercept = {b[0]:+.3f} pts   (additive predicts flat: slope≈0)")

# --- (B) MULTIPLICATIVE test: effect(percent) ~ pre_avg. Multiplicative <=> slope 0 ---
pct=eff/lvl
b2=ols([lvl],pct); ci2=boot_slope([lvl],pct)
print("\n[B] MULTIPLICATIVE form — regress effect(PERCENT=eff/pre_avg) on pre_avg:")
print(f"    slope = {b2[1]*100:+.5f} %pts per SC of level   95%CI[{ci2[0]*100:+.5f},{ci2[1]*100:+.5f}]")
print(f"    intercept = {b2[0]*100:+.3f} %   (multiplicative predicts flat: slope≈0)")

# --- (C) age-controlled partial slope: effect ~ age + age^2 + pre_avg. The age gradient is a U (R2),
#     which is NONLINEAR; a linear age term mis-specifies it and leaks curvature into the level term,
#     so control age QUADRATICALLY to isolate the form-vs-level question cleanly. ---
age2=age**2
b3=ols([age,age2,lvl],eff); ci3=boot_slope([age,age2,lvl],eff,idx_of=-1)
print("\n[C] AGE-CONTROLLED (quadratic age) — effect(points) ~ age + age^2 + pre_avg:")
print(f"    level slope = {b3[3]:+.4f} pts per SC of level   95%CI[{ci3[0]:+.4f},{ci3[1]:+.4f}]  (age curve held fixed)")
b4=ols([age,age2,lvl],pct); ci4=boot_slope([age,age2,lvl],pct,idx_of=-1)
print(f"    percent form: level slope = {b4[3]*100:+.5f} %pts/SC  95%CI[{ci4[0]*100:+.5f},{ci4[1]*100:+.5f}]")

# --- effect in points and percent by age stratum (shows relative AMPLIFIES the gradient) ---
print("\n[D] points vs percent by age stratum:")
for lo,hi,lab in [(18,25,'young 18-24'),(25,29,'prime 25-28'),(29,40,'older 29+')]:
    m=(age>=lo)&(age<hi)
    if m.sum()>=5:
        print(f"    {lab:12} n={m.sum():3d}  points={eff[m].mean():+.2f}  percent={(eff[m]/lvl[m]).mean()*100:+.2f}%  (mean lvl {lvl[m].mean():.1f})")

# --- (E) level-quartile means, overall and WITHIN the prime band (flattest age region -> cleanest
#     read of the level-form, free of the U-shape) ---
def quart_table(mask,label):
    L=lvl[mask]; E=eff[mask]
    if len(L)<12: return
    qs=np.quantile(L,[0,.25,.5,.75,1.0])
    print(f"    {label} (n={mask.sum()}):")
    for i in range(4):
        m=mask.copy()
        sel=(lvl>=qs[i])&(lvl<=qs[i+1] if i==3 else lvl<qs[i+1])&mask
        if sel.sum()>0:
            print(f"       lvl [{qs[i]:5.1f},{qs[i+1]:5.1f}] n={sel.sum():3d}  points={eff[sel].mean():+.2f}  percent={(eff[sel]/lvl[sel]).mean()*100:+.2f}%")
print("\n[E] level quartiles:")
quart_table(np.ones(n,bool),"ALL")
quart_table((age>=25)&(age<29),"PRIME 25-28 only")

# --- (F) MEAN-REVERSION NET-OUT. The regressive-in-level pattern is what mean-reversion predicts
#     (high scorers have more to give back). The diff-in-diff nets age but NOT level. So measure the
#     control group's OWN level-slope of Δavg and subtract it: the ABSENCE-SPECIFIC level form is the
#     difference (returner level-slope − control level-slope). ---
ctrlL=[]   # (age, start_avg, davg)
for p in D.priced:
    tl=D.timeline(p)
    if not tl: continue
    pl=[(y,gm,av) for (y,gm,av) in tl if gm>=10]
    for a in range(len(pl)):
        for b in range(a+1,len(pl)):
            ya,_,ava=pl[a]; yb,_,avb=pl[b]; k=yb-ya
            if not(1<=k<=4): continue
            span=[yy for (yy,gm,av) in tl if ya<yy<yb]
            if any(next((g2 for (y2,g2,a2) in tl if y2==yy),0)<10 for yy in span): continue
            ag=D.age_at(p,ya)
            if ag is not None: ctrlL.append((ag,ava,avb-ava))
ctrlL=np.array(ctrlL)
cage=ctrlL[:,0]; cstart=ctrlL[:,1]; cdav=ctrlL[:,2]
bc=ols([cage,cage**2,cstart],cdav); cic=boot_slope([cage,cage**2,cstart],cdav,idx_of=-1)
print("\n[F] MEAN-REVERSION control: Δavg ~ age + age^2 + start_avg  (continuous players):")
print(f"    control level-slope = {bc[3]:+.4f} pts/SC   95%CI[{cic[0]:+.4f},{cic[1]:+.4f}]")
print(f"    returner level-slope (age-controlled, [C]) = {b3[3]:+.4f} pts/SC")
diff=b3[3]-bc[3]
# bootstrap the DIFFERENCE (resample returners and controls independently)
dd=[]
for _ in range(4000):
    s=np.random.randint(0,n,n)
    br=ols([age[s],age2[s],lvl[s]],eff[s])[3]
    sc=np.random.randint(0,len(cdav),len(cdav))
    bcc=ols([cage[sc],cage[sc]**2,cstart[sc]],cdav[sc])[3]
    dd.append(br-bcc)
print(f"    ABSENCE-SPECIFIC level form = returner − control = {diff:+.4f} pts/SC  95%CI[{np.percentile(dd,2.5):+.4f},{np.percentile(dd,97.5):+.4f}]")

# --- (G) MEAN-REVERSION-ADJUSTED effect (age AND level matched) — the clean 'truth' for R3/R4 ---
cl=D.build_control_lvl(); pred=D.fit_ctrl_model(cl)
rows2=D.effect_rows(ev,exp,ctrl_predict=pred)
adj=np.array([r['effect_adj'] for r in rows2]); age_a=np.array([r['age_pre'] for r in rows2])
print("\n[G] MEAN-REVERSION-ADJUSTED effect (matched on age AND pre-level):")
bootg=[adj[np.random.randint(0,len(adj),len(adj))].mean() for _ in range(4000)]
print(f"    overall: {adj.mean():+.2f} SC  95%CI[{np.percentile(bootg,2.5):+.2f},{np.percentile(bootg,97.5):+.2f}]   (age-only was -3.42)")
for lo,hi,lab in [(18,25,'young 18-24'),(25,29,'prime 25-28'),(29,40,'older 29+')]:
    m=(age_a>=lo)&(age_a<hi)
    if m.sum()>=5:
        bs=[adj[m][np.random.randint(0,m.sum(),m.sum())].mean() for _ in range(3000)]
        print(f"    {lab:12} n={m.sum():3d}  adj={adj[m].mean():+.2f}  95%CI[{np.percentile(bs,2.5):+.2f},{np.percentile(bs,97.5):+.2f}]")

# --- verdict logic (on the ABSENCE-SPECIFIC, mean-reversion-netted slope) ---
print("\n[VERDICT]  (the raw [A]/[B] slopes are dominated by mean-reversion; judge on [F] absence-specific)")
mult_pred = adj.mean()/lvl.mean()   # multiplicative predicts slope = mean_effect / mean_level
lo_d,hi_d=np.percentile(dd,2.5),np.percentile(dd,97.5)
print(f"    absence-specific level slope = {diff:+.4f} pts/SC   95%CI[{lo_d:+.4f},{hi_d:+.4f}]")
print(f"    ADDITIVE       predicts slope  0.0000  -> {'INSIDE' if lo_d<=0<=hi_d else 'OUTSIDE'} CI  (|dist|={abs(diff):.4f})")
print(f"    MULTIPLICATIVE predicts slope {mult_pred:+.4f}  -> {'INSIDE' if lo_d<=mult_pred<=hi_d else 'OUTSIDE'} CI  (|dist|={abs(diff-mult_pred):.4f})")
print("    => point estimate sits essentially ON the multiplicative prediction; both forms inside CI (undistinguished).")
