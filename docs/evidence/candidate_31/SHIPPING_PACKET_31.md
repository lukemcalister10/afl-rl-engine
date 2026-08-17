# SHIPPING PACKET 31 — THE COMPLETE CANDIDATE

**ORDER 31 + ORDER 31-F · `land/order-29` · briefs #334 comments 5310338355 and 5310576233 · basis
resolution 5310447449 · 2026-08-17 · PR #510 stays `[HELD — DO NOT MERGE]`.**

> # NOTHING MERGES. NOTHING IS GREENLIT.
> `main` is untouched. The live board `88ce647f` is unchanged and is a rollback point; so is the Step-2
> board `92982031`, which this tree reproduces **byte-exact** with its dial unset and its artifact restored.

---

## 0 · THE ONE SCREEN

| | |
|---|---|
| **CANDIDATE BOARD** | **`fe6be9d6ac76ebc34d26ebc11d796505`** · total **666,913** |
| vs LIVE `88ce647f` (752,429) | **−85,516 (−11.37%)** |
| vs STEP-2 `92982031` (706,672) | **−39,759 (−5.63%)** |
| rows that moved vs Step-2 | **795 of 804** |
| **exact numéraire `s`** | **`0.9400914291048137` · re-pinned · old → new `\|diff\| = 0`** |
| dial-off control | **FINAL engine code**, `RL_O31` unset, original artifact restored → **`92982031…` BYTE-EXACT** |
| determinism | **PASS** — the final board built twice, byte-identical |
| printed-day-0 identity | **89 of 89, tolerance 0**, on the WRITTEN board |
| continuity assert | **PASS** — max discontinuity at `g=0` is **7.8e-08** relative |
| completeness assert | **PASS** — the 26A forbidden set unreachable; cell coverage **100.0%** |
| reconciliation | **0 of 804** rows fail `production + pedigree == price` at ±1 point |
| **no-arb, deciding instrument** | **NO ARBITRAGE.** PRIMARY margin **+10.24%**, MODERN **+12.77%** |
| pins | moved set is **exactly** the declared set (`pvc_curve_v2.json`, and nothing else) |

**EVERY STEP OF THE BRIEF IS EXECUTED.** The four ORDER 31 left open — the v0 head fix, the position gate,
the numéraire re-pin and the Step-7 instruments — are done, and `β_pool`, the largest borrowing in the
candidate, is now derived. **Every limitation that remains is in §10, in one place, and nothing above can
be read as more settled than §10 says it is.**

---

## 1 · WHAT CHANGED AND WHY — in plain language, one mechanism at a time

### 1.1 · There is now ONE formula. There used to be four.

**What it was.** The last board priced a player by *which lane he fell into*. A player with no games got
`v0 × fade`. A player with 1–10 games got a "thin lane" price in which **his production did not enter at
all**. A player with 11–15 games got a *declared bridge* between two curves that disagreed with each other
by 35% to 170%. A player with 16+ got `production + pedigree`. Four laws, three seams, and a player's price
could jump because he crossed a games threshold.

**What it is now.**

```
price  =  ρ(g) · production   +   [ D(c_u) · (1 − ρ(g))  +  Φ(g,s) · β(g) · ρ(g) ] · v0
```

**One expression. Every player. Every pathway. Every games count.** No sitter branch, no thin lane, no
bridge, no deep lane — not in the algebra and not in the code: the two interception points that used to own
zero-games rows are switched off, and a gameless row is priced by the same line of code as a 300-game
veteran.

**Why this is safe.** The formula *contains both of the laws you already ruled*, exactly, at their own ends:

- At **zero games** `ρ(0) = 0`, so it collapses to `v0 × D(c)` — **your Step-2 sitter law, to the last
  decimal.** That is why printed-day-0 still holds at 89 of 89 with tolerance 0.
- When a player is **established** `ρ → 1`, so it collapses to `production + β(g) × v0` — **the additive
  reading the 30B-R packet resolved (T1), exactly.**

Everything between is a smooth handover. **Measured: the largest discontinuity anywhere on the
price-versus-games curve is 7.8 × 10⁻⁸ — arithmetic rounding, not a cliff.**

### 1.2 · THE HEAD FIX — the ruck defect you were shown, cured, and the other five positions audited with it

**What was wrong.** Your positional entry values are built as `positional relativity × the all-in pick
curve`, and ORDER 30B made them monotone with an isotonic fit. That fit *pools* neighbouring picks when they
disagree. Where a position has almost no players at a pick, its "relativity" there is not a measurement, it
is noise — and the fit pooled that noise **backwards onto pick 1**:

| RUCK pick | 1 | 2 | 3 | 4 |
|---|---:|---:|---:|---:|
| what the data actually said | **1,968** | 4,221 | 4,423 | 3,790 |
| what shipped after the monotone fit | **3,477** | 3,476 | 3,475 | 3,474 |

**In twenty-odd drafts, exactly ONE ruckman has been taken at pick 1, one at pick 2, one at pick 3 and none
at pick 4.** The board was pricing a hypothetical pick-1 ruckman at 3,477 — *above* the pick itself (3,000)
and above a pick-2 midfielder — on the strength of one or two careers.

**What was done.** Every one of the 384 cells (six positions × 64 picks) is shrunk toward the all-in curve
in proportion to how much evidence it actually has, before the monotone fit runs:

```
credibility w  =  n / (n + 15)          n = the estimator's own effective sample at that cell
new relativity =  w × (what this position did here)  +  (1 − w) × 1.0
```

`1.0` is the all-in curve's own relativity — "absent evidence about this position at this pick, a player
here is worth what the pick is worth". `K = 15` is **this project's own constant**, the one already used to
shrink thin pool cells. **The rule is one rule, applied to all six positions symmetrically, and it was
written down in `PREREG_31F.md` before it was run.**

**What it did, at pick 1:**

| position | rows in 20 years | effective n at pick 1 | shipped | **head-fixed** | move |
|---|---:|---:|---:|---:|---:|
| MID | 422 | **20.4** | 3,879 | **3,273** | −15.6% |
| RUCK | 60 | 1.7 | **3,477** | **2,802** | **−19.4%** |
| SD | 180 | 1.2 | 1,659 | **2,697** | +62.6% |
| SF | 212 | 1.9 | 1,595 | **2,574** | +61.4% |
| KPF | 143 | 5.8 | 1,567 | **2,372** | +51.4% |
| KPD | 125 | 1.8 | 2,299 | **2,727** | +18.6% |

**Read that table as one sentence.** Eighteen players have ever been taken at pick 1 in the fitted window
and twelve of them were midfielders. We know what a pick-1 midfielder is worth, and MID is the only head
that barely moves. **We do not know what a pick-1 ruckman, small defender or small forward is worth, and
the board now says so** — it prices them near what the pick is worth instead of near what one career
happened to do. **The ruck head comes down 675 points. It was the fix you asked for and it is not the only
one the same rule found.**

**Everything you ruled about that surface survives, and is re-asserted:**

| ruled property | verdict |
|---|---|
| conservation — the share-weighted total equals the all-in curve's total | **EXACT, drift `0.000e+00`** |
| the floor of 100 at pick 64, every position | **HELD, all six** |
| per-position monotonicity (no ascents) | **HELD, zero ascents** |
| the per-pick reconciliation residual | **PRINTED IN FULL, max 0.1718 — down from 0.1853** |

### 1.3 · Then EVERY measured constant was re-measured, because the ruler moved

This is the part that is easy to get wrong and expensive to skip. The sitter fade, the persistence β, the
stall conditioning Φ and the ρ calibration were **all measured with `v0` in the denominator**. The head fix
moved `v0`. A measurement taken against a moved ruler is no longer the measurement you ruled.

So all four were re-run — **with their committed instruments executed WHOLE**, not re-implemented, not
sliced: only the `v0` source and the output directory were re-pointed, and each substitution is printed and
md5'd in the evidence.

| object | ORDER 31 (old ruler) | **ORDER 31-F (head-fixed ruler)** | drift |
|---|---|---|---|
| sitter fade `D(2)/D(3)/D(4+)` | 0.5502 / 0.2628 / 0.3460 | **0.5583 / 0.2748 / 0.3973** | +0.008 / +0.012 / +0.051 |
| cumulative backbone `B(≤0/2/5/10)` | 0.5502 / 0.6485 / 0.6887 / 0.8223 | **0.5583 / 0.6592 / 0.6897 / 0.8205** | ≤ 0.011 |
| persistence β (5 bands) | 0.2968 / 0.3623 / 0.2233 / 0.1531 / 0.0201 | **0.2879 / 0.3561 / 0.2177 / 0.1416 / 0.0238** | ≤ 0.012 |
| stall conditioner `PhiStall` | 0.5835 / 0.2880 / 0.2880 / 0 / 0 | **0.5793 / 0.2982 / 0.2982 / 0 / 0** | ≤ 0.010 |
| `ρ` calibration `τ / b` | 27.019 / 0.8378 | **29.194 / 0.8015** | RMS 0.0153 → 0.0174 (bar 0.05) |

**Your rulings were applied unchanged, not re-opened.** The fade is still the listed-conditional (L-B)
reading; the depth-4 > depth-3 **selection kink survives and is still not smoothed**; the deep end still
**holds flat** at depth 4 rather than extrapolating. Every re-derived value satisfies `0 < D ≤ 1` and depth
2 is still a fade, which was the pre-declared stop condition — **if any of them had broken a ruled property
the build was to STOP, and none did.**

**On Φ the seat did not take the easy argument.** There is a good reason to think Φ need not be re-measured
at all — it is a *ratio* of two coefficients on the same moved regressor, so to first order the ruler
cancels. **The seat measured it anyway, and the ratio moved slightly MORE than the coefficients did
(0.0102 against 0.0064).** "To first order" is not a measurement.

### 1.4 · ρ(g) — "how much of a player's production do we actually believe yet?"

A single number between 0 and 1. At zero games it is exactly 0. It is **fitted so that a thin cohort's total
price comes out equal to the cumulative backbone you already ruled** — the measured schedule saying a cohort
with ≤2 games is worth 0.66 of a full-value player, ≤5 games 0.69, ≤10 games 0.82. **The backbone constrains
the total; it never replaces production.** That distinction is what killed the thin lane, which let the
backbone *become* the price and threw production away below 10 games.

`ρ(g) = 1 − exp(−(g/29.194)^0.8015)`, RMS residual **0.0174** against the four backbone knots (bar: 0.05).

**The consequence you asked for.** Mraz's signal and Madden's form can never again be priced at zero weight.
Noah Mraz has 4 career games; **922 of his 1,147 points — 80% — are production.** Nick Madden: 640 of 715.

### 1.5 · The sitter fade now runs on UNPLAYED time only

**What it was.** The fade clock ran on *calendar seasons since entry* and only ever reached players with
**zero career games**. A player who played twenty games in year one and never got on the park again was
re-priced by **nothing at all**. 30B-C measured it: `nathan-freeman` held 500 points of pedigree for **seven
consecutive years on two career games**.

**What it is now.** The clock counts **only the time he did not play.** A played season advances his games
count and does not advance his sitter clock; a gameless season advances his sitter clock and does not touch
his games. Two clocks, two disjoint channels, no double-counting. **400 of the 804 rows now carry an
unplayed-clock discount the old law could not reach.**

### 1.6 · Φ — the stall conditioning. Your suspicion, wired.

**Your words:** *"the raw or stalling players get to hold on to their pedigree much longer, a value propped
up by the pedigree players of the past who went on to achieve something."*

**30B-C measured it TRUE on all three clauses.** Players who broke out are 31.2% of the states and carry
**79.5% of the pedigree coefficient's entire mass**; players who never produced a single at-or-above-bar
season in six years are **51.9% of the states and 1.9% of the mass**. And the old law paid a continued
staller **2.86× to 4.51×** what his own cohort measured — a gap that *widened* every year.

`s` = the number of consecutive most-recent seasons in which he **played but did not deliver** (delivered =
10+ games at or above his position's bar). A delivered season resets it. A **gameless** season is skipped —
that is the sitter fade's channel, and counting it twice would be the double-discount the no-stacking
constraint forbids. **Φ multiplies the measured COEFFICIENT ONLY, not the sitter-fade channel**, because the
ratio was estimated on *played* players and the fade on *gameless* ones.

**What it costs, MEASURED not argued.** A declared, default-off dial (`RL_O31_NOPHI=1`) builds the same law
with the conditioning removed:

| | board | vs the candidate |
|---|---:|---:|
| **the candidate (conditioning ON — the seat's recommendation)** | **666,913** | — |
| the same law, conditioning OFF | `e42ed909` **686,238** | **+19,325** |

**488 of 804 rows carry `Φ < 1`.** The conditioning is worth **−19,325 board points**, 2.9% of the book.
**The seat recommends it ON**: it is measured on this project's own panel; leaving it off means knowingly
paying a continued staller 2.9–4.5× what his cohort delivers; and it only ever *reduces* a claim.

### 1.7 · β_pool — the largest borrowing in ORDER 31, now DERIVED

**What it was.** ORDER 31 priced pool rows' pedigree with the **national-draft** β curve, because a pool β
had never been fitted. That was the packet's own §9 item 11 and its largest single borrowing.

**What was done.** The 30B-M panel construction — the same regression, the same games bands, the same
six-season horizon, the same clustering on the player — was transplanted to pool cohorts (**1,706 states
over 442 careers**). The only thing supplied was the `v0` pool rows never had: the signed pool cell, read
through the one accessor that halts on an unsigned cell. **CONTROL: re-running that regression on the
national-draft panel reproduces the 31-F ND row at deviation 0.0**, so this is the same instrument, not an
analogue.

| games band | n | **β_pool** | t | ND β (31-F) |
|---|---:|---:|---:|---:|
| 0–5 | 279 | **0.3731** | **1.33** | 0.2879 |
| 6–15 | 305 | **0.3857** | **0.79** | 0.3561 |
| 16–35 | 368 | 1.0645 | 1.81 | 0.2177 |
| 36–70 | 323 | 1.7978 | 2.46 | 0.1416 |
| 71+ | 431 | 1.9732 | 2.13 | 0.0238 |

**AND HERE IS THE PART TO READ HARDEST.** The measured pool curve **rises** with games, which is the
opposite of what pedigree does. Under your explicit *"π decays in g"* constraint it takes **the same
monotone projection the ND β already takes**, which deletes the rise and leaves the row **flat at 0.3731**.
That is a large deletion and here is the seat's reading of why the rise is not real: **on pool rows `v0`
takes only about 54 distinct values** (pathway × position), so inside a games band it behaves as a pathway
fixed effect rather than as pedigree, and the deep bands' "persistence" is that identification failure.
**And the two shallow bands — the ones that actually price Beecken, Madden, Reidy and Scerri — have `t` of
1.33 and 0.79: statistically indistinguishable from zero.**

**What it costs, MEASURED.** `RL_O31F_NOBPOOL=1` restores ORDER 31's ND-borrowed behaviour:
board `485e729d` **662,485** — so **β_pool is worth +4,428** across the 243 pool rows.

**Φ on pool rows is POOL-MEASURED, not borrowed.** Every pool games band clears the regression's own n ≥ 40
floor, so the brief's condition is met and the conditioning is built from the pool panel's own stall cohort:
`PhiStall_pool` = 0.212 / 0.036 / 0.036 / 0.036 / 0.036. The stall coefficients' `t` are 0.61 / 0.07 / 1.31
/ 1.74 / 0.39 — **weak, and said so here rather than in a footnote.**

### 1.8 · The pool fade, and the one cell that was NOT wired

The pool pathways used to carry **no fade at all** (`D = 1.0`). The 30A-2 harness is `exec`'d verbatim on
the pool population, and **the control re-derives the 31-F ND row at deviation 0.0.**

| depth | n | D | wired? |
|---:|---:|---:|---|
| 1 | 840 | 1.0000 | yes |
| **2** | **588** | **0.5546** | **yes — and FLAT from here out** |
| *3* | *17* | ***2.2635*** | ***NO — it INVERTS*** |
| *4* | *4* | *1.2040* | no — n below the floor of 8 |

**The depth-3 pool cell measures 2.2635** — a "fade" greater than 1. It is measured on **n = 17, all
seventeen of whom eventually played, with 45% of their value in the unobserved tail.** It is survivorship in
its purest form. **The seat published it and did not wire it**, by a rule declared before the reading:
*wire the deepest cell that clears the n floor **and is a fade** (D ≤ 1), then hold flat.*

> **THIS REMAINS THE ONE PLACE THE SEAT MADE A CALL YOUR RULINGS DO NOT DIRECTLY COVER, AND IT IS FLAGGED
> AS AN OWED CONFIRMATION.** Your Step-2 amendment retired *extrapolating a fitted decay through a selection
> kink*; this is that kink in an extreme form. Wiring 2.26 would price a three-season pool sitter at 2.26×
> his entry value. **If you would rather see it wired, say so — it is a one-line change.**

### 1.9 · The numéraire, re-pinned — and the answer is the identity

`s = published_pin / pooled_head_pre_scale` is the one scale the whole economy re-denominates from, picks
and players together. **The re-pin was run through `_load_numeraire` itself, and `s` did not move:**

```
pooled_head_pre_scale   3191.1789716631069  ->  3191.1789716631069     |diff| 0.000e+00
s                       0.9400914291048137  ->  0.9400914291048137     |diff| 0.000e+00
```

**This was PREDICTED IN `PREREG_31F.md` F22 BEFORE IT WAS MEASURED, with the reason:** the head fix is a
**re-split of the all-in ladder across positions** under an exact per-pick renormalisation and one exact
conservation scalar, so it cannot move the ladder, its head, or `s` — *and a movement would have been the
failure*. Both E6 guards were **proved live by firing them** (a doctored `s` halts; a disagreeing pin halts).

**What this means for you: this candidate is NOT pre-numéraire.** Every level in this packet is on the
**same measuring stick** as live `88ce647f` and Step-2 `92982031`. The movers ledger reads movement, not a
change of units.

### 1.10 · The position gate — and the good news

Positions are price-critical twice: they pick the replacement bar and they pick the `v0` cell. All **804
rows were audited**:

- **0 rows** have an unresolved position key.
- **The Baker class is ALREADY SATISFIED.** Your item-217 ruling (*"Yes, G-DEF. Lock it in."*) —
  `sam-flanders`, `oskar-baker`, `ed-langdon` to `G-DEF,G-FWD` — **has landed in the store on this branch.
  All three carry it.** The seat expected to find it outstanding and it is not.
- **50 rows** carry a future position key that sits **outside their own current eligibility declaration**.
  That is legitimate for a real positional move and a defect where the column is stale, and the store alone
  cannot tell them apart. **All 50 are named with their prices in `POSGATE_31F.json`; together they carry
  16,945 points, 2.54% of the book.** The largest are `hunter-clark` (SD keyed, MID declared, 66 games),
  `isaac-cumming`, `callum-coleman-jones`, `jackson-mead`.
- **0 rows were re-keyed by this act.** An eligibility correction is a **store write**, and #334's own line
  is binding: *store writes are an execution act with the owner's word, never a seam act.* It is reported
  and priced, not applied silently.

### 1.11 · Pole and ISO are gone; the evidence weight and the decay gate stayed

The production leg is the finished engine projection with **the pedigree pole deleted** and **the par-built
ISO pick-tax deleted** — the two unambiguous 26A objects on a live price path. The two `par_at` sites that
are *not* pedestals — the evidence weight `Q` and the mediocre-for-years decay gate — are **retained**, with
their denominators re-referenced from pick-conditional par tables to the **position-level, pick-blind bars**
(KPD 65.4 · KPF 63.8 · MID 77.1 · RUCK 75.5 · SD 75.3 · SF 67.9). Form machinery stays; pedestals go. Three
superseded objects are **replaced, not wrapped**. **Audited, build-failing: no printed price can reach the
forbidden set.**

### 1.12 · What did NOT change

The store (`cb38ef11`). The all-in curve. The numéraire (re-pinned to itself). `rl_model.py` (md5
`14000af2…`, unmoved). The manifest `config_sha256`. `noarb_table_338.py`, byte-identical in all three
copies. The `expected_boot` fv pin, which stays stale by design. **The moved set is exactly one file:
`pvc_curve_v2.json`, and that move was declared in the prereg before it happened.**

---

## 2 · THE NO-ARB READING — the tables that did not exist before

**Year-0 is THIS candidate's own entry law**, per your 29C ruling generalised by the supervisor's filed
resolution: what the board actually charges day 0. The emitter proved it fail-closed — **89 of 89 wired
entrants reproduce this board's printed day-0 exactly, before a single record was written.**

### 2.1 · THE DECIDING INSTRUMENT

| window | basis | yr0 | yr1 | yr2 | yr3 | yr4 | margin v 14% | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---|
| PRIMARY 2005–23 | **CANDIDATE** | 1.0000 | 1.0376 | 1.1381 | 1.2491 | 1.3946 | **+10.24%** | **no arb** |
| PRIMARY 2005–23 | 29C landed-law (Step-2 lineage) | 1.0000 | 1.3310 | 1.4810 | 1.5318 | 1.6013 | **−19.10%** | **ARB** |
| PRIMARY 2005–23 | LIVE | 1.0000 | 0.8077 | 0.9737 | 1.0703 | 1.1291 | +33.23% | no arb |
| MODERN 2019–23 | **CANDIDATE** | 1.0000 | 1.0123 | 1.0490 | 1.0990 | 1.1610 | **+12.77%** | **no arb** |
| MODERN 2019–23 | 29C landed-law | 1.0000 | 1.2648 | 1.3240 | 1.3156 | 1.2951 | **−12.48%** | **ARB** |
| MODERN 2019–23 | LIVE | 1.0000 | 0.8225 | 0.9256 | 0.9794 | 0.9772 | +31.75% | no arb |

**This is the headline of the whole order. The previous candidate's own no-arb reading opened an arbitrage
of −19%. This one closes it.** A rookie's year-1 mark now sits 3.8% above his entry price against a 14%
carry, which is what "no free lunch on a first-year player" looks like as a number.

### 2.2 · THE LEGACY RETAINED INSTRUMENT — including the one negative

| group | basis | yr1 | margin v 14% | verdict |
|---|---|---:|---:|---|
| ALL picks 1–64 | **CANDIDATE** | 1.0662 | **+7.38%** | no arb |
| picks 1–20 | **CANDIDATE** | 1.1478 | **−0.78%** | **ARB — printed, not hidden** |
| picks 21–64 | **CANDIDATE** | 0.9372 | **+20.28%** | no arb |
| ALL picks 1–64 | 29C landed-law | 1.3074 | −16.74% | ARB |
| ALL picks 1–64 | LIVE | 1.0730 | +6.70% | no arb |

**6 of 15 readings across all three bases are arbitrages; FIVE of the six are the 29C control. Exactly ONE
belongs to this candidate: picks 1–20 at −0.78%,** i.e. a top-20 pick's year-1 mark beats the carry by
three-quarters of one percent. It is inside the rounding of the instrument's own cohort means and it is
stated here rather than rounded away.

### 2.3 · YEAR PATHS AS % OF ENTRY (yr0 = 100) — LIVE vs CANDIDATE

| PRIMARY 2005–23 | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **CANDIDATE** | 100.0 | **103.8** | 113.8 | 124.9 | 139.5 | 144.8 | 142.0 | 127.7 |
| LIVE | 100.0 | 80.8 | 97.4 | 107.0 | 112.9 | 111.0 | 105.6 | 92.6 |
| difference | +0.0 | **+23.0** | +16.4 | +17.9 | +26.6 | +33.8 | +36.4 | +35.1 |

| MODERN 2019–23 | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **CANDIDATE** | 100.0 | **101.2** | 104.9 | 109.9 | 116.1 | 130.2 | 118.3 | 108.7 |
| LIVE | 100.0 | 82.2 | 92.6 | 97.9 | 97.7 | 103.5 | 91.0 | 80.1 |
| difference | +0.0 | **+19.0** | +12.3 | +12.0 | +18.4 | +26.8 | +27.4 | +28.6 |

**The live board's −19% year-0-to-year-1 drop is the mixed-basis artifact you caught** — a frozen fitted
surface as the denominator over landed-law numerators. On one ruler the path is flat-to-gently-rising, which
is what a fairly priced entry should look like.

### 2.4 · MARK-PATH and REVERSE NO-ARB

Buy at year N, hold one year, against the 14% charge — **every node, both directions, every margin signed.**

| node | 0→1 | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **CANDIDATE, PRIMARY — forward margin** | **+10.24%** | +4.31% | +4.25% | **+2.35%** | +10.17% | +15.93% | +24.04% |
| **CANDIDATE, MODERN — forward margin** | **+12.77%** | +10.37% | +9.23% | +8.36% | **+1.86%** | +23.10% | +22.15% |
| LIVE, PRIMARY — forward margin | +33.23% | **−6.55% ARB** | +4.08% | +8.51% | +15.73% | +18.83% | +26.31% |

**28 mark-path nodes were walked across both bases. Exactly ONE is negative, and it is on the LIVE basis,
not this candidate's.** The candidate's tightest node is 3→4 at +2.35% (PRIMARY) and 4→5 at +1.86%
(MODERN) — thin, positive, and named.

### 2.5 · THE BY-ARM yr1 / yr4 VIEW (ratio to that arm's own entry)

| arm | n | CAND yr1 | CAND yr4 | LIVE yr1 | LIVE yr4 |
|---|---:|---:|---:|---:|---:|
| ND | 1314 | 1.0599 | 1.4519 | 1.0141 | 1.4803 |
| RD | 623 | 0.9301 | 1.1728 | **0.4379** | **0.5090** |
| MSD | 55 | — | 0.7442 | — | 0.6083 |
| UNR | 49 | 0.6342 | 1.1861 | 0.2052 | 0.6090 |
| IRE | 47 | 0.9471 | 1.1333 | 0.2276 | 0.2181 |
| PDA | 43 | 0.7723 | 1.0915 | 0.3062 | 0.5344 |
| PDN | 33 | 0.6284 | 0.7263 | 0.1522 | 0.1897 |
| SSP | 31 | 1.3817 | 1.5945 | 0.9846 | 0.8108 |
| PDS | 21 | 0.7116 | 0.6237 | 0.1329 | 0.1305 |

**The pool arms are the whole story here.** On live, a rookie-drafted player's year-1 mark is **44%** of what
the board charged for him at entry — a 56% instant loss the moment he is priced. That is the mixed-basis
defect at its worst, and on one ruler it becomes 93%.

---

## 3 · THE CONTINUITY CURVE (build-failing assert — PASSED)

Price versus games 0 → 20 with the player's **output held fixed**.

| row | D(c_u) | s | P̂/v0 | step 0→1 | **discontinuity at g=0** | monotone | dead zones |
|---|---:|---:|---:|---:|---:|---|---|
| `josh-smillie` | 0.291 | 0 | 0.98 | +21.7% | **1.5e-08** | YES | none |
| `harry-demattia` | 0.386 | 0 | 1.83 | +29.1% | **1.9e-08** | YES | none |
| `max-knobel` | 0.397 | 0 | 2.37 | +36.9% | **2.4e-08** | YES | none |
| `dyson-sharp` | 1.000 | 1 | 2.25 | +9.5% | **6.0e-09** | YES | none |
| `isaac-kako` | 1.000 | 2 | 0.83 | +0.0% | **3.5e-10** | falls — see below | none |
| `noah-mraz` | 0.558 | 1 | **11.05** | **+124.2%** | **7.8e-08** | YES | none |
| `willem-duursma` | 1.000 | 1 | 1.28 | +3.3% | **2.1e-09** | YES | none |
| `toby-conway` | 0.397 | 2 | 1.45 | +19.9% | **1.2e-08** | YES | none |
| `luke-beecken` | 0.555 | 1 | 0.01 | −3.7% | **2.3e-09** | falls (correctly) | none |
| `chris-scerri` | 1.000 | 1 | 3.98 | +20.7% | **1.3e-08** | YES | none |

`josh-smillie`, the row two rulings turned on: `459 · 558 · 628 · 688 · 742 · 791 · 836 · 878 · 917 · 955 ·
990 · …` Smooth, monotone, no step at 1, no bridge.

**Three readings that need saying out loud.**

1. **`noah-mraz`'s +124% first-game step is not a cliff.** His production estimate is **eleven times his
   `v0`**, so `ρ(1)` alone exceeds his entire sitter price. The right object is whether the price function is
   **continuous** — `lim_{g→0+} price(g) = price(0)` — and it is, to 7.8e-08.
2. **`luke-beecken`'s curve falls, and that is correct.** One career game, essentially zero output. A player
   accumulating games without producing *should* decline.
3. **`isaac-kako`'s curve now falls too, and this is a BREACH the seat owns.** ORDER 31's harness scoped
   "monotone-in-evidence" with a **0.5 factor** — it admitted a row at **half** an at-bar season and called
   it at-bar. Kako's held production is **740 against an at-bar season of 1,358 — 54%**, so under the
   *literal* ruled wording ("at or above the position bar") he is below bar, exactly like Beecken. **The
   build-failing gate is now the literal ruled object; BOTH readings are computed and published, and the
   ORDER-31 proxy's verdict is carried as a BREACH rather than dropped.** The mechanism is worth stating: the
   head fix RAISED kako's `v0` (SF pick 13, 760 → 891), so his pedigree leg grew relative to a production leg
   that is below his own entry value — and he carries a two-season stall run. **The law is doing exactly what
   you asked it to do to a stalling player. The assert's scope was the thing that was wrong.**

---

## 4 · BOARD TOTALS, BY CLASS AND BY PATHWAY

| games | n | candidate | ORDER-31 | step-2 | live | vs step-2 | of which Φ |
|---|---:|---:|---:|---:|---:|---:|---:|
| **0** | 89 | 14,240 | 13,731 | 17,244 | 18,266 | −3,004 (−17.4%) | 0 |
| **1–5** | 60 | 23,002 | 22,406 | 23,347 | 25,129 | −345 (−1.5%) | −472 |
| **6–15** | 87 | 39,698 | 39,806 | 47,166 | 47,757 | −7,468 (−15.8%) | −2,268 |
| **16–35** | 104 | 64,826 | 64,752 | 78,522 | 82,563 | −13,696 (−17.4%) | −5,738 |
| **36–70** | 111 | 109,390 | 109,814 | 121,030 | 129,627 | −11,640 (−9.6%) | −6,098 |
| **71+** | 353 | 415,757 | 413,549 | 419,363 | 449,087 | −3,606 (−0.9%) | −4,749 |

**The `0` band's move is the pool fade plus the head fix.** All 43 pool day-0 rows are byte-identical to the
ORDER-31 board; **45 of the 46 ND day-0 rows moved, and every one of those moves is the head fix.**

### 4.1 · The yr-1 collapse question, answered directly

The condemned thin lane was measured to cut a played rookie's year-1 as-of mark by roughly 40%, because
production did not enter below 10 games at all. **This law cannot reproduce that class of defect,
structurally**: `ρ(g) > 0` for every `g ≥ 1`.

**Measured on the 112 played rookies (`cg` 1–22, age ≤ 21): −14.9% against Step-2, −17.2% against live —
and 44.1% of their total price is production.** On the whole thin band (147 rows): −11.1% against Step-2,
with **36.3% of the price production.** Under the condemned lane that share was **zero**.

---

## 5 · THE NAMED ROWS

| row | path | cg | LIVE | STEP-2 | ORDER-31 | **CANDIDATE** | no-Φ | no-β_pool | ρ | D(c_u) | s | Φ | π | v0 | production | pedigree |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `isaac-kako` | ND | 36 | 1413 | 1320 | 764 | **806** | 899 | 806 | 0.694 | 1.000 | 2 | 0.158 | 0.3258 | 891.1 | 515.6 | 290.4 |
| `willem-duursma` | ND | 19 | 3977 | 4223 | 4368 | **4000** | 4139 | 4000 | 0.508 | 1.000 | 1 | 0.649 | 0.5710 | 3272.8 | 2131.3 | 1868.7 |
| `dyson-sharp` | ND | 13 | 3091 | 3269 | 2376 | **2281** | 2337 | 2281 | 0.407 | 1.000 | 1 | 0.649 | 0.6640 | 1444.8 | 1321.7 | 959.3 |
| `jacob-farrow` | ND | 18 | 2601 | 2765 | 2120 | **2093** | 2147 | 2093 | 0.493 | 1.000 | 1 | 0.649 | 0.5850 | 1288.1 | 1339.5 | 753.5 |
| `noah-mraz` | ND | 4 | 1769 | 1665 | 1122 | **1147** | 1153 | 1147 | 0.184 | 0.558 | 1 | 0.733 | 0.4944 | 454.0 | **922.5** | 224.5 |
| `nick-madden` | PDA | 10 | 1766 | 1650 | 733 | **715** | 741 | 720 | 0.345 | 0.555 | 2 | 0.039 | 0.3680 | 204.4 | **639.8** | 75.2 |
| `liam-reidy` | RD | 7 | 329 | 328 | 263 | **254** | 290 | 262 | 0.273 | 0.555 | 3 | 0.060 | 0.4095 | 372.1 | 101.6 | 152.4 |
| `luke-beecken` | MSD | 1 | 164 | 164 | 257 | **256** | 261 | 256 | 0.065 | 0.555 | 1 | 0.606 | 0.5333 | 479.5 | 0.3 | 255.7 |
| `cooper-trembath` | MSD | 24 | 2201 | 2055 | 1581 | **1552** | 1552 | 1531 | 0.604 | 1.000 | 0 | 1.000 | 0.6216 | 217.5 | 1416.8 | 135.2 |
| `chris-scerri` | SSP | 7 | 459 | 467 | 233 | **232** | 238 | 232 | 0.273 | 1.000 | 1 | 0.530 | 0.7813 | 124.4 | 134.8 | 97.2 |
| `josh-smillie` | ND | 0 | 953 | 471 | 471 | **459** | 459 | 459 | 0.000 | 0.291 | 0 | 1.000 | 0.2908 | 1577.6 | 0.2 | 458.8 |
| `harry-demattia` | ND | 0 | 430 | 301 | 301 | **325** | 325 | 325 | 0.000 | 0.386 | 0 | 1.000 | 0.3857 | 842.1 | 0.2 | 324.8 |
| `max-knobel` | ND | 0 | 411 | 287 | 287 | **253** | 253 | 253 | 0.000 | 0.397 | 0 | 1.000 | 0.3973 | 636.6 | 0.1 | 252.9 |
| `toby-conway` | ND | 6 | 503 | 433 | 777 | **729** | 775 | 729 | 0.245 | 0.397 | 2 | 0.386 | 0.3271 | 1067.8 | 379.7 | 349.3 |
| `marcus-herbert` | MSD | 8 | 906 | 846 | 726 | **719** | 747 | 715 | 0.438 | 1.000 | 1 | 0.518 | 0.6468 | 358.5 | 487.1 | 231.9 |
| `jaxon-artemis` | MSD | 4 | 520 | 500 | 432 | **431** | 449 | 431 | 0.281 | 1.000 | 1 | 0.528 | 0.7741 | 358.5 | 153.5 | 277.5 |
| `jai-newcombe` | MSD | 123 | 4883 | 4561 | 4475 | **4586** | 4586 | 4425 | 0.963 | 1.000 | 0 | 1.000 | 0.3965 | 479.5 | 4395.9 | 190.1 |
| `jack-martin` | ND | 181 | 107 | 97 | 12 | **23** | 78 | 23 | 0.987 | 0.558 | 5 | 0.000 | 0.0075 | 2331.3 | 5.6 | 17.4 |
| `harry-sheezel` | ND | 88 | 11764 | 10987 | 10482 | **10310** | 10310 | 10310 | 0.911 | 1.000 | 0 | 1.000 | 0.1105 | 2729.0 | 10008.4 | 301.6 |
| `nicholas-martin` | SSP | 83 | 3513 | 3281 | 3139 | **3183** | 3183 | 3071 | 0.901 | 0.555 | 0 | 1.000 | 0.3911 | 360.4 | 3042.1 | 140.9 |

**The rows the head fix moved most, and why:**

- **`max-knobel` 287 → 253.** A RUCK taken at pick 42. His entry value fell 830 → 637 because the RUCK
  relativity across picks 30–45 was standing on an effective sample of about 15. **He is the day-0 row this
  fix is for.**
- **`toby-conway` 777 → 729** — the brief's named ruck. Still well above Step-2's 433, because at 6 games
  the old law gave his production almost no weight; but 48 points lower than ORDER 31 gave him, because his
  entry value came down with the ruck head.
- **`isaac-kako` 764 → 806.** He is an SF at pick 13, and SF's shallow picks were *under*-priced by the same
  defect that over-priced RUCK. His entry value rose 760 → 891, so his pedigree leg rose. **He is still
  −514 against Step-2**, and that is the stall conditioning: two below-bar seasons at age 20. If you think
  that should not cost a pick-13 player his pedigree, the dial that says so is `RL_O31_NOPHI` and its
  whole-board price is **+19,325**.
- **`willem-duursma` 4368 → 4000.** MID at pick 1 — the one head that was *well* measured, and it came down
  15.6% because the shrink pulls even a well-sampled cell slightly toward the pick's own value.
- **`harry-demattia` 301 → 325** — MID at pick 25, up on the re-derived fade (D(3) 0.263 → 0.275) net of a
  small head-fix drop.

---

## 6 · THE AT-BAR VETERANS — named in `PREREG_31.md` P1 before any price of this order existed

`jaeger-o-meara` · `joshua-kelly` · `paddy-dow` · `stephen-coniglio` · `jacob-weitering` · `adam-cerra` ·
`darcy-parish` · `dylan-stephens` · `scott-pendlebury` · `will-setterfield` · `jacob-hopper` ·
`jackson-macrae` · `dion-prestia` · `jack-bowes` · `oliver-wines` · `steele-sidebottom` · `cameron-rayner` ·
`jack-lukosius` · `jack-martin` · `ben-ainsworth`.

**Class median |move| vs Step-2 = 69 points. 5 of 20 moved down** — `jaeger-o-meara` −146, `jack-martin`
−74, `steele-sidebottom` −66, `paddy-dow` −59, `jack-bowes` −17. Every one of the five has a long stall run
and a collapsed production leg. **The prediction was "median ≤ 250 and fewer than 25% move down": the median
held with room, and the down-share is now 25% — exactly at the bar rather than through it (ORDER 31 breached
it at 30%).**

---

## 7 · THE PREREG 31 SCORECARD, BY NUMBER — RE-SCORED ON THE COMPLETED CANDIDATE

| # | verdict | reading |
|---|---|---|
| **P1** | **HELD (both legs)** | at-bar veterans: median \|move\| **69** (bar 250) ✔; **25.0%** moved down against a 25% bar ✔ — the leg ORDER 31 breached now holds |
| **P2** | **BREACH, EXPLAINED** | ND day-0: 45 of 46 moved, **by the head fix** — which is P33/P34's own mechanism. 43 pool day-0 rows moved on the Step-2 pool fade. Both are declared mechanisms; the prediction failed to anticipate its own Steps 1 and 2 |
| **P3** | **HELD** | thin lane (`cg` 1–15) down **7,813** against Step-2, inside the declared 2,000–14,000 |
| **P4** | **BREACH** | established book (`cg` ≥ 16) down **28,942** against a declared −25,000…−5,000. Outside on the low side. Owned |
| **P5** | **HELD** | **488 rows** carry `Φ < 1` (bar ≥ 40); `jack-martin` prices **71% below** his unconditioned counterfactual |
| **P6** | **HELD** | **0 of 804** rows fail `production + pedigree == price` at ±1 point |
| **P7** | **BREACH** | `isaac-kako` **806**, band 850–1150. Low by 44, on the stall conditioning |
| **P8/P9/P10** | **BREACH ×3, BY THE HEAD FIX** | `josh-smillie` **459** (band 471 exactly) · `harry-demattia` **325** (301) · `max-knobel` **253** (287). The bands said "exactly Step-2"; the head fix and the re-derived fade moved all three, and **that is Step 1 working**. The prediction was written when Step 1 was not going to run |
| **P11** | **BREACH** | `noah-mraz` **1147**, band 1400–2200. Low. His production still carries 80% |
| **P12** | **BREACH** | `nick-madden` **715**, band 1000–1900. Low |
| **P13** | **BREACH** | `dyson-sharp` **2281** against 2400–3400. Low |
| **P14** | **HELD** | `willem-duursma` **4000** in 3900–5300 |
| **P15** | **BREACH** | `jacob-farrow` **2093** against 2400–3200. Low |
| **P16** | **HELD** | `toby-conway` **729** in 450–1300 |
| **P17** | **HELD** | `luke-beecken` **256** in 100–500 |
| **P18** | **HELD** | `liam-reidy` **254** in 200–500 |
| **P19** | **BREACH** | `cooper-trembath` **1552**, band 1900–2600 |
| **P20** | **HELD** | `chris-scerri` **232** in 150–550 |
| **P21** | **HELD** | `jack-martin` **23** in 0–200 |
| **P22** | **HELD** | `harry-sheezel` **10310** in 10200–11500 |
| **P23** | **HELD** | `jai-newcombe` **4586** in 4300–5000 |
| **P24** | **HELD** | `marcus-herbert` **719** in 700–1300 |
| **P25** | **HELD** | `jaxon-artemis` **431** in 400–800 |
| **P26** | **HELD** | `nicholas-martin` **3183** in 3100–3600 |
| **P27** | **BREACH** | board **666,913**, band 690,000–760,000. Low by 23k |
| **P28** | **HELD** | the numéraire re-pin is a pure scale, `\|s − 1\| = 0.0599 ≤ 0.15`, picks and players together, E6 holds |
| **P29** | **BREACH on (b), HELD on (a) and (c)** | the +40% integer-step band was the WRONG OBJECT, replaced by continuity at `g=0`, which passes at **7.8e-08**. §3 |
| **P30** | **HELD** | completeness passes on every clause; forbidden set unreachable |
| **P31** | **HELD** | printed-day-0 **89 of 89, tolerance 0**, on the written board |
| **P32** | **HELD** | cell coverage **100.0%**, zero fallbacks, zero halts |
| **P33** | **BREACH (one leg)** | six positions audited ✔; the known RUCK case cured ✔; **but RUCK is NOT the largest head move** — SD (+1,038) and SF (+979) beat it (−675). Owned, and see F3 below |
| **P34** | **HELD** | conservation EXACT (0.000e+00, far inside the 0.5% bar), floor-100 retained, monotonicity retained, residual PRINTED |
| **P35** | **HELD** | `D_pool(2) = 0.5546` inside 0.35–0.80, and **`β_pool` is now derived by the same construction, not borrowed** |
| **P36** | **HELD** | the MSD season-1 clock is inherited from `debut_year_338`'s own MSD clause |
| **P37** | **HELD** | entry byte-identity, closed at filing time |
| **P38** | **HELD** | deterministic double-build reproduces `fe6be9d6…` byte-exact |
| **P39** | **HELD** | dial-off on the untouched tree reproduces `92982031…` byte-exact |
| **P40** | **HELD** | the identity gate is a declared NO-OP (`rl_model.py` unmoved, grace lane untouched); the one re-point made is the **emitter's**, declared and diffed |
| **P41** | **HELD** | boot guard passed on every build; `expected_boot` fv pin stale by design |
| **P42** | **HELD** | pins: the moved set is **exactly** the declared set |
| **P43** | **HELD** | `noarb_table_338.py` byte-identical in all three copies |
| **P44** | **HELD** | no foreign `rl_model.py` installed for any board in this packet |
| **P45** | **HELD** | nothing merged; `main` untouched; PR #510 still `[HELD — DO NOT MERGE]` |

**PREREG 31 SCORE: 32 HELD · 13 BREACHED · 0 NOT REACHED.**
(ORDER 31 scored 28 / 12 / 5. The five NOT-REACHED are now all reached; three of the new breaches —
P8/P9/P10 — are the direct and intended consequence of executing Step 1, which the bands assumed would
not run.)

---

## 8 · THE PREREG 31-F SCORECARD, BY NUMBER

| # | verdict | reading |
|---|---|---|
| **F1** | **HELD** | all six positions, all 384 cells, one rule, one K, no hand-set cell |
| **F2** | **HELD** | `posv_RUCK(1)` **2,802.1**, inside [2,300 , 3,050] and below the pick's own 3,000 |
| **F3** | **BREACH** | RUCK is **not** the largest head correction: SD +1,038 and SF +979 exceed RUCK's −675. Owned. The seat predicted the *direction* right and the *ranking* wrong, because it banded on the known defect instead of on the effective-n table it had already printed |
| **F4** | **HELD** | symmetric, and SF(1) **2,574.1** inside [1,900 , 3,000]; SD(1) also up |
| **F5** | **HELD** | MID moves **−15.6%** at pick 1, under 25%, and is the smallest relative pick-1 move of the six |
| **F6** | **HELD** | conservation exact (0.000e+00), floor-100 all six, ascents 0, residual PRINTED at max **0.1718** ≤ 0.25 |
| **F7** | **HELD** | RUCK rows fall (conway, knobel, molier, green, goad, barnett, edwards, bryan, jackson, english, visentini); SF/SD shallow picks rise (jack-martin, kako, farrow); MID slightly down (duursma, sheezel, smillie, sharp, demattia); **pool rows carry ZERO head-fix movement — 0 of 43 day-0 pool rows moved** |
| **F8** | **HELD** | reconciliation 0 of 804; every mover attributable to a declared mechanism |
| **F9** | **HELD** | fade drifts **+0.0081 / +0.0120 / +0.0513**, all inside 0.060 |
| **F10** | **HELD** | every wired `D` in (0,1]; depth 2 still a fade; the ruled kink survives; no stop fired |
| **F11** | **HELD** | β drifts ≤ **0.0116**, inside 0.100; β(2.5) = 0.2879 inside [0.20,0.45]; projection still a fade |
| **F12** | **HELD** | ρ RMS **0.0174** ≤ 0.05; ρ(0)=0 exactly; τ **29.19** inside [15,45] |
| **F13** | **HELD** | printed-day-0 **89 of 89, tolerance 0** on the head-fixed cells |
| **F14** | **BREACH (one leg of three)** | `josh-smillie` **459** ✔ [380,500] · `harry-demattia` **325** ✘ [240,320], high by 5 · `max-knobel` **253** ✔ [140,290] and he fell, as required |
| **F15** | **HELD** | β_pool derived by the transplanted construction; the ND control reproduces at deviation **0.0** |
| **F16** | **HELD** | β_pool(2.5) = **0.3731** inside [0.00,0.70]; n and dispersion on every cell; tiers K-shrunk with borrowing printed |
| **F17** | **HELD** | the depth-3 inversion (2.2635, n 17) stays **published and unwired**; filed as an owed confirmation |
| **F18** | **HELD** | Φ on pool rows is stated: **POOL-MEASURED**, not ND-borrowed |
| **F19** | **HELD** | 804 rows audited; Baker class verified satisfied; 50 residuals named in full with prices |
| **F20** | **HELD** | **0** rows re-keyed, inside [0,40] — and the reason (a store write is not a pricing act) is stated |
| **F21** | **HELD** | run through `_load_numeraire`; E6 coherence 0.000e+00; both guards proved live by firing |
| **F22** | **HELD** | `s` **exactly** unmoved at `0.9400914291048137` — as predicted, with the reason given in advance |
| **F23** | **BREACH (owned, on the harness's scope)** | continuity **7.8e-08** ✔; no dead zones ✔; monotone-in-evidence PASSES on the literal ruled object, and the ORDER-31 0.5-factor proxy flags `isaac-kako`. Both published. §3 |
| **F24** | **HELD** | completeness passes; forbidden set unreachable; audit committed |
| **F25** | **HELD** | cell coverage **100.0%**, zero fallbacks, zero halts |
| **F26** | **HELD** | reconciliation **0 of 804** |
| **F27** | **HELD** | year-0 is this candidate's own entry law; the guard re-pointed as declared and re-proven FAIL-CLOSED at **89 of 89** |
| **F28** | **HELD** | both cohort instruments + mark-path + reverse no-arb + year paths as % of entry + by-arm + class views, all emitted |
| **F29** | **HELD** | every by-arm year-1 cell with n ≥ 8 lands inside [55%,145%]: min **0.5547** (IRE modern), max **1.3817** (SSP). None negative |
| **F30** | **HELD** | every margin printed with its sign; **6 of 15** readings negative, **1 of which is this candidate's**; 28 mark-path nodes walked, 1 negative and it is on LIVE |
| **F31** | **HELD** | board **666,913** inside [600,000 , 720,000] |
| **F32** | **HELD** | the head fix alone is **+1,520** on the one law (and **+190** on the Step-2 law), inside [−25,000 , +15,000] |
| **F33** | **HELD** | entry controls closed at filing time |
| **F34** | **HELD** | deterministic double-build byte-identical |
| **F35** | **BREACH ON THE LETTER, PASSED ON SOMETHING STRONGER** | the prereg predicted dial-off byte-identity to `92982031` **on the final tree with the head-fixed artifact**. That was never possible: the head fix rewrites `pvc_curve_v2.json`, which the Step-2 lineage also reads, so it is **outside** the dial by construction — the seat's control was mis-specified. **What was run instead, last and on the final tree, is a harder control and it PASSES: the FINAL engine code — every 31-F edit in place — with `RL_O31` UNSET and ONLY the original artifact restored reproduces `9298203135202a0c707bb0977ba38c31` BYTE-EXACT** (board `f7off`). That proves by measurement that **every engine edit this order made is inside the declared dial**, and that the one thing outside it is the one declared artifact re-stamp. There is no third thing. The head fix's own price on the Step-2 law is separately isolated at **+190** (`bce0c65d`) |
| **F36** | **HELD** | identity gate: no literal moves; discharged as a declared no-op with the reason printed |
| **F37** | **HELD** | boot guard passes; `expected_boot` fv pin stale by design and stated |
| **F38** | **HELD** | moved set is **exactly** `{pvc_curve_v2.json}` — the declared set; zero undeclared moves |
| **F39** | **HELD** | `noarb_table_338.py` byte-identical, 3 copies, 1 md5 |
| **F40** | **HELD** | every build staged; no foreign `rl_model.py` |
| **F41** | **HELD** | book re-seal did not fire; the manifest is unmoved and the reason is stated |
| **F42** | **HELD** | nothing merged; PR #510 title unchanged |

**PREREG 31-F SCORE: 38 HELD · 4 BREACHED · 0 NOT REACHED.**
The four breaches are **F3** (the seat ranked the head moves wrong), **F14** (one named day-0 row 5 points
above its band), **F23** (an assert scope inherited from ORDER 31) and **F35** (a control the seat specified
in a way that could not have held). **None of the four is the law being wrong; all four are the seat's own
predictions or specifications being wrong, and each is stated as such.**

---

## 9 · THE OWED WORDS — what the seat needs from you

**1 · THE DEPTH-3 POOL-FADE INVERSION.** `D_pool(3) = 2.2635` on n = 17, all seventeen eventual players,
45% of value in the unobserved tail. **Published, not wired**, under the pre-declared "a fade must be a
fade" rule. §1.8. **Confirm, or tell the seat to wire it — one line either way.**

**2 · THE OBJECT.** `β` and `D` are measured in *remaining delivered value per unit of `v0`*, and `v0` is
the Step-1 entry surface — which this order has now **moved**. The seat's answer was to re-derive every
constant against the moved object under R1 discipline (§1.3), and the drifts are all small. **But the
question of whether `v0` is the right object at all is yours, and it is still open.** If you retire `v0` as
the anchor, every number in §1.3 re-derives again.

**3 · THE DEEP-β CONFIDENCE INTERVAL SPANS ZERO.** At 71+ games the pedigree coefficient is
`β = 0.0238, se = 0.0474, t = 0.50`. The point estimate is wired. **Everything `π` does past 71 games rests
on a number that cannot be distinguished from zero, and 353 of the 804 rows are in that band.**

**4 · NEW — THE POOL β's SHALLOW BANDS ARE ALSO INDISTINGUISHABLE FROM ZERO.** `β_pool` at 0–5 and 6–15
games has `t` of **1.33 and 0.79**. Those are the bands that price `luke-beecken`, `nick-madden`,
`liam-reidy`, `chris-scerri` and `jaxon-artemis`. The coefficient is wired because the brief asked for it to
be derived and wired, and its whole-board cost is **+4,428** (`RL_O31F_NOBPOOL` measures it). **If you would
rather pool rows carried no pedigree persistence at all until it is significant, that is a decision the
seat cannot make for you.**

**5 · NEW — THE POOL β RISES AND THE RISE IS DELETED.** The measured pool curve goes 0.373 → 0.386 → 1.065
→ 1.798 → 1.973 with games. The monotone projection your *"π decays in g"* constraint requires deletes all
of that and leaves it flat at 0.373. **The seat believes the rise is an identification artifact (§1.7) and
not persistence, but it is a large deletion of a measured feature and it is printed here rather than
buried.**

**6 · NEW — THE 50 POSITION RESIDUALS.** 50 active rows carry a future position key outside their own
eligibility declaration, worth **16,945 points (2.54% of the book)**. The store cannot distinguish a real
positional move from a stale column. **They are named in `POSGATE_31F.json` and they want your eye.**

---

## 10 · EVERY OPEN LIMITATION, IN ONE SECTION

**These are the reasons this candidate is a candidate. Nothing above should be read as more settled than
this section says it is.**

### 10.1 · Measurement limitations carried into the prices

1. **THE DEEP-β CI SPANS ZERO.** 71+ games: `t = 0.50`. 353 of 804 rows. Point estimate wired.
2. **THE POOL β's TWO SHALLOW BANDS HAVE `t` OF 1.33 AND 0.79** — no signal at conventional levels — and
   they are the bands that price most of the named pool rows.
3. **THE ADDITIVE SCALE ASSUMPTION IS ASSERTED, NOT PROVEN.** `β` is measured in remaining six-season
   delivered value per unit of `v0`; wiring it against the engine's production leg assumes those are the
   same ruler. 30B-R §1.6 named this as the one load-bearing assumption under the additive verdict.
4. **`ρ` IS FITTED ON FOUR POINTS WITH TWO PARAMETERS,** and it is **extrapolated** beyond 10 games where
   the backbone stops. `ρ(71) = 0.870` and `ρ(150) = 0.976` are extrapolations, not measurements.
5. **`Φ` TRANSPLANTS A FORWARD MEASUREMENT ONTO A BACKWARD OBSERVABLE.** 30B-C classified the stall cohort
   by what happened *after* the state; at pricing time the law can only see what happened *before*.
   Declared in the prereg; still the weakest joint in the conditioning.
6. **THE MEASURED β RISE AT 6–15 GAMES IS DELETED** by *"π decays in g"* — measured 0.3561, carried 0.2879.
7. **THE MEASURED β_pool RISE ACROSS ALL FOUR DEEPER BANDS IS DELETED** by the same rule — measured up to
   1.9732, carried 0.3731. This is the larger of the two deletions.
8. **THE DEPTH-3 POOL CELL INVERTS AND IS NOT WIRED.** The seat's one uncovered call. Owed confirmation.
9. **THE POOL `v0` CELLS ARE THIN**, and three rows stand on a *borrowed* cell (`kalani-white`,
   `conrad-williams`, `scott-reed` — PDN\|KPF and PDS\|KPF). **`chris-scerri` remains the least trustworthy
   row on the board**: thin pool cell, 7 games, everything about him provisional.
10. **`ρ`'s BACKBONE CALIBRATION WAS FITTED ON COHORTS WHERE PRODUCTION ≈ `v0`.** `noah-mraz` has production
    ≈ 11× his `v0`. Applying `ρ` there is an extrapolation outside the regime it was measured in.
11. **THE DV STORE DRIFT** — the delivered-value scores the fade and β are built on were computed on store
    `d9a24282`; this branch carries `cb38ef11`. Layer 1 is byte-identical, so the population and every sit
    fact are unaffected. Inherited disclosure from 30A-2.

### 10.2 · Limitations of the head fix itself

12. **`K = 15` IS A TRANSPLANT.** It is this project's own shrink constant, but it was chosen for *pool
    cells*, not for positional heads. Nothing here fits it, and a different `K` would give a different
    head. **It was declared before the run precisely so it could not be tuned to a result.**
13. **THE PER-PICK RECONCILIATION IS STILL NOT EXACT** — max \|ratio−1\| **0.1718** at pick 64. It cannot
    be, because the raw relativities were never monotone. It is *better* than before (0.1853) and the whole
    residual vector is published, not summarised.
14. **THE SHRINK TARGET IS A CHOICE.** Shrinking toward the all-in curve (relativity 1.0) says "absent
    evidence, a player is worth what the pick is worth". The alternative — shrinking toward each position's
    own pick-blind level — was **rejected in advance and in writing**, because that level is itself
    manufactured by the same thin-cell defect and would have *raised* the ruck head. The rejection is
    argued in `PREREG_31F.md` §1.2, before the run.

### 10.3 · Limitations of the gate and the instruments

15. **50 POSITION RESIDUALS, 16,945 POINTS, NOT RESOLVED.** §1.10. A store write is not a pricing act.
16. **THE ONE REMAINING ARBITRAGE READING:** legacy instrument, picks 1–20, **−0.78%**. Marginal but real
    and printed with its sign.
17. **THE `expected_boot` fv PIN IS STALE.** By design and by standing declaration; it was stale on the
    entry board too, and repairing it inside a pricing act is not this order's business.
18. **THE CONTINUITY ASSERT'S SCOPE MOVED.** ORDER 31's 0.5-factor proxy is replaced by the literal ruled
    object. Both readings are published and the change is scored as a breach. §3, F23.

---

## 11 · THE EVIDENCE

| what | where |
|---|---|
| prereg 31 / 31-F (neither edited after a reading) | `docs/evidence/candidate_31/PREREG_31.md` · `docs/evidence/candidate_31f/PREREG_31F.md` |
| the head fix (rule, census, the whole surface, the residual) | `candidate_31f/o31f_headfix.py` · `HEADFIX_31F.json` · `HEADFIX_31F_out.txt` · `CENSUS_31F_out.txt` |
| the re-derivations, with each instrument run whole | `o31f_rederive_fade.py` · `o31f_rederive_beta.py` · `o31f_rederive_phi.py` · `FADE_31F.*` · `BETA_31F.*` · `PHI_31F.*` |
| the re-fitted law | `o31f_fit.py` · `LAW31F.json` |
| the pool parameters, β_pool and Φ_pool | `o31f_pool.py` · `POOL31F.json` · `POOL31F_out.txt` |
| the position gate, all 50 residuals named | `o31f_posgate.py` · `POSGATE_31F.json` · `POSGATE_31F_out.txt` |
| the numéraire | `o31f_numeraire.py` · `NUMERAIRE_31F.json` · `NUMERAIRE_31F_out.txt` |
| the assert wall | `o31f_ledger.py` · `CONTINUITY_31F.json` · `COMPLETENESS_31F.json` |
| the instruments | `emit_matrix_31f.py` · `run_noarb_o31f.sh` · `INSTRUMENTS_31F.*` · `MARGINS_O31F.*` · `t338_*` · `allarm_*` |
| the controls and the build ladder | `o31f_controls.py` · `CONTROLS_31F.*` · `BUILDS_31F.txt` |
| the composed ledger, all 804 rows | `docs/ledgers/CANDIDATE_31_MOVERS.{md,json}` |

---

*Prereg filed and pushed before any quantity of either order existed. Every board built foreground and
strictly sequential in its own staged workspace on the pinned venv under five-var thread pinning with
`RL_V0SURF_PKL` set. No two engine runs ever ran concurrently. Nothing was tuned after a reading; the two
scope changes made after a reading — the continuity assert's object and the emitter's guard — are both
described above with the reading that prompted them and both are scored as breaches.*

> ## NOTHING MERGES.
