"""WIRE (1) delist->~0 (2) staleness floor all-stalled (3) isotonic pick guard INTO the engine. Prove on named players."""
import os,io,contextlib,copy,pickle,numpy as np
import math as _math
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
# ===== DETERMINISM FIX (2026-07-14, session_2026-07-14/determinism_fix) =====
# PART 1 bisect finding: the FIRST cross-environment divergent bit is a BLAS-routed np.dot
# (price6, below) — NOT the NW-smoother the register hypothesised. All 3 np.dot sites on the
# board's critical path (price6 + the two Nadaraya-Watson smoothers) are order-sensitive: the
# OpenBLAS kernel accumulates the sum in a different order per CPU, so the board value moved
# 8 rucks (+1..+4 SCAR) between an AVX-512 (SkylakeX) and an AVX2 (Haswell) build on ONE box.
# The repair (register item 106): replace the order-dependent reductions on the critical path
# with math.fsum — exact-to-one-rounding, order-fixed, identical on every kernel AND every CPU
# SIMD width. The NW normaliser (w.sum) and effective-n (sum(w*w)) are fsum'd for the same
# reason. NOTHING ELSE is touched (fence: this file's identified reductions only).
def _det_dot(a, b):
    return _math.fsum(float(x) * float(y) for x, y in zip(a, b))
def _det_sum(a):
    return _math.fsum(float(x) for x in a)
def _det_mean(a):
    a = [float(x) for x in a]
    return _math.fsum(a) / len(a) if a else 0.0
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA, wire_redesign as W; cm=W.build()
TR=W.TR; rd=TR.rd; cp=TR.cp; dp=TR.dp; PR=W.PR
era={}
for Y in range(2009,2026):
    a=[s['avg'] for p in MA.data for s in p.get('scoring') or [] if s['year']==Y and s['games']>=6]
    if a: era[Y]=float(np.mean(a))
REF=float(np.mean(list(era.values())))
pool=[p for p in MA.data if MA.GRP.get(p['pos'])]
X,yy=[],[]
_L4_MSD=os.environ.get('RL_MSD_POOL_EXCL','1')!='0'   # v2.9 L4: MSD training-pool exclusion (default ON; =0 ⇒ base byte-exact). Kill-switch; G-ATTR-separable.
for p in pool:
    if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')) or (_L4_MSD and p.get('type')=='MSD'): continue
    d0=cp.debutyr(p)-1; last=max([x['year'] for x in p['scoring']]+[d0])
    for Y in range(d0,min(last,2026)+1): X.append(cp._feat(p,Y)); yy.append(cp.fwd_best3_from(p,Y,2026))
# v2.9 L4 EDIT TRIPWIRE (membership stability — L4_AND_TRIO_FINDINGS; register item 17 D7). The re-entry trio
# (Perez/McAndrew/Keane) is kept OUT of the calibration training pool by the DEBUT>2021 window, NOT by entry-type.
# Any store edit (a DOB/debut correction re-admitting them, or a type relabel) that silently flips a named
# load-bearing row's pool membership HALTS for a ruling — that is exactly the silent-re-admit hole.
_L4_TRIP_NAMED={'Flynn Perez','Lachlan McAndrew','Mark Keane'}
def _in_train_pool(p): return not (cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')) or (_L4_MSD and p.get('type')=='MSD'))
for _tp in MA.data:
    if _tp.get('player') in _L4_TRIP_NAMED and _in_train_pool(_tp):
        raise SystemExit("L4 TRIPWIRE HALT (membership stability): %s re-admitted to the calibration training pool "
                         "— a store edit flipped a named load-bearing leg (debut>2021 window / entry-type). Rule "
                         "before shipping (L4_AND_TRIO_FINDINGS; register item 17 D7)."%_tp.get('player'))
# q97m FROZEN 2026-07-14 (owner ruling — determinism fix). WAS: a GradientBoostingRegressor.fit(X,yy) RIGHT HERE,
# on every board/gate/panel import, PINNED BY NOTHING. numpy's OpenBLAS is DYNAMIC_ARCH (it selects a CPU-specific
# float kernel at runtime); GitHub runs a mixed-CPU fleet, so the SAME commit trained q97m slightly differently per
# runner -> every player moved a little in both directions -> the cross-environment CI red (green as pull_request,
# red as push, same SHA). q97 is band[5] (price6 weight 0.10). It now gets the treatment cm already gets: fitted
# ONCE at a bake, pickled to data/q97m.pkl, stamped (data/expected_boot.json 'q97m'), asserted by boot_guard on
# entry, and LOADED here — NEVER fitted at build time. The X/yy pool above is retained UNCHANGED so the ONE
# committed refit entry point (refit_q97m.py) fits from the identical inputs this line used to; the running engine
# no longer consumes X/yy. Regenerate ONLY via refit_q97m.py at a bake (it re-pins + HALTs downstream). A silent
# refit is the exact defect being fixed: there is deliberately no fit path left here.
def _load_q97m():
    _cands=[os.environ.get('RL_Q97M_PKL'), '/home/claude/q97m.pkl',
            os.path.join(os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '','data','q97m.pkl')]
    for _c in _cands:
        if _c and os.path.exists(_c):
            with open(_c,'rb') as _fh: return pickle.load(_fh)
    raise SystemExit("q97m FROZEN-LOAD HALT: no frozen q97m pickle found (looked at RL_Q97M_PKL, "
                     "/home/claude/q97m.pkl, <repo>/data/q97m.pkl). Re-run bootstrap.sh to seed the workspace copy, "
                     "or regenerate via refit_q97m.py at a bake. The engine NEVER fits q97m at build time.")
q97m=_load_q97m()
WQ6=np.array([0.18]*5+[0.10]); WQ6/=WQ6.sum(); RECX=[0.30,0.52,0.67,0.82,0.97,1.30]; RECY=[0.54,0.64,0.84,1.00,1.00,1.00]
midpos=next(r['pos'] for r in MA.data if MA.GRP.get(r.get('pos'))=='MID'); GRPPOS={}
for r in MA.data:
    g=MA.GRP.get(r.get('pos'))
    if g and g not in GRPPOS: GRPPOS[g]=r['pos']
# ===== STEP1 #1-FAMILY FIX (inference-only; band pickle + q97m above trained on ORIGINAL features -> Delta=0 for proven-flat) =====
PROVEN_N=4; POLE_RAMP=22.0    # PROVEN_N surface NOT wired (no committed exec spec) -> scalar 4 + c=n/4 retained; see CHANGELOG 2026-06-30
# ==== GAMES-RAMP PRORATION (D10 03/07/2026 — Luke's design statement, verbatim in the directive):
# every games bar (6/10/14/22) prorates to season progress for the IN-PROGRESS season — a player is
# judged only against games that were playable (R14/24 -> fE=0.58 at this cut; RL_M3_FE = the M2/M3
# season-progress convention, one dial). Completed seasons are byte-identical (fE=1). G_ADQ (12, M1
# proven-player recent-adequacy window) deliberately NOT prorated — outside the 6/10/14/22 enumeration.
SEASON_FE=float(os.environ.get('RL_M3_FE','0.58'))
INPROG_Y=int(os.environ.get('RL_M3_INPROG_Y','2026'))
# ==== RL_AVAIL — LTI/AVAILABILITY LAYER (Chapter-3 2026-07-09; register-driven; touches register keys only) ==
# Part 1 (current-season nerf, R-iv = season-state at the proration seam): for a register name out for the
# remainder of 2026, his 2026 is COMPLETE at his real games — so his effective season fraction is 1.0 (NOT the
# global SEASON_PROG). `_fEy(Y,p)` returns 1.0 for those names, which stops the /SEASON_PROG gross-up and makes
# the τ' penalty, the 6/12-game qualification bars and the sit-out λ blend re-price on FINAL-games footing.
# This is NOT a stacked multiplier — the one new present factor is the lost-production term _avail_hc = L_p
# (set on the record below; feeds the k=0 present haircut the retired _b2hc used to feed). M2/M3 keep owning
# clock proration (the falsified games-completion ruling is honoured: nobody's season is "completed" — Rozee
# stays 2 games; we only stop grossing them up). RL_AVAIL=0 ⇒ _AVAIL_STATE empty ⇒ _fEy(Y,p)==_fEy(Y) and
# _avail_hc==0 for every player ⇒ byte-exact to the layer-off board (register-only movement by construction).
_AVAIL_ON=os.environ.get('RL_AVAIL','1')!='0'
_LTI_RETURN_ON=os.environ.get('RL_LTI_RETURN','1')!='0'       # Part-2 return-haircut arm (separable lever, G-ATTR)
_LTI_CLOCK=os.environ.get('RL_LTI_CLOCK','advance')          # fork-i L1c clock: advance (DEFAULT, owner-ruled R-i 2026-07-10, DECISIONS v90 §36) | pause (retired provisional). Pinned in data/model_config.json + asserted by ruling_config_check.py (a paused bake/gate fails loudly).
_AVAIL_STATE={}                                               # key -> availability state (populated by the layer block below)
_KPF_LD_FALLBACK=set()                                        # fork-v: register names whose LD fell back to count-against (report-only)
def _fe_p_one(p):                                             # True iff this player's 2026 is priced as COMPLETE (out-for-remainder register name)
    st=_AVAIL_STATE.get(p.get('key')) if p is not None else None
    return bool(st and st.get('out'))
def _fEy(Y,p=None):
    if Y==INPROG_Y:
        return 1.0 if _fe_p_one(p) else SEASON_FE
    return 1.0
def _playable(p,Y):                                           # full-season-equivalent games playable since debut
    return cp.SEASON*(max(0,Y-cp.debutyr(p))+(_fEy(Y,p) if Y>=cp.debutyr(p) else 0.0))
# STEP-3 CALIBRATION WIRED 2026-06-30 (candidate): per-group LDECAY + FLAT_TOL (KEY / GEN / MID+RUC)
def _ldg(pos): return 'KEY' if pos in ('KEY_FWD','KEY_DEF') else ('GEN' if pos in ('GEN_FWD','GEN_DEF') else 'MR')
LDECAY_G={'KEY':0.40,'GEN':0.35,'MR':0.225}; FLAT_TOL_G={'KEY':10.3,'GEN':12.0,'MR':14.0}
# DECLINER SHED 2026-06-30 (candidate): DERIVED from realised forward output of established decliners (drop>3).
#   recovery~0 beyond ~3 SC drop (forward stays at declined current); age accelerates forward BELOW current.
#   _AGEMULT = measured smoothed forward/current by age (washout-incl); DOWN_TOL = wobble band (recovery noisy <3).
_AGEMULT_X=[20,22,25,28,30,32,34,37]; _AGEMULT_Y=[0.92,0.89,0.85,0.79,0.73,0.68,0.62,0.55]
def _agemult(a): return float(np.clip(np.interp(a,_AGEMULT_X,_AGEMULT_Y),0.53,0.95)) if a is not None else 0.85
DOWN_TOL=3.0   # down-side hold band (data: recovery~0 beyond ~3); ASYMMETRIC vs up-side FLAT_TOL (10-14)
# FORM-CONDITIONED DECLINER SHED 2026-07-06 (candidate, folded from PR #45 verbatim at the W4 integration): the
#   age-only _agemult over-sheds STILL-ELITE elders (measured: a former-Brownlow-level 33yo who dips >3 is
#   multiplied 0.65 by age alone). DERIVED f(age, level) from realised forward output: r = washout-incl
#   fwd-mean(Y+1..Y+3)/Lc over the established SHED population (nq>=PROVEN_N & Lo-Lc>DOWN_TOL, 2369
#   player-seasons, debut..2024). Level axis = lcr = Lc - REPL[gfut] (production above positional replacement —
#   separates a still-elite dip from a genuine fade; mean r rose 0.11 -> 0.90 across lcr, monotone). _agemult2 =
#   _agemult(age) + UP-ONLY credit bump _fbump(age,lcr): bump = kernel-smoothed E[max(0, r - _agemult(age))]
#   (2-D adaptive Gaussian bw grown to eff-n>=35 per node; all cells eff-n>=40 so the declared thin-cell
#   shrink-to-1D-prior stayed inert), isotonic non-decreasing in lcr / non-increasing in age; positions POOLED
#   (predecessor: position ~uniform; RUC thinnest — DECLARED).
#   SINGLE-LEVER SAFETY: (i) lcr<=0 -> byte-exact _agemult (every below-replacement fader still falls; e.g.
#   Coniglio/Adams/Blicavs Δ=0); (ii) up-only -> the curve never sheds MORE than the age baseline (no down-mover);
#   (iii) reached ONLY on the shed down-branch, so every non-shed player is Δ=0 by construction.
#   Kill-switch RL_FORMDECL=0 -> byte-exact to baked v2.5. Derivation: PR #45 / session_2026-07-06/.
_FORMDECL=os.environ.get('RL_FORMDECL','1')!='0'
_FB_AGE=[22.,25.,28.,30.,32.,34.,37.]; _FB_LCR=[0.,5.,15.,30.]   # runtime knots: 0-anchored (lcr<=0 hard-zeroed)
_FB_Z=[[0.,0.1152,0.1239,0.1439],[0.,0.1152,0.1239,0.1439],[0.,0.0968,0.1192,0.1439],[0.,0.0704,0.0939,0.1439],
       [0.,0.053,0.0802,0.1439],[0.,0.0414,0.0802,0.1369],[0.,0.0296,0.0802,0.1051]]   # up-only credit; fitted session_2026-07-06
def _fbump(a,lcr):
    a=float(np.clip(a,_FB_AGE[0],_FB_AGE[-1])); l=float(np.clip(lcr,0.0,_FB_LCR[-1]))
    col=[float(np.interp(l,_FB_LCR,row)) for row in _FB_Z]       # per-age bump at this lcr, then interp over age
    return float(np.interp(a,_FB_AGE,col))
def _agemult2(a,lcr):                                            # form-conditioned decline multiplier (age x level-above-replacement)
    base=_agemult(a)
    if a is None or not _FORMDECL or lcr<=0.0: return base       # byte-exact age-only where inert / at-or-below replacement
    return float(np.clip(base+_fbump(a,lcr),0.53,0.98))          # ceiling 0.95->0.98: a still-elite elder sheds only lightly
cp._lvl_eff_orig=cp._lvl_eff
def _nqual(p,Y): return sum(1 for x in p['scoring'] if x['games']>=10 and x['year']<=Y and (cp.debutyr(p)-1)<x['year'])
# D10 SCOPE NOTE (declared): the 10-bar prorates for the FIRST qualifying season only (delivered
# fractionally + smoothly via the f1 credit in _coreM1 below — the games-ramp/rookie family, the
# directive's evidence base, DIAG-B CF4). A board-wide prorated 10-bar was measured this session and
# REJECTED: it discontinuously re-prices Luke-ruled anchors outside the games-ramp channel (Tsatas
# accept-and-track 1140 -> 2080 breaking A8; O'Driscoll -525, Cadman -253 via mid-season proven flips).
# Extending the proration to multi-season nqual increments needs a Luke ruling; the pre-existing
# full-10-bar step for those players stands (known seam class, h-M3-blend-seam-noise register).
# ==== FIX 1 — SMOOTH SMALL-SAMPLE DAMPING (R99.1 TAKE, owner-ruled 2026-07-14) ====================
# A season's WEIGHT in the recency-weighted current level becomes w(g)=g^2/(g+5.8) instead of g, so thin
# evidence counts for little and a 1-game cameo can no longer drag a demonstrated level to a cliff.
# w: 0->0 · 1->0.147 · 2->0.513 · 3->1.02 · 5->2.32 · 8->4.64 · 12->8.09 · 22->17.41. ONE curve, both
# directions: it takes Ladhams (1 game @ 97) DOWN off an over-price and the cold-cameo crash (Jamarra) UP.
# Env-gate RL_DAMP (default ON); RL_DAMP=0 => w=g => byte-exact base. Kill-switch, G-ATTR-separable.
# Owner constraint (reported, only APPROXIMATELY met): w(1)~=w(0)~=0 — the 0->1 jump is cut 6.8x but
# w(1)=0.147, NOT zero: the inversion is shrunk, not eliminated (census item 88). SMOOTH THE AVERAGES,
# NOT THE PRICE (R99.4): this touches _lvlcurr only; the convex pricing curve is untouched.
_DAMP=os.environ.get('RL_DAMP','1')!='0'                      # kill-switch (G-ATTR separability): RL_DAMP=0 => w=g => byte-exact base. Declared exception, not a dial.
_DAMP_K=5.8                                                   # PINNED (R100.11 item 3): in-code constant, no os.environ.get on a board-changing dial. Was os.environ.get('RL_DAMP_K','5.8').
def _wg(gm): return (gm*gm/(gm+_DAMP_K)) if _DAMP else float(gm)
# ==== EVIDENCE WEIGHT — FOUR REGIMES -> ONE CONTINUOUS OBJECT (RL_EVW; R98.4/R98.5, register item 65/124) ====
# The FOUR discrete evidence regimes are replaced by ONE continuous evidence weight keyed on ONE quantity:
#   E = career games SEEN (the T5 axis — trust saturates 40-70 games). From E:
#     th(E) = E^2/(E^2+K^2)  — TRUST / maturity, 0 -> 1, saturating (the production weight)
#     pw(E) = r + (1-r)(1-th) — the weight on the PEDIGREE PAR: 1 (no evidence: pedigree carries the row)
#             -> r=0.11 (the T5-measured n=4 residual, CI[0.04,0.17], EXCLUDES ZERO). It FADES, NEVER VANISHES
#             (R98.5) — replacing BOTH the nqual ramp (c=n/4) AND the PROVEN_N cliff (pedigree par -> 0), the
#             "same line of code" item 65 located. Item 65's warning honoured: the transition BETWEEN the thin
#             and established forms is also continuous (th blends the production reference), so we do not
#             "smooth the staircase and leave the cliff at the top of it".
# The 10-game bar dies because E counts games continuously (no games>=10 step). The exposure regime (expgate's
# n>=4 gate) dies via _expgate below. L-SMOOTH: smooth, monotone, no branch. R99.4: touches the LEVEL only
# (the convex price is untouched). Kill-switch RL_EVW=0 => the four discrete regimes => byte-exact base board:
# a DECLARED exception (the #85 RL_DAMP pattern), NOT a manifest dial, so config_sha256 is UNMOVED. Constants
# in-code (item 114): no os.environ.get on a board-changing dial.
_EVW=os.environ.get('RL_EVW','1')!='0'                        # kill-switch (G-ATTR separability): RL_EVW=0 => base byte-exact. Declared exception, not a dial.
_EVW_R=0.11                                                   # PINNED in-code: pedigree residual floor (T5 measured n=4 residual; CI[0.04,0.17]; R98.5 never 0).
_EVW_Q0=11.0; _EVW_QW=1.1                                     # PINNED: soft 10-game qualifying bar centre/width — a season's QUALIFYING weight q(g)=logistic((g-Q0)/QW), CONTINUOUS (no games>=10 step; ~4-game ramp 9->13). Steep enough that a sub-10-game season (a mid-career non-qualifier — the A8/Tsatas trap, whose best season is 7g) counts ~0 and production keeps carrying him.
_EVW_GK=0.55; _EVW_EST=3.6; _EVW_TAU=1.1                      # PINNED: pedigree-gate half-scale (unqualified -> 0), established centre (Lc->est), pedigree fade rate — in EFFECTIVE-QUALIFYING-SEASON units.
def _ev_qual(p,Y):                                            # E_q: EFFECTIVE qualifying seasons (soft 10-game bar; the T5 evidence axis, seasons scale)
    return float(sum(1.0/(1.0+_math.exp(-(x['games']-_EVW_Q0)/_EVW_QW)) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y))
def _ev_rec(Eq):  return float(Eq*Eq/(Eq*Eq+_EVW_GK*_EVW_GK))        # recency trust Lo->Lc: 0 (unqualified: conservative career level) -> 1 (qualified: trust recent form)
def _ev_est(Eq):  return float(Eq*Eq*Eq/(Eq*Eq*Eq+_EVW_EST*_EVW_EST*_EVW_EST))  # established weight Lc->est: 0 (thin) -> 1 (proven), centred at ~PROVEN_N seasons
def _ev_pw(Eq):                                              # PEDIGREE-PAR weight: qualifying-gated, fading to the residual r by ~n=4 (T5)
    gate=Eq*Eq/(Eq*Eq+_EVW_GK*_EVW_GK)                       # ~0 for the unqualified (production carries them: A8/Tsatas) -> 1 as seasons qualify
    fade=_EVW_R+(1.0-_EVW_R)*_math.exp(-Eq/_EVW_TAU)         # the draft bar fades as real games pile up: reaches the residual r=0.11 by ~4 qualifying seasons (T5), NEVER 0 (R98.5)
    return float(gate*fade)
def _expgate(p,Y):                                            # EXPOSURE REGIME (regime 4): pole-recovery gate, smoothed
    ramp=min(1.0, cp._exposure(p,Y)/max(1e-9,POLE_RAMP*min(1.0,_playable(p,Y)/cp.SEASON)))   # D10: 22-bar can't exceed playable games
    if not _EVW: return 1.0 if _nqual(p,Y)>=PROVEN_N else ramp                                # BASE: hard n>=4 -> 1.0 gate
    b=_ev_est(_ev_qual(p,Y)); return ramp + b*(1.0-ramp)     # EVW: smooth — base ramp for the unproven, -> 1.0 as evidence establishes (no n>=4 step; the low-E pole stays exposure-gated)
def _lvlcurr(p,Y):                                            # steeper-recency CURRENT level (trend-aware; ==career avg for a flat player)
    ld=LDECAY_G[_ldg(MA.gfut(p))]                             # STEP-3 per-group recency decay
    rows=[(x['year'],x['games'],x['avg']) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y]
    tw=sum(_wg(gm)*ld**max(0,Y-yr) for yr,gm,_ in rows)       # FIX 1: small-sample damping w(g)=g^2/(g+5.8) (RL_DAMP)
    return float(sum(_wg(gm)*ld**max(0,Y-yr)*a for yr,gm,a in rows)/tw) if tw>0 else 0.0
def _par_prior(p,Y): return PR.par_at(MA.gfut(p),min(MA.effpk(p),cp.KMAX),min(max(PR.tenure(p,Y),1),6))
def eff_ten(p,Y,base):                                        # developmental tenure off a CONTEXT base; proven keeps base exactly
    if _nqual(p,Y)>=PROVEN_N: return base                     # proven: original tenure (each call site passes its own base)
    return max(base, cp._age_asof(p,Y)-18)                    # thin career: max(base, age-18); 18-19yo debut -> ==base (Delta=0)
def _est_core(p,Y,L_old,Lc):                                  # ESTABLISHED (pre-M1 twin): hold UP wobble, SHED DOWN — internals UNCHANGED
    ft=FLAT_TOL_G[_ldg(MA.gfut(p))]
    if Lc>=L_old: return L_old if (Lc-L_old)<=ft else Lc      # UP-side: hold (don't over-credit a wobble/one strong yr)
    drop=L_old-Lc
    if drop<=DOWN_TOL: return L_old                           # down-wobble (<=3): hold steady
    sw=float(np.clip((drop-DOWN_TOL)/5.0,0.0,1.0))            # smooth shed onset over drop 3->8 (no hard boundary)
    return (1.0-sw)*L_old+sw*Lc*_agemult2(cp._age_asof(p,Y),Lc-MA.REPL.get(MA.gfut(p),0.0))  # DECLINER SHED (kept in lock-step with _coreM1)
# NOTE (improver build, register item 134): the THREE improver legs — RL_EO2 (kill the _eo min()), RL_LSYM
# (L-SYMMETRY), RL_SAGE29 (the S_AGE 29-tail) — are wired into the LIVE path ONLY (_inferM1/_est/_S_AGE; the
# number ev() consumes is cp._lvl_eff=_inferM1). This DORMANT twin (_lvl_eff_core/_lvl_eff_infer/_est_core) is
# superseded and never bound/called, and structurally predates the M1/S_AGE up-branch (leg 2/3 have no home
# here); it is left byte-identical so all-switches-off stays byte-exact. Verified dead before the wire.
def _lvl_eff_core(p,Y):                                       # DORMANT twin of _coreM1 (superseded via the _inferM1 bind); kept in lock-step
    L_old=cp._lvl_eff_orig(p,Y)
    # OBITUARY (Leg A, iso evidence-fade build 2026-07-16; SSI/CORE rule 7 — delete, don't disable): the dead
    # `if not _EVW:` discrete-regime branch (the pre-EVW four regimes — n==0 cameo -> L_old · thin ramp c=n/4 ·
    # PROVEN_N n>=4 cliff -> _est_core) is DELETED here. It was UNREACHABLE: this whole `_lvl_eff_core` twin is
    # DORMANT — never bound or called (ev() consumes cp._lvl_eff=_inferM1 -> _coreM1; see :210-214, "Verified
    # dead before the wire"). The LIVE RL_EVW=0 byte-exact base path survives untouched in _coreM1 (:375). No
    # output moves (the function is never invoked). Resurrection ref: git show <pre-LegA base>:_merged_recover.py.
    Lc=_lvlcurr(p,Y); Eq=_ev_qual(p,Y)                        # EVW: one continuous quantity E_q spans all four regimes
    Lrec=L_old + _ev_rec(Eq)*(Lc-L_old)                       # conservative -> recency, by qualification
    prod=(1.0-_ev_est(Eq))*Lrec + _ev_est(Eq)*_est_core(p,Y,L_old,Lc)  # recency/thin -> established, by evidence
    return (1.0-_ev_pw(Eq))*prod + _ev_pw(Eq)*_par_prior(p,Y)  # pedigree hump fades to residual, never vanishes
# UPSIDE FADE 2026-06-30 (GENTLER, candidate): elapsed-opportunity-gated fade of the pedigree/upside credit toward the
#   floor at demonstrated production. Credit target = realised forward ceiling surface E[fwdPeak](dL=ceiling-bar, year N),
#   kernel-smoothed from data. Keys on years-since-draft x exposure (NOT nq); young yr1-2 + first-yrs untouched (eo=0);
#   rising/at-production players unaffected (T=L0). Only ever pulls DOWN. See UNEARNED_UPSIDE_SCOPE_2026-06-30.md.
_UP_DLX=[-30.0,-20.0,-10.0,0.0,10.0]; _UP_NY=[3.0,4.0,5.0,6.0]
_UP_S=[[34.,45.,56.,67.,76.],[22.,33.,46.,59.,71.],[12.,22.,36.,51.,65.],[6.,14.,28.,44.,59.]]
def _upS(dL,N):
    dL=float(np.clip(dL,-30,10)); N=float(np.clip(N,3,6))
    col=[float(np.interp(dL,_UP_DLX,row)) for row in _UP_S]
    return float(np.interp(N,_UP_NY,col))
def _eo(p,Y):                                                 # elapsed-opportunity weight = years-since-draft x exposure (NOT nq)
    d=cp.debutyr(p); N=Y-d+1
    yrw=float(np.clip((N-2)/4.0,0.0,1.0))                     # 0 at yr<=2 (young/first-yrs untouched) -> 1 by yr6
    gm=sum(x.get('games',0) for x in p['scoring'] if (d-1)<x['year']<=Y)
    exp=float(np.clip(gm/(14.0*max(N-1,1)),0.0,1.0))         # fraction of ~14-game/yr opportunity actually taken
    return yrw*exp
def _lvl_eff_infer(p,Y):
    L0=_lvl_eff_core(p,Y); eo=_eo(p,Y)
    if eo<=0.0: return L0
    avs=[x['avg'] for x in p['scoring'] if x.get('games',0)>=6 and (cp.debutyr(p)-1)<x['year']<=Y]
    if not avs: return L0
    bar=MA.REPL.get(MA.gfut(p),0.0)-3.0; N=Y-cp.debutyr(p)+1
    T=min(L0, max(_upS(max(avs)-bar,N), _lvlcurr(p,Y)))       # GENTLER: floor at demonstrated production; keep realised upside
    return (1.0-eo)*L0+eo*T
def _feat_infer(p,Y):
    oh=[0.0]*len(cp.GROUPS); oh[cp.GIDX[MA.gfut(p)]]=1.0
    ep=min(MA.effpk(p),cp.KMAX); age=cp._age_asof(p,Y)
    ten=eff_ten(p,Y, max(0,Y-(cp.debutyr(p)-1)))             # base = original _feat tenure
    return oh+[np.log(ep), cp._exposure(p,Y), ten, cp._lvl_eff(p,Y), age]
# (inference rebind deferred to AFTER the isotonic guard builds on ORIGINAL features -> proven-flat stays Delta=0)
def b6(p,Y=2026):
    MA.BASE_REF=MA.AGE_REF=Y; MA._pe_clear()
    with contextlib.redirect_stdout(io.StringIO()): b=np.asarray(cp.cond_prior_band(p,cm,Y))
    return np.append(b,max(float(q97m.predict(np.array([cp._feat(p,Y)]))[0]),b[4]))
def price6(p,bb,Y=2026):
    sav=dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g]=sav[g]-rd.REPL_DROP.get(g,0)
        MA.BASE_REF=MA.AGE_REF=Y; MA._pe_clear()
        with contextlib.redirect_stdout(io.StringIO()): return float(dp.SCALE_DIST*_det_dot(WQ6,[dp.v_at_peak(p,float(L),'bal') for L in bb]))   # DETERMINISM FIX: order-fixed dot (was np.dot -> BLAS, CPU-dependent)
    finally: MA.REPL.update(sav)
def recover(perf,par): return float(np.clip(np.interp(perf/max(1.0,par),RECX,RECY),0,1))
def synth(pk,avg,pos,nyr=2): return {'player':'s','pos':GRPPOS.get(pos,midpos),'pick':float(pk),'year':2023,'dob':'2005-03-01','type':'ND','scoring':[{'year':2024+i,'games':18,'avg':float(avg)} for i in range(nyr)],'_pos_now':None,'_futpos':None}   # DPP STRIP: single-position synth (gfut falls back to bnow=pos)
_POLE={}
def par_pole(pos,pk,T):
    k=(pos,int(min(pk,cp.KMAX)),int(min(max(T,1),6)))
    if k not in _POLE: sp=synth(k[1],PR.par_at(*k),pos); _POLE[k]=price6(sp,b6(sp))
    _SCALE={'MID':1.19,'GEN_FWD':0.93,'KEY_FWD':0.95,'GEN_DEF':1.08,'KEY_DEF':1.05,'RUC':1.13}  # STEP3-B: principled re-level (trajectory-integrated pole / 2yr synth); piece-2 SHAPE kept, LEVEL rescaled
    return _POLE[k]*_SCALE.get(pos,1.0),PR.par_at(*k)
def raw_ev(p,Y=2026):
    pr=price6(p,b6(p,Y),Y); pos=MA.gfut(p); pk=MA.effpk(p); T=min(max(PR.tenure(p,Y),1),6)
    et=min(max(eff_ten(p,Y, PR.tenure(p,Y)),1),6)                                     # STEP1: developmental tenure off original PR.tenure base
    po,par=par_pole(pos,pk,T); a=MA.age(p)
    wage=0.0 if pos=='RUC' else float(np.clip(1-((a or 21)-20)/6,0,1))
    tfade=float(np.interp(et,[1,2,3,4,5,6],[1.00,0.76,0.40,0.16,0.05,0.05]))          # pole-fade by DEVELOPMENTAL tenure
    expgate=_expgate(p,Y)                                                             # EXPOSURE REGIME (regime 4): smoothed (was 1.0 if nqual>=4 else exposure/POLE_RAMP ramp); RL_EVW=0 => base gate
    w=wage*tfade*expgate
    perf=cp._lvl_wt(p,Y)                                  # WEIGHTED games x recency level (RL_RECENCY_DECAY), not flat best-3
    return pr+w*recover(perf,par)*max(0.0,po-pr)
# ===== (3) ISOTONIC PICK GUARD: per pos, monotone non-increasing in pick at par; correction factor =====
# ==== LEG A — iso_corr EVIDENCE-FADE + ISO MONOTONIZATION (RL_ISOFADE; item 132, spec §3 Leg A) ====
# (a) MONOTONIZE the multiplier: iso_corr = iso/raw is a monotone-non-increasing NUMERATOR over a
#     NON-monotone denominator, so the RATIO is non-monotone — the Newcombe trough (pk19 0.882 < pk34
#     1.000). Re-apply the house isotonic-non-increasing instrument to the MULTIPLIER itself, so no later
#     pick carries a higher multiplier than an earlier one. Conserving (per-pos SigmaD~=0), two-directional.
# (b) FADE per REAL player on the v2.10 evidence weight w=E_q (iso_eff below): full at zero evidence (the
#     pick IS the information; V0 at Y=debutyr-1 has E_q=0 -> unchanged BY CONSTRUCTION), dissolving to 1.0
#     as evidence saturates. DECLARED kill-switch, not a manifest dial: RL_ISOFADE=0 => original table +
#     plain iso_corr at every site => v2.10 board 790136a3 byte-exact (config_sha256 UNMOVED).
_ISOFADE=os.environ.get('RL_ISOFADE','1')!='0'               # kill-switch (G-ATTR separability): RL_ISOFADE=0 => v2.10 byte-exact. Declared exception, not a dial.
_ISOFADE_TAU=_EVW_TAU                                         # =1.1: THE fade parameter — the pedigree-fade family rate (_ev_pw, :186-189) in effective-qualifying-season units; iso uses the residual-0 member exp(-w/tau).
PICKS=list(range(1,71)); ISO={}
for pos in ['MID','GEN_FWD','KEY_FWD','GEN_DEF','KEY_DEF','RUC']:
    raw=np.array([raw_ev(synth(pk,PR.par_at(pos,min(pk,cp.KMAX),4),pos)) for pk in PICKS])
    iso=IsotonicRegression(increasing=False).fit_transform(PICKS,raw)        # monotone non-increasing in pick#
    ISO[pos]=(np.array(PICKS),np.maximum(iso,raw*0)+ (iso-raw>=0)*(iso-raw))  # iso is the guarded floor; correction additive where iso>raw
    fs=iso/np.maximum(raw,1e-6)                                                # multiplicative correction (>=1 where shallow under-priced)
    if _ISOFADE: fs=IsotonicRegression(increasing=False).fit_transform(PICKS,fs)   # LEG A (a): monotonize the MULTIPLIER (the ratio is non-monotone even though the numerator is) — kills the Newcombe trough
    ISO[pos]=(np.array(PICKS), fs)
def iso_corr(pos,pk): xs,fs=ISO[pos]; return float(np.interp(min(pk,70),xs,fs))
def iso_eff(p,Y=2026):                                        # LEG A (b): per-REAL-player EFFECTIVE iso — the pick tax faded on the v2.10 evidence weight w=E_q
    base=iso_corr(MA.gfut(p),MA.effpk(p))
    if not _ISOFADE or not _isreal(p): return base            # switch off, or a synth (structural scaffold; zero-evidence convention) => raw/monotonized table, unfaded
    return 1.0+(base-1.0)*_math.exp(-_ev_qual(p,Y)/_ISOFADE_TAU)   # full at w=0 (V0 unchanged by construction) -> 1.0 as evidence saturates (residual-0 member of the pedigree-fade family)
for _pp in ['MID','GEN_FWD','KEY_FWD','GEN_DEF','KEY_DEF','RUC']:   # STEP1: FREEZE pole table on ORIGINAL features
    for _pk in range(1,int(cp.KMAX)+1):                            #   (pole = pick-side; untouched until step 2-4)
        for _T in range(1,7): par_pole(_pp,_pk,_T)
# ==== M1 + v7-asc (BAKE CANDIDATE v2, D7 02/07/2026 — Luke-ruled config; NOT baked until Luke's bake word) ====
# M1 transplanted VERBATIM from the verified matrix-builder prototype (s4_matrix_M1v7.py; read-pass pack
# session_2026-07-02/readpass_pack_M1v7_8aed420a.md). M1 refines ONLY the up-branch of the level core:
# a proven player earns S_M1 of a current-over-recency gap when the gap >= TOL_M1 AND a recent season
# (within WIN yrs, >= G_ADQ games) sits above the recency level; the down-branch (DOWN_TOL shed) and the
# thin-career par-prior blend are byte-identical to _lvl_eff_core. v7 age-scales the q97 tail (asc) —
# REAL store players only: the ISO/pole tables above are frozen on ORIGINAL features/bands, and gate
# synths (B6 ramp) keep the original band.
# v7-cB DELETED 02/07/2026 (Luke-ruled, D7 — deleted, not disabled): the upper-quantile band compression
# cB = 0.47*clip((effs-1)/3,0,1) on bb[3]/bb[4] is GONE, with its _effs feed (no other consumer).
# Rationale: indiscriminate markdown (2020-cohort Spearman(value,delta) = -0.024, p=0.87 — no quality
# signal), the Curtis squeezer (Curtis -195/-14.4%, Ward -324/-19.6% — D5 term table). Obituary:
# BOARD_LAYERS_OBITUARY.md (ENGINE-TERM DELETIONS). Resurrection ref:
#   git show 0806d90:engine/rl_after/_merged_recover.py   (the D4 candidate, the last commit carrying cB)
TOL_M1=5.0; G_ADQ=12; WIN=2; S_M1=0.46
# v2.9 L3: s(age) breakout-persistence slope replaces the flat S_M1 in the proven-riser up-branch (gate RL_AGE,
# default ON; RL_AGE=0 ⇒ flat 0.46 ⇒ base byte-exact). Curve = the l7hinr s(age) breakout persistence; clip to
# [0,1]; a None as-of age falls back to the flat 0.46. Verified: butters 6060→5997 (−1.04%, inside G-PEAK 2%).
_L3_AGE=os.environ.get('RL_AGE','1')!='0'
_L3_AX=[20,21,22,23,24,25,26,27,28,29,30,31]
_L3_AY=[0.915376,0.860795,0.789170,0.700837,0.599107,0.489589,0.377802,0.265858,0.150620,0.026915,0.0,0.0]
# ==== IMPROVER LEG 3 — THE S_AGE 29-TAIL (RL_SAGE29; register item 128, FEED = PR #88 residual_by_age.csv) ====
# The S_AGE age-persistence slope zeroes 29-year-olds (_L3_AY[age29]=0.026915 ~= the CSV's sage_engine 0.0269),
# but the MEASURED age-29 smoothed forward level is +0.3793 (n_raw=33, CI[0.208,0.534], ZERO EXCLUDED — item 127).
# Wire ONLY the age-29 knot to its measured value; the fade still reaches zero AT 30 (the age-30 knot 0.0 stays
# UNTOUCHED — the measurement validates the 30+ zero) and the curve stays continuous (piecewise-linear np.interp;
# 28=0.1506 -> 29=0.3793 -> 30=0.0, no discontinuity/cliff). Do NOT touch S_AGE anywhere else (one knot, one
# consumer _est). Declared kill-switch (the #85 RL_DAMP / #89 RL_EVW pattern), in-code: RL_SAGE29=0 => age-29
# knot 0.026915 => byte-exact base board.
_SAGE29=os.environ.get('RL_SAGE29','1')!='0'                  # kill-switch (G-ATTR separability): RL_SAGE29=0 => base byte-exact. Declared exception, not a dial.
_SAGE29_VAL=0.3793                                            # PINNED in-code: age-29 smoothed forward level (PR #88 residual_by_age.csv, s_real @ age 29; CI[0.208,0.534])
_L3_AY_EFF=_L3_AY[:9]+[(_SAGE29_VAL if _SAGE29 else 0.026915)]+_L3_AY[10:]   # index 9 == age 29 (29-tail wired); indices 10,11 == age 30,31 (0.0) UNTOUCHED
def _S_AGE(a): return float(np.clip(np.interp(a,_L3_AX,_L3_AY_EFF),0.0,1.0)) if a is not None else 0.46
def _radq(p,Y,Lo): return any(x['games']>=G_ADQ and x['avg']>Lo for x in p['scoring'] if Y-WIN<x['year']<=Y and (cp.debutyr(p)-1)<x['year'])
# ==== IMPROVER LEG 2 — L-SYMMETRY WIRED (RL_LSYM; register item 108, spec = acceptance L-SYMMETRY) ====
# owner (item 108, verbatim): "Risers should have the same smoothing/ramping. And you should have to have the
# same drop for the engine to think you're declining as a rise for it to think you're rising." The base _est
# up-branch has THREE asymmetries vs the decliner shed (acceptance L-SYMMETRY.asymmetry_corrected):
#   (1) UNEQUAL BAR — a rise needs gap>=TOL_M1(5.0); a decline needs drop>DOWN_TOL(3.0). => use the SAME bar
#       DOWN_TOL both sides (no new constant).
#   (2) THE _radq GAMES-TEST — a rise additionally needs a 12-game season above the old level; a decline has NO
#       games test at all. => DROP _radq from the rise gate.
#   (3) CLIFF vs RAMP — fail either gate and the WHOLE improvement is DELETED (hard step to Lo); the decline is a
#       SMOOTH onset ramp sw=clip((drop-DOWN_TOL)/5,0,1). => give the rise the SAME smooth ramp.
# Symmetric up-branch: Lo + sw*s*gap  ==  (1-sw)*Lo + sw*(Lo+s*gap), mirroring the decline Lo + sw*(Lc*agemult2-Lo)
# term-for-term (same DOWN_TOL bar, same 5-pt onset ramp; s=_S_AGE is the up-side form/age persistence fraction,
# the analog of agemult2 — L-SYMMETRY corrects the BAR/RAMP/games-test, the S_AGE fraction is leg 3's territory).
# L-SMOOTH: continuous at gap=DOWN_TOL (sw=0 -> Lo). RL_LSYM=0 => the hard TOL_M1+_radq step => byte-exact base.
_LSYM=os.environ.get('RL_LSYM','1')!='0'                     # kill-switch (G-ATTR separability): RL_LSYM=0 => base byte-exact. Declared exception, not a dial.
def _est(p,Y,Lo,Lc):                                          # ESTABLISHED level: M1/L-SYMMETRY up-credit + decliner shed (the evidence weight gates ENTRY, never these thresholds)
    if Lc>=Lo:
        s=(_S_AGE(cp._age_asof(p,Y)) if _L3_AGE else S_M1); gap=Lc-Lo
        if not _LSYM:                                         # BASE: hard TOL_M1(5.0) bar + _radq games-test; fail EITHER => whole rise DELETED to Lo
            return (Lo+s*gap) if (gap>=TOL_M1 and _radq(p,Y,Lo)) else Lo
        if gap<=DOWN_TOL: return Lo                           # L-SYMMETRY: same bar as the decline (DOWN_TOL), NO games-test
        sw=float(np.clip((gap-DOWN_TOL)/5,0,1)); return Lo+sw*s*gap   # same smooth onset ramp as the decliner shed (no hard delete)
    drop=Lo-Lc
    if drop<=DOWN_TOL: return Lo
    sw=float(np.clip((drop-DOWN_TOL)/5,0,1)); return (1-sw)*Lo+sw*Lc*_agemult2(cp._age_asof(p,Y),Lc-MA.REPL.get(MA.gfut(p),0.0))
def _coreM1(p,Y):
    Lo=cp._lvl_eff_orig(p,Y)
    if not _EVW:
        # ---- BASE: the four discrete regimes (RL_EVW=0 => byte-exact base board) ----
        # D10 n==0 first-evidence f1 credit; multi-year n==0 (e.g. Tsatas: 4 list-years, no 10-game season)
        # keeps the exposure-shrunk Lo path (injecting the 75%-par-prior n=1 asymptote was measured +940 on the
        # Luke-ruled Tsatas A8 anchor and REJECTED). n>=4 established (_est); 1..3 thin ramp c=n/4.
        n=_nqual(p,Y)
        if n==0:
            if Y!=INPROG_Y or any(x['games']>0 and x['year']<Y and (cp.debutyr(p)-1)<x['year'] for x in p['scoring']): return Lo
            gy=sum(x['games'] for x in p['scoring'] if x['year']==Y and (cp.debutyr(p)-1)<x['year'])
            f1=min(1.0, gy/max(1e-9,10.0*SEASON_FE))
            if f1<=0.0: return Lo
            return (1.0-f1)*Lo + f1*((1.0/PROVEN_N)*_lvlcurr(p,Y)+(1.0-1.0/PROVEN_N)*_par_prior(p,Y))
        Lc=_lvlcurr(p,Y)
        if n>=PROVEN_N: return _est(p,Y,Lo,Lc)
        c=n/PROVEN_N; return c*Lc+(1-c)*_par_prior(p,Y)
    # ---- CONTINUOUS EVIDENCE WEIGHT (default): ONE evidence quantity E_q spans all four regimes (item 65) ----
    # 10-game bar dissolved (E_q counts qualifying seasons continuously) · nqual ramp + PROVEN_N cliff replaced
    # by the production blend (Lo->Lc->est) + pedigree weight pw(E_q); the thin->established transition is
    # continuous so no cliff is left "at the top of the staircase". Unqualified (E_q~0: the A8/Tsatas trap)
    # stay on the conservative career level Lo — the base's production-carries protection, made continuous.
    Lc=_lvlcurr(p,Y); Eq=_ev_qual(p,Y)
    Lrec=Lo + _ev_rec(Eq)*(Lc-Lo)                             # conservative career level Lo -> recency Lc, by qualification
    prod=(1.0-_ev_est(Eq))*Lrec + _ev_est(Eq)*_est(p,Y,Lo,Lc) # recency/thin -> established (M1/shed), by evidence
    return (1.0-_ev_pw(Eq))*prod + _ev_pw(Eq)*_par_prior(p,Y)  # + PEDIGREE PAR at weight pw(E_q): hump -> residual r=0.11, never vanishes (R98.5)
# ==== IMPROVER LEG 1 — `_eo` TWO-DIRECTIONAL (RL_EO2; register item 134, HANDOVER rev139 §improver) ====
# The elapsed-opportunity term _eo blends L0 toward the demonstrated-production target T. The base min(L0,T)
# caps T at L0 so the term can ONLY pull DOWN (the "Only ever pulls DOWN" note above) — it can mark over-priced
# players but never under-priced. Kill the min(), KEEP the term (rev139: "it is the only anti-flattery mechanism
# in the engine"): T = max(realised-forward-ceiling, recency-level), blended at weight eo. Now demonstrated
# production ABOVE L0 pulls UP and BELOW pulls DOWN — both expressible. L-SMOOTH: max/blend continuous, eo->0
# still returns L0, no new threshold. Declared kill-switch, in-code: RL_EO2=0 => min(L0,T) kept => byte-exact base.
_EO2=os.environ.get('RL_EO2','1')!='0'                        # kill-switch (G-ATTR separability): RL_EO2=0 => base byte-exact. Declared exception, not a dial.
def _inferM1(p,Y):
    L0=_coreM1(p,Y); eo=_eo(p,Y)
    if eo<=0: return L0
    avs=[x['avg'] for x in p['scoring'] if x.get('games',0)>=6 and (cp.debutyr(p)-1)<x['year']<=Y]
    if not avs: return L0
    bar=MA.REPL.get(MA.gfut(p),0.0)-3.0; N=Y-cp.debutyr(p)+1
    T=max(_upS(max(avs)-bar,N),_lvlcurr(p,Y))                 # demonstrated-production target (realised forward ceiling | recency level)
    return (1-eo)*L0+eo*(T if _EO2 else min(L0,T))            # LEG 1 (RL_EO2): kill the min() => two-directional (UP when T>L0, DOWN when T<L0)
def _v7(bb,p,Y):
    bb=list(bb); m=bb[2]; a=cp._age_asof(p,Y)
    asc=float(np.interp(a,[20,22,24,27],[1.0,0.76,0.58,0.40]))
    # W4 (RL_V7FORM): FORM-CONDITIONED tail retention — the #45 HARD FLAG made a lever. v7 compressed the q97
    # upside tail of EVERY demonstrated producer by AGE ALONE (flat 0.40 from 27; and it hit still-rising young
    # high-ceilings hardest: Serong +111 > Cameron +27 when toggled off). A player whose DEMONSTRATED level sits
    # clearly above his positional replacement (lcr) with at least one qualifying season keeps a share of his
    # tail: asc' = asc + (1-asc)*phi, phi = clip((lcr-4)/26,0,1)*min(nq,2)/2*V7W. Unproven speculation (lcr<=4
    # or nq==0) keeps the FULL age compression — the #43 audit measured young speculation correctly-to-OVER-
    # priced, so the relax is demonstration-earned only. RL_V7FORM=0 -> byte-exact v2.5 taper.
    if _W4V7 and asc<1.0:
        _lcr=_lvlcurr(p,Y)-MA.REPL.get(MA.gfut(p),0.0); _nq=_nqual(p,Y)
        if _lcr>4.0 and _nq>=1:
            _phi=float(np.clip((_lcr-4.0)/26.0,0.0,1.0))*min(_nq,2)/2.0*V7_FORM_W
            asc=asc+(1.0-asc)*_phi
    bb[5]=m+asc*(bb[5]-m); return bb
# STABLE-KEY REAL-membership (F1 fix 2026-07-05, Luke one-source rewire). The _REAL gate decides which players
# receive the engine's real-store layers (RUC prior cap :317/:492, v7 age-taper :198, B5 floor :552). It is now
# keyed on the STABLE player key, NOT id(p) -- so the layers fire regardless of which module instance or object
# copy is priced. (The shipped-board bug: rl_export exec'd a 2nd rl_model instance, so id(p) matched 0/805 and
# every real-store layer was silently dropped, over-pricing ~2/3 of the board.) Synths (no 'key') never match;
# copies carrying the same key resolve as real by construction. Keys verified non-null + unique across MA.data.
_REAL=set(p['key'] for p in MA.data)
def _isreal(p): return p.get('key') in _REAL
_b6_pre_v7=b6
def b6(p,Y=2026):
    bb=_b6_pre_v7(p,Y)
    if _isreal(p):
        try: return _v7(bb,p,Y)
        except Exception: return bb
    return bb
cp._lvl_eff=_inferM1; cp._feat=_feat_infer   # M1 level bind (was _lvl_eff_infer) + STEP1 inference feature path (q97m + ISO + POLE above used ORIGINAL features)
# ==== THE ABSENCE TERM (Option C, owner-ruled 2026-07-14) =========================================
# A missed season carries a PREDICTIVE, MULTIPLICATIVE penalty on a returning player's PROJECTED LEVEL
# (cp._lvl_eff = _inferM1, the number ev() consumes). It is NOT a phantom row (rejected — a phantom season
# carries 6x the evidential weight of six real games and LIFTS collapsed players) and NOT a threshold
# (R98.2 — the age curve is continuous). Magnitude = D2 R2's mean-reversion-adjusted FITTED age curve
# (session_2026-07-14/d2_recut, out_r2.txt; CORE rule 7 — the smooth curve, not the 3-bin cut that produced
# a FALSE prime-negative), expressed as a FRACTION of level (D2 R1: multiplicative is the point-estimate form;
# the CI admits additive — not overclaimed; L_REF=75 = the measured mean pre-absence level).
#   THE DOUBLE-CHARGE (the single most likely way to get this wrong): the recency decay ld^(Y-yr) ALREADY
#   ages a returner's last good season an extra year (D2 R3: mean -1.7 lvl pts charged; the measured truth
#   owed is -4.9 => the SHORTFALL is ~-3.2). We deliver ONLY the shortfall by netting the decay PER PLAYER —
#   L_nogap = _inferM1(gap-filled copy) via D2 R3's shift_out_gap (REUSED). The FULL-prior charge is the
#   shortfall below the multiplicative truth, never lifting: pen = max(0, L_base - L_nogap*(1-frac)); where
#   the decay already over-charges (Jamarra), pen = 0. R100.11: the prior is then WEIGHTED by pw(g) and the
#   level is L_abs = L_base - pw(g)*pen. At pw=1 (a fresh return) this equals the old min(L_base, L_nogap*
#   (1-frac)); as evidence accumulates pw(g)->0 and L_abs->L_base — the shed EMERGES from the arithmetic.
#   (The old build scaled frac by the fade INSIDE the min, so the L_nogap<L_base residual on a returner whose
#   post-return seasons are his best — Bailey Smith — never faded; weighting the whole prior fixes that.)
# Env-gate RL_ABSENCE (default ON); RL_ABSENCE=0 => byte-exact base. Kill-switch, G-ATTR-separable.
_ABSENCE=os.environ.get('RL_ABSENCE','1')!='0'               # kill-switch (G-ATTR separability): RL_ABSENCE=0 => byte-exact base. Declared exception, not a dial (the measurement ablation lever).
_ABS_L_REF=75.0                                              # PINNED (R100.11 item 3): D2 R1 mean pre-absence level (multiplicative base). Was os.environ.get('RL_ABS_LREF').
_ABS_CAP=0.20                                                # PINNED (R100.11 item 3): safety cap on the fraction (extrapolation beyond age 34). Was os.environ.get('RL_ABS_CAP').
# R100.11 EVIDENCE FADE (owner-ruled 2026-07-14, "Agree on Smith — evidence-fade"). The absence term is a
# PRIOR about an UNOBSERVED return; EVIDENCE DISSOLVES IT IN BOTH DIRECTIONS. The fade runs on EVIDENCE
# WEIGHT = games played since the most-recent return (g), NEVER seasons elapsed, and NO SCHEDULE FALLBACK
# (recurrence is an AVAILABILITY risk — _avail_hc / LTI; welding a clock into the LEVEL term double-charges
# the fragility). The prior enters as ONE pseudo-observation against the measured evidence-reliability curve
# w(g)=g^2/(g+K) (Fix 1's curve): its precision-blend weight is pw(g) = 1/(1+w(g)) = (g+K)/(g^2+g+K).
#   pw(0)=1 (fresh return carries the FULL prior) -> 0 as evidence accumulates (the prior dissolves).
# ONE continuous object: smooth, monotone, rational (g^2+g+K>0 for all g>=0). NO threshold, NO counter, NO
# branch (L-SMOOTH, acceptance_v1_13.json). Retires the schedule fade clip(1-npost/_ABS_FADE_N) and its
# >=10g season counter (both violated the ruling; the counter also violated L-SMOOTH).
_ABS_FADE_K=5.8                                              # PINNED (R100.11 item 3): evidence-fade scale K = Fix 1's measured w(g) scale (RL_DAMP_K, :162). In-code, no env read.
_ABS_AGE=[18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]
# D2 R2 mean-reversion-adjusted fitted effect (level points). The positive entries <age~20 are the DECLARED
# data-free kernel extrapolation (raw n~=0) and are clamped to 0 below — an absence is never a bonus.
_ABS_EFF=[3.65,0.28,-2.51,-4.49,-5.55,-5.73,-5.25,-4.46,-3.71,-3.25,-3.25,-3.85,-5.14,-7.10,-9.39,-11.29,-11.88]
def _abs_frac(age):
    if age is None: return 0.0
    a=float(np.clip(age,_ABS_AGE[0],_ABS_AGE[-1]))
    eff=float(np.interp(a,_ABS_AGE,_ABS_EFF))                 # fitted level-point effect (negative = penalty)
    return float(np.clip(max(0.0,-eff)/_ABS_L_REF,0.0,_ABS_CAP))
def _abs_gap(p,Y):
    """the MOST-RECENT mid-career calendar gap (a games==0 year after >=1 prior played season) whose
    return year <= Y. Returns dict(age_pre,ret,last,npost,gpost) or None. gpost = EVIDENCE WEIGHT (games
    played since the most-recent return, i.e. year>=ret) — the R100.11 fade input; npost (the retired
    schedule counter) is kept for the report only. Non-established players INCLUDED (law-4 coverage — the
    curve is extrapolated below the established base, DECLARED). Multiple separate absences are charged on
    the MOST RECENT return only, ONE penalty (law 5(a) assumption, DECLARED)."""
    d0=cp.debutyr(p)
    rows={x['year']:x['games'] for x in p['scoring'] if (d0-1)<x['year']}
    yrs=[y for y,gmv in rows.items() if gmv>0]
    if len(yrs)<2: return None
    lo,hi=min(yrs),max(yrs); tl=[(y,rows.get(y,0)) for y in range(lo,hi+1)]
    best=None; i=0
    while i<len(tl):
        if tl[i][1]!=0: i+=1; continue
        prior=[yy for (yy,g2) in tl[:i] if g2>0]; j=i
        while j<len(tl) and tl[j][1]==0: j+=1
        if prior and j<len(tl):
            ret=tl[j][0]
            if ret<=Y:
                last=prior[-1]; a=cp._age_asof(p,2026)
                age_pre=(a-(2026-last)) if a is not None else None
                npost=sum(1 for x in p['scoring'] if x['games']>=10 and x['year']>ret and (d0-1)<x['year']<=Y)  # RETIRED schedule counter — report only
                gpost=sum(x['games'] for x in p['scoring'] if x['games']>0 and x['year']>=ret and (d0-1)<x['year']<=Y)  # R100.11 EVIDENCE WEIGHT: games since return (return season is the first evidence)
                best=dict(age_pre=age_pre,ret=ret,last=last,npost=npost,gpost=gpost)   # keep LATEST qualifying gap
        i=j
    return best
def _abs_shift(p,last,ret):                                   # D2 R3 shift_out_gap: slide pre-gap seasons forward so the record is contiguous (gap filled)
    glen=ret-last-1                                           # shallow copy + rebuilt scoring (the level path never mutates q; cheaper than deepcopy in the walk-forward)
    q=dict(p); q['scoring']=[({**x,'year':x['year']+glen} if x['year']<=last else x) for x in p['scoring']]
    return q
_lvl_eff_preabs=cp._lvl_eff                                   # = _inferM1 (the projected level WITHOUT the absence term)
def _lvl_eff_abs(p,Y):
    Lb=_lvl_eff_preabs(p,Y)
    if not _ABSENCE or not _isreal(p): return Lb              # synths/lever-off: byte-exact (synths are gap-free anyway)
    gi=_abs_gap(p,Y)
    if gi is None or gi['age_pre'] is None: return Lb
    frac=_abs_frac(gi['age_pre'])                            # FULL age-curve prior (fade=1); the <20 clamp lives inside _abs_frac (owner-kept)
    if frac<=0.0: return Lb                                   # age<20 data-free clamp: no prior to fade
    g=gi['gpost']                                            # EVIDENCE WEIGHT: games played since the most-recent return (R100.11)
    fade=(g+_ABS_FADE_K)/(g*g+g+_ABS_FADE_K)                 # prior weight pw(g)=1/(1+w(g)), w(g)=g^2/(g+K); pw(0)=1 -> 0 on evidence. ONE continuous object; no threshold/counter/branch (L-SMOOTH)
    Lng=_lvl_eff_preabs(_abs_shift(p,gi['last'],gi['ret']),Y) # counterfactual no-absence level (decay netted per player)
    pen=max(0.0, Lb-Lng*(1.0-frac))                          # FULL-prior charge = shortfall below the multiplicative truth, NEVER lifting (=0 where the decay already over-charges, e.g. Jamarra). == base's (Lb-min(Lb,Lng*(1-frac))) at fade=1.
    return Lb-fade*pen                                       # the prior enters as ONE weighted term; weight pw(g)->0 on evidence => L->Lb. The shed EMERGES from the arithmetic (a returner at/above his old level ends uncharged) — no threshold, no "if level>=preabs" branch.
cp._lvl_eff=_lvl_eff_abs
# ==== M3 CLOCK-PIN PLUMBING (BAKE CANDIDATE v2, D7 02/07/2026 — design: session_2026-07-02/
# m3_design_proportional_tenure.md; the D4 backtest's monkeypatch hook inventory made first-class).
# While _M3PIN is on (ONLY inside _ev_m3's pinned evaluation of the in-progress season), the age/tenure
# CLOCK surfaces read as Y-1: cp._age_asof -1yr · MA.age -1yr · PR.tenure -1yr (floor 1) · _eo's
# years-since-draft N-1 (data window untouched) · _feat's explicit ten term re-based to Y-1. Evidence
# windows, era adjust, nseas/nqual and the M2-prorated exposure clock ALL stay at Y — the pin moves the
# CLOCKS only (using plain ev(p,Y-1) would re-prorate the decay channel M2 already prorates). With the
# pin OFF every wrapper is an identity passthrough — byte-exact by construction (verified in the D7 cut).
_M3PIN={'on':False}
M3_INPROG_Y=int(os.environ.get('RL_M3_INPROG_Y','2026'))      # the season in progress at the store cut
_m3_age_asof0=cp._age_asof; _m3_age0=MA.age; _m3_ten0=PR.tenure; _m3_eo0=_eo; _m3_feat0=cp._feat
def _m3_age_asof(p,Y):
    a=_m3_age_asof0(p,Y)
    return (a-1) if (_M3PIN['on'] and Y==M3_INPROG_Y) else a
def _m3_age(p):
    a=_m3_age0(p)
    return (a-1) if (_M3PIN['on'] and a is not None) else a
def _m3_ten(p,Y):
    t=_m3_ten0(p,Y)
    return max(1,t-1) if (_M3PIN['on'] and Y==M3_INPROG_Y) else t
def _eo(p,Y):                                                 # pin-aware rebind; _inferM1/_lvl_eff_infer read this global
    if not (_M3PIN['on'] and Y==M3_INPROG_Y): return _m3_eo0(p,Y)
    d=cp.debutyr(p); N=Y-d+1-1                                # N-1: the clock; data window stays at Y
    yrw=float(np.clip((N-2)/4.0,0.0,1.0))
    gm=sum(x.get('games',0) for x in p['scoring'] if (d-1)<x['year']<=Y)
    exp=float(np.clip(gm/(14.0*max(N-1,1)),0.0,1.0))
    return yrw*exp
def _m3_feat(p,Y):                                            # _feat's ten term uses raw Y-arithmetic, pin it explicitly
    f=list(_m3_feat0(p,Y))
    if _M3PIN['on'] and Y==M3_INPROG_Y:
        f[8]=eff_ten(p,Y, max(0,(Y-1)-(cp.debutyr(p)-1)))     # index 8 = ten (6 one-hots + logep, exposure, ten, lvl, age)
    return f
cp._age_asof=_m3_age_asof; MA.age=_m3_age; PR.tenure=_m3_ten; cp._feat=_m3_feat
# ==== W4 INTEGRATION CORE (2026-07-06, candidate) — FORWARD-VALUATION (present-vs-future) RECALIBRATION ======
# THE AXIS: every price integrates proj_from_peak's year-k contributions at weight 21/(1.15)^k over the forward
# horizon. The owner's ground truth (rev116/ADDENDUM): that flat weighting treats a moderate producer's year-9
# margin as being as certain as a proven elite's year-1 margin — so elite durable veterans are under-credited
# for CERTAIN present above-replacement MARGIN (+captaincy +durability), young fliers are under-credited for
# RUNWAY (the survivor reward is not priced forward into year 1), and the established mid-cohort is over-
# weighted between them. RECALIBRATION = a FORM-CONDITIONED (never age-keyed) weight W(k) on the year-k term:
#   PROVEN (nqual>=4):  W(k) = 1 + CRED·kpf_up·g(m)·dur·sh·c_near(k)  −  FADE·(1−g(m))·h_far(k)
#   then ×(1 − OVPX·ovpx)   [deep-pick GEN_FWD 41-70 over-optimism compress — the ONE owner-agreed #43 flag;
#                            MID 1-3 (2.09) deliberately NOT touched — stays FLAGGED for owner ruling]
# with m = Lc − REPL[pos] (the same conditioning variable as the #45 shed), g(m)=clip((m−6)/22,0,1),
# dur = games(Y−2..Y)/28 clipped, sh = 1−clip((Lo−Lc−3)/5,0,1) (decline gate, mirrors the shed switch),
# c_near = interp(k,[0,2,5],[1,1,0]) (present-tense, runway-independent — a short-horizon elite benefits most;
# captaincy rides inside every credited year via capt_prem), h_far = interp(k,[4,10],[0,1]) (the FUNDING leg:
# a moderate-margin established player's years 5+ carry washout risk the flat discount never charged).
# THE YOUNG LEG (L1c, 2026-07-08 rectification): the original W4 runway leg W(k)=1+YCRED·thin·yage·c_yng(k)
# is REPLACED (G-COHORT breach 142.4/140.8/131.7 vs hard 130, owner-upheld) by the EVIDENCE-CONDITIONED
# EXPECTED-RERATING CREDIT — see the L1c block below the raw_ev wrapper. Same kill-switch (RL_YOUNG); the
# two never stack (the old leg is deleted, not disabled).
# WIRING: MA.proj_from_peak is rebound to the W(k) version; the per-player context is set by a raw_ev wrapper.
# Synths carry no store key → context None → BYTE-EXACT delegation to the original (pole/ISO/gate/ruck-ceiling
# tables untouched). The wrapper binds BEFORE the V0 guard/curve builds, so the young credit flows into V0 →
# the year-1 anchors → the book's year-1 cohort (the no-arbitrage denominator). The V0 fit sees recalibrated
# inputs but stays a function of (pos, draft-age, pick) — D14a/b/c laws hold by construction.
# KILL-SWITCHES (per-lever attribution): RL_FWDRECAL (credit+fade) · RL_YOUNG (= the L1c evidence-conditioned
# expected-rerating credit since 2026-07-08; dial RL_YCRED_W) · RL_OVPX · RL_KPFFIX ·
# RL_V7FORM · RL_W4_RUC · RL_FORMDECL · RL_PVCFIT. ALL OFF ⇒ byte-exact baked v2.5.
# NOTE (2026-07-09, R3 remediation): every lever above DEFAULTS ON in the candidate EXCEPT RL_PVCFIT, which now
# DEFAULTS OFF — owner ruling R3 holds the W4 PVC fit OUT of the bake (see the RL_PVCFIT block below + R3 BAKE
# GUARD in rl_export.py). RL_PVCFIT only re-prices the pick side (board trade currency); it never touches player
# values, so the "ALL OFF ⇒ byte-exact baked v2.5" invariant is unaffected by its default.
_W4FWD=os.environ.get('RL_FWDRECAL','1')!='0'
_W4YNG=os.environ.get('RL_YOUNG','1')!='0'
_W4OVP=os.environ.get('RL_OVPX','1')!='0'
_W4KPF=os.environ.get('RL_KPFFIX','1')!='0'
_W4V7=os.environ.get('RL_V7FORM','1')!='0'
V7_FORM_W=float(os.environ.get('RL_V7_FORM_W','0.6'))     # demonstrated-producer tail retention share (v7 relax)
W4_CRED=float(os.environ.get('RL_W4_CRED','0.17'))        # proven-elite present-margin certainty credit (calibrated: Bont>=+10% with margin, pool net ~redistribution-neutral)
W4_KPFUP=float(os.environ.get('RL_W4_KPFUP','1.6'))       # KPF reward multiplier on the margin credit (low-REPL bar leverage)
W4_FADE=float(os.environ.get('RL_W4_FADE','0.60'))        # moderate-margin established far-year fade (the funding leg; age-ramped 23->26 so young proven keep their prime years)
W4_OVPX=float(os.environ.get('RL_W4_OVPX','1.0'))         # global scale on the deep-pick over-optimism compress (per-pos depths below)
W4_OVPX_D={'GEN_FWD':0.12,'GEN_DEF':0.09,'MID':0.07}      # #43-measured deep-pick (41-70) coverage excess: 2.14 / 1.70 / 1.55 -> partial, data-earned compress; smooth in pick 38->46, thin-career only. MID 1-3 (2.09) NOT touched (owner-flagged).
W4_KPFSH=float(os.environ.get('RL_W4_KPFSH','0.55'))      # established-KPF LOOSE-residual retention (the slice ABOVE all demonstration since the 2026-07-09 rebalance; was the whole residual)
# ==== KPF REBALANCE 2026-07-09 (pre-bake, owner-directed) — three KEY_FWD-scoped reshapes ==================
# OWNER RULING (verbatim): "slightly reducing the valuation of speculative key forwards, and slightly raising
# the valuation of production, especially the ones who are top tier scorers". Mechanisms, never per-player.
# (T1) DEMONSTRATION-KEYED RETENTION: the KPFFIX compress no longer treats the whole above-eP residual as
#   loose. The residual is SPLIT at eD = the engine's own price of the player's SUSTAINED DEMONSTRATED level
#   LD (mean of top-2 high-games seasons, 12-bar, in-progress prorated 12·fE — the D10 bar convention;
#   as-of-Y trailing, leak-free). The demonstrated-backed slice (eP..min(e,eD)) retains SH_DEM=0.70
#   (measured: established-KPF gap-recovery E[r]=0.68 pooled ages 24-30, 0.73 in the 6-10pt gap bin —
#   session_2026-07-09/kpf_rebalance/out/kpfsh_derivation2.json; the 30+ non-recovery is NOT charged here
#   because eD already prices LD through the engine's age/horizon machinery — DECLARED double-count
#   avoidance). The slice BEYOND all demonstration keeps the settled T1-shape 0.55 (measured loose:
#   E[max(fwd−LD,0)]=2.06 vs 4.2-4.6 beyond current). Never touches young/speculative (gates unchanged).
# (T2) TOP-TIER PRODUCTION REWARD (the concave regime, KEY_FWD cells): (i) the credit ramp for KEY_FWD keys
#   on dm = max(m, LD−REPL) — sustained demonstrated margin, so a recency-dipped top-tier scorer is not
#   zeroed — with the regime start/span rescaled by the measured KPF spread leverage (CV spread-ratio
#   6.57/4.17 = 1.575, the SETTLED #9 measurement that motivated KPFFIX): 10/1.575=6.35, 20/1.575=12.70.
#   (ii) a top-tier segment on the reward multiplier: kpfup(dm) = W4_KPFUP + KPFTOP·clip((dm−8)/16, 0, 1) —
#   the regime stays concave (saturating), the plateau rises for genuine top-tier scorers (saturation ≈ the
#   established-KPF 90th-pctile dm). (iii) PARTIAL-PROVEN KPF top-tier credit: a KEY_FWD with 2≤nqual<4 and
#   top-tier SUSTAINED demonstration earns the same credit scaled c=n/PROVEN_N (the engine's standing
#   partial-evidence convention), NO fade (F-YOUNG: the fade never reaches the young). One-season wonders
#   (nqual<2 or <2 high-games seasons) earn nothing — demonstration-earned only.
# (T3) SPECULATIVE TRIM: the L1c young credit's KEY_FWD cell intensity is scaled RL_YCRED_KPF=0.92 (slight,
#   owner's word; denominator cost measured and reported in the build artifacts). Lives on the RL_YOUNG lever.
# KILL-SWITCHES: T1+T2 ride RL_KPFFIX (=0 ⇒ legacy flat-0.55 compress shape? NO — =0 ⇒ NO compress and the
#   legacy m-keyed ramp + flat KPFUP, byte-exact to the pre-rebalance KPFFIX-off path); T3 rides RL_YOUNG.
#   ALL OFF ⇒ byte-exact baked v2.5 (re-verified this build).
W4_KPFSH_DEM=float(os.environ.get('RL_W4_KPFSH_DEM','0.70'))  # demonstrated-backed residual slice retention (measured gap-recovery)
W4_KPFTOP=float(os.environ.get('RL_W4_KPFTOP','0.4'))         # top-tier segment height on the KPF reward multiplier (calibrated to "slight" — the first-cut 0.8 moved elders +25-29%, over the owner's word)
_KPF_M0=float(os.environ.get('RL_W4_KPFM0','8.0'))            # KPF credit-regime start (pool regime 10; the #9 spread leverage 1.575 bounds the rescale at 6.35 — 8.0 is the calibrated-slight point)
_KPF_MS=float(os.environ.get('RL_W4_KPFMS','16.0'))           # KPF credit-regime span (pool 20; leverage bound 12.7; calibrated-slight 16)
def _kpf_LD(p,Y):
    """SUSTAINED RECENT demonstrated level as-of Y: mean of the top-2 high-games seasons WITHIN Y-3..Y
    (12-bar; the in-progress season qualifies at 12·fE — D10 proration). RECENCY WINDOW (calibration 2):
    career-ever top-2 let decade-old peaks hold a demonstration claim at 35 (first-cut Gunston/Walker/Darling
    +22-28%) — the owner's named producers all demonstrate WITHIN the window, and the windowed gap-recovery
    is the stronger measurement (E[r] 0.64 pooled / 0.78 ages 24-30 vs 0.43 unwindowed — derivation3 artifact).
    None with <2 qualifying seasons (one-season wonders earn no demonstration claim). Leak-free: scoring ≤ Y.
    FORK-v (R-v = exclude-and-extend, cap +2): for a register out-name the injured 2026 season is a NUKED
    season — excluded from the top-2 selection and the window extended back year-for-year (cap +2) so the KPF's
    demonstrated level rests on his HEALTHY seasons, not the injury (A-DARCY's KPF-speculative locus can't be
    clipped by the availability locus — enforced by construction). If <2 healthy seasons survive even the
    extended window, FALL BACK to counting-against (original window) and REPORT (_KPF_LD_FALLBACK)."""
    _nuke=set()
    if _AVAIL_ON:
        _st=_AVAIL_STATE.get(p.get('key'))
        if _st and _st.get('out'): _nuke={2026}                # the injured current season (register-flagged)
    _ext=min(2,len(_nuke)); _lo=Y-3-_ext                        # extend back year-for-year, capped +2
    ls=sorted((a*REF/era.get(y,REF) for y,a,gg in ((x['year'],x['avg'],x.get('games',0)) for x in p['scoring'])
               if _lo<=y<=Y and y not in _nuke and gg>=12.0*(_fEy(Y,p) if y==Y else 1.0)),reverse=True)
    if len(ls)>=2: return float(np.mean(ls[:2]))
    if _nuke:                                                  # fork-v fallback: exclusion left <2 healthy seasons
        _KPF_LD_FALLBACK.add(p.get('key'))
        ls0=sorted((a*REF/era.get(y,REF) for y,a,gg in ((x['year'],x['avg'],x.get('games',0)) for x in p['scoring'])
                    if Y-3<=y<=Y and gg>=12.0*(_fEy(Y,p) if y==Y else 1.0)),reverse=True)
        return float(np.mean(ls0[:2])) if len(ls0)>=2 else None
    return None
_W4CTX={'on':None}
def _w4_ctx(p,Y):
    """Per-player form context for the recalibrated projection; None => byte-exact original path."""
    if not (_W4FWD or _W4OVP) or not _isreal(p): return None   # L1c: RL_YOUNG no longer routes through the W(k) context (its credit lives on raw_ev, below)
    pos=MA.gfut(p); n=_nqual(p,Y); a=cp._age_asof(p,Y)
    ctx={'pos':pos,'ep':float(MA.effpk(p)),'n':n,'E':_ev_qual(p,Y)}   # LEG B: per-player evidence weight E for the un-compress map (sites 1-3; flat into projected years — no future store seasons)
    # Part-2 return haircut (RL_LTI_RETURN): apply the derived, net-of-aging return-season dip at the return
    # season k = ret_year - BASE_REF (decays to zero the next season = single k). Section-A out-names only;
    # young/speculative already ship h=0 (set on the record). SEPARABLE from Part 1 (own column lti_return_hc).
    _rh=p.get('_lti_ret_hc',0.0)
    if _LTI_RETURN_ON and _rh>0:
        ctx['ret_hc']=float(_rh); ctx['ret_k']=int(p.get('_lti_ret_year',2027))-int(Y)   # k offset from THIS eval year (deterministic; not global BASE_REF)
    _kpf_reb=_W4KPF and pos=='KEY_FWD'                         # KPF REBALANCE T2 coordinates active
    _partial=False
    if _kpf_reb and 2<=n<PROVEN_N:                             # partial-proven KPF: top-tier sustained demonstration only
        _LDp=_kpf_LD(p,Y)
        if _LDp is not None:
            _dmp=max(_lvlcurr(p,Y)-MA.REPL[pos],_LDp-MA.REPL[pos])
            _partial=_dmp>_KPF_M0                              # below the regime start ⇒ byte-identical legacy thin path
    if n>=PROVEN_N or _partial:
        Lc=_lvlcurr(p,Y); Lo=cp._lvl_eff_orig(p,Y)
        m=Lc-MA.REPL.get(pos,0.0)
        g3=sum(x.get('games',0) for x in p['scoring'] if Y-2<=x['year']<=Y)
        if _kpf_reb:
            _LD=_kpf_LD(p,Y); dm=max(m,(_LD-MA.REPL[pos]) if _LD is not None else m)
            ctx['gm']=float(np.clip((dm-_KPF_M0)/_KPF_MS,0.0,1.0))   # sustained-demonstration ramp, KPF spread-rescaled regime
            ctx['kt']=float(np.clip((dm-8.0)/16.0,0.0,1.0))          # top-tier segment coordinate
            ctx['cw']=1.0 if n>=PROVEN_N else n/float(PROVEN_N)      # partial-evidence convention (c=n/4), credit only — fade stays proven-gated in _w4_W
        else:
            ctx['gm']=float(np.clip((m-10.0)/20.0,0.0,1.0))   # credit ramp starts at m=10: "only the best-of-the-best clearly above replacement" (owner); the m 10-20 mid-band earns partial credit and carries most of the fade
            ctx['cw']=1.0
        ctx['dur']=float(np.clip(g3/28.0,0.0,1.0))
        ctx['sh']=1.0-float(np.clip((Lo-Lc-DOWN_TOL)/5.0,0.0,1.0))
        ctx['fadew']=float(np.clip(((a if a is not None else 25.0)-23.0)/3.0,0.0,1.0))  # fade age-ramp 23->26: a YOUNG proven player's far years are his PRIME (durable-young selection signal), not washout risk — the funding cohort is the established 25-30 mid
        if _partial:                                          # a partial-proven KPF still carries his deep-pick coordinate (legacy else-branch behavior preserved)
            _d=W4_OVPX_D.get(pos)
            if _d: ctx['ovpx']=_d*float(np.interp(ctx['ep'],[38.,46.,99.],[0.,1.,1.]))
    else:
        # (L1c: the thin/yage runway fields are GONE with the old young leg; this branch now only carries
        # the deep-pick over-optimism compress coordinates)
        _d=W4_OVPX_D.get(pos)
        if _d:
            ctx['ovpx']=_d*float(np.interp(ctx['ep'],[38.,46.,99.],[0.,1.,1.]))
    return ctx
def _w4_W(k,ctx):
    W=1.0
    if _W4FWD and ctx.get('cw',0.0)>0.0:
            # KPF REBALANCE T2: kpfup(dm) = base + top-tier segment (KEY_FWD under RL_KPFFIX only); the
            # credit scales by cw (1.0 proven; n/4 partial-proven KPF). The FADE stays PROVEN-gated — the
            # funding leg never reaches a partial-proven young KPF (F-YOUNG).
            up=W4_CRED*((W4_KPFUP+W4_KPFTOP*ctx.get('kt',0.0)) if (_W4KPF and ctx['pos']=='KEY_FWD') else 1.0)
            W+=ctx['cw']*up*ctx['gm']*ctx['dur']*ctx['sh']*float(np.interp(k,[0.,2.,5.],[1.,1.,0.]))
            if ctx.get('n',0)>=PROVEN_N:
                W-=W4_FADE*(1.0-ctx['gm'])*ctx.get('fadew',1.0)*float(np.interp(k,[4.,10.],[0.,1.]))
    # (L1c: the old `elif _W4YNG` runway leg was here — DELETED 2026-07-08, replaced by the evidence-
    #  conditioned expected-rerating credit on raw_ev below; RL_YOUNG gates THAT, never both.)
    if _W4OVP and ctx.get('ovpx',0.0)>0.0:
        W*=(1.0-W4_OVPX*ctx['ovpx'])
    return max(W,0.05)
_proj_w4_0=MA.proj_from_peak
def _proj_w4(g,lp,a,cur,lens,g0=None,fut=None,pre_hc=0.0):
    ctx=_W4CTX['on']
    if ctx is None: return _proj_w4_0(g,lp,a,cur,lens,g0=g0,fut=fut,pre_hc=pre_hc)   # synths / lever-off: byte-exact original
    pa=MA.PEAK_AGE[g]; d=MA.LENS[lens]; cl=cur if cur else lp*MA.frac(a,pa); prod=0.0
    if g0 is None: g0=g
    if fut is None: fut=[(g,1.0)]
    for k in range(18):
        ag=a+k
        if ag>38 or MA.frac(ag,pa)<0.42: break
        lev=lp*MA.frac(ag,pa)
        if ag<=pa: lev=max(lev,cl)
        if k==0: lev=max(lev,cl)
        if k==0 and pre_hc>0 and MA.BASE_REF==2026 and MA.AGE_REF==2026: lev*=(1-pre_hc)  # RL_AVAIL present haircut L_p (was _b2hc)
        if _BOARD_PATH and k==ctx.get('ret_k',-1) and ctx.get('ret_hc',0.0)>0: lev*=(1-ctx['ret_hc'])   # Part-2 return-season haircut (BOARD-ONLY: the walk-forward book stays availability-free; single k -> decays next season)
        _E=ctx.get('E',0.0)                                          # LEG B sites 1/2 (wired W4 proven/ctx-on population)
        Wk=_w4_W(k,ctx)
        if k==0: prod+=Wk*MA.posval_uncomp(lev,g0,_E)*21/((1+d)**k)
        else: prod+=Wk*sum(w*MA.posval_uncomp(lev,gg,_E) for gg,w in fut)*21/((1+d)**k)
    if g in('KEY_FWD','KEY_DEF'): prod*=1.05
    runway=MA.clamp((25-a)/6.0,0,1); elite=MA.clamp((lp/MA.PEAK[g]-0.97)/0.30,0,1); prod*=(1+runway*elite*MA.PMAX)
    return prod
MA.proj_from_peak=_proj_w4
# The DEMONSTRATED-PRODUCTION FLOOR carries the same near-year certainty credit (proven branch only). Without
# this the credit is invisible exactly where the elder's certain present lives: for a still-elite veteran the
# lower band nodes resolve to max(proj, prod_floor) = the FLOOR, and an uncredited floor mutes the owner's
# durability-buffer ("his high floor is low-risk value the runway discount over-penalises — credit the margin").
# The floor is a <=3-year present-value, so h_far(k)=0 there by construction — the fade CANNOT reach it: a
# moderate player's certain demonstrated present is never faded, only his speculative far years are.
_prod_floor_w4_0=MA.prod_floor
def _prod_floor_w4(p,lens='bal'):
    ctx=_W4CTX['on']
    if ctx is None or ctx.get('n',0)<PROVEN_N or not _W4FWD: return _prod_floor_w4_0(p,lens)
    g=MA.bnow(p); a=MA.age(p); pa_=MA.PEAK_AGE[g]; cur=MA.level_now(p)
    if cur is None: return 0
    d=MA.LENS[lens]; H=MA.clamp((40-a)/3.0,1.0,3.0); prod=0.0; k=0
    while k<H:
        ag=a+k; wt=min(1.0,H-k)
        lev=cur*min(1.0, MA.frac(ag,pa_)/max(MA.frac(a,pa_),1e-6))
        if k==0 and p.get('_avail_hc',0)>0 and MA.BASE_REF==2026 and MA.AGE_REF==2026: lev*=(1-p['_avail_hc'])  # RL_AVAIL: register-driven present haircut (was _b2hc; R-B2HC retired)
        prod+=_w4_W(k,ctx)*wt*MA.posval_uncomp(lev,g,ctx.get('E',0.0))*21/((1+d)**k); k+=1   # LEG B site 3 (proven demonstrated-production floor)
    return MA.val(prod)
MA.prod_floor=_prod_floor_w4
# ==== L1c — EVIDENCE-CONDITIONED EXPECTED-RERATING CREDIT (2026-07-08 rectification build) ================
# WHY: G-COHORT (owner-worded, upheld 2026-07-08) breached on the W4 candidate — y4 142.4 / y5 140.8 /
# y6 131.7 vs hard 130, den = y1 57,558.5. Diagnosis: the engine prices year-1 on DELIVERED EVIDENCE only;
# the class's measured ride is +22% by y2 (top decile carrying most of it). Owner doctrine: no blanket lift —
# identify and pay the measured mechanism. THE LEVER (L1c): per cell (position × log-pick KERNEL × played/sat,
# pooling declared per rung in the committed census), the historical ONE-YEAR RE-RATING of the class at the
# year-1 anchor, ATTRITION AND BUSTS INCLUDED, measured on the CREDIT-OFF walk-forward book (one-shot,
# declared), is paid forward at fraction w = RL_YCRED_W (OWNER-RULED w=0.9, 2026-07-08; pre-ruling default was 0.7):
#     e' = e · (1 + w · max(R_cell, 0) · φ(g)),   φ(g) = (1 − g/G0)²  for g < G0 else 0
# KEYED ON EVIDENCE QUANTITY g = career games as-of Y — NEVER career-year: full at ZERO evidence (V0, day 0 —
# V0 IS raw_ev at debut−1 with g=0, so the credit flows into V0, the D14 V0 curve refit, the B5 floor basis,
# the sit-out blend and the y1 anchors by construction), fading smoothly to zero by G0=46 games (the census
# artifact: median cumulative games end-y3=37 / end-y4=54 for a normally developing player — ≈y3-4). C¹ at G0.
# CONTINUITY (owner law, BINDING): no cliff anywhere on pick-PVC → V0 → end-y1 → y2/3/4 — the multiplier is
# continuous in g (φ), in pick (kernel curve, log-pick interp), across the sat/played seam (s(g)=min(g/6,1)
# blend — no first-game step), and carries NO career-year key. D14 V0 laws (a/b/c) hold by construction: the
# V0 curve remains a function of (pos, draft-age, pick) fitted on credited inputs.
# TRAILING / LEAK-FREE (auditor: assert THIS by code reading): the table is keyed by evaluation year —
# _ycred_mult(p,Y) reads _YC_TAB[str(min(Y,TMAX))], and table_T was derived ONLY from classes C with
# C+2 ≤ T (derive_ycred.py, committed) — the credit applied at year T uses data ≤ T. Years before the first
# table (min 2 observable classes, 2007) earn ZERO credit — declared conservatism, leak-free.
# CLIP R ≥ 0: fix direction = raise year-1, NEVER cut young/survivors/denominator members; measured-negative
# stretches (GEN_FWD/played, RUC/sat — census tension report) are reported, not shipped as cuts.
# SCOPE: real in-curve (ND/RD) picked store players — synths carry no key and delegate byte-exact; the RUC
# prior cap (ASK1) still binds ABOVE the credited V0 where hot (declared: the cap is out-of-scope machinery;
# capped rucks keep the cap — visible in the Goad/Green named-player rows of the owner w-table).
# KILL-SWITCH: RL_YOUNG (existing family member, meaning re-pointed to L1c; the old runway leg is DELETED
# above, never stacked). RL_YOUNG=0 ⇒ multiplier is EXACTLY 1.0 ⇒ byte-exact; ALL-OFF ⇒ byte-exact v2.5.
# Table absent while RL_YOUNG=1 ⇒ HALT (halt-not-warn, guard-family behavior).
_YC_W=float(os.environ.get('RL_YCRED_W','0.9'))               # owner dial: fraction of the measured re-rating paid forward — OWNER-RULED 0.9 (2026-07-08, on the W-TABLE; 0.7 was the pre-ruling shipped default)
_YC_KPF=float(os.environ.get('RL_YCRED_KPF','0.92'))          # KPF REBALANCE T3 (2026-07-09): SLIGHT speculative-KPF trim — KEY_FWD cell intensity ×0.92 (owner's "slight"; F-YOUNG honored — no wipe; denominator cost measured in the build artifacts). Rides RL_YOUNG.
_YC_TAB=None; _YC_LGRID=None; _YC_G0=46.0; _YC_TMIN=2007; _YC_TMAX=2026
if _W4YNG:
    import json as _ycjson
    if not os.path.exists('ycred_table.json'):
        raise SystemExit('L1c HALT: RL_YOUNG is ON but ycred_table.json is absent — re-seed the workspace '
                         '(bootstrap.sh); the credit never silently no-ops.')
    _yc=_ycjson.load(open('ycred_table.json'))
    _YC_TAB=_yc['table']; _YC_G0=float(_yc['G0'])
    _YC_LGRID=np.log(np.array(_yc['grid_picks'],dtype=float))
    _YC_TMIN=min(int(t) for t in _YC_TAB); _YC_TMAX=max(int(t) for t in _YC_TAB)
def _ycred_games(p,Y):                                        # EVIDENCE QUANTITY: career games as-of Y (same debut window as _nqual)
    d0=cp.debutyr(p)-1
    g=float(sum(x.get('games',0) for x in p['scoring'] if d0<x['year']<=Y))
    # FORK-i (R-i, RULED ADVANCE — owner 2026-07-10, DECISIONS v90 §36; supersedes the §33 provisional pause).
    # The L1c clock keys on career GAMES, so an injured season adds ~0 and the clock would implicitly PAUSE
    # (the retired RL_LTI_CLOCK=pause). ADVANCE (the DEFAULT now) ages the clock by the expected (lost) games
    # during LTI windows, fading the young credit as if he had played — the owner viewed the pause-vs-advance
    # named table (O'Farrell -206, Gibcus -17; Darcy/Motlop/Flanders past G0, Δ0) and ruled advance. The flip is
    # this config default + the ruling-config assertion (ruling_config_check.py) that makes a paused bake fail.
    if _LTI_CLOCK=='advance' and _AVAIL_ON and Y>=2026:
        _st=_AVAIL_STATE.get(p.get('key'))
        if _st and _st.get('out'): g+=float(_st['L'])*float(cp.SEASON)
    return g
def _ycred_mult(p,Y):
    if not _W4YNG or _YC_TAB is None or not _isreal(p): return 1.0
    if p.get('type') not in ('ND','RD') or p.get('_pickless'): return 1.0
    pk=MA.effpk(p)
    if not pk: return 1.0
    g=_ycred_games(p,Y)
    if g>=_YC_G0: return 1.0                                  # evidence complete: expectation fully replaced by delivery
    T=int(Y)
    if T<_YC_TMIN: return 1.0                                 # trailing: <2 observable classes -> no credit (leak-free)
    row=_YC_TAB[str(min(T,_YC_TMAX))].get(MA.gfut(p))
    if row is None: return 1.0
    lp=float(np.log(min(max(pk,1),90)))
    Rs=float(np.interp(lp,_YC_LGRID,row['1'])); Rp=float(np.interp(lp,_YC_LGRID,row['0']))
    s=min(g/6.0,1.0)                                          # smooth sat->played blend over the first 6 games (no first-game cliff)
    R=max((1.0-s)*Rs+s*Rp,0.0)                                # clip >= 0 (fix direction; tension reported in the census)
    if MA.gfut(p)=='KEY_FWD': R*=_YC_KPF                      # T3 KPF REBALANCE: slight KEY_FWD cell-intensity trim (continuous — a pure scale introduces no cliff on any axis)
    phi=(1.0-g/_YC_G0)**2                                     # full at zero evidence; C1 landing at G0
    return 1.0+_YC_W*R*phi
_raw_ev_w4_0=raw_ev
def raw_ev(p,Y=2026):                                        # W4: context-setting wrapper (real players only; synths delegate clean) + L1c credit
    prev=_W4CTX['on']; ctx=_w4_ctx(p,Y); _W4CTX['on']=ctx
    prevE=MA._UNCOMP_E['cur']; MA._UNCOMP_E['cur']=(ctx['E'] if ctx is not None else 0.0)   # LEG B: thread E to the DELEGATED rl_model sites 4-6 (0 for synths/ctx-None -> byte-exact)
    try: return _raw_ev_w4_0(p,Y)*_ycred_mult(p,Y)           # L1c: ×1.0 exactly when RL_YOUNG=0 (byte-exact off-path)
    finally: _W4CTX['on']=prev; MA._UNCOMP_E['cur']=prevE
_B6PIN={'L':None}                                            # W4 KPF: band pin — collapse the forward band to one level (production-implied EFV probe)
_b6_pre_w4=b6
def b6(p,Y=2026):
    if _B6PIN['L'] is not None: return np.full(6,float(_B6PIN['L']))
    return _b6_pre_w4(p,Y)
def _kpf_prod_efv(p,Y,L=None):
    """The engine's own price of the player's DEMONSTRATED level: band pinned at _lvl_eff (same W4 context, so
    the margin credit survives — the compress removes only the band/prior excess above demonstrated output).
    L pins an alternative demonstrated level (KPF REBALANCE T1: the SUSTAINED level LD prices the eD split)."""
    _B6PIN['L']=cp._lvl_eff(p,Y) if L is None else float(L)
    try:
        with contextlib.redirect_stdout(io.StringIO()): return raw_ev(p,Y)*iso_eff(p,Y)   # LEG A site 1/6 (was iso_corr(gfut,effpk))
    finally: _B6PIN['L']=None
# ===== helpers for delist + staleness =====
def delisted(p): return bool(p.get('_retired')) or (p.get('_last_listed') is not None and p['_last_listed']<2026)
def draftval(p): return float(MA.PVC[min(MA.effpk(p),cp.KMAX)])
def bestlvl(p,Y=2026):
    s=[a*REF/era.get(y,REF) for y,a in [(x['year'],x['avg']) for x in p['scoring'] if x['games']>=6.0*(_fEy(Y,p) if x['year']==Y else 1.0) and x['year']<=Y]]   # D10: 6-bar prorated in-progress
    return max(s) if s else 0.0
def nseas(p,Y=2026): return sum(1 for x in p['scoring'] if x['games']>=6 and x['year']<=Y)   # unprorated career counter (harness/diagnostic callers)
def nseas_pro(p,Y=2026):                                      # D10: qualification judged against PLAYABLE games (6-bar -> 6*fE for the in-progress season)
    return sum(1 for x in p['scoring'] if x['year']<=Y and x['games']>=6.0*(_fEy(Y,p) if x['year']==Y else 1.0))
# ===== GAMES-RAMP SIT-OUT TREATMENT (D10 03/07/2026) — the retired-PVC anchor is PURGED =====
# Replaces the flat SITOUT_RETAIN x draftval anchor (obituary: BOARD_LAYERS_OBITUARY.md; derivation:
# session_2026-07-03/d10_ask2_derivation.md — harvest 2,465 complete-window still-listed cells 2004-2021,
# kernel eff-n>=35, busts=0).
#   V0(p) = raw_ev(p, draft year) x iso — the engine's LIVE zero-evidence pick+position start value
#     (Dean-below / Robey-above property). HELD through pre-season: tau=0 -> R=1, no penalty before a
#     season starts (Luke 2a).
#   R_SIT = retention of V0 for still-listed non-playing draftees, measured RELATIVE to the same-depth
#     all-draftee norm (the locked daEV-convention "0.76 form"), knots at end-of-season depths 1..6,
#     CONCAVE within-season accrual (the penalty prorates to season progress via tau'=(R/24)^1.5 —
#     Luke-signed OPTION A, D12 03/07/2026; SUPERSEDES the D10 linear form — Luke 2c-revised: a penalty
#     "should be slightly more generous as the sample is smaller"; 100% at R24/24, ~35% at halfway),
#     flat tail 6+.
#   LAM_SIT = measured evidence-credit blend toward the LIVE production path e_full (isotonic in games;
#     STRUCTURAL endpoints lam(0)=0, lam(prorated bar)=1 -> value CONTINUOUS at graduation: no cliff,
#     no game-6 jackpot — Luke 2b). Games read AT PACE (g/fE) against the prorated bar.
#   SCORING-AWARE through e_full: the production path prices actual output (Annable's 1g@40 is
#     information — Luke 2d). A lambda-side quality term was tested and NOT supported at finest
#     resolution (partial tau +0.04, non-monotone across q bins, n=364) — DECLARED, not wired.
#   POSITION BASIS preserved end-to-end: V0 and e_full both carry the band's position adjustment;
#     classes RUC/KPP/nonKPP for R_SIT only, with the RUC retention SHAPE pooled with KPP (thin bimodal
#     slice, n=270 cells) scaled to RUC's own measured d1-2 level x1.065 — DECLARED pooling.
# D13 ASK3 03/07/2026 — R_SIT (depth-only, per class, RUC-shape-pooled-with-KPP) is SUPERSEDED by the
# continuous log-pick x depth surface R_SURF below (obituary E4: BOARD_LAYERS_OBITUARY.md). The old table
# VIOLATED Luke's signed law (nonKPP rose d3->d5 .410->.437; KPP rose d5->d6 .253->.266 — a sitter gained
# value by sitting). Resurrection ref: git show af1fc6aa's _merged_recover.py. Old table (for the record):
#   R_SIT={'nonKPP':[.429,.404,.410,.432,.437,.424],'KPP':[.468,.380,.325,.278,.253,.266],'RUC':[.674,.547,.503,.472,.435,.435]}
# ===== RETENTION SURFACE (D13 ASK3) — re-derived at finest supported resolution =====
# R(cls, log-pick, depth) = kernel-smoothed sit-out realization r=O/V0 (winsor 2.0, Gaussian bw grown until
# eff-n>=35) / same-depth all-draftee daEV norm (per class; strips survivor selection, rises 0.44->1.11 w/
# depth), clip[.05,1], then ISOTONIC NON-INCREASING IN DEPTH at every pick (Luke's signed law: a sitter never
# gains value). R1: daEV(V0) denominator KEPT (position-blind dv WIDENED the KPP gap 0.065->0.079 -> numerator-
# driven, not pole-inflated: KPP V0/dv=0.90). R2: FIRES all classes (pick maxdev 0.13-0.21 > 0.05 ribbon) ->
# PICK-CONDITIONED. Derivation: session_2026-07-03/d13/d13_ask3_retention.md; scripts d13_derive.py.
# Knots = DIAGNOSTIC evaluation picks of the smooth surface (never derivation bins). Interp over log-pick + tau
# preserves depth-monotonicity (convex comb of non-increasing vectors). Deep KPP d4-6 pooled (thin, DECLARED).
R_SURF={'nonKPP':{5:[0.547,0.446,0.446,0.446,0.446,0.314], 15:[0.707,0.479,0.479,0.479,0.479,0.307], 30:[0.649,0.436,0.422,0.414,0.414,0.303], 50:[0.549,0.388,0.345,0.239,0.164,0.164]},
        'KPP':{5:[0.660,0.487,0.387,0.194,0.183,0.183], 15:[0.694,0.427,0.273,0.136,0.136,0.136], 30:[0.632,0.383,0.286,0.180,0.172,0.172], 50:[0.642,0.407,0.351,0.334,0.334,0.329]},
        'RUC':{5:[1.000,0.715,0.670,0.562,0.535,0.467], 15:[0.851,0.597,0.597,0.520,0.520,0.468], 30:[0.830,0.616,0.616,0.607,0.540,0.469], 50:[0.781,0.594,0.594,0.594,0.541,0.470]}}
_RS_KNOTS=[5,15,30,50]; _RS_LOGK=[np.log(k) for k in _RS_KNOTS]
# _BOARD_PATH: True on the live board render (present/forward valuation). The BACKTEST/WALK-FORWARD harnesses
# set g['_BOARD_PATH']=False after exec so Luke's D14 board-only laws (KPP retention floor O1 below; V0 curve
# further down) DO NOT touch the historical book (Luke's backtest exemption -> the walk-forward book reproduces).
_BOARD_PATH=True
def _dv_surf(cls,lp):                                        # depth vector (6) for a class at a given log-pick
    kn=R_SURF[cls]; return [float(np.interp(lp,_RS_LOGK,[kn[k][i] for k in _RS_KNOTS])) for i in range(6)]
def _R_surf(cls,pick,tau):                                   # interp over log-pick (knots) then over tau (0->1, depths 1..6, flat 6+)
    lp=np.log(min(max(pick,1),90)); dv=_dv_surf(cls,lp)
    # ==== D14 ASK2 (03/07/2026) — KPP RETENTION FLOOR (SIGNED OWNER OVERRIDE O1, Luke verbatim: "if it's lower,
    # it's carried so it can never be the lowest ... I can't see KPPs losing value for sitting at a faster rate
    # than non KPPs"). Wired KPP sit-out retention surface := pointwise MAX(KPP, nonKPP) at every (log-pick,depth).
    # Comparator = nonKPP ONLY (RUC EXCLUDED — own capped machinery; supervisor spec, stated to Luke pre-fire).
    # BOARD PATH ONLY (O1 scope). max() of two isotonic-non-increasing-in-depth vectors is non-increasing (re-
    # verified numerically in _v0_curve_assert). OWNER-SET where the floor binds, data-derived elsewhere. Governance:
    # docs/process/OWNER_OVERRIDES.md O1; obituary/registration BOARD_LAYERS_OBITUARY.md.
    if _BOARD_PATH and cls=='KPP':
        dvn=_dv_surf('nonKPP',lp); dv=[max(a,b) for a,b in zip(dv,dvn)]
    return float(np.interp(tau,[0,1,2,3,4,5,6],[1.0]+dv))
LAM_SIT=[0.0,0.160,0.493,0.547,0.547,0.816,1.0]
def _sitout_cls(pos): return 'RUC' if pos=='RUC' else ('KPP' if pos in ('KEY_FWD','KEY_DEF') else 'nonKPP')
# ==== ASK1 (D13 03/07/2026): RUC PRIOR CAP — cap the hot ruck band prior as a max V0/PVC ratio. Parameterised
# dial RL_RUC_PRIOR_CAP; DEFAULT 1.73 = the class's own ND-ruck median V0/PVC (Luke's inclination, D13 ASK1:
# "I'd be inclined to just cap ruck prior at the 1.73 median"). Sits at the raw_ev/band level (for RUC wage=0
# so raw_ev==the band price) so it flows into V0, the sit-out blend, the floor and the prior-dominated
# production path — NOT a display-stage V0 clamp (D12: Emmett's board value is blend-fed by the prior). Scope:
# REAL rucks only (synth ISO/POLE tables untouched). The pure prior V0 is capped unconditionally (min binds
# only when hot, V0/PVC>cap). The PRODUCTION leg is capped only in the PRIOR-DOMINATED regime — C*PVC < e_full
# <= V0_uncapped: hot prior AND production has NOT grown beyond the start value; any ruck who has demonstrated
# production above his (uncapped) start value (Sweet 2011, McAndrew 992, Xerri 5755, Grundy, Gawn, Marshall)
# is byte-exact. Derivation/ladder: session_2026-07-03/d13/d13_ask1_ruck_cap.md.
RUC_PRIOR_CAP=float(os.environ.get('RL_RUC_PRIOR_CAP','1.4'))   # BAKED default 1.73->1.4 (owner ruck-cap dial, v2.4 bake 2026-07-04; env override preserved)
# ==== W4 RUCK LEVER (folded from PR #44 verbatim + the owner-required SMOOTH YOUNG-RUCK HEADROOM) ============
# PR #44 core: the old lever capped a real ruck's PRODUCTION leg at a flat multiple of draftval (PVC = draft-pick
# capital), blending heterogeneous units. The swap: the production leg (ev() hook, prior-dominated regime) is
# capped at a ceiling DERIVED off ruck production instead of pick capital:
#   ceiling(p) = RUC_CEIL_HEAD * synthprice_RUC(bestlvl(p)) at the ruck-median slot RUC_CEIL_REFPK=72 — the
#   engine's own pricing of a STANDARDIZED developing ruck at the player's era-normalized peak production.
#   Pick-neutral, production-only, monotone non-decreasing. Thin-slice choice (declared): the ruck slice is
#   POOLED onto one pick-neutral production->$ curve (empirical kernel over live raw_ev was REJECTED —
#   age/tenure-contaminated, non-monotone, crushed thin prospects). NO-PRODUCTION FALLBACK: bestlvl==0 rucks
#   keep the prior cap (RUC_PRIOR_CAP x PVC). V0 draft-prior/floor SCAFFOLD byte-identical (PR #44 scope).
# W4 EXTENSION — YOUNG-RUCK HEADROOM as a SMOOTH function of pick x age (owner's wide-band objection to the
# audit's hard pk1-20 cell; #43 measured the young-ruck convexity coverage 0.61-0.73 = the one genuinely
# UNDER-priced young pocket, while RUC 21-40 is over (1.59) so the fade is OUT by pick ~30):
#   _ruc_head_mult(p) = 1 + YRH * interp(pk,[1,4,18,30],[0.7,1,1,0]) * clip((25-age)/4,0,1)
# applied to BOTH cap paths (production ceiling AND the no-production prior cap) so the fade has no cliff in
# pick, age, or the production/no-production seam. YRH dial: RL_RUC_YRH (default 0.35); RL_W4_RUC=0 -> byte-
# exact v2.5 ruck lever (1.4xPVC cap, no headroom).
_W4RUC=os.environ.get('RL_W4_RUC','1')!='0'
RUC_CEIL_HEAD=float(os.environ.get('RL_RUC_CEIL_HEAD','0.80'))  # headroom on the standardized production price for UNPROVEN exposure (PR #44 owner dial; lands Emmett in his stated 650-800)
RUC_CEIL_REFPK=float(os.environ.get('RL_RUC_CEIL_REFPK','72'))  # ruck-median effpk = the pick-neutral "representative ruck slot"
RUC_YRH=float(os.environ.get('RL_RUC_YRH','0.35'))              # young-ruck smooth headroom amplitude (W4; owner dial)
_RUCCEIL={}; _RUCCEIL_META={}
def _build_ruc_ceiling():                                     # pick-neutral production->$ curve: era-adj peak avg -> ruck price
    avs=list(np.linspace(15.0,150.0,46))
    def _sp(a):
        sp=synth(int(RUC_CEIL_REFPK),float(a),'RUC')
        with contextlib.redirect_stdout(io.StringIO()): return raw_ev(sp)*iso_eff(sp)   # LEG A site 2/6 (synth: iso_eff returns the monotonized table unfaded — structural scaffold)
    ys=[_sp(a) for a in avs]
    for i in range(1,len(ys)): ys[i]=max(ys[i],ys[i-1])     # enforce monotone non-decreasing (guard tiny pole wiggles)
    _RUCCEIL['grid']=(np.array(avs),np.array(ys))
    _RUCCEIL_META.update(refpk=RUC_CEIL_REFPK,head=RUC_CEIL_HEAD,grid_lo=float(ys[0]),grid_hi=float(ys[-1]),n_avg=len(avs))
def _ruc_head_core(pk,a):                                     # W4: SMOOTH young-ruck headroom (pick x age fade; no cliffs)
    if not _W4RUC or RUC_YRH<=0.0: return 1.0
    fpk=float(np.interp(float(min(pk,99)),[1.,4.,18.,30.],[0.7,1.0,1.0,0.0]))
    fage=float(np.clip((25.0-(a if a is not None else 21.0))/4.0,0.0,1.0))
    return 1.0+RUC_YRH*fpk*fage
def _ruc_head_mult(p,Y=2026): return _ruc_head_core(MA.effpk(p),cp._age_asof(p,Y))   # PRODUCTION leg: as-of age (a 24yo producer keeps headroom; a 30yo does not)
def _ruc_head_v0(p):                                          # V0/SCAFFOLD leg: DRAFT-TIME age (V0 is a draft-time anchor -> D14a same pos x draft-age x pick law preserved by construction)
    return _ruc_head_core(MA.effpk(p), cp._age_asof(p, p.get('year') or (cp.debutyr(p)-1)))
def _ruc_ceiling(p,Y=2026):                                   # production-derived $ ceiling for a real ruck (bestlvl->$)
    s=bestlvl(p,Y)
    if s<=0: return RUC_PRIOR_CAP*draftval(p)*_ruc_head_v0(p)  # NO qualified production -> prior cap stands (x smooth young headroom, draft-age keyed like the scaffold it mirrors)
    if 'grid' not in _RUCCEIL: _build_ruc_ceiling()
    xg,yg=_RUCCEIL['grid']; return RUC_CEIL_HEAD*float(np.interp(s,xg,yg))*_ruc_head_mult(p,Y)
def _ruc_prior_cap(p,v):                                      # V0 PRIOR SCAFFOLD cap — PR #44 kept this byte-identical; W4 DELIBERATELY extends it with the smooth young-pick headroom (the #43 under-priced pocket lives in the V0-anchored sit-out young rucks: Goad/Green class), draft-age keyed
    return min(v, RUC_PRIOR_CAP*draftval(p)*_ruc_head_v0(p)) if (_isreal(p) and MA.gfut(p)=='RUC') else v
_V0C={}; _V0U={}
_V0_CM, _V0_Q97 = cm, q97m    # V0 is a STRUCTURAL prior: pin the import-time models (the pole/ISO convention —
                              # gate1's own rule: "pole(_POLE) + ISO stay in-sample structural priors"). In the
                              # live engine this is an identity (same objects); in fold-swapping harnesses the
                              # zero-evidence start value stays fold-stable instead of reading prior-training
                              # variance as phantom leakage at T0/T1 cells.
def _v0key(p): return (p.get('player'),p.get('year'),p.get('pick'),p.get('type'),p.get('dob'),MA.gfut(p),MA.effpk(p))
def _v0_uncapped(p):                                          # zero-evidence band start value — NO ruc cap, NO guard (RUC gate + guard-build use this)
    # cache key = STABLE CONTENT, not id(p): harnesses that deepcopy players (gate1 truncations) recycle
    # memory addresses; V0's inputs are all draft-time content -> same content, same V0.
    k=_v0key(p)
    if k not in _V0U:
        global cm,q97m
        _c,_q=cm,q97m; cm,q97m=_V0_CM,_V0_Q97
        try: _V0U[k]=raw_ev(p,cp.debutyr(p)-1)*iso_eff(p,cp.debutyr(p)-1)   # LEG A site 3/6 (V0: Y=debutyr-1 => E_q=0 => fade=1 => full strength, unchanged BY CONSTRUCTION)
        finally: cm,q97m=_c,_q
    return _V0U[k]
def _v0_raw(p):                                              # ASK1: uncapped V0 -> RUC prior cap (still pre-ASK2-guard)
    k=_v0key(p)
    if k not in _V0C: _V0C[k]=_ruc_prior_cap(p,_v0_uncapped(p))
    return _V0C[k]
# ==== D13 ASK2 V0 PICK-ORDER GUARD — now RETAINED FOR THE BACKTEST/WALK-FORWARD PATH ONLY. On the BOARD PATH it
# is SUPERSEDED by the D14 V0 curve below (obituary E5; Luke's amended law). Luke's backtest exemption (D14,
# verbatim: "For the backtesting this is not a rule and doesn't make sense to be") means the historical book must
# be UNCHANGED; the v2.3 walk-forward book was built on these guard values, so keeping the guard on the backtest
# path reproduces that book byte-for-byte (maxΔ=0). [D13 spec, for the record:] WITHIN (position x draft-age x
# draft-year) cells V0 is NON-INCREASING in RECORDED pick; downward-only projection to the in-cell running min;
# mature-age/differing-age pairs sit in SEPARATE cells (exempt by construction); scope REAL ND (recorded==effective).
_V0GUARD={}
def _v0_cell(p): return (MA.gfut(p), int(round(cp._age_asof(p, p.get('year') or (cp.debutyr(p)-1)))), p.get('year'))
def _build_v0_guard():
    cells={}
    for p in MA.data:
        if not _isreal(p) or p.get('type')!='ND' or p.get('pick') is None: continue
        cells.setdefault(_v0_cell(p),[]).append(p)
    for _cell,ps in cells.items():
        run=float('inf')
        for q in sorted(ps,key=lambda z:z.get('pick')):            # ascending pick (best -> worst)
            run=min(run,_v0_raw(q)); _V0GUARD[_v0key(q)]=run        # non-increasing downward cap over pick
_build_v0_guard()
# ==== D14 ASK1 (03/07/2026): V0 BOARD CURVE — Luke's AMENDED LAW (verbatim): "for the current values that end up
# in the engine/on the board, we can't have a situation where one player who was a mid at pick 8 has a higher
# starting v0 than another in the same boat. It's illogical." => same POSITION x DRAFT-AGE x RECORDED-PICK gives
# the SAME starting V0 across draft years, on the board. Derivation (fitted on the CURRENT roster's CAPPED V0s —
# the ASK1 ruck cap applies FIRST, i.e. we fit _v0_raw = cap(_v0_uncapped); then the curve): a CONTINUOUS
# kernel/local regression of capped V0 over log RECORDED pick, POOLED ACROSS DRAFT YEARS, projected ISOTONIC
# NON-INCREASING in pick. Pick bands are diagnostic slices only, never derivation bins (binding statistics rule).
# CELLS at the finest resolution the sample supports (census in session_2026-07-03/d14):
#   TIER 1 — age<=18 per position (6 cells; 1408/1571 players): adaptive Gaussian bandwidth grown until local
#     eff-n>=35 at every pick, then isotonic. RUC is its OWN age18 curve (fitted on capped V0s).
#   TIER 2 — mature (draft-age>=19; 163 players): every exact (pos x age) cell is eff-n<35 even at max bandwidth
#     -> R1 pooling. Mature V0 is age-dominated and position-washed in-sample (position spread << age spread), so
#     the 5 non-RUC positions POOL into one age-resolved surface V0*(age,log-pick) [DECLARED]; RUC mature keeps
#     its own (thin) cell. Fit is 2D-kernel over (draft-age, log-pick), then isotonic-non-increasing in pick AND
#     non-increasing in draft-age (older draftee never starts above a younger one, same pick) — so mature entrants
#     stay LAWFULLY DIFFERENTIATED from age-18 and by age. eff-n growth/shortfalls recorded in _V0CURVE_META (R1).
# APPLY on the BOARD PATH: every current-roster real-ND start anchor V0 := V0*(pos, draft-age, recorded pick),
# feeding every present/forward consumer (sit-out retention, staleness/stalled/mediocre caps, the B5 floor, the
# delist scrap). The BACKTEST path is untouched (guard, above). By-construction gates in _v0_curve_assert().
_BOARD_PATH  # (declared above, before _R_surf)
_V0CURVE={}; _V0CURVE_META={}; _V0_GRIDPK=list(range(1,91)); _V0_LGRID=np.log(_V0_GRIDPK)
def _ageR(p): return int(round(cp._age_asof(p, p.get('year') or (cp.debutyr(p)-1))))
def _iso_dec(y): return list(map(float,IsotonicRegression(increasing=False,out_of_bounds='clip').fit(_V0_LGRID,y).predict(_V0_LGRID)))
def _fit_pick_curve(pts,effn_min=35.0,h0=0.18,hmax=2.2):     # adaptive-bandwidth NW over log-pick -> isotonic non-increasing
    lx=np.array([a for a,_ in pts]); vy=np.array([b for _,b in pts]); grid=[]; meta_e=[]; meta_hmax=0
    for lg in _V0_LGRID:
        h=h0
        while True:
            w=np.exp(-0.5*((lx-lg)/h)**2); sw=_det_sum(w); effn=(sw*sw)/_det_sum(w*w) if sw>0 else 0.0   # DETERMINISM FIX: order-fixed sums
            if effn>=effn_min or h>=hmax: break
            h*=1.15
        if h>=hmax: meta_hmax+=1
        grid.append((_det_dot(w,vy)/sw) if sw>0 else _det_mean(vy)); meta_e.append(effn)   # DETERMINISM FIX: order-fixed dot/mean
    return _iso_dec(grid), dict(n=len(pts),min_effn=float(min(meta_e)),grid_at_hmax=meta_hmax)
def _fit_mature(pts,label,effn_min=35.0,ha0=1.2,hamax=8.0,hp0=0.18,hpmax=2.2):  # 2D (draft-age,log-pick) kernel; age-resolved surface
    aa=np.array([a for a,_,_ in pts]); lx=np.array([l for _,l,_ in pts]); vy=np.array([v for _,_,v in pts])
    ages=list(range(19,31)); surf={}; mine=1e9; hmaxhit=0
    for ag in ages:
        row=[]
        for lg in _V0_LGRID:
            ha,hp=ha0,hp0
            while True:
                w=np.exp(-0.5*((aa-ag)/ha)**2)*np.exp(-0.5*((lx-lg)/hp)**2); sw=_det_sum(w)   # DETERMINISM FIX: order-fixed sum
                effn=(sw*sw)/_det_sum(w*w) if sw>0 else 0.0   # DETERMINISM FIX: order-fixed sum
                if effn>=effn_min or (ha>=hamax and hp>=hpmax): break
                if ha<hamax: ha*=1.2
                else: hp*=1.15
            if ha>=hamax and hp>=hpmax: hmaxhit+=1
            row.append((_det_dot(w,vy)/sw) if sw>0 else _det_mean(vy)); mine=min(mine,effn)   # DETERMINISM FIX: order-fixed dot/mean
        surf[ag]=_iso_dec(row)                                # pick-isotonic per age
    for i in range(len(_V0_GRIDPK)):                          # then non-increasing in draft-age at each pick
        run=1e18
        for ag in ages: run=min(run,surf[ag][i]); surf[ag][i]=run
    _V0CURVE_META[label]=dict(n=len(pts),min_effn=float(mine),grid_at_hmax=hmaxhit,ages=ages)
    return surf
def _build_v0_curve():
    POS=['MID','KEY_FWD','KEY_DEF','GEN_FWD','GEN_DEF','RUC']; c18={}
    real=[p for p in MA.data if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None]
    for pos in POS:
        pts=[(np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)==pos and _ageR(p)<=18]
        grid,meta=_fit_pick_curve(pts); c18[pos]=grid; _V0CURVE_META[('age18',pos)]=meta
    matN=[(_ageR(p),np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)!='RUC' and _ageR(p)>=19]
    matR=[(_ageR(p),np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)=='RUC'      and _ageR(p)>=19]
    surfN=_fit_mature(matN,'mature_nonRUC'); surfR=_fit_mature(matR,'mature_RUC')
    _V0CURVE_META['_c18']=c18; _V0CURVE_META['_surfN']=surfN; _V0CURVE_META['_surfR']=surfR
    def star(pos,ag,pick):
        lp=np.log(min(max(pick,1),90))
        if ag<=18: return float(np.interp(lp,_V0_LGRID,c18[pos]))
        surf=surfR if pos=='RUC' else surfN; return float(np.interp(lp,_V0_LGRID,surf[min(max(ag,19),30)]))
    _V0CURVE_META['_star']=star
    for p in real: _V0CURVE[_v0key(p)]=star(MA.gfut(p),_ageR(p),p.get('pick'))
_build_v0_curve()
def v0_start(p):                                             # BOARD -> D14 V0 curve (Luke's amended law); BACKTEST -> D13 guard (Luke's exemption)
    v=_v0_raw(p)                                             # ASK1 ruck cap applied FIRST (cap -> curve/guard order)
    if _BOARD_PATH:
        c=_V0CURVE.get(_v0key(p)); return c if c is not None else v
    g=_V0GUARD.get(_v0key(p)); return v if g is None else min(v,g)
def _v0_curve_assert():                                      # BY-CONSTRUCTION GATES (D14 1c): wired, return dict of results
    star=_V0CURVE_META['_star']; ages=_V0CURVE_META['mature_nonRUC']['ages']
    # (i) same (pos,ageR,pick) -> identical V0* across draft years (function of pos,ageR,pick only) — check dispersion
    from collections import defaultdict
    grp=defaultdict(list)
    for p in MA.data:
        if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None:
            grp[(MA.gfut(p),_ageR(p),p.get('pick'))].append(v0_start(p))
    maxdisp=max((max(v)-min(v) for v in grp.values()),default=0.0)
    # (ii) within (pos,ageR,year) cell inversions under V0*
    byc=defaultdict(list); inv=0
    for p in MA.data:
        if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None:
            byc[(MA.gfut(p),_ageR(p),p.get('year'))].append(p)
    for _c,ps in byc.items():
        ps=sorted(ps,key=lambda z:z.get('pick'))
        for i in range(len(ps)):
            for j in range(i+1,len(ps)):
                if ps[j].get('pick')>ps[i].get('pick') and v0_start(ps[j])>v0_start(ps[i])+1e-6: inv+=1
    # (iii) depth-monotonicity of the KPP-floored retention surface (max of non-increasing curves)
    dmono=True
    for pk in [3,8,15,30,50,80]:
        dv=[ _R_surf('KPP',pk,t) for t in range(1,7) ]
        if any(dv[k+1]>dv[k]+1e-9 for k in range(5)): dmono=False
    return dict(cross_draft_maxdisp=maxdisp, within_cell_inversions=inv, kpp_depth_monotone=dmono)
def sitout_ev(p,Y,e_full):
    fe=_fEy(Y,p); tau=max(0.0,Y-cp.debutyr(p))+((fe**1.5) if Y>=cp.debutyr(p) else 0.0)   # D12: CONCAVE penalty proration tau'=(R/24)^1.5 (Luke OPTION A); completed seasons full (integer knots), in-progress season accrues concavely. PENALTY path only — the lam reward blend below is UNTOUCHED.
    R=_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)     # D13 ASK3: pick-conditioned, isotonic-in-depth surface (was depth-only R_SIT)
    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    lam=float(np.interp(min(gy/fe,6.0),[0,1,2,3,4,5,6],LAM_SIT))                 # games AT PACE vs the prorated bar
    return (1.0-lam)*R*v0_start(p)+lam*e_full
def _first_evidence(p,Y):                                     # the games-ramp family: ALL evidence is season Y
    return not any(x['games']>0 and x['year']<Y for x in p['scoring'])
def _prod_path(p,Y):
    """Production price e_full = raw_ev x iso. For the FIRST-EVIDENCE family, a 3-point moving average
    on the GAMES axis (+/-1 game at the player's own scoring rate) — DECLARED smoothing: the band prior
    is a stepwise (GBR) surface whose exposure-axis steps (measured +957 in one game on the B6 synth)
    and the designed M3 pin-fade otherwise leave the evidence ramp non-monotone (B6 law: more games at
    the same rate never worth less). Centered, unit-mass, level-preserving; nobody outside the family
    is touched."""
    e=raw_ev(p,Y)*iso_eff(p,Y)   # LEG A site 4/6 — THE BOARD PATH (feeds ev())
    if not _first_evidence(p,Y): return e
    row=[x for x in p['scoring'] if x['year']==Y and x['games']>0]
    if not row: return e
    r=row[0]; g0=r['games']; out=[]
    try:
        for gg in (max(g0-1,1),g0,g0+1):
            if gg==g0: out.append(e); continue
            r['games']=gg
            out.append(raw_ev(p,Y)*iso_eff(p,Y))   # LEG A site 5/6 (first-evidence games-axis smoothing)
    finally: r['games']=g0
    return float(np.mean(out))
# ===== WIRED ev =====
def ev(p,Y=2026):
    # (1) delist -> near-zero (no future keeper value) — D10: scrap re-anchored to the LIVE start value
    if delisted(p): return round(0.02*v0_start(p))
    e=_prod_path(p,Y)                                        # (3) isotonic guard inside; family games-axis smoothing
    if _isreal(p) and MA.gfut(p)=='RUC':                  # W4/PR#44: cap PRIOR-DOMINATED ruck production leg at the production-derived ceiling (RL_W4_RUC=0 -> v2.5 1.4xPVC cap)
        _cpv=(_ruc_ceiling(p,Y) if _W4RUC else RUC_PRIOR_CAP*draftval(p)); _v0u=_v0_uncapped(p)  # bind iff ceil < e <= V0_uncapped (hot prior, no demonstrated growth);
        if _cpv<e<=_v0u: e=_cpv                               #   e>V0u (demonstrated) or e<=ceil (already low) -> byte-exact
    # W4 KPF (RL_KPFFIX): compress the ESTABLISHED-KPF loose residual only — SETTLED #9 / PR #42 T1-shape.
    # KPFs bunch near the lowest REPL bar (66.8) and the curve levers tiny production gaps into huge value gaps
    # (CV spread-ratio 6.57 vs MID 4.17). For an established (nqual>=4, age>=24) KEY_FWD, any price ABOVE the
    # engine's own price of his DEMONSTRATED level (eP, band pinned at _lvl_eff — same context, so the W4 margin
    # credit survives inside eP) is band/prior looseness, not output: e' = eP + KPFSH·(e−eP). Young/speculative
    # KPFs (nqual<4 or age<24) are NEVER touched — the Darcy/Duff-Tytler ceiling is protected by construction;
    # the reward leg (above-REPL margin credit ×KPFUP) lives in _w4_W. No blunt group compression.
    if _W4KPF and _isreal(p) and MA.gfut(p)=='KEY_FWD':
        _nk=_nqual(p,Y); _ak=cp._age_asof(p,Y)
        if _nk>=PROVEN_N and _ak is not None and _ak>=24.0:
            _eP=_kpf_prod_efv(p,Y)
            if e>_eP:
                # KPF REBALANCE T1 (2026-07-09): the residual is SPLIT at eD = the engine's price of the
                # SUSTAINED demonstrated level LD (top-2 high-games seasons). A KPF with sustained real
                # production is not a loose residual: the demonstrated-backed slice retains SH_DEM=0.70
                # (measured gap-recovery), only the slice beyond ALL demonstration keeps the settled 0.55.
                # LD<=lvl_eff ⇒ eD=eP ⇒ byte-identical to the pre-rebalance take. Continuous everywhere.
                _LD=_kpf_LD(p,Y); _le=cp._lvl_eff(p,Y)
                _eD=_eP if (_LD is None or _LD<=_le) else min(max(_kpf_prod_efv(p,Y,L=_LD),_eP),e)
                e=_eP+W4_KPFSH_DEM*(min(e,_eD)-_eP)+W4_KPFSH*(e-max(_eD,_eP))

    # (2) staleness family — D10: prorated bars + V0 basis (old-PVC draftval PURGED from every penalty path)
    pos=MA.gfut(p); el=PR.tenure(p,Y); ns=nseas_pro(p,Y); v0=v0_start(p); par=PR.par_at(pos,min(MA.effpk(p),cp.KMAX),min(max(el,1),6)); pr=bestlvl(p,Y)/max(1,par)
    if ns==0:                                                 # SIT-OUT: derived games-ramp treatment (V0-anchored, prorated, scoring-aware, continuous at graduation)
        return round(sitout_ev(p,Y,e))
    keyruc = pos in ('KEY_FWD','KEY_DEF','RUC'); onset = (4 if keyruc else 3)
    if el>=onset and ns<=1:                                   # stalled: essentially no production after the window
        frac=0.25*max(0.4,1-0.10*(el-onset))*(1.6 if keyruc else 1.0)
        e=min(e, v0*frac)
    elif el>=onset+2 and pr<0.55:                             # mediocre-for-years (played but never near par) -> decays too
        frac=0.45*max(0.3,1-0.08*(el-onset))*(1.5 if keyruc else 1.0)
        e=min(e, v0*frac)
    return round(e)
# ==== M3 PROPORTIONAL-TENURE/AGE BLEND (BAKE CANDIDATE v2, D7 02/07/2026 — design + backtest:
# session_2026-07-02/m3_design_proportional_tenure.md; NOT baked until Luke's bake word) ====
# Mid-season the age/tenure clocks advance a FULL year while the season is only fE elapsed. M3 evaluates
# the in-progress season as a VALUE-SPACE interpolation between the full-click evaluation and the
# clock-pinned evaluation (the _M3PIN plumbing above):  v = w*ev_click + (1-w)*ev_pin,
# w = 1 - s*(1-fE), s = clip(1 - g_Y/11, 0, 1) (M2's evidence-replacement scope, same denominator).
# On-pace players (g_Y >= 11) have s=0 -> untouched BY CONSTRUCTION. Completed seasons (Y != the
# in-progress season) are untouched by construction. fE = SEASON_PROG = 0.58 at this cut, recomputed per
# evaluation date (fE -> 1 as the season completes). RL_M3_FE=1 = kill-switch (byte-exact inert).
# RE-REGISTERED ACCEPTANCE at this config (D7): A3 >= 0.75 (Luke's amended bar) with ZERO on-pace
# collateral >2% and B-gates holding.
M3_FE=float(os.environ.get('RL_M3_FE','0.58'))                # elapsed-season fraction; 1.0 -> lever off
M3_DEN=11.0                                                   # M2's evidence-replacement denominator (on-pace floor)
_ev_click=ev                                                  # the full-click evaluation (M1+asc + M2 + caps)
def _m3_s(p,Y):
    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    return float(np.clip(1.0-gy/M3_DEN,0.0,1.0))
def _ev_m3(p,Y=2026):
    v=_ev_click(p,Y)
    if Y!=M3_INPROG_Y or M3_FE>=1.0 or delisted(p): return v  # delisted: both evals identical (no clock read) — skip the double eval
    s=_m3_s(p,Y)
    if s<=0.0: return v                                       # on-pace: untouched by construction
    w=1.0-s*(1.0-M3_FE)
    _M3PIN['on']=True
    try: vpin=_ev_click(p,Y)
    finally: _M3PIN['on']=False
    return round(w*v+(1.0-w)*vpin)
# ==== PRICING FLOOR (BAKE CANDIDATE v2, D7 02/07/2026 — Luke's ruling, B5 amendment: the crater floor
# becomes a PRICING FEATURE; prototype engine/prototypes/floor_pricing_clamp.py 66fbf0f6, D6) ====
# D12 03/07/2026 (Luke ruling R8): floor basis RE-ANCHORED old-PVC draftval -> live V0 start value.
# Schedule (FLOOR_YRS) values UNCHANGED — only the denominator moves onto the same ruler as every other
# penalty path (D10 re-anchored those; the floor was the declared dv-basis holdout). Obituary E3.
#   ev(p,Y) = max(ev_prefloor(p,Y), floor_yrs(Y - draft year) * v0_start(p))
# Scope: REAL store players (id in _REAL — gate synths keep the raw engine, same guard as the v7 overlay),
# NATIONAL-DRAFT entrants only; MSD/SSP (type!='ND'), delisted, retired and pickless players are NEVER
# floored (byte-exact passthrough). Pure lower bound: any player at/above floor is untouched byte-exact
# by construction (max()). TAIL VARIANT A — FLAT .05 yrs 7+ (as signed; Luke's D7 ruling). The FLOOR-SAVES
# table prints on every gates-board run (ship_gates_check.py B5 block) — mispricings stay VISIBLE.
FLOOR_YRS={1:0.45,2:0.35,3:0.28,4:0.21,5:0.13,6:0.09}         # yrs 1-6 (signed schedule)
FLOOR_TAIL=0.05                                               # yrs 7+ FLAT (VARIANT A, as signed)
def floor_frac(yis): return FLOOR_YRS.get(yis,FLOOR_TAIL)
ev_prefloor=_ev_m3                                            # harnesses read this for the saves table / lower-bound re-verify
def ev(p,Y=2026):
    v=ev_prefloor(p,Y)
    if not _isreal(p) or p.get('type')!='ND' or p.get('_retired') or p.get('_pickless') or delisted(p):
        return v                                              # out of scope: byte-exact passthrough
    yis=Y-int(p.get('year') or 0)
    if yis<1: return v
    fl=floor_frac(yis)*v0_start(p)     # D12: RE-ANCHORED draftval -> live V0 (schedule unchanged; Luke R8)
    return v if v>=fl else round(fl)
# ==== W4 PVC FIT (RL_PVCFIT, DOWNSTREAM) — per the re-stamped PVC Derivation Spec v1 (PR #41) ================
# PVC(k) = end-of-calendar-year-1 as-of value of the TYPICAL player at pick k, FITTED FROM THE CANDIDATE
# WALK-FORWARD BOOK anchors (2004-2024 ND pool) — so the curve reads the LIFTED young values and the LIVE ruck
# values (nothing hardcoded), kernel-median over log-pick, parametric power top blended in by ~pick 12 (the
# spec's loclin-at-pick-1), isotonic non-increasing, re-anchored to pick1 = RL_PICK1 (3000).
# SCOPE (deliberate, declared): the fitted curve re-prices the PICK side (the board's trade currency) and
# display/advisory consumers (A13/A14, book draftval column). PLAYER pricing does NOT read it back:
# `draftval` — the RUC prior-cap/scaffold basis — is FROZEN on the pre-fit v3.4 curve (_PVC0), honouring the
# PR #44 V0-scaffold scope and cutting the fit→board→fit circularity (one-iteration drift on the anchors is
# declared in the derivation note). Generated artifact: pvc_fit_candidate.json (stamped with source + book id).
_W4PVC=os.environ.get('RL_PVCFIT','0')!='0'                  # DEFAULT 0 (owner ruling R3, 2026-07-09): the W4 PVC fit is HELD OUT of the bake — the frozen v3.4 curve (_PVC0) ships as the board's pick currency. RL_PVCFIT=1 loads the fitted candidate curve for EXPERIMENTS ONLY (re-derivation queued 'with a view to fixing it'); rl_export.py refuses to write a bakeable board with the fit on (R3 BAKE GUARD), so a fitted board is unbakeable-wrong. Was '1' pre-2026-07-09 — that default silently baked the held-out fit into board bcd81363; flipped to '0' as the remediation.
_PVC0=dict(MA.PVC)                                            # frozen v3.4 ruler for the cap/scaffold basis
def draftval(p): return float(_PVC0[min(MA.effpk(p),cp.KMAX)])   # rebind: runtime cap/scaffold callers read the FROZEN curve
# ===== v2.9 L1(b): swap the ev-channel basis _PVC0 to the L1b smoothed derived curve (pin 3000) + rebuild the
#       V0 guard / V0 curve / RUC ceiling grid — verbatim the l1_adopt_sim option-(b) recipe. Gate RL_PVCADOPT
#       (default ON); RL_PVCADOPT=0 ⇒ block skipped ⇒ _PVC0 stays the frozen v3.4 ruler ⇒ base board byte-exact.
#       Verified: board sum +0.179%, anchors byte-identical, knobel 402→505. Candidate ONLY (non-bakeable path).
if os.environ.get('RL_PVCADOPT','1')!='0':
    import json as _l1j
    _L1CURVE={int(_k):int(_v) for _k,_v in _l1j.load(open('pvc_curve_L1b.json'))['curve'].items()}
    _PVC0.clear(); _PVC0.update(_L1CURVE)
    _V0C.clear(); _V0U.clear(); _V0GUARD.clear(); _RUCCEIL.pop('grid',None)
    _build_v0_guard(); _V0CURVE.clear(); _build_v0_curve()
    MA._pe_clear()
import json as _w4json
_PVCFIT_META={}
if _W4PVC and os.path.exists('pvc_fit_candidate.json'):
    try:
        _pf=_w4json.load(open('pvc_fit_candidate.json'))
        MA.PVC={int(k):int(v) for k,v in _pf['curve'].items()}
        _PVCFIT_META.update({k:_pf.get(k) for k in ('fitted_from','store_md5','n_anchors','window')})
    except Exception as _e:
        _PVCFIT_META['error']=repr(_e)
def find(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]; return c[0] if c else None

# ==== LEG B — UN-COMPRESS REFERENCE (L_ref/V_ref) + PRODUCTION-SIDE CONSERVATION (C[pos]); built LOAD-TIME ==
# PLAN §3/§5. Built AFTER ev() is defined + all player attributes finalized, and BEFORE the RL_AVAIL
# attribution block so that block's ev()-diffs see the SAME (mapped) surface the board ships. INERT unless
# RL_UNCOMP is on AND s is set (UNCOMP_S): the guard then leaves L_ref/V_ref/C empty -> posval_uncomp
# returns base -> board 8d90c9ac BYTE-EXACT (poles above are already warmed unmapped: E=0 + empty reference).
def _uncomp_scope(_p):                                        # valuation scope = active board population
    return _isreal(_p) and not delisted(_p) and not _p.get('_retired')
if MA._UNCOMP and MA.UNCOMP_S is not None:
    MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()              # module load leaves MA's clock at a historical V0-build year; pin to the present so level_now/ev = the 2026 surface (mirrors rl_export.py:42)
    # (1) L_ref[pos] = MEDIAN level_now over the DEMONSTRATED-PROVEN population per position (PLAN §3 (b)):
    #     { p : gfut(p)==pos, _nqual(p,2026) >= PROVEN_N (=4), p in scope }.  V_ref[pos] = posval(L_ref-REPL).
    _lref_pool={}
    for _p in MA.data:
        if not _uncomp_scope(_p) or _nqual(_p,2026)<PROVEN_N: continue
        _g=MA.gfut(_p)
        if _g not in MA.REPL: continue
        _ln=MA.level_now(_p)
        if _ln is None: continue
        _lref_pool.setdefault(_g,[]).append(float(_ln))
    for _g,_vals in _lref_pool.items():
        _Lr=float(np.median(_vals)); MA._UNCOMP_LREF[_g]=_Lr; MA._UNCOMP_VREF[_g]=MA.posval(_Lr-MA.REPL[_g])
    # (2) C[pos]: PRODUCTION-SIDE conservation renorm (PLAN §5). ONE load-time calibration pass over the
    #     valuation scope accumulates Sum(v0), Sum(v0p) per position over the MAPPED legs (posval_uncomp with
    #     C==1); C[pos]=Sum(v0)/Sum(v0p) makes the position's TOTAL production value unchanged by the map
    #     (an explicit per-position budget transfer across year-depths; pedigree/iso premiums + captain delta
    #     are NOMINAL, never renormed). Firing the same ev() calls the board fires makes it conserving.
    MA._UNCOMP_CAL['on']=True; MA._UNCOMP_CAL['v0'].clear(); MA._UNCOMP_CAL['v0p'].clear()
    with contextlib.redirect_stdout(io.StringIO()):
        for _p in MA.data:
            if not _uncomp_scope(_p): continue
            try: ev(_p,2026)
            except Exception: pass
    MA._UNCOMP_CAL['on']=False
    for _g,_s0 in MA._UNCOMP_CAL['v0'].items():
        _s0p=MA._UNCOMP_CAL['v0p'].get(_g,0.0); MA._UNCOMP_C[_g]=(_s0/_s0p) if _s0p>0.0 else 1.0
    print("=== RL_UNCOMP LEG B: map ON (s=%.4f Delta=%.1f) | reference+conservation over %d proven / scope-pop ==="
          %(MA.UNCOMP_S,MA.UNCOMP_DELTA,sum(len(v) for v in _lref_pool.values())))
    for _g in sorted(MA._UNCOMP_LREF):
        print("    %-8s L_ref=%7.2f V_ref=%8.2f C=%.5f (n_proven=%d)"%(_g,MA._UNCOMP_LREF[_g],MA._UNCOMP_VREF[_g],MA._UNCOMP_C.get(_g,1.0),len(_lref_pool.get(_g,[]))))

# ==== RL_AVAIL APPLICATION — set per-record availability fields + Part-1 attribution (G-ATTR) ================
# Runs AFTER ev is fully defined so attribution can diff ev(layer-on) vs ev(layer-off) per register name. The
# layer touches ONLY register keys: every non-register record keeps _avail_hc==0 and _fEy(Y,p)==_fEy(Y), so
# the board is byte-identical off the register set (non-mover parity by construction). RL_AVAIL=0 skips it.
import lti_register as LTIREG
_AVAIL_REPORT=[]; _AVAIL_MOVERS=[]
if _AVAIL_ON:
    _sbk={}
    for _p in MA.data: _sbk.setdefault(_p.get('key'),[]).append(_p)
    _skeys={_k:_v[0] for _k,_v in _sbk.items() if len(_v)==1}
    try:
        _st=LTIREG.build_state(_skeys, report=_AVAIL_REPORT)          # HALT on unknown key / bad schema
    except ValueError as _e:
        raise SystemExit("\n==== LTI REGISTER HALT ====\n"+str(_e))
    assert LTIREG.G_FULL==cp.SEASON, "LTI G_FULL %s != engine season-games cp.SEASON %s (one constant, spec §3.1)"%(LTIREG.G_FULL,cp.SEASON)
    _reg_recs={_p.get('key'):_p for _p in MA.data if _p.get('key') in _st}
    # Part-2 return-haircut surface (derived, net-of-aging; young<27 ships ZERO). HALT if RL_LTI_RETURN is on
    # but the derived table is absent (guard-family halt-not-warn).
    _RET_TAB=None
    if _LTI_RETURN_ON:
        import json as _rjson
        if not os.path.exists('lti_return_table.json'):
            raise SystemExit("Part-2 HALT: RL_LTI_RETURN is ON but lti_return_table.json is absent — run "
                             "derive_lti_return.py / re-seed the workspace.")
        _RET_TAB=_rjson.load(open('lti_return_table.json'))
    def _ret_hc_for(_p,_s):
        """derived return-season haircut h for a Section-A out-name at his return age; young/speculative -> 0."""
        if not (_LTI_RETURN_ON and _RET_TAB and _s['return_arm']): return 0.0
        _a=cp._age_asof(_p,int(_s['ret_year']))                    # age AT the return season
        if _a is None or _nqual(_p,2026)<PROVEN_N: return 0.0      # speculative exemption (nqual<4) — never touch young/speculative
        _sf=_RET_TAB['age_surface']; _ks=sorted(int(k) for k in _sf)
        _ai=int(round(_a)); _ai=min(max(_ai,_ks[0]),_ks[-1])
        return float(_sf[str(_ai)])
    # (1) layer-OFF baseline for attribution — _AVAIL_STATE empty, _avail_hc 0, no ret_hc
    with contextlib.redirect_stdout(io.StringIO()):
        _ev_off={_k:ev(_p,2026) for _k,_p in _reg_recs.items()}
    # (2) Part 1 ON: season-state override (_AVAIL_STATE) + present haircut _avail_hc=L_p (ret_hc still 0)
    _AVAIL_STATE.update(_st)
    for _k,_p in _reg_recs.items():
        _s=_st[_k]
        _p['_avail_hc']=float(_s['L']) if _s['out'] else 0.0       # Part-1 present haircut (lost-production term)
        _flags=[]
        if _s['repeat']: _flags.append('repeat_lti')               # fork-ii on-sight flag (report-only)
        if _s['section']=='B': _flags.append('sectionB_no_return_haircut')
        _p['_lti_reg']={'section':_s['section'],'designations':_s['designations'],'out':_s['out'],
                        'L':round(_s['L'],4),'return_arm':_s['return_arm'],'ret_year':_s['ret_year'],'flags':_flags}
    with contextlib.redirect_stdout(io.StringIO()):
        _ev_p1={_k:ev(_p,2026) for _k,_p in _reg_recs.items()}    # Part-1-only value
    # (3) Part 2 ON: derived return-season haircut on Section-A out-names (own column; young ships 0)
    for _k,_p in _reg_recs.items():
        _s=_st[_k]; _h=_ret_hc_for(_p,_s)
        _p['_lti_ret_hc']=_h; _p['_lti_return_hc']=round(_h,4); _p['_lti_ret_year']=int(_s['ret_year'])
        if _h>0: _p['_lti_reg']['flags'].append('return_hc')
        if _k in _KPF_LD_FALLBACK: _p['_lti_reg']['flags'].append('kpf_LD_fallback')   # fork-v report
    # (4) full eval + SEPARABLE attribution: avail_nerf (Part 1) + lti_ret_delta (Part 2) — G-ATTR
    with contextlib.redirect_stdout(io.StringIO()):
        for _k,_p in _reg_recs.items():
            _vfull=ev(_p,2026)
            _p['_avail_nerf']=int(_ev_p1[_k]-_ev_off[_k])         # Part-1 delta
            _p['_lti_ret_delta']=int(_vfull-_ev_p1[_k])           # Part-2 delta (return arm value)
            _AVAIL_MOVERS.append((_k,_p.get('player'),_ev_off[_k],_ev_p1[_k],_vfull,
                                  _p['_avail_nerf'],_p['_lti_ret_delta'],_p.get('_lti_return_hc',0.0)))
    print("=== RL_AVAIL LAYER ON: %d register names (32 A + 11 B); RL_LTI_RETURN=%s; non-register byte-identical ==="%(len(_reg_recs),_LTI_RETURN_ON))
    if _KPF_LD_FALLBACK:
        print("    fork-v KPFFIX LD fell back to count-against (report-only): %s"%sorted(_KPF_LD_FALLBACK))
    if _AVAIL_REPORT:
        print("    register store-vs-designation anomalies (REPORT-ONLY, register governs, engine never re-diagnoses):")
        for _a in _AVAIL_REPORT: print("      - "+_a)
print("=== AFTER (wired: delist + staleness + isotonic) — named players ===")
print(f"{'player':22s}{'pos':8s}{'pk':>3s}{'g':>3s}{'ten':>4s}{'dlst':>5s}{'draft':>6s}{'BEFORE':>7s}{'AFTER':>7s}  reasoning")
before={'Ronin O':526,'Will Martyn':554,'Sam Philp':714,'Oscar Ryan':570,'Tew Jiath':509,'Jakob Ryan':594,'Harrison Jones':528,'Keidean Coleman':723,'Dylan Stephens':761}
reason={'Ronin O':'delisted, 0g -> ~0','Will Martyn':'delisted, 0g -> ~0','Sam Philp':'delisted, 0g -> ~0','Oscar Ryan':'stalled 0g ten3 -> 1/4 draft','Tew Jiath':'stalled 0g ten3 -> 1/4 draft','Jakob Ryan':'stalled 0g ten4 -> notch below 1/4','Harrison Jones':'mediocre 7yr KEY_FWD -> decayed','Keidean Coleman':'career-maker, holds','Dylan Stephens':'declined MID, should fall below Coleman'}
for nm in before:
    p=find(nm)
    if not p: continue
    print(f"{p['player'][:22]:22s}{MA.gfut(p):8s}{MA.effpk(p):3d}{nseas(p):3d}{PR.tenure(p,2026):4d}{('Y' if delisted(p) else '-'):>5s}{draftval(p):6.0f}{before[nm]:7d}{ev(p):7d}  {reason[nm]}")
print("\n=== MONOTONICITY + deep-pick AFTER ===")
for pos in ['KEY_FWD','MID']:
    for pk in [1,2,3,20,60]:
        sp=synth(pk,PR.par_at(pos,min(pk,cp.KMAX),4),pos); print(f"  {pos:8s} pk{pk:2d} @par -> {ev(sp)}", end='')
    print()
c=find('Keidean Coleman'); s=find('Dylan Stephens')
print(f"\n=== Coleman vs Stephens: Coleman {ev(c)} {'>=' if ev(c)>=ev(s) else '<'} Stephens {ev(s)} -> {'FIXED' if ev(c)>=ev(s) else 'STILL INVERTED'}")

print("\n\n════════ DIAGNOSE Harrison/Stephens + GATE1 + deep collapse + falsifier (wired) ════════")
def band_dump(p):
    b=b6(p); pos=MA.gfut(p); par=PR.par_at(pos,min(MA.effpk(p),cp.KMAX),min(max(PR.tenure(p,2026),1),6))
    recent=[ (x['year'],x['avg']) for x in p['scoring'] if x['games']>=6][-3:]
    return b,par,recent
for nm in ['Harrison Jones','Dylan Stephens','Keidean Coleman']:
    p=find(nm); b,par,recent=band_dump(p)
    print(f"  {nm:16s} par{par:.0f} band[q10..q97]={[round(x) for x in b]} recent={recent} best{bestlvl(p):.0f} pr{bestlvl(p)/par:.2f} ev{ev(p)}")
print("  -> if band q50/q70 high vs recent, cond_prior is pricing career not decline; if q97 tail high, upside inflates")
# refine: DECLINE/MEDIOCRE via RECENT production (last-2-season avg vs par), not just best
def recent_ratio(p,Y=2026):
    s=[a*REF/era.get(y,REF) for y,a in [(x['year'],x['avg']) for x in p['scoring'] if x['games']>=6 and x['year']<=Y]][-2:]
    return (np.mean(s)/max(1,PR.par_at(MA.gfut(p),min(MA.effpk(p),cp.KMAX),min(max(PR.tenure(p,Y),1),6)))) if s else 0.0
print("\n  RECENT ratio (last-2 avg / par):")
for nm in ['Harrison Jones','Dylan Stephens','Keidean Coleman','Oscar Ryan']:
    p=find(nm); print(f"    {nm:16s} recent_ratio={recent_ratio(p):.2f}")
print("\n=== GATE1 (wired) MID/KEY_FWD by tenure ===")
for pos in ['MID','KEY_FWD','GEN_DEF']:
    refs=[p for p in MA.data if MA.gfut(p)==pos and p.get('type')=='ND' and p.get('pick') and 2012<=p['year']<=2019 and nseas(p)>=4 and not delisted(p)][:14]
    ser={}
    for k in range(0,6):
        vs=[ev(p,cp.debutyr(p)-1+k) for p in refs if cp.debutyr(p)-1+k<=2026 and any(s['year']<=cp.debutyr(p)-1+k and s['games']>=6 for s in p['scoring'])]
        if vs: ser[k]=np.mean(vs)
    base=ser.get(2,1); print(f"  {pos:8s} "+" ".join(f"yr{k}:{round(100*v/base)}" for k,v in sorted(ser.items())))
print("\n=== 2019 deep-pick (pk>40) REAL collapse (wired) ===")
deep=[p for p in MA.data if p.get('type')=='ND' and p.get('pick') and p['year']==2019 and MA.effpk(p)>40 and MA.GRP.get(p.get('pos'))]
tot_before=sum(raw_ev(p) for p in deep); tot_after=sum(ev(p) for p in deep); tot_draft=sum(draftval(p) for p in deep)
print(f"  {len(deep)} deep picks: BEFORE sum {tot_before:.0f} | AFTER sum {tot_after:.0f} | draft sum {tot_draft:.0f} | realized PVC sum {tot_draft:.0f}")
print(f"  AFTER/draft = {100*tot_after/tot_draft:.0f}% (was {100*tot_before/tot_draft:.0f}%) -> collapse toward realized")
print("\n=== FALSIFIER still clean (wired)? ===")
def mkf(pk,avg): return synth(pk,avg,'MID')
e1=ev(mkf(1,70)); e2=ev(mkf(20,72)); bu=ev(mkf(1,40)); el=ev(mkf(20,95)); md=ev(mkf(1,62))
print(f"  PRIMARY pk1@70 {e1} {'>' if e1>e2 else '<'} pk20@72 {e2} | ELITE pk20@95 {el} {'>' if el>md else '<'} pk1@62 {md} | grid {'PASS' if all(ev(mkf(1,86+d))>ev(mkf(20,67+d)) for d in [-30,-12,0,12,25]) else 'FAIL'}")
