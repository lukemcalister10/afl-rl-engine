#!/bin/bash
# THE H LADDER — three emits of the FULL package at RL_C_H = 1.20 / 1.25 / 1.30.
#
# FULL@1.13 is the baseline and already exists (per_entrant_FULL.json, c698b5b2), so no identity
# re-proof is claimed here. All three rungs sit INSIDE the dial's derived admissible window
# [1.1024, 1.3327] on the #336 basis — the ladder does not leave it.
#
# DIALS ARE BOTH EXPORTED AND WRITTEN, and which is printed. emit_matrix_338.py does NOT call
# config_manifest.enforce(); it execs the engine head directly, so the engine reads the ENVIRONMENT.
# Writing the manifest alone silently produces a copy of the baseline — that is the exact bug that
# invalidated the first V2/V3 emits, and emit_variant.sh now does both.
set -uo pipefail
HERE=$(dirname "$(readlink -f "$0")")
EV=$(dirname "$HERE")
for H in 1.20 1.25 1.30; do
  L="H$(echo "$H" | tr -d '.')"
  echo "=== rung RL_C_H=$H  -> label $L"
  bash "$EV/emit_variant.sh" "$L" HEAD "RL_C_H=$H"
done
echo "H_LADDER_DONE"
