# CURRENT STATE — the incoming-seat read · v49 · supervisor pen · 2026-08-04, register v557

**WHAT THIS IS.** The condensed read for an incoming seat, so orientation costs ~20KB instead of the
register header's ~400KB. It carries *what is true now*, *what the owner actually wants*, and *where
the history lives*.

**WHAT IT IS NOT.** Not the record. `docs/OPEN_ITEMS_REGISTER.md` is the single durable list and
remains append-only and complete. **Where the two disagree, the register wins and this file is
wrong.** This is a derived view, in the same sense the board is derived from the store.

**THE DISCIPLINE THAT KEEPS IT HONEST.** Part B is **REPLACED WHOLESALE every pen, never appended
to**. Part A changes only when a new class is named. A derived copy kept in sync by hand goes stale
silently — that is the `club_valuation.js` fault of 2026-07-27, and this file is the same shape.

**IF THIS FILE AND THE REGISTER DISAGREE, THE REGISTER IS RIGHT.** Read this first, then read the
register only by pointer for the sections your task touches.

---

# PART A — STANDING

## THE GOVERNING TEST — read this before proposing any work

> **Is this a reasonable chance of stopping the project from working?**
> Not: *can this be fixed?*

This is the owner's test, given 2026-07-27, and it overrides every instinct below it. Everything is
imperfect; applying "is this imperfect" means the work never ends. **This is a hobby project.** Most
cars have an oil leak and drive fine.

Three consequences, stated because this project has failed them repeatedly:

1. **If it cannot plausibly stop the thing working, it gets one line in the register and nothing
   else.** No sweep, no cold reviewer, no directive, no norm.
2. **The guards are the maintenance burden.** The proof harnesses take ~86 minutes and are wired to
   nothing. The register grew until it broke the agents that must read it. A hand-typed board id took
   the whole app down. Each was built to prevent imperfection and now costs more than it returns.
   **Before adding a guard, price its upkeep — and deleting one is a legitimate answer.**
3. **Do not fix the symptom of a thing that should not exist.** Club totals were baked into a file
   that goes stale; the fix applied was to regenerate the file, when the right fix was to stop baking
   a sum that a browser computes instantly.

**Owner's own words, 2026-07-27:** *"I'm sick of wasting time on endless over-engineering that
doesn't help serve the project."* · *"We won't get anywhere, because we obsess over small details
that don't help the project."*

**And write plainly.** Not register-dialect, not code names, not "class-(c) defects" and "non-vacuity
proven both directions". A human reads this and should not need a translator.

## The named hazard classes

Found the expensive way. Listed so a seat inherits them in 2KB rather than 300KB. **These are
diagnostic aids, not a mandate to go hunting.**

| # | class | what it looks like | v |
|---|---|---|---|
| 1 | **Right-name-wrong-file** | a *true* hash of the *wrong* artifact | v464 |
| 2 | **Duplicated assertion** | a fix applied to one copy reads as closed and is not | v469 |
| 3 | **Load-bearing invisible character** | a byte that carries meaning, cannot be seen, destroyed by ordinary hygiene | v490 |
| 4 | **False success signal** | a fix whose own report reads clean for the portion it missed | v494 |
| 5 | **Vacuity** | a check that cannot fail: `d41d8cd9` empty-input hashes, `!=` for `==`, a test reading its own expectation | v432 · v463 · v469 · v470 · v471 |
| 6 | **Shallow clone** | ancestry negatives that are container artifacts, not facts | v473 · v487 · v507 |
| 7 | **Two-axis sibling sets** | enumerate what **reads** the changed field *and* what **stamps** the moved identity — the seam repeated this at v522 | v507 · v522 |
| 8 | **Classification-by-symptom is provisional** | a red's class is proven only by attempting the fix | v466 |
| 9 | **First-failures only** | suites halt at the first failure, so a red map is never a completeness claim | v469 |
| 10 | **Same shape is not same cause** | compare maps step-level *and* cause-level | v494 |
| 11 | **A ruling's channel is not its author** | a seam ruling relayed by the owner stays a seam ruling | v495 · v507 |
| 12 | **Every count names its denominator** | *"496 of 2,651 store rows, of which 69 are priced and 38 active"* is the required shape | v501 |
| 13 | **Identity by key, never substring** | a name-fragment match taking `[0]` answers confidently about the wrong object | v505 |
| 14 | **Anchoring sentinels** | a strip rule's off-by-one hashes are invariant under header content | v507 |

## Standing norms

- **Screen by RE-RUNNING, never by reading.** A predecessor's work is hypothesis until reproduced.
- **Verify before recording.** Trace every figure to the artifact it describes before stating it.
- **No predictions of CI maps.**
- **Non-vacuity:** any guard added must be proven able to fail.
- Directives file as GitHub issues at pre-fire-audit time. Cold-review **openers** do not (v507).
- An audited directive is amended by addendum, never edited in place (v461).
- **CI runs and reports. CI never commits.**
- Corridor chat carries **zero authority**.
- Cold seats open bare, outside any project container (v427).
- Scratch is pristine git state **with full history** — `git fetch --unshallow`, never `git archive`
  alone.
- A seat's read is current only to the version it names. Disclose it.
- The seam verifies and rules; it does not do a seat's work, and never reviews what it authored.

## Roles

| | |
|---|---|
| **Owner** | sole owner-word authority: rulebook, stop-points, merges, tags, score-arm |
| **Seam + supervisor pen** | direction, continuity, the register, independent verification. **Docs-only** |
| **Execution supervisors** | direct hands, screen by re-running. Shell = verify/coordinate, **never author product commits** |
| **Hands** | bounded jobs, build-seat authored, read the directive from the filed issue |
| **Cold reviewers** | third seat, bare session, implementer ≠ reviewer ≠ supervisor |

## Housing

Direct push to main is classifier-blocked in cloud housing. Register pens land via the **API carrier
lane**: branch → PR → rebase-merge. The merge under the owner's platform auth is a **housing fact,
not an approval step**. Docs-only pens land **without a per-entry word** (v483, restored by owner
word 2026-07-27), guarded by structural asserts proven pre-commit: line count unchanged, growth equal
to entry length, single stamp, PRIOR chain intact, docs-only diff. **Reversal is self-executing** —
any pen error reaching main restores the per-entry word.

**Ref deletion is proxy-forbidden to seats.** Branch deletes are an owner click. Do not retry it.

---
# PART B — CURRENT STATE
(v49 · supervisor pen · 2026-08-04, register v557 · replaced wholesale at the #306 pre-fire-audit pen — PATH A
is the owner's word; #306 is FILED and AUDITED (pass, three conditions); the FIRE word is the next owner act)

## THE ERA: THE CONSISTENCY ERA — PATH A, REDESIGN-FIRST. Main is the v557 pen or a descendant; four gating
workflows green at every content state. **#292 DONE AND ON MAIN** (`ab68430`; awaits the owner's close click).
**#290:** L6 exited on an exact period-2 cycle (v556); **the owner's sequencing word is PATH A** (#290 comment
5174127049) — N9's G-Y0 limb stands unwaived. **#306 — the year-zero redesign directive — is FILED, NOT
FIRED**, drafted by the d7bnaa seat, **seam pre-fire audited PASS WITH THREE CONDITIONS** (#306 comment
5174229825). The record's LIVE carrier is **`claude/exec-seat-290-handoff-d7bnaa`** at **`ef0d2fb`** or a
descendant (frozen ancestors j0kwl0 `8e8c15b` · fubolo `abf8f4c` · fp78jm `3cccb9d`). The halt substrate is
HELD as captured (`L6_HALT_state.diff` `137c6d2c`, based at tip, 19/19 pre-images verified). **R-K's holding
stands; its mechanism clause is AMENDED by measurement** (seam-re-run exact): the pass-2/pass-4 hysteresis is
60 of 2,646 values, max 0.1 — three orders below the ~2pp cycle swing — so DETERMINISM IS NECESSARY BUT NOT
SUFFICIENT and **the moving limb is the TAIL** (year-zero surface ~64–67% over at picks 46–64, ~3–5% under at
1–10, fit-population figures, corroborated by the V0SURF_DIVERGENCE tail-decile map). The **EXECUTION word
remains WITHHELD**; nothing has landed at any point.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v48 recorded it: N1–N26 stand (N16 superseded in part by N19; R-K = N25). This cycle:
N27. **R-K's MECHANISM CLAUSE AMENDED (D1 supersession at #306 comment 5174229825):** the holding (trigger
    met a fortiori; the redesign fires) STANDS; the clause "path memory is what the deterministic lane
    exists to remove [and would stop the cycle]" is SUPERSEDED — hysteresis measured 60/2,646, max 0.1,
    rel 1.8e-4 (seam re-run exact); the cycle is a property of the ruled composition at ladder resolution;
    determinism is necessary-not-sufficient; the tail is the moving limb. [#306 §2 + audit; v557]
N28. **THE #306 AUDIT CONDITIONS (binding at fire):** C1 — the §2/§3 deciding measurements commit as
    evidence (scripts + outputs) with an addendum pointing at them, plus the owed L5 docket line (the
    payload-recipe convention: `md5(json.dumps(curve, sort_keys=True))[:8]`, string-sorted, `int(round(v))`).
    C2 — the addendum names the LIVE carrier + merge-forward + reconstruction recipe + frozen ancestors.
    C3 — the executing seat's read-back states the exact L6 re-entry state (installed curve + starting
    surface) and HOLDS for the seam before any pass. [#306 comment 5174229825; v557]

## THE QUEUE
- **#306 — the d7bnaa seat satisfies C1–C2** (evidence commit + addendum) → the seam confirms → **the
  owner's FIRE word on #306** → a fresh cold seat opens under #306 §10 + C3 (read-back on-issue · HOLD for
  the seam's go · merge the live carrier forward, `bf6596b` pattern · reconstruct per the recipe below ·
  compute-path assert `92e397bd` gates any refit box) → the redesign job (L-A tail by construction · L-B
  deterministic lane, both-directions non-vacuity · L-C cross-machine byte-assert on OUTPUT BYTES, else
  UNMEASURED by name) → **L6 re-enters under R-H/R-I/N19 unchanged** (bound 4; fixed point = payload md5
  equality; exhausted → HALT-and-report) → the L6 hand-back states the converged G-Y0 against N16's trigger
  naming the surface md5 → L7–L8 → the full rehearsal hand-back → **the EXECUTION word** → the landing
  (ships the CONVERGED surface per N19) → candidate board → adoption (owner's separate act). Landing-critical
  facts carry from v48 unchanged (C.1 identity set · T1 rides · eighth γ site · `ruled_curve_final_279` at
  L1(b) · N23's verify_anchors remedy · R-D's 65-mover attribution · strictly serial behind
  `tools/preboot_assert.sh`). Costs: ≈13 min/pass strictly serial (four-pass bound ≈51 min) · compute-path
  assert ~2 min · the redesigned fit's own cost UNMEASURED, prices at rehearsal.
- **#276 clubs tab · #270 referee** (bias-1 refinement N17) — post-adoption · **#139 feeds** · v1.1 read
  outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
Paste the seam's relay to the d7bnaa seat (C1–C2 addendum work) · **the FIRE word on #306** (after the seam
confirms the conditions) · the `rl_replacement_derive.py` search (N23; found → tell the seam) · the
**EXECUTION word** (after the full rehearsal hand-back) · close clicks **#292 #283 #275** · branch deletes —
**HOLD** g4edkc (until `e339b1e9` reaches main) · 4ql38z (stop-point artifacts) · fp78jm (`3cccb9d`) ·
fubolo (`abf8f4c`) · j0kwl0 (`8e8c15b`) · N12 holds until the landing reaches main · FREE: as at v550.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (binding on successors):** every agent return translated in VERY SIMPLE
  terms, short — what they did, whether it worked, what he must decide (options + recommendation, one line
  each). Relays IN HIS CHANNEL, never a pointer to GitHub. Answer him HERE before filing anywhere.
- The owner's casual questions are load-bearing QC (standing catches as v48). This cycle's model moment: the
  DRAFTING SEAT corrected the SEAM's own ruling clause with a measurement, and the seam re-ran it rather
  than defending the prose — a seat that measures against the seam's reasoning is doing its job; REASONING
  IS NOT EVIDENCE applies to the seam first.
- The permanent guards: as v48 · never pick a limb of a cycle the maths rejects · never re-spec 'settled' ·
  a directive's deciding measurements live in COMMITTED EVIDENCE, never in issue prose alone (the v557
  audit's catch, charter D2).

## ENVIRONMENT CARRIES — carried from v48 in full (the live capture `137c6d2c` at tip `ef0d2fb` · per-pass
surfaces/curves all committed bytes · the reconstruction recipe proven on a second container · compute-path
assert `92e397bd` gates any refit box · supersedes-twin discipline N26 — note it fired FIVE times in L6,
four in `ui/release_pick_curve.json` and once in `pvc_curve_v2.json` where `3068.4647` occurs as a field AND
inside that field's prose · D.1 erratum · REPINNED harness per-pass re-pins · frozen fitted set · `84fb0cde`
sealed L3–L5 record · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin proof · the
responsive-suite HAZARD), plus this cycle's: **the payload recipe is written down NOWHERE IN CODE**
(`md5(json.dumps(curve, sort_keys=True))[:8]`, string-sorted keys, default separators, `int(round(v))`; an
int-keyed ladder hashes to `b43a4231` — the docket line files with C1) · the committed pass matrices
`pass0–4_matrix.json` + identities are the re-runnable inputs for the §2/§3 measurements · **PEN MECHANICS**
unchanged (stamp near char 88 `· v55X <date> · PEN:` → X+1, date updates to the pen date, SAME LENGTH ·
insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry length ·
exactly one new `SEAM v55X` stamp · docs-only diff · Part B wholesale · commit as `supervisor-seat
<supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v557 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 **#306** open · #271 #274 closed · no open PRs; four gating workflows
   green (in-flight stated as in-flight); the LIVE carrier `claude/exec-seat-290-handoff-d7bnaa` at
   `ef0d2fb` or a descendant; the FIVE frozen/HOLD branches intact; the halt capture verifies (`137c6d2c`).
2. The era turns on #306: confirm C1–C2 landed (evidence commit + addendum, seam-verified by re-run of at
   least the §2 headline) → the owner's FIRE word → audit the cold seat's read-back including C3 (the exact
   re-entry state) → hold the loop to R-H/R-I/N19 · after the re-entered L6: check the converged G-Y0
   against N16's trigger and bring the owner the outcome simply, per his communication word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
