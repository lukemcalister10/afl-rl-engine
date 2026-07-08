# L1c OWNER W-TABLE — w = fraction of the measured cell re-rating paid forward (RL_YCRED_W)
## 2026-07-08 · grid {0.5, 0.7, 0.85, 1.0} (owner-amended, matches the investigation simulation) · OWNER RULED w=0.9 (2026-07-08, on this table) — engine default now 0.9; 0.7 was the pre-ruling default

## Per-year G-COHORT landing (conforming measure: class-year SUMS averaged across classes 2004-2020; EACH of y4/5/6 vs min(y1,y2); walk-forward book)
| config | y1 figure | y2 figure | y4/den | y5/den | y6/den | verdict (hard <=130, guide 120-125) |
|---|---|---|---|---|---|---|
| W4 pre-L1c (old runway credit, audited) | 57,558.5 | 70,211.0 | 142.4% | 140.8% | 131.7% | BREACH (owner-upheld) |
| credit-off basis (RL_YOUNG=0) | 55,603 | 67,976 | — | — | — | derivation basis |
| w=0.5 | 60,148.5 | 71,175.6 | 135.5% | 134.2% | 125.9% | BREACH (worst 135.5%) |
| **w=0.7 (shipped)** | 61,974.8 | 72,444.5 | 131.9% | 130.5% | 122.3% | BREACH (worst 131.9%) |
| w=0.85 | 63,360.6 | 73,374.2 | 129.4% | 127.7% | 119.7% | PASS (worst 129.4%) |
| **w=0.9 (OWNER-RULED 2026-07-08)** | 63,821.9 | 73,690.6 | 128.6% | 126.9% | 118.8% | PASS (worst 128.6%) |
| w=1.0 | 64,761.8 | 74,324.8 | 126.9% | 125.1% | 117.1% | PASS (worst 126.9%) |

SIM-vs-BUILT NOTE (owner amendment asked this table to carry the simulated landings): the investigation 
grid simulated **0.85 -> ~120.0 (guide floor)** and **1.0 -> ~116.7 (below guide)**. The BUILT engine lands 
0.85 -> worst 129.4% (y4) and 1.0 -> worst 126.9% (y4) — the simulated values match the built **y6** almost 
exactly (119.7 / 117.1) but not the binding y4. Mechanism of the gap, in order of size: (i) the credit is 
EVIDENCE-FADED at the y1 anchor (a played year-1 player has ~half his phi burnt by the end-of-y1 anchor; the 
simulation paid full credit to the whole y1 sum), (ii) played-cell re-ratings are much smaller than sat-cell 
ones and the blend s(g) moves players onto the played curve within 6 games, (iii) the TRAILING (leak-free) 
table gives classes 2004-05 zero credit and 2006-08 thin-window credit, dragging the 17-class average, 
(iv) negative-measured cells are clipped to zero, and capped rucks keep the RUC prior cap. These are the 
directive's own constraints (evidence-keyed fade, trailing leak-free, clip>=0, cap out of scope) — reported 
as built, not re-tuned.

## Named players (2026 board values; before = baked v2.5 and the W4 pre-L1c candidate)
| player | baked v2.5 | W4 pre-L1c | credit-off | w=0.5 | w=0.7 | w=0.85 | w=1.0 | shape |
|---|---|---|---|---|---|---|---|---|
| Willem Duursma | 4110 | 4295 | 4110 | 4174 | 4199 | 4218 | 4238 | A-DUUR young gun · 2025 pk1 MID · 12g |
| Sam Lalor | 3337 | 3421 | 3337 | 3372 | 3386 | 3396 | 3406 | top-3 pick · 2024 pk1 · 18g |
| Errol Gulden | 5256 | 5715 | 5715 | 5715 | 5715 | 5715 | 5715 | Gulden shape: mid-pick instant producer · 2020 pk34 · 105g |
| Sam Darcy | 4144 | 4330 | 4168 | 4168 | 4168 | 4168 | 4168 | Darcy shape: young KPF ceiling · 2021 pk2 · 51g |
| Taylor Goad | 723 | 801 | 776 | 783 | 785 | 787 | 789 | Goad shape: sat-out young ruck · 2023 pk20 · 1g |
| Dylan Patterson | 762 | 780 | 762 | 824 | 849 | 868 | 887 | pure sit-out · 2025 pk5 · 0 games |
| Riley Bice | 404 | 401 | 401 | 406 | 409 | 410 | 412 | mature-age pick · 2024 pk41 · draft-age 24 · 30g |

## G-ATTR — RL_YOUNG leave-one-out at w=0.7 (book `cur` columns, all-on vs credit-off)
- players compared: 2649 · movers: 1534 · pool delta: +15,903 SCAR = +2.31% of the credit-off board
- negative movers: 0 (credit clipped >=0 by construction)
- top recipients: daniel-annable +347, sullivan-robey +228, cooper-duff-tytler +226, dyson-sharp +216, josh-smillie +215, taj-hotton +210, harry-o-farrell +202, samuel-grlj +188, harry-dean +181, jai-murray +166

## A-DUUR direction
- Duursma baked 4110 -> shipped w=0.7 4199 (+2.2%); credit-off 4110 -> w=0.7 4199 — direction UP: PASS

## w=0.9 (OWNER-RULED) — named players (2026 board)
| player | w=0.9 |
|---|---|
| Willem Duursma | 4225 |
| Sam Lalor | 3400 |
| Errol Gulden | 5715 |
| Sam Darcy | 4168 |
| Taylor Goad | 788 |
| Dylan Patterson | 874 |
| Riley Bice | 411 |

DECLARED TENSION at w=0.9 (scales with w): the extreme-sat-cell evidence-axis dip is -10.4% top-to-trough on a pick-1 MID (games 4->7; was -7.6% at w=0.7); continuous, credit-off sweep monotone; pk7 ~-2.5%, pk5 none (out/gmono_v0_w09.json, out/evidence_sweeps.json).
