#!/bin/bash
# ROUND 2 — the identity proof FIRST, then the three candidates.
# IDENT must reproduce per_entrant_FULL.json (md5 c698b5b2) exactly. If it does not, the three new
# dials are not inert when off and NOTHING after it may be read — see PREREG_ROUND2.md.
set -uo pipefail
HERE=$(dirname "$(readlink -f "$0")")
EV=$(dirname "$HERE")
bash "$EV/emit_variant.sh" IDENT  HEAD
bash "$EV/emit_variant.sh" AFLOOR HEAD RL_A_FLOOR=1
bash "$EV/emit_variant.sh" ADRAG  HEAD RL_A_DRAGFADE=1
bash "$EV/emit_variant.sh" V4     HEAD RL_AGE_DISC=1 RL_AGE_DISC_MODE=4
echo "ROUND2_DONE"
