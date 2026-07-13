#!/bin/bash
# Patch the workspace engine from PRISTINE with a lever set, run a mode, then RESTORE + md5-verify.
# Never leaves the workspace dirty (trap restore on EXIT). The repo engine is never touched.
#   usage: run_levers.sh <levers> <mode> <out>
#     levers : comma set of {L1,L2,L3,L4} or "" for base
#     mode   : board | matrix
#     out    : output json path
set -e
LEVERS="$1"; MODE="$2"; OUT="$3"
RA=/home/claude/rl_workspace/rl_after
REPO=/home/user/afl-rl-engine
SCRIPTS="$REPO/session_2026-07-13/v2_9_continuation/scripts"
SC=/tmp/claude-0/-home-user-afl-rl-engine/3c2e6b18-8ee5-5535-9b38-adbb45999814/scratchpad
export PYTHONPATH="$RA:/home/claude/rl_vendor"
cd "$RA"

# pristine snapshot (once per session); assert it is the pinned candidate engine before trusting it
if [ ! -f "$SC/mr_pristine.py" ]; then cp "$RA/_merged_recover.py" "$SC/mr_pristine.py"; fi
if [ ! -f "$SC/rlm_pristine.py" ]; then cp "$RA/rl_model.py" "$SC/rlm_pristine.py"; fi
MR_PRIS=$(md5sum "$SC/mr_pristine.py" | cut -c1-8)
RLM_PRIS=$(md5sum "$SC/rlm_pristine.py" | cut -c1-8)

restore() {
  cp -f "$SC/mr_pristine.py" "$RA/_merged_recover.py"
  cp -f "$SC/rlm_pristine.py" "$RA/rl_model.py"
  NOW_MR=$(md5sum "$RA/_merged_recover.py" | cut -c1-8)
  NOW_RLM=$(md5sum "$RA/rl_model.py" | cut -c1-8)
  [ "$NOW_MR" = "$MR_PRIS" ] && [ "$NOW_RLM" = "$RLM_PRIS" ] || { echo "RESTORE FAILED ($NOW_MR/$NOW_RLM != $MR_PRIS/$RLM_PRIS)"; exit 2; }
  echo "[restore] engine pristine ($MR_PRIS/$RLM_PRIS)"
}
trap restore EXIT

# patch disk from pristine
python3 - "$LEVERS" "$SC/mr_pristine.py" "$SC/rlm_pristine.py" "$RA/_merged_recover.py" "$RA/rl_model.py" <<PY
import sys
sys.path.insert(0, "$SCRIPTS")
import levers as LV
levs, mrp, rlmp, mro, rlmo = sys.argv[1:6]
mr = open(mrp).read(); rlm = open(rlmp).read()
mr2, rlm2 = LV.patch(levs, mr, rlm)
open(mro, "w").write(mr2); open(rlmo, "w").write(rlm2)
print("[patch] levers=[%s]  mr %s->%s  rlm %s->%s" % (levs or "BASE",
      __import__("hashlib").md5(mr.encode()).hexdigest()[:8], __import__("hashlib").md5(mr2.encode()).hexdigest()[:8],
      __import__("hashlib").md5(rlm.encode()).hexdigest()[:8], __import__("hashlib").md5(rlm2.encode()).hexdigest()[:8]))
PY

if [ "$MODE" = "board" ]; then
  python3 "$SCRIPTS/board_pass.py" "$OUT" "[$LEVERS]"
elif [ "$MODE" = "matrix" ]; then
  S4_MATRIX="$OUT" RL_CONFIG_MODE=gate RL_REPO="$REPO" python3 s4_matrix_M1v7.py | tail -3
else
  echo "unknown mode $MODE"; exit 1
fi
# restore runs via trap
