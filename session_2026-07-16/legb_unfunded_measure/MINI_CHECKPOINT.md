# MINI-CHECKPOINT — RL_UNCONSERVE toggle · diff prescreen · HALT before measurement

- **Diff SHA:** `6d9a4269` (branch `claude/legb-unfunded-measurement-1f7vym`, off base `91d08f2`).
- **Change:** +2 lines / 1 modified across 2 engine files. rl_model.py declares `_UNCONSERVE`
  (default OFF); `_merged_recover.py:332` applies C≡1 when `RL_UNCONSERVE=1`, else shipped `_UC_C`.
- **A/B PROVEN byte-exact:** RL_UNCOMP=0, toggle-unset default, and RL_UNCONSERVE=1(no s) all build
  board `8d90c9ac`. Store `b1fd0bce` untouched; UNCOMP_S_DEFAULT=None, UNCOMP_DECAY=0.25 unmoved.
- **HALT:** measurement grid (5 ON-points, ~2–3.5 h engine loads) proceeds only after the supervisor
  prescreens this diff. Ships nothing.
