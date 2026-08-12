#!/bin/bash
# ORDER 24 -- BUILD A VARIANT BOARD ON THE POOL-DIAL STAGE. Sibling of
# docs/evidence/pool_landing_2026-08-12/build_board_o23.sh, CARRIED except that the surface is staged
# by REPLACING the landed literals (o24_stage_surface.py) rather than injecting a block, and there is
# no levels stage at all: ORDER 24 is the CHEAP PATH and the signed levels in pvc_curve_v2.json are
# FROZEN, read from the file, never written.
#
# THE CHECKOUT'S board, engine, curve artifact and self-test ARE NEVER WRITTEN.
#
# Usage: build_board_o24.sh <outfile> <surface.json|nosurface> [git-ref, default HEAD]
#   the third argument builds the CONTROL: `... nosurface f041d93` checks out the pre-registration
#   commit, whose engine is the UNMODIFIED land/pool-update engine, and must reproduce 665311ca.
set -uo pipefail
OUT="$1"; SURF="$2"; REF="${3:-HEAD}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o24_$(basename "$OUT" .json)
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" "$REF" >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: $REF -> $(git -C "$WT" rev-parse --short HEAD)"

if [ "$SURF" != "nosurface" ]; then
  python3 "$HERE/o24_stage_surface.py" "$WT" "$SURF" || { echo "SURFACE STAGE FAILED"; exit 1; }
fi

python3 - "$WT" <<'PY'
import json, sys, pathlib, hashlib
wt = sys.argv[1]
sys.path.insert(0, wt)
import config_manifest as CM, fv_provenance as F
m = pathlib.Path(wt+'/data/model_config.json'); d = json.loads(m.read_text())
H = CM.canonical_hash(CM.load(wt)['vars'])
d['config_sha256'] = H; m.write_text(json.dumps(d, indent=1)+"\n")
md5 = lambda p: hashlib.md5(open(p,'rb').read()).hexdigest()
b = pathlib.Path(wt+'/data/expected_boot.json'); e = json.loads(b.read_text())
e['config'] = H
e['fv'] = F.fv_identity(wt+'/engine/forward_valuation')
e['rl_model'] = md5(wt+'/engine/rl_after/rl_model.py')
e['engine_head'] = md5(wt+'/engine/rl_after/_merged_recover.py')
b.write_text(json.dumps(e, indent=1)+"\n")
print("  config:", H[:8], " rl_model:", e['rl_model'][:8], " engine_head:", e['engine_head'][:8],
      " curve_artifact:", md5(wt+'/engine/rl_after/pvc_curve_v2.json')[:8])
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
