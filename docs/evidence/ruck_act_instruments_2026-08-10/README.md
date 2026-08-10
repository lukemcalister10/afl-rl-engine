# THE RUCK ACT INSTRUMENTS — the original scripts, landed 2026-08-10

The instruments of the ruck-ceiling act (#334 landing comment **5236274192**; the act was
ordered off the mark-up trace, comment 5235847132). Five deliverables: the ceiling bite, the
D2 intervals and eff-n, the D3 era split, the D4 source-switch counterfactual grid, and the
sit-out exposure. Landed from the session scratchpad on the same footing as the ruler act
(PR #400 precedent) — the originals were never in the tree.

## PATH CONVENTION

Every script hard-codes `SP = /tmp/.../scratchpad` (the session scratchpad root) and reads
its inputs from there. The two runner-driven instruments (`ruck_instr_branch.py`,
`ruck_instr_main.py`, and the `ruck_cf*` counterfactuals) are driven by the `run_*.sh`
wrappers, which set:

    RL_WORKDIR   SP/ws_b/rl_after   (branch engine)  |  SP/ws/rl_after   (main engine)
    RL_REPO      /home/claude/seamcheck_landing      |  /home/user/afl-rl-engine
    RL_V0SURF_PKL SP/v0surf_branch.pkl               |  RL_REPO/data/v0surf.pkl
    RL_MATRIX    RL_REPO/docs/evidence/act_334B_2026-08-07/stage4_amend1/noarb/per_entrant_338_stage4a1.json
    RL_VENDOR    /home/claude/rl_vendor    PATH  /root/rl_venv312/bin

`ws/` and `ws_b/` are snapshot workspaces (a copy of `engine/rl_after` with its
`_merged_recover.py` and `rl_model_data.json`); they are NOT landed here. To re-run, re-snapshot
`engine/rl_after` from the pin you want and point `RL_WORKDIR` at it.

## WHAT THIS SET CONSUMES, AND WHERE THOSE LIVE

| input | md5 | where it lives |
|---|---|---|
| `s6_rows.json` (3.6 MB, the stage-6 per-row emission: key/C/Y/N/pos/pk/nd/v0/price/F) | `9015cda31efc25bd471dcc74fdc265fa` | session scratchpad root; byte-identical to `s6rows_branch.json`. Produced by the stage-6 emitter (`emit_matrix_338.py`, landed at `docs/evidence/noarb_338_2026-08-06/`). NOT on main. |
| `per_entrant_338_stage5.json` (stage-5 landed matrix) | `bfc104f4feedab2f006b4b7408bfdc15` | origin branch `landing/334-stage-b` at `docs/evidence/act_334B_2026-08-07/stage5/noarb/per_entrant_338_stage5.json`. NOT on main. |
| `per_entrant_338_stage4a1.json` (stage4_amend1 matrix) | `b564b12e533119f49c2c6bb0c92a5d91` | same branch, `.../stage4_amend1/noarb/`. NOT on main. |
| `v0surf_branch.pkl` (frozen v0 surface, sig `3e8e50de`) | `9713ec6c83270ab916bb4a5e3ded6cb3` | session scratchpad root. |
| live board `data/rl_build/rl_app_data.json` | — | on main, read directly (`d1_live.py`, `find_n7.py`, `board_check*.py`). |

The `.json` outputs of the instrumented runs ARE landed here (`ruck_instr_*.json`,
`ruck_cf*.json`, `ruck_rows_enriched.json`, `d2_intervals.json`, `d2b_cells.json`), so every
downstream d-script in this set is re-runnable with no engine load at all.

## RUN ORDER

`anchor_check.py` FIRST — it is this act's alignment gate. It must reproduce, on
`s6_rows.json`: leg n=414, mark-up (Sprice/Sv0) 1.2288, F1 1.1363; RUCK n=11, mark-up 0.8326,
F1 1.6959. Reproduced EXACT at STEP 1 of RUCK_PROGRESS.md. If it does not, nothing below may
be read. Then `run_branch.sh` / `run_main.sh` (engine runs — the only compute-heavy step), then
the d-series in numeric order.

## KEY FILES

- `anchor_check.py` — the gate (above).
- `ruck_instr_branch.py` + `run_branch.sh` — instrumented BRANCH engine re-run, 649 RUCK
  established-leg rows with e/cpv/v0u/bind/price/price_nc/pole-CF. `ruck_instr_main.py` +
  `run_main.sh` — the same on the LIVE main board.
- `d1_ceiling.py` / `d1_live.py` — D1, the ceiling bite (branch leg: 8 of 379 ND-1-64 ruck rows
  bind, 5,836 pts; live board: 54 rucks, 8 bind, 130 engine-pts / 123 board).
- `d2_interval.py` + `d2b_effn_era.py` (+ `d2_intervals.json`, `d2b_cells.json`) — the B=20,000
  player-resampled and class-clustered intervals and eff-n. Published cell n=11 F1 1.696,
  eff-n 8.19 — FAILS the F8 eff-n>=35 bar. Per-entrant stage-5 LEG RUCK n=54 F1 1.530,
  eff-n 35.87 — PASSES.
- `ruck_cf_branch.py` (CF v1, SUPERSEDED — it missed the W4 `raw_ev` wrapper),
  `ruck_cf2_branch.py` / `ruck_cf2_main.py` / `ruck_cf3_branch.py` — the D4 source-switch
  counterfactual grid v2/v3 (switch-off identity 649/649). `d4_decomp.py`, `d4_decomp2.py`,
  `d4_live.py`, `d5_cf_intervals.py`, `d6_pe_detail.py`, `d7_grid.py` read those outputs.
- `d8_sitout.py` — sit-out exposure (44 pts over 595 rows). `d9_relative.py` — ruck-vs-leg
  relative intervals.
- `d10_allN_check.py` — the estimand-validity check. **This is the one that bounds the act:**
  F compounds forward at 1.0939^(N-4) past N=4, leg F1 reaches 6.23 at N=12, so all-N pooling
  is NOT a lawful estimand. The act's reads are valid for N<=3 only.
- `diag_pole.py`, `find_n7.py`, `verify_repro.py`, `peek.py`, `ruck_rows.py`, `ruck_leg11.py`,
  `board_check.py`, `board_check2.py` — diagnostics and shape probes kept for provenance.
- `RUCK_PROGRESS.md` — the act's own step log (STEP 0 through STEP 7).

## CAVEAT CARRIED FORWARD

These scripts pre-date the 2026-08-10 sitting that set the F8 evidence bar at PLAYER UNIT.
Any re-run for a restatement applies the player-unit bar on top. The published n=11 cell was
already failing eff-n before that change.

## NAMING TRAP (recorded so it is not re-made)

The Aug-7 scratchpad files `d1.py`, `d2.py`, `d4.py`, `d56.py` are **not** part of this
d-series. They read `pe_stage5.json` / `pe_frozen.json` / `board5.json` through `lib.py` and
belong to the earlier stage-7 design cluster. This act's d-series is the Aug-10 `d1_ceiling.py
… d10_allN_check.py` set, every member of which reads `ruck_instr_*.json` or `s6_rows.json`.
