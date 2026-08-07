# How to reproduce stage 6 — the product IS committed

The engine change, the taught table `engine/rl_after/g6_table.json`, the manifest entries
`RL_G6_W=0` / `RL_G6_KPD=0` and the re-stamped `config` / `engine_head` pins are all on this branch.
The **shipped board does not move**: it is still the stage-5 landing `13f8c2e0`.

```bash
export PATH=/root/rl_venv312/bin:$PATH
git worktree add --detach <worktree> <this commit>
REPO=<worktree>
S6=$REPO/docs/evidence/act_334B_2026-08-07/stage6

RL_VENDOR=/home/claude/rl_vendor bash $REPO/bootstrap.sh    # Guard 5 + ENV PIN; seeds /home/claude/rl_workspace
cp -a /home/claude/rl_workspace <ws>

export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH=<ws>/rl_after:/home/claude/rl_vendor
export RL_REPO=$REPO
export RL_FV=$RL_REPO/engine/forward_valuation
```

## 1 · the SHIPPED build (gate mode) — must reproduce the stage-5 landing byte-exact

```bash
export RL_CONFIG_MODE=gate
cd <ws>/rl_after
rm -f rl_app_data.json
python3 rl_export.py          # config manifest 64 vars, hash 697da6f8 ; PARITY / NUMÉRAIRE / FUT-LABEL / ZERO-EMPTY-CLUB
md5sum rl_app_data.json       # -> 13f8c2e0240600733a5fb42414510445
python3 s4_matrix_M1v7.py     # BOOK<->BOARD PARITY GATE
python3 one_source_selftest.py                        # PASSED, 143 / 0
```

## 2 · the teach — from the FROZEN matrix, never re-emitted for teaching

Dev shell (`unset RL_CONFIG_MODE`, `RL_WORKDIR=<ws>/rl_after`, `RL_VENDOR=/home/claude/rl_vendor`,
`RL_OUT=$S6`), run from `<ws>/rl_after`:

```bash
python3 $S6/measure_g6.py     # -> s6_rows.json ; asserts the teaching matrix md5 b564b12e and HALTS otherwise
python3 $S6/axis_probe.py     # the demonstrated-level axis choice, printed
python3 $S6/teach_g6.py       # -> g6_table.json  md5 5656dd8bbb19b193e1acde5063664cc5  (+ teach_log.txt)
```

`measure_g6.py` asserts `b564b12e533119f49c2c6bb0c92a5d91`. That assert is deliberate: the surface
must be taught from the frozen baseline book and from nothing else. Teaching it from a post-change
book is the fixed point the directive bans.

## 3 · the four rungs — each through the FULL gated build

`RL_G6_W` is a manifest dial, so an ambient `RL_G6_W=0.5` proves nothing in gate mode. `rung_build.py`
flips the manifest, re-stamps `config_sha256` + `expected_boot 'config'` exactly as a bake would, runs
the real gated build, copies the board out, and restores every file it touched (md5-verified).

```bash
for W in 0.25 0.5 0.75 1.0; do python3 $S6/rung_build.py $W; done
#   0.25 -> e5fee49bb9dc553ddbaf55143bd03742      0.75 -> b963e36a8423470ecfdc1f3e5e691806
#   0.5  -> 56b6c21cec6fccdeb3711ccd9981fac1      1.0  -> 17c96ca4add0fd49609ed8fd5009a641
```

## 4 · the walk-forward matrices, one per rung (dev shell, RL_G6_W ambient; the emitter is read-only)

```bash
cd $S6/noarb
for W in 0.25 0.5 0.75 1.0; do
  RL_G6_W=$W RL_G6_KPD=0 RL_OUT=$S6/noarb python3 emit_matrix_338.py
  mv per_entrant_338_confirmation.json per_entrant_338_rung$W.json
done
#   0.25 -> 2eff80a4bbf9031ae8e25e54ef9b63be      0.75 -> 22402f35c41e306bb4fbeb3d2c2302e3
#   0.5  -> 8553acf07bffd5570bc6d8b4e76c9f5a      1.0  -> ca6cd25d725a22b74afe775d7b044c04

for W in 0.25 0.5 0.75 1.0; do
  RL_RUNG=$W python3 noarb_table_338.py per_entrant_338_rung$W.json > noarb_table_rung$W.txt
  mv noarb_table_338.json noarb_table_rung$W.json
  RL_RUNG=$W python3 noarb_ext_338.py   > noarb_ext_rung$W.txt
  RL_RUNG=$W python3 goal_metrics.py    > goal_metrics_rung$W.txt
done
```

## 5 · the gates

```bash
# movers + THE FENCE (one process per rung: a second exec of the engine corrupts the fv caches)
for W in 0.25 0.5 0.75 1.0; do python3 $S6/enumerate_movers.py $W; done

python3 $S6/owner_basis.py                      # the four-rung landing on BOTH bases
for W in 0.25 0.5 0.75 1.0; do python3 $S6/rides.py $W; done
for W in 0.25 0.5 0.75 1.0; do python3 $S6/ladder_seam.py $W; done
python3 $S6/probes_g6.py                        # fence, Mraz/Nairn, recalculation, rollover, fade,
                                                # zero cells, monotonicity, KPD/KPF pair, tail-vs-typical
python3 $S6/within_class.py                     # within-class continuity + convergence

# the dial-0 identity, through the full gate, INCLUDING the structural claim
python3 $S6/killswitch_check.py                 # -> 13f8c2e0 byte-exact, table moved aside, still byte-exact

# fit coupling (declared experiment, so NO RL_CONFIG_MODE) — run from <ws>/rl_after
for W in 0 0.5 1.0; do RL_G6_W=$W RL_V0SURF_REFIT=1 \
  python3 $RL_REPO/session_2026-07-18/legf6/scripts/refit_v0surf.py --verify; done

# the owner review set — the SEVENTH stage column + the `stage 6 rungs` sheet
python3 $S6/../side_by_side/build_xlsx.py && python3 $S6/../side_by_side/verify_xlsx.py
```

## Notes that have burned this build

* **Re-exec'ing `_merged_recover.py` more than once in a single process** blows the recursion limit
  inside `forward_valuation` (process-level caches). Either run one rung per process
  (`enumerate_movers.py`) or exec once and rebind the module globals `G6_W` / `G6_KPD`
  (`probes_g6.py`) — never both.
* `rung_build.py` leaves the LAST rung's board in the workspace. Re-run the shipped build before the
  self-test, or F1/F2 will fail against a rung board.
* The teach's declared boundaries (`RL_G6_PKLO`/`RL_G6_PKHI`/`RL_G6_AGELO`/`RL_G6_AGEHI`) exist so
  the endpoint sweep is re-runnable. The SHIPPED values are the defaults in `teach_g6.py`; they were
  fixed once, from the printed sweep, and were **not** re-picked afterwards.
