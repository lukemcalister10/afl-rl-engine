# UPRIME2_TABLE — ORDER 24B, U″ RE-DERIVED UNDER THE QUALITY-CONDITIONED DELIVERY

Issue #334, ORDER 24B. Branch `build/pool-quality`. Pre-registration: `PREREG_ORDER24B.md`,
committed **before** any U″ was derived.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

---

## 1. The instrument

```
mean = SUM e*[ (1-phi)*R + phi*(1 + q*(U''-1)) ] / SUM e  ==  1.0000000000     HALT if it is not
=>  U'' = 1 + [ SUM e*(1-phi)*(1-R) ] / [ SUM e*phi*q ]
```
Entry weights `e = level(division) * _PL_F` and the population are ORDER 21's, carried verbatim;
`_b_factor == 1.0` is proven on every harvested row. The **numerator is identical to ORDER 24's**,
so the whole move is a denominator move, and the identity

```
U'' - 1  =  (U' - 1) * ( SUM e*phi / SUM e*phi*q )  =  (U' - 1) / qbar,    qbar = the q-mass ratio
```

is computed **independently** in `o24b_uderive.py` and residualised. **U″ ≥ U′ for every pathway,
always** — premium mass shrinks under q-weighting, so the surviving premium must be larger to
redistribute the same total. That is not an assumption: it follows from `q ≤ 1` by the clip.

## 2. U″ vs U′, and the q-mass per pathway

| pathway | cells | sit mass `Σe(1−φ)` | play mass `Σeφ` | **q-mass `Σeφq`** | **qbar** | U (ORDER 21/23) | U′ (ORDER 24, α=1) | **U″ (ORDER 24B)** | (U″−1)/(U′−1) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `RD` | 2352 | 243,343 | 409,450 | **360,474** | **0.8804** | 1.2063 | 1.239884 | **1.272476** | 1.1359 |
| `ND>64` | 441 | 58,960 | 79,345 | **68,324** | **0.8611** | 1.3687 | 1.361599 | **1.419927** | 1.1613 |
| `IRE` | 137 | 7,530 | 7,753 | **6,681** | **0.8617** | 1.3380 | 1.326308 | **1.378674** | 1.1605 |
| `UNR` | 126 | 4,503 | 4,249 | **3,626** | **0.8534** | 1.5041 | 1.510685 | **1.598397** | 1.1718 |
| `PDA` | 106 | 10,189 | 10,783 | **9,600** | **0.8903** | 1.6144 | 1.575357 | **1.646263** | 1.1232 |
| `PDS` | 62 | 2,524 | 1,130 | **946** | **0.8376** | 1.4160 | 1.779469 | **1.930577** | 1.1939 |
| `MSD` | 40 | 11,349 | 4,395 | **3,955** | **0.9000** | 3.0959 | 1.904002 | **2.004494** | 1.1112 |
| `PDN` | 36 | 2,728 | 909 | **813** | **0.8941** | 2.0956 | 1.770823 | **1.862162** | 1.1185 |
| `SSP` | 34 | 3,868 | 7,404 | **6,807** | **0.9194** | 1.2001 | 1.167647 | **1.182345** | 1.0877 |
| `ALL POOL` | 3334 | 344,994 | 525,417 | **461,226** | **0.8778** | 1.2522 | 1.275231 | **1.313536** | 1.1392 |

`qbar = Σeφq / Σeφ` is the share of the premium mass that survives the quality condition. It sits
between **0.8376** (`PDS`) and **0.9194** (`SSP`) — comfortably below 1, because the clip at `q = 1`
removes all of the upside and none of the downside, and well above 0, because par is a
games-weighted mean of the very averages `q` is formed from.

**The ordering across pathways is unchanged.** `U″ − 1 = (U′ − 1)/qbar` and `qbar` varies far less
(0.8376–0.9194) than `U′ − 1` does (0.1676–0.9040), so the rank order of the nine pathways is identical
under U′ and U″.

## 3. The MSD row, read plainly

MSD's premium moves **1.904002 → 2.004494**. Ninety per cent of MSD's historical premium mass survives
the quality condition (`qbar = 0.9000`), so the premium each surviving unit carries rises by
**11.12%**. A currently-playing MSD row at par therefore collects **more** than it did at α=1.0;
a row at half par collects roughly half of a larger number, which is materially less. **That is
the whole mechanism**: the premium is not smaller, it is *aimed*.

## 4. Mean preservation — the HALT instrument

| pathway | post-redistribution entry-weighted mean of M |
|---|---|
| `RD` | `1.0000000000` |
| `ND>64` | `1.0000000000` |
| `IRE` | `1.0000000000` |
| `UNR` | `1.0000000000` |
| `PDA` | `1.0000000000` |
| `PDS` | `1.0000000000` |
| `MSD` | `1.0000000000` |
| `PDN` | `1.0000000000` |
| `SSP` | `1.0000000000` |
| `ALL POOL` | `1.0000000000` |

All ten rows print `1.0000000000` to a tolerance of `1e-9`. `o24b_uderive.py` **asserts** this and
raises before it writes a surface; the build cannot proceed past a failure.

The identity `U″−1 == (U′−1)/qbar`, computed the other way round, residualises to
`2.220e-16` — floating-point exact.

## 5. The control — non-vacuity

`o24b_uderive.py ... CONTROL` forces `q = 1` on every cell and must reproduce ORDER 24's U′ from
the same file. It does, to a worst absolute difference of **4.638e-11** — the α=1.0 surface
artifact's own 10-decimal-place rounding, not a derivation difference. The ORDER 24B machinery is
therefore ORDER 24's machinery with exactly one factor added, and the added factor is the only
thing that moves. The transcript is `UDERIVE_CONTROL_out.txt`; the ψ run is `UDERIVE_psi_out.txt`.

## 6. What produced these numbers

| file | what |
|---|---|
| `o24b_uharvest.py` | the harvest, ORDER 21's gates verbatim + `avg_y` |
| `o24b_par.py` | the par table (`PAR_TABLE.md`) |
| `o24b_uderive.py` | this table's numbers, and `SURFACE_psi.json` |
| `SURFACE_psi.json` | the ψ surface as built — retention block unchanged from ORDER 24's α=1.0, `uplift` = U″, `par` + `par_all` carried alongside |

