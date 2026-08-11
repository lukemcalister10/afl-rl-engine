#!/bin/bash
# ORDER 19 — BUILD A VARIANT BOARD. Sibling of docs/evidence/composition_2026-08-10/build_board_switch.sh
# (filed evidence, carried not modified). The ONE addition is the same variant-B source patch used by
# emit_variant_o19.sh, applied to the SCRATCHPAD WORKTREE ONLY and BEFORE the identity restamp, so the
# boot guards stay armed and the built board's engine identity records the patch.
#
# THE CHECKOUT'S data/rl_build/rl_app_data.json IS NEVER WRITTEN BY THIS SCRIPT.
#
# Usage: build_board_o19.sh <outfile> <patch|patchboth|nopatch> [VAR=VAL ...]
#   patch      = VARIANT B as the order defines it: the R leg lifted for pool rows inside sitout_ev.
#   patchboth  = the DISCLOSED SENSITIVITY only: sitout_ev AND _a_blend (:2178), the SECOND site that
#                reads the same retention surface, on the year-1+ arm. NOT variant B; reported apart.
set -uo pipefail
OUT="$1"; PATCH="$2"; shift 2
REPO=/home/user/afl-rl-engine
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/wt_o19b_$(basename "$OUT" .json)
export PATH=/root/rl_venv312/bin:$PATH
export RL_CONFIG_MODE=gate PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1

rm -rf "$WT"; git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
git -C "$REPO" worktree add --detach "$WT" HEAD >/dev/null 2>&1 || { echo "WORKTREE FAILED"; exit 1; }

if [ "$PATCH" = "patch" ] || [ "$PATCH" = "patchboth" ]; then
python3 - "$WT" "$PATCH" <<'PY'
import sys, pathlib
wt, mode = sys.argv[1], sys.argv[2]
f = pathlib.Path(wt + '/engine/rl_after/_merged_recover.py')
src = f.read_text()
NEW = ("    if p.get('_pool'): R=1.0                                 "
       "# ORDER 19 (MEASUREMENT ONLY, staged copy): the R leg lifted for POOL rows.\n"
       "    #                                                        "
       "ND rows are UNTOUCHED by construction -- the owner's ruling.\n")
SITES = ["    R=_R_surf(_sitout_cls(MA.gfut(p)), MA.effpk(p), tau)     # D13 ASK3"]
if mode == 'patchboth':
    SITES.append("    R=_R_surf(_sitout_cls(MA.gfut(p)),MA.effpk(p),tau)")
for OLD in reversed(SITES):                       # reversed: later site first, offsets stay valid
    assert src.count(OLD) == 1, "anchor line not unique/found (%r): %d" % (OLD[:40], src.count(OLD))
    i = src.index(OLD); j = src.index("\n", i) + 1
    src = src[:j] + NEW + src[j:]
f.write_text(src)
print("  PATCHED %d site(s): R := 1.0 for pool rows (staged worktree only)" % len(SITES))
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
print("  engine_head:", e['engine_head'][:8])
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
cd "$WT/engine/rl_after"; rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
rc=$?
if [ -f rl_app_data.json ]; then cp rl_app_data.json "$OUT"; echo "  OK $(md5sum rl_app_data.json | cut -c1-32)  -> $(basename $OUT)"
else echo "  FAILED (exit $rc) — see $OUT.log"; tail -6 "$OUT.log"; fi
git -C "$REPO" worktree remove --force "$WT" 2>/dev/null
