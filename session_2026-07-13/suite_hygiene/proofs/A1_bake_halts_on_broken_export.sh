#!/usr/bin/env bash
# =============================================================================
# ACCEPTANCE A1 — the BAKE SCRIPT HALTS ON A BROKEN EXPORT.
#
# We run the REAL hardened build_final_board.sh control flow, but substitute a
# BROKEN export INTO THE WORKSPACE ONLY (a scratch copy — the repo source
# engine/rl_after/rl_export.py is NEVER touched). The workspace copy is what the
# bake actually invokes (`cd $WS; python3 rl_export.py`), and it is ephemeral
# (re-seeded from the repo by bootstrap), so breaking it is safe.
#
# We snapshot the REAL board file and the REAL expected_boot.json BEFORE, run the
# bake, then ASSERT:
#   (1) the bake exits NON-ZERO,
#   (2) it printed the FATAL halt line and did NOT print "FINAL BUILD DONE",
#   (3) the committed board data/rl_build/rl_app_data.json is BYTE-IDENTICAL,
#   (4) data/expected_boot.json 'board' pin is BYTE-IDENTICAL (still 3dc19fbb),
#   (5) nothing was re-extracted / published.
# =============================================================================
set -uo pipefail
REPO=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
SCR="$REPO/session_2026-07-13/suite_hygiene/proofs"
LOG="$SCR/A1_run.log"

# --- snapshot real state BEFORE -------------------------------------------------
BOARD="$REPO/data/rl_build/rl_app_data.json"
PIN="$REPO/data/expected_boot.json"
board_before=$(md5sum "$BOARD" | cut -d' ' -f1)
pin_before=$(md5sum "$PIN" | cut -d' ' -f1)
pinboard_before=$(python3 -c "import json;print(json.load(open('$PIN'))['board'][:8])")

# --- build a scratch copy of the bake script with a BROKEN workspace export -----
# Insert, right after the bootstrap re-seed, a line that overwrites the WORKSPACE
# rl_export.py (only) with a scratch copy that fails immediately. Everything else
# in the script is byte-for-byte the real hardened script.
BROKEN="$SCR/rl_export_BROKEN.py"
{ echo 'import sys; sys.stderr.write("INDUCED SUITE-HYGIENE PROOF: rl_export deliberately broken\n"); raise SystemExit(3)'; } > "$BROKEN"

SRC="$REPO/session_2026-07-13/v2_9_export_display/scripts/build_final_board.sh"
PROOF_SH="$SCR/_build_final_board_BROKENEXPORT.sh"
awk -v broken="$BROKEN" -v ws="$WS" '
  { print }
  /^echo "bootstrap OK/ { print "cp -f \"" broken "\" \"" ws "/rl_export.py\"   # A1 PROOF: break the WORKSPACE export copy only" }
' "$SRC" > "$PROOF_SH"
chmod +x "$PROOF_SH"

# --- run it ---------------------------------------------------------------------
echo "### running the REAL hardened bake with a broken workspace export ###" | tee "$LOG"
set +e
bash "$PROOF_SH" >> "$LOG" 2>&1
rc=$?
set -e 2>/dev/null || true

# --- snapshot real state AFTER --------------------------------------------------
board_after=$(md5sum "$BOARD" | cut -d' ' -f1)
pin_after=$(md5sum "$PIN" | cut -d' ' -f1)
pinboard_after=$(python3 -c "import json;print(json.load(open('$PIN'))['board'][:8])")

echo "" | tee -a "$LOG"
echo "=================== A1 ASSERTIONS ===================" | tee -a "$LOG"
fail=0
chk(){ if [ "$2" = "$3" ]; then echo "PASS  $1 ($2)" | tee -a "$LOG"; else echo "FAIL  $1: got [$2] want [$3]" | tee -a "$LOG"; fail=1; fi; }
[ "$rc" -ne 0 ] && echo "PASS  bake exited NON-ZERO (rc=$rc)" | tee -a "$LOG" || { echo "FAIL  bake exited 0 — DID NOT HALT" | tee -a "$LOG"; fail=1; }
grep -q "FATAL: rl_export.py failed" "$LOG" && echo "PASS  printed the FATAL halt line" | tee -a "$LOG" || { echo "FAIL  no FATAL halt line" | tee -a "$LOG"; fail=1; }
grep -q "FINAL BUILD DONE" "$LOG" && { echo "FAIL  reached FINAL BUILD DONE (published!)" | tee -a "$LOG"; fail=1; } || echo "PASS  never reached FINAL BUILD DONE (nothing published)" | tee -a "$LOG"
grep -q "re-pinned" "$LOG" && { echo "FAIL  re-pinned the board" | tee -a "$LOG"; fail=1; } || echo "PASS  no re-pin occurred" | tee -a "$LOG"
chk "committed board byte-identical" "$board_after" "$board_before"
chk "expected_boot.json byte-identical" "$pin_after" "$pin_before"
chk "board pin still 3dc19fbb" "$pinboard_after" "$pinboard_before"
echo "----------------------------------------------------" | tee -a "$LOG"
[ "$fail" = 0 ] && echo "A1 RESULT: PASS  (bake HALTED, published nothing, re-pinned nothing)" | tee -a "$LOG" || echo "A1 RESULT: FAIL" | tee -a "$LOG"

# --- restore the workspace (bootstrap re-seeds the good export) -----------------
bash "$REPO/bootstrap.sh" >/dev/null 2>&1 && echo "(workspace restored via bootstrap)" | tee -a "$LOG"
exit "$fail"
