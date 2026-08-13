# SHIPPING PACKET — ORDER 26B, THE DELIVERED-VALUE REDERIVATION

> ### ⚠ READ §16 FIRST — CORRECTION 1 (26B-C1)
> **Sections 1–15 below were written before CORRECTION ORDER 26B-C1 and their numbers are the
> PRE-CORRECTION numbers. They are left standing deliberately — the correction is published as an
> appendix with its own deltas table rather than by rewriting history.** A standing owner ruling
> (the force-majeure exclusion of `thomas-boyd` and `paddy-mccartin`, whole-draft slide) was missing
> from this order's brief, and applying it moves the ND curve. **§16 carries the corrected numbers and
> is the operative version.** Nothing in §16 changes any per-career delivered value, any pool pathway
> all-in, or any instrument verdict.

**NOTHING HERE IS LANDED.** No engine file was changed, no pin was moved, no board was rebuilt, no
score was ingested. Every number below was measured read-only against pinned bytes. The landing is a
separate order on the owner's word.

Branch `build/delivered-value` from `origin/main` @ `3b4df6f`, PR #489, **MERGE NOTHING**.
Authority: #334 comment 5269952564 (the thirteen owner rulings, "Go" filed the same hour) and
#334 comment 5270492281 (**OWNER RULING "Core, resume"**, which restarted the order at step 3).

---

## 1. THE ANSWER IN SIX SENTENCES

The order was to build a delivered-value scorer, certify it, and then rederive the pick curve and the
pool entry prices from it. **The scorer is exact** — it reproduces the engine's own production price
bit-for-bit on all 804 measurable board rows — and the owner ruled the identity gate satisfied at that
core. **The derived pick curve is startlingly close to today's shipped curve**: pinned at pick 1 =
3000 it lands within about 10 % of today's PVC at most picks, with a pre-anchor scale of 2,113 board
points at pick 1 and a single anchoring factor of ×1.4200. **The pool is where everything moves.** The
derived pool entry prices come in at **0.4554×** today's printed day-0 prices — a cut of about 55 % —
but at **1.1720×** the owner's own signed anchors, which is to say *the derivation lands almost exactly
where the owner's signed levels already sit, and it is today's printed day-0 that is the outlier*.
Both new mandatory instruments pass: every pathway's mark path rises from its derived entry value
toward a peak above it (MSD only under a named repair for a previously-disclosed instrument gap), and
**no pathway is a systematic guaranteed-loss hold**. The single most important caution in the packet is
that the median pool entrant's mark at career depth 4 is **exactly 0.000** — the pool is a barbell, and
every mean here is carried by its right tail.

---

## 2. WHAT WAS DELIVERED

| step | brief | status | artifacts |
|---|---|---|---|
| 0 | PREREG | **DONE**, committed before any measurement | `PREREG_ORDER26B.md` |
| 1 | THE IDENTITY GATE | **DONE** — bit-exact at the pricing core; owner-ruled SATISFIED | `GATE_REPORT.md`, `o26b_gate.py`, `GATE.json` |
| 2 | LAYER 1, THE HARVEST | **DONE**, pinned first-class dataset | `data/delivered_value/layer1_player_seasons.json` md5 `ad1229ea…` |
| 3 | LAYER 2, THE SCORER | **DONE** — 2,650 careers, one config block | `o26b_layer2.py`, `LAYER2.json` |
| 4 | THE DERIVATIONS | **DONE** — curve, relativities, pool ladders, MSD both ways | `o26b_derive.py`, `DERIVE.json` |
| 5 | COMPARISONS + BOTH INSTRUMENTS | **DONE** | `INSTRUMENTS_PRESTATEMENT.md`, `o26b_compare.py`, `COMPARE.json` |
| — | THE V5 APPENDIX (NOT-RULED) | **DONE** | `o26b_v5.py`, `V5_APPENDIX.json` |
| 6 | THE PACKET | **DONE** — this file | |

---

## 3. THE GATE STORY, AS IT NOW STANDS

Ruling 9 ordered the scorer certified against each panel player's **live board price** at ±2 %.
Measured, that gate failed: 2 of 12 on the panel, 9.0 % board-wide. **The failure was not in the price
function.** Step 1 proved that scoring a player's six projected band careers and blending them at WQ6
reproduces the engine's own `price6` **bit-exactly — 800/800 rows, max error 0.000e+00**. The distance
to the live board price is four further engine legs sitting on top of the production price, all named
and all attributed with a residual of **8.9e−16**:

| leg | what it is | where it bites |
|---|---|---|
| `_uncomp_prod` | the LEG-B un-compress map (`RL_UNCOMP=1`, s=0.10) | veterans: bontempelli ×1.0986, gawn ×1.1004 |
| the pedigree-pole blend | `pr + w·recover(perf,par)·max(0, po−pr)` in `raw_ev` | veterans and thin records alike |
| `ev/raw_ev` | `_prod_path`, `iso_eff`, position caps, sit-out and entry-anchor floors | thin records: visentini ×0.2146, ramm ×0.5806 |
| the L7 numéraire | a flat ×1.0524 on every row | everybody, uniformly |

**The owner ruled (comment 5270492281):** the gate is **SATISFIED AT THE PRICING CORE** — bit-exact
804/804 is stronger than the ±2 % bar — and the four legs are **player-STATE machinery, out of the
scorer's scope, deferred whole to the consumption-rewire act**. Steps 3–6 ran on that ruling.

**What the ruling did not change, and the landing act must carry:** the numéraire is the *only* one of
the four legs that is a pure unit change. The other three are state-dependent, and they are exactly the
reason the landing assert has the shape the owner gave it (§11).

---

## 4. THE DERIVED PICK CURVE, BESIDE TODAY'S

ND picks 1–64, entries 2004–2021, **busts kept at 0 in every denominator**, n = **1,143** careers.
Delivered value discounted to acquisition at flat 14 %, in board points, anchored at pick 1 = 3000.

**PRE-ANCHOR SCALE: 2,112.6 board points at pick 1. ANCHORING FACTOR: ×1.4200.**

| pick | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 | 50 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **DERIVED** | **3000** | **3048** | **2871** | **2118** | **1471** | **1540** | **952** | **997** | **725** | **568** | **328** | **218** |
| today's PVC | 3000 | 2999 | 2874 | 1881 | 1549 | 1460 | 1030 | 990 | 663 | 514 | 346 | 185 |
| derived / PVC | 1.000 | 1.016 | 0.999 | 1.126 | 0.950 | 1.055 | 0.924 | 1.007 | 1.094 | 1.105 | 0.947 | 1.180 |

**The two curves are close.** Over picks 1–64 the derived curve sits within **±6 % of today's at 37 of
the 64 picks and within ±12 % at 52 of them**; the largest single gap is **+18.0 % at pick 64**. It runs
*above* today's curve at picks 1–2, 4–5, 8–13, 20–43 and 59–64, and *below* at 3, 6–7, 14–19 and 44–58.
The shape statistics:

| | derived | today |
|---|---|---|
| pick 1 → pick 3 | −4.31 % | −4.20 % |
| pick 1 / pick 10 | 1.948 | 2.055 |
| pick 64 / pick 1 | 0.0727 | 0.0617 |

**Per-pick n is 18 for every pick from 1 to 61** (16 at pick 62, 15 at 63, 14 at 64) — the raw per-pick
cohort means are published beside the smoothed curve in `DERIVE_out.txt`, as PREREG P2.6 pre-committed.

**THE SMOOTHER, BY NAME.** Not invented here: it is the **shipped year-zero aggregator**, imported from
`docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py::kernel_raw` (md5
`f2c81da18e02`) — a Gaussian kernel over `log(pick)` whose bandwidth grows from 0.10 in 0.02 steps
until the effective n reaches 35 (cap 0.60), then a weighted mean.

**Two honest blemishes on the curve, disclosed rather than smoothed away:**

1. **It is not monotone.** Nine picks read above their predecessor, and **pick 2 (3048) reads above the
   anchored pick 1 (3000)** — the raw cohort mean at pick 2 (2,349.6) genuinely exceeds pick 1
   (2,064.3) on 18 careers apiece. No isotonic projection was applied, because applying one would have
   hidden the fact. The shipped fitter PAVA-projects and then hard-sets pick 1; a landing act that
   wants a monotone object should say so and apply the shipped step, with the ascents disclosed first.
2. **14.8 % of the curve is projected tail**, value-weighted (Ruling 8's disclosure). It is remarkably
   even across the pick range — 16.3 % over picks 1–10, 11.8 % over picks 46–64 — so it moves the level
   rather than the shape. By tier: the core (≤2014) is **0.6 %** tail, exactly the "small projected
   tail" Ruling 8 anticipated; the augmented tier (2015–2021) is **37.0 %**.

### Positional relativities by pick band (position = the ACQUISITION slot, Ruling 5)

| band | MID | SD | SF | KPD | KPF | RUCK | all-in |
|---|---|---|---|---|---|---|---|
| 1–10 | 1.275 | 0.724 | 0.585 | 0.606 | 0.653 | 1.255 | 2139 |
| 11–20 | 1.287 | 1.016 | 0.583 | 0.632 | 0.834 | 1.315 | 1131 |
| 21–30 | 1.329 | 0.705 | 0.506 | 0.677 | 0.830 | 2.199 | 807 |
| 31–45 | 1.327 | 0.496 | 0.671 | 0.790 | 0.742 | 2.310 | 589 |
| 46–64 | 1.115 | 0.450 | 1.048 | 1.643 | 0.903 | 1.196 | 292 |
| n | 422 | 180 | 211 | 125 | 145 | 60 | 1143 |

**THE RECONCILIATION LAW IS ASSERTED IN CODE.** Ruling 13 requires the position-weighted mean to equal
the all-in curve at every pick. Measured: **max |weighted mean / all-in − 1| = 2.220e−16** over picks
1–64, and `o26b_derive.py` **halts** if it ever exceeds 1e−12. The law holds by construction — the
positional curves are renormalised onto the all-in at each pick — and the assert exists so a future
change cannot break it silently.

---

## 5. THE POOL — DERIVED v0 BESIDE TODAY'S PRINTED PRICE AND THE SIGNED ANCHOR

**The construction, in three declared multiplications and no others:**
`derived v0 (board) = cell_v0 × ANCHOR_FACTOR (1.4200) × NUMÉRAIRE (1.0524)`.
The numéraire is `pick_redenomination.json::factor` — the same flat ×1.0524 the gate measured on every
board row and the same factor the owner's signed levels already carry into the engine-value sites.

### 5.1 The headline, whole pool (n = 1,201 entrants)

| ratio | n | mean | p05 | median | p95 | **aggregate (sum/sum)** |
|---|---|---|---|---|---|---|
| derived / **printed day-0** | 1201 | 4.7172 | 0.1487 | 0.4354 | 7.2099 | **0.4554** |
| derived / **signed anchor** | 1201 | 1.2277 | 0.6557 | 1.1382 | 2.0653 | **1.1720** |
| printed day-0 / signed anchor | 1201 | 2.9361 | 0.1841 | 2.5176 | 6.9563 | **2.5733** |

*(26A measured printed/anchor at 2.6498 on its own population; **2.5733 aggregate / 2.5176 median**
here is the same fact on this order's population, arrived at independently.)*

**Read that table once more.** The derivation, built from nothing but historical careers and the
engine's own season price, independently lands within **17 %** of the owner's signed pool levels — and
**55 % below** what the board prints for the same players on day one. The wedge 26A found is confirmed
from the other side, by an object that never saw it.

### 5.2 By day-0 position (pooled across pathways)

| pos | n | derived | printed d0 | anchor | der/prn (median) | der/anch (median) | prn/anch (median) |
|---|---|---|---|---|---|---|---|
| MID | 296 | 336.6 | 621.6 | 282.1 | 0.4823 | 0.9427 | 2.3928 |
| SD | 232 | 304.2 | 640.4 | 230.0 | 0.4169 | 1.3542 | 2.9338 |
| SF | 245 | 216.8 | 534.5 | 246.4 | 0.4353 | 1.0128 | 2.3563 |
| KPD | 154 | 266.2 | 1015.3 | 285.6 | 0.2896 | 0.7871 | 3.5866 |
| KPF | 130 | 263.0 | 951.4 | 258.2 | 0.2681 | 1.1939 | 3.9730 |
| **RUCK** | 144 | 437.7 | 349.2 | 234.0 | **1.4730** | 1.9595 | 1.3303 |

**The cut is hardest for KPF (0.268) and KPD (0.290) and lightest for RUCK, where the derivation says
the board is *under*-pricing (1.473).** That is exactly the positional ordering ORDER 26A's `v0/anchor`
spread pointed at, arrived at independently.

### 5.3 Pathway all-ins, ND-pick equivalents, and the derived-vs-printed-vs-anchor comparison

| path | n (fit) | raw all-in | p05 | median | p95 | shrunk | pathway borrow | **ND-pick equiv** | derived | printed d0 | anchor | der/prn | der/anch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **MSD** | 29 | 391.4 | 0.0 | 0.0 | 1688.8 | 324.8 | 34.1 % | **44** | 499.3 | 508.9 | 354.7 | 0.9811 | 1.4080 |
| **ND>64** | 115 | 239.1 | 0.0 | 0.3 | 1702.7 | 234.1 | 11.5 % | **50** | 339.6 | 799.9 | 312.6 | 0.4246 | 1.0866 |
| **SSP** | 24 | 223.9 | 0.0 | 3.0 | 346.1 | 213.2 | 38.5 % | **54** | 301.6 | 417.3 | 325.2 | 0.7228 | 0.9276 |
| **RD** | 611 | 211.7 | 0.0 | 0.0 | 1302.3 | 211.3 | 2.4 % | **54** | 314.9 | 728.9 | 274.8 | 0.4320 | 1.1459 |
| **PDA** | 38 | 145.5 | 0.0 | 0.0 | 1191.3 | 159.8 | 28.3 % | **63** | 232.9 | 592.1 | 202.1 | 0.3934 | 1.1527 |
| **UNR** | 46 | 99.0 | 0.0 | 0.0 | 386.1 | 122.9 | 24.6 % | **> 64** | 153.8 | 280.0 | 68.4 | 0.5492 | 2.2479 |
| **PDN** | 24 | 43.2 | 0.0 | 0.0 | 225.4 | 102.0 | 38.5 % | **> 64** | 116.1 | 569.6 | 101.0 | 0.2038 | 1.1491 |
| **IRE** | 47 | 48.9 | 0.0 | 0.0 | 206.7 | 84.6 | 24.2 % | **> 64** | 107.7 | 586.8 | 111.6 | 0.1836 | 0.9657 |
| **PDS** | 21 | 16.6 | 0.0 | 0.0 | 97.9 | 91.4 | 41.7 % | **> 64** | 108.0 | 637.6 | 58.9 | 0.1694 | 1.8328 |
| *ND 1-64 (ref)* | 1143 | 614.9 | | | | | | *the curve itself* | | | | |

`> 64` means the pathway's all-in sits **below the derived pick-64 value of 218** — off the bottom of
the national-draft curve.

**THE DISPERSION IS THE STORY.** Every one of those `median` columns except SSP reads **0.0**. The pool
mean is not a typical pool player; it is a handful of survivors averaged over a majority who deliver
nothing. `RD` p95 is 1,302 against a median of 0.0. Any consumer of these numbers who reads the mean
without the median will price the pool wrong.

### 5.4 The pool positional v0 table, with every cell's n and borrowing share

Ruling 12's ladder: own cell → shrunk pathway all-in × all-pool positional lens → all-pool.
**K = 15**, which is not a new constant: it is the owner's own signed-level shrinkage constant
(`pvc_curve_v2.json::pool_levels.k`), reused rather than a second one invented.
The all-pool positional lens: MID 1.1587 · SD 1.0372 · SF 0.6746 · KPD 0.8467 · KPF 0.8312 · RUCK 1.4282.

Values in **ladder currency** (multiply by 1.0524 for board currency); *borrow* = the share of the cell's
v0 that did **not** come from the cell's own careers.

| path | MID | SD | SF | KPD | KPF | RUCK |
|---|---|---|---|---|---|---|
| **RD** | 273 (n=180, 8 %) | 332 (108, 12 %) | 248 (121, 11 %) | 278 (83, 15 %) | 246 (61, 20 %) | 504 (58, 21 %) |
| **SSP** | 525 (6, 71 %) | 267 (4, 79 %) | 168 (4, 79 %) | 243 (2, 88 %) | 220 (6, 71 %) | 396 (2, 88 %) |
| **MSD** | 696 (10, 60 %) | 504 (3, 83 %) | 275 (2, 88 %) | 440 (2, 88 %) | 302 (6, 71 %) | 596 (6, 71 %) |
| **IRE** | 132 (3, 83 %) | 109 (29, 34 %) | 74 (2, 88 %) | 70 (7, 68 %) | 79 (4, 79 %) | 151 (2, 88 %) |
| **PDA** | 215 (11, 58 %) | 432 (7, 68 %) | 100 (8, 65 %) | 178 (2, 88 %) | 142 (5, 75 %) | 247 (5, 75 %) |
| **PDN** | 148 (2, 88 %) | 107 (9, 62 %) | 68 (7, 68 %) | 148 (5, 75 %) | 120 (0, **100 %**) | 194 (1, 94 %) |
| **PDS** | 114 (6, 71 %) | 96 (6, 71 %) | 73 (3, 83 %) | 100 (5, 75 %) | 108 (0, **100 %**) | 174 (1, 94 %) |
| **UNR** | 389 (5, 75 %) | 151 (3, 83 %) | 104 (2, 88 %) | 138 (7, 68 %) | 128 (3, 83 %) | 110 (26, 37 %) |
| **ND>64** | 386 (30, 33 %) | 355 (16, 48 %) | 135 (30, 33 %) | 221 (15, 50 %) | 363 (14, 52 %) | 689 (10, 60 %) |

**Two cells — PDN KPF and PDS KPF — have n = 0 and are 100 % borrowed.** They are printed rather than
suppressed, because a v0 that exists entirely on the strength of other cells must say so on its face.
**RD is the only pathway that prices positionally on its own data** (2.4 % pathway-level borrowing,
7–21 % at the cell level), exactly as Ruling 12 anticipated.

---

## 6. THE MSD / YOUNG-PATHWAY QUESTION, BOTH WAYS

| | all-in | p05 | median | p95 | anchored |
|---|---|---|---|---|---|
| **WAY A** — MSD scored with Ruling 8's gated projected tails | **391.4** | 0.0 | 0.0 | 1688.8 | 556 |
| **WAY B** — MSD scored observed-only, positional cells from the all-pool position curves × an MSD pathway offset | **165.9** | 0.0 | 0.0 | 800.4 | 236 |

**WAY A / WAY B = 2.3593** — the gated tails **raise** the MSD all-in by **+135.9 %**. MSD's
value-weighted tail share is **0.5761**: more than half of Way A's number is projection, not record.
The MSD pathway offset (observed-only MSD ÷ observed-only all-pool) is **0.9731** — i.e. on realised
record alone, **MSD is an ordinary pool pathway**, and everything that makes it look exceptional is its
young population's projected future.

| pos | n | WAY A v0 | WAY B v0 | A / B | borrowing under A |
|---|---|---|---|---|---|
| MID | 10 | 490.1 | 196.6 | 2.4930 | 60 % |
| SD | 3 | 354.8 | 177.0 | 2.0039 | 83 % |
| SF | 2 | 193.4 | 113.3 | 1.7062 | 88 % |
| KPD | 2 | 310.0 | 144.2 | 2.1503 | 88 % |
| KPF | 6 | 212.7 | 115.8 | 1.8361 | 71 % |
| RUCK | 6 | 419.5 | 231.8 | 1.8098 | 71 % |

### RECOMMENDATION: **WAY B, STRUCTURAL BORROWING.**

This was pre-committed in PREREG §4 P4.2 before any of these numbers existed, and the numbers make the
case stronger rather than weaker:

1. **Way A is 57.6 % projection.** MSD's fit-window population is 29 careers, of which the young ones
   supply most of the value through tails the record has not yet earned. A pathway price that is
   mostly forecast is a pathway price that moves when the forecast moves.
2. **The instruments back it.** MSD is the **only** arm whose mark path never rises above 1.0 at any
   depth (§8, limb 1 red) — the market itself does not yet validate Way A's level.
3. **Way B is auditable per cell.** Every MSD cell under Way B decomposes into a published all-pool
   position curve and one published scalar offset (0.9731). Way A's cells rest on 2–10 careers apiece
   with 60–88 % borrowing.
4. **The known MSD caveat travels with it.** The signed MSD level already carries a documented
   "+4.7–8.4 % completion optimism" caveat (`pvc_curve_v2.json::pool_levels`). Layering a
   projection-heavy tail on top of an already-optimistic level compounds the same error twice.

**The Way-A numbers are published in full anyway**, in this section and in `DERIVE.json::msd`, so the
owner can rule the other way on the numbers rather than on a summary.

---

## 7. THE MARK-PATH PROGRESSION TEST

**The form was fixed in `PREREG_ORDER26B.md` §6 and detailed in `INSTRUMENTS_PRESTATEMENT.md` §3,
committed and pushed in its own commit (`c913dfd`, 2026-08-12) BEFORE the harness existed.**

With the derived v0s as day-0 and the walk-forward matrix's historical marks as numerators:
`m(d) = Σ marks at depth d / Σ derived day-0`, dead **zeroed and kept** in the denominator.
**PASS iff the path attains a maximum at some d ≥ 2 above its own entry reading — the ND shape.**

| arm | n @ d4 | d0 | d1 | d2 | d3 | d4 | d5 | d6 | peak | at d | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **ND 1-64** | 1200 | 0.967 | 1.204 | 1.368 | **1.431** | 1.402 | 1.342 | 1.170 | 1.431 | 3 | **PASS** *(the reference shape)* |
| **RD** | 655 | 0.993 | 1.088 | 1.095 | **1.204** | 1.171 | 1.102 | 0.953 | 1.204 | 3 | **PASS** |
| **SSP** | 24 | 1.324 | 1.321 | **1.547** | 1.284 | 0.960 | 0.458 | 0.279 | 1.547 | 2 | **PASS** [thin] |
| **MSD** | 44 | *n/a* | 0.688 | 0.661 | 0.619 | 0.693 | **0.947** | 0.403 | 0.947 | 5 | **FAIL literal / PASS repaired** |
| **IRE** | 48 | 1.173 | 1.363 | 1.174 | 1.275 | 1.399 | 1.221 | **1.722** | 1.722 | 6 | **PASS** |
| **PDA** | 38 | 0.767 | 0.955 | 1.100 | 1.289 | **1.517** | 0.701 | 1.081 | 1.517 | 4 | **PASS** [thin] |
| **PDN** | 24 | 0.854 | 1.111 | 0.880 | 0.921 | 0.820 | **1.250** | 0.880 | 1.250 | 5 | **PASS** [thin] |
| **PDS** | 21 | 0.784 | 0.615 | 0.286 | 0.771 | **1.095** | 0.857 | 0.409 | 1.095 | 4 | **PASS** [thin] |
| **UNR** | 46 | 0.356 | 0.501 | 0.680 | 1.086 | **1.306** | 0.805 | 0.289 | 1.306 | 4 | **PASS** |
| **ND>64** | 113 | 0.878 | 1.077 | 1.026 | 1.150 | 1.073 | 1.033 | **1.302** | 1.302 | 6 | **PASS** |

**Every pathway's path is printed above, as ordered.** The pool cohort curves **do** rise from their
derived entry toward a peak above it, like the ND's — which is precisely the property the brief said
the derived v0s had to produce and today's printed day-0 prices do not.

**MSD's `m(0)` is undefined, and it is not MSD's fault.** The emitter builds `yrs` from draft year + 1
on every route while `cohort()` for MSD is the draft year itself, so an MSD entrant's depth 0 always
resolves *before* his first emitted year and every row leaves the denominator. This is the
**previously-disclosed instrument gap** recorded as anomaly 5 of ORDER 26A's `SUMMARY.md`. The literal
reading therefore cannot be evaluated and reads FAIL; the **repaired** reading, re-basing the entry
reference on d1, gives **PASS** (0.688 → 0.947 at d5). Both are printed; neither replaces the other.

**Dispersion behind every verdict** — the per-entrant ratio `mark(d) / derived v0`:

| arm | peak d | p05 | median | p95 | mean | | d=4 median | d=4 p95 |
|---|---|---|---|---|---|---|---|---|
| ND 1-64 | 3 | 0.000 | **0.644** | 5.488 | 1.395 | | 0.431 | 5.892 |
| RD | 3 | 0.000 | **0.000** | 7.595 | 1.232 | | 0.000 | 7.387 |
| SSP | 2 | 0.000 | 0.392 | 8.748 | 1.489 | | 0.000 | 6.690 |
| MSD | 5 | 0.000 | 0.000 | 3.836 | 0.833 | | 0.000 | 3.107 |
| IRE | 6 | 0.000 | 0.000 | 8.535 | 1.583 | | 0.000 | 7.794 |
| PDA | 4 | 0.000 | 0.000 | 10.081 | 1.070 | | 0.000 | 10.081 |
| PDN | 5 | 0.000 | 0.000 | 11.075 | 1.061 | | 0.000 | 1.275 |
| PDS | 4 | 0.000 | 0.000 | 9.348 | 1.045 | | 0.000 | 9.348 |
| UNR | 4 | 0.000 | 0.000 | 7.447 | 0.897 | | 0.000 | 7.447 |
| ND>64 | 6 | 0.000 | 0.000 | 5.831 | 1.038 | | 0.000 | 5.345 |

**The median pool entrant is worth nothing at his own pathway's peak depth.** Only the national draft
has a living median (0.644 at d3). This is the mortality identity ORDER 26A derived, seen directly.

**PREREG §6's literal `mean_i` wording gives a different reading on four arms** (SSP, MSD, PDA, PDN and
ND>64 — the mean-of-ratios path peaks at d0 or d1 for SSP/PDA/PDN/ND>64). Both readings are printed in
`COMPARE_out.txt`; the sum/sum reading is primary because §6's own words are "all-in (dead kept at 0 in
the numerator, entry kept in the denominator)", which is sum/sum language. **The disagreement is
reported, not resolved silently.**

---

## 8. THE REVERSE NO-ARB TEST

**The exact test form was stated in the artifact and dated BEFORE it was computed**
(`INSTRUMENTS_PRESTATEMENT.md` §4, commit `c913dfd`, 2026-08-12):

> A pathway **FAILS** (is a systematic guaranteed-loss hold) iff **both** (1) `m(d) < 1` for **every**
> d = 1…6 at which it has any denominator, **and** (2) the upper end of a 95 % bootstrap interval on
> `max_{d≥1} m(d)` is also below 1. **PASS = no pathway fails.** Bootstrap: B = 2000, **entrant-level**
> resampling, seed **20260812**, 97.5th percentile. n < 8 → printed but marked UNRELIABLE; no FAIL on
> fewer than 8 entrants.

| arm | n | d1 | d2 | d3 | d4 | d5 | d6 | max d≥1 | boot lo | **boot hi** | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ND 1-64 | 1444 | 1.204 | 1.368 | 1.431 | 1.402 | 1.342 | 1.170 | 1.431 | 1.339 | 1.530 | **PASS** |
| RD | 691 | 1.088 | 1.095 | 1.204 | 1.171 | 1.102 | 0.953 | 1.204 | 1.040 | 1.442 | **PASS** |
| SSP | 52 | 1.321 | 1.547 | 1.284 | 0.960 | 0.458 | 0.279 | 1.547 | 0.848 | 2.678 | **PASS** |
| **MSD** | 106 | 0.688 | 0.661 | 0.619 | 0.693 | 0.947 | 0.403 | **0.947** | 0.578 | **1.806** | **PASS** — *limb 1 RED* |
| IRE | 57 | 1.363 | 1.174 | 1.275 | 1.399 | 1.221 | 1.722 | 1.722 | 0.840 | 3.989 | **PASS** |
| PDA | 51 | 0.955 | 1.100 | 1.289 | 1.517 | 0.701 | 1.081 | 1.517 | 0.845 | 3.169 | **PASS** |
| PDN | 43 | 1.111 | 0.880 | 0.921 | 0.820 | 1.250 | 0.880 | 1.250 | 0.694 | 3.035 | **PASS** |
| PDS | 21 | 0.615 | 0.286 | 0.771 | 1.095 | 0.857 | 0.409 | 1.095 | 0.425 | 2.655 | **PASS** |
| UNR | 59 | 0.501 | 0.680 | 1.086 | 1.306 | 0.805 | 0.289 | 1.306 | 0.466 | 2.520 | **PASS** |
| ND>64 | 120 | 1.077 | 1.026 | 1.150 | 1.073 | 1.033 | 1.302 | 1.302 | 0.916 | 2.106 | **PASS** |

### VERDICT: **PASS — no pathway is a systematic guaranteed-loss hold at the derived entry price.**

**The test is able to go red, and one arm came close.** MSD's limb 1 **is** red — every one of its
`m(d)` readings sits below 1.0 — and it is saved only by limb 2, whose bootstrap upper limit is 1.806
on 106 entrants. **That is a genuine warning about MSD**, and it is the second independent reason §6
recommends structural borrowing over MSD's own gated tails: the pathway whose derived price the tails
inflate is the one pathway the market has not yet paid back.

---

## 9. THE NAMED ROWS

Delivered value in board points, discounted to acquisition, flat 14 %.

| player | pathway | day-0 pos | entry | delivered **to date** | delivered **TOTAL** | tail % | **derived v0** | printed day-0 | signed anchor | live board `v` |
|---|---|---|---|---|---|---|---|---|---|---|
| **willem-duursma** | ND pick 1 | MID | 2025 | 53.8 | 3531.0 | 98.5 % | **3157.2** | 3484.6 | 3484.6 | 3977 |
| **callum-moore** | RD pick 9 | KPF | 2015 | 5.2 | 5.2 | 0.0 % | **258.8** | 1773.4 | 216.8 | **NOT ON BOARD** |
| **harrison-ramm** | MSD pick 3 | KPD | 2025 | 0.0 | 696.1 | 100 % | **463.3** | 946.0 | 354.7 | 545 |
| **vigo-visentini** | RD pick 5 | RUCK | 2023 | 56.0 | 588.0 | 90.5 % | **530.0** | 359.8 | 270.5 | 182 |
| **jai-newcombe** | MSD pick 2 | MID | 2021 | 2016.3 | 3992.5 | 49.5 % | **732.5** | 688.0 | 354.7 | 4883 |

- **willem-duursma** — the owner's named gate row. His delivered-value total (3,531) and his derived
  pick-1 v0 (3,157) bracket his printed day-0 (3,485); the gate's `mine/board_v` read **1.0184**.
- **callum-moore** — **not on the live board**, so his delivered-value score is the object used, per the
  order. He delivered **5.2 board points** across three seasons from a rookie-draft pick 9. The board
  printed him at **1,773** on day one — **341×** what he went on to deliver. He is the single clearest
  illustration in the packet of why pool day-0 needs rederiving.
- **harrison-ramm** — a 2025 MSD entrant. **Delivered to date: 0.0.** His entire 696 is Ruling 8's
  projected tail. Derived v0 463 against a printed day-0 of 946 and a signed anchor of 355.
- **vigo-visentini** — the gate's most violent row (`ev/raw` 0.2146). The derivation prices him at
  **530** against a live board `v` of **182**: the delivered-value object says the board's sit-out
  machinery is holding him far below what a RUCK acquisition slot has historically been worth.
- **jai-newcombe** — the pool success case, and the argument that pathway means are low because of
  **mortality, not because live pool players are cheap**. He delivered **3,992.5** — **above the derived
  pick-1 all-in of 3,000**, from an MSD slot whose derived cell v0 is 732.5. PREREG P5.5 predicted only
  "above the derived pick-30 all-in" (725); he clears that by 5.5×.

---

## 10. THE V5 AGE-LADDER APPENDIX — **NOT RULED**

The owner's parked fifth ladder (`rl_model.py::_V5_KNOTS`), resurfaced on real numbers. Run through the
**engine's own** `age_disc()` / `disc_factor()` path at `RL_AGE_DISC_MODE=5`, never a reimplemented
ladder. **flat-14 is the live config and the sole basis of every conclusion above.**

| | flat-14 | V5 | V5 / flat |
|---|---|---|---|
| ND cohort-mean delivered value | 614.9 | 691.5 | **1.1245** |
| pre-anchor scale at pick 1 | 2112.6 | 2378.2 | **1.1257** |
| anchoring factor to pin 3000 | 1.4200 | 1.2614 | 0.8883 |
| all-pool all-in | 196.2 | 212.2 | 1.0820 |

**Direction: V5 RAISES young delivered values.** Its rates below age 22 (12.0–13.5 %) sit *below* flat
14 %, and a lower discount raises present value. By entry age, the median V5/flat ratio: **≤18 → 1.1172**,
19 → 1.0857, 20–21 → 1.0272, 22–25 → 1.0000, 26+ → 0.9806.

**Post-anchor the curve barely moves**: max |V5/flat − 1| across picks 1–64 is **1.35 %**. The pathway
ranking is **identical** under both ladders and the largest ND-pick-equivalent move is **2 picks**
(RD 54→55, SSP 54→56, MSD 44→45, PDA 63→64, the rest unmoved). **V5 is a level dial, not a shape dial**,
and it changes no conclusion in this packet.

---

## 11. THE CAVEAT — NOTHING LANDED

**Nothing in this packet is wired into anything.** No engine file changed, no pin moved, no board was
rebuilt. Every harness asserts its pins at entry *and* at exit and would halt if a byte under
`engine/` had moved.

**The landing act** — a separate order on the owner's word — wires these derived v0s in as the
**printed day-0 price**, with the permanent assert the owner ruled at comment 5270492281:

```
printed day-0  ==  derived v0  ×  the display numéraire
```

with the **fresh-entrant legs-collapse itself asserted at landing**. This packet supplies the right
side of that identity in exactly that decomposition — §5's three declared multiplications,
`cell_v0 × 1.4200 × 1.0524` — so the landing act has nothing to reconstruct.

**Three things the landing act must know before it writes that assert:**

1. **It cannot be written against `ev()` as the engine stands.** The four legs of §3 sit between the
   production price and the shipped board price, and three of them are state-dependent. The owner's
   ruling deferred them to the consumption-rewire act; the assert's *form* is safe, but the *site* it
   is written at must be the day-0 site, before those legs apply.
2. **The derived curve is not monotone** (§4). If the landing wants a monotone printed object it must
   apply the shipped PAVA step explicitly and disclose the nine ascents it removes.
3. **The two n = 0 cells** (PDN KPF, PDS KPF) print a 100 %-borrowed price. They must either land with
   that provenance visible or be ruled unpriceable — never land silently.

---

## 12. THE PREREG, SCORED — §2 THROUGH §7

The committed prereg's §2–§7 stood unscored at the stop. They are scored here **against the text as
committed**, not re-registered. §1 and P5.1 were scored at the gate (`GATE_REPORT.md` §7).

### §2 — THE ALL-IN PICK CURVE

| # | prediction | measured | verdict |
|---|---|---|---|
| P2.1 | pre-anchor cohort mean at pick 1 ∈ [1800, 3800], point 2600; anchoring factor ∈ [0.79, 1.67], point 1.15 | **2112.6**; factor **1.4200** | **HIT** (both in band) |
| P2.2 | derived steeper at the very top: pick 1→3 drop **> 12 %** | **−4.31 %** (today −4.20 %) | **MISS** — the derived curve is no steeper at the top than today's |
| P2.3 | derived sits *below* the shipped curve through the early picks and crosses above between picks 18–34 (point 26), staying above through 64 | it is **above** from pick 1; it oscillates — below at 3, 6–7, 14–19, 44–58; above elsewhere; it does **not** stay above from any crossing | **MISS**, on all three limbs |
| P2.4 | pick64/pick1 ∈ [0.08, 0.18]; anchored pick 64 ∈ [240, 540] | **0.0727**; **218.2** | **MISS** (both just below the band) |
| P2.5 | pick1/pick10 ∈ [1.9, 3.0] | **1.948** | **HIT** |
| P2.6 | name the smoother, print per-pick n, publish raw means beside smoothed; expect n ≈ 18–20 for picks 1–20 | smoother named + md5-pinned; raw means published; **n = 18 at every pick 1–20** | **HIT** and **HONOURED** |
| P2.7 | reconciliation law holds ≤ 0.5 % by construction, any breach a HALT | **2.220e−16**, asserted in code at 1e−12 | **HIT** |

**§2 verdict: 3 HIT, 4 MISS.** The misses are all one mistake: I predicted the derived curve would have
a *materially different shape* from today's, and it does not. That is the most useful thing §2 could
have told the owner, and I got it wrong in the direction that makes today's ND curve look better.

### §3 — THE POOL PATHWAYS

| # | prediction | measured | verdict |
|---|---|---|---|
| P3.1 | ranking RD > SSP > MSD > UNR ≈ IRE > PDA > PDN > PDS | **MSD > SSP > RD > PDA > UNR > IRE > PDN > PDS** | **MISS** — the top three are inverted and PDA is four places high |
| P3.1b | ND-pick equivalents: RD 48–62, SSP 55–64, MSD 58–64, and PDA/PDN/PDS/IRE/UNR all below pick 64 | RD **54** ✔ · SSP **54** ✘ (one pick out) · MSD **44** ✘ · PDA **63** ✘ · PDN/PDS/IRE/UNR **> 64** ✔ | **PART HIT** (2 of 5 limbs) |
| P3.2 | whole-pool derived/printed ∈ [0.28, 0.55], point 0.40 | aggregate **0.4554**, median 0.4354 | **HIT** |
| P3.3 | cut hardest KPF/KPD, lightest RUCK; RUCK > 0.60; KPF < 0.30; ordering RUCK > MID ≈ SD > SF > KPD > KPF | RUCK **1.4730** ✔ · KPF **0.2681** ✔ · order **RUCK > MID > SF > SD > KPD > KPF** | **HIT** — both numeric limbs; the ordering is exact but for SD and SF, which swap and sit within 4 % of each other |
| P3.4 | whole-pool derived/anchor ∈ [0.8, 1.6], point 1.10 | aggregate **1.1720**, median 1.1382 | **HIT** |
| P3.5 | PDS, PDN, IRE cells borrow ≥ 60 %; RD borrows < 15 % in every position; MSD ≥ 50 % in ≥ 4 of 6 | PDS 71–100 % ✔ · PDN 62–100 % ✔ · **IRE 34 % at SD (n=29)** ✘ · **RD 15.3/19.7/20.5 % at KPD/KPF/RUCK** ✘ · MSD 60–88 %, all six ✔ | **PART HIT** (3 of 5 limbs) |

**§3 verdict: 3 HIT, 1 MISS, 2 PART.** The three quantitative headline predictions — the size of the cut
against printed day-0, the positional pattern of the cut, and the closeness to the signed anchors — all
landed. The pathway *ordering* did not.

### §4 — MSD BOTH WAYS

| # | prediction | measured | verdict |
|---|---|---|---|
| P4.1 | gated tails raise the MSD all-in by **10–35 %** | **+135.9 %** (391.4 vs 165.9) | **MISS** — direction right, magnitude ~4× the top of the band |
| P4.2 | recommendation will be structural borrowing, pre-committed | recommended **structural borrowing** (§6) | **HONOURED** — and no deviation was needed |

### §5 — NAMED ROWS

| # | prediction | measured | verdict |
|---|---|---|---|
| P5.1 | duursma `mine/board_v` ∈ [0.90, 1.06] | 1.0184 | **HIT** *(scored at the gate)* |
| P5.2 | callum-moore delivered **< 60**; printed day-0 **more than 5×** it | **5.2**; printed **1773.4 = 341×** | **HIT**, both limbs |
| P5.3 | harrison-ramm delivered value **to date** < 120; ratio to printed 545 < 0.25 | **to date 0.0**, ratio **0.000** | **HIT on the object the prereg named.** On the Ruling-8 TOTAL (696.1, ratio 1.277) it is a **MISS** — both are printed and both are scored, see below |
| P5.4 | vigo-visentini delivered **< 40** against printed 182 | **to date 56.0**; TOTAL **588.0** | **MISS** on both objects |
| P5.5 | jai-newcombe delivered **> 1500**, above the derived pick-30 all-in (725) | **3992.5** — above the derived **pick-1** all-in of 3000 | **HIT**, emphatically |

**On P5.3, owned by name:** the prereg wrote "delivered value **to date**" for harrison-ramm but
"delivered value" plainly for visentini and moore. Ruling 8's scorer produces a *total* that includes a
gated projected tail. Rather than pick whichever object made the prediction look better, both are
printed in §9 and both are scored here. On the total, P5.3 misses by a factor of 5.8.

### §6 — THE TWO INSTRUMENTS

| # | prediction | measured | verdict |
|---|---|---|---|
| P6.1a | every pathway with n ≥ 40 passes the progression test | ND, RD, IRE, UNR, ND>64 pass; **MSD fails the literal reading** (undefined m(0) — the disclosed MSD debut-year gap) and passes the repaired one | **MISS on the literal reading, HIT on the repaired** |
| P6.1b | `m(0) ≈ 1.0` **by construction** | ND 0.967, RD 0.993 — close, but **not by construction** | **PREREG ERROR, owned**: m(0) would only be 1.0 by construction with the *printed* v0 as denominator. With the derived v0 it is a measurement — and it happening to land near 1.0 for the two big arms is a result, not an identity |
| P6.1c | `m* ∈ [1.4, 2.6]` for RD, MSD and SSP | RD **1.204** ✘ · MSD **0.947** ✘ · SSP **1.547** ✔ | **MISS** (1 of 3) |
| P6.2 | at least one thin pathway (PDS or PDN) **fails** | both **PASS** on the primary reading (PDN fails on the secondary mean-of-ratios reading) | **MISS** on the primary reading |
| P6.3a | **no pathway fails** the reverse no-arb test | **no pathway fails** | **HIT** |
| P6.3b | the tightest pathway is **PDS** | the tightest is **MSD** (max m 0.947, the only limb-1-red arm); PDS's max is 1.095 | **MISS** |

### §7 — THE V5 APPENDIX

| # | prediction | measured | verdict |
|---|---|---|---|
| P7.1 | V5 **raises** delivered value for age-18 entrants, by **4–12 %** at the all-in level | direction **up** ✔; entry-age ≤18 median ratio **1.1172 (+11.7 %)** ✔; ND cohort-mean all-in **+12.45 %** — 0.45 pp above the band | **HIT on the age-18 object, marginal MISS at the all-in level.** Scored as a HIT on direction and a near-miss on magnitude, and the 0.45 pp overshoot is named rather than rounded away |
| P7.2 | V5 changes no §3 sign and moves no pathway's ND-pick equivalent by more than 6 picks | pathway ranking **identical**; max move **2 picks** | **HIT**, both limbs |

### THE SCORECARD

**HIT 12 · PART 2 · MISS 11 · PREREG ERROR 1 · HONOURED 2.**

Every quantitative prediction about **where the pool lands** (P3.2, P3.3, P3.4) hit. Every prediction
about the **shape of the ND curve** (P2.2, P2.3, P2.4) missed, in the same direction: I expected the
derivation to disagree with today's curve and it broadly agrees with it. Every prediction about
**pathway ordering and the instruments' fine detail** (P3.1, P6.1c, P6.2, P6.3b) missed. The prereg was
right about the levels and wrong about the shapes.

---

## 13. DEVIATIONS FROM THE PREREG, OWNED BY NAME

1. **The window floor at 2004 was not in the prereg.** Ruling 8 sets no lower bound; I imposed
   `entry_year ≥ 2004`, excluding **106 entries from 2003**, because the store's scoring data begins in
   2005 so a 2003 entry's year 1 is structurally unobservable, and 2004 is the engine's own curve
   teaching-window floor (`YR_LO`). Taken **before** any curve was computed. Declared in
   `CFG.window_floor_note`.
2. **`prod_floor` is not applied to a projected tail.** `dp.v_at_peak` applies it to a whole career;
   a tail is a fragment, and flooring a fragment would invent value the band machinery never
   projected. Declared in `CFG.tail_no_floor`. Taken before any tail was scored.
3. **The dual-position season bar rule was not anticipated in the prereg.** 1,877 of the 11,484
   Layer-1 season rows carry a dual label (`SF/MID`, `SD/MID`, `KPF/RUCK`, …) for which Layer 1
   records `position_group = null`. The first Layer-2 pass **dropped them** — 16.3 % of the league's
   played seasons — and the harness's own counter caught it. They are now resolved through the
   **engine's own** `_fit_bar` rule (split on `/`, collapse, take the lowest-REPL member). This was a
   correction to a defect, made after seeing a counter but before seeing any derived quantity; it is
   disclosed here because a reader is entitled to know the first pass was wrong.
4. **A repaired reading was added to the progression test after seeing MSD's `n/a`.** The literal
   reading is printed unchanged and first; the repair is labelled, and its cause is a
   *previously-documented* instrument gap (26A anomaly 5), not a new discovery of convenience. Still:
   the repair was written after the result, and that is a deviation.
5. **The mean-of-ratios secondary reading was added** so PREREG §6's literal `mean_i` wording could be
   checked against the sum/sum primary. It changes four verdicts, and the disagreement is reported.
6. **`INSTRUMENTS_PRESTATEMENT.md` adds operational detail §6 left open** (depth axis, bootstrap
   spec, PASS predicates). It was committed and pushed in its own commit *before* the harness existed
   so the ordering is a fact in the history. It weakens nothing in §6.
7. **The linear-games-weighting sensitivity was also run whole-population**, beyond Ruling 10's "named
   cases only". The named-case table is the ruling's deliverable; the aggregate line is printed
   separately and labelled "beyond the ruling's ask".

---

## 14. ANOMALIES

1. **The pool median is 0.000 at depth 4 for every pathway.** Not a defect — a fact, and the most
   consequential one in the packet. Any consumer of a pool mean must carry the median beside it.
2. **The derived curve is not monotone**, and pick 2 reads above the anchored pick 1 (§4).
3. **Two ladder cells have n = 0** (PDN KPF, PDS KPF) and are 100 % borrowed (§5.4).
4. **The MSD debut-year gap** (26A anomaly 5) is still live in the emitter and now bites a second
   instrument. It should be fixed in the emitter, not worked around a third time.
5. **The augmented tier is 37.0 % projected tail** at the ND curve level against the core's 0.6 %.
   Ruling 8 ordered exactly this and ordered it disclosed; it is disclosed. But it means the 2015–2021
   half of the curve's evidence is materially forecast, and a landing act should decide whether that
   is acceptable *before* the curve is printed anywhere.
6. **`ND>64` reads as the second-richest pathway** (all-in 239.1, ND-pick equivalent 50) on 115 fit-window
   careers. Its signed level was recently amended by owner ruling (#334 comment 5262928754) to price at
   its derived level with the pick-curve cap removed; this derivation is independent evidence on that
   decision and agrees with it (derived/anchor 1.0866).
7. **`per_entrant_O25R4.json` lived only in the shared scratchpad.** It is now copied into this
   evidence tree with its md5 asserted, so step 5 is reproducible. A shared substrate that exists in
   one ephemeral directory is a durability hazard for every act that reads it.

---

## 15. FILES

| file | what |
|---|---|
| `PREREG_ORDER26B.md` | pre-registration, committed before any measurement |
| `GATE_REPORT.md` · `o26b_gate.py` · `GATE.json` | step 1, the identity gate and the zero-residual attribution |
| `o26b_layer1.py` · `data/delivered_value/` | step 2, the durable assumption-free harvest |
| `o26b_layer2.py` → `LAYER2.json`, `LAYER2_out.txt` | step 3, the valuation layer and its one config block |
| `o26b_derive.py` → `DERIVE.json`, `DERIVE_out.txt` | step 4, curve · relativities · pool ladders · MSD both ways |
| `INSTRUMENTS_PRESTATEMENT.md` | step 5's test forms, dated and committed before the computation |
| `o26b_compare.py` → `COMPARE.json`, `COMPARE_out.txt` | step 5, comparisons and both instruments |
| `o26b_v5.py` → `V5_APPENDIX.json`, `V5_APPENDIX_out.txt` | the V5 age-ladder appendix (NOT RULED) |
| `per_entrant_O25R4.json` | the walk-forward matrix, copied for durability (md5 `3c6ffcde…`) |
| `SHIPPING_PACKET_26B.md` | this file |

---

# 16. CORRECTION 1 (26B-C1) — THE OWNER'S FORCE-MAJEURE EXCLUSION

**Filed 2026-08-13. This section is the operative version of every number it restates.**
Sections 1–15 are left exactly as they were written; nothing is rewritten in place.

## 16.1 What was missed, and whose fault it was

A **standing owner ruling** (register, v533-era) excludes **`thomas-boyd`** (ND pick 1, 2013) and
**`paddy-mccartin`** (ND pick 1, 2014) from pick valuation as **force majeure**. Owner, verbatim:

> "those players were pick 1 KPF busts, so heavily bias the pool against them, however one retired
> early with depression, and another with concussion issues. It's a force majeure situation…"

and, on being shown this order's output:

> "I was under the impression that Thomas Boyd and Paddy McCartin were excluded from the pick
> valuation… It was force majeure, so it seemed wrong for them to contribute to data for pick 1 when
> those acts of god are unlikely to contribute to pick 1 again."

**ORDER 26B's brief did not carry the ruling, and this build included both rows in the pick-1 cohort.**
Re-filed at [#334 comment 5274640130](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5274640130),
which records the failure as the seat's, not the build's — and records that it is the **third ruling
this week found living as register prose instead of a machine check**. That is why this correction
ships as **named config plus a halting assert**, not as a patched number.

## 16.2 The mechanics, as the owner amended them

**WHOLE-DRAFT SLIDE.** In each affected draft year every ND draftee slides **up one pick**: natural
pick N is attributed to slid pick N−1. The excluded key (natural pick 1) is dropped from every cohort
input entirely. A natural pick 65 slides to 64, **enters** the ND 1-64 fit and **leaves** the ND>64
pathway for that year. **Slid effective picks are computed BEFORE the ND/pool split.**
**The store is never edited and Layer 1 is never edited** — the slide is a derivation-time attribution
rule only, and Layer 1 keeps the natural pick.

It ships as `CFG.force_majeure` in `o26b_layer2.py` — keys, reason, provenance, mechanics, slide
years, scope — which builds **one** attribution map emitted to `LAYER2.json::attribution`. The
deriver, the comparison harness and the V5 appendix all **read** that map; none recomputes the slide,
so no two of them can drift.

### The ruling is now an assert. The deriver HALTS on any violation.

| limb | check | result |
|---|---|---|
| **(a)** | neither excluded key appears in **any** ND or pool cohort input, at any pick | **PASS** |
| **(b)** | each slide year's **pick-N cohort holds the natural pick-(N+1) entrant** | **PASS** — 2013: 60 pick positions checked; 2014: 64 |
| **(c)** | a natural pick 65 slid to 64, entered the ND fit, left ND>64 | **PASS** — 2014 `daniel-butler` |

Each limb is proved non-vacuous (limb (b) halts if it checks nothing; limb (c) halts if no slide year
has a natural 65 at all).

### A correction to the correction order, measured rather than assumed

The correction order anticipated that **ND>64 would lose two entrants**. **It loses one.** The **2013
national draft ends at natural pick 61** — it has no 65th selection — so only 2014's `daniel-butler`
slides into the ND fit. The assert is written over the natural-65s that **exist**; asserting two would
have been asserting a fact about the world that is false.

### An independent cross-check the correction order did not ask for

The walk-forward matrix's own emitter **already applies this ruling** (`meta.force_majeure`,
`meta.slide_years`, per-row `pick_stored`/`pick_slid`). This order's attribution map was built
separately, from Layer 1. They are now asserted to agree on **the arm of all 1,565 ND rows** and **the
slid pick of all 1,444 ND 1-64 rows**, with both excluded keys **absent from the matrix entirely**.
Two independent implementations of the same owner ruling, agreeing. (ND>64 picks are deliberately not
compared: the matrix pins every one of them to its `pool_pick` sentinel of 65, so its `pick` there is
a marker, not a draft position.)

## 16.3 Who replaced boyd and mccartin — the owner's question, answered

| year | excluded (natural pick 1) | pos | delivered | → natural pick 2, now the pick-1 cohort member | pos | delivered |
|---|---|---|---|---|---|---|
| 2013 | `thomas-boyd` | KPF | **46.6** | **`joshua-kelly`** | MID | **3,592.8** |
| 2014 | `paddy-mccartin` | KPF | **44.0** | **`christian-petracca`** | MID | **3,621.7** |

**The pick-1 cohort gains 7,123.9 board points across the two rows** (90.6 → 7,214.5) on a cohort of
18. Two KPF careers ended by acts of god are replaced by two of the best midfield careers of the era.

## 16.4 THE DELTAS — old vs corrected

### The curve (anchored at pick 1 = 3000)

| pick | 1 | 2 | 3 | 5 | 7 | 10 | 15 | 20 | 30 | 40 | 50 | 64 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **CORRECTED** | **3000** | **2800** | **2697** | **1854** | **1376** | **1423** | **857** | **931** | **657** | **529** | **301** | **198** |
| old (§4) | 3000 | 3048 | 2871 | 2118 | 1471 | 1540 | 952 | 997 | 725 | 568 | 328 | 218 |
| **delta** | 0.00 % | **−8.16 %** | −6.05 % | **−12.47 %** | −6.46 % | −7.63 % | −9.94 % | −6.57 % | −9.35 % | −6.79 % | −8.19 % | −9.44 % |
| today's PVC | 3000 | 2999 | 2874 | 1881 | 1549 | 1460 | 1030 | 990 | 663 | 514 | 346 | 185 |
| **corrected / PVC** | 1.000 | 0.934 | 0.938 | 0.986 | 0.888 | 0.974 | 0.832 | 0.941 | 0.991 | 1.030 | 0.870 | 1.068 |

Every pick below 1 falls **relative to the anchor** because the anchor itself rose: the pick-1 head is
now much larger, so pinning it at 3000 divides everything else by more.

### The head, the factor, and the shape

| | old | **corrected** |
|---|---|---|
| **PRE-ANCHOR SCALE at pick 1** | 2,112.6 | **2,284.6** (**+8.14 %**) |
| **ANCHORING FACTOR** | ×1.4200 | **×1.3131** |
| ND fit population | 1,143 | **1,142** (−2 excluded, +1 slid in) |
| pick 1 → pick 3 drop | −4.31 % | **−10.09 %** |
| pick 1 / pick 10 | 1.948 | **2.109** |
| pick 64 / pick 1 | 0.0727 | **0.0659** |
| monotonicity ascents | 9 (incl. **pick 2 above pick 1**) | **7 — and the pick-2 ascent is GONE** |
| within ±6 % of today's PVC | 37 of 64 | 31 of 64 |
| ND curve tail share (value-weighted) | 14.79 % | 14.78 % |

**The owner's watchdog expectation is confirmed on all three limbs.** The pick-1 cohort mean **rises
materially** (+8.14 % at the smoothed head). **The top of the curve steepens** — the pick 1→3 drop
more than doubles, from −4.31 % to −10.09 %, and pick 1 / pick 10 rises from 1.948 to 2.109. And the
**embarrassment of §4 is gone**: the derived curve no longer reads pick 2 *above* the anchored pick 1.
That artefact was two force-majeure careers dragging the pick-1 cohort below pick 2's, and the ruling
removes it.

### Positional relativities — moved, but barely

| band | MID | SD | SF | KPD | KPF | RUCK |
|---|---|---|---|---|---|---|
| 1–10 | 1.275→**1.256** | 0.724→**0.703** | 0.585→**0.589** | 0.606→**0.604** | 0.653→**0.684** | 1.255→**1.259** |
| 11–20 | 1.287→1.299 | 1.016→1.012 | 0.583→0.582 | 0.632→0.626 | 0.834→0.825 | 1.315→1.312 |
| 21–30 | 1.329→1.322 | 0.705→0.704 | 0.506→0.503 | 0.677→0.683 | 0.830→0.833 | 2.199→2.217 |
| 31–45 | 1.327→1.323 | 0.496→0.495 | 0.671→0.681 | 0.790→0.802 | 0.742→0.748 | 2.310→2.292 |
| 46–64 | 1.115→1.113 | 0.450→0.454 | 1.048→1.040 | 1.643→1.649 | 0.903→0.906 | 1.196→1.202 |

Only the 1–10 band moves materially, and in the direction the substitution predicts: **two KPF rows
out and two MID rows in at pick 1** lifts KPF's relativity (0.653 → 0.684, because the surviving KPF
rows at the top are no longer averaged against two zeros) and trims MID and SD. **The reconciliation
law still holds at 2.220e−16 and is still asserted.**

### Pathway all-ins and ND-pick equivalents

| path | n old → new | raw all-in old → new | ND-pick equiv old → new |
|---|---|---|---|
| RD | 611 → 611 | 211.7 → 211.7 | 54 → **54** |
| SSP | 24 → 24 | 223.9 → 223.9 | 54 → **53** |
| MSD | 29 → 29 | 391.4 → 391.4 | 44 → **44** |
| PDA | 38 → 38 | 145.5 → 145.5 | 63 → **63** |
| UNR | 46 → 46 | 99.0 → 99.0 | > 64 → **> 64** |
| IRE | 47 → 47 | 48.9 → 48.9 | > 64 → **> 64** |
| PDN | 24 → 24 | 43.2 → 43.2 | > 64 → **> 64** |
| PDS | 21 → 21 | 16.6 → 16.6 | > 64 → **> 64** |
| **ND>64** | **115 → 114** | **239.1 → 240.0 (+0.37 %)** | 50 → **50** |

**No pool pathway's delivered value changes** — the slide touches only ND rows. `ND>64` is the sole
mover, losing `daniel-butler` to the ND fit; its all-in ticks up 0.37 % because the entrant it lost
was below its mean. The `> 64` label now means "below the derived pick-64 value of **198**" (was 218).
`SSP` moves one pick because the *curve* moved beneath it, not because SSP did.

### Pooled derived-vs-printed-vs-anchor

| ratio | old | **corrected** |
|---|---|---|
| derived / printed day-0, **aggregate** | 0.4554 | **0.4211** |
| derived / printed day-0, median | 0.4354 | **0.4027** |
| derived / **signed anchor**, aggregate | 1.1720 | **1.0841** |
| derived / signed anchor, median | 1.1382 | **1.0525** |
| n | 1,201 | 1,200 |

**The correction moves the derivation CLOSER to the owner's signed anchors, not further** — the
whole-pool aggregate falls from 1.1720 to **1.0841**, and the median from 1.1382 to **1.0525**. The
headline finding of §5 is strengthened, not weakened: the derived pool entry prices and the owner's
signed levels are now within **8.4 %** of each other in aggregate, against a printed day-0 that is
2.5× the anchors.

**Per position, derived / printed day-0 (median):** MID 0.4823→**0.4460** · SD 0.4169→**0.3855** ·
SF 0.4353→**0.4025** · KPD 0.2896→**0.2678** · KPF 0.2681→**0.2479** · RUCK 1.4730→**1.3621**. The
ordering and every §5.2 conclusion are unchanged; all six shift down by the same ~7 % anchor-factor
effect.

### Both instruments, re-run

| arm | progression old → new | peak old → new | reverse no-arb old → new | bootstrap hi old → new |
|---|---|---|---|---|
| ND 1-64 | PASS → **PASS** | 1.431 → **1.552** (d3) | PASS → **PASS** | 1.530 → 1.660 |
| RD | PASS → **PASS** | 1.204 → **1.302** (d3) | PASS → **PASS** | 1.442 → 1.560 |
| SSP | PASS → **PASS** | 1.547 → **1.674** (d2) | PASS → **PASS** | 2.678 → 2.896 |
| MSD | FAIL literal / PASS repaired → **same** | 0.947 → **1.025** (d5) | PASS → **PASS** | 1.806 → 1.953 |
| IRE | PASS → **PASS** | 1.722 → **1.862** (d6) | PASS → **PASS** | 3.989 → 4.314 |
| PDA | PASS → **PASS** | 1.517 → **1.640** (d4) | PASS → **PASS** | 3.169 → 3.428 |
| PDN | PASS → **PASS** | 1.250 → **1.352** (d5) | PASS → **PASS** | 3.035 → 3.283 |
| PDS | PASS → **PASS** | 1.095 → **1.184** (d4) | PASS → **PASS** | 2.655 → 2.872 |
| UNR | PASS → **PASS** | 1.306 → **1.412** (d4) | PASS → **PASS** | 2.520 → 2.725 |
| ND>64 | PASS → **PASS** | 1.302 → **1.408** (d6) | PASS → **PASS** | 2.106 → 2.277 |

**Every verdict is unchanged**, on both instruments and on both readings; the same five arms
(SSP, MSD, PDA, PDN, ND>64) still disagree between the sum/sum and mean-of-ratios readings. All peaks
rise by roughly the anchor-factor ratio (1.3131 / 1.4200 = 0.925), because a lower derived day-0
denominator lifts every `m(d)`.

**One thing got WEAKER and it must be said.** §8 reported MSD's limb 1 as **red** — every `m(d) < 1` —
and used that as the live demonstration that the reverse no-arb predicate can go red. After the
correction **MSD's peak crosses above 1.0** (1.0246 at d5) and **no arm has limb 1 red any more**. The
predicate is still able to fire — it is a plain comparison — but the packet no longer has a worked
example of it firing. §6's recommendation of structural borrowing for MSD loses this second supporting
argument; the first (Way A is 57.6 % projection on 29 careers) and the third (the standing completion-
optimism caveat) are untouched, and **the recommendation stands**.

### The named rows

| player | delivered (to date / TOTAL) | derived v0 old → **new** | printed day-0 | signed anchor |
|---|---|---|---|---|
| `willem-duursma` | 53.8 / 3,531.0 | 3,157.2 → **3,157.2** *(unchanged: pick 1 is the anchor)* | 3,484.6 | 3,484.6 |
| `callum-moore` | 5.2 / 5.2 | 258.8 → **239.3** | 1,773.4 | 216.8 |
| `harrison-ramm` | 0.0 / 696.1 | 463.3 → **428.4** | 946.0 | 354.7 |
| `vigo-visentini` | 56.0 / 588.0 | 530.0 → **490.1** | 359.8 | 270.5 |
| `jai-newcombe` | 2,016.3 / 3,992.5 | 732.5 → **677.3** | 688.0 | 354.7 |

**Confirmed as the correction order asked: every named row's delivered value is unchanged.** The only
movement is the cohort-level effect — the four pool rows' derived v0s fall by exactly the anchor-factor
ratio (×0.925), and `willem-duursma` does not move at all because pick 1 *is* the anchor. `jai-newcombe`
still clears the derived pick-1 all-in.

### MSD both ways, and the V5 appendix

**MSD both ways is completely unchanged** (Way A 391.4, Way B 165.9, A/B 2.3593) — MSD is a pool
pathway and the slide does not touch it. **V5 is unchanged in every conclusion**: the V5/flat-14 ND
cohort-mean ratio is still **1.1245**, the max post-anchor shape move is 1.32 % (was 1.35 %), the
pathway ranking is still identical, and the max ND-pick-equivalent move is still **2 picks**. V5's own
pre-anchor head rises 2,378.2 → 2,571.5 in step with flat-14's.

## 16.5 PREREG RE-SCORED — the items the correction moves

Re-scored against the committed prereg text, not against a revised expectation.

| # | prediction | old verdict | **corrected** | what moved |
|---|---|---|---|---|
| **P2.1** | pre-anchor ∈ [1800, 3800] pt 2600; factor ∈ [0.79, 1.67] pt 1.15 | HIT | **HIT** | head 2112.6→**2284.6**, factor 1.4200→**1.3131** — both still in band, and the head moves *toward* the 2600 point estimate |
| **P2.2** | pick 1→3 drop **> 12 %** | MISS (−4.31 %) | **MISS (−10.09 %)** | still a miss, but the gap closes from 7.7 pp to **1.9 pp**. The correction removes most of the error |
| **P2.3** | below the shipped curve through the early picks, crossing above between picks **18–34** (point 26), staying above | MISS on all three limbs | **PART HIT** | the derived curve is now **below** today's from pick 2 through the early range (limb 1 **HIT**), and its main crossing above runs **picks 32–41** — the crossing lands at **32, inside the predicted 18–34 window** (limb 2 **HIT**). It still does not stay above through 64 (below again 42–61, above 62–64), so limb 3 **MISS** |
| **P2.4** | pick64/pick1 ∈ [0.08, 0.18]; anchored pick 64 ∈ [240, 540] | MISS | **MISS** (0.0659; 197.6) | moves *further* from the band |
| **P2.5** | pick1/pick10 ∈ [1.9, 3.0] | HIT (1.948) | **HIT (2.109)** | more comfortably inside |
| **P2.6** | per-pick n ≈ 18–20 for picks 1–20 | HIT | **HIT** (n = 18 at every pick 1–20) | unchanged; picks 61–64 now carry n 14–17 |
| **P2.7** | reconciliation ≤ 0.5 %, else HALT | HIT | **HIT** (2.220e−16) | unchanged |
| **P3.1b** | SSP ND-pick equivalent ∈ 55–64 | MISS (54) | **MISS (53)** | moves one further out |
| **P3.2** | whole-pool derived/printed ∈ [0.28, 0.55] pt **0.40** | HIT (0.4554) | **HIT (0.4211)** | moves **toward** the point estimate |
| **P3.3** | RUCK > 0.60, KPF < 0.30, ordering | HIT | **HIT** (RUCK 1.3621, KPF 0.2479) | unchanged |
| **P3.4** | whole-pool derived/anchor ∈ [0.8, 1.6] pt **1.10** | HIT (1.1720) | **HIT (1.0841)** | lands almost exactly on the point estimate |
| **P6.1c** | m* ∈ [1.4, 2.6] for RD, MSD, SSP | MISS (1 of 3) | **PART (2 of 3)** | SSP 1.674 ✔, **MSD 1.025 still ✘**, RD 1.302 still ✘ but now much closer to 1.4 |
| **P6.3b** | the tightest pathway is **PDS** | MISS | **MISS** | MSD is still tightest (max 1.025 vs PDS 1.184) |

**Unchanged verdicts:** P3.1a (ordering), P3.5, P4.1, P4.2, P5.1–P5.5, P6.1a, P6.1b, P6.2, P6.3a,
P7.1, P7.2. §12's other rows stand.

**REVISED SCORECARD: HIT 13 · PART 3 · MISS 9 · PREREG ERROR 1 · HONOURED 2** (was 12 / 2 / 11 / 1 / 2).

**The correction improved the prereg's score, and that is worth saying plainly rather than quietly
banking.** Three predictions the packet had recorded as misses (P2.2's magnitude, P2.3's direction,
P6.1c's band) move toward or into their predicted ranges once the owner's ruling is applied. §12's
summary line — *"the prereg was right about the levels and wrong about the shapes"* — needs amending:
**it was right about the levels, and it was more right about the shapes than a build missing a
standing owner ruling could show.** The shape predictions were being scored against a curve whose
pick-1 cohort carried two careers the owner had already ruled out.

## 16.6 ANOMALIES FROM THE CORRECTION

1. **ND>64 loses ONE entrant, not the two the correction order anticipated.** The 2013 national draft
   ends at natural pick 61. Measured, asserted over the natural-65s that exist, and reported.
2. **The reverse no-arb test no longer has a worked example of limb 1 firing** (§16.4). The predicate
   is unchanged and still able to fire; the packet's demonstration of it is gone.
3. **Picks 61–64 now carry n 14–17** against 18 everywhere else, because the 2013 draft contributes to
   picks 1–60 after the slide instead of 1–61. The deep tail of the curve is one career thinner than
   it was.
4. **This is the third ruling this week found living as register prose instead of a machine check.**
   The exclusion now ships as named config with a halting assert. **The remaining risk is not in this
   order**: any other standing ruling that exists only as register prose is invisible to a build seat
   that was not told about it, and no assert in this packet can catch that class of failure. The
   register-wide sweep is a separate act and it should be ordered.
5. **`o26b_compare.py` now cross-checks two independent implementations of the same ruling** and
   halts if they disagree (§16.2). That check found nothing wrong here, but it is the pattern the
   other rulings need.
