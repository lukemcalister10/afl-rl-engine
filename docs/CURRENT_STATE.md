# CURRENT STATE — the incoming-seat read · v15 · supervisor pen · 2026-07-28, register v523

**WHAT THIS IS.** The condensed read for an incoming seat, so orientation costs ~20KB instead of the
register header's ~395KB. It carries *what is true now*, *what the owner actually wants*, and *where
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

*Replaced wholesale each pen. Accurate 2026-07-28, register v523, against main `4fe4781`.*

*Figures marked **seam-verified** were re-derived by the seam by re-running. Everything else is the
reporting seat's own measurement. Where it matters, re-run rather than inherit.*

## THE ONE THING GATING EVERYTHING

**The owner is rebuilding positional data for every player-season from scratch. No value is derived until
that lands.** Four separate threads turned out to need it. His words: *"This issue and trying to shortcut
it has gone on for too long and that is the only way to fix it for good."*

**The four-field model — owner's words, 2026-07-28, the specification:**

> **Drafted position:** what bucket their career performance as a whole goes to credit, value wise.
> **Career position:** the position they played for most of their career — so the position that their career
> historical performance is attributed to and measured against for replacement reasons.
> **Future position:** the position they will play from this point forward. For modelling their performance
> in the future.
> Eligibility is a different layer and projects what replacement bar they would be measured against for the
> current and future seasons (for the future eligibility blend).

Career position resolves to **per-season eligibility — sourced, not judged**, which is why it beats the ~416
judgement calls a single `career_position` field would have cost. Collection is DEF/MID/RUCK/FWD plus an
`is_key` flag, generating the six model codes.

**Three of the four already exist:** drafted is `pos`, future is `_futpos`/`gfut()`, the blend is `futblend()`.
Only per-season eligibility is new.

**Size, seam-verified: 11,264 player-season records across 1,924 store rows carrying scoring, 2005–2026.**
Not the 804 active board — the fit trains on the full cohort, and retired players populate the older seasons.

**Two things to settle before the data is trusted.** What happens to a season with no eligibility recorded —
a silent fallback to drafted position puts you back where you started for exactly the seasons you could not
source. And the vocabulary: four spellings of six positions are live (sheet `G-DEF`, store `GDEF`, board
`GEN_DEF`, SuperCoach's). That has produced phantom findings twice — 556 differences once, 73 caught before
filing last night.

## WHAT THE CURRENT WORK IS FOR

**Owner's words, 2026-07-28:**

> Right now, we are doing apples for apples conversion of the new store and ND/RD/Pool split into the current
> system. Anything else would be redefining HOW we model or HOW we value, which is the job of the referee
> project which comes next, and 412. This is about establishing a correct baseline with our new information
> to compare to.

**Method held constant; only data and separation change.** The `× 0.6` ceiling, the isotonic step and the
low-sample pooling all stay. Known defects are reported, not repaired. If you are improving a calculation you
have left the job.

**Sequence:** positional rebuild → re-derive → owner adoption → referee project → ITEM 412.

## THE RULED PRICING STRUCTURE — law since 2026-07-28

The national curve covers **picks 1–64**. Everything past enters a **pool** — ND 65+, all rookie draft, all
post-draft selections — valued **by position**, with order of selection carrying no value. SSP and MSD are
pool-valued, tracked separately.

**There is no price for pick 70.** If you are asking what a pick past 64 is worth, you have reverted.
`RULEBOOK.md` v2.1 law 4 scopes strict descent to 1–64; no further rulebook change is needed.

## THE FACT THAT HAS COST TWO SEAM CYCLES

**The shipped pick curve is a LOADED ARTIFACT, not the in-engine fit.** `rl_export.py` loads
`pvc_curve_v2.json` and `PVC` *is* that artifact. `_merged_recover.py:1537` records **owner ruling R3 of
2026-07-09** holding the in-engine fit out of the bake, with a bake guard enforcing it.

**So cleaning the fit cannot move a shipped price.** The board today is still pre-split. The baseline does not
exist until the re-derivation lands and the owner adopts it.

It has now caused two seam errors: asserting a fitted number could move a price, and then scoping a fix at
two sites that R3 holds out of the bake — see below.

## THE POSITION-BAR DEFECT — real, mapped, not yet fixed

**The fit measures a career against the DRAFTED position's replacement bar while the board prices the player
against the position he PLAYED.** Same career, two currencies. `rl_model.py:69` already states the correct
rule — *"drafted+developed a MID → feeds the MID pool; plays FWD now → valued as a forward"* — and the board
honours it. The fit does not.

Seam-verified: Dylan Moore contributes **15.47** against the MID bar where the played bar gives **24.65**.
**113 of 804** are drafted into one bar and played into another; **68** would score better on the played bar.

**#241 was drafted to fix this, was never fired, and its scope was wrong** — the seam named `_nv_bwd` and
`peakval`, which R3 holds out of the bake, and missed the value path. **#225 filed the corrected site map on
issue #225: eight value-path sites, two build-on-one-axis-read-on-the-other cases, three R3-held sites, and a
"do not fix these" list.** That map is the record. #241 is closed with the error stated on it.

The fix happens once, when the positional data lands, covering all sites on both axes — a one-bar-per-player
fix does not extend to a per-season bar.

## IN FLIGHT

| | |
|---|---|
| **#244 · CI diagnosis** | **DIAGNOSE ONLY, fixes nothing.** Why are Final Integration, CI Guards and Live Scoring red, and are they worth keeping? Deleting a workflow is an allowed finding. |
| **#245 · two stale signals** | The Kako ground-truth anchor (the last red in the selftest) and a committed `RESULTS.json` claiming `8/8`. |
| **positional rebuild** | Owner's, off-seat. Everything waits on it. |
| **ITEM 412** | Owner's, off-seat. |

Closed this cycle: #217, #231, #232, #239 (all landed), #225 (delivered, superseded), #241 (never fired).

## LANDED THIS CYCLE

- **#217 · engine split** `6634221` — the ruled split; pool rows excluded at all five fit sites, with the
  check **observing each site's actual sampled rows** rather than re-deriving them. `v0surf` frozen and its
  silent refit fallback deleted. Seam-verified: breaking any one site alone fails by name; board `750446d7`
  reproduced **byte-exact on a second container**.
- **#231 · hand-pins** `e3dc0be` — `EXPECTED_BOARD` **deleted, not re-pointed**; the fence reads the bundle's
  own stamp. Test split into a per-run invariant plus a non-CI `adoption_gate`. `bootstrap_env.sh` finds
  `python3.12` by name; the env-pin guard reads the dist-info WHEEL tag. Seam-verified: tampering the bundle
  reds the test **and** kills the app together — which is what did not happen during the outage.
- **#232 · ownership sidecar** `4ee1716` — **a trade now costs an edit**: one command, no engine run. openpyxl
  removed rather than satisfied. All 19 read sites migrated; the public tier bridges name→key and **fails
  closed**. Seam-verified: store, both board bundles and movers byte-identical.
- **#239 · FV Provenance** `3d31692` — all four failures were **one assertion at four sites**; GREEN2 gated on
  four conjuncts and printed three. Board proxy replaced with live-computed provenance md5s. **No board id in
  any gating check.** 8/8 green.

## CORRECTIONS TO THE RECORD

- **The `dnp` "known-bad" entry is WITHDRAWN.** It claimed 87–92 players who *played* carry `dnp: true` in
  R15. They did not play — their clubs had byes. Seam-verified: R15 recorded 318 and R16 **319**, against
  405–410 in complete rounds. Two consecutive rounds short by the same amount is a structural cause. The count
  was real; the reading was invented. **This does not prove the flag sound** — only that nobody has shown it
  wrong. Residual, one line: the Movers `DNP` pill does not distinguish bye from omission.
- **#225's pool-artifact finding was overstated**, caught by the owner. The frozen V0 surface carries a
  **78.9%** positional spread at pick 65 (GEN_FWD 446.5 → RUC 798.8) against the 57% the evidence asks for —
  V0 is a lookup keyed `(gfut, ageR, pick)`, not a scalar times a correction. §5 marked withdrawn on the branch.
- **The seam made three denominator errors in one session**, all caught by others: "two board moves", "96
  players", and sizing the positional job at 4,257 records by filtering to the active board when the true
  figure is 11,264. **When you write a ratio, name the population both numbers come from and check they are
  the same population.**

## CI — one working signal, read it correctly

**`fv-provenance` is green.** The other three — Final Integration, CI Guards, Live Scoring and their `proof-*`
jobs — **were already red at `144cd33`, before this cycle's work**. Nobody has ever diagnosed why; #244 is
doing that now.

**The seam broke `fv-provenance` by merging #217 without checking CI**, taking the signal from one-quarter
working to zero. **Check the checks before merging** is now a standing act. A PR showing ~1 of 20 green is the
correct current state, not a failure of the branch under review.

## KNOWN-BAD, NOT COMMISSIONED

- **The baked pick prices** in `ui/data/club_valuation.js` go stale when the curve moves. #232 recommends
  browser-computing them from the shipped curve, on #222's precedent. Owner decides; not urgent until the
  curve lands.
- **The dead baked-clubs block** in the same file — nothing reads it, corrupting it changes nothing.
- **`extract_positions.py` regeneration is stamp-only** — seam-verified content-identical. Safe whenever.

## OWNER ACTS OUTSTANDING

1. **The positional data.** Everything waits on it.
2. **Adopt or reject the derived values** when the re-derivation lands — separate release, own word.
3. **The baseline column label** when the whole effort lands. One column, not one per board move.
4. **The baked pick prices** — browser-computed, or a mandatory step of curve adoption.
5. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified, one read.
6. **#146** — parked until 412 needs a canvas. Its body inverted at D1; do not execute as written.
7. Referee harness scope — a fresh seat, owner-scheduled.

## FILED FOR THE REFEREE PROJECT — not started

- The **four-field positional model** above, in the owner's words.
- **Eligibility should set the replacement bar, and today it cannot for single-eligibility players.**
  `y0dpp_bar` returns `None` below two eligibilities, so present position wins by default. Ginbey is floored
  against KEY_DEF 68.4 where his eligibility implies GEN_DEF 78.3. **159 of 804 have a bar mismatch; 62 are
  single-eligibility with no mechanism to engage; 36 of those get an easier bar.** *Not measured: whether the
  floor binds, or what value moves.* Sizing it is one build and would scope the referee work.
- **7 live DPP data-error rows** where present position is not in the collapsed eligibility set: Dewar,
  Flanders, Baker, Langford, McGovern, Langdon, Blicavs. Report-only.
- **97 of 804** where the store assigns a position the owner's sheet does not list as eligible — 57 outright,
  40 an extra. `session_2026-07-28/item232/position_crossref.txt`. Superseded by the rebuild, but it is the
  thread that surfaced all of this.

## PARKED — do not start

Track D · the conservation gate (`gate_f5.py` cannot be wired as written) · #139 items 6, 7, 8 and 19.

## NORMS SET OR CORRECTED THIS CYCLE

- **Check the checks before merging.**
- **Use hands freely for read-only work** — enumeration, search, register pointer reads. That is the default
  and it is what keeps a seat's context healthy. **But never delegate a load-bearing measurement and report it
  as yours** — re-run the claim first; a hand's report is a hypothesis until reproduced. **Never run engine
  builds in parallel** — every build imports from the single workspace and concurrent runs clobber each other.
  Fan out on reading, serialise on running.
- **A guard that always fails is the same defect as one that cannot.** #231's first fix asserted
  bundle-equals-manifest, which #217's deliberate hold made permanently red. Split by lifetime: per-run
  invariants in the suite, release conditions at the adoption step.
- **Every count names its denominator.**

## ENVIRONMENT CARRIES

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Bare `python3` is 3.11 against a cp312-pinned lock; system pip is PEP 668-blocked.** `bootstrap.sh`
  honours `RL_VENV`: build a 3.12 venv, `pip install --require-hashes --only-binary=:all: -r
  requirements-lock.txt`, then `RL_VENV=<venv> bash bootstrap.sh`. Do not patch it or weaken the pin.
- **`v0surf` HALTs on an unknown config signature. That is the design.** Regenerate deliberately via
  `refit_v0surf.py --bake`; never restore a fallback. Its clean-instance precondition tests a pre-split,
  unreachable board and **cannot be evaluated** — say so rather than substitute.
- **Rebase hazard:** a rebase-merge rewrites SHAs, so `git diff main..branch` on a stale-based branch is not a
  statement of what that branch changed. Diff against the branch's own merge base and verify the replayed diff
  byte-identical before pushing.
- **`sibling_repin` rewrites pins on every board move** and raises unless six structural tokens each match
  exactly once. Anything written into its targets must survive it.
- The register header is **one ~395KB line** — read by pointer, never `head` or `cat`.
- The Actions API can exceed per-call output caps; spill to a file and parse.
- **The seam can merge its own PRs.** Direct push to main is classifier-blocked, so pens go branch → PR →
  rebase-merge. Ref deletion is proxy-forbidden.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
