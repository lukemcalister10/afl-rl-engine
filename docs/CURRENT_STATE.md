# CURRENT STATE — the incoming-seat read · v63 · supervisor pen · 2026-08-05, register v572

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
(v63 · supervisor pen · 2026-08-05, register v572 · replaced wholesale at the CLOSURE PEN — L6 is
closed by owner ruling; L7 is complete and audited; L8 is the last rehearsal act before the owner's
EXECUTION word; Track B is sealed and waits only on the landing; the pen token is retired)

## THE ERA: THE LANDING RUN-IN
- **L6 CLOSED (owner ruling, durable copy 5188042722):** converged AT TOLERANCE — a pass moving no
  pick by more than 1 board point is converged. The ADOPTED CURVE is the loop's last derived ladder,
  payload FULL `01f27f0231929b285de83aaa6713048d`. Reversal condition: any future pass moving any
  pick by more than 1 point re-opens the closure. The bound's four passes produced five distinct
  payloads, no cycle; the final residual was exactly ±1 point on 29 of 64 picks.
- **The closure install is audited (5188217942 / 5188266553):** adopted curve installed; surface
  refit to `ebc3d3303a1956a8ec94b4e2c1497bdf`; converged G-Y0 0.033% ≤ 2.000% HARD (n=1,326 over 64
  picks, VOR) against N16's trigger; the seam reproduced the refit byte-identically cross-host.
  **Deliberate standing state:** the harness pin was NOT moved — the NEXT matrix emit on this
  working state HALTS the loader by design, forcing a ledgered re-pin. Expected, not a defect.
- **L7 complete and audited (5188799545 / 5188841840):** entrant seal `ed5b7fcc` (62,726) on the
  live store at the adopted curve; board-vs-sealed is now a HARD ASSERT at both sites (the old
  printed-boolean check was vacuous and is dead); the G-Y0 dated exception is RETIRED from the
  contract; F5/F4 gates pass; selftest 97/0.
- **L8 IN FLIGHT (cleared 5188841840):** the candidate board built BESIDE shipped; every mover
  carries a named cause (adopted curve · year-zero lens · N43 signed pool levels · other landers);
  the wide-channel caption is load-bearing — the curve and lens are VALID causes for movers in
  evidence-backed rows; only unexplained residuals halt. Then: full rehearsal hand-back → seam
  verification → the owner's EXECUTION word → THE LANDING (adopted curve + surface `ebc3d330` +
  signed pool levels + the #323 store batch incl. Addendum 4 + text cleanup) → the owner's review
  set (5186108632: per-stage attribution · honest backtest book · year-0–7 no-arbitrage table; the
  no-arbitrage table may fire NOW, read-only) → owner satisfaction → round-21 ingest + movers page.

## TRACK B — COMPLETE AND SEALED; fires at the landing
Recipe (122 brandless rules) · constants · verification appendix delivered on the coordinator
branch (tip `bcb12ea`). The store fixture is re-cut per #323 Addendum 4 — md5
`f1e8c9fed35462536d00add604f69a3f` — carrying the UNUSED-SUBSTITUTE CONVENTION: an unused-sub
appearance is not a game played (Bell 2021 = 8 g @ 41.7 · Rockliff 2021 = 1 g @ 25.0). THE FROZEN
MODELS ARE WITHHELD from the blind-build package (owner word, 5188203865): the builder fits its own
models from the recipe alone, judged by OUTPUTS ONLY. The package cuts ONCE, from landed main.

## THE STANDING CAPTIONS EVERY NUMBER CARRIES
Wide feed-back channel (55.78% of movement on the 71 counted rows, 44.22% on the other 1,126 —
never the narrow story) · the engine contributes exactly zero (surface effects only) ·
wholesale-belief 6.18% of teaching value (the −0.63% evidence-backed move is a FLOOR, not the
share) · completion optimism +4.7–8.4% printed beside anything it touches.

## LIVE STATE (verify with your own commands, trust nothing)
Main = `e1aa61e` (the plain-vocabulary merge over the v571 pen) or a descendant · exec seat branch
`claude/exec-306-pass-2-u8ir65` at `b33a03d` or a descendant (thirteen snapshots stand, none
overwritten; the live one is `2b5e99eb` = the L7 state; base of record `472c39d`) · coordinator
branch `claude/afl-valuation-coordinator-4k9vy5` at `bcb12ea` · frozen/HOLD branches as v62 · live
store `81d24704` until the landing · **N35: classify your box before ANY fit figure; check uptime
EVERY time; every box this era carried the same CPU label while differing — only reproducing
recorded output bytes classifies.** Measurement scripts importing numpy run under `RL_VENV`.

## ENVIRONMENT — the content-filter hazard (live, mitigated)
Seat chats repeatedly hit a model-safety FALSE POSITIVE on this project's old metaphor vocabulary.
Standing mitigations: PLAIN WORDS in all new text (the three living documents were re-worded at
PR #324; the primer's glossary maps old → new) · silent-mode seat output (no file contents echoed
into chat; short replies) · model-switch or a fresh seat to resume a blocked session · every
deciding derivation reproduces from committed bytes, so a lost chat never loses work.

## GOVERNANCE THIS PEN
**The pen token is RETIRED** (owner word 2026-08-05; charter amendment of the same date). The
register's protection: only the sitting seam seat pens · the pre-commit structural checks · the
standing reversal (any pen error reaching main restores stricter control). Docs pens land by
branch → PR → the owner's merge click, as before.

## OWNER ACTS OUTSTANDING
The EXECUTION word (after the full rehearsal hand-back) · the review set → the adoption click →
round-21 · close clicks #292 #283 #275 · branch deletes HOLD as before · N12 holds until the landing.

## RUNNING THIS SEAT WELL
As the charter's C1–C3 and M1–M3, plus the owner's binding words: plain English, short sentences,
his questions answered DIRECTLY first, every number names its quantity, about one screen. Agent
results in very simple terms. Audits check INTENT before mechanics. Plain vocabulary always.

## ENVIRONMENT CARRIES
As v62 in full (RL_VENV 5-pin venv + setup_env.sh · N35 recipes: pure pass-0 tree →
`refit_v0surf.py --verify` reproduces `fb9efdec`; the redesigned path reproduces `b540833b`; the
derivation machinery = the #279 panel from `9914c4d` + the pass's re-pinned harness +
`pooled_numeraire.py MATRIX PANEL OUTDIR`; payload = md5 of `json.dumps({str(pick): int(round(v))},
sort_keys=True)` · strictly serial · N32/N33 recipes · PEN MECHANICS: stamp near char 88 SAME
LENGTH · insert before ` · SEAM v540 (2026-07-29)` · line count unchanged (8,438) · growth ==
entry length · one new stamp · docs-only · commit `supervisor-seat <supervisor@seam.local>` ·
branch → PR → rebase-merge → re-verify main by CONTENT), plus the closure-era identities: adopted
curve payload FULL `01f27f0231929b285de83aaa6713048d` · surface `ebc3d330…` · entrant seal
`ed5b7fcc` / 62,726 · fixture `f1e8c9fe…` · snapshots `13b71c26` (pure pass-0) · `2b5e99eb` (L7).

## THE INCOMING SEAT'S FIRST TASKS
0. Onboard per the charter order (charter → primer IN FULL → this file IN FULL → register by
   pointer → live verify → read-back and HOLD). Plain vocabulary in everything you write.
1. Verify live state with your own commands; N35-classify your box.
2. Audit L8 when it files (the wide-channel caption; every mover named; recompute the deciding
   figures from committed bytes).
3. Verify the full rehearsal hand-back → present it for the owner's EXECUTION word.
