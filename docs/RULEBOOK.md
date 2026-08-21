# THE RULEBOOK — v3 · 2026-08-20 · OWNER-SIGNED (in chat, 2026-07-22; amended 2026-07-28, 2026-08-20)
### Amendment v3 — THE OWNER'S WORD, VERBATIM (in chat, 2026-08-20): "Okay agree to the laws updated."
### Provenance: drafted under the locked process plan item 1b as
### docs/proposals/rulebook/AMENDMENT_1b_2026-08-20.md — a four-pass drafting chain plus cold review,
### every section applied and measured in an isolated worktree before presentation — and applied here
### on the owner's word. WHAT v3 CHANGED: law 11 amended (the numbered claims note stays universal and
### machine-generated; the blind independent review is scoped to releases that move player values);
### law 12, YEAR-0 CLOSURE, enters PART 1; PART 4 lands the standing process laws P1–P11, each naming
### the incident that created it; the derived twin is retired and its measurement thresholds are folded
### into PART 3. Laws 1–10 are byte-unchanged from v2.1.
### Amendment v2.1 (owner word, exact wording pre-filed and approved 2026-07-28): law 4 G-MONO
### scoped to the national pick curve, picks 1–64. Pool selections past 64 are valued by
### position and are not on the curve, so no ordering applies to them. No other law changed.
### Replaces CONSTRAINTS v1.19 + acceptance v1.21 as the single governing document.
### No twin: the derived laws view is retired (PLAN_v6 1b). Predecessors archived at the
### 2026-07-22 seam.

## PART 1 — TIMELESS LAWS — 12 laws (never expire; asserted at every release)
1. **ONE SOURCE.** Exactly one authored data source: `engine/rl_after/rl_model_data.json`.
   Everything else is derived, read-only, source-stamped. The five SSI guards HALT, never
   warn (spec: docs/SINGLE_SOURCE_INVARIANT.md — unchanged, still binding).
2. **SILENCE IS A RED.** A check that produces no verdict has failed, not passed.
3. **NO CLIFFS (L-SMOOTH).** Value moves smoothly across age, evidence, and position;
   no wide-bin jumps, no discontinuities a player could fall off.
4. **THE CURVE DESCENDS (G-MONO).** The national pick curve covers picks 1–64 and is
   strictly decreasing across that domain; pick 1 = 3000 exactly. Selections past pick 64
   are not on the curve — they enter the pool and are valued by position, where order of
   selection carries no value and no ordering is required or implied.
5. **SYMMETRY (L-SYMMETRY).** Upside and downside evidence move value by the same
   machinery; no one-directional levers.
6. **AGE FADES (L-SAGE-FADE / A-FADE, direction-only).** Veterans decline toward the
   measured floor, never below it, never propped above the evidence.
7. **THE CAPTAIN LIFT (L-CAPTAIN)** applies wherever a captaincy premium is measured,
   consistently, or nowhere.
8. **PROJECTION LENS (LENS-PROJECTION / CYCLE).** Year-0 prices off present position;
   years-1+ off future position; cohort curves off drafted position. Never inferred
   from one another.
9. **CONSERVATION.** Re-pricing redistributes value; it does not mint or burn it
   (ledger within the stated band).
10. **OWNER-ONLY WORDS.** Three actions need Luke's explicit word, under any level of
    model autonomy: (a) changes to THIS rulebook, (b) tags and releases, (c) arming the
    score-write. Everything else may run autonomous.
11. **THE SEAM PATTERN.** *Amended v3.* Every release ships a numbered claims note. That half
    is UNIVERSAL and admits no exception, and it is machine-generated and machine-checked
    (`tools/claims.py`) rather than written in prose — a claim nobody can recompute is not a
    claim. One BLIND INDEPENDENT REVIEW is required before the owner's word ONLY for a release
    that MOVES PLAYER VALUES; a release that moves no value-bearing artifact — tooling,
    documentation, process — ships on its claims note and its gates, with the byte-unmoved
    identity list as the standing falsifier that it was indeed such a release. The register
    stays the single durable list.
12. **YEAR-0 CLOSURE (G-Y0).** The pooled absolute percentage gap at the year-0 lens
    stays within 2.0% — present-lens prices close against the store they are priced
    from, or the lens is reported broken.

## PART 2 — DATED READS — **ALL RETIRED (owner, 2026-07-22: "they've done their job")**
The pre-seam reads (A-BONT · A-GAWN · A-CAM · A-DARCY · A-DUUR · A-PAIRS · A-PEAK · english_briggs)
are retired as checks. Recorded once so no reviewer re-flags them: english_briggs (>=1.75
captain-lifted) was anchored at the R14 lock and superseded by R15-19 results — the R19 board is
correct on current evidence. Going forward the board is judged by the owner's eye at each release;
new dated reads enter this file only on his word.

## PART 3 — MEASUREMENT STANDARDS (how rules are checked, not what they say)
- Statistics at the finest resolution the sample supports, smoothed; thin slices pooled
  deliberately and declared.
- Every gate names its measured value and margin, not only pass/fail; the three
  narrowest margins are always reported.
- A rule that cannot currently be measured is reported UNMEASURED — never assumed
  passing, never silently waived. (Currently UNMEASURED at R19: the conservation ledger —
  needs the leg-b movement ledger; it comes back green-or-red with the harness migration.)
- **G-COHORT is RETIRED, not unmeasured.** Owner, verbatim, 2026-08-20: *"That cohort rail again
  was retired. Weeks ago."* It was never a numbered law in this document and it is not numbered
  now. Its payload — the walk-forward book ratio against a hard 1.3, carried by the retired twin
  and by the July-8 construction in `ship_gates_check.py` — is struck in the instrument that
  asserted it: gate **B1, STRUCK** on those words, recorded in `ship_gates_check.py` and in
  `SHIP_GATES.md` §B (evidence: `docs/evidence/gate_strikes_2026-08-20/`), per process law P11.
  Recorded here once, with its number, so nothing is lost and no reviewer re-flags it as a
  missing measurement or revives it as a law.
- **MEASUREMENT THRESHOLDS.** Folded in on 2026-08-20 from the retired twin
  (`docs/acceptance_v2_0.json`, removed in the same act) so that no measurement detail died with
  it. These numbers and check prose lived nowhere else in the tree; every other section of the
  twin (its dated-reads list, its carried standing-fails and waivers) is already stated in PART 2
  and in the bullet below, verbatim, so this table is the whole of what the removal owed.

  | law | how it is checked | threshold |
  |---|---|---|
  | 1 ONE SOURCE | five SSI guards halt-not-warn; spec `docs/SINGLE_SOURCE_INVARIANT.md` | HALT, never warn |
  | 2 SILENCE IS A RED | every gate emits a verdict or halts; non-zero exit propagates | — |
  | 3 L-SMOOTH | no undeclared value discontinuities across age/evidence/position; a discontinuity is lawful only if registered before scoring with its step measured and reported as a margin | declared-or-red |
  | 4 G-MONO | national pick curve (picks 1–64) strictly decreasing; selections past 64 are pool-valued by position, unordered | `pick1_equals` = 3000 |
  | 5 L-SYMMETRY | upside and downside evidence use identical machinery | — |
  | 6 L-SAGE-FADE | veteran value declines toward the measured floor, never below, never propped | `direction_only` |
  | 7 L-CAPTAIN | captaincy premium applied consistently or not at all | — |
  | 8 LENS-PROJECTION | year-0 = present_position; years-1+ = future_position; cohort = drafted_position; never inferred | — |
  | 9 CONSERVATION | re-pricing redistributes value | `band_scar` = 200 |
  | 10 OWNER-ONLY WORDS | rulebook changes, tags/releases, score-write arming require the explicit owner word | — |
  | 11 SEAM PATTERN | every release: numbered claims note (universal, `tools/claims.py`) + owner word; blind independent review on value-moving releases; register is the single durable list | — |
  | 12 G-Y0 | pooled abs pct gap at the year-0 lens | `max_pct` = 2.0 |
  | *(retired)* G-COHORT | walk-forward book ratio — RETIRED, see the bullet above | *(was `max` 1.3)* |

- Standing-fails and named-row waivers from v1.21 (A2, A3, A12, A-PAIRS-3, the earned-
  2-row waiver) carry forward AS RECORDED until Luke re-rules or the underlying rows
  change.

## PART 4 — PROCESS LAWS (how work is done; each names the incident that created it)
P1. **THE BOARD MOVES ONLY IN AN ACT THAT SAYS IT WILL.** A process, tooling or
    documentation change leaves every value-bearing artifact byte-identical, and the
    before/after identity check is the standing falsifier, not a courtesy.
    *Incident: the H3 back-rows repair was measured, found to move the board of record,
    and correctly REVERTED because no owner word then covered it — 2026-08-20, and the
    word was later given as its own act.*
P2. **NEVER BOOT ON AN UNVERIFIED STORE.** Any gate, build or suite asserts the store
    and engine head it is about to read against the pinned boot identity, and HALTS
    otherwise, before anything loads.
    *Incident: the stale-boot hardening of 2026-07-05 — the four data guards validate
    whichever directory they are imported from, so a stale-but-self-consistent workspace
    passed all of them silently. Owner ruling, in writing: "the Guard 5 pre-flight is a
    safety addition, not a frozen-gate amendment; apply and keep it."*
P3. **ONE WRITER.** Every engine act holds the build lock. Two overlapping acts through
    the shared workspace produce results that look clean and are void.
    *Incident: 2026-07-31 — it happened, and `tools/preboot_assert.sh` exists because it
    did. A detector was not enough: two seats that check simultaneously both see a clear
    board, so the interlock is a lock, not a check.*
P4. **ASSERT THE RELATIONSHIP, NEVER THIS MONTH'S NUMBER.** A gate computes the truth
    from the artifact and asserts the carriers agree with it. A hand-typed identity in a
    check is a red waiting for the next legitimate move.
    *Incidents, four instruments retired for exactly this: the panel 10/10, the movers
    "exactly two known-reds", the R14 fixture config pin, and BOARD_MD5_GOOD.*
P5. **A GATE'S NAME IS NOT COVERAGE.** A ceremony or law may claim a covering gate only
    with a recent green verdict from it. Dormant is not dead, and named is not run.
    *Incident: `ship_gates_check.py` — the frozen acceptance suite, named in the bake
    checklist as the bar — was self-bricked on its own RL_GAMMA line and then blocked by
    a hardcoded workspace path, and did not execute one gate for weeks while being cited.*
P6. **GENERATED-ONLY.** A derived surface that cannot be generated does not exist. No
    derived view is hand-maintained, whatever banner it carries.
    *Incident: `docs/CURRENT_STATE.md` carries an authority banner and sat 156 register
    versions stale.*
P7. **RULED-RED IS NOT A SNOOZE BUTTON.** A known red is carried only while it is
    presented in writing, still measurable, and still failing the recorded way. An entry
    stops matching, it reds the run.
    *Incident: the R2 ledger entry demanded its own retirement within an hour of being
    written, because the fork it recorded was repaired upstream while it was being built.*
P8. **EXPLICIT PATHS ONLY.** Every commit stages named paths. No `git add -A`, no sweep,
    no bare `git commit`.
    *Incident: register v786; the discipline every act since has recorded in its own
    final state.*
P9. **THE PREREG COMES FIRST.** An act that touches an engine file commits its
    predictions and falsifiers BEFORE the edit, and corrects the prereg against the tree
    rather than the tree against the prereg.
    *Incident: the F5 act's A6 clause predicted `engine_head` would move; it does not
    (it tracks `_merged_recover.py`, and the act edited the exporter). The prereg was
    corrected against the tree and the error named rather than quietly satisfied.*
P10. **NO SECOND LAWS FILE, EVER.** These laws live here. Any derived view is generated,
    carries a do-not-hand-edit banner, and is CI-linted equal to this document.
    *Incident: `docs/acceptance_v2_0.json` — declared regenerated from this file, read
    and regenerated by no code, and two laws out of step with it for months. Disposed of
    under this amendment: the file is removed, its thresholds folded into PART 3, and
    `tools/rulebook_lint.py` R5/R6 now red on a derived laws view REAPPEARING.*
P11. **THE RETIREMENT IS RECORDED WHERE THE GATE LIVES.** When a ruling retires or
    supersedes a gate, the retirement is written into the instrument that carries that
    gate IN THE SAME ACT AS THE RULING. An instrument that cannot run still gets its
    strike recorded — being unrunnable is the reason to record it, not an excuse to
    defer — so a revived instrument can never resurrect retired law. Falsifier: a
    repaired or revived instrument's first run produces no verdict the owner has already
    ruled on; if it does, this law was breached at the time of the ruling, not at the
    revival.
    *Incident: A9 and B1, 2026-08-20. Both were retired by the owner — A9 as a player-
    ordering assertion, B1's July-8 cohort rail "weeks ago" — while `ship_gates_check.py`
    was bricked and executing no gate. Neither retirement was written into the suite,
    because the suite could not run. When it was unbricked, its first full run presented
    both as fresh reds at the current head and they were filed as "TWO REDS THAT ARE NEW
    AT THE CURRENT HEAD". They were not new. They were unrecorded, and two rulings had to
    be re-obtained from the owner to un-say what he had already said.*

P12. **THE PRICED-ARM READING.** Every value-moving adoption carries its own arm's no-arb
    band reading and class check PRE-FLIP, measured inside the prereg — a reading taken on
    a sibling variant does not cover the chosen arm.
    *Incident: the staircase adoption, 2026-08-21. Variant B's no-arb reading stopped the
    landing; the owner's chosen arm was A raw, and its own reading had to be (and was)
    measured inside prereg fb3d3c0 before the flip. This line makes that standing.*
P13. **A PINNED OWNER-INPUT HAS ONE NAMED WRITER.** The pins of an owner-supplied data
    input (today: the sitter sheet's md5/rows/injured-Y in `data/sheet_pins.json`) are
    written by exactly ONE writer of record — the round lander once P2b lands; in any
    window before a lander owns them, the runbook's manual path is EXPLICITLY the interim
    writer, stated in the runbook itself. A pin moved by any other hand is a halt, not a
    repair.
    *Incident: PACKAGE 3a, 2026-08-21 — the sheet pins left the engine for the data file;
    the writer-of-record rule rode the act as runbook ERRATUM E7 pending this line.*

## SIGNED
Owner word given in chat 2026-07-22; amended 2026-07-28 (v2.1) and 2026-08-20 (v3, "Okay agree to
the laws updated."). The derived twin is retired, not regenerated — this document is the only laws
file. CONSTRAINTS v1.19 + acceptance v1.21 archived.
P12–P13 amendment signed 2026-08-21, owner word verbatim: "Sign the rulebook, that's fine" — given
against the supervisor's described batch (the pin-file interim-writer rule + the per-arm no-arb
reading patch queued at the staircase adoption).
