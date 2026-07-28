# CURRENT STATE — the incoming-seat read · v4 · supervisor pen · 2026-07-28, register v509

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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v509, main `cd869b1`.*

## THE PRICING STRUCTURE — owner-ruled 2026-07-28, and it governs everything below

**The national curve stops at pick 64.** Everything past 64 enters a **rookie pool**: ND 65+, all
rookie draft, all post-draft selections. Valued **by position**; **order of selection is irrelevant**
inside the pool. SSP and MSD are valued at the pool but tracked separately so they may become their
own pools as data accumulates.

| | rows |
|---|---|
| ND curve, picks 1–64 | 1,448 |
| rookie pool (121 ND 65+ · 924 RD/post-draft) | 1,045 |
| SSP · MSD (pool-valued, tracked apart) | 52 · 106 |

This is ITEM 412's sealed structure reaching the engine, which had never implemented it.
`rl_model.py:209` and `:215` still chain rookies onto the national draft — that is what is being
removed. **Do not re-derive `national_draft_last_pick.json`**; those two lines are its only consumers.

Owner ruling of the same date: **D1's ND densification is correct** (the store is the authority; the
table is the stale side), and **Matt Maguire's removal was intended**.

## IN FLIGHT

| | |
|---|---|
| **#207 · stage 1** | Returned once, re-tasked. Recalculating bust priors on the new store and re-fitting the curve under the new structure. Was pinned to store `c120cfd5`; the store has since moved and its figures stay valid for the store they name. |
| **#208 · R20** | **Applied, not finalized.** Store `c120cfd5 → e3aaba77`, board `fa172ac1 → 8a38cca4`, 410 players. Phase two refused on a real finding (below). Awaiting the restructure-entry fix. **`3a18ea2` must not be merged as a finished round.** |
| **ITEM 412** | The owner's own work, off-seat. |

## The movers chain break — #208's live blocker

The bundle requires `report[n].board_md5_before == report[n-1].board_md5_after`. R15–R19 is continuous
(`2ab73a6f → 2fe26675 → 8ad41708 → 0308202f → 4323c448 → 92a8f3a0`) and R20 attaches at `fa172ac1`.
**D1/D2 rebuilt the board without a round apply**, and the invariant assumes the board only ever moves
through rounds. `repair()` and `finalize_round(force=True)` fail identically and write nothing — there
is no code path that writes FINALIZED with a broken chain, deliberately.

**Owner ruling:** generate the jump `92a8f3a0 → fa172ac1` as its own bundle entry, labelled the D1/D2
restructure rather than a round. Both boards exist and the machinery already computes movers between
two boards. The board will move outside a round again — the re-derivation will do it, and so will 412.

## The priors — recovered, and being recalculated

Believed unre-derivable; they are not. The producer was a one-off `/tmp/bustprior.py` plus
`FORWARD_MODEL_V3_STATUS.md`, **neither ever committed on any ref**. The recipe is recorded in full in
the register at v509. In short: target is best-3 season average over ≥6-game seasons with
never-established players entered as **0.0** (that zero is the survivorship fix); debut cohorts
2006–2020; `IsotonicRegression(increasing=False)` on effective pick, fitted pooled and per-position,
blended `w = min(n_pos/200, 1) × 0.6`.

**Both of its axes moved**: 538 players changed drafted position, 338 inside its own training window,
crossing strata. New shape — ND 1–64 as written; pool the same target and blend with **no isotonic
step**, because with order irrelevant there is no pick to regress on. One value per position.

Two defects, neither flagged at derivation: the `× 0.6` is a hard ceiling with no stated basis (every
prior is ≥40% pooled — the suspected cause of a real ~19-point top-of-draft spread compressing to ~8),
and `increasing=False` on raw pick gives plateau widths set by noise.

## The propping mechanism — the model of record

`fit_year0` grows an adaptive bandwidth until it finds 35 effective observations and weights by
Gaussian distance in log-pick. **It is stream-blind.** Where national thins the kernel reaches
furthest, into rookie observations sitting above national at the same pick; `monotone_strict` then runs
PAVA, which propagates that lift backward. **Strict descent is the fix, so comparing final curves
cannot see it** — the seam and #207 both did that and both concluded wrongly. Measure the raw fit and
the rookie share of kernel weight.

Structural fact independent of the above: ND effective picks run 1–80, rookies 62–99. Picks 1–60 are
**0% rookie**, 81–99 are **100% rookie**. Past pick 80 the national draft has no observations at all.

## Priority 5 evidence — it points the opposite way to the assumption

**Four guards fired in anger in one R20 round**: identity resolution, `round_finalize` chain validation,
the env pin, and Guard 5. Only the boot pins, the dedup ledger, the dry-run and `movers_conflict` merely
re-armed. **The ceremony worth removing is the four-surface panel re-pin** — hand-typed, blocks every
landing, has never caught anything.

## Closed this cycle

- **ITEM 411 D1** `efaaa7fc` · **ITEM 408 D2** `265bdab` — both landed, issues #151/#157 closed, both
  staging branches deleted.
- **#205 CI parallelisation** — PR #210 merged. **86m12 → 19m16, 4.47×.** §5 discharged on artifact
  check-sets, not conclusions. `live-scoring.yml` timeout raised 90 → 180.
- **supervisor-408** rotated on a clean boundary. **supervisor-411** rotated earlier.

## Owner acts outstanding

1. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified against the
   store, one read. Optional dial: make RD its own observation row inside POOL (693 players).
2. **#146** — parked by owner ruling until 412 needs a canvas. Its body inverted at D1; do not execute
   as written.
3. Referee harness scope — a fresh Fable seat, owner-scheduled.

## Seats

| | |
|---|---|
| **seam + pen** | **Rotating now on a verification-accuracy slip.** Six errors this session, all owner- or seat-caught, none reaching the product. Two families: reading what *describes* the system instead of what *commissions* it, and stating a figure without pinning its basis or population. Artifact verification held throughout. **Distrust any scope or figure it asserted without naming what it read; rely on anything it hashed or re-derived.** |
| **#207 · #208** | Live, fresh, one job each. |

## Parked — do not start

Track D (five items, none touching the product) · the conservation gate (`gate_f5.py` cannot be wired
as written; scheduled behind 412) · `test_club_valuation_current.py` CI wiring (seam ruling: leave it —
it guards a file that bakes a sum a browser computes instantly).

## Environment carries

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **`bootstrap_env.sh` invokes bare `python3`** while the lock pins the cp312 wheel. Containers vary;
  this one defaulted to 3.11 with `/usr/bin/python3.12` present. `live-scoring.yml` already solves it by
  discovering `python3.12` by name — the local bootstrap never got the same treatment. **One-line fix,
  has now cost two seats.** Never bypass the pin: a different numpy wheel silently reorders the board.
- The env-pin guard hashes the bundled OpenBLAS but **not** the numpy binary where `np.interp` lives,
  so it cannot tell the two wheels apart — the exact thing it exists to catch.
- **`sibling_repin` rewrites history every round** — it blanket-replaced `5546f278` in all three
  occurrences in `expected_boot.json`, including inside the clause reading "truth preserved as history".
  Narrative only, no executable reader. Repair in place when that narrative is next rewritten.
- The Actions API can exceed per-call output caps; spill to a file and parse.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
