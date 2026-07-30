# CURRENT STATE — the incoming-seat read · v34 · supervisor pen · 2026-07-30, register v542

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
(v34 · supervisor pen · 2026-07-30, register v542 · replaced wholesale at the shaping-rulings pen)

## THE ERA: POST-ADOPTION, POST-UI-WAVE. Main is `fe672cb`; ALL FOUR WORKFLOWS ARE GREEN — the first
all-green CI of the era. The #274 UI wave is MERGED (PR #282, rebase-merge, seven commits): era succession
landed (movers 65/65, the 30/7 boundary owner-approved, the A22 known-red CLEARED), the A19 Best-23
eligibility selector replaced the adoption stopgap (min-cost max-flow on the ELIGIBILITIES column; Adelaide/
Hawthorn resolve exactly as A19 measured), the over-free lens ships at FHV=190 computed at render, the ten
#139 display items verify green, and the adoption mop-up act re-stamped the F5 contract block to the adopted
77,611 (components 65,925 + 2,631 + 9,055; contract sha now e87ee7ce, self-verified), fixed the ui contract's
stale pool_value to 299 (its md5 now 11adecc8, FROZEN-RULER pin re-stamped in the same commit), restated the
R14-rewind claim honestly, and RETIRED the two R14→R19 replay steps (premise died at adoption; forward
replacement = #139 item 20, docketed not commissioned). The `movers.test.js` known-red era is OVER.
**#279 — the shaping step — has currency, basis, fitter and pin policy SEALED on-issue; the α dial is the ONE open ruling.** No other seat live.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Carried from v33 unchanged: FHV Option A (≈190, #270 ruling comment) · future-leg blend hand-set (#270
retirement comment) · year-0 bar = ELIGIBILITIES column (#271 A4/A6) · §1b retired by supersession (#271
A4/A5) · 62+3 edit set sealed (#271 A12) · held-mechanism law (#271 A11) · tie-sensitive instruments barred
(#271 A13) · Best-23 = A19 law (NOW LIVE via #274 item 2) · movers/era-succession law (#271 A15/A16; the
single-slot limit is FIXED by #274 item 1; the balanced_board_md5 three-way disagreement stays hygiene's,
now with a loud tripwire) · **G-Y0 dated exception STANDS**: 2.929% ruled / 3.035% guard HELD / 3.50%
ceiling = hard FAIL; resolves at step 4's re-derivation [#271 A12/A13]. NEW this cycle, on #279:
N1. **Currency = VOR (γ=1.0)** ["ruling is VOR. Lock it in"]. Echo of full adoption bounded: 21 rucks ≤29
    points via the ruck-cap channel alone; converged curve fixed point 817c0f5a; signature is curve-sensitive
    but γ-blind (the silent case = γ-only flip; RL_GAMMA enters the gates at step 4). [#279 currency ruling]
N2. **Basis = STRUCTURAL, teaching cut at class ≤2022, par = PER-SEASON teaching.** Concluded careers vote
    full (825), actives completed from concluded look-alikes busts-included (372 active, 301 completed),
    prior = counted thin-stratum fallback ONLY — a WATCHED NUMBER at every rebuild (5.93% at ruling). The
    99.975% prior-share finding is why. Truncation backtest: MAE 27/21/17% at depths 2/3/4, consistently
    optimistic (+4.7% at kept depths) — THE WATCH-ITEM if the curve ever reads generous. [#279 basis ruling]
N3. **Fitter = CONTROL** (shipped kernel + local-linear boundary correction, >1%-mass-off-domain rule).
    Panel evidence: held-out accuracy tied (medAE 377.1–377.4); the boundary fix wins picks 46–64 (~9% medAE;
    signed error +8.5 vs the kernel's +21.2); byte-identical to shipped at picks 3–50. Distribution-first =
    the kernel by algebraic identity (2.3e-13); its DECOMPOSITION (establishment rate × value-if-established)
    is ADOPTED as a standing report-only artifact beside the curve. [#279 fitter ruling]
N4. **Pin policy = POOLED NUMERAIRE, in principle.** The hard-set was an asymmetric CEILING (owner-caught):
    all four fitters put raw pick 2 above raw pick 1; the pin clipped ~140 measured points. Ruled design: PAVA
    pools the head honestly, then ONE global factor s = 3000/pooled-head re-denominates the WHOLE economy —
    players included — so pick 1 = 3000 is true, not decreed; conservation is s-invariant. CONFIRMATION
    CONDITION at step 4: the head-anchor noise measurement (pooled band vs raw pick 1, across fitters+folds)
    = the adoption-time churn; one owner word reverts to the hard pin if disqualifying. Player-side ×s
    executes at step 4 ONLY. [#279 fitter+pin ruling comment]
N5. **Pool ≈ tail equivalence (measured, this cycle):** under the ruled basis the pool level is 239.7
    [211,268] n=1,005 while picks 60–64's cohort earned 233 — statistically the same asset. The old
    "pool sits below the curve by construction" prose was an OLD-BASIS fact; the descent asserts bite over
    1–64 only, so nothing halts; one clarifying line lands in the law text at step 4. Priced denominators:
    MSD 303 n=44 · SSP 341 n=31 (STORE stream counts 106/52 are census, not pricing populations); medians ~0
    everywhere — the interval is the finding. These feed the FHV re-denomination word at #279's adoption.

## THE α STOP — the one open ruling of the shaping step
Six full ladders committed (α = 1.0/0.8/0.6, tiered 0.6→0.8, linear 0.8→1.00, linear 0.9→1.05), rebuilt on
the ruled design at the stop. Conservation at α=1: 0.998 — every downside setting slashes total pick value
(S-3's own bar); 0.9→1.05 is the only schedule paying above the honest mean at the tail (1.047× at 64,
conserving 0.988) — the owner's star-chance theory as a knob, both readings filed without a lean. Inter-
schedule differences at picks 1–3 are inside noise (effn 35–38). Seam recommendation on record: α=1.0.

## THE QUEUE — everything fires on an owner word; seam pre-fire audit at each fire
- **#279 step 4 (after the α word): PROPAGATION — the finale.** v0 surface refit under everything ruled ·
  curve re-derived to coherence, G-Y0 re-set honestly · RL_GAMMA into the signature gates (closes the γ-only
  blind spot) · the pool's ruled level ships · par per-season teaching (with the par_build LOUD-HALT
  requirement — empty position group must halt naming the group, never IndexError; the #274 map found the
  crash) · the player-side ×s rescale + the pin confirmation condition · the ruck-cap bite check (Stanley
  812→610 exposure measured, binding unknown) · draftval stale comment fix · the law-text clarification
  (digest N5). **REHEARSAL NORM APPLIES IN FULL:** first-of-a-kind runbook, rehearsed end-to-end in scratch
  before any owner execution word. #279's adoption then re-denominates FHV (one word; evidence in digest N5).
- **#283 — ownership single-source fix (FILED, ready):** store becomes truth, sidecar becomes generated
  mirror, oracle unchanged; the owner's July-29 CSV (18 moves, currently NOT on the board) is the acceptance
  fixture. The read-back must resolve the store-identity ripple lane (the crux; it's why #232 dodged the store).
- **#275 — hygiene: UNBLOCKED** (all-four-green baseline now exists). Carries the balanced_board_md5 anchor
  ruling and the RETENTION LAW (files cited by sealed records are protected — the adoption-review and item279
  evidence trees are now in that class).
- **#276 — clubs tab** (Q5/Q6 collectibles + optional FHV word at fire) · **#270 — referee** opens after #279
  delivers · #146 never as written · #139 feeds the others (item 20 = the retired replay's successor) · v1.1
  amendment read still outstanding (owner).

## OWNER ACTS OUTSTANDING
The α word (then step 4 fires on a second word after rehearsal) · fire words #283/#275/#276 · the v1.1 read ·
branch-delete clicks as they arise.

## RUNNING THIS SEAT WELL — owner-endorsed law (charter D3/D4 + both cycles' additions)
- Answer the owner HERE, completely, FIRST; filings are durable copies, never the reply. Plain sentences.
  His casual questions are load-bearing QC — this cycle they caught the frozen-ladder artifact in the γ
  evidence, the pick-1 ceiling, and the pool≈tail collision. Treat every one as an instrument.
- Cost-estimate norm before commissioning builds · rehearsal norm for first-of-a-kind lanes · subagents Opus
  by default, one-writer discipline, screen by deterministic re-run · spill API payloads to files · register
  by window only (the header is ONE ~450KB line) · every count NAMES ITS DENOMINATOR (store-census vs priced-
  population bit twice this cycle) · prove every instrument can fail BEFORE trusting it (the judge was proven
  able to fail before any fitter was scored; the emit scripts now HALT on missing whitelist vars — silent
  defaulting is one defect class) · **NEVER present numbers not read from a committed artifact — the seam
  itself fabricated two interpolated table columns this cycle, self-caught mid-message; read-verbatim is the
  only guard** · medAE flatters low curves where medians are ~0: judge means with mean-targeting instruments
  (signed error / RMSE) alongside · a held-out judge refuses mismatched fold fingerprints.
- One pen per boundary, batched. Hand-backs: re-run the 2–3 measurements that decide; full content-level
  verification at final seals (the #282 seal pattern: fence audit on the whole diff, CI via API not summary,
  byte-level pin checks). Post-rebase-merge: re-verify main by CONTENT (rebase rewrites SHAs).

## ENVIRONMENT CARRIES
cp312 via RL_VENV (do not weaken; container python3 is 3.11 — always the pinned interpreter) · git fetch
--unshallow before ancestry claims · no parallel engine builds without seam coordination · detached-worktree
discipline per #271 A13 (env -i with an EXPLICIT whitelist — the env -i path-stripping incident is the
cautionary tale) · CRLF in the owner's CSV lane is a known Excel artifact, never "fixed" · GitHub rebase-merge
rewrites SHAs: seal by content.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen (expect the v542 pen commit or a descendant);
   open PRs (expect none, or the v542 pen PR itself pre-merge); the issue map above; all-four-green CI.
2. The #279 seat holds at the α stop with ~630k context: its step-3 segment ends at the α ruling — verify its
   final hand-back against the committed pack, then it rotates; STEP 4 GETS A FRESH SEAT with an opener built
   from #279's body + the four ruling comments + this Part B's step-4 queue entry.
3. Read-back to the owner in his channel; hold for confirmation before any push.
