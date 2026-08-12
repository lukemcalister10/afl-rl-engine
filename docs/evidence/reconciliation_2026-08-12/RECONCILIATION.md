# RECONCILIATION — ORDER 26A

**The two "yr4/yr0" figures reconciled to ZERO residual.** Same players, same years, row by row.

Read-only. Nothing under `engine/` written. No board built. No pin moved.

- matrix `per_entrant_O25R4.json` md5 `3c6ffcdeaac9786473f3f017dba1d61e`, store `d9a24282`,
  v0surf `6ef67f07db98`, window end **2026**
- scripts: `o26a_bridge.py` → `BRIDGE.json` / `BRIDGE_out.txt`; `o26a_rows.py` → `ROWS.json` /
  `ROWS_out.txt`
- the all-arm instrument and its ORDER 25 output are copied into `instruments/` so the record is
  durable independent of the shared scratchpad.

---

## 0. CONTROL — both instruments reproduced before a single step is taken

Neither instrument is modified and neither is imported for its answer. Both are re-implemented in
`o26a_bridge.py` from their sources, then checked against their own **published** outputs. If this
control failed, nothing below would be readable.

| reading | re-implemented | published | |
|---|---|---|---|
| derive RD | 1.379793413 | 1.379793 | PASS |
| derive ALL POOL | 1.338050228 | 1.338050 | PASS |
| derive NATIONAL | 1.554716748 | 1.554717 | PASS |
| allarm RD (PRIMARY) | 0.508978685 | 0.5090 | PASS |
| allarm ND (PRIMARY) | 1.480343866 | 1.4803 | PASS |

---

## 1. THE BRIDGE TABLE

Steps applied one at a time, in the order fixed in `PREREG_ORDER26A.md` §2, starting from the
all-arm reading and landing on the derivation's.

| # | knob | step | reading | n in | delta | share of gap | cause |
|---|---|---|---|---|---|---|---|
| 0 | — | **allarm as published** | **0.508979** | 623 | — | — | baseline |
| P | population | cohort window 2005–2023 → all eligible cohorts | 0.520725 | 667 | **+0.011746** | **1.35 %** | **(a) POPULATION** |
| I | year index | `N=4` (`cohort+N−1`) → `cohort+3` | 0.520725 | 667 | **+0.000000** | **0.00 %** | (b) YEAR INDEXING |
| S | semantics | allarm skip/zero branches → derive skip/zero branches | 0.520725 | 667 | **+0.000000** | **0.00 %** | (a) POPULATION rules |
| A | aggregation | `mean/mean` → `sum/sum` | 0.520725 | 667 | **+0.000000** | **0.00 %** | form |
| D | entry price | `r['v0']` → `anchor_of(r)` = signed level × `_PL_F` | **1.379793** | 667 | **+0.859069** | **98.65 %** | **(c′) ENTRY-PRICE OBJECT** |
| = | | **derive as published** | **1.379793** | 667 | | | |

**RESIDUAL = 0.000e+00.** Exactly zero, not "below tolerance" — the last step lands on the
derivation's published figure bit for bit.

Total gap 1.379793 − 0.508979 = **0.870815**, of which population 0.011746 and the entry-price
object 0.859069. Nothing else moves anything.

---

## 2. THE ROWS BEHIND EACH STEP

### STEP P — POPULATION (+0.011746, 1.35 % of the gap)

derive RD `n = 691`; allarm RD `n = 623`; **68 rows differ**, by cohort:

| cohort | rows | fate in the yr4 reading |
|---|---|---|
| 2004 | 44 | **ADMITTED** — `cohort+3 = 2007 ≤ 2026` |
| 2024 | 9 | skipped, `Y = 2027 >` window end |
| 2025 | 9 | skipped, `Y = 2028 >` window end |
| 2026 | 6 | skipped, `Y = 2029 >` window end |

Only the **44 cohort-2004 rows** actually move the number. They are the pre-2005 rookie class the
all-arm instrument's PRIMARY window excludes by design; the derivation carries no cohort window at
all. The 24 rows from cohorts 2024–2026 are counted in derive's `n = 691` but are **skipped by its
own `Y > W` branch**, which is why the reading is taken over 667 rows and not 691 — the published
`n = 691` is a POPULATION count, not the count actually read. That mismatch between the printed n
and the read n is a documentation defect, listed as an anomaly in `SUMMARY.md`.

Named, from `ROWS_out.txt` (cohort 2004, `Y = 2007`, mark / signed anchor / board v0):

| player | pos | mark@2007 | anchor | board v0 |
|---|---|---|---|---|
| andrew-carrazzo | MID | 3798.0 | 305.2 | 441.5 |
| nathan-foley | MID | 3965.0 | 305.2 | 596.5 |
| aaron-davey | SF | 2353.0 | 229.4 | 427.1 |
| brett-jones | SD | 824.0 | 257.8 | 308.6 |
| paul-duffield | SD | 401.0 | 257.8 | 565.8 |
| james-condos | MID | 0.0 | 305.2 | 255.9 |
| luke-buckland | SD | 0.0 | 257.8 | 565.8 |
| ben-clifton | KPD | 0.0 | 388.3 | 946.0 |

(44 in total; the full key list is in `ROWS.json` → `step_P.admitted`.)

Skipped, named: `loch-rawlinson`, `finnbar-maley`, `sam-clohesy`, `odin-jones`, `vigo-visentini`,
`xavier-walsh` … (24 in total, `ROWS.json` → `step_P.skipped`).

The 2004 class reads slightly better than the 2005–2023 average, which is why the step is positive
and small.

### STEP I — YEAR INDEXING (+0.000000, 0 % of the gap)

Measured, not assumed, over **all 2644 eligible rows**: the number of rows where derive's
`cohort+3` differs from allarm's `cohort+N−1` at `N=4` is **0**.

The brief's framing — "derive uses cohort+3, allarm uses N=4" — describes a real textual difference
that is arithmetically null: `N=4` resolves through `Y = cohort(r) + N − 1` to `cohort+3`. Both
instruments read the **same calendar year for every single row**. There is no off-by-one.

### STEP S — SKIP / ZERO SEMANTICS (+0.000000, 0 % of the gap)

The brief flagged `o25_derive.py:yr4()`'s two `continue` branches (which drop the player's entry
out of the denominator) against its zeroed-dead branch (which keeps it). Both branches are real.
**They are also present, identically, in the all-arm instrument.** Branch for branch:

| condition | derive `yr4()` | allarm `value_at()` + `reached` filter | same? |
|---|---|---|---|
| `Y > window_end` | `continue` — entry leaves denominator | dropped by the `reached` filter — entry leaves denominator | **yes** |
| `Y < yrs[0]` | `continue` — entry leaves denominator | `'pre'` — excluded from both mean and mean_v0 | **yes** |
| `Y > yrs[-1]` | `v = 0.0`, entry **kept** | `'ended'` → `0.0`, entry **kept** | **yes** |
| `vpath[i] is None` | `v = 0.0`, entry kept | `'null'` → `0.0`, entry kept | **yes** |
| `yrs` empty | `v = 0.0`, entry kept | `'ended'` → `0.0`, entry kept | **yes** (0 such rows) |

Rows moved: **zero**. The skip branches are not a difference between the two instruments, so they
cannot be any part of this gap. (What they *are*, and whether they bias the 1.38 in absolute terms,
is answered under H1 in `SUMMARY.md`: they do not — they retain 96.5 % of RD entry price.)

### STEP A — AGGREGATION FORM (+0.000000, 0 % of the gap)

allarm prints `mean(value at N) / mean(v0)`; derive computes `Σ value / Σ entry`. The means are
taken over the **same included set** as the denominator, so the `n` cancels exactly and the two are
algebraically the same object. Rows moved: **zero**.

### STEP D — THE ENTRY-PRICE OBJECT (+0.859069, 98.65 % of the gap)

Rows moved: **all 667**. Every single row in the reading.

- allarm divides by `float(r['v0'])` — the **board's v0-surface price**, the modelled year-zero
  value of that entrant (v0 surface signature `6ef67f07db98`, 339 distinct values among the 691
  RD rows).
- derive, under `--basis anchor`, divides by `anchor_of(r)` — the **signed entry anchor**, the
  engine's signed pool level for that division × `_PL_F = 1.0524`. Six values only, one per
  position.

Over the 667 rows read: **Σ board v0 = 485,738** vs **Σ signed anchor = 183,314**, a ratio of
**2.6498**. `0.520725 × 2.6498 = 1.379793`. That is the entire remaining gap.

Per position (the whole of an RD row's anchor):

| pos | signed level | anchor (× 1.0524) | mean board v0 | v0 / anchor | n |
|---|---|---|---|---|---|
| MID | 290 | 305.20 | 643.5 | 2.108 | 166 |
| SD | 245 | 257.84 | 761.1 | 2.952 | 156 |
| SF | 218 | 229.42 | 475.8 | 2.074 | 143 |
| KPD | 369 | 388.34 | 1381.9 | 3.558 | 71 |
| KPF | 206 | 216.79 | 1108.6 | 5.114 | 63 |
| RUCK | 257 | 270.47 | 355.7 | 1.315 | 68 |

Named — the same player, the same year, the same mark, two entry prices:

| player | pos | Y | mark@Y | anchor | board v0 | mark/anchor | mark/v0 |
|---|---|---|---|---|---|---|---|
| xavier-richards | KPD | 2016 | 626.0 | 388.3 | 2336.7 | 1.612 | 0.268 |
| levi-casboult | KPF | 2013 | 619.0 | 216.8 | 2230.7 | 2.855 | 0.277 |
| rory-thompson | KPD | 2014 | 959.0 | 388.3 | 2215.7 | 2.470 | 0.433 |
| jordon-butts | KPD | 2022 | 306.0 | 388.3 | 2135.4 | 0.788 | 0.143 |
| jack-frost | KPD | 2016 | 209.0 | 388.3 | 1830.1 | 0.538 | 0.114 |
| matthew-taberner | KPF | 2016 | 795.0 | 216.8 | 1791.6 | 3.667 | 0.444 |
| callum-moore | KPF | 2019 | 85.0 | 216.8 | 1773.4 | 0.392 | 0.048 |
| fletcher-roberts | KPD | 2015 | 434.0 | 388.3 | 1735.6 | 1.118 | 0.250 |

---

## 3. THE NUMERATOR IS BYTE-IDENTICAL

Cross-checked row by row over the 623-row shared RD population: **0 numerator mismatches**. Both
instruments read the same `vpath[i]` at the same calendar year. Whatever `vpath` is, it contributes
**nothing** to this gap.

For the record, `vpath` **is** the board's as-of mark series, indexed by the parallel `yrs` list.
It is not a transformed series. The transformed object in the ORDER 25 machinery is
`realised_full(r)` in `harness_pvc_REPINNED_pass3.py:313` — an establishment-weighted (`pw`) mean
over the whole of `vpath` — and that is the **CAREER PROFILE** metric, a different metric that does
not appear in either yr4 reading. The two must not be confused; see `WEDGE_DECOMPOSITION.md`, where
`realised_full` is the calibration basis that sets the signed levels and therefore sets the
denominator that step D swaps in.

---

## 4. THE SAME BRIDGE ON THE OTHER TWO HEADLINES

| reading | allarm | derive | bridge |
|---|---|---|---|
| RD | 0.508979 | 1.379793 | population +0.011746, entry object ×2.6498 |
| ALL POOL | 0.499940 (derive pop, v0 basis) | 1.338050 | entry object ×2.5743 |
| NATIONAL | 1.480344 (allarm ND arm) | 1.554717 | **population only** — `anchor_of ≡ v0` for a national row, so step D is the identity |

The NATIONAL line is the cleanest confirmation of the whole finding: for a national row the two
entry-price objects are the same object, and the two instruments differ by population alone
(allarm's ND arm is every ND row in cohorts 2005–2023, n=1310; derive's NATIONAL is ND rows with
`raw_pick` 1–64 and not pool-flagged, n=1443). There is no 2.7× anywhere on the national side.

---

## 5. WHAT THE RECONCILIATION SETTLES

1. **The two figures are not in conflict.** They are two different ratios that share a numerator.
   Both are correct readings of their own denominators.
2. **1.380 is "board marks at season 4 per unit of SIGNED ENTRY COST".** It answers: what does a
   club get back, at year 4, for what it pays to sign a rookie.
3. **0.509 is "board marks at season 4 per unit of BOARD ENTRY PRICE".** It answers: what does the
   board's own year-zero valuation of this player look like four seasons later.
4. The gap between them is a statement about the board, not about either instrument: **the board's
   v0 surface prices a pool entrant at ~2.65× what signing him costs.** That is the wedge, and
   `WEDGE_DECOMPOSITION.md` takes it apart.
