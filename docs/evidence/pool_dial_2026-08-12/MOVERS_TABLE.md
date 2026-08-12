# THE DIAL TABLE — ORDER 24

Issue #334, ORDER 24, the deliverable. Branch `build/pool-dial`, based on `land/pool-update`.
**Nothing here lands.** The owner picks α off this table; ONE full iteration at the chosen α then
builds the landing packet.

> **levels frozen at #469 values; absolute prices ±few points, MSD up to ~5%; re-trued at landing**

## The six boards

| column | board | md5 |
|---|---|---|
| `pre_act` | main @ `7f4d5d2`, the last board on main before PR #462 merged | `94f1fec59f99c59d5890d5975c79fa9b` |
| `live` | `origin/main` today | `1dbd1480a34c7823f330273211cbb76a` |
| `pr469` | the board committed on `land/pool-update` (PR #469, held) | `665311ca72576df6ff0bbf6dfd007739` |
| `a025` | this order, α = 0.25 | `322df660ccce6c017ded341403b7215f` |
| `a050` | this order, α = 0.50 | `87214d5653e0fb8e48b804f1a890b6bc` |
| `a100` | this order, α = 1.00 — the **pure delivery fix** | `ca3544d8df9272db191a67001a1bb9e4` |

## Attribution — what separates which columns

The α columns differ from `pr469` by **exactly one lever**: the current-state delivery fix plus the
dial (and the U′ re-derivation the fix forces, since mean preservation must hold under the new
delivery weights). Nothing else moves — same store, same signed levels read unmodified from
`pvc_curve_v2.json`, same config, same national code path.

`pr469`'s own three-lever ledger against `live` (H retirement · derived retention · repricing)
already exists at `docs/ledgers/POOL_UPDATE_MOVERS_2026-08-12.json` and is not re-derived here.
`pre_act → live` is the ORDER 20C par separation fix (PR #462), also already ledgered at
`docs/ledgers/PAR_FIX_MOVERS_2026-08-12.json`.

## Separation — asserted, not claimed

| check | a025 | a050 | a100 |
|---|---:|---:|---:|
| national board rows (`ty==ND`, pick ≤ 64) | 561 | 561 | 561 |
| **ND movers vs live `1dbd1480`** | **0** | **0** | **0** |
| ND board value | 620,877 | 620,877 | 620,877 |

ND board value on live: **620,877** — unmoved to the point on all three.
A single ND mover is a hard failure that stops the build; `o24_table.py` asserts it before it
writes anything.

## Pool totals

| board | pool total | Δ vs live | % | moved vs live | up | down | moved vs pr469 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `pre_act` | 123,243 | -1,923 | -1.536% | 119 | 58 | 61 | 205 |
| `live` | 125,166 | 0 | +0.000% | 0 | 0 | 0 | 117 |
| `pr469` | 132,960 | 7,794 | +6.227% | 117 | 96 | 21 | 0 |
| `a025` | 135,583 | 10,417 | +8.323% | 119 | 109 | 10 | 89 |
| `a050` | 134,590 | 9,424 | +7.529% | 119 | 108 | 11 | 89 |
| `a100` | 132,734 | 7,568 | +6.046% | 118 | 101 | 17 | 44 |

## Who the fix reaches, and who it cannot

A pool row feels the pool multiplier only through its **anchor share**, and
`_a_share = (1−lam)·exp(−E_q/1.1)` with `lam` saturating at `LAM_SIT[6] = 1.0`. A pool player at or
above this season's prorated 6-game bar therefore carries an anchor share of **exactly zero**.

| cell | n | moved vs `pr469` at α=0.25 | α=0.50 | α=1.00 |
|---|---:|---:|---:|---:|
| full participants (`gy ≥ 6·fe`) — anchor share exactly 0 | 146 | 0 | 0 | 0 |
| partial participants (`0 < gy < 6·fe`) | 42 | 33 | 33 | 33 |
| current sitters WITH a prior qualifying season — **the Liddy cell** | 10 | 8 | 8 | 8 |
| current sitters with no prior qualifying season | 45 | 45 | 45 | 0 |

(Counts above are over the rows that appear in the table; rows absent from the table are
non-material in every column. The authoritative per-cell counts, taken over all 243 pool rows, are
in `TABLE_out.txt`: full 0/0/0 · partial 36/36/36 · Liddy cell 8/8/8 · never-qualified 45/45/**0**.)

**At α=1.00 the 45 never-qualified current sitters are byte-identical to `pr469`** — `phi=0` and
`R′=R` give back exactly the landed multiplier. They move only when the dial moves, which is what
makes α=1.00 the pure delivery fix.

## The named five — included regardless of materiality

| player | why named | pre_act | live | pr469 | **a025** | **a050** | **a100** | g26 | qual seasons pre-2026 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `mani-liddy` | NAMED (order) — the defect case: MSD 2025 pick 15, 9 games 2025, 0 games 2026 | 128 | 128 | 1025 | **285** | **238** | **168** | 0 | 1 |
| `robert-hansen` | NAMED (order) — the second defect case, same mechanism | 80 | 80 | 650 | **215** | **190** | **143** | 0 | 2 |
| `nicholas-martin` | NAMED (order) — established SSP career, 0 games 2026: same cell, evidence-faded anchor | 2828 | 2822 | 3520 | **3517** | **3515** | **3513** | 0 | 4 |
| `marcus-herbert` | NAMED (build) — healthy currently-playing pool rookie: MSD 2026 pick 13, 8 games 2026 (phi=1) | 1053 | 906 | 906 | **906** | **906** | **906** | 8 | 0 |
| `jai-newcombe` | NAMED (build) — established multi-season MSD star: highest live-board MSD value, 6 qualifying seasons, 21 games 2026 | 4887 | 4883 | 4883 | **4883** | **4883** | **4883** | 21 | 5 |

Selection criteria for the two rows this build chose, stated in the pre-registration before any
board was built: the **rookie** is a pool row whose first professional season is the current one,
with current-season games comfortably above the prorated bar (`phi = 1.0` exactly) and unmoved by
PR #469, so his α columns isolate this order's lever alone; the **MSD star** is the highest
live-board value among MSD rows with ≥5 qualifying seasons and currently playing. Both are
predicted — and measured — to be **completely untouched at every α**, which is the property the
fix exists to deliver.

## The table

Pool rows only. A row appears if **any** column differs from `live` by ≥20 points **or** ≥10%,
sorted by max |Δ| vs live. **152 rows** (151 material, 1 named-only). Material against live on at least one α column: **112 rows**.

| # | player | pathway | pos | g26 | pre_act | live | pr469 | **a025** | **a050** | **a100** | Δ a100 vs live | Δ a100 vs pr469 |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `mani-liddy` **NAMED** | MSD | MID | 0 | 128 | 128 | 1025 | **285** | **238** | **168** | +40 | -857 |
| 2 | `nicholas-martin` **NAMED** | SSP | MID | 0 | 2828 | 2822 | 3520 | **3517** | **3515** | **3513** | +691 | -7 |
| 3 | `robert-hansen` **NAMED** | MSD | SF | 0 | 80 | 80 | 650 | **215** | **190** | **143** | +63 | -507 |
| 4 | `flynn-young` | MSD | SF | 3 | 128 | 128 | 502 | **176** | **184** | **203** | +75 | -299 |
| 5 | `james-blanck` | MSD | KPD | 0 | 60 | 60 | 431 | **125** | **105** | **79** | +19 | -352 |
| 6 | `caleb-may` | MSD | RUCK | 0 | 52 | 52 | 357 | **370** | **366** | **357** | +305 | +0 |
| 7 | `harrison-coe` | MSD | RUCK | 0 | 52 | 52 | 357 | **370** | **366** | **357** | +305 | +0 |
| 8 | `luker-kentfield` | MSD | KPF | 3 | 179 | 178 | 268 | **454** | **468** | **496** | +318 | +228 |
| 9 | `max-mapley` | MSD | RUCK | 0 | 52 | 52 | 357 | **370** | **366** | **357** | +305 | +0 |
| 10 | `max-beattie` | MSD | SF | 0 | 39 | 39 | 200 | **331** | **287** | **200** | +161 | +0 |
| 11 | `oliver-griffin` | MSD | SF | 0 | 39 | 39 | 200 | **331** | **287** | **200** | +161 | +0 |
| 12 | `harrison-ramm` | MSD | KPD | 4 | 320 | 351 | 406 | **555** | **578** | **620** | +269 | +214 |
| 13 | `will-mclachlan` | MSD | SF | 1 | 100 | 117 | 386 | **181** | **175** | **163** | +46 | -223 |
| 14 | `mitch-podhajski` | MSD | KPF | 2 | 195 | 186 | 303 | **387** | **407** | **448** | +262 | +145 |
| 15 | `iliro-smit` | MSD | RUCK | 0 | 100 | 100 | 227 | **337** | **300** | **227** | +127 | +0 |
| 16 | `ned-moyle` | MSD | RUCK | 14 | 2054 | 2285 | 2285 | **2285** | **2285** | **2285** | +0 | +0 |
| 17 | `xavier-walsh` | RD | KPD | 0 | 86 | 86 | 143 | **314** | **257** | **143** | +57 | +0 |
| 18 | `luke-beecken` | MSD | MID | 0 | 100 | 100 | 182 | **326** | **278** | **182** | +82 | +0 |
| 19 | `noah-howes` | MSD | KPF | 1 | 128 | 128 | 185 | **353** | **330** | **282** | +154 | +97 |
| 20 | `jacob-newton` | MSD | SF | 3 | 156 | 156 | 201 | **345** | **355** | **377** | +221 | +176 |
| 21 | `max-ramsden` | MSD | KPF | 2 | 115 | 115 | 167 | **335** | **331** | **321** | +206 | +154 |
| 22 | `lukas-cooke` | MSD | KPD | 2 | 182 | 206 | 289 | **363** | **382** | **421** | +215 | +132 |
| 23 | `oliver-francou` | MSD | MID | 4 | 345 | 375 | 397 | **527** | **550** | **590** | +215 | +193 |
| 24 | `caleb-lewis` | MSD | KPF | 2 | 128 | 138 | 178 | **348** | **348** | **349** | +211 | +171 |
| 25 | `aidan-johnson` | ND>64 | KPF | 1 | 81 | 80 | 200 | **282** | **267** | **237** | +157 | +37 |
| 26 | `jaxon-artemis` | MSD | SD | 4 | 305 | 340 | 360 | **479** | **499** | **536** | +196 | +176 |
| 27 | `xavier-bamert` | MSD | SF | 8 | 313 | 509 | 509 | **509** | **509** | **509** | +0 | +0 |
| 28 | `flynn-riley` | MSD | RUCK | 1 | 232 | 233 | 362 | **391** | **404** | **428** | +195 | +66 |
| 29 | `alex-van-wyk` | MSD | RUCK | 1 | 233 | 233 | 362 | **391** | **404** | **427** | +194 | +65 |
| 30 | `zac-walker` | MSD | SD | 0 | 128 | 128 | 168 | **320** | **267** | **168** | +40 | +0 |
| 31 | `keighton-matofai-forbes` | ND>64 | SD | 0 | 65 | 65 | 105 | **247** | **197** | **105** | +40 | +0 |
| 32 | `lennox-hoffman` | ND>64 | SD | 0 | 65 | 65 | 105 | **247** | **197** | **105** | +40 | +0 |
| 33 | `river-stevens` | ND>64 | SF | 0 | 65 | 65 | 105 | **247** | **197** | **105** | +40 | +0 |
| 34 | `logan-smith` | ND>64 | RUCK | 0 | 91 | 91 | 185 | **270** | **241** | **185** | +94 | +0 |
| 35 | `jack-henderson` | SSP | SF | 0 | 88 | 88 | 115 | **265** | **215** | **115** | +27 | +0 |
| 36 | `tom-hanily` | MSD | SF | 4 | 142 | 154 | 331 | **207** | **216** | **232** | +78 | -99 |
| 37 | `hudson-o-keeffe` | SSP | KPF | 3 | 143 | 136 | 185 | **311** | **303** | **288** | +152 | +103 |
| 38 | `chris-scerri` | SSP | SF | 7 | 285 | 459 | 459 | **459** | **459** | **459** | +0 | +0 |
| 39 | `jordan-boyd` | MSD | SD | 2 | 37 | 37 | 201 | **65** | **64** | **62** | +25 | -139 |
| 40 | `ben-jepson` | SSP | MID | 4 | 88 | 88 | 110 | **244** | **240** | **234** | +146 | +124 |
| 41 | `cooper-trembath` | MSD | KPF | 21 | 2051 | 2201 | 2201 | **2201** | **2201** | **2201** | +0 | +0 |
| 42 | `marcus-herbert` **NAMED** | MSD | SD | 8 | 1053 | 906 | 906 | **906** | **906** | **906** | +0 | +0 |
| 43 | `anthony-caminiti` | SSP | KPF | 18 | 976 | 1110 | 1110 | **1110** | **1110** | **1110** | +0 | +0 |
| 44 | `patrick-retschko` | RD | MID | 16 | 1483 | 1608 | 1608 | **1608** | **1608** | **1608** | +0 | +0 |
| 45 | `fred-rodriguez` | RD | MID | 0 | 143 | 143 | 200 | **267** | **245** | **200** | +57 | +0 |
| 46 | `harry-charleson` | RD | SD | 0 | 86 | 86 | 105 | **210** | **175** | **105** | +19 | +0 |
| 47 | `nick-driscoll` | RD | MID | 0 | 143 | 143 | 200 | **267** | **245** | **200** | +57 | +0 |
| 48 | `riley-onley` | RD | MID | 0 | 143 | 143 | 200 | **267** | **245** | **200** | +57 | +0 |
| 49 | `josh-draper` | PDN | KPD | 0 | 274 | 315 | 432 | **400** | **396** | **389** | +74 | -43 |
| 50 | `ollie-greeves` | RD | MID | 4 | 421 | 475 | 498 | **575** | **580** | **589** | +114 | +91 |
| 51 | `thomas-burton` | SSP | SF | 5 | 305 | 415 | 418 | **438** | **439** | **441** | +26 | +23 |
| 52 | `tom-cochrane` | RD | SF | 3 | 146 | 148 | 147 | **257** | **251** | **239** | +91 | +92 |
| 53 | `nathan-wardius` | PDA | SF | 0 | 54 | 54 | 75 | **160** | **132** | **75** | +21 | +0 |
| 54 | `asher-eastham` | RD | SF | 0 | 81 | 81 | 93 | **186** | **155** | **93** | +12 | +0 |
| 55 | `zak-johnson` | ND>64 | SD | 7 | 634 | 730 | 730 | **730** | **730** | **730** | +0 | +0 |
| 56 | `balyn-o-brien` | SSP | SD | 4 | 263 | 300 | 310 | **395** | **395** | **394** | +94 | +84 |
| 57 | `campbell-lake` | MSD | SF | 7 | 67 | 161 | 161 | **161** | **161** | **161** | +0 | +0 |
| 58 | `aiden-riddle` | RD | RUCK | 0 | 140 | 140 | 152 | **232** | **205** | **152** | +12 | +0 |
| 59 | `joe-pike` | RD | RUCK | 0 | 140 | 140 | 152 | **232** | **205** | **152** | +12 | +0 |
| 60 | `archer-day-wicks` | RD | SF | 19 | 675 | 766 | 766 | **766** | **766** | **766** | +0 | +0 |
| 61 | `leon-kickett` | RD | SF | 0 | 112 | 112 | 151 | **200** | **184** | **151** | +39 | +0 |
| 62 | `tyrell-dewar` | PDN | SF | 0 | 68 | 73 | 161 | **111** | **106** | **96** | +23 | -65 |
| 63 | `liam-hetherton` | PDA | KPF | 0 | 100 | 100 | 164 | **182** | **176** | **164** | +64 | +0 |
| 64 | `andy-moniz-wakefield` | PDN | SD | 2 | 25 | 27 | 108 | **65** | **64** | **61** | +34 | -47 |
| 65 | `josh-lai` | SSP | SD | 16 | 516 | 597 | 597 | **597** | **597** | **597** | +0 | +0 |
| 66 | `caleb-graham` | ND>64 | KPD | 0 | 38 | 37 | 117 | **84** | **74** | **54** | +17 | -63 |
| 67 | `isaiah-dudley` | SSP | SF | 21 | 160 | 234 | 234 | **234** | **234** | **234** | +0 | +0 |
| 68 | `vigo-visentini` | RD | RUCK | 1 | 167 | 168 | 150 | **242** | **222** | **182** | +14 | +32 |
| 69 | `lachlan-mcandrew` | SSP | RUCK | 20 | 1208 | 1279 | 1279 | **1279** | **1279** | **1279** | +0 | +0 |
| 70 | `riley-hamilton` | PDA | SF | 6 | 234 | 305 | 305 | **305** | **305** | **305** | +0 | +0 |
| 71 | `hugo-hall-kahan` | MSD | SD | 9 | 148 | 215 | 215 | **215** | **215** | **215** | +0 | +0 |
| 72 | `james-o-donnell` | UNR | KPD | 17 | 660 | 727 | 727 | **727** | **727** | **727** | +0 | +0 |
| 73 | `shadeau-brain` | PDA | SD | 2 | 78 | 69 | 134 | **124** | **124** | **118** | +49 | -16 |
| 74 | `noah-chamberlain` | PDA | SF | 0 | 87 | 87 | 85 | **150** | **112** | **85** | -2 | +0 |
| 75 | `archie-may` | MSD | KPF | 10 | 415 | 476 | 476 | **476** | **476** | **476** | +0 | +0 |
| 76 | `kye-annand` | MSD | KPD | 9 | 181 | 239 | 239 | **239** | **239** | **239** | +0 | +0 |
| 77 | `bodhi-uwland` | PDA | SD | 21 | 4141 | 4087 | 4087 | **4087** | **4087** | **4087** | +0 | +0 |
| 78 | `patrick-voss` | RD | KPF | 20 | 1592 | 1538 | 1538 | **1538** | **1538** | **1538** | +0 | +0 |
| 79 | `rob-monahan` | IRE | SD | 0 | 37 | 37 | 45 | **90** | **75** | **45** | +8 | +0 |
| 80 | `finnbar-maley` | RD | KPF | 6 | 240 | 192 | 192 | **192** | **192** | **192** | +0 | +0 |
| 81 | `liam-reidy` | RD | RUCK | 4 | 328 | 291 | 246 | **328** | **329** | **331** | +40 | +85 |
| 82 | `darragh-joyce` | IRE | KPD | 3 | 21 | 20 | 64 | **47** | **46** | **43** | +23 | -21 |
| 83 | `karl-worner` | RD | SD | 21 | 1250 | 1206 | 1206 | **1206** | **1206** | **1206** | +0 | +0 |
| 84 | `cillian-burke` | IRE | SD | 0 | 47 | 47 | 43 | **90** | **74** | **43** | -4 | +0 |
| 85 | `eamonn-armstrong` | IRE | SD | 0 | 47 | 47 | 43 | **90** | **74** | **43** | -4 | +0 |
| 86 | `mark-keane` | SSP | KPD | 7 | 1514 | 1557 | 1557 | **1557** | **1557** | **1557** | +0 | +0 |
| 87 | `matt-duffy` | IRE | SD | 0 | 47 | 47 | 43 | **90** | **74** | **43** | -4 | +0 |
| 88 | `benny-barrett` | PDN | SF | 0 | 43 | 43 | 50 | **85** | **73** | **50** | +7 | +0 |
| 89 | `max-heath` | MSD | RUCK | 7 | 640 | 682 | 682 | **682** | **682** | **682** | +0 | +0 |
| 90 | `ricky-mentha` | PDN | SF | 0 | 43 | 43 | 50 | **85** | **73** | **50** | +7 | +0 |
| 91 | `ben-murphy` | IRE | SD | 0 | 60 | 60 | 85 | **101** | **95** | **85** | +25 | +0 |
| 92 | `cillian-bourke` | IRE | SD | 0 | 60 | 60 | 85 | **101** | **95** | **85** | +25 | +0 |
| 93 | `kobe-mcdonald` | IRE | SD | 0 | 60 | 60 | 85 | **101** | **95** | **85** | +25 | +0 |
| 94 | `ewan-mackinlay` | MSD | SF | 14 | 128 | 128 | 168 | **168** | **168** | **168** | +40 | +0 |
| 95 | `lachlan-blakiston` | MSD | KPD | 17 | 128 | 128 | 168 | **168** | **168** | **168** | +40 | +0 |
| 96 | `roan-steele` | MSD | MID | 16 | 128 | 128 | 168 | **168** | **168** | **168** | +40 | +0 |
| 97 | `zac-banch` | MSD | SF | 6 | 128 | 128 | 168 | **168** | **168** | **168** | +40 | +0 |
| 98 | `judd-mcvee` | RD | SD | 20 | 278 | 316 | 316 | **316** | **316** | **316** | +0 | +0 |
| 99 | `malakai-champion` | PDN | SF | 8 | 303 | 341 | 341 | **341** | **341** | **341** | +0 | +0 |
| 100 | `patrick-carr` | UNR | RUCK | 0 | 67 | 67 | 31 | **57** | **48** | **31** | -36 | +0 |
| 101 | `tylar-young` | RD | KPD | 21 | 244 | 279 | 279 | **279** | **279** | **279** | +0 | +0 |
| 102 | `jai-saxena` | PDN | SF | 0 | 60 | 60 | 84 | **93** | **89** | **84** | +24 | +0 |
| 103 | `jesse-mellor` | PDN | MID | 0 | 60 | 60 | 84 | **93** | **89** | **84** | +24 | +0 |
| 104 | `oscar-steene` | SSP | RUCK | 8 | 501 | 468 | 468 | **468** | **468** | **468** | +0 | +0 |
| 105 | `ryda-luke` | PDN | SF | 0 | 60 | 60 | 84 | **93** | **89** | **84** | +24 | +0 |
| 106 | `toby-whan` | PDN | SF | 0 | 60 | 60 | 84 | **93** | **89** | **84** | +24 | +0 |
| 107 | `tyson-stengle` | RD | SF | 0 | 121 | 121 | 153 | **152** | **152** | **151** | +30 | -2 |
| 108 | `jack-hutchinson` | MSD | MID | 5 | 100 | 100 | 131 | **131** | **131** | **131** | +31 | +0 |
| 109 | `oliver-hayes-brown` | UNR | RUCK | 7 | 221 | 190 | 190 | **190** | **190** | **190** | +0 | +0 |
| 110 | `saad-el-hawli` | MSD | SD | 8 | 100 | 100 | 131 | **131** | **131** | **131** | +31 | +0 |
| 111 | `max-hall` | MSD | SF | 21 | 2820 | 2790 | 2790 | **2790** | **2790** | **2790** | +0 | +0 |
| 112 | `ned-long` | RD | MID | 19 | 1386 | 1416 | 1416 | **1416** | **1416** | **1416** | +0 | +0 |
| 113 | `flynn-perez` | SSP | SD | 7 | 113 | 113 | 142 | **142** | **142** | **142** | +29 | +0 |
| 114 | `mitch-zadow` | SSP | SF | 7 | 113 | 113 | 142 | **142** | **142** | **142** | +29 | +0 |
| 115 | `paddy-cross` | SSP | SF | 10 | 113 | 113 | 142 | **142** | **142** | **142** | +29 | +0 |
| 116 | `will-lewis` | SSP | KPF | 11 | 113 | 113 | 142 | **142** | **142** | **142** | +29 | +0 |
| 117 | `tom-blamires` | SSP | SD | 15 | 113 | 114 | 142 | **142** | **142** | **142** | +28 | +0 |
| 118 | `kalani-white` | PDN | KPF | 0 | 67 | 67 | 84 | **93** | **90** | **84** | +17 | +0 |
| 119 | `jack-buller` | MSD | KPF | 10 | 80 | 80 | 105 | **105** | **105** | **105** | +25 | +0 |
| 120 | `tristan-xerri` | ND>64 | RUCK | 17 | 7825 | 7800 | 7800 | **7800** | **7800** | **7800** | +0 | +0 |
| 121 | `jaime-uhr-henry` | UNR | RUCK | 0 | 51 | 51 | 27 | **56** | **47** | **27** | -24 | +0 |
| 122 | `james-borlase` | PDN | KPD | 15 | 448 | 424 | 424 | **424** | **424** | **424** | +0 | +0 |
| 123 | `jacob-moss` | UNR | KPF | 0 | 36 | 36 | 36 | **59** | **51** | **36** | +0 | +0 |
| 124 | `jayden-nguyen` | PDN | SD | 5 | 429 | 452 | 452 | **466** | **468** | **473** | +21 | +21 |
| 125 | `tom-edwards` | SSP | KPF | 7 | 88 | 88 | 110 | **110** | **110** | **110** | +22 | +0 |
| 126 | `josh-treacy` | RD | KPF | 21 | 6942 | 6921 | 6921 | **6921** | **6921** | **6921** | +0 | +0 |
| 127 | `matt-hill` | UNR | SF | 2 | 48 | 49 | 36 | **70** | **67** | **63** | +14 | +27 |
| 128 | `zak-evans` | UNR | MID | 0 | 36 | 36 | 29 | **57** | **48** | **29** | -7 | +0 |
| 129 | `cooper-lord` | MSD | MID | 7 | 1325 | 1345 | 1345 | **1345** | **1345** | **1345** | +0 | +0 |
| 130 | `harry-edwards` | RD | KPD | 2 | 92 | 97 | 117 | **110** | **108** | **105** | +8 | -12 |
| 131 | `wade-derksen` | MSD | KPD | 11 | 128 | 109 | 109 | **109** | **109** | **109** | +0 | +0 |
| 132 | `lachie-sullivan` | SSP | SF | 2 | 70 | 70 | 88 | **88** | **88** | **88** | +18 | +0 |
| 133 | `mykelti-lefau` | SSP | KPF | 19 | 70 | 70 | 88 | **88** | **88** | **88** | +18 | +0 |
| 134 | `joel-fitzgerald` | MSD | MID | 8 | 55 | 72 | 72 | **72** | **72** | **72** | +0 | +0 |
| 135 | `liam-puncher` | MSD | KPD | 6 | 107 | 124 | 124 | **124** | **124** | **124** | +0 | +0 |
| 136 | `oscar-berry` | UNR | KPD | 0 | 47 | 47 | 54 | **63** | **60** | **54** | +7 | +0 |
| 137 | `indy-cotton` | UNR | SD | 0 | 49 | 49 | 48 | **62** | **57** | **48** | -1 | +0 |
| 138 | `wil-parker` | UNR | SD | 5 | 29 | 29 | 18 | **22** | **23** | **25** | -4 | +7 |
| 139 | `toby-pink` | RD | KPD | 5 | 15 | 23 | 33 | **31** | **31** | **32** | +9 | -1 |
| 140 | `liam-o-connell` | IRE | SD | 11 | 45 | 39 | 39 | **39** | **39** | **39** | +0 | +0 |
| 141 | `daniel-butler` | ND>64 | SF | 8 | 10 | 10 | 15 | **15** | **15** | **15** | +5 | +0 |
| 142 | `jed-bews` | ND>64 | SD | 0 | 10 | 10 | 15 | **15** | **15** | **15** | +5 | +0 |
| 143 | `lincoln-mccarthy` | ND>64 | SF | 8 | 10 | 10 | 15 | **15** | **15** | **15** | +5 | +0 |
| 144 | `matt-guelfi` | ND>64 | SF | 3 | 10 | 10 | 15 | **15** | **15** | **15** | +5 | +0 |
| 145 | `nathan-broad` | ND>64 | SD | 20 | 10 | 10 | 15 | **15** | **15** | **15** | +5 | +0 |
| 146 | `jai-newcombe` **NAMED** | MSD | MID | 21 | 4887 | 4883 | 4883 | **4883** | **4883** | **4883** | +0 | +0 |
| 147 | `jordon-butts` | RD | KPD | 9 | 15 | 15 | 18 | **18** | **18** | **18** | +3 | +0 |
| 148 | `oisin-mullin` | IRE | SD | 21 | 17 | 17 | 14 | **14** | **14** | **14** | -3 | +0 |
| 149 | `sam-switkowski` | ND>64 | SF | 21 | 12 | 12 | 15 | **15** | **15** | **15** | +3 | +0 |
| 150 | `mason-cox` | UNR | KPF | 14 | 5 | 5 | 3 | **3** | **3** | **3** | -2 | +0 |
| 151 | `matt-owies` | UNR | SF | 3 | 5 | 5 | 3 | **3** | **3** | **3** | -2 | +0 |
| 152 | `conor-mckenna` | IRE | SF | 15 | 7 | 7 | 6 | **6** | **6** | **6** | -1 | +0 |

Full machine-readable form, with per-column deltas and percentages for every row:
`MOVERS_TABLE.json`.
