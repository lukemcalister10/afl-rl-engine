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
    score-write (for weekly scores, the owner sending the file IS the word — P14). Everything
    else may run autonomous.
11. **THE SEAM PATTERN.** *Amended v3; amended 2026-10-13.* Every release ships the landing's
    own machine-written record (the lander's REPORT.json and FLIGHT.log: every identity it
    measured, every gate's verdict) — a claim nobody can recompute is not a claim. The separate
    claims note (`tools/claims.py`) is retired: it re-asserted what the record already held and
    re-ran every gate to certify the lander's consistency with itself. One BLIND INDEPENDENT REVIEW is required before the owner's word ONLY for a release
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
  | 11 SEAM PATTERN | every release: the landing's own record (REPORT.json/FLIGHT.log) + owner word; blind independent review on value-moving releases; register is the single durable list | — |
  | 12 G-Y0 | pooled abs pct gap at the year-0 lens | `max_pct` = 2.0 |
  | *(retired)* G-COHORT | walk-forward book ratio — RETIRED, see the bullet above | *(was `max` 1.3)* |

- **`ship_gates_check.py` and `SHIP_GATES.md` are RETIRED instruments (2026-10-13).** Neither
  was executed by any workflow or landing step after 2026-09-10; their labels (A1–A15, B1–B6,
  C/D) and the v1.21 standing-fails and waivers (A2, A3, A12, A-PAIRS-3, the earned-2-row
  waiver) are history, recorded here once. The measurement standards above stand; the
  instruments that measure them are the landing gates and CI.

## PART 4 — PROCESS LAWS (how work is done; each names the incident that created it)
P1. **THE BOARD MOVES ONLY IN AN ACT THAT SAYS IT WILL.** A process, tooling or
    documentation change leaves every value-bearing artifact byte-identical, and the
    before/after identity check is the standing falsifier, not a courtesy. A value-moving change
    is built on a COPY first and its movers shown to the owner before it lands — the whole of what
    the prereg ceremony (P9, retired 2026-10-13) was for, kept without the ceremony.
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
    board, so the interlock is a lock, not a check.* *Retires when the engine runs from the
    checkout instead of a shared copy (plan 2026-10-13, phase 5); until then it stands.*
P4. **ASSERT THE RELATIONSHIP, NEVER THIS MONTH'S NUMBER.** A gate computes the truth
    from the artifact and asserts the carriers agree with it. A hand-typed identity in a
    check is a red waiting for the next legitimate move. When a ruling retires an assertion, it
    is removed from the instrument that carries it IN THE SAME ACT (P11, folded in 2026-10-13).
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
P7. **RULED-RED IS NOT A SNOOZE BUTTON — RETIRED 2026-10-13.** Governed the ruled-red ledger (`acceptance/ruled_red.json`), retired with it: a ledger whose probes expire on a date is a snooze button with a timer, and it reds CI on schedule rather than on a defect.
P8. **EXPLICIT PATHS ONLY.** Every commit stages named paths. No `git add -A`, no sweep,
    no bare `git commit`.
    *Incident: register v786; the discipline every act since has recorded in its own
    final state.*
P9. **THE PREREG COMES FIRST — RETIRED 2026-10-13.** Folded into P1: the property (predict, measure on a copy, show the movers, then land) stands; the ceremony (a committed prediction document per act) was the largest single source of failed flights and is gone.
P10. **NO SECOND LAWS FILE, EVER.** These laws live here. Any derived view is generated,
    carries a do-not-hand-edit banner, and is CI-linted equal to this document.
    *Incident: `docs/acceptance_v2_0.json` — declared regenerated from this file, read
    and regenerated by no code, and two laws out of step with it for months. Disposed of
    under this amendment: the file is removed, its thresholds folded into PART 3, and
    `tools/rulebook_lint.py` R5/R6 now red on a derived laws view REAPPEARING.*
P11. **THE RETIREMENT IS RECORDED WHERE THE GATE LIVES — RETIRED 2026-10-13.** Folded into P4 as its corollary. The incident it records (A9/B1 re-presented as fresh reds) stands in git history.
P12. **THE PRICED-ARM READING — RETIRED 2026-10-13.** Governed the no-arb reading ceremony for the staircase adoption (`tools/noarb_page.py`), run by nothing since August. A value-moving adoption is covered by P1 as amended.
P13. **A PINNED OWNER-INPUT HAS ONE NAMED WRITER.** The pins of an owner-supplied data
    input (today: the sitter sheet's md5/rows/injured-Y in `data/sheet_pins.json`) are
    written by exactly ONE writer of record — the round lander once P2b lands; in any
    window before a lander owns them, the runbook's manual path is EXPLICITLY the interim
    writer, stated in the runbook itself. A pin moved by any other hand is a halt, not a
    repair.
    *Incident: PACKAGE 3a, 2026-08-21 — the sheet pins left the engine for the data file;
    the writer-of-record rule rode the act as runbook ERRATUM E7 pending this line.*
P14. **A WEEK OF SCORES IS DATA, NOT AN ACT.** Weekly scores go in by one command,
    `tools/ingest scores/<WEEK>.csv`, and nothing else. They need no prereg, no arming word
    beyond the owner sending the file, no predicted movers and no lander self-test. The
    safety is automatic: every name resolves or it halts before touching anything, the edit
    is byte-checked, the landing gates run, and the bounds gate refuses a week that moves the
    players who did not play. When the command stops, its cause is fixed in the tool, not
    worked around by hand. No session adds a step to this path without the owner's signed
    word.
    *Incident: FW1 and FW2, 2026. Both weeks went through the machinery built for engine
    changes. FW2's scores took about 24 hours and a dozen flights, and the owner stopped
    sending scores. Replaying FW2 through `tools/ingest` reproduced the landed board byte for
    byte (store a367386a, board d3fb6b48).*
P15. **OUTCOME BEFORE PROCESS.** When a documented procedure fails twice for the same kind of
    reason, stop: fix the procedure, or ask the owner. Do not make a third attempt. A
    safeguard is kept only while it can name the failure it catches and that failure can
    still happen. Before adding one, state what it will cost the next routine run.
    *Incident: the same weeks — the retries fixed each symptom and never the procedure.*

## SIGNED
Owner word given in chat 2026-07-22; amended 2026-07-28 (v2.1) and 2026-08-20 (v3, "Okay agree to
the laws updated."). The derived twin is retired, not regenerated — this document is the only laws
file. CONSTRAINTS v1.19 + acceptance v1.21 archived.
P12–P13 amendment signed 2026-08-21, owner word verbatim: "Sign the rulebook, that's fine" — given
against the supervisor's described batch (the pin-file interim-writer rule + the per-arm no-arb
reading patch queued at the staircase adoption).
P14–P15 amendment (with the law 10(c) and P9 riders) signed 2026-09-24, owner word verbatim:
"Agree, on the rulebook changes. sign it." — given against the drafted text (the one-command
weekly ingest; outcome before process).
Amendment 2026-10-13 (P7, P9, P11, P12 retired; P1, P3, P4, law 11 and PART 3 amended; the
P14/P15 review's finding that none of the laws, gates or ledgers surfaced six weeks of red CI),
owner word verbatim: "the laws should help, not hurt or cause damage. So i trust your
recommendation." — given against the supervisor's revised D5 list.
