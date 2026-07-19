# DIRECTIVE — LEG D: THE PVC RE-DERIVATION (construction memo FIRST → checkpoint → derive)
**v1.0** · 2026-07-17 · supervisor seat 12 (Fable-authored per SPEC v1.4 §3: the G-Y0 tolerance +
derivation construction are this directive's design load) · build model: **Opus via Claude Code** ·
ONE JOB, ONE CHAT (S2; the checkpoint is this job's designed midpoint, not scope growth)
STATUS: ISSUED — fire when pasted by the owner. Do not fire from the repo alone.

## ⛔ EXECUTE FIRST — BEFORE READING ANYTHING ELSE (your first committed artifact is this block's proof)
```
bash tools/seat/first_commands.sh 2>/dev/null || true   # if present on your checkout, it prints the six verdicts
git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/claude/r1067-wiring-v11-m86stv
#   MUST print 33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7 — anything else: HALT, report, stop.
git fetch origin claude/r1067-wiring-v11-m86stv
git checkout -B claude/legd-derivation 33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7
git merge-base --is-ancestor 33c8b52cb7a38d5fda2ceff5d3fb96841575c2e7 HEAD && echo ANCESTOR-PROOF-PASS
md5sum engine/rl_after/rl_model_data.json      # MUST begin 968de0c7 — anything else: HALT.
grep -n "END OF CALENDAR YEAR 1" engine/rl_after/s4_matrix_7147.py   # MUST hit ~:62 — else wrong tree: HALT.
git fetch origin claude/legd-groundwork        # THE EVIDENCE FEED — this fetch line IS the KAT fetch path
git show 9845180:session_2026-07-17/legd_groundwork/GROUNDWORK_LEGD.md | head -5   # MUST render — else HALT.
```
Commit the output as `session_2026-07-17/legd_derivation/FIRST_COMMANDS_PROOF.txt` — your FIRST
commit, before the PLAN (prescreen REJECTS any branch whose first commit is not this proof). You are
NOT on main; main carries only docs. Base = the Leg-C candidate head (PR #105); your PR stacks on it.

## THE FIVE (CORE)
- **EFFORT: High.** Why not Extra: the constructions are settled by ruling (derive-from-distribution ·
  numéraire pin · population-level G-Y0) and the groundwork already measured the pool — this job
  chooses among MEASURED options and implements the ruled one; the open design questions route to the
  owner at the checkpoint, not to deeper autonomous search. Why not Medium: it re-derives the curve
  every pick and young player prices through, wires a new BINDING gate, and produces the board the
  owner views at the ladder.
- **MODE: auto.** First committed artifact after the proof = the PLAN. Scope limits = the FENCE, nothing else.
- **TIME: 6–10 h across the checkpoint** (ACT 1 ≈ 2–4 h · ACT 2 ≈ 4–6 h). Confirm up front; flag
  >2×/<½×; report actual. The checkpoint wait is not build time.
- **FEED (documents, not restatements):** DECISIONS v122 · CONSTRAINTS v1.19 (PART 6 G-Y0 · PART 7 ·
  PART 8 row 8–10) · **acceptance_v1_21.json — ASSERT these entries:** `leg_d_placeholders.pvc_strict_descent`
  · `leg_d_placeholders.g_y0_population` · `leg_d_placeholders.posture_2027_discounts` (10/15/5 EXACT) ·
  `numeraire.law` (pick 1 == 3000) · `guards[G-Y0]` (BINDING; `fix_direction` = **RE_DERIVE_AT_LEG_D** —
  the retired raise-young-side remedy is history, NEVER an instruction) · `leg_c.season_prog` (0.58,
  owner dial, UNTOUCHED) · SPEC v1.4 §3 LEG D + §6.3/§6.4 (OPERATIVE, item 313) · the GROUNDWORK
  EVIDENCE at `claude/legd-groundwork` @ `9845180` (fetch path in the block above): GROUNDWORK_LEGD.md +
  out/job2_circularity · job3_survivorship · job4a/4b/4c · job5_acceptance_draft + selftest ·
  docs/NOTE_seat8_legD_circularity_survivorship_2026-07-16.md · register items 130–132 · 194 · 197 · 204 · 309.
- **FENCE.** IN: `engine/rl_after/_merged_recover.py` (the pick-curve derivation/consumption sites,
  incl. the `_iso_dec`/`_fit_pick_curve` chain named at :801-region and the V0 pole `v0_start` :1157-region —
  exact lines re-named from YOUR tree) · `engine/rl_after/s4_matrix_7147.py` (READ; the anchor) · the
  curve artifact (`engine/rl_after/pvc_curve_L1b.json` → its stamped successor) · `engine/rl_after/
  one_source_selftest.py` (harness wiring) · promotion of the job-5 harness into the frozen suite ·
  derived artifacts + `data/expected_boot.json` re-pin · your `session_2026-07-17/legd_derivation/` dir.
  OUT: **the SOURCE STORE — READ-ONLY this entire leg; any store-write impulse is a HALT-and-ask** ·
  docs/ (always) · every Leg-B dial · SEASON_PROG · the flex/§1b machinery beyond reads · lens/posture
  code (Leg E's) · `rl_model.py` unless the ACT-1 site census names a consumption site there — in which
  case HALT AT THE CHECKPOINT and ask; never extend the fence yourself (the item-281 law).

## BASE PIN (store/engine base ⇒ STRICT equality)
Branch `claude/r1067-wiring-v11-m86stv` must resolve to **`33c8b52`** exactly (the ls-remote in the
block above); store md5 at base = **`968de0c7`**; board of the base = `9829d01a`. Any drift ⇒ HALT.
Docs pins are at-or-after and irrelevant to you — you never read docs from main mid-job; the FEED is sealed above.

## THE JOB — TWO ACTS

### ACT 1 — THE CONSTRUCTION MEMO (read-only; the spec's "first act = the measurement discipline")
1. **RE-EMIT THE EVIDENCE ON THIS BASE.** The groundwork's magnitudes were measured at `6306378`/store
   `0efdc5d6` and are provisional BY ITS OWN HEADER. Re-run its emitting scripts (they are committed at
   `9845180` under `scripts/`) against YOUR base (store `968de0c7`): the 2083-entrant pool totals, the
   job-2 circularity tiers, the job-3 exit + peak/anchor tables, the job-4c per-pick counts + smoother.
   Every number in the memo comes from a committed artifact emitted THIS session (counts are
   script-emitted, never typed). Differences vs the groundwork are FINDINGS to state, not problems.
2. **THE SITE CENSUS (item-281: sites named FROM THE CODE, with numbers).** Name every site where the
   shipped curve is derived, loaded, refit, or consumed: the yr-1 anchor (`s4_matrix_7147.py:62`), the
   V0 pole (`v0_start`), the `_iso_dec` import-time refit (:801-region — PART 7 names it an UNCLEARED
   determinism input), the curve artifact and its readers. State, from the code, what a re-derivation
   must replace and what it must leave.
3. **THE MEMO** (`session_2026-07-17/legd_derivation/MEMO_LEGD_construction.md`), owner-readable, with:
   - **The derivation construction — the job-2/NOTE options weighed with THIS base's numbers**
     (A drop-the-poles · B honest-calibration yr-4 end · C two-ends · the life-path pool for the
     survivor tail), a RECOMMENDATION with the symmetric case for each branch, and what each does to
     the yr-1-snapshot understatement (job 3: peak/anchor 1.69–2.66, U-shaped in ratio, top-heavy in
     SCAR). The smoother question rides here (the MEDIAN kernel flattens the tail — job 3's finding).
   - **DESIGN CONSTRAINTS (BINDING, restate and honour):** derive at the finest resolution the sample
     supports, smoothed — wide bins presentation-only (CORE rule 7; job 4c is your resolution
     evidence) · NO THRESHOLD may enter the construction (L-SMOOTH; every transition a curve) ·
     weight-don't-gate for any evidence weighting (R105.4) · **the new curve is an OFFLINE-DERIVED,
     STAMPED artifact (md5 of store+code+config), LOADED not refit — no new import-time fits (the
     q97m/`_iso_dec` disease; PART 7); state how the existing `_iso_dec` chain is retired or bypassed
     by the new path** · include busts (job 3 confirms the current anchor already does; keep it true).
   - **THE G-Y0 TOLERANCE PROPOSAL:** signed residuals by pick decile (audit #37 weighed, per the
     job-5 draft), a concrete proposed number/shape WITH the measured residual distribution that
     motivates it — **the NUMBER is the owner's to rule; propose, never set.** The gate is BINDING and
     effective at THIS derivation (R104.7); design so the ruled tolerance is assertable by the job-5
     harness unchanged.
   - **THE PICK-BAND WIRING PLAN:** held pick = the LIVE curve over its ladder band [low, high]
     (mean; owner weights later if supplied); 2027 picks × (1 − discount), discounts PER-POSTURE
     **0.10/0.15/0.05 EXACT** (R104.5/§6.3), asserted in every generated artifact.
   - **PLANNED TESTS:** multi-start + prior-removed derivations (audit #34/#35/#44) — enumerated, not run yet.
   - **A-PAIRS NOTE:** pair 3 (Sanders/Bontempelli) maps to THIS chapter, but the derivation is NEVER
     result-conditioned on it (L-AXIS; the no-hand-edit doctrine). It is scored at the ladder; the memo
     may state the expected direction, nothing more.
4. **PRE-VIEW HASHES:** record md5s of the memo + `docs/acceptance_v1_21.json` in the checkpoint
   commit, BEFORE any candidate curve renders. Later mutation HALTs the ladder.
5. **CHECKPOINT — committed and PUSHED, ≤25 lines**, naming: the recommended construction + the
   symmetric alternatives · the proposed G-Y0 tolerance · the site-census verdict (fence in/out) ·
   the re-emitted headline numbers. **HALT.** The supervisor prescreens and couriers to the owner;
   the paste-back carrying HIS ruled construction + HIS tolerance number is the go for ACT 2.
   (If this chat's budget is spent at the checkpoint, ACT 2 re-fires as its own chat from your pushed
   checkpoint SHA — a clean seam, not a failure.)

### ACT 2 — THE RE-DERIVATION (on the couriered word; implement the RULED construction exactly)
6. **DERIVE THE CURVE** per the ruling: offline, stamped, committed; **L7 re-base pins curve(1) == 3000**
   (assert). Kill-switch **`RL_PVC2`**: `RL_PVC2=0` ⇒ the shipped curve path byte-exact (board
   `9829d01a` reproduced — assert the md5).
7. **WIRE THE GATES (all halt-not-warn, verdicts committed):**
   - **R104.9 STRICT DESCENT — HARD:** `curve(p+1) ≤ curve(p) − 1`, p = 1..79. The shipped curve fails
     this with **15 plateau violations** (job 5's live self-test: 1→2 at 3000, 7→8, the 343/342 tail
     flats). The new curve must clear ALL 15; the harness runs in the frozen suite.
   - **G-Y0 POPULATION GATE at the OWNER-RULED tolerance** (effective HERE; a red is a HALT of this
     build, not a report). Multi-draft average; a single class off-curve is NOT a breach.
   - **R104.5:** `{balanced: 0.10, contender: 0.15, rebuilder: 0.05}` asserted EXACTLY in every artifact.
   - Numéraire pin · stamp-assert-not-stale (S1) · the promoted job-5 harness as the one instrument (S4/S5).
8. **PICK BANDS WIRE** per the memo plan (§3): live-curve band mean; 2027 × (1 − posture discount).
9. **PLANNED TESTS RUN:** multi-start + prior-removed (audit #34/#35/#44) — committed results; divergence
   between starts is a FINDING with numbers, not a silent pick.
10. **DERIVED + BATTERY:** rebuild board/book/panel; re-pin `expected_boot` (the F2 designed-behaviour
    class — say so in the commit); full battery, frozen-suite-only (S4), hash-cached reuse (S1).
    **HALT SEMANTICS: the G-COHORT 1.30 cap is the SOLE hard halt; a sub-1.08 floor reading is
    REPORTED, never a self-halt.** One line in the session notes fixes nothing else: the job-4a 2019
    provenance prose (a stale "gapless" annotation; the VALUE 65 is correct) is reported for the
    supervisor's pen — inputs/ annotation files are docs-adjacent; do not edit them yourself.

## DELIVERABLES (assert artifacts, never prose statistics)
- The proof · the PLAN · the memo + pre-view hashes · the pushed checkpoint · per-task commits ·
  candidate PR stacked on #105.
- **THE NEW CURVE** (stamped artifact) · **DIFF vs the SHIPPED curve** (stamp-asserted — the S5
  stale-curve failure never repeats) · **reconcile vs the owner's workbook curve** (reference only;
  his Pick Values tab dies with the old PVC).
- **PER-GATE COMMITTED VERDICTS — MANDATORY:** strict descent (all 15 old violations shown cleared) ·
  G-Y0 at the ruled tolerance with the per-decile residuals · R104.5 exact-values · numéraire ·
  Guard 4/5 · F1/F2 · G-COHORT y-band · earned-component (the item-272 two-row waiver is IN acceptance
  — score Carroll/Emmett, never flag) · A-PAIRS (score both pairs against the v1.21 bands; pair 3
  expected to move — report direction and magnitude) · E/B. Each with its exit code; SILENCE IS A RED.
- **NAMED ROWS (committed JSON, exact figures):** the top-10 pick values old→new · Bontempelli ·
  Reid · Sanders (A-PAIRS raw values) · Gawn · the two largest young movers either direction · every
  held-pick asset old→new.
- **THE LEDGERS on the moved board (item-256 schema):** the all-active MOVEMENT ledger + the
  value-up-rank-down FAILURE subset (positional-rank tie-break; ranks carried).
- RETURN ≤30 lines · branch · head SHA · PR number · "in plain terms" close · actual time.

## STANDING CONDUCT (HANDOVER rev158 §3 — binding here)
First commands proof-first (298/299) · a KAT names its fetch path (304/309 — done for you in the
EXECUTE-FIRST block) · counts EMITTED BY SCRIPTS into committed artifacts, never typed (295/309) ·
per-gate committed verdicts, silence is a red (295/306) · checkpoint HALTs arrive PUSHED (282) ·
sites named from the code (281) · stable-ID identity everywhere (269) · one authored source — the
store is READ-ONLY this leg (SSI) · Smoothness Law + L-AXIS + weight-don't-gate as written above ·
no terminal item-counts · designs captured to the memo, not chat.
