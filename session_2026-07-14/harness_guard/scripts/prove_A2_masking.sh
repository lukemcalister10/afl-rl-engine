#!/bin/bash
# A2 — THE MASKING LINT BITES. Add a LIVE runner that pipes a gate through `tail` with no exit-code capture
# (the item-38 signature); assert the suite HALTs and names it (H2); remove it; assert green. Fast path.
set -uo pipefail
ROOT=/home/user/afl-rl-engine
OUT="$ROOT/session_2026-07-14/harness_guard/out"
BAD="$ROOT/run_gates_masked_PROOF.sh"
cd "$ROOT"
cat > "$BAD" <<'EOF'
#!/bin/bash
# a build's run script that MASKS the suite — the exact item-38 signature: the traceback and the exit
# code are both swallowed by `| tail`, so a crashing gate reports a green summary line.
python3 ship_gates_check.py | tail -8
EOF
SGC_HARNESS_ONLY=1 RL_REPO="$ROOT" python3 ship_gates_check.py > "$OUT/a2_mask_present.log" 2>&1; rc_present=$?
rm -f "$BAD"                                                     # remove the masking runner
SGC_HARNESS_ONLY=1 RL_REPO="$ROOT" python3 ship_gates_check.py > "$OUT/a2_mask_removed.log" 2>&1; rc_removed=$?
echo "rc_present=$rc_present  rc_removed=$rc_removed"
pass=1
grep -q 'H2  HALT' "$OUT/a2_mask_present.log" || { echo "FAIL: H2 did not HALT on the masked runner"; pass=0; }
grep -q 'run_gates_masked_PROOF.sh' "$OUT/a2_mask_present.log" || { echo "FAIL: HALT did not name the runner"; pass=0; }
[ "$rc_present" = 1 ] || { echo "FAIL: exit was not non-zero with masked runner present"; pass=0; }
grep -q 'H2  PASS' "$OUT/a2_mask_removed.log" || { echo "FAIL: H2 not green after remove"; pass=0; }
[ "$rc_removed" = 0 ] || { echo "FAIL: exit not zero after remove"; pass=0; }
[ "$pass" = 1 ] && echo "A2 PASS" || echo "A2 FAIL"
echo "$([ "$pass" = 1 ] && echo PASS || echo FAIL) rc_present=$rc_present rc_removed=$rc_removed" > "$OUT/rc_A2"
exit $(( pass == 1 ? 0 : 1 ))
