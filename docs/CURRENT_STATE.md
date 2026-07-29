# CURRENT STATE — the incoming-seat read · v29 · supervisor pen · 2026-07-29, register v537

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

*Replaced wholesale each pen. Accurate 2026-07-29, register v537, written against main `d480564` — this
pen lands on top of it, so `main` will be one commit ahead. That is expected, not staleness.*

## THE INCOMING SEAT'S FIRST TWO TASKS

1. **Draft the re-derivation directive** for pre-fire audit — the next job after #262 lands, the
   biggest of the sequence. Every input is sealed: the spec section below; the eight-site value-path
   map on **closed issue #225** (still readable there); the three curve rulings below; and the output
   the owner needs — a new candidate board beside the current one, every mover attributed, for his
   adoption word. **Method held constant** (owner, 2026-07-28: *"apples for apples conversion... Anything
   else would be redefining HOW we model or HOW we value, which is the job of the referee project which
   comes next, and 412"*). The ×0.6 ceiling, isotonic step and low-sample pooling all stay.
2. **Verify #262's hand-back when it arrives.** Check by re-running: the two-stage proof (rename alone
   = zero value/rank movers; the owner's ~60 deliberate position edits then applied, every mover
   attributed); the rename's zero-live-hits sweep for old vocabulary; sibling re-pins in the landing
   commit — store, `engine_head`, `rl_model`, `fv` identities, **including the `held_candidates`
   candidate md5s in `release_contract.json`**; and CI green except Final Integration's one known red.
   Before merging any long-lived seat branch, diff it against current `main` first — see the
   cherry-pick rule under Environment.

## THE ONE THING GATING EVERYTHING: #262, IN EXECUTION

The owner's per-season positional data — **11,264 player-seasons across 1,924 scoring rows of 2,651
store records, seat-verified 1:1 against the sheet** — is landing now. **Read issue #262 in full:
body, Addendum 1 (STOP-and-ask: any sheet ambiguity goes to the owner as rows-plus-question, the seat
never guesses), Addendum 2 (the owner's complete nine-ruling set, including a ~24-player per-season
key table that supersedes the blanket `is_key` flag for those named), and the seam pre-fire audit.**
Settled — do not re-litigate:

- The landing is value-neutral except the owner's deliberate position edits, proven in two stages.
- Vocabulary is **replaced** repo-wide with the owner's new names — **KPF / KPD / SD / SF / MID /
  RUCK** — so any missed site fails visibly. DPP order is semantic: FWD→DEF→RUCK→MID.
- All ruckmen are key-position players: a DPP season containing RUCK renders its FWD/DEF component
  KPF/KPD regardless of flag; pure RUCK has no key variant.
- The 16 ownership changes route through the **#232 ownership sidecar command**, not store edits.
- The 727 zero-season busts get **no synthetic rows**; they count via draft records at the curve fit
  (ruling R1: busts full weight, no games floor, non-median fit — no survivor bias by design).
- The seat still owes the owner the Q3 review lists (9 key-flagged KDEF + 4 GFWD future-position rows).

**Sequence: land (#262) → re-derive → owner adoption → referee project → ITEM 412.**

## THE SPEC THE RE-DERIVATION EXECUTES

**The four-field model — owner's words, 2026-07-28:**

> **Drafted position:** what bucket their career performance as a whole goes to credit, value wise.
> **Career position:** the position they played for most of their career — so the position that their career
> historical performance is attributed to and measured against for replacement reasons.
> **Future position:** the position they will play from this point forward. For modelling their performance
> in the future.
> Eligibility is a different layer and projects what replacement bar they would be measured against for the
> current and future seasons (for the future eligibility blend).

Confirmed 2026-07-29: career position resolves to the per-season eligibility data (#262); current and
future collapse into one **modelling position** — where he plays from today, projected output priced
against current-season eligibility now and the eligibility blend later. Drafted position is only the
credit bucket for draft grading.

**The defect this fixes:** the fit measures careers against the DRAFTED position's bar while the board
prices the position PLAYED (`rl_model.py:69` states the correct rule; the board honours it, the fit
does not). Seam-verified: 113 of 804 split-bar, 68 better on the played bar, Dylan Moore 15.47 (MID
bar) vs 24.65 (played bar). **The corrected site map is on closed issue #225**: eight value-path
sites, two build-on-one-axis-read-on-the-other cases, three R3-held sites, and a do-not-fix list.
After #262, each season's output is measured against that season's eligibility bar.

**IN SCOPE FOR THE RE-DERIVATION, owner-confirmed 2026-07-29 (this was half-parked under the referee
filings and nearly mis-scoped):** the CURRENT and FUTURE season pricing bar comes from **eligibility**,
not present position — the spec's own sentence. Owner's example: Elliot Yeo is priced today as a pure MID
though he carries forward eligibility; going forward he prices as a forward for the current season. The
mechanism defect this cures is recorded (present position wins by default when the bar cannot engage —
the Ginbey case); the per-season data is what makes the fix possible. Only deeper redefinitions — how
bars are constructed, convexity, replacement levels — stay with the referee project.

**Three curve-input rulings (owner words sealed at v533):** Jeremy Cameron, Dylan Shiel and Adam
Treloar are **included** — the sheet assigns each a notional pick (12 / 4 / 14, 2011 ND); transcribed
as given. Paddy McCartin and Tom Boyd are **excluded force-majeure and every player in their drafts
slides up one pick** — verbatim reasoning at v533. Both are named exceptions to R1, not a method change.

**The ruled pricing structure (law since 2026-07-28):** the national curve covers **picks 1–64 only**;
everything past is a **pool** — ND 65+, all rookie draft, all post-draft — valued by position, order
carrying no value; SSP and MSD pool-valued, tracked separately. **There is no price for pick 70.**
`RULEBOOK.md` v2.1 law 4 already scopes this.

**The fact that has cost two seam cycles:** the shipped curve is a **loaded artifact**
(`pvc_curve_v2.json`, loaded by `rl_export.py`), held out of the bake by owner ruling **R3 of
2026-07-09** (`_merged_recover.py:1537`, bake guard enforcing). Cleaning any in-engine fit moves
nothing shipped. The app shows the **released pre-split board**; #217's split board sits in the tree
as a **declared held candidate** (`release_contract.json` `held_candidates`: three identities, both
sides pinned, only that exact pair excused; an undeclared mismatch still HALTs; the declaration is
deleted in the adoption commit and a surviving one is itself a rejection).

## CI — three of four green; what the last red means

**FV Provenance, CI Guards, Live Scoring: GREEN.** Final Integration is red on
**`club_curve_provenance` alone** (9/35): the engine carries the ruled 1–64 curve while the shipped
bundle correctly lags pre-split per the hold — its "every pick priced from the curve" proof cannot
hold while there is no price for pick 70. It resolves at re-derivation/adoption. **Do not regenerate
the frozen UI bundles to clear it.** Standing behaviours: the Kako store anchor reports **STALE at
R21** and names the owner act (by design — a small recurring owner touch, not a defect);
`invariant_proof.py --adoption` is the adoption-step lane (released-baseline equality lives there,
structural checks per-push); the six `proof-*` jobs are **manual-dispatch only** (they are the weekly
rehearsal set — run deliberately, once, when the engine changes).

## OWNER ACTS OUTSTANDING (none urgent)

1. Review #262's Q3 lists when the seat sends them.
2. **v1.1 referee amendment** — one read: `docs/referee/AMENDMENT_v1_1_DRAFT.md`.
3. **Baked pick prices** — browser-computed vs a mandatory adoption step; matters at curve adoption.
4. **Repo hygiene** (owner-raised 2026-07-29): a `main` ZIP is ~44MB and extraction is slow — identify
   what a working copy actually needs and clean stale files. One candidate job, after the landing era.
5. Branch delete-clicks (cosmetic) · real-iPhone check of `ui/index.html` (unproven; #139 item 22).
6. **Adoption word + the baseline column label**, when the re-derivation lands. One column per landed
   change, not one per rebuild.

## FILED FOR THE REFEREE PROJECT / PARKED — do not start

Referee filings (pointers in the register): the four-field model above; the deeper bar-construction
questions ONLY — *eligibility-sets-the-bar itself moved INTO the re-derivation scope by owner word
2026-07-29, see the spec section* (the `y0dpp_bar` mechanism numbers: 159 of 804 bar-mismatched, 62
single-eligibility, sizing unmeasured); 7 live DPP data-error rows (report-only); the 97-of-804 position crossref (superseded
by #262 but the originating thread). Parked: Track D · the conservation gate (`gate_f5.py` cannot be
wired as written) · #139 items 6, 7, 8, 19 · **#146 (body inverted at D1 — do not execute as written)**.

## RUNNING THIS SEAT WELL — learned the expensive way this cycle, owner-endorsed

- **Verify hand-backs by re-running only the two or three measurements that would change a decision**;
  delegate the reading (report ingestion, log pulls, bulk byte-compares) to hands. Fifteen inline checks
  where three decide is how the last seat burned half its context in a day.
- **Never pull raw GitHub API payloads into context** — spill to a file and parse, every time.
- **One register pen per boundary**, not per event. Docs-only pens **merge immediately** — their
  pre-commit structural asserts are the guard and a docs diff moves no workflow. Code diffs wait on
  exactly the checks they can move, no more.
- **Every fired directive is handed to the owner as a paste-ready relay in chat**; state model/effort
  only when deviating from Opus 5 at default. Call chats by the owner's names, not issue numbers.
- **Report in plain breakdowns**: what happened, what the owner must know or decide, with context.
  Lead with the outcome. No register-dialect. `DO:/WHY:` is retired by owner word.
- **Owner words seal promptly and on the issue first** — chat carries no authority; the pen follows at
  the boundary. A cancelled CI run is not a red. A guard that always fails is the same defect as one
  that cannot — split by lifetime. Every count names its denominator. Hands freely for reading; never
  delegate a load-bearing measurement; never run engine builds in parallel.
- **Check your own test can fail before believing it.** This cycle's seam caught three of its own broken
  test methods (a pipe's `$?`, bytes-vs-characters, tampering a field the gate never owned) — each
  looked like a finding until the method was checked. Effort scales with what a mistake costs to reverse.

## ENVIRONMENT CARRIES

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Bare `python3` is 3.11 against a cp312-pinned lock; system pip is PEP 668-blocked.** Build a 3.12
  venv, `pip install --require-hashes --only-binary=:all: -r requirements-lock.txt`, then
  `RL_VENV=<venv> bash bootstrap.sh`. Do not weaken the pin.
- **`v0surf` HALTs on an unknown config signature — that is the design.** Never restore a fallback or
  widen the frozen set; a halt is a finding.
- **After any rebase-merge, a long-lived seat branch must be recreated from `origin/main` by
  cherry-pick** — rebase-merges rewrite SHAs, so a stale-based branch's snapshot diff silently reverts
  landed work (one nearly reverted #251 plus three pens; caught only by diffing against `main` before
  merging). `git cherry` proves what is genuinely new. **Always diff a PR against current `main` before
  merging it.**
- **`sibling_repin` rewrites pins on every board move** and raises unless six structural tokens each
  match exactly once. `session_2026-07-20/fv_provenance_remediation/test_fv_provenance.py` is a live
  build input inside a session directory — session-archive exemptions must except it.
- The register header is **one ~400KB line** — read by pointer with a windowing script, never `head`
  or `cat`. The Actions API exceeds output caps — spill to a file and parse.
- **Pens**: branch → PR → rebase-merge; the seam merges its own PRs; ref deletion is owner-only.
  Mechanics: bump the version digit in the line-1 stamp (`supervisor pen · vNNN date · PEN:`) and
  insert `· SEAM vNNN (date) — <entry>` immediately before the trailing `· prior: ITEM 407`. Assert
  pre-commit: line count unchanged, byte growth equals entry bytes, single stamp, every prior entry
  intact, docs-only diff — and **measure in one unit**; the line's byte and character lengths differ
  by thousands.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
