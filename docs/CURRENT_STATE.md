# CURRENT STATE — the incoming-seat read · v13 · supervisor pen · 2026-07-28, register v521

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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v519, written against main `144cd33`
(this pen lands on top of it).*

**Reading the figures below:** anything marked *seam-verified* was re-derived by the seam from the
artifact. Everything else is the reporting seat's own measurement, named so you can weigh it. Where it
matters, re-run rather than inherit.

## WHAT THE CURRENT WORK IS FOR — read this before you touch the model

**Owner's words, 2026-07-28:**

> Right now, we are doing apples for apples conversion of the new store and ND/RD/Pool split into the
> current system. Anything else would be redefining HOW we model or HOW we value, which is the job of
> the referee project which comes next, and 412. This is about establishing a correct baseline with our
> new information to compare to.

**The method is held constant. Only the data and the separation change.** If you find yourself improving
a calculation, you have left the job.

This is the costliest drift here: a seat reads "baseline", sees a defect, fixes it — and the baseline is
no longer comparable to anything, which was its entire purpose. **Known defects are reported, not
repaired.** The `× 0.6` blend ceiling stays, the isotonic step stays, the low-sample pooling stays. They
are the thing being replicated.

**Sequence:** baseline (#217 → #225 → owner adoption) → the referee project → ITEM 412.

## THE PRICING STRUCTURE — ruled, and law since 2026-07-28

**The national curve covers picks 1–64.** Everything past 64 enters a **pool**: ND 65+, all rookie draft,
all post-draft selections. Valued **by position**; **order of selection carries no value** inside it.
SSP and MSD are pool-valued but tracked separately.

**There is no price for pick 70.** If you are asking what a pick past 64 is worth, you have reverted.

`RULEBOOK.md` v2.1 law 4 (G-MONO) scopes strict descent to picks 1–64; the pool is outside it. Twin
`acceptance_v2_0.json` v2.1 matches. **No further rulebook change is needed to implement the split.**

**The owner has stated this ten times and it has been lost ten times — never in comprehension, always at
the point where someone turned it into instructions.** A directive must carry his requirement verbatim
and state acceptance as a **property of the result**, not a list of lines to edit. A wrong edit can
satisfy a line list; it cannot satisfy an outcome test.

## THE CRITICAL FACT ABOUT THE CURVE — get this wrong and you will misread everything

**The shipped pick curve is a LOADED ARTIFACT, not the in-engine fit.** `rl_export.py` loads
`pvc_curve_v2.json` and `PVC` *is* that artifact. Nothing in the engine writes it. `_merged_recover.py:1537`
records **owner ruling R3 of 2026-07-09** holding the in-engine fit out of the bake — experiments only,
with a bake guard refusing to write a bakeable board with the fit on.

**So cleaning the fit cannot move a shipped price.** The seam wasted a cycle asserting otherwise. The
prices on the board today are still the pre-split numbers. **Only #225 produces a replacement, and
adopting it is an owner act. The baseline does not yet exist.**

Two layers, routinely conflated: `_PVC0`/`draftval` price by pick and are position-blind, but
`iso_corr(pos, pk)` takes both and V0 is asserted a function of `(pos, ageR, pick)`. **The engine already
prices by position.**

**V0 is not an outcome measure.** It is a function of position, age band and pick only — it carries no
information about whether a player ever played. A mean of V0 describes a population's entry slots and
ages, never what those players became. This produced a false finding twice: the pool's never-played mean
(612.41) sits *above* its played mean (550.29) purely because the never-played group skews younger and
V0 reads youth as runway.

## IN FLIGHT

| | |
|---|---|
| **#217 · engine split** | Split + pool-row exclusion implemented and seam-verified (`a94f26d`). **Not merged.** Now rebuilding the `v0surf` frozen surface, deleting its silent fallback, and re-measuring every figure on it. Then it lands. |
| **#225 · stage 2** | Fired, queued behind #217. Derives the ND 1–64 curve and the pool level from scratch. Apples for apples. |
| **#231 · hand-pins** | Fired, fresh seat. Four defects of one shape — see below. |
| **#232 · ownership sidecar** | Fired, fresh seat. Makes a daily trade cost an edit rather than an engine run. |
| **ITEM 412** | Owner's, off-seat. Retains the open design questions. |

## The exclusion — what #217 has done and what it does not fix

**On #217's branch `a94f26d`, not on `main` — do not grep `main` for it.**
`_teaches_curve(p) = _in_pvc(p) and not is_pool(p)` at `rl_model.py:275`, applied at the three ±4 windows
and the V0 kernel path, with non-vacuity wired into the selftest and proven both directions. The seat
reports 771 pool rows excluded and 1,201 teachers remaining, with the V0 path landing on exactly 1,448 —
which matches the ND 1–64 count in the table above, reached independently. `_grp` stays `'RD'`; `hist`
untouched. Shipped curve truncated 99 → 64 with picks 1–64 byte-identical (seam-verified).

**The contamination was real:** picks 61–64 went 286/284/284/284 → 235 once excluded. It reached the board
through the V0 surface, not the shipped curve.

**Beware the slide-up.** `_pvc_eff` slides pool rows *below* 65 into vacated slots, so picks 58–60 each
carried 67 pool rows. The lowest fully clean pick was 57. "Picks 1–60 are clean" was false.

## The `v0surf` defect — a missing halt, not fake data

`data/v0surf.pkl` is a lookup table computed once at a bake and frozen so every build reads identical
values. Its config signature includes the pick curve, so the split moved it and **the engine silently
recomputed at build time instead of halting.** The values are the right calculation at the wrong time —
what they are not is reproducible, and reproducibility is the whole purpose of a baseline.

**Every figure #217 has reported is measured on the refit surface**, including all board hashes and mover
counts. Precedent to replicate: the sibling `q97m` pickle had its fit path deleted so it halts.

## #231 — four defects of one shape, and one of them took the app down

**A value a human must retype when something moves, or a check that cannot notice it is wrong.**

1. **`EXPECTED_BOARD`** pinned `fa172ac1` while the board of record was `8a38cca4`, so `ringFence()`
   rejected the board and **every tab rendered the fail-closed panel.** Fixed at `6d8f910`; retiring the
   hand-pin is now commissioned. **Provenance, seam-measured — it is worse for process than for
   duration:** the pin had tracked the board correctly at every previous move. It went stale when R20's
   board landed on `main` at `fef7f69` and was corrected hours later at `6d8f910`, both on 2026-07-28.
   **One board move, not two, and the seam caused it** by merging a board move without checking the pin
   that guards it. That is the argument for retiring the pin, not against it.
2. **`release_seam.test.js` builds its fixtures from that pin**, so it passed straight through the
   outage. Vacuity, guarding the thing that broke.
3. **`bootstrap_env.sh` invokes bare `python3`** against a cp312-pinned lock. Has cost two seats.
4. **The env-pin guard** checks the numpy version string and OpenBLAS hash, both identical across the
   cp311/cp312 builds, so it cannot detect the swap it exists to detect.

## Landed this cycle

- **R20 finalised**; Movers is a from/to comparison over eight points (`14`…`20` plus
  `post-r19-redesign-1`). The board-identity chain, its integrity flag and the provenance bridge are gone.
- **#222 · thirteen #139 items** (`6d8f910`): the card's weekly history, the Public navigation defects,
  the tab tidy-up, and club totals summing in the browser — **all 16 clubs had been wrong by up to
  +1,853.** Round review retired; Movers is the weekly-review surface.
- **#208's three closing tasks**: panel re-pin retired, Bailey Williams override round-scoped to R15–R19,
  movers schema bumped to 2.
- **#207 stage 1** measurement preserved at `session_2026-07-28/item207_stage1/`, pinned to store
  `c120cfd5` — **re-run before adopting anything from it.**
- **RULEBOOK v2.1** — G-MONO scoped, Law-10, owner-signed.
- Issues closed: #207, #208, #138 (obsolete), #205 (was done, never closed).

## Standing rules set or corrected this cycle

- **One history column per landed change, not per board rebuild.** A board moves several times inside one
  piece of work; a column each fills the dropdown with noise. **Do not ask for a label mid-job.** The
  whole baseline effort is one change and gets one column — `Post R19 Redesign 2` when it lands.
- **Whenever the board moves outside a round, a column is still written** — at the landing, not the build.
- **Screen by re-running, never by reading.** Three seam errors this cycle came from inferring off a file
  read. Every count names its denominator.

## Known-bad data, shipped, not this cycle's to fix

**The movers bundle carries its own `dnp` flag and it is wrong.** It marks 486 of 804 players "did not
play" in R15, a round that recorded 318 scores. Complete rounds R17–R20 recorded 410/406/405/410, so the
tracked population that plays a full round is **405–410** — the 804 includes players no round would
select. Against R15's 318 that puts **87–92 players who played carrying `dnp: true`.** It is "absent from the score map" dressed as a football fact. #222 correctly
declined to use it.

**The baked pick prices in `ui/data/club_valuation.js` go stale when #225 lands.** #222 left them because
a pick's price comes from the curve rather than the board — sound then, expiring soon. #232 recommends;
the owner decides.

## Owner acts outstanding

1. **Adopt or reject #225's derived values** when they arrive. Separate release, own word.
2. **The label for the baseline column** when the whole effort lands.
3. **The baked pick prices** — browser-computed, or a mandatory step of curve adoption.
4. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified, one read.
5. **#146** — parked until 412 needs a canvas. Its body inverted at D1; do not execute as written.
6. Referee harness scope — a fresh seat, owner-scheduled.

## Parked — do not start

Track D (five items, none touching the product) · the conservation gate (`gate_f5.py` cannot be wired as
written) · #139 items 6, 7 and 19 (eligibility and forward-lens work — ITEM 412 territory, and item 7
needs a store field that does not exist) · #139 item 8 (changes shape once #217 lands).

## Environment carries

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Integration hazard, hit by three branches in one day.** A rebase-merge rewrites SHAs, so a branch that
  keeps building on already-merged history presents those commits again under their original ids; the
  merge base rewinds past them and every touched file reads as an independent edit on both sides. Fix with
  `git rebase --onto origin/main <old-tip>`, then **verify the replayed diff is byte-identical** before
  pushing. **`git diff main..branch` on a stale-based branch is not a statement of what that branch
  changed** — diff against the branch's own merge base.
- **The seam can merge its own PRs.** The housing note describes whose credentials the merge runs under,
  not who may click it. Direct push to main is still classifier-blocked, so pens go branch → PR →
  rebase-merge. Ref deletion remains proxy-forbidden.
- **`sibling_repin` rewrites history every board move** — it overwrote two `5546f278` references, #208
  restored them, and it will do it again.
- The register header is **one ~375KB line**. Read it with a script that windows around a match — never
  `head` or `cat`.
- The Actions API can exceed per-call output caps; spill to a file and parse.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
