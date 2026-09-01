# PREREG — landing the bust exclusion into the live pick-value fit

**Date:** 2026-09-01. Written before the landing build.

## The word

> "McCartin and Boyd should be excluded from everything. It's as if they weren't picked."
> — owner, 2026-09-01

and, on being shown the cost and my recommendation against:

> "If it works, it works though. So surely we just recalculate the old number by removing McCartin and
> Boyd, and everyone adjusts accordingly. That seems reasonable to me?"
> — owner, 2026-09-01

Standing authority: ENGINE_PRIMER §4.5.

## What changes

`engine/rl_after/rl_model.py` declares `BUST_EXCLUDE_KEYS` and sets `_pvc_exclude` on the two `hist`
rows, so the same-draft slide-up machinery that has read that flag for months finally has something to
read. A HALT fires if the cohort does not carry exactly the declared names.

Nothing else. The store is untouched. The adopted pick curve is untouched (it already excluded them).
The v0 lens basis is untouched (it already excluded them). `v0surf.pkl` is untouched.

## What it reaches, and it is not the pick prices

`build_pvc_v34()` no longer ships as the curve. What survives is its HEAD, which sets

```
BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s          rl_model.py:1556
SCALE        = SCALE * BOARD_FACTOR
```

`PVC[1]` is the only object in the engine that states what a pick is worth **in player money**, so it
is the exchange rate between the two sides of the board. Measured:

```
PVC[1]         3784  ->  3877     (+2.458%)   two pick-1 busts out, 197 cohort rows slid
BOARD_FACTOR  0.745316 -> 0.727437 (-2.399%)
```

## The prediction

Board `c8c2f2b6f99445484fadaa8c44afe609` → **`b005096b5e78014425922cae3f28f6c9`**, already built once
under exactly this change (`candidate_build_meta.json`, 802s, canonical, rc=0). The landing build must
reproduce that md5 or the lander refuses.

**Every mover moves DOWN, and the size of the move rises with career games.** That gradient is the
act's own definition, not a defect: a player priced on his own football takes the full move, a player
with no football is priced off his draft pedigree — which reads the ADOPTED curve — and does not move
at all. Measured on the candidate:

```
career games     0        1-10     10-30    30-80    80-200   200+
median move    0.00%    -1.19%   -1.74%   -2.15%   -2.30%   -2.32%
```

622 of 804 players move, none up, sum −2.08%. 266 true order crossings, **83% of which involve a player
with under ten games** — a kid holding his pedigree value while a proven player beside him takes the
correction. If the observed board shows any player moving UP, or the games gradient is absent, the
prediction is wrong and the act does not land.

**No pick price moves.** The shipped ladder is `pvc_curve_v2.json`, which this change does not touch.

## Identities

- `moves`: board
- `unmoved`: store, engine_head, fv, config, register, as_of_round, and **rl_model** — flip-scoped, it
  moves at the flip commit ahead of the transaction and is byte-stable inside it.
