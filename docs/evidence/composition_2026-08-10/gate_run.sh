#!/bin/bash
# GATE RUN — the composition branch. Mirrors docs/evidence/g1_never_rises_2026-08-10/gate_run.sh,
# pointed at the repo checkout rather than a bootstrapped workspace (this branch changes no engine
# file, so the checkout IS the engine under test).
#
# NOTE: no RL_V0SURF_PKL — gate mode rejects it as an unpinned model override. Guard 5 asserts the
# LOADED surface path's md5 == data/expected_boot.json 'v0surf' on every entry.
set -uo pipefail
REPO=/home/user/afl-rl-engine
OUT=$REPO/docs/evidence/composition_2026-08-10
WS=$REPO/engine/rl_after
export PATH=/root/rl_venv312/bin:$PATH
export RL_REPO="$REPO"
export RL_FV="$REPO/engine/forward_valuation"
export RL_CONFIG_MODE=gate
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export PYTHONPATH="$WS:$REPO:$REPO/vendor"
cd "$WS"

echo "== store ==" ; md5sum rl_model_data.json
echo "== engine head ==" ; md5sum _merged_recover.py
echo "== committed board ==" ; md5sum "$REPO/data/rl_build/rl_app_data.json"

rm -f rl_app_data.json rl_app_data.json.srcmd5 s4_matrix.json s4_matrix.json.srcmd5

echo "== rl_export.py (F1 export<->engine parity gate) =="
python3 rl_export.py > "$OUT/gate_export.txt" 2>&1
echo "rl_export exit=$?"
md5sum rl_app_data.json | tee "$OUT/gate_board_rebuild_md5.txt"

echo "== s4_matrix_M1v7.py (book; F2 book<->board parity gate) =="
python3 s4_matrix_M1v7.py > "$OUT/gate_book.txt" 2>&1
echo "s4_matrix exit=$?"

echo "== one_source_selftest.py (THE STANDING GATED BUILD — D14a/b/c/d run here) =="
python3 one_source_selftest.py > "$OUT/gate_selftest.txt" 2>&1
echo "selftest exit=$?"
echo -n "selftest PASS : "; grep -cE '^  PASS ' "$OUT/gate_selftest.txt"
echo -n "selftest FAIL : "; grep -cE '^  FAIL |^  STALE ' "$OUT/gate_selftest.txt"

echo "== guard_correction_canary.py (Guard 4) =="
python3 guard_correction_canary.py > "$OUT/gate_canary.txt" 2>&1
echo "canary exit=$?"

echo "== ship_gates_check.py (the hand-run superset; gate D14d on the board) =="
python3 "$REPO/ship_gates_check.py" > "$OUT/gate_ship.txt" 2>&1
echo "ship_gates exit=$?"

grep -E "NUMÉRAIRE GUARD|PARITY GATE" "$OUT/gate_export.txt"
sed -n '/=== (11)/,$p' "$OUT/gate_selftest.txt"
echo GATES_DONE
