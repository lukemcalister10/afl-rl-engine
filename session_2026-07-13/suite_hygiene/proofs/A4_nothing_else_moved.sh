#!/usr/bin/env bash
# =============================================================================
# ACCEPTANCE A4 — NOTHING ELSE MOVED.
# This job changes how failures PROPAGATE, never what any gate COMPUTES. Prove it:
#   (1) the store is byte-unchanged (repo source AND seeded workspace == 340a7a32),
#   (2) the board is byte-unchanged (data/rl_build/rl_app_data.json == 3dc19fbb) and
#       the boot pin still names 3dc19fbb,
#   (3) the ONLY non-session-dir files changed vs the pre-work base (2bc5151, the
#       merge of PR #70) are the FIVE named harness/doc files,
#   (4) no GATE CONSTRUCTION changed — engine ev()/_merged_recover, config_manifest,
#       model_config.json, and the suite driver ship_gates_check.py are byte-identical
#       to the base.
# Pure git + md5 — this proof NEVER loads the engine.
# =============================================================================
set -uo pipefail
REPO=/home/user/afl-rl-engine
cd "$REPO"
BASE=$(git rev-parse 2bc5151)          # pre-work base = merge of PR #70
OUT="$REPO/session_2026-07-13/suite_hygiene/proofs/A4_run.log"
: > "$OUT"
say(){ echo "$@" | tee -a "$OUT"; }
fail=0
chk(){ if [ "$2" = "$3" ]; then say "PASS  $1 ($2)"; else say "FAIL  $1: got [$2] want [$3]"; fail=1; fi; }

say "===== A4 — NOTHING ELSE MOVED (base $BASE) ====="

# (1) store byte-unchanged
STORE_REPO=$(md5sum engine/rl_after/rl_model_data.json | cut -c1-8)
STORE_WS=$(md5sum /home/claude/rl_workspace/rl_after/rl_model_data.json 2>/dev/null | cut -c1-8)
chk "store (repo source) == 340a7a32" "$STORE_REPO" "340a7a32"
chk "store (seeded workspace) == 340a7a32" "$STORE_WS" "340a7a32"

# (2) board byte-unchanged + pin
BOARD=$(md5sum data/rl_build/rl_app_data.json | cut -c1-8)
PIN=$(python3 -c "import json;print(json.load(open('data/expected_boot.json'))['board'][:8])")
chk "board (rl_app_data.json) == 3dc19fbb" "$BOARD" "3dc19fbb"
chk "boot pin 'board' == 3dc19fbb" "$PIN" "3dc19fbb"

# (3) the ONLY non-session-dir changes are the five named files
say "----- files changed vs base, OUTSIDE session_2026-07-13/suite_hygiene/ -----"
NONSESSION=$(git diff --name-only "$BASE" HEAD | grep -v '^session_2026-07-13/suite_hygiene/' | sort)
echo "$NONSESSION" | sed 's/^/  /' | tee -a "$OUT"
EXPECTED=$(printf '%s\n' \
  "SHIP_GATES.md" \
  "bootstrap.sh" \
  "run_panel.sh" \
  "session_2026-07-13/v2_9_export_display/scripts/build_final_board.sh" \
  "verify_restore.sh" | sort)
if [ "$NONSESSION" = "$EXPECTED" ]; then say "PASS  non-session changes == the 5 named harness/doc files ONLY"; else say "FAIL  unexpected non-session changes (see list above)"; fail=1; fi

# (4) no GATE CONSTRUCTION touched
say "----- gate-construction files: byte-identical to base? -----"
for f in \
  engine/rl_after/_merged_recover.py \
  engine/rl_after/rl_model.py \
  config_manifest.py \
  data/model_config.json \
  ship_gates_check.py \
  one_source_selftest.py \
  boot_guard.py ; do
  if [ ! -e "$f" ]; then say "n/a   $f (not present)"; continue; fi
  if git diff --quiet "$BASE" HEAD -- "$f"; then say "PASS  unchanged: $f"; else say "FAIL  CHANGED: $f"; fail=1; fi
done

say "-------------------------------------------------------------"
[ "$fail" = 0 ] && say "A4 RESULT: PASS  (store/board byte-unchanged; only the 5 files moved; no gate construction touched)" || say "A4 RESULT: FAIL"
exit "$fail"
