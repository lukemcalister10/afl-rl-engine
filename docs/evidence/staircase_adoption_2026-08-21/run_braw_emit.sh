#!/bin/bash
# THE B-RAW NO-ARB EMIT — the leg the pricing seat named in PACKET_STAIRCASE.md §0 and left open.
#
# docs/evidence/staircase_fix_2026-08-20/run_all_emits.sh (the pricing seat's own runner), carried
# with ONE declared change and nothing else: the label/dial pair is SFXBRAW / RL_O44_LVLMONO=smooth
# — VARIANT B RAW, THE ADOPTED ARM — instead of the two conserved arms it already ran.
#
# Everything else is that file's: the same emitter, the same build lock, the same day-0 reference
# (DAY0_SFXBASE.json, this act's own base reference on the live board, 87 of 87 at tolerance 0),
# the same RL_CONFIG_MODE-unset disclosure (RL_O44_LVLMONO is deliberately not a manifest dial, so a
# gate-mode candidate emit would HALT on line one; enforce() is a no-op unset and changes no value,
# and mode-invariance of the OFF board is MEASURED in BUILD_F1_out.txt).
#
# NOTHING IS ADOPTED BY THIS SCRIPT. NO BOARD PIN MOVES. NO ENGINE FILE IS EDITED.
set -uo pipefail
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
cd /home/user/afl-rl-engine
export PATH="/root/rl_venv312/bin:$PATH"
export RL_DAY0_FINAL=$SP/sfx/DAY0_SFXBASE.json
source tools/build_lock.sh && build_lock_acquire sfx-braw-emit 7200 || exit 1
echo "### SFXBRAW (smooth = VARIANT B RAW, THE ADOPTED ARM) ###"
RL_O44_LVLMONO=smooth SFX_LABEL=SFXBRAW bash docs/evidence/staircase_fix_2026-08-20/run_emit_SFX.sh
build_lock_release
echo "### DONE ###"
