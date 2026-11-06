# P3-2 — The season rollover (HIGH; AFTER THE DRAFT — owner ruling 2026-10-14; owner word)

**Depends on.** P3-1 (live_season), P2-3 (tools/player add/retire), P2-4 (season-keyed ids), P5-3 (as-at columns),
P4-3 (the config move: the two INPROG dials go to "2027"). On P2-1, see "Rehearsal" — the reviewer asked to add P2-1
as a dependency; that would be circular (P2-1 needs this rollover landed or rehearsed), so it is split below.

**Done when.** `tools/rollover 2027 --draft <owner's draft file> --list-changes docs/inputs/afl_list_changes/2026.csv [--check]` turns the
end-of-2026 tree into the start-of-2027 tree in one landed store-edit act (or a declared short series), shown to the
owner as a full movers board first, and the first 2027 week can then be ingested (P2-1).

**Facts (checked at ffb2663b).**
- data/season_state.json: season_year 2026, as_of_round 24, calendar_progress 1.0, exposure_pace 0.909 (derived by
  season_state.derive, season_state.py:143; calendar_progress(as_of, total) :55).
- `as_of_round` and `season_state` are DELEGATED_PINS owned by "the round lander (2b)" (steps.py:112-113); the edit
  lane's season-clock step re-derives at the CURRENT as_of_round and STOPS if anything but source_store_md5 moves
  (steps.py:872-892). A rollover therefore needs a declared season-state writer in the edit lane (season_year+1,
  as_of_round 0, re-derived from the edited store). Build it here; P2-1 reuses it for round N→N+1.
- Store: 805 rows carry a 2026 scoring row, 137 of them with 0 games — measure how a 0-game live row is represented
  and whether the engine needs a 2027 row at round 0 (build a copy both ways; do not assume).
- The as-at banks/emitter use SEASONS = (2025, 2024) (emit_asat_seasons.py:42) — they become (2026, 2025).
  Phantom pick classes start at 2027 (rl_export.py:1029). tools/ingest.py:63 SEASON (P3-1 routes it).
  RL_M3_INPROG_Y / RL_EXPO_INPROG_Y are pinned "2026" in data/model_config.json (config identity; P3-1 asserts they
  equal season_year, so the rollover must move them with it).
- scores/fixtures.json `season` "2026"; ui/data/movers.js has one season of reports (P2-4 makes room for two).
- The list-change input exists: docs/inputs/afl_list_changes/2026.csv (commit b7344862, on main after ffb2663b:
  header `club,direction,name,detail`; 160 OUT, 41 IN, details like "delisted", "trade, Port Adelaide", "free agent,
  Western Bulldogs", "committed to signing"). Its README's owner rule (2026-10-14): only `ret` and `del` are list
  exits; a valid exit at the end of Y sets `_last_listed = Y`.
- The RULEBOOK has no season/rollover text (`grep -in "season\|rollover" docs/RULEBOOK.md`): no law 10a edit needed.

**Change.** tools/rollover.py builds the edit spec from 2026.csv: OUT + retired/delisted → `tools/player retire`
(`_retired`, `_last_listed 2026`); OUT as trade or free agent with a destination → `move` to that club; IN from another
AFL club → `move`; IN from outside the AFL → `add`; every row it cannot classify (or match to a store key) is listed for
the owner and the tool stops. Draftees (national, rookie, MSD, pathway, SSP) → `add` at their picks from the owner's
draft file. Season-state move. The two config dials to "2027" ride the act's INPUT commit (data/model_config.json is
not a carrier; recompute its config_sha256) and are declared `config` in `moves` — so P4-3's launch exemption for
declared identities must cover that commit; fixtures reset;
as-at bank re-run for 2026/2025 (so −1 = 2026); movers bundle season section opened. `--check` prints all edits and
the predicted movers (the lane's dry run). docs/runbooks/ROLLOVER.md.

**Must not change.** 2026 history (reports, value/rank histories, release_lineage entries); the frozen v0-surface
signature (a draft intake changes the v0 kernel's roster sample — measure whether the signature moves BEFORE the act;
if it does, a v0surf re-fit is a bake and needs its own word).

**Prove it — rehearsal first (this is P3-3).** A worktree with a scratch remote: run the rollover, land it, build,
every gate green, the owner-readable movers board produced. Then, ONLY once P2-1's code exists, ingest a synthetic
2027 R1 through `tools/ingest` on the same copy (P2-1's own proof). P3-2 lands without waiting for P2-1; its done
condition is the rehearsal through the rollover build. Repeat until boring; then the real act on the owner's word.
Blind independent review (law 11: every player's value moves — ages, calendar 0, retirements, draftees).

**Lands via.** Store-edit act(s) through the lane, `moves` declaring store, board, config, as_of_round, season_state.
