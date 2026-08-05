# #326 rehearsal — exact re-run commands

```
export PATH="/root/rl_venv312/bin:$PATH"
R=/tmp/claude-0/-home-user-afl-rl-engine/52aec7aa-3e34-5a29-a45f-2e2388143230/scratchpad/rehearsal_326
W=/home/claude/rl_workspace/rl_after
E="OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1"
```

## seed the workspace from the rehearsal tree (after every engine-file edit)
```
cd $R && RL_VENDOR=$R/vendor bash $R/bootstrap.sh
```

## canonical board build
```
cd $W && rm -f rl_app_data.json && \
env $E PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation \
  python3 rl_export.py
md5sum rl_app_data.json          # expect 5d1e0709a878e3cff7d7ca24c877e9b4
```

## book + selftest
```
cd $W && env $E PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 s4_matrix_M1v7.py
cd $W && env $E PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 one_source_selftest.py
# expect 114 PASS / 15 FAIL — the 15 are the HALT findings, see HALT_AND_ASK.md
```

## attribution instrument (the committed one, unmodified)
```
python3 $R/docs/evidence/landing_306_648fai/attribute_movers.py \
  <evidence>/baseline_rl_app_data.json <evidence>/rehearsed_rl_app_data.json \
  --ids-base store=f1e8c9fe,engine=15525b03,band=34faa865 \
  --ids-cand store=f1e8c9fe,engine=15525b03,band=34faa865 \
  --json <evidence>/gate7_attribution.json
```

## the population / tier derivation, re-derived from the engine
```
cd $W && env $E PYTHONPATH=$W:/home/claude/rl_vendor \
  RL_CONFIG_MODE=gate RL_REPO=$R RL_FV=$R/engine/forward_valuation \
  python3 <evidence>/derive_pool_population.py
```

## the artifact edit (payload identity asserted unchanged)
```
python3 <evidence>/add_pool_levels.py $R/engine/rl_after/pvc_curve_v2.json
```

## the HALT 2 measurement (two builds, only pool_value differs)
```
# NOT gate mode: RL_V0SURF_REFIT is a declared experiment flag, not a manifest dial.
# RL_LEGF=0 because the sealed entrant total halts on any pool-slot move.
for PV in 237.2 400.0; do
  python3 -c "import json;p='$W/pvc_curve_v2.json';d=json.load(open(p));d['pool_value']=$PV;\
open(p,'w').write(json.dumps(d,indent=1,sort_keys=True)+'\n')"
  cd $W && rm -f rl_app_data.json && env $E PYTHONPATH=$W:/home/claude/rl_vendor \
    RL_V0SURF_REFIT=1 RL_LEGF=0 RL_REPO=$R RL_FV=$R/engine/forward_valuation python3 rl_export.py
done
```
