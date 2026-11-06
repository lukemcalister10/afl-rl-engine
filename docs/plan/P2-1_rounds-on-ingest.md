# P2-1 — Home-and-away rounds through `tools/ingest` (MEDIUM; BEFORE 2027 ROUND 1; owner's signed word)

**Depends on.** P3-1, P2-4, P3-2 (landed, or rehearsed on the same copy). Serial rule: tools/ingest.py, steps.py.
**Owner word.** RULEBOOK P14 (RULEBOOK.md:167-174): "No session adds a step to this path without the owner's signed
word." This item adds the calendar advance and a round report to the weekly path: get the word before landing.

**Done when.** `tools/ingest scores/R<n>.csv` on a 2027 tree resolves names, edits the season row (games +1,
re-averaged), advances the calendar N→N+1 through the lane, writes the round's weekly report, and pushes; it refuses a
round out of order; and the round lane (P4-4) is still in place until a real or rehearsed 2027 round has landed.

**Facts (checked at ffb2663b).**
- tools/ingest.py:179-181 dies on `R\d+` ("the next one is 2027 round 1, after the season rollover"). `R25` is not
  a round: WEEK_ALIASES (:71) maps FW1→25 … GF→29; the next home-and-away round is 2027 R1. SEASON = 2026 is a
  literal (:63; P3-1). build_spec (:388-437) declares `as_of_round` UNMOVED (:418-420).
- Declaring as_of_round in `moves` does nothing: it is a DELEGATED_PIN (steps.py:112) and the pins step only logs
  "delegated … not here" (:1323-1327). The real blocker is the season-clock step (:872-892): it derives at the
  CURRENT as_of_round and stops if anything but source_store_md5 moves; `_finals_exposure_hold` returns None below the
  round-24 ceiling (:933-934). So the lane can neither advance the clock (it derives at N, never N+1) nor absorb a
  round whose games move exposure_pace (it stops).
- The edit lane's `lineage` step writes an out-of-round column and a release_lineage entry when the board moves
  (:1392-1430) — a round earns neither (ROUND_SEQUENCE comment, :3836-3841; build_spec always sends a `column` and `lineage`, :421-430).
- Writer 4c writes a weekly report only for a FINALS column (`feed_round_of(col) is not None`, :2120); a round would
  land with no report. round_movers.fixture_clubs returns None (every club played) when a round has no fixture entry
  (round_movers.py:329-356) — wrong for a BYE round, where clubs sit out and their players would be marked DNP.
- tools/ingest_bounds.py limits were calibrated on FW2 (:7-17), a finals week; rounds move more players.
- A replay of R24 cannot run on the pre-R24 tree (R24 landed 2026-08-23 via the round lane, docs/evidence/
  r24_advance_2026-08-23): tools/ingest.py (added 2026-09-24, 74e084cf), the edit lane and finals_report.py (2026-09-10)
  did not exist. The FW2 replay precedent (docs/runbooks/WEEKLY_SCORES.md:49-53) was finals on a post-ingest tree.

**Change.**
1. A season-state writer for a round act (reuse P3-2's): as_of_round N→N+1 in data/expected_boot.json,
   release_contract.json (restamp_dynamic, release_contract.py:441) and season_state.json, deriving at N+1.
2. No column and no lineage entry for a round. Today spec.py:536-540 refuses a store-edit that moves the board with
   `column: null`; its `column._exempt_because` escape still hands the lineage step a column object, which it then
   writes (:1414-1416). Add one declared round marker that the validator and the lineage step both recognise.
3. A round-report writer (round_movers report for feed round N, keyed per P2-4), run where 4c runs.
4. Fixtures: a bye round carries a fixtures.json entry listing the clubs that played; a round with no entry means
   all 18 played (as today).
5. ingest_bounds re-calibrated on R21-R24 (scores/R21.csv … R24.csv exist): measure each limit on those four rounds.
6. One out-of-order guard: the round must be as_of_round+1.

**Must not change.** The finals path (byte-identical behaviour for FW files); the store-edit shape (change edits only);
the season-clock stop for every non-round act; the engine.

**Prove it.** Hybrid replay: take the tree before the R24 inputs (the parent of a6ba4da7, the R24 scores commit;
the landing is adf380b1, 2026-08-23), overlay today's tools/ingest.py,
tools/landing/, finals_report.py and round_movers.py, run `tools/ingest scores/R24.csv`, and compare the landed store,
board and movers report to the R24 act's (docs/evidence/r24_advance_2026-08-23) — explain every difference (engine
changes since August mean the board will differ; the store edits must not). Then a synthetic 2027 R1 on the P3-2
rehearsal copy. tools/test_ingest.py extended for rounds; test_store_edit.py; acceptance `--profile full`.

**Lands via.** Plain commit of the tooling, on the owner's word. Keep `land round` until a 2027 round has landed (P4-4).
