# DIRECTIVE — LEG-B GAP DIAGNOSTIC (read-only) · 2026-07-16 · Tier 3 · seat 10
### STATUS: fires on the owner's paste. Owner ruling of record (register item 253, verbatim):
### "Diagnose first." Purpose: reconcile the memo lineage's PREDICTION (β_eff ≈ 0.81 at s=0.65,
### rev148 §2 — flagged there as prediction, NOT measurement) against the seg-5 MEASUREMENT
### (β = 0.6747 at s=0.65; grid EMPTY at the owner's 0.80 bar — register item 252), and map what
### could honestly reach the bar. THIS JOB SETS NO NUMBERS AND CHANGES NOTHING.

## EFFORT: High. Why not Medium: the memo algebra must be reproduced faithfully and the gap
## decomposed term-by-term over 116 players × 4 grid points plus counterfactual profiles — a
## Medium pass would eyeball it. Why not Extra: no design work, no writes, bounded sample.
## MODE: auto — the first committed artifact is the PLAN.
## TIME: 1–2.5 h. Confirm up front; flag >2×/<½×; report actual.

## BASE PIN — verify with full-URL ls-remote against https://github.com/lukemcalister10/afl-rl-engine.git
- **Engine/store base — STRICT:** branch `claude/legb-segment5-law-grid-flq57f` at **`91d08f2`**
  exactly (the prescreened seg-5 return head; item 252). Work on a NEW branch from it
  (`claude/legb-gap-diagnostic-*`); commit ONLY under `session_2026-07-16/legb_gap_diag/`.
- **Docs base:** main AT OR AFTER **`277e843`**, `git diff --name-only 277e843..main` docs/-only.

## FEED (documents, not prose restatements)
docs/MEMO_LEGB_functional_form_2026-07-16.md (v1.3; seal md5 `cf6c0080…`) ·
docs/acceptance_v1_20.json (seal md5 `6b83e336…`) ·
session_2026-07-16/segment5_law_grid/FINDING_empty_grid_HALT.md + GRID_FINAL.out (the
measurement of record) · session_2026-07-16/uncompress/beta_measure.py (the FROZEN estimator,
md5 `14c59139` — the ONLY instrument whose β numbers count as verdicts; S4) · DECISIONS refs:
R104.10 (any Leg-B path must pre-sim under G-COHORT 1.30) · R105.4/.5/.6 · this directive.

## THE JOB (read-only; every output a committed artifact)
1. **THE DECOMPOSITION.** Per player over the proven-27+ estimator sample (n=116), at each grid
   s: the realised weight w = s·E·ramp split into its terms (E evidence-saturation; onset ramp;
   plus the ρ ratio and the per-position conservation renorm C's give-back). Where, numerically,
   does the nominal s go? Committed as a CSV + a ≤1-page reading.
2. **THE RECONCILE.** Reproduce the memo lineage's predicted-β computation as written. Identify
   the exact assumption(s) that diverge from measurement and attribute the ~0.14 gap term by
   term (prediction bridge: 0.81 → 0.6747). If the prediction cannot be reproduced from the
   memo's own text, SAY SO — that is itself the finding.
3. **THE REACH MAP (findings, never proposals).** For each honest lever the decomposition
   exposes (e.g., the evidence rate, the onset width, the conservation construction — whatever
   the numbers implicate): the measured w-profile and the β it would deliver across a stated
   range, computed with the frozen estimator on counterfactual boards where feasible, otherwise
   clearly labelled algebraic projections. For ANY profile reaching β ≥ 0.80: the G-COHORT
   y4/y5/y6 pre-sim at that profile (R104.10) + the E/B (hard 1.75) implication. Report levers
   symmetrically; propose NO selection, tune NOTHING shipped.
4. **THE ESTIMATOR'S OWN STORY.** n=116, bootstrap CI width ≈ 0.30, the s=0.70 CI straddling
   the bar: state plainly what the point-estimate rule can and cannot distinguish at this sample,
   and what sample growth (e.g., live-round ingestion) would change. No re-specification of the
   estimator — its verdict construction is owner law.

## FENCE
IN: reading everything · computing/committing under `session_2026-07-16/legb_gap_diag/` only.
OUT (touch = HALT): engine · store · config · docs/ · acceptance · gates/guards · any grid
extension or re-tune · any seat-authored number presented as a selection. SILENCE IS A RED:
every check prints a verdict or the job HALTs; no result swallowed by a pipe.

## RETURN
≤30 lines + a plain-terms close: branch · head SHA · the gap bridge in one line · the reach-map
headline (which levers can/cannot honestly reach 0.80, with G-COHORT/E-B riders) · the estimator
story in one line · actual time · APP counter. Artifacts carry everything else.
