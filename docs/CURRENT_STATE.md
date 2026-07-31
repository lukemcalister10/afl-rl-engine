# CURRENT STATE — the incoming-seat read · v43 · supervisor pen · 2026-07-31, register v551

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
(v43 · supervisor pen · 2026-07-31, register v551 · replaced wholesale at the L1-exit + double-rotation pen; the outgoing seam rotates on the owner's word — this Part B is the handover artifact)

## THE ERA: THE CONSISTENCY ERA — L1 EXITED · BOTH SEATS ROTATED AT THIS BOUNDARY. Main is the v551 pen
or a descendant; four gating workflows green at every content state (`live-scoring-proofs` is dispatch-only;
five files, four gating — measured from the trigger map).
**#292 is DONE AND ON MAIN** (landed `ab68430`, tree content-verified against its seal; awaits the owner's
close click). **#290 rehearsed L0 and L1 to exit under nine filed addenda (A–I)** on branch
`claude/seam-relay-step4-fp78jm`, final tip `3cccb9d`, working tree clean, everything committed or declared
void — seam-verified. **L1 exits 96 PASS / 1 FAIL** (the single red is the accepted G-Y0 waypoint 19.869%;
the 2.000% bar judges the CONVERGED fixed point, not mid-leg). The outgoing #290 seat's handover
(#290 comment 5139994403) carries its three self-caught faults deliberately — one shape: conclusions stated
before testing. **A fresh #290 seat opens on the owner's paste** to measure **L2's two window candidates**.
The **EXECUTION word remains WITHHELD** — it follows the full rehearsal hand-back, after L2–L8.

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

## THE QUEUE
- **#290 — FRESH SEAT OPENS on the owner's paste; its task is L2's TWO WINDOW CANDIDATES** (censor-aware-2003
  vs uniform-2004+): both measured — cell populations, gate classifications, surface deltas — presented at
  the HALT; **the owner words the window; L3 never starts before it** (non-training prep allowed, A.1). Then
  L3–L8 rehearsal → the full hand-back verified the seam way → **the EXECUTION word** → the landing legs →
  candidate board → adoption (owner's separate act: adoption word · FHV word · five SCAR→VOR relabels · the
  appended lineage register entry authored THERE, never earlier, never pre-drafted with placeholders).
  Landing-critical facts a successor must hold: L1 lands as ONE commit under Addendum C.1's identity set
  (the 8/8 `release_contract.identities` mirror; field-level re-stamps only; the ten historical `45b207c0`
  occurrences provably unchanged) · the EIGHTH γ site `rl_model.py:504` (read-default axis) is in the L1(a)
  set · the refit FOLLOWS E2 inside L1(b); L6 keeps only convergence + the POOL/MSD/SSP re-measurement ·
  L1's exit = green boot AND green build lane · every engine act strictly serial behind
  `tools/preboot_assert.sh` · costs: L1 chain 480s, `--bake` 71s, ci-guards-equivalent ≈17 min ·
  L5 dockets by name: the payload-hash NAMED HELPER (recipe `md5(json.dumps(curve, sort_keys=True))`,
  int ladder — seam-reproduced both identities) · manifest-vs-code-default equality asserted for EVERY
  pinned `RL_*` · the `ev()` namespace finding · int-cast-vs-widen framed for L6 beside the re-measured pool.
- **#276 clubs tab · #270 referee** — post-adoption · #139 feeds · v1.1 read outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
The **L2 window word** (at the halt, measured candidates presented) · the **EXECUTION word** (after the full
rehearsal hand-back verifies) · close clicks **#292 #283 #275** · branch deletes — **HOLD
`claude/step-4-execution-supervisor-g4edkc`** (until tree `e339b1e9` reaches main via L0's landing) ·
**HOLD `claude/pre-referee-baseline-shaping-4ql38z`** (sole carrier of the stop-point artifacts until L1
lands them, N12) · **HOLD `claude/seam-relay-step4-fp78jm`** (the live #290 branch) · FREE:
`claude/trade-desk-pricing-split-ui-44652r` + the six measured-free at v550 + the seam carrier branch ·
later: adoption set · the v1.1 read.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND THE M1–M3 TRIPWIRES (second 2026-07-31 block) govern; read them first
- **M1:** an owner-facing reply longer than ~one screen is prima facie a C1 violation — verdict and decision
  in the reply, detail in the filings. **M2:** before every in-seat act ask: *deciding-figure re-run, ruling,
  or audit?* If no — delegate (searches, status reads, artifact location, bulk extraction are NEVER in-seat;
  Opus for mechanical, Fable where judgment is the task; every subagent conclusion re-verified by re-run).
  **M3:** state your context posture in one line at every pen. The outgoing seam drifted on all three
  DESPITE having read C1/C2 — principles lose to load; the tripwires exist because of it.
- The owner's casual questions are load-bearing QC. This cycle's catches, all from measuring rather than
  reading: the #292 stale clone · the C.2 lineage mis-homing (the entry shape said L8/adoption) · the
  self-matching preboot assert (probe every instrument a directive adds — run it, both directions, before
  blessing it) · the head[5] wrong-state transcription · the eighth γ site (hazard 7 on the CONFIGURATION
  axis: what SETS a value and what READS it with a fallback are different censuses).
- The permanent guards: REASONING IS NOT EVIDENCE · never present a number not read from a committed
  artifact · every count names its denominator · sweep "what is missing" with no filter · prove every
  instrument can fail IN BOTH DIRECTIONS (an assert that cannot pass is as vacuous as one that cannot fire)
  · one pen per boundary, batched · post-rebase-merge verify main by CONTENT · seal-cites-main before any
  branch delete · never re-spec a gate to trust the thing it checks (the G.5 lesson — F1 was right).

## ENVIRONMENT CARRIES — carried from v42 in full, plus this cycle's: `/home/claude/rl_workspace/` is
bootstrap's CANONICAL layout AND a single shared mutable workspace — every engine act strictly serial behind
`tools/preboot_assert.sh` (no lockfile, by seam ruling; reversal = a second violation despite a working
assert) · provision `bash setup_env.sh` + independent 5-pin proof, 3.12 asserted · the 1.0524 fallback has
THREE sites · TWO never-conflate per_entrant pairs: (2f8b4bd4 curve input / 40d7da7c byte-freeze) and
(77eba4d3 VOR arm / db8c934c SCAR arm, both at `session_2026-07-30/item279/out/` on the SHAPING branch) ·
the stop-point artifact `ruled_curve_final_279.json` (payload `e69a3f38` · factor_s 0.977688 presentation ·
Σ(1..64)=54,722 · head […, 2886, 2453, **1931**] · pick64 221) lives ONLY on the shaping branch until L1
lands it · the DOB courier durable at `docs/evidence/dob_courier_2026-07-31/` · **HAZARD:**
`ui/tests/responsive_layout.test.mjs` writes into COMMITTED evidence (`:33`/`:185`) — never commit `-a`
after running it · the #290 rehearsal evidence at `docs/evidence/rehearsal_290_2026-07-31/` (L0 rows +
adjudication + the full L1-exit diff `L1_amended/L1_amended_state.diff`) · **PEN MECHANICS**: the register
is ONE header line; each pen (i) bumps the stamp near char 88 (`· v55X 2026-07-31 · PEN:` → X+1), (ii)
inserts its entry immediately BEFORE ` · SEAM v540 (2026-07-29)`, (iii) proves pre-commit: line count
unchanged · growth == entry length · exactly one new `SEAM v55X` stamp · PRIOR count unchanged · docs-only
diff; then Part B replaced wholesale, commit as `supervisor-seat <supervisor@seam.local>`, branch → PR →
rebase-merge → re-verify main by CONTENT.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v551 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 open (#292 done, open for the close click) · #271 #274 closed · PRs
   #297–#299 merged, none open; four gating workflows green; the #290 branch at `3cccb9d` or a descendant
   carrying the runbook with nine addenda A–I + the evidence trees (`e339b1e9` step-4 pack + the rehearsal
   evidence); the three HOLD branches intact.
2. #290's fresh seat opens on the owner's paste (opener already handed to him): it reads the record, reads
   back on-issue, HOLDS for the seam's go via the owner's paste. When its L2 presentation arrives: verify
   both candidates' measurements from committed artifacts (M2: delegate the sweep, re-run the deciding
   figures yourself), then bring the owner the window decision simply — question, options, recommendation,
   one line each. L3 stays halted until his word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.