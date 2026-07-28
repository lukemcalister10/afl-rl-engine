# CURRENT STATE — the incoming-seat read · v14 · supervisor pen · 2026-07-28, register v522

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

*Replaced wholesale each pen. Accurate as of 2026-07-28, register v522, written against main `3d31692`.*

**Reading the figures below:** anything marked *seam-verified* was re-derived by the seam from the artifact
by re-running, not by reading. Everything else is the reporting seat's own measurement, named so you can
weigh it. Where it matters, re-run rather than inherit.

## THE ONE THING GATING EVERYTHING — read this first

**The owner is rebuilding positional data for every player-season from scratch.** Nothing derives a value
until that lands. This is not a delay to work around; it is the fix that four separate threads all turned
out to need.

**Why.** The store's positions disagree with the owner's own eligibility in ways that reach valuation, and
every attempt to shortcut it has produced a partial answer. The owner's words: *"This issue and trying to
shortcut it has gone on for too long and that is the only way to fix it for good."*

**The four-field model, owner's words 2026-07-28 — this is the specification:**

> **Drafted position:** what bucket their career performance as a whole goes to credit, value wise.
> **Career position:** the position they played for most of their career — so the position that their career
> historical performance is attributed to and measured against for replacement reasons.
> **Future position:** the position they will play from this point forward. For modelling their performance
> in the future.
> Eligibility is a different layer and projects what replacement bar they would be measured against for the
> current and future seasons (for the future eligibility blend).

Career position resolves to **per-season eligibility**, sourced rather than judged — SuperCoach assigns it,
so it is data, not 416 arguable calls. The owner is collecting DEF/MID/RUCK/FWD plus an `is_key` flag, which
generates exactly the six model codes, with per-player overrides for the career-long borderline cases.

**Three of the four already exist in the engine:** drafted is `pos`, future position is `_futpos`/`gfut()`,
the future blend is `futblend()`, already wired at `proj_from_peak(…, fut=futblend(p))`. Only per-season
eligibility is new.

**Size of the data job, seam-verified:** **11,264 player-season records across 1,924 store rows carrying
scoring, seasons 2005–2026**, flat at ~600–670 records a year from 2011. **Not** the 804 active board — the
fit trains on the full cohort, and the retired players are precisely who populates the older seasons.

**Decide before collecting, not after:** what happens to a player-season with no eligibility recorded. A
silent fallback to drafted position puts you back where you started for exactly the seasons you could not
source, and it will not announce itself. Exclude, halt, or a named default — any is defensible; silence is not.

**And state the vocabulary before any count.** Four spellings of six positions are live: the owner's sheet
(`G-DEF`), the store (`GDEF`), the board (`GEN_DEF`), and SuperCoach's. This has produced phantom findings
twice — 556 differences once, and #232 caught itself at 73 last night.

## WHAT THE CURRENT WORK IS FOR — unchanged and still binding

**Owner's words, 2026-07-28:**

> Right now, we are doing apples for apples conversion of the new store and ND/RD/Pool split into the
> current system. Anything else would be redefining HOW we model or HOW we value, which is the job of the
> referee project which comes next, and 412. This is about establishing a correct baseline with our new
> information to compare to.

**The method is held constant. Only the data and the separation change.** The `× 0.6` blend ceiling stays,
the isotonic step stays, the low-sample pooling stays. Known defects are reported, not repaired.

**Sequence:** positional rebuild → re-derive (#225's successor) → owner adoption → the referee project → ITEM 412.

## THE PRICING STRUCTURE — ruled, and law since 2026-07-28

**The national curve covers picks 1–64.** Everything past 64 enters a **pool**: ND 65+, all rookie draft, all
post-draft selections. Valued **by position**; order of selection carries no value inside it. SSP and MSD are
pool-valued but tracked separately.

**There is no price for pick 70.** If you are asking what a pick past 64 is worth, you have reverted.

`RULEBOOK.md` v2.1 law 4 (G-MONO) scopes strict descent to picks 1–64; the pool is outside it. **No further
rulebook change is needed.**

## THE CRITICAL FACT ABOUT THE CURVE

**The shipped pick curve is a LOADED ARTIFACT, not the in-engine fit.** `rl_export.py` loads
`pvc_curve_v2.json` and `PVC` *is* that artifact. `_merged_recover.py:1537` records **owner ruling R3 of
2026-07-09** holding the in-engine fit out of the bake, with a bake guard enforcing it.

**So cleaning the fit cannot move a shipped price.** The prices on the board today are still pre-split. The
baseline does not exist until the re-derivation lands and the owner adopts it.

**This ruling has now caused two seam errors, not one.** The second is recorded under the #241 scope error below.

## THE POSITION-BAR DEFECT — found 2026-07-28, not yet fixed

**The fit measures a player's career against his DRAFTED position's replacement bar, while the board prices
him against the position he PLAYED.** Same player, same career, two currencies.

**The engine already states the correct rule** at `rl_model.py:69`: *"drafted+developed a MID → feeds the MID
pool; plays FWD now → valued as a forward."* The board honours it. The fit does not.

**Owner's words:** *"It would make no sense for Moore to offer his owner that value, but then when we look
back and value him, nerf that value."*

Seam-verified: Dylan Moore, drafted MID pick 66, played GEN_FWD, career top-two 95.55 — contributes **15.47**
against the MID bar where the played bar gives **24.65**. **113 of 804 active players are drafted into one bar
and played into another; 68 would score better on the bar they played.**

**#241 was drafted to fix this and was NEVER FIRED, because the seam scoped it wrong.** See below. The
corrected site map is #225's, filed on that issue, and it is what a fix must cover.

## THE #241 SCOPE ERROR — the seam's, and it is the documented one repeating

The seam scoped the fix at `_nv_bwd` and `peakval`. Those feed `build_pvc`/`build_pvc_v34`/`_natcv34` — **the
in-engine fit that R3 holds out of the bake.** They cannot reach a shipped price. The seam named the two sites
that do not matter and missed the sites that do.

**#225 caught it and mapped it properly.** Its map, filed on #225 and organised by whether a site reaches `ev()`:

| group | what |
|---|---|
| **A** | eight value-path sites — `_explicit_peak` :608, `_v4_feats` :626, `_v4_draft_feat` :636, `_v4_spike_guard` :638, `los_decay`, `_role_decay_hc`, and the `PEAK_AGE`/`SPIKE_CAP` reads at :413/:433 |
| **B** | two build-on-one-axis-read-on-the-other cases — `BPK`/`MIX` and `_grpoffP`, where fixing the lookup without rebuilding the table leaves the mismatch and the table still reads clean |
| **C** | three in-engine/export sites R3 holds out of the bake |

Plus a **"not a defect, do not fix"** list for `bnow` and `grp3`, because an over-eager enumeration breaks
`bnow`'s deliberate fallback to drafted.

Seam-verified independently: `peak_est` reads `g=gfut(p)` then `cohort_peak(g,…)` while `BPK`/`MIX` are built
on `GRP[p['pos']]`; and `w=clamp(games/45,0,1)` puts **77.8%** of a 10-game player's peak estimate on the
drafted-position floor.

**Lesson for the record: the seam enumerated one axis. That is hazard 7, and it is the same shape as the
"three fit sites when there were five" error of two weeks ago.**

## IN FLIGHT

**Nothing.** All four seats have stood down. The positional rebuild is the owner's and off-seat.

| | |
|---|---|
| **#217 · engine split** | **LANDED** `6634221`. Split, pool-row exclusion at five fit sites, v0surf frozen with the silent fallback deleted. |
| **#231 · hand-pins** | **LANDED** `e3dc0be`. Four repairs plus a fifth instance, each shown failing. |
| **#232 · ownership sidecar** | **LANDED** `4ee1716`. A trade now costs an edit. |
| **#239 · FV Provenance** | **LANDED** `3d31692`. CI signal restored. |
| **#225 · derivation** | Candidate values delivered at `a5e7537`, **superseded** — they ride the old positional basis. The method, the both-directions check and the site map survive. |
| **#241 · position bar** | Drafted, **never fired**, scope was wrong. |
| **ITEM 412** | Owner's, off-seat. |

## Landed this cycle

- **#217** — the ruled split in the engine. Pool rows no longer teach the national curve, gated at all five fit
  sites with the check **observing what each site actually sampled** rather than re-deriving it. Seam-verified:
  breaking any one site alone fails the suite by name, and deleting a registration fails too. Board `750446d7`
  reproduced **byte-exact on a different container** — the cross-box evidence the implementing seat could not
  produce for itself. v0surf: 0 fits on a shipped build, HALT on an unknown signature, exactly 2 surfaces on a
  declared refit.
- **#231** — `EXPECTED_BOARD` **deleted, not re-pointed**; the fence reads the board of record from the bundle's
  own stamp. Its test split into a per-run invariant and a separate `adoption_gate.test.js` that is *not* wired
  into CI. `bootstrap_env.sh` discovers `python3.12` by name. The env-pin guard reads the dist-info WHEEL tag.
  Plus `extract_positions.py`, which had been halting on a three-moves-stale pin. Seam-verified by perturbation:
  tampering the bundle reds the test **and** kills the app together — which is what did not happen during the outage.
- **#232** — ownership and pick holdings on a live lane. One edit, one command, no engine run. openpyxl **removed**
  rather than satisfied (stdlib zip+xml, halts on an uncached cell). All 19 read sites migrated; the public tier
  bridges name→key and **fails closed** to `⚠ unverified` rather than guessing. Seam-verified: store, both board
  bundles and movers byte-identical; a raw-field read anywhere reds the suite.
- **#239** — all four FV Provenance failures were **one assertion at four sites**. GREEN2 gated on four conjuncts
  and printed three. Replaced the board proxy with live-computed `distribution_pricing_md5` / `rl_model_md5`
  comparisons, which name the mechanism instead of inferring it. **No board id in any gating check**, so nothing
  to edit when the board moves. 8/8 green in CI, verified from the run's own uploaded artifact.

## Corrections to the record — the register wins, and it was wrong on two counts

- **The `dnp` "known-bad data" entry is WITHDRAWN.** It claimed 87–92 players who *played* carry `dnp: true` in
  R15. **They did not play — their clubs had byes.** Seam-verified: R15 recorded 318 and R16 **319**, against
  405–410 in complete rounds; 4 teams × ~22 ≈ 88, two consecutive rounds short by the same amount. The count was
  real; the reading of it was invented — a figure against a denominator it had not earned, which is the fault the
  register elsewhere warns about. The flag is factually correct. **This does not prove the flag sound**; it means
  nobody has shown it wrong. #222's decision not to use it stands on its own reasoning.
  **One residual, one line:** the Movers tab's `DNP` pill does not distinguish "on a bye" from "omitted". The
  player card already sidesteps it — `history.js` deliberately refuses the bundle flag and recomputes from coverage.
- **The Kako selftest red is NOT a data defect and is NOT FIXED.** The anchor was typed when R19 was the latest
  round; R20 was applied, Kako scored 32, nothing re-typed it. Arithmetic: 10 @ 45.4 = 454, +32 = 486, ÷11 = 44.18,
  exactly what the store holds. **It fell through a commissioning gap of the seam's making** — the seam called it
  "a fifth item" for #231 while #231 independently found `extract_positions.py` and called that "the fifth instance".
  Two different things, one label. **Still live at `one_source_selftest.py:128`. Re-commission it.** Fix by
  round-scoping the anchor, not by retyping the number — precedent is #208 round-scoping the Bailey Williams
  override. It is an *owner ground-truth* anchor, so it must not derive its expectation from the store.
- **#225's pool-artifact finding was overstated.** It reported that the artifact cannot carry per-position pool
  values, measuring `pool_value` (a position-blind scalar) and `iso_corr` (3.9%). Seam-verified against the frozen
  V0 surface: **at pick 65 the per-position values span 446.5 (GEN_FWD) to 798.8 (RUC) — 78.9%**, comfortably more
  than the 57% the evidence asks for. V0 is a lookup keyed `(gfut, ageR, pick)`, not a scalar times a correction.
  The owner caught this. #225 has marked its §5 withdrawn rather than deleted.
- **The seam's own denominator error, third of the session:** it sized the positional data job at 4,257 records by
  filtering to the 804 active board, when the fit trains on the full cohort and the true figure is **11,264**. It
  then told the owner 2006–2014 was 4% of the data when it is **31.8%**. The owner caught it.

## CI — restored to one working signal, and read it correctly

**FV Provenance is green.** The other three — Final Integration, CI Guards, Live Scoring, and their `proof-*`
jobs — **were already red at `144cd33` and `df1b1cc`, before any of this cycle's work.** They are not attributable
to #217, #231, #232 or #239 and nobody has been commissioned to fix them.

**The seam broke FV Provenance by merging #217 without checking CI**, taking the signal from one-quarter working
to zero. #239 restored it. **Check the checks before merging** — that is now a standing act, not advice.

A PR will show ~1 of 20 green. That is the correct current state, not a failure of the branch under review.

## Known-bad, shipped, not commissioned

- **`RESULTS.json` is a committed false success signal.** It sits in the tree claiming `pass: 8/8` from the
  `06d8af60` era, and the workflow uploads whatever is on disk if a run cannot write it. Hazard class 4. Reported
  by #239, untouched because it was not asked for.
- **The baked pick prices in `ui/data/club_valuation.js` go stale when the curve moves.** #232 recommends computing
  them in the browser from the shipped curve, on #222's precedent. Owner decides; not urgent until the curve lands.
- **The dead baked-clubs block** in the same file — nothing reads it, and the parity test proves corrupting it
  changes nothing. A few lines whenever someone is in that file.
- **`extract_positions.py` regeneration is stamp-only** — seam-verified content-identical, provenance `06d8af60` →
  `8a38cca4`. Not committed, deliberately, to stay out of #232's lane. Safe to regenerate whenever.

## Owner acts outstanding

1. **The positional data.** Everything waits on it.
2. **Adopt or reject the derived values** when the re-derivation lands. Separate release, own word.
3. **The label for the baseline column** when the whole effort lands — one column, not one per board move.
4. **The baked pick prices** — browser-computed, or a mandatory step of curve adoption.
5. **v1.1 referee amendment** — draft at `docs/referee/AMENDMENT_v1_1_DRAFT.md`, verified, one read.
6. **#146** — parked until 412 needs a canvas. Its body inverted at D1; do not execute as written.
7. Referee harness scope — a fresh seat, owner-scheduled.

## For the referee project, filed not started

- **The four-field positional model** above, in the owner's words.
- **Eligibility should set the replacement bar, and today it cannot for single-eligibility players.**
  `y0dpp_bar` returns `None` below two eligibilities, so present position wins by default. Seam-verified: Reuben
  Ginbey is `present=KDEF`, `eligibilities=G-DEF`, so his season is floored against **KEY_DEF 68.4** where his
  eligibility implies **GEN_DEF 78.3** — an easier bar by 9.9. **159 of 804 have a bar mismatch; 62 are
  single-eligibility where no mechanism can engage; 36 of those get an easier bar.** Largest gaps −11.7.
  **Not measured: whether the floor binds, and what value actually moves.** That is 62 players whose bar comes
  from the wrong concept — *not* 36 players known to be overvalued. Sizing it is one build and would scope the
  referee work.
- **The 7 live DPP data-error rows** where present position is not in the collapsed eligibility set at all:
  Dewar, Flanders, Baker, **Langford**, **McGovern**, Langdon, Blicavs. Report-only, build continues.
- **97 of 804** where the store assigns a position the owner's sheet does not list as eligible — **57 outright,
  40 an extra**. #232's report at `session_2026-07-28/item232/position_crossref.txt`. Superseded by the rebuild,
  but it is the thread that surfaced all of this.

## Parked — do not start

Track D (five items) · the conservation gate (`gate_f5.py` cannot be wired as written) · #139 items 6, 7 and 19
(eligibility and forward-lens — ITEM 412 territory) · #139 item 8 · the three pre-existing red workflows.

## Standing norms set or corrected this cycle

- **Check the checks before merging.** The seam's own miss, now a standing act.
- **Use hands freely for read-only work** — enumeration, search, register pointer reads. That is what keeps a
  seat's context healthy and it should be the default. **But do not delegate a load-bearing measurement and
  report it as yours** — re-run the claim first; a hand's report is a hypothesis until reproduced.
  **Never run engine builds in parallel:** every build imports from the single workspace at
  `/home/claude/rl_workspace` and concurrent runs clobber each other. Fan out on reading, serialise on running.
- **When you write a ratio, name the population both numbers come from and check they are the same population.**
  Stated at v521 and violated by the seam twice more the same day.
- **A guard that always fails is the same defect as one that cannot.** #231's first fix asserted
  bundle-equals-manifest, which #217's deliberate hold made permanently red. Split by lifetime: per-run invariants
  in the suite, release conditions at the adoption step.

## Environment carries

- Containers **shallow-clone by default** — `git fetch --unshallow` before any ancestry claim.
- **Bare `python3` is 3.11 against a cp312-pinned lock, and system pip is PEP 668-blocked.** `bootstrap.sh`
  honours `RL_VENV`: build a 3.12 venv, `pip install --require-hashes --only-binary=:all: -r requirements-lock.txt`,
  then `RL_VENV=<venv> bash bootstrap.sh`. Do not patch the script or weaken the pin. #231 repaired the script's
  discovery; the venv is still needed here.
- **`v0surf` HALTs on an unknown config signature. That is the design.** Regenerate deliberately via
  `refit_v0surf.py --bake`. Do not restore a fallback or widen the accepted set.
  Its clean-instance precondition tests a **pre-split, unreachable** board — it cannot be evaluated. Say so; do
  not substitute.
- **Rebase hazard:** a rebase-merge rewrites SHAs, so `git diff main..branch` on a stale-based branch is not a
  statement of what that branch changed. Diff against the branch's own merge base, and verify the replayed diff
  byte-identical before pushing.
- **`sibling_repin` rewrites pins on every board move** and raises unless six structural tokens each match exactly
  once. Anything written into its targets must survive it — #239 verified this by running its parser and repair.
- The register header is **one ~387KB line**. Read it with a script that windows around a match — never `head` or `cat`.
- The Actions API can exceed per-call output caps; spill to a file and parse.
- **The seam can merge its own PRs.** Direct push to main is classifier-blocked, so pens go branch → PR →
  rebase-merge. Ref deletion remains proxy-forbidden.

---

*Pointers name register versions. The register header on `main` is the record; this file is the map.*
