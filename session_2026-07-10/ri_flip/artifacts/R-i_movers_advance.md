# R-i MOVERS — L1c fade-clock ADVANCE (the flipped default) vs the merged head — v1 · 2026-07-10

**Owner ruling R-i (2026-07-10, DECISIONS v90 §36): the L1c fade-clock ADVANCES during injury.** This job
committed that ruling as the code default (`RL_LTI_CLOCK` pause→advance), pinned it in the config manifest
so it rides artifact identity, and added the ruling-config assertion that fails a paused bake loudly. The
table below is the full list of board movers of the regenerated ADVANCE candidate board (gate-mode,
manifest-pinned) vs the merged-head PAUSE board committed at #56 (`99941f1`, board md5 `d9728208`).

Value = board ev(2026). Δ = advance − pause (advancing NEVER raises value). Only the genuinely young,
under-G0 (46-game) injured register names move; every other board key is **byte-identical** (parity PASS).
Deltas reproduce the #56 R-i comparison table to the digit (the audit spot-check: O'Farrell −206, Gibcus −17).

| player | pause | advance | Δ |
|---|---|---|---|
| Harry O'Farrell | 1016 | 810  | **−206** |
| Jonty Faull     | 1238 | 1166 | −72 |
| Matt Carroll    | 961  | 929  | −32 |
| Josh Gibcus     | 294  | 277  | **−17** |
| Josh Sinn       | 350  | 340  | −10 |
| Darcy Jones     | 1487 | 1484 | −3 |
| Noah Long       | 266  | 264  | −2 |
| Toby Pink       | 40   | 39   | −1 |
| Ollie Lord      | 161  | 160  | −1 |

**9 movers, every one a register name.** Non-register movers: 0. Byte-level record diffs off the register: 0.
The named exemplars Darcy (3825), Motlop (151), Flanders (1714) sit **past G0** — no L1c credit either way,
Δ0, ceilings untouched (A-DARCY loci unaffected by the clock; the owner's sight call is a viewing-time item).
The 0-game sit-out names (Barker, Thredgold, King, Hayes, Conway, Archer, McInnes) are V0/floor-anchored so
the 2026 clock does not reach their shipped value → Δ0.

## Board identity
- advance candidate board md5 = `e2c9bc51`  (was pause `d9728208` at the merged head)
- engine_head = `7a07e369` · config = `69ead79b…` · store = `a2fbc9a0` UNCHANGED · register `652d83e8`

## IN PLAIN TERMS
You ruled that an injured kid's "young clock" keeps ticking while he sits. This build makes that the default
and locks it so nobody can quietly bake the paused version. The only players who move are the young injured
ones on your register — they each lose a bit of value for the season they'll miss (O'Farrell most, −206),
exactly the numbers on the table you approved. Everyone else on the board is untouched to the byte.
