# CURRENT STATE — the incoming-seat read · v33 · supervisor pen · 2026-07-30, register v541

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
(v33 · supervisor pen · 2026-07-30, register v541 · replaced wholesale at the adoption pen)

## THE ERA: POST-ADOPTION. The 30/7 rederivation board is the live board. No seat is live.
Owner word 2026-07-30 (#271 Addendum 14, verbatim): "30/7 rederivation for the label. Adopt." Live identities:
store 6b9d00a7 · board f2df6e0a · curve file 6506d8b1 (payload 08ea9375; pre-stamp candidate id 3dabec04;
pool_value 299; ui curve contract 432f0153, per_entrant 2f8b4bd4) · v0surf ce08c2d1 (frozen pair
b781ed25/d071e743). ADOPTION EXECUTION FACTS, seam-verified: main = f60af6c (single commit on a86c725; A23 amend verified — three fix files only, identities byte-unchanged); bundle f2df6e0a-verified;
contract a0620e0e/sha 0717287e — held_candidates EMPTY, held_checks = G-Y0 alone; boot pins = adopted identities;
the 30/7 column live in all three histories + bundle; lineage register 2 entries (latest ITEM_271_Addendum_17),
current slot = pure ITEM 408 mirror. FINAL CI at f60af6c: guards SUCCESS 0 FAIL / 1 HELD (G-Y0 3.035% under 3.500% ceiling) · FV Provenance SUCCESS · Final Integration FAILURE at step 13's LAST command only — within it: extract 42/42 · release 30/30 · counting 24/24 · club_curve_provenance 35/35 (WAS 24/35 — the split-era crash is dead) · club_valuation PASS (16 teams/160 picks) · parity 11/11 with the Best-23 can-fail lever proven IN CI · movers.test.js LAST at 2/58 = EXACTLY the pinned pair; steps 14-22+42-43 skipped, declared · Live Scoring FAILURE at step 12 on the SAME pinned pair, steps 13-15+31 skipped, declared. Measured by the seam directly (runs 30518162835/851/841/846) after two agent attempts died on server 529s — the spill-and-grep pattern held. A23: the split-era price_pick
crash (KeyError:73, masked all era by the ring-fence halt) fixed under owner word AMEND — 65+ = pool_value. Movers: the 30/7 point + boundary landed via the R20 repair lane (A16); the three-way
balanced_board_md5 anchor disagreement is DOCKETED TO HYGIENE (A17), not fixed.
Sequence of record (owner-amended this cycle): land → re-derive → ADOPT (done) → SHAPE (#279) → referee (#270)
→ ITEM 412. Every queued job fires on the owner's word only. Nothing is running.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Entries are PER RULED QUESTION; supersession is partial by nature.
1. FHV definition → Option A: expectation view, single constant ≈190; survivor 250/528 REJECTED; per-window
   (MSD 352/SSP 277/OTHER 97) = one-word upgrade. First consumer: #276's phantom. [#270, ruling comment]
2. γ (SCAR vs VOR) → NO ruling until a derivation exists under BOTH systems, each with its own surface bake;
   the #271 companion is mixed-denomination evidence of the leak only (canonical leak: 2.32% of strict pairs
   invert; RL_GAMMA absent from the v0surf gates). Executes in #279. [#271 A7, A10; A13 for the canonical figure]
3. G-Y0 (curve↔surface 2% HARD bar) → owner-accepted dated exception at 2.929% ruled / 3.035% guard; loud HELD;
   do-not-exceed ceiling 3.50% = hard FAIL; record-removal = FAIL; resolves at #279 (bar re-set deliberately).
   Sign structure: two-sided wobble, net −0.56% (curve below surface); it never measured the reality gap. [#271 A12/A13]
4. Year-0/current bar source → the store's ELIGIBILITIES COLUMN (owner-maintained), dual → LOWER bar (R105.1);
   season rows = closed seasons' bars; 2026 column supersedes its row in every bar-taking use. [#271 A4, A6]
5. Future-leg blend → PERMANENTLY hand-set (future_position + alternate_position + p_dual_stream; LEG C law:
   lower bar of the pair on the p_dual fraction; primary keys the arc). "Eligibility blend later" RETIRED from
   the referee docket by owner word. [#270 retirement comment]
6. §1b / y0dpp_bar → retired from year-0 by SUPERSESSION only (code untouched; fires 0/804 with column-keyed
   bnow; resurrests at 86/804 if bnow reverts — proven by CF2). [#271 A4/A5; cf2 evidence]
7. The 62-edit set → sealed as 62 + 3 owner-amended (2026-07-29): Roberts/Hall/Williams alternate+p_dual
   pairs cleared (both halves = the unit, selftest invariant), measured board delta 0. [#271 A12, ADDENDUM12_CLEARS]
8. The pick-curve tail → prices ~1.56× busts-included reality at 57–64 (honest ±7% at picks 1–24); mechanism =
   evidence-weighting mutes bust votes where busts cluster + prior dominance at thin cells + curve→surface→curve
   self-reference. REPORT-ONLY until #279/referee; the two knobs are γ=0.85 (sole live dampener) and the retired
   CE dial (never carried into R1). [#270 evidence notes 1-2 + CE correction]
9. Par teaching population → par_build keys ONE gfut per career; role migrants refile prime seasons under
   destination roles (Berry +351 / Addinsall −116 the extremes; median ripple 0). Docketed for #279; fix =
   per-season teaching (data now exists); interim = exclude pre-conversion seasons. [#279 ruling-sheet addition]
10. Held mechanisms → held_candidates admits ONLY the 8 bound release identities (release_contract.py:126);
    check-family holds live in sibling held_checks; every hold pins both sides, reports loudly, reverts to FAIL
    on removal, and names its clearing act. A declaration consumed by two gates is verified against BOTH before
    sealing. [#271 A11]
11. Adoption-era CI, measured at f60af6c: guards green + G-Y0 HELD
    (CORRECT, stays until #279); FV green; FI red at step 13's LAST command and Live Scoring red at step 12 —
    BOTH being movers.test.js 2/58, the DECLARED
    ADOPTION-CREATED KNOWN-RED (owner Option 1, A22), PINNED at exactly two named assertions; any third
    failure in that file is NEW; FI steps 14-22 and LSU steps 13-15 are SHADOWED behind it until #274 — declared.
    The 'bridged' half may self-resolve at R21 (unmeasured — check then). Proof workflows remain manual-dispatch.
12. VOR/rank instruments → adjacent-pair inversion counts are TIE-SENSITIVE (305 shared-integer rows); use the
    order-independent all-pairs count. [#271 A13]
13. Best-23 selection → owner LAW (A19): the value-maximal 23 fillable from the ELIGIBILITIES column,
    DPP-optimised (assignment, not first-fit), on ABSOLUTE BOARD VALUE. The live tab runs the DECLARED
    adoption STOPGAP (top-up backfills unfilled slots) until #274's first item lands the selector — the
    stopgap's presence is the removal marker. [#271 A19; #274 docket]
14. The movers bundle → historical per-round reports are NEVER rewritten (each keeps its frozen era identity
    and vocabulary — that is the record, not staleness). Out-of-round columns ARE represented: they become
    selectable points + model-change boundaries at every derived-block rebuild (owner precedent:
    post-r19-redesign-1; the 30/7 boundary per A16 — outcome in the era block above). ui/data/movers_transition.js
    is GENERATED from data/release_lineage.json's release_transition (fail-closed bridge; never hand-edit;
    ITEM 408 Option A governs). The owner WANTS landed changes visible as movers records — treat that as a
    standing preference. [#271 A15/A16]

## THE QUEUE — everything fires on an owner word; seam pre-fire audit at each fire
- **#279 — the owner's baseline shaping step (his stated priority).** Seed rulings S1–S5 sealed in the filing +
  the par item. Deliverables: minimal-vs-structural prototype pair on one matrix; strict SCAR/VOR dual derivation
  (own surface bakes; RL_GAMMA enters the gates); ruled pick-value basis + explicit variance dial calibrated
  against the conservation yardstick; v0 propagation; G-Y0 re-derived. Owner rules on evidence, never in advance.
- **#274 — UI wave** (independent of #279 post-adoption; parallel seats possible with seam coordination). Three
  pre-ruled/pre-scoped items: (1) ERA-SUCCESSION plumbing, first priority (A22: current transition + archive;
  model_changes over all entries; both validators in lockstep; acceptance = movers 58/58 + the 30/7 flag true;
  clears the declared known-red); (2) the Best-23 eligibility selector (A19 law; replaces the adoption stopgap);
  (3) the over-free column (v − FHV live lens, below-free flag) — depends only on adoption + the ruled ≈190.
- **#276 — clubs tab**: its 250 phantom takes the ruled FHV with one word at fire.
- **#275 — hygiene**: needs the post-adoption green CI as its acceptance baseline. RETENTION LAW: files cited by
  sealed records are protected from pruning (charter D2).
- **#270 — referee project**: opens AFTER #279 delivers the shaped baseline; its docket already carries the FHV
  ruling, the tail evidence, the γ evidence path, and the retired future-blend item.
- #146 NEVER executes as written · #139 feeds the others · v1.1 amendment read = the owner's open parallel act
  (docs/referee/AMENDMENT_v1_1_DRAFT.md).

## OWNER ACTS OUTSTANDING
Fire words (#279/#274/#276/#275, any order — #279 stated priority) · the γ ruling (after #279's dual evidence)
· the v1.1 read · branch-deletion clicks per convention.

## RUNNING THIS SEAT WELL — owner-endorsed law (charter D3/D4 + this cycle's additions)
- **Answer the owner in his channel, completely, FIRST.** Filings are durable copies, never the reply. Interpret
  agent results — conclusions, not process. Plain sentences; no dense compression; lead with what happened and
  what needs deciding. The owner's casual questions are load-bearing QC — three this cycle exposed real findings
  (the tail pricing, the par contamination, the CE retirement).
- **REHEARSAL NORM (adoption-day lesson, 2026-07-30):** irreversible or first-of-their-kind operations are
  REHEARSED end-to-end in a scratch worktree BEFORE the owner's execution word — the full runbook, the tests
  that have never run, the lanes never exercised — so latent defects surface as ONE batched report off the
  critical path, not as serial stop-and-asks on it. First-time paths get first-time estimates, never
  "mechanical from here." Runbooks are drafted from FILE-LEVEL walks of what a law touches (the "UI pair"
  slot-table miss), not from the record's summaries alone. Adoption day's measured cost of skipping this:
  six serial owner round-trips where a rehearsal would have produced two.
- **Cost-estimate norm:** any request whose answer requires building artifacts that don't exist (counterfactual
  boards, new derivations) gets an explicit estimate + go-ahead BEFORE commissioning. General authorization is
  not specific authorization.
- Subagents: Opus by default; Fable only where judgment is the task (owner word). Spill every API payload to
  files. Register by pointer/window only — never head/cat (the header is one ~400KB line).
- One pen per boundary, batched. Hand-backs: re-run the 2–3 measurements that decide; full re-runs at final
  seals (the control-arm/nonvacuity independent re-run pattern and its exact conditions are documented in
  #271 Addendum 13 — the durable copy; scratch logs die with containers).
- Instrument discipline, this cycle's additions to the standing set: assert loaders are NONEMPTY before trusting
  their output (a silent empty load mis-bucketed a whole analysis); never trust a TRUNCATED diff-stat (tail -N
  ate expected_boot and manufactured a false finding); prove every check can fail; state CI posture in every
  seal; prefer order-independent metrics where ties exist.
- Worktree pattern for scratch builds: detached worktree + minimal disclosed pin edits + env -i + PYTHONHASHSEED=0
  + single-thread BLAS + pinned venv (route validated at hash level incl. OpenBLAS — conditions recorded in #271 A13). Never set
  RL_V0SURF_REFIT/RL_BAKE outside the declared lane. Nothing scratch is ever committed.

## ENVIRONMENT CARRIES
cp312 via RL_VENV (setup_env.sh → bootstrap_env.sh → bootstrap.sh; do not weaken the pin) · git fetch --unshallow
before ancestry claims · no parallel engine builds without seam coordination · scripted checkouts assert their
base · CRLF in the owner's CSV lane is a known Excel artifact, never "fixed".

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands (main tip vs this pen; open PRs — expect none; the issue map above).
2. Read-back to the owner in his channel; hold for confirmation before any push.
3. Then idle until an owner fire word; audit the directive at fire per the charter.
