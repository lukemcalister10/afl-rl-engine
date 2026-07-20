#!/bin/bash
set -euo pipefail
for i in 1 2 3 4 5; do
  printf "run %d: " "$i"
  RL_LEGE=0 RL_LEGF=0 bash /home/user/afl-rl-engine/session_2026-07-19/envpin/scripts/build_board.sh confirm$i
done
