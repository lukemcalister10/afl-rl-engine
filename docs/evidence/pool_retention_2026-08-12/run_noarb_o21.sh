#!/bin/bash
# ORDER 21 -- run BOTH cohort instruments on the SHIP and STAGED matrices.
# Both canonical instruments are COPIED, NEVER MODIFIED. noarb_table_allarm.py asserts
# noarb_table_338.py's md5 0f8220351c64c56ccfa90c60edcdfa5f at run and refuses to proceed otherwise.
# They are run from a scratchpad copy because both write their json beside themselves and the
# composition evidence directory is filed evidence.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
N=$SP/o21/noarb
export PATH=/root/rl_venv312/bin:$PATH
export OPENBLAS_NUM_THREADS=1 PYTHONHASHSEED=0
mkdir -p "$N"
cp "$REPO"/docs/evidence/composition_2026-08-10/noarb/noarb_table_338.py \
   "$REPO"/docs/evidence/composition_2026-08-10/noarb/noarb_table_allarm.py \
   "$REPO"/docs/evidence/composition_2026-08-10/noarb/harness_pvc_REPINNED_pass3.py "$N/"
echo "instrument pin at run: $(md5sum "$N/noarb_table_338.py" | cut -c1-32)"
cd "$N"
for L in SHIP DERIVED; do
  echo "=== $L ==="
  python noarb_table_338.py "$SP/per_entrant_O21$L.json" > "t338_$L.txt" 2>&1
  [ -f noarb_table_338.json ] && mv noarb_table_338.json "table_$L.json"
  python noarb_table_allarm.py "$SP/per_entrant_O21$L.json" "$L" > "allarm_$L.txt" 2>&1
  tail -3 "t338_$L.txt"
done
ls -la "$N"
