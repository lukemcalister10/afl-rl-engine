#!/bin/bash
# ORDER 20 — BUILD A BOARD FROM A SCRATCHPAD COPY OF THIS WORKTREE.
#
# Sibling of docs/evidence/pool_sitter_lift_2026-08-11/build_board_o19.sh, with ONE deliberate
# difference: O19's script ran `git -C /home/user/afl-rl-engine worktree add`, which writes to the
# PRIMARY checkout's .git. This order is forbidden to touch the primary checkout at all, so this
# script COPIES the tree with `cp -a` instead. Nothing outside $SP is ever written.
#
# Usage: build_board_o20.sh <outfile> <pymutator|-> [VAR=VAL ...]
#   <pymutator>  a python file run as `python3 <pymutator> <TREEDIR>` after the copy and BEFORE the
#                identity restamp, so the boot guards stay armed and the built board's engine
#                identity records whatever the mutator did. `-` = no mutation (the BASE build).
set -uo pipefail
OUT="$1"; MUT="$2"; shift 2
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../.." && pwd)"                 # the worktree root
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/o20_tree_$(basename "$OUT" .json)
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

mkdir -p "$(dirname "$OUT")"
rm -rf "$WT"; mkdir -p "$WT"
# copy everything the build reads; exclude .git and the heavy evidence tree
tar -C "$SRC" --exclude=.git --exclude=docs/evidence -cf - . 2>/dev/null | tar -C "$WT" -xf -

if [ "$MUT" != "-" ]; then
  python3 "$MUT" "$WT" || { echo "MUTATOR FAILED"; exit 1; }
fi
# The mutator reads RL_O20_* from the environment; gate mode rejects ANY unknown RL_* override, so it
# must not survive into the build. Unset AFTER the mutator has run.
unset RL_O20_PERTURB RL_O20_FIX

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
print("  engine_head:", e['engine_head'][:8], " rl_model:", e['rl_model'][:8])
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
cd "$WT/engine/rl_after"; rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
rc=$?
if [ -f rl_app_data.json ]; then
  cp rl_app_data.json "$OUT"
  echo "  OK $(md5sum rl_app_data.json | cut -c1-32)  -> $(basename $OUT)"
else
  echo "  FAILED (exit $rc) — see $OUT.log"; tail -8 "$OUT.log"; exit 1
fi
rm -rf "$WT"
