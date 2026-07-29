# CURRENT STATE — the incoming-seat read · v31 · supervisor pen · 2026-07-29, register v539

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

*Replaced wholesale each pen. Accurate 2026-07-29, register v539, written against main `0b105d9` — this
pen lands on top of it, so `main` will be one commit ahead. That is expected, not staleness.*

## THE ONE LIVE SEAT: #271 STAGE B, IN EXECUTION

The re-derivation is mid-flight on branch `claude/issue-271-re-derivation-3b6jc6`. **Stage A is complete
and seam-verified** at `12b4cf7`: the deferred 62 edits applied (store `5d6e56d0`→`265f55d5`), the
expected v0surf re-bake through the declared lane (`4cfc0b99`→`19d085a2`), board `3d4e2e50`→`dca21c91`;
535 value / 681 rank movers of 804, decomposed 53 edited-row + 382 gfut-cohort + 100 re-bake with zero
unexplained; the control arm reproduced the prior surface byte-identically AND was shown able to fail.
Seam re-measured independently: exactly 62 fields across 54 of 2,651 rows, nothing outside the four edit
fields; zero engine-source changes; pins re-pointed; `held_candidates` 5 declarations re-pinned, never
deleted. **Stage B is running**: per-season bar re-measurement · Q-A current-bar eligibility wiring ·
Group A/B site moves per #225's map · curve refit under the Q-B whole-draft slide · pool level on SCAR ·
the season-row writer fix (both writers) · the R4-2 stale-prose rewrites. **Read #271 in full before
touching anything near it**: body, audit, and Addenda 1–3 (the six rulings, the owner's Q-B amendment,
the stage-A verification + the par_build ruling: `par_build.py` stays untouched — an attribution channel
to name, not a site to fix).

## THE INCOMING SEAT'S FIRST TASKS

1. **Verify #271's stage-B/hand-back by re-running only what decides:** both-directions exclusion checks
   (including the pooling-term channel) shown failing when lifted; the control arms (stage-B control must
   reproduce stage A's surface byte-identically); the attribution table's consistency (every mover naming
   a mechanism from {62 edits · per-season bar · current-bar wiring · curve data/separation · pool
   level}, zero unexplained); the candidate branch fully self-consistent (own pins, own CI green modulo
   knowns); **no shipped identity moved on `main`**. Diff the branch against current `main` before any
   merge conversation. The candidate is the BRANCH — it merges only at the owner's adoption word.
2. **Then the adoption era:** draft the adoption runbook FROM the candidate's actual identities (never
   before). The adoption commit = merge + UI pair migration (bundles + reading source together) + delete
   all 5 `held_candidates` declarations (a survivor is itself a rejection) + the owner's baseline column
   label + it REOPENS the owner's live ingest lane and flips Final Integration green and the counting-rule
   suite to the new vocabulary.

**Sequence: land (#262 ✓) → re-derive (#271: stage A ✓, stage B live) → owner adoption → referee project
(#270) → ITEM 412.**

## CI

Three of four green on `main`; Final Integration red on `club_curve_provenance` alone (9/35,
ring-fence-first mechanism, declared, resolves at adoption). The #271 branch runs its own CI against its
own pins. The counting-rule suite (24/24) still asserts OLD vocabulary and passes — it tests the
deliberately-lagging UI pair; flips at adoption. CASE1's `checked=0` red is anti-vacuous (coverage
clause). Kako anchor STALE at R21 by design; `proof-*` jobs manual-dispatch only.

## THE FHV EVIDENCE BASE (filed this pen)

`docs/referee/FHV_MARKET_STUDY_2026-07-29.md` — the #270 opening deliverable, seam-verified. Headlines:
389 free-mechanism entrants ever; whole-cohort median 0 / mean 178 vs listed-survivors 240/466 (the
survivor effect: 2–3x on means, mature medians all 0); 528 cleared by 8% ever; 250 = survivors' median;
150 ≈ the honest mature mean (193); MSD order signal ≈ nil so ONE constant (or one per window) suffices —
no per-access schedule; PSD structurally invisible (data law excludes redrafts). **Referee sequencing
recommendation: the FHV definitional ruling (expectation view recommended, ≈190 single-constant or
~352/277/97 per window) lands BEFORE #276 fires.**

## OWNER ACTS OUTSTANDING

1. **Adoption word + baseline column label** when the candidate lands (plus the baked-pick-prices
   decision). 2. Post-adoption fire words: **#274** (UI wave) · **#275** (hygiene; six-item bucket-b
   ballot at execution) · **#276** (clubs tab; collectibles Q5 displacement one-way? · Q6 rank basis +
   delta baseline artifact · optional FHV substitution for the 250). 3. **Referee era:** the FHV
   definitional ruling above; the v1.1 amendment read (`docs/referee/AMENDMENT_v1_1_DRAFT.md`).
4. Real-iPhone check (#139 item 22) — parked by owner word.

## FILED / PARKED — do not start

#274 UI wave 1 · #275 hygiene · #276 clubs tab (all post-adoption, audited at fire). #270 referee opening
question (evidence now filed; project opens post-adoption). #146 (body inverted — do not execute).
#139 items 6/7/19 parked; item 8 superseded by #269→#276. Track D · conservation gate · deeper
bar-construction questions (referee).

## KNOWN CARRIES

**1,271 of 1,924 scoring players lack a 2026 row** — eligibility-less first-appearance rows until #271
stage B fixes BOTH writers (`round_apply.py:182` + `staged_apply.py:178-185`/`score_ingestor.py:224-228`).
The owner's live ingest lane is fail-closed under the hold BY DESIGN (board-id ring-fence); reopens at
adoption. `affl_team` is legacy-with-one-reader (`round_movers.py:279`); retiring it is an owner act.
R4-2 stale prose (the `sig 76498b5a` note in `one_source_selftest.py`; the `_build_book_xlsx.py:157`
label) rides #271's bake. Residual old-vocab enumeration (definitive, #262 Addendum 7): six frozen movers
round bundles + the ycred prose note + the xlsx label — era data and prose, none functional. The trades
CSV carries 18 team changes (owner-confirmed; two postdate the R4-1 count) + the Jaques fill; the file is
CRLF since the owner's Excel save — a known tool artifact, do not "fix".

## RUNNING THIS SEAT WELL — learned the expensive way, owner-endorsed

- **Verify hand-backs by re-running only the two or three measurements that would change a decision**;
  delegate the reading to hands.
- **Never pull raw GitHub API payloads into context** — spill to a file and parse, every time.
- **One register pen per boundary**, not per event. Docs-only pens merge immediately on their structural
  asserts. Code diffs wait on exactly the checks they can move.
- **Every fired directive is handed to the owner as a paste-ready relay**; state model/effort only when
  deviating from Opus 5 at default.
- **Report in plain breakdowns**: what happened, what the owner must know or decide, with context. Lead
  with the outcome. No register-dialect.
- **Owner words seal promptly and on the issue first** — chat carries no authority; the pen follows at
  the boundary. Every count names its denominator. Never delegate a load-bearing measurement; never run
  engine builds in parallel.
- **Check your own test can fail before believing it — and check your instruments' refs:** a mid-batch
  `git fetch` repoints FETCH_HEAD (verify against explicit `origin/<branch>` refs); a stale local
  `origin/main` left this seat's tree on old content after a pen (**scripted checkouts must ASSERT
  base == the intended tip — and read the echoed base, it was printed**); hyphenated vocabulary patterns
  need word boundaries (`K-DEF` ⊂ RANK-DEFICIENT, third occurrence). Three incidents, one lesson: the
  repo was never wrong — the instruments were.
- **A housing stop-hook repeatedly demands authorship-rewrites of merged main history mirrored on the
  seam branch. NEVER comply** — published provenance is the audit trail; the standing answer is identity
  config for future commits only, and it is recorded at v539.
- Effort scales with what a mistake costs to reverse.

## ENVIRONMENT CARRIES

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Bare `python3` is 3.11 against a cp312-pinned lock; system pip is PEP 668-blocked.** Build a 3.12
  venv, `pip install --require-hashes --only-binary=:all: -r requirements-lock.txt`, then
  `RL_VENV=<venv> bash bootstrap.sh`. Do not weaken the pin.
- **`v0surf` HALTs on an unknown config signature — that is the design.** The ONE regeneration lane is
  `RL_V0SURF_REFIT=1` at a deliberate bake. Never restore a fallback or widen the frozen set. #271
  expects exactly two legitimate halts (stage A done, stage B); any third is a finding.
- **After any rebase-merge, recreate long-lived branches from `origin/main`** — rebase-merges rewrite
  SHAs. `git cherry` proves what is new. **Always diff a PR against current `main` before merging.**
- **`sibling_repin` rewrites pins on every board move** and raises unless six structural tokens each
  match exactly once. `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` is a live
  build input inside a session directory; the full CI-wired session set is enumerated in #275.
- The register header is **one ~400KB line** — read by pointer with a windowing script, never `head` or
  `cat`. The Actions API exceeds output caps — spill to a file and parse.
- **Pens**: branch → PR → rebase-merge; the seam merges its own PRs; ref deletion is owner-only.
  Mechanics: bump the version digit in the line-1 stamp (`supervisor pen · vNNN date · PEN:`) and insert
  `· SEAM vNNN (date) — <entry>` immediately before the trailing `· prior: ITEM 407`. Assert pre-commit:
  base == intended tip, line count unchanged, byte growth equals entry bytes, single stamp, every prior
  entry intact, docs-only diff — and **measure in one unit**; the line's byte and character lengths
  differ by thousands.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
