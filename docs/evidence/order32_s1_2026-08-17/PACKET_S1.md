# PACKET S1 — AGE-REFERENCED BARS FOR THE STALL GATE (ORDER 32, SEAT S1)

**MEASUREMENT ONLY. NOTHING IS WIRED.** No engine file, no board, no law was touched by this seat.
Every number below was computed AFTER `PREREG_S1.md` was pushed (commit `0692ae6`, rebased onto the
branch as its own commit before any script ran); the predictions and falsifiers there were written
first and are scored in §11.

Read in this order: this packet → `CENSUS_S1.txt` (the season counts and the flag decomposition) →
`MEASURE_S1_out.txt` (every distribution and every construction cell, machine-emitted) →
`APPLY_S1_out.txt` (the named ten, season by season) → `SEASON_TABLE.json` /
`CONSTRUCTIONS_S1.json` (machine-readable). Scripts: `s1_build.py`, `s1_measure.py`, `s1_apply.py`
— each re-runs from the store alone.

---

## 1. WHAT WAS ASKED AND WHAT THE ANSWER IS

The stall gate (`engine/rl_after/_merged_recover.py::o31_stall_run`, ~line 3319) counts a played
season as a **stall season** when

```
games < 10 x season-fraction        (the GAMES leg)
   OR season avg < the position bar (the AVG leg; _O30BP_BARS: KPD 65.4, KPF 63.8, MID 77.1,
                                     RUCK 75.5, SD 75.3, SF 67.9 — the Ruling-1 replacement bars)
```

Those bars are the owner's ruled **mature** replacement levels, and the gate applies them
**age-blind**. The question: should the gate's AVG leg be age-referenced, judged by whether the bar
separates seasons that presage delivered careers from seasons that presage washouts?

**The answer in four sentences.**

1. The flat bar reads a normal young season as a stall: **86% of age-18–19 full seasons whose
   players went on to delivered careers are flagged**, against 18% at age 24+ — the same bar is
   ~5x harsher on the young players who turn out fine (§5).
2. An age-referenced bar fixes most of that at small cost: the recommended construction (**C3**,
   the development-curve offset, §7) cuts the young false-flag rate 72% → 23% while the washouts it
   newly passes still carry near-zero subsequent delivered value (median 51 vs 1,330 v0-surplus
   points for the seasons it passes, §8).
3. But the bar is only **half the gate**: 64% of currently-flagged young rows are flagged on the
   GAMES leg, which no bar construction touches — the constituency flag rate moves 94% → 84%, not
   to zero, and named rows busslinger and madden stay flagged on games while averaging **above the
   flat mature bar** (§9–10).
4. harry-dean's age-19 KPD season (59.7) reads DELIVERED under every age-referenced construction;
   milan-murdock and every other mature row is untouched by construction (the cap law, §7).

## 2. EVERY TERM, DEFINED ONCE

| term | definition |
|---|---|
| **store** | `engine/rl_after/rl_model_data.json` at `cb38ef11` — 2,650 players, per-season `{year, games, avg, pos}`, 2005–2026. |
| **season row** | one player-season with games > 0. 11,340 of them. Gameless seasons never enter (the gate skips them; they are the unplayed-clock D(c_u) channel). |
| **AGE** | season year − birth year (`_by`, present on all 2,650). The owner's own convention: it reads harry-dean's 2026 as his age-19 season. Exact birthdates exist on only 1,150 rows, so the year-difference is used uniformly; the ~half-year within-cohort spread is disclosed, not corrected. |
| **POS** | the player's `future_position` — exactly the gate's own bar key (`gfut`). Sensitivity by season-label in §4. |
| **FULL season** | a season the AVG leg can bind on: games ≥ 10 (completed years), ≥ 10 × 0.92 = 9.2 for in-progress 2026 (calendar_progress from `data/season_state.json`). This is the gate's own games test. |
| **flat bar** | `_O30BP_BARS[POS]` above (Ruling 1). |
| **DELIVERED season** | FULL season with avg ≥ flat bar — the gate's own delivery test, unchanged. |
| **DELIVERED-LATER** (outcome 1) | for a season in year Y: some season y > Y is DELIVERED. The flat mature bar deliberately stays the OUTCOME criterion — the question under test is only how the gate reads YOUNG seasons, not whether the ruled mature level is right. |
| **washout** (per season) | DELIVERED-LATER = false. |
| **SDV** (outcome 2) | subsequent delivered value = Σ over later seasons of games × max(0, avg − flat bar). v0-language surplus points, the delivered-value lane's language. 2026 games counted raw (not grossed up by 1/0.92) — small disclosed conservatism. |
| **fitted window** | season years 2005–2021, so every fitted season has ≥ 5 subsequent observable seasons. 2026 never enters a fitted cell. Sensitivity to ≤ 2022 in §6. |
| **#338 basis** | minimum-listing-tenure rule (`docs/evidence/noarb_338_2026-08-06/README.md`, commit `30996f8`): a drafted player is listed ≥ 4/3/2 seasons by pick band whether or not the DB kept numbers. Adopted consequence: listed years without scoring are zero-delivery years, and a finished career is a FINAL outcome, not censoring. With ≥ 5 observed years behind every fitted season, no fitted cell's population changes under this rule; it fixes only the READING of never-delivered careers. Disclosure: 58 fitted-window players are counted washout-side while still active in 2025–26 without a later delivered season. |
| **FF** (false-flag rate) | P(under-bar \| season's player DELIVERED-LATER) — eventual deliverers flagged. |
| **MISS** | P(over-bar \| washout) — true stallers passed. |
| **RR** | relative risk of washout given under-bar vs over-bar. 1.0 = the bar separates nothing. |
| **THIN** | cell n < 15. Printed, never silently smoothed; every fallback named in `MEASURE_S1_out.txt`. |
| **cap law** | design constraint fixed in the prereg: every construction's bar(age, POS) ≤ flat bar, and ages 24+ take the flat bar exactly. No currently-passing season can become flagged — the murdock guard is structural, and §9 verifies it empirically anyway (0 mature rows change). |

## 3. THE STRUCTURAL FACT FIRST: THE BAR IS ONLY HALF THE GATE

The AVG leg only binds on a season that already passes the GAMES leg. On the 2026 board's
established constituency (played in 2026, 1–50 career games; n = 263 — and this census reproduces
the established 94% figure exactly: 246/263 flagged):

| 2026 season reading | n | share of flagged |
|---|---:|---:|
| games-leg fail only | 13 | 5% |
| both legs fail | 145 | 59% |
| **avg-leg fail only (bar-relievable)** | **88** | **36%** |
| pass | 17 | — |

**64% of young flags have the games leg in them, and no bar re-reference can touch those this
season.** (Prereg P7 predicted > half; falsifier F4 — avg-only share < 20% would have demoted this
whole exercise — is NOT triggered at 36%.) A bar change can also shorten a standing run by making a
PRIOR full season read delivered (tauru, kako in §10), so its reach is a little wider than the 88
rows, but the games leg is the binding constraint for most of the constituency. §10 names what this
means for the owner.

## 4. WHAT YOUNG SEASONS ACTUALLY LOOK LIKE (distributions)

Full-season scoring averages by age × position, completed seasons 2005–2025, games ≥ 10.
**under-bar% = the share of that cell the gate's AVG leg flags today.** Full quantile table
(p10/p25/p50/p75/p90 per cell) in `MEASURE_S1_out.txt` §A; the spine:

| pos | age→ | 18 | 19 | 20 | 21 | 22 | 23 | 24–28 (mature) |
|---|---|---|---|---|---|---|---|---|
| KPD (bar 65.4) | mean | 37.1 (n1, THIN) | 54.0 (n18) | 58.5 (n42) | 60.1 (n55) | 63.7 (n77) | 64.0 (n89) | 68.9 (n379) |
| | under-bar% | 100% | 89% | 74% | 69% | 58% | 60% | **40%** |
| KPF (63.8) | mean | 55.8 (n3, THIN) | 51.1 (n25) | 56.3 (n55) | 62.0 (n67) | 65.2 (n76) | 65.8 (n72) | 71.7 (n250) |
| | under-bar% | 100% | 92% | 78% | 61% | 53% | 49% | **31%** |
| RUCK (75.5) | mean | — (n0) | 59.4 (n4, THIN) | 56.4 (n9, THIN) | 67.8 (n15) | 71.1 (n33) | 77.6 (n34) | 84.8 (n191) |
| | under-bar% | — | 100% | 89% | 60% | 64% | 50% | **35%** |
| MID (77.1) | mean | 64.3 (n7, THIN) | 62.8 (n139) | 69.6 (n208) | 74.1 (n227) | 79.9 (n238) | 83.5 (n217) | 87.8 (n801) |
| | under-bar% | 86% | 86% | 70% | 58% | 46% | 37% | **28%** |
| SD (75.3) | mean | 61.2 (n4, THIN) | 56.5 (n54) | 62.0 (n109) | 64.6 (n155) | 68.1 (n180) | 71.6 (n165) | 76.2 (n672) |
| | under-bar% | 100% | 91% | 85% | 75% | 72% | 61% | **50%** |
| SF (67.9) | mean | 52.3 (n3, THIN) | 55.3 (n84) | 59.9 (n113) | 62.8 (n145) | 66.6 (n149) | 67.0 (n170) | 71.1 (n538) |
| | under-bar% | 100% | 87% | 68% | 63% | 52% | 54% | **43%** |

The picture is the same everywhere: the flat bar sits between the 28th (MID) and 50th (SD)
percentile of MATURE seasons, but flags 86–100% of age-18–19 seasons. The development gap
(mature mean − age mean) pooled by class:

| class | 18 | 19 | 20 | 21 | 22 | 23 | mature mean (24–28) | mature sd |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| TALL (KPD/KPF/RUCK) | 22.3 (n4, THIN) | 20.6 (n47) | 16.3 (n106) | 11.6 (n137) | 7.8 (n186) | 6.4 (n195) | 73.5 (n820) | 16.2 |
| SMALL (MID/SD/SF) | 18.6 (n14, THIN) | 20.2 (n277) | 14.3 (n430) | 11.3 (n527) | 6.8 (n567) | 4.6 (n552) | 79.4 (n2011) | 17.9 |

A 19-year-old scores ~20 points below his mature self, a 21-year-old ~11, a 23-year-old ~5. The
gate currently prices none of that.

**Sensitivities** (full rows in `MEASURE_S1_out.txt`): at games ≥ 6 the under-bar shares rise 2–7
points at every age (part-seasons score lower — and the gate's own games leg already handles them);
keying position by the season's own label instead of `future_position` moves the age-18 pooled
share 94% → 83% and every other age by ≤ 1 point. Nothing turns on either choice.

## 5. DOES THE FLAT BAR SEPARATE FUTURES AT YOUNG AGES? (the predictive tables, C0)

Fitted full seasons 2005–2021 (n = 5,081 across all ages; every season has ≥ 5 subsequent years).
Read `dl|under` as: of the seasons the gate flags, what share belonged to players who went on to
deliver anyway.

| age cut | n | n over | n under | dl\|over | dl\|under | FF | MISS | RR | SDV over med [mean] | SDV under med [mean] |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 18–19 | 279 | 34 | 245 | 91% | **75%** | **86%** | 5% | 2.82 | 3347 [3668] | 716 [1628] |
| 20 | 439 | 123 | 316 | 97% | 65% | 63% | 3% | 10.80 | 2508 [2887] | 240 [978] |
| 21 | 534 | 199 | 335 | 91% | 58% | 52% | 11% | 4.89 | 1748 [2424] | 111 [635] |
| 22 | 603 | 278 | 325 | 92% | 51% | 39% | 12% | 6.18 | 1437 [2087] | 16 [467] |
| 23 | 589 | 309 | 280 | 90% | 51% | 34% | 19% | 4.72 | 1250 [1825] | 29 [385] |
| **24+ (the bar's home ground)** | 2637 | 1688 | 949 | 82% | **33%** | **18%** | 32% | 3.82 | 603 [1140] | 0 [155] |

Two readings, both true, both owed to the owner:

- **The flat bar is not noise at young ages.** RR ≈ 2.8 at 18–19: an under-bar young season really
  is ~3x likelier to belong to a washout than an over-bar one. The bar's DIRECTION carries signal
  at every age.
- **But its POSITION is mis-set for the young.** At 24+ an under-bar season means something (only
  33% of those players deliver later; median subsequent surplus 0). At 18–19 the same reading is
  mostly a false alarm: **75% of flagged seasons belong to players who deliver anyway**, carrying a
  median 716 (mean 1,628) v0-surplus points of subsequent delivery. The false-flag rate on
  eventually-delivered careers is 86% vs 18% mature — the gate treats a normal development year as
  evidence of stalling. Per-position detail (§C of `MEASURE_S1_out.txt`): FF at 18–20 is 72% KPD,
  75% KPF, 92% RUCK, 70% MID, 84% SD, 63% SF — with MISS ≤ 9% everywhere, i.e. today's young
  operating point is "flag nearly everyone, catch every washout, and mis-tax three-quarters of the
  real careers while doing it."

## 6. THE THREE CONSTRUCTIONS (all prereg'd; values in full in `MEASURE_S1_out.txt` §B)

All obey the cap law (bar ≤ flat; flat at 24+). All fallbacks for THIN cells are printed
per cell in the transcript.

- **C1 — age-quantile-matched.** The flat bar sits at percentile q* of the mature (24–28)
  distribution (KPD .40, KPF .31, RUCK .35, MID .28, SD .50, SF .43); bar(a,pos) = the same
  percentile of the age-a distribution. "Equal strictness at every age."
- **C2 — equal false-flag anchoring.** Among mature deliverer-seasons, the flat bar flags a share
  r_mature (KPD .25, KPF .12, RUCK .18, MID .12, SD .29, SF .17); bar(a,pos) = the r_mature-quantile
  of age-a deliverer-season averages. "A young season on a real career is flagged no more often
  than a mature one."
- **C3 — development-curve offset (recommended).** bar(a,pos) = flat(pos) − Δ(a, class), where
  Δ is the class-pooled mature-minus-age mean gap of §4, floored at 0 and monotone in age.
  "The same bar, moved down by exactly the measured development gap."

Head-to-head at the ages the order is about (fitted window; C0 for reference):

| construction | 18–20: FF | 18–20: MISS | 18–20: RR | TALL 18–20: FF / MISS | 21–23: FF / MISS |
|---|---:|---:|---:|---:|---:|
| C0 flat | 72% | 4% | 6.88 | 76% / 0% | 41% / 14% |
| C1 quantile-matched | 27% | 38% | 2.96 | 31% / 44% | 23% / 35% |
| C2 equal-false-flag | 19% | 49% | 2.86 | 27% / 56% | 19% / 39% |
| C3 development-offset | 23% | 41% | **3.07** | **16% / 61%** | 22% / 37% |

And the trade is favourable in value terms, not only in counts: the washouts each construction
newly passes at 18–20 are LOW-VALUE washouts — under C3 the median SDV of an under-bar season stays
near zero (51) while over-bar seasons carry 1,330; the flagged set stays the empty-future set.

**Why C3 and not the others.**

1. **It reaches the whole constituency.** C1 and C2 need an age × position distribution, and for
   young RUCK there isn't one (n = 0 at 18, 4 at 19, 9 at 20 — falsifier F1 fires): both fall back
   to FLAT there, i.e. **no relief at all for young rucks** — madden's cell. C3's class pooling
   stands on n = 47–195 (TALL) and 277–567 (SMALL) at every age 19–23.
2. **Best separation retained.** RR 3.07 at 18–20, the highest of the three; C2 buys its lower FF
   with the most washouts passed (MISS 49%).
3. **One parameter, owner-checkable.** C3 is "subtract the measured development gap," six numbers
   per class, monotone by construction. C1/C2 quantile cells wobble non-monotonically where thin
   (C1 RUCK 21 = 59.8 < RUCK 20 = 57.8 is a 15-row artefact).
4. **Sensitivity-stable.** Extending the fitted window to 2022 moves C3's 18–20 row by ≤ 1 point
   (FF 23%, MISS 40→41%, RR 3.13).

## 7. THE RECOMMENDED TABLE — C3, value per age × position

bar(age, pos) = flat(pos) − Δ(age, class). Ages ≥ 24: flat, by the cap law. Ages ≤ 18 take the
age-18 column.

| pos | 18 | 19 | 20 | 21 | 22 | 23 | 24+ (flat) |
|---|---:|---:|---:|---:|---:|---:|---:|
| KPD | 43.1 | 44.8 | 49.1 | 53.8 | 57.6 | 59.0 | 65.4 |
| KPF | 41.5 | 43.2 | 47.5 | 52.2 | 56.0 | 57.4 | 63.8 |
| RUCK | 53.2 | 54.9 | 59.2 | 63.9 | 67.7 | 69.1 | 75.5 |
| MID | 57.0 | 57.0 | 62.8 | 65.8 | 70.3 | 72.5 | 77.1 |
| SD | 55.2 | 55.2 | 61.0 | 64.0 | 68.5 | 70.7 | 75.3 |
| SF | 47.8 | 47.8 | 53.6 | 56.6 | 61.1 | 63.3 | 67.9 |

**Data support per cell** — the Δ each column subtracts, with its n and the cell dispersion
(the offsets are class-level, so support is class-level; per-position distribution n's are in §4):

| class | quantity | 18 | 19 | 20 | 21 | 22 | 23 |
|---|---|---:|---:|---:|---:|---:|---:|
| TALL | Δ | 22.3 | 20.6 | 16.3 | 11.6 | 7.8 | 6.4 |
| | n / sd | **4 THIN** / 9.7 | 47 / 10.5 | 106 / 11.8 | 137 / 11.8 | 186 / 12.8 | 195 / 14.7 |
| SMALL | Δ | 20.1* | 20.2 | 14.3 | 11.3 | 6.8 | 4.6 |
| | n / sd | **14 THIN** / 10.5 | 277 / 13.5 | 430 / 15.6 | 527 / 16.8 | 567 / 17.7 | 552 / 17.6 |

\* SMALL 18's raw offset (18.6, n = 14) violated monotonicity against age 19 and was pooled with it
(prereg'd pool-adjacent-violators), landing at 20.1. **Both age-18 columns are THIN and are honest
extrapolations of the age-19 cells more than measurements** — they matter little in practice
(an age-18 season is nearly always games-flagged anyway; 18 full seasons exist in the whole store)
but they are flagged here, not smoothed silently. Every cell at ages 19–23 clears the n ≥ 15 law.
Standard error of each Δ ≈ sd/√n: ≤ 1.6 points for every cell with age ≥ 19.

## 8. MISCLASSIFICATION BOTH WAYS, C0 vs C3 (fitted window, full tables in transcript)

| | eventual-deliverer seasons flagged (FF) | true-staller seasons passed (MISS) |
|---|---|---|
| ages 18–19 | 86% → **26%** (SMALL) / 40% → **14%** (TALL) | 5% → 39% (SMALL) / 0% → 60% (TALL, n=7 under, THIN) |
| ages 18–20 | 72% → **23%** | 4% → 41% |
| ages 21–23 | 41% → **22%** | 14% → 37% |
| ages 24+ | 18% (unchanged) | 32% (unchanged) |

The passed washouts are cheap: median SDV of what C3 still flags at 18–20 is 51 points vs 1,330 for
what it passes; and a passed young washout is not price-inflated the way a flagged deliverer is
price-taxed — he is merely not yet discounted through Φ, while remaining exposed to every other
mechanism (β, ρ, the games leg itself next season). The asymmetry the owner priced into the gate
(median 8.5% tax, p90 37%) currently lands on the 75%-innocent; C3 moves it to a population that is
majority-guilty (dl|under 54% at 18–20 → washout-majority the moment the run reaches 2, because
consecutive under-bar seasons compound).

## 9. THE BOARD EFFECT (2026, replicated gate — engine not run)

Constituency = played in 2026, career games 1–50 (n = 263). `s` = the stall run o31_stall_run
would count.

| construction | s ≥ 1 (flagged) | s distribution |
|---|---:|---|
| C0 (today) | 246/263 = **94%** | s=0: 17 · s=1: 87 · s=2: 81 · s=3: 40 · s=4: 21 · s=5: 9 · s=6: 6 · s=7: 2 |
| C1 | 220/263 = 84% | s=0: 43 · s=1: 85 · s=2: 69 · s=3: 32 · s=4: 18 · s=5: 8 · s=6: 6 · s=7: 2 |
| C2 | 217/263 = 83% | s=0: 46 · s=1: 86 · s=2: 68 · s=3: 29 · s=4: 18 · s=5: 8 · s=6: 6 · s=7: 2 |
| **C3** | **220/263 = 84%** | s=0: 43 · s=1: 83 · s=2: 68 · s=3: 35 · s=4: 18 · s=5: 8 · s=6: 6 · s=7: 2 |

Under C3: **26 rows fully unflagged** (among them harry-dean, cooper-duff-tytler, levi-ashcroft,
sam-lalor, willem-duursma, daniel-curtin, ty-gallop, finn-o-sullivan — full list in
`APPLY_S1_out.txt`), 11 runs shortened but still ≥ 1, **0 worsened** (cap law, verified), and
**0 mature-only rows change** (murdock guard verified store-wide, not just for murdock).
Replication caveat, bounded: the engine gives out-for-remainder register names season-fraction 1.0
(games test 10 not 9.2); this replication uses 0.92 for all — **zero** constituency rows sit in the
affected [9.2, 10) games band, so the gap changes nothing here.

## 10. THE NAMED TEN, SEASON BY SEASON

Full per-season transcript in `APPLY_S1_out.txt`. `s`: stall run C0 → C3 (C1/C2 shown where they
differ).

| player | pos | seasons (year, age, games, avg) | s: C0 → C3 | what happened |
|---|---|---|---|---|
| harry-dean | KPD | 2026, 19, 17g, 59.7 | 1 → **0** | 59.7 vs age-19 bar 44.8: DELIVERED. The season the order was named for reads as what the owner says it is. |
| cooper-duff-tytler | KPF | 2026, 19, 13g, 50.3 | 1 → **0** | 50.3 vs 43.2: DELIVERED. |
| alix-tauru | KPD | 2025, 19, 10g, 51.7 · 2026, 20, 8g, 41.9 | 2 → **1** | 2025 becomes DELIVERED (51.7 vs 44.8); 2026 stays a games-leg stall (8 < 9.2). |
| isaac-kako | SF | 2025, 19, 23g, 55.2 · 2026, 20, 13g, 42.9 | 2 → **1** | 2025 DELIVERED (55.2 vs 47.8); 2026 still under even the age-20 bar (42.9 < 53.6). |
| ethan-read | KPF | 2024, 19, 4g · 2025, 20, 21g, 44.9 · 2026, 21, 13g, 45.6 | 3 → **3** | Unrelieved: 44.9 sits under even the age-20 bar (47.5) and 45.6 under the age-21 bar (52.2). C2, the most permissive at KPF 20 (42.5), would read 2025 delivered → s=1. The measurement's honest answer: read's output is below age-referenced replacement too. |
| jordan-croft | KPF | 2025, 20, 2g · 2026, 21, 16g, 39.6 | 2 → **2** | Unrelieved under all three: 39.6 is under every age-21 KPF bar (C3 52.2). |
| jedd-busslinger | KPD | 2025, 21, 7g, 44.1 · 2026, 22, 8g, **70.4** | 2 → **2** | Pure games-leg flags both years — his 2026 avg is above even the FLAT bar. No bar construction can reach him. |
| nick-madden | RUCK | 2025, 21, 3g, 86.0 · 2026, 22, 7g, **78.4** | 2 → **2** | Same: averaging above the flat RUCK bar on part-seasons, flagged on games both years. |
| kye-annand | KPD | 2026, 23, 9g, 59.8 | 1 → **1** | Games-leg fail (9 < 9.2) — the bar never gets asked. Had he played one more game: 59.8 vs age-23 bar 59.0 → DELIVERED under C3 (under C0: stall). |
| milan-murdock | SF | 2026, 26, 17g, 70.1 | 0 → **0** | Mature, above-bar, Φ = 1.00 — untouched, as the cap law guarantees. |

**What the named rows teach.** The bar re-reference does exactly what it should — it clears the
young seasons that were normal for their age (dean, duff-tytler, tauru '25, kako '25) and it
declines to clear the ones that were poor even for their age (croft, read) — but it exposes the
next defect in the same gate: **busslinger and madden are "stallers" while out-averaging the flat
mature bar**, because the GAMES leg is age-blind AND role-blind and 10 games x fraction is a heavy
ask for a developing tall. That is a finding for the owner, out of this order's scope, and it is
the reason §3's 64% figure should temper expectations of what a bar fix alone buys.

## 11. THE PREREG SCORECARD (predictions and falsifiers, scored against `PREREG_S1.md`)

| item | verdict |
|---|---|
| P1 (18–19 sit 8–20 pts under mature, TALL larger) | **HELD in direction; band edge breached** — TALL 20.6–22.3 exceeds the predicted ceiling of 20. The gap is bigger than predicted. |
| P2 (flat bar 35–65th pctile mature; ≥ 75th at 18–19 talls) | **HALF-HELD** — young half held everywhere (89–100% under-bar at 18–19 talls); mature half breached low for MID (28th) and KPF (31st). |
| P3 (young FF ≥ 2x mature) | **HELD** — 86% vs 18% at 18–19 (4.8x); 72% vs 18% at 18–20 (4x). |
| P4 (flat bar separates worse when young) | **HELD** — RR 2.82 at 18–19 vs 3.82 mature (26% lower); dl|under 75% vs 33%. |
| P5 (≥ ⅓ FF cut, MISS rise smaller in pp) | **HELD** — C3 18–20: FF −49pp vs MISS +37pp; C2: −53pp vs +45pp. |
| P6 (dean passes, murdock unchanged) | **HELD** — both, under all three constructions. |
| P7 (> half of young flags are games-leg) | **HELD** — 64%. |
| F1 (position cell n < 15 at 18–19 ⇒ position-level bar unsupported there) | **FIRED** for RUCK 18–20 and every position at 18 — this is why the class-pooled C3 is the recommendation; C1/C2 leave young RUCK with no relief at all. |
| F2 (young RR within 20% of mature ⇒ don't re-reference) | **NOT fired** — 26% below, and the dl|under gap (75% vs 33%) is the substantive case. |
| F3 (no construction cuts FF without passing > 10pp more washouts) | **NOT fired** as prereg'd (the pp rise is smaller than the pp cut) — but stated plainly: MISS does rise 4% → 41% at 18–20; §8 shows the passed washouts are the near-zero-SDV ones. |
| F4 (avg-only share < 20% ⇒ demote the whole exercise) | **NOT fired** — 36%. Section 3 leads with the games-leg fact anyway. |

## 12. THE COUPLING THE OWNER MUST KNOW BEFORE ANY BUILD ORDER (§5 of the brief; no measurement)

`_O30BP_BARS` is **one object with two jobs**. It is built once
(`_merged_recover.py` ~line 447) as `MA.REPL[pos] − rd.REPL_DROP[pos]` and consumed as:

1. **the stall gate's AVG bar** (`o31_stall_run`) — the thing this order re-references; and
2. **the v0-language production reference** — the effective positional bars that the preview lane's
   two retained par denominators (Q and the decay gate) are re-referenced to, the same object
   ORDER 30B-M asserted against the owner's Ruling-1 numbers.

Job 2 is the ruled MATURE replacement level and this seat's own outcome definitions deliberately
kept it flat (§2: DELIVERED-LATER is judged against the flat bar). **If a build order edits
`_O30BP_BARS` in place to age-reference the gate, the production reference and both par
denominators silently move with it** — a ripple no one measured and this packet does not endorse.
The clean wiring, when ruled: a NEW object (say `_O32_GATE_BARS[(pos, age)]`, flat at 24+, cap law
enforced at construction) consumed **only** inside `o31_stall_run`, with `_O30BP_BARS` untouched.
One further honest coupling: the same flat bars define this packet's OUTCOME criterion, so any
future re-ruling of the Ruling-1 levels themselves would re-open these tables too.

## 13. FILES, PROVENANCE, REPRODUCTION

| file | what |
|---|---|
| `PREREG_S1.md` | predictions/constructions/falsifiers, pushed before any result (commit `0692ae6`). |
| `s1_build.py` → `SEASON_TABLE.json`, `CENSUS_S1.txt` | the season table (11,340 played seasons, 2005–2026) and census. Store `cb38ef11`. |
| `s1_measure.py` → `MEASURE_S1_out.txt`, `CONSTRUCTIONS_S1.json` | every distribution, every construction cell with n and fallback, every predictive table. |
| `s1_apply.py` → `APPLY_S1_out.txt` | board effect, mature guard, the named ten. |

Reproduce: `python docs/evidence/order32_s1_2026-08-17/s1_build.py` then `s1_measure.py` then
`s1_apply.py` (pure-python + json; threads pinned; engine never imported — the gate is transcribed
from `_merged_recover.py` ~3319 and the transcription is line-cited in each script header).
Exclusions and thresholds, one list: no era normalization (owner ruling); gameless seasons never
counted; 2026 never in a fitted cell; fitted window 2005–2021 (sensitivity ≤ 2022 shown); THIN
= n < 15, all fallbacks printed; no winsorisation; cap law everywhere.

*— Seat S1, 2026-08-17. Measurement only; the fallback if nothing is ruled is the current flat
bar, which stays operative untouched.*
