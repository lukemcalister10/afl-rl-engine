#!/bin/bash
# D6-CONSOLIDATION — THE ACCEPTANCE SUITE on the CANDIDATE's own dial line. STRICTLY SEQUENTIAL.
# Run after the boards exist. Every item is run on the line the candidate board was actually built
# with, RL_O42=1 included.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
unset RL_O42 RL_AVAIL 2>/dev/null || true
echo "THREAD PINS: OPENBLAS=$OPENBLAS_NUM_THREADS OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS NUMEXPR=$NUMEXPR_NUM_THREADS VECLIB=$VECLIB_MAXIMUM_THREADS  PYTHONHASHSEED=$PYTHONHASHSEED"
echo "engine: $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"

BASE="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1 \
RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7"
CAND="$BASE RL_O42=1"

echo; echo "===== 1 · THE BURN CENSUS + THE BIRTHDAY PROBE — THE CANDIDATE (RL_O42=1) ====="
python3 "$RL_ROOT/docs/evidence/assembly_2026-08-19/os_census.py" D6CAND $CAND \
  > "$HERE/CENSUS_D6CAND_out.txt" 2>&1
echo "exit=$?"
grep -iE "BURN CENSUS|rows that BURN|TOTAL|birthday|points handed back|board total" "$HERE/CENSUS_D6CAND_out.txt" | head -12

echo; echo "===== 2 · THE BURN CENSUS + THE BIRTHDAY PROBE — THE BASE, for like-for-like ====="
python3 "$RL_ROOT/docs/evidence/assembly_2026-08-19/os_census.py" D6BASE $BASE \
  > "$HERE/CENSUS_D6BASE_out.txt" 2>&1
echo "exit=$?"
grep -iE "BURN CENSUS|rows that BURN|TOTAL|birthday|points handed back|board total" "$HERE/CENSUS_D6BASE_out.txt" | head -12

echo; echo "===== 3 · THE TAIL CALIBRATION ====="
python3 "$HERE/d6_tail.py" > "$HERE/TAIL_D6_run.txt" 2>&1
echo "exit=$?"
grep -iE "calibration|SMOOTH|realized|deep" "$HERE/TAIL_D6_out.txt" 2>/dev/null | head -14

echo; echo "ACCEPTANCE SUITE DONE"
