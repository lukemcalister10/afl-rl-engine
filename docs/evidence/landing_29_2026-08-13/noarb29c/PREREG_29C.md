# PREREGISTRATION — ORDER 29C, THE RE-BASED NO-ARB READING

**Filed before the ORDER 29C emitter exists, before `per_entrant_29C.json` exists, and before either
cohort instrument has been pointed at anything. Committed in its own commit. NEVER EDITED.**

Brief: issue #334 comment 5289123976. Branch `land/order-29`, tip `77ede64`, board `36d5dfc7`.
This is a MEASUREMENT act. No engine, store, curve, artifact or board byte moves. The only tree
changes ORDER 29C is permitted are `docs/evidence/landing_29_2026-08-13/noarb29c/` and one appended
packet section.

---

## 0. THE DEFECT BEING CURED, AND THE ONE THING THAT CHANGES

ORDER 29 and ORDER 29B both read a cohort matrix whose **year-0 column comes from the frozen fitted
surface**: `emit_matrix_338.py:252` writes `v0 = round(v0_start(p), 1)`, while years 1…7 are
`ev(p, Y)`. ORDER 29B wired `ev()` to the landed entry law and measured the consequence
(`NOARB_MARGINS_29.md` §B3): **0 of 2648 year-0 cells moved**, the whole margin move sat in the
numerator, and P29B-25/26 were scored breached *for a reason about the plumbing rather than about the
board*. The review pack is therefore **mixed-basis**: its numerator is the landed law and its
denominator is the pre-landing surface.

ORDER 29C produces the **coherent** reading. One declared change to a copied emitter:

> the `v0` column is the **LANDED ENTRY LAW's** day-0 price — the same object `ev()` returns for a
> day-0 entrant on board `36d5dfc7` — instead of `v0_start(p)`.

Years 1–7 are not touched. The engine is not touched. The instruments are not touched.

### THE LAW, quoted from `_merged_recover.py` (commit `13cbebb`), not paraphrased

```
day0_v0(p):  p['_pool']                     -> float(MA.pool_v0_of(p))        # cell '<pathway>|<gfut>'
             type ND and 1 <= pick <= 64    -> float(nd_v0.posv[MA.gfut(p)][pick])
             otherwise                      -> None
ev(day-0 entrant, Y) = day0_v0(p) * _PL_F                      # BOARD -> ENGINE currency
printed              = int(round(ev / _F)),  and _F == _PL_F   # both read pick_redenomination.json
```

The numéraire `s` is **already inside both published objects** (`posv` is built on the shipped ladder
`raw × s`; the pool cells carry `× anchor_factor == s == 0.9400914291048137`), so `_PL_F = 1.0524` is
the only conversion and it is applied exactly once. The two Option-A borrowed cells
(`PDN|KPF` 92.35874340265629, `PDS|KPF` 83.97715038537063) are consumed through `MA.pool_v0_of`, the
one accessor, exactly as the board consumes them.

### WHAT THE PREDICTIONS BELOW ARE MADE FROM, AND WHAT THEY CANNOT SEE

Filed in this same Step-1 commit, as this preregistration's own auditable inputs:

| file | what it does | what it may NOT see |
|---|---|---|
| `o29c_lawprobe.py` · `LAWPROBE_29C.{json,_out.txt}` · `LANDED_V0_29C.json` | replicates the law standalone; proves it against the board's 89 printed day-0 numbers; walks the standing emitter's own population and computes the landed-law year-0 column | any instrument, any matrix |
| `o29c_predict.py` · `PREDICT_29C.{json,_out.txt}` | re-derives, in THIS SEAT'S OWN CODE, the aggregation the two instruments perform, over the **committed** 29B matrix `ca24a49a` with the year-0 column substituted | the instruments themselves — it never runs them |
| `o29c_delta.py` · `V0DELTA_29C.json` · `o29c_roundtrip.py` · `ROUNDTRIP_29C.json` | count the year-0 movement and the 1-dp round-trip | as above |

**Therefore the numbers below are sharp rather than adjectival, and a wrong one is a scoreable
breach.** If this seat's model of an instrument is wrong, Step 3's real instrument will disagree with
this file and the prediction is scored **BREACHED** — that is precisely what makes filing it worth
doing. Step 3 is forbidden to edit this file, the calculators, or their outputs.

---

## 1. THE PREDICTIONS, BY NUMBER

### P29C-1 — THE REPLICATION IS EXACT, 89 OF 89, TOLERANCE 0
For the 89 rows of `DAY0_29B_FINAL.json` (board `36d5dfc7`), the standalone law gives
`int(round(landed_v0_board(p))) == row['printed']` **and** `landed_v0_board(p) == row['derived_v0']`
at `|err| == 0.0`, on **89 of 89**, with **zero** rows excluded and zero tolerance. The ORDER 29C
emitter re-asserts this at emit time and HALTS if it is not 89 of 89.

### P29C-2 — NOT ONE ENTRANT IS UNMAPPABLE, AND NO DAY-0 POSITION HAS TO BE RECONSTRUCTED
**0 of 2648** records fail to map to a landed-law day-0 object. The brief allows for a historical
entrant lacking a field the law needs; **that case does not arise, and the reason is measurable**:
the law's position key is `MA.gfut(p)`, which reads `p['_futpos']`, else `GRP[p['_pos_now']]`, else
`GRP[p['pos']]` — **all store columns, none scoring-derived**, so the key is invariant under the
walk-forward's scoring truncation. Census: **`_futpos` supplies the key on 2648 of 2648 records**, so
the `layer1`/LEDGER day-0-position convention is never reached. Predicted disclosure: the emitter
prints this census and an unmappable count of **0**; any non-zero is excluded and counted loudly.

### P29C-3 — THE ONLY DIFFERENCE BETWEEN THE TWO MATRICES IS THE YEAR-0 COLUMN
Diffed record by record against `per_entrant_O29B.json` (`ca24a49a`): **every field except `v0` is
byte-identical on all 2648 records** — `vpath`, `yrs`, `anchor`, `cur`, `peak`, `eq`, `pw`,
`games_by`, `seasons`, every predicate and every `#338` disclosure. `meta` matches except the
emitter's own identity fields. Population stays **2648**; ND 1–64 teaching stays **1447**; ruled pool
stays **1201**.

### P29C-4 — THE YEAR-0 COLUMN MOVES ON EVERY SINGLE ROW
**2648 of 2648** `v0` cells move (ORDER 29B moved **0 of 2648**; that contrast is the whole point of
the act). **887 rise, 1761 fall.** Σ`v0` over all records **1,904,793.4 → 1,369,559.9**, a factor of
**0.7190**.

### P29C-5 — THE PER-ARM YEAR-0 MEANS, TABLED IN ADVANCE
Mean `v0` in engine currency over the standing emitter's own population. The brief anticipated pool
arms falling "~2–3×"; **that is right for four arms and materially wrong for three, and the measured
numbers are filed rather than the expectation**: `IRE`, `PDN` and `PDS` fall by **~7–8×**, and `MSD`
by only **1.41×**.

| arm | n | OLD basis (`v0_start`) | LANDED LAW | old ÷ new |
|---|---:|---:|---:|---:|
| ND 1–64 | 1446 | 746.61 | **755.93** | **0.988** (year-0 *rises*) |
| RD | 691 | 761.45 | **245.39** | 3.103 |
| ND>64 | 122 | 832.54 | **264.24** | 3.151 |
| MSD | 106 | 497.16 | **351.74** | 1.413 |
| UNR | 59 | 281.76 | **115.24** | 2.445 |
| IRE | 57 | 597.26 | **86.41** | 6.912 |
| SSP | 52 | 424.26 | **197.82** | 2.145 |
| PDA | 51 | 626.13 | **193.93** | 3.229 |
| PDN | 43 | 601.34 | **86.19** | 6.977 |
| PDS | 21 | 678.42 | **85.28** | 7.955 |

**The brief's own diagnosis is confirmed by the RD line**: the old matrix's RD mean year-0 is
**761.45**, while the rederived RD cells sit at 206–369 — the old column really was reconstructing the
pre-landing entry class. The landed-law RD mean is **245.39**, inside the rederived band.

### P29C-6 — FIVE ROWS PRICE TO EXACTLY ZERO, AND THAT IS A POPULATION CHANGE
The artifact's own declared `ruck_floor_63_64` (`posv_63 = posv_64 = 0.0`, ORDER 28 §9.4, floored not
clipped) puts **five** RUCK rows at year-0 **0.0**: `matthew-dick` (63), `matthew-arnot` (63),
`tom-derickx` (63), `tom-downie` (64), `luke-davis` (64). Consequences, predicted:
* `noarb_table_allarm.py` excludes `v0 <= 0`, so its eligible set goes **2647 → 2643** and
  **PRIMARY n 2215 → 2211**. **MODERN n stays 540** (none of the five is a modern cohort).
* `noarb_table_338.py` does **not** exclude them; they stay in the denominator at 0, so the legacy ND
  population stays **1200** and the `EXPECT_N` pin holds.

### P29C-7 — THE 1-dp ROUND-TRIP IS 87 OF 89, AND THAT IS DISCLOSED, NOT REPAIRED
The matrix cell keeps the standing emitter's convention `round(·, 1)` — ORDER 29C changes the VALUE,
never the schema or the rounding. Consequence: `int(round(matrix_v0 / _PL_F))` reproduces the board's
printed day-0 on **87 of 89** rows; **`hunter-holmes` (661 vs 660)** and **`cooper-bell` (409 vs 408)**
land one point low purely from the 1-dp cell. **This seat will not un-round the column to make the
number 89** — that would be a second, undeclared change to the emitter. P29C-1 (the law's own
unrounded arithmetic) is the replication proof; this is the disclosed cost of the schema.

### P29C-8 — THE POOL ARMS' yr1/yr4 RISE, AND WHICH ONES CROSS 1.0
Pooled ratio within the arm, all-arm construction. `29B` = the historical-print basis already
published in `NOARB_MARGINS_29.md`; `29C` = predicted landed-law basis.

**PRIMARY, cohorts 2005–2023**

| arm | n | yr1 29B | **yr1 29C** | crosses 1.0? | yr4 29B | **yr4 29C** | crosses 1.0? |
|---|---:|---:|---:|:--|---:|---:|:--|
| ND | 1309 | 1.2308 | **1.3068** | already >1, stays | 1.5539 | **1.6484** | already >1, stays |
| RD | 623 | 0.4602 | **1.4461** | **YES** | 0.4585 | **1.4407** | **YES** |
| MSD | 55 | n/a | **n/a** | n/a (debut-year gap) | 0.6039 | **0.8567** | **NO** |
| UNR | 49 | 0.4363 | **1.0490** | **YES** | 0.5612 | **1.3492** | **YES** |
| IRE | 47 | 0.2230 | **1.5547** | **YES** | 0.2008 | **1.3997** | **YES** |
| PDA | 43 | 0.4120 | **1.2628** | **YES** | 0.4738 | **1.4523** | **YES** |
| PDN | 33 | 0.1484 | **1.0361** | **YES** | 0.1685 | **1.1764** | **YES** |
| SSP | 31 | 0.9474 | **2.4081** | **YES** | 0.7390 | **1.8783** | **YES** |
| PDS | 21 | 0.1721 | **1.3689** | **YES** | 0.1233 | **0.9806** | **NO — stops just short** |

**MODERN, cohorts 2019–2023**

| arm | n | yr1 29B | **yr1 29C** | crosses? | yr4 29B | **yr4 29C** | crosses? |
|---|---:|---:|---:|:--|---:|---:|:--|
| ND | 325 | 1.2119 | **1.2386** | stays >1 | 1.3037 | **1.3324** | stays >1 |
| RD | 66 | 0.3650 | **1.3157** | **YES** | 0.3570 | **1.2869** | **YES** |
| MSD | 55 | n/a | **n/a** | n/a | 0.6039 | **0.8567** | **NO** |
| SSP | 31 | 0.9474 | **2.4081** | **YES** | 0.7390 | **1.8783** | **YES** |
| PDN | 25 | 0.1371 | **1.0339** | **YES** | 0.0865 | **0.6523** | **NO** |
| UNR | 13 | 0.4865 | **1.3188** | **YES** | 0.2600 | **0.7046** | **NO** |
| PDA | 13 | 0.3318 | **0.9344** | **NO** | 0.4141 | **1.1664** | **YES** |
| IRE | 12 | 0.1246 | **1.0000** | **EXACTLY 1** | 0.0244 | **0.1959** | **NO** |

### P29C-9 — THE IRE MODERN yr1 LANDS ON EXACTLY 1.0000000000, AND THAT IS THE THESIS IN ONE CELL
Predicted **1.0000000000**, not approximately. All 12 modern `IRE` rows played no games in their
cohort year 1, so under the 29B wiring their year-1 `ev()` **is** a day-0 print — the same number the
landed law gives as their year-0. On a coherent ruler the yr0→yr1 step for a zero-evidence entrant is
therefore **exactly flat**, and the 0.1246 the mixed-basis pack reported was an artefact of measuring
a landed-law numerator against a pre-landing denominator. **If this cell prints anything other than
1.0000, this seat has misread the plumbing and P29C-9 is BREACHED.**

### P29C-10 — THE ND READINGS MOVE ONLY MODESTLY, AND THEY IMPROVE SLIGHTLY
ND was already ≈ the new basis (the surface is curve-keyed and was re-baked at ORDER 29), so the
in-curve ND year-0 mean moves **746.61 → 755.93, +1.25%** — it **RISES**, which pushes ND appreciation
**DOWN**. Predicted direction: **every legacy ND reading improves relative to ORDER 29B, and by a
small amount.** The measurable driver is filed: the positional relativity `posv[g][pick]/curve[pick]`
over the in-curve ND rows reads **min 0.0000 · max 3.5948 · mean 0.9531**, and equals 1.0 on **0** rows.

### P29C-11 — THE ND yr0→1 ARBITRAGE PERSISTS ON THE LANDED-LAW BASIS
All three legacy ND groups remain **ARB**. Predicted, against the 14% carry:

| group | n | margin 29B | **margin 29C** | verdict 29C |
|---|---:|---:|---:|---|
| ALL picks 1–64 | 1200 | −18.01% | **−16.74%** | **ARB** |
| picks 1–20 | 380 | −20.93% | **−17.12%** | **ARB** |
| picks 21–64 | 820 | −13.56% | **−16.12%** | **ARB** |

Note the split: 1–20 and ALL improve, **21–64 gets worse**. Predicted `yr1`: **1.3074 / 1.3112 /
1.3012**.

### P29C-12 — THE ALL-ARM WINDOWS DO **NOT** STAY NO-ARB. BOTH FLIP, AND HERE ARE THE NUMBERS
The brief asked for "no-arb, or state otherwise with a number". **Stating otherwise, with numbers.**

| window | n 29C | apprec 0→1 29B | **apprec 0→1 29C** | margin 29B | **margin 29C** | verdict 29C |
|---|---:|---:|---:|---:|---:|---|
| PRIMARY 2005–2023 | 2211 | −6.75% | **+33.10%** | +20.75% | **−19.10%** | **ARB — NEW** |
| MODERN 2019–2023 | 540 | −4.11% | **+26.48%** | +18.11% | **−12.48%** | **ARB — NEW** |

**This is the single most consequential prediction in the file and it is the one the owner's merge
decision most depends on.** The all-arm instrument is the *deciding* one, and on the coherent ruler it
opens an arbitrage in both windows. The cause is not the numerator — the numerator is byte-identical
to 29B's — it is that the pool arms' year-0 denominators fall by 2–8×, which is what the landed law
actually prices them at. **Predicted total: 5 of 5 readings ARB on the landed-law basis** (ORDER 29B's
own basis: 3 of 5; live: 0 of 5). On the canonical reporter's two-variant line that reads
**"ARBITRAGES OPENED: 8 of 10 readings"** (5 on the 29C variant + 3 on the 29B control variant).

### P29C-13 — THE HISTORICAL-PRINT CONTROL REPRODUCES §B2 TO THE DIGIT
Run alongside on the unchanged `per_entrant_O29B.json` (`ca24a49a`) with the same instrument copies:
PRIMARY **−6.75% / +20.75%**, MODERN **−4.11% / +18.11%**, ND **+32.01% / −18.01%**, **+34.93% /
−20.93%**, **+27.56% / −13.56%**; **3 ARB**. Any deviation means the pipeline moved and the 29C
reading is void.

### P29C-14 — NO PIN MOVES AND NO INSTRUMENT IS RE-POINTED
Store `cb38ef11`, v0surf `4405cba2b42f`, `EXPECT_N 1200` all hold on the 29C matrix, because ORDER 29C
changes neither store, surface nor teaching population. **`noarb_table_338.py` md5
`0f8220351c64c56ccfa90c60edcdfa5f`** everywhere, computed at run. `noarb_table_allarm.py` and
`harness_pvc_REPINNED_pass3.py` byte-unchanged. **`emit_matrix_338.py` md5 `bffde2f7…` byte-unchanged
— the 29C emitter is a COPY under `noarb29c/`, and the standing emitter is not touched.** If any pin
refuses, this seat **stops and reports** rather than re-pointing anything.

### P29C-15 — THE BOARD DOES NOT MOVE, AND NOTHING MERGES
`rl_app_data.json` stays **`36d5dfc73e2b508ece530bc7dfae2090`** — instruments read the matrix, never
the board. Store `cb38ef11`, `pvc_curve_v2.json` `911774bc`, `rl_model.py` `14000af2`,
`_merged_recover.py` `a353a9d3`, `v0surf.pkl` `5dd34ca8` all unmoved. Tree diffs confined to
`docs/evidence/landing_29_2026-08-13/noarb29c/` plus the packet append. **PR #510 stays HELD; the
title is not touched; nothing merges.**

---

## 2. THE STANDING RULE FOR STEP 3

**If a reading embarrasses a prediction, the reading stands and the prediction is scored BREACHED.**
No literal is re-pointed, no window moved, no population filtered, no rounding changed, and no
predicate switched after seeing a number. If an instrument halts, **the halt is the finding**: it is
pushed and reported verbatim, not worked around.
