#!/bin/bash
# Regenerate the R-i pause-vs-advance comparison table (fork-i). Runs the engine TWICE (RL_LTI_CLOCK=pause
# then advance) via ri_worker.py in the bootstrapped workspace, then diffs into artifacts/R-i_comparison_table.md.
# A flip of R-i is exactly this config change (RL_LTI_CLOCK), never a rebuild.
set -e
HERE=$(cd "$(dirname "$0")" && pwd); REPO=$(cd "$HERE/../.." && pwd); WS=/home/claude/rl_workspace/rl_after
python3 "$REPO/session_2026-07-09/injury_build/restamp_head.py" >/dev/null
bash "$REPO/bootstrap.sh" >/dev/null 2>&1
cp "$HERE/ri_worker.py" "$WS/"
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH=/home/claude/rl_workspace/rl_after:/home/claude/rl_vendor
RL_LTI_CLOCK=pause   python3 ri_worker.py /tmp/ri_pause.json
RL_LTI_CLOCK=advance python3 ri_worker.py /tmp/ri_advance.json
python3 "$HERE/ri_render.py" /tmp/ri_pause.json /tmp/ri_advance.json "$HERE/artifacts/R-i_comparison_table.md"
echo "R-i table -> $HERE/artifacts/R-i_comparison_table.md"
