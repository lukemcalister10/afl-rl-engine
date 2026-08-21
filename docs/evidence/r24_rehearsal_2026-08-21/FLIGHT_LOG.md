# R24 DRESS REHEARSAL — THE FLIGHT LOG

Six flights of `tools/land round`, 2026-08-21, in a `git worktree` sandbox cut from live HEAD
`94bca14`. Every one used the REAL invocation and the REAL builder, so every one ran the
pre-transaction self-test (30 PASS / 0 FAIL) before opening a transaction.
**SYNTHETIC THROUGHOUT. No owner word exists or is claimed. The board these produced never left the sandbox.**

| run | started (UTC) | spec | flag | exit | halted at | seconds |
|---|---|---|---|---:|---|---:|
| A | 10:32:49 | `ACT_SPEC_R24_SYNTHETIC.json` | — | 1 | `preflight` — `?? scores/R24.csv` | 0.02 |
| B | 10:35:12 | `ACT_SPEC_R24_SYNTHETIC.json` | — | 1 | `catchup_preflight` — H2: `['connor-rozee','tom-green']` | 0.09 |
| C | 10:36:56 | `ACT_SPEC_R24_SYNTHETIC_RECUT.json` | — | 1 | `catchup_preflight` — input commit: nothing to commit | 0.39 |
| D | 10:39:28 | `ACT_SPEC_R24_SYNTHETIC_FULL.json` | `--no-commit --keep-work` | 1 | `advance` — `ConfigPolicyError: RL_BUILD_LOCK_FILE` | 0.39 |
| E | 10:41:07 | `ACT_SPEC_R24_SYNTHETIC_FULL.json` | `--no-commit --keep-work` | 1 | `gates` — acceptance runner RED (2 of 17) | 281.49 |
| F | 10:49:21 | `ACT_SPEC_R24_SYNTHETIC_LEG2.json` | `--no-commit` | **0** | **COMPLETE** | 278.36 |

## PER-STEP TIMINGS — RUN F, the complete journey

| # | step | seconds | verdict |
|---:|---|---:|---|
| 0 | preflight | 0.09 | OK |
| 1 | sheet | 0.01 | OK |
| 2 | scores | 0.00 | OK |
| 3 | catchup_preflight | 0.10 | OK |
| 4 | **advance** | **275.64** | OK |
| 5 | generator_sync | 0.01 | OK |
| 6 | day0 | 0.00 | OK |
| 7 | contract | 0.07 | OK |
| 8 | sibling | 0.11 | OK |
| 9 | ui | 1.70 | OK |
| 10 | movers_page | 0.10 | OK |
| 11 | state | 0.15 | OK |
| 12 | gates | 0.13 | OK (narrowed set — see the report §3.5) |
| 13 | claims | 0.23 | OK — GREEN, 9 of 9 |
| 14 | commit | 0.02 | OK — 38 explicit paths |
| | **TOTAL** | **278.36** | |

RUN E's identical journey through step 11 totalled 281.49s, with the advance at 271.11s.
The advance is ~97% of the wall clock; everything else is under fifteen seconds.

## THE FILES

* `RUN_<X>_stdout.txt` — the full console transcript of each flight
* `RUN_<X>.log` — the lander's own structured transcript (`--log`)
* `RUN_<X>_report.json` — the machine-readable result: `ok`, `failed_step`, per-step timings, abort record, measured facts
* `08_preflight_r24.txt` / `09_armed_r24.txt` — the round tool's own captures, written by the lander
* `R24_REHEARSAL_CLAIMS.json` / `claims_check.txt` — the claims file the landing emitted and the checker's recomputation
* `gate_release_manifest_check.txt` / `gate_release_contract_check.txt` — the two gates the landing ran
* `RUNE_gate_acceptance_runner.txt` (+ `_evidence/`) — RUN E's RED acceptance run and the two failing checks' raw output
* `LANDED_gate3_acceptance.txt` / `LANDED_gate4_movers_py.txt` / `LANDED_gate5_movers_js.txt` — the three remaining gates, measured BY HAND on the landed R24 tree
* `LANDED_gate4_unmasked.txt` — the py suite re-run past its first halt (sandbox-only edit, reverted byte-exact) so the second red is visible instead of masked
* `LANDED_movers_direction.txt` — the twenty declared movers, measured against `movers_R24.json`
* `PRETXN_SELFTEST_SUMMARY.json` — the pre-transaction self-test's own result
* `../aborts/ABORT_*.json` — one record per halt
