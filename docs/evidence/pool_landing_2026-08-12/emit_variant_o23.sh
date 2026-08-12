#!/bin/bash
# ORDER 23 -- PER-ENTRANT COHORT-BOOK EMIT (24-year walk-forward) ON THE FULL POOL-UPDATE STAGE.
# Sibling of docs/evidence/pool_final_2026-08-12/emit_variant_o22.sh, same two additions as
# build_board_o23.sh (the surface committed as source, and o23_stage.py with the ND65+ amendment).
#
# Usage: emit_variant_o23.sh <label> <nopatch|derived> <levels.json|nolevels> [VAR=VAL ...]
#   env O23_SURFACE  the retention surface to wire (required unless nopatch)
set -uo pipefail
LABEL="$1"; PATCH="$2"; LEV="$3"; shift 3
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
E22="$REPO/docs/evidence/pool_final_2026-08-12"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o23e_$LABEL
OUT=$SP/o23/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: HEAD -> $(git -C "$WT" rev-parse --short HEAD)"
mkdir -p "$OUT"

if [ "$PATCH" != "nopatch" ]; then
  echo "  surface: ${O23_SURFACE}"
  python3 "$E22/o21_patch.py" "$WT" "$PATCH" "${O23_SURFACE}" || { echo "PATCH FAILED"; exit 1; }
  python3 "$HERE/o23_surface_source.py" "$WT" "${O23_SURFACE}" || { echo "SURFACE SOURCE FAILED"; exit 1; }
fi
if [ "$LEV" != "nolevels" ]; then
  python3 "$HERE/o23_stage.py" "$WT" "$LEV" || { echo "STAGE FAILED"; exit 1; }
fi

python3 - "$WT" "$@" <<'PY'
import json, sys, pathlib, hashlib
wt = sys.argv[1]; kv = [a.split('=',1) for a in sys.argv[2:]]
m = pathlib.Path(wt+'/data/model_config.json'); d = json.loads(m.read_text())
for k,v in kv:
    assert k in d['vars'], "unknown manifest var %s" % k
    d['vars'][k] = v
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
print("  rl_model:", e['rl_model'][:8], " engine_head:", e['engine_head'][:8],
      " curve_artifact:", md5(wt+'/engine/rl_after/pvc_curve_v2.json')[:8])
PY

cp "$REPO/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUT/emit.py"
# THE DIALS MUST BE EXPORTED: emit_matrix_338.py does not call config_manifest.enforce(), it execs the
# engine head directly and the dials read the ENVIRONMENT (the documented V2/V3 bug).
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
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/per_entrant_O23$LABEL.json"
  echo "  OK -> per_entrant_O23$LABEL.json  ($(md5sum "$SP/per_entrant_O23$LABEL.json" | cut -c1-8))"
else
  echo "  NO MATRIX -- see $OUT/emit.log"; tail -12 "$OUT/emit.log"; fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
