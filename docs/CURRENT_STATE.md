# CURRENT STATE — the incoming-seat read · v66 · supervisor pen · 2026-08-06, register v575

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
(v66 · supervisor pen · 2026-08-06, register v575 · replaced wholesale at the HANDOVER-READINESS PEN —
the #334 store-completion act is IN REHEARSAL; the review tooling exists; two new owner laws bind
presentations; the road: land #334 + its re-derivations → regenerate the review tables → the backtest
book (#332, addendum owed) → the re-anchoring memo (#333) → ADOPTION)

## THE ERA: DATA COMPLETION INSIDE THE REVIEW ROAD. #326 landed; #334 mid-act; nothing adopted.
- **MERGED MAIN = `da9aa70` or descendant.** Store `f1e8c9fed35462536d00add604f69a3f` · curve payload
  `df766dff…` (file md5 `988135ef`) · surface `d594dc03…` · board `864b6726` · engine head `9f258a3b` ·
  contract sha `8cc7d897` · selftest 145/0. The league-facing app UNCHANGED until adoption.
- **#334 (store early-season completion + re-derivation) is the live act — owner-ordered, censused
  from the owner's own corrected sheet, audit-passed, IN REHEARSAL at this pen.** The census (evidence
  `docs/evidence/store_completion_2004_2005/`, committed): 51 season inserts (2005: 14 · 2006: 37, +287
  career games over 40 players), 177 zero-confirmations writing NO rows (ruled — explicit zeros would
  silently add ~138 bust training-cells; the owner's "empty = 0 games" is a world-fact, not a
  write instruction), 0 conflicts; Drummond year 2003→2004 pick 35→40 between Shaw and Clarke, both
  rookie groups re-numbered, stream mirrors move too. Binding spec = #334 addendum 1 + owner answers
  (Iles insert STANDS; Paul Thomas confirmed). Stage A: store fix, ZERO board movement (all touched
  rows retired; assert keyed on `key` — two distinct Will Hamills exist). Stage B: N35 fit-class
  classification FIRST (reproduce surface `d594dc03` from current inputs; if the box fails, stage A
  stands alone), then matrix re-emit under the post-#326 engine, curve+surface re-derivation, the ±1
  rule vs payload `df766dff` (any pick moving >1 board point RETURNS TO THE OWNER pre-ship).
- **The #326 story in one line for the incoming seat:** the owner ruled pool entry anchors bite like
  the pick curve for year-0 players (issue #326 addenda 5–6); landed 2026-08-06; 177 pool movers, zero
  non-pool; the veteran-floor reach stands as ruled; the ENTRY-PRICE ASYMMETRY it fixed is measured at
  #333 (pool non-debutants 0.34× vs ND 0.58×; debutants near-parity).

## TWO OWNER LAWS OF 2026-08-06 (filed #333, binding on every presentation)
- **UNIFIED REVIEW BASIS:** cohort tables use cohorts 2004–2025 (2003 never — its year 1 predates the
  data), 2004/05 records excluded from year-1/2 totals until #334 lands (then the exclusions LIFT),
  young classes count where reached, MSD to the prior-year cohort.
- **PRESENTATION LAW:** owner-facing review material is CURRENT-BASIS end to end or it does not ship;
  a superseded view may appear only as a labeled baseline BESIDE its current counterpart, never alone.
  A staleness caption is NOT sufficient (the recorded failure: the pre-#326 pool cohort table).
  The no-arb/cohort pages are FROZEN until #334's chain refreshes the walk-forward record.

## WHAT FIRES NEXT, IN ORDER
1. **#334 hand-back → seam verifies deciding figures → land** (branch → PR → rebase-merge, evidence
   tree, pen). If stage B moved any pick >1 point: owner decision BEFORE ship. Pool-level measures may
   shift (rookie careers extended) — the signed levels NEVER auto-recompute; re-sign is owner word.
2. **Regenerate the review tables from the refreshed record** (current-basis law); pre-#326 pool table
   shown only as labeled baseline. Published pages: board review + no-arb tables (claude.ai artifacts,
   session-published; rebuild recipes = the committed instrument + the conventions filed on #333).
3. **#332 backtest book:** audit verdict NOT PASSED — the owner's PRIMARY words (#306 comment
   5186108632) order a COHORT-DEVELOPMENT book ("prior cohorts and their development over time, on the
   walk-forward record", governing word "HONEST and sincere", busts in denominators AT EVERY YEAR);
   the seat owes an addendum re-centering the directive on those words with the cohort tables as the
   spine; the audit's fault list (stale harness pointer, McCartin/Boyd over-scope, ch4 hard-band
   import, no bust flag — use never_established()) is on the issue.
4. **The re-anchoring memo (#333):** all steers filed verbatim (partial pricing-in, never inversion;
   top-end 4.03× "a little steep"; pedigree-conditioned reactivity — the Mraz case; the tenure-window
   note). Wants the refreshed pool table first (the residual cliff is what it prices).
5. **ADOPTION (owner click) → round-21 ingest + movers page.** Release-transition register at adoption.
- Queued small repairs unchanged from v65 (ship_gates γ conflict · extract_seam stale seal ·
  RECLOSURE "100 PASS" prose · weekly_updater · first-failure masking · attribution instrument scoped
  to intra-engine acts).

## RUNNING THIS SEAT WELL (deltas from v65)
The owner's casual questions remain the best QC in the project — this era's catches (γ, currency,
store gaps, Drummond, the pool cliff) all came from them. Answer the question asked, verify before
agreeing OR disagreeing, and file his words verbatim the moment they carry a ruling. Subagents
OPUS-ONLY. Threads by comment id. The register by pointer. Six audit rounds this era each found real
faults: never skip the loop, and remember #326's lesson — audits read code, rehearsals measure it.

## ENVIRONMENT CARRIES
As v65 plus: the #334 rehearsal working copy is a git worktree of this container (scratchpad —
EPHEMERAL; if the container died mid-act, re-run the hand from the committed census: the act is fully
specified by #334's body + addendum 1 + owner answers + census.json). Build/verify recipes proven this
session: five-pin venv + bootstrap from the worktree + the canonical rl_export invocation
(docs/evidence/act_326_2026-08-06/RUN_COMMANDS.md). The no-arb instrument at
docs/evidence/noarb_2026-08-05/ (re-run recipe in its README); the cohort-table conventions filed on
#333 (unified-basis comment). Fit-class recipes unchanged from v63/v64 carries.

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order. Plain vocabulary. Opus-only subagents.
1. Verify MERGED MAIN above with your own commands. Check #334's state: if the act landed, verify its
   evidence; if mid-flight, the rehearsal is re-runnable from the committed census (nothing depends on
   dead scratchpad state).
2. Drive the order above: #334 → tables → #332 addendum → memo → ADOPTION.
3. Every presentation obeys the two owner laws of 2026-08-06. Every number names its quantity.
