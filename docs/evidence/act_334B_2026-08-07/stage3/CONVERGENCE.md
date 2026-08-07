# Stage 3 step 8 — THE CONVERGENCE MEASUREMENT

## Instruments and what moved

The four instrument files were copied to scratch and re-run on the FINAL stage-3 workspace engine.
Committed here beside the tables: `emit_matrix_338.py`, `noarb_table_338.py`, `noarb_ext_338.py`,
`harness_pvc_REPINNED_pass3.py`.

**Harness pin re-pointed (one):** `EXPECT_V0SURF` `af556bdca53d` → **`3e8e50de5103`** — the DECLARED
surface refit around the settled ladder moved the year-zero surface signature. The assert is
byte-identical; only the pinned value moved, and the loader was re-run against the stage-3 matrix to
prove it accepts (store 37ced3ce, v0surf 3e8e50de5103, ND 1197). `EXPECT_STORE` (37ced3ce) and
`EXPECT_N` (1197) did not move — both re-measured, not assumed.

**Re-emitted matrix:** `per_entrant_338_stage3.json`, md5 **`b7ed144ec5e4d44263d553a2c23d919b`**
(store 37ced3ce, engine head a0a20d6e, v0surf 3e8e50de51030297c99cf367161c161f, frozen=True,
2645 records, ND teaching population 1197).

## THE WHOLE-COHORT YEAR-RATIO ROW

Whole cohort n = 1197, busts at 0 in every denominator, `mean_yr0` taken over the SAME included set as
each row. Years 0–9:

| yr | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| n | 1197 | 1197 | 1197 | 1197 | 1197 | 1139 | 1075 | 1014 | 950 | 886 |
| ratio | 1.000000 | 0.965667 | 1.197198 | 1.352823 | **1.432364** | 1.430640 | 1.393985 | 1.210792 | 0.997166 | 0.772468 |

## THE PEAK

* **PEAK YEAR = 4** — argmax over the full-inclusion years 0–4, the same convention stage 2 used.
* **PEAK VALUE = 1.432364**
* **DISTANCE TO 1.40 = +0.032364**

**1.432364 ∈ [1.35, 1.45] → the rule says DONE. ONE iteration used. No refinement was performed and
none was permitted.** (Stage 2 measured the same ratio at **1.5345** on the frozen surface; the
re-anchor plus the declared refit carried it to 1.4324.)

## THE SPLITS — readouts only, no estimator bands on them

| cut | n | peak year | peak ratio | distance to 1.40 |
|---|---|---|---|---|
| **whole cohort 1-64** | 1197 | 4 | **1.432364** | +0.032364 |
| **picks 1-20** | 377 | 4 | **1.428538** | +0.028538 |
| **picks 21-64** | 820 | 4 | **1.438430** | +0.038430 |

Both splits peak at year 4 and both land inside the band, 0.0099 apart — the per-pick re-anchor did
what it was built to do: it took a curve whose head and tail were mis-anchored by different amounts and
left the two ends within a hundredth of each other.

## YEAR-1 TO PEAK, all three cuts

| cut | mean yr1 | mean yr4 (peak) | yr1 → peak |
|---|---|---|---|
| whole cohort 1-64 | 775.2189 | 1149.8747 | **1.483290** |
| picks 1-20 | 1523.1698 | 2232.9019 | **1.465957** |
| picks 21-64 | 431.3439 | 651.9463 | **1.511431** |

Year 1 sits *below* year 0 in every cut (0.9657 / 0.9745 / 0.9517): the engine's first as-of revaluation
prices a single played season against a draft-day pedigree, and most entrants come off it. The
yr1→peak figures are therefore larger than the yr0→peak ratios, and both are reported rather than
one standing in for the other.

## Files

`noarb_table_stage3.txt` / `.json` — years 0–7, whole cohort + both pick splits, with the zero-source
breakdown. `noarb_ext_stage3.txt` — the extended cuts: years 0–9, the 2020 class, and the recency
windows (last 10 / 12 / 15 classes). `convergence_stage3.json` — the machine-readable rows above.
