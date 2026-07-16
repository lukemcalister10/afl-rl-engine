#!/bin/bash
# LEG B UNFUNDED — the measurement grid driver (dev-shell; store b1fd0bce untouched). Fans out the
# per-point jobs (gcohort + beta + ledger) with a concurrency cap; OFF baseline (beta_c + ledger) once.
# All verdicts from FROZEN instruments. Writes to out/. NB: s=1.00 already measured (gc + beta); this
# run fills OFF, s=1.00 ledger, and the other four points in full.
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

run_off () {
  RL_UNCOMP=0 python3 beta_measure.py 2>"$OUT/beta_OFF.txt"
  RL_UNCOMP=0 python3 ledger_dump.py "$OUT/led_OFF.json" >"$OUT/led_OFF.log" 2>&1
  RL_UNCOMP=0 python3 measure_gcohort.py OFF >"$OUT/gc_OFF.txt" 2>"$OUT/gc_OFF.err"
  echo "DONE OFF"
}
run_pt () {
  local s="$1"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 measure_gcohort.py "s$s" >"$OUT/gc_s$s.txt" 2>"$OUT/gc_s$s.err"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 beta_measure.py 2>"$OUT/beta_s$s.txt"
  RL_UNCONSERVE=1 RL_UNCOMP_S="$s" python3 ledger_dump.py "$OUT/led_s$s.json" >"$OUT/led_s$s.log" 2>&1
  echo "DONE s=$s"
}
export -f run_off run_pt
export OUT WS HERE RL_REPO PYTHONHASHSEED RL_GAMMA RL_PICK1 RL_RUCK_TAX RL_RECENCY_DECAY RL_PRIOR_TREES PAR_RAMPS PYTHONPATH RL_Q97M_PKL

# concurrency cap 2 (4 cores; each job is a chain of ~1-core loads)
( run_off ) &
for s in 0.65 0.85 1.25 1.50; do echo "run_pt $s"; done | xargs -I{} -P 2 bash -c '{}'
wait
# s=1.00 ledger (gc + beta already captured for s=1.00)
run_pt_ledger_only () { RL_UNCONSERVE=1 RL_UNCOMP_S=1.00 python3 ledger_dump.py "$OUT/led_s1.00.json" >"$OUT/led_s1.00.log" 2>&1; }
run_pt_ledger_only
echo "ALL DONE"
