#!/bin/bash
# ORDER S — the in-process measurement suite. STRICTLY SEQUENTIAL: every one of these loads the
# engine, so none of them may run beside a board build or beside each other.
#   os_census.py     the burn census, the birthday census, the CHARGE DISTRIBUTION and the named rows
#   os_continuity.py continuity on every axis INCLUDING THE SEASON-TURN AXIS, on the EFFECTIVE
#                    constants and through the engine's OWN cap function
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
cd "$HERE"
run () { # run SCRIPT TAG dials...
  local S=$1 T=$2; shift 2
  echo; echo "########## $S  $T  $* ##########"
  python3 "$S" "$T" "$@" > "${S%.py}_${T}_run.txt" 2>&1
  local rc=$?
  echo "  rc=$rc"
  [ $rc -ne 0 ] && tail -25 "${S%.py}_${T}_run.txt"
  tail -4 "${S%.py}_${T}_run.txt"
  return 0
}
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
echo "=== ORDER S CENSUSES — strictly sequential ==="
for spec in "${SPECS[@]}"; do
  T=${spec%%:*}; D=${spec#*:}
  run os_census.py "$T" $D
done
echo
echo "=== ORDER S CONTINUITY — strictly sequential, INCLUDING THE SEASON-TURN AXIS ==="
# CONTINUITY IS RUN ON A SUBSET AND THE SUBSET IS NAMED HERE RATHER THAN LEFT TO BE NOTICED.
# Every ORDER S variant carries FIX B1, and B1 collapses the 23->24 age step to exactly zero on
# EVERY cell (ORDER Q measured that and ORDER R reproduced it on twelve boards), so the age axis is
# structurally identical across the eleven variants. The cells run below are: both controls, both
# recency cells (the only ones that can move the SEASON-TURN axis at all), both compression cells
# (the only ones that change the shape of T), both mature cells, and the far corner. The three not
# run are SW28, SC15 and the two LAMBDA frontier endpoints, whose axes are bracketed by cells that
# ARE run. THIS IS A WALL-CLOCK CHOICE AND IT IS DISCLOSED, NOT HIDDEN.
CSPECS=(
  "SB1:RL_O37=1 RL_O38B1=1"
  "SAB1:RL_O37=1 RL_O38A=1 RL_O38B1=1"
  "SW47:RL_O37=1 RL_O38B1=1 RL_O40_RECW=0.47"
  "SW47A:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=0.47"
  "SC20:RL_O37=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20"
  "SC20A:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20"
  "SM:RL_O37=1 RL_O38B1=1 RL_O40_PGMAT=1"
  "SMA:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_PGMAT=1"
  "SALL:RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O40_RECW=0.47 RL_O40_CAPFORM=smooth RL_O40_CAPPCT=20 RL_O40_PGMAT=1"
)
for spec in "${CSPECS[@]}"; do
  T=${spec%%:*}; D=${spec#*:}
  run os_continuity.py "$T" $D
done
