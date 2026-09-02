# LANDING A FINALS WEEK — the runbook, written from the one that worked

FW2..GF are the same act as FW1 with a different score file. Four steps, two builds.

## 0. The score file

`scores/FW2.csv` etc., in the FootyWire SC-column form `footywire_parser` reads. Declare which
clubs played nowhere — a store edit does not need a fixture, because it does not describe absence.
A player not in the file simply gains no game, which is the whole of the rule.

## 1. The plan  (one engine load, ~20 min)

    ./tools/harness docs/evidence/<act>/pass_finals_edit_plan.py

Emits `FINALS_EDIT_PLAN.json`: the edit list and the movers it predicts. It CONTROLS first — the
untouched board must reprice to the live board with 0 diffs, because a plan measured against a board
that does not reproduce is worthless. The arithmetic is the ingestor's own `_mean` at the ingestor's
own `ROUND_DECIMALS`, CALLED rather than restated; the first FW1 preview restated it at one decimal
and was wrong.

## 2. The spec

    python3 docs/evidence/<act>/build_finals_edit_spec.py

Mechanical: drops no-op fields, halts if any player would carry no edit at all or if a played game
fails to increment `games`, then validates.

## 3. Fly it — AND EXPECT THE FIRST FLIGHT TO ABORT ON THE MOVERS

    ./tools/land edit --spec <spec> --log <log> --report <report>

**The plan's mover prediction will be wrong, and this is not a bug in the plan.** Pricing in memory
cannot reproduce the engine's LOAD-TIME CALIBRATION REFIT: move 92 players' season averages and the
population statistics the model prices against move with them, so every valued row shifts a little.
FW1 predicted 86 movers and a ripple of exactly zero; the builder found 234, of which 146 were
players who did not play, moving by a median of 1 point (0.082% of value).

So the first flight builds the board, measures every mover, aborts on the declaration, and restores
every carrier byte-exact. That is the falsifier working.

## 4. READ the difference, then declare it and re-fly

**Do not automate this step.** Parsing the true movers out of the flight log and writing them back
into the spec is three lines of code, and making it automatic would turn the one assertion that
catches a bad edit into a rubber stamp — it would have accepted the 0.83 `calendar_progress`
disaster without comment. The judgement being made here is *"is this ripple the model
re-calibrating, or is it the act doing something it should not?"*, and that judgement is the point.

The bar: the ripple is small (single points, sub-0.1% of value), mixed in direction, and confined to
re-calibration. A systematic move — every completed season repriced, one direction, percentage-scale
— is the finals lane's known failure mode and a HALT, not a thing to declare and re-fly.

Once declared, the re-flight asserts DETERMINISM: identical inputs, identical board, or an abort
naming the player. Say so in the spec's own doc field; do not present a measurement as a forecast.

## 5. MAKE THE WEEK A POINT ON THE MOVERS LIST  (added 2026-09-02)

FW1 was landed without this step and the week vanished: the board moved, the store carried the
scores, and the movers list ended at R24 as if the week had not been played. The store edit is not
self-announcing. Two things have to be written by hand.

**(a) The weekly report.** A round becomes a point on the movers list because
`round_movers.py` writes a report into `ui/data/movers.js`. The finals lane does not run that path,
so emit the report yourself at the FEED round (FW1 = 25, FW2 = 26, ...) from the edit that was
actually flown:

    python3 docs/evidence/fw<N>_report_<date>/emit_fw<N>_report.py

Copy `docs/evidence/fw1_report_2026-09-02/emit_fw1_report.py` and change the four constants at the
top (`FEED_ROUND`, `PREV_POINT`, `THIS_POINT`, and the two store md5s). It RECONCILES rather than
restates: for every player it recomputes `score = games_new * avg_new - games_old * avg_old` from
the landed spec and refuses to emit if any score disagrees by more than 0.6, or if `games` did not
increment by exactly one. That check is the whole value of the step — it is the only thing standing
between a typo in a score file and a board nobody can audit.

The report's `release_identity` is read from the LANDING COMMIT's `data/expected_boot.json`, not
from the working tree, with `as_of_round` set to the FEED round. The engine contract holds at 24
while a finals week is played; the report names the week, and `ui/app/movers.js` reads the feed
round. Do not "fix" the app to clamp it — `ui/tests/movers.test.js` already has the fixture that
proves the app is right.

**(b) The retro window.** Extend `ROUNDS` / `APPLIED` by the new feed round in all three of
`retro_walkforward.py`, `pass_retro_series.py` and `emit_retro_series.py`, and add the week to
`FINALS_NAMES`. The calendar must NOT advance: `derive_season_state` clamps with
`min(R, HOME_AND_AWAY_ROUNDS)`, so a finals round prices at `cal 1.00` exactly as the live board
does. Then re-emit the truncated stores and re-price:

    ./tools/harness docs/evidence/walkforward_retro_2026-08-29/pass_retro_series.py

ONE engine load for the whole series (~8 min load, ~2 min a round). Never the per-round subprocess
path, and never `resume` under a timer — `resume` skips only BANKED rounds, so a timer around it
starts a second build on the same workspace and the two rmtree each other.

The control is the last round in the window: re-pricing the finals week from the truncated store
must reproduce the LIVE board exactly, 0 diffs. If it does not, the retro is wrong, not the board.

**The three checks that must hold before this is done:**

1. The weekly report reproduces the store's counts exactly (a played finalist's `games` goes up one).
2. Every round's game count is the true as-at count — a finalist at R14 must NOT carry the finals
   game. This is the failure the 2026-09-01 re-price introduced: the finals game was pushed back
   into every retro round because the control was stale and the data was bent to satisfy it.
3. The finals point reproduces the live board exactly.

## 6. Close the act

    python3 docs/evidence/walkforward_retro_2026-08-29/emit_retro_series.py
    node docs/evidence/<act>/verify_movers_history.js <baseline-movers.js> ui/data/movers.js

Every act that rebuilds the bundle DROPS the R14-R24 retrospective — `points` is built from the
value-history columns and a retro point is not one. Re-emit it (banked values, no re-pricing, so it
is byte-exact) and verify. `ui/tests/movers.test.js` now fails if the shipped bundle is missing it,
and gate 5 runs that file inside every landing, so this cannot go unnoticed again.

Take the baseline copy of `ui/data/movers.js` BEFORE step 3.

## What this act does NOT do, and must not start doing

* It does not touch the calendar. `as_of_round`, `calendar_progress` and `season_total_rounds` are
  untouched, which is why non-finalists' completed seasons are safe BY CONSTRUCTION.
* It does not touch the career `games` field. `_merge_into_store` does not either.
* It is not a round. There is no dedup ledger key, no finalization state, no round history point.
  Re-applying the same week halts because `old` no longer matches the store.
