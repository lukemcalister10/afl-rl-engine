#!/bin/bash
# ORDER 29C -- the prediction calculator, run before the emit and before any instrument.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
# ORDER 29's disclosed instrument copies — imported READ-ONLY for `load_matrix`'s population filter
# and its identity pins. Nothing in this directory is modified by ORDER 29C.
export RL_NOARB_DIR="$(cd "$HERE/../noarb" && pwd)"
echo "  harness read from: $RL_NOARB_DIR  ($(md5sum "$RL_NOARB_DIR/noarb_table_338.py" | cut -c1-32))"
echo "  29B matrix md5: $(md5sum "$SP/per_entrant_O29B.json" | cut -c1-32)"
python3 "$HERE/o29c_predict.py" "$SP/per_entrant_O29B.json" "$HERE/LANDED_V0_29C.json" \
        "$HERE/PREDICT_29C.json" 2>&1 | tee "$HERE/PREDICT_29C_out.txt"
