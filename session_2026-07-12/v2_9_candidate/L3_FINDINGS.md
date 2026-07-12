# L3 — AGE(A) s(age) adoption + the G-COHORT gate · 2026-07-12

## L3a — s(age) wiring, executed + verified (read-only sim)
Adopts the l7hinr up-side breakout-persistence slope (option A): replaces the flat `S_M1=0.46` in
`_coreM1`'s proven-riser up-branch (`_merged_recover.py:225`) with `clip(s_age(age),0,1)` — the
`s_clip` table (age 20:0.915 · 22:0.789 · 25:0.490 · 27:0.266 · 29:0.027 · 30+:0.0), crossing 0.46
at ~25.3. Patched in the source string (`scripts/l3_age_sim.py`); the permanent `RL_AGE` lever
(default 0) rides the refit. To ship in the candidate it needs the cohort gate (below) + it is
GATED per the ruling.

**Reproduces the l7hinr research to the number:**
| metric | l7hinr research | this sim |
|---|---|---|
| movers | 43/46 risers, 20 up / 23 dn | **43 (20 up / 23 dn)** |
| net delta | +1675 | **+1670** |
| top risers | wilmot +460 · callaghan +367 · bowey +315 · berry +214 · macdonald +199 | **+460 · +366 · +314 · +214 · +198** |
| **Butters (G-PEAK margin)** | −1.0% | **6060 → 5997 (−1.04%)** |

**Butters holds:** −1.04% is inside the G-PEAK ≤2% drop tolerance (~0.96pp slack) — the narrowest
guard margin, watched per the directive. Anchors bont/gawn/darcy byte-identical (they don't fire the
up-branch). Old-name drops as researched (xerri −160). max-holmes +2.95% (young riser).

## L3b — the walk-forward G-COHORT re-measure (the GATE)
[in progress / see G_COHORT section below]
