# U′ PER PATHWAY PER α — ORDER 24, CURRENT-STATE DELIVERY

Issue #334, ORDER 24. Branch `build/pool-dial`, based on `land/pool-update`.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

## What was re-derived, and why it had to be

`U` is the mean-preserving uplift the pathway's participating rows carry so that the sitter
retention `R` redistributes **inside** the pathway rather than being a net charge. ORDER 21/22/23
derived it against a **career-state** partition. ORDER 24 delivers `R` and `U` against **current**
participation, so the same instrument must be re-solved with each cell weighted by its own
`phi = min(gy/(6·fe), 1)` instead of by a career-state flag:

```
mean = SUM_all e·[ (1-phi)·R' + phi·U' ] / SUM_all e  ==  1.0000000000   (asserted; HALTS otherwise)
U'   = 1 + [ SUM_all e·(1-phi)·(1-R') ] / [ SUM_all e·phi ]
R'   = 1 + alpha·(R - 1)
```

Entry weights `e = pool_level(division) · _PL_F` are unchanged (`_b_factor == 1.0`, re-asserted in
the harvest). The signed levels are **read from `engine/rl_after/pvc_curve_v2.json` as committed on
this branch** and are not modified — the ND65+ cap-removal law as landed.

## The harvest control — the new instrument reproduces the landed table on the old delivery

Run with the career-state partition (`phi := 0 if sitout else 1`) the ORDER 24 instrument must
reproduce the `uplift` block of `engine/rl_after/pool_retention_surface.json` exactly. It does:

| pathway | landed U | reproduced | \|diff\| |
|---|---:|---:|---:|
| RD | 1.2063266569 | 1.2063266569 | 2.994e-11 |
| ND>64 | 1.3686704435 | 1.3686704435 | 4.839e-11 |
| IRE | 1.3379685672 | 1.3379685672 | 3.581e-11 |
| UNR | 1.5040535246 | 1.5040535246 | 9.831e-12 |
| PDA | 1.6144369057 | 1.6144369057 | 3.962e-11 |
| PDS | 1.4159780385 | 1.4159780385 | 3.846e-11 |
| MSD | 3.0959013333 | 3.0959013333 | 3.333e-11 |
| PDN | 2.0955998571 | 2.0955998571 | 4.286e-11 |
| SSP | 1.2000961905 | 1.2000961905 | 2.381e-11 |

Worst |diff| = 4.839e-11 — the 10-decimal rounding of the committed artifact, nothing else.
**CONTROL PASSES.** The population, the gates and the weights are the ORDER 21 ones.

## The population, split both ways

    national rows encountered and EXCLUDED at the harvest gate: 1390
    cells harvested 4241   complete-window with a priceable anchor 3334
    _b_factor == 1.0 on every harvested row: ASSERTED (violations 0)
    _PL_F = 1.0524
    season fractions present in the harvest window: {1.0: 3334}  (1.0 everywhere == completed seasons)
    THE TWO DELIVERIES ON ONE POPULATION
    CAREER-state sitters (ORDER 21/22/23 flag) .......... 1325 of 3334 cells (0.3974 by count)
    CURRENT-state: phi == 0 (no games at all this season)  1010 cells
    CURRENT-state: 0 < phi < 1 (partial participation) ... 656 cells
    CURRENT-state: phi == 1 (at or above the bar) ........ 1668 cells
    CAREER non-sitters sitting out THIS season (the Liddy cell in history): 74 cells
    CAREER sitters PARTLY playing this season .............................. 389 cells

The two deliveries disagree about **463 of 3,334 cells** (74 career non-sitters sitting out the
season — the Liddy cell in history — plus 389 career sitters partly playing). That disagreement is
the whole of the U′ move.

## U′ per pathway per α

| pathway | landed U (career delivery) | **U′ α=0.25** | **U′ α=0.50** | **U′ α=1.00** | Δ U′(1.00) vs landed |
|---|---:|---:|---:|---:|---:|
| RD | 1.206327 | 1.059971 | 1.119942 | **1.239884** | +0.033557 |
| ND>64 | 1.368670 | 1.090400 | 1.180799 | **1.361599** | -0.007071 |
| IRE | 1.337969 | 1.081577 | 1.163154 | **1.326308** | -0.011660 |
| UNR | 1.504054 | 1.127671 | 1.255342 | **1.510685** | +0.006631 |
| PDA | 1.614437 | 1.143839 | 1.287679 | **1.575357** | -0.039080 |
| PDS | 1.415978 | 1.194867 | 1.389734 | **1.779469** | +0.363491 |
| MSD | 3.095901 | 1.226001 | 1.452001 | **1.904002** | -1.191899 |
| PDN | 2.095600 | 1.192706 | 1.385412 | **1.770823** | -0.324777 |
| SSP | 1.200096 | 1.041912 | 1.083824 | **1.167647** | -0.032449 |
| ALL POOL | 1.252214 | 1.068808 | 1.137615 | **1.275231** | +0.023016 |

**The dial is exactly linear in α, and it acts identically on both halves of the pair.** Because
`(1−R′) = α(1−R)` and the denominator `Σ e·phi` is α-free, `U′(α) − 1 == α·(U′(1.00) − 1)` to
floating precision. Checked on every pathway:

| pathway | U′(1.00)−1 | α·(U′(1.00)−1) at 0.25 vs measured | at 0.50 vs measured | max abs residual |
|---|---:|---|---|---:|
| RD | 0.239884089 | 0.059971022 / 0.059971022 | 0.119942044 / 0.119942044 | 5.0e-11 |
| ND>64 | 0.361598993 | 0.090399748 / 0.090399748 | 0.180799496 / 0.180799496 | 1.1e-16 |
| IRE | 0.326308225 | 0.081577056 / 0.081577056 | 0.163154113 / 0.163154113 | 5.0e-11 |
| UNR | 0.510684807 | 0.127671202 / 0.127671202 | 0.255342403 / 0.255342403 | 5.0e-11 |
| PDA | 0.575357346 | 0.143839336 / 0.143839336 | 0.287678673 / 0.287678673 | 1.1e-16 |
| PDS | 0.779468783 | 0.194867196 / 0.194867196 | 0.389734391 / 0.389734391 | 5.0e-11 |
| MSD | 0.904002358 | 0.226000590 / 0.226000590 | 0.452001179 / 0.452001179 | 5.0e-11 |
| PDN | 0.770823296 | 0.192705824 / 0.192705824 | 0.385411648 / 0.385411648 | 5.0e-11 |
| SSP | 0.167647492 | 0.041911873 / 0.041911873 | 0.083823746 / 0.083823746 | 5.0e-11 |
| ALL POOL | 0.275230752 | 0.068807688 / 0.068807688 | 0.137615376 / 0.137615376 | 5.0e-11 |

## Sit shares and mean R′ (the mean-preservation proof output, α-by-α)

`sit mass` = `Σ e·(1−phi)`, `play mass` = `Σ e·phi`, both in entry-anchor currency and both
**α-invariant** (the dial moves R, never the weights). `post-redist mean` is the instrument that
halts the build.

### α = 0.25

| pathway | cells | sit mass | play mass | sit share | mean R′ | U′ | post-redist mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| RD | 2352 | 243343.3 | 409449.9 | 0.3728 | 0.899093 | 1.059971 | 1.0000000000 |
| ND>64 | 441 | 58959.7 | 79344.6 | 0.4263 | 0.878345 | 1.090400 | 1.0000000000 |
| IRE | 137 | 7529.9 | 7753.0 | 0.4927 | 0.916006 | 1.081577 | 1.0000000000 |
| UNR | 126 | 4503.2 | 4248.5 | 0.5146 | 0.879549 | 1.127671 | 1.0000000000 |
| PDA | 106 | 10189.3 | 10782.9 | 0.4858 | 0.847782 | 1.143839 | 1.0000000000 |
| PDS | 62 | 2524.4 | 1129.6 | 0.6909 | 0.912803 | 1.194867 | 1.0000000000 |
| MSD | 40 | 11348.7 | 4395.2 | 0.7208 | 0.912474 | 1.226001 | 1.0000000000 |
| PDN | 36 | 2727.8 | 909.3 | 0.7500 | 0.935765 | 1.192706 | 1.0000000000 |
| SSP | 34 | 3867.6 | 7403.6 | 0.3431 | 0.919769 | 1.041912 | 1.0000000000 |
| ALL POOL | 3334 | 344993.9 | 525416.7 | 0.3964 | 0.895208 | 1.068808 | 1.0000000000 |

### α = 0.50

| pathway | cells | sit mass | play mass | sit share | mean R′ | U′ | post-redist mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| RD | 2352 | 243343.3 | 409449.9 | 0.3728 | 0.798185 | 1.119942 | 1.0000000000 |
| ND>64 | 441 | 58959.7 | 79344.6 | 0.4263 | 0.756690 | 1.180799 | 1.0000000000 |
| IRE | 137 | 7529.9 | 7753.0 | 0.4927 | 0.832012 | 1.163154 | 1.0000000000 |
| UNR | 126 | 4503.2 | 4248.5 | 0.5146 | 0.759099 | 1.255342 | 1.0000000000 |
| PDA | 106 | 10189.3 | 10782.9 | 0.4858 | 0.695563 | 1.287679 | 1.0000000000 |
| PDS | 62 | 2524.4 | 1129.6 | 0.6909 | 0.825605 | 1.389734 | 1.0000000000 |
| MSD | 40 | 11348.7 | 4395.2 | 0.7208 | 0.824948 | 1.452001 | 1.0000000000 |
| PDN | 36 | 2727.8 | 909.3 | 0.7500 | 0.871529 | 1.385412 | 1.0000000000 |
| SSP | 34 | 3867.6 | 7403.6 | 0.3431 | 0.839537 | 1.083824 | 1.0000000000 |
| ALL POOL | 3334 | 344993.9 | 525416.7 | 0.3964 | 0.790415 | 1.137615 | 1.0000000000 |

### α = 1.00

| pathway | cells | sit mass | play mass | sit share | mean R′ | U′ | post-redist mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| RD | 2352 | 243343.3 | 409449.9 | 0.3728 | 0.596371 | 1.239884 | 1.0000000000 |
| ND>64 | 441 | 58959.7 | 79344.6 | 0.4263 | 0.513380 | 1.361599 | 1.0000000000 |
| IRE | 137 | 7529.9 | 7753.0 | 0.4927 | 0.664023 | 1.326308 | 1.0000000000 |
| UNR | 126 | 4503.2 | 4248.5 | 0.5146 | 0.518197 | 1.510685 | 1.0000000000 |
| PDA | 106 | 10189.3 | 10782.9 | 0.4858 | 0.391127 | 1.575357 | 1.0000000000 |
| PDS | 62 | 2524.4 | 1129.6 | 0.6909 | 0.651210 | 1.779469 | 1.0000000000 |
| MSD | 40 | 11348.7 | 4395.2 | 0.7208 | 0.649895 | 1.904002 | 1.0000000000 |
| PDN | 36 | 2727.8 | 909.3 | 0.7500 | 0.743059 | 1.770823 | 1.0000000000 |
| SSP | 34 | 3867.6 | 7403.6 | 0.3431 | 0.679075 | 1.167647 | 1.0000000000 |
| ALL POOL | 3334 | 344993.9 | 525416.7 | 0.3964 | 0.580831 | 1.275231 | 1.0000000000 |

**Every pathway prints `1.0000000000` at every α.** The instrument is able to fail — it is a hard
`assert` at 1e-9 in `o24_uderive.py` and it halts the build before a surface is written.

## Files

| file | what |
|---|---|
| `o24_uharvest.py` | the harvest, ORDER 21 gates carried, `gy`/`fe` added per cell |
| `o24_uderive.py` | the dial + the U′ instrument (and the CONTROL mode above) |
| `UHARVEST_out.txt`, `UDERIVE_CONTROL_out.txt`, `UDERIVE_a*.txt` | transcripts |
| `SURFACE_a0.25.json`, `SURFACE_a0.50.json`, `SURFACE_a1.00.json` | the three dialled surfaces as built |
