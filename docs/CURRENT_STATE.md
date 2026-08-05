# CURRENT STATE — the incoming-seat read · v62 · supervisor pen · 2026-08-05, register v570

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

## THE OWNER'S PRODUCT LAWS (2026-08-04, the v562 correction — read these before touching the surface)

> *"The core tenet of this project was to value picks, and recognise that different intersections
> have different effects."*
> *"A key defender at pick 6 may be, and probably should be, worth less than pick 6, but at pick 45,
> maybe it's worth more. It could be by lots, or not by much. It's that simple: we have the data."*

- **LAW (intersections):** the year-zero surface is a TRUE position × age × pick surface — per
  position/age the data draws a line along the pick axis, below the curve where the data says below,
  above where it says above, **crossing freely**. A position dial constant across picks is BARRED.
- **LAW (no hard bands):** no hard banding on any axis, **in the implementation OR in the
  presentation of results**. Every pick its own value; neighbouring picks near-identical; locality
  binds (*"I don't care for pick 20s data in considering pick 1"*). Report per-pick or smooth
  curves, never buckets.
- These were violated once, by a seam-approved design (v561, voided v562). The audit of any surface
  design checks these laws FIRST, and the load-bearing property of any design is stated to the owner
  in one plain sentence before approval is even discussed.

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
| 15 | **A label is not a compute path** | identical CPU string + byte-identical pins, divergent fitted bytes; a box is classified only by reproducing output bytes | v560 |
| 16 | **A correct audit of the wrong question** | every figure re-runs byte-identical, yet the design contradicts the owner's stated intent — mechanics verified, intent unchecked; the owner had to extract the load-bearing property himself | v562 |

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
path**: branch → PR → rebase-merge. The merge under the owner's platform auth is a **housing fact,
not an approval step**. Docs-only pens land **without a per-entry word** (v483, restored by owner
word 2026-07-27), guarded by structural asserts proven pre-commit: line count unchanged, growth equal
to entry length, single stamp, PRIOR chain intact, docs-only diff. **Reversal is self-executing** —
any pen error reaching main restores the per-entry word.

**Ref deletion is proxy-forbidden to seats.** Branch deletes are an owner click. Do not retry it.

---
# PART B — CURRENT STATE
(v62 · supervisor pen · 2026-08-05, register v570 · replaced wholesale at the ROTATION PEN — the
channel-width discovery and the measured-outcomes correction are sealed; the owner has ordered the
RECIPE AUDIT and the TWO-TRACK posture (N45); the seam rotates; you, the reader, onboard per the
amended charter order: charter → PRIMER (v3) IN FULL → this file IN FULL → register by pointer →
live verify → read-back and HOLD)

## THE ERA: TWO TRACKS (N45). READ THE v570 REGISTER ENTRY AND COMMENTS 5186208519 · 5186277660 · 5186108632 VERBATIM BEFORE ACTING.
**TRACK A (main, the hedge) — #306 continues under existing law:** the L6 derivation verdict (seat
`2a1xa4` was cleared to run fire-order steps 5–7 on the committed emitted matrix; the verdict may
already be filed when you read this — AUDIT IT, channel decomposition beside it) → L7–L8 → full
rehearsal hand-back → EXECUTION word → the landing (ruled curve + converged surface + N43 signed pool
levels) → the owner's review set (5186108632: per-stage attribution · honest backtest book · year-0–7
no-arbitrage table) → owner satisfaction → round-21 ingest + movers page. Post-verdict orders standing:
the separating run (old surface `fb9efdec` under the new engine) + the belief-mass measurement — their
numbers go to the OWNER (how much of the basis level is model-shaped).
**TRACK B (side project, the owner's direction) — THE RECIPE AUDIT:** audit the RUNNING CODE into a
plain-English recipe — three lists: (1) the store + everything feeding it; (2) PREDICTION, one line per
step, input → rule → output; (3) VALUATION, same shape, through to the board number. **The recipe is
BRANDLESS** (no code refs, no machinery — a blind builder bakes from it); code citations live in a
SEPARATE verification appendix the builder never sees; the seam personally verifies every line against
code. **The failure test, owner verbatim: "If our valuation and projection can't be done as a recipe,
then we have already failed."** Every unstatable item is a NAMED finding. Then: fresh repo, blind
build, judged by OUTPUTS ONLY. Extraction delegated to subagents; file the directive as a GitHub issue
first. KEEP THE TRACKS SEPARATE — track B must not be poisoned by track A's way, and track A must not
stall for track B.

## THE TWO CORRECTIONS EVERY NUMBER NOW CARRIES
1. **Channel width:** the surface+engine reaches the curve's teaching values through MOST of the
   population, not only the 71 counted-fallback rows (55.78% / 44.22% split of movement; concluded
   475/825 moved; hard-zero rows immune). Never tell the narrow story.
2. **Measured outcomes:** career value = pw-weighted aggregate of `ev(p, Y)` as-of values — the
   ENGINE measuring, not raw scores over bars; thin-record seasons lean on the year-zero estimate.
   No raw-scores measure has ever existed; building one is the owner's standing requirement (N45 /
   the recipe's prediction list). PRIMER v3 §4 item 5.5 carries this permanently.

## LIVE STATE (verify with your own commands, trust nothing)
Main = the v570 pen or a descendant · four gating workflows green (in-flight stated as in-flight) ·
eleven issues open, #271 #274 closed, no open PRs · LIVE carrier `d7bnaa` at `7e9d7f9` · outgoing-seat
branch `claude/exec-seat-306-afl-rl-zlaarm` at `472c39d` (hand-off in `HANDOFF.md`, a repo file not a
comment) · CURRENT exec seat branch `claude/exec-seat-306-handoff-2a1xa4` at `8e18535` or a descendant
(the verdict commit expected) · frozen/HOLD branches intact (j0kwl0 `8e8c15b` · fubolo `abf8f4c` ·
fp78jm `3cccb9d` · 4ql38z `9914c4d` — carries the #279 machinery BOTH tracks read · g4edkc `592c7a2`) ·
snapshots: `13b71c26` = the N35-assert working state (→ `fb9efdec`, curve `e69a3f38`) · `2b7640be` = the
live L6 working state (surface `b540833b`, both engine pins `15525b03`, contract seal deliberately stale
per N44 addendum) — verify both by apply-and-hash. **N35: classify your own box before ANY fit figure;
check uptime EVERY time; the assert stales on any restart (the outgoing seam re-classified five times
in one day).** Measurement scripts importing numpy run under `RL_VENV` (recipe in ENVIRONMENT CARRIES).

## STANDING RULINGS SUMMARY — the map, NEVER the law. Act on a ruling → read its durable copy verbatim.
N1–N44 stand as v61 recorded them (N41 acceptance population · N42 pool principle · N43 signed levels +
ND-65+ cap bound to curve[64] · N44 + addendum engine-pin/stale-seal). **N45 (v570, owner words):** the
recipe audit + two-track order, the brandless-recipe law, the failure test, the owner's standing
raw-scores-over-bar requirement. The loop's terms unchanged (fixed point = payload md5 equality ·
bound 4 · exhausted → HALT).

## OWNER ACTS OUTSTANDING
Re-provide the pen token to the INCOMING seam (this pen is the rotation) · the EXECUTION word (after
the full hand-back, track A) · the recipe's review when track B delivers it · close clicks #292 #283
#275 · branch deletes HOLD as v61 · N12 holds until the landing.

## RUNNING THIS SEAT WELL — charter C1/C2/C3, M1–M3, the two rules, and the OWNER'S COMMUNICATION WORD
- The owner's words 2026-08-05, BINDING and recorded after a failure of this seat's own register:
  **plain English, no riddles, no dense waffle** — he called this seam's prose "incredibly confusing,
  dense and waffly, devoid of substance" and he was right. Short sentences. Substance only. His
  questions get DIRECT answers before anything else.
- Every agent return in VERY SIMPLE terms: what they did, whether it worked, what he must decide.
  Relays in his channel. Answer him HERE before filing anywhere.
- M1 one screen · M2 deciding-figure/ruling/audit else delegate · M3 posture at every pen · audits
  check INTENT before mechanics (the measured-outcomes correction is what missing that costs) · every
  number names its quantity · ad-hoc shell is where discipline dies; run the committed instrument ·
  the preboot pgrep runs in its OWN command (self-match otherwise).

## ENVIRONMENT CARRIES — as v61 in full (RL_VENV 5-pin venv + setup_env.sh · N35 recipe: bootstrap from
the PURE pass-0 tree then `refit_v0surf.py --verify` must reproduce `fb9efdec` · strictly serial ·
compute-path assert `92e397bd` · N32 payload recipe (string keys, int(round), sort_keys, [:8]) · N33
srcmd5 re-stamps · PEN MECHANICS: stamp near char 88 SAME LENGTH · insert before ` · SEAM v540
(2026-07-29)` · line count unchanged (8,438) · growth == entry length · one new stamp · docs-only ·
Part B wholesale · commit `supervisor-seat <supervisor@seam.local>` · branch → PR → rebase-merge →
re-verify main by CONTENT · reset pen branch onto origin/main first · force-with-lease normal when the
old tip is merged history), plus: `structural_basis_279.json` `25a72f85` · `lane_expectation.json`
(`…|e69a3f38|…` → `b760b17e`) · the committed instruments (acceptance · pool rerun `pool_levels_rerun`
= N43's source · lb determinism · path emitter · `l6/run_pass.sh` · `channel_width.py`) · the #279
machinery on `…-4ql38z` RETENTION-PROTECTED.

## THE INCOMING SEAM'S FIRST TASKS
0. Onboard per the amended charter order. Read the v570 entry and comments 5186208519, 5186277660,
   5186108632 verbatim. Every number you present names its quantity IN PLAIN ENGLISH.
1. Verify live state with your own commands (the LIVE STATE block above); N35-classify your box.
2. TRACK A: audit the L6 verdict when it files (or immediately if already filed) — channel
   decomposition beside it, the narrow story never told.
3. TRACK B: file the RECIPE AUDIT directive as a GitHub issue (the N45 terms: brandless recipe,
   separate verification appendix, the failure test verbatim, outputs-only acceptance), delegate
   extraction, verify every line personally before the owner sees it.
4. Read-back to the owner — plain, short — and hold for his confirmation before any push.
