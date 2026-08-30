# PREREG — FINALS WEEK 1 · 2026-08-30

## What this act is, and what it deliberately is not

FW1 applies real football to the store: 92 players across four clubs, the SuperCoach SC column,
transcribed from the owner's screenshots and verified against his own conservation check.

**It is not a round advance.** Feed round 25 is a `(player, season, round)` dedup-ledger key. The
CALENDAR round is HELD at 24 (`staged_apply.calendar_rounds`), so `calendar_progress` stays 1.00 and
every non-finalist's completed season is priced exactly as it is today. Stretching the season to 29
calendar rounds instead would drop progress to 0.83 and re-open every finished season in the
competition — the punishment of non-finalists the owner ruled against.

Because the board moves and the round does not, this act **earns an out-of-round column and a
lineage entry**, exactly as a dial flip does (standing rule 2026-07-28).

## The prediction, measured

A preview ran on a loaded engine — the ingestor's own merge (`avg × games + score`, over `games + 1`),
applied in memory, priced, then restored:

* **CONTROL PASS** — the untouched board repriced to the live board, **0 diffs**, before anything was
  changed. A preview measured against a board that does not reproduce is worthless.
* **87 direct movers**, every one of them a player who played. The other 5 of the 92 priced unchanged.
* **Nobody who did not play moves at all.** No ripple.
* Pool **702,917 → 704,376 (+1,459)**.
* Restored and re-priced: the board returned byte-identical to where it started.

Largest: Freijah +359 (112), Dean +230 (99), Naughton +225 (110). Largest falls: Windsor −128 (49),
Hewett −128 (72), Wilson −115 (52). Bontempelli's 134 — the round's top score — moves him +79, the
diminishing return on a player already priced high.

## Participation — the owner's ruling, asserted as a partition

    played        92   the four clubs, 23 each
    dnp           93   at a club that PLAYED, not selected — a real DNP, shown
    unrecorded   619   club did not play — the engine is told nothing about him
    ----------------
    total        804   == the active board

Owner, 2026-08-30: *"should carry a DNP but the DNP shouldn't directly count against a player."*
Under the two-state rule that shipped before this, `dnp` would have been **712**. `round_movers`
asserts the partition and refuses a report whose counts do not add up, so a mis-scoped fixture is a
halt rather than a silently mislabelled board.

## Arming

LAW 10(c). Owner word, verbatim: **"Explicit word given"**, on the movers preview above. The token
`FW1-2026-08-30-owner-approved` follows the R24 convention because he gave his word without naming
one; `_apply_enabled()` requires only that it be non-empty alongside the separate ARMED code half, so
it is a label on the record rather than a secret. The authorisation is his; the string is not, and
that is stated rather than passed off.

## What must hold

`board_after` is null: a round board is a function of scores nobody has priced through the real
applier yet, and a seat predicting it would be copying it out of a build already run. The preview
above is the expectation the movers are read against, not a byte-exact prediction.

`as_of_round` is declared UNMOVED. If it moves, the act has failed at its central purpose.
