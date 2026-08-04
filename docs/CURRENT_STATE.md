# CURRENT STATE — the incoming-seat read · v58 · supervisor pen · 2026-08-04, register v566

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
(v58 · supervisor pen · 2026-08-04, register v566 · replaced wholesale at the L-A ACCEPTANCE PEN — the
lens is implemented and ACCEPTED on the artifact under the N41 ruling; the pathway taxonomy is corrected;
the owner's pool rulings N42 are sealed and the pooled-completion re-run is ordered; L-B is open)

## THE ERA: THE CONSISTENCY ERA — #306 EXECUTING; L-A ACCEPTED; L-B OPEN; THE POOL RE-RUN ORDERED.
Main is the v566 pen or a descendant; four gating workflows green at every content state. **L-A:** the
sibling-basis lens is implemented (basis-as-inputs verified: `RL_LENS_BASIS`, HALT-no-fallback, basis
artifact `25a72f85` from the unmodified #279 machinery) and **ACCEPTED on the artifact** after the N41
acceptance-population addendum: worst per-pick deviation 1e-4, 0/64 picks out, 0 position lines out of
[0.5, 2.0]; the born-failing A/B control unchanged. Audits: 5178998844 (implementation, PASS with
corrections) · 5179480421 (addendum, PASS). The seat's honest correction episode (a checkout destroyed
uncommitted fixes; a capture self-captured an evidence file) is recorded; standing rule: **evidence
committed before any substrate operation.** The **EXECUTION word remains WITHHELD**; the bake is HELD
(`expected_boot.json` still pins the pass-0 engine `3c7b0c3c` — the re-pin IS the bake act; Guard 5 halts
on the mismatch by design); nothing has landed at any point. The record's LIVE carrier is
**`claude/exec-seat-290-handoff-d7bnaa`** at **`7e9d7f9`**; the #306 seat branch is
**`claude/exec-seat-306-afl-rl-zlaarm`** at **`f3958c3`** or a descendant.

## THE TWO-CURVE IDENTITY CENSUS — unchanged (full glossary: the PRIMER §5, now incl. the pathway tags)
| curve | payload | what it is | where it lives |
|---|---|---|---|
| the SHIPPED curve | `08ea9375` | #271 stage-B ladder (measured 0.0248% reality) | main's product files — replaced at the landing |
| **the RULED curve — THE ANCHOR** | **`e69a3f38`** | #279 structural ladder: classes 2004–2022, pick64=221, NO pick 65, completion +4.7–8.4% optimistic REPORTED | the rehearsal substrate; ships with the EXECUTION word |
**Pathway tags (owner-corrected v566): PD\* = POST-DRAFT — PDA academy · PDN next-gen · PDS scholarship;
UNR = post-draft UNREGISTERED (a real pathway, not missing data); IRE = post-draft Ireland.**

## THE CAPTURE TABLE — A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | what it is | base |
|---|---|---|---|
| `LA_applied_neutrality_state.diff` — **THE LIVE SUBSTRATE** | `59ef1940` | pass-0 + lens + N41 applied-population neutrality; v0surf UNMOVED `fb9efdec`, curve `e69a3f38` | `9442832` |
| `L6_pass0_state.diff` — **the N35-assert substrate** | `13b71c26` | yields `data/v0surf.pkl` `fb9efdec` (curve `e69a3f38`) — the fit-path assert is defined HERE | `f0128d6` |
| `LA_lensfield_state.diff` — superseded as live | `8650c060` | the basis-population lens whose acceptance failed limb 1 (sealed record) | `346faff` |
| `LA_anchored_state.diff` — the voided flat-lens (sealed) | `02e248dc` | — | `6736a6f` |
| `L6_HALT_state.diff` — held | `137c6d2c` | surface `31e7f00b` (curve `ca662051`) | `3ffbc1f` |
(peak `f305fe53` / pvc `ade79790` across all. Verify any capture by apply-and-hash before trusting a
recipe that names it. N35 asserts run on the PURE pass-0 substrate, never on a lens substrate.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v57 recorded it: N1–N40 stand. This cycle:
N41. **THE ACCEPTANCE-POPULATION RULING (owner word, 2026-08-04, comment 5178998844; discharged
    5179480421):** the lens's local-neutrality solve λ(pick) runs on the APPLIED population's
    anchor-weighted composition (all real ND rows, picks 1–64, drafts 2003–2025 — the acceptance's own
    population); applied rows enter as COMPOSITION WEIGHTS ONLY (pos, age, pick — no careers, no v0, no
    outcomes); the lens shape is taught exclusively by the basis artifact; tolerance/bounds/A-B unchanged;
    still-failing ⇒ HALT, never iterate. Amends the approved design by addendum on this one clause. [v566]
N42. **THE POOL RULINGS (owner words, 2026-08-04):** (a) PER-DIVISION LEVELS are the ruling — the single
    blended level retires at the landing; EXACT NUMBERS UNRULED and the pool stays NAMED UNRESOLVED
    (N37.5) until the owner signs on the re-run's return; (b) positional differentiation ROOKIE DRAFT
    ONLY; (c) the SHRINKAGE STEER — final levels confidence-weighted n/(n+K) toward the pool-wide
    MEASURED aggregate (never the model prior), K sensitivity shown (15/25/50). The re-run order is
    5179598225 (pooled-completion strata cross-division; prior-share reported before/after; raw + shrunk
    per division; RD positional raw + shrunk; same-window controls committed). [v566]

## THE QUEUE
- **#306 — L-B executing** (deterministic fit lane; the failing direction discharged by the recorded
  cross-container pair; the passing direction to earn) **+ the pool re-run beside it** (order 5179598225;
  returns via the seam, byte-identical verification, then the numbers to the OWNER for his exact-level
  signature) → **L-C** per the amended benchmark → **L6 re-enters under R-H/R-I/N19 unchanged** (bound 4 ·
  fixed point = payload md5 equality · exhausted → HALT) → converged G-Y0 vs N16 naming the surface md5 →
  L7–L8 → full rehearsal hand-back → **the EXECUTION word** → the landing (ruled curve + converged surface
  + the pool levels ship together) → candidate board → adoption (owner's separate act). Next seam
  decisions: the L-B audit · the pool re-run verification + presentation · L-C · the converged G-Y0.
- **#276 clubs tab · #270 referee** (post-adoption) · **#139 feeds** · v1.1 read outstanding.

## OWNER ACTS OUTSTANDING
The **pool exact-level signature** (when the re-run returns through the seam) · the **EXECUTION word**
(after the full rehearsal hand-back) · close clicks **#292 #283 #275** · the `rl_replacement_derive.py`
search (N23) · branch deletes — **HOLD** g4edkc · 4ql38z (carries the #279 machinery the lens depends on)
· fp78jm · fubolo · j0kwl0 · N12 holds until the landing reaches main.

## RUNNING THIS SEAT WELL — charter C1/C2/C3, M1–M3, AND the 2026-08-04 amendment govern; read them first
- **M1** one-screen replies, detail in filings · **M2** deciding-figure re-run, ruling, or audit — else
  delegate · **M3** context posture at every pen · **the twin rules:** audits check the owner's INTENT AND
  LAWS before mechanics (hazard 16); every presented number NAMES ITS QUANTITY in plain words (belief or
  outcome · basis · curve · denomination · population).
- **The owner's communication word (binding):** every agent return in VERY SIMPLE terms — what they did,
  whether it worked, what he must decide (options + recommendation, one line each). Relays IN HIS CHANNEL.
  Answer him HERE before filing anywhere.
- The era's verification standards: **v558** byte-identical re-runs (confirm the run actually RAN) ·
  **v559** verify the capture pair · **v560/N35** classify boxes by output bytes — **the assert stales on
  any observed restart; this seat re-classified mid-cycle when its container restarted, on a host whose
  CPU label matched the recorded off-class box and whose bytes proved fit-class** · the v562–v563 lessons
  as the PRIMER carries them.

## ENVIRONMENT CARRIES — as v57 in full (measurements/ lane · sealed captures · compute-path assert
`92e397bd` · strictly serial behind the preboot pgrep (bracket-safe — an unbracketed name elsewhere in the
same compound command self-matches) · venv 5-pin proof (`RL_VENV`; scripts importing numpy MUST run under
it) · N32 · N33 · N35 recipe (bootstrap from the pass-0 tree → `refit_v0surf.py --verify` from the seeded
workspace must reproduce `fb9efdec`) · envpin facts · **PEN MECHANICS** unchanged: stamp near char 88
`· v56X <date> · PEN:` → X+1, SAME LENGTH · insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · line
count unchanged · growth == entry length · one new `SEAM v56X` stamp · docs-only diff · Part B wholesale ·
commit as `supervisor-seat <supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by
CONTENT · **reset the pen branch onto origin/main BEFORE each pen**), plus: the #279 structural machinery
remains the basis of record (`…-4ql38z` AND byte-identical copies on the seat branch — RETENTION-PROTECTED)
· `structural_basis_279.json` `25a72f85` = the lens basis artifact · the acceptance instrument
`la_acceptance_perpick.py` · the pool instrument `pool_divisions.py` (labels corrected; prior-share beside
every level) · RD positional measured levels (KPD 308.1 / MID 297.8 / RUCK 286.8 / SD 248.4 / SF 228.5 /
KPF 211.8; medians 0.0, busts full weight).

## THE INCOMING SEAM'S FIRST TASKS
0. **Onboard per the amended charter order:** charter → **docs/ENGINE_PRIMER.md IN FULL** → this file IN
   FULL → register by pointer → live verify → read-back and HOLD. Every number you present names its
   quantity in plain words.
1. Verify live state with your own commands: main tip = the v566 pen or a descendant; issues #290 #292
   #279 #283 #275 #276 #270 #269 #146 #139 #306 open · #271 #274 closed · no open PRs; four gating
   workflows green (in-flight stated as in-flight); the LIVE carrier at `7e9d7f9`; the seat branch at
   `f3958c3` or a descendant; the five frozen/HOLD branches intact; the captures by apply-and-hash
   (minimum: `13b71c26` → `fb9efdec` curve `e69a3f38`, and `59ef1940` applies at the seat tip with
   v0surf unmoved); **N35-classify your own box before trusting any fit figure — check uptime first,
   the assert stales on any observed restart.**
2. The #306 seat is on **L-B** with the **pool re-run** beside it: audit L-B in the ruled order (basis →
   laws → mechanics); verify the pool re-run byte-identically and present its numbers to the OWNER simply
   — per-division, denominators and prior-shares named, raw AND shrunk (N42c) — for his exact-level
   signature.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
