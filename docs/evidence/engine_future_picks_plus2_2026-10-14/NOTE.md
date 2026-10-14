# The +2 board carries the 2027 class as picks — engine act, 2026-10-14

Owner word (verbatim, in chat): 2026-10-13 "For the future boards... phantom draft picks (ie 2027 pick 1 onward
for +1 year and then for the +2 2027 and 2028 pick 1 onwards)"; 2026-10-14, to the item "+2 board carries 2027
picks": "2. Yes, please do."

## What changed (engine/rl_after/rl_export.py, `lensPicks` / `draftAssetTotals`)
Each lens carries every draft class not yet on the board. The +1 view is unchanged (2027 picks 1-64). The +2
view carried only the 2028 class; it now carries the 2027 class too (ids `draft-pick:2027:<n>:lens2`, so they
never collide with the +1 ids). `draftAssetTotals['+2']` gains `classes: [2027, 2028]` and `nVisiblePicks` 128.
`_merged_recover.py` and `rl_model.py` are untouched: no player value moves on any lens.

## Measured before landing (build on the current tree, store 68bd9396 / engine_head 0fe52264)
| lens | players | picks | total | n picks |
|---|---|---|---|---|
| now | 687,821 | 0 | 687,821 | 0 |
| +1 | 635,134 | 47,198 | 682,332 | 64 |
| +2 | 593,206 | 94,396 | 687,602 | 128 |

Spread of the lens total against the present board: +1 -0.8%, +2 -0.03% (was -6.9% before this act).
Player values changed: 0 (every v / vP1 / vP2 identical to the live board 769eb79e). Predicted board e22e3ef6.
