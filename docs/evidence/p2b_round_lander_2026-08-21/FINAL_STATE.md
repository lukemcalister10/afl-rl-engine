# FINAL STATE — PACKAGE 2b, THE ROUND LANDER

> ## `land round` EXISTS, IS SELF-TESTED, AND HAS FLOWN A NO-OP AGAINST THE LIVE TREE.
> **Board `b3e8da99bc7f632e5d1eebc732f9cf01` BYTE-IDENTICAL before and after. Store
> `b745002eb0a0fbb1c34fa44f1ef708d6` BYTE-IDENTICAL. ZERO of 167 carrier files moved.
> Self-test 28 PASS / 0 FAIL — 17 steps broken, 17 caught, 17 aborts byte-exact.**
>
> **NO REAL ROUND WAS LANDED.** Round 24's scores do not exist. The deliverable is the proven
> machine, and its first real flight is round 24 under the soak rule (2a.4).

---

## 1. WHAT WAS BUILT

`tools/land round --spec <act_spec.json>` — the SECOND thin entry point over the P2a landing
transaction library, exactly as PLAN_v6 2a.1 required it to be built ("2b becomes a second thin
entry point — mirrored script pairs drift; the repo's loader/emitter history proves it").

**Fourteen steps. SEVEN of them are the lever lander's own functions**, registered again in
`ROUND_SEQUENCE` rather than copied. `tools/land` itself did not grow a line.

| # | step | | what it does |
|---|---|---|---|
| 0 | `preflight` | SHARED | clean tree, the build lock, the restore point |
| 1 | `sheet` | **NEW** | the sheet re-cut + its ONE pin declaration, own commit — PACKAGE 3a's form. **SOLE WRITER of `data/sheet_pins.json`.** |
| 2 | `scores` | **NEW** | the owner's score file of record and its bindings, asserted — never placed, never edited |
| 3 | `catchup_preflight` | **NEW** | the read-only preflight; CLEAN, not-already-applied, prereg counts, and the H2 injured∩listed check. Then the inputs commit |
| 4 | `advance` | **NEW** | the ARMED catch-up. `staged_apply` runs ADVANCE-REPIN inside its own transaction |
| 5 | `generator_sync` | **NEW** | the generator-side board copy, synced and DISCLOSED (ERRATUM E5) |
| 6 | `day0` | **NEW** | the day-0 reference regenerated AT the advance — and only here |
| 7 | `contract` | SHARED | `restamp_dynamic` + the bake-lane repin + check |
| 8 | `sibling` | SHARED | verify — after an advance the repin has already run in-transaction |
| 9 | `ui` | SHARED | **ALL FOUR** UI writers, and the identity read back out of the bundle |
| 10 | `movers_page` | **NEW** | the owner's movers page through the frozen `ui/templates` skeleton |
| 11 | `gates` | SHARED | the standard landing gate set |
| 12 | `claims` | SHARED | emit the claims file and verify it against the tree |
| 13 | `commit` | SHARED | ONE commit, explicit paths only |

**There is no `build_proofs` step and no `lineage` step, and both absences are load-bearing.** A
round advance does not build a candidate board and assert a predicted md5 — `staged_apply`
regenerates the board inside its own transaction from the staged store. And a round advance earns
no lineage entry and no out-of-round column (ERRATUM E5); `spec.validate` REFUSES a spec that
declares either.

**Every P2a lander rule applies identically, because it is the same code**: the build lock, the
explicit-path commits (P8), day-0 EXPLICIT and OFF-BY-DEFAULT with the mandatory printed row diff
(M1b), per-step machine timing (M2), the fv-provenance exclusion on the shared box (2a.1), and all
four UI bundle writers — the class closed by exhaustion on F-9/F-10 stays closed, inherited rather
than re-derived.

### THE PREREG A ROUND ADVANCE CAN HONESTLY MAKE

A lever landing's board is predictable and the lander refuses any other. **A round advance's board
is a function of scores nobody has seen**, so the round prereg predicts what a seat CAN know before
arming, and every field is a falsifier `advance` asserts against the tool's own output:
`round · listed · resolved · absent_dnp · scores_sha256 · ledger_before · ledger_delta`, plus
`board_before`. At R23 those were 23 · 411 · 411 · 393 · `e3d5410e0e57` · 3,086 · +411.

### THE ABORT LADDER GAINED WHAT A ROUND NEEDS

The round lander commits **mid-flight** — 3a's form puts the sheet in its own commit before the
advance, and the owner's input of record must enter the tree before anything is armed. So `_abort`
now **rewinds exactly the commits this landing made**: only when HEAD is its own last commit, only
back to the recorded base, refusing loudly otherwise. Byte-exact that stopped at the working tree
would have quietly excluded history. **Every round fault case asserts HEAD is back at the base.**

Step 0's clean-tree rule gained its first DECLARED exception, enumerated and printed: an act that
declares a sheet re-cut may start on exactly two dirty paths — the owner's sheet and its
prereg-lite — because committing them is the `sheet` step's job. An untracked *directory* is walked
and admitted only if every file under it is declared dirt.

---

## 2. THE SELF-TEST — 28 PASS / 0 FAIL

`docs/evidence/p2b_round_lander_2026-08-21/02_SELFTEST_RUN.txt` (transcripts in `02_selftest/`).

```
STEPS BROKEN 17   CAUGHT 17   ABORTED BYTE-EXACT 17
SELF-TEST: 28 PASS / 0 FAIL
```

**Every NEW round step broken once, by a fault that breaks the thing that step exists to check** —
the same standard the ten lever steps met, plus the HEAD assertion:

| step | fault | what it breaks |
|---|---|---|
| `sheet` | `sheet_pin_drift` | the owner sheet moves and its ONE declaration does not — the drift that halts ORDER 41 inside the staged transaction |
| `scores` | `scores_absent` | the act declares an owner file of record that is not in the tree |
| `catchup_preflight` | `round_already_applied` | the round is in the dedup ledger; the preflight says CLEAN and the advance would certify a round it did not apply |
| `advance` | `round_mismatch` | the act claims a round the tree is not standing on |
| `generator_sync` | `generator_drift` | the generator-side copy stops being the published board |
| `day0` | `day0_no_movers` | the M1b guard: the re-base is ACTIVATED and no row moves |
| `movers_page` | `movers_report_drift` | the report stops naming the board the manifest names |

Each: caught at that step, **carriers moved after abort: NONE (byte-exact)**, **HEAD back at the
base**.

**And the sole writer proved in both directions**, because a writer nobody has watched write is a
claim, not a fact. The sandbox performs a synthetic re-cut (one byte into a notes cell; md5 moves,
rows and injured=Y hold) and runs the step twice — negative first, so a dead assertion cannot pass
as a live one:

* `sheet_recut_wrong_prediction` — a prereg-lite predicting the wrong md5 **HALTS**; the
  declaration is not written and HEAD is back at the base.
* `sheet_recut_writer` — the correct prediction writes the pin, commits sheet + declaration +
  prereg-lite as ONE explicit-path commit, and **asserts `engine_head` UNMOVED across it**.

The non-vacuity controls run first and always: a clean lever no-op AND a clean round rehearsal must
SUCCEED in the same sandbox before any fault case is believed. The live tree is hashed before and
after the whole self-test and asserted byte-unmoved.

---

## 3. THE DRY RUN — THE NO-OP PROOF ON THE LIVE TREE

`tools/land round --spec ACT_SPEC_DRYRUN.json --dry-run`, on a clean tree at `cd53872`.
Transcript: `03_DRYRUN_STDOUT.txt` / `03_DRYRUN.log` / `03_DRYRUN_REPORT.json`.
Predictions written and committed **first**: `01_DRYRUN_DECLARATION.md`.

**LANDING COMPLETE — every step's postcondition held.** All fourteen steps ran.

| # | prediction | measured | |
|---|---|---|---|
| P1 | board `b3e8da99bc7f632e5d1eebc732f9cf01` byte-identical | `b3e8da99bc7f632e5d1eebc732f9cf01` | **MET** |
| P2 | store `b745002eb0a0fbb1c34fa44f1ef708d6` byte-identical | `b745002eb0a0fbb1c34fa44f1ef708d6` | **MET** |
| P3 | ZERO carriers move | **0 of 167 carrier files moved** | **MET** |
| P4 | `as_of_round` holds at 23 in all three carriers | 23 / 23 / 23 | **MET** |
| P5 | `engine_head` `3af8c1f7…` unmoved | unmoved | **MET** |
| P6 | sheet pins `21361291f26d35108b88f92f885c5063` / 219 / 35 | unchanged | **MET** |
| P7 | every step runs; commit commits nothing | 14/14 OK; `--dry-run: not committing` | **MET** |
| P8 | the pre-transaction self-test passes first | 28 PASS / 0 FAIL, filed at `preflight_lander_selftest/` | **MET** |
| P9 | the STANDARD gate set, all green | 5/5 PASS, acceptance runner GREEN 17/17 in-transaction | **MET** |

### MEASURED STEP TIMINGS (the M2 measure-then-quote ruling)

```
    preflight          0.11s      contract           0.01s
    sheet              0.00s      sibling            0.14s
    scores             0.00s      ui                 0.09s
    catchup_preflight  0.00s      movers_page        0.14s
    advance            0.01s      gates            427.96s
    generator_sync     0.00s      claims             0.04s
    day0               0.00s      commit             0.02s
                                  TOTAL            428.52s
```

**THE COST OF A ROUND ADVANCE IS ITS GATES, AND NOTHING ELSE COMES CLOSE.** 427.96s of 428.52s is
the gate step, and 425.0s of that is the acceptance runner, whose own dominant leg is the
build-twice determinism check (two full builds). The thirteen other steps together cost **0.56
seconds** in this rehearsal. That is the honest quote for the no-op shape; a REAL advance adds the
armed catch-up itself (one staged transaction with a board regen and the sibling repin inside it,
the R23 measurement of which is in `docs/evidence/r23_advance_2026-08-20/`), plus the four UI
writers (~2.6s measured in the self-test sandbox), plus the sheet/scores/preflight legs (the
preflight measured at 0.135s on the live tree). **No turnaround target is quoted here that this
package has not measured.**

Individual gate timings: `release_manifest_check` 0.1s · `release_contract_check` 0.1s ·
`acceptance_runner` 425.0s · `movers_transition` 2.0s · `movers_ui` 0.7s.

### ONE THING THE DRY RUN FOUND, AND IT IS A CORRECTION TO A FENCE, NOT A DEFECT IN THE TREE

The first draft of `movers_page` asserted unconditionally that the round's movers report names the
live board. On this tree it does not, and **both facts are correct**: the R23 report names
`7a3f4fe2`, and three out-of-round columns have been registered at round 23 since
(`the-f5-rounding-20-8`, `the-backrows-repair-20-8`, `the-staircase-adoption-21-8` → `b3e8da99`).
An unconditional equality would have been the estate's fifth hand-typed instrument: true the day it
was written, a false red the day the tree legitimately moved (process law P4). The fence now has
two forms — the strict one binds when THIS transaction applied the round; the standing one, which
binds always, is a cross-artifact equality (the shipped movers bundle's own copy of the round-N
report must agree with the report of record on all four identities) and it is what the
`movers_report_drift` fault case fires on. Drift that is not explained by a stored out-of-round
point at this round still halts.

---

## 4. THE MANIFEST CARRIER-FIELD EXTENSION

PACKAGE 3a specified this and deferred it to 2b in its own words. Delivered:

**`release_manifest_check.py`: 40 → 43 carrier fields, 8 → 11 identities, 7 → 8 files.** New
identities `sheet` / `sheet_rows` / `sheet_injured_y`; new carrier group `sheet_pins`; one field
each. Truth is COMPUTED FROM THE ARTIFACT — the gate reads the file the DECLARATION names, md5s the
raw bytes, counts `csv.DictReader` rows and injured=Y rows, **character for character what ORDER 41
and ORDER 42 do**, because a gate that measured the sheet a nearly-identical way would pass a file
the build then halts on. There is still not one identity literal in that file. The fields are
`live`, never `sealed`: a sheet that has moved without its declaration moving is not a lag, it is a
build about to halt.

Measured on the live tree: **42 of 43 coherent, 0 incoherent, 1 sealed-lag**
(`book_stable_seal.head_md5`, pre-existing since 3a's engine edit, reported and non-gating).
Negative control, run against a doctored declaration on a copy of the tree:
`sheet_pins:sheet_injured_y` halts with `99 (expected 35)`.

`acceptance/checks/manifest.py` and `acceptance/checks/__init__.py` extend `_GROUPS`/`_IDENTS` so
the blocked-once law covers the new carrier at `<group>:<identity>` granularity.

---

## 5. THE RUNBOOK AMENDMENT — `ERRATUM E8`

`docs/runbooks/R23_RUNBOOK.md`, the seventh erratum, which is itself the argument for the pin file's
header being the rule's durable home and the runbook merely repeating it.

* the errata table gains row **E8**;
* **§3 THE COMMAND LIST is now the FALLBACK.** The primary path is `tools/land round`; every command
  in the section is named as a step of that program. Kept written down because an unexercised
  fallback is fake safety (2a.3), retired for this act type only on the owner's word (2a.4);
* **E7's "THE INTERIM WRITER — say it out loud, because it expires" clause is struck through and
  superseded in place.** It expired the same day it was written. `land round`'s `sheet` step is the
  SOLE WRITER of `data/sheet_pins.json`;
* §2's ADVANCE-REPIN note repointed at the lander.

`data/sheet_pins.json`'s `_writer_of_record` header — the rule's durable home — records the same,
and a new `_manifest_checked` header names the gate. **PROSE ONLY: the three pinned facts,
`sheet_path`, `pinned_at` and `provenance` are byte-unchanged.**

---

## 6. THE DAY-0 REFERENCE (register v810 item 1)

The register's words: *"the standing DAY0_CP.json wants regeneration AT THE R24 ADVANCE (its natural
home; the round lander 2b inherits it as a step or the advance does it once by hand — DO NOT re-base
mid-round)."*

The round lander **inherits it as a step**, and the inheritance is structural rather than
remembered: `day0` exists in `ROUND_SEQUENCE` and nowhere else, so a mid-round act cannot activate
one even if its spec asked. It is still EXPLICIT, still OFF BY DEFAULT, and still carries the
mandatory printed row diff (M1b). **The lander does not compute day-0**: the act's spec names the
GENERATOR — the emitter of record, where the law is carried (`ok_day0.py` → `fcrb_day0.py` →
`cprb_day0.py`, each carried with its changes declared) — the lander runs it as a child, prints the
diff between the standing reference and what the generator produced, and installs. Computing the law
here would create a second implementation beside the emitter, which is the mirrored-pair hazard M1b
warns about. `docs/evidence/final_candidate_2026-08-19/DAY0_CP.json` is a declared carrier, so an
activated re-base that then aborts puts the standing reference back byte-exact.

**It is not activated by this act.** Activating it at R24 is an owner-visible input and the R24 seat
carries the emitter selection.

---

## 7. THE ACT'S OWN IDENTITIES

| identity | before | after | |
|---|---|---|---|
| board `data/rl_build/rl_app_data.json` | `b3e8da99bc7f632e5d1eebc732f9cf01` | *same* | **BYTE-UNMOVED** |
| store `engine/rl_after/rl_model_data.json` | `b745002eb0a0fbb1c34fa44f1ef708d6` | *same* | **BYTE-UNMOVED** |
| `engine_head` | `3af8c1f7d61275c198a5df70c34608c7` | *same* | **BYTE-UNMOVED** — no engine file touched |
| `as_of_round` | 23 | 23 | HELD |
| sheet pins (md5 / rows / injured-Y) | `21361291f26d…` / 219 / 35 | *same* | **BYTE-UNMOVED** |
| every one of the 167 carrier files | — | — | **0 moved** |

This is a tooling act under process law **P1**: it moves no value-bearing artifact, and the
before/after identity list is the standing falsifier, not a courtesy.

**`docs/OPEN_ITEMS_REGISTER.md` and `docs/register/` were NOT touched.** That pen is the
supervisor's.

---

## 8. WHAT IS STILL OWED, STATED PLAINLY

* **The lander is UNFLOWN on a real round.** Its first flight is R24, and the soak rule (2a.4)
  stands: supervisor hand-verification runs ALONGSIDE it, standing down for this act type only on
  the owner's word. The manual path stays in the runbook until then.
* **`engine/rl_after/_merged_recover.py`'s `_sheet_pins()` header still says "until PACKAGE 2b's
  `land round` exists, the INTERIM WRITER is the amended manual path".** That sentence is now stale.
  It is NOT fixed here, deliberately: it is a comment, and editing it would move `engine_head` in a
  tooling act — the exact red ERRATUM E7 exists to prevent. The rule's durable home
  (`data/sheet_pins.json`) and the runbook are both correct; the engine comment is a repeat, and it
  is queued for the next act that legitimately touches that file.
* **The day-0 regeneration is not activated**, by design. It is an owner-visible input at R24.
