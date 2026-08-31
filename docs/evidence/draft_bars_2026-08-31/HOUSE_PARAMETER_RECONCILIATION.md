# Draft day vs the house's already-derived knowledge

**Date:** 2026-08-31 · maintainer note, renders nowhere on a user surface.

## Why this exists

The Draft day tab was built by deriving its own parameters from the outcome store. The owner asked
whether existing derived knowledge had been consulted. It had not. This note records the audit that
followed, parameter by parameter: what the house had already ruled, what was independently chosen,
whether they agreed, and what moved.

## The two sources of prior knowledge

1. `session_2026-07-30/item279/panel/harness_pvc.py` — the pick-value curve harness. It carries the
   declared sampling parameters the v0/PVC ratings were fitted under.
2. `docs/ENGINE_PRIMER.md` §4 ("the oh shit ledger") and §6 — the standing rulings.

## Parameter by parameter

| Parameter | House value | Independently chosen | Agreed? | Action |
|---|---|---|---|---|
| Class floor | `YR_LO = 2004` | none (2003 was in) | **NO** | Adopted 2004. Verified: the store holds **0** 2004 seasons for the 61-man 2003 class, so its year one is unobservable. |
| A real season | `QUAL_GAMES = 6` | `REAL_SEASON_GAMES = 10` | **NO** | Adopted 6, generator re-run. |
| Thin-sample mark | `MIN_STRATUM = 20` | `THIN_MAX = 8` | **NO** | Adopted 20. |
| Pick universe | `ND_LAST = 64` | picks 1–64 | yes | — |
| Column shape | `RANGES = [(1,10),(11,20),(21,30),(31,45),(46,64)]` | point picks ±8 | n/a | **Declined, declared.** Bands are right for fitting a curve; draft day asks "I hold pick 15", and a band answering 11 and 20 identically cannot serve that. Reasoning is in the `BOARD_PICKS` docblock. |
| Replacement bars | `rl_model.py:824 REPL` less `RL_REPL_DROP` (3) | derived from scratch, twice | **NO** | Owner-corrected. Board now reads `REPL_BAR` published by `extract_board_view.py`; the generator holds no bar at all. |
| Star lines | not derived anywhere; `PEAK` is the elite-ramp denominator, not a star line | mistakenly read `PEAK` as elite | **NO** | Owner declared: MID 105, RUCK 105, SD 97, SF 92, KPD 85, KPF 85 → `docs/inputs/OWNER_STAR_SEASONS.json`. |
| Era normalisation | ENGINE_PRIMER §4.10: **none**, SuperCoach assigns a fixed 3,300 points a match, so averages are comparable by construction | caveated "2003–2016 football is different" | **NO** | Caveat withdrawn from the code comments. It was wrong. |
| Bust exclusion | §4: McCartin / Boyd force-majeure exclusion is ruled but **not applied in the store** | not applied | yes (by accident) | Left as-is; put to the owner. Measured cost at KPF pick 1: VOR 15.6 with them vs 17.0 without, star 36% vs 40%. |
| Never-established | `never_established(r)` = no season ≥ 6 games | own bust definition = no measurable season | same rule once QUAL_GAMES adopted | converged |

## What was NOT in the house's knowledge, and had to be derived

- **The peak threshold (11 seasons).** The bundle's `maturitySeasons = 4` is a DEBUT threshold — 99%
  of eventual debutants have debuted by four seasons. It was being reused to gate peak questions.
  Only 31% of first-star seasons have arrived by four. Measured cost of the misuse: star rate 15.3%
  against 17.0%, understated ~3× worse at picks 41–64 than at picks 1–10, and it flipped the
  MID/RUCK headline. The 11-season line (93% of first-star seasons landed) is derived in
  `draftday.js` rather than the generator, because it needs the star lines and the generator holds
  no bars.
- **The midfield yardstick.** No prior expression of a cross-position pick equivalence existed.

## Measured impact of the reconciliation

Whole national-draft population, classes with a full run:

| | before | after |
|---|---|---|
| bust % | 32.4% | 23.7% |
| VOR | 9.29 | 9.58 |
| clear % | 46.3% | 48.8% |
| population | 901 (classes 2003+, ≥10) | 840 (classes 2004–2015, ≥11) |

Most of the bust move is `QUAL_GAMES` 10 → 6: a man with a 7-game season was being counted as
never having produced a measurable one.

## Pinned

`ui/tests/draftday.test.js` §9 reads `harness_pvc.py` at test time and asserts the app and the
generator still carry the house's values. If the harness moves, the test fails rather than the
board silently drifting.
