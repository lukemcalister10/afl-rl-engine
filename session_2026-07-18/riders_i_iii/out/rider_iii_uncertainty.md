# RIDER (iii) — uncertainty grading past ~p50
**REPORT-ONLY · finding, not a verdict · gross · no decile bands.**  
`stamps: code_sha=e4177c21934148c19d9cec3c015fee5d28480102 curve_payload=89c14729 store_base=968de0c7 per_entrant=40d7da7c (frozen @ e4177c2; read-only; asserted at load)`

**Declared grade:** `U(p) = RSS( sampling , generalization )`, kernel-smoothed over log-pick (bw=0.08) into a **continuous** curve — no bands. `sampling` = rider-(ii) RAW per-exact-pick cohort-bootstrap relative SD; `generalization` = rider-(i) leave-one-cohort-out residual half-width. The fit-vs-2003 gap is reported per pick as context but is thin (one held-out cohort) and does not drive the grade. The pick-99 sink is down-weighted (w=0.2) in the smoother — it is an aggregate, not a same-resolution exact pick.

**Headline:** the uncertainty grade is roughly flat and low across the top and rises steeply past ~p50 — deep-tail median **37%** vs top (p≤30) **17%**, about **2.2×** higher. Past ~p50 the curve should be read as a low-confidence region.

## Uncertainty grade by exact pick (past ~p50)
| pick | grade U(p) % | sampling (boot-SD) % | generalization (LOCO ½) % | fit-vs-2003 gap % | curve | raw n |
|---|---|---|---|---|---|---|
| 40 | 24.8 | 26.8 | 4.9 | 27.5 | 677 | 15 |
| 50 | 28.1 | 35.3 | 2.6 | 2.4 | 589 | 14 |
| 55 | 29.1 | 39.6 | 3.1 | 8.7 | 562 | 14 |
| 60 | 30.9 | 48.1 | 2.6 | 11.3 | 542 | 15 |
| 65 | 33.2 | 39.9 | 3.0 | 6.2 | 528 | 15 |
| 70 | 36.0 | 43.4 | 3.0 | 4.1 | 516 | 14 |
| 75 | 37.7 | 34.6 | 3.0 | 14.8 | 505 | 14 |
| 80 | 38.6 | 39.1 | 3.0 | 20.3 | 494 | 14 |
| 85 | 39.5 | 48.5 | 2.5 | 21.0 | 483 | 13 |
| 90 | 39.8 | 33.6 | 1.8 | 17.8 | 473 | 11 |
| 95 | 39.3 | 44.1 | 1.6 | 13.5 | 467 | 11 |
| 98 | 38.8 | 34.1 | 1.6 | 12.0 | 464 | 12 |
| 99 *(sink)* | 38.6 | 8.2 | 1.6 | 12.3 | 463 | 250 |

_Full 1–99 series in `rider_iii_uncertainty.json`; curve in `rider_iii_uncertainty.svg`._

## Finding (one plain sentence, no verdict)
A continuous uncertainty grade built from cohort-bootstrap and leave-one-cohort-out dispersion is low and flat across the top of the board and climbs steeply beyond ~p50 (about 2.2× the top by the deep tail), so the deep-tail region of the frozen curve carries materially less statistical support per exact pick than the top.
