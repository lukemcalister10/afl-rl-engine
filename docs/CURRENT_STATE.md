# CURRENT STATE — the incoming-seat read · v65 · supervisor pen · 2026-08-06, register v574

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
(v65 · supervisor pen · 2026-08-06, register v574 · replaced wholesale at the #326 LANDING PEN — the
per-division pool entry anchors are LANDED; the board identity moved; the road left is: the review
set → ADOPTION)

## THE ERA: THE REVIEW ROAD. Everything is landed — including #326; nothing is adopted.
- **MERGED MAIN = the v574 landing commit or a descendant.** The official state: store
  `f1e8c9fed35462536d00add604f69a3f` (unchanged) · ruled curve payload `df766dff94657940e2a892e91da5a6e2`
  (UNMOVED by #326; the artifact FILE md5 moved to `988135ef` for the pool_levels block) · surface
  `d594dc03…` (LOADED, never refit — proven) · **board `864b6726`** (was `2b7c1a00`; 177 pool movers,
  zero non-pool field changes) · engine head `9f258a3b` (was `15525b03`) · contract sha `8cc7d897` ·
  selftest **145/0** (97 pre-existing + 48 new #326 checks, each proven able to fail both directions).
- **#326 IS LANDED (2026-08-06, owner words "Keep as ruled. Land it.").** The N43 signed levels price
  pool entrants AT ENTRY the way the pick curve prices national draftees: the entry anchor feeds the
  year-zero floor (scope widened from ND-only to engine-pool, NOT gated on _pickless) and the sit-out/
  thin-record blend; ladder currency at the ruck-cap sites, ×1.0524 at the engine-value sites; the old
  single-pool-value machinery is superseded on the entry path. Kept deliberately (byte-identical, the
  one place old machinery still fires, reversal = one owner sentence): staleness cap, mediocre cap,
  delisted remnant. The veteran-floor reach stands AS RULED (26 remnant-value movers, Rampe 1→12 class).
  The inherited club_curve_provenance red is structurally resolved. Full trail: issue #326 addenda 5–6 +
  the fifth audit pass; evidence `docs/evidence/act_326_2026-08-06/` and the halted first rehearsal
  `docs/evidence/rehearsal_326_2026-08-05/`.
- **THE APP THE LEAGUE SEES IS UNCHANGED** (adoption = the owner's separate click). NOTE for the next
  seat: the repo's UI bundles (`ui/data/board_view_*.js`) already carry the landed board — they were
  regenerated at #328 step 6b and again by #326; whether the deployed app shows them depends on the
  owner's deploy step, not this repo.

## WHAT FIRES NEXT, IN ORDER
1. **The review set to the owner** (in progress this era): the before/after board review EXISTS as an
   owner-facing page (published artifact "Board review — before and after"; data + generator in the
   session scratchpad, rebuildable from committed boards): raw before/after decomposed into
   engine+store catch-up (−52,528, NOT the redesign) · curve+surface swap (+954, like-for-like on the
   committed B0 intermediate `31f7108a`) · store corrections (+638) · re-closure (+10,258) · now the
   #326 pool slice (177 movers). Remaining: the honest backtest book (directive to author; busts stay
   in every denominator) · the no-arbitrage tables re-run on final bytes (instrument committed at
   `docs/evidence/noarb_2026-08-05/`) · the re-anchoring design memo (the 1.57× hump).
2. **ADOPTION (owner click) → round-21 ingest + movers page.** Release-transition register appends at
   adoption only.
- Small queued repairs, any convenient act: live-scoring `test_weekly_updater` (inherited) ·
  first-failure masking on Final Integration · `ship_gates_check.py` gamma env conflict at tip
  (pre-existing; its re-scoped B5 block is correct and was exercised directly) · `ui/tests/
  extract_seam.test.py` still asserts the pre-reclosure entrant seal `a17aafed` · RECLOSURE.md says
  "100 PASS" where the committed evidence shows 97 · the committed attribution instrument is scoped to
  intra-engine acts (halts honestly when the engine head moves — by design, recorded).

## TRACK B — CUTTABLE NOW (unchanged from v64; frozen models withheld, judged by outputs only)

## THE STANDING CAPTIONS EVERY NUMBER CARRIES
As v64 (wide feed-back channel 55.78%/44.22% · completion optimism +4.7–8.4% — now printed beside the
MSD level everywhere it shows · the no-arbitrage 1.57× hump measured, awaiting the owner's design word)
PLUS: γ is the SCAR(0.85, concave)-vs-VOR(1.0, linear) compression exponent on an internal function —
NOT a future-season discount, and NOT the shipped board's denomination in either era (owner-corrected
2026-08-05; both eras' exporters price from the engine's gated ev()).

## THE ENVIRONMENT HAZARD (unchanged from v64: plain vocabulary is law; never echo file contents into
seat chat; recovery from the pushed record works)

## N35 — THE BOX DISCIPLINE (unchanged). This era's box: value-path classified by byte-reproducing the
board twice (2b7c1a00 pre-act, 864b6726 post-act). No fits were run; fit-class classification not needed.

## OWNER ACTS OUTSTANDING
The review set → ADOPTION click → round-21 · the queued small repairs can ride any act · N12 and
branch-delete holds as before.

## RUNNING THIS SEAT WELL (unchanged from v64 — Opus-only subagents; threads by comment id only;
the register by pointer; intent before mechanics; every number names its quantity. This era's lesson,
twice over: a four-pass-audited premise was refuted by the first build that tested it — audits read
code, rehearsals measure it; and the owner's memory beat the derived caption on γ within minutes.)

## ENVIRONMENT CARRIES
As v64 with these deltas: board `864b6726` · engine head `9f258a3b` · contract sha `8cc7d897` · curve
FILE md5 `988135ef` (payload `df766dff` unmoved) · selftest count 145/0 · register line count 8,438 ·
the #326 build/verify recipe in `docs/evidence/act_326_2026-08-06/RUN_COMMANDS.md`.

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order. Plain vocabulary in everything.
1. Verify the MERGED MAIN block above with your own commands (board, payload, selftest count).
2. Assemble the remaining review set items (backtest book directive → pre-fire audit; no-arbitrage
   re-run on final bytes; re-anchoring memo) and present for ADOPTION.
3. At adoption: release-transition register appends, with the owner's word; then round-21 ingest.
