# P5-3 — The export writes the as-at −1/−2 columns itself (HIGH: player values move on −1/−2)

**Depends on.** P4-3 (repin step; traced stash key). Serial: rl_export.py and tools/landing/steps.py (new step).
**Owner word + blind review.** vM1/vM2 ARE player values (the −1/−2 lenses, ui/app/config.js:43; card.js:299-303
draws them). Replacing them is a value move: RULEBOOK law 11 (blind independent review) and P1 (show the owner the
movers first). The old brief's "not a value move" was wrong.

**Done when.** rl_export.py sets each current row's vM1/vM2 from the banked as-at values (null when the player was
not on that season's as-at board), writes no `back` section, the lander's ui step regenerates ui/data/asat_boards.js
from the same banks, and the act lands on the owner's word with the movers shown.

**Facts (checked at ffb2663b).**
- rl_export.py:210-212: with BASE_REF=AGE_REF=2026, `_vM2, _vM1 = ev(p,2024), ev(p,2025)` on the current roster.
- Banks: docs/evidence/walkforward_retro_2026-08-29/values_asat_2025.json / values_asat_2024.json, produced by
  `tools/harness …/pass_asat_seasons.py` (its Y=2026 control first, :47-50). emit_asat_seasons.py PATCHES
  ui/data/board_view_working.js's lens columns after the fact and writes ui/data/asat_boards.js (:45, :48); the
  lander never runs it (no reference in steps.py), so every landing's extract_board_view rewrite drops the patch.
- They differ from today's columns for a second reason: the level-axis smoothing runs only when Y == BASE_REF
  (_merged_recover.py:2921-2926); the banks price with BASE_REF = Y (smoothed), today's columns at BASE_REF 2026 do not.
- `back` = 228 rows (data/rl_build/rl_app_data.json). Readers: rl_export.py:688-700 (lensConservation adds `back`
  on −1/−2), :994-1004 (the 64-pick recompute, same sum), :702 (`out`); ui/tools/extract_board_view.py:366, :480, :571;
  tools/landing/steps.py:962-972 (`board_values` reads active+back for store-edit summaries); ui/tests/extract_seam.test.py
  :175, :236 and its fixture ui/tests/fixtures/extract_seam_legf_schema.json:2429. No ui/app file reads `back`. The
  sealed F5 reconciliation (release_contract.json `f5_entrant_reconciliation`) is the entrant layer only.
- rl_export.py is in neither PIN_MEASURERS nor proofstash BUILD_INPUT_FILES today (P4-3's traced key adds it).
- Each bank records `store_md5` (f49dbef6, the live store) and `board_md5` e944be20 (not the live 96896e1c) and no
  engine identity. Since the bank commit (ce102b03) _merged_recover.py and rl_model.py changed by comments only
  (`git diff ce102b03 HEAD` has no non-comment line) and the survival act changed rl_export's +1/+2 only: the banks are
  VALID; only their stamp is old.

**Change.** (1) pass_asat_seasons records engine_head, rl_model, config and fv in each bank; rl_export reads the two
banks and HALTS only if a bank is missing or one of THOSE FOUR differs from the live tree. Store and board are excluded
by rule: the pass rewinds the store to season Y, and the board is an output (otherwise every weekly ingest, tools/player
act, P3-2 and this act itself would halt). An engine act that moves any of the four re-runs the pass as a declared
lander step after `repin` (P4-3) and before build_proofs, with both banks as carriers; (2) delete `back` and both lensConservation sums
over it (−1/−2 totals then mean "players on the as-at board who are still current" — say so in `_meta`);
(3) extract_board_view, board_values, extract_seam.test.py and its legf fixture stop expecting `back`; (4) emit_asat_seasons stops
patching board_view_working.js and becomes the ui step's writer of asat_boards.js (add a carrier entry);
(5) the banks enter the proof-stash key (P4-3 trace; bump KEY_SCHEMA). The banks are re-stamped, not re-priced, before measuring.

**Must not change.** v, vP1, vP2 key for key; the store; the banks' `values` (only their stamp gains four fields); the present lens conservation.

**Prove it.** Measurement build first: per-row vM1/vM2 old vs new (count, median, largest movers, by age), the −1/−2
lensConservation before/after — shown to the owner. Then: v/vP1/vP2 identical; vM1/vM2 == banks; `back` absent;
every ui/tests suite (`node ui/tests/*.test.js`, `*.test.mjs`, `python3 ui/tests/*.test.py`); blind review filed.

**Lands via.** Lever act, `moves: [board]` (+ engine_head only if the engine is touched), movers declared, owner word.
