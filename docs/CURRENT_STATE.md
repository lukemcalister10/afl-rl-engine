# CURRENT STATE — the incoming-seat read · v22 · supervisor pen · 2026-07-29, register v530

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

*Replaced wholesale each pen. Accurate 2026-07-29, register v530, written against main `50d5506` — this
pen lands on top of it, so `main` will be one commit ahead. That is expected, not staleness.*

*Figures marked **seam-verified** were re-derived by the seam by re-running. Everything else is the
reporting seat's own measurement. Where it matters, re-run rather than inherit.*

## THE ONE THING GATING EVERYTHING

**The owner is rebuilding positional data for every player-season from scratch. No value is derived until
that lands.** Four separate threads turned out to need it. His words: *"This issue and trying to shortcut
it has gone on for too long and that is the only way to fix it for good."*

**2026-07-29: the sheet is FINISHED, not yet landed.** Per-season eligibility (FWD/DEF/RUC/MID plus DPP
variants) against every store season, plus a player-level `is_key` column. The owner confirmed the model
collapse: current/future position is ONE field — the **modelling position** (where he plays from today,
used to project output; priced against current-season eligibility now, the eligibility blend later) — and a
separate career-position field is redundant because per-season eligibility *is* the career record. **Ruled
with it: the position vocabulary is REPLACED with new canonical names rather than merged to a variant** —
K-FWD→**KPF**, K-DEF→**KPD**, G-DEF→**SD**, G-FWD→**SF**, MID→**MID**, RUC/RUCK→**RUCK** — precisely so any
un-migrated site fails visibly instead of half-matching; the rename rides WITH the data landing, one
migration. **Two questions the owner still owes one line each:** does player-level `is_key` apply to every
season of the career (a tall who played general before becoming key would get the key bar for those
seasons); and the blank-cell rule — a season with no eligibility recorded must fail loudly or carry an
explicit marked default, never silently fall back to drafted position.

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
issue #225 (closed — the map is still readable there): eight value-path sites, two build-on-one-axis-read-on-the-other cases, three R3-held sites, and a
"do not fix these" list.** That map is the record. #241 is closed with the error stated on it.

The fix happens once, when the positional data lands, covering all sites on both axes — a one-bar-per-player
fix does not extend to a per-season bar.

## IN FLIGHT

| | |
|---|---|
| **positional sheet landing** | Owner's, off-seat: route the finished sheet in. The re-derivation directive drafts against it (spec + rename map above). |
| **#256 · finish the CI restore** | **FIRED by owner word 2026-07-29 ("Happy to commission it").** Part A: `invariant_proof.py`'s released-baseline equality checks move to the adoption step (structural invariants stay per-push; every check kept, moved, or explicitly retired — none silently dropped), proven both ways. Part B: the `_repo_root_of` regression — a root that cannot resolve fails loudly, never synthesizes from `/`; `live-scoring-light` green with production outputs byte-unmoved. Outcome: all four workflows green on a main push, or a report naming what surfaced next. |
| **positional rebuild** | Owner's, off-seat. Everything waits on it. |
| **ITEM 412** | Owner's, off-seat. |

Closed this cycle: #217, #231, #232, #239 (all landed), #225 (delivered, superseded), #241 (never fired),
**#244 (diagnosis delivered, seam-verified, merged `a22be828`)**, **#245 (landed `8073dcd`, seam-verified:
the Kako anchor is round-scoped and fails legibly when outrun; a run verdict can no longer outlive its
run — exit 0 requires all-pass AND a written verdict)**, **#251 (landed `d8462c8`, seam-verified: the
release gate understands a declared held candidate and still HALTs on anything undeclared — three tamper
directions re-run by the seam; the six proof jobs moved byte-exact to a manual workflow; one season-anchor
definition at both former constant sites, 32/32 + 11/11 + 31/31 re-run)**.

## CI — CORRECTED RECORD. Five causes, and the wall of red already cost one real catch

**The "red for a week" premise was WRONG.** All three workflows were **green at `a7dc1b4a`, 04:25:55Z
on 2026-07-28** — and at the five commits before it. First reds: **05:07:43Z** (`59d740ca` — CI Guards and
Final Integration) and **05:47:15Z** (`69e84580` — Live Scoring). They went red **during the R20 go-live**,
hours before this was written. Seam-verified: all five runs re-pulled from the Actions API. Also corrected:
`CI_MIGRATION_DIAGNOSIS.md` (repo root, 2026-07-22) had already diagnosed the *R19-era* reds — overtaken,
but the repo was never a blank page. And *cancelled* cells in old CI tables are concurrency cancellations —
no verdict either way.

**The full diagnosis is `session_2026-07-28/item244/CI_DIAGNOSIS.md`** (merged `a22be828`). Five causes:

| # | cause | hits | class |
|---|---|---|---|
| 1 | Kako R19 anchor, `one_source_selftest.py:128` | CI Guards | stale constant — **#245's job** |
| 2 | season-state R19 constants `0.727`/`c120cfd5` at **TWO sites**: `season_progress_test.py:73-75` AND `final-integration.yml:154` | Final Integration | stale constant, hazard 2 — fixing the test alone leaves the workflow red |
| 3 | `_repo_root_of` regression from `eb602b9` (`round_movers.py:529-531`) | live-scoring-light | real defect — **test harness only**: both production callers (`round_movers.py:747`, `round_finalize.py:314`) pass `repo_root=` explicitly, seam-read |
| 4 | v0surf frozen-signature HALT on a third, staged-build signature `65b9fbaf` (cause undetermined) | all six `proof-*` jobs | the design working — they structurally **cannot pass** as wired |
| 5 | **release-contract drift at #217** | Final Integration | real inconsistency — see below |

**Cause 5 is RESOLVED by #251's Part A** — and two details of the original diagnosis were corrected by that
seat and re-verified by the seam: **three identities were drifted, not one** (board, engine_head, rl_model —
all the same #217 hold, all now declared), and **divergence began at `4156d66`**, four commits before
`6634221`, in the same #217 series (v525 said "only at 6634221" from a six-commit sample — corrected).
The contract now carries an explicit `held_candidates` declaration: each entry pins both sides and a reason,
only that exact pair is excused, an undeclared mismatch HALTs exactly as before, and a declaration that
survives adoption is itself a rejection. Seam re-ran all three failure directions. FAIL (e) is resolved
(`season_progress_test` 31/31).

**What greens when.** **CI Guards is GREEN on main** — the owner's R20 re-anchor landed at `50d5506`
(guards success on both event runs of `764cf6e`, seam-parsed), and it un-skipped four guards that had not
executed since the anchor went stale, including the ~7-minute correction canary. By design it will report
STALE again at R21 and name the owner act. **Integration near-miss, recorded as a live hazard:** the
seat's first re-anchor branch sat on pre-rebase-merge history, and merging it would have silently reverted
#251's landing and three pens — caught only by diffing the branch against current main before merging
(1,867 deletion lines where a 6-line change belonged). After any rebase-merge, a long-lived seat branch
must be recreated from `origin/main` by cherry-pick; `git cherry` proves what is genuinely new. Final Integration: the gate and season anchors
now pass; **it halts at `invariant_proof.py`, 22/33** — hard-coded released-baseline totals
(`PRESENT_TOTAL 764021`, F5 `83538`/`4649`/`14272`, zero movers demanded) measured against the held
candidate board (`771772`, 749 movers — the ruled split working). Pre-existing, seat-verified identical on
stock main; confirmed from the run's own log by the seam. **Owner decision — same lifetime problem Part A
just solved**: split-by-lifetime says released-baseline equality is a release condition and belongs at the
adoption step, not the per-push suite. Live Scoring: `live-scoring-light` red on cause 3 — **corrected
blast radius: it fails CI's own run path too** (`accumulate_bundle` never reads `RL_REPO`; only an explicit
`repo_root=` argument helps, and the CI test caller doesn't pass one). The six proofs are manual-only now.

**No deletion finding.** Nothing fits "red for weeks, nobody noticed, caught nothing" — two of the three
caught real problems within hours of them landing. **Both open decisions were RULED 2026-07-29** — gate
learns a declared hold, proof jobs off every-push — and are commissioned as **#251** (filed, not fired).
The six `proof-*` jobs, for the record: each is a full weekly-update rehearsal in a scratch workspace
(two-round, catch-up, crash injection mid-run and mid-finalization, store writes, FV provenance). Built as
one-off proofs for the weekly-updater work; their future use is a deliberate one-shot rehearsal when the
positional rebuild changes the engine — which is why #251 keeps them runnable by hand rather than deleting
them.

**`fv-provenance` stays green** (repaired under #239) and is still the only fully working signal.
**Check the checks before merging** remains standing.

## KNOWN-BAD, NOT COMMISSIONED

- **The baked pick prices** in `ui/data/club_valuation.js` go stale when the curve moves. #232 recommends
  browser-computing them from the shipped curve, on #222's precedent. Owner decides; not urgent until the
  curve lands.
- **The dead baked-clubs block** in the same file — nothing reads it, corrupting it changes nothing.
- **`extract_positions.py` regeneration is stamp-only** — seam-verified content-identical. Safe whenever.
- **The `_repo_root_of` fallback** (cause 3 above) — real regression, and it breaks CI's own
  `live-scoring-light` run, not only the local no-argument path (#251 correction). Commissioning is owner
  decision 3 above.
- **A hidden red behind live-scoring-light's halt:** the Movers acceptance proof fails
  `0_production_populated_and_provenance_bridge` — 1 of 11 checks, never reported by CI (hazard 9).

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
- **A cancelled CI run is not a red.** Concurrency cancellations carry no verdict; reading them as failures
  helped the "red for a week" premise survive unexamined.
- **Report to the owner in plain breakdowns** (owner word 2026-07-29): what the agents did, what he needs to
  know or decide, with context — nothing verbose or dense, no register dialect. The charter's `DO:/WHY:`
  format is retired on the same word.
- **Seam context economy — three rules learned the expensive way this cycle** (the seat burned its own
  context in one day; owner raised it 2026-07-29): (1) **never pull raw GitHub API payloads into context** —
  every Actions/PR lookup goes through a spill-to-file + parse, or to a hand that returns the conclusion;
  (2) **one register pen per working session** at a natural boundary, not one per event — each pen costs a
  full PR/CI/merge cycle; (3) **delegate the reading half of verification to hands** (report ingestion, log
  pulling, bulk byte-comparison) and re-run inline only the two or three measurements that would change a
  decision. The verify-before-record norm is unchanged — this is about *where* the reading happens.
- **Check-the-checks is scoped by what the diff can move** (owner word 2026-07-29): a docs-only pen whose
  structural asserts prove the diff merges immediately — no CI wait; a code diff waits on exactly the
  checks it can move. Sub-agents: owner supports Opus 5 hands for anything safe to delegate, and directives
  to supervisors say so explicitly.
- **Every fired directive is handed to the owner as a paste-ready relay in chat** — the seam states model
  and effort only when deviating from Opus 5 at default; silence means no deviation. Chats are called by
  the owner's names for them, not by the current issue number — one chat has carried #231/#239/#245.

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
- **Pen mechanics, so no seat re-derives them:** a pen bumps the version digit in the line-1 stamp
  (`supervisor pen · vNNN date · PEN:`) and inserts `· SEAM vNNN (date) — <entry>` immediately before the
  trailing `· prior: ITEM 407`. Assert before commit: line count unchanged, byte growth equals entry bytes,
  single stamp, every prior `vNNN (date)` entry intact, docs-only diff. Measure in one unit — the line is
  multi-byte UTF-8, so its byte length and character length differ by thousands.
- The Actions API can exceed per-call output caps; spill to a file and parse.
- **The seam can merge its own PRs.** Direct push to main is classifier-blocked, so pens go branch → PR →
  rebase-merge. Ref deletion is proxy-forbidden.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
