#!/bin/bash
# A1 — THE LOOKALIKE TRIPWIRE BITES. Copy the canonical suite runner to a NEW path; assert the suite HALTs
# and names the file (H1); delete it; assert the suite is green again. Uses the fast SGC_HARNESS_ONLY path.
set -uo pipefail
ROOT=/home/user/afl-rl-engine
OUT="$ROOT/session_2026-07-14/harness_guard/out"
COPY="$ROOT/ship_gates_lookalike_COPY.py"
cd "$ROOT"
cp ship_gates_check.py "$COPY"                                  # a SECOND copy of the harness at a new path
SGC_HARNESS_ONLY=1 RL_REPO="$ROOT" python3 ship_gates_check.py > "$OUT/a1_copy_present.log" 2>&1; rc_present=$?
rm -f "$COPY"                                                    # remove the copy
SGC_HARNESS_ONLY=1 RL_REPO="$ROOT" python3 ship_gates_check.py > "$OUT/a1_copy_removed.log" 2>&1; rc_removed=$?
echo "rc_present=$rc_present  rc_removed=$rc_removed"
pass=1
grep -q 'H1  HALT' "$OUT/a1_copy_present.log" || { echo "FAIL: H1 did not HALT on the copy"; pass=0; }
grep -q 'ship_gates_lookalike_COPY.py' "$OUT/a1_copy_present.log" || { echo "FAIL: HALT did not name the copy"; pass=0; }
[ "$rc_present" = 1 ] || { echo "FAIL: exit was not non-zero with copy present"; pass=0; }
grep -q 'H1  PASS' "$OUT/a1_copy_removed.log" || { echo "FAIL: H1 not green after delete"; pass=0; }
[ "$rc_removed" = 0 ] || { echo "FAIL: exit not zero after delete"; pass=0; }
[ "$pass" = 1 ] && echo "A1 PASS" || echo "A1 FAIL"
echo "$([ "$pass" = 1 ] && echo PASS || echo FAIL) rc_present=$rc_present rc_removed=$rc_removed" > "$ROOT/session_2026-07-14/harness_guard/out/rc_A1"
exit $(( pass == 1 ? 0 : 1 ))
