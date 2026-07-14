# SUITE HYGIENE — RETURN (silent-failure class; proofs finished)

- **branch**: `claude/suite-hygiene-silent-failures-f9wgwb`
- **head SHA**: `f4c3e8c` (proofs+logs+RETURN commit; a one-line stamp commit rides on top with PR/SHA)
- **PR**: **#72** (candidate — NOT merged, NOT tagged) · https://github.com/lukemcalister10/afl-rl-engine/pull/72

## The four acceptance results (each with proof file · exit code · before→after)
- **A1 — bake halts on a broken export** · `proofs/A1_bake_halts_on_broken_export.sh` · **exit 0 (PASS)**.
  Scratch bake with a 2-line broken workspace `rl_export.py` (real one untouched): **before** the unmask it
  copied+re-pinned a board it never built; **after**, bake **exit 3**, published nothing, re-pinned nothing —
  board `3dc19fbb` byte-identical, boot-pin `3dc19fbb`. Stub exits instantly; engine never loads.
- **A2 — a swallowed failure cannot survive** · `proofs/A2_swallowed_failure_cannot_survive.sh` · **exit 0 (PASS)**.
  Three worst live-harness sites, before→after exit: run_panel.sh computed-FAIL **0→1**; bootstrap.sh md5-pipe
  on a missing seed **0→1**; verify_restore.sh with a real chk FAIL **0→1**. (Fixed this run: the "before"
  baseline was reading the already-committed hardened HEAD; repointed to the pre-hardening base `c3b0337^`.)
- **A3 — nothing green turned red** · `proofs/A3_nothing_green_turned_red.sh` · **exit 0 (PASS)**.
  One real `ship_gates_check.py` (`A3_ship_gates.log`): reds **exactly {A2, A3, A12}**; **B1 PASS
  1.2601 / 1.2407 / 1.1521** on the July-8 construction; VERDICT FAIL=3 PASS=17 (== baseline); panel **10/10**;
  Guard 5 boot-store + collision sentry green. SSI guards 1–2/F1–F2 need the baked, read-only, `.srcmd5`-stamped
  board+book in the workspace — an out-of-fence bake — so per RULE 1 they are certified in-suite instead by
  ship_gates B3 (book seal MATCHES) + B4 (board byte-agree, export exit=0) + D14a/b/c, all PASS.
- **A4 — nothing else moved** · `proofs/A4_nothing_else_moved.sh` · **exit 0 (PASS)**.
  store `340a7a32` (repo source + workspace) and board `3dc19fbb` byte-identical; boot-pin `3dc19fbb`; the ONLY
  non-session-dir changes vs base are the **5 named harness/doc files**; engine `_merged_recover`/`rl_model`,
  `config_manifest`, `model_config.json`, `ship_gates_check.py`, `boot_guard` all byte-identical to base.

## Confirmations
- **store/board byte-unchanged** (A4): store `340a7a32`, board `3dc19fbb` — no movement.
- **no gate CONSTRUCTION touched** (A4): only propagation (`set -o pipefail`/`-e`/`-u`, captured `rc`, authoritative
  `exit`) changed; no gate's computation changed. Derived suite report regenerated on the A3 run and was reverted
  (`git checkout --`); nothing else dirty.

## In plain terms
The harness now obeys "silence is a red." Break the export and the bake stops instead of pinning a board it never
built; make any of the three worst runners fail and the failure now shows up as a non-zero exit instead of a green
lie — while every gate still computes exactly what it did before, on the same store and the same board.
