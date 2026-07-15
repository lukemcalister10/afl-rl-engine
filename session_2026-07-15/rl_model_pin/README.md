# rl_model pin — asserted by boot_guard (Guard 5)

**Directive:** GUARD — assert the `rl_model` pin in `boot_guard` (L-CAPTAIN prerequisite (1), Tier-1-LITE, 2026-07-15).
**Base (STRICT):** improver build's returned head `2c7b905cb7f47c87a96fd5150177e856b4c14b70` (PR #90), owner-confirmed.
Merge line: `#82→#83→#85→#89→improver→this`.

## What changed
The `rl_model` pin in `data/expected_boot.json` (`952ddb3d15fe6d4f72432d431abe75cc`) was present and
**correct** but never **checked** — the one engine source Guard 5 did not assert. `boot_guard.py` now
asserts it on entry exactly as it asserts the store: block **(0f)** computes the md5 of the checked-out
`engine/rl_after/rl_model.py`, compares (full-hash) to the pin, and **HALTs** (never warns) on mismatch.
The PASS line prints the verdict (SILENCE IS A RED): `rl_model 952ddb3d == pinned 952ddb3d`.

Fence: `boot_guard.py` only (no pin-format touch was required — the pin already existed) + this session dir.
Store, board, config, engine, docs untouched. This job moves **no** value.

## Proofs (in this dir)
- `redpath_evidence.txt` — negative test in an isolated scratch checkout: pristine copy PASSES (exit 0);
  corrupting only `rl_model.py` makes boot **HALT** with the `checkout rl_model … != pinned rl_model …`
  message and **exit 1**; real repo file untouched (`952ddb3d…`).
- `green_evidence.txt` — fresh bootstrap PASSES all guards incl. the new assertion; board md5
  `dc43d602c5140cac5be8e668380dda6e` **unchanged** from base (both printed).
