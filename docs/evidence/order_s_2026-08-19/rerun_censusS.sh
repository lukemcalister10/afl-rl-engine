#!/bin/bash
# ORDER S — re-run of the censuses that raised on this seat's own scorer bug (o38_parts now returns
# FIVE values, not three; ORDER R's scorer unpacked three). STRICTLY SEQUENTIAL. The bug and its fix
# are reported in the packet rather than silently corrected.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
cd "$HERE"
SPECS=(
  "SRoff:RL_O37=1"
  "SB1:RL_O37=1 RL_O38B1=1"
  "SAB1:RL_O37=1 RL_O38A=1 RL_O38B1=1"
  "SR20A:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20"
  "SW47:RL_O37=1 RL_O38B1=1 RL_O40_RECW=0.47"
  "SW28:RL_O37=1 RL_O38B1=1 RL_O40_RECW=0.28"
  "SW47A:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=0.47"
  "SC15:RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=15"
  "SC20:RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20"
  "SC20A:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20"
  "SL56:RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=0.56"
  "SL10:RL_O37=1 RL_O38B1=1 RL_O40_LAMBDA=0.10"
  "SM:RL_O37=1 RL_O38B1=1 RL_O40_PGMAT=1"
  "SMA:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_PGMAT=1"
  "SALL:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=0.47 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 RL_O40_PGMAT=1"
)
for spec in "${SPECS[@]}"; do
  T=${spec%%:*}; D=${spec#*:}
  [ -f "CENSUS_$T.json" ] && { echo "  $T already done"; continue; }
  echo "########## os_census.py $T ##########"
  python3 os_census.py "$T" $D > "os_census_${T}_run.txt" 2>&1
  echo "  rc=$?"
done
