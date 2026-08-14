# SITTER DISCOUNT TABLE — ORDER 30A

All three lenses. **n and dispersion on every cell.** Machine-readable twin:
`SITTER_DISCOUNT_TABLE.json`. Transcript: `DERIVE30A_out.txt`. Harness: `o30a_derive.py`.

**READ-ONLY. NOTHING IS WIRED.** The old `los_decay` schedule is the DECLARED FALLBACK and remains
operative until the owner rules.

---

## 0. What is being measured

| | |
|---|---|
| **depth `N`** | `N = season_year − entry_year`, the engine's own `los()` clock. `N = 1` is a normal draftee's first season. |
| **still sitting at N** | zero games in **every** season `k = 1 … N−1`. Cells are **NESTED** — a two-year sitter is in the N=1, N=2 and N=3 cells. |
| **numerator** | the delivered-value lane's **grace-A** career score (`LAYER2.json::grace_a[key].total`, Layer 1 `ad1229ea`), **re-anchored to the start of year N** by `× disc_factor(k = N−1)` — the engine's own `disc_factor`, imported, never reimplemented. A sitter has zero delivered value before depth N, so his whole career score **is** his from-depth-N score. |
| **denominator** | `pvc_curve_v2.json::nd_v0.posv[day0_position][attributed_pick]` — the ORDER-29 **landed positional entry law** at the acquisition slot (Ruling 5; force-majeure slid pick; the two excluded keys dropped). |
| **statistic** | `r_i = V_N(i) / posv_i`; `RAW(N) = mean r_i`; **`D(N) = RAW(N) / RAW(1)`**. |
| **why normalise on N=1** | it cancels every level offset between outcome basis and price basis (different stores, different `SCALE`, numeraire `0.94009`) and leaves only the **conditional** effect of having sat. `RAW(1)` is published so the offset is visible: it is **1.0286**, i.e. the two objects already agree to within 2.9 %. |

**Pins** — layer1 `ad1229ea6f44` · LAYER2 `1eed6f94f67c` · curve `911774bc92de` · DAY0_29B `2c5c06684a73`
· rl_model `14000af2a46f` · store `cb38ef1171dc`.
**Store drift disclosed:** the delivered-value scores were built on store `d9a24282`; this branch
carries `cb38ef11`. Layer 1 is byte-identical, so the population and every sit fact are unaffected;
the N=1 normalisation absorbs any level effect. No DV number was recomputed on the new store.

---

## 1. POPULATION AND CENSORING

| | n |
|---|---:|
| ND rows attributed to mechanism `ND 1-64`, priceable on the landed entry law | **1,447** |
| **FITTED window, entry_year 2004–2021** | **1,142** |
| — of which core (≤2014) | 697 |
| — of which augmented (2015–2021) | 445 |
| SENSITIVITY tier, entry_year ≥ 2022 — **EXCLUDED from every fitted number** | 244 |
| pre-2004 — excluded (the DV lane's window floor; 2005 is where scoring data begins) | 61 |
| `posv == 0` rows dropped from ratios (the RUCK pick-63/64 floor the artifact declares) | 2 |

**Depth-cell sizes, fitted window.** The cells are nested, so N=1 is the whole class.

| depth N | n | never played a game | ever played | entry-year span | median entry year | % core (≤2014) |
|---:|---:|---:|---:|---|---:|---:|
| 1 | **1,140** | 121 | 1,019 | 2004–2021 | 2012 | 61 % |
| 2 | **462** | 121 | 341 | 2004–2021 | 2012 | 62 % |
| 3 | **234** | 121 | 113 | 2004–2021 | 2012 | 63 % |
| 4 | **154** | 121 | 33 | 2004–2021 | 2012 | 62 % |
| 5 | **130** | 121 | 9 | 2004–2021 | 2013 | 60 % |
| 6 | **117** | 113 | 4 | 2004–2020 | 2012 | 64 % |

40.5 % of top-64 national draftees played **no** senior game in their first season; 10.6 % never
played one at all.

**Censoring, stated and enforced (PREREG §2).**

- **CENSOR-1** — 2022+ classes are excluded from every fitted number. They are reported in their own
  panel and nowhere else.
- **CENSOR-2** — a row enters the depth-N cell only if seasons `k = 1 … N−1` are **completed**
  (`entry_year + N − 1 ≤ 2025`; 2026 is in progress). Under CENSOR-1 this binds only at N ≥ 6.
- **CENSOR-3** — a cell with mean tail share > 0.50 is **NOT USABLE AS EVIDENCE**: it would be the
  engine projecting the very players in question. **No fitted cell trips it** (max 0.100 at N=1,
  falling to 0.001 at N=6). **Every 2022+ panel cell at N ≤ 3 trips it.**
- **CENSOR-4** — store drift disclosed above, not laundered.
- **THE LISTING LIMIT, OWNED** — list membership is **not observable** in Layer 1 (`last_listed` is
  non-null on 3 of 1,448 ND rows). A player delisted after two gameless seasons is therefore still
  counted in the depth-3+ cells at zero delivered value. That makes the headline reading a **harsh
  (lower) bound**. The generous (upper) bound is sensitivity **S5**, which restricts each cell to
  entrants who eventually played — explicit selection on the outcome, published as a bound only, and
  it goes uninterpretable beyond depth 3 (0.44 at N=4, 2.37 at N=6). **The truth is between S5 and
  the headline, and closer to the headline at shallow depth where few rows are delisted.**

---

## 2. LENS 1 — YEARS IN THE SYSTEM (the axis). THE ALL-PICK ROW

**Primary basis: grace-A, re-anchored, fitted window. Dispersion on every cell.**

| depth | n | RAW mean | median | p25 | p75 | pooled Σ/Σ | tail share | **D(N)** | old `los_decay` non-KPP | old KPP+RUCK |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1,140 | 1.0286 | 0.1510 | 0.0007 | 1.1704 | 1.0568 | 0.100 | **1.0000** | 1.000 | 1.000 |
| 2 | 462 | 0.5846 | 0.0028 | 0.0000 | 0.3042 | 0.5763 | 0.081 | **0.5684** | 0.852 | 1.000 |
| 3 | 234 | 0.2205 | 0.0000 | 0.0000 | 0.0333 | 0.1800 | 0.044 | **0.2143** | 0.568 | 0.956 |
| 4 | 154 | 0.1082 | 0.0000 | 0.0000 | 0.0000 | 0.0611 | 0.023 | **0.1052** | 0.307 | 0.716 |
| 5 | 130 | 0.0764 | 0.0000 | 0.0000 | 0.0000 | 0.0371 | 0.008 | **0.0742** | 0.136 | 0.428 |
| 6 | 117 | 0.0931 | 0.0000 | 0.0000 | 0.0000 | 0.0445 | 0.001 | **0.0905** | 0.050 | 0.209 |

**The distribution is a spike at zero plus a long right tail.** The median is 0.15 at depth 1 and
**0.0000 at every depth ≥ 3**; p25 is ≈ 0 at every depth. A price is an expectation, so the **mean**
is the statistic — and the median is published beside it so nobody mistakes the mean for a typical
outcome.

### The recommended surface

Running-minimum monotone enforcement applied to the row above. One repair, at depth 6.

| depth | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---:|---:|---:|---:|---:|---:|
| **D_rec(N)** | **1.000** | **0.568** | **0.214** | **0.105** | **0.074** | **0.074** |
| raw D(N) | 1.000 | 0.568 | 0.214 | 0.105 | 0.074 | 0.091 |
| monotone repair | – | – | – | – | – | **YES** |

### Sensitivities — D(N) on every alternative basis

| basis | D(2) | D(3) | D(4) | D(5) | D(6) |
|---|---:|---:|---:|---:|---:|
| **PRIMARY** grace-A, re-anchored | **0.5684** | **0.2143** | **0.1052** | **0.0742** | **0.0905** |
| S1 day-0 anchored (no re-anchor) | 0.5665 | 0.2142 | 0.0923 | 0.0571 | 0.0611 |
| S2 flat-14 basis (the DV lane's operative ladder) | 0.6350 | 0.2720 | 0.1335 | 0.0942 | 0.1148 |
| S3 observed leg only, no projected tail | 0.5755 | 0.2319 | 0.1126 | 0.0839 | 0.1041 |
| S4 core window only (≤2014, near-complete careers) | 0.6233 | 0.2762 | 0.1362 | 0.1061 | 0.1237 |
| S5 EVER-PLAYED — **generous bound, selection on outcome** | 0.6883 | 0.3967 | 0.4389 | 0.9585 | 2.3662 |
| W winsor-2.0 robustness (ORDER 21's own guard) | 0.5317 | 0.2279 | 0.1165 | 0.0638 | 0.0711 |

**Every honest basis puts D(2) in 0.53–0.64, D(3) in 0.21–0.28, D(4) in 0.09–0.14.** The old
schedule sits outside all of those bands at every depth ≥ 2.

**Robustness W in full:** winsorising the per-player ratio at 2.0 bites 192 of the 1,140 depth-1 rows
and cuts `RAW(1)` by 40 % — because the tail it truncates is **real** (jordan-dawson pk 55,
thomas-stewart pk 40, errol-gulden pk 34, harris-andrews pk 59), not artefact. It is therefore **not
adopted**. What it proves is that the **normalised** D(N) moves by **< 0.04 at every depth**: the
derived surface does not depend on the right tail at all.

---

## 3. LENS 2 — DRAFT PICK. Bands, K-shrunk toward the all-pick row (K = 15)

`shrunk = (n·cell + K·allpick)/(n + K)` at the SAME depth; the **borrowing fraction `K/(n+K)`** is
printed on every cell. K = 15 is borrowed from the delivered-value lane, not invented here.

| depth | band | n | RAW mean | median | p25 | p75 | D_raw | **D_shrunk** | borrow | old (non-KPP) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1–20 | 360 | 1.0620 | 0.6143 | 0.1018 | 1.5082 | 1.033 | **1.031** | 4.0 % | 1.000 |
| 1 | 21–40 | 360 | 1.0440 | 0.1112 | 0.0009 | 1.0641 | 1.015 | **1.014** | 4.0 % | 1.000 |
| 1 | 41–64 | 420 | 0.9868 | 0.0112 | 0.0000 | 0.6413 | 0.959 | **0.961** | 3.4 % | 1.000 |
| 2 | 1–20 | 61 | 0.6944 | 0.2306 | 0.0053 | 1.0198 | 0.675 | **0.654** | 19.7 % | 0.852 |
| 2 | 21–40 | 152 | 0.4368 | 0.0077 | 0.0000 | 0.3211 | 0.425 | **0.438** | 9.0 % | 0.852 |
| 2 | 41–64 | 249 | 0.6480 | 0.0001 | 0.0000 | 0.1079 | 0.630 | **0.627** | 5.7 % | 0.852 |
| 3 | 1–20 | **20** | 0.2411 | 0.0057 | 0.0001 | 0.1519 | 0.234 | **0.226** | **42.9 %** | 0.568 |
| 3 | 21–40 | 67 | 0.1315 | 0.0000 | 0.0000 | 0.0329 | 0.128 | **0.144** | 18.3 % | 0.568 |
| 3 | 41–64 | 147 | 0.2582 | 0.0000 | 0.0000 | 0.0257 | 0.251 | **0.248** | 9.3 % | 0.568 |
| 4 | 1–20 | **4** | 0.0129 | 0.0028 | 0.0000 | 0.0157 | 0.013 | **0.086** | **78.9 %** | 0.307 |
| 4 | 21–40 | 40 | 0.0108 | 0.0000 | 0.0000 | 0.0000 | 0.011 | **0.036** | 27.3 % | 0.307 |
| 4 | 41–64 | 110 | 0.1471 | 0.0000 | 0.0000 | 0.0000 | 0.143 | **0.139** | 12.0 % | 0.307 |
| 5 | 1–20 | **3** | 0.0021 | 0.0000 | 0.0000 | 0.0032 | 0.002 | **0.062** | **83.3 %** | 0.136 |
| 5 | 21–40 | 32 | 0.0057 | 0.0000 | 0.0000 | 0.0000 | 0.006 | **0.027** | 31.9 % | 0.136 |
| 5 | 41–64 | 95 | 0.1025 | 0.0000 | 0.0000 | 0.0000 | 0.100 | **0.096** | 13.6 % | 0.136 |
| 6 | 1–20 | **2** | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.000 | **0.080** | **88.2 %** | 0.050 |
| 6 | 21–40 | 30 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.000 | **0.030** | 33.3 % | 0.050 |
| 6 | 41–64 | 85 | 0.1281 | 0.0000 | 0.0000 | 0.0000 | 0.125 | **0.120** | 15.0 % | 0.050 |

**UNUSABLE CELLS, NAMED:** `1–20` at depths **4, 5, 6** (n = 4, 3, 2; borrowing 79 %, 83 %, 88 %).
They are printed for completeness and must not be read as measurements. At depth 3 the `1–20` cell
(n = 20, borrowing 43 %) is **marginal**.

**What the lens says.** At depth 2 the ordering is **non-monotone in pick** — 0.65 (early) · 0.44
(middle) · 0.63 (late). The late-pick cell is lifted by the deep tail of the entry law (§5, Anomaly
A2): where `posv` is small, any delivery reads as a large ratio. Strip the two artefact-prone bands
and there is no clean pick effect at any depth. **The pick lens is second-order at best and is
contaminated at the late end.**

---

## 4. LENS 3 — POSITION (acquisition slot). Six groups, then the collapse

Collapse disclosed: **KPP+RUCK = {KPF, KPD, RUCK}** (the three the old schedule grants a 2.5-year
grace) vs **nonKPP = {MID, SD, SF}** (grace 1.0).

| depth | group | n | RAW mean | median | D_raw | **D_shrunk** | borrow | old `los_decay` for that group |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 2 | KPD | 56 | 0.5951 | 0.0211 | 0.579 | **0.576** | 21.1 % | 1.000 |
| 2 | KPF | 74 | 0.6848 | 0.0059 | 0.666 | **0.649** | 16.9 % | 1.000 |
| 2 | MID | 145 | 0.4957 | 0.0006 | 0.482 | **0.490** | 9.4 % | 0.852 |
| 2 | RUCK | **37** | 1.0923 | 0.2832 | 1.062 | **0.920** | 28.8 % | 1.000 |
| 2 | SD | 79 | 0.3488 | 0.0001 | 0.339 | **0.376** | 16.0 % | 0.852 |
| 2 | SF | 71 | 0.6513 | 0.0003 | 0.633 | **0.622** | 17.4 % | 0.852 |
| 2 | **KPP+RUCK** | 167 | 0.7450 | 0.0587 | 0.724 | **0.711** | 8.2 % | 1.000 |
| 2 | **nonKPP** | 295 | 0.4939 | 0.0004 | 0.480 | **0.484** | 4.8 % | 0.852 |
| 3 | KPD | 35 | 0.2331 | 0.0000 | 0.227 | **0.223** | 30.0 % | 0.956 |
| 3 | KPF | 40 | 0.1333 | 0.0000 | 0.130 | **0.153** | 27.3 % | 0.956 |
| 3 | MID | 65 | 0.1248 | 0.0000 | 0.121 | **0.139** | 18.8 % | 0.568 |
| 3 | RUCK | **19** | 0.5495 | 0.0624 | 0.534 | **0.393** | 44.1 % | 0.956 |
| 3 | SD | 41 | 0.2258 | 0.0000 | 0.220 | **0.218** | 26.8 % | 0.568 |
| 3 | SF | 34 | 0.3025 | 0.0000 | 0.294 | **0.270** | 30.6 % | 0.568 |
| 3 | **KPP+RUCK** | 94 | 0.2546 | 0.0000 | 0.248 | **0.243** | 13.8 % | 0.956 |
| 3 | **nonKPP** | 140 | 0.1975 | 0.0000 | 0.192 | **0.194** | 9.7 % | 0.568 |
| 4 | **KPP+RUCK** | 62 | 0.1841 | 0.0000 | 0.179 | **0.165** | 19.5 % | 0.716 |
| 4 | **nonKPP** | 92 | 0.0571 | 0.0000 | 0.056 | **0.063** | 14.0 % | 0.307 |
| 5 | **KPP+RUCK** | 51 | 0.1945 | 0.0000 | 0.189 | **0.163** | 22.7 % | 0.428 |
| 5 | **nonKPP** | 79 | 0.0001 | 0.0000 | 0.000 | **0.012** | 16.0 % | 0.136 |
| 6 | **KPP+RUCK** | 46 | 0.2368 | 0.0000 | 0.230 | **0.196** | 24.6 % | 0.209 |
| 6 | **nonKPP** | 71 | 0.0000 | 0.0000 | 0.000 | **0.016** | 17.4 % | 0.050 |

*(The six-way rows at depths 4–6 are in the JSON and the transcript; every one has n < 42 with
several under 12, and RUCK there is the artefact cell described below. They are not tabled here as
measurements.)*

**UNUSABLE CELLS, NAMED:** every **six-way** position cell at depth ≥ 4 (n between 7 and 41, RUCK
n = 11 / 8 / 7); **RUCK at every depth** (n = 37 / 19 / 11 / 8 / 7, and it is the cell the
denominator artefact lands on — raw RUCK reads **1.20 at depth 5 and 1.56 at depth 6**, i.e. a
six-year sitter apparently worth *more* than a fresh entrant. That is arithmetic on a ~0 denominator,
not evidence).

**What the lens says.** The **two-way collapse does carry a real, consistent signal**:

| depth | KPP+RUCK | nonKPP | gap | the old schedule's implied gap |
|---:|---:|---:|---:|---|
| 2 | 0.711 | 0.484 | **+0.23** | 1.000 vs 0.852 = +0.15 |
| 3 | 0.243 | 0.194 | **+0.05** | 0.956 vs 0.568 = +0.39 |
| 4 | 0.165 | 0.063 | **+0.10** | 0.716 vs 0.307 = +0.41 |

Big-bodied positions do hold value longer than smalls when they sit — the direction of the old
schedule's grace is **right**. Its **size is wrong by a factor of 4–8 at depths 3–4**, and the
measured gap is not even monotone in depth. **The six-way lens is noise; the two-way collapse is a
real but second-order effect that the sample supports only at depth 2.**

---

## 5. ANOMALIES

**A1 — the right tail is real, not artefact.** 192 of 1,140 depth-1 rows have `r_i > 2.0`. The top of
that list is `jordan-dawson` (MID pk 55, landed v0 253, delivered 3,768, ratio 14.9),
`jarryd-lyons` (pk 61, 13.9), `jase-burgoyne` (pk 60, 13.8), `thomas-stewart` (pk 40, 13.1),
`errol-gulden` (pk 34, 11.0), `harris-andrews` (pk 59, 8.0). These are late-pick stars. Both the
spike at zero and this tail belong in an expectation — which is exactly why the mean is the right
statistic for a price and the median is not.

**A2 — the positional entry law goes to ~0 in its own deep tail.** Landed `nd_v0.posv`:

| | pk 50 | pk 55 | pk 60 | pk 62 | pk 63 | pk 64 |
|---|---:|---:|---:|---:|---:|---:|
| KPD | 417 | 415 | 419 | 510 | 558 | 643 |
| KPF | 220 | 190 | 199 | 240 | 253 | 291 |
| MID | 355 | 253 | 163 | 127 | 94 | 57 |
| RUCK | 318 | 186 | 84 | 31 | **0** | **0** |
| SD | 94 | 106 | 176 | 236 | 269 | 312 |
| SF | 281 | 277 | 148 | 78 | 70 | **18** |

The ORDER-29 artifact declares this about itself (`nd_v0.ruck_floor_63_64`: *"THE FLOOR VALUE IS
ZERO … a thin-cell artefact of the last two picks"*). **Consequence for this act:** the RUCK position
column and the `41–64` pick band are both lifted by near-zero denominators. It is the single
clearest demonstration that the position lens carries no usable signal at depth. **It is a finding
about the denominator, and it is handed forward: any future act that reads `posv` per pick per
position inherits it.**

**A3 — the 29B reinflated count reconciles to 42, not 43.** On this act's stated clock
(`2026 − entry_year ≥ 2`, zero games in every completed season since entry), the 29B day-0 print
carries **42** year-2+ 0-game rows across its 89 wired rows — **22 ND 1-64** and **20 pool**. The
brief's figure is 43. The one-row difference is not resolved here; it is flagged rather than
smoothed over. **All 42 sit in the 2022+ sensitivity tier and contribute nothing to any fitted
number** — the players the change would price are, by construction, not in the evidence that prices
them.

---

## 6. THE 2022+ SENSITIVITY PANEL — excluded from every fitted number

| depth | n | RAW mean | tail share | usable? |
|---:|---:|---:|---:|---|
| 1 | 244 | 1.7669 | 0.878 | **NO** — CENSOR-3 |
| 2 | 82 | 1.3005 | 0.756 | **NO** — CENSOR-3 |
| 3 | 39 | 0.6982 | 0.598 | **NO** — CENSOR-3 |
| 4 | 14 | 0.0934 | 0.143 | marginal (n = 14) |

At depths 1–3 the "delivered value" of a recent class is 60–88 % **projection**, from the engine's
own band machinery, of the very players whose price is in question. Fitting on it would be circular.
Note the shape it would have implied had it been used: **1.30 / 0.70 relative to a 1.77 baseline =
0.74 / 0.40** — materially more generous than the fitted answer, which is precisely the direction
projection bias runs.

---

## 7. METHOD SYMMETRY — the ND surface built the pool's way

The pool's ψ machinery (ORDER 21/24B) builds its depth object as
`R(cls,d) = E[winsor(O/entry_anchor, 2)  |  sit-out] ÷ norm(cls,d)`, where
`norm(cls,d) = E[winsor(O/entry_anchor, 2)]` over **all** cells at that depth — a same-depth norm
that strips survivor selection. This act's headline normalises on the **depth-1 baseline** instead.
Both are computed here, on ND, so the difference is a number and not an argument. The
pool-symmetric leg uses the **observed leg only** on the **live store**, applied identically to
numerator and denominator, so the store cancels inside the ratio.

| depth | n sitters | n all | E[sit] | norm | **Rₙ(N)** pool-construction | **D(N)** this act | old `los_decay` non-KPP |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 695 | 695 | 0.6057 | 0.6057 | **1.0000** | 1.0000 | 1.000 |
| 2 | 286 | 695 | 0.3723 | 0.6309 | **0.5900** | 0.5684 | 0.852 |
| 3 | 148 | 695 | 0.1858 | 0.6445 | **0.2883** | 0.2143 | 0.568 |
| 4 | 95 | 695 | 0.0951 | 0.6412 | **0.1483** | 0.1052 | 0.307 |
| 5 | 78 | 695 | 0.0564 | 0.6091 | **0.0926** | 0.0742 | 0.136 |
| 6 | 75 | 695 | 0.0571 | 0.5722 | **0.0999** | 0.0905 | 0.050 |

**The two constructions agree to within 0.075 at every depth**, and the pool's is the slightly more
generous of the two (its same-depth norm rises with depth — deep survivors are increasingly the
developers — so dividing by it lifts the sitter). **Both are far harsher than the old ND schedule at
every depth.**

And the pool's own landed surface, for the side-by-side (ORDER 21 `whole_pool`; **its `d` = one
completed sit-out season, so pool `d` maps to this act's `N = d + 1`**):

| pool class | d1 (≙ N2) | d2 (≙ N3) | d3 (≙ N4) | d4 (≙ N5) | d5 (≙ N6) | d6 |
|---|---:|---:|---:|---:|---:|---:|
| nonKPP | 0.624 | 0.380 | 0.380 | 0.380 | 0.380 | 0.380 |
| KPP | 0.817 | 0.500 | 0.467 | 0.359 | 0.359 | 0.336 |
| RUCK | 1.000 | 0.522 | 0.522 | 0.488 | 0.354 | 0.344 |
| **ND, derived here** | **0.568** | **0.214** | **0.105** | **0.074** | **0.074** | – |

Same machinery, **pathway-specific values** — which is the owner's one-machinery law working as
intended. The ND pathway decays **faster** than the pool: an ND sitter is a player a club paid a
first-64 pick for and still would not play, whereas a pool sitter was cheap to begin with and the
same silence carries less information. The two shapes are the same object; the numbers are the
pathway's own.

---

## 8. WHICH LENS CARRIES SIGNAL

| lens | verdict |
|---|---|
| **years in the system** | **REAL, AND IT CARRIES ESSENTIALLY ALL OF IT.** n = 462 / 234 / 154 at depths 2 / 3 / 4; the ordering is monotone on the raw row through depth 5; every alternative basis reproduces it within ±0.06; and the pool-symmetric construction reproduces it within 0.075. |
| **draft pick** | **NOT USABLE AS FILED.** Non-monotone at depth 2, the early-pick cells collapse to n = 4 / 3 / 2 at depths 4–6 (borrowing 79–88 %), and the late-pick band is contaminated by Anomaly A2. Published with its n and its borrowing; not recommended for wiring. |
| **position** | **SIX-WAY: NO SIGNAL.** RUCK, the cell the old schedule's grace is really about, has n = 37 / 19 / 11 / 8 / 7 and sits on the artefact denominator. **TWO-WAY COLLAPSE: a real second-order effect** — KPP+RUCK holds value longer than nonKPP at depths 2, 3 and 4 — but the measured gap (+0.23 / +0.05 / +0.10) is **not monotone** and is **4–8× smaller than the old 2.5-year grace implies**. Supportable at depth 2 only. |

---

*Generated by `o30a_derive.py`. Read-only. Nothing wires until the owner rules.*
