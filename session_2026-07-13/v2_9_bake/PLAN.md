# v2.9 BAKE — PLAN OF RECORD (first committed artifact) · 2026-07-13

Auto-mode. This PLAN is committed FIRST, before any value/code change. It enumerates the fenced
bake steps, the mechanism map I verified by reading the code, and the acceptance each step proves.

## BASE VERIFY (done)
- Full-URL `git ls-remote github.com/lukemcalister10/afl-rl-engine`:
  `claude/v2-9-export-display-jkcd5e = 065489707463e643b44f915fb21fd6473b1b40ae` ✓ UNMOVED (== directive base).
- Store `b0c39d78` identical on the code candidate (0654897) AND the register head (6f86bf9). ✓ (fence holds).
- **Base assembled** (this branch `claude/v2-9-bake-execution-dysldl`): merged the code candidate
  `export-display@0654897` (engine 2030e5df, board f2d6e3f5, store b0c39d78, config 69ead79b) into the
  register head `6f86bf9` (v56, carries the bake requirements items 19/24/26). CONFLICT-FREE (disjoint
  file sets), mirroring v2.8's in-bake main-merge so the final promote is a clean fast-forward.
  Re-bootstrapped: Guard 5 GREEN, store b0c39d78 == pinned.

## MECHANISM MAP (verified by reading the pipeline)
- **L7 is a DISPLAY-LAYER rebase.** Fence: "NOTHING here changes an engine value; the ONLY
  value-presentation change is the uniform L7 rebase." ev()/engine/store/config/book stay FROZEN.
  ship_gates acceptance reads engine ev() via `E(name)` (ratio/ordering) ⇒ **invariant under a uniform
  ÷1.0524 ⇒ reds stay EXACTLY {A2,A3,A12}** with no acceptance re-quote. Confirmed by shard S2:
  "class-sum RATIOS are mathematically invariant; the gate carries through the bake unchanged."
- **Numéraire factor F = 1.0524** (pick_redenomination.json `factor`; the certified l7_rebase.py divisor).
- **Adopted curve = `engine/rl_after/pvc_curve_L1b.json` `curve`** (stamped, curve_md5 645fce16):
  pick-1 = 3000, 99 picks, monotone non-increasing (verified). Players are ALREADY priced off this
  curve's SHAPE (L1 ev-channel, RL_PVCADOPT default ON); the DISPLAYED pick curve is still frozen v3.4×F
  (3157) — the "two currencies" oddity (A13/A14). The repoint makes the displayed pick curve BE the
  adopted curve at 3000.
- **Board = `data/rl_build/rl_app_data.json`** (md5 f2d6e3f5 = FINAL-HEAD board). Built by rl_export.py
  in gate/bake mode, six levers (RL_PVCADOPT/MSD_POOL_EXCL/DIAL14/AGE/L5_PICKLESS) default-ON in code
  (config_manifest clears ambient; code defaults apply). This is the ship_gates B4 path.
- **Stale prose to refresh (S3 Finding A):** the string `8a66b4ba` in expected_boot prose, PANEL_EXPECTED
  header, run_panel.sh comment, gates_2030e5df.json B4 detail — the pin FIELD f2d6e3f5 is correct.

## THE BAKE STEPS (fenced; each proves itself)

### 1. OVERRIDE RESTORATION (S1 fix set)
- `engine/rl_after/owner_overrides.py`: in gate/bake mode (RL_CONFIG_MODE in {bake,gate}) resolution
  HALTS (SystemExit) instead of silent `[]` — missing repo root OR missing file → HALT. Dev-shell
  unchanged (silent skip preserved; ci_guard_brodie stays green).
- `engine/rl_after/rl_export.py`: post-application PRESENCE ASSERTION — every player_key in
  owner_overrides.json must carry an `ov` block on the exported board (key-verified vs the store), else
  HALT in gate/bake. (Escalates the current key-drift WARNING to a HALT.)
- `boot_guard.py`: ASSERT expected_boot's `board` field (currently decorative/unasserted) at FULL hash —
  add a board-path check; compare full-length (fix the 8-char `_fmt` truncation for the board leg).
- `config_manifest.py`: remove `RL_NO_OWNER_OVERRIDES` from `INFRA_ALLOW` ⇒ in gate/bake it becomes an
  unknown RL_* override → REJECT/HALT (cannot silently disable overrides at a bake). Dev-shell unaffected.
- **PROVE 3 red paths** (committed proofs): (a) missing owner_overrides.json → HALT; (b) listed override
  key not applied (drift) → HALT; (c) wrong board pin in expected_boot → boot_guard HALT.
- ci_guard_brodie exclusion test stays GREEN (override OUT of guards/aggregates; dev-shell).

### 2. L7 NUMÉRAIRE REBASE + ADOPTED-CURVE REPOINT (rl_export.py, display layer)
- Divide displayed player values by F at the ev-read: `_v,_vM1,_vM2,_vP1,_vP2 = round(ev/F)`. Only the
  '_v*' display caches change; engine functions (peak/level/track/…) untouched. Parity gate updated to
  compare board v == round(ev/F) (F1 tripwire preserved in numéraire units).
- (f) block: `PVC = adopted curve (pvc_curve_L1b.json)` replacing frozen v3.4×F. ⇒ pick-1 = 3000; every
  pick-derived field (picks, lensPicks, intake*, lensConservation) reads the adopted curve.
- (g) NUMÉRAIRE ASSERT made **UNCONDITIONAL**: retire the dormant `_legacy_redenom` branch; `PVC[1]!=3000`
  HALTS, no legacy path. Add asserts: displayed PVC == the stamped pvc_curve artifact; adopted[1]==3000;
  monotone non-increasing; order preserved (no strict inversion, along before-order); all 10 anchor-pair
  ratios preserved (<0.2%).
- Brodie `ov` = round(REBASED_v × 0.50), marked OWNER OVERRIDE (unchanged override code reads the now-
  numéraire row['v']).

### 3. REGENERATE + ACCEPT
- Rebuild the board (gate/bake mode). Acceptance: diff vs f2d6e3f5 = the uniform rebase + adopted pick
  curve + exactly one row (will-brodie) gaining `ov` + nothing else; 0 relative movers (order preserved);
  name old→new md5s. Validate numéraire anchors against CERTIFICATION §5 (bont 3664→3482, gawn 2518→2393,
  darcy 4067→3865, emmett 851→809).

### 4. RE-PIN + PROSE REFRESH
- expected_boot.json: board = new full md5 (asserted). PANEL_EXPECTED.txt: numéraire values + rebase-note
  header. run_panel.sh: panel = round(ev/F) + numéraire pins + comment refresh. Refresh all stale
  `8a66b4ba` prose (expected_boot prose, PANEL_EXPECTED header, run_panel comment, gates_2030e5df.json B4).

### 5. BOOK RE-SEAL (B3)
- Re-seal `data/book_stable_seal.json` at the refit head (engine 2030e5df, store b0c39d78, n=2649).
  B3 then reads PASS (sealed head == candidate head), not differs-by-design. (Independent of L7; the book
  stays engine-ev by design — the rebase is board-display only.)

### 6. FULL SUITE (fresh bootstrap)
- Five SSI guards + Guard 5 GREEN. ship_gates: B1–B6 green · panel 10/10 on numéraire pins · acceptance
  reds EXACTLY {A2,A3,A12} (any other red = HALT). ci_guard_brodie exclusion GREEN.

### 7. UI RE-EXTRACT
- `ui/tools/extract_board_view.py` vs the numéraire board; EXPECTED_BOARD re-pinned; the four UI letters' rulings hold.

### 8. L-STOP (owner's word in-chat)
- Commit + push everything above; present the one-screen bake summary (old→new board md5s · pick-1 3000
  assert · brodie ov proof · suite verdict · B3 re-seal) and **STOP**. Tag `v2.9` + main fast-forward
  (never force) + PR #68 ONLY on the owner's explicit in-chat word.

## FENCE
The store md5 `b0c39d78` is identical at the last commit. ev()/valuation logic untouched (engine 2030e5df
unchanged — the rebase is display-only). No engine value changes; the only value-presentation change is
the uniform L7 rebase + the adopted-curve repoint. CONSTRAINTS v1.8 constant re-quote is a DOC fold
noted for the seam (the ship_gates gates read ev() ratios, not the doc constants — not bake-blocking).
