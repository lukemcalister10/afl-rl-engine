# CURRENT STATE — the incoming-seat read · v51 · supervisor pen · 2026-08-04, register v559

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
(v51 · supervisor pen · 2026-08-04, register v559 · replaced wholesale at the #306-go + SEAM-ROTATION pen —
this Part B is the seam handover artifact; the sitting seam raised its own rotation at ~430k, charter C3/M3)

## THE ERA: THE CONSISTENCY ERA — #306 IS FIRED AND ITS COLD SEAT HAS THE GO. Main is the v559 pen or a
descendant; four gating workflows green at every content state. **#292 DONE AND ON MAIN** (`ab68430`; awaits
the owner's close click). **#290:** L6 exited on an exact period-2 cycle (v556); Path A; **#306 (the
year-zero redesign) is FIRED** with governing set: body + audit 5174229825 + the owner's ANCHOR STEER
5174404784 (N29) + Addendum 1 5174450071 + confirmation 5174497326 (Acceptance 7 = N30 · C3′ = N31) + FIRE
word 5174594459 + **the read-back audit, v50-correction, re-entry ruling and GO 5174786873**. The #306
execution seat's read-back PASSED (its branch at `f169204` or a descendant); it CAUGHT a stale-recipe defect
in v50 (seam-confirmed; corrected below). The record's LIVE carrier is **`claude/exec-seat-290-handoff-
d7bnaa`** at **`7e9d7f9`** (frozen ancestors j0kwl0 `8e8c15b` · fubolo `abf8f4c` · fp78jm `3cccb9d`); the
#306 seat's own branch carries its work and merges the carrier forward on the go. The **EXECUTION word
remains WITHHELD**; nothing has landed at any point.

## THE CAPTURE-TRIO TABLE — the v559 correction; A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | applying it yields `data/v0surf.pkl` | peak / pvc |
|---|---|---|---|
| `L6_pass0_state.diff` — **THE RULED RE-ENTRY STATE** | `13b71c26` | **`fb9efdec`** (installed curve `e69a3f38`) | `f305fe53` / `ade79790` |
| `L6_HALT_state.diff` — the halt state, held | `137c6d2c` | **`31e7f00b`** (installed curve `ca662051`) | `f305fe53` / `ade79790` |
| `L4_state.diff` — sealed L4 exit-record | `2cc5041c` | `84fb0cde` | `f305fe53` / `ade79790` |
(v50's reconstruction line paired the halt capture with `fb9efdec` — WRONG, caught by the #306 seat's
measurement, seam-confirmed by apply-and-hash of both captures. Verify the PAIR, never the prose.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v50 recorded it: N1–N33 stand. This cycle:
N34. **RE-ENTRY = OPTION A, OPERATIONALIZED (seam word, owner-reversible):** L6 re-enters from the PASS-0
    STATE — apply `13b71c26`; installed curve `e69a3f38` (the ruled curve of record, N6; the only candidate
    not produced by the defective loop); no install act. C3′ satisfied from committed bytes: the first fit
    runs from BOTH `fb9efdec` AND `31e7f00b`, byte-agreement required, disagreement = L-B failed → HALT
    (`84fb0cde` optional third). [#306 comment 5174786873; v559]

## THE QUEUE
- **#306 — the cold seat EXECUTES on the go** (given, comment 5174786873): (1) merge the live carrier
  forward (TRUE MERGE, `bf6596b` pattern, merge-base/conflicts/span measured before the act) → (2)
  reconstruct per N34 — apply `13b71c26`, verify `fb9efdec`/`f305fe53`/`ade79790` byte-exact, `.srcmd5`
  per N33, **COMPUTE-PATH ASSERT `92e397bd` — FAIL → HALT to the seam** → (3) the redesign legs: **L-A**
  anchored construction per N29 with N30's acceptance (aggregate-neutral + band bounds, born failing at
  +8.4%/+64%) · **L-B** deterministic lane (both-directions non-vacuity — must reproduce today's defect on
  the old lane) · **L-C** cross-machine byte-assert on OUTPUT BYTES, else UNMEASURED by name → (4) **L6
  re-enters under R-H/R-I/N19 unchanged** (bound 4 · fixed point = payload md5 equality · exhausted →
  HALT-and-report) → the hand-back states the converged G-Y0 against N16's trigger naming the surface md5 →
  L7–L8 → the full rehearsal hand-back → **the EXECUTION word** → the landing (ships the CONVERGED surface
  per N19) → candidate board → adoption (owner's separate act). Landing-critical facts carry from v50
  unchanged. Costs: ≈13 min/pass strictly serial · compute-path assert ~2 min · the redesigned fit's cost
  UNMEASURED, prices at rehearsal.
- **#276 clubs tab · #270 referee** (bias-1 refinement N17) — post-adoption · **#139 feeds** · v1.1 read
  outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
Re-provide the pen token to the INCOMING SEAM (rotation raised this pen) · the **EXECUTION word** (after
the full rehearsal hand-back) · the `rl_replacement_derive.py` search (N23; found → tell the seam) · close
clicks **#292 #283 #275** · branch deletes — **HOLD** g4edkc (until `e339b1e9` reaches main) · 4ql38z
(stop-point artifacts) · fp78jm (`3cccb9d`) · fubolo (`abf8f4c`) · j0kwl0 (`8e8c15b`) · N12 holds until the
landing reaches main · FREE: as at v550.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (binding on successors):** every agent return translated in VERY SIMPLE
  terms, short — what they did, whether it worked, what he must decide (options + recommendation, one line
  each). Relays IN HIS CHANNEL, never a pointer to GitHub. Answer him HERE before filing anywhere.
- The owner's casual questions are load-bearing QC (standing catches as v50 — his anchor question BECAME
  N29). The era's verification standards, both proven in anger: **the v558 standard** — confirm committed
  measurements by re-running the scripts in a clean worktree, byte-identical required; **the v559 lesson**
  — a recipe is current only to the capture it names; verify the PAIR by apply-and-hash, never the prose.
  Seats correcting the seam's own documents by measurement is the system working; the seam re-runs, never
  defends.
- The permanent guards: as v50, unchanged.

## ENVIRONMENT CARRIES — carried from v50 in full (measurements/ evidence lane · ten sealed captures ·
compute-path assert `92e397bd` · supersedes-twin discipline N26 · D.1 erratum · frozen fitted set ·
`84fb0cde` sealed L3–L5 record · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin proof · the
responsive-suite HAZARD · payload recipe unwritten-in-code N32 · `.srcmd5` route N33), plus this cycle's:
**THE CAPTURE-TRIO TABLE above is the reconstruction authority** (v50's single-line recipe is retired) ·
the C3′ double-start surfaces are committed bytes (`fb9efdec` = pass-0 · `31e7f00b` = halt) · **PEN
MECHANICS** unchanged (stamp near char 88 `· v55X <date> · PEN:` → X+1, date = pen date, SAME LENGTH ·
insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry length ·
exactly one new `SEAM v55X` stamp · docs-only diff · Part B wholesale · commit as `supervisor-seat
<supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v559 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 #306 open · #271 #274 closed · no open PRs; four gating workflows
   green (in-flight stated as in-flight); the LIVE carrier `claude/exec-seat-290-handoff-d7bnaa` at
   `7e9d7f9`; the #306 seat's branch at `f169204` or a descendant; the FIVE frozen/HOLD branches intact;
   **the capture-trio table verifies by apply-and-hash** (at minimum: apply `13b71c26` → `fb9efdec`).
2. The #306 seat is executing on the go (comment 5174786873): audit each leg's filing by re-running its
   deciding figures (M2; the v558 standard for committed measurements). The next seam decisions arrive at:
   the L-A construction design (audit against N29/N30) · the L-B/L-C acceptance runs · the re-entered L6's
   converged G-Y0 against N16's trigger — bring the owner each outcome simply, per his communication word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
