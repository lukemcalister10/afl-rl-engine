# P3-2 — The season rollover (MEDIUM; AFTER THE DRAFT — owner ruling 2026-10-14)

**Goal.** `tools/rollover 2027` turns the end-of-2026 tree into the start-of-2027 tree in one landed act:
season_state (season_year 2027, as_of_round 0, calendar_progress 0, exposure_pace from the previous season's
completed rows), every store row gains an empty 2027 scoring row where the engine expects one (read how 2026's
0-game rows are represented: 805 rows incl. 0-game), the retirements/delistings from the AFL 2026 list applied
via `tools/player retire` (the listing fact), the draft intake added via `tools/player add` from the owner's
draft file (national, rookie, MSD, pathway, SSP as they occur), the fixtures file reset, the column/report ids
keyed 2027 (P2-4), the movers bundle's season rolled (a new season section; 2026 kept), the phantom-pick
classes advanced (2028/2029), and the as-at banks for end-2026 produced by the as-at pass (so −1 becomes 2026).

**Why.** The engine has never rolled a season; everything that says 2026 was hand-written in July.

**Files.** New tools/rollover.py; season_state.py; tools/ingest.py (first week of 2027 must work after);
engine/rl_after/rl_export.py (lens years from LIVE_SEASON — P3-1); scores/fixtures.json; docs/runbooks/ROLLOVER.md.

**Rules.** Depends on P3-1, P2-3, P2-4, P5-3. The rollover is a store-edit act with declared movers (every
retired row leaves the board; every draftee appears at his pick price): the dry run predicts them. Rehearsal
on a copy FIRST (P3-3 is this rehearsal: a worktree with a scratch remote, run the rollover, build, run the
first "week" with a synthetic R1 file through tools/ingest, every gate green) before the real one. The
rulebook's P1 applies (owner sees the movers: the whole new board).

**Proof.** The rehearsal, repeated until it is boring; then the real act with the owner's word.

**Lands via.** Store-edit act(s) through the lane.
