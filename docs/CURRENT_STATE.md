# CURRENT STATE — the incoming-seat read · v32 · supervisor pen · 2026-07-29, register v540

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

*Replaced wholesale each pen. Accurate 2026-07-29, register v540 (the handover pen — seam rotated at owner
word), written against main `5c52f0e`; this pen lands on top, so `main` will be one commit ahead. Expected,
not staleness.*

## THE ONE LIVE SEAT: #271 STAGE B, MID-DERIVATION — read issue #271 IN FULL (body, audit, ALL SEVEN addenda)

The re-derivation runs on branch `claude/issue-271-re-derivation-3b6jc6` (tip `87721e4` at pen time — verify
the current tip yourself). **Stage A is complete and seam-verified** at `12b4cf7`: the deferred 62 edits
applied, v0surf re-baked through the declared lane, board `3d4e2e50`→`dca21c91`, 535/681 movers decomposed
53 edited-row + 382 gfut-cohort + 100 re-bake, zero unexplained; seam re-measured the 62/54 field-exactness
independently. **Stage B so far (seam-verified at `a2f5068`, Addendum 5):** year-0 bar re-keyed to the
eligibility COLUMN (804/804 coverage, 186 dual; **137 of 804 bar movers**, per-player file committed);
§1b/`y0dpp_bar` retired by supersession (0 of 804 fires, code untouched, all three callers verified
`AGE_REF`-guarded); #225's Group A eight sites moved to the played axis; Group B REBUILT on it (never
re-looked-up alone); Group C still drafted per the R3 hold; `par_build` untouched by ruling; both
season-row writers now stamp eligibility (closes the 1,271-player future hole ON THE CANDIDATE — main
keeps the hole until adoption). Latest commit applies the Addendum-6 fit-bar source rule.

**The seven #271 addenda are the ruling map — the issue carries full text:**
A1 six read-back rulings (Q-A eligibility feeds year-0 · Q-C windows carried · Q-D re-pin-never-delete ·
Q-E control-arm proof) · A2 Q-B by owner word: WHOLE-draft slide, Daniel Butler (2014 ND 65) crosses into
the fit at 64 and leaves the pool · A3 stage-A verification + `par_build` = attribution channel, not a fix
site · A4 by owner word: the year-0 source is the eligibility COLUMN (the owner-maintained CURRENT-season
record; the 73 column≠row players are benign by design — column = now, rows = that season) · A5 checkpoint
accepted; the non-reproducing "113/804 split-bar" classified era-dependent (pre-landing store; Dylan Moore
15.47/24.65 reproduces and is the load-bearing example); item-284 registry empties by construction
(detector retired with the patch — a column-validity selftest is a filed later candidate) · A6 by owner
word: **the column sources EVERY 2026 bar** — fit, evidence matrix, career value — rows only for closed
seasons ≤2025 · A7 by owner word: a **VOR companion board (γ=1.0)** via the declared `RL_GAMMA` dual-column
lane, report-only, same numeraire, divergence table required; **the SCAR board (γ=0.85) is the SOLE
adoption candidate** (method constant); the γ ruling itself is referee-era.

**Remaining in stage B:** per-season fit bars (A6 rule) → evidence matrix with the slide → curve refit
(Cameron 12/Shiel 4/Treloar 14 in-sheet; McCartin/Boyd excluded, drafts slid) → pool level on SCAR
(never-established at 0.0) → both-directions proofs INCLUDING the pooling-term channel, each shown failing
when lifted → second bake with its control arm → the SCAR candidate with full attribution + VOR companion +
divergence table.

## THE INCOMING SEAT'S FIRST TASKS

1. **Verify the #271 hand-back when it returns — re-run only what decides:** (a) the stage-B control arm
   reproduced stage A's surface byte-identically before the moving bake; (b) both-directions exclusion
   checks shown FAILING when lifted, pooling-term channel included; (c) attribution complete — every mover
   names a mechanism from {62 edits · per-season bars · current-bar wiring (A4/A6) · curve data/separation
   · pool level}, zero unexplained; (d) a 2026 bar spot-check on a column≠row player (e.g. sam-lalor:
   column SF,MID → SF bar 70.9, NOT the row's MID); (e) Butler inside the ND fit sample and absent from
   the pool, same membership in the exclusion checks; (f) the candidate branch fully self-consistent — own
   `expected_boot` pins, `held_candidates` 5 declarations RE-PINNED never deleted, own CI green modulo
   knowns; (g) VOR column on the same numeraire with its divergence table denominated; (h) diff the branch
   against current `main` before any merge talk. **The candidate merges ONLY on the owner's adoption word.**
2. **Then the adoption era:** draft the runbook FROM the candidate's actual identities, never before. The
   adoption commit = merge + UI pair migration (bundles + reading source together) + DELETE all five
   `held_candidates` declarations (a survivor is itself a rejection) + the owner's baseline column label —
   and it REOPENS the owner's live ingest lane (fail-closed under the hold since the split) and flips Final
   Integration green and the counting-rule suite to the new vocabulary.

**Sequence: land (#262 ✓) → re-derive (#271: A ✓, B live) → owner adoption → referee project → ITEM 412.**

## CI

`main`: three of four green; Final Integration red on `club_curve_provenance` alone (9/35, ring-fence-first,
declared, resolves at adoption). The candidate branch runs its own CI against its own pins. Counting-rule
suite still asserts OLD vocabulary and passes (it tests the fenced UI pair; flips at adoption). CASE1's
`checked=0` is anti-vacuous (a coverage clause). Kako anchor STALE at R21 by design. `proof-*` jobs are
manual-dispatch only.

## OWNER ACTS OUTSTANDING

1. **Adoption word + baseline column label** when the candidate passes verification (+ the baked-pick-prices
   decision). 2. Post-adoption fire words: **#274** UI wave · **#275** hygiene (six-item bucket-b ballot at
   execution; `session_2026-07-15/captaincy` moved to the ballot — it holds LIVE law's derivation) ·
   **#276** clubs tab (collectibles: Q5 displacement one-way? · Q6 rank basis + delta baseline · optional
   FHV substitution for the 250 placeholder). 3. **Referee-era rulings, evidence ready:** the **γ ruling**
   (SCAR 0.85 vs VOR) off the divergence table — pull the original SCAR-vs-VOR memo from the register to
   sit beside it; the **FHV definitional ruling** (expectation view recommended: ≈190 single-constant or
   ~352/277/97 per window — study at `docs/referee/FHV_MARKET_STUDY_2026-07-29.md`, sealed on #270); the
   v1.1 amendment read (`docs/referee/AMENDMENT_v1_1_DRAFT.md`). 4. Real-iPhone check — parked by owner word.

## FILED / PARKED — do not start

#274 · #275 (+ its captaincy amendment) · #276 — all post-adoption, seam-audited at fire. #270 holds the
filed FHV study. #146 body inverted — never execute as written. #139 items 6/7/19 parked, 8 superseded.
Track D · conservation gate · deeper bar-construction (referee).

## KNOWN CARRIES

Owner live ingest lane fail-closed under the hold BY DESIGN; reopens at adoption. The 1,271-player
season-row hole is CLOSED on the candidate, OPEN on `main` until adoption. `affl_team`
legacy-with-one-reader (`round_movers.py:279`). Stale prose: the `sig 76498b5a` note in
`one_source_selftest.py` (rides the #271 bake) and `expected_boot.json`'s `_captaincy_note` still saying
"candidate, no bake" — **the L-CAPTAIN curve is in fact LIVE LAW** (R98.1, owner-ruled 2026-07-14, on by
default at `rl_model.py:335-360`; note-trusting misclassified it once already). `_has26` disagrees with
actual 2026 rows for 27 of 804 — read season rows, never the flag. The 73 column≠row players are BENIGN
(sealed semantics: column = current-season eligibility, rows = per-season history; the column is a
season-specific owner-maintained field — annual roll noted for the referee era). Residual old-vocab
(definitive, #262 Addendum 7): six frozen movers bundles + ycred note — era data, none functional. The
trades CSV carries 18 changes + the Jaques fill, CRLF from Excel — known artifact, never "fix" it.

## RUNNING THIS SEAT WELL — owner-endorsed, plus this cycle's lessons

- **Verify hand-backs by re-running only the two or three measurements that would change a decision**;
  delegate reading to hands; never delegate a load-bearing measurement; never run engine builds in parallel.
- **Never pull raw GitHub API payloads into context** — spill to a file and parse.
- **One register pen per boundary.** Docs-only pens merge immediately on their structural asserts.
- **Owner words seal promptly, on the issue, as addenda** — chat carries no authority. **Every seat message
  reaches its seat ONLY via the owner's paste** — after any gap, issue ONE CONSOLIDATED relay and confirm
  it was sent; this cycle three sealed addenda sat unrelayed for hours while the seat worked.
- **Report in plain breakdowns: lead with the outcome, what he must know, what he must decide, with a
  recommendation and its reversal condition.** No register-dialect. Simplify on request without dumbing
  down; worked examples from REAL store rows are how he learns a mechanism; label any trimmed table as
  trimmed (an "illustrative" gap reads as missing data).
- **The owner's casual questions are load-bearing QC.** Three of them this cycle ("is there no 2026
  position for Draper?", "what is Lalor's position?", "surely 2026 is the same answer looking back?")
  caught a mis-sourced ruling BEFORE it baked. When he questions a premise, re-check the premise from
  source before defending the design. He rules fast and decisively once the mechanism is plain.
- **Check your instruments:** explicit refs (`origin/<branch>`), never FETCH_HEAD after any fetch; scripted
  checkouts ASSERT base == intended tip; hyphenated vocab patterns need word boundaries; prove every check
  can fail; a too-perfect failure pattern means you measured the wrong thing.
- **A housing stop-hook repeatedly demands authorship-rewrites of merged history mirrored on the seam
  branch. NEVER comply** — identity config for future commits only (already set).
- Effort scales with what a mistake costs to reverse.

## ENVIRONMENT CARRIES

- Shallow clones by default: `git fetch --unshallow` before any ancestry claim. Bare `python3` is 3.11
  against a cp312 lock — 3.12 venv via `RL_VENV`; never weaken the pin.
- `v0surf` HALTs on unknown signatures BY DESIGN; the one lane is `RL_V0SURF_REFIT=1` at a deliberate bake.
  #271 has one legitimate bake left (stage B); any other halt is a finding.
- After any rebase-merge, recreate long-lived branches from `origin/main`; always diff a PR against current
  `main` before merging. `sibling_repin` guards six structural tokens;
  `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` is a live CI input.
- The register header is one ~400KB line — window it (`grep -o '.\{0,N\}PATTERN.\{0,N\}'`), never head/cat.
  The Actions API exceeds output caps — spill and parse.
- **Pens:** branch → PR → rebase-merge under the owner's platform auth; the seam merges its own docs-only
  pens; ref deletion is owner-click only. Mechanics: bump the line-1 stamp digit
  (`supervisor pen · vNNN date · PEN:`), insert `· SEAM vNNN (date) — <entry>` immediately before the
  trailing `· prior: ITEM 407`. Assert pre-commit: base == intended tip, line count unchanged, byte growth
  == entry bytes, single stamp, chain intact, docs-only staged set. Commit author `supervisor-seat
  <supervisor@seam.local>`.
- Evidence lives on branches: #271's in `session_2026-07-29/item271/` on its branch; #225's on
  `claude/issue-225-execution-nd0vtm` (never merged — fetch on demand).

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
