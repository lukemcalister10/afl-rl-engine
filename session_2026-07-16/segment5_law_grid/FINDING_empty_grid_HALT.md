# LEG B SEGMENT-5 — THE GRID IS EMPTY at the owner's bar β ≥ 0.80 → HALT (sanctioned)

**Outcome:** No grid point in {0.55, 0.60, 0.65, 0.70} lifts the proven-27+ β to the OWNER-SET bar 0.80.
Per the directive ("EMPTY ⇒ HALT with the table (never extend, never re-tune)") and memo v1.3 ("the GRID
ITSELF is now the arbiter — empty ⇒ HALT with the table, the owner accepted that risk with open eyes"),
this is a **sanctioned HALT**. No s selected; `UNCOMP_S_DEFAULT` stays `None` (map inert); board stays
`8d90c9ac`. The grid is NOT extended and NOTHING is re-tuned.

## THE GRID (frozen fit_beta; d=0.25; owner bar β ≥ 0.80; smallest-clearing rule)

| point       | β (point) | CI (1000-boot, seed 0) | width | n   | ≥ 0.80 |
|-------------|-----------|------------------------|-------|-----|--------|
| β_c (OFF)   | 0.6219    | [0.4836, 0.7899]       | 0.306 | 116 | no     |
| s = 0.55    | 0.6665    | [0.5275, 0.8257]       | 0.298 | 116 | no     |
| s = 0.60    | 0.6706    | [0.5315, 0.8297]       | 0.298 | 116 | no     |
| s = 0.65    | 0.6747    | [0.5354, 0.8342]       | 0.299 | 116 | no     |
| s = 0.70    | 0.6788    | [0.5402, 0.8403]       | 0.300 | 116 | no     |

Frozen estimator: OLS slope of ln(ev) on ln(recent-2 realised avg − REPL[pos]) over proven-27+
(age ≥ 27, o > 0, p > 0, pos ∈ REPL); 1000-sample bootstrap percentile CI, np.random.default_rng(0)
fresh per process. Verbatim `beta_measure.py` (md5 14c59139), one process per point. A/B verified this
run: `RL_UNCOMP=0` board == `8d90c9ac` BYTE-EXACT.

## WHY the grid is empty (measured, not projected)
- β_c = 0.6219 matches the memo §1 base (~0.622).
- The map lifts β by only +0.045 (s=0.55) rising to +0.057 (s=0.70): a nearly-flat slope of ~0.0008 per
  0.01 of s. Extrapolated, β would not reach 0.80 until s ≈ 4+ — far outside any sane strength.
- Cause: the realised evidence weight is **w = s·E·ramp**, not s. Across the proven-27+ sample the
  average effective w at s=0.55 is only ≈ (0.6665−0.6219)/(λ_ρ−β_c) ≈ 0.045/0.30 ≈ **0.15** — E
  (evidence saturation) and the onset ramp knock w down to ~1/4 of s, and the games×recency ρ-ratios
  cluster near the positional median (t = V_ref·ρ ≈ V_ref) so most proven players barely move. The
  memo's β_eff = (1−w)β_c + w·λ_ρ was the SATURATED-w elasticity (w=1 ⇒ β_eff = λ_ρ ≈ 0.92 at d=0.25);
  the realised population β never approaches that because real players carry w ≪ 1.
- This is consistent with the seg-4 kernel-family finding (item 245: "β_eff ≈ 0.75", never a realised
  population number) and item 247 (the 0.83 ceiling is the SATURATED law at the fast fade; the realised
  proven-population β sits well below it).

## Secondary (non-deciding) note
The proven-27+ frozen sample is **n = 116 < the acceptance `min_effective_n` = 120** — a fixed property
of the store's population, identical at every s. Even had a point cleared on the estimate, the β
precision gate could not pass on n as written. The grid is empty on the point estimate regardless.

## What is committed / unchanged
- Kept (all inert-safe, board `8d90c9ac`): the flip (UNCOMP_DECAY 0.25), the load-order fix, the two
  self-tests, the preflight. `UNCOMP_S_DEFAULT` = `None` (UNCHANGED — no s selected).
- Store `b1fd0bce` + config UNMOVED. No board/book/gate regeneration (there is no chosen s to regenerate at).

## The decision returns to the owner
The empty grid is the ruled outcome; the next move is the owner's (accept no-uplift at his law/bar; or
re-rule the bar/fade/grid via a new directive). This seat does not extend or re-tune (fence + memo v1.3).
