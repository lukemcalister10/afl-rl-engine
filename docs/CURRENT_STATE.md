# CURRENT STATE — the incoming-seat read · v46 · supervisor pen · 2026-07-31, register v554

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
(v46 · supervisor pen · 2026-07-31, register v554 · replaced wholesale at the L3-close pen)

## THE ERA: THE CONSISTENCY ERA — L3 CLOSED IN FULL · THE FRESH EXECUTION SEAT RUNS L4–L8. Main is the v554
pen or a descendant; four gating workflows green at every content state (`live-scoring-proofs` is dispatch-only;
five files, four gating). **#292 is DONE AND ON MAIN** (`ab68430`; awaits the owner's close click). **#290:** the
record's LIVE carrier is the fresh seat's branch **`claude/exec-seat-290-handoff-j0kwl0`** at **`206a5f5`** or a
descendant (fubolo a frozen ancestor at `abf8f4c`; fp78jm frozen at `3cccb9d`, an ancestor of both). L0–L3 are
rehearsed, verified and CLOSED: window A applied · v0surf frozen as bytes (N16) · the watched number re-based ·
bias-1 landed as owner word T1, gates green 96/1, G-Y0 UNCHANGED at 13.919% — the ≤2.000% closure is ENTIRELY
L6's convergence job · the state diffs name their bases (L3_T1 PROVEN at `79ee8e5`; L1_amended UNRECOVERABLE,
recorded UNRESOLVED — reconstruction is N16's frozen bytes + the L3_T1 diff, never that record) · the S-1/S-2
ruled lane is IN-TREE and round-trip PROVEN (N14 identities exact; the 2×2 interlock fail-capable both ways).
The first pass on the ruled substrate is a WAYPOINT ONLY — payload `6dedc611` · ladder 54,532 · s 0.996218 ·
head 3011.3898 — no bar claim, nothing installed. The **EXECUTION word remains WITHHELD** — it follows the full
rehearsal hand-back after L4–L8.

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
N11. **THE BUST RULING**: a pick prices what it bought FROM THERE — never-scored draftees teach as
    zero-outcome busts at full weight; teach-as-zero is RULED behavior; the censoring word is one limb (the
    2003 class's SCORED careers). [#290 comment 5138401971]
N12. **SEAL-CITES-MAIN:** a sealed record may only cite content reachable from main; NO branch delete until
    the seam confirms nothing sealed-cited lives only there. [#290 read-back audit]
N13. **YEAR-ONLY DOB word** (Kirkby/Looby `_by` only). Courier 302/302, provenance per row, durable at
    `docs/evidence/dob_courier_2026-07-31/`. [#290 comment 5138530044]
N14. **THE NUMERAIRE PRIMITIVE (seam ruling, owner-reversible):** the MEASURED HEAD is primitive —
    `pooled_head_pre_scale = 3068.4647` exact, `s` full-precision DERIVED (0.9776876364…), `published_pin
    = 3000`; 6dp `0.977688` is presentation only; E6 coherence exact by construction (0.000e+00); E6's
    numeraire block carries all three keys bound to 1e-9. [#290 comments 5139486512 + Addendum F; v551 item 5]
N15. **WINDOW WORD A** (owner, 2026-07-31): the par window is CENSOR-AWARE 2003 — the code's current window.
    Censoring measured ABSENT (0 store scoring rows at Y2004; `gather()` skips absent seasons, never teaches
    zero); tenure-1 identical under both windows (438 = 438). [#290 comments 5140668094 + 5141734922; v552]
N16. **THE V0SURF FREEZE + YEAR-ZERO REDESIGN TRIGGER (seam, owner-directed):** the fitted surface travels as
    BYTES — frozen `84fb0cde` / blob `2f4c3859` at `docs/evidence/rehearsal_290_2026-07-31/v0surf_frozen_
    2026-07-31/` (on the #290 carrier line) is the RULED SUBSTRATE for L3–L8, L6's convergence and the landing
    (`expected_boot.v0surf` re-stamps inside the C.1 set). Every G-Y0 statement names the surface md5 it was
    measured on; waypoints 19.869% (predecessor container) and 13.919% (host 1/2) are container-bound; NO gate
    moves. The year-zero REDESIGN is DECIDED work — spec: constrained tail · deterministic fit lane ·
    cross-machine byte-assert; TRIGGER = L6's converged G-Y0: fails the 2.000% law → fires immediately as the
    remedy (directive + pre-fire audit); passes → rides the referee era beside #270. Engine compute is PROVEN
    cross-CPU byte-deterministic once the surface is supplied. [v552 items 4–6; V0SURF_DIVERGENCE.md +
    CROSS_MACHINE_ASSERT.txt + PROVENANCE.md at 57bfea1]
N17. **BIAS-1 = OWNER WORD T1** (2026-07-31): drop the 64 phantom rows (unobservable pre-2005 seasons taught
    as zeros — known-false evidence); KEEP true tenure labels. Each tenure cell is taught only by classes
    observable at that tenure (measured: exactly the owner's asked-for shape). The residual — the invisible
    2004 season thins the 2003 class's cumulative features at each label — is a NAMED referee-era refinement,
    not a defect left silently. The limbs interact (T3 ≠ T1+T2 for 804/804; aggregate sign flips), so any
    revisit re-measures whole treatments, never sums limbs. [#290 comments 5142523045 + 5142798385; v553]
N18. **A STATE DIFF NAMES ITS BASE COMMIT BESIDE ITSELF** — on the line that carries ALL of its targets; the
    base is recorded when the diff is cut, because it is unrecoverable after (the probe returns an interval,
    never a point; L1_amended narrowed to NOTHING and is recorded UNRESOLVED). Satisfied on both tree diffs.
    [v553 queue clause + the act-(1) annotations at 206a5f5; v554]

## THE QUEUE
- **#290 — the fresh seat RUNS L4–L8** on `claude/exec-seat-290-handoff-j0kwl0` (opening acts (0)–(2) DONE,
  seam-verified, v554). Remaining, in order: **L4** — the first lawful in-repo build, unmeasured by anyone,
  priced at L1's cost (~480s chain) → **L5 dockets** → **L6** — convergence + POOL/MSD/SSP re-measurement;
  **its hand-back must state the converged G-Y0 against N16's trigger explicitly, naming the surface md5** →
  L7–L8 → the full hand-back verified the seam way → **the EXECUTION word** → the landing legs → candidate
  board → adoption (owner's separate act: adoption word · FHV word · five SCAR→VOR relabels · the lineage
  entry authored THERE, never earlier). Landing-critical facts a successor must hold: L1 lands as ONE commit
  under Addendum C.1's identity set (8/8 `release_contract.identities` mirror; field-level re-stamps only;
  the ten historical `45b207c0` occurrences provably unchanged) · **the landing ships the frozen v0surf
  bytes** (`data/v0surf.pkl` ← `84fb0cde`) and re-stamps `expected_boot.v0surf` · **L3's T1 rides the landing
  set** (the `conditional_prior.py` unobservable-season drop + derived `first_observable_season()`, captured
  in `L3_T1_state.diff`, base `79ee8e5` per N18) · the EIGHTH γ site `rl_model.py:504` is in the L1(a) set ·
  the refit FOLLOWS E2 inside L1(b) · **`ruled_curve_final_279.json` installs at L1(b) under its own identity
  set — NOT carried before then** · **`derive_271.py`'s `fit_year0` is NOT edited** (N3 rules the fitter;
  editing it authors a different curve) · every engine act strictly serial behind `tools/preboot_assert.sh` ·
  costs: L1 chain 480s · prior fit ~37s · ci-guards-equivalent ≈17 min · L5 dockets: the payload-hash NAMED
  HELPER (`md5(json.dumps(curve, sort_keys=True))`, int ladder) · manifest-vs-code-default equality for EVERY
  pinned `RL_*` · the `ev()` namespace finding · int-cast-vs-widen framed for L6.
- **#276 clubs tab · #270 referee** (home of the year-zero redesign if L6 passes, N16, and of bias-1's
  cumulative-features refinement, N17) — post-adoption · **#139 feeds** · v1.1 read outstanding (13
  screenshots held).

## OWNER ACTS OUTSTANDING
The **EXECUTION word** (only after the full rehearsal hand-back verifies) · close clicks **#292 #283 #275** ·
branch deletes — **HOLD `claude/step-4-execution-supervisor-g4edkc`** (until `e339b1e9` reaches main) ·
**HOLD `claude/pre-referee-baseline-shaping-4ql38z`** (sole carrier of the stop-point artifacts) · **HOLD
`claude/seam-relay-step4-fp78jm`** (frozen ancestor at `3cccb9d`) · **HOLD
`claude/player-stack-290-handoff-fubolo`** (frozen ancestor at `abf8f4c`; N12 holds until the landing reaches
main) · FREE: as at v550 · later: adoption set · the v1.1 read.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate (searches/status/location/bulk NEVER in-seat) · **M3** context posture
  in one line at every pen.
- **The owner's communication word of this cycle (2026-07-31, this seat):** every agent return is translated
  for the owner in VERY SIMPLE terms, short — what they did, whether it worked, what he must decide (options +
  recommendation, one line each). Relays he must paste are given IN HIS CHANNEL, never as a pointer to
  GitHub. Answer him HERE before filing anywhere. These are owner words; they bind successors.
- The owner's casual questions are load-bearing QC. Standing catches: the window-era censoring question was
  answered PAR-scoped and the same hazard was later REAL in `build_cond_prior` — scope every "measured
  absent" to its path · "why refit v0surf at all?" removed a wasted step from the seam's own ruling · his
  bias-1 framing WAS the right treatment (T1) before any recommendation · the seam's round-trip re-run caught
  the unnamed diff base the filing's own proof had missed. Verification catches drift the moment a proof is
  re-run somewhere the prover didn't stand.
- The permanent guards: REASONING IS NOT EVIDENCE · never present a number not read from a committed
  artifact · every count names its denominator · sweep "what is missing" with no filter · prove every
  instrument can fail IN BOTH DIRECTIONS · one pen per boundary, batched · post-rebase-merge verify main by
  CONTENT · seal-cites-main before any branch delete · never re-spec a gate to trust the thing it checks.

## ENVIRONMENT CARRIES — carried from v45 in full, plus this cycle's: **THE STATE-DIFF-BASE CLAUSE (N18) IS
SATISFIED ON BOTH TREE DIFFS** — annotations live BESIDE the diffs (`L3_T1_state.diff.BASE` names `79ee8e5` +
the at-later-tips recipe; `L1_amended_state.diff.BASE` records UNRESOLVED; that diff is the L1-exit RECORD,
never a build input — reconstruction is N16's frozen bytes + the L3_T1 diff) · the probe
`state_diff_base_probe.py` returns an INTERVAL, never a point — measurement narrows, provenance decides · the
ruled derivation lane is IN-TREE at `session_2026-07-30/item279/panel/` (+ `out/per_entrant_279_vor.json`;
`carry_verify.sh` is the round-trip instrument; the 2×2 harness/matrix interlock is proven fail-capable both
directions; matrix identities RULED store `81d24704` vs VOR `6b9d00a7` — any cross-pairing HALTs) · the
first-pass waypoint (`6dedc611` / 54,532 / s 0.996218 / head 3011.3898) carries NO bar claim · prior carries,
all still live: the committed watched-number input `L3_watched_number/nd_matrix_ruled.json` (md5 `a216e6e6` ·
store `81d24704` · v0surf_sig `96d671c9…`; byte-invariant under T1) · the emitter for it writes
`session_2026-07-29/item271/out/per_entrant_271.json` IN PLACE (live md5 `2f8b4bd4`, never-conflate pair,
provenance-cited) — backup→emit→capture→restore with md5-proved restore is the ruled routing ·
`harness_pvc_REPINNED.py` pins are the FULL-CHAIN convention; its three asserts are proven fail-capable ·
**containers can migrate hosts mid-session** — provenance names the MACHINE · frozen v0surf at
`docs/evidence/rehearsal_290_2026-07-31/v0surf_frozen_2026-07-31/` (`84fb0cde`/blob `2f4c3859`, on the #290
carrier line) · the v0surf FIT is the chain's only machine-sensitive act · `l2_window_measure.py` carries
`L2_AUDIT_CONTROL=1` · `/home/claude/rl_workspace/` canonical AND shared-mutable — strictly serial behind
`tools/preboot_assert.sh` · `bash setup_env.sh` + 5-pin proof, 3.12 · the 1.0524 fallback has THREE sites ·
TWO never-conflate per_entrant pairs (2f8b4bd4 curve input / 40d7da7c byte-freeze; 77eba4d3 VOR / db8c934c
SCAR on the SHAPING branch) · the stop-point artifact `ruled_curve_final_279.json` lives ONLY on the shaping
branch until L1 lands it · the DOB courier durable at `docs/evidence/dob_courier_2026-07-31/` · **HAZARD:**
`ui/tests/responsive_layout.test.mjs` writes into COMMITTED evidence — never commit `-a` after running it ·
**PEN MECHANICS**: the register is ONE header line; each pen (i) bumps the stamp near char 88 (`· v55X
2026-07-31 · PEN:` → X+1), (ii) inserts its entry immediately BEFORE ` · SEAM v540 (2026-07-29)`, (iii)
proves pre-commit: line count unchanged · growth == entry length · exactly one new `SEAM v55X` stamp ·
docs-only diff; then Part B replaced wholesale, commit as `supervisor-seat <supervisor@seam.local>`, branch →
PR → rebase-merge → re-verify main by CONTENT.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v554 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 open · #271 #274 closed · no open PRs; four gating workflows green (if
   a run is in flight, say so — never predict); the #290 LIVE carrier `claude/exec-seat-290-handoff-j0kwl0`
   at `206a5f5` or a descendant; the FOUR frozen/HOLD branches intact (g4edkc · 4ql38z · fp78jm `3cccb9d` ·
   fubolo `abf8f4c`); the frozen v0surf verifies (`84fb0cde`, from the carrier tree — it is NOT on main).
2. The #290 seat is mid-rehearsal at L4–L8: audit each leg's filing by re-running its deciding figures (M2),
   and translate each return for the owner in very simple terms (his standing word — see RUNNING THIS SEAT
   WELL). After L6: check the converged G-Y0 against N16's trigger and bring the owner the outcome simply.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
