# PLAN — LEG D: THE PVC RE-DERIVATION (auto mode, EFFORT High)

Branch `claude/legd-pvc-rederivation-o290ye` (harness-designated) pinned to directive base
**`33c8b52`** (store `968de0c7`, board `9829d01a`). First commit = `FIRST_COMMANDS_PROOF.txt`
(six EXECUTE-FIRST verdicts PASS). This PLAN is the first artifact after the proof.

Two ACTs across a designed checkpoint. **This chat delivers ACT 1 (read-only construction memo)
and HALTS at the pushed checkpoint.** ACT 2 fires only on the owner's couriered ruling (construction
+ G-Y0 tolerance number) — from this checkpoint SHA, this chat or a fresh one.

---

## SCOPE — the FENCE (nothing else)
**IN:** `_merged_recover.py` (curve derive/consume sites) · `s4_matrix_7147.py` (READ, the anchor) ·
the curve artifact `pvc_curve_L1b.json` → stamped successor · `one_source_selftest.py` (harness
wiring) · promotion of the job-5 harness into the frozen suite · derived artifacts + `data/expected_boot.json`
re-pin · `session_2026-07-17/legd_derivation/`.
**OUT (READ-ONLY / untouched):** the **SOURCE STORE** (entire leg — any store-write impulse HALTs) ·
`docs/` (always — I do not read docs from main mid-job; the FEED is sealed in the directive) · every
Leg-B dial · SEASON_PROG (leg_c.season_prog 0.58, owner dial) · flex/§1b beyond reads · lens/posture
code (Leg E) · `rl_model.py` unless the ACT-1 census names a consumption site there — then HALT at the
checkpoint and ask (never extend the fence myself: item-281 law).

## ACT 1 — CONSTRUCTION MEMO (this chat)
1. **Re-emit evidence on THIS base.** Copy the six groundwork scripts (committed @`9845180`) into
   `legd_derivation/scripts/`, re-pathing their OUT dir to `legd_derivation/out/`; run against MY
   base (store `968de0c7`). The groundwork measured store `0efdc5d6` @ `6306378` and is provisional
   by its own header — differences vs it are FINDINGS I state, never problems. Counts are
   script-emitted into committed artifacts, never typed (295/309).
2. **Site census from the code** (item-281, with line numbers on MY tree). Distinguish the two
   instruments (groundwork Job 1): the PVC (pick value, the day BEFORE) vs the V0 curve / `v0_start`
   (day AFTER, the G-Y0 gate instrument). Name every derive/load/refit/consume site; state what a
   re-derivation must replace and what it must leave. Verdict: fence in/out (esp. any `rl_model.py`
   consumption site → checkpoint question, not a self-extension).
3. **MEMO** `MEMO_LEGD_construction.md` (owner-readable):
   - Derivation construction options weighed with THIS base's numbers — A drop-the-poles ·
     B honest-calibration yr-4 end · C two-ends · the life-path pool for the survivor tail — with a
     RECOMMENDATION and the symmetric case for each branch; what each does to the yr-1-snapshot
     understatement (job-3 peak/anchor 1.69–2.66, U-shaped in ratio, top-heavy in dollars). The
     smoother question (MEDIAN kernel flattens the tail) rides here.
   - DESIGN CONSTRAINTS restated and honoured: finest resolution smoothed, wide bins presentation-only
     (CORE rule 7) · NO THRESHOLD in the construction (L-SMOOTH) · weight-don't-gate (R105.4) · the
     new curve is an OFFLINE-DERIVED, STAMPED artifact (md5 of store+code+config), LOADED not refit —
     no new import-time fit; state how the `_iso_dec`/`_fit_pick_curve` import-time chain is
     bypassed/left · include busts.
   - G-Y0 TOLERANCE PROPOSAL: signed residuals by pick decile (audit #37), a concrete proposed
     number/shape WITH the measured residual distribution that motivates it. **The number is the
     owner's to rule — propose, never set.** Design so the ruled tolerance is assertable by the job-5
     harness unchanged.
   - PICK-BAND WIRING PLAN: held pick = live curve over ladder band [low,high] (mean); 2027 picks ×
     (1 − discount), per-posture 0.10/0.15/0.05 EXACT, asserted in every artifact.
   - PLANNED TESTS: multi-start + prior-removed derivations (audit #34/#35/#44) — enumerated, not run.
   - A-PAIRS NOTE: pair 3 (Sanders/Bontempelli) maps here but the derivation is NEVER
     result-conditioned on it (L-AXIS). Scored at the ladder; memo may state expected direction only.
4. **PRE-VIEW HASHES.** Record md5 of the memo + the acceptance file BEFORE any candidate curve
   renders. (Acceptance version note below is a checkpoint finding.)
5. **CHECKPOINT** (≤25 lines, committed + PUSHED): recommended construction + symmetric alternatives ·
   proposed G-Y0 tolerance · site-census verdict (fence in/out) · re-emitted headline numbers. **HALT.**

## ACT 2 — RE-DERIVATION (only on the couriered ruling; NOT this chat)
Derive the curve per the ruling (offline, stamped, committed; L7 re-base pins curve(1)==3000).
Kill-switch `RL_PVC2`: `RL_PVC2=0` ⇒ shipped path byte-exact (board `9829d01a`, md5-asserted).
Wire gates (all halt-not-warn, verdicts committed): R104.9 strict descent HARD (clear all 15 shipped
plateau violations) · G-Y0 population gate at the owner-ruled tolerance · R104.5 exact 0.10/0.15/0.05 ·
numéraire pin · stamp-assert-not-stale · promoted job-5 harness as the one instrument. Pick bands wire
per the memo. Run planned tests. Rebuild board/book/panel, re-pin `expected_boot` (F2 designed-behaviour),
full frozen-suite battery, hash-cached. G-COHORT 1.30 cap = sole hard halt; sub-1.08 floor reported not
self-halted. Report the stale 2019 "gapless" annotation for the supervisor's pen (do not edit inputs myself).

## FINDINGS FLAGGED UP FRONT (for the checkpoint)
- **Acceptance version:** the engine base carries `docs/acceptance_v1_20.json`, not the FEED's
  `acceptance_v1_21.json`. Docs pins are at-or-after the engine base and OUT of my fence; the operative
  entries (pvc_strict_descent · g_y0_population · posture 0.10/0.15/0.05 · numéraire pick1==3000 ·
  guards[G-Y0]) are all present on v1_20 with substance identical to the directive's v1_21 restatement:
  v1_20 still records the retired `fix_direction` (raise_young_side…) but overrides it with
  `fix_direction_STALE_DO_NOT_APPLY` + `identity_2026_07_14_CORRECTED`; v1_21's `RE_DERIVE_AT_LEG_D` is
  the formalisation of exactly that override. I ASSERT against v1_20 (present) and pre-view-hash it.
- **`pvc_fit.py`** referenced by the groundwork is not a standalone file on this base; the PVC ships as
  the `pvc_curve_L1b.json` artifact loaded at `_merged_recover.py:1336-1339` (offline-derived by
  `l1_adopt_sim.py`, per the artifact's `source`/`derived_from` stamp). Census reflects the real tree.

## CONDUCT (rev158 §3): proof-first · counts script-emitted not typed · per-gate committed verdicts
(silence is a red) · checkpoint HALTs arrive PUSHED · sites named from the code · store READ-ONLY this
leg · Smoothness Law + L-AXIS + weight-don't-gate · designs to the memo, not chat.

TIME: ACT 1 ≈ 2–4 h (confirmed in range).
