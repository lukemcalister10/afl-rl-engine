# STAGE 4 AMENDMENT 1 — FINAL MEASUREMENT (re-emitted on the amended engine)

Everything below was re-run end-to-end on the amendment engine (`engine_head bc45d773`), not carried over.
The four instruments are stage 4's, copied into `noarb/` and re-pointed only at the input matrix filename
and the board filename — **no method change**. Machine output: `noarb/FINAL_TABLES.txt`,
`noarb/noarb_table_stage4a1.txt`, `noarb/noarb_ext_stage4a1.txt`, `noarb/goal_metrics_stage4a1.txt`.

**Harness pins RE-MEASURED, none re-pointed.** `EXPECT_STORE 37ced3ce` · `EXPECT_V0SURF 3e8e50de5103` ·
`EXPECT_N 1197`, all unchanged, so no assert was patched. Emitter banner:
`store=37ced3ce engine=bc45d773 v0surf=3e8e50de51030297c99cf367161c161f frozen=True`.

## The matrix, old → new

| | stage 4 | **amendment 1** |
|---|---|---|
| per-entrant matrix | `per_entrant_338_stage4.json`, md5 `6a36cd7a2154272320f6c16ffa4c4d32` | **`per_entrant_338_stage4a1.json`, md5 `b564b12e533119f49c2c6bb0c92a5d91`** |
| records | 2645 | 2645 |
| cohort (harness ND filter) | 1197 | 1197 |
| board | `b490ae8b` | **`b56bbddea15f`** |

## THE FINAL WHOLE-COHORT ROW (ALL picks 1–64, n=1197, classes 2004–2022)

| yr N | n incl | n zero | mean yrN | median yrN | mean yr0 (same set) | **ratio** | stage-4 ratio | Δ |
|---|---|---|---|---|---|---|---|---|
| 0 | 1197 | 0 | 802.78 | 572.0 | 802.78 | 1.0000 | 1.0000 | — |
| 1 | 1197 | 0 | 762.99 | 461.0 | 802.78 | 0.9504 | 0.9605 | **−0.0101** |
| 2 | 1197 | 0 | 942.66 | 506.0 | 802.78 | 1.1742 | 1.1891 | **−0.0149** |
| 3 | 1197 | 141 | 1079.89 | 624.0 | 802.78 | 1.3452 | 1.3499 | −0.0047 |
| **4** | 1197 | 258 | **1149.66** | 442.0 | 802.78 | **1.4321** | 1.4322 | −0.0001 |
| 5 | 1139 | 334 | 1142.70 | 296.0 | 798.81 | 1.4305 | 1.4306 | −0.0001 |
| 6 | 1075 | 391 | 1112.19 | 137.0 | 797.90 | 1.3939 | 1.3939 | +0.0000 |
| 7 | 1014 | 430 | 967.24 | 63.0 | 798.84 | 1.2108 | 1.2108 | +0.0000 |

**PEAK: year 4, ratio 1.432092** (full precision, `goal_metrics`).

## BAND CHECK — REPORT ONLY

| | value |
|---|---|
| whole-cohort peak year | **4** (unmoved) |
| whole-cohort peak ratio | **1.432092** (stage 4: 1.432196) |
| band `[1.35, 1.45]` | **INSIDE — PASS** |
| distance to the 1.40 target | **+0.032092** (stage 4: +0.032196) |

**NOTHING WAS RETUNED.** The amendment moved the peak by **−0.000104** — a rounding-scale move that happens
to sit marginally closer to 1.40 than stage 4 did. No dial was chosen to achieve that and no dial would have
been changed if it had gone the other way; the instruction is to report and flag, not to retune, and there
is nothing to flag.

The reason the peak barely moves while the calibration case moves 45% is structural: the mechanism only
touches players with a **thin record AND live evidence claiming a large re-rate**, which is a small,
low-valued slice of any draft class at any as-of year, and the peak year (4) is dominated by players who long
since crossed the establishment bar. Where the mechanism lives — the deep-pick early years — it shows
clearly, and only there:

| cut | N=1 Δ | N=2 Δ | N=3 Δ | N=4 Δ | peak Δ |
|---|---|---|---|---|---|
| picks 1–20 | −0.0028 | −0.0021 | −0.0008 | +0.0005 | **+0.0005** |
| picks 21–64 | **−0.0217** | **−0.0351** | −0.0108 | −0.0012 | +0.0000 |

The deep-pick cut moves roughly **an order of magnitude more** than the top cut, in the first two years, and
converges to nothing by year 4. That is the mechanism's own signature, read off an instrument that knows
nothing about it — and it is the same signature stage 4 produced, larger.

## YR1-TO-PEAK, all cuts

| cut | peak yr | stage 4 | **amendment 1** | Δ |
|---|---|---|---|---|
| ALL picks 1–64 | 4 | 1.491034 | **1.506782** | **+0.015748** |
| picks 1–20 | 4 | 1.467663 | **1.472512** | +0.004849 |
| picks 21–64 | 6 | 1.569242 | **1.606251** | +0.037009 |

**⚠ YR1-TO-PEAK WENT UP AGAIN, away from the relocation target, and it is reported straight.** It rose for
the same reason it rose at stage 4, only more so: the change cuts year-1 thin-record values and leaves the
peak alone. It is **compensated for nowhere**. The rise is concentrated in the deep-pick cut (+0.037) and is
small in the top cut (+0.005) — the same concentration stage 4 showed.

This is the number the act's return-trigger watches. **The amendment does not resolve it and does not try
to.** The side-by-side carries it to the owner as an open ruling, unchanged in kind from stage 4.

## PER-ENTRY-YEAR N = 0..5 (mean at peak year 4 ÷ mean at year N, whole cohort)

| N | n (both) | mean yr4 | mean yrN | **ratio** | stage 4 | Δ |
|---|---|---|---|---|---|---|
| 0 | 1197 | 1149.6558 | 802.7809 | 1.432092 | 1.432196 | −0.000104 |
| **1** | 1197 | 1149.6558 | 762.9875 | **1.506782** ← the maximum | 1.491034 | +0.015748 |
| 2 | 1197 | 1149.6558 | 942.6633 | 1.219583 | 1.204437 | +0.015146 |
| 3 | 1197 | 1149.6558 | 1079.8906 | 1.064604 | 1.060997 | +0.003607 |
| 4 | 1197 | 1149.6558 | 1149.6558 | 1.000000 | 1.000000 | 0.000000 |
| 5 | 1139 | 1164.7902 | 1142.6989 | 1.019333 | 1.019347 | −0.000014 |

The cheapest buy-in remains the **end of year 1**, and it got cheaper.

**FRONT-LOADED ASSERT** (yr1→2 increment strictly exceeds yr3→4): **+0.223817 > +0.086904 → PASS**.

## TOP-END

| quantity | stage 4 | **amendment 1** |
|---|---|---|
| max active display value | 10,668 (Harry Sheezel, North Melbourne) | **10,668 — UNMOVED** |
| as a multiple of the numéraire (÷ pick 1 = 3,000) | 3.556000 | **3.556000 — UNMOVED** |
| runners-up | Nick Daicos 9,649 · Luke Jackson 8,670 · Nasiah Wanganeen-Milera 8,633 | **identical** |

The top of the board is untouched, as it must be: every one of those players crossed the establishment bar
years ago and never enters `sitout_ev`.

## THE BOARD ITSELF

| | stage 4 | **amendment 1** |
|---|---|---|
| board md5 | `b490ae8b3bbd28b908ccb923ed8412c1` | **`b56bbddea15fd48e35b5794b1b5e9e23`** |
| active rows | 804 | 804 (**same keys, no adds, no drops**) |
| board total | 654,570 | **652,183** (−2,387, **−0.3647%**) |
| rows moved | — | **45 (5.60%)** — 38 cuts, 7 lifts |
| mean abs move across movers | — | 13.02% |
| largest cut / largest lift | — | −49.32% (George Stevens) / +51.52% (Mitch Podhajski) |
| every mover on the thin-record path | — | **TRUE** |
