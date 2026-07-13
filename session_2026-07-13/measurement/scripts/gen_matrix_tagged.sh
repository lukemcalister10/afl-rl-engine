#!/bin/bash
# Generate the OFFICIAL walk-forward cohort matrix (s4_matrix_M1v7.py gate mode) on the TAGGED store (ws_tag).
# usage: gen_matrix_tagged.sh <out_matrix.json>
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
source "$HERE/env.sh"
OUT=$1
cd "$WS_TAG"
S4_MATRIX="$OUT" RL_CONFIG_MODE=gate RL_REPO="$RL_REPO" python3 s4_matrix_M1v7.py
echo "MATRIX_DONE rc=$? bytes=$(wc -c < "$OUT" 2>/dev/null || echo 0)"
