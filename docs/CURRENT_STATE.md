# CURRENT STATE — the incoming-seat read · v42 · supervisor pen · 2026-07-31, register v550

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
(v42 · supervisor pen · 2026-07-31, register v550 · replaced wholesale at the consistency-era boundary pen: rotation complete, #292 landed, #290 amended — re-rehearsal pending its erratum)

## THE ERA: THE CONSISTENCY ERA — #292 LANDED · #290 AMENDED, RE-REHEARSING. Main is the v550 pen or a
descendant; all four gating workflows green at every content state; `live-scoring-proofs` is
workflow_dispatch-only (five workflow files, four gating — measured from the trigger map).
**#292 (trade-desk pricing split) is DONE AND ON MAIN** — landed `ab68430`, tree content-verified against the
seat's seal (`acd5ff61…`). Ordinals 1–64 plus ONE pool item (`{t:"pick", pool:true}`, trade.js-local),
one-source read of the bundle's index-65, missing key ⇒ no pool item offered; the phantom ordinal is dead,
proven before/after in `docs/evidence/trade_desk_pool_split_2026-07-31/`. The issue awaits the owner's close click.
**#290 rehearsed and the rehearsal did its job by failing:** L0 done (denominator **187**), L1 NOT executable
as filed — four defects, every one seam-verified at source; the owner **WITHHELD the EXECUTION word**.
**ADDENDUM C** (the L1 amendment, `d755c42` on `claude/seam-relay-step4-fp78jm`) is seam-audited **PASS WITH
TWO CONDITIONS**: (1) the appended `release_lineage` register entry re-homes **L7→L8/adoption** (its
destination shape needs board/balanced_board_md5/release_version + `owner_approved` — L8/adoption identities
and word); (2) the preboot pgrep assert **self-matches its invoking shell** (seam-reproduced false HALT) —
fix the pattern or run from a script file, prove it can both fire and pass. Errata: stop-point head[5] =
**1931** (1892 is the converged curve's). Seam rulings: **NO workspace lockfile** (serial rule + fixed assert
suffice; reversal = a second violation despite a working assert); the `refit_v0surf --bake` cost stays
flagged UNMEASURED — its measured line is mandatory in the next hand-back.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law, each read verbatim before acting: FHV Option A ≈190 [#270 ruling comment] · Best-23 =
A19 law, live [#271 A19 / #274 item 2] · G-Y0 2.000% hard-bar law [data/release_contract held_checks + #271
A12] · movers/era-succession law [#271 A15/A16] · deletion protections: sealed-cited (charter D2) + anything
an outstanding owner read depends on [#275 audit, v544]. The era's rulings:
N1. Currency = VOR γ=1.0 [#279 issuecomment-5129956044]
N2. Basis = STRUCTURAL · class ≤2022 · par PER-SEASON; prior = counted thin-stratum fallback, a WATCHED
    NUMBER with denominator [#279 issuecomment-5130411507]
N3. Fitter = CONTROL; the distfirst decomposition is a standing report-only artifact [#279 issuecomment-5131746312]
N4. Pin = POOLED NUMERAIRE in principle; the confirmation condition holds ONLY on the ruled fitter (honest
    form); one owner word reverts to the hard pin [#279 issuecomment-5131746312]
N5. Pool ≈ tail equivalence; the register-carried 233 has no committed artifact — re-measure with
    denominator before the law line lands [#279 issuecomment-5131865182 + v543]
N6. α = 1.0; curve e69a3f38; the s-invariance reading; the "three decimals" correction by addendum
    [#279 issuecomment-5132136796]
N7. Ownership single-source + exact-byte courier + both-literals repin sweep + join-by-key [#283 seal +
    seam audits, on-issue]
N8. F1 RL_PICK1 into the gates · F3 two-sided rescale from one pooled head · Q1 overwrite-with-logged-
    history · Q2 dual rule = PRIMARY [#279 issuecomments 5133081878 / 5136920875 / 5137264158 / 5137016272]
N9. FULL INTERNAL CONSISTENCY — live pricing inputs re-derive; sealed history stays; G-Y0 ≤2.000% real
    [#279 issuecomment-5137582245]
N10. The SUBAGENT BOUNDARY LAW — measures fan out, writes are one seat; every subagent conclusion
    re-verified by re-run [#290 body + v545]
N11. **THE BUST RULING** ["Pre window careers do not count… that pick was a bust"]: a pick prices what it
    bought FROM THERE — never-scored draftees teach as zero-outcome busts at full weight at the
    store-referenced pick; teach-as-zero is now RULED behavior; the censoring word narrows to one limb (the
    2003 class's SCORED careers). [#290 comment 5138401971]
N12. **SEAL-CITES-MAIN (standing rule):** a sealed record may only cite content reachable from main;
    evidence lands before or with the seal that cites it; NO branch delete until the seam confirms nothing
    sealed-cited lives only there. [#290 read-back audit]
N13. **YEAR-ONLY DOB word** (Kirkby/Looby: days contested across published sources; `_by` undisputed;
    seam-verified the engine consumes `_by` only — nothing reads `_bd`). Courier 302/302: 300 full dates +
    2 year-only, provenance stamped per row. [#290 comment 5138530044]

## THE QUEUE
- **#290 — L1 AMENDED, RE-REHEARSING.** Sequence: the erratum block (seam checks its text against the three
  audit points on push — no full re-audit) → **L1 re-rehearsed to a GREEN BOOT** (the exit condition Addendum C
  added; ≥2 attempts expected, ~7–9 min/cycle measured plus the unmeasured `--bake`) → the serial canary
  baseline (>8 min, still owed) → **the L2 window presentation** (censor-aware-2003 vs uniform-2004+ —
  measured both, owner words one; **L3 HALTS until it lands**, non-training prep allowed) → rehearsal
  completes → hand-back verified the seam way → **the EXECUTION word** → the landing legs → candidate board →
  adoption (owner's separate act; FHV word + five SCAR→VOR relabels there; **the appended lineage register
  entry is authored at L8/adoption**, per the C-audit). Key runbook facts carried: three curve states
  (stop/iter1/converged — POOL 234.3 etc. are STOP-POINT figures; L6 re-measures at convergence) · L1 one
  commit or not at all, identity set per Addendum C.1 (the 8/8 `release_contract.identities` mirror) ·
  field-level re-stamps only, the ten historical `45b207c0` occurrences provably unchanged · L4 first lawful
  in-repo build (copy-back + identity proofs; training-store stamps; age-source census hard acceptance) ·
  the workspace absolute paths are bootstrap's canonical layout.
- **#276 clubs tab · #270 referee** — post-#290/adoption; the referee inherits the measured dockets
  (duals-teach-both · median-vs-mean ramp · truncation optimism). · #139 feeds · v1.1 read outstanding
  (13 screenshots held for it).

## OWNER ACTS OUTSTANDING
The **L2 window word** (mid-rehearsal STOP, after L1 re-rehearses green) · the **EXECUTION word** (after the
full rehearsal hand-back verifies) · close clicks **#292 #283 #275** · branch deletes — **HOLD
`claude/step-4-execution-supervisor-g4edkc`** (until evidence tree `e339b1e9` reaches main via L0) and
**HOLD `claude/pre-referee-baseline-shaping-4ql38z`** (sole carrier of the stop-point curve artifact + both
per_entrant arms until the L1 landing, N12); **FREE**: `claude/trade-desk-pricing-split-ui-44652r` (landed,
fully contained in main) + the six measured-free at v550 (zero unique commits each) · later: adoption + FHV
+ relabels · the v1.1 read.

## RUNNING THIS SEAT WELL — the charter's C1/C2/C3 (owner-directed 2026-07-31) govern; read them first
- **C1 in practice:** the owner reads short, plain, prioritized messages — what happened, what he must
  decide (question → options → recommendation, one line each). Hashes, line numbers, and dialect go in the
  filings, surfaced only on request. His casual questions are load-bearing QC.
- **C2 in practice:** verify deciding figures yourself; delegate everything else; heavy payloads spill to
  files and are windowed with jq/python, never ingested. This cycle's catches all came from measuring
  rather than reading: the #292 stale clone (its "level with main" was v545), the C.2 lineage entry
  mis-homed to L7 (the destination shape said L8/adoption), the preboot assert that HALTs on its own shell,
  and the head[5] wrong-state transcription. **Probe the instruments a directive adds** — run the assert,
  read the entry shape — before blessing them.
- The permanent guards: REASONING IS NOT EVIDENCE · never present a number not read from a committed
  artifact · every count names its denominator · a filter answers only the question it was built from —
  sweep "what is missing" with no filter · prove every instrument can fail — **in both directions: an
  assert that cannot pass is as vacuous as one that cannot fire** (the preboot assert, this cycle) · one pen
  per boundary, batched · post-rebase-merge, verify main by CONTENT (tree ids are the clean seal — #292
  landed exactly so) · seal-cites-main (N12) before any branch delete.

## ENVIRONMENT CARRIES — carried from v41 in full, plus this cycle's: `/home/claude/rl_workspace/` is the
engine's CANONICAL runtime layout (bootstrap.sh:39-43) — never "fix" workspace paths; it is also a SINGLE
SHARED MUTABLE WORKSPACE with no interlock — every engine act runs strictly serially (N10; Addendum C.6's
rule; no lockfile by seam ruling) · fresh containers provision via `bash setup_env.sh` then independent pin
verification (5 pins; 3.12 asserted before any engine import) · the 1.0524 fallback has THREE sites
(one_source_selftest:65 · s4_matrix:129 · guard_correction_canary:112) · the two per_entrant files are never
conflated (2f8b4bd4 = curve input, moves; 40d7da7c = byte-freeze, does not) — and a SECOND never-conflate
pair: `per_entrant_279_vor.json` **77eba4d3** (VOR arm, the stop-point input) vs `per_entrant_279_scar.json`
**db8c934c** (SCAR arm), both on the shaping branch at `session_2026-07-30/item279/out/` · the stop-point
curve artifact `ruled_curve_final_279.json` (payload `e69a3f38` · factor_s 0.977688 · Σ(1..64)=54,722 exact ·
pick64 221) lives ONLY on `claude/pre-referee-baseline-shaping-4ql38z` until L1 lands it · the DOB courier
staging (302 rows, provenance per row) is DURABLE at `docs/evidence/dob_courier_2026-07-31/` · **HAZARD:**
`ui/tests/responsive_layout.test.mjs` writes into COMMITTED evidence `session_2026-07-20/ui_release_seam/
evidence/` in place (OUT :33, writeFileSync :185) — never commit `-a` after running it · **PEN MECHANICS**
(so no seat re-derives them): the register is ONE header line; each pen (i) bumps the version stamp near
char 88 (`· v55X 2026-07-31 · PEN:` → X+1), (ii) inserts its entry block immediately BEFORE
` · SEAM v540 (2026-07-29)`, (iii) proves pre-commit: file line count unchanged · growth == entry length ·
exactly one new `SEAM v55X` stamp · PRIOR count unchanged · docs-only diff; then Part B replaced wholesale,
commit as `supervisor-seat <supervisor@seam.local>`, branch → PR → rebase-merge → re-verify main by content.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen (the v550 pen rides on `ab68430`, the
   #292 landing); issues #290 #292 #279 #283 #275 #276 #270 #269 #146 #139 open (#292's work is DONE —
   open only for the owner's close click) · #271 #274 closed · PR #297 merged; four gating workflows green;
   the #290 branch `claude/seam-relay-step4-fp78jm` carries the runbook through Addendum C (`d755c42` or a
   descendant) and the evidence tree `e339b1e9`.
2. #290 is mid-cycle: the next post via the owner's paste is the **erratum** (check its text against the
   audit's three points — the two conditions and the head[5] errata; no full re-audit) or the **L1
   re-rehearsal hand-back** (verify the deciding figures by re-run: a green boot, the identity set moving
   together, the ten historical occurrences unchanged) or, after that, the **L2 window presentation**
   (verify both candidates' measurements from committed artifacts; the owner words the window; L3 is halted
   until he does).
3. Read-back to the owner in his channel; hold for confirmation before any push.