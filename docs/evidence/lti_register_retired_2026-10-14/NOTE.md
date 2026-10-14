# The LTI register retired — engine/tools act, 2026-10-14

Owner word (in chat, 2026-10-14, to "retire the LTI register"): "5. Agree".

## What changed
- Deleted: `LTI_REGISTER.md`, `engine/rl_after/lti_register.py`, `engine/rl_after/derive_lti_return.py`,
  `engine/rl_after/lti_return_table.json`, `tools/owner/lti_repin.py` (+ its test). The owner sheet
  (`docs/owner_annotations/SITTER_2026_v1.csv`, ORDER 42) has been the only injury truth; `build_state` was never
  called, and the Part-2 return arm could never fire (`return_arm` is False for every sheet entry), so
  `_lti_ret_hc` was 0 on every row. The arm, its table load/halt and its never-true multiplier sites are gone.
- `rl_export.py` no longer stamps `lti_register_md5` into the board (the only board bytes that move).
- The `register` identity is frozen as a historical field (expected_boot / release_contract keep the value; nothing
  re-hashes it; `spec.py` refuses it in `moves`; STATE.md shows it beside `balanced_board_md5`). Every existing
  ACT_SPEC still validates (8/8). Guard 5, bootstrap, the harness, staged_apply, the acceptance r14 restore control
  and the seat scripts no longer look for the file.
- Docs: WEEKLY_SCORES.md paragraph; REQUIRED_INPUTS.md row RETIRED; HOW_TO_LTI.md is a stub pointing at the sheet.

## Proof (build on the act tree, store b0eeaf4b)
See REPORT.json / FLIGHT.log: the predicted board differs from the live board e40c37cc by the dropped top-level
key only; every other key byte-identical as JSON. No player value, rank or lens value moved.
