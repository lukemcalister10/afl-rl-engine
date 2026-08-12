# MOVERS_TABLE — ORDER 24B, THE ψ COLUMN BESIDE a100

Issue #334, ORDER 24B. Branch `build/pool-quality`, stacked on ORDER 24's `build/pool-dial`.
Pre-registration: `PREREG_ORDER24B.md`, committed **before** any measurement or code change.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

---

## 1. The seven boards

| column | what it is | md5 |
|---|---|---|
| `pre_act` | main @ `7f4d5d2`, the last board-touching main commit before PR #462 | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` | `origin/main` today | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` | committed on `land/pool-update` / this branch | `665311ca72576df6ff0bbf6dfd007739` |
| `a025` | ORDER 24, α = 0.25 | `322df660ccce6c017ded341403b7215f` |
| `a050` | ORDER 24, α = 0.50 | `87214d5653e0fb8e48b804f1a890b6bc` |
| `a100` | ORDER 24, α = 1.00 — the pure delivery fix | `ca3544d8df9272db191a67001a1bb9e4` |
| **`psi`** | **ORDER 24B — the quality-conditioned premium** | **`e2bf7347e07c08f1efbdda17d6601e4e`** |

The first six are ORDER 24's **recorded** boards, re-used and re-pinned by md5 in `o24b_table.py`
before a single row is read. The ψ board was built twice from scratch and produced `e2bf7347`
both times.

## 2. The separation law

| check | a100 | psi |
|---|---:|---:|
| national rows on the board (`ty==ND`, pick ≤ 64) | 561 | 561 |
| **ND movers vs live `1dbd1480`** | **0** | **0** |
| ND rows absent | 0 | 0 |
| ND board value (live: 620,877) | 620,877 | 620,877 |

`o24b_table.py` **asserts this and raises before it writes anything at all** — the Q table, the
movers table and the JSON are all downstream of the assertion.

## 3. Pool totals

| board | pool total | vs live | vs live % | moved vs live | moved vs `pr469` | **moved vs `a100`** |
|---|---:|---:|---:|---:|---:|---:|
| `pre_act` | 123,243 | -1,923 | -1.536% | 119 | 205 | **204** |
| `live` | 125,166 | 0 | +0.000% | 0 | 117 | **118** |
| `pr469` | 132,960 | 7,794 | +6.227% | 117 | 0 | **44** |
| `a025` | 135,583 | 10,417 | +8.323% | 119 | 89 | **89** |
| `a050` | 134,590 | 9,424 | +7.529% | 119 | 89 | **89** |
| `a100` | 132,734 | 7,568 | +6.046% | 118 | 44 | **0** |
| `psi` | 132,342 | 7,176 | +5.733% | 118 | 44 | **33** |

## 4. Who can move at all, and who did

| cell (243 pool rows) | n | moved `a100` → `psi` |
|---|---:|---:|
| full participants, `φ = 1` — anchor share **exactly 0** | 146 | **0** |
| **partial participants, `0 < φ < 1`** | **42** | **33** |
| current sitters, `φ = 0` — `M = R`, no premium leg exists | 55 | **0** |

**Movers outside the partial cell: 0**, asserted. That is not a happy accident — it is the
arithmetic. A sitter reads `R` and never touches `U″`; a full participant carries an anchor share
of exactly zero, so no multiplier of any kind reaches his price. **ψ can only reach a pool player
who is playing, but not yet playing a full load.**

## 5. The direction law, verified on every one of the 42 partials

```
M_psi - M_a100  =  phi * (U'-1) * ( q/qbar - 1 )
```
so a partial with `q > qbar` **rises** and one with `q < qbar` **falls** — the price never enters
the decision, only the quality does. Measured across all 42 partials: **0 violations**.
26 rows moved down, 7 moved up, 9 sat still because the move was below one point at integer
rounding (deep careers whose evidence fade has all but extinguished the anchor leg).

## 6. THE EIGHT NAMED ROWS

| player | pathway | g26 | avg26 | d | par | **q** | φ | pre_act | live | pr469 | a025 | a050 | a100 | **psi** | ψ−a100 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `mani-liddy` | MSD | 0 | — | 2 | 62.48 | **0.0000** | 0.0000 | 128 | 128 | 1025 | 285 | 238 | 168 | **168** | +0 |
| `robert-hansen` | MSD | 0 | — | 4 | 61.70 | **0.0000** | 0.0000 | 80 | 80 | 650 | 215 | 190 | 143 | **143** | +0 |
| `nicholas-martin` | SSP | 0 | — | 5 | 56.88 | **0.0000** | 0.0000 | 2828 | 2822 | 3520 | 3517 | 3515 | 3513 | **3513** | +0 |
| `marcus-herbert` | MSD | 8 | 88.87 | 1 | 56.89 | **1.0000** | 1.0000 | 1053 | 906 | 906 | 906 | 906 | 906 | **906** | +0 |
| `jai-newcombe` | MSD | 21 | 103.15 | 6 | 61.70 | **1.0000** | 1.0000 | 4887 | 4883 | 4883 | 4883 | 4883 | 4883 | **4883** | +0 |
| `harrison-ramm` | MSD | 4 | 28.75 | 2 | 62.48 | **0.4602** | 0.7246 | 320 | 351 | 406 | 555 | 578 | 620 | **567** | -53 |
| `luker-kentfield` | MSD | 3 | 32.33 | 3 | 62.81 | **0.5147** | 0.5435 | 179 | 178 | 268 | 454 | 468 | 496 | **449** | -47 |
| `vigo-visentini` | RD | 1 | 84.0 | 3 | 67.14 | **1.0000** | 0.1812 | 167 | 168 | 150 | 242 | 222 | 182 | **183** | +1 |

- `mani-liddy` — NAMED (order) — ORDER 24 defect case: MSD 2025 pick 15, 0 games 2026. phi=0, so psi cannot reach him: 168 EXACT is the test.
- `robert-hansen` — NAMED (order) — the second ORDER 24 defect case, same mechanism, same phi=0 test
- `nicholas-martin` — NAMED (order) — established SSP career, 0 games 2026: phi=0, evidence-faded anchor
- `marcus-herbert` — NAMED (order) — healthy currently-playing pool rookie, 8 games 2026 (phi=1, anchor share exactly 0)
- `jai-newcombe` — NAMED (order) — established MSD star, 21 games 2026 (phi=1, anchor share exactly 0)
- `harrison-ramm` — NAMED (order) — THE ORDER 24B DEFECT CASE: MSD, 4 games 2026 at 28.75, collected the full MSD premium 406 -> 620
- `luker-kentfield` — NAMED (order) — MSD, 3 games 2026 at 32.33, the second quality-blind lift
- `vigo-visentini` — NAMED (order) — RD ruck, 1 game 2026 at 84.00: quality ABOVE par, earned a fraction. The row the clip is for.

## 7. Top movers `a100` → `psi`

### Down (26 rows)

| player | pathway | avg26 | par | **q** | φ | a100 | **psi** | Δ |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `caleb-lewis` | MSD | 12.50 | 62.48 | **0.2001** | 0.3623 | 349 | **258** | -91 |
| `jacob-newton` | MSD | 27.70 | 62.48 | **0.4434** | 0.5000 | 377 | **320** | -57 |
| `harrison-ramm` | MSD | 28.75 | 62.48 | **0.4602** | 0.7246 | 620 | **567** | -53 |
| `luker-kentfield` | MSD | 32.33 | 62.81 | **0.5147** | 0.5435 | 496 | **449** | -47 |
| `max-ramsden` | MSD | 40.50 | 61.70 | **0.6564** | 0.3623 | 321 | **292** | -29 |
| `noah-howes` | MSD | 32.00 | 62.48 | **0.5122** | 0.1812 | 282 | **255** | -27 |
| `flynn-young` | MSD | 44.00 | 62.48 | **0.7042** | 0.5435 | 203 | **186** | -17 |
| `lukas-cooke` | MSD | 43.50 | 56.89 | **0.7646** | 0.3623 | 421 | **404** | -17 |
| `tom-cochrane` | RD | 30.67 | 63.50 | **0.4830** | 0.5435 | 239 | **229** | -10 |
| `hudson-o-keeffe` | SSP | 29.70 | 56.88 | **0.5222** | 0.5435 | 288 | **279** | -9 |
| `will-mclachlan` | MSD | 28.00 | 62.81 | **0.4458** | 0.1812 | 163 | **155** | -8 |
| `balyn-o-brien` | SSP | 26.75 | 56.15 | **0.4764** | 0.7246 | 394 | **386** | -8 |
| `ollie-greeves` | RD | 44.00 | 60.36 | **0.7290** | 0.7246 | 589 | **582** | -7 |
| `tom-hanily` | MSD | 47.50 | 62.81 | **0.7562** | 0.7246 | 232 | **225** | -7 |
| `aidan-johnson` | ND>64 | 34.00 | 59.81 | **0.5684** | 0.1812 | 237 | **230** | -7 |

### Up (7 rows)

| player | pathway | avg26 | par | **q** | φ | a100 | **psi** | Δ |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `oliver-francou` | MSD | 71.50 | 56.89 | **1.0000** | 0.7246 | 590 | **601** | +11 |
| `flynn-riley` | MSD | 80.00 | 56.89 | **1.0000** | 0.1812 | 428 | **434** | +6 |
| `jaxon-artemis` | MSD | 54.25 | 56.89 | **0.9536** | 0.7246 | 536 | **542** | +6 |
| `alex-van-wyk` | MSD | 69.00 | 56.89 | **1.0000** | 0.1812 | 427 | **433** | +6 |
| `jordan-boyd` | MSD | 66.00 | 61.70 | **1.0000** | 0.3623 | 62 | **65** | +3 |
| `shadeau-brain` | PDA | 54.50 | 54.04 | **1.0000** | 0.3623 | 118 | **120** | +2 |
| `vigo-visentini` | RD | 84.00 | 67.14 | **1.0000** | 0.1812 | 182 | **183** | +1 |

## 8. THE TABLE — 152 rows (151 material, 1 named-only)

Materiality: any of `pre_act`, `pr469`, `a025`, `a050`, `a100`, `psi` differs from `live` by
**≥ 20 points or ≥ 10%%**. Pool rows only. The eight named rows are always present and flagged.
Material against live on the ψ column alone: **101** rows.

| player | pathway | pos | g26 | q | pre_act | live | pr469 | a025 | a050 | a100 | **psi** | ψ−a100 | named |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `mani-liddy` | MSD | MID | 0 | 0.000 | 128 | 128 | 1025 | 285 | 238 | 168 | **168** | +0 | **named** |
| `nicholas-martin` | SSP | MID | 0 | 0.000 | 2828 | 2822 | 3520 | 3517 | 3515 | 3513 | **3513** | +0 | **named** |
| `robert-hansen` | MSD | SF | 0 | 0.000 | 80 | 80 | 650 | 215 | 190 | 143 | **143** | +0 | **named** |
| `flynn-young` | MSD | SF | 3 | 0.704 | 128 | 128 | 502 | 176 | 184 | 203 | **186** | -17 |  |
| `james-blanck` | MSD | KPD | 0 | 0.000 | 60 | 60 | 431 | 125 | 105 | 79 | **79** | +0 |  |
| `caleb-may` | MSD | RUCK | 0 | 0.000 | 52 | 52 | 357 | 370 | 366 | 357 | **357** | +0 |  |
| `harrison-coe` | MSD | RUCK | 0 | 0.000 | 52 | 52 | 357 | 370 | 366 | 357 | **357** | +0 |  |
| `luker-kentfield` | MSD | KPF | 3 | 0.515 | 179 | 178 | 268 | 454 | 468 | 496 | **449** | -47 | **named** |
| `max-mapley` | MSD | RUCK | 0 | 0.000 | 52 | 52 | 357 | 370 | 366 | 357 | **357** | +0 |  |
| `max-beattie` | MSD | SF | 0 | 0.000 | 39 | 39 | 200 | 331 | 287 | 200 | **200** | +0 |  |
| `oliver-griffin` | MSD | SF | 0 | 0.000 | 39 | 39 | 200 | 331 | 287 | 200 | **200** | +0 |  |
| `harrison-ramm` | MSD | KPD | 4 | 0.460 | 320 | 351 | 406 | 555 | 578 | 620 | **567** | -53 | **named** |
| `will-mclachlan` | MSD | SF | 1 | 0.446 | 100 | 117 | 386 | 181 | 175 | 163 | **155** | -8 |  |
| `mitch-podhajski` | MSD | KPF | 2 | 0.853 | 195 | 186 | 303 | 387 | 407 | 448 | **443** | -5 |  |
| `iliro-smit` | MSD | RUCK | 0 | 0.000 | 100 | 100 | 227 | 337 | 300 | 227 | **227** | +0 |  |
| `ned-moyle` | MSD | RUCK | 14 | 1.000 | 2054 | 2285 | 2285 | 2285 | 2285 | 2285 | **2285** | +0 |  |
| `xavier-walsh` | RD | KPD | 0 | 0.000 | 86 | 86 | 143 | 314 | 257 | 143 | **143** | +0 |  |
| `luke-beecken` | MSD | MID | 0 | 0.000 | 100 | 100 | 182 | 326 | 278 | 182 | **182** | +0 |  |
| `oliver-francou` | MSD | MID | 4 | 1.000 | 345 | 375 | 397 | 527 | 550 | 590 | **601** | +11 |  |
| `noah-howes` | MSD | KPF | 1 | 0.512 | 128 | 128 | 185 | 353 | 330 | 282 | **255** | -27 |  |
| `jacob-newton` | MSD | SF | 3 | 0.443 | 156 | 156 | 201 | 345 | 355 | 377 | **320** | -57 |  |
| `max-ramsden` | MSD | KPF | 2 | 0.656 | 115 | 115 | 167 | 335 | 331 | 321 | **292** | -29 |  |
| `lukas-cooke` | MSD | KPD | 2 | 0.765 | 182 | 206 | 289 | 363 | 382 | 421 | **404** | -17 |  |
| `caleb-lewis` | MSD | KPF | 2 | 0.200 | 128 | 138 | 178 | 348 | 348 | 349 | **258** | -91 |  |
| `aidan-johnson` | ND>64 | KPF | 1 | 0.568 | 81 | 80 | 200 | 282 | 267 | 237 | **230** | -7 |  |
| `jaxon-artemis` | MSD | SD | 4 | 0.954 | 305 | 340 | 360 | 479 | 499 | 536 | **542** | +6 |  |
| `flynn-riley` | MSD | RUCK | 1 | 1.000 | 232 | 233 | 362 | 391 | 404 | 428 | **434** | +6 |  |
| `alex-van-wyk` | MSD | RUCK | 1 | 1.000 | 233 | 233 | 362 | 391 | 404 | 427 | **433** | +6 |  |
| `xavier-bamert` | MSD | SF | 8 | 0.751 | 313 | 509 | 509 | 509 | 509 | 509 | **509** | +0 |  |
| `zac-walker` | MSD | SD | 0 | 0.000 | 128 | 128 | 168 | 320 | 267 | 168 | **168** | +0 |  |
| `keighton-matofai-forbes` | ND>64 | SD | 0 | 0.000 | 65 | 65 | 105 | 247 | 197 | 105 | **105** | +0 |  |
| `lennox-hoffman` | ND>64 | SD | 0 | 0.000 | 65 | 65 | 105 | 247 | 197 | 105 | **105** | +0 |  |
| `river-stevens` | ND>64 | SF | 0 | 0.000 | 65 | 65 | 105 | 247 | 197 | 105 | **105** | +0 |  |
| `logan-smith` | ND>64 | RUCK | 0 | 0.000 | 91 | 91 | 185 | 270 | 241 | 185 | **185** | +0 |  |
| `jack-henderson` | SSP | SF | 0 | 0.000 | 88 | 88 | 115 | 265 | 215 | 115 | **115** | +0 |  |
| `tom-hanily` | MSD | SF | 4 | 0.756 | 142 | 154 | 331 | 207 | 216 | 232 | **225** | -7 |  |
| `hudson-o-keeffe` | SSP | KPF | 3 | 0.522 | 143 | 136 | 185 | 311 | 303 | 288 | **279** | -9 |  |
| `chris-scerri` | SSP | SF | 7 | 0.848 | 285 | 459 | 459 | 459 | 459 | 459 | **459** | +0 |  |
| `jordan-boyd` | MSD | SD | 2 | 1.000 | 37 | 37 | 201 | 65 | 64 | 62 | **65** | +3 |  |
| `ben-jepson` | SSP | MID | 4 | 0.749 | 88 | 88 | 110 | 244 | 240 | 234 | **228** | -6 |  |
| `cooper-trembath` | MSD | KPF | 21 | 1.000 | 2051 | 2201 | 2201 | 2201 | 2201 | 2201 | **2201** | +0 |  |
| `marcus-herbert` | MSD | SD | 8 | 1.000 | 1053 | 906 | 906 | 906 | 906 | 906 | **906** | +0 | **named** |
| `anthony-caminiti` | SSP | KPF | 18 | 0.779 | 976 | 1110 | 1110 | 1110 | 1110 | 1110 | **1110** | +0 |  |
| `patrick-retschko` | RD | MID | 16 | 1.000 | 1483 | 1608 | 1608 | 1608 | 1608 | 1608 | **1608** | +0 |  |
| `fred-rodriguez` | RD | MID | 0 | 0.000 | 143 | 143 | 200 | 267 | 245 | 200 | **200** | +0 |  |
| `harry-charleson` | RD | SD | 0 | 0.000 | 86 | 86 | 105 | 210 | 175 | 105 | **105** | +0 |  |
| `nick-driscoll` | RD | MID | 0 | 0.000 | 143 | 143 | 200 | 267 | 245 | 200 | **200** | +0 |  |
| `riley-onley` | RD | MID | 0 | 0.000 | 143 | 143 | 200 | 267 | 245 | 200 | **200** | +0 |  |
| `josh-draper` | PDN | KPD | 0 | 0.000 | 274 | 315 | 432 | 400 | 396 | 389 | **389** | +0 |  |
| `ollie-greeves` | RD | MID | 4 | 0.729 | 421 | 475 | 498 | 575 | 580 | 589 | **582** | -7 |  |
| `thomas-burton` | SSP | SF | 5 | 0.702 | 305 | 415 | 418 | 438 | 439 | 441 | **439** | -2 |  |
| `tom-cochrane` | RD | SF | 3 | 0.483 | 146 | 148 | 147 | 257 | 251 | 239 | **229** | -10 |  |
| `nathan-wardius` | PDA | SF | 0 | 0.000 | 54 | 54 | 75 | 160 | 132 | 75 | **75** | +0 |  |
| `asher-eastham` | RD | SF | 0 | 0.000 | 81 | 81 | 93 | 186 | 155 | 93 | **93** | +0 |  |
| `zak-johnson` | ND>64 | SD | 7 | 0.874 | 634 | 730 | 730 | 730 | 730 | 730 | **730** | +0 |  |
| `balyn-o-brien` | SSP | SD | 4 | 0.476 | 263 | 300 | 310 | 395 | 395 | 394 | **386** | -8 |  |
| `campbell-lake` | MSD | SF | 7 | 0.994 | 67 | 161 | 161 | 161 | 161 | 161 | **161** | +0 |  |
| `aiden-riddle` | RD | RUCK | 0 | 0.000 | 140 | 140 | 152 | 232 | 205 | 152 | **152** | +0 |  |
| `joe-pike` | RD | RUCK | 0 | 0.000 | 140 | 140 | 152 | 232 | 205 | 152 | **152** | +0 |  |
| `archer-day-wicks` | RD | SF | 19 | 0.762 | 675 | 766 | 766 | 766 | 766 | 766 | **766** | +0 |  |
| `leon-kickett` | RD | SF | 0 | 0.000 | 112 | 112 | 151 | 200 | 184 | 151 | **151** | +0 |  |
| `tyrell-dewar` | PDN | SF | 0 | 0.000 | 68 | 73 | 161 | 111 | 106 | 96 | **96** | +0 |  |
| `liam-hetherton` | PDA | KPF | 0 | 0.000 | 100 | 100 | 164 | 182 | 176 | 164 | **164** | +0 |  |
| `andy-moniz-wakefield` | PDN | SD | 2 | 0.491 | 25 | 27 | 108 | 65 | 64 | 61 | **55** | -6 |  |
| `josh-lai` | SSP | SD | 16 | 1.000 | 516 | 597 | 597 | 597 | 597 | 597 | **597** | +0 |  |
| `caleb-graham` | ND>64 | KPD | 0 | 0.000 | 38 | 37 | 117 | 84 | 74 | 54 | **54** | +0 |  |
| `isaiah-dudley` | SSP | SF | 21 | 1.000 | 160 | 234 | 234 | 234 | 234 | 234 | **234** | +0 |  |
| `vigo-visentini` | RD | RUCK | 1 | 1.000 | 167 | 168 | 150 | 242 | 222 | 182 | **183** | +1 | **named** |
| `lachlan-mcandrew` | SSP | RUCK | 20 | 1.000 | 1208 | 1279 | 1279 | 1279 | 1279 | 1279 | **1279** | +0 |  |
| `riley-hamilton` | PDA | SF | 6 | 0.661 | 234 | 305 | 305 | 305 | 305 | 305 | **305** | +0 |  |
| `hugo-hall-kahan` | MSD | SD | 9 | 1.000 | 148 | 215 | 215 | 215 | 215 | 215 | **215** | +0 |  |
| `james-o-donnell` | UNR | KPD | 17 | 0.901 | 660 | 727 | 727 | 727 | 727 | 727 | **727** | +0 |  |
| `shadeau-brain` | PDA | SD | 2 | 1.000 | 78 | 69 | 134 | 124 | 124 | 118 | **120** | +2 |  |
| `noah-chamberlain` | PDA | SF | 0 | 0.000 | 87 | 87 | 85 | 150 | 112 | 85 | **85** | +0 |  |
| `archie-may` | MSD | KPF | 10 | 0.765 | 415 | 476 | 476 | 476 | 476 | 476 | **476** | +0 |  |
| `kye-annand` | MSD | KPD | 9 | 1.000 | 181 | 239 | 239 | 239 | 239 | 239 | **239** | +0 |  |
| `bodhi-uwland` | PDA | SD | 21 | 1.000 | 4141 | 4087 | 4087 | 4087 | 4087 | 4087 | **4087** | +0 |  |
| `patrick-voss` | RD | KPF | 20 | 0.945 | 1592 | 1538 | 1538 | 1538 | 1538 | 1538 | **1538** | +0 |  |
| `rob-monahan` | IRE | SD | 0 | 0.000 | 37 | 37 | 45 | 90 | 75 | 45 | **45** | +0 |  |
| `finnbar-maley` | RD | KPF | 6 | 0.616 | 240 | 192 | 192 | 192 | 192 | 192 | **192** | +0 |  |
| `liam-reidy` | RD | RUCK | 4 | 0.902 | 328 | 291 | 246 | 328 | 329 | 331 | **331** | +0 |  |
| `darragh-joyce` | IRE | KPD | 3 | 0.719 | 21 | 20 | 64 | 47 | 46 | 43 | **41** | -2 |  |
| `karl-worner` | RD | SD | 21 | 1.000 | 1250 | 1206 | 1206 | 1206 | 1206 | 1206 | **1206** | +0 |  |
| `cillian-burke` | IRE | SD | 0 | 0.000 | 47 | 47 | 43 | 90 | 74 | 43 | **43** | +0 |  |
| `eamonn-armstrong` | IRE | SD | 0 | 0.000 | 47 | 47 | 43 | 90 | 74 | 43 | **43** | +0 |  |
| `mark-keane` | SSP | KPD | 7 | 1.000 | 1514 | 1557 | 1557 | 1557 | 1557 | 1557 | **1557** | +0 |  |
| `matt-duffy` | IRE | SD | 0 | 0.000 | 47 | 47 | 43 | 90 | 74 | 43 | **43** | +0 |  |
| `benny-barrett` | PDN | SF | 0 | 0.000 | 43 | 43 | 50 | 85 | 73 | 50 | **50** | +0 |  |
| `max-heath` | MSD | RUCK | 7 | 0.833 | 640 | 682 | 682 | 682 | 682 | 682 | **682** | +0 |  |
| `ricky-mentha` | PDN | SF | 0 | 0.000 | 43 | 43 | 50 | 85 | 73 | 50 | **50** | +0 |  |
| `ben-murphy` | IRE | SD | 0 | 0.000 | 60 | 60 | 85 | 101 | 95 | 85 | **85** | +0 |  |
| `cillian-bourke` | IRE | SD | 0 | 0.000 | 60 | 60 | 85 | 101 | 95 | 85 | **85** | +0 |  |
| `kobe-mcdonald` | IRE | SD | 0 | 0.000 | 60 | 60 | 85 | 101 | 95 | 85 | **85** | +0 |  |
| `ewan-mackinlay` | MSD | SF | 14 | 0.848 | 128 | 128 | 168 | 168 | 168 | 168 | **168** | +0 |  |
| `lachlan-blakiston` | MSD | KPD | 17 | 0.810 | 128 | 128 | 168 | 168 | 168 | 168 | **168** | +0 |  |
| `roan-steele` | MSD | MID | 16 | 0.870 | 128 | 128 | 168 | 168 | 168 | 168 | **168** | +0 |  |
| `zac-banch` | MSD | SF | 6 | 0.702 | 128 | 128 | 168 | 168 | 168 | 168 | **168** | +0 |  |
| `judd-mcvee` | RD | SD | 20 | 0.825 | 278 | 316 | 316 | 316 | 316 | 316 | **316** | +0 |  |
| `malakai-champion` | PDN | SF | 8 | 0.644 | 303 | 341 | 341 | 341 | 341 | 341 | **341** | +0 |  |
| `patrick-carr` | UNR | RUCK | 0 | 0.000 | 67 | 67 | 31 | 57 | 48 | 31 | **31** | +0 |  |
| `tylar-young` | RD | KPD | 21 | 0.901 | 244 | 279 | 279 | 279 | 279 | 279 | **279** | +0 |  |
| `jai-saxena` | PDN | SF | 0 | 0.000 | 60 | 60 | 84 | 93 | 89 | 84 | **84** | +0 |  |
| `jesse-mellor` | PDN | MID | 0 | 0.000 | 60 | 60 | 84 | 93 | 89 | 84 | **84** | +0 |  |
| `oscar-steene` | SSP | RUCK | 8 | 0.907 | 501 | 468 | 468 | 468 | 468 | 468 | **468** | +0 |  |
| `ryda-luke` | PDN | SF | 0 | 0.000 | 60 | 60 | 84 | 93 | 89 | 84 | **84** | +0 |  |
| `toby-whan` | PDN | SF | 0 | 0.000 | 60 | 60 | 84 | 93 | 89 | 84 | **84** | +0 |  |
| `tyson-stengle` | RD | SF | 0 | 0.000 | 121 | 121 | 153 | 152 | 152 | 151 | **151** | +0 |  |
| `jack-hutchinson` | MSD | MID | 5 | 0.713 | 100 | 100 | 131 | 131 | 131 | 131 | **131** | +0 |  |
| `oliver-hayes-brown` | UNR | RUCK | 7 | 0.771 | 221 | 190 | 190 | 190 | 190 | 190 | **190** | +0 |  |
| `saad-el-hawli` | MSD | SD | 8 | 0.849 | 100 | 100 | 131 | 131 | 131 | 131 | **131** | +0 |  |
| `max-hall` | MSD | SF | 21 | 1.000 | 2820 | 2790 | 2790 | 2790 | 2790 | 2790 | **2790** | +0 |  |
| `ned-long` | RD | MID | 19 | 0.959 | 1386 | 1416 | 1416 | 1416 | 1416 | 1416 | **1416** | +0 |  |
| `flynn-perez` | SSP | SD | 7 | 0.893 | 113 | 113 | 142 | 142 | 142 | 142 | **142** | +0 |  |
| `mitch-zadow` | SSP | SF | 7 | 0.692 | 113 | 113 | 142 | 142 | 142 | 142 | **142** | +0 |  |
| `paddy-cross` | SSP | SF | 10 | 0.827 | 113 | 113 | 142 | 142 | 142 | 142 | **142** | +0 |  |
| `will-lewis` | SSP | KPF | 11 | 0.836 | 113 | 113 | 142 | 142 | 142 | 142 | **142** | +0 |  |
| `tom-blamires` | SSP | SD | 15 | 1.000 | 113 | 114 | 142 | 142 | 142 | 142 | **142** | +0 |  |
| `kalani-white` | PDN | KPF | 0 | 0.000 | 67 | 67 | 84 | 93 | 90 | 84 | **84** | +0 |  |
| `jack-buller` | MSD | KPF | 10 | 0.565 | 80 | 80 | 105 | 105 | 105 | 105 | **105** | +0 |  |
| `tristan-xerri` | ND>64 | RUCK | 17 | 1.000 | 7825 | 7800 | 7800 | 7800 | 7800 | 7800 | **7800** | +0 |  |
| `jaime-uhr-henry` | UNR | RUCK | 0 | 0.000 | 51 | 51 | 27 | 56 | 47 | 27 | **27** | +0 |  |
| `james-borlase` | PDN | KPD | 15 | 1.000 | 448 | 424 | 424 | 424 | 424 | 424 | **424** | +0 |  |
| `jacob-moss` | UNR | KPF | 0 | 0.000 | 36 | 36 | 36 | 59 | 51 | 36 | **36** | +0 |  |
| `jayden-nguyen` | PDN | SD | 5 | 0.714 | 429 | 452 | 452 | 466 | 468 | 473 | **471** | -2 |  |
| `tom-edwards` | SSP | KPF | 7 | 0.814 | 88 | 88 | 110 | 110 | 110 | 110 | **110** | +0 |  |
| `josh-treacy` | RD | KPF | 21 | 1.000 | 6942 | 6921 | 6921 | 6921 | 6921 | 6921 | **6921** | +0 |  |
| `matt-hill` | UNR | SF | 2 | 0.382 | 48 | 49 | 36 | 70 | 67 | 63 | **57** | -6 |  |
| `zak-evans` | UNR | MID | 0 | 0.000 | 36 | 36 | 29 | 57 | 48 | 29 | **29** | +0 |  |
| `cooper-lord` | MSD | MID | 7 | 1.000 | 1325 | 1345 | 1345 | 1345 | 1345 | 1345 | **1345** | +0 |  |
| `harry-edwards` | RD | KPD | 2 | 0.152 | 92 | 97 | 117 | 110 | 108 | 105 | **104** | -1 |  |
| `wade-derksen` | MSD | KPD | 11 | 0.959 | 128 | 109 | 109 | 109 | 109 | 109 | **109** | +0 |  |
| `lachie-sullivan` | SSP | SF | 2 | 0.891 | 70 | 70 | 88 | 88 | 88 | 88 | **88** | +0 |  |
| `mykelti-lefau` | SSP | KPF | 19 | 0.942 | 70 | 70 | 88 | 88 | 88 | 88 | **88** | +0 |  |
| `joel-fitzgerald` | MSD | MID | 8 | 1.000 | 55 | 72 | 72 | 72 | 72 | 72 | **72** | +0 |  |
| `liam-puncher` | MSD | KPD | 6 | 0.653 | 107 | 124 | 124 | 124 | 124 | 124 | **124** | +0 |  |
| `oscar-berry` | UNR | KPD | 0 | 0.000 | 47 | 47 | 54 | 63 | 60 | 54 | **54** | +0 |  |
| `indy-cotton` | UNR | SD | 0 | 0.000 | 49 | 49 | 48 | 62 | 57 | 48 | **48** | +0 |  |
| `wil-parker` | UNR | SD | 5 | 0.659 | 29 | 29 | 18 | 22 | 23 | 25 | **24** | -1 |  |
| `toby-pink` | RD | KPD | 5 | 0.777 | 15 | 23 | 33 | 31 | 31 | 32 | **31** | -1 |  |
| `liam-o-connell` | IRE | SD | 11 | 0.789 | 45 | 39 | 39 | 39 | 39 | 39 | **39** | +0 |  |
| `daniel-butler` | ND>64 | SF | 8 | 0.438 | 10 | 10 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `jed-bews` | ND>64 | SD | 0 | 0.000 | 10 | 10 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `lincoln-mccarthy` | ND>64 | SF | 8 | 0.774 | 10 | 10 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `matt-guelfi` | ND>64 | SF | 3 | 0.482 | 10 | 10 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `nathan-broad` | ND>64 | SD | 20 | 0.876 | 10 | 10 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `jai-newcombe` | MSD | MID | 21 | 1.000 | 4887 | 4883 | 4883 | 4883 | 4883 | 4883 | **4883** | +0 | **named** |
| `jordon-butts` | RD | KPD | 9 | 0.705 | 15 | 15 | 18 | 18 | 18 | 18 | **18** | +0 |  |
| `oisin-mullin` | IRE | SD | 21 | 0.866 | 17 | 17 | 14 | 14 | 14 | 14 | **14** | +0 |  |
| `sam-switkowski` | ND>64 | SF | 21 | 0.801 | 12 | 12 | 15 | 15 | 15 | 15 | **15** | +0 |  |
| `mason-cox` | UNR | KPF | 14 | 0.637 | 5 | 5 | 3 | 3 | 3 | 3 | **3** | +0 |  |
| `matt-owies` | UNR | SF | 3 | 0.684 | 5 | 5 | 3 | 3 | 3 | 3 | **3** | +0 |  |
| `conor-mckenna` | IRE | SF | 15 | 0.733 | 7 | 7 | 6 | 6 | 6 | 6 | **6** | +0 |  |

One mover is **not** in this table: `brandon-zerk-thatcher` (a100 49 → ψ 48), which fails the
materiality bar against live on every column. It is in `Q_TABLE.md` and in the JSON.

