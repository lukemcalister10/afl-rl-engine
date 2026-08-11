#!/bin/bash
# ORDER 20 — emit the per-entrant matrices the nd_profile leg of the separation test needs.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
bash "$HERE/emit_matrix_o20.sh" BASE -
RL_O20_PERTURB=x3.0    bash "$HERE/emit_matrix_o20.sh" P_x3.0    "$HERE/perturb_pool.py"
RL_O20_PERTURB=flat100 bash "$HERE/emit_matrix_o20.sh" P_flat100 "$HERE/perturb_pool.py"
