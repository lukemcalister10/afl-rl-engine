# THE SIDE-BY-SIDE — act #334 stage B, the owner review set

**What this is.** The board as it stands adopted, against the board this act produces, laid next to each
other so the difference can be ruled on. Seven stages landed, six of which moved the board; nothing merged;
nothing registered. Adoption is the owner's word and this document does not presume it.

> **STAGE 5 IS NOW IN, AND IT CHANGES THE LEAD NUMBER.** The quiet-starter reprice (board `13f8c2e0`) is
> the sixth stage column. Two things must be read before anything else in this file:
>
> 1. **The conservation view now leads with the FULL COHORT**, per the owner's ruling (#334 comment
>    5217177098): ND 1-64 **plus every pool route**, classes 2004-2025 at reached years. On that basis
>    year 1 lands at **0.9461** (from 0.9082). The ND-only splits sit beside it in §1.
> 2. **Stage 5 did not reach the 1.00 floor on the ND teaching window: it lands at 0.9908.** The single
>    thing standing between it and the floor is a law this seat itself introduced — *no cell taught a
>    price above its own entry anchor*. Lifting it lands **1.0000**. That is an owner question, it is now
>    a number, and it is set out in `../stage5/CONSISTENCY_PASS.md §3`. **Read that before ruling.**

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
| stage 4 amendment 1 | `b56bbddea15fd48e35b5794b1b5e9e23` | `c05f214` | surprise-scaled evidence trust |
| **FINAL** | `13f8c2e0240600733a5fb42414510445` | *this commit* | **+ stage 5, the QUIET-STARTER REPRICE (`RL_G5_W` = 1.0)** |

All seven boards carry **804 players — the same 804 keys, no adds and no drops.** The companion workbook is
`board_before_after.xlsx` beside this file; its per-row stage deltas sum **exactly** to the total, asserted
on all 804 rows by `verify_xlsx.py` (LibreOffice is non-functional in this sandbox, so the formulas are
evaluated in Python). Date of assembly: **2026-08-07**, branch `landing/334-stage-b`.

### THE SIXTH COLUMN — stage 5 in one screen

| | |
|---|---|
| **the owner's word** | *"these mechanisms probably should phase out over season 2/3 etc instead of just hard dropping"* — with the measurement behind it: quiet starters (1-5 games) are priced at 0.707 of entry against a measured discounted future of ~0.95 |
| **the change** | one engine file. `sitout_ev`'s anchor leg becomes `G · R · entry_anchor` at **both** anchor sites (the blend term and `_surprise`'s anchor argument). `_ped_prior` is a decay statistic, not an anchor, and is untouched |
| **G** | a taught surface over **τ × CUMULATIVE career games × log-pick**, per retention class, frozen in `engine/rl_after/g5_table.json` (md5 `1bd109cb`) and re-evaluated from each player's record at every build — never stored, never stamped |
| **the dial** | **`RL_G5_W` = 1.0**. `RL_G5_W=0` is a structural short-circuit and rebuilds `b56bbdde` **byte-exact through the full gate** |
| **who moves** | **66 of 804 — every one UP, zero cuts.** Board total +0.3658% |
| **Mraz** | `1,585 → 1,645` = **3.10× his pick** (was 2.99×), inside the owner's 3.0-3.5× disclosed tier |
| **Nairn** | `471 → 605` (+28.45%) |
| **the ladder** | **UNMOVED** at all 64 picks; numéraire pick-1 = 3,000 held |

---

## 1. THE HEADLINE — the conservation-of-value year ratios

This is the act's target instrument. It asks: across an entry cohort, what is the engine's own mean
valuation N years after the draft, divided by that same cohort's mean valuation at year 0? The denominator
is the **mean year-0 value over the same included set** as the row, so it is apples to apples. Busts stay
in the denominator at 0.

### 1a. THE FULL COHORT — the basis the owner ruled this table must lead with

> *"when I'm talking about the conservation of value, for me it's about cohorts as a whole, not just ND
> picks (but the split is often helpful too). And why wouldn't 2023/24/25 drafts be included in this
> presentation given they too have year 0 and year 1 cohort ratings"* — owner, #334 comment 5217177098

**ND picks 1–64 PLUS every pool route, draft classes 2004–2025, at reached years. n = 2,517 at year 1.**

| years after draft | baseline `b56bbdde` | **FINAL `13f8c2e0`** | stage-5 move |
|---|---|---|---|
| 0 | 1.000000 | 1.000000 | — (the denominator) |
| **1** | 0.908179 | **0.946050** | **+0.037870** |
| 2 | 1.097539 | **1.111225** | +0.013686 |
| 3 | 1.242814 | **1.246016** | +0.003202 |
| 4 | 1.344534 | **1.345462** | +0.000928 |
| 5 | 1.346731 | **1.346923** | +0.000191 |
| 6 | 1.295768 | **1.295768** | +0.000000 |

**Year 1 on the full cohort lands at 0.9461.** The splits, on the owner's 2004–2025 window:

| split | n | baseline | **FINAL** | move |
|---|---|---|---|---|
| ND 1–64 | 1,383 | 0.949994 | **0.988526** | +0.038531 |
| pool routes | 1,134 | 0.752800 | **0.788214** | +0.035414 |
| class 2023 ND | 64 | 1.043485 | **1.077494** | +0.034010 |
| class 2024 ND | 64 | 0.875930 | **0.901970** | +0.026040 |
| class 2025 ND | 58 | 0.926992 | **0.947385** | +0.020393 |

Stage 5 **did** reach the pool quiet starters — the sit-out path serves pool entrants off their signed
division levels, and their cells taught from their own outcomes. The remaining full-cohort drag is the pool
leg's deep sub-par level; **its own honesty has not been measured on the current basis** and is a separately
fired research item, not a claim this act makes.

### 1b. ND 1–64, classes 2004–2022 — the TEACHING window, printed so the two are never confused

**n = 1,197.** A class must have realised outcomes to teach from, so the fit population stops at 2022.

| years after draft | **SHIPPED basis** | stage 4 amend 1 | **FINAL** | change vs shipped |
|---|---|---|---|---|
| 0 | 1.000 | 1.000 | 1.000 | — (both are the denominator) |
| 1 | 1.123 | 0.9504 | **0.9908** | −0.132 |
| 2 | 1.373 | 1.1742 | **1.1855** | −0.188 |
| 3 | 1.506 | 1.3452 | **1.3471** | −0.159 |
| **4** | **1.572** ← shipped peak | 1.4321 | **1.4327** ← **final peak** | −0.139 |
| 5 | 1.566 | 1.4305 | **1.4306** | −0.135 |
| 6 | 1.519 | 1.3939 | **1.3939** | −0.125 |
| 7 | 1.318 | 1.2108 | **1.2108** | −0.107 |

**The peak year is 4 on both boards — it did not move.** The peak ratio moved from **1.572 to 1.432651**,
inside the ruling band `[1.35, 1.45]` and **+0.0327** above the 1.40 target. Stage 5 moved the peak by
**+0.000559** — a rounding-scale move; the reprice lands almost entirely at year 1, which is its point.

**Year 1 rose 0.9504 → 0.9908, and it did NOT clear 1.00.** §3 below carries the reason and the number.

*Basis: shipped rows from `docs/evidence/noarb_338_2026-08-06/noarb_table_338.txt`; final rows from
`stage5/noarb/noarb_table_stage5.txt`; full-cohort rows from `stage5/OWNER_BASIS.txt`. All under the
CORRECTED #338 minimum-listing-tenure rule.*

---

## 2. PER-ENTRY-YEAR — where the cheapest buy-in sits now

Same cohort, final board only. Mean value at the peak year (4) ÷ mean value at year N.

| N — end of year | n (both years) | mean at yr 4 | mean at yr N | **ratio to peak** |
|---|---|---|---|---|
| 0 | 1,197 | 1,150.10 | 802.78 | 1.4327 |
| **1** | **1,197** | **1,150.10** | **795.40** | **1.4459** ← the maximum |
| 2 | 1,197 | 1,150.10 | 951.71 | 1.2085 |
| 3 | 1,197 | 1,150.10 | 1,081.40 | 1.0635 |
| 4 | 1,197 | 1,150.10 | 1,150.10 | 1.0000 |
| 5 | 1,139 | 1,165.24 | 1,142.79 | 1.0196 |

**In one sentence:** the cheapest buy-in on the final board is still at the **end of year 1**, but at
**1.446** to the peak rather than the amendment's 1.507 — **stage 5 made year 1 dearer**, which is the first
time in this act that number has moved back toward the 1.40 target.

*Basis: `stage5/noarb/goal_metrics_stage5.txt`, whole cohort, busts at 0 in every denominator.*

---

## 3. ⚠ THE OWNER DECISION STAGE 5 LEAVES ON THE TABLE — read this before ruling

**Stage 5 lands year 1 at `0.9908` on the ND teaching window and does NOT clear the 1.00 floor. One law,
and only one, accounts for the whole remaining distance.**

The law is *"no cell taught an INSTALLED price above its own entry anchor."* It is **this seat's own
construction**, introduced mid-build; the governing directive and Addendum 2 require only that the composed
surface `G·R` be **isotonic non-increasing in τ** — a statement about SHAPE, which is enforced separately
and independently of this cap. Rebuilding the identical surface with the cap lifted is a one-line diagnostic
and it was run:

| | shipped (law held) | diagnostic (law lifted) |
|---|---|---|
| **ND 2004–2022 year 1** | **0.990805** | **1.000020** |
| quiet starters 1–5 games | 0.8762 | 0.9166 |
| picks 21–64 | 0.9737 | 0.9948 |

**The cap is the entire remaining distance to the floor, to four decimal places.** It binds because for the
deep-pick quiet starters the measured discounted future genuinely **exceeds** the entry anchor — `F/A` runs
up to **1.17** at nonKPP picks 50–65 — exactly the class round 2 flagged (*"at picks 41–64 the gap is
dramatic: realized yr4 2.15 vs clock 0.58"*).

**The owner's own words bear directly on it:** *"Even young players should lose value in line with age. It's
career resources they're chewing up. **It's just the trend upward because often performance gives a greater
positive signal than aging takes.**"* A pick-50 quiet starter who played three games and whose measured
future is 1.17× his entry anchor is that sentence.

**The law was NOT lifted in this build**, because relaxing a self-imposed constraint at the exact moment it
is the only thing between the act and its target is tuning, not measurement. The diagnostic table
(`stage5/g5_table_NOCAP_DIAGNOSTIC.json`) was built, measured and **never installed**. Full argument on both
sides: `../stage5/CONSISTENCY_PASS.md §3`.

---

## 3b. THE RETURN-TRIGGER — still open, and stage 5 moved it BACK toward target

**Condition (b) of the ruling fired at stage 4 and the amendment moved it further out. Stage 5 reverses
part of that**, because it is the first stage that lifts year-1 values rather than cutting them.

| quantity | shipped | stage 4 | amendment 1 | **final (stage 5)** |
|---|---|---|---|---|
| **yr1-to-peak ratio** (cohort mean at peak yr 4 ÷ cohort mean at yr 1, same n = 1,197) | **1.400** | 1.4910 | 1.5068 | **1.4459** |

The number the ruling watches sits **+0.046** above target, down from **+0.107** at the amendment. Stage 5
closed **57%** of the gap the previous two stages opened, and it did so by lifting the denominator — the
year-1 quiet starters — rather than by touching the peak, which has already converged.

The historical text below is retained for the record; the per-cut chain now runs
**stage 3 → stage 4 → amendment 1 → stage 5**.

The rise was concentrated in the deep picks — and so is stage 5's reversal of it, which is the point:
the deep picks are where round 2 located the year-1 deficit.

| cut (each at ITS OWN peak year) | stage 3 | stage 4 | amendment 1 | **final (stage 5)** |
|---|---|---|---|---|
| picks 21–64 (deep, peak yr 6) | 1.5500 | 1.5692 | 1.6021 | **1.5110** |
| picks 1–20 (top, peak yr 4) | 1.4660 | 1.4677 | 1.4725 | **1.4270** |

*(The amendment-1 deep figure is restated as 1.6021 rather than the 1.6063 printed at that stage: it is
recomputed here at the cut's own peak year on the committed matrices, so the two columns are the same
measurement. The stage-3 and stage-4 entries are carried from the earlier build unchanged.)*

**Response (b) is what stage 5 was.** The follow-up design this section asked for at the amendment has now
been built and measured: a targeted year-1-side lift that leaves the peak alone. It moved yr1-to-peak from
1.5068 to **1.4459** without moving the peak (+0.000559), and it moved the deep cut hardest — 1.6021 to
1.5110 — which is where round 2 said the deficit was. What remains open is no longer *whether* to act
on year 1 — it is the single law in §3 above, which is worth the last **0.0092** of the year-1 ratio.

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

### THE DIALS — three numbers to move

| dial | value | mechanism | at 0 |
|---|---|---|---|
| `RL_PED_BAR` | 0.5 | *whose* record it is: `1 + PED_BAR × (1 − q)`, `q = ped(pick) × sit(depth)` | board returns to `6c9f8d3a` |
| `RL_SUR_W` | 5.0 | *what the record claims*: `+ SUR_W × s × u` | board returns to `b490ae8b`, byte-exact |
| **`RL_G5_W`** | **1.0** | *what the class is worth*: the anchor leg becomes `G · R · entry_anchor` | **board returns to `b56bbdde`, byte-exact through the full gate** |

All three live in `data/model_config.json` as valued owner dials (the manifest went 59 → 60 → 61 → **62**
variables). **None moves the ladder.** The settled ladder (`pvc_curve_v2.json`, `curve_md5` `18203822`, pick 1 = 3,000)
and the numéraire are byte-identical across both stages — asserted at all 64 picks in the workbook build —
so either dial can be re-ruled **without re-deriving any curve**.

### WHO MOVED

| | stage 4 | amendment 1 | **stage 5** |
|---|---|---|---|
| players moved (of 804) | 51 (6.34%) | 45 (5.60%) | **66 (8.21%)** |
| cuts / lifts | 41 / 10 | 38 / 7 | **0 / 66** |
| board total | 655,759 → 654,570 (−0.18%) | 654,570 → 652,183 (−0.365%) | **652,183 → 654,569 (+0.366%)** |
| largest cut | −17.36% (George Stevens) | −49.32% (George Stevens) | **none — no row falls** |
| largest lift | +23.36% (Mitch Podhajski) | +51.52% (Mitch Podhajski) | **+63.41% (Matt Hill)** |

**Stage 5 is the only stage in this act that cuts nobody.** All 66 movers are in the workbook verbatim on
the **"quiet-starter movers"** sheet, each with the taught `G` at his own cell, his cumulative career games,
his τ, his anchor before and after, and his evidence weight before and after.

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

## 5b. THE QUIET-STARTER AXIS — what stage 5 does

**The measurement it answers** (pre-measurement round 2): the year-1 sit-out leg splits in two, and only one
half is mispriced. The **zero-games** first-years are priced honestly — their retention matches their
realised outcomes in every pick band, largest gap +0.02, and 27% never play a game. The **quiet starters**
— 1 to 5 games, the evidence ramp barely engaged — are not: they are priced at **0.707** of entry against a
measured discounted future of **~0.95**, and at picks 41–64 the gap is dramatic.

**What was built.** A taught factor `G` multiplying the sit-out anchor leg at both anchor sites. It is a
continuous surface over **τ** (the engine's own round-driven clock) × **cumulative career games** × log-pick,
resolved per retention class and pooled where the class's own effective n falls under 35. It is taught ONCE
from the frozen baseline walk-forward book, then frozen as a committed table the engine loads — it is never
fitted at build.

**Three properties worth the owner's eye:**

1. **It is a state function, never a stamp.** The owner asked: *"in year 2, it would use year 1 + 2 data and
   outcomes, not just year 1?"* It does. A synthetic year-2 player with his year-1 season held **frozen**
   and only his year-2 games varied moves `G` across **1.020 … 1.251**. Nothing is stored per player.
2. **It phases out, and the fade was measured, not assumed.** The τ=2 and τ=3 knots were measured off the
   persisting-unproven classes *before* the fit, with the owner's phase-out shape used only as a prior. The
   taught fade reaches **exactly 1.000 at τ=6**. The counterfactual was built too: a hard drop at τ≥2 — the
   shape the owner rejected — deepens the persisting-unproven year-1→year-2 fall from −25.4% to **−30.8%**,
   and the taper recovers **all** of it (landed −25.1%).
3. **It is inert where it must be.** At the 6-game establishment bar the evidence weight is 1, the anchor
   leg drops out of the blend, and the surprise term's unresolved share is exactly 0 — so prices at the bar
   are **byte-identical** across the dial on every probe. Across the season rollover the clock is continuous
   and `G` steps by **1e-05**.

**What it costs, stated:** the quiet starters who *stay* unproven fall harder from year 1 to year 2 than
they did (−25.4% → −34.7% on that subset) — a lifted option value dies when the option does not progress.
Round 2 warned of exactly this; the taper halves it; it is printed rather than netted away.

---

## 6. ⚠ THE CALIBRATION CRITERION WAS NOT FULLY MET — and here is exactly where

*(This section is amendment 1's, unchanged. Stage 5 re-ran the same near-projection proof and it fails there
too, for a different and larger reason: stage 5 is a LIFT, and a player running AT his projection on 1-5
games IS a quiet starter — the exact population the act exists to reprice. 5 of the 6 band players move, the
largest by +43% continuous, and that is not granularity. It is filed as a disclosed criterion failure in
`../stage5/NEAR_PROJECTION_PROOF.txt`. The condition that IS binding — "no broad hit to young players" — is
met absolutely: stage 5 cuts nobody.)*

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

* **The store is untouched** — `37ced3ce45914e6feb00d27e26922e9a`, unchanged across all seven stages. Every
  stage in this act is read-only against player data. No record was edited, added or removed.
* **The deep frozen fits stand exactly as fitted, and are named:** the **peak model**, the **band tables**
  (`cm_400`), and **`q97m`** — all unmoved. The **year-zero surface** (`v0surf`) was refit **once**, in
  stage 3 only; stage 4, the amendment and stage 5 all leave it alone (`9713ec6c…`, unchanged), and each was
  proven not to be owed one — stage 5 re-verified by a declared refit at `RL_G5_W` **0 / 1.0 / 2.0**, all
  three reproducing the committed pickle at signature `3e8e50de5103`.
* **The ladder and the numéraire.** `pvc_curve_v2.json` `18203822`, pick 1 = 3,000. Byte-identical at all 64
  picks from stage 4 to final, asserted in the workbook build. Stage 5's own pick/player seam gate re-emits
  the implied ladder from the post-change book and finds the largest per-pick move attributable to stage 5
  is **1.887%**, inside the ±2% seam tolerance — **but not far inside**, and the reason it moves at all is
  stated rather than assumed away in `../stage5/LADDER_SEAM.txt`.
* **The top of the board.** Sheezel, Daicos, Jackson, Wanganeen-Milera: all unmoved by the amendment and by
  stage 5. Top-end ratio **3.556×** the numéraire, unchanged.
* **The established year-1 leg** (414 players, priced 1.2288) is **byte-identical** across stage 5 — it is
  fenced, and it is stage 6's scope. Its own measured future is **1.3470**, so it carries ≈ +0.059 of
  cohort year-1 value that this act does not claim.
* **Round 22 is not ingested.** The board is stamped `as_of_round: 21`.
* **Nothing merged, nothing registered.** No PR, no adoption, no registry entry. Main is untouched. The
  final board exists only on `landing/334-stage-b`. **Adoption is the owner's word.**

---

## 8. GATES — one line

**Parity 804/804, eps = 0** · **numéraire guard PASS, pick 1 = 3,000** · **self-test PASSED, 143 assertions,
0 FAIL, exit 0, 0 re-points** · **Guard 5 PASS** · **fit-class proven (v0surf unmoved, by three-signature
measurement at `RL_G5_W` 0 / 1.0 / 2.0)** · **dial-0 proven (`RL_G5_W=0` rebuilds `b56bbdde` byte-exact
THROUGH THE FULL GATE, manifest flipped and restored, md5-verified on the way out)** · **boundary clean
(prices at the 6-game bar byte-identical on all five probes, seam ratio 1.0000; rollover step in `G` 1e-05;
zero new cliffs in g=1..10)** · **band in range at every table's own peak** (whole 1.4327, 1–20 1.4293;
21–64 1.4713 outside but **byte-identical to the baseline**) · **entry-year rides: no machine STOP**
(largest excess over draft day +3.68pp/yr against a +5.00pp/yr line) · **within-class continuity PASS**
(realised max |Δln G|/Δτ 0.446 against the fitted taper's own max slope 0.536) · **convergence PASS**
(the year-1 gap between 1–20 and 21–64 falls 0.0523 → 0.0279).

Also green: book↔board parity, config-manifest check (**62 vars**), fut-label, zero-empty-club, env pin,
v0surf frozen-load assert (zero fits at build), recalculation-law probe (`G` responds to year-2 games with
year 1 frozen).

**Not green, and disclosed:** the year-1 landing floor (0.9908 against 1.00 — §3) and the near-projection
criterion as literally written (§6).

---

*Assembled 2026-08-07 · branch `landing/334-stage-b` · workbook `board_before_after.xlsx` (regenerated with
the amendment as a fifth stage column; per-row stage sums re-asserted on all 804 rows) · evidence under
`docs/evidence/act_334B_2026-08-07/` and `docs/evidence/noarb_338_2026-08-06/`.*
