# PREREG P — THE PEDIGREE-CONDITIONAL EXPECTATION, AND THE CHARGE DERIVED ON IT

**Seat:** ORDER P. **Date:** 2026-08-18. **Base:** `land/order-29` at `90b4d45` (ORDER N's tree).

**This seat is READ-ONLY on the engine, the board and the law. It builds no board. It changes no
engine line. It adopts nothing. It measures, derives and estimates, for the owner to rule on.**

This document is pushed **before any result number in this order exists**. Everything below is fixed
in advance: the surface construction, the estimator, the statistics, the derivation rule, the
falsifiers, and the forbidden-set argument.

---

## 0 · THE OWNER'S INSIGHT, VERBATIM, WHICH IS THE WHOLE BRIEF

> *"Instead of performance relief going to players producing above their age level, should it go to
> players performing ahead of expectation? As the expectation is priced into them. Top picks are
> priced higher because there is a belief that their pedigree is more predictive of success. So,
> there should be a higher bar/more positive signs required to maintain a higher valuation. Whereas
> less expectation of performance is priced into lower picks. It seems silly to measure all first
> years on the same 'performance for age' bar when these players are priced differently to begin with
> based on differing expectations."*

**The measured consequence that provoked it.** ORDER N derived a charge whose relief is keyed on
surplus against an AGE-ONLY bar. `PACKET_N.md` §8.3 measured what that does:

| pick band | rows | median surplus vs the age bar | share earning full relief |
|---|---:|---:|---:|
| 1-10 | 584 | +6.12 | **41.3%** |
| 11-20 | 572 | +0.63 | 26.4% |
| 21-40 | 1015 | −4.78 | 15.7% |
| 41-64 | 888 | −7.60 | **12.5%** |

Spearman(pick, surplus) = **−0.3303**. Relief therefore flows to the top of the draft, picks 1-10
break the +14% buy rail (+16.13% primary, +23.90% modern), and the late bands come out WORSE than
ORDER K (31-40 −10.70% → −13.17%; 41-64 −6.89% → −9.99%).

**The owner's diagnosis is that the bar is the wrong object.** A pick-1 player is priced with a high
expectation. Clearing an age-only bar is therefore weak evidence for him and strong evidence for a
pick-50 player. The bar must scale with what is priced in.

**His prediction, which this order tests:** the top-of-draft inflation collapses ON ITS OWN once the
bar scales with price, with no cap bolted on.

**There are no named-player targets in this order.** No constant is chosen to move any row to any
value. Named rows appear once, at the end of the packet, wherever the derived rule puts them.

---

## 1 · WHAT WAS LOOKED AT BEFORE THIS DOCUMENT WAS WRITTEN

Full disclosure, so nobody has to wonder what was known when the design was fixed.

1. `PREREG_N.md` and `PACKET_N.md` in full, and every ORDER N script (`on_lib.py`, `on_step1.py`,
   `on_step2.py`, `on_step3.py`, `on_step4.py`, `on_variant.py`, `on_bands.py`). This order REUSES
   that machinery and does not rebuild it.
2. `docs/evidence/order32_s4_2026-08-17/s4_shootout.py` — the house delivered-value ruler, reused
   whole and md5-asserted.
3. The engine source for the deleted par machinery: `engine/forward_valuation/par_build.py`,
   `engine/forward_valuation/par_redesign.py`, and the four live `par_at` sites plus `par_pole` in
   `engine/rl_after/_merged_recover.py`. Structure and history only; no board was run.
4. `docs/evidence/one_machinery_2026-08-14/STOP_STEP3_FORBIDDEN_SET_BOUNDARY.md`,
   `docs/evidence/candidate_31/SHIPPING_PACKET_31.md` §1.11, and
   `docs/evidence/order_c_2026-08-17/PACKET_C.md` §1-§2 — the lineage of the forbidden-set deletion
   and of the age bar that replaced it.
5. **Four structural counts, computed before this prereg, and declared here rather than presented
   later as findings.** They fix the binning and nothing else. Season rows played at age ≤ 23 by
   entrants from 2005 on: **5,042 over 1,575 players**. By class and age:

   | age | 18 | 19 | 20 | 21 | 22 | 23 |
   |---|---:|---:|---:|---:|---:|---:|
   | TALL | 8 | 169 | 246 | 281 | 298 | 294 |
   | SMALL | 31 | 639 | 794 | 821 | 774 | 686 |

   Entry price `v0` over the 2,432 entrants from 2005 on, percentiles 1/5/10/25/50/75/90/95/99:
   **62.8 · 91.6 · 130.9 · 211.3 · 293.2 · 611.4 · 1127.8 · 1659.3 · 2947.6.**

   These are counts and a spread. **No relationship between pedigree and production, and no
   relationship between anything and outcomes, has been looked at.**

---

## 2 · STEP 1 — THE OLD PAR SYSTEM, AND THE FORBIDDEN-SET ARGUMENT

The owner noticed that a pedigree-conditional bar resembles the deleted par machinery. It does. The
resemblance has to be met head on, before any number is produced, because if the object proposed here
is the forbidden set coming back through a side door then it must not be proposed at all.

### 2.1 What `par_at(pos, pick, tenure)` actually was

From `engine/forward_valuation/par_build.py`:

```
par(pos, pick, tenure)  =  level_pos(log-pick)  +  ramp_pos(tenure)          [additive; ramp(yr1) = 0]
```

- **What it computed.** The median recency-weighted per-game level among players ON THE PARK at that
  position and tenure, as a local-linear kernel regression over `log(pick)` with tricube weights and
  bandwidth `H_LOGPICK = 0.40`, plus a per-position tenure ramp fitted by additive backfitting and
  shrunk toward the global ramp for thin positions. Cohort: draft 2003-2018. In one sentence: **the
  AFL Fantasy points per game a player of that draft position is expected to be producing at that
  stage of his career.**
- **How it entered price.** Four live sites, all on printed-price paths:
  1. `_par_prior(p,Y) = PR.par_at(gfut, effpk, T)`, blended into the assessed LEVEL at
     `_merged_recover.py:339/741`: `(1 − pw)·prod + pw·par_prior`. **A high pick producing badly had
     his assessed level pulled UP toward his par.** The comment on that line calls it "the pedigree
     hump".
  2. `par_pole(pos, pk, T)` — a SYNTHETIC player is created at that pick producing exactly par, priced
     through the whole engine, and the result is added on top of the production price:
     `raw_ev = pr + w·recover(perf, par)·max(0, po − pr)`. **The `max(0, ·)` makes it strictly
     non-negative: a pedestal that lifts a high pick toward what a pick of his number "should" be
     worth, and never lowers anyone.**
  3. The isotonic pick-tax `ISO`, built by probing `raw_ev(synth(pk, par_at(pos, pk, 4)))` across
     picks 1-70 — a multiplicative pick-side correction on the production leg.
  4. Two denominators: the evidence weight `Q = clip(career avg / par, 0, 2)` and the
     mediocre-for-years decay gate `pr = bestlvl / par`.
- **Why it was deleted.** The owner's ruled forbidden set — *"pathway pedestals, par tables, prior
  poles (bars/aging/form legitimately retained)"*. The seat that hit the boundary stopped and priced
  it (`STOP_STEP3_FORBIDDEN_SET_BOUNDARY.md`): deleting the pole moved 271 rows and −19,273 points.
  Candidate 31 then executed the ruling: **the pole and the par-built ISO were deleted; sites 3 and 4
  were RETAINED with their denominators re-referenced from pick-conditional par tables to pick-blind
  flat positional bars** (KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). ORDER C /
  Candidate 32 then re-referenced those same two denominators again, from the flat mature bar to the
  **age** bar, because S1 measured that the flat bars fail 86-100% of age-18/19 seasons even for
  players who turn out fine. That age bar is `o32_gate_bar`, and it is the bar ORDER N's surplus is
  measured against today.

### 2.2 The forbidden-set argument, stated in advance

**The ruled objection was to pick information ADDING unearned value.** Every deleted object had that
signature: `max(0, po − pr)` can only be non-negative; `pw · par_prior` raises a weak high pick's
assessed level; the ISO multiplier was ≥ 1 where the pick curve was judged shallow. A player was paid
for being pick 1 whether or not he had done anything.

**The object proposed here has the opposite sign.** It enters as a bar inside a CHARGE:

```
pi  *=  exp( -LAMBDA * A(g) * T(s) )        T non-increasing in s,  s = production - bar
bar(pedigree, age)  =  age bar  +  pedigree premium
```

Raising the bar for an expensively-priced player RAISES `T`, which RAISES his charge and LOWERS his
price. Lowering the bar for a cheaply-priced player lowers his charge. **The partial derivative of
price with respect to pedigree, through this object alone, is negative. Par's was positive.**

**Three bounds, declared now and asserted at run:**

- **P-F1. The object can never price a row above its own uncharged price.** `F = 1 − exp(−LAMBDA·A·T)`
  lies in `[0, 1)` for every input because `LAMBDA, A, T ≥ 0`. So `v = v(F=0) − F·C ≤ v(F=0)`, and
  `v(F=0)` is ORDER K's own eta-zero board, which contains no par object. **The ceiling this mechanism
  can reach is a board the forbidden set is already absent from.** It cannot add value anywhere.
- **P-F2. `A(0) = 0` exactly, so no day-0 print can move.** Entry prices are untouched, so the object
  cannot re-price the pick curve itself.
- **P-F3. The bar is measured from OUTCOMES, not from prices.** The premium is estimated on realised
  per-game production of past entrants. No board price enters the bar. `v0` is used only as the
  pedigree LABEL — the axis the outcomes are indexed by — never as a value that is paid out.

**Where it could nonetheless smuggle pick value back in, stated honestly before it is measured.**
Two channels, and both are measured in Step 4 rather than argued away:

- **S1 — the relief channel.** Relief is a reduction of a charge, and the charge is proportional to the
  pedigree leg `C`, which is larger for expensive players. So equal relief in PERCENTAGE terms is
  unequal relief in POINTS: a top-ten pick who clears his bar gets back more points than a pick-50 who
  clears his. This is arithmetically unavoidable for any multiplicative charge on the pedigree leg,
  and it is already true of ORDER K's blind charge. It is bounded by P-F1: the most any row can get
  back is its own uncharged pedigree. **Measured, reported, not assumed away.**
- **S2 — an under-demanding bar.** If the measured production premium for expensive players is
  SHALLOWER than the premium their price implies, then the bar does not rise as fast as the price
  does, and expensive players are let off relative to what is priced into them. This is the direction
  in which the object would quietly become a pedestal again. **Declared test:** compare the pedigree
  gradient of the measured production bar with the pedigree gradient of price, both in the same
  units. Reported in the packet whichever way it comes out.

**If Step 4 finds either channel dominant, this order says so. That is a finding, not a failure.**

---

## 3 · FIXED CONSTRUCTIONS

### 3.1 Everything reused from ORDER N, unchanged

The age bar `bar(pos, age)` (the S1 C3 surface asserted against the engine's own `O32_GATE_DELTA`),
the house delivered-value ruler (md5 `241842f61ddd3c486f04f201a7efcce9`), the matrices `OKRULED`
(`f3101883`, eta 0.50) and `M0ETA0` (`73bf9617`, eta 0), the offline pricing identity, the class
machinery, the band machinery, the games bins, and the young windows. `op_lib.py` imports
`on_lib.py` and adds only the objects below.

### 3.2 THE PEDIGREE AXIS — and why it is `v0`, not the pick

**Declared choice: the pedigree axis is `x = ln(v0)`, the row's own entry price.** Three reasons,
fixed before any number:

1. **It is what the owner's sentence says.** *"As the expectation is priced into them."* The
   expectation priced into a player IS his entry price. The pick is a proxy for it.
2. **It is continuous and position-aware.** `v0` already carries the position surface, so a key
   forward and a midfielder taken at the same pick have different prices and therefore different
   bars. A pick band cannot do that.
3. **It covers the whole board.** Pool entrants, rookie-draft rows and mid-season entrants have no
   national-draft pick. On a pick axis they are a residual bucket; on `v0` they sit where their price
   puts them.

**Pick band is carried as a declared SENSITIVITY, not as the primary.** The whole surface is
re-estimated on the four bands `1-10 / 11-20 / 21-40 / 41+ and pool` and reported beside the primary.

### 3.3 THE PEDIGREE-CONDITIONAL EXPECTATION SURFACE (the object the order turns on)

The bar is built as the age bar **plus a measured pedigree premium**, so that the whole difference
from ORDER N is one named object and can be read on its own:

```
BAR_P(v0, pos, age)  =  bar(pos, age)  +  PG(ln v0, class)
PG(x, class)         =  E[ avg_s - bar(pos_s, age_s)  |  ln v0 = x,  class ]
```

- **Population.** Every season row with `games > 0`, played at age 18-23, by an entrant whose entry
  year is 2005 or later, with a position in the ruler's six groups, in seasons up to and including
  `LAST_REAL_SEASON = 2025`. Force-majeure keys `paddy-mccartin`, `thomas-boyd` excluded, as the
  house ruler excludes them. **5,042 rows over 1,575 players** (§1.5).
- **Estimator.** Games-weighted **local-linear kernel regression** on `x = ln(v0)`, tricube kernel,
  bandwidth `H = 0.40` in log-v0 units, fitted separately for `TALL` (KPD, KPF, RUCK) and `SMALL`
  (MID, SD, SF) — the same class pooling the C3 age surface uses, and the same estimator family
  `par_build.py` used over log-pick, chosen deliberately so the comparison to the deleted object is
  like-for-like rather than flattering.
- **Bandwidth sensitivities, declared now:** `H = 0.25` and `H = 0.60`.
- **Monotonicity.** `PG` must be non-decreasing in `x`: a more expensively priced player is never
  expected to produce less. If the raw local-linear fit is non-monotone, the house isotonic
  instrument (`sklearn.isotonic.IsotonicRegression(increasing=True)`, the one the engine already
  uses for the pick guard) is applied to the fitted grid. **Both the raw and the isotonised surface
  are printed, and every place they differ is named.**
- **Support and thin cells.** The fit is evaluated on a grid over the 1st-99th percentile of `x`.
  Outside that range the premium is HELD FLAT at the end value — bounded, never extrapolated. Every
  grid cell carries its effective sample size; a cell with ESS < 30 is printed as thin and the
  packet says so rather than smoothing it away.
- **The age axis.** The age LEVEL is already removed by `bar(pos, age)`. Whether the pedigree PREMIUM
  itself varies with age is a measurement, not an assumption: the premium is re-estimated per age
  18-23 and printed with counts. **The primary bar pools ages**, because that is the thicker estimate
  and because at ages 18-19 the TALL cells hold 8 and 169 rows. If the age slices disagree materially,
  the disagreement is reported and bounded, not smoothed.
- **The games axis.** The order asks for the surface at a given number of GAMES as well. The premium
  is re-estimated within career-games bins and printed. **The primary bar does NOT carry a games
  axis**, because games is evidence and evidence enters the charge through `A(g)`; letting the bar
  rise with games as well would charge the same fact twice. A bar carrying the games axis is run as a
  declared sensitivity and its effect on the headline numbers is reported.
- **Selection, declared before it is measured.** Only players who PLAY have a per-game average. A
  cheap player has to be good to get a game; an expensive one plays anyway. So
  `E[avg | played, v0]` is FLATTER in `v0` than the underlying talent gradient, and the measured
  premium is a LOWER bound on the true one. **This cuts against the owner's purpose** — it makes the
  bar less demanding for expensive players than it should be, which is smuggle channel S2. It is
  measured, bounded and reported; it is not corrected, because correcting it needs a construction
  choice this seat has not been given.

### 3.4 THE NEW PERFORMANCE SURPLUS

```
s_P(p, Y)  =  SUM_s [ games_s * ( avg_s - BAR_P(v0_p, pos_s, age_s) ) ]  /  SUM_s [ games_s ]
```

over every season `s` with `year_s <= Y` and `games_s > 0`. Units: AFL Fantasy points per game.

**Positive means the player is producing above what a player priced like him produces at his age.**

Because `BAR_P = bar + PG` and `PG` does not depend on the season, this is exactly

```
s_P  =  s_N  -  PG(ln v0, class)
```

where `s_N` is ORDER N's surplus. **The whole change is a per-player shift of the origin of the
surplus scale, by an amount measured from outcomes.** That is stated now so that nobody later reads
the result as a bigger change than it is.

Gameless rows are excluded from every population, exactly as in ORDER N: `A(0) = 0` is a structural
law of the engine and no mechanism proposed here may change it.

---

## 4 · STEP 2 — WHAT THE NEW SURPLUS PREDICTS

Same cohort, same ruler, same estimator, same seeds as ORDER N §4, so the two are comparable line by
line: entrants from 2005 on, vantages `N = 1..6`, age at vantage ≤ 22, `1 <= g <= 60`, at least one
observable future season, delivered value `DVREST` = discounted sum of every later season at 1.14,
`DV1` = next season, `DV5` = the censoring-balanced five-year window.

**Estimands, per career-games bin `[1,3] [4,7] [8,12] [13,17] [18,24] [25,39] [40,60]`:**

- **Q1 — the premium itself, with dispersion and sample size.** `PG` over the pedigree grid, with ESS,
  the interquartile range of the underlying age-surplus in each cell, and the per-age and per-games
  slices. **Reported where it is thin and bounded rather than smoothed.**
- **Q2 — BETA_P.** OLS of `ln(1 + DVREST)` on vantage-year effects, `ln(v0)` and `s_P`. `BETA_P` is
  the estimand. 90% CIs bootstrapped by CLUSTERING ON PLAYER, 2000 resamples, seed 32 — ORDER N's own
  B and seed.
- **Q3 — the comparison.** `BETA_P` against ORDER N's `BETA_N`, per bin. **Predicted in advance:** at
  fixed `v0`, `s_P` and `s_N` differ by a function of `v0` alone, so the two slopes should come out
  close. If they do, the honest reading is that the owner's fix is about WHERE ZERO SITS on the
  surplus scale, not about how steep the scale is, and the packet says so.
- **Q4 — the null test that matters.** Does the pedigree premium carry information at LOW games?
  `PG` is re-estimated on rows with `g <= 7`, with its CI. If it is not distinguishable from zero
  there, the case for a separate bar at low games fails, falsifier P4 fires, and the packet reports
  the null.
- **Q5 — the band balance.** Spearman(pick, `s_P`) and the share of each pick band at or past the
  relief zero point, against ORDER N's −0.3303 / 41.3% / 12.5%. This is the owner's prediction, tested
  on the surplus itself before any price is computed.
- **Q6 — smuggle test S2.** The pedigree gradient of the measured production bar against the pedigree
  gradient of price, in the same units.

---

## 5 · STEP 3 — THE DERIVATION RULE, FIXED BEFORE THE NUMBERS

Identical discipline to ORDER N §5. The form is ORDER N's, because ORDER N's form was derived and
this order changes the surplus, not the shape:

```
pi  *=  exp( -LAMBDA * A(g) * T(s_P) )

A(g)   = 1 - exp(-g / G0)                                    monotone in evidence, A(0) = 0 exactly
T(s)   = clip( 1 - THETA_R * (s - s0), 0, TMAX )             non-increasing in s, linear in the exponent
```

| constant | derived from | never from |
|---|---|---|
| `G0`, `BETA_sat` | the `BETA_P(g)` curve of Step 2, fitted as `BETA_sat·(1 − exp(−g/G0))`, weighted by each bin's own inverse variance | any player's price |
| `LAMBDA × THETA_R` | pinned `= BETA_sat`, so the delivered slope `d ln(retained pedigree)/ds = LAMBDA·A(g)·THETA_R` equals the measured slope at every level of surplus | — |
| `s0` | the games-weighted mean `s_P` of the young cohort, so a row at the centre pays the base charge | — |
| `TMAX` | `T` at the cohort's own 5th percentile of `s_P` — the worst 5% all pay the same top rate rather than an unbounded one | — |
| `LAMBDA` | **solved** by the anchoring identity: the derived charge removes exactly the same total number of points from the year-1 class-mark population (cohort classes 2005-2015) as the current charge does | — |
| age gate | 24, as ORDER N, because the age bar has content below 24 and none at or above it | — |

**There is no free parameter.** `THETA_R = BETA_sat / LAMBDA` follows.

**Pre-committed structural properties. If any fails, nothing is proposed.**

- **P-S1.** `A(0) = 0` exactly: every day-0 print is untouched.
- **P-S2.** `A` non-decreasing in `g`.
- **P-S3.** `T` non-increasing in `s_P`.
- **P-S4.** the factor is in `(0, 1]` for every row on the board.
- **P-S5.** no row prices above its own uncharged price `v(F=0)` (this is P-F1, asserted row by row).

**Pre-committed honesty clause.** If `BETA_P` is indistinguishable from zero at a games level,
`THETA_R` is zero there and the packet says the intuition is not supported by outcomes at that level.
If the anchoring requirement and the new conditioning conflict — no `LAMBDA` holds the board while
giving the tilt the measurement justifies — **the conflict is quantified and both sides are
presented. This seat will not choose for the owner.**

---

## 6 · STEP 4 — THE OFFLINE ESTIMATE

The identity is ORDER N's, already proved (falsifier N1 passed: `IDENT_N_out.txt`, worst relative
round-trip error 1.9e-16 over 14,420 vantages, largest deviation from linearity 0.467 board points
across six built boards):

```
C_N      = ( v_M0ETA0[N] - v_OKRULED[N] ) / ( 0.50 * m_d(g_N) )      the charge base
v_new[N] = v_M0ETA0[N] - C_N * F_new(row, N)
```

**Everything estimated here is labelled an estimate pending a build**, and the same things ORDER N
could not do this seat cannot do: the engine's assert wall, the continuity objects, rho32
monotonicity, and the day-0 identity all need a build.

**What is produced, all three columns side by side — ORDER K `f3101883` · ORDER N derived · ORDER P
derived:**

1. **The owner's prediction, tested.** Share of each pick band earning full relief, against ORDER N's
   41.3% / 12.5%. Spearman(pick, surplus) and Spearman(pick, relief).
2. **The year-1 class mark** on ORDER L's registered basis (W2 scorer, draft classes 2005-2015,
   `ENTRY_FLOOR = 2005`) and on the cohort clock, through the committed class machinery unchanged.
3. **The full ND band tables, years 0 to 7, in BOTH windows** — PRIMARY cohorts 2005-2023 and MODERN
   cohorts 2019-2023 — through the committed band machinery unchanged. This is the standing owner
   requirement and it is not optional.
4. **The PEAK values by band, in both windows** — the maximum of each band's year-0-to-7 path and the
   year it falls in. ORDER N's peaks came in 2-5% below ORDER K's at the same peak years, with the
   board total −1.36%. The packet reports whether this construction restores them and whether the
   board still deflates.
5. **The pool arms**, which ORDER N left un-retabled and named as owed.
6. **The veteran caps** (churn and net against the standing rails) under the age gate.
7. **The named rows**, last, as illustrations — including a matched pair: a top-10 pick and a 41-64
   pick producing similarly for their age, so the owner can read directly how the new bar treats
   them differently. **These are consequences, not targets.**

---

## 7 · FALSIFIERS

Fired means the finding it guards is withdrawn or restated, in the packet, in the same words.

| # | falsifier | what it kills |
|---|---|---|
| **P1** | the ORDER N pricing identity does not reproduce `OKRULED` from `M0ETA0` at eta 0.50 to 1e-6 relative on every row and vantage | all of Step 4 |
| **P2** | the S1 C3 age surface does not reproduce the engine's own `O32_GATE_DELTA` | the surplus construction; Steps 2-4 stop |
| **P3** | the S4 ruler copy does not md5-match the house file | the delivered-value ruler; Step 2 stops |
| **P4** | the pedigree premium is **not distinguishable from zero** on the young population, or is not distinguishable from zero at `g <= 7` | the case for a separate bar. **This is the null the order says matters.** The packet reports it and proposes nothing new |
| **P5** | the pedigree premium is **negative** — expensively priced players produce BELOW cheap ones at the same age | the direction of the bar. Reported, never inverted to suit the story |
| **P6** | `BETA_P` is not distinguishable from zero at every games level | the whole charge. Nothing is derived |
| **P7** | no `LAMBDA` in `(0, 3]` reproduces the current aggregate charge under the derived `A` and `T` | the anchoring half. The conflict is quantified, nothing is proposed |
| **P8** | any of P-S1 … P-S5 fails on any row of the board | the proposal. It is not put forward |
| **P9** | **picks 1-10 still breaks the +14% buy rail** in the PRIMARY window under the derived charge | **the owner's prediction that the inflation collapses on its own.** Reported plainly with the number |
| **P10** | relief still flows to the top of the draft: `abs(Spearman(pick, relief as a share of v0)) > 0.20` under the derived charge | the claim that the new bar is pedigree-neutral. Smuggle channel S1 confirmed |
| **P11** | the measured production premium is shallower than the price premium over the same pedigree range | smuggle channel S2 confirmed: the bar under-charges expensive players relative to what is priced into them |
| **P12** | the late bands (31-40, 41-64) come out WORSE than ORDER K in either window | the other half of the owner's complaint about ORDER N. Reported with the numbers |

---

## 8 · WHAT THIS SEAT WILL NOT DO

- It will not build a board.
- It will not edit the engine, the law, or any ledger.
- It will not adopt, rule, or recommend on its own word.
- It will not tune any constant to move any named player to any value.
- It will not report a Step 4 number without the words "estimate, pending a build" attached.
- It will not present a pedigree-conditional bar as safe on the forbidden set without measuring both
  smuggle channels named in §2.2 and printing whichever answer comes out.

**Deliverable:** `PACKET_P.md` in this directory — the old-par comparison and the forbidden-set
verdict, the measured surface, the derived charge, the test of the owner's prediction, the band
tables in both windows, the peaks, the class, the illustrations, and any conflicts. Plain language,
short sentences, one idea each, worked examples, no metaphors.
