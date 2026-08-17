# PREREG — ORDER 33 SEAT W4: THE TRAJECTORY NULL, RE-POSED ONCE AT FULL POWER

**Filed BEFORE any result is computed.** Everything below this line was written from schema
inspection, the lineage documents quoted in §1, and one sample-size census (player count, season-row
count, count of players with 3+ played seasons — no outcome, no delta, no slope, no cell mean was
computed). Results computed before this file's push are void by house law. This seat is READ-ONLY:
no engine code, no board, no law is touched.

Seat: W4 (measurement). Program brief: issue #334 comment 5312369107.
Branch: `land/order-29` at commit `441b7990` (tree `c4d86cb0`).

---

## 1. THE NULL BEING RE-POSED — QUOTED, NOT PARAPHRASED

The candidate law prices production evidence as an evidence-weighted **LEVEL** (output vs the
position bar, age-projected). It prices 40→55→70 identically to 70→55→40 at equal evidence weight.
The standing null that licenses this came from the ORDER 30B-M pedigree-persistence measurement
(re-run under 31-F), and this seat's first duty is to state exactly what that null was and was not.

**Original construction** (`docs/evidence/pedigree_persistence_2026-08-14/o30bm_measure.py`;
results in `PEDIGREE_PERSISTENCE_PACKET.md` §3 and `docs/evidence/candidate_31f/PERSISTENCE_31F.json`
`q2_form`):

- Panel: one state per played season end; **ND draftees, picks 1–64, entry ≥ 2005 only**; target
  fully observed ⇒ state years ≤ 2019. **n = 4,033 season-states.**
- Target: `R` = discounted delivered value over the **next H=6 seasons** (engine scorer points,
  disc 0.14, missing seasons = 0).
- Forms: `P` production-only (16 params: pos dummies + age, age², log1p(g), o, o², cur, cur3,
  games_at_Y, o·age, cur·age) · `L` = P + v0 + v0·log1p(g) (18 params) · `T` = L + **pick-class
  (hi/lo) × {age, age², o, cur, lg} interactions + class dummies** (30 params).
- Decision rule (preregistered there): adopt the richer form iff held-out RMS reduction ≥ 2.0% AND
  ≥ 4/5 player-clustered folds won.
- **Result:** L→T reduction **−0.02%**, **2/5 folds** (30B-M packet: L 709.42 vs T 709.53); 31-F
  re-run: L 710.95 vs T 710.58, reduction +0.05%, 2/5 folds, `adopt_richer=false`. Time-block
  (fit ≤2012, test ≥2013): L 718.92/719.19 vs T 724.94/724.29 — **T degrades out of era**.
  Prereg item P6 HELD: "trajectory does NOT clear the 2.0%/4-of-5 bar."
- The packet's own honesty clause, quoted: *"the trajectory question cannot be settled by cells —
  there are not enough of them, which is itself the honest answer to Q2."*

**What the original T was and was not.** It was a **pick-conditional** trajectory: 12 extra
parameters asking whether the growth curve differs by pedigree class. It was NOT a direct test of
the within-career shape itself. Two further dilutions the re-pose must remove:

1. **The age confound.** No form adjusted season-over-season change for the population age
   expectation; a 20-year-old's rise and a 30-year-old's fade were both left inside `cur` vs `cur3`
   raw. The improvement signal, if any, was fighting the age curve for identification.
2. **A 12-df interaction block on 4,033 ND-only states.** Power was spent on the pick interaction,
   not on the one scalar question: does direction of travel, per se, predict beyond level?

Note also, for honesty in BOTH directions: the base form already carried `cur` (this season) and
`cur3` (mean of last 3) as free covariates, so a crude 2-season level contrast was linearly
spanned in every form, including L. The original null therefore already says something about raw
recent-vs-older weighting. What it never tested is the object this seat constructs: **the
age-adjusted within-player slope, as a single degree of freedom, against the BEST level-only
weighting, on the whole store.**

**Distinguish from the recency-clock failure (different object).** ORDER 30B-R T2 tested a
recency-weighted **evidence clock** `u = Σ games·0.25^(Y−y)` as a replacement for raw career games
inside the pedigree blend, and it **lost its own preregistered criterion** (OOF RMSE 722.87 vs
715.15; `one_machinery_2026-08-14/resolution/BLEND_RESOLUTION_PACKET.md`). That clock weights HOW
MUCH is known (games), saturates at 26.67, and destroyed durability information. This seat's object
weights nothing about the clock: it asks whether the SHAPE of the production series carries forward
signal. A verdict here neither rescues nor re-condemns the 30B-R clock, and vice versa.

---

## 2. DATA AND DEFINITIONS (all fixed before computation)

- **Store:** `engine/rl_after/rl_model_data.json` on this tree — 2,650 players, seasons 2005–2026,
  11,340 played season rows, 1,389 players with 3+ played seasons (the pre-registration census; md5
  pinned in the build output). `data/season_state.json`: 2026 in progress at fraction 0.92.
- **Pooling:** ALL players with the needed seasons — every entry type (ND, rookie, pickless, all
  eras in store 2005–2026), not ND 1–64 only. Power is the point of the re-pose.
- **AGE** = season year − `_by` (house convention, S1 precedent).
- **POS** (bar key) = season `pos` label collapsed by the engine's `_collapse_elig` to the
  cheapest-bar eligible group, fallback `future_position` (the o30bm `bar_group` convention).
- **SEASON POINTS** `P(k,y)` = the engine's pinned scorer, staged read-only exactly as o30bm stages
  it: `SCALE · posval(avg + capt_prem(avg) − BAR[pos]) · 21 · min(1, sqrt(games/10))` — identical
  to the original test's `cur`, asserted against Ruling-1 bars. 2026 never contributes to any
  outcome (in progress).
- **STATE:** every (player, year Y) with **played seasons at both Y and Y−1** (consecutive; a
  missed year breaks the pair), age known. This is the panel; per-target windows below.
- **TRAJ (the tested variable):** age-adjusted last-2-season slope
  `TRAJ(Y) = [P(Y) − P(Y−1)] − d(age_Y, pos)` where `d(a,pos)` is the population age-expected
  one-season change: mean of `P(y)−P(y−1)` over all consecutive pairs at age `a` (age at the later
  season) in position group `pos`, ages binned 17-or-less, 18, 19, …, 33, 34-plus, shrunk toward
  the all-position age mean with weight n/(n+50) where a pos×age cell is thin. Inside the CV, `d`
  is re-estimated on TRAINING folds only (folds are player-clustered, so no player's own pairs
  inform his own adjustment); the full-sample coefficient fit uses the full-panel `d`. The `d`
  curve itself is reported (it is the measurable age curve the brief names, Order 32 S1 build
  precedent).

### Targets

- **(a) PRIMARY — next-season output:** `Y1 = P(k, Y+1)`, **zero if not played** (exit is part of
  delivered value). States with Y+1 ≤ 2025.
- **(b) SECONDARY — 3-year forward delivered value:** `R3 = Σ_{j=1..3} P(k,Y+j)/1.14^j`, states
  with Y+3 ≤ 2025.
- **(c) SECONDARY — the ORIGINAL target on the pooled panel:** `R6 = Σ_{j=1..6} P(k,Y+j)/1.14^j`,
  states with Y+6 ≤ 2025 (i.e. Y ≤ 2019) — direct comparability with the 30B-M/31-F null.

### The two forms (the comparison that binds)

Controls, identical in both: pos dummies, age, age², log1p(career games through Y), games_at_Y.

- **L\* — the BEST level-only form (the anti-strawman benchmark):**
  controls + `L_w`, `L_w²`, `L_w·age`, where `L_w = (P(Y) + w·P(Y−1) + w²·P(Y−2)) / (1 + w + w²)`
  (P(Y−2) term dropped and weights renormalised when that season wasn't played), and **w is chosen
  on the training rows of each fold** from the grid {0.0, 0.1, …, 1.0} by training RMS. This family
  spans "the current season is a noisy read of the level" (w→1 pools; w→0 trusts the latest): the
  mean-reversion trap is absorbed HERE, not left for trajectory to fake. Chosen w per fold is
  reported.
- **T\* — level plus trajectory, ONE added degree of freedom:** L\* + `TRAJ`.

Fit: OLS on standardised columns, 5-fold player-clustered CV (fold = stable hash of player key mod
5, deterministic, no RNG), same machinery as the original. Full-sample fit with player-clustered
(CR1) SEs for the coefficient read. Player-clustered bootstrap (B=1000, seed 0) CIs on the TRAJ
coefficient and on all subgroup/quantile effects.

---

## 3. DECISION RULE — WHAT OVERTURNS, WHAT CONFIRMS (binds; no design-shopping after results)

All confirmatory weight sits on **target (a), L\* vs T\*, held-out**. Named outcomes:

- **O1 — ADOPTION-GRADE OVERTURN:** held-out RMS reduction ≥ **2.0%** AND ≥ **4/5** folds won —
  the original bar, unchanged. Then the null is overturned outright and wiring is sketched.
- **O2 — REAL-BUT-SMALL SIGNAL:** cluster-robust **|t(TRAJ)| ≥ 3.0** on the full-sample fit AND
  the fitted TRAJ coefficient has the **same sign in ≥ 4/5 training folds** AND held-out RMS
  reduction > 0. Then trajectory carries information the level does not; it is sized (points per
  1 SD of TRAJ, and per 100 raw slope points), localised (age band, level tercile, sign of slope,
  games band, era), marked **AWAITING RULING**, and it is stated plainly whether it clears the
  adoption bar (per O1) or not.
- **O3 — NULL CONFIRMED:** |t(TRAJ)| < 3.0 on target (a). The null is confirmed at a panel that
  is larger, age-adjusted, single-df, and benchmark-hardened; the seat writes the register-ready
  sentence recommending it be accepted as settled. Secondary targets and quantile reads are then
  descriptive only and **cannot** overturn.
- **O4 — AMBIGUOUS:** |t| ≥ 3.0 but sign-unstable across folds or held-out RMS worse. The null
  STANDS (trajectory does not improve prediction); the instability is reported, not spun.

Secondary targets (b), (c) and all subgroup/quantile reads can **localise** a primary signal but
can never overturn a primary null. If (c) on the ND-only subpanel disagrees with the original
recorded numbers by more than re-run noise, that is reported as a discrepancy, not silently
absorbed.

### Preregistered secondary reads (reported whatever the verdict, with dispersion)

1. **Quantile reads:** linear quantile regression (pinball loss) at q10 / q50 / q90 on target (a),
   L\* covariates ± TRAJ; report the TRAJ coefficient per quantile with bootstrap CIs — does
   trajectory matter more for the tails than the mean?
2. **Sign asymmetry:** TRAJ⁺ / TRAJ⁻ split coefficients (improvers vs decliners priced
   separately).
3. **Owner-readable sort:** within age-band × L_w-quintile cells, states split by TRAJ tercile;
   mean / median / p25 / p75 of (a) and (b) per tercile, plus next-season exit rate (share with
   Y1 = 0). Full table, thin cells shown with their n, never hidden.
4. **Age localisation:** TRAJ coefficient by age band (≤21, 22–25, 26–28, 29+).
5. **Rank terms:** held-out Spearman for L\* and T\*; mean |Δ percentile rank| between the two
   predictions (how much would prices actually move).

### Preregistered sensitivities (listed in advance; none may replace the primary)

- s1: slope from **raw avg** (not points) with games ≥ 6·u in both Y and Y−1 (kills the
  games-weight artefact where a 20-game→5-game season fakes a fade).
- s2: 3-season slope `[P(Y) − P(Y−2)]/2` age-adjusted, where Y−2 played.
- s3: **ND 1–64, entry ≥ 2005 subpanel** on target (c) — the original panel, for continuity.
- s4: era split ≤2014 / ≥2015 (descriptive).
- s5: w-grid refinement {0.0, 0.05, …, 1.0} (checks grid coarseness only).
- s6: add linear `year` to controls (era drift guard).

### Power statement (why this re-pose is stronger, written before results)

Target (a) pools every consecutive-pair state in the whole store (expected order 7–9k states,
~2k players — exact n reported in the census step) vs 4,033 ND-only states on a 6-year window;
the test is 1 df instead of 12; the age confound is removed by construction; and the benchmark is
the best convex level-weighting rather than a single-season strawman. If TRAJ still fails a |t|≥3
read here, the question has had its properly-powered day in court.

### Void conditions

- Any outcome-bearing number computed before this file's push: void.
- Any post-hoc change to the w-grid, fold scheme, shrinkage k=50, age bins, bar values, or
  decision thresholds: void, unless filed as a named amendment with reason BEFORE the affected
  run.

*Prediction (seat's own, non-binding, filed for honesty): most likely outcome is O3 or a small
NEGATIVE TRAJ read (extra mean reversion beyond the level), because the 31-F time-block already
showed T degrading out of era; but that expectation exerts no force on the rule above.*

---

## AMENDMENT A1 — filed 2026-08-17, BEFORE the measurement run (w4_measure.py has not executed)

The bootstrap for the QUANTILE-regression TRAJ coefficients (secondary read 1 only) is reduced
from B=1000 to **B=200**. Reason: one pinball LP at the panel's size was timed at ~4.5 s on a
synthetic same-shape problem (no panel data touched); 3 quantiles × 1000 cluster resamples ≈ 3.8
hours exceeds the seat's runtime budget, while B=200 (~45 min) still gives a serviceable 95% CI on
a secondary, descriptive read. ALL OLS bootstraps (primary TRAJ coefficient, secondary targets,
sign split, age localisation, pooled sort-table gap) remain at the preregistered **B=1000, seed
0**. No point estimate, threshold, or decision rule changes. The quantile point estimates
themselves are computed exactly as preregistered.
