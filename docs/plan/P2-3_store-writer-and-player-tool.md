# P2-3 — Whole-row store verbs and `tools/player` (MEDIUM)

**Depends on.** P4-2 (serial rule: tools/landing/steps.py, spec.py). Needed by P3-2 (draft intake, delistings).

**Done when.** `tools/player add|retire|move|set … [--check]` builds a store-edit spec and lands it through the edit
lane; `add` uses a new lane verb `add_row` with the same byte-reverse proof as the existing verbs; `--check` prints the
edits and stops; a rehearsal adds and then retires a synthetic player end to end on a scratch worktree (no push).

**Facts (checked at ffb2663b).**
- The store engine/rl_after/rl_model_data.json is 1,982,499 bytes (≈2 MB, not 5 MB), ONE line, a JSON list of 2,650
  rows. Keys: 31 in the union, 19 on every row: `_by _cat _draft _draft_club _has26 _pickless _retired draft_stream
  drafted_position future_position games key pick player present_position scoring stream_year type year`. The other
  12 (count of rows): `_bd` 1150, `_force_active` 63, `_last_listed` 214, `_pick_source` 8, `affl_team` 804, `afl_club`
  804, `alternate_position` 804, `eligibilities` 804, `p_dual_stream` 804, `pick_correction_note` 1041,
  `stable_player_id` 804, `stream_pick` 2367.
- The lane today: `apply_store_edits` (steps.py:547) — a change verb (`old`/`new` on an existing field) and the
  `add` verb for a new top-level field (`_ADD_FIELD` :390, :477); no verb creates or removes a row.
- The season clock: steps.py:872-892 re-derives season_state from the edited store at the CURRENT as_of_round and
  STOPS if anything but `source_store_md5` moves; the finals hold (:913-958) applies only at the round-24 ceiling.
  Adding or retiring a row that has current-season games can move exposure_pace (the durable median,
  season_state.py:100) and trip that stop.
- `_has26` is on all 2,650 rows and test_has26_derived.py:51-53 asserts it; a new row must carry it.
- The courier for clubs from the locations sheet: ui/tools/ownership_store_apply.py.

**Change.**
1. `add_row` verb (steps.py + spec.py validation): the full row object, appended at the end of the array in the
   file's own compact spacing; key unique; REQUIRED keys = the 19 shared; ALLOWED keys = the 31 in the union;
   anything else refused. Byte-reverse proof: removing the appended bytes restores the original exactly.
2. tools/player.py: `add` (from a JSON/CSV row), `retire KEY --last-listed Y` (two change edits: `_retired`, and
   `_last_listed` as `add` when absent), `move KEY CLUB` (one change edit on `afl_club`, refused for the 1,846 rows
   that have no `afl_club`), `set KEY FIELD VALUE` (one change edit). Each writes a spec like tools/ingest.build_spec
   (ingest.py:388-437) and lands it through `tools/land edit` (cmd_edit, cli.py:305 — launch checks and the
   pre-transaction self-test run; this is not P14's weekly path); `--check` = the lane's dry run.
3. When the season-clock stop fires, the tool says so plainly (the act is a re-derivation and needs its own word).

**Must not change.** Existing verbs and their proofs; the store bytes for any act that does not use `add_row`; the
courier; the season-clock stop (do not weaken it to make a roster act pass).

**Prove it.** tools/landing/test_store_edit.py (add_row happy path; duplicate key, missing required key, unknown key
refused; byte-reverse); tests for tools/player (each verb's generated spec validates with spec.py); the rehearsal act
on a scratch worktree with a scratch remote (add a synthetic 0-game player, land; retire him, land; assert the
store differs from the original only by the appended row with `_retired`/`_last_listed` set); acceptance
`--profile full`. test_has26_derived.py:52 asserts exactly 2,650 rows (a typed number; RULEBOOK P4): replace it in this
item with a relationship (e.g. rows == boot-pinned store's row count) so the first real `add` does not red it.

**Lands via.** Plain commits for the tool and verb; real roster changes then land as store-edit acts (value-moving
→ movers shown; the draft intake is part of P3-2).
