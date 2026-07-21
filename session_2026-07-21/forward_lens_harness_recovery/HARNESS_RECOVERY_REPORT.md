# Leg E/F Harness Recovery — Slim Evidence

## Verdict

**FAIL.** The specifically requested Leg E/F harnesses were invocation/path failures in the prior diagnostic: Board B reproduced the expected MD5 and all five corrected harness/gate commands exited 0. However, the broader remaining-gate inventory did **not** locate every required original gate as an unchanged rerunnable pass/fail harness, so owner review is **not** cleared.

## Provenance

- Starting checkout: `f05ebe6df49b653b053f0ebdd82ddc56ee8d4187`.
- GitHub draft PR #127 live head verified by GitHub API as `f05ebe6df49b653b053f0ebdd82ddc56ee8d4187` before acting.
- `bootstrap.sh` passed Guard 5: store `968de0c7`, rl_model `cc626d7d`, FV `de4c7ec3`.
- Fail-closed FV provenance check passed with `python3 -c 'import boot_guard; boot_guard.assert_fv_provenance()'`.

## Disposable Board B

- Command: `python3 rl_export.py`
- CWD: disposable copy `/tmp/legEF_boardB_gjpeyfa3/rl_after`
- Environment: `RL_PVC2=1 RL_LEGE=1 RL_LEGF=1`, `RL_CONFIG_MODE` unset, deterministic single-thread env.
- Temporary path: `/tmp/legEF_boardB_gjpeyfa3/rl_after/rl_app_data.json`
- MD5: `1f10220c341679903b79a319f554672c`
- Row count: `804`
- Present-value total: `752427.0`

## Corrected Harness Results

| Gate / harness | Command | CWD | Exit | Classification |
|---|---|---:|---:|---|
| F3 k0 dormancy | `python3 $ROOT/session_2026-07-18/legf3/tests/test_k0_dormancy.py` | `$ROOT/engine/rl_after` | 0 | RERUN PASS |
| F4 k0 dormancy | `python3 $ROOT/session_2026-07-18/legf4/tests/test_k0_dormancy_f4.py` | `$ROOT/engine/rl_after` | 0 | RERUN PASS |
| F5 k0 dormancy | `python3 $ROOT/session_2026-07-18/legf5/tests/test_k0_dormancy_f5.py $BOARD_B_TEMP_PATH` | `$ROOT/engine/rl_after` | 0 | RERUN PASS |
| F4 historical roster gate | `python3 $ROOT/session_2026-07-18/legf4/scripts/gate_f4.py $BOARD_B_TEMP_PATH` | `$ROOT/engine/rl_after` | 0 | RERUN PASS |
| F5 conservation gate | `python3 $ROOT/session_2026-07-18/legf5/scripts/gate_f5.py $BOARD_B_TEMP_PATH $ROOT/session_2026-07-18/legf5/sealed_entrant_structure.json` | `$ROOT/engine/rl_after` | 0 | RERUN PASS |

## Remaining Gate Inventory

| Required evidence area | Classification | Basis |
|---|---|---|
| historical -1 → now | RERUN PASS | `gate_f4.py` and `gate_f5.py` reran unchanged against Board B. |
| historical -2 → -1 | RERUN PASS | `gate_f4.py` and `gate_f5.py` reran unchanged against Board B. |
| ±5% league-total gate | RERUN PASS | `gate_f5.py` reran unchanged and passed. |
| developing ≥ mid-career ≥ veteran gradient | RERUN PASS | `legf3/scripts/backtest.py` reran unchanged; developing `-3.8%` ≥ mid `-9.5%` ≥ veteran `-18.3%`. |
| age and evidence continuity | COMMITTED RESULT ONLY — NOT RERUNNABLE | Located as narrative/probe evidence in Leg F3 checkpoint/exit materials; no dedicated original unchanged pass/fail gate located. |
| horizon cliffs | COMMITTED RESULT ONLY — NOT RERUNNABLE | Located as narrative/probe evidence in Leg F3/F4 materials; no dedicated original unchanged pass/fail gate located. |
| pedigree fading | COMMITTED RESULT ONLY — NOT RERUNNABLE | Located as probe/narrative evidence in Leg F3 scripts and reports; no dedicated original unchanged pass/fail gate located. |
| LTI/availability | COMMITTED RESULT ONLY — NOT RERUNNABLE | Located in Leg F4 diagnostics; no dedicated original unchanged pass/fail gate located. |
| retirement and exit behavior | COMMITTED RESULT ONLY — NOT RERUNNABLE | Located in F3/F4/F5 reports and exit-inclusive gate behavior; no standalone unchanged retirement gate located. |
| RL_LEGF=0 kill switch | RERUN PASS | F3/F4/F5 k0 dormancy harnesses reran unchanged and passed. |

## Interpretation

The concrete Leg E/F command recovery shows the prior reported failures were not model-gate failures for the five required invocations; they were invocation/path/environment failures. The final verdict remains FAIL only because the directive requires OWNER REVIEW REQUIRED **only if every required original gate is located, rerun unchanged and passes**, and several inventory categories were located only as committed narrative/probe evidence rather than unchanged runnable gates.
