#!/bin/bash
# Generate a walk-forward cohort matrix via the OFFICIAL pricer s4_matrix_M1v7.py in GATE mode
# (clean config, __meta__ hashes stamped), exactly as ship_gates_check.py regenerates the candidate.
# usage: gen_matrix.sh <out_matrix.json>   [engine source is whatever is currently in the workspace]
set -e
RA=/home/claude/rl_workspace/rl_after
REPO=/home/user/afl-rl-engine
OUT=$1
cd "$RA"
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor   # vendored unidecode (offline); gate mode clears model env, not PYTHONPATH
S4_MATRIX="$OUT" RL_CONFIG_MODE=gate RL_REPO="$REPO" python3 s4_matrix_M1v7.py
