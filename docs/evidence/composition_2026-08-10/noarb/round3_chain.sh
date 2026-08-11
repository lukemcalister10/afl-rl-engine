#!/bin/bash
# One emit lane. Args: a series of "LABEL:DIAL=V,DIAL=V" (or "LABEL:" for HEAD defaults).
set -uo pipefail
EV=/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10
for spec in "$@"; do
  L="${spec%%:*}"; D="${spec#*:}"
  DIALS=$(echo "$D" | tr ',' ' ')
  echo "=== LANE START $L $(date -u +%H:%M:%S) ==="
  bash "$EV/emit_variant.sh" "$L" HEAD $DIALS
done
echo "LANE_DONE"
