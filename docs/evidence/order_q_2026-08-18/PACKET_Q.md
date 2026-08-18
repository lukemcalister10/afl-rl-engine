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

## 2 · WHAT WAS BUILT

Three repairs, each behind its own dial. The dials are independent, so the two combinations are just
two dials on at once. `RL_O38B1` and `RL_O38B2` are alternatives and setting both HALTS at load.

| dial | repair |
|---|---|
| `RL_O38A` | **FIX A** — the pedigree leg is monotonised in ENTRY PRICE |
| `RL_O38B1` | **FIX B1** — the age-24 gate is DELETED |
| `RL_O38B2` | **FIX B2** — the charge is RAMPED OUT across ages 23 to 26 |

### 2.1 FIX A, and why it has no free parameter

Write `x = ln(v0)` in engine currency. The charged pedigree leg is proportional to `exp(psi(x))`
where

    psi(x) = x - LAMBDA * A(g) * T( OUT - wTALL*PG(x,TALL) - wSMALL*PG(x,SMALL) )

`OUT` is the row's games-weighted production above his AGE bar. It does not move with price. The
whole of the price dependence is in `PG`.

The repair takes the RUNNING MAXIMUM from the left:

    psi_A(x) = max over u <= x of psi(u)          factor = exp( psi_A(x) - x )

Three things follow by construction, and all three are asserted at load and measured on the boards:

1. `exp(psi_A)` is non-decreasing in `x`, so **no lower entry price can price higher**.
2. `psi_A >= psi`, so the charge is only ever CAPPED. **A price can only move UP against ORDER P.**
3. `psi(u) <= u` for every `u <= x`, so the factor stays in `(0,1]` and **no row can price above its
   own uncharged price**.

Nothing is tuned. There is no constant to choose. The precedent is the ISO multiplier, which this
engine already monotonises isotonically over pick; this does the same thing over entry price.

**It is computed exactly, not on a grid.** `PG` is piecewise linear on its published nodes and `T` is
piecewise linear in `s` with two clip breakpoints, so `psi` is piecewise linear in `x` and its maximum
sits at a breakpoint. The candidate set is the premium grid nodes of both classes below `x`, the clip
crossings inside each segment, and `x` itself.

**ONE DISCLOSED RESIDUAL, MEASURED NOT ASSERTED.** The engine reads the premium at `v0` rounded to
one decimal, so the true function is a staircase with steps of 0.1 in engine currency. Monotonicity
holds up to one rounding cell, not to the last bit. In log terms the residual is bounded by about
3e-5 of the leg at `v0` 3,000 — well under one board point. The dense continuity sweep below reads
**0 falling steps in 30 of 30 cells**, so it does not show up at that resolution either.

### 2.2 FIX B1

The `>= O37_AGE_GATE` early return is removed. The charge runs at every age on the same bar. From 24
the S1 age bar already equals the flat bar by construction, so a mature row is judged against the
flat bar plus the measured premium. No phase-out, no new parameter.

**The known cost, measured in §6: mature rows are no longer byte-identical to ORDER K.**

### 2.3 FIX B2, and the parameter this seat invented

    ln f = w(age) * ln f_P + (1 - w(age)) * ln f_K
    w = 1 at 23 and below, 2/3 at 24, 1/3 at 25, 0 at 26 and above

**THE ENDPOINT 26 IS A FREE PARAMETER. THIS SEAT INVENTED IT. IT WAS NOT MEASURED.** It is never
described as derived and nothing in the measurement chose it.

**A second disclosure.** Age in this engine is the integer `int(Y) - int(birth year)`. There is no
finer resolution. So B2 does not remove the step. It replaces one step of full size with three steps
of about a third the size. That is what a ramp can be on an integer axis, and §7 shows exactly what
it does to the count of rows that jump.

---

## 3 · THE BUILD-LEVEL FALSIFIERS. ALL PASSED.

| # | falsifier | result |
|---|---|---|
| **Q1** | all three new dials unset does not rebuild ORDER P `374d4e44` byte-exact | **no — `374d4e44`** |
| **Q2** | determinism x2 on any variant | **no — all five identical on a repeat** |
| **Q3** | `RL_O38A` alone does not carry the O37/O36/O35/O32/O31 stack | **no — `d7aad579` both ways** |
| **Q4** | the base stack no longer rebuilds `1f176444` | **no — `1f176444`** |
| **Q5** | ORDER K's ruled line no longer rebuilds `f3101883` | **no — `f3101883`** |
| **Q6** | **FIX A's burn census is not ZERO** | **no — 0 of 268, 0 points, every band** |
| **Q7** | FIX A lowers any row's price | **no — 0 rows down, on all three A boards** |
| **Q8** | any variant prices a row above its own uncharged price | **no — 0 of 804, every variant** |
| **Q9** | any gameless row or day-0 print moves | **no — 0 of 95 rows; day-0 89 of 89 exact on every emit** |
| **Q10** | under B2 a row aged 26+ is not byte-identical to ORDER K | **no — 0 of 320 move** |

**The boards.**

| board | md5 | total | vs ORDER P | vs ORDER K |
|---|---|---:|---:|---:|
| base stack (landing candidate) | `1f176444` | 667,916 | +1,482 | −5,181 |
| ORDER K | `f3101883` | 673,097 | +6,663 | — |
| ORDER P (all Q dials off) | `374d4e44` | 666,434 | — | −6,663 |
| **FIX A** | **`d7aad579`** | **668,791** | **+2,357** | −4,306 |
| **FIX B1** | **`1b1817f3`** | **659,867** | **−6,567** | −13,230 |
| **FIX B2** | **`96708014`** | **663,570** | **−2,864** | −9,527 |
| **A + B1** | **`cbbb94d4`** | **662,685** | **−3,749** | −10,412 |
| **A + B2** | **`d9607467`** | **666,093** | **−341** | −7,004 |
| uncharged ceiling (ORDER P's own) | `73bf9617` | 702,734 | +36,300 | +29,637 |

**The engine `_merged_recover.py` and `rl_model.py` both move in this order, so their md5s move with
them.** Every board was built through `bbQ.sh`, which pins the store, the engine, the
forward-valuation tree and the five thread variables explicitly and prints their md5s on every run.
The store is `cb38ef11` on every board, unchanged.

---

## 4 · THE BURN CENSUS RE-RUN. FIX A TAKES IT TO ZERO.

The population is the supervisor's: young ND+pool rows, age under 24, games above 0, and
`|fK - fP| >= 0.02` **on ORDER P's own factors**, so the same 268 rows are censused under every
variant and the bands are comparable across the table.

| band | n | ORDER P | **FIX A** | FIX B1 | FIX B2 | **A+B1** | **A+B2** |
|---|---:|---:|---:|---:|---:|---:|---:|
| picks 1-10 | 43 | 24 | **0** | 24 | 24 | **0** | **0** |
| picks 11-20 | 44 | 13 | **0** | 13 | 13 | **0** | **0** |
| picks 21-30 | 35 | 11 | **0** | 11 | 11 | **0** | **0** |
| picks 31-40 | 28 | 4 | **0** | 4 | 4 | **0** | **0** |
| picks 41+ | 51 | 13 | **0** | 13 | 13 | **0** | **0** |
| pool | 67 | 12 | **0** | 12 | 12 | **0** | **0** |
| **TOTAL rows burned** | **268** | **77** | **0** | **77** | **77** | **0** | **0** |
| **TOTAL points burned** | | **2,308** | **0** | **2,308** | **2,308** | **0** | **0** |

**B1 and B2 leave the burn exactly where it was.** They are repairs to the age axis and they do not
touch the price axis. That is not a fault of theirs; it is the reason the two defects need two
repairs.

**FIX A moves exactly the rows it was burning and no others.** Against ORDER P, FIX A moves 77 rows,
all of them up, and that is the same 77 the census was reading. The 191 unburned rows in the census
population are byte-identical to ORDER P.

---

## 5 · THE BIRTHDAY CENSUS RE-RUN

**Two objects are reported and they are different questions.**

### 5.1 The 23-to-24 birthday, which is where ORDER P's cliff is

| quantity | ORDER P | FIX A | **FIX B1** | **FIX B2** | **A+B1** | **A+B2** |
|---|---:|---:|---:|---:|---:|---:|
| age-23 rows with a pedigree leg | 81 | 81 | 81 | 81 | 81 | 81 |
| rows gaining 50%+ from the birthday alone | 12 | 12 | **0** | **0** | **0** | **0** |
| rows that move at all | 70 | 70 | **0** | 67 | **0** | 66 |
| points handed back, gains only | +2,271 | +2,161 | **+0** | **+430** | **+0** | **+419** |
| points handed back, net | +1,533 | +1,388 | **+0** | **+150** | **+0** | **+125** |
| worst ratio | **4.890x** | 4.697x | **1.000x** | **1.425x** | **1.000x** | **1.434x** |

**B1 collapses it to EXACTLY ZERO.** Not "small" — zero. The reason is structural and worth stating
plainly: `s_P` is a games-weighted average over the seasons a player has PLAYED, each judged against
the bar for the age he was IN THAT SEASON. It never reads his current age. Once the gate is gone, the
charge does not read current age at all, so a birthday cannot move a price.

**B2 collapses the 50%-gainers to zero and cuts the worst jump from 4.89x to 1.43x**, which is what a
three-step ramp can do.

**FIX A barely touches it**, as it should: A repairs the price axis, not the age axis.

### 5.2 EVERY birthday, not just the 23rd — and this is where B2 pays

The order asked for the age axis across 23/24. This seat swept EVERY age. **B2 does not remove the
50%-gain birthdays. It moves them one and two years later.**

| variant | rows that move on ANY birthday | rows gaining 50%+ on ANY birthday | where | worst jump | net points |
|---|---:|---:|---|---:|---:|
| ORDER P | 70 | **12** | all at 23->24 | 4.890x | +1,533 |
| FIX A | 70 | **12** | all at 23->24 | 4.697x | +1,388 |
| **FIX B1** | **0** | **0** | nowhere | **1.000x** | **+0** |
| **FIX B2** | **148** | **16** | 7 at 24->25, 9 at 25->26 | **2.368x** | +1,738 |
| **A+B1** | **0** | **0** | nowhere | **1.000x** | **+0** |
| **A+B2** | 147 | 16 | 7 at 24->25, 9 at 25->26 | 2.368x | +1,632 |

**B2's trade, stated plainly: it more than doubles the number of rows whose price moves on a birthday
(70 to 148) and raises the net points handed across birthdays (+1,533 to +1,738), in exchange for
cutting the worst single jump in half (4.89x to 2.37x).** It does not dominate ORDER P on every
reading of the defect and this packet does not present it as if it did.

**B1 is the only variant on which no row's price moves on any birthday.**

---

## 6 · MATURE-ROW MOVEMENT — AND THE ORDER'S OWN EXPECTATION IS WRONG ON ONE POINT

**The order expects zero mature-row movement under A and B2 and non-zero under B1. A and B1 come out
as expected. B2 does NOT.** This was written down in the prereg before the first build:

> "This seat expects NON-ZERO movement at ages 24 and 25, because the ramp puts a partial ORDER P
> charge on exactly those ages."

**That is what happened.** "Mature" means aged 24 and over at the year priced — the 429 rows that
have been byte-identical to ORDER K since ORDER P.

| variant | rows 24+ | of which move | net vs ORDER K |
|---|---:|---:|---:|
| **FIX A** | 429 | **0** | **+0** — as the order expected |
| **FIX B1** | 429 | **245** | **−6,567** — as the order expected |
| **FIX B2** | 429 | **84** | **−2,864** — the order expected zero |
| **A + B1** | 429 | **245** | **−6,106** |
| **A + B2** | 429 | **84** | **−2,698** |

**Where B2's movement sits, exactly.** All of it is at ages 24 and 25. Rows aged 26 and over are
byte-identical to ORDER K, 0 of 320. **That is the ramp working as designed, not a fault — but the
order's phrase "keeps mature rows still" is not true of it, and this packet will not pretend
otherwise.**

**The full age table, net points against ORDER K.** The young rows are shown too, so the whole board
is visible rather than only the part the question was about.

| age | n | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 |
|---:|---:|---:|---:|---:|---:|---:|
| 19 | 71 | +1,648 | +1,009 | +1,009 | +1,648 | +1,648 |
| 20 | 87 | −945 | −1,894 | −1,894 | −945 | −945 |
| 21 | 75 | −1,273 | −1,510 | −1,510 | −1,273 | −1,273 |
| 22 | 61 | −2,348 | −2,735 | −2,735 | −2,348 | −2,348 |
| 23 | 81 | −1,388 | −1,533 | −1,533 | −1,388 | −1,388 |
| **24** | 58 | **+0** | **−2,420** | **−2,011** | **−2,288** | **−1,890** |
| **25** | 51 | **+0** | **−1,667** | **−853** | **−1,619** | **−808** |
| 26 | 55 | +0 | −699 | **+0** | −633 | **+0** |
| 27 | 46 | +0 | −770 | +0 | −720 | +0 |
| 28 | 57 | +0 | −589 | +0 | −488 | +0 |
| 29 | 40 | +0 | −146 | +0 | −108 | +0 |
| 30 | 33 | +0 | −84 | +0 | −76 | +0 |
| 31 | 24 | +0 | −38 | +0 | −38 | +0 |
| 32 | 19 | +0 | −31 | +0 | −24 | +0 |
| 33 | 22 | +0 | −112 | +0 | −103 | +0 |
| 34 | 11 | +0 | −8 | +0 | −6 | +0 |
| 35 | 5 | +0 | −3 | +0 | −3 | +0 |
| 36-39 | 8 | +0 | +0 | +0 | +0 | +0 |

**Why B1 costs so much.** ORDER K's blind charge decays to essentially nothing past 14 games:
at 250 career games it removes under a millionth of the pedigree leg. The ORDER P charge does not
decay — `A(g)` rises to 1 and stays there — so a veteran who has spent his career below the bar his
entry price implies now pays close to the full rate. **6,567 points, 245 of 429 rows, mostly down.**
That is the price of B1 and it is the largest single number in this order.

**The rows it lands on hardest, under B1, against ORDER P:** Jamarra Ugle-Hagan 534 -> 297 (−237),
Conor Stone 218 -> 17 (−201), Paddy Dow 206 -> 10 (−196), Luke Pedlar 217 -> 43 (−174), Dylan
Stephens 687 -> 515 (−172). **These are consequences and not targets. No row's value is an acceptance
criterion in this order.**

**Where FIX A's money goes, by career games, against ORDER P.** It is concentrated where evidence is
thin enough that the pedigree leg still matters and games are high enough that `A(g)` bites.

| career games | rows | net | per row |
|---|---:|---:|---:|
| 0 | 95 | +0 | +0.0 |
| 1-4 | 48 | +1 | +0.0 |
| 5-9 | 53 | +35 | +0.7 |
| 10-15 | 48 | +283 | +5.9 |
| **16-29** | 79 | **+1,060** | **+13.4** |
| 30-59 | 99 | +707 | +7.1 |
| 60+ | 382 | +271 | +0.7 |

---

## 7 · CONTINUITY — INCLUDING THE AXIS ORDER P DID NOT TEST

### 7.1 Q14, CONFIRMED: the age axis of the CHARGE was never tested

**ORDER P's continuity suite has an AGE axis. It is not this axis.** `op_continuity.py` sweeps
`MA.o36_bar(pos, age)` — the S1 age BAR — and its own header says of it: *"the S1 age bar, ages
18..30, every position. UNCHANGED by this order; re-asserted."* It never sweeps `o37_factor` across
age and it never sweeps a row's price across age. **The age-24 handover ORDER P introduced was never
tested by ORDER P's own suite. The omission is real.**

Here is the axis it left out. The charge factor at 20 career games, ages 18 to 30. The factor is what
multiplies the pedigree leg; 1.000 means no charge at all.

**ORDER P (and FIX A, which does not touch this axis) — one step, and it is large:**

| s_P | 18-23 | **24** | 25-30 |
|---:|---:|---:|---:|
| −25.0 | 0.0913 | **0.5347** | 0.5347 |
| −10.0 | 0.4057 | **0.5347** | 0.5347 |
| −3.0 | 0.8140 | **0.5347** | 0.5347 |
| 0.0 | 1.0000 | **0.5347** | 0.5347 |

**Largest step between two consecutive ages: 0.4653.** And note the direction flips with the row's
own surplus: a player 25 points a game below his pedigree bar is charged LESS on his birthday
(0.0913 -> 0.5347), while a player exactly at his bar is charged MORE (1.0000 -> 0.5347). **The
handover does not even push one way.**

**FIX B1 — the step is gone entirely:**

| s_P | 18 to 30 |
|---:|---:|
| −25.0 | 0.0913 at every age |
| −10.0 | 0.4057 at every age |
| −3.0 | 0.8140 at every age |
| 0.0 | 1.0000 at every age |

**Largest step: 0.0000. The charge does not read current age at all.**

**FIX B2 — one step of 0.4653 becomes three smaller ones:**

| s_P | 23 | 24 | 25 | 26+ |
|---:|---:|---:|---:|---:|
| −25.0 | 0.0913 | 0.1645 | 0.2966 | 0.5347 |
| −10.0 | 0.4057 | 0.4448 | 0.4877 | 0.5347 |
| −3.0 | 0.8140 | 0.7076 | 0.6151 | 0.5347 |
| 0.0 | 1.0000 | 0.8116 | 0.6588 | 0.5347 |

**Largest step: 0.2381** (at 25->26, s_P −25). The biggest step is about half ORDER P's, and there are
three of them instead of one.

### 7.2 THE ENTRY-PRICE AXIS — DEFECT 1, MEASURED DENSELY

The charged pedigree leg swept across entry prices 40 to 6,000 at 0.1% steps, in 30 cells (two
position classes x three games counts x five levels of production).

| board | cells where the LEG FALLS with price | total falling steps | worst single fall |
|---|---:|---:|---:|
| ORDER P | **30 of 30** | **17,381** | 5.658e-03 of the leg (TALL, g=60, at v0 2,779) |
| **FIX A** | **0 of 30** | **0** | **NONE** |
| FIX B1 | 30 of 30 | 17,381 | 5.658e-03 |
| FIX B2 | 30 of 30 | 17,381 | 5.658e-03 |
| **A + B1** | **0 of 30** | **0** | **NONE** |
| **A + B2** | **0 of 30** | **0** | **NONE** |

**The defect is board-wide on ORDER P, exactly as the order said, and FIX A removes it completely at
this resolution.** The disclosed one-decimal rounding residual does not show up here.

### 7.3 The axes ORDER P did test — all unchanged on every variant

| axis | result, identical on all six boards |
|---|---|
| GAMES — the charge across 0 to 400 at 0.01, seven surplus levels | largest step **3.709e-03**; the charge RISES with games at **0 of 280,000** steps |
| SURPLUS — the charge across 100 points of surplus at 0.01 | largest step **9.934e-04**; a better player is charged more at **0 of 10,000** steps |
| ENTRY PRICE — the premium itself | falls with price at **0 of 10,028** steps; largest one-node move 0.0570 |

**No repair in this order creates a cliff on any axis, and FIX A removes one.**

---

## 8 · THE FULL NO-ARB TABLES, IN THE STANDING FORMAT

Reading rule, in plain words. A group is fairly priced if it appreciates between 0% and +14% over its
first year. Below 0% is a SELL-SIDE RED: you could sell at draft day, buy back a year later and keep
the difference. Above +14% is a BUY-SIDE RED: you could buy at draft day and beat the cost of
carrying him. The buy margin is how much room is left before the buy rail.

**Instrument pins, computed at run and unmodified by this order:** `t338_extended_DISCLOSED.py`
`d59ad5501…` (required `d59ad550116ebbe3d90ed82becd2c4d5`), `noarb_table_338.py` `0f822035…`
(required `0f8220351c64c56ccfa90c60edcdfa5f`), `harness_pvc_REPINNED_pass3.py` `02dcf28c…`.
The band tables in both windows come from `oq_bands.py`, which is ORDER L's `ol_bands.py` re-pointed
at these seven matrices with the population filter and the byte-carried `value_at()` unchanged.

**TWO NEW BREACHES ARE IN THESE TABLES. They are called out in §9 and they are not hidden here.**

### PRIMARY window, cohorts 2005-2023

**ALL picks 1-64** — n = 1200

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.042 | 1.176 | 1.364 | 1.498 | 1.532 | 1.492 | 1.320 | +4.23% | +9.77% | ok |
| ORDER P | 1.000 | 1.053 | 1.172 | 1.339 | 1.462 | 1.501 | 1.491 | 1.320 | +5.33% | +8.67% | ok |
| FIX A | 1.000 | 1.064 | 1.185 | 1.349 | 1.470 | 1.505 | 1.491 | 1.320 | +6.44% | +7.56% | ok |
| FIX B1 | 1.000 | 1.053 | 1.172 | 1.339 | 1.462 | 1.500 | 1.466 | 1.302 | +5.34% | +8.66% | ok |
| FIX B2 | 1.000 | 1.053 | 1.172 | 1.339 | 1.462 | 1.500 | 1.471 | 1.311 | +5.34% | +8.66% | ok |
| A+B1 | 1.000 | 1.065 | 1.185 | 1.349 | 1.469 | 1.504 | 1.469 | 1.304 | +6.45% | +7.55% | ok |
| A+B2 | 1.000 | 1.064 | 1.185 | 1.349 | 1.469 | 1.505 | 1.473 | 1.312 | +6.45% | +7.55% | ok |

**picks 1-20** — n = 380

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.092 | 1.220 | 1.396 | 1.559 | 1.566 | 1.480 | 1.317 | +9.22% | +4.78% | ok |
| ORDER P | 1.000 | 1.098 | 1.205 | 1.353 | 1.511 | 1.527 | 1.479 | 1.317 | +9.79% | +4.21% | ok |
| FIX A | 1.000 | 1.116 | 1.226 | 1.369 | 1.522 | 1.534 | 1.479 | 1.317 | +11.59% | +2.41% | ok |
| FIX B1 | 1.000 | 1.098 | 1.205 | 1.353 | 1.510 | 1.527 | 1.449 | 1.297 | +9.79% | +4.21% | ok |
| FIX B2 | 1.000 | 1.098 | 1.205 | 1.353 | 1.511 | 1.527 | 1.455 | 1.307 | +9.79% | +4.21% | ok |
| A+B1 | 1.000 | 1.116 | 1.226 | 1.369 | 1.521 | 1.533 | 1.453 | 1.299 | +11.59% | +2.41% | ok |
| A+B2 | 1.000 | 1.116 | 1.226 | 1.369 | 1.521 | 1.533 | 1.458 | 1.309 | +11.59% | +2.41% | ok |

**picks 21-64** — n = 820

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.963 | 1.106 | 1.314 | 1.401 | 1.478 | 1.510 | 1.324 | -3.67% | +17.67% | SELL-RED |
| ORDER P | 1.000 | 0.983 | 1.120 | 1.316 | 1.386 | 1.459 | 1.509 | 1.324 | -1.73% | +15.73% | SELL-RED |
| FIX A | 1.000 | 0.983 | 1.122 | 1.318 | 1.388 | 1.461 | 1.510 | 1.324 | -1.70% | +15.70% | SELL-RED |
| FIX B1 | 1.000 | 0.983 | 1.120 | 1.316 | 1.385 | 1.458 | 1.492 | 1.311 | -1.69% | +15.69% | SELL-RED |
| FIX B2 | 1.000 | 0.983 | 1.120 | 1.316 | 1.386 | 1.459 | 1.496 | 1.318 | -1.70% | +15.70% | SELL-RED |
| A+B1 | 1.000 | 0.983 | 1.122 | 1.317 | 1.387 | 1.460 | 1.493 | 1.312 | -1.66% | +15.66% | SELL-RED |
| A+B2 | 1.000 | 0.983 | 1.121 | 1.317 | 1.387 | 1.460 | 1.497 | 1.319 | -1.68% | +15.68% | SELL-RED |

**picks 1-10** — n = 190

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.082 | 1.209 | 1.400 | 1.552 | 1.518 | 1.423 | 1.247 | +8.22% | +5.78% | ok |
| ORDER P | 1.000 | 1.086 | 1.181 | 1.351 | 1.502 | 1.480 | 1.423 | 1.247 | +8.62% | +5.38% | ok |
| FIX A | 1.000 | 1.112 | 1.210 | 1.371 | 1.516 | 1.488 | 1.423 | 1.247 | +11.18% | +2.82% | ok |
| FIX B1 | 1.000 | 1.086 | 1.181 | 1.351 | 1.502 | 1.480 | 1.394 | 1.226 | +8.62% | +5.38% | ok |
| FIX B2 | 1.000 | 1.086 | 1.181 | 1.351 | 1.502 | 1.480 | 1.400 | 1.236 | +8.62% | +5.38% | ok |
| A+B1 | 1.000 | 1.112 | 1.210 | 1.371 | 1.516 | 1.488 | 1.399 | 1.229 | +11.18% | +2.82% | ok |
| A+B2 | 1.000 | 1.112 | 1.210 | 1.371 | 1.516 | 1.488 | 1.404 | 1.238 | +11.18% | +2.82% | ok |

**picks 11-20** — n = 190

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.112 | 1.241 | 1.388 | 1.571 | 1.660 | 1.591 | 1.456 | +11.16% | +2.84% | ok |
| ORDER P | 1.000 | 1.121 | 1.252 | 1.359 | 1.527 | 1.620 | 1.589 | 1.456 | +12.07% | +1.93% | ok |
| FIX A | 1.000 | 1.124 | 1.257 | 1.365 | 1.533 | 1.623 | 1.589 | 1.456 | +12.38% | +1.62% | ok |
| FIX B1 | 1.000 | 1.121 | 1.252 | 1.358 | 1.526 | 1.618 | 1.556 | 1.437 | +12.07% | +1.93% | ok |
| FIX B2 | 1.000 | 1.121 | 1.252 | 1.358 | 1.526 | 1.618 | 1.563 | 1.447 | +12.07% | +1.93% | ok |
| A+B1 | 1.000 | 1.124 | 1.257 | 1.365 | 1.531 | 1.621 | 1.558 | 1.438 | +12.38% | +1.62% | ok |
| A+B2 | 1.000 | 1.124 | 1.257 | 1.365 | 1.532 | 1.621 | 1.564 | 1.448 | +12.38% | +1.62% | ok |

**picks 21-30** — n = 190

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.053 | 1.223 | 1.467 | 1.632 | 1.629 | 1.686 | 1.458 | +5.26% | +8.74% | ok |
| ORDER P | 1.000 | 1.074 | 1.242 | 1.447 | 1.595 | 1.594 | 1.686 | 1.458 | +7.37% | +6.63% | ok |
| FIX A | 1.000 | 1.074 | 1.243 | 1.449 | 1.597 | 1.595 | 1.686 | 1.458 | +7.41% | +6.59% | ok |
| FIX B1 | 1.000 | 1.075 | 1.242 | 1.447 | 1.594 | 1.592 | 1.658 | 1.443 | +7.54% | +6.46% | ok |
| FIX B2 | 1.000 | 1.075 | 1.242 | 1.447 | 1.595 | 1.593 | 1.664 | 1.451 | +7.47% | +6.53% | ok |
| A+B1 | 1.000 | 1.076 | 1.243 | 1.449 | 1.597 | 1.594 | 1.659 | 1.443 | +7.57% | +6.43% | ok |
| A+B2 | 1.000 | 1.075 | 1.243 | 1.449 | 1.597 | 1.595 | 1.665 | 1.452 | +7.51% | +6.49% | ok |

**picks 31-40** — n = 190

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.893 | 0.974 | 1.288 | 1.268 | 1.403 | 1.294 | 1.161 | -10.70% | +24.70% | SELL-RED |
| ORDER P | 1.000 | 0.911 | 0.978 | 1.295 | 1.254 | 1.384 | 1.292 | 1.161 | -8.88% | +22.88% | SELL-RED |
| FIX A | 1.000 | 0.911 | 0.979 | 1.296 | 1.256 | 1.385 | 1.292 | 1.161 | -8.87% | +22.87% | SELL-RED |
| FIX B1 | 1.000 | 0.911 | 0.981 | 1.296 | 1.255 | 1.384 | 1.276 | 1.142 | -8.88% | +22.88% | SELL-RED |
| FIX B2 | 1.000 | 0.911 | 0.980 | 1.295 | 1.254 | 1.383 | 1.279 | 1.152 | -8.88% | +22.88% | SELL-RED |
| A+B1 | 1.000 | 0.911 | 0.982 | 1.297 | 1.256 | 1.385 | 1.278 | 1.143 | -8.88% | +22.88% | SELL-RED |
| A+B2 | 1.000 | 0.911 | 0.981 | 1.297 | 1.256 | 1.384 | 1.280 | 1.152 | -8.88% | +22.88% | SELL-RED |

**picks 41-64** — n = 440

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.931 | 1.096 | 1.180 | 1.277 | 1.386 | 1.512 | 1.325 | -6.89% | +20.89% | SELL-RED |
| ORDER P | 1.000 | 0.950 | 1.116 | 1.199 | 1.283 | 1.385 | 1.513 | 1.325 | -5.03% | +19.03% | SELL-RED |
| FIX A | 1.000 | 0.950 | 1.117 | 1.201 | 1.284 | 1.386 | 1.513 | 1.325 | -4.99% | +18.99% | SELL-RED |
| FIX B1 | 1.000 | 0.949 | 1.114 | 1.197 | 1.280 | 1.383 | 1.506 | 1.321 | -5.08% | +19.08% | SELL-RED |
| FIX B2 | 1.000 | 0.949 | 1.114 | 1.198 | 1.282 | 1.384 | 1.508 | 1.324 | -5.06% | +19.06% | SELL-RED |
| A+B1 | 1.000 | 0.950 | 1.115 | 1.199 | 1.281 | 1.385 | 1.507 | 1.321 | -5.03% | +19.03% | SELL-RED |
| A+B2 | 1.000 | 0.950 | 1.116 | 1.200 | 1.283 | 1.386 | 1.508 | 1.324 | -5.02% | +19.02% | SELL-RED |


### MODERN window, cohorts 2019-2023

**ALL picks 1-64** — n = 311

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.990 | 1.071 | 1.180 | 1.241 | 1.376 | 1.238 | 1.193 | -0.96% | +14.96% | SELL-RED |
| ORDER P | 1.000 | 1.014 | 1.063 | 1.132 | 1.187 | 1.335 | 1.238 | 1.193 | +1.45% | +12.55% | ok |
| FIX A | 1.000 | 1.024 | 1.073 | 1.142 | 1.194 | 1.338 | 1.238 | 1.193 | +2.41% | +11.59% | ok |
| FIX B1 | 1.000 | 1.014 | 1.062 | 1.132 | 1.185 | 1.334 | 1.205 | 1.176 | +1.40% | +12.60% | ok |
| FIX B2 | 1.000 | 1.014 | 1.063 | 1.132 | 1.186 | 1.334 | 1.211 | 1.185 | +1.42% | +12.58% | ok |
| A+B1 | 1.000 | 1.024 | 1.073 | 1.142 | 1.193 | 1.337 | 1.206 | 1.177 | +2.36% | +11.64% | ok |
| A+B2 | 1.000 | 1.024 | 1.073 | 1.142 | 1.193 | 1.338 | 1.213 | 1.185 | +2.38% | +11.62% | ok |

**picks 1-20** — n = 100

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.096 | 1.194 | 1.336 | 1.480 | 1.578 | 1.356 | 1.548 | +9.58% | +4.42% | ok |
| ORDER P | 1.000 | 1.129 | 1.184 | 1.280 | 1.422 | 1.542 | 1.356 | 1.548 | +12.88% | +1.12% | ok |
| FIX A | 1.000 | 1.144 | 1.201 | 1.295 | 1.433 | 1.546 | 1.356 | 1.548 | +14.41% | -0.41% | **BUY-RED** |
| FIX B1 | 1.000 | 1.129 | 1.184 | 1.280 | 1.422 | 1.541 | 1.326 | 1.537 | +12.88% | +1.12% | ok |
| FIX B2 | 1.000 | 1.129 | 1.184 | 1.280 | 1.422 | 1.541 | 1.332 | 1.542 | +12.88% | +1.12% | ok |
| A+B1 | 1.000 | 1.144 | 1.201 | 1.295 | 1.432 | 1.545 | 1.328 | 1.538 | +14.41% | -0.41% | **BUY-RED** |
| A+B2 | 1.000 | 1.144 | 1.201 | 1.295 | 1.432 | 1.546 | 1.334 | 1.543 | +14.41% | -0.41% | **BUY-RED** |

**picks 21-64** — n = 211

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.820 | 0.873 | 0.929 | 0.854 | 1.062 | 1.058 | 0.647 | -17.97% | +31.97% | SELL-RED |
| ORDER P | 1.000 | 0.830 | 0.866 | 0.894 | 0.806 | 1.014 | 1.058 | 0.647 | -17.01% | +31.01% | SELL-RED |
| FIX A | 1.000 | 0.830 | 0.867 | 0.896 | 0.808 | 1.016 | 1.058 | 0.647 | -16.98% | +30.98% | SELL-RED |
| FIX B1 | 1.000 | 0.829 | 0.866 | 0.893 | 0.804 | 1.012 | 1.020 | 0.622 | -17.13% | +31.13% | SELL-RED |
| FIX B2 | 1.000 | 0.829 | 0.866 | 0.893 | 0.805 | 1.013 | 1.028 | 0.636 | -17.08% | +31.08% | SELL-RED |
| A+B1 | 1.000 | 0.829 | 0.867 | 0.895 | 0.806 | 1.014 | 1.021 | 0.623 | -17.10% | +31.10% | SELL-RED |
| A+B2 | 1.000 | 0.830 | 0.867 | 0.895 | 0.807 | 1.015 | 1.029 | 0.636 | -17.04% | +31.04% | SELL-RED |

**picks 1-10** — n = 50

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.137 | 1.257 | 1.450 | 1.621 | 1.667 | 1.426 | 1.604 | +13.65% | +0.35% | ok |
| ORDER P | 1.000 | 1.188 | 1.252 | 1.394 | 1.569 | 1.639 | 1.426 | 1.604 | +18.85% | -4.85% | **BUY-RED** |
| FIX A | 1.000 | 1.208 | 1.274 | 1.412 | 1.579 | 1.644 | 1.426 | 1.604 | +20.83% | -6.83% | **BUY-RED** |
| FIX B1 | 1.000 | 1.188 | 1.252 | 1.394 | 1.569 | 1.639 | 1.401 | 1.592 | +18.85% | -4.85% | **BUY-RED** |
| FIX B2 | 1.000 | 1.188 | 1.252 | 1.394 | 1.569 | 1.639 | 1.406 | 1.597 | +18.85% | -4.85% | **BUY-RED** |
| A+B1 | 1.000 | 1.208 | 1.274 | 1.412 | 1.579 | 1.644 | 1.403 | 1.593 | +20.83% | -6.83% | **BUY-RED** |
| A+B2 | 1.000 | 1.208 | 1.274 | 1.412 | 1.579 | 1.644 | 1.408 | 1.598 | +20.83% | -6.83% | **BUY-RED** |

**picks 11-20** — n = 50

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 1.021 | 1.077 | 1.127 | 1.223 | 1.420 | 1.233 | 1.442 | +2.11% | +11.89% | ok |
| ORDER P | 1.000 | 1.019 | 1.060 | 1.070 | 1.154 | 1.367 | 1.233 | 1.442 | +1.94% | +12.06% | ok |
| FIX A | 1.000 | 1.027 | 1.068 | 1.079 | 1.165 | 1.371 | 1.233 | 1.442 | +2.66% | +11.34% | ok |
| FIX B1 | 1.000 | 1.019 | 1.060 | 1.070 | 1.152 | 1.364 | 1.193 | 1.434 | +1.94% | +12.06% | ok |
| FIX B2 | 1.000 | 1.019 | 1.060 | 1.070 | 1.153 | 1.366 | 1.200 | 1.439 | +1.94% | +12.06% | ok |
| A+B1 | 1.000 | 1.027 | 1.068 | 1.079 | 1.163 | 1.369 | 1.195 | 1.434 | +2.66% | +11.34% | ok |
| A+B2 | 1.000 | 1.027 | 1.068 | 1.079 | 1.163 | 1.370 | 1.202 | 1.439 | +2.66% | +11.34% | ok |

**picks 21-30** — n = 50

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.857 | 1.006 | 0.917 | 0.810 | 1.093 | 1.361 | 0.485 | -14.26% | +28.26% | SELL-RED |
| ORDER P | 1.000 | 0.862 | 1.013 | 0.868 | 0.741 | 1.014 | 1.361 | 0.485 | -13.84% | +27.84% | SELL-RED |
| FIX A | 1.000 | 0.862 | 1.014 | 0.869 | 0.743 | 1.017 | 1.361 | 0.485 | -13.82% | +27.82% | SELL-RED |
| FIX B1 | 1.000 | 0.862 | 1.013 | 0.868 | 0.741 | 1.014 | 1.301 | 0.446 | -13.84% | +27.84% | SELL-RED |
| FIX B2 | 1.000 | 0.862 | 1.013 | 0.868 | 0.741 | 1.014 | 1.312 | 0.465 | -13.84% | +27.84% | SELL-RED |
| A+B1 | 1.000 | 0.862 | 1.014 | 0.869 | 0.743 | 1.017 | 1.303 | 0.448 | -13.82% | +27.82% | SELL-RED |
| A+B2 | 1.000 | 0.862 | 1.014 | 0.869 | 0.743 | 1.017 | 1.314 | 0.466 | -13.82% | +27.82% | SELL-RED |

**picks 31-40** — n = 50

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.857 | 0.920 | 1.283 | 1.264 | 1.539 | 1.349 | 1.018 | -14.27% | +28.27% | SELL-RED |
| ORDER P | 1.000 | 0.883 | 0.908 | 1.250 | 1.221 | 1.507 | 1.349 | 1.018 | -11.73% | +25.73% | SELL-RED |
| FIX A | 1.000 | 0.883 | 0.908 | 1.250 | 1.224 | 1.508 | 1.349 | 1.018 | -11.73% | +25.73% | SELL-RED |
| FIX B1 | 1.000 | 0.883 | 0.908 | 1.249 | 1.221 | 1.509 | 1.324 | 0.991 | -11.73% | +25.73% | SELL-RED |
| FIX B2 | 1.000 | 0.883 | 0.908 | 1.249 | 1.221 | 1.507 | 1.329 | 1.006 | -11.73% | +25.73% | SELL-RED |
| A+B1 | 1.000 | 0.883 | 0.908 | 1.249 | 1.224 | 1.510 | 1.325 | 0.991 | -11.73% | +25.73% | SELL-RED |
| A+B2 | 1.000 | 0.883 | 0.908 | 1.250 | 1.224 | 1.508 | 1.329 | 1.007 | -11.73% | +25.73% | SELL-RED |

**picks 41-64** — n = 111

| board | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0->1 | buy margin | verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ORDER K | 1.000 | 0.749 | 0.694 | 0.636 | 0.548 | 0.627 | 0.482 | 0.487 | -25.06% | +39.06% | SELL-RED |
| ORDER P | 1.000 | 0.751 | 0.677 | 0.615 | 0.515 | 0.599 | 0.482 | 0.487 | -24.88% | +38.88% | SELL-RED |
| FIX A | 1.000 | 0.752 | 0.678 | 0.617 | 0.517 | 0.600 | 0.482 | 0.487 | -24.81% | +38.81% | SELL-RED |
| FIX B1 | 1.000 | 0.748 | 0.676 | 0.613 | 0.510 | 0.591 | 0.455 | 0.476 | -25.23% | +39.23% | SELL-RED |
| FIX B2 | 1.000 | 0.749 | 0.677 | 0.614 | 0.513 | 0.595 | 0.465 | 0.483 | -25.08% | +39.08% | SELL-RED |
| A+B1 | 1.000 | 0.749 | 0.679 | 0.616 | 0.512 | 0.592 | 0.456 | 0.477 | -25.15% | +39.15% | SELL-RED |
| A+B2 | 1.000 | 0.750 | 0.679 | 0.616 | 0.515 | 0.596 | 0.466 | 0.484 | -25.00% | +39.00% | SELL-RED |


### The pool arms, both windows, both baselines


**PRIMARY window**

| arm | n | ORDER K | ORDER P | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 | verdict on ORDER P | verdict worst variant |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| RD | 623 | -3.39% | -1.86% | -1.84% | -2.04% | -2.02% | -2.00% | -1.98% | SELL-RED | SELL-RED |
| MSD | 55 | — | — | — | — | — | — | — | n/a | n/a — MSD debuts in his own draft year, so the matrix has no year-1 cell; excluded and counted, never scored zero |
| UNR | 49 | -42.91% | -43.12% | -43.12% | -43.86% | -43.63% | -43.86% | -43.63% | SELL-RED | SELL-RED |
| IRE | 47 | +13.34% | +13.62% | +13.62% | +14.04% | +13.88% | +14.04% | +13.88% | ok | **BUY-RED** |
| PDA | 43 | -20.70% | -20.26% | -20.22% | -20.26% | -20.26% | -20.22% | -20.22% | SELL-RED | SELL-RED |
| PDN | 33 | -40.32% | -40.77% | -40.77% | -40.94% | -40.83% | -40.94% | -40.83% | SELL-RED | SELL-RED |
| PDS | 21 | -27.70% | -26.15% | -26.15% | -26.15% | -26.15% | -26.15% | -26.15% | SELL-RED | SELL-RED |
| SSP | 31 | +52.71% | +58.17% | +58.25% | +56.71% | +57.57% | +56.96% | +57.73% | **BUY-RED** | **BUY-RED** |
| ALLPOOL | 1016 | -4.93% | -3.60% | -3.58% | -3.77% | -3.71% | -3.73% | -3.68% | SELL-RED | SELL-RED |

**MODERN window**

| arm | n | ORDER K | ORDER P | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 | verdict on ORDER P | verdict worst variant |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| RD | 66 | -20.41% | -19.74% | -19.70% | -20.48% | -20.01% | -20.37% | -19.93% | SELL-RED | SELL-RED |
| MSD | 55 | — | — | — | — | — | — | — | n/a | n/a — MSD debuts in his own draft year, so the matrix has no year-1 cell; excluded and counted, never scored zero |
| UNR | 13 | -35.13% | -35.38% | -35.38% | -35.38% | -35.38% | -35.38% | -35.38% | SELL-RED | SELL-RED |
| IRE | 12 | -54.98% | -54.98% | -54.98% | -54.98% | -54.98% | -54.98% | -54.98% | SELL-RED | SELL-RED |
| PDA | 13 | -45.58% | -45.92% | -45.92% | -45.92% | -45.92% | -45.92% | -45.92% | SELL-RED | SELL-RED |
| PDN | 25 | -36.53% | -37.12% | -37.12% | -37.12% | -37.12% | -37.12% | -37.12% | SELL-RED | SELL-RED |
| SSP | 31 | +52.71% | +58.17% | +58.25% | +56.71% | +57.57% | +56.96% | +57.73% | **BUY-RED** | **BUY-RED** |
| ALLPOOL | 229 | -10.47% | -8.99% | -8.96% | -9.76% | -9.28% | -9.66% | -9.21% | SELL-RED | SELL-RED |

**PDS is absent from the modern window** because the arm has no rows in cohorts 2019-2023 that the
instrument can score. It is reported as absent, never as zero.

---

## 9 · THE TWO NEW RAIL BREACHES. NEITHER IS CAPPED AND NEITHER IS CHASED.

**The order's standing instruction is to halt and report on any law breach and never to trade one law
for another silently. Two variants break a rail that ORDER P did not. Both are stated here on their
own lines, at full precision, and nothing was moved to make them go away.**

### 9.1 FIX A pushes MODERN picks 1-20 through the +14% buy rail

| board | MODERN picks 1-20, n = 100 | verdict |
|---|---:|---|
| ORDER K | +9.577% | ok |
| ORDER P | +12.879% | ok |
| **FIX A** | **+14.414%** | **BUY-RED** |
| FIX B1 | +12.879% | ok |
| FIX B2 | +12.879% | ok |
| **A + B1** | **+14.414%** | **BUY-RED** |
| **A + B2** | **+14.414%** | **BUY-RED** |

**This is a band that was inside the rail on ORDER P and is outside it on any board carrying FIX A.**
It is 0.414 percentage points over, on 100 rows.

The mechanism is not mysterious. FIX A gives back the charge it was over-collecting from expensive
young rows, and expensive young rows are concentrated in the top twenty picks of recent drafts. The
same movement shows in the neighbouring cells: MODERN picks 1-10 goes +18.85% -> **+20.83%** (already
a disclosed breach on ORDER P, now worse by 1.98 points), and PRIMARY picks 1-10 goes +8.62% ->
**+11.18%** (still inside the rail, with 2.82 points of room left against ORDER P's 5.38).

**This seat does not rule on it. It is the direct cost of repairing defect 1 and it is priced here so
the owner can weigh the two against each other rather than be told a repair is free.**

### 9.2 FIX B1 pushes the IRE pool arm through the +14% buy rail

| board | IRE, primary window, n = 47 | verdict |
|---|---:|---|
| ORDER K | +13.344% | ok |
| ORDER P | +13.618% | ok |
| FIX A | +13.618% | ok |
| **FIX B1** | **+14.039%** | **BUY-RED** |
| FIX B2 | +13.883% | ok |
| **A + B1** | **+14.039%** | **BUY-RED** |
| A + B2 | +13.883% | ok |

**IRE was 0.38 points under the rail on ORDER P and B1 takes it 0.04 points over.** B2 leaves it
0.117 points under. This is a 47-row arm and the margin is thin in both directions; it is reported
because it crosses, not because it is large.

### 9.3 The breaches that were already there, and what the repairs do to them

| breach | ORDER K | ORDER P | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| MODERN picks 1-10 (+14% rail) | +13.65% | **+18.85%** | **+20.83%** | +18.85% | +18.85% | **+20.83%** | **+20.83%** |
| SSP, both windows (+14% rail) | +52.71% | **+58.17%** | **+58.25%** | **+56.71%** | **+57.57%** | **+56.96%** | **+57.73%** |

**Both are inherited.** Modern picks 1-10 was ORDER P's own disclosed breach and the branch the owner
already agreed to rule on; FIX A makes it worse by 1.98 points and the B variants leave it exactly
alone. SSP was over the rail before ORDER K existed; **B1 and B2 both IMPROVE it** (58.17 -> 56.71 and
-> 57.57) and FIX A worsens it by 0.08, which is inside the noise of a 31-row arm and is printed
rather than rounded away.

---

## 10 · THE CLASS MARKS

**The basis is the registered W2 basis: DRAFT classes 2005-2015, ENTRY_FLOOR 2005, which is cohort
years 2006-2016. That is the basis the 1.03 floor and the 1.14 rail are written on. It is NOT the
`ok_class.py` 2004-2014 window, which is the cohort clock and is carried below only so the two can be
told apart on sight.**

**The instrument was validated before any ORDER Q number was quoted:** it reproduces ORDER K's own
published marks off ORDER K's own matrix — W2 1.0513 against 1.0513 and cohort 1.0324 against 1.0324,
both to 0.0000.

| board | **W2 mark (the rail's basis)** | cohort clock | max single class | at cohort | classes >= 1.14 |
|---|---:|---:|---:|---:|---:|
| ORDER K | 1.0513 | 1.0324 | 1.1363 | 2012 | **0** |
| ORDER P | 1.0613 | 1.0322 | 1.2047 | 2016 | **3** |
| **FIX A** | **1.0697** | 1.0410 | **1.2081** | 2016 | **3** |
| **FIX B1** | **1.0611** | 1.0321 | **1.2046** | 2016 | **3** |
| **FIX B2** | **1.0611** | 1.0321 | **1.2045** | 2016 | **3** |
| **A + B1** | **1.0696** | 1.0409 | **1.2083** | 2016 | **3** |
| **A + B2** | **1.0696** | 1.0409 | **1.2081** | 2016 | **3** |

**Every variant is inside the owner's law on the registered basis: above the 1.03 floor and under the
1.14 rail.** FIX A raises the mark by 0.0084; B1 and B2 each lower it by 0.0002.

### The per-class table, on the registered W2 window

| draft class (cohort) | ORDER K | ORDER P | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2005 (2006) | 0.8562 | 0.8230 | 0.8311 | 0.8230 | 0.8230 | 0.8311 | 0.8311 |
| 2006 (2007) | 1.0579 | 1.0155 | 1.0231 | 1.0155 | 1.0155 | 1.0231 | 1.0231 |
| 2007 (2008) | 1.0713 | 1.0378 | 1.0548 | 1.0378 | 1.0378 | 1.0548 | 1.0548 |
| 2008 (2009) | 1.0063 | 1.0263 | 1.0392 | 1.0259 | 1.0261 | 1.0388 | 1.0390 |
| 2009 (2010) | 1.0432 | 1.0680 | 1.0815 | 1.0680 | 1.0680 | 1.0814 | 1.0814 |
| **2010 (2011)** | 1.1359 | **1.1570** | **1.1657** | **1.1581** | **1.1572** | **1.1669** | **1.1659** |
| **2011 (2012)** | 1.1363 | **1.1595** | **1.1621** | **1.1577** | **1.1591** | **1.1605** | **1.1618** |
| 2012 (2013) | 1.0673 | 1.0901 | 1.0967 | 1.0915 | 1.0891 | 1.0981 | 1.0957 |
| 2013 (2014) | 1.0535 | 1.0760 | 1.0815 | 1.0745 | 1.0757 | 1.0799 | 1.0812 |
| 2014 (2015) | 1.0300 | 1.0158 | 1.0232 | 1.0153 | 1.0159 | 1.0227 | 1.0232 |
| **2015 (2016)** | 1.1060 | **1.2047** | **1.2081** | **1.2046** | **1.2045** | **1.2083** | **1.2081** |

**THE THREE CLASSES OVER THE 1.14 LINE DO NOT MOVE OFF IT UNDER ANY VARIANT.** The engine's own
O32/O36 calibration was held to "max class <= 1.139 (the 1.14 no-arb line)". ORDER P broke it on three
classes and **no repair in this order fixes that, and FIX A makes all three slightly worse**: draft
2010 +0.0087, draft 2011 +0.0026, draft 2015 +0.0034. B1 and B2 move them by less than 0.002 in
either direction.

**That is a null result on a question the order asked, and it is reported as one.** These repairs are
about the price axis and the age axis; the three-class breach is about the size of the charge's
effect on particular cohorts, and nothing here touches it.

Every class in the full range, so a single class breaking the rail cannot hide, is in
`CLASS_PERCLASS_Q_out.txt`. Outside the W2 window nothing crosses 1.14 on any variant.

---

## 11 · THE NAMED ROWS — CONSEQUENCES, NEVER TARGETS

**Not one constant in this order was chosen with any of these rows in view, and no row's value is an
acceptance criterion. That is a standing prohibition in this project after a real error.**

| row | age | pick | g | ORDER K | ORDER P | FIX A | FIX B1 | FIX B2 | A+B1 | A+B2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sam Lalor | 20 | 1 | 20 | 3,456 | 3,060 | **3,395** | 3,060 | 3,060 | **3,395** | **3,395** |
| Willem Duursma | 19 | 1 | 17 | 3,703 | 3,920 | **4,236** | 3,920 | 3,920 | **4,236** | **4,236** |
| Zane Duursma | 21 | 4 | 38 | 629 | 194 | **206** | 194 | 194 | **206** | **206** |
| Finn O'Sullivan | 20 | 2 | 37 | 3,462 | 2,810 | **3,055** | 2,810 | 2,810 | **3,055** | **3,055** |
| Harley Reid | 21 | 1 | 58 | 3,786 | 3,723 | **3,813** | 3,723 | 3,723 | **3,813** | **3,813** |
| Zeke Uwland | 19 | 2 | 16 | 1,949 | 1,486 | **1,582** | 1,486 | 1,486 | **1,582** | **1,582** |
| Josh Sinn | 23 | 12 | 30 | 357 | 73 | **76** | 73 | 73 | **76** | **76** |
| Campbell Chesser | 23 | 14 | 39 | 333 | 167 | **168** | 167 | 167 | **168** | **168** |
| James Tunstill | 23 | 41 | 23 | 176 | 42 | **44** | 42 | 42 | **44** | **44** |
| Sam Darcy | 23 | 2 | 51 | 4,373 | 4,450 | 4,450 | 4,450 | 4,450 | 4,450 | 4,450 |
| Taj Hotton | 20 | 12 | 13 | 1,628 | 1,722 | **1,829** | 1,722 | 1,722 | **1,829** | **1,829** |

**Read the B1 and B2 columns against ORDER P: every one of these rows is under 24, so no B variant
touches any of them.** The B repairs act on ages 24 and over. The rows they move are elsewhere.

**Read Josh Sinn, James Tunstill and Campbell Chesser against ORDER K.** Their ORDER K prices — 357,
176 and 333 — are exactly what ORDER P hands them back on their 24th birthday. Under B1 that handback
is zero: their price on the birthday is their price the day before.

**Sam Darcy does not move on any variant.** His charge is already zero on ORDER P, so there is nothing
to cap and he is 23, so no B variant reaches him. A null, reported as one.

---

## 12 · THE MOVERS LEDGERS

**FIX A against ORDER P — 77 rows, all up, +2,357 points. Ten largest:**

| row | pick | age | g | ORDER P | FIX A | move |
|---|---:|---:|---:|---:|---:|---:|
| Sam Lalor | 1 | 20 | 20 | 3,060 | 3,395 | +335 |
| Willem Duursma | 1 | 19 | 17 | 3,920 | 4,236 | +316 |
| Finn O'Sullivan | 2 | 20 | 37 | 2,810 | 3,055 | +245 |
| Sam Cumming | 7 | 19 | 13 | 2,007 | 2,150 | +143 |
| Harvey Langford | 6 | 20 | 41 | 2,422 | 2,536 | +114 |
| Taj Hotton | 12 | 20 | 13 | 1,722 | 1,829 | +107 |
| Zeke Uwland | 2 | 19 | 16 | 1,486 | 1,582 | +96 |
| Harley Reid | 1 | 21 | 58 | 3,723 | 3,813 | +90 |
| Samuel Grlj | 8 | 19 | 17 | 1,390 | 1,467 | +77 |
| Cameron Mackenzie | 7 | 22 | 63 | 1,852 | 1,924 | +72 |

**There is no "down" list for FIX A. It has no downward movers, by construction.**

**FIX B1 against ORDER P — 245 rows, 46 up and 199 down, −6,567 points. Five largest each way:**

| direction | row | pick | age | g | ORDER P | FIX B1 | move |
|---|---|---:|---:|---:|---:|---:|---:|
| up | Marcus Herbert | 13 | 24 | 6 | 690 | 793 | +103 |
| up | Ned Moyle | 5 | 24 | 25 | 1,568 | 1,671 | +103 |
| up | Lachlan McAndrew | pool | 26 | 21 | 841 | 920 | +79 |
| up | Tom McCarthy | 1 | 26 | 28 | 1,211 | 1,259 | +48 |
| up | Milan Murdock | pool | 26 | 15 | 156 | 196 | +40 |
| down | Jamarra Ugle-Hagan | 1 | 24 | 70 | 534 | 297 | −237 |
| down | Conor Stone | 15 | 24 | 28 | 218 | 17 | −201 |
| down | Paddy Dow | 3 | 27 | 83 | 206 | 10 | −196 |
| down | Luke Pedlar | 11 | 24 | 49 | 217 | 43 | −174 |
| down | Dylan Stephens | 5 | 25 | 100 | 687 | 515 | −172 |

**FIX B2 against ORDER P — 84 rows, 13 up and 71 down, −2,864 points.** Same shape, about half the
size, and confined to ages 24 and 25. Largest up Ned Moyle +63, largest down Jamarra Ugle-Hagan −185.

The full ledgers, five board columns and the mechanism legs, are in `BOARDS_Q_out.txt`.

---

## 13 · THE INTERACTION. THE SUPERVISOR EXPECTED ONE AND THERE IS ONE.

**The variants are not additive.**

| combination | arithmetic if additive | **actual** | difference |
|---|---:|---:|---:|
| A + B1 | 666,434 + 2,357 − 6,567 = **662,224** | **662,685** | **+461** |
| A + B2 | 666,434 + 2,357 − 2,864 = **665,927** | **666,093** | **+166** |

**A on top of B1 gives back 2,818 points where A on top of ORDER P gives back 2,357.** The reason is
direct: B1 extends the ORDER P charge to rows aged 24 and over, and some of those rows are burned by
defect 1 as well. A can only cap a charge that is being applied, so widening the population that
carries the charge widens the population A can help.

**The same shows in the row counts, and Q7 holds on every one of them — every move is UP.**

| comparison | rows moved | up | down | points given back |
|---|---:|---:|---:|---:|
| FIX A against ORDER P | 77 | **77** | **0** | +2,357 |
| FIX A against FIX B1 | 170 | **170** | **0** | **+2,818** |
| FIX A against FIX B2 | 114 | **114** | **0** | **+2,523** |

A alone reaches 77 rows. On top of B1 it reaches 170 — **93 more rows, and every one of them is a
mature row that only has a capped charge to give back because B1 put a charge on it in the first
place.** On top of B2 it reaches 114, the extra 37 being the ages-24-and-25 rows B2 charges.

---

## 14 · PREDICTIONS SCORED. THE PREREG WROTE EIGHT AND ONE WAS WRONG.

| # | prediction, written before the first build | outcome |
|---|---|---|
| 1 | Step 0 check 0A agrees essentially exactly | **RIGHT** — exact algebra, 9.1e-13 on the decomposition; the only error is board rounding |
| 2 | FIX A raises the board total | **RIGHT** — +2,357 |
| 3 | FIX A's effect is concentrated in picks 1-10 | **RIGHT** — 1,820 of 2,308 burned points are picks 1-10 |
| 4 | FIX B1 moves mature rows a lot, and downward | **RIGHT** — 245 of 429 rows, −6,567, 199 of 245 down |
| 5 | FIX B1 makes the board total fall substantially | **RIGHT** — −6,567, the largest number in the order |
| 6 | FIX B2 moves rows aged 24 and 25 and no others | **RIGHT** — 84 rows, all at 24-25; 0 of 320 rows aged 26+ |
| 7 | the combinations are not additive; A on top of B1 gives back more | **RIGHT** — +2,818 against +2,357 |
| 8 | B1 and B2 move the W2 class mark and A moves it only a little | **WRONG, and backwards.** A moves it by **+0.0084**; B1 and B2 each move it by **−0.0002**. The reasoning was that the W2 window's rows are now mature, so the B repairs would reach them — but the class mark is a year-0-to-year-1 ratio and a class's year-1 cell is priced when its members are 19, not when they are 30. The B repairs cannot reach it and A can. |

**Prediction 8 was wrong for a stateable reason and the reason is written down rather than glossed.**

**The order's own expectation about B2's mature rows was also wrong**, and the prereg said so in
advance. §6.

---

## 15 · WHAT THIS SEAT COULD NOT MEASURE, AND EVERY DEVIATION

- **Nothing is adopted, nothing lands, no variant is recommended and no pull request was opened.**
  This seat delivers prices.
- **The three draft classes over 1.14 are NOT repaired by anything here** and FIX A makes all three
  slightly worse. §10. That remains an open ruling from ORDER P.
- **Modern picks 1-10 is not repaired either** and FIX A makes it worse by 1.98 points. §9.3.
- **FIX A's monotonicity holds up to the engine's own one-decimal rounding of the premium axis, not to
  the last bit.** The residual is bounded at about 3e-5 of the leg at v0 3,000 and does not appear at
  the 0.1%-of-price resolution of the dense sweep (0 falling steps in 30 of 30 cells). It is a real
  qualification and it is not asserted away.
- **B2's endpoint of 26 is invented.** Nothing measured it. A different endpoint gives different
  numbers and this seat has not swept it, because sweeping an invented parameter to find a flattering
  value is the thing the project forbids.
- **B2's ramp is on an integer age axis**, so it replaces one step with three, and it moves the
  50%-gain birthdays from age 23 to ages 24 and 25 rather than removing them. §5.2.
- **The birthday census isolates the CHARGE channel only.** It re-prices each row with the charge
  evaluated one year older and everything else — games, output, bar, fade, age credit — held exactly
  fixed. A player's real 24th birthday also moves the S1 bar and zeroes the age credit; those are
  ORDER K and S1 machinery that exist identically on every board here and are not this order's
  defect. **This is a scope choice and it is disclosed rather than implied.**
- **`v0_start`'s decay-gate channel was named in the prereg as the one thing that could break the
  sweep, and it binds on 0 of 289 young rows.** It was measured, not reasoned about. It may still bind
  on some other population; only the young board cross-section was swept.
- **The full-engine sweep (`oq_sweep.py`) was run on ORDER P only.** The other five variants use
  `oq_census.py`, which recomputes only the charge factor per step and reuses the engine's own
  constant non-pedigree legs. **That is exact given the 0-of-289 result above, and it was validated:
  on ORDER P it reproduces the full-engine sweep's census row for row and point for point — 77 of 268,
  2,308 points, the same worst five.** It is still a shortcut and it is named as one.
- **The QB1 continuity run tested 803 rows where the others tested 804.** One row carries no
  reassemblable pedigree leg on that board. It is one row and it is reported rather than rounded to
  "all".
- **`run_panel.sh` / Guard 5 does not pass on this branch and did not pass before this order.** The
  register's v737 entry records five stale pins on `land/order-29`, all of which predate ORDER P.
  This seat has not touched the workspace, `data/expected_boot.json` or `engine/forward_valuation`.
  The `engine_head` pin necessarily moves again because this order edits `_merged_recover.py` and
  `rl_model.py`; re-stamping it is a landing act and this order lands nothing. **Every board here was
  built through `bbQ.sh`, which pins the store, the engine, the forward-valuation tree and the five
  thread variables explicitly and prints their md5s on every run.**
- **The load-time banner counters read zero in the standalone-import context** (`0 active rows now
  carry the ORDER P charge`). That is the same pre-existing property of every order's banner in that
  context that ORDER P disclosed; the real counts are on the boards. Disclosed rather than quietly
  corrected.
- **There is no hold-out.** These repairs act on ORDER P's premium surface, which is estimated on the
  same board's `v0` it is applied to. ORDER P disclosed that and it is unchanged here.
- **The veteran board (RL_O33) is still parked.** Nothing in this order touches it.
- **Three deviations from the prereg, declared.** (1) The prereg said the burn census would be run
  in-engine for every variant; it was run in-engine for ORDER P and by the validated exact shortcut
  for the other five. (2) The birthday census was extended to EVERY age, not only 23, because
  restricting it to 23 would have hidden B2's real behaviour. (3) A per-class table across all seven
  boards was added; the prereg only promised the three flagged classes.

---

## 16 · EVERY FILE

| file | what it is |
|---|---|
| `PREREG_Q.md` | the prereg, pushed at `df02eaa` before the first engine edit |
| `oq_lib.py` | the engine harness and the blend-site leg recorder |
| `oq_step0a.py` · `STEP0A_Q.json` · `STEP0A_Q_out.txt` | STEP 0 check 0A — the supervisor's inference against the engine's own legs |
| `oq_sweep.py` · `SWEEP_P.json` · `SWEEP_P_out.txt` | STEP 0 check 0B — the burn census re-run by full-engine re-pricing, with the wrapper proved inert |
| `oq_census.py` · `CENSUS_*.json` · `CENSUS_*_out.txt` | the burn and birthday censuses for every variant |
| `bbQ.sh` · `build_allQ.sh` · `BUILD_Q_out.txt` | the board suite: base stack, ORDER K, ORDER P byte-exact, five variants, the dial-implies test, five determinism repeats |
| `run_emit_Q.sh` · `run_emits_Q.sh` · `EMIT_*_out.txt` | the five walk-forward matrices, day-0 guard pointed at ORDER K's own reference |
| `bb_noarbQ.sh` · `NOARB_Q_out.txt` · `t338ext_*.txt` | the disclosed no-arb instruments, md5-pinned at run |
| `oq_bands.py` · `BANDS_Q.json` · `BANDS_Q_out.txt` · `BANDS_SUMMARY_Q_out.txt` | the ND band tables in BOTH windows |
| `oq_tables.py` · `STANDING_TABLES_Q.json` · `STANDING_TABLES_Q_out.txt` | the standing suite, pool arms both windows, vantage matrix, entry-year control |
| `oq_class.py` · `CLASS_Q.json` · `CLASS_Q_out.txt` · `CLASS_PERCLASS_Q_out.txt` | the class marks on both bases and the per-class table for all seven boards |
| `oq_boards.py` · `BOARDS_Q.json` · `BOARDS_Q_out.txt` | totals, falsifiers, mature-row movement, the named rows, the movers ledgers |
| `oq_continuity.py` · `CONTINUITY_*.json` · `CONTINUITY_*_out.txt` | continuity on every axis, including the two the ORDER P suite did not have |
