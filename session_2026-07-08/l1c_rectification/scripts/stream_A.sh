#!/bin/bash
set -e
L=/home/user/afl-rl-engine/session_2026-07-08/l1c_rectification
bash $L/scripts/run_matrix.sh $L/out/s4_matrix_w05.json RL_YCRED_W=0.5 RL_APP_DATA=/nonexistent
bash $L/scripts/run_matrix.sh $L/out/s4_matrix_w06.json RL_YCRED_W=0.6 RL_APP_DATA=/nonexistent
