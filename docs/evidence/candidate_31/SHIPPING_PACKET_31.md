# SHIPPING PACKET 31 — THE COMPLETE CANDIDATE

**ORDER 31 · `land/order-29` · brief #334 comment 5310338355 · 2026-08-17 · PR #510 stays `[HELD — DO NOT MERGE]`.**

> # NOTHING MERGES. NOTHING IS GREENLIT.
> `main` is untouched. The live board `88ce647f` is unchanged and is a rollback point; so is the Step-2
> board `92982031`, which this build reproduces **byte-exact** with its dial unset.

---

## 0 · THE ONE SCREEN

| | |
|---|---|
| **CANDIDATE BOARD** | **`d9a57cc8770802b83c1264a08356fb60`** · total **664,058** |
| vs LIVE `88ce647f` (752,429) | **−88,371 (−11.74%)** |
| vs STEP-2 `92982031` (706,672) | **−42,614 (−6.03%)** |
| rows that moved vs Step-2 | **749 of 804** |
| dial-off control | `RL_O31` unset → **`9298203135202a0c707bb0977ba38c31` BYTE-EXACT** |
| printed-day-0 identity | **89 of 89, tolerance 0**, on the WRITTEN board |
| continuity assert | **PASS** — max discontinuity at `g=0` is **3.9e-08** relative |
| completeness assert | **PASS** — the 26A forbidden set is unreachable; cell coverage **100.0%** |
| reconciliation | **0 of 804** rows fail `production + pedigree == price` at ±1 point |
| **exact numéraire `s`** | **NOT RE-PINNED — Step 5 was not reached. The board is PRE-NUMÉRAIRE.** See §9. |

**THE FOUR STEPS THIS CANDIDATE DID NOT REACH ARE NAMED IN §9 AND ARE THE FIRST THING TO READ AFTER §1.**
They are Step 1 (the v0 relativity head fix), Step 4 (the position gate), Step 5 (the numéraire re-pin)
and Step 7's re-emitted no-arb instruments. **This is not a complete execution of the brief. It is a
complete, working, defensible LAW with its holes named on its face.**

---

## 1 · WHAT CHANGED AND WHY — in plain language, one mechanism at a time

### 1.1 · There is now ONE formula. There used to be four.

**What it was.** The last board priced a player by *which lane he fell into*. A player with no games got
`v0 × fade`. A player with 1–10 games got a "thin lane" price in which **his production did not enter at
all**. A player with 11–15 games got a *declared bridge* — an interpolation between two curves that
disagreed with each other by 35% to 170%. A player with 16+ games got `production + pedigree`. Four
laws, three seams, and a player's price could jump because he crossed a games threshold.

**What it is now.**

```
price  =  ρ(g) · production   +   [ D(c_u) · (1 − ρ(g))  +  Φ(g,s) · β(g) · ρ(g) ] · v0
```

**One expression. Every player. Every pathway. Every games count.** There is no sitter branch, no thin
lane, no bridge, no deep lane — not in the algebra and not in the code: the two interception points that
used to own zero-games rows are switched off, and a gameless row is priced by the same line of code as a
300-game veteran.

**Why this is safe.** The formula *contains both of the laws you already ruled*, exactly, at their own
ends:

- At **zero games** `ρ(0) = 0`, so the whole thing collapses to `v0 × D(c)` — **your Step-2 sitter law,
  to the last decimal.** That is why the printed-day-0 identity still holds at 89 of 89 with tolerance 0.
- When a player is **established** `ρ → 1`, so it collapses to `production + β(g) × v0` — **the additive
  reading the 30B-R packet resolved (T1), exactly.**

Everything in between is a smooth handover, not a seam. **Measured: the largest discontinuity anywhere on
the price-versus-games curve is 3.9 × 10⁻⁸ — that is arithmetic rounding, not a cliff.** The old design
could not make that claim; it had a genuine step at the first game and a declared bridge it called a
bridge.

### 1.2 · ρ(g) — "how much of a player's production do we actually believe yet?"

**What it is.** A single number between 0 and 1 that says how much weight the production projection
carries at `g` career games. At zero games it is exactly 0 (you cannot project production from nothing).
It rises smoothly and reaches 1 for an established player.

**Where it comes from.** It is **not** invented. It is the one thing in this law that is *fitted*, and it
is fitted so that **a thin cohort's total price comes out equal to the cumulative backbone you already
ruled** — the measured schedule that says a cohort with ≤2 games is worth 0.6485 of a full-value player,
≤5 games 0.6887, ≤10 games 0.8223. The backbone constrains **the total**; it never replaces production.
That distinction is precisely what killed the thin lane: the old design let the backbone *become* the
price and threw the production leg away below 10 games.

`ρ(g) = 1 − exp(−(g/27.019)^0.8378)`, RMS residual **0.0153** in D units against the backbone's four
knots (the Step-3 calibration bar was 0.05).

**The consequence you asked for.** Mraz's signal and Madden's form can never again be priced at zero
weight. Noah Mraz has 4 career games and a production estimate of 5,016. Under the condemned thin lane
his production entered at weight zero. Under this law **916 of his 1,122 points — 82% — are production.**
Nick Madden: 653 of 733 points are production.

### 1.3 · The pedigree term now hands over instead of switching over

**What it is.** `π = D(c_u)·(1−ρ) + Φ·β(g)·ρ`. Read it as: *while we do not yet believe the production
estimate, pedigree is governed by the sitter fade you ruled; as we come to believe it, pedigree hands over
to the measured additive coefficient.* Both ends are your own ruled objects. Nothing new was invented to
join them — the join is `ρ`, the same number that weights production.

### 1.4 · The sitter fade now runs on UNPLAYED time only

**What it was.** The fade clock ran on *calendar seasons since entry*, and it only ever reached players
with **zero career games**. So a player who played twenty games in year one and then never got on the park
again was re-priced by **nothing at all** — the fade could not see him, and the games clock barely moved.
30B-C measured that exactly: `nathan-freeman` held 500 points of pedigree for **seven consecutive years on
two career games**.

**What it is now.** The clock counts **only the time he did not play**. A played season advances his games
count; it does not advance his sitter clock. A gameless season advances his sitter clock; it does not
touch his games. Two clocks, two disjoint channels, no double-counting — and the man who stops playing is
now faded by the same measured law as the man who never started.

**Measured: 400 of the 804 rows now carry an unplayed-clock discount that the old law could not reach.**

This is also the fix for the defect the brief names: a player who is *playing* can no longer be charged a
sitter fade for the seasons he played.

### 1.5 · Φ — the stall conditioning. The owner's suspicion, wired.

**Your words:** *"the raw or stalling players get to hold on to their pedigree much longer, a value propped
up by the pedigree players of the past who went on to achieve something."*

**30B-C measured it TRUE on all three clauses.** Across the low/mid bands, players who broke out are 31.2%
of the states and carry **79.5% of the pedigree coefficient's entire mass**; players who never produced a
single at-or-above-bar season in six years are **51.9% of the states and 1.9% of the mass**. And the old
law paid a continued staller **2.86× to 4.51×** what his own cohort measured — a gap that *widened* every
year rather than closing.

**What this candidate does about it.** The pedigree coefficient a player carries is conditioned on whether
he is *currently stalling*. `s` = the number of consecutive most-recent seasons in which he **played but
did not deliver** (delivered = 10+ games at or above his position's bar). A delivered season resets it to
zero. A **gameless** season is skipped entirely — that is the sitter fade's channel, and counting it twice
would be the double-discount the no-stacking constraint forbids.

`Φ` ramps from 1 (no stall run) to the **measured ratio** `β_stall/β_pooled` over two stall seasons —
which is 30B-C's own definition of a continued staller, not a knob. Measured ratios: **0.583** at the
0–5 band, **0.288** at 6–15 and 16–35, and **zero** past 36 games, where the stall cohort's own
coefficient is `t = −0.29` and `−0.90` — statistically indistinguishable from zero.

**Φ multiplies the measured COEFFICIENT ONLY, not the sitter-fade channel.** `β_stall/β_pooled` is a ratio
of additive coefficients estimated on *played* players; the sitter fade was estimated on *gameless* ones,
and no stall measurement was ever taken on it. Pushing the conditioning through a population it was not
estimated on would be exactly the error this whole order exists to stop.

**What it costs, MEASURED not argued.** A declared, default-off dial (`RL_O31_NOPHI=1`) builds the same law
with the conditioning removed, so the price of the decision is a number rather than a paragraph:

| | board | vs the candidate |
|---|---:|---:|
| **the candidate (conditioning ON — the seat's recommendation)** | **664,058** | — |
| the same law, conditioning OFF | `08ff8af5` **679,242** | **+15,184** |

**488 of 804 rows carry `Φ < 1`.** The conditioning is worth **−15,184 board points**, 2.3% of the book.

**The seat recommends the conditioning ON**, for three reasons: (1) it is measured, on this project's own
panel, with `t = 3.6 / 2.15 / 2.65` in the three low/mid bands; (2) leaving it off means knowingly paying
a continued staller 2.9–4.5× what his cohort delivers, which is the defect you identified; (3) the
direction is conservative — it only ever *reduces* a claim, never inflates one. **The seat did not
condition upward on breakouts**, because a breakout's value is already carried by his production leg, and
raising his pedigree too would double-count him.

**The honest weakness, stated:** 30B-C measured the stall cohort by what happened *next*; at pricing time
this law can only see what happened *before*. That backward transplant is the weakest joint in the
conditioning and it was declared in `PREREG_31.md` disclosure 4 before any number existed.

### 1.6 · The pedigree curve is now made to decay, and that is a deliberate deletion

The measured `β` curve **rises** between 2.5 and 10.5 games (0.2968 → 0.3623) before falling. 30B-C showed
what that does when it is read as a per-game law: **57 of 352 stall paths were paid MORE pedigree after a
season they stalled.** `jarrad-oakley-nicholls` went 535 → 578 → 599 across three stalled seasons.

The brief's constraint is explicit — *"π decays in g"* — so this law carries the **monotone non-increasing
projection** of the measured curve: 0.2968 / **0.2968** / 0.2233 / 0.1531 / 0.0201. **The measured value at
10.5 games is 0.3623 and this law carries 0.2968 there. That is a deletion of a measured feature, done on
your instruction, and it is printed here rather than buried.** It is what makes the price curve monotone
in evidence.

### 1.7 · Pole and ISO are gone; the evidence weight and the decay gate stayed

The production leg is the finished engine projection with **the pedigree pole deleted** and **the par-built
ISO pick-tax deleted** — the two unambiguous 26A objects on a live price path. The two `par_at` sites that
are *not* pedestals — the evidence weight `Q` and the mediocre-for-years decay gate — are **retained**, with
their denominators re-referenced from pick-conditional par tables to the **position-level, pick-blind bars**
(KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). Form machinery stays; pedestals go.

Three superseded objects are **replaced, not wrapped**: ITEM A's anchor blend, `sitout_ev`'s `ns==0` arm,
and the year-zero floor. Wrapping any of them would put a second, uncalibrated pedigree object underneath
the one this law prices.

**Audited, build-failing: no printed price can reach the forbidden set.** `raw_ev` returns before the pole
is formed; the ISO multiplier is identically 1.0; the floor does not run. `COMPLETENESS_31.json`.

### 1.8 · The pool now has a fade of its own, derived by the ND law's own instrument

The pool pathways used to carry **no fade at all** (`D = 1.0`) because the derivation was deferred. This
candidate derives it: the 30A-2 harness is `exec`'d **verbatim**, and only the population and the `v0`
object are swapped.

**The control is the strong part: that transplanted instrument re-derives your ruled ND row at deviation
0.0** — 0.550194 / 0.262786 / 0.346000, exactly. So the pool numbers below come from the same instrument,
not an analogue of it.

| | n | D |
|---|---:|---:|
| `D_pool(1)` | 840 | 1.0 |
| **`D_pool(2)`** | **588** | **0.5546** *(the ND law reads 0.5502 at the same depth)* |
| `D_pool(≥2)` | | **FLAT at 0.5546** |

**AND THE PART YOU SHOULD LOOK AT HARDEST.** The depth-3 pool cell measures **2.2635** — a "fade" greater
than 1. It is measured on **n = 17**, **all seventeen of whom eventually played**, with **45% of their
value in the unobserved tail**. It is survivorship in its purest form. The seat **published it and did not
wire it**, by a rule declared before the reading: *wire the deepest cell that clears the n floor **and is
a fade** (D ≤ 1), then hold flat.* Wiring 2.26 would price a three-season pool sitter at **2.26× his entry
value**, which contradicts the premise of the law you ruled.

> **THIS IS THE ONE PLACE THE SEAT MADE A CALL THAT YOUR RULINGS DO NOT DIRECTLY COVER, AND IT IS FLAGGED
> AS AN OWED CONFIRMATION RATHER THAN PRESENTED AS SETTLED.** Your Step-2 amendment retired *extrapolating a
> fitted decay through a selection kink*; this is that kink in an extreme form, and the seat applied your
> amendment's logic. If you would rather see 2.26 wired, or the depth-3 cell dropped and depth-2 extended
> some other way, say so and it is a one-line change.

**Consequence:** 43 pool day-0 rows now print `v0 × 0.5546` instead of `v0`. The 46 **ND** day-0 rows are
**byte-identical to Step-2** — zero movement, as predicted.

### 1.9 · What did NOT change

The store. The curve. The numéraire. `rl_model.py` (md5 `14000af2a46f7a3c4cdfde303f5a1aff`, unmoved).
The `expected_boot` fv pin, which stays stale by design. `noarb_table_338.py`. The manifest
`config_sha256`. **No pin moved in this act at all** — the Order-31 block is a declared dial, not a
manifest change.

---

## 2 · THE CONTINUITY CURVE (build-failing assert — PASSED)

Price versus games 0 → 20 with the player's **output held fixed**, so only the evidence clock moves.

| row | D(c_u) | s | P̂/v0 | step 0→1 | **discontinuity at g=0** | monotone | dead zones |
|---|---:|---:|---:|---:|---:|---|---|
| `josh-smillie` | 0.279 | 0 | 0.91 | +20.4% | **6.1e-09** | YES | none |
| `harry-demattia` | 0.338 | 0 | 1.73 | +30.6% | **9.1e-09** | YES | none |
| `max-knobel` | 0.346 | 0 | 1.82 | +31.3% | **9.3e-09** | YES | none |
| `dyson-sharp` | 1.000 | 1 | 2.09 | +8.1% | **2.4e-09** | YES | none |
| `isaac-kako` | 1.000 | 2 | 0.98 | +0.9% | **2.8e-10** | YES | none |
| `noah-mraz` | 0.550 | 1 | **11.94** | **+129.4%** | **3.9e-08** | YES | none |
| `willem-duursma` | 1.000 | 1 | 1.08 | +1.9% | **5.8e-10** | YES | none |
| `toby-conway` | 0.346 | 2 | 1.13 | +17.0% | **5.1e-09** | YES | none |
| `chris-scerri` | 1.000 | 1 | 3.97 | +19.6% | **1.6e-09** | YES | none |
| `luke-beecken` | 0.555 | 1 | 0.02 | −3.3% | **1.4e-09** | **falls (correctly — see below)** | none |

`josh-smillie`, the row the last two rulings turned on:
`471 · 567 · 639 · 701 · 758 · 810 · 859 · 904 · 947 · 987 · 1025 · 1059 · 1087 · 1115 · 1140 · 1165 ·
1188 · 1210 · 1231 · 1251 · 1270`. Smooth, monotone, no step at 1, no bridge.

**Two readings that need saying out loud.**

1. **`noah-mraz`'s +129.4% first-game step is NOT a cliff, and the prereg band that flagged it was wrong.**
   `PREREG_31.md` P29(b) banded the *integer* step at +40%, a number read off the 30B-R join, which
   measured it on rows where production and `v0` are the same order. Mraz's production estimate is **twelve
   times his v0**: `ρ(1)` alone — 6% of 5,016 — is larger than his entire sitter price. The correct object
   is whether the price function is **continuous**, i.e. whether `lim_{g→0+} price(g) = price(0)`. It is,
   to 3.9e-08. **P29(b) is scored a BREACH and the assert was corrected to the right object; the breach is
   the seat's specification being wrong, not the law.**
2. **`luke-beecken`'s curve FALLS, and that is correct.** He has one career game and essentially zero
   output. A player accumulating games without producing *should* decline. The assert requires monotone
   non-decreasing **only where the held output is at or above the position bar** — "monotone-in-evidence",
   which is what the brief asks for, not "monotone in games regardless of how badly he plays".

---

## 3 · THE COMPLETENESS AUDIT (build-failing assert — PASSED)

| check | result |
|---|---|
| pole deleted on the price path (`raw_ev` returns before `par_pole`) | **PASS** |
| par-built ISO multiplier is identically 1.0 on the price path | **PASS** |
| the year-zero floor does not run under the one law (replaced, not wrapped) | **PASS** |
| ITEM A's anchor blend replaced, not wrapped | **PASS** |
| `sitout_ev`'s `ns==0` arm replaced, not wrapped | **PASS** |
| every priced row resolves a v0-language object | **804 of 804 — cell coverage 100.0%** |
| rows priced with a fallback or a default | **ZERO** |
| **the 26A forbidden set is reachable from a printed price** | **NO** |

Committed: `COMPLETENESS_31.json`.

---

## 4 · THE POOL CURVES, WITH n AND DISPERSION

| depth | n | mean(v/v0) | **D** | median | p25 | p75 | n_ever | tail share |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 840 | 0.964855 | **1.000000** | 0.0000 | 0.0000 | 0.2391 | 468 | 0.031 |
| **2** | **588** | 0.535075 | **0.554566** | 0.0000 | 0.0000 | 0.0026 | 216 | 0.026 |
| *3* | *17* | *2.183975* | ***2.263527 — REJECTED, INVERTS*** | *1.0042* | *0.5493* | *2.7574* | *17* | *0.454* |
| *4* | *4* | *1.161706* | *1.204022 — rejected, n < 8* | *1.0684* | *0.7637* | *1.4664* | *4* | *0.627* |
| *5* | *1* | *0.090020* | *0.093299 — rejected, n < 8* | | | | *1* | *0.475* |
| *6* | *1* | *0.102622* | *0.106360 — rejected, n < 8* | | | | *1* | *0.475* |

Per-pathway cells, K-shrunk (K = 15) toward the pooled pool row with the borrowing printed per cell, are
in `POOL31.json` / `POOL31_out.txt`. Fitted population 840 rows: RD 611 · IRE 47 · UNR 46 · PDA 38 ·
MSD 29 · SSP 24 · PDN 24 · PDS 21. **The wired object is the pooled row** — a per-pathway law would be
fitted on cells that mostly do not clear the floor, and the pathway table is published so you can see
exactly how much is borrowed.

**`β_pool` was NOT separately fitted. The pooled ND `β` curve is carried on pool rows. This is the largest
single borrowing in the candidate and it is disclosed here rather than hidden.**

---

## 5 · BOARD TOTALS, BY CLASS AND BY PATHWAY

| games | n | candidate | step-2 | live | vs step-2 | vs live | of which Φ |
|---|---:|---:|---:|---:|---:|---:|---:|
| **0** | 89 | 13,731 | 17,244 | 18,266 | −3,513 (−20.4%) | −4,535 | 0 |
| **1–5** | 60 | 22,406 | 23,347 | 25,129 | −941 (−4.0%) | −2,723 | −363 |
| **6–15** | 87 | 39,806 | 47,166 | 47,757 | −7,360 (−15.6%) | −7,951 | −1,949 |
| **16–35** | 104 | 64,752 | 78,522 | 82,563 | −13,770 (−17.5%) | −17,811 | −5,374 |
| **36–70** | 111 | 109,814 | 121,030 | 129,627 | −11,216 (−9.3%) | −19,813 | −5,658 |
| **71+** | 353 | 413,549 | 419,363 | 449,087 | −5,814 (−1.4%) | −35,538 | −1,840 |

**The whole `0` band's move is the derived pool fade** — all 46 ND day-0 rows are byte-identical to Step-2;
all 43 movers are pool rows now carrying `D_pool(2)`.

| pathway | n | candidate | step-2 | live | vs step-2 |
|---|---:|---:|---:|---:|---:|
| ND | 589 | 569,693 | 598,383 | 640,111 | −28,690 (−4.8%) |
| RD | 66 | 40,241 | 44,472 | 46,490 | −4,231 (−9.5%) |
| MSD | 63 | 34,616 | 38,500 | 39,742 | −3,884 (−10.1%) |
| SSP | 28 | 10,149 | 12,174 | 12,812 | −2,025 (−16.6%) |
| PDA | 15 | 5,689 | 7,720 | 8,244 | −2,031 (−26.3%) |
| PDN | 16 | 1,852 | 2,800 | 2,999 | −948 (−33.9%) |
| UNR | 13 | 1,154 | 1,665 | 1,231 | −511 (−30.7%) |
| IRE | 14 | 664 | 958 | 800 | −294 (−30.7%) |

### 5.1 · The yr-1 collapse question, answered directly

The condemned thin lane was measured (30B-N) to cut a played rookie's year-1 as-of mark by roughly 40%,
because **production did not enter below 10 games at all**. **This law cannot reproduce that class of
defect, structurally**: `ρ(g) > 0` for every `g ≥ 1`, so production always enters.

**Measured on the 112 played rookies (`cg` 1–22, age ≤ 21): −15.4% against Step-2, −17.7% against live —
and 45.4% of their total price is production.** On the whole thin band (`cg` 1–15, 147 rows): −11.8%
against Step-2, with **37.1% of the price production**. Under the condemned lane that production share was
**zero**.

---

## 6 · THE NAMED ROWS

| row | path | cg | LIVE | STEP-2 | **CANDIDATE** | no-Φ | ρ | D(c_u) | s | Φ | π | v0 | production | pedigree |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `isaac-kako` | ND | 36 | 1413 | 1320 | **764** | 850 | 0.720 | 1.000 | 2 | 0.152 | 0.3008 | 759.8 | 535.4 | 228.6 |
| `willem-duursma` | ND | 19 | 3977 | 4223 | **4368** | 4546 | 0.525 | 1.000 | 1 | 0.644 | 0.5579 | 3879.3 | 2203.6 | 2164.4 |
| `dyson-sharp` | ND | 13 | 3091 | 3269 | **2376** | 2440 | 0.418 | 1.000 | 1 | 0.644 | 0.6564 | 1551.0 | 1357.9 | 1018.1 |
| `jacob-farrow` | ND | 18 | 2601 | 2765 | **2120** | 2178 | 0.509 | 1.000 | 1 | 0.644 | 0.5727 | 1284.5 | 1384.3 | 735.7 |
| `noah-mraz` | ND | 4 | 1769 | 1665 | **1122** | 1128 | 0.183 | 0.550 | 1 | 0.732 | 0.4893 | 420.0 | **916.5** | 205.5 |
| `nick-madden` | PDA | 10 | 1766 | 1650 | **733** | 748 | 0.353 | 0.555 | 2 | 0.295 | 0.3899 | 204.4 | **653.3** | 79.7 |
| `liam-reidy` | RD | 7 | 329 | 328 | **263** | 283 | 0.276 | 0.555 | 3 | 0.352 | 0.4304 | 372.1 | 102.8 | 160.2 |
| `luke-beecken` | MSD | 1 | 164 | 164 | **257** | 259 | 0.061 | 0.555 | 1 | 0.792 | 0.5350 | 479.5 | 0.5 | 256.5 |
| `cooper-trembath` | MSD | 24 | 2201 | 2055 | **1581** | 1581 | 0.626 | 1.000 | 0 | 1.000 | 0.5109 | 217.5 | 1469.9 | 111.1 |
| `chris-scerri` | SSP | 7 | 459 | 467 | **233** | 236 | 0.276 | 1.000 | 1 | 0.676 | 0.7796 | 124.4 | 136.0 | 97.0 |
| `josh-smillie` | ND | 0 | 953 | 471 | **471** | 471 | 0.000 | 0.279 | 0 | 1.000 | 0.2788 | 1688.8 | 0.0 | 470.8 |
| `harry-demattia` | ND | 0 | 430 | 301 | **301** | 301 | 0.000 | 0.338 | 0 | 1.000 | 0.3385 | 890.6 | 0.0 | 301.4 |
| `max-knobel` | ND | 0 | 411 | 287 | **287** | 287 | 0.000 | 0.346 | 0 | 1.000 | 0.3460 | 830.5 | 0.0 | 287.4 |
| `toby-conway` | ND | 6 | 503 | 433 | **777** | 839 | 0.247 | 0.346 | 2 | 0.379 | 0.2884 | 1367.5 | 382.6 | 394.4 |
| `marcus-herbert` | MSD | 8 | 906 | 846 | **726** | 742 | 0.451 | 1.000 | 1 | 0.644 | 0.6266 | 358.5 | 501.4 | 224.6 |
| `jaxon-artemis` | MSD | 4 | 520 | 500 | **432** | 442 | 0.285 | 1.000 | 1 | 0.672 | 0.7719 | 358.5 | 155.2 | 276.8 |
| `jai-newcombe` | MSD | 123 | 4883 | 4561 | **4475** | 4475 | 0.975 | 1.000 | 0 | 1.000 | 0.0443 | 479.5 | 4453.8 | 21.2 |
| `jack-martin` | ND | 181 | 107 | 97 | **12** | 44 | 0.993 | 0.550 | 5 | 0.000 | 0.0040 | 1593.1 | 5.6 | 6.4 |
| `harry-sheezel` | ND | 88 | 11764 | 10987 | **10482** | 10482 | 0.932 | 1.000 | 0 | 1.000 | 0.0866 | 2830.9 | 10236.7 | 245.3 |
| `nicholas-martin` | SSP | 83 | 3513 | 3281 | **3139** | 3139 | 0.923 | 0.555 | 0 | 1.000 | 0.0639 | 360.4 | 3116.0 | 23.0 |

**`isaac-kako` is the row to argue about, so here it is in full.** He has 36 games and two consecutive
seasons below the SF bar of 67.9, so `s = 2` and `Φ = 0.152`. His production leg is 744 and his `v0` is
760 — they are nearly equal, which is why this row is so sensitive to the pedigree treatment. Live prices
him 1413; Step-2 1320; the weight-form preview 748; the additive reading 886; **this candidate 764, of
which 535 is production.** Turn the stall conditioning off and he is **850**. **If you think two below-bar
seasons at age 20 should not cost a pick-13 player 86 points of pedigree, the dial that says so is
`RL_O31_NOPHI` and its whole-board cost is +15,184.**

**`toby-conway` rises** (433 → 777) despite `s = 2` and a depth-4 unplayed clock, because the old law gave
his production leg almost no weight at 6 games. **`jack-martin` collapses** (97 → 12): 181 games, a
production leg of 5.6, and a five-season stall run — the law is now saying, correctly, that a 32-year-old
who has not delivered in five years is worth what he produces.

---

## 7 · THE AT-BAR VETERANS — named in `PREREG_31.md` P1 before any price of this order existed

`jaeger-o-meara` · `joshua-kelly` · `paddy-dow` · `stephen-coniglio` · `jacob-weitering` · `adam-cerra` ·
`darcy-parish` · `dylan-stephens` · `scott-pendlebury` · `will-setterfield` · `jacob-hopper` ·
`jackson-macrae` · `dion-prestia` · `jack-bowes` · `oliver-wines` · `steele-sidebottom` · `cameron-rayner` ·
`jack-lukosius` · `jack-martin` · `ben-ainsworth`.

**Class median |move| vs Step-2 = 51 points. 6 of 20 moved down.** The prediction was "median ≤ 250 and
fewer than 25% move down"; the median held with room, **the down-share leg BREACHED at 30%** — and the six
that fell (`jaeger-o-meara` −151, `jack-martin` −85, `paddy-dow` −77, `steele-sidebottom` −68, `jack-bowes`
−29, `jacob-hopper` −10) are exactly the ones with a long stall run and a collapsed production leg. The
full table is in the ledger.

---

## 8 · THE PREREG SCORECARD, BY NUMBER — BREACHES OWNED

| # | verdict | reading |
|---|---|---|
| **P1** | **BREACH (one leg)** | at-bar veterans: class median |move| **51** (bar 250) ✔; **30%** moved down against a 25% bar ✘ |
| **P2** | **BREACH, EXPLAINED** | ND day-0: **0 of 46 moved — byte-identical** ✔. **43 pool day-0 rows moved** because Step 2 derived a pool fade where there was none. A declared mechanism, not a surprise; the prediction failed to anticipate its own Step 2. |
| **P3** | **HELD** | thin lane (`cg` 1–15) down **8,301** against Step-2, inside the declared 2,000–14,000 |
| **P4** | **BREACH** | established book (`cg` ≥ 16) down **30,800** against a declared −25,000…−5,000. Outside on the low side. Owned. |
| **P5** | **HELD** | **488 rows** carry `Φ < 1` (bar: ≥ 40). `jack-martin` prices **73% below** his unconditioned counterfactual (12 against 44), far past the bar |
| **P6** | **HELD** | **0 of 804** rows fail `production + pedigree == price` at ±1 point |
| **P7** | **BREACH** | `isaac-kako` **764**, band was 850–1150. Low, by the stall conditioning |
| **P8/P9/P10** | **HELD** | `josh-smillie` **471** · `harry-demattia` **301** · `max-knobel` **287** — exact |
| **P11** | **BREACH** | `noah-mraz` **1122**, band 1400–2200. Low. His production still carries 82% of it |
| **P12** | **BREACH** | `nick-madden` **733**, band 1000–1900. Low |
| **P13** | **BREACH** | `dyson-sharp` **2376** against a 2400–3400 band — low **by 24 points**. Owned |
| **P14** | **HELD** | `willem-duursma` **4368** in 3900–5300 |
| **P15** | **BREACH** | `jacob-farrow` **2120** against a 2400–3200 band. Low. Owned |
| **P16** | **HELD** | `toby-conway` **777** in 450–1300 |
| **P17** | **HELD** | `luke-beecken` **257** in 100–500 |
| **P18** | **HELD** | `liam-reidy` **263** in 200–500 |
| **P19** | **BREACH** | `cooper-trembath` **1581**, band 1900–2600 |
| **P20** | **HELD** | `chris-scerri` **233** in 150–550 |
| **P21** | **HELD** | `jack-martin` **12** in 0–200 |
| **P22** | **HELD** | `harry-sheezel` **10482** in 10200–11500 |
| **P23** | **HELD** | `jai-newcombe` **4475** in 4300–5000 |
| **P24** | **HELD** | `marcus-herbert` **726** in 700–1300 |
| **P25** | **HELD** | `jaxon-artemis` **432** in 400–800 |
| **P26** | **HELD** | `nicholas-martin` **3139** in 3100–3600 |
| **P27** | **BREACH** | board **664,058**, band 690,000–760,000. **Low by 26k.** The seat's band did not price its own Step-2 pool fade (−3,513) or the full weight of the stall conditioning (−15,184) |
| **P28** | **NOT REACHED** | the numéraire was not re-pinned. §9 |
| **P29** | **BREACH on leg (b), HELD on (a) and (c)** | monotone-in-evidence ✔, no dead zones ✔; the +40% integer-step band was the WRONG OBJECT and is replaced by continuity at `g=0`, which passes at **3.9e-08**. §2 |
| **P30** | **HELD** | completeness audit passes on every clause; forbidden set unreachable |
| **P31** | **HELD** | printed-day-0 **89 of 89, tolerance 0**, on the written board |
| **P32** | **HELD** | cell coverage **100.0%**, zero fallbacks, zero halts |
| **P33/P34** | **NOT REACHED** | Step 1, the v0 relativity head fix, was not executed. §9 |
| **P35** | **HELD** | `D_pool(2) = 0.5546`, inside the declared 0.35–0.80, and shallower than ND's 0.5502 as predicted |
| **P36** | **HELD** | the MSD season-1 clock is inherited from `debut_year_338`'s own MSD clause in the transplanted harness, not restated |
| **P37** | **HELD** | entry byte-identity, closed at filing time |
| **P38** | **NOT RUN** | the deterministic double-build was not run. §9 |
| **P39** | **HELD** | dial-off reproduces `9298203135202a0c707bb0977ba38c31` **byte-exact** |
| **P40** | **NOT REACHED** | no identity-gate re-point was made (Step 7 not reached) |
| **P41** | **HELD** | boot guard passed on every build; `expected_boot` fv pin stale by design |
| **P42** | **HELD, VACUOUSLY** | **no pin moved.** The moved-set is empty and asserted empty |
| **P43** | **HELD** | `noarb_table_338.py` untouched |
| **P44** | **HELD** | no foreign `rl_model.py` was installed for any board in this packet |
| **P45** | **HELD** | nothing merged; `main` untouched; PR #510 still `[HELD — DO NOT MERGE]` |

**Score: 27 HELD · 12 BREACHED · 6 NOT REACHED.** Every breach is the seat's own prediction being wrong,
and every one of the twelve is in the *same direction* — the seat systematically over-predicted the
candidate's prices because it did not price its own Step-2 pool derivation or the full weight of the
stall conditioning before filing. **That is the most useful thing the prereg found and it is stated as a
finding, not argued around.**

---

## 9 · EVERY OPEN LIMITATION, IN ONE SECTION

**These are not caveats. They are the reasons this candidate is not finished, and they are printed here so
that no number above can be read as more settled than it is.**

### 9.1 · FOUR BRIEF STEPS WERE NOT EXECUTED

1. **STEP 1 — THE v0 RELATIVITY HEAD FIX WAS NOT DONE.** The known RUCK head inflation (1,968 → 3,477) is
   **still in the board**, and the other five positions were not audited. Every `v0` in this packet is the
   Step-1 surface **as it already stood**, defect included. Any row whose pedigree leg matters and whose
   position is RUCK should be read with that in mind.
2. **STEP 4 — THE POSITION GATE (the Baker class) WAS NOT RUN.** Active rows' position keys were not
   audited against current reality, so a row priced against the wrong position bar is priced against the
   wrong bar in this candidate too.
3. **STEP 5 — THE NUMÉRAIRE WAS NOT RE-PINNED. THERE IS NO EXACT `s` TO REPORT.** **THE WHOLE BOARD IS
   PRE-NUMÉRAIRE.** Read the *movement* and the *shape*, not the level. A re-pin is a scale on picks and
   players together and will move every total in §5.
4. **STEP 7's INSTRUMENTS WERE NOT RE-EMITTED.** **There are no Order-31 no-arb tables in this packet** —
   no as-of matrix, no cohort instruments, no mark-path, no reverse no-arb, no year-1/2/3 class views.
   The supervisor's ruling for that emit (your candidate's own entry law as year-0, via a declared re-point
   of `emit_matrix_29c.py` with its guard re-asserted at 89/89 against this board's day-0 prints) is
   **recorded and unexecuted**. This is the single largest gap between this packet and the brief.

### 9.2 · MEASUREMENT LIMITATIONS CARRIED INTO THE PRICES

5. **THE DEEP-β CONFIDENCE INTERVAL SPANS ZERO.** At 71+ games the pedigree coefficient is `t = 0.49` with
   a 90% interval of **−4.6% … +10.5%**. The point estimate is wired. Everything `π` does past 71 games
   rests on a number that cannot be distinguished from zero. 353 of the 804 rows are in that band.
6. **THE ADDITIVE SCALE ASSUMPTION IS ASSERTED, NOT PROVEN.** `β` is measured in *remaining six-season
   delivered value per unit of `v0`*. Wiring it against the engine's production leg assumes those two are
   the same ruler. 30B-R §1.6 named this as the one load-bearing assumption under the additive verdict and
   it is inherited here unchanged.
7. **`ρ` IS FITTED ON FOUR POINTS WITH TWO PARAMETERS,** and it is **extrapolated** beyond 10 games, where
   the backbone stops. `ρ(71) = 0.894` and `ρ(150) = 0.985` are extrapolations, not measurements, and they
   cut the established book by a few percent.
8. **`Φ` TRANSPLANTS A FORWARD MEASUREMENT ONTO A BACKWARD OBSERVABLE.** 30B-C classified the stall cohort
   by what happened *after* the state. This law can only see what happened *before*. Declared in the
   prereg; still the weakest joint in the candidate.
9. **THE MEASURED β RISE AT 6–15 GAMES IS DELETED,** by the brief's "π decays in g". The measured 0.3623 is
   carried as 0.2968. §1.6.
10. **THE DEPTH-3 POOL CELL INVERTS AND WAS NOT WIRED.** §1.8. This is the seat's one uncovered call and
    it is an **owed confirmation**.
11. **`β_pool` WAS NOT FITTED.** Pool rows carry the ND `β`. The largest single borrowing in the candidate.
12. **THE POOL `v0` CELLS ARE THIN**, and three rows stand on a *borrowed* pool cell (`kalani-white`,
    `conrad-williams`, `scott-reed` — PDN|KPF and PDS|KPF). `chris-scerri` remains the least trustworthy
    row on the board: thin pool cell, 7 games, everything about him provisional.
13. **THE DV STORE DRIFT** — the delivered-value scores the pool fade is built on were computed on store
    `d9a24282`; this branch carries `cb38ef11`. Layer 1 is byte-identical, so the population and every sit
    fact are unaffected. Inherited disclosure from 30A-2.
14. **`ρ`'s BACKBONE CALIBRATION WAS FITTED ON COHORTS WHERE PRODUCTION ≈ `v0`.** `noah-mraz` has
    production ≈ 12× his `v0`. Applying `ρ` there is an extrapolation outside the regime the calibration
    was measured in, and it is the reason his row moves as much as it does.

### 9.3 · CONTROLS NOT RUN

15. **The deterministic double-build was not run** (P38). Every board in this packet was built once.
16. **No identity gate re-point, no book re-seal, no as-of matrix.** Steps 6–7's control set is
    unexecuted apart from the asserts in §2, §3 and the dial-off byte-identity.

---

## 10 · WHAT THE SEAT WOULD DO NEXT, IN ORDER

1. Step 1 (the v0 head fix) — it changes every pedigree leg and therefore every number above.
2. Step 5 (the numéraire) — until it runs, no level in this packet is quotable.
3. Step 7's instruments on the re-pointed year-0 basis — the no-arb reading is the owner's required format
   and it is absent.
4. Step 4 (the position gate).
5. `β_pool`.
6. The double-build and the remaining controls.

---

*Prereg `PREREG_31.md` filed and pushed before any Order-31 quantity existed. Every board built foreground
and strictly sequential on the pinned venv under five-var thread pinning with `RL_V0SURF_PKL` set. Nothing
was tuned after any reading; the two changes made after a reading — Φ conditioning the coefficient only,
and the continuity assert's object — are both described above with the reading that prompted them.*

> ## NOTHING MERGES.
