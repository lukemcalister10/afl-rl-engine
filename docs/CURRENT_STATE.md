# CURRENT STATE — the incoming-seat read · v39 · supervisor pen · 2026-07-31, register v547

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
(v39 · supervisor pen · 2026-07-31, register v547 · replaced wholesale at the handover pen; the outgoing seam rotated at owner word — this Part B is the handover artifact)

## THE ERA: THE CONSISTENCY ERA — #290 IN REHEARSAL. Main is `c49ed30`+; all four workflows green.
**#290 (the player-stack re-derivation) is FIRED into a FRESH seat** (owner word; branch
`claude/seam-relay-step4-fp78jm`, which also carries the step-4 evidence cherry-picked forward,
seam-verified byte-perfect at tree `e339b1e9`). Its read-back and runbook are AUDITED (PASS); the seat is
**RELEASED TO REHEARSE L0–L8** per `docs/RUNBOOK_290_player_stack_rederivation.md` (on its branch).
**#292 (trade-desk pricing split) is FIRED in parallel** — UI lane, seat opens on owner paste; the owner
corrected the span at fire: 65–80, pick 65 being the pool level wearing an ordinal label. **The DOB courier
act is FULLY CLEARED, 302/302** — staged, verified, executes inside #290's runbook. The old step-4 seat is
ROTATED CLEAN; **its branch (`claude/step-4-execution-supervisor-g4edkc`) must NOT be deleted until the
seam confirms the evidence has landed on main** (rides L0's first landing).

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Carried from v37 unchanged: N1–N10 (the five shaping rulings + s-invariance · ownership single-source /
exact-byte courier / both-literals sweep / join-by-key · F1/F3/Q1/Q2 · full-internal-consistency · the
subagent boundary law). New:
N11. **THE BUST RULING** ["Pre window careers do not count… that pick was a bust"]: a pick prices what it
    bought FROM THERE — never-scored draftees teach as zero-outcome busts at full weight at the
    store-referenced pick; teach-as-zero is now RULED behavior; the censoring word narrows to one limb (the
    2003 class's SCORED careers). [#290 comment 5138401971]
N12. **SEAL-CITES-MAIN (new standing rule, from a seam-owned miss):** a sealed record may only cite content
    reachable from main; evidence lands before or with the seal that cites it; NO branch delete until the
    seam confirms nothing sealed-cited lives only there. [#290 read-back audit]
N13. **YEAR-ONLY DOB word** (Kirkby/Looby: days contested across published sources; `_by` undisputed;
    seam-verified the engine consumes `_by` only — nothing reads `_bd`). Courier 302/302: 300 full dates +
    2 year-only, provenance stamped per row. [#290 comment 5138530044]

## THE QUEUE
- **#290 — REHEARSING L0–L8.** Next STOP: after L0/L1 rehearsal evidence, the **L2 window presentation**
  (censor-aware-2003 vs uniform-2004+ — measured both, owner words one; L3 HALTS until it lands, non-training
  prep allowed). Then rehearsal completes → hand-back verified the seam way → **the EXECUTION word** → the
  landing legs → candidate board → adoption (owner's separate act; FHV word + five SCAR→VOR relabels there).
  Key runbook facts: three curve states (stop/iter1/converged — POOL 234.3 etc. are STOP-POINT figures;
  L6 re-measures at convergence) · L1 lands as one commit or not at all (four re-stamp dependents; twelve
  sealed-history non-movers) · L4 is a FIRST lawful in-repo build (copy-back with identity proofs;
  training-store stamps mandatory; the age-source census is a hard acceptance) · the workspace absolute
  paths are bootstrap's canonical layout, NOT dead paths.
- **#292 — trade-desk split fix**, parallel UI seat (opens on owner paste; read-back → seam go → land;
  merge order through the seam).
- **#276 clubs tab · #270 referee** — post-#290/adoption; the referee inherits the measured dockets
  (duals-teach-both · median-vs-mean ramp · truncation optimism). · #139 feeds · v1.1 read outstanding
  (13 screenshots held for it).

## OWNER ACTS OUTSTANDING
The **L2 window word** (mid-rehearsal STOP, measured candidates presented) · the **EXECUTION word** (after
the rehearsal hand-back verifies) · paste #292's opener if not yet sent · later: adoption + FHV + relabels ·
close clicks #283 #275 · branch deletes (HOLD `claude/step-4-execution-supervisor-g4edkc` until the seam
confirms the evidence on main; others free) · the v1.1 read.

## RUNNING THIS SEAT WELL — carried from v37 in full, plus: the owner's QC caught the DOB population gap
(busts teach too) and the defect-span correction (65–80) this cycle — treat every casual question as an
instrument · REASONING IS NOT EVIDENCE has four instances now; the rehearsal-validation clause and
re-running are the guards · a filter answers only the question it was built from — the safe sweep for
"what is missing" has no filter at all · **INGESTION LAW (owner-directed at the v547 rotation): the seam
verifies DECIDING FIGURES, it does not ingest bulk — uploads, artifact dumps, and row-level validation go
to subagents returning verdicts + the deciding numbers for seam re-check; Fable context is the system's
scarcest resource.**

## ENVIRONMENT CARRIES — carried from v37 in full, plus: `/home/claude/rl_workspace/` is the engine's
CANONICAL runtime layout (bootstrap.sh:39-43) — never "fix" workspace paths; fresh containers provision via
`bash setup_env.sh` then independent pin verification (5 pins; 3.12 asserted before any engine import) ·
the 1.0524 fallback has THREE sites (one_source_selftest:65 · s4_matrix:129 · guard_correction_canary:112) ·
the two per_entrant files are never conflated (2f8b4bd4 = curve input, moves; 40d7da7c = byte-freeze, does
not) · the DOB courier staging (302 rows, provenance per row) + both cross-check tables are DURABLE at
`docs/evidence/dob_courier_2026-07-31/` — the courier input of record; the store is the destination truth.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen; issues #290 #292 #279 #283 #275 #276
   #270 #269 #146 #139 open · #271 #274 closed; four workflows green; the #290 branch
   `claude/seam-relay-step4-fp78jm` carries the evidence tree `e339b1e9` + the runbook.
2. #290 is mid-rehearsal: its next post is either L0/L1 rehearsal evidence + the L2 window presentation
   (verify the candidates' measurements the seam way, present to the owner for the window word) or a
   rehearsal hand-back (verify, then the owner's execution word). The DOB courier staging note above.
3. Read-back to the owner in his channel; hold for confirmation before any push.
