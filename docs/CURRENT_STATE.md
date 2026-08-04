# CURRENT STATE — the incoming-seat read · v48 · supervisor pen · 2026-07-31, register v556

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
(v48 · supervisor pen · 2026-07-31, register v556 · replaced wholesale at the L6-exit pen — THE LOOP HAS NO
FIXED POINT; N16'S TRIGGER FIRED (R-K); the YEAR-ZERO REDESIGN is live; SEQUENCING sits with the owner)

## THE ERA: THE CONSISTENCY ERA — L6 EXITED WITHOUT A FIXED POINT; THE YEAR-ZERO REDESIGN FIRES. Main is the
v556 pen or a descendant; four gating workflows green at every content state. **#292 DONE AND ON MAIN**
(`ab68430`; awaits the owner's close click). **#290:** the record's LIVE carrier is the execution seat's
branch **`claude/exec-seat-290-handoff-d7bnaa`** at **`ef0d2fb`** or a descendant (j0kwl0 frozen ancestor
`8e8c15b` · fubolo `abf8f4c` · fp78jm `3cccb9d`). The R-H lane OPENED on the seat's box (compute-path assert
`92e397bd` byte-exact); PASS1_INSTALL_SET executed atomically under the supersedes-twin discipline; **the
loop ran to the R-I bound of 4 and EXITED ON AN EXACT PERIOD-2 CYCLE** — curves `ca662051` ↔ `b0bda532`
byte-identical on recurrence (64/64, max diff 0), G-Y0 oscillating 8.842% / 11.028%, best stationary
waypoint 8.084% on `fb9efdec` at pass 0. **THE CAUSE IS MEASURED: the surface refit carries PATH MEMORY**
(same curve + same frozen stack → different surface bytes, `864c11b9` ≠ `31e7f00b`). **R-K: N16's trigger
fired a fortiori — no converged G-Y0 can exist under the current design, and everything measured is 4–5×
over the 2.000% law.** POOL held ≈233 (n=1,005) across all five measurements. The **EXECUTION word remains
WITHHELD**; nothing has landed at any point.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v47 recorded it: N1–N18 stand (N16 superseded in part by N19); N19–N24 stand. This
cycle adds:
N25. **R-K — N16'S TRIGGER FIRED A FORTIORI (seam, owner-reversible):** the R-I bound exhausted on an exact
    period-2 cycle; the surface refit carries measured PATH MEMORY; no converged G-Y0 can exist under the
    current year-zero design and every measured point is 4–5× over the 2.000% law. THE YEAR-ZERO REDESIGN
    FIRES as the ruled remedy. Spec (N16 + this exit): constrained tail · DETERMINISTIC FIT LANE that
    removes path memory (acceptance includes same-curve double-fit → byte-identical surface from ANY
    starting state) · cross-machine byte-assert. Process: the d7bnaa seat drafts the directive as a GitHub
    issue → the seam pre-fire audits (taint respected) → FIRES ONLY ON THE OWNER'S WORD.
    [#290 comments 5173782339 + 5174014160; v556]
N26. **THE SUPERSEDES-TWIN DISCIPLINE (binding):** any install file where a sealed twin shares a token with
    a live pin is edited by JSON path with `/supersedes/*` (and any sealed block) asserted byte-unchanged
    BEFORE and AFTER. Confirmed live in `ui/release_pick_curve.json` (twins `1554b98e`/`f14a6622`/
    `968de0c7`). [#290 comments 5173197747 + 5173233711; v556]

## THE QUEUE
- **#290 — SEQUENCING SITS WITH THE OWNER** [presented at #290 comment 5174014160]:
  **Path A (seam-recommended): redesign-first** — the d7bnaa seat DRAFTS the year-zero redesign directive
  (from N16's spec + the halt evidence), files it as a GitHub issue, the seam pre-fire audits, the owner
  fires; L6 re-enters under the deterministic lane; the trigger's number becomes real; L7–L8 + the landing
  follow with the converged surface per N19. **Path B: land-with-exception** — L7–L8 proceed on the pass-0
  substrate (`e69a3f38` + `fb9efdec`, 8.084%); the 2.000% bar stays a dated exception as the shipped board
  carries today; the redesign lands in the referee era; **this WAIVES N9's G-Y0 limb — an owner word**.
  Either path: the substrate is HELD as captured (`L6_HALT_state.diff` `137c6d2c`, based at tip `ef0d2fb`,
  19/19 pre-images verified); its disposition follows the sequencing word. Landing-critical facts carry
  from v47 unchanged (C.1 identity set · the landing ships the CONVERGED surface per N19 — under Path B
  this line itself needs a seam amendment · T1 rides the landing · eighth γ site · `ruled_curve_final_279`
  at L1(b) · N23's verify_anchors remedy · R-D's 65-mover attribution · strictly serial behind
  `tools/preboot_assert.sh`).
- **#276 clubs tab · #270 referee** (bias-1 refinement N17; under Path B also the redesign's home) —
  post-adoption · **#139 feeds** · v1.1 read outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
**THE SEQUENCING WORD (Path A or B — the single decision in front of the owner)** · then paste the seam's
ruling relay to the d7bnaa seat (drafting begins) · the `rl_replacement_derive.py` search (N23; found →
tell the seam) · the **EXECUTION word** (after the full rehearsal hand-back, whichever path) · close clicks
**#292 #283 #275** · branch deletes — **HOLD** g4edkc (until `e339b1e9` reaches main) · 4ql38z (sole
carrier of the stop-point artifacts) · fp78jm (`3cccb9d`) · fubolo (`abf8f4c`) · **j0kwl0 (`8e8c15b`,
frozen ancestor of the live carrier)** · N12 holds until the landing reaches main · FREE: as at v550.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (binding on successors):** every agent return translated in VERY SIMPLE
  terms, short — what they did, whether it worked, what he must decide (options + recommendation, one line
  each). Relays IN HIS CHANNEL, never a pointer to GitHub. Answer him HERE before filing anywhere.
- The owner's casual questions are load-bearing QC (standing catches as v47; his "aren't the bars hand-set?"
  surfaced the true REPL provenance — answer from the record, never memory).
- The permanent guards: as v47, plus this exit's pair now proven in anger: **never pick a limb of a cycle
  the maths rejects · never re-spec 'settled' to make a loop pass.**

## ENVIRONMENT CARRIES — carried from v47 in full, plus this cycle's: **THE LIVE CAPTURE is
`L6_HALT_state.diff` `137c6d2c` based AT the tip `ef0d2fb`** (19/19 pre-images verified; applies directly —
no ancestor checkout needed); sealed exit-records: `L6_pass0_state.diff` `13b71c26` · `L4_state.diff`
`2cc5041c` · the N18 pair · **the per-pass surfaces/curves are ALL committed bytes** (pass table: `fb9efdec`
→ `aaf45964` → `864c11b9` → `2d7dab64` → `31e7f00b`; curves `1a8db02b` → `ca662051` → `b0bda532` →
`ca662051` → `b0bda532`) · the reconstruction recipe (v47 queue step 3) is PROVEN on a second container —
capture-apply reproduced `13b71c26` byte-identically · the compute-path assert (`92e397bd`) is the gate on
any refit box; the d7bnaa box PASSED it · the supersedes-twin discipline (N26) · the D.1 erratum (1892 is
the CONVERGED curve's position 5; the stop-point's is 1931) — runbook amends by addendum · the REPINNED
harness re-pins per pass, lawful instrument maintenance · prior carries all still live (frozen fitted set ·
`84fb0cde` sealed L3–L5 record · panel lane · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin
proof · the responsive-suite HAZARD · **PEN MECHANICS** unchanged: stamp near char 88 `· v55X 2026-07-31 ·
PEN:` → X+1 · insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · prove line count unchanged · growth
== entry length · exactly one new `SEAM v55X` stamp · docs-only diff · Part B wholesale · commit as
`supervisor-seat <supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v556 pen or a descendant; the same issue/PR/
   workflow set as v47 (a run in flight is stated as in flight); the #290 LIVE carrier
   `claude/exec-seat-290-handoff-d7bnaa` at `ef0d2fb` or a descendant; the FIVE frozen/HOLD branches
   intact; the halt capture verifies (`137c6d2c`).
2. The era turns on the owner's SEQUENCING word (Path A/B, #290 comment 5174014160). Path A: audit the
   d7bnaa seat's redesign directive PRE-FIRE (you did not author it — taint clean); hold it to N25's spec
   including the path-memory acceptance test. Path B: amend N19's landing clause by seam word first.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
