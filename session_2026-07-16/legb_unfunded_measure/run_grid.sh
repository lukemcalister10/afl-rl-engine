#!/bin/bash
# LEG B UNFUNDED — the measurement grid driver (dev-shell; store b1fd0bce untouched).
# SEQUENTIAL + SINGLE-THREADED BLAS: the repo determinism fix made par_build/price6/NW order-fixed
# (thread-count invariant, register A1), so 1-thread BLAS is byte-identical and avoids the OpenBLAS
# oversubscription spin-thrash that stalled the -P2 run (load 12 on 4 cores). Each point ~2-4 min.
# All verdicts from FROZEN instruments. Writes to out/.
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
OUT="$HERE/session_2026-07-16/legb_unfunded_measure/out"
mkdir -p "$OUT"
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/session_2026-07-16/uncompress/beta_measure.py" "$WS/beta_measure.py"
cp -f "$HERE/session_2026-07-16/segment5_law_grid/ledger_dump.py" "$WS/ledger_dump.py"
cp -f "$HERE/session_2026-07-16/legb_unfunded_measure/measure_gcohort.py" "$WS/measure_gcohort.py"
[ "$(md5sum "$WS/beta_measure.py"|cut -c1-8)" = "14c59139" ] || { echo "FROZEN beta_measure md5 MISMATCH — HALT"; exit 3; }
cd "$WS"
export RL_REPO="$HERE" PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

echo "[$(date +%H:%M:%S)] OFF baseline (beta_c + ledger + gcohort)"
RL_UNCOMP=0 python3 beta_measure.py 2>"$OUT/beta_OFF.txt"
RL_UNCOMP=0 python3 ledger_dump.py "$OUT/led_OFF.json" >"$OUT/led_OFF.log" 2>&1
RL_UNCOMP=0 python3 measure_gcohort.py OFF >"$OUT/gc_OFF.txt" 2>"$OUT/gc_OFF.err"
echo "[$(date +%H:%M:%S)] OFF done: $(grep RATIOS "$OUT/gc_OFF.txt")"

for s in 0.65 0.85 1.00 1.25 1.50; do
  echo "[$(date +%H:%M:%S)] point s=$s (gcohort + beta + ledger)"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 measure_gcohort.py "s$s" >"$OUT/gc_s$s.txt" 2>"$OUT/gc_s$s.err"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 beta_measure.py 2>"$OUT/beta_s$s.txt"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 ledger_dump.py "$OUT/led_s$s.json" >"$OUT/led_s$s.log" 2>&1
  echo "[$(date +%H:%M:%S)] s=$s done: $(grep RATIOS "$OUT/gc_s$s.txt") | $(grep '^s=' "$OUT/beta_s$s.txt")"
done
echo "ALL DONE"
