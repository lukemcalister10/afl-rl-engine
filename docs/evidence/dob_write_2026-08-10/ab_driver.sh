#!/bin/bash
# DIAGNOSTIC A/B — how far does the DOB write move real prices?
# Nothing here is committed and no repo file is written. The v0surf refit is DECLARED
# (RL_V0SURF_REFIT=1), matching the sanctioned refit lane in
# session_2026-07-18/legf6/scripts/refit_v0surf.py, which also runs outside gate mode.
#   A = old store, frozen surface, no gate mode   -> control, must reproduce 6e724cca
#   B = old store, DECLARED refit                 -> isolates the cost of refitting alone
#   C = written store, DECLARED refit             -> B vs C isolates the DOB write
set -uo pipefail
WS=/home/claude/dob_ws/rl_after
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

run () {  # $1 repo  $2 label  $3 refit(0|1)
  local REPO="$1" LABEL="$2" REFIT="$3"
  cd "$REPO"
  RL_VENV=/root/rl_venv312 bash "$REPO/dob_bootstrap.sh" > /home/claude/ab_${LABEL}_boot.log 2>&1
  export RL_REPO="$REPO"
  export RL_FV="$REPO/engine/forward_valuation"
  export PYTHONPATH="$WS:/home/claude/rl_vendor"
  unset RL_CONFIG_MODE
  if [ "$REFIT" = "1" ]; then export RL_V0SURF_REFIT=1; else unset RL_V0SURF_REFIT; fi
  cd "$WS"
  echo "=== $LABEL : store $(md5sum rl_model_data.json | cut -c1-8) refit=$REFIT"
  rm -f rl_app_data.json rl_app_data.json.srcmd5
  python3 rl_export.py > /home/claude/ab_${LABEL}.log 2>&1
  echo "  exit=$?"
  if [ -f rl_app_data.json ]; then
    md5sum rl_app_data.json
    cp rl_app_data.json /home/claude/ab_${LABEL}.json
  else
    echo "  NO BOARD PRODUCED"
    tail -4 /home/claude/ab_${LABEL}.log
  fi
}

run /home/claude/dob_ctrl  A 0
run /home/claude/dob_ctrl  B 1
run /home/claude/dobwrite  C 1
echo AB_DONE
