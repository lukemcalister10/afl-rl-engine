# PREREG — THE EDIT VERB (`tools/land edit`), 2026-08-24

**Committed BEFORE the first edit to `tools/landing/` (process law P9).** This is a TOOLING act: it
adds a third verb to the landing library and moves no value-bearing artifact. The predictions below
are therefore mostly P1 predictions — *nothing moves* — plus the self-test coverage the directive
requires and the sandbox acceptance flight it names.

**Authority.** `docs/directives/LAND_EDIT_VERB_2026-08-24.md`, the owner's ruling verbatim
(2026-08-24): *"There will likely be lots of out of round edits. So that lander needs to be redone so
round edits are one option, but there's also a general edit option. That is user unfriendly as it
stands."* The capability gap this closes is the record of register v836: three byte-exact lander
refusals, the last of which (the lineage CHAIN check) jointly with the pins step forbids a
pre-committed store flip.

## WHAT THE ACT CHANGES

Code only, inside the one landing library (S7 — no mirrored script pairs):

- `tools/landing/spec.py` — `act_kind: "store-edit"`: the declarative `edit` block, the optional
  `board_after`, the optional `expected_movers`, and the template.
- `tools/landing/steps.py` — ONE new step, `store_edit`, and `EDIT_SEQUENCE` = the lever sequence
  with that step inserted after `preflight` and before `build_proofs`. Every other step in the
  sequence is the lever lander's OWN function, registered again rather than copied.
- `tools/landing/txn.py` — the fault injectors the two new self-test cases need, and the self-test
  builder's synthetic-mover mode.
- `tools/landing/carriers.py` — `EDIT_CARRIERS` (the lever set, NAMED not re-enumerated: the store is
  already a lever carrier, captured so an abort can prove it byte-exact).
- `tools/landing/preview.py` — NEW: `--dry-run`, the owner-facing prediction, run in a scratch git
  worktree so it writes nothing to any carrier.
- `tools/landing/cli.py` — `cmd_edit`, the third thin entry point.
- `tools/landing/selftest.py` — the new cases.
- `tools/land` — UNCHANGED (it adds nothing but the name; the second verb did not grow it a line and
  neither does the third).

Nothing under `docs/register/` is touched. No push, no PR.

## PREDICTION 1 (P1) — ADDING THE VERB MOVES NOTHING

Every carrier of the ROUND carrier set (a superset of the lever set) and the live board are
BYTE-IDENTICAL between the branch base and the branch tip. The 114 carrier identities measured
before the first code edit are filed beside this prereg at `P1_BEFORE.json`; the same measurement is
re-taken at the tip into `P1_AFTER.json` and the two must compare EQUAL, key for key.

The spot identities, stated here so the falsifier is readable without a diff:

| carrier | md5 at the base, and predicted at the tip |
|---|---|
| `data/rl_build/rl_app_data.json` (the board) | `6fd0f7ded2b280d1a90962c299a152e3` |
| `engine/rl_after/rl_app_data.json` | `6fd0f7ded2b280d1a90962c299a152e3` |
| `engine/rl_after/rl_model_data.json` (the store) | `daa93053bc2d4eba30d9dc6e06e4af9e` |
| `data/expected_boot.json` | `4cb6bd57183de42743a0de28c43b021c` |
| `data/release_contract.json` | `391b34c8a6298e713de718f0c4ccb39a` |
| `data/release_lineage.json` | `1aa3d62e5f301c6da79e5b4c03f9db51` |
| `ui/data/movers.js` | `0daba7dacdaedec308672ea94834a500` |
| `ui/data/board_view_working.js` | `6a611cf9bd70b306799c37d14fc61bf9` |
| `docs/STATE.md` | `65c99c9b41799f35dd2299544a4fe980` |

**FALSIFIER:** any carrier whose md5 differs at the tip. A tooling act that moved a value-bearing
artifact is reverted, not explained (P1's own incident).

## PREDICTION 2 — THE SELF-TEST

BASELINE, measured on this tree before the first code edit, transcript filed at `SELFTEST_BEFORE.txt`:

    STEPS BROKEN 20   CAUGHT 20   ABORTED BYTE-EXACT 20
    SELF-TEST: 38 PASS / 0 FAIL

PREDICTED after the verb lands: **44 PASS / 0 FAIL, STEPS BROKEN 22**. The 38 existing cases stay
green UNTOUCHED — the lever and round sequences, their faults, their carrier sets and their aborts are
not edited by this act — and SIX cases are added:

1. `edit_control_clean_run` — THE NON-VACUITY CONTROL, first and always: a clean store-edit landing in
   the sandbox must SUCCEED before any edit fault case is believed.
2. `edit_commit_explicit_paths` — every path the edit landing committed is inside the declared
   carrier set (P8, asserted the way the lever and round controls assert it).
3. `edit_lineage_straddles` — THE STRADDLE: the appended lineage entry's `source.store` is the
   PRE-edit store and its `destination.store` is the POST-edit store, and the same for the board. This
   is the whole reason the edit is applied in the work dir rather than in a commit ahead of the
   landing, and it is the thing register v836's third abort says cannot otherwise be had.
4. `edit_fault_store_edit` — THE OLD-VALUE MISMATCH: the store already carries the new value, so the
   asserted `old` is not there. The step must ABORT (never repair — the exact-string law, ERRATUM E2
   class), and every carrier must come back byte-exact.
5. `edit_fault_second_mover` — THE UNEXPECTED MOVER: the build produces a SECOND moved board row that
   the act did not declare, with `board_after` declared. The landing must abort AT `build_proofs` and
   the transcript must NAME the undeclared mover.
6. `edit_abort_restores_store` — THE MID-STEP FAILURE: a landing that has already applied the edit and
   written pins + column + lineage + contract fails at `sibling`; every carrier — the STORE first
   among them — is restored byte-exact by the parent's own re-hash, and HEAD is back at the base
   commit (the commit-rewind leg, asserted even though this verb makes no mid-flight commit).

**FALSIFIERS:** any existing case going red; any new case that cannot be made to fail (each fault
case is paired with the control run above, which is the standing non-vacuity discipline of this
self-test); a fault case whose abort is not byte-exact.

## PREDICTION 3 — THE GRAHAM ACCEPTANCE FLIGHT, IN THE SELF-TEST SANDBOX

The standing Graham prediction (register v836, `docs/evidence/graham_dual_2026-08-24/PREREG.md`) is
unchanged and is the acceptance case for the verb. Flown through `tools/land edit` in a SANDBOX
WORKTREE — never the live tree; the supervisor flies the real act — it must produce:

- store `daa93053bc2d4eba30d9dc6e06e4af9e` → `fb640ca0baf92bbb122b1ad7e25c5a88`, by surgical byte
  replacement of `"p_dual_stream": 90` → `40` INSIDE the `will-graham` row's span, no other byte of
  the store moving;
- board `6fd0f7ded2b280d1a90962c299a152e3` → `82fcd8bb1e552b927299b5702122e321`, asserted byte-exact
  at `build_proofs` against the standing prereg;
- EXACTLY ONE mover: `will-graham` 1533 → 1271 (−262); pool (sum of `active.v`) 700,119 → 699,857;
- the lineage entry straddling the edit: `source.store` = `daa93053…`, `destination.store` =
  `fb640ca0…`, `source.board` = `6fd0f7de…`, `destination.board` = `82fcd8bb…`;
- and the live tree byte-unmoved across the whole flight (the sandbox is a git worktree; the parent
  re-hashes every live carrier before and after).

**FALSIFIERS:** a second mover; a different Graham value; any store byte outside the `will-graham`
row moving (the md5 is the check); the flight needing any pre-committed flip or pin companion.

## WHAT THIS ACT DOES NOT DO

- It does not fly the real Graham act. The supervisor reviews, lands the verb, and flies it.
- It does not touch `docs/register/`, push, or open a PR.
- It does not change one line of the lever or round sequences' behaviour. Where a shared step must
  know the third act kind (the claims file's unmoved-carrier set, the commit message's verb name),
  it is PARAMETERISED on `act_kind` exactly as `build_proofs`, `pins` and `lineage` already are —
  never forked, and the existing two branches keep their existing text.
