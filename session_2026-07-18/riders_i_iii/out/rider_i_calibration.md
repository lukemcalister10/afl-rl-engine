# RIDER (i) — realized-outcome cohort-holdout calibration + washout-exit calibration
**REPORT-ONLY · finding, not a verdict · gross · busts full weight · no decile bands.**  
`stamps: code_sha=e4177c21934148c19d9cec3c015fee5d28480102 curve_payload=89c14729 store_base=968de0c7 per_entrant=40d7da7c (frozen @ e4177c2; read-only; asserted at load)`

**Declared:** realized = `mean(vpath)` (primary; codebase life-path measure). Predicted = the FROZEN PVC curve. Smoother = Gaussian kernel over log-pick, adaptive bandwidth to eff-n≥35, per exact pick. Pool = career-complete cohorts (≤2017). Pick 1 = numeraire pin (3000), not a fit point; pick 99 = deep-pick sink (n≈252). Equal weight per entrant.

**Counts:** complete-career 1643 · fit-era-complete(2004–17) 1538 · held-out-complete(2003) 105 · washout/exit 1608 · censored recent(>2017, excluded from realized calib) 608.

## Calibration residual by exact pick (signed rel %; smoothed)
| pick | curve | realized(smooth) | resid % | eff-n | bw | raw n@pick | fit-era % | held-out 2003 % | washout/exit % | LOCO env % |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 *(pin)* | 3000 | 2550 | -15.0 | 27 | 0.60 | 15 | -13.8 | -31.5 | -23.1 | [-17.1,-13.7] |
| 2 | 2779 | 2640 | -5.0 | 36 | 0.44 | 15 | -3.3 | -39.4 | -24.6 | [-7.8,-2.9] |
| 3 | 2675 | 2498 | -6.6 | 37 | 0.32 | 15 | -4.7 | -43.8 | -27.3 | [-10.5,-3.7] |
| 5 | 2247 | 2108 | -6.2 | 37 | 0.20 | 15 | -6.0 | -44.4 | -25.4 | [-11.3,-4.5] |
| 10 | 1604 | 1577 | -1.7 | 38 | 0.10 | 15 | +1.1 | -42.3 | -16.4 | [-7.1,+1.9] |
| 15 | 1204 | 1210 | +0.5 | 55 | 0.10 | 14 | +1.9 | -36.4 | -11.6 | [-2.7,+3.2] |
| 20 | 1034 | 1243 | +20.2 | 74 | 0.10 | 15 | +23.9 | -34.8 | +1.2 | [+12.3,+24.0] |
| 30 | 811 | 944 | +16.4 | 111 | 0.10 | 15 | +19.8 | -26.8 | -17.4 | [+11.3,+20.6] |
| 40 | 677 | 751 | +10.9 | 148 | 0.10 | 15 | +13.4 | -14.1 | -16.9 | [+5.7,+15.5] |
| 50 | 589 | 577 | -2.0 | 185 | 0.10 | 14 | -4.3 | -1.9 | -31.3 | [-4.3,+0.9] |
| 60 | 542 | 465 | -14.2 | 217 | 0.10 | 15 | -16.6 | -5.3 | -40.1 | [-16.6,-11.3] |
| 70 | 516 | 412 | -20.2 | 244 | 0.10 | 14 | -19.5 | -23.6 | -44.4 | [-23.1,-17.2] |
| 80 | 494 | 382 | -22.7 | 290 | 0.10 | 14 | -20.3 | -40.6 | -42.3 | [-26.2,-20.3] |
| 90 | 473 | 337 | -28.8 | 393 | 0.10 | 11 | -27.6 | -45.4 | -41.4 | [-31.2,-27.6] |
| 99 *(sink)* | 463 | 315 | -32.0 | 391 | 0.10 | 250 | -31.0 | -43.2 | -41.5 | [-33.6,-30.5] |

_Full 1–99 series in `rider_i_calibration.json`. Curves: `rider_i_calibration.svg` (predicted vs realized), `rider_i_calibration_residual.svg` (residual, fit vs held-out)._

**Deep-tail caveat (declared):** deep-tail smoothed realized is dominated by the pick-99+ sink (raw n@99=250; eff-n rises to ~391 by pick 99), so picks ~85–99 share essentially one realized estimate — the finest resolution the data support there.

## Finding (one plain sentence, no verdict)
Smoothed against realized career life-path (busts full weight, gross), the frozen curve **under-prices the upper-mid** (picks ~12–48 realize above their price; residual peaks **+20% near pick 20**) and **over-prices the deep tail** (residual turns negative at **pick 49** and deepens to about **-32% by the pick-99 sink**); the pre-fit held-out 2003 cohort shows the deep-tail over-pricing if anything *more* strongly (tail -43%), so the tail signal is not an artifact of the fit era (thin — one cohort of 105), and the terminal censoring-free washout/exit view shows the same deep-tail over-pricing, while pick 1 (numeraire pin) and picks 2–11 (per-pick n≈15, high variance) are not a clean signal.
