# P2-3 — Whole-row store verbs and `tools/player` (MEDIUM)

**Depends on.** P4-2 (order only: with `add_row` landed this item no longer edits steps.py or spec.py). Needed by
P3-2 (draft intake; the end-of-2026 delistings already landed, 777c8f47).

**Done when.** `tools/player add|retire|move|set … [--check]` builds a store-edit spec and lands it through the edit
lane; `add` uses the lane's existing `add_row` verb (landed b52b74e5); `--check` prints the edits and stops; a
rehearsal adds and then retires a synthetic player end to end on a scratch worktree (no push).

**Facts (checked at 9a400286).**
- The store engine/rl_after/rl_model_data.json is 1,986,282 bytes (≈2 MB, not 5 MB), ONE line, a JSON list of 2,652
  rows (701 not retired). Keys: 31 in the union, 19 on every row: `_by _cat _draft _draft_club _has26 _pickless _retired draft_stream
  drafted_position future_position games key pick player present_position scoring stream_year type year`. The other
  12 (count of rows): `_bd` 1152, `_force_active` 66, `_last_listed` 321, `_pick_source` 8, `affl_team` 808, `afl_club`
  808, `alternate_position` 806, `eligibilities` 808, `p_dual_stream` 806, `pick_correction_note` 1041,
  `stable_player_id` 806, `stream_pick` 2367.
- The lane today: `apply_store_edits` (steps.py:940) — a change verb (`old`/`new` on an existing field), the `add` verb
  for a new top-level field (`_ADD_FIELD` :390, :523), the `scoring[Y]` season add (`_SEASON_ADD_FIELD` :618,
  `_apply_add_season` :682) and `add_row` (`_apply_add_row` :854-937; spec.py `_validate_add_row` :432). `add_row`
  measures the row shape off the store (`_row_shape` :778: REQUIRED = the 19 keys on every row, ALLOWED = the 31 in the
  union, key order = the rows' majority pairwise precedence), appends at the end with the file's separator, and
  store_edit re-reads the row and asserts the row count moved by exactly the adds (:1218-1262); the reverse check
  (:1125-1140) covers it. Both verbs landed in
  b52b74e5 with tests in tools/landing/test_store_edit.py. No verb removes a row.
- Hand-written precedents for the specs tools/player must generate: docs/evidence/store_edit_roster_returns_2026-11-06/
  ACT_SPEC.json (2 `add_row`, 2 un-retires `_retired`/`_last_listed`, `scoring[2026]` adds, field adds) and
  docs/evidence/store_edit_delistings_2026_2026-11-06/ACT_SPEC.json (107 × `_retired` change + `_last_listed` add).
- The season clock: steps.py:1316-1336 re-derives season_state from the edited store at the CURRENT as_of_round and
  STOPS if anything but `source_store_md5` moves; the finals hold (:1355-1402) applies only at the round-24 ceiling.
  Adding or retiring a row that has current-season games can move exposure_pace (the durable median,
  season_state.py:100) and trip that stop.
- `_has26` is on all 2,652 rows; test_has26_derived.py:53-59 asserts it on every row and the row count as a floor
  (`>= 2650`, b52b74e5); `add_row` refuses a row without it (required key).
- The courier for clubs from the locations sheet: ui/tools/ownership_store_apply.py.

**Change.**
1. `add_row` exists (Facts), byte-reverse proof included (apply_store_edits' reverse check, steps.py:1125-1140, treats
   an add as a record with an empty `old_text`). Do not re-implement or change it; tools/player only calls it.
2. tools/player.py: `add` (from a JSON/CSV row), `retire KEY --last-listed Y` (two change edits: `_retired`, and
   `_last_listed` as `add` when absent), `move KEY CLUB` (one change edit on `afl_club`, refused for the 1,844 rows
   that have no `afl_club`), `set KEY FIELD VALUE` (one change edit). Each writes a spec like tools/ingest.build_spec
   (ingest.py:388-437) and lands it through `tools/land edit` (cmd_edit, cli.py:305 — launch checks and the
   pre-transaction self-test run; this is not P14's weekly path); `--check` = the lane's dry run.
3. When the season-clock stop fires, the tool says so plainly (the act is a re-derivation and needs its own word).

**Must not change.** Existing verbs and their proofs; the store bytes for any act that does not use `add_row`; the
courier; the season-clock stop (do not weaken it to make a roster act pass).

**Prove it.** tools/landing/test_store_edit.py stays green (it already covers add_row's happy path and refusals); tests for tools/player (each verb's generated spec validates with spec.py); the rehearsal act
on a scratch worktree with a scratch remote (add a synthetic 0-game player, land; retire him, land; assert the
store differs from the original only by the appended row with `_retired`/`_last_listed` set); acceptance
`--profile full`. (test_has26_derived.py's row count is already a floor, so an `add` does not red it.)

**Lands via.** Plain commits for the tool; real roster changes then land as store-edit acts (value-moving
→ movers shown; the draft intake is part of P3-2).
