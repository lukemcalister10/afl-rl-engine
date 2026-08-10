#!/bin/bash
# PER-ITEM ATTRIBUTION BY KILL-SWITCH — the repo's own G-ATTR-separable method.
#
# Building each item's board by checking out its commit does not work: an intermediate commit's
# expected_boot.json still carries the identities of the tree BEFORE the later ports, and Guard 5
# correctly refuses to boot on a forward_valuation tree whose identity is not the pinned one.
# So every variant is built from HEAD instead, with the item's declared kill-switch set — which is
# exactly how this repo already attributes levers (RL_ISOFADE, RL_PVC2, RL_LEGE: "declared
# kill-switch, G-ATTR-separable"). Each variant restamps its OWN worktree's manifest and boot pins
# so the guards stay armed rather than being bypassed.
#
# Usage: build_board_switch.sh <outfile> [VAR=VAL ...]
set -uo pipefail
OUT="$1"; shift
REPO=/home/user/afl-rl-engine
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_sw
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }

# put the requested manifest values in, then restamp config + boot identities for THIS tree
python3 - "$WT" "$@" <<'PY'
import json, sys, pathlib, hashlib
wt = sys.argv[1]; kv = [a.split('=',1) for a in sys.argv[2:]]
m = pathlib.Path(wt+'/data/model_config.json'); d = json.loads(m.read_text())
for k,v in kv:
    if k in d['vars']: d['vars'][k] = v
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
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
# the non-manifest declared kill-switches ride the environment
for a in "$@"; do case "$a" in RL_ITEM_A=*|RL_ITEM_H=*|RL_C_H=*|RL_RUC_WAGE=*) export "$a";; esac; done
cd "$WT/engine/rl_after"; rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
rc=$?
if [ -f rl_app_data.json ]; then cp rl_app_data.json "$OUT"; echo "  OK $(md5sum rl_app_data.json | cut -c1-32)  -> $(basename $OUT)"
else echo "  FAILED (exit $rc) — see $OUT.log"; tail -4 "$OUT.log"; fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
