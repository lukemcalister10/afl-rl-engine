# CURRENT STATE — the incoming-seat read · v55 · supervisor pen · 2026-08-04, register v563

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
lane**: branch → PR → rebase-merge. The merge under the owner's platform auth is a **housing fact,
not an approval step**. Docs-only pens land **without a per-entry word** (v483, restored by owner
word 2026-07-27), guarded by structural asserts proven pre-commit: line count unchanged, growth equal
to entry length, single stamp, PRIOR chain intact, docs-only diff. **Reversal is self-executing** —
any pen error reaching main restores the per-entry word.

**Ref deletion is proxy-forbidden to seats.** Branch deletes are an owner click. Do not retry it.

---
# PART B — CURRENT STATE
(v55 · supervisor pen · 2026-08-04, register v563 · replaced wholesale at the sibling-order pen — the lens
basis is ruled: the ruled curve's own structural machinery; the seam raises rotation at this boundary)

## THE ERA: THE CONSISTENCY ERA — #306 EXECUTING; THE SIBLING ORDER IS OUT (comment 5178008507). Main is the
v563 pen or a descendant; four gating workflows green at every content state. **#292 DONE AND ON MAIN**
(`ab68430`; awaits the owner's close click). **#306:** the flat-lens approval was VOIDED (v562); the revised
`m(pos, age, pick)` smooth-field design (seat filing 5177163945, branch `27f8a82`) audited clean on MECHANICS
(byte-identical re-run; locality 0.7728/0.1407; local neutrality worst 1.75e-04 across all 64 picks) — but
the owner's interrogation exposed its RAW MATERIAL: the lens was being fitted from the year-zero surface's
SELF-REFERENTIAL SLOT PRIOR (the lineage #279 measured at 0.0248% reality — the owner's "1/4000th",
literal). **THE SIBLING ORDER** (owner word, verbatim in 5178008507) retires that fit target and rules: the
lens fits from the **#279 structural career values** — the ruled curve's own machinery, inherited wholesale
(class window 2004–2022 HARD CUT · concluded careers realized-in-full · never-established at 0.0 · active =
played-so-far × concluded-look-alike completion, busts' zero-remainders in stratum · prior only as a counted
fallback · McCartin/Boyd exclusions + slides · VOR, γ=1.0 · reuse `harness_pvc.py structural_values()` from
`session_2026-07-30/item279`, branch `…-4ql38z`) — "we're looking at pick 4, and seeing what it'd be worth
if it was a defender, midfielder, key forward etc. based on outcomes." The record's LIVE carrier is
**`claude/exec-seat-290-handoff-d7bnaa`** at **`7e9d7f9`** (frozen ancestors j0kwl0 `8e8c15b` · fubolo
`abf8f4c` · fp78jm `3cccb9d`). The **EXECUTION word remains WITHHELD**; nothing has landed at any point.

## THE TWO-CURVE IDENTITY CENSUS — v563; READ FLAGS AS SEMANTICS AT YOUR PERIL
| curve | payload | what it is | where it lives |
|---|---|---|---|
| the SHIPPED curve | `08ea9375` | #271 stage-B ladder, measured by #279 at 0.0248% reality | main's `pvc_curve_v2.json` / `release_pick_curve.json` — replaced at the landing |
| **the RULED curve — THE ANCHOR** | **`e69a3f38`** | #279 structural ladder: classes 2004–2022, pick64=221, NO pick 65, completion +4.7–8.4% optimistic REPORTED | the rehearsal substrate (pass-0 capture `13b71c26`); ships with the EXECUTION word |
The matrix's `incurve`/`teaches_curve` flags describe the SURFACE fit population (drafts 2003–2025, 38%
still-active) — NOT the pick curve's teaching set (1,197 rows, classes 2004–2022). `in_hist` (2003–2021) is
the engine's separate hist cohort; it fed neither curve. Every rehearsal measurement asserts `e69a3f38`
before computing — the anchor side has never been contaminated.

## OUTCOME FACTS THE OWNER'S QUESTIONS ESTABLISHED (realized careers vs same-pick peers; durable copy 5178008507 thread)
Early KPD careers run BELOW peers (0.60–0.79 at picks 3–20), above only late (1.33 at 60) — the old
surface's early-KPD-high belief is unsupported · RUCK careers run 1.31–1.84 ABOVE peers at almost every pick
while their year-one games run 0.24–0.64 — the owner's standing finding, reproduced · mature 19–20 careers
run 1.16–1.42 above peers mid-late draft (n_eff 28–54); 21+ ~0.90; ZERO drafted 21+ exist in the top 10 —
never draw a line where no data lives · the surface population carries 553/1,444 still-active careers —
completion-not-presumption must govern any outcome fit (the structural basis supplies exactly that).

## THE CAPTURE TABLE — A RECIPE IS CURRENT ONLY TO THE CAPTURE IT NAMES
| capture | md5 | yields `data/v0surf.pkl` | base |
|---|---|---|---|
| `L6_pass0_state.diff` — the LIVE substrate & N35-assert state | `13b71c26` | **`fb9efdec`** (curve `e69a3f38`) | `f0128d6` |
| `LA_anchored_state.diff` — the voided flat-lens state (sealed record) | `02e248dc` | `1a52b787` | `6736a6f` |
| `L6_HALT_state.diff` — the halt state, held | `137c6d2c` | `31e7f00b` (curve `ca662051`) | `3ffbc1f` |
| `L4_state.diff` — sealed L4 exit-record | `2cc5041c` | `84fb0cde` | `f0128d6` era |
(peak `f305fe53` / pvc `ade79790` across all. A sibling-basis design + capture is expected next.)

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Older standing law as v54 recorded it: N1–N38 stand. This cycle:
N39. **THE SIBLING ORDER (owner word, 5178008507):** the lens's `_v0_raw`/slot-prior fit target is RETIRED
    (the #279 surgery completed at the position/age layer); the lens fits from the #279 STRUCTURAL CAREER
    VALUES with window/completion/exclusions/denomination inherited wholesale; anchor `e69a3f38` unchanged
    (N6/N34); all v562-era orders stand (smooth field · graded locality · hierarchical confidence · m ∈
    [0.5, 2.0] · local neutrality per pick · no hard bands anywhere · per-pick presentation, no-data fades);
    the KPF-floor decision is WITHDRAWN (wrong-basis; re-poses only if the bound binds on the new basis);
    the completion optimism (+4.7–8.4%, 25.1% of teaching rows) is stated beside every result. [v563]

## THE QUEUE
- **#306 — the seat designs the SIBLING-BASIS lens** (orders: 5176541552 laws · 5177058181 confidence/locality
  spec · 5178008507 basis), measured on committed rows, per-pick, HOLD for seam audit — LAWS FIRST, mechanics
  second → implement on approval → acceptance on the artifact (per-pick local neutrality + bounds; band-free)
  → **L-B** deterministic lane (failing direction discharged by the recorded cross-container pair) → **the
  pool-division measurement** (N37) → **L-C** per the amended benchmark → **L6 re-enters under R-H/R-I/N19
  unchanged** → converged G-Y0 vs N16 naming the surface md5 → L7–L8 → full rehearsal hand-back → **the
  EXECUTION word** → the landing (ruled curve + converged surface ship together) → candidate board →
  adoption (owner's separate act).
- **#276 clubs tab · #270 referee** (bias-1 N17) — post-adoption · **#139 feeds** · v1.1 read outstanding.

## OWNER ACTS OUTSTANDING
**The seam rotation** (raised again v563 at ~460k, charter C3 — also standing from v562 on its own grounds) ·
paste the sibling order's relay to the seat · the **EXECUTION word** (after the full rehearsal hand-back) ·
**the pool LEVEL ruling** (after the N37 measurement) · close clicks **#292 #283 #275** · the
`rl_replacement_derive.py` search (N23) · branch deletes — **HOLD** g4edkc · 4ql38z (carries the #279
machinery the sibling order reuses — DO NOT delete before the landing) · fp78jm · fubolo · j0kwl0 · N12
holds until the landing reaches main · pen-token re-issue at the owner's discretion.

## RUNNING THIS SEAT WELL — charter C1/C2/C3 AND M1–M3 govern; read them first
- **M1** one-screen replies, detail in filings · **M2** deciding-figure re-run, ruling, or audit — else
  delegate · **M3** context posture at every pen.
- **The owner's communication word (binding):** every agent return in VERY SIMPLE terms — what they did,
  whether it worked, what he must decide. Relays IN HIS CHANNEL. Answer him HERE before filing anywhere.
- **The v562–v563 lessons, paid in trust:** check every design against the owner's stated intent FIRST
  (hazard 16) and state its load-bearing property in ONE PLAIN SENTENCE · a chart of model beliefs is not a
  chart of outcomes — say which it is, every time · never draw where no data lives · a flag's name is not
  its semantics — trace what a flag actually feeds before quoting it · the owner's memory of his own rulings
  beats derived views; verify against the primary record before contradicting him. His questions became
  N36–N39: when he pushes, measure — never defend.
- The era's verification standards: **v558** byte-identical re-runs · **v559** verify the capture pair ·
  **v560** classify boxes by output bytes (N35).

## ENVIRONMENT CARRIES — as v54 in full (measurements/ lane · sealed captures · compute-path assert
`92e397bd` · strictly serial behind `tools/preboot_assert.sh` · venv 5-pin proof · N32 · N33 · N35 recipe ·
envpin proportion facts · **PEN MECHANICS** unchanged: stamp near char 88 `· v56X <date> · PEN:` → X+1, SAME
LENGTH · insert immediately BEFORE ` · SEAM v540 (2026-07-29)` · line count unchanged · growth == entry
length · one new `SEAM v56X` stamp · docs-only diff · Part B wholesale · commit as `supervisor-seat
<supervisor@seam.local>` · branch → PR → rebase-merge → re-verify main by CONTENT · reset the pen branch
onto origin/main before each pen), plus this cycle's: **the #279 structural machinery is the lens's basis of
record** (`session_2026-07-30/item279/harness_pvc.py structural_values()`, branch `…-4ql38z`,
RETENTION-PROTECTED) · the two-curve census above · the committed sibling-era measurement scripts
(`lens_field_sim.py` — mechanics-valid, wrong-basis targets; its successors fit from structural values).

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip = the v563 pen or a descendant; issues #290 #292 #279
   #283 #275 #276 #270 #269 #146 #139 #306 open · #271 #274 closed · no open PRs; four gating workflows
   green (in-flight stated as in-flight); the LIVE carrier at `7e9d7f9`; the `zlaarm` branch at `27f8a82` or
   a descendant; the five frozen/HOLD branches intact; the capture table by apply-and-hash (minimum:
   `13b71c26` → `fb9efdec`, curve payload `e69a3f38`).
2. **Read the owner's laws (Part A), the v562 correction (5176541552), and the sibling order (5178008507)
   IN FULL before auditing anything.** The next seam act: audit the sibling-basis design — owner's laws and
   the BASIS first (does it fit from the structural values, the right window, the right completion?), then
   mechanics (byte-identical re-runs; N35-classify your own box first). State every design's load-bearing
   property to the owner in one plain sentence. Bring him each outcome simply.
3. Read-back to the owner in his channel — short and simple — then hold for confirmation before any push.
