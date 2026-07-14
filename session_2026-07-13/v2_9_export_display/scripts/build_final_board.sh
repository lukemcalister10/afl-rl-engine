#!/bin/bash
# Build the wired v2.9 export/display board with the new fields, re-pin, and re-extract the UI bundle.
# Deterministic + fenced to the export/display layer. Run from the repo root after the attribution
# sidecar (engine/rl_after/export_attribution.json) is built.
set -euo pipefail   # SUITE HYGIENE 2026-07-13: pipefail makes a pipeline's status the FAILING command's,
                    # not the last one's — a masked export can no longer green a bake. (SHIP_GATES §HARNESS)
REPO=/home/user/afl-rl-engine
WS=/home/claude/rl_workspace/rl_after
cd "$REPO"

# 1. re-seed the workspace from THIS checkout (picks up rl_export.py edits + export_attribution.json sidecar)
#    (two statements, not `A && echo`: under set -e a failing left side of && is not reliably fatal, so a
#    broken bootstrap must be a plain simple command that HALTs the bake.)
bash "$REPO/bootstrap.sh" >/tmp/boot.log 2>&1
echo "bootstrap OK (engine $(md5sum $WS/_merged_recover.py|cut -c1-8))"

# 2. generate the wired board under the full six-lever refit env
cd "$WS"
export PYTHONHASHSEED=0 RL_GAMMA=0.85 RL_PICK1=3000 RL_RUCK_TAX=0.25 RL_RECENCY_DECAY=0.72 RL_PRIOR_TREES=400 PAR_RAMPS=22
export PYTHONPATH="$WS:/home/claude/rl_vendor"
export RL_PVCADOPT=1 RL_MSD_POOL_EXCL=1 RL_DIAL14=1 RL_AGE=1 RL_L5_PICKLESS=1
# UNMASKED (SUITE HYGIENE 2026-07-13): capture the export's exit status FIRST, then show the summary
# lines from the log. A bake must NEVER proceed on a broken export — halt here, before any publish or
# re-pin, so we can never pin a board we did not successfully build. (Was: `… | grep … || true`, which
# swallowed a failing export and re-pinned the stale/partial board — the worst site of the class.)
EXPORT_LOG=/tmp/rl_export.log
if python3 rl_export.py > "$EXPORT_LOG" 2>&1; then rc=0; else rc=$?; fi
grep -E "EXPORT ATTRIBUTION|PARITY GATE|exported active|NUMÉRAIRE" "$EXPORT_LOG" || true
if [ "$rc" -ne 0 ]; then
  echo "FATAL: rl_export.py failed (rc=$rc) — NOT publishing, NOT re-pinning the board."
  echo "----- last 40 lines of $EXPORT_LOG -----"
  tail -40 "$EXPORT_LOG"
  exit "$rc"
fi
NEWMD5=$(md5sum "$WS/rl_app_data.json" | cut -c1-8)
echo "new board md5 = $NEWMD5"

# 3. publish to the committed board path + re-pin EXPECTED_BOARD
cp -f "$WS/rl_app_data.json" "$REPO/data/rl_build/rl_app_data.json"
python3 - "$NEWMD5" << 'PY'
import json, sys
md5 = sys.argv[1]
p = "/home/user/afl-rl-engine/data/expected_boot.json"
b = json.load(open(p))
old = b.get("board")
b["board"] = md5
json.dump(b, open(p, "w"), indent=2, sort_keys=True)
print("expected_boot board re-pinned: %s -> %s" % (old, md5))
PY

# 4. re-extract the UI view bundles (ring-fence asserts srcmd5 == the re-pinned board)
cd "$REPO"
python3 ui/tools/extract_board_view.py
echo "FINAL BUILD DONE board=$NEWMD5"
