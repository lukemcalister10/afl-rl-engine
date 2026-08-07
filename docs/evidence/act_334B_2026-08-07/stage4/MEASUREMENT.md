# STAGE 4 — FINAL MEASUREMENT (re-emitted on the stage-4 engine)

Everything below was re-run end-to-end on the stage-4 engine (`engine_head 9a0c7fdc`), not carried over.
The four instruments are the stage-3 ones, copied into `noarb/` and re-pointed only at the input matrix
filename and the board filename — no method change.

**Harness pins RE-MEASURED, none re-pointed.** `EXPECT_STORE 37ced3ce` · `EXPECT_V0SURF 3e8e50de5103` ·
`EXPECT_N 1197`, all unchanged, so no assert was patched. Emitter banner:
`store=37ced3ce engine=9a0c7fdc v0surf=3e8e50de51030297c99cf367161c161f frozen=True`.

## The matrix, old → new

| | stage 3 | **stage 4** |
|---|---|---|
| per-entrant matrix | `per_entrant_338_stage3.json`, md5 `b7ed144ec5e4d44263d553a2c23d919b` | **`per_entrant_338_stage4.json`, md5 `6a36cd7a2154272320f6c16ffa4c4d32`** |
| records | 2645 | 2645 |
| ND 1-64 (teaches curve) | 1444 | 1444 |
| ruled pool | 1201 | 1201 |
| cohort (harness ND filter) | 1197 | 1197 |
| #338 windows extended | 698 | 698 |

## THE FINAL WHOLE-COHORT ROW  (ALL picks 1-64, n=1197, classes 2004-2022)

| yr N | n incl | n zero | mean yrN | median yrN | mean yr0 (same set) | **ratio** | stage-3 ratio | Δ |
|---|---|---|---|---|---|---|---|---|
| 0 | 1197 | 0 | 802.78 | 572.0 | 802.78 | 1.0000 | 1.0000 | — |
| 1 | 1197 | 0 | 771.10 | 477.0 | 802.78 | 0.9605 | 0.9657 | −0.0052 |
| 2 | 1197 | 0 | 954.59 | 512.0 | 802.78 | 1.1891 | 1.1972 | −0.0081 |
| 3 | 1197 | 141 | 1083.64 | 625.0 | 802.78 | 1.3499 | 1.3528 | −0.0029 |
| **4** | 1197 | 258 | **1149.74** | 446.0 | 802.78 | **1.4322** | 1.4324 | −0.0002 |
| 5 | 1139 | 334 | 1142.77 | 296.0 | 798.79 | 1.4306 | 1.4306 | 0.0000 |
| 6 | 1075 | 391 | 1112.23 | 137.0 | 797.90 | 1.3939 | 1.3940 | −0.0001 |
| 7 | 1014 | 430 | 967.22 | 63.0 | 798.76 | 1.2108 | 1.2108 | 0.0000 |

**PEAK: year 4, ratio 1.4322.**

## BAND CHECK — REPORT ONLY

| | value |
|---|---|
| whole-cohort peak year | **4** (unmoved) |
| whole-cohort peak ratio | **1.432196** (stage 3: 1.432364) |
| band `[1.35, 1.45]` | **INSIDE — PASS** |
| distance to the 1.40 target | **+0.0322** (stage 3: +0.0324) |

**NOTHING WAS RETUNED.** Stage 4 moved the peak by **−0.0002** — a rounding-scale move that happens to
sit marginally CLOSER to 1.40 than stage 3 did. No dial was chosen to achieve that and no dial would be
changed if it had gone the other way; the directive's instruction is to report and flag, not to retune,
and there is nothing to flag.

The reason the peak barely moves while the calibration case moves 13.7% is structural and worth stating:
the mechanism only touches players with a thin record AND live evidence, which is a small, low-valued
slice of any draft class at any as-of year, and the peak year (4) is dominated by players who long since
crossed the establishment bar. Where the mechanism actually lives — the deep-pick early years — it shows
clearly, and only there:

| cut | N=1 Δ | N=2 Δ | N=3 Δ | peak Δ |
|---|---|---|---|---|
| picks 1-20 | −0.0010 | −0.0012 | −0.0006 | **+0.0003** |
| picks 21-64 | **−0.0117** | **−0.0190** | −0.0067 | −0.0001 |

The deep-pick cut moves an order of magnitude more than the top cut, in the first two years, and
converges by year 4. That is the mechanism's own signature, read off an instrument that knows nothing
about it.

## YR1-TO-PEAK, all three cuts

| cut | peak yr | stage 3 | **stage 4** | Δ |
|---|---|---|---|---|
| ALL picks 1-64 | 4 | 1.483282 | **1.491039** | +0.007757 |
| picks 1-20 | 4 | 1.465956 | **1.467663** | +0.001707 |
| picks 21-64 | 6 | 1.549984 | **1.569242** | +0.019259 |

Yr1-to-peak RISES, because the change cuts year-1 values (thin record, live evidence — exactly the year-1
population) and leaves the peak alone. The rise is concentrated in the deep-pick cut, again the
mechanism's own signature. This is a movement AWAY from the relocation target the act has been narrowing;
it is reported straight and not compensated for anywhere.

## PER-ENTRY-YEAR TABLE, N = 0..5  (mean value at the peak year 4 / mean value at year N)

| N | n (both) | mean yr4 | mean yrN | ratio |
|---|---|---|---|---|
| 0 | 1197 | 1149.7393 | 802.7809 | 1.432196 |
| 1 | 1197 | 1149.7393 | 771.1019 | 1.491034 |
| 2 | 1197 | 1149.7393 | 954.5865 | 1.204437 |
| 3 | 1197 | 1149.7393 | 1083.6408 | 1.060997 |
| 4 | 1197 | 1149.7393 | 1149.7393 | 1.000000 |
| 5 | 1139 | 1164.8797 | 1142.7709 | 1.019347 |

**FRONT-LOADED ASSERT** (yr1→2 increment strictly exceeds yr3→4): **+0.228561 > +0.082337 → PASS.**

## TOP-END RATIO

| | |
|---|---|
| max active display value | **10668** — Harry Sheezel (North Melbourne) |
| ratio to the numéraire (pick 1 = 3000) | **10668 / 3000 = 3.556000** |
| runners-up | Nick Daicos 9649 · Luke Jackson 8670 · Nasiah Wanganeen-Milera 8633 |

**UNMOVED from stage 3.** No top-end player is on the thin-record path, by construction.

## THE BOARD DELTA vs `6c9f8d3a`

**51 movers of 804 (6.34%) — 41 cuts, 10 lifts.** Total `655759 → 654570`, ratio **0.998187**
(delta −1189). Mean |relative move| **0.4302%** board-wide, **6.7812%** across the movers.

| age bucket | n | movers | total | ratio |
|---|---|---|---|---|
| ≤22 | 294 | **45** | 225541 → 224332 | 0.994640 |
| 23-26 | 245 | 5 | 261511 → 261506 | 0.999981 |
| ≥27 | 265 | **1** | 168707 → 168732 | 1.000148 |

The move is almost entirely inside the ≤22 bucket, which is what a thin-record mechanism should look
like. The six movers over 22 were checked one by one rather than waved through — **Mitch Podhajski (27),
Aidan Johnson (26), Liam Reidy (26), Lukas Cooke (23), Liam Puncher (23), Max Ramsden (23)** — and every
one is a pool-route entrant (`effpk 65`, no draft-day pedigree) whose **best season is 5 games or fewer**
and who has therefore never crossed the establishment bar in his career. Genuinely thin records at an
unusual age, not leakage into established players. Each is in `MOVERS_FULL.txt` with his full record.

Full list: `board_delta_vs_6c9f8d3a.txt`. Every mover with its triggering record: `MOVERS_FULL.txt`,
`movers_full.csv`, `movers_full.json`.
