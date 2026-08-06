# #326 second rehearsal — exact re-run commands

```
export PATH="/root/rl_venv312/bin:$PATH"
R=/tmp/claude-0/-home-user-afl-rl-engine/52aec7aa-3e34-5a29-a45f-2e2388143230/scratchpad/rehearsal_326
E=/tmp/claude-0/-home-user-afl-rl-engine/52aec7aa-3e34-5a29-a45f-2e2388143230/scratchpad/rehearsal_326b_evidence
W=/home/claude/rl_workspace/rl_after
ENV="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
```

## seed the workspace (after every engine-file edit)
```
cd $R && RL_VENDOR=$R/vendor bash $R/bootstrap.sh
```

## the board
```
cd $W && rm -f rl_app_data.json && \
env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 rl_export.py
md5sum rl_app_data.json          # expect 864b6726a4612b0d8afe57f230421514
```

## the book, then the selftest
```
cd $W && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 s4_matrix_M1v7.py
cd $W && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 one_source_selftest.py
# expect 145 PASS / 0 FAIL  (~80s; section (10) is the #326 block)
```

## attribution — the engine's own pool classification
```
cd $W && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 $E/classify_movers.py $E
```

## the committed instrument, unmodified, with TRUTHFUL identities (HALTS — see HALT_AND_ASK.md #2)
```
python3 $R/docs/evidence/landing_306_648fai/attribute_movers.py \
  $E/baseline_rl_app_data.json $E/rehearsed_rl_app_data.json \
  --ids-base store=f1e8c9fe,engine=15525b03,band=34faa865 \
  --ids-cand store=f1e8c9fe,engine=9f258a3b,band=34faa865
```

## the frozen surface, by the committed probe
```
cd $W && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation \
  python3 $R/docs/evidence/landing_306_648fai/v0surf_signature_probe.py "#326 rehearsed engine"
```

## the re-scoped B5 block (ship_gates_check.py itself cannot run — HALT_AND_ASK.md #3)
```
cd $W && env $ENV PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 $E/b5_rescope_probe.py
```

## the artifact edit and the identity re-pins (idempotent scripts, already applied)
```
python3 $E/add_pool_levels.py $R/engine/rl_after/pvc_curve_v2.json    # payload identity asserted unmoved
python3 $E/repin.py engines
python3 $E/repin.py board <board md5>
python3 $E/repin.py contract_md5
python3 $R/ui/tools/extract_board_view.py                            # the two UI board bundles
```

## the RED proofs (each edits one thing, runs, then restores)
| RED | break | expected |
|---|---|---|
| wrong level | `pool_levels.signed_flat.MSD = 300.0` in the artifact | selftest red on the signed table + 33 parity mismatches (`gate3a_wrong_level_RED.txt`) |
| wrong field | `pool_levels.rd_position_field = present_position` | build HALTS naming 171 rows (`gate5_wrongfield_build_RED.txt`) |
| currency, engine site | `entry_anchor` drops the `*_PL_F` | build HALTS on the isolation assert (`gate3b_currency_engine_site_RED.txt`) |
| currency, ladder site | `_cap_basis` adds a `*_PL_F` | build HALTS the same way (`gate3c_currency_ladder_site_RED.txt`) |
| currency, at the SITE | the floor divides `_PL_F` back out | selftest red on the end-to-end board check (`gate3d_currency_site_RED.txt`) |
| silent refit | `RL_V0SURF_REFIT=1` (outside gate mode) | build HALTS on the no-silent-refit assert (`gate7_nosilentrefit_RED.txt`) |
| isolation | `_cap_basis` returns `draftval` for pool rows | selftest red, structural AND measured (`gate3e_isolation_RED.txt`); this build is also `buildB_no_ruckcap_rebase.json`, which enumerates the ruck-cap route |

Nothing here was pushed or committed. `cd $R && git status` shows the whole change set; `git diff` is
captured as `rehearsal_326b.patch`.
