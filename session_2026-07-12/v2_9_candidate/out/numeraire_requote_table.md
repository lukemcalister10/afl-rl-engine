# NUMÉRAIRE RE-QUOTE TABLE — L7 (÷1.0524) — for CONSTRAINTS v1.8 fold at the seam
### Register v30 item 17 · owner "Rebase, 3000 is it." · PICK 1 = 3000 is the numéraire.
### Factor = 1.0524 (pick_redenomination.json; MEASURED 4.68336/4.45 = 1.052440). Uniform scalar ⇒
### every ratio preserved; only the unit changes. These are the v1.7 absolute-SCAR constants ÷1.0524.

| constant | source | v1.7 (×1.0524 units) | → v1.8 (numéraire) | note |
|---|---|---|---|---|
| A-BONT baseline | acceptance A-BONT.baseline | 3246 | **3084** | back to the pre-redenomination 3084 class (round-trips: 3084×1.0524=3246) |
| G-CONVEX young-floor ≤21 | acceptance G-CONVEX | 189579 | **180140** | band-aggregate SCAR floor |
| G-CONVEX young-floor 22-24 | acceptance G-CONVEX | 187563 | **178224** | |
| G-CONVEX young-floor 25-26 | acceptance G-CONVEX | 113420 | **107773** | |
| SCALE anchor (7000/ref^γ numerator) | rl_model.py:457 | 7000 | **6651** | sets absolute board magnitude; equivalently SCALE 4.68336 → **4.45017** (== baked v2.7 4.45) |

## Disposition of the other registry magnitudes
- **REPLACEMENT BARS** (MID 80.1 · GEN_DEF 78.3 · GEN_FWD 70.9 · KEY_DEF 68.4 · KEY_FWD 66.8 ·
  RUC 78.5): already quoted "pre-redenomination basis" (v1.7 Part 1b) — they live in level/par space,
  NOT board-SCAR, and are **unchanged** by L7 (they are already in the numéraire's parent unit).
- **G-FLOOR SCAR dispensations** (≤5-SCAR on ≤45 rows; NAMED-16 ≤13-SCAR): SCAR-delta magnitudes;
  these were one-off historical waivers on specific past boards — they do NOT re-quote forward (they
  are closed). If ever re-applied to a numéraire board, the SCAR deltas scale ÷1.0524 (5→4.75, 13→12.35).
- **A-GAWN "≈+40 above REPL"**: descriptive SCAR delta, not a hard threshold; scales ÷1.0524 (~+38) if quoted.

## Assertions L7 must pass (register v30)
1. **All ratios preserved** — verified: order has no strict inversion (12/804 rounding ties, declared),
   all anchor-pair ratios match to <0.2% (`out/l7_rebased_board.json`).
2. **adopted_curve[1] == 3000 exactly** — the L1 ev-channel curve is pinned 3000; the ×1.0524 display
   pick-1 (3157) ÷1.0524 → 3000.

## Standing law (mechanical)
`_numeraire_guard()` in `rl_export.py` + a step in `BAKE_CHECKLIST.md`: a numéraire board with
pick-1 ≠ 3000 HALTS. Future scale drift re-bases the CURRENCY to the anchor, never the anchor to the
drift (register v30). CONSTRAINTS v1.8 folds these numbers at the seam (supervisor pen).
