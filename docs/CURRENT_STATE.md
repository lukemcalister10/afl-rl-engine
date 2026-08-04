# CURRENT STATE — the incoming-seat read · v52 · supervisor pen · 2026-08-04, register v560

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
| 15 | **A label is not a compute path** | identical CPU string + byte-identical pins, divergent fitted bytes; a box is classified only by reproducing output bytes | v560 |

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
(v52 · supervisor pen · 2026-08-04, register v560 · replaced wholesale at the act-3-halt-audit + N35 pen —
the #306 seat resumes under the fit-path assert; the pen ran on the owner's direct word "A", 2026-08-04)

## THE ERA: THE CONSISTENCY ERA — #306 EXECUTING; THE ACT-3 HALT IS AUDITED AND RESOLVED; THE SEAT RESUMES
UNDER N35. Main is the v560 pen or a descendant; four gating workflows green at every content state. **#292
DONE AND ON MAIN** (`ab68430`; awaits the owner's close click). **#306 governing set** as v51 recorded, PLUS
the act-3 halt filing 5174986197 and the seam's halt audit + N35 + resume order **5175271118**. The seat
`zlaarm` (branch `claude/exec-seat-306-afl-rl-zlaarm`, halt tip `79898f6`): acts (1)(2) PASS — true merge
measured · reconstruction byte-exact per the capture-trio table · compute-path assert `92e397bd` PASS — act
(3) HALTED on the cross-host fit divergence, audited, **RESUMED**. The record's LIVE carrier is
**`claude/exec-seat-290-handoff-d7bnaa`** at **`7e9d7f9`** (frozen ancestors j0kwl0 `8e8c15b` · fubolo
`abf8f4c` · fp78jm `3cccb9d`). The **EXECUTION word remains WITHHELD**; nothing has landed at any point.

## THE CROSS-HOST FIT TABLE — the v560 finding; A BOX IS CLASSIFIED BY OUTPUT BYTES, NEVER BY LABEL
| container | when | the same fit (`refit_v0surf.py --verify`, pass-0 substrate, curve `e69a3f38`) |
|---|---|---|
| the record's (L6 pass 0) | 2026-07-31 | **`fb9efdec`** ×2 — the committed bytes |
| the `zlaarm` seat's | 2026-08-04 | `5939fa35` ×5 — start/thread-invariant; **PINS NOTHING** |
| the seam's | 2026-08-04 | **`fb9efdec`** ×3 — start-invariant, incl. the record's exact fit shape |
Identical declared pins on all three (5-pin venv · OpenBLAS `05c9f9eb` · Guard 5); the two 2026-08-04
containers report the SAME CPU string (Xeon @2.80GHz, family 6 model 85 stepping 7). Every pin passes and
the fitted bytes still differ: the pin was never the guard, and neither is the label (hazard class 15).
Proportion (envpin study, `session_2026-07-19/envpin/out/`): the worst per-chip effect on record is ±95
VALUE units on ~7,964 (~1.2%, item 380); the board md5 flips at ~3e-7 injected noise while 1e-6 moves one
player +1 unit, top-6 order unchanged. Byte-identity is a tripwire; the stake is comparability, not value.

## THE CAPTURE-TRIO TABLE — carried from v51 UNCHANGED; A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | applying it yields `data/v0surf.pkl` | peak / pvc |
|---|---|---|---|
| `L6_pass0_state.diff` — **THE RULED RE-ENTRY STATE** | `13b71c26` | **`fb9efdec`** (installed curve `e69a3f38`) | `f305fe53` / `ade79790` |
| `L6_HALT_state.diff` — the halt state, held | `137c6d2c` | **`31e7f00b`** (installed curve `ca662051`) | `f305fe53` / `ade79790` |
| `L4_state.diff` — sealed L4 exit-record | `2cc5041c` | `84fb0cde` | `f305fe53` / `ade79790` |
(Re-verified by this seam's apply-and-hash of both live rows at onboarding. Verify the PAIR, never the prose.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v51 recorded it: N1–N34 stand. This cycle:
N35. **THE FIT-PATH ASSERT (seam word, owner-reversible):** before ANY measurement act of the #306 job (fit,
    acceptance run, loop pass), the box must reproduce the record's fit — `refit_v0surf.py --verify` on the
    reconstructed pass-0 substrate → **`fb9efdec` FULL md5** (N22; ~52s, behind the preboot/serial
    discipline). FAIL → no measurement act on that box; restart and re-assert. The assert goes STALE on any
    observed host migration or restart. The compute-path assert `92e397bd` is measured NECESSARY BUT NOT
    SUFFICIENT. Riders: L-B Acceptance 1's failing direction DISCHARGED by the recorded cross-container pair
    (`5939fa35` ×5 vs `fb9efdec` ×3, both filed 2026-08-04); the `ca662051` pair re-run NOT ordered;
    `5939fa35` pins nothing; C3′ unchanged for the new lane; L-C's benchmark = byte-identical output
    spanning the measured divide, else UNMEASURED by name. [#306 comment 5175271118; v560]

## THE QUEUE
- **#306 — the seat RESUMES act (3)** (halt 5174986197 · audit/resume 5175271118): **N35's fit-path assert
  first** (restart the container if it still reads off-class) → **L-A** anchored construction per N29 with
  N30's acceptance (aggregate-neutral + band bounds, born failing at +8.4%/+64%) → **L-B** deterministic
  lane (the failing direction is DISCHARGED; the passing direction — byte-identical across hosts — is the
  lane's to earn) → **L-C** cross-host byte-assert per the amended benchmark → **L6 re-enters under
  R-H/R-I/N19 unchanged** (bound 4 · fixed point = payload md5 equality · exhausted → HALT-and-report) →
  the hand-back states the converged G-Y0 against N16's trigger naming the surface md5 → L7–L8 → the full
  rehearsal hand-back → **the EXECUTION word** → the landing (ships the CONVERGED surface per N19) →
  candidate board → adoption (owner's separate act). Next seam decisions: the L-A construction design audit
  (N29/N30) · the L-B/L-C acceptance runs · the converged G-Y0 against N16. Costs: ≈13 min/pass strictly
  serial · compute-path assert ~2 min · fit-path assert ~52s · the redesigned fit's cost UNMEASURED.
- **#276 clubs tab · #270 referee** (bias-1 refinement N17) — post-adoption · **#139 feeds** · v1.1 read
  outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
The **EXECUTION word** (after the full rehearsal hand-back) · close clicks **#292 #283 #275** · the
`rl_replacement_derive.py` search (N23; found → tell the seam) · branch deletes — **HOLD** g4edkc (until
`e339b1e9` reaches main) · 4ql38z · fp78jm (`3cccb9d`) · fubolo (`abf8f4c`) · j0kwl0 (`8e8c15b`) · N12
holds until the landing reaches main · pen-token re-issue at the owner's discretion (the v560 pen ran on
his direct word).

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (binding on successors):** every agent return translated in VERY SIMPLE
  terms, short — what they did, whether it worked, what he must decide (options + recommendation, one line
  each). Relays IN HIS CHANNEL, never a pointer to GitHub. Answer him HERE before filing anywhere.
- The era's verification standards, all proven in anger: **v558** — confirm committed measurements by
  re-running the scripts in a clean worktree, byte-identical required · **v559** — a recipe is current only
  to the capture it names; verify the PAIR by apply-and-hash · **v560** — a box is classified by OUTPUT
  BYTES, never by CPU string or pin; N35's assert is the instrument. Quote the record, never memory: the
  seam mis-said "ranks" for item 380's ±95 VALUE units in the owner's channel and corrected itself on the
  record — the owner's casual questions remain load-bearing QC.
- The permanent guards: as v51, unchanged.

## ENVIRONMENT CARRIES — carried from v51 in full (measurements/ evidence lane · ten sealed captures ·
compute-path assert `92e397bd` · supersedes-twin discipline N26 · D.1 erratum · frozen fitted set ·
`84fb0cde` sealed L3–L5 record · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin proof · the
responsive-suite HAZARD · payload recipe unwritten-in-code N32 · `.srcmd5` route N33 · the capture-trio
table as reconstruction authority · the C3′ committed-bytes surfaces `fb9efdec`/`31e7f00b` · **PEN
MECHANICS** unchanged: stamp near char 88 `· v56X <date> · PEN:` → X+1, SAME LENGTH · insert immediately
BEFORE ` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry length · exactly one new
`SEAM v56X` stamp · docs-only diff · Part B wholesale · commit as `supervisor-seat
<supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT), plus this cycle's:
**the N35 fit-path-assert recipe** (clean worktree at `f0128d6` + apply `13b71c26` → verify `fb9efdec` on
disk → `bash bootstrap.sh` under `RL_VENV` → from the workspace rl_after, `RL_V0SURF_REFIT=1
refit_v0surf.py --verify` with `RL_REPO`+`PYTHONPATH` per the bootstrap's printed ENV → `fb9efdec` full
md5) · the cross-host fit table above · the envpin proportion facts.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v560 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 #306 open · #271 #274 closed · no open PRs; four gating workflows
   green (in-flight stated as in-flight); the LIVE carrier `claude/exec-seat-290-handoff-d7bnaa` at
   `7e9d7f9`; the `zlaarm` branch at `79898f6` or a descendant (resume commits expected); the FIVE
   frozen/HOLD branches intact; **the capture-trio table verifies by apply-and-hash** (at minimum: apply
   `13b71c26` → `fb9efdec`).
2. The #306 seat executes on the resume order (5175271118): audit each leg's filing by re-running its
   deciding figures (M2; the v558 standard) — and CLASSIFY YOUR OWN BOX by N35's fit-path assert before
   trusting any fit figure you re-run there. The next seam decisions arrive at: the L-A construction design
   (audit against N29/N30) · the L-B/L-C acceptance runs · the re-entered L6's converged G-Y0 against N16's
   trigger — bring the owner each outcome simply, per his communication word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
