# ACCEPTANCE TABLE — KPF REBALANCE (pre-bake) · 2026-07-09 · engine 275aa2a5 on L1c w=0.9 candidate
BEFORE = the L1c w=0.9 owner-ruled candidate (engine fbefdc2b) · AFTER = the rebalanced candidate.
"KPFFIX net" = value minus the same engine with RL_KPFFIX=0 · "young credit" = minus RL_YOUNG=0.

## 1. The owner's six top-tier names (Task 2 acceptance — magnitudes owner-on-sight)
| player | before | after | Δ | Δ% | KPFFIX net before → after |
|---|---|---|---|---|---|
| jake-waterman | 1307 | 1483 | +176 | +13.5% | -101 → +75 |
| charlie-curnow | 1005 | 1198 | +193 | +19.2% | -48 → +145 |
| riley-thilthorpe | 3202 | 3641 | +439 | +13.7% | -541 → -102 |
| josh-treacy | 5478 | 6055 | +577 | +10.5% | -118 → +459 |
| sam-darcy | 4168 | 4470 | +302 | +7.2% | +0 → +302 |
| jeremy-cameron | 1252 | 1453 | +201 | +16.1% | +41 → +242 |

## 2. The softened-take set (Task 1 acceptance — each named take before/after)
| player | take before (vs KPFFIX-off) | take after | comment |
|---|---|---|---|
| logan-mcdonald | -292 (-25.7%) | -282 (-24.9%) | no sustained demonstration (LD=Lc) — the honest take STANDS |
| mitch-georgiades | -193 (-13.7%) | -133 (-9.4%) | three high-games seasons — demonstrated slice retained at 0.70 |
| jake-waterman | -101 (-7.2%) | +75 (+5.3%) | take reversed by the top-tier reward (net give) |
| riley-thilthorpe | -541 (-14.5%) | -102 (-2.7%) | take softened 5.3× (demonstration + top-tier reward) |
| jack-lukosius | -254 (-15.3%) | -210 (-12.7%) | recent demonstration moderate — softened, still a take |
| josh-treacy | -118 (-2.1%) | +459 (+8.2%) | top-tier reward exceeds the residual take (net give) |
| jack-gunston | +17 (+1.8%) | +189 (+19.8%) | was the owner's "+17 gives little back" case — now a real give |
| jeremy-cameron | +41 (+3.4%) | +242 (+20.0%) | A-CAM: up, clears its bar |

## 3. The speculative set (Task 3 acceptance — slight, F-YOUNG honored, no wipe)
| player | before | after | Δ | Δ% | young credit before → after |
|---|---|---|---|---|---|
| jordan-croft | 1055 | 1039 | -16 | -1.5% | +202 → +186 |
| thomas-sims | 1069 | 1056 | -13 | -1.2% | +164 → +151 |
| matt-whitlock | 426 | 422 | -4 | -0.9% | +55 → +51 |
| jack-whitlock | 1261 | 1250 | -11 | -0.9% | +139 → +128 |
| harry-armstrong | 862 | 851 | -11 | -1.3% | +134 → +123 |
| archer-reid | 1072 | 1064 | -8 | -0.7% | +98 → +90 |
| murphy-reid | 3749 | 3749 | +0 | +0.0% | +7 → +7 |
| zach-reid | 1640 | 1640 | +0 | +0.0% | +31 → +31 |
| jonty-faull | 1245 | 1238 | -7 | -0.6% | +92 → +85 |
| ethan-read | 1428 | 1425 | -3 | -0.2% | +38 → +35 |
| jed-walter | 1511 | 1510 | -1 | -0.1% | +14 → +13 |
| calsher-dear | 1055 | 1054 | -1 | -0.1% | +12 → +11 |
| mitchell-marsh | 675 | 669 | -6 | -0.9% | +81 → +75 |
| daniel-curtin | 2148 | 2148 | +0 | +0.0% | +13 → +13 |
| cody-curtin | 683 | 677 | -6 | -0.9% | +78 → +72 |

## 4. GEORGIADES vs WHITLOCK (owner read: Georgiades above)
- BEFORE: georgiades 1218 vs jack-whitlock 1261 → BELOW (the owner-flagged inversion)
- AFTER : georgiades 1278 vs jack-whitlock 1250 → RESTORED (Georgiades above)
- (both Whitlocks exist in the store; matt-whitlock 422 — reported for completeness; the KPF-speculative read is jack-whitlock. Flagged: the directive says "Whitlock" unqualified.)

## 5. Anchor noise check (frozen levers — movement >0.5% is a finding)
| anchor | before | after | Δ% | verdict |
|---|---|---|---|---|
| marcus-bontempelli | 3524 | 3524 | +0.00% | UNTOUCHED |
| max-gawn | 2413 | 2413 | +0.00% | UNTOUCHED |
| willem-duursma | 4225 | 4225 | +0.00% | UNTOUCHED |
| kieren-briggs | 2109 | 2109 | +0.00% | UNTOUCHED |
| charlie-cameron | 271 | 271 | +0.00% | UNTOUCHED |
- A-GAWN comparator: max-gawn 2413 clearly above kieren-briggs 2109 — held.
- charlie-cameron (the drifted registry key) is a DIFFERENT player (GEN_FWD, pick 6) — 0.00%, untouched by the KEY_FWD-scoped anchor/reward logic; A-CAM keys jeremy-cameron (verified against the store).

## 6. A-DARCY three-way attribution (owner "too low" standing read)
- sam-darcy 4168 → 4470 (+7.2%) — direction UP.
  - young_convexity_ceiling: young-credit delta +0 before → +0 after (his evidence is past G0=46 games — the credit, and therefore the T3 trim, cannot touch him; ZERO by construction).
  - kpf_speculative (RL_KPFFIX lever): +302 — the WHOLE rise; the T2 partial-proven top-tier credit (nq=2, c=0.5, dm=23.0). He stays EXEMPT from the T1 compress (age<24).
  - availability_layer: ABSENT — no LTI return-haircut machinery exists in the engine (2026-07-08 diagnostic, re-confirmed; _b2hc/season-proration did not move him this build). Absence is the finding.

## 7. Net movement
- whole board: 687,922 → 690,941 (+0.44%)
- KEY_FWD position: 78,642 → 81,663 (+3.84%)
- movers: 30 up · 33 down · 742 unchanged (of 805 active); all non-KEY_FWD movement is ±1 rounding on 2 rows (the D14 KPP-class floor couples KEY_FWD/KEY_DEF V0 curves — declared).
