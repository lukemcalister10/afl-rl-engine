# CURRENT STATE — the incoming-seat read · v68 · supervisor pen · 2026-08-06, register v577

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
(v68 · supervisor pen · 2026-08-06, register v577 · replaced wholesale at THE ADOPTION + HANDOVER PEN —
the redesign era is ADOPTED; the seat rotates; this is the incoming seam's complete read)

## THE ERA: ADOPTED. Track A refines; Track B commences on the owner's word.
- **ADOPTED 2026-08-06, owner words "Adopt. Then cut the handover and start a new seam."** The
  release-transition register carries the boundary (data/release_lineage.json entry 4, at round 20):
  destination board `827fb1fd` · store `f1e7f20c` · rl_model `33f94073` · engine_head `9f258a3b` ·
  fv `d920557e…` · balanced_board_md5 `4939d740` unmoved. One boundary adopted the whole era: the
  #306 redesign landing, the #323/#328 corrections + re-closure, the #326 pool entry anchors, the
  #334 store completion. **Adopted with eyes open:** #336 and #338 (below) continue in Track A; the
  adopted board is strictly closer to the owner's laws than its predecessor — the governing test's bar.
- **DEPLOY NOTE:** the repo's UI bundles carry the adopted board. If the owner's deploy step is
  manual, deploying is HIS act; nothing further in-repo is owed for the league to see it.
- **MERGED MAIN identities** = the destination block above + curve payload `df766dff…` (file
  `988135ef`) · surface `d594dc03…` (valid, signature unmoved) · contract sha `7033d200…` ·
  selftest 145/0. Verify with your own commands before trusting this paragraph.

## THE OWNER LAWS (all 2026-08-06, filed verbatim — read the primary copies)
- **Monotonicity (#336):** a strictly worse career never produces a better-looking baseline. The
  survivorship sweep (filed on the issue) scored 49 sites; the par surface and the load-time
  references are INVERTED; the curve's teaching basis is clean.
- **Minimum listing tenure (#338):** ND picks 1–20 → 4 seasons · 21–40 → 3 · others → 2; own data
  extends; known facts override; an evidence-less year within tenure is a LISTED sitting-out year,
  never a delisted remnant (the Willits-16 bug; historical/current era parity).
- **Presentation law (#333):** owner-facing review material is current-basis end to end or it does
  not ship; superseded views only as labeled baselines beside the current. **The owner's frustration
  is DATA, never a trigger for appeasement** (the voided Track B cut, #322, is the recorded anti-pattern).
- Unified review basis (#333) · "empty = 0 games" is a world-fact not a write instruction (#334) ·
  busts-in-denominators everywhere it is ruled · plain vocabulary · every number names its quantity.

## THE NEW SEAM'S ROAD (in order; each step's record is on its issue)
1. **Round-21 ingest + movers snapshot** — also resolves the 3 PRE-EXISTING movers-test reds
   (65-check suite; history bundle predates the live release; proven unchanged by the adoption append).
2. **The #326 guard fix:** `_merged_recover.py:1909` bars even DECLARED surface refits; teach it
   declared-vs-silent (undeclared stays red, proven able to fail). Small act, audited.
3. **#338 implemented** → the walk-forward book re-emits honestly (historical = current logic).
4. **#336 bust-inclusive variant** built on the honest book (the sweep's three levers; expectation-
   shaped consumers get P(establish)×level, NOT naive zero-filled par — the conditional/unconditional
   distinction is ruled on the issue) → **ONE side-by-side to the owner: current vs bust-inclusive**
   (board deltas, hump ratio, top-end ratio). His single open decision.
5. #332 addendum (re-center the backtest book on the owner's cohort-development words, comment
   5186108632) · the #333 re-anchoring memo absorbs the #336 result as lead candidate.
- **TRACK B (owner-framed FRESH DESIGN):** commences on the owner's word — package = the landed
  store + the owner's laws + (optionally) the #322 recipe as reference. The #322 checklist's
  recipe-amendment condition applied to the blind-rebuild framing only. Never cut under pressure.

## THE STANDING CAPTIONS
Survivorship defect LIVE in the adopted machinery (named, measured, being fixed — #336) · tenure
asymmetry LIVE in the walk-forward book (#338) · the cohort/no-arb page is marked PROVISIONAL until
the honest re-emit · completion optimism +4.7–8.4% · MSD caveat travels with its level · the book
(s4_matrix.json) is never byte-reproducible (id()-keyed) · pool tables denominate by the SIGNED
ENTRY ANCHORS (the book's v0 field for pool rows is a superseded remnant — cleanup queued with the
guard fix).

## RUNNING THIS SEAT WELL
The owner's casual questions are the project's best QC — eight catches in two days came from them.
Verify before agreeing OR disagreeing; concede precisely; file his words the same hour. His two-line
rules beat elaborate process. OPUS-ONLY subagents (owner word). Threads by comment id. The register
by pointer. Audits read code, rehearsals measure it — never skip the loop, never present on a
superseded basis, never deliver under pressure.

## ENVIRONMENT CARRIES
As v67 (venv five-pin · bootstrap-from-worktree · canonical build recipe in
docs/evidence/act_326_2026-08-06/RUN_COMMANDS.md · act evidence trees under docs/evidence/) plus:
the walk-forward book of record is SESSION-SCRATCH ONLY (per_entrant_334 was never committed — the
new seam re-emits per docs/evidence/act_334_2026-08-06/ recipes or commits its own emit with the
tenure rule); the owner-facing pages (board review · cohort tables) are claude.ai artifacts owned
by the owner's account, rebuild recipes = committed instruments + the #333-filed conventions.

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order (charter → primer → this file → register by pointer → live verify
   → read-back and HOLD). Plain vocabulary. Opus-only subagents.
1. Verify the adopted identities above with your own commands; N35-classify before any fit figure.
2. Give the owner the Track B starter package on his word (store + laws; his framing).
3. Drive the road above. His single queued decision is the #336/#338 side-by-side — reach it soon,
   with everything measured and nothing presented on a superseded basis.
