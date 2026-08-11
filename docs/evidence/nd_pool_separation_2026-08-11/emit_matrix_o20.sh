#!/bin/bash
# ORDER 20 — PER-ENTRANT MATRIX EMIT. Sibling of pool_sitter_lift_2026-08-11/emit_variant_o19.sh,
# with the same one deliberate difference as build_board_o20.sh: it COPIES the tree instead of
# running `git worktree add` against the primary checkout, which this order may not touch.
#
# Usage: emit_matrix_o20.sh <label> <pymutator|-> [VAR=VAL ...]
set -uo pipefail
LABEL="$1"; MUT="$2"; shift 2
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/o20_emit_$LABEL; OUT=$SP/o20/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT" "$OUT"; mkdir -p "$WT" "$OUT"
tar -C "$SRC" --exclude=.git --exclude=docs/evidence -cf - . 2>/dev/null | tar -C "$WT" -xf -
mkdir -p "$WT/docs/evidence/noarb_338_2026-08-06"
cp "$SRC/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUT/emit.py"

if [ "$MUT" != "-" ]; then python3 "$MUT" "$WT" || { echo "MUTATOR FAILED"; exit 1; } fi
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
import config_manifest as CM, fv_provenance as F
H = CM.canonical_hash(CM.load(wt)['vars'])
d = json.loads(m.read_text()); d['config_sha256'] = H; m.write_text(json.dumps(d, indent=1)+"\n")
md5 = lambda p: hashlib.md5(open(p,'rb').read()).hexdigest()
b = pathlib.Path(wt+'/data/expected_boot.json'); e = json.loads(b.read_text())
e['config']=H; e['fv']=F.fv_identity(wt+'/engine/forward_valuation')
e['rl_model']=md5(wt+'/engine/rl_after/rl_model.py'); e['engine_head']=md5(wt+'/engine/rl_after/_merged_recover.py')
b.write_text(json.dumps(e, indent=1)+"\n")
print("  engine_head:", e['engine_head'][:8], " rl_model:", e['rl_model'][:8])
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export RL_WORKDIR="$WT/engine/rl_after" RL_VENDOR="$WT/vendor" RL_OUT="$OUT"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
S=$(date +%s); python3 "$OUT/emit.py" > "$OUT/emit.log" 2>&1; rc=$?; E=$(date +%s)
echo "  emit exit=$rc  cost $(( (E-S)/60 ))m $(( (E-S)%60 ))s"
if [ -f "$OUT/per_entrant_338_confirmation.json" ]; then
  mv "$OUT/per_entrant_338_confirmation.json" "$SP/o20/per_entrant_$LABEL.json"
  echo "  OK -> per_entrant_$LABEL.json ($(md5sum "$SP/o20/per_entrant_$LABEL.json" | cut -c1-8))"
  grep -E "boundary crossers|band reading differs" "$OUT/emit.log" || true
else
  echo "  NO MATRIX — see $OUT/emit.log"; tail -10 "$OUT/emit.log"; exit 1
fi
rm -rf "$WT"
