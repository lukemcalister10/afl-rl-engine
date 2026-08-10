#!/bin/bash
# FULL GATE RUN — landed store d9a24282 + re-cut v0surf 5a03c9ea, gated path.
# NOTE: no RL_V0SURF_PKL here — gate mode rejects it as an unpinned model override.
# The engine resolves v0surf by natural precedence and finds /home/claude/v0surf.pkl,
# which this job seeded from THIS checkout (the canonical pattern, e.g.
# session_2026-07-19/envpin/scripts/build_board.sh:20). Guard 5 asserts the LOADED
# path's md5 == data/expected_boot.json 'v0surf' on every entry, so a wrong surface halts.
set -uo pipefail
REPO=/home/claude/dobwrite
OUT=$REPO/docs/evidence/dob_write_2026-08-10
WS=/home/claude/dob_ws/rl_after
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export RL_CONFIG_MODE=gate
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$WS:/home/claude/rl_vendor"
cd "$WS"

echo "== store in workspace ==" ; md5sum rl_model_data.json
echo "== v0surf on the load path ==" ; md5sum /home/claude/v0surf.pkl

rm -f rl_app_data.json rl_app_data.json.srcmd5 s4_matrix.json s4_matrix.json.srcmd5
echo "== rl_export.py (F1 export<->engine parity gate) =="
python3 rl_export.py > "$OUT/gate_export.txt" 2>&1
echo "rl_export exit=$?"
md5sum rl_app_data.json | tee "$OUT/gate_board_rebuild_md5.txt"

echo "== s4_matrix_M1v7.py (book; F2 book<->board parity gate) =="
python3 s4_matrix_M1v7.py > "$OUT/gate_book.txt" 2>&1
echo "s4_matrix exit=$?"
md5sum s4_matrix.json

echo "== one_source_selftest.py =="
python3 one_source_selftest.py > "$OUT/gate_selftest.txt" 2>&1
echo "selftest exit=$?"
echo -n "selftest PASS : "; grep -cE '^  PASS ' "$OUT/gate_selftest.txt"
echo -n "selftest FAIL : "; grep -cE '^  FAIL |^  STALE ' "$OUT/gate_selftest.txt"

echo "== guard_correction_canary.py (Guard 4) =="
python3 guard_correction_canary.py > "$OUT/gate_canary.txt" 2>&1
echo "canary exit=$?"

grep -E "NUMÉRAIRE GUARD|PARITY GATE" "$OUT/gate_export.txt"
echo GATES_DONE
