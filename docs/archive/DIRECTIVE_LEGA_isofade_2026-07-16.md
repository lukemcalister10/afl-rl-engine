# DIRECTIVE — LEG A: THE iso_corr EVIDENCE-FADE + ISO MONOTONIZATION · 2026-07-16
### THE PVC+FLEX CHAPTER OPENER (spec: docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md, §3 Leg A).
### TIER 1 candidate leg · store/engine WRITER (the only one in flight) · fires ONLY on the owner's
### written word, pasted into a FRESH Claude Code chat. One job, one chat, candidate PR, retire.

## EFFORT: High. Why not Medium: `iso_corr` multiplies raw_ev at EVERY valuation site
(`_merged_recover.py` :747 :855 :889 :1032 :1041 · `_ov_angleA.py:39`) — a defect here moves every
player. Why not Extra: ONE surgical mechanism; the fade instrument (the v2.10 evidence-weight `w`)
already exists and is baked; no new statistical fitting beyond the fade family.

## MODE: auto — your FIRST COMMITTED ARTIFACT is the PLAN (S2: fence sized to finish in one chat with
a clean RETURN, never a checkpoint apology).

## TIME: one working session (2–5 h of chat time). Confirm up front; flag >2× or <½×; report actual.

## BASE PIN (THE BASE-PIN RULE, full URL):
`git ls-remote https://github.com/lukemcalister10/afl-rl-engine.git refs/heads/main`
**main AT OR AFTER `b78dd8e77c462a84d7fc812a8a01bc90d9628b63`, and
`git diff --name-only b78dd8e..main` must be `docs/`-ONLY.** (The supervisor pen moves main between
writing and pasting.) On entry, Guard 5 asserts the pinned boot store (`b1fd0bce`) before the engine
loads. Engine tree expected `fc7045d6` — a different engine hash is a HALT-AND-ASK, not a warning.

## FEED (fetch these AT THE PINNED SHA from the repo — documents, never prose restatements):
- `docs/SPEC_PVC_FLEX_CHAPTER_v1_2026-07-16.md` (§1 law · §3 Leg A · §5 acceptance frame)
- `docs/DECISIONS_v106_2026-07-16.md` + `docs/CONSTRAINTS_v1_17.md` + `docs/acceptance_v1_16.json`
  (v1.16 remains the machine-readable set until v1.17 files with Leg B — assert its entries)
- `docs/OPEN_ITEMS_REGISTER.md` items **130 · 131 · 132** (VERBATIM law: no young net-strip ·
  lift-led · conserving · two-directional · the fade construction) and **170** (the measured baseline)
- CORE v2.8 (S1–S6 · SILENCE IS A RED · frozen-suite-only measurement)

## THE JOB (per-task commits, in this order)
1. **THE FADE.** `iso_corr(pos, pk)` gains an evidence fade in the house family on the v2.10 weight
   `w`: FULL strength at zero evidence (debut/V0 — where the pick IS the information — unchanged BY
   CONSTRUCTION), dissolving toward **1.0** as evidence saturates. Effective form:
   `iso_eff = 1 + (iso_corr − 1) · fade(w)` with `fade` from the house family (the same family as the
   pedigree fade; the PLAN names the exact member + its one parameter and cites the family's code
   home). Wire at EVERY site listed above — a missed site is a red, not a note.
2. **MONOTONIZE the ISO table** across picks within each position (kills the pick-19 0.882 <
   pick-34 1.000 Newcombe trough) — isotonic non-increasing penalty toward later picks (equivalently:
   no LATER pick may carry a HIGHER multiplier than an earlier one). This now matters only where the
   pick still speaks (low `w`).
3. **KILL-SWITCH** `RL_ISOFADE` (env-gated, DEFAULT ON in the candidate; =0 restores v2.10 behaviour
   byte-for-byte — prove it with a gated A/B board build).
4. **HYGIENE RIDERS (one-shot, in-fence):** (a) ship-gates strip/reject `SGC_*` env leakage (the
   three-build tripwire, rev143); (b) DELETE the dead `if not _EVW:` discrete-regime branch
   (`_merged_recover.py:358–372`) with an OBITUARY comment per SSI (delete, don't disable).
5. **MEASURE (frozen suite only; ad-hoc constructions are FINDINGS, never verdicts):**
   before/after board with the switch ON — · full movers list (expect PURE LIFTS concentrated in
   proven mid-round picks; **English and the trough rucks are the faces**) · the WHERE-DOES-THE-
   VALUE-GO report (ΣΔ · age/cohort distribution · over-performer scan — item 130's standing check;
   **any young net-strip or any above-projection young player cut is a HALT**) · census-v2 unearned
   gauge (must not grow past +15,612) · L-SMOOTH discontinuity census on the new multipliers ·
   G-COHORT y1–y5 (hard 1.30) · A-PAIRS scored · English/Briggs priced ratio printed (the R104.3
   floor 1.75 is a CHAPTER acceptance — Leg A alone need not reach it, but print where it lands).
6. **Self-test additions:** the fade is asserted (a zero-evidence player's iso unchanged; a
   saturated-evidence player's iso ≈ 1.0 within tolerance) and the monotone table is asserted.
   SILENCE IS A RED: every check prints a verdict or HALTs; exit codes propagate.

## FENCE
IN: `_merged_recover.py` (iso construction + wiring + the two riders) · `_ov_angleA.py:39` ·
gates/self-test additions · derived-artifact regeneration (board/matrices, stamped per S1).
OUT (touch = HALT): the output→price map (Leg B) · the store (Leg C — NO store writes; the eleven
future-position changes are NOT yours) · the PVC/pick code (Leg D) · lens/UI · ALL docs authoring
(builds never author docs) · gates' thresholds (never self-amend a gate).

## RETURN (≤30 lines + committed artifacts): branch · head git SHA · PR number · the measured set
above · confirm the kill-switch A/B byte-identity · "in plain terms" close. A return without its SHA
is incomplete. The supervisor prescreens against item 130's value-flow check + this directive; the
cold audit rides the CHAPTER ladder, not this leg.
