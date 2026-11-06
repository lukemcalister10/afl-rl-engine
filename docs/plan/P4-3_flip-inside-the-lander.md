# P4-3 — The engine and config flip move inside the landing transaction (MEDIUM)

**Depends on.** P4-2 (serial rule: steps.py, spec.py). Unblocks P5-2, P5-1, P5-4, P5-3, P3-1, P3-2.

**Done when.** A lever/edit spec may declare `engine_head`, `rl_model`, `fv` and `config` in `identities.moves`;
the lander writes their MEASURED pins into data/expected_boot.json after the restore point and BEFORE the build;
the proof stash keys on the measured value of every input identity; old specs still validate and land; and a
rehearsal act lands an engine change end to end with no hand flip.

**Facts (checked at ffb2663b).**
- spec.py:65 FLIP_SCOPED_IDENTITIES = engine_head, rl_model, fv, config, v0surf; :481-488 refuses them in `moves`.
  steps.py:120-124 asserts at import that FLIP_SCOPED ⊆ PIN_MEASURERS and NO_WRITER = TRACKED − PIN_MEASURERS −
  DELEGATED_PINS. There is no `contract` identity in TRACKED_IDENTITIES (spec.py:43-45).
- Step order (steps.py:3800-3811): preflight (restore point) → build_proofs → pins → lineage → contract → ui → …
  The pins step (:1287-1389) can already write any declared PIN_MEASURERS identity, but only AFTER the build.
- The build is canonical mode (`_build_child.py`, config_mode 'canonical'); rl_export.py:36-43 then verifies the
  config manifest against the `config` pin (config_manifest.enforce step 2, config_manifest.py:149-154) and calls
  boot_guard.assert_fv_provenance against the pinned `fv`. So a moved fv or config halts the build unless the new
  pin is already written. (engine_head/rl_model are checked later, by the contract step, steps.py:1642-1649.)
- proofstash.build_key (proofstash.py:93-108) SKIPS every identity in `moves` (:99-100). Declaring engine_head
  moving would make the stash blind to engine edits: a relaunch after a further engine edit could install a stale
  proof. KEY_SCHEMA = 2 (:50). BUILD_INPUT_FILES (:59-62) omits engine modules the build imports:
  rl_export.py, single_source.py (rl_export.py:7), owner_overrides.py (:762), wire_redesign.py
  (_merged_recover.py:25), pgrid.py (rl_model.py:3).
- data/expected_boot.json is a carrier (carriers.py:109), so the restore point puts pins back on abort.
  data/model_config.json is NOT a carrier: a config change is part of the act's committed input, with its own
  `config_sha256` field recomputed (checked by config_manifest.py:185-192 and acceptance config_manifest).
- The contract step writes config_sha256 + engine_head/rl_model/fv from measurement (release_contract.py:366-437).

**Change.**
1. spec.py: remove engine_head, rl_model, fv, config from FLIP_SCOPED_IDENTITIES (v0surf stays: a new surface is
   a bake, out of scope). Keep accepting them in `unmoved` (flip-carried old specs).
2. New step `repin` between preflight and build_proofs (LEVER_SEQUENCE, so EDIT_SEQUENCE inherits it): for each of
   those four in `moves`, measure via PIN_MEASURERS, HALT if equal to the pin, replace textually (old value must
   occur once — the pins step's own rule, :1335-1346), re-read. The pins step then counts these as moved (compare
   against the base-commit values captured by preflight, not the file as it now stands).
3. proofstash: key on `str(fn(ctx))` for EVERY PIN_MEASURERS identity except `board` (the output) — moving or not;
   add the five modules above to BUILD_INPUT_FILES; KEY_SCHEMA = 3.
4. docs/runbooks: the flip procedure text becomes "commit the source, declare it in moves". tools/restamp.py
   keeps `check`; `apply` stays only as a hand-recovery tool (say so in its docstring).

**Must not change.** Any landed artifact of a spec that declares these identities `unmoved` (byte-identical
behaviour). The `unmoved` assertions (:1347-1357). The pins step's "exactly the declared set moved" check. v0surf.

**Prove it.**
- test_proofstash.py extended: a key changes when engine_head, rl_model, fv, config, rl_export.py or any new
  BUILD_INPUT_FILES entry changes, whether or not it is in `moves`. test_txn.py: repin writes, abort restores.
- the spec baseline: the 28 still validate; say whether ACT_SPEC_P3A now passes.
- Rehearsal on a worktree with a scratch remote (no push): a comment-only edit to _merged_recover.py committed,
  then `tools/land lever` with `moves: [engine_head]`, `prereg.board_before == board_after` = 96896e1c; it lands,
  board byte-identical; then `python3 tools/restamp.py check` reports every stamp agreeing (board_view_working /
  club_valuation carry engine_head, restamp.py:140-145). Repeat with a config-only change on the scratch worktree
  (never pushed). Commit the rehearsal evidence dir.
- acceptance `--profile full`; `python3 tools/test_restamp.py`.

**Lands via.** Plain commit of the lander; the rehearsal evidence is the proof.
