# The retro control failed because the TRUNCATED STORES predated Finals Week 1

**Date:** 2026-09-01 · maintainer note. Corrects the diagnosis filed in commit `1327ceb`.

## The owner got it from four names

Shown the control's sample diffs, he said:

> "It seems like a coincidence that the four players cited are players from the four teams who
> played fw1 recently, and Freijah and Dean especially had very good games that week so likely rose
> in value a lot. So I think you've just forgotten to update with the fw1 scores."

He was right. Measured:

```
the 87 control diffs, by club        share of each squad
  Carlton           23                 23 of 49   47%
  Melbourne         22                 22 of 46   48%
  Collingwood       22                 22 of 47   47%
  Western Bulldogs  20                 20 of 43   47%
```

Four clubs, nobody else, and about half of each list — which is the twenty-two who played. That is
Finals Week 1: two matches, four teams.

## The mechanism

`pass_retro_series.py` does not truncate the store itself. It swaps in a PRE-COMPUTED truncated
store per round, emitted separately by `retro_walkforward.py emit-stores`. Those files were written

```
r24 truncated store written: 2026-08-29 02:29
```

before FW1 landed. So every round was priced against a store that did not know FW1 had happened:

```
harry-dean          live 2026: 20 games 61.49 avg    r24-truncated: 19 games 59.52
joel-freijah        live 24 / 79.02                  truncated 23 / 77.59
marcus-bontempelli  live 23 / 117.90                 truncated 22 / 117.17
nick-daicos         live 23 / 119.76                 truncated 22 / 119.48
```

One game short each — their FW1 game. R24's truncation is the CONTROL precisely because it is meant
to be a no-op; it was instead quietly removing a round of football the live board had since gained.
Dean and Freijah move most because their FW1 games were good ones and lifted their averages.

## The fix

`retro_walkforward.py emit-stores`, re-run against the current store:

```
r24  store 8303e0ce  truncated 0    cal 1.00 pace 0.909
```

`truncated 0` — a genuine no-op again, so the control's premise holds. All eleven rounds then
re-priced on one engine load.

## What this corrects, and what still stands

**CORRECTED.** Commit `1327ceb` filed two wrong causes. The first — state carried between rounds —
was tested and cleared (R24 priced FIRST on a clean load gave the same 87). The second — a
pre-existing divergence between the harness's in-process `ev()` and the export path — was a guess
made instead of asking what the 87 rows had in common. There is no such divergence in evidence.

**STILL STANDS.** The series does go stale on a board move and nothing notices: the control is run
only at emission time, `RETRO_ONELOAD_VERDICT.json` records the state of the day it was written, and
MAINTAINER.md's "re-run that control before trusting any re-emission" has no runner. The cause is
stale TRUNCATED STORES rather than stale prices, and the remedy is that `emit-stores` must re-run
whenever football is applied — not only the pricing.

**AMENDED — the override finding was half right.** `pass_retro_series.py` did read the owner display
overrides with `row.get('key')` while `data/owner_overrides.json` writes them under `player_key`, so it
reported "0 overrides" with one on file and applied nothing. But the remedy is NOT to fix the key name.

The override IS applied on the live board. The export writes it as an `ov` block beside the engine
value and never touches `v`, exactly as the file itself declares — *"Applied LAST at the
export/display layer … NEVER touches the engine value `v`"*:

```
will-brodie   v 117   ov {factor: 0.5, dispv: 58, mark: "OWNER OVERRIDE ×0.50"}
```

and `ui/app/seam.js:113` substitutes `ov.dispv` wherever the board shows his value, ordering included.
So the owner sees 58 everywhere.

A WORKING multiplication in the harness would therefore CONTRADICT THIS PASS'S OWN CONTROL: `live_v`
reads `r['v']`, the pre-override 117, so banking 58 would red the control by one row forever. The
block is not a bug to repair, it is a second application site for something the display layer already
owns — the duplicated-assertion class. It has been DELETED, with the reasoning in place, and banking
the pre-override value is what keeps the retro points consistent with every other surface.

The one thing still owed on this: retro points are read through the movers bundle's own `byPoint`
values, so they need to reach `seam.js`'s accessor like every other value does, or Brodie will show
117 on a retro point and 58 everywhere else. That is a UI wiring question, not a pricing one.
