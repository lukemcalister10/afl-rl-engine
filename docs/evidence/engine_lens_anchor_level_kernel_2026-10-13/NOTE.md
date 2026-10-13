# The +2 lens anchor (D1) and level-axis smoothing (kA) — engine act, 2026-10-13

Owner word (verbatim, in chat 2026-10-13): "Yeah approved on the ka/level axis" and, after the kA before/after
board and the D1 lens totals were shown, "Yep approved".

## What changed (engine/rl_after/_merged_recover.py)
- D1: `o41_absence_depth`, `o41_completed_absent` and `o31_cu` start their walk at min(Y, _LENS_FORM); their
  in-progress fraction reads use the same anchored year. Pricing 2028 no longer counts 2027 as a completed
  missed season. Present values (Y=2026, _LENS_FORM None) are untouched by construction.
- kA: `_prod_path` prices a live-season row (Y == BASE_REF, not first-evidence) at avg -1.0, -0.5, 0, +0.5, +1.0
  and takes the uniform mean, so a split in the band's level axis becomes a ramp. The -1/-2 columns and
  harness as-of years are not smoothed (blind-review condition).
- Also riding (from Phase 0.4): rl_model.py reads `active()`'s recency from the scoring rows instead of the stale
  `_has26` flag — identical truth on all 2,650 rows (engine/rl_after/ingestion/test_has26_derived.py).

## Measured before landing (control build reproduced the live board 6541dc14 exactly)
- Present: 423 of 804 change, median 1.0%, p90 3.7%, largest -199 (Noah Anderson) / +157 (Connor O'Sullivan);
  total 686,595 -> 687,821 (+0.2%). D1 alone: 0 present changes.
- +1: total 623,605 -> 634,002 from D1 (169 players; Sam Darcy 2,954 -> 5,127 largest).
- +2: total 193,789 -> 592,162; median vP2/vP1 1.00 at ages 19-24 falling to 0.83 at 31 (was 0.23 at every age).
- Sweep (Serong, 24 games): the +217 step at avg -1.5 becomes +59/+58/+59; the +137 at +1.5 becomes +34/+9/+41/+42.
- Combined build on a copy: 769eb79e6a70cd0417519d33de1bc8ff. Lens order-independence (blind-review test): 804/804 rows identical whether the
  +1/+2 prices follow the export loop's 2024/2025/2026 evaluations or are computed on a fresh copy.
- Build time 427 s -> 742 s.

## Blind independent review (law 11)
PASS WITH NOTES. Conditions met in this act: kA scoped to the live season; the parity test above. Notes carried
forward: the never-delivered arm of o31_cu (fade30b_clock) is not anchored — owner ruling owed; 70 thin-evidence
19-21-year-olds now show vP2 > vP1 (the removed phantom charge was masking LEG E's growth credit).
