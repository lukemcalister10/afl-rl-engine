# P2-3 — The whole-row store verbs and `tools/player` (MEDIUM)

**Goal.** `tools/player add|move|retire|set` as the owner's one command for roster facts, each landing through
the store-edit lane: `add` creates a row (new lane verb `add_row`: the full row object, inserted at the end of
the store array in the file's own spacing, key unique); `retire` sets `_retired true` + `_last_listed Y`
(two `add`/change edits); `move` changes `afl_club` (today's courier in ui/tools/ownership_store_apply.py does
this from the locations sheet — `move` is the one-player form of the same write, or it calls the courier);
`set` is a single flat-field change (the existing change verb). Every verb: `--check` prints the edits and the
predicted movers (the lane's dry run) and does nothing.

**Why.** Today a new player (e.g. a mid-season signing) has no path but a hand edit of a 5 MB one-line JSON;
the lane "never creates a row". The add-field verb (2026-10-14) is the precedent and the pattern.

**Files.** tools/landing/steps.py (`apply_store_edits`: the `add_row` verb with the same byte-reverse proof),
tools/landing/spec.py (validation), tools/landing/test_store_edit.py, new tools/player.py (+ tests), docs/runbooks/.

**Rules.** A new row must carry every field the engine requires (read rl_model.py's load; the schema the
store rows share: player, pick, year, type, drafted_position, present_position, key, games, scoring, _has26,
_retired, _by, _cat, _draft, _draft_club, _pickless, future_position, …) — the verb validates the row against
the set of keys the file's rows carry and refuses a row with unknown or missing keys. `retire` on an active row
moves the board (the row leaves the active section): the spec declares the movers; the dry run predicts them.
No courier of the locations sheet changes.

**Proof.** test_store_edit (add_row happy path, duplicate key refused, bad schema refused, byte-reverse);
tools/player tests; one rehearsal act on a scratch worktree (add a synthetic player, retire him) landed end to
end with no push; acceptance green.

**Lands via.** Plain commits for the tool; real roster changes then land as store-edit acts.
