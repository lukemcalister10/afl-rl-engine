#!/bin/bash
# ORDER 20C — THE NO-CAP LANE'S BOARD BUILDER.
#
# A DECLARED DERIVATIVE of build_board_o20b.sh (carried here byte-identical alongside). The two arms of
# this order that can run in gate mode DO run in gate mode, through that script untouched. This sibling
# exists for the one arm that cannot, and the diff is exactly four things:
#
#   1. RL_CONFIG_MODE is NOT set (dev shell instead of gate). Forced: config_manifest's reject scan
#      halts on ANY RL_/PAR_ var that is not a manifest var at its canonical value, and the no-cap lane
#      needs RL_V0SURF_PKL, which is not a manifest var and must not become one in a measurement.
#   2. The cap is moved through the ENV DIAL `RL_RUC_PRIOR_CAP` (_merged_recover.py:1157) — which is the
#      dial the owner's question is about — rather than through the manifest.
#   3. RL_V0SURF_PKL points at the merged pickle from v0surf_merge.py: the SHIPPED surfaces, re-keyed so
#      the cap-99 signature resolves. Needed because /home/claude/v0surf.pkl outranks <repo>/data in
#      _load_v0surf's precedence, so writing into the copied tree would be ignored.
#   4. expected_boot.json's `v0surf` pin is restamped to that pickle's md5, because boot_guard checks the
#      pin against the RESOLVED load path (boot_guard.py:263-273). Declared, not silent.
#
# THE LANE IS NOT ASSUMED INERT — IT IS MEASURED. `run_board.sh FIX_dev` runs this same script at the
# SHIPPED cap 1.4 with the same merged pickle; it must reproduce 1dbd1480a34c7823f330273211cbb76a, the
# gate-mode FIX board, byte-for-byte. Only then does the cap-99 board mean anything.
#
# Usage: RC_CAP=<value> [RC_NOFIX=1] build_board_rc.sh <outfile>
set -uo pipefail
OUT="$1"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC="$(cd "$HERE/../../../.." && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
WT=$SP/rc_tree_$(basename "$OUT" .json)
MERGED=$SP/v0surf_merged.pkl
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset RL_CONFIG_MODE

mkdir -p "$(dirname "$OUT")"
rm -rf "$WT"; mkdir -p "$WT"
tar -C "$SRC" --exclude=.git --exclude=docs/evidence -cf - . 2>/dev/null | tar -C "$WT" -xf -

if [ "${RC_NOFIX:-0}" != "1" ]; then
  python3 "$HERE/mut_fix.py" "$WT" || { echo "MUTATOR FAILED"; exit 1; }
else
  echo "  MUT fix: SKIPPED (RC_NOFIX=1 — HEAD engine)"
fi

python3 - "$WT" "$MERGED" <<'PY'
import json, sys, pathlib, hashlib
wt, merged = sys.argv[1], sys.argv[2]
sys.path.insert(0, wt)
import config_manifest as CM, fv_provenance as F
md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
H = CM.canonical_hash(CM.load(wt)['vars'])
b = pathlib.Path(wt + '/data/expected_boot.json'); e = json.loads(b.read_text())
e['config'] = H
e['fv'] = F.fv_identity(wt + '/engine/forward_valuation')
e['rl_model'] = md5(wt + '/engine/rl_after/rl_model.py')
e['engine_head'] = md5(wt + '/engine/rl_after/_merged_recover.py')
old = e.get('v0surf'); e['v0surf'] = md5(merged)
b.write_text(json.dumps(e, indent=1) + "\n")
print("  engine_head:", e['engine_head'][:8], " rl_model:", e['rl_model'][:8])
print("  v0surf pin :", str(old)[:8], "->", e['v0surf'][:8], "(the merged pickle)")
PY

export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export RL_V0SURF_PKL="$MERGED"
export RL_RUC_PRIOR_CAP="${RC_CAP:?RC_CAP must be set}"
echo "  DIAL: RL_RUC_PRIOR_CAP=$RL_RUC_PRIOR_CAP   v0surf: $RL_V0SURF_PKL"
cd "$WT/engine/rl_after"; rm -f rl_app_data.json rl_app_data.json.srcmd5
python3 rl_export.py > "$OUT.log" 2>&1
rc=$?
if [ -f rl_app_data.json ]; then
  cp rl_app_data.json "$OUT"
  echo "  OK $(md5sum rl_app_data.json | cut -c1-32)  -> $(basename $OUT)"
else
  echo "  FAILED (exit $rc) — see $OUT.log"; tail -12 "$OUT.log"; exit 1
fi
rm -rf "$WT"
