# CURRENT STATE — the incoming-seat read · v37 · supervisor pen · 2026-07-31, register v545

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
(v37 · supervisor pen · 2026-07-31, register v545 · replaced wholesale at the consistency pen)

## THE ERA: THE CONSISTENCY ERA. Main is `ec1827e`; all four workflows green at every content state of
2026-07-30. The shaping step's pick side is DONE AND CONVERGED (the ruled curve reaches its own fixed
point, s→0.999968). Its coherence gate then measured the truth that set this era's work: **G-Y0 diverged
3.035% → 11.224%** — the player-pricing stack (peak model · priors · par spine · v3.4 anchor · SCAR γ)
still derives from superseded bases. **THE OWNER RULED FULL INTERNAL CONSISTENCY** (#279
issuecomment-5137582245): every live pricing input rooted in the old store, the old curve, or a superseded
method is re-derived; the referee receives a SOLID baseline. The CONSISTENCY INVENTORY is delivered and
filed (`docs/evidence/consistency_inventory_2026-07-31/`, seam-verified, retention-protected). **#290 is
FILED, NOT FIRED** — the player-stack re-derivation, the largest job of the era. The step-4 seat HOLDS as
its default executor. #283 (ownership single-source) and #275 (tree halved) are MERGED, seats rotated.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Carried from v36 unchanged: N1–N6 (VOR · structural/≤2022/per-season · control · pooled numeraire ·
pool≈tail · α=1.0 with the s-invariance reading) · N7 (ownership single-source + exact-byte courier +
repin-sweep-both-literals + join-by-key) · N8 (F1 RL_PICK1 in the gates · F3 two-sided from one pooled
head · Q1 overwrite-with-logged-history · Q2 PRIMARY) · G-Y0 2.000% hard bar law · the hygiene standing
constraint (nothing an outstanding owner read depends on is deleted). New:
N9. **FULL INTERNAL CONSISTENCY (owner ruling 2026-07-30→31):** live pricing inputs re-derive under the
    ruled philosophy; sealed history stays history; G-Y0 returns to a REAL ≤2.000% gate as the acceptance;
    the seam's door-1 (exception + defer to referee) withdrawn as a seam correction against ruling-sheet
    item 4 and S-1. The E6 corrected mechanism (BOARD_FACTOR = (_P1/PVC[1])×s, numeraire block, coherence
    halts proven three ways) and the G3c finding (the two sides were anchored on DIFFERENT curves, agreeing
    only by pin-value coincidence) are the design facts of record. [#279: the stop, the ruling, the
    inventory comments]
N10. **SUBAGENT BOUNDARY LAW (owner-endorsed):** if it MEASURES, the seam/seat may parallelize with Opus
    subagents; if it WRITES, it is a seat with an owner word; one writer per bake; no parallel engine
    builds; every subagent conclusion re-verified by re-run before entering the record. REASONING IS NOT
    EVIDENCE — 2026-07-30 produced two self-falsifications (the seam's word-3 mechanism; the seat's
    RL_PICK1 transitivity) and one shared misread (the no-op BOARD_FACTOR); the rehearsal-validation
    clause caught all three. [#290 body + v545]

## THE QUEUE
- **#290 — THE PLAYER-STACK RE-DERIVATION (FILED, NOT FIRED; the era's job).** Dependency-ordered legs
  0–10 (before-picture+F5 real assertion · training-data provenance · priors under S-1/S-2 · par spine ·
  v3.4 exorcism · γ propagation · curve artifact install · v0surf refit · curve↔surface CONVERGENCE ·
  gates/seals · candidate board). Acceptance: G-Y0 ≤2.000% at the fixed point; every inventory
  STALE-ROOTED row dispositioned; the closing both-literals sweep; training-store stamps mandatory;
  rehearsal norm in full. **OPEN INPUT: the DOB source** (`dob_corrected.json` absent; owner hunting) —
  the fire word follows the DOB answer + the seam pre-fire audit on #290. Default seat: the step-4 seat
  continues (owner may word fresh); its branch `claude/step-4-execution-supervisor-g4edkc` carries the
  converged curve, E6, and all gate evidence at `592c7a2`.
- **Owner words in flight inside #290:** the par teaching-window word (candidates measured at rehearsal) ·
  the trade-desk fix timing (live defect: picks 66–80 price at 0, pick 65 as ordinal — UI lane) · at
  adoption: the FHV re-denomination word (three sites) + the five SCAR→VOR label relabels.
- **#276 clubs tab · #270 referee** — post-#290/adoption, in that order; the referee inherits the
  measured dockets (duals-teach-both · median-vs-mean ramp · truncation optimism). · #146 never as
  written · #139 feeds the others · v1.1 read outstanding (13 screenshots held for it).

## OWNER ACTS OUTSTANDING
The DOB answer → the #290 fire word (after pre-fire audit) · the par-window word and trade-desk timing
word (inside #290) · later: adoption word + FHV word · close clicks #283 #275 · branch deletes · the
v1.1 read.

## RUNNING THIS SEAT WELL — carried from v36 in full (D3/D4 law, review lanes, read-verbatim,
denominators, cost-estimate norm, one pen per boundary, content seals by tree id), plus: REASONING IS NOT
EVIDENCE is now N10 law · the owner's casual questions remain the best instrument in the system — this
cycle they caught the scope drift itself (full consistency was the filed intent; the seam's doors had
narrowed it) and the 3/7 numeraire question that clarified the anchor layering for the record.

## ENVIRONMENT CARRIES — carried from v36 in full (cp312/RL_VENV · unshallow · env -i whitelist · CRLF ·
seal by content/tree ids · repin sweeps both literals · deletion protections), plus: sibling_repin
resolves at #290 (its first lawful sibling build) · the config_sha re-stamp moves five artifacts in ONE
commit · the two per_entrant files are never conflated (selftest 2f8b4bd4 = curve input; sibling_repin
40d7da7c = byte-freeze).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen (expect the v545 pen or a descendant);
   open PRs (none, or this pen's pre-merge); issues #290 #279 #283 #275 #276 #270 #269 #146 #139 open
   (#283/#275 await owner close clicks) · #271 #274 closed; four workflows green.
2. #290 is the era: if unfired, the DOB answer gates the fire word — the pre-fire audit is yours to run
   on #290 before the owner fires. If fired, the executing seat's read-back/runbook/rehearsal artifacts
   are on #290 and its branch — verify hand-backs the seam way (re-run the deciding figures from
   committed artifacts, never prose).
3. Read-back to the owner in his channel; hold for confirmation before any push.
