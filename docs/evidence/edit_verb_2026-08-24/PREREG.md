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

## ADDENDUM — THE PREREG CORRECTED AGAINST THE TREE (P9), 2026-08-24

Process law P9 says an act "corrects the prereg against the tree rather than the tree against the
prereg", and names the error rather than quietly satisfying it. Two of the three predictions above
were WRONG, and both were wrong in the same way: they assumed a clean end-to-end edit landing could
be flown inside the self-test's sandbox. It cannot, and the reason is a property of the tree.

**ERROR 1 — `edit_control_clean_run` and `edit_commit_explicit_paths` are not reachable in the
sandbox, and were replaced.** The `sibling` step's repin REBUILDS the balanced board FROM THE REAL
STORE and refuses to stage a forward view that is not the board the manifest pins ("CONFORMANCE GATE
FAILED … this is a STOP", owner ruling v471 §4). The self-test builder produces a synthetic board, so
no landing that MOVES the board can pass that step with it — which is exactly why the existing
`SELFTEST_SPEC_MOVED` fixture is only ever used for faults at or before `lineage`, and why the lever
control lands a NO-OP. The prereg predicted a case the harness cannot host.

The coverage was split the way the evidence is, and nothing was dropped:

- `edit_steps_clean_through_contract` (new name for the control) — the six steps that carry the edit
  run with NOTHING injected and each proves its own postcondition: the store written surgically, the
  season clock re-derived, the board built FROM the edited store, `pins` moving exactly
  `['board','store']`, the column registered, the lineage entry appended, the contract re-sealed and
  `release_contract.py check` PASSing. The run then stops at `sibling` for the one documented reason
  above.
- the CLEAN END-TO-END landing — real build, real sibling reconcile, real UI writers, the full gate
  set, the explicit-path commit — is proved by the Graham acceptance flight with the REAL builder,
  filed here as `GRAHAM_SANDBOX_FLIGHT.log`. That is a stronger proof than the predicted case, not a
  weaker one, and P8's explicit-path assertion is made there.

**ERROR 2 — the count.** 38 + 6 = 44 was predicted; the tree gives **43 PASS / 0 FAIL, STEPS BROKEN
22**, because five cases were added rather than six. The 38 existing cases are green and untouched, as
predicted.

**FOUND, NOT PREDICTED — the season clock.** `release_contract.py check` REFUSES a tree whose
`data/season_state.json` names a store that is not the live one ("exposure_pace was derived from a
STALE store"), and that refusal is correct: `exposure_pace` IS derived from the store. The first run
of the new step died at `contract` with exactly that message. So `store_edit` re-derives the clock
through `season_state.derive` — the sole deriver — and HALTS if any derived VALUE moves rather than
re-stamping a provenance md5 over values nobody re-derived. `data/season_state.json` therefore joins
the edit carrier set (taken from `ROUND_EXTRA_CARRIERS`, not enumerated twice). The estate's other
out-of-round store writer moves the same field for the same reason (the #283 ownership store-apply's
`restamp_season_state`, its target 4).

**ALSO NOT PREDICTED — `tools/claims.py`.** The checker's `ACT_TYPES` table did not know `store-edit`,
so the `claims` step's own verification would have refused the file it had just emitted. The table
gains a fourth act type, requiring the landing kinds AND an `unmoved` claim.

**FOUND, NOT PREDICTED — TWO HAND-PINS STAND BETWEEN ANY LANDING AND A GREEN `gates` STEP TODAY, and
neither belongs to this verb.** The acceptance flight found them one at a time, each as an abort with
a byte-exact restore, which is the lander behaving correctly:

1. `acceptance::inbox_manifest` is RED IN ANY FRESH CHECKOUT, including this live worktree right now
   (`python3 tools/inbox_manifest.py check` → exit 1, two STALE files). The check compares a COMMITTED
   generated file against a render whose `arrived` column is the archived file's FILESYSTEM MTIME, so
   a fresh clone re-dates every row: on disk `2026-08-20`, regenerated `2026-08-24`. That is the P4
   class ("assert the relationship, never this month's number") living inside an acceptance check. It
   reds the gates step of ANY landing flown today, this act's and the supervisor's alike.
2. `ui/tests/movers.test.js` carries TWO PER-ACT HAND-PINS that any out-of-round board move moves, and
   both are hand-pins by standing design rather than defects — the file's own header says "the advance
   transaction does not own this file, so the advance seat moves it and discloses it":
   - the NUMBER of declared out-of-round boundaries, BY LITERAL (`mc.length === 11`). Any act that
     registers a column writes one more. The last bump has its own commit (`65800f0` — "THE WEEKLY
     TEST PIN: OUT-OF-ROUND BOUNDARY COUNT 10 -> 11 … the tenth such bump, documented in place like
     the nine before it").
   - the LINEAGE-STATE expectation, which swings between `[true,"ok"]` and `[true,"bridged"]` with
     what kind of act moved the board LAST. `ok` is the direct-lineage branch and requires the latest
     ROUND report's terminal board to be the loaded board; an out-of-round act makes `bridged` the
     honest reading, and the next round advance swings it back. The file documents both swings in
     eleven lines of its own history ("RESTATED 2026-08-10 (#334 DOB courier landing) … the expected
     state is `bridged` again, and that is the honest reading, not a weakening").

   **The real Graham act needs BOTH as a companion commit before it flies** — 11 → 12, and `ok` →
   `bridged` — exactly as the #334 DOB courier landing needed them. The lander does not write them and
   should not: both assertions carry owner-facing prose naming what happened, and composing that is
   authorship, not landing.

All three were reproduced INSIDE THE DISPOSABLE SANDBOX (regenerate the manifest; bump the count; swing
the lineage state), as their own commits there, so the acceptance flight measures the verb rather than
pins nobody has moved yet. THE LIVE TREE WAS NOT TOUCHED — every flight re-hashed all 114 live carriers
afterwards and found 0 moved. Each was found the same way: the lander flew, the gate red, and the abort
put every carrier back byte-exact. Three aborts, three findings, one instrument.

**NON-VACUITY, MEASURED RATHER THAN ASSERTED.** Each of the five new cases was proved able to fail by
neutering the guard it exists to catch, one at a time, in the working copy the self-test copies into
its sandbox — and each target case RED under its own mutation, with every mutated file restored
byte-exact afterwards. `NONVACUITY.json` carries the five runs and their transcripts.

## WHAT THIS ACT DOES NOT DO

- It does not fly the real Graham act. The supervisor reviews, lands the verb, and flies it.
- It does not touch `docs/register/`, push, or open a PR.
- It does not change one line of the lever or round sequences' behaviour. Where a shared step must
  know the third act kind (the claims file's unmoved-carrier set, the commit message's verb name),
  it is PARAMETERISED on `act_kind` exactly as `build_proofs`, `pins` and `lineage` already are —
  never forked, and the existing two branches keep their existing text.
