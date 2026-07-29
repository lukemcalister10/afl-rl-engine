# CURRENT STATE — the incoming-seat read · v30 · supervisor pen · 2026-07-29, register v538

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

*Replaced wholesale each pen. Accurate 2026-07-29, register v538, written against main `3df3a859` — this
pen lands on top of it, so `main` will be one commit ahead. That is expected, not staleness.*

## WHAT JUST LANDED

**#262 is merged** (PR #272, rebase-merge): the vocabulary is KPF/KPD/SD/SF/MID/RUCK repo-wide;
**11,264 of 11,264 per-season eligibility rows** are in the store; store `e3aaba77` → `5d6e56d0`, board
`750446d7` → `3d4e2e50` — byte-identical to the rename-only board, zero value/rank movers across 103,146
cells, proven seat-local and by CI's cross-environment rebuild. v0surf was refit twice through the declared
`RL_V0SURF_REFIT` lane; the frozen set is now `8faa737b`/`b08a5a7e`. **The 62 position-field edits are
DEFERRED to #271** (owner word, Addendum 5 R3-1; the write-then-revert history is preserved in the branch).
The complete ruling record is **#262 Addenda 1–7** — read them before touching anything near the landing.

## THE INCOMING SEAT'S FIRST TASKS

1. **Fire #271 on the owner's word.** The re-derivation directive is FILED and seam pre-fire AUDITED (both
   on issue #271). The audit's two corrections bind: only the CURRENT-season bar moves to eligibility (the
   future blend stays referee-era), and **the candidate is the branch** — fully self-consistent with its own
   re-pins, never merged until the owner's adoption word. Two v0surf re-bakes are expected (stage A: the 62
   edits; stage B: the derivation). Attribution baseline is `3d4e2e50`. The owner's fire word should also
   settle the pool statistic (SCAR default). The executing seat is fresh and cold.
2. **Verify #271's hand-back by re-running only what decides:** stage-A movers = exactly the 62 edits'
   footprint; the both-directions exclusion checks (including the pooling-term channel) shown failing when
   lifted; the candidate branch self-consistent (its CI green modulo knowns); no shipped identity moved on
   `main`. Diff any long-lived branch against current `main` before merging it.

**Sequence: land (#262 ✓) → re-derive (#271, fire-ready) → owner adoption → referee project (#270 opens
it) → ITEM 412.** The adoption commit is: merge the candidate + migrate the UI pair + delete the
`held_candidates` declarations + the baseline column label — and it REOPENS the owner's live ingest lane.

## CI — three of four green; the last red, precisely

Final Integration is red on **`club_curve_provenance` alone** (9/35, same count as before the landing, the
mechanism verified different: most cases now halt on the board-id ring-fence — bundle `8a38cca4` vs release
board `3d4e2e50`, declared in `held_candidates` — with the old no-price-for-pick-70 assertion unreachable
behind it). It resolves at adoption. The counting-rule suite (24/24) still asserts OLD vocabulary and
passes, because it tests the deliberately-lagging UI pair — it flips at adoption. CASE1's `checked=0` red
is **anti-vacuous** (a coverage clause, `club_curve_provenance.test.py:186`), not the vacuity class.
Standing behaviours unchanged: Kako store anchor STALE at R21 by design; `invariant_proof.py --adoption`
is the adoption lane; the six `proof-*` jobs are manual-dispatch only.

## OWNER ACTS OUTSTANDING

1. **Fire word for #271** (+ pool statistic: SCAR unless he says otherwise).
2. Clicks: delete branch `claude/issue-262-supervision-hjmixs` · close #262.
3. **The 16 trades** (R4-1): edit `docs/inputs/AFFL_Player_Locations.csv` via his own lane whenever;
   `ownership.js` catches up at adoption. Accepted caveat: a round baked pre-adoption carries stale teams
   for the 16 (`round_movers.py:279`); self-corrects after.
4. #269's three shaping questions (the `+250*` asterisk · the 2027 blend's ⅓ anchor · round-5 zero vs half).
5. v1.1 referee amendment — one read: `docs/referee/AMENDMENT_v1_1_DRAFT.md`.
6. Real-iPhone check of `ui/index.html` (#139 item 22).
7. Adoption era: adoption word + baseline column label · the baked-pick-prices decision.
8. Repo hygiene go-word: measured 2026-07-29 — 129MB/2,252 files; ~52MB zero-reference archive candidates;
   ~8.5MB of session evidence is CI-wired and excepted by name (enumeration in the seam session record).

## FILED / PARKED — do not start

**#269** clubs-tab re-valuation (owner spec verbatim; supersedes #139 item 8; fires on its own directive).
**#270** free-hit value — the referee project's opening question (report-only market study first
deliverable; until then the "working system" is today's bars, carried unchanged). **UI wave** (#139 items
2–5, 9–18): draft post-adoption to avoid churning the fenced UI pair; the owner picks items. **#146** (body
inverted at D1 — do not execute as written). #139 items 6, 7, 19 parked; item 8 superseded by #269. Track D
· the conservation gate (`gate_f5.py` cannot be wired as written) · the deeper bar-construction questions
(referee).

## KNOWN CARRIES

**1,271 of 1,924 scoring players lack a 2026 row** — each lands an eligibility-less season on first
appearance until #271 fixes BOTH season-row writers (`round_apply.py:182` and the independent
`merged_entry` construction in `staged_apply.py:178-185` / `score_ingestor.py:224-228`). The owner's live
ingest lane (`ingest_inputs.py`) is **fail-closed under the hold by design** (board-id ring-fence) and
reopens at adoption. `affl_team` is legacy-with-one-reader (`round_movers.py:279`); retiring it is an owner
act. Carried by ruling R4-2, rewritten at #271's bake: the stale `sig 76498b5a` prose in
`one_source_selftest.py` and the `_build_book_xlsx.py:157` label. Definitive residual old-vocab enumeration
(Addendum 7): six frozen movers round bundles + the ycred prose note + the xlsx label — era data and prose,
none functional.

## RUNNING THIS SEAT WELL — learned the expensive way, owner-endorsed

- **Verify hand-backs by re-running only the two or three measurements that would change a decision**;
  delegate the reading (report ingestion, log pulls, bulk byte-compares) to hands.
- **Never pull raw GitHub API payloads into context** — spill to a file and parse, every time.
- **One register pen per boundary**, not per event. Docs-only pens **merge immediately** on their
  structural asserts. Code diffs wait on exactly the checks they can move.
- **Every fired directive is handed to the owner as a paste-ready relay in chat**; state model/effort only
  when deviating from Opus 5 at default. Call chats by the owner's names, not issue numbers.
- **Report in plain breakdowns**: what happened, what the owner must know or decide, with context. Lead
  with the outcome. No register-dialect.
- **Owner words seal promptly and on the issue first** — chat carries no authority; the pen follows at the
  boundary. A cancelled CI run is not a red. Every count names its denominator. Hands freely for reading;
  never delegate a load-bearing measurement; never run engine builds in parallel.
- **Check your own test can fail before believing it.** This cycle added two concrete instances: a
  mid-batch `git fetch` silently repoints FETCH_HEAD — **verify against explicit refs
  (`origin/<branch>`), never FETCH_HEAD** (this seat measured main believing it was the branch; caught
  because the failures were too perfect) — and **hyphenated vocabulary patterns need word boundaries**
  (`K-DEF` matches RANK-DEFICIENT; the spelling-phantom class's third occurrence).
- Effort scales with what a mistake costs to reverse.

## ENVIRONMENT CARRIES

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Bare `python3` is 3.11 against a cp312-pinned lock; system pip is PEP 668-blocked.** Build a 3.12
  venv, `pip install --require-hashes --only-binary=:all: -r requirements-lock.txt`, then
  `RL_VENV=<venv> bash bootstrap.sh`. Do not weaken the pin.
- **`v0surf` HALTs on an unknown config signature — that is the design.** The ONE regeneration lane is
  `RL_V0SURF_REFIT=1` at a deliberate bake. Never restore a fallback or widen the frozen set.
- **After any rebase-merge, a long-lived seat branch must be recreated from `origin/main` by
  cherry-pick** — rebase-merges rewrite SHAs. `git cherry` proves what is genuinely new. **Always diff a
  PR against current `main` before merging it.**
- **`sibling_repin` rewrites pins on every board move** and raises unless six structural tokens each match
  exactly once. `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` is a live build input
  inside a session directory — session-archive exemptions must except it (the CI-wired session set is
  enumerated in the 2026-07-29 hygiene audit).
- The register header is **one ~400KB line** — read by pointer with a windowing script, never `head` or
  `cat`. The Actions API exceeds output caps — spill to a file and parse.
- **Pens**: branch → PR → rebase-merge; the seam merges its own PRs; ref deletion is owner-only.
  Mechanics: bump the version digit in the line-1 stamp (`supervisor pen · vNNN date · PEN:`) and insert
  `· SEAM vNNN (date) — <entry>` immediately before the trailing `· prior: ITEM 407`. Assert pre-commit:
  line count unchanged, byte growth equals entry bytes, single stamp, every prior entry intact, docs-only
  diff — and **measure in one unit**; the line's byte and character lengths differ by thousands.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
