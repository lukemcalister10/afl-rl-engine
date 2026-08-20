# FINAL STATE — PACKAGE 2a, THE LEVER LANDER

**Authority:** `docs/proposals/process_plan/PLAN_v6.md`, items 2a.1–2a.4 · **Date:** 2026-08-20
**Base at brief:** `main` @ `9787a3b` · **Base as built:** `main` @ `246af1c` (see `g1_BASE_MOVED.md`)
**Nothing was pushed. `docs/OPEN_ITEMS_REGISTER.md` was not touched.**

---

## 1. THE COMMITS

| # | sha | deliverable |
|---|---|---|
| 1 | `3e5ea89` | **2a.1** — `land lever`: the landing transaction, one command, one shared library |
| 2 | `844e3af` | **2a.2** — the decision-packet template and its slot validator |
| 3 | `552b201` | **2a.3** — the self-test and the abort path; registered as runner check 17 |
| 4 | `ff64ef0` | **2a.1 repair** — the lander WAITS for a contended build lock, as `build_lock.sh` does |
| 5 | `d02ef2b` | **2a.1 repair** — the deadlock against its own gate (first, WRONG, fix) |
| 6 | `1aa63dd` | **2a.1/2a.3 repairs** — the lock is released before the gates; the self-test's own cleanup bug |
| 7 | `d044437` | **2a.1 repair** — the twice-burned rule, third occurrence: this lander's own `RL_`-prefixed env var |
| 8 | *(this)* | the evidence tail: the self-test transcripts, the no-op rehearsal, G1 |

FOUR OF THE EIGHT ARE REPAIRS FOUND BY RUNNING THE THING, each its own commit rather than folded
into the deliverable. §6 says what they were, in the order the wrong answers were tried — which is
the useful part of the record, not an embarrassment to be tidied.

## 2. WHAT WAS BUILT

```
tools/land                          the entry point:  tools/land lever --spec <act.json>
tools/landing/__init__.py           the library's own account of what it consolidates
tools/landing/carriers.py           the ENUMERATED carrier set + Snapshot (capture/restore/prove)
tools/landing/spec.py               the act spec: fixed slots, validated before anything runs
tools/landing/steps.py              the ten steps, in the day's proven order
tools/landing/txn.py                the driver: fail-closed sequencing, timing, THE ABORT PATH
tools/landing/_build_child.py       the board build, in a child process, out of the lock's env
tools/landing/packet.py             the decision-packet slot validator (2a.2)
tools/landing/PACKET_TEMPLATE.md    the fixed-slot template (2a.2)
tools/landing/selftest.py           the sandbox self-test (2a.3)
tools/landing/cli.py                `land lever` — and where `land round` (2b) attaches
acceptance/checks/landing.py        the self-test, registered as runner check 17
acceptance/checks/__init__.py       +14 lines: the registration
```

**ONE LIBRARY, TWO ENTRY POINTS.** `land round` (2b, after 3a) is the second thin entry point over
the same library. The verb exists today and exits non-zero saying what it waits for — a verb that
pretended to work is the first thing a tired seat would reach for.

## 3. THE SEQUENCE, AND WHERE EACH STEP CAME FROM

`tools/land lever --print-sequence` prints this, with the carrier set beneath it.

| # | step | consolidates |
|---|---|---|
| 0 | `preflight` | clean-tree assertion, the build lock, **the restore point** — in that order |
| 1 | `build_proofs` | `d8_build.py` / `br_build.py` / the F5 build driver + their `0*_builds.txt` assertions |
| 2 | `pins` | `land_a_pins.py` / `land_br_pins.py` / `land_f5_pins.py` |
| 3 | `lineage` | `register_*_column.py` + `append_*_transition.py` + `measure_lineage.py` |
| 4 | `contract` | `land_c_contract.py` / `land_br_contract.py` / `land_f5_contract.py` |
| 5 | `sibling` | the `sibling_repin.py` verify→plan→reconcile→verify the three landings ran by hand |
| 6 | `ui` | `land_e_ui.py` / `land_br_ui.py` / `land_f5_ui.py` — BOTH writers, the thrice-proven trap |
| 7 | `gates` | the gate block each landing's `*_gates.txt` recorded |
| 8 | `claims` | `tools/claims.py` (P1 1c), emitted from what the transaction measured, then verified |
| 9 | `commit` | the explicit-path landing-transaction commit each act made by hand |

**What moved into data.** Every per-act constant — the predicted board, the must-not-move list, the
column id and label, the lineage citation — is now an ACT SPEC slot. `land_f5_pins.py` and
`land_br_pins.py` differ in four literals and one docstring; that is the definition of a thing that
should be data. **The prereg's prediction is an INPUT**: a lander that learned the expected board
from the build it just ran would assert nothing at all.

**What did NOT move into the library, deliberately:** the day-0 LAW (the lander prints the row diff
and installs a reference its emitter produced; computing day-0 here would be a second implementation
beside the byte-carried emitter — the hazard M1b names), the BOOK RE-SEAL (`reseal_backrows.py` is
act-specific and owner-gated, and is not part of a lever landing), and JUDGMENT of any kind.

## 4. THE SELF-TEST — 17 of 17, in 10.0 SECONDS

`docs/evidence/p2a_lander_2026-08-20/02_selftest.txt`, transcripts in `selftest/`.

```
STEPS BROKEN 10   CAUGHT 10   ABORTED BYTE-EXACT 10
SELF-TEST: 17 PASS / 0 FAIL
```

| case | what it proves |
|---|---|
| `control_clean_run` | **the non-vacuity control** — a clean no-op landing in the same sandbox SUCCEEDS |
| `commit_explicit_paths` | the control's commit re-read from git; every path a declared carrier |
| `build_lock_refuses` | a landing started while a second holder has the lock refuses to start |
| `fault_preflight` | an uncommitted file before the restore point (`dirty_tree`) |
| `fault_build_proofs` | a build reporting a board the prereg did not predict (`wrong_board`) |
| `fault_pins` | an installed board that no longer matches what was built (`board_corrupt`) |
| `fault_lineage` | a register tail no movers report can bridge (`chain_broken`) |
| `fault_contract` | a contract seal that does not verify going in (`seal_broken`) |
| `fault_sibling` | an unreadable sibling provenance sidecar (`sidecar_corrupt`) |
| `fault_ui` | **THE THRICE-PROVEN TRAP** — writer 2 never runs (`skip_second_writer`) |
| `fault_gates` | a landed pin the manifest gate reds on (`gate_red`) |
| `fault_claims` | a claims file the tree contradicts (`false_claim`) |
| `fault_commit` | a file outside the declared carrier set at commit time (`foreign_path`) |
| `abort_restores_writers` | **the depth case** — 11 carriers WRITTEN then restored byte-exact |
| `claims_negative_control` | `tools/claims.py selftest`, 11 of 11, run inside the sandbox |
| `packet_slot_validator` | the packet validator's own negative control, 5 of 5 |
| `live_tree_untouched` | every live carrier byte-unmoved across the whole self-test |

**THE PARENT NEVER TRUSTS THE CHILD'S VERDICT.** It re-hashes every carrier itself, before and after
each case. A self-test that asked the program under test whether it had succeeded would certify
nothing but the program's opinion of itself.

**The depth case is the one that matters most.** A landing on a synthetic board move that WROTE the
pins, the history column (`value_history` / `rank_history` / `pos_rank_history`), the append-only
lineage entry and the restamped contract — then failed at the sibling step. Eleven carriers written,
eleven restored **byte-exact**. The writers that only fire on a board move are exercised against real
files, not simulated.

**Honest scope of the fault cases:** their landings use `SelftestBuilder`, which runs no engine at
all — the fault cases prove the TRANSACTION (detection, abort, byte-exact restore) in seconds. The
clean end-to-end run in §5 proves the transaction ON A REAL BUILD. Which is which is stated here
rather than blurred.

**REGISTERED AS RUNNER CHECK 17**, on the brief's own test: fast (10.0s measured) and no builds.
`PROFILE='full'`, so the per-push host-insensitive lane never pays for a git worktree; `BLOCKED`
rather than `FAIL` where no worktree can be created, because that is a host fact wearing the
lander's name. An unexercised fallback is fake safety; an unexercised self-test is fake proof.

## 5. THE ACCEPTANCE — A REAL NO-OP LEVER LANDING, END TO END, ON A SCRATCH COPY

`05_noop_rehearsal_COMPLETE.txt` (transcript) · `08_noop_ACT_SPEC.json` (the spec it was given) ·
`06_noop_CLAIMS.json` + `07_noop_claims_check.txt` (what it emitted and how it verified).

A `git worktree` of the live tree, a DECLARED no-op act spec — it predicts the board the tree already
has and moves no identity — the REAL builder, and the FULL default gate set. Every step ran.

```
--- STEP TIMING, MACHINE-RECORDED (the M2 measure-then-quote ruling) ---
    preflight          0.06s  OK        clean tree, lock, 51 carriers captured
    build_proofs     109.27s  OK        THE BOARD REPRODUCED: 68be10c7…757 == the prereg prediction
    pins               0.02s  OK        no pin moves (declared no-op); coherence proved anyway
    lineage            0.00s  OK        no column owed, no entry owed (board unmoved out of round)
    contract           0.09s  OK        restamped; seal cde9f70a -> cde9f70a; check PASS
    sibling            0.14s  OK        verify ok, 0 fails — CURRENT, nothing to reconcile, no build
    ui                 0.30s  OK        both writers; embedded identity read back == 68be10c7
    gates            226.00s  OK        5 of 5 PASS (runner 17/17 GREEN inside it)
    claims           227.41s  OK        GREEN — every claim recomputed and held
    commit             0.21s  OK        explicit paths; ONE path, the evidence dir
    TOTAL            563.50s
LANDING COMPLETE — every step's postcondition held.
SOAK: hand-verification stands until the owner's word per act type (G3.iv).
```

**THE BOARD IDENTITY IS REPRODUCED END TO END.** `68be10c79d0ee096455754e084bcf757`, built from
source by the accepted disposable FV builder in 109.3s, asserted equal to the prediction the spec
carried in *before* the build ran, and asserted byte-identical to the board on disk.

**AND THE NO-OP IS BYTE-EXACT.** Measured independently after the run — the diff between the
sandbox's base commit and the rehearsal's own commit is EIGHT FILES, all of them the act's own
evidence, and **not one carrier**:

```
CARRIERS MOVED: NONE — the no-op is byte-exact
working tree after the landing: clean
```

That is the trailing-newline repair (§6.4) paying for itself: before it, a landing that moved nothing
still moved `data/release_contract.json` by one byte.

**THE MEASURED LANDING COST, QUOTED ONLY BECAUSE IT WAS MEASURED (M2):** ~9.4 minutes for a
no-op — 1.8 min of build, 3.8 min of gates, 3.8 min of claims, and under a second for everything the
landing actually *writes*. **The gates are paid for TWICE** and that is not an accident: `claims`
re-runs every gate through `tools/claims.py`, which recomputes claims and never reads a verdict back.
An act that moves a board adds its own build legs and a sibling reconcile (~2 more minutes) on top.
No turnaround target is promised here; this is the number a target would have to start from.

**Two earlier attempts of this same rehearsal ABORTED at the gate step**, and both aborts were
byte-exact with 0 carriers moved. `04_noop_rehearsal_ABORTED_at_gates.txt` is kept as evidence:
the lander refusing to land through a red is the behaviour, and both reds were real (§6.3, §6.5).

## 6. DEVIATIONS, REPAIRS AND THINGS RECORDED — NONE ABSORBED

1. **THE BASE MOVED UNDER THIS SEAT.** `g1_BASE_MOVED.md`. The RULEBOOK v3 seat landed `455d593`,
   `427985e` and `246af1c` on the same tree while P2a was being built. The complete delta is
   `docs/RULEBOOK.md` and the removal of `docs/acceptance_v2_0.json`. **No value-bearing artifact
   moved across it.** Recorded, not absorbed, per the F5 seat's precedent.

2. **REPAIR 1 — the lander refused a contended lock instead of waiting** (`ff64ef0`). Found by
   running the acceptance landing on a box where another seat held the lock. `build_lock.sh` prints
   the required line and waits; the lander must be interchangeable with it or seats work around
   whichever is stricter.

3. **REPAIR 2 — the lander deadlocked against its own gate** (`d02ef2b`, then `1aa63dd`). The lander
   holds the lock; its gate set runs the acceptance runner; the runner's determinism check shells out
   to `build_lock.sh run` and blocks on the lock the lander is holding. **The first fix was WRONG and
   the lander's own gate step caught it**: exporting `RL_BUILD_LOCK_HELD` to gate children made
   `build_lock.sh` see a reentrant grant, and also made `ruled_red_ledger` FAIL — an unknown
   RL_-prefixed variable changes how the r15 proof dies, so its probe no longer failed the way its
   ruling records. THE SECOND FIX STOPS CARRYING THE CONTRADICTION: `steps.LOCK_HELD_THROUGH = 'ui'`
   — the lock covers steps 0-6, which build; `gates`/`claims`/`commit` write nothing to the shared
   workspace and the one gate that builds takes the lock itself. No child carries the variable.

4. **REPAIR 3 — THE TWICE-BURNED RULE, THIRD OCCURRENCE, and it was this package's own** (`d044437`).
   `RL_LANDING_SNAPSHOT_DIR`, the override for where the restore point is stored, was inherited by
   every probe child and drifted the same r15 probe — red-ing a whole acceptance landing.
   Reproduced in one line in both directions on the live tree. `acceptance/checks/ledger.py:29-34`
   had already written the rule down after the identical burn ("A TOOL'S OWN FLAGS ARE NEVER RL_*")
   and this seat read it as a rule about FLAGS, then wrote a comment in `carriers.py` explaining why
   an ENV VAR was fine. It was not. Renamed to `LANDING_SNAPSHOT_DIR`; the wrong comment is replaced
   by the measurement that disproves it; and preflight now PRINTS the RL_/PAR_ environment the
   landing inherited, so the next seat sees the poison list before the gate red.

5. **REPAIR 4 — the self-test tore down its own transcripts before writing its summary** (`1aa63dd`).
   It reported `FAIL` with a reason line reading `17 PASS / 0 FAIL`. Found by the acceptance landing,
   whose gate step runs the self-test without an evidence directory. A defect in the harness, found
   by the program the harness tests.

6. **ONE BEHAVIOUR CHANGE AGAINST THE HAND SCRIPTS, declared:** the contract writer PRESERVES the
   committed file's trailing newline. Every hand-written landing script printed a note about the
   discrepancy and dropped the byte anyway, so a landing that moved nothing still moved a file. With
   the repair, a no-op rehearsal is genuinely byte-exact.

7. **THE PACKET VALIDATOR'S OWN FIRST RUN FAILED TWICE**, and both failures were real defects in the
   instrument: a prefix-matching heading pattern that accepted "Costing" as the cost slot, and an
   order check that compared a list against itself and could never fire. Both fixed, both recorded
   in the code.

8. **`PACKET_D8.md` DOES NOT PASS the packet validator**, and that is recorded rather than smoothed.
   It predates the template and numbers its sections its own way. The slot list is the PLAN's; D8 is
   where the CONTENT of each slot is shown to exist, and `packet.py` maps slot to D8 section.

9. **NO REAL BOARD-MOVING LANDING HAS BEEN RUN BY THIS LANDER.** The acceptance is a no-op rehearsal
   on a real build plus fault cases on a synthetic move; the first act that actually moves a board
   runs under the 2a.4 soak with hand-verification alongside. That is what the soak rule is for, and
   it is stated here so nobody reads §5 as more than it is.

## 7. G4 — WHAT PACKAGE 2a RETIRES, NAMED

The plan's net-negative-process test: every mechanism names what it retires, and anything that
cannot, stays out. P2a names four, and **three of the four retire ON THE OWNER'S WORD PER ACT TYPE
(G3.iv), not on this seat's say-so** — the soak rule (2a.4) is conduct, and the lander prints it at
every completion: *"SOAK: hand-verification stands until the owner's word per act type (G3.iv)."*

| retired | by what | when |
|---|---|---|
| **The hand-walked landing checklist** — the tail sequence a seat re-derived from the last act's evidence dir each time | `LEVER_SEQUENCE`: the order is stated once, in code, and executed | on the owner's stand-down word for lever landings |
| **Per-act script writing** — the five `land_*`/`append_*`/`register_*` scripts each landing wrote by adapting the previous landing's | the library + the act spec: the per-act content is now a dozen data slots | immediately for the writers; the SPEC still needs a seat's judgment |
| **The forgotten-UI-writer class** — the trap this tree caught three times and then documented three more times | `steps.ui` runs both writers and reads the identity back OUT of the bundle; a skipped writer 2 is a fault case in the self-test | immediately — it is now impossible to land with one writer and pass |
| **Supervisor re-derivation of the landing's mechanical facts** | the claims file, emitted by the transaction and verified by `tools/claims.py` (P1 1c) — the lander is now a producer of it, not a seat writing one afterwards | already ruled by 1c; P2a supplies the producer |

**NOT retired, and named so nobody assumes otherwise:** judgment review of any kind; the prereg; the
owner's landing/publish words; the independent read; the manual round path (which is 3a's interim
writer for the whole 3a→2b window and must not be retired before 2b exists); and hand-verification
itself, until the owner's word per act type.

## 8. OPEN, REFERRED

1. **`land round` is not built** — PACKAGE 2b, after 3a, by the plan's own sequence. The verb exists
   and says what it waits for.
2. **The claims step re-runs the whole gate set**, because `tools/claims.py` recomputes every claim
   and never reads a verdict back — so a landing pays for its gates twice. That is the 1c rule
   working as designed, and the measured price of an independently verifiable claims file. It is
   named here as a cost the owner may want to rule on, not smuggled.
3. **The first REAL board-moving landing has not happened.** It runs under soak, hand-verification
   alongside, per 2a.4.

## 9. G1 — THE STANDING FALSIFIER

`g1_BEFORE_REBASED.txt` (at `246af1c`, this package's base — see `g1_BASE_MOVED.md`) against
`g1_AFTER.txt` (after the last code commit `d044437`). **The complete diff is ONE LINE:**

```
1c1
< commit            246af1c7e0b51640294c5e6a636dc2de9ad8feae
---
> commit            d0444377e273e6d1fb37a8277cea56aff139b699
```

The commit line moves by construction — this package made commits. **Every value-bearing artifact is
byte-unmoved**: the board `68be10c7`, the store `b745002e`, `_merged_recover.py` `1867e953`,
`rl_model.py` `6fe7c415`, `model_config.json`, all three fitted pickles, `LTI_REGISTER.md`,
`docs/RULEBOOK.md`, both UI bundles, every `expected_boot` pin, the contract seal `cde9f70a` and the
book seal `9f46aba3`. **PACKAGE 2a IS PURE TOOLING and the tree says so.**

The self-test asserts the same thing on every run, from the other side: `live_tree_untouched` hashes
every carrier in the live tree before and after the whole self-test and reds if one moved.
