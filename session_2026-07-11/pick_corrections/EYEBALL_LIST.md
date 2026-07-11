# OWNER EYEBALL LIST — pick-corrections + re-denomination candidate — 2026-07-11

OLD = baked v2.7 board (e2c9bc51). NEW = candidate regenerated board. Every player AND every pick asset below.

## ONE-PAGE SUMMARY

- **MEASURED CURRENCY FACTOR = 1.0524** — the global board SCALE ratio (new 4.68336 / baked 4.45000). This is the definitive uniform scalar; owner ruling (f): shipped pick assets = frozen v3.4 x this factor. Matches audit Q4 (1.0524).
- Players: 805. Pick assets: 30.
- Player Δ% distribution: min -0.26% / **median 5.50%** / max 100.00%. The MEDIAN (~currency factor) is the representative per-player shift; the MEAN is right-skewed by low-value floor players whose few-SCAR rises are large in %.
- Non-RUC players **median Δ% +5.52%** (mean +6.93%, skewed). RUC cohort **median Δ% +5.33%** (mean +5.23%). Established RUCs move LESS than the currency (e.g. Max Gawn baked 2413 -> 2483 = +2.90%, i.e. ~-2.3% relative to the +5.24% currency — the RUC cap machinery; FLAGGED per directive).
- Pick assets Δ%: uniform **+5.24%** (= factor-1; pick-vs-pick ratios byte-preserved, uniform scalar).

### Three narrowest guard margins (candidate)

- **G-COHORT y4 (BINDING, class-year-sum vs hard 1.30)**: 1.29 vs 1.30 -> 1.0 pt (band-pool fix narrows it from ~1.2; B1 candidate avg-peak row y4=129 consistent)
- **A10 Curnow decline (frozen suite, bar 0.50)**: 0.55 vs 0.50 -> +0.05 (narrowest PASSING anchor; PROVISIONAL, data-caused)
- **A8 Berry >= 2x Tsatas (frozen suite)**: 2.13x vs 2.00x -> +0.13x
- Gate suite: all green except the owner-ruled expected reds **{A2, A3, A12}** (data-caused, unchanged by this build); B4 board-parity PASS; B3 book-seal PASS (candidate re-seal); B5 raise-only intact (0 lowered).

### Per-position mean Δ% (players)

| position | n | mean Δ% | median Δ% |
|---|---|---|---|
| GEN_DEF | 176 | +6.18% | +5.60% |
| GEN_FWD | 184 | +7.11% | +5.77% |
| KEY_DEF | 92 | +7.76% | +5.46% |
| KEY_FWD | 103 | +6.62% | +5.59% |
| MID | 195 | +7.21% | +5.43% |
| RUC | 55 | +5.23% | +5.33% |

### FLOOR-DIPPERS (G-FLOOR dispensation — players whose value LOWERED)

Count = **1** (owner ruling: ≤5 SCAR dips on the floor anchors ruled not-cratering, dispensation granted). 
Largest absolute dip = **1 SCAR**. ALL ≤5 SCAR ✓

| player | key | pos | old | new | Δabs | Δ% |
|---|---|---|---|---|---|---|
| Alex Dodson | alex-dodson | RUC | 388 | 387 | -1 | -0.26% |

### RUC cohort (flagged — moves less than the currency shift)

| player | key | old | new | Δabs | Δ% |
|---|---|---|---|---|---|
| Alex Dodson | alex-dodson | 388 | 387 | -1 | -0.26% |
| Jacob Molier | jacob-molier | 393 | 393 | +0 | +0.00% |
| Flynn Riley | flynn-riley | 389 | 389 | +0 | +0.00% |
| Caleb May | caleb-may | 389 | 389 | +0 | +0.00% |
| Alex Van Wyk | alex-van-wyk | 389 | 389 | +0 | +0.00% |
| Max Mapley | max-mapley | 389 | 389 | +0 | +0.00% |
| Max Knobel | max-knobel | 402 | 402 | +0 | +0.00% |
| Patrick Carr | patrick-carr | 389 | 389 | +0 | +0.00% |
| Jaime Uhr-Henry | jaime-uhr-henry | 301 | 301 | +0 | +0.00% |
| Joe Pike | joe-pike | 301 | 301 | +0 | +0.00% |
| Vigo Visentini | vigo-visentini | 256 | 256 | +0 | +0.00% |
| Aiden Riddle | aiden-riddle | 301 | 301 | +0 | +0.00% |
| Logan Smith | logan-smith | 372 | 372 | +0 | +0.00% |
| Iliro Smit | iliro-smit | 256 | 256 | +0 | +0.00% |
| Max Heath | max-heath | 141 | 141 | +0 | +0.00% |
| Rhys Stanley | rhys-stanley | 30 | 30 | +0 | +0.00% |
| Toby Conway | toby-conway | 473 | 479 | +6 | +1.27% |
| Oscar Steene | oscar-steene | 251 | 255 | +4 | +1.59% |
| Harry Barnett | harry-barnett | 536 | 545 | +9 | +1.68% |
| Will Green | will-green | 575 | 590 | +15 | +2.61% |
| Nick Bryan | nick-bryan | 802 | 834 | +32 | +3.99% |
| Lachlan Smith | lachlan-smith | 671 | 702 | +31 | +4.62% |
| Tom De Koning | tom-de-koning | 1638 | 1715 | +77 | +4.70% |
| Marc Pittonet | marc-pittonet | 512 | 537 | +25 | +4.88% |
| Brodie Grundy | brodie-grundy | 3770 | 3960 | +190 | +5.04% |
| Luke Jackson | luke-jackson | 7411 | 7799 | +388 | +5.24% |
| Peter Ladhams | peter-ladhams | 456 | 480 | +24 | +5.26% |
| Nick Madden | nick-madden | 1464 | 1542 | +78 | +5.33% |
| Max Gawn | max-gawn | 2413 | 2543 | +130 | +5.39% |
| Sean Darcy | sean-darcy | 945 | 996 | +51 | +5.40% |
| Timothy English | timothy-english | 3187 | 3359 | +172 | +5.40% |
| Toby Nankervis | toby-nankervis | 2001 | 2109 | +108 | +5.40% |
| Samson Ryan | samson-ryan | 608 | 641 | +33 | +5.43% |
| Ned Moyle | ned-moyle | 1598 | 1686 | +88 | +5.51% |
| Darcy Cameron | darcy-cameron | 1446 | 1526 | +80 | +5.53% |
| Bailey J. Williams | bailey-williams-wc | 1672 | 1766 | +94 | +5.62% |
| Kieren Briggs | kieren-briggs | 2109 | 2229 | +120 | +5.69% |
| Matthew Flynn | matthew-flynn | 703 | 743 | +40 | +5.69% |
| Lloyd Meek | lloyd-meek | 896 | 949 | +53 | +5.92% |
| Taylor Goad | taylor-goad | 788 | 835 | +47 | +5.96% |
| Jarrod Witts | jarrod-witts | 384 | 407 | +23 | +5.99% |
| Darcy Fort | darcy-fort | 83 | 88 | +5 | +6.02% |
| Mitchell Edwards | mitchell-edwards | 1539 | 1632 | +93 | +6.04% |
| Lachlan McAndrew | lachlan-mcandrew | 998 | 1059 | +61 | +6.11% |
| Reilly O'Brien | reilly-o-brien | 783 | 831 | +48 | +6.13% |
| Rowan Marshall | rowan-marshall | 612 | 650 | +38 | +6.21% |
| Tristan Xerri | tristan-xerri | 6384 | 6784 | +400 | +6.27% |
| Harrison Coe | harrison-coe | 95 | 101 | +6 | +6.32% |
| Jordon Sweet | jordon-sweet | 2064 | 2195 | +131 | +6.35% |
| Oliver Hayes-Brown | oliver-hayes-brown | 335 | 358 | +23 | +6.87% |
| Sam Draper | sam-draper | 631 | 677 | +46 | +7.29% |
| Ned Reeves | ned-reeves | 374 | 405 | +31 | +8.29% |
| Dante Visentini | dante-visentini | 723 | 821 | +98 | +13.55% |
| Liam Reidy | liam-reidy | 279 | 373 | +94 | +33.69% |
| Louis Emmett | louis-emmett | 788 | 1178 | +390 | +49.49% |

## FULL LIST — every player AND every pick asset, sorted by Δ%

| # | kind | name | key | pos/asset | old | new | Δabs | Δ% | flag |
|---|---|---|---|---|---|---|---|---|---|
| 1 | player | Alex Dodson | alex-dodson | RUC | 388 | 387 | -1 | -0.26% | RUC FLOOR-DIP |
| 2 | player | Jacob Molier | jacob-molier | RUC | 393 | 393 | +0 | +0.00% | RUC |
| 3 | player | Flynn Riley | flynn-riley | RUC | 389 | 389 | +0 | +0.00% | RUC |
| 4 | player | Caleb May | caleb-may | RUC | 389 | 389 | +0 | +0.00% | RUC |
| 5 | player | Alex Van Wyk | alex-van-wyk | RUC | 389 | 389 | +0 | +0.00% | RUC |
| 6 | player | Max Mapley | max-mapley | RUC | 389 | 389 | +0 | +0.00% | RUC |
| 7 | player | Max Knobel | max-knobel | RUC | 402 | 402 | +0 | +0.00% | RUC |
| 8 | player | Patrick Carr | patrick-carr | RUC | 389 | 389 | +0 | +0.00% | RUC |
| 9 | player | Riley Onley | riley-onley | MID | 2 | 2 | +0 | +0.00% |  |
| 10 | player | Jaime Uhr-Henry | jaime-uhr-henry | RUC | 301 | 301 | +0 | +0.00% | RUC |
| 11 | player | Joe Pike | joe-pike | RUC | 301 | 301 | +0 | +0.00% | RUC |
| 12 | player | Vigo Visentini | vigo-visentini | RUC | 256 | 256 | +0 | +0.00% | RUC |
| 13 | player | Aiden Riddle | aiden-riddle | RUC | 301 | 301 | +0 | +0.00% | RUC |
| 14 | player | Logan Smith | logan-smith | RUC | 372 | 372 | +0 | +0.00% | RUC |
| 15 | player | Iliro Smit | iliro-smit | RUC | 256 | 256 | +0 | +0.00% | RUC |
| 16 | player | Zak Evans | zak-evans | MID | 8 | 8 | +0 | +0.00% |  |
| 17 | player | Roan Steele | roan-steele | MID | 15 | 15 | +0 | +0.00% |  |
| 18 | player | Lachie Sullivan | lachie-sullivan | GEN_FWD | 1 | 1 | +0 | +0.00% |  |
| 19 | player | Oisin Mullin | oisin-mullin | GEN_DEF | 12 | 12 | +0 | +0.00% |  |
| 20 | player | Jordan Boyd | jordan-boyd | GEN_DEF | 10 | 10 | +0 | +0.00% |  |
| 21 | player | Lachlan McNeil | lachlan-mcneil | GEN_FWD | 20 | 20 | +0 | +0.00% |  |
| 22 | player | Max Heath | max-heath | RUC | 141 | 141 | +0 | +0.00% | RUC |
| 23 | player | Brody Mihocek | brody-mihocek | KEY_FWD | 12 | 12 | +0 | +0.00% |  |
| 24 | player | Rhys Stanley | rhys-stanley | RUC | 30 | 30 | +0 | +0.00% | RUC |
| 25 | player | Matt Owies | matt-owies | GEN_FWD | 2 | 2 | +0 | +0.00% |  |
| 26 | player | Mason Cox | mason-cox | KEY_FWD | 1 | 1 | +0 | +0.00% |  |
| 27 | player | Harry Cunningham | harry-cunningham | GEN_DEF | 3 | 3 | +0 | +0.00% |  |
| 28 | player | Archer Day-Wicks | archer-day-wicks | GEN_FWD | 422 | 423 | +1 | +0.24% |  |
| 29 | player | Hugh Bond | hugh-bond | GEN_DEF | 225 | 226 | +1 | +0.44% |  |
| 30 | player | Will Hayes | will-hayes-b | GEN_FWD | 320 | 322 | +2 | +0.62% |  |
| 31 | player | Sam Clohesy | sam-clohesy | MID | 237 | 239 | +2 | +0.84% |  |
| 32 | player | Chris Scerri | chris-scerri | GEN_FWD | 356 | 360 | +4 | +1.12% |  |
| 33 | player | Josaia Delana | josaia-delana | GEN_FWD | 237 | 240 | +3 | +1.27% |  |
| 34 | player | Toby Conway | toby-conway | RUC | 473 | 479 | +6 | +1.27% | RUC |
| 35 | player | Oscar Steene | oscar-steene | RUC | 251 | 255 | +4 | +1.59% | RUC |
| 36 | player | Tyrell Dewar | tyrell-dewar | GEN_DEF | 309 | 314 | +5 | +1.62% |  |
| 37 | player | Lewis Hayes | lewis-hayes | KEY_DEF | 358 | 364 | +6 | +1.68% |  |
| 38 | player | Harry Barnett | harry-barnett | RUC | 536 | 545 | +9 | +1.68% | RUC |
| 39 | player | Wil Dawson | wil-dawson | KEY_DEF | 515 | 524 | +9 | +1.75% |  |
| 40 | player | Blake Thredgold | blake-thredgold | KEY_DEF | 538 | 548 | +10 | +1.86% |  |
| 41 | player | Sam Sturt | sam-sturt | GEN_FWD | 52 | 53 | +1 | +1.92% |  |
| 42 | player | Hugh Davies | hugh-davies | KEY_DEF | 299 | 305 | +6 | +2.01% |  |
| 43 | player | Aidan Corr | aidan-corr | KEY_DEF | 49 | 50 | +1 | +2.04% |  |
| 44 | player | James Barrat | james-barrat | KEY_DEF | 414 | 423 | +9 | +2.17% |  |
| 45 | player | Ben McKay | ben-mckay | KEY_DEF | 46 | 47 | +1 | +2.17% |  |
| 46 | player | Noah Mraz | noah-mraz | KEY_DEF | 403 | 412 | +9 | +2.23% |  |
| 47 | player | Jed Adams | jed-adams | KEY_DEF | 266 | 272 | +6 | +2.26% |  |
| 48 | player | Darcy Gardiner | darcy-gardiner | KEY_DEF | 44 | 45 | +1 | +2.27% |  |
| 49 | player | Jack Carroll | jack-carroll | MID | 175 | 179 | +4 | +2.29% |  |
| 50 | player | Josh Dolan | josh-dolan | GEN_FWD | 435 | 445 | +10 | +2.30% |  |
| 51 | player | Ollie Murphy | ollie-murphy | KEY_DEF | 281 | 288 | +7 | +2.49% |  |
| 52 | player | Lachlan Fogarty | lachlan-fogarty | GEN_FWD | 79 | 81 | +2 | +2.53% |  |
| 53 | player | Connor Budarick | connor-budarick | GEN_DEF | 155 | 159 | +4 | +2.58% |  |
| 54 | player | Will Green | will-green | RUC | 575 | 590 | +15 | +2.61% | RUC |
| 55 | player | Reef McInnes | reef-mcinnes | KEY_DEF | 76 | 78 | +2 | +2.63% |  |
| 56 | player | Alex Pearce | alex-pearce | KEY_DEF | 37 | 38 | +1 | +2.70% |  |
| 57 | player | Jake Kolodjashnij | jake-kolodjashnij | KEY_DEF | 36 | 37 | +1 | +2.78% |  |
| 58 | player | James Trezise | james-trezise | GEN_DEF | 179 | 184 | +5 | +2.79% |  |
| 59 | player | Joel Hamling | joel-hamling | KEY_DEF | 35 | 36 | +1 | +2.86% |  |
| 60 | player | Caiden Cleary | caiden-cleary | GEN_FWD | 756 | 778 | +22 | +2.91% |  |
| 61 | player | Patrick Retschko | patrick-retschko | MID | 809 | 833 | +24 | +2.97% |  |
| 62 | player | Archie May | archie-may | KEY_FWD | 399 | 411 | +12 | +3.01% |  |
| 63 | player | Jaxon Prior | jaxon-prior | GEN_DEF | 295 | 304 | +9 | +3.05% |  |
| 64 | player | Max Michalanney | max-michalanney | GEN_DEF | 576 | 594 | +18 | +3.12% |  |
| 65 | player | Mitch Zadow | mitch-zadow | GEN_FWD | 158 | 163 | +5 | +3.16% |  |
| 66 | player | Lance Collard | lance-collard | GEN_FWD | 281 | 290 | +9 | +3.20% |  |
| 67 | player | Ryan Angwin | ryan-angwin | MID | 436 | 450 | +14 | +3.21% |  |
| 68 | player | Jack Whitlock | jack-whitlock | KEY_FWD | 1250 | 1291 | +41 | +3.28% |  |
| 69 | player | Sandy Brock | sandy-brock | KEY_DEF | 363 | 375 | +12 | +3.31% |  |
| 70 | player | Joel Cochran | joel-cochran | KEY_DEF | 362 | 374 | +12 | +3.31% |  |
| 71 | player | Ollie Greeves | ollie-greeves | MID | 422 | 436 | +14 | +3.32% |  |
| 72 | player | Elijah Hewett | elijah-hewett | MID | 894 | 924 | +30 | +3.36% |  |
| 73 | player | Corey Warner | corey-warner | GEN_FWD | 147 | 152 | +5 | +3.40% |  |
| 74 | player | Oliver Henry | oliver-henry | GEN_FWD | 88 | 91 | +3 | +3.41% |  |
| 75 | player | Tom Cole | tom-cole | GEN_DEF | 28 | 29 | +1 | +3.57% |  |
| 76 | player | Edward Allan | edward-allan | MID | 725 | 751 | +26 | +3.59% |  |
| 77 | player | Cooper Bell | cooper-bell | KEY_DEF | 356 | 369 | +13 | +3.65% |  |
| 78 | player | Tom Blamires | tom-blamires | GEN_DEF | 82 | 85 | +3 | +3.66% |  |
| 79 | player | Jacob Konstanty | jacob-konstanty | GEN_FWD | 353 | 366 | +13 | +3.68% |  |
| 80 | player | Lincoln McCarthy | lincoln-mccarthy | GEN_FWD | 27 | 28 | +1 | +3.70% |  |
| 81 | player | Changkuoth Jiath | changkuoth-jiath | GEN_DEF | 27 | 28 | +1 | +3.70% |  |
| 82 | player | Alex Davies | alex-davies | MID | 592 | 614 | +22 | +3.72% |  |
| 83 | player | Connor Idun | connor-idun | GEN_DEF | 1962 | 2035 | +73 | +3.72% |  |
| 84 | player | Oliver Hannaford | oliver-hannaford | GEN_FWD | 423 | 439 | +16 | +3.78% |  |
| 85 | player | Callum Coleman-Jones | callum-coleman-jones | KEY_FWD | 52 | 54 | +2 | +3.85% |  |
| 86 | player | Shai Bolton | shai-bolton | GEN_FWD | 2231 | 2317 | +86 | +3.85% |  |
| 87 | player | Cooper Trembath | cooper-trembath | KEY_FWD | 1509 | 1568 | +59 | +3.91% |  |
| 88 | player | Karl Worner | karl-worner | GEN_DEF | 587 | 610 | +23 | +3.92% |  |
| 89 | player | Nick Vlastuin | nick-vlastuin | GEN_DEF | 102 | 106 | +4 | +3.92% |  |
| 90 | player | Corey Durdin | corey-durdin | GEN_FWD | 51 | 53 | +2 | +3.92% |  |
| 91 | player | Tyler Sonsie | tyler-sonsie | MID | 764 | 794 | +30 | +3.93% |  |
| 92 | player | Nick Bryan | nick-bryan | RUC | 802 | 834 | +32 | +3.99% | RUC |
| 93 | player | Heath Chapman | heath-chapman | GEN_DEF | 623 | 648 | +25 | +4.01% |  |
| 94 | player | Tom Anastasopoulos | thomas-anastasopoulos | GEN_FWD | 299 | 311 | +12 | +4.01% |  |
| 95 | player | Robert Hansen | robert-hansen | GEN_FWD | 174 | 181 | +7 | +4.02% |  |
| 96 | player | Josh Draper | josh-draper | KEY_DEF | 621 | 646 | +25 | +4.03% |  |
| 97 | player | Jayden Nguyen | jayden-nguyen | GEN_DEF | 421 | 438 | +17 | +4.04% |  |
| 98 | player | Matt Hill | matt-hill | GEN_FWD | 147 | 153 | +6 | +4.08% |  |
| 99 | player | Jade Gresham | jade-gresham | GEN_FWD | 49 | 51 | +2 | +4.08% |  |
| 100 | player | Elijah Tsatas | elijah-tsatas | MID | 1185 | 1234 | +49 | +4.14% |  |
| 101 | player | Josh Lai | josh-lai | GEN_DEF | 338 | 352 | +14 | +4.14% |  |
| 102 | player | Ashton Moir | ashton-moir | GEN_FWD | 265 | 276 | +11 | +4.15% |  |
| 103 | player | Noah Long | noah-long | GEN_FWD | 264 | 275 | +11 | +4.17% |  |
| 104 | player | Isaac Cumming | isaac-cumming | GEN_DEF | 48 | 50 | +2 | +4.17% |  |
| 105 | player | Taylor Adams | taylor-adams | GEN_FWD | 72 | 75 | +3 | +4.17% |  |
| 106 | player | Oscar McDonald | oscar-mcdonald | KEY_DEF | 48 | 50 | +2 | +4.17% |  |
| 107 | player | Jed Bews | jed-bews | GEN_DEF | 24 | 25 | +1 | +4.17% |  |
| 108 | player | Rory Lobb | rory-lobb | KEY_DEF | 359 | 374 | +15 | +4.18% |  |
| 109 | player | Touk Miller | touk-miller | MID | 1432 | 1492 | +60 | +4.19% |  |
| 110 | player | Joel Amartey | joel-amartey | KEY_FWD | 143 | 149 | +6 | +4.20% |  |
| 111 | player | Harry Sharp | harry-sharp | GEN_FWD | 212 | 221 | +9 | +4.25% |  |
| 112 | player | Tyson Stengle | tyson-stengle | GEN_FWD | 258 | 269 | +11 | +4.26% |  |
| 113 | player | Archie Perkins | archie-perkins | GEN_FWD | 281 | 293 | +12 | +4.27% |  |
| 114 | player | Jesse Dattoli | jesse-dattoli | GEN_FWD | 468 | 488 | +20 | +4.27% |  |
| 115 | player | Sam Berry | sam-berry | MID | 2520 | 2628 | +108 | +4.29% |  |
| 116 | player | Braeden Campbell | braeden-campbell | GEN_DEF | 210 | 219 | +9 | +4.29% |  |
| 117 | player | Bailey Laurie | bailey-laurie | GEN_FWD | 70 | 73 | +3 | +4.29% |  |
| 118 | player | Cillian Burke | cillian-burke | GEN_DEF | 116 | 121 | +5 | +4.31% |  |
| 119 | player | Matt Duffy | matt-duffy | GEN_DEF | 185 | 193 | +8 | +4.32% |  |
| 120 | player | Campbell Chesser | campbell-chesser | MID | 553 | 577 | +24 | +4.34% |  |
| 121 | player | Lachy Dovaston | lachy-dovaston | GEN_FWD | 897 | 936 | +39 | +4.35% |  |
| 122 | player | Nicholas Holman | nicholas-holman | GEN_FWD | 23 | 24 | +1 | +4.35% |  |
| 123 | player | Will Graham | will-graham | GEN_FWD | 1145 | 1195 | +50 | +4.37% |  |
| 124 | player | Bo Allan | bo-allan | GEN_DEF | 1190 | 1242 | +52 | +4.37% |  |
| 125 | player | Jai Murray | jai-murray | MID | 1154 | 1205 | +51 | +4.42% |  |
| 126 | player | Lachlan Sholl | lachlan-sholl | MID | 225 | 235 | +10 | +4.44% |  |
| 127 | player | Jobe Shanahan | jobe-shanahan | KEY_FWD | 1550 | 1619 | +69 | +4.45% |  |
| 128 | player | Sam Taylor | sam-taylor | KEY_DEF | 1774 | 1853 | +79 | +4.45% |  |
| 129 | player | Patrick Snell | patrick-snell | KEY_DEF | 246 | 257 | +11 | +4.47% |  |
| 130 | player | Deven Robertson | deven-robertson | MID | 290 | 303 | +13 | +4.48% |  |
| 131 | player | Ben Miller | ben-miller | KEY_DEF | 1177 | 1230 | +53 | +4.50% |  |
| 132 | player | Zak Johnson | zak-johnson | GEN_DEF | 532 | 556 | +24 | +4.51% |  |
| 133 | player | Jordan Croft | jordan-croft | KEY_FWD | 1039 | 1086 | +47 | +4.52% |  |
| 134 | player | Riley Thilthorpe | riley-thilthorpe | KEY_FWD | 3641 | 3806 | +165 | +4.53% |  |
| 135 | player | Isaac Keeler | isaac-keeler | KEY_FWD | 419 | 438 | +19 | +4.53% |  |
| 136 | player | Keidean Coleman | keidean-coleman | GEN_DEF | 617 | 645 | +28 | +4.54% |  |
| 137 | player | Sam Wicks | sam-wicks | GEN_DEF | 22 | 23 | +1 | +4.55% |  |
| 138 | player | Hugh Boxshall | hugh-boxshall | MID | 921 | 963 | +42 | +4.56% |  |
| 139 | player | Thomas Liberatore | thomas-liberatore | MID | 1883 | 1969 | +86 | +4.57% |  |
| 140 | player | Mattaes Phillipou | mattaes-phillipou | MID | 1050 | 1098 | +48 | +4.57% |  |
| 141 | player | Patrick Lipinski | patrick-lipinski | GEN_FWD | 524 | 548 | +24 | +4.58% |  |
| 142 | player | Cameron Nairn | cameron-nairn | GEN_FWD | 764 | 799 | +35 | +4.58% |  |
| 143 | player | Tom Brown | tom-brown | GEN_DEF | 502 | 525 | +23 | +4.58% |  |
| 144 | player | Jack Payne | jack-payne | KEY_DEF | 218 | 228 | +10 | +4.59% |  |
| 145 | player | Bayley Fritsch | bayley-fritsch | GEN_FWD | 196 | 205 | +9 | +4.59% |  |
| 146 | player | Esava Ratugolea | esava-ratugolea | KEY_DEF | 87 | 91 | +4 | +4.60% |  |
| 147 | player | Jack Scrimshaw | jack-scrimshaw | GEN_DEF | 87 | 91 | +4 | +4.60% |  |
| 148 | player | Sam Darcy | sam-darcy | KEY_FWD | 3825 | 4001 | +176 | +4.60% |  |
| 149 | player | Lachlan Cowan | lachlan-cowan | GEN_DEF | 630 | 659 | +29 | +4.60% |  |
| 150 | player | Archer Reid | archer-reid | KEY_FWD | 1064 | 1113 | +49 | +4.61% |  |
| 151 | player | Kane McAuliffe | kane-mcauliffe | MID | 1235 | 1292 | +57 | +4.62% |  |
| 152 | player | Lachlan Smith | lachlan-smith | RUC | 671 | 702 | +31 | +4.62% | RUC |
| 153 | player | Jack Lukosius | jack-lukosius | KEY_FWD | 1447 | 1514 | +67 | +4.63% |  |
| 154 | player | Daniel Turner | daniel-turner | KEY_DEF | 1592 | 1666 | +74 | +4.65% |  |
| 155 | player | Ryan Maric | ryan-maric | MID | 1204 | 1260 | +56 | +4.65% |  |
| 156 | player | Charlie Banfield | charlie-banfield | MID | 773 | 809 | +36 | +4.66% |  |
| 157 | player | Max King | max-king-stk | KEY_FWD | 365 | 382 | +17 | +4.66% |  |
| 158 | player | Daniel McStay | daniel-mcstay | KEY_FWD | 64 | 67 | +3 | +4.69% |  |
| 159 | player | Joe Berry | joe-berry | GEN_FWD | 1278 | 1338 | +60 | +4.69% |  |
| 160 | player | Christian Moraes | christian-moraes | MID | 979 | 1025 | +46 | +4.70% |  |
| 161 | player | Tom De Koning | tom-de-koning | RUC | 1638 | 1715 | +77 | +4.70% | RUC |
| 162 | player | Elijah Hollands | elijah-hollands | GEN_FWD | 913 | 956 | +43 | +4.71% |  |
| 163 | player | Willem Duursma | willem-duursma | MID | 4225 | 4424 | +199 | +4.71% |  |
| 164 | player | Hamish Davis | hamish-davis | MID | 933 | 977 | +44 | +4.72% |  |
| 165 | player | Mitchito Owens | mitchito-owens | KEY_FWD | 2205 | 2309 | +104 | +4.72% |  |
| 166 | player | James Peatling | james-peatling | MID | 1208 | 1265 | +57 | +4.72% |  |
| 167 | player | Nick Watson | nick-watson | GEN_FWD | 3539 | 3706 | +167 | +4.72% |  |
| 168 | player | Sam Allen | sam-allen | MID | 784 | 821 | +37 | +4.72% |  |
| 169 | player | John Noble | john-noble | GEN_DEF | 2497 | 2615 | +118 | +4.73% |  |
| 170 | player | Sam Lalor | sam-lalor | MID | 3400 | 3561 | +161 | +4.74% |  |
| 171 | player | Jaspa Fletcher | jaspa-fletcher | GEN_DEF | 1916 | 2007 | +91 | +4.75% |  |
| 172 | player | Jake Lloyd | jake-lloyd | GEN_DEF | 42 | 44 | +2 | +4.76% |  |
| 173 | player | Cody Angove | cody-angove | MID | 608 | 637 | +29 | +4.77% |  |
| 174 | player | Logan Morris | logan-morris | KEY_FWD | 3018 | 3162 | +144 | +4.77% |  |
| 175 | player | Harry DeMattia | harry-demattia | MID | 460 | 482 | +22 | +4.78% |  |
| 176 | player | Jack Gunston | jack-gunston | KEY_FWD | 1145 | 1200 | +55 | +4.80% |  |
| 177 | player | Malakai Champion | malakai-champion | GEN_FWD | 333 | 349 | +16 | +4.80% |  |
| 178 | player | Jedd Busslinger | jedd-busslinger | KEY_DEF | 728 | 763 | +35 | +4.81% |  |
| 179 | player | Beau McCreery | beau-mccreery | GEN_FWD | 208 | 218 | +10 | +4.81% |  |
| 180 | player | Finlay Macrae | finlay-macrae | MID | 104 | 109 | +5 | +4.81% |  |
| 181 | player | Sam Banks | sam-banks | GEN_DEF | 915 | 959 | +44 | +4.81% |  |
| 182 | player | Zach Reid | zach-reid | KEY_DEF | 1640 | 1719 | +79 | +4.82% |  |
| 183 | player | Nathan O'Driscoll | nathan-o-driscoll | MID | 934 | 979 | +45 | +4.82% |  |
| 184 | player | Nate Caddy | nate-caddy | KEY_FWD | 1678 | 1759 | +81 | +4.83% |  |
| 185 | player | Thomas Sims | thomas-sims | KEY_FWD | 1056 | 1107 | +51 | +4.83% |  |
| 186 | player | Matthew Kennedy | matthew-kennedy-1 | MID | 600 | 629 | +29 | +4.83% |  |
| 187 | player | Jacob Weitering | jacob-weitering | KEY_DEF | 1282 | 1344 | +62 | +4.84% |  |
| 188 | player | Bruce Reville | bruce-reville | MID | 62 | 65 | +3 | +4.84% |  |
| 189 | player | Harley Reid | harley-reid | MID | 3549 | 3721 | +172 | +4.85% |  |
| 190 | player | Mitch Georgiades | mitch-georgiades | KEY_FWD | 1278 | 1340 | +62 | +4.85% |  |
| 191 | player | Brent Daniels | brent-daniels | GEN_FWD | 1315 | 1379 | +64 | +4.87% |  |
| 192 | player | Alix Tauru | alix-tauru | KEY_DEF | 1642 | 1722 | +80 | +4.87% |  |
| 193 | player | Tim Membrey | tim-membrey | KEY_FWD | 41 | 43 | +2 | +4.88% |  |
| 194 | player | James Jordon | james-jordon | MID | 41 | 43 | +2 | +4.88% |  |
| 195 | player | Marc Pittonet | marc-pittonet | RUC | 512 | 537 | +25 | +4.88% | RUC |
| 196 | player | Harry Sheezel | harry-sheezel | MID | 7734 | 8112 | +378 | +4.89% |  |
| 197 | player | Clay Hall | clay-hall | MID | 592 | 621 | +29 | +4.90% |  |
| 198 | player | Ryan Lester | ryan-lester | KEY_DEF | 939 | 985 | +46 | +4.90% |  |
| 199 | player | Shannon Neale | shannon-neale | KEY_FWD | 2327 | 2441 | +114 | +4.90% |  |
| 200 | player | Eric Hipwood | eric-hipwood | KEY_FWD | 102 | 107 | +5 | +4.90% |  |
| 201 | player | Hayden McLean | hayden-mclean | KEY_FWD | 631 | 662 | +31 | +4.91% |  |
| 202 | player | Elliott Himmelberg | elliot-himmelberg | KEY_FWD | 122 | 128 | +6 | +4.92% |  |
| 203 | player | Jai Newcombe | jai-newcombe | MID | 4187 | 4393 | +206 | +4.92% |  |
| 204 | player | Archie Roberts | archie-roberts | GEN_DEF | 4327 | 4540 | +213 | +4.92% |  |
| 205 | player | Logan McDonald | logan-mcdonald | KEY_FWD | 852 | 894 | +42 | +4.93% |  |
| 206 | player | Harley Barker | harley-barker | MID | 710 | 745 | +35 | +4.93% |  |
| 207 | player | Noah Balta | noah-balta | KEY_FWD | 426 | 447 | +21 | +4.93% |  |
| 208 | player | Hugh McCluggage | hugh-mccluggage | MID | 1643 | 1724 | +81 | +4.93% |  |
| 209 | player | Lawson Humphries | lawson-humphries | GEN_DEF | 1764 | 1851 | +87 | +4.93% |  |
| 210 | player | Tyan Prindable | tyan-prindable | MID | 709 | 744 | +35 | +4.94% |  |
| 211 | player | Josh Worrell | josh-worrell | GEN_DEF | 3016 | 3165 | +149 | +4.94% |  |
| 212 | player | Logan Evans | logan-evans | GEN_DEF | 1194 | 1253 | +59 | +4.94% |  |
| 213 | player | Sam Butler | sam-butler-1 | GEN_FWD | 101 | 106 | +5 | +4.95% |  |
| 214 | player | Reuben Ginbey | reuben-ginbey | KEY_DEF | 2847 | 2988 | +141 | +4.95% |  |
| 215 | player | Henry Hustwaite | henry-hustwaite | MID | 343 | 360 | +17 | +4.96% |  |
| 216 | player | Tylah Williams | tylah-williams | GEN_FWD | 464 | 487 | +23 | +4.96% |  |
| 217 | player | Miles Bergman | miles-bergman | GEN_DEF | 664 | 697 | +33 | +4.97% |  |
| 218 | player | Tom Sparrow | tom-sparrow | MID | 482 | 506 | +24 | +4.98% |  |
| 219 | player | Bailey Williams | bailey-williams-wb | GEN_DEF | 582 | 611 | +29 | +4.98% |  |
| 220 | player | Sam Durham | sam-durham | MID | 1505 | 1580 | +75 | +4.98% |  |
| 221 | player | Tom McCarthy | tom-mccarthy | GEN_DEF | 1523 | 1599 | +76 | +4.99% |  |
| 222 | player | Justin McInerney | justin-mcinerney | MID | 1460 | 1533 | +73 | +5.00% |  |
| 223 | player | Jacob Van Rooyen | jacob-van-rooyen | KEY_FWD | 1040 | 1092 | +52 | +5.00% |  |
| 224 | player | Jack Higgins | jack-higgins | GEN_FWD | 200 | 210 | +10 | +5.00% |  |
| 225 | player | Jackson Archer | jackson-archer | GEN_DEF | 80 | 84 | +4 | +5.00% |  |
| 226 | player | Xavier O'Halloran | xavier-o-halloran | GEN_FWD | 40 | 42 | +2 | +5.00% |  |
| 227 | player | Ty Gallop | ty-gallop | KEY_FWD | 1119 | 1175 | +56 | +5.00% |  |
| 228 | player | Cooper Duff-Tytler | cooper-duff-tytler | KEY_FWD | 1775 | 1864 | +89 | +5.01% |  |
| 229 | player | Luke Parker | luke-parker | GEN_DEF | 1415 | 1486 | +71 | +5.02% |  |
| 230 | player | Josh Rachele | josh-rachele | GEN_FWD | 1793 | 1883 | +90 | +5.02% |  |
| 231 | player | Jack Darling | jack-darling | KEY_FWD | 378 | 397 | +19 | +5.03% |  |
| 232 | player | Calsher Dear | calsher-dear | KEY_FWD | 1054 | 1107 | +53 | +5.03% |  |
| 233 | player | Brodie Kemp | brodie-kemp | KEY_FWD | 814 | 855 | +41 | +5.04% |  |
| 234 | player | Brodie Grundy | brodie-grundy | RUC | 3770 | 3960 | +190 | +5.04% | RUC |
| 235 | player | Koby Evans | koby-evans | GEN_FWD | 475 | 499 | +24 | +5.05% |  |
| 236 | player | Joshua Weddle | joshua-weddle | GEN_DEF | 1543 | 1621 | +78 | +5.06% |  |
| 237 | player | Bailey Humphrey | bailey-humphrey | GEN_FWD | 1422 | 1494 | +72 | +5.06% |  |
| 238 | player | Eamonn Armstrong | eamonn-armstrong | GEN_DEF | 158 | 166 | +8 | +5.06% |  |
| 239 | player | Liam Duggan | liam-duggan | GEN_DEF | 395 | 415 | +20 | +5.06% |  |
| 240 | player | Nick Haynes | nick-haynes | GEN_DEF | 79 | 83 | +4 | +5.06% |  |
| 241 | player | Ryley Sanders | ryley-sanders | MID | 3930 | 4129 | +199 | +5.06% |  |
| 242 | player | Jake Riccardi | jake-riccardi | KEY_FWD | 296 | 311 | +15 | +5.07% |  |
| 243 | player | Luke Trainor | luke-trainor | KEY_DEF | 1420 | 1492 | +72 | +5.07% |  |
| 244 | player | Judd McVee | judd-mcvee | GEN_DEF | 276 | 290 | +14 | +5.07% |  |
| 245 | player | Beau Addinsall | beau-addinsall | MID | 1064 | 1118 | +54 | +5.08% |  |
| 246 | player | Jason Horne-Francis | jason-horne-francis | MID | 3802 | 3995 | +193 | +5.08% |  |
| 247 | player | Oliver Hollands | oliver-hollands | GEN_DEF | 1457 | 1531 | +74 | +5.08% |  |
| 248 | player | Sam Walsh | sam-walsh | MID | 2756 | 2896 | +140 | +5.08% |  |
| 249 | player | Mykelti Lefau | mykelti-lefau | KEY_FWD | 59 | 62 | +3 | +5.08% |  |
| 250 | player | Lewis Young | lewis-young | KEY_DEF | 177 | 186 | +9 | +5.08% |  |
| 251 | player | Mason Wood | mason-wood | GEN_FWD | 157 | 165 | +8 | +5.10% |  |
| 252 | player | Maxwell King | max-king-syd | GEN_FWD | 255 | 268 | +13 | +5.10% |  |
| 253 | player | Darcy Byrne-Jones | darcy-byrne-jones | GEN_DEF | 255 | 268 | +13 | +5.10% |  |
| 254 | player | Max Holmes | max-holmes | MID | 5959 | 6263 | +304 | +5.10% |  |
| 255 | player | Hunter Holmes | hunter-holmes | MID | 686 | 721 | +35 | +5.10% |  |
| 256 | player | Michael Frederick | michael-frederick | GEN_FWD | 98 | 103 | +5 | +5.10% |  |
| 257 | player | Adam Sweid | adam-sweid | GEN_FWD | 626 | 658 | +32 | +5.11% |  |
| 258 | player | Sam Powell-Pepper | sam-powell-pepper | GEN_FWD | 313 | 329 | +16 | +5.11% |  |
| 259 | player | Lachlan Gulbin | lachlan-gulbin | GEN_FWD | 332 | 349 | +17 | +5.12% |  |
| 260 | player | Tom Doedee | tom-doedee | GEN_DEF | 410 | 431 | +21 | +5.12% |  |
| 261 | player | Ethan Read | ethan-read | KEY_FWD | 1425 | 1498 | +73 | +5.12% |  |
| 262 | player | Jordan Clark | jordan-clark | GEN_DEF | 3142 | 3303 | +161 | +5.12% |  |
| 263 | player | Lachlan Weller | lachlan-weller | MID | 78 | 82 | +4 | +5.13% |  |
| 264 | player | Finn Callaghan | finn-callaghan | MID | 5183 | 5449 | +266 | +5.13% |  |
| 265 | player | Matt Rowell | matt-rowell | MID | 3984 | 4189 | +205 | +5.15% |  |
| 266 | player | Jonty Faull | jonty-faull | KEY_FWD | 1166 | 1226 | +60 | +5.15% |  |
| 267 | player | Griffin Logue | griffin-logue | KEY_DEF | 136 | 143 | +7 | +5.15% |  |
| 268 | player | Murphy Reid | murphy-reid | GEN_FWD | 3749 | 3942 | +193 | +5.15% |  |
| 269 | player | Aliir Aliir | aliir-aliir | KEY_DEF | 1009 | 1061 | +52 | +5.15% |  |
| 270 | player | Jay Polkinghorne | jay-polkinghorne | GEN_FWD | 252 | 265 | +13 | +5.16% |  |
| 271 | player | Xavier Taylor | xavier-taylor | GEN_DEF | 814 | 856 | +42 | +5.16% |  |
| 272 | player | Brayden George | brayden-george | GEN_FWD | 310 | 326 | +16 | +5.16% |  |
| 273 | player | Ned Bowman | ned-bowman | GEN_FWD | 406 | 427 | +21 | +5.17% |  |
| 274 | player | Zac Fisher | zac-fisher | GEN_FWD | 174 | 183 | +9 | +5.17% |  |
| 275 | player | Rhyan Mansell | rhyan-mansell | GEN_FWD | 58 | 61 | +3 | +5.17% |  |
| 276 | player | Hayden Young | hayden-young | MID | 2625 | 2761 | +136 | +5.18% |  |
| 277 | player | Scott Pendlebury | scott-pendlebury | MID | 579 | 609 | +30 | +5.18% |  |
| 278 | player | Jake Bowey | jake-bowey | GEN_DEF | 2932 | 3084 | +152 | +5.18% |  |
| 279 | player | Harvey Langford | harvey-langford | MID | 2469 | 2597 | +128 | +5.18% |  |
| 280 | player | Tom Green | tom-green | MID | 4165 | 4381 | +216 | +5.19% |  |
| 281 | pick | Pick 23 | pick-23 | PICK ASSET | 617 | 649 | +32 | +5.19% |  |
| 282 | player | Toby Greene | toby-greene | GEN_FWD | 829 | 872 | +43 | +5.19% |  |
| 283 | player | Shadeau Brain | shadeau-brain | GEN_DEF | 77 | 81 | +4 | +5.19% |  |
| 284 | pick | Pick 16 | pick-16 | PICK ASSET | 1001 | 1053 | +52 | +5.19% |  |
| 285 | player | Tom Barrass | tom-barrass | KEY_DEF | 481 | 506 | +25 | +5.20% |  |
| 286 | player | Tanner Bruhn | tanner-bruhn | MID | 1000 | 1052 | +52 | +5.20% |  |
| 287 | player | Ed Richards | ed-richards | MID | 2922 | 3074 | +152 | +5.20% |  |
| 288 | pick | Pick 24 | pick-24 | PICK ASSET | 615 | 647 | +32 | +5.20% |  |
| 289 | player | Cooper Hynes | cooper-hynes | MID | 1249 | 1314 | +65 | +5.20% |  |
| 290 | player | Bradley Hill | bradley-hill | GEN_FWD | 807 | 849 | +42 | +5.20% |  |
| 291 | player | Harry Rowston | harry-rowston | MID | 903 | 950 | +47 | +5.20% |  |
| 292 | player | Andrew McGrath | andrew-mcgrath | GEN_DEF | 1095 | 1152 | +57 | +5.21% |  |
| 293 | player | Caleb Daniel | caleb-daniel | GEN_DEF | 1229 | 1293 | +64 | +5.21% |  |
| 294 | player | Aaron Naughton | aaron-naughton | KEY_FWD | 1651 | 1737 | +86 | +5.21% |  |
| 295 | player | Patrick Cripps | patrick-cripps | MID | 1382 | 1454 | +72 | +5.21% |  |
| 296 | player | Ben Ainsworth | ben-ainsworth | GEN_FWD | 307 | 323 | +16 | +5.21% |  |
| 297 | pick | Pick 25 | pick-25 | PICK ASSET | 614 | 646 | +32 | +5.21% |  |
| 298 | player | Izak Rankine | izak-rankine | GEN_FWD | 2628 | 2765 | +137 | +5.21% |  |
| 299 | pick | Pick 11 | pick-11 | PICK ASSET | 1381 | 1453 | +72 | +5.21% |  |
| 300 | pick | Pick 15 | pick-15 | PICK ASSET | 1074 | 1130 | +56 | +5.21% |  |
| 301 | player | Errol Gulden | errol-gulden | MID | 5715 | 6013 | +298 | +5.21% |  |
| 302 | player | Jase Burgoyne | jase-burgoyne | GEN_DEF | 1975 | 2078 | +103 | +5.22% |  |
| 303 | pick | Pick 8 | pick-8 | PICK ASSET | 1706 | 1795 | +89 | +5.22% |  |
| 304 | player | Taylor Walker | taylor-walker | KEY_FWD | 230 | 242 | +12 | +5.22% |  |
| 305 | player | Harry McKay | harry-mckay | KEY_FWD | 1762 | 1854 | +92 | +5.22% |  |
| 306 | player | Darcy Fogarty | darcy-fogarty | KEY_FWD | 383 | 403 | +20 | +5.22% |  |
| 307 | player | Will Day | will-day | MID | 2949 | 3103 | +154 | +5.22% |  |
| 308 | player | Luke Ryan | luke-ryan | GEN_DEF | 1646 | 1732 | +86 | +5.22% |  |
| 309 | pick | Pick 6 | pick-6 | PICK ASSET | 1875 | 1973 | +98 | +5.23% |  |
| 310 | pick | Pick 4 | pick-4 | PICK ASSET | 2085 | 2194 | +109 | +5.23% |  |
| 311 | pick | Pick 10 | pick-10 | PICK ASSET | 1492 | 1570 | +78 | +5.23% |  |
| 312 | player | Rhylee West | rhylee-west | GEN_FWD | 153 | 161 | +8 | +5.23% |  |
| 313 | pick | Pick 26 | pick-26 | PICK ASSET | 612 | 644 | +32 | +5.23% |  |
| 314 | player | Lachie Whitfield | lachie-whitfield | GEN_DEF | 2180 | 2294 | +114 | +5.23% |  |
| 315 | player | Kyle Langford | kyle-langford | KEY_FWD | 650 | 684 | +34 | +5.23% |  |
| 316 | player | Seth Campbell | seth-campbell | GEN_FWD | 1032 | 1086 | +54 | +5.23% |  |
| 317 | player | Cooper Sharman | cooper-sharman | KEY_FWD | 516 | 543 | +27 | +5.23% |  |
| 318 | pick | Pick 1 | pick-1 | PICK ASSET | 3000 | 3157 | +157 | +5.23% |  |
| 319 | player | Luke Jackson | luke-jackson | RUC | 7411 | 7799 | +388 | +5.24% | RUC |
| 320 | pick | Pick 5 | pick-5 | PICK ASSET | 1967 | 2070 | +103 | +5.24% |  |
| 321 | pick | Pick 7 | pick-7 | PICK ASSET | 1795 | 1889 | +94 | +5.24% |  |
| 322 | pick | Pick 9 | pick-9 | PICK ASSET | 1604 | 1688 | +84 | +5.24% |  |
| 323 | pick | Pick 13 | pick-13 | PICK ASSET | 1203 | 1266 | +63 | +5.24% |  |
| 324 | pick | Pick 27 | pick-27 | PICK ASSET | 611 | 643 | +32 | +5.24% |  |
| 325 | pick | Pick 2 | pick-2 | PICK ASSET | 2501 | 2632 | +131 | +5.24% |  |
| 326 | pick | Pick 18 | pick-18 | PICK ASSET | 859 | 904 | +45 | +5.24% |  |
| 327 | player | Angus Sheldrick | angus-sheldrick | MID | 801 | 843 | +42 | +5.24% |  |
| 328 | player | Xavier Duursma | xavier-duursma | MID | 267 | 281 | +14 | +5.24% |  |
| 329 | pick | Pick 3 | pick-3 | PICK ASSET | 2249 | 2367 | +118 | +5.25% |  |
| 330 | player | Nasiah Wanganeen-Milera | nasiah-wanganeen-milera | MID | 6270 | 6599 | +329 | +5.25% |  |
| 331 | player | Hugo Garcia | hugo-garcia | MID | 2058 | 2166 | +108 | +5.25% |  |
| 332 | player | Callum Mills | callum-mills | GEN_DEF | 1810 | 1905 | +95 | +5.25% |  |
| 333 | player | Sam Marshall | sam-marshall | MID | 1105 | 1163 | +58 | +5.25% |  |
| 334 | player | Christian Petracca | christian-petracca | MID | 2703 | 2845 | +142 | +5.25% |  |
| 335 | pick | Pick 28 | pick-28 | PICK ASSET | 609 | 641 | +32 | +5.25% |  |
| 336 | pick | Pick 21 | pick-21 | PICK ASSET | 685 | 721 | +36 | +5.26% |  |
| 337 | player | Caleb Serong | caleb-serong | MID | 4490 | 4726 | +236 | +5.26% |  |
| 338 | player | Peter Wright | peter-wright | KEY_FWD | 1902 | 2002 | +100 | +5.26% |  |
| 339 | player | Jack Steele | jack-steele | MID | 1597 | 1681 | +84 | +5.26% |  |
| 340 | player | Samuel Grlj | samuel-grlj | MID | 2470 | 2600 | +130 | +5.26% |  |
| 341 | player | Dyson Sharp | dyson-sharp | MID | 1615 | 1700 | +85 | +5.26% |  |
| 342 | player | Saad El-Hawli | saad-el-hawli | GEN_DEF | 19 | 20 | +1 | +5.26% |  |
| 343 | player | Peter Ladhams | peter-ladhams | RUC | 456 | 480 | +24 | +5.26% | RUC |
| 344 | player | Liam Stocker | liam-stocker | GEN_DEF | 38 | 40 | +2 | +5.26% |  |
| 345 | pick | Pick 22 | pick-22 | PICK ASSET | 646 | 680 | +34 | +5.26% |  |
| 346 | pick | Pick 29 | pick-29 | PICK ASSET | 607 | 639 | +32 | +5.27% |  |
| 347 | pick | Pick 14 | pick-14 | PICK ASSET | 1138 | 1198 | +60 | +5.27% |  |
| 348 | player | Jake Lever | jake-lever | KEY_DEF | 550 | 579 | +29 | +5.27% |  |
| 349 | player | Mac Andrew | mac-andrew | KEY_DEF | 3508 | 3693 | +185 | +5.27% |  |
| 350 | player | Zac Bailey | zac-bailey | GEN_FWD | 2389 | 2515 | +126 | +5.27% |  |
| 351 | player | Matt Carroll | matt-carroll | MID | 929 | 978 | +49 | +5.27% |  |
| 352 | pick | Pick 17 | pick-17 | PICK ASSET | 929 | 978 | +49 | +5.27% |  |
| 353 | player | Ned Long | ned-long | MID | 910 | 958 | +48 | +5.27% |  |
| 354 | pick | Pick 12 | pick-12 | PICK ASSET | 1270 | 1337 | +67 | +5.28% |  |
| 355 | player | Luke Nankervis | luke-nankervis | GEN_DEF | 341 | 359 | +18 | +5.28% |  |
| 356 | pick | Pick 30 | pick-30 | PICK ASSET | 606 | 638 | +32 | +5.28% |  |
| 357 | pick | Pick 19 | pick-19 | PICK ASSET | 795 | 837 | +42 | +5.28% |  |
| 358 | player | Jackson Macrae | jackson-macrae | MID | 246 | 259 | +13 | +5.28% |  |
| 359 | player | Darcy Parish | darcy-parish | MID | 1419 | 1494 | +75 | +5.29% |  |
| 360 | player | Harrison Himmelberg | harrison-himmelberg | GEN_DEF | 454 | 478 | +24 | +5.29% |  |
| 361 | player | Jordan Ridley | jordan-ridley | GEN_DEF | 1059 | 1115 | +56 | +5.29% |  |
| 362 | player | Darcy Wilmot | darcy-wilmot | GEN_DEF | 3763 | 3962 | +199 | +5.29% |  |
| 363 | player | Mason Redman | mason-redman | GEN_DEF | 1437 | 1513 | +76 | +5.29% |  |
| 364 | player | Jed Walter | jed-walter | KEY_FWD | 1510 | 1590 | +80 | +5.30% |  |
| 365 | player | Matthew Roberts | matthew-roberts | GEN_DEF | 1679 | 1768 | +89 | +5.30% |  |
| 366 | player | Bailey Smith | bailey-smith | MID | 5282 | 5562 | +280 | +5.30% |  |
| 367 | player | Jack Ross | jack-ross | MID | 1641 | 1728 | +87 | +5.30% |  |
| 368 | player | Jevan Phillipou | jevan-phillipou | GEN_FWD | 509 | 536 | +27 | +5.30% |  |
| 369 | player | Hugo Mikunda | hugo-mikunda | GEN_FWD | 377 | 397 | +20 | +5.31% |  |
| 370 | pick | Pick 20 | pick-20 | PICK ASSET | 735 | 774 | +39 | +5.31% |  |
| 371 | player | Harry O'Farrell | harry-o-farrell | KEY_DEF | 810 | 853 | +43 | +5.31% |  |
| 372 | player | Sam Flanders | sam-flanders | MID | 1714 | 1805 | +91 | +5.31% |  |
| 373 | player | Kysaiah Pickett | kysaiah-pickett | GEN_FWD | 3329 | 3506 | +177 | +5.32% |  |
| 374 | player | Samuel Collins | samuel-collins | KEY_DEF | 940 | 990 | +50 | +5.32% |  |
| 375 | player | Will Brodie | will-brodie | MID | 1034 | 1089 | +55 | +5.32% |  |
| 376 | player | Ryan Byrnes | ryan-byrnes | GEN_DEF | 94 | 99 | +5 | +5.32% |  |
| 377 | player | Shaun Mannagh | shaun-mannagh | GEN_FWD | 526 | 554 | +28 | +5.32% |  |
| 378 | player | Rob Monahan | rob-monahan | GEN_DEF | 169 | 178 | +9 | +5.33% |  |
| 379 | player | Zak Butters | zak-butters | MID | 5745 | 6051 | +306 | +5.33% |  |
| 380 | player | Nick Madden | nick-madden | RUC | 1464 | 1542 | +78 | +5.33% | RUC |
| 381 | player | Tom McDonald | tom-mcdonald | KEY_DEF | 356 | 375 | +19 | +5.34% |  |
| 382 | player | Will Hayward | will-hayward | GEN_FWD | 206 | 217 | +11 | +5.34% |  |
| 383 | player | Brayden Maynard | brayden-maynard | GEN_DEF | 880 | 927 | +47 | +5.34% |  |
| 384 | player | Levi Ashcroft | levi-ashcroft | MID | 3032 | 3194 | +162 | +5.34% |  |
| 385 | player | Joe Richards | joe-richards | GEN_FWD | 842 | 887 | +45 | +5.34% |  |
| 386 | player | Daniel Rioli | daniel-rioli | GEN_DEF | 711 | 749 | +38 | +5.34% |  |
| 387 | player | Josh Battle | josh-battle | KEY_DEF | 2095 | 2207 | +112 | +5.35% |  |
| 388 | player | Jayden Laverde | jayden-laverde | KEY_DEF | 505 | 532 | +27 | +5.35% |  |
| 389 | player | Jarman Impey | jarman-impey | GEN_DEF | 692 | 729 | +37 | +5.35% |  |
| 390 | player | Massimo D'Ambrosio | massimo-d-ambrosio | MID | 1739 | 1832 | +93 | +5.35% |  |
| 391 | player | Oliver Wines | oliver-wines | MID | 486 | 512 | +26 | +5.35% |  |
| 392 | player | Nick Blakey | nick-blakey | GEN_DEF | 3431 | 3615 | +184 | +5.36% |  |
| 393 | player | Kane Farrell | kane-farrell | GEN_DEF | 1435 | 1512 | +77 | +5.37% |  |
| 394 | player | Joshua Kelly | joshua-kelly | MID | 559 | 589 | +30 | +5.37% |  |
| 395 | player | Jye Caldwell | jye-caldwell | MID | 1452 | 1530 | +78 | +5.37% |  |
| 396 | player | Connor Rozee | connor-rozee | MID | 2271 | 2393 | +122 | +5.37% |  |
| 397 | player | Lachlan Bramble | lachlan-bramble | GEN_FWD | 93 | 98 | +5 | +5.38% |  |
| 398 | player | Brayden Cook | brayden-cook | MID | 743 | 783 | +40 | +5.38% |  |
| 399 | player | Max Gawn | max-gawn | RUC | 2413 | 2543 | +130 | +5.39% | RUC |
| 400 | player | Sean Darcy | sean-darcy | RUC | 945 | 996 | +51 | +5.40% | RUC |
| 401 | player | Mabior Chol | mabior-chol | KEY_FWD | 315 | 332 | +17 | +5.40% |  |
| 402 | player | Timothy English | timothy-english | RUC | 3187 | 3359 | +172 | +5.40% | RUC |
| 403 | player | Toby Nankervis | toby-nankervis | RUC | 2001 | 2109 | +108 | +5.40% | RUC |
| 404 | player | Dion Prestia | dion-prestia | MID | 333 | 351 | +18 | +5.41% |  |
| 405 | player | Zane Peucker | zane-peucker | GEN_FWD | 554 | 584 | +30 | +5.42% |  |
| 406 | player | James Worpel | james-worpel | MID | 517 | 545 | +28 | +5.42% |  |
| 407 | player | Charlie Curnow | charlie-curnow | KEY_FWD | 1198 | 1263 | +65 | +5.43% |  |
| 408 | player | Bailey Dale | bailey-dale | GEN_DEF | 1898 | 2001 | +103 | +5.43% |  |
| 409 | player | Samson Ryan | samson-ryan | RUC | 608 | 641 | +33 | +5.43% | RUC |
| 410 | player | Cameron Mackenzie | cameron-mackenzie | MID | 1473 | 1553 | +80 | +5.43% |  |
| 411 | player | Harvey Harrison | harvey-harrison | GEN_FWD | 92 | 97 | +5 | +5.43% |  |
| 412 | player | Jeremy Cameron | jeremy-cameron | KEY_FWD | 1453 | 1532 | +79 | +5.44% |  |
| 413 | player | Neil Erasmus | neil-erasmus | MID | 809 | 853 | +44 | +5.44% |  |
| 414 | player | Harrison Petty | harrison-petty | KEY_DEF | 147 | 155 | +8 | +5.44% |  |
| 415 | player | Brayden Fiorini | brayden-fiorini | MID | 312 | 329 | +17 | +5.45% |  |
| 416 | player | Will Ashcroft | will-ashcroft | MID | 4895 | 5162 | +267 | +5.45% |  |
| 417 | player | Jack Viney | jack-viney | MID | 385 | 406 | +21 | +5.45% |  |
| 418 | player | Connor MacDonald | connor-macdonald | GEN_FWD | 2309 | 2435 | +126 | +5.46% |  |
| 419 | player | Cillian Bourke | cillian-bourke | GEN_DEF | 366 | 386 | +20 | +5.46% |  |
| 420 | player | Willem Drew | willem-drew | MID | 860 | 907 | +47 | +5.47% |  |
| 421 | player | Jack Ough | jack-ough | MID | 402 | 424 | +22 | +5.47% |  |
| 422 | player | Jy Simpkin | jy-simpkin | MID | 603 | 636 | +33 | +5.47% |  |
| 423 | player | Zeke Uwland | zeke-uwland | GEN_DEF | 2119 | 2235 | +116 | +5.47% |  |
| 424 | player | Joel Jeffrey | joel-jeffrey | GEN_DEF | 1644 | 1734 | +90 | +5.47% |  |
| 425 | player | Jordan Dawson | jordan-dawson | MID | 3156 | 3329 | +173 | +5.48% |  |
| 426 | player | Adam Cerra | adam-cerra | MID | 1149 | 1212 | +63 | +5.48% |  |
| 427 | player | Harry Dean | harry-dean | KEY_DEF | 1969 | 2077 | +108 | +5.49% |  |
| 428 | player | Thomas Matthews | thomas-matthews | GEN_FWD | 565 | 596 | +31 | +5.49% |  |
| 429 | player | Christian Salem | christian-salem | GEN_DEF | 583 | 615 | +32 | +5.49% |  |
| 430 | player | James Tunstill | james-tunstill | MID | 91 | 96 | +5 | +5.49% |  |
| 431 | player | James Sicily | james-sicily | GEN_DEF | 1965 | 2073 | +108 | +5.50% |  |
| 432 | player | Wayne Milera | wayne-milera | GEN_DEF | 1692 | 1785 | +93 | +5.50% |  |
| 433 | player | Chad Warner | chad-warner | MID | 2728 | 2878 | +150 | +5.50% |  |
| 434 | player | Harris Andrews | harris-andrews | KEY_DEF | 1782 | 1880 | +98 | +5.50% |  |
| 435 | player | Jarrod Berry | jarrod-berry | MID | 527 | 556 | +29 | +5.50% |  |
| 436 | player | Darcy Wilson | darcy-wilson | GEN_FWD | 2343 | 2472 | +129 | +5.51% |  |
| 437 | player | Ned Moyle | ned-moyle | RUC | 1598 | 1686 | +88 | +5.51% | RUC |
| 438 | player | Riley Hardeman | riley-hardeman | GEN_DEF | 363 | 383 | +20 | +5.51% |  |
| 439 | player | Oliver Florent | oliver-florent | GEN_DEF | 743 | 784 | +41 | +5.52% |  |
| 440 | player | Dayne Zorko | dayne-zorko | GEN_DEF | 1105 | 1166 | +61 | +5.52% |  |
| 441 | player | Jordan De Goey | jordan-de-goey | GEN_FWD | 1594 | 1682 | +88 | +5.52% |  |
| 442 | player | Jhye Clark | jhye-clark | MID | 670 | 707 | +37 | +5.52% |  |
| 443 | player | Darcy Cameron | darcy-cameron | RUC | 1446 | 1526 | +80 | +5.53% | RUC |
| 444 | player | Elliot Yeo | elliot-yeo | MID | 542 | 572 | +30 | +5.54% |  |
| 445 | player | Milan Murdock | milan-murdock | GEN_FWD | 831 | 877 | +46 | +5.54% |  |
| 446 | player | Jack Silvagni | jack-silvagni | KEY_DEF | 614 | 648 | +34 | +5.54% |  |
| 447 | player | Darcy Moore | darcy-moore | KEY_DEF | 198 | 209 | +11 | +5.56% |  |
| 448 | player | Mitchell Knevitt | mitchell-knevitt | MID | 198 | 209 | +11 | +5.56% |  |
| 449 | player | Luke McDonald | luke-mcdonald | GEN_DEF | 54 | 57 | +3 | +5.56% |  |
| 450 | player | Jeremy Sharp | jeremy-sharp | MID | 108 | 114 | +6 | +5.56% |  |
| 451 | player | Sullivan Robey | sullivan-robey | MID | 2141 | 2260 | +119 | +5.56% |  |
| 452 | player | Noah Anderson | noah-anderson | MID | 4528 | 4780 | +252 | +5.57% |  |
| 453 | player | Jack Dalton | jack-dalton | GEN_FWD | 539 | 569 | +30 | +5.57% |  |
| 454 | player | Jake Soligo | jake-soligo | MID | 2079 | 2195 | +116 | +5.58% |  |
| 455 | player | Kade Chandler | kade-chandler | GEN_FWD | 1021 | 1078 | +57 | +5.58% |  |
| 456 | player | Will Setterfield | will-setterfield | MID | 1540 | 1626 | +86 | +5.58% |  |
| 457 | player | Hudson O'Keeffe | hudson-o-keeffe | KEY_FWD | 376 | 397 | +21 | +5.59% |  |
| 458 | player | Oscar Allen | oscar-allen | KEY_FWD | 179 | 189 | +10 | +5.59% |  |
| 459 | player | Marcus Windhager | marcus-windhager | MID | 1557 | 1644 | +87 | +5.59% |  |
| 460 | player | Joel Freijah | joel-freijah | MID | 2182 | 2304 | +122 | +5.59% |  |
| 461 | player | Finn O'Sullivan | finn-o-sullivan | MID | 3451 | 3644 | +193 | +5.59% |  |
| 462 | player | Isaac Heeney | isaac-heeney | MID | 3772 | 3983 | +211 | +5.59% |  |
| 463 | player | Karl Amon | karl-amon | GEN_DEF | 786 | 830 | +44 | +5.60% |  |
| 464 | player | Harry Kyle | harry-kyle | GEN_DEF | 875 | 924 | +49 | +5.60% |  |
| 465 | player | Josh Daicos | josh-daicos | GEN_DEF | 1873 | 1978 | +105 | +5.61% |  |
| 466 | player | Jasper Alger | jasper-alger | GEN_FWD | 321 | 339 | +18 | +5.61% |  |
| 467 | player | Bailey Macdonald | bailey-macdonald | GEN_DEF | 107 | 113 | +6 | +5.61% |  |
| 468 | player | Nick Daicos | nick-daicos | MID | 7626 | 8054 | +428 | +5.61% |  |
| 469 | player | Jeremy Howe | jeremy-howe | GEN_DEF | 285 | 301 | +16 | +5.61% |  |
| 470 | player | Marcus Bontempelli | marcus-bontempelli | MID | 3524 | 3722 | +198 | +5.62% |  |
| 471 | player | Bailey J. Williams | bailey-williams-wc | RUC | 1672 | 1766 | +94 | +5.62% | RUC |
| 472 | player | Sam Cumming | sam-cumming | MID | 2115 | 2234 | +119 | +5.63% |  |
| 473 | player | Dan Houston | dan-houston | GEN_DEF | 1207 | 1275 | +68 | +5.63% |  |
| 474 | player | George Wardlaw | george-wardlaw | MID | 3035 | 3206 | +171 | +5.63% |  |
| 475 | player | Andrew Brayshaw | andrew-brayshaw | MID | 2785 | 2942 | +157 | +5.64% |  |
| 476 | player | Ed Langdon | ed-langdon | GEN_DEF | 567 | 599 | +32 | +5.64% |  |
| 477 | player | Josh Dunkley | josh-dunkley | MID | 903 | 954 | +51 | +5.65% |  |
| 478 | player | Jaeger O'Meara | jaeger-o-meara | MID | 177 | 187 | +10 | +5.65% |  |
| 479 | player | Anthony Caminiti | anthony-caminiti | KEY_FWD | 690 | 729 | +39 | +5.65% |  |
| 480 | player | Lachlan Schultz | lachlan-schultz | GEN_FWD | 619 | 654 | +35 | +5.65% |  |
| 481 | player | Harry Schoenberg | harry-schoenberg | MID | 53 | 56 | +3 | +5.66% |  |
| 482 | player | Trent Rivers | trent-rivers | GEN_DEF | 1713 | 1810 | +97 | +5.66% |  |
| 483 | player | Brandon Zerk-Thatcher | brandon-zerk-thatcher | KEY_DEF | 247 | 261 | +14 | +5.67% |  |
| 484 | player | Colby McKercher | colby-mckercher | MID | 3627 | 3833 | +206 | +5.68% |  |
| 485 | player | Samuel Swadling | samuel-swadling | MID | 616 | 651 | +35 | +5.68% |  |
| 486 | player | Billy Wilson | billy-wilson | GEN_DEF | 264 | 279 | +15 | +5.68% |  |
| 487 | player | Balyn O'Brien | balyn-o-brien | GEN_DEF | 264 | 279 | +15 | +5.68% |  |
| 488 | player | Ben Murphy | ben-murphy | GEN_DEF | 264 | 279 | +15 | +5.68% |  |
| 489 | player | Kobe McDonald | kobe-mcdonald | GEN_DEF | 264 | 279 | +15 | +5.68% |  |
| 490 | player | Indy Cotton | indy-cotton | GEN_DEF | 264 | 279 | +15 | +5.68% |  |
| 491 | player | Harry Perryman | harry-perryman | GEN_DEF | 176 | 186 | +10 | +5.68% |  |
| 492 | player | Blake Hardwick | blake-hardwick | GEN_DEF | 387 | 409 | +22 | +5.68% |  |
| 493 | player | James Leake | james-leake | GEN_DEF | 334 | 353 | +19 | +5.69% |  |
| 494 | player | Kieren Briggs | kieren-briggs | RUC | 2109 | 2229 | +120 | +5.69% | RUC |
| 495 | player | Matthew Flynn | matthew-flynn | RUC | 703 | 743 | +40 | +5.69% | RUC |
| 496 | player | Dylan Moore | dylan-moore | GEN_FWD | 1454 | 1537 | +83 | +5.71% |  |
| 497 | player | Sam De Koning | sam-de-koning | KEY_DEF | 995 | 1052 | +57 | +5.73% |  |
| 498 | player | Jacob Newton | jacob-newton | GEN_FWD | 157 | 166 | +9 | +5.73% |  |
| 499 | player | Paddy Dow | paddy-dow | MID | 157 | 166 | +9 | +5.73% |  |
| 500 | player | Stephen Coniglio | stephen-coniglio | MID | 157 | 166 | +9 | +5.73% |  |
| 501 | player | Alex Neal-Bullen | alex-neal-bullen | GEN_FWD | 488 | 516 | +28 | +5.74% |  |
| 502 | player | Zachary Merrett | zachary-merrett | MID | 2925 | 3093 | +168 | +5.74% |  |
| 503 | player | Tim Kelly | tim-kelly | MID | 921 | 974 | +53 | +5.75% |  |
| 504 | player | Tim Taranto | tim-taranto | MID | 2534 | 2680 | +146 | +5.76% |  |
| 505 | player | Phoenix Gothard | phoenix-gothard | GEN_FWD | 399 | 422 | +23 | +5.76% |  |
| 506 | player | Lachlan Ash | lachlan-ash | GEN_DEF | 4924 | 5208 | +284 | +5.77% |  |
| 507 | player | Todd Marshall | todd-marshall | KEY_FWD | 156 | 165 | +9 | +5.77% |  |
| 508 | player | Gryan Miers | gryan-miers | GEN_FWD | 1505 | 1592 | +87 | +5.78% |  |
| 509 | player | Tom Papley | tom-papley | GEN_FWD | 467 | 494 | +27 | +5.78% |  |
| 510 | player | Billy Dowling | billy-dowling | GEN_FWD | 121 | 128 | +7 | +5.79% |  |
| 511 | player | Taj Hotton | taj-hotton | MID | 1607 | 1700 | +93 | +5.79% |  |
| 512 | player | Will Lorenz | will-lorenz | MID | 397 | 420 | +23 | +5.79% |  |
| 513 | player | Jake Stringer | jake-stringer | GEN_FWD | 138 | 146 | +8 | +5.80% |  |
| 514 | player | Sid Draper | sid-draper | MID | 1448 | 1532 | +84 | +5.80% |  |
| 515 | player | Josh Ward | josh-ward | MID | 1650 | 1746 | +96 | +5.82% |  |
| 516 | player | Nick Larkey | nick-larkey | KEY_FWD | 550 | 582 | +32 | +5.82% |  |
| 517 | player | Daniel Curtin | daniel-curtin | MID | 2148 | 2273 | +125 | +5.82% |  |
| 518 | player | Aaron Cadman | aaron-cadman | KEY_FWD | 2970 | 3143 | +173 | +5.82% |  |
| 519 | player | Tew Jiath | tew-jiath | GEN_DEF | 223 | 236 | +13 | +5.83% |  |
| 520 | player | Mark Keane | mark-keane | KEY_DEF | 1557 | 1648 | +91 | +5.84% |  |
| 521 | player | Mitchell Lewis | mitchell-lewis | KEY_FWD | 581 | 615 | +34 | +5.85% |  |
| 522 | player | Brennan Cox | brennan-cox | KEY_DEF | 512 | 542 | +30 | +5.86% |  |
| 523 | player | George Hewett | george-hewett | MID | 1412 | 1495 | +83 | +5.88% |  |
| 524 | player | Tom Lynch | tom-lynch-1 | KEY_FWD | 187 | 198 | +11 | +5.88% |  |
| 525 | player | Sam Switkowski | sam-switkowski | GEN_FWD | 51 | 54 | +3 | +5.88% |  |
| 526 | player | Finn Maginness | finn-maginness | GEN_FWD | 34 | 36 | +2 | +5.88% |  |
| 527 | player | Callum M. Brown | callum-brown-ire | GEN_FWD | 17 | 18 | +1 | +5.88% |  |
| 528 | player | Charlie Spargo | charlie-spargo | GEN_FWD | 34 | 36 | +2 | +5.88% |  |
| 529 | player | Connor O'Sullivan | connor-o-sullivan | KEY_DEF | 2701 | 2860 | +159 | +5.89% |  |
| 530 | player | Tom Powell | tom-powell | GEN_FWD | 1885 | 1996 | +111 | +5.89% |  |
| 531 | player | Jagga Smith | jagga-smith | MID | 3031 | 3210 | +179 | +5.91% |  |
| 532 | player | Max Hall | max-hall | GEN_FWD | 1844 | 1953 | +109 | +5.91% |  |
| 533 | player | Lloyd Meek | lloyd-meek | RUC | 896 | 949 | +53 | +5.92% | RUC |
| 534 | player | Thomas Stewart | thomas-stewart | GEN_DEF | 1031 | 1092 | +61 | +5.92% |  |
| 535 | player | Zachary Williams | zachary-williams | GEN_DEF | 152 | 161 | +9 | +5.92% |  |
| 536 | player | Caleb Windsor | caleb-windsor | MID | 1636 | 1733 | +97 | +5.93% |  |
| 537 | player | Toby Bedford | toby-bedford | GEN_FWD | 236 | 250 | +14 | +5.93% |  |
| 538 | player | Jack Bowes | jack-bowes | MID | 118 | 125 | +7 | +5.93% |  |
| 539 | player | James Rowbottom | james-rowbottom | MID | 471 | 499 | +28 | +5.94% |  |
| 540 | player | Patrick Voss | patrick-voss | KEY_FWD | 1631 | 1728 | +97 | +5.95% |  |
| 541 | player | Dylan Patterson | dylan-patterson | GEN_DEF | 874 | 926 | +52 | +5.95% |  |
| 542 | player | Daniel Annable | daniel-annable | MID | 1948 | 2064 | +116 | +5.95% |  |
| 543 | player | Oskar Taylor | oskar-taylor | GEN_DEF | 772 | 818 | +46 | +5.96% |  |
| 544 | player | Tom McCartin | tom-mccartin | KEY_DEF | 1443 | 1529 | +86 | +5.96% |  |
| 545 | player | Taylor Goad | taylor-goad | RUC | 788 | 835 | +47 | +5.96% | RUC |
| 546 | player | Jarrod Witts | jarrod-witts | RUC | 384 | 407 | +23 | +5.99% | RUC |
| 547 | player | Hunter Clark | hunter-clark | GEN_DEF | 50 | 53 | +3 | +6.00% |  |
| 548 | player | Jake Waterman | jake-waterman | KEY_FWD | 1483 | 1572 | +89 | +6.00% |  |
| 549 | player | Jesse Hogan | jesse-hogan | KEY_FWD | 383 | 406 | +23 | +6.01% |  |
| 550 | player | Luke Davies-Uniacke | luke-davies-uniacke | MID | 3274 | 3471 | +197 | +6.02% |  |
| 551 | player | Darcy Fort | darcy-fort | RUC | 83 | 88 | +5 | +6.02% | RUC |
| 552 | player | Clayton Oliver | clayton-oliver | MID | 2473 | 2622 | +149 | +6.03% |  |
| 553 | player | Jack Crisp | jack-crisp | MID | 597 | 633 | +36 | +6.03% |  |
| 554 | player | Cameron Zurhaar | cameron-zurhaar | GEN_FWD | 199 | 211 | +12 | +6.03% |  |
| 555 | player | Mitchell Edwards | mitchell-edwards | RUC | 1539 | 1632 | +93 | +6.04% | RUC |
| 556 | player | Lucca Grego | lucca-grego | GEN_DEF | 248 | 263 | +15 | +6.05% |  |
| 557 | player | Isaac Kako | isaac-kako | GEN_FWD | 1570 | 1665 | +95 | +6.05% |  |
| 558 | player | Cameron Rayner | cameron-rayner | GEN_FWD | 479 | 508 | +29 | +6.05% |  |
| 559 | player | Cooper Simpson | cooper-simpson | GEN_DEF | 231 | 245 | +14 | +6.06% |  |
| 560 | player | Jamie Cripps | jamie-cripps | GEN_FWD | 33 | 35 | +2 | +6.06% |  |
| 561 | player | Rhett Bazzo | rhett-bazzo | KEY_DEF | 560 | 594 | +34 | +6.07% |  |
| 562 | player | Bodie Ryan | bodie-ryan | GEN_DEF | 312 | 331 | +19 | +6.09% |  |
| 563 | player | Adam Treloar | adam-treloar | MID | 607 | 644 | +37 | +6.10% |  |
| 564 | player | Bodhi Uwland | bodhi-uwland | GEN_DEF | 3045 | 3231 | +186 | +6.11% |  |
| 565 | player | Lachlan McAndrew | lachlan-mcandrew | RUC | 998 | 1059 | +61 | +6.11% | RUC |
| 566 | player | Callum Wilkie | callum-wilkie | KEY_DEF | 3252 | 3451 | +199 | +6.12% |  |
| 567 | player | Nic Newman | nic-newman | GEN_DEF | 882 | 936 | +54 | +6.12% |  |
| 568 | player | Isaac Quaynor | isaac-quaynor | GEN_DEF | 490 | 520 | +30 | +6.12% |  |
| 569 | player | Cooper Harvey | cooper-harvey | GEN_FWD | 98 | 104 | +6 | +6.12% |  |
| 570 | player | Patrick Dangerfield | patrick-dangerfield | GEN_FWD | 98 | 104 | +6 | +6.12% |  |
| 571 | player | Mitchell Marsh | mitchell-marsh | KEY_FWD | 669 | 710 | +41 | +6.13% |  |
| 572 | player | Reilly O'Brien | reilly-o-brien | RUC | 783 | 831 | +48 | +6.13% | RUC |
| 573 | player | Jayden Short | jayden-short | GEN_DEF | 1516 | 1609 | +93 | +6.13% |  |
| 574 | player | Finnegan Davis | finnegan-davis | GEN_DEF | 407 | 432 | +25 | +6.14% |  |
| 575 | player | Tom Atkins | tom-atkins | MID | 293 | 311 | +18 | +6.14% |  |
| 576 | player | Zane Zakostelsky | zane-zakostelsky | KEY_DEF | 602 | 639 | +37 | +6.15% |  |
| 577 | player | Ben Keays | ben-keays | GEN_FWD | 309 | 328 | +19 | +6.15% |  |
| 578 | player | Rory Laird | rory-laird | GEN_DEF | 924 | 981 | +57 | +6.17% |  |
| 579 | player | Jye Amiss | jye-amiss | KEY_FWD | 1199 | 1273 | +74 | +6.17% |  |
| 580 | player | Angus Clarke | angus-clarke | GEN_DEF | 729 | 774 | +45 | +6.17% |  |
| 581 | player | Ben Camporeale | ben-camporeale | MID | 340 | 361 | +21 | +6.18% |  |
| 582 | player | Jack Buckley | jack-buckley | KEY_DEF | 728 | 773 | +45 | +6.18% |  |
| 583 | player | Aidan Schubert | aidan-schubert | KEY_FWD | 663 | 704 | +41 | +6.18% |  |
| 584 | player | Blake Acres | blake-acres | MID | 97 | 103 | +6 | +6.19% |  |
| 585 | player | Lachie Neale | lachie-neale | MID | 1826 | 1939 | +113 | +6.19% |  |
| 586 | player | Will Darcy | will-darcy | KEY_DEF | 532 | 565 | +33 | +6.20% |  |
| 587 | player | Rowan Marshall | rowan-marshall | RUC | 612 | 650 | +38 | +6.21% | RUC |
| 588 | player | Jack Sinclair | jack-sinclair | GEN_DEF | 3013 | 3201 | +188 | +6.24% |  |
| 589 | player | Patrick Said | patrick-said | GEN_FWD | 192 | 204 | +12 | +6.25% |  |
| 590 | player | Conor Stone | conor-stone | GEN_DEF | 80 | 85 | +5 | +6.25% |  |
| 591 | player | Liam Henry | liam-henry | GEN_FWD | 80 | 85 | +5 | +6.25% |  |
| 592 | player | Nicholas Coffield | nicholas-coffield | GEN_DEF | 48 | 51 | +3 | +6.25% |  |
| 593 | player | Bailey Scott | bailey-scott | MID | 32 | 34 | +2 | +6.25% |  |
| 594 | player | Ryan Gardner | ryan-gardner | KEY_DEF | 32 | 34 | +2 | +6.25% |  |
| 595 | player | Jack Ginnivan | jack-ginnivan | GEN_FWD | 1772 | 1883 | +111 | +6.26% |  |
| 596 | player | Tristan Xerri | tristan-xerri | RUC | 6384 | 6784 | +400 | +6.27% | RUC |
| 597 | player | Cooper Lord | cooper-lord | MID | 383 | 407 | +24 | +6.27% |  |
| 598 | player | Darcy Jones | darcy-jones | GEN_FWD | 1484 | 1577 | +93 | +6.27% |  |
| 599 | player | Jack Graham | jack-graham | MID | 303 | 322 | +19 | +6.27% |  |
| 600 | player | Rhys Unwin | rhys-unwin | GEN_FWD | 191 | 203 | +12 | +6.28% |  |
| 601 | player | Adam Saad | adam-saad | GEN_DEF | 636 | 676 | +40 | +6.29% |  |
| 602 | player | Harrison Coe | harrison-coe | RUC | 95 | 101 | +6 | +6.32% | RUC |
| 603 | player | James Borlase | james-borlase | KEY_DEF | 475 | 505 | +30 | +6.32% |  |
| 604 | player | Steele Sidebottom | steele-sidebottom | MID | 95 | 101 | +6 | +6.32% |  |
| 605 | player | Ben King | ben-king | KEY_FWD | 364 | 387 | +23 | +6.32% |  |
| 606 | player | Max Kondogiannis | max-kondogiannis | GEN_DEF | 538 | 572 | +34 | +6.32% |  |
| 607 | player | Jordon Sweet | jordon-sweet | RUC | 2064 | 2195 | +131 | +6.35% | RUC |
| 608 | player | Francis Evans | francis-evans | GEN_FWD | 63 | 67 | +4 | +6.35% |  |
| 609 | player | Nicholas Martin | nicholas-martin | MID | 2809 | 2988 | +179 | +6.37% |  |
| 610 | player | Koltyn Tholstrup | koltyn-tholstrup | GEN_DEF | 1332 | 1417 | +85 | +6.38% |  |
| 611 | player | Jake Melksham | jake-melksham | KEY_FWD | 47 | 50 | +3 | +6.38% |  |
| 612 | player | Oscar Ryan | oscar-ryan | GEN_DEF | 266 | 283 | +17 | +6.39% |  |
| 613 | player | Billy Frampton | billy-frampton | KEY_DEF | 172 | 183 | +11 | +6.40% |  |
| 614 | player | Matt Whitlock | matt-whitlock | KEY_FWD | 422 | 449 | +27 | +6.40% |  |
| 615 | player | Matt Johnson | matt-johnson-1 | MID | 608 | 647 | +39 | +6.41% |  |
| 616 | player | Harvey Thomas | harvey-thomas | GEN_FWD | 2368 | 2520 | +152 | +6.42% |  |
| 617 | player | Xavier Lindsay | xavier-lindsay | GEN_DEF | 1385 | 1474 | +89 | +6.43% |  |
| 618 | player | Ollie Dempsey | ollie-dempsey | MID | 1737 | 1849 | +112 | +6.45% |  |
| 619 | player | Harry Charleson | harry-charleson | GEN_DEF | 248 | 264 | +16 | +6.45% |  |
| 620 | player | Dougal Howard | dougal-howard | KEY_DEF | 93 | 99 | +6 | +6.45% |  |
| 621 | player | Jack Martin | jack-martin | GEN_FWD | 93 | 99 | +6 | +6.45% |  |
| 622 | player | Tobie Travaglia | tobie-travaglia | GEN_DEF | 758 | 807 | +49 | +6.46% |  |
| 623 | player | Avery Thomas | avery-thomas | GEN_DEF | 509 | 542 | +33 | +6.48% |  |
| 624 | player | Wil Powell | wil-powell | GEN_DEF | 955 | 1017 | +62 | +6.49% |  |
| 625 | player | Jack Henry | jack-henry | KEY_DEF | 200 | 213 | +13 | +6.50% |  |
| 626 | player | Lachlan Carmichael | lachlan-carmichael | GEN_DEF | 598 | 637 | +39 | +6.52% |  |
| 627 | player | Matt Cottrell | matt-cottrell | MID | 46 | 49 | +3 | +6.52% |  |
| 628 | player | Paddy Cross | paddy-cross | GEN_FWD | 61 | 65 | +4 | +6.56% |  |
| 629 | player | Josh Smillie | josh-smillie | MID | 1250 | 1332 | +82 | +6.56% |  |
| 630 | player | Liam O'Connell | liam-o-connell | GEN_DEF | 91 | 97 | +6 | +6.59% |  |
| 631 | player | Lachlan Jones | lachlan-jones | GEN_DEF | 91 | 97 | +6 | +6.59% |  |
| 632 | player | Chayce Jones | chayce-jones | MID | 106 | 113 | +7 | +6.60% |  |
| 633 | player | Koby Coulson | koby-coulson | MID | 528 | 563 | +35 | +6.63% |  |
| 634 | player | Toby McMullin | toby-mcmullin | GEN_FWD | 196 | 209 | +13 | +6.63% |  |
| 635 | player | Conor Nash | conor-nash | MID | 286 | 305 | +19 | +6.64% |  |
| 636 | player | Lennox Hoffman | lennox-hoffman | GEN_DEF | 240 | 256 | +16 | +6.67% |  |
| 637 | player | Jakob Ryan | jakob-ryan | GEN_DEF | 255 | 272 | +17 | +6.67% |  |
| 638 | player | Jamie Elliott | jamie-elliott | GEN_FWD | 30 | 32 | +2 | +6.67% |  |
| 639 | player | Mark O'Connor | mark-o-connor | GEN_DEF | 15 | 16 | +1 | +6.67% |  |
| 640 | player | Zane Duursma | zane-duursma | GEN_FWD | 749 | 799 | +50 | +6.68% |  |
| 641 | player | Keighton Matofai-Forbes | keighton-matofai-forbes | GEN_DEF | 239 | 255 | +16 | +6.69% |  |
| 642 | player | Kai Lohmann | kai-lohmann | GEN_FWD | 463 | 494 | +31 | +6.70% |  |
| 643 | player | Paul Curtis | paul-curtis | GEN_FWD | 1355 | 1446 | +91 | +6.72% |  |
| 644 | player | Luke Pedlar | luke-pedlar | GEN_FWD | 134 | 143 | +9 | +6.72% |  |
| 645 | player | Brady Hough | brady-hough | GEN_DEF | 357 | 381 | +24 | +6.72% |  |
| 646 | player | Jacob Farrow | jacob-farrow | GEN_DEF | 1664 | 1776 | +112 | +6.73% |  |
| 647 | player | Jack Ison | jack-ison | GEN_FWD | 489 | 522 | +33 | +6.75% |  |
| 648 | player | Liam McMahon | liam-mcmahon | KEY_FWD | 220 | 235 | +15 | +6.82% |  |
| 649 | player | Leo Lombard | leo-lombard | GEN_FWD | 1583 | 1691 | +108 | +6.82% |  |
| 650 | player | Charlie Comben | charlie-comben | KEY_DEF | 718 | 767 | +49 | +6.82% |  |
| 651 | player | Liam Baker | liam-baker | GEN_DEF | 630 | 673 | +43 | +6.83% |  |
| 652 | player | Jacob Hopper | jacob-hopper | MID | 117 | 125 | +8 | +6.84% |  |
| 653 | player | Oliver Hayes-Brown | oliver-hayes-brown | RUC | 335 | 358 | +23 | +6.87% | RUC |
| 654 | player | Tom Edwards | tom-edwards | KEY_FWD | 58 | 62 | +4 | +6.90% |  |
| 655 | player | Dylan Stephens | dylan-stephens | MID | 348 | 372 | +24 | +6.90% |  |
| 656 | player | Oskar Baker | oskar-baker | GEN_FWD | 29 | 31 | +2 | +6.90% |  |
| 657 | player | Cody Weightman | cody-weightman | GEN_FWD | 275 | 294 | +19 | +6.91% |  |
| 658 | player | James O'Donnell | james-o-donnell | KEY_DEF | 390 | 417 | +27 | +6.92% |  |
| 659 | player | Jai Serong | jai-serong | GEN_DEF | 101 | 108 | +7 | +6.93% |  |
| 660 | player | Bobby Hill | bobby-hill | GEN_FWD | 72 | 77 | +5 | +6.94% |  |
| 661 | player | Cody Anderson | cody-anderson | GEN_FWD | 187 | 200 | +13 | +6.95% |  |
| 662 | player | Joseph Fonti | joseph-fonti | GEN_DEF | 703 | 752 | +49 | +6.97% |  |
| 663 | player | Sam Davidson | sam-davidson | GEN_FWD | 86 | 92 | +6 | +6.98% |  |
| 664 | player | Malcolm Rosas | malcolm-rosas | GEN_FWD | 86 | 92 | +6 | +6.98% |  |
| 665 | player | Charlie Cameron | charlie-cameron | GEN_FWD | 271 | 290 | +19 | +7.01% |  |
| 666 | player | Riley Hamilton | riley-hamilton | GEN_FWD | 342 | 366 | +24 | +7.02% |  |
| 667 | player | Lewis Melican | lewis-melican | KEY_DEF | 57 | 61 | +4 | +7.02% |  |
| 668 | player | Harvey Gallagher | harvey-gallagher | GEN_DEF | 128 | 137 | +9 | +7.03% |  |
| 669 | player | Josh Lindsay | josh-lindsay | GEN_DEF | 1620 | 1734 | +114 | +7.04% |  |
| 670 | player | Lachie Jaques | lachie-jaques | GEN_DEF | 723 | 774 | +51 | +7.05% |  |
| 671 | player | River Stevens | river-stevens | GEN_FWD | 184 | 197 | +13 | +7.07% |  |
| 672 | player | Riley Garcia | riley-garcia | GEN_FWD | 155 | 166 | +11 | +7.10% |  |
| 673 | player | Noah Roberts-Thomson | noah-roberts-thomson | GEN_FWD | 408 | 437 | +29 | +7.11% |  |
| 674 | player | Blake Howes | blake-howes | GEN_DEF | 308 | 330 | +22 | +7.14% |  |
| 675 | player | Will Lewis | will-lewis | KEY_FWD | 14 | 15 | +1 | +7.14% |  |
| 676 | player | Jesse Mellor | jesse-mellor | MID | 293 | 314 | +21 | +7.17% |  |
| 677 | player | Harrison Oliver | harrison-oliver | GEN_DEF | 541 | 580 | +39 | +7.21% |  |
| 678 | player | Luke Cleary | luke-cleary | GEN_DEF | 83 | 89 | +6 | +7.23% |  |
| 679 | player | Zac Taylor | zac-taylor | GEN_FWD | 359 | 385 | +26 | +7.24% |  |
| 680 | player | Nikolas Cox | nikolas-cox | KEY_FWD | 400 | 429 | +29 | +7.25% |  |
| 681 | player | Charlie Nicholls | charlie-nicholls | KEY_FWD | 358 | 384 | +26 | +7.26% |  |
| 682 | player | Jai Saxena | jai-saxena | GEN_FWD | 234 | 251 | +17 | +7.26% |  |
| 683 | player | Ryda Luke | ryda-luke | GEN_FWD | 234 | 251 | +17 | +7.26% |  |
| 684 | player | Toby Whan | toby-whan | GEN_FWD | 234 | 251 | +17 | +7.26% |  |
| 685 | player | Jacob Moss | jacob-moss | KEY_FWD | 275 | 295 | +20 | +7.27% |  |
| 686 | player | Hugo Ralphsmith | hugo-ralphsmith | MID | 55 | 59 | +4 | +7.27% |  |
| 687 | player | Sam Draper | sam-draper | RUC | 631 | 677 | +46 | +7.29% | RUC |
| 688 | player | Luker Kentfield | luker-kentfield | KEY_FWD | 315 | 338 | +23 | +7.30% |  |
| 689 | player | Corey Wagner | corey-wagner | GEN_DEF | 41 | 44 | +3 | +7.32% |  |
| 690 | player | Callum Ah Chee | callum-ah-chee | GEN_FWD | 82 | 88 | +6 | +7.32% |  |
| 691 | player | Kye Fincher | kye-fincher | MID | 490 | 526 | +36 | +7.35% |  |
| 692 | player | Josh Sinn | josh-sinn | GEN_DEF | 340 | 365 | +25 | +7.35% |  |
| 693 | player | Thomas Burton | thomas-burton | GEN_FWD | 340 | 365 | +25 | +7.35% |  |
| 694 | player | Jamarra Ugle-Hagan | jamarra-ugle-hagan | KEY_FWD | 190 | 204 | +14 | +7.37% |  |
| 695 | player | Jy Farrar | jy-farrar | KEY_FWD | 27 | 29 | +2 | +7.41% |  |
| 696 | player | Harry Morrison | harry-morrison | MID | 27 | 29 | +2 | +7.41% |  |
| 697 | player | Nick Murray | nick-murray | KEY_DEF | 215 | 231 | +16 | +7.44% |  |
| 698 | player | Kaleb Smith | kaleb-smith | GEN_DEF | 107 | 115 | +8 | +7.48% |  |
| 699 | player | Nathan Wardius | nathan-wardius | GEN_FWD | 147 | 158 | +11 | +7.48% |  |
| 700 | player | Noah Chamberlain | noah-chamberlain | GEN_FWD | 160 | 172 | +12 | +7.50% |  |
| 701 | player | Tyler Brockman | tyler-brockman | GEN_FWD | 53 | 57 | +4 | +7.55% |  |
| 702 | player | Tom Hanily | tom-hanily | GEN_FWD | 145 | 156 | +11 | +7.59% |  |
| 703 | player | Isaiah Dudley | isaiah-dudley | GEN_FWD | 79 | 85 | +6 | +7.59% |  |
| 704 | player | Maurice Rioli | maurice-rioli-1 | GEN_FWD | 79 | 85 | +6 | +7.59% |  |
| 705 | player | Tom Gross | tom-gross | MID | 618 | 665 | +47 | +7.61% |  |
| 706 | player | Charlie Ballard | charlie-ballard | KEY_DEF | 118 | 127 | +9 | +7.63% |  |
| 707 | player | Kayle Gerreyn | kayle-gerreyn | KEY_FWD | 327 | 352 | +25 | +7.65% |  |
| 708 | player | Angus Hastie | angus-hastie | GEN_DEF | 287 | 309 | +22 | +7.67% |  |
| 709 | player | Lucas Camporeale | lucas-camporeale | MID | 287 | 309 | +22 | +7.67% |  |
| 710 | player | William McCabe | william-mccabe | KEY_FWD | 533 | 574 | +41 | +7.69% |  |
| 711 | player | Tylar Young | tylar-young | KEY_DEF | 91 | 98 | +7 | +7.69% |  |
| 712 | player | Toby Pink | toby-pink | KEY_DEF | 39 | 42 | +3 | +7.69% |  |
| 713 | player | Brandon Starcevich | brandon-starcevich | GEN_DEF | 39 | 42 | +3 | +7.69% |  |
| 714 | player | Harry Armstrong | harry-armstrong | KEY_FWD | 851 | 917 | +66 | +7.76% |  |
| 715 | player | Zach Guthrie | zach-guthrie | GEN_DEF | 464 | 500 | +36 | +7.76% |  |
| 716 | player | Finnbar Maley | finnbar-maley | KEY_FWD | 244 | 263 | +19 | +7.79% |  |
| 717 | player | Josh Treacy | josh-treacy | KEY_FWD | 6055 | 6529 | +474 | +7.83% |  |
| 718 | player | Matthew LeRay | matthew-leray | MID | 472 | 509 | +37 | +7.84% |  |
| 719 | player | Kalani White | kalani-white | KEY_FWD | 280 | 302 | +22 | +7.86% |  |
| 720 | player | Luke Urquhart | luke-urquhart | MID | 280 | 302 | +22 | +7.86% |  |
| 721 | player | Mitchell Hinge | mitchell-hinge | GEN_DEF | 458 | 494 | +36 | +7.86% |  |
| 722 | player | Luke Lloyd | luke-lloyd | KEY_FWD | 203 | 219 | +16 | +7.88% |  |
| 723 | player | Mani Liddy | mani-liddy | MID | 38 | 41 | +3 | +7.89% |  |
| 724 | player | Ricky Mentha | ricky-mentha | GEN_FWD | 139 | 150 | +11 | +7.91% |  |
| 725 | player | Benny Barrett | benny-barrett | GEN_FWD | 139 | 150 | +11 | +7.91% |  |
| 726 | player | Jake Rogers | jake-rogers | GEN_FWD | 592 | 639 | +47 | +7.94% |  |
| 727 | player | Brandon Walker | brandon-walker | GEN_DEF | 88 | 95 | +7 | +7.95% |  |
| 728 | player | Liam Hetherton | liam-hetherton | KEY_FWD | 213 | 230 | +17 | +7.98% |  |
| 729 | player | Mitch McGovern | mitch-mcgovern | GEN_DEF | 25 | 27 | +2 | +8.00% |  |
| 730 | player | Zac Walker | zac-walker | GEN_DEF | 174 | 188 | +14 | +8.05% |  |
| 731 | player | Jaxon Artemis | jaxon-artemis | GEN_DEF | 372 | 402 | +30 | +8.06% |  |
| 732 | player | Buku Khamis | buku-khamis | KEY_DEF | 74 | 80 | +6 | +8.11% |  |
| 733 | player | Steely Green | steely-green | GEN_FWD | 256 | 277 | +21 | +8.20% |  |
| 734 | player | Xavier Bamert | xavier-bamert | GEN_FWD | 279 | 302 | +23 | +8.24% |  |
| 735 | player | Harvey Johnston | harvey-johnston | GEN_DEF | 254 | 275 | +21 | +8.27% |  |
| 736 | player | Cody Curtin | cody-curtin | KEY_FWD | 677 | 733 | +56 | +8.27% |  |
| 737 | player | Matthew Jefferson | matthew-jefferson | KEY_FWD | 555 | 601 | +46 | +8.29% |  |
| 738 | player | Ned Reeves | ned-reeves | RUC | 374 | 405 | +31 | +8.29% | RUC |
| 739 | player | Bradley Close | bradley-close | GEN_FWD | 24 | 26 | +2 | +8.33% |  |
| 740 | player | Dane Rampe | dane-rampe | GEN_DEF | 12 | 13 | +1 | +8.33% |  |
| 741 | player | Conor McKenna | conor-mckenna | GEN_FWD | 12 | 13 | +1 | +8.33% |  |
| 742 | player | Matt Guelfi | matt-guelfi | GEN_FWD | 24 | 26 | +2 | +8.33% |  |
| 743 | player | Hussien El Achkar | hussien-el-achkar | GEN_FWD | 371 | 402 | +31 | +8.36% |  |
| 744 | player | Harrison Ramm | harrison-ramm | KEY_DEF | 297 | 322 | +25 | +8.42% |  |
| 745 | player | Riak Andrew | riak-andrew | KEY_DEF | 306 | 332 | +26 | +8.50% |  |
| 746 | player | Jack Williams | jack-williams | KEY_FWD | 529 | 574 | +45 | +8.51% |  |
| 747 | player | Harry Edwards | harry-edwards | KEY_DEF | 94 | 102 | +8 | +8.51% |  |
| 748 | player | Tobyn Murray | tobyn-murray | GEN_FWD | 421 | 457 | +36 | +8.55% |  |
| 749 | player | Michael Sellwood | michael-sellwood | GEN_DEF | 80 | 87 | +7 | +8.75% |  |
| 750 | player | Ollie Lord | ollie-lord | KEY_FWD | 160 | 174 | +14 | +8.75% |  |
| 751 | player | Reece Torrent | reece-torrent | MID | 205 | 223 | +18 | +8.78% |  |
| 752 | player | Henry Smith | henry-smith | KEY_FWD | 147 | 160 | +13 | +8.84% |  |
| 753 | player | Will Edwards | will-edwards | KEY_DEF | 260 | 283 | +23 | +8.85% |  |
| 754 | player | Archie Ludowyke | archie-ludowyke | KEY_FWD | 373 | 406 | +33 | +8.85% |  |
| 755 | player | Campbell Gray | campbell-gray | KEY_DEF | 236 | 257 | +21 | +8.90% |  |
| 756 | player | Leek Aleer | leek-aleer | KEY_DEF | 323 | 352 | +29 | +8.98% |  |
| 757 | player | Lachlan Blakiston | lachlan-blakiston | KEY_DEF | 22 | 24 | +2 | +9.09% |  |
| 758 | player | Charlie West | charlie-west | KEY_FWD | 427 | 466 | +39 | +9.13% |  |
| 759 | player | Zac McCarthy | zac-mccarthy | KEY_FWD | 360 | 393 | +33 | +9.17% |  |
| 760 | player | Tyler Welsh | tyler-welsh | KEY_FWD | 229 | 250 | +21 | +9.17% |  |
| 761 | player | Judson Clarke | judson-clarke | GEN_FWD | 87 | 95 | +8 | +9.20% |  |
| 762 | player | Caleb Graham | caleb-graham | KEY_DEF | 76 | 83 | +7 | +9.21% |  |
| 763 | player | Oliver Griffin | oliver-griffin | GEN_FWD | 238 | 260 | +22 | +9.24% |  |
| 764 | player | Angus Anderson | angus-anderson | MID | 119 | 130 | +11 | +9.24% |  |
| 765 | player | Jack Hutchinson | jack-hutchinson | MID | 54 | 59 | +5 | +9.26% |  |
| 766 | player | Talor Byrne | talor-byrne | GEN_FWD | 494 | 540 | +46 | +9.31% |  |
| 767 | player | Oscar Adams | oscar-adams | GEN_DEF | 106 | 116 | +10 | +9.43% |  |
| 768 | player | Charlie Edwards | charlie-edwards | MID | 674 | 738 | +64 | +9.50% |  |
| 769 | player | Riley Bice | riley-bice | GEN_DEF | 411 | 451 | +40 | +9.73% |  |
| 770 | player | Liam Fawcett | liam-fawcett | KEY_FWD | 512 | 562 | +50 | +9.77% |  |
| 771 | player | Max Gruzewski | max-gruzewski | KEY_FWD | 414 | 455 | +41 | +9.90% |  |
| 772 | player | Will McLachlan | will-mclachlan | GEN_FWD | 140 | 154 | +14 | +10.00% |  |
| 773 | player | Ben Long | ben-long | GEN_FWD | 30 | 33 | +3 | +10.00% |  |
| 774 | player | Laitham Vandermeer | laitham-vandermeer | GEN_FWD | 30 | 33 | +3 | +10.00% |  |
| 775 | player | Noah Howes | noah-howes | KEY_FWD | 217 | 239 | +22 | +10.14% |  |
| 776 | player | Jaren Carr | jaren-carr | GEN_FWD | 225 | 248 | +23 | +10.22% |  |
| 777 | player | Harrison Jones | harrison-jones | KEY_FWD | 107 | 118 | +11 | +10.28% |  |
| 778 | player | Daniel Butler | daniel-butler | GEN_FWD | 19 | 21 | +2 | +10.53% |  |
| 779 | player | Oliver Francou | oliver-francou | MID | 398 | 440 | +42 | +10.55% |  |
| 780 | player | Liam Ryan | liam-ryan | GEN_FWD | 28 | 31 | +3 | +10.71% |  |
| 781 | player | Noah Answerth | noah-answerth | GEN_DEF | 28 | 31 | +3 | +10.71% |  |
| 782 | player | Jai Culley | jai-culley | MID | 81 | 90 | +9 | +11.11% |  |
| 783 | player | Mark Blicavs | mark-blicavs | MID | 9 | 10 | +1 | +11.11% |  |
| 784 | player | Jesse Motlop | jesse-motlop | GEN_FWD | 151 | 168 | +17 | +11.26% |  |
| 785 | player | Luke Kennedy | luke-kennedy | MID | 387 | 431 | +44 | +11.37% |  |
| 786 | player | Max Ramsden | max-ramsden | KEY_FWD | 182 | 203 | +21 | +11.54% |  |
| 787 | player | Josh Gibcus | josh-gibcus | KEY_DEF | 277 | 309 | +32 | +11.55% |  |
| 788 | player | George Stevens | george-stevens | MID | 337 | 376 | +39 | +11.57% |  |
| 789 | player | Ben Jepson | ben-jepson | MID | 17 | 19 | +2 | +11.76% |  |
| 790 | player | Andy Moniz-Wakefield | andy-moniz-wakefield | GEN_DEF | 59 | 66 | +7 | +11.86% |  |
| 791 | player | Jackson Mead | jackson-mead | GEN_FWD | 59 | 66 | +7 | +11.86% |  |
| 792 | player | Toby Murray | toby-murray | KEY_FWD | 202 | 226 | +24 | +11.88% |  |
| 793 | player | Latrelle Pickett | latrelle-pickett | GEN_FWD | 617 | 692 | +75 | +12.16% |  |
| 794 | player | Arthur Jones | arthur-jones | GEN_FWD | 236 | 265 | +29 | +12.29% |  |
| 795 | player | Josh Goater | josh-goater | GEN_DEF | 97 | 109 | +12 | +12.37% |  |
| 796 | player | James Blanck | james-blanck | KEY_DEF | 8 | 9 | +1 | +12.50% |  |
| 797 | player | Tai Hayes | tai-hayes | GEN_FWD | 271 | 306 | +35 | +12.92% |  |
| 798 | player | Jack Buller | jack-buller | KEY_FWD | 37 | 42 | +5 | +13.51% |  |
| 799 | player | Dante Visentini | dante-visentini | RUC | 723 | 821 | +98 | +13.55% | RUC |
| 800 | player | Oliver Wiltshire | oliver-wiltshire | GEN_FWD | 93 | 106 | +13 | +13.98% |  |
| 801 | player | Jordon Butts | jordon-butts | KEY_DEF | 14 | 16 | +2 | +14.29% |  |
| 802 | player | Wil Parker | wil-parker | GEN_DEF | 34 | 39 | +5 | +14.71% |  |
| 803 | player | Flynn Perez | flynn-perez | GEN_DEF | 13 | 15 | +2 | +15.38% |  |
| 804 | player | Ewan Mackinlay | ewan-mackinlay | GEN_FWD | 42 | 49 | +7 | +16.67% |  |
| 805 | player | Bailey Banfield | bailey-banfield | GEN_DEF | 6 | 7 | +1 | +16.67% |  |
| 806 | player | Tom Cochrane | tom-cochrane | GEN_FWD | 257 | 300 | +43 | +16.73% |  |
| 807 | player | Asher Eastham | asher-eastham | GEN_FWD | 208 | 243 | +35 | +16.83% |  |
| 808 | player | Campbell Lake | campbell-lake | GEN_FWD | 114 | 134 | +20 | +17.54% |  |
| 809 | player | Aidan Johnson | aidan-johnson | KEY_FWD | 79 | 93 | +14 | +17.72% |  |
| 810 | player | Xavier Walsh | xavier-walsh | KEY_DEF | 223 | 263 | +40 | +17.94% |  |
| 811 | player | Nathan Broad | nathan-broad | GEN_DEF | 11 | 13 | +2 | +18.18% |  |
| 812 | player | Billy Cootee | billy-cootee | MID | 79 | 94 | +15 | +18.99% |  |
| 813 | player | Mitch Podhajski | mitch-podhajski | KEY_FWD | 5 | 6 | +1 | +20.00% |  |
| 814 | player | Hugo Hall-Kahan | hugo-hall-kahan | GEN_DEF | 89 | 107 | +18 | +20.22% |  |
| 815 | player | Zac Banch | zac-banch | GEN_FWD | 49 | 59 | +10 | +20.41% |  |
| 816 | player | Wade Derksen | wade-derksen | KEY_DEF | 81 | 98 | +17 | +20.99% |  |
| 817 | player | Jacob Wehr | jacob-wehr | GEN_DEF | 19 | 23 | +4 | +21.05% |  |
| 818 | player | Flynn Young | flynn-young | GEN_FWD | 9 | 11 | +2 | +22.22% |  |
| 819 | player | Jack Henderson | jack-henderson | GEN_FWD | 4 | 5 | +1 | +25.00% |  |
| 820 | player | Darragh Joyce | darragh-joyce | KEY_DEF | 8 | 10 | +2 | +25.00% |  |
| 821 | player | Marcus Herbert | marcus-herbert | GEN_DEF | 26 | 33 | +7 | +26.92% |  |
| 822 | player | Caleb Lewis | caleb-lewis | KEY_FWD | 111 | 142 | +31 | +27.93% |  |
| 823 | player | Joel Fitzgerald | joel-fitzgerald | MID | 66 | 86 | +20 | +30.30% |  |
| 824 | player | Liam Reidy | liam-reidy | RUC | 279 | 373 | +94 | +33.69% | RUC |
| 825 | player | Oscar Berry | oscar-berry | KEY_DEF | 105 | 143 | +38 | +36.19% |  |
| 826 | player | Kye Annand | kye-annand | KEY_DEF | 111 | 154 | +43 | +38.74% |  |
| 827 | player | Max Beattie | max-beattie | GEN_FWD | 38 | 53 | +15 | +39.47% |  |
| 828 | player | Lukas Cooke | lukas-cooke | KEY_DEF | 96 | 138 | +42 | +43.75% |  |
| 829 | player | Louis Emmett | louis-emmett | RUC | 788 | 1178 | +390 | +49.49% | RUC |
| 830 | player | Fred Rodriguez | fred-rodriguez | MID | 2 | 3 | +1 | +50.00% |  |
| 831 | player | Luke Beecken | luke-beecken | MID | 17 | 26 | +9 | +52.94% |  |
| 832 | player | Liam Puncher | liam-puncher | KEY_DEF | 89 | 144 | +55 | +61.80% |  |
| 833 | player | Nick Driscoll | nick-driscoll | MID | 4 | 8 | +4 | +100.00% |  |
| 834 | player | Leon Kickett | leon-kickett | GEN_FWD | 4 | 8 | +4 | +100.00% |  |
| 835 | player | Jack Watkins | jack-watkins | MID | 1 | 2 | +1 | +100.00% |  |
