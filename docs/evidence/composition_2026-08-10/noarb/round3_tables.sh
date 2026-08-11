#!/bin/bash
# Parallel-safe canonical table runs. Each lane gets its OWN directory holding an UNMODIFIED copy of
# noarb_table_338.py (md5 verified after the copy) and the repinned harness, so the instrument's own
# output file (noarb_table_338.json, written next to itself) cannot race between lanes.
set -uo pipefail
LANE="$1"; shift
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
EV=/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10/noarb
D=$SP/o3/tbl_$LANE; rm -rf "$D"; mkdir -p "$D"
cp "$EV/noarb_table_338.py" "$EV/harness_pvc_REPINNED_pass3.py" "$D/"
M=$(md5sum "$D/noarb_table_338.py" | cut -d' ' -f1)
[ "$M" = "0f8220351c64c56ccfa90c60edcdfa5f" ] || { echo "INSTRUMENT MD5 MISMATCH $M"; exit 1; }
export OPENBLAS_NUM_THREADS=1
for L in "$@"; do
  /root/rl_venv312/bin/python "$D/noarb_table_338.py" "$SP/per_entrant_$L.json" > "$EV/table_$L.txt" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "$L FAILED rc=$rc"; tail -3 "$EV/table_$L.txt"; continue; fi
  mv "$D/noarb_table_338.json" "$EV/table_$L.json"
  echo "$L OK  matrix=$(md5sum "$SP/per_entrant_$L.json" | cut -c1-8)  table=$(md5sum "$EV/table_$L.txt" | cut -c1-8)"
done
echo "TBL_LANE_DONE $LANE"
