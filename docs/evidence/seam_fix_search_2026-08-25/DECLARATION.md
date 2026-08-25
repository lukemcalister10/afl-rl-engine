# SEAM FIX · BOUNDED SEARCH · construction declared BEFORE computation · 2026-08-25

Mandate: register v848 — the error gets fixed; bounded fresh-eyes search before defaulting to the
validated backup (the hard floor); any solution must lift cameo>=threshold rows AT LEAST to their
never-played selves; closed roads stay closed (point models 0-60, centering 39/40, conditioned
feature alone board-invisible).

## CANDIDATE 1 — THE SMOOTH SEAM RAMP (the "smooth seam blend" of v848(a), corrected in shape)

A logistic MIXTURE centered at the threshold fails the settled requirement: rows just above 45 get
partial lifts and stay below their never-played selves (leake at lambda=0.575 -> 314 < 421). The
requirement forces lambda == 1 AT AND ABOVE the threshold. Therefore the smooth object is a RAMP:

    v_final = v_ev + lambda(c) * max(0, v_cf - v_ev)
    lambda(c) = 0                    for c <= 40
              = 3t^2 - 2t^3, t=(c-40)/5   for 40 < c < 45     (smoothstep, C1 at both knots)
              = 1                    for c >= 45

  - v_cf = the engine's own price for the row with scoring stripped (the counterfactual method,
    validated exact on all 48 live sitters). v_ev = the engine's evidence price.
  - ZERO fitted constants. The two knots are exactly the two thresholds already on the owner's desk
    (40 vs 45, the goad question) — the ramp spans them instead of choosing between them.
  - c > = 45: identical to the hard floor (the six settled rows lift by the full gap, +649).
  - c <= 40: identical to no floor (barnett-class weak-late harshness preserved EXACTLY, not
    asymptotically — the owner's measured principle).
  - 40 < c < 45: graded lift. This is where the ramp differs from both hard floors, and it removes
    the law-3 cliff both of them carry at their threshold (a row whose cameo average drifts across
    the knot moves smoothly, not by a jump).

## PREDICTIONS (declared now, computed next)
P-S1. On the 51-row census: floor45 movers = 6 rows +649 (the register's numbers, reproduced).
P-S2. floor40 movers = 7 rows (+goad ~ +235) ~ +884.
P-S3. ramp movers = the 6 full rows +649, plus goad at lambda(43.5)=smoothstep(0.7)=0.784 ~ +184,
      plus anastasopoulos at lambda(42.2)~0.47 ~ +3; total ~ +836; NO row below c=40 moves.
P-S4. New-inversion check: lifted rows price exactly at (or below) their own never-played selves, so
      no lifted row can overtake the sitter side; within the cameo side, any created cameo-strength
      inversions are counted and reported for ramp AND both floors identically — if the ramp creates
      more than floor45, that is reported as its cost.

## CANDIDATE 2 — LEVEL-VOCABULARY ROOT FIX: cost scoping only (no prototype), after candidate 1.
## BOUND ON THE SEARCH: these two candidates, measured; then the packet recommends ramp / floor /
## root-fix-deferred with the numbers beside each. No further solution-hunting this window.
