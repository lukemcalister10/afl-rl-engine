# SUITE HYGIENE — close the silent-failure CLASS

## Context
On 2026-07-13 a binding gate crashed, printed nothing behind a `| tail -8` pipe, and the suite
still reported **PASS** (register item 38). Job A fixed that one gate. The measurement build (PR #71,
report-only) then found the disease is a **class**: harness runners that can swallow a step's failure —
no runner sets `pipefail`, and `build_final_board.sh` **masks a failing export** (`… || true`) and then
**re-pins the board**, i.e. a bake script that can pin a board it never successfully built. CORE v2.5
rule 1: **SILENCE IS A RED.** This job makes the harness obey it — I change how failures **propagate**,
never what any gate **computes**.

## Base verification (done)
- `main` = `2bc5151` = **the merge of PR #70** (Job A2). ✅ PR #70 IS merged — safe to proceed.
- My branch `claude/suite-hygiene-silent-failures-f9wgwb` is on that merge; tree clean.
- `bootstrap.sh` ran at session start; Guard 5 PASS (store `340a7a32`, board `3dc19fbb`). ✅

## Scope reconciliation (READ — two points the owner should see)
1. **D3's enumeration is NOT in `main`.** PR #71 was report-only (prescreened, unmerged), so
   `session_2026-07-13/measurement/out/` does not exist here. I could not read the literal "48 sites /
   15 files" list. I reconstructed the triage by a **direct sweep** of every runner (grep for `| tail`,
   `| head`, `| grep … || true`, `2>/dev/null`, `|| true`, `2>&1 |`, and missing `set` flags).
2. **The fence walls off history.** The fence says "a runner inside a CLOSED session dir is history, not
   harness." My sweep finds **~59 swallow-sites, and the large majority live in CLOSED session-dir
   runners** (session_2026-07-08/-09/-10/-11 and the closed 2026-07-13 sub-chapters — v2.9 bake,
   store-identity job (item 20, merged/closed), refit_cert, continuation). Those are **OUT — history,
   not touched.** The directive **explicitly overrides the fence for exactly one session-dir file**:
   `build_final_board.sh` (named in IN, and the reason the job exists — the reusable bake script). I
   treat that one file as IN and every other session-dir runner as history.

   ⇒ **In-fence live harness = 6 files.** Two already comply. Real edits land in **4 files** below.

## TRIAGE TABLE (the census; DANGEROUS = could report green while dead, HARMLESS = decorative)

### IN-FENCE — LIVE HARNESS (edited)
| file:line | invokes | today if it raises | class |
|---|---|---|---|
| `run_panel.sh` (no `set` flags) | whole script | pipe/exit not enforced | **DANGEROUS** (file-level) |
| `run_panel.sh:13` `python3 2>/dev/null - <<PY` (panel gate) | panel 10/10 | stderr hidden; python has **no `sys.exit`**, so a crash OR a computed FAIL both exit **0** | **DANGEROUS** |
| `run_panel.sh:8` boot_guard `… \|\| exit 1` | Guard 5 | already halts | HARMLESS (guarded) |
| `bootstrap.sh` (`set -e` only) | seed+Guard5 | no `-u`/`pipefail` | **DANGEROUS** (file-level) |
| `bootstrap.sh:38-40` `md5sum \| cut` | md5 display | missing store file → pipe still 0, wrong md5 shown | **DANGEROUS** |
| `bootstrap.sh:41` unidecode `2>/dev/null \|\| echo FAIL` | vendor probe | guarded; engine fails loud later | HARMLESS |
| `bootstrap.sh:45-49` Guard5 `… \|\| {echo;exit 1}` | Guard 5 | already halts | HARMLESS (guarded) |
| `verify_restore.sh` (`set -uo pipefail`, no authoritative exit) | restore-verify | prints `RESTORE-VERIFY FAIL` but **always `exit 0`** | **DANGEROUS** |
| `verify_restore.sh:49` `bash run_panel.sh 2>&1 \| grep \| tail -4` | panel echo | truncating pipe (decorative here) | DANGEROUS (decorative) |
| `verify_restore.sh:20` `python3 2>/dev/null <<PY`, `:43` guarded md5 | ev probe / pair-guard | value surfaces via `chk` FAIL | HARMLESS (mitigated) |
| `build_final_board.sh` (`set -e` only) | bake | no `-u`/`pipefail` | **DANGEROUS** (file-level) |
| **`build_final_board.sh:18`** `python3 rl_export.py 2>&1 \| grep … \|\| true` then **re-pin** | the export | **broken export → board copied, `expected_boot.json` re-pinned, UI re-extracted** | **DANGEROUS — worst of the class (A1)** |
| `build_final_board.sh:11` `bash bootstrap.sh … && echo` | bootstrap | `&&`-left under `set -e` is not reliably fatal | **DANGEROUS** |

### IN-FENCE — ALREADY COMPLIANT (no edit)
`setup_env.sh` (`set -euo pipefail`) · `.claude/hooks/session-start.sh` (`set -euo pipefail`).

### IN-FENCE — PYTHON INVOKER (no edit, and off-limits)
`ship_gates_check.py` — the only Python wrapper that invokes sub-checks. It already checks every
`subprocess.run().returncode`/`__meta__`, turns absences into named HALTs, and `sys.exit(1)` on any
red. **Its exit semantics are owned by Job A2 (PR #70)** — the directive's own warning says not to
double-edit it. Left untouched. (`config_manifest.py`, `ruling_config_check.py`, `boot_guard.py`,
`doc_lint.py` invoke no subprocess — they are checks, not invokers.)

### OUT — HISTORY (closed session-dir runners; ~45 swallow-sites; NOT touched)
`session_2026-07-08/l1c_rectification/*.sh` · `session_2026-07-09/injury_build/{run_proofs,reverify_gates}.sh`
· `session_2026-07-10/{bake_v2_7/run_final_suite,ri_flip/run_proofs_ri}.sh`
· `session_2026-07-11/pick_corrections/*.sh` · `session_2026-07-13/{v2_9_bake/run_final_suite,
store_identity_job/scripts/run_suite,v2_9_refit_cert/scripts/*,v2_9_continuation/scripts/*}.sh`.
These are the record of what happened. Per the fence I do **not** rewrite them.

## THE FIXES

**1. `build_final_board.sh` (A1 — the one that matters most)**
- Header `set -e` → `set -euo pipefail`.
- Line 11: split `bash bootstrap.sh … && echo` into two statements so a bootstrap failure is fatal.
- Line 18: **unmask.** Capture the export's status first, print the summary grep from the log, then
  **HALT before any publish/re-pin** on non-zero:
  ```
  LOG=/tmp/rl_export.log
  if python3 rl_export.py > "$LOG" 2>&1; then rc=0; else rc=$?; fi
  grep -E "EXPORT ATTRIBUTION|PARITY GATE|exported active|NUMÉRAIRE" "$LOG" || true
  if [ "$rc" -ne 0 ]; then
    echo "FATAL: rl_export.py failed (rc=$rc) — NOT publishing, NOT re-pinning."; tail -40 "$LOG"; exit "$rc"
  fi
  ```
  Steps 3–4 (cp board, re-pin `expected_boot.json`, re-extract UI) are unchanged and now unreachable
  on a broken export. The engine/store/board/export **construction is untouched.**

**2. `run_panel.sh`** — add `set -euo pipefail`; drop `2>/dev/null` on line 13 so a traceback is
visible; add `sys.exit(0 if ok else 1)` as the last line of the heredoc so the **exit code is the
authority** (not the printed string). Panel math unchanged. Normal run = `PASS 10/10`, exit 0 —
byte-identical output.

**3. `bootstrap.sh`** — `set -e` → `set -euo pipefail` (additive; all vars are assigned, all pipes
succeed on a good tree, so a normal boot is unchanged; a missing seed file now HALTs instead of
printing a wrong md5).

**4. `verify_restore.sh`** — keep `set -uo pipefail`; add an **authoritative exit** as the final line:
`exit $(( fail > 0 ? 1 : 0 ))`. **Deliberately NOT adding bare `set -e`**: this script is designed to
run *all* `chk`s and print a tallied verdict; `set -e` would abort on the first failure and hide the
report. The propagation goal — "the non-zero exit is the authority" — is met exactly by the exit code
without changing the run-all-checks behavior. (Flagged for owner visibility.)

**5. `SHIP_GATES.md`** — extend the existing STANDING INVOCATION RULE with a short harness clause:
*every live runner sets `set -o pipefail` (+ `-e`/`-u`); no runner may mask a check (`… || true`
around a gate/export is forbidden); a bake script must never publish or pin a board it did not
successfully build.* Additive doc text only.

## ACCEPTANCE (proofs committed to `session_2026-07-13/suite_hygiene/`)
- **A1 — bake halts on broken export.** Copy `rl_export.py` to a scratch dir, inject a top-level
  `raise SystemExit("INDUCED")`, point a scratch copy of `build_final_board.sh` at it, run, and assert:
  non-zero exit, board file mtime/md5 unchanged, `expected_boot.json` `board` still `3dc19fbb`, no UI
  re-extract. Real `rl_export.py` never touched. Commit script + log.
- **A2 — three worst in-fence sites now exit non-zero.** (D3's literal three weren't available; these
  are the three worst live-harness propagation sites.) For each, induce a failure on a scratch copy and
  show exit ≠ 0 where it was 0 before: (i) `run_panel.sh` panel python raises; (ii) `bootstrap.sh`
  md5sum on a missing file under pipefail; (iii) `verify_restore.sh` with a forced `chk` fail. Commit
  before/after exit codes + logs.
- **A3 — nothing green turned red.** Full `ship_gates_check.py` run: reds exactly **{A2, A3, A12}**,
  B1 PASS on the July-8 construction (**1.2601 / 1.2407 / 1.1521**), `run_panel.sh` 10/10, all five SSI
  guards green. Print it.
- **A4 — nothing else moved.** `git diff` touches only the 5 files above; store `340a7a32` and board
  `3dc19fbb` byte-identical; no gate construction touched. Show it.

## Ladder / delivery
Tier-1-lite: supervisor prescreen + these proofs + owner's word; no value moves. **Candidate PR only —
do NOT merge, do NOT tag.** Commit + push to `claude/suite-hygiene-silent-failures-f9wgwb`. Write the
≤25-line RETURN to the session dir.
