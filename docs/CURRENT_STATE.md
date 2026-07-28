# CURRENT STATE — the incoming-seat read · v3 · supervisor pen · 2026-07-28, register v508

**WHAT THIS IS.** The condensed read for an incoming seat, so orientation costs ~18KB instead of the
register header's 325KB. It carries *what is true now*, *what the owner actually wants*, and *where
the history lives*.

**WHAT IT IS NOT.** Not the record. `docs/OPEN_ITEMS_REGISTER.md` is the single durable list and
remains append-only and complete. **Where the two disagree, the register wins and this file is
wrong.** This is a derived view, in the same sense the board is derived from the store.

**THE DISCIPLINE THAT KEEPS IT HONEST.** Part B is **REPLACED WHOLESALE every pen, never appended
to**. Part A changes only when a new class is named. A derived copy kept in sync by hand goes stale
silently — that is the `club_valuation.js` fault of 2026-07-27, and this file is the same shape.

**Audited** by a bare cold seat against the register; five findings raised and all corrected in v2.

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
2. **The guards are the maintenance burden.** The panel check blocks every landing and needs hand
   re-pinning. The proof harnesses take ~86 minutes and are wired to nothing. The register grew until
   it broke the agents that must read it. Each was built to prevent imperfection and now costs more
   than it returns. **Before adding a guard, price its upkeep.**
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
| 7 | **Two-axis sibling sets** | enumerate what **reads** the changed field *and* what **stamps** the moved identity | v507 |
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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v508, main `85e39ee`.*

## WHAT THE OWNER WANTS — read this first, and work on these

Given directly 2026-07-27, in his order. **Nothing outside this list should be started without his
word.**

1. **Recalculate everything derived from the old store.** V0, the pick curve, priors, age curves —
   all fitted on the pre-restructure world. **Nothing downstream is trustworthy until this is
   re-derived, and nobody has measured what changed.** → **STAGE 1 IS FIRED**, see below.
2. **Establish the referee and optimise the model to beat the blind challenger.** The protocol is
   frozen and ready; **the harness that runs the scoring has never been built.** That is the only
   blocker. Build it *after* (1) or it scores against stale priors.
3. **ITEM 412 pricing** — **the owner is working this himself** (2026-07-28). Do not seat it.
4. **Round 20 scores + live local updating.** → **FIRED**, see below. The one time-sensitive item.
5. **Run the engine locally without the bake ceremony.** Owner ruling: **after (2)**. *Partly already
   true:* the score-apply gate arms by environment alone — no code edit — see the R20 directive §1.
6. **Off-season transformation spec** — new positions, draftees entering, ageing, retirements. The
   46-line runbook at `docs/archive/pre-mvp-2026-07/SPEC_SEASON_ROLLOVER_v1_2026-07-16.md` predates
   the restructure and knows nothing of the stream split. A starting point, not a spec.

## IN FLIGHT — three streams, deliberately concurrent

**The rule that makes them safe: stage 1 is PINNED, R20 is the only writer.**

| stream | seat | touches | state |
|---|---|---|---|
| **Priority 1 · stage 1** — measure what the restructure moved | fresh execution supervisor | nothing; read-only, pinned to `85e39ee` / store `c120cfd5` | directive filed: `docs/directives/PRIORITY_1_STAGE_1_fit_measurement.md` |
| **Priority 4 · R20 go-live** — apply round 20 | fresh execution supervisor | **the store, board and boot pins** | directive filed: `docs/directives/PRIORITY_4_R20_go_live.md`. Needs the owner's score file + `INGEST_SCORE_APPLY` token |
| **#205 · CI parallelisation** | supervisor-408 (held through execution) | `.github/workflows/live-scoring.yml` only | **FIRED 2026-07-28.** Audited, Addendum 1 filed |
| ITEM 412 pricing | **the owner** | — | his own work, off-seat |

Stage 1 must not re-read `main` after its pinned checkout. R20 may move the store freely underneath
it. Neither waits for the other. #205 collides with nothing and makes R20's test cycle ~4× faster if
it lands first.

## What stage 1 already knows before it starts

Traced to the artifact by the seam, 2026-07-28 — the directive carries the detail.

- **It is nine artifacts, not four.** `boot_guard.py:223` names five (`q97m`, `v0surf`, `peak_model`,
  `pvc_snapshot`, `bust_prior`); `band`/`cm_400.pkl` is pinned too; and `pvc_curve_v2.json`,
  `params.json` and `national_draft_last_pick.json` are **not pinned at all**, so nothing halts when
  they go stale.
- **The pick curve declares its own source store as `968de0c7`** — the 17 July store. It was already
  stale before D1.
- **D1 moved the `store` and `board` pins in `expected_boot.json` and left `v0surf` untouched.** The
  board of record `fa172ac1` was built with the old V0 surface on the new store.
- **The priors and the age curves carry no provenance record and have no identified producer.** The
  priors are an *input* to the peak model, so the chain has an unknown root. If nothing regenerates
  them, that is the finding.
- **The peak model and `pvc_snapshot.json` are one action.** `build_peak_model_v4.py` co-emits the
  snapshot; the freeze is a coupling rule, not a bar on re-deriving. Owner ruling 2026-07-28: they are
  re-derived together.
- **The stream split exists in the store and not in the engine.** `draft_stream` / `stream_pick` /
  `stream_year` are populated and nothing reads them; the boundary still comes from
  `national_draft_last_pick.json`, last touched 11 July.
- **Measured store delta across D1:** `pick` 679 · `drafted_position` 538 · `present_position` 499 ·
  `future_position` 1, over 572 distinct players, plus four new fields across 8,711 rows;
  1,733 + 8,711 = 10,444 field edits, matching the filed bijection exactly. *The register's "1,035
  position and 615 pick changes" is a v437 roadmap estimate filed before the transform ran.*
- **The pick-vs-player join test PASSES on the national draft** — 2021 1.37 · 2022 1.00 · 2023 1.18 ·
  2024 1.00 · 2025 0.90. No entry discontinuity. **An earlier seam version of this test was wrong**:
  it priced mid-season-draft picks off the national curve and produced a false 0.17. `PICKLESS`
  excludes MSD/SSP and `rl_model.py:218` says so directly. Filter on `type` before comparing anything
  to a pick price.

## Closed this cycle

- **ITEM 411 · D1 store restructure — LANDED** at `efaaa7fc`, true two-parent. Store
  `f37d9716 → c120cfd5`, board `6f07f7cb → fa172ac1`. 2,651 players. Class-(c) defects: zero.
  Issue #151 closed; `ci/item-411-d1-staging` deleted. *History: v408–v508.*
- **ITEM 408 · D2 forward-lens integration — LANDED** at `265bdab`, true two-parent, tree `c12650ec`.
  Issue #157 closed; `ci/item-408-d2-staging` deleted. *History: v422, v443, v448, v461–v508.*
- **Terminal CI for both:** all four suites green attempt-1 on tip `40a3da7`, every step success, zero
  skipped. The merge commits' own runs were cancelled by supersession, not red — `cancel-in-progress`
  keyed on the ref, three pushes inside 52 minutes. No workflow reads `docs/`, so the tip's product
  tree is byte-identical to the D2 merge and the tip run is valid evidence for both (v481).
- **live-scoring timeout raised 90 → 180** (`85e39ee`). It had been running at 86m12 against a 90m
  ceiling — 3m48 of margin — because D1 grew the store 18.2% and every proof slowed 3–7%.

## ITEM 410 — referee · FROZEN, HARNESS UNBUILT

`docs/referee/REFEREE_PROTOCOL.md` v1.0 FROZEN (owner word, v407). **v1.1 amendment drafted** at
`docs/referee/AMENDMENT_v1_1_DRAFT.md`, awaiting the owner's word. The harness is owner priority 2.
*History: v390–v407, v472.*

## Owner words of record — the unchallengeable set

| word | v |
|---|---|
| Express restructure-release word — buys staging only | v461 |
| The D1 transition legitimately moves the store | v467 |
| Widened restatement authorization | v469 |
| Amendment 5 GO | v481 |
| Token seal `ITEM_411_D1_restatement_v467` | v487 |
| The three-way architecture: position / current eligibility / future positioning | v499 · v500 |
| "future can follow present" | v503 |
| "Relaxed" — v483 standing authority restored | v507 |
| Viewing discharged; **"let's fire D1"** — the second word | v507 |
| Rotate 408 · scope conservation as its own job | v507 |
| The re-key is scoped **current season only** | v507 |
| **The governing test** and the six priorities | 2026-07-27 |
| Fire #205 · stage 1 and R20 both start · parallelise · 412 is his own | 2026-07-28 |
| `pvc_snapshot` is re-derived with the rest, not held frozen | 2026-07-28 |

## Outstanding owner acts

1. **The R20 score file and the `INGEST_SCORE_APPLY` token** — blocks priority 4. Nothing else does.
2. **v1.1 amendment word** — draft filed, one read.
3. **What #146 is for now** — he has commented on the issue; the purpose statement is still open.
   Its body inverted at D1: it says not to populate `draft_stream`/`stream_pick`/`stream_year`/
   `pick_correction_note` "unless they already exist", and they now do, on 2,651 players.
4. **G-MONO rulebook + twin wording** — later, with 412. Law-10: exact wording pre-filed.
5. *Optional:* revoke the unused ceremony PAT. Off-repo, owner-attested only.

## Seats

| seat | state |
|---|---|
| **seam + pen** | seated 2026-07-27. Rotates on a **verification-accuracy slip**. Disclosed this cycle: one wrong finding — priced MSD picks off the national curve and reported a false entry discontinuity; owner-caught. Artifact verification (hashes, counts, merges, ancestry) held throughout. |
| **supervisor-408** | held through #205 by seam ruling; rotate after it executes, or on any degradation sign. Disclosed one enumeration error (seven writers vs eight), root-caused and addended by itself. |
| **supervisor-411** | **rotated out 2026-07-28**, clean boundary, ITEM 411 closed, queue empty. |
| **stage-1 seat** | to be seated, fresh, cold |
| **R20 seat** | to be seated, fresh, cold |

Live seat depths are deliberately **not** recorded here. **Capability maps vary per environment and
are re-tested per seat, never inherited.**

## Parked — do not start

- **Track D**, five items, all in *test harnesses*, none touching the engine or board. **None can stop
  the project working.**
- **Conservation gate.** `gate_f5.py` cannot be wired as written — its input board exists nowhere in
  the tree, its path and epoch are hardcoded, its comparison side is a static July file. The law is
  reusable; the file is not. Placement, *seam ruling not owner word*: inside the advance transaction,
  before commit. Scheduled before ITEM 412's pricing work. Figures: entrant intake 83,538
  (69,266 + 14,272, seal `a17aafed`); realised totals 770,987 / 771,152 / 752,427; band −1.2% / +1.7%.
- **`test_club_valuation_current.py` is not wired into CI.** Seam ruling: leave it. It guards a file
  that bakes a sum a browser computes instantly, and the owner's ruling on that fault is to stop
  baking the sum, not to guard it. Revisit only if someone is in that code for another reason.

## Environment carries

- Containers **shallow-clone by default**. `git fetch --unshallow` before any ancestry claim.
- **The numpy pin is deterministic per container, not intermittent.** `bootstrap.sh` asserts a sha256
  of the OpenBLAS bundled inside the numpy 2.4.4 wheel; an environment either matches or never will.
  Fix by running `bootstrap_env.sh` (needs PyPI reachable), never by bypassing. Different wheels
  compile `np.interp` differently — ~1e-8 divergence against a ~1e-12 board flip threshold — so an
  unpinned wheel silently reorders the board. This guard prevents a *wrong* board.
- Run **`bootstrap.sh`**, not `setup_env.sh` alone — `unidecode` is vendored and seeded by bootstrap.
  **Exception:** `live-scoring.yml` deliberately does not run `bootstrap.sh` (legacy Guard 5 would red
  on register item 399's stale engine pins); it seeds the dependency itself.
- The Actions API can exceed per-call output caps; spill to a file and parse rather than re-pulling.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
