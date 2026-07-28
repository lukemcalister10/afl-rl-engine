# CURRENT STATE — the incoming-seat read · v5 · supervisor pen · 2026-07-28, register v510

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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v510, main `a7dc1b4`.*

## THE PRICING STRUCTURE — owner-ruled, and the engine still does not implement it

**The national curve stops at pick 64.** Everything past 64 enters a **pool**: ND 65+, all rookie
draft, all post-draft selections. Valued **by position**; **order of selection is irrelevant** inside
the pool. SSP and MSD are valued at the pool but tracked separately.

| | rows |
|---|---|
| ND curve, picks 1–64 | 1,448 |
| pool (121 ND 65+ · 924 RD/post-draft) | 1,045 |
| SSP · MSD (pool-valued, tracked apart) | 52 · 106 |

**There is no price for pick 70.** A player taken there is priced from the pool by position, not from
a curve. If you find yourself asking what a pick past 64 is worth, you have reverted to the old model.

**Read this before you touch anything in this area.** The owner has ruled this seven or eight times
and seats keep returning questions that assume picks past 64 are priced. The reason is not that the
ruling is unclear. The old structure is implemented in the code, in every artifact shaped 1–99, in the
tests, and across the register; the new structure lives in owner rulings and this page. A seat doing
work reads code and artifacts, so it rebuilds the old model from the material in front of it. **The
ruling loses to the code, because the code is what you are looking at.** That is why the engine change
below now comes before any further measurement.

Two things are position-blind and two are not, and conflating them has cost this project real time:
`_PVC0`/`draftval` price by pick with no position argument — but `iso_corr(pos, pk)` takes both, and
`_v0_curve_assert` asserts V0* is a function of `(pos, ageR, pick)`. **The engine already prices by
position.** The pool needs one index, not a new capability.

## THE PRIORITY — the engine change

Remove the chaining at `rl_model.py:209` and `:215`, end the curve at 64, give the pool one index so
the existing position layer prices it. Owner-agreed as the thing that comes first, because after it no
seat can rediscover the old structure.

**It must not run concurrently with #208.** It re-prices every player and moves the board — the exact
out-of-round board move that broke the movers chain. #208's from/to work is the prerequisite that makes
the board safe to move.

**Do not re-derive `national_draft_last_pick.json`**; lines 209 and 215 are its only consumers and both
are being removed.

**G-MONO.** `docs/RULEBOOK.md` §4 says *"the pick curve is strictly decreasing; pick 1 = 3000 exactly."*
That is law, not code — the engine's own assert (`rl_export.py:137`) is only non-increasing. Under the
ruled structure the pick curve is 1–64 and descends, and the pool is not a pick curve, so **G-MONO is
satisfied as written and no amendment is needed.** The owner has been offered that reading and it is his
to confirm. Any Law-10 act still needs his exact wording and explicit word.

## IN FLIGHT

| | |
|---|---|
| **#208 · R20 + Movers** | Directive `docs/directives/PRIORITY_4_movers_from_to.md` on main at `a7dc1b4`. The tab becomes a from/to comparison; the chain is deleted, not repaired; R20 finalises with it. **`3a18ea2` must not merge as a finished round** — its committed `movers.js` already carries R20 stamped `board_chain_ok: false`. |
| **#207 · stage 1** | Returned. Measurement-only discipline held. Both of its stage-2 blockers were wrong (see below) and its scratch-board figures name a structure the owner did not rule. To be re-tasked: hand back what stands alone, leave the pool's board effect to the engine change. |
| **ITEM 412** | Its ruled slice folded back into build work. See below. |

## The Movers tab — what was ruled and why

The chain required each round to start from the board the previous round finished on. That holds only
if the board never moves except through a round, and it now permanently does not. Rather than patch it,
the tab becomes **from/to**: two dropdowns, any two stored points compared on request. Each comparison
names its own endpoints, so it needs no chain, no integrity flag and no provenance bridge.

Verified facts behind the ruling: `value_history`, `rank_history` and `pos_rank_history` each hold
**804 players across rounds 14–20**, so nothing needs deriving to compare round to round; the browser
(`ui/app/movers.js`) enforced the same continuity independently, so "accept the break and finalise
anyway" was never available; and the `92a8f3a0 → fa172ac1` jump already had an owner-approved record in
`movers_transition.js`, which is why a synthetic bundle entry was withdrawn.

Standing rule that comes out of it: **whenever the board moves outside a round, write a history column
at that point.** The first is labelled `Post R19 Redesign 1` — owner-set, verbatim. The re-derivation
and 412 each add one. `movers_transition.js` is kept as the register of those moments; its enforcement
is removed.

## ITEM 412 — what folded back and what did not

412 is a read-only design seat producing three documents. Its structure spec listed pool construction,
but **the owner has since ruled the pool's construction himself**, so that slice is implementation and
folds into build work now.

**412 retains:** the pricing validation design (G-MONO, CONSERVATION, L-CAPTAIN, LENS-PROJECTION, G-Y0,
G-COHORT bind at that layer), curve family, era handling, observation-lane mechanics, the replacement
bar re-keyed from position to eligibility, and the future-eligibility instrument that does not exist as
a field.

**Fence on whoever implements:** build exactly what is ruled and decide nothing else. Anything you find
yourself *choosing* is 412's and goes back to the owner.

## The priors — recovered, recalculation not yet trustworthy

The producer was a one-off `/tmp/bustprior.py` plus `FORWARD_MODEL_V3_STATUS.md`, neither ever
committed. The recipe is in the register at v509: best-3 season average over ≥6-game seasons with
never-established players entered as **0.0**, debut cohorts 2006–2020, `IsotonicRegression(increasing=False)`
on effective pick, fitted pooled and per-position, blended `w = min(n_pos/200, 1) × 0.6`.

#207 has recalculated them, but on the wrong tail shape. Its prior values, rookie-share percentages and
the findings that the bandwidth never grows and PAVA never fires are **on the seat's word only** — the
seam did not re-run the fit. Treat them as unverified until re-run under the ruled structure.

Known defect, still standing: the `× 0.6` is a hard ceiling with no stated basis, and it binds for five
of six positions, so above n=200 sample size stops mattering.

## Priority 5 — the ceremony worth removing

Four guards fired in anger in one R20 round: identity resolution, `round_finalize` chain validation, the
env pin, and Guard 5. Only the boot pins, the dedup ledger, the dry-run and `movers_conflict` merely
re-armed. **The four-surface panel re-pin is the one to delete** — hand-typed, blocks every landing, has
never caught anything. Owner-agreed.

## Closed this cycle

- **PR #212** — the from/to directive, merged `a7dc1b4`.
- **ITEM 411 D1** `efaaa7fc` · **ITEM 408 D2** `265bdab` — landed, issues #151/#157 closed.
- **#205 CI parallelisation** — PR #210 merged. **86m12 → 19m16, 4.47×.**

## Owner acts outstanding

1. **Confirm the G-MONO reading** above — his law, his call, and it decides whether a Law-10 amendment
   is needed at all.
2. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified, one read.
3. **#146** — parked until 412 needs a canvas. Its body inverted at D1; do not execute as written.
4. Referee harness scope — a fresh seat, owner-scheduled.

## Seats

| | |
|---|---|
| **seam + pen** | Four errors this session, all owner- or hook-caught, none reaching the product: staged another seat's product files onto the seam branch during a verification checkout; said the engine could not price by position after reading only the pick ladder; said nothing needed relaxing on strict descent without reading the rulebook; checked whether a curve tail was flat instead of asking why it had a tail. **All four are the same fault — reading what implements the system instead of what commissions it.** Artifact verification held: every hash, count, diff and ancestry check it ran itself has stood. |
| **#207 · #208** | Live, one job each. |

## Parked — do not start

Track D (five items, none touching the product) · the conservation gate (`gate_f5.py` cannot be wired as
written) · `test_club_valuation_current.py` CI wiring — it guards a file that bakes a sum a browser
computes instantly.

## Environment carries

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **`bootstrap_env.sh` invokes bare `python3`** while the lock pins the cp312 wheel. `live-scoring.yml`
  already solves this by discovering `python3.12` by name; the local bootstrap never got the same
  treatment. **One-line fix, has now cost two seats.** Never bypass the pin — a different numpy wheel
  silently reorders the board.
- The env-pin guard hashes the bundled OpenBLAS but **not** the numpy binary where `np.interp` lives.
- **`sibling_repin` rewrites history every round** — it blanket-replaced `5546f278` in all three
  occurrences in `expected_boot.json`, including inside a clause reading "truth preserved as history".
  Narrative only, no executable reader. Repair in place when that narrative is next rewritten.
- The register header is **one 340KB line**. `head` on it dumps the whole file — read it with a script
  that windows around a match, never with `head` or `cat`.
- The Actions API can exceed per-call output caps; spill to a file and parse.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
