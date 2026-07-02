"""
tail_restore.py  (cont.27) -- TAIL-RESTORATION prototype for the par-path pre-debut band.

WHY: empirical decomposition (cont.27 Check 2) showed the par-path band UNDER-DISPERSES the
high-pick UPPER tail for HIGH-SCORING positions (MID emp p90 116 vs band ~105; KEY_FWD 101 vs 88),
while GEN_DEF/KEY_DEF are correct (103 vs 102 -- no high tail to clip) and are LEFT UNTOUCHED.
Root cause = the quantile GBR smooths the sparse high-scoring star tail (dispersion axis, NOT pick axis;
proof: position-dependent at the SAME pick). PVC is an expected-value curve (Check 1), so the high-pick
~50%-of-PVC gap is under-pricing, not honest markdown.

FIX (this module): restore the band's UPPER quantiles (p70/p90) toward the EMPIRICAL at-draft best-3
distribution, evidence-weighted -- at exposure 0 the upper tail = empirical (full pedigree ceiling), and
as evidence accrues it -> the GBR band. max() so it only RAISES. STRICTLY MID/KEY_FWD, high picks only.

THREE REQUIREMENTS (Luke) -- all satisfied by construction:
  (1) DISPERSION axis, not pick axis: we raise p70/p90 SPREAD; the empirical target is loclin-smoothed
      over log-pick + isotonic (monotone non-increasing) -- same smoothing the centre uses. No pick-curve extension.
  (2) HOLDS AT PRESEASON / exposure 0: the restoration weight is (1-w)*pickf, w=min(1,exposure/RAMP).
      At exposure 0, w=0 -> full restoration, decoupled from season progress/availability. DUURSMA TEST passes
      (pk1 MID, 0 games, preseason -> ~full pedigree, no crash, continuous through debut).
  (3) TWO MOMENTS distinct: this fix is ORTHOGONAL to the season-aware haircut -- it touches only the upper
      quantiles (ceiling), keyed on EVIDENCE; the availability tilt touches p50/p10, keyed on SEASON. Restoring
      the ceiling does NOT reintroduce a draft-day discount. (Integrating the season-aware haircut into the
      par-path pre-debut path so "season-underway-undebuted" < "just-drafted" is a separate WIRE-IN concern.)

MAGNITUDE: empirical p90 (MID ~115) is the FLOOR of the plausible range. Final high-pick upside is set
against ACTUAL league draft-capital trades (Luke's call). The residual gap to PVC (pk1 ~79%) is NOT clipping
and NOT captaincy (both PVC and v_at_peak include capt_prem) -- it is PVC's best2+CE pick-curve method pricing
the same outcome distribution ~10-20% above the engine's v_at_peak best-3 chain. The restored numbers are
engine-consistent; do not chase PVC to 100%.

STATUS: prototype, NOT wired into engine value(). Import after par_redesign (PR). 200-tree mock fidelity.
"""
import numpy as np
import copy

# late-bound against par_redesign (PR) so train/inference share the par-centred level monkeypatch
PR=MA=cp=rd=dp=None; RAMP=22.0
HIGH_TAIL={'MID','KEY_FWD','GEN_DEF'}   # cont.28: GEN_DEF added — mid-pick (pk7-40) prospects were excluded from tail
# restoration, capping their upper tail at p90 91-94 vs defenders' own realized p95 97-102 (per-tier test). The max()
# guard self-limits: pk1-6 already reach elite (band 112 >= realized p90) -> no-op; KEY_DEF stays OUT (its lower elite
# is correctly capped, like KEY_FWD). SCOPE: PRE-DEBUT prospects only (the established path does NOT call restore); the
# on-list named young defenders (Kyle/Zeke, 3g/10g = established) are unreachable here — their dead level=0 pedigree pole
# is the separate established-path item (U28-D). TEMPORARY ARTIFACT: a restored undebuted defender can LOSE the lift at
# debut (routes to the established path) until U28-D closes it. Accepted as marginal/temporary, logged.
PICK_GATE=46            # cont.27: 16->26->46. Extended so pk21-40 reach the same empirical-p90 anchor pk1-20 already meet
TAPER_FULL=40          # cont.27: 8->20->40. FULL restoration pk1-40 (pk1-20 unchanged-already-full; pk21-40 lifted); fade pk40->46.
# WHY (cont.27, verified clean-chain + survivorship-gated): the band under-disperses the high-scoring upper tail more at higher
# picks; the fade died too early (16, then 26), leaving pk21-40 under-restored. The clean DRAFT-AGE realized gradient stabilises
# at 1.69-1.73x once careers are resolved (draft<=2017/2018, peak reached) with pk40~430-452 (bust-RETAINED); the band's
# unrestored pk40 of 325 was tail-clipped. The 12% "validated-pick under-leveling" was a PEAK_AGE pricing artifact, NOT real
# (pk1-8 stand). max() guard in restore() => only RAISES where band < empirical-p90; no-op (incl. KEY_FWD/converged late picks).
_EMP={}; EMPC={}

def bind(par_redesign):
    """Wire to a loaded par_redesign module and build the empirical curves."""
    global PR,MA,cp,rd,dp,RAMP
    PR=par_redesign; MA=PR.MA; cp=PR.cp; rd=PR.rd; dp=PR.dp; RAMP=PR.RAMP
    _build_curves()

def _atdraft_pts(pos):
    o=[]
    for p in MA.data:
        if p.get('_double_count') or MA.gfut(p)!=pos or not (p.get('pick') or p.get('_ft')): continue
        if not (2003<=cp.debutyr(p)-1<=2018): continue
        b=cp.fwd_best3_from(p,cp.debutyr(p)-1,2026)
        if b is not None: o.append((MA.effpk(p),b))
    return o

def _loclin(xs,ys,x0,bw=0.45):
    pts=[(np.log(x),y,np.exp(-0.5*((np.log(x)-np.log(x0))/bw)**2)) for x,y in zip(xs,ys) if y==y]
    W=sum(w for *_,w in pts)
    if W<1e-9: return float('nan')
    xb=sum(w*x for x,_,w in pts)/W; yb=sum(w*y for _,y,w in pts)/W
    sxx=sum(w*(x-xb)**2 for x,_,w in pts)
    if sxx<1e-9: return yb
    b=sum(w*(x-xb)*(y-yb) for x,y,w in pts)/sxx
    return (yb-b*xb)+b*np.log(x0)

def _pava_dec(val):   # isotonic non-increasing (weighted pool-adjacent-violators on the negation)
    a=[-x for x in val]; idx=[[i] for i in range(len(a))]; i=0
    while i<len(a)-1:
        if a[i]>a[i+1]+1e-9:
            m=(a[i]*len(idx[i])+a[i+1]*len(idx[i+1]))/(len(idx[i])+len(idx[i+1]))
            a[i]=m; idx[i]+=idx[i+1]; del a[i+1]; del idx[i+1]; i=max(0,i-1)
        else: i+=1
    out=[0.0]*len(val)
    for vv,ix in zip(a,idx):
        for j in ix: out[j]=-vv
    return out

def _build_curve(pos,q):
    pk=list(range(1,47)); raw=[]   # cont.27: 21->27->47; extended to pk46 to anchor full restoration pk1-40 + fade pk40-46
    for k in pk:
        v=[b for ppk,b in _EMP[pos] if abs(ppk-k)<=5]
        if len(v)<8: v=[b for ppk,b in _EMP[pos] if abs(ppk-k)<=10]
        if len(v)<8: v=[b for ppk,b in _EMP[pos] if abs(ppk-k)<=15]   # cont.27: widen smoothing where the late-pick slice is thin (say so)
        raw.append(np.percentile(v,q) if len(v)>=8 else float('nan'))
    sm=[_loclin(pk,raw,k) for k in pk]; iso=_pava_dec(sm)
    return {k:iso[i] for i,k in enumerate(pk)}

def _build_curves():
    global _EMP,EMPC
    _EMP={pos:_atdraft_pts(pos) for pos in HIGH_TAIL}
    EMPC={(pos,q):_build_curve(pos,q) for pos in HIGH_TAIL for q in (70,90)}

def emp_q(pos,pk,q): return EMPC.get((pos,q),{}).get(min(pk,46))   # cont.27: cap 20->26->46
def pickf(pk):       return max(0.0,min(1.0,(PICK_GATE-pk)/float(PICK_GATE-TAPER_FULL)))  # 1.0 @ pk1-8 -> 0 @ PICK_GATE

def restore(band,p,Y=2026,_w=None):
    """Return the band with upper quantiles (p70/p90) restored toward the empirical at-draft tail.
    Only MID/KEY_FWD, only high picks; only RAISES; full at exposure 0."""
    pos=MA.gfut(p); pk=MA.effpk(p)
    if pos not in HIGH_TAIL or pk>PICK_GATE: return band
    w=min(1.0,cp._exposure(p,Y)/RAMP) if _w is None else _w
    rw=(1.0-w)*pickf(pk)
    if rw<=0: return band
    b=list(band); e70=emp_q(pos,pk,70); e90=emp_q(pos,pk,90)
    if e70 is not None: b[3]=max(b[3],(1-rw)*b[3]+rw*e70)
    if e90 is not None: b[4]=max(b[4],(1-rw)*b[4]+rw*e90)
    b[4]=max(b[4],b[3]); b[3]=max(b[3],b[2])     # keep monotone after the raise
    return b

def rband(p,cm,Y=2026): return restore(PR.band5(p,cm,Y),p,Y)
def rval(p,cm,Y=2026):  return PR.priceband(p,rband(p,cm,Y))

# ─────────────────────────────────────────────────────────────────────────────
# WIRE-IN ROUTER (cont.27, option B) — THE production value() entry point.
# ─────────────────────────────────────────────────────────────────────────────
# Lives HERE (tail_restore, above dist_redesign) because the restoration (rval) lives here and the bind to
# PR is guaranteed at this layer. The documented step-1 plan ("edit dist_redesign.redesign_value") is option A
# and was REJECTED against a fact the plan did not have: the dep graph runs tail_restore -> par_redesign ->
# dist_redesign, so redesign_value calling UP to rval needs TR bound first — which build_dist_walkforward
# violates (it imports rd WITHOUT par_redesign loaded) => a latent binding bug detonating in the irreversible
# step. This router runs rval VERBATIM, so the validated pre-debut numbers reproduce byte-exact; redesign_value
# is untouched; established stays on the validated par-path.
SCORERS=['MID','GEN_FWD','KEY_FWD']     # RUC borrows this data-rich scorer shape, anchored to RUC's own level

def synth(pos,pk):                       # VERBATIM from pickcurve_build.py — byte-exact synth scorer for the RUC pool
    b=[p for p in MA.players if MA.gfut(p)==pos and MA.GRP.get(p['pos'])][0]
    q=copy.deepcopy(b)
    q['pick']=pk; q['_eff']=pk; q['_ft']=False; q['scoring']=[]; q['year']=2025; q['_by']=2007
    return q

def _plvl(pos,pk): return PR.pb.level_at(PR.F,pos,pk)[0]   # par-build level at (pos,pk); pb,F reached via the PR bind

def production_value(p,cm,Y=2026,lens='bal'):
    """Production value entry point (wire-in, option B).
    PRE-DEBUT (level_now None): par-path. RUC -> scorer-borrow POOL (n=69 too thin for a per-pick ruck curve;
      the band over-fits late-pick outliers -> the pk20-30 inversion; rucks score ~0.95x the scorer pool at every
      pick, a reliable level ratio, so borrow the data-rich scorer SHAPE anchored to RUC's own level). Everyone else
      -> rval (MID/KEY_FWD carry the restored upper tail; others the unrestored band).
    ESTABLISHED: rd.redesign_value (validated par-path: production / position-beta floor / brodie / ruck-tax).
    DEFERRED (tail_restore docstring pt 3): the season-aware haircut ('season-underway-undebuted' < 'just-drafted')
      is NOT yet in the par-path, so in-window 0-game players currently price == genuine pre-debut. Logged, not silent.
    rval is called UNCHANGED => the pre-debut curve is byte-exact to the pre-router validated values (step-4 gate)."""
    if MA.level_now(p) is None:                                  # PRE-DEBUT
        if MA.gfut(p)=='RUC':                                    # scorer-borrow pool
            pk=MA.effpk(p)
            sc =float(np.mean([float(rval(synth(g,pk),cm,Y)) for g in SCORERS]))
            scl=float(np.mean([_plvl(g,pk) for g in SCORERS]))
            return sc*(_plvl('RUC',pk)/scl) if scl else sc
        return rval(p,cm,Y)                                      # MID/KEY_FWD restored tail; others unrestored band
    return rd.redesign_value(p,cm,lens=lens)                     # ESTABLISHED: validated par-path
