export PATH="/root/rl_venv312/bin:$PATH"
export RL_REPO="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r24_rehearsal/sandbox"
export CLAUDE_PROJECT_DIR="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r24_rehearsal/sandbox"
export RL_FV="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r24_rehearsal/sandbox/engine/forward_valuation"
export PYTHONPATH="/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/r24_rehearsal/sandbox/engine/rl_after:/home/claude/rl_vendor"
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
# RL_BUILD_LOCK_FILE DELIBERATELY UNSET — it is an RL_-prefixed flag and
# staged_apply._assert_config_policy refuses any RL_* not in config_manifest.INFRA_ALLOW.
# The lander therefore takes the real shared lock, which is the REAL R24 behaviour too.
export GIT_AUTHOR_NAME=r24-rehearsal GIT_COMMITTER_NAME=r24-rehearsal
export GIT_AUTHOR_EMAIL=rehearsal@sandbox.local GIT_COMMITTER_EMAIL=rehearsal@sandbox.local
