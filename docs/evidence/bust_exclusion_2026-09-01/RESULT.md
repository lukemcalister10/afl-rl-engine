# RESULT — what setting the live `_pvc_exclude` flag actually does to the board

**Date:** 2026-09-01. Read `PREREG.md` first; it was written before this build was looked at.

## The build

```
baseline (pinned)   c8c2f2b6f99445484fadaa8c44afe609    data/rl_build/rl_app_data.json
candidate           b005096b5e78014425922cae3f28f6c9    802s, canonical mode, rc=0
```

The only difference between them is `BUST_EXCLUDE_KEYS` in `rl_model.py` setting `_pvc_exclude` on
`paddy-mccartin` and `thomas-boyd`. Store, engine head, fv, config, v0surf, the adopted pick curve —
all unmoved.

## What moved

```
active rows        804 -> 804
players moved      622        of which UP: 0        unchanged: 182
sum of values      703,913 -> 689,275               -2.08%
per-player ratio   min 0.8889   median 0.9806   mean 0.9841   max 1.0000
```

Every mover moves DOWN. That much the prereg predicted, and it is the `BOARD_FACTOR` signature: the
v3.4 pre-anchor head `PVC[1]` rises when two pick-1 rows are struck out and the rest slide up, so
`BOARD_FACTOR = (RL_PICK1 / PVC[1]) * s` falls, and `SCALE` with it.

## THE PREDICTION FAILED, and this is why the act is not landing

The prereg said, in as many words:

> "they move **coherently, in one direction, by one ratio** — relativities preserved; no reordering
> of the board … If the observed board instead shows players moving in BOTH directions, or any rank
> change, the prediction is wrong and this act does not land."

It is not one ratio, and there is reordering. Counting only pairs whose values are strictly distinct
on BOTH boards — so no tie-break artefact can be mistaken for a crossing:

```
true order crossings   266
```

```
aaron-cadman   2121 -> 2077   (-2.07%)
josh-daicos    2125 -> 2074   (-2.40%)      Cadman is behind Daicos before and ahead after
```

Two players 4 points apart on a 2,100-point value, moving by different percentages and swapping. So
the flag does not reach the board as a clean rescale; it reaches it through `SCALE` into a valuation
that is not linear in it. Whatever the mechanism, **the change reorders the board**, which is a
repricing with real consequences for a trade, not a cosmetic restatement of the same relativities.

## Disposition

Reverted. `engine/rl_after/rl_model.py` is byte-exact to its pin (`6fe7c415`) and `restamp check`
agrees on all five stamps. Nothing about this measurement is lost: the numbers are here, and
`ui/tests/draftday.test.js` asserts the hole is still open, so the next attempt starts from a failing
test rather than from a rediscovery.

**The owner's word is needed** — not on whether the two men should be excluded (he has given that),
but on whether closing this particular divergence is worth 266 order crossings and a 2% drop in every
value on the board. It buys consistency between the live fit and an adopted curve that already
excluded them; it does not change any pick price, because the pick curve is the frozen artifact.
