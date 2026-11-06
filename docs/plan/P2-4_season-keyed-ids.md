# P2-4 — Season-keyed ids wherever a round number is a key (MEDIUM)

**Depends on.** P2-2 (one movers serialiser, so the migrated bundle has one canonical form). Serial rule:
steps.py, tools/ingest.py. Needed by P3-2 and P2-1.

**Done when.** Every report, retro point, bank and fixture keyed by a bare round number carries the season, through
ONE parser per language (`round_key.parse(id) -> (season, feed_round)` in engine/rl_after/ingestion, mirrored once in
ui/app/movers.js `core`), the committed data is migrated once with a reversible mapping beside it, and every reader
uses the parser (no dual-shape readers).

**Facts (checked at ffb2663b).**
- ui/data/movers.js `reports` keys are bare strings '15'…'29' (feed rounds 25-29 = FW1…GF, tools/ingest.py:71).
- season_state.finals_played does `int(rnd)` on every report key (season_state.py:67-78); a key like `2026-FW1`
  raises ValueError, and it is called by every held store edit (steps.py:937, `_finals_exposure_hold`).
- steps.py:2089-2095: banks found by `re.match(r'values_r(\d+)\.json$')`; retro point ids parsed by
  `int(_i.split('-r')[-1])`. tools/ingest.py:445 carries `values_r*.json` as a glob (WEEK_CARRIERS);
  :189-194 tests `str(feed) in reports` and `range(25, feed)`; :63 `SEASON = 2026`; the column id already carries the
  season (`<prefix><slug>-<SEASON>`, :398).
- Banks: docs/evidence/walkforward_retro_2026-08-29/values_r14.json … values_r29.json; point ids `retro-r14` …
  (ui/tests/movers.test.js has 11 `retro-r` occurrences).
- The value history is engine/rl_after/ingestion/value_history.json (written via out_of_round_column; read at steps.py:1443, :3488);
  there is no data/value_history.json.
- The UI has no `> 24` comparisons: it uses `core.HOME_AND_AWAY_ROUNDS` (ui/app/movers.js:373, :418) and
  `core.FINALS_COLUMNS` (:445-448), read by card.js:212 and history.js:52. Python twins: spec.py:30 HOME_AND_AWAY_ROUNDS,
  :36 FINALS_FEED_CEILING, round_movers.FINALS_WEEK_NAMES / FINALS_COLUMN_PREFIXES (test_finals_bounds.py asserts
  they agree).
- scores/fixtures.json: `season` "2026", `weeks` keyed '25'… .

**Change.** Pick the id form once (e.g. `2026-R24`, `2026-F25` — the feed number keeps finals ordering trivial) and
write it in round_key.py's docstring. Migrate movers.js `reports`/`rounds`/`points` ids, the bank filenames (or a
season sub-directory), fixtures.json `weeks`, and value_history column references in ONE commit, with the
old→new mapping committed as JSON beside the migrated data (reversible). Every reader above goes
through the parser; season_state.finals_played compares (season, round) against (season_year, 24).

**Must not change.** Values, rows, report contents, board, store, pins. The lander's writer 4 + 4b full-cycle check
(P2-2) must reproduce the migrated bundle byte-identically.

**Prove it.** `node` every ui/tests suite (movers.test.js fixtures updated to the new ids);
`python3 engine/rl_after/ingestion/test_movers_transition.py`, `test_finals_report.py`; `python3 tools/test_ingest.py`;
`python3 tools/landing/test_finals_bounds.py`, `test_store_edit.py`; a held-store-edit dry run (`tools/ingest --check`
on a synthetic finals file in a scratch copy) reaches `_finals_exposure_hold` without a ValueError; the P2-2 full-cycle
drift check; acceptance `--profile full`; standalone smoke of the UI movers page.

**Lands via.** Plain commit (UI/ingest data migration, no identity moves), with the full DEFAULT_GATES run by hand.
