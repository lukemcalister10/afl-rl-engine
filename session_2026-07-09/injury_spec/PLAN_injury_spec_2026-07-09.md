# PLAN — Chapter-3 injury derivation spec — 2026-07-09 · FABLE seat · auto mode
### Job: DIRECTIVE_injury_spec_fable_v1 (manifest tier 6). READ-ONLY on engine/data — spec only, Opus implements.
### Base main SHA read on entry: d4e8f6dc580eccc9bbb3413d324d64ce26bf6b1b (= tag v2.6, matches pin).
### Feed asserted: acceptance_v1_6.json (loaded, JSON asserted) · CONSTRAINTS v1.6 · DECISIONS v86 ·
### LTI_REGISTER 2026-07-02 (repo copy read INCLUDING header stamps: machinery lookup RESOLVED-ABSENT —
### not re-queued; A3 evaluated PRE-LTI-layer; engine haircuts, never re-diagnoses).
### Time band 2–4 h: confirmed feasible at entry.

## Evidence gathered before writing (all read-only)
1. Store located and verified: `engine/rl_after/rl_model_data.json`, md5 e1b4d8bf == pinned. 2652 players,
   per-season `scoring` rows {year, avg, games}, seasons 2005–2026 (2026 partial, `_has26`). No injury or
   availability field exists in the schema.
2. All 43 register names verified against store keys — zero guesses. Three needed disambiguation:
   Nic Martin → `nicholas-martin` · Josh Kelly → `joshua-kelly` (GWS pick-2 2013) · Maxwell King →
   `max-king-syd` (Sydney pick 49, 2025). NOTE: `max-king-syd` and `max-king-stk` share the identical
   DOB 2007-01-09 — name+DOB is non-discriminating; only the store key separates them (hard evidence for
   the register's owed `key` column).
3. Existing availability logic = `_b2hc` only (rl_model.py:792–803): transient, inference-based (0 games
   in 2026 + established), age-banded (<27→0.088, 27–29→0.039, 30+→0), present-component/Now-board only.
   Season progress = hardcoded SEASON_PROG=0.58 (rl_model.py:583) — no live calendar.
4. Derivation sample for return-from-injury pricing EXISTS in the store: 184 gap-season return cases
   (≥5 games in Y, none in Y+1, played Y+2). Raw return-vs-prior ratio median 0.97; age-banded medians
   ≤22: 1.03 · 23–26: 1.00 · 27–29: 0.87 · 30+: 0.64 — i.e. most of the raw "haircut" IS aging, which is
   exactly the double-count the directive's "net of new aging" rule exists to prevent. Attrition base:
   513 same-shape cases never returned.
5. Register-vs-store anomaly rows catalogued (e.g. toby-conway last store games 2024) — spec will define a
   report-only diagnostic, never an overwrite (register is ground truth).

## Spec structure (one document, committed next)
§1 Scope + inherited facts · §2 Register as versioned input: schema WITH key column (all 43 keys listed,
verified), timing-designation → engine-semantics map, repeat-LTI windows, owner workflow, SSI compliance
options (fold-into-store vs pinned sidecar) — one owner fork · §3 Part 1 CURRENT-SEASON NERF: progress
measure, register fields driving it, Section B nil-production-no-haircut treatment · §4 Part 2
RETURN-FROM-INJURY PRICING derived fresh per study-v2: derivation data, cells, smoothing, net-of-aging
construction · §5 The five symmetric owner forks (i–v per FENCE), each priced on named players, with
recommendation · §6 Acceptance sketch: A3/Rozee (pre-LTI-layer stamp honoured), A-DARCY attribution,
nerf shape test, guard interactions (G-COHORT denominator direction, G-FLOOR, G-PEAK) · §7 Plain-language
section for the owner · §8 The consolidated list of owner rulings requested.

## Remaining steps
- Fold in the mechanism survey (L1c fade-clock, SITOUT_RETAIN/games-ramp, calendar fix, cliff blend,
  KPFFIX, A3 gate text, study-v2 rules) — in flight.
- Write spec → commit → push → candidate PR → ≤30-line return.
