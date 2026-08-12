# PAR-FIX MOVERS LEDGER — the par separation fix, every board row that moves

**Lever:** the par arm-split separation fix — `engine/forward_valuation/par_build.py` +
`par_redesign.py`, PR #457, `build/nd-pool-separation` `78d5c38`.
**Adopted:** owner ruling 2026-08-12 (*"Yes, adopt."*), issue #334 comment `5261191193`, on ORDER
20B's evidence packet. **Landed:** ORDER 20C, branch `land/par-fix-adoption`.

**Board `94f1fec59f99c59d5890d5975c79fa9b` → `1dbd1480a34c7823f330273211cbb76a`.**

This is the lever's record. One lever, one ledger — the owner's standing attribution requirement.
Every row below is a board row whose value `v` changed when the fix was applied, with nothing else
changed: same store (`d9a24282`), same config (`cd38fb00`), same frozen pickles, same shipped
defaults. Both boards were rebuilt on the landing tree by ORDER 20B's own harness; the control
reproduced the live board `94f1fec5` byte-identical before the fix was applied.

Arm predicate is ORDER 20's, verbatim: **NATIONAL** = `ty=='ND' and ep<=64`; **POOL** = everything
else. Values are board `v` (numéraire-rebased SCAR), integers as exported.

## Totals

| arm | rows | movers | total before | total after | delta | pct |
|---|---:|---:|---:|---:|---:|---:|
| NATIONAL | 668 | 279 | 624418 | 622650 | -1768 | -0.2831% |
| POOL | 334 | 195 | 123939 | 126244 | +2305 | +1.8598% |

**474 ledger rows** (279 national + 195 pool). The national side is the one-time de-contamination —
pool rows leaving the national fit — and it is a *fall* of −1,768 (−0.28%). The pool side rises
+2,305 (+1.86%) as those rows are priced on their own arm. The national pick curve does **not**
move: 0 of 64 PVC points, 0 of 64 `picks[]`, pick 1 = 3000 (the numéraire law holds).

## Whole-board attribution by par channel (ORDER 20B)

Source: `docs/evidence/par_adoption_2026-08-12/movers/CHANNEL_DECOMP.json`. Two independent
decompositions — one-at-a-time (switch one channel to the fixed arm split) and leave-one-out
(switch all but one). Units are national-arm board points.

| channel | one-at-a-time | leave-one-out |
|---|---:|---:|
| `ISO` | +1651 | +1539 |
| `POLE` | -1196 | -1315 |
| `BLEND` | -1563 | -1573 |
| `BAR` | +4 | +2 |
| `BASE` | 0 | 0 |
| `LVLPAR` | -545 | -547 |
| **residual** | -119 | +126 |
| **board total** | -1768 | |

Two findings the owner should keep in view, both ORDER 20B's:

1. **`BASE_RATE` contributes EXACTLY ZERO** — on the whole board and on every decomposed mover.
   It has no board consumer outside `par_redesign.py`'s own `__main__` report block.
2. **`LVLPAR` (`par_redesign.lvl_par:126`) carries −545 of the −1,768** — roughly a third of the
   national move — and it is a par consumer ORDER 20's sixteen-site sweep never named. It is the
   highest-traffic par consumer on the board (38,159 calls).

## The named large movers, decomposed per channel

The seven movers ORDER 20B decomposed. `oaat` = one-at-a-time, `loo` = leave-one-out.

| player | arm | pos | pick | before | after | delta | `ISO` | `POLE` | `BLEND` | `BAR` | `BASE` | `LVLPAR` |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Harry Dean** | NATIONAL | KPD | 3 | 2815 | 2577 | -238 (-8.45%) | +21 / +23 | 0 / +3 | -251 / -262 | 0 / 0 | 0 / 0 | 0 / -9 |
| **Angus Clarke** | NATIONAL | SD | 39 | 680 | 555 | -125 (-18.38%) | +13 / +10 | -82 / -107 | -29 / -46 | 0 / 0 | 0 / 0 | -3 / +1 |
| **Harvey Johnston** | NATIONAL | SD | 49 | 224 | 329 | +105 (+46.88%) | +11 / +13 | +1 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | +92 / +94 |
| **Willem Duursma** | NATIONAL | MID | 1 | 4067 | 3977 | -90 (-2.21%) | +9 / +10 | 0 / 0 | -70 / -99 | 0 / 0 | 0 / 0 | 0 / -29 |
| **James Leake** | NATIONAL | SD | 17 | 476 | 563 | +87 (+18.28%) | +16 / +19 | +3 / +3 | 0 / 0 | 0 / 0 | 0 / 0 | +66 / +68 |
| **Will Hayes** | NATIONAL | SF | 56 | 461 | 378 | -83 (-18.00%) | +11 / +9 | -23 / -22 | 0 / 0 | 0 / 0 | 0 / 0 | -71 / -71 |
| **Luke Cleary** | NATIONAL | SD | 61 | 37 | 29 | -8 (-21.62%) | 0 / 0 | -5 / -4 | -5 / -3 | 0 / 0 | 0 / 0 | -1 / 0 |

Channel cells read `oaat / loo`. Residual (the interaction the single-channel probes cannot see) is
carried per player in the `.json` sidecar.

## NATIONAL — all 279 movers

Sorted by absolute move, largest first. `ty` = intake type, `pk` = draft pick, `ep` = effective
pick (the board's arm key).

| # | player | ty | pk | ep | before | after | delta | pct |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Harry Dean | ND | 3 | 3 | 2815 | 2577 | -238 | -8.45% |
| 2 | Ty Gallop | ND | 42 | 42 | 1355 | 1199 | -156 | -11.51% |
| 3 | Christian Moraes | ND | 38 | 38 | 1043 | 906 | -137 | -13.14% |
| 4 | Jacob Farrow | ND | 10 | 10 | 2734 | 2601 | -133 | -4.86% |
| 5 | Dyson Sharp | ND | 13 | 13 | 3216 | 3091 | -125 | -3.89% |
| 6 | Angus Clarke | ND | 39 | 39 | 680 | 555 | -125 | -18.38% |
| 7 | Matthew Roberts | ND | 34 | 34 | 1940 | 1818 | -122 | -6.29% |
| 8 | Lachie Jaques | ND | 29 | 29 | 843 | 725 | -118 | -14.00% |
| 9 | Jai Serong | ND | 53 | 53 | 1346 | 1233 | -113 | -8.40% |
| 10 | Joe Berry | ND | 15 | 15 | 1365 | 1259 | -106 | -7.77% |
| 11 | Harvey Johnston | ND | 49 | 49 | 224 | 329 | +105 | +46.88% |
| 12 | Willem Duursma | ND | 1 | 1 | 4067 | 3977 | -90 | -2.21% |
| 13 | James Leake | ND | 17 | 17 | 476 | 563 | +87 | +18.28% |
| 14 | Harrison Oliver | ND | 19 | 19 | 613 | 528 | -85 | -13.87% |
| 15 | Hugh Boxshall | ND | 45 | 45 | 1049 | 965 | -84 | -8.01% |
| 16 | Will Hayes | ND | 56 | 56 | 461 | 378 | -83 | -18.00% |
| 17 | Josh Lindsay | ND | 19 | 19 | 2412 | 2335 | -77 | -3.19% |
| 18 | Harvey Thomas | ND | 59 | 59 | 2318 | 2247 | -71 | -3.06% |
| 19 | Jase Burgoyne | ND | 60 | 60 | 2617 | 2549 | -68 | -2.60% |
| 20 | Jasper Alger | ND | 58 | 58 | 500 | 434 | -66 | -13.20% |
| 21 | Kane McAuliffe | ND | 40 | 40 | 1376 | 1312 | -64 | -4.65% |
| 22 | Jack Williams | ND | 57 | 57 | 478 | 415 | -63 | -13.18% |
| 23 | Noah Mraz | ND | 35 | 35 | 1707 | 1769 | +62 | +3.63% |
| 24 | Jack Ough | ND | 36 | 36 | 741 | 687 | -54 | -7.29% |
| 25 | Calsher Dear | ND | 56 | 56 | 945 | 892 | -53 | -5.61% |
| 26 | Jay Polkinghorne | ND | 44 | 44 | 349 | 297 | -52 | -14.90% |
| 27 | Tobie Travaglia | ND | 8 | 8 | 734 | 685 | -49 | -6.68% |
| 28 | Liam Fawcett | ND | 43 | 43 | 503 | 454 | -49 | -9.74% |
| 29 | Luke Trainor | ND | 21 | 21 | 1599 | 1551 | -48 | -3.00% |
| 30 | Jack Whitlock | ND | 33 | 33 | 1225 | 1271 | +46 | +3.76% |
| 31 | Talor Byrne | ND | 45 | 45 | 899 | 857 | -42 | -4.67% |
| 32 | Sam Darcy | ND | 2 | 2 | 5211 | 5250 | +39 | +0.75% |
| 33 | Sam Lalor | ND | 1 | 1 | 4052 | 4087 | +35 | +0.86% |
| 34 | Charlie West | ND | 50 | 50 | 658 | 692 | +34 | +5.17% |
| 35 | Jack Ison | ND | 47 | 47 | 544 | 512 | -32 | -5.88% |
| 36 | Connor O'Sullivan | ND | 11 | 11 | 2890 | 2920 | +30 | +1.04% |
| 37 | Jedd Busslinger | ND | 13 | 13 | 886 | 916 | +30 | +3.39% |
| 38 | Max Kondogiannis | ND | 36 | 36 | 465 | 435 | -30 | -6.45% |
| 39 | Jai Murray | ND | 17 | 17 | 1167 | 1138 | -29 | -2.48% |
| 40 | Billy Wilson | ND | 34 | 34 | 954 | 983 | +29 | +3.04% |
| 41 | Nick Bryan | ND | 37 | 37 | 749 | 778 | +29 | +3.87% |
| 42 | Finn O'Sullivan | ND | 2 | 2 | 3768 | 3740 | -28 | -0.74% |
| 43 | Mitchell Edwards | ND | 32 | 32 | 2411 | 2439 | +28 | +1.16% |
| 44 | Campbell Chesser | ND | 14 | 14 | 302 | 330 | +28 | +9.27% |
| 45 | Isaac Kako | ND | 13 | 13 | 1439 | 1413 | -26 | -1.81% |
| 46 | Beau Addinsall | ND | 18 | 18 | 1495 | 1521 | +26 | +1.74% |
| 47 | Sullivan Robey | ND | 9 | 9 | 3003 | 2981 | -22 | -0.73% |
| 48 | Xavier Lindsay | ND | 11 | 11 | 2128 | 2106 | -22 | -1.03% |
| 49 | Lachy Dovaston | ND | 16 | 16 | 490 | 512 | +22 | +4.49% |
| 50 | Cody Curtin | ND | 43 | 43 | 449 | 427 | -22 | -4.90% |
| 51 | Riley Bice | ND | 41 | 41 | 295 | 274 | -21 | -7.12% |
| 52 | Hugo Garcia | ND | 50 | 50 | 3082 | 3062 | -20 | -0.65% |
| 53 | Dylan Patterson | ND | 5 | 5 | 1648 | 1628 | -20 | -1.21% |
| 54 | Luke Kennedy | ND | 62 | 62 | 304 | 284 | -20 | -6.58% |
| 55 | Jagga Smith | ND | 3 | 3 | 4836 | 4855 | +19 | +0.39% |
| 56 | Alix Tauru | ND | 10 | 10 | 1665 | 1684 | +19 | +1.14% |
| 57 | Xavier Taylor | ND | 11 | 11 | 821 | 802 | -19 | -2.31% |
| 58 | Leo Lombard | ND | 9 | 9 | 1938 | 1957 | +19 | +0.98% |
| 59 | Leek Aleer | ND | 15 | 15 | 213 | 231 | +18 | +8.45% |
| 60 | Oliver Hannaford | ND | 18 | 18 | 415 | 398 | -17 | -4.10% |
| 61 | Archie Roberts | ND | 54 | 54 | 4742 | 4726 | -16 | -0.34% |
| 62 | Jacob Van Rooyen | ND | 19 | 19 | 1878 | 1894 | +16 | +0.85% |
| 63 | Harvey Langford | ND | 6 | 6 | 2641 | 2657 | +16 | +0.61% |
| 64 | Phoenix Gothard | ND | 12 | 12 | 1875 | 1891 | +16 | +0.85% |
| 65 | Steely Green | ND | 55 | 55 | 166 | 150 | -16 | -9.64% |
| 66 | Zach Reid | ND | 10 | 10 | 1078 | 1093 | +15 | +1.39% |
| 67 | Thomas Sims | ND | 28 | 28 | 568 | 583 | +15 | +2.64% |
| 68 | Josh Dolan | ND | 31 | 31 | 516 | 501 | -15 | -2.91% |
| 69 | Jason Horne-Francis | ND | 1 | 1 | 6028 | 6042 | +14 | +0.23% |
| 70 | Harry Armstrong | ND | 23 | 23 | 606 | 620 | +14 | +2.31% |
| 71 | Lachlan Cowan | ND | 30 | 30 | 738 | 724 | -14 | -1.90% |
| 72 | Noah Roberts-Thomson | ND | 54 | 54 | 227 | 213 | -14 | -6.17% |
| 73 | Cooper Duff-Tytler | ND | 4 | 4 | 1574 | 1561 | -13 | -0.83% |
| 74 | William McCabe | ND | 19 | 19 | 586 | 599 | +13 | +2.22% |
| 75 | Jhye Clark | ND | 8 | 8 | 1046 | 1059 | +13 | +1.24% |
| 76 | Samuel Swadling | ND | 37 | 37 | 763 | 776 | +13 | +1.70% |
| 77 | Hussien El Achkar | ND | 53 | 53 | 340 | 353 | +13 | +3.82% |
| 78 | Murphy Reid | ND | 17 | 17 | 4129 | 4141 | +12 | +0.29% |
| 79 | Taj Hotton | ND | 12 | 12 | 2367 | 2355 | -12 | -0.51% |
| 80 | Elijah Tsatas | ND | 5 | 5 | 1228 | 1240 | +12 | +0.98% |
| 81 | Angus Anderson | ND | 57 | 57 | 177 | 165 | -12 | -6.78% |
| 82 | Rhett Bazzo | ND | 37 | 37 | 464 | 476 | +12 | +2.59% |
| 83 | Will Lorenz | ND | 57 | 57 | 296 | 284 | -12 | -4.05% |
| 84 | Mac Andrew | ND | 5 | 5 | 4158 | 4169 | +11 | +0.26% |
| 85 | Caiden Cleary | ND | 24 | 24 | 460 | 471 | +11 | +2.39% |
| 86 | Neil Erasmus | ND | 10 | 10 | 1015 | 1026 | +11 | +1.08% |
| 87 | Logan Morris | ND | 31 | 31 | 3237 | 3247 | +10 | +0.31% |
| 88 | Nate Caddy | ND | 10 | 10 | 1852 | 1862 | +10 | +0.54% |
| 89 | Wil Dawson | ND | 22 | 22 | 515 | 525 | +10 | +1.94% |
| 90 | Harry Rowston | ND | 16 | 16 | 777 | 787 | +10 | +1.29% |
| 91 | Shannon Neale | ND | 35 | 35 | 2702 | 2711 | +9 | +0.33% |
| 92 | Jonty Faull | ND | 14 | 14 | 998 | 989 | -9 | -0.90% |
| 93 | Bailey Humphrey | ND | 6 | 6 | 2564 | 2573 | +9 | +0.35% |
| 94 | Cameron Mackenzie | ND | 7 | 7 | 2242 | 2251 | +9 | +0.40% |
| 95 | Joe Richards | ND | 48 | 48 | 924 | 915 | -9 | -0.97% |
| 96 | Max Gruzewski | ND | 22 | 22 | 617 | 626 | +9 | +1.46% |
| 97 | Reuben Ginbey | ND | 9 | 9 | 2341 | 2349 | +8 | +0.34% |
| 98 | Sam Cumming | ND | 7 | 7 | 2280 | 2288 | +8 | +0.35% |
| 99 | Joel Freijah | ND | 45 | 45 | 2891 | 2883 | -8 | -0.28% |
| 100 | Ethan Read | ND | 9 | 9 | 1016 | 1024 | +8 | +0.79% |
| 101 | Jordan Croft | ND | 15 | 15 | 1040 | 1048 | +8 | +0.77% |
| 102 | Matthew Jefferson | ND | 15 | 15 | 397 | 405 | +8 | +2.02% |
| 103 | Noah Long | ND | 57 | 57 | 132 | 124 | -8 | -6.06% |
| 104 | Luke Cleary | ND | 61 | 61 | 37 | 29 | -8 | -21.62% |
| 105 | Zeke Uwland | ND | 2 | 2 | 2626 | 2633 | +7 | +0.27% |
| 106 | Mitchito Owens | ND | 33 | 33 | 2064 | 2071 | +7 | +0.34% |
| 107 | Darcy Jones | ND | 21 | 21 | 1137 | 1144 | +7 | +0.62% |
| 108 | George Wardlaw | ND | 4 | 4 | 3229 | 3235 | +6 | +0.19% |
| 109 | Cooper Hynes | ND | 20 | 20 | 1537 | 1543 | +6 | +0.39% |
| 110 | Jake Rogers | ND | 14 | 14 | 581 | 587 | +6 | +1.03% |
| 111 | Jack Dalton | ND | 34 | 34 | 431 | 437 | +6 | +1.39% |
| 112 | Jacob Konstanty | ND | 20 | 20 | 175 | 181 | +6 | +3.43% |
| 113 | Charlie Banfield | ND | 41 | 41 | 542 | 536 | -6 | -1.11% |
| 114 | Elijah Hollands | ND | 7 | 7 | 704 | 710 | +6 | +0.85% |
| 115 | Dante Visentini | ND | 56 | 56 | 1268 | 1274 | +6 | +0.47% |
| 116 | Harry Sharp | ND | 45 | 45 | 149 | 155 | +6 | +4.03% |
| 117 | Samson Ryan | ND | 42 | 42 | 296 | 302 | +6 | +2.03% |
| 118 | Lachlan Ash | ND | 4 | 4 | 5733 | 5728 | -5 | -0.09% |
| 119 | Koltyn Tholstrup | ND | 13 | 13 | 1693 | 1698 | +5 | +0.30% |
| 120 | Cameron Nairn | ND | 20 | 20 | 601 | 606 | +5 | +0.83% |
| 121 | Louis Emmett | ND | 27 | 27 | 754 | 749 | -5 | -0.66% |
| 122 | Marcus Windhager | ND | 47 | 47 | 1869 | 1864 | -5 | -0.27% |
| 123 | Archer Reid | ND | 30 | 30 | 757 | 762 | +5 | +0.66% |
| 124 | Tom Gross | ND | 46 | 46 | 465 | 460 | -5 | -1.08% |
| 125 | Brady Hough | ND | 31 | 31 | 297 | 292 | -5 | -1.68% |
| 126 | Jack Carroll | ND | 43 | 43 | 85 | 80 | -5 | -5.88% |
| 127 | Riley Thilthorpe | ND | 2 | 2 | 4464 | 4468 | +4 | +0.09% |
| 128 | Nick Watson | ND | 5 | 5 | 3835 | 3839 | +4 | +0.10% |
| 129 | Darcy Wilson | ND | 18 | 18 | 3220 | 3224 | +4 | +0.12% |
| 130 | Nick Blakey | ND | 10 | 10 | 4277 | 4273 | -4 | -0.09% |
| 131 | Jed Walter | ND | 3 | 3 | 1435 | 1439 | +4 | +0.28% |
| 132 | Sid Draper | ND | 4 | 4 | 1246 | 1250 | +4 | +0.32% |
| 133 | Josh Battle | ND | 39 | 39 | 2024 | 2028 | +4 | +0.20% |
| 134 | Zane Duursma | ND | 4 | 4 | 811 | 815 | +4 | +0.49% |
| 135 | Aidan Schubert | ND | 23 | 23 | 485 | 481 | -4 | -0.82% |
| 136 | Riley Hardeman | ND | 23 | 23 | 262 | 258 | -4 | -1.53% |
| 137 | Joseph Fonti | ND | 44 | 44 | 592 | 596 | +4 | +0.68% |
| 138 | Bodie Ryan | ND | 46 | 46 | 214 | 210 | -4 | -1.87% |
| 139 | Hugh Bond | ND | 50 | 50 | 149 | 153 | +4 | +2.68% |
| 140 | Oscar Adams | ND | 51 | 51 | 75 | 79 | +4 | +5.33% |
| 141 | Harry Sheezel | ND | 3 | 3 | 11761 | 11764 | +3 | +0.03% |
| 142 | Josh Worrell | ND | 28 | 28 | 3720 | 3723 | +3 | +0.08% |
| 143 | Jye Amiss | ND | 8 | 8 | 1492 | 1495 | +3 | +0.20% |
| 144 | Jordan Clark | ND | 15 | 15 | 3267 | 3264 | -3 | -0.09% |
| 145 | Lachie Whitfield | ND | 1 | 1 | 2226 | 2223 | -3 | -0.13% |
| 146 | Jaspa Fletcher | ND | 12 | 12 | 2613 | 2616 | +3 | +0.11% |
| 147 | Daniel Annable | ND | 6 | 6 | 1398 | 1395 | -3 | -0.21% |
| 148 | Harris Andrews | ND | 60 | 60 | 1620 | 1623 | +3 | +0.19% |
| 149 | Tom McCartin | ND | 33 | 33 | 1686 | 1689 | +3 | +0.18% |
| 150 | Harry Kyle | ND | 14 | 14 | 1155 | 1158 | +3 | +0.26% |
| 151 | Bo Allan | ND | 16 | 16 | 1131 | 1128 | -3 | -0.27% |
| 152 | Matt Whitlock | ND | 27 | 27 | 375 | 372 | -3 | -0.80% |
| 153 | Zane Peucker | ND | 31 | 31 | 381 | 384 | +3 | +0.79% |
| 154 | Josh Gibcus | ND | 9 | 9 | 251 | 254 | +3 | +1.20% |
| 155 | Joel Jeffrey | ND | 30 | 30 | 1576 | 1579 | +3 | +0.19% |
| 156 | Isaac Keeler | ND | 44 | 44 | 170 | 173 | +3 | +1.76% |
| 157 | Heath Chapman | ND | 14 | 14 | 457 | 460 | +3 | +0.66% |
| 158 | Brandon Walker | ND | 52 | 52 | 60 | 57 | -3 | -5.00% |
| 159 | Will Ashcroft | ND | 2 | 2 | 7328 | 7330 | +2 | +0.03% |
| 160 | Finn Callaghan | ND | 3 | 3 | 6060 | 6062 | +2 | +0.03% |
| 161 | Jake Bowey | ND | 22 | 22 | 4321 | 4319 | -2 | -0.05% |
| 162 | Levi Ashcroft | ND | 5 | 5 | 3521 | 3519 | -2 | -0.06% |
| 163 | Aaron Cadman | ND | 1 | 1 | 1767 | 1769 | +2 | +0.11% |
| 164 | Bailey Dale | ND | 45 | 45 | 2257 | 2255 | -2 | -0.09% |
| 165 | Josh Daicos | ND | 57 | 57 | 2106 | 2104 | -2 | -0.10% |
| 166 | Taylor Goad | ND | 20 | 20 | 728 | 730 | +2 | +0.27% |
| 167 | Mattaes Phillipou | ND | 10 | 10 | 2279 | 2281 | +2 | +0.09% |
| 168 | Joshua Weddle | ND | 18 | 18 | 1508 | 1510 | +2 | +0.13% |
| 169 | Lawson Humphries | ND | 63 | 63 | 1814 | 1816 | +2 | +0.11% |
| 170 | Jobe Shanahan | ND | 30 | 30 | 1741 | 1739 | -2 | -0.11% |
| 171 | Jacob Weitering | ND | 1 | 1 | 1011 | 1013 | +2 | +0.20% |
| 172 | Sam Marshall | ND | 25 | 25 | 702 | 704 | +2 | +0.28% |
| 173 | Sam Taylor | ND | 28 | 28 | 1210 | 1212 | +2 | +0.17% |
| 174 | Samuel Collins | ND | 54 | 54 | 617 | 619 | +2 | +0.32% |
| 175 | Miles Bergman | ND | 14 | 14 | 920 | 922 | +2 | +0.22% |
| 176 | Will Brodie | ND | 9 | 9 | 771 | 773 | +2 | +0.26% |
| 177 | Angus Sheldrick | ND | 18 | 18 | 746 | 748 | +2 | +0.27% |
| 178 | Brodie Kemp | ND | 17 | 17 | 678 | 680 | +2 | +0.29% |
| 179 | Clay Hall | ND | 38 | 38 | 216 | 214 | -2 | -0.93% |
| 180 | Charlie Comben | ND | 31 | 31 | 807 | 809 | +2 | +0.25% |
| 181 | Toby McMullin | ND | 34 | 34 | 133 | 135 | +2 | +1.50% |
| 182 | Tom Anastasopoulos | ND | 48 | 48 | 175 | 173 | -2 | -1.14% |
| 183 | Cooper Harvey | ND | 56 | 56 | 543 | 545 | +2 | +0.37% |
| 184 | Bailey Macdonald | ND | 51 | 51 | 150 | 148 | -2 | -1.33% |
| 185 | Ryan Angwin | ND | 19 | 19 | 481 | 483 | +2 | +0.42% |
| 186 | Alex Davies | ND | 17 | 17 | 399 | 401 | +2 | +0.50% |
| 187 | Jackson Archer | ND | 59 | 59 | 29 | 27 | -2 | -6.90% |
| 188 | Jaxon Prior | ND | 58 | 58 | 307 | 305 | -2 | -0.65% |
| 189 | Ryan Byrnes | ND | 51 | 51 | 66 | 64 | -2 | -3.03% |
| 190 | Hugo Ralphsmith | ND | 45 | 45 | 56 | 54 | -2 | -3.57% |
| 191 | Nick Daicos | ND | 4 | 4 | 10944 | 10945 | +1 | +0.01% |
| 192 | Nasiah Wanganeen-Milera | ND | 11 | 11 | 9687 | 9688 | +1 | +0.01% |
| 193 | Luke Jackson | ND | 3 | 3 | 10202 | 10203 | +1 | +0.01% |
| 194 | Zak Butters | ND | 12 | 12 | 7091 | 7092 | +1 | +0.01% |
| 195 | Errol Gulden | ND | 34 | 34 | 7238 | 7239 | +1 | +0.01% |
| 196 | Harley Reid | ND | 1 | 1 | 3819 | 3820 | +1 | +0.03% |
| 197 | Bailey J. Williams | ND | 35 | 35 | 2469 | 2470 | +1 | +0.04% |
| 198 | Chad Warner | ND | 38 | 38 | 4410 | 4411 | +1 | +0.02% |
| 199 | Darcy Wilmot | ND | 16 | 16 | 3312 | 3313 | +1 | +0.03% |
| 200 | Ryley Sanders | ND | 6 | 6 | 3884 | 3885 | +1 | +0.03% |
| 201 | Josh Ward | ND | 7 | 7 | 2816 | 2817 | +1 | +0.04% |
| 202 | Kysaiah Pickett | ND | 12 | 12 | 4248 | 4249 | +1 | +0.02% |
| 203 | Tom Green | ND | 10 | 10 | 4718 | 4719 | +1 | +0.02% |
| 204 | Colby McKercher | ND | 2 | 2 | 4284 | 4285 | +1 | +0.02% |
| 205 | Izak Rankine | ND | 3 | 3 | 4684 | 4685 | +1 | +0.02% |
| 206 | Connor MacDonald | ND | 26 | 26 | 2739 | 2740 | +1 | +0.04% |
| 207 | Kieren Briggs | ND | 34 | 34 | 1991 | 1992 | +1 | +0.05% |
| 208 | Sam Flanders | ND | 11 | 11 | 2066 | 2067 | +1 | +0.05% |
| 209 | Zac Bailey | ND | 15 | 15 | 2913 | 2914 | +1 | +0.03% |
| 210 | Connor Idun | ND | 61 | 61 | 2225 | 2224 | -1 | -0.04% |
| 211 | Touk Miller | ND | 29 | 29 | 2377 | 2378 | +1 | +0.04% |
| 212 | Max King | ND | 4 | 4 | 238 | 239 | +1 | +0.42% |
| 213 | Logan McDonald | ND | 4 | 4 | 692 | 693 | +1 | +0.14% |
| 214 | Toby Nankervis | ND | 35 | 35 | 2030 | 2031 | +1 | +0.05% |
| 215 | Will Day | ND | 13 | 13 | 2386 | 2387 | +1 | +0.04% |
| 216 | Wayne Milera | ND | 11 | 11 | 1801 | 1800 | -1 | -0.06% |
| 217 | Callum Mills | ND | 3 | 3 | 1995 | 1994 | -1 | -0.05% |
| 218 | Daniel Curtin | ND | 8 | 8 | 2487 | 2488 | +1 | +0.04% |
| 219 | Samuel Grlj | ND | 8 | 8 | 1736 | 1735 | -1 | -0.06% |
| 220 | Josh Rachele | ND | 6 | 6 | 2007 | 2008 | +1 | +0.05% |
| 221 | James Sicily | ND | 52 | 52 | 1422 | 1421 | -1 | -0.07% |
| 222 | Jake Soligo | ND | 36 | 36 | 2050 | 2051 | +1 | +0.05% |
| 223 | Luke Parker | ND | 42 | 42 | 1340 | 1339 | -1 | -0.07% |
| 224 | Caleb Daniel | ND | 46 | 46 | 1339 | 1338 | -1 | -0.07% |
| 225 | Trent Rivers | ND | 32 | 32 | 1853 | 1852 | -1 | -0.05% |
| 226 | Charlie Curnow | ND | 12 | 12 | 1364 | 1365 | +1 | +0.07% |
| 227 | Will Green | ND | 16 | 16 | 605 | 604 | -1 | -0.17% |
| 228 | Paul Curtis | ND | 35 | 35 | 1621 | 1622 | +1 | +0.06% |
| 229 | Thomas Stewart | ND | 40 | 40 | 1102 | 1101 | -1 | -0.09% |
| 230 | Gryan Miers | ND | 57 | 57 | 1649 | 1650 | +1 | +0.06% |
| 231 | Caleb Windsor | ND | 7 | 7 | 1783 | 1784 | +1 | +0.06% |
| 232 | Brent Daniels | ND | 27 | 27 | 1198 | 1199 | +1 | +0.08% |
| 233 | Mason Redman | ND | 30 | 30 | 1177 | 1176 | -1 | -0.09% |
| 234 | Oliver Hollands | ND | 11 | 11 | 1738 | 1739 | +1 | +0.06% |
| 235 | Jarman Impey | ND | 21 | 21 | 846 | 845 | -1 | -0.12% |
| 236 | Shaun Mannagh | ND | 36 | 36 | 662 | 663 | +1 | +0.15% |
| 237 | Kane Farrell | ND | 51 | 51 | 1307 | 1306 | -1 | -0.08% |
| 238 | Kai Lohmann | ND | 20 | 20 | 878 | 879 | +1 | +0.11% |
| 239 | Charlie Edwards | ND | 21 | 21 | 623 | 624 | +1 | +0.16% |
| 240 | Harry O'Farrell | ND | 40 | 40 | 200 | 201 | +1 | +0.50% |
| 241 | Jordan Ridley | ND | 22 | 22 | 694 | 695 | +1 | +0.14% |
| 242 | Ben Miller | ND | 62 | 62 | 1041 | 1042 | +1 | +0.10% |
| 243 | Oliver Florent | ND | 11 | 11 | 733 | 732 | -1 | -0.14% |
| 244 | Wil Powell | ND | 19 | 19 | 776 | 775 | -1 | -0.13% |
| 245 | Elijah Hewett | ND | 14 | 14 | 729 | 730 | +1 | +0.14% |
| 246 | Edward Allan | ND | 19 | 19 | 977 | 978 | +1 | +0.10% |
| 247 | Josh Sinn | ND | 12 | 12 | 265 | 266 | +1 | +0.38% |
| 248 | Jack Silvagni | ND | 53 | 53 | 616 | 617 | +1 | +0.16% |
| 249 | Lance Collard | ND | 28 | 28 | 147 | 146 | -1 | -0.68% |
| 250 | Matt Johnson | ND | 21 | 21 | 1132 | 1131 | -1 | -0.09% |
| 251 | Brayden Maynard | ND | 30 | 30 | 490 | 489 | -1 | -0.20% |
| 252 | Daniel Rioli | ND | 15 | 15 | 641 | 640 | -1 | -0.16% |
| 253 | Archie Ludowyke | ND | 50 | 50 | 205 | 206 | +1 | +0.49% |
| 254 | Francis Evans | ND | 40 | 40 | 493 | 494 | +1 | +0.20% |
| 255 | Tom Brown | ND | 17 | 17 | 492 | 493 | +1 | +0.20% |
| 256 | Angus Hastie | ND | 33 | 33 | 182 | 181 | -1 | -0.55% |
| 257 | Tyler Sonsie | ND | 28 | 28 | 1094 | 1095 | +1 | +0.09% |
| 258 | Matthew Flynn | ND | 41 | 41 | 501 | 502 | +1 | +0.20% |
| 259 | Sam De Koning | ND | 19 | 19 | 935 | 936 | +1 | +0.11% |
| 260 | Billy Dowling | ND | 43 | 43 | 151 | 150 | -1 | -0.66% |
| 261 | Alex Neal-Bullen | ND | 40 | 40 | 370 | 371 | +1 | +0.27% |
| 262 | Braeden Campbell | ND | 5 | 5 | 402 | 403 | +1 | +0.25% |
| 263 | Jesse Motlop | ND | 27 | 27 | 91 | 90 | -1 | -1.10% |
| 264 | Rory Lobb | ND | 29 | 29 | 275 | 276 | +1 | +0.36% |
| 265 | Blake Howes | ND | 39 | 39 | 273 | 272 | -1 | -0.37% |
| 266 | Jeremy Howe | ND | 35 | 35 | 225 | 224 | -1 | -0.44% |
| 267 | Tom Doedee | ND | 17 | 17 | 227 | 228 | +1 | +0.44% |
| 268 | Archie Perkins | ND | 9 | 9 | 238 | 239 | +1 | +0.42% |
| 269 | Lachlan Jones | ND | 16 | 16 | 124 | 125 | +1 | +0.81% |
| 270 | Nathan O'Driscoll | ND | 28 | 28 | 596 | 597 | +1 | +0.17% |
| 271 | Harrison Himmelberg | ND | 16 | 16 | 139 | 138 | -1 | -0.72% |
| 272 | Corey Durdin | ND | 39 | 39 | 48 | 49 | +1 | +2.08% |
| 273 | Rhylee West | ND | 26 | 26 | 99 | 100 | +1 | +1.01% |
| 274 | Tyler Brockman | ND | 48 | 48 | 49 | 50 | +1 | +2.04% |
| 275 | Ollie Lord | ND | 51 | 51 | 106 | 105 | -1 | -0.94% |
| 276 | Harrison Jones | ND | 30 | 30 | 171 | 172 | +1 | +0.58% |
| 277 | Elliott Himmelberg | ND | 51 | 51 | 55 | 56 | +1 | +1.82% |
| 278 | Riley Garcia | ND | 61 | 61 | 46 | 47 | +1 | +2.17% |
| 279 | Jeremy Sharp | ND | 27 | 27 | 62 | 63 | +1 | +1.61% |

## POOL — all 195 movers

Sorted by absolute move, largest first. `ty` = intake type, `pk` = draft pick, `ep` = effective
pick (the board's arm key).

| # | player | ty | pk | ep | before | after | delta | pct |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | Ned Moyle | MSD | 5 | 65 | 2054 | 2285 | +231 | +11.25% |
| 2 | Xavier Bamert | MSD | 5 | 65 | 313 | 509 | +196 | +62.62% |
| 3 | Chris Scerri | SSP | None | 65 | 285 | 459 | +174 | +61.05% |
| 4 | Cooper Trembath | MSD | 9 | 65 | 2051 | 2201 | +150 | +7.31% |
| 5 | Marcus Herbert | MSD | 13 | 65 | 1053 | 906 | -147 | -13.96% |
| 6 | Anthony Caminiti | SSP | None | 65 | 976 | 1110 | +134 | +13.73% |
| 7 | Patrick Retschko | RD | 8 | 65 | 1483 | 1608 | +125 | +8.43% |
| 8 | Thomas Burton | SSP | None | 65 | 305 | 415 | +110 | +36.07% |
| 9 | Zak Johnson | ND | 70 | 65 | 634 | 730 | +96 | +15.14% |
| 10 | Campbell Lake | MSD | 7 | 65 | 67 | 161 | +94 | +140.30% |
| 11 | Archer Day-Wicks | RD | 1 | 65 | 675 | 766 | +91 | +13.48% |
| 12 | Josh Lai | SSP | None | 65 | 516 | 597 | +81 | +15.70% |
| 13 | Isaiah Dudley | SSP | None | 65 | 160 | 234 | +74 | +46.25% |
| 14 | Lachlan McAndrew | SSP | None | 65 | 1208 | 1279 | +71 | +5.88% |
| 15 | Riley Hamilton | PDA | None | 65 | 234 | 305 | +71 | +30.34% |
| 16 | Hugo Hall-Kahan | MSD | 10 | 65 | 148 | 215 | +67 | +45.27% |
| 17 | James O'Donnell | UNR | None | 65 | 660 | 727 | +67 | +10.15% |
| 18 | Archie May | MSD | 6 | 65 | 415 | 476 | +61 | +14.70% |
| 19 | Kye Annand | MSD | 2 | 65 | 181 | 239 | +58 | +32.04% |
| 20 | Bodhi Uwland | PDA | None | 65 | 4141 | 4087 | -54 | -1.30% |
| 21 | Patrick Voss | RD | 5 | 65 | 1592 | 1538 | -54 | -3.39% |
| 22 | Ollie Greeves | RD | 5 | 65 | 421 | 475 | +54 | +12.83% |
| 23 | Finnbar Maley | RD | 2 | 65 | 240 | 192 | -48 | -20.00% |
| 24 | Karl Worner | RD | 4 | 65 | 1250 | 1206 | -44 | -3.52% |
| 25 | Mark Keane | SSP | None | 65 | 1514 | 1557 | +43 | +2.84% |
| 26 | Max Heath | MSD | 7 | 65 | 640 | 682 | +42 | +6.56% |
| 27 | Josh Draper | PDN | None | 65 | 274 | 315 | +41 | +14.96% |
| 28 | Malakai Champion | PDN | None | 65 | 303 | 341 | +38 | +12.54% |
| 29 | Judd McVee | RD | 9 | 65 | 278 | 316 | +38 | +13.67% |
| 30 | Balyn O'Brien | SSP | None | 65 | 263 | 300 | +37 | +14.07% |
| 31 | Liam Reidy | RD | 4 | 65 | 328 | 291 | -37 | -11.28% |
| 32 | Jaxon Artemis | MSD | 1 | 65 | 305 | 340 | +35 | +11.48% |
| 33 | Tylar Young | RD | 9 | 65 | 244 | 279 | +35 | +14.34% |
| 34 | Oscar Steene | SSP | None | 65 | 501 | 468 | -33 | -6.59% |
| 35 | Harrison Ramm | MSD | 3 | 65 | 320 | 351 | +31 | +9.69% |
| 36 | Oliver Hayes-Brown | UNR | None | 65 | 221 | 190 | -31 | -14.03% |
| 37 | Max Hall | MSD | 4 | 65 | 2820 | 2790 | -30 | -1.06% |
| 38 | Ned Long | RD | 3 | 65 | 1386 | 1416 | +30 | +2.16% |
| 39 | Oliver Francou | MSD | 3 | 65 | 345 | 375 | +30 | +8.70% |
| 40 | Levi Casboult | RD | 35 | 65 | 16 | 43 | +27 | +168.75% |
| 41 | Tristan Xerri | ND | 71 | 65 | 7825 | 7800 | -25 | -0.32% |
| 42 | Lukas Cooke | MSD | 11 | 65 | 182 | 206 | +24 | +13.19% |
| 43 | James Borlase | PDN | None | 65 | 448 | 424 | -24 | -5.36% |
| 44 | Jayden Nguyen | PDN | None | 65 | 429 | 452 | +23 | +5.36% |
| 45 | Josh Treacy | RD | 4 | 65 | 6942 | 6921 | -21 | -0.30% |
| 46 | Matthew Taberner | RD | 11 | 65 | 13 | 34 | +21 | +161.54% |
| 47 | Cooper Lord | MSD | 9 | 65 | 1325 | 1345 | +20 | +1.51% |
| 48 | Wade Derksen | MSD | 5 | 65 | 128 | 109 | -19 | -14.84% |
| 49 | Joel Fitzgerald | MSD | 16 | 65 | 55 | 72 | +17 | +30.91% |
| 50 | Liam Puncher | MSD | 15 | 65 | 107 | 124 | +17 | +15.89% |
| 51 | Will McLachlan | MSD | 6 | 65 | 100 | 117 | +17 | +17.00% |
| 52 | Odin Jones | RD | 4 | 65 | 10 | 26 | +16 | +160.00% |
| 53 | Matt Carroll | RD | 7 | 65 | 999 | 1014 | +15 | +1.50% |
| 54 | Luke Nankervis | RD | 1 | 65 | 369 | 384 | +15 | +4.07% |
| 55 | Tom Fullarton | UNR | None | 65 | 10 | 25 | +15 | +150.00% |
| 56 | Harrison Jones | RD | 5 | 65 | 10 | 25 | +15 | +150.00% |
| 57 | Jeremy Finlayson | ND | 75 | 65 | 10 | 25 | +15 | +150.00% |
| 58 | Tom Hanily | MSD | 14 | 65 | 142 | 154 | +12 | +8.45% |
| 59 | Ollie Dempsey | RD | 7 | 65 | 2439 | 2428 | -11 | -0.45% |
| 60 | Tom McCarthy | MSD | 1 | 65 | 1468 | 1457 | -11 | -0.75% |
| 61 | Charlie Dean | RD | 2 | 65 | 18 | 29 | +11 | +61.11% |
| 62 | Jordon Sweet | RD | 14 | 65 | 2295 | 2285 | -10 | -0.44% |
| 63 | Caleb Lewis | MSD | 13 | 65 | 128 | 138 | +10 | +7.81% |
| 64 | Hamish Davis | ND | 65 | 65 | 1038 | 1028 | -10 | -0.96% |
| 65 | Jai Culley | MSD | 1 | 65 | 188 | 178 | -10 | -5.32% |
| 66 | Conrad Williams | PDN | None | 65 | 8 | 18 | +10 | +125.00% |
| 67 | Jacob Bauer | MSD | 10 | 65 | 9 | 19 | +10 | +111.11% |
| 68 | Mitch Podhajski | MSD | 17 | 65 | 195 | 186 | -9 | -4.62% |
| 69 | Shadeau Brain | PDA | None | 65 | 78 | 69 | -9 | -11.54% |
| 70 | Logan Evans | MSD | 12 | 65 | 1369 | 1361 | -8 | -0.58% |
| 71 | Sandy Brock | PDA | None | 65 | 165 | 173 | +8 | +4.85% |
| 72 | Ned Reeves | SSP | None | 65 | 228 | 236 | +8 | +3.51% |
| 73 | Toby Pink | RD | 33 | 65 | 15 | 23 | +8 | +53.33% |
| 74 | Tyler Sellers | SSP | None | 65 | 6 | 14 | +8 | +133.33% |
| 75 | Jasper Scaife | MSD | 5 | 65 | 17 | 25 | +8 | +47.06% |
| 76 | Jaiden Hunter | MSD | 8 | 65 | 6 | 14 | +8 | +133.33% |
| 77 | Chris Burgess | SSP | None | 65 | 17 | 25 | +8 | +47.06% |
| 78 | Seth Campbell | RD | 3 | 65 | 1003 | 1010 | +7 | +0.70% |
| 79 | Hudson O'Keeffe | SSP | None | 65 | 143 | 136 | -7 | -4.90% |
| 80 | Sam Frost | RD | 5 | 65 | 26 | 33 | +7 | +26.92% |
| 81 | Callum Wilkie | RD | 1 | 65 | 3627 | 3633 | +6 | +0.17% |
| 82 | Nicholas Martin | SSP | None | 65 | 2828 | 2822 | -6 | -0.21% |
| 83 | Liam O'Connell | IRE | None | 65 | 45 | 39 | -6 | -13.33% |
| 84 | Jacob Blight | MSD | 2 | 65 | 4 | 10 | +6 | +150.00% |
| 85 | Kallan Dawson | MSD | 2 | 65 | 2 | 8 | +6 | +300.00% |
| 86 | Alex Keath | UNR | None | 65 | 2 | 8 | +6 | +300.00% |
| 87 | Jeremy McGovern | RD | 37 | 65 | 24 | 30 | +6 | +25.00% |
| 88 | Nick Madden | PDA | None | 65 | 1761 | 1766 | +5 | +0.28% |
| 89 | Ryan Maric | MSD | 1 | 65 | 1401 | 1406 | +5 | +0.36% |
| 90 | Campbell Gray | MSD | 15 | 65 | 181 | 176 | -5 | -2.76% |
| 91 | Will Edwards | PDA | None | 65 | 209 | 214 | +5 | +2.39% |
| 92 | Tyrell Dewar | PDN | None | 65 | 68 | 73 | +5 | +7.35% |
| 93 | Harry Edwards | RD | 12 | 65 | 92 | 97 | +5 | +5.43% |
| 94 | Xavier Ivisic | RD | 4 | 65 | 11 | 16 | +5 | +45.45% |
| 95 | Kynan Brown | RD | 9 | 65 | 11 | 16 | +5 | +45.45% |
| 96 | Ethan Phillips | SSP | None | 65 | 1 | 6 | +5 | +500.00% |
| 97 | Joshua Bennetts | PDN | None | 65 | 13 | 18 | +5 | +38.46% |
| 98 | Harry Arnold | MSD | 5 | 65 | 1 | 6 | +5 | +500.00% |
| 99 | Zane Trew | RD | 7 | 65 | 11 | 16 | +5 | +45.45% |
| 100 | Ash Johnson | MSD | 3 | 65 | 1 | 6 | +5 | +500.00% |
| 101 | Ethan Hughes | RD | 10 | 65 | 12 | 17 | +5 | +41.67% |
| 102 | Jake Kelly | RD | 22 | 65 | 14 | 19 | +5 | +35.71% |
| 103 | Lachlan Keeffe | UNR | None | 65 | 13 | 18 | +5 | +38.46% |
| 104 | Jai Newcombe | MSD | 2 | 65 | 4887 | 4883 | -4 | -0.08% |
| 105 | Reilly O'Brien | RD | 8 | 65 | 981 | 985 | +4 | +0.41% |
| 106 | Jack Buckley | PDN | None | 65 | 552 | 548 | -4 | -0.72% |
| 107 | Mitchell Lewis | ND | 75 | 65 | 521 | 517 | -4 | -0.77% |
| 108 | Milan Murdock | SSP | None | 65 | 212 | 208 | -4 | -1.89% |
| 109 | Sam Clohesy | RD | 3 | 65 | 284 | 288 | +4 | +1.41% |
| 110 | Josaia Delana | PDA | None | 65 | 395 | 391 | -4 | -1.01% |
| 111 | Blake Leidler | RD | 6 | 65 | 12 | 16 | +4 | +33.33% |
| 112 | Will White | SSP | None | 65 | 5 | 9 | +4 | +80.00% |
| 113 | Kelsey Rypstra | MSD | 8 | 65 | 5 | 9 | +4 | +80.00% |
| 114 | Oscar Murdoch | RD | 7 | 65 | 14 | 18 | +4 | +28.57% |
| 115 | Jed McEntee | MSD | 11 | 65 | 5 | 9 | +4 | +80.00% |
| 116 | Nathan Kreuger | RD | 13 | 65 | 0 | 4 | +4 | +400.00% |
| 117 | James Harmes | RD | 1 | 65 | 12 | 16 | +4 | +33.33% |
| 118 | Rory Atkins | ND | 68 | 65 | 11 | 15 | +4 | +36.36% |
| 119 | Alex Sexton | ND | 79 | 65 | 13 | 17 | +4 | +30.77% |
| 120 | Jason Johannisen | RD | 32 | 65 | 13 | 17 | +4 | +30.77% |
| 121 | Dylan Grimes | RD | 1 | 65 | 14 | 18 | +4 | +28.57% |
| 122 | Jack Sinclair | RD | 1 | 65 | 3325 | 3322 | -3 | -0.09% |
| 123 | John Noble | MSD | 8 | 65 | 2162 | 2159 | -3 | -0.14% |
| 124 | Jack Ginnivan | RD | 8 | 65 | 2245 | 2242 | -3 | -0.13% |
| 125 | Peter Ladhams | RD | 7 | 65 | 492 | 489 | -3 | -0.61% |
| 126 | Nick Murray | SSP | None | 65 | 324 | 321 | -3 | -0.93% |
| 127 | Buku Khamis | PDN | None | 65 | 147 | 144 | -3 | -2.04% |
| 128 | Loch Rawlinson | RD | 1 | 65 | 8 | 11 | +3 | +37.50% |
| 129 | Will Rowlands | RD | 8 | 65 | 8 | 11 | +3 | +37.50% |
| 130 | Geordie Payne | MSD | 1 | 65 | 7 | 10 | +3 | +42.86% |
| 131 | Blake Drury | RD | 1 | 65 | 8 | 11 | +3 | +37.50% |
| 132 | Oliver Sestan | RD | 10 | 65 | 8 | 11 | +3 | +37.50% |
| 133 | Jaiden Magor | RD | 11 | 65 | 8 | 11 | +3 | +37.50% |
| 134 | Osca Ricciardi | RD | 12 | 65 | 8 | 11 | +3 | +37.50% |
| 135 | Kyah Farris-White | UNR | None | 65 | 7 | 10 | +3 | +42.86% |
| 136 | Anthony Munkara | PDN | None | 65 | 7 | 10 | +3 | +42.86% |
| 137 | Ted Clohesy | PDN | None | 65 | 7 | 10 | +3 | +42.86% |
| 138 | Brodie McLaughlin | SSP | None | 65 | 0 | 3 | +3 | +300.00% |
| 139 | Brandon Ryan | MSD | 9 | 65 | 0 | 3 | +3 | +300.00% |
| 140 | Jack Hayes | SSP | None | 65 | 0 | 3 | +3 | +300.00% |
| 141 | Patrick Parnell | MSD | 4 | 65 | 10 | 13 | +3 | +30.00% |
| 142 | Lachlan Murphy | RD | 19 | 65 | 7 | 10 | +3 | +42.86% |
| 143 | Jamaine Jones | RD | 30 | 65 | 7 | 10 | +3 | +42.86% |
| 144 | Darcy MacPherson | RD | 17 | 65 | 7 | 10 | +3 | +42.86% |
| 145 | Zach Tuohy | IRE | None | 65 | 7 | 10 | +3 | +42.86% |
| 146 | Luke Breust | RD | 37 | 65 | 10 | 13 | +3 | +30.00% |
| 147 | Sam Durham | MSD | 9 | 65 | 2533 | 2531 | -2 | -0.08% |
| 148 | Lloyd Meek | ND | 68 | 65 | 1302 | 1300 | -2 | -0.15% |
| 149 | Daniel Turner | MSD | 20 | 65 | 1532 | 1534 | +2 | +0.13% |
| 150 | James Peatling | MSD | 8 | 65 | 1100 | 1098 | -2 | -0.18% |
| 151 | Kade Chandler | RD | 10 | 65 | 813 | 811 | -2 | -0.25% |
| 152 | Michael Sellwood | MSD | 5 | 65 | 166 | 168 | +2 | +1.20% |
| 153 | James Trezise | MSD | 10 | 65 | 120 | 118 | -2 | -1.67% |
| 154 | Tom Cochrane | RD | 5 | 65 | 146 | 148 | +2 | +1.37% |
| 155 | Mitchell Hinge | RD | 15 | 65 | 322 | 320 | -2 | -0.62% |
| 156 | Andy Moniz-Wakefield | PDN | None | 65 | 25 | 27 | +2 | +8.00% |
| 157 | Harry Boyd | SSP | None | 65 | 2 | 4 | +2 | +100.00% |
| 158 | Oskar Smartt | MSD | 16 | 65 | 9 | 11 | +2 | +22.22% |
| 159 | Karl Gallagher | IRE | None | 65 | 3 | 5 | +2 | +66.67% |
| 160 | Indhi Kirk | PDA | None | 65 | 9 | 11 | +2 | +22.22% |
| 161 | Darcy Craven | MSD | 17 | 65 | 9 | 11 | +2 | +22.22% |
| 162 | Rhett Montgomerie | RD | 2 | 65 | 2 | 4 | +2 | +100.00% |
| 163 | Hamish Free | RD | 8 | 65 | 4 | 6 | +2 | +50.00% |
| 164 | Brynn Teakle | MSD | 8 | 65 | 6 | 8 | +2 | +33.33% |
| 165 | Jye Menzie | MSD | 13 | 65 | 9 | 11 | +2 | +22.22% |
| 166 | Kieran Strachan | RD | 3 | 65 | 6 | 8 | +2 | +33.33% |
| 167 | Dan Houston | RD | 30 | 65 | 1097 | 1096 | -1 | -0.09% |
| 168 | Luke Ryan | ND | 65 | 65 | 1316 | 1315 | -1 | -0.08% |
| 169 | Dylan Moore | ND | 66 | 65 | 1183 | 1182 | -1 | -0.08% |
| 170 | Massimo D'Ambrosio | MSD | 3 | 65 | 1566 | 1565 | -1 | -0.06% |
| 171 | Cooper Sharman | MSD | 18 | 65 | 430 | 429 | -1 | -0.23% |
| 172 | Sam Draper | RD | 1 | 65 | 1106 | 1107 | +1 | +0.09% |
| 173 | Rory Laird | RD | 8 | 65 | 702 | 701 | -1 | -0.14% |
| 174 | Jake Waterman | ND | 76 | 65 | 1161 | 1160 | -1 | -0.09% |
| 175 | Nic Newman | RD | 24 | 65 | 629 | 628 | -1 | -0.16% |
| 176 | Flynn Riley | MSD | 4 | 65 | 232 | 233 | +1 | +0.43% |
| 177 | Vigo Visentini | RD | 5 | 65 | 167 | 168 | +1 | +0.60% |
| 178 | Matt Hill | UNR | None | 65 | 48 | 49 | +1 | +2.08% |
| 179 | Tom Blamires | SSP | None | 65 | 113 | 114 | +1 | +0.89% |
| 180 | Luker Kentfield | MSD | 11 | 65 | 179 | 178 | -1 | -0.56% |
| 181 | Aidan Johnson | ND | 68 | 65 | 81 | 80 | -1 | -1.23% |
| 182 | Toby Murray | MSD | 7 | 65 | 216 | 215 | -1 | -0.46% |
| 183 | Hayden McLean | SSP | None | 65 | 215 | 214 | -1 | -0.47% |
| 184 | Zach Guthrie | RD | 21 | 65 | 211 | 210 | -1 | -0.47% |
| 185 | Malcolm Rosas | RD | 14 | 65 | 26 | 25 | -1 | -3.85% |
| 186 | Caleb Graham | ND | 71 | 65 | 38 | 37 | -1 | -2.63% |
| 187 | Darragh Joyce | IRE | None | 65 | 21 | 20 | -1 | -4.76% |
| 188 | Jason Gillbee | PDA | None | 65 | 9 | 10 | +1 | +11.11% |
| 189 | Lloyd Johnston | PDA | None | 65 | 9 | 10 | +1 | +11.11% |
| 190 | Nathan Barkla | PDN | None | 65 | 9 | 10 | +1 | +11.11% |
| 191 | Angus McLennan | PDN | None | 65 | 9 | 10 | +1 | +11.11% |
| 192 | Jordyn Baker | PDN | None | 65 | 9 | 10 | +1 | +11.11% |
| 193 | Matt Coulthard | MSD | 4 | 65 | 1 | 2 | +1 | +100.00% |
| 194 | Robbie Fox | RD | 22 | 65 | 1 | 2 | +1 | +100.00% |
| 195 | Oscar McInerney | RD | 23 | 65 | 7 | 8 | +1 | +14.29% |

## Provenance

- Both boards rebuilt on the landing tree with `docs/evidence/par_adoption_2026-08-12/scripts/build_board_o20b.sh`
  (ORDER 20B's harness), shipped defaults, no manifest override.
- Control (unmodified tree) → `94f1fec59f99c59d5890d5975c79fa9b`, byte-identical to the live pinned board.
- Fix (`78d5c38`'s two files) → `1dbd1480a34c7823f330273211cbb76a`, byte-identical to ORDER 20's measured FIX board.
- Delta computed with ORDER 20's own `fix/board_delta.py`; every published figure in its committed
  `BOARD_DELTA_par_armsplit.json` reproduces, and all 40+40 of its named top movers reproduce to the unit.
- Channel decomposition carried unchanged from ORDER 20B's `movers/CHANNEL_DECOMP.json`.
- Machine-readable sidecar: `PAR_FIX_MOVERS_2026-08-12.json` (same directory), which additionally
  carries each row's board `key` and section and each decomposed mover's channel residuals.

---

_Generated by [Claude Code](https://claude.ai/code)_
