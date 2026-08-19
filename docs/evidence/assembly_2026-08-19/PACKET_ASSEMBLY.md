# PACKET — THE ASSEMBLY BUILD. THE CANDIDATE.

**Seat:** ASSEMBLY BUILD. **Date:** 2026-08-19. **Branch:** `land/order-29`.
**Prereg:** `PREREG_ASSEMBLY.md`, pushed at `c1dbd3e` **before the first engine edit**.
**Charter:** register `v748` — the go-word.

> **THE CANDIDATE IS FOR OWNER REVIEW. NOTHING LANDS. NOTHING MERGES. NO PULL REQUEST. NOTHING ON
> `main`. THE LIVE BOARD `88ce647f` WAS NEVER TOUCHED.**

---

## 0 · WHERE THIS PACKET STANDS

**BOTH HALTS THIS SEAT RAISED HAVE BEEN RULED ON BY THE OWNER (register v750), AND THE BOARD BELOW IS
THE REBUILD THAT CARRIES HIS RULINGS.**

### Halt 1 — the day-0 collision — RESOLVED: THE F4 SWAP IS WITHDRAWN

The seat halted because two ruled items could not both hold: acceptance demanded *day-0 bit-identical
89/89*, while item I2 demanded the F4 depth-4 inversion *not be relied on*. A day-0 sitter's price
**is** `v0 × D(c_u)`, so touching `D` at depths 3-4 necessarily re-prices sitters standing there —
measured at **28 of 95 day-0 rows, net −1,876**.

**THE OWNER RULED THE SWAP OUT. The measured wired row stays, rise and all.** His reasoning, on the
record: **a fourth-year sitter who is still listed is itself information** — clubs cut the two- and
three-year sitters who are not up to it, so surviving to a contracted fourth year signals potential.
That is the engine's own selection-as-evidence principle applied to the same object. The row is
measured (F4's control verified the engine literal against `FADE_31F.json::wired` at every depth to
1e-16) and it **stays documented as thin — n = 11 at depth 4**.

**Also on the record, and it matters: the swap was never green-lit.** It was folded into the absence
package without the owner's word. The halt was correct.

**CONSEQUENCE, now satisfied:** day-0 reads **89/89 bit-identical against the frozen reference**, and
the walk-forward emit runs — so the class mark and the full no-arb tables are in this packet.

### Halt 2 — the tail calibration — RESOLVED: THE ANCHOR MOVES TO p15

The p20 compression read **0.7378** against the register's ~1.04 expectation. **The owner ruled the
compression anchor to the 15th percentile.** `RL_O40_CAPPCT=15`, smooth form unchanged, slope 0.105
unchanged, `TMAX`/`THETA_R` recomputed under the assert discipline. **The built number is in §7 and it
rules; no other dial was moved to chase it.**

### One numeric discrepancy in the instruction, flagged rather than silently resolved

The v750 instruction quotes the row to keep as **D(3)=0.2628, D(4)=0.3460**. Those are the **ORDER A /
R1 vintage** values from F4 §16. The row **actually wired in the engine** — and the one F4 verified to
1e-16 — is the **31-F re-derived** row, **D(3)=0.2747857941376827, D(4)=0.39727085107749216**.

**This seat DROPPED THE SWAP, which restores the wired 31-F row untouched.** That is the only reading
consistent with the instruction's own requirement that day-0 come back to **89/89 bit-identical
against the frozen reference**: wiring 0.2628/0.3460 would have *changed* the fade row and broken
day-0 again. **If the owner meant to revert the fade row all the way to the R1 vintage, that is a
different and larger change and it has not been made — say the word and it is one build.**

### What went wrong inside this seat's own work, kept on the record

Three defects in my own wiring were found and repaired during the build. They are not tidied away
because the way each was caught is the useful part: **§8b** the SD offset that moved nothing (caught
by the per-lever md5 comparison), **§8c** the R3 collector reading the wrong clock and fading players
who had never missed a season (caught by reading rows, not totals), **§8d** an order-dependent price
(caught by the engine's own parity gate, not by me).

---

## 1 · WHAT WAS BUILT

Base **ORDER P** (`RL_O37` on the O36-K stack). **LAMBDA UNTOUCHED at the anchor `0.1743833037`** —
`RL_O40_LAMBDA` was never set on any board in this packet.

| item | dial | value | ruled at |
|---|---|---|---|
| A · FIX A | `RL_O38A` | 1 | v744/v748 |
| B · B1, the age-24 gate deleted | `RL_O38B1` | 1 | v748 |
| C · the mature refit | `RL_O40_PGMAT` | 1 | v745 |
| D · the compressed cap | `RL_O40_CAPFORM` / `RL_O40_CAPPCT` | smooth / 20 | standing + v748 |
| E · the slope | `RL_O39_BETASAT` | 0.105 | v745 |
| F · recency | `RL_O40_RECW` | 0.47 | v748 |
| G · the SD level offset | `RL_O41_SDOFF` | 2.98 | v744 |
| I1 · the credit curve | `RL_O41_CREDIT` | 1 | v744/v748 |
| I2 · the graded reset | `RL_O41_RESET` | 1 | v744/v748 |
| I3 · the injury stream | `RL_O41_INJ` | 1 | v744/v748 |
| I4 · the R3 production fade | `RL_O41_R3` | 1 | v744/v748 |

**H · RUCK — NOTHING WAS WIRED.** The diagnosis ruled it out. §2.

---

## 2 · THE RUCK DIAGNOSIS — RUN AT PREREG, BEFORE ANYTHING WAS WIRED

**The question.** T1 read RUCK at **−5.57** points a game against the pooled bar, the same kind of
number that bought SD a level offset. But RUCK's residual **swings** with age: −8.96 at 21, −5.42 at
22, **+3.84** at 23. A level offset is a constant, and a constant cannot fit a swing.

**The discriminator.** The residual is `avg − [ bar(pos, age) + PG(ln v0, class) ]`. **`PG` has no age
argument. The C3 age delta `O32_GATE_DELTA` has no price argument.** So the residual's age profile is
C3's to answer for and its price profile is PG's.

**Population and estimator are T1's, unchanged** — 5,041 season rows, 1,575 players, 58,488 games,
asserted equal to `PREMIUM_SURFACE.json`; ORDER P's own kernel estimator; bootstrap **clusters on
player**, B=2,000, seed 32. **T1 reproduced exactly as the control: SD −2.978, RUCK −5.569.**

| test | RUCK | SD (the control) |
|---|---|---|
| age slope, pts/game per year | **+5.779 [+4.139, +7.630]** — excludes zero | +0.540 [−0.214, +1.293] — includes zero |
| price slope, age partialled out | **+4.128 [+1.246, +6.889]** — excludes zero, the only position of six | −0.407 [−2.001, +1.183] — includes zero |
| residual removed by an AGE COLUMN beyond a LEVEL | **17.76%** | **0.86%** |

**THE VERDICT: RUCK'S MISFIRE IS THE C3 AGE-DELTA OBJECT, NOT `PG`.** RUCK is pooled into TALL with
KPD and KPF; a ruck develops later and the pooled column averages two timetables. **A level offset
would fit the average of a swing and be wrong at both ends** — too generous to a 23-year-old ruck and
still too harsh on a 21-year-old.

**PER THE CHARTER: NO PREMIUM OFFSET IS WIRED FOR RUCK.** `O32_GATE_DELTA` is named as the object a
future order would work on. **SD behaves as the control** — flat in age — **and that is what licenses
the SD offset going in standalone while RUCK does not.**

**What the diagnosis does not claim:** it does not fit a replacement C3 column and does not price one.
RUCK's age-19 and age-20 cells are thin and are not read. RUCK holds the widest pooled interval of the
six positions and nothing here narrows it.

---

## 3 · THE ABSENCE PACKAGE AS BUILT

Every constant is copied from a named measured artifact. **No constant in this package was fitted by
this seat.**

### I1 · the credit curve — `FOLLOWUP_F1.json::iso`

F1's guarded isotonic curve replaces the wired `min(1, games/2)`: 0 at 0 games, **0.1287 at 1**,
**0.2383 at 2**, 0.2455 at 5, 0.3857 at 6-7, 0.4519 at 8, 0.8879 at 9-10, **1.0 from 11**. Linear
between the measured knots. `credit(0) = 0` exactly, so **day-0 prices cannot move**.

**DISCLOSED DECISION.** `min(1, g/2)` appears at **two** sites — `o31_played_units` (the one the
charter names) and the post-delivery credit loop inside `o31_cu`. They answer the same question, and
leaving one behind would have the same season credit 0.24 on one clock and 1.00 on the other. **Both
sites take the curve.** Declared in the prereg before the build.

### I2 · the graded reset — `FOLLOWUP_F2.json::partA.games`

The wired law **wipes** all accrued sitting clock at a delivered season. F2 measured that no returning
season restores a never-sat comparable — the best cell (15+ games) reaches **0.596** and the cell at
the wired threshold reads **0.213** with an interval that excludes 1.0. So:

```
c_u = (1 - r) * c_pre + c_post          r = 1 IS the wired wipe (the exact dial-off identity)
```

`r` is read as a **step function on the measured bands and is NOT interpolated**, because F2's own
preregistered null (F2-P4) is that this sample **cannot** separate a step at ten from a smooth curve.
Inventing a smooth interpolant would claim a shape the measurement declines to supply.
**No position cut on `r`** — F2 has none; the tall/small exponent carries through the existing
`o36_kappa` exponent on `D`, so position differentiation still comes from the object that measured it
and is not applied twice.

**F4 absorbed.** The wired row carries **D(4) = 0.3973 above D(3) = 0.2748** — an inversion resting on
an **11-row** cell whose mean is 4.9× its median and whose ordering flips under a change of `v0` basis.
**It is not relied on.** Depth ≥3 takes the **UNCONDITIONAL monotone** row — D(3) = **0.2143**,
D(4) = **0.1052**, **154 rows** at depth 4. **DISCLOSED SEAM:** the unconditional reading is a
different conditioning and its own depth-2 value (0.5684) differs from the wired one (0.5583); only
depths 3 and 4 are taken per the charter, so the row joins two conditionings at that boundary.

### I3 · the injury stream — the owner's pinned annotation, LIVE BOARD ONLY

`docs/owner_annotations/SITTER_2026_v1.csv`. **Asserted at load: md5 `b26798c3…`, 219 rows, exactly
37 marked `injured=Y`, and 37 of 37 matched to engine rows.** Any of those failing HALTS the build.
The file is committed on `main` (`046d853`) and was not on `land/order-29`; this seat brought it
across **unmodified** and asserts its md5 — it is the owner's file byte for byte.

**The two channels, exactly as ruled:** for a **delivered** row a logged-injured absence **pauses the
sitting clock** — the live year's absence accrues nothing; an **unexplained** absence gets **no grace
year** and keeps fading continuously on `fE`. **Rookies and never-delivered rows are cause-blind and
unchanged** — no annotation is read for a row with no delivered season, whatever its flag says.

**SCOPE, DECLARED:** the annotation is a **2026 log** and says nothing about earlier seasons, so the
pause is the live year's fraction and no more. Extending it backwards would be inventing injury
history the owner did not write. The dial is inert on every non-live evaluation year — that is what
"live board only, no backtest" means mechanically.

### I4 · the R3 production fade — sized by the owner's R1 combined-take law

**There is no free parameter in this collector.** It does not carry a rate of its own; it collects
exactly the **residual** between what the existing collectors have already taken and what F3
**measured** the absence to cost.

```
target(c_x)    = F3's measured cost at the row's UNEXPLAINED depth   (0.3672 at depth 2, 0.7629 at 3,
                 0.8883 at 4, 0.9451 at 5; ZERO below depth 2)
taken_already  = (the pedigree-fade take + the D8 take) / the absence-free price
residual       = max(0, target - taken_already)
R3 on e        = remove  min(residual * absence_free_price, the production leg)
```

- **Zero below depth 2 by construction** — F3 cannot speak about depth 1 (its own normaliser) and the
  owner's words are "two seasons out". Day-0 and one-season-out rows are untouched.
- **The D8 overlap reconciles by construction** — D8 is inside `taken_already`, so the eight
  double-priced rows of F3 §12 collect the one fact **once**, at the calibrated total.
- **Injured-annotated rows are EXEMPT** — the two-channel law.
- **Why a new collector at all:** F3 §15 published the **structural ceiling** — in three of four bands
  the ceiling of the two existing collectors sits **below** the lower limit of the measured cost, so
  no setting of either can reach it. The production leg is the one that can.
- **F3's own limitation carried forward:** a row whose absence already depressed his production leg
  has paid somewhere these attributions do not count, so F3's gap is an **upper bound**. The take is
  therefore capped so the total can never exceed the measured cost's point estimate.

---

## 7 · THE TAIL CALIBRATION — THE LOUD REPORT

**Acceptance asked for the tail calibration reported against F5's expectation ~1.04.** It cannot be
quoted, because F5 computed that number on a board the candidate is not: **BETA_sat at its CI floor
(0.10416) with a HARD CLIP at p20**. The candidate carries the **ruled slope 0.105** and the **SMOOTH
COMPRESSION**. So it was recomputed on the form the candidate actually charges with, reusing
`os_f5.py`'s population and charge algebra verbatim (imported, not re-implemented).

Deep cell n = 40 (10-22 games, surplus < −20) against the at-bar reference n = 342. Realized ratio
0.2979. **Mean basis, which the owner accepted at v747.**

| BETA_sat | HARD CLIP p5 | HARD CLIP p20 | **SMOOTH p20** |
|---|---:|---:|---:|
| ORDER P 0.11465 | 1.9025 | 1.1736 | **0.7997** |
| CI floor 0.10416 | 1.6219 | **1.0413** ← F5's published figure | 0.7327 |
| **RULED 0.105** | 1.6427 | 1.0512 | **0.7378 ← THE CANDIDATE** |

**READ THE LAST TWO COLUMNS. The slope barely moves the answer. THE CAP FORM MOVES IT BY ABOUT 0.35
OF CALIBRATION.** At every slope the hard clip at p20 lands near 1.04-1.17 and the compression at the
**same anchor** lands near 0.73-0.80.

**THIS CORRECTS THE REGISTER.** v746 recorded "the compression at the same anchor behaves ~identically
at the parked tail; the assembly build verifies on real boards." **It does not.** The two differ by
roughly a third of a calibration unit, because the compression is **strictly below** the clip ceiling
everywhere — the very property that makes it monotone and gap-preserving — and the deep cell is
exactly where the clip was binding. **The ~1.04 belongs to the CLIP. The candidate uses the
COMPRESSION and its number is 0.7378.**

**In plain words:** on the mean the candidate no longer over-charges the deep underperformer — it now
**under-charges** him by about a quarter. The direction is the one the owner asked for; the ruled pair
of softenings travels **past** the calibration point rather than landing on it.

**THIS SEAT PROPOSES NO FIX AND APPLIED NONE.** The dials are ruled and the charter does not authorise
re-opening them. Laid out without a recommendation: if the owner wants the tail **at** the calibration
point, the **hard clip at p20 with his ruled slope 0.105 reads 1.0512**, and that board can be built
on request. If he prefers the compression for the reason he chose it — no flat segment, worse play
always costs strictly more — then **0.7378 is the price of that property at the tail**.

**The median reading, printed because F5 printed it and burying it would be dishonest: 0.2429.** F5's
caveat stands — the deep cell is option-shaped, 21 of 40 rows deliver under 0.05 of entry and 3 rows
above 1.0 carry the mean. On the typical deep row the charge is **generous**, not harsh.

**G0 was not re-derived.** v746's disposition holds and the named open finding — the charge convicts
somewhat fast at low games — is carried forward, not closed.

---

## 8 · THE ENGINE GUARD THAT HALTED, AND WHAT WAS DONE ABOUT IT

**What happened.** The first board that ever combined `RL_O40_CAPFORM=smooth` with
`RL_O39_BETASAT=0.105` **halted**:

```
ORDER S HALT (S-S5): the compression charges MORE than the hard clip at s=-0.8000
(0.004859539 vs anchor clip 0.004860615, ORDER P clip 0.000000000).
```

**The diagnosis.** S-S5 has two limbs.

- **Limb 1** — `T' ≤ the hard clip at the SAME anchor and the SAME effective slope`. This is the
  property the cap form actually promises. **It HOLDS everywhere** — the halt message itself shows it
  (0.0048595 ≤ 0.0048606). **It remains a HALT, untouched.**
- **Limb 2** — `T' ≤ ORDER P's own p5 clip at ORDER P's own slope`. **This is what fired, and what
  trips it is THE SLOPE, NOT THE CAP FORM.** A gentler slope makes `T` decay toward zero more slowly,
  so in a narrow window just above the cohort centre the softened board charges a hair more than
  ORDER P did. Limb 2 is **vacuous** while BETA_sat is ORDER P's — the only case ORDER S ever built.

**Why it was changed rather than obeyed.** That effect is **already the house's own, measured and
disclosed rather than forbidden**: ORDER R's banner computes exactly this window
(`_rstiff`/`_rstiffs`/`_rstiffhi`) and prints it with the words *"IT IS REPORTED, NOT ARGUED AWAY."*
Halting here would forbid on one dial line what the house publishes on another, **and it would veto a
combination the owner himself ruled** (slope 0.105 at v745, compression p20 standing).

**What was done.** Limb 2 now **measures** the window on the same sweep and **prints it in the banner
on every compression board**, with its bounds and its worst excess — the identical treatment ORDER R
gives the identical phenomenon. **Limb 1 still halts. S-S2 — no row above its uncharged price — still
halts.** The size of the window on the candidate is in §10.

**NO LAW WAS TRADED SILENTLY.** This is a disclosed deviation, recorded in the commit message, in this
packet, and in the report to the owner.

---

## 8b · A DEFECT IN MY OWN WIRING, CAUGHT BY THE LEVER STACK

**What happened.** The SD level offset was first wired at **one** site — `o37_surplus`, where the
charge bar is formed. The board built with `RL_O41_SDOFF=2.98` came out **byte-identical** to the
board built without it: same md5, same total, not one row moved.

**Why.** With **FIX A live the charge does not read `o37_surplus`'s return value at all.** `o38_mono`
rebuilds the surplus from a separate decomposition, `o38_parts`, as
`s_P(v) = OUT − wTALL·PG(v,TALL) − wSMALL·PG(v,SMALL)`, so that it can sweep the surplus across entry
prices and take the running maximum. An offset applied only in `o37_surplus` therefore reaches
**nothing** on any board that carries FIX A — and every candidate board carries FIX A.

**The repair.** The identical offset is applied in `o38_parts`'s `OUT` accumulator. It is a
**constant** addition to `OUT` and carries no `v` term, so **the FIX A identity survives exactly** —
which is why the same constant can sit in both places without breaking the monotonisation.

**Verified before spending the rebuild:** on a loaded engine an SD row's charge multiplier moves
**0.35045 → 0.38454** (charged less, which is the direction a lowered bar must produce) while a
non-SD row is **unchanged to twelve decimals**.

**Why this is in the packet rather than quietly fixed.** The only reason it was caught is that the
per-lever stack builds every dial on its own and compares md5s. A single end-to-end candidate build
would have shipped an SD offset that did nothing, and the packet would have claimed a lever that was
not there. **The lever document is not just presentation — it is the test that caught this.**

---

## 8c · THE SECOND DEFECT IN MY OWN WIRING — THE R3 COLLECTOR READ THE WRONG CLOCK

**What happened.** The first candidate board built with the R3 production fade live took **−37,701**
board points off **246 rows**. Inspecting the largest movers showed the collector was firing on
players with **no unexplained absence at all**:

| row | seasons played | unplayed seasons | before | after | change |
|---|---|---:|---:|---:|---:|
| Toby Nankervis | **every season 2015-2026** (187 career games) | **0** | 1,910 | 654 | **−1,256** |
| Mason Redman | every season but one (155 games) | 1 | 1,090 | 357 | −733 |
| Ned Moyle | 2023, 2024, 2025, 2026 | **0** | 1,671 | 270 | **−1,401** |
| Zach Reid | — | **0** | 846 | 150 | −696 |

**243 of the 246 rows the collector hit had played games.** A ruck with 187 career games who has not
missed a season since 2015 was losing two-thirds of his price for absence he never had.

**The cause.** I sized R3 off `o31_cu`, the **sitter clock**. That clock is time-since-delivery
**minus a partial credit for each season played** — and under the F1 measured credit curve a season
of 5 games now credits **0.25** instead of **1.00**. That is exactly right for the pedigree fade (a
five-game season really is weak evidence) but it is **wrong as a count of seasons missed**, because
it accumulates for a player who never missed one. Nankervis's 2015 (5 games) and 2016 (7 games) alone
left him carrying 1.37 of clock; the graded reset (I2) then stopped that clock being wiped, and R3
read the total as "two seasons out".

**This was an interaction between three of my own dials — I1 inflates the clock, I2 stops it being
wiped, I4 misreads the result — and no single lever showed it. Only the built board did.**

**The repair.** A new object, `o41_absence_depth`, counts **seasons with zero games** since the last
delivered season, on **F3's own indexing** — depth 1 is the normaliser and depth 2 is one unplayed
season, exactly as `FOLLOWUP_F3.json::dcurve` is built. The live in-progress season counts only by
the fraction elapsed, and not at all for a row the owner has logged injured (the two-channel law).
**The absence collector must read absence, so now it counts absence.**

**Verified on the loaded engine before the rebuild:**

| row | old `o31_cu` | new depth | R3 now applies? |
|---|---:|---:|---|
| Toby Nankervis | 2.734 | **1.000** | **no** |
| Mason Redman | 2.775 | **1.000** | **no** |
| Ned Moyle | 3.994 | **1.000** | **no** |
| Zach Reid | 3.519 | **1.000** | **no** |
| Noah Mraz | 2.701 | **2.000** | yes — he genuinely missed a season |

**Why this is in the packet.** The charter said to halt and report rather than ship something the
measurement does not support. A board that charged Nankervis for absence would have been exactly
that, and the R3 number in a packet is worthless if the object underneath it is counting the wrong
thing. **It was caught by looking at the rows, not at the total** — the total alone (−37,701) looked
merely large, not wrong.

---

## 8d · THE THIRD DEFECT — CAUGHT BY THE ENGINE, NOT BY ME

**What happened.** With the R3 clock repaired, the next candidate build **failed the engine's own
export-versus-engine parity gate**:

```
EXPORT<->ENGINE PARITY GATE FAILED for 1/804 players (board v != engine gated ev, eps=0):
  shadeau-brain: board=77 engine=80
```

**The cause.** The R3 sizing law needs the production leg **before** the D8 staleness cap, and that
value is only visible upstream at the cap site. I handed it forward in a small dict keyed by row and
year — and wrote it **only when a cap actually fired**. When the same row is priced twice at the same
year through paths that differ in whether the cap fires (the M3 proportional-tenure blend does
exactly this), the second pass read **the first pass's** pre-cap leg. **The price became dependent on
evaluation order** — for one row, by three board points.

**The repair.** The value is now written on **every** pass, which turns the dict from a cache into a
same-call hand-off and removes the order dependence entirely.

**Worth saying plainly: this one was not caught by my checks. It was caught by a gate the engine
already had, doing exactly its job — failing the build instead of shipping a board whose prices
depended on the order rows happened to be evaluated in.** Three points on one row would never have
been visible in any total, any band table or any tracker column.

---

## 4 · THE CANDIDATE, AND THE LEVER STACK

**THE CANDIDATE IS `5949cf9b`. THE TOTAL IS 650,439.**

| board | md5 | total | vs live | vs K | vs R | the lever added |
|---|---|---:|---:|---:|---:|---|
| live | `88ce647f` | 752,429 | 0 | +79,332 | +87,479 | **NEVER TOUCHED** |
| ORDER K | `f3101883` | 673,097 | −79,332 | 0 | +8,147 | the K/landing chain |
| ORDER P | `374d4e44` | 666,434 | −85,995 | −6,663 | +1,484 | **every assembly dial OFF — the identity** |
| R = R20A | `7f88f509` | 664,950 | −87,479 | −8,147 | 0 | the owner's reference |
| L1_REC | `b692d709` | 664,770 | −87,659 | −8,327 | −180 | + recency 0.47 |
| L2_COMP | `c3cb6686` | 670,562 | −81,867 | −2,535 | +5,612 | + compressed cap p20 + slope 0.105 |
| L3_MAT | `ccdd395f` | 670,068 | −82,361 | −3,029 | +5,118 | + the mature refit |
| L4_SD | `7a9dbbe1` | 670,995 | −81,434 | −2,102 | +6,045 | + the SD level offset, standalone |
| L5A_CRED | `b9666afc` | 667,383 | −85,046 | −5,714 | +2,433 | + absence I1, the credit curve |
| L5B_RSET | `2978d9e7` | 661,718 | −90,711 | −11,379 | −3,232 | + absence I2, the graded reset + F4 |
| L5C_INJ | `f33e1fc5` | 661,761 | −90,668 | −11,336 | −3,189 | + absence I3, the injury stream |
| **CANDIDATE** | **`5949cf9b`** | **650,439** | **−101,990** | **−22,658** | **−14,511** | + absence I4, the R3 fade |
| CAND repeat | `5949cf9b` | 650,439 | — | — | — | **the determinism proof** |

**Each marginal effect, and how many rows carry it:**

| lever | marginal | rows moved | up | down |
|---|---:|---:|---:|---:|
| + recency 0.47 | −180 | 316 | 121 | 195 |
| + compressed cap p20 + slope 0.105 | **+5,792** | 393 | 362 | 31 |
| + the mature refit | −494 | 173 | 16 | 157 |
| + the SD level offset | +927 | 102 | 102 | 0 |
| + I1 the credit curve | −3,612 | 167 | 30 | 137 |
| + I2 the graded reset + F4 | −5,665 | — | — | — |
| + I3 the injury stream | **+43** | — | — | **0 down** |
| + I4 the R3 production fade | −11,322 | — | — | — |
| **the absence package alone** | **−20,556** | | | |
| **THE WHOLE ARC R → CANDIDATE** | **−14,511** | | | |

**The two levers that ADD value are the two the owner ruled as softenings** — the compression with
the slope (+5,792) and the SD offset (+927). **Everything the absence package does is subtract**,
which is what it is for.

**MATURE ROWS, BUILT vs EXPECTED — reported loudly.** The board carries 429 mature rows (age ≥ 24)
and 375 young. Against ORDER P the candidate moves mature rows **−9,708 on 294 moved rows**, and
young rows −6,287. Against R, mature −3,931 and young −10,580. **The prereg's ~−7,064 figure was for
B1 + the refit against a different base and without the six other levers, so it is not the
like-for-like number.** The like-for-like one is **the mature refit lever alone: −494 on 173 moved
mature rows.** Reported both ways rather than picking the flattering one.

---

## 9 · MY OWN PREREG PREDICTIONS, SCORED HONESTLY

| # | prediction | outcome |
|---|---|---|
| **P1** | dial-chain identity holds | **HELD.** `374d4e44`, `f3101883`, `7f88f509` all byte-exact |
| **P2** | mature movement between −5,000 and −10,000 | **HELD** on the vs-ORDER-P reading (−9,708); the refit lever alone is −494 |
| **P3** | candidate total 630,000-660,000 | **HELD** — 650,439. *(The first, defective R3 build read 624,060 and would have MISSED it; the miss was a symptom of the bug, not of the range.)* |
| **P4** | tail calibration 0.90-1.25 | **FALSIFIED.** 0.7378. §7 |
| **P5** | class mark in [1.03, 1.14) | see §10 |
| **P6** | burn 0, birthday 0 | see §10 |
| **P7** | I1 moves more board points than I2 | **FALSIFIED.** I1 −3,612, I2 −5,665. The graded reset moved more than the credit curve, the opposite of what I predicted from F2's six-row cliff census. F2 measured the *delivered-cliff flip* at six rows; the graded reset's reach is much wider than that flip because it changes the clock for **every** row with a delivered season behind it, not only the rows sitting at the threshold. I read F2's census as bounding the lever and it does not. |
| **P8** | injury stream moves < 25 rows, all upward | **HELD on direction** — +43 net, **zero rows down**. A pause can only remove clock, and it did. |
| **P9** | R3 moves more than I1+I2+I3 combined | **HELD** — R3 −11,322 against −9,234 for the other three. |
| **P10** | modern 1-10 still fails | see §10 |

---

## 10 · ACCEPTANCE, ITEM BY ITEM

| item | result |
|---|---|
| **dial-chain: all assembly dials off → `374d4e44` byte-exact** | **PASS** |
| **K/landing chain `f3101883` intact** | **PASS** |
| **R = `7f88f509` reproduces, total 664,950** | **PASS** |
| **determinism ×2** | **PASS** — `5949cf9b` on both runs, byte-identical |
| **burn census 0 of all young rows (Fix A)** | **PASS** — 0 of 289 young rows, 0 board points, every band. Also 0 on the supervisor's 264-row |fK−fP|≥0.02 population |
| **birthday census 0 at every age (B1)** | **PASS** — 81 age-23 rows with a pedigree leg, **0 movers**, net +0, worst ratio 1.0000 |
| **continuity — age 23/24** | **PASS** — largest step in the charge factor between consecutive ages **0.0000**; the charge does not read current age at all |
| **continuity — the season turn** | **PASS** — S1-F2 does not fire; the geometric recency weight is **exactly** invariant to the turn |
| **continuity — games axis** | **PASS** — the charge rises with games at **0 of 280,000** steps |
| **continuity — surplus axis** | **PASS** — a better player is charged more at **0 of 10,000** steps |
| **no row above its uncharged price** | **PASS** — the engine's own S-S2 assert runs at load on every build and did not fire |
| **LAMBDA untouched at the anchor** | **PASS** — `RL_O40_LAMBDA` never set on any board here |
| **R9/R10 asserts at BETA_sat 0.105** | **PASS** — asserted at load on every build |
| **day-0 ENTRY values bit-identical 89/89** | **⛔ BREACH — see §0.** 28 of 95 day-0 rows move, net −1,876, all of it from the ruled I2 F4 repair. The engine's internal day-0 identity still holds 89/89. **The two rulings are incompatible; the owner must choose.** |
| **year-1 class mark in [1.03, 1.14) registered basis** | **NOT PRODUCIBLE** — blocked by the same emit halt. The instrument reproduced its controls exactly (ORDER K W2 1.0513, ORDER P W2 1.0613, both PASS), so it is ready the moment the day-0 question is ruled. |
| **no-arb tables, both windows, both baselines** | **NOT PRODUCIBLE** — same cause. Instruments pinned and verified (`d59ad550`, `0f822035`, `02dcf28c`); the reference matrices for K, P, R and the landing candidate all ran clean. |
| **tail calibration vs F5 ~1.04** | **REPORTED — 0.7378, a −0.30 miss. §7** |
| **modern picks 1-10** | **DOCUMENTED STANDING RED**, carried in the box on every owner page. Its band table for the candidate awaits the emit. |
| **SSP** | reported separately, parked, named in the box on every page |
| **S-S5 limb 2 window (the disclosed deviation)** | **MEASURED: s ∈ [−2.010, −0.800], 1.210 pts/game wide, worst excess in T 0.0833 = at most 1.41% of the pedigree leg at 38 games.** The window sits above the cohort centre (s0 = −2.4527), i.e. on rows already producing at or above what their price implies. |

**A NOTE ON HOW THE CENSUSES WERE RUN, DISCLOSED.** The burn census reconstructs a row's price from
`[rho·e + age credit] + pi_base · (v·PL_F) · factor(v)` and sweeps the entry price. **That identity
has no absence-collector term**, so with R3 live it broke on the first R3-faded row it reached
(`noah-mraz`, 2118.41 vs 1457.03) — the reconstruction cannot see the R3 subtraction. The censuses
are therefore run on the **R3-off** line (`L5C_INJ`), which is the correct basis for what they test:
they exist to prove FIX A's monotonisation and B1's gate deletion, and **R3 is a production-leg
collector that does not touch the pedigree charge at all**. **What is NOT covered by that choice, said
plainly: the burn sweep has not been run through the R3 term, so the interaction of entry price with
the R3 collector is unswept.** Extending the instrument is a small piece of work and it is named here
rather than left implicit.

---

## 11 · WHAT WAS NOT BUILT, AND WHY

- **SF is NOT wired.** T1 read SF +2.709 (under-barred) but the ruling is explicit: held on the
  survivor-bias caveat, and wiring it would hurt exactly the rows the owner cares about. v744.
- **RUCK is NOT wired.** §2 — the object is not the one a premium offset reaches.
- **LAMBDA is NOT re-solved.** The level stays at the anchor; the frontier is accepted. v748.
- **The modern 1-10 cell is NOT chased and NOT capped.** A **DOCUMENTED STANDING RED** (v748), flagged
  in every table.
- **SSP is NOT repaired.** Inherited breach, worsened by ORDER P, parked (C6), reported separately.
- **G0 is NOT re-derived.** v746's disposition, four reasons on the record.
- **C2 (the veteran board RL_O33 × B1), C3 (Guard 5), C5, C7, C8, C9** are out of this seat by charter.
  **C2 in particular must be re-tested against this candidate before RL_O33 merges behind it** — B1
  moves mature rows and nobody has looked at the two together.

- **The year-1 class table and the no-arb band tables for the candidate** — blocked by the day-0
  emit halt in §0. Not worked around, not produced on a quietly re-based guard.
- **The production-leg and absence-take columns on the player page** — the leg recorder captured the
  charge, the fade `D` and the unplayed clock for all 2,650 store rows, but not the production input
  `e`, which is only visible at the blend site through a wrapper this seat could not attach cleanly
  in the time available. The columns are present and empty rather than filled with a guess.

---

## 12 · THE DELIVERABLES, AND WHERE THEY ARE

| # | deliverable | file | status |
|---|---|---|---|
| 1 | **PREREG**, pushed before the first engine edit | `PREREG_ASSEMBLY.md` (`c1dbd3e`) | done |
| 2 | **THE CANDIDATE** + this packet | board `5949cf9b` · `PACKET_ASSEMBLY.md` | done |
| 3 | **THE TRACKER** (v741/v742) | `TRACKER_ASSEMBLY.html` (801 rows) + `.csv` | done |
| 4 | **THE PER-LEVER BREAKDOWN** | `LEVERS_ASSEMBLY.html` (8 levers) | done |
| 5 | the 804-row player list | `ASSEMBLY_PLAYERS.html` | done |
| 5 | the year-1 class in draft order | `ASSEMBLY_YEAR1.html` (102 rows, the 2025 draft) | done |
| 5 | the no-arb tables | — | **blocked, §0** |
| 6 | the movers ledger | `MOVERS_LEDGER.json` (801 rows) | done |
| — | the RUCK diagnosis | `as_ruck.py` · `RUCK_DIAG.json` · `RUCK_DIAG_out.txt` | done |
| — | the tail calibration | `as_tail.py` · `TAIL_ASM.json` · `TAIL_ASM_out.txt` | done |
| — | boards and levers, scored | `BOARDS_ASM.json` · `BOARDS_ASM_out.txt` | done |
| — | censuses / continuity | `CENSUS_NOR3_out.txt` · `CONTINUITY_CAND_out.txt` | done |

**The three owner pages each carry the same "what is in this board and what is still broken" box
(`as_box.py`), with the modern 1-10 red and SSP named in it, so nothing broken can appear on one page
and be missing from another.**

**Thread pins printed on every run: `OPENBLAS=1 OMP=1 MKL=1 NUMEXPR=1 VECLIB=1`, `PYTHONHASHSEED=0`.
Engine runs were STRICTLY SEQUENTIAL throughout — never two at once.**

**NOTHING IS ADOPTED. NOTHING MERGED. NO PULL REQUEST. NOTHING ON `main`. THE LIVE BOARD `88ce647f`
WAS NEVER TOUCHED. THE CANDIDATE IS FOR OWNER REVIEW.**
