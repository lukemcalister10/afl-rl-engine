"""PAR estimator (U26-REDESIGN, step 1) — ON THE ENGINE'S VALUE PATH. Not a diagnostic.

E5 (#279 step 4, seam word Q3 2026-07-30): this docstring used to say "STANDALONE DIAGNOSTIC, nothing wired
into the engine". That is FALSE and has been for some time. The live chain is
  _merged_recover.py imports wire_redesign -> W.PR = par_redesign -> par_redesign runs pb.fit() from THIS file
  -> _par_prior(p,Y) = PR.par_at(...) enters the value blend at _merged_recover.py:580, weighted by _ev_pw
     with the pinned residual floor _EVW_R = 0.11.
So a change here MOVES PLAYER VALUES. Treat it with value-path care; the prose, not the behaviour, was wrong.

par(pos, pick, tenure) = level_pos(log-pick)  +  ramp_pos(tenure)     [additive; ramp(yr1)=0]
  - target = median recency-weighted level (_lvl_wt) among players ON THE PARK at that pos x tenure
  - "on the park" = games_at_tenure >= f * base_play_rate(pos,tenure)   (base-rate-relative, NOT flat >=6g)
  - level: local-LINEAR kernel regression over log(pick), tricube, bandwidth H_LOGPICK
  - ramp: fit SEPARATELY per position via additive backfitting (shares strength across both axes),
          then SHRUNK toward the global ramp via n/(n+k) for thin positions (RUCK/KPP)
  - cohort: DRAFT 2003-2018 (locked Decision A)

Run: cd /home/claude/rl_after && PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RECENCY_DECAY=0.72 \
     python3 ../forward_valuation/par_build.py
"""
import sys, os, io, contextlib, collections
# rl_model provenance (fv-provenance remediation 2026-07-20): hardcoded /home/claude/rl_after insert REMOVED;
# rl_model resolves through the configured environment only (already-imported by the engine, else RL_REPO
# checkout). conditional_prior resolves from the canonically-resolved _FV (par_redesign puts it on sys.path).
if 'rl_model' not in sys.modules and os.environ.get('RL_REPO'):
    _rl_ra = os.path.join(os.environ['RL_REPO'], 'engine', 'rl_after')
    if os.path.isdir(_rl_ra): sys.path.insert(0, _rl_ra)
os.environ.setdefault('RL_GAMMA','1.0'); os.environ.setdefault('RL_PICK1','3000')
import math as _math
import numpy as np
with contextlib.redirect_stdout(io.StringIO()):
    import rl_model as MA
import conditional_prior as CP   # reuse _lvl_wt / debutyr / _exposure (same recency machinery)

# ---- dials (surfaced) ----
H_LOGPICK  = float(os.environ.get('PAR_BW',    '0.40'))  # kernel bandwidth in log-pick units
MIN_GAMES  = float(os.environ.get('PAR_MING', '6'))     # par gate = flat >=6g at that tenure
SHRINK_K   = float(os.environ.get('PAR_K',     '30'))    # ramp shrinkage n/(n+k) toward global
TEN_MAX    = 6
DRAFT_LO, DRAFT_HI = 2003, 2018
GROUPS = ['MID','SD','SF','KPD','KPF','RUCK']
EVAL_PICKS = [1,3,5,8,12,20,30,45,60]

def draftyr(p): return CP.debutyr(p) - 1
def season_row(p, Y):
    for x in p['scoring']:
        if x['year'] == Y: return x
    return None

# ============================================================================================================
# #336 VARIANT — THE BUST-INCLUSIVE PAR SURFACE.  EXPERIMENT ONLY; branch variant/336-bust-inclusive.
# NEVER MERGED. No pin moves, no artifact ships. See issue #336 (the VARIANT DIRECTIVE of 2026-08-06).
#
# THE DEFECT (the owner's, verbatim): "0 game busts make the history look better than mediocre players."
# The par surface is the developmental benchmark every projection leans on, and it samples SURVIVORS ONLY:
# :88-90 never emit a zero-game cell, and the >=MIN_GAMES gate at :99-101 drops the rest. 59.7% of
# (player, tenure) cells never teach. So the ordering best > mediocre > bust maps to measured contributions
# of "down > invisible" — order-reversed in the middle of the spectrum. That is the monotonicity breach.
#
# THE REPAIR FORM (recorded rule, primer §4.6 — these tables are PER-GAME benchmarks, so naive zero-filling
# is BARRED; a zero-game season has no per-game level to average in). Each cell becomes a true expectation
# over the TENURE-WINDOWED population:
#
#       E[level]  =  P(establishes)  x  E[level | establishes]
#
# with never-established players in the denominator at their REALIZED NOTHING. The identity is realised HERE,
# in gather(), by scaling every on-park observation by its own stratum's P(establishes) BEFORE the fit sees
# it. A kernel-weighted mean (and a per-tenure median) of P-scaled targets is P x (the same statistic of the
# unscaled targets) within a stratum, so the fitted surface IS E[level] and the shipped additive structure
# (level_pos(log-pick) + ramp_pos(tenure)), the isotonic priors and the ESS weighting all survive untouched.
#
# WHY HERE AND NOT AT par_at(): par_redesign.py carries its OWN par_at (its :77), composing pb.level_at with
# F['ramp_shr'] directly. The scope fence for this variant is TWO FILES (this one and rl_after/rl_model.py),
# so a multiplicative factor applied at this file's exit point would not reach the engine at all — and no
# additive pair (level', ramp') can equal P(pick,T) x (level + ramp) when P moves on BOTH axes. Scaling the
# observations is the only site inside the fence that every consumer sees, and it is also the honest one:
# the fit is a fit to the bust-inclusive expectation, not a post-hoc multiplier on a survivors' fit.
#
# ------------------------------------------------------------------------------------------------------------
# ADDENDUM 1 (issue #336, 2026-08-06) — THE AMENDED REPAIR FORM.  THIS SUPERSEDES THE FIRST CUT'S BY-TENURE P.
#
# THE OWNER'S CATCH, verbatim: "Robey losing 2/3 of his value seems crazy to me. He was a top 10 midfielder
# drafted who has had a good first season so far. And yet based on this he'd be valued at half of what he was
# on draft day? ... picks are fixed in value, year 1 players have dropped so much that the 1.57 year 0 to 5
# issue may now just be a bigger ratio at year 1 to 5 instead? Robbing peter to pay paul?"
#
# THE NAMED DEFECT of the first cut (measured, verified): it applied ESTABLISHED-BY-TENURE probability
# P(establishes at T | pos, band) at the level anchor. At T1 that factor is small BY CONSTRUCTION for every
# band (MID 8-12 T1 = 0.583, MID 13-20 T1 = 0.390, MID 49-99 T1 = 0.122) because most first-year listees have
# not yet played six games — a fact about the CALENDAR, not about the player's career prospects. Multiplying
# the year-1 anchor by it DOUBLE-CHARGES establishment risk that the forward band's low quantiles already
# carry by design, and it anchors a top-band year-1 player to a class average dominated by not-yet-established
# seasons his own class has ~99% odds of surviving. Measured cost: year-1-to-peak appreciation went 1.394x ->
# 1.988x — the hump MOVED from year 0 to year 1 rather than closing.
#
# THE AMENDMENT, binding here: the probability at every LEVEL-ANCHOR site is CAREER-LEVEL
#         P(EVER establishes | position x pick band)      -- NO tenure index, ever.
# Tenure enters ONLY through #338 window MEMBERSHIP (who is in the denominator), never as a probability
# discount on the anchor. The conditional level E[level | ever establishes] REMAINS tenure-resolved: it is
# still the establisher's own on-park observation at tenure T, so the ramp still learns the real development
# shape from the seasons that happened. Establishment risk is thereby charged EXACTLY ONCE, at the career
# level, where the owner's "counted as busts" requirement lives.
#
# P(ever establishes) IS DERIVED, NOT ASSUMED — per (position x pick-band), on this file's own par cohort:
#   numerator   : players with ANY season inside their #338 listed window of >= QUAL_338 (6) games — the
#                 establishment definition of engine/forward_valuation/build_cohort_book.py:181-185, quoted
#                 not re-invented. "Ever", so a late bloomer who first qualifies at tenure 7 counts.
#   denominator : the #338 tenure-windowed population of the cell. Every par-cohort member carries a listed
#                 window of at least two seasons under the minimum-listing-tenure rule (4/3/2 by pick band;
#                 helpers below mirror engine/rl_after/s4_matrix_M1v7.py:53-70, commit 30996f8), so for this
#                 CAREER-level quantity the tenure axis marginalises out and the denominator is the whole
#                 (position x band) cell — the never-established sit in it at their realized nothing.
#                 This is now the SAME construction as the BPK/POOL lever in rl_after/rl_model.py, which was
#                 already career-level and is NOT changed by this addendum.
#   position    : MA.gfut(p) — the SETTLED career position. It has to be: a player who never took the park
#                 has no season-position to key on, and season_pos() (the E3 ruling) can only label a season
#                 that happened. DISCLOSED axis mixture: the level is keyed on the season position, the
#                 probability on the career position.
#   pooling     : DELIBERATE AND DECLARED. Thin strata are not dropped and not silently trusted — every cell
#                 is shrunk toward the ALL-POSITION band marginal by n/(n+K_338), the same n/(n+k) design the
#                 ramp shrinkage already uses. K_338 = 10 pseudo-observations. Cell n's are printed by the
#                 report block below and recorded in the evidence dir, so every rate names its own denominator.
#
# NOT TOUCHED HERE: the frozen year-zero surface (held at its shipped survivors-basis fit, deliberately and
# disclosed — the joint re-derivation is #334 stage B, after the ruling), MIN_GAMES, the cohort window, the
# dual rule, the fit machinery.
#
# ------------------------------------------------------------------------------------------------------------
# AMENDMENT 2 (issue #336, OWNER CATCH 2 + "amend and rerun", 2026-08-06) — RESOLVED-STATE CONDITIONING.
#
# THE OWNER'S CATCH, verbatim: "How is establishment defined though? Have Trembath and Taylor, for example,
# not already established?"
#
# THE DEFINITION, quoted not re-invented (engine/forward_valuation/build_cohort_book.py:181-185): a player has
# ESTABLISHED when he has at least one season of >= 6 games. Under Addendum 1 EVERY real player — established
# or not — was anchored to P(ever establishes) x E[level | establishes]. Trembath (20 games @ 65.5), Taylor
# (9/17/18-game seasons), Moyle (8 and 13) and Lai (15) have ALL already established, and were still charged
# the class's chance of never establishing. That is establishment risk that HAS ALREADY RESOLVED IN THEIR
# FAVOUR, charged anyway. Addendum 1 fixed the wrong RATE; this fixes the wrong CONDITIONING.
#
# THE AMENDED FORM, binding at every site where a REAL player's own value regresses toward a class reference:
#
#   ESTABLISHED player (>=1 season of >=6 games on his own store record as of the valuation):
#         anchor = E[level | ever establishes]  for his (position x pick-band x tenure).  NO P discount.
#   UNRESOLVED player (no such season yet):
#         anchor = P(ever establishes | position x pick band) x E[level | ever establishes].
#
# Busts stay in EVERY establishment-rate denominator — P is unchanged from Addendum 1, career-level, with the
# never-established counted at their realized nothing. Nothing reverts to survivor averaging: the conditional
# level is taken over establishers, and (see gather() below) the tenure-axis survivorship gate is dropped so
# an establisher who FADED still teaches at his realized level instead of vanishing.
#
# STRUCTURAL CONSEQUENCE, and why this file's exit points change shape: under Addendum 1 the P factor was
# folded into the observations, so ONE fitted surface served every consumer. Amendment 2 needs the two legs
# separately, because which leg applies is a property OF THE PLAYER, not of the cell. So:
#     the FIT is now the CONDITIONAL level              (par_at / level_at, unchanged signatures)
#     P is applied AT THE CONSUMER, once, per player    (pest_at() below; par_redesign.par_at_p())
# MONOTONICITY, by construction: P <= 1, so the established anchor is ALWAYS >= the unconditional expectation
# for the same cell. The resolved/unresolved seam is therefore exactly the factor P — measured and reported
# in the evidence dir, NOT smoothed here (a cliff is a finding, and L-SMOOTH is a law about the shipped
# engine, not a licence for the build hand to invent a taper the owner has not ruled on).
# ============================================================================================================
QUAL_338 = 6      # establishment bar: a season of >=6 games (build_cohort_book.py:181-185)
K_338    = 10.0   # pooling strength: shrink each stratum toward the all-position BAND marginal

def _min_tenure_338(p):
    """#338: minimum listed seasons implied by the entry route/pick band. Mirrors s4_matrix_M1v7.py:53-59."""
    if p.get('type') == 'ND' and not p.get('_pickless'):
        pk = MA.effpk(p)
        if pk <= 20: return 4
        if pk <= 40: return 3
    return 2                     # ND 41+ and every pool route (RD/MSD/SSP/UNR/IRE/PDA/PDN/PDS)

def _debut_year_338(p):
    """#338: first season ON A LIST. MSD debuts in its entry year; every other route the year after.
    Mirrors s4_matrix_M1v7.py:61-64 (and equals CP.debutyr, which draftyr() already uses)."""
    C = p.get('year')
    return None if C is None else (C if p.get('type') == 'MSD' else C + 1)

def _listed_through_338(p):
    """#338: the year the player's listing runs through, or None if he is still listed. Mirrors
    s4_matrix_M1v7.py:66-70 — an explicit _last_listed is a KNOWN FACT and stands even when shorter;
    own data extends the minimum; active players are untouched."""
    LL = p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d = _debut_year_338(p)
    lastscore = max((r['year'] for r in p['scoring']), default=0)
    return max((d + _min_tenure_338(p) - 1) if d is not None else 0, lastscore)

def _in_window_338(p, Y):
    """Is calendar year Y inside this player's #338 LISTED tenure window? (the denominator's membership rule)"""
    d = _debut_year_338(p)
    if d is None or Y < d: return False
    lt = _listed_through_338(p)
    return True if lt is None else (Y <= lt)      # lt None => still listed => at risk

def _ever_established_338(p):
    """ADDENDUM 1: did this player EVER establish (a >=QUAL_338-game season) inside his #338 listed window?
    Career-level, no tenure index — tenure enters only through the window membership test."""
    for r in p['scoring']:
        if r['games'] >= QUAL_338 and _in_window_338(p, r['year']): return True
    return False

def build_pest(pool):
    """ADDENDUM 1 (#336, 2026-08-06): P(EVER establishes) per (gfut position x MA pick-band), CAREER-LEVEL,
    over the #338 tenure-windowed par cohort. The by-tenure P of the first cut is superseded — it
    double-charged establishment risk the forward band's low quantiles already carry.
    Returns (P, num, den): P is the POOLED rate actually consumed; num/den are the RAW counts, disclosed."""
    num = collections.defaultdict(int); den = collections.defaultdict(int)
    bnum = collections.defaultdict(int); bden = collections.defaultdict(int)   # all-position band marginal
    for p in pool:
        g = MA.gfut(p); b = MA.bandof(MA.effpk(p)); d0 = draftyr(p)
        # MEMBERSHIP: the #338 window must cover at least one tenure year of the par range. Under the
        # minimum-listing-tenure rule every drafted member's window covers draftyr+1, so this admits the
        # whole cohort — stated as a test rather than assumed, so the rule is the one that is enforced.
        if not any(_in_window_338(p, d0+T) for T in range(1, TEN_MAX+1)): continue
        den[(g,b)] += 1; bden[b] += 1
        if _ever_established_338(p):
            num[(g,b)] += 1; bnum[b] += 1
    gn = sum(bnum.values()); gd = sum(bden.values())
    grate = (gn/gd) if gd else 0.0
    P = {}
    for b in range(MA.NB):
        pbar = (bnum[b]/bden[b]) if bden[b] else grate
        for g in GROUPS:
            n = den[(g,b)]
            P[(g,b)] = (num[(g,b)] + K_338*pbar)/(n + K_338)
    return P, num, den

# ---- E3 (#279 step 4 item 6; the par ruling, owner word 2026-07-30 "Yes, per season") ------
# The par surface used to key every observation by MA.gfut(p) — ONE label for a whole career — so a role
# migrant's prime seasons refiled under his DESTINATION position and dragged up the young players anchored
# in those cells (the Joe Berry +351 ripple). Each season now files under the position RECORDED FOR THAT
# SEASON, which the store carries on every one of its 11,264 scoring rows (landed at #262).
#
# 1,874 of those rows (16.6%) record a DUAL position ('SF/MID', 'KPF/RUCK', ...), and GRP maps only the six
# single positions, so the rule for duals must be STATED. PAR_DUAL_RULE is that statement — an OWNER word
# (#279, pending at the time of writing), not a dial and not env-readable:
#   'primary' — the primary component. futblend's own law: "The PRIMARY keys peak/curve/runway/key-premium".
#   'lower'   — the pair's LOWER replacement bar; the eligibility-collapse law (R105.1 / _collapse_elig).
#   'exclude' — dual seasons do not teach the par.
# MEASURED at the step-4 rehearsal: 'primary' and 'lower' disagree on exactly 2 of 1,874 dual rows (the two
# 'SF/KPD'), and neither reaches this cohort — so they produce a BYTE-IDENTICAL par surface here.
PAR_DUAL_RULE = 'primary'

def season_pos(r):
    """The group a single season's observation teaches. None => this season does not teach."""
    s = r.get('pos')
    if not s: return None
    if '/' not in s: return MA.GRP.get(s)
    if PAR_DUAL_RULE == 'exclude': return None
    a, b = s.split('/', 1)
    ga, gb = MA.GRP.get(a), MA.GRP.get(b)
    if PAR_DUAL_RULE == 'lower' and ga is not None and gb is not None:
        return gb if MA.REPL.get(gb, float('inf')) < MA.REPL.get(ga, float('inf')) else ga
    return ga if ga is not None else gb

# ---- 1. gather on-park observations: (pos, logpick, tenure, lvl, games) -------------------
def gather():
    pool = [p for p in MA.data if MA.GRP.get(p.get('pos'))
            and (p.get('pick') or p.get('_ft')) and DRAFT_LO <= draftyr(p) <= DRAFT_HI]
    # raw rows first (need base_play_rate before applying the gate)
    raw = []  # (pos, pick, ten, Y, games, p)
    for p in pool:
        pk = min(MA.effpk(p), CP.KMAX); d0 = draftyr(p)
        for T in range(1, TEN_MAX+1):
            Y = d0 + T; r = season_row(p, Y); g = r['games'] if r else 0
            if g > 0:
                pos = season_pos(r)                  # E3: PER-SEASON, not one career-long gfut label
                if pos is None: continue             # only reachable under the 'exclude' rule
                raw.append((pos, pk, T, Y, g, p))
    # base play rate = median games among players who PLAYED (g>0) at that pos x tenure
    base = {}
    bycell = collections.defaultdict(list)
    for pos, pk, T, Y, g, p in raw: bycell[(pos,T)].append(g)
    for k,v in bycell.items(): base[k] = float(np.median(v))
    # #336 VARIANT (ADDENDUM 1): CAREER-LEVEL P(ever establishes) over the #338 tenure-windowed
    # population, derived from THIS pool. No tenure index — see the amended header block.
    PEST, PNUM, PDEN = build_pest(pool)
    # #336 AMENDMENT 2 — THE SAMPLE IS NOW THE ESTABLISHER'S, AND THE FIT IS THE CONDITIONAL LEVEL.
    # Two changes against Addendum 1, both required by the resolved-state repair shape:
    #
    #  (1) NO P SCALING HERE. Under Addendum 1 every observation was multiplied by the career-level
    #      P(ever establishes) so the fitted surface was the UNCONDITIONAL expectation. Amendment 2
    #      needs BOTH legs of the identity separately, because which leg a player gets depends on HIS
    #      OWN resolved state. So the fit is now the CONDITIONAL level E[level | ever establishes],
    #      and P is applied AT THE CONSUMER, exactly once, only to players who have not yet resolved
    #      (par_redesign.par_at / par_at_p). This is also strictly more honest than the first form:
    #      P is now an exact per-player factor rather than a factor smeared through a kernel
    #      regression over log-pick.
    #
    #  (2) THE TENURE-AXIS SURVIVORSHIP GATE IS DROPPED. The shipped sample at tenure T is
    #      `games_at_T >= MIN_GAMES` — and since MIN_GAMES == QUAL_338 == 6, that gate is exactly
    #      "is he ON THE PARK at T", i.e. survivors-at-that-tenure. An establisher who faded to three
    #      games at T vanished from the table, so a worse career again became invisible rather than
    #      low — the same breach one axis over. The sample is now EVERY EVER-ESTABLISHER'S SEASON IN
    #      WHICH HE TOOK THE PARK AT ALL, at his realized recency-weighted level. Never-establishers
    #      still do not teach the conditional level (they are the OTHER leg — they sit in P's
    #      denominator at their realized nothing).
    #
    # WHAT IS *NOT* DONE, AND WHY — the third reading, measured and rejected on a recorded rule.
    # "All establishers in the window at T" could also be read as ZERO-FILLING the establisher's
    # zero-game seasons. primer 4.6 BARS that: these are PER-GAME benchmarks and a zero-game season
    # has no per-game level to average in. It is also the Addendum-1 defect returning by another
    # door: measured on this cohort the zero-filled reading multiplies the YEAR-ONE conditional level
    # by 0.570 (see act336c/cond_variants.txt), which is a CALENDAR discount on a player who has
    # already established — precisely what Addendum 1 removed. Measured sizes of all three readings:
    #      yr1 / yr2 / yr3 / yr4 / yr5 / yr6, as a ratio to the shipped on-park sample
    #   (i)   on-park >=6g   (Addendum 1)      1.000 1.000 1.000 1.000 1.000 1.000
    #   (ii)  played  >=1g   (THIS VARIANT)    0.898 0.949 0.959 0.969 0.971 0.978
    #   (iii) in-window, zero-filled (BARRED)  0.570 0.819 0.905 0.947 0.953 0.968
    # ========================================================================================================
    # CHANNEL (c) — RL_336_PARSURV=1: DECLARED MEASUREMENT ABLATION LEVER, DEFAULT OFF, BYTE-EXACT WHEN OFF.
    # Added by #334 ORDER 3 (build brief 5248006413) so the #336 layer's par_build leg can be attributed
    # separately from its rl_model leg. It reverts THE ONE LINE below to the shipped pre-#336 sample gate
    # `g >= MIN_GAMES` — survivors-at-that-tenure — leaving everything else in this file in place.
    #
    # WHY THIS ONE LINE IS THE WHOLE CHANNEL, and it is a finding rather than a convenience. Amendment 2/3's
    # par-side machinery — build_pest / PEST / pest_of / resolved_336 / resolve_w / dpar_of and the A3_D
    # reconciliation constants — is DEAD ON THE VALUE PATH: par_redesign.py carries its own par_at (:68)
    # composing pb.level_at with F['ramp_shr'] and never calls pest_of/dpar_of, and a repo-wide search finds
    # NO consumer of any of those symbols outside this file. So the only way #336 reaches the engine through
    # forward_valuation is by changing WHICH OBSERVATIONS THE SURFACE IS FITTED TO, which is this gate.
    # Reverting it is therefore the complete par-side counterfactual, not a partial one.
    # ========================================================================================================
    _PARSURV = os.environ.get('RL_336_PARSURV', '0') != '0'
    obs = []  # (pos, logpick, T, lvl)  — E[level | ever establishes], tenure-resolved
    for pos, pk, T, Y, g, p in raw:
        _keep = (g >= MIN_GAMES) if _PARSURV else (g >= 1 and _ever_established_338(p))
        if _keep:
            # RL_336_XW: the 5th element is the observation weight. It is 1.0 for every row when the
            # dial is off, and the fit then passes ws=None, so the off path never multiplies at all.
            obs.append((pos, np.log(pk), T, CP._lvl_wt(p, Y), (min(g, XW_CAP) if XW else 1.0)))
    return obs, base, raw, PEST, PNUM, PDEN

# ---- 2. local-linear kernel regression over log-pick --------------------------------------
def tricube(u):
    u = np.abs(u); w = (1 - u**3)**3; w[u >= 1] = 0.0; return w
def loclin(x0, xs, ys, h, ws=None):
    """local-linear fit at x0; returns (yhat, ESS=(sum w)^2/sum w^2).

    ws (#336 ORDER 4, RL_336_XW): OPTIONAL per-observation weight multiplied into the kernel weight.
    ws=None is the DEFAULT and takes the identical code path as before — no multiplication happens at
    all, so the fit is byte-exact. When supplied, the effective weight is tricube(u) * ws, which is the
    standard weighted local-linear estimator; the closed-form fsum solve below is unchanged.
    DETERMINISM FIX (2026-07-14, session_2026-07-14/determinism_fix): PART 1 measured the PAR table
    as the FIRST cross-environment divergent stage (upstream of everything) — NOT the NW-smoother the
    register (item 106) hypothesised, and NOT price6. The cause is here: BLAS `@` (Xd.T@W@Xd, Xd.T@W@ys)
    plus np.linalg.solve accumulate the weighted normal-equation sums in a CPU-kernel-dependent ORDER,
    so the PAR level moved between an AVX-512 and an AVX2 build on ONE box. The 2-parameter weighted
    normal equations have a CLOSED FORM; solving it with math.fsum (order-fixed, correctly-rounded) is
    the SAME maths, identical on every kernel and every CPU. b0 (the fit AT x0) is all we return."""
    w = tricube((xs - x0)/h)
    if ws is not None: w = w * np.asarray(ws, dtype=float)   # RL_336_XW: exposure weight on top of the kernel
    # Only tricube-nonzero points contribute; dropping the exact zeros is EXACT for math.fsum (a 0.0 term
    # changes no correctly-rounded sum) and shrinks each fsum from the full column to the in-bandwidth handful
    # — the board is byte-identical, the per-build cost falls back near the pre-fix baseline.
    nz = np.asarray(w, dtype=float) > 0.0
    if not nz.any(): return float('nan'), 0.0
    wa = np.asarray(w, dtype=float)[nz]; u = np.asarray(xs, dtype=float)[nz] - x0; ya = np.asarray(ys, dtype=float)[nz]
    Sw = _math.fsum(wa.tolist())
    if Sw <= 0: return float('nan'), 0.0
    Swu  = _math.fsum((wa*u).tolist())
    Swuu = _math.fsum((wa*u*u).tolist())
    Swy  = _math.fsum((wa*ya).tolist())
    Swuy = _math.fsum((wa*u*ya).tolist())
    # Solve  [[Sw, Swu],[Swu, Swuu]] [b0,b1]^T = [Swy, Swuy]^T  by LU WITH PARTIAL PIVOTING — the SAME
    # algorithm LAPACK dgesv uses — so a well-conditioned cell tracks the old np.linalg.solve to float
    # precision. For a RANK-DEFICIENT cell (thin low picks whose tricube weight sits on one pick, so the
    # weighted design has no x-spread) the local-linear fit is undefined; fall back to the local-CONSTANT
    # (weighted mean) — the standard, numerically-stable degradation. relcond = det/(Sw*Swuu) at machine
    # epsilon flags it. NOTE (measured, session_2026-07-14): the board of record e6a8e6ef used the native
    # kernel's UNSTABLE solve of one boundary cell (relcond~2e-16, pick~4): a deterministic result there is
    # the stable weighted mean, which differs from that garbage — this is the source of the ruck A3 delta.
    relcond = (Sw*Swuu - Swu*Swu)/(Sw*Swuu) if Sw*Swuu > 0 else 0.0
    if relcond < 1e-9:
        yhat = Swy/Sw                                        # rank-deficient -> local-constant (weighted mean)
    else:
        a, b, c, d, e, f = Sw, Swu, Swu, Swuu, Swy, Swuy
        if abs(c) > abs(a): a, b, e, c, d, f = c, d, f, a, b, e   # partial pivot on the larger leading entry
        m = c/a; d2 = d - m*b; f2 = f - m*e
        b1 = (f2/d2) if d2 != 0.0 else 0.0
        yhat = (e - b*b1)/a                                  # b0 = the fit AT x0 (the intercept)
    ess = (Sw*Sw)/_math.fsum((wa*wa).tolist())
    return float(yhat), float(ess)

# ============================================================================================================
# #336 ORDER 4 — EXPOSURE WEIGHTING OF THE PAR SAMPLE.  DIAL-GATED, DEFAULT OFF, BYTE-EXACT WHEN OFF.
#
# THE DEFECT IT ADDRESSES. The par surface is a PER-GAME benchmark, and it is consumed as a denominator
# against player statistics that are THEMSELVES games-weighted — ITEM C's evidence weight is Q = sa/par
# with sa the career GAMES-WEIGHTED average (_merged_recover.py:2075-2080). Today every observation
# enters the fit with equal weight, so a one-game debut counts as much as a twenty-game season, and the
# fitted par answers "the average of season-averages" rather than "the level in a typical game played".
# That is a unit mismatch between numerator and denominator, and it exists independently of #336.
#
# WHY IT MATTERS HERE. #336 changed the sample from ">=6 games at that tenure" to "every
# ever-establisher's played season". That repair is correct and STAYS — an establisher who faded to
# three games must not vanish. But it also admitted many 1-5 game seasons at EQUAL weight, and the
# resulting cut is front-loaded (tenure-1 cell level x0.897, fading to x0.978 by tenure 6). The channel
# split measured that par leg at 89.2% of the #336 year-1 drop.
#
# THE HONESTY TEST THIS SURVIVED, BEFORE IT WAS WIRED (PREREG_ORDER4.md / XW_HONESTY.txt). The
# suspicion was that exposure weighting is survivor bias by another door, because busts have little
# exposure. Measured on the same cohort: the sub-6-game rows keep 4.8% of pooled fit weight (11.5% at
# tenure 1) against 19.7% of the row count — DOWN-WEIGHTED BY ABOUT FOUR, NOT DROPPED; the estimator
# diverges from the survivors-only one in 37 of 44 informative (tenure x band) cells; and at tenure 1 in
# the LATE pick bands it lands BELOW the survivors-only level, which is the opposite of survivor bias.
#
# NOTHING IS DROPPED BY THIS DIAL. Every row in the #336 sample stays in the sample. The dial changes
# weights only. RL_336_XW=0 (DEFAULT) => ws is None everywhere => the identical pre-dial code path.
# XW_CAP=18 (a full season's exposure) is the CONSERVATIVE choice of the three measured: uncapped games
# and the target's own recency-weighted exposure both move the level FURTHER, so the cap works against
# the design rather than for it. That is disclosed rather than left to be discovered.
# ============================================================================================================
# ORDER 9 ADOPTION: DEFAULT FLIPS OFF -> ON by owner word (filed 5249802288) — XW is the counterbalance
# he included in the bake. It cleared its kill test before wiring (XW_HONESTY.txt): the sub-6-game rows
# keep 4.8% of pooled fit weight against 19.7% of the row count, the estimator diverges from the
# survivors-only one in 37 of 44 informative cells, and at tenure 1 in the LATE pick bands it lands
# BELOW survivors-only. RL_336_XW=0 is now the ABLATION rather than the default.
XW = os.environ.get('RL_336_XW', '1') != '0'
XW_CAP = float(os.environ.get('RL_336_XW_CAP', '18'))

def _wmedian(v, w):
    """weighted median: the value at which cumulative weight crosses half the total. Used ONLY under
    RL_336_XW; the unweighted path keeps np.median exactly (np.median averages the two middle values at
    even n, which a weighted median does not, so the two are not interchangeable and are not swapped)."""
    v = np.asarray(v, dtype=float); w = np.asarray(w, dtype=float)
    o = np.argsort(v, kind='stable'); v = v[o]; w = w[o]
    c = np.cumsum(w); tot = c[-1]
    if tot <= 0: return float(np.median(v))
    return float(v[int(np.searchsorted(c, 0.5*tot))])

# ---- 3. additive backfitting: level_pos(logpick) + ramp_pos(T) ----------------------------
def fit():
    obs, base, raw, PEST, PNUM, PDEN = gather()   # #336 VARIANT: gather() now also returns the P(establishes) strata
    POS = {g: np.array([(x,T,lv,w) for (pos,x,T,lv,w) in obs if pos==g], dtype=float) for g in GROUPS}
    # E3 LOUD HALT (#279 step 4 item 6). An empty group used to travel silently from here to the ramp step
    # below, where POS[g] is shape (0,) and POS[g][:,1] raised a BARE IndexError naming nothing — a cohort
    # or keying change that starved a position looked like an indexing bug. Halt here instead, NAMING the
    # group, the cohort window, and what the gather actually produced.
    _empty = [g for g in GROUPS if POS[g].size == 0]
    if _empty:
        raise SystemExit(
            "par_build HALT: no on-park observations for position group(s) %s.\n"
            "  cohort DRAFT %d-%d | tenure 1-%d | par gate >=%g games | dual rule '%s'\n"
            "  gather() produced %d raw rows -> %d gated observations; per-group counts: %s\n"
            "  A starved group cannot be fitted. Widen the cohort, relax the gate, or revisit the keying —\n"
            "  do NOT drop the group silently."
            % (', '.join(_empty), DRAFT_LO, DRAFT_HI, TEN_MAX, MIN_GAMES, PAR_DUAL_RULE,
               len(raw), len(obs), {g: int(POS[g].shape[0]) for g in GROUPS}))
    ramp = {g: np.zeros(TEN_MAX+1) for g in GROUPS}     # ramp[g][T], index 0 unused
    # iterate
    for _ in range(4):
        # (a) level fit on tenure-detrended values, per position
        levelfn = {}
        for g in GROUPS:
            A = POS[g]
            if len(A) < 4: levelfn[g] = None; continue
            xs, Ts, lv = A[:,0], A[:,1].astype(int), A[:,2]
            detr = lv - np.array([ramp[g][t] for t in Ts])
            levelfn[g] = (xs.copy(), detr.copy(), A[:,3].copy())   # 3rd slot: the RL_336_XW weights (all 1.0 when off)
        # (b) ramp = median pick-detrended resid by tenure, anchored ramp(1)=0
        for g in GROUPS:
            A = POS[g]
            if levelfn[g] is None: continue
            xs, Ts, lv = A[:,0], A[:,1].astype(int), A[:,2]
            lx, ldetr, lw = levelfn[g]
            lvlhat = np.array([loclin(x, lx, ldetr, H_LOGPICK, lw if XW else None)[0] for x in xs])
            resid = lv - lvlhat
            r = np.zeros(TEN_MAX+1)
            for T in range(1, TEN_MAX+1):
                m = (Ts==T)
                if m.sum()>0:
                    # the RAMP is where the tenure profile lives, so the weighting must reach it too --
                    # an exposure-weighted level fit with an equal-weighted ramp would be a half-measure.
                    r[T] = _wmedian(resid[m], A[:,3][m]) if XW else float(np.median(resid[m]))
                else:
                    r[T] = (r[T-1] if T>1 else 0.0)
            r = r - r[1]                                  # anchor yr1 = 0
            ramp[g] = r
    # global ramp (pooled across positions, sample-weighted by cell counts)
    allresid_byT = collections.defaultdict(list)
    n_by_pos = {}
    for g in GROUPS:
        A = POS[g]; n_by_pos[g] = len(A)
        if levelfn[g] is None: continue
        xs, Ts, lv = A[:,0], A[:,1].astype(int), A[:,2]
        lx, ldetr, lw = levelfn[g]
        lvlhat = np.array([loclin(x, lx, ldetr, H_LOGPICK, lw if XW else None)[0] for x in xs])
        resid = lv - lvlhat
        for T,rv,wv in zip(Ts, resid, A[:,3]): allresid_byT[T].append((rv, wv))
    gramp = np.zeros(TEN_MAX+1)
    for T in range(1, TEN_MAX+1):
        _rv = allresid_byT[T]
        if not _rv: gramp[T] = 0.0
        elif XW:    gramp[T] = _wmedian([x[0] for x in _rv], [x[1] for x in _rv])
        else:       gramp[T] = float(np.median([x[0] for x in _rv]))
    gramp = gramp - gramp[1]
    # shrink each position's ramp toward global
    ramp_shr = {}; sw = {}
    for g in GROUPS:                              # UN-POOLED per Luke: enough per-position data; level kernel-ESS carries thin cells
        ramp_shr[g] = ramp[g].copy(); sw[g] = 1.0
    # ---- MONOTONICITY PRIOR (Decision-D class), weighted isotonic on BOTH axes ----
    # (a) level NON-INCREASING in pick (better pick -> par >= worse pick); weights = kernel ESS
    PKGRID = list(range(1, int(CP.KMAX)+1))
    level_grid = {}
    for g in GROUPS:
        lf = levelfn[g]
        if lf is None: level_grid[g] = None; continue
        raw = [loclin(np.log(pk), lf[0], lf[1], H_LOGPICK, lf[2] if XW else None) for pk in PKGRID]
        ys = np.array([r[0] for r in raw]); es = np.array([max(r[1],0.5) for r in raw])
        ok = np.isfinite(ys)                               # nan-fill empty cells (e.g. RUCK pk3) before isotonic
        if ok.any() and not ok.all():
            ys = np.interp(np.arange(len(ys)), np.where(ok)[0], ys[ok])
        ys_mono = _pava(ys, es, increasing=False)          # non-increasing in pick
        level_grid[g] = (np.array(PKGRID, float), ys_mono, es)
    # (b) ramp NON-DECREASING in tenure (development monotone); weights = per-tenure obs count
    for g in GROUPS:
        _Ts = POS[g][:,1].astype(int); _W = POS[g][:,3]
        cnt = np.array([1.0]+[float(_W[_Ts==T].sum() if XW else (_Ts==T).sum()) for T in range(1,TEN_MAX+1)])
        r = ramp_shr[g].copy()
        r[1:] = _pava(r[1:TEN_MAX+1], cnt[1:TEN_MAX+1], increasing=True)
        ramp_shr[g] = r - r[1]                              # re-anchor yr1 = 0
    return dict(obs=obs, base=base, POS=POS, levelfn=levelfn, ramp=ramp, gramp=gramp,
                ramp_shr=ramp_shr, sw=sw, n_by_pos=n_by_pos, level_grid=level_grid,
                pest=PEST, pest_num=PNUM, pest_den=PDEN)   # #336 VARIANT: the strata travel with the fit, for disclosure

def _pava(y, w, increasing=True):
    """weighted pool-adjacent-violators. increasing=True -> non-decreasing; False -> non-increasing."""
    blocks=[]                                              # [value, weight, count]
    for yi,wi in zip(y,w):
        blocks.append([float(yi), max(float(wi),1e-6), 1])
        while len(blocks)>1 and ((blocks[-2][0]>blocks[-1][0]) if increasing else (blocks[-2][0]<blocks[-1][0])):
            v2,w2,c2=blocks.pop(); v1,w1,c1=blocks.pop()
            blocks.append([(v1*w1+v2*w2)/(w1+w2), w1+w2, c1+c2])
    out=[]
    for v,wt,c in blocks: out += [v]*c
    return np.array(out)

def level_at(F, g, pick):
    grid = F.get('level_grid',{}).get(g) if isinstance(F.get('level_grid',{}),dict) else None
    if grid is not None:
        xs,ys,es = grid; pk=min(max(pick,1),70)
        return float(np.interp(pk, xs, ys)), float(np.interp(pk, xs, es))
    lf = F['levelfn'][g]
    if lf is None: return float('nan'), 0.0
    # RL_336_XW: the ungridded fallback carries the same weights as the gridded path, so the two cannot
    # disagree about the estimator. lf[2] is all-1.0 when the dial is off and ws=None is passed anyway.
    return loclin(np.log(pick), lf[0], lf[1], H_LOGPICK, lf[2] if XW else None)

def par_at(F, g, pick, T):
    """#336 AMENDMENT 2: this is now the ESTABLISHED-CONDITIONAL anchor, E[level | ever establishes].
    Consumers that price a REAL player must select on his resolved state (par_redesign.par_at_p);
    consumers that price a PICK or a synthetic take the unconditional expectation = pest_at() x this."""
    lv,_ = level_at(F, g, pick); return lv + F['ramp_shr'][g][T]

def pest_of(F, p):
    """#336 AMENDMENT 2: the career-level P(ever establishes) for the cell a REAL player sits in.
    Keyed EXACTLY as build_pest() derived it — settled career position MA.gfut(p), band of the RAW
    effective pick MA.effpk(p) (not the KMAX-clamped pick the level surface uses; clamping there is a
    property of the kernel's support, not of the probability's stratum). Unknown cell -> 1.0, which
    makes the unresolved anchor fall back to the conditional level rather than to a silent zero."""
    P = F.get('pest')
    if not P: return 1.0
    v = P.get((MA.gfut(p), MA.bandof(MA.effpk(p))))
    return 1.0 if v is None else float(v)

QUAL_RESOLVE = QUAL_338      # the SAME bar, named at the consumer so the two cannot drift apart
def resolved_336(p, Y=None):
    """#336 AMENDMENT 2: has this player's establishment already RESOLVED, on his own store record as
    of the valuation? True iff he has at least one season of >= 6 games at or before Y (the definition
    at build_cohort_book.py:181-185). Y=None means the whole record — used only where the surrounding
    engine code is itself career-basis (rl_model's pkbest/srel), never on the year-indexed value path."""
    for r in p['scoring']:
        if r['games'] >= QUAL_RESOLVE and (Y is None or r['year'] <= Y): return True
    return False

# ============================================================================================================
# #336 AMENDMENT 3 (issue #336, "AMENDMENT 3 FIRED — the continuous experiment", owner word "run it",
# 2026-08-06).  TWO changes to amendment 2's construction, and nothing else.
#
# ------------------------------------------------------------------------------------------------------------
# (1) THE SMOOTH RESOLUTION WEIGHT r(p) — the binary established/unresolved switch becomes a ramp.
#
# Amendment 2 selected between two anchors on a BOOLEAN. That put a cliff at the establishment bar: the same
# player one game either side of six games moved by the whole factor 1/P (measured: up to 2.434x at the anchor,
# +58% in board points on the 12-probe difference-in-differences). A cliff on the price path violates the
# engine's own no-cliffs law (L-SMOOTH, acceptance_v1_13.json) — the amendment-2 evidence reported it as a
# design red rather than smoothing it, because a taper was then unruled. It is ruled now.
#
# THE FORM, and it is REUSED, NOT INVENTED. The engine already carries a continuous evidence-resolution
# object: the R100.11 evidence fade at _merged_recover.py:711-735,
#       w(g) = g^2/(g+K)                 Fix 1's measured evidence-reliability curve
#       pw(g) = 1/(1+w(g)) = (g+K)/(g^2+g+K)      the PRIOR's weight: 1 at zero evidence -> 0 on evidence
# described there as "ONE continuous object: smooth, monotone, rational (g^2+g+K>0 for all g>=0). NO threshold,
# NO counter, NO branch (L-SMOOTH)".  Its complement is exactly the quantity amendment 3 needs — how far a
# player's own record has RESOLVED him — so that is what is used:
#       rho(g) = 1 - pw(g) = g^2 / (g^2 + g + K)
# NO NEW WIDTH IS SET.  K is taken unchanged from the engine's pinned constant (_ABS_FADE_K = 5.8, itself
# "Fix 1's measured w(g) scale (RL_DAMP_K, :162)"), restated here with its source because par_build cannot
# import the engine module. The one construction on top of the borrowed object is a NORMALISATION, disclosed:
# rho is rescaled to reach exactly 1.0 at the ruled establishment bar and capped there, so that
#       r(0) = 0                         zero evidence -> the full class discount, exactly
#       r(g>=6) = 1                      the ruled establishment definition -> no class discount, exactly
#       r monotone and continuous in between
# which is amendment 3's stated requirement verbatim. The ramp variable is the player's BEST SINGLE-SEASON
# games as of the valuation, because the establishment definition (build_cohort_book.py:181-185) is itself a
# MAX over seasons — the ramp must run on the same statistic the bar tests, or the two could disagree.
#
#   MEASURED SHAPE (K=5.8, bar=6):  g:  0     1     2     3     4     5     6+
#                                   r:  0.000 0.170 0.450 0.671 0.824 0.927 1.000
#   The residual step across the OLD cliff (5g -> 6g) is 0.073 of the class discount, against 1.000 under
#   amendment 2 — a 92.7% reduction by construction, before the reconciliation below shrinks it further.
#   It cannot be zero: a monotone map that is 0 at zero evidence and 1 at the bar must climb somewhere, and
#   pushing the last step to zero means handing the full established anchor to a player who has NOT
#   established. The residual is MEASURED on the same 12-probe difference-in-differences and reported.
#
# ------------------------------------------------------------------------------------------------------------
# (2) SINGLE-CHARGE RECONCILIATION — the unresolved leg is no longer P.
#
# Addendum 1 proved the anchor charges establishment risk ONCE for players who go on to establish (probe mean
# excess 1.023). It never asked the same question on the players who have NOT: for them the forward band's own
# low quantiles are also pricing establishment failure, and stacking the full career-level P on top of that is
# the double charge one population over. Amendment 3 measures the band's own charge and then sets the anchor
# side to whatever is left, so the TOTAL equals the class risk and no more:
#
#       d_band  =  ev(unresolved player, anchor UNDISCOUNTED) / ev(certainty-equivalent established comparator)
#                  ... what the band already takes off, measured on the unresolved subset (never before probed)
#       target  =  P(ever establishes | position x pick band)          the true class risk (Addendum 1's P)
#       required total  =  d_band x pass(D)  =  target
#   =>  D  =  pass^-1( target / d_band ),   capped at 1.0
#
# where pass(.) is the MEASURED pass-through from the anchor to the price (the anchor is one input among many,
# so scaling it by D does not scale the price by D; pass(D) = D^ALPHA, ALPHA fitted on the unresolved probe
# set). THE FLOOR IS A REAL CASE, not a formality: if d_band <= target the band ALREADY charges the whole class
# risk or more, D = 1.0 and the anchor charges NOTHING further. The anchor discount never goes negative — the
# anchor is never LIFTED above the conditional level to make room for a band that over-charges.
#
# Both constants below are PINNED from a measurement pass on this same build (the derivation lever
# RL_336_DFORCE, declared beside them), and the reconciliation is then PROVEN on the unresolved subset by
# re-decomposing the finished build: total effective discount / true class risk, target 1.0.
#
#   THE ANCHOR, in one line, for a REAL player:
#       anchor(p) = E[level | establishes] x [ D(p) + r(p) x (1 - D(p)) ]
#   r=1 (established) -> E[level | establishes], amendment 2's established leg, unchanged.
#   r=0 (no evidence) -> D x E[level | establishes], the SINGLE-CHARGED unresolved leg.
#   A PICK or a synthetic still takes the full unconditional expectation P x E[level | establishes]: it has no
#   record to resolve and must carry the entire entrant risk. That is par_at(), untouched by this amendment.
# ============================================================================================================
RES_K = 5.8       # PINNED, NOT SET HERE: = _merged_recover._ABS_FADE_K, "Fix 1's measured w(g) scale
                  # (RL_DAMP_K, :162)". Restated (not imported) because par_build cannot import the engine.
def _rho_336(g):
    """the engine's R100.11 evidence-resolution curve, rho(g) = 1 - pw(g) = g^2/(g^2+g+K)."""
    g = float(max(0.0, g)); return (g*g)/(g*g + g + RES_K)
_RHO_BAR = _rho_336(QUAL_RESOLVE)      # rho at the ruled bar; the normaliser, so r(bar) == 1 exactly
def bestgames_336(p, Y=None):
    """the establishment statistic itself: best single-season games at or before Y (max over seasons)."""
    gs = [r['games'] for r in p['scoring'] if (Y is None or r['year'] <= Y)]
    return max(gs) if gs else 0
def resolve_w(p, Y=None):
    """#336 AMENDMENT 3: r(p) in [0,1] — how far this player's establishment has RESOLVED.
    0 at zero evidence, 1 at (and above) the ruled >=6-game bar, the engine's own R100.11 evidence curve
    in between, normalised to the bar. Replaces amendment 2's boolean resolved_336() at every real-player
    anchor; resolved_336 itself is KEPT (it is the ruled definition and r's own endpoint)."""
    if _RFORCE is not None: return float(_RFORCE)
    return min(1.0, _rho_336(bestgames_336(p, Y)) / _RHO_BAR)

# ------------------------------------------------------------------------------------------------------------
# THE RECONCILIATION, MEASURED — and the answer it returned.  (derive_a3.py / reconcile_a3.py, this act.)
#
# PROBE SET: every real board player with NO season of >=6 games as of 2026 and at least one played season.
#            n = 329 of 349 unresolved (20 excluded: no played season, so no per-game average to hold fixed
#            and therefore no comparator that is not invented). Denominator disclosed on every figure.
# COMPARATOR: CE(p) — the same player, same key, pick, position, age, tenure and per-season AVERAGE, with his
#            BEST season raised to the >=6-game bar. The MINIMAL edit that makes his establishment certain.
#            Chosen deliberately as the CONSERVATIVE reading: it moves the least evidence, so it yields the
#            smallest comparator and therefore the LARGEST d_band — the reading least favourable to the
#            conclusion below. Two other readings are reported beside it and both point the same way.
# BOTH priced with the anchor UNDISCOUNTED (RL_336_DFORCE=1), so the anchor leg is identical for p and CE(p)
# and the ratio is exactly what the forward band and the price map take off for being unresolved.
#
#   MEASURED, value-weighted over the probe set (sum of prices, not a mean of ratios — the question is about
#   VALUE, and a mean of ratios is dominated by the 60% of the subset whose price the anchor cannot move at
#   all; both statistics are reported in the evidence):
#         d_band  =  0.707707        the band's OWN charge: a 29.2% discount, already applied
#         target  =  0.707455        the true class risk P(ever establishes), value-weighted on this subset
#         D       =  min(1, target/d_band)  =  0.999644
#
#   THE FINDING, and it is the one the directive named as a possible outcome: THE FORWARD BAND ALREADY
#   CHARGES ESTABLISHMENT FAILURE IN FULL. 0.7077 against a class risk of 0.7075 — the two agree to 0.04%.
#   The anchor owes essentially NOTHING further, and the reconciliation lands on its floor. Amendment 2's
#   anchor-side P on unresolved players was therefore a SECOND charge on top of a band that was already
#   pricing the whole risk — the same double charge Addendum 1 removed for establishers, one population over.
#   Robustness (all three comparator readings, total/target at this D):
#         minimal best-season->6g  (OPERATIVE)  d_band 0.7077   ratio 1.0004
#         every season->6g                      d_band 0.7007   ratio 0.9899
#         every season->18g (full exposure)     d_band 0.6240   ratio 0.8983   (band over-charges outright)
#
#   WHY POOLED AND NOT PER-CELL, declared. Per-cell d_band is n-driven noise at this sample (band 1: n=3,
#   d_band 1.105; band 4: n=20, d_band 0.443; band 7: n=211, d_band 0.685). Applying a pooled d_band against
#   per-cell P was MEASURED and it OVER-charges — total/target falls to 0.954. The reconciliation is
#   therefore stated and applied at the pooled level, one number, with its spread disclosed.
#
#   THE PASS-THROUGH, measured and NOT USED, recorded because it is the reason per-cell fails: scaling the
#   anchor by D does not scale the price by D. With the ramp held at r=0 to isolate it, 60% of the probe set
#   does not move AT ALL (priced off the fixed pick curve), and in aggregate the elasticity is 0.57 at D=0.8
#   and 0.24 at D=0.5 — strongly saturating, not a power law. No exponent is fitted or applied here: at
#   D = 0.9996 there is no discount left to pass through.
# ------------------------------------------------------------------------------------------------------------
A3_DBAND  = float(os.environ.get('RL_336_DBAND',  '0.707707'))   # PINNED: the band's own charge, measured
A3_TARGET = float(os.environ.get('RL_336_TARGET', '0.707455'))   # PINNED: the class risk it must total to
_RFORCE  = os.environ.get('RL_336_RFORCE')                # DECLARED MEASUREMENT ABLATION LEVER. Forces the
                                                          # resolution weight r to a constant. Its ONLY use is
                                                          # the pass-through derivation: with r free, forcing D
                                                          # moves the anchor by (D + r(1-D)), so a player who
                                                          # is 93% resolved barely moves and the price rounds
                                                          # to the same integer — the estimate would be a
                                                          # measurement of the ramp, not of the pass-through.
                                                          # RL_336_RFORCE=0 isolates D. Unset when reported.
_DFORCE  = os.environ.get('RL_336_DFORCE')                # DECLARED MEASUREMENT ABLATION LEVER (precedent:
                                                          # RL_ABSENCE, _merged_recover.py:684). When set, the
                                                          # anchor-side discount is FORCED to this constant for
                                                          # every real player — RL_336_DFORCE=1 is the
                                                          # UNDISCOUNTED-anchor build d_band is measured on.
                                                          # Unset on every reported build. Never a dial.
A3_D = min(1.0, A3_TARGET / A3_DBAND) if A3_DBAND > 0 else 1.0   # = 0.999644. The floor is min(...,1.0):
                                                                 # the anchor is never LIFTED above the
                                                                 # conditional level to make room for a band
                                                                 # that over-charges. Never negative.
def dpar_of(F, p):
    """#336 AMENDMENT 3: D — the anchor-side discount that survives the reconciliation.
        D = min(1, target / d_band)      target = the true class risk; d_band = what the band already takes
    Measured at 0.999644 (see the block above): the band already charges the whole class risk, so the anchor
    charges essentially nothing further. Kept as the general expression, not hard-coded to 1.0 — the same
    arithmetic would produce a real anchor discount on a build where the band under-charged, and that is the
    mechanism the amendment is asking for, not this particular number.
    P (pest_of) is NOT applied here any more: that is exactly the second charge this reconciliation removes.
    It is still applied, in full, to PICKS and synthetics via par_at() — they have no record to resolve and
    no band of their own, so they carry the entire entrant risk."""
    if _DFORCE is not None: return float(_DFORCE)
    return A3_D

# ============================ REPORT ============================
if __name__ == '__main__':
    F = fit()
    print(f"PAR estimator — cohort DRAFT {DRAFT_LO}-{DRAFT_HI} | additive (par=level+ramp, ramp[yr1]=0)")
    print(f"dials: bandwidth(log-pick)={H_LOGPICK}  par gate>={MIN_GAMES:.0f}g  ramps UN-POOLED (thin-cell protection in level kernel-ESS)")

    print("\n=== A. base play rate (median games among players who played) — pos x tenure ===")
    print("  pos        " + "".join(f"  yr{T}" for T in range(1,TEN_MAX+1)))
    for g in GROUPS:
        print(f"  {g:9s} " + "".join(f"  {F['base'].get((g,T),0):4.0f}" for T in range(1,TEN_MAX+1)))

    print("\n=== B. on-park sample (resolution map) — #players per pos x tenure ===")
    cnt = collections.defaultdict(int)
    for pos,x,T,lv in F['obs']: cnt[(pos,int(T))]+=1
    print("  pos        " + "".join(f"  yr{T}" for T in range(1,TEN_MAX+1)) + "   TOTAL")
    for g in GROUPS:
        tot = F['n_by_pos'][g]
        print(f"  {g:9s} " + "".join(f"  {cnt[(g,T)]:4d}" for T in range(1,TEN_MAX+1)) + f"   {tot:5d}")

    print("\n=== C. level_pos(log-pick) curve + kernel ESS at each eval point ===")
    print("  pos        " + "".join(f"  pk{p:<2d}" for p in EVAL_PICKS))
    for g in GROUPS:
        row=[]; 
        for pk in EVAL_PICKS:
            lv,ess = level_at(F,g,pk); row.append((lv,ess))
        print(f"  {g:9s} " + "".join(f" {lv:5.1f}" for lv,_ in row))
        print(f"   (ESS)    " + "".join(f" {ess:5.1f}" for _,ess in row))

    print(f"\n=== D. tenure ramp per position — RAW vs GLOBAL vs SHRUNK (n/(n+{SHRINK_K:.0f})) ===")
    print("  global ramp:        " + "".join(f"  yr{T}:{F['gramp'][T]:+5.1f}" for T in range(1,TEN_MAX+1)))
    for g in GROUPS:
        n=F['n_by_pos'][g]; w=F['sw'][g]
        raw_s  = "".join(f" {F['ramp'][g][T]:+5.1f}" for T in range(1,TEN_MAX+1))
        shr_s  = "".join(f" {F['ramp_shr'][g][T]:+5.1f}" for T in range(1,TEN_MAX+1))
        flag = "  <-- POOLED (thin)" if w < 0.8 else ""
        print(f"  {g:9s} n={n:4d} w={w:.2f}")
        print(f"     raw   {raw_s}")
        print(f"     shrunk{shr_s}   (yr1->yr5 delta = {F['ramp_shr'][g][5]-F['ramp_shr'][g][1]:+.1f}){flag}")

    print("\n=== E. assembled par(pos,pick,tenure) — sample cells ===")
    print("  pos        pk |  yr1   yr2   yr3   yr4   yr5")
    for g,pk in [('MID',7),('MID',1),('SD',14),('KPD',8),('KPF',4),('RUCK',20),('SF',12)]:
        print(f"  {g:9s} {pk:2d} | " + " ".join(f"{par_at(F,g,pk,T):5.1f}" for T in range(1,6)))

    print("\n=== F. ANCHOR RECONCILIATION — MID yr1, picks 1-8 should ~= 66 (cont.26 §2) ===")
    lv18 = np.mean([level_at(F,'MID',pk)[0] for pk in range(1,9)])
    print(f"  mean level_MID(yr1) over picks 1-8 = {lv18:.1f}   (cont.26 empirical par = 66.0)")
    print(f"  level_MID(yr1) @pk7 = {level_at(F,'MID',7)[0]:.1f}   (Cumming's pick; cont.26 break-even@20g = 66)")

    print("\n=== E2. #336 AMENDMENT 2 — THE TWO ANCHORS SIDE BY SIDE (established vs unresolved) ===")
    print("  the SAME cell, priced for a player who HAS established and for one who has NOT.")
    print("  the ratio between them IS P(ever establishes) — the resolved/unresolved seam, disclosed.")
    print("  pos    pk band     |  yr1 est/unres    yr2 est/unres    yr4 est/unres      P")
    for g,pk in [('MID',7),('MID',1),('MID',60),('SD',14),('KPD',8),('KPF',4),('KPF',46),('RUCK',20),('SF',12)]:
        _b = MA.bandof(pk); _p = F['pest'][(g,_b)]
        cells = "".join("   %5.1f/%-5.1f " % (par_at(F,g,pk,T), _p*par_at(F,g,pk,T)) for T in (1,2,4))
        print(f"  {g:6s} {pk:2d} {('%d-%d'%tuple(MA.BANDS[_b])):7s} |" + cells + f"  {_p:6.3f}")

    # ==== #336 VARIANT (ADDENDUM 1) — G. P(ever establishes) DISCLOSURE: every rate names its denominator ====
    print("\n=== G. #336 VARIANT (ADDENDUM 1) — CAREER-LEVEL P(ever establishes) per (position x pick-band) ===")
    print("  AMENDMENT 2: this P is applied ONLY to UNRESOLVED players now — it is no longer folded into")
    print("               the surface. An established player takes the conditional level with no discount.")
    print(f"  establishment bar >= {QUAL_338}g in ANY season inside the #338 listed window (build_cohort_book.py:181-185)")
    print(f"  denominator = the #338 tenure-windowed cell population (s4_matrix_M1v7.py:53-70); tenure enters")
    print(f"                ONLY as window MEMBERSHIP — it is NOT a probability index (Addendum 1, 2026-08-06)")
    print(f"  pooling     = shrink toward the ALL-POSITION band marginal by n/(n+{K_338:.0f})")
    _den = F['pest_den']; _num = F['pest_num']
    _ns = sorted(_den.values())
    print(f"  strata filled {len(_den)} | n min={_ns[0]} median={_ns[len(_ns)//2]} max={_ns[-1]}"
          f" | n<20: {sum(1 for v in _ns if v<20)}  n<10: {sum(1 for v in _ns if v<10)}  n<5: {sum(1 for v in _ns if v<5)}")
    print("    pos        " + "".join(f"{('%d-%d'%tuple(MA.BANDS[b])):>9s}" for b in range(MA.NB)))
    for g in GROUPS:
        print(f"    {g:<10s} " + "".join(f"  {F['pest'][(g,b)]:7.3f}" for b in range(MA.NB)))
        print(f"    {'  (est/n)':<10s} " + "".join(f"  {('%d/%d'%(_num.get((g,b),0),_den.get((g,b),0))):>7s}"
                                                  for b in range(MA.NB)))
    _an = {b: sum(_num.get((g,b),0) for g in GROUPS) for b in range(MA.NB)}
    _ad = {b: sum(_den.get((g,b),0) for g in GROUPS) for b in range(MA.NB)}
    print(f"    {'ALL-POS':<10s} " + "".join(f"  {(_an[b]/_ad[b] if _ad[b] else 0.0):7.3f}" for b in range(MA.NB)))
    print(f"    {'  (est/n)':<10s} " + "".join(f"  {('%d/%d'%(_an[b],_ad[b])):>7s}" for b in range(MA.NB)))
