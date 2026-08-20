#!/bin/bash
# THE BAKE — PROOF THAT THE FROZEN-SIGNATURE GUARD IS STILL LIVE (register v780, 2026-08-20).
#
# WHY THIS EXISTS. Two of this seat's edits could, if done carelessly, have WEAKENED a guard:
#   (1) '/home/claude/v0surf.pkl' was removed from the load precedence;
#   (2) RL_V0SURF_PKL was added to config_manifest.INFRA_ALLOW, so gate mode no longer rejects it.
# Together those make the var SETTABLE where it previously was not. This seat's own claim in
# PREREG_BAKE.md §2 is that ALLOWING THE VAR TO BE SET IS NOT ALLOWING IT TO BE WRONG — the engine's
# frozen-SIGNATURE check and Guard 5's loaded-path leg both still stop a surface that is not the
# pinned one. A claim like that is worthless unpriced, so it is priced here.
#
# THE PROBE: point RL_V0SURF_PKL at the OUT-OF-REPO /home/claude/v0surf.pkl (fbc5b393) — the very file
# the precedence fix removed — and try to build. It must HALT. If a board comes out, a guard was
# weakened by this seat's edits and that is a FIRED falsifier, reported in those words.
#
# THE OUT-OF-REPO FILE IS ONLY READ. It is not moved, modified, or deleted.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export RL_ROOT="$(cd "$HERE/../../.." && pwd)"
export RL_SCRATCH="${RL_SCRATCH:?}"
export PATH="/root/rl_venv312/bin:$PATH"

echo "=== FROZEN-SIGNATURE PROBE — RL_V0SURF_PKL pointed at the OUT-OF-REPO surface ==="
echo "  in-repo pinned   data/v0surf.pkl        : $(md5sum "$RL_ROOT/data/v0surf.pkl" | cut -c1-32)  (pin 5dd34ca8)"
echo "  out-of-repo      /home/claude/v0surf.pkl: $(md5sum /home/claude/v0surf.pkl | cut -c1-32)  (fbc5b393 — READ ONLY, not touched)"
echo "  RL_V0SURF_PKL is in INFRA_ALLOW now, so GATE MODE will NOT reject it. The question is whether"
echo "  the ENGINE still refuses the surface. It must."
echo

WS="$RL_SCRATCH/frozensig"
rm -rf "$WS"; mkdir -p "$WS"
cp -rf "$RL_ROOT/engine/rl_after" "$WS/rl_after"
cp -rf "$RL_ROOT/engine/forward_valuation" "$WS/forward_valuation"
cp -f "$RL_ROOT/config_manifest.py" "$RL_ROOT/fv_provenance.py" "$RL_ROOT/boot_guard.py" "$RL_ROOT/LTI_REGISTER.md" "$WS/rl_after/"
chmod -R u+w "$WS"; rm -f "$WS/rl_after/rl_app_data.json"
cd "$WS/rl_after"
export RL_REPO="$RL_ROOT" RL_FV="$WS/forward_valuation" PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
export PYTHONPATH="$WS/rl_after:$RL_ROOT/vendor:$RL_ROOT"
export RL_V0SURF_PKL=/home/claude/v0surf.pkl

python3 rl_export.py > "$WS/out.txt" 2> "$WS/err.txt"
RC=$?
echo "  export exit = $RC"
echo
echo "--- stderr tail ---"
tail -22 "$WS/err.txt"
echo
if [ -f "$WS/rl_after/rl_app_data.json" ]; then
  echo "  A BOARD WAS PRODUCED: $(md5sum "$WS/rl_after/rl_app_data.json" | cut -c1-32)"
  echo "  VERDICT: THE FROZEN-SIGNATURE GUARD DID NOT HALT — A GUARD WAS WEAKENED. FALSIFIER FIRED."
else
  echo "  NO BOARD — the build HALTED on the unpinned surface."
  echo "  VERDICT: THE FROZEN-SIGNATURE GUARD IS LIVE. Allowing the var to be SET did not allow it to be WRONG."
fi
echo
echo "  /home/claude/v0surf.pkl after the probe: $(md5sum /home/claude/v0surf.pkl | cut -c1-32)  (unchanged — read only)"
