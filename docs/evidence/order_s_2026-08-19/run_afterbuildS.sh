#!/bin/bash
# ORDER S — everything that runs AFTER the board suite, in one strictly sequential chain.
# NEVER two engine runs at once. Order chosen so the cheapest, highest-value objects land first.
#   1  os_boards.py    pure JSON, no engine — the identities, totals, movers, mature rows
#   2  run_measureS.sh the in-process censuses and continuity (engine, sequential)
#   3  run_emits_S.sh  the walk-forward matrices (engine, sequential, the expensive step)
#   4  bb_noarbS.sh    the disclosed no-arb instruments over every matrix
#   5  os_bands / os_class / os_tables / os_pathtest / os_cap  — pure reads
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
cd "$HERE"
echo "########## 1 · BOARDS ##########"
python3 os_boards.py > os_boards_run.txt 2>&1; echo "  rc=$?"; tail -3 os_boards_run.txt
echo; echo "########## 1b · FALSIFIER S-F3, THE FIX A DECOMPOSITION IDENTITY ##########"
bash run_identityS.sh > IDENTITY_S_out.txt 2>&1; echo "  rc=$?"; cat IDENTITY_S_out.txt
echo; echo "########## 2 · CENSUS + CONTINUITY ##########"
bash run_measureS.sh > MEASURE_S_out.txt 2>&1; echo "  rc=$?"; tail -3 MEASURE_S_out.txt
echo; echo "########## 3 · EMITS ##########"
bash run_emits_S.sh > EMITS_S_out.txt 2>&1; echo "  rc=$?"; tail -6 EMITS_S_out.txt
echo; echo "########## 4 · NO-ARB INSTRUMENTS ##########"
bash bb_noarbS.sh > /dev/null 2>&1; echo "  rc=$?"; tail -4 NOARB_S_out.txt
echo; echo "########## 5 · THE READS ##########"
for s in os_bands.py os_class.py os_tables.py os_pathtest.py os_cap.py; do
  echo "-- $s --"
  python3 "$s" > "${s%.py}_run.txt" 2>&1; echo "  rc=$?"; tail -3 "${s%.py}_run.txt"
done
echo; echo "########## DONE ##########"
