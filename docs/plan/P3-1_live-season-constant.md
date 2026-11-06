# P3-1 — One live season (MEDIUM; board byte-identical)

**Depends on.** P4-3 (engine_head/rl_model in `moves`), P5-4 (last engine refactor before this; serial rule).
Needed by P3-2 and P2-1.

**Done when.** Every literal 2026 that means "the season in progress" in the engine, rl_export, season tooling and
tools/ingest reads one accessor, `season_read.live_season()` (from data/season_state.json `season_year`); every 2026
that is a historical fact keeps its literal with a one-line comment saying so; an inventory of every remaining 2026
literal (file:line, class: live | historical | label) is committed; the board is byte-identical; a 2027 copy builds.

**Facts (checked at ffb2663b).**
- data/season_state.json carries `season_year` 2026 and `inprog_year` 2026. engine/rl_after/season_read.py reads only
  KEYS = calendar_progress, exposure_pace (:16, :26-29): `live_season()` is new.
- Engine sites: rl_model.py:74 `LIVE_SEASON=2026`, :163-164 `AGE_REF`/`BASE_REF=2026`, :1187 and :1215
  `BASE_REF==2026 and AGE_REF==2026`; _merged_recover.py:138 `INPROG_Y` and :1237 `M3_INPROG_Y` (both read
  RL_M3_INPROG_Y), conditional_prior.py:65 `EXPO_INPROG_Y` (RL_EXPO_INPROG_Y); rl_export.py:210-212 (`BASE_REF=
  AGE_REF=2026`, `ev(p,2024/2025/2026)`), :695 and :1005 (`lensYear: 2026+_off`), :1029 (`range(2027, …)` pick classes). tools/ingest.py:63 `SEASON = 2026`.
  The default `Y=2026` arguments of every `ev`/`raw_ev` definition (P5-1 lists them) are live-season defaults.
- RL_M3_INPROG_Y and RL_EXPO_INPROG_Y are manifest dials pinned "2026" (data/model_config.json `vars`) — config
  identity. `config` is in FLIP_SCOPED_IDENTITIES (spec.py:65) and refused in `moves` (:481-488) until P4-3.
- `_has26`: on all 2,650 rows, asserted by test_has26_derived.py:52-53; deleting it is a store edit and the lane has
  no remove verb. DROPPED from this item (the old brief's sub-item). Its reads are already derived from rows.

**Change.**
1. `live_season()` in season_read.py (halts like `value()` when unreadable). Route the live sites through it.
2. Keep the two manifest dials pinned (config UNMOVED in this item) and add a load-time check in the engine that
   each equals `live_season()` — HALT with the remedy if not. P3-2 moves them to 2027 as a declared config move.
3. Lens years in rl_export become `live_season() + k`; the `Y=2026` defaults become `Y=None → live_season()`
   only where the result is byte-identical (prove per site; leave a default literal if a caller relies on it).
4. tools/ingest.py SEASON reads season_state (the column id stays `<prefix><slug>-<SEASON>`).

**Must not change.** The board at season_year 2026 (96896e1c), store, config, every historical literal (ruling
dates, frozen anchors, `draft-pick:<class>` labels), the frozen v0-surface signature.

**Prove it.**
- Bare canonical build byte-identical; `tools/harness docs/evidence/walkforward_retro_2026-08-29/pass_asat_seasons.py`
  control passes and the banks are byte-identical; engine/rl_after/one_source_selftest.py; acceptance `--profile full`.
- A 2027 copy (scratch worktree): set season_year/inprog_year 2027, both dials "2027" (recompute config_sha256 and the
  `config` pin there), then a DEV-mode build (`_build_child.py … dev …`) completes; grep its log and the board for a
  2026 that should have been 2027 (a lens year, a `lensYear`, an INPROG halt). Pricing sense is P3-2's rehearsal.
- The lever act: `moves: [engine_head, rl_model]` (+ `fv` if conditional_prior.py changes), board unmoved by prediction.

**Lands via.** Lever act; config unmoved.
