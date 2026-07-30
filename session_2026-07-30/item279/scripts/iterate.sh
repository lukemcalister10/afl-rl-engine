#!/bin/bash
# One convergence iteration: install curve -> reseed -> refit surface + rebuild board -> re-derive curve.
set -euo pipefail
SP=/tmp/claude-0/-home-user-afl-rl-engine/d48a4c8b-795f-5b7c-b858-a744667dac28/scratchpad
WT=$SP/wt-085; E=$SP/echo; C=$SP/curve
IT="$1"; SRC_CURVE="$2"; SRC_POOL="$3"; EXTRA="${4:-}"
RUN () { env -i HOME=/root PATH=/root/rl_venv312/bin:/usr/bin:/bin RL_VENV=/root/rl_venv312 \
  RL_REPO="$WT" PYTHONHASHSEED=0 \
  OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
  LC_ALL=C.UTF-8 LANG=C.UTF-8 PYTHONPATH="$WT:$WT/vendor" \
  RL_FV="$WT/engine/forward_valuation" RL_GAMMA=1.0 RL_PICK1=3000 RL_V0SURF_REFIT=1 \
  ITEM279_OUT="$E" ITEM279_MATRIX_NAME="per_entrant_it${IT}.json" CURVE_STATISTIC=VOR "$@"; }
if [ "${SKIP_INSTALL:-0}" != "1" ]; then
  echo "### ITERATION $IT  (curve in: $(basename $SRC_CURVE), pool $SRC_POOL) $EXTRA"
  /root/rl_venv312/bin/python $E/install_curve.py "$SRC_CURVE" "$WT/engine/rl_after/pvc_curve_v2.json" "$SRC_POOL" $EXTRA
  env -i HOME=/root PATH=/root/rl_venv312/bin:/usr/bin:/bin RL_VENV=/root/rl_venv312 RL_REPO="$WT" \
    PYTHONHASHSEED=0 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 LC_ALL=C.UTF-8 \
    bash "$WT/bootstrap.sh" > $E/log_boot_$IT.txt 2>&1
  grep -q "bootstrap OK" $E/log_boot_$IT.txt && echo "  reseed OK"
  cd /home/claude/rl_workspace/rl_after
  chmod u+w rl_app_data.json 2>/dev/null || true; rm -f rl_app_data.json
  T=$(date +%s); RUN python3 rl_export.py > $E/log_board_$IT.txt 2>&1
  echo "  board built in $(( $(date +%s)-T ))s -> $(md5sum rl_app_data.json | cut -c1-32)"
  cp rl_app_data.json $E/board_it$IT.json
fi
cd /home/claude/rl_workspace/rl_after
T=$(date +%s); RUN python3 $C/emit_matrix_279.py > $E/log_emit_$IT.txt 2>&1
echo "  matrix emitted in $(( $(date +%s)-T ))s -> $(ls -la $E/per_entrant_it$IT.json | awk '{print $5}') bytes"
cd "$WT"
RUN python3 $C/derive_279.py --matrix "$E/per_entrant_it$IT.json" --out "$E/derived_it$IT.json" > $E/log_derive_$IT.txt 2>&1
grep -E "^store|^curve:|^pool level" $E/log_derive_$IT.txt | sed 's/^/  /'
echo "  both-directions: $(grep -c 'PASS site' $E/log_derive_$IT.txt) PASS / $(grep -c 'FAIL site' $E/log_derive_$IT.txt || true) FAIL"
