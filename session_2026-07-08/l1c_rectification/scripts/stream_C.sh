#!/bin/bash
set -e
L=/home/user/afl-rl-engine/session_2026-07-08/l1c_rectification
bash $L/scripts/run_matrix.sh $L/out/s4_matrix_w085.json RL_YCRED_W=0.85 RL_APP_DATA=/nonexistent
bash $L/scripts/run_matrix.sh $L/out/s4_matrix_w10.json RL_YCRED_W=1.0 RL_APP_DATA=/nonexistent
