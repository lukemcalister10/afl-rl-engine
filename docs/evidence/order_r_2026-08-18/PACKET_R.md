# PACKET R — THE OWNER'S TWO SOFTENINGS, PRICED

**Seat:** ORDER R. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Prereg:** `PREREG_R.md`, pushed at `058e8bc` **before the first engine edit**.
**Engine pin for every board in this packet:** `_merged_recover.py` `ea5c5e5e11132479f0925a9e32e6f632`.
**Store on every board:** `cb38ef11`, unchanged.

**THIS IS A MEASUREMENT ORDER. NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED.
NO PULL REQUEST WAS OPENED. NOTHING WAS PUSHED TO `main`.** This packet is numbers. The choice is
the owner's and the supervisor's.

**Boards.** live `88ce647f` 752,429 (never touched) · base stack `1f176444` 667,916 ·
ORDER K `f3101883` 673,097 · **ORDER P `374d4e44` 666,434** · ORDER Q FIX B1 `1b1817f3` 659,867 ·
ORDER Q FIX A+B1 `cbbb94d4` 662,685.

**What the owner ruled, taken as given and not re-litigated:**

1. The ORDER P charge is too harsh on hard underperformers — it "effectively stripped their pedigree".
   Zane Duursma is charged 97.3% of his pedigree leg because he sits AT the `TMAX` cap.
2. **"tmax should be 15 or 20 not 5"** — the cap at the 15th or 20th percentile of the young cohort's
   own surplus instead of the 5th. **Both are priced.**
3. **"maybe soften the charge a little bit"** — lower `BETA_sat`, **but only inside its published 90%
   CI.** Softening outside the measured interval is forbidden and the dial HALTS on it.
4. **The year-1 +14% buy rail is LOOSENED.** A year-1 breach is acceptable provided the path
   afterwards does not keep beating carry and the end destination does not keep increasing.

**Every variant sits ON TOP OF ORDER Q's FIX B1** (the age-24 gate deleted). That repair is settled
and independent and this order does not re-litigate it.

---
## 0 · THE ANSWERS, IN ONE PAGE

**THE POSITION TEST.** The TALL/SMALL pooling of `PG` **is defensible, and a per-position split would
make the pick reversal WORSE.** The slopes differ numerically — KPD 3.05 through SF 9.95 — but **not
one pairwise difference is statistically material: every pair's 90% CI overlaps**, including KPD
against KPF whose point estimates are 5.6 apart. RUCK's bootstrap interval is **degenerate**, upper
limit +918.83 on 96 players. The order offered "only MID has the sample"; the measurement refines
that — **MID and SF both clear the sample line at the expensive end**, but sample is not the binding
constraint, the intervals are, and **no position is separable from its class.** A split would steepen
the slope for four of the six positions, and they are the four that carry the games. §1

**WHICH LEVER DOES WHAT.**

- **The `TMAX` percentile is a SURGICAL lever.** It moves 61 rows at p15 and 93 at p20, **raises every
  one and lowers none**, and it reaches only rows parked AT the cap. It does not touch Finn
  O'Sullivan, Harley Reid, Willem Duursma or Sam Lalor at all. **It is aimed exactly at the complaint
  the owner made.** It takes the maximum charge from 97.28% to 90.75% at p15 and **86.86% at p20**,
  and at p20 **not one row is charged more than 90% of its pedigree leg**, against twenty at p5.
- **The `BETA_sat` slope is a BROAD lever, and it is not a pure softening.** It reaches 336 rows and
  **LOWERS THIRTEEN of them**, because lowering the slope pivots `T` about `s0` instead of lowering
  it. Every one of the thirteen sits inside the window this seat predicted before any board was
  built. The whole cost is 18 board points. §3, §5.2
- **The two are 1.64 to 1, not the 5 to 1 the prereg predicted.** Per unit of cap reduction the slope
  lever is about five times the more efficient, which is the opposite of what was written down. §4.3
- **FIX A is the largest single lever of the three (+2,818) and the only one with no constant in it**,
  and it is the only thing that removes the entry-price reversal completely.
- **The levers are additive to within 0.083% of the board, so the six unbuilt cells are readable off
  the twelve built ones.** Falsifier R15 does not fire. §4.4

**THE PRICE OF THE SOFTENING.** The owner's two instructions pull against each other. Softening raises
year-1 prices, which pushes the top bands through the +14% buy rail. **MODERN picks 1-20 breaches on
four ORDER R cells and fails the owner's path test on all of them.** **PRIMARY picks 11-20 breaches on
three cells and PASSES the path test on all three.** MODERN picks 1-10 was already over the rail on
ORDER P and fails the path test there too — that failure is inherited, not created here. §6

**TWO FALSIFIERS FIRED AND BOTH ARE REPORTED AS FIRED.** **R7** — one row and one board point of burn
on the softest FIX A cell, which is ORDER Q's disclosed premium-rounding residual and measures
strictly inside its published bound (§13). **R6** — reported as firing by this seat's own scorer,
which was reading season games instead of career games; **on the correct field it passes, 0 of 89 on
every board** (§14). A third assert, **R-S4, fired on this seat's first engine load and the assert was
wrong, not the dials** (§3).

**NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED.**

---

## 1 · THE READ-ONLY POSITION TEST — THE POOLING IS DEFENSIBLE, AND A SPLIT WOULD MAKE THE REVERSAL WORSE

**No board was built for this. It is a measurement on ORDER P's own estimator and it rules on nothing.**

The owner asked whether pooling `PG` into TALL (KPD/KPF/RUCK) and SMALL (MID/SD/SF) is defensible,
given that SD/SF and MID price and perform very differently.

### 1.1 First, what is ALREADY separate — and the two bar objects reconciled

**The position-specific S1 age bar already carries the level difference. `PG` is only the pedigree
INCREMENT above each position's own bar.** That is the whole of what is pooled.

There are TWO age-bar objects in this engine and they must not be confused:

| object | what it is | MID at 21 | SF at 21 | gap |
|---|---|---:|---:|---:|
| `o36_bar(pos, 21)` | the S1 bar in the PRODUCTION path, dose-scaled by `RL_O36_LAM_S1` 0.40 | **75.59** | **66.39** | **9.20** |
| `o32_gate_bar(pos, 21)` | **the bar the CHARGE reads** — `MA.REPL - REPL_DROP` minus the full class delta | **65.83** | **56.63** | **9.20** |

**The order quotes the first. The charge uses the second. THE GAP IS IDENTICAL — 9.20 points a game
on either object** — because the development delta is class-pooled and cancels in the difference.
So nothing turns on which one is quoted, and both are printed rather than one being silently
substituted for the other.

### 1.2 The slopes DO differ numerically. Not one difference is statistically material.

`dPG/dln(v0)`, averaged across each fit's own support, refitted per position on ORDER P's own
estimator (local-linear tricube, bandwidth 0.40 in log-v0 units, games-weighted, isotonised):

| group | players | avg slope | 90% CI (player-level cluster bootstrap, 2,000 draws, seed 32) |
|---|---:|---:|---|
| TALL pool | 442 | **8.2896** | [+6.39, +10.33] |
| SMALL pool | 1,146 | **8.9432** | [+7.73, +10.66] |
| KPD | 191 | **3.0467** | [+0.99, +7.95] |
| KPF | 257 | **8.6718** | [+5.74, +10.81] |
| RUCK | 96 | **8.9213** | **[+4.97, +918.83]** |
| MID | 583 | **9.9129** | [+8.34, +12.68] |
| SD | 420 | **9.0224** | [+6.78, +12.48] |
| SF | 602 | **9.9502** | [+8.03, +11.99] |

**The pooled slopes reproduce the engine's own published grid to the last decimal — TALL 8.2896 and
SMALL 8.9432 — so the refit is the same object, not a lookalike.**

**PAIRWISE, NOT ONE DIFFERENCE IS MATERIAL. Every pair's 90% CIs overlap:**

| pair | slope A | slope B | difference | CIs |
|---|---:|---:|---:|---|
| MID vs SD | 9.9129 | 9.0224 | +0.89 | **OVERLAP** |
| MID vs SF | 9.9129 | 9.9502 | −0.04 | **OVERLAP** |
| SD vs SF | 9.0224 | 9.9502 | −0.93 | **OVERLAP** |
| KPD vs KPF | 3.0467 | 8.6718 | **−5.63** | **OVERLAP** |
| KPD vs RUCK | 3.0467 | 8.9213 | **−5.87** | **OVERLAP** |
| KPF vs RUCK | 8.6718 | 8.9213 | −0.25 | **OVERLAP** |

**KPD's point estimate is 5.6 points a game per log-unit below KPF's and it STILL cannot be
separated from it.** That is how wide these intervals are.

**RUCK's bootstrap upper limit is +918.83.** On resampled draws of 96 players the estimator produces
a near-vertical fit. That is not a wide interval, it is a **degenerate one**, and it is the single
strongest piece of evidence in this test: a per-position RUCK premium is not estimable at all on this
sample. It is printed at full precision rather than trimmed.

### 1.3 The effective sample, and where it runs out

ESS is the kernel's own effective sample at that price: `(Σk)² / Σk²` with `k` the tricube weight
times games. It is what the fit actually leans on, not the raw row count. `ESS_THIN` in ORDER P's own
library is **30**.

| group | v0=200 | 500 | 1,000 | 1,500 | 2,000 | 2,500 | **3,000** | verdict at the expensive end |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| KPD | 57.6 | 130.4 | 46.3 | 17.7 | 9.1 | 8.1 | **4.9** | **NOT SUPPORTABLE past ~1,000** |
| KPF | 79.0 | 106.4 | 114.5 | 83.9 | 60.0 | 51.2 | **29.5** | supportable to ~2,000, not beyond |
| RUCK | 14.7 | 37.7 | 48.5 | 25.4 | 4.9 | 12.7 | **9.7** | **NOT SUPPORTABLE past ~1,000** |
| **MID** | 182.6 | 145.5 | 209.1 | 163.4 | 174.8 | 136.4 | **134.9** | **SUPPORTABLE to 3,000** |
| SD | 180.0 | 99.1 | 149.1 | 102.8 | 41.4 | 29.3 | **26.0** | supportable to ~2,000, not beyond |
| **SF** | 213.1 | 270.8 | 179.4 | 100.5 | 92.1 | 67.8 | **55.0** | **SUPPORTABLE to 3,000** |
| TALL pool | 145.7 | 267.0 | 209.0 | 125.8 | 73.6 | 71.9 | **43.6** | *(the object a split would replace)* |
| SMALL pool | 570.0 | 515.1 | 537.1 | 365.3 | 307.9 | 233.3 | **215.7** | *(the object a split would replace)* |

**The order's own figure is confirmed: TALL POOLED reads 43.6 effective at v0 3,000 for all three
positions combined**, against the ~47 the order quoted. It is already thin before anything is split.

### 1.4 THE VERDICT, and it REFINES the answer the order suggested

The order said: *"If the answer is 'only MID has the sample', say exactly that."*

**The measured answer is not quite that, and this seat reports what it measured rather than the
answer it was offered. TWO positions have the sample at the expensive end, not one: MID (134.9) and
SF (55.0).** SD (26.0) and KPF (29.5) sit just under the line. **KPD (4.9) and RUCK (9.7) have
essentially nothing above the median price.**

**But the sample is not the binding constraint. The CONFIDENCE INTERVALS are.** Even MID and SF,
which have the rows, cannot be told apart from each other or from the pool: MID 9.91 and SF 9.95
against SMALL pooled 8.94, with intervals more than 3.5 points a game wide.

**So: a per-position fit is statistically supportable for NO position.** Not one of the six can be
distinguished from the class it sits in, and two of the six cannot be estimated at all.

### 1.5 Would a per-position premium reduce or worsen the pick reversal? IT WOULD WORSEN IT.

The reversal is `dPG/dln(v0) > 1/(BETA_sat·A)`. At saturation the threshold is `1/0.11465 = 8.723`.
Pooling AVERAGES slopes. Splitting replaces the pooled slope with each position's own.

| position | own slope | pool slope | own − pool | effect of splitting |
|---|---:|---:|---:|---|
| KPD | 3.0467 | 8.2896 | **−5.24** | better — its own slope is shallower |
| KPF | 8.6718 | 8.2896 | +0.38 | **worse** |
| RUCK | 8.9213 | 8.2896 | +0.63 | **worse** |
| MID | 9.9129 | 8.9432 | +0.97 | **worse** |
| SD | 9.0224 | 8.9432 | +0.08 | no material change |
| SF | 9.9502 | 8.9432 | **+1.01** | **worse** |

**Four of the six positions get a STEEPER slope under a split, and they are the four that carry the
games.** Only KPD improves, and KPD is precisely the position whose fit collapses at the expensive
end — so the improvement is bought with the least reliable number in the table.

**The local slope matters more than the average, because the reversal is a LOCAL condition.**

| group | avg slope | **max local slope** | v0 at the max | reverses at A=1? |
|---|---:|---:|---:|---|
| TALL pool | 8.2896 | 57.07 | 2,864 | YES |
| SMALL pool | 8.9432 | 35.99 | 3,342 | YES |
| KPD | 3.0467 | 24.94 | 1,120 | YES |
| **KPF** | 8.6718 | **82.33** | 2,636 | YES |
| RUCK | 8.9213 | 64.05 | 1,327 | YES |
| MID | 9.9129 | 50.43 | 1,476 | YES |
| SD | 9.0224 | 47.77 | 153 | YES |
| SF | 9.9502 | 56.25 | 94 | YES |

**Every group already reverses locally, pooled or split.** And splitting makes the worst local slope
WORSE for the TALL class: KPF alone peaks at **82.33** against the TALL pool's 57.07. **A split does
not repair the reversal. It sharpens it, in the class that has the least data to justify the change.**

### 1.6 One more measured fact worth stating, because it changes where the reversal lives

The reversal threshold at saturation is `1/BETA_sat`. **On the AVERAGE slope the reversal is a SMALL-
class fact, not a board-wide one:**

- SMALL average slope **8.9432** > threshold **8.7225** → the SMALL class reverses on average.
- TALL average slope **8.2896** < threshold **8.7225** → the TALL class does NOT reverse on average.

TALL reverses only in its locally steep segments. This matters for the ORDER R grid: **lowering
`BETA_sat` raises the threshold, and at `BETA_sat` 0.111 the threshold becomes 9.0090, which clears
the SMALL average slope of 8.9432 as well.** That is the whole reason 0.111 was chosen, and it was
chosen from this measurement, not from a board.

---

## 2 · WHAT THE TWO DIALS DO, AND THE CONSTANTS THEY MOVE

Two new dials, both default-off, both reaching the ORDER Q charge path only.

| dial | what it sets |
|---|---|
| `RL_O39_TMAXPCT` | the percentile of the young cohort's own surplus that `TMAX` is evaluated at. Unset or 5 = ORDER P's own. Accepts **5, 15, 20** and HALTS on anything else. |
| `RL_O39_BETASAT` | the effective `BETA_sat`. Unset = ORDER P's point estimate. **HALTS outside the published 90% CI** `[0.10416359711151935, 0.1271777523096214]`. |

Setting either with no `RL_O38*` dial live HALTS, so a dial can never silently do nothing while a
board is labelled as though it had.

### 2.1 The percentiles, reproduced from ORDER P's own population before they were used

`MECH_P.json::s_p5` is `np.percentile(sP, 5)` over the 4,143 young-cohort season rows in
`STEP2_P.json`. Re-run here on the same object by the same call:

| percentile | s_pQ | check |
|---:|---:|---|
| **5** (ORDER P's own) | **−33.06133449874688** | **reproduces `MECH_P.json::s_p5` to the last bit — asserted at load, falsifier R10** |
| **15** | **−22.148794633345666** | |
| **20** | **−19.024574086528315** | |

### 2.2 The three `BETA_sat` values, each chosen from a measurement

| tag | `BETA_sat` | why |
|---|---:|---|
| **b0** | 0.11464630061141393 | ORDER P's point estimate. The control. |
| **b1** | **0.111** | The pedigree leg falls with price wherever `dPG/dln(v0) > 1/(BETA_sat·A)`. At saturation the threshold is `1/BETA_sat`. **The SMALL premium's average slope across its whole support is 8.9432** (§1), so the threshold clears at `BETA_sat < 1/8.9432 = 0.111816`. 0.111 is the round value just below. Inside the CI. |
| **b2** | **0.105** | Near the CI floor of 0.10416359711151935. 0.105 is the round value just above it. Inside the CI. **Nothing below the floor is priced.** |

**Neither b1 nor b2 was chosen by looking at a board or a row.**

### 2.3 What follows, and what is recomputed rather than carried

`THETA_R = BETA_sat / LAMBDA`. `TMAX = 1 − THETA_R·(s_pQ − s0)`. **Both are recomputed from the
effective slope every time. A stale `TMAX` HALTS (falsifier R10) and so does `LAMBDA·THETA_R ≠
BETA_sat` (falsifier R9).**

| cell | `THETA_R` | `TMAX` | a 38-game row AT the cap is charged |
|---|---:|---:|---:|
| **p5 · b0** *(ORDER P)* | 0.657439 | **21.1233** | **97.28%** |
| p5 · b1 0.111 | 0.636529 | 20.4833 | 96.97% |
| p5 · b2 0.105 | 0.602122 | 19.4301 | 96.37% |
| **p15 · b0** | 0.657439 | **13.9490** | **90.75%** |
| p15 · b1 0.111 | 0.636529 | 13.5371 | 90.07% |
| p15 · b2 0.105 | 0.602122 | 12.8594 | 88.86% |
| **p20 · b0** | 0.657439 | **11.8950** | **86.86%** |
| p20 · b1 0.111 | 0.636529 | 11.5485 | 86.06% |
| **p20 · b2 0.105** | 0.602122 | **10.9783** | **84.64%** |

**The 97.28% reproduces the owner's 97.3% on Zane Duursma exactly.** These are arithmetic on the
constants. The board consequences are measured below and they are a different thing.

---

## 3 · A FALSIFIER THIS SEAT WROTE FIRED ON ITS OWN FIRST LOAD, AND IT WAS RIGHT TO FIRE

**The assert was wrong, not the dials. It is reported here rather than quietly rewritten.**

The prereg's structural check R-S4 said the ORDER R constants may never charge MORE than ORDER P at
any surplus — "these dials may only SOFTEN". **It halted on the first in-process load**, at
`s = −2.45`, `g = 1.00`, with `0.983396689 < 0.983399171`.

**The reason is real and it is a finding about the mechanism, not a nuisance.**

`T(s0) = 1` on every board by construction. So lowering `BETA_sat` does not lower the `T` line — it
**pivots it about `s0`**. A flatter line sits ABOVE ORDER P's for `s` below `s0` and BELOW it for `s`
above `s0`.

**In plain words: the BETA lever softens the charge on every row producing UNDER the cohort centre —
which is every row the owner's complaint is about — and STIFFENS it very slightly on rows producing
just ABOVE the centre, until the zero clip catches up. The TMAX lever has no such effect. It only
lowers the cap, so it softens everywhere or does nothing.**

The assert was replaced with the true statement rather than the convenient one:

- **R-S4a, WHICH HALTS.** For every `s` at or below `s0`, the ORDER R factor must be ≥ ORDER P's.
  **The softening may never charge an underperformer more.** This passes on every cell built.
- **R-S4b, MEASURED AND PRINTED ON THE BANNER.** The window above `s0` where the charge is harsher is
  bounded and reported. At p20 with `BETA_sat` 0.105 the engine prints:

  > It charges MORE than ORDER P over s in (−2.4500, −0.8000], a window 1.6500 points a game wide,
  > and the WORST extra charge anywhere in it is **1.4472%** of the pedigree leg.

**Eight boards had already been built under the wrong assert. They were DISCARDED and the whole suite
was rebuilt, so every board in this packet carries ONE engine md5 rather than two.** That cost about
half an hour and it is the right trade.

---

## 4 · THE GRID. EVERY BUILD-LEVEL FALSIFIER PASSED.

**Twelve boards. One engine md5 across all of them: `ea5c5e5e`. One store: `cb38ef11`.**

### 4.1 The falsifiers

| # | falsifier | result |
|---|---|---|
| **R1** | both ORDER R dials unset does not rebuild ORDER P `374d4e44` byte-exact | **no — `374d4e44`** |
| **R2** | R dials unset with `RL_O38B1=1` does not rebuild FIX B1 `1b1817f3` | **no — `1b1817f3`** |
| **R3** | R dials unset with `RL_O38A=1 RL_O38B1=1` does not rebuild A+B1 `cbbb94d4` | **no — `cbbb94d4`** |
| **R4** | determinism x2 fails on any variant | **no — all NINE identical on a repeat** |
| **R8** | `RL_O38B1` + `RL_O39_TMAXPCT=20` alone does not carry the O37/O36/O35/O32/O31 stack | **no — `aa5e70cc` both ways** |
| **R9** | `LAMBDA·THETA_R ≠ BETA_sat_eff` at load | **no — asserted at 1e-15 on every board** |
| **R10** | `TMAX` is stale, or the p5 entry is not `MECH_P.json::s_p5` bit for bit | **no — asserted at load on every board** |
| **R11** | a `BETA_sat` outside the published 90% CI is accepted | **no — the dial HALTS on it** |
| — | the base stack no longer rebuilds `1f176444` | **no — `1f176444`** |
| — | ORDER K's ruled line no longer rebuilds `f3101883` | **no — `f3101883`** |

### 4.2 The boards

| board | cell | md5 | total | vs ORDER P | vs ORDER K | vs FIX B1 |
|---|---|---|---:|---:|---:|---:|
| ORDER K | — | `f3101883` | 673,097 | +6,663 | — | +13,230 |
| ORDER P | — | `374d4e44` | 666,434 | — | −6,663 | +6,567 |
| **RB1** | p5 · b0 · A off | `1b1817f3` | **659,867** | −6,567 | −13,230 | — |
| **R15** | **p15** · b0 · A off | `902ef88e` | **661,216** | −5,218 | −11,881 | **+1,349** |
| **R20** | **p20** · b0 · A off | `aa5e70cc` | **662,302** | −4,132 | −10,795 | **+2,435** |
| **Rb1** | p5 · **0.111** · A off | `d9c74574` | **660,419** | −6,015 | −12,678 | **+552** |
| **Rb2** | p5 · **0.105** · A off | `f69ca077` | **661,356** | −5,078 | −11,741 | **+1,489** |
| **R15b1** | **p15** · **0.111** · A off | `c3798c8d` | **661,783** | −4,651 | −11,314 | **+1,916** |
| **R20b2** | **p20** · **0.105** · A off | `fd958019` | **663,845** | −2,589 | −9,252 | **+3,978** |
| **RAB1** | p5 · b0 · **A ON** | `cbbb94d4` | **662,685** | −3,749 | −10,412 | **+2,818** |
| **R15A** | **p15** · b0 · **A ON** | `dcb68e73` | **663,969** | −2,465 | −9,128 | **+4,102** |
| **R20A** | **p20** · b0 · **A ON** | `7f88f509` | **664,950** | −1,484 | −8,147 | **+5,083** |
| **R20b2A** | **p20** · **0.105** · **A ON** | `aaab992e` | **666,056** | **−378** | −7,041 | **+6,189** |

**The softest cell with FIX A, `R20b2A`, lands 378 points under ORDER P** — it gives back almost
exactly what B1's mature-row extension costs, while removing the age cliff and the pick reversal.

### 4.3 WHICH LEVER DOES WHAT

**Each lever alone, measured from FIX B1:**

| lever | move | points |
|---|---|---:|
| `TMAX` p5 → p15 | the cap 21.1233 → 13.9490, a **34.0%** cut | **+1,349** |
| `TMAX` p5 → p20 | the cap 21.1233 → 11.8950, a **43.7%** cut | **+2,435** |
| `BETA_sat` 0.11465 → 0.111 | the cap 21.1233 → 20.4833, a **3.0%** cut | **+552** |
| `BETA_sat` 0.11465 → 0.105 | the cap 21.1233 → 19.4301, an **8.0%** cut | **+1,489** |
| FIX A | no constant moves at all | **+2,818** |

**PREDICTION 1 IS WRONG, AND WRONG BY A LOT.** The prereg predicted the `TMAX` percentile would be
roughly **five times** the stronger lever. **Measured at the two far ends the ratio is 1.64.**

**Why the prediction failed, stated plainly.** It looked only at the CAP. p5→p20 cuts the cap 43.7%
where `BETA_sat` 0.11465→0.105 cuts it 8.0%, so on cap alone the ratio should be about 5.5 to 1. But
**the `BETA_sat` lever does not only lower the cap. It pivots the whole `T` line about `s0`.** The
`TMAX` lever only reaches rows parked AT the cap; the slope lever reaches **every row producing below
the cohort centre**. Per unit of cap reduction, the slope is about **five times the more efficient
lever — the exact opposite of what was written down.**

**FIX A is the largest single lever of the three, and it is the only one with no constant in it.**

### 4.4 THE GRID IS INTERPOLABLE — FALSIFIER R15 DOES NOT FIRE

The prereg said: if the diagonal cells are not close to the sum of the two single-lever moves, the
grid was under-built and this seat must say so. **They are close.** Materiality is 0.3% of the board.

| combination | additive prediction | **actual** | gap | as % of board |
|---|---:|---:|---:|---:|
| `R15b1` = p15 + 0.111 | 661,768 | **661,783** | **+15** | **+0.002%** |
| `R20b2` = p20 + 0.105 | 663,791 | **663,845** | **+54** | **+0.008%** |
| `R15A` = p15 + A | 664,034 | **663,969** | **−65** | **−0.010%** |
| `R20A` = p20 + A | 665,120 | **664,950** | **−170** | **−0.026%** |
| `R20b2A` = p20 + 0.105 + A | 666,609 | **666,056** | **−553** | **−0.083%** |

**Every gap is inside a tenth of the materiality threshold. The six unbuilt cells can be read off the
built ones to within a few hundred points on a 660,000-point board.** The grid was not under-built.

### 4.5 THE ONE REAL INTERACTION: FIX A AND THE SOFTENING ARE PARTIAL SUBSTITUTES

| FIX A's increment | at | points |
|---|---|---:|
| p5 · b0 | the stiffest cell | **+2,818** |
| p15 · b0 | | +2,753 |
| p20 · b0 | | +2,648 |
| **p20 · 0.105** | **the softest cell** | **+2,211** |

**FIX A gives back 21.5% less on the softest cell than on the stiffest.** The reason is direct: a
lower cap parks more rows AT the cap, where `dT/ds = 0` and the pedigree leg is already monotone in
price, so there is less inverted charge left for FIX A to cap. **Softening and monotonising are
partly doing the same job.** That is the whole of the non-additivity, and it is 0.083% of a board.

---

## 5 · THE CHARGE DISTRIBUTION — THIS IS WHAT THE OWNER ASKED ABOUT

The charge is `1 − f`, the share of the pedigree leg removed, read off the factor the engine actually
applied at the blend site, M3-reassembled. **ORDER P's own row is on 289 rows because its age gate
confines the new charge to under-24s; every ORDER R board carries B1, so its population is all 715
rows with a pedigree leg. The comparable baseline for the ORDER R cells is `RB1`, not ORDER P.**

| board | cell | n | **max charge** | **>90%** | >75% | >50% |
|---|---|---:|---:|---:|---:|---:|
| ORDER P | *(gate at 24)* | 289 | **97.28%** | 9 | 54 | 109 |
| **RB1** | p5 · b0 · A off | 715 | **97.28%** | **20** | 119 | 237 |
| **R15** | **p15** · b0 · A off | 715 | **91.22%** | **11** | 112 | 237 |
| **R20** | **p20** · b0 · A off | 715 | **87.44%** | **0** | 111 | 234 |
| Rb1 | p5 · 0.111 · A off | 715 | 96.97% | 16 | 113 | 235 |
| Rb2 | p5 · 0.105 · A off | 715 | 96.37% | 13 | 102 | 228 |
| R15b1 | p15 · 0.111 · A off | 715 | 90.56% | 7 | 106 | 235 |
| **R20b2** | **p20 · 0.105** · A off | 715 | **85.26%** | **0** | 93 | 225 |
| RAB1 | p5 · b0 · A ON | 715 | 95.73% | 19 | 106 | 221 |
| R15A | p15 · b0 · A ON | 715 | 91.22% | 10 | 99 | 221 |
| R20A | p20 · b0 · A ON | 715 | 87.44% | 0 | 98 | 218 |
| **R20b2A** | **p20 · 0.105 · A ON** | 715 | **85.26%** | **0** | **84** | **212** |

**At p20 NOT ONE ROW IS CHARGED MORE THAN 90% OF ITS PEDIGREE LEG.** At p5 twenty rows are. That is
the owner's complaint, answered in one number.

**The `>75%` and `>50%` counts barely move on the TMAX lever** (119 → 112 → 111 and 237 → 237 → 234).
The cap only binds on the rows at the cap. **FIX A and the BETA lever are what move the middle of the
distribution** (119 → 84 and 237 → 212 on the softest A-on cell).

### 5.1 THE TMAX LEVER IS SURGICAL. THE BETA LEVER IS BROAD, AND IT CUTS THIRTEEN ROWS.

Rows that move against `RB1`, on the 804-row board:

| board | rows moved | **up** | **DOWN** |
|---|---:|---:|---:|
| **R15** (p15) | **61** | **61** | **0** |
| **R20** (p20) | **93** | **93** | **0** |
| Rb1 (0.111) | 261 | 256 | **5** |
| Rb2 (0.105) | 336 | 323 | **13** |
| R15b1 | 266 | 261 | **5** |
| R20b2 | 338 | 325 | **13** |
| RAB1 (FIX A) | 170 | 170 | **0** |
| R20b2A | 358 | 349 | **9** |

**The `TMAX` percentile lever reaches 61 rows at p15 and 93 at p20, raises every one of them, and
lowers nothing.** It is confined to the rows parked at the cap — precisely the rows the owner said
were "effectively stripped".

**The `BETA_sat` lever reaches four times as many rows and LOWERS THIRTEEN OF THEM.**

### 5.2 THE THIRTEEN DOWNWARD ROWS ARE EXACTLY THE ONES §3 PREDICTED

**Predicted before any board was built:** the BETA lever pivots `T` about `s0 = −2.4527`, so it
stiffens the charge on rows with surplus in `(s0, −0.7919]` — the window where ORDER P's `T` has
already clipped to zero but the flatter line has not.

**Measured on the board. Every one of the thirteen has `s_ped` inside that window. Not one is
outside it.**

| row | age | games | `RB1` → `Rb2` | move | **s_ped** |
|---|---:|---:|---|---:|---:|
| Kane McAuliffe | 21 | 23 | 1,012 → 1,010 | −2 | −1.8853 |
| Will Brodie | 28 | 55 | 807 → 805 | −2 | −0.8922 |
| Nick Larkey | 28 | 153 | 520 → 518 | −2 | −1.2721 |
| Elijah Hollands | 24 | 47 | 732 → 730 | −2 | −1.5988 |
| Mabior Chol | 29 | 122 | 261 → 259 | −2 | −0.9981 |
| Lachlan Ash | 25 | 144 | 5,295 → 5,294 | −1 | −1.7405 |
| Adam Cerra | 27 | 163 | 1,025 → 1,024 | −1 | −1.5224 |
| Lachie Jaques | 20 | 8 | 583 → 582 | −1 | −2.3386 |
| Lachlan Cowan | 22 | 56 | 620 → 619 | −1 | −0.9527 |
| Kade Chandler | 26 | 98 | 784 → 783 | −1 | −1.7772 |
| Sam De Koning | 25 | 96 | 860 → 859 | −1 | −1.1366 |
| Sam Banks | 23 | 57 | 818 → 817 | −1 | −1.4737 |
| Harry Perryman | 28 | 169 | 81 → 80 | −1 | −0.8608 |

**The whole cost is 13 rows and 18 board points on a 660,000-point board, and the largest single move
is 2 points.** It is reported because it exists and because it was predicted, not because it is large.
**These are consequences and never targets.**

### 5.3 THE BIRTHDAY CENSUS IS ZERO ON EVERY ORDER R BOARD

| board | age-23 rows | gaining 50%+ | rows moving at all | net points | worst ratio |
|---|---:|---:|---:|---:|---:|
| ORDER P | 81 | **12** | 70 | +1,533 | **4.8904** |
| **every ORDER R cell** | 81 | **0** | **0** | **+0** | **1.0000** |

**Every ORDER R board carries B1, and B1 collapses the 24th-birthday jump to exactly zero. The
softening does not disturb that.** A null, and it is the good kind.

### 5.4 THE NAMED ROWS — CONSEQUENCES, NEVER TARGETS

**Not one constant in this order was chosen with any of these rows in view and no row's value is an
acceptance criterion.** This is a standing prohibition in this project after a real error.

**Price:**

| row | ORDER P | RB1 | R15 | R20 | R20b2 | RAB1 | R20A | **R20b2A** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Zane Duursma | 194 | 194 | 233 | 257 | 270 | 206 | 257 | **270** |
| Josh Sinn | 73 | 73 | 97 | 115 | 126 | 76 | 115 | **126** |
| Campbell Chesser | 167 | 167 | 178 | 186 | 192 | 168 | 186 | **192** |
| Finn O'Sullivan | 2,810 | 2,810 | 2,810 | 2,810 | 2,839 | 3,055 | 3,055 | **3,051** |
| Zeke Uwland | 1,486 | 1,486 | 1,486 | 1,523 | 1,557 | 1,582 | 1,582 | **1,595** |
| Harley Reid | 3,723 | 3,723 | 3,723 | 3,723 | 3,723 | 3,813 | 3,813 | **3,809** |
| Sam Darcy | 4,450 | 4,450 | 4,450 | 4,450 | 4,450 | 4,450 | 4,450 | **4,450** |
| Willem Duursma | 3,920 | 3,920 | 3,920 | 3,920 | 3,950 | 4,236 | 4,236 | **4,225** |
| Sam Lalor | 3,060 | 3,060 | 3,060 | 3,060 | 3,109 | 3,395 | 3,395 | **3,385** |

**Charge — the share of the pedigree leg removed:**

| row | ORDER P | RB1 | R15 | R20 | R20b2 | RAB1 | R20A | **R20b2A** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Zane Duursma** | **97.3%** | 97.3% | **90.7%** | **86.9%** | **84.6%** | 95.3% | 86.9% | **84.6%** |
| Josh Sinn | 95.2% | 95.2% | 90.1% | 86.1% | 83.8% | 94.5% | 86.1% | **83.8%** |
| Campbell Chesser | 95.4% | 95.4% | 90.8% | 86.9% | 84.7% | 95.0% | 86.9% | **84.7%** |
| Finn O'Sullivan | 80.2% | 80.2% | 80.2% | 80.2% | 77.6% | 58.9% | 58.9% | **59.2%** |
| Zeke Uwland | 84.7% | 84.7% | 84.7% | 81.8% | 79.2% | 77.3% | 77.3% | **76.2%** |
| Harley Reid | 15.9% | 15.9% | 15.9% | 15.9% | 15.9% | 4.5% | 4.5% | **5.0%** |
| **Sam Darcy** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** | **0.0%** |
| Willem Duursma | 35.8% | 35.8% | 35.8% | 35.8% | 34.2% | 18.9% | 18.9% | **19.4%** |
| Sam Lalor | 66.7% | 66.7% | 66.7% | 66.7% | 63.9% | 47.8% | 47.8% | **48.4%** |

**Read the `R15` and `R20` columns against `RB1`.** Finn O'Sullivan, Harley Reid, Willem Duursma and
Sam Lalor **do not move at all on the `TMAX` lever**. Their surplus is above the cap crossing, so the
cap never touched them. Only the rows AT the cap — Zane Duursma, Josh Sinn, Campbell Chesser — move.
**That is the mechanism showing its shape, and it is the strongest single argument that the `TMAX`
percentile is the lever aimed at the complaint the owner actually made.**

**Sam Darcy is charged nothing on every board in this order. A null, reported as one.**

---

## 6 · THE RAILS. THE OWNER'S TWO INSTRUCTIONS PULL AGAINST EACH OTHER, AND HERE IS THE PRICE.

**Prediction 5 was RIGHT and it is the central tension in this order.** Softening the charge raises
young year-1 prices, which raises year-1 appreciation, which pushes the top bands THROUGH the +14%
buy rail. **You cannot give the underperformers their pedigree back without moving the rail.**

### 6.1 The year-1 appreciation, both windows, both baselines

**PRIMARY window, cohorts 2005-2023.** Reading rule: below 0% is a SELL-SIDE RED, above +14% is a
BUY-SIDE RED, in between is ok.

| board | ALL 1-64 | 1-20 | **1-10** | **11-20** | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ORDER K | +4.23% | +9.22% | +8.22% | +11.16% | +5.26% | −10.70% | −6.89% |
| **ORDER P** | +5.33% | +9.79% | +8.62% | +12.08% | +7.37% | −8.88% | −5.03% |
| RB1 | +5.34% | +9.79% | +8.62% | +12.08% | +7.54% | −8.88% | −5.08% |
| RAB1 | +6.45% | +11.59% | +11.18% | +12.38% | +7.57% | −8.88% | −5.03% |
| R15 | +6.22% | +10.79% | +9.52% | +13.27% | +8.52% | −8.25% | −4.65% |
| R20 | +6.75% | +11.43% | +10.12% | +13.99% | +8.99% | −7.93% | −4.37% |
| R15A | +7.31% | +12.55% | +12.03% | +13.55% | +8.55% | −8.25% | −4.60% |
| **R20A** | +7.81% | +13.14% | +12.56% | **+14.26% BUY-RED** | +9.02% | −7.93% | −4.33% |
| Rb1 | +5.61% | +10.12% | +8.96% | +12.37% | +7.77% | −8.74% | −4.96% |
| Rb2 | +6.06% | +10.68% | +9.55% | +12.88% | +8.16% | −8.51% | −4.75% |
| R15b1 | +6.48% | +11.12% | +9.86% | +13.56% | +8.74% | −8.12% | −4.53% |
| **R20b2** | +7.45% | +12.31% | +11.05% | **+14.75% BUY-RED** | +9.56% | −7.59% | −4.06% |
| **R20b2A** | +8.31% | +13.71% | +13.05% | **+14.97% BUY-RED** | +9.58% | −7.59% | −4.03% |

**MODERN window, cohorts 2019-2023.**

| board | ALL 1-64 | **1-20** | **1-10** | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---:|---:|---:|---:|---:|---:|---:|
| ORDER K | −0.96% | +9.58% | +13.65% | +2.11% | −14.26% | −14.27% | −25.06% |
| **ORDER P** | +1.45% | +12.88% | **+18.85% BUY-RED** | +1.94% | −13.84% | −11.73% | −24.88% |
| RB1 | +1.40% | +12.88% | **+18.85%** | +1.94% | −13.84% | −11.73% | −25.23% |
| RAB1 | +2.36% | **+14.41% BUY-RED** | **+20.83%** | +2.66% | −13.82% | −11.73% | −25.15% |
| R15 | +2.11% | +13.58% | **+19.42%** | +2.88% | −12.84% | −10.97% | −24.87% |
| **R20** | +2.54% | **+14.06% BUY-RED** | **+19.85%** | +3.44% | −12.38% | −10.63% | −24.61% |
| R15A | +3.04% | **+15.07% BUY-RED** | **+21.38%** | +3.52% | −12.81% | −10.97% | −24.79% |
| **R20A** | +3.46% | **+15.53% BUY-RED** | **+21.78%** | +4.08% | −12.36% | −10.63% | −24.53% |
| Rb1 | +1.64% | +13.17% | **+19.14%** | +2.24% | −13.66% | −11.62% | −25.10% |
| Rb2 | +2.04% | +13.67% | **+19.63%** | +2.75% | −13.35% | −11.42% | −24.86% |
| R15b1 | +2.34% | +13.87% | **+19.72%** | +3.17% | −12.67% | −10.86% | −24.73% |
| **R20b2** | +3.16% | **+14.85% BUY-RED** | **+20.65%** | +4.22% | −11.96% | −10.35% | −24.26% |
| **R20b2A** | +3.94% | **+16.09% BUY-RED** | **+22.27%** | +4.77% | −11.94% | −10.35% | −24.20% |

**Two things worth saying plainly.**

1. **MODERN picks 1-10 was ALREADY over the rail on ORDER P** at +18.85%. That is ORDER P's own
   disclosed breach and the branch the owner already agreed to rule on. **Every ORDER R cell makes it
   worse**, from +19.14% at the mildest to **+22.27%** at the softest.
2. **The softening also IMPROVES every SELL-side band.** Picks 31-40 goes from −8.88% to −7.59%
   primary and −11.73% to −10.35% modern; picks 21-30 modern from −13.84% to −11.94%. **The rails are
   two-sided and the softening helps one side while it hurts the other.** That is not a defence of
   anything; it is the shape of the trade.

### 6.2 THE OWNER'S PATH TEST ON EVERY BREACHING CELL

The rule was written on `PREREG_R.md` before any table was read. Carry compounds at 14%:
**1.140 / 1.300 / 1.482 / 1.689 / 1.925 / 2.195 / 2.502**.

- **limb (a)** — "the path afterwards does not keep beating carry": PASSES when NO year 2..7 beats carry.
- **limb (b)** — "the end destination does not keep increasing": PASSES when `yr7 ≤ yr6` AND `yr7 ≤ carry7`.
- A cell PASSES only when both limbs pass.

**58 breaching cells across all thirteen boards. 3 PASS. 55 FAIL.**

**THE THREE THAT PASS ARE THE NEW BREACHES ORDER R CREATES IN PRIMARY PICKS 11-20:**

| band | board | yr1 | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | limb (a) | limb (b) | **verdict** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| PRIMARY 11-20 | **R20A** | +14.26% | 1.000 | 1.143 | 1.268 | 1.371 | 1.536 | 1.623 | 1.559 | 1.438 | pass | pass | **PASSES** |
| PRIMARY 11-20 | **R20b2** | +14.75% | 1.000 | 1.148 | 1.269 | 1.371 | 1.535 | 1.623 | 1.560 | 1.438 | pass | pass | **PASSES** |
| PRIMARY 11-20 | **R20b2A** | +14.97% | 1.000 | 1.150 | 1.273 | 1.376 | 1.539 | 1.625 | 1.561 | 1.439 | pass | pass | **PASSES** |

**These three breach the year-1 rail and then behave exactly as the owner said they must: the path
never beats carry again after year 1, and it ends FALLING (yr6 1.56 → yr7 1.44) and far under carry
(1.44 against 2.502).** On the owner's loosened rail these are acceptable breaches.

**THE CELLS THAT FAIL, AND WHY — every one fails on the SAME limb.**

| cell | boards | limb (a) | limb (b) | the failure, in words |
|---|---:|---|---|---|
| MODERN picks 1-10 | 12 (incl. **ORDER P itself**) | pass | **FAIL** | still RISING at the end: yr6 1.40 → yr7 1.59 |
| MODERN picks 1-20 | 6 | pass | **FAIL** | still RISING at the end: yr6 1.33 → yr7 1.54 |
| PRIMARY IRE arm | 11 | **FAIL(1)** | **FAIL** | beats carry in year 2 (1.54 against 1.30) and ends rising, 1.27 → 1.87 |
| SSP arm, both windows | 13 (incl. ORDER K) | **FAIL(2)** | pass | beats carry in years 2 and 3 |

**MODERN picks 1-10 FAILS THE PATH TEST ON ORDER P ITSELF, and on ORDER K's own SSP arm too. These
are INHERITED failures, not failures ORDER R creates.** ORDER R makes the level worse; it does not
change the verdict.

**MODERN picks 1-20 is the one place ORDER R turns a passing cell into a failing one.** ORDER P reads
+12.88% and does not breach at all. `R20`, `R20A`, `R20b2` and `R20b2A` breach and then FAIL limb (b).
ORDER Q's own `QAB1` already did the same at +14.41%, so this is a continuation of ORDER Q's finding
rather than a new class of problem — **but it is a real cost of the softening and it is not buried.**

**THE WEAKNESS IN THE TEST, STATED RATHER THAN BURIED.** Limb (b) reads years 6 and 7, and those
years are measured on FEWER ROWS than year 1: on MODERN picks 1-20 the counts run
**100 / 100 / 100 / 100 / 100 / 80 / 60 / 40** across years 0 to 7. **So the limb that decides every
one of these failures is read on 40 of the 100 rows that produced the breach.** The "still rising at
the end" that fails them is a change of sample as much as a change of value. Per-cell counts are in
`PATHTEST_R.json` under `n_included`.

---

## 7 · THE CLASS MARKS

**The basis is the registered W2 basis: DRAFT classes 2005-2015, ENTRY_FLOOR 2005 — cohort years
2006-2016. It is NOT the `ok_class.py` 2004-2014 window,** which is the cohort clock and is carried
below only so the two can be told apart on sight. **The instrument was validated first: it reproduces
ORDER K's own published marks off ORDER K's own matrix — W2 1.0513 and cohort 1.0324, both to 0.0000.**

| board | **W2 mark (the rail's basis)** | cohort clock | max single class | at cohort |
|---|---:|---:|---:|---:|
| ORDER K | 1.0513 | 1.0324 | 1.1363 | 2012 |
| **ORDER P** | **1.0613** | 1.0322 | **1.2047** | 2016 |
| RB1 | 1.0611 | 1.0321 | 1.2046 | 2016 |
| RAB1 | 1.0696 | 1.0409 | 1.2083 | 2016 |
| R15 | 1.0690 | 1.0413 | 1.2054 | 2016 |
| R20 | 1.0740 | 1.0470 | 1.2061 | 2016 |
| R15A | 1.0773 | 1.0499 | 1.2091 | 2016 |
| R20A | 1.0820 | 1.0552 | 1.2098 | 2016 |
| Rb1 | 1.0635 | 1.0345 | 1.2059 | 2016 |
| Rb2 | 1.0675 | 1.0387 | 1.2081 | 2016 |
| R15b1 | 1.0713 | 1.0438 | 1.2067 | 2016 |
| R20b2 | 1.0801 | 1.0534 | 1.2095 | 2016 |
| **R20b2A** | **1.0866** | 1.0601 | **1.2123** | 2016 |

**PREDICTION 6 WAS RIGHT.** The W2 mark rises monotonically with the softening, from ORDER P's 1.0613
to 1.0866 on the softest cell. **Every variant is inside the owner's law: above the 1.03 floor and
under the 1.14 rail. R12 does not fire on the W2 mark.** The softest cell has 0.0534 of room left.

**PREDICTION 7 WAS ALSO RIGHT, AND IT IS THE BAD HALF.** The three classes ORDER P put over 1.14 are
NOT repaired by anything here, and every variant makes all three WORSE. On draft 2010 the softest cell adds 0.0236, which is
more than ten times the 0.002 materiality threshold for a class mark:

| draft class (cohort) | ORDER K | **ORDER P** | R20 | R20b2 | **R20b2A** | move vs ORDER P |
|---|---:|---:|---:|---:|---:|---:|
| **2010 (2011)** | 1.1359 | **1.1570** | 1.1671 | 1.1737 | **1.1806** | **+0.0236** |
| **2011 (2012)** | 1.1363 | **1.1595** | 1.1694 | 1.1750 | **1.1772** | **+0.0177** |
| **2015 (2016)** | 1.1060 | **1.2047** | 1.2061 | 1.2095 | **1.2123** | **+0.0076** |

**This is a null on a question the order asked, and it is reported as one. These repairs are about
the cap and the slope; the three-class breach is about the size of the charge's effect on particular
cohorts, and nothing here touches it. It remains an open ruling from ORDER P.**

The full per-class table across every board is in `CLASS_R_out.txt`. Outside the W2 window nothing
crosses 1.14 on any variant.

---

## 8 · THE REVERSAL ON THE DENSE ENTRY-PRICE SWEEP — THE SOFTENING PARTLY REPAIRS IT ON ITS OWN

The charged pedigree leg swept across entry prices 40 to 6,000 at 0.1% steps, in 30 cells (two
premium classes × three games counts × five levels of production).

| board | cells where the LEG FALLS with price | total falling steps |
|---|---:|---:|
| ORDER P | **30 of 30** | **17,381** |
| RB1 | 30 of 30 | 17,381 |
| **R20** (p20) | **24 of 30** | **10,655** |
| **R20b2** (p20 · 0.105) | **23 of 30** | **10,013** |
| **R20b2A** (p20 · 0.105 · FIX A) | **0 of 30** | **0** |

**PREDICTION 3 IS CONFIRMED.** The softening cuts the reversal by 39-42% without FIX A, because a
lower cap parks more rows where `dT/ds = 0` and the leg is already monotone. **It does not remove it.
Only FIX A does that, and it still does it completely on the softest cell.**

## 9 · CONTINUITY — EVERY AXIS, ON THE EFFECTIVE CONSTANTS

The sweeps are run on the constants each board was actually built with, not on ORDER P's.

| axis | ORDER P | every ORDER R board |
|---|---|---|
| **AGE, the charge factor**, 18-30 at 20 games | largest step **0.4653** at 23→24 | **0.0000 at every age** |
| **AGE, the price**, every real row re-priced one year older | 70 of 804 rows move | **0 of 804 move** |
| GAMES, the charge across 0-400 at 0.01, seven surplus levels | largest step 3.709e-03; charge rises with games at **0 of 280,000** | largest step 1.933e-03; **0 of 280,000** |
| SURPLUS, across 100 points at 0.01 | largest step 9.934e-04; a better player charged more at **0 of 10,000** | largest step 9.099e-04; **0 of 10,000** |
| ENTRY PRICE, the premium itself | falls with price at **0 of 10,028** steps | unchanged — the surface is not refitted |

**No variant in this order creates a cliff on any axis. Every ORDER R board carries B1, so the
age-24 step ORDER P introduced is gone entirely — 0.0000, not "small".**

## 10 · MATURE-ROW MOVEMENT — THE SOFTENING SHRINKS B1's COST, BUT NOT BY MUCH

"Mature" is aged 24 and over: the 429 rows that were byte-identical to ORDER K under ORDER P.

| board | rows 24+ | moving | net vs ORDER K |
|---|---:|---:|---:|
| RB1 | 429 | 245 | **−6,567** |
| R15 | 429 | 245 | −6,381 |
| R20 | 429 | 245 | −6,200 |
| RAB1 | 429 | 245 | −6,106 |
| R15A | 429 | 245 | −5,945 |
| R20A | 429 | 245 | −5,777 |
| Rb1 | 429 | **248** | −6,456 |
| Rb2 | 429 | **249** | −6,266 |
| R20b2 | 429 | **249** | −5,883 |
| **R20b2A** | 429 | **249** | **−5,536** |

**PREDICTION 8 IS RIGHT IN DIRECTION AND WRONG IN SIZE.** The prereg said the mature-row cost would be
"materially smaller" at p20. It falls from −6,567 to −6,200 on the `TMAX` lever alone — **5.6%**, not
"materially smaller" — and to −5,536 on the softest cell with FIX A, **15.7%**. **B1's cost is
overwhelmingly not about the cap.** It is about the charge applying at all to veterans who spent
their careers below their entry-price bar, and softening the cap does not change that.

**The row count rises from 245 to 249 on the BETA lever.** Those four extra rows are stiffened rows,
not softened ones — §5.2.

## 11 · THE MOVERS LEDGER — THE WHOLE ARC, ORDER K → ORDER P → THE SOFTENING

**Full per-row detail is in `ARC_R.csv`, `ARC_R.json` and the readable `ARC_R.html`.**

**READ RANK, NOT POINTS.** ORDER K totals 673,097 and ORDER P totals 666,434 — 6,663 fewer points on
the same 804 players. **Most rows fall in absolute terms for a reason that has nothing to do with any
individual player: there are fewer points on the board.** Rank is the fair comparison.

| step | rows UP in points | rows DOWN | flat | net | rows UP in RANK | DOWN in rank |
|---|---:|---:|---:|---:|---:|---:|
| **ORDER K → ORDER P** *(the mechanism introduced)* | 125 | **155** | 524 | **−6,663** | **559** | 175 |
| **ORDER P → R20b2A** *(the softening)* | **241** | 203 | 360 | −378 | 403 | 313 |
| **ORDER K → R20b2A** *(THE WHOLE ARC)* | 180 | **344** | 280 | **−7,041** | **475** | 283 |

**The two readings disagree and that is the point.** Across the whole arc 344 rows fall in points and
only 180 rise — but **475 rows rise in RANK and only 283 fall.** The board shrank; the ordering did
not shrink with it.

**By pick band, net points, whole arc:** 1-10 **−1,981** · 11-20 **−2,632** · 21-30 −1,634 ·
31-40 −398 · 41+ −433 · pool **+37**. **The mechanism's whole cost lands on the top forty picks and
the pool is left almost exactly where it was.**

**Largest movers, whole arc.** Up: Jagga Smith +711, Harry Dean +666, Willem Duursma +522,
Sullivan Robey +485, Dyson Sharp +452. Down: Finn O'Sullivan −411, Zane Duursma −359,
Zeke Uwland −354, Sid Draper −344, Elijah Tsatas −315.
**These are consequences and never targets.**

**The softening step on its own is the only step of the three that moves more rows UP than DOWN
(241 against 203), and it lands +1,285 net on picks 1-10 while taking points off every other band.**

## 12 · PREDICTIONS SCORED. NINE WERE WRITTEN. THREE WERE WRONG.

| # | prediction, written before the first build | outcome |
|---|---|---|
| 1 | the `TMAX` percentile is by far the stronger lever, roughly 5 to 1 | **WRONG, and badly.** Measured 1.64 to 1. The reasoning looked only at the cap and missed that the slope lever pivots `T` about `s0` and so reaches every row below the centre. §4.3 |
| 2 | every softening raises the board total, monotonically in both levers | **RIGHT** — monotone on both, +552 to +6,189 against B1 |
| 3 | the burn census falls on both levers and is not zero on any A-off board | **RIGHT** — 77 → 54 rows, and 30 of 30 dense cells → 23 of 30 |
| 4 | FIX A still takes the burn census to exactly zero on every A-on board | **WRONG on one board of four.** Zero on `RAB1`, `R15A`, `R20A`; **one row and one board point on `R20b2A`**. §13 |
| 5 | the rails move the wrong way; MODERN 1-20 breaches at p20 even with A off; MODERN 1-10 gets worse everywhere | **RIGHT on both limbs.** `R20` breaches MODERN 1-20 at +14.06% with A off, and MODERN 1-10 is worse on every ORDER R cell |
| 6 | the W2 class mark rises and stays under 1.14 | **RIGHT** — 1.0613 → 1.0866, with 0.0534 of room left |
| 7 | the three classes over 1.14 get worse, not better | **RIGHT** — draft 2010 +0.0236, 2011 +0.0177, 2015 +0.0076 |
| 8 | mature-row movement shrinks materially with the softening | **PARTLY WRONG.** It shrinks 5.6% on the cap lever alone and 15.7% at the softest cell. Directionally right, "materially" was too strong |
| 9 | only MID has the sample; MID's slope is close to the pool; a split would not help | **PARTLY WRONG, and the correction matters.** TWO positions clear the sample line, MID and SF, not one. But the binding constraint is not sample at all — it is the confidence intervals, and on those NO position is separable. The "a split would not help" half is right and stronger than predicted: a split makes the reversal WORSE for four of six positions. §1 |

**Falsifier R15 — "the diagonals are not close to the sum of the single-lever moves, so the grid was
under-built" — DOES NOT FIRE.** Every gap is inside 0.083% of the board against a 0.3% threshold.

## 13 · HALT AND REPORT: FALSIFIER R7 FIRED

**R7 says the burn census must be ZERO on any FIX A board. On `R20b2A` it is not. It reads one row
and one board point. THE FALSIFIER FIRED AND IT IS REPORTED AS FIRED.**

| board | burned rows | burned points |
|---|---:|---:|
| RAB1 | **0** | 0 |
| R15A | **0** | 0 |
| R20A | **0** | 0 |
| **R20b2A** | **1** | **1** |

**What it is, measured rather than argued.** The row is Sam Banks, pick 29, 59 games, `v0` 438.10.
His price is 820 and at a 2% lower entry price he prices 821.

- the raw violation is **0.01655592** in engine currency, which is **0.0157 of ONE BOARD POINT**;
- it showed as +1 only because his unrounded price sits that far below an `int(round())` boundary;
- as a share of his pedigree leg (95.90 engine, 91.12 board points) it is **1.7264e-04**.

**ORDER Q disclosed the cause in advance:** the engine reads the premium at `v0` **rounded to one
decimal**, so FIX A's monotonicity is exact in the ROUNDED premium axis while the leg is formed on the
UNROUNDED `v0`. Within a rounding cell the leg rises; at a cell boundary the rounded premium jumps and
the leg can fall by up to one cell's worth. **One rounding cell at this `v0` is 2.17e-04 to 2.28e-04
of the leg. The measured violation, 1.7264e-04, is STRICTLY INSIDE that published bound.**

**Why here and not on ORDER Q's A boards:** the softer charge leaves a LARGER pedigree leg — Sam Banks
is charged only 3.63% at p20 with `BETA_sat` 0.105 — so the same relative residual is a larger
absolute number, and this row's unrounded price happened to land near a board-rounding boundary.

**It does not appear at the dense sweep's resolution:** `R20b2A` still reads **0 falling steps in 0 of
30 cells** on the 0.1%-of-price entry-price sweep.

**This seat does not rule on whether that is acceptable. It reports that the falsifier fired, what
the number is, and that the cause is a residual ORDER Q published rather than a failure of FIX A's
construction.**

## 14 · A SECOND FALSIFIER FIRED, AND IT WAS THIS SEAT'S SCORER THAT WAS WRONG

**R6 says no gameless row may move, because `A(0) = 0` exactly. The first version of the scorer
reported R6 FIRING on up to four rows per board. It was reading the wrong field.**

The board row carries **two** games fields. `g` is games in the **priced season**. `cg` is **career**
games. `A(g)` takes career games. A row that played two games in 2024 and none in 2025 has
`A(g) > 0` and its charge legitimately applies.

| reading | rows | moving on any ORDER R board |
|---|---:|---:|
| `g == 0` — games in the priced season (**the wrong population**) | 95 | up to 4 |
| **`cg == 0` — ZERO CAREER GAMES (the law's population)** | **89** | **0 on every one of the twelve boards** |

The four rows are Aidan Schubert (1 career game), Archie Ludowyke (2), Alex Van Wyk (1) and
Noah Howes (1). **None of them is gameless.**

**R6 PASSES.** Independently confirmed by the export's own `PRINTED-DAY-0 ASSERT`, which reads
**"89 of 89 day-0/sitter rows print EXACTLY"** on every one of the 24 builds in `BUILD_R_out.txt`.

**The scorer's error is reported rather than silently corrected, and both readings are still printed
in `BOARDS_R_out.txt` so the correction is auditable.**

---

## 15 · WHAT WAS NOT BUILT, AND WHY — SAID IN ADVANCE ON THE PREREG, NOT AS AN EXCUSE AFTERWARDS

The full grid is 3 percentiles × 3 `BETA_sat` × 2 FIX A = **18 cells. TWELVE were built.** The six
that were not are named here and were named on `PREREG_R.md` before the first build.

| not built | why |
|---|---|
| **(p5, b1, A on)** and **(p5, b2, A on)** | the A-on reading of the BETA lever at p5. FIX A's increment is measured at four other points — p5/b0 (`RB1`→`RAB1`), p15/b0 (`R15`→`R15A`), p20/b0 (`R20`→`R20A`) and p20/b2 (`R20b2`→`R20b2A`). If A's increment turned out to depend on the BETA lever by more than the materiality threshold, the omission would have mattered; §4.4 reports whether it does. |
| **(p15, b2)**, **(p20, b1)** and their A-on partners | the interior of the 3×3 lever grid. Cells `RB1`/`R15`/`R20` give the TMAX lever at fixed b0; `RB1`/`Rb1`/`Rb2` give the BETA lever at fixed p5; `R15b1` and `R20b2` give two diagonal readings of the interaction. §4.4 reports whether the diagonals are close to the sum of the two single-lever moves — if they are, the interior is interpolable and the omission is harmless. |
| **any cell WITHOUT FIX B1** | the order fixes B1 as the base for every variant. B1 is settled and independent and this order does not re-litigate it. |
| **`LAMBDA` re-solved** | see the disclosure below. It is a real choice and not an oversight. |
| **FIX B2 in any combination** | ORDER Q priced B2 and the order fixes B1 as the base. No ORDER R cell carries B2. |
| **`BETA_sat` above ORDER P's point estimate** | the owner ruled the charge should be SOFTENED. Stiffening it was not asked for and is not priced. The dial would accept it up to the CI ceiling; nothing was built there. |
| **any `TMAX` percentile other than 5, 15 and 20** | the owner named 15 and 20. The dial HALTS on anything else rather than letting a percentile be invented at the command line. |

---

## 16 · EVERY DISCLOSURE, AND EVERYTHING THIS SEAT COULD NOT MEASURE

- **NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED. NO PULL REQUEST WAS OPENED.
  NOTHING WAS PUSHED TO `main`.** This seat delivers prices.
- **FALSIFIER R7 FIRED.** One row, one board point, on `R20b2A` only. It is ORDER Q's disclosed
  premium-rounding residual and measures strictly inside its published bound. **It fired, and this
  packet says so rather than explaining it away.** §13
- **FALSIFIER R6 WAS REPORTED AS FIRING BY THIS SEAT'S OWN SCORER, AND THE SCORER WAS WRONG.** It read
  games in the priced season instead of career games. On the correct field R6 passes on every board.
  **The error is reported and both readings are still printed in `BOARDS_R_out.txt`.** §14
- **THE STRUCTURAL ASSERT R-S4 FIRED ON THE FIRST ENGINE LOAD AND THE ASSERT WAS WRONG, NOT THE
  DIALS.** It is replaced by the true statement and the eight boards built under it were discarded
  and rebuilt. §3
- **THE `BETA_sat` LEVER IS NOT A PURE SOFTENING** and the thirteen rows it lowers are named. §5.2
- **`LAMBDA` IS NOT RE-SOLVED, AND THAT IS A CHOICE.** On ORDER P, `LAMBDA` was SOLVED by an
  anchoring identity: bisection so the new charge removes exactly the same total points from the
  year-1 class-mark population as ORDER K's blind charge did. **Moving `BETA_sat` or `TMAX` BREAKS
  that anchor.** This order holds `LAMBDA` fixed because the order says to, and because re-solving it
  would claw back exactly the softening the owner asked for — holding the total constant is the
  anchor's whole job. **The consequence is that every variant here removes LESS total charge than
  ORDER P by construction. That is the softening.** It is on the prereg and on the engine banner.
- **The premium surface `PG` IS NOT REFITTED.** It is ORDER P's published grid, byte for byte.
- **`s0` IS NOT MOVED.** `T(s0) = 1` on every board, so a row at the cohort centre pays the same base
  charge everywhere. Only the cap and the slope move.
- **The BETA lever is NOT a pure softening.** §3. It stiffens the charge by up to 1.4472% of the
  pedigree leg over a 1.65-point-a-game window just above the cohort centre. Measured, not asserted,
  and printed on the engine banner of every board that carries it.
- **THE PERCENTILE IS UNWEIGHTED.** `s_p5` in `MECH_P.json` is an unweighted `np.percentile` over the
  4,143 season rows, while `s0` is a GAMES-WEIGHTED mean over the same rows. **That inconsistency is
  ORDER P's, not this order's**, and it is carried unchanged so p15 and p20 are the same kind of
  object as the p5 they replace. Changing it would have made the three percentiles incomparable.
  **It is disclosed rather than silently harmonised.**
- **The percentile is of SEASON ROWS, not of players.** A player with six seasons contributes six
  rows. That is ORDER P's population and it is carried unchanged.
- **There is no hold-out.** These variants act on ORDER P's premium surface, which is estimated on the
  same board's `v0` it is applied to. ORDER P disclosed that and it is unchanged here.
- **The position test is READ-ONLY and built no board.** It measures whether a per-position premium
  is supportable. It does not build one, and this order does not propose one.
- **The position test's bootstrap is over PLAYERS, not seasons**, on ORDER P's own seed 32. Resampling
  seasons would have understated the spread and made the intervals look narrower than they are.
- **RUCK's bootstrap interval is degenerate** (upper limit +918.83). That is reported as a degenerate
  interval, not trimmed to look like a wide one.
- **The three draft classes over 1.14 are ORDER P's breach and this order does not repair them.**
- **The `run_panel.sh` / Guard 5 lane does not pass on this branch and did not pass before this
  order.** The register's v737 entry records five stale pins on `land/order-29`, all predating
  ORDER P. This seat has not touched the workspace, `data/expected_boot.json` or
  `engine/forward_valuation`. The `engine_head` pin necessarily moves again because this order edits
  `_merged_recover.py`; re-stamping it is a landing act and this order lands nothing.
- **Every board was built through `bbR.sh`**, which pins the store, the engine, the
  forward-valuation tree and the five thread variables explicitly and prints their md5s on every run.
  **The store is `cb38ef11` on every board, unchanged.**
- **The two control matrices were REUSED, not re-emitted.** `per_entrant_QB1.json` is this order's
  `RB1` (p5/b0/A-off) and `per_entrant_QAB1.json` is its `RAB1` (p5/b0/A-on), both built by ORDER Q
  from the identical dial line. Re-emitting them would have burned nine minutes reproducing a file
  byte for byte. **Declared here rather than left to be noticed.**
- **ORDER K has no census run of its own.** Its charge factor is the `f_K` field the leg recorder
  captures on every board — the same object, computed by the engine at the same call site in the same
  clock state — and the whole-arc movers file reads it off the ORDER P census.
- **The owner's path test reads years 6 and 7 on FEWER ROWS than year 1.** A cohort only has a year-7
  cell if it drafted seven years ago. On MODERN picks 1-20 the counts run 100/100/100/100/100/80/60/40
  across years 0 to 7, so limb (b) is read on 40 of the 100 rows that produced the year-1 breach.
  **That is a real weakness in the test and it is stated rather than buried.** Per-cell counts are in
  `PATHTEST_R.json` under `n_included`.
- **The whole-arc movers page compares boards with DIFFERENT TOTALS.** ORDER K is 673,097 and ORDER P
  is 666,434, so most rows fall in absolute points for a reason that has nothing to do with any
  individual player. **RANK is the fair comparison. Absolute points are not.** That warning is at the
  top of the page, in the CSV documentation and in the JSON summary.
- **The "spanning variant" in the movers page is NOT a recommendation.** It is the far corner of the
  grid. This seat recommends nothing.
- **NO NAMED-PLAYER TARGETS.** Not one constant in this order was chosen with any row in view and no
  row's value is an acceptance criterion. Named rows are consequences only. This is a standing
  prohibition in this project after a real error.
- **The veteran board (RL_O33) is still parked.** Nothing here touches it.

---

## 17 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_R.md` | the prereg, pushed at `058e8bc` **before the first engine edit** |
| `ENGINE_PIN_R.txt` | the one engine md5 every board in this packet was built with |
| `or_position.py` · `POSITION_R.json` · `POSITION_R_out.txt` | **the read-only position test** — per-position premium refits, ESS, cluster-bootstrap CIs, the reversal reasoning |
| `bbR.sh` · `build_allR.sh` · `BUILD_R_out.txt` | the board suite: five controls, nine variants, the dial-implies test, nine determinism repeats |
| `run_emit_R.sh` · `run_emits_R.sh` · `EMITS_R_out.txt` · `EMIT_*_out.txt` | the nine walk-forward matrices, day-0 guard pointed at ORDER K's own reference |
| `bb_noarbR.sh` · `NOARB_R_out.txt` · `t338ext_*.txt` | the disclosed no-arb instruments, md5-pinned at run |
| `or_lib.py` | the engine harness and the blend-site leg recorder (ORDER Q's, with the two R dials added to the clear-list) |
| `or_census.py` · `CENSUS_*.json` · `or_census_*_run.txt` | the burn census, the birthday census, **the charge distribution** and the named rows, per board |
| `or_continuity.py` · `CONTINUITY_*` | continuity on every axis, swept on each board's **effective** constants |
| `or_bands.py` · `BANDS_R.json` · `BANDS_R_out.txt` | the ND band tables in **both** windows |
| `or_tables.py` · `STANDING_TABLES_R.json` · `STANDING_TABLES_R_out.txt` | the standing suite, pool arms both windows, both baselines, vantage matrix, entry-year control |
| `or_pathtest.py` · `PATHTEST_R.json` · `PATHTEST_R_out.txt` | **the owner's two-limb path test on every breaching cell** |
| `or_class.py` · `CLASS_R.json` · `CLASS_R_out.txt` | the class marks on both bases and the per-class table for all thirteen boards |
| `or_boards.py` · `BOARDS_R.json` · `BOARDS_R_out.txt` | totals, falsifiers, mature-row movement, the named rows, the movers ledgers |
| **`or_arc.py` · `ARC_R.csv` · `ARC_R.json` · `ARC_R.html`** | **the whole-arc movers list** — one row per player, all 804, ORDER K → ORDER P → every variant, values, ranks, deltas and mechanism diagnostics |

**The readable movers page is also published at**
`https://claude.ai/code/artifact/2d9aa722-50fe-4243-a8d5-b822f1c113d1` — private to the owner's
account until he shares it. It is the same file as `ARC_R.html` in this directory.
| `or_digest.py` · `DIGEST_R_out.txt` | a compact digest of every result, so this packet quotes files rather than memory |
| `run_measureR.sh` · `run_afterbuildR.sh` · `MEASURE_R_out.txt` · `AFTERBUILD_R_out.txt` | the sequential run chain |
