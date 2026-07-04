#!/usr/bin/env python3
"""
GROWTH-CURVE VALIDATION  —  read-only diagnostic (EVIDENCE 1/3, V0/PVC overhaul)
================================================================================
Does the age / production growth-curve SHAPE the BAKED engine assumes match what
players REALISED on the baked walk-forward history?

  [BAKED c47cb43d]  main 389ac39  ·  engine md5(_merged_recover.py)=c47cb43d

READ-ONLY on every engine/data path.  Writes ONLY to evidence/growth_curve/.
No engine change, no bake, no derivation committed to the engine.

HOW TO RUN (reproduces byte-for-byte at the baked state):
  cd /home/claude/rl_workspace/rl_after            # the bootstrapped engine dir
  export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 \
         RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
  export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
  python3 <repo>/evidence/growth_curve/growth_curve_validation.py
  # engine dir overridable via RL_AFTER=... ; output dir via GC_OUT=...

WHAT IT PRODUCES (all under evidence/growth_curve/):
  growth_curve_report.txt   full printed report (this script's stdout)
  wf_frame.csv              the walk-forward observation frame (one row per player,Y)
  residual_by_age.csv       smoothed residual-by-age curves + eff-n (production & value)
  assumed_vs_realised.csv   the assumed value shape (age-sweep) alongside realised
  anchors.csv               Gawn/Bontempelli/Heeney modelled-vs-realised trajectories

METHOD — the two traps, addressed in code and in FINDINGS.md:
 (a) SURVIVORSHIP.  Players who leave the league are ABSENT from late-age buckets,
     so a raw realised-by-age curve is biased UP at old ages (only good old players
     remain).  The HEADLINE read is the MATCHED residual (predicted-minus-realised on
     the SAME rows): predicted is computed on the identical survivor set as realised,
     so the survivor bias cancels in the residual.  We ALSO print the raw survivor
     curve next to a cohort-complete curve (fully-resolved 2009-2016 cohorts, washouts
     retained as 0) to make the bias visible and quantify it.
 (b) VALUE != SCORING.  The engine prices VALUE, not raw SC average.  We keep two
     separate residuals: a PRODUCTION residual (engine's central forward-best3
     projection vs realised forward best3, SC-avg units) and a VALUE residual (band
     price vs the realised forward best3 priced on the engine's OWN value ladder
     v_at_peak, at the matched evaluation age).  They are never mixed.
"""
import io, contextlib, os, sys, json, csv, subprocess, hashlib
import numpy as np

# ----------------------------------------------------------------------------- paths
RL_AFTER = os.environ.get('RL_AFTER', '/home/claude/rl_workspace/rl_after')
OUT      = os.environ.get('GC_OUT',  os.path.join(os.path.dirname(os.path.abspath(__file__))))
REPO     = os.environ.get('GC_REPO', '/home/user/afl-rl-engine')
os.makedirs(OUT, exist_ok=True)

# tee stdout to the report file
class _Tee:
    def __init__(self,*s): self.s=s
    def write(self,d):
        for x in self.s: x.write(d)
    def flush(self):
        for x in self.s: x.flush()
_report = open(os.path.join(OUT,'growth_curve_report.txt'),'w')
sys.stdout = _Tee(sys.__stdout__, _report)

def hr(t=''): print('\n'+'='*92+('\n'+t if t else ''))

# ----------------------------------------------------------------- STEP 0 ASSERT (blocking)
hr("STEP 0 — FETCH + ASSERT   [BAKED c47cb43d]")
def _md5(path):
    return hashlib.md5(open(path,'rb').read()).hexdigest()[:8]
eng_repo = os.path.join(REPO,'engine/rl_after/_merged_recover.py')
eng_run  = os.path.join(RL_AFTER,'_merged_recover.py')
md5_repo = _md5(eng_repo) if os.path.exists(eng_repo) else 'MISSING'
md5_run  = _md5(eng_run)  if os.path.exists(eng_run)  else 'MISSING'
try:
    main_sha = subprocess.check_output(['git','-C',REPO,'rev-parse','origin/main']).decode().strip()[:7]
    head_sha = subprocess.check_output(['git','-C',REPO,'rev-parse','HEAD']).decode().strip()[:7]
except Exception as e:
    main_sha=head_sha=f'(git n/a: {e})'
print(f"  origin/main            : {main_sha}     (expect 389ac39)")
print(f"  HEAD (this branch)     : {head_sha}")
print(f"  md5 repo engine        : {md5_repo}     (expect c47cb43d)")
print(f"  md5 run-dir engine     : {md5_run}     (the engine actually exec'd below)")
ASSERT_OK = (md5_run=='c47cb43d')
print(f"  ASSERT engine==c47cb43d: {'PASS' if ASSERT_OK else 'FAIL -> STOP'}")
if not ASSERT_OK:
    print("  *** engine md5 mismatch — STOP per STEP 0 ***"); sys.exit(1)

# ------------------------------------------------------------------------ load the engine
os.chdir(RL_AFTER)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
# Walk-forward / backtest path: Luke's D14 exemption — board-only laws (V0 curve, KPP floor)
# OFF so the historical book reproduces byte-for-byte. (Same switch _comb_book.py sets.)
g['_BOARD_PATH'] = False
MA=g['MA']; cp=g['cp']; dp=g['dp']
ev=g['ev']; b6=g['b6']; price6=g['price6']; raw_ev=g['raw_ev']
WQ6=np.asarray(g['WQ6']); fwd=cp.fwd_best3_from
delisted=g['delisted']
POS6=('MID','GEN_DEF','GEN_FWD','KEY_DEF','KEY_FWD','RUC')

def set_year(Y):
    MA.BASE_REF=MA.AGE_REF=Y; MA._pe_clear()

# sanity: reproduce a couple of board anchors on the BOARD path (independent check we hold baked state)
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None
g['_BOARD_PATH']=True; set_year(2026)
_daic=ev(find('Nick Daicos')); _gawn=ev(find('Max Gawn'))
g['_BOARD_PATH']=False
print(f"  board sanity           : Nick Daicos={_daic} (expect 7013)  Max Gawn={_gawn} (expect 2120)  "
      f"{'OK' if (_daic==7013 and _gawn==2120) else 'MISMATCH'}")

# ============================================================================ SECTION A
hr("SECTION A — THE ENGINE'S ASSUMED GROWTH CURVE (constants, no data)  [BAKED c47cb43d]")
print("""  The baked engine layers several AGE surfaces onto the forward valuation:
   1. PEAK_AGE[pos]          per-position peak age (the vertex of the value curve)
   2. DELTAS / frac(a-peak)  fraction-of-peak VALUE by (age - peak_age)  [drives v_at_peak]
   3. AGE_CURVE[pos][age]    per-position empirical fraction-of-peak (dev-advance roll)
   4. _AGEMULT(age)          decliner-shed: realised-forward / current, by age
   5. wage = clip(1-(a-20)/6,0,1)   upside/pole credit weight (linear fade 20->26)
   6. _v7 asc = interp(a,[20,22,24,27],[1.00,0.76,0.58,0.40])  q97 tail age-scale (REAL players)
""")
print("  PEAK_AGE:", dict(MA.PEAK_AGE))
print("\n  DELTAS (fraction-of-peak VALUE by age-minus-peak):")
for d in sorted(MA.DELTAS): print(f"      {d:+3d}: {MA.DELTAS[d]:.2f}", end='')  # noqa
print()
print("\n  AGE_CURVE (fraction-of-peak by ABSOLUTE age, per position):")
print("      age " + "".join(f"{a:6d}" for a in range(18,35)))
for pos in POS6:
    c=MA.AGE_CURVE.get(pos,{})
    print(f"      {pos:8s}"+"".join(f"{c.get(a,float('nan')):6.2f}" for a in range(18,35)))
print("\n  _AGEMULT (decliner realised-forward/current):",
      dict(zip(g['_AGEMULT_X'], g['_AGEMULT_Y'])))
print("  wage(age)=clip(1-(a-20)/6,0,1):",
      {a: round(float(np.clip(1-(a-20)/6,0,1)),2) for a in range(20,28)})
print("  v7 asc(age):",
      {a: round(float(np.interp(a,[20,22,24,27],[1.0,0.76,0.58,0.40])),2) for a in [20,22,24,26,28,30]})

# ============================================================================ SECTION B
hr("SECTION B — WALK-FORWARD FRAME: predicted vs realised (one row / player,Y)  [BAKED c47cb43d]")
print("""  For every REAL store player (ND/MSD, GRP position, national-draft pedigree) and every
  evaluation year Y from draft-year(d0) through 2023 (Y<=2023 => forward window >=3 yrs to
  2026, so realised best-3 is not truncation-starved), on the BACKTEST path:
     age_Y            = cp._age_asof(p,Y)                         (self-corrects AGE_REF offset)
     pred_fwd  [prod] = WQ6 . b6(p,Y)      engine central forward-best3 projection (SC-avg units)
     real_fwd  [prod] = fwd_best3_from(p,Y,2026)   realised forward best-3 (0 for washouts)
     pred_val  [val ] = price6(p,b6(p,Y),Y)        band priced to value at age Y
     real_val  [val ] = SCALE_DIST*v_at_peak(p,real_fwd) at age Y   realised prod on the SAME ladder
     horizon          = 2026 - Y
  pred_* and real_* are matched on the SAME row => survivor bias cancels in the residual.""")
pool=[p for p in MA.data if not p.get('_double_count') and MA.gfut(p) in POS6
      and (p.get('pick') or p.get('_ft')) and p.get('type') in ('ND','MSD')]
print(f"\n  pool: {len(pool)} real store players (outfield+RUC, national-draft pedigree)")

print("""
  ANTI-CONTAMINATION (critical): evaluate ONLY at in-career years.  Post-retirement years
  (Y after a player's last active season) are EXCLUDED — there the band still prices frozen
  history (b6/price6 don't check delist) while realised=0, which would spuriously inflate the
  old-age residual.  Frame = Y in [draft-year(d0) .. min(last_active_season, 2023)] (pre-debut
  draft point d0 kept).  horizon=2026-Y recorded so we can DECOUPLE age from forward-window
  length (age and horizon are otherwise confounded: older age <=> later Y <=> shorter window).""")
rows=[]; n_postcareer=0
for p in pool:
    d0=cp.debutyr(p)-1
    pos=MA.gfut(p)
    last_active=max([x['year'] for x in p['scoring'] if x['games']>0], default=d0)
    for Y in range(d0, 2024):
        if Y>last_active:            # post-career -> not a real walk-forward point
            n_postcareer+=1; continue
        set_year(Y)
        try:
            bb=b6(p,Y)
            pred_fwd=float(np.dot(WQ6,bb))
            pred_val=float(price6(p,bb,Y))
            pred_ev =float(ev(p,Y))                      # full engine value (delist/staleness/floor)
            real_fwd=float(fwd(p,Y,2026))
            real_val=float(dp.SCALE_DIST*dp.v_at_peak(p,real_fwd))
        except Exception:
            continue
        a=cp._age_asof(p,Y)
        # qualifying forward seasons actually observed in [Y..2026] (>=6 games)
        nqf=sum(1 for x in p['scoring'] if x['games']>=6 and max(Y,cp.debutyr(p))<=x['year']<=2026)
        rows.append(dict(player=p['player'], pid=id(p), pos=pos, pick=p.get('pick'),
                         eff=MA.effpk(p), draftyr=p.get('year'), typ=p.get('type'),
                         by=(p.get('_by') if p.get('_by') else None), Y=Y, age=round(a,2),
                         horizon=2026-Y, nqf=nqf,
                         pred_fwd=pred_fwd, real_fwd=real_fwd, pred_ev=pred_ev,
                         pred_val=pred_val, real_val=real_val,
                         resid_fwd=pred_fwd-real_fwd, resid_val=pred_val-real_val,
                         active=1 if any(x['games']>=6 and x['year']==Y for x in p['scoring']) else 0))
print(f"  frame: {len(rows)} in-career (player,Y) observations  (excluded {n_postcareer} post-career rows)")
with open(os.path.join(OUT,'wf_frame.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

age =np.array([r['age']      for r in rows])
rf  =np.array([r['resid_fwd'] for r in rows])
rv  =np.array([r['resid_val'] for r in rows])
pf  =np.array([r['pred_fwd']  for r in rows])
qf  =np.array([r['real_fwd']  for r in rows])
pv  =np.array([r['pred_val']  for r in rows])
qv  =np.array([r['real_val']  for r in rows])
hz  =np.array([r['horizon']   for r in rows])

# ------------------------------------------------------- kernel (Nadaraya-Watson) smoother
def nw(agrid, x, y, bw=1.5):
    """Gaussian-kernel local mean of y over age x, plus eff-n=(sum w)^2/sum w^2 at each grid pt."""
    out=[]; effn=[]
    for a0 in agrid:
        w=np.exp(-0.5*((x-a0)/bw)**2)
        sw=w.sum()
        out.append(float(np.dot(w,y)/sw) if sw>0 else float('nan'))
        effn.append(float(sw*sw/np.sum(w*w)) if sw>0 else 0.0)
    return np.array(out), np.array(effn)

AGRID=np.arange(19,35.0001,1.0)
# restrict smoother to ages with real support
def curve_block(title, resid, extra=None):
    print(f"\n  {title}")
    sm,en = nw(AGRID, age, resid, bw=1.5)
    hdr="      age:"+"".join(f"{a:7.0f}" for a in AGRID)
    print(hdr)
    print("      res :"+"".join(f"{v:7.1f}" for v in sm))
    print("      effn:"+"".join(f"{e:7.0f}" for e in en))
    return sm,en

hr("SECTION B1 — SMOOTHED RESIDUAL-BY-AGE (survivorship-ROBUST: matched rows)  [BAKED c47cb43d]")
print("  Sign convention: residual = PREDICTED - REALISED.")
print("    positive => engine OVER-projects at that age;  negative => UNDER-projects.")
smf,enf = curve_block("[PRODUCTION units, SC-avg]  pred_fwd - real_fwd:", rf)
smv,env = curve_block("[VALUE units, keeper $]     pred_val - real_val:", rv)

# ---- horizon control: age and forward-window length are confounded. Re-read the residual on the
# ---- fixed-window subset horizon>=5 (realised best-3 has a full ~5-8yr window at every age), so any
# ---- remaining age-tilt is SHAPE, not truncation.
mH=hz>=5
print("\n  HORIZON-CONTROLLED (forward window >=5 yrs; decouples age from truncation):")
print(f"    subset n={int(mH.sum())} of {len(rows)}")
def nw_sub(agrid,x,y,bw=1.5):
    o=[];e=[]
    for a0 in agrid:
        w=np.exp(-0.5*((x-a0)/bw)**2); sw=w.sum()
        o.append(float(np.dot(w,y)/sw) if sw>0 else float('nan'))
        e.append(float(sw*sw/np.sum(w*w)) if sw>0 else 0.0)
    return np.array(o),np.array(e)
for lab,resid in [("[PRODUCTION] pred_fwd-real_fwd (H>=5)",rf[mH]),("[VALUE] pred_val-real_val (H>=5)",rv[mH])]:
    sm,en=nw_sub(AGRID, age[mH], resid, 1.5)
    print(f"    {lab}")
    print("      age :"+"".join(f"{a:7.0f}" for a in AGRID))
    print("      res :"+"".join(f"{v:7.1f}" for v in sm))
    print("      effn:"+"".join(f"{e:7.0f}" for e in en))
print("      (mean forward horizon by age, full frame):")
mh,_=nw(AGRID, age, hz, 1.5)
print("      hzn :"+"".join(f"{v:7.1f}" for v in mh))
# also the raw predicted & realised means by age (for the overlay + survivorship section)
mpf,_ = nw(AGRID, age, pf, 1.5); mqf,_ = nw(AGRID, age, qf, 1.5)
mpv,_ = nw(AGRID, age, pv, 1.5); mqv,_ = nw(AGRID, age, qv, 1.5)
print("\n  Overlay — PRODUCTION forward-best3 by age (survivor-conditioned means):")
print("      age  :"+"".join(f"{a:7.0f}" for a in AGRID))
print("      pred :"+"".join(f"{v:7.1f}" for v in mpf))
print("      real :"+"".join(f"{v:7.1f}" for v in mqf))
print("  Overlay — VALUE by age (survivor-conditioned means):")
print("      pred :"+"".join(f"{v:7.0f}" for v in mpv))
print("      real :"+"".join(f"{v:7.0f}" for v in mqv))

# save residual curves
with open(os.path.join(OUT,'residual_by_age.csv'),'w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['age','resid_fwd','effn_fwd','resid_val','effn_val',
                                  'pred_fwd','real_fwd','pred_val','real_val'])
    for i,a in enumerate(AGRID):
        w.writerow([a, round(smf[i],2), round(enf[i],1), round(smv[i],2), round(env[i],1),
                    round(mpf[i],2), round(mqf[i],2), round(mpv[i],1), round(mqv[i],1)])

# headline: net over/under by age-band
def band_stat(lo,hi):
    m=(age>=lo)&(age<hi)
    if m.sum()==0: return None
    return dict(n=int(m.sum()), rf=float(rf[m].mean()), rv=float(rv[m].mean()),
                pf=float(pf[m].mean()), qf=float(qf[m].mean()),
                pv=float(pv[m].mean()), qv=float(qv[m].mean()))
print("\n  HEADLINE by age band (matched residual, survivorship-robust):")
print(f"      {'band':10s}{'n':>6s}{'resid_fwd':>11s}{'resid_val':>11s}{'pred_val':>10s}{'real_val':>10s}")
for lo,hi,lab in [(19,22,'19-21'),(22,25,'22-24'),(25,28,'25-27'),(28,31,'28-30'),(31,34,'31-33'),(34,99,'34+')]:
    s=band_stat(lo,hi)
    if s: print(f"      {lab:10s}{s['n']:6d}{s['rf']:+11.1f}{s['rv']:+11.0f}{s['pv']:10.0f}{s['qv']:10.0f}")

# ============================================================================ SECTION C
hr("SECTION C — SURVIVORSHIP made visible: raw survivor vs cohort-complete  [BAKED c47cb43d]")
print("""  The MATCHED residual above is survivorship-robust.  This section quantifies the bias it
  avoids.  Cohorts 2009-2016 are fully resolved (>=10 seasons observed by 2026).  For each age a:
    survivor mean = mean era-adj SC-avg over players ACTIVE (>=6g) at age a
    cohort-complete = mean over ALL cohort members of (era-adj avg if active at a, else 0)
    %active = fraction of the cohort still producing (>=6g) at age a
  The survivor curve rises/holds at old age purely because washouts have dropped out; the
  cohort-complete curve declines.  Reading 'engine under-prices old age' off the survivor
  curve would be the trap.""")
REF=g['REF']; era=g['era']
def eadj(avmt,yr): return avmt*REF/era.get(yr,REF)
cohort=[p for p in pool if 2009<=(p.get('year') or 0)<=2016]
print(f"\n  cohort-complete pool (draft 2009-2016): {len(cohort)} players")
def age_in_year(p,yr):
    set_year(yr); return cp._age_asof(p,yr)
survmean={}; survn={}; compl={}; totn={}
for a in range(19,35):
    sv=[]; cc=[]; act=0; tot=0
    for p in cohort:
        # the player's era-adj avg in the season where they are age a (if any active season maps to age a)
        best=None
        for x in p['scoring']:
            if x['games']>=6:
                ay=age_in_year(p,x['year'])
                if abs(ay-a)<0.5:
                    best=eadj(x['avg'],x['year']); break
        # is age a within the player's plausible career span (debut..2026)?
        set_year(2026)
        d=cp.debutyr(p)
        # map age a to a calendar year for this player using _by (real ages only)
        if p.get('_by'):
            yr=p['_by']+a
        else:
            continue
        if not (d<=yr<=2026): continue
        tot+=1
        if best is not None: sv.append(best); cc.append(best); act+=1
        else: cc.append(0.0)
    if sv: survmean[a]=float(np.mean(sv)); survn[a]=len(sv)
    if cc: compl[a]=float(np.mean(cc)); totn[a]=tot
print("      age      :"+"".join(f"{a:7d}" for a in range(19,35)))
print("      survivor :"+"".join(f"{survmean.get(a,float('nan')):7.1f}" for a in range(19,35)))
print("      complete :"+"".join(f"{compl.get(a,float('nan')):7.1f}" for a in range(19,35)))
print("      %active  :"+"".join(f"{(100*survn.get(a,0)/totn.get(a,1)):7.0f}" for a in range(19,35)))
print("      surv-n   :"+"".join(f"{survn.get(a,0):7d}" for a in range(19,35)))

# ============================================================================ SECTION D
hr("SECTION D — PURE AGE-SWEEP: the engine's assumed VALUE shape, isolated  [BAKED c47cb43d]")
print("""  Isolate the age surface: pin a representative player's demonstrated level via MA._LEVEL_OVR
  (level_now returns it verbatim) so ONLY the age clock moves, and read the engine's value ladder
  dp.v_at_peak(p,L) DIRECTLY at each age (not through ev(), which would reset AGE_REF=Y).  This
  traces the assumed value-vs-age curve driven by PEAK_AGE + frac(age-peak) + the dev roll, holding
  demonstrated level FIXED.  Level L pinned per position at a representative ELITE bar.  NOTE: this
  isolates the CORE ladder; the additional wage/v7 age markdowns (Section A) tilt young>old further.""")
reps=[('MID','Marcus Bontempelli',110.0),('RUC','Max Gawn',105.0),('KEY_FWD','Charlie Curnow',95.0),
      ('KEY_DEF','Sam Taylor',88.0),('GEN_DEF','Jordan Dawson',105.0),('GEN_FWD','Isaac Heeney',100.0)]
sweep_ages=list(range(20,37))
sweep={}; sweep_realage={}
print(f"\n      {'player (pos, L)':30s}"+"".join(f"{a:6d}" for a in sweep_ages))
for pos,nm,L0 in reps:
    p=find(nm)
    if not p: continue
    by=MA.by(p)
    MA.BASE_REF=2026; MA._LEVEL_OVR=float(L0)
    vals=[]; realages=[]
    for a in sweep_ages:
        MA.AGE_REF=int(round(by+a)); MA._pe_clear()
        realages.append(MA._age_at(p,MA.AGE_REF))
        try: vals.append(float(dp.SCALE_DIST*dp.v_at_peak(p,float(L0))))
        except Exception: vals.append(float('nan'))
    MA._LEVEL_OVR=None
    sweep[(pos,nm)]=vals; sweep_realage[(pos,nm)]=realages
    print(f"      {nm[:16]+' ('+pos+f',{L0:.0f})':30s}"+"".join(f"{v:6.0f}" for v in vals))
print("\n  SHAPE (each row normalised to its own peak=100):")
print(f"      {'player (pos)':30s}"+"".join(f"{a:6d}" for a in sweep_ages))
for (pos,nm),vals in sweep.items():
    v=np.array(vals,float); pk=np.nanmax(v) if np.isfinite(v).any() else 1
    pk_age=sweep_ages[int(np.nanargmax(v))]
    print(f"      {nm[:16]+' ('+pos+f',pk{pk_age})':30s}"+"".join(f"{100*x/pk:6.0f}" for x in v))
MA._LEVEL_OVR=None; set_year(2026)
with open(os.path.join(OUT,'assumed_vs_realised.csv'),'w',newline='') as fh:
    w=csv.writer(fh); w.writerow(['pos','player','L']+[f'age{a}' for a in sweep_ages])
    for (pos,nm,L0) in reps:
        if (pos,nm) in sweep: w.writerow([pos,nm,L0]+[round(x,1) for x in sweep[(pos,nm)]])

# ============================================================================ SECTION E
hr("SECTION E — ANCHOR CHECK: modelled vs realised trajectory  [BAKED c47cb43d]")
print("  Identity printed (name-collision guard). modelled = walk-forward ev(p,Y) using evidence")
print("  through Y only (BACKTEST path); realised = actual era-adj SC-avg that season + realised")
print("  forward best-3 from Y.  Do the SHAPES agree?")
anchor_rows=[]
for nm in ['Max Gawn','Marcus Bontempelli','Isaac Heeney']:
    p=find(nm)
    a2026=None; set_year(2026); a2026=cp._age_asof(p,2026)
    print(f"\n  {p['player']}  id={id(p)}  pos={MA.gfut(p)}  pick={p.get('pick')}/eff{MA.effpk(p)}  "
          f"cohort(draft)={p.get('year')}  _by={p.get('_by')}  age2026={a2026:.0f}")
    print(f"      {'year':6s}{'age':>5s}{'games':>6s}{'avg':>6s}{'eadj':>6s}{'ev(Y)modelled':>15s}{'real_fwd3':>10s}")
    for x in sorted(p['scoring'], key=lambda z:z['year']):
        Y=x['year']
        if Y>2023:
            # still show recent years but note short horizon
            pass
        set_year(Y)
        a=cp._age_asof(p,Y)
        try: evY=ev(p,Y)
        except Exception: evY=float('nan')
        rfwd=fwd(p,Y,2026)
        eadj_v=eadj(x['avg'],Y) if x['games']>=6 else float('nan')
        print(f"      {Y:6d}{a:5.0f}{x['games']:6d}{x['avg']:6.1f}{eadj_v:6.1f}{evY:15.0f}{rfwd:10.1f}")
        anchor_rows.append(dict(player=p['player'],pid=id(p),year=Y,age=round(a,1),games=x['games'],
                                avg=x['avg'],eadj=round(eadj_v,1) if x['games']>=6 else '',
                                ev_modelled=round(evY,1) if np.isfinite(evY) else '',
                                real_fwd3=round(rfwd,1)))
with open(os.path.join(OUT,'anchors.csv'),'w',newline='') as fh:
    w=csv.DictWriter(fh, fieldnames=list(anchor_rows[0].keys())); w.writeheader(); w.writerows(anchor_rows)

# ============================================================================ VERDICT
hr("SECTION F — SHAPE VERDICT  [BAKED c47cb43d]")
# peak of the assumed shape vs peak of the realised production
# assumed peak: age at max of a representative MID sweep (Bontempelli), and per-position PEAK_AGE
mid_sweep=sweep.get(('MID','Marcus Bontempelli'))
if mid_sweep:
    ma=sweep_ages[int(np.nanargmax(mid_sweep))]
    print(f"  Assumed MID value peak (age-sweep): age {ma}   (PEAK_AGE MID={MA.PEAK_AGE['MID']})")
# realised production peak by age (cohort-complete, survivorship-honest)
if compl:
    cca=max(compl, key=lambda a:compl[a])
    print(f"  Realised production peak (cohort-complete): age {cca}")
# residual tilt: sign of residual young vs old
def mean_band(arr, lo, hi):
    m=(age>=lo)&(age<hi); return float(arr[m].mean()) if m.sum() else float('nan')
print(f"\n  Matched residual tilt (pred-real, survivorship-robust):")
print(f"    PRODUCTION  young(21-24) {mean_band(rf,21,25):+.1f}   prime(25-28) {mean_band(rf,25,29):+.1f}"
      f"   old(29-33) {mean_band(rf,29,34):+.1f}  SC-avg")
print(f"    VALUE       young(21-24) {mean_band(rv,21,25):+.0f}   prime(25-28) {mean_band(rv,25,29):+.0f}"
      f"   old(29-33) {mean_band(rv,29,34):+.0f}  keeper$")
print("\n  (interpretation & SHAPE verdict written up in FINDINGS.md)")

hr("DONE — outputs under evidence/growth_curve/")
print("  growth_curve_report.txt · wf_frame.csv · residual_by_age.csv · assumed_vs_realised.csv · anchors.csv")
_report.flush()
