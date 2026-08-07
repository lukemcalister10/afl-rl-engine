# How to reproduce the stage-5 board — the product IS committed

Stage 5 LANDED on the consistency pass, so the engine change, the taught table, the manifest entry and the
board are all on this branch. This file is the re-run recipe; `engine_sitout_ev.patch` is retained as a
readable diff of the one engine file that moved.

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add --detach /home/claude/s5_landing <this commit>
S5=/home/claude/s5_landing/docs/evidence/act_334B_2026-08-07/stage5

# the engine change, g5_table.json (md5 1bd109cb0b428ed91c1988c0c72d4000) and the manifest entry
# RL_G5_W=1.0 are ALREADY in the checkout. `python3 config_manifest.py check` prints PASS (62 vars).

RL_VENDOR=/home/claude/rl_vendor bash /home/claude/s5_landing/bootstrap.sh   # Guard 5, seeds the workspace

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=<workspace>/rl_after:/home/claude/rl_vendor
export RL_CONFIG_MODE=gate
export RL_REPO=/home/claude/s5_landing
export RL_FV=$RL_REPO/engine/forward_valuation

cd <workspace>/rl_after
rm -f rl_app_data.json
python3 rl_export.py          # PARITY + NUMÉRAIRE + FUT-LABEL + ZERO-EMPTY-CLUB; board -> 13f8c2e0240600733a5fb42414510445
python3 s4_matrix_M1v7.py     # BOOK<->BOARD PARITY GATE
python3 one_source_selftest.py                        # PASSED, 143 / 0
```

Then, in a **dev shell** (`unset RL_CONFIG_MODE`, `RL_WORKDIR=<workspace>/rl_after`,
`RL_VENDOR=/home/claude/rl_vendor`, `RL_OUT=$S5`):

```bash
# the teach, from the FROZEN baseline matrix (never re-emitted for teaching)
python3 $S5/measure_surface.py          # -> s5_rows.json, the raw per-row measurement
python3 $S5/teach_g5_consistency.py     # -> g5_table_LANDED.json  md5 1bd109cb0b428ed91c1988c0c72d4000
python3 $S5/consistency_verify.py       # proves the fixed point prices each cell at its own F

# the tracking + the gates
git -C $RL_REPO show c05f214:data/rl_build/rl_app_data.json > /tmp/board_base.json
RL_NEWBOARD=13f8c2e0 python3 $S5/enumerate_movers.py      /tmp/board_base.json <workspace>/rl_after/rl_app_data.json
RL_NEWBOARD=13f8c2e0 python3 $S5/near_projection_proof.py /tmp/board_base.json <workspace>/rl_after/rl_app_data.json
RL_TAG=stage5        python3 $S5/probes.py
python3 $S5/precheck_mraz.py
python3 $S5/rides.py ; python3 $S5/convergence.py ; python3 $S5/within_class.py ; python3 $S5/owner_basis.py
RL_OLDBOARD=/tmp/board_base.json RL_NEWBOARDFILE=<workspace>/rl_after/rl_app_data.json python3 $S5/below_own_pick.py
python3 $S5/frontier.py ; python3 $S5/landing_decomp.py

# the measurement chain
cd $S5/noarb && RL_OUT=$S5/noarb python3 emit_matrix_338.py
mv per_entrant_338_confirmation.json per_entrant_338_stage5.json      # md5 bfc104f4feedab2f006b4b7408bfdc15
python3 noarb_table_338.py per_entrant_338_stage5.json ; python3 noarb_ext_338.py ; python3 goal_metrics.py
cd $S5 && python3 ladder_seam.py                                     # gate 7

# the dial-0 identity, through the full gate (flips the manifest, restores it, md5-verified on the way out)
python3 $S5/killswitch_check.py       # -> board b56bbdde byte-exact

# the fit-coupling proof (declared experiment, so NO RL_CONFIG_MODE)
for W in 0 1.0 2.0; do RL_G5_W=$W RL_V0SURF_REFIT=1 \
  python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify; done

# the owner review set — the SIXTH stage column
python3 $S5/../side_by_side/build_xlsx.py && python3 $S5/../side_by_side/verify_xlsx.py

# the diagnostic that prices the aging law (NEVER installed; see CONSISTENCY_PASS.md section 3)
RL_G5_NOCAP=1 python3 $S5/teach_g5_consistency.py   # -> g5_table_NOCAP_DIAGNOSTIC.json
```

**One warning about the teach.** `teach_g5.py` reads `RL_OUT/s5_rows.json`, which `measure_surface.py`
writes, and `measure_surface.py` asserts the teaching matrix md5 is `b564b12e533119f49c2c6bb0c92a5d91`
and halts otherwise. That assert is deliberate: the surface must be taught from the FROZEN baseline book
and from nothing else. Teaching it from the post-change book would be the fixed point the directive bans.
