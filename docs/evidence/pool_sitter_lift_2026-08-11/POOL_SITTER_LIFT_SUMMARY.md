# ORDER 19 — LIFTING THE POOL SITTER PENALTY: HOW BIG IS IT?

**Short answer for the owner: lifting the H leg alone is worth `+2,306` board points (`+0.31%` of the
whole board, `+1.87%` of the pool). Lifting the whole pool sitter penalty is worth `+8,467`
(`+1.14%` of the board, `+6.87%` of the pool), across 75 named players. And it changes the v0 of
exactly nobody — the sitter penalty never touches v0, on either leg, and that is proven three
different ways below.**

**The ND sitter treatment is untouched in both variants.** That is the owner's ruling; it is enforced
by construction and **verified**: zero national-draft rows on the live board move under either variant.

Instruments (this dir, all re-runnable, all outputs committed):
`pool_sitter_lift.py` → `pool_sitter_lift_out.txt` / `POOL_SITTER_LIFT.json` ·
`lift_consequence.py` → `lift_consequence_out.txt` / `LIFT_CONSEQUENCE.json` ·
builders `emit_variant_o19.sh`, `build_board_o19.sh` ·
pre-registration `PREREG_ORDER19.md`, **committed before any measurement was run** (`081ca02`).

Pins asserted at entry **and** exit of both instruments, all three **UNMOVED**:
board `94f1fec59f99c59d5890d5975c79fa9b` · store `d9a24282357cf3083b1640466e3ecd83` ·
instrument `noarb_table_338.py` `0f8220351c64c56ccfa90c60edcdfa5f`.
**Nothing was wired. No shipped default changed. The live board was not touched.**

---

## THE TWO VARIANTS, AND HOW EACH WAS BUILT

| | what is lifted | how it was built |
|---|---|---|
| **VARIANT A** | the **H leg** only: `H_POOLSIT` (0.804) and `H_UNION` (0.280) → 1.0 | existing manifest dials, gate mode, guards armed, config hash restamped |
| **VARIANT B** | **the whole pool sitter penalty**: A **plus** the R leg neutralised inside `sitout_ev` for pool rows (`if p.get('_pool'): R=1.0`) | no dial exists for the R leg, so a **one-line source patch in a scratchpad git worktree**. The checkout's `engine/rl_after/_merged_recover.py` was never written |

The patch is applied **before** the identity restamp, so `expected_boot.json` carries the patched
`engine_head` and every boot guard stays armed. The proof it is a *code* variant and not a silently
identical rebuild is machine-readable: emitted matrix `engine_head` is `a8071af4` for SHIP and
variant A, **`002ff843` for variant B**.

**ND rows keep R exactly as they are, at both R sites.** The patch is `p.get('_pool')`-gated.

### The four controls, run before anything was reported

| | control | result |
|---|---|---|
| 1 | a HEAD-defaults board build vs **the live board** | **md5 `94f1fec59f99c59d5890d5975c79fa9b` — byte-identical** |
| 2 | a fresh HEAD-defaults 24-year emit vs `per_entrant_SHIP.json` | **`recs` byte-identical** (only the worktree path in `meta` differs) |
| 3 | this act's cell construction vs ORDER 18's published composed `R × H` column | max abs delta **0.000045 → REPRODUCED** |
| 4 | phase 1's own `phase1_derive.py` re-run on SHIP vs the committed `PHASE1_DERIVE.json` | max abs λ delta **0.0**, `nd_profile` delta **0.0 → REPRODUCED** |
| 5 | `noarb_table_338.py` re-run on SHIP vs the committed `table_SHIP.json` | **groups identical** |

---

## 1. THE BOARD EFFECT

Live board, 804 `active` rows, `v = round(engine ev(p,2026) / F)`. Board total today **745,888**.
Pool rows carry **123,243** of that (16.52%) across 243 rows.

| | board total | change | change % | rows moved | up | down |
|---|---|---|---|---|---|---|
| **TODAY (shipped)** | 745,888 | — | — | — | — | — |
| **VARIANT A** (H lifted) | 748,194 | **+2,306** | **+0.309%** | **49** | 49 | 0 |
| **VARIANT B** (H and R lifted) | 754,355 | **+8,467** | **+1.135%** | **75** | 75 | 0 |

- **Every moved row is a pool row. Zero national-draft rows move under either variant.**
- **A's row set is a strict subset of B's** (`B \ A` = 26 rows, `A \ B` = 0).
- Nothing moves **down**. Both variants are pure lifts, as designed.
- The `back` board (198 delisted/non-active rows, 2,469 points) does not move at all under either
  variant: `delisted(p)` returns `0.02*v0_start` before any sitter site is reached (`ev():2229`).

### Distribution of the moves (each row's own % change)

| variant | n | min | p25 | median | p75 | max |
|---|---|---|---|---|---|---|
| A | 49 | +2.50% | +17.05% | **+23.88%** | +26.53% | +344.23% |
| B | 75 | +2.50% | +51.59% | **+106.25%** | +184.62% | **+633.33%** |

Bucketed under variant B: 4 rows move under 10% (28 pts) · 12 rows 10–25% (1,270) ·
3 rows 25–50% (298) · 7 rows 50–100% (598) · **26 rows 100–150% (2,869)** ·
**23 rows 150%+ (3,404)**.

### By pathway — total and mean

| pathway | rows | moved | today | VAR A | VAR B | A delta | B delta | A % | B % | mean/row A | mean/row B |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RD | 66 | 14 | 45,676 | 45,950 | 47,480 | +274 | **+1,804** | +0.60% | +3.95% | +4.2 | +27.3 |
| SSP | 28 | 6 | 10,856 | 11,560 | 12,046 | +704 | **+1,190** | +6.49% | +10.96% | +25.1 | +42.5 |
| MSD | 63 | 21 | 35,223 | 36,098 | 38,277 | +875 | **+3,054** | +2.48% | +8.67% | +13.9 | +48.5 |
| IRE | 14 | 7 | 719 | 810 | 1,292 | +91 | +573 | +12.66% | **+79.69%** | +6.5 | +40.9 |
| PDA | 15 | 3 | 8,081 | 8,137 | 8,422 | +56 | +341 | +0.69% | +4.22% | +3.7 | +22.7 |
| PDN | 16 | 10 | 2,651 | 2,817 | 3,211 | +166 | +560 | +6.26% | **+21.12%** | +10.4 | +35.0 |
| PDS | 0 | 0 | — | — | — | — | — | — | — | — | — |
| UNR | 13 | 8 | 1,259 | 1,339 | 1,639 | +80 | +380 | +6.35% | **+30.18%** | +6.2 | +29.2 |
| ND>64 | 28 | 6 | 18,778 | 18,838 | 19,343 | +60 | +565 | +0.32% | +3.01% | +2.1 | +20.2 |
| **ND 1-64** | **561** | **0** | **622,645** | **622,645** | **622,645** | **0** | **0** | **+0.000%** | **+0.000%** | 0 | 0 |
| **ALL POOL** | **243** | **75** | **123,243** | **125,549** | **131,710** | **+2,306** | **+8,467** | **+1.871%** | **+6.870%** | +9.5 | +34.8 |

**PDS has zero rows on the live board.** Every PDS figure elsewhere in this act is a historical-cell
figure and moves no live value.

The **biggest cash effect is MSD (+3,054) and RD (+1,804)** — the two largest pool arms. The biggest
**proportional** effect is IRE (+79.7%), UNR (+30.2%), PDN (+21.1%) — the small, heavily-sitting arms.

### Every pool player on the live board whose value changes

Sorted by absolute move under variant B. `g26` = games played in 2026 so far; `d` = sit-out depth in
seasons, `q` = he has a qualifying season on the record.

| player | pathway | age | g26 | d | TODAY | VAR A | VAR B | A move | B move | A % | B % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Nicholas Martin | SSP | 25 | 0 | q | 2,828 | 3,517 | 3,517 | +689 | +689 | +24.36% | +24.36% |
| Oliver Griffin | MSD | 19 | 0 | 1 | 39 | 172 | 286 | +133 | +247 | +341.03% | **+633.33%** |
| Max Beattie | MSD | 23 | 0 | 1 | 39 | 172 | 286 | +133 | +247 | +341.03% | **+633.33%** |
| Caleb May | MSD | 21 | 0 | 1 | 52 | 231 | 286 | +179 | +234 | +344.23% | +450.00% |
| Max Mapley | MSD | 21 | 0 | 1 | 52 | 231 | 286 | +179 | +234 | +344.23% | +450.00% |
| Harrison Coe | MSD | 27 | 0 | 1 | 52 | 231 | 286 | +179 | +234 | +344.23% | +450.00% |
| Xavier Walsh | RD | 21 | 0 | 3 | 86 | 107 | 300 | +21 | +214 | +24.42% | +248.84% |
| Luker Kentfield | MSD | 21 | 3 | 3 | 179 | 179 | 375 | 0 | +196 | +0.00% | +109.50% |
| Iliro Smit | MSD | 21 | 0 | 3 | 100 | 170 | 286 | +70 | +186 | +70.00% | +186.00% |
| Luke Beecken | MSD | 25 | 0 | 3 | 100 | 100 | 286 | 0 | +186 | +0.00% | +186.00% |
| Jack Henderson | SSP | 27 | 0 | 2 | 88 | 103 | 252 | +15 | +164 | +17.05% | +186.36% |
| Hudson O'Keeffe | SSP | 22 | 3 | 4 | 143 | 143 | 306 | 0 | +163 | +0.00% | +113.99% |
| Noah Howes | MSD | 21 | 1 | 2 | 128 | 128 | 289 | 0 | +161 | +0.00% | +125.78% |
| Harry Charleson | RD | 20 | 0 | 2 | 86 | 100 | 246 | +14 | +160 | +16.28% | +186.05% |
| Zac Walker | MSD | 20 | 0 | 2 | 128 | 128 | 286 | 0 | +158 | +0.00% | +123.44% |
| Riley Onley | RD | 19 | 0 | 1 | 143 | 177 | 294 | +34 | +151 | +23.78% | +105.59% |
| Fred Rodriguez | RD | 19 | 0 | 1 | 143 | 177 | 294 | +34 | +151 | +23.78% | +105.59% |
| Max Ramsden | MSD | 23 | 2 | 5 | 115 | 115 | 266 | 0 | +151 | +0.00% | +131.30% |
| Nick Driscoll | RD | 19 | 0 | 1 | 143 | 177 | 294 | +34 | +151 | +23.78% | +105.59% |
| Asher Eastham | RD | 20 | 0 | 2 | 81 | 94 | 231 | +13 | +150 | +16.05% | +185.19% |
| Joe Pike | RD | 21 | 0 | 2 | 140 | 174 | 282 | +34 | +142 | +24.29% | +101.43% |
| Aiden Riddle | RD | 21 | 0 | 2 | 140 | 174 | 282 | +34 | +142 | +24.29% | +101.43% |
| Nathan Wardius | PDA | 22 | 0 | 3 | 54 | 67 | 194 | +13 | +140 | +24.07% | +259.26% |
| Caleb Lewis | MSD | 23 | 2 | 2 | 128 | 128 | 267 | 0 | +139 | +0.00% | +108.59% |
| Jacob Newton | MSD | 20 | 3 | 2 | 156 | 156 | 286 | 0 | +130 | +0.00% | +83.33% |
| Lennox Hoffman | ND>64 | 20 | 0 | 2 | 65 | 75 | 185 | +10 | +120 | +15.38% | +184.62% |
| Tom Cochrane | RD | 20 | 3 | 2 | 146 | 146 | 266 | 0 | +120 | +0.00% | +82.19% |
| Keighton Matofai-Forbes | ND>64 | 20 | 0 | 2 | 65 | 75 | 185 | +10 | +120 | +15.38% | +184.62% |
| River Stevens | ND>64 | 20 | 0 | 2 | 65 | 75 | 185 | +10 | +120 | +15.38% | +184.62% |
| Leon Kickett | RD | 20 | 0 | 1 | 112 | 139 | 231 | +27 | +119 | +24.11% | +106.25% |
| Harrison Ramm | MSD | 20 | 4 | 2 | 320 | 320 | 438 | 0 | +118 | +0.00% | +36.88% |
| Vigo Visentini | RD | 21 | 1 | 3 | 167 | 167 | 282 | 0 | +115 | +0.00% | +68.86% |
| Noah Chamberlain | PDA | 19 | 0 | 1 | 87 | 106 | 194 | +19 | +107 | +21.84% | +122.99% |
| Ben Jepson | SSP | 25 | 4 | 2 | 88 | 88 | 195 | 0 | +107 | +0.00% | +121.59% |
| Aidan Johnson | ND>64 | 26 | 1 | 2 | 81 | 81 | 185 | 0 | +104 | +0.00% | +128.40% |
| Rob Monahan | IRE | 22 | 0 | 3 | 37 | 47 | 133 | +10 | +96 | +27.03% | +259.46% |
| Logan Smith | ND>64 | 20 | 0 | 2 | 91 | 114 | 185 | +23 | +94 | +25.27% | +103.30% |
| Liam Hetherton | PDA | 19 | 0 | 1 | 100 | 124 | 194 | +24 | +94 | +24.00% | +94.00% |
| Mitch Podhajski | MSD | 27 | 2 | 1 | 195 | 195 | 285 | 0 | +90 | +0.00% | +46.15% |
| Lukas Cooke | MSD | 23 | 2 | 1 | 182 | 182 | 272 | 0 | +90 | +0.00% | +49.45% |
| Ollie Greeves | RD | 19 | 4 | 1 | 421 | 421 | 509 | 0 | +88 | +0.00% | +20.90% |
| Cillian Burke | IRE | 23 | 0 | 2 | 47 | 54 | 133 | +7 | +86 | +14.89% | +182.98% |
| Matt Duffy | IRE | 22 | 0 | 2 | 47 | 54 | 133 | +7 | +86 | +14.89% | +182.98% |
| Eamonn Armstrong | IRE | 20 | 0 | 2 | 47 | 54 | 133 | +7 | +86 | +14.89% | +182.98% |
| Ricky Mentha | PDN | 20 | 0 | 2 | 43 | 50 | 123 | +7 | +80 | +16.28% | +186.05% |
| Benny Barrett | PDN | 20 | 0 | 2 | 43 | 50 | 123 | +7 | +80 | +16.28% | +186.05% |
| Oliver Francou | MSD | 20 | 4 | 1 | 345 | 345 | 418 | 0 | +73 | +0.00% | +21.16% |
| Kobe McDonald | IRE | 19 | 0 | 1 | 60 | 80 | 133 | +20 | +73 | +33.33% | +121.67% |
| Ben Murphy | IRE | 19 | 0 | 1 | 60 | 80 | 133 | +20 | +73 | +33.33% | +121.67% |
| Cillian Bourke | IRE | 20 | 0 | 1 | 60 | 80 | 133 | +20 | +73 | +33.33% | +121.67% |
| Liam Reidy | RD | 26 | 4 | 4 | 328 | 328 | 400 | 0 | +72 | +0.00% | +21.95% |
| Zak Evans | UNR | 26 | 0 | 2 | 36 | 42 | 103 | +6 | +67 | +16.67% | +186.11% |
| Jacob Moss | UNR | 22 | 0 | 2 | 36 | 45 | 103 | +9 | +67 | +25.00% | +186.11% |
| Jaxon Artemis | MSD | 20 | 4 | 1 | 305 | 305 | 370 | 0 | +65 | +0.00% | +21.31% |
| Josh Draper | PDN | 22 | 0 | q | 274 | 338 | 338 | +64 | +64 | +23.36% | +23.36% |
| Toby Whan | PDN | 19 | 0 | 1 | 60 | 74 | 123 | +14 | +63 | +23.33% | +105.00% |
| Ryda Luke | PDN | 19 | 0 | 1 | 60 | 74 | 123 | +14 | +63 | +23.33% | +105.00% |
| Jai Saxena | PDN | 19 | 0 | 1 | 60 | 74 | 123 | +14 | +63 | +23.33% | +105.00% |
| Jesse Mellor | PDN | 19 | 0 | 1 | 60 | 74 | 123 | +14 | +63 | +23.33% | +105.00% |
| Alex Van Wyk | MSD | 22 | 1 | 1 | 233 | 233 | 290 | 0 | +57 | +0.00% | +24.46% |
| Oscar Berry | UNR | 24 | 0 | 1 | 47 | 70 | 103 | +23 | +56 | +48.94% | +119.15% |
| Flynn Riley | MSD | 22 | 1 | 1 | 232 | 232 | 288 | 0 | +56 | +0.00% | +24.14% |
| Balyn O'Brien | SSP | 19 | 4 | 1 | 263 | 263 | 319 | 0 | +56 | +0.00% | +21.29% |
| Kalani White | PDN | 19 | 0 | 1 | 67 | 85 | 123 | +18 | +56 | +26.87% | +83.58% |
| Indy Cotton | UNR | 19 | 0 | 1 | 49 | 62 | 103 | +13 | +54 | +26.53% | +110.20% |
| Jaime Uhr-Henry | UNR | 23 | 0 | 2 | 51 | 64 | 103 | +13 | +52 | +25.49% | +101.96% |
| Matt Hill | UNR | 22 | 2 | 2 | 48 | 48 | 95 | 0 | +47 | +0.00% | +97.92% |
| Patrick Carr | UNR | 21 | 0 | 1 | 67 | 83 | 103 | +16 | +36 | +23.88% | +53.73% |
| Tyson Stengle | RD | 28 | 0 | q | 121 | 150 | 150 | +29 | +29 | +23.97% | +23.97% |
| Tyrell Dewar | PDN | 22 | 0 | q | 68 | 82 | 82 | +14 | +14 | +20.59% | +20.59% |
| Jayden Nguyen | PDN | 20 | 5 | 2 | 429 | 429 | 443 | 0 | +14 | +0.00% | +3.26% |
| Thomas Burton | SSP | 19 | 5 | 1 | 305 | 305 | 316 | 0 | +11 | +0.00% | +3.61% |
| Caleb Graham | ND>64 | 26 | 0 | q | 38 | 45 | 45 | +7 | +7 | +18.42% | +18.42% |
| Robert Hansen | MSD | 22 | 0 | q | 80 | 82 | 82 | +2 | +2 | +2.50% | +2.50% |
| Wil Parker | UNR | 24 | 5 | 3 | 29 | 29 | 30 | 0 | +1 | +0.00% | +3.45% |
| **TOTAL (moved rows)** | | | | | **11,663** | **13,969** | **20,130** | **+2,306** | **+8,467** | | |

**Read the `d` column against the moves.** The lift is worth most to the players sitting **deepest**
and priced **lowest**. The 26 rows that move under B but not under A (`A move = 0`) are exactly the
rows the H leg cannot reach — see the structural finding below.

### A structural finding the two legs force into the open

**The "pool sitter penalty" is not one population. It is two, and they do not coincide.**

- `_h_cut`'s sitter test (`:2043`) is **`games this season <= 0`** — a hard zero.
- `sitout_ev` is reached only when `ns = nseas_pro(p,Y) == 0` (`ev():2262`), i.e. **the player has
  never had a qualifying season at pace** — and at `SEASON_PROG = 0.58` the in-progress bar is
  `6 × 0.58 = 3.48` games, so a player with 1–3 games in 2026 is still on that path.

Consequences, both measured on the live board:

1. **26 rows with games this season move under B and not under A** (Luker Kentfield 3 games, Hudson
   O'Keeffe 3, Jacob Newton 3, Harrison Ramm 4, Ollie Greeves 4 …). They pay the R leg but not the H
   leg, so lifting H alone does nothing for them.
2. **6 rows marked `q` move under A and B identically** (Nicholas Martin, Josh Draper, Tyson Stengle,
   Tyrell Dewar, Caleb Graham, Robert Hansen). They are established players sitting out this season:
   they take the **year-1+** arm (`ns >= 1`), where `_h_cut` still fires but `sitout_ev` never does.
   Nicholas Martin alone is **+689 points, 30% of the entire variant-A effect**, and he is not a
   "sitter" in the sit-out-machinery sense at all — he is an established SSP player who has not
   played in 2026.

**This contradicted a code fact this seat declared in the pre-registration (F2) and it is owned in
full in the breach section below.**

---

## 2. THE PER-PATHWAY MEAN-PRESERVING FIGURE

Entry-weighted mean of the applied sitter multiplier over the pathway's complete-window cells
(`Y <= 2021`), on ORDER 18's cell construction, which is phase 1's, carried verbatim.
`mean < 1.0` is a **net charge** and a breach of the owner's D8 mean-preserving law.

| pathway | cells | sitters | sit share (wtd) | **TODAY** | net charge | **VAR A** | net charge | **VAR B** | net charge |
|---|---|---|---|---|---|---|---|---|---|
| RD | 2352 | 832 | 0.3527 | 0.789801 | −0.210199 | 0.832482 | −0.167518 | **1.000000** | **0.000000** |
| SSP | 34 | 13 | 0.3824 | 0.793576 | −0.206424 | 0.850059 | −0.149941 | **1.000000** | **0.000000** |
| MSD | 40 | 34 | 0.8500 | 0.262104 | −0.737896 | 0.647975 | −0.352025 | **1.000000** | **0.000000** |
| IRE | 137 | 70 | 0.5109 | 0.547311 | −0.452689 | 0.747847 | −0.252153 | **1.000000** | **0.000000** |
| PDA | 106 | 53 | 0.5000 | 0.693845 | −0.306155 | 0.753538 | −0.246462 | **1.000000** | **0.000000** |
| PDN | 36 | 29 | 0.8056 | 0.513917 | −0.486083 | 0.602778 | −0.397222 | **1.000000** | **0.000000** |
| PDS | 62 | 36 | 0.5806 | 0.643645 | −0.356355 | 0.698323 | −0.301677 | **1.000000** | **0.000000** |
| UNR | 126 | 65 | 0.5159 | 0.670915 | −0.329085 | 0.798548 | −0.201452 | **1.000000** | **0.000000** |
| ND>64 | 441 | 193 | 0.4376 | 0.727445 | −0.272555 | 0.776882 | −0.223118 | **1.000000** | **0.000000** |
| **ALL POOL** | **3334** | **1325** | **0.3845** | **0.762329** | **−0.237671** | **0.816779** | **−0.183221** | **1.000000** | **0.000000** |
| **ND 1-64** | 6662 | 1385 | 0.1394 | 0.938846 | −0.061154 | *untouched (ruled)* | | *untouched (ruled)* | |

**Where it lands.**

- **Today**: pool pathways span **0.2621 (MSD)** to **0.7936 (SSP)**; pooled **0.762329**.
- **Variant A**: they span **0.6028 (PDN)** to **0.8501 (SSP)**; pooled **0.816779**. It moves toward
  1.0 and **does not get there** — lifting H alone leaves **every one of the nine pathways still in
  breach on the surviving R leg**, worse than the national arm's −6.12%.
- **Variant B**: every pool pathway lands at **exactly 1.000000**. The law holds, by construction,
  because the whole pool differential is gone.

Cross-check: variant A reproduces ORDER 18's published **R-leg-only** column to max abs delta
**0.000048**, which is the 4-decimal rounding of that published column and nothing else.

---

## 3. THE v0 QUESTION — ANSWERED FROM THE CODE, AND PROVED BY EXECUTION

> "How much would that change values of the pool and **the v0 of them**?"

### **THE SITTER PENALTY DOES NOT REACH v0 AT ALL. LIFTING IT CHANGES NO PLAYER'S v0 BY ANY AMOUNT, ON EITHER LEG, IN EITHER VARIANT. THE DELTA IS EXACTLY ZERO, NOT MERELY SMALL.**

Three independent proofs, all by execution, none by assertion.

**PROOF 1 — the full-engine proof.** Three complete 24-year walk-forward emits, one per variant, each
writing every entrant's own `v0 = v0_start(p)` under *that* engine:

| quantity | value |
|---|---|
| records | 2,645 (of which **1,201 pool**) |
| `max abs( v0(VARIANT A) − v0(SHIP) )`, all rows | **0** |
| `max abs( v0(VARIANT B) − v0(SHIP) )`, all rows | **0** |
| same, pool rows only | **0** and **0** |
| records whose **walk-forward priced path** did change | **884 (A)**, **1,022 (B)** |

The instrument is plainly sensitive — nearly 40% of careers reprice — and `v0` still does not move by
one float bit.

**PROOF 2 — the call-graph proof by execution.** `_h_cut` and `sitout_ev` were wrapped with counters
in the staged engine, then the whole v0 chain was called for all **1,202** pool players:

| calls during | `_h_cut` | `sitout_ev` |
|---|---|---|
| `_v0_uncapped` + `_v0_raw` + `v0_start` + `entry_anchor` + `raw_ev(p, debutyr-1)` | **0** | **0** |
| 60 calls to `ev(p, 2026)` on the same players | **109** | **70** |

The counters are live and they fire at `ev()`. They never fire on the v0 chain.

**PROOF 3 — the in-process perturbation.** `H_POOLSIT = H_UNION = 1.0` and `_R_surf` pool-gated to
1.0 in the staged engine, v0 caches cleared, whole chain recomputed for all 1,202 pool rows:

| function | max abs delta |
|---|---|
| `_v0_uncapped` | **0** |
| `_v0_raw` | **0** |
| `v0_start` | **0** |
| `entry_anchor` | **0** |

**The mechanism, so the verdict is understood and not just believed.**

```
_v0_uncapped(p) = raw_ev(p, debutyr-1) * iso_eff(p, debutyr-1)     :1228-1238
_v0_raw(p)      = _ruc_prior_cap(p, _v0_uncapped(p))               :1239-1241
v0_start(p)     = _V0CURVE[key]  on the board path                 :1756-1760
entry_anchor(p) = pool_level(p)*_PL_F*_b_factor(p)  for a pool row  :1852-1857
```

Not one of those reads `H_POOLSIT`, `H_UNION` or `_R_surf`. `_h_cut` (`:2037`) and `sitout_ev`
(`:1961`) are both applied **inside `ev()`** (`:2228-2277`); `raw_ev` is a different function
(`:1061`). The engine says so itself at `:1999`: *"this runs at ev(), NEVER inside raw_ev —
`_v0_uncapped` calls `raw_ev` at Y=debutyr-1 to BUILD the very year-0 prior being borrowed."*

**What the owner should take from this.** Lifting the pool sitter penalty changes what a pool player
is **worth today**. It does not change what he **entered at**. v0 and the signed division levels are
a separate object and a separate lever — **the two do not overlap at the v0 site.**

**But they are not independent downstream. See section 4.**

---

## 4. THE DERIVED-LEVEL INTERACTION — **THEY DO CHANGE**

> Does the phase-1 profile measure (`realised_full / v0`) read H or R at all?

### **YES — IT READS BOTH, THROUGH THE NUMERATOR. THE DERIVED POOL ENTRY LEVELS DO CHANGE.**

The mechanism, from the code before the numbers:

```
profile_X      = SUM_X structural_value / SUM_X v0        phase1_derive.py:87-90
structural_val ← harness.realised_full(r)                 harness:311-315
realised_full  = realised_at(r, len(vpath))               harness:298-309
               = an evidence-weighted mean of r['vpath']
vpath[i]       = ev(p, C+1+i) — THE ENGINE'S OWN AS-OF PRICE   emitter:137-138,166
```

A sit-out season's as-of price is **exactly** where R and H are applied. The **numerator** of the
profile carries the sitter penalty; the **denominator** (`v0`) does not. So lifting the penalty raises
measured pool returns and raises every derived level.

Proved by re-running **phase 1's own `phase1_derive.py`** (carried unmodified from
`build/pool-repricing-phase1`, which this act does not touch) against each variant's matrix. Its
re-run on SHIP reproduces the committed `PHASE1_DERIVE.json` **exactly** (control 4).

| pathway | n | profile NOW | profile A | profile B | **λ NOW** | **λ A** | **λ B** | A rel | B rel |
|---|---|---|---|---|---|---|---|---|---|
| RD | 688 | 0.5233 | 0.5269 | 0.5509 | 0.5104 | 0.5141 | 0.5384 | +0.71% | **+5.48%** |
| SSP | 52 | 1.0287 | 1.0499 | 1.0695 | 1.0034 | 1.0243 | 1.0453 | +2.09% | +4.17% |
| MSD | 106 | 0.9418 | 0.9422 | 0.9599 | 0.9187 | 0.9192 | 0.9381 | +0.06% | +2.12% |
| IRE | 57 | 0.2006 | 0.2142 | 0.2285 | 0.1956 | 0.2090 | 0.2233 | +6.82% | **+14.13%** |
| PDA | 51 | 0.4279 | 0.4329 | 0.4725 | 0.4174 | 0.4224 | 0.4618 | +1.19% | **+10.63%** |
| PDN | 43 | 0.1422 | 0.1448 | 0.1633 | 0.1387 | 0.1413 | 0.1596 | +1.83% | **+15.04%** |
| PDS | 21 | 0.1259 | 0.1287 | 0.1556 | 0.2837 | 0.2871 | 0.3123 | +1.20% | **+10.11%** |
| UNR | 59 | 0.3493 | 0.3546 | 0.3673 | 0.3408 | 0.3460 | 0.3590 | +1.53% | +5.34% |
| ND>64 | 120 | 0.5477 | 0.5511 | 0.5736 | 0.5342 | 0.5377 | 0.5606 | +0.64% | +4.93% |

ALL-POOL profile: **0.521756 → 0.526011 (A) → 0.549172 (B)**.
Entry-weighted mean derived level moves **+0.835% (A)** and **+5.426% (B)**.

### **THE ORDER OF OPERATIONS MATTERS, AND THIS IS THE FINDING THE OWNER SHOULD ACT ON**

The pool **repricing** (phase 1) and the pool **sitter lift** are **not independent**. The repricing
derives entry levels from measured pool returns, and those returns are recorded **net of the sitter
penalty**. Derive the levels first and lift the penalty second, and **the levels are taught on a
charge that no longer exists** — every pool level would be set 2% to 15% too low. The two acts have
to be sequenced, or the repricing re-derived after the lift. **That is a design ruling and is not
made here.**

### A cross-arm contamination, reported because it was measured

`nd_profile` — **the calibration target every λ is measured against** — moves:
**1.025217711 (today) → 1.024988839 (A, −0.0223%) → 1.023229369 (B, −0.1939%)**.

It should not have. **No national row's own price moves** (verified: 1 of 1,444 non-pool records,
named below). It moves because `structural_values()` builds its career-**completion** strata
`S[(pos,t)]` over the **whole eligible cohort — pool rows included** (`harness:337-350`;
`phase1_derive.py:79-80` passes `elig`, which is pool + national). A live ND career is completed with
a ratio taught partly by pool careers, so moving pool prices moves ND's completed values. **Small
(−0.19%), but not zero and not noise. It is a property of phase 1's measure, not of the lift.**

**The one non-pool record whose price does move, named:** `daniel-butler`. He is the **#338 Q-B slide
crosser** the emitter itself already tracks (`emit_matrix_338.py:298 crossers`): the **engine** prices
him as a pool row (`effpk 65`, `_pool True`) so the lift reaches him, while the **matrix** records his
*slid* pick as 64 and therefore admits him to the national teaching population. He is 1 row of 1,197
and he is the entire reason the "no national row moves" statement needs a footnote at all.

---

## 5. THE COHORT INSTRUMENTS

Convention carried unchanged from `menu_table.py:126-141`: **a negative margin is free money** (the
book grows faster than the engine discounts, so holding dominates). The order names **14%**, so 14.00%
is the bar; the shipped ladder's own 13.00% rate at draft age 18 is printed beside it, not instead.

### 5a. All-arm cohort — the owner's ruled cohort, THE DECIDING INSTRUMENT

`noarb_table_allarm.py`, canonical `noarb_table_338.py` md5 `0f8220351c64c56ccfa90c60edcdfa5f`
asserted at run.

**PRIMARY, cohorts 2005-2023, n = 2209**

| variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | vs 13% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| TODAY | 1.0000 | 0.8850 | 1.1051 | 1.2113 | 1.2859 | 1.2685 | −11.50% | **+25.50%** | +24.50% | no arb |
| VARIANT A | 1.0000 | 0.8977 | 1.1104 | 1.2121 | 1.2873 | 1.2699 | −10.23% | **+24.23%** | +23.23% | no arb |
| VARIANT B | 1.0000 | 0.9503 | 1.1795 | 1.2254 | 1.2930 | 1.2733 | −4.97% | **+18.97%** | +17.97% | no arb |

yr1 ratio moves **+0.0127 (A)** and **+0.0653 (B)**.

**MODERN, cohorts 2019-2023, n = 540**

| variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | vs 13% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| TODAY | 1.0000 | 0.8862 | 1.0340 | 1.0932 | 1.0985 | 1.1690 | −11.38% | **+25.38%** | +24.38% | no arb |
| VARIANT A | 1.0000 | 0.8956 | 1.0382 | 1.0937 | 1.0990 | 1.1719 | −10.44% | **+24.44%** | +23.44% | no arb |
| VARIANT B | 1.0000 | 0.9310 | 1.0978 | 1.1040 | 1.1024 | 1.1737 | −6.90% | **+20.90%** | +19.90% | no arb |

**The lift closes the year-1 hole and does not open an arbitrage.** The margin narrows by 6.5 points
under the full lift and remains comfortably positive at +18.97%. The year-1 dip (0.885 today) is the
long-standing envelope defect; the full lift takes it to 0.950 — the largest single move on that
number this act has seen — without approaching the no-arb bound.

**By arm, PRIMARY window** (pooled ratio within the arm):

| arm | n | yr1 NOW | yr1 A | yr1 B | yr4 NOW | yr4 A | yr4 B |
|---|---|---|---|---|---|---|---|
| ND | 1310 | 1.0447 | 1.0463 | 1.0539 | 1.5166 | 1.5170 | 1.5183 |
| RD | 620 | 0.4806 | 0.5218 | **0.7002** | 0.7214 | 0.7225 | 0.7377 |
| MSD | 55 | nan | nan | nan | 0.9485 | 0.9549 | 0.9937 |
| UNR | 49 | 0.3276 | 0.4087 | **0.5456** | 0.7672 | 0.7679 | 0.7918 |
| IRE | 47 | 0.2537 | 0.2904 | **0.4328** | 0.2628 | 0.3166 | 0.3310 |
| PDA | 43 | 0.3681 | 0.4116 | **0.5914** | 0.7709 | 0.7719 | 0.7956 |
| PDN | 33 | 0.1475 | 0.1775 | **0.3094** | 0.2575 | 0.2635 | 0.2635 |
| SSP | 31 | 1.2499 | 1.3031 | **1.4753** | 1.3507 | 1.3507 | 1.3691 |
| PDS | 21 | 0.2165 | 0.2496 | **0.3782** | 0.1694 | 0.1727 | 0.2162 |

The ND row moves only through the `daniel-butler` crosser and the shared strata; its own prices are
untouched. **Year 1 is where the whole effect lives** — the pool arms roughly double their year-1
delivery under the full lift; year 4 barely moves, because by then production leads and the anchor is
already faded out.

### 5b. Legacy picks 1-64 — `noarb_table_338.py`, UNMODIFIED

Population = `teaches_curve & pick 1..64 & draft year 2004-2022`, n = 1197.

| variant | yr0 | yr1 | yr2 | yr3 | yr4 | yr5 | apprec 0→1 | **margin vs 14%** | vs 13% | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| TODAY | 1.0000 | 1.0884 | 1.3586 | 1.4941 | 1.5660 | 1.5500 | +8.84% | **+5.16%** | +4.16% | no arb |
| VARIANT A | 1.0000 | 1.0884 | 1.3586 | 1.4941 | 1.5660 | 1.5500 | +8.84% | **+5.16%** | +4.16% | no arb |
| VARIANT B | 1.0000 | 1.0885 | 1.3587 | 1.4941 | 1.5660 | 1.5500 | +8.85% | **+5.15%** | +4.15% | no arb |

The legacy instrument is **essentially inert** — its population is national by construction, so a pool
lift has nothing to act on. It is **not exactly** inert: yr1 moves **+0.0001** under variant B, and
that entire move is the one `daniel-butler` row.

---

## 6. THE OWNER'S OWN CONCERN, MEASURED

> "given more pool players sit, if we keep it for them it will destroy their values"

**The premise holds on every pathway, on both weightings, without exception.**

Complete-window cells; a cell is a sit-out if the player has no season of ≥6 games up to that year.

| pathway | cells | sitters | share (count) | share (entry-wtd) | vs ND (count) | **vs ND (wtd)** |
|---|---|---|---|---|---|---|
| RD | 2352 | 832 | 0.3537 | 0.3527 | 1.70x | **2.53x** |
| SSP | 34 | 13 | 0.3824 | 0.3824 | 1.84x | 2.74x |
| MSD | 40 | 34 | **0.8500** | **0.8500** | 4.09x | **6.10x** |
| IRE | 137 | 70 | 0.5109 | 0.5109 | 2.46x | 3.67x |
| PDA | 106 | 53 | 0.5000 | 0.5000 | 2.41x | 3.59x |
| PDN | 36 | 29 | **0.8056** | **0.8056** | 3.87x | **5.78x** |
| PDS | 62 | 36 | 0.5806 | 0.5806 | 2.79x | 4.17x |
| UNR | 126 | 65 | 0.5159 | 0.5159 | 2.48x | 3.70x |
| ND>64 | 441 | 193 | 0.4376 | 0.4376 | 2.11x | 3.14x |
| **ALL POOL** | **3334** | **1325** | **0.3974** | **0.3845** | **1.91x** | **2.76x** |
| **ND 1-64** | 6662 | 1385 | 0.2079 | 0.1394 | 1.00x | 1.00x |

**Pathways at or below ND 1-64: NONE, on either weighting.** Pooled, a pool entrant sits **1.91x** as
often as a national 1-64 pick by count and **2.76x** as often by entry weight.

The entry-weighted gap is the larger of the two, and that is the mechanism the owner's sentence is
describing: on the national arm the expensive picks almost never sit (pick 1-10 sitter share 0.058),
so the harsh multiplier lands on cheap rows. **In the pool there is no such shelter — the pool index
is a single constant (`POOL_PICK = 65`), so every pool entrant draws the same knot-50 retention column
and the charge lands on the whole arm at full weight.**

**And on the live board today (2026, zero games so far this season):**

| pathway | rows | sit-outs | share | value sitting | share of pathway value |
|---|---|---|---|---|---|
| RD | 66 | 11 | 0.1667 | 1,206 | 0.0264 |
| SSP | 28 | 2 | 0.0714 | 2,916 | 0.2686 |
| MSD | 63 | 11 | 0.1746 | 830 | 0.0236 |
| IRE | 14 | 7 | **0.5000** | 358 | **0.4979** |
| PDA | 15 | 3 | 0.2000 | 241 | 0.0298 |
| PDN | 16 | 9 | **0.5625** | 735 | **0.2773** |
| UNR | 13 | 6 | **0.4615** | 286 | **0.2272** |
| ND>64 | 28 | 6 | 0.2143 | 334 | 0.0178 |
| **ALL POOL** | **243** | **55** | **0.2263** | **6,906** | **0.0560** |
| ND 1-64 | 561 | 87 | 0.1551 | 27,822 | 0.0447 |

---

## 7. THE SECOND R SITE — A DISCLOSED SENSITIVITY, NOT PART OF EITHER VARIANT

The order defines the R leg as `anch = R * entry_anchor(p)` **inside `sitout_ev`**, and variant B is
scoped to exactly that. But `_merged_recover.py:2178` reads the **same retention surface a second
time**, in `_a_blend`, on the year-1+ arm: `anch0 = R * entry_anchor(p)`. A pool player who has ever
had a qualifying season takes *that* site and never `sitout_ev` — variant B does not reach him.

A board with **both** R sites lifted for pool rows was built so the residue is sized, not guessed:

| | board total | change | change % | rows moved |
|---|---|---|---|---|
| TODAY (shipped) | 745,888 | — | — | — |
| VARIANT A (H only) | 748,194 | +2,306 | +0.309% | 49 |
| **VARIANT B (H + R at `sitout_ev`)** | **754,355** | **+8,467** | **+1.135%** | **75** |
| *sensitivity* (H + R at **both** sites) | 754,977 | +9,089 | +1.219% | 88 |

**The second site adds 19 further rows worth 622 points — 7.3% on top of variant B.** Zero of them
are national 1-64 rows (the patch is pool-gated at both sites). Largest: Mani Liddy MSD +127,
Robert Hansen MSD +112, James Blanck MSD +55, Andy Moniz-Wakefield PDN +49, Darragh Joyce IRE +40.
**This is reported, not folded in. Whether the R leg should be lifted at one site or two is a design
question the order did not put and this seat does not answer.**

---

## 8. PRE-REGISTRATION BREACHES — OWNED, NOT HIDDEN

**Six of sixteen predictions breached, one partially — plus one declared CODE FACT that was simply
wrong, which is the more serious of the two categories and is listed first.**

### The declared code fact that was wrong

**F2, as written in `PREREG_ORDER19.md`:** *"`sitout_ev` is reached from `ev()` only at `ns==0`.
`_h_cut` is applied at the same site. So **both legs bite only on sit-out rows**; the two variants
cannot move a pool row that played this season through these sites."*

**Both halves of the conclusion are false, measured.** `_h_cut` is also applied on the **year-1+**
arm (`ev():2263`), and its sitter test is `games this season <= 0` — not `ns == 0`. Meanwhile
`sitout_ev`'s gate `ns = nseas_pro(p,Y) == 0` admits rows that **have** played this season, because
the in-progress qualification bar is `6 × SEASON_PROG = 3.48` games. Measured consequence: **26 live
board rows that played 1–5 games in 2026 move under variant B**, and **6 rows move identically under A
and B because they take the year-1+ arm where only H fires** — including Nicholas Martin, who is 30%
of variant A's entire effect. This was stated as settled code, not as a forecast, and it was wrong.
It is the reason P1, P3 and P5 all missed in the same direction.

### The predictions

| # | quantity | predicted | measured | result |
|---|---|---|---|---|
| P1 | rows moved, variant A | 12 – 45 | **49** | **BREACH** — above band |
| P2 | board total change, A | +0.20% – +1.20% | +0.309% | ✓ |
| P3 | B moves exactly A's row set | TRUE | **A ⊂ B; B\A = 26 rows** | **BREACH** |
| P4 | board total change, B | +0.80% – +4.00%, ≥2.5x A | +1.135%, **3.67x A** | ✓ |
| P5 | largest single mover under B | +90% – +250% | **+633.33%** (Oliver Griffin, Max Beattie) | **BREACH** — far above band |
| P6 | A reproduces ORDER 18's R-only column, max delta < 1e-6 | < 1e-6 | **4.8e-5** | **BREACH** — the band was ill-posed: ORDER 18's column is published to 4 dp, so 5e-5 is the floor rounding alone can achieve. The reproduction is exact to the published precision |
| P7 | B's per-pathway figure | exactly 1.000000 on all nine | **1.000000 on all nine** | ✓ |
| P8 | v0 delta | < 1e-12 relative | **exactly 0** | ✓ — stronger |
| P9 | derived levels change | TRUE | TRUE, +2.1% to +15.0% | ✓ |
| P10 | `nd_profile` unchanged to < 1e-9 rel | TRUE | **−0.1939% under B** | **BREACH** — and the most instructive one: phase 1's completion strata are built over pool + national together, so the calibration target is not pool-independent |
| P11 | worst pathway's λ rises +10% – +80% under B | PDN/PDS/IRE | PDN +15.04%, IRE +14.13%, PDS +10.11% | ✓ as stated — **disclosed**: MSD, which carries the *harshest* charge today (−0.7379), rises only +2.12%, outside the band. The prediction named the three pathways it did, and they held; had it said "the harshest pathway" it would have failed |
| P12 | legacy 1-64 tables byte-identical, both variants | TRUE | A identical; **B moves yr1 by +0.0001** | **PARTIAL BREACH** — one row, `daniel-butler`, the #338 slide crosser |
| P13 | all-arm PRIMARY yr1 rise under B | +0.005 – +0.060 | **+0.0653** | **BREACH** — just above band |
| P14 | no-arb margin vs 14% stays positive | TRUE | all-arm +18.97%, legacy +5.15% | ✓ |
| P15 | every pool pathway sits more than ND 1-64 | TRUE on all nine | TRUE on all nine, both weightings | ✓ |
| P16 | pooled pool sit share vs ND 1-64 | 2.0x – 4.5x | **2.76x** entry-weighted | ✓ |

**Direction of the misses.** Every quantitative breach except P6 is in the same direction: **I
under-predicted the size and reach of the lift.** More rows move than predicted (P1), a set of rows I
had ruled out moves at all (P3), the largest mover is 2.5x my ceiling (P5), and the all-arm year-1
move overshoots (P13). The single non-quantitative breach (P10) is the opposite kind of error — an
assumed independence between the two arms that the phase-1 measure does not actually have.

**None of these touches the headline answers.** The two figures the owner asked for — the size of the
lift and its effect on v0 — are P2/P4 (both confirmed) and P8 (confirmed, and stronger than predicted).

---

## 9. WHAT THIS SEAT COULD NOT DETERMINE

1. **Whether the R leg should be lifted at one site or two.** `sitout_ev` and `_a_blend` read the same
   surface. The order scopes variant B to the first. The second is sized here (+622 points, 19 rows)
   and left as a design question.
2. **Whether the levels should be re-derived after the lift, or the lift applied after the levels.**
   Section 4 proves the two interact and sizes the interaction (+5.43% entry-weighted on the derived
   levels). The sequencing is a ruling, not a measurement.
3. **Whether `nd_profile`'s −0.19% drift is acceptable, or whether phase 1's completion strata should
   be built per-arm.** This is a defect in the *measure*, surfaced by this act, and belongs to the
   phase-1 branch, which this act must not touch.
4. **Whether `daniel-butler` should be in the national teaching population at all.** The engine prices
   him as pool; the matrix teaches him as national 1-64. One row of 1,197; disclosed, not resolved.
5. **What the sitter penalty should be REBUILT as**, which the owner explicitly contemplated
   ("rebuild it again if needed afterwards"). Nothing here derives a replacement surface. The only
   thing measured is the size of removing the present one.
6. **The mid-season `tau` fraction.** The board is priced at `SEASON_PROG = 0.58`, so every live sitter
   sits at a fractional depth. The historical cell tables use integer depth (phase 1's and ORDER 18's
   mapping, carried so the three acts are comparable). The two are not reconciled here, and the live
   board figures — which are the ones the owner will read — use the engine's own fractional `tau`
   because they are actual engine builds.
