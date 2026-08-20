# PREREG_S2 — ORDER 32, SEAT S2: THE SITTER SPECTRUM SURFACE. PRE-REGISTRATION.

**Committed BEFORE the harness `o32s2_spectrum.py` existed in runnable form and before any cell of any
result was counted.** Program brief: #334 comment 5311991190. Owner scope ruling (2026-08-17): *"it
shouldn't be a limited measurement... sitting is a spectrum (0 games to 1 game isn't that different
from 1 to 2)."*

**READ-ONLY MANDATE.** This seat measures and reports. No engine file, no board, no store, no curve
moves. Every credit/restoration/recency/injury term this act produces is a **WIRING PROPOSAL AWAITING
RULING**, never a decision. The wired candidate law (`o31_played_units` full-unit credit for any
games>0) stands untouched; its defect is owner-caught and on the record
(`docs/evidence/candidate_31f/ext_2026-08-17/README_EXT.md`) — this act measures its **replacement**,
it does not re-litigate the finding.

## 0. THE INSTRUMENT AND ITS BASIS — NO PARALLEL METHODOLOGY

The 30A-2 estimator lineage is **transplanted, not re-implemented**: `o32s2_spectrum.py` will exec
`docs/evidence/sitter_fade_2026-08-14/o30a2_recut.py` **WHOLE** (the o31_pool.py / o31f_rederive_fade.py
discipline), with exactly one character-level substitution — `OUTD = HERE` re-pointed into this act's
directory so no committed artifact is overwritten — and then harvest that namespace: the population
(`FIT`, ND 1-64, attributed, 2004–2021 fitted window, v0>0), the listing basis (`listed_LB`, the #338
minimum-tenure rule, L-B outcome-blind floor, per the standing ruling), the per-season decomposition
(`PTS`, `share_from`, `t4_cell`: `V_from_N = (ga_obs·s_N + ga_tail)·DF(N−1)`), the normaliser
`RAW(1)`, and the quantile/dispersion machinery. Every number in this act is produced by the committed
instrument's own estimator evaluated on new conditioning cells.

**Pins expected at entry** (the harness's own asserts must pass): Layer 1 `ad1229ea`, store `cb38ef11`,
rl_model `14000af2`, pvc_curve_v2 `78ad9842` (= the 31-F HEAD-FIXED surface — verified equal to the
md5 printed in `FADE_31F_out.txt` before this prereg was filed), `data/season_state.json`
calendar_progress 0.92.

**Definitions, fixed now:**
- Season index `k = year − entry_year`, k ≥ 1 (ND debut = entry+1). `g_k` = games in season k
  (`games_in`). At depth N, seasons 1..N−1 are completed (`entry_year + N − 1 ≤ 2025`).
- A **gameless** season: `g_k = 0`. `s` = count of gameless seasons among 1..N−1.
- **D-cell** (verbatim 30A-2 T4): `D = mean( (ga_obs·s_N + ga_tail)·DF(N−1) / v0 ) / RAW(1)` over the
  cell's rows, L-B listed at N. Dispersion always: n, median, p25, p75, n_zero, tail_share.
- **Delivered season k** (the engine's own stall/delivery bar, `o31_stall_run` semantics carried to
  the DV lane's season bars): `g_k ≥ 10` AND `avg_k ≥ BARS[season_bar_group]` for completed seasons;
  for the in-progress 2026 season, `g ≥ 10 × calendar_progress` AND avg ≥ bar.
- **MIN_CELL = 10**: a cell with n < 10 is published as a **BOUND**, never quoted as a law and never
  smoothed into a fit.
- Named rows through the surface: josh-smillie, lachlan-carmichael, phoenix-gothard, billy-wilson,
  will-green, william-mccabe, charlie-edwards, alex-dodson.

## 1. THE FOUR QUESTIONS — METHOD, FIXED BEFORE COUNTING

**Q1 — THE CREDIT FUNCTION / SATURATION G\*.** Cells: depth N ∈ {2,3,4}; **pattern-restricted**:
seasons 1..N−2 all gameless, season N−1 carries g games, g bucketed {0, 1, 2, 3-5, 6-10, 11+}; at
depth 2 additionally per-game g = 0..5 singletons. (Depth 2 has no prior seasons, so its cells are
exactly T4's transition — a built-in control.) The measured `D(N, g)` is inverted against **this act's
own pure-sitter L-B row** (continuous, log-linear, the 31-F re-derived values) on its decreasing
branch to an implied unplayed clock `ĉ_u`, giving **credit units cured** `û(g) = N − ĉ_u`, per cell.
Cells with D > 1.0 (pedigree exceedance, seen in T4) are flagged SATURATED-FULL, not inverted. The
candidate replacement family, fixed now: `u(g) = min(1, g/G*)`; G\* fitted by n-weighted least squares
on all non-thin, non-saturated cells at depths 2 and 3, over grid G\* ∈ {1.0, 1.5, …, 30.0}. Residuals
reported in both unit- and D-space. The backbone's 6–10 saturation hint is tested by comparing û(6-10)
with û(11+).

**Q2 — RESTORATION.** Sat group: rows with ≥1 gameless season among 1..k−1 and a **delivered** season
at k. Control group: rows with **zero** gameless seasons among 1..k−1 and a delivered season at k.
Estimand: `R(k) = D_sat(k+1-on) / D_ctrl(k+1-on)` where each D is the transplanted from-(k+1) cell,
L-B listed at k+1; pooled over k = 2..5 and per-k where both cells clear MIN_CELL. R ≈ 1 = full
restoration of pedigree persistence; R ≈ the fade ratio = the faded level is sticky. Secondary,
weaker bar: "substantial season" `g_k ≥ 10` regardless of avg (published beside, since delivered
cells may be thin). Split by prior sat count (1 vs 2+) where n permits.

**Q3 — ORDER/RECENCY.** At depth N ∈ {3,4}, at **fixed s**, split by the position of the gameless
seasons: most-recent completed season (N−1) gameless ("sat-recent") vs most-recent played
("sat-early"). Headline contrast, the one with usable n: **N=3, s=1 — (0,g) vs (g,0)**. The owner's
4-0-0 vs 0-0-4 is the N=4, s=2 contrast — (g,0,0) vs (0,0,g) — published with its n whatever it is.
Confound disclosed per cell: the games distribution inside the played seasons of each pattern.

**Q4 — THE INJURY SPLIT.** Ground truth: `LTI_REGISTER.md` (R-REG, pinned, owner-maintained,
2025/2026 windows only — verified before this prereg: no historical injury source exists anywhere in
the repo; the store carries no injury field). Method: (a) parse the register; classify every
**sit-season observable to it** (2025 designations → 2025 season; 2026/2026_preseason → 2026);
(b) count, per fitted surface cell, the fraction of sit-seasons whose cause is register-resolvable —
the historical resolution, expected ≈ 0, **reported as a number, not hidden**; (c) classify the
CURRENT (2026) sitting of every live ND-entrant row at accrued c_u ≥ 1, injured (in-register) vs
healthy-unselected (absent — meaningful, because the register is curated ground truth for 2025/26);
(d) the named rows classified individually. **What this act will NOT do:** infer historical injury
from performance patterns and present it as a cause measurement. The Q3 sat-early/sat-recent split is
the closest observable proxy (the register's own exemplar semantics: established→zero is the injury
shape) and will be cross-referenced as a PROXY, labelled as such. If the historical split is
unmeasurable, that **null is a result** and the pooled fade row is published with an explicit
mixture-bound statement.

**THE TWO-WAY SURFACE (the owner's object).** For each depth N ∈ {2,3,4}: the full grid
s (gameless count 0..N−1) × total games G in played seasons (0/1-2/3-5/6-10/11-20/21+) → D, every
cell with n and dispersion, thin cells flagged. Q1/Q3 are cuts of this surface; it is published whole.

**Named rows:** current continuous fade clock c (φ=0.92), wired c_u (full-unit credit) vs proposed
c_u (fitted `min(1, g/G*)` credit), D under each, × 29B flat v0 — arithmetic on a packet, nothing
wired.

## 2. PREDICTIONS AND FALSIFIERS — NUMBERED, SCORED IN THE PACKET

- **S1 (control).** The whole-harness rerun on this HEAD reproduces the 31-F re-derived L-B row to
  <1e-9: D(2)=0.5582775, D(3)=0.2747858, D(4)=0.3972709, and T4's depth-2 transition cells likewise.
  FALSIFIER: any deviation ≥1e-9 = the transplant is broken; HALT, fix, nothing downstream is quoted.
- **S2.** Depth-2 per-game: D(g=1) − D(g=0) ≥ 0.15, with D(1) ∈ [0.75, 1.05].
- **S3.** The single-game steps beyond the first are each smaller than the 0→1 step:
  D(2)−D(1) < D(1)−D(0), and each per-game step for g ∈ {2..5} is < 0.10 in D. (The owner's "0→1 isn't
  that different from 1→2" is TESTED here: I predict the first game still carries the largest single
  step; if D(2)−D(1) ≥ D(1)−D(0) the owner is right and the packet says so.)
- **S4.** n at depth-2 singleton cells: n(g=1) ∈ [30,90], n(g=2) ∈ [25,80].
- **S5.** Depth-3 pattern (0,g): D rises with g, and D(N=3, g∈6-10) ≥ 0.55 — one substantial season
  after a sat year prices at or above the one-year-sitter level (a season's sitting is roughly cured
  by ~a season of games). FALSIFIER: D(3, 6-10) < 0.45.
- **S6.** The fitted G\* ∈ [5,12] (the 6–10 backbone hint). FALSIFIER: G\* outside [3,16] = the
  min(1,g/G\*) family is wrong or saturation is not where the backbone hints.
- **S7.** û(11+) − û(6-10) ≤ 0.15 units — saturation, not linear growth in g.
- **S8.** û(1) ∈ [0.10, 0.50] — i.e. the wired full-unit credit at g=1 overstates the cure by ≥2×.
  This is the headline replacement number for the owner-caught defect.
- **S9.** Fit quality: RMS residual of `min(1, g/G*)` over used cells ≤ 0.12 in D-space.
- **S10 (restoration).** Pooled R ∈ [0.75, 1.05]. FALSIFIERS both ways: R < 0.55 = restoration fails
  (fade is sticky through delivery); R > 1.15 = selection artifact suspected, quoted only as a bound
  with the suspicion named.
- **S11.** Pooled sat-then-delivered n ∈ [40, 160].
- **S12.** The 2+-prior-sat delivered cell is thin (n < 10) and is published as a bound.
- **S13 (recency).** At N=3, s=1: D(sat-early (g,0)) < D(sat-recent (0,g)) — no wait, stated
  carefully: **the row sitting NOW prices below the row playing NOW.** Pattern (g,0) [played year 1,
  sat year 2 — sitting now] prices BELOW pattern (0,g) [sat year 1, playing year 2 — playing now], by
  ≥ 0.10 in D. FALSIFIER: gap ≤ 0 = recency does not matter in the owner's suspected direction; the
  current order-blind law stands supported.
- **S14.** The N=4 patterns (g,0,0) and (0,0,g) are both thin (n < 10 each) → bounds, not laws.
- **S15 (injury).** Historical resolution: < 2% of fitted-window sit-seasons are register-resolvable.
  The historical injured-vs-unselected fade split is therefore UNMEASURABLE on this repo's data — a
  null published as a result, with the mixture bound stated.
- **S16.** Of the 8 named rows, the register classifies **0** as injured (none appear in it).
- **S17.** Among live ND-entrant rows currently sitting (2026 gameless, c_u ≥ 1), the register marks
  between 5% and 25% injured.
- **S18 (named rows).** Under the fitted credit: lachlan-carmichael's D falls from the wired ~1.00
  back to ≤ 0.75 (one game cures ≤ 0.2 units at G\* ≥ 5); will-green likewise (1 game);
  phoenix-gothard (15 games) retains ≥ 0.9 units of credit for 2026; billy-wilson (4 then 13 games)
  retains most credit both years. Gothard's 2026 (15 g @ 68.8) and Wilson's 2026 (13 g @ 73.5)
  qualify as DELIVERED under the position bar; if the bar says otherwise the packet reports it.
- **S19.** Dispersion shape: p25 = 0 in every g=0 cell; p25 > 0 in every depth-2 cell with g ≥ 3.
- **S20.** The two-way surface at depth 3 and 4 is **not** monotone in every axis-direction cell pair
  (spike-plus-tail noise at these n's); the packet reports directionality per axis, not a smoothed
  surface.
- **S21 (conduct).** The harness writes only into `docs/evidence/order32_s2_2026-08-17/`; two runs
  byte-identical (md5s printed); no engine/board/store/curve file is touched.

## 3. EXCLUSIONS, NAMED IN ADVANCE

As the transplanted instrument's own: non-ND-1-64 mechanisms, pre-2004 (DV floor), 2022+ entries
(sensitivity, not fitted — the named rows all sit here and are priced THROUGH the surface, never in
it), v0 ≤ 0 rows. Cells emptied by the pattern restriction are printed with n=0, never dropped
silently. Censoring: the projected tail (`ga_tail`) is assigned wholly to from-N, as T4; tail_share
printed per cell; a cell with mean tail share > 0.375 carries the 30A CENSOR-3 flag.

*Seat S2, ORDER 32. Filed before computation. The packet scores every S-number, breaches owned.*
