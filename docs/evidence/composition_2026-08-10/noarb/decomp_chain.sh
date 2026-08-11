#!/bin/bash
# PER-ITEM DECOMPOSITION of the main->FULL year-1 drop, on the CANONICAL instrument.
#
# Single-item-removed variants, each through a DECLARED kill-switch — the repo's own attribution
# method. Each arm is FULL with exactly one item switched off, so (FULL - arm) is that item's share.
#
#   noA    RL_ITEM_A=0   the year-1+ anchor blend
#   noSUR  RL_SUR_W=0    the surprise law   (engine comment: "RL_SUR_W=0 => exponent 1 => byte-exact")
#   noH    RL_ITEM_H=0   the sitter cuts
#
# #336 IS NOT IN THIS CHAIN AND THAT IS A FINDING, NOT AN OMISSION. It has NO declared kill-switch,
# and it landed as a mid-stack commit (9a8bbd9) with later work built on top, so it cannot be removed
# by git ref either. It is handled separately — see decomp_336.sh / the table's residual line.
set -uo pipefail
HERE=$(dirname "$(readlink -f "$0")")
EV=$(dirname "$HERE")
bash "$EV/emit_variant.sh" noA   HEAD RL_ITEM_A=0
bash "$EV/emit_variant.sh" noSUR HEAD RL_SUR_W=0
bash "$EV/emit_variant.sh" noH   HEAD RL_ITEM_H=0
echo "DECOMP_DONE"
