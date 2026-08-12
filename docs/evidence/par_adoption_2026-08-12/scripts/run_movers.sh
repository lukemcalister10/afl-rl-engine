#!/bin/bash
# ORDER 20B TASK 4 — render the per-cell surface report and the per-mover channel decomposition.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
python3 "$HERE/par_cells.py" "$SP/probe_HEAD.json" "$SP/probe_FIX.json" "$HERE/../movers/PAR_CELLS" \
  | tee "$HERE/../movers/PAR_CELLS.txt"
python3 "$HERE/mover_decomp.py" "$SP" "$HERE/../movers/CHANNEL_DECOMP" \
  | tee "$HERE/../movers/CHANNEL_DECOMP.txt"
