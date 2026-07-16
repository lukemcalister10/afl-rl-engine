# LEG B — s-DIAL MEASUREMENT: HALT-AND-ASK (empty grid) · 2026-07-16

**Status: HALT-AND-ASK per PLAN §7 / acceptance `leg_b.s_dial_selection` ("If NO grid value
clears ⇒ HALT-AND-ASK with the measured table; do not extend the grid") and the directive
("any design ambiguity mid-build is a HALT-AND-ASK to the supervisor").**

The engine implementation of the amended PLAN is COMPLETE and byte-safe. The frozen-suite β
measurement then shows the specified map **compresses** (lowers β) instead of un-compressing it,
at every grid point. No `s` clears the `β ≥ 0.85` gate. This is a design-level finding surfaced
at exactly the checkpoint the frozen suite exists to catch.

## What was built (all committed; A/B identity PROVEN)
- `posval_uncomp()` wired at **all six** posval sites (site 7 `_nv_bwd` NOT-wired), captain
  preserved additively (δ byte-identical), ρ pre-captain, κ=1, Δ=6.0 onset ramp.
- E = saturating evidence weight `1−exp(−Eq/τ)`, τ=1.1 (memo §2 algebra: w∈[0,s]).
- Load-time L_ref[pos] = median `level_now` over the demonstrated-proven pop; V_ref =
  posval(L_ref−REPL); production-side per-position conservation renorm C[pos].
- Kill-switch `RL_UNCOMP` (default ON, declared exception — config unmoved).
- Hygiene rider: dead `_coreM1 if not _EVW:` branch deleted with obituary.

**Kill-switch A/B identity (dev-shell board md5):**
`RL_UNCOMP=0` → **8d90c9ac** byte-exact · map-inert default → **8d90c9ac** · `RL_UNCOMP_S=0.55` → 51df83d7 (moves).
Hygiene deletion byte-safe: inert board still 8d90c9ac.

## The frozen estimator (declared before build, identical at every grid point)
β = OLS slope of ln(price) on ln(realised-output) [`np.polyfit`], 1000-sample bootstrap-percentile
CI (seed 0), verbatim from `session_2026-07-15/book_calibration/calibrate.py:40`. Sample =
proven-27+ contributors (age≥27, o>0, p>0; the item-131 low-runway regime). o = recent-2 realised
season avg − REPL[pos]. p = engine current price ev(p) (numéraire-invariant for β). n=116.

## THE MEASURED TABLE (map OFF = β_c ≡ s→0; RL_UNCOMP_S per grid point)
| s        | β point | CI (2.5–97.5) | width | n | β≥0.85 |
|----------|---------|---------------|-------|---|--------|
| OFF (β_c)| 0.6219  | 0.4836–0.7899 | 0.306 | 116 | ✗ |
| 0.45     | 0.5140  | 0.3843–0.6704 | 0.286 | 116 | ✗ |
| 0.50     | 0.5031  | 0.3741–0.6607 | 0.287 | 116 | ✗ |
| 0.55     | 0.4923  | 0.3634–0.6483 | 0.285 | 116 | ✗ |
| 0.60     | 0.4817  | 0.3522–0.6388 | 0.287 | 116 | ✗ |

β falls **monotonically** in s. **No grid value clears β ≥ 0.85.** (β_c=0.62 already matches the
memo's declared β_c≈0.683; the map only lowers it.)

## Diagnosis — why the posval-level blend compresses
The memo's algebra `β_eff = (1−w)·β_c + w` (→ β up toward 1) holds when the blend is applied in a
space whose local price-vs-output elasticity is β_c < 1. The PLAN wires the blend at the **posval
production** level: v0 = posval(lev−REPL), target t = V_ref·ρ with ρ = lev/L_ref and V_ref =
posval(L_ref−REPL). But:
- **posval production is NOT the compressed quantity.** d ln(posval(lev−REPL)) / d ln(lev) is ≥ 1
  for elite players (the REPL offset makes it super-linear), so the local elasticity being blended
  is already ≥ 1 — blending toward the β=1 target `t` pulls it **down**, not up.
- **V_ref = posval(L_ref−REPL) is tiny** (0.7–8.9 across positions; for KEY_FWD/GEN_FWD the
  median proven level sits at/below REPL), so t = V_ref·ρ stays small while v0 spans 0…40. For
  above-median players t ≪ v0 → the blend collapses elite production toward the reference; the
  conservation renorm then scales the whole position back up (C≈1.3–1.9). Net: the price–output
  spread **narrows** → β falls.
- The board-level compression the memo targets (β_c≈0.68) is introduced by the layers **around**
  posval (runway discount, forward-horizon band integration, pick priors, iso), not by posval
  itself — so a posval-level blend cannot raise the board β and empirically lowers it.

This is not an implementation defect: the six sites, ρ/E/V_ref, conservation, kill-switch and A/B
identity are all correct to spec; the measured OFF board is byte-exact 8d90c9ac. It is a mismatch
between the memo's abstract β_eff algebra (blend the board price) and the PLAN's concrete wiring
(blend the posval production). Resolving it is a **design ruling**, not an in-build decision.

## State left (safe HALT)
`UNCOMP_S_DEFAULT = None` → the map ships **INERT** (board byte-exact 8d90c9ac). All machinery,
the kill-switch A/B identity, and the hygiene rider are committed. Nothing that would degrade the
board is shipped. The map turns on only when a strength dial is set — which awaits a corrected
functional-form ruling. The s-grid harness (`beta_measure.py`, `grid_verify.sh`) reproduces the
table above in ~7 min.
