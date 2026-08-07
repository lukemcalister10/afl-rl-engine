# THE SIDE-BY-SIDE — act #334 stage B, the owner review set

**What this is.** The board as it stands adopted, against the board this act produces, laid next to each
other so the difference can be ruled on. Six stages landed, five of which moved the board; nothing merged;
nothing registered. Adoption is the owner's word and this document does not presume it.

**Where every number comes from.** Board values are DISPLAY BOARD VALUES in VOR board points, the currency
the board itself prints, denominated so that national-draft **pick 1 = 3,000**. The boards are the file
`data/rl_build/rl_app_data.json` at these commits:

| | board md5 | commit | what it is |
|---|---|---|---|
| **SHIPPED** | `113b36f898a32363c49c2a62fb809f4b` | `f8fe8361` | the adopted board, on main today |
| stage 1 | `de5110bb` | `ad50dad` | the #336 reference layer |
| era removal | `f94e0778` | `f7ae027` | era normalization removed (owner ruling) |
| stage 3 | `6c9f8d3a` | `c0ea507` | curve re-teach + re-anchor + surface refit + numéraire re-base |
| stage 4 | `b490ae8b` | `44950de` | pedigree-conditioned reactivity |
| **FINAL** | `b56bbddea15fd48e35b5794b1b5e9e23` | *this commit* | **+ surprise-scaled evidence trust (amendment 1)** |

All six boards carry **804 players — the same 804 keys, no adds and no drops.** The companion workbook is
`board_before_after.xlsx` beside this file; its per-row stage deltas sum **exactly** to the total, asserted
on all 804 rows. Date of assembly: **2026-08-07**, branch `landing/334-stage-b`.

---

## 1. THE HEADLINE — the whole-cohort no-arbitrage year ratios

This is the act's target instrument. It asks: across every national-draft entrant, what is the engine's own
mean valuation N years after the draft, divided by that same cohort's mean valuation at year 0? The
denominator is the **mean year-0 value over the same included set** as the row, so it is apples to apples.

**Cohort: n = 1,197 entrants, national-draft picks 1–64, draft classes 2004–2022. Busts stay in the
denominator at 0.** Values are the engine's own walk-forward as-of valuations `ev(p,Y)`, not raw scores.

| years after draft | **SHIPPED basis** | stage 4 | **FINAL** | change vs shipped |
|---|---|---|---|---|
| 0 | 1.000 | 1.000 | 1.000 | — (both are the denominator) |
| 1 | 1.123 | 0.9605 | **0.9504** | −0.173 |
| 2 | 1.373 | 1.1891 | **1.1742** | −0.199 |
| 3 | 1.506 | 1.3499 | **1.3452** | −0.161 |
| **4** | **1.572** ← shipped peak | 1.4322 | **1.4321** ← **final peak** | −0.140 |
| 5 | 1.566 | 1.4306 | **1.4305** | −0.136 |
| 6 | 1.519 | 1.3939 | **1.3939** | −0.125 |
| 7 | 1.318 | 1.2108 | **1.2108** | −0.107 |

**The peak year is 4 on both boards — it did not move.** The peak ratio moved from **1.572 to 1.432092**.

The target the act was given is a residual hump of **1.40**. The final peak sits **+0.0321 above it**, inside
the ruling band `[1.35, 1.45]`. The shipped board sat **+0.172 above it**. Convergence took **one iteration**
and no refinement was performed or permitted. **The amendment moved the peak by −0.000104** — a
rounding-scale move, retuned for nowhere.

*Basis: shipped rows from `docs/evidence/noarb_338_2026-08-06/noarb_table_338.txt`; final rows from
`stage4_amend1/noarb/noarb_table_stage4a1.txt`. Both under the CORRECTED #338 minimum-listing-tenure rule.*

---

## 2. PER-ENTRY-YEAR — where the cheapest buy-in sits now

Same cohort, final board only. Mean value at the peak year (4) ÷ mean value at year N.

| N — end of year | n (both years) | mean at yr 4 | mean at yr N | **ratio to peak** |
|---|---|---|---|---|
| 0 | 1,197 | 1,149.66 | 802.78 | 1.4321 |
| **1** | **1,197** | **1,149.66** | **762.99** | **1.5068** ← the maximum |
| 2 | 1,197 | 1,149.66 | 942.66 | 1.2196 |
| 3 | 1,197 | 1,149.66 | 1,079.89 | 1.0646 |
| 4 | 1,197 | 1,149.66 | 1,149.66 | 1.0000 |
| 5 | 1,139 | 1,164.79 | 1,142.70 | 1.0193 |

**In one sentence:** the cheapest buy-in on the final board is at the **end of year 1**, at a ratio of
**1.507** to the peak — and the amendment made it cheaper still.

*Basis: `stage4_amend1/noarb/goal_metrics_stage4a1.txt`, whole cohort, busts at 0 in every denominator.*

---

## 3. ⚠ THE RETURN-TRIGGER — this act does NOT ship without an owner ruling on this

**Condition (b) of the ruling fires, and the amendment moved it further.**

| quantity | shipped | stage 4 | **final** |
|---|---|---|---|
| **yr1-to-peak ratio** (cohort mean at peak yr 4 ÷ cohort mean at yr 1, same n = 1,197) | **1.400** | 1.4910 | **1.5068** |

The number the ruling watches has moved **away** from where the act was narrowing it, by **+0.107** in total
and by a further **+0.016** at this amendment. It moved away because the last two stages cut year-1 values
specifically.

The rise is concentrated in the deep picks, and the per-cut chains below run **stage 3 → stage 4 → final**
(the per-cut figures are not published on the shipped basis, so they are shown from the stage-3 board on):

| cut | stage 3 | stage 4 | **final** |
|---|---|---|---|
| picks 21–64 (deep) | 1.5500 | 1.5692 | **1.6063** |
| picks 1–20 (top) | 1.4660 | 1.4677 | **1.4725** |

The deep cut carries almost all of the movement; the top cut barely moves.

**This is reported straight and is not compensated for anywhere in the build.** No dial was moved to soften
it. **The act does not ship on this number without the owner's word.** The two available responses are
unchanged from stage 4:

**(a) Accept the year-1 dip as honest.** Year-1 records are genuinely thin — one partial season, often a
handful of games — and the engine now prices that uncertainty bust-inclusive rather than letting a small
sample carry the price. On this reading the mark-down is the board telling the truth about what it does not
yet know.

**(b) Order a year-1-side adjustment as a follow-up design.** The year-1 population is the one the last two
stages moved hardest; a targeted design there could bring yr1-to-peak back toward 1.40 without touching the
peak, which has already converged. That would be a new stage with its own derivation and gates.

*This memo does not recommend between them.*

---

## 4. THE TOP END — and the currency re-base

The most valuable player on the board is **Harry Sheezel (North Melbourne)**, on both boards.

| quantity | shipped | **final** |
|---|---|---|
| Sheezel display value (VOR board points) | 12,124 | **10,668** |
| **as a multiple of the numéraire** (÷ pick 1 = 3,000) | **4.041×** | **3.556×** |

Runners-up on the final board: Nick Daicos 9,649 · Luke Jackson 8,670 · Nasiah Wanganeen-Milera 8,633.
**The amendment moves none of them** — every player at the top of the board crossed the establishment bar
years ago and never enters the function this amendment touches.

**THE NUMÉRAIRE NOTE — read this before reading any single-player change as a real move.** Stage 3 re-based
the display currency by a **single uniform factor of ×0.891738 applied to every player alike**. It changes
the printed number and **nothing about relativities**. **Pick 1 stays pinned at 3,000 on both boards.**
The plain "% Δ" column in the workbook therefore shows a shift that applies to everybody and means nothing
about anybody; the workbook's **"% change beyond the currency re-base"** column is the honest measure.
Sheezel's real move: 12,124 × 0.891738 = 10,811 re-denominated against 10,668 actual — **−1.3%**, not the
−12.0% the raw column shows.

---

## 5. THE MRAZ AXIS — what the last two stages actually do

**Noah Mraz — key defender, national-draft pick 35 (2024), sat out year 1, one played season: 2026, four
games at 84.25.** He is the calibration case the owner named.

**His full chain across the act, in display board points:**

| board | value | stage that moved him |
|---|---|---|
| SHIPPED `113b36f8` | **3,847** | — |
| stage 1 `de5110bb` | 3,762 | reference layer (−85) |
| era removal `f94e0778` | 3,762 | unmoved |
| stage 3 `6c9f8d3a` | 3,358 | curve + surface + numéraire (−404) |
| stage 4 `b490ae8b` | 2,898 | reactivity (−460, −13.70%) |
| **FINAL `b56bbdde`** | **1,585** | **surprise-trust (−1,313, −45.31%)** |

**Total across the act: 3,847 → 1,585, a fall of 2,262 points (−58.8%).** His own pick (35) is worth **530**
on the final ladder, so he now prices at **2.99× his pick**, where on the stage-4 board he was at 5.47×.

### What the amendment does, and what it does not

Every **input** to his price is untouched — draft-day anchor `V0` 461.25, retention at depth 0.45877, anchor
leg 211.61, production path `e_full` 5,068.48, all unmoved from stage 4. The amendment conditions **one
weight** on **one new question**: *how big a re-rate is this record claiming?*

| | |
|---|---|
| his prior-implied price today (`R × V0`) | **211.61** |
| what his four games claim he is worth (`e_full`) | **5,068.48** |
| **the claim** | **23.95×** |
| **surprise `s` = \|log 23.95\|** | **3.176** nats — the second-largest on the board |
| how resolved his record is (4.55 games at pace vs the 6-game bar) | 88.5% resolved → **`u` = 0.115 unresolved** |
| **extra evidence demanded** (`SUR_W × s × u`) | **1.830 further passes of the engine's own evidence ramp** |
| `lam` — the share of his price taken from the four games | 0.6937 raw → 0.5926 (stage 4) → **0.3035** |

The anchor now holds the **majority** of his price instead of the minority. **Nothing about his four games
was altered, capped, or re-scored,** and if he keeps playing at that level the shrink dissolves continuously
to **exactly nothing** by six games.

**Why this is the right correction, in one line:** a fringe player's played games are selection-biased
upward — clubs pick him when he is hot, so his four games are his *best* four — and the larger the surprise
a thin record claims, the more of it is that selection rather than the player.

### The pedigree pair — the owner's judgment number

One identical record (four games at 84.25, key defender, age and position matched to Mraz) priced under
different entry histories, draft age held so the only difference is the pick:

| arm | stage 3 | stage 4 | **amendment 1** |
|---|---|---|---|
| **(i)** pick 3, straight year-1 debut | 4,801 | 4,666 | **3,962** |
| **(ii)** pick 35, year-1 sit-out (Mraz-shaped) | 3,534 | 3,050 | **1,668** |
| **RATIO (i) / (ii)** | **1.36** | **1.53** | **2.38** |

**The gap widened again — and it widened without adding a pedigree term.** The top-5 arm falls too (−15%),
because a pick-3 player claiming the same four-game re-rate is *also* making a large claim on a thin sample.
But it falls far less than the pick-35 arm (−45%), because **its prior was already high, so the same four
games are a much smaller surprise against it.** The separation emerges from the statistic itself.

The change never makes anybody's breakout believed *faster*; it makes a **large claim on a thin record**
believed *more slowly*, wherever it is made.

### THE DIALS — two numbers to move

| dial | value | mechanism | at 0 |
|---|---|---|---|
| `RL_PED_BAR` | 0.5 | *whose* record it is: `1 + PED_BAR × (1 − q)`, `q = ped(pick) × sit(depth)` | board returns to `6c9f8d3a` |
| **`RL_SUR_W`** | **5.0** | *what the record claims*: `+ SUR_W × s × u` | **board returns to `b490ae8b`, byte-exact** |

Both live in `data/model_config.json` as valued owner dials (the manifest went 59 → 60 → **61** variables).
**Neither moves the ladder.** The settled ladder (`pvc_curve_v2.json`, `curve_md5` `18203822`, pick 1 = 3,000)
and the numéraire are byte-identical across both stages — asserted at all 64 picks in the workbook build —
so either dial can be re-ruled **without re-deriving any curve**.

### WHO MOVED

| | stage 4 | **amendment 1** |
|---|---|---|
| players moved (of 804) | 51 (6.34%) | **45 (5.60%)** |
| cuts / lifts | 41 / 10 | **38 / 7** |
| board total | 655,759 → 654,570 (−0.18%) | **654,570 → 652,183 (−0.365%)** |
| largest cut | −17.36% (George Stevens) | **−49.32% (George Stevens)** |
| largest lift | +23.36% (Mitch Podhajski) | **+51.52% (Mitch Podhajski)** |

All 45 are in the workbook verbatim, on the **"surprise movers"** sheet, with the record that triggered each
one. The change is ordered by **surprise and nothing else** — mean absolute move by quartile of `s` across
the 56 thin-record players with live evidence: **1.90% / 4.02% / 16.86% / 25.77%**.

**The 7 up-movers are the symmetric consequence, and they are named rather than hidden.** `s` is an
*absolute* log-ratio, so by owner law (L-SYMMETRY, register item 108) a four-game **collapse** from a high
prior is shrunk toward that prior exactly as hard as a four-game breakout of the same size — and that
player's price **rises**. Mitch Podhajski's two games ran at **0.06× his projection**; he is held nearer his
anchor and gains 51.5%. A one-sided rule would be a branch and is refused under L-SMOOTH. If the mechanism
is accepted, the up-movers come with it.

---

## 6. ⚠ THE CALIBRATION CRITERION WAS NOT FULLY MET — and here is exactly where

The amendment was given a two-part target: **Mraz in ~1,100–1,600, while players within ±25% of projection
move less than 1%.** **No dial setting achieves both on the integer board**, and that is reported rather
than forced.

| ruler | max move among the 6 near-projection players | verdict |
|---|---|---|
| **continuous engine price** | **0.657%** | **PASS** |
| integer board value | 1.036% | **FAIL** |

**The entire gap is one row.** *Jaxon Artemis* — board value **193** — moves **193 → 191, two board points**.
His true continuous move is **−0.617%**, i.e. **1.19 board points**, well inside the bar. But one board point
on a 193-point player is already **0.518%**, so a "<1%" test on that row means *"moves by less than 1.93
board points"*. The integer grid cannot express the move the engine actually made.

**Of the 6 players in the band, 4 do not move at all.** Of the 165 thin-record players on the affected path,
the **109 with no live evidence are byte-exact**. If the integer reading is binding for the owner,
`RL_SUR_W = 2.0` satisfies it (band max 0.518% — one board point) with Mraz at **2,267**, outside the Mraz
target. One edit, either way.

---

## 7. WHAT DID **NOT** MOVE

* **The store is untouched** — `37ced3ce45914e6feb00d27e26922e9a`, unchanged across all six stages. Every
  stage in this act is read-only against player data. No record was edited, added or removed.
* **The deep frozen fits stand exactly as fitted, and are named:** the **peak model**, the **band tables**
  (`cm_400`), and **`q97m`** — all unmoved. The **year-zero surface** (`v0surf`) was refit **once**, in
  stage 3 only; stage 4 did not touch it and neither does this amendment (`9713ec6c…`, unchanged), and both
  were proven not to be owed one — re-verified here at **four times** the shipped dial magnitude.
* **The ladder and the numéraire.** `pvc_curve_v2.json` `18203822`, pick 1 = 3,000. Byte-identical at all 64
  picks from stage 4 to final.
* **The top of the board.** Sheezel, Daicos, Jackson, Wanganeen-Milera: all unmoved by the amendment.
* **Round 22 is not ingested.** The board is stamped `as_of_round: 21`.
* **Nothing merged, nothing registered.** No PR, no adoption, no registry entry. Main is untouched. The
  final board exists only on `landing/334-stage-b`. **Adoption is the owner's word.**

---

## 8. GATES — one line

**Parity 804/804, eps = 0** · **numéraire guard PASS, pick 1 = 3,000** · **self-test PASSED, 143 assertions,
0 FAIL, exit 0, 0 re-points** · **Guard 5 PASS** · **fit-class proven (v0surf unmoved, statically and by
three-signature measurement at `SUR_W` 0 / 5 / 20)** · **kill-switch proven (`RL_SUR_W=0` rebuilds
`b490ae8b` byte-exact)** · **boundary clean (SEAM RATIO 1.0000 ×4, prices at the bar byte-identical, no new
cliff in g=1..10)** · **convergence: one iteration** (1.4321, in band, no refinement performed).

Also green: book↔board parity, config-manifest check (61 vars), fut-label, zero-empty-club, env pin, v0surf
frozen-load assert (zero fits at build).

---

*Assembled 2026-08-07 · branch `landing/334-stage-b` · workbook `board_before_after.xlsx` (regenerated with
the amendment as a fifth stage column; per-row stage sums re-asserted on all 804 rows) · evidence under
`docs/evidence/act_334B_2026-08-07/` and `docs/evidence/noarb_338_2026-08-06/`.*
