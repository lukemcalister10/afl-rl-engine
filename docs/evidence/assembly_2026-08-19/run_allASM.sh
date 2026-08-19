#!/bin/bash
# ASSEMBLY BUILD — everything that runs AFTER the boards exist. STRICTLY SEQUENTIAL.
# Pure-JSON analysis first (fast, no engine), then the engine-loading acceptance items, then the
# walk-forward emit and the no-arb chain, then the owner documents.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
echo "THREAD PINS: OPENBLAS=$OPENBLAS_NUM_THREADS OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS NUMEXPR=$NUMEXPR_NUM_THREADS VECLIB=$VECLIB_MAXIMUM_THREADS PYTHONHASHSEED=$PYTHONHASHSEED"

CAND="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 RL_O41_R3=1"

echo; echo "########## 1 · THE BOARDS AND THE LEVER STACK (no engine) ##########"
python3 "$HERE/as_boards.py"  > "$HERE/BOARDS_run.txt" 2>&1; echo "exit=$?"; tail -30 "$HERE/BOARDS_run.txt"

echo; echo "########## 2 · THE TRACKER AND THE PER-LEVER DOCUMENT (no engine) ##########"
python3 "$HERE/as_tracker.py" > "$HERE/TRACKER_run.txt" 2>&1; echo "exit=$?"; tail -20 "$HERE/TRACKER_run.txt"

echo; echo "########## 3 · THE MECHANISM LEGS + THE S-S5 WINDOW (engine) ##########"
python3 "$HERE/as_legs.py"    > "$HERE/LEGS_run.txt" 2>&1; echo "exit=$?"; tail -14 "$HERE/LEGS_run.txt"

echo; echo "########## 4 · THE TWO CENSUSES + THE CHARGE DISTRIBUTION (engine) ##########"
python3 "$HERE/os_census.py" CAND $CAND > "$HERE/CENSUS_CAND_out.txt" 2>&1; echo "exit=$?"
grep -iE "burn|birthday|CENSUS|0 of|VIOLAT" "$HERE/CENSUS_CAND_out.txt" | head -20

echo; echo "########## 5 · CONTINUITY, EVERY AXIS (engine) ##########"
python3 "$HERE/os_continuity.py" CAND $CAND > "$HERE/CONTINUITY_CAND_out.txt" 2>&1; echo "exit=$?"
grep -iE "VERDICT|BREAK|jump|season turn|23/24|PASS|FAIL" "$HERE/CONTINUITY_CAND_out.txt" | head -20

echo; echo "########## 6 · THE WALK-FORWARD EMIT FOR THE CANDIDATE (engine) ##########"
env $CAND OP_LABEL=ASMCAND bash "$HERE/run_emit_ASM.sh"

echo; echo "########## 7 · THE NO-ARB INSTRUMENTS ##########"
bash "$HERE/bb_noarbASM.sh"

echo; echo "########## 8 · THE BAND TABLES, BOTH WINDOWS ##########"
python3 "$HERE/as_bands.py" > "$HERE/BANDS_run.txt" 2>&1; echo "exit=$?"; tail -12 "$HERE/BANDS_run.txt"

echo; echo "########## 9 · THE YEAR-1 CLASS MARK, REGISTERED BASIS ##########"
python3 "$HERE/as_class.py" > "$HERE/CLASS_ASM_out.txt" 2>&1; echo "exit=$?"
grep -iE "ASMCAND|W2|FLOOR|RAIL|BREACH" "$HERE/CLASS_ASM_out.txt" | head -20

echo; echo "########## 10 · THE OWNER DOCUMENTS ##########"
python3 "$HERE/as_pages.py"  > "$HERE/PAGES_run.txt" 2>&1; echo "exit=$?"; tail -8 "$HERE/PAGES_run.txt"

echo; echo "ALL DONE"
