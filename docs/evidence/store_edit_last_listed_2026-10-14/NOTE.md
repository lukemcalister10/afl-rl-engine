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

## What moves on the board (measured by the first flight, which the lander aborted because the spec said nothing would)
No active row: the active pool is 687,821 before and after. The engine's old retiree recall (rl_model.py
`_on_board`/`_backval`) reads `_last_listed`, so 31 of the 201 rows APPEAR in the board's dormant `back` section at
scrap values (1..54). Nothing renders that section; it is the old −1/−2 machinery the as-at boards supersede.
The 31 are declared as the act's movers.
