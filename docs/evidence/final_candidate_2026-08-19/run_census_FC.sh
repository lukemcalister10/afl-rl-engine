#!/bin/bash
# FINAL-CANDIDATE — THE BURN CENSUS AND THE BIRTHDAY CENSUS. STRICTLY SEQUENTIAL.
#
# TWO LINES ARE RUN AND BOTH ARE KEPT, because the pair is the evidence:
#
#  1. FCCAND — the candidate's own line, RL_O41_R3 LIVE. This is EXPECTED TO ASSERT. os_census.py
#     reconstructs price as [rho*e + age credit] + pi_base*(v*PL_F)*factor(v) — an identity with NO
#     absence-collector term — so it breaks on the first R3-faded row. The D6 seat recorded the same
#     assert on both its lines (PACKET_D6 §10b). It is run here so this seat's own build shows it
#     rather than citing someone else's run.
#
#  2. FCNOR3 — the same line with RL_O41_R3 (and, forced, BREAK/UNWIND) OFF. THIS is the line the
#     burn census is scorable on, and it is the basis the assembly seat used for the same reason
#     (PACKET_ASSEMBLY §10: "the censuses are run on the R3-off line").
#
# WHAT IS THEREFORE NOT COVERED, AND IS SAID PLAINLY RATHER THAN LEFT TO BE INFERRED:
# THE BURN SWEEP HAS NOT BEEN RUN THROUGH THE R3 TERM. The interaction of entry price with the R3
# collector is UNSWEPT on this board, exactly as it was unswept on the assembly board.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
export RL_V0SURF_PKL="$RL_ROOT/data/v0surf.pkl"
unset RL_O42 RL_AVAIL RL_O41_R3 RL_O41_BREAK RL_O41_UNWIND RL_O41_RAMP 2>/dev/null || true
echo "THREAD PINS: OPENBLAS=$OPENBLAS_NUM_THREADS OMP=$OMP_NUM_THREADS MKL=$MKL_NUM_THREADS NUMEXPR=$NUMEXPR_NUM_THREADS VECLIB=$VECLIB_MAXIMUM_THREADS  PYTHONHASHSEED=$PYTHONHASHSEED"
echo "RL_V0SURF_PKL=$RL_V0SURF_PKL  ($(md5sum "$RL_V0SURF_PKL" | cut -c1-32))"
echo "engine: $(md5sum "$RL_ROOT/engine/rl_after/_merged_recover.py" | cut -c1-32)"

COMMON="RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_BETASAT=0.105 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15 \
RL_O40_RECW=0.47 RL_O40_PGMAT=1 RL_O41_SDOFF=2.98 RL_O41_CREDIT=1 RL_O41_RESET=1 RL_O41_INJ=1"
CAND="$COMMON RL_O41_R3=1 RL_O41_RAMP=1 RL_O41_BREAK=unwind RL_O41_UNWIND=7 RL_O42=1"
NOR3="$COMMON RL_O41_RAMP=1 RL_O42=1"

echo; echo "===== 1 · THE CANDIDATE LINE (R3 LIVE) — EXPECTED TO ASSERT ====="
python3 "$HERE/os_census.py" FCCAND $CAND > "$HERE/CENSUS_FCCAND_out.txt" 2>&1
echo "exit=$?"
grep -iE "board total|AssertionError|identity broke" "$HERE/CENSUS_FCCAND_out.txt" | head -5

echo; echo "===== 2 · THE R3-OFF LINE — THE SCORABLE BURN CENSUS ====="
python3 "$HERE/os_census.py" FCNOR3 $NOR3 > "$HERE/CENSUS_FCNOR3_out.txt" 2>&1
echo "exit=$?"
grep -iE "board total|BURN CENSUS|TOTAL|birthday|rows that GAIN|points handed back|worst ratio|AssertionError" \
  "$HERE/CENSUS_FCNOR3_out.txt" | head -20

echo; echo "CENSUS RUN DONE"
