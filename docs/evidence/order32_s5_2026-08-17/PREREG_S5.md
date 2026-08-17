# PREREG — ORDER 32 SEAT S5: v0 fit residuals by pick band (the 21-30 question)

**Date:** 2026-08-17. **Seat:** S5 (measurement, READ-ONLY). **Tree:** land/order-29 tip (53f7433).
**Registered BEFORE any residual, bootstrap, era, or counterfactual number was computed.**
(Schema/lineage inspection only was done before this file: file keys, row counts, and the
artifact==HEADFIX_31F.posv_headfixed identity check. No band means, no residuals.)

## Question (owner's)
Under the candidate entry law, cohort year-paths show picks 21-30 peaking at 1.675x entry (yr6,
highest of any band) while 31-40 peaks at 1.373x. Is 21-30 underpriced at entry — is the strict
monotone-non-increasing-in-pick constraint (owner ruling) suppressing a real bump at 21-30 by
smoothing it into neighbours?

## Fixed lineage (the fit's own data path; nothing re-derived in a parallel lane)
- Fitted v0 surface: `engine/rl_after/pvc_curve_v2.json :: nd_v0.posv` == `HEADFIX_31F.json ::
  posv_headfixed` (verified identical before this prereg). Pipeline: loclin positional surface
  (V0REFIT30B `posv_in`) -> K=15 thin-sample shrink toward all-in relativity + per-pick
  renormalisation (o31f_headfix.py) -> weighted PAVA non-increasing -> floor 100 -> -1 tiebreak ->
  one conservation scalar (o30b_v0refit.py stages lifted verbatim).
- Raw delivered-value data: the ND fit population the surface is built from —
  `grace_adoption_2026-08-13/inputs/LAYER2.json :: fit_nd_keys` (1,142 rows), value =
  `grace_a[k].total` (#338 minimum-tenure delivered-value basis), pick = `attribution[k].pick`,
  position = layer1 `position_group`, era = layer1 `entry_year` (population spans 2004-2021).
- Board for impact framing: scratchpad `cand31.json :: rows` (804 rows: v0, pick, pathway, pos).

## Planned measurements (in order; push-per-step)
1. **S1 inputs**: reproduce the fit input surface from HEADFIX_31F.json + artifact (recompute the
   shrunk PAVA input from persisted posv_raw, credibility_w, share, curve); re-run the lifted PAVA
   block on it and assert it reproduces posv_headfixed exactly. Full pick x position table of raw
   player means / SD / n from the fit population.
2. **S2 residuals**: R = fitted v0 minus raw, at three stages (fit vs raw player mean; fit vs
   loclin surface; fit vs shrunk PAVA input = the pure PAVA/floor/tiebreak/lambda transfer), by
   band (1-10/11-20/21-30/31-40/41-64), per position and pooled (player-weighted). Transfer
   quantified in v0 points and % of band fitted value.
3. **S3 composition**: position mix per band; within-position residual pattern.
4. **S4 era**: band residuals on entry_year >= 2015 vs the full 2004-2021 window; raw
   value-by-band gradient per era (pre-2015 vs 2015+).
5. **S5 bootstrap**: player-level bootstrap (resample the 1,142 fit rows with replacement,
   >= 4,000 reps, fitted surface held fixed) of band residuals and of the gap statistic
   G = R(21-30) - R(31-40); report 95% CIs. If feasible in budget, a smaller full-pipeline
   bootstrap (loclin -> shrink -> PAVA per rep) as a secondary check on constraint binding.
6. **S6 decision framing**: band-monotone counterfactual (PAVA across band means only, flexible
   within band, floor + conservation re-applied) and its rough v0 deltas on the 804-row board's
   ND pick 1-64 rows. No recommendation beyond evidence.

## Predictions (point) — sign convention: R = fitted v0 MINUS raw; R < 0 = band underpriced
- **P1**: R(21-30) < 0 on the full window, pooled (the fit sits below that band's raw mean).
- **P2**: G = R(21-30) - R(31-40) < 0 (21-30 more underpriced than 31-40; consistent with the
  yr-path peak ratio ordering).
- **P3 (noise, my honest prior)**: the bootstrap 95% CI of G INCLUDES 0. With n ~ 180 per band
  and delivered-value dispersion of the same order as the mean (SE of a band mean ~ 5-10% of
  band value), a 1.675x-vs-1.373x path ratio need not imply a raw-mean gap that clears noise —
  the paths compound prices, not the entry-lane raw means. I expect a real point-direction bump
  that does NOT clear the noise bar.
- **P4 composition**: the sign of R(21-30) < R(31-40) survives within at least the two largest
  positions by n in those bands (not a pure mix artifact), though within-position CIs will be wide.
- **P5 era**: same sign of G on 2015+ cohorts; magnitude prediction: within a factor of ~2 of the
  full-window G (no strong era drift in the 21-40 region).
- **P6 magnitude**: |pooled R| in every band <= 12% of band fitted value; the PAVA-stage transfer
  (fit vs shrunk input) at 21-30 and 31-40 each <= 6% of band value — the constraint binds
  locally, not wholesale.

## Falsifiers
- P1 falsified if R(21-30) >= 0 pooled on the full window.
- P2 falsified if G >= 0.
- P3 falsified if the 95% bootstrap CI of G excludes 0 — in which case the verdict flips to
  "the bump clears noise" and the decision framing (Step 6) becomes live rather than optional.
- P4 falsified if, among positions with >= 20 players in EACH of bands 21-30 and 31-40, a majority
  show sign(G) > 0.
- P5 falsified if sign(G) flips on 2015+.
- P6 falsified by any band residual > 12% or PAVA-stage transfer > 6% at 21-30/31-40.
- A "no real bump" verdict (P3 confirmed) is a COMPLETE SUCCESS of this seat, per the mandate.

## Honesty commitments
Dispersion (SD, and SE or CI) accompanies every mean. Every exclusion named (expected: none —
the fit population is taken whole; any row lacking pick/pos/value/entry_year will be counted and
named). Full 64-pick x 6-position tables go in the packet inline. All aggregation weights stated.
