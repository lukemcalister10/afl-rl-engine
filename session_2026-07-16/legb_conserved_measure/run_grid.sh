#!/bin/bash
# LEG B CONSERVED — the measurement grid driver (dev-shell; store b1fd0bce untouched).
# CONSERVED = shipped C: RL_UNCONSERVE stays UNSET, so the memo §3 per-position conservation
# renorm C[pos] is APPLIED at _merged_recover.py:333 (the shipped byte-exact path). Points differ
# ONLY by the un-compress map strength RL_UNCOMP_S=<s>. This is the item-260 battery re-run at the
# eight conserved grid points; ZERO new engine code (the toggle stays off). All verdicts from FROZEN
# instruments (beta_measure md5 14c59139, ship_gates_check._b1_july8, ledger_dump). Writes to out/.
# SEQUENTIAL + SINGLE-THREADED BLAS (order-fixed determinism, register A1): 1-thread == byte-identical
# and avoids the OpenBLAS oversubscription thrash. Each ON point ~2-4 min.
set -uo pipefail
HERE=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
DIR="$HERE/session_2026-07-16/legb_conserved_measure"
OUT="$DIR/out"
mkdir -p "$OUT"
cp -f "$HERE/engine/rl_after/rl_model.py" "$HERE/engine/rl_after/_merged_recover.py" "$WS/"
cp -f "$HERE/session_2026-07-16/uncompress/beta_measure.py" "$WS/beta_measure.py"
cp -f "$HERE/session_2026-07-16/segment5_law_grid/ledger_dump.py" "$WS/ledger_dump.py"
cp -f "$DIR/measure_gcohort.py" "$WS/measure_gcohort.py"
[ "$(md5sum "$WS/beta_measure.py"|cut -c1-8)" = "14c59139" ] || { echo "FROZEN beta_measure md5 MISMATCH — HALT"; exit 3; }
cd "$WS"
export RL_REPO="$HERE" PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS":/home/claude/rl_vendor RL_Q97M_PKL="$HERE/data/q97m.pkl"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1

echo "[$(date +%H:%M:%S)] OFF baseline (beta_c + ledger + gcohort) — RL_UNCOMP=0 => board 8d90c9ac"
RL_UNCOMP=0 python3 beta_measure.py 2>"$OUT/beta_OFF.txt"
RL_UNCOMP=0 python3 ledger_dump.py "$OUT/led_OFF.json" >"$OUT/led_OFF.log" 2>&1
RL_UNCOMP=0 python3 measure_gcohort.py OFF >"$OUT/gc_OFF.txt" 2>"$OUT/gc_OFF.err"
echo "[$(date +%H:%M:%S)] OFF done: $(grep RATIOS "$OUT/gc_OFF.txt")"

for s in 0.15 0.25 0.35 0.45 0.55 0.60 0.65 0.70; do
  echo "[$(date +%H:%M:%S)] point s=$s (gcohort + beta + ledger; conserved, toggle UNSET)"
  RL_UNCOMP_S="$s" python3 measure_gcohort.py "s$s" >"$OUT/gc_s$s.txt" 2>"$OUT/gc_s$s.err"
  RL_UNCOMP_S="$s" python3 beta_measure.py 2>"$OUT/beta_s$s.txt"
  RL_UNCOMP_S="$s" python3 ledger_dump.py "$OUT/led_s$s.json" >"$OUT/led_s$s.log" 2>&1
  python3 "$DIR/analyze_conserved.py" "$OUT/led_OFF.json" "$OUT/led_s$s.json" "$s" >"$OUT/an_s$s.log" 2>&1
  echo "[$(date +%H:%M:%S)] s=$s done: $(grep RATIOS "$OUT/gc_s$s.txt") | $(grep '^s=' "$OUT/beta_s$s.txt")"
done
echo "ALL DONE"
