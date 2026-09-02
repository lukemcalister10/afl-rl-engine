# FW1 REPORT — making Finals Week 1 a point on the movers list

## What was wrong

FW1 was landed on 2026-08-30 as a store edit: 92 finalists gained a game, their season averages
moved, the board moved. The store was right. Nothing else was.

* **The movers list ended at R24.** A round becomes a point because `round_movers.py` writes a
  weekly report into `ui/data/movers.js`. The finals lane never runs that path, so the week that
  moved the board left no record. Harry Dean's 100+ was in his average and nowhere in his history.
* **Then the bust-exclusion landing evicted FW1 from the default view**, because the model change
  was newer than the last stored point.
* **Then a re-price made it worse.** The R14–R24 retrospective was re-priced against a stale
  control that still expected r24 to reproduce a live board which now included the finals game.
  Satisfying that control pushed the finals game backwards into every round: Dean carried 11 games
  at R14 when he had played 10. The control was stale; the data was bent to fit it.

## What this does

`emit_fw1_report.py` emits the FW1 weekly report at **feed round 25** from the edit that was
actually flown, and reconciles every score rather than restating it:

    implied = games_new * avg_new - games_old * avg_old
    HALT if |implied - score| > 0.6, or if games_new != games_old + 1

Result: **92 players resolved, all 92 scores reconciled**; report 25 carries 804 players,
92 played, 712 DNP.

The report's `release_identity` is read from the landing commit `3016935`'s
`data/expected_boot.json` (not the working tree) with `as_of_round = 25`. The engine contract
holds at 24 while a finals week is played — the report names the FEED round, and the app reads it
that way. `ui/tests/movers.test.js` carries the fixture that proves this.

Source store: `a9dec7e4785c6861a84f3beaae2f020e` -> `415929d3c9d561cc58bef00ae63432b2`.

## The rest of the repair

* Retro window extended to `ROUNDS 14..25` / `APPLIED 15..25` in all three retro scripts.
* `derive_season_state` clamps the calendar with `min(R, HOME_AND_AWAY_ROUNDS)`, so r25 prices at
  `cal 1.00 pace 0.909` — identical to live. A finals week does not advance the season clock.
* The control moved from a hardcoded r24 to `ROUNDS[-1]`: the finals point must reproduce the live
  board exactly.
* Two new assertions in `ui/tests/movers.test.js` fail if a finals week that moved the board has no
  weekly report — the defect that started this cannot recur silently.

Verified game counts after the repair: Dean **R14 = 10** (was 11), **R24 = 19**, **FW1 = 20**.

The repeatable procedure is step 5 of `docs/evidence/finals_fw1_2026-08-30/RUNBOOK_finals_week.md`.
