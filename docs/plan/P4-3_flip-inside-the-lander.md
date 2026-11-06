# P4-3 — The engine and config flip move inside the landing transaction (MEDIUM)

**Depends on.** P4-2 (serial rule: steps.py, spec.py). Unblocks P5-2, P5-1, P5-4, P5-3, P3-1, P3-2.

**Done when.** A lever/edit spec may declare `engine_head`, `rl_model`, `fv`, `config` in `identities.moves`; the
launch checks accept that tree; the lander writes the MEASURED pins after the restore point and BEFORE the build; the
proof stash keys on every file the build opens; old specs still validate and land; a rehearsal lands an engine-only
change end to end with no hand flip, getting past launch, the self-test and every step.

**Facts (checked at ffb2663b).**
- spec.py:65 FLIP_SCOPED_IDENTITIES (engine_head, rl_model, fv, config, v0surf); :481-488 refuses them in `moves`.
  steps.py:120-124 cross-asserts FLIP_SCOPED ⊆ PIN_MEASURERS. No `contract` identity exists (spec.py:43-45).
- Step order (steps.py:3800-3811): preflight (restore point) → build_proofs → pins → lineage → contract → ui → …
  pins (:1287-1389) writes declared PIN_MEASURERS identities, but only after the build.
- The landing build runs `mode='dev'` (steps.py:1114), so rl_export.py:36-44's config check and
  assert_fv_provenance do NOT run there (an earlier version of this brief said they did — wrong). Pins must still be
  written before the build because the contract step asserts measured == expected_boot for config/engine_head/
  rl_model/fv (:1642-1650) and the gates (release_manifest_check, release_contract check) read them.
- LAUNCH: cli._run_cheap_preflight (cli.py:171; used by cmd_lever :223, cmd_edit :324, and tools/ingest.py:459)
  runs preflight.py checks against HEAD before the lock: pins_vs_tree (:101-121, already skips `moves`), release_contract.py check
  (:124-128), release_manifest_check.py (:130-135; it computes engine_head/rl_model from the tree,
  release_manifest_check.py:156-157, and reports DRIFT against the pins), tools/restamp.py check (:170-176). With
  engine source committed and pins unmoved these FAIL → no transaction opens; a config change also fails
  config_sha256.
- SELF-TEST: cli._preflight_selftest (cli.py:78-150) runs selftest.main before every `tools/land` transaction, cut from
  `coherent_base` or HEAD (the ruling at cli.py:106-112 wants a tree where pins == source). selftest.py:482-485 loops
  over EVERY LEVER_SEQUENCE step and reads `TX.FAULTS[step_name]` — a new step without a FAULTS entry raises KeyError.
- proofstash.build_key (proofstash.py:93-108) skips identities in `moves` (:99-100) → blind to engine edits.
  BUILD_INPUT_FILES (:59-62) is a hand list that misses files the build opens: rl_export.py, single_source.py,
  owner_overrides.py, wire_redesign.py, pgrid.py, and data files rl_model opens by cwd — params.json, rl_passmark.json
  (rl_model.py:5), national_draft_last_pick.json (:274), peak_model_v4.pkl, bust_prior_table.json, pvc_snapshot.json
  (:1255-1257), pvc_curve_v2.json (:1613).
- data/expected_boot.json is a carrier (carriers.py:109); data/model_config.json is not (a config change rides the
  input commit with its `config_sha256` recomputed, config_manifest.py:185-192).

**Change.**
1. spec.py: drop engine_head, rl_model, fv, config from FLIP_SCOPED (v0surf stays: a surface is a bake).
2. Launch: preflight.py's release_contract, release_manifest and identity_stamps checks exempt exactly
   the identities the spec declares in `moves` (still FAIL on any other drift). Self-test: set/require `coherent_base`
   = the commit before the source change for such specs (or derive it), so the sandbox has pins == source.
3. New step `repin` between preflight and build_proofs, with `txn.FAULTS['repin']` and its self-test leg: for each of
   the four in `moves`, measure, HALT if equal to the pin, replace textually (old value once, :1335-1346), re-read.
   pins then counts them as moved against the base-commit values. Under `--dry-run` repin writes nothing and records
   the measured values in ctx.facts; the contract step compares against those facts instead of the file.
4. proofstash: key on every PIN_MEASURERS identity except `board`, moving or not, plus every file the build opens —
   enumerated by an import/open trace of one real build (commit the trace script and its output), not a hand list;
   KEY_SCHEMA = 3. docs/runbooks: "commit the source, declare it in moves". restamp.py `apply` = hand recovery only.

**Must not change.** Behaviour for specs declaring these identities `unmoved`; the `unmoved` assertions (:1347-1357);
the "exactly the declared set moved" check; v0surf; launch-check strictness for undeclared identities.

**Prove it.** test_proofstash (key moves on each identity and each traced file, in `moves` or not); test_txn (repin
writes; abort restores; dry-run writes nothing); `tools/land selftest` green with the repin leg; spec baseline (say if
ACT_SPEC_P3A now passes). Rehearsal on a worktree with a scratch remote (no push): commit a comment-only edit to
_merged_recover.py, `tools/land lever` with `moves: [engine_head]`, board_before == board_after = 96896e1c — it must
pass launch, self-test and land; then `python3 tools/restamp.py check` all agree (restamp.py:140-145). Repeat with a
config-only change on the scratch worktree. Commit the evidence. acceptance `--profile full`; test_restamp.py.

**Lands via.** Plain commit of the lander; the rehearsal evidence is the proof.
