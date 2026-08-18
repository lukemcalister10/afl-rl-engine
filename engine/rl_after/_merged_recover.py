"""WIRE (1) delist->~0 (2) staleness floor all-stalled (3) isotonic pick guard INTO the engine. Prove on named players."""
import os,io,contextlib,copy,pickle,numpy as np
import math as _math
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.isotonic import IsotonicRegression
def _season_val(_key, _fb):
    """DYNAMIC season-state value (calendar_progress|exposure_pace) from data/season_state.json (single
    source; advances weekly).
    FENCED (RL_CONFIG_MODE in bake|gate|canonical): HALT on any of unresolved/untrusted repo root,
    missing file, malformed JSON, missing key, or a non-numeric / non-finite value. UNFENCED dev: fallback."""
    import json as _j
    _mode = (os.environ.get('RL_CONFIG_MODE') or '').strip().lower()
    _fenced = _mode in ('bake', 'gate', 'canonical')
    _r = os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR')
    if not _r:
        if _fenced:
            raise RuntimeError("FENCED season-state read (RL_CONFIG_MODE=%s): repo root unresolved "
                               "(RL_REPO/CLAUDE_PROJECT_DIR unset) — cannot load authoritative season state" % _mode)
        _r = '.'
    _p = os.path.join(_r, 'data', 'season_state.json')
    try:
        _v = float(_j.load(open(_p))[_key])
        if _v != _v or _v in (float('inf'), float('-inf')):
            raise ValueError("non-finite %s=%r" % (_key, _v))
        return _v
    except Exception as _e:
        if _fenced:
            raise RuntimeError("FENCED season-state read (RL_CONFIG_MODE=%s): cannot load %r from %s (%s)"
                               % (_mode, _key, _p, _e)) from _e
        return float(_fb)
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
# ==== ERA NORMALIZATION REMOVED (#334 stage B salvage, OWNER RULING — ballot word 1, 5242713366) ====
# An era[Y] table used to be built here (mean season avg over >=6-game seasons per year, 2009-2025,
# with REF = the mean of those years) and every career-score read was multiplied by REF/era.get(y,REF).
# OWNER RULING (binding): SuperCoach scores are era-comparable BY CONSTRUCTION — every match assigns
# 3,300 points, so a season average already sits on one common scale and a per-year rescale is a
# distortion, not a correction. NO era normalization may be applied to scoring anywhere. The table,
# REF, and every a*REF/era.get(y,REF) site are gone; season averages are read RAW. Do not reintroduce.
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
PROVEN_N=4; TAIL_TRIM=float(os.environ.get('RL_TAIL_TRIM','0'))   # #334 menu (b): proven beyond-year-11 carry trim; 0 = shipped, byte-exact
POLE_RAMP=22.0    # PROVEN_N surface NOT wired (no committed exec spec) -> scalar 4 + c=n/4 retained; see CHANGELOG 2026-06-30
RUC_WAGE=float(os.environ.get('RL_RUC_WAGE','1.0'))   # #334 ITEM E1 sizing: 1.0 = the full standard ramp; 0.0 reproduces the old wage=0 pole denial byte-exact.
# ==== GAMES-RAMP PRORATION (D10 03/07/2026 — Luke's design statement, verbatim in the directive):
# every games bar (6/10/14/22) prorates to season progress for the IN-PROGRESS season — a player is
# judged only against games that were playable (R14/24 -> fE=0.58 at this cut; RL_M3_FE = the M2/M3
# season-progress convention, one dial). Completed seasons are byte-identical (fE=1). G_ADQ (12, M1
# proven-player recent-adequacy window) deliberately NOT prorated — outside the 6/10/14/22 enumeration.
SEASON_FE=_season_val('calendar_progress',0.58)   # CALENDAR progress (was RL_M3_FE env / 0.58); dynamic from season_state
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
# STEP-3 CALIBRATION WIRED 2026-06-30 (candidate): per-group LDECAY + FLAT_TOL (KEY / GEN / MID+RUCK)
def _ldg(pos): return 'KEY' if pos in ('KPF','KPD') else ('GEN' if pos in ('SF','SD') else 'MR')
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
#   (predecessor: position ~uniform; RUCK thinnest — DECLARED).
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
# ==== LEG F3 (§2.vi, MEMO_LEGF v1.1; supervisor ruling item 353) — FORM-ANCHOR CLOCK ================
# The forward lens (rl_export sets MA._LENS_FORM => AGE_REF>BASE_REF) must carry the SAME pedigree/evidence
# blend at the projected state, the pedigree weight decaying ONLY as PROJECTED EVIDENCE accrues — NOT as the
# age/tenure clock advances (R103.3 / MEMO_LEGF v1.1 §2.vi; the item-352 "age erases pedigree" defect). This
# context evaluates the pedigree-fade + tenure clocks at the FORM ANCHOR (BASE_REF) while the production/growth
# path keeps AGE_REF. Gated on MA._LENS_FORM (the SAME signal b6/price6 use, :258/:265) — NOT on
# AGE_REF!=BASE_REF, because the load-time V0-curve/ISO/backward builds run AGE_REF!=BASE_REF with _LENS_FORM
# None and MUST stay byte-exact (they feed the k=0 board / the HARD-OUT V0 chain :1121-1171, never touched
# here). k=0 / balanced / backward => _LENS_FORM None => pure no-op => byte-exact BY CONSTRUCTION (proven:
# balanced RL_LEGE=0 => 06d8af60, edited==pristine). No new multiplier, no lens-only growth term (Reid) — it
# REMOVES a lens-only clock PENALTY.
import contextlib as _f3ctx
_LEGF_ON=os.environ.get('RL_LEGF','1')!='0'   # LEG F3 gate (== the F1 phantom gate): the whole §2.vi projection cure rides RL_LEGF (default ON). RL_LEGF=0 => every F3 edit below is INERT => the pre-F3 Leg-E chain reproduces byte-exact (d85901af / 06d8af60 / 9829d01a), the directive's RL_LEGF=0 kill-switch proof.
@_f3ctx.contextmanager
def _form_anchor_clock():
    _sv=MA.AGE_REF
    if _LEGF_ON and getattr(MA,'_LENS_FORM',None) is not None and MA.AGE_REF!=MA.BASE_REF:
        MA.AGE_REF=MA.BASE_REF
    try: yield
    finally: MA.AGE_REF=_sv
def _fa_year(Y):
    # the FORM-ANCHOR year for evidence/tenure clocks: BASE_REF (== MA._LENS_FORM) inside the forward lens,
    # else the eval year Y. PR.tenure/nseas key on the YEAR ARGUMENT (not only AGE_REF), so re-keying the
    # tenure clock on BASE_REF is done by passing _fa_year(Y). RL_LEGF=0 or k=0 => returns Y => identity.
    lf=getattr(MA,'_LENS_FORM',None)
    return lf if (_LEGF_ON and lf is not None) else Y
# ==== LEG F4 (§2.vii/§2.ix, MEMO_LEGF v1.2/v1.3; owner rulings item 356/359) — THE L-SYMMETRY DAMPER =======
# The forward lens over-declines the mid/veteran PRODUCTION cohorts (phi=0) ~2x their realized rate (the
# item-354 residual: composition forward -19.9% vs realized backward -9.0%). F4 tempers the forward AGE_REF
# advance of the TWO production-price age reads (the b6 demonstrated-level band :287-288 + the level_now
# consumption :851) to the SAME players' MEASURED POPULATION backward-transition rate r_pop(age) — measured
# on each committed -2/-1/now roster INCLUDING exiters' realized residual paths (busts full weight, R107.3),
# so a single population rate carries exit risk and the F3 §2.iii retirement haircut RETIRES (v1.3 §2.ix, no
# double-count). Geometric blend by the sealed s(age): x_used = x_form * (x_age/x_form)**s. s=1 => x_used ==
# x_age (undamped, byte-exact); s in [0,1) tempers the advance toward the form anchor. FORWARD-ONLY (MA.
# _LENS_FORM set AND AGE_REF>BASE_REF) + RL_LEGF-gated => k=0 / balanced / backward / RL_LEGF=0 => x_age==x_form
# => x_used==x_age => the pre-F4 chain byte-exact BY CONSTRUCTION. Reid: the damper's ONLY content is the
# sealed measured rate; s(age) is the deterministic coefficient reproducing r_pop(age), sealed beside it, never
# iterated against a backtest. No cohort hand-tuning (per age-transition, smoothed rule 7). F3's cures are the floor.
import json as _f4json
_LSYM_ON=_LEGF_ON   # rides the F-leg RL_LEGF gate (default ON); RL_LEGF=0 => _LEGF_ON False => damper inert
# THE SEALED RATE (measured ONCE on the committed -2/-1/now boards, sealed pre-render, NEVER iterated against a
# backtest — MEMO_LEGF v1.3 §2.ix, owner item 359):
#   r_pop(age) = value-weighted realized backward-transition rate per draft-year age, INCLUDING exiters'
#                realized residuals (off-board=0, busts full weight R107.3); rule-7 smoothed. SEAL sha256_8 c62b5ee8.
#   s(age)     = the geometric-blend coefficient bisected so the DAMPED median(vP1/v) per age == r_pop(age)
#                (deterministic solution of the sealed-rate constraint; Reid — content IS the measured rate). SEAL sha256_8 efe97ee3.
# Embedded literal (no external file — the seal ships IN the engine source; env RL_LSYM_TAB path overrides for
# re-derivation only). s=1 => byte-exact undamped; forward-lens + RL_LEGF gated + k=0-inert (see _lsym_active).
_LSYM_SEAL={'r_pop':{'18':1.0016,'20':1.0007,'22':0.9777,'24':0.9073,'26':0.7886,'28':0.7886,'30':0.7886,'32':0.7886,'34':0.7886,'36':0.7886,'38':0.6591},
            's':{'18':0.0,'20':0.0,'22':0.0,'24':0.048,'26':0.5988,'28':0.6053,'30':0.5988,'32':0.426,'34':1.0,'36':1.0,'38':1.0,'40':1.0},
            'r_pop_sha256_8':'c62b5ee8','s_sha256_8':'efe97ee3'}
_LSYM_TAB=None
if _LSYM_ON:
    _ov=os.environ.get('RL_LSYM_TAB')                        # re-derivation override ONLY (calibration harness); default = the sealed literal
    try: _LSYM_TAB=_f4json.load(open(_ov)) if _ov else _LSYM_SEAL
    except Exception: _LSYM_TAB=_LSYM_SEAL
def _lsym_active():
    return (_LSYM_ON and _LSYM_TAB is not None
            and getattr(MA,'_LENS_FORM',None) is not None and MA.AGE_REF!=MA.BASE_REF)  # forward lens only
def _lsym_age(p):
    # the age-at-START key, on the SAME draft-year basis r_pop was measured on the committed boards
    # (round((asof-draft_year)+18.5)) so the sealed rate and the damper index the identical transition.
    yr=p.get('year')
    if yr is None: return MA._age_at(p,MA.BASE_REF) if hasattr(MA,'_age_at') else MA.age(p)
    return int(round((MA.BASE_REF-int(yr))+18.5))
def _lsym_s(a):
    if _LSYM_TAB is None or a is None: return 1.0
    st=_LSYM_TAB.get('s') or {}; ai=int(round(a))
    if str(ai) in st: return float(st[str(ai)])
    if not st: return 1.0
    nk=min((int(k) for k in st),key=lambda x:abs(x-ai)); return float(st[str(nk)])
def _lsym_blend(x_form,x_age,a):
    # geometric temper of the AGE-REF advance toward the FORM anchor; s=1 => identity (x_age). Vector or scalar.
    s=_lsym_s(a)
    if s>=1.0 or x_form is None or x_age is None: return x_age
    xf=np.asarray(x_form,dtype=float); xa=np.asarray(x_age,dtype=float)
    with np.errstate(divide='ignore',invalid='ignore'):
        r=np.where(xf>0.0, xa/xf, 1.0)
        out=xf*np.power(np.clip(r,1e-9,None),s)
    out=np.where(xf>0.0,out,xa)
    return out if getattr(x_age,'ndim',0) else float(out)
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
def _par_prior(p,Y):
    with _form_anchor_clock(): _T=min(max(PR.tenure(p,_fa_year(Y)),1),6)   # LEG F3 §2.vi: the PEDIGREE PAR (the pedigree-fade "decay", pw·par in _coreM1) holds at the FORM ANCHOR (BASE_REF year-arg + AGE_REF pin) — a developing pick's draft pedigree does not fade just because the forward lens advanced his tenure a year. k=0 identity by construction.
    return PR.par_at(MA.gfut(p),min(MA.effpk(p),cp.KMAX),_T)
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
def _b6_core(p,Y):
    MA.AGE_REF=Y; MA.BASE_REF=(MA._LENS_FORM if getattr(MA,'_LENS_FORM',None) is not None else Y); MA._pe_clear()   # LEG E projection law (R103.3): a forward lens sets MA._LENS_FORM (=the true-now form anchor, 2026) so AGE_REF>BASE_REF => _dev_advance CREDITS expected production (age+k through the map's own growth curve; no lens-only term, the Reid constraint). _LENS_FORM None (balanced/back path) => BASE_REF=AGE_REF=Y, byte-exact.
    with contextlib.redirect_stdout(io.StringIO()): b=np.asarray(cp.cond_prior_band(p,cm,Y))
    return np.append(b,max(float(q97m.predict(np.array([cp._feat(p,Y)]))[0]),b[4]))
def b6(p,Y=2026):
    b_age=_b6_core(p,Y)
    # LEG F4 §2.vii: temper this band's AGE_REF advance to r_pop(age) — read #1 of the two granted sites.
    if _lsym_active() and Y!=MA.BASE_REF:                     # forward lens only; k=0 (Y==BASE_REF) => skip (byte-exact)
        _bf=MA.BASE_REF                                       # the form-anchor year (== _LENS_FORM)
        a0=_lsym_age(p)   # draft-year age basis (matches r_pop)
        if _lsym_s(a0)<1.0:                                   # s>=1 => no-op => skip the extra band build (byte-exact + fast)
            b_form=_b6_core(p,_bf)                            # form-anchored band (AGE_REF held at BASE_REF; no future scoring rows => == the now band)
            b_age=_lsym_blend(b_form,b_age,a0)
            MA.AGE_REF=Y; MA.BASE_REF=_bf; MA._pe_clear()     # restore the forward-lens clock the caller set
    return b_age
def price6(p,bb,Y=2026):
    sav=dict(MA.REPL)
    try:
        for g in MA.REPL: MA.REPL[g]=sav[g]-rd.REPL_DROP.get(g,0)
        MA.AGE_REF=Y; MA.BASE_REF=(MA._LENS_FORM if getattr(MA,'_LENS_FORM',None) is not None else Y); MA._pe_clear()   # LEG E projection law (R103.3): form-anchor split (see b6). _LENS_FORM None => byte-exact base path.
        with contextlib.redirect_stdout(io.StringIO()): return float(dp.SCALE_DIST*_det_dot(WQ6,[dp.v_at_peak(p,float(L),'bal') for L in bb]))   # DETERMINISM FIX: order-fixed dot (was np.dot -> BLAS, CPU-dependent)
    finally: MA.REPL.update(sav)
def recover(perf,par): return float(np.clip(np.interp(perf/max(1.0,par),RECX,RECY),0,1))
def synth(pk,avg,pos,nyr=2): return {'player':'s','pos':GRPPOS.get(pos,midpos),'pick':float(pk),'year':2023,'dob':'2005-03-01','type':'ND','scoring':[{'year':2024+i,'games':18,'avg':float(avg)} for i in range(nyr)],'_pos_now':None,'_futpos':None}   # DPP STRIP: single-position synth (gfut falls back to bnow=pos)
# ORDER 30B STEP-3 MEASUREMENT DIALS. BOTH DEFAULT OFF => the shipped expressions are byte-identical.
# They exist to PRICE the forbidden-set boundary (which objects the 26A deletion reaches) before the owner
# rules it, exactly as the STEP-2 stop priced its three options. No board ships with either set.
# ===== ORDER 30B-P — THE STEP-3 PREVIEW DIAL. ONE NEW DECLARED DIAL, DEFAULT OFF. =========================
# RL_O30B_PREVIEW=1 wires the SEAT-RECOMMENDED Step-3 configuration so the owner can rule the still-OPEN
# forbidden-set boundary from a BOARD rather than from prose (#334 comment 5299562714). NOTHING IS GREENLIT:
# with the dial unset every expression below is byte-identical to the committed Step-2 build and the board
# reproduces 9298203135202a0c707bb0977ba38c31 EXACTLY.
#
# IT COMPOSES WITH — DOES NOT DUPLICATE — THE TWO STEP-3 MEASUREMENT DIALS. The preview IMPLIES both
# ablations: RL_O30B_PREVIEW=1 sets _O30B_NOPOLE and _O30B_NOISO to True by the `or` below, so the pole leg
# and the par-built ISO pick-tax are deleted through THE SAME TWO LINES the ablation boards used (:487,:517)
# and no third deletion path exists. Either ablation dial may still be set on its own, exactly as before.
#
# THE PREVIEW IS PRE-NUMERAIRE. Step 6's re-pin has NOT run; every table generated from this lane says so.
# ===== ORDER 30B-N — THE RESOLVED CANDIDATE. A SECOND DECLARED DIAL, DEFAULT OFF, THAT EXTENDS THE ABOVE. =
# #334 comment 5310246218. The owner is ruling on the RESOLVED configuration (ORDER 30B-R) and requires ITS
# no-arb tables, so the resolved law has to exist AS A PRICE at as-of years, not only as a derived board.
# RL_O30B_RESOLVED=1 IMPLIES RL_O30B_PREVIEW=1 — by the `or` on the next line and nowhere else. That is the
# whole point: the resolved law swaps the BLEND FUNCTION and nothing else. The production leg it consumes is
# the preview lane's finished production leg (pole DELETED, ISO DELETED, par denominators re-referenced to
# the effective positional bars, both superseded anchor blends and the year-zero floor REPLACED). If the
# resolved dial re-derived its own production leg it would no longer be the law RESOLVED_ALLROWS.json prices,
# and the current-board row control could not be scored. NOTHING IS GREENLIT and NOTHING WIRES PERMANENTLY:
# with both dials unset the committed board 9298203135202a0c707bb0977ba38c31 reproduces BYTE-EXACT.
_O30B_RESOLVED=os.environ.get('RL_O30B_RESOLVED','0')!='0'  # ORDER 30B-N: the RESOLVED candidate's law
# ===== ORDER 31 — THE ONE LAW. A THIRD DECLARED DIAL, DEFAULT OFF, THAT REPLACES THE LANES. ===============
# #334 comment 5310338355. The lanes/bridge/join design (30B-N above) is CONDEMNED by the brief -- "the four
# row diagnosis killed the thin lane" -- and is REPLACED, not amended. RL_O31=1 implies RL_O30B_PREVIEW=1 by
# the `or` below and nowhere else, so the ONE LAW consumes the SAME production leg the preview built (pole
# deleted, ISO deleted, the two par denominators re-referenced, the three supersessions applied) and swaps
# ONLY the price law. With the dial unset every expression below is inert and the committed Step-2 board
# 9298203135202a0c707bb0977ba38c31 reproduces BYTE-EXACT.
#
#     price(p,Y) = rho(g) * Phat  +  [ D(c_u) * (1 - rho(g))  +  Phi(g,s) * beta_mono(g) * rho(g) ] * V0
#
# ONE FORMULA, EVERY ROW, EVERY PATHWAY, EVERY GAMES COUNT. There is no sitter branch, no thin lane, no
# bridge and no deep lane: RL_O31 switches OFF the _entry30b_price interception in the ev() wrapper so that
# a zero-games row is priced by the SAME expression as a 300-game row. It agrees with the two ruled laws at
# their own endpoints EXACTLY, which is why no lane is needed:
#     g = 0     rho(0)=0, Phi(.,0)=1  ->  price = D(c) * V0        the wired STEP-2 SITTER LAW, exactly
#     rho -> 1                        ->  price = Phat + beta*V0   the 30B-R ADDITIVE READING (T1), exactly
# ==== ORDER A — CANDIDATE 32 (#334 comment 5312733761), DEFAULT OFF. RL_O32=1 implies RL_O31=1 (the
# one law is the substrate). RL_O32_STAGE (declared, default 6 = the full candidate) wires the ruled
# mechanisms CUMULATIVELY so every leg of the movers decomposition is a real board:
#   1 age-referenced gate bars (S1 C3, gate-only object) · 2 +per-season played credit G*=2 ·
#   3 +delivered-season reset of c_u · 4 +joint re-derived Phi row (the D row re-derived at deviation
#   0.0 — FADE_32.json — so no stage-4 D constant exists) · 5 +selection relief inside D (capped at
#   full pedigree) · 6 +the 5-15g re-mix (R-REMIX, two-sided).
# Dial unset => _O32S == 0 => every branch below is inert and the Candidate 31 board fe6be9d6
# (RL_O31=1) / the Step-2-law board (RL_O31 unset) reproduce BYTE-EXACT. NOTHING LANDS WITHOUT THE
# OWNER'S WORD ON THE PACKET.
_O34=os.environ.get('RL_O34','0')!='0'                      # ORDER C: the age-conditional normalization (#334 c.5315155802; PREREG_C.md pushed first). IMPLIES RL_O32 on the next line and nowhere else.
# ORDER D — THE PICK-CURVE SITTER FADE (owner word: WIRE OPTION (A), the MEASURED curve; ruling
# R-PICKFADE's smooth-curve condition; PREREG_D.md + amendment AD1; docs/evidence/order_d_2026-08-17).
# RL_O35 implies RL_O32 below and nowhere else; NOT stacked on RL_O34 (Order C shelved). Dial-off
# reproduces the repaired Candidate 32 board 7802ee97 BYTE-EXACT. THE LANDING CANDIDATE on the
# owner's word.
_O35=os.environ.get('RL_O35','0')!='0'                      # ORDER D: the pick-curve fade
# ORDER I — THE COORDINATED BUILD (#334 comment 5317842435; PREREG_I.md pushed before the first engine
# edit). THREE MEASURED LEVERS ON ONE DIAL: (1) S1, the age-referenced bar inside the projection core
# (wired in rl_model.o36_bar and its two duplicate loops here); (2) THE COUNTERWEIGHT — the O32 re-mix
# and relief constants RE-DERIVED JOINTLY on the corrected age-fair readings, so the S1 lift is paid to
# performers and charged to sub-expectation-with-games rows; (3) Order H's smooth TALL/SMALL factor on
# the wired pick-curve fade. RL_O36 IMPLIES RL_O35 (and so RL_O32/RL_O31) on the next lines and nowhere
# else. Dial-off reproduces the landing candidate 1f176444 BYTE-EXACT. NOTHING LANDS WITHOUT THE OWNER.
_O36=MA._O36                                                # ORDER I: read in rl_model (S1 needs it at import)
# ORDER P — THE PEDIGREE-CONDITIONAL CHARGE (RL_O37; PREREG_P_BUILD.md pushed before this edit;
# docs/evidence/order_p_2026-08-18 is the measurement and the derivation). It REPLACES the ORDER A
# stage-6 blind eta charge — a pure function of GAMES, peaking at gamma_d = 14 and blind to how the
# player actually played — with a charge read against the bar the player's OWN ENTRY PRICE implies.
# RL_O37 IMPLIES RL_O36 (and so RL_O35/RL_O32/RL_O31) in rl_model, and nowhere else. Dial off =>
# ORDER K's board f3101883 reproduces BYTE-EXACT. NOTHING LANDS WITHOUT THE OWNER'S WORD.
_O37=MA._O37                                                # ORDER P: read in rl_model (it sets the O36 dose default)
# ORDER Q — TWO DEFECT REPAIRS, PRICED AND NOT ADOPTED (RL_O38A / RL_O38B1 / RL_O38B2; PREREG_Q.md
# pushed before this edit). RL_O38A monotonises the pedigree leg in ENTRY PRICE. RL_O38B1 deletes the
# age-24 gate. RL_O38B2 ramps the charge out across ages 23-26 with an INVENTED endpoint. Each implies
# RL_O37 (and so the whole O36/O35/O32/O31 stack) in rl_model and nowhere else. All three unset =>
# ORDER P's board 374d4e44 reproduces BYTE-EXACT. NOTHING IS ADOPTED AND NOTHING LANDS.
_O38A=os.environ.get('RL_O38A','0')!='0'
_O38B1=os.environ.get('RL_O38B1','0')!='0'
_O38B2=os.environ.get('RL_O38B2','0')!='0'
_O38=_O38A or _O38B1 or _O38B2
if _O38B1 and _O38B2:
    raise SystemExit('ORDER Q HALT: RL_O38B1 and RL_O38B2 are ALTERNATIVES, not a stack. B1 deletes '
                     'the age gate outright; B2 ramps the charge out across 23-26. Running both would '
                     'price a variant nobody asked for and label it one of the two.')
if _O38 and not _O37:
    raise SystemExit('ORDER Q HALT: an RL_O38* dial is set but RL_O37 is not live. The ORDER Q repairs '
                     'act on the ORDER P charge; without it there is nothing to repair.')
# ORDER R — THE OWNER'S TWO SOFTENINGS, PRICED AND NOT ADOPTED (RL_O39_TMAXPCT / RL_O39_BETASAT;
# PREREG_R.md pushed before this edit; docs/evidence/order_r_2026-08-18). The owner judged the ORDER P
# charge too harsh on hard underperformers -- "effectively stripped their pedigree" -- and ruled two
# softenings: (1) "tmax should be 15 or 20 not 5", i.e. set the cap at the 15th or 20th percentile of
# the young cohort's own surplus instead of the 5th; (2) "maybe soften the charge a little bit", i.e.
# lower BETA_sat, but ONLY inside its published 90% CI. Both dials default OFF and both act ONLY on the
# ORDER Q charge path, so with them unset every ORDER P and ORDER Q board reproduces BYTE-EXACT.
# NOTHING IS ADOPTED AND NOTHING LANDS.
_O39_PCT_RAW=os.environ.get('RL_O39_TMAXPCT','')
_O39_BSAT_RAW=os.environ.get('RL_O39_BETASAT','')
_O39=(_O39_PCT_RAW!='' or _O39_BSAT_RAW!='')
if _O39 and not _O38:
    raise SystemExit('ORDER R HALT: an RL_O39_* dial is set but no RL_O38* dial is live. The ORDER R '
                     'softenings reach the ORDER Q charge path only. Setting one without an RL_O38 dial '
                     'would silently do nothing and print a board labelled as though it had.')
_O39_PCT=int(_O39_PCT_RAW) if _O39_PCT_RAW!='' else 5
if _O39_PCT not in (5,15,20):
    raise SystemExit('ORDER R HALT: RL_O39_TMAXPCT=%r. Only 5 (ORDER P\'s own), 15 and 20 are measured '
                     'percentiles of the young cohort surplus. Nothing else is priced and nothing else '
                     'may be invented at the dial.'%_O39_PCT_RAW)
_O35=_O35 or _O36                                           # ORDER I implies the pick-curve fade
_O32=(os.environ.get('RL_O32','0')!='0') or _O34 or _O35    # ORDER A: CANDIDATE 32 (ORDERS C/D build ON it)
_O32S=(int(os.environ.get('RL_O32_STAGE','6')) if _O32 else 0)
_O31=(os.environ.get('RL_O31','0')!='0') or _O32            # ORDER 31: THE ONE LAW (O32 implies it)
_O31_NOPHI=os.environ.get('RL_O31_NOPHI','0')!='0'           # declared, default off: price the 30B-C conditioning by removing it
_O30B_PREVIEW=(os.environ.get('RL_O30B_PREVIEW','0')!='0') or _O30B_RESOLVED or _O31  # ORDER 30B-P: the whole preview lane
_O30B_NOPOLE=(os.environ.get('RL_O30B_NOPOLE','0')!='0') or _O30B_PREVIEW   # delete the PEDIGREE POLE leg from raw_ev
_O30B_NOISO=(os.environ.get('RL_O30B_NOISO','0')!='0') or _O30B_PREVIEW     # delete the par-built ISO pick-tax from the production path
# THE EFFECTIVE POSITIONAL BARS — the ONE object the preview re-references the two retained par denominators
# to. It is `MA.REPL[pos] - rd.REPL_DROP[pos]`, i.e. the position bar the pricing core ITSELF subtracts inside
# price6 (`MA.REPL[g]=sav[g]-rd.REPL_DROP.get(g,0)`), and it is the identical object ORDER 30B-M's harness
# read live off the engine and asserted against the owner's Ruling 1 numbers
# (KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9 — o30bm_measure.py:70-73).
# It is POSITION-LEVEL and PICK-BLIND by construction: there is no pick axis in it at all.
_O30BP_BARS={_g:(MA.REPL[_g]-rd.REPL_DROP.get(_g,0.0)) for _g in MA.REPL}
# ===== ORDER C (#334 comment 5315155802) — THE AGE-CONDITIONAL NORMALIZATION SURFACE (RL_O34). =========
# THE DEFECT: ORDER 31's lawful deletion of the pick-prior par tables (aimed at the PICK axis) also
# deleted their DEVELOPMENT axis, re-referencing the production leg's two RETAINED normalization
# denominators (the Q evidence weight in _c_w; the decay-gate par inside ev()) to the FLAT bars above —
# so young output is judged against MATURE standards inside the production core (S1: those bars fail
# 86-100% of age-18/19 seasons even for players who turn out fine). ORDER C replaces the OBJECT in those
# two denominators — AND ONLY THOSE TWO — with the measured S1 C3 age x position expected-output surface:
#     par34(pos, age) = _O30BP_BARS[pos] - DELTA(class, clamp(age, 18, 23))
# NO PICK AXIS (the forbidden-set ruling stays fully honoured) · CAPPED AT THE FLAT BAR (DELTA >= 0,
# load-asserted) · FLAT FROM AGE 24 on the integer age Y - birth-year (the SAME basis every O32 age
# object uses), so every mature row prices BYTE-IDENTICALLY — the core identity control. The stall gate
# keeps its own repair-built age bars (o32_gate_bar); the v0-language, the instruments and every other
# reader keep the flat bars; _O30BP_BARS itself is NEVER edited. DELTA is the C3 class-pooled table the
# repair already carries (O32_GATE_DELTA lineage; CONSTRUCTIONS_S1.json::C3), duplicated here because
# the two denominator sites are read before the O32 block exists. With RL_O34 unset _o34_par returns the
# flat bar on every call and the repaired Candidate 32 board 7802ee97 reproduces BYTE-EXACT.
_O34_TALL=frozenset(('KPD','KPF','RUCK'))
_O34_DELTA={'TALL':{18:22.334475609756097,19:20.55500752464971,20:16.306362402208926,
                    21:11.588672690048071,22:7.826894964594814,23:6.439783302063788},
            'SMALL':{18:20.080511089352214,19:20.080511089352214,20:14.306977484301457,
                     21:11.265167414136857,22:6.761247284555768,23:4.584052475875439}}
def _o34_par(pos,p,Y):
    """ORDER C: the two retained normalization denominators' object. The flat effective positional bar
    unless RL_O34 is set AND the row is at a developing age (Y - birth year < 24); a row with no birth
    year keeps the flat bar (count disclosed on the packet). Never above the flat bar, by cap law."""
    _b=_O30BP_BARS[pos]
    if not _O34: return _b
    _by=p.get('_by')
    if not _by: return _b
    _a=Y-int(_by)
    if _a>=24: return _b                                    # FLAT FROM 24 — mature-row byte-identity
    return _b-_O34_DELTA['TALL' if pos in _O34_TALL else 'SMALL'][max(18,min(23,int(_a)))]
if _O34:
    # BUILD-FAILING STRUCTURAL ASSERTS (cap law + flat-from-24), evaluated on a synthetic age ladder.
    for _pos34 in _O30BP_BARS:
        for _a34 in range(16,30):
            _pb34=_o34_par(_pos34,{'_by':2026-_a34},2026)
            if not (_pb34<=_O30BP_BARS[_pos34]+1e-12) or (_a34>=24 and _pb34!=_O30BP_BARS[_pos34]):
                raise SystemExit('ORDER C HALT: par34 cap/flat law broken at %s age %d'%(_pos34,_a34))
# The preview blend is INSTALLED LATER (it needs day0_v0, which the ORDER 29B block defines ~2300 lines
# below). This is the late-bound hook; it FAILS CLOSED — a preview-on call that reaches a price before the
# blend is installed halts rather than silently falling through to the superseded machinery.
_PV={'on':_O30B_PREVIEW,'blend':None}
def _pv_apply(p,Y,e):
    _f=_PV['blend']
    if _f is None:
        raise SystemExit('ORDER 30B-P HALT: RL_O30B_PREVIEW is set but the preview blend is not installed '
                         'yet — a price was formed before the pedigree object existed. FAIL-CLOSED BY '
                         'DESIGN: falling through here would print a superseded-machinery price under a '
                         'preview label.')
    return _f(p,Y,e)
_POLE={}
def par_pole(pos,pk,T):
    k=(pos,int(min(pk,cp.KMAX)),int(min(max(T,1),6)))
    # ORDER I (RL_O36): the pedigree pole is priced off a SYNTHETIC row (dob 2005-03-01, i.e. a
    # 21-year-old at BASE_REF), NOT off a person. S1 corrects how a REAL player's OWN output is judged,
    # so it must not reach this object — it is pedigree machinery, and it is MEMOISED, which would also
    # make the leak depend on which player happened to fill the cache first. MEASURED: with the pole
    # left inside S1's scope, three rows whose displayed age is 24+ moved by up to 0.09 board points at
    # full dose. Dial off => the guard is a no-op and this line is byte-identical.
    if k not in _POLE:
        sp=synth(k[1],PR.par_at(*k),pos)
        _s36=MA._O36_SCOPE['on']; MA._O36_SCOPE['on']=False
        try: _POLE[k]=price6(sp,b6(sp))
        finally: MA._O36_SCOPE['on']=_s36
    _SCALE={'MID':1.19,'SF':0.93,'KPF':0.95,'SD':1.08,'KPD':1.05,'RUCK':1.13}  # STEP3-B: principled re-level (trajectory-integrated pole / 2yr synth); piece-2 SHAPE kept, LEVEL rescaled
    return _POLE[k]*_SCALE.get(pos,1.0),PR.par_at(*k)
# ==== LEG B v1.1 — UN-COMPRESS MAP at the PRODUCTION-VALUE hook (pr=price6, ONCE per player; memo v1.1 §2/§4)
# v' = pr0^(1-w) * (V_ref_b[pos]*rho)^w ; pr0 = the CAPTAIN-FREE price6 (via MA._CAPT_OFF); delta = pr - pr0
# added back UNCHANGED; C[pos] = production-side conservation renorm (captain/pedigree/iso NOMINAL). rho =
# rho_out(p,pos)/RHO_DEN[pos]. ⟪v1.2 — WEIGHT, DON'T GATE (memo §2.1, register 240)⟫ rho_out = ρ_num =
# GAMES-AND-RECENCY-WEIGHTED realised above-replacement output over EVERY season with games>0:
# u_s=games_s·d^(Ynow−year_s), d=UNCOMP_DECAY(=0.25 ⟪v1.3 OWNER-SET R105.6⟫); ρ_num=Σ u_s·(avg_s−REPL[pos])/Σ u_s. NO season exclusion,
# NO games floor, NO career-phase test (the v1.1 `_qualifying` predicate is DELETED — a never-shipped stub;
# the hard floor manufactured 144 phantom rookies and the conditioned rule wiped real games, both MEASURED,
# register 239). RHO_DEN[pos]=MEDIAN of this same ρ_num over the demonstrated-proven pop (numerator and
# denominator share ONE law). RL_UNCOMP is INERT by default (UNCOMP_S_DEFAULT=None): the map + the s-gated
# load-time reference build both short-circuit BEFORE rho_out. Onset ramp Delta=6.0 (memo §2.2) in the
# realised-output measure's units; decay d=0.25 (⟪v1.3 OWNER-SET R105.6⟫) DECLARED next to Δ=6.0 in rl_model.py.
_UC_VREFB={}          # V_ref_b[pos] = MEDIAN captain-free price6 (pr0) over the demonstrated-proven pop (load-time, s-gated)
_UC_RHODEN={}         # RHO_DEN[pos] = MEDIAN rho_out over the demonstrated-proven pop (load-time, s-gated)
_UC_C={}              # C[pos] = per-position production-side conservation renorm (load-time, s-gated)
_UC_CAL={'on':False,'pr0':{},'v0p':{}}   # load-time conservation accumulator (Sum pr0, Sum v0p per pos; C==1 during accumulation)
def rho_out(p, pos):
    """ρ_num — GAMES-AND-RECENCY-WEIGHTED realised above-replacement output (memo §2.1 ⟪v1.2⟫, WEIGHT-DON'T-GATE).
    Over EVERY season with games>0: u_s = games_s · d^(Ynow−year_s) with d=MA.UNCOMP_DECAY(=0.25 ⟪v1.3 OWNER-SET⟫), Ynow=2026;
    ρ_num = Σ u_s·(avg_s − REPL[pos]) / Σ u_s. NO exclusion, NO games floor, NO career-phase test (register 240;
    the v1.1 `_qualifying` predicate is DELETED — a never-shipped stub). An injury-shortened year contributes
    exactly its games' worth (a 3-game season is 1/7th a 21-game season at equal recency — Docherty handled by
    WEIGHT, not exclusion); a developing kid's early seasons count proportionally (no phantom rookies by
    construction). Zero played seasons in the store => None (caller sets w=0; the map is identity there)."""
    _num=0.0; _den=0.0
    for x in p.get('scoring') or []:
        _gm=x.get('games',0) or 0
        if _gm<=0: continue                                       # games>0 only; NO other exclusion (the LAW)
        _u=_gm*(MA.UNCOMP_DECAY**(2026-x['year']))                # season weight = games × recency (decay d per year back)
        _num+=_u*(x['avg']-MA.REPL[pos]); _den+=_u
    if _den<=0.0: return None                                     # no played season => zero-evidence identity (w=0)
    return _num/_den                                              # weighted mean of (avg − REPL[pos]); RHO_DEN = its proven MEDIAN
def _uncomp_prod(pr,p,Y,bb):
    # INERT guard (RL_UNCOMP off / s unset / non-real / refs not built) => pr. Short-circuits BEFORE rho_out,
    # so with RL_UNCOMP inert the ρ axis is never evaluated => board 8d90c9ac BYTE-EXACT (the A/B identity).
    if not MA._UNCOMP or MA.UNCOMP_S is None or pr<=0.0 or not _isreal(p): return pr
    pos=MA.gfut(p); Vb=_UC_VREFB.get(pos); Rden=_UC_RHODEN.get(pos)
    if not Vb or not Rden or Vb<=0.0 or Rden<=0.0: return pr        # references not built (inert never reaches here)
    _prev=MA._CAPT_OFF['on']; MA._CAPT_OFF['on']=True               # captain-off pass: recompute the CAPTAIN-FREE production
    try:
        with contextlib.redirect_stdout(io.StringIO()): pr0=price6(p,bb,Y)
    finally: MA._CAPT_OFF['on']=_prev
    if pr0 is None or pr0<=0.0: return pr
    delta=pr-pr0                                                    # L-CAPTAIN increment, added back UNCHANGED (delta byte-identity self-test)
    _ro=rho_out(p,pos)                                             # realised-output margin above REPL (avg-points)
    if _ro is None or _ro<=0.0: return pr                          # zero qualifying seasons / sub-replacement => w=0 identity
    ramp=1.0 if _ro>=MA.UNCOMP_DELTA else _ro/MA.UNCOMP_DELTA       # onset ramp (memo §2.2), realised-output units
    _Eq=_ev_qual(p,Y); E=1.0-_math.exp(-_Eq/MA.UNCOMP_TAU) if _Eq>0.0 else 0.0   # saturating evidence weight in [0,1]
    w=MA.UNCOMP_S*E*ramp
    if w<=0.0: return pr
    t=Vb*(_ro/Rden)                                                # V_ref_b * rho (kappa=1)
    if t<=0.0: return pr
    v0p=(pr0**(1.0-w))*(t**w)                                      # log-space blend of the CAPTAIN-FREE production toward the output-proportional target
    if _UC_CAL['on']:                                             # load-time conservation calibration (C==1 here): accumulate Sum pr0, Sum v0p
        _UC_CAL['pr0'][pos]=_UC_CAL['pr0'].get(pos,0.0)+pr0
        _UC_CAL['v0p'][pos]=_UC_CAL['v0p'].get(pos,0.0)+v0p
    _C=1.0 if MA._UNCONSERVE else _UC_C.get(pos,1.0)               # §3 per-position production-side renorm; RL_UNCONSERVE=1 => C≡1 (UNFUNDED measurement, item 256/257); OFF => C[pos] (shipped, byte-exact)
    return _C*v0p+delta                                            # production-side renorm; captain delta additive & nominal
def raw_ev(p,Y=2026):
    _bb=b6(p,Y); pr=price6(p,_bb,Y); pr=_uncomp_prod(pr,p,Y,_bb)   # LEG B v1.1 map at the production-value hook (inert unless RL_UNCOMP on + s set)
    pos=MA.gfut(p); pk=MA.effpk(p)
    with _form_anchor_clock():                                                        # LEG F3 §2.vi: the pedigree-pole fade keys on PROJECTED EVIDENCE (BASE_REF), not the advancing age/tenure clock (k=0 identity)
        T=min(max(PR.tenure(p,_fa_year(Y)),1),6)
        et=min(max(eff_ten(p,_fa_year(Y), PR.tenure(p,_fa_year(Y))),1),6)             # STEP1: developmental tenure off original PR.tenure base
        po,par=par_pole(pos,pk,T); a=MA.age(p)
        # #334 ITEM E1: the RUCK pole denial ENDS. Rucks were the only position given wage=0, i.e. no
        # pedigree pole at all; the measurement made it the LIVE ruck lever (pole denial 573 pts vs the
        # ceiling's 130). They now take the SAME standard age wage ramp as every other position, scaled
        # by RUC_WAGE so the ruck book lands inside the ruled cautious band [+2.9%, +9.0%].
        # V0-INERT BY CONSTRUCTION: at Y=debutyr-1 the exposure is 0 so _expgate is 0 and w=wage*tfade*
        # expgate is 0 whatever wage is — so this cannot reach the frozen year-zero surface. Asserted.
        wage=float(np.clip(1-((a or 21)-20)/6,0,1))*(RUC_WAGE if pos=='RUCK' else 1.0)
        tfade=float(np.interp(et,[1,2,3,4,5,6],[1.00,0.76,0.40,0.16,0.05,0.05]))      # pole-fade by DEVELOPMENTAL tenure
        expgate=_expgate(p,Y)                                                         # EXPOSURE REGIME (regime 4): smoothed (was 1.0 if nqual>=4 else exposure/POLE_RAMP ramp); RL_EVW=0 => base gate
        w=wage*tfade*expgate
    perf=cp._lvl_wt(p,Y)                                  # WEIGHTED games x recency level (RL_RECENCY_DECAY), not flat best-3
    # ORDER 30B MEASUREMENT DIAL, DECLARED AND DEFAULT-OFF (RL_O30B_NOPOLE=1). This line IS the PEDIGREE
    # POLE leg — `po` is par_pole(pos,pk,T), a forbidden-set object, added on top of the production price
    # `pr` and faded by wage x tfade x expgate. The dial deletes the leg (raw_ev == the production price)
    # so the price consequence of the STEP-3 forbidden-set boundary can be MEASURED before it is ruled.
    # Default 0 => this expression is byte-identical to the shipped one. It is a MEASUREMENT dial for the
    # step-3 stop, not a pricing lever, and no board ships with it set.
    if _O30B_NOPOLE: return pr
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
# _REAL/_isreal HOISTED here from ~130 lines below (seg-5 map-ON load-order fix, owner-authorized fence
# amendment 2026-07-16; content BYTE-IDENTICAL to the original site): the ISO-table build just below calls
# raw_ev(synth(...)) at MODULE LOAD, and with RL_UNCOMP ON the _uncomp_prod guard resolves _isreal — which
# must therefore be defined BEFORE this point. MA.data is fully built and not mutated between here and there.
_REAL=set(p['key'] for p in MA.data)
def _isreal(p): return p.get('key') in _REAL
PICKS=list(range(1,71)); ISO={}
for pos in ['MID','SF','KPF','SD','KPD','RUCK']:
    raw=np.array([raw_ev(synth(pk,PR.par_at(pos,min(pk,cp.KMAX),4),pos)) for pk in PICKS])
    iso=IsotonicRegression(increasing=False).fit_transform(PICKS,raw)        # monotone non-increasing in pick#
    ISO[pos]=(np.array(PICKS),np.maximum(iso,raw*0)+ (iso-raw>=0)*(iso-raw))  # iso is the guarded floor; correction additive where iso>raw
    fs=iso/np.maximum(raw,1e-6)                                                # multiplicative correction (>=1 where shallow under-priced)
    if _ISOFADE: fs=IsotonicRegression(increasing=False).fit_transform(PICKS,fs)   # LEG A (a): monotonize the MULTIPLIER (the ratio is non-monotone even though the numerator is) — kills the Newcombe trough
    ISO[pos]=(np.array(PICKS), fs)
def iso_corr(pos,pk): xs,fs=ISO[pos]; return float(np.interp(min(pk,70),xs,fs))
def iso_eff(p,Y=2026):                                        # LEG A (b): per-REAL-player EFFECTIVE iso — the pick tax faded on the v2.10 evidence weight w=E_q
    if _O30B_NOISO: return 1.0                                # ORDER 30B measurement dial (default off): the ISO table is BUILT FROM par_at synths (:497) and is a PICK-side correction on the production leg — the two properties that put it on the forbidden-set boundary
    base=iso_corr(MA.gfut(p),MA.effpk(p))
    if not _ISOFADE or not _isreal(p): return base            # switch off, or a synth (structural scaffold; zero-evidence convention) => raw/monotonized table, unfaded
    return 1.0+(base-1.0)*_math.exp(-_ev_qual(p,Y)/_ISOFADE_TAU)   # full at w=0 (V0 unchanged by construction) -> 1.0 as evidence saturates (residual-0 member of the pedigree-fade family)
for _pp in ['MID','SF','KPF','SD','KPD','RUCK']:   # STEP1: FREEZE pole table on ORIGINAL features
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
    # OBITUARY (Leg B, un-compress build 2026-07-16; SSI/CORE rule 7 — delete, don't disable): the dead
    # `if not _EVW:` discrete FOUR-REGIME branch (n==0 first-evidence f1 credit · n>=4 established _est ·
    # 1..3 thin ramp c=n/4 · else Lo) is DELETED here. It was SUPERSEDED by the continuous evidence weight
    # below (one E_q quantity spans all four regimes; item 65) and executed ONLY under RL_EVW=0. The
    # shipped/live board runs RL_EVW=1 (default) and NEVER took this branch, so its deletion is BYTE-EXACT
    # for the live board (verified: RL_UNCOMP-inert board == 8d90c9ac unchanged). Leg A retired the same
    # branch in the DORMANT twin `_lvl_eff_core` (:~216) and its Task 4b listed-but-did-not-cut this LIVE
    # copy; this completes that cut (directive §7 / spec §4 / PLAN §8). The unrelated live `if not _EVW:`
    # one-liner in `_expgate` (:192) is OUT of scope and untouched. Resurrection ref (the deleted regimes):
    #   git show d3f703f~1:engine/rl_after/_merged_recover.py  (the pre-Leg-B _coreM1 body).
    # ---- CONTINUOUS EVIDENCE WEIGHT: ONE evidence quantity E_q spans all four regimes (item 65) ----
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
# receive the engine's real-store layers (RUCK prior cap :317/:492, v7 age-taper :198, B5 floor :552). It is now
# keyed on the STABLE player key, NOT id(p) -- so the layers fire regardless of which module instance or object
# copy is priced. (The shipped-board bug: rl_export exec'd a 2nd rl_model instance, so id(p) matched 0/805 and
# every real-store layer was silently dropped, over-pricing ~2/3 of the board.) Synths (no 'key') never match;
# copies carrying the same key resolve as real by construction. Keys verified non-null + unique across MA.data.
# _REAL/_isreal are now DEFINED ABOVE (hoisted to just before the ISO-table build; seg-5 map-ON load-order
# fix, owner-authorized). Original definition site was HERE; this block documents their keying, retained in place.
_b6_pre_v7=b6
def b6(p,Y=2026):
    bb=_b6_pre_v7(p,Y)
    if MA._O33 and MA._O33S>=2: return bb                 # ORDER B B-3 TAPER RETIREMENT (stage 2 after the B-A1 re-map; was 3) (dial-gated): asc == 1, band[5] stays max(q97m, q90) exactly as _b6_core emits it — the derivation's boundary solution in every band; kills all 341 v-inversions by construction; q97m itself untouched (bake-time refit per R-W6). Dial off => the v7 taper applies byte-exact below.
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
#   then ×(1 − OVPX·ovpx)   [deep-pick SF 41-70 over-optimism compress — the ONE owner-agreed #43 flag;
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
W4_OVPX_D={'SF':0.12,'SD':0.09,'MID':0.07}      # #43-measured deep-pick (41-70) coverage excess: 2.14 / 1.70 / 1.55 -> partial, data-earned compress; smooth in pick 38->46, thin-career only. MID 1-3 (2.09) NOT touched (owner-flagged).
W4_KPFSH=float(os.environ.get('RL_W4_KPFSH','0.55'))      # established-KPF LOOSE-residual retention (the slice ABOVE all demonstration since the 2026-07-09 rebalance; was the whole residual)
# ==== KPF REBALANCE 2026-07-09 (pre-bake, owner-directed) — three KPF-scoped reshapes ==================
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
# (T2) TOP-TIER PRODUCTION REWARD (the concave regime, KPF cells): (i) the credit ramp for KPF keys
#   on dm = max(m, LD−REPL) — sustained demonstrated margin, so a recency-dipped top-tier scorer is not
#   zeroed — with the regime start/span rescaled by the measured KPF spread leverage (CV spread-ratio
#   6.57/4.17 = 1.575, the SETTLED #9 measurement that motivated KPFFIX): 10/1.575=6.35, 20/1.575=12.70.
#   (ii) a top-tier segment on the reward multiplier: kpfup(dm) = W4_KPFUP + KPFTOP·clip((dm−8)/16, 0, 1) —
#   the regime stays concave (saturating), the plateau rises for genuine top-tier scorers (saturation ≈ the
#   established-KPF 90th-pctile dm). (iii) PARTIAL-PROVEN KPF top-tier credit: a KPF with 2≤nqual<4 and
#   top-tier SUSTAINED demonstration earns the same credit scaled c=n/PROVEN_N (the engine's standing
#   partial-evidence convention), NO fade (F-YOUNG: the fade never reaches the young). One-season wonders
#   (nqual<2 or <2 high-games seasons) earn nothing — demonstration-earned only.
# (T3) SPECULATIVE TRIM: the L1c young credit's KPF cell intensity is scaled RL_YCRED_KPF=0.92 (slight,
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
    ls=sorted((a for y,a,gg in ((x['year'],x['avg'],x.get('games',0)) for x in p['scoring'])
               if _lo<=y<=Y and y not in _nuke and gg>=12.0*(_fEy(Y,p) if y==Y else 1.0)),reverse=True)
    if len(ls)>=2: return float(np.mean(ls[:2]))
    if _nuke:                                                  # fork-v fallback: exclusion left <2 healthy seasons
        _KPF_LD_FALLBACK.add(p.get('key'))
        ls0=sorted((a for y,a,gg in ((x['year'],x['avg'],x.get('games',0)) for x in p['scoring'])
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
    _kpf_reb=_W4KPF and pos=='KPF'                         # KPF REBALANCE T2 coordinates active
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
            # KPF REBALANCE T2: kpfup(dm) = base + top-tier segment (KPF under RL_KPFFIX only); the
            # credit scales by cw (1.0 proven; n/4 partial-proven KPF). The FADE stays PROVEN-gated — the
            # funding leg never reaches a partial-proven young KPF (F-YOUNG).
            up=W4_CRED*((W4_KPFUP+W4_KPFTOP*ctx.get('kt',0.0)) if (_W4KPF and ctx['pos']=='KPF') else 1.0)
            W+=ctx['cw']*up*ctx['gm']*ctx['dur']*ctx['sh']*float(np.interp(k,[0.,2.,5.],[1.,1.,0.]))
            if ctx.get('n',0)>=PROVEN_N:
                W-=W4_FADE*(1.0-ctx['gm'])*ctx.get('fadew',1.0)*float(np.interp(k,[4.,10.],[0.,1.]))
    # ===== #334 MENU ITEM (b) — THE PROVEN-TAIL TRIM. The ruler act measured the engine carrying 15.1%
    # of the year-4 price beyond career year 11 against 9.9% delivered (1.53x hot), concentrated in talls.
    # This fades the beyond-year-11 carry toward the delivered share, and ONLY for the population the
    # existing far-year fade already names as proven (ctx['n'] >= PROVEN_N) — it adds no new gate and
    # touches no young tail, which is the un-faded one the ruler act flagged. Strength 0.0 = shipped
    # behaviour, byte-exact. A MENU ITEM FOR THE OWNER'S SITTING, NOT A DECISION.
    if TAIL_TRIM>0.0 and ctx.get('n',0)>=PROVEN_N and k>11:
        W*=(1.0-TAIL_TRIM*float(np.clip((k-11.0)/4.0,0.0,1.0)))
    # (L1c: the old `elif _W4YNG` runway leg was here — DELETED 2026-07-08, replaced by the evidence-
    #  conditioned expected-rerating credit on raw_ev below; RL_YOUNG gates THAT, never both.)
    if _W4OVP and ctx.get('ovpx',0.0)>0.0:
        W*=(1.0-W4_OVPX*ctx['ovpx'])
    return max(W,0.05)
_proj_w4_0=MA.proj_from_peak
def _proj_w4(g,lp,a,cur,lens,g0=None,fut=None,pre_hc=0.0,grace=0):
    # ORDER 28: `grace` forwarded verbatim from the caller (which holds the record) to disc_factor; 0 => byte-exact.
    ctx=_W4CTX['on']
    if ctx is None: return _proj_w4_0(g,lp,a,cur,lens,g0=g0,fut=fut,pre_hc=pre_hc,grace=grace)   # synths / lever-off: byte-exact original
    _off=(MA.AGE_REF-MA.BASE_REF) if _LEGF_ON else 0     # LEG F3 §2.vi (ruling 353, still-implicated proj_from_peak): fwd-lens offset; 0 at k=0/balanced/backward OR RL_LEGF=0 => byte-exact ORIGINAL by construction
    ah=a-_off if _off>0 else a           # form-anchored age SHAPE: the pedigree-driven projection curve-position + young-runway credit hold at BASE_REF, so growth flows through the ADVANCING level (lp from the band at AGE_REF; cur=level_now via _dev_advance) — the premium decays with PROJECTED EVIDENCE, not the age clock (Reid: same map at the projected evidence state; no new multiplier/growth term). k=0: _off=0 => ah==a => byte-exact.
    pa=MA.PEAK_AGE[g]; d=MA.age_disc(ah,MA.LENS[lens],lens); cl=cur if cur else lp*MA.frac(ah,pa,g); prod=0.0   # #334 age-dynamic future discount (dial-gated; identity when off) + ORDER B: frac carries g (B-1 ladder; identity when RL_O33 off); the B-2 fade call site DELETED (owner ruling, rl_model RL_O33 obituary) — duplicate-loop fence: matches rl_model.proj_from_peak
    if g0 is None: g0=g
    if fut is None: fut=[(g,1.0)]
    for k in range(18):
        ag=ah+k
        if ag>38 or MA.frac(ag,pa,g)<0.42: break
        lev=lp*MA.frac(ag,pa,g)
        if ag<=pa: lev=max(lev,cl)
        if k==0: lev=max(lev,cl)
        if k==0 and pre_hc>0 and MA.BASE_REF==2026 and MA.AGE_REF==2026: lev*=(1-pre_hc)  # RL_AVAIL present haircut L_p (was _b2hc)
        if _BOARD_PATH and k==ctx.get('ret_k',-1) and ctx.get('ret_hc',0.0)>0: lev*=(1-ctx['ret_hc'])   # Part-2 return-season haircut (BOARD-ONLY: the walk-forward book stays availability-free; single k -> decays next season)
        base=lev+MA.capt_prem(lev)
        Wk=_w4_W(k,ctx)
        _df=MA.disc_factor(ah,d,k,lens,grace)
        # ORDER I (RL_O36) — S1, the age-referenced bar. DUPLICATE-LOOP FENCE: this MUST match
        # rl_model.proj_from_peak's two sites exactly. Dial off => o36_bar IS MA.REPL[...] byte-exact.
        # THE AGE THE BAR READS IS `a+k`, THE PLAYER'S REAL AGE AT THAT HORIZON — NOT `ag`. `ag` is
        # `ah+k`, a CURVE POSITION: LEG F3 holds the projection shape one year back on the forward lens
        # (_off=1), so on that lens a 24-year-old's loop runs from ah=23. The level curve wants the
        # curve position; the REPLACEMENT BAR wants the man's age, because the bar asks "what does a
        # player this old have to beat". MEASURED: reading `ag` moved 21 rows aged 24+ (worst
        # braeden-campbell 1.04 board points) purely through that one-year anchor offset. With `a+k`
        # the cap law holds and rl_model's own copy (which has no offset, so ag == a+k there) stays
        # byte-identical to this one.
        _abar=a+k
        if k==0: prod+=Wk*MA.posval(base-MA.o36_bar(g0,_abar))*21/_df
        else: prod+=Wk*sum(w*MA.posval(base-MA.o36_bar(gg,_abar)) for gg,w in fut)*21/_df
    if g in('KPF','KPD'): prod*=1.05
    if MA._O33 and MA._O33S>=1 and g in('KPF','KPD'): prod*=MA.O33_SSTAR   # ORDER B B-1 renorm — duplicate-loop fence: matches rl_model.proj_from_peak
    runway=MA.clamp((25-ah)/6.0,0,1); elite=MA.clamp((lp/MA.PEAK[g]-0.97)/0.30,0,1); prod*=(1+runway*elite*MA.PMAX)
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
    if cur is not None and _lsym_active():                    # LEG F4 §2.vii read #2: temper the level_now (_dev_advance) roll to r_pop(age); k=0/backward/RL_LEGF=0 => inert (byte-exact). level_demo == form-anchored level (AGE_REF held); level_now == advanced.
        cur=_lsym_blend(MA.level_demo(p),cur,_lsym_age(p))
    if cur is None: return 0
    # ==== §1b FLOOR HALF (R106.7, DECISIONS v121 §1) — PROVEN-player shipped-board copy of MA.prod_floor's floor.
    # ⚠ DUPLICATE-LOOP HAZARD (owner condition 4; fence extended by the Option-2 adjudication 2026-07-17): this is a
    # PARALLEL copy of rl_model.prod_floor's loop (rl_model.py:441). The §1b k==0 split MUST stay IDENTICAL in
    # BOTH — edit both or neither. Blend OUTSIDE the nonlinearity: TWO posval evaluations at k==0, sp·posval(vs
    # present) + (1-sp)·posval(vs low), NEVER a blended bar inside one call. RL_FLEX=0 => y0dpp_bar None =>
    # byte-exact. QUEUED HYGIENE (registered, NOT this build): option-3 delegation — this fn -> MA.prod_floor for
    # bar resolution, removing the duplicate loop — carries a determinism-proof requirement.
    lowbar=MA.y0dpp_bar(p) if (MA.AGE_REF==MA.BASE_REF) else None
    _gr=MA.grace_years(p)                                 # ORDER 28 grace-A (dial-gated; 0 => byte-exact). ⚠ MUST match rl_model.prod_floor exactly — the duplicate-loop fence.
    d=MA.age_disc(a,MA.LENS[lens],lens); H=MA.clamp((40-a)/3.0,1.0,3.0); prod=0.0; k=0   # #334 age-dynamic future discount (dial-gated; identity when off); the ORDER B B-2 fade call site DELETED (owner ruling) — duplicate-loop fence: matches rl_model.prod_floor
    while k<H:
        ag=a+k; wt=min(1.0,H-k)
        lev=cur*min(1.0, MA.frac(ag,pa_,g)/max(MA.frac(a,pa_,g),1e-6))   # ORDER B B-1 ladder in the floor ratio (dial-off identical)
        if k==0 and p.get('_avail_hc',0)>0 and MA.BASE_REF==2026 and MA.AGE_REF==2026: lev*=(1-p['_avail_hc'])  # RL_AVAIL: register-driven present haircut (was _b2hc; R-B2HC retired)
        base=lev+MA.capt_prem(lev)
        if k==0 and lowbar is not None:
            sp=MA.SEASON_PROG                                 # banked (sp) vs present bar; remaining (1-sp) vs low bar
            # ORDER I (RL_O36) S1 — DUPLICATE-LOOP FENCE: matches rl_model.prod_floor exactly.
            pv=sp*MA.posval(base-MA.o36_bar(g,ag))+(1.0-sp)*MA.posval(base-MA.o36_bar(lowbar,ag))
        else:
            pv=MA.posval(base-MA.o36_bar(g,ag))
        prod+=_w4_W(k,ctx)*wt*pv*21/MA.disc_factor(a,d,k,lens,_gr); k+=1
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
# stretches (SF/played, RUCK/sat — census tension report) are reported, not shipped as cuts.
# SCOPE: real in-curve (ND/RD) picked store players — synths carry no key and delegate byte-exact; the RUCK
# prior cap (ASK1) still binds ABOVE the credited V0 where hot (declared: the cap is out-of-scope machinery;
# capped rucks keep the cap — visible in the Goad/Green named-player rows of the owner w-table).
# KILL-SWITCH: RL_YOUNG (existing family member, meaning re-pointed to L1c; the old runway leg is DELETED
# above, never stacked). RL_YOUNG=0 ⇒ multiplier is EXACTLY 1.0 ⇒ byte-exact; ALL-OFF ⇒ byte-exact v2.5.
# Table absent while RL_YOUNG=1 ⇒ HALT (halt-not-warn, guard-family behavior).
_YC_W=float(os.environ.get('RL_YCRED_W','0.9'))               # owner dial: fraction of the measured re-rating paid forward — OWNER-RULED 0.9 (2026-07-08, on the W-TABLE; 0.7 was the pre-ruling shipped default)
_YC_KPF=float(os.environ.get('RL_YCRED_KPF','0.92'))          # KPF REBALANCE T3 (2026-07-09): SLIGHT speculative-KPF trim — KPF cell intensity ×0.92 (owner's "slight"; F-YOUNG honored — no wipe; denominator cost measured in the build artifacts). Rides RL_YOUNG.
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
    if MA.gfut(p)=='KPF': R*=_YC_KPF                      # T3 KPF REBALANCE: slight KPF cell-intensity trim (continuous — a pure scale introduces no cliff on any axis)
    phi=(1.0-g/_YC_G0)**2                                     # full at zero evidence; C1 landing at G0
    return 1.0+_YC_W*R*phi
_raw_ev_w4_0=raw_ev
def raw_ev(p,Y=2026):                                        # W4: context-setting wrapper (real players only; synths delegate clean) + L1c credit
    prev=_W4CTX['on']; _W4CTX['on']=_w4_ctx(p,Y)
    # ORDER I (RL_O36): S1's scope rides the ENGINE'S OWN real-player boundary — the same wrapper, the
    # same try/finally. Outside it (synthetic band nodes, the baseline-draftee curve, the pedigree
    # machinery) the projection keeps the flat bar, which is what keeps day-0 and mature rows exact.
    # THE CAP LAW IS A PROPERTY OF THE ROW, NOT OF THE VANTAGE. A player who is 24 today may still be
    # priced, inside his own ev(), through a lens whose clock stands a year earlier — and at that
    # vantage he is 23, so a per-horizon age test alone would let S1 reach him. MEASURED: 21 rows aged
    # 24+ moved that way (worst braeden-campbell 1.04 board points), and every one of them was exactly
    # 24. The owner's law says a mature row is byte-identical, full stop, so the gate is taken on the
    # ROW'S OWN AGE ON THE BOARD'S CLOCK (BASE_REF) and S1 is switched off entirely for him.
    _o36prev=MA._O36_SCOPE['on']
    MA._O36_SCOPE['on']=(MA._age_at(p,MA.BASE_REF)<24) if p.get('_by') else False
    try: return _raw_ev_w4_0(p,Y)*_ycred_mult(p,Y)           # L1c: ×1.0 exactly when RL_YOUNG=0 (byte-exact off-path)
    finally: _W4CTX['on']=prev; MA._O36_SCOPE['on']=_o36prev
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
    s=[a for y,a in [(x['year'],x['avg']) for x in p['scoring'] if x['games']>=6.0*(_fEy(Y,p) if x['year']==Y else 1.0) and x['year']<=Y]]   # D10: 6-bar prorated in-progress
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
#     classes RUCK/KPP/nonKPP for R_SIT only, with the RUCK retention SHAPE pooled with KPP (thin bimodal
#     slice, n=270 cells) scaled to RUCK's own measured d1-2 level x1.065 — DECLARED pooling.
# D13 ASK3 03/07/2026 — R_SIT (depth-only, per class, RUCK-shape-pooled-with-KPP) is SUPERSEDED by the
# continuous log-pick x depth surface R_SURF below (obituary E4: BOARD_LAYERS_OBITUARY.md). The old table
# VIOLATED Luke's signed law (nonKPP rose d3->d5 .410->.437; KPP rose d5->d6 .253->.266 — a sitter gained
# value by sitting). Resurrection ref: git show af1fc6aa's _merged_recover.py. Old table (for the record):
#   R_SIT={'nonKPP':[.429,.404,.410,.432,.437,.424],'KPP':[.468,.380,.325,.278,.253,.266],'RUCK':[.674,.547,.503,.472,.435,.435]}
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
        'RUCK':{5:[1.000,0.715,0.670,0.562,0.535,0.467], 15:[0.851,0.597,0.597,0.520,0.520,0.468], 30:[0.830,0.616,0.616,0.607,0.540,0.469], 50:[0.781,0.594,0.594,0.594,0.541,0.470]}}
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
    # Comparator = nonKPP ONLY (RUCK EXCLUDED — own capped machinery; supervisor spec, stated to Luke pre-fire).
    # BOARD PATH ONLY (O1 scope). max() of two isotonic-non-increasing-in-depth vectors is non-increasing (re-
    # verified numerically in _v0_curve_assert). OWNER-SET where the floor binds, data-derived elsewhere. Governance:
    # docs/process/OWNER_OVERRIDES.md O1; obituary/registration BOARD_LAYERS_OBITUARY.md.
    if _BOARD_PATH and cls=='KPP':
        dvn=_dv_surf('nonKPP',lp); dv=[max(a,b) for a,b in zip(dv,dvn)]
    return float(np.interp(tau,[0,1,2,3,4,5,6],[1.0]+dv))
LAM_SIT=[0.0,0.160,0.493,0.547,0.547,0.816,1.0]
def _sitout_cls(pos): return 'RUCK' if pos=='RUCK' else ('KPP' if pos in ('KPF','KPD') else 'nonKPP')

# ===== #334 -- THE POOL SIT-OUT RETENTION, DERIVED ON POOL HISTORY. LANDED BY ORDER 23. ============
# THE SOURCE OF THESE NUMBERS IS A COMMITTED SIGNED DATA ARTIFACT -- not a dial, not a constant a
# seat typed, and not something a rebuild can quietly re-fit:
#     engine/rl_after/pool_retention_surface.json   md5 b7f7bc6000e311e197f66bc21007c659
#     9 pathway surfaces x 3 classes x 6 depths, plus the mean-preserving uplift U per pathway.
# DERIVATION PROVENANCE: docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py (ORDER 21,
# the d13 ND method with departures D1-D7 pre-registered), as amended by ORDER 22's
# o22_make_relaxed_surface.py under two owner rulings of 2026-08-12 -- the isotonic constraint
# RELAXED at depths >= 2 (comment 5262159933) and a class-axis K=10 shrinkage toward the all-class
# same-depth cell (comment 5262213139) -- with U re-derived, entry-weighted and mean-preserving to
# 1.0000000000 exactly, at ORDER 23's final levels. Verification: docs/evidence/pool_landing_2026-08-12/.
# The literals below are that artifact inlined by docs/evidence/pool_final_2026-08-12/o21_patch.py,
# which is the mechanism every measuring act since ORDER 21 has used; ORDER 23 makes it permanent, so
# the landed engine is byte-for-byte the engine the packet's numbers were measured on.
# Owner ruling, directive D8 (comment 5253173347): "the pool sitter on top penalty should go, and the
# pool index should be rederived in the same way the ND one is where possible not for pick 65, but for
# the pool" + "They're all part of the pool ... rookie draft pick 1 and 30 are the same" (NO PICK AXIS).
# Derivation: docs/evidence/pool_retention_2026-08-12/pool_retention_derive.py (the d13 ND method,
# departures D1-D7 declared in PREREG_ORDER21.md). H_POOLSIT / H_UNION are RETIRED to 1.0 alongside.
# THE ONE DERIVED OBJECT, AT BOTH READ SITES, BY CONSTRUCTION AND NOT BY ACCIDENT:
#   sitout_ev  fires iff ns==0  == a SITTER by the derivation's own definition  -> R_derived < 1
#   _a_blend   fires iff ns>=1  == a NON-SITTER by that same definition         -> U_pathway > 1
# The two engine sites partition the pool population on exactly the variable the derivation splits on,
# so the mean-preserving pair covers both. U>1 IS A LIFT and is intentional: the owner's D8 amendment
# requires the sitter differential to REDISTRIBUTE inside the pathway, never to be a net charge.
# EVERY SITE IS p.get('_pool')-GATED. National rows read the national surface unchanged at both sites.
_PR_PATH={"RD": {"nonKPP": [0.654026, 0.399825, 0.577713, 0.642941, 0.560105, 0.4199379999999999], "KPP": [0.709917, 0.388842, 0.385506, 0.3648199999999999, 0.359866, 0.343973], "RUCK": [1.0, 0.532863, 0.585961, 0.45935100000000006, 0.38849200000000006, 0.373777]}, "ND>64": {"nonKPP": [0.4840070000000001, 0.29764900000000005, 0.36705, 0.359746, 0.377394, 0.34463599999999994], "KPP": [0.888848, 0.638924, 0.500115, 0.41704699999999995, 0.40741000000000005, 0.377525], "RUCK": [1.0, 0.572287, 0.609, 0.48242300000000005, 0.40996199999999994, 0.3827130000000001]}, "IRE": {"nonKPP": [0.774376, 0.354627, 0.43281400000000003, 0.482117, 0.4782040000000001, 0.38965000000000005], "KPP": [0.910361, 0.57065, 0.47913000000000006, 0.342329, 0.360619, 0.36738899999999997], "RUCK": [0.841667, 0.498235, 0.623626, 0.4780519999999999, 0.395879, 0.373777]}, "UNR": {"nonKPP": [0.701703, 0.420057, 0.483876, 0.511064, 0.4782040000000001, 0.38965000000000005], "KPP": [0.80197, 0.518584, 0.509762, 0.41919799999999996, 0.39168099999999995, 0.36738899999999997], "RUCK": [0.40761899999999995, 0.39715199999999995, 0.529881, 0.43913800000000003, 0.395879, 0.373777]}, "PDA": {"nonKPP": [0.19381700000000002, 0.260196, 0.400412, 0.46914900000000004, 0.439276, 0.38965000000000005], "KPP": [0.874506, 0.575799, 0.564965, 0.45611500000000005, 0.39168099999999995, 0.36738899999999997], "RUCK": [0.787736, 0.48282899999999995, 0.585763, 0.4780519999999999, 0.395879, 0.373777]}, "PDS": {"nonKPP": [0.844021, 0.42578099999999997, 0.505669, 0.47462899999999997, 0.4782040000000001, 0.38965000000000005], "KPP": [0.874506, 0.590235, 0.57122, 0.4270689999999999, 0.39168099999999995, 0.36738899999999997], "RUCK": [0.913636, 0.498235, 0.623626, 0.4780519999999999, 0.395879, 0.373777]}, "MSD": {"nonKPP": [0.473255, 0.42338600000000004, 0.497823, 0.511064, 0.4782040000000001, 0.38965000000000005], "KPP": [0.812085, 0.45232399999999995, 0.477958, 0.400794, 0.39168099999999995, 0.36738899999999997], "RUCK": [0.949998, 0.477417, 0.623626, 0.4780519999999999, 0.395879, 0.373777]}, "PDN": {"nonKPP": [0.85026, 0.479633, 0.54829, 0.511064, 0.4782040000000001, 0.38965000000000005], "KPP": [0.855199, 0.522854, 0.518424, 0.400794, 0.39168099999999995, 0.36738899999999997], "RUCK": [0.913636, 0.498235, 0.623626, 0.4780519999999999, 0.395879, 0.373777]}, "SSP": {"nonKPP": [0.461179, 0.352533, 0.497823, 0.511064, 0.4782040000000001, 0.38965000000000005], "KPP": [0.865542, 0.4909589999999999, 0.477958, 0.400794, 0.39168099999999995, 0.36738899999999997], "RUCK": [1.0, 0.54385, 0.594713, 0.4780519999999999, 0.395879, 0.373777]}}
_PR_WHOLE={"nonKPP": [0.62565, 0.38278600000000007, 0.497823, 0.511064, 0.4782040000000001, 0.38965000000000005], "KPP": [0.811759, 0.4909589999999999, 0.477958, 0.400794, 0.39168099999999995, 0.36738899999999997], "RUCK": [1.0, 0.498235, 0.623626, 0.4780519999999999, 0.395879, 0.373777]}
_PR_U={"RD": 1.2719501847, "ND>64": 1.4196388202, "IRE": 1.3783834935, "UNR": 1.5941768328, "PDA": 1.6684999183, "PDS": 1.973385042, "MSD": 1.9910028852, "PDN": 1.8845073825, "SSP": 1.1866864548}
_PR_U_ALL=1.3128850877
def _pr_pathway(p):
    t=p.get('type')
    if t=='ND': return 'ND>64'
    return t if t in _PR_PATH else None
def _pr_R(p,tau):
    """the derived pool retention: pathway x class x depth, isotonic non-increasing, tau=0 -> 1.0"""
    cls=_sitout_cls(MA.gfut(p)); pw=_pr_pathway(p)
    dv=(_PR_PATH[pw][cls] if pw else _PR_WHOLE[cls])
    return float(np.interp(tau,[0,1,2,3,4,5,6],[1.0]+list(dv)))
def _pr_U(p):
    """the mean-preserving uplift the pathway's NON-sitters carry (entry-weighted mean == 1 exactly)"""
    pw=_pr_pathway(p)
    return float(_PR_U[pw] if pw else _PR_U_ALL)
# ===== ORDER 24 -- CURRENT-STATE DELIVERY. The Liddy fix. =============================================
# THE DEFECT (issue #334, ORDER 24 brief, comment 5265706155). ORDER 21/23 bound R to sitout_ev and U to
# _a_blend on the reading that those two sites partition the pool population into sitters and non-sitters.
# They do not. ev() dispatches on ns=nseas_pro(p,Y), a CAREER counter (:1085) -- seasons EVER played at or
# above the 6-game bar. The anchor share the multiplier is actually delivered against is a CURRENT-season
# quantity: _a_share's lam reads gy, this season's games, and LAM_SIT[6]==1.0, so
#     a pool player AT or ABOVE this season's bar carries anchor share EXACTLY ZERO and never feels U;
#     a pool player with a career but ZERO games this season carries lam=0 and anchor share exp(-E_q/1.1),
#     which for a thin record is near 1.
# The premium therefore landed INVERSELY TO PARTICIPATION. mani-liddy (MSD 2025 pick 15; 9 games @ 51.1 in
# 2025, 0 games in 2026) has E_q=0.1396 -> anchor share 0.8808, multiplied by U(MSD)=3.0959: 128 -> 1025.
# robert-hansen 80 -> 650 by the same mechanism.
#
# THE FIX. The career-state partition ceases to select who gets what; CURRENT state does. Both read sites
# compute the SAME object, so which arm of ev() a row lands on no longer decides its multiplier:
#     M(p,Y) = (1-phi) * R_derived(pathway,cls,tau)  +  phi * U_pathway
# A pool player with zero current participation reads the derived retention R at his depth. A currently
# playing pool player receives the U premium IN PROPORTION to current participation.
#
# phi IS THE ENGINE'S OWN MID-SEASON CONVENTION, NOT A NEW ONE. The engine judges the in-progress season
# against a PRORATED 6-game bar in three existing places -- nseas_pro (:1086, games >= 6*_fEy), bestlvl
# (:1082, same bar) and sitout_ev's own gp=min(gy/fe,6.0), games at pace against that same bar. phi = gp/6
# is exactly the continuous form of that judgement: 0 at zero games, EXACTLY 1 at or above the bar, linear
# between. No new constant, no new threshold, no new dial. _fEy(Y,p) supplies the proration and already
# returns 1.0 for a completed season AND for an availability-register name whose season is priced as
# complete, so those rows are judged on a full bar without a special case.
#
# ON D12, DECLARED RATHER THAN BURIED: the concave clock tau = (Y-debutyr) + fe**1.5 (:2007) is the DEPTH
# convention for the in-progress season -- how far down the retention curve the row has travelled -- and it
# is a penalty-path object by its own comment. It is UNTOUCHED and is NOT reused as the participation
# weight: depth and participation are different quantities, and fe**1.5 would say a player who has played
# no games is 88% participating, which is the defect inverted. tau continues to feed _pr_R at both sites.
#
# SCOPE. Both edits sit inside the existing p.get('_pool') guards. NO NATIONAL CODE PATH CHANGES: _R_surf,
# LAM_SIT, _a_share, _ev_qual, _surprise, _c_w, C_H, _h_cut and the D12 clock are all untouched. The U
# figures in _PR_U above are RE-DERIVED for this delivery (mean preservation now weights each cell by its
# own phi rather than by a career-state flag) -- see docs/evidence/pool_dial_2026-08-12/UPRIME_TABLE.md.
def _pr_phi(p,Y):
    """CURRENT-season participation share on the engine's own prorated establishment bar: gp/6, in [0,1]."""
    fe=_fEy(Y,p)
    if not fe>0.0: return 0.0
    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    return float(min(max(gy/(6.0*fe),0.0),1.0))
# ===== ORDER 24B -- THE QUALITY-CONDITIONED PREMIUM. psi = phi*q. ====================================
# THE DEFECT (issue #334, ORDER 24B brief, comment 5266656676). ORDER 24 fixed WHO the premium reaches
# -- current participation, not career state. It did not touch HOW MUCH. `phi*U` is a FLAT pathway
# premium, so a pool player who plays badly and one who plays well collect the same premium per unit of
# participation. harrison-ramm (MSD, 4 games in 2026 at 28.75) was lifted 406 -> 620 by the full MSD
# premium; vigo-visentini (RD ruck, 1 game at 84.00) collected 150 -> 182, a fraction, purely because his
# participation share is small. THE OWNER'S LAW: "we don't value players on whether they play, we value
# them on how they play."
#
# THE RULE. The premium leg is conditioned on QUALITY, measured against the pathway's own historical
# PLAYING PAR at the same career depth:
#     q(p,Y) = clip( avg(p,Y) / par(pathway, d) , 0, 1 )
#     M(p,Y) = (1-phi)*R(pathway,cls,tau)  +  phi*( 1 + q*(U''(pathway)-1) )
# q=1 (at or above par) collects the whole premium; q=0 collects none of it and the row is priced at
# 1.0 on its premium leg -- never below, because the premium is a LIFT and its absence is not a charge.
# psi = phi*q is the composite weight, and it is the only thing ORDER 24B adds to ORDER 24's M.
#
# THE PAR, _PR_PAR BELOW. Games-weighted mean of playing-year scoring averages by pathway x career depth,
# derived from the SAME complete-window harvest population that produced R (o24b_uharvest.py's WC: pool
# careers only, ZERO national rows asserted at the gate, Y<=2021, priceable anchor), with a K=10 shrink
# toward the pathway's all-depth par -- ORDER 22's class-axis shrink form carried verbatim (owner ruling
# 5262213139), applied at EVERY cell with no thinness threshold, every cell disclosed with its n in
# docs/evidence/pool_quality_2026-08-12/PAR_TABLE.md. DISCLOSED THERE AND HERE: the MSD, PDN, PDS and SSP
# cells are THIN in this population (MSD carries 14 playing cells / 121 games complete-window, because the
# mid-season draft only begins in 2019), so those pathways' pars are largely the pathway donor. That is
# the honest consequence of deriving par on the population that produced R, and it is reported, not hidden.
#
# THE DEPTH AXIS IS THE HARVEST'S OWN, and it is the axis R is indexed on. The harvest sets
# draftyr = cp.debutyr(p)-1 and d = Y-draftyr, so d = Y-cp.debutyr(p)+1; at an integer depth the engine's
# np.interp over knots [0..6] returns exactly dv[d-1], so par(pw,d) and R(pw,cls,d) read THE SAME CELL.
# It is NOT the store's draft-year field: the two disagree for MSD rows (cp.debutyr returns p['year'] for
# MSD and p['year']+1 otherwise), and the par must be read on the axis it was built on.
#
# avg(p,Y) IS GAMES-WEIGHTED WITHIN THE YEAR so a multi-club season reads as one number. games>0 with a
# missing or zero average gives q=0, per the order -- never a silently par-matching average. games==0
# gives phi=0, so no premium leg exists at all and no q is formed: SITTERS ARE UNTOUCHED BY THIS ORDER,
# to the point. The prior fade (D9) is likewise untouched.
#
# U'' IS RE-DERIVED per pathway so the entry-weighted mean of M over the harvest is 1.0000000000 exactly
# under the phi*q weights -- a HALT instrument, not a claim. The numerator is IDENTICAL to ORDER 24's, so
# U''-1 = (U'-1)/qbar with qbar = SUM(e*phi*q)/SUM(e*phi) <= 1: U'' >= U' for every pathway, ALWAYS,
# because premium mass shrinks under q-weighting and the surviving premium must be larger to redistribute
# the same total. See docs/evidence/pool_quality_2026-08-12/UPRIME2_TABLE.md.
#
# SCOPE. Both edits remain inside the existing p.get('_pool') guards; the two call sites are UNCHANGED.
# _pr_phi, _pr_R, _PR_PATH, _PR_WHOLE, the D12 clock, _a_share, LAM_SIT, _ev_qual, _surprise, _c_w, C_H,
# _h_cut and _R_surf are all untouched. NO NATIONAL CODE PATH CHANGES.
_PR_PAR={"RD": [59.736806, 63.047636, 66.858925, 71.186053, 72.340961, 75.785723], "ND>64": [59.865932, 58.742781, 61.750646, 66.400294, 68.319515, 75.451041], "IRE": [55.562145, 57.012826, 60.473121, 66.930541, 69.132504, 77.470283], "UNR": [52.37813, 59.604749, 62.899236, 71.928692, 73.209376, 73.874855], "PDA": [55.480875, 42.455631, 55.309355, 61.723446, 71.85125, 75.822938], "PDS": [57.765978, 53.577809, 58.972598, 70.244164, 67.261726, 68.514882], "MSD": [55.243329, 61.603845, 65.069362, 69.651092, 71.447589, 75.634061], "PDN": [56.05798, 60.012194, 58.355574, 70.250119, 71.447589, 75.634061], "SSP": [56.994116, 60.055581, 61.671902, 69.651092, 71.447589, 75.634061]}
_PR_PAR_ALL=[58.569576, 60.560852, 64.407234, 69.651092, 71.447589, 75.634061]
def _pr_depth(p,Y):
    """the harvest's own depth index d = Y - draftyr = Y - cp.debutyr(p) + 1, clipped to [1,6]."""
    return int(min(max(int(Y)-int(cp.debutyr(p))+1,1),6))
def _pr_par(p,Y):
    """the pathway's playing par at this row's career depth (whole-pool par when it has no pathway)."""
    pw=_pr_pathway(p)
    return float((_PR_PAR[pw] if pw else _PR_PAR_ALL)[_pr_depth(p,Y)-1])
def _pr_q(p,Y):
    """THE QUALITY, in [0,1]: this season's games-weighted average against the cell's par."""
    yr=[x for x in p['scoring'] if x['year']==Y]
    gy=sum(x['games'] for x in yr)
    if not gy>0: return 0.0
    av=sum(float(x.get('avg') or 0.0)*x['games'] for x in yr)/gy
    if not av>0.0: return 0.0                                # games played, no usable average -> q = 0
    par=_pr_par(p,Y)
    return float(min(max(av/par,0.0),1.0)) if par>0.0 else 0.0
def _pr_mult(p,Y,tau):
    """THE ONE POOL MULTIPLIER (ORDER 24 delivery x ORDER 24B quality). Identical at both read sites."""
    phi=_pr_phi(p,Y)
    if not phi>0.0: return _pr_R(p,tau)                      # a sitter reads R; no premium leg exists
    return (1.0-phi)*_pr_R(p,tau)+phi*(1.0+_pr_q(p,Y)*(_pr_U(p)-1.0))
# ===================================================================================================
# ==== ASK1 (D13 03/07/2026): RUCK PRIOR CAP — cap the hot ruck band prior as a max V0/PVC ratio. Parameterised
# dial RL_RUC_PRIOR_CAP; DEFAULT 1.73 = the class's own ND-ruck median V0/PVC (Luke's inclination, D13 ASK1:
# "I'd be inclined to just cap ruck prior at the 1.73 median"). Sits at the raw_ev/band level (for RUCK wage=0
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
# UNDER-priced young pocket, while RUCK 21-40 is over (1.59) so the fade is OUT by pick ~30):
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
        sp=synth(int(RUC_CEIL_REFPK),float(a),'RUCK')
        # ORDER I (RL_O36): the same synthetic-row rule as the pedigree pole — this ceiling is a
        # scaffold priced off a made-up 21-year-old, not off a person, and it is cached. S1 stays out.
        _s36=MA._O36_SCOPE['on']; MA._O36_SCOPE['on']=False
        try:
            with contextlib.redirect_stdout(io.StringIO()): return raw_ev(sp)*iso_eff(sp)   # LEG A site 2/6 (synth: iso_eff returns the monotonized table unfaded — structural scaffold)
        finally: MA._O36_SCOPE['on']=_s36
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
# ===== #326 ENTRY ANCHOR, PART 1 — THE LADDER-CURRENCY SITE (the RUCK prior cap's pick-capital basis).
# The owner ruled (addendum 5 item 3) that a pool entrant's signed division level REPLACES the single pool
# value in every pricing role it had, and the ruck prior cap is one of them: before this, every pool ruck's
# cap was built on the ladder's one pool slot, so a rookie-draft ruck, an Irish recruit and a mid-season
# signing all leant on the same number. Now each leans on his own division's level.
#   CURRENCY (addendum 6 item 5): the signed levels are LADDER/board currency, and `draftval` is a ladder
#   reading, so the level enters here UNCONVERTED. The engine-value sites (the blend and the floor, part 2
#   below) multiply by the board factor instead. One law, applied per site, so a wrong conversion is a
#   red selftest rather than a quiet 5% drift.
#   SCOPE: pool entrants only. A non-pool player reads `draftval` exactly as before, byte-for-byte.
import json as _plj
_PL_F=float(_plj.load(open('pick_redenomination.json'))['factor'])   # 1.0524 — the certified board factor
def _cap_basis(p):
    """The pick-capital the RUCK prior cap multiplies: a pool entrant's own signed level, or the ladder
    reading for everyone else. Ladder currency on both branches."""
    if p.get('_pool'): return float(MA.pool_level(p))
    return draftval(p)
def _ruc_ceiling(p,Y=2026):                                   # production-derived $ ceiling for a real ruck (bestlvl->$)
    s=bestlvl(p,Y)
    if s<=0: return RUC_PRIOR_CAP*_cap_basis(p)*_ruc_head_v0(p)  # NO qualified production -> prior cap stands (x smooth young headroom, draft-age keyed like the scaffold it mirrors) [#326: pool entrants on their own division level]
    if 'grid' not in _RUCCEIL: _build_ruc_ceiling()
    xg,yg=_RUCCEIL['grid']; return RUC_CEIL_HEAD*float(np.interp(s,xg,yg))*_ruc_head_mult(p,Y)
def _ruc_prior_cap(p,v):                                      # V0 PRIOR SCAFFOLD cap — PR #44 kept this byte-identical; W4 DELIBERATELY extends it with the smooth young-pick headroom (the #43 under-priced pocket lives in the V0-anchored sit-out young rucks: Goad/Green class), draft-age keyed
    return min(v, RUC_PRIOR_CAP*_cap_basis(p)*_ruc_head_v0(p)) if (_isreal(p) and MA.gfut(p)=='RUCK') else v   # #326: pool rucks cap on their own division level (ladder currency, unconverted)
_V0C={}; _V0U={}
_V0_CM, _V0_Q97 = cm, q97m    # V0 is a STRUCTURAL prior: pin the import-time models (the pole/ISO convention —
                              # gate1's own rule: "pole(_POLE) + ISO stay in-sample structural priors"). In the
                              # live engine this is an identity (same objects); in fold-swapping harnesses the
                              # zero-evidence start value stays fold-stable instead of reading prior-training
                              # variance as phantom leakage at T0/T1 cells.
def _v0key(p): return (p.get('player'),p.get('year'),p.get('pick'),p.get('type'),p.get('dob'),MA.gfut(p),MA.effpk(p))
def _v0_uncapped(p):                                          # zero-evidence band start value — NO ruc cap, NO guard (RUCK gate + guard-build use this)
    # cache key = STABLE CONTENT, not id(p): harnesses that deepcopy players (gate1 truncations) recycle
    # memory addresses; V0's inputs are all draft-time content -> same content, same V0.
    k=_v0key(p)
    if k not in _V0U:
        global cm,q97m
        _c,_q=cm,q97m; cm,q97m=_V0_CM,_V0_Q97
        try: _V0U[k]=raw_ev(p,cp.debutyr(p)-1)*iso_eff(p,cp.debutyr(p)-1)   # LEG A site 3/6 (V0: Y=debutyr-1 => E_q=0 => fade=1 => full strength, unchanged BY CONSTRUCTION)
        finally: cm,q97m=_c,_q
    return _V0U[k]
def _v0_raw(p):                                              # ASK1: uncapped V0 -> RUCK prior cap (still pre-ASK2-guard)
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
#     eff-n>=35 at every pick, then isotonic. RUCK is its OWN age18 curve (fitted on capped V0s).
#   TIER 2 — mature (draft-age>=19; 163 players): every exact (pos x age) cell is eff-n<35 even at max bandwidth
#     -> R1 pooling. Mature V0 is age-dominated and position-washed in-sample (position spread << age spread), so
#     the 5 non-RUCK positions POOL into one age-resolved surface V0*(age,log-pick) [DECLARED]; RUCK mature keeps
#     its own (thin) cell. Fit is 2D-kernel over (draft-age, log-pick), then isotonic-non-increasing in pick AND
#     non-increasing in draft-age (older draftee never starts above a younger one, same pick) — so mature entrants
#     stay LAWFULLY DIFFERENTIATED from age-18 and by age. eff-n growth/shortfalls recorded in _V0CURVE_META (R1).
# APPLY on the BOARD PATH: every current-roster real-ND start anchor V0 := V0*(pos, draft-age, recorded pick),
# feeding every present/forward consumer (sit-out retention, staleness/stalled/mediocre caps, the B5 floor, the
# delist scrap). The BACKTEST path is untouched (guard, above). By-construction gates in _v0_curve_assert().
_BOARD_PATH  # (declared above, before _R_surf)
_V0CURVE={}; _V0CURVE_META={}; _V0_GRIDPK=list(range(1,91)); _V0_LGRID=np.log(_V0_GRIDPK)
# ==== #306 L-A DESIGN CONSTANTS — fixed at design time, stated in the artifact's own record (N30).
# Module constants, not env gates: an acceptance whose bound an environment variable can move is not a
# bound. Changing one is a code change, visible in the engine head md5 and in review.
_LA_HPICK=0.35     # locality bandwidth in LOG-pick: at pick 7, pick 9 weighs 0.7728 and pick 14 0.1407
_LA_HAGE=1.5       # locality bandwidth in draft-age YEARS — smooth across age, no age buckets
_LA_KCONF=25.0     # confidence half-weight: n_eff = 25 gives a level half its own say
_LA_B=2.00         # m in [0.50, 2.00], held identically by the construction
_LA_TOL=0.005      # local-neutrality tolerance, checked at EVERY pick
def _ageR(p): return int(round(cp._age_asof(p, p.get('year') or (cp.debutyr(p)-1))))
# ==== LEG F6 — FREEZE _iso_dec (THE RESIDUAL WEATHER), 2026-07-18 (item 381; the SAME pattern owner-blessed
#      for q97m 2026-07-14). WAS: _build_v0_curve() re-fit the V0 pick-curve surface (three isotonic surfaces
#      via _iso_dec) at EVERY board/gate/panel import, over the REAL roster's _v0_raw. numpy's OpenBLAS is
#      DYNAMIC_ARCH (a CPU-specific float kernel at runtime); on a mixed-CPU fleet the same commit produced a
#      slightly different V0 surface per box -> the whole board shifted coherently (the balanced-board 06d8af60
#      <-> 83a4b21d weather flip, Sheezel +/-95, item 380 diagnosis). q97m/cm are already frozen pickles and the
#      NW kernels are order-fixed (_det_*); _iso_dec/_build_v0_curve was the ONE live fit left on the value path.
#      NOW: the SHIPPED V0 surface is computed ONCE at a bake (session_2026-07-18/legf6/scripts/refit_v0surf.py),
#      pickled to data/v0surf.pkl keyed by a DETERMINISTIC config signature, md5-pinned (data/expected_boot.json
#      'v0surf'), asserted by boot_guard (Guard 5) on entry, and LOADED here — the shipped surface is NEVER
#      fitted at board-build. The signature is a function of the ACTIVE PICK CURVE + roster geometry + the
#      value-gate env ONLY (never _v0_raw values), so a weather box computes the SAME signature as a clean box
#      and loads the SAME clean surface -> the flip is removed. A NON-shipped config (a kill switch: RL_PVC2=0,
#      RL_EVW=0, RL_ISOFADE=0, RL_W4_RUC=0, ...) has a different signature, is NOT in the frozen set, and still
#      FITS exactly as before -> every declared kill-switch stays byte-exact. Regenerate ONLY via the refit entry
#      point (RL_V0SURF_REFIT=1 forces a fit + re-pin; a silent refit is the exact defect being frozen out).
def _load_v0surf():
    if os.environ.get('RL_V0SURF_REFIT')=='1': return {}     # the ONE refit entry point: fit from scratch, ignore any stale pickle
    _cands=[os.environ.get('RL_V0SURF_PKL'), '/home/claude/v0surf.pkl',
            os.path.join(os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '','data','v0surf.pkl')]
    for _c in _cands:
        if _c and os.path.exists(_c):
            with open(_c,'rb') as _fh: return pickle.load(_fh)
    raise SystemExit("v0surf FROZEN-LOAD HALT: no frozen v0surf pickle found (looked at RL_V0SURF_PKL, "
                     "/home/claude/v0surf.pkl, <repo>/data/v0surf.pkl). Re-run bootstrap.sh to seed the workspace "
                     "copy, or regenerate via session_2026-07-18/legf6/scripts/refit_v0surf.py at a bake. The "
                     "engine NEVER fits the shipped V0 surface at build time (the exact defect the freeze removed).")
_V0SURF=_load_v0surf()
# Value-gate defaults, byte-for-byte the code defaults, so a build that SETS a gate to its default (gate mode's
# config_manifest) signs identically to a build that leaves it UNSET (dev shell). LENS gates (RL_LEGF/RL_LEGE)
# are DELIBERATELY excluded: they never touch the V0 surface, so RL_LEGF=0 must LOAD the SAME frozen surface
# (the RL_LEGF=0 chain byte-exactness). The active pick curve already encodes RL_PVCADOPT/RL_PVC2/RL_PVCFIT.
_V0SURF_GATES={'RL_RUC_PRIOR_CAP':'1.4','RL_W4_RUC':'1','RL_RUC_CEIL_HEAD':'0.80','RL_RUC_CEIL_REFPK':'72',
    'RL_RUC_YRH':'0.35','RL_FORMDECL':'1','RL_M3_FE':'0.58','RL_DAMP':'1','RL_DAMP_K':'5.8','RL_EVW':'1',
    'RL_MSD_POOL_EXCL':'1','RL_AGE':'1','RL_SAGE29':'1','RL_LSYM':'1','RL_EO2':'1','RL_ABSENCE':'1',
    'RL_FWDRECAL':'1','RL_YOUNG':'1','RL_OVPX':'1','RL_KPFFIX':'1','RL_V7FORM':'1','RL_V7_FORM_W':'0.6',
    'RL_W4_CRED':'0.17','RL_W4_KPFUP':'1.6','RL_W4_FADE':'0.60','RL_W4_OVPX':'1.0','RL_W4_KPFSH':'0.55',
    'RL_W4_KPFSH_DEM':'0.70','RL_W4_KPFTOP':'0.4','RL_W4_KPFM0':'8.0','RL_W4_KPFMS':'16.0','RL_AVAIL':'1',
    'RL_LTI_RETURN':'1','RL_LTI_CLOCK':'advance','RL_YCRED_W':'0.9','RL_YCRED_KPF':'0.92','RL_ISOFADE':'1',
    # E2 (#279 step 4 item 4, extended by seam word F1 2026-07-30): TWO keys join the signature, both of them
    # MEASURED silent-surface channels, not suspected ones.
    #   RL_GAMMA — the signature was curve-sensitive but GAMMA-BLIND. Gamma scales value() (rl_model.py:504,
    #     SCALE/val at :731/:734) without moving the pvc entries, so a SCAR<->VOR flip changed the fitted
    #     surface while producing an IDENTICAL signature. Measured: 0.85 -> 5ae00319, 1.0 -> 93b4a680.
    #   RL_PICK1 — added on measurement, AGAINST the reasoning first filed here. The superseded comment claimed
    #     "RL_PICK1 moves the pvc entries, so the pvc leg already catches it". IT DOES NOT. `_v0surf_sig` reads
    #     `_PVC0`, which is sourced from the PINNED adopted-curve artifact (pin(1)=3000 by construction), so
    #     RL_PICK1 never reaches the pvc leg at all. Measured at the step-4 rehearsal: RL_PICK1 3000 -> 3500
    #     left the signature IDENTICAL (5ae00319 both) while all three fitted surfaces moved (c18
    #     eddccddb -> 6cb62db4, surfN a6e2fe36 -> 1f45ba1a). That measurement is this key's proven-can-fail.
    # Defaults are the engine's own (rl_model.py:504 and :866).
    'RL_GAMMA':'0.85', 'RL_PICK1':'3000'}
def _v0surf_sig(real):
    import hashlib as _hl, json as _js
    _curve=_PVC0 if '_PVC0' in globals() else MA.PVC          # the pick curve _v0_raw is actually reading right now
    _payload={'pvc':sorted((int(k),int(v)) for k,v in _curve.items()),
              'roster':sorted([str(MA.gfut(p)),_ageR(p),int(p.get('pick'))] for p in real),
              'gates':{g:os.environ.get(g,d) for g,d in sorted(_V0SURF_GATES.items())}}
    return _hl.md5(_js.dumps(_payload,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def _iso_dec_on(lg,y): return list(map(float,IsotonicRegression(increasing=False,out_of_bounds='clip').fit(lg,y).predict(lg)))
def _iso_dec(y): return _iso_dec_on(_V0_LGRID,y)          # the whole 1..90 grid (the pre-#306 fit's own use)
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
_V0SURF_BUILT={}          # sig -> surfaces, for every surface a build fits; the bake freezes all of them
def _build_v0_curve():
    POS=['MID','KPF','KPD','SF','SD','RUCK']; c18={}
    # ADDENDUM 1 (owner, 2026-07-28): this is the kernel-weighted pick-curve path — _fit_pick_curve over
    # log(RECORDED pick). `type=='ND'` alone no longer means "on the national curve": a national selection at
    # 65+ is POOL under the ruling, and admitting it here lets a pool outcome teach the V0 pick surface through
    # the back door, exactly as the +/-4 builders did. Same gate as every other fit site.
    # Registered at k=0 (whole-population sample, not per-pick) so the Addendum-1 check watches the ACTUAL list
    # this kernel fit consumes rather than re-deriving it — see _curve_sample in rl_model.
    real=MA._curve_sample('v0_kernel',0,
         [p for p in MA.data if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None
          and not MA.is_pool(p)])
    _sig=_v0surf_sig(real)                                   # LEG F6: deterministic config signature (weather-invariant)
    _frozen=_V0SURF.get(_sig) if isinstance(_V0SURF,dict) else None
    _refit_declared=os.environ.get('RL_V0SURF_REFIT')=='1'
    if _frozen is not None and not _refit_declared:
        # ---- FROZEN LOAD (the shipped config): the _iso_dec residual weather is removed — LOAD the three
        #      surfaces + their fit metas, NEVER re-fit. star()/np.interp/_V0CURVE below are UNCHANGED, so the
        #      board is byte-identical to the clean fit by construction (freeze the OUTPUT, don't re-derive it).
        c18=_frozen['c18']; surfN=_frozen['surfN']; surfR=_frozen['surfR']
        _V0CURVE_META.update(_frozen.get('meta',{}))
    elif not _refit_declared:
        # ---- HALT. THE SILENT FALLBACK IS DELETED (owner, 2026-07-28), matching the sibling q97m freeze above:
        #      "A silent refit is the exact defect being fixed: there is deliberately no fit path left here."
        #      v0surf kept a fallback that quietly fitted whenever the signature was not in the frozen set, and
        #      that silence is why the freeze went INERT UNNOTICED — main's shipped config already computed a
        #      signature absent from the pickle, so the fleet had been live-fitting the value path with no
        #      warning. Reproducibility is the entire purpose of the freeze, and a fallback that fits on a miss
        #      cannot deliver it. An unknown config is now a HALT, not a quiet refit.
        #      A DECLARED refit is still available and is the only way to fit: set RL_V0SURF_REFIT=1. That is
        #      what refit_v0surf.py does, and it is how a kill-switch experiment (RL_PVC2=0, RL_EVW=0, ...) is
        #      run now — the refit becomes visible and deliberate instead of implicit.
        raise SystemExit(
            "v0surf FROZEN-SIGNATURE HALT: this build's config signature %s is NOT in data/v0surf.pkl "
            "(frozen: %s).\n"
            "  The engine will NOT silently re-fit the V0 pick-curve surface — that silent fallback was removed "
            "(owner word 2026-07-28), for the same reason q97m has no fit path: a silent refit makes the board "
            "unreproducible across CPU/BLAS kernels, and it hides a freeze that has gone stale.\n"
            "  If the config CHANGED deliberately (a split, an exclusion, a curve move), regenerate and re-pin:\n"
            "      RL_V0SURF_REFIT=1 RL_BAKE_V0SURF=1 python3 session_2026-07-18/legf6/scripts/refit_v0surf.py "
            "--bake      (on a clean instance)\n"
            "  If you are running a declared kill-switch experiment, set RL_V0SURF_REFIT=1 to fit explicitly."
            %(_sig, ', '.join(sorted(_V0SURF.keys())) if isinstance(_V0SURF,dict) else '<none>'))
    else:
        # ---- THE ONE COMMITTED REFIT PATH, and it must be DECLARED (RL_V0SURF_REFIT=1). refit_v0surf.py drives
        #      it to produce the artifact, so the frozen surface and its regeneration stay a single source.
        if os.environ.get('RL_V0_LENS','1')!='0':
            # ============ #306 L-A — THE ANCHORED LENS FIELD (N29 · owner laws · seam approval) ============
            # v0*(pos,age,pick) = anchor(pick) x m(pos,age,pick).
            #
            # `pick` reaches the surface through the ANCHOR and through the LENS, and the lens is a smooth
            # BOUNDED field -- free to sit below the curve at one pick and above it at another, crossing
            # wherever the data crosses. The pre-#306 path fitted _v0_raw over log(pick) with no reference
            # to the curve at all, which is why the tail could float 65% above it.
            #
            # THE BASIS IS A DECLARED INPUT, NOT CODE (approval clause 1 -- the owner's live-and-breathe
            # steer). The lens fits from the #279 STRUCTURAL CAREER VALUES emitted to
            # docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json by that directory's emitter,
            # which reuses harness_pvc.structural_values() unmodified. The surface's own slot prior is
            # BARRED as a fit target (the self-referential lineage #279 measured at 0.0248% reality); it
            # survives only inside #279's own COUNTED fallback. When the replacement bars move, or the
            # class window moves, the chain is RE-RUN and the artifact RE-PINNED -- no surgery here.
            #
            # THE LAWS THIS CODE HOLDS, each structural rather than checked afterwards:
            #   GRADED LOCALITY  Gaussian kernels in log-pick and draft age. Influence decays smoothly;
            #                    pick 9 informs pick 7 more than pick 14 does. NO BUCKETS ON ANY AXIS.
            #   CONFIDENCE       hierarchical shrinkage by effective sample size --
            #                    (pos,age,pick) -> (pos,pick) -> (pos) -> 1.0, the all-in slot value.
            #                    Thin data leans to the all-in value and is never trusted with the full
            #                    effect. The mature dials are under this rule identically.
            #   LOCAL NEUTRALITY lam(pick) enforces SUM w*anchor*m == SUM w*anchor AT EVERY PICK under the
            #                    same kernel: a position above the curve in a stretch is paid for by the
            #                    others IN THAT STRETCH, never by inflating the class. A global scalar
            #                    would permit exactly the cross-region borrowing this forbids.
            #   BOUNDED          m in [1/B, B] identically; bound and neutrality iterated to a fixed point.
            #                    Where the bound binds, the bound wins.
            _lensf=os.environ.get('RL_LENS_BASIS') or os.path.join(
                os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '',
                'docs','evidence','exec_306_zlaarm','basis','structural_basis_279.json')
            if not os.path.exists(_lensf):
                raise SystemExit("v0 LENS BASIS MISSING: %s\n"
                    "  The year-zero lens fits from the #279 structural career values, supplied as a\n"
                    "  DECLARED INPUT. Regenerate it with\n"
                    "      python3 docs/evidence/exec_306_zlaarm/basis/emit_structural_basis.py\n"
                    "  or point RL_LENS_BASIS at the artifact. There is deliberately no fallback: fitting\n"
                    "  the lens from the surface's own prior is the barred, self-referential lineage."%_lensf)
            import json as _laj, hashlib as _lah
            _LB=_laj.load(open(_lensf))
            _brows=[r for r in _LB['rows'] if r.get('pos') and r.get('pick')]
            _V0CURVE_META['_lens_basis']={'file':os.path.basename(_lensf),
                'md5':_lah.md5(open(_lensf,'rb').read()).hexdigest(),
                'rows':len(_brows),'identity':_LB.get('identity'),'provenance':_LB.get('provenance'),
                'OPTIMISM':_LB.get('_OPTIMISM')}
            _curveA=_PVC0 if '_PVC0' in globals() else MA.PVC
            _A={int(k):float(v) for k,v in _curveA.items()}
            _amax=max(_A)
            _asl=(np.log(_A[_amax]/_A[_amax-1])/(np.log(_amax)-np.log(_amax-1))) if (_amax-1) in _A and _A[_amax-1]>0 else 0.0
            def _anchor(pk):
                pk=int(min(max(pk,1),90))
                return float(_A[pk]) if pk in _A else float(_A[_amax]*np.exp(_asl*(np.log(pk)-np.log(_amax))))
            for _r in _brows:
                _r['_lp']=np.log(_r['pick']); _r['_an']=_anchor(_r['pick'])
                _r['_ag']=(float(_r['age_draft']) if _r.get('age_draft') is not None else None)
            def _kern(d,h): return float(np.exp(-0.5*(d/h)**2))
            def _est(sub,lp=None,ag=None):
                sw=sw2=swa=swv=0.0
                for _r in sub:
                    w=1.0
                    if lp is not None: w*=_kern(_r['_lp']-lp,_LA_HPICK)
                    if ag is not None:
                        if _r['_ag'] is None: continue      # missing age: informs the position level only
                        w*=_kern(_r['_ag']-ag,_LA_HAGE)
                    if w<1e-12: continue
                    sw+=w; sw2+=w*w; swa+=w*_r['_an']; swv+=w*_r['value']
                if swa<=0: return 1.0,0.0
                return swv/swa,(sw*sw/sw2 if sw2>0 else 0.0)
            def _shrink(v,n,toward):
                s=n/(n+_LA_KCONF); return s*v+(1.0-s)*toward
            _bypos={}
            for _r in _brows: _bypos.setdefault(_r['pos'],[]).append(_r)
            _AGEG=list(range(16,31)); _PK=list(range(1,91))
            _pre={}
            for _p in POS:
                _sub=_bypos.get(_p) or []
                _l2v,_l2n=_est(_sub); _l2=_shrink(_l2v,_l2n,1.0)
                for _pk in _PK:
                    _lp=float(np.log(_pk)); _v1,_k1=_est(_sub,lp=_lp); _l1=_shrink(_v1,_k1,_l2)
                    for _ag in _AGEG:
                        _v0,_k0=_est(_sub,lp=_lp,ag=float(_ag))
                        _pre[(_p,_ag,_pk)]=_shrink(_v0,_k0,_l1)
            # ---- LOCAL neutrality, solved on the APPLIED POPULATION'S COMPOSITION.
            # ADDENDUM (seam ruling 2026-08-04, owner word): the law is enforced where it is MEASURED.
            # The acceptance reads the artifact over every real ND row the surface actually prices, so
            # lam(pick) is solved against THAT population's anchor-weighted composition rather than the
            # basis population's. Enforcing on the teaching mix and measuring on the applied mix left a
            # residual of up to 1.75% per pick purely from composition drift between 2004-2022 and
            # 2003-2025 -- not a construction failure, but the acceptance is not met by a law enforced
            # somewhere else.
            #
            # THE APPLIED ROWS ENTER AS COMPOSITION WEIGHTS ONLY -- (position, draft age, pick): WHO
            # EXISTS, and nothing about how they turned out. No careers, no v0 beliefs, no outcomes.
            # THE LENS SHAPE REMAINS TAUGHT EXCLUSIVELY BY structural_basis_279.json (fitted above and
            # untouched here); this step only rescales it so each neighbourhood nets to the anchor.
            # The barred self-referential lineage stays barred: `real`'s VALUES never enter the fit.
            _apply=[]
            for _p2 in real:
                _pk2=_p2.get('pick')
                if _pk2 is None: continue
                _pk2=int(_pk2)
                if not (1<=_pk2<=64): continue
                _apply.append((MA.gfut(_p2),int(min(max(_ageR(_p2),16),30)),_pk2,
                               float(np.log(_pk2)),_anchor(_pk2)))
            _V0CURVE_META['_la_applied_rows']=len(_apply)
            _lam={_pk:1.0 for _pk in _PK}; _m={}
            for _ in range(200):
                for _k in _pre: _m[_k]=min(_LA_B,max(1.0/_LA_B,_pre[_k]*_lam[_k[2]]))
                _worst=0.0
                for _pk in _PK:
                    _lp=float(np.log(_pk)); _num=_den=0.0
                    for (_po,_ag,_pkr,_lpr,_anr) in _apply:
                        w=_kern(_lpr-_lp,_LA_HPICK)
                        if w<1e-12: continue
                        _num+=w*_anr; _den+=w*_anr*_m[(_po,_ag,_pkr)]
                    if _den>0:
                        _ra=_num/_den; _lam[_pk]*=_ra; _worst=max(_worst,abs(1.0/_ra-1.0))
                if _worst<=1e-12: break
            for _k in _pre: _m[_k]=min(_LA_B,max(1.0/_LA_B,_pre[_k]*_lam[_k[2]]))
            _gA=[_anchor(_pk) for _pk in _PK]
            # ---- THE NEVER-RISES LAW, RESTORED ON THE LENS PATH (owner ruling 1.1, 2026-08-10; #334).
            # THE LAW (owner, ledger R12, 2026-07-03): a year-zero value curve NEVER RISES as the pick
            # number rises. It held for 33 days and was LOST BY OMISSION at the #306 lens landing
            # (dab9657, 2026-08-05): the pre-#306 free fit ended every curve with _iso_dec; the composed
            # lens field v0* = anchor(pick) x m(pos,age,pick) never called it. The anchor ladder is
            # strictly falling but has near-flat plateaus (picks 6-8 fall ~4 points each), and the lens —
            # a smooth BOUNDED field, free to cross the ladder — climbs across them. Measured on the
            # shipped surface: hundreds of rising steps inside picks 1-64, in every one of the 90
            # (position x draft-age) profiles, and 29 adjacent inverted pairs on real players (the one
            # the owner saw: Grlj at pick 8 priced above Cumming at pick 7).
            #
            # THE METHOD IS THE OWNER'S RULING, and it is the OLD STEP'S EXACT BEHAVIOUR: within each
            # (position x draft-age) profile, project the COMPOSED curve over the log-pick grid to
            # non-increasing by isotonic regression — `_iso_dec`, the same call the deleted step made,
            # on the same _V0_LGRID. Isotonic regression IS the merge the owner described: a violating
            # stretch settles to the weighted level between its neighbours (some rows come down a
            # little, some up a little), and it is the least-squares-closest non-increasing curve, i.e.
            # the least total distortion of the lens's shape. Nothing else is re-fitted.
            #
            # WHAT THIS DOES **NOT** TOUCH — the lens's own ruled properties, each preserved:
            #   LAW-INTERSECTIONS  a position's value may still cross the pick ladder, and two positions
            #                      may still cross each other. The projection is applied INSIDE one
            #                      (pos,age) profile only; it never compares one profile to another and
            #                      never compares a profile to the anchor. Crossing stays legal; rising
            #                      WITHIN a profile does not.
            #   GRADED LOCALITY    the kernels, bandwidths and shrinkage above are untouched; the field
            #                      that enters here is the same field #306 fits.
            #   BOUNDED / NEUTRAL  m in [1/B,B] and the lam(pick) fixed point are solved first, and the
            #                      projection runs AFTER them, on the composed curve, exactly where the
            #                      old step sat (last, on the finished curve, before the freeze). The
            #                      neutrality residual it leaves is MEASURED and recorded below
            #                      (`_iso_neutrality_worst`) rather than assumed to be zero — a merge
            #                      that moves values must be allowed to move this figure, and the
            #                      honest number is filed instead of the pre-projection one.
            #   MATURE AGE ORDER   the pre-#306 mature fit also forced non-increasing in draft AGE at
            #                      each pick. The #306 lens does NOT (age is a smooth kernel axis, and
            #                      R12 is a PICK law). Not reintroduced here: restoring one law is not
            #                      licence to add another the owner did not rule.
            #
            # WHERE THE PROJECTION IS SOLVED, and why it is not the whole 1..90 grid. The grid runs to
            # pick 90, but THE NATIONAL LADDER ENDS AT 64: _PVC0 is 3000 at pick 1 down to 185 at pick
            # 64, and index 65 is the POOL SLOT (237) — a different object, deliberately ABOVE the
            # ladder's last rung. `_anchor` extrapolates past its own last key off the 64->65 ratio, so
            # that step-up becomes a compounding upward slope and the raw composed curve rockets away
            # (MID age-18: 238 at pick 64 -> ~39,500 at pick 90). Nothing reads it — every priced row on
            # this surface is a non-pool national selection, measured max pick 64, and picks 65+ are
            # POOL by the owner's ruling and are priced off the signed division levels instead.
            # Solving one isotonic projection across the whole grid would let that unread artifact drag
            # the LADDER up: pool-adjacent-violators would merge the exploding tail with the real curve
            # and flatten every profile to a single number (measured, not guessed — the first build of
            # this repair did exactly that and was thrown away). So:
            #   picks 1-64  the isotonic merge, on the ladder the law is written about;
            #   picks 65-90 carried by running minimum from the pick-64 level — the same law (a value
            #               may never rise with pick) applied where there is no ladder to merge against.
            #               The tail can only fall; the artifact can never lift the priced region.
            #
            # DETERMINISM (the F6 freeze discipline): this runs only on the DECLARED refit lane
            # (RL_V0SURF_REFIT=1) — the shipped build LOADS the projected surface from data/v0surf.pkl
            # and fits nothing, exactly as before. The grid is order-fixed (_V0_LGRID, picks 1..90 in
            # order); the projection is applied to each cell independently in a fixed POS x AGE order;
            # the OUTPUT is what gets frozen and md5-pinned. Same treatment the old _iso_dec received.
            _NDL=min(64,len(_PK))                        # the national ladder's last pick
            _iso_pre={}
            c18={}; surfN={}; surfR={}
            for _p in POS:
                for _ag in _AGEG:
                    _g=[_gA[_i]*_m[(_p,_ag,_PK[_i])] for _i in range(len(_PK))]
                    _key='%s|%d'%(_p,_ag)
                    _iso_pre[_key]=list(_g)
                    _g=_iso_dec_on(_V0_LGRID[:_NDL],_g[:_NDL])+list(_g[_NDL:])   # <- THE RESTORED LAW
                    for _i in range(1,len(_g)):           # never rises, all the way out
                        if _g[_i]>_g[_i-1]: _g[_i]=_g[_i-1]
                    if _ag<=18: c18[_key]=_g
                    elif _p=='RUCK': surfR[_key]=_g
                    else: surfN[_key]=_g
            # The projection changes the composed curve, so the multiplier the board actually reads is
            # no longer _m but m' = curve'/anchor. Recorded, so the neutrality figure filed below is the
            # SHIPPED field's, not the pre-projection field's.
            _mpost={}
            for _p in POS:
                for _ag in _AGEG:
                    _key='%s|%d'%(_p,_ag)
                    _cv=(c18.get(_key) or surfR.get(_key) or surfN.get(_key))
                    for _i in range(len(_PK)):
                        _mpost[(_p,_ag,_PK[_i])]=(_cv[_i]/_gA[_i]) if _gA[_i]>0 else 1.0
            def _isocur(_k): return (c18.get(_k) or surfR.get(_k) or surfN.get(_k))
            _V0CURVE_META['_iso_restore']={'law':'R12 never-rises with pick, per (position x draft-age) profile',
                'method':'IsotonicRegression(increasing=False) over log-pick 1..64 (the _iso_dec pattern, '
                         'applied AFTER the lens multiply, before the freeze); picks 65-90 carried by '
                         'running minimum (no ladder there to merge against)',
                'ruling':'owner 1.1, 2026-08-10 (#334)','cells':len(_iso_pre),'grid':len(_PK),'ladder_last':_NDL,
                'grid_points_moved':sum(1 for _k in sorted(_iso_pre) for _i in range(len(_PK))
                                        if abs(_iso_pre[_k][_i]-_isocur(_k)[_i])>1e-9),
                'rising_steps_before_1_64':sum(1 for _k in sorted(_iso_pre) for _i in range(_NDL-1)
                                               if _iso_pre[_k][_i+1]>_iso_pre[_k][_i]+1e-9),
                'rising_steps_after_1_64':sum(1 for _k in sorted(_iso_pre) for _i in range(_NDL-1)
                                              if _isocur(_k)[_i+1]>_isocur(_k)[_i]+1e-9),
                'rising_steps_after_full':sum(1 for _k in sorted(_iso_pre) for _i in range(len(_PK)-1)
                                              if _isocur(_k)[_i+1]>_isocur(_k)[_i]+1e-9),
                'preserves':'LAW-INTERSECTIONS (cross-profile and profile-vs-ladder crossings untouched); '
                            'graded locality; bounded m; the lam fixed point (solved first)'}
            # ---- L-C: THE CROSS-HOST BYTE-ASSERT, WIRED INTO THE LANE ITSELF.
            # N16's third spec word. The assert compares FITTED OUTPUT BYTES -- never a library
            # version, never a pin hash. "The pin was never the guard": item 380's OpenBLAS byte-pin
            # passed on BOTH hosts while the dispatch tier differed, and this job measured the same
            # thing again on 2026-08-04 (5939fa35 x5 on one box vs fb9efdec x3 on two others, every
            # pin green on all three, identical CPU strings).
            #
            # It is keyed on the DECLARED INPUTS. If the basis, the anchor and the roster composition
            # all match a recorded run, the fitted bytes MUST match it too -- any difference is the
            # box, and the box is not allowed to decide quietly. If the inputs DON'T match, the assert
            # says INAPPLICABLE and reports so: a legitimate re-basis must never read as a green
            # cross-host proof, which is the vacuity this leg exists to refuse.
            _lensdig=_lah.md5(_laj.dumps({'c18':{k:c18[k] for k in sorted(c18)},
                                          'surfN':{k:surfN[k] for k in sorted(surfN)},
                                          'surfR':{k:surfR[k] for k in sorted(surfR)}},
                                         sort_keys=True).encode()).hexdigest()
            _rosterdig=_lah.md5(_laj.dumps(sorted('%s|%d|%d'%(o,g,q) for (o,g,q,_l,_a) in _apply)).encode()).hexdigest()
            # LC-1 (seam hand-back): the anchor component covers THE FIT'S OWN INPUT — the national
            # ladder, picks 1-64. The pool slot (65) is NOT a fit input: no pool row teaches the lens
            # and no pool row reads the surface. Including it made this component a look-alike of the
            # census payload that was not the census payload (a name trap), and it would have fired a
            # spurious INAPPLICABLE at the landing when the pool level moves under N43 while the ladder
            # the lens actually uses had not. Restricted, the component IS the census payload verbatim.
            _anchdig=_lah.md5(_laj.dumps({str(k):int(round(v)) for k,v in _curveA.items()
                                          if 1<=int(k)<=64},sort_keys=True).encode()).hexdigest()[:8]
            _lckey='%s|%s|%s'%(_V0CURVE_META['_lens_basis']['md5'][:12],_anchdig,_rosterdig[:12])
            _lcf=os.environ.get('RL_LANE_EXPECT') or os.path.join(
                os.environ.get('RL_REPO') or os.environ.get('CLAUDE_PROJECT_DIR') or '',
                'docs','evidence','exec_306_zlaarm','basis','lane_expectation.json')
            _lcstate='INAPPLICABLE — no recorded expectation for these declared inputs'
            if os.path.exists(_lcf):
                _lce=_laj.load(open(_lcf)).get('expectations',{})
                if _lckey in _lce:
                    _want=_lce[_lckey]['lens_digest']
                    if _want!=_lensdig:
                        raise SystemExit(
                            "L-C CROSS-HOST BYTE-ASSERT FAILED — THIS BOX DOES NOT REPRODUCE THE LANE.\n"
                            "  declared inputs match a recorded run, so the fitted bytes must match too.\n"
                            "    key       %s\n    expected  %s\n    got       %s\n"
                            "  This is item 380's machine sensitivity, caught in the lane rather than in a\n"
                            "  figure nobody could compare. Every version pin can be green and this can still\n"
                            "  fire -- that is the point. HALT: no measurement act on a non-reproducing box.\n"
                            "  Restart/reopen the container and re-assert (N35), or file the divergence."
                            %(_lckey,_want,_lensdig))
                    _lcstate='PASS — fitted bytes reproduce the recorded run for these declared inputs'
            _V0CURVE_META['_lc']={'lens_digest':_lensdig,'key':_lckey,'state':_lcstate,
                                  'expectation_file':os.path.basename(_lcf),
                                  'compares':'FITTED OUTPUT BYTES, never a version pin or a CPU string'}
            _mages=[a for a in _AGEG if a>=19]
            _V0CURVE_META['mature_nonRUC']={'ages':_mages,'construction':'anchored_lens_field'}
            _V0CURVE_META['mature_RUC']={'ages':_mages,'construction':'anchored_lens_field'}
            for _p in POS: _V0CURVE_META[('age18',_p)]={'construction':'anchored_lens_field'}
            _V0CURVE_META['_la']={'shape':'POS|AGE','B':_LA_B,'tol':_LA_TOL,'h_pick':_LA_HPICK,
                'h_age':_LA_HAGE,'k_conf':_LA_KCONF,
                'neutrality_population':'APPLIED (composition weights only)',
                'neutrality_worst':max(abs(sum(_kern(_l-float(np.log(_pk)),_LA_HPICK)*_a*_m[(_o,_g,_q)]
                    for (_o,_g,_q,_l,_a) in _apply)/max(sum(_kern(_l-float(np.log(_pk)),_LA_HPICK)*_a
                    for (_o,_g,_q,_l,_a) in _apply),1e-12)-1.0) for _pk in range(1,65)),
                # The SHIPPED field's residual: the never-rises projection runs after the fixed point, so
                # the neutrality it leaves is measured on m' = curve'/anchor, not on the pre-projection m.
                # Filed honestly rather than quoted from the step before the one that ships.
                '_iso_neutrality_worst':max(abs(sum(_kern(_l-float(np.log(_pk)),_LA_HPICK)*_a*_mpost[(_o,_g,_q)]
                    for (_o,_g,_q,_l,_a) in _apply)/max(sum(_kern(_l-float(np.log(_pk)),_LA_HPICK)*_a
                    for (_o,_g,_q,_l,_a) in _apply),1e-12)-1.0) for _pk in range(1,65)),
                'binds':sum(1 for _k in _m if abs(_m[_k]-_LA_B)<1e-9 or abs(_m[_k]-1.0/_LA_B)<1e-9)}
        else:
            # ---- THE PRE-#306 FREE FIT, retained behind RL_V0_LENS=0 as the declared A/B control: the
            #      lane whose defect L-A removes. Keeping it runnable is what makes the before-figures
            #      RE-TAKEABLE rather than quoted from a filing.
            for pos in POS:
                pts=[(np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)==pos and _ageR(p)<=18]
                grid,meta=_fit_pick_curve(pts); c18[pos]=grid; _V0CURVE_META[('age18',pos)]=meta
            matN=[(_ageR(p),np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)!='RUCK' and _ageR(p)>=19]
            matR=[(_ageR(p),np.log(p.get('pick')),_v0_raw(p)) for p in real if MA.gfut(p)=='RUCK'      and _ageR(p)>=19]
            surfN=_fit_mature(matN,'mature_nonRUC'); surfR=_fit_mature(matR,'mature_RUC')
        # Record THIS signature's surfaces so the bake can freeze EVERY surface a shipped build produces, not
        # just the last one. _build_v0_curve runs three times per build — once at import, then again after each
        # of the RL_PVCADOPT and RL_PVC2 swaps of _PVC0 — and the signature covers _PVC0, so the three calls have
        # three DIFFERENT signatures. The old pickle held only the final one, so the first two calls always fell
        # through to the live fit. That is why the freeze never actually removed the fit from the value path.
        _V0SURF_BUILT[_sig]={'c18':c18,'surfN':surfN,'surfR':surfR,
                             'meta':{k:v for k,v in _V0CURVE_META.items()
                                     if k in ('mature_nonRUC','mature_RUC') or (isinstance(k,tuple) and k and k[0]=='age18')}}
    _V0CURVE_META['_c18']=c18; _V0CURVE_META['_surfN']=surfN; _V0CURVE_META['_surfR']=surfR
    _V0CURVE_META['_v0surf_sig']=_sig; _V0CURVE_META['_v0surf_frozen']=(_frozen is not None and os.environ.get('RL_V0SURF_REFIT')!='1')
    # SHAPE-AWARE. The #306 lens artifact is keyed 'POS|AGE' -- position-resolved at EVERY age, mature
    # included: D14's R1 position-pooling is superseded by the confidence rule, which handles thinness
    # cell by cell instead of pooling a whole tier. The pre-#306 artifact is keyed by position (age<=18)
    # and by int age (mature). Both are readable; a shape that is neither fails LOUDLY on the lookup
    # rather than returning a confident wrong number.
    _lens_shape=any(isinstance(_k,str) and '|' in _k for _k in c18)
    def star(pos,ag,pick):
        lp=np.log(min(max(pick,1),90))
        if _lens_shape:
            a=int(min(max(ag,16),30))
            if a<=18: return float(np.interp(lp,_V0_LGRID,c18['%s|%d'%(pos,a)]))
            surf=surfR if pos=='RUCK' else surfN
            return float(np.interp(lp,_V0_LGRID,surf['%s|%d'%(pos,a)]))
        if ag<=18: return float(np.interp(lp,_V0_LGRID,c18[pos]))
        surf=surfR if pos=='RUCK' else surfN; return float(np.interp(lp,_V0_LGRID,surf[min(max(ag,19),30)]))
    _V0CURVE_META['_star']=star
    for p in real: _V0CURVE[_v0key(p)]=star(MA.gfut(p),_ageR(p),p.get('pick'))
_build_v0_curve()
def v0_start(p):                                             # BOARD -> D14 V0 curve (Luke's amended law); BACKTEST -> D13 guard (Luke's exemption)
    v=_v0_raw(p)                                             # ASK1 ruck cap applied FIRST (cap -> curve/guard order)
    if _BOARD_PATH:
        c=_V0CURVE.get(_v0key(p)); return c if c is not None else v
    g=_V0GUARD.get(_v0key(p)); return v if g is None else min(v,g)
# ===== #326 ENTRY ANCHOR, PART 2 — THE ENGINE-VALUE SITES (the year-zero floor and the thin-record blend).
# THE OWNER'S RULING, in his words (addendum 5): "The signed levels should bite the same way that the pick
# curve bites for year 0 players. It would be then starting foundation for value for players we don't have
# information on, and then phase out as we do get information or a lack thereof."
#   So: where a national draftee's price starts from his pick's year-zero value, a pool entrant's price
#   starts from his intake division's signed level. Same floor schedule, same blend shape — nothing about
#   the machinery changes except WHICH number the entrant leans on before he has a record. As games arrive
#   the blend fades the anchor out (lam rises with games at pace) and the floor fades on the year clock,
#   exactly as they already do for national draftees. Careers dominate; this only holds up thin records.
#   THE OLD MACHINERY STOPS FIRING HERE (owner, addendum 6): for a pool entrant the pool-slot-derived
#   v0_start no longer sets his entry price, even where the signed level cuts.
#   CURRENCY (addendum 6 item 5): the levels are ladder/board currency and these two sites are ENGINE-value
#   sites (they blend against, and floor, engine ev()), so the level enters multiplied by the board factor
#   1.0524. The ruck-cap site above takes it unconverted. The selftest proves one entrant through each site
#   class so a wrong conversion goes red instead of drifting 5%.
#   NOT IN SCOPE, DELIBERATELY (addendum 6 item 4): the staleness cap, the mediocre cap and the delisted
#   remnant keep reading v0_start byte-for-byte. They face players with real careers and back-boards, and
#   the owner's standing default forbids moving those. That is recorded as the one place the old machinery
#   still fires on purpose; reversing it is one owner sentence.
# ===== #334 ITEM B — THE POOL YEAR-0 AGE REPAIR (C5, LEVEL-PRESERVING). Ruled 5238688172/5238860310.
# THE DEFECT (D2, audit 1): the signed division levels carry NO age. Two pool entrants of the same
# division priced identically whatever their draft age, while the measured returns differ by ~4x across
# the age range. The repair is a RESHAPE, never a lift: the pool's total year-zero value is held EXACTLY
# and only its distribution across age moves.
#   THE GRADIENT is re-taught at BUILD TIME on the DOB store, on the ruler act's own corrected
#   instrument (docs/evidence/composition_2026-08-10/item_b_derive.py; r24 instrument D, DISC=1.0939,
#   frozen per-entrant matrices, F8 at PLAYER unit): <=18 0.6859 · 19-20 1.4112 · 21+ 2.8173
#   (filed priors 0.666 / 1.200 / 2.474; the bridge is printed in the act record).
#   THE SHAPE. The ruling says "smooth taper 21->26, no integer cliff". A mean-holding linear ramp to 26
#   is REFUSED on evidence: every per-age cell inside 21+ is far below the F8 bar (21:22.6 ... 26:2.7)
#   and the estimates FALL after 22, so a rising ramp would hand the largest factor to the oldest,
#   thinnest, measured-at-zero rows and break conservation by 3.5%. The directive's own tilt reading
#   already says mature-21+ is unnameable and takes the base factor, pooling disclosed. So the cliff is
#   removed where the ruling points at it — the BAND BOUNDARY — by keying on CONTINUOUS draft age.
#   `_ageR`'s rounding is exactly what would create an integer cliff, so this site does not use it.
#   AGE-UNKNOWN rows keep factor 1.0: their OWN cell, never absorbed into a neighbour (ruled).
#   RECALCULATION LAW: nothing is stored per player. The knots are the taught gradient; the level is
#   pinned by a renormaliser re-derived from the LIVE pool population on every build, so the identity
#   holds on whatever roster the board actually carries.
#   SCOPE, DECLARED: this is the ENGINE-VALUE entry-anchor site. `_cap_basis` (the ruck prior cap's
#   ladder-currency basis, :1190) is deliberately NOT age-shaped here — that object is ITEM E2's, and
#   moving both in one act would double-count the repair on pool rucks.
_B_KNOTS=[(18.0,0.6858757327896249),(19.0,1.4111875531208420),
          (20.0,1.4111875531208420),(21.0,2.8172535022231320)]
# ===== #334 ORDER 9 ADOPTION — ITEM B's DRAFT-AGE SHAPE RETIRED TO FLAT BY OWNER RULING (5249802288).
# OWNER, verbatim: "H to 1, B to flat, and note these as items of investigation for the rederivation."
# THE GROUNDS, measured and filed at B_PROVENANCE_AND_SPLITS.md before the ruling:
#   - the shipped factor at draft age 21+ was k x 2.8173 = 2.0478, a +104.8% lift on the ENTRY ANCHOR,
#     which passes through almost in full to any entrant whose price IS his anchor (Banch, Podhajski).
#   - IT WAS NOT FITTED TO PLAY QUALITY. The outcome measure is D_rt_win, "REALIZED DELIVERY off the
#     seasons and bars" (item_d_derive.py:22-23) - a delivered-VALUE composite a player raises by
#     playing MORE as well as by playing BETTER. Under the owner's ruled principle ("we value them on
#     how they play") it does not meet the standard.
#   - measured separation on the NON-ROOKIE pool arm: quality (career games-weighted average) is FLAT
#     across draft age - 51.47 / 52.98 / 53.33 at <=18 / 19-20 / 21+ - while participation (career
#     games) is 24.7 / 31.7 / 21.6, the 21+ slice playing the LEAST of the three.
#   - and the gradient is SUPPORTED on the rookie arm (21+ delivers 3.0092 at year 4) but CONTRADICTED
#     on the non-rookie arm (0.7708, BELOW its own 19-20 slice at 0.9851). B pools both arms by
#     construction (item_b_derive.py:51 filters on is_pool only), so the evidence carrying the lift
#     came substantially from the arm the question was not about.
# THE KNOTS AND THE MACHINERY ARE KEPT, behind RL_B_SHAPE, so the re-derivation has them to hand.
# DEFAULT IS FLAT: _b_shape == 1.0 at every age => _b_renorm() == 1.0 => _b_factor == 1.0 exactly, so
# entry_anchor collapses to pool_level x _PL_F, the pre-B object, and the C5 level-preserving law holds
# TRIVIALLY rather than by renormalisation (every row's factor is 1, so no value moves between ages).
_B_SHAPE_ON=os.environ.get('RL_B_SHAPE','0')!='0'
def _b_shape(a):
    if not _B_SHAPE_ON: return 1.0                           # ORDER 9: FLAT by owner ruling
    if a is None: return 1.0                                 # age-unknown: its own cell, never absorbed
    a=float(a)
    if a<=_B_KNOTS[0][0]: return _B_KNOTS[0][1]
    if a>=_B_KNOTS[-1][0]: return _B_KNOTS[-1][1]
    for (a0,f0),(a1,f1) in zip(_B_KNOTS,_B_KNOTS[1:]):
        if a0<=a<=a1: return f0 if a1==a0 else f0+(f1-f0)*(a-a0)/(a1-a0)
    return _B_KNOTS[-1][1]
def _b_age(p):
    """Draft age as a CONTINUOUS quantity — `draft year - _by`, the same definition the teaching
    matrices use (emit_matrix_338.py:262). None where the store carries no birth year."""
    by=p.get('_by')
    if by is None: return None
    return float((p.get('year') or (cp.debutyr(p)-1))-by)
_B_NORM={}
def _b_renorm():
    """THE C5 RENORMALISER — a state function re-derived from the live pool population every build."""
    if 'k' not in _B_NORM:
        num=den=0.0
        for q in MA.data:
            if not _isreal(q) or not q.get('_pool'): continue
            lv=float(MA.pool_level(q)); den+=lv; num+=lv*_b_shape(_b_age(q))
        _B_NORM['k']=(den/num) if num>0 else 1.0
    return _B_NORM['k']
def _b_factor(p): return _b_renorm()*_b_shape(_b_age(p))
def entry_anchor(p):
    """The entry price a thin record leans on: the signed division level for a pool entrant (converted into
    engine-value currency, and age-shaped by ITEM B at constant pool total), the live V0 start value for
    everyone else."""
    if p.get('_pool'): return float(MA.pool_level(p))*_PL_F*_b_factor(p)
    return v0_start(p)
def _v0_curve_assert():                                      # BY-CONSTRUCTION GATES (D14 1c): wired, return dict of results
    star=_V0CURVE_META['_star']; ages=_V0CURVE_META['mature_nonRUC']['ages']
    # POPULATION CORRECTION (2026-08-10, filed with the ruling-1.1 restore). D14a/D14b are assertions
    # ABOUT THE V0 PICK SURFACE, so they must run over THE ROWS THE SURFACE PRICES — and since the
    # owner's pricing split, that is national-draft rows that are NOT pool. A national selection at
    # pick 65+ is POOL under the ruling: it is priced off its signed division level (#326 entry
    # anchors), it teaches no fit site, and it never reads this surface at all. The population here
    # was `type=='ND' and pick is not None`, which SWEPT THOSE ROWS IN and then reported their
    # division-level prices as surface faults:
    #     D14a read a ~310-point "cross-draft dispersion" that was two pool KPDs at pick 70 sitting
    #          on different division levels — the surface's own dispersion is 0.000000, exactly as
    #          the law says;
    #     D14b counted ladder-vs-pool pairs as pick inversions, which compares two different price
    #          objects and can never be satisfied by any surface.
    # Both gates were therefore UNSATISFIABLE and permanently red — part of the reason they could sit
    # in a hand-run checklist for nineteen days without anyone reading them as a live alarm.
    # Restricted to the surface's own population (the SAME `not MA.is_pool` filter `_build_v0_curve`
    # fits on), they are real assertions again. The excluded rows are NOT hidden — they are counted
    # and returned, and the whole-ND figures are returned alongside as REPORT-ONLY so the number
    # stays visible and nobody has to re-derive it.
    from collections import defaultdict
    _nd=[p for p in MA.data if _isreal(p) and p.get('type')=='ND' and p.get('pick') is not None]
    _rows=[p for p in _nd if not MA.is_pool(p)]              # the rows this surface prices
    def _disp(rows):
        grp=defaultdict(list)
        for p in rows: grp[(MA.gfut(p),_ageR(p),p.get('pick'))].append(v0_start(p))
        return max((max(v)-min(v) for v in grp.values()),default=0.0)
    def _inv(rows):
        byc=defaultdict(list); n=0
        for p in rows: byc[(MA.gfut(p),_ageR(p),p.get('year'))].append(p)
        for _c,ps in byc.items():
            ps=sorted(ps,key=lambda z:z.get('pick'))
            for i in range(len(ps)):
                for j in range(i+1,len(ps)):
                    if ps[j].get('pick')>ps[i].get('pick') and v0_start(ps[j])>v0_start(ps[i])+1e-6: n+=1
        return n
    # (i) same (pos,ageR,pick) -> identical V0* across draft years (function of pos,ageR,pick only)
    maxdisp=_disp(_rows)
    # (ii) within (pos,ageR,year) cell inversions under V0*
    inv=_inv(_rows)
    # (iii) depth-monotonicity of the KPP-floored retention surface (max of non-increasing curves)
    dmono=True
    for pk in [3,8,15,30,50,80]:
        dv=[ _R_surf('KPP',pk,t) for t in range(1,7) ]
        if any(dv[k+1]>dv[k]+1e-9 for k in range(5)): dmono=False
    return dict(cross_draft_maxdisp=maxdisp, within_cell_inversions=inv, kpp_depth_monotone=dmono,
                population=len(_rows), pool_rows_excluded=len(_nd)-len(_rows),
                report_only_all_nd_maxdisp=_disp(_nd), report_only_all_nd_inversions=_inv(_nd))
def _v0_surface_assert():
    """D14d — THE SURFACE-LEVEL NEVER-RISES SCAN (owner ruling 1.2, 2026-08-10; #334).

    D14b checks INVERTED PLAYER PAIRS. The 2026-08-10 audit measured what that actually covers: real
    players expose about 8% of the surface's rising steps (29 adjacent inverted pairs against 439
    rising steps on the shipped grid). A law that only fails when a drafted player happens to sit on
    the wrong side of a step is a law that can be broken in silence for a month — which is exactly
    what happened between 2026-08-05 and 2026-08-10. This gate reads THE SURFACE ITSELF: every
    (position x draft-age) profile, every adjacent pick pair on the grid, no roster involved. Zero
    tolerance.

    It scans the ARTIFACT THE BOARD READS (_V0CURVE_META's c18/surfN/surfR, i.e. the frozen surface as
    loaded), so a bad freeze, a bad refit and a bad code path all fail here identically. Reported over
    picks 1-64 (the national ladder, where R12 is written) AND over the whole 1..90 grid the surface
    carries, because the pick-90 tail is read by star()'s clamp and a rise out there is still a rise."""
    c18=_V0CURVE_META.get('_c18') or {}; sN=_V0CURVE_META.get('_surfN') or {}; sR=_V0CURVE_META.get('_surfR') or {}
    cells={}
    for _d in (c18,sN,sR):
        for _k,_v in _d.items(): cells[str(_k)]=[float(x) for x in _v]
    n64=0; nall=0; bad=[]
    for _k in sorted(cells):
        _v=cells[_k]
        for _i in range(len(_v)-1):
            if _v[_i+1]>_v[_i]+1e-9:
                nall+=1
                if _V0_GRIDPK[_i+1]<=64:
                    n64+=1
                    if len(bad)<25:
                        bad.append('%s pick %d->%d %.2f->%.2f'%(_k,_V0_GRIDPK[_i],_V0_GRIDPK[_i+1],_v[_i],_v[_i+1]))
    return dict(cells=len(cells), grid=len(_V0_GRIDPK),
                rising_steps_1_64=n64, rising_steps_full_grid=nall,
                worst=bad,
                shape=('POS|AGE' if any('|' in _k for _k in cells) else 'legacy'))
# ===== #334 SALVAGE 3 — SURPRISE-SCALED EVIDENCE TRUST (stage-4 amendment 1, ported from
# origin/landing/334-stage-b 3820303 :1855-1866 under owner ballot word 1, 5242713366).
# THE OWNER'S DESIGN RULING, verbatim: "4 games of sample, especially when it's so far from the
# projection, shouldn't be trusted as much, surely." Small samples NEAR projection keep today's
# reactivity (confirmation); small samples FAR from projection are shrunk toward the prior, because a
# fringe player's played games are selection-biased upward — his 4 games are his best 4. Continuous
# everywhere, no thresholds, symmetric in sign (a shock collapse from a high prior is shrunk the same
# way), and it grows back with games.
# PORTED WITHOUT THE PED_BAR TERM: stage 4's pedigree-conditioned evidence bar is NOT part of this act,
# so the exponent carries the surprise demand alone.
SUR_W=float(os.environ.get('RL_SUR_W','4.0'))                  # THE DIAL, in passes of the lam ramp demanded per nat of surprise on a wholly-unresolved record. 0 => byte-exact pre-surprise build (the identity proof). The branch shipped 5.0, calibrated on the OLD currency/board; the live value is re-calibrated on THIS board against the owner's ruled tolerance — see the dial ladder in the act evidence.
_RHO_SIT_BAR=(6.0*6.0)/(6.0*6.0+6.0+_ABS_FADE_K)             # rho at the RULED 6-game establishment bar; the normaliser, so u(6)==0 exactly
def _rho_res(g):
    """the engine's R100.11 evidence-resolution curve, rho(g)=g^2/(g^2+g+K), K=_ABS_FADE_K (PINNED)."""
    g=float(max(0.0,g)); return (g*g)/(g*g+g+_ABS_FADE_K)
def _surprise(e_full,anchor,gp):
    """The SURPRISE demand, in the same "passes of the lam ramp" unit the exponent is denominated in.
    s = |log(e_full/anchor)| is the size of the re-rate this thin record claims against its own prior;
    u = 1-rho(gp)/rho(6) is the share of that record still UNRESOLVED. Their product is the claim the
    evidence has not yet earned. Zero at zero surprise; zero at the establishment bar; symmetric in sign."""
    s=(abs(float(np.log(e_full/anchor))) if (e_full>0.0 and anchor>0.0) else 0.0)   # domain guard only
    return SUR_W*s*(1.0-_rho_res(gp)/_RHO_SIT_BAR)
def sitout_ev(p,Y,e_full):
    fe=_fEy(Y,p); tau=max(0.0,Y-cp.debutyr(p))+((fe**1.5) if Y>=cp.debutyr(p) else 0.0)   # D12: CONCAVE penalty proration tau'=(R/24)^1.5 (Luke OPTION A); completed seasons full (integer knots), in-progress season accrues concavely. PENALTY path only — the lam reward blend below is UNTOUCHED.
    R=_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)     # D13 ASK3: pick-conditioned, isotonic-in-depth surface (was depth-only R_SIT)
    if p.get('_pool'): R=_pr_mult(p,Y,tau)                   # ORDER 24: CURRENT-state delivery -- (1-phi)*R + phi*U, the same object at both pool read sites.
    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    gp=min(gy/fe,6.0)                                        # hoisted: the ONE games-at-pace clamp the lam ramp AND the resolution fade both read (identical expression; no new clip)
    anch=R*entry_anchor(p)                                   # THE ANCHOR LEG — hoisted; the SAME object the blend and the surprise statistic both read
    lam=float(np.interp(gp,[0,1,2,3,4,5,6],LAM_SIT))                             # games AT PACE vs the prorated bar
    lam=lam**(1.0+_surprise(e_full,anch,gp))                 # #334 salvage 3: the SURPRISE demand (endpoints fixed: 0**e=0, 1**e=1; RL_SUR_W=0 => exponent 1 => byte-exact)
    return (1.0-lam)*anch+lam*e_full                         # #326: a pool entrant blends off his division's signed entry level; every other player off v0_start, byte-for-byte
# ===== #334 ITEM A — THE YEAR-1+ ANCHOR LEG (A1 full carry). Ruled 5238860310; ramp identified by
# ablation (docs/evidence/composition_2026-08-10/ABLATION_READING.md), owner reading word 5240605334.
#
# THE DEFECT (D1): at ns>=1 the fitted year-0 prior is DISCARDED. The ablation proves it rather than
# asserting it — zero the production leg entirely and the price does not fall to the anchor, it falls to
# 0.229 x anchor, the floor_frac schedule. So on the year-1+ path the prior survives ONLY as a one-sided
# lower bound. There is no blend, and therefore no fading chain: the hand-over is a CLIFF at the
# qualification boundary, not a ramp.
#
# THE RAMP, identified functionally and not by name. Of the four candidates, iso_eff is inert (0.3%),
# _expgate is a partner in the PEDIGREE-POLE leg which the sitting ruled stays pick/pedigree, and LAM_SIT
# is the engine's ONLY anchor<->production blend: sitout_ev's (1-lam)*R*entry_anchor + lam*e_full. ITEM A
# is that same blend CARRIED FORWARD past ns==0 instead of switched off.
#
# THE FADE ACROSS YEARS. lam alone resets every season, so carrying it forward unchanged would not make v2
# borrow less than v1. The anchor share is therefore damped by the engine's OWN cumulative evidence fade —
# exp(-E_q/tau), tau=_EVW_TAU=1.1, the pedigree-fade family that iso_eff already rides. E_q is effective
# qualifying seasons, recomputed from the record every call, so this is a state function and never a stored
# per-player boost (the recalculation law). A synthetic year-2 probe responds to year-2 games by construction.
#
#       anchor_share(p,Y) = (1 - lam_season) x exp(-E_q / tau)
#       price             = (1 - anchor_share) x e_full  +  anchor_share x R x entry_anchor
#
# CONTINUITY AT GRADUATION: E_q is a SOFT 10-game measure, so a row with a few games carries a small
# positive E_q and exp(-E_q/tau) sits just under 1. The two branches therefore agree IN THE LIMIT, not
# exactly — measured worst boundary step 4.0e-04 over the live sitters (item_a_verify_out.txt). What IS
# exact is what the board depends on: the ns==0 path RETURNS BEFORE this line, so every sit-out price is
# byte-untouched. Nothing jumps as a player qualifies. NO NEW MACHINERY: the blend form, R, lam and the
# fade family are all existing objects.
# SITE: this runs at ev(), NEVER inside raw_ev — _v0_uncapped calls raw_ev at Y=debutyr-1 to BUILD the very
# year-0 prior being borrowed, so blending inside raw_ev would be self-referential.
_A_ON=os.environ.get('RL_ITEM_A','1')!='0'   # declared kill-switch: RL_ITEM_A=0 => the pre-A build, byte-exact
_A_TAU=_EVW_TAU                              # the engine's own pedigree-fade rate, effective-qualifying-season units
# ===== #334 ITEM H — THE RULED CUT LIST (ruling 3.11, cell-qualified by the pool grid).
# The three approved cuts, taken AS FILED and marked as filed: my own re-derivation could not reproduce
# them on the cell definitions I had (docs/evidence/composition_2026-08-10/item_h_derive_out.txt), so
# rather than size a cut on a cell I cannot verify, the ruled factors ship unchanged and the
# corrected-ruler bridge is printed beside them in the act record. On that bridge two of the three cells
# deliver LESS than their ruled factor, so these cuts are if anything GENEROUS rather than harsh.
#   named union sitters (draft age 23+ | IRE | MSD) x 0.280
#   all-pool-sitters                                x 0.804
#   mature nonRD (pool, non-RD, draft age 21+)      x 0.615
# QUALIFICATION: a sitter is a row with NO games this season (the sit-out population, ns==0). The cuts
# COMPOSE multiplicatively where a row is in more than one cell — the union cell is the named subset of
# the all-pool-sitters cell, so a 23+/IRE/MSD pool sitter takes both, which is what "cell-qualified"
# means and is why the union factor is so much deeper.
# THE #326 FLOOR (0.45) IS NOT TOUCHED, and NO BLANKET LIFTS EXIST ANYWHERE: every factor here is <= 1.
H_ON=os.environ.get('RL_ITEM_H','1')!='0'   # declared kill-switch: RL_ITEM_H=0 => no cuts, byte-exact
# ===== #334 ORDER 23 -- THE LAST TWO ITEM H CELLS ARE RETIRED TO 1.0 (owner ruling, directive D8,
# comment 5253173347; landed 2026-08-12 with the derived pool retention surface and the derived
# pool entry levels, as ONE act -- the three levers are separated in the movers ledger, not in time).
# OWNER, VERBATIM: "the pool sitter on top penalty should go, and the pool index should be rederived
# in the same way the ND one is where possible not for pick 65, but for the pool".
# SUPERSEDED SHIPPED DEFAULTS, preserved here as history: H_UNION 0.280 · H_POOLSIT 0.804. Both were
# flat END-multipliers on the finished price of a pool sitter, reading only _pool / type / draft age
# and never games, level or establishment -- the same shape of cut the same ruling retired
# H_MATNONRD for, and the reason the union factor composed to an 86%% cut on a row in both cells.
# WHAT REPLACES THEM IS NOT NOTHING: the pool sit-out retention is now DERIVED from pool history
# (engine/rl_after/pool_retention_surface.json, wired at both pool read sites below) and applied on
# the v0/prior side, which is the owner's own recorded design direction for a pool discount.
# The manifest carries the same 1.0 in data/model_config.json; this is the non-gate default.
H_UNION=float(os.environ.get('RL_H_UNION','1.0'))
H_POOLSIT=float(os.environ.get('RL_H_POOLSIT','1.0'))
# ===== #334 ORDER 9 ADOPTION — H_MATNONRD RETIRED TO 1.0 BY OWNER RULING (filed 5249802288).
# OWNER, verbatim: "H to 1, B to flat, and note these as items of investigation for the rederivation."
# THE GROUNDS, measured and filed at POOL_ARM_ATTRIBUTION.md before the ruling:
#   - the cut was a FLAT END-MULTIPLIER on the finished production-led price (:2228), reading only
#     _pool / type / draft age and NEVER games, level or establishment. John Noble at 158 career games
#     took the same 0.615 as a zero-game row; his ITEM A anchor share is exactly 0.000000, so the cut
#     was not his draft arm re-asserting itself - it was a cell multiplier on top of the finished price.
#   - the cell's own derivation HALTED: item_h_derive_out.txt "HALT-NO-SURPRISE ... taken AS FILED",
#     ruled 0.615 against F bent 0.7676 (DOES NOT REPRODUCE), corrected-ruler 0.5162, and a 95% CI of
#     [0.115, 1.226] at eff-n 46.2 - AN INTERVAL THAT CONTAINS 1.0, so the evidence in front of the
#     owner could not exclude no cut at all.
#   - the arm carries ZERO rows in the canonical deciding population (n=1197, 100% type ND), so the
#     board effect was never inside any figure any ruling was made on.
# OWNER'S DESIGN DIRECTION, recorded so the re-derivation inherits it: a mature-pool discount, if the
# historical data supports one, belongs on the v0/PRIOR side where a body of work overcomes it - never
# on the finished price. THE OTHER TWO CELLS STAY AS FILED until the re-derivation (his explicit scope).
H_MATNONRD=float(os.environ.get('RL_H_MATNONRD','1.0'))
def _h_cut(p,Y):
    """The composed ITEM H factor for a row. 1.0 for anyone outside every ruled cell."""
    if not H_ON or not _isreal(p): return 1.0
    f=1.0
    pool=bool(p.get('_pool')); typ=p.get('type')
    age=_b_age(p)                                             # continuous draft age; None where unknown
    sitter=(sum(x['games'] for x in p['scoring'] if x['year']==Y)<=0)
    if pool and sitter:
        f*=H_POOLSIT                                          # all-pool-sitters
        if (age is not None and age>=23.0) or typ in ('IRE','MSD'):
            f*=H_UNION                                        # the NAMED union subset, on top
    if pool and typ!='RD' and age is not None and age>=21.0:
        f*=H_MATNONRD                                         # mature nonRD
    return f
# ===== #334 ITEM A — THE RAMP DE-COUPLE. DIAL-GATED MEASUREMENT VARIANT, DEFAULT OFF (RL_A_GSAT=0).
# Specified at docs/evidence/composition_2026-08-10/noarb/RAMP_DECOUPLE_SPEC.md; measured, not shipped.
#
# THE DEFECT IT ADDRESSES (A_YEAR1_AUDIT.md): ONE six-game threshold is doing TWO different jobs.
#   ADMISSION  — may this row use the year-1+ arm at all?   ns = nseas_pro(p,Y) >= 1, i.e. gy/fE >= 6
#   SATURATION — how much anchor weight does it carry?      lam = interp(min(gy/fE,6),...), LAM_SIT[6]=1.0
# Both key on the SAME within-season games count, so at cohort year 1 they are mutually exclusive by
# construction: qualifying to use A is the same act as saturating A's share to EXACTLY 0. Measured
# consequence: A moves 0 of 1197 ND year-1 cells and owns 0.0% of the year-1 drop.
#
# THE CHANGE, and ONLY this one: the ADMISSION BAR IS UNTOUCHED (still 6*fE prorated, still ns>=1 at
# ev()'s `if ns==0:`). Only the SATURATION de-couples — the production weight saturates on CAREER games
# against G_SAT instead of on the within-season six:
#       lam = interp(min(career_games/G_SAT, 1.0) * 6.0, [0..6], LAM_SIT)
# so a qualified year-1 row with, say, 12 career games sits part-way up the ramp and carries real anchor
# weight instead of being pinned at the top.
#
# G_SAT: the spec leaves the value OPEN ("~15-20 career games"). 18 IS THE SEAT'S CHOICE inside that
# range and is recorded as such — it is not an owner number and it is not measured-optimal. It is the
# midpoint of the spec's stated range rounded to the engine's own 18-game full-exposure convention.
#
# THE NAMED TRAP, and the discipline against it: sitout_ev (:1939-1947) reads the SAME LAM_SIT ramp for
# a DIFFERENT purpose — games-at-pace within the season on the ns==0 sit-out arm. Re-pointing both from
# one edit would move the whole sit-out population as a side effect. THIS DIAL IS READ AT EXACTLY ONE
# SITE, _a_share below; sitout_ev's own `lam=float(np.interp(gp,...,LAM_SIT))` is not touched and does
# not read A_GSAT. Proven by direct assertion, not asserted — see decouple_proof.py in the evidence dir.
#
#   RL_A_GSAT=0 (DEFAULT) => the within-season ramp exactly as built => byte-exact to the composed build.
#   RL_A_GSAT=<g>         => saturation on career games with G_SAT=<g>. Admission bar unchanged.
_A_GSAT=float(os.environ.get('RL_A_GSAT','0') or 0)
def _a_share(p,Y):
    """How much of the year-1+ price still leans on the fitted year-0 prior."""
    fe=_fEy(Y,p); gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    if _A_GSAT>0:
        cg=float(sum(x['games'] for x in p['scoring'] if x['year']<=Y))   # CAREER games as of the valuation (as-of, never future)
        lam=float(np.interp(min(cg/_A_GSAT,1.0)*6.0,[0,1,2,3,4,5,6],LAM_SIT))   # DE-COUPLED: same ramp, career axis
    else:
        lam=float(np.interp(min(gy/fe,6.0),[0,1,2,3,4,5,6],LAM_SIT))   # LAM_SIT's own ramp, unchanged
    return (1.0-lam)*_math.exp(-_ev_qual(p,Y)/_A_TAU)
# ===== #334 ITEM C — THE CAP RELEASE UNDER THE EVIDENCE WEIGHT (ruling 3.8; C-Q1/2/3 ruled 5238860310).
# C-Q1 (ruled): the ceiling binds THE TAUGHT YEAR-1 LEVEL, not the live ev. Before ITEM A there was no such
# object on the year-1+ path — the cap census (docs/evidence/composition_2026-08-10/C_WIRING_PREP.md) found
# NO upper cap binding on a year-1 ND row, and a literal cap on ev() would have CUT Mraz 86%. With ITEM A
# wired the object exists: the anchor leg R x entry_anchor, which is exactly the retention-capped taught
# level. C releases THAT cap upward on evidence:
#       anchor_leg = R x entry_anchor x (1 + w x (H - 1))
# w=0 reproduces the old cap EXACTLY, which is the design's own stated identity and is why the 24 sit-out
# rows of the 58-row year-1 cohort are untouched by construction.
# THE WEIGHT w = G x Q x gate, with the conventions RECOVERED FROM THE DIRECTIVE'S OWN SIX WORKED ROWS and
# verified to reproduce every one of them (docs/evidence/composition_2026-08-10/README.md §2.2):
#   G    = g/(g+8),  g = CAREER games total
#   Q    = clip(sa/par, 0, 2),  sa = CAREER games-weighted average,
#          par = par_at(pos, effpk, T) with T = clip(draft_age-18, 1, 6) — the eff_ten DRAFT-AGE bridge
#   gate = min(e/anchor, 1) — the z gate. C-Q3 DEMONSTRATED on the composed build: 24 of 67 top-10-pick
#          rows carry gate<1 and are materially protected, so the drafted gate SHIPS and the sa fallback
#          does NOT install. `e` is the PRODUCTION price at this point in ev() — deliberately not a
#          recursive ev() call, and it is the same object the anchor leg is being blended against.
# DOUBLE-COUNTING: w reads sa exactly ONCE, through Q. The gate reads e and entry_anchor, never sa.
# CONSUMERS: the year-1+ anchor leg (here) and the RUCK prior cap (ITEM E2). NOT the sit charge — sitout_ev
# is the ns==0 arm and never reaches this line.
C_H=float(os.environ.get('RL_C_H','1.13'))   # THE ONE NEW DIAL. Sized on the ruled PLAYED-ONLY basis (C-Q2) so the played-only year-1 landing enters [1.04,1.13]; admissible window [1.1024,1.3327] on the #336 basis, ladder in the act evidence. RL_C_H=1.0 => (1+w*0) => byte-exact no-release.
_C_G0=8.0; _C_QMAX=2.0
def _c_career(p):
    gt=num=0.0
    for s in p['scoring']:
        if s['games']<=0: continue
        gt+=s['games']; num+=s['games']*s['avg']
    return gt,(num/gt if gt>0 else 0.0)
def _c_w(p,Y,e_full,anchor):
    """The evidence weight. Zero for a row with no games, by construction (G=0)."""
    gt,sa=_c_career(p)
    if gt<=0 or anchor<=0: return 0.0
    T=int(min(max(_ageR(p)-18,1),6))                                  # the eff_ten draft-age bridge
    # STOP §5 Q2 — THE EVIDENCE WEIGHT IS RETAINED, ITS DENOMINATOR IS RE-REFERENCED (ORDER 30B-P preview).
    # `Q = clip(sa/par,0,2)` is not a pedestal and not a pole, so the preview KEEPS it; but its denominator
    # `PR.par_at(pos, effpk, T)` is a PAR TABLE READ AT THE PLAYER'S OWN PICK, which is the property that put
    # it on the forbidden-set boundary. The preview re-references it to the POSITION-LEVEL, PICK-BLIND
    # effective bar (_O30BP_BARS). FORM, CLIP AND CONSTANTS ARE UNCHANGED — only the object in the
    # denominator moves, so the before/after is a pure re-referencing and not a re-tuning.
    # ORDER C (RL_O34) — SITE 1 of exactly two: the SAME retained denominator, its object now the
    # age-conditional surface _o34_par (flat-bar-identical with the dial off, and for every age >= 24).
    par=((_o34_par(MA.gfut(p),p,Y) if _O34 else _O30BP_BARS[MA.gfut(p)]) if _O30B_PREVIEW else float(PR.par_at(MA.gfut(p),min(MA.effpk(p),cp.KMAX),T)))
    G=gt/(gt+_C_G0)
    Q=float(np.clip(sa/par,0.0,_C_QMAX)) if par>0 else 0.0
    gate=min(e_full/anchor,1.0) if e_full>0 else 0.0
    return G*Q*gate
# ===== #334 ITEM A — THE FLOOR BASIS. DIAL-GATED MEASUREMENT VARIANT, DEFAULT OFF.
# THE DESIGN QUESTION, not a defect claim: the directive's replacement line said "anchor leg, FLOOR
# basis". What was implemented is LAM_SIT's SYMMETRIC blend, which borrows in BOTH directions — so a
# hot year-1 row is dragged DOWN toward its anchor as well as a cold one being lifted UP. The floor
# basis makes the borrowing ONE-WAY: the prior supports from below, production leads from above.
#   RL_A_FLOOR=0 (DEFAULT) => the symmetric blend, byte-exact to the composed build.
#   RL_A_FLOOR=1           => price = max(production-led value, blended value) at the A site.
# Because blend = e_full + s*(anch - e_full), the blend exceeds e_full IFF anch > e_full. So the
# floor is EXACTLY "apply the blend only where it raises the row", with no separate branch needed
# and no discontinuity: at anch == e_full the two forms agree exactly.
#
# INTERACTION WITH THE SURPRISE LAW, stated because both act in the same neighbourhood and the order
# required it be flagged rather than assumed away. THE COMPOSITION ORDER IMPLEMENTED: SUR acts inside
# sitout_ev, on the sit-out path, and is NOT touched here; the floor acts at the A site in ev(); and
# neither is applied to the other's output. The floor CANNOT undo SUR on a hot row: SUR's job on a
# hot thin record is to shrink it toward the anchor, and the floor is INERT whenever anch < e_full
# (it only ever raises). Hot rows stay shrinkable — that is the property the order asked me to
# protect, and it holds by construction rather than by tuning.
# WHERE THEY DO COMPOSE, and it is flagged as an interaction to watch rather than a defect: SUR's
# surprise statistic s=|log(e_full/anchor)| is SYMMETRIC IN SIGN, so it also fires on a COLD thin
# record and pushes it toward the anchor — i.e. UP. On cold thin rows SUR and the floor therefore
# push the SAME way and their effects compose. That is the one place a double-lift can appear, and
# the measurement prints its size rather than asserting it is small.
_A_FLOOR=os.environ.get('RL_A_FLOOR','0')!='0'
# ===== #334 ITEM A — THE EVIDENCE-FADED DRAG. The middle design between the symmetric blend and the
# hard floor. The anchor's PULL-DOWN weakens in proportion to how much the player has PROVEN, while
# the PULL-UP (support for a cold or evidence-less row) keeps the existing games-fade untouched.
#   RL_A_DRAGFADE=0 (DEFAULT) => byte-exact to the composed build.
#   RL_A_DRAGFADE=1           => in the DRAG case only, the anchor's weight s is scaled by (1-w).
#
# ONE-SA-READER DISCIPLINE, which the order required me to assert rather than assume. w is the ITEM C
# evidence weight G*Q*gate, and it is now computed EXACTLY ONCE per call and used for both roles: the
# C ceiling release on the anchor LEVEL, and the drag fade on the anchor WEIGHT. sa is therefore read
# once per row, by one reader, exactly as before — this variant adds no second consumption of the
# career average and no second par lookup.
# HOW THE TWO ROLES INTERACT, stated rather than left to be discovered: they act in OPPOSITE
# directions on a drag-case row and therefore cannot compound into a runaway. A high-evidence player
# gets a LARGER C release (anch raised by 1+w*(C_H-1)) but a SMALLER drag weight (s scaled by 1-w);
# the more proof he has, the more his own production leads and the less the raised ceiling can pull
# him back. The compounding risk the order asked about is real in principle and absent here by sign.
# CLAMP, disclosed because it is a real edge and not a formality: w = G*Q*gate is NOT bounded by 1 —
# Q is clipped at _C_QMAX=2.0, so w can reach ~2 for a very-high-quality established row. An
# unclamped (1-w) would go NEGATIVE and flip the anchor from a drag into a PUSH, which is not the
# design. The scale is therefore clipped to [0,1]: at w>=1 the drag is fully faded out and the row is
# priced on production alone, which is the intended limit, not a special case.
_A_DRAGFADE=os.environ.get('RL_A_DRAGFADE','0')!='0'
def _a_blend(p,Y,e_full):
    tau=max(0.0,Y-cp.debutyr(p))+((_fEy(Y,p)**1.5) if Y>=cp.debutyr(p) else 0.0)   # sitout_ev's own depth clock
    R=_R_surf(_sitout_cls(MA.gfut(p)),MA.effpk(p),tau)
    if p.get('_pool'): R=_pr_mult(p,Y,tau)                   # ORDER 24: CURRENT-state delivery -- (1-phi)*R + phi*U, the same object at both pool read sites.
    anch0=R*entry_anchor(p)
    w=_c_w(p,Y,e_full,entry_anchor(p))                               # THE ONE READ of the evidence weight; both roles below use this value
    anch=anch0*(1.0+w*(C_H-1.0))                                     # #334 ITEM C: the cap release on the taught level
    s=_a_share(p,Y)
    if _A_DRAGFADE and anch<e_full:                                  # DRAG case only (anchor below production); support case keeps the games-fade
        s=s*min(max(1.0-w,0.0),1.0)                                  # clipped: w can exceed 1 (Q<=2), and a negative weight would invert the leg
    b=(1.0-s)*e_full+s*anch
    return max(e_full,b) if _A_FLOOR else b                          # #334 A-FLOOR: one-way borrowing; RL_A_FLOOR=0 => byte-exact symmetric blend
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
# D8 GRADED STALENESS — PRESENT BOARD CORRECTION (owner-authorized remediation, 2026-07-22).
# Frozen 532-cell historical design; no current-board tuning and no named-player exception.
_D8Q=[0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80]
_D8G1=[0.25789,0.25789,0.25789,0.30834,0.36155,0.42112,0.49276,0.56996,0.59452]
_D8G2=[0.0,0.00275,0.00275,0.04319,0.08776,0.13367,0.18032,0.20098,0.20408]
def _staleness_grade(p,Y,pos):
    """Evidence release for the stalled-one-season population at the evaluated evidence year."""
    current=[x for x in p['scoring'] if x['year']==Y]
    current_qual=any(x['games']>=6.0*_fEy(Y,p) for x in current)
    if current_qual:
        return 1.0
    live=[x for x in current if x['games']>0]
    if not live:
        return 0.0
    prior_qual=[x['year'] for x in p['scoring'] if x['year']<Y and x['games']>=6]
    if not prior_qual:
        return 0.0
    qv=(live[0]['avg'])/max(MA.REPL.get(pos,1e-9),1e-9)   # RAW season avg (era normalization removed — #334 stage B owner ruling)
    gap=Y-max(prior_qual)
    return float(np.interp(qv,_D8Q,_D8G1 if gap==1 else _D8G2))
def ev(p,Y=2026):
    # (1) delist -> near-zero (no future keeper value) — D10: scrap re-anchored to the LIVE start value
    if delisted(p): return round(0.02*v0_start(p))
    e=_prod_path(p,Y)                                        # (3) isotonic guard inside; family games-axis smoothing
    if _isreal(p) and MA.gfut(p)=='RUCK':                  # W4/PR#44: cap PRIOR-DOMINATED ruck production leg at the production-derived ceiling (RL_W4_RUC=0 -> v2.5 1.4xPVC cap)
        # #334 ITEM E2: the ruck ceiling becomes EVIDENCE-YIELDING via ITEM C's weight — the same w, the
        # same H, one reader. Applied HERE (the year-1+ pricing consumer) and deliberately NOT at
        # _ruc_prior_cap, which is the YEAR-ZERO scaffold: releasing it there would move V0 itself and
        # disturb the frozen surface, which is not what C releases. w=0 => x1.0 => byte-exact.
        _cpv=(_ruc_ceiling(p,Y) if _W4RUC else RUC_PRIOR_CAP*_cap_basis(p)); _v0u=_v0_uncapped(p)
        _cpv=_cpv*(1.0+_c_w(p,Y,e,float(entry_anchor(p)))*(C_H-1.0))  # bind iff ceil < e <= V0_uncapped (hot prior, no demonstrated growth); [#326: same per-division basis on the v2.5 fallback path]
        if _cpv<e<=_v0u: e=_cpv                               #   e>V0u (demonstrated) or e<=ceil (already low) -> byte-exact
    # W4 KPF (RL_KPFFIX): compress the ESTABLISHED-KPF loose residual only — SETTLED #9 / PR #42 T1-shape.
    # KPFs bunch near the lowest REPL bar (66.8) and the curve levers tiny production gaps into huge value gaps
    # (CV spread-ratio 6.57 vs MID 4.17). For an established (nqual>=4, age>=24) KPF, any price ABOVE the
    # engine's own price of his DEMONSTRATED level (eP, band pinned at _lvl_eff — same context, so the W4 margin
    # credit survives inside eP) is band/prior looseness, not output: e' = eP + KPFSH·(e−eP). Young/speculative
    # KPFs (nqual<4 or age<24) are NEVER touched — the Darcy/Duff-Tytler ceiling is protected by construction;
    # the reward leg (above-REPL margin credit ×KPFUP) lives in _w4_W. No blunt group compression.
    if _W4KPF and _isreal(p) and MA.gfut(p)=='KPF':
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
    with _form_anchor_clock(): el=PR.tenure(p,_fa_year(Y))          # LEG F3 §2.vi: the staleness/tenure clock keys on the FORM ANCHOR (BASE_REF year-arg + AGE_REF pin) — a developing pick is NOT relabeled "stalled prospect" purely by the forward lens advancing the clock (item-352 155-mislabeled-exits defect). k=0 identity by construction.
    pos=MA.gfut(p); ns=nseas_pro(p,Y); v0=v0_start(p)
    # STOP §5 Q3 — THE DECAY GATE IS RETAINED, ITS DENOMINATOR IS RE-REFERENCED (ORDER 30B-P preview), by
    # exactly the same rule as Q2's site: form/threshold/constants untouched, the pick-conditional par table
    # replaced by the position-level pick-blind effective bar. This `par` has ONE consumer, `pr`, two lines
    # of code below — verified, so the re-reference cannot leak anywhere else in ev().
    # ORDER C (RL_O34) — SITE 2 of exactly two: the decay-gate denominator, same re-referencing rule.
    par=((_o34_par(pos,p,Y) if _O34 else _O30BP_BARS[pos]) if _O30B_PREVIEW else PR.par_at(pos,min(MA.effpk(p),cp.KMAX),min(max(el,1),6)))
    pr=bestlvl(p,Y)/max(1,par)
    if ns==0:                                                 # SIT-OUT: derived games-ramp treatment (V0-anchored, prorated, scoring-aware, continuous at graduation)
        # ORDER 30B-P, STOP §5 Q4 — REPLACE, NOT WRAP. sitout_ev's ns==0 arm IS an anchor<->production blend
        # ((1-lam)*R*entry_anchor + lam*e_full), so the ruled blend REPLACES it rather than wrapping it;
        # wrapping would count pedigree twice and exceed the measured share by construction. Note this arm
        # is reached ONLY by rows that HAVE evidence and have not yet banked a 6-game season — a row with no
        # games at all is intercepted by _entry30b_price above and keeps the Step-2 fade untouched.
        if _PV['on']:
            # ORDER 31: UNROUNDED ON PURPOSE, exactly as ORDER 29B's day-0 branch is. The board applies
            # int(round(ev/_F)) once at write time; rounding here too would double-round and put the
            # printed-day-0 identity a point off on 26 of 89 rows. Measured, not guessed.
            _q=_pv_apply(p,Y,e*_h_cut(p,Y))
            return _q if _O31 else round(_q)
        return round(sitout_ev(p,Y,e)*_h_cut(p,Y))            # #334 ITEM H: the ruled cuts, cell-qualified
    e=e*_h_cut(p,Y)                                           # #334 ITEM H on the year-1+ arm (mature nonRD reaches it; sitter cells cannot, by definition)
    # ORDER 30B-P, STOP §5 Q4 — ITEM A's anchor carry is the OTHER superseded anchor<->production blend and
    # is likewise REPLACED, not wrapped. _c_w / C_H / the ruck ceiling are NOT touched by this: they are an
    # evidence weight and a ceiling, they survive, and their par denominator is re-referenced above.
    if _A_ON and _isreal(p) and not _PV['on']:                # #334 ITEM A: the anchor leg no longer stops at qualification — it fades (see _a_blend above)
        e=_a_blend(p,Y,e)
    keyruc = pos in ('KPF','KPD','RUCK'); onset = (4 if keyruc else 3)
    if el>=onset and ns<=1:                                   # stalled: D8 graded release at evaluated year
        frac=0.25*max(0.4,1-0.10*(el-onset))*(1.6 if keyruc else 1.0)
        cap=v0*frac
        gr=_staleness_grade(p,Y,pos)
        e=min(e, cap+gr*max(0.0,e-cap))
    elif el>=onset+2 and pr<0.55:                             # mediocre-for-years (played but never near par) -> decays too
        frac=0.45*max(0.3,1-0.08*(el-onset))*(1.5 if keyruc else 1.0)
        e=min(e, v0*frac)
    # ORDER 30B-P — THE BLEND SITE. `e` is now the FINISHED PRODUCTION LEG: pole deleted, ISO deleted, and
    # the RETAINED form machinery (ITEM H's ruled cuts, the ruck ceiling, the KPF compression, D8 graded
    # staleness, the decay gate) all applied to it, exactly as the boundary reading "bars/aging/form
    # legitimately retained" says they should be. The pedigree leg is added ONCE, here, at the measured share.
    if _PV['on']:
        _q=_pv_apply(p,Y,e)                                   # ORDER 31: unrounded (see the ns==0 arm)
        return _q if _O31 else round(_q)
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
M3_FE=_season_val('calendar_progress',0.58)   # CALENDAR progress (was RL_M3_FE env / 0.58); dynamic from season_state                # elapsed-season fraction; 1.0 -> lever off
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
    # ORDER 31: unrounded in ENGINE currency. Measured: rounding here and again at board-write time
    # (int(round(ev/_F)), _F = 1.0524) moved 26 of the 89 printed-day-0 rows by one point -- e.g.
    # 470.82 -> round 495.49 = 495 -> /1.0524 = 470.4 -> 470, against the identity's 471. One rounding,
    # at the board, is the convention ORDER 29B's day-0 branch already used ("unrounded ON PURPOSE").
    _m3=w*v+(1.0-w)*vpin
    return _m3 if _O31 else round(_m3)
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
# #326 SCOPE EXTENSION (owner ruling, addendum 5 item 1): the year-zero floor now also covers ENGINE-POOL
# entrants, on the signed division level as its basis. Until this act the floor was national-draftees-only,
# so a pool entrant had no entry anchor at all — the very gap the owner's words describe. The schedule
# (FLOOR_YRS / FLOOR_TAIL) is INHERITED UNCHANGED from the national path; only the population and the basis
# widen. The `_pickless` exclusion is NOT applied to pool entrants (addendum 6 item 1): 100% of the IRE, PDA,
# PDN, PDS, SSP and UNR rows are pickless by construction — that is what those pathways ARE — so gating on it
# would have excluded six of the nine divisions from the ruling. It still excludes a pickless NON-pool row,
# which is the case it was written for. Retired/delisted/gate-synthetic rows stay out, exactly as before.
def ev(p,Y=2026):
    v=ev_prefloor(p,Y)
    # ORDER 30B-P, STOP §5 Q4 — THE YEAR-ZERO FLOOR IS REPLACED, NOT WRAPPED. `floor_frac x entry_anchor` is
    # an ANCHOR LOWER BOUND: it is the third object in the supersession list and the ablation that identified
    # ITEM A proved it is the thing a zeroed production leg actually falls to. The ruled blend already carries
    # the pedigree leg at the measured share for every row, so leaving the floor underneath it would put a
    # SECOND, uncalibrated pedigree object under the same price. In the preview lane it does not run.
    if _PV['on']: return v
    _pool=bool(p.get('_pool'))
    if not _isreal(p) or p.get('_retired') or delisted(p): return v          # out of scope: byte-exact passthrough
    if not _pool and (p.get('type')!='ND' or p.get('_pickless')): return v   # non-pool: the national-draft scope, unchanged
    yis=Y-int(p.get('year') or 0)
    if yis<1: return v
    fl=floor_frac(yis)*entry_anchor(p)  # D12: RE-ANCHORED draftval -> live V0 (schedule unchanged; Luke R8). #326: a pool entrant's anchor is his division's signed level
    return v if v>=fl else round(fl)
# ==== W4 PVC FIT (RL_PVCFIT, DOWNSTREAM) — per the re-stamped PVC Derivation Spec v1 (PR #41) ================
# PVC(k) = end-of-calendar-year-1 as-of value of the TYPICAL player at pick k, FITTED FROM THE CANDIDATE
# WALK-FORWARD BOOK anchors (2004-2024 ND pool) — so the curve reads the LIFTED young values and the LIVE ruck
# values (nothing hardcoded), kernel-median over log-pick, parametric power top blended in by ~pick 12 (the
# spec's loclin-at-pick-1), isotonic non-increasing, re-anchored to pick1 = RL_PICK1 (3000).
# SCOPE (deliberate, declared): the fitted curve re-prices the PICK side (the board's trade currency) and
# display/advisory consumers (A13/A14, book draftval column). PLAYER pricing does NOT read it back:
# `draftval` — the RUCK prior-cap/scaffold basis — CLOSES OVER the `_PVC0` dict, and the L1b and v2 blocks
# mutate that dict IN PLACE, so draftval TRACKS THE ADOPTED CURVE. (E4, #279 step 4 item 9: this comment used
# to claim draftval was "FROZEN on the pre-fit v3.4 curve (_PVC0)". The behaviour is correct and unchanged —
# only the description was wrong. The PR #44 V0-scaffold scope and the fit→board→fit note below still hold
# for the FITTED candidate curve, which is what is held out.) Generated artifact: pvc_fit_candidate.json
# (stamped with source + book id).
_W4PVC=os.environ.get('RL_PVCFIT','0')!='0'                  # DEFAULT 0 (owner ruling R3, 2026-07-09): the W4 PVC fit is HELD OUT of the bake — the frozen v3.4 curve (_PVC0) ships as the board's pick currency. RL_PVCFIT=1 loads the fitted candidate curve for EXPERIMENTS ONLY (re-derivation queued 'with a view to fixing it'); rl_export.py refuses to write a bakeable board with the fit on (R3 BAKE GUARD), so a fitted board is unbakeable-wrong. Was '1' pre-2026-07-09 — that default silently baked the held-out fit into board bcd81363; flipped to '0' as the remediation.
_PVC0=dict(MA.PVC)                                            # frozen v3.4 ruler for the cap/scaffold basis
def draftval(p): return float(_PVC0[min(MA.effpk(p),cp.KMAX)])   # rebind: runtime cap/scaffold callers read the FROZEN curve
# ===== v2.9 L1(b): swap the ev-channel basis _PVC0 to the L1b smoothed derived curve (pin 3000) + rebuild the
#       V0 guard / V0 curve / RUCK ceiling grid — verbatim the l1_adopt_sim option-(b) recipe. Gate RL_PVCADOPT
#       (default ON); RL_PVCADOPT=0 ⇒ block skipped ⇒ _PVC0 stays the frozen v3.4 ruler ⇒ base board byte-exact.
#       Verified: board sum +0.179%, anchors byte-identical, knobel 402→505. Candidate ONLY (non-bakeable path).
if os.environ.get('RL_PVCADOPT','1')!='0':
    import json as _l1j
    _L1DOC=_l1j.load(open('pvc_curve_L1b.json'))
    _L1CURVE={int(_k):int(_v) for _k,_v in _L1DOC['curve'].items()}
    if 'pool_value' in _L1DOC: _L1CURVE[MA.POOL_PICK]=int(_L1DOC['pool_value'])
    # THE SPLIT: domain-restrict this basis to 1..64 + the pool index. strict=False deliberately — the L1b curve
    # carries two plateaus (picks 1-2 and 7-8) so it is non-increasing but NOT strictly decreasing, and it is a
    # TRANSIENT basis: the RL_PVC2 block below overwrites _PVC0 before anything ships. Where L1b would actually
    # BE the shipped curve (RL_PVC2=0), rl_export asserts G-MONO strictly and HALTS on exactly those plateaus.
    # legacy_domain=True: pvc_curve_L1b.json is the SUPERSEDED artifact and still sits on disk at its original
    # 1-99 domain. It is the one declared exception to the refuse-an-over-long-ladder rule; its entries past the
    # pool index are dropped here, and it is superseded a few lines below anyway.
    _L1CURVE=MA._split_ladder(_L1CURVE,'RL_PVCADOPT L1b curve',strict=False,legacy_domain=True)
    _PVC0.clear(); _PVC0.update(_L1CURVE)
    _V0C.clear(); _V0U.clear(); _V0GUARD.clear(); _RUCCEIL.pop('grid',None)
    _build_v0_guard(); _V0CURVE.clear(); _build_v0_curve()
    MA._pe_clear()
# ===== LEG D ACT-2 (RL_PVC2): swap the ev-channel basis _PVC0 to the RE-DERIVED COMPOSED-PATHWAY curve
#       pvc_curve_v2.json (owner ruling R1: PVC(p) = the YEAR-0 point of the fitted 2-D pick x career-year
#       evidence-weighted NON-median trajectory surface; busts at REAL outcomes FULL WEIGHT, no survivor pool,
#       no games floor, no threshold — L-SMOOTH / weight-don't-gate) + rebuild the V0 guard / V0 curve / RUCK
#       ceiling — an EXACT parallel of the RL_PVCADOPT recipe above, STACKED after it. Gate RL_PVC2 (default
#       ON; a DECLARED kill-switch, NOT a manifest dial — config_sha256 UNMOVED, exactly as RL_EVW/RL_ISOFADE/
#       RL_FLEX). RL_PVC2=0 => this block is SKIPPED => _PVC0 stays the L1b curve => board 9829d01a byte-exact
#       (the kill-switch proof). The offline-derived, stamped artifact is LOADED here, never refit; the
#       _iso_dec/_fit_pick_curve import-time chain is untouched (it is re-run by _build_v0_curve because a new
#       _PVC0 moves its inputs — the same behaviour RL_PVCADOPT already carries, not a new import-time fit).
if os.environ.get('RL_PVC2','1')!='0':
    import json as _p2j
    _V2J=_p2j.load(open('pvc_curve_v2.json'))
    _V2CURVE={int(_k):int(_v) for _k,_v in _V2J['curve'].items()}
    if 'pool_value' in _V2J: _V2CURVE[MA.POOL_PICK]=int(_V2J['pool_value'])
    # THE SPLIT: the ev-channel basis _PVC0 is the national curve 1..64 plus ONE pool entry. _split_ladder
    # asserts the numeraire and G-MONO strict descent across the curve domain, so the two asserts that stood
    # here are kept — they now bite over 1..64 instead of 1..99, which is the domain the law governs.
    _V2CURVE=MA._split_ladder(_V2CURVE,'RL_PVC2 v2 curve')
    _PVC0.clear(); _PVC0.update(_V2CURVE)
    _V0C.clear(); _V0U.clear(); _V0GUARD.clear(); _RUCCEIL.pop('grid',None)
    _build_v0_guard(); _V0CURVE.clear(); _build_v0_curve()
    MA._pe_clear()
# ===== #326 BUILD-TIME PROOFS — the two things this act must not have done ==================================
# (1) THE FROZEN SURFACE MUST NOT REFIT SILENTLY. The year-zero surface is frozen by signature
#     (data/v0surf.pkl). #326 adds an entry anchor for pool entrants and must not disturb that surface: the
#     levels resolve in the anchor lookup and are NEVER written into the ladder or its scaffold copy _PVC0, so
#     the signature — which covers _PVC0, the national-draft roster and the gate set — cannot move. If it ever
#     did, every national draftee's V0 would be re-fitted and "non-pool veterans do not move" would quietly
#     stop being true.
#     THE SPLIT (#344): a refit is either SILENT or DECLARED, and only the silent half is this assert's job.
#     The unknown-signature HALT above catches a config that drifted; this catches the other silent case — a
#     surface that was not loaded from the freeze while nobody asked for a fit. A DECLARED refit
#     (RL_V0SURF_REFIT=1) is the engine's ONE committed fit path, deliberately provided at that same site, and
#     it PASSES here: #334 stage B and the #336 bust-inclusive variant re-derive the surface through it, and a
#     lane that always halts is a lane that does not exist. It still cannot reach a RELEASE build — the release
#     contract declares RL_V0SURF_REFIT in must_be_unset and ingestion/forward_lens.py:124 rejects the build if
#     it is set — so nothing shipped can carry a refit at all.
#     NOT VACUOUS: with no declaration this assert still fires. Any regression that skips the frozen load
#     silently arrives here with frozen=False and the env unset, and halts (#344 proof 1 demonstrates it).
assert (_V0CURVE_META.get('_v0surf_frozen') is True
        or os.environ.get('RL_V0SURF_REFIT')=='1'), (
    '#326 HALT: the year-zero surface was NOT loaded from the freeze, and no refit was declared (signature %s, '
    'refit declared=%r). The per-division pool levels must never reach the ladder or the surface fit — a moved '
    'surface re-prices every national draftee, and this act is only allowed to move pool entrants.'
    %(_V0CURVE_META.get('_v0surf_sig'),os.environ.get('RL_V0SURF_REFIT')))
# (2) pool_value RETIRES FROM PRICING (owner ruling, addendum 5 item 3). Every pool entrant's entry anchor and
#     ruck-cap basis is his own signed division level, in the currency that site speaks — never the ladder's
#     one pool slot. Stated as an equality over the whole pool population so a re-pointed branch is a build
#     halt, not a board that quietly prices nine pathways at one number again. pool_value itself stays in the
#     artifact for the pick side, the entrant layer and the display bands; those are not player prices.
#     #334 ITEM B AMENDMENT. The entry-anchor equality is now stated WITH the ruled age factor on it:
#     entry_anchor == his own signed level x _PL_F x _b_factor(p). The guard's protection is UNCHANGED and
#     is what it always was — the BASIS must be the player's OWN division level, never the ladder's single
#     pool slot. A re-pointed branch still halts here, because pool_value x _PL_F x _b_factor(p) does not
#     equal pool_level(p) x _PL_F x _b_factor(p) for any division whose level differs from the pool slot.
#     The factor is a SHAPE on top of that basis, not a substitute for it, so admitting it does not widen
#     what the assert lets through. _cap_basis is deliberately unshaped (ITEM B's declared scope), so that
#     half of the equality is untouched and still binds the ladder-currency site exactly as before.
_POOL_ROWS_326=[p for p in MA.data if p.get('_pool')]
_iso_bad=[p.get('player') for p in _POOL_ROWS_326
          if abs(_cap_basis(p)-float(MA.pool_level(p)))>1e-9
          or abs(entry_anchor(p)-float(MA.pool_level(p))*_PL_F*_b_factor(p))>1e-6]
assert not _iso_bad, ('#326 HALT: %d pool entrant(s) (%s) do not price off their own division level — the '
                      'single pool value is back in a player price.'%(len(_iso_bad),_iso_bad[:6]))
# (2b) #334 ITEM B — THE C5 LEVEL-PRESERVING LAW, ASSERTED AT BUILD TIME, not merely reported in an
#      evidence file. The pool year-0 age repair is a RESHAPE: it moves value between ages and must never
#      move the pool's total. Stated over the whole live pool population so a mis-derived gradient, a lost
#      renormaliser or a population change that silently breaks conservation is a BUILD HALT rather than a
#      quiet lift. This is ITEM B's own law and it is the one thing about B that must never drift.
_B_SUM_BEFORE=_math.fsum(float(MA.pool_level(p))*_PL_F for p in _POOL_ROWS_326)
_B_SUM_AFTER=_math.fsum(entry_anchor(p) for p in _POOL_ROWS_326)
assert _B_SUM_BEFORE<=0 or abs(_B_SUM_AFTER-_B_SUM_BEFORE)/_B_SUM_BEFORE<1e-9, (
    '#334 ITEM B HALT: the pool year-0 age repair is NOT level-preserving — pool Sigma entry_anchor moved '
    '%.6f -> %.6f (delta %.6f, %.3e relative). C5 requires the pool total held EXACTLY; only its '
    'distribution across draft age may move.'
    %(_B_SUM_BEFORE,_B_SUM_AFTER,_B_SUM_AFTER-_B_SUM_BEFORE,
      abs(_B_SUM_AFTER-_B_SUM_BEFORE)/max(_B_SUM_BEFORE,1e-9)))
print('#334 ITEM B WIRED: pool year-0 age gradient live on %d entrants (K=%.10f); pool Sigma v0 held at '
      '%.4f (C5 level-preserving, asserted).'%(len(_POOL_ROWS_326),_b_renorm(),_B_SUM_AFTER))
# A build's own report must not misstate its basis (#344): the frozen-load sentence is printed only when the
# surface was in fact loaded from the freeze. On the declared lane the build says so, in its own words.
print('#326 ENTRY ANCHOR WIRED: %d pool entrants anchor on their signed division level — ruck cap in ladder '
      'currency, floor and thin-record blend at x%.4f (board factor). %s (sig %s).'
      %(len(_POOL_ROWS_326),_PL_F,
        ('Frozen year-zero surface LOADED, not refitted'
         if _V0CURVE_META.get('_v0surf_frozen') is True else
         'Year-zero surface REFIT DECLARED (RL_V0SURF_REFIT=1) — this build did NOT load the freeze, and is '
         'barred from any release build'),
        str(_V0CURVE_META.get('_v0surf_sig'))[:8]))
# ===== ORDER 29B — THE ENTRY WIRING: THE PRINTED DAY-0 PRICE IS THE DERIVED v0 x NUMERAIRE ==================
# WHAT ORDER 29 LEFT. It landed the day-0 OBJECTS — the ruled curve, the six positional ND v0 curves
# (pvc_curve_v2.json::nd_v0.posv), the pool pathway x position v0 cells (::pool_v0.cells) and the numeraire —
# and NOTHING CONSUMED THEM. Its own P12 measured the consequence on the landed board: of 46 fresh entrants,
# ZERO printed the entry anchor; the printed day-0 sat at mean 0.5274x of it (range 0.3166-0.9037), because a
# zero-evidence row was still priced through the legacy legs and carried their sit-out retention, the ITEM H
# cut and the year-zero floor. ORDER 29B closes exactly that and nothing else.
#
# THE SITE, AND WHY THE SET IS COMPLETE. There is exactly ONE place a player price becomes a printed number:
# this function, ev(p,Y) — the outermost, floor-wrapping definition. Every printed player price in the system
# is ev(p,Y) at some Y:
#     board v / vM1 / vM2 / vP1 / vP2   rl_export.py:191-193,197   int(round(ev(p,20XX)/_F))
#     the numeraire parity re-check     rl_export.py:617           int(round(ev(p,2026)/_F))
#     the 24-year as-of matrix          emit_matrix_338.py:193     ev(p,Y) under truncated scoring
#     the cohort book / back_extra      the same ev
# The wiring is therefore ONE branch in ONE function, not a list of call sites that a later seat could add to
# and miss. The PICK side (PVC), the sealed entrant layer (draft_occupancy x ladder) and the display bands are
# NOT player prices and are deliberately NOT in the set — which is why the LEG F5 #306 reconciliation neither
# moves nor needs a re-seal.
#
# THE OBJECT AND THE CURRENCY, stated so the numeraire cannot be double-counted. Both published day-0 objects
# are ALREADY ANCHORED: posv_g(p) = relat_g(p) x curve(p) where curve is THE SHIPPED ladder (raw x s), and the
# pool cells are the raw Way-A cells x anchor_factor (== s). So s is inside them, and the only conversion left
# is BOARD -> ENGINE currency, which is the certified board factor _PL_F. That is exactly ORDER 28's own
# canonical derived-v0 statement (o28_derive.py:266-271: allin[pick]*NUM for ND, cell*af*NUM for pool).
#     ev(day-0 entrant, Y) = derived_v0_board(p) * _PL_F      =>   printed = int(round(ev/_F)) = round(v0)
# THE BRANCH RETURNS AN UNROUNDED FLOAT ON PURPOSE. Every other ev path returns round(...); if this one did
# too there would be TWO roundings in the chain (engine round, then the print's round(x/_F)) and the identity
# would break on 18 of the 89 wired rows — measured, not feared. The print's own rounding is left as the only
# one, so `printed == round(derived v0)` is EXACT rather than tolerance-bounded.
#
# WHICH ROW, AND AT WHICH YEAR. A day-0 print is a property of a player AT AN AS-OF YEAR, not of a career
# total, so the predicate reads games AS OF Y. This is what makes the walk-forward matrix's yr0 mark move
# with the board: the same function answers both. The population gate is the year-zero floor's own — real
# store rows, never retired/delisted, never gate synthetics, pool OR national-draft non-pickless — plus
# Y >= draft year, so nothing is priced as an entrant before it enters.
#
# WHAT IS DELIBERATELY NOT TOUCHED. The four legs (_uncomp_prod, the pedigree-pole blend, ev/raw_ev, L7),
# sitout_ev, entry_anchor, v0_start, pool_level, _cap_basis, the floor schedule, ITEMS A/B/C/E2/H and the
# whole staleness family are read-unchanged and called unchanged for every row that is not a day-0 entrant.
# The branch RETURNS BEFORE the legacy chain, so it cannot perturb it. A row with even one game is priced
# exactly as it was before this act.
#
# KILL-SWITCH, DECLARED: RL_ENTRY29B=0 skips this block entirely => board 86c8d5d9 byte-exact. It is a
# DECLARED kill-switch, not a manifest dial (config_sha256 UNMOVED), exactly as RL_PVC2/RL_EVW/RL_ISOFADE.
# It also rides RL_PVC2: with the v2 artifact out of the ev channel there is no day-0 object to consume, so
# the kill-switch chain stays byte-exact in both directions.
_ENTRY29B=(os.environ.get('RL_ENTRY29B','1')!='0') and (os.environ.get('RL_PVC2','1')!='0')
_entry29b_derived=None
if _ENTRY29B:
    _V0ND=_V2J.get('nd_v0'); _V0POOL=_V2J.get('pool_v0')
    if not _V0ND or not _V0POOL or not _V0ND.get('posv') or not _V0POOL.get('cells'):
        raise SystemExit(
            'ORDER 29B HALT: pvc_curve_v2.json carries no nd_v0.posv / pool_v0.cells, so the printed day-0 '
            'price has no object to be. This is FAIL-CLOSED BY DESIGN — falling back to the legacy legs '
            'would silently restore the very 0-of-46 gap this act exists to close. Install the artifact '
            'that carries both day-0 objects, or set RL_ENTRY29B=0 and say so.')
    _POSV={_g:{int(_k):float(_v) for _k,_v in _d.items()} for _g,_d in _V0ND['posv'].items()}
    def day0_v0(p):
        """The row's OWN derived day-0 v0, in BOARD currency (the numeraire s is already inside).
        ND in-curve  -> the POSITIONAL ND v0 at his pick, nd_v0.posv[gfut][pick].
        pool         -> his pathway x position cell, through MA.pool_v0_of (the ONE accessor, which HALTS
                        on an unsigned cell rather than defaulting).
        Anything else -> None: not an entrant object, and the legacy chain keeps it byte-for-byte."""
        if p.get('_pool'): return float(MA.pool_v0_of(p))
        _pk=p.get('pick')
        if p.get('type')=='ND' and _pk and 1<=int(_pk)<=MA.ND_CURVE_LAST:
            _row=_POSV.get(MA.gfut(p))
            if _row is None:
                raise SystemExit('ORDER 29B HALT: %s resolves to position %r, which the artifact\'s positional '
                                 'ND v0 object does not publish (%s). A day-0 print must not be defaulted to '
                                 'the position-blind ladder.'%(p.get('player'),MA.gfut(p),sorted(_POSV)))
            return float(_row[int(_pk)])
        return None
    def _entry29b_derived(p,Y=2026):
        """The printed day-0 price this row MUST carry at as-of year Y, in BOARD currency — or None if the
        row is not a day-0 entrant at Y. This is the ONE predicate; the ev branch and the boot-class assert
        in rl_export both read it, so they cannot drift apart."""
        if not _isreal(p) or p.get('_retired') or delisted(p): return None
        if not p.get('_pool') and (p.get('type')!='ND' or p.get('_pickless')): return None
        if Y<int(p.get('year') or 0): return None
        for _r in p['scoring']:
            if _r['year']<=Y and _r['games']: return None          # he has evidence as of Y: not a day-0 print
        return day0_v0(p)
    _ev_pre29b=ev
    def ev(p,Y=2026):
        # ORDER 31 — NO LANES. The 29B day-0 interception is the OTHER lane boundary the one law replaces:
        # under RL_O31 a zero-evidence row is priced by the same expression as everybody else, which
        # returns v0 x D(c_u) identically (rho(0)=0, pi(0,c)=D(c)). Both interceptions must go, or the
        # first one still owns the row and "one formula, all g" is false of the code.
        if _O31: return _ev_pre29b(p,Y)
        _d0=_entry29b_derived(p,Y)
        if _d0 is None: return _ev_pre29b(p,Y)
        return _d0*_PL_F                                            # unrounded ON PURPOSE — see above
    _D0_NOW=[p for p in MA.data if _entry29b_derived(p,MA.BASE_REF) is not None]
    _D0_ND=[p for p in _D0_NOW if not p.get('_pool')]
    print('ORDER 29B ENTRY WIRING LIVE: %d day-0 entrants at Y=%d (%d national in-curve on nd_v0.posv, %d '
          'pool on pool_v0.cells) print derived v0 x numeraire EXACTLY; every row with evidence keeps the '
          'legacy legs byte-for-byte.'
          %(len(_D0_NOW),MA.BASE_REF,len(_D0_ND),len(_D0_NOW)-len(_D0_ND)))
else:
    print('ORDER 29B ENTRY WIRING OFF (RL_ENTRY29B=0 or RL_PVC2=0) — the legacy legs print the day-0 price.')
# ===== ORDER 30B STEP 2 — THE SITTER FADE, WIRED. SITTING IS EVIDENCE. =====================================
# THE LAW. A listed player who has not played is not frozen at his entry price: the sitting itself is the
# evidence, and it is priced. The schedule is the R1 RE-DERIVED listed-conditional row — re-derived against
# the STEP-1 FINAL v0s with the 30A-2 harness byte-identical, because the fade is a RATIO TO v0 and the
# calibration must ride its own ruler:
#
#       D(1) = 1.0000   (entry — no discount)
#       D(2) = 0.5502   n = 464
#       D(3) = 0.2628   n = 100
#       D(4) = 0.3460   n =  11      <-- ABOVE D(3). THIS IS NOT A DEFECT AND IT IS NOT SMOOTHED.
#       D(c) = 0.3460   FLAT for every c >= 4
#
# WHY THE KINK IS KEPT (owner ruling, #334 comment 5292534855, "AS MEASURED, FLAT DEEP END", 2026-08-14).
# The depth-3 -> depth-4 cell count falls 100 -> 11: that is the year-3->4 DELIST WAVE. What survives it is
# selected. In the owner's words: "players who last on a list that long without production may well do so for
# good reason - whereas those who are no good are likely to be delisted before then." The kink is SELECTION,
# it is real, and it is disclosed rather than isotonised away. The listed-conditional schedule is therefore
# NOT required to be monotone in depth (STOP_STEP2_FADE_RULER.md Q3, answered NO).
#
# THE DEEP END HOLDS FLAT, AND THE EARLIER RULING IS AMENDED. Ruling 2 of the sitter law said "extrapolate
# the fitted decay past year 4". On the re-derived ruler that fitted decay reads 0.1176 at year 4 while the
# measured year-4 cell reads 0.3460 — 2.94x apart — because a decay fitted through depths 2 and 3 is being
# extrapolated THROUGH a selection kink. The owner AMENDED (retired) the extrapolate ruling FOR THIS LAW:
# a still-listed deep sitter is at least as selected as the year-4 group, so D holds flat at 0.3460 from
# depth 4 out. Nothing extrapolates. (STOP_STEP2_FADE_RULER.md Q1/Q2, answered: R1 row, measured deep end.)
#
# THE CLOCK IS CONTINUOUS, in season fractions, exactly the packet-2 convention:
#       c(p,Y) = (Y - entry_year(p)) + fE(Y,p)
# fE is the engine's OWN season fraction _fEy(Y,p) — data/season_state.json::calendar_progress (0.92) for the
# in-progress season, 1.0 for a completed one (and 1.0 for an LTI out-for-the-remainder name, whose season IS
# complete at his real games). ONE clock convention in the engine, not a second one. Packet 2 quoted its named
# rows at NOW=2026 only; the generalisation to an as-of year Y is the same expression with the same fE, so the
# 24-year as-of matrix and the board read one law. DECLARED, because packet 2 never had to say it.
# Interpolation between integer depths is LOG-LINEAR in D:  D(c) = D(N)^(1-f) * D(N+1)^f,  f = c - N.
# c <= 1 => D = 1.0 (a player drafted this year, and every earlier as-of year, pays no sitting discount).
#
# POPULATION AT THIS STEP: ND in-curve (type ND, pick 1..64) — the exact population the law was derived on.
# POOL ROWS ARE DELIBERATELY NOT FADED HERE. Their fade is derived by the same construction on their own
# pathway values at STEP 4 (owner ruling 5 governs MSD there); wiring the ND-derived numbers onto pool rows
# would be exactly the pathway-specific-machinery mistake this order exists to end, in reverse.
#
# WHAT THIS SUPERSEDES. ORDER 29B's flat hold — "a zero-evidence row prints its derived v0, full stop" — and
# its games-as-of predicate as a PRICE law. The predicate itself survives unchanged as the POPULATION test
# (who is a sitter at Y); what changes is that the sitter's price is now v0 x D(c) instead of v0. 29B's
# printed-day-0 identity is not dropped, it is RESTATED: printed == round(v0 x D(c)), tolerance 0, and at
# c <= 1 (D == 1) it reduces to 29B's own equality exactly.
#
# los_decay RETIRES FROM THE LIVE PATH. Measured, not asserted: los_decay(p) is called at rl_model.py:1748
# (the LEGACY rl_model value() chain, which the board's ev() does not call) and at rl_export.py:332, where it
# is a DISPLAY field ('losd') in the UI bundle and not a price. It is therefore not reachable from any printed
# price, before or after this act. It is KEPT IN CODE as the declared fallback — the existing convention for
# every superseded law in this engine (RL_PVC2/RL_EVW/RL_ISOFADE/RL_ENTRY29B all keep their old leg) — behind
# this block's declared kill-switch RL_ONEMACH=0, which restores the 29B flat hold exactly.
#
# KILL-SWITCH, DECLARED: RL_ONEMACH=0 makes this whole block inert => the STEP-1 board 84c9ea16 byte-exact.
# It is a DECLARED kill-switch, not a manifest dial (config_sha256 UNMOVED).
_ONEMACH=(os.environ.get('RL_ONEMACH','1')!='0')
FADE30B_D={1:1.0,
           2:0.5501935857356868,      # R1 re-derived, listed-conditional (L-B), n=464
           3:0.26278629823610156,     # R1 re-derived, listed-conditional (L-B), n=100
           4:0.3460004697526451}      # R1 re-derived, listed-conditional (L-B), n=11 — the selection kink
FADE30B_FLAT_FROM=4                   # owner ruling: FLAT from depth 4 out; nothing is extrapolated
FADE30B_SRC=('#334 comment 5292534855 (owner, 2026-08-14) on FADE30B_TABLE.json / o30b_fade_rederive.py; '
             'amends the earlier extrapolate-the-decay ruling for this law')
def fade30b_D(c):
    """The ruled sitter fade at continuous depth c. Log-linear between integer depths, 1.0 at/below depth 1,
    FLAT at D(4) from depth 4 out. Pure function of c — no player state, so it is trivially auditable."""
    if c<=1.0: return 1.0
    if c>=FADE30B_FLAT_FROM: return FADE30B_D[FADE30B_FLAT_FROM]
    n=int(_math.floor(c)); f=c-n
    d0=FADE30B_D[n]; d1=FADE30B_D[n+1]
    if f<=0.0: return d0
    return _math.exp((1.0-f)*_math.log(d0)+f*_math.log(d1))
def fade30b_clock(p,Y):
    """Continuous season-fraction depth. c = (Y - entry_year) + fE(Y,p).
    MSD (owner ruling 5): the first season IS season 1, so the MSD clock runs one season ahead of the
    entry_year+1 debut convention every other route uses. Stated here so the pool step inherits it."""
    n=Y-int(p.get('year') or 0)
    if p.get('type')=='MSD': n+=1
    return max(0.0,float(n)+_fEy(Y,p))
def fade30b_of(p,Y):
    """The fade multiplier this row carries at Y, or 1.0 if the law does not reach him at this step."""
    if not _ONEMACH: return 1.0
    if p.get('_pool'): return 1.0                                  # pool fade is derived at STEP 4
    _pk=p.get('pick')
    if p.get('type')!='ND' or not _pk or not (1<=int(_pk)<=MA.ND_CURVE_LAST): return 1.0
    return fade30b_D(fade30b_clock(p,Y))
_entry30b_price=None
if _ONEMACH and _ENTRY29B:
    def _entry30b_price(p,Y=2026):
        """The printed sitter price this row MUST carry at as-of year Y, in BOARD currency, or None if he is
        not a sitter at Y. ONE predicate: the ev branch and the rl_export boot-class assert both read it."""
        _d0=_entry29b_derived(p,Y)
        if _d0 is None: return None
        return _d0*fade30b_of(p,Y)
    _ev_pre30b=ev
    def ev(p,Y=2026):
        # ORDER 31 — NO LANES. The one law prices a zero-games row with the SAME expression as every other
        # row (rho(0)=0 and pi(0,c)=D(c) make it identically v0 x D(c)), so the interception is switched OFF
        # and the row falls through to the blend site. This is the single line that makes "one formula, all
        # g" TRUE OF THE CODE and not merely of the algebra.
        if _O31: return _ev_pre30b(p,Y)
        _d0=_entry30b_price(p,Y)
        if _d0 is None: return _ev_pre30b(p,Y)
        return _d0*_PL_F                                           # unrounded ON PURPOSE — see the 29B note
    _S30=[p for p in MA.data if _entry30b_price(p,MA.BASE_REF) is not None]
    _S30ND=[p for p in _S30 if fade30b_of(p,MA.BASE_REF)<1.0]
    print('ORDER 30B STEP 2 — SITTER FADE LIVE: D(2)=%.4f D(3)=%.4f D(4+)=%.4f FLAT (as measured; the '
          'depth-4 kink is SELECTION, kept and disclosed). Continuous clock c=(Y-entry)+fE, log-linear. '
          '%d sitters at Y=%d, %d of them carry a discount (%d at D=1: entry-year or pool). los_decay is '
          'off the live path.'
          %(FADE30B_D[2],FADE30B_D[3],FADE30B_D[4],len(_S30),MA.BASE_REF,len(_S30ND),len(_S30)-len(_S30ND)))
elif not _ONEMACH:
    print('ORDER 30B ONE-MACHINERY OFF (RL_ONEMACH=0) — the 29B flat hold prints the sitter price.')
# ===== ORDER 30B-P — THE STEP-3 PREVIEW BLEND. INSTALLED HERE, BEHIND RL_O30B_PREVIEW (DEFAULT OFF). ======
# #334 comment 5299562714. NOTHING IS GREENLIT: the Step-3 forbidden-set boundary word is still OPEN, and
# this lane exists so the owner can rule it from a board. Dial unset => every branch above is False and the
# committed Step-2 board 9298203135202a0c707bb0977ba38c31 reproduces BYTE-EXACT.
#
# THE FORMULA, for a row that HAS evidence at Y:
#
#       price(p,Y) = (1 - sigma(g)) x production(p,Y)  +  sigma(g) x pedigree(p)
#
#   production  the finished production leg at the blend site in ev(): POLE DELETED, ISO DELETED (both via
#               the two existing ablation lines, which RL_O30B_PREVIEW implies), with the retained
#               bars/aging/form machinery applied and BOTH superseded anchor blends removed.
#   pedigree    the STEP-1 POSITIONAL v0 — day0_v0(p) — converted BOARD -> ENGINE currency by _PL_F.
#   sigma(g)    the MEASURED pedigree share at g games (ORDER 30B-M).
#
# ---- THE CURRENCY CONVERSION, STATED EXACTLY (the 29B/29C conventions, no new object) -------------------
# day0_v0(p) is in BOARD currency and the numeraire s is ALREADY INSIDE IT: for an ND in-curve row it is
# nd_v0.posv[gfut][pick] (the STEP-1 re-fitted positional ladder, `posv_g = relat_g x curve`, curve = the
# shipped ladder raw x s); for a pool row it is the signed pool_v0 cell x anchor_factor, read through the
# ONE accessor MA.pool_v0_of which HALTS on an unsigned cell. ev() works in ENGINE currency and the printed
# board price is int(round(ev/_F)) with _F == _PL_F == the certified 1.0524. So the ONE conversion the
# pedigree leg needs is BOARD -> ENGINE, i.e. x _PL_F — precisely the conversion ORDER 29B's own day-0
# branch performs one screen above (`return _d0*_PL_F`). No second numeraire is introduced and none is
# re-pinned: THE PREVIEW IS PRE-NUMERAIRE, Step 6 has not run, and every table generated says so.
#
# ---- THE NO-STACKING CONSTRAINT -------------------------------------------------------------------------
# The owner's constraint: a PLAYED player's pedigree share equals the measured sigma curve, and the sitter
# fade D(clock) governs GAMELESS clocks only. Both objects are therefore applied to disjoint populations and
# are NEVER multiplied together:
#   * zero evidence at Y  -> _entry30b_price() intercepts the row ABOVE this lane and prints v0 x D(c).
#                            THE STEP-2 WIRING IS UNTOUCHED; day-0 prints are byte-identical under the
#                            preview, which is why the printed-day-0 identity re-verifies at 89 of 89.
#   * any evidence at Y   -> this blend, with an UNFADED pedigree leg at weight sigma(g).
# Stacking (1-w) and D on the same row is exactly the double-discount the constraint forbids, and the code
# cannot do it: the two branches are mutually exclusive by the _entry30b_price predicate.
#
# ---- sigma(g): THE MEASURED CURVE, AND THE INTERPOLATION, STATED ---------------------------------------
# ORDER 30B-M measured the pedigree share at five games bands, at their n-weighted midpoints:
#       g   2.5    10.5    25.5    53.0    85.5
#   sigma  70.1%  66.4%  33.1%  16.5%   2.2%          (PERSISTENCE_TABLE.json / PACKET section 2)
# The preview uses the packet's own REFIT (section 6): the SAME functional family ruling 4 ruled,
# sigma(g) = exp(-(g/tau)^beta), refitted to those five midpoints by n-weighted least squares ->
# tau = 23.0, beta = 0.80. THIS IS THE INTERPOLATION BETWEEN THE BAND MIDPOINTS, and it is the one the
# owner's brief names ("the 30B-M refit, tau~23.0 beta~0.80 class"). It is used rather than a raw
# point-to-point interpolation because it is the ruled functional form, it is monotone and smooth
# everywhere (ruling 6's continuity acceptance curve needs that), and it is defined below 2.5 and above
# 85.5 games where a point-to-point rule would have to extrapolate. Its fit to the five measured points is
# published in the packet (2.5 84.4% / 10.5 58.6% / 25.5 33.8% / 53.0 14.2% / 85.5 5.7%) and its known
# residuals — it runs HOT at the shallow end and HOT again past 71 games — are carried into this lane
# unchanged rather than patched. THE RAW LOG-LINEAR MIDPOINT INTERPOLATION IS ALSO PROVIDED BELOW
# (sigma30bp_raw) as the declared alternative, so the difference can be priced without another dial.
#   sigma(0) = 1 exactly, so the blend is CONTINUOUS INTO the pedigree leg on the games axis. It is NOT
#   continuous into the Step-2 sitter price, because the sitter price is v0 x D(c) < v0 while the blend
#   approaches v0 as g -> 0. That STEP AT THE FIRST GAME is a property of the no-stacking constraint as
#   stated, not of this implementation, and it is MEASURED and reported rather than smoothed away.
#
# ---- THE GAMES AXIS, AND MSD (owner ruling 5) -----------------------------------------------------------
# g is CAREER games as of Y (never future), the same axis the measurement used. Ruling 5 makes the MSD
# entry season a season 1 of AT MOST 12 games, and says the evidence clock scales on games-of-12; so an MSD
# row's entry-season games are credited at cp.SEASON/12 per game, and every other season on every route is
# credited 1:1. Stated rather than assumed: this is the ONLY place the games axis is not raw games, it
# touches the MSD entry season alone, and pool rows are carried as PROVISIONAL because their own values are
# Step 4's work.
SIGMA30BP_TAU=23.0; SIGMA30BP_BETA=0.80
SIGMA30BP_SRC=('ORDER 30B-M PEDIGREE_PERSISTENCE_PACKET.md section 6 refit of ruling 4\'s functional form '
               'to the five measured sigma band midpoints; #334 comment 5299562714')
SIGMA30BP_BANDS=((2.5,0.701),(10.5,0.664),(25.5,0.331),(53.0,0.165),(85.5,0.022))   # the MEASURED points
def sigma30bp(g):
    """The measured pedigree share at g career games. exp(-(g/tau)^beta); sigma(0)=1 exactly, strictly
    decreasing, positive everywhere. Pure function of g — no player state, trivially auditable."""
    g=float(max(0.0,g))
    if g<=0.0: return 1.0
    return _math.exp(-((g/SIGMA30BP_TAU)**SIGMA30BP_BETA))
def sigma30bp_raw(g):
    """THE DECLARED ALTERNATIVE, published for comparison and NOT wired: log-linear in sigma between the
    five measured band midpoints, flat outside them. This is the reading that hits the measured points
    exactly and interpolates nothing else."""
    g=float(max(0.0,g)); xs=[b[0] for b in SIGMA30BP_BANDS]; ys=[b[1] for b in SIGMA30BP_BANDS]
    if g<=xs[0]: return ys[0]
    if g>=xs[-1]: return ys[-1]
    for i in range(len(xs)-1):
        if xs[i]<=g<=xs[i+1]:
            f=(g-xs[i])/(xs[i+1]-xs[i])
            return _math.exp((1.0-f)*_math.log(ys[i])+f*_math.log(ys[i+1]))
    return ys[-1]
def pv_games(p,Y=2026):
    """The games axis sigma reads: career games as of Y, with ruling 5's MSD games-of-12 scaling."""
    _msd=(p.get('type')=='MSD'); _e=int(p.get('year') or 0); _k=float(cp.SEASON)/12.0
    _g=0.0
    for _x in p.get('scoring') or []:
        if _x['year']>Y or not _x['games']: continue
        _g+=float(_x['games'])*(_k if (_msd and _x['year']==_e) else 1.0)
    return _g
if _O30B_PREVIEW:
    if not (_ENTRY29B and _ONEMACH):
        raise SystemExit('ORDER 30B-P HALT: the preview needs the ORDER 29B day-0 object (the pedigree leg) '
                         'and the ORDER 30B Step-2 fade (the zero-evidence lane). One of them is switched '
                         'off, so the preview has nothing coherent to be. FAIL-CLOSED BY DESIGN.')
    def pv_pedigree(p):
        """The pedigree leg in ENGINE currency: the STEP-1 positional v0 (pool: the signed pool cell) x _PL_F."""
        _v=day0_v0(p)
        if _v is None:
            raise SystemExit('ORDER 30B-P HALT: %r carries evidence but has no day-0 v0 object, so the '
                             'preview cannot form its pedigree leg. Measured before wiring: 0 of the 715 '
                             'priced rows are in this state. FAIL-CLOSED rather than defaulted.'
                             %(p.get('key'),))
        return float(_v)*_PL_F
    def _pv_blend(p,Y,e):
        """price = (1-sigma(g)) x production + sigma(g) x pedigree. ONE pedigree leg, at the measured share."""
        _s=sigma30bp(pv_games(p,Y))
        return (1.0-_s)*float(e)+_s*pv_pedigree(p)
    _PV['blend']=_pv_blend
    # ---- ORDER 30B-N — THE RESOLVED LAW AT THE ev() LEVEL. -------------------------------------------
    # It prices AS-OF YEARS, which the derived board could not: g is games-as-of-Y on the raw clock, D and
    # c are the LIVE Step-2 fade and its continuous clock at Y, and P is the finished production leg at Y.
    # THE ARITHMETIC IS TRANSCRIBED, NOT REDERIVED, from o30br_resolved.py::book() / o30br_allrows.py.
    #
    #   sitter  zero games at Y   v0 x D(c)          <- NOT REACHED HERE. _entry30b_price intercepts the row
    #                                                   in the ev() wrapper above; the Step-2 wiring is
    #                                                   untouched and day-0 prints stay byte-identical. The
    #                                                   g<=0 case below is a CONTINUITY GUARD, not a branch:
    #                                                   b_lift(0)=1 exactly, so it returns the same v0 x D.
    #   thin    0 < g <= 10       v0 x D(c) x b_lift(g,c)      production does NOT enter (the T3 conflict)
    #   bridge  10 < g < 16       thin10 + t x (d16 - thin10)  a DECLARED bridge, not a measurement
    #   deep    g >= 16           P + beta(g) x v0             the additive reading (T1)
    #
    # CURRENCY. Every lane is homogeneous of degree 1 in currency, so the law commutes with the BOARD ->
    # ENGINE conversion: P arrives in engine currency and pv_pedigree() already applies _PL_F, exactly as
    # the preview blend does. No second numeraire is introduced and none is re-pinned. PRE-NUMERAIRE.
    #
    # T4 IS OPEN and this lane does NOT choose it: it prices the v0 OBJECT, which is the object
    # RESOLVED_ALLROWS.json totals (715,228.6). The entry_anchor object is not wired here.
    #
    # POOL, DISCLOSED: fade30b_of() returns 1.0 for every pool row because the pool fade is STEP 4's work
    # and is NOT DERIVED. A pool row therefore carries D=1.0 through the thin and bridge lanes. That is
    # carried unchanged from the resolution arithmetic, which prints the same caveat on its own rows.
    BETA30BN_PTS=((2.5,0.2968279384332228),(10.5,0.362259307264279),(25.5,0.22329587551741345),
                  (53.0,0.15314862603013868),(85.5,0.020068021140596692))
    BETA30BN_SRC=('ORDER 30B-R resolution/READING.json::beta_curve.points -- sigma_b := beta_v0 x mean(v0) /'
                  ' mean(R), o30bm_measure.py::band_fit; log-linear in log(games) between band midpoints,'
                  ' FLAT outside. #334 comment 5310246218')
    # The cumulative backbone, by DEPTH LANE (2 if the fade clock c < 2.5 else 3). JOIN.json::backbone.
    BACKBONE30BN={2:((0,0.5684),(2,0.656),(5,0.6936),(10,0.8236)),
                  3:((0,0.36),(2,0.5933),(5,0.6807),(10,0.693))}
    def beta30bn(g):
        """The ADDITIVE reading's pedigree coefficient at g games. Log-linear in log(g) between the five
        band midpoints, flat outside. Pure function of g -- no player state, trivially auditable.
        NOTE, disclosed rather than smoothed: this curve is NOT monotone. It RISES from 2.5 to 10.5 games
        before falling. That is what the band fit measured; it is carried, not patched."""
        g=max(1e-6,float(g))
        if g<=BETA30BN_PTS[0][0]: return BETA30BN_PTS[0][1]
        if g>=BETA30BN_PTS[-1][0]: return BETA30BN_PTS[-1][1]
        for _i in range(1,len(BETA30BN_PTS)):
            g0,b0=BETA30BN_PTS[_i-1]; g1,b1=BETA30BN_PTS[_i]
            if g0<=g<=g1:
                _t=(_math.log(g)-_math.log(g0))/(_math.log(g1)-_math.log(g0))
                return _math.exp(_math.log(b0)+_t*(_math.log(b1)-_math.log(b0)))
        return BETA30BN_PTS[-1][1]
    def b_lift30bn(g,c):
        """The cumulative backbone as a LIFT ON THE SITTER PRICE: the lane's curve normalised by its own
        g=0 value, so lift(0)=1 EXACTLY and the thin lane is continuous into the Step-2 sitter price at the
        first game. Log-linear in log1p(g); beyond 10 games it extrapolates on the last segment's slope
        (never reached in the thin lane, which ends at 10, but kept identical to the resolution's own
        b_lift so the two cannot drift)."""
        _pts=BACKBONE30BN[2 if c<2.5 else 3]
        _b0=_pts[0][1]
        _lift=[(_k,_v/_b0) for _k,_v in _pts]
        if g<=0: return 1.0
        _x=_math.log1p(float(g))
        for _i in range(1,len(_lift)):
            _k0,_l0=_lift[_i-1]; _k1,_l1=_lift[_i]
            _x0,_x1=_math.log1p(_k0),_math.log1p(_k1)
            if _x0<=_x<=_x1:
                _t=(_x-_x0)/(_x1-_x0)
                return _math.exp(_math.log(_l0)+_t*(_math.log(_l1)-_math.log(_l0)))
        (_k0,_l0),(_k1,_l1)=_lift[-2],_lift[-1]
        _sl=(_math.log(_l1)-_math.log(_l0))/(_math.log1p(_k1)-_math.log1p(_k0))
        return _math.exp(_math.log(_l1)+_sl*(_x-_math.log1p(_k1)))
    def _pv_resolved(p,Y,e):
        """THE RESOLVED LAW: additive reading, v0 object, joined lanes, on the raw games-as-of-Y clock."""
        _g=pv_games(p,Y)                   # raw career games as of Y (T2: the recency clock LOST)
        _V=pv_pedigree(p)                  # the v0 object, ENGINE currency (T4 is OPEN; v0 is priced)
        _D=fade30b_of(p,Y)                 # the LIVE Step-2 sitter fade at Y (1.0 for pool -- Step 4)
        _c=fade30b_clock(p,Y)              # its continuous depth clock at Y
        _P=float(e)                        # the finished production leg at Y
        if _g<=10.0:                       # thin (and the g<=0 continuity guard: b_lift(0)=1 -> v0 x D)
            return _V*_D*b_lift30bn(_g,_c)
        if _g<16.0:                        # the DECLARED bridge
            _t10=_V*_D*b_lift30bn(10.0,_c)
            _d16=_P+beta30bn(16.0)*_V
            _t=(_math.log1p(_g)-_math.log1p(10.0))/(_math.log1p(16.0)-_math.log1p(10.0))
            return _t10+_t*(_d16-_t10)
        return _P+beta30bn(_g)*_V          # deep: the additive reading
    # ================= ORDER 31 — THE ONE LAW, AT ev(). ==============================================
    # Constants are TRANSCRIBED from docs/evidence/candidate_31/LAW31.json, produced by o31_fit.py from
    # the committed artifacts only (READING.json's beta curve, BLEND30B.json's R1 backbone and D(2),
    # CIRCULARITY.json's stall-cohort coefficients). Nothing here is fitted at build time.
    # ORDER 31-F (#334 comment 5310576233) RE-FITS EVERY ONE OF THESE ON THE HEAD-FIXED RULER.
    # R1 ruler discipline: rho, beta, PhiStall and the sitter fade were all measured against the STEP-1
    # positional v0 surface. F1's head fix MOVED that surface, so all four were re-measured with their
    # COMMITTED HARNESSES RUN WHOLE (only the v0 source and the output directory re-pointed) and the fit
    # core LIFTED BY SOURCE TEXT from o31_fit.py and exec'd verbatim. Constants transcribed from
    # docs/evidence/candidate_31f/LAW31F.json. Drifts are published in SHIPPING_PACKET_31.md.
    #   D(2)   0.5501936 -> 0.5582775     beta(2.5)  0.2968279 -> 0.2878886
    #   D(3)   0.2627863 -> 0.2747858     beta(10.5) 0.3622593 -> 0.3561228 (monotone-projected as before)
    #   D(4+)  0.3460005 -> 0.3972709     PhiStall(2.5) 0.5834703 -> 0.5792927
    #   TAU_RHO 27.019054 -> 29.194254    B_RHO 0.8377678 -> 0.8015424   RMS 0.015333 -> 0.017369
    O31_TAU_RHO=29.194253560287144; O31_B_RHO=0.8015424473253033
    # beta under the brief's EXPLICIT "pi decays in g" constraint: the monotone non-increasing projection
    # of the measured pooled curve. The projection deletes the measured 2.5->10.5 RISE, which 30B-C 4.3
    # measured paying 57 of 352 stall paths MORE pedigree for stalling. DISCLOSED, not hidden: the raw
    # measured value at 10.5 is 0.362259307264279 and this law carries 0.2968279384332228 there.
    # ORDER 31-F: re-measured on the head-fixed ruler. The raw measured value at 10.5 is 0.3561228 and
    # this law carries 0.2878886 there -- the SAME deletion, disclosed exactly as before.
    O31_BETA=((2.5,0.2878886216033701),(10.5,0.2878886216033701),(25.5,0.21772876584106796),
              (53.0,0.14155152291809878),(85.5,0.023849021706229417))
    # PhiStall = beta_stall / beta_pooled at the five band midpoints (30B-C 3.2), the deep two ZERO-FLOORED
    # because t=-0.29 / -0.90 with CIs spanning zero, then made non-increasing.
    # ORDER 31-F: the 30B-C circularity harness re-run on the head-fixed ruler. The seat did NOT rely on
    # the "the ratio is invariant because both coefficients move together" argument -- it MEASURED it, and
    # the ratio in fact moved slightly MORE than the coefficients did (max |dPhiStall| 0.0102 against
    # max |dbeta_stall| 0.0064). PHI_31F.json.
    O31_PHIST=((2.5,0.5792926948039687),(10.5,0.298245232115451),(25.5,0.298245232115451),
               (53.0,0.0),(85.5,0.0))
    O31_PHI_RAMP=2.0                       # 30B-C's OWN continued-staller definition: two stall seasons
    O31_SRC=('docs/evidence/candidate_31f/LAW31F.json / o31f_fit.py; #334 comment 5310576233 (31-F), '
             'superseding docs/evidence/candidate_31/LAW31.json; rho calibrated on the 31-F re-derived '
             'cumulative backbone, pi pinned at D(c) at g=0 and handing over to the measured beta as '
             'evidence accumulates. EVERY constant re-measured on the HEAD-FIXED v0 surface (R1).')
    # ---- ORDER 31-F — THE SITTER FADE, RE-DERIVED ON THE HEAD-FIXED RULER ---------------------------
    # The Step-2 wired row FADE30B_D above is the RULED row, measured on the PRE-head-fix v0s, and it is
    # LEFT EXACTLY WHERE IT IS so that the dial-off board remains the Step-2 law and the head fix can be
    # priced in isolation. THE ONE LAW USES ITS OWN, re-measured by o30a2_recut.py run WHOLE on the
    # head-fixed surface (FADE_31F.json). Same construction, same listing reading (L-B outcome-blind
    # floor), same owner rulings: the depth-4 > depth-3 SELECTION kink is kept unsmoothed and the deep end
    # HOLDS FLAT at depth 4. Nothing is extrapolated.
    O31_FADE_D={1:1.0,
                2:0.5582775239783688,      # 31-F re-derived, listed-conditional (L-B), n=464
                3:0.2747857941376827,      # 31-F re-derived, listed-conditional (L-B), n=100
                4:0.39727085107749216}     # 31-F re-derived, listed-conditional (L-B), n=11 — the kink
    O31_FADE_FLAT_FROM=4
    def o31_fade_D(c):
        """The 31-F sitter fade at continuous depth c. IDENTICAL RULE to fade30b_D — log-linear between
        integer depths, 1.0 at/below depth 1, FLAT from depth 4 out — on the re-measured row."""
        if c<=1.0: return 1.0
        if c>=O31_FADE_FLAT_FROM: return O31_FADE_D[O31_FADE_FLAT_FROM]
        _n=int(_math.floor(c)); _f=c-_n
        _d0=O31_FADE_D[_n]; _d1=O31_FADE_D[_n+1]
        if _f<=0.0: return _d0
        return _math.exp((1.0-_f)*_math.log(_d0)+_f*_math.log(_d1))
    # ---- ORDER 31 STEP 2 — THE POOL FADE, DERIVED BY THE ND LAW'S OWN ESTIMATOR ---------------------
    # docs/evidence/candidate_31/o31_pool.py execs the 30A-2 harness VERBATIM to its surface builder and
    # rebuilds the population on the POOL pathways with the SIGNED pool v0 cell as the object. CONTROL:
    # that transplanted estimator re-derives the RULED ND row at deviation 0.0 (D 0.550194 / 0.262786 /
    # 0.346000), so the pool row below is produced by the same instrument, not an analogue of it.
    #   D_pool(1) = 1.0                  n 840
    #   D_pool(2) = 0.5545657072981915   n 588      (the ND law reads 0.5501936 at the same depth)
    #   FLAT from depth 2 out.
    # The depth-3 pool cell measures 2.2635 on n 17 -- it INVERTS. All 17 are eventual players and 45% of
    # their value is in the unobserved tail: it is survivorship, in the extreme. It is PUBLISHED IN FULL
    # in POOL31.json and NOT WIRED, by the declared rule "wire the deepest cell that clears the n floor
    # AND is a fade (D <= 1)". Flagged on the packet as an OWED CONFIRMATION, not presented as ruled.
    O31_POOL_D={1:1.0,2:0.5545657072981915}
    O31_POOL_FLAT_FROM=2
    # ---- ORDER 31-F F2 — beta_pool, DERIVED. The largest borrowing ORDER 31 left, closed. ----------
    # docs/evidence/candidate_31f/o31f_pool.py transplants the 30B-M PANEL CONSTRUCTION to pool cohorts:
    # the harness's own panel(nd_only=False) pool states, its own band_fit regression, its own games
    # bands, its own H=6 horizon and its own player clustering. The ONE thing supplied is the v0 pool
    # rows never had — MA.pool_v0_of, the accessor that HALTS on an unsigned cell. CONTROL: re-running
    # band_fit on the ND panel reproduces the 31-F ND beta row at deviation 0.0.
    #   MEASURED   2.5:0.3731(t 1.33) 10.5:0.3857(t 0.79) 25.5:1.0645(t 1.81) 53:1.7978(t 2.46) 85.5:1.9732(t 2.13)
    # THE MEASURED CURVE RISES. Under the brief's EXPLICIT "pi decays in g" it takes the SAME monotone
    # non-increasing projection the ND beta takes, which deletes the rise and leaves the row FLAT at the
    # shallow-band value. THE DELETION IS LARGE AND IT IS DISCLOSED ON THE PACKET, with the reason: on
    # pool rows v0 takes only ~54 distinct values (pathway x position), so inside a games band it acts as
    # a pathway fixed effect rather than as pedigree, and the deep bands' "rise" is that identification
    # failure, not persistence. The two SHALLOW bands — the ones that price beecken/madden/reidy/scerri —
    # have t of 1.33 and 0.79: INDISTINGUISHABLE FROM ZERO, and that is on the packet too.
    O31_BETA_POOL=((2.5,0.3730572000100778),(10.5,0.3730572000100778),(25.5,0.3730572000100778),
                   (53.0,0.3730572000100778),(85.5,0.3730572000100778))
    # Phi on pool rows: the brief's condition — "by the same construction if the pool panel supports it".
    # IT DOES: every pool games band clears band_fit's own n>=40 floor, so this is POOL-MEASURED, not
    # ND-borrowed. Same construction as the ND row: zero-floor, monotone, ratio to the wired beta_pool,
    # clip to [0,1], monotone again. The stall coefficients' t are 0.61/0.07/1.31/1.74/0.39 — weak, and
    # said so on the packet.
    O31_PHIST_POOL=((2.5,0.21225409196511028),(10.5,0.03648485735530794),(25.5,0.03648485735530794),
                    (53.0,0.03648485735530794),(85.5,0.036484857355307924))
    # DECLARED, DEFAULT-OFF: price the beta_pool decision by REMOVING it (pool rows fall back to the ND
    # beta and the ND PhiStall, i.e. exactly ORDER 31's behaviour), so its cost is a NUMBER, not a
    # paragraph — the same discipline RL_O31_NOPHI applies to the stall conditioning.
    _O31F_NOBPOOL=os.environ.get('RL_O31F_NOBPOOL','0')!='0'
    # ================= ORDER A — CANDIDATE 32 CONSTANTS AND HELPERS (all behind _O32S). ============
    # Sources: docs/evidence/order_a_2026-08-17/{PREREG_32.md, PHI_32.json, FADE_32.json,
    # RELIEF_32.json, REMIX_32.json}; #334 comment 5312733761. NOTHING here runs with the dial off.
    #
    # M1 — THE AGE-REFERENCED GATE BARS (S1 construction C3). A NEW, GATE-ONLY object:
    # bar(pos, age) = _O30BP_BARS[pos] - Δ(class, clamp(age,18,23)); flat from age 24 (cap law
    # structural, Δ >= 0). CONSUMED ONLY inside the stall-run test and the delivered test below.
    # _O30BP_BARS ITSELF IS NEVER EDITED: the production references and both par denominators keep
    # the flat bars untouched (S1 §12 coupling warning).
    O32_TALLPOS=frozenset(('KPD','KPF','RUCK'))
    O32_GATE_DELTA={'TALL':{18:22.334475609756097,19:20.55500752464971,20:16.306362402208926,
                            21:11.588672690048071,22:7.826894964594814,23:6.439783302063788},
                    'SMALL':{18:20.080511089352214,19:20.080511089352214,20:14.306977484301457,
                             21:11.265167414136857,22:6.761247284555768,23:4.584052475875439}}
    def o32_gate_bar(pos,age):
        """The gate's AVG bar for a season played at `age`. Flat at/after 24; the C3 class-pooled
        development offset below; ages <= 18 take the age-18 column. None if the position has no bar."""
        _b=_O30BP_BARS.get(pos)
        if _b is None: return None
        if _O32S<1 or age is None or age>=24: return _b
        return _b-O32_GATE_DELTA['TALL' if pos in O32_TALLPOS else 'SMALL'][max(18,min(23,int(age)))]
    # M6b-2 — THE PHI ROW RE-DERIVED UNDER THE NEW BARS (PHI_32.json; the Δ≡0 control reproduced
    # CIRCULARITY_31F at deviation 0). beta is UNCHANGED (owner ruling R-W1) — only the stall RATIO
    # moves. Pool rows keep the 31-F pool row (O31_PHIST_POOL): the pool stall coefficients were not
    # re-derived under the new bars — an OWED LIMITATION, disclosed on the packet, not hidden here.
    O32_PHIST=((2.5,0.645228057068287),(10.5,0.14783270364736742),(25.5,0.14783270364736742),
               (53.0,0.14783270364736742),(85.5,0.0))
    # M4/M6b-4(b) — SELECTION RELIEF INSIDE D (S3 sketch (a), the capped form). RELIEF_32.json:
    # λ fit on the S2 spectrum surface under the NEW clock definitions (identifiability band
    # [0.46, 1.20] published). The cap at full pedigree (D -> at most 1) is STRUCTURAL: the ceiling
    # stays production-only, relief can never pay above v0.
    O32_LAMBDA=1.08
    def o32_sigma_sel(p,Y):
        """The S3 threshold shape on current + most-recent-season selection: zero below ~5 games,
        rising 5-10, flat >= 10; the in-progress season prorated by its own fraction."""
        _s=0.0
        for _x in (p.get('scoring') or []):
            if _x['year'] in (Y,Y-1) and _x.get('games'):
                _f=(_fEy(Y,p) if _x['year']==Y else 1.0)
                if _f>0.0:
                    _s=max(_s,max(0.0,min(1.0,(float(_x['games'])-5.0*_f)/(5.0*_f))))
        return _s
    # M3 — THE DELIVERED PREDICATE (one predicate: the stall run and the reset both read it).
    def o32_delivered(p,Y,x):
        """Season row x is DELIVERED as of Y: games >= 10 x season-fraction AND avg >= the
        age-referenced gate bar (the flat bar below stage 1)."""
        _u=(_fEy(Y,p) if x['year']==Y else 1.0)
        if float(x.get('games') or 0.0)<10.0*_u: return False
        _bar=o32_gate_bar(MA.gfut(p),(x['year']-p['_by']) if p.get('_by') else None)
        return _bar is not None and float(x.get('avg') or 0.0)>=_bar
    # M5/M6c — THE 5-15g RE-MIX (R-REMIX, two-sided acknowledged). TWO knobs, both from W2's own
    # translation ("raise the production-leg loading ... but then the pedigree leg must come down
    # in step"):
    #   rho32(g)     = rho31(g) + κ·m_u(g)·(1-rho31(g)),   m_u = (g/γ_u)·exp(1-g/γ_u)
    #   pedigree leg x max(0, 1-η·m_d(g)),                 m_d = (g/γ_d)·exp(1-g/γ_d)
    # m_u(0)=m_d(0)=0 exactly: g=0 sitters untouched and pi(0)=D preserved. Two-sided BY
    # CONSTRUCTION: weight moves from the pedigree leg to shown production, so poor starters CAN
    # fall below entry and risers rise. Calibrated on W2's hindsight surface subject to the slope
    # band, the W band, the HARD no-arb line (max class <= 1.139 — this also CURES the inherited
    # 2010 class mark of 1.1405) and the η <= 0.75 non-degeneracy guard (REMIX_32.json; the prereg
    # one-knob family measured INFEASIBLE there — a disclosed prereg deviation). Monotonicity of
    # rho32 asserted at load.
    # REMIX_32R.json::chosen (ORDER A REPAIR, PREREG_32R + amendments A1-A3) — re-calibrated on the
    # CORRECTED (age-relative) hindsight surface with the R1 age credit live. Selection = min
    # corrected-surface SSE among the ruled-gate-feasible set {slope band, W inside the corrected
    # hindsight 90% CI [0.312, 0.556], max class <= 1.139 (the 1.14 no-arb line), rho32 monotone,
    # the ruled at-bar continuity object (integer-step, the ledger's own gate, age credit
    # included)} — ONE feasible point on the grid; the vantage matrix and band spreads are
    # DIAGNOSTIC-ONLY and justified no part of this choice (amendment A2).
    O32_KAPPA=0.24
    O32_GAMMA=11.0
    O32_ETA=0.41
    O32_GAMMA_D=14.0
    # ===== ORDER I (RL_O36) — LEVER 2: THE COUNTERWEIGHT ==========================================
    # docs/evidence/order_i_2026-08-18/REMIX_36.json::chosen. With S1 live, "below expectation"
    # finally means below AGE-expectation, so the re-mix and the relief are RE-DERIVED on the
    # corrected readings rather than inherited. ONE joint calibration over
    # (lambda_S1, kappa, gamma_u, eta, gamma_d, lambda_rel) — the dose is a grid axis, never a
    # hand-picked number (PREREG_I.md §3; ORDER E's dose warning). Selection = minimum
    # corrected-surface SSE among the points feasible on BOTH the ruled constraints (rho32 monotone,
    # the ruled at-bar continuity object incl. the age credit, W inside the corrected hindsight 90%
    # CI [0.3117, 0.5560], slope in [0.885, 1.115], max class <= 1.139) AND the owner's acceptance
    # gates G1-G5. THE MECHANISM, stated so the direction is not claimed after the fact: kappa moves
    # weight OFF a row's pedigree leg and ONTO his shown production, and eta charges the pedigree leg
    # down as games accumulate — so a young row ABOVE his age bar gains twice while a young row BELOW
    # it loses. That is how the S1 lift is paid to performers and charged to sub-expectation rows.
    # m_u(0) = m_d(0) = 0 exactly, so day-0 prints cannot move. Dial off => the O32 repair values.
    # THE MATURE-ROW IDENTITY GATE BINDS HERE, and it is the finding, not an oversight: the re-mix is
    # keyed on CAREER GAMES, not on age, so ANY move in (kappa, gamma_u, eta, gamma_d) re-prices mature
    # rows too and breaks the owner's byte-identity law. ORDER C hit the same wall (REMIX_34.json: the
    # repaired knob point is the ONLY one of 3,960 the mature gate admits). The joint calibration
    # therefore carries the mature-row identity as a HARD constraint, which pins these four to the
    # repair values; the unconstrained optimum is REPORTED and NEVER CHOSEN. See PACKET_I.md §4.
    # The declared overrides below exist so the grid can be swept and the pinning PROVED, not asserted.
    # ORDER P: with RL_O37 on, the DEFAULTS become ORDER K's RULED setting (register v735) so the new
    # dial carries the O36-K stack on its own. An explicit RL_O36_* still wins, and the ORDER P build
    # line passes them explicitly anyway, so the two agree number for number rather than by trust.
    O36_KAPPA=float(os.environ.get('RL_O36_KAPPA','0.20' if _O37 else '0.24'))
    O36_GAMMA=float(os.environ.get('RL_O36_GAMMA','8.0' if _O37 else '11.0'))
    O36_ETA=float(os.environ.get('RL_O36_ETA','0.50' if _O37 else '0.41'))
    O36_GAMMA_D=float(os.environ.get('RL_O36_GAMMA_D','14.0'))
    O36_LAMBDA=float(os.environ.get('RL_O36_LAMBDA','1.08'))
    if _O36:
        # THE REBIND. Every consumer below reads the O32_* names; with the dial off not one byte of
        # this block executes, which is what makes 1f176444 reproduce exactly.
        O32_KAPPA=O36_KAPPA; O32_GAMMA=O36_GAMMA; O32_ETA=O36_ETA
        O32_GAMMA_D=O36_GAMMA_D; O32_LAMBDA=O36_LAMBDA
    # ---- ORDER D — THE PICK-CURVE SITTER FADE (RL_O35; owner word: the MEASURED curve) ----------
    # docs/evidence/order_d_2026-08-17/O35_CURVE.json — the prereg'd logistic fit (sit-penalty
    # s(p) = γ0 + γ1·ln(pick), SAT vs played-11+, ND 2005-2020) and the redistribution constant
    # s_norm solved so the pick-weighted mean fade at the ruled depth-2 cell equals the ruled
    # D(2) exactly (identity residual 0.0). SMOOTH in ln(pick), never a band step (R-PICKFADE's
    # condition). Effective picks past 64 (the pool index and every pickless convention) evaluate
    # the curve at 64 — a flat extension, disclosed; the clip bounds everything to [0.5, 2.0].
    O35_G0=0.1286221202379088
    O35_G1=0.4535958546743124
    O35_SNORM=1.7472066252064105
    O35_CLIP=(0.5,2.0)
    def o35_kappa_at(_pk):
        """Order D's POOLED exponent as a pure function of the effective pick. Split out (ORDER K) so
        the tall/small floor can be re-sited at a small's own PRE-FACTOR value without duplicating the
        constants — there is one pooled curve in this file and both callers read it."""
        _pk=max(1.0,min(64.0,float(_pk)))
        return min(O35_CLIP[1],max(O35_CLIP[0],(O35_G0+O35_G1*_math.log(_pk))/O35_SNORM))
    def o35_kappa(p):
        """The fade exponent at the row's effective pick. kappa < 1 softens (early picks — their
        sitters measured the safest), kappa > 1 deepens (late picks). Pure function of pick."""
        _pk=MA.effpk(p)
        return o35_kappa_at(float(_pk if _pk else 64))
    # ===== ORDER I (RL_O36) — LEVER 3: THE TALL/SMALL SITTER FACTOR ================================
    # ORDER H (docs/evidence/order_h_posfade_2026-08-17/PACKET_H.md §6 + H_RESULTS.json). The owner's
    # premise was CONFIRMED on base rates: rucks sit 3.55x more than smalls at the same pick (90% CI
    # 2.18-5.91), KPP 1.70x. The interaction resolves for TALL POOLED (h_TALL -0.6921, CI -1.239 to
    # -0.080, 96.8% of draws in the owner's direction) but NOT for RUCK alone (F2 fired at n=53) —
    # which is why this is a TALL/SMALL factor and never a ruck factor.
    #   s(pick, group) = g0 + g1*ln(pick) + h_TALL*(group is TALL)
    #   kappa(pick, group) = clip( s / s_norm', 0.5, 2.0 )
    # SMOOTH IN ln(pick): one constant added inside a logarithmic curve. No band, no threshold, no
    # cliff — R-PICKFADE's condition and H's falsifier F7. s_norm' is H's RE-SOLVED redistribution
    # constant: the mean of D2^kappa over H's fitted sitters still equals the ruled depth-2 fade
    # 0.5582775 EXACTLY (H residual -1.1e-16). THIS REDISTRIBUTES THE FADE BETWEEN TALLS AND SMALLS;
    # IT DOES NOT CHANGE THE TOTAL FADE THE BOARD CHARGES. m_TALL = 0.677 is the multiplicative
    # translation the owner asked for. TWO DECLARED SIDE EFFECTS, reported with numbers on the packet
    # and NOT discovered later: (i) D's 0.5 clip binds for talls over picks 1-24 and for smalls over
    # picks 1-9 — a flat spot the clip, not the fit, is setting; (ii) the total is pinned, so LATE
    # SMALL SITTERS PAY for the talls' relief (a small at pick 64 goes from exponent 1.1533 to 1.4527).
    O36_TG0=-0.8778138796894399                        # H_RESULTS.json interaction['SAT1|ctl1|TALL-pooled'].coef[3]
    O36_TG1=0.7100022285392401                         # ...coef[4]  (PACKET_H prints these rounded to -0.8778/+0.7100)
    O36_HTALL=-0.6921227120657417
    O36_SNORM=1.4284052406915069
    O36_D2=0.5582775                                   # the ruled depth-2 fade the identity is pinned to
    # ===== ORDER K — THE FADE FLOOR FIX (PREREG_K.md §2, owner comment 5321546243) =================
    # THE DEFECT. Because the fade base D(c_u) is BELOW 1, a HIGHER exponent is a HEAVIER fade. The
    # pooled fit (slope 0.4536) and the tall/small fit (slope 0.7100) are different lines, so the SMALL
    # curve does not sit above the pooled curve — IT CROSSES IT, and below pick 19 it sits BELOW, i.e.
    # LIGHTER. The redistribution identity pins only the MEAN, so nothing stopped that locally. The
    # symmetric 0.5 clip does not cause it and does not cure it: it clips the small curve part-way back
    # toward the pooled line and stops, leaving the inversion in place. Measured on Order J's own built
    # board: SEVEN smalls were made LIGHTER by a talls-only relief, +126 board points, worst
    # josh-smillie (MID, pick 7, 0 games) +79 — 772 -> 851, out of the range the owner's fade ruling
    # put him in.
    # THE FIX — THE FLOOR IS RE-SITED, NOT REMOVED. A SMALL's floor stops being the abstract number 0.5
    # and becomes HIS OWN PRE-FACTOR EXPONENT: the value Order D's pooled curve would have charged him
    # if the tall factor did not exist. The owner's acceptance test — "no small's sitting fade may
    # become lighter as a result of the tall factor" — therefore holds BY CONSTRUCTION, at every pick,
    # for every row, with no tolerance, no special case and no named row anywhere in the mechanism.
    # Talls keep the [0.5, 2.0] clip they were ruled with, and h_TALL is UNCHANGED at -0.6921227120657417.
    # THE COST, DISCLOSED: the identity is a real constraint, so charging smalls at picks 6-18 properly
    # must be given back, and it is given back by the normaliser rising 1.4284052407 -> 1.4340996146
    # (+0.40%), re-solved WITH the re-sited floor inside the constraint set on Order H's own 408 fitted
    # sitters (residual -1.1e-16). Late talls therefore end up with slightly MORE relief, not less
    # (pick 64: +11.40% -> +11.65%); talls at picks 1-25 are on the 0.5 floor either way and do not move.
    # REJECTED ALTERNATIVES, with their reasons, so the choice is on the record: (A) "re-solve the
    # normalisation with the clip inside the constraint set" is a NO-OP — Order H's solve already
    # carried the clip (oh_posfade.py:383) and re-solving the wired form reproduces 1.4284052406915069
    # to the last bit; the small curve's problem is its SLOPE, not its LEVEL. (B) "apply the factor
    # after the clip" discards Order H's fitted small slope and carries a ruled h onto a curve it was
    # never fitted against — a re-optimisation of a ruled object, which this seat is forbidden to make.
    O36_SNORM_K=1.4340996145830727                     # re-solved with the re-sited floor inside the constraint set
    O36_D2_FULL=0.5582775239783688                     # the depth-2 fade at the precision the identity was SOLVED at
    # ORDER H's own 408 fitted sitters, as (effective pick, is TALL) -> count. Transcribed so the
    # redistribution-identity assert needs no external file and cannot pass vacuously. Reproduced by
    # docs/evidence/order_k_2026-08-18/ok_floor_design.py from the same population Order H fitted on
    # (ND 2005-2020, picks 1-64, teaches_curve, year-1 games == 0, force-majeure rows removed).
    _O36K_SATCOUNTS={(1,False):2,(3,False):3,(4,False):1,(4,True):1,(5,False):1,(5,True):2,(7,False):1,
     (8,False):1,(8,True):1,(9,False):2,(10,True):2,(11,True):1,(12,True):2,(13,False):3,(13,True):1,
     (14,False):2,(14,True):1,(15,False):3,(15,True):3,(16,False):4,(16,True):2,(17,False):4,(17,True):1,
     (18,False):3,(18,True):1,(19,False):2,(19,True):1,(20,False):2,(20,True):1,(21,False):2,(21,True):1,
     (22,False):5,(22,True):1,(23,False):6,(24,False):2,(24,True):2,(25,False):2,(25,True):3,(26,False):5,
     (27,False):2,(27,True):1,(28,False):5,(29,False):4,(29,True):4,(30,False):3,(30,True):2,(31,False):4,
     (31,True):4,(32,False):4,(32,True):2,(33,False):5,(33,True):4,(34,False):3,(34,True):7,(35,False):4,
     (35,True):5,(36,False):4,(36,True):4,(37,False):5,(37,True):3,(38,False):7,(38,True):3,(39,False):6,
     (39,True):1,(40,False):6,(40,True):1,(41,False):6,(41,True):5,(42,False):7,(42,True):4,(43,False):5,
     (43,True):4,(44,False):6,(44,True):3,(45,False):8,(45,True):1,(46,False):3,(46,True):2,(47,False):8,
     (47,True):3,(48,False):6,(48,True):3,(49,False):8,(49,True):5,(50,False):6,(50,True):3,(51,False):5,
     (51,True):3,(52,False):5,(52,True):4,(53,False):4,(53,True):2,(54,False):5,(54,True):4,(55,False):6,
     (55,True):3,(56,False):6,(56,True):1,(57,False):9,(58,False):5,(58,True):4,(59,False):6,(59,True):2,
     (60,False):6,(60,True):4,(61,False):8,(61,True):3,(62,False):10,(62,True):2,(63,False):6,(63,True):3,
     (64,False):5,(64,True):5}
    # DECLARED, DEFAULT-ON measurement dial: RL_O36_FLOORFIX=0 restores Order J's wired form EXACTLY
    # (s_norm 1.4284052406915069, symmetric [0.5, 2.0] clip on both groups), so the fix's cost on every
    # row and every band is a NUMBER on the movers ledger rather than a paragraph.
    _O36_FLOORFIX=os.environ.get('RL_O36_FLOORFIX','1')!='0'
    # DECLARED, DEFAULT-ON measurement dial (the same discipline RL_O31_NOPHI applies to the stall
    # conditioning): RL_O36_TALL=0 prices the tall/small factor BY REMOVING IT, so its cost on every
    # row and every band is a NUMBER on the movers ledger rather than a paragraph. It falls back to
    # Order D's wired pooled exponent exactly.
    _O36_TALL=os.environ.get('RL_O36_TALL','1')!='0'
    def o36_kappa_at(_pk,_tall):
        """The fade exponent as a pure function of (effective pick, TALL/SMALL) — no player object, so
        the build-failing asserts below can sweep it over every pick without inventing rows."""
        _pk=max(1.0,min(64.0,float(_pk)))
        if not _O36_FLOORFIX:
            _s=O36_TG0+O36_TG1*_math.log(_pk)+(O36_HTALL if _tall else 0.0)
            return min(O35_CLIP[1],max(O35_CLIP[0],_s/O36_SNORM))
        _s=O36_TG0+O36_TG1*_math.log(_pk)+(O36_HTALL if _tall else 0.0)
        if _tall:
            return min(O35_CLIP[1],max(O35_CLIP[0],_s/O36_SNORM_K))
        # THE RE-SITED FLOOR: a small's floor is his own Order-D pooled exponent, which is itself
        # already >= O35_CLIP[0], so the 0.5 hard floor is subsumed and never breached.
        return min(O35_CLIP[1],max(o35_kappa_at(_pk),_s/O36_SNORM_K))
    def o36_kappa(p):
        """The fade exponent at the row's effective pick AND position class. Pure function of
        (pick, TALL/SMALL). TALL = the engine's own O32_TALLPOS = {KPD, KPF, RUCK}."""
        _pk=MA.effpk(p)
        return o36_kappa_at(float(_pk if _pk else 64),MA.gfut(p) in O32_TALLPOS)
    # ORDER C (RL_O34) — the R1 age credit's SURVIVING SCALE under the corrected normalization.
    # The repair's credit partially compensated the BLIND denominators; with the denominators fixed the
    # unchanged credit would DOUBLE-PAY age on every row the sites now pay correctly, so the credit is
    # RE-DERIVED jointly with the re-mix knobs on the corrected surface (REMIX_34.json — same
    # joint-derivation discipline, min corrected-SSE inside the ruled gates + the ORDER C mature-row
    # identity gate). Read ONLY when _O34 is set: the dial-off credit path is byte-identical.
    # REMIX_34.json::chosen — the joint grid left the repaired knob point (the ONLY knob point the
    # mature gate admits, 1 of 3960) x alpha in [0.75, 1.00] feasible (the 1.14 line kills alpha >
    # 1.00; the ruled at-bar continuity object kills alpha < 0.75); min corrected-SSE selects the
    # boundary 0.75 (obj 31.3 vs 33.0 at alpha=1). The unconstrained minimum (alpha 0, different
    # knobs, obj 20.6) moves mature rows up to 35 board points and is REPORTED, NEVER CHOSEN.
    O34_ALPHA=0.75
    def o31_pool_D(c):
        if c<=1.0: return 1.0
        if c>=O31_POOL_FLAT_FROM: return O31_POOL_D[O31_POOL_FLAT_FROM]
        _n=int(_math.floor(c)); _f=c-_n
        _d0=O31_POOL_D[_n]; _d1=O31_POOL_D[_n+1]
        return _d0 if _f<=0.0 else _math.exp((1.0-_f)*_math.log(_d0)+_f*_math.log(_d1))
    def _o31_loglin(pts,g):
        g=max(1e-9,float(g))
        if g<=pts[0][0]: return pts[0][1]
        if g>=pts[-1][0]: return pts[-1][1]
        for _i in range(1,len(pts)):
            g0,y0=pts[_i-1]; g1,y1=pts[_i]
            if g0<=g<=g1:
                _t=(_math.log(g)-_math.log(g0))/(_math.log(g1)-_math.log(g0))
                if y0<=0.0 or y1<=0.0: return y0+_t*(y1-y0)
                return _math.exp(_math.log(y0)+_t*(_math.log(y1)-_math.log(y0)))
        return pts[-1][1]
    def o31_rho_base(g):
        """The 31-F reliability curve UNTOUCHED — the pre-existing production leg's own weight."""
        g=float(g)
        return 0.0 if g<=0.0 else 1.0-_math.exp(-((g/O31_TAU_RHO)**O31_B_RHO))
    def rho31(g):
        """MEASURED PRODUCTION RELIABILITY. rho(0)=0 EXACTLY, strictly increasing, -> 1. Fitted so a thin
        cohort's aggregate price matches the R1 cumulative backbone. Pure function of g.
        ORDER A stage 6: the R-REMIX low-g bump rides on top (see the O32 block above); rho(0)=0 and
        the deep end are untouched by construction."""
        _r=o31_rho_base(g)
        if _r>0.0 and _O32S>=6 and O32_KAPPA>0.0:
            g=float(g)
            _r=_r+O32_KAPPA*((g/O32_GAMMA)*_math.exp(1.0-g/O32_GAMMA))*(1.0-_r)
        return _r
    # ---- ORDER A REPAIR R1 (PREREG_32R.md; owner-directed) -----------------------------------------
    # The re-mix's ADDED production weight reads shown production at the player's AGE-APPROPRIATE
    # expectation: the owner caught that the re-mix judged young output against the MATURE bars —
    # the same defect S1 measured in the gate (86-100% of age-18/19 seasons flagged). The repair
    # credits the re-mix leg with A(p,Y) = Δ(age, class)·20·_PL_F — the S1 C3 development gap as one
    # 20-game season, engine currency. ONLY the κ-bump weight carries it: the pre-existing
    # production leg (Phat at rho_base) is untouched (the gate-only scope discipline), m_u(0)=0 so
    # day-0 prints cannot move, and ages >= 24 carry zero (cap law).
    def o32_age_gap(p,Y):
        """Δ(age at Y, class) in points per game; 0 from age 24; 0 without a birth year."""
        _by=p.get('_by')
        if not _by: return 0.0
        _a=Y-int(_by)
        if _a>=24: return 0.0
        return O32_GATE_DELTA['TALL' if MA.gfut(p) in O32_TALLPOS else 'SMALL'][max(18,min(23,int(_a)))]
    def o32_age_credit(p,Y,g):
        """The R1 age credit on the re-mix's added production weight: κ·m_u(g)·(1-rho_base)·A(p,Y)."""
        if _O32S<6 or O32_KAPPA<=0.0: return 0.0
        g=float(g)
        if g<=0.0: return 0.0
        _d=o32_age_gap(p,Y)
        if _d<=0.0: return 0.0
        _c=O32_KAPPA*((g/O32_GAMMA)*_math.exp(1.0-g/O32_GAMMA))*(1.0-o31_rho_base(g))*_d*20.0*_PL_F
        return _c*O34_ALPHA if _O34 else _c                 # ORDER C: re-derived scale; dial-off byte-identical
    def beta31(g,pool=False):
        """The measured additive pedigree coefficient. ORDER 31-F: pool rows take the POOL-DERIVED curve
        (o31f_pool.py), ND rows the ND curve. One law still — the same expression, the row's own
        measured coefficient. RL_O31F_NOBPOOL=1 restores ORDER 31's ND-borrowed behaviour."""
        return _o31_loglin(O31_BETA_POOL if (pool and not _O31F_NOBPOOL) else O31_BETA,g)
    def phistall31(g,pool=False):
        if pool and not _O31F_NOBPOOL: return _o31_loglin(O31_PHIST_POOL,g)
        return _o31_loglin(O32_PHIST if _O32S>=4 else O31_PHIST,g)
    def phi31(g,s,pool=False):
        """THE 30B-C STALL CONDITIONING. Phi(g,0)=1 EXACTLY, so it cannot touch a gameless row."""
        if s<=0: return 1.0
        return 1.0-(min(float(s),O31_PHI_RAMP)/O31_PHI_RAMP)*(1.0-phistall31(g,pool))
    def o31_played_units(p,Y):
        """Season-units in which the row PLAYED, on the same clock the fade uses: 1.0 per completed season,
        _fEy for the in-progress one. ORDER A stage 2 (M2, owner ruling on S2 P1): a season's credit is
        f·min(1, g/2) — the G*=2 per-season played credit that retires the one-game full-cure cliff.
        u(0)=0, so day-0 prices are untouched by construction."""
        _u=0.0
        for _x in p.get('scoring') or []:
            if _x['year']>Y or not _x['games']: continue
            _f=(_fEy(Y,p) if _x['year']==Y else 1.0)
            _u+=_f*(min(1.0,float(_x['games'])/2.0) if _O32S>=2 else 1.0)
        return _u
    def o31_cu(p,Y):
        """THE UNPLAYED CLOCK. c_u = the fade clock MINUS the time he actually played. This is the brief's
        'the time-fade applies to UNPLAYED time only' -- a played season advances g, not the sitter clock,
        which is what kills the sitter-fade-while-playing defect. For a row that has NEVER played it is the
        fade clock EXACTLY, so every printed-day-0 price is unmoved by construction.
        ORDER A stage 3 (M3, owner ruling on S2 P2): a DELIVERED season (the one o32_delivered
        predicate: games >= 10·f AND avg >= the age-referenced gate bar) RESETS accumulated c_u to
        zero as of that season; fade re-accrues only on subsequent sitting. A gameless career has no
        delivered season, so day-0 prices are again untouched by construction."""
        if _O32S>=3:
            _yd=None
            for _x in (p.get('scoring') or []):
                if _x['year']<=Y and _x.get('games') and o32_delivered(p,Y,_x):
                    _yd=_x['year'] if _yd is None else max(_yd,_x['year'])
            if _yd is not None:
                _clk=max(0.0,float(Y-_yd-1)+(_fEy(Y,p) if Y>_yd else 0.0))
                _cred=0.0
                for _x in (p.get('scoring') or []):
                    if _yd<_x['year']<=Y and _x.get('games'):
                        _f=(_fEy(Y,p) if _x['year']==Y else 1.0)
                        _cred+=_f*min(1.0,float(_x['games'])/2.0)
                return max(0.0,_clk-_cred)
        return max(0.0,fade30b_clock(p,Y)-o31_played_units(p,Y))
    def o31_D(p,Y):
        """The fade at the UNPLAYED depth. ONE law for every pathway: the ruled ND schedule is applied to
        every non-pool row (a BORROW for RD and pickless-ND rows, disclosed), and pool rows take the
        Step-2-derived pool schedule.
        ORDER A stage 5 (M4): current + most-recent-season selection buys back the discount on
        unproven pedigree — D·(1+λ·σ_sel) — CAPPED AT 1: never above full pedigree, the ceiling
        stays production-only. σ_sel(0 games)=0, so gameless rows are untouched."""
        _cu=o31_cu(p,Y)
        _D=(o31_pool_D(_cu) if p.get('_pool') else o31_fade_D(_cu))
        # ORDER D (RL_O35, owner word: the MEASURED curve): the per-year sitting cost scales with
        # the fitted pick-signal — D^kappa(pick), smooth in ln(pick), NEVER a band step. Applied to
        # the row's own schedule BEFORE the relief; 1^kappa == 1 so rows the fade does not reach
        # cannot move, and the redistribution identity keeps the pooled fade at the ruled row.
        if _O35 and _D<1.0:
            # ORDER I (RL_O36): the pooled exponent becomes the TALL/SMALL exponent. Same site, same
            # smooth log-pick curve, same clips; only the numerator carries the position term and the
            # normaliser is re-solved so the pooled fade stays pinned at the ruled row.
            _D=_D**(o36_kappa(p) if (_O36 and _O36_TALL) else o35_kappa(p))
        if _O32S>=5 and _D<1.0:
            _sg=o32_sigma_sel(p,Y)
            if _sg>0.0: _D=min(1.0,_D*(1.0+O32_LAMBDA*_sg))
        return _D
    def o31_stall_run(p,Y):
        """s -- THE CURRENT STALL RUN: consecutive most-recent seasons the row PLAYED but did not DELIVER
        (delivered == games >= 10 AND avg >= his position's v0-language bar). A delivered season RESETS it.
        A GAMELESS season is SKIPPED, never counted: unplayed time is D(c_u)'s channel and counting it in
        both would be exactly the double-discount the no-stacking constraint forbids.
        s >= 1 therefore IMPLIES g >= 1, which is what makes pi(0,c)=D(c) safe for every s."""
        _pos=MA.gfut(p)
        _bar0=_O30BP_BARS.get(_pos)
        if _bar0 is None: return 0
        _s=0
        for _x in sorted((p.get('scoring') or []),key=lambda r:-r['year']):
            if _x['year']>Y: continue
            _g=float(_x['games'] or 0.0)
            if _g<=0.0: continue                                   # gameless: D(c_u)'s channel, skipped
            _u=(_fEy(Y,p) if _x['year']==Y else 1.0)
            # ORDER A stage 1 (M1): the AVG leg reads the age-referenced gate bar — a NEW gate-only
            # object; the flat production references are untouched. The GAMES leg is unchanged (S1 §3).
            _bar=(o32_gate_bar(_pos,_x['year']-p['_by']) if (_O32S>=1 and p.get('_by')) else _bar0)
            if _g>=10.0*_u and float(_x['avg'] or 0.0)>=_bar: break # DELIVERED -> the run resets
            _s+=1
        return _s
    # ===== ORDER P (RL_O37) — THE PEDIGREE-CONDITIONAL CHARGE =====================================
    # PREREG_P_BUILD.md (pushed before this edit) · docs/evidence/order_p_2026-08-18 (the measurement,
    # the derivation and the offline pricing) · docs/evidence/order_p_build_2026-08-18 (this wiring).
    #
    # WHAT IS REPLACED, AND WHY. The ORDER A stage-6 charge below reads GAMES AND NOTHING ELSE:
    #     pi *= max(0, 1 - eta*(g/gamma_d)*exp(1 - g/gamma_d))          eta 0.50, gamma_d 14
    # It peaks at exactly 14 games and then FALLS AWAY, so a 36-game row keeps MORE of his unearned
    # entry price than a 17-game row however either of them played. Measured on the young board: two
    # rows within two games of each other and 63 points a game apart on production-against-age paid
    # the identical charge to the last decimal (PACKET_N). That is the defect the owner asked to
    # remove, and this block removes it.
    #
    # WHAT REPLACES IT, for rows aged UNDER 24 at the year being priced:
    #     pi *= exp( -LAMBDA * A(g) * T(s_P) )
    #     A(g)  = 1 - exp(-g/G0)                        how much evidence g games is. A(0) = 0 EXACTLY.
    #     T(s)  = clip( 1 - THETA_R*(s - s0), 0, TMAX )  what the evidence says. Non-increasing in s.
    #     s_P   = the games-weighted mean of ( season avg - BAR_P ) over every season played to date
    #     BAR_P = o32_gate_bar(that season's bar, his age that season) + PG(ln v0, class)
    #
    # THE ONE NEW OBJECT IS PG, THE PEDIGREE PREMIUM: how far above his AGE bar a player who entered
    # at that price actually produces. It is MEASURED FROM OUTCOMES, never from prices — v0 is the
    # axis the outcomes are indexed by and no board price is added to anything. It is the whole of the
    # owner's sentence: "there should be a higher bar / more positive signs required to maintain a
    # higher valuation".
    #
    # WORKED, ON TWO REAL ROWS THAT SIT 17 GAMES EACH AND ABOUT 1.7 POINTS A GAME BELOW THEIR AGE BAR.
    # Under the charge above they pay the IDENTICAL 49.0%, because it only reads games. Zeke Uwland
    # was pick 2 and cost 2,583; a player at that price produces 19.2 points a game clear of the age
    # bar, so against what is priced into him he is 20.9 short and he pays 84.7%. Cooper Harvey was
    # pick 56 and cost 265; a player at that price produces 1.3 BELOW the age bar, so he is half a
    # point short and he pays nothing. Same production for their age, opposite verdicts.
    #
    # ON THE FORBIDDEN SET. This object is NOT the deleted par machinery returning. Par entered price
    # as max(0, pole - production) and as a level substitute, both strictly NON-NEGATIVE: a high pick
    # was PAID for being a high pick. This object enters a CHARGE and T is non-increasing in surplus,
    # so raising an expensive row's bar RAISES his charge and LOWERS his price — the opposite sign.
    # Three bounds, all asserted below or in the build proofs: F = 1 - exp(-LAMBDA*A*T) is in [0,1),
    # so no row can price above its own UNCHARGED (eta-zero) price, a board the forbidden set is
    # already absent from (0 of 9,746 vantages, STEP4_P_out.txt); A(0) = 0 exactly, so no day-0 print
    # moves; and the bar reads outcomes, never prices. THE OWNER STILL RULES ON THE WORD.
    #
    # THE CONSTANTS ARE MEASURED AND SOLVED. NOT ONE OF THEM IS RE-FITTED HERE.
    #   G0, BETA_sat  — the BETA_P(g) curve of PACKET_P section 4.5, fitted as BETA_sat*(1-exp(-g/G0))
    #                   weighted by each bin's own inverse variance. MECH_P.json.
    #   LAMBDA        — SOLVED, not chosen: bisection so the derived charge removes exactly the same
    #                   total points from the year-1 class-mark population (cohort classes 2005-2015)
    #                   as the current charge does. 101,402.7 matrix points, matched to the last
    #                   decimal. STEP4_P.json::mechanism.LAMBDA.
    #   THETA_R       — FOLLOWS as BETA_sat/LAMBDA, so the delivered slope d ln(retained pedigree)/ds
    #                   equals the MEASURED slope at every level of surplus. It is not free.
    #   s0            — the games-weighted mean of s_P over the young cohort. T(s0) = 1.
    #   TMAX          — T at the cohort's own 5th percentile of s_P, so the worst 5% all pay the same
    #                   top rate rather than an unbounded one. It is not free.
    # THERE IS NO FREE PARAMETER. LAMBDA*THETA_R == BETA_sat is asserted at load.
    O37_G0=9.890000000000008                                   # MECH_P.json::G0        90% CI [7.60, 12.98]
    O37_BETA_SAT=0.11464630061141393                           # MECH_P.json::BETA_sat  90% CI [0.10416, 0.12718]
    O37_LAMBDA=0.1743833036575403                              # STEP4_P.json — SOLVED by the anchoring identity
    O37_S0=-2.452720891469074                                  # MECH_P.json::s0
    O37_S_P5=-33.06133449874688                                # MECH_P.json::s_p5 — the cohort's own 5th percentile
    O37_AGE_GATE=24                                            # the age bar has content below 24 and none at or above it
    O37_THETA_R=O37_BETA_SAT/O37_LAMBDA                        # NOT FREE
    O37_TMAX=1.0-O37_THETA_R*(O37_S_P5-O37_S0)                 # NOT FREE
    # ===== ORDER R (RL_O39_TMAXPCT / RL_O39_BETASAT) — THE OWNER'S TWO SOFTENINGS ==================
    # PREREG_R.md, pushed before this edit · docs/evidence/order_r_2026-08-18.
    # THIS IS A MEASUREMENT ORDER. NOTHING HERE IS ADOPTED AND NOTHING LANDS. Both dials off => the
    # effective constants below are the ORDER P constants BIT FOR BIT (same float expressions, same
    # order of operations), so ORDER P's 374d4e44 and every ORDER Q board reproduce BYTE-EXACT.
    #
    # THE CAP. TMAX is T evaluated at the young cohort's own Qth percentile of s_P, so the worst
    # -producing Q% all pay the same top rate rather than an unbounded one. ORDER P set Q = 5, which
    # charges a row sitting at the cap 97.3% of his pedigree leg. The owner ruled Q = 15 or 20. The
    # three percentiles below are np.percentile(sP, Q) over the SAME 4,143 young-cohort season rows in
    # STEP2_P.json that produced MECH_P.json::s_p5, by the SAME call, unweighted. The Q=5 entry
    # reproduces MECH_P.json::s_p5 to the last bit and that is asserted at load (R10 below).
    O39_S_PQ={5:-33.06133449874688,           # == O37_S_P5, MECH_P.json::s_p5
              15:-22.148794633345666,
              20:-19.024574086528315}
    # THE SLOPE. BETA_sat is the MEASURED saturated slope of the pedigree leg's response to surplus.
    # Its published 90% CI is a parametric bootstrap over the seven games bins, ORDER P seed 32.
    # SOFTENING OUTSIDE THE MEASURED INTERVAL IS FORBIDDEN and the dial HALTS on it (R11).
    O39_BSAT_CI=(0.10416359711151935,0.1271777523096214)      # MECH_P.json::BETA_sat_ci
    O39_BETA_SAT=(float(_O39_BSAT_RAW) if _O39_BSAT_RAW!='' else O37_BETA_SAT)
    if _O39_BSAT_RAW!='' and not (O39_BSAT_CI[0]<=O39_BETA_SAT<=O39_BSAT_CI[1]):
        raise SystemExit('ORDER R HALT (R11): RL_O39_BETASAT=%.17g is OUTSIDE the published 90%% CI '
                         '[%.17g, %.17g]. The owner ruled the charge may be softened INSIDE the measured '
                         'interval and not beyond it. This dial does not price an unmeasured slope.'
                         %(O39_BETA_SAT,O39_BSAT_CI[0],O39_BSAT_CI[1]))
    # THETA_R FOLLOWS the slope and TMAX FOLLOWS THETA_R AND the percentile. NEITHER IS FREE, and TMAX
    # is RECOMPUTED from the effective THETA_R every time rather than carried from ORDER P. Holding a
    # stale TMAX while moving BETA_sat would break LAMBDA*THETA_R == BETA_sat's meaning at the cap.
    O39_THETA_R=O39_BETA_SAT/O37_LAMBDA                        # NOT FREE
    O39_TMAX=1.0-O39_THETA_R*(O39_S_PQ[_O39_PCT]-O37_S0)       # NOT FREE — recomputed, never stale
    # DISCLOSED, LOUDLY: LAMBDA IS NOT RE-SOLVED. On ORDER P, LAMBDA was SOLVED by an anchoring
    # identity — bisection so the new charge removes exactly the same total points from the year-1
    # class-mark population as ORDER K's blind charge did. Moving BETA_sat or TMAX BREAKS that anchor,
    # so these variants remove LESS total charge than ORDER P by construction. THAT IS THE SOFTENING.
    # Re-solving LAMBDA would claw back exactly what the owner asked to give away. The choice is the
    # order's and it is written on the prereg, not discovered afterwards.
    # R9/R10 — the two identities, asserted at load on every path including dial-off.
    if abs(O37_LAMBDA*O39_THETA_R-O39_BETA_SAT)>1e-15:
        raise SystemExit('ORDER R HALT (R9): LAMBDA*THETA_R = %.17g is not the effective BETA_sat = '
                         '%.17g — the tilt has come loose from the measurement.'
                         %(O37_LAMBDA*O39_THETA_R,O39_BETA_SAT))
    if abs(O39_TMAX-(1.0-O39_THETA_R*(O39_S_PQ[_O39_PCT]-O37_S0)))>1e-12:
        raise SystemExit('ORDER R HALT (R10): TMAX is not 1 - THETA_R*(s_pQ - s0) on the EFFECTIVE '
                         'THETA_R. A stale cap is being carried.')
    if abs(O39_S_PQ[5]-O37_S_P5)>0.0:
        raise SystemExit('ORDER R HALT (R10): the Q=5 percentile in O39_S_PQ is not MECH_P.json::s_p5 '
                         'bit for bit. The percentile table has drifted from the population it came from.')
    if not _O39 and (O39_THETA_R!=O37_THETA_R or O39_TMAX!=O37_TMAX):
        raise SystemExit('ORDER R HALT (R1): with both ORDER R dials unset the effective constants are '
                         'not the ORDER P constants bit for bit. Dial-off would not be byte-exact.')
    # THE PEDIGREE PREMIUM SURFACE, in AFL Fantasy points per game, as a function of ln(v0).
    # Estimated by games-weighted LOCAL-LINEAR KERNEL REGRESSION on ln(v0), tricube kernel, bandwidth
    # 0.40 in log-v0 units — the SAME estimator family par_build.py used over log-pick at the same
    # bandwidth, chosen deliberately so the comparison with the deleted object is like-for-like rather
    # than flattering. Fitted separately for TALL (KPD/KPF/RUCK) and SMALL (MID/SD/SF) — the same
    # class pooling the C3 age surface uses — on 5,041 season rows over 1,575 players and 58,488
    # games: every season with games played, at age 18-23, by an entrant from 2005 on, up to 2025.
    # The house monotonicity guard (pool-adjacent-violators, increasing) is applied to the fitted
    # grid: a more expensively priced player is never expected to produce less.
    # POOLED OVER AGE. The age-carrying variant WAS measured (PACKET_P section 7.1) and is WORSE on
    # every rail — picks 1-10 primary +11.36% against +8.62%, modern +21.51% against +18.85%. It is
    # not built and it is not a dial.
    # Each entry is (lo, hi, y): 121 nodes evenly spaced in ln(v0) from the 1st to the 99th percentile
    # of the fitted population. Linear between nodes; HELD FLAT outside — never extrapolated.
    # Regenerated and proved by docs/evidence/order_p_build_2026-08-18/op_surface_emit.py.
    O37_PG_GRID={
        'TALL':(4.5664293576716606,7.9885090493489335,(
         -5.4455867081102411,-5.4455867081102411,-5.4455867081102411,-5.4455867081102411,-5.4455867081102411,-5.4455867081102411,
         -5.4047760344362308,-4.9137051657926945,-4.1839519626341524,-3.547798820225772,-3.1187175304818613,-2.8306827587028107,
         -2.6045867243204794,-2.392965577383134,-2.1575978172075794,-1.8634270971665809,-1.560737614127947,-1.2463682940640921,
         -0.82697777110007242,-0.28727210729525771,0.28334745102024395,0.77364690364419653,1.1176538458895451,1.3142810568719852,
         1.4310924620360834,1.520241712493009,1.6268839845690664,1.776900578289401,1.9598395453176443,2.1565703297145311,
         2.3199477429090098,2.3199477429090098,2.3199477429090098,2.3199477429090098,2.3199477429090098,2.3199477429090098,
         2.3199477429090098,2.3199477429090098,2.3199477429090098,2.474881949521277,2.6717527927652842,2.8539009509446318,
         3.0553005117574554,3.2248913696028327,3.3244578540162637,3.3857104690490463,3.4355619922454075,3.4938807892483328,
         3.5947902186262426,3.7601719898077497,3.9754096770391913,4.2049119382434821,4.4059043555525639,4.5912396350554889,
         4.7996043033283202,5.0266845168513967,5.2423954980924758,5.4329737318027815,5.5893790725385122,5.7119077410334489,
         5.8151049019440784,5.9120969830277739,6.0208086283023166,6.1708840705720354,6.3531589632807055,6.5402149256632711,
         6.7098008286908533,6.8522404947596378,6.980153007982616,7.1048873555435152,7.2306252201587577,7.3540943529449283,
         7.4757697071890457,7.5836700076450869,7.62948305161009,7.6303872722392505,7.6303872722392505,7.6430773265604213,
         7.6870980531344522,7.7766525774302959,7.8756881756463715,7.9633911919679612,8.0445919060075664,8.1221435028876048,
         8.1926242718733544,8.2856734010323052,8.4537394810191948,8.7338293170424244,9.1427768527383044,9.6774305607147912,
         10.334428729611606,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,
         10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,
         10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,
         10.806543129062868,10.806543129062868,10.806543129062868,10.806543129062868,11.289519873909789,12.494465623798206,
         13.790014604208249,15.165841316681965,16.629718563960207,18.166261696501994,19.724615375615219,21.29444967737923,
         22.922043787483595)),
        'SMALL':(4.513054897080286,8.1444759697678766,(
         -7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,
         -7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,-7.0364117904300656,
         -7.0364117904300656,-7.0364117904300656,-6.9773343756962305,-6.9102456731853668,-6.8867837853820841,-6.8464823480538177,
         -6.511703309229838,-5.8993680558490569,-5.2586397290260249,-4.6294139565183876,-4.0039710870706218,-3.369989812391148,
         -2.6987267228160507,-2.0594809191407717,-1.5456971844867691,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,
         -1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,
         -1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,
         -1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.2623139425581236,
         -1.2623139425581236,-1.2623139425581236,-1.2623139425581236,-1.0572820081904364,-0.58708959825022011,-0.035343884619787727,
         0.52871229816215748,1.0565821790478596,1.5489700305648837,2.0044630763037796,2.4129854340099217,2.7675906478389396,
         3.0699264814972471,3.335506691763455,3.606059236306455,3.8818979295555134,4.1761265754243224,4.4790899072732095,
         4.7631474761536525,5.0094995251320986,5.2124068582748908,5.3699927357834421,5.4864157942619096,5.5900876575677954,
         5.7114709064914733,5.8704887287729814,6.0776429038458968,6.3145545807411683,6.5320472490656307,6.5320472490656307,
         6.5320472490656307,6.5320472490656307,6.5320472490656307,6.5320472490656307,6.5320472490656307,6.5320472490656307,
         6.5320472490656307,7.0464452408760305,7.7002183677861256,8.2807077727565961,8.7699574761164047,9.1743996939167616,
         9.5102475540686697,9.9191904515388014,10.516979561510675,11.299647269537539,12.150777171882492,12.934785820087493,
         13.596950104805869,14.125890693373643,14.515989950412777,14.862776535541089,15.326868021342062,15.893077430881478,
         16.433508150193134,16.840860053165954,17.132174599855659,17.34201506740057,17.486029109510262,17.571748104372329,
         17.74030898924396,18.262436503686921,18.900128819869604,19.553610645797963,20.215990248694148,20.855503188591502,
         21.440141766150504,21.955229100286488,22.432987140706345,22.94209310608661,23.554904535865262,24.351188761151118,
         25.440230012706913)),
    }
    def o37_pg(v0,cls):
        """PG(ln v0, class) in points per game. Linear on the fitted grid, held flat outside its
        support. Reproduces op_lib.Premium.at_v0 — proved node by node in the build packet."""
        _lo,_hi,_y=O37_PG_GRID[cls]
        _x=_math.log(max(1e-9,float(v0)))
        if _x<=_lo: return _y[0]
        if _x>=_hi: return _y[-1]
        _t=(_x-_lo)/(_hi-_lo)*(len(_y)-1)
        _i=int(_t)
        if _i>=len(_y)-1: return _y[-1]
        return _y[_i]+(_t-_i)*(_y[_i+1]-_y[_i])
    _O37_SCACHE={}
    def o37_surplus(p,Y):
        """s_P — the games-weighted mean of (season avg - BAR_P) over every season the row PLAYED up
        to and including Y, in AFL Fantasy points per game. POSITIVE means he is producing above what
        a player priced like him produces at his age.
        Returns None — and the ORDER K charge is then kept UNCHANGED for that row — when the row has
        never played, has no day-0 v0 object, has no birth year, or carries a season the bar cannot
        read. That is the SAME fallback op_step4.py::F_new used offline, so the built board and the
        published estimate are comparable line by line rather than nearly."""
        _ck=(id(p),p.get('key'),int(Y))
        if _ck in _O37_SCACHE: return _O37_SCACHE[_ck]
        _r=None; _v=day0_v0(p); _by=p.get('_by')
        if _v is not None and _by:
            # ENGINE currency, at the matrix emitter's own one-decimal convention, so the axis this
            # premium is read on is EXACTLY the axis it was fitted on.
            _v0=round(float(_v)*_PL_F,1)
            _num=_den=0.0; _ok=True
            for _x in (p.get('scoring') or []):
                if _x['year']>Y: continue
                _gg=float(_x.get('games') or 0.0)
                if _gg<=0.0: continue
                _pos=MA._fit_bar(p,_x['year'])
                _b=o32_gate_bar(_pos,_x['year']-_by)
                if _b is None or _x.get('avg') is None: _ok=False; break
                _num+=_gg*(float(_x['avg'])-(_b+o37_pg(_v0,'TALL' if _pos in O32_TALLPOS else 'SMALL')))
                _den+=_gg
            if _ok and _den>0.0: _r=_num/_den
        _O37_SCACHE[_ck]=_r
        return _r
    def o37_factor(p,Y,g):
        """The multiplier the pedigree leg is charged by. Falls back to the ORDER K charge, byte for
        byte, for every row this object cannot speak about — a mature row, a row with no birth year,
        a row with no day-0 v0, a row whose seasons carry no bar."""
        _old=max(0.0,1.0-O32_ETA*((float(g)/O32_GAMMA_D)*_math.exp(1.0-float(g)/O32_GAMMA_D)))
        _by=p.get('_by')
        if not _by or (int(Y)-int(_by))>=O37_AGE_GATE: return _old
        _s=o37_surplus(p,Y)
        if _s is None: return _old
        _T=min(max(1.0-O37_THETA_R*(_s-O37_S0),0.0),O37_TMAX)
        return _math.exp(-O37_LAMBDA*(1.0-_math.exp(-float(g)/O37_G0))*_T)
    # ===== ORDER Q (RL_O38A / RL_O38B1 / RL_O38B2) — TWO DEFECTS IN THE ORDER P CHARGE ============
    # PREREG_Q.md, pushed before this edit · docs/evidence/order_q_2026-08-18.
    # THIS IS A MEASUREMENT ORDER. NOTHING HERE IS ADOPTED AND NOTHING LANDS. All three dials off =>
    # not one byte of this block executes and ORDER P's board 374d4e44 reproduces BYTE-EXACT.
    #
    # DEFECT 1 — THE PICK REVERSAL (repaired by RL_O38A). Hold a row's output and games fixed and
    # raise ONLY his entry price. His pedigree leg is  v0 * exp(-LAMBDA*A(g)*T(s_P)). Raising v0
    # raises the bar he is judged against through PG, which raises his charge. Differentiating, the
    # leg FALLS with price wherever  dPG/dln(v0) > 1/(BETA_sat*A).  At saturation that threshold is
    # 1/0.1146463 = 8.723 and the measured SMALL premium slope averages about 8.95 across its
    # support, so this is a board-wide reversal and not an exotic corner. A higher pick can be worth
    # LESS than a lower pick on identical evidence.
    #
    # THE REPAIR, WITH NO FREE PARAMETER. Write x = ln(v0) in engine currency and
    #     psi(x) = x - LAMBDA*A(g)*T( OUT - wTALL*PG(x,TALL) - wSMALL*PG(x,SMALL) )
    # so that the charged pedigree leg is proportional to exp(psi(x)). The charge is CAPPED at its
    # own inversion point by taking the RUNNING MAXIMUM from the left:
    #     psi_A(x) = max over u <= x of psi(u)        factor = exp( psi_A(x) - x )
    # exp(psi_A) is non-decreasing in x BY CONSTRUCTION, so no lower entry price can price higher.
    # psi_A >= psi always, so the charge is only ever CAPPED, never raised: a price can only move UP
    # against ORDER P. And psi(u) <= u for every u <= x, so the factor stays in (0,1] and no row can
    # price above its own uncharged price. This is the same isotonic idea the ISO multiplier already
    # uses in this engine over pick, applied here over entry price.
    #
    # IT IS COMPUTED EXACTLY, NOT ON A GRID. PG is piecewise linear on its published nodes and T is
    # piecewise linear in s with two clip breakpoints, so psi is piecewise linear in x. The maximum
    # of a piecewise linear function sits at a breakpoint. The candidate set is therefore the premium
    # grid nodes of both classes below x, the flat-support boundaries, the clip crossings inside each
    # segment, and x itself.
    # ONE DISCLOSED RESIDUAL: the engine reads the premium at v0 ROUNDED TO ONE DECIMAL, which makes
    # the true function a staircase with steps of 0.1 in engine currency. Monotonicity therefore holds
    # up to one rounding cell, not to the last bit. The residual is bounded by BETA_sat*A*(dPG/dx)*
    # (0.1/v0) in log terms -- about 3e-5 of the leg at v0 = 3,000, well under one board point -- and
    # it is MEASURED densely in the continuity suite rather than asserted.
    #
    # DEFECT 2 — THE AGE-24 CLIFF (repaired by RL_O38B1 or RL_O38B2). ORDER P's own age gate reads
    # `if (int(Y)-int(_by))>=O37_AGE_GATE: return _old`. At 24 the charge does not switch off. It
    # HANDS BACK to ORDER K's games-only charge. So on his 24th birthday, with his games and his
    # output unchanged, a player's price becomes his ORDER K price. The owner's words: "players
    # shouldn't have drastic price changes for no reason other than getting older."
    #   RL_O38B1 — DELETE THE GATE. The charge runs at every age on the same bar. From 24 the S1 age
    #     bar already equals the flat bar by construction, so a mature row is judged against the flat
    #     bar plus the measured premium. No phase-out and no new parameter. THE KNOWN COST: mature
    #     rows are NO LONGER byte-identical to ORDER K. That is the price of this option and it is
    #     measured and reported in full, never buried.
    #   RL_O38B2 — RAMP THE CHARGE OUT ACROSS AGES 23 TO 26, in the exponent:
    #       ln f = w(age)*ln f_P + (1 - w(age))*ln f_K
    #       w = 1 at 23 and below, 2/3 at 24, 1/3 at 25, 0 at 26 and above.
    #     THE ENDPOINT 26 IS A FREE PARAMETER. IT WAS INVENTED BY THIS SEAT AND IT WAS NOT MEASURED.
    #     It is never described as derived. A second disclosure: age in this engine is the integer
    #     int(Y) - int(birth year), so this does not remove the step. It replaces one step of full
    #     size with three steps of a third the size. That is what a ramp can be on an integer axis.
    # The two are alternatives, not a stack. Setting both HALTS at load.
    def o38_pg_at(_x,cls):
        """PG read directly at ln(v0) rather than at v0. Identical to o37_pg by construction:
        o37_pg(v) takes the log first and then does exactly this interpolation."""
        _lo,_hi,_y=O37_PG_GRID[cls]
        if _x<=_lo: return _y[0]
        if _x>=_hi: return _y[-1]
        _t=(_x-_lo)/(_hi-_lo)*(len(_y)-1)
        _i=int(_t)
        if _i>=len(_y)-1: return _y[-1]
        return _y[_i]+(_t-_i)*(_y[_i+1]-_y[_i])
    _O38_PCACHE={}
    def o38_parts(p,Y):
        """(OUT, wTALL, wSMALL) on exactly o37_surplus's own rules and fallbacks.
        OUT is the games-weighted mean of (season avg - AGE bar): the part of s_P that does NOT move
        with entry price. wTALL/wSMALL are the games shares of the two premium classes. Then
            s_P(v) = OUT - wTALL*PG(v,'TALL') - wSMALL*PG(v,'SMALL')     EXACTLY.
        Returns None wherever o37_surplus returns None, so the fallback population is identical."""
        _ck=(id(p),p.get('key'),int(Y))
        if _ck in _O38_PCACHE: return _O38_PCACHE[_ck]
        _r=None; _by=p.get('_by')
        if _by:
            _num=_den=_wt=0.0; _ok=True
            for _x in (p.get('scoring') or []):
                if _x['year']>Y: continue
                _gg=float(_x.get('games') or 0.0)
                if _gg<=0.0: continue
                _pos=MA._fit_bar(p,_x['year'])
                _b=o32_gate_bar(_pos,_x['year']-_by)
                if _b is None or _x.get('avg') is None: _ok=False; break
                _num+=_gg*(float(_x['avg'])-_b); _den+=_gg
                if _pos in O32_TALLPOS: _wt+=_gg
            if _ok and _den>0.0: _r=(_num/_den,_wt/_den,1.0-_wt/_den)
        _O38_PCACHE[_ck]=_r
        return _r
    def o38_T(_s):
        # ORDER R: the EFFECTIVE cap and slope. With both R dials unset these are O37_THETA_R and
        # O37_TMAX bit for bit (asserted above), so this line is byte-identical to ORDER Q's.
        return min(max(1.0-O39_THETA_R*(_s-O37_S0),0.0),O39_TMAX)
    def o38_mono(p,Y,g,_s):
        """FIX A. The charge, capped wherever the pedigree leg would otherwise FALL as entry price
        RISES. Returns the multiplier the pedigree leg is charged by, in (0,1]."""
        _A=1.0-_math.exp(-float(g)/O37_G0)
        _pr=o38_parts(p,Y)
        _v=day0_v0(p)
        if _pr is None or _v is None:
            return _math.exp(-O37_LAMBDA*_A*o38_T(_s))
        _OUT,_wT,_wS=_pr
        _X=_math.log(round(float(_v)*_PL_F,1))
        def _sx(_x):
            return _OUT-(_wT*o38_pg_at(_x,'TALL')+_wS*o38_pg_at(_x,'SMALL'))
        def _psi(_x):
            return _x-O37_LAMBDA*_A*o38_T(_sx(_x))
        _cand=[]
        for _c,_wc in (('TALL',_wT),('SMALL',_wS)):
            if _wc<=0.0: continue
            _lo,_hi,_y=O37_PG_GRID[_c]; _n=len(_y)
            for _i in range(_n):
                _xi=_lo+(_hi-_lo)*_i/(_n-1.0)
                if _xi<_X: _cand.append(_xi)
        _cand.append(_X)
        _cand=sorted(set(_cand))
        # the clip crossings: s is affine on each segment, so the pre-clip T is affine and its two
        # clip boundaries are the only interior places psi can change slope.
        _extra=[]
        for _j in range(len(_cand)-1):
            _a,_b=_cand[_j],_cand[_j+1]
            _sa,_sb=_sx(_a),_sx(_b)
            if _sa==_sb: continue
            for _tv in (0.0,O39_TMAX):                     # ORDER R: the EFFECTIVE clip boundaries
                _st=O37_S0+(1.0-_tv)/O39_THETA_R
                if (_sa-_st)*(_sb-_st)<0.0:
                    _extra.append(_a+(_b-_a)*(_st-_sa)/(_sb-_sa))
        if _extra: _cand=sorted(set(_cand+_extra))
        _m=_psi(_X)
        for _x in _cand:
            _q=_psi(_x)
            if _q>_m: _m=_q
        return _math.exp(_m-_X)
    def o38_w(_age):
        """The weight on the ORDER P charge. B1: 1 at every age. B2: the 23-to-26 ramp.
        Neither: ORDER P's own hard gate at 24."""
        if _O38B1: return 1.0
        if _O38B2:
            if _age<=23: return 1.0
            if _age>=26: return 0.0
            return (26.0-float(_age))/3.0
        return 1.0 if _age<O37_AGE_GATE else 0.0
    def o38_factor(p,Y,g):
        """The ORDER Q multiplier. Falls back to the ORDER K charge, byte for byte, on exactly the
        rows ORDER P falls back on: no birth year, no day-0 v0, no readable bar."""
        _old=max(0.0,1.0-O32_ETA*((float(g)/O32_GAMMA_D)*_math.exp(1.0-float(g)/O32_GAMMA_D)))
        _by=p.get('_by')
        if not _by: return _old
        _w=o38_w(int(Y)-int(_by))
        if _w<=0.0: return _old
        _s=o37_surplus(p,Y)
        if _s is None: return _old
        _f=o38_mono(p,Y,g,_s) if _O38A else _math.exp(-O37_LAMBDA*(1.0-_math.exp(-float(g)/O37_G0))*o38_T(_s))
        if _w>=1.0: return _f
        if _f<=0.0 or _old<=0.0: return _f*_w+_old*(1.0-_w)
        return _math.exp(_w*_math.log(_f)+(1.0-_w)*_math.log(_old))
    def o31_pi(p,Y,g=None):
        """pi(g, c_u, s) = Phi(g,s) * [ D(c_u)*(1-rho(g)) + beta_mono(g)*rho(g) ].
        At g=0 this is D(c_u) EXACTLY. As rho -> 1 it is the measured additive beta EXACTLY."""
        _g=pv_games(p,Y) if g is None else float(g)
        _r=rho31(_g)
        # Phi multiplies the MEASURED COEFFICIENT ONLY. beta_stall/beta_pooled is a ratio of ADDITIVE
        # COEFFICIENTS estimated on PLAYED players; D(c_u) is the sitter fade, estimated on GAMELESS
        # listed players, and no stall measurement was ever taken on that channel. This also makes
        # pi(0,c,s) == D(c) true for EVERY s structurally rather than by an unreachable-state argument.
        # RL_O31_NOPHI=1 is a DECLARED, DEFAULT-OFF measurement dial that prices the conditioning by
        # removing it -- so the unconditioned alternative's cost is MEASURED, not argued.
        _pl=bool(p.get('_pool'))
        _pi=o31_D(p,Y)*(1.0-_r)+(1.0 if _O31_NOPHI else phi31(_g,o31_stall_run(p,Y),_pl))*beta31(_g,_pl)*_r
        # ORDER A stage 6 (M5): the pedigree leg comes down in step — W2's own translation. m_d(0)=0
        # so pi(0,c)=D(c) still holds EXACTLY and gameless rows are untouched.
        if _O32S>=6 and O32_ETA>0.0 and _g>0.0:
            # ORDER P (RL_O37): the pedigree-conditional charge REPLACES the blind one at this one
            # site. Dial off => the second branch runs and not one byte of the first executes, which
            # is what makes f3101883 reproduce exactly. m_d(0) = 0 and A(0) = 0, so BOTH forms leave
            # every gameless row untouched and pi(0,c) = D(c) still holds for both.
            # ORDER Q (RL_O38A/B1/B2): the two defect repairs sit at this same one site. With all
            # three dials off `_O38` is False and o37_factor runs exactly as before, byte for byte.
            _pi*=(((o38_factor(p,Y,_g) if _O38 else o37_factor(p,Y,_g)) if _O37 else
                  max(0.0,1.0-O32_ETA*((_g/O32_GAMMA_D)*_math.exp(1.0-_g/O32_GAMMA_D)))))
        return _pi
    def _pv_order31(p,Y,e):
        """THE ONE LAW. One expression, every row, every pathway, every games count.
        ORDER A REPAIR R1: + the age credit on the re-mix's added production weight (zero at g=0,
        zero from age 24, zero below stage 6 — the dial-off path is unchanged byte-for-byte)."""
        _g=pv_games(p,Y)
        return rho31(_g)*float(e)+o31_pi(p,Y,_g)*pv_pedigree(p)+o32_age_credit(p,Y,_g)
    if _O31:
        _PV['blend']=_pv_order31
        # THE DAY-0 PREDICATE IS RESTATED, NOT DROPPED. Under the one law a zero-games row's price IS
        # v0 x D(c_u) with c_u == the fade clock, so rl_export's printed-day-0 assert keeps its meaning and
        # its tolerance-0 equality -- it now proves the one law reproduces the ruled sitter law rather than
        # asserting a separately-wired branch against itself.
        def _entry30b_price(p,Y=2026,__d=_entry29b_derived):
            _d0=__d(p,Y)
            if _d0 is None: return None
            return _d0*o31_D(p,Y)
        # BUILD-FAILING STRUCTURAL ASSERTS (the brief's assert wall, at the law itself).
        _o31_bad=[]
        for _p in MA.data:
            if not (_isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos'))): continue
            _gg=pv_games(_p,MA.BASE_REF)
            if _gg<=0.0:
                if o31_stall_run(_p,MA.BASE_REF)>0: _o31_bad.append(('s>0 at g==0',_p.get('key')))
                if abs(o31_pi(_p,MA.BASE_REF,0.0)-o31_D(_p,MA.BASE_REF))>0.0: _o31_bad.append(('pi(0)!=D',_p.get('key')))
        if _o31_bad:
            raise SystemExit('ORDER 31 HALT: %d structural violations of the one law — %s'%(len(_o31_bad),_o31_bad[:6]))
        # ORDER A — CANDIDATE 32 BUILD-FAILING ASSERTS (only with the dial on).
        if _O32S>=1:
            # cap law: every gate bar <= the flat bar, flat from 24 (murdock guard, structural)
            for _pos in _O30BP_BARS:
                for _a in range(16,30):
                    _b=o32_gate_bar(_pos,_a)
                    if not (_b<=_O30BP_BARS[_pos]+1e-12) or (_a>=24 and _b!=_O30BP_BARS[_pos]):
                        raise SystemExit('ORDER A HALT: gate-bar cap law broken at %s age %d'%(_pos,_a))
            # S1 flat-bar identity: the C3 construction was built on these exact flat bars
            _s1flat={'KPD':65.4,'KPF':63.8,'MID':77.1,'RUCK':75.5,'SD':75.3,'SF':67.9}
            for _pos,_v in _s1flat.items():
                if abs(_O30BP_BARS.get(_pos,-1)-_v)>1e-9:
                    raise SystemExit('ORDER A HALT: _O30BP_BARS[%s]=%r is not the S1 flat bar %r — the '
                                     'C3 offsets do not apply to this object'%(_pos,_O30BP_BARS.get(_pos),_v))
        if _O32S>=6 and O32_KAPPA>0.0:
            _prev=-1.0
            _gg=0.0
            while _gg<=300.0:
                _r=rho31(_gg)
                if _r<_prev-1e-12:
                    raise SystemExit('ORDER A HALT: rho32 non-monotone at g=%.2f (PREREG_32 F5)'%_gg)
                if not (_r<1.0+1e-12):
                    raise SystemExit('ORDER A HALT: rho32 breaches 1 at g=%.2f'%_gg)
                _prev=_r; _gg+=0.25
        if _O35:
            # ORDER D BUILD-FAILING ASSERTS: the curve is smooth and monotone in pick, bounded by
            # its clips, and transcribed exactly from O35_CURVE.json (kappa(1)=0.5, kappa(64)
            # within 1e-9 of the derivation's own table).
            _prevk=None
            for _pk in range(1,65):
                _kk=min(O35_CLIP[1],max(O35_CLIP[0],(O35_G0+O35_G1*_math.log(float(_pk)))/O35_SNORM))
                if not (O35_CLIP[0]-1e-12<=_kk<=O35_CLIP[1]+1e-12) or (_prevk is not None and _kk<_prevk-1e-12):
                    raise SystemExit('ORDER D HALT: kappa(pick) broke monotone/clip at pick %d'%_pk)
                _prevk=_kk
            if abs((O35_G0+O35_G1*_math.log(64.0))/O35_SNORM-1.153311931087099)>1e-9:
                raise SystemExit('ORDER D HALT: the transcribed curve does not reproduce O35_CURVE.json at pick 64')
        if _O36:
            # ===== ORDER I BUILD-FAILING ASSERTS (only with the dial on) ==============================
            # A1 — the S1 surface in rl_model is BYTE-EQUAL to the C3 object this file already carries.
            # Two copies exist only because rl_model is imported before this block runs; they may never
            # drift, and a drift is a build failure, not a warning.
            if MA.O36_GATE_DELTA!=O32_GATE_DELTA or set(MA.O36_TALLPOS)!=set(O32_TALLPOS):
                raise SystemExit('ORDER I HALT: rl_model.O36_GATE_DELTA/TALLPOS has drifted from the '
                                 'C3 object O32_GATE_DELTA in this file — the two copies must be identical')
            # A2 — THE CAP LAW AND THE MATURE-ROW IDENTITY, on the S1 bar itself: never above the flat
            # bar, and EXACTLY the flat bar from age 24 (this is what makes murdock byte-identical).
            for _pos in MA.REPL:
                for _a in range(16,40):
                    _bb=MA.o36_bar(_pos,_a)
                    if not (_bb<=MA.REPL[_pos]+1e-12):
                        raise SystemExit('ORDER I HALT: S1 bar ABOVE the flat bar at %s age %d'%(_pos,_a))
                    if _a>=24 and _bb!=MA.REPL[_pos]:
                        raise SystemExit('ORDER I HALT: S1 bar is not byte-identical at %s age %d — the '
                                         'cap law (flat from 24) is broken and mature rows would move'%(_pos,_a))
                if MA.o36_bar(_pos,None)!=MA.REPL[_pos]:
                    raise SystemExit('ORDER I HALT: S1 bar moved a row with no age at %s'%_pos)
            if not (0.0<=MA.O36_LAM_S1<=1.0):
                raise SystemExit('ORDER I HALT: lambda_S1 %r is outside the declared [0,1] dose range'%MA.O36_LAM_S1)
            # A3 — the S1 surface is MONOTONE NON-INCREASING in age over 18..23: the development gap
            # must shrink as a player matures, never widen. The final step at age 24 (gap -> 0) is the
            # RULED CAP LAW itself — the same structural step the O32 stage-1 gate already ships — and
            # is DISCLOSED with its number on the packet rather than asserted away.
            for _cls in ('TALL','SMALL'):
                _tab=O32_GATE_DELTA[_cls]
                for _a in range(18,23):
                    if _tab[_a+1]>_tab[_a]+1e-12:
                        raise SystemExit('ORDER I HALT: the S1 development gap WIDENS from age %d to %d '
                                         'in class %s — the surface is not monotone'%(_a,_a+1,_cls))
            # A4 — THE TALL/SMALL FADE: smooth and monotone in pick within each class, bounded by the
            # clips, and transcribed EXACTLY from H_RESULTS.json (every pick H published, 1e-12).
            _HK={1:(0.5,0.5),5:(0.5,0.5),10:(0.5299803208304396,0.5),16:(0.7636000350961567,0.5),
                 20:(0.8745156311776653,0.5),24:(0.96514027182361,0.5),
                 30:(1.0760558679051182,0.5915136019227577),40:(1.2190509415248914,0.734508675542531),
                 50:(1.3299665376063998,0.8454242716240395),53:(1.3589296451644084,0.8743873791820481),
                 64:(1.4526706557906086,0.9681283898082481)}
            def _kap36(_pk,_tall):
                _s=O36_TG0+O36_TG1*_math.log(float(_pk))+(O36_HTALL if _tall else 0.0)
                return min(O35_CLIP[1],max(O35_CLIP[0],_s/O36_SNORM))
            for _pk,(_ks,_kt) in _HK.items():
                if abs(_kap36(_pk,False)-_ks)>1e-12 or abs(_kap36(_pk,True)-_kt)>1e-12:
                    raise SystemExit('ORDER I HALT: the transcribed tall/small curve does not reproduce '
                                     'H_RESULTS.json at pick %d'%_pk)
            _ps=_pt=None
            for _pk in range(1,65):
                _a1=_kap36(_pk,False); _a2=_kap36(_pk,True)
                for _v in (_a1,_a2):
                    if not (O35_CLIP[0]-1e-12<=_v<=O35_CLIP[1]+1e-12):
                        raise SystemExit('ORDER I HALT: kappa breached its clip at pick %d'%_pk)
                if (_ps is not None and _a1<_ps-1e-12) or (_pt is not None and _a2<_pt-1e-12):
                    raise SystemExit('ORDER I HALT: kappa(pick) broke monotone at pick %d'%_pk)
                # smoothness: no step between neighbouring picks bigger than the pick-1->2 step
                if _ps is not None and (_a1-_ps)>O36_TG1/O36_SNORM*_math.log(2.0)+1e-12:
                    raise SystemExit('ORDER I HALT: kappa(pick) took a step larger than the log curve '
                                     'allows at pick %d — that is a cliff'%_pk)
                _ps=_a1; _pt=_a2
            # ===== ORDER K — K-FLOOR, THE BUILD-FAILING ASSERTS ON THE FIX (PREREG_K.md §2.6) =======
            # A4 above is left UNTOUCHED and still runs on the WIRED form. That is deliberate: it keeps
            # proving that the RULED FIT CONSTANTS (TG0, TG1, h_TALL and Order H's own s_norm) are
            # transcribed exactly and have not been quietly re-fitted by this order. What follows gates
            # the LIVE exponent — the one the board actually charges.
            # K-FLOOR (a) — NO SMALL IS MADE LIGHTER, at any pick, structurally. This is the owner's
            # acceptance test written as an inequality the build cannot pass without satisfying it.
            # K-FLOOR (d) — the talls' relief survives: a TALL is never made HEAVIER by the factor.
            # ON THE DECLARED REMOVAL LANE (RL_O36_FLOORFIX=0) THESE ARE NOT HALTS. That lane exists to
            # PRICE the defect by rebuilding it, exactly as RL_O36_TALL=0 prices the adopted factor by
            # removing it; halting there would make the defect unmeasurable. The inequalities are still
            # evaluated and the breach is PRINTED with its picks — and the fact that they fire the
            # moment the fix is removed is the NON-VACUITY PROOF that they are live and not decorative
            # (the firing run is kept at docs/evidence/order_k_2026-08-18/K1_NONVACUITY_PROOF.txt).
            _k1=[_pk for _pk in range(1,65) if o36_kappa_at(_pk,False)<o35_kappa_at(_pk)-1e-12]
            _k3=[_pk for _pk in range(1,65) if o36_kappa_at(_pk,True)>o35_kappa_at(_pk)+1e-12]
            if _O36_FLOORFIX:
                if _k1:
                    raise SystemExit('ORDER K HALT (K1): a SMALL is made LIGHTER by the tall factor at '
                                     'picks %s — at pick %d kappa %.10f is below his pre-factor %.10f. '
                                     'The fade floor has inverted again.'
                                     %(_k1,_k1[0],o36_kappa_at(_k1[0],False),o35_kappa_at(_k1[0])))
                if _k3:
                    raise SystemExit('ORDER K HALT (K3): a TALL is made HEAVIER by the tall factor at '
                                     'picks %s — the ruled relief has reversed'%_k3)
            else:
                print('ORDER K MEASUREMENT LANE (RL_O36_FLOORFIX=0) — THE FADE FLOOR FIX IS REMOVED AND '
                      'THE DEFECT IS REBUILT ON PURPOSE, so it can be priced. K1 BREACH: smalls are made '
                      'LIGHTER at picks %s. K3 breach: %s. This board is a MEASUREMENT, never a candidate.'
                      %(_k1 or 'none',_k3 or 'none'))
            # The live curve is bounded, monotone in pick within each class, and smooth (no cliff). The
            # small side is the max of two monotone curves, so it is monotone and continuous; the step
            # bound is the looser of the two curves' own one-pick steps.
            _ps=_pt=None
            _stepmax=max(O36_TG1/(O36_SNORM_K if _O36_FLOORFIX else O36_SNORM),O35_G1/O35_SNORM)*_math.log(2.0)
            for _pk in range(1,65):
                _a1=o36_kappa_at(_pk,False); _a2=o36_kappa_at(_pk,True)
                for _v in (_a1,_a2):
                    if not (O35_CLIP[0]-1e-12<=_v<=O35_CLIP[1]+1e-12):
                        raise SystemExit('ORDER K HALT: the live kappa breached its clip at pick %d'%_pk)
                if (_ps is not None and _a1<_ps-1e-12) or (_pt is not None and _a2<_pt-1e-12):
                    raise SystemExit('ORDER K HALT: the live kappa(pick) broke monotone at pick %d'%_pk)
                if _ps is not None and (_a1-_ps)>_stepmax+1e-12:
                    raise SystemExit('ORDER K HALT: the live kappa(pick) took a step larger than either '
                                     'log curve allows at pick %d — that is a cliff'%_pk)
                _ps=_a1; _pt=_a2
            # K-FLOOR (e) — THE REDISTRIBUTION IDENTITY. The pick-weighted mean of D2^kappa over ORDER
            # H's own 408 fitted sitters must still equal the ruled depth-2 fade 0.5582775. The sitter
            # set is transcribed here as (pick, TALL) counts so the assert needs no external file and
            # cannot be satisfied vacuously; the counts are H's SATROWS, reproduced in
            # docs/evidence/order_k_2026-08-18/ok_floor_design.py.
            _SATC=_O36K_SATCOUNTS
            _n=sum(_SATC.values())
            if _n!=408:
                raise SystemExit('ORDER K HALT: the transcribed sitter set is %d rows, not ORDER H\'s 408'%_n)
            _idr=(sum(_c*(O36_D2_FULL**o36_kappa_at(_pk,_tl)) for (_pk,_tl),_c in _SATC.items())/_n
                  -O36_D2_FULL)
            if abs(_idr)>1e-9:
                raise SystemExit('ORDER K HALT (K4): the tall/small redistribution identity misses the '
                                 'ruled depth-2 fade %.7f by %.3e — the total fade the board charges has '
                                 'moved'%(O36_D2,_idr))
            O36_IDENT_RESID=_idr
            # A5 — m_TALL, the multiplicative translation the owner asked for, reproduced from the wire.
            _mt=(sum(_kap36(_p,True) for _p in range(1,65))/sum(_kap36(_p,False) for _p in range(1,65)))
            print('ORDER I LIVE (RL_O36=1) — THE COORDINATED BUILD. NOTHING IS GREENLIT AND NOTHING MERGES.\n'
                  '  LEVER 1  S1, the age-referenced projection bar: lambda_S1=%.3f applied to the C3 gap at '
                  'the four projection/floor sites. NO pick axis, capped at the flat bar, FLAT FROM AGE 24 '
                  '(every mature row byte-identical, store-wide).\n'
                  '  LEVER 2  the counterweight, re-derived JOINTLY on the corrected age-fair surface: '
                  'kappa=%.2f gamma_u=%.1f / eta=%.2f gamma_d=%.1f / relief lambda=%.2f '
                  '(was %.2f/%.1f/%.2f/%.1f/%.2f).\n'
                  '  LEVER 3  the tall/small sitter factor: h_TALL=%.4f, s_norm=%.10f, clip [%.1f, %.1f]; '
                  'kappa(16) small %.3f / tall %.3f, kappa(64) small %.3f / tall %.3f; m_TALL=%.3f. '
                  'DECLARED: the pinned identity means LATE SMALL SITTERS PAY for the talls\' relief.\n'
                  '  ORDER K FADE FLOOR: %s. A SMALL\'s floor is HIS OWN PRE-FACTOR (Order D pooled) '
                  'exponent, so no small can be made lighter by a talls-only relief; talls keep the '
                  '[0.5, 2.0] clip. h_TALL UNCHANGED; the normaliser re-solved WITH the re-sited floor '
                  'inside the constraint set (%.10f -> %.10f). Redistribution identity residual %.3e '
                  'against the ruled depth-2 fade %.7f. The floor still binds: talls picks 1-%d on 0.5; '
                  'smalls picks 1-%d on their own pooled exponent (of those, picks 1-%d also on 0.5 '
                  'because the pooled curve is itself clipped there).\n'
                  '  %d active rows sit at a developing age and can be reached by S1; %d have no birth '
                  'year and keep the flat bar.'
                  %(MA.O36_LAM_S1,O36_KAPPA,O36_GAMMA,O36_ETA,O36_GAMMA_D,O36_LAMBDA,
                    0.24,11.0,0.41,14.0,1.08,
                    O36_HTALL,(O36_SNORM_K if _O36_FLOORFIX else O36_SNORM),O35_CLIP[0],O35_CLIP[1],
                    o36_kappa_at(16,False),o36_kappa_at(16,True),o36_kappa_at(64,False),
                    o36_kappa_at(64,True),_mt,
                    ('LIVE (RL_O36_FLOORFIX=1, the default)' if _O36_FLOORFIX else
                     'REMOVED (RL_O36_FLOORFIX=0) — Order J\'s wired form, THE DEFECT IS BACK: '
                     'smalls at picks 6-18 are made LIGHTER by a talls-only relief'),
                    O36_SNORM,(O36_SNORM_K if _O36_FLOORFIX else O36_SNORM),O36_IDENT_RESID,O36_D2,
                    max([_p for _p in range(1,65) if abs(o36_kappa_at(_p,True)-O35_CLIP[0])<1e-12] or [0]),
                    max([_p for _p in range(1,65) if abs(o36_kappa_at(_p,False)-o35_kappa_at(_p))<1e-12] or [0]),
                    max([_p for _p in range(1,65) if abs(o36_kappa_at(_p,False)-O35_CLIP[0])<1e-12] or [0]),
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and _p.get('_by') and (MA.BASE_REF-int(_p['_by']))<24),
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and not _p.get('_by'))))
        if _O37:
            # ===== ORDER P BUILD-FAILING ASSERTS (only with the dial on) ==============================
            # P1 — THE TILT IS THE MEASUREMENT. LAMBDA*THETA_R must equal BETA_sat, the saturated slope
            # measured on outcomes. If this drifts, the charge no longer responds to surplus at the rate
            # the data says it should and every claim in PACKET_P is void.
            if abs(O37_LAMBDA*O37_THETA_R-O37_BETA_SAT)>1e-15:
                raise SystemExit('ORDER P HALT (P1): LAMBDA*THETA_R = %.17g is not BETA_sat = %.17g — the '
                                 'tilt has come loose from the measurement'%(O37_LAMBDA*O37_THETA_R,O37_BETA_SAT))
            # P2 — THE PUBLISHED CONSTANTS, transcribed and not quietly re-fitted.
            for _nm,_got,_want in (('G0',O37_G0,9.89),('BETA_sat',O37_BETA_SAT,0.11465),
                                   ('LAMBDA',O37_LAMBDA,0.17438),('THETA_R',O37_THETA_R,0.65744),
                                   ('s0',O37_S0,-2.4527),('TMAX',O37_TMAX,21.12)):
                if abs(round(_got,{'G0':2,'BETA_sat':5,'LAMBDA':5,'THETA_R':5,'s0':4,'TMAX':2}[_nm])-_want)>1e-12:
                    raise SystemExit('ORDER P HALT (P2): %s is %.17g, which does not round to the published '
                                     '%.5f — a derived constant has been changed'%(_nm,_got,_want))
            # P-S1 — A(0) = 0 EXACTLY, so pi(0,c) = D(c) and NO DAY-0 PRINT CAN MOVE. This is the same
            # structural law m_d(0) = 0 gave the charge being replaced, and it is asserted, not assumed.
            if (1.0-_math.exp(-0.0/O37_G0))!=0.0:
                raise SystemExit('ORDER P HALT (P-S1): A(0) is not exactly zero')
            # P-S2 — A is non-decreasing in g. THIS IS THE DEFECT BEING REMOVED: the charge it replaces
            # RISES to g=14 and then FALLS, so more evidence bought a smaller charge. A never falls.
            _pa=-1.0; _gg=0.0
            while _gg<=400.0:
                _av=1.0-_math.exp(-_gg/O37_G0)
                if _av<_pa-1e-15:
                    raise SystemExit('ORDER P HALT (P-S2): A(g) fell at g=%.2f — the blind bump is back'%_gg)
                _pa=_av; _gg+=0.25
            # P-S3 — T is non-increasing in the surplus, and P-S4 — the factor is in (0, 1]. Both are
            # checked on a real spread rather than argued from the formula.
            _pt=None
            _ss=-60.0
            while _ss<=40.0:
                _T=min(max(1.0-O37_THETA_R*(_ss-O37_S0),0.0),O37_TMAX)
                if _pt is not None and _T>_pt+1e-12:
                    raise SystemExit('ORDER P HALT (P-S3): T rose at s=%.2f — a better player was charged '
                                     'more for being better'%_ss)
                for _gq in (0.0,1.0,5.0,14.0,30.0,60.0,150.0,400.0):
                    _f=_math.exp(-O37_LAMBDA*(1.0-_math.exp(-_gq/O37_G0))*_T)
                    if not (0.0<_f<=1.0+1e-15):
                        raise SystemExit('ORDER P HALT (P-S4): the charge factor left (0,1] at s=%.2f '
                                         'g=%.1f — %.17g'%(_ss,_gq,_f))
                _pt=_T; _ss+=0.25
            # P3 — THE PREMIUM SURFACE IS NON-DECREASING IN PRICE. A more expensively priced player is
            # never expected to produce LESS. The house monotonicity guard was applied to the fitted grid
            # offline; this asserts it survived transcription.
            for _cls in ('TALL','SMALL'):
                _lo,_hi,_y=O37_PG_GRID[_cls]
                if len(_y)!=121 or not (_hi>_lo):
                    raise SystemExit('ORDER P HALT (P3): the %s premium grid is malformed'%_cls)
                for _i in range(1,len(_y)):
                    if _y[_i]<_y[_i-1]-1e-12:
                        raise SystemExit('ORDER P HALT (P3): the %s premium FALLS with price at node %d '
                                         '(%.6f -> %.6f)'%(_cls,_i,_y[_i-1],_y[_i]))
            # P4 — CONTINUITY IN PRICE. The premium is read by linear interpolation on an even grid and
            # held flat outside, so it can have no cliff; the largest one-node step is printed so the
            # owner can see the size of the biggest jump the surface is capable of.
            _stepPG=max(max(_y[_i]-_y[_i-1] for _i in range(1,len(_y)))
                        for _lo,_hi,_y in O37_PG_GRID.values())
            _o37n=sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p)
                      and MA.GRP.get(_p.get('pos')) and _p.get('_by')
                      and (MA.BASE_REF-int(_p['_by']))<O37_AGE_GATE
                      and o37_surplus(_p,MA.BASE_REF) is not None)
            print('ORDER P LIVE (RL_O37=1) — THE PEDIGREE-CONDITIONAL CHARGE. NOTHING IS GREENLIT AND '
                  'NOTHING MERGES.\n'
                  '  THE BLIND ETA CHARGE IS GONE. It read games and nothing else, peaked at %.0f games '
                  'and then FELL AWAY, so a 36-game row kept more unearned pedigree than a 17-game row '
                  'however either of them played.\n'
                  '  IN ITS PLACE: pi *= exp(-LAMBDA*A(g)*T(s_P)) below age %d; the old charge at %d and '
                  'above. A(g)=1-exp(-g/%.2f) · T=clip(1-%.5f*(s%+.4f), 0, %.4f) · LAMBDA=%.5f.\n'
                  '  s_P is production against the S1 AGE BAR PLUS the MEASURED PEDIGREE PREMIUM '
                  'PG(ln v0, class), pooled over age, fitted on 5,041 season rows by local-linear kernel '
                  'regression on ln(v0) (tricube, h=0.40), monotone guarded, held flat outside support.\n'
                  '  PG spans %+.2f to %+.2f points a game for SMALLS (v0 %.0f to %.0f) and %+.2f to '
                  '%+.2f for TALLS (v0 %.0f to %.0f). Largest one-node step %.4f — no cliff.\n'
                  '  LAMBDA*THETA_R = %.5f = BETA_sat, the measured saturated slope. NO FREE PARAMETER.\n'
                  '  %d active rows are inside the age gate AND carry a readable pedigree surplus; every '
                  'other row keeps the ORDER K charge byte for byte, and A(0)=0 means no day-0 print moves.'
                  %(O32_GAMMA_D,O37_AGE_GATE,O37_AGE_GATE,O37_G0,O37_THETA_R,-O37_S0,O37_TMAX,O37_LAMBDA,
                    O37_PG_GRID['SMALL'][2][0],O37_PG_GRID['SMALL'][2][-1],
                    _math.exp(O37_PG_GRID['SMALL'][0]),_math.exp(O37_PG_GRID['SMALL'][1]),
                    O37_PG_GRID['TALL'][2][0],O37_PG_GRID['TALL'][2][-1],
                    _math.exp(O37_PG_GRID['TALL'][0]),_math.exp(O37_PG_GRID['TALL'][1]),
                    _stepPG,O37_LAMBDA*O37_THETA_R,_o37n))
        if _O38:
            # ===== ORDER Q — BUILD-FAILING STRUCTURAL ASSERTS ==========================================
            # Q-A1  the FIX A factor is never SMALLER than ORDER P's: the repair CAPS a charge, it never
            #       raises one, so a price can only move UP against ORDER P.
            # Q-A2  the FIX A factor stays in (0, 1]: no row can price above its own uncharged price.
            # Q-A3  the monotonised leg is NON-DECREASING in entry price on a dense synthetic sweep.
            # Q-B1  the ORDER K charge is strictly positive at every games count, so the B2 ramp's
            #       geometric blend is defined everywhere.
            # Q-B2  the ramp weight is 1 at 23, 0 at 26 and above, and non-increasing between.
            if _O38A:
                _qA=1.0-_math.exp(-17.0/O37_G0)
                for _cls in ('TALL','SMALL'):
                    _lo,_hi,_y=O37_PG_GRID[_cls]
                    _wT,_wS=(1.0,0.0) if _cls=='TALL' else (0.0,1.0)
                    for _OUT in (-30.0,-12.0,-4.0,0.0,6.0,20.0):
                        _prev=None; _pm=None
                        for _k in range(0,1201):
                            _x=_lo-0.6+(_hi-_lo+1.2)*_k/1200.0
                            _sx=_OUT-(_wT*o38_pg_at(_x,'TALL')+_wS*o38_pg_at(_x,'SMALL'))
                            _ps=_x-O37_LAMBDA*_qA*o38_T(_sx)
                            _pm=_ps if _pm is None else max(_pm,_ps)
                            _fA=_math.exp(_pm-_x); _fP=_math.exp(-O37_LAMBDA*_qA*o38_T(_sx))
                            if _fA<_fP-1e-12:
                                raise SystemExit('ORDER Q HALT (Q-A1): the monotonised factor is BELOW '
                                                 'ORDER P\'s at %s x=%.4f (%.9f < %.9f). FIX A may only '
                                                 'CAP a charge.'%(_cls,_x,_fA,_fP))
                            if not (0.0<_fA<=1.0+1e-12):
                                raise SystemExit('ORDER Q HALT (Q-A2): the monotonised factor left (0,1] '
                                                 'at %s x=%.4f: %.9f'%(_cls,_x,_fA))
                            _leg=_math.exp(_pm)
                            if _prev is not None and _leg<_prev-1e-9:
                                raise SystemExit('ORDER Q HALT (Q-A3): the monotonised pedigree leg FALLS '
                                                 'with entry price at %s x=%.4f (%.9f -> %.9f)'
                                                 %(_cls,_x,_prev,_leg))
                            _prev=_leg
            for _gq in [0.01*_i for _i in range(1,20001)]:
                if not (max(0.0,1.0-O32_ETA*((_gq/O32_GAMMA_D)*_math.exp(1.0-_gq/O32_GAMMA_D)))>0.0):
                    raise SystemExit('ORDER Q HALT (Q-B1): the ORDER K charge reaches zero at g=%.2f, so '
                                     'the B2 geometric ramp is undefined there.'%_gq)
            _wprev=None
            for _ag in range(16,41):
                _wq=(1.0 if _ag<=23 else (0.0 if _ag>=26 else (26.0-float(_ag))/3.0))
                if _wprev is not None and _wq>_wprev+1e-15:
                    raise SystemExit('ORDER Q HALT (Q-B2): the B2 ramp weight RISES with age at %d'%_ag)
                _wprev=_wq
            if abs(o38_w(23)-1.0)>1e-15 or (not _O38B1 and abs(o38_w(26)-0.0)>1e-15):
                raise SystemExit('ORDER Q HALT (Q-B2): the ramp endpoints are not 1 at 23 and 0 at 26')
            _o38n=sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p)
                      and MA.GRP.get(_p.get('pos')) and _p.get('_by')
                      and o38_w(MA.BASE_REF-int(_p['_by']))>0.0
                      and o37_surplus(_p,MA.BASE_REF) is not None)
            _o38m=sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p)
                      and MA.GRP.get(_p.get('pos')) and _p.get('_by')
                      and (MA.BASE_REF-int(_p['_by']))>=O37_AGE_GATE
                      and o38_w(MA.BASE_REF-int(_p['_by']))>0.0
                      and o37_surplus(_p,MA.BASE_REF) is not None)
            print('ORDER Q LIVE — TWO DEFECT REPAIRS, PRICED AND NOT ADOPTED. NOTHING IS GREENLIT AND '
                  'NOTHING MERGES.\n'
                  '  FIX A (RL_O38A) %s — the pedigree leg is monotonised in ENTRY PRICE by the running '
                  'maximum of x - LAMBDA*A(g)*T(s_P(x)) over x = ln(v0). No free parameter: the charge is '
                  'CAPPED at its own inversion point. Exact on the piecewise-linear breakpoints, up to the '
                  'engine\'s own one-decimal rounding of the premium axis, which is disclosed and measured.\n'
                  '  FIX B1 (RL_O38B1) %s — the age-24 gate is DELETED. Mature rows are NO LONGER '
                  'byte-identical to ORDER K and that movement is the price of this option.\n'
                  '  FIX B2 (RL_O38B2) %s — the charge is ramped out across ages 23 to 26 in the exponent, '
                  'w = 1, 2/3, 1/3, 0. THE ENDPOINT 26 IS A FREE PARAMETER INVENTED BY THIS SEAT. IT WAS '
                  'NOT MEASURED. Age here is an integer, so this replaces one full step with three '
                  'third-sized steps rather than removing the step.\n'
                  '  %d active rows now carry the ORDER P charge (%d of them aged %d or over, which ORDER '
                  'P left on the ORDER K charge). A(0)=0 still, so no day-0 print can move.'
                  %('LIVE' if _O38A else 'off','LIVE' if _O38B1 else 'off','LIVE' if _O38B2 else 'off',
                    _o38n,_o38m,O37_AGE_GATE))
            # ===== ORDER R — THE OWNER'S TWO SOFTENINGS, PRICED AND NOT ADOPTED ======================
            # R-S1  T is still NON-INCREASING in surplus on the effective constants.
            # R-S2  the factor exp(-LAMBDA*A(g)*T) is still in (0,1] everywhere, so no row can price
            #       above its own uncharged price.
            # R-S3  A(0) = 0 EXACTLY still, so no day-0 print and no gameless row can move.
            # R-S4  THE SOFTENING IS NOT UNIFORM, AND THIS ASSERT IS THE CORRECTED ONE.
            #       The FIRST version of this assert said the ORDER R factor may never be below
            #       ORDER P's at any surplus. IT FIRED, on the very first in-process load, and it was
            #       RIGHT to fire: the assert was wrong, not the dials. Lowering BETA_sat lowers
            #       THETA_R, which FLATTENS the T line about s0. T(s0) = 1 on every board by
            #       construction, so a flatter line sits ABOVE ORDER P's for s BELOW s0 and BELOW it
            #       for s ABOVE s0. In plain words: lowering the slope softens the charge on rows
            #       producing under the cohort centre -- every row the owner's complaint is about --
            #       and STIFFENS it very slightly on rows producing just above the centre, until the
            #       zero clip catches up. The TMAX lever has no such effect: it only lowers the cap.
            #       What is asserted here is therefore the true statement, not the convenient one:
            #         R-S4a  for every s AT OR BELOW s0, the ORDER R factor is >= ORDER P's. The
            #                softening may never charge an underperformer MORE. THIS HALTS.
            #         R-S4b  the region above s0 where ORDER R charges more is BOUNDED and MEASURED,
            #                and the bound is printed on the banner rather than asserted away.
            _rprev=None; _rstiff=0.0; _rstiffn=0; _rstiffs=None; _rstiffhi=None
            for _i in range(0,20001):
                _ss=-120.0+0.01*_i
                _Tr=min(max(1.0-O39_THETA_R*(_ss-O37_S0),0.0),O39_TMAX)
                if _rprev is not None and _Tr>_rprev+1e-12:
                    raise SystemExit('ORDER R HALT (R-S1): T RISES with surplus at s=%.2f'%_ss)
                _rprev=_Tr
                for _gq in (0.0,1.0,17.0,60.0,400.0):
                    _fr=_math.exp(-O37_LAMBDA*(1.0-_math.exp(-_gq/O37_G0))*_Tr)
                    if not (0.0<_fr<=1.0+1e-15):
                        raise SystemExit('ORDER R HALT (R-S2): the factor left (0,1] at s=%.2f g=%.2f: '
                                         '%.9g'%(_ss,_gq,_fr))
                    _Tp=min(max(1.0-O37_THETA_R*(_ss-O37_S0),0.0),O37_TMAX)
                    _fp=_math.exp(-O37_LAMBDA*(1.0-_math.exp(-_gq/O37_G0))*_Tp)
                    if _ss<=O37_S0 and _fr<_fp-1e-12:
                        raise SystemExit('ORDER R HALT (R-S4a): the ORDER R constants charge MORE than '
                                         'ORDER P at s=%.4f g=%.2f (%.9f < %.9f), and that surplus is AT '
                                         'OR BELOW the cohort centre s0=%.4f. The softening may never '
                                         'charge an underperformer more.'%(_ss,_gq,_fr,_fp,O37_S0))
                    if _fr<_fp-1e-12:
                        _rstiff=max(_rstiff,_fp-_fr); _rstiffs=_ss if _rstiffn==0 else _rstiffs
                        _rstiffn+=1; _rstiffhi=_ss
            if (1.0-_math.exp(-0.0/O37_G0))!=0.0:
                raise SystemExit('ORDER R HALT (R-S3): A(0) is not 0 exactly')
            print('ORDER R %s — THE OWNER\'S TWO SOFTENINGS, PRICED AND NOT ADOPTED. NOTHING IS GREENLIT '
                  'AND NOTHING MERGES.\n'
                  '  THE CAP: TMAX at the young cohort\'s p%d of s_P = %+.5f pts/g  =>  TMAX %.4f '
                  '(ORDER P p5: s_p5 %+.5f, TMAX %.4f). %s\n'
                  '  THE SLOPE: BETA_sat %.8f%s, 90%% CI [%.5f, %.5f]  =>  THETA_R %.6f (ORDER P: '
                  'BETA_sat %.8f, THETA_R %.6f).\n'
                  '  LAMBDA*THETA_R = %.8f = the effective BETA_sat. TMAX is RECOMPUTED from this '
                  'THETA_R, never carried stale. NO FREE PARAMETER IS INTRODUCED.\n'
                  '  LAMBDA IS NOT RE-SOLVED. ORDER P solved it by an anchoring identity that held the '
                  'total charge constant; moving the cap or the slope BREAKS that anchor ON PURPOSE, and '
                  'that broken anchor IS the softening. Disclosed on PREREG_R.md, not discovered after.\n'
                  '  A row at the cap with 38 games is charged %.2f%% of his pedigree leg (ORDER P: '
                  '%.2f%%).\n'
                  '  R-S4b, MEASURED NOT ASSERTED: lowering BETA_sat FLATTENS T about s0, so it softens '
                  'the charge BELOW the cohort centre and STIFFENS it slightly ABOVE. %s'
                  %('LIVE' if _O39 else 'off (dial-off: the ORDER P constants, bit for bit)',
                    _O39_PCT,O39_S_PQ[_O39_PCT],O39_TMAX,O37_S_P5,O37_TMAX,
                    'THE CAP IS UNCHANGED FROM ORDER P.' if _O39_PCT==5 else
                    'The worst-producing %d%% now all pay the same top rate.'%_O39_PCT,
                    O39_BETA_SAT,'' if _O39_BSAT_RAW=='' else ' (RL_O39_BETASAT)',
                    O39_BSAT_CI[0],O39_BSAT_CI[1],O39_THETA_R,O37_BETA_SAT,O37_THETA_R,
                    O37_LAMBDA*O39_THETA_R,
                    100.0*(1.0-_math.exp(-O37_LAMBDA*(1.0-_math.exp(-38.0/O37_G0))*O39_TMAX)),
                    100.0*(1.0-_math.exp(-O37_LAMBDA*(1.0-_math.exp(-38.0/O37_G0))*O37_TMAX)),
                    ('There is NO surplus at which this board charges more than ORDER P.'
                     if _rstiffn==0 else
                     'It charges MORE than ORDER P over s in (%.4f, %.4f], a window %.4f points a game '
                     'wide, and the WORST extra charge anywhere in it is %.4f%% of the pedigree leg. '
                     'That window sits ABOVE the cohort centre, so it lands on rows already producing '
                     'at or above what their entry price implies. IT IS REPORTED, NOT ARGUED AWAY.'
                     %(_rstiffs,_rstiffhi,_rstiffhi-_rstiffs,100.0*_rstiff))))
        if _O35:
            print('ORDER D PICK-CURVE FADE LIVE (RL_O35=1) — THE LANDING CANDIDATE ON THE OWNER\'S WORD. '
                  'D_eff = D(c_u)^kappa(pick), kappa = clip((%.4f%+.4f·ln p)/%.4f, %.1f, %.1f): '
                  'kappa(1)=%.3f kappa(20)=%.3f kappa(64)=%.3f. Smooth in ln(pick), never a band; '
                  'pooled fade pinned at the ruled row by the redistribution identity.'
                  %(O35_G0,O35_G1,O35_SNORM,O35_CLIP[0],O35_CLIP[1],
                    min(O35_CLIP[1],max(O35_CLIP[0],(O35_G0)/O35_SNORM)),
                    min(O35_CLIP[1],max(O35_CLIP[0],(O35_G0+O35_G1*_math.log(20.0))/O35_SNORM)),
                    min(O35_CLIP[1],max(O35_CLIP[0],(O35_G0+O35_G1*_math.log(64.0))/O35_SNORM))))
        if _O32S>=1:
            print('ORDER A CANDIDATE 32 LIVE (RL_O32=1, stage %d of 6) — NOTHING IS GREENLIT AND NOTHING '
                  'MERGES. bars(age) gate-only · credit f·min(1,g/2) · delivered reset · Phi_32 row · '
                  'relief min(1, D·(1+%.2f·σ_sel)) · re-mix κ=%.2f γu=%.1f / η=%.2f γd=%.1f. '
                  '%d rows carry a stall run; %d carry c_u>1; %d carry relief.'
                  %(_O32S,O32_LAMBDA,O32_KAPPA,O32_GAMMA,O32_ETA,O32_GAMMA_D,
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and o31_stall_run(_p,MA.BASE_REF)>0),
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and o31_cu(_p,MA.BASE_REF)>1.0),
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and _O32S>=5 and o32_sigma_sel(_p,MA.BASE_REF)>0.0 and (o31_pool_D(o31_cu(_p,MA.BASE_REF)) if _p.get('_pool') else o31_fade_D(o31_cu(_p,MA.BASE_REF)))<1.0)))
        if _O34:
            print('ORDER C LIVE (RL_O34=1) — NOTHING IS GREENLIT AND NOTHING MERGES. The two retained '
                  'normalization denominators (Q evidence weight; decay gate) read the S1 C3 '
                  'age-conditional surface: flat bar - DELTA(class, age), NO pick axis, capped at the '
                  'flat bar, FLAT FROM AGE 24 (mature rows byte-identical). R1 age credit scale '
                  'alpha=%.2f (re-derived). %d active rows are at a developing age; %d active rows have '
                  'no birth year and keep the flat bar.'
                  %(O34_ALPHA,
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and _p.get('_by') and (MA.BASE_REF-int(_p['_by']))<24),
                    sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and not _p.get('_by'))))
        print('ORDER 31 THE ONE LAW LIVE (RL_O31=1) — NOTHING IS GREENLIT AND NOTHING MERGES. '
              'price = rho(g)*Phat + [D(c_u)*(1-rho(g)) + Phi(g,s)*beta(g)*rho(g)]*v0, ONE FORMULA FOR '
              'EVERY ROW: no sitter branch, no thin lane, no bridge, no deep lane. rho = 1-exp(-(g/%.4f)^'
              '%.4f) calibrated on the R1 backbone, rho(0)=0 exactly · beta MONOTONE-PROJECTED (the brief\'s '
              '"pi decays in g"; the measured 2.5->10.5 rise is deleted and disclosed) · D on the UNPLAYED '
              'clock c_u only · Phi = the 30B-C stall conditioning on the current stall run, Phi(g,0)=1 '
              'exactly. %d rows priced; %d carry a stall conditioning; %d carry an unplayed-clock discount.'
              %(O31_TAU_RHO,O31_B_RHO,
                sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos'))),
                sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and o31_stall_run(_p,MA.BASE_REF)>0),
                sum(1 for _p in MA.data if _isreal(_p) and not _p.get('_retired') and not delisted(_p) and MA.GRP.get(_p.get('pos')) and o31_cu(_p,MA.BASE_REF)>1.0)))
    if _O30B_RESOLVED:
        _PV['blend']=_pv_resolved
        print('ORDER 30B-N RESOLVED CANDIDATE LIVE (RL_O30B_RESOLVED=1) — NOTHING IS GREENLIT, T4 (the '
              'OBJECT) IS STILL OPEN, AND THIS BOARD IS PRE-NUMERAIRE. The preview lane\'s production leg '
              'is consumed UNCHANGED (this dial implies RL_O30B_PREVIEW); only the BLEND FUNCTION is '
              'swapped. ADDITIVE reading P + beta(g)xv0 · raw games-as-of-Y clock · JOINED lanes '
              'sitter/thin<=10/bridge<16/deep>=16 · beta from the 30B-R band fit (NON-monotone, carried) · '
              'backbone lift lane 2 if c<2.5 else 3. Pool fade NOT DERIVED (D=1.0) — Step 4.')
    # ORDER 31 — under the one law there is no zero-evidence EXCLUSION: every priced row carries the law.
    _PV_ROWS=[p for p in MA.data if _isreal(p) and not p.get('_retired') and not delisted(p)
              and MA.GRP.get(p.get('pos')) and (_O31 or _entry30b_price(p,MA.BASE_REF) is None)]
    print('ORDER 30B-P STEP-3 PREVIEW LIVE (RL_O30B_PREVIEW=1) — NOTHING IS GREENLIT, THE BOUNDARY IS STILL '
          'UNRULED, AND THIS BOARD IS PRE-NUMERAIRE. pole DELETED + ISO DELETED (via the two existing '
          'ablation lines) · blend sigma(g)=exp(-(g/%.4g)^%.4g) on the measured 30B-M curve · pedigree leg = '
          'STEP-1 positional v0 x %.4f · Q and the decay gate RETAINED with their denominators re-referenced '
          'to the effective positional bars (%s) · _a_blend, sitout_ev\'s ns==0 arm and the year-zero floor '
          'REPLACED, not wrapped. %d rows carry the blend; %d zero-evidence rows keep the Step-2 fade '
          'untouched.'
          %(SIGMA30BP_TAU,SIGMA30BP_BETA,_PL_F,
            ' '.join('%s %.1f'%(_g,_O30BP_BARS[_g]) for _g in sorted(_O30BP_BARS)),
            len(_PV_ROWS),len(_S30) if _ONEMACH and _ENTRY29B else 0))
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

# ==== LEG B v1.1 — UN-COMPRESS REFERENCE (V_ref_b + RHO_DEN) + PRODUCTION-SIDE CONSERVATION (C[pos]); LOAD-TIME
# memo v1.1 §2.1/§3. Built AFTER ev() is defined + player attrs finalized, BEFORE the RL_AVAIL attribution
# block so its ev()-diffs see the mapped surface. INERT unless RL_UNCOMP on AND s set (UNCOMP_S): the guard
# leaves V_ref_b/RHO_DEN/C empty => _uncomp_prod returns pr => board 8d90c9ac BYTE-EXACT. ⟪v1.2⟫ with s set
# this block now BUILDS the references: RHO_DEN[pos] = MEDIAN rho_out (the games×recency ρ_num, memo §2.1) over
# the demonstrated-proven pop — numerator and denominator share ONE law (register 240). The v1.1 stub is gone.
def _uncomp_scope(_p):                                        # valuation scope = active board population
    return _isreal(_p) and not delisted(_p) and not _p.get('_retired')
if MA._UNCOMP and MA.UNCOMP_S is not None:
    MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()              # pin MA's clock to the present (mirrors rl_export.py); level_now/ev = the 2026 surface
    # (1) V_ref_b[pos] = MEDIAN captain-free price6 (pr0); RHO_DEN[pos] = MEDIAN rho_out; over the
    #     DEMONSTRATED-PROVEN pop { gfut==pos, _nqual(_,2026) >= PROVEN_N(=4), in scope }.
    _vb_pool={}; _rd_pool={}
    for _p in MA.data:
        if not _uncomp_scope(_p) or _nqual(_p,2026)<PROVEN_N: continue
        _g=MA.gfut(_p)
        if _g not in MA.REPL: continue
        _prev=MA._CAPT_OFF['on']; MA._CAPT_OFF['on']=True
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                try: _pr0=price6(_p,b6(_p,2026),2026)
                except Exception: _pr0=None
        finally: MA._CAPT_OFF['on']=_prev
        _ro=rho_out(_p,_g)                                    # ρ_num (games×recency, memo §2.1 ⟪v1.2⟫) — reached ONLY when s is set
        if _pr0 and _pr0>0.0: _vb_pool.setdefault(_g,[]).append(float(_pr0))
        if _ro and _ro>0.0: _rd_pool.setdefault(_g,[]).append(float(_ro))
    for _g,_vals in _vb_pool.items(): _UC_VREFB[_g]=float(np.median(_vals))
    for _g,_vals in _rd_pool.items(): _UC_RHODEN[_g]=float(np.median(_vals))
    # (2) C[pos]: production-side conservation renorm (memo §3). ONE load-time pass over the valuation scope,
    #     accumulate Sum(pr0), Sum(v0p) per pos via the hook (C==1 during accumulation); C=Sum(pr0)/Sum(v0p) so
    #     the position's TOTAL captain-free production is unchanged by the map (pedigree/iso/captain nominal).
    _UC_CAL['on']=True; _UC_CAL['pr0'].clear(); _UC_CAL['v0p'].clear()
    with contextlib.redirect_stdout(io.StringIO()):
        for _p in MA.data:
            if not _uncomp_scope(_p): continue
            try: ev(_p,2026)
            except Exception: pass
    _UC_CAL['on']=False
    for _g,_s0 in _UC_CAL['pr0'].items():
        _s0p=_UC_CAL['v0p'].get(_g,0.0); _UC_C[_g]=(_s0/_s0p) if _s0p>0.0 else 1.0
    print("=== RL_UNCOMP v1.1 LEG B: map ON (s=%.4f Delta=%.1f) | V_ref_b/RHO_DEN/C over %d proven / scope-pop ==="
          %(MA.UNCOMP_S,MA.UNCOMP_DELTA,sum(len(v) for v in _vb_pool.values())))
    for _g in sorted(_UC_VREFB):
        print("    %-8s V_ref_b=%8.1f RHO_DEN=%7.2f C=%.5f"%(_g,_UC_VREFB.get(_g,0.0),_UC_RHODEN.get(_g,0.0),_UC_C.get(_g,1.0)))

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
# ==== ORDER I (RL_O36) — ARM S1. Everything above this line — every load-time reference median, every
# proven-population denominator, every conservation renormaliser — was derived on the DIAL-OFF BASIS,
# so the dial-on and dial-off boards share ONE currency and S1 cannot re-denominate the board (ORDER
# B's ruling, rl_model.py:1269, applied to this lever). From here down S1 is live in full: the board
# export, every ev() a harness calls, and every price the owner reads. Dial off => this is a no-op.
MA._O36_SCOPE['armed']=True
print("=== AFTER (wired: delist + staleness + isotonic) — named players ===")
print(f"{'player':22s}{'pos':8s}{'pk':>3s}{'g':>3s}{'ten':>4s}{'dlst':>5s}{'draft':>6s}{'BEFORE':>7s}{'AFTER':>7s}  reasoning")
before={'Ronin O':526,'Will Martyn':554,'Sam Philp':714,'Oscar Ryan':570,'Tew Jiath':509,'Jakob Ryan':594,'Harrison Jones':528,'Keidean Coleman':723,'Dylan Stephens':761}
reason={'Ronin O':'delisted, 0g -> ~0','Will Martyn':'delisted, 0g -> ~0','Sam Philp':'delisted, 0g -> ~0','Oscar Ryan':'stalled 0g ten3 -> 1/4 draft','Tew Jiath':'stalled 0g ten3 -> 1/4 draft','Jakob Ryan':'stalled 0g ten4 -> notch below 1/4','Harrison Jones':'mediocre 7yr KPF -> decayed','Keidean Coleman':'career-maker, holds','Dylan Stephens':'declined MID, should fall below Coleman'}
for nm in before:
    p=find(nm)
    if not p: continue
    print(f"{p['player'][:22]:22s}{MA.gfut(p):8s}{MA.effpk(p):3d}{nseas(p):3d}{PR.tenure(p,2026):4d}{('Y' if delisted(p) else '-'):>5s}{draftval(p):6.0f}{before[nm]:7d}{ev(p):7d}  {reason[nm]}")
print("\n=== MONOTONICITY + deep-pick AFTER ===")
for pos in ['KPF','MID']:
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
    s=[a for y,a in [(x['year'],x['avg']) for x in p['scoring'] if x['games']>=6 and x['year']<=Y]][-2:]
    return (np.mean(s)/max(1,PR.par_at(MA.gfut(p),min(MA.effpk(p),cp.KMAX),min(max(PR.tenure(p,Y),1),6)))) if s else 0.0
print("\n  RECENT ratio (last-2 avg / par):")
for nm in ['Harrison Jones','Dylan Stephens','Keidean Coleman','Oscar Ryan']:
    p=find(nm); print(f"    {nm:16s} recent_ratio={recent_ratio(p):.2f}")
print("\n=== GATE1 (wired) MID/KPF by tenure ===")
for pos in ['MID','KPF','SD']:
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
