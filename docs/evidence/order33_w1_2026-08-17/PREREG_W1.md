# PREREG_W1 — ORDER 33 seat W1: the DEEP END of beta, re-measured with more power

**Committed and pushed BEFORE any measurement number exists. Read-only seat: no engine, board or law
file is touched. Program brief: #334 comment 5312369107.**

## 1 · Object and registered prior

The object is the deep end (g >= ~40) of the wired additive pedigree-persistence curve
`O31_BETA` (`engine/rl_after/_merged_recover.py:3188`):

    (2.5 -> 0.2879) (10.5 -> 0.2879) (25.5 -> 0.2177) (53.0 -> 0.1416) (85.5 -> 0.0238)

derived in `docs/evidence/candidate_31f/` (BETA_31F.json; harness = the 30B-M panel run whole on the
head-fixed v0 surface). The 71+ band there is statistically indistinguishable from zero
(beta 0.0238, se 0.0474, t 0.50, n=1339, 297 clusters).

**Registered prior (Order 32 seat S4, `docs/evidence/order32_s4_2026-08-17/`):** the candidate loses
years 4–6 rank skill to the old flat-pedigree law on both horizons with clean 90% CIs (Δρ −0.008 to
−0.023), while raw pick alone still holds Spearman 0.25–0.31 there. Reading: pedigree signal persists
deeper into careers than the wired beta pays; the fade after ~40 games looks too aggressive. This
prior is why the deep end is being re-measured; it is NOT allowed to move the estimator — every
estimator below is fixed here before any number is seen.

## 2 · Instruments (all run whole, declared substitutions only)

* **W1-CONTROL** — `o31f_rederive_beta.py` lineage: the 30B-M harness (`o30bm_measure.py`, committed
  md5 e910fe6482ab7b05a92f18c173667073) exec'd whole with the SAME four 31-F substitutions (head-fixed
  v0 source, POSV key, output paths) except the outputs land in THIS seat's directory, never
  overwriting `candidate_31f/`. **Must reproduce BETA_31F.json's five band coefficients at deviation
  0** (same code path, same pins, same seeds) or the seat STOPS.
* **W1-DEEP** — the SAME harness source exec'd to the end of its panel construction (`ROWS`,
  `build_states`, `panel`, `band_fit`, `cluster_se`, `q` lifted from the executed namespace, not
  re-implemented), then the estimators of §3 run on that panel. Every departure from the 31-F
  construction is listed in §3 and justified there; anything not listed is carried unchanged
  (population ND 1–64 entry>=2005, H=6 target Y<=2019, zeros stay in, player clustering,
  head-fixed v0, force-majeure exclusions, Ruling-1/Ruling-3 scorer).
* **W1-CF-EMIT** — the ORDER 31-F emitter (`emit_matrix_31f.py`) and runner conventions
  (`emit_variant_o31f.sh`) run whole from a detached scratch worktree of THIS tree
  (engine 71d9949a = the exact engine that produced `per_entrant_O31FFINAL.json`), with ONE declared
  substitution in the worktree's engine copy only: the `O31_BETA` tuple replaced by the proposed
  curve of §4 (exact original string asserted to occur exactly once). `O31_BETA_POOL`, `O31_PHIST`,
  `O31_FADE_D`, rho and every other constant untouched. RL_O31=1; day-0 replication guard stays live
  (day-0 prices have g=0 and cannot move — the guard passing is required).
* **W1-CF-SCORE** — `s4_shootout.py` (Order 32 S4, prereg-bound rules) exec'd whole with two declared
  substitutions: `CAND_P` -> the counterfactual matrix; output path -> this directory. B=2000,
  seed 32, verdict rule, cohorts, metrics all carried untouched from PREREG_S4.md.

Environment: `/root/rl_venv312/bin` python, PYTHONHASHSEED=0, five-var thread pinning, numeric runs
strictly sequential.

## 3 · Estimators for the deep end (fixed now)

* **E1 — finer deep bands, harness estimator verbatim.** `band_fit` (the 31-F object: within-band
  OLS of R on [pos dummies, age, age2, o, o2, cur, cur3, games_at_Y, lg] + v0, CR0 cluster SE on
  player) run on games bands `0-5, 6-15, 16-35, 36-50, 51-70, 71-90, 91-120, 121+` (midpoints
  2.5, 10.5, 25.5, 43, 60.5, 80.5, 105.5, and the 121+ band's empirical mean g). Departure from
  31-F: the two deep bands 36-70 / 71+ are split into five. Justification: localisation — the 71+
  band spans 71..350+ games and its single coefficient can hide a positive 71–100 shelf.
* **E2 — pooled-power H=4 panel.** The identical panel construction with `H=4` (full window
  requires Y<=2021), adding the 2020–2021 state-years, scored on the same discounted remaining-value
  target at the shorter horizon. Same bands as E1 plus the original 36-70/71+ split. Departure:
  horizon. Justification: statistical power at the deep end (~35–45% more deep states); H=6 remains
  primary; E2 is a robustness/power check and is reported beside E1, never averaged with it.
* **E3 — PRIMARY: joint monotone-constrained fit.** One regression on the FULL H=6 panel:
  R ~ [pos dummies, age, age2, o, o2, cur, cur3, games_at_Y, lg, fine-games-band dummies]
  + v0 · h_k(g), where h_k are the log-g piecewise-linear hat functions at the wired knots
  (2.5, 10.5, 25.5, 53.0, 85.5) with the outer knots clamped (g<=2.5 -> knot 1, g>=85.5 -> knot 5,
  matching `_o31_loglin`'s clamping). The five fitted coefficients b_k ARE the knot values of an
  additive pedigree curve estimated jointly, borrowing strength across adjacent bands through the
  shared control surface. 90% CIs by player-cluster bootstrap, B=400, seed 33. Then the isotonic
  non-increasing projection (the brief's standing "pi decays in g" ruling), floored at 0.
* **E4 — deep-local slope check.** On g>=36 states only: the band_fit control set + v0 +
  v0·(log g − log 53). Reports the deep level at g=53 and the deep log-slope with cluster SEs —
  a two-parameter summary of how fast pedigree actually fades past 36 games.

No other estimator will be run; no estimator will be dropped for its answer.

## 4 · The proposed curve — deterministic construction rule

1. Knots stay at (2.5, 10.5, 25.5, 53.0, 85.5); interpolation rule stays `_o31_loglin` (log-linear).
2. **Shallow knots (2.5, 10.5, 25.5) KEEP the wired values.** S4 shows the candidate winning years
   1–3; this seat's mandate is the deep end. E3's shallow coefficients are reported as a lineage
   cross-check; a >2·SE clash with the wired values is flagged, not wired.
3. **Deep knots take E3's fitted values at 53.0 and 85.5**, then the whole 5-knot curve takes the
   isotonic non-increasing projection with the shallow knots fixed (i.e. deep values are capped at
   the wired 0.2177 at 25.5) and the 0 floor.
4. Identification statement per deep knot: **identified** iff the E3 pre-projection 90% CI at that
   knot excludes zero. If beta(85.5) is NOT identified, the counterfactual of §5 still runs (the
   owner's build decision needs the number either way) but the packet labels the 85.5 leg
   "prior-consistent, not separately identified", does NOT recommend wiring on measurement alone,
   and names the alternative channels for closing the S4 gap (the pedigree leg's D channel; an
   explicit floor on beta; the old-law pole carry). No identification will be manufactured.

## 5 · Payoff quantification (the owner's number)

W1-CF-EMIT + W1-CF-SCORE produce the S4 cell table under the proposed curve. Reported per S4
years-4–6 primary cell (and every cell family): ρ_cf vs ρ_cand vs ρ_old, Δ vs old law with the S4
CI machinery, and **recovery = (ρ_cf − ρ_cand) / (ρ_old − ρ_cand)** for the 8 old-law-won primary
M1 cells.

**Built-in controls on the counterfactual pipeline (all must PASS or the run is discarded):**
* Day-0 `v0` column identical to `per_entrant_O31FFINAL.json` on all 2648 records.
* `vpath` entries identical wherever the row's career games at that vantage are <= 25.5 (the
  proposed curve is identical to the wired curve on g<=25.5 by construction).
* Pool rows identical everywhere (`O31_BETA_POOL` untouched); the S4 pool cells must reproduce
  the O31FFINAL pool results.

## 6 · Predictions and falsifiers (registered before results)

* **P1:** W1-CONTROL reproduces the five BETA_31F coefficients at deviation 0.
  *Falsifier: any nonzero drift -> STOP, report, no measurement proceeds.*
* **P2 (the prior under test):** the deep end carries more pedigree than the wired curve pays —
  E3's fitted beta at 85.5 lands above the wired 0.0238, and E1's 71-90 band lands above its
  interpolated wired value, with at least one deep estimate's 90% CI excluding zero.
  *Falsifier: if every deep CI (E1 fine bands, E2 pooled, E3 knots, E4 level) still spans zero, the
  deep end is declared UNIDENTIFIED at this sample size; the packet reports the achieved CI widths
  as the bound and the S4 gap must be closed some other way (candidates named in §4.4).*
* **P3:** wiring the proposed curve recovers >= 50% of the S4 years-4–6 M1 gap (median recovery over
  the 8 old-law-won primary cells) while every years-1–3 candidate M1 win survives (Δ vs old law
  stays positive with CI excluding zero at N=1,2 next+rest).
  *Falsifier: median recovery < 50% -> the deep beta is NOT the (whole) mechanism behind the S4
  years-4–6 result; the packet says so and sizes what remains. Any years-1–3 win lost -> the
  proposal as constructed is REJECTED and reported as such.*

## 7 · Named rows

For every current-board row in `cand31.json` with 40 <= g <= 90 (148 rows): repriced under the
proposed curve by the law's own algebra, price_new = price + rho·Phi·(beta_new(g) − beta_old(g))·v0
(non-pool rows; pool rows unmoved), cross-checked against the counterfactual emit where the row
exists there. Full table in the packet; ~10 named examples in the body.

## 8 · Interaction disclosure (ORDER A)

The proposed curve, if adopted, rides ORDER A's joint re-derivation. The pedigree leg is
pi = D(c_u)·(1−rho) + Phi·beta·rho: any sitter-fade/selection change to D or to the listed-row
population moves the SAME panel this seat fits beta on (the #338 tenure windows enter
`build_states` through the store's season rows and the fade enters the emitted prices). The knot
VALUES proposed here are therefore conditional on the 31-F tree and must be re-derived by the same
instruments on ORDER A's tree, not transplanted. This is stated in the packet, not merely here.

*Seat W1 · 2026-08-17 · evidence dir docs/evidence/order33_w1_2026-08-17/*
