# P3-1 — One LIVE_SEASON (MEDIUM; board byte-identical)

**Goal.** Every "2026" that means "the season in progress" reads one constant, `season_state.json:season_year`
(already there), through one accessor (engine/rl_after/season_read.py gains `live_season()`); every "2026" that
means a fixed historical fact (a ruling date, a frozen anchor, a draft-class label like `draft-pick:2027`) is
left as a literal with a comment saying which it is.

**Why.** The as-at scout counted the sites that assume 2026: rl_model.py (LIVE_SEASON :74, AGE_REF/BASE_REF
:163, the availability haircuts, `_last_listed<2026`, `_recent_starter` g25/g26, P_estab), _merged_recover.py
(INPROG_Y, the haircut sites, `delisted()`, the D7/O45/O46/O49 guards), conditional_prior.py (EXPO_INPROG_Y,
build_cond_prior cap), rl_export.py (BASE_YEAR, the lens years, `has26`), season_state.py, release_contract.py
(season_year), data/model_config.json (RL_M3_INPROG_Y / RL_EXPO_INPROG_Y pinned "2026"), the UI (card.js
fallback years, finals feed rounds). 589 non-comment "2026" tokens in the engine and tools; most are labels.
Without this the rollover (P3-2) is a 40-site hand edit every November.

**Rules.** Byte-identical board at season_year 2026 (the proof); a build with season_year 2027 on a copy must
RUN (not necessarily price sensibly: that is P3-2's rehearsal) and must not read 2026 anywhere the accessor
should have been used — grep the build log for 2026-literal halts. The `_has26` field is renamed or derived
(`_has26` reads are derived from rows since 2026-10-13; the store field itself can go). The two config pins
`RL_M3_INPROG_Y` / `RL_EXPO_INPROG_Y` become reads of season_state (config identity moves: declare it).

**Proof.** Bare build byte-identical at 2026; the harness control; a 2027-copy build that completes; acceptance.

**Lands via.** Lever act (engine_head, rl_model, fv, config move; board unmoved).
