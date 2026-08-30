# PREREG — FINALS WEEK 1 · 2026-08-30

## What this act is

92 players at four clubs played a final. Each gains **one game** and a **re-averaged 2026 season
row**. That is the whole change to the store.

## Why it is a store edit and not a round

The owner, 2026-08-30: *"We're literally just updating player averages and game counts. Before round
14 we didn't add games one by one, we just priced based off averages and total season game counts.
It really shouldn't be that hard."*

The store agrees with him, and always has. Marcus Bontempelli's own rows:

    2016   avg 108.7    games 26     22 home-and-away + 4 finals
    2021   avg 119.5    games 26     a Grand Final year
    2026   avg 117.17   games 22     where FW1 goes

A finals game has never been a calendar event in this store; it is two numbers on a season row. The
round-advance lane was asked to model it as "a round that holds the calendar", which dragged in the
dedup ledger, finalization state, round history and — the reason this act exists at all — a
recomputation of `season_state`. That recomputation stretched `calendar_progress` from 1.00 to 0.83
(fixed in 2d28deb), which is the punishment of non-finalists the owner ruled against.

**A store edit does not recompute season state. It holds it.** Non-finalists are untouched by
construction rather than by a hold applied correctly in eleven places.

## The edits

    184 edits over 92 players
      scoring[2026].games   g  ->  g + 1
      scoring[2026].avg     a  ->  round((a*g + score) / (g+1), 2)

and nothing else. The career `games` field is deliberately NOT touched: `_merge_into_store`
(round_apply.py:185) does not touch it either, and an edit that also moved it would be a second
writer inventing a rule the ingestor never had.

The averages come from the ingestor's own `_mean` at the ingestor's own `ROUND_DECIMALS = 2`,
called rather than restated. **The earlier preview rounded to one decimal and was wrong to**; its
mover list is superseded by the one below.

## The prediction, measured — REVISED after the first flight

The first flight priced the edit IN MEMORY on a loaded engine and predicted **86 movers, all of
them players who played, none who did not**. The builder disagreed, and aborted on the declaration
before touching anything: **234 movers**. The in-memory path cannot reproduce the **load-time
calibration refit** — move 92 players' averages and the population statistics the model prices
against move with them, so every valued row shifts a little. The first prediction was wrong in the
interesting direction: it claimed a ripple of zero, and there is one.

That flight built the board, measured every mover, and restored the tree byte-exact. What is
declared below is therefore what the REAL builder produced from these exact 184 edits on this exact
store, and the re-flight asserts determinism rather than prediction.

    234 movers of 1002 valued rows
      88 of the 92 players who played FW1   (4 of them priced unchanged)
      146 who did not play — the calibration ripple
    pool  702,917 -> 703,913  (+996)

Largest rises: Joel Freijah +358, Harry Dean +229, Aaron Naughton +226.
Largest falls: Jack Viney -215, George Hewett -135, Caleb Windsor -131.

### The ripple, measured — because "doesn't punish non finalist sides" is the ruling

    median  1 point   (0.082% of value)
    mean    1.9 points
    90th    4 points  (0.331%)
    max     8 points  (Harry Sheezel)
    moved by more than 5 points: 5 of 146

It is noise, not a penalty, and it is not one-directional — some non-finalists gain. This is the
same re-calibration any store edit or round advance produces, and it is a different animal from the
`calendar_progress` stretch the round lane would have applied: that one moved every completed
season's pricing systematically, which is what the owner ruled against.

## What must hold

`board_after` is null: a board priced from scores nobody has put through the real builder cannot be
predicted without running it, and copying it out of a build already run is not a prediction.

`as_of_round` is declared UNMOVED, and so is every model pin. The calendar does not move because
nothing in this act asks it to.

## The movers list since round 14

Owner: *"As long as it doesn't impact the movers list still being accurate as of each round since
round 14."*

Two facts, both checked against the record rather than assumed:

1. **The per-round reports R15-R24 are frozen era history and a store edit does not touch them.**
   Verified on the previous store edit (f1026eb): every one of the ten reports was byte-identical
   before and after.
2. **The retrospective series R14-R24 is dropped from the bundle by any act that rebuilds it**, and
   must be re-emitted afterwards. That is not new to this act — f1026eb dropped it too and
   b53cde1 restored it. The emitter replays BANKED per-round values (`values_r14..24.json`); it does
   not re-price, so what comes back is byte-identical. Verified: the series regenerated after
   f1026eb matches the first emission exactly, and matches what is live now.

The re-emission is part of this act's close, and the byte-identity of all 11 retro points is
asserted rather than hoped for.
