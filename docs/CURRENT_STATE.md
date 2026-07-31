# CURRENT STATE — the incoming-seat read · v44 · supervisor pen · 2026-07-31, register v552

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
(v44 · supervisor pen · 2026-07-31, register v552 · replaced wholesale at the window-word + v0surf-freeze pen)

## THE ERA: THE CONSISTENCY ERA — WINDOW A WORDED · L3 IN FLIGHT. Main is the v552 pen or a descendant; four
gating workflows green at every content state (`live-scoring-proofs` is dispatch-only; five files, four gating).
**#292 is DONE AND ON MAIN** (landed `ab68430`; awaits the owner's close click). **#290:** L0+L1 rehearsed to
exit (96 PASS / 1 FAIL — the single red is the accepted G-Y0 waypoint; the 2.000% bar judges the CONVERGED
fixed point). The record was carried forward by TRUE MERGE of `claude/seam-relay-step4-fp78jm` (frozen at
`3cccb9d`, an ancestor forever) into the LIVE seat branch **`claude/player-stack-290-handoff-fubolo`** (merge
`3d253c6`, pure-additive, proofs passed). **L2 was measured, presented at the HALT, and the owner worded
WINDOW A** (N15). **v0surf is frozen as committed bytes** (N16) after the container finding. **L3 is open,
baseline at `57bfea1`.** The **EXECUTION word remains WITHHELD** — it follows the full rehearsal hand-back.

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
    2026-07-31/` is the RULED SUBSTRATE for L3–L8, L6's convergence and the landing (`expected_boot.v0surf`
    re-stamps inside the C.1 set). Every G-Y0 statement names the surface md5 it was measured on; waypoints
    19.869% (predecessor container) and 13.919% (host 1/2) are container-bound; NO gate moves. The year-zero
    REDESIGN is DECIDED work — spec: constrained tail · deterministic fit lane · cross-machine byte-assert;
    TRIGGER = L6's converged G-Y0: fails the 2.000% law → fires immediately as the remedy (directive +
    pre-fire audit); passes → rides the referee era beside #270. Engine compute is PROVEN cross-CPU
    byte-deterministic once the surface is supplied. [v552 items 4–6; V0SURF_DIVERGENCE.md +
    CROSS_MACHINE_ASSERT.txt + PROVENANCE.md at 57bfea1]

## THE QUEUE
- **#290 — L3 IN FLIGHT** on the seat branch (`57bfea1`): carry the step-4 harness's ruled S-1/S-2 into the
  live `conditional_prior` path (1,572 of 1,930 resolved careers are CONCLUDED = 81.45% and currently teach a
  prior S-1 retires from them; the harness carries real store markers + counted fallback + sums-to-population
  assert) · land bias-1 BOTH limbs — 64 true phantoms of 13,221 rows (0.484%; the other 214 pre-2005 rows are
  draft-year zero-games BY DESIGN) AND the tenure offset (641 class rows over 106 players read one tenure year
  older than 2004-class on identical evidence). **SEAM REQUIREMENT on the L3 hand-back: both limbs presented
  MEASURED — treatment options with their prior-surface deltas — nothing chosen silently.** Then L4–L8 →
  the full hand-back verified the seam way → **the EXECUTION word** → the landing legs → candidate board →
  adoption (owner's separate act: adoption word · FHV word · five SCAR→VOR relabels · the appended lineage
  register entry authored THERE, never earlier). Landing-critical facts a successor must hold: L1 lands as
  ONE commit under Addendum C.1's identity set (the 8/8 `release_contract.identities` mirror; field-level
  re-stamps only; the ten historical `45b207c0` occurrences provably unchanged) · **the landing ships the
  frozen v0surf bytes** (`data/v0surf.pkl` ← `84fb0cde`) and re-stamps `expected_boot.v0surf` to it · the
  EIGHTH γ site `rl_model.py:504` (read-default axis) is in the L1(a) set · the refit FOLLOWS E2 inside
  L1(b); L6 keeps only convergence + the POOL/MSD/SSP re-measurement, and **its hand-back must state the
  converged G-Y0 against N16's trigger explicitly** · every engine act strictly serial behind
  `tools/preboot_assert.sh` · costs: L1 chain 480s, v0surf bake 66–71s (now never needed — bytes travel),
  ci-guards-equivalent ≈17 min · L5 dockets by name: the payload-hash NAMED HELPER (recipe
  `md5(json.dumps(curve, sort_keys=True))`, int ladder — seam-reproduced both identities) ·
  manifest-vs-code-default equality asserted for EVERY pinned `RL_*` · the `ev()` namespace finding ·
  int-cast-vs-widen framed for L6 beside the re-measured pool.
- **#276 clubs tab · #270 referee** (also the year-zero redesign's home if L6 passes) — post-adoption ·
  **#139 feeds** · v1.1 read outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
The **EXECUTION word** (after the full rehearsal hand-back verifies) · close clicks **#292 #283 #275** ·
branch deletes — **HOLD `claude/step-4-execution-supervisor-g4edkc`** (until tree `e339b1e9` reaches main) ·
**HOLD `claude/pre-referee-baseline-shaping-4ql38z`** (sole carrier of the stop-point artifacts until L1
lands them, N12) · **HOLD `claude/seam-relay-step4-fp78jm`** (frozen ancestor of the live record at
`3cccb9d`; its content is now contained in the seat branch's history, but the hold stands until the landing
reaches main, N12) · FREE: `claude/trade-desk-pricing-split-ui-44652r` + the six measured-free at v550 +
the seam carrier branches · later: adoption set · the v1.1 read.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND THE M1–M3 TRIPWIRES (second 2026-07-31 block) govern; read them first
- **M1:** an owner-facing reply longer than ~one screen is prima facie a C1 violation — verdict and decision
  in the reply, detail in the filings. **M2:** before every in-seat act ask: *deciding-figure re-run, ruling,
  or audit?* If no — delegate (searches, status reads, artifact location, bulk extraction are NEVER in-seat;
  Opus for mechanical, Fable where judgment is the task; every subagent conclusion re-verified by re-run).
  **M3:** state your context posture in one line at every pen.
- The owner's casual questions are load-bearing QC. This cycle's catches: the owner's questions removed a
  WASTED PINNED-REFIT step from the seam's own v0surf ruling (three iterations to final form — hold rulings
  loosely under owner QC) · the seam's ruled-in reconstruction assert caught a container divergence that
  matching signatures missed (`_v0surf_sig` keys on the INPUT — it cannot certify fitted bytes) · the #290
  seat self-caught a raw-store stdlib read (`pos` is derived at engine load — measure engine-derived
  quantities THROUGH the load path).
- The permanent guards: REASONING IS NOT EVIDENCE · never present a number not read from a committed
  artifact · every count names its denominator · sweep "what is missing" with no filter · prove every
  instrument can fail IN BOTH DIRECTIONS · one pen per boundary, batched · post-rebase-merge verify main by
  CONTENT · seal-cites-main before any branch delete · never re-spec a gate to trust the thing it checks.

## ENVIRONMENT CARRIES — carried from v43 in full, plus this cycle's: **CONTAINERS CAN MIGRATE HOSTS
MID-SESSION** — provenance names the MACHINE (CPU model + numpy dispatch tiers), never "this container" ·
the frozen v0surf at `docs/evidence/rehearsal_290_2026-07-31/v0surf_frozen_2026-07-31/` (`84fb0cde` / blob
`2f4c3859` / 49,758 bytes; PROVENANCE.md beside it) · the v0surf FIT is the chain's ONLY machine-sensitive
act (engine compute cross-CPU byte-identical: board `1432f5e4`, selftest `8d769d42` on both hosts; the
OpenBLAS byte-pin passes while dispatch differs — the pin is not the guard) · `l2_window_measure.py` carries
`L2_AUDIT_CONTROL=1` (the non-vacuity control on the instrument itself; original blob `d7c8655` in history) ·
the L2/L3 evidence under `docs/evidence/rehearsal_290_2026-07-31/` (`L2_window/`, `L3_baseline/`) · prior
carries: `/home/claude/rl_workspace/` is bootstrap's CANONICAL layout AND a single shared mutable workspace —
every engine act strictly serial behind `tools/preboot_assert.sh` · provision `bash setup_env.sh` +
independent 5-pin proof, 3.12 asserted · the 1.0524 fallback has THREE sites · TWO never-conflate
per_entrant pairs: (2f8b4bd4 curve input / 40d7da7c byte-freeze) and (77eba4d3 VOR arm / db8c934c SCAR arm,
both at `session_2026-07-30/item279/out/` on the SHAPING branch) · the stop-point artifact
`ruled_curve_final_279.json` (payload `e69a3f38` · factor_s 0.977688 presentation · Σ(1..64)=54,722 · head
[…, 2886, 2453, **1931**] · pick64 221) lives ONLY on the shaping branch until L1 lands it · the DOB courier
durable at `docs/evidence/dob_courier_2026-07-31/` · **HAZARD:** `ui/tests/responsive_layout.test.mjs`
writes into COMMITTED evidence (`:33`/`:185`) — never commit `-a` after running it · **PEN MECHANICS**: the
register is ONE header line; each pen (i) bumps the stamp near char 88 (`· v55X 2026-07-31 · PEN:` → X+1),
(ii) inserts its entry immediately BEFORE ` · SEAM v540 (2026-07-29)`, (iii) proves pre-commit: line count
unchanged · growth == entry length · exactly one new `SEAM v55X` stamp · PRIOR count unchanged · docs-only
diff; then Part B replaced wholesale, commit as `supervisor-seat <supervisor@seam.local>`, branch → PR →
rebase-merge → re-verify main by CONTENT.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v552 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 open (#292 done, open for the close click) · #271 #274 closed · PRs
   through the v552 pen's merged, none open; four gating workflows green; **the LIVE #290 record is the seat
   branch `claude/player-stack-290-handoff-fubolo` at `57bfea1` or a descendant** (`3cccb9d` on
   `…-fp78jm` is its frozen ancestor); the three HOLD branches intact; the frozen v0surf bytes verify
   (`84fb0cde`).
2. #290 is MID-L3. Its next hand-back arrives via the owner's paste: verify the S-1/S-2 carry-across and
   BOTH bias-1 limbs presented measured (M2: delegate the sweep, re-run the deciding figures yourself);
   after L6, check the converged G-Y0 against N16's redesign trigger and bring the owner the outcome simply.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
