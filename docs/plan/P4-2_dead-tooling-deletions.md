# P4-2 — Delete the tooling that is actually retired, and nothing that is live (LOW)

**Depends on.** P4-1a (both edit tools/landing/steps.py; serial rule).

**Done when.** The three units below are gone or made optional, each in its own commit naming the ruling, every
reader of each unit is retired in the same commit, and the KEEP list is untouched.

**Facts — what is live and must be KEPT (the old brief listed these as dead; it was wrong):**
- acceptance/selftest.py — the acceptance runner's own self-test, run by CI first
  (.github/actions/host-insensitive-gates/action.yml:72).
- tools/landing/selftest.py — the lander runs it before EVERY transaction (cli.py:78-150, called at :231, :293,
  :335); preview.py:161-165 builds its Sandbox from it; acceptance registers it as `lander_selftest`
  (acceptance/checks/landing.py:43-71, PROFILE 'full'). RULEBOOK P7 retired the ruled-red ledger and P9 the
  prereg ceremony (RULEBOOK.md:145, :150); neither retired the lander self-test. The `--selftest` paths in cli.py
  are its practice landings: keep them.
- engine/rl_after/ingestion/sibling_repin.py + forward_lens.py — live inside the round lane: staged_apply.py:883-884
  loads sibling_repin (c3), which loads forward_lens (sibling_repin.py:82-84). They go with the lane in P4-4.
- tools/landing/day0_emit.py — DAY0_GENERATOR (steps.py:3438) for the round lane's `day0` step (:3365-3433).
  Goes with the lane in P4-4.

**Unit 1 — tools/claims.py and the `claims` step** (retired by RULEBOOK law 11, RULEBOOK.md:46-48).
Readers to retire in the same commit: steps.py `claims` (:2580-~2690) and its entries in LEVER_SEQUENCE (:3809)
and ROUND_SEQUENCE (:3856) — EDIT_SEQUENCE inherits it from LEVER_SEQUENCE (:3871-3875); txn.py:449 FAULTS['claims'];
selftest.py:25, :105, :1144-1147 (the claims leg); tools/ingest.py:463 (the filter that drops the step: delete it).
**Unit 2 — `day0_rebase` becomes optional** (owner: off; the M1b ruling quoted at steps.py:1226-1229).
It is a REQUIRED_SLOT (spec.py:70-71) validated at :515-529; four existing specs carry `"state": "on"`
(r24_advance ACT_SPEC_R24, combined_build ACT_SPEC_COMBINED, two r24_rehearsal specs) and must still load.
Change: drop it from REQUIRED_SLOTS, keep the validation when the slot is present, absent = off. proofstash.build_key
reads it (proofstash.py:105): normalise `spec.get('day0_rebase') or {'state': 'off'}` so existing stash keys do
not move. Leave steps.py `_day0` (:1214, :1223) for the lever lane's off path; the `on` path stays until P4-4.
**Unit 3 — dead function** engine/rl_after/ingestion/scratch_fixture.py `align_to_config_of_record` (:406-~470)
opens sibling_repin.py (:427) and has no caller (`git grep align_to_config_of_record` = its definition only).
test_r14_fixture.py uses `install_sibling_support_trees` (:235), not this; leave that.

**Rule for each unit.** `git grep -n <symbol> -- ':!docs/evidence' ':!session_*' ':!backups'` across tools/,
acceptance/, .github/, engine/, ui/, docs/runbooks/, docs/RULEBOOK.md. A live reader you cannot retire in the
same commit stops that unit: report it, do not delete. The RULEBOOK is not edited (law 10a).

**Must not change.** The board, the store, any pin. The 28 specs that validate today still validate (the README's
spec baseline). The KEEP list above. Stash keys for existing specs.

**Prove it.** `python3 tools/landing/test_txn.py`, `test_proofstash.py`, `test_store_edit.py`,
`test_finals_bounds.py`; `python3 tools/test_restamp.py`; `python3 tools/test_ingest.py`;
`python3 ui/tests/ownership_store_apply.test.py`; `tools/land selftest` (the lander's own self-test, legs
reduced by exactly the removed claims leg); the spec baseline (validate every ACT_SPEC*.json); `tools/ingest --check
scores/GF.csv` still stops cleanly with "already on the board" (ingest.py:189-191); acceptance `--profile full`; CI green.

**Lands via.** Plain commits, one per unit, each message naming the ruling that retired it.
