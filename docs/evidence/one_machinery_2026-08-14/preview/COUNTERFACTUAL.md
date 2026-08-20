# THE SELECTABILITY COUNTERFACTUAL — what the preview law pays a player for being picked

**ORDER 30B-P · `land/order-29` · 2026-08-15 · preview board `6a392bca7ad0dee04a6b4f037c758f65`.**
Every number here is read off that board and the preview-lane engine. Harness: `o30bp_movers.py`.
Raw output: `PREVIEW_MOVERS_out.txt`. Machine-readable: `PREVIEW_MOVERS.json` (`counterfactual`, `continuity`).

> **NOTHING IS GREENLIT** — the Step-3 boundary word is still OPEN.
> **THE PREVIEW IS PRE-NUMERAIRE** — Step 6's re-pin has not run; read the *movement*, not the level.
> **Pool rows are PROVISIONAL — pool values pending Step 4.**

---

## 1 · THE QUESTION AND THE TWO OBJECTS

**The question.** Under the new law, is a player better off having been *selected and played*, or having
*sat*? The engine now prices sitting (Step 2's ruled fade) and prices playing (Step 3's blend). The two
are different branches, so the incentive is a **subtraction**, not an argument:

| | |
|---|---|
| **PREVIEW price** | what he actually prints: `(1 − σ(g)) × production + σ(g) × v0` |
| **SAT counterfactual** | what the *same row* would print if he had never played, at his own clock: **`v0 × D(c)`** — the Step-2 sitter law, exactly as wired |

`v0` is the **Step-1 positional v0** (pool rows: their own signed pool cell), `c = (Y − entry) + fE` is the
continuous fade clock, `D` is the ruled fade `1 / 0.5502 / 0.2628 / 0.3460-flat`.

**One honest caveat on the pool rows, stated up front.** `D(c) = 1.0000` for MSD and SSP rows because
**the pool fade is Step 4's work and has not been derived.** Their sat-counterfactual is therefore the
*undiscounted* `v0` — the most generous sitter counterfactual available — and the gaps below are the
**conservative** reading for those two rows.

---

## 2 · THE NAMED ROWS

| player | path | pick | pos | games | σ(g) | v0 (Step-1) | D(c) | **SAT = v0 × D** | **PREVIEW** | **gap** | gap % |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`isaac-kako`** | ND | 13 | SF | 36 | 0.2391 | 759.8 | 0.2788 | **211.8** | **748** | **+536.2** | **+253.1%** |
| `willem-duursma` | ND | 1 | MID | 19 | 0.4239 | 3879.3 | 0.5771 | **2238.9** | **4063** | **+1824.1** | +81.5% |
| `dyson-sharp` | ND | 13 | MID | 13 | 0.5307 | 1551.0 | 0.5771 | **895.2** | **2347** | **+1451.8** | +162.2% |
| `jacob-farrow` | ND | 10 | SD | 18 | 0.4396 | 1284.5 | 0.5771 | **741.3** | **2089** | **+1347.7** | +181.8% |
| `cooper-trembath` * | MSD | 9 | KPF | 24 | 0.3263 | 217.5 | 1.0000 † | **217.5** | **1652** | **+1434.5** | +659.7% |
| `chris-scerri` * | SSP | — | SF | 7 | 0.6797 | 124.4 | 1.0000 † | **124.4** | **242** | **+117.6** | +94.6% |

`*` provisional — pool values pending Step 4.  `†` pool fade not yet derived; shown undiscounted, so the gap is the conservative reading.

**All six named rows are paid to have played.** The demonstration is cleanest on **kako**, the poster row:
his 36 games are worth **+536 board points**, **3.5× his own sat price** — and that is with his production
leg (744.3) sitting *below* his Step-2 print. The law says: even a modest 36-game record beats sitting on
the same pedigree by a wide margin.

### The arithmetic on kako, laid out so it can be checked by hand

```
production leg (pole DELETED, ISO DELETED, form machinery retained) = 744.3
pedigree leg  = STEP-1 positional v0, SF pick 13                    = 759.8
sigma(36)     = exp(-(36/23)^0.80)                                  = 0.2391
price         = (1 - 0.2391) x 744.3  +  0.2391 x 759.8  =  566.4 + 181.7 = 748.1  ->  748
sat           = 759.8 x D(2.920) = 759.8 x 0.2788                            = 211.8
```

His Step-2 price was **1320**; the preview prints **748** (**−572, −43.3%**). **The gap against sitting is
where the incentive lives; the fall against Step-2 is where the deleted pole and ISO went.** Both are real
and they are different facts — see `PREVIEW_MOVERS.md`.

---

## 3 · THE INCENTIVE HAS A CLIFF AT THE FIRST GAME, AND THE SEAT WILL NOT SMOOTH IT

The no-stacking constraint sends a **gameless** row to `v0 × D(c)` and a **one-game** row to
`σ(1) × v0 + (1 − σ(1)) × production` with **`σ(1) = 0.9218`**. The two are not continuous, and the step is
not small. Printed price against games in the current season, straight off the preview engine:

| row | 0 games | 1 game | 2 | 5 | 10 | 15 | **first-game step** |
|---|---:|---:|---:|---:|---:|---:|---:|
| `josh-smillie` (ND 7, MID, c 2.92) | **471** | **1671** | 1659 | 1598 | 1545 | 1607 | **+1200 (+254.8%)** |
| `harry-demattia` (ND 25, MID, c 3.92) | **301** | **878** | 868 | 858 | 787 | 790 | **+577 (+191.7%)** |
| `max-knobel` (ND 42, RUCK, c 4.92) | **287** | **823** | 823 | 846 | 853 | 959 | **+536 (+186.8%)** |
| `dyson-sharp` (ND 13, MID, c 1.92) | **895** | **1581** | 1626 | 1784 | 2123 | 2538 | **+686 (+76.6%)** |

**This is a property of the constraint as ruled, not of the implementation.** The owner's own words set it
up: *"the sitter fade governs gameless clocks only"*. The moment a player's clock stops being gameless, the
fade stops applying to him — and his pedigree leg jumps from `D(c) × v0` to `σ(1) × v0`, which at c = 2.92
is a jump from **0.279 × v0** to **0.922 × v0**.

**Two consequences the owner should rule on, not the seat:**

1. **Ruling 6's continuity acceptance curve (price vs games, smooth and monotone-in-evidence, 0–15) FAILS
   under the preview as specified** — at the 0→1 boundary in all four rows above, and on
   monotonicity in three of them (the price dips after game 1 as the production leg's own shape takes over,
   then recovers). `dyson-sharp` is the only one of the four that is monotone from game 1 onward.
2. **The board consequence is already visible in the top movers.** The four largest *rises* on the whole
   board are exactly this class — players with **1 to 6 games** who now price near their un-faded `v0`:

| row | path | pick | pos | games | Step-2 | **PREVIEW** | Δ | σ(g) | v0 |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|
| `toby-conway` | ND | 24 | RUCK | 6 | 433 | **1420** | **+987 (+227.9%)** | 0.7108 | 1367.5 |
| `harry-barnett` | ND | 23 | RUCK | 2 | 469 | **1345** | +876 (+186.8%) | 0.8679 | 1368.4 |
| `will-green` | ND | 16 | RUCK | 1 | 489 | **1324** | +835 (+170.8%) | 0.9218 | 1375.4 |
| `taylor-goad` | ND | 20 | RUCK | 2 | 597 | **1370** | +773 (+129.5%) | 0.8679 | 1371.0 |

`toby-conway` is the sharpest statement of the law available: **6 games** at a depth-6 clock take him from
**433 to 1420**. Under the Step-2 fade a gameless row at his clock prints `0.3460 × v0`; six games move him
to `0.7108 × v0 + 0.2892 × production`. **The incentive to be selected is enormous, and it is front-loaded
into the first game.**

---

## 4 · THE EDGE THE SEAT WILL NOT HIDE — WHERE THE INCENTIVE **INVERTS**

Two rows in the same family price **below** their own sat-counterfactual. They are reported because the
demonstration is dishonest without them.

| player | path | pick | pos | games | σ(g) | production | v0 | D(c) | SAT | **PREVIEW** | **gap** |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `zane-duursma` | ND | 4 | SF | 38 | 0.2244 | 222.7 | 1592.1 | 0.3385 | **538.9** | **530** | **−8.9 (−1.6%)** |
| `xavier-duursma` | ND | 18 | MID | 128 | 0.0193 | 134.1 | 960.4 | 0.3460 | **332.3** | **150** | **−182.3 (−54.9%)** |

**What this says, plainly: once a player's production leg falls far enough, the law prices him below what
it would have paid him for never playing at all.** For `zane-duursma` — a pick 4 with 38 games and a
production leg of 222.7 — the two are within 1.6% of each other, i.e. **38 games of evidence bought him
almost exactly nothing against the counterfactual of having sat**. For `xavier-duursma` at 128 games the
gap is wide, and at that depth the sat-counterfactual is not a real object (a 26-year-old with no games
would not still be listed) — but the arithmetic is the arithmetic and it is on the record.

**This is the honest boundary of the selectability claim: the new law pays for being selected, and it pays
for playing WELL. It does not pay for playing badly — and past a point it charges for it.** Whether that
is the intended incentive is the owner's ruling, not the seat's.

---

## 5 · WHAT THIS DOES AND DOES NOT DEMONSTRATE

- **It demonstrates** that under the preview law the six named rows are all materially better off having
  played than having sat, and that the effect is very large at the poster row.
- **It does not demonstrate** anything about the *level* of these prices: the board is **pre-numéraire**
  and Steps 4–7 have not run.
- **The pool rows carry an extra provisionality**: their `v0` cells and their fade are Step 4's, so
  `cooper-trembath` and `chris-scerri` are shown against an undiscounted sitter and are labelled twice.
- **The first-game cliff and the two inverted rows are the two things this table exists to surface.**
  Neither is smoothed, neither is argued away, and both are owed owner words.
