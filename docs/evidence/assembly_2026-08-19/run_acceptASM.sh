#!/bin/bash
# ASSEMBLY BUILD — THE ACCEPTANCE SUITE on THE CANDIDATE's dial line. STRICTLY SEQUENTIAL.
# Every item the charter lists, run on the line the candidate board was actually built with.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
echo "THREAD PINS: OPENBLAS=$OPENBLAS_NUM_THREADS OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS NUMEXPR=$NUMEXPR_NUM_THREADS VECLIB=$VECLIB_MAXIMUM_THREADS  PYTHONHASHSEED=$PYTHONHASHSEED"

CAND="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1"
R20A="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20"

echo; echo "===== THE TWO CENSUSES + THE CHARGE DISTRIBUTION — THE CANDIDATE ====="
python3 "$HERE/os_census.py" CAND $CAND > "$HERE/CENSUS_CAND_out.txt" 2>&1
echo "exit=$?"; tail -6 "$HERE/CENSUS_CAND_out.txt"

echo; echo "===== CONTINUITY (every axis, incl. age 23/24 and the season turn) — THE CANDIDATE ====="
python3 "$HERE/os_continuity.py" CAND $CAND > "$HERE/CONTINUITY_CAND_out.txt" 2>&1
echo "exit=$?"; tail -6 "$HERE/CONTINUITY_CAND_out.txt"

echo; echo "===== THE PSI IDENTITY — THE CANDIDATE ====="
python3 "$HERE/os_identity.py" > "$HERE/IDENTITY_CAND_out.txt" 2>&1
echo "exit=$?"; tail -4 "$HERE/IDENTITY_CAND_out.txt"

echo; echo "===== CENSUS ON R, for the like-for-like comparison ====="
python3 "$HERE/os_census.py" R20A $R20A > "$HERE/CENSUS_R20A_out.txt" 2>&1
echo "exit=$?"; tail -4 "$HERE/CENSUS_R20A_out.txt"
echo; echo "ACCEPTANCE SUITE DONE"
