# RUCK VALUES DERIVED OFF PRODUCTION — before→after (BATCH2, 2026-07-06)
Engine (candidate) — production-derived ceiling replaces 1.4×PVC on the ruck production leg.
Ceiling: HEAD=0.8 × synthprice_RUC(bestlvl) at refpk=72 (grid $885..$11804). No-production rucks (bestlvl=0) → prior cap (byte-exact).

## SINGLE-LEVER: non-ruck moved = **0** (must be 0); rucks moved = **7**/217

## Ruck $ — moved rucks + anchors + top rucks (before → after)
| ruck | pick | bestlvl | OLD $ | NEW $ | Δ |
|---|--:|--:|--:|--:|--:|
| Luke Jackson | 3 | 120.8 | 6803 | 6803 | +0 |
| Tristan Xerri | 71 | 131.1 | 5795 | 5795 | +0 |
| Brodie Grundy | 22 | 129.3 | 3314 | 3314 | +0 |
| Timothy English | 19 | 130.7 | 2916 | 2916 | +0 |
| Kieren Briggs | 34 | 107.4 | 2145 | 2145 | +0 |
| Max Gawn | 33 | 134.2 | 2112 | 2112 | +0 |
| Jordon Sweet | 16 | 100.7 | 2026 | 2026 | +0 |
| Toby Nankervis | 35 | 112.9 | 1806 | 1806 | +0 |
| Bailey J. Williams | 35 | 93.9 | 1704 | 1704 | +0 |
| Tom De Koning | 30 | 104.0 | 1678 | 1678 | +0 |
| Ned Moyle | 5 | 87.9 | 1598 | 1598 | +0 |
| Nick Madden | None | 0.0 | 1464 | 1464 | +0 |
| Sean Darcy *moved* | 38 | 120.2 | 826 | 948 | +122 |
| Reilly O'Brien *moved* | 8 | 104.0 | 618 | 783 | +165 |
| Louis Emmett **(anchor)** | 27 | 32.8 | 855 | 724 | -131 |
| Rowan Marshall *moved* | 9 | 118.7 | 431 | 612 | +181 |
| Samson Ryan *moved* | 42 | 55.4 | 569 | 581 | +12 |
| Jarrod Witts *moved* | 81 | 112.3 | 375 | 384 | +9 |
| Oliver Hayes-Brown *moved* | None | 49.6 | 319 | 335 | +16 |
| Nicholas Naitanui **(anchor)** | 2 | 117.5 | 23 | 23 | +0 |

## Cross-position SANITY (active players; ruck $ vs active non-ruck $ at bestlvl ±12) — FLAG only, NOT calibration
| ruck | bestlvl | ruck $ | non-ruck q75 | ratio | moved by this lever? |
|---|--:|--:|--:|--:|:--:|
| Luke Jackson | 120.8 | 6803 | 3414 | 1.99 | no (byte-exact) |
| Tristan Xerri | 131.1 | 5795 | 3301 | 1.76 | no (byte-exact) |
| Mitchell Edwards | 50.8 | 1359 | 786 | 1.73 | no (byte-exact) |
| Jarrod Witts | 112.3 | 384 | 3171 | 0.12 | YES |
| Darcy Fort | 81.8 | 83 | 1502 | 0.06 | no (byte-exact) |
| Rhys Stanley | 94.5 | 30 | 1832 | 0.02 | no (byte-exact) |
