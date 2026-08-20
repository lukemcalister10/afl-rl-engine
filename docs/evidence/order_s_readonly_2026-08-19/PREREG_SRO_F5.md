# PREREG ADDITION — F5, THE SEVERITY CALIBRATION

**Seat:** ORDER S READ-ONLY. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Extends:** `PREREG_SRO.md` (`09d5e3f`), `PREREG_SRO_FOLLOWUP.md` (`6fab2f8`).

**NO ENGINE EDIT. NO DIAL. NO BOARD. NO STORE WRITE. NO PULL REQUEST. NOTHING ADOPTED.**
Deliverables go only to `docs/evidence/order_s_readonly_2026-08-19/` as an `F5_` set.

**This file is pushed BEFORE any number in F5 exists.**

**Named rows may illustrate. They gate nothing.** The owner's shape — a pick-12 first-year with 15
games sitting about 19 points a game below his bar — is a SHAPE, and every cell below is defined by
the shape, never by a player.

---

## 0 · THE QUESTION, AND WHAT IS ACTUALLY BEING TESTED

The owner: *"I'm not sure the first season is enough evidence to ever justify a player like that
losing 4x his starting value."*

**Two separate claims live inside that sentence and this seat separates them before measuring.**

1. **A LEVEL claim.** At that point in a career, with that evidence, does the charge mark the row
   below what history says he goes on to deliver?
2. **A SPEED claim.** `A(g) = 1 − exp(−g/G0)` with `G0 = 9.89` decides how fast the charge firms up
   with games. `G0` was measured from where the PRODUCTION slope `BETA(g)` saturates — how fast shown
   production starts predicting delivered value at all. **Using it inside the charge assumes that
   pedigree-conviction should firm at the same speed as production-prediction. That is an assumption,
   not a measurement, and F5 tests it directly.**

**F5 answers both. It does not propose a repair to either.**

---

## 1 · THE VANTAGE, AND WHY IT IS THE RIGHT ONE

The engine charges a row at a vantage year `Y` using `A(career games to Y)` and `T(s_P over seasons
played to Y)`. F5 reproduces exactly that vantage on history:

```
STAGE N (N = 1, 2, 3)     the vantage immediately after the player's Nth season
  g   = CUMULATIVE career games through depth N        -- the axis A(g) reads
  s_P = ORDER P's surplus over seasons 1..N            -- the axis T(s) reads
  OUT = the DISC-discounted house-ruler delivered value from depth N+1 onward, over v0
```

`s_P` is built with ORDER P's own `op_lib`: `BAR_P(pos, age, v0) = o32_gate_bar(pos, age) +
PG(ln v0, class)`, the premium surface refitted node-for-node and asserted against the built engine
grid, exactly as T1 did.

**Bins, taken from the order and fixed here:**

- career stage: **1st / 2nd / 3rd season**
- games in the window: **1-9 / 10-22 / 23+**
- surplus against the PEDIGREE bar: **0 to −10 / −10 to −20 / −20 to −35 / worse than −35**

A finer games grid (1-4 / 5-9 / 10-14 / 15-19 / 20-24 / 25-34 / 35+) is used for the SPEED test only,
because a two-parameter saturating curve cannot be fitted to three points.

---

## 2 · THE TWO MARKS, AND THE ONE HONEST WAY TO COMPARE THEM

**THE CHARGED MARK** is exact, not estimated. For each historical row at its own vantage:

```
f_i = exp( -LAMBDA * A(g_i) * T(s_i) )        LAMBDA 0.174383, G0 9.89, THETA_R 0.65744,
                                              s0 -2.4527, TMAX 21.12 -- the wired O37 constants
```

This is the fraction of the pedigree leg the mechanism retains. It is what the mechanism controls and
it carries no sampling error of its own.

**THE REALIZED MARK** is `OUT`, in house-ruler units over `v0`.

**THE TWO ARE IN DIFFERENT UNITS AND A LEVEL COMPARISON BETWEEN THEM IS MEANINGLESS.** The house
ruler is not board currency and no constant converts one to the other without a board build, which
this seat is not doing. **So the comparison is made RELATIVE TO A REFERENCE CELL, which makes both
sides unit-free:**

```
charged ratio  = mean f over the cell            /  mean f over the REFERENCE cell
realized ratio = mean OUT over the cell          /  mean OUT over the REFERENCE cell
CALIBRATION    = realized ratio / charged ratio
```

- `CALIBRATION > 1` — **the row delivers MORE than the charge marks him at, relative to his peer. The
  charge front-loads.**
- `CALIBRATION < 1` — the row delivers less. The charge is generous.
- `CALIBRATION = 1` — the charge is calibrated at that cell.

**The reference cell is fixed here, before the run: the SAME career stage and the SAME games bin, at
surplus 0 to −10.** A second reference, `s_P >= 0` (strictly at or above bar), is run alongside
because the SPEED test in §4 is explicitly about "at-bar players", and both are printed.

**Raw levels are printed too** — mean `f`, mean `OUT`, median `OUT`, and the pooled aggregate — so the
ratios can be checked and nothing is hidden behind a normalisation.

**Intervals.** Player-clustered bootstrap, 2,000 draws, seed 32, resampling players and recomputing
both sides of every ratio inside each draw, so the charged side carries its own cell-composition noise
rather than being treated as fixed.

**Heavy tails.** F1 established that the mean and the pooled aggregate can disagree on these outcomes.
Both are reported for every headline cell, and the median beside them.

---

## 3 · CENSORING AND SURVIVAL — STATED BEFORE THE RUN

- **Delisted and retired rows are OUTCOMES, not exclusions.** A player delisted after his first season
  contributes `OUT` near zero and stays in the population. **The delisted share of every cell is
  printed.** Dropping them would be the survivor bias that would flatter the charge.
- **Recent cohorts are censored out.** The vantage at stage `N` needs future seasons to score, so the
  rule fixed here is: **at least FOUR observed seasons after the vantage**, i.e. entry year
  `<= 2021 − N`. A six-season sensitivity is run and printed. **The last several draft classes are
  therefore absent from F5 entirely and no claim here reaches them.**
- **The population is ND entrants from 2005** with a positive `v0`, force-majeure keys excluded.
  Pool routes are run as a declared sensitivity, not folded into the primary.
- **Right-censoring of the outcome itself:** `OUT` sums observed seasons to 2025 only. There is no
  projected tail, unlike ORDER 30A-2's estimand. **That biases `OUT` DOWN for later cohorts, which
  cuts AGAINST finding that the charge front-loads**, and is therefore a conservative direction for
  F5-P1. It is stated here so the direction of the bias is on the record before the result.

---

## 4 · THE CONVICTION-SPEED TEST

The charge implies a specific shape for how the outcome gap between a deep underperformer and an
at-bar player should open with games. From the mechanism's own algebra, with `Δs` the surplus gap:

```
ln f(at-bar) - ln f(deep) = LAMBDA * A(g) * THETA_R * Δs = BETA_sat * A(g) * Δs
```

so the mechanism predicts the log outcome ratio is proportional to `A(g)`. Inverting it gives an
**empirical A**, recovered per games bin from outcomes alone:

```
A_hat(g) = -ln( OUT(deep, g) / OUT(at-bar, g) ) / ( BETA_sat * Δs(g) )
```

Then `A_hat(g) = 1 − exp(−g / G0_hat)` is fitted by weighted least squares over the finer games grid,
`G0_hat` reported with a player-clustered bootstrap CI **against the published `[7.60, 12.98]`**.

`A_hat` is not bounded to `[0, 1]` by construction and **whatever it comes out as is printed raw.**

---

## 5 · PREDICTIONS

- **F5-P1 (the owner's tail).** At stage 1-2, games 10-22, surplus −20 to −35 and worse, predicted:
  **CALIBRATION > 1 — the realized value sits ABOVE the charged mark and the charge front-loads.**
  **Falsified if the 90% CI on CALIBRATION contains or sits below 1.0.** Reasoning stated in advance:
  ORDER P itself recorded that `LAMBDA` solved low and `THETA_R` high, making the charge *"more like a
  switch than a dial"*, and a switch on a noisy axis over-reacts at the tail.
- **F5-P2 (the speed).** Predicted: **`G0_hat > 12.98`, i.e. above the published upper limit — pedigree
  conviction firms SLOWER in games than the production slope saturates.** **Falsified if `G0_hat` sits
  inside `[7.60, 12.98]`, and falsified in the opposite direction if it comes out below 7.60.**
  Reasoning stated in advance: early games are selection-driven, so who plays them carries information
  about the club's view as well as about the player, and that should slow the rate at which a bad
  start ought to convict a prior.
- **F5-P3 (the tail flattens).** Predicted: the "worse than −35" cell is NOT separable from the
  "−20 to −35" cell on realized outcome. **Falsified if they separate.** This is the empirical version
  of the question `TMAX` exists to answer, and a null here is a real result.
- **F5-P4 (survival).** Predicted: the delisted share rises with the depth of underperformance and the
  deepest cells are majority-delisted. **Falsified if it does not rise.** Reported whichever way, and
  the point is that the population is not survivors-only.
- **F5-P5 (the honest one).** Predicted: at least one cell the verdicts require holds **under 25
  players** and is marked THIN. **Falsified if every required cell clears 25.** Preregistered so that
  a thin verdict is stated as thin rather than dressed up.

---

## 6 · WHAT IS ALSO REPORTED, AND WHAT IS NOT

- **The owner's premise, checked exactly.** The "~0.24x" figure is verified on the engine's own
  numbers rather than assumed: the charged fraction at the named shape is computed from the wired
  constants, and the closest ACTUAL board rows to that shape are printed with their real
  `price / entry price`. **That is a check of the premise, not a target.**
- **The already-priced softenings are shown for reference only** — ORDER R's `TMAX` at p15 and p20 and
  `BETA_sat` at its CI floor — so the owner can see whether any variant already on the record lands
  where the measurement points. **This seat recommends none of them and derives no new constant.**
- **NO REPAIR IS PROPOSED.** If the measurement says the constants are miscalibrated, F5 reports the
  measured value and its interval and stops. Choosing is the owner's and the supervisor's.

---

## 7 · WHAT THIS SEAT WILL REPORT REGARDLESS

Sample size and delisted share for every cell; thin cells marked and not read; the censoring cutoff
and the direction of its bias; nulls reported as nulls; every prediction above scored HELD or FIRED by
number; and the unit problem in §2 restated wherever a ratio is quoted.
