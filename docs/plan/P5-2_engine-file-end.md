# P5-2 — The engine file ends where the engine ends (MEDIUM; board byte-identical)

**Depends on.** P4-3 (engine_head is declared in `moves`, no hand flip). Serial rule: engine + harness.

**Done when.** engine/rl_after/_merged_recover.py no longer contains the demo tail (lines 6299-6347, from
`print("=== AFTER (wired: delist + staleness + isotonic) — named players ===")` to end of file), rl_export.py and
the harness exec the whole file, the harness asserts the marker is ABSENT, and the board is byte-identical.

**Facts (checked at ffb2663b).**
- The file is 6,347 lines; the marker is line 6299 and is the only occurrence (`grep -n "=== AFTER"`).
- rl_export.py:68 execs `open('_merged_recover.py').read().split('print("=== AFTER')[0]`.
- tools/harness_run.py:39 defines TAIL_MARKER and :71-74 STOPS ("the script-tail marker … is not in
  _merged_recover.py") if it is gone; :76 execs the slice. This is the one site that breaks.
- `s.split(m)[0]` returns the whole of `s` when `m` is absent. So once lines 6299-6347 are deleted, every other
  slicer execs exactly the text it execs today (lines 1-6298). Live slicers (`git grep -n "=== AFTER" --
  ':!docs/evidence' ':!session_*' ':!backups' ':!docs/plan'`): rl_export.py:68, one_source_selftest.py:112 (not :153),
  ship_gates_check.py:165 (a retired instrument, RULEBOOK.md:102), tools/landing/day0_emit.py:118,
  ui/tools/gen_v0_sidecar.py:135, verify/d15/_d15_common.py:75, run_panel.sh:48, verify_restore.sh:28, 30 scratch
  scripts engine/rl_after/_*.py and 4 engine/rl_after/s4_matrix_*.py. refit_q97m.py:73 only mentions the marker
  (it splits at the q97m load). 188 more copies live under docs/evidence/ and session_*/ — historical, leave them.
- The D7 comment block (_merged_recover.py:5969-5985) explains that rl_export truncates at this sentinel and
  warns never to write it verbatim; it must be reworded in the same edit.

**Change.**
1. Delete lines 6299-6347. Reword the D7 comment (no behaviour change).
2. rl_export.py:68, one_source_selftest.py:112, day0_emit.py:118, gen_v0_sidecar.py:135: exec the whole file.
3. tools/harness_run.py in the SAME commit: exec the whole file and assert the marker is NOT present (a re-added
   tail is then a halt, keeping the "boundary moved deliberately" property its comment at :36-38 asks for).
4. Leave the other slicers (they are equivalent by the split rule above). Making the module importable is NOT in
   scope: import would run module-level code that needs RL_REPO and the engine cwd.

**Must not change.** The text exec'd: `old_src.split('print("=== AFTER')[0] == new_src` must hold byte for byte.
Every module-level statement above line 6299. The board (96896e1c), store, config.

**Prove it.**
- The string identity above (print both sha256s in the commit message).
- Bare canonical build byte-identical (README recipe); `tools/harness docs/evidence/walkforward_retro_2026-08-29/
  pass_asat_seasons.py` still loads, its Y=2026 control passes (pass_asat_seasons.py:47-50) and `git diff
  --exit-code` holds on the values_asat_*.json banks it rewrites; run engine/rl_after/one_source_selftest.py yourself
  (acceptance `oneliner_f1_lens` only reads its text, acceptance/checks/m1a.py:296-305); acceptance `--profile full`.
- The lever act: `moves: [engine_head]`, `prereg.board_before == board_after == 96896e1c…`.

**Lands via.** Lever act (after P4-3), board declared unmoved by prediction; the lander proves it.
