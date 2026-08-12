#!/bin/bash
# ORDER 22 -- BUILD A VARIANT BOARD. Sibling of docs/evidence/pool_retention_2026-08-12/build_board_o21.sh,
# CARRIED VERBATIM except for ONE addition: an optional levels stage (o22_levels.py) applied to the
# scratchpad worktree's pvc_curve_v2.json BEFORE the identity restamp, so the built board's engine
# identity records the levels that produced it.
#
# THE CHECKOUT'S data/rl_build/rl_app_data.json, engine AND pvc_curve_v2.json ARE NEVER WRITTEN.
#
# Usage: build_board_o22.sh <outfile> <nopatch|derived|derived_sit|liftR|liftRboth> <levels.json|nolevels> [VAR=VAL ...]
set -uo pipefail
OUT="$1"; PATCH="$2"; LEV="$3"; shift 3
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o22_$(basename "$OUT" .json)
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }

echo "  surface: ${O22_SURFACE:-$HERE/POOL_RETENTION_SURFACE.json}"
if [ "$PATCH" != "nopatch" ]; then
  python3 "$HERE/o21_patch.py" "$WT" "$PATCH" "${O22_SURFACE:-$HERE/POOL_RETENTION_SURFACE.json}" || { echo "PATCH FAILED"; exit 1; }
fi
if [ "$LEV" != "nolevels" ]; then
  python3 "$HERE/o22_levels.py" "$WT" "$LEV" || { echo "LEVELS FAILED"; exit 1; }
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
import config_manifest as CM
H = CM.canonical_hash(CM.load(wt)['vars'])
d = json.loads(m.read_text()); d['config_sha256'] = H; m.write_text(json.dumps(d, indent=1)+"\n")
import fv_provenance as F
md5 = lambda p: hashlib.md5(open(p,'rb').read()).hexdigest()
b = pathlib.Path(wt+'/data/expected_boot.json'); e = json.loads(b.read_text())
e['config'] = H
e['fv'] = F.fv_identity(wt+'/engine/forward_valuation')
e['rl_model'] = md5(wt+'/engine/rl_after/rl_model.py')
e['engine_head'] = md5(wt+'/engine/rl_after/_merged_recover.py')
b.write_text(json.dumps(e, indent=1)+"\n")
print("  variant manifest:", " ".join("%s=%s"%(k,v) for k,v in kv) or "(HEAD defaults)")
print("  engine_head:", e['engine_head'][:8], " curve_artifact:", md5(wt+'/engine/rl_after/pvc_curve_v2.json')[:8])
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
mkdir -p "$(dirname "$OUT")"
cd "$WT/engine/rl_after"; rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
rc=$?
if [ -f rl_app_data.json ]; then cp rl_app_data.json "$OUT"; echo "  OK $(md5sum rl_app_data.json | cut -c1-32)  -> $(basename $OUT)"
else echo "  FAILED (exit $rc) -- see $OUT.log"; tail -12 "$OUT.log"; fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
