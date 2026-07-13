# L7 — THE NUMÉRAIRE RE-BASE · built + verified · 2026-07-12 (register v30 item 17)

Owner ruling ("Rebase, 3000 is it."): **PICK 1 = 3000 is the numéraire.** L7 = the refit's FINAL
step — one declared uniform **÷1.0524** across every player value, pick value, anchor baseline and
absolute-SCAR constant. Uniform scalar ⇒ every ratio/ordering preserved; only the unit changes. This
supersedes the v29 "3157" reading (equivalent relative worlds; the owner picked the 3000 quotation).

## Where the ×1.0524 lives (so L7 divides the right thing)
`pick_redenomination.json` (factor 1.0524) applied at `rl_export.py:55`: shipped pick assets =
frozen v3.4 × 1.0524 → pick-1 **3157**. Player values already carry the +5.24% (the band-pool fix,
via `ev()`), anchored by `SCALE=7000/ref^γ` (`rl_model.py:457`; SCALE 4.68336 = 4.45 × 1.0524). So
the whole SCAR world sits ×1.0524 above the numéraire; L7 divides it back.

## The re-base, verified (`scripts/l7_rebase.py` → `out/l7_rebased_board.json`)
- **adopted_curve[1] == 3000 exactly** (the L1 ev-channel curve is pinned 3000). ✓
- **display pick-1 3157 → 3000.** ✓
- **All ratios preserved:** no strict inversion in 804 rows (12 rounding ties, declared); all 10
  anchor-pair ratios match to <0.2% (e.g. bont/gawn 1.4661 → 1.4660). ✓
- Anchors re-base: bont 3721→3536 · gawn 2538→2412 · briggs 2222→2111 · darcy 4013→3813 ·
  emmett 1178→1119. Board sum ÷1.0524.

## Constants re-quote (`out/numeraire_requote_table.md`; CONSTRAINTS v1.8 folds at the seam)
| constant | v1.7 | → v1.8 numéraire |
|---|---|---|
| A-BONT baseline | 3246 | **3084** (round-trips: 3084×1.0524=3246 — back to the pre-redenom class) |
| G-CONVEX ≤21 / 22-24 / 25-26 | 189579 / 187563 / 113420 | **180140 / 178224 / 107773** |
| SCALE anchor (7000/ref^γ) | 7000 | **6651** (≡ SCALE 4.68336→4.45017, the baked v2.7 4.45) |

Replacement bars already sit "pre-redenomination basis" → **unchanged**. G-FLOOR SCAR dispensations
were one-off historical waivers → closed, not re-quoted forward.

## Standing law, wired mechanically
- `rl_export.py` **(g) NUMÉRAIRE ASSERT**: a numéraire board with pick-1 ≠ 3000 **HALTS** the write.
  Auto-active in the numéraire world (factor→1.0 / sidecar retired / `RL_NUMERAIRE=1`); a legacy
  ×1.0524 board (pre-L7) is dormant-with-warning so the current candidate is not broken. Unit-tested
  across all branches (dormant / pass / HALT-on-drift); `py_compile` clean.
- `BAKE_CHECKLIST.md` §3: numéraire assert added as a mandatory ship-gate step.
- Principle enforced (register v30): future scale drift re-bases the CURRENCY to the anchor, never
  the anchor to the drift.

## Sequencing
L7 is the refit's **final** step: it applies AFTER L1+L4+L2+L3 land in the one refit, on the combined
board. Built + verified here on the current board as the machinery + the numbers; the live
application rides the permanent refit. Per-lever attribution will report in **re-based (numéraire)
units** consistently once the refit board exists.
