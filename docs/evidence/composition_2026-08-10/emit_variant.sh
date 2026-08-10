#!/bin/bash
# PER-ENTRANT COHORT-BOOK EMIT, PER ENGINE VARIANT — the project's standing instrument.
#
# The relativity/landing/envelope numbers I reported earlier were LIVE-BOARD CROSS-SECTIONS. The
# owner is right that the standing instrument for cohort progression and no-arb is the HISTORICAL
# cohort book, so every one of those readings is re-emitted here on emit_matrix_338.py, the
# instrument of record, once per engine variant.
#
# COST WARNING, stated because the record should carry the price: this is a 24-year walk-forward
# (ASOF 2003..2026) re-pricing every eligible entrant at every as-of year — of order 60,000 ev()
# calls per variant, each of which runs the full forward valuation. It is far more expensive than a
# board build. Each emit is timed and the cost is printed.
#
# Usage: emit_variant.sh <label> <git-ref> [VAR=VAL ...]
#   pre-act engine = origin/main; every act variant = HEAD with its dials
set -uo pipefail
LABEL="$1"; REF="$2"; shift 2
REPO=/home/user/afl-rl-engine
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_emit_$LABEL
OUT=$SP/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" "$REF" >/dev/null 2>&1 || { echo "WORKTREE FAILED ($REF)"; exit 1; }
mkdir -p "$OUT"

python3 - "$WT" "$@" <<'PY'
import json, sys, pathlib, hashlib
wt = sys.argv[1]; kv = [a.split('=',1) for a in sys.argv[2:]]
m = pathlib.Path(wt+'/data/model_config.json'); d = json.loads(m.read_text())
for k,v in kv:
    if k in d['vars']: d['vars'][k] = v
m.write_text(json.dumps(d, indent=1)+"\n")
sys.path.insert(0, wt)
import config_manifest as CM, fv_provenance as F
H = CM.canonical_hash(CM.load(wt)['vars'])
d = json.loads(m.read_text()); d['config_sha256'] = H; m.write_text(json.dumps(d, indent=1)+"\n")
md5 = lambda p: hashlib.md5(open(p,'rb').read()).hexdigest()
b = pathlib.Path(wt+'/data/expected_boot.json'); e = json.loads(b.read_text())
e['config']=H; e['fv']=F.fv_identity(wt+'/engine/forward_valuation')
e['rl_model']=md5(wt+'/engine/rl_after/rl_model.py'); e['engine_head']=md5(wt+'/engine/rl_after/_merged_recover.py')
b.write_text(json.dumps(e, indent=1)+"\n")
print("  variant:", " ".join("%s=%s"%(k,v) for k,v in kv) or "(HEAD defaults)")
PY

cp "$REPO/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUT/emit.py"
# THE DIALS MUST BE EXPORTED. Unlike rl_export.py, emit_matrix_338.py does NOT call
# config_manifest.enforce() — it execs _merged_recover.py directly. The engine's dials read the
# ENVIRONMENT, so editing the worktree manifest alone leaves every variant identical to the base.
# That is exactly what happened on the first V2/V3 emits: both reproduced FULL to the digit.
for a in "$@"; do export "$a"; done
echo "  dials exported: ${*:-none}"
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
echo "  emit starting $(date -u +%H:%M:%S)"
S=$(date +%s)
python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1
rc=$?; E=$(date +%s)
echo "  emit exit=$rc  COST: $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUT/per_entrant_338_confirmation.json" ]; then
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/per_entrant_$LABEL.json"
  echo "  OK -> per_entrant_$LABEL.json  ($(md5sum "$SP/per_entrant_$LABEL.json" | cut -c1-8))"
else
  echo "  NO MATRIX — see $OUT/emit.log"; tail -5 "$OUT/emit.log"
fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
