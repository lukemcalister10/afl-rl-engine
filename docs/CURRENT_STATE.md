# CURRENT STATE — the incoming-seat read · v35 · supervisor pen · 2026-07-30, register v543

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
(v35 · supervisor pen · 2026-07-30, register v543 · replaced wholesale at the α pen)

## THE ERA: POST-ADOPTION, SHAPING RULINGS CLOSED. Main is `ba96ed2` (the v542 pen); ALL FOUR WORKFLOWS
GREEN at the tip — the all-green baseline holds. **The #279 shaping step's ruling sheet is COMPLETE:
currency VOR · basis STRUCTURAL/≤2022/par-per-season · fitter CONTROL · pin POOLED NUMERAIRE in principle ·
α = 1.0.** The #279 execution seat is ROTATED, its final hand-back seam-verified clean (every commissioned
figure recomputed from the committed pack at `9914c4d` on `claude/pre-referee-baseline-shaping-4ql38z`:
payload hashes reproduced under the pack's own convention, fold sds recomputed exactly, evidence-tree-only
diff). **STEP 4 — PROPAGATION — is the queue head: opener FILED on #279 (https://github.com/lukemcalister10/afl-rl-engine/issues/279#issuecomment-5132497378), fresh seat opens on
the owner's paste; rehearsal norm in full before any execution word. The opener was COLD-SCREENED pre-filing
(fresh-context Opus reviewer): three blockers found and folded — the comment-1 supersession (C1 real store
fields `_retired`/`_last_listed`; C2 γ/pick-1 hard pins at build_peak_model_v4.py:8) entered the read order,
and the draftval fix gained its locator (_merged_recover.py:1573).** #283 and #275 are FIRED the same day —
three seats may run in parallel; the #283-before-step-4-bake sequencing rule is in both filings. No seat
live at this pen.

## STANDING RULINGS DIGEST — the map, NEVER the law (charter O1). Act on a ruling → read its durable copy verbatim.
Carried from v34 unchanged: FHV Option A (≈190, #270 ruling comment) · future-leg blend hand-set (#270
retirement comment) · year-0 bar = ELIGIBILITIES column (#271 A4/A6) · §1b retired by supersession (#271
A4/A5) · 62+3 edit set sealed (#271 A12) · held-mechanism law (#271 A11) · tie-sensitive instruments barred
(#271 A13) · Best-23 = A19 law (live via #274 item 2) · movers/era-succession law (#271 A15/A16; the
single-slot limit FIXED by #274 item 1; the balanced_board_md5 three-way disagreement stays hygiene's, with
its loud tripwire) · **G-Y0 dated exception STANDS until step 4 re-derives the bar honestly**: 2.929% ruled /
3.035% held / 3.50% hard FAIL [#271 A12/A13]. The five #279 rulings:
N1. **Currency = VOR (γ=1.0)** ["ruling is VOR. Lock it in"]. Adoption echo bounded: 21 rucks ≤29 points via
    the ruck-cap channel alone; the signature is curve-sensitive but γ-blind — RL_GAMMA enters the gates at
    step 4. [#279 currency ruling]
N2. **Basis = STRUCTURAL, teaching cut at class ≤2022, par = PER-SEASON teaching.** Concluded careers vote
    full; actives completed from concluded look-alikes busts-included; prior = counted thin-stratum fallback
    ONLY — a WATCHED NUMBER at every rebuild (5.93% at ruling). Truncation backtest consistently optimistic
    (+4.7% at kept depths) — THE WATCH-ITEM if the curve ever reads generous. [#279 basis ruling]
N3. **Fitter = CONTROL** (shipped kernel + local-linear boundary correction, >1%-mass-off-domain rule).
    The distfirst DECOMPOSITION (establishment rate × value-if-established) is a standing report-only
    artifact beside the curve. [#279 fitter ruling]
N4. **Pin = POOLED NUMERAIRE, in principle.** PAVA pools the head honestly; ONE global factor
    s = 3000/pooled-head re-denominates the WHOLE economy — players included, at step 4 only. The
    CONFIRMATION CONDITION rides step 4 IN ITS HONEST FORM: passes on the ruled fitter (raw-pick-1 sd
    56.10 → pooled-head sd 27.29) and would NOT survive as a general claim (quieter in 2 of 4 panel arms,
    panel mean −3.6%; distfirst noisier — head-pool-size switching between folds); one owner word reverts
    to the hard pin if the bake's churn measure disqualifies. [#279 fitter+pin ruling]
N5. **Pool ≈ tail equivalence (measured):** under the ruled basis the pool level 239.7 [211,268] n=1,005 vs
    picks 60–64's cohort 233 — statistically the same asset (the 233 is REGISTER-CARRIED with no committed
    artifact behind it: step 4 re-measures the tail cohort with n and interval before the law line lands); the descent asserts bite over 1–64 only; one
    law-text line lands at step 4. Priced denominators: MSD 303 n=44 · SSP 341 n=31 (STORE stream counts
    106/52 are census, not pricing populations); medians ~0 — the interval is the finding. These feed the
    FHV re-denomination word at #279's adoption. [#279 final segment report]
N6. **α = 1.0** ["Agree with a=1. Let's lock it in"]. At the stop, α=1 IS the ruled curve: payload
    `e69a3f38`, ladder 54,722, s = 0.977688 (pooled head 3068.46; recovered clipped mass 137.93 — expressed
    as a UNIT change, not extra head units). Unit-adjusted conservation 0.9998 at α=1; every downside dial
    taxes the pick class (−2.4 / −6.5 / −8.3 / −14.2%, softened by the pooled numeraire from
    −4.2 / −8.2 / −11.9 / −17.7 hard-set); the upside lin 0.9→1.05 (1.0588× at pick 64, −0.2%) filed
    without a lean, NOT taken. THE s-INVARIANCE READING (owner-confirmed, recorded in the ruling): the −2%
    ladder fall is a unit change; the player-side ×s at step 4 preserves every pick-to-player relativity;
    the ONE real relative move is the head vs picks 3–64 (~2.2% — the recovered clip, deliberate); until
    step 4 lands, the new-unit ladder and the old-unit player values must NOT be read against each other.
    SEAM CORRECTION on the pack, fix-by-addendum queued to step 4: "identical to three decimals" overstates
    the α=1 conservation pair (0.9998 vs 0.9980, gap 0.0018; downside pairs ≤0.0008; the finding — dial
    cost is a property of the dial, not the pin — stands). [#279 α ruling]

## THE QUEUE — everything fires on an owner word; seam pre-fire audit at each fire
- **#279 STEP 4 — PROPAGATION, the finale. NEXT; opener FILED (https://github.com/lukemcalister10/afl-rl-engine/issues/279#issuecomment-5132497378); the opener is the directive.**
  Fresh execution seat opens on the owner's paste. Scope: v0 surface refit under everything ruled (reads the
  ADOPTED store's per-season positions — per-position bust reality enters via the structural completions and
  per-season par teaching; movers from that channel attributed like any other) · curve re-derived to
  coherence (reference `e69a3f38`; recompute s at the bake; drift attributed, never silent) · G-Y0
  re-derived honestly (the dated exception resolves) · RL_GAMMA into the signature gates (prove it can
  fail) · the pool's ruled level ships (levels ×s: POOL 234.3 [206.4, 262.3] n=1,005 · MSD 296.4 n=44 ·
  SSP 333.4 n=31) · par per-season with the par_build LOUD-HALT (empty group halts NAMING the group, never
  IndexError) · player-side ×s + the pin confirmation condition (honest form, N4) · ruck-cap bite check
  (Stanley 812→610 exposure, binding unknown; report only) · draftval stale comment fix · the pool≈tail
  law-text line (N5) · the "three decimals" correction by addendum (N6). **REHEARSAL NORM IN FULL:**
  runbook first, rehearsed END-TO-END in scratch (unbakeable by construction — RL_V0SURF_REFIT is on the
  must-unset list) before any owner execution word; the seam audits the runbook pre-fire. Deliverable: an
  attributed candidate beside the shipped state; a mover with no named cause is a HALT-and-report finding.
  Adoption is the owner's separate act; adoption then re-denominates FHV (one word; evidence N5).
- **#283 — ownership single-source fix: FIRED 2026-07-30 (owner word).** Store becomes truth, sidecar becomes
  generated mirror, oracle unchanged; the owner's July-29 CSV (18 moves, currently NOT on the board) is the
  acceptance fixture. Pre-fire audit PASSED on-issue; seat opener filed; seat opens on the owner's paste.
  SEQUENCING RULE (binding): the store-write LANDS before step 4's rehearsal bake pins store identity, or
  holds for post-adoption. The read-back must resolve the store-identity ripple lane (the crux; it's why
  #232 dodged the store) and state the landing estimate vs step 4's bake.
- **#275 — hygiene: FIRED 2026-07-30 (owner word).** Pre-fire audit PASSED on-issue with a BINDING SCOPE
  AMENDMENT (ui/screenshots/issue_274 + docs/evidence/adoption_review_2026-07-30 + session_2026-07-29-onward
  are MUST-KEEP by name — sealed-record-cited = retention-protected, charter D2); seat opener filed; seat
  opens on the owner's paste. Deletions only; carries the balanced_board_md5 three-way docket (resolve or
  re-docket, never silent-drop).
- **#276 — clubs tab** (Q5/Q6 collectibles + optional FHV word at fire) · **#270 — referee** opens after #279
  delivers · #146 never as written · #139 feeds the others (item 20 = the retired replay's successor) · v1.1
  amendment read still outstanding (owner).

## OWNER ACTS OUTSTANDING
Open the step-4 seat (paste the opener) · after rehearsal passes: the execution word · later: the adoption
word + the FHV re-denomination word · fire words #283/#275/#276 · the v1.1 read · branch-delete clicks as they arise (the #274
close click is DONE — closed by owner 2026-07-30 14:17Z).

## RUNNING THIS SEAT WELL — owner-endorsed law (charter D3/D4 + both cycles' additions)
- Answer the owner HERE, completely, FIRST; filings are durable copies, never the reply. Plain sentences.
  His casual questions are load-bearing QC — they caught the frozen-ladder artifact, the pick-1 ceiling, the
  pool≈tail collision, and (this pen) the s-invariance reading and the store-positional attribution channel.
  Treat every one as an instrument.
- Cost-estimate norm before commissioning builds · rehearsal norm for first-of-a-kind lanes · subagents Opus
  by default, one-writer discipline, screen by deterministic re-run · spill API payloads to files · register
  by window only (the header is ONE ~450KB line) · every count NAMES ITS DENOMINATOR (store-census vs priced-
  population bit twice) · prove every instrument can fail BEFORE trusting it · **NEVER present numbers not
  read from a committed artifact — a prior seam fabricated two interpolated table columns, self-caught;
  read-verbatim is the only guard** · medAE flatters low curves where medians are ~0: judge means with
  mean-targeting instruments (signed error / RMSE) alongside · a held-out judge refuses mismatched fold
  fingerprints · REVIEW LANES by owner word 2026-07-30: Opus-subagent cold-screens of seam work are
  standing-approved, AND the seam may review its own work when the owner asks for a double-check (pen
  verifications included) — self-review on owner request is a permitted instrument, not a barred act; the
  charter's implementer≠reviewer taint still governs seat work products and cold reviews.
- One pen per boundary, batched. Hand-backs: re-run the 2–3 measurements that decide; full content-level
  verification at final seals (the #282 seal pattern: fence audit on the whole diff, CI via API not summary,
  byte-level pin checks). Post-rebase-merge: re-verify main by CONTENT (rebase rewrites SHAs).

## ENVIRONMENT CARRIES
cp312 via RL_VENV (do not weaken; container python3 is 3.11 — always the pinned interpreter) · git fetch
--unshallow before ancestry claims · no parallel engine builds without seam coordination · detached-worktree
discipline per #271 A13 (env -i with an EXPLICIT whitelist — the env -i path-stripping incident is the
cautionary tale; loaders assert nonempty) · CRLF in the owner's CSV lane is a known Excel artifact, never
"fixed" · GitHub rebase-merge rewrites SHAs: seal by content.

## THE INCOMING SEAM'S FIRST TASKS
1. Verify live state with your own commands: main tip vs this pen (expect the v543 pen commit or a
   descendant); open PRs (expect none, or this pen's PR pre-merge); the issue map (#279 #283 #276 #275
   #270 #269 #146 #139 open · #271 #274 closed); all four
   workflows green at the tip.
2. The step-4 seat: its READ-BACK lands as a #279 comment — the seam pre-fire audit happens there BEFORE the
   owner fires anything. When its rehearsal hand-back arrives, verify the seam way: re-run the deciding
   figures from committed artifacts, never from prose.
3. Read-back to the owner in his channel; hold for confirmation before any push.
