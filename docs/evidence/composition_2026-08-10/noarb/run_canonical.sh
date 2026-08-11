#!/bin/bash
# THE CANONICAL INSTRUMENT, RUN UNMODIFIED, ONCE PER ENGINE VARIANT.
#
# noarb_table_338.py is byte-identical to the #338 evidence copy and the stage-5 copy
# (md5 0f8220351c64c56ccfa90c60edcdfa5f). Nothing in it is touched. The only thing this act
# re-pointed is the harness's pinned store/v0surf identity — documented in the harness header,
# asserts untouched, and proven able to fire.
#
# STEP 1 (the reproduction gate) is run first and separately: the same untouched script against
# the stage-5 matrix under the STAGE-5 pins must reproduce noarb_table_stage5.txt exactly. That is
# recorded in REPRODUCTION.md. This runner is STEP 2/3 — the five variants under the re-pointed pins.
set -uo pipefail
HERE=$(dirname "$(readlink -f "$0")")
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
export OPENBLAS_NUM_THREADS=1
PY=/root/rl_venv312/bin/python

# Labels default to the five decision variants; pass labels as args for any other set (the H ladder
# uses the SAME code path and the SAME untouched script — there is no second reader).
LABELS="${*:-main FULL V1 V2 V3}"
for L in $LABELS; do
  M="$SP/per_entrant_$L.json"
  if [ ! -f "$M" ]; then echo "MISSING $M"; continue; fi
  $PY "$HERE/noarb_table_338.py" "$M" > "$HERE/table_$L.txt" 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "$L FAILED rc=$rc"; tail -3 "$HERE/table_$L.txt"; continue; fi
  mv "$HERE/noarb_table_338.json" "$HERE/table_$L.json"
  echo "$L OK  matrix_md5=$(md5sum "$M" | cut -c1-8)  table=$(md5sum "$HERE/table_$L.txt" | cut -c1-8)"
done
