# RULEBOOK AMENDMENT — PLAN_v6 ITEM 1b. **PROPOSED. NOT APPLIED. AWAITING THE OWNER'S SIGNATURE.**

`docs/RULEBOOK.md` is the owner-signed single governing document and RULEBOOK law 10(a) makes any
change to it an owner-word act. So this file is the DIFF, drafted, checked, and left unapplied.
Nothing in `docs/RULEBOOK.md` has been edited. Nothing in `docs/acceptance_v2_0.json` has been
edited. The tooling that makes each option real is built and demonstrated below; the acts
themselves wait.

**Three questions need a word.** Everything else in 1b landed without one.

---

## QUESTION 1 — the law-count flag, measured

The register header has carried this for months:

> flag standing: RULEBOOK.md Part 1 numbers 11 laws vs '13' in its commit message + seat brief —
> owner to eyeball

**It is not an eyeballing problem and it is not a miscount.** `tools/rulebook_lint.py` resolves it
mechanically: PART 1 numbers **eleven** laws, and the twin `docs/acceptance_v2_0.json` carries
**thirteen**. The two extra are real entries with real thresholds, and they appear in no numbered
law:

| twin law | its payload | where it appears in the RULEBOOK |
|---|---|---|
| `G-Y0` | `check: "pooled abs pct"`, `max_pct: 2.0` | **nowhere** |
| `G-COHORT` | `check: "walk-forward book ratio"`, `max: 1.3`, `note: UNMEASURED at R19 until harness migration rebuilds the book` | PART 3 names G-COHORT as *currently UNMEASURED* — as a measurement status, not as a numbered law |

So the "13" was never wrong about anything except which document it was counting. **The flag is a
question about two laws, not about arithmetic**, and only the owner can answer it:

- **1A — they are laws.** They enter PART 1 as laws 12 and 13 (draft wording in the diff below,
  Section A, marked OPTIONAL). The count becomes 13 everywhere and the flag closes.
- **1B — they are gate thresholds, not laws.** They leave the twin and live where measurement
  detail lives. The count is 11 everywhere and the flag closes.

`tools/rulebook_twin.py` **refuses to regenerate the twin** until this is answered, by design:

```
$ python3 tools/rulebook_twin.py diff
REGENERATION REFUSED: the committed twin carries 2 law(s) the RULEBOOK does not number:
G-COHORT, G-Y0. Regeneration REFUSES rather than choosing: either the RULEBOOK gains them (an
owner-signed amendment, RULEBOOK law 10(a)) or they leave the twin. This is the register's standing
law-count flag, and it is not a generator's to settle.
```

A generator that silently dropped them, or silently kept them, would have decided an owner-signed
question by itself. It stops instead.

---

## QUESTION 2 — the process laws land, as PART 4

Ten standing process laws are restated in every seat brief and enforced by nobody in particular.
1b lands them in the one governing document. **Each one names the incident that created it** — a law
without an incident is a preference, and the estate has enough of those.

They enter as **PART 4, numbered P1–P10**, NOT appended to PART 1. PART 1 is about the model, its
count is the subject of Question 1, and renumbering it in the same act would make the flag harder
to close rather than easier. `tools/rulebook_lint.py` already parses and number-checks a process-law
section; it currently reports *"no such section in the RULEBOOK yet — the rule is armed and simply
has nothing to read"*.

---

## QUESTION 3 — `docs/acceptance_v2_0.json`, disposed of

The RULEBOOK calls it its **Twin**. It declares itself `regenerated_from RULEBOOK.md v2.1`. **No
code reads it and no code regenerates it.** It is a hand-maintained derived laws view with no
regeneration trigger and no banner — the in-tree violator of "no second laws file, ever". Both
disposals are built. The owner picks one.

### OPTION A — WIRE IT (built, `tools/rulebook_twin.py`)

| | |
|---|---|
| derived every run | version, date, `regenerated_from`, the law set, the law ORDER, the banner |
| carried by law id | each law's `check` prose and thresholds (`pick1_equals`, `band_scar`, `max_pct`, …) |
| refuses | any law in the twin the RULEBOOK does not number (Question 1) |
| CI-enforced | `tools/rulebook_lint.py` R5/R6 red on parity loss or a missing banner; the runner's `rulebook_lint` row carries it on every push |

The carried half is stated honestly rather than hidden: those thresholds are measurement detail
that exists **nowhere else in the tree**, so a regenerator that dropped them would destroy
information and one that invented them would be worse. The banner says exactly that, in the file.

### OPTION B — REMOVE IT

`git rm docs/acceptance_v2_0.json`, plus the two pointer edits the removal requires. **Every reader
enumerated** (the 3b PRE-ACT discipline, applied):

| reader | line | what the removal owes it |
|---|---|---|
| `docs/RULEBOOK.md` | `:6` — "Twin: docs/acceptance_v2_0.json." | the line goes (it is in the diff below, Section C) |
| `docs/referee/REFEREE_PROTOCOL.md` | `:10` — "gates bound to `docs/acceptance_v2_0.json`" | repoint to the RULEBOOK, same act |
| `docs/referee/F3_REVIEW_v0_3.md`, `docs/directives/ITEM_408_COLD_REVIEW_partial.md` | past-tense records of what was reviewed | **nothing** — history is frozen, never rewritten |
| any code | — | **none exists**; measured, not assumed |

Under Option B the thresholds in Question 1's table are the only content that dies with the file, so
Option B and answer 1B should be taken together or not at all.

**Not a third option:** leaving it as it is. The rulebook lint is armed and reds on it; the red is
carried as presented ruling `RB1-rulebook-twin-unruled-laws` in `acceptance/ruled_red.json`, whose
own expiry probe retires it the moment this signature lands. The ledger is not a place to park a
question indefinitely (`ruled_red.json:_how_to_add` — *"RULED-RED is not a snooze button"*).

---

# THE DIFF

Apply with `git apply` after the word is given; the three sections are independent.

## Section A — PART 1 (OPTIONAL, only under answer 1A)

```diff
diff --git a/docs/RULEBOOK.md b/docs/RULEBOOK.md
index 8a4875d..80e2214 100644
--- a/docs/RULEBOOK.md
+++ b/docs/RULEBOOK.md
@@ -33,6 +33,12 @@
 11. **THE SEAM PATTERN.** Every release ships a numbered claims note and receives one
     blind independent review before the owner's word. The register stays the single
     durable list.
+12. **YEAR-0 CLOSURE (G-Y0).** The pooled absolute percentage gap at the year-0 lens
+    stays within 2.0% — present-lens prices close against the store they are priced
+    from, or the lens is reported broken.
+13. **COHORT CURVE (G-COHORT).** The walk-forward book ratio stays at or under 1.3.
+    UNMEASURED at R19 and since: it needs the walk-forward book, and PART 3 reports it
+    UNMEASURED rather than assuming it passes.
 
 ## PART 2 — DATED READS — **ALL RETIRED (owner, 2026-07-22: "they've done their job")**
 The pre-seam reads (A-BONT · A-GAWN · A-CAM · A-DARCY · A-DUUR · A-PAIRS · A-PEAK · english_briggs)
```

> Committed verbatim as `docs/proposals/rulebook/patch_A.diff`; `git apply --check` passes against `docs/RULEBOOK.md` at 0244935.

*(Under answer 1B this section is not applied, and `G-Y0` / `G-COHORT` leave the twin instead.)*

## Section B — PART 4, the process laws

```diff
diff --git a/docs/RULEBOOK.md b/docs/RULEBOOK.md
index 8a4875d..5a90e4d 100644
--- a/docs/RULEBOOK.md
+++ b/docs/RULEBOOK.md
@@ -54,5 +54,57 @@ new dated reads enter this file only on his word.
   2-row waiver) carry forward AS RECORDED until Luke re-rules or the underlying rows
   change.
 
+## PART 4 — PROCESS LAWS (how work is done; each names the incident that created it)
+P1. **THE BOARD MOVES ONLY IN AN ACT THAT SAYS IT WILL.** A process, tooling or
+    documentation change leaves every value-bearing artifact byte-identical, and the
+    before/after identity check is the standing falsifier, not a courtesy.
+    *Incident: the H3 back-rows repair was measured, found to move the board of record,
+    and correctly REVERTED because no owner word then covered it — 2026-08-20, and the
+    word was later given as its own act.*
+P2. **NEVER BOOT ON AN UNVERIFIED STORE.** Any gate, build or suite asserts the store
+    and engine head it is about to read against the pinned boot identity, and HALTS
+    otherwise, before anything loads.
+    *Incident: the stale-boot hardening of 2026-07-05 — the four data guards validate
+    whichever directory they are imported from, so a stale-but-self-consistent workspace
+    passed all of them silently. Owner ruling, in writing: "the Guard 5 pre-flight is a
+    safety addition, not a frozen-gate amendment; apply and keep it."*
+P3. **ONE WRITER.** Every engine act holds the build lock. Two overlapping acts through
+    the shared workspace produce results that look clean and are void.
+    *Incident: 2026-07-31 — it happened, and `tools/preboot_assert.sh` exists because it
+    did. A detector was not enough: two seats that check simultaneously both see a clear
+    board, so the interlock is a lock, not a check.*
+P4. **ASSERT THE RELATIONSHIP, NEVER THIS MONTH'S NUMBER.** A gate computes the truth
+    from the artifact and asserts the carriers agree with it. A hand-typed identity in a
+    check is a red waiting for the next legitimate move.
+    *Incidents, four instruments retired for exactly this: the panel 10/10, the movers
+    "exactly two known-reds", the R14 fixture config pin, and BOARD_MD5_GOOD.*
+P5. **A GATE'S NAME IS NOT COVERAGE.** A ceremony or law may claim a covering gate only
+    with a recent green verdict from it. Dormant is not dead, and named is not run.
+    *Incident: `ship_gates_check.py` — the frozen acceptance suite, named in the bake
+    checklist as the bar — was self-bricked on its own RL_GAMMA line and then blocked by
+    a hardcoded workspace path, and did not execute one gate for weeks while being cited.*
+P6. **GENERATED-ONLY.** A derived surface that cannot be generated does not exist. No
+    derived view is hand-maintained, whatever banner it carries.
+    *Incident: `docs/CURRENT_STATE.md` carries an authority banner and sat 156 register
+    versions stale.*
+P7. **RULED-RED IS NOT A SNOOZE BUTTON.** A known red is carried only while it is
+    presented in writing, still measurable, and still failing the recorded way. An entry
+    stops matching, it reds the run.
+    *Incident: the R2 ledger entry demanded its own retirement within an hour of being
+    written, because the fork it recorded was repaired upstream while it was being built.*
+P8. **EXPLICIT PATHS ONLY.** Every commit stages named paths. No `git add -A`, no sweep,
+    no bare `git commit`.
+    *Incident: register v786; the discipline every act since has recorded in its own
+    final state.*
+P9. **THE PREREG COMES FIRST.** An act that touches an engine file commits its
+    predictions and falsifiers BEFORE the edit, and corrects the prereg against the tree
+    rather than the tree against the prereg.
+    *Incident: the F5 act's A6 clause predicted `engine_head` would move; it does not
+    (it tracks `_merged_recover.py`, and the act edited the exporter). The prereg was
+    corrected against the tree and the error named rather than quietly satisfied.*
+P10. **NO SECOND LAWS FILE, EVER.** These laws live here. Any derived view is generated,
+    carries a do-not-hand-edit banner, and is CI-linted equal to this document.
+    *Incident: `docs/acceptance_v2_0.json` — declared regenerated from this file, read
+    and regenerated by no code, and two laws out of step with it for months.*
 ## SIGNED
 Owner word given in chat 2026-07-22. Twin regenerated. CONSTRAINTS v1.19 + acceptance v1.21 archived.
```

> Committed verbatim as `docs/proposals/rulebook/patch_B.diff`; `git apply --check` passes against `docs/RULEBOOK.md` at 0244935.

## Section C — the twin pointer

Under **Option A** (wire it):

```diff
diff --git a/docs/RULEBOOK.md b/docs/RULEBOOK.md
index 8a4875d..5f9b4d5 100644
--- a/docs/RULEBOOK.md
+++ b/docs/RULEBOOK.md
@@ -3,7 +3,9 @@
 ### scoped to the national pick curve, picks 1–64. Pool selections past 64 are valued by
 ### position and are not on the curve, so no ordering applies to them. No other law changed.
 ### Replaces CONSTRAINTS v1.19 + acceptance v1.21 as the single governing document.
-### Twin: docs/acceptance_v2_0.json. Predecessors archived at the 2026-07-22 seam.
+### Twin: docs/acceptance_v2_0.json — GENERATED from this file by tools/rulebook_twin.py and
+### CI-linted equal to it by tools/rulebook_lint.py. THIS DOCUMENT WINS; the twin is never
+### hand-edited. Predecessors archived at the 2026-07-22 seam.
 
 ## PART 1 — TIMELESS LAWS (never expire; asserted at every release)
 1. **ONE SOURCE.** Exactly one authored data source: `engine/rl_after/rl_model_data.json`.
```

> Committed verbatim as `docs/proposals/rulebook/patch_C_optionA.diff`; `git apply --check` passes against `docs/RULEBOOK.md` at 0244935.

Under **Option B** (remove it):

```diff
diff --git a/docs/RULEBOOK.md b/docs/RULEBOOK.md
index 8a4875d..c9ef992 100644
--- a/docs/RULEBOOK.md
+++ b/docs/RULEBOOK.md
@@ -3,7 +3,8 @@
 ### scoped to the national pick curve, picks 1–64. Pool selections past 64 are valued by
 ### position and are not on the curve, so no ordering applies to them. No other law changed.
 ### Replaces CONSTRAINTS v1.19 + acceptance v1.21 as the single governing document.
-### Twin: docs/acceptance_v2_0.json. Predecessors archived at the 2026-07-22 seam.
+### No twin: the derived laws view is retired (PLAN_v6 1b). Predecessors archived at the
+### 2026-07-22 seam.
 
 ## PART 1 — TIMELESS LAWS (never expire; asserted at every release)
 1. **ONE SOURCE.** Exactly one authored data source: `engine/rl_after/rl_model_data.json`.
```

> Committed verbatim as `docs/proposals/rulebook/patch_C_optionB.diff`; `git apply --check` passes against `docs/RULEBOOK.md` at 0244935.

---

## WHAT LANDED WITHOUT A SIGNATURE (1b's unsigned half)

| built | what it does |
|---|---|
| `tools/rulebook_lint.py` | six rules over the RULEBOOK: signed, numbered, counted, one laws file, twin parity, twin banner |
| `tools/rulebook_twin.py` | the regenerator the twin never had — `diff` / `write` / `check`, and the refusal above |
| `acceptance/checks/standing.py::rulebook_lint` | the lint as a registered runner check, adjudicated against the ledger |
| `acceptance/ruled_red.json::RB1` | the current finding carried as a presented ruling, with an expiry probe that retires it the moment this signature lands |
| `.github/actions/host-insensitive-gates` | the lint on every push, in all four push workflows |

---

## THE DIFF WAS APPLIED, MEASURED, AND REVERTED — in an isolated worktree, 2026-08-20

A proposed diff nobody has tried to apply is a wish. All three signable sections (A + B + Section C
Option A) were applied together to a clean worktree at `0244935`, the twin was regenerated, and the
result measured. `docs/RULEBOOK.md` on the live tree was never touched.

```
$ git apply patch_A.diff patch_B.diff patch_C_optionA.diff
$ python3 tools/rulebook_lint.py .
rulebook_lint: 1 FAIL
  note PART 1 laws counted: 13   (… G-Y0, G-COHORT)          <- R5 TWIN PARITY closes
  note PROCESS LAWS counted: 10  (P1 … P10, contiguous)       <- R2 numbering holds
  FAIL R6 TWIN BANNER: docs/acceptance_v2_0.json carries no banner

$ python3 tools/rulebook_twin.py write --root .
wrote docs/acceptance_v2_0.json (13 laws)

$ python3 tools/rulebook_lint.py .
rulebook_lint: 0 FAIL

$ python3 tools/rulebook_twin.py check --root .
twin is byte-identical to its regeneration (13 laws)
```

Signing this closes the count flag, lands the process laws, disposes of the twin, and expires
ruled-red `RB1` in the same act — the ledger probe (`python3 tools/rulebook_lint.py`, exit 0) then
FAILS the runner until the entry is retired, which is the ledger doing its job.

---

# APPENDED 2026-08-20 — A PROPOSED ELEVENTH PROCESS LAW, P11

**Still PROPOSED. Still NOT APPLIED.** This file is an unsigned draft and appending a proposed law
to it is a drafting act, not a ruling. `docs/RULEBOOK.md` is untouched; `docs/acceptance_v2_0.json`
is untouched. RULEBOOK law 10(a) still owns the signature.

Section B above lands ten process laws, each naming the incident that created it. **An eleventh
incident happened after that section was drafted, on the same day, and it is the cleanest example
the estate has produced of a failure mode none of P1–P10 covers.**

## P11 — RECORD THE RETIREMENT IN THE INSTRUMENT, IN THE SAME ACT

> **P11. THE RETIREMENT IS RECORDED WHERE THE GATE LIVES.** When a ruling retires or supersedes a
> gate, the retirement is written into the instrument that carries that gate **in the same act as
> the ruling**. An instrument that cannot run still gets its strike recorded — being unrunnable is
> the reason to record it, not an excuse to defer — so a revived instrument can never resurrect
> retired law.
> *Incident: A9 and B1, 2026-08-20. Both were retired by the owner — A9 as a player-ordering
> assertion, B1's July-8 cohort rail "weeks ago" — while `ship_gates_check.py` was bricked and
> executing no gate. Neither retirement was written into the suite, because the suite could not
> run. When 1a unbricked it, its first full run presented both as fresh reds at the current head,
> and they were filed as "TWO REDS THAT ARE NEW AT THE CURRENT HEAD". They were not new. They were
> unrecorded. Two rulings had to be re-obtained from the owner to un-say what he had already said.*

## WHY P1–P10 DO NOT ALREADY COVER IT

P5 ("a gate's name is not coverage") is the closest and it is the wrong direction. **P5 governs
what a dormant instrument may be CLAIMED to prove; P11 governs what a dormant instrument must be
TOLD.** P5 protects against believing a silent gate is green. P11 protects against believing a
revived gate is current. The A9/B1 episode tripped both halves of the same brick, in sequence:

| | P5, already drafted | P11, proposed here |
|---|---|---|
| the failure | the suite is cited as the bar while executing nothing | the suite is revived still carrying law the owner has repealed |
| what is lost | coverage that was never there | rulings that were genuinely given |
| the tell | a ceremony names a gate with no recent verdict | a first run since a repair produces "new" reds that predate it |
| the cost | undetected regressions | the owner re-adjudicating settled questions |

P7 ("ruled-red is not a snooze button") is adjacent and also does not reach: it disciplines how a
**live** red is carried. A9 and B1 were never carried — they were **retired**, and the retirement
evaporated because it was recorded only in conversation and in the register, never in the file that
does the asserting.

## THE FALSIFIER, so the law is testable rather than admirable

**A repaired or revived instrument's first run produces no verdict the owner has already ruled on.**
If it does, P11 was breached at the time of the ruling — the breach is dated to the ruling, not to
the revival. The 2026-08-20 first run fails this test twice, which is what makes it the incident.

## WHAT IT WOULD HAVE COST, MEASURED

Two lines. `gate('A9', ..., 'STRUCK', ...)` and B1's status, written on the day of each ruling
against a file that could not then execute them — the same two edits made today, weeks late, plus
the two re-obtained rulings and the finding document that had to be written to ask for them.

## PRECEDENT: THE MECHANISM ALREADY EXISTED

This law asks for nothing new to be built. `ship_gates_check.py` has carried the STRIKE mechanism
since **A15, struck by the owner on 02/07/2026** — recorded in the code, recorded in `SHIP_GATES.md`
with its reason, rendering `STRUCK` on every board run since, counted against nothing. A15 is what
compliance with P11 looks like, and it has looked like that for seven weeks. **A9 and B1 are now
recorded the same way, by the same mechanism, in this act** (`docs/evidence/gate_strikes_2026-08-20/`).
The proposed law is the generalization of a practice this instrument already had.

## IF SIGNED

`patch_B.diff` gains one entry, P11, after P10; the "PROCESS LAWS counted" line in
`tools/rulebook_lint.py`'s output becomes 11; nothing in Section A or Section C changes; Question 1
and Question 3 are untouched and still need their own answers. The patch file in this directory has
**not** been regenerated — it still carries P1–P10 — because regenerating it would present an
unsigned proposal as though it were part of the checked diff.
