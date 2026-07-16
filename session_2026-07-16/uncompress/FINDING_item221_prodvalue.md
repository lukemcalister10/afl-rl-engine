# LEG B — item-221 DIAGNOSTIC (production-value-level blend): FINDINGS · HALT AGAIN · 2026-07-16

**Supervisor ruling item 221 (Option 2, narrowly scoped): ONE diagnostic round, FINDINGS ONLY.** Apply the
un-compress blend at the FINAL PRODUCTION-VALUE level and measure β with the frozen estimator. RL_UNCOMP
stays INERT; nothing selected; commit the table, HALT again.

## Construction measured (as ruled, findings-only)
`v' = v^(1−w)·(V_ref_b·ρ)^w` per player, hooked behind a SEPARATE flag `RL_UNCOMP_L2_S` (RL_UNCOMP inert;
inert board md5 = **8d90c9ac** unchanged, verified):
- **v = pr = price6(p)** — the production-side board value BEFORE the pole-recovery term in `raw_ev`. NOTE:
  the board renders `ev()` (=raw_ev×iso), not `value()`, so the ev-path analogue of the ruling's
  "prod_full, pre-max-with-pedestal" is `pr`; `value()`≠`ev()` (Daicos value()=7077 vs ev()=8567).
- **ρ = level_now/L_ref[pos]** (smoothed-level ratio, pre-captain, unchanged per §2.1).
- **V_ref_b[pos] = MEDIAN price6 over the demonstrated-proven pop** (built load-time; value-scale 190–628,
  vs the posval V_ref 0.7–8.9 — the value-space analogue as ruled).
- **w = s·E per player**, E = 1−exp(−Eq/1.1) (current evidence; no per-leg split at this level).
- **CAPTAIN CAVEAT (flagged per the ruling, NOT reworked):** `pr` carries the captain via the posval sites,
  so this blends captain-inclusive production.

## RESULT — β STILL FALLS (frozen estimator, proven-27+, n=116)
| s        | β point | CI (2.5–97.5) | width |
|----------|---------|---------------|-------|
| OFF (β_c)| 0.6219  | 0.484–0.790   | 0.306 |
| 0.45     | 0.4891  | 0.396–0.606   | 0.210 |
| 0.50     | 0.4718  | 0.379–0.573   | 0.194 |
| 0.55     | 0.4548  | 0.361–0.555   | 0.194 |
| 0.60     | 0.4374  | 0.343–0.535   | 0.191 |

The production-value-level blend **also compresses** (β falls monotonically), slightly harder than the
posval-level wiring (0.44 vs 0.48 at s=0.60). **No s clears β ≥ 0.85.**

## ROOT CAUSE — it is the ρ AXIS, not the attachment point (elasticities vs realised output o, same sample)
| axis (price) | β vs o |
|---|---|
| `ev`   (= β_c)            | **0.6219** |
| `price6` (production side)| **0.6107** |
| `level_now` (the ρ axis) | **0.1236** |

`level_now` — the smoothed-level ratio the target rides — has an output-elasticity of only **0.12**: for
proven-27+ players the robust multi-season level is nearly FLAT in realised output. So the un-compress
target `t = V_ref_b·ρ` is itself almost output-insensitive, and the blend drives β from β_c=0.62 **toward
λ=0.12**, not toward 1:  β(s) ≈ (1−w)·β_c + w·λ  (matches the grid). `price6`'s own elasticity (0.61 ≈ β_c)
confirms the compression does NOT live in the pole/pedestal layers around production — moving the hook from
posval to production-value changes nothing, because both blend toward the same smoothed-level target.

**Implication for the v1.1 memo (your ruling reserves the redesign):** the lever that can raise β is the
**ρ axis** — the target must track REALISED OUTPUT (elasticity → 1), not the smoothed level (§2.1's
injured-season-robust choice caps the achievable β at λ ≈ 0.12). Neither attachment point (posval,
production-value) nor the s dial can overcome an output-flat target. A partial-output or output-tracking-but-
robust ρ is the design fork; that is a supervisor design decision, not an in-build one.

## Budget note
July-8 y4/y5/y6 at s=0.55 was DEFERRED (matrix rebuild ~5 min): with β compressing, s=0.55 is not a
candidate setting, so its G-COHORT is not decision-relevant this round. Available on request for v1.1.

## State (unchanged, safe)
RL_UNCOMP INERT (UNCOMP_S_DEFAULT=None → board 8d90c9ac). The item-221 diagnostic lever `RL_UNCOMP_L2_S`
is likewise inert by default (no default board effect). Harness: `beta_L2_allgrid.py` (grid in one load),
`beta_axes.py` (the elasticity decomposition). HALT again per the ruling — awaiting the v1.1 memo + directive.
