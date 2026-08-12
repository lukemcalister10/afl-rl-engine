# PAR_TABLE — ORDER 24B, THE PLAYING PAR BY PATHWAY × CAREER DEPTH

Issue #334, ORDER 24B. Branch `build/pool-quality`. Pre-registration: `PREREG_ORDER24B.md`,
committed **before** this table was computed.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

---

## 1. The population, and the gate

The par comes from the **same complete-window harvest population that produced `R`** and from
nothing else — `o24b_uharvest.py`'s `WC`: pool careers only, complete window `Y ≤ 2021`,
priceable entry anchor. **National rows: 1390 encountered at the harvest gate and excluded, and
zero present in this file — asserted in `o24b_par.py` before a single par is formed.**

| quantity | n |
|---|---:|
| complete-window cells with a priceable anchor | 3334 |
| of which **playing** (`games > 0`) with a usable average — **the par population** | **2323** |
| playing cells with no usable average (read as `q = 0`, never as par) | 1 |
| non-playing cells (`φ = 0`, no `q` exists) | 1010 |

## 2. The rule

```
par_own(pw,d)  = SUM(avg_y * games) / SUM(games)   over playing cells with that (pw,d)
par_donor(pw)  = SUM(avg_y * games) / SUM(games)   over ALL playing cells of that pathway
w(pw,d)        = n(pw,d) / (n(pw,d) + 10)          n = raw exact-depth CELL count
par(pw,d)      = w * par_own + (1-w) * par_donor
```

`d` is the harvest's own depth, `d = Y − debutyr + 1`, clipped to `[1,6]` — **the same integer
`R` is indexed on**, so `par(pw,d)` and `R(pw,cls,d)` read the same cell. The K=10 shrink is
ORDER 22's class-axis form carried verbatim (owner ruling 5262213139); it applies at **every**
cell with no thinness threshold, and every cell is disclosed below.

## 3. The shrink donor — each pathway's all-depth playing par

| pathway | all-depth par | games | cells |
|---|---:|---:|---:|
| `RD` | 71.29 | 21,326 | 1698 |
| `ND>64` | 67.52 | 3,448 | 316 |
| `IRE` | 67.22 | 885 | 89 |
| `UNR` | 68.11 | 839 | 73 |
| `PDA` | 55.82 | 771 | 69 |
| `PDS` | 59.68 | 212 | 26 |
| `MSD` | 61.70 | 121 | 14 |
| `PDN` | 60.07 | 77 | 15 |
| `SSP` | 56.88 | 270 | 23 |
| **ALL POOL** | **69.87** | 27,949 | 2323 |

## 4. THE PAR TABLE — every cell, with its n and its shrink disclosed

| pathway | d | cells `n` | games | own par | donor | w = n/(n+10) | **WIRED** | shrink | thin? |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `RD` | 1 | 194 | 1,437 | 59.80 | 71.29 | 0.9510 | **60.36** | +0.56 (+0.94%) |  |
| `RD` | 2 | 229 | 2,185 | 63.16 | 71.29 | 0.9582 | **63.50** | +0.34 (+0.54%) |  |
| `RD` | 3 | 238 | 2,679 | 66.96 | 71.29 | 0.9597 | **67.14** | +0.17 (+0.26%) |  |
| `RD` | 4 | 211 | 2,883 | 71.26 | 71.29 | 0.9548 | **71.26** | +0.00 (+0.00%) |  |
| `RD` | 5 | 176 | 2,568 | 72.39 | 71.29 | 0.9462 | **72.33** | -0.06 (-0.08%) |  |
| `RD` | 6 | 650 | 9,574 | 75.79 | 71.29 | 0.9848 | **75.72** | -0.07 (-0.09%) |  |
| `ND>64` | 1 | 37 | 254 | 60.22 | 67.52 | 0.7872 | **61.77** | +1.55 (+2.58%) | shrink ≥ 2% |
| `ND>64` | 2 | 55 | 441 | 58.41 | 67.52 | 0.8462 | **59.81** | +1.40 (+2.40%) | shrink ≥ 2% |
| `ND>64` | 3 | 53 | 519 | 61.25 | 67.52 | 0.8413 | **62.24** | +1.00 (+1.62%) |  |
| `ND>64` | 4 | 44 | 535 | 65.66 | 67.52 | 0.8148 | **66.01** | +0.34 (+0.52%) |  |
| `ND>64` | 5 | 34 | 414 | 67.40 | 67.52 | 0.7727 | **67.43** | +0.03 (+0.04%) |  |
| `ND>64` | 6 | 93 | 1,285 | 75.43 | 67.52 | 0.9029 | **74.66** | -0.77 (-1.02%) |  |
| `IRE` | 1 | 9 | 36 | 52.22 | 67.22 | 0.4737 | **60.12** | +7.90 (+15.12%) | **THIN** — n<10, donor carries the majority |
| `IRE` | 2 | 15 | 99 | 54.65 | 67.22 | 0.6000 | **59.68** | +5.03 (+9.21%) | shrink ≥ 2% |
| `IRE` | 3 | 17 | 160 | 58.16 | 67.22 | 0.6296 | **61.52** | +3.36 (+5.77%) | shrink ≥ 2% |
| `IRE` | 4 | 13 | 137 | 64.84 | 67.22 | 0.5652 | **65.88** | +1.04 (+1.60%) |  |
| `IRE` | 5 | 10 | 124 | 66.82 | 67.22 | 0.5000 | **67.02** | +0.20 (+0.30%) |  |
| `IRE` | 6 | 25 | 329 | 78.20 | 67.22 | 0.7143 | **75.07** | -3.14 (-4.01%) | shrink ≥ 2% |
| `UNR` | 1 | 5 | 42 | 40.00 | 68.11 | 0.3333 | **58.74** | +18.74 (+46.87%) | **THIN** — n<10, donor carries the majority |
| `UNR` | 2 | 14 | 110 | 58.92 | 68.11 | 0.5833 | **62.75** | +3.83 (+6.50%) | shrink ≥ 2% |
| `UNR` | 3 | 16 | 141 | 61.96 | 68.11 | 0.6154 | **64.32** | +2.37 (+3.82%) | shrink ≥ 2% |
| `UNR` | 4 | 11 | 131 | 74.00 | 68.11 | 0.5238 | **71.20** | -2.80 (-3.79%) | shrink ≥ 2% |
| `UNR` | 5 | 9 | 133 | 75.17 | 68.11 | 0.4737 | **71.45** | -3.71 (-4.94%) | **THIN** — n<10, donor carries the majority |
| `UNR` | 6 | 18 | 282 | 72.90 | 68.11 | 0.6429 | **71.19** | -1.71 (-2.35%) | shrink ≥ 2% |
| `PDA` | 1 | 8 | 45 | 51.62 | 55.82 | 0.4444 | **53.95** | +2.33 (+4.52%) | **THIN** — n<10, donor carries the majority |
| `PDA` | 2 | 15 | 124 | 30.39 | 55.82 | 0.6000 | **40.56** | +10.17 (+33.48%) | shrink ≥ 2% |
| `PDA` | 3 | 14 | 184 | 48.81 | 55.82 | 0.5833 | **51.73** | +2.92 (+5.98%) | shrink ≥ 2% |
| `PDA` | 4 | 8 | 144 | 51.81 | 55.82 | 0.4444 | **54.04** | +2.23 (+4.30%) | **THIN** — n<10, donor carries the majority |
| `PDA` | 5 | 7 | 86 | 72.43 | 55.82 | 0.4118 | **62.66** | -9.77 (-13.49%) | **THIN** — n<10, donor carries the majority |
| `PDA` | 6 | 17 | 188 | 75.93 | 55.82 | 0.6296 | **68.48** | -7.45 (-9.81%) | shrink ≥ 2% |
| `PDS` | 1 | 1 | 11 | 49.73 | 59.68 | 0.0909 | **58.78** | +9.05 (+18.20%) | **THIN** — n<10, donor carries the majority |
| `PDS` | 2 | 3 | 10 | 30.30 | 59.68 | 0.2308 | **52.90** | +22.60 (+74.59%) | **THIN** — n<10, donor carries the majority |
| `PDS` | 3 | 3 | 7 | 40.86 | 59.68 | 0.2308 | **55.34** | +14.48 (+35.44%) | **THIN** — n<10, donor carries the majority |
| `PDS` | 4 | 2 | 21 | 73.21 | 59.68 | 0.1667 | **61.94** | -11.27 (-15.40%) | **THIN** — n<10, donor carries the majority |
| `PDS` | 5 | 5 | 60 | 58.89 | 59.68 | 0.3333 | **59.42** | +0.53 (+0.90%) | **THIN** — n<10, donor carries the majority |
| `PDS` | 6 | 12 | 103 | 62.58 | 59.68 | 0.5455 | **61.26** | -1.32 (-2.11%) | shrink ≥ 2% |
| `MSD` | 1 | 9 | 40 | 51.55 | 61.70 | 0.4737 | **56.89** | +5.34 (+10.36%) | **THIN** — n<10, donor carries the majority |
| `MSD` | 2 | 3 | 41 | 65.08 | 61.70 | 0.2308 | **62.48** | -2.60 (-4.00%) | **THIN** — n<10, donor carries the majority |
| `MSD` | 3 | 2 | 40 | 68.38 | 61.70 | 0.1667 | **62.81** | -5.57 (-8.14%) | **THIN** — n<10, donor carries the majority |
| `MSD` | 4 | 0 | 0 | _empty_ | 61.70 | 0.0000 | **61.70** | — | **THIN** — n<10, donor carries the majority |
| `MSD` | 5 | 0 | 0 | _empty_ | 61.70 | 0.0000 | **61.70** | — | **THIN** — n<10, donor carries the majority |
| `MSD` | 6 | 0 | 0 | _empty_ | 61.70 | 0.0000 | **61.70** | — | **THIN** — n<10, donor carries the majority |
| `PDN` | 1 | 2 | 4 | 43.50 | 60.07 | 0.1667 | **57.31** | +13.81 (+31.75%) | **THIN** — n<10, donor carries the majority |
| `PDN` | 2 | 3 | 12 | 58.18 | 60.07 | 0.2308 | **59.64** | +1.45 (+2.50%) | **THIN** — n<10, donor carries the majority |
| `PDN` | 3 | 7 | 29 | 49.71 | 60.07 | 0.4118 | **55.81** | +6.10 (+12.26%) | **THIN** — n<10, donor carries the majority |
| `PDN` | 4 | 3 | 32 | 72.25 | 60.07 | 0.2308 | **62.88** | -9.36 (-12.96%) | **THIN** — n<10, donor carries the majority |
| `PDN` | 5 | 0 | 0 | _empty_ | 60.07 | 0.0000 | **60.07** | — | **THIN** — n<10, donor carries the majority |
| `PDN` | 6 | 0 | 0 | _empty_ | 60.07 | 0.0000 | **60.07** | — | **THIN** — n<10, donor carries the majority |
| `SSP` | 1 | 10 | 134 | 55.42 | 56.88 | 0.5000 | **56.15** | +0.73 (+1.32%) |  |
| `SSP` | 2 | 6 | 52 | 59.21 | 56.88 | 0.3750 | **57.75** | -1.46 (-2.46%) | **THIN** — n<10, donor carries the majority |
| `SSP` | 3 | 7 | 84 | 57.76 | 56.88 | 0.4118 | **57.24** | -0.52 (-0.90%) | **THIN** — n<10, donor carries the majority |
| `SSP` | 4 | 0 | 0 | _empty_ | 56.88 | 0.0000 | **56.88** | — | **THIN** — n<10, donor carries the majority |
| `SSP` | 5 | 0 | 0 | _empty_ | 56.88 | 0.0000 | **56.88** | — | **THIN** — n<10, donor carries the majority |
| `SSP` | 6 | 0 | 0 | _empty_ | 56.88 | 0.0000 | **56.88** | — | **THIN** — n<10, donor carries the majority |
| `ALL POOL` | 1 | 275 | 2,003 | 58.57 | 69.87 | 0.9649 | **58.97** | +0.40 (+0.68%) |  |
| `ALL POOL` | 2 | 343 | 3,074 | 60.56 | 69.87 | 0.9717 | **60.82** | +0.26 (+0.44%) |  |
| `ALL POOL` | 3 | 357 | 3,843 | 64.41 | 69.87 | 0.9728 | **64.56** | +0.15 (+0.23%) |  |
| `ALL POOL` | 4 | 292 | 3,883 | 69.65 | 69.87 | 0.9669 | **69.66** | +0.01 (+0.01%) |  |
| `ALL POOL` | 5 | 241 | 3,385 | 71.45 | 69.87 | 0.9602 | **71.38** | -0.06 (-0.09%) |  |
| `ALL POOL` | 6 | 815 | 11,761 | 75.63 | 69.87 | 0.9879 | **75.56** | -0.07 (-0.09%) |  |

**Every cell in this table is shrunk** — that is the rule, applied uniformly. The `shrink`
column is the size of the move in points and per cent, so a reader can see exactly where the
donor is doing the work. Cells flagged **THIN** carry `n < 10`, where the donor holds the
majority weight; cells flagged `shrink ≥ 2%` are the ones where the pooling materially moved
the number even though the cell was not thin.

## 5. Monotonicity in depth — reported, never projected

Par is a measurement, not a shape: **no isotonic projection is applied**, and a non-monotone
step is reported as measured.

| pathway | d1 | d2 | d3 | d4 | d5 | d6 | steps |
|---|---:|---:|---:|---:|---:|---:|---|
| `RD` | 60.36 | 63.50 | 67.14 | 71.26 | 72.33 | 75.72 | ↑ ↑ ↑ ↑ ↑ |
| `ND>64` | 61.77 | 59.81 | 62.24 | 66.01 | 67.43 | 74.66 | ↓ ↑ ↑ ↑ ↑ |
| `IRE` | 60.12 | 59.68 | 61.52 | 65.88 | 67.02 | 75.07 | ↓ ↑ ↑ ↑ ↑ |
| `UNR` | 58.74 | 62.75 | 64.32 | 71.20 | 71.45 | 71.19 | ↑ ↑ ↑ ↑ ↓ |
| `PDA` | 53.95 | 40.56 | 51.73 | 54.04 | 62.66 | 68.48 | ↓ ↑ ↑ ↑ ↑ |
| `PDS` | 58.78 | 52.90 | 55.34 | 61.94 | 59.42 | 61.26 | ↓ ↑ ↑ ↓ ↑ |
| `MSD` | 56.89 | 62.48 | 62.81 | 61.70 | 61.70 | 61.70 | ↑ ↑ ↓ ↓ ↓ |
| `PDN` | 57.31 | 59.64 | 55.81 | 62.88 | 60.07 | 60.07 | ↑ ↓ ↑ ↓ ↓ |
| `SSP` | 56.15 | 57.75 | 57.24 | 56.88 | 56.88 | 56.88 | ↑ ↓ ↓ ↓ ↓ |
| `ALL POOL` | 58.97 | 60.82 | 64.56 | 69.66 | 71.38 | 75.56 | ↑ ↑ ↑ ↑ ↑ |

## 6. Reconciliation with the supervising seat's reference points

The seat computed four cells from the store (md5 `d9a24282`, complete-window ≤2021,
`d = Y − draftyr`). The conventions are not identical — the seat's quick cut against this
order's harvest gate — so the order asks for reconciliation, not agreement.

| pathway | d | seat par | my own par | my **wired** par | gap (own) | gap (wired) | seat `n` | my cells | my games |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `MSD` | 1 | 58.9 | 51.55 | **56.89** | -12.48% | -3.41% | 162 | 9 | 40 |
| `MSD` | 2 | 61.4 | 65.08 | **62.48** | +5.99% | +1.76% | 174 | 3 | 41 |
| `RD` | 3 | 66.5 | 66.96 | **67.14** | +0.69% | +0.96% | 2,878 | 238 | 2,679 |
| `SSP` | 1 | 57.7 | 55.42 | **56.15** | -3.95% | -2.69% | 166 | 10 | 134 |

