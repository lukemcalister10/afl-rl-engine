# OWNER EYEBALL LIST — pick-convention remediation candidate — 2026-07-11

OLD = baked v2.7 board (SCALE 4.45). NEW = pick-convention remediation regenerated board (SCALE 4.68336). Remediation REVERTED the 190 rookie renumbers to database-universe store ordinals + re-derived the chain table (2010 77->93); KEPT the (a) band-pool fix, (c) _draft fills + 8 PSD splits, (f) re-denomination. Every player AND every pick asset below.

## ONE-PAGE SUMMARY

- **MEASURED CURRENCY FACTOR = 1.0524** — the global board SCALE ratio (new 4.68336 / baked 4.45000). This is the definitive uniform scalar; owner ruling (f): shipped pick assets = frozen v3.4 x this factor. Matches audit Q4 (1.0524).
- Players: 805. Pick assets: 30.
- Player Δ% distribution: min -16.67% / **median 5.03%** / max 50.00%. The MEDIAN (~currency factor) is the representative per-player shift; the MEAN is right-skewed by low-value floor players whose few-SCAR rises are large in %.
- Non-RUC players **median Δ% +5.07%** (mean +4.72%, skewed). RUC cohort **median Δ% +4.12%** (mean +3.53%). Established RUCs move LESS than the currency (e.g. Max Gawn baked 2413 -> 2483 = +2.90%, i.e. ~-2.3% relative to the +5.24% currency — the RUC cap machinery; FLAGGED per directive).
- Pick assets Δ%: uniform **+5.24%** (= factor-1; pick-vs-pick ratios byte-preserved, uniform scalar).

### Three narrowest guard margins (candidate)

- **G-COHORT y4 (BINDING, class-year-sum vs hard 1.30)**: 1.29 vs 1.30 -> 1.0 pt (B1 remediated avg-peak row y4=129; UNCHANGED by the remediation — rookie reverts + 2010 chain cap out)
- **A10 Curnow decline (frozen suite, bar 0.50)**: 0.55 vs 0.50 -> +0.05 (narrowest PASSING anchor; PROVISIONAL, data-caused)
- **A8 Berry >= 2x Tsatas (frozen suite)**: 2.14x vs 2.00x -> +0.14x
- Gate suite: all green except the owner-ruled expected reds **{A2, A3, A12}** (data-caused, unchanged by this build); B4 board-parity PASS; B3 book-seal PASS (candidate re-seal); B5 raise-only intact (0 lowered).

### Per-position mean Δ% (players)

| position | n | mean Δ% | median Δ% |
|---|---|---|---|
| GEN_DEF | 176 | +4.72% | +4.92% |
| GEN_FWD | 184 | +4.20% | +5.07% |
| KEY_DEF | 92 | +5.14% | +5.22% |
| KEY_FWD | 103 | +4.82% | +5.07% |
| MID | 195 | +4.97% | +5.06% |
| RUC | 55 | +3.53% | +4.12% |

### FLOOR-DIPPERS (G-FLOOR dispensation — players whose value LOWERED)

Count = **30** (owner ruling: ≤5 SCAR dips on the floor anchors ruled not-cratering, dispensation granted). 
Largest absolute dip = **13 SCAR**. !!! A DIP EXCEEDS 5 SCAR — STOP/REVIEW !!!

| player | key | pos | old | new | Δabs | Δ% |
|---|---|---|---|---|---|---|
| Robert Hansen | robert-hansen | GEN_FWD | 174 | 161 | -13 | -7.47% |
| Jacob Newton | jacob-newton | GEN_FWD | 157 | 145 | -12 | -7.64% |
| Flynn Riley | flynn-riley | RUC | 389 | 381 | -8 | -2.06% |
| Caleb May | caleb-may | RUC | 389 | 381 | -8 | -2.06% |
| Alex Van Wyk | alex-van-wyk | RUC | 389 | 381 | -8 | -2.06% |
| Max Mapley | max-mapley | RUC | 389 | 381 | -8 | -2.06% |
| Patrick Carr | patrick-carr | RUC | 389 | 381 | -8 | -2.06% |
| Tom Hanily | tom-hanily | GEN_FWD | 145 | 137 | -8 | -5.52% |
| Jaime Uhr-Henry | jaime-uhr-henry | RUC | 301 | 294 | -7 | -2.33% |
| Joe Pike | joe-pike | RUC | 301 | 294 | -7 | -2.33% |
| Aiden Riddle | aiden-riddle | RUC | 301 | 294 | -7 | -2.33% |
| Ewan Mackinlay | ewan-mackinlay | GEN_FWD | 42 | 35 | -7 | -16.67% |
| Will McLachlan | will-mclachlan | GEN_FWD | 140 | 133 | -7 | -5.00% |
| Max Beattie | max-beattie | GEN_FWD | 38 | 32 | -6 | -15.79% |
| Vigo Visentini | vigo-visentini | RUC | 256 | 250 | -6 | -2.34% |
| Iliro Smit | iliro-smit | RUC | 256 | 250 | -6 | -2.34% |
| Oliver Griffin | oliver-griffin | GEN_FWD | 238 | 234 | -4 | -1.68% |
| Zac Banch | zac-banch | GEN_FWD | 49 | 45 | -4 | -8.16% |
| Campbell Lake | campbell-lake | GEN_FWD | 114 | 111 | -3 | -2.63% |
| Logan Smith | logan-smith | RUC | 372 | 369 | -3 | -0.81% |
| Mani Liddy | mani-liddy | MID | 38 | 35 | -3 | -7.89% |
| Max Heath | max-heath | RUC | 141 | 138 | -3 | -2.13% |
| Alex Dodson | alex-dodson | RUC | 388 | 386 | -2 | -0.52% |
| Michael Sellwood | michael-sellwood | GEN_DEF | 80 | 78 | -2 | -2.50% |
| Toby Murray | toby-murray | KEY_FWD | 202 | 200 | -2 | -0.99% |
| Jacob Molier | jacob-molier | RUC | 393 | 392 | -1 | -0.25% |
| Flynn Young | flynn-young | GEN_FWD | 9 | 8 | -1 | -11.11% |
| Jack Hutchinson | jack-hutchinson | MID | 54 | 53 | -1 | -1.85% |
| Jack Buller | jack-buller | KEY_FWD | 37 | 36 | -1 | -2.70% |
| Max Ramsden | max-ramsden | KEY_FWD | 182 | 181 | -1 | -0.55% |

### RUC cohort (flagged — moves less than the currency shift)

| player | key | old | new | Δabs | Δ% |
|---|---|---|---|---|---|
| Vigo Visentini | vigo-visentini | 256 | 250 | -6 | -2.34% |
| Iliro Smit | iliro-smit | 256 | 250 | -6 | -2.34% |
| Jaime Uhr-Henry | jaime-uhr-henry | 301 | 294 | -7 | -2.33% |
| Joe Pike | joe-pike | 301 | 294 | -7 | -2.33% |
| Aiden Riddle | aiden-riddle | 301 | 294 | -7 | -2.33% |
| Max Heath | max-heath | 141 | 138 | -3 | -2.13% |
| Flynn Riley | flynn-riley | 389 | 381 | -8 | -2.06% |
| Caleb May | caleb-may | 389 | 381 | -8 | -2.06% |
| Alex Van Wyk | alex-van-wyk | 389 | 381 | -8 | -2.06% |
| Max Mapley | max-mapley | 389 | 381 | -8 | -2.06% |
| Patrick Carr | patrick-carr | 389 | 381 | -8 | -2.06% |
| Logan Smith | logan-smith | 372 | 369 | -3 | -0.81% |
| Alex Dodson | alex-dodson | 388 | 386 | -2 | -0.52% |
| Jacob Molier | jacob-molier | 393 | 392 | -1 | -0.25% |
| Max Knobel | max-knobel | 402 | 402 | +0 | +0.00% |
| Rhys Stanley | rhys-stanley | 30 | 30 | +0 | +0.00% |
| Oscar Steene | oscar-steene | 251 | 252 | +1 | +0.40% |
| Toby Conway | toby-conway | 473 | 479 | +6 | +1.27% |
| Harry Barnett | harry-barnett | 536 | 544 | +8 | +1.49% |
| Will Green | will-green | 575 | 588 | +13 | +2.26% |
| Lachlan Smith | lachlan-smith | 671 | 693 | +22 | +3.28% |
| Taylor Goad | taylor-goad | 788 | 818 | +30 | +3.81% |
| Nick Madden | nick-madden | 1464 | 1521 | +57 | +3.89% |
| Lloyd Meek | lloyd-meek | 896 | 931 | +35 | +3.91% |
| Ned Reeves | ned-reeves | 374 | 389 | +15 | +4.01% |
| Lachlan McAndrew | lachlan-mcandrew | 998 | 1039 | +41 | +4.11% |
| Jordon Sweet | jordon-sweet | 2064 | 2149 | +85 | +4.12% |
| Sam Draper | sam-draper | 631 | 657 | +26 | +4.12% |
| Tristan Xerri | tristan-xerri | 6384 | 6649 | +265 | +4.15% |
| Jarrod Witts | jarrod-witts | 384 | 400 | +16 | +4.17% |
| Reilly O'Brien | reilly-o-brien | 783 | 816 | +33 | +4.21% |
| Rowan Marshall | rowan-marshall | 612 | 638 | +26 | +4.25% |
| Oliver Hayes-Brown | oliver-hayes-brown | 335 | 350 | +15 | +4.48% |
| Peter Ladhams | peter-ladhams | 456 | 477 | +21 | +4.61% |
| Samson Ryan | samson-ryan | 608 | 636 | +28 | +4.61% |
| Darcy Fort | darcy-fort | 83 | 87 | +4 | +4.82% |
| Nick Bryan | nick-bryan | 802 | 841 | +39 | +4.86% |
| Tom De Koning | tom-de-koning | 1638 | 1719 | +81 | +4.95% |
| Darcy Cameron | darcy-cameron | 1446 | 1518 | +72 | +4.98% |
| Brodie Grundy | brodie-grundy | 3770 | 3959 | +189 | +5.01% |
| Marc Pittonet | marc-pittonet | 512 | 538 | +26 | +5.08% |
| Timothy English | timothy-english | 3187 | 3349 | +162 | +5.08% |
| Matthew Flynn | matthew-flynn | 703 | 739 | +36 | +5.12% |
| Max Gawn | max-gawn | 2413 | 2538 | +125 | +5.18% |
| Luke Jackson | luke-jackson | 7411 | 7799 | +388 | +5.24% |
| Toby Nankervis | toby-nankervis | 2001 | 2106 | +105 | +5.25% |
| Bailey J. Williams | bailey-williams-wc | 1672 | 1760 | +88 | +5.26% |
| Sean Darcy | sean-darcy | 945 | 995 | +50 | +5.29% |
| Kieren Briggs | kieren-briggs | 2109 | 2221 | +112 | +5.31% |
| Dante Visentini | dante-visentini | 723 | 762 | +39 | +5.39% |
| Mitchell Edwards | mitchell-edwards | 1539 | 1634 | +95 | +6.17% |
| Ned Moyle | ned-moyle | 1598 | 1697 | +99 | +6.20% |
| Liam Reidy | liam-reidy | 279 | 298 | +19 | +6.81% |
| Harrison Coe | harrison-coe | 95 | 102 | +7 | +7.37% |
| Louis Emmett | louis-emmett | 788 | 1177 | +389 | +49.37% |

## FULL LIST — every player AND every pick asset, sorted by Δ%

| # | kind | name | key | pos/asset | old | new | Δabs | Δ% | flag |
|---|---|---|---|---|---|---|---|---|---|
| 1 | player | Ewan Mackinlay | ewan-mackinlay | GEN_FWD | 42 | 35 | -7 | -16.67% | FLOOR-DIP |
| 2 | player | Max Beattie | max-beattie | GEN_FWD | 38 | 32 | -6 | -15.79% | FLOOR-DIP |
| 3 | player | Flynn Young | flynn-young | GEN_FWD | 9 | 8 | -1 | -11.11% | FLOOR-DIP |
| 4 | player | Zac Banch | zac-banch | GEN_FWD | 49 | 45 | -4 | -8.16% | FLOOR-DIP |
| 5 | player | Mani Liddy | mani-liddy | MID | 38 | 35 | -3 | -7.89% | FLOOR-DIP |
| 6 | player | Jacob Newton | jacob-newton | GEN_FWD | 157 | 145 | -12 | -7.64% | FLOOR-DIP |
| 7 | player | Robert Hansen | robert-hansen | GEN_FWD | 174 | 161 | -13 | -7.47% | FLOOR-DIP |
| 8 | player | Tom Hanily | tom-hanily | GEN_FWD | 145 | 137 | -8 | -5.52% | FLOOR-DIP |
| 9 | player | Will McLachlan | will-mclachlan | GEN_FWD | 140 | 133 | -7 | -5.00% | FLOOR-DIP |
| 10 | player | Jack Buller | jack-buller | KEY_FWD | 37 | 36 | -1 | -2.70% | FLOOR-DIP |
| 11 | player | Campbell Lake | campbell-lake | GEN_FWD | 114 | 111 | -3 | -2.63% | FLOOR-DIP |
| 12 | player | Michael Sellwood | michael-sellwood | GEN_DEF | 80 | 78 | -2 | -2.50% | FLOOR-DIP |
| 13 | player | Vigo Visentini | vigo-visentini | RUC | 256 | 250 | -6 | -2.34% | RUC FLOOR-DIP |
| 14 | player | Iliro Smit | iliro-smit | RUC | 256 | 250 | -6 | -2.34% | RUC FLOOR-DIP |
| 15 | player | Jaime Uhr-Henry | jaime-uhr-henry | RUC | 301 | 294 | -7 | -2.33% | RUC FLOOR-DIP |
| 16 | player | Joe Pike | joe-pike | RUC | 301 | 294 | -7 | -2.33% | RUC FLOOR-DIP |
| 17 | player | Aiden Riddle | aiden-riddle | RUC | 301 | 294 | -7 | -2.33% | RUC FLOOR-DIP |
| 18 | player | Max Heath | max-heath | RUC | 141 | 138 | -3 | -2.13% | RUC FLOOR-DIP |
| 19 | player | Flynn Riley | flynn-riley | RUC | 389 | 381 | -8 | -2.06% | RUC FLOOR-DIP |
| 20 | player | Caleb May | caleb-may | RUC | 389 | 381 | -8 | -2.06% | RUC FLOOR-DIP |
| 21 | player | Alex Van Wyk | alex-van-wyk | RUC | 389 | 381 | -8 | -2.06% | RUC FLOOR-DIP |
| 22 | player | Max Mapley | max-mapley | RUC | 389 | 381 | -8 | -2.06% | RUC FLOOR-DIP |
| 23 | player | Patrick Carr | patrick-carr | RUC | 389 | 381 | -8 | -2.06% | RUC FLOOR-DIP |
| 24 | player | Jack Hutchinson | jack-hutchinson | MID | 54 | 53 | -1 | -1.85% | FLOOR-DIP |
| 25 | player | Oliver Griffin | oliver-griffin | GEN_FWD | 238 | 234 | -4 | -1.68% | FLOOR-DIP |
| 26 | player | Toby Murray | toby-murray | KEY_FWD | 202 | 200 | -2 | -0.99% | FLOOR-DIP |
| 27 | player | Logan Smith | logan-smith | RUC | 372 | 369 | -3 | -0.81% | RUC FLOOR-DIP |
| 28 | player | Max Ramsden | max-ramsden | KEY_FWD | 182 | 181 | -1 | -0.55% | FLOOR-DIP |
| 29 | player | Alex Dodson | alex-dodson | RUC | 388 | 386 | -2 | -0.52% | RUC FLOOR-DIP |
| 30 | player | Jacob Molier | jacob-molier | RUC | 393 | 392 | -1 | -0.25% | RUC FLOOR-DIP |
| 31 | player | Archie May | archie-may | KEY_FWD | 399 | 399 | +0 | +0.00% |  |
| 32 | player | Xavier Bamert | xavier-bamert | GEN_FWD | 279 | 279 | +0 | +0.00% |  |
| 33 | player | Marcus Herbert | marcus-herbert | GEN_DEF | 26 | 26 | +0 | +0.00% |  |
| 34 | player | Joel Fitzgerald | joel-fitzgerald | MID | 66 | 66 | +0 | +0.00% |  |
| 35 | player | Mitch Podhajski | mitch-podhajski | KEY_FWD | 5 | 5 | +0 | +0.00% |  |
| 36 | player | Max Knobel | max-knobel | RUC | 402 | 402 | +0 | +0.00% | RUC |
| 37 | player | Leon Kickett | leon-kickett | GEN_FWD | 4 | 4 | +0 | +0.00% |  |
| 38 | player | Riley Onley | riley-onley | MID | 2 | 2 | +0 | +0.00% |  |
| 39 | player | Ben Jepson | ben-jepson | MID | 17 | 17 | +0 | +0.00% |  |
| 40 | player | Luke Beecken | luke-beecken | MID | 17 | 17 | +0 | +0.00% |  |
| 41 | player | Zak Evans | zak-evans | MID | 8 | 8 | +0 | +0.00% |  |
| 42 | player | Matt Hill | matt-hill | GEN_FWD | 147 | 147 | +0 | +0.00% |  |
| 43 | player | Roan Steele | roan-steele | MID | 15 | 15 | +0 | +0.00% |  |
| 44 | player | Jack Watkins | jack-watkins | MID | 1 | 1 | +0 | +0.00% |  |
| 45 | player | Saad El-Hawli | saad-el-hawli | GEN_DEF | 19 | 19 | +0 | +0.00% |  |
| 46 | player | Jack Henderson | jack-henderson | GEN_FWD | 4 | 4 | +0 | +0.00% |  |
| 47 | player | Lachie Sullivan | lachie-sullivan | GEN_FWD | 1 | 1 | +0 | +0.00% |  |
| 48 | player | Oscar Adams | oscar-adams | GEN_DEF | 106 | 106 | +0 | +0.00% |  |
| 49 | player | Oisin Mullin | oisin-mullin | GEN_DEF | 12 | 12 | +0 | +0.00% |  |
| 50 | player | James Blanck | james-blanck | KEY_DEF | 8 | 8 | +0 | +0.00% |  |
| 51 | player | Tyler Brockman | tyler-brockman | GEN_FWD | 53 | 53 | +0 | +0.00% |  |
| 52 | player | Jordan Boyd | jordan-boyd | GEN_DEF | 10 | 10 | +0 | +0.00% |  |
| 53 | player | Lachlan McNeil | lachlan-mcneil | GEN_FWD | 20 | 20 | +0 | +0.00% |  |
| 54 | player | Riley Garcia | riley-garcia | GEN_FWD | 155 | 155 | +0 | +0.00% |  |
| 55 | player | Brody Mihocek | brody-mihocek | KEY_FWD | 12 | 12 | +0 | +0.00% |  |
| 56 | player | Lincoln McCarthy | lincoln-mccarthy | GEN_FWD | 27 | 27 | +0 | +0.00% |  |
| 57 | player | Mark O'Connor | mark-o-connor | GEN_DEF | 15 | 15 | +0 | +0.00% |  |
| 58 | player | Dane Rampe | dane-rampe | GEN_DEF | 12 | 12 | +0 | +0.00% |  |
| 59 | player | Callum M. Brown | callum-brown-ire | GEN_FWD | 17 | 17 | +0 | +0.00% |  |
| 60 | player | Rhys Stanley | rhys-stanley | RUC | 30 | 30 | +0 | +0.00% | RUC |
| 61 | player | Nathan Broad | nathan-broad | GEN_DEF | 11 | 11 | +0 | +0.00% |  |
| 62 | player | Mark Blicavs | mark-blicavs | MID | 9 | 9 | +0 | +0.00% |  |
| 63 | player | Jordon Butts | jordon-butts | KEY_DEF | 14 | 14 | +0 | +0.00% |  |
| 64 | player | Matt Owies | matt-owies | GEN_FWD | 2 | 2 | +0 | +0.00% |  |
| 65 | player | Mason Cox | mason-cox | KEY_FWD | 1 | 1 | +0 | +0.00% |  |
| 66 | player | Harry Cunningham | harry-cunningham | GEN_DEF | 3 | 3 | +0 | +0.00% |  |
| 67 | player | Jed Bews | jed-bews | GEN_DEF | 24 | 24 | +0 | +0.00% |  |
| 68 | player | Oscar Steene | oscar-steene | RUC | 251 | 252 | +1 | +0.40% | RUC |
| 69 | player | Toby McMullin | toby-mcmullin | GEN_FWD | 196 | 197 | +1 | +0.51% |  |
| 70 | player | Oliver Hannaford | oliver-hannaford | GEN_FWD | 423 | 426 | +3 | +0.71% |  |
| 71 | player | Liam O'Connell | liam-o-connell | GEN_DEF | 91 | 92 | +1 | +1.10% |  |
| 72 | player | Malcolm Rosas | malcolm-rosas | GEN_FWD | 86 | 87 | +1 | +1.16% |  |
| 73 | player | Toby Conway | toby-conway | RUC | 473 | 479 | +6 | +1.27% | RUC |
| 74 | player | Harry Barnett | harry-barnett | RUC | 536 | 544 | +8 | +1.49% | RUC |
| 75 | player | Mitchell Knevitt | mitchell-knevitt | MID | 198 | 201 | +3 | +1.52% |  |
| 76 | player | Tyrell Dewar | tyrell-dewar | GEN_DEF | 309 | 314 | +5 | +1.62% |  |
| 77 | player | Jayden Nguyen | jayden-nguyen | GEN_DEF | 421 | 428 | +7 | +1.66% |  |
| 78 | player | Mykelti Lefau | mykelti-lefau | KEY_FWD | 59 | 60 | +1 | +1.69% |  |
| 79 | player | Zac Walker | zac-walker | GEN_DEF | 174 | 177 | +3 | +1.72% |  |
| 80 | player | Rhyan Mansell | rhyan-mansell | GEN_FWD | 58 | 59 | +1 | +1.72% |  |
| 81 | player | Noah Howes | noah-howes | KEY_FWD | 217 | 221 | +4 | +1.84% |  |
| 82 | player | Mitch Zadow | mitch-zadow | GEN_FWD | 158 | 161 | +3 | +1.90% |  |
| 83 | player | Luker Kentfield | luker-kentfield | KEY_FWD | 315 | 321 | +6 | +1.90% |  |
| 84 | player | Connor Budarick | connor-budarick | GEN_DEF | 155 | 158 | +3 | +1.94% |  |
| 85 | player | Malakai Champion | malakai-champion | GEN_FWD | 333 | 340 | +7 | +2.10% |  |
| 86 | player | Hugh Bond | hugh-bond | GEN_DEF | 225 | 230 | +5 | +2.22% |  |
| 87 | player | Will Green | will-green | RUC | 575 | 588 | +13 | +2.26% | RUC |
| 88 | player | Archer Day-Wicks | archer-day-wicks | GEN_FWD | 422 | 432 | +10 | +2.37% |  |
| 89 | player | Jake Lloyd | jake-lloyd | GEN_DEF | 42 | 43 | +1 | +2.38% |  |
| 90 | player | Jaxon Artemis | jaxon-artemis | GEN_DEF | 372 | 381 | +9 | +2.42% |  |
| 91 | player | Jai Culley | jai-culley | MID | 81 | 83 | +2 | +2.47% |  |
| 92 | player | Lance Collard | lance-collard | GEN_FWD | 281 | 288 | +7 | +2.49% |  |
| 93 | player | Will Hayes | will-hayes-b | GEN_FWD | 320 | 328 | +8 | +2.50% |  |
| 94 | player | Jackson Archer | jackson-archer | GEN_DEF | 80 | 82 | +2 | +2.50% |  |
| 95 | player | Josaia Delana | josaia-delana | GEN_FWD | 237 | 243 | +6 | +2.53% |  |
| 96 | player | Luke Kennedy | luke-kennedy | MID | 387 | 397 | +10 | +2.58% |  |
| 97 | player | Lachlan Gulbin | lachlan-gulbin | GEN_FWD | 332 | 341 | +9 | +2.71% |  |
| 98 | player | Corey Warner | corey-warner | GEN_FWD | 147 | 151 | +4 | +2.72% |  |
| 99 | player | Oliver Francou | oliver-francou | MID | 398 | 409 | +11 | +2.76% |  |
| 100 | player | James Trezise | james-trezise | GEN_DEF | 179 | 184 | +5 | +2.79% |  |
| 101 | player | Chris Scerri | chris-scerri | GEN_FWD | 356 | 366 | +10 | +2.81% |  |
| 102 | player | Oscar Berry | oscar-berry | KEY_DEF | 105 | 108 | +3 | +2.86% |  |
| 103 | player | Judd McVee | judd-mcvee | GEN_DEF | 276 | 284 | +8 | +2.90% |  |
| 104 | player | Wil Parker | wil-parker | GEN_DEF | 34 | 35 | +1 | +2.94% |  |
| 105 | player | Ashton Moir | ashton-moir | GEN_FWD | 265 | 273 | +8 | +3.02% |  |
| 106 | player | Noah Long | noah-long | GEN_FWD | 264 | 272 | +8 | +3.03% |  |
| 107 | player | Caiden Cleary | caiden-cleary | GEN_FWD | 756 | 779 | +23 | +3.04% |  |
| 108 | player | Ollie Greeves | ollie-greeves | MID | 422 | 435 | +13 | +3.08% |  |
| 109 | player | Tyson Stengle | tyson-stengle | GEN_FWD | 258 | 266 | +8 | +3.10% |  |
| 110 | player | Ollie Lord | ollie-lord | KEY_FWD | 160 | 165 | +5 | +3.12% |  |
| 111 | player | Bailey Scott | bailey-scott | MID | 32 | 33 | +1 | +3.12% |  |
| 112 | player | Ryan Gardner | ryan-gardner | KEY_DEF | 32 | 33 | +1 | +3.12% |  |
| 113 | player | Jamarra Ugle-Hagan | jamarra-ugle-hagan | KEY_FWD | 190 | 196 | +6 | +3.16% |  |
| 114 | player | Luke Ryan | luke-ryan | GEN_DEF | 1646 | 1698 | +52 | +3.16% |  |
| 115 | player | Dylan Moore | dylan-moore | GEN_FWD | 1454 | 1500 | +46 | +3.16% |  |
| 116 | player | Ryan Byrnes | ryan-byrnes | GEN_DEF | 94 | 97 | +3 | +3.19% |  |
| 117 | player | Bruce Reville | bruce-reville | MID | 62 | 64 | +2 | +3.23% |  |
| 118 | player | Karl Worner | karl-worner | GEN_DEF | 587 | 606 | +19 | +3.24% |  |
| 119 | player | Josh Gibcus | josh-gibcus | KEY_DEF | 277 | 286 | +9 | +3.25% |  |
| 120 | player | Lachlan Smith | lachlan-smith | RUC | 671 | 693 | +22 | +3.28% | RUC |
| 121 | player | Zachary Williams | zachary-williams | GEN_DEF | 152 | 157 | +5 | +3.29% |  |
| 122 | player | Jesse Motlop | jesse-motlop | GEN_FWD | 151 | 156 | +5 | +3.31% |  |
| 123 | player | Sam Cumming | sam-cumming | MID | 2115 | 2186 | +71 | +3.36% |  |
| 124 | player | Hugo Hall-Kahan | hugo-hall-kahan | GEN_DEF | 89 | 92 | +3 | +3.37% |  |
| 125 | player | Sam Clohesy | sam-clohesy | MID | 237 | 245 | +8 | +3.38% |  |
| 126 | player | Andy Moniz-Wakefield | andy-moniz-wakefield | GEN_DEF | 59 | 61 | +2 | +3.39% |  |
| 127 | player | Cooper Lord | cooper-lord | MID | 383 | 396 | +13 | +3.39% |  |
| 128 | player | Oskar Baker | oskar-baker | GEN_FWD | 29 | 30 | +1 | +3.45% |  |
| 129 | player | Milan Murdock | milan-murdock | GEN_FWD | 831 | 860 | +29 | +3.49% |  |
| 130 | player | Joel Amartey | joel-amartey | KEY_FWD | 143 | 148 | +5 | +3.50% |  |
| 131 | player | Rob Monahan | rob-monahan | GEN_DEF | 169 | 175 | +6 | +3.55% |  |
| 132 | player | Patrick Retschko | patrick-retschko | MID | 809 | 838 | +29 | +3.58% |  |
| 133 | player | Luke Cleary | luke-cleary | GEN_DEF | 83 | 86 | +3 | +3.61% |  |
| 134 | player | Caleb Windsor | caleb-windsor | MID | 1636 | 1696 | +60 | +3.67% |  |
| 135 | player | Charlie Cameron | charlie-cameron | GEN_FWD | 271 | 281 | +10 | +3.69% |  |
| 136 | player | Tobie Travaglia | tobie-travaglia | GEN_DEF | 758 | 786 | +28 | +3.69% |  |
| 137 | player | Daniel Annable | daniel-annable | MID | 1948 | 2020 | +72 | +3.70% |  |
| 138 | player | Harry Morrison | harry-morrison | MID | 27 | 28 | +1 | +3.70% |  |
| 139 | player | Changkuoth Jiath | changkuoth-jiath | GEN_DEF | 27 | 28 | +1 | +3.70% |  |
| 140 | player | Harvey Thomas | harvey-thomas | GEN_FWD | 2368 | 2456 | +88 | +3.72% |  |
| 141 | player | Kade Chandler | kade-chandler | GEN_FWD | 1021 | 1059 | +38 | +3.72% |  |
| 142 | player | Jai Murray | jai-murray | MID | 1154 | 1197 | +43 | +3.73% |  |
| 143 | player | Jasper Alger | jasper-alger | GEN_FWD | 321 | 333 | +12 | +3.74% |  |
| 144 | player | Lennox Hoffman | lennox-hoffman | GEN_DEF | 240 | 249 | +9 | +3.75% |  |
| 145 | player | Rhett Bazzo | rhett-bazzo | KEY_DEF | 560 | 581 | +21 | +3.75% |  |
| 146 | player | Keighton Matofai-Forbes | keighton-matofai-forbes | GEN_DEF | 239 | 248 | +9 | +3.77% |  |
| 147 | player | Bo Allan | bo-allan | GEN_DEF | 1190 | 1235 | +45 | +3.78% |  |
| 148 | player | Matt Duffy | matt-duffy | GEN_DEF | 185 | 192 | +7 | +3.78% |  |
| 149 | player | Balyn O'Brien | balyn-o-brien | GEN_DEF | 264 | 274 | +10 | +3.79% |  |
| 150 | player | Ben Murphy | ben-murphy | GEN_DEF | 264 | 274 | +10 | +3.79% |  |
| 151 | player | Kobe McDonald | kobe-mcdonald | GEN_DEF | 264 | 274 | +10 | +3.79% |  |
| 152 | player | Indy Cotton | indy-cotton | GEN_DEF | 264 | 274 | +10 | +3.79% |  |
| 153 | player | Billy Cootee | billy-cootee | MID | 79 | 82 | +3 | +3.80% |  |
| 154 | player | Eamonn Armstrong | eamonn-armstrong | GEN_DEF | 158 | 164 | +6 | +3.80% |  |
| 155 | player | Aidan Johnson | aidan-johnson | KEY_FWD | 79 | 82 | +3 | +3.80% |  |
| 156 | player | Taylor Goad | taylor-goad | RUC | 788 | 818 | +30 | +3.81% | RUC |
| 157 | player | Dan Houston | dan-houston | GEN_DEF | 1207 | 1253 | +46 | +3.81% |  |
| 158 | player | Campbell Gray | campbell-gray | KEY_DEF | 236 | 245 | +9 | +3.81% |  |
| 159 | player | Cillian Bourke | cillian-bourke | GEN_DEF | 366 | 380 | +14 | +3.83% |  |
| 160 | player | Ned Long | ned-long | MID | 910 | 945 | +35 | +3.85% |  |
| 161 | player | Callum Coleman-Jones | callum-coleman-jones | KEY_FWD | 52 | 54 | +2 | +3.85% |  |
| 162 | player | Sam Sturt | sam-sturt | GEN_FWD | 52 | 54 | +2 | +3.85% |  |
| 163 | player | Tom Papley | tom-papley | GEN_FWD | 467 | 485 | +18 | +3.85% |  |
| 164 | player | Charlie Edwards | charlie-edwards | MID | 674 | 700 | +26 | +3.86% |  |
| 165 | player | Sullivan Robey | sullivan-robey | MID | 2141 | 2224 | +83 | +3.88% |  |
| 166 | player | Charlie Banfield | charlie-banfield | MID | 773 | 803 | +30 | +3.88% |  |
| 167 | player | Nick Madden | nick-madden | RUC | 1464 | 1521 | +57 | +3.89% | RUC |
| 168 | player | Shadeau Brain | shadeau-brain | GEN_DEF | 77 | 80 | +3 | +3.90% |  |
| 169 | player | Lloyd Meek | lloyd-meek | RUC | 896 | 931 | +35 | +3.91% | RUC |
| 170 | player | Nick Vlastuin | nick-vlastuin | GEN_DEF | 102 | 106 | +4 | +3.92% |  |
| 171 | player | Sam Switkowski | sam-switkowski | GEN_FWD | 51 | 53 | +2 | +3.92% |  |
| 172 | player | Xavier Taylor | xavier-taylor | GEN_DEF | 814 | 846 | +32 | +3.93% |  |
| 173 | player | Caleb Graham | caleb-graham | KEY_DEF | 76 | 79 | +3 | +3.95% |  |
| 174 | player | Josh Treacy | josh-treacy | KEY_FWD | 6055 | 6297 | +242 | +4.00% |  |
| 175 | player | Lachlan Sholl | lachlan-sholl | MID | 225 | 234 | +9 | +4.00% |  |
| 176 | player | Mitch McGovern | mitch-mcgovern | GEN_DEF | 25 | 26 | +1 | +4.00% |  |
| 177 | player | Ned Reeves | ned-reeves | RUC | 374 | 389 | +15 | +4.01% | RUC |
| 178 | player | Tom Anastasopoulos | thomas-anastasopoulos | GEN_FWD | 299 | 311 | +12 | +4.01% |  |
| 179 | player | Hugh Boxshall | hugh-boxshall | MID | 921 | 958 | +37 | +4.02% |  |
| 180 | player | Will Graham | will-graham | GEN_FWD | 1145 | 1191 | +46 | +4.02% |  |
| 181 | player | Cameron Zurhaar | cameron-zurhaar | GEN_FWD | 199 | 207 | +8 | +4.02% |  |
| 182 | player | Harry Charleson | harry-charleson | GEN_DEF | 248 | 258 | +10 | +4.03% |  |
| 183 | player | Samuel Grlj | samuel-grlj | MID | 2470 | 2570 | +100 | +4.05% |  |
| 184 | player | Brandon Zerk-Thatcher | brandon-zerk-thatcher | KEY_DEF | 247 | 257 | +10 | +4.05% |  |
| 185 | player | Jake Rogers | jake-rogers | GEN_FWD | 592 | 616 | +24 | +4.05% |  |
| 186 | player | Buku Khamis | buku-khamis | KEY_DEF | 74 | 77 | +3 | +4.05% |  |
| 187 | player | Jack Ginnivan | jack-ginnivan | GEN_FWD | 1772 | 1844 | +72 | +4.06% |  |
| 188 | player | Jaxon Prior | jaxon-prior | GEN_DEF | 295 | 307 | +12 | +4.07% |  |
| 189 | player | Sam Marshall | sam-marshall | MID | 1105 | 1150 | +45 | +4.07% |  |
| 190 | player | Josh Smillie | josh-smillie | MID | 1250 | 1301 | +51 | +4.08% |  |
| 191 | player | Patrick Dangerfield | patrick-dangerfield | GEN_FWD | 98 | 102 | +4 | +4.08% |  |
| 192 | player | Harrison Petty | harrison-petty | KEY_DEF | 147 | 153 | +6 | +4.08% |  |
| 193 | player | Aidan Corr | aidan-corr | KEY_DEF | 49 | 51 | +2 | +4.08% |  |
| 194 | player | Jade Gresham | jade-gresham | GEN_FWD | 49 | 51 | +2 | +4.08% |  |
| 195 | player | Tom Atkins | tom-atkins | MID | 293 | 305 | +12 | +4.10% |  |
| 196 | player | Harry Rowston | harry-rowston | MID | 903 | 940 | +37 | +4.10% |  |
| 197 | player | Lachlan McAndrew | lachlan-mcandrew | RUC | 998 | 1039 | +41 | +4.11% | RUC |
| 198 | player | Jordon Sweet | jordon-sweet | RUC | 2064 | 2149 | +85 | +4.12% | RUC |
| 199 | player | Sam Draper | sam-draper | RUC | 631 | 657 | +26 | +4.12% | RUC |
| 200 | player | Sandy Brock | sandy-brock | KEY_DEF | 363 | 378 | +15 | +4.13% |  |
| 201 | player | Zak Johnson | zak-johnson | GEN_DEF | 532 | 554 | +22 | +4.14% |  |
| 202 | player | Josh Lai | josh-lai | GEN_DEF | 338 | 352 | +14 | +4.14% |  |
| 203 | player | Matthew Jefferson | matthew-jefferson | KEY_FWD | 555 | 578 | +23 | +4.14% |  |
| 204 | player | Joe Berry | joe-berry | GEN_FWD | 1278 | 1331 | +53 | +4.15% |  |
| 205 | player | Tristan Xerri | tristan-xerri | RUC | 6384 | 6649 | +265 | +4.15% | RUC |
| 206 | player | Jack Whitlock | jack-whitlock | KEY_FWD | 1250 | 1302 | +52 | +4.16% |  |
| 207 | player | Jarrod Witts | jarrod-witts | RUC | 384 | 400 | +16 | +4.17% | RUC |
| 208 | player | Isaac Cumming | isaac-cumming | GEN_DEF | 48 | 50 | +2 | +4.17% |  |
| 209 | player | Taylor Adams | taylor-adams | GEN_FWD | 72 | 75 | +3 | +4.17% |  |
| 210 | player | Oscar McDonald | oscar-mcdonald | KEY_DEF | 48 | 50 | +2 | +4.17% |  |
| 211 | player | Nicholas Coffield | nicholas-coffield | GEN_DEF | 48 | 50 | +2 | +4.17% |  |
| 212 | player | Bradley Close | bradley-close | GEN_FWD | 24 | 25 | +1 | +4.17% |  |
| 213 | player | Matt Guelfi | matt-guelfi | GEN_FWD | 24 | 25 | +1 | +4.17% |  |
| 214 | player | Nick Murray | nick-murray | KEY_DEF | 215 | 224 | +9 | +4.19% |  |
| 215 | player | Tyler Sonsie | tyler-sonsie | MID | 764 | 796 | +32 | +4.19% |  |
| 216 | player | James Leake | james-leake | GEN_DEF | 334 | 348 | +14 | +4.19% |  |
| 217 | player | Conor Nash | conor-nash | MID | 286 | 298 | +12 | +4.20% |  |
| 218 | player | Angus Anderson | angus-anderson | MID | 119 | 124 | +5 | +4.20% |  |
| 219 | player | Kane McAuliffe | kane-mcauliffe | MID | 1235 | 1287 | +52 | +4.21% |  |
| 220 | player | Steele Sidebottom | steele-sidebottom | MID | 95 | 99 | +4 | +4.21% |  |
| 221 | player | Reilly O'Brien | reilly-o-brien | RUC | 783 | 816 | +33 | +4.21% | RUC |
| 222 | player | Jack Sinclair | jack-sinclair | GEN_DEF | 3013 | 3140 | +127 | +4.22% |  |
| 223 | player | Jayden Short | jayden-short | GEN_DEF | 1516 | 1580 | +64 | +4.22% |  |
| 224 | player | Will Edwards | will-edwards | KEY_DEF | 260 | 271 | +11 | +4.23% |  |
| 225 | player | Toby Bedford | toby-bedford | GEN_FWD | 236 | 246 | +10 | +4.24% |  |
| 226 | player | Rowan Marshall | rowan-marshall | RUC | 612 | 638 | +26 | +4.25% | RUC |
| 227 | player | Harvey Langford | harvey-langford | MID | 2469 | 2574 | +105 | +4.25% |  |
| 228 | player | Jacob Hopper | jacob-hopper | MID | 117 | 122 | +5 | +4.27% |  |
| 229 | player | Hayden McLean | hayden-mclean | KEY_FWD | 631 | 658 | +27 | +4.28% |  |
| 230 | player | Will Lorenz | will-lorenz | MID | 397 | 414 | +17 | +4.28% |  |
| 231 | player | Braeden Campbell | braeden-campbell | GEN_DEF | 210 | 219 | +9 | +4.29% |  |
| 232 | player | Liam Baker | liam-baker | GEN_DEF | 630 | 657 | +27 | +4.29% |  |
| 233 | player | Isaac Keeler | isaac-keeler | KEY_FWD | 419 | 437 | +18 | +4.30% |  |
| 234 | player | Lachlan Bramble | lachlan-bramble | GEN_FWD | 93 | 97 | +4 | +4.30% |  |
| 235 | player | Bodhi Uwland | bodhi-uwland | GEN_DEF | 3045 | 3176 | +131 | +4.30% |  |
| 236 | player | Nic Newman | nic-newman | GEN_DEF | 882 | 920 | +38 | +4.31% |  |
| 237 | player | Cillian Burke | cillian-burke | GEN_DEF | 116 | 121 | +5 | +4.31% |  |
| 238 | player | Mason Redman | mason-redman | GEN_DEF | 1437 | 1499 | +62 | +4.31% |  |
| 239 | player | Kai Lohmann | kai-lohmann | GEN_FWD | 463 | 483 | +20 | +4.32% |  |
| 240 | player | Rory Laird | rory-laird | GEN_DEF | 924 | 964 | +40 | +4.33% |  |
| 241 | player | Ben McKay | ben-mckay | KEY_DEF | 46 | 48 | +2 | +4.35% |  |
| 242 | player | Matt Cottrell | matt-cottrell | MID | 46 | 48 | +2 | +4.35% |  |
| 243 | player | Nicholas Holman | nicholas-holman | GEN_FWD | 23 | 24 | +1 | +4.35% |  |
| 244 | player | Jack Crisp | jack-crisp | MID | 597 | 623 | +26 | +4.36% |  |
| 245 | player | Jacob Moss | jacob-moss | KEY_FWD | 275 | 287 | +12 | +4.36% |  |
| 246 | player | Keidean Coleman | keidean-coleman | GEN_DEF | 617 | 644 | +27 | +4.38% |  |
| 247 | player | Ty Gallop | ty-gallop | KEY_FWD | 1119 | 1168 | +49 | +4.38% |  |
| 248 | player | Max King | max-king-stk | KEY_FWD | 365 | 381 | +16 | +4.38% |  |
| 249 | player | Alix Tauru | alix-tauru | KEY_DEF | 1642 | 1714 | +72 | +4.38% |  |
| 250 | player | Clay Hall | clay-hall | MID | 592 | 618 | +26 | +4.39% |  |
| 251 | player | Jedd Busslinger | jedd-busslinger | KEY_DEF | 728 | 760 | +32 | +4.40% |  |
| 252 | player | Tylar Young | tylar-young | KEY_DEF | 91 | 95 | +4 | +4.40% |  |
| 253 | player | Adam Saad | adam-saad | GEN_DEF | 636 | 664 | +28 | +4.40% |  |
| 254 | player | Matt Carroll | matt-carroll | MID | 929 | 970 | +41 | +4.41% |  |
| 255 | player | Daniel Curtin | daniel-curtin | MID | 2148 | 2243 | +95 | +4.42% |  |
| 256 | player | Tai Hayes | tai-hayes | GEN_FWD | 271 | 283 | +12 | +4.43% |  |
| 257 | player | Lachie Neale | lachie-neale | MID | 1826 | 1907 | +81 | +4.44% |  |
| 258 | player | Jaren Carr | jaren-carr | GEN_FWD | 225 | 235 | +10 | +4.44% |  |
| 259 | player | Jackson Macrae | jackson-macrae | MID | 246 | 257 | +11 | +4.47% |  |
| 260 | player | Ryan Lester | ryan-lester | KEY_DEF | 939 | 981 | +42 | +4.47% |  |
| 261 | player | Oliver Hayes-Brown | oliver-hayes-brown | RUC | 335 | 350 | +15 | +4.48% | RUC |
| 262 | player | Taj Hotton | taj-hotton | MID | 1607 | 1679 | +72 | +4.48% |  |
| 263 | player | Cooper Hynes | cooper-hynes | MID | 1249 | 1305 | +56 | +4.48% |  |
| 264 | player | Xavier Walsh | xavier-walsh | KEY_DEF | 223 | 233 | +10 | +4.48% |  |
| 265 | player | Nicholas Martin | nicholas-martin | MID | 2809 | 2935 | +126 | +4.49% |  |
| 266 | player | Bodie Ryan | bodie-ryan | GEN_DEF | 312 | 326 | +14 | +4.49% |  |
| 267 | player | Ollie Dempsey | ollie-dempsey | MID | 1737 | 1815 | +78 | +4.49% |  |
| 268 | player | Christian Moraes | christian-moraes | MID | 979 | 1023 | +44 | +4.49% |  |
| 269 | player | Tom McDonald | tom-mcdonald | KEY_DEF | 356 | 372 | +16 | +4.49% |  |
| 270 | player | Jack Henry | jack-henry | KEY_DEF | 200 | 209 | +9 | +4.50% |  |
| 271 | player | Koltyn Tholstrup | koltyn-tholstrup | GEN_DEF | 1332 | 1392 | +60 | +4.50% |  |
| 272 | player | Beau Addinsall | beau-addinsall | MID | 1064 | 1112 | +48 | +4.51% |  |
| 273 | player | Isaac Kako | isaac-kako | GEN_FWD | 1570 | 1641 | +71 | +4.52% |  |
| 274 | player | Zach Guthrie | zach-guthrie | GEN_DEF | 464 | 485 | +21 | +4.53% |  |
| 275 | player | Brayden Maynard | brayden-maynard | GEN_DEF | 880 | 920 | +40 | +4.55% |  |
| 276 | player | Lachlan Blakiston | lachlan-blakiston | KEY_DEF | 22 | 23 | +1 | +4.55% |  |
| 277 | player | Nick Larkey | nick-larkey | KEY_FWD | 550 | 575 | +25 | +4.55% |  |
| 278 | player | Oliver Henry | oliver-henry | GEN_FWD | 88 | 92 | +4 | +4.55% |  |
| 279 | player | Liam McMahon | liam-mcmahon | KEY_FWD | 220 | 230 | +10 | +4.55% |  |
| 280 | player | Sam Wicks | sam-wicks | GEN_DEF | 22 | 23 | +1 | +4.55% |  |
| 281 | player | Joel Jeffrey | joel-jeffrey | GEN_DEF | 1644 | 1719 | +75 | +4.56% |  |
| 282 | player | Harry DeMattia | harry-demattia | MID | 460 | 481 | +21 | +4.57% |  |
| 283 | player | Jake Soligo | jake-soligo | MID | 2079 | 2174 | +95 | +4.57% |  |
| 284 | player | Cooper Trembath | cooper-trembath | KEY_FWD | 1509 | 1578 | +69 | +4.57% |  |
| 285 | player | Riak Andrew | riak-andrew | KEY_DEF | 306 | 320 | +14 | +4.58% |  |
| 286 | player | Rhylee West | rhylee-west | GEN_FWD | 153 | 160 | +7 | +4.58% |  |
| 287 | player | Joel Freijah | joel-freijah | MID | 2182 | 2282 | +100 | +4.58% |  |
| 288 | player | Matthew Roberts | matthew-roberts | GEN_DEF | 1679 | 1756 | +77 | +4.59% |  |
| 289 | player | Jack Payne | jack-payne | KEY_DEF | 218 | 228 | +10 | +4.59% |  |
| 290 | player | Bayley Fritsch | bayley-fritsch | GEN_FWD | 196 | 205 | +9 | +4.59% |  |
| 291 | player | Josh Dolan | josh-dolan | GEN_FWD | 435 | 455 | +20 | +4.60% |  |
| 292 | player | Cody Angove | cody-angove | MID | 608 | 636 | +28 | +4.61% |  |
| 293 | player | Peter Ladhams | peter-ladhams | RUC | 456 | 477 | +21 | +4.61% | RUC |
| 294 | player | Samson Ryan | samson-ryan | RUC | 608 | 636 | +28 | +4.61% | RUC |
| 295 | player | Jordan Croft | jordan-croft | KEY_FWD | 1039 | 1087 | +48 | +4.62% |  |
| 296 | player | Jhye Clark | jhye-clark | MID | 670 | 701 | +31 | +4.63% |  |
| 297 | player | Jeremy Sharp | jeremy-sharp | MID | 108 | 113 | +5 | +4.63% |  |
| 298 | player | Elijah Tsatas | elijah-tsatas | MID | 1185 | 1240 | +55 | +4.64% |  |
| 299 | player | Will Brodie | will-brodie | MID | 1034 | 1082 | +48 | +4.64% |  |
| 300 | player | Mitchell Lewis | mitchell-lewis | KEY_FWD | 581 | 608 | +27 | +4.65% |  |
| 301 | player | Harley Barker | harley-barker | MID | 710 | 743 | +33 | +4.65% |  |
| 302 | player | Sam Davidson | sam-davidson | GEN_FWD | 86 | 90 | +4 | +4.65% |  |
| 303 | player | Patrick Voss | patrick-voss | KEY_FWD | 1631 | 1707 | +76 | +4.66% |  |
| 304 | player | Wil Dawson | wil-dawson | KEY_DEF | 515 | 539 | +24 | +4.66% |  |
| 305 | player | Henry Hustwaite | henry-hustwaite | MID | 343 | 359 | +16 | +4.66% |  |
| 306 | player | Harrison Jones | harrison-jones | KEY_FWD | 107 | 112 | +5 | +4.67% |  |
| 307 | player | Bailey Macdonald | bailey-macdonald | GEN_DEF | 107 | 112 | +5 | +4.67% |  |
| 308 | player | Lachy Dovaston | lachy-dovaston | GEN_FWD | 897 | 939 | +42 | +4.68% |  |
| 309 | player | Patrick Said | patrick-said | GEN_FWD | 192 | 201 | +9 | +4.69% |  |
| 310 | player | Daniel McStay | daniel-mcstay | KEY_FWD | 64 | 67 | +3 | +4.69% |  |
| 311 | player | Errol Gulden | errol-gulden | MID | 5715 | 5983 | +268 | +4.69% |  |
| 312 | player | Luke Nankervis | luke-nankervis | GEN_DEF | 341 | 357 | +16 | +4.69% |  |
| 313 | player | Caleb Serong | caleb-serong | MID | 4490 | 4701 | +211 | +4.70% |  |
| 314 | player | Rhys Unwin | rhys-unwin | GEN_FWD | 191 | 200 | +9 | +4.71% |  |
| 315 | player | Chayce Jones | chayce-jones | MID | 106 | 111 | +5 | +4.72% |  |
| 316 | player | Trent Rivers | trent-rivers | GEN_DEF | 1713 | 1794 | +81 | +4.73% |  |
| 317 | player | Alex Davies | alex-davies | MID | 592 | 620 | +28 | +4.73% |  |
| 318 | player | Kane Farrell | kane-farrell | GEN_DEF | 1435 | 1503 | +68 | +4.74% |  |
| 319 | player | Shaun Mannagh | shaun-mannagh | GEN_FWD | 526 | 551 | +25 | +4.75% |  |
| 320 | player | Mabior Chol | mabior-chol | KEY_FWD | 315 | 330 | +15 | +4.76% |  |
| 321 | player | Francis Evans | francis-evans | GEN_FWD | 63 | 66 | +3 | +4.76% |  |
| 322 | player | Matt Johnson | matt-johnson-1 | MID | 608 | 637 | +29 | +4.77% |  |
| 323 | player | Thomas Liberatore | thomas-liberatore | MID | 1883 | 1973 | +90 | +4.78% |  |
| 324 | player | Tom Brown | tom-brown | GEN_DEF | 502 | 526 | +24 | +4.78% |  |
| 325 | player | Taylor Walker | taylor-walker | KEY_FWD | 230 | 241 | +11 | +4.78% |  |
| 326 | player | Hudson O'Keeffe | hudson-o-keeffe | KEY_FWD | 376 | 394 | +18 | +4.79% |  |
| 327 | player | Paul Curtis | paul-curtis | GEN_FWD | 1355 | 1420 | +65 | +4.80% |  |
| 328 | player | Jaspa Fletcher | jaspa-fletcher | GEN_DEF | 1916 | 2008 | +92 | +4.80% |  |
| 329 | player | Mitchell Hinge | mitchell-hinge | GEN_DEF | 458 | 480 | +22 | +4.80% |  |
| 330 | player | Oliver Hollands | oliver-hollands | GEN_DEF | 1457 | 1527 | +70 | +4.80% |  |
| 331 | player | Finlay Macrae | finlay-macrae | MID | 104 | 109 | +5 | +4.81% |  |
| 332 | player | Cody Anderson | cody-anderson | GEN_FWD | 187 | 196 | +9 | +4.81% |  |
| 333 | player | Ryan Angwin | ryan-angwin | MID | 436 | 457 | +21 | +4.82% |  |
| 334 | player | Darcy Fort | darcy-fort | RUC | 83 | 87 | +4 | +4.82% | RUC |
| 335 | player | Nate Caddy | nate-caddy | KEY_FWD | 1678 | 1759 | +81 | +4.83% |  |
| 336 | player | Deven Robertson | deven-robertson | MID | 290 | 304 | +14 | +4.83% |  |
| 337 | player | Willem Duursma | willem-duursma | MID | 4225 | 4429 | +204 | +4.83% |  |
| 338 | player | Josh Draper | josh-draper | KEY_DEF | 621 | 651 | +30 | +4.83% |  |
| 339 | player | Jack Lukosius | jack-lukosius | KEY_FWD | 1447 | 1517 | +70 | +4.84% |  |
| 340 | player | Ethan Read | ethan-read | KEY_FWD | 1425 | 1494 | +69 | +4.84% |  |
| 341 | player | Oliver Florent | oliver-florent | GEN_DEF | 743 | 779 | +36 | +4.85% |  |
| 342 | player | Wayne Milera | wayne-milera | GEN_DEF | 1692 | 1774 | +82 | +4.85% |  |
| 343 | player | Connor O'Sullivan | connor-o-sullivan | KEY_DEF | 2701 | 2832 | +131 | +4.85% |  |
| 344 | player | Tom Gross | tom-gross | MID | 618 | 648 | +30 | +4.85% |  |
| 345 | player | Joshua Weddle | joshua-weddle | GEN_DEF | 1543 | 1618 | +75 | +4.86% |  |
| 346 | player | Riley Thilthorpe | riley-thilthorpe | KEY_FWD | 3641 | 3818 | +177 | +4.86% |  |
| 347 | player | Nick Bryan | nick-bryan | RUC | 802 | 841 | +39 | +4.86% | RUC |
| 348 | player | Leo Lombard | leo-lombard | GEN_FWD | 1583 | 1660 | +77 | +4.86% |  |
| 349 | player | Darcy Wilson | darcy-wilson | GEN_FWD | 2343 | 2457 | +114 | +4.87% |  |
| 350 | player | Nick Blakey | nick-blakey | GEN_DEF | 3431 | 3598 | +167 | +4.87% |  |
| 351 | player | Xavier Duursma | xavier-duursma | MID | 267 | 280 | +13 | +4.87% |  |
| 352 | player | Luke Parker | luke-parker | GEN_DEF | 1415 | 1484 | +69 | +4.88% |  |
| 353 | player | Tim Membrey | tim-membrey | KEY_FWD | 41 | 43 | +2 | +4.88% |  |
| 354 | player | Callum Ah Chee | callum-ah-chee | GEN_FWD | 82 | 86 | +4 | +4.88% |  |
| 355 | player | James Jordon | james-jordon | MID | 41 | 43 | +2 | +4.88% |  |
| 356 | player | Tom Powell | tom-powell | GEN_FWD | 1885 | 1977 | +92 | +4.88% |  |
| 357 | player | Campbell Chesser | campbell-chesser | MID | 553 | 580 | +27 | +4.88% |  |
| 358 | player | Liam Fawcett | liam-fawcett | KEY_FWD | 512 | 537 | +25 | +4.88% |  |
| 359 | player | Touk Miller | touk-miller | MID | 1432 | 1502 | +70 | +4.89% |  |
| 360 | player | River Stevens | river-stevens | GEN_FWD | 184 | 193 | +9 | +4.89% |  |
| 361 | player | Isaac Quaynor | isaac-quaynor | GEN_DEF | 490 | 514 | +24 | +4.90% |  |
| 362 | player | Eric Hipwood | eric-hipwood | KEY_FWD | 102 | 107 | +5 | +4.90% |  |
| 363 | player | Jobe Shanahan | jobe-shanahan | KEY_FWD | 1550 | 1626 | +76 | +4.90% |  |
| 364 | player | Harry Kyle | harry-kyle | GEN_DEF | 875 | 918 | +43 | +4.91% |  |
| 365 | player | Sam Darcy | sam-darcy | KEY_FWD | 3825 | 4013 | +188 | +4.92% |  |
| 366 | player | Paddy Cross | paddy-cross | GEN_FWD | 61 | 64 | +3 | +4.92% |  |
| 367 | player | Elliott Himmelberg | elliot-himmelberg | KEY_FWD | 122 | 128 | +6 | +4.92% |  |
| 368 | player | Oskar Taylor | oskar-taylor | GEN_DEF | 772 | 810 | +38 | +4.92% |  |
| 369 | player | Harry Sheezel | harry-sheezel | MID | 7734 | 8115 | +381 | +4.93% |  |
| 370 | player | Zach Reid | zach-reid | KEY_DEF | 1640 | 1721 | +81 | +4.94% |  |
| 371 | player | Zane Duursma | zane-duursma | GEN_FWD | 749 | 786 | +37 | +4.94% |  |
| 372 | player | Peter Wright | peter-wright | KEY_FWD | 1902 | 1996 | +94 | +4.94% |  |
| 373 | player | Jordan Dawson | jordan-dawson | MID | 3156 | 3312 | +156 | +4.94% |  |
| 374 | player | Neil Erasmus | neil-erasmus | MID | 809 | 849 | +40 | +4.94% |  |
| 375 | player | Tom De Koning | tom-de-koning | RUC | 1638 | 1719 | +81 | +4.95% | RUC |
| 376 | player | Leek Aleer | leek-aleer | KEY_DEF | 323 | 339 | +16 | +4.95% |  |
| 377 | player | Cameron Mackenzie | cameron-mackenzie | MID | 1473 | 1546 | +73 | +4.96% |  |
| 378 | player | Hugo Garcia | hugo-garcia | MID | 2058 | 2160 | +102 | +4.96% |  |
| 379 | player | Patrick Lipinski | patrick-lipinski | GEN_FWD | 524 | 550 | +26 | +4.96% |  |
| 380 | player | Sid Draper | sid-draper | MID | 1448 | 1520 | +72 | +4.97% |  |
| 381 | player | Christian Salem | christian-salem | GEN_DEF | 583 | 612 | +29 | +4.97% |  |
| 382 | player | Sam Allen | sam-allen | MID | 784 | 823 | +39 | +4.97% |  |
| 383 | player | Heath Chapman | heath-chapman | GEN_DEF | 623 | 654 | +31 | +4.98% |  |
| 384 | player | Darcy Cameron | darcy-cameron | RUC | 1446 | 1518 | +72 | +4.98% | RUC |
| 385 | player | Tom Sparrow | tom-sparrow | MID | 482 | 506 | +24 | +4.98% |  |
| 386 | player | Harley Reid | harley-reid | MID | 3549 | 3726 | +177 | +4.99% |  |
| 387 | player | Jake Waterman | jake-waterman | KEY_FWD | 1483 | 1557 | +74 | +4.99% |  |
| 388 | player | Finn Callaghan | finn-callaghan | MID | 5183 | 5442 | +259 | +5.00% |  |
| 389 | player | Jacob Van Rooyen | jacob-van-rooyen | KEY_FWD | 1040 | 1092 | +52 | +5.00% |  |
| 390 | player | Josh Sinn | josh-sinn | GEN_DEF | 340 | 357 | +17 | +5.00% |  |
| 391 | player | Luke Urquhart | luke-urquhart | MID | 280 | 294 | +14 | +5.00% |  |
| 392 | player | Jack Higgins | jack-higgins | GEN_FWD | 200 | 210 | +10 | +5.00% |  |
| 393 | player | Conor Stone | conor-stone | GEN_DEF | 80 | 84 | +4 | +5.00% |  |
| 394 | player | Liam Henry | liam-henry | GEN_FWD | 80 | 84 | +4 | +5.00% |  |
| 395 | player | Phoenix Gothard | phoenix-gothard | GEN_FWD | 399 | 419 | +20 | +5.01% |  |
| 396 | player | Brodie Grundy | brodie-grundy | RUC | 3770 | 3959 | +189 | +5.01% | RUC |
| 397 | player | Rory Lobb | rory-lobb | KEY_DEF | 359 | 377 | +18 | +5.01% |  |
| 398 | player | Kysaiah Pickett | kysaiah-pickett | GEN_FWD | 3329 | 3496 | +167 | +5.02% |  |
| 399 | player | Reuben Ginbey | reuben-ginbey | KEY_DEF | 2847 | 2990 | +143 | +5.02% |  |
| 400 | player | Andrew McGrath | andrew-mcgrath | GEN_DEF | 1095 | 1150 | +55 | +5.02% |  |
| 401 | player | Jeremy Cameron | jeremy-cameron | KEY_FWD | 1453 | 1526 | +73 | +5.02% |  |
| 402 | player | Jack Darling | jack-darling | KEY_FWD | 378 | 397 | +19 | +5.03% |  |
| 403 | player | Shannon Neale | shannon-neale | KEY_FWD | 2327 | 2444 | +117 | +5.03% |  |
| 404 | player | Nathan O'Driscoll | nathan-o-driscoll | MID | 934 | 981 | +47 | +5.03% |  |
| 405 | player | Callum Wilkie | callum-wilkie | KEY_DEF | 3252 | 3416 | +164 | +5.04% |  |
| 406 | player | Matt Rowell | matt-rowell | MID | 3984 | 4185 | +201 | +5.05% |  |
| 407 | player | Harrison Ramm | harrison-ramm | KEY_DEF | 297 | 312 | +15 | +5.05% |  |
| 408 | player | Hugh McCluggage | hugh-mccluggage | MID | 1643 | 1726 | +83 | +5.05% |  |
| 409 | player | Liam Duggan | liam-duggan | GEN_DEF | 395 | 415 | +20 | +5.06% |  |
| 410 | player | Lachlan Fogarty | lachlan-fogarty | GEN_FWD | 79 | 83 | +4 | +5.06% |  |
| 411 | player | Nick Haynes | nick-haynes | GEN_DEF | 79 | 83 | +4 | +5.06% |  |
| 412 | player | Ryley Sanders | ryley-sanders | MID | 3930 | 4129 | +199 | +5.06% |  |
| 413 | player | Logan Morris | logan-morris | KEY_FWD | 3018 | 3171 | +153 | +5.07% |  |
| 414 | player | Anthony Caminiti | anthony-caminiti | KEY_FWD | 690 | 725 | +35 | +5.07% |  |
| 415 | player | Max Gruzewski | max-gruzewski | KEY_FWD | 414 | 435 | +21 | +5.07% |  |
| 416 | player | Mark Keane | mark-keane | KEY_DEF | 1557 | 1636 | +79 | +5.07% |  |
| 417 | player | Archer Reid | archer-reid | KEY_FWD | 1064 | 1118 | +54 | +5.08% |  |
| 418 | player | Tyan Prindable | tyan-prindable | MID | 709 | 745 | +36 | +5.08% |  |
| 419 | player | Marc Pittonet | marc-pittonet | RUC | 512 | 538 | +26 | +5.08% | RUC |
| 420 | player | Sam Berry | sam-berry | MID | 2520 | 2648 | +128 | +5.08% |  |
| 421 | player | Jack Buckley | jack-buckley | KEY_DEF | 728 | 765 | +37 | +5.08% |  |
| 422 | player | Callum Mills | callum-mills | GEN_DEF | 1810 | 1902 | +92 | +5.08% |  |
| 423 | player | Timothy English | timothy-english | RUC | 3187 | 3349 | +162 | +5.08% | RUC |
| 424 | player | Lewis Young | lewis-young | KEY_DEF | 177 | 186 | +9 | +5.08% |  |
| 425 | player | Jack Bowes | jack-bowes | MID | 118 | 124 | +6 | +5.08% |  |
| 426 | player | Jaeger O'Meara | jaeger-o-meara | MID | 177 | 186 | +9 | +5.08% |  |
| 427 | player | Jackson Mead | jackson-mead | GEN_FWD | 59 | 62 | +3 | +5.08% |  |
| 428 | player | Jye Amiss | jye-amiss | KEY_FWD | 1199 | 1260 | +61 | +5.09% |  |
| 429 | player | Cody Weightman | cody-weightman | GEN_FWD | 275 | 289 | +14 | +5.09% |  |
| 430 | player | Paddy Dow | paddy-dow | MID | 157 | 165 | +8 | +5.10% |  |
| 431 | player | Stephen Coniglio | stephen-coniglio | MID | 157 | 165 | +8 | +5.10% |  |
| 432 | player | Darcy Byrne-Jones | darcy-byrne-jones | GEN_DEF | 255 | 268 | +13 | +5.10% |  |
| 433 | player | Cooper Harvey | cooper-harvey | GEN_FWD | 98 | 103 | +5 | +5.10% |  |
| 434 | player | Jason Horne-Francis | jason-horne-francis | MID | 3802 | 3996 | +194 | +5.10% |  |
| 435 | player | Edward Allan | edward-allan | MID | 725 | 762 | +37 | +5.10% |  |
| 436 | player | Harry McKay | harry-mckay | KEY_FWD | 1762 | 1852 | +90 | +5.11% |  |
| 437 | player | Shai Bolton | shai-bolton | GEN_FWD | 2231 | 2345 | +114 | +5.11% |  |
| 438 | player | Sam Powell-Pepper | sam-powell-pepper | GEN_FWD | 313 | 329 | +16 | +5.11% |  |
| 439 | player | Nick Watson | nick-watson | GEN_FWD | 3539 | 3720 | +181 | +5.11% |  |
| 440 | player | Gryan Miers | gryan-miers | GEN_FWD | 1505 | 1582 | +77 | +5.12% |  |
| 441 | player | Sam Lalor | sam-lalor | MID | 3400 | 3574 | +174 | +5.12% |  |
| 442 | player | Aaron Cadman | aaron-cadman | KEY_FWD | 2970 | 3122 | +152 | +5.12% |  |
| 443 | player | Jesse Mellor | jesse-mellor | MID | 293 | 308 | +15 | +5.12% |  |
| 444 | player | Miles Bergman | miles-bergman | GEN_DEF | 664 | 698 | +34 | +5.12% |  |
| 445 | player | Matthew Flynn | matthew-flynn | RUC | 703 | 739 | +36 | +5.12% | RUC |
| 446 | player | Darcy Jones | darcy-jones | GEN_FWD | 1484 | 1560 | +76 | +5.12% |  |
| 447 | player | Tom Doedee | tom-doedee | GEN_DEF | 410 | 431 | +21 | +5.12% |  |
| 448 | player | Mitchito Owens | mitchito-owens | KEY_FWD | 2205 | 2318 | +113 | +5.12% |  |
| 449 | player | Sam De Koning | sam-de-koning | KEY_DEF | 995 | 1046 | +51 | +5.13% |  |
| 450 | player | Tom McCartin | tom-mccartin | KEY_DEF | 1443 | 1517 | +74 | +5.13% |  |
| 451 | player | Lachlan Weller | lachlan-weller | MID | 78 | 82 | +4 | +5.13% |  |
| 452 | player | Toby Pink | toby-pink | KEY_DEF | 39 | 41 | +2 | +5.13% |  |
| 453 | player | Will Setterfield | will-setterfield | MID | 1540 | 1619 | +79 | +5.13% |  |
| 454 | player | Luke Trainor | luke-trainor | KEY_DEF | 1420 | 1493 | +73 | +5.14% |  |
| 455 | player | Elijah Hewett | elijah-hewett | MID | 894 | 940 | +46 | +5.15% |  |
| 456 | player | Griffin Logue | griffin-logue | KEY_DEF | 136 | 143 | +7 | +5.15% |  |
| 457 | player | Jacob Weitering | jacob-weitering | KEY_DEF | 1282 | 1348 | +66 | +5.15% |  |
| 458 | player | Aaron Naughton | aaron-naughton | KEY_FWD | 1651 | 1736 | +85 | +5.15% |  |
| 459 | player | Charlie West | charlie-west | KEY_FWD | 427 | 449 | +22 | +5.15% |  |
| 460 | player | Sam Walsh | sam-walsh | MID | 2756 | 2898 | +142 | +5.15% |  |
| 461 | player | Jacob Farrow | jacob-farrow | GEN_DEF | 1664 | 1750 | +86 | +5.17% |  |
| 462 | player | Tom Edwards | tom-edwards | KEY_FWD | 58 | 61 | +3 | +5.17% |  |
| 463 | player | Dylan Stephens | dylan-stephens | MID | 348 | 366 | +18 | +5.17% |  |
| 464 | player | Zac Fisher | zac-fisher | GEN_FWD | 174 | 183 | +9 | +5.17% |  |
| 465 | player | Charlie Curnow | charlie-curnow | KEY_FWD | 1198 | 1260 | +62 | +5.18% |  |
| 466 | player | Max Gawn | max-gawn | RUC | 2413 | 2538 | +125 | +5.18% | RUC |
| 467 | player | Scott Pendlebury | scott-pendlebury | MID | 579 | 609 | +30 | +5.18% |  |
| 468 | pick | Pick 23 | pick-23 | PICK ASSET | 617 | 649 | +32 | +5.19% |  |
| 469 | player | Toby Greene | toby-greene | GEN_FWD | 829 | 872 | +43 | +5.19% |  |
| 470 | player | Logan Evans | logan-evans | GEN_DEF | 1194 | 1256 | +62 | +5.19% |  |
| 471 | pick | Pick 16 | pick-16 | PICK ASSET | 1001 | 1053 | +52 | +5.19% |  |
| 472 | player | Xavier Lindsay | xavier-lindsay | GEN_DEF | 1385 | 1457 | +72 | +5.20% |  |
| 473 | player | Max Holmes | max-holmes | MID | 5959 | 6269 | +310 | +5.20% |  |
| 474 | pick | Pick 24 | pick-24 | PICK ASSET | 615 | 647 | +32 | +5.20% |  |
| 475 | player | Patrick Cripps | patrick-cripps | MID | 1382 | 1454 | +72 | +5.21% |  |
| 476 | player | Ben Ainsworth | ben-ainsworth | GEN_FWD | 307 | 323 | +16 | +5.21% |  |
| 477 | pick | Pick 25 | pick-25 | PICK ASSET | 614 | 646 | +32 | +5.21% |  |
| 478 | pick | Pick 11 | pick-11 | PICK ASSET | 1381 | 1453 | +72 | +5.21% |  |
| 479 | pick | Pick 15 | pick-15 | PICK ASSET | 1074 | 1130 | +56 | +5.21% |  |
| 480 | player | Mac Andrew | mac-andrew | KEY_DEF | 3508 | 3691 | +183 | +5.22% |  |
| 481 | pick | Pick 8 | pick-8 | PICK ASSET | 1706 | 1795 | +89 | +5.22% |  |
| 482 | player | Luke Pedlar | luke-pedlar | GEN_FWD | 134 | 141 | +7 | +5.22% |  |
| 483 | pick | Pick 6 | pick-6 | PICK ASSET | 1875 | 1973 | +98 | +5.23% |  |
| 484 | pick | Pick 4 | pick-4 | PICK ASSET | 2085 | 2194 | +109 | +5.23% |  |
| 485 | pick | Pick 10 | pick-10 | PICK ASSET | 1492 | 1570 | +78 | +5.23% |  |
| 486 | pick | Pick 26 | pick-26 | PICK ASSET | 612 | 644 | +32 | +5.23% |  |
| 487 | player | Lachie Whitfield | lachie-whitfield | GEN_DEF | 2180 | 2294 | +114 | +5.23% |  |
| 488 | player | Kyle Langford | kyle-langford | KEY_FWD | 650 | 684 | +34 | +5.23% |  |
| 489 | player | Jed Walter | jed-walter | KEY_FWD | 1510 | 1589 | +79 | +5.23% |  |
| 490 | player | Josh Daicos | josh-daicos | GEN_DEF | 1873 | 1971 | +98 | +5.23% |  |
| 491 | player | Billy Frampton | billy-frampton | KEY_DEF | 172 | 181 | +9 | +5.23% |  |
| 492 | pick | Pick 1 | pick-1 | PICK ASSET | 3000 | 3157 | +157 | +5.23% |  |
| 493 | player | Noah Anderson | noah-anderson | MID | 4528 | 4765 | +237 | +5.23% |  |
| 494 | player | Riley Hardeman | riley-hardeman | GEN_DEF | 363 | 382 | +19 | +5.23% |  |
| 495 | player | Luke Jackson | luke-jackson | RUC | 7411 | 7799 | +388 | +5.24% | RUC |
| 496 | pick | Pick 5 | pick-5 | PICK ASSET | 1967 | 2070 | +103 | +5.24% |  |
| 497 | pick | Pick 7 | pick-7 | PICK ASSET | 1795 | 1889 | +94 | +5.24% |  |
| 498 | pick | Pick 9 | pick-9 | PICK ASSET | 1604 | 1688 | +84 | +5.24% |  |
| 499 | pick | Pick 13 | pick-13 | PICK ASSET | 1203 | 1266 | +63 | +5.24% |  |
| 500 | pick | Pick 27 | pick-27 | PICK ASSET | 611 | 643 | +32 | +5.24% |  |
| 501 | pick | Pick 2 | pick-2 | PICK ASSET | 2501 | 2632 | +131 | +5.24% |  |
| 502 | player | Zeke Uwland | zeke-uwland | GEN_DEF | 2119 | 2230 | +111 | +5.24% |  |
| 503 | pick | Pick 18 | pick-18 | PICK ASSET | 859 | 904 | +45 | +5.24% |  |
| 504 | player | Jack Gunston | jack-gunston | KEY_FWD | 1145 | 1205 | +60 | +5.24% |  |
| 505 | player | James Sicily | james-sicily | GEN_DEF | 1965 | 2068 | +103 | +5.24% |  |
| 506 | player | Sam Taylor | sam-taylor | KEY_DEF | 1774 | 1867 | +93 | +5.24% |  |
| 507 | player | Mitch Georgiades | mitch-georgiades | KEY_FWD | 1278 | 1345 | +67 | +5.24% |  |
| 508 | pick | Pick 3 | pick-3 | PICK ASSET | 2249 | 2367 | +118 | +5.25% |  |
| 509 | player | Toby Nankervis | toby-nankervis | RUC | 2001 | 2106 | +105 | +5.25% | RUC |
| 510 | player | Joel Cochran | joel-cochran | KEY_DEF | 362 | 381 | +19 | +5.25% |  |
| 511 | player | Brayden Cook | brayden-cook | MID | 743 | 782 | +39 | +5.25% |  |
| 512 | player | Jordan Clark | jordan-clark | GEN_DEF | 3142 | 3307 | +165 | +5.25% |  |
| 513 | player | Hamish Davis | hamish-davis | MID | 933 | 982 | +49 | +5.25% |  |
| 514 | player | Christian Petracca | christian-petracca | MID | 2703 | 2845 | +142 | +5.25% |  |
| 515 | pick | Pick 28 | pick-28 | PICK ASSET | 609 | 641 | +32 | +5.25% |  |
| 516 | pick | Pick 21 | pick-21 | PICK ASSET | 685 | 721 | +36 | +5.26% |  |
| 517 | player | Jack Steele | jack-steele | MID | 1597 | 1681 | +84 | +5.26% |  |
| 518 | player | Bailey J. Williams | bailey-williams-wc | RUC | 1672 | 1760 | +88 | +5.26% | RUC |
| 519 | player | Dylan Patterson | dylan-patterson | GEN_DEF | 874 | 920 | +46 | +5.26% |  |
| 520 | player | Jed Adams | jed-adams | KEY_DEF | 266 | 280 | +14 | +5.26% |  |
| 521 | player | Will Darcy | will-darcy | KEY_DEF | 532 | 560 | +28 | +5.26% |  |
| 522 | player | Jacob Wehr | jacob-wehr | GEN_DEF | 19 | 20 | +1 | +5.26% |  |
| 523 | player | Lewis Melican | lewis-melican | KEY_DEF | 57 | 60 | +3 | +5.26% |  |
| 524 | player | Liam Stocker | liam-stocker | GEN_DEF | 38 | 40 | +2 | +5.26% |  |
| 525 | player | Daniel Butler | daniel-butler | GEN_FWD | 19 | 20 | +1 | +5.26% |  |
| 526 | pick | Pick 22 | pick-22 | PICK ASSET | 646 | 680 | +34 | +5.26% |  |
| 527 | player | Adam Treloar | adam-treloar | MID | 607 | 639 | +32 | +5.27% |  |
| 528 | pick | Pick 29 | pick-29 | PICK ASSET | 607 | 639 | +32 | +5.27% |  |
| 529 | pick | Pick 14 | pick-14 | PICK ASSET | 1138 | 1198 | +60 | +5.27% |  |
| 530 | player | Jake Lever | jake-lever | KEY_DEF | 550 | 579 | +29 | +5.27% |  |
| 531 | player | Brennan Cox | brennan-cox | KEY_DEF | 512 | 539 | +27 | +5.27% |  |
| 532 | pick | Pick 17 | pick-17 | PICK ASSET | 929 | 978 | +49 | +5.27% |  |
| 533 | pick | Pick 12 | pick-12 | PICK ASSET | 1270 | 1337 | +67 | +5.28% |  |
| 534 | player | Jack Graham | jack-graham | MID | 303 | 319 | +16 | +5.28% |  |
| 535 | pick | Pick 30 | pick-30 | PICK ASSET | 606 | 638 | +32 | +5.28% |  |
| 536 | player | Logan McDonald | logan-mcdonald | KEY_FWD | 852 | 897 | +45 | +5.28% |  |
| 537 | player | Harry Dean | harry-dean | KEY_DEF | 1969 | 2073 | +104 | +5.28% |  |
| 538 | pick | Pick 19 | pick-19 | PICK ASSET | 795 | 837 | +42 | +5.28% |  |
| 539 | player | Patrick Snell | patrick-snell | KEY_DEF | 246 | 259 | +13 | +5.28% |  |
| 540 | player | Darcy Parish | darcy-parish | MID | 1419 | 1494 | +75 | +5.29% |  |
| 541 | player | Harrison Himmelberg | harrison-himmelberg | GEN_DEF | 454 | 478 | +24 | +5.29% |  |
| 542 | player | Tim Taranto | tim-taranto | MID | 2534 | 2668 | +134 | +5.29% |  |
| 543 | player | Beau McCreery | beau-mccreery | GEN_FWD | 208 | 219 | +11 | +5.29% |  |
| 544 | player | Sean Darcy | sean-darcy | RUC | 945 | 995 | +50 | +5.29% | RUC |
| 545 | player | Tanner Bruhn | tanner-bruhn | MID | 1000 | 1053 | +53 | +5.30% |  |
| 546 | pick | Pick 20 | pick-20 | PICK ASSET | 735 | 774 | +39 | +5.31% |  |
| 547 | player | Jy Simpkin | jy-simpkin | MID | 603 | 635 | +32 | +5.31% |  |
| 548 | player | Lewis Hayes | lewis-hayes | KEY_DEF | 358 | 377 | +19 | +5.31% |  |
| 549 | player | James Rowbottom | james-rowbottom | MID | 471 | 496 | +25 | +5.31% |  |
| 550 | player | Adam Cerra | adam-cerra | MID | 1149 | 1210 | +61 | +5.31% |  |
| 551 | player | Sam Flanders | sam-flanders | MID | 1714 | 1805 | +91 | +5.31% |  |
| 552 | player | Levi Ashcroft | levi-ashcroft | MID | 3032 | 3193 | +161 | +5.31% |  |
| 553 | player | Kieren Briggs | kieren-briggs | RUC | 2109 | 2221 | +112 | +5.31% | RUC |
| 554 | player | Will Ashcroft | will-ashcroft | MID | 4895 | 5155 | +260 | +5.31% |  |
| 555 | player | Jagga Smith | jagga-smith | MID | 3031 | 3192 | +161 | +5.31% |  |
| 556 | player | Andrew Brayshaw | andrew-brayshaw | MID | 2785 | 2933 | +148 | +5.31% |  |
| 557 | player | Cody Curtin | cody-curtin | KEY_FWD | 677 | 713 | +36 | +5.32% |  |
| 558 | player | Harry Edwards | harry-edwards | KEY_DEF | 94 | 99 | +5 | +5.32% |  |
| 559 | player | Tim Kelly | tim-kelly | MID | 921 | 970 | +49 | +5.32% |  |
| 560 | player | Brent Daniels | brent-daniels | GEN_FWD | 1315 | 1385 | +70 | +5.32% |  |
| 561 | player | Dyson Sharp | dyson-sharp | MID | 1615 | 1701 | +86 | +5.33% |  |
| 562 | player | Bailey Williams | bailey-williams-wb | GEN_DEF | 582 | 613 | +31 | +5.33% |  |
| 563 | player | Izak Rankine | izak-rankine | GEN_FWD | 2628 | 2768 | +140 | +5.33% |  |
| 564 | player | Finnbar Maley | finnbar-maley | KEY_FWD | 244 | 257 | +13 | +5.33% |  |
| 565 | player | Connor Rozee | connor-rozee | MID | 2271 | 2392 | +121 | +5.33% |  |
| 566 | player | Lachlan Schultz | lachlan-schultz | GEN_FWD | 619 | 652 | +33 | +5.33% |  |
| 567 | player | Cooper Bell | cooper-bell | KEY_DEF | 356 | 375 | +19 | +5.34% |  |
| 568 | player | Ollie Murphy | ollie-murphy | KEY_DEF | 281 | 296 | +15 | +5.34% |  |
| 569 | player | Ed Richards | ed-richards | MID | 2922 | 3078 | +156 | +5.34% |  |
| 570 | player | Will Hayward | will-hayward | GEN_FWD | 206 | 217 | +11 | +5.34% |  |
| 571 | player | Lachlan Ash | lachlan-ash | GEN_DEF | 4924 | 5187 | +263 | +5.34% |  |
| 572 | player | Jesse Dattoli | jesse-dattoli | GEN_FWD | 468 | 493 | +25 | +5.34% |  |
| 573 | player | Karl Amon | karl-amon | GEN_DEF | 786 | 828 | +42 | +5.34% |  |
| 574 | player | Jayden Laverde | jayden-laverde | KEY_DEF | 505 | 532 | +27 | +5.35% |  |
| 575 | player | Jarman Impey | jarman-impey | GEN_DEF | 692 | 729 | +37 | +5.35% |  |
| 576 | player | Tom Lynch | tom-lynch-1 | KEY_FWD | 187 | 197 | +10 | +5.35% |  |
| 577 | player | Willem Drew | willem-drew | MID | 860 | 906 | +46 | +5.35% |  |
| 578 | player | Oliver Wines | oliver-wines | MID | 486 | 512 | +26 | +5.35% |  |
| 579 | player | Hugh Davies | hugh-davies | KEY_DEF | 299 | 315 | +16 | +5.35% |  |
| 580 | player | Nasiah Wanganeen-Milera | nasiah-wanganeen-milera | MID | 6270 | 6606 | +336 | +5.36% |  |
| 581 | player | Reece Torrent | reece-torrent | MID | 205 | 216 | +11 | +5.37% |  |
| 582 | player | Joshua Kelly | joshua-kelly | MID | 559 | 589 | +30 | +5.37% |  |
| 583 | player | Angus Sheldrick | angus-sheldrick | MID | 801 | 844 | +43 | +5.37% |  |
| 584 | player | Connor MacDonald | connor-macdonald | GEN_FWD | 2309 | 2433 | +124 | +5.37% |  |
| 585 | player | Jye Caldwell | jye-caldwell | MID | 1452 | 1530 | +78 | +5.37% |  |
| 586 | player | Jack Silvagni | jack-silvagni | KEY_DEF | 614 | 647 | +33 | +5.37% |  |
| 587 | player | Oliver Wiltshire | oliver-wiltshire | GEN_FWD | 93 | 98 | +5 | +5.38% |  |
| 588 | player | Jack Martin | jack-martin | GEN_FWD | 93 | 98 | +5 | +5.38% |  |
| 589 | player | Blake Thredgold | blake-thredgold | KEY_DEF | 538 | 567 | +29 | +5.39% |  |
| 590 | player | Will Day | will-day | MID | 2949 | 3108 | +159 | +5.39% |  |
| 591 | player | Hunter Holmes | hunter-holmes | MID | 686 | 723 | +37 | +5.39% |  |
| 592 | player | Dante Visentini | dante-visentini | RUC | 723 | 762 | +39 | +5.39% | RUC |
| 593 | player | Ryan Maric | ryan-maric | MID | 1204 | 1269 | +65 | +5.40% |  |
| 594 | player | Noah Balta | noah-balta | KEY_FWD | 426 | 449 | +23 | +5.40% |  |
| 595 | player | Finnegan Davis | finnegan-davis | GEN_DEF | 407 | 429 | +22 | +5.41% |  |
| 596 | player | Brodie Kemp | brodie-kemp | KEY_FWD | 814 | 858 | +44 | +5.41% |  |
| 597 | player | Tom Barrass | tom-barrass | KEY_DEF | 481 | 507 | +26 | +5.41% |  |
| 598 | player | Jake Riccardi | jake-riccardi | KEY_FWD | 296 | 312 | +16 | +5.41% |  |
| 599 | player | Dion Prestia | dion-prestia | MID | 333 | 351 | +18 | +5.41% |  |
| 600 | player | Alex Pearce | alex-pearce | KEY_DEF | 37 | 39 | +2 | +5.41% |  |
| 601 | player | Justin McInerney | justin-mcinerney | MID | 1460 | 1539 | +79 | +5.41% |  |
| 602 | player | Bailey Humphrey | bailey-humphrey | GEN_FWD | 1422 | 1499 | +77 | +5.41% |  |
| 603 | player | James Worpel | james-worpel | MID | 517 | 545 | +28 | +5.42% |  |
| 604 | player | Darcy Wilmot | darcy-wilmot | GEN_DEF | 3763 | 3967 | +204 | +5.42% |  |
| 605 | player | Tom Green | tom-green | MID | 4165 | 4391 | +226 | +5.43% |  |
| 606 | player | Josh Dunkley | josh-dunkley | MID | 903 | 952 | +49 | +5.43% |  |
| 607 | player | Blake Hardwick | blake-hardwick | GEN_DEF | 387 | 408 | +21 | +5.43% |  |
| 608 | player | Mattaes Phillipou | mattaes-phillipou | MID | 1050 | 1107 | +57 | +5.43% |  |
| 609 | player | Charlie Comben | charlie-comben | KEY_DEF | 718 | 757 | +39 | +5.43% |  |
| 610 | player | Harvey Harrison | harvey-harrison | GEN_FWD | 92 | 97 | +5 | +5.43% |  |
| 611 | player | Josh Worrell | josh-worrell | GEN_DEF | 3016 | 3180 | +164 | +5.44% |  |
| 612 | player | Murphy Reid | murphy-reid | GEN_FWD | 3749 | 3953 | +204 | +5.44% |  |
| 613 | player | Zac Bailey | zac-bailey | GEN_FWD | 2389 | 2519 | +130 | +5.44% |  |
| 614 | player | Brayden Fiorini | brayden-fiorini | MID | 312 | 329 | +17 | +5.45% |  |
| 615 | player | Aliir Aliir | aliir-aliir | KEY_DEF | 1009 | 1064 | +55 | +5.45% |  |
| 616 | player | Jack Viney | jack-viney | MID | 385 | 406 | +21 | +5.45% |  |
| 617 | player | Hugo Ralphsmith | hugo-ralphsmith | MID | 55 | 58 | +3 | +5.45% |  |
| 618 | player | Noah Mraz | noah-mraz | KEY_DEF | 403 | 425 | +22 | +5.46% |  |
| 619 | player | Marcus Windhager | marcus-windhager | MID | 1557 | 1642 | +85 | +5.46% |  |
| 620 | player | Zak Butters | zak-butters | MID | 5745 | 6059 | +314 | +5.47% |  |
| 621 | player | Harvey Gallagher | harvey-gallagher | GEN_DEF | 128 | 135 | +7 | +5.47% |  |
| 622 | player | Jack Ough | jack-ough | MID | 402 | 424 | +22 | +5.47% |  |
| 623 | player | James Borlase | james-borlase | KEY_DEF | 475 | 501 | +26 | +5.47% |  |
| 624 | player | Jesse Hogan | jesse-hogan | KEY_FWD | 383 | 404 | +21 | +5.48% |  |
| 625 | player | Darcy Fogarty | darcy-fogarty | KEY_FWD | 383 | 404 | +21 | +5.48% |  |
| 626 | player | Daniel Rioli | daniel-rioli | GEN_DEF | 711 | 750 | +39 | +5.49% |  |
| 627 | player | Jonty Faull | jonty-faull | KEY_FWD | 1166 | 1230 | +64 | +5.49% |  |
| 628 | player | Maxwell King | max-king-syd | GEN_FWD | 255 | 269 | +14 | +5.49% |  |
| 629 | player | Thomas Sims | thomas-sims | KEY_FWD | 1056 | 1114 | +58 | +5.49% |  |
| 630 | player | Lachlan Jones | lachlan-jones | GEN_DEF | 91 | 96 | +5 | +5.49% |  |
| 631 | player | James Tunstill | james-tunstill | MID | 91 | 96 | +5 | +5.49% |  |
| 632 | player | Cameron Nairn | cameron-nairn | GEN_FWD | 764 | 806 | +42 | +5.50% |  |
| 633 | player | Matthew Kennedy | matthew-kennedy-1 | MID | 600 | 633 | +33 | +5.50% |  |
| 634 | player | Ben Keays | ben-keays | GEN_FWD | 309 | 326 | +17 | +5.50% |  |
| 635 | player | Jarrod Berry | jarrod-berry | MID | 527 | 556 | +29 | +5.50% |  |
| 636 | player | Zachary Merrett | zachary-merrett | MID | 2925 | 3086 | +161 | +5.50% |  |
| 637 | player | Matthew LeRay | matthew-leray | MID | 472 | 498 | +26 | +5.51% |  |
| 638 | player | Kye Fincher | kye-fincher | MID | 490 | 517 | +27 | +5.51% |  |
| 639 | player | Josh Battle | josh-battle | KEY_DEF | 2095 | 2211 | +116 | +5.54% |  |
| 640 | player | Isaac Heeney | isaac-heeney | MID | 3772 | 3981 | +209 | +5.54% |  |
| 641 | player | Harrison Oliver | harrison-oliver | GEN_DEF | 541 | 571 | +30 | +5.55% |  |
| 642 | player | James Barrat | james-barrat | KEY_DEF | 414 | 437 | +23 | +5.56% |  |
| 643 | player | Harry O'Farrell | harry-o-farrell | KEY_DEF | 810 | 855 | +45 | +5.56% |  |
| 644 | player | Max Michalanney | max-michalanney | GEN_DEF | 576 | 608 | +32 | +5.56% |  |
| 645 | player | Riley Hamilton | riley-hamilton | GEN_FWD | 342 | 361 | +19 | +5.56% |  |
| 646 | player | Darcy Moore | darcy-moore | KEY_DEF | 198 | 209 | +11 | +5.56% |  |
| 647 | player | Luke McDonald | luke-mcdonald | GEN_DEF | 54 | 57 | +3 | +5.56% |  |
| 648 | player | Jake Kolodjashnij | jake-kolodjashnij | KEY_DEF | 36 | 38 | +2 | +5.56% |  |
| 649 | player | Bobby Hill | bobby-hill | GEN_FWD | 72 | 76 | +4 | +5.56% |  |
| 650 | player | Nick Daicos | nick-daicos | MID | 7626 | 8050 | +424 | +5.56% |  |
| 651 | player | Finn O'Sullivan | finn-o-sullivan | MID | 3451 | 3643 | +192 | +5.56% |  |
| 652 | player | Colby McKercher | colby-mckercher | MID | 3627 | 3829 | +202 | +5.57% |  |
| 653 | player | Archie Roberts | archie-roberts | GEN_DEF | 4327 | 4568 | +241 | +5.57% |  |
| 654 | player | Lucas Camporeale | lucas-camporeale | MID | 287 | 303 | +16 | +5.57% |  |
| 655 | player | Ben Camporeale | ben-camporeale | MID | 340 | 359 | +19 | +5.59% |  |
| 656 | player | Marcus Bontempelli | marcus-bontempelli | MID | 3524 | 3721 | +197 | +5.59% |  |
| 657 | player | Jake Bowey | jake-bowey | GEN_DEF | 2932 | 3096 | +164 | +5.59% |  |
| 658 | player | George Hewett | george-hewett | MID | 1412 | 1491 | +79 | +5.59% |  |
| 659 | player | Kaleb Smith | kaleb-smith | GEN_DEF | 107 | 113 | +6 | +5.61% |  |
| 660 | player | Caleb Daniel | caleb-daniel | GEN_DEF | 1229 | 1298 | +69 | +5.61% |  |
| 661 | player | Seth Campbell | seth-campbell | GEN_FWD | 1032 | 1090 | +58 | +5.62% |  |
| 662 | player | George Wardlaw | george-wardlaw | MID | 3035 | 3206 | +171 | +5.63% |  |
| 663 | player | Cameron Rayner | cameron-rayner | GEN_FWD | 479 | 506 | +27 | +5.64% |  |
| 664 | player | George Stevens | george-stevens | MID | 337 | 356 | +19 | +5.64% |  |
| 665 | player | Samuel Collins | samuel-collins | KEY_DEF | 940 | 993 | +53 | +5.64% |  |
| 666 | player | Chad Warner | chad-warner | MID | 2728 | 2882 | +154 | +5.65% |  |
| 667 | player | Lucca Grego | lucca-grego | GEN_DEF | 248 | 262 | +14 | +5.65% |  |
| 668 | player | Luke Davies-Uniacke | luke-davies-uniacke | MID | 3274 | 3459 | +185 | +5.65% |  |
| 669 | player | Harry Schoenberg | harry-schoenberg | MID | 53 | 56 | +3 | +5.66% |  |
| 670 | player | Clayton Oliver | clayton-oliver | MID | 2473 | 2613 | +140 | +5.66% |  |
| 671 | player | Jack Ross | jack-ross | MID | 1641 | 1734 | +93 | +5.67% |  |
| 672 | player | Samuel Swadling | samuel-swadling | MID | 616 | 651 | +35 | +5.68% |  |
| 673 | player | Koby Coulson | koby-coulson | MID | 528 | 558 | +30 | +5.68% |  |
| 674 | player | Harry Perryman | harry-perryman | GEN_DEF | 176 | 186 | +10 | +5.68% |  |
| 675 | player | Sam Banks | sam-banks | GEN_DEF | 915 | 967 | +52 | +5.68% |  |
| 676 | player | Calsher Dear | calsher-dear | KEY_FWD | 1054 | 1114 | +60 | +5.69% |  |
| 677 | player | Bradley Hill | bradley-hill | GEN_FWD | 807 | 853 | +46 | +5.70% |  |
| 678 | player | Joe Richards | joe-richards | GEN_FWD | 842 | 890 | +48 | +5.70% |  |
| 679 | player | Lachlan Cowan | lachlan-cowan | GEN_DEF | 630 | 666 | +36 | +5.71% |  |
| 680 | player | Bailey Laurie | bailey-laurie | GEN_FWD | 70 | 74 | +4 | +5.71% |  |
| 681 | player | Joel Hamling | joel-hamling | KEY_DEF | 35 | 37 | +2 | +5.71% |  |
| 682 | player | Elliot Yeo | elliot-yeo | MID | 542 | 573 | +31 | +5.72% |  |
| 683 | player | Mason Wood | mason-wood | GEN_FWD | 157 | 166 | +9 | +5.73% |  |
| 684 | player | Alex Neal-Bullen | alex-neal-bullen | GEN_FWD | 488 | 516 | +28 | +5.74% |  |
| 685 | player | Judson Clarke | judson-clarke | GEN_FWD | 87 | 92 | +5 | +5.75% |  |
| 686 | player | Jack Scrimshaw | jack-scrimshaw | GEN_DEF | 87 | 92 | +5 | +5.75% |  |
| 687 | player | Nikolas Cox | nikolas-cox | KEY_FWD | 400 | 423 | +23 | +5.75% |  |
| 688 | player | Jordan Ridley | jordan-ridley | GEN_DEF | 1059 | 1120 | +61 | +5.76% |  |
| 689 | player | Todd Marshall | todd-marshall | KEY_FWD | 156 | 165 | +9 | +5.77% |  |
| 690 | player | Hayden Young | hayden-young | MID | 2625 | 2777 | +152 | +5.79% |  |
| 691 | player | Josh Lindsay | josh-lindsay | GEN_DEF | 1620 | 1714 | +94 | +5.80% |  |
| 692 | player | Brayden George | brayden-george | GEN_FWD | 310 | 328 | +18 | +5.81% |  |
| 693 | player | Josh Ward | josh-ward | MID | 1650 | 1746 | +96 | +5.82% |  |
| 694 | player | Thomas Stewart | thomas-stewart | GEN_DEF | 1031 | 1091 | +60 | +5.82% |  |
| 695 | player | Ed Langdon | ed-langdon | GEN_DEF | 567 | 600 | +33 | +5.82% |  |
| 696 | player | Latrelle Pickett | latrelle-pickett | GEN_FWD | 617 | 653 | +36 | +5.83% |  |
| 697 | player | Hugo Mikunda | hugo-mikunda | GEN_FWD | 377 | 399 | +22 | +5.84% |  |
| 698 | player | Bailey Dale | bailey-dale | GEN_DEF | 1898 | 2009 | +111 | +5.85% |  |
| 699 | player | Dayne Zorko | dayne-zorko | GEN_DEF | 1105 | 1170 | +65 | +5.88% |  |
| 700 | player | Corey Durdin | corey-durdin | GEN_FWD | 51 | 54 | +3 | +5.88% |  |
| 701 | player | Finn Maginness | finn-maginness | GEN_FWD | 34 | 36 | +2 | +5.88% |  |
| 702 | player | Charlie Spargo | charlie-spargo | GEN_FWD | 34 | 36 | +2 | +5.88% |  |
| 703 | player | Angus Clarke | angus-clarke | GEN_DEF | 729 | 772 | +43 | +5.90% |  |
| 704 | player | Daniel Turner | daniel-turner | KEY_DEF | 1592 | 1686 | +94 | +5.90% |  |
| 705 | player | Adam Sweid | adam-sweid | GEN_FWD | 626 | 663 | +37 | +5.91% |  |
| 706 | player | Charlie Ballard | charlie-ballard | KEY_DEF | 118 | 125 | +7 | +5.93% |  |
| 707 | player | Tobyn Murray | tobyn-murray | GEN_FWD | 421 | 446 | +25 | +5.94% |  |
| 708 | player | Sam Butler | sam-butler-1 | GEN_FWD | 101 | 107 | +6 | +5.94% |  |
| 709 | player | Jai Serong | jai-serong | GEN_DEF | 101 | 107 | +6 | +5.94% |  |
| 710 | player | Jay Polkinghorne | jay-polkinghorne | GEN_FWD | 252 | 267 | +15 | +5.95% |  |
| 711 | player | Jeremy Howe | jeremy-howe | GEN_DEF | 285 | 302 | +17 | +5.96% |  |
| 712 | player | Hunter Clark | hunter-clark | GEN_DEF | 50 | 53 | +3 | +6.00% |  |
| 713 | player | Cooper Sharman | cooper-sharman | KEY_FWD | 516 | 547 | +31 | +6.01% |  |
| 714 | player | Lachlan Carmichael | lachlan-carmichael | GEN_DEF | 598 | 634 | +36 | +6.02% |  |
| 715 | player | Tylah Williams | tylah-williams | GEN_FWD | 464 | 492 | +28 | +6.03% |  |
| 716 | player | Jack Williams | jack-williams | KEY_FWD | 529 | 561 | +32 | +6.05% |  |
| 717 | player | Lachie Jaques | lachie-jaques | GEN_DEF | 723 | 767 | +44 | +6.09% |  |
| 718 | player | Tom Blamires | tom-blamires | GEN_DEF | 82 | 87 | +5 | +6.10% |  |
| 719 | player | Koby Evans | koby-evans | GEN_FWD | 475 | 504 | +29 | +6.11% |  |
| 720 | player | Tyler Welsh | tyler-welsh | KEY_FWD | 229 | 243 | +14 | +6.11% |  |
| 721 | player | Bailey Smith | bailey-smith | MID | 5282 | 5605 | +323 | +6.12% |  |
| 722 | player | Ben Miller | ben-miller | KEY_DEF | 1177 | 1249 | +72 | +6.12% |  |
| 723 | player | Nathan Wardius | nathan-wardius | GEN_FWD | 147 | 156 | +9 | +6.12% |  |
| 724 | player | Oscar Allen | oscar-allen | KEY_FWD | 179 | 190 | +11 | +6.15% |  |
| 725 | player | Zane Zakostelsky | zane-zakostelsky | KEY_DEF | 602 | 639 | +37 | +6.15% |  |
| 726 | player | Ned Bowman | ned-bowman | GEN_FWD | 406 | 431 | +25 | +6.16% |  |
| 727 | player | Mitchell Edwards | mitchell-edwards | RUC | 1539 | 1634 | +95 | +6.17% | RUC |
| 728 | player | Wade Derksen | wade-derksen | KEY_DEF | 81 | 86 | +5 | +6.17% |  |
| 729 | player | Wil Powell | wil-powell | GEN_DEF | 955 | 1014 | +59 | +6.18% |  |
| 730 | player | Blake Acres | blake-acres | MID | 97 | 103 | +6 | +6.19% |  |
| 731 | player | Ned Moyle | ned-moyle | RUC | 1598 | 1697 | +99 | +6.20% | RUC |
| 732 | player | Elijah Hollands | elijah-hollands | GEN_FWD | 913 | 970 | +57 | +6.24% |  |
| 733 | player | Noah Chamberlain | noah-chamberlain | GEN_FWD | 160 | 170 | +10 | +6.25% |  |
| 734 | player | Joseph Fonti | joseph-fonti | GEN_DEF | 703 | 747 | +44 | +6.26% |  |
| 735 | player | Angus Hastie | angus-hastie | GEN_DEF | 287 | 305 | +18 | +6.27% |  |
| 736 | player | Mitchell Marsh | mitchell-marsh | KEY_FWD | 669 | 711 | +42 | +6.28% |  |
| 737 | player | Tew Jiath | tew-jiath | GEN_DEF | 223 | 237 | +14 | +6.28% |  |
| 738 | player | Harris Andrews | harris-andrews | KEY_DEF | 1782 | 1894 | +112 | +6.29% |  |
| 739 | player | Jevan Phillipou | jevan-phillipou | GEN_FWD | 509 | 541 | +32 | +6.29% |  |
| 740 | player | Zane Peucker | zane-peucker | GEN_FWD | 554 | 589 | +35 | +6.32% |  |
| 741 | player | Thomas Matthews | thomas-matthews | GEN_FWD | 565 | 601 | +36 | +6.37% |  |
| 742 | player | William McCabe | william-mccabe | KEY_FWD | 533 | 567 | +34 | +6.38% |  |
| 743 | player | Jake Melksham | jake-melksham | KEY_FWD | 47 | 50 | +3 | +6.38% |  |
| 744 | player | Oscar Ryan | oscar-ryan | GEN_DEF | 266 | 283 | +17 | +6.39% |  |
| 745 | player | Jai Saxena | jai-saxena | GEN_FWD | 234 | 249 | +15 | +6.41% |  |
| 746 | player | Ryda Luke | ryda-luke | GEN_FWD | 234 | 249 | +15 | +6.41% |  |
| 747 | player | Toby Whan | toby-whan | GEN_FWD | 234 | 249 | +15 | +6.41% |  |
| 748 | player | James O'Donnell | james-o-donnell | KEY_DEF | 390 | 415 | +25 | +6.41% |  |
| 749 | player | Kalani White | kalani-white | KEY_FWD | 280 | 298 | +18 | +6.43% |  |
| 750 | player | Billy Wilson | billy-wilson | GEN_DEF | 264 | 281 | +17 | +6.44% |  |
| 751 | player | Dougal Howard | dougal-howard | KEY_DEF | 93 | 99 | +6 | +6.45% |  |
| 752 | player | Thomas Burton | thomas-burton | GEN_FWD | 340 | 362 | +22 | +6.47% |  |
| 753 | player | Ricky Mentha | ricky-mentha | GEN_FWD | 139 | 148 | +9 | +6.47% |  |
| 754 | player | Benny Barrett | benny-barrett | GEN_FWD | 139 | 148 | +9 | +6.47% |  |
| 755 | player | Avery Thomas | avery-thomas | GEN_DEF | 509 | 542 | +33 | +6.48% |  |
| 756 | player | Aidan Schubert | aidan-schubert | KEY_FWD | 663 | 706 | +43 | +6.49% |  |
| 757 | player | Cooper Simpson | cooper-simpson | GEN_DEF | 231 | 246 | +15 | +6.49% |  |
| 758 | player | Blake Howes | blake-howes | GEN_DEF | 308 | 328 | +20 | +6.49% |  |
| 759 | player | Jake Stringer | jake-stringer | GEN_FWD | 138 | 147 | +9 | +6.52% |  |
| 760 | player | Josh Rachele | josh-rachele | GEN_FWD | 1793 | 1910 | +117 | +6.53% |  |
| 761 | player | Jack Ison | jack-ison | GEN_FWD | 489 | 521 | +32 | +6.54% |  |
| 762 | player | Massimo D'Ambrosio | massimo-d-ambrosio | MID | 1739 | 1853 | +114 | +6.56% |  |
| 763 | player | Liam Hetherton | liam-hetherton | KEY_FWD | 213 | 227 | +14 | +6.57% |  |
| 764 | player | Reef McInnes | reef-mcinnes | KEY_DEF | 76 | 81 | +5 | +6.58% |  |
| 765 | player | Billy Dowling | billy-dowling | GEN_FWD | 121 | 129 | +8 | +6.61% |  |
| 766 | player | Matt Whitlock | matt-whitlock | KEY_FWD | 422 | 450 | +28 | +6.64% |  |
| 767 | player | Zac McCarthy | zac-mccarthy | KEY_FWD | 360 | 384 | +24 | +6.67% |  |
| 768 | player | Jakob Ryan | jakob-ryan | GEN_DEF | 255 | 272 | +17 | +6.67% |  |
| 769 | player | Jamie Elliott | jamie-elliott | GEN_FWD | 30 | 32 | +2 | +6.67% |  |
| 770 | player | Ben Long | ben-long | GEN_FWD | 30 | 32 | +2 | +6.67% |  |
| 771 | player | Laitham Vandermeer | laitham-vandermeer | GEN_FWD | 30 | 32 | +2 | +6.67% |  |
| 772 | player | Jordan De Goey | jordan-de-goey | GEN_FWD | 1594 | 1701 | +107 | +6.71% |  |
| 773 | player | Asher Eastham | asher-eastham | GEN_FWD | 208 | 222 | +14 | +6.73% |  |
| 774 | player | Jase Burgoyne | jase-burgoyne | GEN_DEF | 1975 | 2108 | +133 | +6.73% |  |
| 775 | player | Henry Smith | henry-smith | KEY_FWD | 147 | 157 | +10 | +6.80% |  |
| 776 | player | Liam Reidy | liam-reidy | RUC | 279 | 298 | +19 | +6.81% | RUC |
| 777 | player | Cooper Duff-Tytler | cooper-duff-tytler | KEY_FWD | 1775 | 1896 | +121 | +6.82% |  |
| 778 | player | Brandon Walker | brandon-walker | GEN_DEF | 88 | 94 | +6 | +6.82% |  |
| 779 | player | Darcy Gardiner | darcy-gardiner | KEY_DEF | 44 | 47 | +3 | +6.82% |  |
| 780 | player | James Peatling | james-peatling | MID | 1208 | 1291 | +83 | +6.87% |  |
| 781 | player | Max Kondogiannis | max-kondogiannis | GEN_DEF | 538 | 575 | +37 | +6.88% |  |
| 782 | player | Luke Lloyd | luke-lloyd | KEY_FWD | 203 | 217 | +14 | +6.90% |  |
| 783 | player | Archie Ludowyke | archie-ludowyke | KEY_FWD | 373 | 399 | +26 | +6.97% |  |
| 784 | player | Tom Cochrane | tom-cochrane | GEN_FWD | 257 | 275 | +18 | +7.00% |  |
| 785 | player | Archie Perkins | archie-perkins | GEN_FWD | 281 | 301 | +20 | +7.12% |  |
| 786 | player | Will Lewis | will-lewis | KEY_FWD | 14 | 15 | +1 | +7.14% |  |
| 787 | player | Liam Ryan | liam-ryan | GEN_FWD | 28 | 30 | +2 | +7.14% |  |
| 788 | player | Tom Cole | tom-cole | GEN_DEF | 28 | 30 | +2 | +7.14% |  |
| 789 | player | Noah Answerth | noah-answerth | GEN_DEF | 28 | 30 | +2 | +7.14% |  |
| 790 | player | Kye Annand | kye-annand | KEY_DEF | 111 | 119 | +8 | +7.21% |  |
| 791 | player | Caleb Lewis | caleb-lewis | KEY_FWD | 111 | 119 | +8 | +7.21% |  |
| 792 | player | Lawson Humphries | lawson-humphries | GEN_DEF | 1764 | 1892 | +128 | +7.26% |  |
| 793 | player | Charlie Nicholls | charlie-nicholls | KEY_FWD | 358 | 384 | +26 | +7.26% |  |
| 794 | player | Harry Armstrong | harry-armstrong | KEY_FWD | 851 | 913 | +62 | +7.29% |  |
| 795 | player | Sam Durham | sam-durham | MID | 1505 | 1615 | +110 | +7.31% |  |
| 796 | player | Corey Wagner | corey-wagner | GEN_DEF | 41 | 44 | +3 | +7.32% |  |
| 797 | player | Kayle Gerreyn | kayle-gerreyn | KEY_FWD | 327 | 351 | +24 | +7.34% |  |
| 798 | player | Noah Roberts-Thomson | noah-roberts-thomson | GEN_FWD | 408 | 438 | +30 | +7.35% |  |
| 799 | player | Jai Newcombe | jai-newcombe | MID | 4187 | 4495 | +308 | +7.36% |  |
| 800 | player | Harrison Coe | harrison-coe | RUC | 95 | 102 | +7 | +7.37% | RUC |
| 801 | player | Max Hall | max-hall | GEN_FWD | 1844 | 1980 | +136 | +7.38% |  |
| 802 | player | Jy Farrar | jy-farrar | KEY_FWD | 27 | 29 | +2 | +7.41% |  |
| 803 | player | John Noble | john-noble | GEN_DEF | 2497 | 2683 | +186 | +7.45% |  |
| 804 | player | Xavier O'Halloran | xavier-o-halloran | GEN_FWD | 40 | 43 | +3 | +7.50% |  |
| 805 | player | Maurice Rioli | maurice-rioli-1 | GEN_FWD | 79 | 85 | +6 | +7.59% |  |
| 806 | player | Tom McCarthy | tom-mccarthy | GEN_DEF | 1523 | 1639 | +116 | +7.62% |  |
| 807 | player | Arthur Jones | arthur-jones | GEN_FWD | 236 | 254 | +18 | +7.63% |  |
| 808 | player | Jacob Konstanty | jacob-konstanty | GEN_FWD | 353 | 380 | +27 | +7.65% |  |
| 809 | player | Talor Byrne | talor-byrne | GEN_FWD | 494 | 532 | +38 | +7.69% |  |
| 810 | player | Flynn Perez | flynn-perez | GEN_DEF | 13 | 14 | +1 | +7.69% |  |
| 811 | player | Brandon Starcevich | brandon-starcevich | GEN_DEF | 39 | 42 | +3 | +7.69% |  |
| 812 | player | Brady Hough | brady-hough | GEN_DEF | 357 | 385 | +28 | +7.84% |  |
| 813 | player | Liam Puncher | liam-puncher | KEY_DEF | 89 | 96 | +7 | +7.87% |  |
| 814 | player | Ben King | ben-king | KEY_FWD | 364 | 393 | +29 | +7.97% |  |
| 815 | player | Esava Ratugolea | esava-ratugolea | KEY_DEF | 87 | 94 | +7 | +8.05% |  |
| 816 | player | Connor Idun | connor-idun | GEN_DEF | 1962 | 2120 | +158 | +8.05% |  |
| 817 | player | Jack Dalton | jack-dalton | GEN_FWD | 539 | 583 | +44 | +8.16% |  |
| 818 | player | Michael Frederick | michael-frederick | GEN_FWD | 98 | 106 | +8 | +8.16% |  |
| 819 | player | Josh Goater | josh-goater | GEN_DEF | 97 | 105 | +8 | +8.25% |  |
| 820 | player | Lukas Cooke | lukas-cooke | KEY_DEF | 96 | 104 | +8 | +8.33% |  |
| 821 | player | Conor McKenna | conor-mckenna | GEN_FWD | 12 | 13 | +1 | +8.33% |  |
| 822 | player | Hussien El Achkar | hussien-el-achkar | GEN_FWD | 371 | 404 | +33 | +8.89% |  |
| 823 | player | Harry Sharp | harry-sharp | GEN_FWD | 212 | 231 | +19 | +8.96% |  |
| 824 | player | Harvey Johnston | harvey-johnston | GEN_DEF | 254 | 277 | +23 | +9.06% |  |
| 825 | player | Jamie Cripps | jamie-cripps | GEN_FWD | 33 | 36 | +3 | +9.09% |  |
| 826 | player | Jack Carroll | jack-carroll | MID | 175 | 192 | +17 | +9.71% |  |
| 827 | player | Riley Bice | riley-bice | GEN_DEF | 411 | 452 | +41 | +9.98% |  |
| 828 | player | Steely Green | steely-green | GEN_FWD | 256 | 282 | +26 | +10.16% |  |
| 829 | player | Zac Taylor | zac-taylor | GEN_FWD | 359 | 396 | +37 | +10.31% |  |
| 830 | player | Isaiah Dudley | isaiah-dudley | GEN_FWD | 79 | 88 | +9 | +11.39% |  |
| 831 | player | Darragh Joyce | darragh-joyce | KEY_DEF | 8 | 9 | +1 | +12.50% |  |
| 832 | player | Bailey Banfield | bailey-banfield | GEN_DEF | 6 | 7 | +1 | +16.67% |  |
| 833 | player | Nick Driscoll | nick-driscoll | MID | 4 | 5 | +1 | +25.00% |  |
| 834 | player | Louis Emmett | louis-emmett | RUC | 788 | 1177 | +389 | +49.37% | RUC |
| 835 | player | Fred Rodriguez | fred-rodriguez | MID | 2 | 3 | +1 | +50.00% |  |
