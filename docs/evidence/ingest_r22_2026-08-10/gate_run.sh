#!/bin/bash
# Independent gate run for the round-22 landing, in a PRIVATE workspace (/home/claude/r22_ws).
# Rebuilds the board from the landed store (F1 export<->engine parity gate), rebuilds the book
# (F2 book<->board parity gate), then runs the one-source self-test and the Guard 4 canary.
# Byte-reproducing the landed board 6e724cca is itself the determinism check.
set -uo pipefail
REPO=/home/claude/r22
WS=/home/claude/r22_ws/rl_after
OUT=$REPO/docs/evidence/ingest_r22_2026-08-10
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export RL_CONFIG_MODE=gate
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$WS:/home/claude/rl_vendor"
cd "$WS"

echo "== store in workspace ==" ; md5sum rl_model_data.json

rm -f rl_app_data.json rl_app_data.json.srcmd5 s4_matrix.json s4_matrix.json.srcmd5
echo "== rl_export.py (F1 export<->engine parity gate) =="
python3 rl_export.py > "$OUT/gate_export.txt" 2>&1
echo "rl_export exit=$?"
md5sum rl_app_data.json | tee "$OUT/gate_board_rebuild_md5.txt"

echo "== s4_matrix_M1v7.py (book; F2 book<->board parity gate) =="
python3 s4_matrix_M1v7.py > "$OUT/gate_book.txt" 2>&1
echo "s4_matrix exit=$?"

echo "== one_source_selftest.py =="
python3 one_source_selftest.py > "$OUT/gate_selftest.txt" 2>&1
echo "selftest exit=$?"
grep -cE '^  PASS ' "$OUT/gate_selftest.txt"
grep -cE '^  FAIL |^  STALE ' "$OUT/gate_selftest.txt"

echo "== guard_correction_canary.py (Guard 4) =="
python3 guard_correction_canary.py > "$OUT/gate_canary.txt" 2>&1
echo "canary exit=$?"
echo "GATES_DONE"
