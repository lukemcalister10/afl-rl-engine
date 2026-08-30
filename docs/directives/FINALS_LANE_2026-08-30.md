# THE FINALS LANE — how FW1..GF reach the engine · design, 2026-08-30

**Owner rulings this is built on, verbatim:**

* *"it would be beneficial if the movers list was round 23 to 24, under the current model"* — the
  same standing rule gives a finals week its own column.
* *"a way … that accounts for some players playing more than 23 games in a season and that being
  fine, but also doesn't punish non finalist sides"*.
* *"should carry a DNP but the DNP shouldn't directly count against a player"*.
* *"FW1 is 4 teams playing / FW2 is 8 teams / SF is 4 teams / PF is 4 teams / GF is 2 teams"*,
  *"46 players in a match not 44"*, *"28 is the max games, as 23 is the max in the regular season"*.

## What already works and must not be rebuilt

**The merge is already right.** `staged_apply` folds a round's scores into the season row as
`mtotal = avg × games + total; avg = mean(mtotal, games + n)`. Finals games fold in exactly as
home-and-away games do — which is what 2024 and 2025 already look like in the store (max 27 games,
55 and 61 players over 23). Applying finals is CONSISTENT with every completed season, not a new
rule. Nothing about the merge changes.

**The store already does the right thing on absence.** A player not in the scores file simply has no
games added. There is no "DNP" written anywhere in the store, so a non-finalist is not marked with
anything. The problem is entirely in the REPORT, below.

## The four changes, smallest first

### 1. The DNP becomes three-state, scoped by the fixture — THE OWNER'S RULING

`round_movers.py:311` sets `'played': did_play, 'dnp': not did_play`, and `did_play = key in played`.
Every active player absent from the file is a DNP. In a home-and-away round that is correct, because
all 18 clubs play. In FW1 it marks **712 of 804 players** as DNP for the crime of their club not
making the four.

The vocabulary for the fix already exists and is already rendered: `ui/app/movers.js`
`core.participation()` reads `played: null, dnp: null` as **"not recorded"**, a third state distinct
from both played and DNP, and `ui/app/history.js` carries the same law — *"it fails SAFE — an
unrecognised shape yields 'not recorded', never a DNP."* The producer simply has to emit it.

    dnp        = absent AND his club played this week      (a real DNP: dropped, or a late out)
    unrecorded = absent AND his club did not play          (no football happened for him)

This is the whole of *"the DNP shouldn't directly count against a player"*: a genuine finals DNP is
shown, and a non-finalist is told to the engine as nothing at all.

**It needs one input the scores file cannot carry: which clubs played that week.** Two matches of
names do not identify the fixture, because a club can field a player the store has at another club —
three of them appear in FW1 alone (Schultz, Membrey, Sharp). The fixture is declared, not inferred.

### 2. The feed-round bound, so a finals week is a legal round

`round_apply.DEFAULT_SEASON_ROUNDS = 24` refuses a feed round outside [1, 24] as a fat-fingered
round. Finals need distinct round numbers because the dedup ledger keys on
`(stable_player_id, season, round)` — that ledger is what blocks an accidental re-send, and it is
worth keeping exactly as it is. So finals take feed rounds **25 = FW1, 26 = FW2, 27 = SF, 28 = PF,
29 = GF**, and the bound rises to 29.

A FEED ROUND IS NOT THE CALENDAR. This number is a ledger key and a sanity bound. It is not
`as_of_round`, which is the next point.

### 3. `as_of_round` HOLDS at 24 — this is what protects non-finalists

`calendar_progress = as_of_round / season_total_rounds` is 24/24 = **1.00**, and it must stay there.
A non-finalist's season IS complete; his row is priced on final-games footing with no gross-up,
exactly as it is today, and a finals application must not move him by a single point.

Stretching the season to 29 rounds would drop calendar progress to 0.83 and re-open every
non-finalist's season as though it were still running. That is the trap, and it is avoided by simply
not doing it. The edit verb already HOLDS the round it finds (`spec.py`: *"a store-edit act … HOLDS
the round it finds, exactly as a lever landing does"*), so the lane is the edit verb, not the round
advance.

### 4. `exposure_pace` is fenced to home-and-away games

`season_state.exposure_pace` is `median(current-season games of the durable population) / 22` — a
POPULATION statistic with a shared denominator, and only finalists can raise it. Measured: it would
not actually move, because finals games land on players already above the median (median 20 either
way, pace 0.909). But that is luck, not structure, and it would move if the population shifted. The
pace is computed on feed rounds ≤ 24 so eight clubs cannot move a league-wide dial.

## What each finals week needs from the owner

1. `scores/FW<n>.csv` — `name,score` from the SC column (already delivered for FW1, verified).
2. **The fixture**: which clubs played. Five words.

## Verification, per week, before anything is applied

* `tools/score_sheet_check.py` — the conservation law: each match's two teams sum to ~3300 (±25).
  This is the only check that catches a misread SCORE on a correctly spelled name.
* Name resolution against the store — catches a misread NAME; already fail-closed in the applier.
* `tools/store_sanity.py` — no season exceeds 28 games (23 H&A + 5 finals).
* The movers report's own counts: `played + dnp + unrecorded == the active board`, with `unrecorded`
  equal to the players at clubs that did not play. A finals week where that identity does not hold
  has mis-scoped its fixture, and the count is the proof.
