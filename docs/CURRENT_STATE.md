# CURRENT STATE — the incoming-seat read · v67 · supervisor pen · 2026-08-06, register v576

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
path**: branch → PR → rebase-merge. The merge under the owner's platform auth is a **housing fact,
not an approval step**. Docs-only pens land **without a per-entry word** (v483, restored by owner
word 2026-07-27), guarded by structural asserts proven pre-commit: line count unchanged, growth equal
to entry length, single stamp, PRIOR chain intact, docs-only diff. **Reversal is self-executing** —
any pen error reaching main restores the per-entry word.

**Ref deletion is proxy-forbidden to seats.** Branch deletes are an owner click. Do not retry it.

---
# PART B — CURRENT STATE
(v67 · supervisor pen · 2026-08-06, register v576 · replaced wholesale at the #334 STAGE-A LANDING —
the store is completed on the owner's census; the SURVIVORSHIP DEFECT re-sequenced the road; the
curve re-derivation is DEFERRED; the owner's next ruling is the current-vs-bust-inclusive side-by-side)

## THE ERA: THE SURVIVORSHIP RECKONING. Store complete; the design question is open; nothing adopted.
- **MERGED MAIN = the v576 landing or descendant.** Store **`f1e7f20c4adea9b17d19457a5217c735`**
  (the owner's census applied: 51 back-filled 2005/06 seasons, +287 career games/40 players,
  Drummond to 2004 pick 40, both rookie groups re-numbered) · board **`827fb1fd`** (154 indirect
  movers net −819 vs 864b6726 through the load-time references; zero direct movement; owner-accepted) ·
  curve payload `df766dff…` UNCHANGED (file `988135ef`; its source-store stamps deliberately still
  `f1e8c9fe` — the store the ruled curve was derived on; all FROZEN-RULER checks pass) · surface
  `d594dc03…` (valid against the completed store — signature unmoved) · engine head `9f258a3b` ·
  contract sha `7033d200…` · selftest 145/0. League-facing app UNCHANGED until adoption.
- **THE SURVIVORSHIP DEFECT (#336) governs the road.** Owner-named (the ABLETT INVERSION): the
  engine's load-time reference tables sample `pkbest is not None` — mediocre careers lower the
  average, zero-game busts VANISH, so measured history ranks nothing above something. The owner's
  MONOTONICITY LAW is filed: a strictly worse career never produces a better-looking baseline.
  Standing hypothesis with the memo: survivors-only benchmarks suppress early-career prices and
  MANUFACTURE the 1.57× hump. Sibling instances named: the walk-forward training window
  (row-presence keyed) and the per-year calibration (the owner's tenure point).
- **SEQUENCING (owner word 2026-08-06):** the curve re-derivation under the current method is
  DEFERRED — never present a table that the pending ruling would supersede (presentation law).
  The road: (1) matrix re-emit on the completed store under current machinery = the measurement
  substrate; (2) the #336 SWEEP (every sample-membership filter on the price path, one table,
  each tested against the monotonicity law) + the BUST-INCLUSIVE VARIANT (references rebuilt
  counting zero-row players; board re-priced; hump + top-end ratios recomputed); (3) ONE owner
  ruling on the side-by-side; (4) the ruled overhaul lands as its own audited directive; then the
  review set completes and ADOPTION.
- **STAGE B LANE BLOCKED:** #326's no-silent-refit assert (`_merged_recover.py:1909`) bars even the
  DECLARED refit lane — a small audited guard fix is owed before any surface refit (undeclared
  refit must stay red). Not urgent while the re-derivation is deferred.
- **TRACK B:** a package was cut prematurely and VOIDED by owner word within the hour. The
  READINESS CHECKLIST is sealed on #322 (comment 5200190050): store landed ✓(now) · #336 ruled +
  recipe amended with the monotonicity law · measurement layer current · recipe re-verified.
  Cuts once, from landed main, when the list is green. Do not cut early again — recorded seat miss.

## THE OWNER LAWS OF 2026-08-06 (all filed verbatim, #333/#336)
Unified review basis (2004–2025, no 2003; 04/05 y1-2 excluded until the census extends there —
NOTE stage A landed the 2005/06 fills, so those exclusions LIFT when the tables regenerate on the
re-emitted record) · the presentation law (current-basis or it does not ship; baselines only
labeled and beside their current counterpart) · the monotonicity law (above) · "empty = 0 games"
is a world-fact, not a write instruction (no zero rows; the zero-convention ruling, #334 add.1).

## WHAT FIRES NEXT, IN ORDER
1. Matrix re-emit on `f1e7f20c` (current machinery) — measurement substrate. Regenerate the frozen
   review pages from it (presentation law; the pre-#326 pool table only as labeled baseline).
2. #336 sweep + bust-inclusive variant → the side-by-side → OWNER RULING.
3. The ruled overhaul (its own directive + audit) · the #326 guard fix rides it or precedes it.
4. #332 backtest book addendum (owed: re-centered on the owner's cohort-development words, comment
   5186108632) — its cohort tables regenerate from the re-emitted record.
5. The re-anchoring memo (#333) absorbs #336's result (lead candidate) → owner design ruling.
6. Review set assembled → ADOPTION (owner click) → round-21 ingest + movers page.
- Queued small repairs as v65/66 list, plus: the book (s4_matrix.json) is id()-keyed and not
  byte-reproducible by construction (workspace intermediate, unpinned — never claim its bytes).

## RUNNING THIS SEAT WELL (the v576 lessons, additive to v65/66)
The owner's frustration signals are DATA about the project, never triggers for appeasement — the
voided Track B cut is the recorded anti-pattern (delivering under pressure inverted the seat's
function). Hold readiness lines; convert frustration into filed laws and checklists. His logic
challenges have been right seven consecutive times — verify, concede precisely, and file his
words the same hour. Opus-only subagents; threads by comment id; every number names its quantity.

## ENVIRONMENT CARRIES
As v66 plus: stage-A act evidence + re-run recipes at `docs/evidence/act_334_2026-08-06/` (the
apply/parse/gate scripts are re-runnable from the committed census; the rehearsal worktree is
ephemeral). The board baseline pair for attribution: `864b6726` (pre) → `827fb1fd` (post stage A).

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order. Plain vocabulary. Opus-only subagents.
1. Verify MERGED MAIN above by your own commands (store, board, carriers, selftest).
2. Drive the order above. The owner's open decision is the #336 side-by-side — build it soonest.
3. Every presentation obeys the owner laws. Track B only by the #322 checklist.
