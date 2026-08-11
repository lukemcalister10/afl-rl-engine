#!/bin/bash
# ORDER 20 — run the population probe against this checkout.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation"
export RL_PROBE_OUT="$HERE/POPULATION_PROBE.json"
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 PYTHONHASHSEED=0
python3 "$HERE/population_probe.py" | tee "$HERE/POPULATION_PROBE.txt"
