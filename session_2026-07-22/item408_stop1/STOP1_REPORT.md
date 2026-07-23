# ITEM 408 — R19 STOP-1 candidate report (OWNER VIEW)

**STOP-1 OWNER VIEW — CANDIDATE ONLY; NO PIN MOVED; BOARD OF RECORD 6f07f7cb NOT REPLACED**

Mechanical builder: build-seat-claude-code. This is a candidate for the owner's STOP-1 view only.
**Board of record `6f07f7cb` is NOT replaced by this build and is not replaced at STOP-1.** The STOP-1
decision is whether to approve advancing the balanced/strict board pin from `06d8af60` to the candidate
`1373e824` and, after the owner's word, moving all dependent balanced-board / FV / reference identities
atomically. No production artifact is written by this build (fences below are measured, not asserted).

## Input identity (exact, reproducible)

| input | identity |
|---|---|
| generated at commit | `517af20bc019a088ed29d6550bed45eb7e2a6156` |
| authoritative store md5 | `f37d9716648cfe4382b8c6a24c4f064f` |
| rl_model md5 (build prov) | `4f776e073ea50548ebe017cdb2f06368` |
| forward-valuation identity | `6a9a520fa2f8b4051e889d324d905cff0a37e592232cd5e68f0e0d9bdfeeec35` |
| forward-valuation module dir | `/home/user/afl-rl-engine/engine/forward_valuation` |
| distribution-pricing md5 | `dd19a2349a5b5a361b6eead0aab83ff3` |
| config-manifest identity | `45b207c03a8cf2e449d831d54c19f848ace1b7c87dd699305048dccbe05d2140` |
| expected_boot md5 | `f4603e627096ea04a9dbf2b23f0cceff` |
| release-contract md5 | `54ec77eb6c8d5a6c451604b034537130` |
| release-pick-curve md5 | `676ad2b77612a4fbd4df3362b6f88fab` |
| reference-vector 06d8af60 md5 | `6565a4ef51d67bdf6adfaaaf15fd3976` |
| board-of-record md5 | `6f07f7cbe042f8e56426a01226c967c9` |
| pinned env | {"numpy": "2.4.4", "scipy": "1.17.1", "sklearn": "1.8.0", "openpyxl": "3.1.5", "python": "3.12.3"} |
| deterministic env | {"PYTHONHASHSEED": "0", "OPENBLAS_NUM_THREADS": "1", "OMP_NUM_THREADS": "1", "MKL_NUM_THREADS": "1", "NUMEXPR_NUM_THREADS": "1", "RL_PVC2": "1", "RL_LEGE": "0", "RL_LEGF": "0", "RL_PRIOR_TREES": "400"} |

- generation command: `python3 session_2026-07-22/item408_stop1/build_stop1_candidate.py`

## Candidate identity (derived dynamically)

| field | value |
|---|---|
| candidate board md5 | `1373e82471a81064ef96820f3db065df` |
| active players | 804 |
| total value (sum_v) | 760253 |
| Harry Sheezel | 9542 |
| scratch board path | `session_2026-07-22/item408_stop1/candidate_balanced_r19.json` |

### Comparison 1 — candidate vs historical balanced board 06d8af60 (the stale pin)

| metric | value |
|---|---|
| candidate board md5 | `1373e82471a81064ef96820f3db065df` |
| comparison board md5 | `06d8af60b679a12db07c064c60c065f9` |
| candidate active count | 804 |
| comparison active count | 804 |
| total candidate value | 760253 |
| total comparison value | 752427 |
| total-value delta | +7826 |
| Harry Sheezel candidate | 9542 |
| Harry Sheezel comparison | 7964 |
| Harry Sheezel delta | +1578 |
| mover count | 723 |
| added keys (only in candidate) | 0 |
| removed keys (only in comparison) | 0 |

Added keys: (none)

Removed keys: (none)

Top 20 absolute movers:

| key | before | after | delta |
|---|---|---|---|
| noah-mraz | 412 | 2198 | +1786 |
| harry-sheezel | 7964 | 9542 | +1578 |
| phoenix-gothard | 410 | 1852 | +1442 |
| will-ashcroft | 4729 | 6020 | +1291 |
| jacob-van-rooyen | 1057 | 1978 | +921 |
| christian-petracca | 2955 | 2140 | -815 |
| ned-moyle | 1686 | 2467 | +781 |
| jai-serong | 116 | 894 | +778 |
| will-day | 3585 | 2822 | -763 |
| errol-gulden | 5857 | 5097 | -760 |
| jason-horne-francis | 4127 | 4884 | +757 |
| darcy-parish | 1460 | 707 | -753 |
| nasiah-wanganeen-milera | 6709 | 7460 | +751 |
| sam-durham | 1787 | 2529 | +742 |
| will-setterfield | 1632 | 910 | -722 |
| sam-cumming | 2119 | 2822 | +703 |
| josh-ward | 2003 | 2684 | +681 |
| hayden-young | 2732 | 2056 | -676 |
| nick-daicos | 8017 | 8683 | +666 |
| aaron-cadman | 2837 | 2175 | -662 |

### Comparison 2 — candidate vs board of record 6f07f7cb (frozen; NOT replaced)

| metric | value |
|---|---|
| candidate board md5 | `1373e82471a81064ef96820f3db065df` |
| comparison board md5 | `6f07f7cbe042f8e56426a01226c967c9` |
| candidate active count | 804 |
| comparison active count | 804 |
| total candidate value | 760253 |
| total comparison value | 760253 |
| total-value delta | +0 |
| Harry Sheezel candidate | 9542 |
| Harry Sheezel comparison | 9542 |
| Harry Sheezel delta | +0 |
| mover count | 0 |
| added keys (only in candidate) | 0 |
| removed keys (only in comparison) | 0 |

Added keys: (none)

Removed keys: (none)

Top 0 absolute movers:

| key | before | after | delta |
|---|---|---|---|

## Protected artifacts — measured before/after (build mutates nothing)

| artifact | path | before md5 | after md5 | unchanged |
|---|---|---|---|---|
| canonical_board | `data/rl_build/rl_app_data.json` | `6f07f7cbe042f8e56426a01226c967c9` | `6f07f7cbe042f8e56426a01226c967c9` | True |
| curve | `engine/rl_after/pvc_curve_v2.json` | `56dd7a7bca4306d9224aec0ef52efa32` | `56dd7a7bca4306d9224aec0ef52efa32` | True |
| curve_contract | `ui/release_pick_curve.json` | `676ad2b77612a4fbd4df3362b6f88fab` | `676ad2b77612a4fbd4df3362b6f88fab` | True |
| expected_boot | `data/expected_boot.json` | `f4603e627096ea04a9dbf2b23f0cceff` | `f4603e627096ea04a9dbf2b23f0cceff` | True |
| per_entrant | `session_2026-07-17/legd_derivation/out/per_entrant.json` | `40d7da7c7461024048fe48fcba5692ff` | `40d7da7c7461024048fe48fcba5692ff` | True |
| release_contract | `data/release_contract.json` | `54ec77eb6c8d5a6c451604b034537130` | `54ec77eb6c8d5a6c451604b034537130` | True |
| score_ledger | `engine/rl_after/ingestion/applied_rounds_ledger.json` | `1d9faae56bc4896a1bf10f9289d45461` | `1d9faae56bc4896a1bf10f9289d45461` | True |
| store | `engine/rl_after/rl_model_data.json` | `f37d9716648cfe4382b8c6a24c4f064f` | `f37d9716648cfe4382b8c6a24c4f064f` | True |

## Fences (measured from the hashes above; True == that artifact was written/armed)

| fence | written/armed |
|---|---|
| canonical_board_written | False |
| curve_contract_written | False |
| curve_written | False |
| expected_boot_written | False |
| per_entrant_written | False |
| release_contract_written | False |
| score_apply_armed | False |
| store_written | False |

## STOP-1 owner decision

PENDING — the owner is the sole authority to approve advancing the balanced/strict board pin and, after
his word, atomically moving the dependent balanced-board / FV / reference identities. This builder stops
at the candidate; no pin is moved and board of record `6f07f7cb` is not replaced.
