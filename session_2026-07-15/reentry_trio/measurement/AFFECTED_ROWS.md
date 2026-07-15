# AFFECTED_ROWS — RE-ENTRY TRIO store correction (base dc43d602 -> candidate 800d0399)

- Total v-movers: **106** | material (>=5%): **43** (all MSD) | hairline (|d|<=2): **33** | net **+30** num-SCAR
- Trio own values UNCHANGED: Perez 13, McAndrew 1232, Keane 2155 (engine override already SSP-prices them).
- Isolation: Perez-only=0 movers, Keane-only=0 movers, McAndrew-only=106 movers (=full trio). Driver = PICKEQ['MSD'] 60->90.

## Material movers (>=5%), all MSD, before -> after (delta, %):
| player | pos | before | after | d | % |
|---|---|--:|--:|--:|--:|
| Jai Newcombe | MID | 4302 | 3975 | -327 | -8% |
| Harrison Coe | RUC | 97 | 258 | +161 | +166% |
| John Noble | GEN_DEF | 2699 | 2554 | -145 | -5% |
| Max Hall | GEN_FWD | 2310 | 2168 | -142 | -6% |
| Massimo D'Ambrosio | MID | 1755 | 1622 | -133 | -8% |
| Sam Durham | MID | 1823 | 1694 | -129 | -7% |
| Archie May | KEY_FWD | 370 | 487 | +117 | +32% |
| James Peatling | MID | 1434 | 1346 | -88 | -6% |
| Caleb Lewis | KEY_FWD | 136 | 224 | +88 | +65% |
| Toby Murray | KEY_FWD | 192 | 278 | +86 | +45% |
| Lukas Cooke | KEY_DEF | 118 | 191 | +73 | +62% |
| Kye Annand | KEY_DEF | 125 | 192 | +67 | +54% |
| Liam Puncher | KEY_DEF | 106 | 173 | +67 | +63% |
| Noah Howes | KEY_FWD | 225 | 292 | +67 | +30% |
| Luker Kentfield | KEY_FWD | 336 | 389 | +53 | +16% |
| Max Ramsden | KEY_FWD | 180 | 229 | +49 | +27% |
| Joel Fitzgerald | MID | 67 | 112 | +45 | +67% |
| Jack Buller | KEY_FWD | 36 | 79 | +43 | +119% |
| Campbell Gray | KEY_DEF | 236 | 276 | +40 | +17% |
| Wade Derksen | KEY_DEF | 81 | 121 | +40 | +49% |
| Campbell Lake | GEN_FWD | 126 | 154 | +28 | +22% |
| Mitch Podhajski | KEY_FWD | 5 | 32 | +27 | +540% |
| Will McLachlan | GEN_FWD | 150 | 177 | +27 | +18% |
| Jack Hutchinson | MID | 45 | 71 | +26 | +58% |
| Hugo Hall-Kahan | GEN_DEF | 86 | 109 | +23 | +27% |
| Mani Liddy | MID | 33 | 56 | +23 | +70% |
| Tom Hanily | GEN_FWD | 149 | 172 | +23 | +15% |
| Luke Beecken | MID | 15 | 36 | +21 | +140% |
| James Blanck | KEY_DEF | 12 | 33 | +21 | +175% |
| Max Beattie | GEN_FWD | 36 | 56 | +20 | +56% |
| Harrison Ramm | KEY_DEF | 310 | 329 | +19 | +6% |
| Robert Hansen | GEN_FWD | 147 | 165 | +18 | +12% |
| Zac Walker | GEN_DEF | 184 | 168 | -16 | -9% |
| Ewan Mackinlay | GEN_FWD | 45 | 61 | +16 | +36% |
| Oliver Griffin | GEN_FWD | 253 | 239 | -14 | -6% |
| Michael Sellwood | GEN_DEF | 73 | 87 | +14 | +19% |
| Zac Banch | GEN_FWD | 54 | 68 | +14 | +26% |
| Marcus Herbert | GEN_DEF | 22 | 35 | +13 | +59% |
| Roan Steele | MID | 13 | 22 | +9 | +69% |
| Jai Culley | MID | 85 | 79 | -6 | -7% |
| Flynn Young | GEN_FWD | 9 | 13 | +4 | +44% |
| Lachlan Blakiston | KEY_DEF | 13 | 16 | +3 | +23% |
| Saad El-Hawli | GEN_DEF | 19 | 22 | +3 | +16% |

## Non-material movers (63): all hairline float ripple, |d|<=3 num-SCAR
| player | pos | type | before | after | d |
|---|---|---|--:|--:|--:|
| Ned Moyle | RUC | MSD | 1766 | 1682 | -84 |
| Tom McCarthy | GEN_DEF | MSD | 1611 | 1541 | -70 |
| Daniel Turner | KEY_DEF | MSD | 1623 | 1592 | -31 |
| Logan Evans | GEN_DEF | MSD | 1286 | 1255 | -31 |
| Cooper Trembath | KEY_FWD | MSD | 1558 | 1535 | -23 |
| Flynn Riley | RUC | MSD | 427 | 412 | -15 |
| Caleb May | RUC | MSD | 427 | 412 | -15 |
| Alex Van Wyk | RUC | MSD | 427 | 412 | -15 |
| Max Mapley | RUC | MSD | 427 | 412 | -15 |
| Ryan Maric | MID | MSD | 1262 | 1247 | -15 |
| Josh Lindsay | GEN_DEF | ND | 2395 | 2382 | -13 |
| Oskar Taylor | GEN_DEF | ND | 813 | 823 | +10 |
| Joseph Fonti | GEN_DEF | ND | 792 | 782 | -10 |
| Iliro Smit | RUC | MSD | 280 | 271 | -9 |
| Kysaiah Pickett | GEN_FWD | ND | 3901 | 3909 | +8 |
| Xavier Bamert | GEN_FWD | MSD | 300 | 292 | -8 |
| Xavier Taylor | GEN_DEF | ND | 900 | 906 | +6 |
| Wil Powell | GEN_DEF | ND | 955 | 949 | -6 |
| Hussien El Achkar | GEN_FWD | ND | 463 | 469 | +6 |
| Dylan Patterson | GEN_DEF | ND | 978 | 983 | +5 |
| Harry Kyle | GEN_DEF | ND | 929 | 934 | +5 |
| Jaxon Artemis | GEN_DEF | MSD | 391 | 386 | -5 |
| Jacob Newton | GEN_FWD | MSD | 150 | 155 | +5 |
| Max Heath | RUC | MSD | 155 | 150 | -5 |
| James Trezise | GEN_DEF | MSD | 177 | 181 | +4 |
| Cooper Sharman | KEY_FWD | MSD | 751 | 748 | -3 |
| Jayden Nguyen | GEN_DEF | PDN | 425 | 422 | -3 |
| Corey Warner | GEN_FWD | ND | 79 | 76 | -3 |
| Judd McVee | GEN_DEF | RD | 270 | 267 | -3 |
| Harry Sharp | GEN_FWD | ND | 105 | 108 | +3 |
| Latrelle Pickett | GEN_FWD | ND | 581 | 583 | +2 |
| Lachlan Carmichael | GEN_DEF | ND | 645 | 647 | +2 |
| James Leake | GEN_DEF | ND | 348 | 350 | +2 |
| Max Kondogiannis | GEN_DEF | ND | 549 | 551 | +2 |
| Oliver Francou | MID | MSD | 413 | 415 | +2 |
| Tyrell Dewar | GEN_DEF | PDN | 211 | 209 | -2 |
| Conor Stone | GEN_DEF | ND | 84 | 86 | +2 |
| Harvey Thomas | GEN_FWD | ND | 2414 | 2415 | +1 |
| Connor MacDonald | GEN_FWD | ND | 2661 | 2662 | +1 |
| Shai Bolton | GEN_FWD | ND | 2256 | 2255 | -1 |
| Josh Rachele | GEN_FWD | ND | 2274 | 2273 | -1 |
| Lawson Humphries | GEN_DEF | ND | 1894 | 1893 | -1 |
| Leo Lombard | GEN_FWD | ND | 1462 | 1461 | -1 |
| Joshua Weddle | GEN_DEF | ND | 1578 | 1579 | +1 |
| Oliver Hollands | GEN_DEF | ND | 1494 | 1493 | -1 |
| Bradley Hill | GEN_FWD | ND | 795 | 796 | +1 |
| Harrison Oliver | GEN_DEF | ND | 617 | 616 | -1 |
| Lachie Jaques | GEN_DEF | ND | 803 | 802 | -1 |
| Max Michalanney | GEN_DEF | ND | 584 | 585 | +1 |
| Angus Hastie | GEN_DEF | ND | 305 | 304 | -1 |
| Oscar Ryan | GEN_DEF | ND | 289 | 290 | +1 |
| Tom Brown | GEN_DEF | ND | 477 | 478 | +1 |
| Brady Hough | GEN_DEF | ND | 360 | 359 | -1 |
| Zak Johnson | GEN_DEF | ND | 582 | 581 | -1 |
| Cooper Lord | MID | MSD | 389 | 390 | +1 |
| Josh Goater | GEN_DEF | ND | 105 | 106 | +1 |
| Karl Worner | GEN_DEF | RD | 591 | 590 | -1 |
| Zac Fisher | GEN_FWD | ND | 211 | 210 | -1 |
| Maurice Rioli | GEN_FWD | ND | 78 | 79 | +1 |
| Hunter Clark | GEN_DEF | ND | 54 | 55 | +1 |
| Nicholas Coffield | GEN_DEF | ND | 52 | 53 | +1 |
| Jackson Mead | GEN_FWD | ND | 56 | 57 | +1 |
| Brandon Starcevich | GEN_DEF | ND | 42 | 43 | +1 |
