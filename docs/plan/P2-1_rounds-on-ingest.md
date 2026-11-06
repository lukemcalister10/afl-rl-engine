# P2-1 — Home-and-away rounds through `tools/ingest` (LOW)

**Goal.** `tools/ingest scores/R25.csv` applies a home-and-away round the way it applies a finals week today:
names resolved, games +1 and averages re-averaged, inputs committed first, landed through the store-edit lane,
pushed. The only difference from a finals week: the calendar ADVANCES (`as_of_round` +1, `season_state`
re-derived with the new round, calendar_progress recomputed) and every club plays, so absence is a DNP.

**Why.** Today `tools/ingest.py:180` dies on a round ("Rounds ADVANCE the calendar, which this path does not
do") and rounds go through the separate `land round` lane (ROUND_SEQUENCE in tools/landing/steps.py), a second
copy of the same machinery (it still carries the retired sibling step). One command for every week is the
owner's standing ask ("It really shouldn't be that hard").

**Files.** tools/ingest.py (the round branch, `WEEK_CARRIERS`, the summary), tools/landing/steps.py (the
`_finals_exposure_hold` / season-state re-derive: a round must NOT hold, it advances), season_state.py (the
derive call), engine/rl_after/ingestion/round_movers.py (report writer: `fixture_clubs` returns None for a
round — already), scores/fixtures.json (no entry needed for a round), docs/runbooks/WEEKLY_SCORES.md.

**Rules.** The store edit for a round is the same shape as a finals week (change edits only). The calendar
advance is the ONLY extra write: `as_of_round` in data/expected_boot.json / release_contract.json /
season_state.json move together (the lane's pins step must declare `as_of_round` in `moves` for a round act;
today's finals specs declare it unmoved — read tools/landing/spec.py for the as_of_round rules). The exposure
pace re-derives from the edited store (no hold). Column id `<prefix><slug>-<SEASON>` as today. The
`ingest_bounds` gate stays. Nothing in the engine changes.

**Proof.** Replay R24 (scores/R24.csv exists) on a copy of the pre-R24 tree: the landed R24 store and board
must reproduce byte-identical (the FW2 replay precedent in WEEKLY_SCORES.md: store a367386a, board d3fb6b48).
tools/test_ingest.py extended for the round branch; the lane's test_txn / test_store_edit; acceptance green.

**Lands via.** Plain commit of the tooling; the proof is the replay. After this lands, P4-4 deletes the round lane.
