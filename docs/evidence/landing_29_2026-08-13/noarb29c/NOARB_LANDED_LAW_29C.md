# NO-ARBITRAGE ON THE LANDED-LAW BASIS — ORDER 29C, THE RE-BASED READING

**Board `36d5dfc73e2b508ece530bc7dfae2090` — UNMOVED. Nothing merges. PR #510 stays HELD.**
Brief #334 comment 5289123976. Preregistration `PREREG_29C.md`, filed before the emitter existed and
never edited. Machine-readable twin: `NOARB_LANDED_LAW_29C.json` (assembled from the instrument
outputs, never re-typed).

---

> ## READ THIS FIRST
>
> **The published review pack was mixed-basis, and on a coherent ruler the deciding instrument opens
> an arbitrage it did not previously show.**
>
> ORDER 29B measured that `emit_matrix_338.py:252` writes the cohort matrix's year-0 from the **frozen
> fitted surface** while years 1…7 are the landed `ev()`. So every margin in §13–§14 divides a
> landed-law numerator by a pre-landing denominator. **ORDER 29C changes that one column to the landed
> entry law and nothing else** — years 1–7 are byte-identical, proven by diff.
>
> | reading | HISTORICAL-PRINT (the record) | **LANDED-LAW (the merge criterion)** | |
> |---|---:|---:|---|
> | all-arm PRIMARY, margin v14% | +20.75% no arb | **−19.10%** | **ARB — NEW** |
> | all-arm MODERN, margin v14% | +18.11% no arb | **−12.48%** | **ARB — NEW** |
> | legacy ND ALL 1–64 | −18.01% ARB | **−16.74%** | ARB (slightly better) |
> | legacy ND 1–20 | −20.93% ARB | **−17.12%** | ARB (slightly better) |
> | legacy ND 21–64 | −13.56% ARB | **−16.12%** | ARB (slightly worse) |
>
> **Arbitrages: 3 of 5 → 5 of 5.** The ND arbitrage **persists** and barely moves; the all-arm
> instrument **flips in both windows**. Every one of these numbers was **tabled in `PREREG_29C.md`
> before the emitter ran, and every one printed exactly as filed.**
>
> **The cause is not the numerator.** The numerator is byte-identical across the two bases — the
> legacy ND `mean_yrN` columns are literally the same numbers (981.53 / 1093.71 / 1195.56 / 1245.19).
> The cause is that **the pool arms' year-0 denominators were wrong by 2–8×**, and the landed law is
> what the board actually prices those entrants at.

---

## 1. THE TWO BASES, NAMED

| | **HISTORICAL-PRINT basis** | **LANDED-LAW basis** |
|---|---|---|
| what it is | the record — what ORDER 29 §13 and ORDER 29B §14 read | the merge criterion — what the landed board actually prices day 0 at |
| year 0 | `emit_matrix_338.py:252` → `round(v0_start(p), 1)`, the **frozen fitted surface** | the **ORDER 29B entry law**: ND in-curve `nd_v0.posv[gfut][pick]`; pool `pool_v0_of(p)` cell; `× _PL_F` |
| years 1–7 | `ev(p, Y)` walk-forward under the 29B engine | **identical, byte for byte** |
| coherent? | **NO** — landed-law numerator over a pre-landing denominator | **YES** — both sides of the ratio are the same object |
| matrix | `per_entrant_O29B.json` `ca24a49a` | `per_entrant_O29CFINAL.json` **`6db06e40`** |

A third column, **LIVE**, appears in the tables as a pipeline control only (the pinned matrix behind
live board `88ce647f`, read on the pre-re-point instrument copies).

## 2. THE LAW, AND THE PROOF THAT THIS IS IT

Quoted from `_merged_recover.py` (ORDER 29B block, commit `13cbebb`), not paraphrased:

```
day0_v0(p):  p['_pool']                    -> MA.pool_v0_of(p)             # cell '<pathway>|<gfut>'
             type ND and 1 <= pick <= 64   -> nd_v0.posv[MA.gfut(p)][pick]
ev(day-0 entrant, Y) = day0_v0(p) * _PL_F                                  # BOARD -> ENGINE currency
printed              = int(round(ev / _F)),  _F == _PL_F == 1.0524
```

The numéraire `s` is **already inside** both published objects (`posv` is built on the shipped ladder
`raw × s`; the pool cells carry `× anchor_factor == s == 0.9400914291048137`), so `_PL_F` is the only
conversion and it is applied exactly once. The two owner-Option-A borrowed cells (`PDN|KPF`
92.35874340265629, `PDS|KPF` 83.97715038537063) are consumed through `MA.pool_v0_of` — the one
accessor — exactly as the board consumes them.

| the proof | result |
|---|---|
| **replication against the board's own printed day-0**, 89 wired entrants, board `36d5dfc7` | **89 of 89 EXACT, tolerance 0** — on the printed integer **and** the unrounded `derived_v0` (`\|err\| == 0.0`). Fail-closed **inside the emitter**: it halts rather than emit on anything less |
| **unmappable entrants** | **0 of 2648.** The law's position key `MA.gfut(p)` reads `_futpos` / `_pos_now` / `pos` — **all store columns, none scoring-derived** — so it is invariant under the walk-forward's scoring truncation. Census: **`_futpos` supplies the key on 2648 of 2648**, so the `layer1`/LEDGER day-0-position fallback the brief authorised is **never reached** |
| **matrix identity** (`o29c_matrixdiff.py`) | **every field except `v0` byte-identical on all 2648 records**; schema identical; record order identical; store `cb38ef11`, v0surf `4405cba2b42f`, `n_records` 2648 all unmoved. Only `meta.emitter` and the new `meta.basis_29c` differ |
| **the year-0 column** | **2648 of 2648 cells move** (ORDER 29B moved **0 of 2648**). 887 rise, 1761 fall. Σ`v0` **1,904,793.4 → 1,369,559.9**, ×**0.7190** |
| **the emitter** | `emit_matrix_29c.py` = `emit_matrix_338.py` (`bffde2f7…`) copied, **one value site changed**; the standing emitter's md5 is asserted *inside the copy at run*. Full diff: `EMITTER_29C.diff` |
| **1-dp round-trip**, disclosed not repaired | **87 of 89.** `hunter-holmes` (661 vs 660) and `cooper-bell` (409 vs 408) land one point low purely from the emitter's carried `round(·,1)` convention. **The column was not un-rounded to make this 89** — that would be a second, undeclared change |

## 3. THE DENOMINATOR SHIFT, PER ARM — WHY EVERYTHING ELSE MOVES

Mean year-0 in engine currency, over the standing emitter's own population (2648 records).
**This table is the whole finding.**

| arm | n | HISTORICAL-PRINT | **LANDED-LAW** | old ÷ new |
|---|---:|---:|---:|---:|
| ND 1–64 | 1446 | 746.61 | **755.93** | **0.988** — year-0 *rises* |
| RD | 691 | 761.45 | **245.39** | **3.10×** |
| ND>64 | 122 | 832.54 | **264.24** | 3.15× |
| MSD | 106 | 497.16 | **351.74** | 1.41× |
| UNR | 59 | 281.76 | **115.24** | 2.45× |
| IRE | 57 | 597.26 | **86.41** | **6.91×** |
| SSP | 52 | 424.26 | **197.82** | 2.15× |
| PDA | 51 | 626.13 | **193.93** | 3.23× |
| PDN | 43 | 601.34 | **86.19** | **6.98×** |
| PDS | 21 | 678.42 | **85.28** | **7.96×** |

**The owner's diagnosis is confirmed to the digit.** In the all-arm PRIMARY window the instrument's
own per-arm figure reads **RD mean year-0 `772.2`** on the historical-print basis — the "~772" the
brief named — against rederived RD cells of 206–369. On the landed law it reads **`245.8`**, inside
that band. The old column really was reconstructing the pre-landing entry class.

**The brief's "~2–3×" expectation is right for four arms and materially wrong for three** — `IRE`,
`PDN` and `PDS` fall by **~7–8×**, `MSD` by only 1.41×. The measured numbers were filed in
`PREREG_29C.md` §P29C-5 in advance of the emit, not fitted afterwards.

### 3.1 Five rows price to exactly zero — a declared artifact, and a population change

The artifact's own `nd_v0.ruck_floor_63_64` (`posv_63 = posv_64 = 0.0`; ORDER 28 §9.4 — the
per-position local-linear fit goes negative in the thinnest tail and is **floored**, not silently
clipped) puts five RUCK rows at year-0 **0.0**: `matthew-dick` (63), `matthew-arnot` (63),
`tom-derickx` (63), `tom-downie` (64), `luke-davis` (64). Measured consequences, predicted in advance:

* `noarb_table_allarm.py` excludes `v0 <= 0` → eligible **2647 → 2643**, **PRIMARY n 2215 → 2211**,
  **MODERN n 540 (unchanged)**.
* `noarb_table_338.py` does **not** exclude them; they stay in the denominator at 0, so the legacy ND
  population stays **1200** and the `EXPECT_N` pin holds.

---

## 4. THE READINGS

Every table below is labelled with its **instrument**, **population**, **window** and **basis**.
Instrument copies are ORDER 29's disclosed pair under `noarb/`, **unmodified from their §13 state** —
`noarb_table_338.py` md5 **`0f8220351c64c56ccfa90c60edcdfa5f`**, computed at run.

### 4.1 ALL-ARM DECIDING INSTRUMENT — `noarb_table_allarm.py`
**Population: ND + every pool pathway, one cohort. Aggregation: pooled book ratio,
mean(value at cohort year N) / mean(v0) over the same set.**

| window | basis | n | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| PRIMARY 2005–2023 | LIVE *(control)* | 2212 | 1.0000 | 0.8077 | 0.9737 | 1.0703 | 1.1291 | 1.1096 | 1.0560 | 0.9260 | −19.23% | **+33.23%** | no arb |
| PRIMARY 2005–2023 | HISTORICAL-PRINT | 2215 | 1.0000 | 0.9325 | 1.0381 | 1.0742 | 1.1228 | 1.1006 | 1.0451 | 0.9152 | −6.75% | **+20.75%** | no arb |
| **PRIMARY 2005–2023** | **LANDED-LAW** | **2211** | 1.0000 | **1.3310** | 1.4810 | 1.5318 | 1.6013 | 1.5795 | 1.5108 | 1.3273 | **+33.10%** | **−19.10%** | **ARB** |
| MODERN 2019–2023 | LIVE *(control)* | 540 | 1.0000 | 0.8225 | 0.9256 | 0.9794 | 0.9772 | 1.0345 | 0.9099 | 0.8009 | −17.75% | **+31.75%** | no arb |
| MODERN 2019–2023 | HISTORICAL-PRINT | 540 | 1.0000 | 0.9589 | 0.9986 | 0.9923 | 0.9768 | 1.0289 | 0.9017 | 0.7926 | −4.11% | **+18.11%** | no arb |
| **MODERN 2019–2023** | **LANDED-LAW** | **540** | 1.0000 | **1.2648** | 1.3240 | 1.3156 | 1.2951 | 1.3782 | 1.2321 | 1.0841 | **+26.48%** | **−12.48%** | **ARB** |

### 4.2 LEGACY RETAINED INSTRUMENT — `noarb_table_338.py`, UNMODIFIED
**Population: the legacy ND teaching set (`EXPECT_N` 1200, asserted at run). Draft clock, not cohort clock.**

| group | basis | n | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | yr6 | yr7 | apprec 0→1 | margin v14% | verdict |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| ALL picks 1–64 | LIVE *(control)* | 1197 | 1.0000 | 1.0730 | 1.3343 | 1.4952 | 1.5712 | 1.5529 | 1.4981 | 1.3005 | +7.30% | **+6.70%** | no arb |
| ALL picks 1–64 | HISTORICAL-PRINT | 1200 | 1.0000 | 1.3201 | 1.4710 | 1.6080 | 1.6747 | 1.6530 | 1.5937 | 1.3829 | +32.01% | **−18.01%** | **ARB** |
| **ALL picks 1–64** | **LANDED-LAW** | **1200** | 1.0000 | **1.3074** | 1.4568 | 1.5925 | 1.6586 | 1.6350 | 1.5753 | 1.3640 | **+30.74%** | **−16.74%** | **ARB** |
| picks 1–20 | LIVE *(control)* | 377 | 1.0000 | 1.1218 | 1.3642 | 1.4886 | 1.5981 | 1.5685 | 1.4750 | 1.2931 | +12.18% | **+1.82%** | no arb |
| picks 1–20 | HISTORICAL-PRINT | 380 | 1.0000 | 1.3493 | 1.4649 | 1.5883 | 1.7076 | 1.6736 | 1.5741 | 1.3782 | +34.93% | **−20.93%** | **ARB** |
| **picks 1–20** | **LANDED-LAW** | **380** | 1.0000 | **1.3112** | 1.4235 | 1.5434 | 1.6594 | 1.6232 | 1.5268 | 1.3323 | **+31.12%** | **−17.12%** | **ARB** |
| picks 21–64 | LIVE *(control)* | 820 | 1.0000 | 0.9996 | 1.2894 | 1.5051 | 1.5307 | 1.5299 | 1.5322 | 1.3113 | −0.04% | **+14.04%** | no arb |
| picks 21–64 | HISTORICAL-PRINT | 820 | 1.0000 | 1.2756 | 1.4803 | 1.6380 | 1.6246 | 1.6220 | 1.6230 | 1.3899 | +27.56% | **−13.56%** | **ARB** |
| **picks 21–64** | **LANDED-LAW** | **820** | 1.0000 | **1.3012** | 1.5100 | 1.6709 | 1.6572 | 1.6536 | 1.6517 | 1.4141 | **+30.12%** | **−16.12%** | **ARB** |

**The numerators are byte-identical between the two landed bases** — `mean_yrN` for ALL picks 1–64
reads **981.53 / 1093.71 / 1195.56 / 1245.19** on *both*. The only thing that moved is `mean_yr0`:
**743.52 → 750.76** (ALL), **1417.71 → 1458.90** (1–20), **431.09 → 422.60** (21–64). That is why
1–20 improves while 21–64 gets worse: the positional object lifts the top of the ladder and cuts the
tail, and the two halves move in opposite directions.

### 4.3 BY ARM — `noarb_table_allarm.py`, PRIMARY 2005–2023
**Pooled ratio within the arm, same construction. `mean_v0` is the arm's own year-0 denominator.**

| arm | n | yr1 HIST | **yr1 LANDED** | yr4 HIST | **yr4 LANDED** | mean_v0 HIST | **mean_v0 LANDED** |
|---|---:|---:|---:|---:|---:|---:|---:|
| ND | 1313→1309 | 1.2308 | **1.3068** | 1.5539 | **1.6484** | 752.6 | **711.1** |
| RD | 623 | 0.4602 | **1.4461** | 0.4585 | **1.4407** | **772.2** | **245.8** |
| MSD | 55 | n/a\* | n/a\* | 0.6039 | **0.8567** | n/a\* | n/a\* |
| UNR | 49 | 0.4363 | **1.0490** | 0.5612 | **1.3492** | 278.7 | **115.9** |
| IRE | 47 | 0.2230 | **1.5547** | 0.2008 | **1.3997** | 602.7 | **86.4** |
| PDA | 43 | 0.4120 | **1.2628** | 0.4738 | **1.4523** | 636.8 | **207.8** |
| PDN | 33 | 0.1484 | **1.0361** | 0.1685 | **1.1764** | 613.7 | **87.9** |
| SSP | 31 | 0.9474 | **2.4081** | 0.7390 | **1.8783** | 531.3 | **209.0** |
| PDS | 21 | 0.1721 | **1.3689** | 0.1233 | **0.9806** | 678.4 | **85.3** |

\* the disclosed MSD debut-year gap: the emitter builds `yrs` from draft year + 1, so an MSD entrant's
cohort year 1 is not carried. Those rows are **excluded from that year, never scored zero** — carried
convention, not an ORDER 29C choice.

### 4.4 BY ARM — MODERN 2019–2023

| arm | n | yr1 HIST | **yr1 LANDED** | yr4 HIST | **yr4 LANDED** | mean_v0 HIST | **mean_v0 LANDED** |
|---|---:|---:|---:|---:|---:|---:|---:|
| ND | 325 | 1.2119 | **1.2386** | 1.3037 | **1.3324** | 763.6 | **747.1** |
| RD | 66 | 0.3650 | **1.3157** | 0.3570 | **1.2869** | 876.9 | **243.3** |
| MSD | 55 | n/a\* | n/a\* | 0.6039 | **0.8567** | n/a\* | n/a\* |
| SSP | 31 | 0.9474 | **2.4081** | 0.7390 | **1.8783** | 531.3 | **209.0** |
| PDN | 25 | 0.1371 | **1.0339** | 0.0865 | **0.6523** | 654.9 | **86.8** |
| UNR | 13 | 0.4865 | **1.3188** | 0.2600 | **0.7046** | 313.7 | **115.7** |
| PDA | 13 | 0.3318 | **0.9344** | 0.4141 | **1.1664** | 783.6 | **278.2** |
| IRE | 12 | 0.1246 | **1.0000** | 0.0244 | **0.1959** | 645.2 | **80.4** |

### 4.5 THE `IRE` MODERN CELL — THE THESIS IN ONE NUMBER

On the landed-law basis `IRE` MODERN yr1 reads **exactly `1.0000000000`**, and it was predicted at
exactly that in `PREREG_29C.md` §P29C-9 before the emitter ran. All twelve rows played no games in
their cohort year 1, so under the 29B wiring their year-1 `ev()` **is a day-0 print** — the very
number the landed law gives as their year-0. **On a coherent ruler, the yr0→yr1 step for a
zero-evidence entrant is exactly flat.** The `0.1246` the mixed-basis pack reported for the same
twelve rows — an apparent 8× cliff — was an artefact of dividing a landed-law numerator by a
pre-landing denominator. Nothing about those players changed between the two readings.

---

## 5. WHAT THE OWNER'S MERGE DECISION NOW RESTS ON

1. **The pool yr0→yr1 "cliffs" were largely a measurement artefact.** Every pool arm's yr1 ratio rises
   and **seven of nine cross 1.0** in the PRIMARY window (`RD`, `UNR`, `IRE`, `PDA`, `PDN`, `SSP`,
   `PDS`; `ND` was already above; only `MSD` — which has no yr1 cell — does not). §13's and §14's pool
   cliffs are, to that extent, **cured by fixing the ruler rather than by touching the legs**.
2. **The ND arbitrage is real and survives the re-basis.** ND was already ≈ the new basis, so its
   readings move only modestly (**−18.01% → −16.74%** all-in) and **all three groups stay ARB**. This
   is the finding §13.2 and §14.6 reported, and **it is not an artefact of the mixed basis**.
3. **The deciding instrument flips.** All-arm PRIMARY **+20.75% → −19.10%** and MODERN
   **+18.11% → −12.48%**. On the coherent ruler the board's day-0 entry prices are **low enough
   against the un-rewired year-1+ legs that the whole cohort book carries an arbitrage against the 14%
   charge**, in both windows. Arbitrages **3 of 5 → 5 of 5**.
4. **The mechanism is the same one ORDER 29B named, seen without the distortion.** §B3 concluded "the
   gap P12 sized has been closed at day 0 and TRANSFERRED to the yr0→yr1 step". ORDER 29C measures
   that transfer on a ruler that can actually see it: the year-1+ marks are still produced by the
   **un-rewired legs**, and pricing day 0 correctly while leaving year 1+ alone puts the whole
   discontinuity in one step.
5. **§14.7's owed decision is unchanged and is now better posed.** The as-of vs career-total predicate
   still needs an owner word. ORDER 29C does not touch it and does not prefer either; it only removes
   the reason the question looked like a measurement problem.

**None of this changes a byte of the board, the store, the curve or the engine.** It changes the
ruler the review pack is read with, and the ruler now says something different about the deciding
instrument than the pack does.

---

## 6. CONTROLS AND EXIT ASSERTS

| control | status |
|---|---|
| **LIVE-basis control** (pre-re-point copies, `per_entrant_O25R4.json`) | **PASS** — reproduces `NOARB_MARGINS_V2` to the last digit: +33.23% / +31.75% / +6.70% / +1.82% / +14.04%, **0 arbitrages** |
| **HISTORICAL-PRINT control** (`per_entrant_O29B.json` `ca24a49a`, re-run in this session on the same copies) | **PASS — reproduces `NOARB_MARGINS_29.md` §B2 to the digit**: −6.75% / +20.75%, −4.11% / +18.11%, +32.01% / −18.01%, +34.93% / −20.93%, +27.56% / −13.56%. **3 ARB** |
| replication of the landed law vs the board's printed day-0 | **PASS — 89 of 89, tolerance 0**, fail-closed inside the emitter |
| unmappable entrants | **0 of 2648**, `_futpos` census 2648/2648 |
| matrix identity: only `v0` differs | **PASS** — every other field byte-identical on 2648 records |
| identity pins (`EXPECT_STORE cb38ef11` · `EXPECT_V0SURF 4405cba2b42f` · `EXPECT_N 1200`) | **ALL HOLD — no instrument re-pointed by ORDER 29C** |
| `noarb_table_338.py` byte-identical | **PASS — `0f8220351c64c56ccfa90c60edcdfa5f`** on all three copies, computed at run |
| standing emitter `emit_matrix_338.py` unmodified | **PASS — `bffde2f786be85037483e9f5f1563068`**, asserted inside the 29C copy at run |
| board / store / artifact / engine unmoved | **PASS** — `36d5dfc7` · `cb38ef11` · `911774bc` · `rl_model.py 14000af2` · `_merged_recover.py a353a9d3` · `v0surf.pkl 5dd34ca8` |
| tree scope | **PASS** — diffs confined to `docs/evidence/landing_29_2026-08-13/noarb29c/` plus one packet append |
| 1-dp round-trip | **87 of 89 — DISCLOSED, not repaired** |

## 7. PROVENANCE

| file | what |
|---|---|
| `PREREG_29C.md` | the fifteen predictions, filed before the emitter existed, never edited |
| `o29c_lawprobe.py` · `LAWPROBE_29C.{json,_out.txt}` · `LANDED_V0_29C.json` | the law replicated standalone and proven 89/89; the landed-law year-0 column |
| `o29c_predict.py` · `PREDICT_29C.{json,_out.txt}` | the predicted readings, computed from committed inputs before any instrument ran |
| `emit_matrix_29c.py` · `EMITTER_29C.diff` | the disclosed emitter copy — one declared change, fail-closed replication inside it |
| `emit_variant_o29c.sh` · `EMIT_O29CFINAL_out.txt` | the emit on a detached worktree of HEAD; matrix **`6db06e40`** |
| `o29c_matrixdiff.py` · `MATRIXDIFF_29C.{json,_out.txt}` | **the identity assert: only `v0` differs, on all 2648 records** |
| `o29c_delta.py` · `V0DELTA_29C.json` · `o29c_roundtrip.py` · `ROUNDTRIP_29C.json` | the year-0 movement and the disclosed 1-dp round-trip |
| `run_noarb_o29c.sh` · `NOARB_MARGINS_29C_out.txt` · `MARGINS_O29C.{txt,json}` | both instruments, three bases, and the canonical margins reporter |
| `t338_O29CFINAL.txt` · `allarm_O29CFINAL.{txt,json}` · `table_O29CFINAL.json` | the raw landed-law readings |
| `t338_O29BFINAL_control.txt` · `allarm_O29BFINAL_control.txt` | the historical-print control, re-run in this session |
| `NOARB_LANDED_LAW_29C.json` | this document's machine-readable twin, assembled from the instrument outputs |
