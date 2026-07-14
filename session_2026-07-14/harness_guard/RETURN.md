# RETURN — anti-copy rule made a GUARD (supervisor seat 5, owner-ruled 2026-07-13)

- **branch**: `claude/anti-copy-guard-enforcement-bj9ivh` · base main @ `7e2e1ed` (PR #72 merge)
- **head SHA**: `f2e3322` (this doc-update rides on top) · **PR**: #73 (draft candidate — do not merge, do not tag)
- **canonical suite runner**: `ship_gates_check.py` — the ONE committed suite runner; a build CALLS it
  with config (`SGC_SKIP`/`SGC_REPORT_DIR`/`SGC_B1_MATRIX`/`SGC_HARNESS_ONLY`), never copies it.
- **lookalike threshold (H1)**: `ov_can ≥ 0.50` AND `≥ 12` shared significant lines, where `ov_can` =
  (shared significant lines)/(canonical runner's significant lines). WHY: tree-wide max `ov_can` today =
  **0.136**, so 0.50 is a 3.7× margin (zero false positives) while a genuine copy ≈ 1.0; the 12-line floor
  stops coincidental matches against the small runners (setup_env 15 / run_panel 22 sig lines).
- **allowlist (data/harness_manifest.json)**: H1_lookalike.allowlist = **EMPTY**; H2_masking.allowlist =
  **EMPTY**. The only live masking finding (`verify_restore.sh:49`, a masked panel display) was FIXED, not
  allowlisted. 15 closed-session scripts carry the historical pattern — OUT of scope by rule (the record).
- **acceptance** (proofs in `session_2026-07-14/harness_guard/`; `out/rc_A*`, exit codes):
  - **A1 lookalike bites** — PASS. Copy → suite HALTs naming `ship_gates_lookalike_COPY.py`, rc=1; delete → green, rc=0.
  - **A2 masking bites** — PASS. `| tail` runner → HALTs naming `run_gates_masked_PROOF.sh`, rc=1; remove → green, rc=0.
  - **A3 zero false positives** — PASS. H1 flags 0; H2 flagged 1 (fixed). Both allowlists empty.
  - **A4 config stamp halts a stale book** — PASS. Config-mismatched book via `SGC_B1_MATRIX` → B1 HALT
    naming the config mismatch (rc=1); matching config → stamp accepts the book. (Cheap; no hot bake.)
  - **A5 nothing green turned red** — PASS. reds exactly {A2,A3,A12}; B1 PASS 1.2601/1.2407/1.1521;
    panel 10/10; Guard 5 green; H1/H2 PASS; store `340a7a32` and board `3dc19fbb` byte-identical.
- **confirmation**: store `340a7a32` and board `3dc19fbb` byte-unchanged; NO existing gate's construction
  changed (H1/H2 are ADDED; the config_sha256 assertion was already wired via PR #66 — this job verifies it).
- **note**: setting `SGC_REPORT_DIR` in the ambient env leaks into B1's gate-mode regen subprocess, which
  `config_manifest.enforce` then rejects (item-38 SGC_* fail-close) — a loud HALT, not a silent pass, so
  left as-is; flagged for a future harness-hygiene pass (scrub SGC_* from the regen env).

## In plain terms
The rule "don't copy the build runner" used to be a sentence. Nothing stopped anyone from ignoring it, so
it rotted — exactly the store-copy messes we already fixed, but for code. Now the suite itself refuses to
pass if a second copy of a runner shows up anywhere in the tree (H1), or if any live script hides a gate's
failure behind `| tail` / `|| true` / a missing `pipefail` (H2). Both point at the same idea that already
holds the store together — a copy becomes a red the moment it exists, not three chapters later. And a
formula change smuggled through config can no longer certify an old walk-forward book: the book's config
fingerprint is now checked like its code and store fingerprints already were. One canonical runner; every
exception written down in one owner-visible file, with a reason.
