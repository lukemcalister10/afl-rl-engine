#!/bin/bash
# ORDER R — the in-process measurement suite. STRICTLY SEQUENTIAL: every one of these loads the
# engine, so none of them may run beside a board build or beside each other.
#   or_census.py     the burn census, the birthday census, the CHARGE DISTRIBUTION and the named rows
#   or_continuity.py continuity on every axis, on the EFFECTIVE constants
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONHASHSEED=0
cd "$HERE"
B1="RL_O37=1 RL_O38B1=1"
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
echo "=== ORDER R CENSUSES — 13 boards, strictly sequential ==="
# ORDER K needs no census run of its own: its charge factor is the f_K field the leg recorder
# captures on every board, and or_arc.py reads it off the ORDER P census. Declared, not hidden.
run or_census.py RP     RL_O37=1
run or_census.py RB1    RL_O37=1 RL_O38B1=1
run or_census.py RAB1   RL_O37=1 RL_O38A=1 RL_O38B1=1
run or_census.py R15    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run or_census.py R20    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run or_census.py R15A   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run or_census.py R20A   RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run or_census.py Rb1    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=0.111
run or_census.py Rb2    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=0.105
run or_census.py R15b1  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15 RL_O39_BETASAT=0.111
run or_census.py R20b2  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105
run or_census.py R20b2A RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105
echo
echo "=== ORDER R CONTINUITY — the base, the two levers and both corners ==="
run or_continuity.py RP     RL_O37=1
run or_continuity.py RB1    RL_O37=1 RL_O38B1=1
run or_continuity.py R15    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=15
run or_continuity.py R20    RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20
run or_continuity.py Rb2    RL_O37=1 RL_O38B1=1 RL_O39_BETASAT=0.105
run or_continuity.py R20b2  RL_O37=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105
run or_continuity.py R20b2A RL_O37=1 RL_O38A=1 RL_O38B1=1 RL_O39_TMAXPCT=20 RL_O39_BETASAT=0.105
echo; echo "=== MEASUREMENT SUITE DONE ==="
