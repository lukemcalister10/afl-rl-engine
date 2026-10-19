#!/bin/bash
# ORDER 19 — PER-ENTRANT COHORT-BOOK EMIT for the two pool-sitter-lift variants.
#
# A SIBLING of docs/evidence/composition_2026-08-10/emit_variant.sh, carried rather than modified
# (that file is FILED EVIDENCE of a landed act and is not touched here). The ONLY addition is the
# PATCH step: variant B has no env dial for the R leg, so it is produced by a one-line source patch
# applied to the SCRATCHPAD WORKTREE ONLY. The checkout's engine is never written.
#
# The patch is applied BEFORE the identity restamp, so the worktree's expected_boot.json carries the
# PATCHED engine_head md5 and every boot guard stays armed. The emitted matrix's meta.engine_head is
# therefore an independent, machine-readable proof that variant B differs by CODE from SHIP.
#
# Usage: emit_variant_o19.sh <label> <patch|nopatch> [VAR=VAL ...]
set -uo pipefail
LABEL="$1"; PATCH="$2"; shift 2
REPO=/home/user/afl-rl-engine
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o19_$LABEL
OUT=$SP/o19/emit_$LABEL
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT" "$OUT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }
echo "  ref: HEAD -> $(git -C "$WT" rev-parse --short HEAD)"
mkdir -p "$OUT"

# ---- THE VARIANT-B SOURCE PATCH, applied to the STAGED WORKTREE ONLY -------------------------------
if [ "$PATCH" = "patch" ]; then
python3 - "$WT" <<'PY'
import sys, pathlib
wt = sys.argv[1]
f = pathlib.Path(wt + '/engine/rl_after/_merged_recover.py')
src = f.read_text()
OLD = "    R=_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)     # D13 ASK3"
assert src.count(OLD) == 1, "anchor line not unique/found: %d" % src.count(OLD)
i = src.index(OLD); j = src.index("\n", i) + 1
NEW = ("    if p.get('_pool'): R=1.0                                 "
       "# ORDER 19 VARIANT B (MEASUREMENT ONLY, staged copy): the R leg lifted for POOL rows.\n"
       "    #                                                        "
       "ND rows are UNTOUCHED by construction -- the owner's ruling.\n")
f.write_text(src[:j] + NEW + src[j:])
print("  PATCHED sitout_ev: R := 1.0 for pool rows (staged worktree only)")
PY
[ $? -eq 0 ] || { echo "PATCH FAILED"; exit 1; }
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
print("  engine_head after patch+restamp:", e['engine_head'][:8])
PY

cp "$REPO/docs/evidence/noarb_338_2026-08-06/emit_matrix_338.py" "$OUT/emit.py"
# THE DIALS MUST BE EXPORTED: emit_matrix_338.py does not call config_manifest.enforce(), it execs the
# engine head directly and the dials read the ENVIRONMENT. Editing the manifest alone silently
# reproduces the baseline (the documented V2/V3 bug).
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
  echo "  NO MATRIX — see $OUT/emit.log"; tail -8 "$OUT/emit.log"
fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
