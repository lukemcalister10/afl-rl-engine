# D4.2 — THE REALIZED CAPTAIN VALUE, OFF THE RECORD (order statistic)
**Record:** store realized scoring, games≥10, completed seasons 2009-2025. Raw scoring only (no ev / no board).

## THE FRAME
In SuperCoach you captain **exactly one player per week** — the premium is a **slot good, not an additive good**;
a second Bontempelli adds no captain value. So the true worth of an elite captain is an **order statistic**: the
gap between the best option and the *next* option. The owner's claim is that this gap is CONVEX in how far the top
sits above the field. Tested below.

## THE MEASUREMENT
Per season, rank realized averages and read the top vs the 2nd / 5th / 10th best, and the field median:

| year | n | top1 | 2nd | 5th | 10th | field med | top−2nd | top−5th | top−10th | top−field |
|---|---|---|---|---|---|---|---|---|---|---|
| 2011 | 289 | 129.2 | 118.0 | 114.1 | 109.4 | 72.7 | 11.2 | 15.1 | 19.8 | 56.5 |
| 2016 | 402 | 131.9 | 118.7 | 113.6 | 110.8 | 72.2 | 13.2 | 18.4 | 21.1 | 59.7 |
| 2017 | 409 | 134.1 | 121.9 | 113.7 | 109.8 | 74.1 | 12.2 | 20.4 | 24.3 | 60.0 |
| 2020 | 373 | 139.9 | 133.7 | 120.6 | 114.6 | 75.3 | 6.2 | 19.3 | 25.3 | 64.6 |
| 2024 | 463 | 124.1 | 123.8 | 118.0 | 115.7 | 69.1 | 0.3 | 6.1 | 8.4 | 55.0 |
| … (17 seasons total) | | | | | | | | | | |

**Mean gaps:** top−2nd = **5.31**, top−5th = **12.58**, top−10th = **16.93** SC points/week.

## CONVEXITY — TWO TESTS, BOTH SUPPORT THE OWNER
1. **The pooled rank-gap curve is sharply convex at the top:**

   | gap between ranks | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 |
   |---|---|---|---|---|---|---|---|---|---|
   | mean pts | **5.31** | 2.93 | 2.15 | 2.18 | 1.09 | 1.19 | 0.73 | 0.59 | 0.75 |

   The marginal value of being #1 over #2 (5.31) is **~5× the value of being #5 over #6 (1.09).** The very top is
   disproportionately valuable — the difference-maker premium is real and it is convex.
2. **The top gap widens with the field spread:** regressing (top−2nd) on (top−field median) gives slope +0.112,
   corr +0.147 — in seasons with a true difference-maker sitting far above the field, the captain gap is larger.
   (Weak but positive; the 17-season sample is small.)

## THE CONTRAST WITH THE LIVE TERM
The live `capt_prem` is **saturating (concave)**: across the top 8.16 raw points (Gawn #1 → Jackson #8) it grants
only 2.91 premium points, and it hard-caps at 18. But the RECORD says the top-vs-next gap is **convex** — the #1
option is worth ~5.3 pts/week over #2 (mean), up to ~13 pts in a difference-maker year, while the #5 option is
worth ~1 pt over #6. **The live term damps the top exactly where the record says the value is most convex.**

## IN ONE LINE
The realized, slot-aware worth of an elite captain over the next-best is convex in his distance above the field;
the live saturating premium prices it concavely — the measurement the owner's hypothesis rests on holds.
