# SEAM ADOPTION-REVIEW EVIDENCE — #271, filed at the v541 adoption pen under docs/evidence/adoption_review_2026-07-30/ (seam, 2026-07-30)
The owner's adoption review basis (Addendum 14 rests on it). All figures computed from committed artifacts;
the two counterfactual boards were built in scratch worktrees at e2eac1b/e51a19d under the pinned cp312 env
(env -i, PYTHONHASHSEED=0, single-thread BLAS), never committed, deterministic across two runs each.
- board_review_before_after.csv — shipped board 3d4e2e50 → candidate f2df6e0a, per player, cause-flagged.
- board_review_step_by_step.csv — adds the committed intermediate (stage A dca21c91) + stage-A internal split.
- board_review_four_levers.csv — the full decomposition; telescopes EXACTLY per player:
  v_baseline + d_your_edits + d_rebake + d_axis + d_bars + d_curve_pool = v_final (asserted for all 804).
  Lever totals: edits +2,575/429 · rebake +895/132 · axis +17,068/641 · bars +11,620/228 · curve+pool −1,540/160.
- cf_values.csv — CF1 board (md5 0a3ef5b8...): stage-B engine code + PRE-#271 curve (1554b98e) + stage-A
  surface (19d085a2). final−CF1 = curve+pool per player; CF1−stageA = whole engine channel (reproduces the
  sealed 647/160 key sets exactly, incl. the 13 round-trip rows).
- cf2_values.csv — CF2 board (md5 78753e29...): CF1 config + the bar-sourcing hunk of rl_model.py reverse-applied
  (cf2_surgery.diff; the 0b105d9→e51a19d diff separates cleanly: hunk 1 = bars, hunks 2–10 = axis). Validated:
  137/137 YEAR0_BAR_MOVERS reproduce bar_before; §1b resurrects at exactly 86/804; additivity exact.
  CF2−stageA = axis per player; CF1−CF2 = bars per player.
- VOR instrument note: adjacent-pair inversion counts are tie-sensitive (305 shared-integer rows). The canonical
  order-independent figure: 7,496 of 322,531 strictly-ordered pairs invert = 2.32% (Addendum 13).
