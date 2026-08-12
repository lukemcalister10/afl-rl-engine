# THE COMPOSED POOL-UPDATE v2 MOVERS LEDGER — 2026-08-12

Issue #334, ORDER 25 (the landing build). Branch `land/pool-update-v2`. Owner's word: **"Land"**
(comment [5267147448](https://github.com/lukemcalister10/afl-rl-engine/issues/334#issuecomment-5267147448)),
with the par amendment folded in. Rulings underneath: 5253173347 (D8, H), 5262159933, 5262213139,
5262928754 (the ND>64 cap amendment), 5265698024 and 5266652914 (the delivery and the premium).

**Live board `1dbd1480a34c7823f330273211cbb76a` → landed board `88ce647f531030d8d2e094188b258191`.**

| board | md5 | total | Δ vs LIVE | % | moved | up | down |
|---|---|---:|---:|---:|---:|---:|---:|
| LIVE 1dbd1480 | `1dbd1480a34c7823f330273211cbb76a` | 746,043 | 0 | +0.000% | 0 | 0 | 0 |
| lever 1 — H retirement | `452623adeb9aaed115d883dbe6b0239c` | 748,355 | 2,312 | +0.310% | 48 | 48 | 0 |
| lever 2 — + the ψ retention/delivery machinery | `0cfa973a997e3361708679dbb3a6a78a` | 751,332 | 5,289 | +0.709% | 82 | 80 | 2 |
| lever 3 — + the repricing (LANDED) | `88ce647f531030d8d2e094188b258191` | 752,429 | 6,386 | +0.856% | 117 | 101 | 16 |

**Lever totals across every moved row: H retirement +2303 · ψ retention/delivery +2965 · repricing +1118 = +6386.**

**Lever 1 is ORDER 23's own board, reused byte-identically** (`452623ad`). Nothing in ORDERS 24,
24B or 25 touches H, so re-measuring that lever would be re-measuring the same thing under a new
name. Its column total here (**+2303**) is identical to the H column of ORDER 23's ledger.

## Separation — asserted, not claimed

| check | result |
|---|---|
| non-pool board rows moved, lever 1 — H retirement | **0** |
| non-pool board rows moved, lever 2 — + the ψ retention/delivery machinery | **0** |
| non-pool board rows moved, lever 3 — + the repricing (LANDED) | **0** |
| ND 1-64 board value, LIVE → LANDED | **620,877 → 620,877** |

**The national arm does not move under any lever, at any stage.** Not as a claim — the
consequence builder computes it on the board bytes at every one of the three stages, and the
landing act's own separation instrument asserts it and raises before anything is written.

## By pathway

| pathway | rows | moved | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | **%** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ND 1-64 | 561 | 0 | 620,877 | 620,877 | 620,877 | **620,877** | **+0** | **+0.000%** |
| RD | 66 | 22 | 45,874 | 46,148 | 46,571 | **46,490** | **+616** | **+1.343%** |
| MSD | 63 | 34 | 36,089 | 36,962 | 38,728 | **39,742** | **+3653** | **+10.122%** |
| ND>64 | 28 | 13 | 18,828 | 18,887 | 18,924 | **19,234** | **+406** | **+2.156%** |
| SSP | 28 | 14 | 11,535 | 12,237 | 12,498 | **12,812** | **+1277** | **+11.071%** |
| PDA | 15 | 4 | 8,103 | 8,159 | 8,249 | **8,244** | **+141** | **+1.740%** |
| PDN | 16 | 11 | 2,729 | 2,906 | 3,166 | **2,999** | **+270** | **+9.894%** |
| UNR | 13 | 9 | 1,296 | 1,376 | 1,398 | **1,231** | **-65** | **-5.015%** |
| IRE | 14 | 10 | 712 | 803 | 921 | **800** | **+88** | **+12.360%** |

## THE MOVERS ≥ 50 POINTS — the owner's attribution requirement, every one named (36 rows)

| player | pathway | pos | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | % | lever H | lever ψ delivery | lever repricing |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Nicholas Martin **[NAMED]** | SSP | SF | 2822 | 3509 | 3512 | **3513** | **+691** | +24.5% | +687 | +3 | +1 |
| Caleb May | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| Harrison Coe | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| Max Mapley | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| Luker Kentfield **[NAMED]** | MSD | KPF | 178 | 178 | 379 | **419** | **+241** | +135.4% | +0 | +201 | +40 |
| Mitch Podhajski | MSD | KPF | 186 | 186 | 337 | **399** | **+213** | +114.5% | +0 | +151 | +62 |
| Oliver Francou | MSD | MID | 375 | 375 | 543 | **576** | **+201** | +53.6% | +0 | +168 | +33 |
| Harrison Ramm **[NAMED]** | MSD | KPD | 351 | 351 | 512 | **545** | **+194** | +55.3% | +0 | +161 | +33 |
| Jaxon Artemis | MSD | SD | 340 | 340 | 490 | **520** | **+180** | +52.9% | +0 | +150 | +30 |
| Alex Van Wyk | MSD | RUCK | 233 | 233 | 332 | **391** | **+158** | +67.8% | +0 | +99 | +59 |
| Flynn Riley | MSD | RUCK | 233 | 233 | 332 | **391** | **+158** | +67.8% | +0 | +99 | +59 |
| Lukas Cooke | MSD | KPD | 206 | 206 | 311 | **364** | **+158** | +76.7% | +0 | +105 | +53 |
| Aidan Johnson | ND>64 | KPF | 80 | 80 | 143 | **229** | **+149** | +186.2% | +0 | +63 | +86 |
| Jacob Newton | MSD | SF | 156 | 156 | 275 | **299** | **+143** | +91.7% | +0 | +119 | +24 |
| Max Beattie | MSD | SF | 39 | 172 | 153 | **181** | **+142** | +364.1% | +133 | -19 | +28 |
| Max Ramsden | MSD | KPF | 115 | 115 | 227 | **257** | **+142** | +123.5% | +0 | +112 | +30 |
| Oliver Griffin | MSD | SF | 39 | 172 | 153 | **181** | **+142** | +364.1% | +133 | -19 | +28 |
| Hudson O'Keeffe | SSP | KPF | 136 | 136 | 243 | **275** | **+139** | +102.2% | +0 | +107 | +32 |
| Ben Jepson | SSP | MID | 88 | 88 | 179 | **222** | **+134** | +152.3% | +0 | +91 | +43 |
| Ollie Greeves | RD | MID | 475 | 475 | 586 | **583** | **+108** | +22.7% | +0 | +111 | -3 |
| Iliro Smit | MSD | RUCK | 100 | 170 | 174 | **204** | **+104** | +104.0% | +70 | +4 | +30 |
| Noah Howes | MSD | KPF | 128 | 128 | 195 | **229** | **+101** | +78.9% | +0 | +67 | +34 |
| Caleb Lewis | MSD | KPF | 138 | 138 | 200 | **233** | **+95** | +68.8% | +0 | +62 | +33 |
| Logan Smith | ND>64 | RUCK | 91 | 114 | 115 | **185** | **+94** | +103.3% | +23 | +1 | +70 |
| Balyn O'Brien | SSP | SD | 300 | 300 | 355 | **383** | **+83** | +27.7% | +0 | +55 | +28 |
| Tom Cochrane | RD | SF | 148 | 148 | 239 | **230** | **+82** | +55.4% | +0 | +91 | -9 |
| Josh Draper | PDN | KPD | 315 | 389 | 391 | **389** | **+74** | +23.5% | +74 | +2 | -2 |
| Liam Hetherton | PDA | KPF | 100 | 124 | 170 | **168** | **+68** | +68.0% | +24 | +46 | -2 |
| Luke Beecken | MSD | MID | 100 | 100 | 140 | **164** | **+64** | +64.0% | +0 | +40 | +24 |
| Tom Hanily | MSD | SF | 154 | 154 | 203 | **216** | **+62** | +40.3% | +0 | +49 | +13 |
| Fred Rodriguez | RD | SF | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| Nick Driscoll | RD | SF | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| Riley Onley | RD | MID | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| Xavier Walsh | RD | KPF | 86 | 107 | 116 | **143** | **+57** | +66.3% | +21 | +9 | +27 |
| Robert Hansen **[NAMED]** | MSD | SF | 80 | 80 | 119 | **132** | **+52** | +65.0% | +0 | +39 | +13 |
| Shadeau Brain | PDA | SD | 69 | 69 | 121 | **120** | **+51** | +73.9% | +0 | +52 | -1 |

## EVERY MOVER — all 117 rows, with the same decomposition

| # | player | pathway | pos | LIVE | H only | + ψ delivery | **LANDED** | **Δ** | % | lever H | lever ψ delivery | lever repricing |
|---:|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | Nicholas Martin **[NAMED]** | SSP | SF | 2822 | 3509 | 3512 | **3513** | **+691** | +24.5% | +687 | +3 | +1 |
| 2 | Caleb May | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| 3 | Harrison Coe | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| 4 | Max Mapley | MSD | RUCK | 52 | 231 | 274 | **322** | **+270** | +519.2% | +179 | +43 | +48 |
| 5 | Luker Kentfield **[NAMED]** | MSD | KPF | 178 | 178 | 379 | **419** | **+241** | +135.4% | +0 | +201 | +40 |
| 6 | Mitch Podhajski | MSD | KPF | 186 | 186 | 337 | **399** | **+213** | +114.5% | +0 | +151 | +62 |
| 7 | Oliver Francou | MSD | MID | 375 | 375 | 543 | **576** | **+201** | +53.6% | +0 | +168 | +33 |
| 8 | Harrison Ramm **[NAMED]** | MSD | KPD | 351 | 351 | 512 | **545** | **+194** | +55.3% | +0 | +161 | +33 |
| 9 | Jaxon Artemis | MSD | SD | 340 | 340 | 490 | **520** | **+180** | +52.9% | +0 | +150 | +30 |
| 10 | Alex Van Wyk | MSD | RUCK | 233 | 233 | 332 | **391** | **+158** | +67.8% | +0 | +99 | +59 |
| 11 | Flynn Riley | MSD | RUCK | 233 | 233 | 332 | **391** | **+158** | +67.8% | +0 | +99 | +59 |
| 12 | Lukas Cooke | MSD | KPD | 206 | 206 | 311 | **364** | **+158** | +76.7% | +0 | +105 | +53 |
| 13 | Aidan Johnson | ND>64 | KPF | 80 | 80 | 143 | **229** | **+149** | +186.2% | +0 | +63 | +86 |
| 14 | Jacob Newton | MSD | SF | 156 | 156 | 275 | **299** | **+143** | +91.7% | +0 | +119 | +24 |
| 15 | Max Beattie | MSD | SF | 39 | 172 | 153 | **181** | **+142** | +364.1% | +133 | -19 | +28 |
| 16 | Max Ramsden | MSD | KPF | 115 | 115 | 227 | **257** | **+142** | +123.5% | +0 | +112 | +30 |
| 17 | Oliver Griffin | MSD | SF | 39 | 172 | 153 | **181** | **+142** | +364.1% | +133 | -19 | +28 |
| 18 | Hudson O'Keeffe | SSP | KPF | 136 | 136 | 243 | **275** | **+139** | +102.2% | +0 | +107 | +32 |
| 19 | Ben Jepson | SSP | MID | 88 | 88 | 179 | **222** | **+134** | +152.3% | +0 | +91 | +43 |
| 20 | Ollie Greeves | RD | MID | 475 | 475 | 586 | **583** | **+108** | +22.7% | +0 | +111 | -3 |
| 21 | Iliro Smit | MSD | RUCK | 100 | 170 | 174 | **204** | **+104** | +104.0% | +70 | +4 | +30 |
| 22 | Noah Howes | MSD | KPF | 128 | 128 | 195 | **229** | **+101** | +78.9% | +0 | +67 | +34 |
| 23 | Caleb Lewis | MSD | KPF | 138 | 138 | 200 | **233** | **+95** | +68.8% | +0 | +62 | +33 |
| 24 | Logan Smith | ND>64 | RUCK | 91 | 114 | 115 | **185** | **+94** | +103.3% | +23 | +1 | +70 |
| 25 | Balyn O'Brien | SSP | SD | 300 | 300 | 355 | **383** | **+83** | +27.7% | +0 | +55 | +28 |
| 26 | Tom Cochrane | RD | SF | 148 | 148 | 239 | **230** | **+82** | +55.4% | +0 | +91 | -9 |
| 27 | Josh Draper | PDN | KPD | 315 | 389 | 391 | **389** | **+74** | +23.5% | +74 | +2 | -2 |
| 28 | Liam Hetherton | PDA | KPF | 100 | 124 | 170 | **168** | **+68** | +68.0% | +24 | +46 | -2 |
| 29 | Luke Beecken | MSD | MID | 100 | 100 | 140 | **164** | **+64** | +64.0% | +0 | +40 | +24 |
| 30 | Tom Hanily | MSD | SF | 154 | 154 | 203 | **216** | **+62** | +40.3% | +0 | +49 | +13 |
| 31 | Fred Rodriguez | RD | SF | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| 32 | Nick Driscoll | RD | SF | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| 33 | Riley Onley | RD | MID | 143 | 177 | 204 | **201** | **+58** | +40.6% | +34 | +27 | -3 |
| 34 | Xavier Walsh | RD | KPF | 86 | 107 | 116 | **143** | **+57** | +66.3% | +21 | +9 | +27 |
| 35 | Robert Hansen **[NAMED]** | MSD | SF | 80 | 80 | 119 | **132** | **+52** | +65.0% | +0 | +39 | +13 |
| 36 | Shadeau Brain | PDA | SD | 69 | 69 | 121 | **120** | **+51** | +73.9% | +0 | +52 | -1 |
| 37 | Flynn Young | MSD | SF | 128 | 128 | 143 | **168** | **+40** | +31.2% | +0 | +15 | +25 |
| 38 | Keighton Matofai-Forbes | ND>64 | SF | 65 | 75 | 65 | **104** | **+39** | +60.0% | +10 | -10 | +39 |
| 39 | Lennox Hoffman | ND>64 | SD | 65 | 75 | 65 | **104** | **+39** | +60.0% | +10 | -10 | +39 |
| 40 | Leon Kickett | RD | SF | 112 | 139 | 161 | **151** | **+39** | +34.8% | +27 | +22 | -10 |
| 41 | River Stevens | ND>64 | SF | 65 | 75 | 65 | **104** | **+39** | +60.0% | +10 | -10 | +39 |
| 42 | Liam Reidy | RD | KPF | 291 | 291 | 358 | **329** | **+38** | +13.1% | +0 | +67 | -29 |
| 43 | Patrick Carr | UNR | RUCK | 67 | 83 | 49 | **31** | **-36** | -53.7% | +16 | -34 | -18 |
| 44 | Will McLachlan | MSD | SF | 117 | 117 | 140 | **148** | **+31** | +26.5% | +0 | +23 | +8 |
| 45 | Tyson Stengle | RD | SF | 121 | 150 | 151 | **151** | **+30** | +24.8% | +29 | +1 | +0 |
| 46 | Andy Moniz-Wakefield | PDN | SD | 27 | 27 | 65 | **54** | **+27** | +100.0% | +0 | +38 | -11 |
| 47 | Flynn Perez | SSP | SD | 113 | 113 | 113 | **139** | **+26** | +23.0% | +0 | +0 | +26 |
| 48 | Mitch Zadow | SSP | SF | 113 | 113 | 113 | **139** | **+26** | +23.0% | +0 | +0 | +26 |
| 49 | Paddy Cross | SSP | SF | 113 | 113 | 113 | **139** | **+26** | +23.0% | +0 | +0 | +26 |
| 50 | Will Lewis | SSP | KPF | 113 | 113 | 113 | **139** | **+26** | +23.0% | +0 | +0 | +26 |
| 51 | Ben Murphy | IRE | SD | 60 | 80 | 106 | **85** | **+25** | +41.7% | +20 | +26 | -21 |
| 52 | Cillian Bourke | IRE | SD | 60 | 80 | 106 | **85** | **+25** | +41.7% | +20 | +26 | -21 |
| 53 | Jack Henderson | SSP | SF | 88 | 103 | 92 | **113** | **+25** | +28.4% | +15 | -11 | +21 |
| 54 | Jaime Uhr-Henry | UNR | RUCK | 51 | 64 | 41 | **26** | **-25** | -49.0% | +13 | -23 | -15 |
| 55 | Kobe McDonald | IRE | SD | 60 | 80 | 106 | **85** | **+25** | +41.7% | +20 | +26 | -21 |
| 56 | Tom Blamires | SSP | SD | 114 | 114 | 114 | **139** | **+25** | +21.9% | +0 | +0 | +25 |
| 57 | Ewan Mackinlay | MSD | SF | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 58 | Jai Saxena | PDN | SF | 60 | 74 | 106 | **84** | **+24** | +40.0% | +14 | +32 | -22 |
| 59 | Jesse Mellor | PDN | SF | 60 | 74 | 106 | **84** | **+24** | +40.0% | +14 | +32 | -22 |
| 60 | Lachlan Blakiston | MSD | KPD | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 61 | Mani Liddy **[NAMED]** | MSD | MID | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 62 | Roan Steele | MSD | MID | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 63 | Ryda Luke | PDN | SF | 60 | 74 | 106 | **84** | **+24** | +40.0% | +14 | +32 | -22 |
| 64 | Thomas Burton | SSP | MID | 415 | 415 | 431 | **439** | **+24** | +5.8% | +0 | +16 | +8 |
| 65 | Toby Whan | PDN | MID | 60 | 74 | 106 | **84** | **+24** | +40.0% | +14 | +32 | -22 |
| 66 | Zac Banch | MSD | SF | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 67 | Zac Walker | MSD | KPD | 128 | 128 | 128 | **152** | **+24** | +18.8% | +0 | +0 | +24 |
| 68 | Nathan Wardius | PDA | SF | 54 | 67 | 78 | **77** | **+23** | +42.6% | +13 | +11 | -1 |
| 69 | Tyrell Dewar | PDN | SD | 73 | 88 | 102 | **96** | **+23** | +31.5% | +15 | +14 | -6 |
| 70 | Darragh Joyce | IRE | KPD | 20 | 20 | 51 | **41** | **+21** | +105.0% | +0 | +31 | -10 |
| 71 | Tom Edwards | SSP | KPF | 88 | 88 | 88 | **108** | **+20** | +22.7% | +0 | +0 | +20 |
| 72 | Harry Charleson | RD | SD | 86 | 100 | 105 | **105** | **+19** | +22.1% | +14 | +5 | +0 |
| 73 | Jayden Nguyen | PDN | SD | 452 | 452 | 478 | **471** | **+19** | +4.2% | +0 | +26 | -7 |
| 74 | Jack Hutchinson | MSD | MID | 100 | 100 | 100 | **118** | **+18** | +18.0% | +0 | +0 | +18 |
| 75 | Jordan Boyd | MSD | SD | 37 | 37 | 48 | **55** | **+18** | +48.6% | +0 | +11 | +7 |
| 76 | Saad El-Hawli | MSD | SD | 100 | 100 | 100 | **118** | **+18** | +18.0% | +0 | +0 | +18 |
| 77 | Caleb Graham | ND>64 | KPD | 37 | 43 | 45 | **54** | **+17** | +45.9% | +6 | +2 | +9 |
| 78 | Kalani White | PDN | KPF | 67 | 85 | 107 | **84** | **+17** | +25.4% | +18 | +22 | -23 |
| 79 | Lachie Sullivan | SSP | SF | 70 | 70 | 70 | **86** | **+16** | +22.9% | +0 | +0 | +16 |
| 80 | Mykelti Lefau | SSP | KPF | 70 | 70 | 70 | **86** | **+16** | +22.9% | +0 | +0 | +16 |
| 81 | Jack Buller | MSD | KPF | 80 | 80 | 80 | **94** | **+14** | +17.5% | +0 | +0 | +14 |
| 82 | Vigo Visentini **[NAMED]** | RD | RUCK | 168 | 168 | 200 | **182** | **+14** | +8.3% | +0 | +32 | -18 |
| 83 | Asher Eastham | RD | SF | 81 | 94 | 99 | **94** | **+13** | +16.0% | +13 | +5 | -5 |
| 84 | Aiden Riddle | RD | RUCK | 140 | 174 | 165 | **151** | **+11** | +7.9% | +34 | -9 | -14 |
| 85 | Joe Pike | RD | RUCK | 140 | 174 | 165 | **151** | **+11** | +7.9% | +34 | -9 | -14 |
| 86 | James Blanck | MSD | KPD | 60 | 60 | 60 | **70** | **+10** | +16.7% | +0 | +0 | +10 |
| 87 | Rob Monahan | IRE | SD | 37 | 47 | 56 | **45** | **+8** | +21.6% | +10 | +9 | -11 |
| 88 | Toby Pink | RD | KPD | 23 | 23 | 29 | **31** | **+8** | +34.8% | +0 | +6 | +2 |
| 89 | Benny Barrett | PDN | SF | 43 | 50 | 65 | **50** | **+7** | +16.3% | +7 | +15 | -15 |
| 90 | Harry Edwards | RD | KPD | 97 | 97 | 101 | **104** | **+7** | +7.2% | +0 | +4 | +3 |
| 91 | Matt Hill | UNR | SD | 49 | 49 | 80 | **56** | **+7** | +14.3% | +0 | +31 | -24 |
| 92 | Ricky Mentha | PDN | SF | 43 | 50 | 65 | **50** | **+7** | +16.3% | +7 | +15 | -15 |
| 93 | Zak Evans | UNR | MID | 36 | 42 | 47 | **29** | **-7** | -19.4% | +6 | +5 | -18 |
| 94 | Oscar Berry | UNR | KPD | 47 | 70 | 85 | **53** | **+6** | +12.8% | +23 | +15 | -32 |
| 95 | Daniel Butler | ND>64 | SF | 10 | 10 | 10 | **15** | **+5** | +50.0% | +0 | +0 | +5 |
| 96 | Jed Bews | ND>64 | SD | 10 | 10 | 10 | **15** | **+5** | +50.0% | +0 | +0 | +5 |
| 97 | Lincoln McCarthy | ND>64 | SF | 10 | 10 | 10 | **15** | **+5** | +50.0% | +0 | +0 | +5 |
| 98 | Matt Guelfi | ND>64 | SF | 10 | 10 | 10 | **15** | **+5** | +50.0% | +0 | +0 | +5 |
| 99 | Nathan Broad | ND>64 | SD | 10 | 10 | 10 | **15** | **+5** | +50.0% | +0 | +0 | +5 |
| 100 | Wil Parker | UNR | SD | 29 | 29 | 31 | **24** | **-5** | -17.2% | +0 | +2 | -7 |
| 101 | Cillian Burke | IRE | SD | 47 | 54 | 54 | **43** | **-4** | -8.5% | +7 | +0 | -11 |
| 102 | Eamonn Armstrong | IRE | SD | 47 | 54 | 54 | **43** | **-4** | -8.5% | +7 | +0 | -11 |
| 103 | Matt Duffy | IRE | KPD | 47 | 54 | 54 | **43** | **-4** | -8.5% | +7 | +0 | -11 |
| 104 | Peter Ladhams | RD | KPF | 489 | 489 | 494 | **493** | **+4** | +0.8% | +0 | +5 | -1 |
| 105 | Jordon Butts | RD | KPD | 15 | 15 | 15 | **18** | **+3** | +20.0% | +0 | +0 | +3 |
| 106 | Oisin Mullin | IRE | SD | 17 | 17 | 17 | **14** | **-3** | -17.6% | +0 | +0 | -3 |
| 107 | Sam Switkowski | ND>64 | SF | 12 | 12 | 12 | **15** | **+3** | +25.0% | +0 | +0 | +3 |
| 108 | Jack Watkins | RD | SF | 132 | 132 | 132 | **130** | **-2** | -1.5% | +0 | +0 | -2 |
| 109 | Mason Cox | UNR | KPF | 5 | 5 | 5 | **3** | **-2** | -40.0% | +0 | +0 | -2 |
| 110 | Matt Owies | UNR | SF | 5 | 5 | 5 | **3** | **-2** | -40.0% | +0 | +0 | -2 |
| 111 | Mitchell Hinge | RD | SD | 320 | 320 | 322 | **322** | **+2** | +0.6% | +0 | +2 | +0 |
| 112 | Bailey Banfield | RD | SD | 11 | 11 | 11 | **10** | **-1** | -9.1% | +0 | +0 | -1 |
| 113 | Brandon Zerk-Thatcher | ND>64 | KPD | 47 | 47 | 48 | **48** | **+1** | +2.1% | +0 | +1 | +0 |
| 114 | Conor McKenna | IRE | SF | 7 | 7 | 7 | **6** | **-1** | -14.3% | +0 | +0 | -1 |
| 115 | Indy Cotton | UNR | SF | 49 | 62 | 76 | **48** | **-1** | -2.0% | +13 | +14 | -28 |
| 116 | Lachlan McNeil | RD | SF | 21 | 21 | 21 | **20** | **-1** | -4.8% | +0 | +0 | -1 |
| 117 | Noah Chamberlain | PDA | KPF | 87 | 106 | 87 | **86** | **-1** | -1.1% | +19 | -19 | -1 |

**Movers by pathway:** IRE 10 · MSD 34 · ND>64 13 · PDA 4 · PDN 11 · RD 22 · SSP 14 · UNR 9.

**The lever-sum identity holds on all 117 rows** (H + ψ delivery + repricing == total delta, asserted at write time; the writer halts otherwise).

**Why the lever column totals (+2303 / +2965 / +1118) do not equal the board-wide lever deltas (+2312 / +2977 / +1097).** The columns are summed over the rows that move on the LANDED board. ONE row moves under the intermediate levers and lands back on EXACTLY its live value, so it carries no total delta and is not a ledger row: **jacob-moss** (36 → 45 → 57 → **36**; H +9, ψ delivery +12, repricing −21). It accounts for the whole of each of the three gaps. Named here rather than reconciled away.

## The seven named rows, with their lever split

| player | pathway | LIVE | H only | + ψ delivery | **LANDED** | lever H | lever ψ delivery | lever repricing |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `harrison-ramm` | MSD | 351 | 351 | 512 | **545** | +0 | +161 | +33 |
| `luker-kentfield` | MSD | 178 | 178 | 379 | **419** | +0 | +201 | +40 |
| `mani-liddy` | MSD | 128 | 128 | 128 | **152** | +0 | +0 | +24 |
| `robert-hansen` | MSD | 80 | 80 | 119 | **132** | +0 | +39 | +13 |
| `vigo-visentini` | RD | 168 | 168 | 200 | **182** | +0 | +32 | -18 |
| `marcus-herbert` | — | — | — | — | **unmoved** | 0 | 0 | 0 |
| `jai-newcombe` | — | — | — | — | **unmoved** | 0 | 0 | 0 |
| `nicholas-martin` | SSP | 2822 | 3509 | 3512 | **3513** | +687 | +3 | +1 |

`marcus-herbert` and `jai-newcombe` do not appear because they **do not move at all**: both are
full current participants (φ = 1) carrying an anchor share of exactly zero, so no multiplier and
no level reaches them. That is the design working, and it is the cheapest available check that
the delivery fix reaches only the population it is meant to reach.

One act, three levers, one ledger.

_Generated by [Claude Code](https://claude.ai/code)_
