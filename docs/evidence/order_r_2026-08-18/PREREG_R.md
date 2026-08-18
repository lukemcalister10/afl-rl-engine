# PREREG R — SOFTENING THE ORDER P CHARGE: THE CAP AND THE SLOPE, PRICED

**Seat:** ORDER R. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Base board:** ORDER P `374d4e44`, total 666,434.
**All variants sit ON TOP OF FIX B1** (`RL_O38B1`, the age-24 gate deleted). That repair is settled
and independent, and this order does not re-litigate it.
**Comparators:** ORDER K `f3101883` 673,097 · live `88ce647f` 752,429 (never touched) ·
ORDER Q FIX A `d7aad579` · FIX B1 `1b1817f3` 659,867 · A+B1 `cbbb94d4` 662,685.

**THIS IS A MEASUREMENT ORDER. NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED.**
**NO PULL REQUEST IS OPENED.** This seat delivers numbers.

**This file is pushed before the first engine edit.** Everything below is written down in advance.

---

## 1 · WHAT THE OWNER RULED, TAKEN AS GIVEN

The owner judges the ORDER P charge too harsh on hard underperformers: it "effectively stripped
their pedigree". Zane Duursma is charged 97.3% of his pedigree leg because he sits AT the `TMAX` cap.

Two rulings, taken as given and NOT re-litigated by this seat:

1. **"tmax should be 15 or 20 not 5"** — set the cap at the 15th or 20th percentile of the young
   cohort's own surplus distribution instead of the 5th. **BOTH are priced.**
2. **"maybe soften the charge a little bit"** — lower `BETA_sat`, but ONLY inside its published 90%
   CI `[0.10416, 0.12718]`. Softening outside the measured interval is forbidden and this seat does
   not do it.

A third ruling changes how the rails are read:

3. **The year-1 +14% buy rail is LOOSENED.** A year-1 breach is acceptable **provided the path
   afterwards does not keep beating carry and the end destination does not keep increasing.**

---

## 2 · THE MECHANISM AND WHAT MOVES

    pi *= exp( -LAMBDA * A(g) * T(s_P) )
    A(g) = 1 - exp(-g/G0)
    T(s) = clip( 1 - THETA_R*(s - s0), 0, TMAX )

Constants on ORDER P, all carried unchanged unless named:

| constant | value | status under ORDER R |
|---|---|---|
| `G0` | 9.890000000000008 | UNCHANGED |
| `LAMBDA` | 0.1743833036575403 | **UNCHANGED — see the disclosure in §7** |
| `BETA_sat` | 0.11464630061141393, 90% CI [0.10416359711151935, 0.1271777523096214] | **MOVED, inside the CI only** |
| `s0` | -2.452720891469074 | UNCHANGED |
| `THETA_R` | `BETA_sat / LAMBDA` = 0.657439 | **FOLLOWS `BETA_sat`. NOT FREE.** |
| `TMAX` | `1 - THETA_R*(s_pQ - s0)` = 21.1233 at Q=5 | **FOLLOWS `THETA_R` AND the chosen percentile. NOT FREE.** |

**`TMAX` IS RECOMPUTED FROM THE EFFECTIVE `THETA_R` EVERY TIME. No stale value is held.** That is
asserted at load and it is falsifier **R10**.

### 2.1 The percentile values, measured from ORDER P's own population

`s_p5` in `MECH_P.json` is `np.percentile(sP, 5)` over the 4,143 young-cohort season rows in
`STEP2_P.json`. Re-run here on the same object, same estimator, same rows:

| percentile | s_pQ |
|---:|---:|
| 5 (ORDER P's own) | **-33.06133449874688** — reproduces `MECH_P.json::s_p5` to the last bit |
| 15 | **-22.148794633345666** |
| 20 | **-19.024574086528315** |

### 2.2 The three `BETA_sat` values and why each one

| tag | `BETA_sat` | why this value |
|---|---:|---|
| **b0** | **0.11464630061141393** | ORDER P's point estimate. The control. |
| **b1** | **0.111** | **Clears the average SMALL premium slope.** The pedigree leg falls with price wherever `dPG/dln(v0) > 1/(BETA_sat*A)`. At saturation `A=1` the threshold is `1/BETA_sat`. The SMALL premium's average slope across its whole support is **8.9432** points per log-unit, so the threshold clears at `BETA_sat < 1/8.9432 = 0.111816`. **0.111 is the round value just below that.** It is inside the CI. (TALL's average slope is 8.2896, threshold 0.120633, already cleared by b0 — so the average-slope reversal is a SMALL-class fact.) |
| **b2** | **0.105** | **Near the CI floor.** The published 90% CI floor is 0.10416359711151935; 0.105 is the round value just above it. It is inside the CI. Nothing below the floor is priced. |

**b1 and b2 are chosen from the measured objects above, not tuned to any board or any row.**

### 2.3 What the cap does to the worst-charged row, computed in advance

`A(38) = 0.9787` for a 38-game row. Predicted charge on the pedigree leg AT the cap:

| | b0 0.11465 | b1 0.111 | b2 0.105 |
|---|---:|---:|---:|
| **p5** `TMAX` | 21.1233 → **97.28%** | 20.4833 → 96.97% | 19.4301 → 96.37% |
| **p15** `TMAX` | 13.9490 → **90.75%** | 13.5371 → 90.07% | 12.8594 → 88.86% |
| **p20** `TMAX` | 11.8950 → **86.86%** | 11.5485 → 86.06% | 10.9783 → **84.64%** |

The 97.28% reproduces the owner's 97.3% on Zane Duursma. **These are arithmetic, not board numbers.**
The board numbers are what this order measures.

---

## 3 · WHAT WILL BE BUILT — 12 BOARDS, AND WHAT IS DELIBERATELY NOT BUILT

Two new dials, both default-off:

| dial | what it does |
|---|---|
| `RL_O39_TMAXPCT` | the percentile `TMAX` is set at. Unset or 5 = ORDER P's own. Accepts 5, 15, 20 only. |
| `RL_O39_BETASAT` | the effective `BETA_sat`. Unset = ORDER P's point estimate. HALTS outside the published 90% CI. |

Both unset ⇒ **not one byte of the ORDER R block changes any number**, and every ORDER P and ORDER Q
board reproduces BYTE-EXACT. The dials only reach the ORDER Q (`RL_O38*`) charge path; setting one
with no `RL_O38*` dial live HALTS rather than silently doing nothing.

The full grid is 3 percentiles x 3 `BETA_sat` x 2 FIX A = **18**. **12 are built.**

| # | tag | pct | BETA_sat | FIX A | on B1 | why this cell |
|---|---|---|---|---|---|---|
| 1 | `Roff` | — | — | off | no | **control** — must be ORDER P `374d4e44` byte-exact |
| 2 | `RB1` | 5 | b0 | off | yes | **control** — must be FIX B1 `1b1817f3` byte-exact |
| 3 | `RAB1` | 5 | b0 | **on** | yes | **control** — must be A+B1 `cbbb94d4` byte-exact |
| 4 | `R15` | **15** | b0 | off | yes | the TMAX lever, alone |
| 5 | `R20` | **20** | b0 | off | yes | the TMAX lever, alone, at its far end |
| 6 | `R15A` | **15** | b0 | **on** | yes | the TMAX lever with A |
| 7 | `R20A` | **20** | b0 | **on** | yes | the TMAX lever with A |
| 8 | `Rb1` | 5 | **0.111** | off | yes | the BETA lever, alone |
| 9 | `Rb2` | 5 | **0.105** | off | yes | the BETA lever, alone, at its far end |
| 10 | `R15b1` | **15** | **0.111** | off | yes | the middle of both levers — the interaction |
| 11 | `R20b2` | **20** | **0.105** | off | yes | **both levers at their softest** |
| 12 | `R20b2A` | **20** | **0.105** | **on** | yes | both levers at their softest, with A |

**WHAT IS NOT BUILT, AND WHY. Stated in advance so it is not an excuse afterwards.**

- **(p5, b1, A on) and (p5, b2, A on)** — the A-on reading of the BETA lever at p5. Not built.
  FIX A's increment is measured at three points already (p5/b0 as cells 2→3, p15/b0 as 4→6,
  p20/b0 as 5→7, and p20/b2 as 11→12). If A's increment turns out to depend on the BETA lever by
  more than the materiality threshold, this seat will say the omission mattered.
- **(p15, b2), (p20, b1), and their A-on partners** — the interior of the 3x3 lever grid. Not built.
  Cells 2/4/5 give the TMAX lever at fixed b0; cells 2/8/9 give the BETA lever at fixed p5; cells
  10 and 11 give two diagonal readings of the interaction. If cells 10 and 11 come out close to the
  sum of the two single-lever moves, the interior is interpolable and the omission is harmless. **If
  they do not, this seat will report that the grid was under-built.**
- **Any cell WITHOUT B1.** The order fixes B1 as the base for every variant.
- **No `LAMBDA` re-solve.** See §7.

---

## 4 · THE READ-ONLY POSITION TEST — NO BOARD, RUN REGARDLESS

`PG` is pooled into TALL (KPD/KPF/RUCK) and SMALL (MID/SD/SF). The position-specific S1 **age bar**
already separates the positions (MID 75.59 against SF 66.39 at age 21). The pooled object is only the
pedigree INCREMENT above each position's own bar. This is measured, on ORDER P's own estimator
(`op_lib.Premium`, local-linear tricube, bandwidth 0.40 in log-v0 units, games-weighted, isotonised),
refitted per position:

1. Does `dPG/dln(v0)` differ materially between MID, SD and SF? Between KPD, KPF and RUCK?
2. What is the per-position effective sample (ESS) across the price range, especially at the
   expensive end?
3. Is a per-position fit statistically supportable for any position, and for which? **CIs reported,
   from a player-level cluster bootstrap on ORDER P's own seed 32.**
4. Would a per-position premium reduce or worsen the pick reversal? Reasoned from the measured slopes
   against the `1/(BETA_sat*A)` threshold.

**A null is a result. If the answer is "only MID has the sample", that is what will be written.**

---

## 5 · WHAT IS REPORTED FOR EVERY VARIANT

- **The burn census** — rows that would price HIGHER had they been drafted later on identical output —
  by pick band, using **ORDER Q's engine-verified method** (`oq_census.py`), NOT the supervisor's
  inference.
- **Max charge and the charge distribution**: rows charged >90%, >75%, >50%, and the maximum.
- **Named rows**: Zane Duursma, Josh Sinn, Campbell Chesser, Finn O'Sullivan, Zeke Uwland, Harley
  Reid, Sam Darcy, Willem Duursma, Sam Lalor. **NO NAMED-PLAYER TARGETS. Not one constant in this
  order is chosen with any row in view, and no row's value is an acceptance criterion. This is a
  standing prohibition in this project after a real error.**
- **The full no-arb tables in the STANDING format** — year paths yr0-7, appreciation, margin,
  verdict, for bands 1-10 / 11-20 / 21-30 / 31-40 / 41+ plus ALL / 1-20 / 21-64, in BOTH windows
  (full history and modern 2019-2023), plus the pool arms both windows, both baselines per row.
- **The owner's path test on EVERY breaching cell**, defined here in advance so it cannot be bent
  afterwards. Carry compounds at 14%: **1.140 / 1.300 / 1.482 / 1.689 / 1.925 / 2.195 / 2.502** for
  years 1..7. For a cell whose year-1 appreciation exceeds +14%:
  - **limb (a) — "the path afterwards does not keep beating carry":** count the years k in 2..7 where
    `path_k > carry_k`. Limb (a) PASSES when that count is 0.
  - **limb (b) — "the end destination does not keep increasing":** limb (b) PASSES when
    `path_7 <= path_6` (the path is not still rising at the end) AND `path_7 <= carry_7`.
  - **The cell PASSES the owner's path test only when both limbs pass.** Every raw year is printed
    alongside so the owner can apply his own reading instead of this seat's.
- **Class marks** on the **W2 basis (DRAFT classes 2005-2015, ENTRY_FLOOR 2005 — NOT the
  `ok_class.py` 2004-2014 window)** and the per-class table, including the three classes currently
  over 1.14 (draft 2010 1.1570, 2011 1.1595, 2015 1.2047).
- **Board total; movers ledger; mature-row movement; continuity on every axis INCLUDING age across
  23/24; determinism x2; dial-off identities.**

---

## 6 · FALSIFIERS. TEN OF THEM HALT.

| # | falsifier | halt? |
|---|---|---|
| **R1** | with both ORDER R dials unset the board is not `374d4e44` BYTE-EXACT | HALT |
| **R2** | with the R dials unset and `RL_O38B1=1` the board is not `1b1817f3` BYTE-EXACT | HALT |
| **R3** | with the R dials unset and `RL_O38A=1 RL_O38B1=1` the board is not `cbbb94d4` BYTE-EXACT | HALT |
| **R4** | determinism x2 fails on any variant board | HALT |
| **R5** | any variant prices a row ABOVE its own uncharged (eta-zero) price | HALT |
| **R6** | any variant moves a day-0 print or any of the 89 gameless rows | HALT (`A(0)=0` still) |
| **R7** | on any FIX A board the burn census is not ZERO | HALT |
| **R8** | a variant dial does not carry the O37/O36/O35/O32/O31 stack on its own defaults | HALT |
| **R9** | `LAMBDA * THETA_R_eff != BETA_sat_eff` at load, to 1e-15 | HALT |
| **R10** | `TMAX_eff != 1 - THETA_R_eff*(s_pQ - s0)` at load, to 1e-12 — a stale `TMAX` | HALT |
| **R11** | an effective `BETA_sat` outside the published 90% CI is accepted | HALT |
| R12 | the W2 class mark reaches 1.14 or falls below 1.03 on any variant | report, do not halt |
| R13 | a pick band or pool arm breaches a rail that ORDER P did not | report; run the path test |
| R14 | the max charge does not fall as the percentile rises | report — it would mean the lever is not the lever |
| R15 | cells 10/11 are not close to the sum of the two single-lever moves | report — the grid was under-built |

---

## 7 · THE DISCLOSURES, WRITTEN BEFORE THE FIRST BUILD

**`LAMBDA` IS NOT RE-SOLVED, AND THAT IS A REAL CHOICE, NOT AN OVERSIGHT.** On ORDER P, `LAMBDA`
was SOLVED by an anchoring identity: bisection so the new charge removes exactly the same total
points from the year-1 class-mark population as ORDER K's blind charge did. Moving `BETA_sat` or
`TMAX` BREAKS that anchor. This order holds `LAMBDA` fixed because the order says to
(`THETA_R = BETA_sat/LAMBDA` with `LAMBDA` given), and because re-solving it would claw back exactly
the softening the owner asked for — the anchor's whole job is to hold the total constant. **The
consequence is that these variants remove LESS total charge than ORDER P did, by construction. That
is the softening. It is stated here so it is not later presented as a discovery.**

**The premium surface `PG` IS NOT REFITTED.** It is ORDER P's published grid, byte for byte. Changing
`BETA_sat` changes the charge's slope, not the measurement the bar is built from.

**`s0` IS NOT MOVED.** `T(s0) = 1` still, so a row at the cohort centre pays the same base charge on
every variant. Only the cap and the slope move.

**The percentile is a percentile of the SAME population `MECH_P.json` used**, computed by the same
`np.percentile` call, unweighted, over the same 4,143 rows. It is reproduced to the last bit before
it is used.

---

## 8 · PREDICTIONS, WRITTEN BEFORE THE FIRST BUILD

These are predictions. Being wrong is a finding, not a failure.

1. **The TMAX percentile is by far the stronger lever.** p5→p20 cuts the cap 44% (21.12→11.89);
   b0→b2 cuts it about 8% at any percentile. Predicted ratio of effect: roughly 5 to 1.
2. **Every softening raises the board total** against FIX B1's 659,867, monotonically in the
   percentile and monotonically as `BETA_sat` falls.
3. **The burn census FALLS as the cap falls, without FIX A.** The reversal lives where `T` is in its
   interior; a lower cap parks more rows AT the cap, where `dT/ds = 0` and the leg is monotone in
   price. Lowering `BETA_sat` also raises the reversal threshold `1/(BETA_sat*A)`. Predicted: the
   burn count falls on both levers and is **not** zero on any A-off board.
4. **FIX A still takes the burn census to exactly zero on every A-on board.** Structural.
5. **The rails move the wrong way for the owner.** Softening the charge raises young year-1 prices,
   which raises year-1 appreciation, which pushes the top bands THROUGH the +14% buy rail.
   Predicted: MODERN picks 1-20 breaches at p20 even with FIX A off; MODERN picks 1-10 gets worse
   than ORDER P's +18.85% on every softened board. **This is the direct tension between the owner's
   two instructions and it will be reported as such.**
6. **The W2 class mark RISES with the softening**, because the mark is a year-1-over-year-0 ratio and
   year 0 is a day-0 print that cannot move. Predicted above ORDER P's 1.0613 on every variant, and
   predicted still under 1.14.
7. **The three classes over 1.14 get WORSE, not better, on every variant.** Nothing here touches the
   channel that put them there.
8. **Mature-row movement shrinks with the softening.** B1 costs 6,567 points against ORDER P;
   predicted materially smaller at p20 because the veterans B1 reaches are exactly the ones parked
   at the cap.
9. **Position test:** predicted that **only MID has the effective sample at the expensive end**, and
   that SD, SF, KPD, KPF and RUCK are all too thin above the median price for a supportable
   per-position fit. Predicted that MID's slope is close to the pooled SMALL slope, because MID
   carries most of SMALL's games weight — so a per-position premium would **not** materially reduce
   the reversal for MID, and would make SD/SF noisier rather than better.

**Materiality, fixed here before any result: 0.5 percentage points on a band, 0.002 on a class mark,
0.3% on the board total.**

---

## 9 · CONVENTIONS THIS SEAT IS HELD TO

- **NOTHING IS ADOPTED. NOTHING LANDS. NO PULL REQUEST. NOTHING IS PUSHED TO `main`.**
- **NO named-player targets.** Named rows are consequences only.
- **Nulls reported as nulls.** Never scored zero, never dropped.
- **HALT AND REPORT on any law breach.** Never trade one law for another silently.
- **Built-against-expected, reported loudly.**
- **Plain speech.** Short sentences. One idea each. No metaphors for mechanics. What is MEASURED is
  marked apart from what is asserted and not checked.
- The working directory `/home/user/afl-rl-engine` is shared and its checked-out branch is NOT
  changed by this seat. All work is in a separate `git worktree`.
- Engine runs are STRICTLY SEQUENTIAL. Board and store pins are threaded and printed on every run.
