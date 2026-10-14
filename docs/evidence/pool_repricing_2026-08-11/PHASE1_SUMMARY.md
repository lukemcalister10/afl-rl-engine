# POOL REPRICING — BUILD PHASE 1: DERIVE AND REPORT

**Order:** #334 comment 5253523232 (ORDER 17). **Directive of record:**
`docs/directives/POOL_REPRICING_DIRECTIVE_2026-08-11.md` (1,255 lines, md5 `2913c122c3d8e02319c2856dc593a7ac`).
**Branch:** `build/pool-repricing-phase1`, cut from main `d3d5f55`. **Nothing is wired. The shipped
board has not moved.**

## IDENTITY — asserted at start and at end

| anchor | expected | measured | |
|---|---|---|---|
| `origin/main` | `d3d5f55` | `d3d5f5592e57ffbe0f90fe5744c7c6fb17392b82` | OK |
| live board `data/rl_build/rl_app_data.json` | `94f1fec5…` | `94f1fec59f99c59d5890d5975c79fa9b` | OK |
| store | `d9a24282` | `d9a24282357cf3083b1640466e3ecd83` | OK |
| instrument `noarb_table_338.py` | `0f822035…` | `0f8220351c64c56ccfa90c60edcdfa5f` | **UNMODIFIED** |

**One identity note, recorded rather than passed over.** The session's working tree opened on branch
`directive/pool-repricing-d3` at `db688f6`, six commits ahead of main. The directive file is
**byte-identical** on both (`2913c122…`), so the specification is the same document; the build branch
was nevertheless cut from `d3d5f55` as ordered.

## WHAT WAS DERIVED

Every figure below comes from a committed, re-runnable script in this directory. Every script names
its own instrument in its header.

| script | output | task |
|---|---|---|
| `phase1_population.py` | `PHASE1_POPULATION.json` · `phase1_population_out.txt` | 1 |
| `phase1_derive.py` | `PHASE1_DERIVE.json` · `phase1_derive_out.txt` | 2, 3, 4 |
| `phase1_retention.py` | `PHASE1_RETENTION.json` · `phase1_retention_out.txt` | 5 |
| `phase1_age.py` | `PHASE1_AGE.json` · `phase1_age_out.txt` | 6 |
| `phase1_consequence.py` | `PHASE1_CONSEQUENCE.json` · `phase1_consequence_out.txt` | 7 |
| `PREREG_ORDER17.md` | the predictions, written before any measurement | — |

---

# 1 — THE POPULATION QUESTION (D8 iii). **IT IS DETERMINABLE, AND THE ANSWER IS SPLIT.**

**The directive says the question "cannot be determined from the derivation script".** That is correct
about `d13_derive.py` — and `d13_derive.py` is the **consumer**. It reads `d13_normcells.json`. The
**producer** of that file, `d13_norm_harvest.py`, survives in the repo and its population gate is
explicit. **The seat reports this as a correction to the directive, not a disagreement with its ruling.**

The gate (`d13_norm_harvest.py:43-52`) has **no `_pool` exclusion**. Entry turns on gate 2,
`pick or _ft`, and that is not uniform across pool pathways:

| pathway | n | in R's population | why |
|---|---|---|---|
| ND>64 | 122 | **122 (100%)** | `_ft=True`, plus a stored pick |
| RD | 691 | **685 (99.1%)** | `_ft=True`, plus a stored pick 1–51 |
| MSD | 106 | **88 (83.0%)** | `_ft=False` **but carries a stored pick 1–20** |
| SSP · IRE · PDA · PDN · PDS · UNR | 283 | **0** | pickless mechanisms, `_ft=False` |

**Both of the directive's "two possibilities, both bad" are true at once, of different pathways:**
for the **895** rows that were in `R`, `_h_cut` **charged the same effect a second time**; for the
**283** that were not, it was a **bolt-on to a surface read outside its evaluated range**.

**This is a positive reason for the D8 ruling, not merely a consistent one.** A single pool-wide
retention cannot inherit from `R`, because `R` already contains three of the nine pathways and none of
the other six. Deriving one object on pool history is the only construction correct for both halves.

**A second correction: the [1,90] clamp the directive named as the obstacle is INERT.** The rookie
ladder in store `d9a24282` tops out at **51**, and **zero rows** in the whole store carry a stored pick
above 90. The clamp was not what made the question hard; gate 2 was.

**What is NOT determinable, stated rather than papered over:**
1. `d13_normcells.json` is **absent from the repo**, so this is a faithful **gate replay**, not a
   read-back. It reproduces the gate exactly; it cannot prove the 2026-07-03 run met an identical roster.
2. The harvest ran on engine `af1fc6aa` against a store since moved to `d9a24282`. **Row-level**
   membership at that engine is not recoverable. The pathway-level verdict is robust because it turns
   on `_ft` and on pick presence, both structural; the exact counts would differ.
3. `_double_count` is not carried on the matrix and is not reconstructible.
4. Depth-cell counts are not reconstructible (`listed_through` unavailable).

---

# 2 — LAYER 1: the positionless all-in value per pathway

Basis: the full career profile via `realised_full` / `structural_values`, **called from the harness**,
never re-implemented. **ND 1-64 profile = 1.0252 — that is the calibration target, not 1.00.**

| pathway | n | profile | vs ND | shrunk | vs ND | level now | **DERIVED** | change |
|---|---|---|---|---|---|---|---|---|
| RD | 688 | 0.5233 | 0.5104 | — | 0.5104 | 261.6 | **133.5** | −49.0% |
| SSP | 52 | 1.0287 | 1.0034 | — | 1.0034 | 252.8 | **253.7** | +0.3% |
| MSD | 106 | 0.9418 | 0.9187 | — | 0.9187 | 286.8 | **263.5** | −8.1% |
| IRE | 57 | 0.2006 | 0.1956 | — | 0.1956 | 133.4 | **26.1** | −80.4% |
| PDA | 51 | 0.4279 | 0.4174 | — | 0.4174 | 194.3 | **81.1** | −58.3% |
| PDN | 43 | 0.1422 | 0.1387 | — | 0.1387 | 123.0 | **17.1** | −86.1% |
| **PDS** | 21 | 0.1259 | 0.1228 | **0.2908** | **0.2837** | 145.0 | **41.1** | −71.6% |
| UNR | 59 | 0.3493 | 0.3408 | — | 0.3408 | 103.7 | **35.3** | −65.9% |
| ND>64 | 120 | 0.5477 | 0.5342 | — | 0.5342 | 266.1 | **142.2** | −46.6% |
| ALL POOL | 1197 | 0.5218 | 0.5089 | | | | | |

**PDS shrunk toward the pool aggregate at K=15** as ruled: `w = 21/(21+15) = 0.5833`,
`0.5833×0.1259 + 0.4167×0.5218 = 0.2908`. No other pathway is shrunk; every other holds n ≥ 43.

---

# 3 — LAYER 2: the player v0, keyed on **pathway × position × age only**

**No pick axis exists and none was invented** — `effpk` returns the constant `POOL_PICK = 65` for every
pool entrant. The age key is the third key and is multiplicative (`_b_shape`/`_b_factor`), currently
**flat at 1.0**; section 6 measures whether it should stay flat.

**The donor is whole-pool only** (the D4 pre-check failed for the national draft). Whole-pool shape:
MID 1.2476 · SD 0.8846 · SF 1.1254 · KPD 0.5106 · KPF 1.0258 · **RUCK 1.6614**.

Cells at n ≥ 20 derive from their own outcomes; thin cells borrow at **K=10**; every pathway is then
**renormalised** so it still averages its own all-in value.

**Renormalised cell λ (vs ND), the shipped construction:**

| pathway | MID | SD | SF | KPD | KPF | RUCK | renorm k |
|---|---|---|---|---|---|---|---|
| RD | 0.5780 | 0.4688 | 0.6376 | **0.2737** | 0.4233 | **0.9240** | 0.9999 |
| SSP | 1.6206 | 0.9919 | 0.8736 | 0.5528 | 1.0085 | 1.4024 | 1.0124 |
| MSD | 1.4150 | 1.1582 | 0.8858 | 0.3642 | 0.7739 | 0.9677 | 0.9654 |
| IRE | 0.2125 | 0.2224 | 0.2862 | 0.0771 | 0.1660 | 0.2665 | 0.9841 |
| PDA | 0.4776 | 0.4274 | 0.4030 | 0.1866 | 0.3240 | 0.6359 | 0.9494 |
| PDN | 0.1597 | 0.1205 | 0.1239 | 0.1750 | 0.1283 | 0.2078 | 1.0820 |
| PDS | 0.3883 | 0.2118 | 0.3109 | 0.1874 | 0.3349 | 0.5424 | 1.2661 |
| UNR | 1.0168 | 0.2296 | 0.3076 | 0.1926 | 0.3205 | 0.3462 | 1.0225 |
| ND>64 | 0.6129 | 0.4533 | 0.5506 | 0.2317 | 0.8352 | 1.4545 | 1.0297 |

**Derived RD positional levels** — the load-bearing cells, and the inversion the directive flagged:

| pos | n | level now | λ | **DERIVED** | change |
|---|---|---|---|---|---|
| MID | 176 | 294.8 | 0.5780 | **170.4** | −42.2% |
| SD | 158 | 246.9 | 0.4688 | **115.8** | −53.1% |
| SF | 147 | 231.5 | 0.6376 | **147.6** | −36.2% |
| **KPD** | 72 | **300.3** | 0.2737 | **82.2** | **−72.6%** |
| KPF | 64 | 216.0 | 0.4233 | **91.4** | −57.7% |
| **RUCK** | 71 | 282.5 | 0.9240 | **261.0** | −7.6% |

Rookie-draft key defenders were the **most expensive** cell and the **worst-delivering** one; rucks
were near the bottom on price and top on delivery. The derivation inverts that ordering onto the
outcomes. Full per-pathway × position derived levels are in `phase1_derive_out.txt`.

---

# 4 — RECONCILIATION: **PASS, worst residual 2.14e-16 against a 1e-9 tolerance**

Entry-weighted in both layers. `Σ_c (v0_c · λ_c) = (Σ_c v0_c) · P_s`.

| pathway | rule 1 (remainder at pathway value) | rule 2 (remainder as own group) | **SHIPPED** |
|---|---|---|---|
| RD | 1.62e-16 PASS | 1.62e-16 PASS | **0.00e+00 PASS** |
| SSP | 0.00e+00 PASS | 0.00e+00 PASS | **1.48e-16 PASS** |
| MSD | **1.52e-01 FAIL** | 0.00e+00 PASS | **0.00e+00 PASS** |
| IRE | **1.36e-01 FAIL** | 2.03e-16 PASS | **0.00e+00 PASS** |
| PDA | 0.00e+00 PASS | 0.00e+00 PASS | **2.13e-16 PASS** |
| PDN | 0.00e+00 PASS | 0.00e+00 PASS | **0.00e+00 PASS** |
| **PDS** | 0.00e+00 PASS | **5.67e-01 FAIL** | **1.62e-16 PASS** |
| UNR | **7.78e-02 FAIL** | 0.00e+00 PASS | **0.00e+00 PASS** |
| ND>64 | **3.93e-02 FAIL** | 0.00e+00 PASS | **2.14e-16 PASS** |

Rule 1's failures **reproduce [RECON] exactly** (MSD 1.52e-01, IRE 1.36e-01, UNR 7.78e-02, ND>64
3.93e-02). The unsampled remainder's own profile is not the pathway average — MSD's remainder measures
0.7153 against a pathway value of 0.9418; ND>64's 0.6075 against 0.5477.

## A CONDITION THE BUILD FOUND THAT THE DIRECTIVE'S TABLE DOES NOT CONTAIN

**Rule 2 FAILS for PDS at 5.67e-01 — and it fails *because* PDS is shrunk.** [RECON] was measured
before the PDS shrinkage was ruled, so its table cannot show this. Shrinkage deliberately moves a
pathway's value away from its own measured outcomes (0.1259 → 0.2908); rule 2 alone then prices the
whole pathway at its unshrunk measured profile and the two no longer agree, by exactly the size of the
shrink.

**The renormalisation guard is what reconciles them** (`k = 1.2661` for PDS). So the guard is not only
protection against a mismatched position mix, as D4 §2 describes it — **it is also the step that makes
stream-level shrinkage compatible with the reconciliation law at all.** Without it, the two rulings
D4 issued in the same sitting — shrink PDS, and reconcile at 1e-9 — would contradict each other.

---

# 5 — THE POOL SIT-OUT RETENTION

`H_POOLSIT` (0.804) and `H_UNION` (0.280) **retire**. Derived on pool history: 3,334 complete-window
pool cells, 1,325 of them sit-outs (39.7%).

**A forced departure from "the same way the ND one is", declared not absorbed.** d13's outcome term
was `avg × REF/era[year]`. **Era normalization no longer exists** — removed by owner ruling in the
#334 stage B salvage (comment 5242713366): *"NO era normalization may be applied to scoring anywhere…
Do not reintroduce."* The national method therefore **cannot be replayed verbatim**; averages are read
raw, the current engine's own convention.

**Derived retention vs what the pool takes today (depth 1):**

| class | today `R` at pool index | × H_POOLSIT | × H_UNION | **DERIVED** | derived ÷ composed |
|---|---|---|---|---|---|
| nonKPP | 0.5490 | 0.4414 | 0.1236 | **0.5725** | **1.297×** |
| KPP | 0.6420 | 0.5162 | 0.1445 | **0.7528** | **1.459×** |
| RUCK | 0.7810 | 0.6279 | 0.1758 | **0.8783** | **1.399×** |

**The composed read is 30–46% harsher than pool history supports.** Full depth profiles, and the
alternative `v0_start` denominator, are in `phase1_retention_out.txt`. The denominator was changed
deliberately: d13 used `v0_start` for every row, which is the **national** v0 curve, and a pool entrant
is not priced off it — he is priced off `entry_anchor`. Both are reported.

## THE MEAN-PRESERVING LAW — CHECKED, AND TODAY'S COMPOSITION BREACHES IT ON EVERY PATHWAY

| pathway | sit share | mean R | **uplift U** | post-redistribution mean | **today's mean** | today's net charge |
|---|---|---|---|---|---|---|
| RD | 0.3527 | 0.5952 | 1.2206 | 1.0000000000 | 0.9193 | **−8.07%** |
| SSP | 0.3824 | 0.6883 | 1.1930 | 1.0000000000 | 0.9080 | **−9.20%** |
| MSD | 0.8500 | 0.6639 | 2.9047 | 1.0000000000 | 0.3414 | **−65.86%** |
| IRE | 0.5109 | 0.5785 | 1.4404 | 1.0000000000 | 0.6041 | **−39.59%** |
| PDA | 0.5000 | 0.5813 | 1.4187 | 1.0000000000 | 0.8802 | **−11.98%** |
| PDN | 0.8056 | 0.5796 | 2.7415 | 1.0000000000 | 0.8260 | **−17.40%** |
| PDS | 0.5806 | 0.5644 | 1.6032 | 1.0000000000 | 0.8862 | **−11.38%** |
| UNR | 0.5159 | 0.6964 | 1.3235 | 1.0000000000 | 0.7978 | **−20.22%** |
| ND>64 | 0.4376 | 0.5625 | 1.3405 | 1.0000000000 | 0.9024 | **−9.76%** |

The derived object is a **pure redistribution** — sitters carry R < 1, non-sitters carry the uplift U,
and the pathway's entry-weighted mean lands on 1.0000000000 by construction. **What ships today takes
value out of every pathway and gives it back to nobody**, which is exactly what the owner's amendment
forbids once a pathway is calibrated. MSD is the extreme at **−65.9%**, because 85% of its cells are
sit-outs and MSD sits inside the union cell.

---

# 6 — DRAFT AGE (D7): **only the rookie draft earns an adjustment**

Fitted to **playing quality only** — quality = `Σ(games×avg)/Σ(games)`, points per game, which
**cannot rise by playing more**. Primary aggregate is the **unweighted** mean across players (one
player, one vote); D7's games-weighted column is reported beside it and **flagged**, because weighting
players by games lets participation back in through the weights. It decided nothing here.

Decision rule, **pre-specified before the numbers were seen**: adjustment only if |t| ≥ 2.0 **and** the
fitted change across the stream's own age range is ≥ 2% of its mean quality.

| stream | n | slope/yr | se | **t** | % of mean | **ruling** |
|---|---|---|---|---|---|---|
| ND 1-64 | 1251 | 0.096 | 0.492 | 0.19 | 1.6% | NO ADJUSTMENT |
| **RD** | 379 | 0.904 | 0.369 | **2.45** | 25.9% | **EARNED** |
| SSP | 43 | 0.664 | 0.896 | 0.74 | 10.2% | NO ADJUSTMENT |
| MSD | 76 | 0.951 | 0.989 | 0.96 | 16.8% | NO ADJUSTMENT |
| IRE | 23 | −1.543 | 2.413 | −0.64 | 14.7% | NO ADJUSTMENT |
| PDA | 31 | 1.400 | 2.328 | 0.60 | 16.0% | NO ADJUSTMENT |
| PDN | 17 | 2.061 | 2.018 | 1.02 | 28.8% | NO ADJUSTMENT |
| PDS | 7 | 3.572 | 25.301 | 0.14 | 7.7% | NO ADJUSTMENT |
| UNR | 24 | 1.348 | 1.531 | 0.88 | 21.2% | NO ADJUSTMENT |
| ND>64 | 86 | 0.887 | 0.705 | 1.26 | 28.7% | NO ADJUSTMENT |

**One of nine pool pathways earns an age adjustment.** Eight get none — that is the finding the ruling
anticipated, not a failure. **The national draft shows no age signal on quality at all** (t = 0.19),
which is its own result.

**The ITEM B contrast, measured:** quality and participation move *differently* across age bands in
almost every stream — e.g. IRE quality 52.76/55.92/**42.65** while games run 58.6/76.5/**19.8**; PDN
quality 46.39/**65.13**/58.74 while games run 22.8/**51.5**/8.5. Any measure mixing the two prices the
mixture, which is what retired ITEM B. **Nothing above is fitted to participation.**

**An unavoidable limit, stated rather than hidden:** a player who never played has no scoring rate, so
quality is undefined for him. Every conclusion here is conditional on having played. That excludes 312
of 691 RD rows and 34 of 57 IRE rows.

---

# 7 — THE CONSEQUENCE READ

**Modelled through the engine's own measured pass-through, not built.** A board build is adoption work
and the directive's own ledger defers it. Pass-through e: **0.996** at 0 games, **0.119** at 1–9,
**0.000** at 10+.

**Board total: 745,888 → 744,350 (−0.21%).** 242 pool rows on the board; **82 reachable at all**, worth
**11,300 points = 1.51% of the board**; **79 actually move**.

**Both cohort instruments, with the margin against the 14% charge:**

| instrument | now | **DERIVED** | appreciation | charge | **margin** | verdict |
|---|---|---|---|---|---|---|
| **ALL-ARM year 1 (deciding)** | 0.8850 | **1.0371** | +3.71% | 14.00% | **+10.29%** | **legal** |
| legacy picks 1-64 year 1 | 1.0884 | **1.0884** | +8.84% | 14.00% | **+5.16%** | legal |
| ALL-ARM year 4 (context) | 1.2859 | 1.5309 | | | | |
| legacy picks 1-64 year 4 | 1.5660 | 1.5660 | | | | |

**The legacy instrument is invariant, and that is structural rather than a null result:** the picks
1-64 table contains national-draft rows only and no pool level enters any of them. It is reported as
unmoved *because it cannot move*.

**Both headline metrics** (career profile and year-4-over-year-0) are tabulated per pathway in
`phase1_consequence_out.txt`. The gap between them is the "year four flatters the pool" finding itself:
e.g. UNR reads 0.3408 on the career profile against 0.4952 at year four.

**The named lines:**

| player | stream | pos | games | e | λ | SHIP | **DERIVED** |
|---|---|---|---|---|---|---|---|
| John Noble | MSD | SD | 158 | 0.000 | 1.158 | 2162 | **2162** |
| Max Hall | MSD | SF | 44 | 0.000 | 0.886 | 2820 | **2820** |
| James Peatling | MSD | MID | 88 | 0.000 | 1.415 | 1100 | **1100** |
| Mark Keane | SSP | KPD | 63 | 0.000 | 0.553 | 1514 | **1514** |
| Tom McCarthy | MSD | SD | 30 | 0.000 | 1.158 | 1468 | **1468** |
| Lachlan McAndrew | SSP | RUCK | 22 | 0.000 | 1.402 | 1208 | **1208** |
| Zac Banch | MSD | SF | 10 | 0.000 | 0.886 | 128 | **128** |
| Flynn Perez | SSP | SD | 31 | 0.000 | 0.992 | 113 | **113** |
| Paddy Cross | SSP | SF | 10 | 0.000 | 0.874 | 113 | **113** |
| **Marcus Herbert** | MSD | SD | 8 | 0.119 | 1.158 | 1053 | **1072** |
| Mitch Podhajski | MSD | KPF | 2 | 0.119 | 0.774 | 195 | **189** |
| Harrison Coe | MSD | RUCK | 0 | 0.996 | 0.968 | 52 | **50** |

**The owner's expectation is confirmed exactly:** Noble, Hall and Peatling do not move.

**A departure from the directive's own option-C sizing, reported because it disagrees.** The directive
had Herbert at 1053 → **1042** (down). On the derived per-cell numbers he goes **1053 → 1072, UP.**
The reason is the positional lens: option C applied MSD's *pathway* multiplier 0.919 to every MSD row,
whereas Herbert is an **MSD small defender**, whose own cell λ is **1.158**. The largest movers are
similarly per-cell: Liam Hetherton (PDA KPF) −67, Xavier Walsh (RD KPD) −62, and **Logan Smith (ND>64
RUCK) +41**. Several pool rows go **up**, which no pathway-level option could produce.

## `_ruc_prior_cap` — the ordered check

`_ruc_prior_cap(p,v) = min(v, 1.4 × _cap_basis(p) × _ruc_head_v0(p))`, and `_cap_basis` for a pool row
**is its own division level**. **The cap is therefore exactly proportional to the level this act
changes** — it is not a fixed ceiling. `_v0_uncapped = raw_ev(…) × iso_eff(…)` is a production-side
object that does not read the level, so a level **cut tightens** the cap against an unchanged v0.

Mitigating structure, measured: **every pathway's RUCK cell carries the highest λ in its pathway**
(RD 0.9240, SSP 1.4024, MSD 0.9677, ND>64 1.4545), so the ruck ceiling falls *less* than its
pathway's other cells.

**What this check does not claim:** whether the cap actually *binds* on a given derived ruck v0 is a
property of the machinery's **output**, which exists only once levels are wired and the engine re-run.
That is adoption work by the order's own scope boundary.

---

# PRE-REGISTRATION BREACHES — reported plainly

Predictions are in `PREREG_ORDER17.md`, written before any measurement.

### BREACH 1 — P1.b/P1.c: **MSD was misclassified as a pickless mechanism.**
Predicted the pickless pathways would be "largely OUT" and named MSD among them. **MSD carries a
stored pick (1–20) and is therefore IN `R`'s derivation population at 83%.** The RD/ND>64 half of the
prediction held (99.1%, 100%); the pickless half held for the six genuinely pickless pathways (0%).
The error was treating "pickless mechanism" as a class label rather than checking the field.

### BREACH 2 — P1.d: **the stated blocker was the wrong blocker.**
Predicted the [1,90] clamp and the 1-99 rookie ladder would be the obstacle. **Measured: zero rows in
the entire store carry a stored pick above 90; the RD ladder tops out at 51.** The clamp is inert. The
directive inherited this concern and the build inherited it from the directive; neither checked it.

### BREACH 3 — two wrong fields in the first population replay, caught before publication.
The first draft read the matrix's `pick` (the *effective* pick, constant 65 for all pool) and `debut`
(actual first game, null for the 708 never-played rows). Either would have inverted the verdict — the
second would have excluded the entire sit-out subset, which is the population the surface is derived
on. Corrected to `pick_stored` and to `year` via `cp.debutyr`. **Recorded because the corrected script
is the only one visible in the evidence, and the error is not.**

### BREACH 4 — P4.a: **rule 2 does not pass on every pathway.**
Predicted all pathways reconcile under rule 2. **PDS fails at 5.67e-01 under rule 2** because the PDS
shrinkage moves the pathway value off its own measured profile. The *shipped* construction passes at
1.62e-16, so the deliverable is unaffected — but the prediction as written was wrong, and the
interaction between the shrinkage ruling and the reconciliation ruling is a real finding.

### BREACH 5 — P5.b: **the retention range was too narrow at the top.**
Predicted 0.30–0.65 at depth 1. Measured nonKPP **0.5725** (in range), **KPP 0.7528** and **RUCK
0.8783** (both above). The *direction* was right — the composed read is harsher than pool history
supports — but the range understated how much harsher for KPP and RUCK.

### BREACH 6 — P7.d: **Herbert moves in the opposite direction to the prediction's basis.**
Predicted Herbert, Podhajski and Coe move — correct. But the directive's option C had Herbert falling
to 1042 and he **rises to 1072** on the derived per-cell numbers. The prediction did not anticipate
that the positional lens would reverse a named line's sign.

### NOT BREACHED
P2.a (layer 1 reproduces [PROFILE] — every pathway matches to 4 dp), P2.b (PDS → 0.291; measured
0.2908), P2.c (ND target 1.0252), P3.a (RD cells reproduce D3B), P3.b (no pick axis), P3.c
(renormalisation exact), P3.d (whole-pool shape rank order matches RD — RUCK best, KPD worst), P4.b
(rule 1 reproduces [RECON] exactly), P5.a, P5.c (redistribution, mean 1.0000000000), P6.a, P6.b
(RD shows signal), P6.c (1 of 9 ≤ 2), P7.a (−0.21%, predicted ≈ −0.25% and < 1%), P7.b (1.0371,
margin +10.29%, predicted ≈1.03 and +10 to +12), P7.c.

P8.a is **not resolved either way** — see the `_ruc_prior_cap` section. The prediction that the cap
"does bind" could not be tested without the machinery's outputs, which Phase 1 does not produce.

---

# WHAT COULD NOT BE DETERMINED

1. **Row-level membership of `R`'s derivation population at engine `af1fc6aa`.** The artefact
   (`d13_normcells.json`) is absent and the store has moved. The pathway-level verdict is structural
   and robust; exact counts are not recoverable.
2. **`_double_count` exclusions** — the flag is not on the matrix and is not reconstructible.
3. **Depth-cell counts** for the population replay (`listed_through` unavailable).
4. **Whether `_ruc_prior_cap` binds** on any derived ruck v0 — requires the machinery's outputs, i.e.
   wiring, which is out of Phase 1's scope.
5. **The iterate-to-tolerance step.** The order requires derived numbers be treated as calibration
   targets that the machinery is iterated onto. That iteration requires wiring the levels and
   re-running the engine, which Phase 1 is explicitly forbidden from doing. **The levels here are the
   targets; the iteration is adoption work.**
6. **Whether the modelled consequence matches a real build.** The figures use the measured carry
   curve, exact only where the carry is 0.000 or 0.996 and an estimate at 0.119.
7. **Whether MSD rucks behave like RD rucks** — the whole-pool shape is RD-dominated and this cannot
   be tested at n=14. A declared limit of the borrow, carried from D4.

---

# STATUS

**Phase 1 is complete. Nothing is wired. The shipped board has not moved. No engine configuration was
altered.** The engine was loaded read-only from a staged copy in scratch so the repo was never touched.

**Adoption is a separate act on the owner's word.**
