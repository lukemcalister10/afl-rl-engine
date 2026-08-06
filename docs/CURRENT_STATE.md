# CURRENT STATE — the incoming-seat read · v76 · supervisor pen · 2026-08-06, register v585

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
(v76 · supervisor pen · 2026-08-06, register v585 · replaced wholesale at the NO-ARB REISSUE PEN —
the per_entrant lineage and no-arb tables are on the #338 basis; cohort tables NO LONGER
PROVISIONAL for tenure (the #336 survivorship dimension remains open). The primer is at v4 — read
it first, in full.)

## THE ERA: ADOPTED. Track A refines; TRACK B IS CUT.
- **ADOPTED 2026-08-06, owner words "Adopt. Then cut the handover and start a new seam."** The
  release-transition register carries the boundary (data/release_lineage.json, entry 4, at round 20).
  One boundary adopted the whole era: #306 landing · #323/#328 corrections + re-closure · #326 pool
  anchors · #334 stage-A store completion. Adopted with eyes open: #336 and #338 continue in Track A.
- **THE CURRENT IDENTITIES (round 21 applied 2026-08-06; verify with your own commands):**
  store `37ced3ce45914e6feb00d27e26922e9a` = `engine/rl_after/rl_model_data.json` · board
  `113b36f898a32363c49c2a62fb809f4b` = `data/rl_build/rl_app_data.json` · rl_model `33f94073` ·
  engine_head `8f0e3eb1` (#344 merged 2026-08-06, owner word) · curve payload
  `df766dff…` (file `988135ef`) · surface `d594dc03…` = `data/v0surf.pkl` · balanced_board_md5
  `4939d740` (present-lens anchor, unmoved) · season round 21 · adoption-era pair for attribution:
  `827fb1fd` (adopted, round-20 basis, out-of-round column `redesign-adoption-6-8`) → `113b36f8`
  (round 21). The v582 seat byte-reproduced the ADOPTED board pre-R21 on this box (N35 value-path). SELFTEST EXPECTATION: 144 PASS / 0 FAIL (the Kako 2026 anchor retired by owner word 2026-08-06; every older \u0022145/0\u0022 note is superseded).
- **EXPECTED, NOT DRIFT:** `ui/release_pick_curve.json` still stamps `curve_source_store_md5 =
  f1e8c9fe` (pre-completion) — #334 STAGE B deferred by owner word behind the #336 ruling. The
  movers reds are CLEARED (R21 landed; #271 A17 closed; suites 66/66 · 39/39 · 5/5).
- **DEPLOY:** the repo's UI bundles carry the adopted board; `ui/index.html` from a checkout/zip IS
  the app. If the owner's deploy step is manual, deploying is his act.

## THE OWNER LAWS (2026-08-06 unless noted; primary copies on the named issues)
- **Monotonicity (#336):** a strictly worse career never produces a better-looking baseline. The
  49-site sweep is on the issue; par surface + load-time references INVERTED; curve teaching clean.
  Repair rule: expectation-shaped consumers get P(establish)×level; never zero-fill a per-game bench.
- **Minimum listing tenure (#338):** ND 1–20 → 4 seasons · 21–40 → 3 · others → 2; own data extends;
  known facts override; evidence-less years inside tenure are LISTED sitting-out years. IMPLEMENTED
  2026-08-06 in the book emitter (board untouched); cohort tables PROVISIONAL until the no-arb
  lineage re-emits under the rule.
- **Presentation law (#333):** owner-facing material is current-basis end to end or it does not
  ship; superseded views only as labeled baselines beside the current. **Owner frustration is DATA,
  never a trigger** (the voided Track B cut, #322 comment 5200190050, is the recorded anti-pattern).
- Unified review basis (#333 comment 5199421546) · "empty = 0 games" is a world-fact, not a write
  instruction (#334 addendum 1) · busts-in-denominators wherever ruled · plain vocabulary · every
  number names its quantity · the pool-table denominator is the SIGNED ENTRY ANCHORS (primer §4.8).

## TRACK B: CUT, RE-CUT SIMPLE ON OWNER WORD, DELIVERED 2026-08-06 (register v579–v580)
The v579 pack (laws bundle + constants + addendum) was REJECTED by the owner as a dense deposit
imposing this project's structure — his frame: "This is the store, it has the information. This is
the recipe we use to calculate value based on this information." Delivered instead:
`AFFL_track_b_2026-08-06.zip` = TWO files — the landed store verbatim (`f1e7f20c…`) +
`THE_RECIPE.md` (the #322 recipe surgically updated to the adopted truth, dangling references
removed, closing "WHAT WE GOT WRONG" advice section — 8 items, advice not law). The v579 zip is
withdrawn; FINDINGS.md stays owner-side; the filed #322 recipe on its branch is untouched. The
full pen detail is the v580 register entry; the v581 entry records the owner-asked verification
(engine diff = redesign landings only; six store-count corrections; the #326 per-stream anchor
restated at L3 step 33) and the corrected re-delivery. Any extension is a NEW owner word.

## THE SEAM'S ROAD (updated at v582)
1. ~~Round-21 ingest + movers snapshot~~ **DONE 2026-08-06** (txn 4a7d259; pattern for R22+: the
   catchup verb per the v582 register entry; the owner may run it himself — one-pager pending).
2. ~~#344 merge + engine_head re-pin~~ **DONE 2026-08-06, owner word "Merge 346"** — the
   declared-refit lane (RL_V0SURF_REFIT=1) is OPEN; silent refits stay red; engine_head `8f0e3eb1`.
3. ~~#338 implemented~~ **DONE 2026-08-06, owner word "Fire 338"** — the honest book of record is
   committed (engine/rl_after/s4_matrix_M1v7.json, meta: store 37ced3ce · engine 8f0e3eb1 · n 2647);
   era parity exact (460 pairs); the no-arb/per_entrant lineage REISSUED on the rule same day
   (docs/evidence/noarb_338_2026-08-06/, v585) — tenure-provisionality lifted; #336 remains open.
4. **#336 bust-inclusive variant** on the honest book → ONE side-by-side to the owner. His single
   queued decision.
5. **#332 addendum** (#306 comment 5186108632) · the #333 memo absorbs the #336 result · #334
   stage B rides the post-ruling re-derivation.
## RUNNING THIS SEAT WELL — including the FABLE BUDGET (owner word 2026-08-06)
**The seam runs on Fable; spend Fable ONLY on judgment** — rulings, verifying the two-or-three
deciding figures, and talking to the owner. Everything mechanical (searches, extraction, builds,
table-making, audits' legwork) goes to OPUS subagents with tight checklists — never Fable, never an
inherited default (charter law; a prior session burned ~1.7M Fable tokens). Keep owner replies to
~one screen of short plain sentences; his confusion at dense wording is a recorded failure mode.
His casual questions are the project's best QC (eight catches in two days); verify before agreeing
OR disagreeing; file his words the same hour. Threads by comment id only; the register by pointer
(grep for N-numbers); audits read code, rehearsals measure it — never skip the loop.

## ENVIRONMENT CARRIES (inlined in full — nothing dangles)
Pinned venv: `bash setup_env.sh` → `/root/rl_venv312` (Python 3.12.3 · numpy 2.4.4 · scipy 1.17.1 ·
sklearn 1.8.0 · openpyxl 3.1.5). Prepared workspace: `RL_VENDOR=<tree>/vendor bash <tree>/bootstrap.sh`
(seeds `/home/claude/rl_workspace` from the tree it runs from; Guard 5 asserts the pinned store).
Canonical build (byte-reproduced the boards all era): cd `/home/claude/rl_workspace/rl_after` &&
`rm -f rl_app_data.json` && env with single-thread BLAS (`OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`),
`PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor`, `RL_CONFIG_MODE=gate`,
`RL_REPO=<tree>`, `RL_FV=<tree>/engine/forward_valuation`, `python3 rl_export.py`; then
`s4_matrix_M1v7.py`; then `one_source_selftest.py` (expect 145 PASS/0 FAIL). Full recipe:
`docs/evidence/act_326_2026-08-06/RUN_COMMANDS.md` (its inline expected board md5 `864b6726` is the
PRE-#334 rehearsal figure — the adopted pin is `827fb1fd`; the pair is named below); #334 recipes:
`docs/evidence/act_334_2026-08-06/`.
N32 payload recipe: `{str(pick): int(round(v))}` over the ladder's `curve` object, `json.dumps(...,
sort_keys=True)`, md5. PEN MECHANICS: register line 1 is the header; edit the version stamp near
char 88 SAME LENGTH (`v585 2026-08-06` → next); insert the entry before the ` · SEAM v540
(2026-07-29)` marker; asserts: line count 8,438 unchanged · growth == entry length · one new stamp ·
docs-only diff; commit `supervisor-seat <supervisor@seam.local>`; branch → PR → rebase-merge →
re-verify main BY CONTENT (the branch may need `git rebase origin/main` first — merged twins drop
patch-identical; force-with-lease is sanctioned for already-merged history). Board attribution
baseline pair: `864b6726` (pre-#334) → `827fb1fd` (adopted). The book (`s4_matrix.json`) is
id()-keyed — never byte-reproducible, never claim its bytes. The owner-facing pages (board review ·
cohort tables) are claude.ai artifacts on the owner's account; rebuild recipes = the committed
instruments + the #333-filed conventions. The Track B pack's build tree lives only in the delivered
zip; its authored files (README_FIRST · PROJECT_LAWS · RECIPE_STATUS) are reconstructible from the
v579 register entry + the governing documents.

## THE SEAT'S STANDING ORDERS (post-cut)
0. Onboard per the charter order (charter — later amendment blocks SUPERSEDE earlier text in place
   — then primer v4 IN FULL, then this file, then the register by pointer). Plain vocabulary.
   Opus-only subagents.
1. Verify THE ADOPTED IDENTITIES above with your own commands; N35-classify your box before
   trusting any fitted figure (value-path: byte-reproduce the board).
2. Next act: ASK THE OWNER for the round-21+ scores and drive road step 1. Steps 2–4 follow in
   order; his single queued decision is the #336 side-by-side at step 4.
3. Never present on a superseded basis; never deliver under pressure.
