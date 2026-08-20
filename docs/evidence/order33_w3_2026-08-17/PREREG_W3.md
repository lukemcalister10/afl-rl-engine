# ORDER 33 — SEAT W3 PREREGISTRATION (pushed before any result)

**Date:** 2026-08-17. **Mandate:** READ-ONLY measurement. No engine/board/law change.
**Program brief:** issue #334 comment 5312369107.
**Question:** at fixed AGE and fixed current output, does CAREER EXPOSURE (career games /
seasons-in-system) carry additional information about FUTURE IMPROVEMENT? The owner's
hypothesis (2026-08-17, re milan-murdock and hugo-hall-kahan): age is the primary growth
variable, time-in-system a secondary one — a mature-age FIRST-YEAR player has more
improvement ahead than a same-age veteran at the same games/average.

## 1. Population and definitions (S1 conventions reused verbatim)

- Store: `engine/rl_after/rl_model_data.json` (md5 recorded in build output).
- AGE = season year − `_by` (owner convention, as ORDER 32 S1).
- POS = `future_position`, six groups {KPD, KPF, MID, RUCK, SD, SF}; pos-class TALL =
  {KPD,KPF,RUCK}, SMALL = {MID,SD,SF}. Flat bars = ORDER 32 S1's `_O30BP_BARS`.
- Season row = (player, year) with games > 0, from the scoring arrays, 2005–2026.
- u(Y) = 0.92 for Y=2026 else 1.0 (calendar progress, as S1).
- **Base sample** for the change analysis: season rows with games ≥ 6·u (avg reliable),
  age 18–30 at the season, year Y ≤ 2025 (so Y+1 is observable in the store).
  Sensitivity: games ≥ 10·u (FULL).

## 2. Exposure measures (fixed before running)

Measured at the END of season Y (the information a valuer has when projecting Y+1):

- **X1 career games** = Σ games over all seasons ≤ Y.
- **X2 played-season index** = 1 + number of prior seasons with games > 0
  (Hall-Kahan 2026 → 1; Murdock 2026 → 1; McAndrew 2026 → 2).
- **X3 listed tenure** = Y − entry year (`year` field) + 1 for mid-season entry types
  (MSD/SSP/UNR/PDx, whose first season = entry year), and Y − entry year for end-of-year
  types (ND/RD/IRE, whose first season is normally entry year + 1); clamped to ≥ 1.
  X3 counts listed-but-not-played years as system time; X2 does not. Both reported.
- **FIRST2** = indicator X2 ≤ 2 (first or second played season).

## 3. Outcomes

- **O1 next-season change (conditional on surviving):** Δ1 = avg(Y+1) − avg(Y), defined
  when season Y+1 has games ≥ 6·u(Y+1). **Age adjustment:** ΔA = Δ1 minus the sample mean
  Δ1 of the (age × pos-class) cell — the longitudinal age curve measured in this same
  sample (the longitudinal analogue of S1 §4's cross-sectional development-gap table;
  both printed for reconciliation). Ages pooled 27+ for the curve; cells with n < 20
  pool into neighbours (stated in output).
- **O2 exit (the censoring outcome):** EXIT1 = no season at Y+1 with games ≥ 1;
  EXITEVER = no later season with games ≥ 1 at all (Y ≤ 2025). Reported by exposure at
  fixed age × output band. A mature first-year who fails leaves the list fast — this is
  the survivorship trap named in the order; it is an outcome here, not a nuisance.
- **O3 unconditional reading:** P(IMPROVE&SURVIVE) = P(season Y+1 has games ≥ 6·u and
  avg(Y+1) ≥ avg(Y)). Exit counts as failure. No imputation of ghost averages.
- **O4 longer horizon:** best avg over seasons Y+1..Y+3 with games ≥ 6·u, minus avg(Y),
  conditional on at least one such season (Y ≤ 2023 for full window), plus P(at least one).

## 4. Specs

- **M1 pooled regression:** ΔA ~ β·exposure + age dummies (18..30) + pos dummies +
  avg-vs-bar (linear) + output-band dummies (avg − bar(POS) in bands (−∞,−10),[−10,0),
  [0,10),[10,∞)). Exposure entered three ways (separately): X1/50 (per 50 career games),
  X2, FIRST2. SEs: cluster bootstrap by player, 1000 reps, seed 33. Owner's claim
  predicts **β < 0 for X1/X2 and β > 0 for FIRST2**.
- **M2 key cells, reported raw:** age band {23, 24, 25, 26+} (and pooled 23+) ×
  pos-class × output band: mean Δ1, mean ΔA, sd, n for X2 ≤ 2 vs X2 ≥ 4, plus EXIT1 and
  P(IMPROVE&SURVIVE) for both groups. Any side with n < 5: cell declared UNSUPPORTED
  and no contrast claimed.
- **M3 shape:** coefficients on X2 dummies (1,2,3,4,5+; baseline 5+) in the M1 frame —
  is the premium a level shift or concentrated in seasons 1–2 (adaptation-to-level)?
- **M4 named rows:** milan-murdock, hugo-hall-kahan, lachlan-mcandrew + a same-age
  same-position veteran comparator each (chosen from the store: same age in 2026, same
  POS, nearest 2026 avg, X2 ≥ 4; choice rule fixed here, applied mechanically).

## 5. Falsifiers (stated before running)

- **F1 (support):** FIRST2 coefficient at fixed age/output is ≥ +2.0 avg points with
  95% bootstrap CI excluding 0, and the age-23+ pooled cell contrast points the same way.
- **F2 (null):** FIRST2 CI includes 0 with point estimate < +1.0 — exposure adds nothing
  measurable at fixed age; the age-only keying stands as measured. A null is a result.
- **F3 (conditional-only):** improvement premium exists under O1 but low-exposure mature
  players' EXIT1 is enough higher that O3 shows no advantage — then the claim holds only
  conditional on survival, and any wiring must price the exit side too.
- **F4 (shape):** adaptation story requires the X2=1 and X2=2 dummies to carry most of
  the premium (season-1→2 drop larger than all later drops combined). A flat level shift
  across X2 instead would point at a selection artifact (who GETS a mature debut), not
  adaptation — this alternative reading is acknowledged now: mature first-years are a
  selected group (SSP/IRE/mature ND), and no regression here removes that selection.
  The packet must carry this caveat regardless of sign.
- Between F1 and F2 lies INCONCLUSIVE and will be called that.

## 6. Guards

- Thread pins on all numeric runs (OPENBLAS/OMP/MKL/NUMEXPR/VECLIB = 1); seed 33;
  deterministic output; store md5 printed in every output file.
- 2026 rows are never used as season Y in the change analysis (no Y+1 exists); they
  appear only in named-row readings, marked in-progress.
- Dispersion always (sd + IQR where means are shown); full tables in the out files.
- Wiring proposals, if any, are marked AWAITING RULING and carry the no-double-counting
  note vs S3's selection channel: S3 pays SELECTION at fixed output (bust-risk
  resolution — games as evidence you belong); this seat prices remaining GROWTH at
  fixed age (games as evidence you have already adapted). The same career-games count
  must not be paid twice; the packet must state the boundary.
