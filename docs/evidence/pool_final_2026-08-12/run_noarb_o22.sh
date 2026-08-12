#!/bin/bash
# ORDER 22 -- run BOTH cohort instruments on any set of matrices.
# Sibling of docs/evidence/pool_retention_2026-08-12/run_noarb_o21.sh, carried; the ONE change is that
# the matrix labels are arguments instead of a fixed pair.
#
# BOTH CANONICAL INSTRUMENTS ARE COPIED, NEVER MODIFIED. noarb_table_allarm.py asserts
# noarb_table_338.py's md5 at run and refuses to proceed otherwise. The md5 is COMPUTED here and
# printed -- never hardcoded.
#
# Usage: run_noarb_o22.sh <matrixfile> <label> [<matrixfile> <label> ...]
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/o22/noarb
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 PYTHONHASHSEED=0
mkdir -p "$N"
cp "$REPO"/docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py \
   "$REPO"/docs/evidence/composition_2026-08-10/noarb/noarb_table_allarm.py \
   "$REPO"/docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py "$N/"
echo "instrument pin COMPUTED at run: noarb_table_338.py $(md5sum "$N/noarb_table_338.py" | cut -c1-32)"
echo "                                noarb_table_allarm.py $(md5sum "$N/noarb_table_allarm.py" | cut -c1-32)"
cd "$N"
while [ "$#" -ge 2 ]; do
  MX="$1"; L="$2"; shift 2
  echo "=== $L  ($(md5sum "$MX" | cut -c1-8)) ==="
  python noarb_table_338.py "$MX" > "t338_$L.txt" 2>&1
  [ -f noarb_table_338.json ] && mv noarb_table_338.json "table_$L.json"
  python noarb_table_allarm.py "$MX" "$L" > "allarm_$L.txt" 2>&1
  tail -3 "t338_$L.txt"
done
ls "$N"
