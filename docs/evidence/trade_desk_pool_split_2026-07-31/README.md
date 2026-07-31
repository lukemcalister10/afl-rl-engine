# Trade desk — the ruled pricing split (#292). Evidence, 2026-07-31.

What this proves: the trade desk now prices picks the way RULEBOOK v2.1 law 4 rules them, and the way
`ui/tools/ingest_inputs.py:378` `price_pick()` already priced them on the ingest side. Ordinals 1–64 come
off the national curve; everything past 64 is THE POOL at one position-blind level, read from the pvc
bundle's index-65 value. There is no ordinal pick 65, and no price for pick 70.

Everything below was produced by driving the real app in Chromium from `file://`, not by reading source.
Base: `5ed38d3` (register v549). Changed file: `ui/app/trade.js` only.

## The bundle, read from the live page

65 keys of 65, indices 1–65. Tail: 64 → 571, **65 → 299**. The 571 → 299 step is the pool level, not a
curve point. No figure in this fix is hard-coded — `grep -n 299 ui/app/trade.js` returns nothing.

## Before → after, same query, same bundle

| query | BEFORE | AFTER |
|---|---|---|
| `70` | `Pick 70` priced **0** | `Pool pick — position-blind level` priced **299** |
| `65` | `Pick 65` priced **299** (the pool wearing an ordinal label) | `Pool pick — position-blind level` priced **299** |
| `7` | `Pick 7` 1,907 + `Pick 70…74` **all 0** | `Pick 7` 1,907 + the one pool item at 299 |
| `pool` | no match | the pool item |
| verdict line, seeded trade | "about **a mid fourth-round pick (≈ pick 65)**" | "about **a pool pick**" |

The verdict line is the strongest single row: the phantom ordinal was rendering on the desk **as it
opens**, on the seeded trade, with no user input at all.

Screenshots: `screenshots/before_query_*.png` vs `screenshots/after_query_*.png`; full desks at
`before_desk.png` / `after_desk.png`. Machine-readable in `reports/before.json` / `reports/after.json`.

## The basket path

Selecting the pool item stores `{t: "pick", pool: true}` — measured keys exactly `["t","pool"]`, and
`hasOwnProperty("n") === false`, so **no ordinal exists on the item for anything downstream to read**.
The row chip reads `POOL PICK · 2026 ND · position-blind level · 299`; the side total moves 4,361 → 4,660,
exactly +299. Screenshot `screenshots/after_pool_in_basket.png`.

## Non-vacuity, both directions

1. **The price follows the artifact.** A scratch copy with the bundle's index-65 value changed 299 → 777,
   and nothing else, moves every pool reading to 777 — picker, basket, descriptor. No code change.
   `reports/nonvac.json`, `screenshots/nonvac_query_70.png`.
2. **No pool value published → no invented price.** A scratch copy with index 65 removed (64 keys) offers
   **no pool item at all**; queries `65`, `70`, `pool` return empty rather than pricing a phantom. This is
   the UI's form of `price_pick()`'s HALT. `reports/nopool.json`.
3. **The instrument can fail** — it reported the defect in full on the pristine BEFORE tree.

## Regression

`ui/tests/ui_222_items.test.mjs` **74/74**. `ui/tests/responsive_layout.test.mjs` **72/72**
(12/12 at each of 320 · 360 · 390 · 430 · 720 · 1440px). Zero page errors in every run above.

## Reproducing

```
node docs/evidence/trade_desk_pool_split_2026-07-31/harness/pool_split_proof.mjs   # RL_REPO=<tree> TAG=<t> SHOTS=<dir>
node docs/evidence/trade_desk_pool_split_2026-07-31/harness/pool_in_basket.mjs     # RL_REPO=<tree> SHOTS=<dir>
```

## Not in this change

The five rendered SCAR labels — they relabel at #290's L8 with the γ adoption. The board's pick-asset
(`ui/app/board.js:621`, ring-fenced by `MD.isPickAsset`) is a disjoint representation: no `t` field, never
enters a trade basket, untouched here.
