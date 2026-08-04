# CURRENT STATE — the incoming-seat read · v54 · supervisor pen · 2026-08-04, register v562

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

## THE OWNER'S PRODUCT LAWS (2026-08-04, the v562 correction — read these before touching the surface)

> *"The core tenet of this project was to value picks, and recognise that different intersections
> have different effects."*
> *"A key defender at pick 6 may be, and probably should be, worth less than pick 6, but at pick 45,
> maybe it's worth more. It could be by lots, or not by much. It's that simple: we have the data."*

- **LAW (intersections):** the year-zero surface is a TRUE position × age × pick surface — per
  position/age the data draws a line along the pick axis, below the curve where the data says below,
  above where it says above, **crossing freely**. A position dial constant across picks is BARRED.
- **LAW (no hard bands):** no hard banding on any axis, **in the implementation OR in the
  presentation of results**. Every pick its own value; neighbouring picks near-identical; locality
  binds (*"I don't care for pick 20s data in considering pick 1"*). Report per-pick or smooth
  curves, never buckets.
- These were violated once, by a seam-approved design (v561, voided v562). The audit of any surface
  design checks these laws FIRST, and the load-bearing property of any design is stated to the owner
  in one plain sentence before approval is even discussed.

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
| 16 | **A correct audit of the wrong question** | every figure re-runs byte-identical, yet the design contradicts the owner's stated intent — mechanics verified, intent unchecked; the owner had to extract the load-bearing property himself | v562 |

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
(v54 · supervisor pen · 2026-08-04, register v562 · replaced wholesale at the L-A-voiding pen — the flat-lens
approval was a seam audit error, caught by the owner; his laws are recorded; the revision is ordered; the
seam's rotation is RAISED and sits with the owner)

## THE ERA: THE CONSISTENCY ERA — #306 EXECUTING; THE L-A APPROVAL IS VOIDED (v562); THE REVISION IS ORDERED.
Main is the v562 pen or a descendant; four gating workflows green at every content state. **#292 DONE AND ON
MAIN** (`ab68430`; awaits the owner's close click). **#306:** the seat `zlaarm` (branch at `a59db87`)
implemented the FLAT lens `m(pos, age)` and filed acceptance (5176149209); the seam audited it PASS at
5175872733 — **that approval is VOIDED at comment 5176541552**: the flat lens erases the position × age ×
pick intersections that are the project's core tenet (the ruled structure keys the surface
`(gfut, ageR, pick)`, #271 §6), and the audit never stated the flat-dial property to the owner in plain
words. **The owner's two product laws now stand in Part A.** The REVISION ORDER (same comment) reaches the
seat via the owner's paste: build `m(pos, age, pick)` as a smooth bounded field — locality, anchored totals,
thin stretches shrink to 1.0, no cliffs on any axis, per-pick presentation, DESIGN FIRST and HOLD for audit.
The record's LIVE carrier is **`claude/exec-seat-290-handoff-d7bnaa`** at **`7e9d7f9`** (frozen ancestors
j0kwl0 `8e8c15b` · fubolo `abf8f4c` · fp78jm `3cccb9d`). The **EXECUTION word remains WITHHELD**; nothing
has landed at any point.

## WHAT STANDS OF L-A, AND WHAT IS VOIDED
**STANDS (audited, kept):** the skeleton — curve as anchor with totals preserved (a position above the curve
in a stretch is paid for by others in that stretch, never by inflating the class) · bounds m ∈ [0.5, 2.0] ·
the A/B control lane (`RL_V0_ANCHORED`) · the sealed-capture discipline (`LA_anchored_state.diff`
`02e248dc`, base `6736a6f`, BASE annotation per N18) · acceptance measured on the artifact · N35 asserts ·
the pool fence (N37.5). **VOIDED:** the flat lens's cell structure and every claim that it satisfied the
owner's steer. **WITHDRAWN:** the seam's banded ±5% acceptance proposal (violates LAW no-hard-bands); a
band-free drift check is to be designed and audited. Seam verification figures recorded before the voiding
and still true OF THE FLAT DESIGN: acceptance JSON byte-identical re-run; the anchored fit `1a52b787`
reproduced byte-exact on a second host; N35 caught the seam's own container restart mid-audit.

## THE CROSS-HOST FIT TABLE — the v560 finding; A BOX IS CLASSIFIED BY OUTPUT BYTES, NEVER BY LABEL
| container | when | the same fit (`refit_v0surf.py --verify`, pass-0 substrate, curve `e69a3f38`) |
|---|---|---|
| the record's (L6 pass 0) | 2026-07-31 | **`fb9efdec`** ×2 — the committed bytes |
| the `zlaarm` seat's SECOND host | 2026-08-04 | `5939fa35` ×5 — off-class; **PINS NOTHING** |
| the seam's (re-classified after ITS restart) | 2026-08-04 | **`fb9efdec`** ×4 | 
| the `zlaarm` seat's THIRD host | 2026-08-04 | **`fb9efdec`** — N35 assert PASS, fit-class |
N35's assert is the classifier; it re-runs after any observed migration or restart — proven necessary twice
in one day (both the seat's and the seam's containers migrated mid-session).

## THE CAPTURE TABLE — A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | applying it yields `data/v0surf.pkl` | base |
|---|---|---|---|
| `L6_pass0_state.diff` — the N35-assert substrate | `13b71c26` | **`fb9efdec`** (curve `e69a3f38`) | `f0128d6` |
| `LA_anchored_state.diff` — the FLAT-lens state (voided design; capture stays sealed as record) | `02e248dc` | `1a52b787` | `6736a6f` |
| `L6_HALT_state.diff` — the halt state, held | `137c6d2c` | `31e7f00b` (curve `ca662051`) | `3ffbc1f` |
| `L4_state.diff` — sealed L4 exit-record | `2cc5041c` | `84fb0cde` | `f0128d6` era |
(peak `f305fe53` / pvc `ade79790` across all. A REVISED-lens capture is expected after the next design audit.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v53 recorded it: N1–N37 stand, with N36's mapping clause CORRECTED (see N38). This cycle:
N38. **THE VOIDING AND THE OWNER'S LAWS (comment 5176541552):** the v561 L-A approval is VOIDED as a seam
    audit error; N36's "changes no line" clause is corrected — the owner's steer DID demand pick-resolved
    effects. The two OWNER LAWS (intersections · no-hard-bands, now in Part A) bind every future seat and
    every design audit checks them FIRST. The revision order: `m(pos, age, pick)` smooth bounded field,
    locality, anchored totals with stated neutrality weighting, thin-data shrink to 1.0, no cliffs, per-pick
    presentation, design-first-hold-for-audit. The banded ±5% acceptance proposal is WITHDRAWN. The seam's
    rotation was raised on this failure and sits with the owner. [v562]

## THE QUEUE
- **#306 — the seat awaits the REVISION ORDER via the owner's paste** (comment 5176541552), then: design
  `m(pos, age, pick)` per the owner's laws, measured on committed rows, HOLD for seam audit (laws first,
  mechanics second) → implement on approval → acceptance on the artifact with a band-free drift check →
  **L-B** deterministic lane (failing direction discharged by the recorded cross-container pair) → **the
  pool-division measurement** (N37) → **L-C** per the amended benchmark → **L6 re-enters under R-H/R-I/N19
  unchanged** → converged G-Y0 vs N16 naming the surface md5 → L7–L8 → full rehearsal hand-back → **the
  EXECUTION word** → the landing → candidate board → adoption (owner's separate act).
- **#276 clubs tab · #270 referee** (bias-1 refinement N17) — post-adoption · **#139 feeds** · v1.1 read
  outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
**The seam rotation decision** (raised v562; rotation is cheap by construction) · paste the revision order
to the seat · the **EXECUTION word** (after the full rehearsal hand-back) · **the pool LEVEL ruling** (after
the N37 measurement) · close clicks **#292 #283 #275** · the `rl_replacement_derive.py` search (N23) ·
branch deletes — **HOLD** g4edkc · 4ql38z · fp78jm · fubolo · j0kwl0 · N12 holds until the landing reaches
main · pen-token re-issue at the owner's discretion.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** deciding-figure re-run, ruling, or audit — else
  delegate · **M3** context posture at every pen.
- **The owner's communication word (binding):** every agent return in VERY SIMPLE terms — what they did,
  whether it worked, what he must decide. Relays IN HIS CHANNEL. Answer him HERE before filing anywhere.
- **The v562 lesson, paid for in the owner's trust:** an audit that re-runs every figure byte-identical can
  still approve the wrong thing — CHECK THE DESIGN AGAINST THE OWNER'S STATED INTENT FIRST (hazard class
  16), and state the load-bearing property of any design to the owner in ONE PLAIN SENTENCE before
  discussing approval. Never band anything shown to him. When he pushes back, measure, concede what is
  true, and never defend the seam's own work. His casual questions are the project's best QC — four of
  them this cycle became law.
- The era's verification standards: **v558** byte-identical re-runs · **v559** verify the capture pair ·
  **v560** classify boxes by output bytes.

## ENVIRONMENT CARRIES — as v53 in full (measurements/ lane · sealed captures · compute-path assert
`92e397bd` · N26 · frozen fitted set · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin proof ·
N32 · N33 · N35 recipe · envpin proportion facts · **PEN MECHANICS** unchanged: stamp near char 88 `· v56X
<date> · PEN:` → X+1, SAME LENGTH · insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · line count
unchanged · growth == entry length · one new `SEAM v56X` stamp · docs-only diff · Part B wholesale · commit
as `supervisor-seat <supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT ·
reset the pen branch onto origin/main before each pen).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v562 pen or a descendant; the same eleven issues
   open, #271 #274 closed; no open PRs; four gating workflows green; the LIVE carrier at `7e9d7f9`; the
   `zlaarm` branch at `a59db87` or a descendant; the five frozen/HOLD branches intact; the capture table by
   apply-and-hash (minimum: `13b71c26` → `fb9efdec`).
2. **Read the owner's laws in Part A and the v562 correction (5176541552) IN FULL before auditing anything.**
   The next seam act is the audit of the revised `m(pos, age, pick)` design — against the laws first, the
   mechanics second. Classify your own box by N35 before trusting any fit figure. Bring the owner each
   outcome in very simple terms; state every design's load-bearing property in one plain sentence.
3. Read-back to the owner in his channel — short and simple — then hold for confirmation before any push.
