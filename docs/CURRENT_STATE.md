# CURRENT STATE — the incoming-seat read · v50 · supervisor pen · 2026-08-04, register v558

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
(v50 · supervisor pen · 2026-08-04, register v558 · replaced wholesale at the #306 FIRE pen — the year-zero
redesign is FIRED; a fresh cold execution seat opens on the owner's paste)

## THE ERA: THE CONSISTENCY ERA — **#306 IS FIRED** (owner word, #306 comment 5174594459). Main is the v558
pen or a descendant; four gating workflows green at every content state. **#292 DONE AND ON MAIN** (`ab68430`;
awaits the owner's close click). **#290:** L6 exited on an exact period-2 cycle (v556); Path A is the owner's
word; **the year-zero redesign directive #306 is FIRED with its full governing set**: the body + the pre-fire
audit (5174229825, PASS with three conditions) + the owner's ANCHOR STEER (5174404784: *values anchor to
measured pick outcomes; position/age modulate within bounds, never inflate*) + Addendum 1 (5174450071, C1–C2
discharged) + the seam confirmation (5174497326, byte-identical script re-run; ACCEPTANCE 7 adopted —
aggregate-neutral + band bounds, born failing at +8.4%/+64%; C3′ — first fit from ≥2 starting surfaces,
byte-agreement or HALT). The record's LIVE carrier is **`claude/exec-seat-290-handoff-d7bnaa`** at
**`7e9d7f9`** or a descendant (frozen ancestors j0kwl0 `8e8c15b` · fubolo `abf8f4c` · fp78jm `3cccb9d`). The
halt substrate is HELD as captured (`L6_HALT_state.diff` `137c6d2c`, base `3ffbc1f`, applies at tip —
re-verify, never assume). The **EXECUTION word remains WITHHELD**; nothing has landed at any point.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v49 recorded it: N1–N28 stand (N16 superseded in part by N19; R-K = N25 amended by
N27). This cycle:
N29. **THE ANCHOR STEER (owner word, L-A's organizing principle):** year-zero values ANCHOR to the measured
    pick outcomes; position and age MODULATE within bounds — redistribute, never inflate. The pick curve is
    the skeleton the surface cannot leave; "by construction" bars post-hoc clamping. [#306 comment
    5174404784 + Addendum 1 §A; v558]
N30. **ACCEPTANCE 7 (seam word, owner-reversible):** the modulation is AGGREGATE-NEUTRAL against the anchor
    to a stated tolerance and no band exceeds its stated bound; tolerance/bounds fixed at design time, each
    limb fail-capable; born failing on today's artifact (+8.4% aggregate, +64% tail) — its own non-vacuity
    proof. Measurable by the committed `tail_gap_by_band.py`. [#306 comment 5174497326; v558]
N31. **C3′:** the executing seat's read-back names the INSTALLED CURVE it re-enters from and HOLDS; the
    first fit under the new lane runs from ≥2 materially different held starting surfaces with
    BYTE-AGREEMENT REQUIRED — disagreement = L-B failed, HALT. [#306 comment 5174497326; v558]
N32. **THE KEY-TYPE IDENTITY FACT (L5 docket entry 11):** `sort_keys=True` orders string keys lexically and
    int keys numerically — the same ladder hashes `b43a4231` (int-keyed) vs `1a8db02b` (string-keyed); the
    payload-recipe NAMED HELPER remains OWED (E.5 finding 4 has bitten twice). [Addendum 1 §B; v558]
N33. **THE `.srcmd5` LAWFUL ROUTE:** regenerate via `single_source.stamp_tier2_frozen` — a pure function of
    the artifact bytes; NO peak rebuild (a model rebuild on a travelling substrate is a modelling act).
    Expect `d14f0f12` / `aaccad1c`. [Addendum 1 §C; v558]

## THE QUEUE
- **#306 — A FRESH COLD SEAT OPENS on the owner's paste.** Opening order (§10 + Addendum 1 §C/§D + C3′):
  (1) read `docs/CURRENT_STATE.md` IN FULL → **#306 IN FULL including every comment in order** → the L6
  halt evidence on the live carrier (`L6_RI_BOUND_EXHAUSTED.md` + `measurements/`); (2) verify live state
  with its own commands; (3) READ-BACK ON #306 — deciding figures re-run · the C3′ statement (installed
  curve named; ≥2 starting surfaces for the first fit) · its box's compute-path posture — then **HOLD for
  the seam's go via the owner's paste**; (4) on the go: merge the live carrier forward (TRUE MERGE,
  `bf6596b` pattern, merge-base/conflicts/span measured BEFORE the act) → reconstruct (apply `137c6d2c`,
  verify `fb9efdec`/`f305fe53`/`ade79790`, `.srcmd5` per N33, **compute-path assert `92e397bd` — FAIL →
  HALT to the seam**) → the redesign job: **L-A** anchored construction per N29 with N30's acceptance ·
  **L-B** deterministic lane (both-directions non-vacuity: must reproduce today's defect on the old lane) ·
  **L-C** cross-machine byte-assert on OUTPUT BYTES, else UNMEASURED by name → **L6 re-enters under
  R-H/R-I/N19 unchanged** (bound 4 · fixed point = payload md5 equality · exhausted → HALT-and-report) →
  the hand-back states the converged G-Y0 against N16's trigger naming the surface md5 → L7–L8 → the full
  rehearsal hand-back → **the EXECUTION word** → the landing (ships the CONVERGED surface per N19) →
  candidate board → adoption (owner's separate act). Landing-critical facts carry from v49 unchanged.
  Costs: ≈13 min/pass strictly serial · compute-path assert ~2 min · the redesigned fit's cost UNMEASURED,
  prices at rehearsal.
- **#276 clubs tab · #270 referee** (bias-1 refinement N17) — post-adoption · **#139 feeds** · v1.1 read
  outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
Paste the fresh #306 seat's opener (the seam supplies it in-channel) · the **EXECUTION word** (after the
full rehearsal hand-back) · the `rl_replacement_derive.py` search (N23; found → tell the seam) · close
clicks **#292 #283 #275** · branch deletes — **HOLD** g4edkc (until `e339b1e9` reaches main) · 4ql38z
(stop-point artifacts) · fp78jm (`3cccb9d`) · fubolo (`abf8f4c`) · j0kwl0 (`8e8c15b`) · N12 holds until the
landing reaches main · FREE: as at v550.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (binding on successors):** every agent return translated in VERY SIMPLE
  terms, short — what they did, whether it worked, what he must decide (options + recommendation, one line
  each). Relays IN HIS CHANNEL, never a pointer to GitHub. Answer him HERE before filing anywhere.
- The owner's casual questions are load-bearing QC. This era's model moments: his "aren't the bars
  hand-set?" surfaced true REPL provenance · his "can't we just anchor to what picks delivered?" BECAME
  L-A's organizing principle (N29) before any construction was designed — and the drafting seat's
  measurement confirmed it named the defect exactly · the drafting seat corrected the seam's own R-K
  mechanism clause and the seam re-ran rather than defended (N27). REASONING IS NOT EVIDENCE applies to
  the seam first.
- The permanent guards: as v49 · a directive's deciding measurements live in COMMITTED EVIDENCE (the v557
  catch) · the seam confirms evidence by RE-RUNNING THE COMMITTED SCRIPTS in a clean worktree and requiring
  byte-identical outputs (the v558 standard).

## ENVIRONMENT CARRIES — carried from v49 in full (the live capture `137c6d2c` base `3ffbc1f` at tip
`7e9d7f9` · per-pass surfaces/curves committed · reconstruction recipe proven on a second container ·
compute-path assert `92e397bd` · supersedes-twin discipline N26, fired five times in L6 · D.1 erratum ·
frozen fitted set · `84fb0cde` sealed L3–L5 record · strictly serial behind `tools/preboot_assert.sh` ·
venv 5-pin proof · the responsive-suite HAZARD · the payload recipe unwritten-in-code, N32), plus this
cycle's: **`measurements/` is the re-runnable evidence lane** (md5-asserted inputs · HALT-don't-report ·
different-curve control · FIT-population caveat in three places) · **ten sealed captures on the carrier,
none overwritten** · the candidate-starts table for C3′ (halt `ca662051`/`31e7f00b`/8.842% · pass-0
`e69a3f38`/`fb9efdec`/8.084% · L3–L5 record `e69a3f38`/`84fb0cde`/13.919%) · **PEN MECHANICS** unchanged
(stamp near char 88 `· v55X <date> · PEN:` → X+1, date = pen date, SAME LENGTH · insert immediately BEFORE
` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry length · exactly one new `SEAM v55X`
stamp · docs-only diff · Part B wholesale · commit as `supervisor-seat <supervisor@seam.local>` · branch →
PR → rebase-merge → re-verify main by CONTENT).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v558 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 #306 open · #271 #274 closed · no open PRs; four gating workflows
   green (in-flight stated as in-flight); the LIVE carrier `claude/exec-seat-290-handoff-d7bnaa` at
   `7e9d7f9` or a descendant; the FIVE frozen/HOLD branches intact; the halt capture verifies (`137c6d2c`);
   the measurement scripts re-run byte-identical (the v558 standard).
2. The #306 cold seat opens on the owner's paste: audit its read-back — deciding figures re-run · the C3′
   statement · its compute-path posture — give the go via the owner's paste, and hold the job to N29/N30/
   N31 and the directive's acceptance set. After the re-entered L6: check the converged G-Y0 against N16's
   trigger and bring the owner the outcome simply, per his communication word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
