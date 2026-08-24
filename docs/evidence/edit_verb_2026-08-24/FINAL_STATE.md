# THE EDIT VERB — FINAL STATE, 2026-08-24

`tools/land edit` is built, self-tested, and proven on the standing Graham act in a sandbox worktree.
The live tree is byte-identical to the tree this act started from. Nothing was pushed; the supervisor
reviews, lands the verb, and flies the real act.

## WHAT IS IN THE TREE

| file | change |
|---|---|
| `tools/landing/spec.py` | `act_kind: "store-edit"` — the `edit` block, the optional `board_after`, `expected_movers`, the template |
| `tools/landing/steps.py` | the `store_edit` step + `EDIT_SEQUENCE` (composed FROM `LEVER_SEQUENCE`), the surgical applier, the season-clock re-derivation, the mover assertions |
| `tools/landing/txn.py` | two fault injectors (`store_old_mismatch`, `second_mover`) and the self-test builder's mover mode |
| `tools/landing/carriers.py` | `EDIT_CARRIERS` = the lever set + `data/season_state.json` |
| `tools/landing/preview.py` | NEW — `--dry-run`, the owner's one-screen prediction in a scratch worktree |
| `tools/landing/cli.py` | `cmd_edit`, the third thin entry point |
| `tools/landing/selftest.py` | the edit fixture and five new cases |
| `tools/claims.py` | `store-edit` as a fourth act type |
| `docs/evidence/graham_dual_2026-08-24/ACT_SPEC_EDIT.json` | the Graham act, re-specified for the verb |

`tools/land` is UNCHANGED. It did not grow a line for the second verb and it did not grow one for the
third.

## THE SEQUENCE

    0 preflight     1 store_edit    2 build_proofs   3 pins      4 lineage    5 contract
    6 sibling       7 ui            8 state          9 gates    10 claims    11 commit

Eleven of the twelve steps are the lever lander's own functions, registered again rather than copied
(S7). `store_edit` is the twelfth, and its POSITION is the design: after the restore point, before the
build, so the board is built from the edited store and the lineage entry's source (measured at the
base commit) and destination (measured live) STRADDLE the edit.

## THE SELF-TEST

    BEFORE:  38 PASS / 0 FAIL   STEPS BROKEN 20     (SELFTEST_BEFORE.txt, measured before the first edit)
    AFTER:   43 PASS / 0 FAIL   STEPS BROKEN 22     (SELFTEST_AFTER.txt)

The five new cases, each PROVEN ABLE TO FAIL by neutering the guard it exists to catch
(`nonvacuity/NONVACUITY.json` — five mutations, five reds, every file restored byte-exact):

| case | mutation that reds it |
|---|---|
| `edit_steps_clean_through_contract` | the store write itself is skipped |
| `edit_lineage_straddles` | the lineage source is measured live instead of at the base commit |
| `edit_abort_restores_store` | the store is dropped from the edit carrier set |
| `edit_fault_store_edit` | the old-value assertion is neutered |
| `edit_fault_second_mover` | the declared-mover comparison is neutered |

## THE GRAHAM ACCEPTANCE FLIGHT (sandbox worktree, real builder)

`GRAHAM_SANDBOX_FLIGHT.log` — **exit 0, LANDING COMPLETE, 390.6s.** Every prediction of the standing
prereg met, none of them typed into the lander:

    store   daa93053bc2d4eba30d9dc6e06e4af9e -> fb640ca0baf92bbb122b1ad7e25c5a88   (1,978,074 bytes, +0)
    board   6fd0f7ded2b280d1a90962c299a152e3 -> 82fcd8bb1e552b927299b5702122e321   (asserted byte-exact)
    movers  EXACTLY ONE — will-graham  1533 -> 1271  (-262)   of 1,002 valued rows
    pool    700,119 -> 699,857  (-262)
    lineage source.store daa93053 (PRE-edit) -> destination.store fb640ca0 (POST-edit); chain bridged by R24
    claims  13 claims, every one recomputed: GREEN
    commit  ONE, explicit paths only

| step | seconds |
|---|---|
| preflight | 0.06 |
| store_edit | 0.13 |
| build_proofs | 121.73 |
| pins | 0.02 |
| lineage | 0.18 |
| contract | 0.08 |
| sibling | 245.18 |
| ui | 1.83 |
| state | 0.14 |
| gates | 10.11 |
| claims | 10.73 |
| commit | 0.43 |
| **TOTAL** | **390.62** |

THREE FLIGHTS, TWO ABORTS, THREE FINDINGS. The first two attempts are filed beside this one because
what they found is the point: `GRAHAM_SANDBOX_ATTEMPT1_inbox_red.log` (aborted at `gates` —
`acceptance::inbox_manifest` is red in ANY fresh checkout) and
`GRAHAM_SANDBOX_ATTEMPT2_movers_pin_red.log` (aborted at `gates` — two per-act hand-pins in
`ui/tests/movers.test.js`). Each abort restored all 44 written carriers byte-exact and left HEAD where
it found it. The three pins are reproduced INSIDE the sandbox as their own commits; see the PREREG
addendum for what the real act needs.

## THE LIVE TREE

Every flight re-hashed all 114 live carriers before and after and found **0 moved**. `P1_BEFORE.json`
and `P1_AFTER.json` are the same measurement at the branch base and at the tip.
