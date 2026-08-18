#!/bin/bash
# ORDER R — everything after the board suite, chained so there is no idle time and so no two engine
# runs ever overlap. STRICTLY SEQUENTIAL throughout.
#   1  the nine walk-forward matrices          (engine runs)
#   2  the in-process censuses and continuity  (engine runs)
#   3  the disclosed no-arb instruments        (no engine)
#   4  the tables, bands, class marks, boards, path test, whole-arc movers  (no engine)
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
# wait for the board suite to be finished
while pgrep -f 'build_allR.sh|rl_export.py' > /dev/null; do sleep 15; done
echo "=== BOARD SUITE FINISHED $(date -u +%H:%M:%S) ==="
echo; echo "### 1 · THE NINE WALK-FORWARD MATRICES ###"
bash "$HERE/run_emits_R.sh" > "$HERE/EMITS_R_out.txt" 2>&1
echo "  emits rc=$?"; grep -E 'COST|OK ->|NO MATRIX' "$HERE/EMITS_R_out.txt" | tail -30
echo; echo "### 2 · CENSUSES AND CONTINUITY ###"
bash "$HERE/run_measureR.sh" > "$HERE/MEASURE_R_out.txt" 2>&1
echo "  measure rc=$?"; grep -E '^##########|rc=|wrote' "$HERE/MEASURE_R_out.txt" | tail -50
echo; echo "### 3 · THE DISCLOSED NO-ARB INSTRUMENTS ###"
bash "$HERE/bb_noarbR.sh" > /dev/null 2>&1
echo "  noarb rc=$?"; grep -E '^=== |must be' "$HERE/NOARB_R_out.txt" | tail -20
echo; echo "### 4 · THE TABLES ###"
cd "$HERE"
for S in or_bands.py or_tables.py or_class.py or_boards.py; do
  echo "--- $S ---"; python3 "$S" > "${S%.py}_run.txt" 2>&1; echo "  rc=$?"; tail -3 "${S%.py}_run.txt"
done
echo "--- or_pathtest.py ---"; python3 or_pathtest.py > or_pathtest_run.txt 2>&1; echo "  rc=$?"; tail -3 or_pathtest_run.txt
echo "--- or_arc.py ---";      python3 or_arc.py      > or_arc_run.txt      2>&1; echo "  rc=$?"; tail -8 or_arc_run.txt
echo; echo "=== ORDER R MEASUREMENT COMPLETE $(date -u +%H:%M:%S) ==="
