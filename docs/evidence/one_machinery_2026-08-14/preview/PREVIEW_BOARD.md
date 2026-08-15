# THE STEP-3 PREVIEW BOARD — READ THIS FIRST

**ORDER 30B-P · preview seat · `land/order-29` · 2026-08-15 · brief #334 comment `5299562714`.**

> ## NOTHING IS GREENLIT.
> The Step-3 forbidden-set boundary word (STOP §5 Q1–Q4) is still **OPEN**. This order wires the
> seat-recommended configuration **behind one new declared dial, `RL_O30B_PREVIEW`, default OFF**, so the
> owner can rule from a board instead of from prose. **With the dial off, the committed Step-2 board
> `9298203135202a0c707bb0977ba38c31` reproduces BYTE-EXACT.**
>
> ## THE PREVIEW IS PRE-NUMERAIRE.
> Step 6's re-pin has **not** run. Every table this order emits says so on its face. **Read the movement,
> not the level.** Steps 4–7 are not started. No pool value is derived. PR #510 stays **HELD**.

| | |
|---|---|
| **PREVIEW BOARD** | **`6a392bca7ad0dee04a6b4f037c758f65`** |
| total | **679,875** — vs Step-2 706,672 (**−26,797, −3.79%**); vs live `88ce647f` 752,429 (**−72,554, −9.64%**) |
| movers vs Step-2 | **678 of 804**. The **89 day-0 rows move zero.** |
| determinism | **three** independent builds from freshly staged trees, all **`6a392bca7ad0dee04a6b4f037c758f65`** |
| dial-off control | **`9298203135202a0c707bb0977ba38c31` byte-exact**, twice |
| printed-day-0 | **89 of 89, tolerance 0**, under the preview |
| prereg | **10 HELD, 5 BREACHED** (P6, P7, P8-second-leg, P10, P12) — every breach owned in §6 |

**The deliverables.** `PREVIEW_MOVERS.{md,json}` (all 804 rows) · `AGE_LENS.{md,json}` ·
`COUNTERFACTUAL.md` · `PREREG_30BP.md` (filed and pushed before any preview quantity existed).

---

## 1 · WHAT IS WIRED, IN ONE SCREEN

For a row that **has evidence** at `Y`:

```
price = (1 - sigma(g)) x production  +  sigma(g) x pedigree
```

| element | the exact object | where |
|---|---|---|
| the dial | `RL_O30B_PREVIEW`, default `0`. It **IMPLIES** `_O30B_NOPOLE` and `_O30B_NOISO` by `or` — so the pole and the par-built ISO pick-tax are deleted **through the two existing ablation lines** and **no third deletion path exists**. | `:409-411`, `:487`, `:517` |
| `production` | the finished production leg: pole deleted, ISO deleted, **retained** form machinery applied (ITEM H's ruled cuts, the ruck ceiling, the KPF compression, D8 graded staleness, the decay gate). | blend site in `ev()` |
| `pedigree` | the **STEP-1 positional v0** `day0_v0(p)` × `_PL_F` = 1.0524. ND: `nd_v0.posv[gfut][pick]`. Pool: the signed `pool_v0` cell through `MA.pool_v0_of` (halts on an unsigned cell). **The numéraire `s` is already inside both**, so BOARD→ENGINE is the only conversion — the identical conversion ORDER 29B's own day-0 branch performs. | `pv_pedigree` |
| `sigma(g)` | `exp(-(g/23.0)^0.80)` — the 30B-M packet §6 **refit of ruling 4's own functional form** to the five measured band midpoints. | `sigma30bp` |
| `g` | career games as of `Y`. **Ruling 5:** an MSD entry season is credited at `cp.SEASON/12` per game. | `pv_games` |
| Q + decay gate | **RETAINED**, form/clip/constants unchanged, **denominator re-referenced** from `PR.par_at(pos, effpk, T)` to the **effective positional bar** `MA.REPL[pos] − rd.REPL_DROP[pos]` — position-level, **pick-blind**, the object 30B-M read live off the engine and asserted against Ruling 1. | `_c_w`, `ev` |
| replace-not-wrap | `_a_blend`, `sitout_ev`'s `ns==0` arm and the year-zero floor `floor_frac × entry_anchor` are **REPLACED**, not wrapped. | STOP §5 Q4 |
| no stacking | zero-evidence rows are intercepted by `_entry30b_price` **above** this lane and keep the Step-2 fade untouched; a played row carries an **unfaded** pedigree leg at weight `σ(g)`. The two branches are **mutually exclusive by predicate**, so `(1−w)` and `D` can never multiply. | |

### THE INTERPOLATION, STATED

`σ` is the **two-parameter interpolant of the five measured band midpoints** in the family ruling 4 ruled:

| games (band midpoint) | 2.5 | 10.5 | 25.5 | 53.0 | 85.5 |
|---|---:|---:|---:|---:|---:|
| **measured σ** | 70.1% | 66.4% | 33.1% | 16.5% | 2.2% |
| **σ wired here** (τ 23.0, β 0.80) | 84.4% | 58.6% | 33.8% | 14.2% | 5.7% |

It is used rather than a raw point-to-point rule because it is the **ruled functional form**, it is
monotone and smooth everywhere, and it is defined below 2.5 and above 85.5 games. **Its known residuals —
hot at the shallow end, hot again past 71 games — are carried unchanged, not patched.** The raw log-linear
midpoint interpolation is published beside it as `sigma30bp_raw` and is **not wired**; the difference it
would make to the named rows is **≤ 103 board points** (`CHECKS_out.txt` §5), so the choice is **not
load-bearing**.

---

## 2 · THE ONE THING THE OWNER MUST SEE BEFORE ANYTHING ELSE — **THE TWO READINGS OF "THE PEDIGREE SHARE"**

The brief's no-stacking constraint says *"pedigree/total = σ(games)"*. **There are two objects that phrase
can name, they are not equal, and the seat is not going to let one stand in for the other.**

| reading | what it is | is it σ? |
|---|---|---|
| the **WEIGHT** share | `σ(g)` — the coefficient on the pedigree leg | **EXACT, by construction, for every blended row** |
| the **VALUE** share | `σ(g) × v0 / printed price` — what fraction of the printed number the pedigree leg actually is | **NOT σ** unless `v0` happens to equal the price |

**What is wired is the WEIGHT reading**, because that is the object the 30B-M packet §6 refit was fitted
to: the packet refits `1 − w(g) = exp(−(g/τ)^β)` **against the measured σ points**, i.e. it identifies
`(1 − w)` with σ. The measured VALUE share that results:

| games class | n | σ (weight), median | **VALUE share, median** | range |
|---|---:|---:|---:|---|
| cg 1–5 | 60 | 0.8220 | **0.7867** | 0.230 … 1.000 |
| cg 6–15 | 87 | 0.5745 | **0.6272** | 0.141 … 1.001 |
| cg 16–35 | 104 | 0.3434 | **0.4893** | 0.043 … 0.996 |
| cg 36–70 | 111 | 0.1382 | **0.1668** | 0.007 … 0.990 |
| cg 71+ | 353 | 0.0122 | **0.0168** | 0.000 … 1.023 |
| **whole blended book** | 715 | — | **0.1342** (88,942 pedigree points of 662,631 printed) | |

**If the owner meant the VALUE reading, the calibration is different and the seat has not built it.**
Solving `(1−w)·V / [w·P + (1−w)·V] = σ` gives a **harmonic** blend, `1/price = (1−σ)/P + σ/V`, not the
arithmetic one the brief writes down as `price = w·production + (1−w)·pedigree_term`. **The brief writes
the arithmetic form and the packet's refit identifies `(1−w)` with σ, so the seat wired that** — and
reports the value share so the owner can see the difference rather than discover it later. **Which reading
is meant is an owed word.**

---

## 3 · THE BOARD

### 3.1 By career-games class (vs Step-2)

| cg class | movers | sum Δ |
|---|---:|---:|
| 1–2 | 26 | **+5,922** |
| 3–5 | 34 | +1,129 |
| 6–10 | 47 | −1,038 |
| 11–15 | 39 | −3,451 |
| **16–35** | **103** | **−11,751** |
| **36–70** | **110** | **−10,392** |
| **71+** | **319** | **−7,216** |

**The preview cuts the young established book hardest and lifts the barely-played.** `cg 16–70` alone is
**−22,143 over 213 rows**; `cg 1–5` is **+7,051 over 60 rows**.

### 3.2 By pathway (vs Step-2)

| ND | RD | MSD * | SSP * | PDA * | PDN * | IRE * | UNR * |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 513 (−18,378) | 49 (−2,506) | 56 (−1,782) | 27 (−1,804) | 12 (−1,549) | 8 (−630) | 7 (−10) | 6 (−138) |

`*` **provisional — pool values pending Step 4.** Pool rows are priced under the **same** formula with
their **own** signed pool `v0` cells and the same σ curve; the pool fade and the pathway-specific
derivations are Step 4's and have not run.

### 3.3 The top 20 by |Δ| vs Step-2

| key | name | path | pick | pos | age | games | LIVE | STEP-2 | **PREVIEW** | Δ | % |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| `toby-conway` | Toby Conway | ND | 24 | RUCK | 23 | 6 | 503 | 433 | **1420** | **+987** | +227.9% |
| `dyson-sharp` | Dyson Sharp | ND | 13 | MID | 19 | 13 | 3091 | 3269 | **2347** | −922 | −28.2% |
| `josh-lindsay` | Josh Lindsay | ND | 19 | SD | 19 | 13 | 2335 | 2479 | **1573** | −906 | −36.5% |
| `harry-barnett` | Harry Barnett | ND | 23 | RUCK | 22 | 2 | 553 | 469 | **1345** | +876 | +186.8% |
| `will-green` | Will Green | ND | 16 | RUCK | 21 | 1 | 604 | 489 | **1324** | +835 | +170.8% |
| `nick-madden` * | Nick Madden | PDA | — | RUCK | 22 | 10 | 1766 | 1650 | **867** | −783 | −47.5% |
| `archie-roberts` | Archie Roberts | ND | 54 | SD | 21 | 46 | 4726 | 4415 | **3642** | −773 | −17.5% |
| `taylor-goad` | Taylor Goad | ND | 20 | RUCK | 21 | 2 | 730 | 597 | **1370** | +773 | +129.5% |
| `sullivan-robey` | Sullivan Robey | ND | 9 | MID | 19 | 14 | 2981 | 3158 | **2397** | −761 | −24.1% |
| `sid-draper` | Sid Draper | ND | 4 | MID | 20 | 10 | 1250 | 1155 | **1906** | +751 | +65.0% |
| `jagga-smith` | Jagga Smith | ND | 3 | MID | 20 | 20 | 4855 | 4533 | **3822** | −711 | −15.7% |
| `jacob-farrow` | Jacob Farrow | ND | 10 | SD | 19 | 18 | 2601 | 2765 | **2089** | −676 | −24.4% |
| `alix-tauru` | Alix Tauru | ND | 10 | KPD | 20 | 18 | 1684 | 1572 | **903** | −669 | −42.6% |
| `murphy-reid` | Murphy Reid | ND | 17 | SF | 20 | 45 | 4141 | 3868 | **3251** | −617 | −16.0% |
| `zeke-uwland` | Zeke Uwland | ND | 2 | SD | 19 | 17 | 2633 | 2509 | **1906** | −603 | −24.0% |
| `mitchell-edwards` | Mitchell Edwards | ND | 32 | RUCK | 21 | 16 | 2439 | 2279 | **1686** | −593 | −26.0% |
| **`isaac-kako`** | **Isaac Kako** | **ND** | **13** | **SF** | **20** | **36** | **1413** | **1320** | **748** | **−572** | **−43.3%** |
| `patrick-retschko` | Patrick Retschko | RD | 8 | MID | 20 | 16 | 1608 | 1501 | **931** | −570 | −38.0% |
| `sam-darcy` | Sam Darcy | ND | 2 | KPF | 23 | 51 | 5250 | 4903 | **4365** | −538 | −11.0% |
| `xavier-taylor` | Xavier Taylor | ND | 11 | SD | 19 | 2 | 802 | 735 | **1247** | +512 | +69.7% |

**The shape of the whole board in one line: the movers up are barely-played high-`v0` rows (four rucks in
the top ten), and the movers down are young established rows in their second and third seasons.**

---

## 4 · THE FIVE FINDINGS THE OWNER'S RULING TURNS ON

**(1) THE FIRST GAME IS A CLIFF, AND RULING 6's CONTINUITY CURVE FAILS AT IT.** The no-stacking constraint
as stated sends a gameless row to `v0 × D(c)` and a one-game row to `σ(1)×v0 + …` with **σ(1) = 0.9218**.
Measured on the preview engine: `josh-smillie` **471 → 1671 (+254.8%)**, `harry-demattia` **301 → 878
(+191.7%)**, `max-knobel` **287 → 823 (+186.8%)**, `dyson-sharp` **895 → 1581 (+76.6%)** — and the price is
**non-monotone in evidence** in three of the four. **This is a property of the constraint, not of the
implementation, and the seat has not smoothed it.** Full curves: `COUNTERFACTUAL.md` §3.

**(2) THE MEASURED PEDIGREE SHARE PAYS THE YOUNG BOOK *LESS* THAN THE MACHINERY IT REPLACES.** Against
ablation B (pole+ISO deleted, **no** blend, ITEM A and the floor still in), the blend moves:

| cg | n | sum under ablation B | **PREVIEW − ablation B** | per row |
|---|---:|---:|---:|---:|
| 1–5 | 60 | 23,048 | **+7,350** | +122.5 |
| 6–15 | 87 | 45,603 | **−2,926** | −33.6 |
| 16–35 | 104 | 69,959 | **−3,188** | −30.7 |
| 36–70 | 111 | 116,002 | **−5,364** | −48.3 |
| 71+ | 353 | 417,909 | **−5,762** | −16.3 |

**Everywhere past 5 games, replacing ITEM A's anchor carry and the year-zero floor with the *measured*
σ-weighted `v0` leg takes MORE out than the pedigree leg puts back.** The reason is an object mismatch
worth naming: **ITEM A and the floor lean on `entry_anchor` (`v0_start`, the D14 V0 curve) while the blend's
pedigree leg is the STEP-1 positional `v0`, and for the rows in question the first is much larger.**
kako: `entry_anchor` **1069.0** against Step-1 `v0` **759.8**. The 30B-M measurement said the *share* was
too low; it did not say which `v0` object the share should be a share **of**. **That is an owed word.**

**(3) kako PRINTS 748, NOT 900–1000 — AND THE SEAT PREDICTED THE BREACH BEFORE BUILDING.** P7's band came
from the brief; the seat's blind note in the prereg said the band required a production leg of ~945–1075
and that ablation B's 744 was an upper bound. Measured: production **744.3**, pedigree **181.7**, price
**748**. **P7 BREACHED LOW, owned, nothing re-tuned.**

**(4) THE DECAY-GATE BOUNDARY QUESTION (STOP §5 Q3) IS WORTH ZERO BOARD POINTS IN THIS CONFIGURATION.**
Only two rows ever reached the gate under the par denominator (`campbell-chesser`, `finlay-macrae`), and
re-referencing removes both (`pr` 0.5397 → 0.5759 and 0.5316 → 0.5720, against the 0.55 threshold). **But
the gate would not have cut them anyway**: with the pole and ISO deleted their production legs are **216.2
and 43.1** engine points against a gate cap of **486.6 and 362.7**, so `min()` is a no-op. **The same
preview configuration with the par denominator retained prints them at exactly 434 and 403 — identical.**
`P10 BREACHED` (the seat predicted they would print higher), and the *useful* answer is better than the
prediction: **Q3 can be ruled either way for free.**

**(5) AGE-AT-STATE MOVES THE PICK GAP AT 16–35 GAMES — AND NOT AT 36–70, WHICH IS THE OWNER'S OWN EXAMPLE.**
At 16–35 games the ≤20 cell's matched pick contrast is **+362.7** and the 24+ cell's is **−170.2**;
difference **+532.9**, 90% interval **[+184.2, +881.7]**, z **+2.51** — **separated**. At 36–70 games the
difference is **+286.2** with an interval spanning zero. **Nothing is applied.** Full caveats (the interval
is **not** cluster-robust, the separating cell is n = 82 over 4 strata, and the age/games confound has a
name) and the wiring implication as an **owed word** are in `AGE_LENS.md`.

---

## 5 · CONTROLS CLOSED

| control | result |
|---|---|
| dial-off byte identity | **`9298203135202a0c707bb0977ba38c31` byte-exact**, dial present and unset — run **twice** (`bb_dialoff`, `bb_dialoff2`, either side of a comment-only cleanup) |
| determinism double-build | **three** independent staged builds (`bb_prevA`, `bb_prevB`, `bb_prevC`) → **`6a392bca7ad0dee04a6b4f037c758f65`** every time |
| ops disclosure | one build was first attempted **detached** and was killed mid-export; it wrote **no board** and was re-run in the foreground. Every scored build is a foreground, sequential engine run under the pinned five-var environment. |
| printed-day-0 identity | **89 of 89, tolerance 0** under the preview; **0 of the 89 day-0 rows move** |
| population | **804 rows, zero population change**; 715 blended, 89 on the Step-2 fade |
| pedigree-object coverage | **715 of 715** blended rows have a `day0_v0` object; the fallback is a **halt**, not a default |
| lane scope | `git diff 3e5c581..HEAD -- engine/ data/` = **`_merged_recover.py` only**. Store, `v0surf.pkl`, `pvc_curve_v2.json`, `rl_model.py`, every committed board: **unmoved** |
| numéraire | **not re-pinned.** Shipped pick-1 = 3000, numéraire guard PASS |

---

## 6 · PREREG SCORED BY NUMBER — BREACHES OWNED

| # | verdict | reading |
|---|---|---|
| **P1** | **HELD** | dial-off reproduces `92982031` byte-exact |
| **P2** | **HELD** | printed-day-0 **89 of 89, tolerance 0**; **0 of 89** day-0 rows move |
| **P3** | **HELD** | two builds, both `6a392bca7ad0dee04a6b4f037c758f65` |
| **P4** | **HELD** | 715 blended / 89 fade / 804 rows; zero population change |
| **P5** | **HELD** | total **679,875**, inside [640,000 , 730,000]; direction **DOWN** as predicted |
| **P6** | **BREACHED** | predicted ≥ 700 movers; measured **678**. **37 of the 715 blended rows round to the same integer.** A small breach and it is the seat's arithmetic that was wrong, not the board |
| **P7** | **BREACHED (LOW)** | the brief's kako band 900–1000; measured **748**. **The seat filed the breach in advance** with the arithmetic that predicted it (prereg P7 seat note). Nothing re-tuned |
| **P8** | **FIRST LEG HELD, SECOND LEG BREACHED** | `cg 16+` carries **532 of 678 movers (78.5%)** and the majority of the summed delta — **HELD**. But `cg 6–70` moves **DOWN** against ablation B (−2,926 / −3,188 / −5,364), not up — **BREACHED**, and it is finding (2) above |
| **P9** | **HELD** | at-bar class (`cg 16–70`, career average within 10% of its positional bar, n 40) median **\|Δ%\| 10.12**; star class (`cg 100+`, top-decile price, n 36) median **0.83**. The at-bar class re-references; the star class barely moves |
| **P10** | **BREACHED** | predicted the two gate rows print **higher** under the re-referencing; measured **identical** (434 and 403 either way). The gate's cap sits above their pole-free production legs, so it was already a no-op. Finding (4) |
| **P11** | **HELD** | first-game step **+254.8% / +191.7% / +186.8% / +76.6%** — all ≥ the predicted +40%; ruling 6's continuity curve **FAILS**; measured, reported, **not smoothed** |
| **P12** | **BREACHED (16–35), HELD (36–70)** | predicted the ≤20 and 23+ cells would **overlap in both bands**. At 16–35 they **separate** (z +2.51). **Not applied** — stated as an owed word |
| **P13** | **HELD** | all **six** named rows print strictly above their sat-counterfactual. Two **additional** rows the seat added and reports rather than hides (`zane-duursma`, `xavier-duursma`) print **below** theirs — `COUNTERFACTUAL.md` §4 |
| **P14** | **HELD** | nothing outside the lane moved; no re-pin; PR #510 HELD |
| **P15** | **HELD** | pool rows priced under the same formula with their own cells, labelled *provisional — pool values pending Step 4* in every table |

**10 HELD · 5 BREACHED.** Four of the five breaches (P6, P7, P8-second-leg, P10) are the seat's own
predictions being wrong about a board it had not yet built; **the fifth (P12) is the measurement
disagreeing with the seat and agreeing with the owner**, and it is the one that is **not applied**.

---

## 7 · THE WORDS THE SEAT IS OWED, AND WILL NOT CHOOSE

1. **WHICH READING OF "PEDIGREE SHARE"** — the **weight** share (wired: `(1−w) = σ`, the packet's own
   refit identification) or the **value** share (a harmonic blend, not built)? §2.
2. **WHICH `v0` THE SHARE IS A SHARE OF** — the **Step-1 positional v0** (wired) or `entry_anchor` /
   `v0_start`, which is what the machinery being replaced actually leaned on. This is worth the whole of
   finding (2): kako 759.8 vs 1069.0. §4(2).
3. **THE FIRST-GAME CLIFF** — the constraint as ruled makes ruling 6's continuity curve fail. Accept the
   step, fade the pedigree leg on the clock as well (which is the stacking the constraint forbids), or
   rule a third thing. §4(1).
4. **STOP §5 Q1–Q4 THEMSELVES ARE STILL OPEN.** This board is one reading of them, priced. Q3 in
   particular is now known to be **free** — §4(4).
5. **THE AGE TERM** — signal at 16–35, none at 36–70, not cluster-robust, not applied. `AGE_LENS.md` §6.

---

*Every board was built once per configuration from a freshly staged tree, sequentially, under the pinned
five-var environment. Nothing was tuned after seeing any reading. The prereg was committed and pushed
(`cb2883b`) before the first preview board existed.*
