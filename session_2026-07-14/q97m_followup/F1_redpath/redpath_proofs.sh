#!/bin/bash
# RED-PATH PROOFS.
#  A3 (P1): the EXISTING (0d) repo-checkout assertion — corrupt data/q97m.pkl => HALT naming it => restore => PASS;
#           same for a newly-pinned artifact (bust_prior_table.json).
#  F1: the NEW (0e) loaded-path assertion — RL_Q97M_PKL -> corrupt => HALT; stale workspace copy => HALT; restore => PASS.
# boot_guard exits non-zero (1) on HALT, 0 on PASS. We assert the exit code AND that the message names the path.
set -uo pipefail
export PATH="/root/rl_venv312/bin:$PATH"
MAIN=/home/user/afl-rl-engine
export RL_REPO="$MAIN"
WS=/home/claude/rl_workspace/rl_after
export PYTHONPATH=$WS:/home/claude/rl_vendor
STORE=$WS/rl_model_data.json
OUT=$MAIN/session_2026-07-14/q97m_followup/F1_redpath
LOG=$OUT/redpath_results.txt
: > "$LOG"
run_guard () { RL_REPO="$MAIN" python3 "$MAIN/boot_guard.py" redpath "$STORE" 2>&1; echo "rc=$?"; }
say () { echo "$@" | tee -a "$LOG"; }

say "RED-PATH PROOFS — $(date -u +%FT%TZ)"
say "================================================================"

# baseline PASS
say "[0] BASELINE (clean) — expect PASS rc=0"
run_guard | tee -a "$LOG" | grep -E 'PASS|FAILED|rc=' | tail -3

# ---- A3 proof 1: corrupt the REPO data/q97m.pkl (0d) ----
say ""; say "[A3.1] corrupt data/q97m.pkl (repo) — expect (0d) HALT naming q97m, rc=1"
cp "$MAIN/data/q97m.pkl" /tmp/q97m.bak
printf 'CORRUPT' >> "$MAIN/data/q97m.pkl"
run_guard | tee -a "$LOG" | grep -Ei 'q97m|HALT|FAILED|rc=' | tail -4
cp /tmp/q97m.bak "$MAIN/data/q97m.pkl"
say "  -> restored data/q97m.pkl (md5 $(md5sum "$MAIN/data/q97m.pkl"|cut -c1-8)); re-run expect PASS"
run_guard | grep -E 'PASS|rc=' | tail -2 | tee -a "$LOG"

# ---- A3 proof 2: corrupt a newly-pinned artifact bust_prior_table.json (0d) ----
say ""; say "[A3.2] corrupt engine/rl_after/bust_prior_table.json (newly pinned) — expect (0d) HALT naming bust_prior, rc=1"
cp "$MAIN/engine/rl_after/bust_prior_table.json" /tmp/bust.bak
printf '\n"corrupt"' >> "$MAIN/engine/rl_after/bust_prior_table.json"
run_guard | tee -a "$LOG" | grep -Ei 'bust_prior|HALT|FAILED|rc=' | tail -4
cp /tmp/bust.bak "$MAIN/engine/rl_after/bust_prior_table.json"
say "  -> restored bust_prior_table.json; re-run expect PASS"
run_guard | grep -E 'PASS|rc=' | tail -2 | tee -a "$LOG"

# ---- F1 proof 1: RL_Q97M_PKL points at a corrupt pickle (0e loaded-path) ----
say ""; say "[F1.1] RL_Q97M_PKL -> corrupt pickle (engine WOULD load it) — expect (0e) LOAD-PATH HALT, rc=1"
cp "$MAIN/data/q97m.pkl" /tmp/q97m_corrupt.pkl; printf 'CORRUPT' >> /tmp/q97m_corrupt.pkl
( export RL_Q97M_PKL=/tmp/q97m_corrupt.pkl; run_guard ) | tee -a "$LOG" | grep -Ei 'LOAD-PATH|q97m|HALT|rc=' | tail -5
say "  -> unset RL_Q97M_PKL; re-run expect PASS"
run_guard | grep -E 'PASS|rc=' | tail -2 | tee -a "$LOG"

# ---- F1 proof 2: stale the WORKSPACE copy /home/claude/q97m.pkl (0e loaded-path) ----
say ""; say "[F1.2] stale /home/claude/q97m.pkl (workspace copy the engine loads) — expect (0e) LOAD-PATH HALT, rc=1"
cp /home/claude/q97m.pkl /tmp/ws_q97m.bak
printf 'STALE' >> /home/claude/q97m.pkl
run_guard | tee -a "$LOG" | grep -Ei 'LOAD-PATH|q97m|HALT|rc=' | tail -5
cp /tmp/ws_q97m.bak /home/claude/q97m.pkl
say "  -> restored /home/claude/q97m.pkl (md5 $(md5sum /home/claude/q97m.pkl|cut -c1-8)); re-run expect PASS"
run_guard | grep -E 'PASS|rc=' | tail -2 | tee -a "$LOG"

say ""; say "DONE_redpath — final git status (must be clean; all repo files restored):"
cd "$MAIN"; git status --short | tee -a "$LOG"
