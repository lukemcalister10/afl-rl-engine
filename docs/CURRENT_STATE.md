# CURRENT STATE — the incoming-seat read · v36 · supervisor pen · 2026-07-30, register v544

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
(v36 · supervisor pen · 2026-07-30, register v544 · replaced wholesale at the three-landings pen)

## THE ERA: POST-ADOPTION, SHAPING RULINGS CLOSED, TWO LANDINGS DOWN, PROPAGATION MID-FLIGHT. Main is
`b306400`; ALL FOUR WORKFLOWS GREEN. Today's three landings: **#283 MERGED** — the store is now the single
source of ownership truth (store `81d24704`; the owner's 18 July-29 moves live; sidecar = generated mirror,
never authoritative; board `f2df6e0a` untouched by seam byte-proof). **#275 MERGED** — the tree HALVED
(136→68.6MB, 2,310→1,432 files; 878 deletions, zero adds/mods; history never rewritten). **#279 STEP 4 is
mid-flight**: rehearsal phase 1 verified (gates fired in anger), the bake gate is OPEN against store
`81d24704`, and ONE runbook amendment is due before the bake-gated remainder. **The step — and the whole
shaping era — is ONE owner word from done: the execution word.** Both landed seats are ROTATED clean.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Carried unchanged from v35: FHV Option A (≈190) · future-leg blend hand-set · year-0 bar = ELIGIBILITIES ·
§1b retired · 62+3 edit set sealed · held-mechanism law · tie-sensitive instruments barred · Best-23 = A19
law (live) · movers/era-succession law · G-Y0 dated exception (2.929/3.035/3.50; 2.000% hard bar; retires AT
ADOPTION, new exception = owner act) · the five #279 rulings N1–N5 (VOR · structural/≤2022/par-per-season ·
control · pooled numeraire + honest confirmation condition · pool≈tail with the 233 re-measure requirement) ·
N6 α=1.0 (curve e69a3f38, ladder 54,722, s=0.977688; the s-invariance reading; the "three decimals"
correction by addendum). New:
N7. **Ownership single-source law (#283, LANDED):** the store's `affl_team` is the ONE truth; the sidecar is
    a generated mirror with a store-pin check (a wrong-store sidecar is refused); ownership rides the
    appended release_transition entry lane, never a round apply. **EXACT-BYTE COURIER LAW:** the store takes
    the owner's bytes verbatim — canonicalize for the mirror, never for the store. **REPIN SWEEP LAW
    (standing, hazard class 7 on the identity axis):** sweep the OUTGOING literal AND the incoming — stale
    bundles are invisible to a current-literal sweep. Join by KEY (five board players have store name-twins;
    one was in the change set). [#283 seal + seam audits, on-issue]
N8. **Step-4 mid-flight words (all on #279):** F1 — RL_PICK1 joins the signature gates (measured silent
    surface channel; G3's self-falsification is the can-fail proof). F3 — the player-side ×s is TWO-SIDED:
    picks and players from ONE measured pooled head in ONE act (the engine's rescale is one-sided in
    practice — artifact pins picks, RL_PICK1 moves only players); G5 carries three negative controls
    (double, pick-alone, player-alone). Q1 — the declared refit overwrites the pickle wholesale; freeze
    history lives in `v0surf_refit_log.json` (amends the seam's word 3 — a recorded seam self-correction).
    **Q2 (OWNER-RULED): dual-position seasons teach under their PRIMARY COMPONENT** [owner word "Primary.",
    issuecomment-5137016272]; 0.5/0.5 examined and declined. REFEREE DOCKETS (report-only, in the step-4
    seal watch-items): duals-teach-both · the median-vs-mean tenure-ramp gap.

## THE QUEUE
- **#279 STEP 4 — the ONLY live lane.** State: rehearsal phase 1 VERIFIED (evidence `6e0e55e`: G2 dead-key
  halt in anger · G4 loud-halt vs bare IndexError · G5 12/12 both directions · cost 385s/cycle · Q2
  candidates measured). Bake gate OPEN (store `81d24704`, main `b306400`-or-later, pinned tip named in the
  before-picture). NEXT: one runbook amendment (F1 gate key + F3 two-sided design + Q1 overwrite + Q2
  primary) → quick seam audit → bake-gated rehearsal remainder → hand-back verified the seam way → **THE
  EXECUTION WORD** (the step's last). Then: candidate lands with the four-channel attribution ledger
  (channel A = the shipped artifact's store-lag, +2.24%, already committed) · adoption is the owner's
  separate act · adoption re-denominates FHV on one word (evidence N5) · #270 referee opens after delivery.
- **#276 — clubs tab** (post-#279-adoption; Q5/Q6 collectibles + optional FHV word at fire) · **#270 —
  referee** opens after #279 delivers, inheriting three report-only dockets (duals-teach-both · median-vs-
  mean ramp · truncation-backtest optimism, the N2 watch-item) · #146 never as written · #139 feeds the
  others · v1.1 amendment read still outstanding (owner) — and 13 PLAN_v1.1-cited screenshots are RETAINED
  pending it (re-ballot at the next hygiene pass after the read).

## OWNER ACTS OUTSTANDING
The EXECUTION WORD (after the amendment audit + bake-gated rehearsal pass) · later: the adoption word + the
FHV re-denomination word · close clicks on #283 and #275 (acceptance fulfilled, merged, seats rotated) ·
branch-delete clicks (`claude/issue-283-supervisor-rrjyzw` · `claude/afl-rl-engine-275-audit-tp9akk` ·
`claude/seam-authority-afl-rl-oseyxv` after this pen · the shaping branch stays — its evidence is
retention-protected) · the v1.1 read.

## RUNNING THIS SEAT WELL — owner-endorsed law (charter D3/D4 + three cycles' additions)
- Answer the owner HERE, completely, FIRST; filings are durable copies, never the reply. Plain sentences.
  His casual questions are load-bearing QC — this cycle alone they caught the s-invariance framing, the
  store-positional attribution channel, the 0.5/0.5 design question that surfaced the median-ramp docket,
  and the b6 referee-read constraint. Treat every one as an instrument.
- Cost-estimate norm before commissioning builds · rehearsal norm for first-of-a-kind lanes · subagents Opus
  by default · spill API payloads to files · register by window only (ONE ~450KB line) · every count NAMES
  ITS DENOMINATOR · prove every instrument can fail BEFORE trusting it · **NEVER present numbers not read
  from a committed artifact** · medAE flatters low curves; judge means with mean-targeting instruments ·
  REVIEW LANES by owner word 2026-07-30: Opus-subagent cold-screens of seam work standing-approved, AND the
  seam may self-review when the owner asks (pen double-checks included); implementer≠reviewer still governs
  seat work products · **REASONING IS NOT EVIDENCE — a seat's (or the seam's) mechanical claim enters a seal
  only as a measurement; this cycle's two catches: the seam's word-3 pickle mechanism (code contradicted it)
  and the seat's RL_PICK1 transitivity (its own probe falsified it).**
- One pen per boundary, batched. Hand-backs: re-run the 2–3 measurements that decide; full content-level
  verification at final seals. Post-rebase-merge: re-verify main by CONTENT — tree-object ids are the clean
  content seal (the #275 pattern: the seat re-derives the expected tree at its rebased head; the merged main
  tree must equal it byte-exactly).

## ENVIRONMENT CARRIES
cp312 via RL_VENV (container python3 is 3.11 — always the pinned interpreter) · git fetch --unshallow before
ancestry claims · no parallel engine builds without seam coordination · env -i ONLY with an explicit
whitelist; loaders assert nonempty · CRLF in the owner's CSV lane is an Excel artifact, never "fixed" ·
rebase-merge rewrites SHAs: seal by content (tree ids) · **repin sweeps run on the outgoing AND incoming
literal (N7)** · **sibling_repin is KNOWN-REFUSING** (state pins a pre-adoption store; stale against two
values; docketed to the next lawful sibling build — weekly lane or step 4; do NOT hand-stamp it) ·
**deletion protection: sealed-record-cited files (charter D2) AND anything an outstanding owner read
depends on (owner word 2026-07-30)**.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen (expect the v544 pen commit or a
   descendant); open PRs (none, or this pen's pre-merge); issues #279 #283 #275 #276 #270 #269 #146 #139
   open (#283/#275 close on owner clicks) · #271 #274 closed; all four workflows green at the tip.
2. Step 4 is mid-flight on `claude/step-4-execution-supervisor-g4edkc`: its runbook amendment lands on #279
   for seam audit; then the bake-gated rehearsal remainder; verify its hand-back the seam way (re-run the
   deciding figures from committed artifacts, never prose) before the owner's execution word.
3. Read-back to the owner in his channel; hold for confirmation before any push.
