# How to update the LTI & availability register — RETIRED 2026-10-14

**The LTI register is retired on the owner's word ("retire the LTI register", 2026-10-14).** This
page used to be the owner's update path for `LTI_REGISTER.md` and its one command,
`tools/owner/lti_repin.py`. Both are deleted, with the parser `engine/rl_after/lti_register.py` and
the Part-2 return arm (`derive_lti_return.py`, `lti_return_table.json`) the register fed.

What replaced it, and had already replaced it in the engine since ORDER 42 (2026-08-20): the owner's
annotation sheet `docs/owner_annotations/SITTER_2026_v1.csv` is the ONLY injury truth. It is pinned by
`data/sheet_pins.json` (md5, row count, injured=Y count), the pin is a manifest-checked carrier field
(`release_manifest_check.py`), and the engine halts at ORDER 41 / ORDER 42 if the sheet and its
declaration disagree. The sheet is updated through the round lander (`tools/land round`), never by hand
against a stale pin.

The `register` identity (`652d83e8…`) stays in `data/expected_boot.json`, `data/release_contract.json`
and the UI stamp as a FROZEN HISTORICAL field — carried, never asserted against a file, exactly as
`balanced_board_md5` is carried since the balanced sibling's retirement the same day. See
`docs/runbooks/WEEKLY_SCORES.md` for the one-paragraph record.

The pre-retirement text of this page is in git history (`git show 3911fdfc:docs/HOW_TO_LTI.md`).
