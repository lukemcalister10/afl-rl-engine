# PACKET Q — THREE REPAIRS TO THE ORDER P CHARGE, PRICED

**Seat:** ORDER Q. **Date:** 2026-08-18. **Branch:** `land/order-29`.
**Prereg:** `PREREG_Q.md`, pushed at `df02eaa` before the first engine edit.

**THIS IS A MEASUREMENT ORDER. NOTHING IS ADOPTED. NOTHING LANDS. NO VARIANT IS RECOMMENDED.**
This packet is numbers. The choice is the owner's and the supervisor's.

**Boards.** live `88ce647f` 752,429 (never touched) · landing candidate `1f176444` 667,916 ·
ORDER K `f3101883` 673,097 · **ORDER P `374d4e44` 666,434 — the base for this order** ·
uncharged `73bf9617` 702,734.

**Pins.** store `cb38ef11` (unchanged) · engine `_merged_recover.py` before this order `7df6a923` ·
`rl_model.py` before this order `e1076eff`.

---

## 1 · STEP 0 FIRST — THE SUPERVISOR'S ARITHMETIC IS RIGHT

**The order told this seat to check the supervisor before using anything he wrote. It has been
checked against the engine's own internals, and it holds.**

His census of both defects rests on an inference: for each young row he took the ORDER K and ORDER P
prices and the two charge factors, and inferred the charged pedigree leg as
`ped_P = (P_K - P_P) * fP / (fK - fP)`, treating the production leg and `pi_base` as independent of
entry price.

### 1.1 What was measured, and how

The engine was instrumented with a recorder on the blend site. The recorder READS and delegates; it
changes no arithmetic. It captures, at the exact moment each price is formed, the production input
`e`, and then reads the engine's own `rho31`, `o31_pi`, `pv_pedigree`, `o32_age_credit` and
`o37_factor` in the same clock state.

**The decomposition is the engine's own, and it is exact.**

| check | result |
|---|---|
| `price = rho31(g)*e + pi*pv_pedigree + o32_age_credit` reproduces `ev()` | **worst error 9.1e-13 on 804 of 804 rows** |
| the in-process engine reproduces the built board `374d4e44` | **0 of 804 rows disagree** |

### 1.2 One thing he could not have seen from board prices, and it did not bite

**396 of 804 rows reach the blend TWICE at the same year.** That is the M3 proportional-tenure blend
(`_ev_m3`): the engine prices the row on the full clock and again on a PINNED clock and returns
`w*click + (1-w)*pin`. A row priced that way has two charge factors, not one, so "the row's charge
factor" is not obviously well defined.

**It turns out to be well defined anyway.** On the 268 selected young rows, 158 are M3 rows, and the
worst gap between a row's two ORDER P charge factors is **0.0000**, and between its two ORDER K
factors **0.0000**. The clock pin does not move `pv_games` for these rows, so both calls see the same
games and the same surplus. **A single factor per row is correct. This is reported because it was a
real risk to his arithmetic and it had to be ruled out rather than assumed.**

### 1.3 The identity: exact algebra, with board rounding on top

| quantity | result |
|---|---|
| board `(P_K - P_P)` against the engine's exact pedigree-leg difference | max **0.9234**, mean **0.2950** |
| — which is pure board rounding: each price is `int(round(ev/F))`, so up to 1.0 of slack | |
| inferred `ped_P` against the TRUE engine leg, points | max **25.1**, mean **1.62**, median **0.54** |
| the same, as a share of the true leg | max **100.00%**, mean **2.14%**, median **0.53%** |
| rows off by more than 2% of the leg | **66 of 268** |
| rows off by more than one board point | **98 of 268** |

**The algebra is right and the practice carries rounding noise.** `fP/(fK - fP)` is an amplifier: at
his own `|fK - fP| >= 0.02` filter it multiplies a rounding error of up to 1.0 board point by up to
50. The worst case is Will Ashcroft, whose true leg is 393.1 and whose inferred leg is 368.0, off by
6.4%. On a row whose true leg is small the error can be the whole leg — Jase Burgoyne's true leg is
23.5 and the inference reads -0.0.

**This does not change any of his verdicts.** The census asks whether a 2% step in entry price moves
the price, and 2% of a large leg is far larger than the rounding noise. That is measured next, not
argued.

### 1.4 The assumption this seat named in advance as the risk — it holds EXACTLY

The prereg named one channel that could have broken his sweep: `ev()`'s staleness and decay gates cap
the production leg at `v0_start(p) * frac`, and `v0_start` is a function of the row's entry value.
If that cap binds on a young row, the production leg is not independent of entry price for that row.

**It binds on none of them.**

> Worst spread of (production leg + age credit) across a row's whole entry-price sweep:
> **0.0000e+00**. Rows where it moves at all: **0 of 289**.

That is measured by re-pricing every young row through the full engine at every step of the sweep,
not by reading the code.

### 1.5 The burn census, re-run INSIDE the engine

`day0_v0` is the single accessor for a row's entry price. It feeds exactly three places: the pedigree
leg, the day-0 print predicate, and the ORDER P premium axis. It was wrapped for one row at a time
and the row was re-priced by the engine's own `ev()`. **The wrapper is proved inert: at scale 1.0
every one of 804 rows reprices BIT-IDENTICALLY.**

| band | HIS burned / n | **THIS SEAT burned / n** | his points | **this seat, points** |
|---|---:|---:|---:|---:|
| picks 1-10 | 24 / 43 | **24 / 43** | 1,815 | **1,820** |
| picks 11-20 | 13 / 44 | **13 / 44** | — | **292** |
| picks 21-30 | 12 / 35 | **11 / 35** | — | **38** |
| picks 31-40 | 4 / 28 | **4 / 28** | — | **28** |
| picks 41+ | 13 / 52 | **13 / 51** | — | **60** |
| pool | 10 / 65 | **12 / 67** | — | **70** |
| **TOTAL** | **76 / 267** | **77 / 268** | **2,323** | **2,308** |

**Named rows, his against the engine's own sweep:**

| row | his | **measured here** |
|---|---|---|
| Sam Lalor, pick 1 | 3,061 -> 3,395 (+334) | **3,060 -> 3,395 (+335)** |
| Willem Duursma, pick 1 | 3,920 -> 4,225 | **3,920 -> 4,226** |
| Finn O'Sullivan, pick 2 | 2,810 -> 3,055 | **2,810 -> 3,054** |
| Harley Reid, pick 1 | 3,724 -> 3,805 | see below |

Harley Reid's ORDER P board price is 3,723, not 3,724, and he does not appear in this seat's worst
five; Sam Cumming (+142) and Harvey Langford (+113) do. That is a difference in the tail of a list,
not in the census.

**The differences are one row in the total, three rows in the band splits, and 15 points in 2,323.
They come from the rounding described in 1.3 and from two rows sitting on the `|fK - fP| >= 0.02`
boundary. THE CENSUS IS CONFIRMED.**

### 1.6 The birthday census, re-run

**First, the definition was checked rather than assumed.** Under ORDER P the age gate hands the whole
charge back at 24, so a row's price on his 24th birthday, with games and output unchanged, IS his
ORDER K price. Verified on the built boards: Josh Sinn reads 73 on `374d4e44` and 357 on `f3101883`,
a ratio of 4.890 — exactly the supervisor's number.

| quantity | his | **measured here** |
|---|---:|---:|
| age-23 rows with a pedigree leg | 81 | **81** |
| rows gaining 50% or more from the birthday alone | 12 | **12** |
| points handed back, gains only | 2,271 | **+2,271** |
| points handed back, NET of the rows that fall | — | **+1,533** |
| rows that move at all | — | **70 of 81** |
| worst ratio | 4.89 (Josh Sinn) | **4.8904 (Josh Sinn), 73 -> 357** |

James Tunstill 42 -> 176 (4.190x) matches. Campbell Chesser 167 -> 333 (1.994x) matches.

**Both readings of the total are printed because they are different objects.** The birthday RAISES 
some rows and LOWERS others. His 2,271 is the gains-only figure and it is exactly right.

### 1.7 THE STEP 0 VERDICT

**The supervisor's arithmetic is correct.** His inference is exact algebra; the assumption he made
about the production leg is exactly true; the census reproduces from engine internals to within one
row and 15 points; the birthday census reproduces exactly. The one qualification is that his inferred
per-row LEG carries board-rounding noise of up to 25 points, which matters if anyone quotes a
particular row's leg and does not matter to either census.

**Everything below stands on measured internals, not on that inference.**

---
