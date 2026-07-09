# R-i COMPARISON TABLE — L1c fade-clock PAUSE vs ADVANCE for injured young register names — v1 · 2026-07-09
### PROVISIONAL (R-i, DECISIONS §33). Fork-i: does an injured youngster's L1c young-credit clock PAUSE while
### he is out (status quo — the clock keys on career GAMES, so an injured season adds ~0 and it implicitly
### pauses) or ADVANCE by his expected (lost) games (fading the credit as if he had played)? RECOMMENDATION
### = (a) PAUSE (default). Clean toggle `RL_LTI_CLOCK=pause|advance` — an owner flip is this config change,
### NOT a rebuild. **The owner confirms or flips R-i on THIS table BEFORE any bake.** Regenerate:
### `session_2026-07-09/injury_build/run_ri_table.sh`. Engine head tracks the candidate; store a2fbc9a0.

Value = board ev(2026). Δ = advance − pause (advancing NEVER raises value). Only the genuinely young,
under-G0 (46-game) register names move; the named exemplars Darcy/Motlop/Flanders sit past G0 (no L1c
credit either way), so R-i does not touch them — Gibcus is the one named exemplar the clock still bites.

| player | sec | pause | advance | Δ | yc pause | yc adv | g pause→adv | driver |
|---|---|---|---|---|---|---|---|---|
| Harry O'Farrell | A | 1016 | 810 | -206 | 1.343 | 1.069 | 6→28 | young L1c credit fades 1.343→1.069 as the clock advances g 6→28 (≈22 expected games added) |
| Jonty Faull | B | 1238 | 1166 | -72 | 1.073 | 1.012 | 26→38 | young L1c credit fades 1.073→1.012 as the clock advances g 26→38 (≈12 expected games added) |
| Matt Carroll | A | 961 | 929 | -32 | 1.040 | 1.005 | 27→39 | young L1c credit fades 1.040→1.005 as the clock advances g 27→39 (≈12 expected games added) |
| Josh Gibcus | A | 294 | 277 | -17 | 1.063 | 1.001 | 22→43 | young L1c credit fades 1.063→1.001 as the clock advances g 22→43 (≈21 expected games added) |
| Josh Sinn | A | 350 | 340 | -10 | 1.030 | 1.000 | 30→52 | young L1c credit fades 1.030→1.000 as the clock advances g 30→52 (≈22 expected games added) |
| Darcy Jones | A | 1487 | 1484 | -3 | 1.002 | 1.000 | 37→59 | young L1c credit fades 1.002→1.000 as the clock advances g 37→59 (≈22 expected games added) |
| Noah Long | A | 266 | 264 | -2 | 1.005 | 1.000 | 36→58 | young L1c credit fades 1.005→1.000 as the clock advances g 36→58 (≈22 expected games added) |
| Ollie Lord | A | 161 | 160 | -1 | 1.008 | 1.000 | 35→56 | young L1c credit fades 1.008→1.000 as the clock advances g 35→56 (≈21 expected games added) |
| Toby Pink | B | 40 | 39 | -1 | 1.005 | 1.000 | 37→54 | young L1c credit fades 1.005→1.000 as the clock advances g 37→54 (≈17 expected games added) |
| Harley Barker | B | 710 | 710 | +0 | 1.196 | 1.077 | 0→22 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Blake Thredgold | A | 538 | 538 | +0 | 1.186 | 1.090 | 0→22 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Maxwell King | A | 255 | 255 | +0 | 1.095 | 1.034 | 0→22 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Lewis Hayes | A | 358 | 358 | +0 | 1.205 | 1.080 | 1→23 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Sam Darcy | A | 3825 | 3825 | +0 | 1.000 | 1.000 | 51→67 | past G0=46 — no L1c credit either way (value driven by KPF/production, not the young clock) |
| Toby Conway | A | 473 | 473 | +0 | 1.148 | 1.030 | 6→28 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Jesse Motlop | A | 151 | 151 | +0 | 1.000 | 1.000 | 63→85 | past G0=46 — no L1c credit either way (value driven by KPF/production, not the young clock) |
| Jackson Archer | A | 80 | 80 | +0 | 1.019 | 1.000 | 26→48 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Reef McInnes | A | 76 | 76 | +0 | 1.079 | 1.000 | 23→45 | 0-games sit-out name — value is V0/floor-anchored (draft-year credit); the 2026 clock doesn't reach the shipped value |
| Sam Flanders | A | 1714 | 1714 | +0 | 1.000 | 1.000 | 101→111 | past G0=46 — no L1c credit either way (value driven by KPF/production, not the young clock) |

## Reading / recommendation
- **(a) PAUSE — RECOMMENDED (default).** The games-clock already pauses implicitly; a returning youngster keeps his young-credit runway intact (forfeited-growth-year hypothesis — his lost year costs him Part 1's nerf, not his ceiling). Zero new constant.
- **(b) ADVANCE** fades the credit with NO new evidence against the player — it violates the evidence-quantity rationale the owner accepted for L1c, and it moves the young, low-games names DOWN (O'Farrell −206, Faull −72, Carroll −32, Gibcus −17…) purely for being injured. A-DARCY: Darcy himself is past G0 (Δ0) so his ceiling is untouched either way, but for the general young cohort advance clips the runway through the availability locus.
- **(c) pause + calendar cap** = identical to (a) for every current register name (none is near a sane cap); a dormant guard to derive only if a perpetual-youth case appears.

## IN PLAIN TERMS
Injured kids: leave their 'young clock' paused while they're out (recommended) and their comeback keeps full runway — or advance it and they quietly lose value for a year they never played. Only the genuinely young, low-games names move; Darcy/Motlop/Flanders are already past the young-credit line, so this choice barely touches your headline names (Gibcus aside). Your call before any bake.
