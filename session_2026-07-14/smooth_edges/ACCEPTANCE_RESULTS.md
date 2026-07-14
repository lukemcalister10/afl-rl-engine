# ACCEPTANCE RESULTS — smooth the three hard edges (ablated + combined)

**Board of record:** `3dc19fbb` (store `340a7a32`, engine `2030e5df`) — ITEM-20 successor to tagged
`81e48293` (bramble +1 the only delta; no measured player affected). Baseline rebuilt twice byte-identical
(`3dc19fbb`), panel PASS 10/10. **All-fixes-off overlay reproduces base byte-exact** (ev-md5 `b5dbead0`).
ev/F = numéraire (÷1.0524). ev/F-board md5s: BASE `cb0e0528` · F1 `2c7eb319` · F2 `b14b8009` ·
F3 `e2371ef2` · F1+F2+F3 `c72c2033`.

## PER-FIX EFFECT (movers = |Δev/F|≥1; net in numéraire SCAR)
| config    | movers | up | down | net SCAR |
|-----------|-------:|---:|-----:|---------:|
| F1 (lvlcurr damping) | 278 | 166 | 112 | +1171 |
| F2 (tolerance ramp)  | 57  | 51  | 6   | +4675 |
| F3 (pedigree fade)   | 86  | 30  | 56  | −2612 |
| **F1+F2+F3**         | 335 | 205 | 130 | +4171 |

## A1 — JAMARRA (which fix: **F1 alone**; F2/F3 do not touch him, n=3 thin branch)
Sweep career games (2026 cameo @26.0), ev/F | level `_lvl_eff`:
| games | BASE ev/F (L) | F1 ev/F (L) |
|------:|--------------:|------------:|
| 60 | 996 (60.75) | 996 (60.75) |
| 64 | 1009 (61.07)| 1009 (61.16)|
| 67 | 1009 (61.26)| 1006 (61.40)|
| **70** | **187 (48.75)** | **466 (54.56)** |
| 74 | 142 (44.00) | 162 (44.72) |

- 67→70g: BASE **−81%** (1009→187); F1 **−54%** (1006→466). F1 halves the level drop (−20%→−11%)
  AND the value cliff.
- **BUT the ~20% target is NOT met by any of the three fixes.** The residual −54% is the
  **ev(level) pricing convexity** near the KEY_FWD replacement bar (66.8): an 11% level move
  amplifies ~5× (F1 level 61.40→54.56 = −11%, but ev/F 1006→466 = −54%). That amplification is a
  **fourth hard edge** outside this job's three (it lives in the band/floor pricing, not in
  `_lvlcurr`/`_coreM1`/pedigree). Per the directive's "STOP and report if a new construction is
  needed," we report it rather than redesign the pricing curve.

## A2 — THE KIDS ARE NOT NERFED — net SCAR by season band (nseas 1..9)
| band | n | F1 | F2 | F3 | ALL |
|-----:|--:|---:|---:|---:|----:|
| 1 | 280 | −100 | 0 | 0 | **−100** |
| 2 | 200 | −3 | 0 | 0 | −3 |
| 3 | 166 | +60 | 0 | 0 | +60 |
| 4 | 118 | −199 | +1424 | −1314 | +242 |
| 5 | 112 | −828 | +944 | −578 | +42 |
| 6 | 114 | −75 | +1239 | −641 | +861 |
| 7 | 94 | +1501 | +861 | −25 | +2034 |
| 8 | 93 | +119 | +187 | −55 | +275 |
| 9 | 386 | +696 | +20 | +1 | +760 |

Under **ALL**, only bands 1 (−100) and 2 (−3) are negative — band 1 is **not** the only negative one → **PASS**.
Band-1 detail (ALL): 280 players, 24 movers (17 up, 7 down), net −100 (avg −0.36). Rookies (debut≥2025):
222 players, 24 movers (13 up, 11 down), net −292; largest down Lindsay −109, Marshall −63. Contrast the
REJECTED games-basis build (60/76 down, net −3593): **these fixes barely touch the kids.** F1 leaves a
single-season player exactly unchanged by construction (ρ cancels in the normalized ratio).

## A3 — BLAKEY & ENGLISH (+Wilmot, Berry) — ev/F
| player | BASE | F1 | F2 | F3 | ALL |
|--------|-----:|---:|---:|---:|----:|
| Nick Blakey (GEN_DEF, Lc−Lo=+8.04) | 3330 | 3328 | 3330 | 3330 | 3328 |
| Timothy English (RUC, Lc−Lo=−2.83) | 3132 | 3251 | 3132 | 3132 | 3251 |
| Darcy Wilmot (GEN_DEF)             | 4237 | 3544 | 4237 | 3764 | 3751 |
| Joe Berry (GEN_FWD)               | 1321 | 1328 | 1321 | 1321 | 1328 |

**Fix 2 moves NEITHER Blakey nor English** — neither straddles the live TOL_M1=5.0 step (Blakey is an
up-mover +8.04, already fully credited; English is a −2.83 down-holder, not on the up-branch at all).
The directive's premise — "identical inputs, opposite signs from the tolerance step; must move together
after Fix 2" — does not hold on the live path. Their base divergence is genuine opposite-signed
form-vs-history, not a tolerance-cliff artifact. The +686/−189 the directive cites was from the prior
(λ/recency) build, not this step.

## A4 — THE IMPROVERS SURVIVE — ev/F
| player | BASE | F1 | F3 | ALL |
|--------|-----:|---:|---:|----:|
| Tristan Xerri | 6251 | 6251 | 5934 | 5934 |
| Max Holmes    | 6150 | 6150 | 6150 | 6150 |
| Lachlan Ash   | 5043 | 5024 | 5028 | 5024 |
| Bailey Smith  | 5243 | 5243 | 5243 | 5203 |

**F1 leaves every improver essentially untouched** (targeted at thin cameos, not established form).
The only notable drag is **F3 on Xerri (−317, −5%)** — the pedigree fade pulls a proven above-par
improver back toward par. That is the cost of Fix 3; F1 and F2 have no such effect.

## A5 — GUARDS (BASE vs F1+F2+F3, on the rebuilt board)
| guard | status | BASE | F1+F2+F3 | verdict |
|-------|--------|------|----------|---------|
| A-BONT (≥+10% / 3084 num) | BINDING | 3482 (+12.9%) | 3482 (+12.9%) | PASS, unchanged |
| A-PAIRS p2 (\|reid/bont−1\|≤10%) | BINDING | +3.2% | +3.0% | PASS |
| A-PAIRS p3 (bont>sanders 0-10%) | OWNER_ON_SIGHT | sanders +13.7% (fail) | sanders +10.9% | still fails, **improves** |
| A-DUUR (duursma up; > Zeke) | OWNER_ON_SIGHT | 4339 (>2692) | 4339 (>2692) | PASS, unchanged |
| G-PEAK (butters/holmes ≤2% drop) | BINDING | 5688 / 6150 | 5688 / 6150 | PASS (0% drop) |
| G-FLOOR (B5 below-floor count) | FEATURE | 13 (incl Jamarra) | 12 (Jamarra saved) | improves, no new breach |
| G-CONVEX (band floors 180140/178224/107773) | ADVISORY | 202797/190622/115005 | 202273/190982/117889 | PASS, all clear |
| G-Y0 (walk-fwd y2>y1) | PENDING | y1 620 y2 722 ✓ | y1 620 y2 723 ✓ | PASS, shape held |
| G-COHORT (walk-fwd l3, hard 1.30) | BINDING | y4/5/6 = 136.5/137.3/141.2 | 136.2/139.8/142.9 | see note |

**G-COHORT note (important):** the sanctioned walk-forward l3 gated construction (class-year SUMS ÷
min(y1,y2), classes 2014-2020) **already breaches 1.30 at BASE** (136.5/137.3/141.2) — reproduced
byte-for-byte by the official `l3_cohort_gate.py`. This is a **pre-existing property of the current
board**, not caused by this job. (The "126.8/125.2/116.1 PASS" headline is the *demoted indexed*
reading — per-class renorm to yr1=100 — a different construction, per the cohort-gate obituary.) The
fix moves the gated ratios by ≤ +2.5pt (y5 +2.5, y6 +1.7, y4 −0.3) and **does not create the breach**.
The canonical binding B1 (2004-2020 matrix Vpath) cannot be rebuilt under WIRE-NOTHING (its subprocess
re-execs the pinned engine; Guard 5 blocks a patched engine), so this is flagged, not certified clean.

## A6 — CONTINUITY — named sweep (max step per 3-game change), BASE → F1+F2+F3
Jamarra 81%→**58%** · Xerri 19%→11% · Wilmot 19%→13% · English 14%→16% · Bont 12%→12% ·
Blakey 2%→4% · Holmes 3%→3% · Smith 4%→6% · Reid 6%→6%. The fix reduces the worst step for the
edge cases; **Jamarra still steps 58%** (the residual pricing-convexity edge, A1). Board-wide scan below.

## A6 — BOARD-WIDE (real players nqual≤4; 2026 cameo swept 0/3/6/9/12 @ player's own avg)
- BASE: **243** players step >20% for a 3-game change · F1+F2+F3: **236** (−7).
- The three fixes reduce the worst edge-case steps (Jamarra 81→58, Xerri 19→11, Wilmot 19→13) but the
  bulk of the 236 residual steppers (Milan Murdock 98%, Ned Moyle 90%, … down to Tyler Sonsie 20%) are
  **fringe/low-value players crossing the ev(level) replacement-bar convexity** — the same fourth edge
  as A1. The level-construction fixes (F1/F2/F3) cannot smooth these; smoothing them requires smoothing
  the pricing curve near replacement/floor, which is OUT of this job's three edges.
- **Player who still steps (named):** Jamarra Ugle-Hagan (58%), plus the fringe cohort above — all via
  the pricing convexity, not the level terms this job fixes.

## PLAIN-TERMS BOTTOM LINE
Fix 1 is real and correctly aimed: it stops three bad games from erasing a career by damping thin
seasons on a data-fit reliability curve, and it cuts Jamarra's cliff roughly in half without nerfing
kids or improvers. Fix 2 as written moves nobody load-bearing (the pair it targets isn't on that step,
and the step it names is in dead code). Fix 3 does what the owner asked but has a cost — it drags proven
improvers like Xerri toward their pedigree. And the biggest remaining jump in every case is NOT in the
three edges at all: it's the pricing curve near the replacement bar, a fourth hard edge that turns a
20% level move into an 80% value move. That one needs its own ruling.
