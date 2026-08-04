# CURRENT STATE — the incoming-seat read · v47 · supervisor pen · 2026-07-31, register v555

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
(v47 · supervisor pen · 2026-07-31, register v555 · replaced wholesale at the L6 mid-loop rotation pen — the
EXECUTION SEAT ROTATED at a clean boundary; a fresh execution seat opens on the owner's paste)

## THE ERA: THE CONSISTENCY ERA — L6 MID-LOOP: PASS 0 DONE, PASS 1 SPECIFIED-NOT-EXECUTED. Main is the v555
pen or a descendant; four gating workflows green at every content state (`live-scoring-proofs` dispatch-only).
**#292 DONE AND ON MAIN** (`ab68430`; awaits the owner's close click). **#290:** the record's LIVE carrier is
**`claude/exec-seat-290-handoff-j0kwl0`** at **`8e8c15b`** or a descendant (fubolo frozen ancestor `abf8f4c`;
fp78jm frozen `3cccb9d`). L0–L5 CLOSED (L3 close v554 · L4 · R-A freeze · L5 census 187/187 · R-F seal). L6
runs under the R-H CONTROLLED REFIT LANE: both gates PASSED on the last box (compute-path `92e397bd` ·
double-fit `fb9efdec` twice); pass 0 (surface catch-up, curve unchanged) moved **G-Y0 13.919% → 8.084% on
`fb9efdec`** — the largest single move toward the 2.000% bar, and NOT a verdict; the loop contracts (s 0.9777
→ 0.9962 → 0.9982); curve 1 `1a8db02b` is derived, verified, and NOT installed. **The next act is
`PASS1_INSTALL_SET.md` executed atomically** — six files, interlocking derived hashes, the order is forced,
"the risk is atomicity, not time". The **EXECUTION word remains WITHHELD** — it follows the full rehearsal
hand-back after L6–L8.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law, each read verbatim before acting: FHV Option A ≈190 [#270 ruling comment] · Best-23 =
A19 law, live [#271 A19 / #274 item 2] · G-Y0 2.000% hard-bar law [data/release_contract held_checks + #271
A12] · movers/era-succession law [#271 A15/A16] · deletion protections: sealed-cited (charter D2) + anything
an outstanding owner read depends on [#275 audit, v544]. The era's rulings N1–N18 stand as v46 recorded them
(N16 now SUPERSEDED IN PART by N19 — read both). This cycle adds:
N19. **THE R-H CONTROLLED REFIT LANE** (seam, owner-reversible; supersedes N16's "L6's convergence" clause IN
    PART — `84fb0cde` stays the sealed L3–L5 substrate of record; C.4 stands whole): refits lawful only on a
    box passing the compute-path assert (pre-L4 rebuild → board `92e397bd` byte-exact) with the first refit
    double-run and byte-compared; every pass's surface committed bytes+md5+signature-key BEFORE load;
    migration mid-loop → HALT; the CONVERGED surface freezes and THE LANDING SHIPS IT (re-stamps
    `expected_boot.v0surf` inside C.1); the converged G-Y0 states against N16's trigger naming the converged
    surface md5. [#290 comment 5145089656; v555 item 5]
N20. **THE R-I BOUND:** fixed point = derived payload md5 EQUALS installed payload md5; bound = 4 passes;
    exhausted → HALT-and-report with the per-pass record, never declare. [#290 comment 5147350709; v555]
N21. **THE R-J CAPTURE-CURRENCY LAW** (N18 extension): any act touching a product file refreshes the ruled
    capture IN THE SAME evidence commit; prior captures seal as exit-records. "I checked this before" is not
    a check. [#290 comment 5147350709; v555]
N22. **THE SIGNATURE FACT:** `_v0surf_sig` hashes curve+roster+gates, NOT the fitted stack — two surfaces can
    share a key while bytes differ. A surface's IDENTITY is its FULL MD5 (Guard 5's pin); the signature only
    SELECTS. Signature-stability is never byte-stability. [#290 comments 5147273506 + 5147350709; v555]
N23. **THE R-F SEAL + R-G′:** MA.REPL bars are CARRIED-NOT-REGENERABLE — the deriver
    `rl_replacement_derive.py` PREDATES the repository (reform 2026-06-17; first commit 2026-07-02); HALT
    armed against any step re-deriving from them; `verify_anchors.py` RETAINED as their only surviving check
    (delete WITHDRAWN; landing remedy = re-default + docstring inside the identity set). The owner is
    searching his pre-repo environment for the deriver; found → exact-byte courier + 9-anchor verification.
    [#290 comments 5144529223 + 5145089656; v555 item 4]
N24. **N5 IS COMPLETE:** POOL = 233.0 (re-held 233.4), n=1,005, ci95 [205.2, 260.8], provenance 888/56/61 —
    committed artifact; the law line cites the measurement. MSD/SSP: intervals-and-denominators posture is
    BINDING; no point-estimate law lines. [#290 comment 5144529223 evidence + 5145089656; v555 item 5]

## THE QUEUE
- **#290 — A FRESH EXECUTION SEAT OPENS on the owner's paste.** Ruled opening order [#290 comment 5173035045]:
  (1) read CURRENT_STATE IN FULL + the runbook/Addenda A–I + `PASS1_INSTALL_SET.md` + the L6 chain (comments
  5145089656 · 5147273506 · 5147350709 · 5172917328) → **read-back on-issue, HOLD for the seam's go via the
  owner's paste**; (2) merge `8e8c15b` forward — true merge, carrier untouched (the `bf6596b` pattern);
  (3) **RECONSTRUCT THE SUBSTRATE from committed bytes**: apply `L6_pass0_state.diff` (md5 `13b71c26`, base
  `f0128d6`, applies at tip) → verify `fb9efdec` / `f305fe53` / `ade79790` byte-exact → regenerate the two
  `.srcmd5` (31s; md5s in the R-A freeze provenance) → **COMPUTE-PATH ASSERT `92e397bd` on the new box; FAIL
  → HALT to the seam, no refit runs there** (verification acts stay lawful — N16 cross-CPU determinism);
  (4) execute `PASS1_INSTALL_SET.md` ATOMICALLY in the working tree (rehearsal posture, R-C holds, nothing
  lands) + R-J same-commit capture refresh → loop under N19 to the N20 bound → **the L6 hand-back states the
  converged G-Y0 against N16's trigger, naming the surface md5** → L7–L8 → the full hand-back verified the
  seam way → **the EXECUTION word** → the landing legs → candidate board → adoption (owner's separate act).
  Landing-critical facts a successor must hold: L1 lands as ONE commit under Addendum C.1's identity set
  (8/8 mirror; field-level re-stamps only; ten historical `45b207c0` occurrences provably unchanged) · **the
  landing ships the CONVERGED surface bytes per N19** (supersedes the `84fb0cde` line; `84fb0cde` sealed as
  the L3–L5 record) · L3's T1 rides the landing set (`L3_T1_state.diff`, base `79ee8e5`) · the EIGHTH γ site
  `rl_model.py:504` is in the L1(a) set · the refit FOLLOWS E2 inside L1(b) · `ruled_curve_final_279.json`
  installs at L1(b) under its own identity set, NOT before · `derive_271.py`'s `fit_year0` is NOT edited (N3)
  · the bust-prior false-provenance note + `verify_anchors.py` remedy (N23) + the 65-mover attribution (R-D:
  unattributed movers HALT at L8) are LANDING-SET items · every engine act strictly serial behind
  `tools/preboot_assert.sh` · costs: build 31s · refit ~73s · chain 281s · compute-path assert 139s ·
  ci-guards-equivalent ≈17 min.
- **#276 clubs tab · #270 referee** (year-zero redesign home if L6 passes N16's trigger; bias-1 refinement
  N17) — post-adoption · **#139 feeds** · v1.1 read outstanding (13 screenshots held).

## OWNER ACTS OUTSTANDING
Paste the fresh #290 seat's opener (the hand-back 5172917328 + the seam's 5173035045) · the **EXECUTION
word** (only after the full rehearsal hand-back verifies) · the `rl_replacement_derive.py` search (N23; if
found, tell the seam — courier + 9-anchor verification follows) · close clicks **#292 #283 #275** · branch
deletes — **HOLD** `claude/step-4-execution-supervisor-g4edkc` (until `e339b1e9` reaches main) ·
`claude/pre-referee-baseline-shaping-4ql38z` (sole carrier of the stop-point artifacts) ·
`claude/seam-relay-step4-fp78jm` (frozen ancestor `3cccb9d`) · `claude/player-stack-290-handoff-fubolo`
(frozen ancestor `abf8f4c`) · N12 holds until the landing reaches main · FREE: as at v550 · later: adoption
set · the v1.1 read.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** before every in-seat act: deciding-figure re-run,
  ruling, or audit? — else delegate · **M3** context posture in one line at every pen.
- **The owner's communication word (2026-07-31, binding on successors):** every agent return is translated
  for the owner in VERY SIMPLE terms, short — what they did, whether it worked, what he must decide (options
  + recommendation, one line each). Relays he must paste are given IN HIS CHANNEL, never as a pointer to
  GitHub. Answer him HERE before filing anywhere.
- The owner's casual questions are load-bearing QC. Standing catches as v46, plus this cycle's: his "aren't
  the bars hand-set?" question surfaced the true provenance (five of six REPL values are the absent script's
  outputs verbatim; one owner dial KPF 67.8→66.8 baked 2026-07-04) — answer such questions from the record,
  never from memory.
- The permanent guards: REASONING IS NOT EVIDENCE · never present a number not read from a committed
  artifact · every count names its denominator · sweep "what is missing" with no filter · prove every
  instrument can fail IN BOTH DIRECTIONS · one pen per boundary, batched · post-rebase-merge verify main by
  CONTENT · seal-cites-main before any branch delete · never re-spec a gate to trust the thing it checks ·
  a negative sweep ends at WHY, not at "not found" (the R-F standard).

## ENVIRONMENT CARRIES — carried from v46 in full, plus this cycle's: **THE SUBSTRATE RECONSTRUCTION RECIPE**
(queue step 3 — the working tree is rebuilt from committed bytes on any new container; the live capture is
`L6_convergence/L6_pass0_state.diff` md5 `13b71c26` base `f0128d6`; sealed exit-records: `L4_state.diff`
`2cc5041c` · the L3_T1/L1_amended pair per N18) · **the two `.srcmd5` are the cannot-carry exclusion** —
regenerate 31s, md5s in the R-A freeze provenance · **`PASS1_INSTALL_SET.md` is the fully-specified next
act** (six files · hash-forced order · three hashes compute from bytes written earlier in the SAME act · the
8-vs-32 asymmetric convention fails if written the natural way) · pass-0 artifacts: surface `fb9efdec`
(committed bytes + IDENTITY) · matrix `pass0_matrix.json` `9c4bca53` · curve 1 `1a8db02b` (Σ 54,350 · strict
descent 63/63 · head 3000/2999/2864/2425/1892 · pick64 215; corroborated against step 4's converged
`fd9e8b63`, ladder Δ4) · the frozen fitted-model set `fitted_models_frozen_2026-07-31/` (peak `f305fe53` ·
pvc `ade79790` · cm_400 `34faa865` · q97m `cfdc7321`) · frozen v0surf `84fb0cde` SEALED as the L3–L5 record ·
prior carries all still live: `nd_matrix_ruled.json` `a216e6e6` · the per_entrant emit-in-place routing ·
`harness_pvc_REPINNED.py` full-chain pins · containers migrate hosts — provenance names the MACHINE and the
compute-path assert (`92e397bd`) is the gate on any refit box · the panel lane at
`session_2026-07-30/item279/panel/` · `/home/claude/rl_workspace/` strictly serial behind
`tools/preboot_assert.sh` · `bash setup_env.sh` + 5-pin proof, 3.12 · the 1.0524 fallback has THREE sites ·
the stop-point artifact `ruled_curve_final_279.json` lives ONLY on the shaping branch until L1(b) · the DOB
courier durable · **HAZARD:** `ui/tests/responsive_layout.test.mjs` writes into COMMITTED evidence — never
commit `-a` after running it · **PEN MECHANICS**: the register is ONE header line; each pen (i) bumps the
stamp near char 88 (`· v55X 2026-07-31 · PEN:` → X+1), (ii) inserts its entry immediately BEFORE ` · SEAM
v540 (2026-07-29)`, (iii) proves pre-commit: line count unchanged · growth == entry length · exactly one new
`SEAM v55X` stamp · docs-only diff; then Part B replaced wholesale, commit as `supervisor-seat
<supervisor@seam.local>`, branch → PR → rebase-merge → re-verify main by CONTENT.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v555 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 open · #271 #274 closed · no open PRs; four gating workflows green (a
   run in flight is stated as in flight, never predicted); the #290 LIVE carrier
   `claude/exec-seat-290-handoff-j0kwl0` at `8e8c15b` or a descendant; the FOUR frozen/HOLD branches intact;
   the pass-0 surface verifies (`fb9efdec`, committed bytes on the carrier).
2. The fresh #290 execution seat opens on the owner's paste: audit its read-back (deciding figures re-run,
   M2), give the go via the owner's paste, hold it to the ruled opening order (comment 5173035045) — the
   COMPUTE-PATH ASSERT on its new box decides whether the R-H lane is open there; FAIL → the seat HALTs and
   the seam rules. After L6: check the converged G-Y0 against N16's trigger and bring the owner the outcome
   simply, translated per his communication word.
3. Read-back to the owner in his channel — short and simple per C1/M1 — then hold for confirmation before
   any push.
