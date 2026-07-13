# DELIVERABLE 3 — THE SILENT-FAILURE SWEEP (report-only)
**Board:** n/a (pure code audit). **Method:** ripgrep for pipe-without-pipefail, `| tail`/`| head`/`| grep`,
`|| true`, `set +e`, swallowed `subprocess` returncodes, and `except:pass` around a check; then control-flow
traced from each site to the suite's PASS/FAIL decision. Historical session logs/records excluded. **Change: none.**

## HEADLINE
- **48 distinct DANGEROUS (file:line) gate-steps across 15 files** (≈40 are the SAME bug replicated across six
  near-identical bake/proof suite runners). Exceeds the ~23 floor.
- The internally-graded Python guards (`ship_gates_check.py`, `boot_guard.py`, `ruling_config_check.py`,
  `config_manifest.py`, `one_source_selftest.py`, `guard_correction_canary.py`, `doc_lint.py`) are **robust** —
  they accumulate failures and `sys.exit(1)`; their unchecked subprocess returncodes are compensated by downstream
  output-presence / byte-compare checks (HARMLESS).
- The danger is at two layers: (1) **two gates that never turn a real FAIL/BREACH verdict into a non-zero exit**
  (`run_panel.sh` panel; `cohort_gate_official.py`), and (2) **the session suite-runners** that discard every
  gate's exit code (`set +e` / `set -e` without `pipefail`, plus `| tail`/`| grep`/`|| true`/`2>/dev/null`) and
  then write an unconditional DONE marker — a crashing or breaching gate reads green.

## WORST 3 (DANGEROUS, by name)
1. **`session_2026-07-13/store_identity_job/scripts/run_suite.sh:31` → `cohort_gate_official.py`** — the LITERAL
   2026-07-13 incident: the official G-COHORT gate is invoked `… 2>&1 | tail -8` under `set +e`, so a crash (or a
   130-breach) loses its exit code and the script proceeds to write `SUITE_DONE`. Worse, `cohort_gate_official.py`
   prints `GATE: BREACH` but **never `sys.exit(1)`**, so even a clean breach is invisible to any exit-code check.
2. **`run_panel.sh:13`** — the most EXPOSED site: the only one reachable from the always-on CI workflow
   (`.github/workflows/ci-guards.yml` `run: bash run_panel.sh`). The inline panel computes `ok`, prints
   `RESULT: FAIL` on a real 10/10 regression, but **never calls `sys.exit`** → Python exits 0 → the CI "Panel
   10/10" step is GREEN while the panel is failing; `2>/dev/null` additionally hides any traceback.
3. **`session_2026-07-13/v2_9_export_display/scripts/build_final_board.sh:18`** —
   `python3 rl_export.py 2>&1 | grep … || true` swallows rl_export's own halt-not-warn bake-guard
   (PARITY GATE / override-presence `SystemExit`), and the script then unconditionally copies the produced board to
   the committed path **and re-pins `expected_boot.json`** to whatever md5 resulted — a mis-built board can be
   published and self-certified as the new expected pin, defeating the guard designed to stop it.

## pipefail POSTURE
- **Sets pipefail (good):** `setup_env.sh` (pipes no checks), `.claude/hooks/session-start.sh`,
  `.github/workflows/ci-guards.yml` (invokes the Python guards UN-piped, so their exits propagate — its only weak
  spot is delegating the panel to `run_panel.sh`), `verify_restore.sh` (its one pipe is decorative).
- **No pipefail (exposed) — every gate-invoking script that pipes checks:** `run_panel.sh` (no `set` at all),
  `store_identity_job/…/run_suite.sh`, `v2_9_bake/run_final_suite.sh`, `bake_v2_7/run_final_suite.sh`,
  `ri_flip/run_proofs_ri.sh`, `injury_build/run_proofs.sh` + `reverify_gates.sh`,
  `v2_9_continuation/scripts/validate_and_gate.sh` + `run_levers.sh`, `v2_9_export_display/…/build_final_board.sh`.
  (`bootstrap.sh` is `set -e` only but uses explicit `|| { …; exit 1; }`, so it is actually safe.)

## FULL CANDIDATE TABLE (file · line · invokes · today-if-raises · class)
| # | file : line | invokes | if it raises/breaches today | class |
|---|---|---|---|---|
| 1 | run_panel.sh:13–27 | inline panel (ev vs 10 expected) | prints RESULT:FAIL, exits 0; CI green on a real mismatch; 2>/dev/null hides traceback | **DANGEROUS** |
| 2 | v2_9_continuation/scripts/cohort_gate_official.py:79 (also 47) | G-COHORT 130-breach | prints GATE:BREACH, never sys.exit(1) → exit 0 on breach; empty matrix raises but callers discard | **DANGEROUS** |
| 3 | store_identity_job/scripts/run_suite.sh:31 | cohort_gate_official.py … \|tail-8 under set +e | crash/breach code lost through pipe; SUITE_DONE written | **DANGEROUS** |
| 4 | store_identity_job/scripts/run_suite.sh:33 | ship_gates_check.py … \|tail-18 | ship_gates sys.exit(1) discarded by pipe under set +e | **DANGEROUS** |
| 5 | store_identity_job/scripts/run_suite.sh:11 | bootstrap.sh … \|grep | Guard-5 boot HALT lost through pipe; suite continues | **DANGEROUS** |
| 6 | store_identity_job/scripts/run_suite.sh:14,15,18,22,24,27,29 | config_manifest/ruling_config/rl_export bake-guard/selftest/canary/prove_red_paths/run_panel each \|tail/\|grep | 7 guards' non-zero exits thrown away under set +e | **DANGEROUS** |
| 7 | v2_9_bake/run_final_suite.sh:13,16,17,23,25,28,30,32 | bootstrap/config/ruling/selftest/canary/override-excl/prove_red_paths/run_panel piped, set +e | FINAL_SUITE_DONE written unconditionally | **DANGEROUS** |
| 8 | bake_v2_7/run_final_suite.sh:13,17,18,37,39,42–43,45 | bootstrap/config/ruling/selftest/canary/ship_gates(>file)+grep/panel, set +e | ship_gates exit ignored (>file then bare grep VERDICT); others \|tail | **DANGEROUS** |
| 9 | ri_flip/run_proofs_ri.sh:53,55,57,59,61,63,64,65 | s4_matrix/selftest/canary/ruling/config/ship_gates each `> file 2>&1 \|\| true`; panel \|tail | `\|\| true` swallows each guard's exit | **DANGEROUS** |
| 10 | injury_build/run_proofs.sh:41,44,49,50,53 | s4_matrix `\|\| echo`; selftest & ship_gates `\|\| true`; grep\|tail; panel\|tail (set -e) | exits swallowed despite set -e | **DANGEROUS** |
| 11 | injury_build/reverify_gates.sh:23,25 | ship_gates `>file 2>&1 \|\| true`; run_panel \|tail-1 | gate results not gating; reaches "REVERIFY DONE" | **DANGEROUS** |
| 12 | v2_9_continuation/scripts/validate_and_gate.sh:13,17 | `bash run_levers.sh \| grep` (set -e, no pipefail) | run_levers crash → grep matches partial output → pipeline 0 → set -e never fires | **DANGEROUS** |
| 13 | v2_9_continuation/scripts/run_levers.sh:50 | `s4_matrix_M1v7.py \| tail-3` (no pipefail) | matrix producer exit masked; returns success with a partial/missing matrix that feeds the cohort gate | **DANGEROUS** |
| 14 | v2_9_export_display/scripts/build_final_board.sh:18 | `rl_export.py 2>&1 \| grep … \|\| true` | masks export bake-guard; copies board to committed path + re-pins expected_boot | **DANGEROUS** |
| 15 | v2_9_refit_cert/scripts/run_combined.sh:8 | `board_pass.py 2>/dev/null; echo COMBINED_DONE rc=$?` | crash traceback hidden; rc echoed but not acted on; produces g_full.json for the cohort gate | **DANGEROUS** |
| 16 | verify/d15/book_hashcheck.py:156 | book byte-identity verdict | prints VERDICT:FAIL, main() returns None → exit 0 on FAIL (manual tool, not suite-wired) | **DANGEROUS (minor)** |
| — | ship_gates_check.py:261,347,456 | subprocess s4_matrix/_gate1_wf/rl_export, returncode not gated | crash → no __meta__/no cert/'MISSING' → gate set FAIL/ERROR (hard-fail L681) | HARMLESS |
| — | verify_restore.sh:20 | inline python 2>/dev/null (Maric/Langdon ev) | crash → empty → compares ""≠1271 → FAIL counted | HARMLESS |
| — | verify_restore.sh:49 | run_panel \|grep -v Warning\|tail-4 | decorative "confirm 10/10" echo, not in the pass/fail verdict | HARMLESS |
| — | bootstrap.sh:41 | unidecode import 2>/dev/null \|\| echo FAIL | decorative $U; real gate is boot_guard.py \|\| exit 1 | HARMLESS |
| — | config_manifest.py:75 / ruling_config_check.py:101 | except:return None around optional pin/manifest | intended-optional, or the next check() FAILs and records it | HARMLESS |
| — | ship_gates_check.py:83,88,499,627,640 | except:<benign default> (state label/snapshot/register/persistence) | decorative reporting columns; no gate reads them | HARMLESS |
| — | run_matrix.sh:4 | echo "MATRIX_DONE rc=$? bytes=$(wc -c…)" | rc recorded into text; downstream md5/bytes compare | HARMLESS |

**The single fix that closes the class:** add `set -o pipefail` and drop the `set +e` / `| tail` / `|| true`
wrappers in the suite-runners (or have them aggregate exit codes instead of a human reading VERDICT/RESULT text),
and give the two root gates (`run_panel.sh` panel, `cohort_gate_official.py`) an explicit `sys.exit(1)` on
FAIL/BREACH. **Owner rules which must halt — reported only, nothing changed.**
