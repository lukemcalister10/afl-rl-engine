# The end-of-2026 exits — store-edit act, 2026-11-06

Owner words (verbatim): "players who have been delisted in real life now also do not have an afl club listed either
(some of these are free agents, some remain affl listed players). so the master store might need an update to
reflect that."; "Please proceed."
Source: the AFL's "Ins and outs: every club's full list changes ahead of 2027" page
(docs/inputs/afl_list_changes/2026.csv), cross-referenced with the owner's locations sheet (blank AFL club).
The two agree on 107 players once Bailey Laurie (Melbourne, owner's correction) is taken out.

## The edits
107 active store rows × two edits each: `_retired` false→true and `_last_listed` add 2026 (the listing fact the
as-at boards read; the owner's rule of 2026-10-14: `ret` and `del` are list exits). AFFL-owned rows keep their
`affl_team`; free agents keep 'Free Agents'. No scoring, draft, or identity field is touched.

## Movers
The 107 rows leave the active board (they move to the dormant back section, as every retired row does).
`expected_movers` is deliberately unset: the board is normalised to its pool, so removing 107 active rows
re-scales every remaining value by a hair and the rounding lands as ±1 on dozens of rows (the returns act of the
same day showed the mirror ripple: 61 rows at exactly −1 when four rows were added). The dry run is the prediction
of record; the report lists every mover with its old and new value, and the 107 vanish entries are checked
against this list by hand after the flight.

## Order
Flown after the roster-returns act (Bedendo, Mirkov, Roarty, Purcell), so `prereg.board_before` is that act's
`board_after`.
