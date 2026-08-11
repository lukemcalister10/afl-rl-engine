# INSTRUMENTS LANDING INDEX — 2026-08-10

What was landed from the session scratchpad in this act, how it was classified, and — the
point of this file — **every scratchpad file that was NOT landed, and why**. Nothing here is
a value judgement about the work; it is a record so that a later seat looking for a missing
instrument knows whether it was skipped deliberately and on what ground.

Companion to `docs/evidence/ruler_act_2026-08-10/` (PR #400), which established the pattern.

## 1. WHAT WAS LANDED

| set | act | landing comment | files |
|---|---|---|---|
| `ruck_act_instruments_2026-08-10/` | the ruck ceiling act | 5236274192 | 45 |
| `sitter_act_2026-08-10/` | the sitter cross-section (ruling 2.7) | 5235734225 (QC 5235830131) | 7 |
| `pool_design_2026-08-10/` | the pool-design act (ruling 2.5) | 5235784509 | 6 |
| `markup_trace_2026-08-10/` | the mark-up trace (ruling 2.6) | 5235847132 | 22 |
| `probe_3axis_2026-08-10/` | the 3-axis probe (ruling 2.4) | 5235775326 | 11 |
| `audit1_2026-08-10/` | audit 1, the year-0 surface audit | brief 5235093657 | 6 |
| `directive_assembly_2026-08-10/` | the build-seat directive computation | — (assembly act) | 21 |

Each set carries its own README with the act, the landing comment ids, the path conventions,
and an explicit table of which matrices/stores it consumes and where those live.

## 2. HOW FILES WERE CLASSIFIED

By **reading the header comments and path constants of every `.py` landed**, then checking
that the file's inputs and outputs match the claims in the act's own progress file. Filename
prefixes were treated as a hint only, and two prefix guesses in the landing brief turned out
to be wrong:

- **`an1.py … an13.py` are the MARK-UP TRACE, not the sitter act.** All thirteen open
  `decomp_b.json` or `live.json` — the outputs of `decomp.py` and `live.py` — and reproduce
  MARKUP_PROGRESS steps 7-10 in order. The sitter act's instruments are `xsec.py … xsec5.py`,
  identified by the cohort filter in SITTER_PROGRESS step 5 appearing verbatim in all five.
- **The Aug-7 `d1.py d2.py d4.py d56.py` are NOT the ruck act's d-series.** They read
  `pe_stage5.json` / `pe_frozen.json` / `board5.json` through `lib.py`. The ruck d-series is
  the Aug-10 `d1_ceiling.py … d10_allN_check.py` set, every member of which reads
  `ruck_instr_*.json` or `s6_rows.json`.

## 3. WHAT WAS NOT LANDED, AND WHY

### 3.1 Already on main — do not re-land

- **The ruler act's own instruments**, landed at `docs/evidence/ruler_act_2026-08-10/` by
  PR #400: `r1.py r2.py r1_cells.json r2_qual.json r1_peek.py r2_anchors.py r3_leg.py
  r4_six.py r5_six2.py r6_anchor_final.py r7_scale.py r7_scale.json r8_pop.py r9_hurley.py
  r10_tilt.py r10_rows.json r11_cells.py r11_cells.json r12_censor.py r12_censor.txt
  r13_map.py r13_map.json r13_map.txt r14_dip.py r14_dip.txt r15_align.py r16_final.py
  r16_final.json r16_final.txt r17_disclose.py r17_disclose.txt r18_selection.py
  r19_dipsplit.py r20_rate.py r20_rows.json r21_sidebyside.py/.json/.txt r21v22.csv
  r22_level.py r23_onesided.py r24_horizon.py r24_rows.json r25_2x2.py/.json/.txt
  r26_tail.py/.txt r27_xsec.py/.json/.log r28_xsec_tables.py r29_pkl.py
  r30_owner_table.py/.json r31_nodes.py/.json/.txt r32_nodes_true.py/.json r32.log
  r33_owner_true.py/.json r33.log r34_render.py r34_table.txt r35_compare.py/.txt
  r36_dob.py/.txt r36_ages.json r37_ageaxis.py/.json/.txt r38_followup.py/.txt
  RULER_PROGRESS.md`. (The r30/r34 owner tables the assembly act uses are in that set —
  note r30's proj-boundary table is VOID, superseded by r34's true-weight table.)
- `emit_matrix_338.py` — landed at `docs/evidence/noarb_338_2026-08-06/`. `emit.py` is a
  byte-identical duplicate of it under a shorter name; both skipped as duplicates of a landed
  file.
- `gate_export.txt`, `gate_selftest.txt` — the gate artefacts of the DOB-write / G1 acts,
  already landed at `docs/evidence/dob_write_2026-08-10/` and
  `docs/evidence/g1_never_rises_2026-08-10/`.

### 3.2 Not this landing's acts — other acts' instruments, left for their own landings

- **Stage-6 conformance repair**: `teach_g6.py`, `probes_g6.py`, `measure_g6.py`,
  `measure_g6_branch.py`, `g6_table.json`, `teach_repro.txt`, `stage6_README.md`,
  `s6_MEMO.md`, `s6memo.md`, `s6_FRONTIER.txt`, `ladder_seam.py`, `ladder_final.json`,
  `ladder_shipped.json`, `seam_r1.json`, `tab.py`, `show.py`, `gm_rung1.txt`. The 3-axis probe
  reads their conventions and reproduces their output as a control but does not own them.
- **The Aug-7 stage-7 design cluster**: `lib.py`, `lib2.py`, `d1.py`, `d2.py`, `d4.py`,
  `d56.py`, `d1_cells.json`, `d2_qual.json`, `d4_cutlist.json`, `gate.py`, `final.py`,
  `cells.py`, `axis.py`, `calib.py`, `sweep.py`, `repro.py`, `verify_estimand.py`,
  `curve.json`, `predenom.json`, `within_class.json`, `rides_rung1.0.json`,
  `movers_rung1.0.json`, `movers_rung025.json`. **Unclassified in the strict sense**: this
  cluster has no progress file in the scratchpad and no landing-comment id in the brief that
  ordered this act, so I could not name the act it belongs to or cite its landing. Two of its
  members (`r1.py`, `r2.py`) already went out with the ruler set. Flagged for a seat who knows
  which sitting it answers to.
- **Audit 2 and audit 5**: `AUDIT2_PROGRESS.md`, `AUDIT5_PROGRESS.md` — progress files present,
  instruments not separable from the general scratchpad residue with confidence. Left.
- **Other acts with progress files but instruments already landed or out of scope**:
  `DOB_PROGRESS.md`, `G1_PROGRESS.md`, `INGEST_PROGRESS.md`, `TABLES_PROGRESS.md`,
  `RULER_PROGRESS.md` (landed with the ruler set), `COMPOSITION_BUILD_PROGRESS.md` (the live
  build's own file — **actively being written by another seat, must not be copied**).
- `p334_poolleg.py/.json/.out`, `p334_poolmeas.py/.out`, `p334_probe.py`, `x334_games.py/.out`,
  `x334_stage6.py/.out`, `x334_tstat.py/.out`, `legsplit.py/.json`, `legsplit3.py/.json`,
  `m1.py m2.py m3.py m1_board.json m1_rows.json`, `mraz.py`, `mrazchk.py`, `probe_mraz.py`,
  `cohort.py`, `pop.py`, `probe2.py`, `scan.py`, `spotcheck.py`, `quickcheck.py`,
  `board_delta.py`, `build_wb.py`, `explore.py`, `h.py`, `patch_v3.py`, `repin_stage1.py`,
  `calib.py` — Aug-7 pool/leg and stage-2/3 work belonging to earlier landed acts.

### 3.3 Shared INPUTS, not instruments — documented in the set READMEs instead of copied

These are consumed by the landed sets but are matrices/stores/surfaces, not measuring
instruments. Each set's README states the md5 and the branch path where the file lives.
Landing them here would duplicate branch content and blow the size budget.

- Per-entrant matrices, 3.3-3.5 MB each: `matrix.json` `s4a1.json` `stage4a1.json` `pe338.json`
  `matrix_a1.json` (all md5 `b564b12e…`, the stage4_amend1 matrix); `s5.json` `stage5.json`
  `pe_stage5.json` `per_entrant_338_stage5.json` `matrix_s5_landed.json` (all md5
  `bfc104f4…`, the stage-5 landed matrix); `matrix_s5.json`, `matrix_before.json`,
  `pe_frozen.json`, `pe_r0.25/0.5/0.75/1.0.json`, `per_entrant_338_stage5.json`,
  `stage4a1.json`, `s4a1.json`.
- `s6_rows.json` / `s6rows_branch.json` (3.5 MB, md5 `9015cda3…`) — the stage-6 per-row
  emission, input to four of the seven landed sets. **>5 MB rule not invoked; skipped as a
  shared input, not as an oversized file.**
- v0 surfaces: `v0surf_branch.pkl` (`9713ec6c…`), `v0surf_main.pkl`, `v0surf_stageb.pkl`,
  `v0surf_306.pkl`, `v0surf_pre306.pkl`, `v0surf_271.pkl`, `v0surf_f6.pkl`,
  `v0surf_homeclaude.pkl`, `wsb_v0surf.pkl`.
- Boards and rung sweeps: `board5.json`, `board_a1.json`, `board_s5.json`,
  `board_s5_landed.json`, `board_stage3.json`, `b6_0.25/0.5/0.75/1.0.json`,
  `b6r_0.25/1.0.json`, `m6_0.25/0.5/0.75/1.0.json`, `m6r_0.25/1.0.json`, `d13_baseline.json`.
- `pvc2.json` (`73d6f679…`, the board picks curve), `pvc2_main.json`, `basis279.json`,
  `sitout_pop.json`, `sitpop.json`, `qc_base/off/on.json`, `tierA.json`, `tierAGE.json`,
  `tierPOOL.json`, `target175.json`, `found_dobs.json`, `dob_staging.csv`, `ruling.json`,
  `brief.json`, `wb_counts.json`, `wsb_season_state.json`.

### 3.4 Engine and store copies — never land these

`engine.py`, `mr.py`, `mr_a1.py`, `mr_ad50dad.py`, `mr_branch.py`, `mr_landing.py`,
`mr_now.py`, `mr_stageb.py`, `_merged_recover.py.orig`, `_merged_recover_branch.py`,
`_merged_recover_main.py`, `_mr_base.py`, `rl_model.py`, `rlm.py`, `rlm_stageb.py`,
`rl_model_data_branch.json` (1.9 MB store copy). These are working copies of the engine and
its store at various pins, 136 KB - 1.9 MB each. The engine of record is in `engine/`; copies
of it do not belong in `docs/evidence/` at all, at any size.

### 3.5 Registers, memos, transcripts and comment dumps — not instruments

- `register_main.md` (1.5 MB), `reg_main_now.md` (1.5 MB), `register_stageb.md` (1.4 MB) —
  **the only files in the scratchpad that approach the size rule.** Skipped on both grounds:
  they are register transcripts, not instrument outputs, and they are the largest files here.
- `c_5199560650.md … c_5219180436.md` — 41 dumped issue comments. The issue thread is the
  record; a copy in `docs/evidence/` would be a second, forkable copy of it.
- `DIRECTIVE.md`, `COMPOSITION_DIRECTIVE_DRAFT.md`, `DIRECTIVE_SLOT_UPDATES.md`, `MEMO.md`,
  `memo_333.md`, `FRONTIER.txt`, `OWNER_BASIS_COHORT.txt`, `runbook290.md`, `cs_stageb.md`,
  `item279_EVIDENCE.md`, `msg.txt`, `commitmsg.txt`, `s4.txt`, `bootstrap.txt`, `build.txt`,
  `delta.txt`, `delta2.txt`, `stage1_delta.txt`, `repin.txt`, `ext_a1.txt`,
  `final_tables.txt`, `allgrep.txt`, `st_now.txt`, `st_old.txt`, `selftest.txt`,
  `selftest1.txt`, `selftest_raw.txt`, `selftest_before.txt`, `rwm_files.txt`,
  `wsb_files.txt`, `R22.csv`, `movers_a1.csv`, `class2025.html`, `class2025_full.html`,
  `cohort2025.html`, `noarb_before_after.html`, `board_before_after.xlsx`,
  `c334.json`, `c334_all.json`, `build_w0.log`, `server.log` — drafts, notes, renders and
  logs. The directive itself lands through the composition build, not through this act.
- `pen_v622.py … pen_v631.py` — the register-pen scripts of the live composition build. That
  build owns them; this seat does not land another seat's in-flight work.

### 3.6 Regenerable outputs of landed instruments

`inv_players.json` (16 KB) and `inv_surface.json` (116 KB) — written by `a1_scan.py`, which IS
landed, from four inputs whose md5s are recorded in that set's README. Regenerable in seconds.

### 3.7 Environment, harness and throwaway

`env.sh`, `env_v3a.sh`, `env_v3b.sh` (superseded by the `run_*.sh` landed with the ruck set),
`print_c.py`, `extract_comment.py`, `explore.js`, `shots.js`, `tabs.js`, `item_c_rows.err`
(0 bytes), `BRIEF_5236054423.md` (0 bytes), `_all.txt`, `_landed.txt`, `copy_sets.sh`,
`PARALLEL_LANE_PROGRESS.md` (this act's own log), `__pycache__/`.

Directories not traversed for this landing: `ws/`, `ws_b/`, `wsb/`, `rw/`, `rwm/`, `repoB/`,
`repoM/`, `boards/`, `stage2/`, `stage2ef/`, `stage3/`, `stage3b/`, `stage5/`, `noarb/`,
`out_control/`, `out_v1/`, `out_v1f/`, `out_v2/`, `out_v3a/`, `out_v3b/`, `credoff_probe/`,
`fitclass_proof/`, `memo_inputs/`, `evidence/`, `wt-fix/` (another seat's git worktree),
`wt-parallel/` (this act's). These are workspace snapshots and repo clones; the acts that need
them describe how to re-create them in their READMEs.

## 4. SIZE DISCIPLINE

No single landed file exceeds 5 MB. The largest landed file is `ruck_instr_main.json`
(1.3 MB). Total addition ≈ **4.8 MB** against a ~30 MB budget. Three files in the scratchpad
exceed 1.4 MB and were skipped on the grounds recorded in §3.5 (`register_main.md`,
`reg_main_now.md`, `register_stageb.md`); no file was skipped **only** for being large.

## 5. WHAT IS STILL UNCLASSIFIED

The Aug-7 stage-7 design cluster in §3.2 is the one genuine unknown: real instruments, clearly
the product of a completed sitting, but with no progress file and no landing-comment id
available to this seat. It is named here in full so the next seat can land it against its own
act rather than rediscovering it.
