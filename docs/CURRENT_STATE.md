# CURRENT STATE — the incoming-seat read · v95 · supervisor pen · 2026-08-07, register v605

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
(v95 · supervisor pen · 2026-08-07, register v605 · STAGE 5 FIRED with ADDENDUM 1 (the
RECALCULATION LAW + stage-6 partial intensity, owner words 5215167494); conformance audit +
stage-6 cross-section measurement running at the pen; this version is the thorough
handover-quality pass the owner ordered while waiting. Read the v604 register entry IN FULL
before touching stage 5 — the design loop's two NOT-FIT audits and three measurement rounds are
the ground. Primer v7 first.)

## THE ERA: ADOPTED. Target RULED 1.40. STAGE B FIRED 2026-08-07 (comment 5210606449) — EXECUTING.
- **ADOPTED 2026-08-06** (owner word; release-transition register entry 4 at round 20). Landed
  since, all owner-worded, all on main: **round 21** applied (409 scores, txn catchup pattern) ·
  **#344** the declared-refit lane (RL_V0SURF_REFIT=1 passes, silent stays red) · **the Kako 2026
  anchor retired** ("Kako is now correct - 12 at 42.75. Retire the anchor.") · **#338 minimum
  tenure IMPLEMENTED** (book emitter; board untouched; era parity exact — 460 pairs, BOOK lineage, register v584 P5; the no-arb sheets' pair values are the per_entrant lineage, a different population) · **the no-arb
  tables and the owner's cohort artifact reissued on the #338 basis** · **#336 RULED: ADOPTED**
  (the amendment-3 form, correctness grounds, ships with stage B). **Track B**: cut, re-cut simple
  on owner word (store + one recipe), verified, delivered; any extension is a new owner word.
- **THE CURRENT IDENTITIES (verify with your own commands; N35-classify before trusting any
  fitted figure — value-path: byte-reproduce the board):**
  store `37ced3ce45914e6feb00d27e26922e9a` = `engine/rl_after/rl_model_data.json` · board
  `113b36f898a32363c49c2a62fb809f4b` = `data/rl_build/rl_app_data.json` · engine_head `8f0e3eb1…`
  = `engine/rl_after/_merged_recover.py` · rl_model `33f94073…` = `engine/rl_after/rl_model.py` ·
  curve payload `df766dff…` (N32 recipe over the `curve` object of
  `engine/rl_after/pvc_curve_v2.json`; file md5 `988135ef`) · surface `d594dc03…` = `data/v0surf.pkl`
  · balanced_board_md5 `123deccb` current pin (expected_boot.json; moves with round advances; the
  immutable present-lens anchor is `06d8af60` — the older "4939d740 present-lens anchor" note was
  a stale role-conflation, corrected v595) · season round 21
  (progress 0.88) · **SELFTEST EXPECTATION: 144 PASS / 0 FAIL** (the Kako 2026 anchor retired by
  owner word — every older "145/0" note is superseded). Movers attribution chain: `827fb1fd`
  (the adopted board, registered as out-of-round column `redesign-adoption-6-8` after round 20) →
  `113b36f8` (round 21). Suites: movers 66/66 · transition 39/39 · preflight 5/5.
- **EXPECTED, NOT DRIFT:** `ui/release_pick_curve.json` still stamps `curve_source_store_md5 =
  f1e8c9fe` (pre-completion) — #334 STAGE B re-derives it. `docs/evidence/act_326_2026-08-06/
  RUN_COMMANDS.md`'s inline expected board `864b6726` is a pre-#334 rehearsal figure — the live
  pin is `113b36f8` now.

## THE OWNER LAWS (2026-08-06 unless noted; primary copies on the named issues)
- **Monotonicity + the ADOPTED #336 FORM:** a strictly worse career never produces a better-looking
  baseline. Adopted form (supersedes "P(establish)×level" phrasing): anchors read bust-inclusive
  E[level | ESTABLISHED] (de-survivored); **no probability discount at any anchor** — the forward
  band already charges establishment failure IN FULL (measured 0.7077 vs 0.7075); resolution is
  smooth (the engine's own evidence fade; no six-game cliff); the v3.4 clamp is retired. Ships with
  stage B; held on branch `variant/336-bust-inclusive` @ `3bbc688` until then.
- **The two-lever framing (owner words, verbatim):** *"the way to address the 1.57 was either
  established players should be worth less, or picks, and year 0/1 players as a byproduct, worth
  more."* Both levers go OPEN to the #333 memo — the survivorship route to lever one is measured
  weak (hump 1.572→1.535 fully honest); the proven-player credit machinery and year-0 re-teaching
  are untested. Never present either lever as pre-decided.
- **Minimum listing tenure (#338, IMPLEMENTED):** ND 1–20 → 4 · 21–40 → 3 · others → 2; own data
  extends; known facts override; evidence-less years inside tenure are LISTED sitting-out years.
- **Presentation (#333):** owner-facing material is current-basis end to end or it does not ship;
  superseded views only as labeled baselines beside the current. Owner frustration is DATA, never a
  trigger. Every number names its quantity, basis, denominator. Plain vocabulary.
- **His casual questions are the project's best QC** — two of today's became binding amendments
  (the Robey catch; the resolved-establishment catch). Verify before agreeing OR disagreeing; file
  his words the same hour.

## THE ROAD (in order)
1. **EXECUTE STAGE B (FIRED 2026-08-07).** The governing chain on #334: DIRECTIVE (comment
   5210366916) · pre-fire audit, fit-to-fire-after-amendments (5210507691) · ADDENDUM 1 closing
   all 17 findings (5210513069) · ADDENDUM 2 + THE FIRE WORD, owner words verbatim (5210606449).
   Ruled target 1.40 (#333 comment 5210304078). Binding terms: BRANCH-HELD landing — nothing
   merges, no attribution column registers before the owner's side-by-side word · per-pick
   re-anchor TAUGHT FROM DATA, uniform decree BARRED · no even steps (front-loaded-increments
   assert) · no forward escalator (target-perturbation byte-identity test) · three return-
   triggers (yr1/2 ordering; yr1-to-peak vs shipped 1.400 — expected LIVE, the #336 layer alone
   measures 1.503; top-end ≥~3×) · max two declared-refit iterations, band [1.35,1.45] at the
   named peak year on a re-emitted matrix, distance-to-1.40 always printed · per-row attribution
   residual ≤1 board point · credits-off ablation never baked. OWNER DELIVERABLE MINIMUM
   (Addendum 2): before/after no-arb tables WITH per-entry-year view (N=0..5) · full before/after
   board xlsx (old/new/abs/rel + per-stage attribution + 64 pick rows) · REACTIVITY LANDS
   (required, was exploratory) with every moved player enumerated + the pedigree-pair probe.
   EXECUTION STATE (v598): fit-class gate PASSED · STAGE 1 LANDED @ ad50dad (board de5110bb
   byte-matched the amend3 control; selftest 144/0) · **NEW PRODUCT LAW (owner ruling 2026-08-07,
   #334 Addendum 3, comment 5211125357): NO ERA NORMALIZATION — SuperCoach is scaled by
   construction (3,300 pts/match); store-mean era gaps are population-composition artifacts;
   the shipped `era[Y]` rescaling (2009–2025, in the seed engine) is REMOVED everywhere.**
   Stage 3's first run was HALTED mid-flight on the ruling (nothing committed); the era-adjusted
   stage-2 ladder was SUPERSEDED and reverted. ERA REMOVAL LANDED @ f7ae027 (v599, seam-verified:
   board f94e0778; 28 movers, all KPF, all cuts, ratio 0.998986; engine_head a0a20d6e; the strip
   complete incl. a duplicate _gate1 table and twelve diagnostic scripts). OPEN ONE-LINER: the
   STAGE 3 LANDED @ c0ea507 (v601; seam-verified incl. an independent recompute of the hump row):
   CONVERGENCE HIT FIRST PASS — era-free row 0.9657/1.1972/1.3528/**1.4324 peak yr4**, inside
   [1.35,1.45], distance +0.032; splits 1.4285 / 1.4384 both peak yr4; TOP-END Sheezel 10,668 =
   3.556×; front-loaded assert PASS; no-forward-escalator proven (target-perturbed board
   byte-identical). **RETURN-TRIGGER LIVE (condition b): yr1-to-peak 1.4833 > shipped 1.400**
   (yr1 ratio 0.9657 — best cohort buy-in is now end of year 1); goes to the owner on the
   side-by-side; stage 4 may move it. Identities on the branch: board 6c9f8d3a · ladder payload
   18203822 (p1=3000; numeraire s→s/1.1214, all player display ×0.8917, relativities exact) ·
   v0surf 9713ec6c (declared bake, 2 signatures) · entrant seal 5c38e8ba (re-sealed by its own
   rule) · selftest 143/0 (3 enumerated FROZEN-RULER re-points; the 144/146 count anomaly CLOSED
   as a counting-method artifact — assertion count never moved). Pre-existing branch red
   disclosed: ui club_curve_provenance (UI bundle still carries the release board — expected,
   branch-held). release_contract.json + club_valuation.js deliberately NOT re-pointed (they name
   the ADOPTED board; the owner's click moves them). Era-free basis notes (v600): era was
   near-neutral on the hump (1.5345 clean floor pre-re-anchor); deep frozen fits stay as-fitted,
   NAMED. STAGE 4 LANDED @ 44950de (v602): lam in `sitout_ev` pedigree-conditioned
   (RL_PED_BAR=0.5, model_config, fit-decoupling proven); Mraz 3358→2898; pair ratio 1.36→1.53;
   51 movers enumerated; board b490ae8b; band held 1.4322; yr1-to-peak 1.4910 (trigger still
   live). THE OWNER'S MRAZ CATCH (verbatim at #334 comment 5212567158): 2898 still excessive —
   seam-verified rank 56, 5.5× his pick, #3 KPD; structural (max dial leaves ~2500). His ruled
   form: SURPRISE-SCALED TRUST — small samples far from projection shrink toward the prior;
   near-projection players untouched (no-rebalance condition, proven ±25%/<1% on the
   enumeration); symmetric, continuous, fades with games; selection-rate proposal REJECTED
   (hits all young players). AMENDMENT 1 LANDED @ 0056ed5 + SIDE-BY-SIDE @ c05f214 (v603,
   seam-verified on the PUSHED bytes: board md5 b56bbdde exact, Mraz row 1585, board total
   652,183, matrix md5 b564b12e, hump independently recomputed, workbook stage sums re-summed
   804/804 exact): surprise-scaled trust at the same sitout_ev site — s=|log(e_full/
   anchor_full)| on the SAME discounted anchor leg the blend uses (s=0 ⟺ inert, a forced
   choice, disclosed) · unresolved share u=1−rho(gp)/rho(6) from the engine's own K=5.8
   evidence fade, u(6)=0 exactly (smooth handover at the bar) · composition ADDITIVE
   lam^(1+0.5(1−q)+SUR_W·s·u) · RL_SUR_W=5.0 in model_config (61 vars; dial=0 rebuilds
   stage-4 board b490ae8b BYTE-EXACT; fit-decoupling re-proven at dials 0/5/20, v0surf
   9713ec6c unmoved). MRAZ 2898→1585 = 2.99× pick 35's 530 (INSIDE the ruled 2–3×; whole
   chain 3847→1585, −58.8%); pair ratio 1.53→2.38; 45 movers (38 cuts, 7 lifts, all named,
   all thin-record path; 109 zero-game players byte-identical); board total −0.365%.
   NEAR-PROJECTION PROOF: 6 players in the ±25% band; continuous max |move| 0.657% PASS;
   INTEGER board FAILS BY ONE ROW (Artemis 193→191: −2 points where one point = 0.52% —
   granularity, filed as a failure anyway; RL_SUR_W=2.0 named as the integer-clean
   alternative, Mraz 2267). Band HELD 1.4321 peak yr4; **yr1-to-peak 1.4910→1.5068 — trigger
   (b) STILL LIVE and moved AWAY, reported straight, compensated nowhere.** Top-end 3.556×
   unmoved. Selftest 143/0 zero re-points. WORKBOOK (the concurrent assembly agent died
   uncommitted; the amendment hand built it FRESH): 5 sheets, players 804 rows × one delta
   column PER STAGE summing exactly to the total (the owner-ordered per-stage sheet); 3,344
   formulas verified in Python (LibreOffice broken in sandbox — disclosed, verifier shipped).
   Identities: engine_head bc45d773 · config 38a73675 · board b56bbdde · matrix b564b12e.
   THE REVIEW RULED (2026-08-07, all owner words verbatim on #334): baseline word "I'm happy
   with the current board" = b56bbdde IS the ruled baseline + surprise dial HELD at 5.0
   (5213766677) · **TRIGGER (b) UPHELD — the shape REJECTED** ("a loophole to tick success...
   Year 1 players being worth less than their picks does not make sense", 5213743952).
   STAGE 5 FIRED (5215125681): the QUIET-STARTER REPRICE, directive v3 (5215130236) — G
   taught once from the frozen baseline book over (continuous τ × games-at-pace × log-pick),
   sitout_ev anchor leg both sites, zero-games cells held at measured-honest (their clock is
   TRUE: median career peak 0.74× entry), quiet starters (287 of the 783-player deficit leg)
   repriced to measured futures (+40–60% anchor; landing yr1 ≈ 1.01–1.03, gate [1.00,1.04]);
   Mraz tolerance 3.0×→3.5–3.8× (owner slack); FRONT-LOADED assert = printed guide (owner:
   "a relic"); SEASON-ROUND clock + smooth-over-years + phase-out seasons 2/3 (owner laws);
   design loop on the record: v1 NOT FIT (5213853619) → pre-meas 1 (5214041025, pole channel
   dropped as wrong tool) → v2+pub-test amendment NOT FIT (5214209797) → pre-meas 2
   (5214400439, the three-class discovery). STAGE 6 QUEUED, its own directive after the
   cross-section measurement (running): the conditioned established-leg residual (yr1
   established 414 priced 1.229 vs discounted future ~1.40; owner reframe: teach it per
   pick/position/level, some cells already priced; combined trajectory ~1.07–1.11 satisfies
   his [1.04,1.13] ACROSS THE SEQUENCE). **ADDENDUM 1 to v3 (owner words, 5215167494), binding
   both stages:** THE RECALCULATION LAW — G and any stage-6 premium are STATE FUNCTIONS,
   re-derived every build from the record-to-date (year-2 treatment reads year-1+2 cumulative
   evidence against that intersection's measured futures, at phase-out weight), NEVER a stored
   per-player boost; probe gate: a synthetic year-2 player's G-contribution must respond to
   his year-2 games. Teaching reads CUMULATIVE career games where eff-n supports, coarser
   axes disclosed where thin. Stage-6 INTENSITY IS PARTIAL by default expectation (dial =
   fraction of measured residual adopted; owner rules the level at its side-by-side, per band
   if evidence splits — his caution matches the evidence softness: engine-lensed,
   completion-optimistic). RUNNING AT THIS PEN: the v3 conformance audit (light,
   non-authoring) and the stage-6 cross-section measurement (X1 residual surface by
   pick×pos×perf-tercile×age · X2 yr-2/3 extension+fade curve · X3 age axis · X4 honesty
   checks). Build fires on the audit's clean return; seam verifies on pushed bytes; then the
   side-by-side. NOTHING merges, no out-of-round column registers before his word.
   Seat-conduct note (v604): twice said-before-done, corrected on the record; guard adopted
   (no completion/launch claim except in the message carrying the tool call). Evidence
   `docs/evidence/act_334B_2026-08-07/` on the branch; pre-measurement instruments' md5s and
   exact commands filed in the #334 comments (5214041025, 5214400439). Product commits:
   build-seat; the seam verifies deciding figures. Track B note (v597): PROCESS-light, not
   model-simple.
2. **THE SEQUENCE TO ADOPTION** — stages 1–4+a1 are BUILT (branch tip c05f214, ruled baseline
   b56bbdde); stage 5 is EXECUTING; stage 6 authors after its cross-section returns. Then: the
   refreshed side-by-side (workbook per-stage columns, no-arb before/after incl. per-entry-year,
   pub-test items printed — the ride table, the within-class path, the FRONT-LOADED guide
   reading) → the owner's adoption word → ONLY THEN: merge to main, the out-of-round
   attribution column (id sorting AFTER `redesign-adoption-6-8` under the registry's
   (after_round, id) tiebreak, registered BEFORE the next weekly apply), and the
   `ui/release_pick_curve.json` + release_contract re-points (they name the ADOPTED board).
   Parked items riding the act: thin-cell band steps · Dean-class held-surface boundary
   artefact · pool-entry knock-ons.
3. **Round 22** (weekly, not yet run as of 2026-08-07): the owner may run it himself — his
   one-pager is in his channel (queued for docs/) — or courier the file; the catchup pattern is
   the v582 register entry.

## RUNNING THIS SEAT WELL — the FABLE BUDGET (owner word 2026-08-06)
Spend Fable ONLY on judgment — rulings, verifying the two-or-three deciding figures, talking to
the owner. Everything mechanical goes to OPUS subagents with tight checklists (charter law; never
an inherited default). Keep owner replies ~one screen, short plain sentences. The auto-mode
content classifier false-positives on arming/guard vocabulary — rephrase plainly, never work
around it; on repeated blocks, stop and ask the owner. Verify hand-backs by re-running deciding
figures with your own commands BEFORE presenting anything. Present the number that answers the
owner's actual question (the yr1-to-peak lesson: relocating a gap is not closing it). Threads by
comment id only; the register by pointer (grep N-numbers); one pen per boundary, batched;
incremental CURRENT_STATE edits must assert count==1 per match or replace Part B wholesale (the
silent no-op caught at the v587 pen, repaired at commit 1e1a1cc, is the recorded failure).

## ENVIRONMENT CARRIES (inlined in full — nothing dangles)
Pinned venv: `bash setup_env.sh` → `/root/rl_venv312` (Python 3.12.3 · numpy 2.4.4 · scipy 1.17.1 ·
sklearn 1.8.0 · openpyxl 3.1.5); then PATH the venv, then `bootstrap_env.sh` (no-op check), then
`RL_VENDOR=<tree>/vendor bash <tree>/bootstrap.sh` (seeds `/home/claude/rl_workspace`; Guard 5
asserts the pinned store). Canonical build: cd `/home/claude/rl_workspace/rl_after` && `rm -f
rl_app_data.json` && single-thread BLAS env (`OPENBLAS/OMP/MKL/NUMEXPR_NUM_THREADS=1`),
`PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor`, `RL_CONFIG_MODE=gate`,
`RL_REPO=<tree>`, `RL_FV=<tree>/engine/forward_valuation`, `python3 rl_export.py`; then
`s4_matrix_M1v7.py`; then `one_source_selftest.py` (expect 144/0). Weekly rounds: the catchup verb —
`tools/round_entry/weekly_update.sh catchup --file N=scores/RN.csv` unarmed = preview;
`INGEST_SCORE_APPLY_ARMED=1 INGEST_SCORE_APPLY=<any> ... --approve` = apply; ledger blocks
double-apply; exit 6 → `finalize --round N` then `repair --round N`. N32 payload recipe:
`{str(pick): int(round(v))}` over the ladder's `curve` object, `json.dumps(..., sort_keys=True)`,
md5. PEN MECHANICS: register line 1 is the header; edit the version stamp near char 86 SAME LENGTH
(`v591 2026-08-06` → next); insert the entry before the ` · SEAM v540 (2026-07-29)` marker;
asserts: line count 8,438 unchanged · growth == entry length · one new stamp · docs-only diff;
commit `supervisor-seat <supervisor@seam.local>`; branch → PR → rebase-merge → re-verify main BY
CONTENT; after every rebase-merge the local branch needs `git rebase origin/main` +
force-with-lease (twins drop patch-identical; sanctioned for merged history). Product commits:
`build-seat <build@seam.local>`; both end with the Co-Authored-By + Claude-Session trailers. The
book (`s4_matrix.json`) is id()-keyed — never byte-reproducible; the committed book of record is
`engine/rl_after/s4_matrix_M1v7.json` (meta block carries its identity). The owner's cohort
artifact (claude.ai, updated to the #338 basis this day): pass its URL to the Artifact tool to
update in place; conventions printed on the page itself. Evidence trees this era:
`act_326_2026-08-06/` · `act_334_2026-08-06/` · `noarb_338_2026-08-06/` ·
`act_336_variant_2026-08-06/{,amended/,amend2/,amend3/}` ·
`act_334B_2026-08-07/{stage1,stage2,stage2_erafree,stageER,stage3,stage4,stage4_amend1,side_by_side}`
— all RETENTION-PROTECTED. Worktrees/workspaces on THIS box (ephemeral — container-bound,
recipes filed on #334): seam `/home/claude/seamcheck_landing` · amend1
`/home/claude/amend1_{landing,ws}` · pre-measurement `/home/claude/premeas_landing` +
`/home/claude/premeas_ws{,_v1,_v1f,_v2,_v3a,_v3b}`; a fresh box rebuilds any of them from the
branch + the filed commands.

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order (charter — later amendment blocks SUPERSEDE earlier text in
   place — then primer v7 IN FULL, then this file, then the register by pointer; the v604
   register entry IN FULL is mandatory before touching stage 5). Plain vocabulary. Opus-only
   subagents.
1. Verify THE CURRENT IDENTITIES above with your own commands; N35-classify your box
   (byte-reproduce board `113b36f8` via the canonical build — MAIN basis; the landing branch's
   b56bbdde is the act's ruled baseline) before trusting any fitted figure.
2. CHECK THE IN-FLIGHT WORK before anything else: stage-5 build state on
   `landing/334-stage-b` (was it pushed? seam-verify its deciding figures — yr1 landing vs
   [1.00,1.04], Mraz vs the 3.5–3.8× tolerance, the recalculation-law probe, kill-switch
   byte-identity) and the stage-6 cross-section (filed on #334 or still owed). The #334
   comment thread of 2026-08-07 is the governing record; every owner ruling of that day is
   quoted verbatim there.
3. READ-BACK to the owner and HOLD. His likely first words: the stage-5 side-by-side, the
   stage-6 intensity ruling, or round-22 scores.
4. Drive the road. Never present on a superseded basis; never deliver under pressure; never
   claim done before the tool call is in the same message; the owner's casual questions are
   load-bearing QC.
