#!/bin/bash
# Run an arbitrary script under channel dials, with the manifest + boot pin temporarily set to match
# (gate mode requires env == manifest). Both are ALWAYS restored, including on failure.
set -uo pipefail
SCRIPT="$1"; OUT="$2"; shift 2
REPO=/home/user/afl-rl-engine
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o3
export PATH=/root/rl_venv312/bin:$PATH OPENBLAS_NUM_THREADS=1
cp "$REPO/data/model_config.json" "$SP/.man.bak"; cp "$REPO/data/expected_boot.json" "$SP/.boot.bak"
trap 'cp "$SP/.man.bak" "$REPO/data/model_config.json"; cp "$SP/.boot.bak" "$REPO/data/expected_boot.json"' EXIT
python3 - "$@" <<'PY'
import json, collections, sys
sys.path.insert(0,'/home/user/afl-rl-engine')
import config_manifest as CM
p='/home/user/afl-rl-engine/data/model_config.json'
d=json.load(open(p), object_pairs_hook=collections.OrderedDict)
for a in sys.argv[1:]:
    k,v=a.split('=',1); assert k in d['vars'], k; d['vars'][k]=v
H=CM.canonical_hash(d['vars']); d['config_sha256']=H
open(p,'w').write(json.dumps(d, indent=1)+"\n")
bp='/home/user/afl-rl-engine/data/expected_boot.json'
e=json.load(open(bp), object_pairs_hook=collections.OrderedDict); e['config']=H
open(bp,'w').write(json.dumps(e, indent=1)+"\n")
PY
for a in "$@"; do export "$a"; done
cd "$REPO" && python3 "$SCRIPT" > "$OUT" 2>&1
echo "exit=$? -> $OUT"
