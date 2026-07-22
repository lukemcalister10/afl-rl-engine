# COLD-AUDIT SEED · candidate head `15a9abd` · seat 13 · 2026-07-18
### Five INDEPENDENT shard prompts. The owner pastes EACH block into a SEPARATE fresh incognito
### chat OUTSIDE the Project, verbatim, one shard per chat. Each shard: compute and report ONLY —
### no pass/fail against unstated expectations; verdicts are reconciled by the supervisor after.
### Leak-guard applied: this seed carries ADDRESSES and INPUT PINS only, never computed results.

## COMMON HEADER (include at the top of every shard paste)
You are an independent auditor. Repo: https://github.com/lukemcalister10/afl-rl-engine (public).
Pin: branch `claude/legf5-entrant-layer-conservation-p4susl`, head SHA
`15a9abd996f8f7426e98f173d83a0d600b966a3c` — `git ls-remote` must show it; HALT on mismatch.
`git clone --depth 30 -b <branch>` then `git checkout <SHA>`. Input pins (assert before anything):
`engine/rl_after/rl_model_data.json` md5 `968de0c7…` · `engine/rl_after/pvc_curve_v2.json`
payload stamp `89c14729` (per its own KAT note). Set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1` for every run. Report format: ≤30 lines — what you
computed · the values · exit codes · an ANNEX (numpy + OpenBLAS versions, `lscpu` model line,
thread settings) · anything that would not run (a non-run is a finding, not a skip). Do not
consult any prior conversation; you have none.

## SHARD A — ENVIRONMENT · REPRODUCTION · GUARDS
1. Run the repo's self-test and boot-guard entry scripts as committed (`boot_guard.py`,
   `one_source_selftest.py` or per `bootstrap.sh`); report each verdict line and exit code
   verbatim (including any RED — report it, do not interpret it).
2. Build the export board at defaults, single-threaded, TWICE; report both md5s and whether they
   are identical. Then build with each kill-switch env var at 0 — `RL_PVC2=0`, `RL_LEGE=0`,
   `RL_LEGF=0` (one at a time, others default) — and report each board md5.
3. If ANY two runs that should agree differ, or a second container is available and differs:
   report the count of differing rows and the NAMES of up to 10, with per-row deltas, and if
   feasible localize which code branch flips (bisect one named row).

## SHARD B — THE GATES, FROM THE FROZEN SUITE ONLY
1. Run the committed gate suite (`tools/seat/gates_score.py` and the suite `bootstrap.sh`/README
   names). Report: the pooled year-0 calibration gate value (as a %) · the strict-descent
   violation count · the curve value at pick 1 · the posture discount triple as applied · the
   three narrowest margins the suite reports.
2. Open `docs/acceptance_v1_21.json`; report, BY KEY, the entries governing the values above
   (key name + threshold), and whether your computed values sit inside each threshold — numbers
   beside numbers, no summary verdict.

## SHARD C — THE KILL-SWITCH EQUIVALENCE CHAIN
1. From `15a9abd`, compute and report board md5s for: all-defaults · `RL_PVC2=0` ·
   `RL_LEGE=0` · `RL_LEGF=0` · `RL_LEGF=0,RL_LEGE=0` · `RL_LEGF=0,RL_LEGE=0,RL_PVC2=0`.
2. Re-execute the committed per-consumer proof scripts under `session_2026-07-18/five_migration/`
   from their INPUTS (not their stored outputs); report per-consumer: shipped-value parity count
   (rows changed / total) and rank-mover count.
3. Report the store file's md5 after a full pipeline run (it must be re-read from disk, not
   assumed).

## SHARD D — THE PROJECTION CHAIN
1. Run every committed dormancy test: `session_2026-07-18/legf3/tests/`, `…/legf4/tests/`,
   `…/legf5/tests/` — report each test file's result and exit code.
2. Re-run the committed backtest/gate harnesses AS COMMITTED: `session_2026-07-18/legf4/scripts/
   gate_f4.py` and `…/legf5/scripts/gate_f5.py` (their own READMEs/headers state usage). Report
   every number they print (predictions, realized, errors) — do not be told what they should be.
3. Report the seal-file hashes you find (`…/legf3/sealed_strawman.json`, `…/legf4/sealed_rate*.json`,
   `…/legf5/sealed_entrant_structure.json`): sha256 of each, and the one-line derivation note each
   carries about what it was derived from.
4. Two diffs to review BY ADDRESS and describe in one line each — what behavior they change and
   what they cannot change: `git diff 33c8b52 15a9abd -- engine/rl_after/_merged_recover.py`
   restricted to the `_feat_infer` hunk near :255; and `git diff a90052a cc58570 --
   engine/forward_valuation/distribution_pricing.py`.

## SHARD E — THE EXTERNAL FAILURE-MODE CHECKLIST, BY ADDRESS
Work through `docs/inputs/CLEANROOM_GPT_section5_failure_modes_2026-07-18.md` §5.1–§5.9. For
each: compute the check it implies against THIS repo's committed data/code and report the number
or the code-line answer. Specifically include: §5.1 — the pick↔value relationship at career year
1 vs later years (report coefficients); §5.2 — state, from
`session_2026-07-17/legd_derivation/scripts/derive_pvc2.py`'s own target construction, whether
the pick price is an entry price or a career aggregate; §5.3 — state from the same scripts
whether a hard maturity cutoff exists; §5.9 — re-verify the four data-coding observations against
`per_entrant` at the pinned inputs. Also: report what `emit_matrix.py` says (its own comments +
code) about year-truncation in its walk-forward, by line number.
