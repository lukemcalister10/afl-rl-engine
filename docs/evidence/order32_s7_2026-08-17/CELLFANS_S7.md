# ORDER 32 S7 — THE PEDIGREE-LEG CELL FANS (owner tables)

READ-ONLY measurement. PREREG_S7.md was pushed before any number below was computed. Full
machine output: `CELLFANS_S7.json`; full transcript: `CELLFANS_S7_out.txt`; instrument:
`s7_cellfans.py`.

**What this is.** The pedigree leg v0 is a cell MEAN with no distribution attached. These are the
empirical outcome fans of the very cells the v0 is fitted on — realized career delivered value
(grace-A total, #338 minimum-tenure basis), the fit's own target variable, on the fit's own rows.

**Controls, both REPRODUCED:** ND population = the fit population exactly (1142 rows,
KPD 125 / KPF 143 / MID 422 / RUCK 60 / SD 180 / SF 212); pool population = the pool fit
population exactly (840 fitted of 1080; o30a2 prefix md5 `fe6f436a...` = the POOL31F pin).

**How to read:** six levels q10/q30/q50/q70/q90/q97 — the production fan's own levels
(`b6`/`price6`, weights WQ6 = [.18 ×5, .10]). `*` = BOUND(max): the level does not resolve at
this n; the sample max is shown as a bound, never smoothed. `n0` = careers delivering ~zero.
Cells with n < 8 publish no fan (min/median/max only).

## THE HEADLINE FINDING — the skew IS the lottery structure

Mean/median of the ALL row, by pick band:

| band | 1-10 | 11-20 | 21-30 | 31-40 | 41-64 |
|---|---|---|---|---|---|
| mean/median | 1.67 | 2.47 | 9.34 | 17.5 | **153.6** |
| zero-share | 0% | 1% | 6% | 12% | **21%** |

Mean > median in **33 of 33** resolved ND cells. Late picks are exactly the shape the owner
intuits: band 41-64 ALL has **median 1.9 against mean 287.2** — half of these careers deliver
essentially nothing — while q90 = 953 and q97 = 2301. The v0 mean is real, but it is made of a
zero-spike plus a long right tail, not of typical outcomes. A variance display that scales with
the production leg only would show these cells as LOW variance; they are the highest-variance
cells on the board relative to their price.

**Mean vs fitted v0 (the §6 statement):** the raw cell mean tracks the fitted comparator closely
on the ND lane — mean/v0 = 1.05 / 1.09 / 1.09 / 1.02 / 1.03 across the five bands (the fitted
surface is a smoothed, conserved transform of these very means). So the fitted v0 sits near the
q70 of its own cell in the late bands: the pedigree price of a late pick is paid for by the tail,
not the median.

## ND LANE — pick band × position

Value = realized career delivered value (grace-A total). `*` = BOUND(max).

### Band 1-10  (ALL: n=180, v0 comparator 1895, mean/v0 1.051)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 180 | 0 | 19.7 | 374.6 | 1190.7 | 2652.9 | 5114.9 | 7281.6 | 1992.5 | 1.7 |
| KPD | 19 | 0 | 5.9 | 225.6 | 397.3 | 1247.7 | 3359.9 | 3817.6* | 1112.5 | 2.8 |
| KPF | 31 | 0 | 27.8 | 340.8 | 1003.8 | 1611.7 | 3429.6 | 6491.7* | 1405.6 | 1.4 |
| MID | 96 | 0 | 23.2 | 570.2 | 1931.1 | 3543.3 | 5742.3 | 8098.7 | 2512.2 | 1.3 |
| RUCK | 7 | 0 | — | — | med 1941.7 | — | — | max 8447.8 | UNRESOLVED (n<8) | — |
| SD | 12 | 0 | 147.8 | 346.8 | 666.6 | 1620.7 | 3389.1 | 3986.7* | 1287.4 | 1.9 |
| SF | 15 | 0 | 98.3 | 367.2 | 684.5 | 1345.5 | 3415.4 | 3950.8* | 1254.1 | 1.8 |

### Band 11-20  (ALL: n=180, v0 comparator 964, mean/v0 1.093)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 180 | 2 | 1.8 | 83.1 | 425.9 | 1177.8 | 2875.2 | 5113.6 | 1054.0 | 2.5 |
| KPD | 17 | 0 | 66.7 | 230.5 | 468.7 | 742.2 | 2021.6 | 2895.6* | 755.1 | 1.6 |
| KPF | 24 | 1 | 3.4 | 85.0 | 215.9 | 938.2 | 2553.5 | 3406.0* | 786.1 | 3.6 |
| MID | 65 | 1 | 0.2 | 52.5 | 477.7 | 1476.2 | 4250.3 | 5784.6 | 1374.3 | 2.9 |
| RUCK | 8 | 0 | 3.4 | 52.4 | 135.3 | 285.9 | 4951.8* | 4951.8* | 807.1 | 6.0 |
| SD | 33 | 0 | 1.5 | 189.3 | 623.9 | 1301.0 | 2804.2 | 8298.3* | 1140.8 | 1.8 |
| SF | 33 | 0 | 1.9 | 32.9 | 366.1 | 1003.8 | 2016.3 | 3869.1* | 745.2 | 2.0 |

### Band 21-30  (ALL: n=180, v0 comparator 677, mean/v0 1.091)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 180 | 10 | 0.0 | 4.7 | 79.1 | 596.7 | 2771.1 | 4194.3 | 739.2 | 9.3 |
| KPD | 21 | 3 | 0.0 | 0.2 | 23.0 | 318.7 | 997.0 | 3036.9* | 405.5 | 17.6 |
| KPF | 17 | 1 | 0.1 | 1.9 | 359.0 | 607.5 | 2840.6 | 3588.1* | 880.0 | 2.5 |
| MID | 77 | 2 | 0.0 | 13.0 | 122.9 | 708.6 | 3109.6 | 5301.2 | 961.2 | 7.8 |
| RUCK | 5 | 0 | — | — | med 1455.5 | — | — | max 6991.7 | UNRESOLVED (n<8) | — |
| SD | 23 | 2 | 0.0 | 0.0 | 48.2 | 461.1 | 1936.0 | 3229.7* | 596.7 | 12.4 |
| SF | 37 | 2 | 0.0 | 6.5 | 26.6 | 277.6 | 816.6 | 1316.4 | 285.7 | 10.7 |

### Band 31-40  (ALL: n=180, v0 comparator 539, mean/v0 1.015)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 180 | 21 | 0.0 | 1.2 | 31.3 | 306.7 | 1822.9 | 3226.4 | 547.5 | 17.5 |
| KPD | 22 | 4 | 0.0 | 4.5 | 116.4 | 228.5 | 952.3 | 2367.8* | 345.3 | 3.0 |
| KPF | 23 | 5 | 0.0 | 0.2 | 3.0 | 317.7 | 1599.4 | 2168.0* | 418.8 | 140.9 |
| MID | 60 | 6 | 0.0 | 0.2 | 15.3 | 298.9 | 1794.8 | 4438.0 | 583.3 | 38.2 |
| RUCK | 14 | 0 | 29.7 | 418.0 | 952.2 | 2156.9 | 4332.8 | 6134.8* | 1695.5 | 1.8 |
| SD | 28 | 5 | 0.0 | 0.2 | 7.9 | 39.7 | 832.3 | 3149.8* | 294.4 | 37.1 |
| SF | 33 | 1 | 0.2 | 1.8 | 55.0 | 427.2 | 1379.6 | 2294.8* | 434.5 | 7.9 |

### Band 41-64  (ALL: n=422, v0 comparator 279, mean/v0 1.029)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| ALL | 422 | 88 | 0.0 | 0.0 | 1.9 | 80.3 | 953.3 | 2301.1 | 287.2 | 153.6 |
| KPD | 46 | 8 | 0.0 | 7.7 | 83.7 | 305.3 | 1477.2 | 2897.9 | 442.8 | 5.3 |
| KPF | 48 | 18 | 0.0 | 0.0 | 0.1 | 180.2 | 802.0 | 1394.7 | 227.4 | 1615.9 |
| MID | 124 | 24 | 0.0 | 0.0 | 0.7 | 56.5 | 1373.1 | 3517.6 | 389.1 | 551.9 |
| RUCK | 26 | 3 | 0.0 | 5.4 | 50.8 | 362.4 | 991.1 | 1877.1* | 311.2 | 6.1 |
| SD | 84 | 16 | 0.0 | 0.0 | 0.3 | 17.1 | 202.5 | 1157.4 | 129.5 | 481.9 |
| SF | 94 | 19 | 0.0 | 0.0 | 1.4 | 42.6 | 690.3 | 2041.4 | 241.6 | 171.1 |

Position texture worth the owner's eye: **RUCK inverts the pattern** — thin early (n<8 twice)
but at 31-40 it is the strongest cell on the row (median 952, mean 1696, zero-share 0%), and at
41-64 RUCK/KPD keep a real median while KPF/MID/SD/SF medians are ~0. The lottery shape is
sharpest for small forwards/defenders and late KPFs.

## ND FINER CUT — position-pooled 5-pick bands (supported: every cell n ≥ 34)

| band | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean | mean/med |
|---|---|---|---|---|---|---|---|---|---|---|
| 1-5 | 90 | 0 | 193.3 | 861.6 | 2249.6 | 3789.8 | 5515.7 | 8448.7 | 2710.4 | 1.2 |
| 6-10 | 90 | 0 | 7.3 | 147.1 | 611.7 | 1445.4 | 3307.8 | 6105.8 | 1274.6 | 2.1 |
| 11-15 | 90 | 1 | 1.8 | 66.8 | 534.7 | 1457.9 | 2896.7 | 5580.1 | 1202.2 | 2.2 |
| 16-20 | 90 | 1 | 2.6 | 83.7 | 335.0 | 948.3 | 2864.4 | 4025.9 | 905.9 | 2.7 |
| 21-25 | 90 | 5 | 0.0 | 7.9 | 39.8 | 587.0 | 2793.2 | 5772.7 | 811.5 | 20.4 |
| 26-30 | 90 | 5 | 0.0 | 1.1 | 186.4 | 664.1 | 2429.6 | 3264.1 | 667.0 | 3.6 |
| 31-35 | 90 | 12 | 0.0 | 0.7 | 65.3 | 437.2 | 1822.9 | 2666.0 | 579.6 | 8.9 |
| 36-40 | 90 | 9 | 0.0 | 1.3 | 18.7 | 201.0 | 1813.3 | 3494.8 | 515.3 | 27.6 |
| 41-45 | 90 | 14 | 0.0 | 0.1 | 29.5 | 172.8 | 1706.7 | 3708.7 | 500.6 | 17.0 |
| 46-50 | 90 | 21 | 0.0 | 0.0 | 3.5 | 68.0 | 616.0 | 1356.0 | 207.4 | 59.6 |
| 51-55 | 90 | 17 | 0.0 | 0.0 | 6.8 | 112.2 | 966.9 | 3207.5 | 343.9 | 50.5 |
| 56-60 | 90 | 20 | 0.0 | 0.0 | 1.2 | 27.2 | 613.7 | 1631.7 | 194.0 | 165.6 |
| 61-64 | 62 | 16 | 0.0 | 0.0 | 0.0 | 4.5 | 260.4 | 1624.2 | 146.3 | 13163.2 |

The q97 column is remarkably FLAT from pick 21 out (~1.4k-3.7k, no trend to speak of) while the
median collapses 2250 → 0. That is the measured content of "lottery ticket": what a later pick
loses is the middle of its distribution, not its ceiling.

## POOL LANE — per arm (position-pooled, fitted window 2004-2021)

| arm | n | n0 (zero-share) | q10 | q30 | q50 | q70 | q90 | q97 | mean | v0 comparator | mean/v0 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RD | 611 | 261 (43%) | 0.0 | 0.0 | 0.0 | 24.0 | 824.6 | 2086.0 | 245.7 | 232.9 | 1.055 |
| SSP | 24 | 7 (29%) | 0.0 | 0.0 | 2.1 | 108.4 | 275.7 | 3797.5* | 231.4 | 198.1 | 1.168 |
| MSD | 29 | 11 (38%) | 0.0 | 0.0 | 0.0 | 119.7 | 1527.7 | 3992.5* | 422.3 | 363.4 | 1.162 |
| UNR | 46 | 26 (57%) | 0.0 | 0.0 | 0.0 | 0.2 | 162.4 | 1078.8 | 101.7 | 111.8 | 0.909 |
| IRE | 47 | 26 (55%) | 0.0 | 0.0 | 0.0 | 0.3 | 83.6 | 442.3 | 60.0 | 82.1 | 0.731 |
| PDA | 38 | 15 (39%) | 0.0 | 0.0 | 0.0 | 1.1 | 173.4 | 1543.1 | 189.0 | 185.3 | 1.020 |
| PDN | 24 | 13 (54%) | 0.0 | 0.0 | 0.0 | 1.0 | 222.6 | 511.7* | 49.7 | 84.7 | 0.587 |
| PDS | 21 | 14 (67%) | 0.0 | 0.0 | 0.0 | 0.0 | 1.8 | 323.7* | 21.6 | 81.0 | 0.266 |

Every pool arm's MEDIAN career is zero or ~zero. The rookie-draft arm (the only well-supported
one, n=611) delivers nothing through q50, then 825 at q90 and 2086 at q97 — a purer lottery
shape than any ND band. Note the mean/v0 column: RD/PDA/UNR sit near 1, but PDS (0.27),
PDN (0.59) and IRE (0.73) have raw arm means well below the mean of their signed v0 cells. That
is expected mechanically — the pool v0 cells are per arm × position, K-shrunk toward the pooled
pool row, so a thin arm's signed cells borrow level from the pool — but it means the thin arms'
displayed v0 leans on borrowed level, and their fans below are bounds. Reported, not adjusted.

### Pool arm × position (only cells with n ≥ 20; a split of a thin arm)

| cell | n | n0 | q10 | q30 | q50 | q70 | q90 | q97 | mean |
|---|---|---|---|---|---|---|---|---|---|
| RD KPD | 83 | 39 | 0.0 | 0.0 | 0.0 | 40.9 | 562.1 | 1681.9 | 220.2 |
| RD KPF | 61 | 29 | 0.0 | 0.0 | 0.0 | 39.1 | 403.7 | 1248.6 | 203.8 |
| RD MID | 180 | 81 | 0.0 | 0.0 | 0.0 | 11.6 | 515.3 | 2031.5 | 221.2 |
| RD RUCK | 58 | 27 | 0.0 | 0.0 | 0.0 | 230.1 | 1184.6 | 2634.4 | 407.7 |
| RD SD | 108 | 33 | 0.0 | 0.0 | 0.4 | 139.0 | 937.9 | 1890.4 | 273.2 |
| RD SF | 121 | 52 | 0.0 | 0.0 | 0.0 | 8.7 | 880.7 | 1894.6 | 218.7 |
| UNR RUCK | 26 | 22 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 419.3* | 24.6 |
| IRE SD | 29 | 16 | 0.0 | 0.0 | 0.0 | 1.9 | 155.1 | 1604.6* | 86.6 |

## LIMITATIONS, STATED

1. These are fans of the FIT TARGET (raw grace-A career totals), the same rows the v0 means are
   fitted on. The fitted v0 additionally passes through local-linear estimation, K-shrink, PAVA
   and one conservation scalar; per-cell mean/v0 is printed so the gap is visible (≤ 9% on every
   ND band ALL row; larger and disclosed on thin pool arms).
2. Right-censoring: recent entrants' careers are incomplete; the grace-A total already carries
   the DV lane's tail projection (`tail_share` machinery), and the fitted window 2004-2021 is the
   fits' own. Nothing extra was done here — same exposure as the fits themselves.
3. Thin cells are bounds. Every `*` is a BOUND(max), and n<8 cells publish no fan at all
   (ND: RUCK 1-10 n=7, RUCK 21-30 n=5). Nothing was smoothed or borrowed to fill them.
4. Store drift disclosures of the o30a2 prefix are inherited unchanged (Layer 1 byte-identical).
