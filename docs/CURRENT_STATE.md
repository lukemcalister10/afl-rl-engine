# CURRENT STATE — the incoming-seat read · v60 · supervisor pen · 2026-08-04, register v568

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
(v60 · supervisor pen · 2026-08-04, register v568 · replaced wholesale at the L-C/L6 boundary pen — all
three redesign legs stand; the lane byte-assert is wired, LC-1 discharged; L6 is OPEN; the seam raised
rotation at ~330k and the owner ruled continue)

## THE ERA: THE CONSISTENCY ERA — #306 EXECUTING; ALL THREE REDESIGN LEGS DONE; **L6 IS RUNNING.**
Main is the v568 pen or a descendant; four gating workflows green at every content state. **L-A accepted**
(N41; 0/64 out, worst 1e-4). **L-B earned** (`b540833b` byte-identical from five materially different
starts; two extreme states re-run on the seam's box). **L-C complete as scoped**: the cross-host
byte-assert is WIRED INTO THE LANE (three outcomes: PASS · HALT naming both digests · INAPPLICABLE
stated; proven able to fire, twice independently), the emitter records only on N35-passed boxes and
refuses to overwrite disagreements; **the cross-host measurement itself is UNMEASURED BY NAME** (no
off-class box; the guard stands ahead of the evidence — never quietly green). LC-1 discharged: the
assert's anchor key component is the N32 census payload VERBATIM (`e69a3f38`, picks 1–64 only — the pool
slot excluded, so N43's landing cannot silently retire the expectation). **The pool levels are SIGNED
(N43).** The **EXECUTION word remains WITHHELD**; the bake is HELD; nothing has landed. LIVE carrier
`claude/exec-seat-290-handoff-d7bnaa` at `7e9d7f9`; seat branch `claude/exec-seat-306-afl-rl-zlaarm` at
`fd0d0c5` or a descendant (L6 passes expected).

## THE TWO-CURVE IDENTITY CENSUS — unchanged (glossary: PRIMER §5 incl. pathway tags)
| curve | payload | what it is | where it lives |
|---|---|---|---|
| the SHIPPED curve | `08ea9375` | #271 stage-B ladder (measured 0.0248% reality) | main's product files — replaced at the landing |
| **the RULED curve — THE ANCHOR** | **`e69a3f38`** | #279 structural ladder: classes 2004–2022, pick64=221, NO pick 65, completion +4.7–8.4% optimistic REPORTED | the rehearsal substrate; ships with the EXECUTION word |
`b540833b` = the lens-lane surface (any-start L-B result under `e69a3f38`) · `b760b17e` = the lane
assert's lens-grid digest · lane key = `basis md5 12 | census payload 8 | roster digest 12`.

## THE CAPTURE TABLE — A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | what it is | base |
|---|---|---|---|
| `LC1_anchor_component_state.diff` — **THE LIVE SUBSTRATE** | `efaf67d6` | lens + N41 neutrality + the lane assert (anchor component = census payload); v0surf UNMOVED `fb9efdec` | `279e9be` |
| `L6_pass0_state.diff` — **the N35-assert substrate** | `13b71c26` | yields `fb9efdec` (curve `e69a3f38`) — the fit-path assert is defined HERE | `f0128d6` |
| `LC_lane_assert_state.diff` — superseded (LC-1) | `e9508660` | the 65-key anchor component (sealed) | `352a51e` |
| `LA_applied_neutrality_state.diff` — superseded | `59ef1940` | L-A accepted state | `9442832` |
| `8650c060` · `02e248dc` · `137c6d2c` | — | failed-limb-1 lens · voided flat-lens · the halt state | sealed records |
(N35 asserts run on the PURE pass-0 substrate only. L6 passes will supersede the live capture per pass —
verify each by apply-and-hash before trusting its recipe.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
N1–N43 stand as v59 recorded them (N41 acceptance-population · N42 pool principle/RD-only/shrinkage ·
N43 the signed levels with the ND-65+ cap bound to curve[64]). No new numbered ruling this cycle; the
L-C completion, LC-1, and the L6 opening are recorded at v568.

## THE QUEUE
- **#306 — L6 IS RUNNING** (the re-entered convergence loop, R-H/R-I/N19 unchanged: bound 4 · fixed
  point = payload md5 equality · exhausted → HALT · G-Y0 every pass with its denominator · the lane
  expectation re-recorded per pass on an N35-passed box) → **converged G-Y0 vs N16's trigger naming the
  surface md5** → L7–L8 → **full rehearsal hand-back** → **the EXECUTION word** → the landing (ruled
  curve + converged surface + the N43 signed pool levels ship together) → candidate board → adoption
  (owner's separate act). Next seam decisions: the L6 outcome audit (fixed point or honest HALT — both
  are outcomes; audit basis → laws → mechanics) · the converged G-Y0 against N16 · the hand-back
  verification.
- **#276 clubs tab · #270 referee** (post-adoption) · **#139 feeds** · v1.1 read outstanding.

## OWNER ACTS OUTSTANDING
The **EXECUTION word** (after the full rehearsal hand-back) · close clicks **#292 #283 #275** · the
`rl_replacement_derive.py` search (N23) · branch deletes — **HOLD** g4edkc · 4ql38z (the #279 machinery
the lens depends on) · fp78jm · fubolo · j0kwl0 · N12 holds until the landing reaches main.

## RUNNING THIS SEAT WELL — charter C1/C2/C3, M1–M3, AND the 2026-08-04 amendment govern; read them first
- **M1** one-screen replies · **M2** deciding-figure re-run, ruling, or audit — else delegate · **M3**
  context posture at every pen · **the twin rules:** intent-and-laws before mechanics (hazard 16); every
  number names its quantity (belief or outcome · basis · curve · denomination · population).
- **The owner's communication word (binding):** agent returns in VERY SIMPLE terms — what they did,
  whether it worked, what he must decide (options + recommendation, one line each). Relays IN HIS
  CHANNEL. Answer him HERE before filing anywhere.
- Verification standards: **v558** byte-identical re-runs (confirm the run RAN) · **v559** verify the
  capture pair · **v560/N35** boxes classify by output bytes; **check uptime before EVERY fit figure —
  this seat re-classified four times in one day**, every restart caught before a figure was trusted ·
  the preboot pgrep runs in its OWN command (self-match otherwise — bitten twice) · rotation raised at
  ~330k, owner ruled continue; next raise at the post-L6 boundary or any degradation sign.

## ENVIRONMENT CARRIES — as v59 in full (measurements/ lane · sealed captures · compute-path assert
`92e397bd` · strictly serial · `RL_VENV` 5-pin venv · N32 · N33 · N35 recipe (bootstrap from the pass-0
tree → `refit_v0surf.py --verify` reproduces `fb9efdec`) · **PEN MECHANICS** unchanged (stamp near char
88 SAME LENGTH · insert before ` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry
length · one new stamp · docs-only · Part B wholesale · commit `supervisor-seat <supervisor@seam.local>`
· branch → PR → rebase-merge → re-verify main by CONTENT · reset pen branch onto origin/main first;
force-with-lease is the normal push when the old tip is merged history)), plus: `structural_basis_279.json`
`25a72f85` · `lane_expectation.json` (key `25a72f85a96b|e69a3f38|bce3c13d27ff` → lens digest `b760b17e`)
· instruments: `la_acceptance_perpick.py` · `pool_levels_rerun.py` (N43's source) · `lb_determinism.py` ·
`emit_lane_expectation.py` · the #279 machinery on `…-4ql38z` RETENTION-PROTECTED.

## THE INCOMING SEAM'S FIRST TASKS
0. **Onboard per the amended charter order:** charter → PRIMER IN FULL → this file IN FULL → register by
   pointer → live verify → read-back and HOLD. Every number names its quantity.
1. Verify live state with your own commands: main tip = the v568 pen or a descendant; eleven issues open
   / #271 #274 closed / no open PRs; four gating workflows green (in-flight stated as in-flight); LIVE
   carrier `7e9d7f9`; seat branch `fd0d0c5` or a descendant; frozen/HOLD branches intact; captures by
   apply-and-hash (minimum `13b71c26` → `fb9efdec`; the live capture applies at the seat tip, v0surf
   unmoved) — **N35-classify your own box first; check uptime; the assert stales on any restart.**
2. The #306 seat is running **L6**: audit its passes as they file (basis → laws → mechanics; every pass's
   G-Y0 with denominator; the lane expectation re-recorded per pass; fixed point = payload md5 equality;
   HALT is an honest outcome, not a failure to hide) → the converged G-Y0 against N16 → the hand-back.
3. Read-back to the owner — short and simple per C1/M1 — then hold for confirmation before any push.
