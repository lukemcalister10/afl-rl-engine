# The listing fact — store-edit act, 2026-10-14

Owner word (in chat, 2026-10-14): the AFL "Retirements and delistings" pages for 2025 and 2024 are the lists;
"obviously ignore anyone who is trd or fa"; a player who re-appears later voids the exit; "Tarryn Thomas was
cut at the end of 2023".

## What changed
`_last_listed` (the last season a player was on an AFL list) is ADDED to 201 retired rows, via the store-edit
lane's new `add` verb (byte-surgical, anchored after `_pickless` as the 13 rows that already carried the field
are). Inputs: docs/inputs/afl_list_changes/{2025,2024}.csv (+ README with the rule and the Thomas override).
Match report: 217 valid exits (13 already carried the fact and agree), 21 void (re-appeared: active now, played
later, or on the next year's list), 4 names not in the store (never played: McHenry, Adam Kennedy, Trent
McKenzie, the young Tom Scully), 3 name twins resolved by last game <= exit year.

## Why the board cannot move
Every edited row is `_retired`; the engine prices a retired row as scrap regardless of `_last_listed`
(`delisted()` is `_retired or _last_listed < 2026`). The as-at season boards read the fact; the live board does not.
