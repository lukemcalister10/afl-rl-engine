# DIRECTIVE — LEG-B UNFUNDED MEASUREMENT (dev-toggle, ships nothing) · 2026-07-16 · seat 10
### STATUS: fires on the owner's paste. Owner words of record: item 256 (conservation is not his
### law; unfunded value permitted; guards = G-COHORT + SINCERITY) and item 257 ("Measure").
### PURPOSE: measure the DECIDED output-anchored family with the per-position conservation renorm
### OFF (C≡1) — the road item 256 opened — against the frozen instruments. NO SELECTION IS MADE:
### the bar/grid construction returns to the owner with these numbers. This build SHIPS NOTHING.

## EFFORT: High. Why not Medium: five ON-boards + the frozen gate suite per point + an all-804
## rank ledger per point is real compute with real bookkeeping; Medium would thin the coverage.
## Why not Extra: one toggle, no design, no store writes, bounded grid.
## MODE: auto — first committed artifact is the PLAN.
## TIME: 2–3.5 h (engine loads dominate; seg-5 measured ~35 min/ON-point all-in). Confirm up
## front; flag >2×/<½×; report actual + the APP counter.

## BASE PIN — verify with full-URL ls-remote against https://github.com/lukemcalister10/afl-rl-engine.git
- **Engine/store base — STRICT:** branch `claude/legb-segment5-law-grid-flq57f` at **`91d08f2`**
  exactly (the prescreened Leg-B candidate head). NEW branch from it. ONE writer in flight: this.
- **Docs base:** main AT OR AFTER the SHA carried in the owner's fire paste;
  `git diff --name-only <that SHA>..main` must be docs/-only.

## FEED (documents, never prose restatements)
docs/MEMO_LEGB_functional_form_2026-07-16.md (seal `cf6c0080…`) · docs/acceptance_v1_20.json
(seal `6b83e336…`) · register items 254/255/256 (the corrected mechanism · the provenance finding
· THE OWNER'S RULING verbatim) · session_2026-07-16/legb_gap_diag/{DECOMP.csv, RECONCILE.md,
REACH_MAP.md} · session_2026-07-16/segment5_law_grid/GRID_FINAL.out ·
session_2026-07-16/uncompress/beta_measure.py (FROZEN, md5 `14c59139`) · this directive.

## THE JOB
1. **THE TOGGLE.** `RL_UNCONSERVE` env dev-override (the RL_ISOFADE/RL_UNCOMP_S pattern):
   `=1` ⇒ the §3 per-position renorm is identity (C≡1) on the un-compress map; unset/`0` ⇒
   shipped behaviour BYTE-EXACT. Default OFF. One clean commit, then a mini-checkpoint HALT
   (≤5 lines, diff SHA) for the supervisor's diff prescreen before any measurement.
2. **A/B.** Toggle unset ⇒ default board `8d90c9ac` BYTE-EXACT (and RL_UNCOMP=0 identity holds).
3. **THE MEASUREMENT GRID (measurement points, not a selection grid):** C≡1 at
   s ∈ {0.65, 0.85, 1.00, 1.25, 1.50}. Per point, ALL VERDICTS FROM FROZEN INSTRUMENTS ONLY (S4):
   - β via frozen `beta_measure.py` (md5-assert first), with CI + width-rail note (≤0.35) + n.
   - **G-COHORT y4/y5/y6 via the FROZEN repo gate suite** (the July-8 construction — the real
     gate, NOT the memo §6 proxy). This is THE unmeasured question of record: does the decided
     family unfunded hold ≤1.30?
   - E/B vs the owner's hard 1.75 · the census/unearned gauge · position-pool Δ totals (which
     pools re-rate, by how much — the owner expects to SEE this).
   - **THE SINCERITY LEDGER (item 256, all 804 rows):** ΔSCAR · Δ% · rank before/after · Δrank.
     Headlines per point: top-20 rank gainers/losers · the named row **Bontempelli** (the
     owner's own test: SCAR up AND rank up, or it is reported as a failure) · any player whose
     SCAR rises while rank falls, counted and named.
4. **HALT CONDITIONS.** Any G-COHORT breach at a point: record it and CONTINUE the sweep (a
   measurement job measures; breach points are findings). Any guard/suite failure to produce a
   verdict: SILENCE IS A RED — HALT.

## FENCE
IN: the one env toggle · the measurement grid · committed artifacts under
`session_2026-07-16/legb_unfunded_measure/` · the mini-checkpoint. OUT (touch = HALT): the
STORE · docs/ · config · acceptance · gate/guard code · shipped constants (UNCOMP_S_DEFAULT
stays None; UNCOMP_DECAY stays 0.25) · any selection, hard-coding, or tuning · grid values
outside the five listed.

## RETURN
≤30 lines + plain-terms close: branch · head SHA · per-point one-liners (β/width · y4/y5/y6 ·
E/B · Bontempelli SCAR+rank) · pool re-rate headline · sincerity-failure count · actual time ·
APP counter. The artifacts carry everything else. The disposition returns to the owner.
