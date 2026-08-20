# PACKET — THE STAIRCASE FIX (ORDER 44), BOTH BOUNDED VARIANTS PRICED SIDE BY SIDE

**Seat:** pricing seat, THE STAIRCASE FIX · **Date:** 2026-08-20 · **Base:** `main` @ `efbe1b6` · **Prereg:** `docs/evidence/staircase_fix_2026-08-20/PREREG_STAIRCASE.md`, committed at `5f94a44` **before** the engine edit at `1446dec`
**Owner word:** "Yes, bounded fix now"

> **THIS IS A PRICING ACT. NOTHING IS ADOPTED AND NOTHING IS ASKED TO BE.** The dial ships **OFF**.
> The live board is `68be10c79d0ee096455754e084bcf757` before this act and after it. The owner
> chooses the variant; this seat does not flip the dial default and has not.

---

## 1. What changes

`engine/rl_after/_merged_recover.py` gains **one declared dial**, `RL_O44_LVLMONO`, **default OFF**, in the
kill-switch family the estate already runs (`RL_CAPT` / `RL_ISOFADE` / `RL_EVW` / `RL_O33_TAPEROFF`). Three
hunks in that one file: (1) `_b6_core`, the band READ site, where the OFF path is the two shipped lines
byte-for-byte untouched behind an `if _O44 and not suspended` guard; (2) one line at the `raw_ev` production
hook, `if _O44_CONSERVE: pr *= _O44_C.get(gfut(p), 1.0)`, the same hook and the same per-position class the
shipped `_UC_C` renorm already uses; (3) a load-time calibration block beside the `_UC_C` block it is
isomorphic to. Five accepted values — `off` / `ratchet` / `ratchet+conserve` / `smooth` / `smooth+conserve`;
anything else HALTS at import, because a dial that reads a typo as "off" is a check that produces no verdict.

**What it does.** The five pinned quantile forests plus `q97m` are piecewise-constant and carry no monotonicity
constraint on the level feature (index 9), so a player's band can step DOWN on a RISING level — the mechanism
`docs/evidence/trough_diagnosis_2026-08-20/WORKINGS_TROUGH.md` established and register v806 recorded as a LAW
3 (NO CLIFFS) violation. ORDER 44 monotonises the composed six-leg band **at the read site**, over the
forests' **own split thresholds** on that feature (2,329 of them, range 40.7489–116.2636, measured; sampled at
`knot + 1e-9` against a measured minimum gap of 7.629e-06). That sample set is **nested in the level**, so the
running maximum is non-decreasing **by construction**, with no residual to shrink. **VARIANT A** is that
ratchet. **VARIANT B** is the ratchet's plateaus replaced by linear interpolation between plateau midpoints —
parameter-free, and strictly rising wherever the ratchet rises.

**What is NOT touched, with the same precision.** `engine/forward_valuation/conditional_prior.py` is **not
edited**. `cm_400.pkl` (`34faa865`) and `data/q97m.pkl` (`cfdc7321`) are Guard-5-pinned frozen artifacts and are
**read exactly as they are** — no refit, no re-pin, no re-stamp. **This is not a bake**, and that is the whole
of what makes it bounded rather than FIX 1. `data/model_config.json` is byte-unmoved at `269d20ab`:
`RL_O44_LVLMONO` is **deliberately not a manifest dial**, so `config_manifest.enforce()` rejects it as an
unknown model override in bake/gate/canonical mode and **no certifying build can carry it** — measured, not
asserted: `config_manifest` reads PASS at hash `eed19a75` on the final tree.

**One thing this act moves that the prereg did not say it would**, disclosed rather than absorbed: the engine
file's md5 moved `1867e953 → 3f4aa10b`, and four carriers name it. Commit `1446dec` did not restamp them and
the gates went RED. Repaired at `1590a37` by the established pattern (`d8_restamp.py`, byte-carried) —
`expected_boot.engine_head`, `release_contract.identities.engine_head` (+ recomputed `contract_sha256`
`cde9f70a → 8e6dcdbc`), and the two `board_view_working.js` stamps through **both** of their writers of record.
See §8 for the two prereg corrections that repair forces.

---

## 2. Who moves — by name

**Full movers lists attached, by name, with before / after / delta / percent, for every one of the four
readings:** `MOVERS_A_RAW.json` · `MOVERS_A_CON.json` · `MOVERS_B_RAW.json` · `MOVERS_B_CON.json` (804 rows
each, `all_rows`), with their printed companions `MOVERS_*_out.txt`. The top 20 by absolute move are inline
below; the rest are in the files.

### Headline counts, against the live board `68be10c7` (total 692,296 / 804 rows)

| reading | dial | candidate board | movers | up | down | unmoved | total after | mint |
|---|---|---|---|---|---|---|---|---|
| **A raw** | `ratchet` | `b3e8da99` | 551 | 519 | 32 | **253** | 700,756 | **+8,460 SCAR (+1.222 %)** |
| **A conserved** | `ratchet+conserve` | `9c78fe09` | 615 | 280 | 335 | **189** | 688,271 | **−4,025 SCAR (−0.581 %)** |
| **B raw** | `smooth` | `219266fa` | 605 | 491 | 114 | **199** | 700,681 | **+8,385 SCAR (+1.211 %)** |
| **B conserved** | `smooth+conserve` | `f2282349` | 620 | 290 | 330 | **184** | 688,127 | **−4,169 SCAR (−0.602 %)** |

### THE FOUR NAMED PLAYERS — the rows this fix exists for

Live board → candidate, under each reading. Their measured max-drops on the raw board were
Kondogiannis 40.2 %, Dolan 27.2 %, West 34.1 %, Hayes 39.8 % (diagnosis §8).

| player | pos | live | **A raw** | **A conserved** | **B raw** | **B conserved** |
|---|---|---|---|---|---|---|
| Max Kondogiannis | SD | 359 | **409 (+13.93 %)** | **406 (+13.09 %)** | **409 (+13.93 %)** | **405 (+12.81 %)** |
| Josh Dolan | SF | 247 | **311 (+25.91 %)** | **305 (+23.48 %)** | **311 (+25.91 %)** | **305 (+23.48 %)** |
| Charlie West | KPF | 381 | **383 (+0.52 %)** | **372 (−2.36 %)** | **382 (+0.26 %)** | **372 (−2.36 %)** |
| Will Hayes (`will-hayes-b`) | SF | 180 | **250 (+38.89 %)** | **245 (+36.11 %)** | **250 (+38.89 %)** | **245 (+36.11 %)** |

Read that honestly: three of the four are repaired by a margin close to the drop the diagnosis measured.
**Charlie West barely moves under either raw variant and goes DOWN under both conserved ones** — the
renormalisation takes more off him than the monotoniser puts on. He is the row that says the conservation leg
is not free.

### Top 20 by absolute move — VARIANT A

| **A raw** (`ratchet`) | | | **A conserved** (`ratchet+conserve`) | | |
|---|---|---|---|---|---|
| Max Holmes MID | 7588 → 7742 | +154 (+2.03 %) | Luke Jackson RUCK | 9265 → 8967 | −298 (−3.22 %) |
| Nasiah Wanganeen-Milera MID | 8660 → 8805 | +145 (+1.67 %) | Josh Treacy KPF | 6179 → 5957 | −222 (−3.59 %) |
| Errol Gulden MID | 7075 → 7205 | +130 (+1.84 %) | Sam Darcy KPF | 5116 → 4967 | −149 (−2.91 %) |
| Tristan Xerri RUCK | 7024 → 7147 | +123 (+1.75 %) | Izak Rankine SF | 4819 → 4676 | −143 (−2.97 %) |
| Nick Daicos MID | 9892 → 10012 | +120 (+1.21 %) | Brodie Grundy RUCK | 4212 → 4089 | −123 (−2.92 %) |
| Ethan Read KPF | 490 → 605 | +115 (+23.47 %) | Tristan Xerri RUCK | 7024 → 6901 | −123 (−1.75 %) |
| Nate Caddy KPF | 1612 → 1726 | +114 (+7.07 %) | Riley Thilthorpe KPF | 4048 → 3929 | −119 (−2.94 %) |
| Cooper Duff-Tytler KPF | 1809 → 1921 | +112 (+6.19 %) | Murphy Reid SF | 3427 → 3311 | −116 (−3.38 %) |
| Will Ashcroft MID | 6589 → 6699 | +110 (+1.67 %) | Timothy English RUCK | 3336 → 3224 | −112 (−3.36 %) |
| Liam Fawcett KPF | 267 → 370 | +103 (+38.58 %) | Nick Watson SF | 3594 → 3488 | −106 (−2.95 %) |
| Jobe Shanahan KPF | 1298 → 1400 | +102 (+7.86 %) | Max Gawn RUCK | 3194 → 3092 | −102 (−3.19 %) |
| Colby McKercher MID | 4263 → 4354 | +91 (+2.13 %) | Logan Morris KPF | 2945 → 2845 | −100 (−3.40 %) |
| Finn O'Sullivan MID | 3222 → 3312 | +90 (+2.79 %) | Ethan Read KPF | 490 → 587 | +97 (+19.80 %) |
| Ned Reeves RUCK | 342 → 432 | +90 (+26.32 %) | Harry Sheezel MID | 10428 → 10331 | −97 (−0.93 %) |
| Archer Reid KPF | 373 → 457 | +84 (+22.52 %) | Liam Fawcett KPF | 267 → 360 | +93 (+34.83 %) |
| Sean Darcy RUCK | 837 → 921 | +84 (+10.04 %) | Jason Horne-Francis MID | 5609 → 5519 | −90 (−1.60 %) |
| Hussien El Achkar SF | 364 → 447 | +83 (+22.80 %) | Darcy Wilson SF | 2828 → 2741 | −87 (−3.08 %) |
| Hugo Garcia MID | 2544 → 2626 | +82 (+3.22 %) | Kysaiah Pickett SF | 3878 → 3792 | −86 (−2.22 %) |
| Sam Draper RUCK | 1012 → 1092 | +80 (+7.91 %) | Bailey J. Williams RUCK | 2438 → 2354 | −84 (−3.45 %) |
| George Wardlaw MID | 2974 → 3050 | +76 (+2.56 %) | Shannon Neale KPF | 2329 → 2246 | −83 (−3.56 %) |

### Top 20 by absolute move — VARIANT B

| **B raw** (`smooth`) | | | **B conserved** (`smooth+conserve`) | | |
|---|---|---|---|---|---|
| Tristan Xerri RUCK | 7024 → 7212 | +188 (+2.68 %) | Luke Jackson RUCK | 9265 → 8911 | −354 (−3.82 %) |
| Nasiah Wanganeen-Milera MID | 8660 → 8820 | +160 (+1.85 %) | Josh Treacy KPF | 6179 → 5941 | −238 (−3.85 %) |
| Max Holmes MID | 7588 → 7717 | +129 (+1.70 %) | Izak Rankine SF | 4819 → 4630 | −189 (−3.92 %) |
| Cooper Duff-Tytler KPF | 1809 → 1932 | +123 (+6.80 %) | Sam Darcy KPF | 5116 → 4964 | −152 (−2.97 %) |
| Nick Daicos MID | 9892 → 10012 | +120 (+1.21 %) | Kysaiah Pickett SF | 3878 → 3739 | −139 (−3.58 %) |
| Ethan Read KPF | 490 → 606 | +116 (+23.67 %) | Harry Sheezel MID | 10428 → 10293 | −135 (−1.29 %) |
| Errol Gulden MID | 7075 → 7187 | +112 (+1.58 %) | Brodie Grundy RUCK | 4212 → 4082 | −130 (−3.09 %) |
| Tom Green MID | 5575 → 5684 | +109 (+1.96 %) | Darcy Wilson SF | 2828 → 2704 | −124 (−4.38 %) |
| Nate Caddy KPF | 1612 → 1719 | +107 (+6.64 %) | Nick Watson SF | 3594 → 3473 | −121 (−3.37 %) |
| Colby McKercher MID | 4263 → 4363 | +100 (+2.35 %) | Riley Thilthorpe KPF | 4048 → 3928 | −120 (−2.96 %) |
| Finn O'Sullivan MID | 3222 → 3320 | +98 (+3.04 %) | Murphy Reid SF | 3427 → 3310 | −117 (−3.41 %) |
| Liam Fawcett KPF | 267 → 363 | +96 (+35.96 %) | Timothy English RUCK | 3336 → 3221 | −115 (−3.45 %) |
| Will Ashcroft MID | 6589 → 6684 | +95 (+1.44 %) | Max Gawn RUCK | 3194 → 3087 | −107 (−3.35 %) |
| Jake Bowey SD | 3896 → 3986 | +90 (+2.31 %) | Bailey J. Williams RUCK | 2438 → 2338 | −100 (−4.10 %) |
| Hugo Garcia MID | 2544 → 2631 | +87 (+3.42 %) | Ethan Read KPF | 490 → 589 | +99 (+20.20 %) |
| Ned Reeves RUCK | 342 → 429 | +87 (+25.44 %) | Jason Horne-Francis MID | 5609 → 5511 | −98 (−1.75 %) |
| Sean Darcy RUCK | 837 → 923 | +86 (+10.27 %) | Logan Morris KPF | 2945 → 2853 | −92 (−3.12 %) |
| Hussien El Achkar SF | 364 → 449 | +85 (+23.35 %) | Jai Newcombe MID | 4587 → 4496 | −91 (−1.98 %) |
| Archer Reid KPF | 373 → 457 | +84 (+22.52 %) | Jack Ginnivan SF | 2089 → 2000 | −89 (−4.26 %) |
| Harley Reid MID | 3919 → 4002 | +83 (+2.12 %) | Luke Davies-Uniacke MID | 3615 → 3527 | −88 (−2.43 %) |

**The shape of it, in one sentence per column.** The raw variants pay the thin-evidence rows out of nothing and
the board grows by ~1.2 %. The conserved variants pay them by charging every established row in the same
future-position class about 3 % — Luke Jackson, Josh Treacy, Max Gawn, Harry Sheezel — and the board still
falls 0.58 %.

### A PREREG PREDICTION THAT DID NOT HOLD, NAMED

Prereg §5 predicted raw A would be **up-only**. **It is not.** 32 rows move DOWN under raw A, totalling
−237 SCAR against +8,697 up: Joe Richards −23, Aaron Naughton −20, Murphy Reid −17, Massimo D'Ambrosio −16,
Tom Brown −16, Joshua Weddle −14, Kieren Briggs −14, Connor Rozee −12, and 24 more in the attached file. The
monotoniser itself can only raise a band; the down-movers therefore come from something downstream reacting to
other rows rising. **The mechanism is NOT measured by this seat.** The obvious candidate is the SHIPPED
`_UC_C` per-position production renorm, which is calibrated at load over the same valuation scope
(`_merged_recover.py:5866-5878`), so raising some rows in a class re-scales the rest — but naming a candidate
is not measuring it, and it is filed in §9 rather than claimed here.

---

## 3. Who does NOT move — by name

**153 of 804 rows are byte-unmoved under ALL FOUR readings**, and 253 under raw A alone. Named rather than
counted: **Josh Smillie** (759), **Oskar Taylor** (585), **Mitchell Marsh** (546), **Will Green** (497),
**Harley Barker** (492), **Toby Conway** (460), **Sam Allen** (439), **Taylor Goad** (439), **Harry Barnett**
(422), **Blake Thredgold** (377), **Tyan Prindable** (366), **Flynn Riley** (350), **Hunter Holmes** (347),
**Harry DeMattia** (335), **Logan Smith** (321), **Tai Hayes** (147) — the full unmoved set is derivable row by
row from any `MOVERS_*.json` `all_rows` block. Under raw A the largest unmoved rows are **Max Gawn** (3194),
**Darcy Wilson** (2828), **Joel Freijah** (2582), **Jaspa Fletcher** (2505), **Tom Powell** (2000). That is the
exact-knot construction working as designed: a row sitting on an already-monotone stretch is priced at its own
raw band, **unchanged, exactly** — not at a grid approximation of itself.

**THE LIVE BOARD DOES NOT MOVE, AND THAT IS F1.** `data/rl_build/rl_app_data.json` and
`engine/rl_after/rl_app_data.json` both read `68be10c79d0ee096455754e084bcf757` on the final tree, and with the
dial OFF the EDITED tree **rebuilds** that board byte-exact — dev twice (103.6 s, 101.7 s), canonical once
(100.9 s) — and the balanced sibling byte-exact at `556ad70d295923455982ae33e4b8bfd3` (102.7 s).
`BUILD_F1_out.txt`.

**Byte-unmoved carriers, each with the measurement that says so:**

| carrier | value | how it is known |
|---|---|---|
| board (both copies) | `68be10c7` | md5 on the final tree + F1 rebuild |
| balanced sibling | `556ad70d` | F1 rebuild |
| store `rl_model_data.json` | `b745002e` | md5; `store_coherence_six_way` PASS |
| `rl_model.py` | `6fe7c415` | md5; asserted by `sfx_restamp.py` before it wrote |
| `data/model_config.json` | `269d20ab` | md5; `config_manifest` PASS at hash `eed19a75` |
| `q97m.pkl` | `cfdc7321` | Guard-5 pin; `mirror_parity` PASS |
| `cm_400.pkl` | `34faa865` | Guard-5 pin, re-measured this seat |
| `v0surf.pkl` | `5dd34ca8` | Guard-5 pin |
| `LTI_REGISTER.md` | `652d83e8` | md5 |
| `conditional_prior.py` and every `engine/forward_valuation` source | fv `6e9a370e…` | unmoved: this act edits one file and it is not in that set |

**The year-0 column does not move — 0 of 2,648 records, under BOTH variants, at tolerance 0.** That is §5's
day-0 leg and it is the second reading of a law the emitter also enforces fail-closed.

**MSD's year-1 no-arb cell does not move and cannot**: an MSD row keys its cohort on the draft year itself, so
at year 1 it is PRE-WINDOW and excluded rather than scored as zero. It carries no verdict on any of the three
boards and therefore no verdict change.

---

## 4. Cost

**Measured, then quoted.** Wall-clock on this box, from the run logs named beside each figure.

| leg | measured |
|---|---|
| pre-edit baseline build (proves the box can make the live board) | **101.3 s** (`BASE_PREEDIT.meta.json`) |
| F1 — four builds, dial OFF: dev, dev, canonical, balanced | **103.6 + 101.7 + 100.9 + 102.7 s = 6 m 49 s** (`BUILD_F1_out.txt`) |
| the four candidate board builds (A raw / A con / B raw / B con) | **not recorded** — the prior seat's movers files carry the boards, not the build minutes. Named as missing rather than estimated. |
| the monotonicity math check on the pinned forests | seconds (`MATHCHECK_out.txt`) |
| day-0 reference regenerated on the live board | **~60 s**, one in-process engine load (`sfx_day0.py`) |
| walk-forward emit, base (dial unset) | **2 m 11 s** |
| walk-forward emit, **variant A conserved** | **5 m 30 s** |
| walk-forward emit, **variant B conserved** | **11 m 19 s** |
| one emit discarded on the stale day-0 reference (see §9) | 46 s |
| ND bands / pool arms / class / checks / two rendered pages | **< 30 s each**, pure reads |
| `acceptance.runner --profile full` | **~14 min** (it builds the board twice for `build_twice_determinism`) |
| `release_manifest_check.py` | **~40 s** |

**The cost that matters for adoption, and it is not a seat cost.** ORDER 44 evaluates the six-leg band at up to
2,329 knots per row instead of once. Measured on the same work: the emit goes **2 m 11 s → 5 m 30 s under
variant A (2.5×) and → 11 m 19 s under variant B (5.2×)**. Variant B costs roughly **twice what variant A
costs** because the smoothing evaluates the whole knot grid rather than stopping at the row's own level. Any
adoption inherits that multiplier on every build in the loop.

---

## 5. Standing-table impacts

**The standing law: no-arb tables and the rendered page ride every priced delivery.** Both conserved variants
carry both. `NOARB_SFX_SFXACON.html` and `NOARB_SFX_SFXBCON.html` are the rendered pages — every ND band, every
pool arm, both windows, each cell printed **beside the live board's own cell**, with the owner's path test
scored on every breaching cell on both boards. Raw: `BANDS_NOARB_SFX_out.txt`,
`STANDING_TABLES_NOARB_SFX_out.txt`, `CLASS_SFX_out.txt`. Inputs checked, not asserted:
`NOARB_SFX_CHECKS_out.txt` — **ALL CHECKS PASS**.

### ND bands — year-0→1 appreciation (buy rail +14 %, sell rail 0 %)

| cell | live `68be10c7` | **A conserved** | **B conserved** |
|---|---|---|---|
| PRIMARY ALL 1-64 | +6.73 % ok | +7.82 % ok | +7.99 % ok |
| PRIMARY 1-10 | +13.12 % ok | +13.64 % ok | +13.84 % ok |
| PRIMARY 1-20 | +12.98 % ok | +13.70 % ok | +13.93 % ok |
| **PRIMARY 11-20** | **+12.71 % ok** | **+13.83 % ok** | **+14.11 % BUY-RED** ← **new breach** |
| PRIMARY 21-30 | +6.16 % ok | +7.84 % ok | +7.90 % ok |
| PRIMARY 21-64 | −3.15 % SELL-RED | −1.47 % SELL-RED | −1.41 % SELL-RED |
| PRIMARY 31-40 | −10.61 % SELL-RED | −9.37 % SELL-RED | −9.38 % SELL-RED |
| PRIMARY 41-64 | −6.41 % SELL-RED | −4.35 % SELL-RED | −4.24 % SELL-RED |
| MODERN 1-10 | +21.32 % BUY-RED | +22.32 % BUY-RED | +22.72 % BUY-RED |
| MODERN 1-20 | +14.88 % BUY-RED | +15.94 % BUY-RED | +16.39 % BUY-RED |
| MODERN 21-64 | −18.93 % SELL-RED | −17.31 % SELL-RED | −17.17 % SELL-RED |
| MODERN 41-64 | −26.91 % SELL-RED | −24.95 % SELL-RED | −25.06 % SELL-RED |

**Read in one line.** Both variants push **every** sell-side red **toward fair** — that is the correction doing
what it should, since the under-priced rows are exactly the thin-evidence ones. Both also push the buy-side
cells further up. **Under variant A no cell breaches that did not already breach, and none stops breaching.**
**Under variant B, PRIMARY picks 11-20 crosses the +14 % buy rail (+14.11 %) and becomes a NEW no-arb breach.**
Both variants flip the EX0506 sensitivity cell PRIMARY 21-64 from SELL-SIDE RED to fair — a repair, on a
sensitivity table rather than the standing basis. Those statements are **computed by the pages from the tables
they render**, not typed into them.

### Pool arms

Every arm moves the same way — toward fair from the sell side, further up on the buy side — and no arm changes
verdict on either variant. **SSP, the inherited breach (register v744 C6, parked), reads +63.12 % on the live
board, +63.54 % under A and +63.97 % under B**, and fails the owner's path test on all three (beats carry in
years 2, 3 and 4). ORDER 44 neither repairs it nor makes it materially worse; it is reported so its reading
stands beside the baseline instead of being described in prose.

### THE CLASS-DISCIPLINE NUMBER — F4, the law bound

Registered W2 basis: DRAFT classes 2005-2015. Owner's floor **≥ 1.03**; buy rail **< 1.14**. The instrument
self-validates against ORDER K's published marks (**1.0513 / 1.0324, difference 0.0000**) off ORDER K's own
matrix before any candidate number is read.

| board | W2 mark | vs floor 1.03 | vs rail 1.14 | verdict |
|---|---|---|---|---|
| **live R23 board `68be10c7`** | **1.0738** | +0.0438 | −0.0662 | inside the law |
| **A conserved** | **1.0829** | +0.0529 | **−0.0571** | **inside the law — F4 PASS** |
| **B conserved** | **1.0838** | +0.0538 | **−0.0562** | **inside the law — F4 PASS** |

For lineage: the registered 1.0672 belongs to the PRIOR live board `a05fe951`; the mark moved to 1.0738 at the
D8 adoption and the R23 advance, and this seat's own dial-unset emit reproduces that. No cohort crosses 1.14
that was not already across, on either variant — computed, printed in `CLASS_SFX_out.txt`.

### DAY-0 REFERENCE CHECK — expected 0 moved, read 0 moved

The year-0 column is **unmoved on all 2,648 records and on all 87 wired day-0 entrants, under both variants, at
tolerance 0**. Two independent readings: the ORDER 31-F replication guard inside each emit, which is
**fail-closed** and read **87 of 87** on all three emits (`EMIT_SFXBASE_out.txt`, `EMIT_SFXACON_out.txt`,
`EMIT_SFXBCON_out.txt`), and a direct row-by-row diff of the matrices in `NOARB_SFX_CHECKS_out.txt`. That is
the expected answer: ORDER 44 monotonises the BAND, and a day-0 entrant has no games, so his price is
`v0 × D(c_u)` and the dial has no path to it.

### THE LEDGER OF WHAT WAS CHECKED AND FOUND UNMOVED

Board, balanced sibling, store, `rl_model`, `model_config`, `q97m`, `cm_400`, `v0surf`, `LTI_REGISTER`,
`fv` source set, `docs/OPEN_ITEMS_REGISTER.md` (not touched by this seat, as the prereg declared), the day-0
column, and MSD's year-1 cell. `data/book_stable_seal.json` reads **SEALED-LAG** (sealed against `1867e953`,
tree now `3f4aa10b`) — reported by the manifest, never gating, and a book re-seal is a separate act.

---

## 6. What would make this silly

**This is scaffolding and it says so in its own code.** ORDER 44 monotonises the OUTPUT of a surface whose
defect is at the FIT. FIX 1 — `monotonic_cst` on feature 9 at `conditional_prior.py:160-161` and at
`refit_q97m.py` — makes "more demonstrated level is never worth less" true BY CONSTRUCTION, permanently, for
every row, and retires this entire dial. It is owner-scheduled for the variant-C rebake next week, post-R24.
**ORDER 44 is classified for retirement at that rebake and its removal is a rebake MUST-MOVE PROOF.** If the
rebake is a week away and holds, the honest reading is that this act buys one week of correct prices at the
cost of a dial, a 2.5–5.2× build-time multiplier, and a scaffold somebody has to remember to tear down. **The
reading under which this act is not worth doing is: wait for the rebake.**

**VARIANT A's specific defect: PLATEAUS ARE ZERO MARGINAL REWARD.** The ratchet is a step function. On a
plateau, a player can score more, raise his level, and be worth **exactly the same**. That is a strictly better
world than the current one — where he can score more and be worth **less** — but it is not the world the owner
would design. `MATHCHECK_out.txt` measures the plateaus rather than describing them: on the MID/pick-40 sweep
44→58 at 0.05, variant A shows **203 of 281 steps FLAT**; at 0.002 resolution over 46→50, **1,985 of 2,000
FLAT**. Most of the axis pays nothing at the margin. If the owner's objection to the trough is really "effort
must be rewarded", A answers only half of it.

**VARIANT B's specific defect: THE INTERPOLATION IS A CHOICE.** B is strictly rising — 0 flat steps at every
resolution tested, minimum step +0.0003 at 0.002 level units, roughly 1/25th of one round-23 score point — and
it introduces **no new parameter**, which is exactly why a minimum-slope floor was rejected. But "put each
plateau's value at that plateau's midpoint and interpolate linearly" is still a *shape this seat picked*. It is
parameter-free; it is not assumption-free. It redistributes within each plateau — below the plateau value on
the left half, above it on the right — which is why **B is not ≥ A pointwise** and why more rows move DOWN
under raw B (114) than under raw A (32). And it costs about twice A's build time. **And it is the variant that
puts a new cell over the no-arb buy rail.**

**THE CONSERVATION LEG DOES NOT CONSERVE THE BOARD, AND BOTH READINGS BREACH LAW 9.** Law 9 says re-pricing
redistributes value, it does not mint or burn it; the rail is `band_scar = 200`, which against a 692,296 board
is ±0.029 %.

| reading | mint | as a multiple of the 200-SCAR rail |
|---|---|---|
| A raw | **+8,460 SCAR (+1.222 %)** | **42.3× the rail** |
| A conserved | **−4,025 SCAR (−0.581 %)** | **20.1× the rail** |
| B raw | **+8,385 SCAR (+1.211 %)** | **41.9× the rail** |
| B conserved | **−4,169 SCAR (−0.602 %)** | **20.8× the rail** |

The renormaliser conserves exactly what it was defined to conserve — each future-position class's **total
production leg** — and the prereg said in advance that the board total is not the production total, because
ORDER 31 blends production with pedigree and age credit downstream, and that the residual would be **measured
and reported, never assumed to be zero**. It is measured: it is **−0.58 %**, twenty times the rail, in the
opposite direction to the raw mint. So the conservation leg halves the magnitude of the law-9 breach and
**flips its sign**; it does not remove it. Anyone reading "conserved" as "law 9 satisfied" is reading it wrong,
and that is why the number is in this slot and not only in §2.

**And conservation is not incidence-neutral.** It pays the thin-evidence rows by cutting 335 established rows
about 3 % — Luke Jackson −298, Josh Treacy −222, Sam Darcy −149, Max Gawn −102, Harry Sheezel −97. Under the
conserved readings **Charlie West, one of the four rows this fix exists for, ends up 2.36 % BELOW where he
started.** A fix for a trough that leaves one of its four named victims lower than it found him is a fix worth
looking at twice.

**What is NOT held.** F5 (determinism) is held for the OFF build only — dev twice plus canonical, all byte-
identical. **The four candidate boards were each built ONCE**; no candidate has a determinism repeat, and this
seat did not add one (the candidate builds carry the same 2.5–5.2× multiplier the emits measured). F2's
monotonicity leg is held on the band's weighted mean as a proxy, at 0.002 level resolution, on three rows;
**F2's "trough measurably gone" leg through TRUE `ev()` — the 76-point score sweep on each named victim and the
86-row class sweep — was not re-run by this seat.** The board-level before/after in §2 is a partial reading of
it, not a substitute. Both ride adoption. Named here rather than in a footnote because a falsifier nobody fired
is a decoration.

---

## 7. Recommendation

**Price both, adopt neither today, and if the owner adopts, adopt VARIANT A.** The deciding fact is not
aesthetic: **variant B puts a cell over the no-arb buy rail that was inside it — PRIMARY picks 11-20, +12.71 %
on the live board, +14.11 % under B — and variant A does not** (+13.83 %, inside by 0.17 pp, which is itself
thin enough to say out loud). B also moves more rows down against the live board, costs about twice as much per
build, and its extra property over A — strict rise instead of plateaus — buys a *smaller* violation of the
owner's real complaint than it looks: A already guarantees "more level is never worth less", which is the law-3
breach; B additionally guarantees "more level is always worth more", which is a preference, not a law. **This
seat would not create a new no-arb breach to buy a preference.**

On raw versus conserved this seat states a lean and does not pretend it is a finding: **RAW, with the mint
stated as the owner ruling the diagnosis §8.1 already framed** — *either renormalise, or the owner rules that
the lift is the correction rather than an inflation*. The reason is that the conserved leg **fails its own
purpose** (−0.58 %, 20× the rail, sign flipped) while charging 335 established rows ~3 % and pushing Charlie
West below where he started. If the owner's instinct is that a 1.2 % board lift is inflation rather than
correction, then the honest next move is **not** this renormaliser but a board-level one, which **was not built
and is not being smuggled in here** (§9).

**What this seat is NOT asking for.** Not adoption. Not a dial default flip. Not a board move, a pin move, a
register edit or a re-seal. The dial ships OFF, the live board is `68be10c7` at this seat's final commit, and
the owner's word is the only thing that changes any of that.

---

## 8. Falsifiers

**F1 — THE KILL-SWITCH. HELD, MEASURED.** With the dial OFF, a build off the EDITED tree reproduces
`68be10c79d0ee096455754e084bcf757` **byte-exact** in dev (twice: 103.6 s, 101.7 s) and in canonical posture
(100.9 s), and the balanced sibling reproduces `556ad70d295923455982ae33e4b8bfd3` byte-exact (102.7 s).
`BUILD_F1_out.txt`. **Re-asserted at this seat's final commit:** both committed copies of the board still read
`68be10c7`. *Would have fired on any differing byte.* This is also P1's standing falsifier for the act.

**F2 — THE TROUGH IS MEASURABLY GONE. PARTIALLY HELD, AND THE UNHELD HALF IS NAMED.**
*Held:* the monotonicity proof, on the pinned forests, at the read site, on three archetype rows (MID/pick-40,
KPD/pick-8, SF/pick-55) over two sweeps. Variant A: **0 negative steps**, legwise minimum **+0.000000**.
Variant B: **0 negative and 0 flat**, minimum step **+0.0003** at 0.002 level units (≈ 1/25th of one round-23
score point). The same table shows the raw surface at **69 negative steps, worst −1.161**, and the PREREG'S OWN
DISCARDED grid-ratchet at **30 negative, worst −0.471** — the instrument fires on both, so it is not a
tautology. `MATHCHECK_out.txt`.
*Held at board level:* the four named victims move +13.93 % / +25.91 % / +0.52 % / +38.89 % under raw A against
measured drops of 40.2 / 27.2 / 34.1 / 39.8 %.
**NOT held:** the 76-point score sweep through TRUE `ev()` on each named victim, and the 86-row class sweep
(44 of 86 → 0, and the 33 / 16 / 5 depth counts → 0). **This seat did not re-run them. F2 is therefore OPEN and
rides adoption.**

**F3 — LAW 12 (G-Y0) CLOSURE, pooled absolute percentage gap at the year-0 lens within 2.0 %. NOT MEASURED BY
THIS SEAT.** Stated as unheld rather than quietly dropped. What IS measured on the year-0 lens is stronger in
one narrow respect and weaker in another: the year-0 column is **byte-unmoved under both variants** (2,648 of
2,648 records, 87 of 87 wired day-0 entrants, tolerance 0 — §5), so no candidate can have moved the G-Y0 gap by
moving a year-0 print. It could still move the gap by moving the *year-0 lens's other side*, which is what F3
would have measured. **F3 rides adoption.**

**F4 — THE CLASS LAW. HELD, MEASURED, BOTH CONSERVED VARIANTS.** Year-1 class cohort mark on the registered W2
basis (draft classes 2005-2015) inside the owner's floor ≥ 1.03 and under the buy rail < 1.14. Live R23 board
**1.0738**; **variant A conserved 1.0829, margin −0.0571 to the rail; variant B conserved 1.0838, margin
−0.0562.** Both PASS. The instrument reproduced ORDER K's published 1.0513 / 1.0324 at difference **0.0000**
before either number was read. `CLASS_SFX_out.txt`, `NOARB_SFX_CHECKS_out.txt` CHECK 5. *Would have fired
outside either bound, and the breach would have been stated with its number rather than the candidate
withdrawn.* **Not measured on the two RAW variants** — they were not emitted, because the no-arb delivery the
standing law requires was scoped to the conserved pair.

**F5 — DETERMINISM. HELD FOR THE OFF BUILD ONLY.** `OFF_DEV_1 == OFF_DEV_2 == OFF_CANON == 68be10c7` and the
runner's own `build_twice_determinism` reads **PASS — two bare builds are BYTE-IDENTICAL** on the final tree.
**The four candidate boards were built once each and have no determinism repeat. F5 is OPEN for the candidates
and rides adoption.**

**F-NEW (not in the prereg, and this seat is adding it rather than hiding behind the prereg's list) — THE DIAL
CANNOT REACH A CERTIFYING BUILD.** `RL_O44_LVLMONO` is absent from `data/model_config.json`, so
`config_manifest.enforce()` rejects it as an unknown model override in bake / gate / canonical mode. Measured
twice: `config_manifest` reads **PASS (hash `eed19a75`, 84 vars, pin+stored consistent)** on the final tree,
and `dial_coverage` reads **PASS, 83 of 84 declared dials, 1 self-declared orphan** — the undeclared count
moved by exactly the predicted amount and no gate reds on it. `data/model_config.json` is byte-unmoved at
`269d20ab`.

**A FALSIFIER THAT ACTUALLY FIRED, ON THIS SEAT'S OWN INSTRUMENT.** The ORDER 31-F day-0 replication guard is
fail-closed, and it **fired**: pointed at the standing reference `DAY0_CP.json` (board `a05fe951`, pre-R23),
this seat's **dial-unset** emit read **24 of 89** and refused to produce a matrix
(`EMIT_SFXBASE_STALEREF_out.txt`, kept). That is not ORDER 44 — the dial was unset. See §9.

**TWO PREREG CORRECTIONS, MADE AGAINST THE TREE (P9), NOT THE OTHER WAY ROUND.**
(1) Prereg §1 says the release-contract seal `cde9f70a` **stands**. It cannot: `contract_sha256` hashes every
field of the contract except itself, so moving `identities.engine_head` necessarily re-stamps it. It moved to
`8e6dcdbc`. The claim the prereg was *actually* making — that **`config_sha256` is unmoved** because the dial is
not a manifest var — is true and is measured above. The prereg conflated a derived stamp with the claim.
(2) The prereg did not list the `engine_head` restamp among what this act moves. It moves it, at `1590a37`.
Correction 1 to the prereg (the window) was already filed at `901e731`, before the edit, and is not restated
here.

---

## 9. Findings this seat did not go looking for

**1. THE R23 ADVANCE DID NOT REGENERATE THE DAY-0 REFERENCE, AND EVERY WALK-FORWARD EMIT ON THE R23 BOARD FAILS
CLOSED BECAUSE OF IT.** Referred, not absorbed. The standing reference is
`docs/evidence/final_candidate_2026-08-19/DAY0_CP.json`, board `a05fe951`, pre-R23. On today's R23 board with
the **dial unset**, the ORDER 31-F guard reads **24 of 89** and halts. Cause, measured rather than guessed
(`sfx_day0.py` output): the R23 advance moved the unplayed clock `c_u`, so the sitter fade `D(c_u)` moved, so
the printed day-0 price moved on **63 of 89** rows — while `derived_v0`, the raw entry object, moved on **0**.
Two rows (`lachlan-carmichael`, `max-beattie`) left the day-0 population entirely; none joined. This is exactly
the case ORDER D and ORDER K regenerated for, and the R23 advance did not. **This seat generated
`DAY0_SFXBASE.json` on the live board (87 of 87 at tolerance 0) as THIS ACT'S OWN base reference and
supersedes nothing on the record** — `DAY0_CP.json` is unaltered and un-repointed. **A round-advance seat
should own the standing regeneration; this seat is not doing it under a pricing act.**

**2. THE EDIT COMMIT DID NOT RESTAMP `engine_head`, AND TWO GATES WENT RED ON IT.** Also referred, though the
repair rode this seat because it had to. `1446dec` moved the engine file and left four carriers naming the old
value; `release_manifest_check` read **FAIL, 4 of 40**, and the runner read **RED** with
`boot_guard_checkout` and `release_contract_seal` **BLOCKED** behind it. `MANIFEST_BEFORE_REPIN_out.txt` and
`RUNNER_BEFORE_REPIN_out.txt` keep the gates' word. The class is worth naming: **the D8 pricing seat declared
this restamp in its prereg §2.1 and wrote the tool; ORDER 44's prereg did not carry that clause forward.** The
cure that would actually retire the class is a prereg clause, not another tool — *any act that edits an engine
file restamps `engine_head` in the same commit* — and it belongs in the RULEBOOK's process laws, not in a
seat's memory.

**3. THE LANDER SELF-TEST WENT RED, AND ITS RED WAS DOWNSTREAM OF FINDING 2.** `lander_selftest` read
**7 PASS / 9 FAIL** with its CONTROL failing — and every fault case is meaningless while the control fails. The
control's own log names the cause exactly: *"`engine_head` is declared UNMOVED and the tree measures `3f4aa10b`
against a pin of `1867e953`"*, aborting at step `pins` in a sandbox built from the committed tree. It is
recorded here because it is a **real property of the lander that is worth keeping**: the self-test's control
run is a live coherence check on the tree it is invoked from, and it caught the missing restamp independently
of the manifest gate.

**4. RAW VARIANT A IS NOT UP-ONLY, AND THIS SEAT DID NOT MEASURE WHY.** 32 rows move DOWN under a construction
that can only raise a band (§2). The candidate mechanism — the shipped `_UC_C` per-position production renorm,
calibrated at load over the same valuation scope, so raising some rows in a class re-scales the others — is
**named as a candidate and not measured**. It is a small effect (−237 SCAR against +8,697) and it does not
change any recommendation, but it means "the ratchet only ever raises" is true of the BAND and false of the
BOARD, and anyone reasoning from the first to the second will be wrong.

**5. A BOARD-LEVEL CONSERVATION LEG WAS NOT BUILT.** The law-9 renormaliser this act carries conserves the
**production leg per future-position class**, because that is the class the shipped `_UC_C` conserves on and
the class law is the rail. Law 9 is stated on the **board**. The two are not the same object, the prereg said so
in advance, and the measured gap is −0.58 %. A renormaliser calibrated on the board total would close it — and
would break the class law's rail in the process, which is presumably why nobody has built one. **It is not
built, not measured, and not being offered here as an option that exists.**

**6. `data/book_stable_seal.json` NOW READS SEALED-LAG.** `head_md5` is sealed against `1867e953`; the tree is
`3f4aa10b`. The manifest reports it and never gates on it, which is correct. But a gate that consumes the seal
as a *baseline* is now comparing against the older state, and the next seat that re-seals the book should know
that the lag dates from this act.
