# P5-3 — The export writes the as-at −1/−2 columns itself (HIGH: player values move on −1/−2)

**Depends on.** P4-3 (repin step; traced stash key). Serial: rl_export.py and tools/landing/steps.py (new step).
**Owner word + blind review.** vM1/vM2 ARE player values (the −1/−2 lenses, ui/app/config.js:43; card.js:299-303
draws them). Replacing them is a value move: RULEBOOK law 11 (blind independent review) and P1 (show the owner the
movers first). The old brief's "not a value move" was wrong.

**Done when.** rl_export.py sets each current row's vM1/vM2 from the banked as-at values (null when the player was
not on that season's as-at board), writes no `back` section, the lander's ui step regenerates ui/data/asat_boards.js
from the same banks, and the act lands on the owner's word with the movers shown. (`back` and asat_boards.js parts:
see the open question below.)

**Facts (checked at 9a400286).**
- rl_export.py:210-212: with BASE_REF=AGE_REF=2026, `_vM2, _vM1 = ev(p,2024), ev(p,2025)` on the current roster.
- Banks: docs/evidence/walkforward_retro_2026-08-29/values_asat_2025.json / values_asat_2024.json, produced by
  `tools/harness …/pass_asat_seasons.py` (its Y=2026 control first, :47-50). emit_asat_seasons.py PATCHES
  ui/data/board_view_working.js's lens columns after the fact and writes ui/data/asat_boards.js (:45, :48); the
  lander never runs it (no reference in steps.py), so every landing's writer 1 (extract_board_view) rewrite drops the
  patch, and committing the patched bundle breaks tools/probe_bundle_equality.py (final-integration.yml:193).
  ui/data/asat_boards.js has no reader: nothing in ui/app or ui/index.html loads it.
- They differ from today's columns for a second reason: the level-axis smoothing runs only when Y == BASE_REF
  (_merged_recover.py:2921-2926); the banks price with BASE_REF = Y (smoothed), today's columns at BASE_REF 2026 do not.
- `back` = 327 rows beside 701 `active` (data/rl_build/rl_app_data.json). Since the exits act (777c8f47) it also
  holds the 107 end-of-2026 exits at a retiree value; every `back` row is a `_retired` store row.
  Readers: rl_export.py:688-700 (lensConservation adds `back` on −1/−2), :994-1004 (the 64-pick recompute, same sum), :702 (`out`); ui/tools/extract_board_view.py:366, :480, :571;
  tools/landing/steps.py:1405-1416 (`board_values` reads active+back for store-edit summaries and board_movers; its
  fixture tools/landing/test_store_edit.py:696-699); ui/tests/extract_seam.test.py :175, :236 and its fixture
  ui/tests/fixtures/extract_seam_legf_schema.json:2429; ui/tests/ownership_sidecar.test.js:250 (since c518ad1a the
  movers orphan check reads the working bundle's `back` as well as `players`: a movers key off both sections must be a
  retired store row; it tolerates a missing `back` via `|| []`, and today every off-active movers key is a retired store
  row, so it would stay green, but its premise changes). No ui/app file reads `back`. The
  sealed F5 reconciliation (release_contract.json `f5_entrant_reconciliation`) is the entrant layer only.
- rl_export.py is in neither PIN_MEASURERS nor proofstash BUILD_INPUT_FILES today (P4-3's traced key adds it).
- The banks were re-run at 9a400286 on the post-roster tree (2025: 810 rows, 2024: 809; Y=2026 control 0 diffs). Each
  records `store_md5` 6d70c6b9 and `board_md5` 159d3972 (both live at HEAD) and no engine identity; the engine files
  are unchanged since. The banks are VALID and current; they lack only the four engine fields of Change (1).

**Change.** (1) pass_asat_seasons records engine_head, rl_model, config and fv in each bank; rl_export reads the two
banks and HALTS only if a bank is missing or one of THOSE FOUR differs from the live tree. Store and board are excluded
by rule: the pass rewinds the store to season Y, and the board is an output (otherwise every weekly ingest, tools/player
act, P3-2 and this act itself would halt). An engine act that moves any of the four re-runs the pass as a declared
lander step after `repin` (P4-3) and before build_proofs, with both banks as carriers; (2) delete `back` and both lensConservation sums
over it (−1/−2 totals then mean "players on the as-at board who are still current" — say so in `_meta`);
(3) extract_board_view, board_values (and test_store_edit's fixture), extract_seam.test.py and its legf fixture, and
ownership_sidecar.test.js's orphan check (players + store-retired only) stop expecting `back`; (4) emit_asat_seasons stops
patching board_view_working.js and becomes the ui step's writer of asat_boards.js (add a carrier entry);
(5) the banks enter the proof-stash key (P4-3 trace; bump KEY_SCHEMA). The banks are re-stamped, not re-priced, before measuring.

**Owner ruling (2026-11-18) on `back`.** "Retirees - quarantine them outside of the board but sometimes guys come back
so not fully deleting them from the store might be a good idea." So Change (2) stands: retirees come OFF the board
(no `back` section). Their STORE rows are never deleted — a retired row stays in rl_model_data.json with `_retired`
and `_last_listed`, so a return is a store edit (`_retired` true→false), as Bedendo and Mirkov were on 2026-11-06.
Change (3) must also move the two readers the roster acts added: ownership_sidecar.test.js's orphan check (a movers
key not on the board must be a retired STORE row) and steps.py `board_values`/`board_movers` (a retirement then
reports as a vanish, not a move to `back`; the store-edit NOTE template should say so).
**Owner ruling (2026-11-18) on asat_boards.js.** "Make the as-at file a lander carrier": Change (4) makes
ui/data/asat_boards.js a carrier (tools/landing/carriers.py) that the lander's ui step regenerates from the banks on
every landing, as WRITER 9 does for the positions map. It has no ui/app reader yet; keep it current regardless.

**Must not change.** v, vP1, vP2 key for key; the store; the banks' `values` (only their stamp gains four fields); the present lens conservation.

**Prove it.** Measurement build first: per-row vM1/vM2 old vs new (count, median, largest movers, by age), the −1/−2
lensConservation before/after — shown to the owner. Then: v/vP1/vP2 identical; vM1/vM2 == banks; `back` absent;
every ui/tests suite (`node ui/tests/*.test.js`, `*.test.mjs`, `python3 ui/tests/*.test.py`); blind review filed.

**Lands via.** Lever act, `moves: [board]` (+ engine_head only if the engine is touched), movers declared, owner word.
