# PLAN — anti-copy rule as a GUARD (supervisor seat 5 directive, 2026-07-13)

Branch: `claude/anti-copy-guard-enforcement-bj9ivh` · base main @ 7e2e1ed (PR #72 merge) —
diff since base is `docs/`-only-permitted; verified working tree clean, Guard 5 PASS
(store 340a7a32 / board 3dc19fbb). Canonical suite runner = **`ship_gates_check.py`**.

## What the base already has (measured, not assumed)
- **Piece 4 (config stamp) is ALREADY WIRED.** `ship_gates_check.py` L280-281 asserts
  `_meta['config_sha256'] == CONFIG_HASH` (guarded by `CONFIG_HASH is not None`, which is
  non-None in gate mode). The matrix generator `s4_matrix_M1v7.py` L105-109 stamps
  `config_sha256 = config_manifest.manifest_hash()` on the gate-regen path. It landed via
  PR #66 (`22dd592`), AFTER the directive/register-v78 text was written. So my job on
  piece 4 is **verify it bites (A4) + document it**, not re-add it. Current config hash
  `69ead79b944d…` == pinned boot `config`.

## The gap that is real (pieces 1-3)
SSI Guard 3 polices a second copy of the STORE (`rl_model_data*.json`). There is **no
equivalent tripwire for CODE**, and no behavioural lint for the `| tail` masking that
propagated the item-38 silent failure. That is what this job adds.

## Threshold calibration — MEASURED against the whole tree (446 tracked .py/.sh)
**H1 lookalike (line-overlap):** metric = `ov_can` = (shared significant lines) / (canonical
runner's significant lines) — "how much of a canonical runner is reproduced". Significant =
non-blank, non-comment, ≥8 chars.
- Tree-wide MAX `ov_can` today = **0.136** (3 coincidental env-export lines vs the 22-line
  `run_panel.sh`). A genuine copy reproduces ≈1.0.
- **Threshold: `ov_can ≥ 0.50` AND `shared ≥ 12` significant lines.** 0.50 is a 3.7× margin
  over today's max (zero false positives) yet fires on any copy edited up to ~50%; the
  `shared ≥ 12` floor stops a coincidental match against the small runners (setup_env 15 /
  run_panel 22 sig lines) — a real copy of those clears 12 easily (full copy = 15/22 shared).
- **Scan scope = the ENTIRE working tree** (os.walk, incl. untracked, so a not-yet-committed
  copy is caught), pruning `.git __pycache__ vendor backups node_modules`, excluding the
  canonical set + the H1 allowlist. Scanning session dirs is FREE here (max 0.136) and is the
  point: it catches a copy dropped in a session dir — exactly the deleted
  `cohort_gate_official.py` scenario.

**H2 masking lint (behavioural):** flags a LIVE harness script that (R1) invokes a gate/guard/
assertion but omits `set -o pipefail`; or (R2) pipes a gate-like command through `tail`/`head`
without capturing the exit code; or (R3) wraps a gate-like command in `|| true` / `|| :`.
- **Scope = LIVE scripts only**: repo-root `*.sh` + `.claude/hooks/*.sh` + any `*.sh` outside
  `session_*/ backups/ vendor/`. Closed session dirs are EXCLUDED **by the directive's explicit
  rule** — and the measurement proves it is necessary, not lazy: 15 session-dir scripts carry
  the historical pattern (they are the record; out of fence). Live tree carries exactly **1**.

## A3 — every file flagged TODAY, with a verdict (required before writing the checks)
**H1 (lookalike):** ZERO files flagged at `ov_can ≥ 0.50`. (Top non-canonical `ov_can` = 0.136.)
→ H1 allowlist is EMPTY.

**H2 (masking), live scope:** exactly ONE file flagged:
| file:line | pattern | verdict |
|---|---|---|
| `verify_restore.sh:49` | R2 — `bash run_panel.sh 2>&1 \| grep -v Warning \| tail -4` drops the panel's exit code | **FIX** (genuinely wrong: a masked gate). Capture `run_panel.sh`'s status and fail restore-verify on non-zero. |

→ After the fix, H2 allowlist is EMPTY. No bulk-allowlisting; the single real finding is fixed.

(15 closed-session-dir scripts also carry the pattern — OUT of scope by rule; they are the
historical record and are never scanned.)

## Deliverables
1. `data/harness_manifest.json` — the ONE owner-visible file: `canonical_runners` (the canonical
   set), `lookalike_allowlist` (empty), `masking_allowlist` (empty), scan scope + thresholds,
   each list carrying a `reason` convention.
2. `ship_gates_check.py` — SECTION H: gate **H1** (lookalike tripwire) + gate **H2** (masking
   lint), added to `order`; a fast `SGC_HARNESS_ONLY=1` path that runs H1/H2 and exits BEFORE
   the engine loads (so proofs test propagation cheaply). Config assertion untouched (already
   correct). No existing gate's construction changed.
3. `verify_restore.sh` — unmask line 49.
4. `SHIP_GATES.md` — SECTION H: the canonical-harness contract + H1/H2 spec + threshold + the
   allowlist mechanism.
5. Proofs A1-A5 in `session_2026-07-14/harness_guard/` with `rc_<step>` files.

## Acceptance
- A1 lookalike bites: copy `ship_gates_check.py` → new path, `SGC_HARNESS_ONLY=1` HALTs naming
  it; delete → green. A2 masking bites: add a `| tail` gate script → HALTs naming it; remove →
  green. A3 zero false positives (above). A4 config stamp: feed a config-mismatched matrix via
  `SGC_B1_MATRIX` → HALT naming the config mismatch; matching config → no config halt. A5 full
  normal run: reds exactly {A2,A3,A12}, B1 1.2601/1.2407/1.1521, panel 10/10, Guard 5 green,
  store 340a7a32 / board 3dc19fbb byte-identical.
