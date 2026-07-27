# CURRENT STATE — the incoming-seat read · v2, audited · supervisor pen · 2026-07-27, register v507

**WHAT THIS IS.** The condensed read for an incoming seat, so orientation costs ~18KB instead of the
register header's 323KB. It carries *what is true now*, *what the owner actually wants*, and *where
the history lives*.

**WHAT IT IS NOT.** Not the record. `docs/OPEN_ITEMS_REGISTER.md` is the single durable list and
remains append-only and complete. **Where the two disagree, the register wins and this file is
wrong.** This is a derived view, in the same sense the board is derived from the store.

**THE DISCIPLINE THAT KEEPS IT HONEST.** Part B is **REPLACED WHOLESALE every pen, never appended
to**. Part A changes only when a new class is named. A derived copy kept in sync by hand goes stale
silently — that is the `club_valuation.js` fault of 2026-07-27, and this file is the same shape.

**Audited** by a bare cold seat against the register; five findings raised and all corrected in this
version.

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
   re-pinning. The proof harnesses take ~71 minutes and are wired to nothing. The register grew until
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

---

# PART B — CURRENT STATE

*Replaced wholesale each pen. Accurate as of 2026-07-27 14:40Z, register v507.*

## WHAT THE OWNER WANTS — read this first, and work on these

Given directly 2026-07-27, in his order. **Nothing outside this list should be started without his
word.**

1. **Recalculate everything derived from the old store.** V0, the pick curve, priors, age curves —
   all fitted on the pre-restructure world. Positions moved for 538 players, picks for 615, and the
   rookie stream was split out of the national draft. **Nothing downstream is trustworthy until this
   is re-derived, and nobody has measured what changed.** This is the long-queued
   "RL_PVCFIT re-adoption". **Do this first — everything else sits on it.**
2. **Establish the referee and optimise the model to beat the blind challenger.** The protocol is
   frozen and ready; **the harness that runs the scoring has never been built.** That is the only
   blocker. Build it *after* (1) or it scores against stale priors.
3. **ITEM 412 pricing** — genuinely independent, can start now.
4. **Round 20 scores + live local updating.** Tooling is built and merged; the switch is off by the
   owner's own decision (2026-07-12). Its one dependency was D2, merging now.
5. **Run the engine locally without the bake ceremony** — a new LTI or a positional change should not
   need a 48-stage procedure. Owner ruling: **after (2)**, because he does not want to work locally
   on something not yet in a satisfactory state.
6. **Off-season transformation spec** — new positions, draftees entering, ageing, retirements. A
   46-line runbook exists at `docs/archive/pre-mvp-2026-07/SPEC_SEASON_ROLLOVER_v1_2026-07-16.md`,
   but it predates the restructure and knows nothing of the stream split. A starting point, not a
   spec.

## Where the two long-running items stand

### ITEM 411 · D1 — store restructure · **LANDED**
Merged to main 2026-07-27 at `efaaa7fc` — true two-parent (`663d1a7` + `45d9808`), authored
supervisor-411, register v507 preserved, zero product bytes differing from the branch tip.
Store `f37d9716 → c120cfd5`, board `6f07f7cb → fa172ac1`. 2,651 players; 1,035 position and 615 pick
corrections; **zero unattributed movement, proven as an exact bijection over 10,444 field edits plus
one removal, independently re-run by three parties.** Class-(c) defects across the item: **zero**.
Remaining: four suites terminal on the merge commit (three green, Live Scoring running at pen time),
then the staging branch is deleted. *History: v408–v507; the landing v496–v507.*

### ITEM 408 · D2 — forward-lens integration · **MERGING**
`ci/item-408-d2-staging` @ `537eb5d`, nine commits, four suites green attempt-1, cold review
discharged in full across three passes. **Zero conflicts with main.** Carries the binding pre-R20
deadline — the projection must follow the live board from the R20 bake onward.
*History: **v422** (the ruling that creates the deadline), v443, v448, v461–v507.*

### ITEM 410 — referee · **FROZEN, HARNESS UNBUILT**
`docs/referee/REFEREE_PROTOCOL.md` v1.0 FROZEN (owner word, v407); the AUD-004 specification of
record, amendable only by owner-worded version bump. **v1.1 amendment drafted** at
`docs/referee/AMENDMENT_v1_1_DRAFT.md`, awaiting the owner's word now D1 has landed. The harness is
owner priority 2. *History: v390–v407, v472.*

### ITEM 412 — pricing · **OPEN, NOT STARTED**
Sealed structure: PVC covers ND picks 1–64 with an empirical shape and pool asymptote; positional
POOL for ND 65+/post-draft/RD; SSP/MSD as observation lanes. First deliverable: **re-key the
replacement bar from position to eligibility**, scoped **current season only** by owner word — that
scoping is what makes it small, since it needs no future-eligibility field. G-MONO rulebook wording
drafts alongside the curve spec. *History: v438/v439, v441/v445, v497–v503, **v507**.*

## Owner words of record — the unchallengeable set

A seam ruling is revisable on evidence. These are not.

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
| **The governing test** (Part A) and the six priorities above | 2026-07-27 |

## Outstanding owner acts

1. **v1.1 amendment word** — draft filed, one read. Now unblocked.
2. **G-MONO rulebook + twin wording** — later, with 412's curve spec. Law-10: exact wording pre-filed.
3. **Maintenance-lane trigger word** — his priority 5, after priority 2.
4. **Rightsizing** — lighter ceremony post-landing was queued for him to word *at the viewing*; the
   viewing passed without it. Not blocking; the register's own list omits it too.
5. *Optional:* revoke the unused ceremony PAT. Off-repo, owner-attested only.

## Landing checklist

| # | item | state |
|---|---|---|
| 1 | T1 panel re-pin — **four surfaces**: `run_panel.sh:43`, the `expected_boot.json` panel block, the panel **narrative**, and the **regenerated UI bundle**. Never `PANEL_EXPECTED.txt` (zero executable readers) | **DONE** `f293d91` |
| 2 | `release_contract` narrative conforms at the re-seal | **DONE** `f293d91` |
| 3 | Live-tip integration — supervisor proposes, owner words | **DONE** — merge commit, owner-worded |
| 4 | The staging branch dies at the landing decision | open, after the merge-commit suites |
| 5 | R3 RULING-CONFIG + CONFIG-MANIFEST integrity | **DISCHARGED** — both executed and passed at `45d9808` |
| 6 | The transform files | **DONE** `5863646` |
| 7 | Stale committed `invariant_proof.json` — CI regenerates it | noted, out of scope |

**Standing predicate:** conforming a *true* statement about the old world can silently manufacture an
*untrue* claim of acceptance about the new one.

## Seats

| seat | state |
|---|---|
| **seam + pen** | seated 2026-07-27. Rotates on a **verification-accuracy slip**, not on schedule — its errors have been method, not depth. |
| **supervisor-411** | carries to the merge; **revisit after landing** — not a scheduled rotation. **Any degradation sign rotates immediately, regardless of depth.** |
| **supervisor-408** | **rotated 2026-07-27**; successor seated and read-back verified. Its environment does **not** reach `workbench.md` — environment-specific, not a retraction of v460. |
| **cold reviewers** | d1-cold-review and d2-cold-review both discharged; state-doc-audit filed five findings on this document. |

Live seat depths are deliberately **not** recorded here: they exist only in chat, cannot be checked
against the repo, and are stale within hours. **Capability maps vary per environment and are
re-tested per seat, never inherited.**

## Parked — low priority by owner ruling, do not start

- **Track D**, five items, all in *test harnesses*, none touching the engine or board: the two long
  proofs aren't CI-wired; one test line that cannot fail; two round-19 pins that will throw noise at
  R20; formatting padding; a boolean/string field inconsistency. **None can stop the project working.**
- **Conservation gate.** `gate_f5.py` **cannot be wired as written** — its input board exists nowhere
  in the tree, its path and epoch are hardcoded, its comparison side is a static July file. The law is
  reusable; the file is not. Placement, *seam ruling not owner word*: inside the advance transaction,
  before commit. Scheduled before ITEM 412's pricing work. Figures: entrant intake 83,538
  (69,266 + 14,272, seal `a17aafed`); realised totals 770,987 / 771,152 / 752,427; band −1.2% / +1.7%.
- **CI parallelisation** — owner-directed and in flight with 408: six proofs run sequentially for ~71
  minutes; as concurrent jobs, ~20. Scheduling change only, no coverage narrowing.

## Environment carries

- Containers **shallow-clone by default**. `git fetch --unshallow` before any ancestry claim.
- Run **`bootstrap.sh`**, not `setup_env.sh` alone — `unidecode` is vendored and seeded by bootstrap.
- A numpy env-pin hash mismatch blocks config-of-record board builds in at least one review container.
  Pre-existing, outside any current scope.
- *Observed this session, not register-sourced:* the Actions API can exceed per-call output caps;
  spill to a file and parse rather than re-pulling.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
