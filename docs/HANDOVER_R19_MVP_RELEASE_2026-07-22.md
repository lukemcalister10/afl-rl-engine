# Round 19 MVP release handover

## Factual claims

1. `docs/HANDOVER_CHANGED_FILES_2026-07-22.txt` contains the output of `git diff --name-only 612d4c058560568b3d4d49ecd785759931885081..HEAD` and lists 737 changed paths.
2. `docs/HANDOVER_R19_MVP_RELEASE_2026-07-22.md` is this handover note.
3. Tag `v2.11-r19-mvp` points to commit `6c47f032f88e0a1c36b9330e98c347d34523576a`.
4. Branch `checkpoint/r19-mvp-baseline` points to commit `6c47f032f88e0a1c36b9330e98c347d34523576a`.
5. Pull request `#135` merged head `a2945f61c0d6ba1182ccd2d7da2dcd34f65bf11e` into `integration/v2.11-final-rc` as commit `6c47f032f88e0a1c36b9330e98c347d34523576a`.
6. `data/expected_boot.json` identifies Round 19, board `6f07f7cbe042f8e56426a01226c967c9`, engine `7c452715dc98ac42723834d08021e9d2`, store `f37d9716648cfe4382b8c6a24c4f064f`, config `45b207c03a8cf2e449d831d54c19f848ace1b7c87dd699305048dccbe05d2140`, and forward-valuation source set `6a9a520fa2f8b4051e889d324d905cff0a37e592232cd5e68f0e0d9bdfeeec35`.
7. The GitHub release for `v2.11-r19-mvp` contains a standalone HTML file, a portable ZIP, a release manifest, SHA-256 sums, and source archives.
8. `.github/workflows/ci-guards.yml` runs repository guard checks and contains assumptions that do not match the released Round 19 store and board.
9. `.github/workflows/final-integration.yml` runs config, release-state, season-state, invariant, UI, rebuild, R15, R14-R19, and updater checks.
10. `.github/workflows/fv-provenance.yml` runs the forward-valuation provenance red/green suite.
11. `.github/workflows/live-scoring.yml` runs score-ingestion, catch-up, transaction, finalization, Movers, store-write, and forward-valuation provenance proofs on scratch repositories.
12. The four workflows in claims 8-11 fail on the released commit because their fixtures or oracles retain pre-R19 assumptions, and the owner waiver is recorded on pull request `#135` and merge commit `6c47f032f88e0a1c36b9330e98c347d34523576a`.
13. `FIRST_COMMANDS_PROOF.txt`: changed, reason unknown to this session.
14. `PANEL_EXPECTED.txt` contains the panel identities and values read by the panel workflow.
15. `boot_guard.py` checks the store, engine, forward-valuation source set, config, fitted artifacts, register, and board identities against repository pins.
16. `bootstrap.sh` creates or seeds the engine workspace, uses `RL_VENV` when supplied, and runs boot checks.
17. `bootstrap_env.sh` provisions the Python environment used by repository workflows.
18. `config_manifest.py` reads, hashes, and checks the model configuration manifest.
19. `fv_provenance.py` resolves the forward-valuation directory and checks the imported source-set identity.
20. `release_contract.py` checks release identities and season metadata and can halt on mismatches.
21. `season_state.py` derives calendar progress and exposure pace from round and store data.
22. `requirements-lock.txt` records the Python package versions used for the pinned environment.
23. `run_panel.sh` runs the panel against the pinned release state.
24. `ship_gates_check.py` runs the repository ship-gate checks and writes gate evidence.
25. `verify_restore.sh` checks restored repository files and identities.
26. `data/book_stable_seal.json` stores the cohort-book seal and source identities.
27. `data/gates_snapshots/gates_40f43772.json`, `data/gates_snapshots/gates_a83c9f6d.json`, and `data/gates_snapshots/gates_bea8fea8.json` store gate snapshots for their named board or engine identities.
28. `data/model_config.json` stores the configuration variables and season-state policy identifier used by release checks.
29. `data/release_contract.json` stores the release contract, board/store/engine identities, and season metadata.
30. `data/release_lineage.json` stores release-lineage references.
31. `data/rl_build/rl_app_data.json` is the Round 19 board file for board `6f07f7cbe042f8e56426a01226c967c9`.
32. `data/rl_build/rl_app_data.json.srcmd5` stores the source-store stamp for `data/rl_build/rl_app_data.json`.
33. `data/season_state.json` stores the Round 19 season-state values read by the engine and release contract.
34. `data/v0surf.pkl` is a fitted valuation artifact loaded by the engine and pinned in `data/expected_boot.json`.
35. `docs/OPEN_ITEMS_REGISTER.md` contains item 406, which links the post-release Movers work in issue `#138` and the UI, public-view, pick-policy, future-lens, and operating work in issue `#139`.
36. `docs/RECOVERY_STATE_2026-07-20.md` records the recovery branch and artifact state used for the v2.11 recovery process.
37. `docs/RELEASE_ARTIFACT_MAP_v2_11.md` maps v2.11 release artifacts and identities.
38. `docs/RELEASE_CANDIDATE_v2_11.md` describes the v2.11 release-candidate state and boundaries.
39. `docs/GO_LIVE_round_score_ingestion.md` describes the owner-facing score-ingestion go-live procedure and gate state.
40. `docs/**` paths in `docs/HANDOVER_CHANGED_FILES_2026-07-22.txt` that are not named in claims 1-2 and 35-39: changed, reason unknown to this session.
41. `engine/forward_valuation/build_cohort_book.py`, `engine/forward_valuation/build_peak_model_v4.py`, `engine/forward_valuation/conditional_prior.py`, `engine/forward_valuation/dist_redesign.py`, `engine/forward_valuation/distribution_pricing.py`, `engine/forward_valuation/par_build.py`, and `engine/forward_valuation/par_redesign.py` form the imported forward-valuation source set checked by `fv_provenance.py`.
42. `engine/rl_after/_merged_recover.py` contains the valuation implementation used to build the released board, including the present-board graded-staleness treatment.
43. `engine/rl_after/_ov_angleA.py`: changed, reason unknown to this session.
44. `engine/rl_after/rl_model.py` exposes the valuation model and reads the season-state values used by the current-year calculation.
45. `engine/rl_after/rl_export.py` writes present, prior-year, +1, and +2 board views and applies the existing future-value floor.
46. `engine/rl_after/single_source.py` defines the single-source file set, source stamps, and lookalike checks.
47. `engine/rl_after/one_source_selftest.py` checks boot identity, source stamps, board-to-engine parity, book-to-board parity, data assertions, position assertions, and pick-curve assertions.
48. `engine/rl_after/pvc_curve_v2.json` stores the adopted draft-pick curve with pick 1 set to 3,000.
49. `engine/rl_after/wire_redesign.py`: changed, reason unknown to this session.
50. `engine/rl_after/rl_model_data.json` is the store with MD5 `f37d9716648cfe4382b8c6a24c4f064f`, 804 active players, identity and position fields, AFFL ownership fields, and Round 15-Round 19 scoring entries.
51. `engine/rl_after/ingestion/.weekly_txn/txn_catchup_r15/**` through `engine/rl_after/ingestion/.weekly_txn/txn_catchup_r19/**` contain the transaction manifests and journals for the five applied rounds.
52. `engine/rl_after/ingestion/applied_rounds_ledger.json` contains 1,858 applied player-round entries across R15-R19.
53. `engine/rl_after/ingestion/finalization_state.json` and `engine/rl_after/ingestion/finalization_journal.jsonl` store finalization state and finalization events for the applied rounds.
54. `engine/rl_after/ingestion/value_history.json`, `engine/rl_after/ingestion/rank_history.json`, and `engine/rl_after/ingestion/pos_rank_history.json` contain R14-R19 value, overall-rank, and positional-rank histories generated before the present-board staleness change.
55. `engine/rl_after/ingestion/movers/movers_R15.csv` through `movers_R19.csv` and `engine/rl_after/ingestion/movers/movers_R15.json` through `movers_R19.json` contain the pre-staleness-change Movers reports.
56. `engine/rl_after/ingestion/round_apply.py`, `round_catchup.py`, `round_entry.py`, `round_finalize.py`, `round_history.py`, `round_movers.py`, and `staged_apply.py` implement preview, application, catch-up, finalization, history, Movers generation, and staged transactions.
57. `engine/rl_after/ingestion/score_ingestor.py` parses and validates score updates and requires both apply-gate halves before a store write.
58. `engine/rl_after/ingestion/footywire_parser.py` parses FootyWire score input into the ingestion format.
59. `engine/rl_after/ingestion/scratch_fixture.py`, `round_entry_fixture_proof.py`, `test_catchup_preflight.py`, `test_weekly_updater.py`, and `dry_run_proof.py` provide scratch fixtures and ingestion proofs.
60. `engine/rl_after/ingestion/README.md`, `engine/rl_after/ingestion/PROOF.md`, `engine/rl_after/ingestion/proof.json`, `engine/rl_after/ingestion/__init__.py`, and `engine/rl_after/ingestion/catchup_identity_overrides.json` document and expose the ingestion package and its catch-up identity mappings.
61. `session_2026-07-02/**`: changed, reason unknown to this session.
62. `session_2026-07-16/**`: changed, reason unknown to this session.
63. `session_2026-07-17/base_guard/**`, `session_2026-07-17/legc_relay/**`, `session_2026-07-17/legd_derivation/**`, `session_2026-07-17/r1067_wiring/**`, `session_2026-07-17/round_entry_tool/**`, and `session_2026-07-17/viewing_pack/**`: changed, reason unknown to this session.
64. `session_2026-07-18/five_migration/**`, `session_2026-07-18/lege/**`, `session_2026-07-18/legf1/**`, `session_2026-07-18/legf3/**`, `session_2026-07-18/legf4/**`, `session_2026-07-18/legf5/**`, and `session_2026-07-18/legf6/**`: changed, reason unknown to this session.
65. `session_2026-07-19/envpin/**` contains environment-pin plans, scripts, logs, board comparisons, and wheel checks.
66. `session_2026-07-19/storewrite/**` contains the store-write proof, proof output, and instructions for scratch writes.
67. `session_2026-07-20/fv_provenance_remediation/**` contains the forward-valuation provenance remediation description, results, fixtures, reference vector, and test suite.
68. `session_2026-07-20/live_scoring_catchup/**` contains the R15-R19 catch-up proof, score fixtures, pre-correction Movers reports, Movers bundle generator, and proof output.
69. `session_2026-07-20/live_scoring_two_round/**` contains the two-round updater proof and its child process and output files.
70. `session_2026-07-20/ui_release_seam/**` contains board, club, held-pick, public-view, responsive-layout, and release-seam evidence.
71. `session_2026-07-20/weekly_updater_hardening/**` contains transaction failure-injection, finalization failure-injection, release-metadata, and forward-valuation provenance proofs.
72. `session_2026-07-21/final_integration/**` contains the final-integration report, test scripts, tools, JSON evidence, and browser screenshots.
73. `session_2026-07-21/r19_mvp/BROWSER_RESULT.json` records the Round 19 MVP browser result.
74. `session_2026-07-22/present_board_correction/source_patch.json` records the source patch used for the present-board staleness change.
75. `session_2026-07-22/present_board_correction/summary.json` records the 18 present-rating changes, 786 unchanged present ratings, total change of 5,181, board identity, engine identity, and store identity.
76. `tools/round_entry/README.md`, `tools/round_entry/round_entry.py`, `tools/round_entry/samples/round_entry.out.txt`, `tools/round_entry/weekly_update.bat`, and `tools/round_entry/weekly_update.sh` provide the owner-facing round-entry wrapper and sample output.
77. `tools/seat/README.md`, `tools/seat/first_commands.sh`, `tools/seat/prescreen.sh`, and `tools/seat/viewing_pack.py` provide base-prescreen and viewing-pack commands.
78. `ui/app/board.js` renders the rankings table, working/public view selection, filters, and player selection behavior.
79. `ui/app/clubs.js` renders club totals, club comparisons, held picks, and club rosters.
80. `ui/app/config.js` stores UI release and display configuration.
81. `ui/app/main.js` routes the Board, Clubs, Player Card, Trade Desk, Round Review, and Movers surfaces.
82. `ui/app/movers.js` checks Movers report lineage and renders Movers only when the report board matches the loaded board.
83. `ui/app/positions_data.js` stores the generated position mapping used by the UI.
84. `ui/app/seam.js` checks UI data seams and release identities.
85. `ui/data/board_view_working.js` and `ui/data/board_view_public.js` contain the released working and public board bundles for board `6f07f7cbe042f8e56426a01226c967c9`.
86. `ui/data/club_valuation.js` contains 16 AFFL club summaries and 160 held picks and currently includes picks 65-80 in pick counts and values.
87. `ui/data/movers.js` contains the pre-staleness-change Movers chain whose latest board identity is `92a8f3a0...`.
88. `ui/index.html` loads the board, club, position, Movers, app, and style bundles.
89. `ui/release_pick_curve.json` records the pick-curve provenance and current release identity used by club-value ingestion.
90. `ui/screenshots/movers_desktop.png`, `ui/screenshots/movers_empty.png`, and `ui/screenshots/movers_mobile.png` are Movers UI screenshots.
91. `ui/styles/matchday.css` defines the released UI layout and responsive styles.
92. `ui/tests/club_curve_provenance.test.py`, `extract_seam.test.py`, `movers.test.js`, `release_seam.test.js`, `responsive_layout.test.mjs`, and `test_club_valuation_current.py` test club-curve provenance, extraction, Movers behavior, release seams, responsive layout, and club totals.
93. `ui/tools/extract_board_view.py`, `ui/tools/extract_positions.py`, `ui/tools/ingest_inputs.py`, and `ui/tools/movers_ui_check.mjs` generate or check the board, position, club, and Movers UI bundles.
94. Branch `model/r19-staleness-graded` contains the first graded-staleness candidate and is not merged into the release.
95. Branch `model/r19-staleness-graded-anchor-fix` contains the future-lens evidence-anchor diagnostic and is not merged into the release.
96. Branch `archive/r19-ui-forward-lens-work-2026-07-22` preserves UI and future-lens notes and is not merged into the release.
97. Pull requests `#136` and `#137` are closed without merge.
98. The option to display the old Movers report by weakening or changing the board-lineage check was not implemented.
99. The one-shot register, release, and file-census workflows were removed from `main` after their repository writes.
100. Issue `#138` is open and specifies the R14-R19 history and Movers rebuild under engine `7c452715dc98ac42723834d08021e9d2`.
101. Issue `#139` is open and specifies the UI, public-view, pick-policy, future-lens, and operating backlog.

## Not built or not working

102. The released Movers tab is not working because `ui/data/movers.js` names board `92a8f3a0...` and `ui/data/board_view_working.js` names board `6f07f7cb...`.
103. The R14-R19 value, rank, positional-rank, and Movers chain has not been rebuilt under engine `7c452715dc98ac42723834d08021e9d2`.
104. The Round Review tab remains separate from Movers and retains placeholder or overlapping behavior.
105. Weekly rating, value, rank, score, and played/DNP movement is not displayed on player cards.
106. Movers does not provide separate base-round and comparison-round selectors for R14 through the latest round.
107. `Free agents` and `Free Agents` remain separate display categories, including Liam Stocker and Tyler Brockman in the second category.
108. Current-season dual-position eligibility is not displayed as a separate user-facing position concept.
109. Player cards do not display drafted position, development position, current-season model position, current-season eligibility, future position, and future positional split as separate fields.
110. Picks 65-80 remain included in `ui/data/club_valuation.js` pick counts, pick values, overall club values, and club rankings.
111. The public rankings view does not display AFFL team ownership information.
112. The club positional-value breakdown is not available as a persistent page or table view.
113. Club pages do not show the comparison-page summary before the player list.
114. Clicking a club in the public view returns to the all-player list instead of the selected club profile.
115. The Board tab is not named `AFFL Rankings`.
116. The tab subtitle does not change to `Player Rankings`, `Club Breakdown`, `Player Profiles`, `Trade Desk`, or `Weekly Review` according to the active surface.
117. Back navigation is not a universal previous-page control across player and club routes.
118. Clicking a player in the public rankings view does not open the player profile.
119. Public player cards do not show the Recent Form section.
120. Public player cards do not show the same draft-pick and rank-denominator information requested for working/public parity.
121. The +1 and +2 lenses retain the evidence-year defect in which future evaluation years can have no scoring rows.
122. The +1 and +2 lenses retain the shared Leg-F floor that can produce the same value in both horizons.
123. A full disposable Round 20 run through apply, board generation, histories, finalization, Movers, club totals, and browser output has not been completed.
124. Direct Python finalization does not own the club-total refresh performed by `tools/round_entry/weekly_update.sh`.
125. iPhone Safari hardware behavior has not been verified.
126. A hosted public website has not been built or deployed.
127. The four release workflows have not been migrated from their pre-R19 fixtures and oracles.
128. Score writing remains disabled because `APPLY_DEFAULT` is false and the two apply environment variables are not enabled.
129. The fifth-round-pick exclusion exists only in the separate spreadsheet analysis and is not applied to the released UI or data bundle.
130. No change from issues `#138` or `#139` is included in tag `v2.11-r19-mvp` unless the change is separately named in claims 1-101.

Branch: `docs/handover-r19-mvp-release-2026-07-22`

Final commit SHA: `6c47f032f88e0a1c36b9330e98c347d34523576a`
