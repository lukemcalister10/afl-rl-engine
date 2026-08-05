# CURRENT STATE — the incoming-seat read · v64 · supervisor pen · 2026-08-05, register v573

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
(v64 · supervisor pen · 2026-08-05, register v573 · replaced wholesale at the SECOND-ERA PEN — the
landing AND the store act are MERGED; the corrected store is the official state; the curve is
re-closed on it; the seam rotates at this pen; the road left is: #326 → the review set → ADOPTION)

## THE ERA: THE REVIEW ROAD. Everything is landed; nothing is adopted.
- **MERGED MAIN = `8915b3a` or a descendant.** The official state: store `f1e8c9fed35462536d00add604f69a3f`
  (the #323 corrections in full — the old pin `81d24704` is RETIRED) · ruled curve payload
  **`df766dff94657940e2a892e91da5a6e2`** (the re-closure, owner word "A") with pool companion 237.2 ·
  surface `d594dc03…` · entrant seal `c9e7491b` at total 62,931 · G-Y0 0.033% (n=1,326, 2.000% HARD,
  no exception behind it) · selftest 97/0.
- **The closure HOLDS on the final pair** (confirmation derivation: 15 picks differ, max 1, zero over
  the ±1 tolerance). REVERSAL CONDITION STANDING, re-anchored to `df766dff…`: any future derivation
  pass moving any pick by MORE than 1 board point re-opens the closure and returns it to the owner.
- **THE APP THE LEAGUE SEES IS UNCHANGED.** Adoption is the owner's separate click, after his review
  set. The release-transition register appends AT ADOPTION ONLY (seam records ruling, #328 thread).

## WHAT FIRES NEXT, IN ORDER
1. **#326 — the N43 per-division pool levels** (AUDIT-PASSED after 4 passes; fires on the OWNER'S
   SLOT WORD — before adoption is the seam recommendation). It also structurally resolves the
   inherited `club_curve_provenance` red (the single pool level above curve[64]=185 is the exact
   tension the signed design removes: only ND-65+ is capped).
2. **The review set to the owner:** the per-stage before/after (curve+surface stage committed at the
   landing evidence; store + re-closure stages committed at the store-act evidence; assemble the
   owner-facing view) · the honest backtest book (directive to author; owner's word: busts stay in
   every denominator, biases printed beside results) · the no-arbitrage tables (measured, delivered
   in-channel; the instrument is COMMITTED at `docs/evidence/noarb_2026-08-05/` — re-run it on
   final bytes per its README) · **the RE-ANCHORING DESIGN MEMO** (the measured 1.57× hump vs the
   owner's no-arbitrage law; his convexity mechanism endorsed; candidate fixes with this same table
   recomputed under each — the design conversation of the review era).
3. **ADOPTION (owner click) → round-21 ingest + movers page.**
- Small queued repairs, either-order: live-scoring `test_weekly_updater` (scratch-fixture drift,
  proven inherited) · the first-failure masking on Final Integration (main hid a red stack).

## TRACK B — CUTTABLE NOW
The corrected store IS main's store, so the blind-build package (recipe · constants · store) cuts
from real main whenever the owner wants it. FROZEN MODELS WITHHELD (owner word, #322 5188203865).
Judged by OUTPUTS ONLY against the landed board.

## THE STANDING CAPTIONS EVERY NUMBER CARRIES
Wide feed-back channel (55.78%/44.22%) · the engine contributes zero to teaching-value movement ·
wholesale-belief 6.18% of teaching value (the −0.63% move is a floor) · completion optimism
+4.7–8.4% beside anything it touches · the no-arbitrage hump (year-0 → 1.57× by years 4–5, the 2020
class excepted) is MEASURED and awaits the owner's design word — no price moves because of it yet.

## THE ENVIRONMENT HAZARD (live, managed)
Model content-filter false positives on the project's OLD vocabulary paused three seats this era;
every recovery worked (model-switch → continue; or a fresh seat from the pushed record). PLAIN
VOCABULARY IS LAW for all new text (charter amendment 2026-08-05); the primer's glossary maps
old → new; never echo file contents into seat chat; keep seat replies short.

## N35 — THE BOX DISCIPLINE (unchanged, and it caught everything this era)
Classify before ANY fit figure by REPRODUCING recorded bytes (the recipes in ENVIRONMENT CARRIES);
check uptime EVERY time; a restart voids the classification. This era's record: five distinct
old-path byte patterns across boxes with identical CPU labels; the redesigned fit path reproduced
its surfaces on every fit-class box AND the value path reproduced the board byte-identically on a
DIFFERENT ARCHITECTURE. Labels classify nothing; bytes classify.

## OWNER ACTS OUTSTANDING
The #326 slot word (before/after adoption) · the review set → ADOPTION click → round-21 · the two
queued small repairs can ride any convenient act · N12 and branch-delete holds as before.

## RUNNING THIS SEAT WELL
Charter C1–C3, M1–M3, the two rules (intent before mechanics · every number names its quantity),
the owner's binding words (plain English, short sentences, direct answers first, ~one screen), the
pre-fire audit loop for every directive (10 real faults caught in one day — never skip it), and the
owner's casual questions are load-bearing QC (two of this era's findings came from them).
**SUBAGENTS ON OPUS ONLY — never Fable, never an inherited default** (owner word; charter amendment
2026-08-05 third block; a prior session burned ~1.7M Fable tokens learning this). **Context economy:
the #306 and #328 threads are enormous — read ONLY the comment ids this file names, never a thread
front to back; the register only by pointer; evidence trees only the files a task touches.**

## ENVIRONMENT CARRIES
As v63 (RL_VENV five-pin venv · setup_env.sh · the N32 payload recipe (string keys, int(round),
sort_keys, md5) · N33 re-stamps · strictly serial fits · PEN MECHANICS: stamp near char 88 SAME
LENGTH · insert before the ` · SEAM v540 (2026-07-29)` marker · line count 8,438 · growth == entry
length · one new stamp · docs-only · commit `supervisor-seat <supervisor@seam.local>` · branch → PR
→ rebase-merge → re-verify main by CONTENT), with the era's identities REPLACED by the MERGED MAIN
block above. The derivation machinery: the #279 panel from `9914c4d` + the CURRENT re-pinned
harness from main + `pooled_numeraire.py MATRIX PANEL OUTDIR`. The fit recipes: old path reproduces
`fb9efdec` from the pure pass-0 snapshot `13b71c26` (fit-class test); the live path's current
surface is `d594dc03` on the merged pair. The no-arbitrage instrument is COMMITTED with outputs
and re-run recipe at `docs/evidence/noarb_2026-08-05/` — never rebuild it; its README says how
to re-run on final bytes.

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order (charter → primer IN FULL → this file IN FULL → register by
   pointer → live verify → read-back and HOLD). Plain vocabulary in everything.
1. Verify the MERGED MAIN block with your own commands; N35-classify your box.
2. Ask the owner for the #326 slot word; fire #326 (its audit trail is complete on the issue).
3. Assemble the review set (the four items above), verifying each number from committed bytes.
4. Present for ADOPTION; the release-transition register appends there, with the owner's word.
