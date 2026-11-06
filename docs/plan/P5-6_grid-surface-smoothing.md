# P5-6 — Grid-surface smoothing replaces the level-axis kernel (HIGH; owner word + blind review)

**Goal.** The band (cm / q97m quantile-GBR) is piecewise-constant in level and exposure, so a single game can
step a value (the Ash +3x case). The 2026-10-13 act smoothed the LEVEL axis by pricing each live-season row at
avg −1, −0.5, 0, +0.5, +1 and averaging (kA: five engine prices per row). Replace it with a smooth surface
evaluated once: fit the band's prediction grid over (level, exposure) at load time to a monotone smooth
surface (e.g. a tensor-product P-spline or isotonic-in-level bilinear grid on a fine lattice, fitted ONCE and
pinned as a build input like data/q97m.pkl), read by `_prod_path` instead of the five-point average, with the
games axis smoothed by the same surface (the games-axis ±1 patch becomes unnecessary).

**Why.** kA costs five prices per row per lens (machine time), smooths one axis only, and only Y == BASE_REF.
Owner (2026-10-14): "Quality is important. Is there a better way to do the smoothness that doesn't take the
machine time?" — the grid surface was the answer given.

**Rules.** Measure first: the surface must reproduce kA's board within tolerance on the present board (show
the owner the diff: median, p90, largest), remove the single-game steps on BOTH axes (demonstrate on Ash and
the 70 young players), and price every lens including the as-at boards consistently (kA was BASE_REF-only).
The fitted surface is a pinned artifact with its fit script committed (like data/v0surf.pkl); the engine halts
on a signature mismatch. Blind review.

**Proof.** Measurement build; the step-removal demonstration; blind review; landing gates; the as-at harness
re-run (the as-at boards move too — show them).

**Lands via.** Lever act on the owner's word (RULEBOOK P1, law 11).
