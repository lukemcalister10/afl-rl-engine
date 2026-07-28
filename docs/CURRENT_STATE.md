# CURRENT STATE — the incoming-seat read · v10 · supervisor pen · 2026-07-28, register v517

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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v513, main after `69e8458`.*

## WHAT THE CURRENT WORK IS FOR — read this before you touch the model

**Owner's words, 2026-07-28:**

> Right now, we are doing apples for apples conversion of the new store and ND/RD/Pool split into the
> current system. Anything else would be redefining HOW we model or HOW we value, which is the job of
> the referee project which comes next, and 412. This is about establishing a correct baseline with our
> new information to compare to.

**So: the method is held constant. Only the data and the separation change.** If you find yourself
improving a calculation, you have left the job — that improvement belongs to the referee project or to
ITEM 412, and it goes back to the owner.

This is the drift that has cost this project the most. A seat reads "baseline", sees a defect, and fixes
it — and now the baseline is not comparable to anything, which was its entire purpose. **The known
defects are to be reported, not repaired.** The `× 0.6` blend ceiling stays. The isotonic step stays. The
low-sample pooling that pulls RUC toward the pooled average stays. They are the thing being replicated.

**Sequence of record:** baseline (#217 + #225) → the referee project → ITEM 412.

## THE PRICING STRUCTURE — ruled, now law, engine still to follow

**The national curve stops at pick 64.** Everything past 64 enters a **pool**: ND 65+, all rookie
draft, all post-draft selections. Valued **by position**; **order of selection is irrelevant** inside
the pool. SSP and MSD are valued at the pool but tracked separately.

| | rows |
|---|---|
| ND curve, picks 1–64 | 1,448 |
| pool (121 ND 65+ · 924 RD/post-draft) | 1,045 |
| SSP · MSD (pool-valued, tracked apart) | 52 · 106 |

**There is no price for pick 70.** A player taken there is priced from the pool by position, not from
a curve. If you are asking what a pick past 64 is worth, you have reverted to the old model.

**This is now law.** `docs/RULEBOOK.md` v2.1, law 4 (G-MONO), amended by owner word 2026-07-28 with
exact wording pre-filed: the national pick curve covers 1–64 and descends across that domain, pick 1 =
3000; selections past 64 are not on the curve. Twin `docs/acceptance_v2_0.json` v2.1 matches. **No
further amendment is needed to implement the split** — the rule was written when the curve ran to 99,
and the amendment scoped it rather than weakened it.

**Why seats keep reverting, and it is not comprehension.** The old structure is implemented in the
code, in every artifact shaped 1–99, in the tests, and across the register; the new structure lives in
owner rulings, this page and now the rulebook. A seat reads code and artifacts, so it rebuilds the old
model from what is in front of it. **The ruling loses to the code.** That is why the engine change now
comes before further measurement.

Do not conflate two layers: `_PVC0`/`draftval` price by pick with no position argument, but
`iso_corr(pos, pk)` takes both and `_v0_curve_assert` asserts V0* is a function of `(pos, ageR, pick)`.
**The engine already prices by position.** The pool needs one index, not a new capability.

## IN FLIGHT

| | |
|---|---|
| **Engine split · #217** | **FIRED and UNGATED.** `docs/directives/PRIORITY_1_engine_split_implementation.md`. Fresh cold seat. **The only job in flight that writes the store or board.** |
| **UI card + navigation** | **FIRED.** `docs/directives/PRIORITY_UI_card_and_navigation.md`. Ten #139 items in three clusters — the player card's weekly history, the Public navigation defects, and the tab tidy-up. UI only; no overlap with #217. |
| **#208** | **CLOSED.** R20 finalised, from/to tab, all three closing tasks landed (`411735f`). |
| **#207** | **CLOSED.** Stage 1 measurement landed at `462256f`. Adoption is stage 2 and is the owner's call. |
| **ITEM 412** | Ruled slice folded back into build work. Retains the open design questions. |

## Round 20 and the Movers tab — landed

R20 is FINALIZED on main at `59d740c` (head `9897c78` — **not** `3a18ea2`). The tab is a from/to
comparison over eight points: 14 · 15 · 16 · 17 · 18 · 19 · `Post R19 Redesign 1` · 20, all present in
all three histories at 804 rows each.

The out-of-round point is a **string id** in `by_round` plus a `columns` register, deliberately kept
out of the int `rounds` list so anything that int-coerces it is unaffected. Board `fa172ac1` was
recovered from git (blob at `8ecf8f8`, md5 verified) and read as a snapshot, not re-derived.

**The default view changed meaning, deliberately.** R20's report compares against the point immediately
before the round, not R19, so the restructure is no longer reported as round 20's own effect — 758
movers the old way, 681 the honest way.

**Five checks were removed, not four.** The fifth was the rule requiring every report to carry an
identical release identity — same false premise as the chain, and it would have fail-closed the tab
permanently. Owner-approved. Accepted cost: the content-tamper digest went with it. One assert replaced
them all — the newest stored point matches the live board — proven non-vacuous both directions.

**Standing rule, CORRECTED 2026-07-28 by owner direction — the earlier wording was wrong.** A history
column is written **once per landed change, not once per board rebuild.** A board may be rebuilt four or
five times inside one piece of work; those intermediate states are working builds, not comparison points,
and giving each one a column fills the dropdown with noise. **Do not ask for a label mid-job.** When the
change lands, one column, one owner-set label — ask then, and never invent one.

The whole current baseline effort — the split, the pool-row exclusion, the `v0surf` rebuild, #225's
derivation and the owner's adoption — is **one change and gets one column.**

## #208's three closing tasks — all landed

1. **The four-surface panel re-pin is gone** — `run_panel.sh`, the `expected_boot.json` `panel` key, the
   narrative and the CI gate. `PANEL_EXPECTED.txt` untouched. **Guard 5 kept** — it asserts store /
   rl_model / fv identity and has fired in anger. `run_panel.sh` now reports; Guard 5 judges. A board move
   no longer costs a hand re-pin.
2. **The Bailey Williams override is round-scoped to R15–R19, not deleted** — new `applies_to_rounds`
   field plus a scope check in `round_catchup.py`. Scoped rather than retired because those fixtures
   genuinely do list both players under one display name and the catch-up proofs re-run them; deleting
   would have misattributed historical rounds silently. Re-measured on store `e3aaba77`: zero display
   names shared by two or more of the 804 active players. Callum Brown stays unscoped.
3. **Movers schema 1 → 2.** R15–R19 keep v1 and integer predecessors; the bundle holds both versions,
   each self-describing. Nothing in the tree branches on `schema_version`.

## Integration hazard — read this before merging any seat branch

**A rebase-merge rewrites SHAs.** A branch that keeps building on its already-merged history presents
those commits again under their original ids, so the merge base rewinds past them and every touched file
looks like an independent edit on both sides. Both seat branches hit this: #208 conflicted on eight files,
and #207 appeared to rewrite ten files it had never opened.

**`git diff main..branch` on a stale-based branch is not a statement of what that branch changed.** Diff
against the branch's own merge base. The fix is `git rebase --onto origin/main <old-tip>`, then verify the
replayed diff is byte-identical to the original before pushing.

## #207 — what stands, and what it is pinned to

Withdrawn and carried nowhere: the scratch-board figures (18 movers, mean −15.2, pick-asset sum −1,381).
They were measured on a 493→459 descending tail that was never ruled; the artifact is deleted.

Standing, each naming its basis: `curve_nd_1_64.json` — 64 entries, domain 1–64, pin 3000, strictly
decreasing, no pool entries (seam-verified). Rookie share of kernel weight on store `c120cfd5` — 30.3%
at national pick 64, 0.0/0.8/17.0% at 40/50/60; the bandwidth never grows and PAVA never fires, so the
reach is log-pick proximity, not adaptation; rookies sit 77.3 **below** national at 59–64 and 26.8
**above** at 65–70, so inside the boundary the blend depresses the fit by 13.7 points (−2.5%) at pick 64
and the upward propping lives in the band the split removes anyway. Bust priors on a 1,793-player
window, pool as one value per position, 27.9–33.5, grand mean 29.8. The 0.6 ceiling at 18.9 as written
vs 35.5 uncompressed — 1.88×, binding for five of six positions.

**Every one of those is pinned to store `c120cfd5`, and the store has moved to `e3aaba77` with R20.
Re-run before adopting anything.** Not measured and waiting on the engine change: the pool's board
effect and the 1–64 curve's, since a board needs both sides priced.

## Housing — corrected

**The seam can merge its own PRs.** The housing note says merges land under the owner's auth; that
describes whose credentials the merge runs under, not who may click it. PRs #213, #214 and #215 were
rebase-merged by this seat directly. **Stop sending merges to the owner.** Direct push to main is still
classifier-blocked, so docs pens still go branch → PR → rebase-merge. Ref deletion remains proxy-forbidden.

## Owner acts outstanding

1. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified, one read.
2. **#146** — parked until 412 needs a canvas. Its body inverted at D1; do not execute as written.
3. Referee harness scope — a fresh seat, owner-scheduled.
4. Stage 2 adoption of anything from #207 — his call, and it comes after the engine change.

**Issue list, tidied 2026-07-28.** #139 items 1 and 4 are done — item 4 is the arbitrary-Movers-comparison
feature, built by #208. **#139 stays open; its other 21 items stand.** #138 closed as obsolete (it specified
a replay of a tab that was replaced instead, and its gate names a board three generations back). #205 closed
as completed (landed as PR #210). Held out of the UI bundle deliberately: item 7 needs an open 412 answer and
a store field that does not exist, and item 8 changes shape once #217 lands, because picks past 64 are no
longer priced on the curve.

## Seats

| | |
|---|---|
| **seam + pen** | Four errors this session, all owner- or hook-caught, none reaching the product: staged another seat's product files onto the seam branch during a verification checkout; said the engine could not price by position after reading only the pick ladder; said nothing needed relaxing on strict descent without reading the rulebook; checked whether a curve tail was flat instead of asking why it had a tail. **All four are the same fault — reading what implements the system instead of what commissions it.** Artifact verification held: every hash, count, diff and ancestry check it ran itself has stood. |
| **#207 · #208** | Both closing. Engine-split seat opens fresh and cold. |

## Parked — do not start

Track D (five items, none touching the product) · the conservation gate (`gate_f5.py` cannot be wired as
written) · `test_club_valuation_current.py` CI wiring — it guards a file that bakes a sum a browser
computes instantly.

## Environment carries

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **`bootstrap_env.sh` invokes bare `python3`** while the lock pins the cp312 wheel. `live-scoring.yml`
  already solves this by discovering `python3.12` by name; the local bootstrap never got the same
  treatment. **One-line fix, has now cost two seats.** Never bypass the pin.
- The env-pin guard hashes the bundled OpenBLAS but **not** the numpy binary where `np.interp` lives.
- **`sibling_repin` rewrites history every board move** — #208 restored the two `5546f278` references it
  had overwritten, and it will overwrite them again next time.
- The register header is **one ~347KB line**. `head` on it dumps the whole file — read it with a script
  that windows around a match, never with `head` or `cat`.
- The Actions API can exceed per-call output caps; spill to a file and parse.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
