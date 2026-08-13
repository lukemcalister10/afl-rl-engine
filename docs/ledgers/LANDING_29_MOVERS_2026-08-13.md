# LANDING 29 — THE COMPOSED MOVERS LEDGER

**2026-08-13 · branch `land/order-29` · ORDER 29, the landing build.**

> ## THIS LEDGER IS PARTIAL, AND SAYS SO IN ITS FIRST LINE.
> The landing **STOPPED at Step 3**: the ruled curve halts the engine on G-MONO strict descent
> (`STOP_STEP3_GMONO.md`). Two of the four levers were built and are measured here in full, every
> player, exactly. The other two — the v0/curve re-print and the numéraire scalar — were **never
> built**, so they are **absent, not estimated**. No row below carries a modelled or inferred
> component; every number is a difference of two boards that exist on disk.

## THE STAGES

| stage | what it is | `rl_app_data.json` md5 |
|---|---|---|
| **LIVE** | the frozen live board | `88ce647f531030d8d2e094188b258191` |
| **B_U** | + the unflag-three (store `cb38ef11`), dial OFF | `71cbb13b3414d031135771dd7e564b3c` |
| **B_G** | + the grace dial ON (the last board this build can produce) | `0017657e0469addda9260964938bad78` |
| ~~B_V~~ | + the curve / v0 re-print | **BLOCKED — never built** |
| ~~B_F~~ | + the numéraire re-pin (the intended FINAL board) | **BLOCKED — never built** |

Each lever is the difference of **consecutive** stages, so the lever columns sum to the total
**by construction**. The reconciliation assert below is therefore a check on the arithmetic and
the row alignment, not a fudge factor: it must be exactly zero for every row.

## 1. BOARD TOTALS

| stage | board total | Δ vs previous | Δ vs LIVE |
|---|---|---|---|
| LIVE | 752,429 | — | — |
| B_U | 743,734 | -8695 (-1.1556%) | -8695 (-1.1556%) |
| B_G | 748,405 | +4671 (+0.6280%) | -4024 (-0.5348%) |

### the national / pool split

| population | n | LIVE | B_U | B_G | Δ vs LIVE |
|---|---|---|---|---|---|
| national (ND 1–64) | 561 | 620,877 | 613,631 | 618,074 | -2803 (-0.4515%) |
| pool (everything past 64) | 243 | 131,552 | 130,103 | 130,331 | -1221 (-0.9282%) |

## 2. THE MOVER COUNT, PER LEVER

| lever | movers | up | down | Σ Δ | what it is |
|---|---|---|---|---|---|
| lever 1 — THE UNFLAG-THREE | **543** | 6 | 537 | -8695 | store d9a24282 -> cb38ef11; reaches every priced row through the v3.4 kernel head (3917 -> 3966) and hence BOARD_FACTOR (0.761344 -> 0.751937, -1.2355%) |
| lever 2 — THE GRACE DIAL | **39** | 38 | 1 | +4671 | RL_GRACE code default '0' -> '1'; entry age <= 19 carries seasons 1 and 2 at full weight |
| **TOTAL (LIVE → B_G)** | **543 of 804** | 42 | 501 | -4024 | the two landed levers composed |

## 3. THE RECONCILIATION — EXACT, EVERY ROW

For every one of the 804 priced rows:

```
  (lever 1) + (lever 2)  ==  total(LIVE -> B_G)
  rows failing to reconcile : 0
  max |residual|           : 0
```

**PASS** — the levers sum to the total exactly, with no unexplained remainder.

## 4. DISPERSION (never a bare mean)

| lever | min | p05 | median | mean | p95 | max |
|---|---|---|---|---|---|---|
| lever 1 — THE UNFLAG-THREE (relative) | -4.76% | -1.64% | **-1.23%** | -1.20% | -0.56% | +0.45% |
| lever 1 — THE UNFLAG-THREE (absolute) | -146 | -53 | **-9** | -16.0 | -1 | +1 |
| lever 2 — THE GRACE DIAL (relative) | -0.41% | +0.84% | **+8.72%** | +8.78% | +13.91% | +14.02% |
| lever 2 — THE GRACE DIAL (absolute) | -2 | +1 | **+42** | +119.8 | +403 | +538 |

## 5. THE NAMED ROWS (PREREG P14)

P14 names ten rows to be reported live → landed with their per-lever split. They are reported
here **live → B_G**, which is as far as the landing got. Two of the four levers never ran, so
P14 cannot be scored as written — see the packet.

| row | pos | pick | entry age | grace | LIVE | lever 1 | lever 2 | B_G | Δ vs LIVE |
|---|---|---|---|---|---|---|---|---|---|
| **harrison-ramm** | KPD | 3 | 19 | 0 | 545 | -4 | +0 | 541 | -4 (-0.73%) |
| **luker-kentfield** | KPF | 11 | 19 | 0 | 419 | -2 | +0 | 417 | -2 (-0.48%) |
| **mani-liddy** | MID | 15 | 23 | 0 | 152 | +0 | +0 | 152 | +0 (+0.00%) |
| **robert-hansen** | SF | 2 | 19 | 0 | 132 | +0 | +0 | 132 | +0 (+0.00%) |
| **dante-visentini** | RUCK | 56 | 18 | 0 | 1274 | -16 | +0 | 1258 | -16 (-1.26%) |
| **vigo-visentini** | RUCK | 5 | 18 | 0 | 182 | +0 | +0 | 182 | +0 (+0.00%) |
| **nicholas-martin** | MID | pool | 20 | 0 | 3513 | -44 | +0 | 3469 | -44 (-1.25%) |
| **marcus-herbert** | SD | 13 | 24 | 0 | 906 | -12 | +0 | 894 | -12 (-1.32%) |
| **jai-newcombe** | MID | 2 | 20 | 0 | 4883 | -61 | +0 | 4822 | -61 (-1.25%) |
| **willem-duursma** | MID | 1 | 18 | 1 | 3977 | -50 | +538 | 4465 | +488 (+12.27%) |
| **harry-sheezel** | MID | 3 | 18 | 0 | 11764 | -146 | +0 | 11618 | -146 (-1.24%) |

## 6. THE LARGEST MOVERS, LIVE → B_G

| # | key | pos | pick | entry age | grace | LIVE | lever 1 | lever 2 | B_G | Δ | Δ pct |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | willem-duursma | MID | 1 | 18 | 1 | 3977 | -50 | +538 | 4465 | **+488** | +12.27% |
| 2 | dyson-sharp | MID | 13 | 18 | 1 | 3091 | -38 | +403 | 3456 | **+365** | +11.81% |
| 3 | sullivan-robey | MID | 9 | 18 | 1 | 2981 | -37 | +395 | 3339 | **+358** | +12.01% |
| 4 | jacob-farrow | SD | 10 | 18 | 1 | 2601 | -33 | +356 | 2924 | **+323** | +12.42% |
| 5 | harry-dean | KPD | 3 | 18 | 1 | 2577 | -32 | +354 | 2899 | **+322** | +12.50% |
| 6 | josh-lindsay | SD | 19 | 18 | 1 | 2335 | -29 | +316 | 2622 | **+287** | +12.29% |
| 7 | sam-cumming | MID | 7 | 18 | 1 | 2288 | -28 | +312 | 2572 | **+284** | +12.41% |
| 8 | samuel-grlj | MID | 8 | 18 | 1 | 1735 | -22 | +237 | 1950 | **+215** | +12.39% |
| 9 | cooper-duff-tytler | KPF | 4 | 18 | 1 | 1561 | -20 | +216 | 1757 | **+196** | +12.56% |
| 10 | beau-addinsall | MID | 18 | 18 | 1 | 1521 | -19 | +208 | 1710 | **+189** | +12.43% |
| 11 | harry-sheezel | MID | 3 | 18 | 0 | 11764 | -146 | +0 | 11618 | **-146** | -1.24% |
| 12 | dylan-patterson | SD | 5 | 18 | 1 | 1628 | -19 | +162 | 1771 | **+143** | +8.78% |
| 13 | nick-daicos | MID | 4 | 18 | 0 | 10945 | -136 | +0 | 10809 | **-136** | -1.24% |
| 14 | luke-jackson | RUCK | 3 | 18 | 0 | 10203 | -125 | +0 | 10078 | **-125** | -1.23% |
| 15 | nasiah-wanganeen-milera | MID | 11 | 18 | 0 | 9688 | -119 | +0 | 9569 | **-119** | -1.23% |
| 16 | talor-byrne | SF | 45 | 18 | 1 | 857 | -10 | +117 | 964 | **+107** | +12.49% |
| 17 | max-holmes | MID | 21 | 18 | 0 | 8406 | -103 | +0 | 8303 | **-103** | -1.23% |
| 18 | samuel-swadling | MID | 37 | 18 | 1 | 776 | -9 | +106 | 873 | **+97** | +12.50% |
| 19 | tristan-xerri | RUCK | 71 | 18 | 0 | 7800 | -97 | +0 | 7703 | **-97** | -1.24% |
| 20 | errol-gulden | MID | 34 | 18 | 0 | 7239 | -91 | +0 | 7148 | **-91** | -1.26% |
| 21 | will-ashcroft | MID | 2 | 18 | 0 | 7330 | -90 | +0 | 7240 | **-90** | -1.23% |
| 22 | louis-emmett | KPF | 27 | 18 | 1 | 749 | -10 | +99 | 838 | **+89** | +11.88% |
| 23 | zak-butters | MID | 12 | 18 | 0 | 7092 | -87 | +0 | 7005 | **-87** | -1.23% |
| 24 | josh-treacy | KPF | 4 | 18 | 0 | 6921 | -85 | +0 | 6836 | **-85** | -1.23% |
| 25 | jai-murray | MID | 17 | 18 | 1 | 1138 | -14 | +98 | 1222 | **+84** | +7.38% |

## 7. THE CONTROL GROUP — WHO THE GRACE DIAL MUST NOT REACH

Rows debuting 2026 at entry age >= 20 — the ruled discrimination (20+ gets no grace):

```
  rows in the control group          : 30
  moved by lever 2 (the grace dial)  : 0
```

**PASS** — the dial's own leg moves them by exactly zero, which is the ruling visible in the data
rather than asserted in a sentence. (They still move under lever 1, which is a board-wide scalar
and reaches every priced row by construction.)

## 8. EVERY PLAYER

All 804 priced rows, per-lever. Rows are ordered by |Δ vs LIVE| descending.

| key | pos | pick | LIVE | lever 1 (unflag) | lever 2 (grace) | B_G | Δ | Δ pct |
|---|---|---|---|---|---|---|---|---|
| willem-duursma | MID | 1 | 3977 | -50 | +538 | 4465 | +488 | +12.27% |
| dyson-sharp | MID | 13 | 3091 | -38 | +403 | 3456 | +365 | +11.81% |
| sullivan-robey | MID | 9 | 2981 | -37 | +395 | 3339 | +358 | +12.01% |
| jacob-farrow | SD | 10 | 2601 | -33 | +356 | 2924 | +323 | +12.42% |
| harry-dean | KPD | 3 | 2577 | -32 | +354 | 2899 | +322 | +12.50% |
| josh-lindsay | SD | 19 | 2335 | -29 | +316 | 2622 | +287 | +12.29% |
| sam-cumming | MID | 7 | 2288 | -28 | +312 | 2572 | +284 | +12.41% |
| samuel-grlj | MID | 8 | 1735 | -22 | +237 | 1950 | +215 | +12.39% |
| cooper-duff-tytler | KPF | 4 | 1561 | -20 | +216 | 1757 | +196 | +12.56% |
| beau-addinsall | MID | 18 | 1521 | -19 | +208 | 1710 | +189 | +12.43% |
| harry-sheezel | MID | 3 | 11764 | -146 | +0 | 11618 | -146 | -1.24% |
| dylan-patterson | SD | 5 | 1628 | -19 | +162 | 1771 | +143 | +8.78% |
| nick-daicos | MID | 4 | 10945 | -136 | +0 | 10809 | -136 | -1.24% |
| luke-jackson | RUCK | 3 | 10203 | -125 | +0 | 10078 | -125 | -1.23% |
| nasiah-wanganeen-milera | MID | 11 | 9688 | -119 | +0 | 9569 | -119 | -1.23% |
| talor-byrne | SF | 45 | 857 | -10 | +117 | 964 | +107 | +12.49% |
| max-holmes | MID | 21 | 8406 | -103 | +0 | 8303 | -103 | -1.23% |
| samuel-swadling | MID | 37 | 776 | -9 | +106 | 873 | +97 | +12.50% |
| tristan-xerri | RUCK | 71 | 7800 | -97 | +0 | 7703 | -97 | -1.24% |
| errol-gulden | MID | 34 | 7239 | -91 | +0 | 7148 | -91 | -1.26% |
| will-ashcroft | MID | 2 | 7330 | -90 | +0 | 7240 | -90 | -1.23% |
| louis-emmett | KPF | 27 | 749 | -10 | +99 | 838 | +89 | +11.88% |
| zak-butters | MID | 12 | 7092 | -87 | +0 | 7005 | -87 | -1.23% |
| josh-treacy | KPF | 4 | 6921 | -85 | +0 | 6836 | -85 | -1.23% |
| jai-murray | MID | 17 | 1138 | -14 | +98 | 1222 | +84 | +7.38% |
| bailey-smith | MID | 7 | 6683 | -83 | +0 | 6600 | -83 | -1.24% |
| harry-kyle | SD | 14 | 1158 | -14 | +93 | 1237 | +79 | +6.82% |
| finn-callaghan | MID | 3 | 6062 | -75 | +0 | 5987 | -75 | -1.24% |
| jason-horne-francis | MID | 1 | 6042 | -74 | +0 | 5968 | -74 | -1.22% |
| lachlan-ash | SD | 4 | 5728 | -71 | +0 | 5657 | -71 | -1.24% |
| sam-darcy | KPF | 2 | 5250 | -66 | +0 | 5184 | -66 | -1.26% |
| noah-anderson | MID | 2 | 5256 | -65 | +0 | 5191 | -65 | -1.24% |
| jack-ison | SF | 47 | 512 | -6 | +70 | 576 | +64 | +12.50% |
| caleb-serong | MID | 8 | 5027 | -62 | +0 | 4965 | -62 | -1.23% |
| jagga-smith | MID | 3 | 4855 | -61 | +0 | 4794 | -61 | -1.26% |
| jai-newcombe | MID | 2 | 4883 | -61 | +0 | 4822 | -61 | -1.25% |
| matt-rowell | MID | 1 | 4770 | -59 | +0 | 4711 | -59 | -1.24% |
| tom-green | MID | 10 | 4719 | -59 | +0 | 4660 | -59 | -1.25% |
| archie-roberts | SD | 54 | 4726 | -58 | +0 | 4668 | -58 | -1.23% |
| izak-rankine | SF | 3 | 4685 | -58 | +0 | 4627 | -58 | -1.24% |
| brodie-grundy | RUCK | 22 | 4490 | -55 | +0 | 4435 | -55 | -1.22% |
| chad-warner | MID | 38 | 4411 | -55 | +0 | 4356 | -55 | -1.25% |
| riley-thilthorpe | KPF | 2 | 4468 | -55 | +0 | 4413 | -55 | -1.23% |
| jake-bowey | SD | 22 | 4319 | -54 | +0 | 4265 | -54 | -1.25% |
| colby-mckercher | MID | 2 | 4285 | -53 | +0 | 4232 | -53 | -1.24% |
| kysaiah-pickett | SF | 12 | 4249 | -53 | +0 | 4196 | -53 | -1.25% |
| nick-blakey | SD | 10 | 4273 | -53 | +0 | 4220 | -53 | -1.24% |
| bodhi-uwland | SD | pool | 4087 | -51 | +0 | 4036 | -51 | -1.25% |
| luke-davies-uniacke | MID | 4 | 4070 | -51 | +0 | 4019 | -51 | -1.25% |
| mac-andrew | KPD | 5 | 4169 | -51 | +0 | 4118 | -51 | -1.22% |
| sam-lalor | MID | 1 | 4087 | -51 | +0 | 4036 | -51 | -1.25% |
| lachy-dovaston | SF | 16 | 512 | -6 | +56 | 562 | +50 | +9.77% |
| murphy-reid | SF | 17 | 4141 | -50 | +0 | 4091 | -50 | -1.21% |
| sam-berry | MID | 29 | 3992 | -50 | +0 | 3942 | -50 | -1.25% |
| marcus-bontempelli | MID | 4 | 3876 | -49 | +0 | 3827 | -49 | -1.26% |
| ed-richards | MID | 16 | 3924 | -48 | +0 | 3876 | -48 | -1.22% |
| harley-reid | MID | 1 | 3820 | -48 | +0 | 3772 | -48 | -1.26% |
| nick-watson | SF | 5 | 3839 | -48 | +0 | 3791 | -48 | -1.25% |
| ryley-sanders | MID | 6 | 3885 | -48 | +0 | 3837 | -48 | -1.24% |
| finn-o-sullivan | MID | 2 | 3740 | -47 | +0 | 3693 | -47 | -1.26% |
| josh-worrell | SD | 28 | 3723 | -46 | +0 | 3677 | -46 | -1.24% |
| callum-wilkie | KPD | 1 | 3633 | -45 | +0 | 3588 | -45 | -1.24% |
| isaac-heeney | MID | 4 | 3537 | -44 | +0 | 3493 | -44 | -1.24% |
| levi-ashcroft | MID | 5 | 3519 | -44 | +0 | 3475 | -44 | -1.25% |
| nicholas-martin | MID | pool | 3513 | -44 | +0 | 3469 | -44 | -1.25% |
| timothy-english | RUCK | 19 | 3535 | -44 | +0 | 3491 | -44 | -1.24% |
| jordan-dawson | MID | 55 | 3443 | -43 | +0 | 3400 | -43 | -1.25% |
| jack-sinclair | SD | 1 | 3322 | -42 | +0 | 3280 | -42 | -1.26% |
| darcy-wilmot | SD | 16 | 3313 | -41 | +0 | 3272 | -41 | -1.24% |
| max-gawn | RUCK | 33 | 3336 | -41 | +0 | 3295 | -41 | -1.23% |
| darcy-wilson | SF | 18 | 3224 | -40 | +0 | 3184 | -40 | -1.24% |
| george-wardlaw | MID | 4 | 3235 | -40 | +0 | 3195 | -40 | -1.24% |
| jordan-clark | SD | 15 | 3264 | -40 | +0 | 3224 | -40 | -1.23% |
| logan-morris | KPF | 31 | 3247 | -40 | +0 | 3207 | -40 | -1.23% |
| andrew-brayshaw | MID | 2 | 3138 | -39 | +0 | 3099 | -39 | -1.24% |
| sam-walsh | MID | 1 | 3041 | -38 | +0 | 3003 | -38 | -1.25% |
| daniel-annable | MID | 6 | 1395 | -5 | +42 | 1432 | +37 | +2.65% |
| hugo-garcia | MID | 50 | 3062 | -37 | +0 | 3025 | -37 | -1.21% |
| connor-o-sullivan | KPD | 11 | 2920 | -36 | +0 | 2884 | -36 | -1.23% |
| joel-freijah | MID | 45 | 2883 | -36 | +0 | 2847 | -36 | -1.25% |
| ollie-greeves | MID | 5 | 583 | -3 | +39 | 619 | +36 | +6.17% |
| zac-bailey | SF | 15 | 2914 | -36 | +0 | 2878 | -36 | -1.24% |
| josh-ward | MID | 7 | 2817 | -35 | +0 | 2782 | -35 | -1.24% |
| chris-scerri | SF | pool | 459 | -6 | +40 | 493 | +34 | +7.41% |
| jack-ross | MID | 43 | 2761 | -34 | +0 | 2727 | -34 | -1.23% |
| max-hall | SF | 4 | 2790 | -34 | +0 | 2756 | -34 | -1.22% |
| shannon-neale | KPF | 35 | 2711 | -34 | +0 | 2677 | -34 | -1.25% |
| thomas-burton | SF | pool | 439 | -6 | +40 | 473 | +34 | +7.74% |
| connor-macdonald | SF | 26 | 2740 | -33 | +0 | 2707 | -33 | -1.20% |
| connor-rozee | MID | 5 | 2725 | -33 | +0 | 2692 | -33 | -1.21% |
| harvey-langford | MID | 6 | 2657 | -33 | +0 | 2624 | -33 | -1.24% |
| jack-dalton | SF | 34 | 437 | -3 | +36 | 470 | +33 | +7.55% |
| zachary-merrett | MID | 26 | 2704 | -33 | +0 | 2671 | -33 | -1.22% |
| bailey-humphrey | MID | 6 | 2573 | -32 | +0 | 2541 | -32 | -1.24% |
| cameron-nairn | SF | 20 | 606 | -4 | +36 | 638 | +32 | +5.28% |
| jaspa-fletcher | SD | 12 | 2616 | -32 | +0 | 2584 | -32 | -1.22% |
| xavier-bamert | SF | 5 | 509 | -6 | +38 | 541 | +32 | +6.29% |
| bailey-williams-wc | RUCK | 35 | 2470 | -31 | +0 | 2439 | -31 | -1.26% |
| daniel-curtin | MID | 8 | 2488 | -31 | +0 | 2457 | -31 | -1.25% |
| jase-burgoyne | SD | 60 | 2549 | -31 | +0 | 2518 | -31 | -1.22% |
| sam-durham | MID | 9 | 2531 | -31 | +0 | 2500 | -31 | -1.22% |
| ollie-dempsey | MID | 7 | 2428 | -30 | +0 | 2398 | -30 | -1.24% |
| will-day | MID | 13 | 2387 | -30 | +0 | 2357 | -30 | -1.26% |
| clayton-oliver | MID | 4 | 2334 | -29 | +0 | 2305 | -29 | -1.24% |
| lachie-neale | MID | 66 | 2348 | -29 | +0 | 2319 | -29 | -1.24% |
| mattaes-phillipou | MID | 10 | 2281 | -29 | +0 | 2252 | -29 | -1.27% |
| mitchell-edwards | RUCK | 32 | 2439 | -29 | +0 | 2410 | -29 | -1.19% |
| reuben-ginbey | KPD | 9 | 2349 | -29 | +0 | 2320 | -29 | -1.23% |
| taj-hotton | MID | 12 | 2355 | -29 | +0 | 2326 | -29 | -1.23% |
| tim-taranto | MID | 2 | 2423 | -29 | +0 | 2394 | -29 | -1.20% |
| touk-miller | SF | 29 | 2378 | -29 | +0 | 2349 | -29 | -1.22% |
| bailey-dale | SD | 45 | 2255 | -28 | +0 | 2227 | -28 | -1.24% |
| cameron-mackenzie | MID | 7 | 2251 | -28 | +0 | 2223 | -28 | -1.24% |
| cody-curtin | KPF | 43 | 427 | -3 | +31 | 455 | +28 | +6.56% |
| cooper-trembath | KPF | 9 | 2201 | -28 | +0 | 2173 | -28 | -1.27% |
| max-kondogiannis | SD | 36 | 435 | -6 | +34 | 463 | +28 | +6.44% |
| tanner-bruhn | MID | 12 | 2214 | -28 | +0 | 2186 | -28 | -1.26% |
| connor-idun | SD | 61 | 2224 | -27 | +0 | 2197 | -27 | -1.21% |
| harvey-thomas | MID | 59 | 2247 | -27 | +0 | 2220 | -27 | -1.20% |
| jack-ginnivan | SF | 8 | 2242 | -27 | +0 | 2215 | -27 | -1.20% |
| john-noble | SD | 8 | 2159 | -27 | +0 | 2132 | -27 | -1.25% |
| jordon-sweet | RUCK | 14 | 2285 | -27 | +0 | 2258 | -27 | -1.18% |
| justin-mcinerney | MID | 44 | 2143 | -27 | +0 | 2116 | -27 | -1.26% |
| ned-moyle | RUCK | 5 | 2285 | -27 | +0 | 2258 | -27 | -1.18% |
| tom-powell | MID | 13 | 2103 | -27 | +0 | 2076 | -27 | -1.28% |
| josh-daicos | SD | 57 | 2104 | -26 | +0 | 2078 | -26 | -1.24% |
| lachie-whitfield | SD | 1 | 2223 | -26 | +0 | 2197 | -26 | -1.17% |
| sam-flanders | MID | 11 | 2067 | -26 | +0 | 2041 | -26 | -1.26% |
| shai-bolton | SF | 29 | 2150 | -26 | +0 | 2124 | -26 | -1.21% |
| toby-nankervis | RUCK | 35 | 2031 | -26 | +0 | 2005 | -26 | -1.28% |
| xavier-lindsay | MID | 11 | 2106 | -26 | +0 | 2080 | -26 | -1.23% |
| callum-mills | SD | 3 | 1994 | -25 | +0 | 1969 | -25 | -1.25% |
| christian-petracca | MID | 2 | 2038 | -25 | +0 | 2013 | -25 | -1.23% |
| george-hewett | MID | 32 | 2056 | -25 | +0 | 2031 | -25 | -1.22% |
| jake-soligo | MID | 36 | 2051 | -25 | +0 | 2026 | -25 | -1.22% |
| josh-battle | KPD | 39 | 2028 | -25 | +0 | 2003 | -25 | -1.23% |
| josh-rachele | SF | 6 | 2008 | -25 | +0 | 1983 | -25 | -1.25% |
| kieren-briggs | RUCK | 34 | 1992 | -25 | +0 | 1967 | -25 | -1.26% |
| mitchito-owens | KPF | 33 | 2071 | -25 | +0 | 2046 | -25 | -1.21% |
| rowan-marshall | RUCK | 8 | 2027 | -25 | +0 | 2002 | -25 | -1.23% |
| hussien-el-achkar | SF | 53 | 353 | -4 | +28 | 377 | +24 | +6.80% |
| jacob-van-rooyen | KPF | 19 | 1894 | -24 | +0 | 1870 | -24 | -1.27% |
| phoenix-gothard | SF | 12 | 1891 | -24 | +0 | 1867 | -24 | -1.27% |
| trent-rivers | SD | 32 | 1852 | -24 | +0 | 1828 | -24 | -1.30% |
| lawson-humphries | SD | 63 | 1816 | -23 | +0 | 1793 | -23 | -1.27% |
| leo-lombard | SF | 9 | 1957 | -23 | +0 | 1934 | -23 | -1.18% |
| matthew-roberts | SD | 34 | 1818 | -23 | +0 | 1795 | -23 | -1.27% |
| riley-hamilton | SF | pool | 305 | -4 | +27 | 328 | +23 | +7.54% |
| tom-de-koning | RUCK | 30 | 1830 | -23 | +0 | 1807 | -23 | -1.26% |
| aaron-cadman | KPF | 1 | 1769 | -22 | +0 | 1747 | -22 | -1.24% |
| balyn-o-brien | SD | pool | 383 | -3 | +25 | 405 | +22 | +5.74% |
| caleb-windsor | MID | 7 | 1784 | -22 | +0 | 1762 | -22 | -1.23% |
| harry-mckay | KPF | 10 | 1735 | -22 | +0 | 1713 | -22 | -1.27% |
| hayden-young | MID | 7 | 1762 | -22 | +0 | 1740 | -22 | -1.25% |
| jobe-shanahan | KPF | 30 | 1739 | -22 | +0 | 1717 | -22 | -1.27% |
| marcus-windhager | MID | 47 | 1864 | -22 | +0 | 1842 | -22 | -1.18% |
| nate-caddy | KPF | 10 | 1862 | -22 | +0 | 1840 | -22 | -1.18% |
| wayne-milera | SD | 11 | 1800 | -22 | +0 | 1778 | -22 | -1.22% |
| alix-tauru | KPD | 10 | 1684 | -21 | +0 | 1663 | -21 | -1.25% |
| gryan-miers | SF | 57 | 1650 | -21 | +0 | 1629 | -21 | -1.27% |
| koltyn-tholstrup | SD | 13 | 1698 | -21 | +0 | 1677 | -21 | -1.24% |
| nick-madden | RUCK | pool | 1766 | -21 | +0 | 1745 | -21 | -1.19% |
| oliver-hollands | MID | 11 | 1739 | -21 | +0 | 1718 | -21 | -1.21% |
| peter-wright | KPF | 10 | 1619 | -21 | +0 | 1598 | -21 | -1.30% |
| will-graham | MID | 26 | 1708 | -21 | +0 | 1687 | -21 | -1.23% |
| darcy-cameron | RUCK | 48 | 1669 | -20 | +0 | 1649 | -20 | -1.20% |
| harris-andrews | KPD | 60 | 1623 | -20 | +0 | 1603 | -20 | -1.23% |
| luke-trainor | KPD | 21 | 1551 | -20 | +0 | 1531 | -20 | -1.29% |
| massimo-d-ambrosio | MID | 3 | 1565 | -20 | +0 | 1545 | -20 | -1.28% |
| patrick-retschko | MID | 8 | 1608 | -20 | +0 | 1588 | -20 | -1.24% |
| paul-curtis | SF | 35 | 1622 | -20 | +0 | 1602 | -20 | -1.23% |
| tom-mccartin | KPD | 33 | 1689 | -20 | +0 | 1669 | -20 | -1.18% |
| tom-sparrow | MID | 27 | 1632 | -20 | +0 | 1612 | -20 | -1.23% |
| charlie-banfield | MID | 41 | 536 | -3 | +22 | 555 | +19 | +3.54% |
| cooper-hynes | MID | 20 | 1543 | -19 | +0 | 1524 | -19 | -1.23% |
| hugh-mccluggage | MID | 3 | 1543 | -19 | +0 | 1524 | -19 | -1.23% |
| joel-jeffrey | SD | 30 | 1579 | -19 | +0 | 1560 | -19 | -1.20% |
| joshua-weddle | SD | 18 | 1510 | -19 | +0 | 1491 | -19 | -1.26% |
| mark-keane | KPD | pool | 1557 | -19 | +0 | 1538 | -19 | -1.22% |
| patrick-cripps | MID | 13 | 1488 | -19 | +0 | 1469 | -19 | -1.28% |
| zeke-uwland | SD | 2 | 2633 | -32 | +51 | 2652 | +19 | +0.72% |
| charlie-curnow | KPF | 12 | 1365 | -18 | +0 | 1347 | -18 | -1.32% |
| daniel-turner | KPD | 20 | 1534 | -18 | +0 | 1516 | -18 | -1.17% |
| james-sicily | SD | 52 | 1421 | -18 | +0 | 1403 | -18 | -1.27% |
| jordan-de-goey | SF | 6 | 1433 | -18 | +0 | 1415 | -18 | -1.26% |
| jye-amiss | KPF | 8 | 1495 | -18 | +0 | 1477 | -18 | -1.20% |
| ned-long | MID | 3 | 1416 | -18 | +0 | 1398 | -18 | -1.27% |
| patrick-voss | KPF | 5 | 1538 | -18 | +0 | 1520 | -18 | -1.17% |
| tom-mccarthy | SD | 1 | 1457 | -18 | +0 | 1439 | -18 | -1.24% |
| caleb-daniel | SD | 46 | 1338 | -17 | +0 | 1321 | -17 | -1.27% |
| cooper-lord | MID | 9 | 1345 | -17 | +0 | 1328 | -17 | -1.26% |
| isaac-kako | SF | 13 | 1413 | -17 | +0 | 1396 | -17 | -1.20% |
| jed-walter | KPF | 3 | 1439 | -17 | +0 | 1422 | -17 | -1.18% |
| kane-farrell | SD | 51 | 1306 | -17 | +0 | 1289 | -17 | -1.30% |
| kane-mcauliffe | MID | 40 | 1312 | -17 | +0 | 1295 | -17 | -1.30% |
| logan-evans | SD | 12 | 1361 | -17 | +0 | 1344 | -17 | -1.25% |
| luke-parker | SD | 42 | 1339 | -17 | +0 | 1322 | -17 | -1.27% |
| mitch-georgiades | KPF | 18 | 1427 | -17 | +0 | 1410 | -17 | -1.19% |
| ryan-maric | MID | 1 | 1406 | -17 | +0 | 1389 | -17 | -1.21% |
| dante-visentini | RUCK | 56 | 1274 | -16 | +0 | 1258 | -16 | -1.26% |
| lachlan-mcandrew | RUCK | pool | 1279 | -16 | +0 | 1263 | -16 | -1.25% |
| lloyd-meek | RUCK | 68 | 1300 | -16 | +0 | 1284 | -16 | -1.23% |
| luke-ryan | SD | 65 | 1315 | -16 | +0 | 1299 | -16 | -1.22% |
| xavier-taylor | SD | 11 | 802 | -2 | +18 | 818 | +16 | +2.00% |
| bradley-hill | SF | 42 | 1225 | -15 | +0 | 1210 | -15 | -1.22% |
| brent-daniels | SF | 27 | 1199 | -15 | +0 | 1184 | -15 | -1.25% |
| elijah-tsatas | MID | 5 | 1240 | -15 | +0 | 1225 | -15 | -1.21% |
| jack-steele | MID | 21 | 1191 | -15 | +0 | 1176 | -15 | -1.26% |
| jack-whitlock | KPF | 33 | 1271 | -15 | +0 | 1256 | -15 | -1.18% |
| jai-serong | SD | 53 | 1233 | -15 | +0 | 1218 | -15 | -1.22% |
| james-rowbottom | MID | 25 | 1205 | -15 | +0 | 1190 | -15 | -1.24% |
| joe-berry | SF | 15 | 1259 | -15 | +0 | 1244 | -15 | -1.19% |
| karl-worner | SD | 4 | 1206 | -15 | +0 | 1191 | -15 | -1.24% |
| matt-johnson-1 | MID | 21 | 1131 | -15 | +0 | 1116 | -15 | -1.33% |
| noah-mraz | KPD | 35 | 1769 | -15 | +0 | 1754 | -15 | -0.85% |
| sam-taylor | KPD | 28 | 1212 | -15 | +0 | 1197 | -15 | -1.24% |
| tim-kelly | MID | 24 | 1219 | -15 | +0 | 1204 | -15 | -1.23% |
| aaron-naughton | KPF | 9 | 1166 | -14 | +0 | 1152 | -14 | -1.20% |
| anthony-caminiti | KPF | pool | 1110 | -14 | +0 | 1096 | -14 | -1.26% |
| dan-houston | SD | 30 | 1096 | -14 | +0 | 1082 | -14 | -1.28% |
| dylan-moore | SF | 66 | 1182 | -14 | +0 | 1168 | -14 | -1.18% |
| jake-waterman | KPF | 76 | 1160 | -14 | +0 | 1146 | -14 | -1.21% |
| james-peatling | MID | 8 | 1098 | -14 | +0 | 1084 | -14 | -1.28% |
| josh-dunkley | MID | 25 | 1134 | -14 | +0 | 1120 | -14 | -1.23% |
| jy-simpkin | MID | 12 | 1164 | -14 | +0 | 1150 | -14 | -1.20% |
| mason-redman | SD | 30 | 1176 | -14 | +0 | 1162 | -14 | -1.19% |
| thomas-liberatore | MID | 24 | 1018 | -14 | +0 | 1004 | -14 | -1.38% |
| thomas-stewart | SD | 40 | 1101 | -14 | +0 | 1087 | -14 | -1.27% |
| ty-gallop | KPF | 42 | 1199 | -14 | +0 | 1185 | -14 | -1.17% |
| tyler-sonsie | MID | 28 | 1095 | -14 | +0 | 1081 | -14 | -1.28% |
| zach-reid | KPD | 10 | 1093 | -14 | +0 | 1079 | -14 | -1.28% |
| andrew-mcgrath | SD | 1 | 1022 | -13 | +0 | 1009 | -13 | -1.27% |
| billy-wilson | SD | 34 | 983 | -13 | +0 | 970 | -13 | -1.32% |
| bo-allan | SD | 16 | 1128 | -13 | +0 | 1115 | -13 | -1.15% |
| darcy-jones | SF | 21 | 1144 | -13 | +0 | 1131 | -13 | -1.14% |
| dayne-zorko | SD | 38 | 998 | -13 | +0 | 985 | -13 | -1.30% |
| hamish-davis | MID | 65 | 1028 | -13 | +0 | 1015 | -13 | -1.26% |
| jhye-clark | MID | 8 | 1059 | -13 | +0 | 1046 | -13 | -1.23% |
| jordan-croft | KPF | 15 | 1048 | -13 | +0 | 1035 | -13 | -1.24% |
| jye-caldwell | MID | 11 | 979 | -13 | +0 | 966 | -13 | -1.33% |
| sam-draper | RUCK | 1 | 1107 | -13 | +0 | 1094 | -13 | -1.17% |
| adam-cerra | MID | 5 | 1030 | -12 | +0 | 1018 | -12 | -1.17% |
| ben-miller | KPD | 62 | 1042 | -12 | +0 | 1030 | -12 | -1.15% |
| edward-allan | MID | 19 | 978 | -12 | +0 | 966 | -12 | -1.23% |
| ethan-read | KPF | 9 | 1024 | -12 | +0 | 1012 | -12 | -1.17% |
| jacob-weitering | KPD | 1 | 1013 | -12 | +0 | 1001 | -12 | -1.18% |
| jayden-short | SD | 9 | 887 | -12 | +0 | 875 | -12 | -1.35% |
| joe-richards | SF | 48 | 915 | -12 | +0 | 903 | -12 | -1.31% |
| jonty-faull | KPF | 14 | 989 | -12 | +0 | 977 | -12 | -1.21% |
| marcus-herbert | SD | 13 | 906 | -12 | +0 | 894 | -12 | -1.32% |
| matt-carroll | MID | 7 | 1014 | -12 | +0 | 1002 | -12 | -1.18% |
| miles-bergman | SD | 14 | 922 | -12 | +0 | 910 | -12 | -1.30% |
| neil-erasmus | MID | 10 | 1026 | -12 | +0 | 1014 | -12 | -1.17% |
| sam-banks | SD | 29 | 937 | -12 | +0 | 925 | -12 | -1.28% |
| sam-de-koning | KPD | 19 | 936 | -12 | +0 | 924 | -12 | -1.28% |
| seth-campbell | SF | 3 | 1010 | -12 | +0 | 998 | -12 | -1.19% |
| adam-treloar | SF | 14 | 911 | -11 | +0 | 900 | -11 | -1.21% |
| calsher-dear | KPF | 56 | 892 | -11 | +0 | 881 | -11 | -1.23% |
| christian-moraes | MID | 38 | 906 | -11 | +0 | 895 | -11 | -1.21% |
| hugh-boxshall | MID | 45 | 965 | -11 | +0 | 954 | -11 | -1.14% |
| jedd-busslinger | KPD | 13 | 916 | -11 | +0 | 905 | -11 | -1.20% |
| kai-lohmann | SF | 20 | 879 | -11 | +0 | 868 | -11 | -1.25% |
| reilly-o-brien | RUCK | 8 | 985 | -11 | +0 | 974 | -11 | -1.12% |
| toby-greene | SF | 17 | 847 | -11 | +0 | 836 | -11 | -1.30% |
| angus-sheldrick | MID | 18 | 748 | -10 | +0 | 738 | -10 | -1.34% |
| archer-day-wicks | SF | 1 | 766 | -10 | +0 | 756 | -10 | -1.31% |
| charlie-comben | KPD | 31 | 809 | -10 | +0 | 799 | -10 | -1.24% |
| darcy-fogarty | KPF | 12 | 852 | -10 | +0 | 842 | -10 | -1.17% |
| elijah-hewett | MID | 14 | 730 | -10 | +0 | 720 | -10 | -1.37% |
| elijah-hollands | SF | 7 | 710 | -10 | +0 | 700 | -10 | -1.41% |
| harry-rowston | MID | 16 | 787 | -10 | +0 | 777 | -10 | -1.27% |
| jack-gunston | KPF | 29 | 753 | -10 | +0 | 743 | -10 | -1.33% |
| james-o-donnell | KPD | pool | 727 | -10 | +0 | 717 | -10 | -1.38% |
| jarman-impey | SD | 21 | 845 | -10 | +0 | 835 | -10 | -1.18% |
| kade-chandler | SF | 10 | 811 | -10 | +0 | 801 | -10 | -1.23% |
| sean-darcy | RUCK | 38 | 734 | -10 | +0 | 724 | -10 | -1.36% |
| will-mclachlan | SF | 6 | 148 | -1 | +11 | 158 | +10 | +6.76% |
| zane-duursma | SF | 4 | 815 | -10 | +0 | 805 | -10 | -1.23% |
| aliir-aliir | KPD | 44 | 773 | -9 | +0 | 764 | -9 | -1.16% |
| archer-reid | KPF | 30 | 762 | -9 | +0 | 753 | -9 | -1.18% |
| brayden-cook | MID | 26 | 782 | -9 | +0 | 773 | -9 | -1.15% |
| charlie-west | KPF | 50 | 692 | -9 | +0 | 683 | -9 | -1.30% |
| ed-langdon | SD | 54 | 795 | -9 | +0 | 786 | -9 | -1.13% |
| jack-graham | MID | 53 | 651 | -9 | +0 | 642 | -9 | -1.38% |
| jeremy-cameron | KPF | 12 | 778 | -9 | +0 | 769 | -9 | -1.16% |
| jordan-ridley | SD | 22 | 695 | -9 | +0 | 686 | -9 | -1.29% |
| keidean-coleman | SD | 36 | 754 | -9 | +0 | 745 | -9 | -1.19% |
| lachie-jaques | SD | 29 | 725 | -9 | +0 | 716 | -9 | -1.24% |
| logan-mcdonald | KPF | 4 | 693 | -9 | +0 | 684 | -9 | -1.30% |
| nick-bryan | RUCK | 37 | 778 | -9 | +0 | 769 | -9 | -1.16% |
| oliver-florent | SD | 11 | 732 | -9 | +0 | 723 | -9 | -1.23% |
| wil-powell | SD | 19 | 775 | -9 | +0 | 766 | -9 | -1.16% |
| zak-johnson | SD | 70 | 730 | -9 | +0 | 721 | -9 | -1.23% |
| bailey-williams-wb | SD | 48 | 612 | -8 | +0 | 604 | -8 | -1.31% |
| brodie-kemp | KPF | 17 | 680 | -8 | +0 | 672 | -8 | -1.18% |
| darcy-parish | MID | 5 | 562 | -8 | +0 | 554 | -8 | -1.42% |
| dylan-stephens | MID | 5 | 620 | -8 | +0 | 612 | -8 | -1.29% |
| isaac-quaynor | SD | 13 | 596 | -8 | +0 | 588 | -8 | -1.34% |
| jack-ough | MID | 36 | 687 | -8 | +0 | 679 | -8 | -1.16% |
| jack-silvagni | KPD | 53 | 617 | -8 | +0 | 609 | -8 | -1.30% |
| joseph-fonti | SD | 44 | 596 | -8 | +0 | 588 | -8 | -1.34% |
| josh-lai | SD | pool | 597 | -8 | +0 | 589 | -8 | -1.34% |
| lachlan-cowan | SD | 30 | 724 | -8 | +0 | 716 | -8 | -1.10% |
| lachlan-schultz | SF | 57 | 740 | -8 | +0 | 732 | -8 | -1.08% |
| max-heath | RUCK | 7 | 682 | -8 | +0 | 674 | -8 | -1.17% |
| nathan-o-driscoll | MID | 28 | 597 | -8 | +0 | 589 | -8 | -1.34% |
| patrick-lipinski | SF | 28 | 735 | -8 | +0 | 727 | -8 | -1.09% |
| rory-laird | SD | 8 | 701 | -8 | +0 | 693 | -8 | -1.14% |
| samuel-collins | KPD | 54 | 619 | -8 | +0 | 611 | -8 | -1.29% |
| tobie-travaglia | SD | 8 | 685 | -8 | +0 | 677 | -8 | -1.17% |
| angus-clarke | SD | 39 | 555 | -7 | +0 | 548 | -7 | -1.26% |
| blake-hardwick | SD | 44 | 524 | -7 | +0 | 517 | -7 | -1.34% |
| daniel-rioli | SD | 15 | 640 | -7 | +0 | 633 | -7 | -1.09% |
| darcy-byrne-jones | SD | 50 | 664 | -7 | +0 | 657 | -7 | -1.05% |
| francis-evans | SF | 40 | 494 | -7 | +0 | 487 | -7 | -1.42% |
| jake-rogers | SF | 14 | 587 | -7 | +0 | 580 | -7 | -1.19% |
| josh-dolan | SF | 31 | 501 | -7 | +0 | 494 | -7 | -1.40% |
| max-gruzewski | KPF | 22 | 626 | -7 | +0 | 619 | -7 | -1.12% |
| nic-newman | SD | 24 | 628 | -7 | +0 | 621 | -7 | -1.11% |
| sam-marshall | MID | 25 | 704 | -7 | +0 | 697 | -7 | -0.99% |
| shaun-mannagh | SF | 36 | 663 | -7 | +0 | 656 | -7 | -1.06% |
| will-brodie | MID | 9 | 773 | -7 | +0 | 766 | -7 | -0.91% |
| will-setterfield | MID | 5 | 559 | -7 | +0 | 552 | -7 | -1.25% |
| willem-drew | MID | 33 | 608 | -7 | +0 | 601 | -7 | -1.15% |
| alex-davies | MID | 17 | 401 | -6 | +0 | 395 | -6 | -1.50% |
| archie-may | KPF | 6 | 476 | -6 | +0 | 470 | -6 | -1.26% |
| cameron-rayner | SF | 1 | 457 | -6 | +0 | 451 | -6 | -1.31% |
| cooper-harvey | SF | 56 | 545 | -6 | +0 | 539 | -6 | -1.10% |
| cooper-sharman | KPF | 18 | 429 | -6 | +0 | 423 | -6 | -1.40% |
| heath-chapman | SD | 14 | 460 | -6 | +0 | 454 | -6 | -1.30% |
| jack-buckley | KPD | pool | 548 | -6 | +0 | 542 | -6 | -1.09% |
| jack-williams | KPF | 57 | 415 | -6 | +0 | 409 | -6 | -1.45% |
| james-borlase | KPD | pool | 424 | -6 | +0 | 418 | -6 | -1.42% |
| james-leake | SD | 17 | 563 | -6 | +0 | 557 | -6 | -1.07% |
| kyle-langford | KPF | 18 | 518 | -6 | +0 | 512 | -6 | -1.16% |
| liam-baker | SD | 11 | 402 | -6 | +0 | 396 | -6 | -1.49% |
| liam-fawcett | KPF | 43 | 454 | -6 | +0 | 448 | -6 | -1.32% |
| marc-pittonet | RUCK | 50 | 466 | -6 | +0 | 460 | -6 | -1.29% |
| matthew-kennedy-1 | MID | 13 | 423 | -6 | +0 | 417 | -6 | -1.42% |
| max-michalanney | SD | 17 | 493 | -6 | +0 | 487 | -6 | -1.22% |
| mitchell-lewis | KPF | 75 | 517 | -6 | +0 | 511 | -6 | -1.16% |
| nick-larkey | KPF | 72 | 455 | -6 | +0 | 449 | -6 | -1.32% |
| noah-roberts-thomson | SF | 54 | 213 | -1 | +7 | 219 | +6 | +2.82% |
| peter-ladhams | RUCK | 7 | 493 | -6 | +0 | 487 | -6 | -1.22% |
| rhett-bazzo | KPD | 37 | 476 | -6 | +0 | 470 | -6 | -1.26% |
| ryan-angwin | MID | 19 | 483 | -6 | +0 | 477 | -6 | -1.24% |
| tom-brown | SD | 17 | 493 | -6 | +0 | 487 | -6 | -1.22% |
| adam-saad | SD | 19 | 426 | -5 | +0 | 421 | -5 | -1.17% |
| alex-neal-bullen | SF | 40 | 371 | -5 | +0 | 366 | -5 | -1.35% |
| brayden-maynard | SD | 30 | 489 | -5 | +0 | 484 | -5 | -1.02% |
| caiden-cleary | SF | 24 | 471 | -5 | +0 | 466 | -5 | -1.06% |
| harrison-oliver | SD | 19 | 528 | -5 | +0 | 523 | -5 | -0.95% |
| harry-armstrong | KPF | 23 | 620 | -5 | +0 | 615 | -5 | -0.81% |
| jack-lukosius | SF | 2 | 462 | -5 | +0 | 457 | -5 | -1.08% |
| jasper-alger | SF | 58 | 434 | -5 | +0 | 429 | -5 | -1.15% |
| jayden-nguyen | SD | pool | 471 | -5 | +0 | 466 | -5 | -1.06% |
| josh-draper | KPD | pool | 389 | -5 | +0 | 384 | -5 | -1.29% |
| karl-amon | SD | 59 | 344 | -5 | +0 | 339 | -5 | -1.45% |
| lachlan-gulbin | SF | pool | 415 | -5 | +0 | 410 | -5 | -1.20% |
| luke-nankervis | SD | 1 | 384 | -5 | +0 | 379 | -5 | -1.30% |
| mason-wood | SF | 44 | 383 | -5 | +0 | 378 | -5 | -1.31% |
| matthew-flynn | RUCK | 41 | 502 | -5 | +0 | 497 | -5 | -1.00% |
| matthew-jefferson | KPF | 15 | 405 | -5 | +0 | 400 | -5 | -1.23% |
| noah-balta | KPF | 25 | 418 | -5 | +0 | 413 | -5 | -1.20% |
| oliver-francou | MID | 3 | 576 | -5 | +0 | 571 | -5 | -0.87% |
| oliver-hannaford | SF | 18 | 398 | -5 | +0 | 393 | -5 | -1.26% |
| oscar-steene | RUCK | pool | 468 | -5 | +0 | 463 | -5 | -1.07% |
| tom-hanily | SF | 14 | 216 | -2 | +7 | 221 | +5 | +2.31% |
| wil-dawson | KPD | 22 | 525 | -5 | +0 | 520 | -5 | -0.95% |
| will-hayes-b | SF | 56 | 378 | -5 | +0 | 373 | -5 | -1.32% |
| william-mccabe | KPF | 19 | 599 | -5 | +0 | 594 | -5 | -0.83% |
| brady-hough | SD | 31 | 292 | -4 | +0 | 288 | -4 | -1.37% |
| braeden-campbell | SD | 5 | 403 | -4 | +0 | 399 | -4 | -0.99% |
| campbell-chesser | MID | 14 | 330 | -4 | +0 | 326 | -4 | -1.21% |
| connor-budarick | SD | 9 | 281 | -4 | +0 | 277 | -4 | -1.42% |
| daniel-mcstay | KPF | 25 | 338 | -4 | +0 | 334 | -4 | -1.18% |
| elliot-yeo | MID | 36 | 331 | -4 | +0 | 327 | -4 | -1.21% |
| harrison-ramm | KPD | 3 | 545 | -4 | +0 | 541 | -4 | -0.73% |
| harvey-johnston | SD | 49 | 329 | -4 | +0 | 325 | -4 | -1.22% |
| jack-crisp | MID | 34 | 410 | -4 | +0 | 406 | -4 | -0.98% |
| james-worpel | MID | 45 | 413 | -4 | +0 | 409 | -4 | -0.97% |
| jaxon-artemis | SD | 1 | 520 | -4 | +0 | 516 | -4 | -0.77% |
| jaxon-prior | SD | 58 | 305 | -4 | +0 | 301 | -4 | -1.31% |
| josaia-delana | SF | pool | 391 | -4 | +0 | 387 | -4 | -1.02% |
| joshua-kelly | MID | 2 | 370 | -4 | +0 | 366 | -4 | -1.08% |
| malakai-champion | SF | pool | 341 | -4 | +0 | 337 | -4 | -1.17% |
| mitchell-hinge | SD | 15 | 322 | -4 | +0 | 318 | -4 | -1.24% |
| nick-murray | KPD | pool | 321 | -4 | +0 | 317 | -4 | -1.25% |
| oliver-wines | MID | 10 | 255 | -4 | +0 | 251 | -4 | -1.57% |
| riley-bice | SD | 41 | 274 | -4 | +0 | 270 | -4 | -1.46% |
| sam-clohesy | MID | 3 | 288 | -4 | +0 | 284 | -4 | -1.39% |
| thomas-sims | KPF | 28 | 583 | -4 | +0 | 579 | -4 | -0.69% |
| toby-bedford | SF | 75 | 272 | -4 | +0 | 268 | -4 | -1.47% |
| tom-doedee | SD | 17 | 228 | -4 | +0 | 224 | -4 | -1.75% |
| tom-gross | MID | 46 | 460 | -4 | +0 | 456 | -4 | -0.87% |
| tom-papley | SF | 11 | 353 | -4 | +0 | 349 | -4 | -1.13% |
| zachary-williams | SF | pool | 368 | -4 | +0 | 364 | -4 | -1.09% |
| zane-peucker | SF | 31 | 384 | +0 | +4 | 388 | +4 | +1.04% |
| ben-keays | SF | 24 | 196 | -3 | +0 | 193 | -3 | -1.53% |
| ben-king | KPF | 6 | 218 | -3 | +0 | 215 | -3 | -1.38% |
| blake-howes | SD | 39 | 272 | -3 | +0 | 269 | -3 | -1.10% |
| brennan-cox | KPD | 41 | 259 | -3 | +0 | 256 | -3 | -1.16% |
| conor-nash | MID | pool | 235 | -3 | +0 | 232 | -3 | -1.28% |
| dion-prestia | MID | 9 | 251 | -3 | +0 | 248 | -3 | -1.20% |
| harrison-petty | KPD | 37 | 207 | -3 | +0 | 204 | -3 | -1.45% |
| hayden-mclean | KPF | pool | 214 | -3 | +0 | 211 | -3 | -1.40% |
| hugo-hall-kahan | SD | 10 | 215 | -3 | +0 | 212 | -3 | -1.40% |
| isaiah-dudley | SF | pool | 234 | -3 | +0 | 231 | -3 | -1.28% |
| jack-henry | KPD | 12 | 251 | -3 | +0 | 248 | -3 | -1.20% |
| jack-viney | MID | 13 | 229 | -3 | +0 | 226 | -3 | -1.31% |
| jacob-konstanty | SF | 20 | 181 | -3 | +0 | 178 | -3 | -1.66% |
| jake-riccardi | KPF | 50 | 257 | -3 | +0 | 254 | -3 | -1.17% |
| jamarra-ugle-hagan | KPF | 1 | 287 | -3 | +0 | 284 | -3 | -1.05% |
| james-jordon | MID | 33 | 176 | -3 | +0 | 173 | -3 | -1.70% |
| jeremy-howe | SD | 35 | 224 | -3 | +0 | 221 | -3 | -1.34% |
| judd-mcvee | SD | 9 | 316 | -3 | +0 | 313 | -3 | -0.95% |
| leek-aleer | KPD | 15 | 231 | -3 | +0 | 228 | -3 | -1.30% |
| liam-duggan | SD | 12 | 210 | -3 | +0 | 207 | -3 | -1.43% |
| max-king-stk | KPF | 4 | 239 | -3 | +0 | 236 | -3 | -1.26% |
| milan-murdock | SF | pool | 208 | -3 | +0 | 205 | -3 | -1.44% |
| ned-reeves | RUCK | pool | 236 | -3 | +0 | 233 | -3 | -1.27% |
| rory-lobb | KPD | 29 | 276 | -3 | +0 | 273 | -3 | -1.09% |
| samson-ryan | RUCK | 42 | 302 | -3 | +0 | 299 | -3 | -0.99% |
| sandy-brock | KPD | pool | 173 | -3 | +0 | 170 | -3 | -1.73% |
| scott-pendlebury | MID | 5 | 353 | -3 | +0 | 350 | -3 | -0.85% |
| sid-draper | MID | 4 | 1250 | -3 | +0 | 1247 | -3 | -0.24% |
| stephen-coniglio | MID | 3 | 215 | -3 | +0 | 212 | -3 | -1.40% |
| toby-mcmullin | SF | 34 | 135 | -3 | +0 | 132 | -3 | -2.22% |
| toby-murray | KPF | 7 | 215 | -3 | +0 | 212 | -3 | -1.40% |
| tom-atkins | MID | 7 | 298 | -3 | +0 | 295 | -3 | -1.01% |
| tylar-young | KPD | 9 | 279 | -3 | +0 | 276 | -3 | -1.08% |
| tyson-stengle | SF | 4 | 151 | -3 | +0 | 148 | -3 | -1.99% |
| will-edwards | KPD | pool | 214 | -3 | +0 | 211 | -3 | -1.40% |
| will-hayward | SF | 21 | 229 | -3 | +0 | 226 | -3 | -1.31% |
| will-lorenz | MID | 57 | 284 | -3 | +0 | 281 | -3 | -1.06% |
| zac-taylor | SF | 44 | 207 | -3 | +0 | 204 | -3 | -1.45% |
| angus-anderson | MID | 57 | 165 | -2 | +0 | 163 | -2 | -1.21% |
| archie-perkins | SF | 9 | 239 | -2 | +0 | 237 | -2 | -0.84% |
| arthur-jones | SF | 43 | 92 | -2 | +0 | 90 | -2 | -2.17% |
| bailey-macdonald | SD | 51 | 148 | -2 | +0 | 146 | -2 | -1.35% |
| bayley-fritsch | SF | 31 | 199 | -2 | +0 | 197 | -2 | -1.01% |
| ben-ainsworth | SF | 4 | 204 | -2 | +0 | 202 | -2 | -0.98% |
| brayden-fiorini | MID | 20 | 167 | -2 | +0 | 165 | -2 | -1.20% |
| campbell-gray | KPD | 15 | 176 | -2 | +0 | 174 | -2 | -1.14% |
| campbell-lake | SF | 7 | 161 | -2 | +0 | 159 | -2 | -1.24% |
| charlie-cameron | SF | 6 | 151 | -2 | +0 | 149 | -2 | -1.32% |
| cody-weightman | SF | 15 | 153 | -2 | +0 | 151 | -2 | -1.31% |
| darcy-moore | KPD | 8 | 141 | -2 | +0 | 139 | -2 | -1.42% |
| deven-robertson | MID | 22 | 174 | -2 | +0 | 172 | -2 | -1.15% |
| finnbar-maley | KPF | 2 | 192 | -2 | +0 | 190 | -2 | -1.04% |
| griffin-logue | KPD | 8 | 78 | -2 | +0 | 76 | -2 | -2.56% |
| harrison-jones | KPF | 30 | 172 | -2 | +0 | 170 | -2 | -1.16% |
| harry-sharp | SF | 45 | 155 | -2 | +0 | 153 | -2 | -1.29% |
| hugh-bond | SD | 50 | 153 | -2 | +0 | 151 | -2 | -1.31% |
| jack-darling | KPF | 28 | 155 | -2 | +0 | 153 | -2 | -1.29% |
| jai-culley | MID | 1 | 178 | -2 | +0 | 176 | -2 | -1.12% |
| jake-lever | KPD | 15 | 143 | -2 | +0 | 141 | -2 | -1.40% |
| jake-lloyd | SD | 16 | 173 | -2 | +0 | 171 | -2 | -1.16% |
| jarrod-berry | MID | 17 | 189 | -2 | +0 | 187 | -2 | -1.06% |
| jayden-laverde | KPD | 20 | 193 | -2 | +0 | 191 | -2 | -1.04% |
| jesse-hogan | KPF | 5 | 205 | -2 | +0 | 203 | -2 | -0.98% |
| joel-fitzgerald | MID | 16 | 72 | -2 | +0 | 70 | -2 | -2.78% |
| kye-annand | KPD | 2 | 239 | -2 | +0 | 237 | -2 | -0.84% |
| lachlan-bramble | SF | pool | 89 | -2 | +0 | 87 | -2 | -2.25% |
| luke-kennedy | MID | 62 | 284 | -2 | +0 | 282 | -2 | -0.70% |
| luker-kentfield | KPF | 11 | 419 | -2 | +0 | 417 | -2 | -0.48% |
| mabior-chol | KPF | 25 | 205 | -2 | +0 | 203 | -2 | -0.98% |
| michael-sellwood | SD | 5 | 168 | -2 | +0 | 166 | -2 | -1.19% |
| noah-long | SF | 57 | 124 | -2 | +0 | 122 | -2 | -1.61% |
| oliver-hayes-brown | RUCK | pool | 190 | -2 | +0 | 188 | -2 | -1.05% |
| oliver-henry | SF | 18 | 197 | -2 | +0 | 195 | -2 | -1.02% |
| oscar-allen | KPF | 21 | 100 | -2 | +0 | 98 | -2 | -2.00% |
| sam-powell-pepper | SF | 18 | 167 | -2 | +0 | 165 | -2 | -1.20% |
| steely-green | SF | 55 | 150 | -2 | +0 | 148 | -2 | -1.33% |
| tim-membrey | KPF | 49 | 129 | -2 | +0 | 127 | -2 | -1.55% |
| wade-derksen | KPD | 5 | 109 | -2 | +0 | 107 | -2 | -1.83% |
| zac-fisher | SF | 27 | 113 | -2 | +0 | 111 | -2 | -1.77% |
| zach-guthrie | SD | 21 | 210 | -2 | +0 | 208 | -2 | -0.95% |
| aidan-schubert | KPF | 23 | 481 | +1 | -2 | 480 | -1 | -0.21% |
| angus-hastie | SD | 33 | 181 | -1 | +0 | 180 | -1 | -0.55% |
| ashton-moir | SF | 29 | 214 | -1 | +0 | 213 | -1 | -0.47% |
| beau-mccreery | SF | 46 | 134 | -1 | +0 | 133 | -1 | -0.75% |
| ben-jepson | MID | pool | 222 | +1 | +0 | 223 | +1 | +0.45% |
| bodie-ryan | SD | 46 | 210 | -1 | +0 | 209 | -1 | -0.48% |
| buku-khamis | KPD | pool | 144 | -1 | +0 | 143 | -1 | -0.69% |
| caleb-graham | KPD | 71 | 54 | -1 | +0 | 53 | -1 | -1.85% |
| cameron-zurhaar | SF | 9 | 125 | -1 | +0 | 124 | -1 | -0.80% |
| charlie-edwards | MID | 21 | 624 | -1 | +0 | 623 | -1 | -0.16% |
| christian-salem | SD | 9 | 92 | -1 | +0 | 91 | -1 | -1.09% |
| clay-hall | MID | 38 | 214 | -1 | +0 | 213 | -1 | -0.47% |
| corey-durdin | SF | 39 | 49 | -1 | +0 | 48 | -1 | -2.04% |
| dougal-howard | KPD | 56 | 45 | -1 | +0 | 44 | -1 | -2.22% |
| harrison-himmelberg | SD | 16 | 138 | -1 | +0 | 137 | -1 | -0.72% |
| harry-edwards | KPD | 12 | 104 | -1 | +0 | 103 | -1 | -0.96% |
| harvey-harrison | SF | 52 | 50 | -1 | +0 | 49 | -1 | -2.00% |
| hudson-o-keeffe | KPF | pool | 275 | -1 | +0 | 274 | -1 | -0.36% |
| jack-carroll | SD | 43 | 80 | -1 | +0 | 79 | -1 | -1.25% |
| jack-higgins | SF | 17 | 52 | -1 | +0 | 51 | -1 | -1.92% |
| jack-payne | KPD | 54 | 94 | -1 | +0 | 93 | -1 | -1.06% |
| jack-scrimshaw | SD | 7 | 89 | -1 | +0 | 88 | -1 | -1.12% |
| jacob-newton | SF | 8 | 299 | -1 | +0 | 298 | -1 | -0.33% |
| jake-stringer | SF | 7 | 103 | -1 | +0 | 102 | -1 | -0.97% |
| james-trezise | SD | 10 | 118 | -1 | +0 | 117 | -1 | -0.85% |
| jarrod-witts | RUCK | 74 | 139 | -1 | +0 | 138 | -1 | -0.72% |
| jay-polkinghorne | SF | 44 | 297 | -1 | +0 | 296 | -1 | -0.34% |
| jeremy-sharp | MID | 27 | 63 | -1 | +0 | 62 | -1 | -1.59% |
| jesse-motlop | SF | 27 | 90 | -1 | +0 | 89 | -1 | -1.11% |
| joel-amartey | KPF | 17 | 31 | -1 | +0 | 30 | -1 | -3.23% |
| josh-gibcus | KPD | 9 | 254 | -1 | +0 | 253 | -1 | -0.39% |
| josh-sinn | SD | 12 | 266 | -1 | +0 | 265 | -1 | -0.38% |
| lachlan-jones | SD | 16 | 125 | -1 | +0 | 124 | -1 | -0.80% |
| lachlan-sholl | MID | 64 | 137 | -1 | +0 | 136 | -1 | -0.73% |
| lachlan-smith | RUCK | 47 | 399 | -1 | +0 | 398 | -1 | -0.25% |
| lewis-melican | KPD | 32 | 21 | -1 | +0 | 20 | -1 | -4.76% |
| lewis-young | KPD | 49 | 116 | -1 | +0 | 115 | -1 | -0.86% |
| liam-o-connell | SD | pool | 39 | -1 | +0 | 38 | -1 | -2.56% |
| liam-reidy | RUCK | 4 | 329 | -1 | +0 | 328 | -1 | -0.30% |
| lukas-cooke | KPD | 11 | 364 | +1 | +0 | 365 | +1 | +0.27% |
| matt-cottrell | MID | pool | 72 | -1 | +0 | 71 | -1 | -1.39% |
| matt-whitlock | KPF | 27 | 372 | -1 | +0 | 371 | -1 | -0.27% |
| michael-frederick | SF | 60 | 50 | -1 | +0 | 49 | -1 | -2.00% |
| mitch-mcgovern | SD | 43 | 40 | -1 | +0 | 39 | -1 | -2.50% |
| nick-haynes | SD | 10 | 60 | -1 | +0 | 59 | -1 | -1.67% |
| nick-vlastuin | SD | 12 | 83 | -1 | +0 | 82 | -1 | -1.20% |
| nikolas-cox | KPF | 8 | 136 | -1 | +0 | 135 | -1 | -0.74% |
| noah-howes | KPF | 14 | 229 | +1 | +0 | 230 | +1 | +0.44% |
| oscar-adams | KPD | 51 | 79 | -1 | +0 | 78 | -1 | -1.27% |
| oscar-mcdonald | KPD | 53 | 68 | -1 | +0 | 67 | -1 | -1.47% |
| oscar-ryan | SD | 27 | 305 | +1 | +0 | 306 | +1 | +0.33% |
| rhyan-mansell | SF | pool | 48 | -1 | +0 | 47 | -1 | -2.08% |
| rhylee-west | SF | 26 | 100 | -1 | +0 | 99 | -1 | -1.00% |
| riley-garcia | SF | 61 | 47 | -1 | +0 | 46 | -1 | -2.13% |
| riley-hardeman | SD | 23 | 258 | -1 | +0 | 257 | -1 | -0.39% |
| ryan-byrnes | SD | 51 | 64 | -1 | +0 | 63 | -1 | -1.56% |
| taylor-walker | KPF | 64 | 132 | -1 | +0 | 131 | -1 | -0.76% |
| thomas-anastasopoulos | SF | 48 | 173 | -1 | +0 | 172 | -1 | -0.58% |
| todd-marshall | KPF | 16 | 61 | -1 | +0 | 60 | -1 | -1.64% |
| tom-cochrane | SF | 5 | 230 | -1 | +0 | 229 | -1 | -0.43% |
| tom-mcdonald | KPD | 54 | 75 | -1 | +0 | 74 | -1 | -1.33% |
| tyler-brockman | SF | 48 | 50 | -1 | +0 | 49 | -1 | -2.00% |
| tyrell-dewar | SF | pool | 96 | -1 | +0 | 95 | -1 | -1.04% |
| will-green | RUCK | 16 | 604 | +1 | +0 | 605 | +1 | +0.17% |
| xavier-duursma | MID | 18 | 143 | -1 | +0 | 142 | -1 | -0.70% |
| adam-sweid | SF | 25 | 397 | +0 | +0 | 397 | +0 | +0.00% |
| aidan-corr | KPD | 18 | 38 | +0 | +0 | 38 | +0 | +0.00% |
| aidan-johnson | KPF | 68 | 229 | +0 | +0 | 229 | +0 | +0.00% |
| aiden-riddle | RUCK | 2 | 151 | +0 | +0 | 151 | +0 | +0.00% |
| alex-dodson | RUCK | 53 | 274 | +0 | +0 | 274 | +0 | +0.00% |
| alex-pearce | KPD | 37 | 23 | +0 | +0 | 23 | +0 | +0.00% |
| alex-van-wyk | RUCK | 14 | 391 | +0 | +0 | 391 | +0 | +0.00% |
| andy-moniz-wakefield | SD | pool | 54 | +0 | +0 | 54 | +0 | +0.00% |
| archie-ludowyke | KPF | 50 | 206 | +0 | +0 | 206 | +0 | +0.00% |
| asher-eastham | SF | 7 | 94 | +0 | +0 | 94 | +0 | +0.00% |
| avery-thomas | SD | 28 | 394 | +0 | +0 | 394 | +0 | +0.00% |
| bailey-banfield | SF | 3 | 10 | +0 | +0 | 10 | +0 | +0.00% |
| bailey-laurie | SF | 23 | 56 | +0 | +0 | 56 | +0 | +0.00% |
| bailey-scott | MID | 49 | 23 | +0 | +0 | 23 | +0 | +0.00% |
| ben-camporeale | MID | 43 | 249 | +0 | +0 | 249 | +0 | +0.00% |
| ben-long | SF | 25 | 28 | +0 | +0 | 28 | +0 | +0.00% |
| ben-mckay | KPD | 21 | 35 | +0 | +0 | 35 | +0 | +0.00% |
| ben-murphy | SD | pool | 85 | +0 | +0 | 85 | +0 | +0.00% |
| benny-barrett | SF | pool | 50 | +0 | +0 | 50 | +0 | +0.00% |
| billy-cootee | MID | 42 | 264 | +0 | +0 | 264 | +0 | +0.00% |
| billy-dowling | SF | 43 | 150 | +0 | +0 | 150 | +0 | +0.00% |
| billy-frampton | KPD | 74 | 34 | +0 | +0 | 34 | +0 | +0.00% |
| blake-acres | MID | 19 | 86 | +0 | +0 | 86 | +0 | +0.00% |
| blake-thredgold | KPD | 26 | 373 | +0 | +0 | 373 | +0 | +0.00% |
| bobby-hill | SF | 24 | 29 | +0 | +0 | 29 | +0 | +0.00% |
| bradley-close | SF | 8 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| brandon-starcevich | SD | 18 | 41 | +0 | +0 | 41 | +0 | +0.00% |
| brandon-walker | SD | 52 | 57 | +0 | +0 | 57 | +0 | +0.00% |
| brandon-zerk-thatcher | KPD | 65 | 48 | +0 | +0 | 48 | +0 | +0.00% |
| brayden-george | SF | 26 | 234 | +0 | +0 | 234 | +0 | +0.00% |
| brody-mihocek | KPF | 14 | 10 | +0 | +0 | 10 | +0 | +0.00% |
| bruce-reville | MID | pool | 54 | +0 | +0 | 54 | +0 | +0.00% |
| caleb-lewis | KPF | 13 | 233 | +0 | +0 | 233 | +0 | +0.00% |
| caleb-may | RUCK | 9 | 322 | +0 | +0 | 322 | +0 | +0.00% |
| callum-ah-chee | SF | 8 | 64 | +0 | +0 | 64 | +0 | +0.00% |
| callum-brown-ire | SF | pool | 28 | +0 | +0 | 28 | +0 | +0.00% |
| callum-coleman-jones | KPF | 20 | 38 | +0 | +0 | 38 | +0 | +0.00% |
| changkuoth-jiath | SD | pool | 12 | +0 | +0 | 12 | +0 | +0.00% |
| charlie-ballard | KPD | 42 | 45 | +0 | +0 | 45 | +0 | +0.00% |
| charlie-nicholls | KPF | 34 | 199 | +0 | +0 | 199 | +0 | +0.00% |
| charlie-spargo | SF | 29 | 26 | +0 | +0 | 26 | +0 | +0.00% |
| chayce-jones | SD | 9 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| cillian-bourke | SD | pool | 85 | +0 | +0 | 85 | +0 | +0.00% |
| cillian-burke | SD | pool | 43 | +0 | +0 | 43 | +0 | +0.00% |
| cody-anderson | SF | 64 | 62 | +0 | +0 | 62 | +0 | +0.00% |
| cody-angove | MID | 24 | 483 | +0 | +0 | 483 | +0 | +0.00% |
| conor-mckenna | SF | pool | 6 | +0 | +0 | 6 | +0 | +0.00% |
| conor-stone | SD | 15 | 76 | +0 | +0 | 76 | +0 | +0.00% |
| cooper-bell | KPD | 49 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| cooper-simpson | SD | 35 | 179 | +0 | +0 | 179 | +0 | +0.00% |
| corey-wagner | SD | 43 | 20 | +0 | +0 | 20 | +0 | +0.00% |
| corey-warner | SF | 40 | 49 | +0 | +0 | 49 | +0 | +0.00% |
| dane-rampe | SD | 23 | 12 | +0 | +0 | 12 | +0 | +0.00% |
| daniel-butler | SF | 65 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| darcy-fort | RUCK | 65 | 16 | +0 | +0 | 16 | +0 | +0.00% |
| darcy-gardiner | KPD | 22 | 33 | +0 | +0 | 33 | +0 | +0.00% |
| darragh-joyce | KPD | pool | 41 | +0 | +0 | 41 | +0 | +0.00% |
| eamonn-armstrong | SD | pool | 43 | +0 | +0 | 43 | +0 | +0.00% |
| elliot-himmelberg | KPF | 51 | 56 | +0 | +0 | 56 | +0 | +0.00% |
| eric-hipwood | KPF | 14 | 42 | +0 | +0 | 42 | +0 | +0.00% |
| esava-ratugolea | KPD | 43 | 64 | +0 | +0 | 64 | +0 | +0.00% |
| ewan-mackinlay | SF | 10 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| finlay-macrae | MID | 20 | 322 | +0 | +0 | 322 | +0 | +0.00% |
| finn-maginness | SF | 29 | 26 | +0 | +0 | 26 | +0 | +0.00% |
| finnegan-davis | SD | 51 | 165 | +0 | +0 | 165 | +0 | +0.00% |
| flynn-perez | SD | pool | 139 | +0 | +0 | 139 | +0 | +0.00% |
| flynn-riley | RUCK | 4 | 391 | +0 | +0 | 391 | +0 | +0.00% |
| flynn-young | SF | 4 | 168 | +0 | +0 | 168 | +0 | +0.00% |
| fred-rodriguez | MID | 1 | 201 | +0 | +0 | 201 | +0 | +0.00% |
| george-stevens | MID | 58 | 142 | +0 | +0 | 142 | +0 | +0.00% |
| harley-barker | MID | 24 | 677 | +0 | +0 | 677 | +0 | +0.00% |
| harrison-coe | RUCK | 8 | 322 | +0 | +0 | 322 | +0 | +0.00% |
| harry-barnett | RUCK | 23 | 553 | +0 | +0 | 553 | +0 | +0.00% |
| harry-charleson | SD | 3 | 105 | +0 | +0 | 105 | +0 | +0.00% |
| harry-cunningham | SD | pool | 10 | +0 | +0 | 10 | +0 | +0.00% |
| harry-demattia | MID | 25 | 430 | +0 | +0 | 430 | +0 | +0.00% |
| harry-morrison | MID | 73 | 20 | +0 | +0 | 20 | +0 | +0.00% |
| harry-o-farrell | KPD | 40 | 201 | +0 | +0 | 201 | +0 | +0.00% |
| harry-perryman | SD | 14 | 68 | +0 | +0 | 68 | +0 | +0.00% |
| harry-schoenberg | MID | 24 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| harvey-gallagher | SD | 39 | 87 | +0 | +0 | 87 | +0 | +0.00% |
| henry-hustwaite | MID | 37 | 235 | +0 | +0 | 235 | +0 | +0.00% |
| henry-smith | KPF | 50 | 82 | +0 | +0 | 82 | +0 | +0.00% |
| hugh-davies | KPD | 33 | 185 | +0 | +0 | 185 | +0 | +0.00% |
| hugo-mikunda | SF | 48 | 177 | +0 | +0 | 177 | +0 | +0.00% |
| hugo-ralphsmith | MID | 45 | 54 | +0 | +0 | 54 | +0 | +0.00% |
| hunter-clark | SD | 7 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| hunter-holmes | MID | 33 | 517 | +0 | +0 | 517 | +0 | +0.00% |
| iliro-smit | RUCK | 10 | 204 | +0 | +0 | 204 | +0 | +0.00% |
| indy-cotton | SD | pool | 48 | +0 | +0 | 48 | +0 | +0.00% |
| isaac-cumming | SD | 20 | 41 | +0 | +0 | 41 | +0 | +0.00% |
| isaac-keeler | KPF | 44 | 173 | +0 | +0 | 173 | +0 | +0.00% |
| jack-bowes | MID | 10 | 97 | +0 | +0 | 97 | +0 | +0.00% |
| jack-buller | KPF | 11 | 94 | +0 | +0 | 94 | +0 | +0.00% |
| jack-henderson | SF | pool | 113 | +0 | +0 | 113 | +0 | +0.00% |
| jack-hutchinson | MID | 3 | 118 | +0 | +0 | 118 | +0 | +0.00% |
| jack-martin | SF | 3 | 107 | +0 | +0 | 107 | +0 | +0.00% |
| jack-watkins | MID | 3 | 130 | +0 | +0 | 130 | +0 | +0.00% |
| jackson-archer | SD | 59 | 27 | +0 | +0 | 27 | +0 | +0.00% |
| jackson-macrae | MID | 8 | 101 | +0 | +0 | 101 | +0 | +0.00% |
| jackson-mead | SF | 25 | 29 | +0 | +0 | 29 | +0 | +0.00% |
| jacob-hopper | MID | 7 | 101 | +0 | +0 | 101 | +0 | +0.00% |
| jacob-molier | RUCK | 52 | 283 | +0 | +0 | 283 | +0 | +0.00% |
| jacob-moss | KPF | pool | 36 | +0 | +0 | 36 | +0 | +0.00% |
| jacob-wehr | SD | 61 | 14 | +0 | +0 | 14 | +0 | +0.00% |
| jade-gresham | SF | 18 | 39 | +0 | +0 | 39 | +0 | +0.00% |
| jaeger-o-meara | MID | 1 | 165 | +0 | +0 | 165 | +0 | +0.00% |
| jai-saxena | SF | pool | 84 | +0 | +0 | 84 | +0 | +0.00% |
| jaime-uhr-henry | RUCK | pool | 26 | +0 | +0 | 26 | +0 | +0.00% |
| jake-kolodjashnij | KPD | 41 | 22 | +0 | +0 | 22 | +0 | +0.00% |
| jake-melksham | KPF | 10 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| jakob-ryan | SD | 28 | 239 | +0 | +0 | 239 | +0 | +0.00% |
| james-barrat | KPD | 32 | 225 | +0 | +0 | 225 | +0 | +0.00% |
| james-blanck | KPD | 14 | 70 | +0 | +0 | 70 | +0 | +0.00% |
| james-tunstill | MID | 41 | 82 | +0 | +0 | 82 | +0 | +0.00% |
| jamie-cripps | SF | 26 | 28 | +0 | +0 | 28 | +0 | +0.00% |
| jamie-elliott | SF | 39 | 19 | +0 | +0 | 19 | +0 | +0.00% |
| jaren-carr | SF | 63 | 65 | +0 | +0 | 65 | +0 | +0.00% |
| jed-adams | KPD | 38 | 154 | +0 | +0 | 154 | +0 | +0.00% |
| jed-bews | SD | 77 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| jesse-dattoli | SF | 22 | 318 | +0 | +0 | 318 | +0 | +0.00% |
| jesse-mellor | MID | pool | 84 | +0 | +0 | 84 | +0 | +0.00% |
| jevan-phillipou | SF | 35 | 273 | +0 | +0 | 273 | +0 | +0.00% |
| joe-pike | RUCK | 9 | 151 | +0 | +0 | 151 | +0 | +0.00% |
| joel-cochran | KPD | 47 | 161 | +0 | +0 | 161 | +0 | +0.00% |
| joel-hamling | KPF | 41 | 18 | +0 | +0 | 18 | +0 | +0.00% |
| jordan-boyd | SD | 17 | 55 | +0 | +0 | 55 | +0 | +0.00% |
| jordon-butts | KPD | 17 | 18 | +0 | +0 | 18 | +0 | +0.00% |
| josh-goater | SD | 22 | 93 | +0 | +0 | 93 | +0 | +0.00% |
| josh-smillie | MID | 7 | 953 | +0 | +0 | 953 | +0 | +0.00% |
| judson-clarke | SF | 30 | 90 | +0 | +0 | 90 | +0 | +0.00% |
| jy-farrar | KPF | 59 | 10 | +0 | +0 | 10 | +0 | +0.00% |
| kalani-white | KPF | pool | 84 | +0 | +0 | 84 | +0 | +0.00% |
| kaleb-smith | SD | 49 | 67 | +0 | +0 | 67 | +0 | +0.00% |
| kayle-gerreyn | KPF | 37 | 177 | +0 | +0 | 177 | +0 | +0.00% |
| keighton-matofai-forbes | SD | 69 | 104 | +0 | +0 | 104 | +0 | +0.00% |
| kobe-mcdonald | SD | pool | 85 | +0 | +0 | 85 | +0 | +0.00% |
| koby-coulson | MID | 46 | 316 | +0 | +0 | 316 | +0 | +0.00% |
| koby-evans | SF | 38 | 254 | +0 | +0 | 254 | +0 | +0.00% |
| kye-fincher | MID | 52 | 249 | +0 | +0 | 249 | +0 | +0.00% |
| lachie-sullivan | SF | pool | 86 | +0 | +0 | 86 | +0 | +0.00% |
| lachlan-blakiston | KPD | 12 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| lachlan-carmichael | SD | 21 | 548 | +0 | +0 | 548 | +0 | +0.00% |
| lachlan-fogarty | SF | 22 | 35 | +0 | +0 | 35 | +0 | +0.00% |
| lachlan-mcneil | SF | 6 | 20 | +0 | +0 | 20 | +0 | +0.00% |
| lachlan-weller | MID | 14 | 74 | +0 | +0 | 74 | +0 | +0.00% |
| laitham-vandermeer | SF | 37 | 20 | +0 | +0 | 20 | +0 | +0.00% |
| lance-collard | SF | 28 | 146 | +0 | +0 | 146 | +0 | +0.00% |
| latrelle-pickett | SF | 12 | 548 | +0 | +0 | 548 | +0 | +0.00% |
| lennox-hoffman | SD | 66 | 104 | +0 | +0 | 104 | +0 | +0.00% |
| leon-kickett | SF | 4 | 151 | +0 | +0 | 151 | +0 | +0.00% |
| lewis-hayes | KPD | 25 | 250 | +0 | +0 | 250 | +0 | +0.00% |
| liam-henry | SF | 9 | 63 | +0 | +0 | 63 | +0 | +0.00% |
| liam-hetherton | KPF | pool | 168 | +0 | +0 | 168 | +0 | +0.00% |
| liam-mcmahon | KPF | 33 | 135 | +0 | +0 | 135 | +0 | +0.00% |
| liam-puncher | KPD | 15 | 124 | +0 | +0 | 124 | +0 | +0.00% |
| liam-ryan | SF | 26 | 24 | +0 | +0 | 24 | +0 | +0.00% |
| liam-stocker | SD | 19 | 41 | +0 | +0 | 41 | +0 | +0.00% |
| lincoln-mccarthy | SF | 73 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| logan-smith | RUCK | 71 | 185 | +0 | +0 | 185 | +0 | +0.00% |
| lucas-camporeale | MID | 54 | 159 | +0 | +0 | 159 | +0 | +0.00% |
| lucca-grego | SD | 48 | 124 | +0 | +0 | 124 | +0 | +0.00% |
| luke-beecken | MID | 16 | 164 | +0 | +0 | 164 | +0 | +0.00% |
| luke-cleary | SD | 61 | 29 | +0 | +0 | 29 | +0 | +0.00% |
| luke-lloyd | KPD | 42 | 164 | +0 | +0 | 164 | +0 | +0.00% |
| luke-mcdonald | SD | 8 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| luke-pedlar | SF | 11 | 112 | +0 | +0 | 112 | +0 | +0.00% |
| luke-urquhart | MID | 57 | 143 | +0 | +0 | 143 | +0 | +0.00% |
| malcolm-rosas | SF | 14 | 25 | +0 | +0 | 25 | +0 | +0.00% |
| mani-liddy | MID | 15 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| mark-blicavs | MID | pool | 5 | +0 | +0 | 5 | +0 | +0.00% |
| mark-o-connor | SD | pool | 8 | +0 | +0 | 8 | +0 | +0.00% |
| mason-cox | KPF | pool | 3 | +0 | +0 | 3 | +0 | +0.00% |
| matt-duffy | SD | pool | 43 | +0 | +0 | 43 | +0 | +0.00% |
| matt-guelfi | SF | 75 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| matt-hill | SF | pool | 56 | +0 | +0 | 56 | +0 | +0.00% |
| matt-owies | SF | pool | 3 | +0 | +0 | 3 | +0 | +0.00% |
| matthew-leray | MID | 56 | 219 | +0 | +0 | 219 | +0 | +0.00% |
| maurice-rioli-1 | SF | 53 | 27 | +0 | +0 | 27 | +0 | +0.00% |
| max-beattie | SF | 12 | 181 | +0 | +0 | 181 | +0 | +0.00% |
| max-king-syd | SF | 49 | 156 | +0 | +0 | 156 | +0 | +0.00% |
| max-knobel | RUCK | 42 | 411 | +0 | +0 | 411 | +0 | +0.00% |
| max-mapley | RUCK | 18 | 322 | +0 | +0 | 322 | +0 | +0.00% |
| max-ramsden | KPF | 6 | 257 | +0 | +0 | 257 | +0 | +0.00% |
| mitch-podhajski | KPF | 17 | 399 | +0 | +0 | 399 | +0 | +0.00% |
| mitch-zadow | SF | pool | 139 | +0 | +0 | 139 | +0 | +0.00% |
| mitchell-knevitt | MID | 25 | 258 | +0 | +0 | 258 | +0 | +0.00% |
| mitchell-marsh | KPF | 22 | 506 | +0 | +0 | 506 | +0 | +0.00% |
| mykelti-lefau | KPF | pool | 86 | +0 | +0 | 86 | +0 | +0.00% |
| nathan-broad | SD | 65 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| nathan-wardius | SF | pool | 77 | +0 | +0 | 77 | +0 | +0.00% |
| ned-bowman | SF | 26 | 257 | +0 | +0 | 257 | +0 | +0.00% |
| nicholas-coffield | SD | 8 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| nicholas-holman | SF | 49 | 14 | +0 | +0 | 14 | +0 | +0.00% |
| nick-driscoll | MID | 6 | 201 | +0 | +0 | 201 | +0 | +0.00% |
| noah-answerth | SD | 55 | 12 | +0 | +0 | 12 | +0 | +0.00% |
| noah-chamberlain | SF | pool | 86 | +0 | +0 | 86 | +0 | +0.00% |
| oisin-mullin | SD | pool | 14 | +0 | +0 | 14 | +0 | +0.00% |
| oliver-griffin | SF | 6 | 181 | +0 | +0 | 181 | +0 | +0.00% |
| oliver-wiltshire | SF | 61 | 49 | +0 | +0 | 49 | +0 | +0.00% |
| ollie-lord | KPF | 51 | 105 | +0 | +0 | 105 | +0 | +0.00% |
| ollie-murphy | KPD | 41 | 168 | +0 | +0 | 168 | +0 | +0.00% |
| oscar-berry | KPD | pool | 53 | +0 | +0 | 53 | +0 | +0.00% |
| oskar-baker | MID | 48 | 14 | +0 | +0 | 14 | +0 | +0.00% |
| oskar-taylor | SD | 15 | 629 | +0 | +0 | 629 | +0 | +0.00% |
| paddy-cross | SF | pool | 139 | +0 | +0 | 139 | +0 | +0.00% |
| paddy-dow | MID | 3 | 158 | +0 | +0 | 158 | +0 | +0.00% |
| patrick-carr | RUCK | pool | 31 | +0 | +0 | 31 | +0 | +0.00% |
| patrick-dangerfield | SF | 10 | 63 | +0 | +0 | 63 | +0 | +0.00% |
| patrick-said | SF | 60 | 80 | +0 | +0 | 80 | +0 | +0.00% |
| patrick-snell | KPD | 53 | 115 | +0 | +0 | 115 | +0 | +0.00% |
| reece-torrent | MID | 64 | 79 | +0 | +0 | 79 | +0 | +0.00% |
| reef-mcinnes | KPD | 24 | 164 | +0 | +0 | 164 | +0 | +0.00% |
| rhys-stanley | RUCK | 47 | 28 | +0 | +0 | 28 | +0 | +0.00% |
| rhys-unwin | SF | 61 | 91 | +0 | +0 | 91 | +0 | +0.00% |
| riak-andrew | KPD | 55 | 138 | +0 | +0 | 138 | +0 | +0.00% |
| ricky-mentha | SF | pool | 50 | +0 | +0 | 50 | +0 | +0.00% |
| riley-onley | MID | 2 | 201 | +0 | +0 | 201 | +0 | +0.00% |
| river-stevens | SF | 67 | 104 | +0 | +0 | 104 | +0 | +0.00% |
| roan-steele | MID | 7 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| rob-monahan | SD | pool | 45 | +0 | +0 | 45 | +0 | +0.00% |
| robert-hansen | SF | 2 | 132 | +0 | +0 | 132 | +0 | +0.00% |
| ryan-gardner | KPD | 58 | 18 | +0 | +0 | 18 | +0 | +0.00% |
| ryan-lester | SD | 30 | 38 | +0 | +0 | 38 | +0 | +0.00% |
| ryda-luke | SF | pool | 84 | +0 | +0 | 84 | +0 | +0.00% |
| saad-el-hawli | SD | 13 | 118 | +0 | +0 | 118 | +0 | +0.00% |
| sam-allen | MID | 29 | 618 | +0 | +0 | 618 | +0 | +0.00% |
| sam-butler-1 | SF | 23 | 81 | +0 | +0 | 81 | +0 | +0.00% |
| sam-davidson | SF | 51 | 80 | +0 | +0 | 80 | +0 | +0.00% |
| sam-sturt | SF | 17 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| sam-switkowski | SF | 72 | 15 | +0 | +0 | 15 | +0 | +0.00% |
| sam-wicks | SD | pool | 10 | +0 | +0 | 10 | +0 | +0.00% |
| shadeau-brain | SD | pool | 120 | -1 | +1 | 120 | +0 | +0.00% |
| steele-sidebottom | MID | 11 | 96 | +0 | +0 | 96 | +0 | +0.00% |
| tai-hayes | SF | 44 | 194 | +0 | +0 | 194 | +0 | +0.00% |
| taylor-goad | RUCK | 20 | 730 | +0 | +0 | 730 | +0 | +0.00% |
| tew-jiath | SD | 37 | 167 | +0 | +0 | 167 | +0 | +0.00% |
| thomas-matthews | SF | 30 | 337 | +0 | +0 | 337 | +0 | +0.00% |
| toby-conway | RUCK | 24 | 503 | +0 | +0 | 503 | +0 | +0.00% |
| toby-pink | KPD | 33 | 31 | +0 | +0 | 31 | +0 | +0.00% |
| toby-whan | SF | pool | 84 | +0 | +0 | 84 | +0 | +0.00% |
| tobyn-murray | SF | 40 | 234 | +0 | +0 | 234 | +0 | +0.00% |
| tom-barrass | KPD | 43 | 21 | +0 | +0 | 21 | +0 | +0.00% |
| tom-blamires | SD | pool | 139 | +0 | +0 | 139 | +0 | +0.00% |
| tom-cole | SD | 36 | 47 | +0 | +0 | 47 | +0 | +0.00% |
| tom-edwards | KPF | pool | 108 | +0 | +0 | 108 | +0 | +0.00% |
| tom-lynch-1 | KPF | 11 | 50 | +0 | +0 | 50 | +0 | +0.00% |
| tyan-prindable | MID | 32 | 543 | +0 | +0 | 543 | +0 | +0.00% |
| tylah-williams | SF | 39 | 249 | +0 | +0 | 249 | +0 | +0.00% |
| tyler-welsh | KPF | 59 | 80 | +0 | +0 | 80 | +0 | +0.00% |
| vigo-visentini | RUCK | 5 | 182 | +0 | +0 | 182 | +0 | +0.00% |
| wil-parker | SD | pool | 24 | +0 | +0 | 24 | +0 | +0.00% |
| will-darcy | KPD | 58 | 187 | +0 | +0 | 187 | +0 | +0.00% |
| will-lewis | KPF | pool | 139 | +0 | +0 | 139 | +0 | +0.00% |
| xavier-o-halloran | SF | 22 | 47 | +0 | +0 | 47 | +0 | +0.00% |
| xavier-walsh | KPD | 6 | 143 | +0 | +0 | 143 | +0 | +0.00% |
| zac-banch | SF | 2 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| zac-mccarthy | KPF | 55 | 147 | +0 | +0 | 147 | +0 | +0.00% |
| zac-walker | SD | 11 | 152 | +0 | +0 | 152 | +0 | +0.00% |
| zak-evans | MID | pool | 29 | +0 | +0 | 29 | +0 | +0.00% |
| zane-zakostelsky | KPD | 51 | 209 | +0 | +0 | 209 | +0 | +0.00% |

---

*Levers 3 (v0 / curve re-print) and 4 (the numéraire scalar) are absent because they were never
built. `STOP_STEP3_GMONO.md` records why, with the engine's own halt transcript.*
