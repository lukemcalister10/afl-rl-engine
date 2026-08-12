# PAR_TABLE_V2 — ORDER 25, THE AMENDED PLAYING PAR (all-pool same-depth donor)

Issue #334, ORDER 25. Branch `land/pool-update-v2`. Pre-registration: `PREREG_ORDER25.md`,
committed **before** this table was computed.

> **the landing configuration: alpha=1.0 current-state delivery, quality-conditioned premium, ALL-POOL SAME-DEPTH par donor (owner amendment 2026-08-12); levels RE-TRUED in this act**

---

## 1. The amendment, in one line

**Owner, verbatim** (#334 comment [5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)):

> "I feel like MSD pars should borrow from the wider pool given the thin sample. Do they not?"

```
ORDER 24B:  par(pw,d) = w*par_own(pw,d) + (1-w)*par_donor(pw)   donor = the PATHWAY's ALL-DEPTH par
ORDER 25:   par(pw,d) = w*par_own(pw,d) + (1-w)*par_all(d)      donor = the ALL-POOL SAME-DEPTH par
            w = n/(n+10),  n = the RAW EXACT-DEPTH CELL COUNT   [unchanged]
```

This is the **ORDER 21 class-axis convention**, adopted exactly: `o22_make_relaxed_surface.py`
lines 109–127 shrink each class cell toward the **all-class same-depth cell** at K=10 on the raw
exact-depth cell count. ORDER 24B carried the K and the weight but pointed the donor down the
wrong axis. **An empty cell _is_ its donor**, so the pathways with no deep careers — MSD, SSP,
PDN — were being told that a fourth-year player is measured against their own first-year
average. They are now measured against fourth-year players.

### The weight's `n`, declared

The brief says "K=10 on games". This table reads that as **the par itself is games-weighted**
— it is, at every cell, own and donor alike — and keeps `n` as the **cell count**, for two
reasons: it is the named ORDER 21 convention, and it is the reading under which thin cells
borrow **more**, which is the purpose of the amendment. The alternative reading
(`w = games/(games+10)`) is computed and published in §6 rather than argued away. Under it MSD
d1 would weight its own 9-cell sample at 0.800 instead of 0.474 — borrowing **less** from the
wider pool, the opposite of the instruction.

## 2. The population, and the gate

The same complete-window harvest that produced `R` and `q`, byte-identical to ORDER 24B's
(`ucells.json` md5 `68bc25e7e0c95cc75ee7fa013bacabcd`, re-run from scratch on this branch and
reproduced exactly). **National rows: 1390 encountered at the harvest gate and excluded, zero
present in this file — asserted before a single par is formed.**

| quantity | n |
|---|---:|
| complete-window cells with a priceable anchor | 3334 |
| of which **playing** with a usable average — **the par population** | **2323** |
| playing cells with no usable average (read as `q = 0`) | 1 |
| non-playing cells (`φ = 0`, no `q` exists) | 1010 |

## 3. THE AMENDED DONOR — the all-pool par at each depth

| depth | all-pool par | games | cells |
|---|---:|---:|---:|
| **d1** | **58.57** | 2,003 | 275 |
| **d2** | **60.56** | 3,074 | 343 |
| **d3** | **64.41** | 3,843 | 357 |
| **d4** | **69.65** | 3,883 | 292 |
| **d5** | **71.45** | 3,385 | 241 |
| **d6** | **75.63** | 11,761 | 815 |

**The donor now rises with depth (58.57 → 75.63)** instead of being one flat pathway number.
For comparison, the retired donors — each pathway's all-depth par — were: `RD` 71.29 · `ND>64` 67.52 · `IRE` 67.22 · `UNR` 68.11 · `PDA` 55.82 · `PDS` 59.68 · `MSD` 61.70 · `PDN` 60.07 · `SSP` 56.88.

## 4. THE PAR TABLE — every cell, both donors, and what was wired

| pathway | d | cells `n` | games | own par | OLD donor (retired) | **NEW donor** | w = n/(n+10) | **WIRED** | ORDER 24B wired | change |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `RD` | 1 | 194 | 1,437 | 59.80 | 71.29 | **58.57** | 0.9510 | **59.74** | 60.36 | -1.03% |
| `RD` | 2 | 229 | 2,185 | 63.16 | 71.29 | **60.56** | 0.9582 | **63.05** | 63.50 | -0.71% |
| `RD` | 3 | 238 | 2,679 | 66.96 | 71.29 | **64.41** | 0.9597 | **66.86** | 67.14 | -0.41% |
| `RD` | 4 | 211 | 2,883 | 71.26 | 71.29 | **69.65** | 0.9548 | **71.19** | 71.26 | -0.10% |
| `RD` | 5 | 176 | 2,568 | 72.39 | 71.29 | **71.45** | 0.9462 | **72.34** | 72.33 | +0.01% |
| `RD` | 6 | 650 | 9,574 | 75.79 | 71.29 | **75.63** | 0.9848 | **75.79** | 75.72 | +0.09% |
| `ND>64` | 1 | 37 | 254 | 60.22 | 67.52 | **58.57** | 0.7872 | **59.87** | 61.77 | -3.08% |
| `ND>64` | 2 | 55 | 441 | 58.41 | 67.52 | **60.56** | 0.8462 | **58.74** | 59.81 | -1.79% |
| `ND>64` | 3 | 53 | 519 | 61.25 | 67.52 | **64.41** | 0.8413 | **61.75** | 62.24 | -0.79% |
| `ND>64` | 4 | 44 | 535 | 65.66 | 67.52 | **69.65** | 0.8148 | **66.40** | 66.01 | +0.60% |
| `ND>64` | 5 | 34 | 414 | 67.40 | 67.52 | **71.45** | 0.7727 | **68.32** | 67.43 | +1.32% |
| `ND>64` | 6 | 93 | 1,285 | 75.43 | 67.52 | **75.63** | 0.9029 | **75.45** | 74.66 | +1.05% |
| `IRE` | 1 | 9 | 36 | 52.22 | 67.22 | **58.57** | 0.4737 | **55.56** | 60.12 | -7.58% |
| `IRE` | 2 | 15 | 99 | 54.65 | 67.22 | **60.56** | 0.6000 | **57.01** | 59.68 | -4.47% |
| `IRE` | 3 | 17 | 160 | 58.16 | 67.22 | **64.41** | 0.6296 | **60.47** | 61.52 | -1.70% |
| `IRE` | 4 | 13 | 137 | 64.84 | 67.22 | **69.65** | 0.5652 | **66.93** | 65.88 | +1.60% |
| `IRE` | 5 | 10 | 124 | 66.82 | 67.22 | **71.45** | 0.5000 | **69.13** | 67.02 | +3.15% |
| `IRE` | 6 | 25 | 329 | 78.20 | 67.22 | **75.63** | 0.7143 | **77.47** | 75.07 | +3.20% |
| `UNR` | 1 | 5 | 42 | 40.00 | 68.11 | **58.57** | 0.3333 | **52.38** | 58.74 | -10.83% |
| `UNR` | 2 | 14 | 110 | 58.92 | 68.11 | **60.56** | 0.5833 | **59.60** | 62.75 | -5.01% |
| `UNR` | 3 | 16 | 141 | 61.96 | 68.11 | **64.41** | 0.6154 | **62.90** | 64.32 | -2.21% |
| `UNR` | 4 | 11 | 131 | 74.00 | 68.11 | **69.65** | 0.5238 | **71.93** | 71.20 | +1.03% |
| `UNR` | 5 | 9 | 133 | 75.17 | 68.11 | **71.45** | 0.4737 | **73.21** | 71.45 | +2.46% |
| `UNR` | 6 | 18 | 282 | 72.90 | 68.11 | **75.63** | 0.6429 | **73.87** | 71.19 | +3.77% |
| `PDA` | 1 | 8 | 45 | 51.62 | 55.82 | **58.57** | 0.4444 | **55.48** | 53.95 | +2.83% |
| `PDA` | 2 | 15 | 124 | 30.39 | 55.82 | **60.56** | 0.6000 | **42.46** | 40.56 | +4.67% |
| `PDA` | 3 | 14 | 184 | 48.81 | 55.82 | **64.41** | 0.5833 | **55.31** | 51.73 | +6.92% |
| `PDA` | 4 | 8 | 144 | 51.81 | 55.82 | **69.65** | 0.4444 | **61.72** | 54.04 | +14.22% |
| `PDA` | 5 | 7 | 86 | 72.43 | 55.82 | **71.45** | 0.4118 | **71.85** | 62.66 | +14.67% |
| `PDA` | 6 | 17 | 188 | 75.93 | 55.82 | **75.63** | 0.6296 | **75.82** | 68.48 | +10.71% |
| `PDS` | 1 | 1 | 11 | 49.73 | 59.68 | **58.57** | 0.0909 | **57.77** | 58.78 | -1.72% |
| `PDS` | 2 | 3 | 10 | 30.30 | 59.68 | **60.56** | 0.2308 | **53.58** | 52.90 | +1.28% |
| `PDS` | 3 | 3 | 7 | 40.86 | 59.68 | **64.41** | 0.2308 | **58.97** | 55.34 | +6.57% |
| `PDS` | 4 | 2 | 21 | 73.21 | 59.68 | **69.65** | 0.1667 | **70.24** | 61.94 | +13.41% |
| `PDS` | 5 | 5 | 60 | 58.89 | 59.68 | **71.45** | 0.3333 | **67.26** | 59.42 | +13.20% |
| `PDS` | 6 | 12 | 103 | 62.58 | 59.68 | **75.63** | 0.5455 | **68.51** | 61.26 | +11.84% |
| `MSD` | 1 | 9 | 40 | 51.55 | 61.70 | **58.57** | 0.4737 | **55.24** | 56.89 | -2.89% |
| `MSD` | 2 | 3 | 41 | 65.08 | 61.70 | **60.56** | 0.2308 | **61.60** | 62.48 | -1.40% |
| `MSD` | 3 | 2 | 40 | 68.38 | 61.70 | **64.41** | 0.1667 | **65.07** | 62.81 | +3.60% |
| `MSD` | 4 | 0 | 0 | _empty — **the donor IS the par**_ | 61.70 | **69.65** | 0.0000 | **69.65** | 61.70 | +12.89% |
| `MSD` | 5 | 0 | 0 | _empty — **the donor IS the par**_ | 61.70 | **71.45** | 0.0000 | **71.45** | 61.70 | +15.80% |
| `MSD` | 6 | 0 | 0 | _empty — **the donor IS the par**_ | 61.70 | **75.63** | 0.0000 | **75.63** | 61.70 | +22.59% |
| `PDN` | 1 | 2 | 4 | 43.50 | 60.07 | **58.57** | 0.1667 | **56.06** | 57.31 | -2.19% |
| `PDN` | 2 | 3 | 12 | 58.18 | 60.07 | **60.56** | 0.2308 | **60.01** | 59.64 | +0.63% |
| `PDN` | 3 | 7 | 29 | 49.71 | 60.07 | **64.41** | 0.4118 | **58.36** | 55.81 | +4.57% |
| `PDN` | 4 | 3 | 32 | 72.25 | 60.07 | **69.65** | 0.2308 | **70.25** | 62.88 | +11.71% |
| `PDN` | 5 | 0 | 0 | _empty — **the donor IS the par**_ | 60.07 | **71.45** | 0.0000 | **71.45** | 60.07 | +18.93% |
| `PDN` | 6 | 0 | 0 | _empty — **the donor IS the par**_ | 60.07 | **75.63** | 0.0000 | **75.63** | 60.07 | +25.90% |
| `SSP` | 1 | 10 | 134 | 55.42 | 56.88 | **58.57** | 0.5000 | **56.99** | 56.15 | +1.50% |
| `SSP` | 2 | 6 | 52 | 59.21 | 56.88 | **60.56** | 0.3750 | **60.06** | 57.75 | +3.98% |
| `SSP` | 3 | 7 | 84 | 57.76 | 56.88 | **64.41** | 0.4118 | **61.67** | 57.24 | +7.74% |
| `SSP` | 4 | 0 | 0 | _empty — **the donor IS the par**_ | 56.88 | **69.65** | 0.0000 | **69.65** | 56.88 | +22.45% |
| `SSP` | 5 | 0 | 0 | _empty — **the donor IS the par**_ | 56.88 | **71.45** | 0.0000 | **71.45** | 56.88 | +25.61% |
| `SSP` | 6 | 0 | 0 | _empty — **the donor IS the par**_ | 56.88 | **75.63** | 0.0000 | **75.63** | 56.88 | +32.97% |
| `ALL POOL` | 1 | 275 | 2,003 | 58.57 | 69.87 | **58.57** | 0.9649 | **58.57** | 58.97 | -0.67% |
| `ALL POOL` | 2 | 343 | 3,074 | 60.56 | 69.87 | **60.56** | 0.9717 | **60.56** | 60.82 | -0.43% |
| `ALL POOL` | 3 | 357 | 3,843 | 64.41 | 69.87 | **64.41** | 0.9728 | **64.41** | 64.56 | -0.23% |
| `ALL POOL` | 4 | 292 | 3,883 | 69.65 | 69.87 | **69.65** | 0.9669 | **69.65** | 69.66 | -0.01% |
| `ALL POOL` | 5 | 241 | 3,385 | 71.45 | 69.87 | **71.45** | 0.9602 | **71.45** | 71.38 | +0.09% |
| `ALL POOL` | 6 | 815 | 11,761 | 75.63 | 69.87 | **75.63** | 0.9879 | **75.63** | 75.56 | +0.09% |

**The eight cells the amendment moves most:** `SSP` d6 +33.0% · `PDN` d6 +25.9% · `SSP` d5 +25.6% · `MSD` d6 +22.6% · `SSP` d4 +22.5% · `PDN` d5 +18.9% · `MSD` d5 +15.8% · `PDA` d5 +14.7%.
Every one of the largest is an **empty or near-empty deep cell** — exactly the population the
owner named.

## 5. Monotonicity in depth — reported, never projected

| pathway | d1 | d2 | d3 | d4 | d5 | d6 | steps |
|---|---:|---:|---:|---:|---:|---:|---|
| `RD` | 59.74 | 63.05 | 66.86 | 71.19 | 72.34 | 75.79 | ↑ ↑ ↑ ↑ ↑ |
| `ND>64` | 59.87 | 58.74 | 61.75 | 66.40 | 68.32 | 75.45 | ↓ ↑ ↑ ↑ ↑ |
| `IRE` | 55.56 | 57.01 | 60.47 | 66.93 | 69.13 | 77.47 | ↑ ↑ ↑ ↑ ↑ |
| `UNR` | 52.38 | 59.60 | 62.90 | 71.93 | 73.21 | 73.87 | ↑ ↑ ↑ ↑ ↑ |
| `PDA` | 55.48 | 42.46 | 55.31 | 61.72 | 71.85 | 75.82 | ↓ ↑ ↑ ↑ ↑ |
| `PDS` | 57.77 | 53.58 | 58.97 | 70.24 | 67.26 | 68.51 | ↓ ↑ ↑ ↓ ↑ |
| `MSD` | 55.24 | 61.60 | 65.07 | 69.65 | 71.45 | 75.63 | ↑ ↑ ↑ ↑ ↑ |
| `PDN` | 56.06 | 60.01 | 58.36 | 70.25 | 71.45 | 75.63 | ↑ ↓ ↑ ↑ ↑ |
| `SSP` | 56.99 | 60.06 | 61.67 | 69.65 | 71.45 | 75.63 | ↑ ↑ ↑ ↑ ↑ |
| `ALL POOL` | 58.57 | 60.56 | 64.41 | 69.65 | 71.45 | 75.63 | ↑ ↑ ↑ ↑ ↑ |

**6 of 10 pathways are now monotone in depth**, against 2 of 10 under ORDER 24B. No isotonic
projection is applied and none is wanted — the repair is a consequence of pointing the donor
down the depth axis, not of imposing a shape.

## 6. The declared sensitivity — the other reading of "K=10 on games"

`w = games/(games+10)` instead of `w = cells/(cells+10)`. **Not wired.** Cells differing by
≥ 0.5 points:

| pathway | d | w (cells, wired) | w (games) | **WIRED** | wired under games reading | diff |
|---|---:|---:|---:|---:|---:|---:|
| `ND>64` | 4 | 0.8148 | 0.9817 | **66.40** | 65.73 | -0.67 |
| `ND>64` | 5 | 0.7727 | 0.9764 | **68.32** | 67.50 | -0.82 |
| `IRE` | 1 | 0.4737 | 0.7826 | **55.56** | 53.60 | -1.96 |
| `IRE` | 2 | 0.6000 | 0.9083 | **57.01** | 55.19 | -1.82 |
| `IRE` | 3 | 0.6296 | 0.9412 | **60.47** | 58.53 | -1.95 |
| `IRE` | 4 | 0.5652 | 0.9320 | **66.93** | 65.17 | -1.77 |
| `IRE` | 5 | 0.5000 | 0.9254 | **69.13** | 67.16 | -1.97 |
| `IRE` | 6 | 0.7143 | 0.9705 | **77.47** | 78.13 | +0.66 |
| `UNR` | 1 | 0.3333 | 0.8077 | **52.38** | 43.57 | -8.81 |
| `UNR` | 2 | 0.5833 | 0.9167 | **59.60** | 59.06 | -0.55 |
| `UNR` | 3 | 0.6154 | 0.9338 | **62.90** | 62.12 | -0.78 |
| `UNR` | 4 | 0.5238 | 0.9291 | **71.93** | 73.69 | +1.76 |
| `UNR` | 5 | 0.4737 | 0.9301 | **73.21** | 74.91 | +1.70 |
| `UNR` | 6 | 0.6429 | 0.9658 | **73.87** | 72.99 | -0.88 |
| `PDA` | 1 | 0.4444 | 0.8182 | **55.48** | 52.88 | -2.60 |
| `PDA` | 2 | 0.6000 | 0.9254 | **42.46** | 32.64 | -9.82 |
| `PDA` | 3 | 0.5833 | 0.9485 | **55.31** | 49.61 | -5.69 |
| `PDA` | 4 | 0.4444 | 0.9351 | **61.72** | 52.97 | -8.75 |
| `PDS` | 1 | 0.0909 | 0.5238 | **57.77** | 53.94 | -3.83 |
| `PDS` | 2 | 0.2308 | 0.5000 | **53.58** | 45.43 | -8.15 |
| `PDS` | 3 | 0.2308 | 0.4118 | **58.97** | 54.71 | -4.26 |
| `PDS` | 4 | 0.1667 | 0.6774 | **70.24** | 72.06 | +1.82 |
| `PDS` | 5 | 0.3333 | 0.8571 | **67.26** | 60.68 | -6.58 |
| `PDS` | 6 | 0.5455 | 0.9115 | **68.51** | 63.74 | -4.78 |
| `MSD` | 1 | 0.4737 | 0.8000 | **55.24** | 52.95 | -2.29 |
| `MSD` | 2 | 0.2308 | 0.8039 | **61.60** | 64.19 | +2.59 |
| `MSD` | 3 | 0.1667 | 0.8000 | **65.07** | 67.59 | +2.52 |
| `PDN` | 1 | 0.1667 | 0.2857 | **56.06** | 54.26 | -1.79 |
| `PDN` | 2 | 0.2308 | 0.5455 | **60.01** | 59.26 | -0.75 |
| `PDN` | 3 | 0.4118 | 0.7436 | **58.36** | 53.48 | -4.88 |
| `PDN` | 4 | 0.2308 | 0.7619 | **70.25** | 71.63 | +1.38 |
| `SSP` | 1 | 0.5000 | 0.9306 | **56.99** | 55.64 | -1.36 |
| `SSP` | 2 | 0.3750 | 0.8387 | **60.06** | 59.43 | -0.62 |
| `SSP` | 3 | 0.4118 | 0.8936 | **61.67** | 58.47 | -3.20 |

Worst difference across all cells: **9.82 points**. Under the games reading every thin cell
borrows **less** from the wider pool — the opposite of the owner's instruction — which is the
ground on which the cell-count reading is adopted.

