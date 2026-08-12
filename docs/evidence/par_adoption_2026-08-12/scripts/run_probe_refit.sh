#!/bin/bash
# ORDER 20B — the SAME probe, but with the D14 V0 pick surface REFIT instead of read from its freeze.
#
# WHY THIS RUN EXISTS. On the board path `v0_start` returns `_V0CURVE[...]`, the D14 surface, and that
# surface is FROZEN (`_V0CURVE_META['_v0surf_frozen'] == True` on both trees). A frozen artifact is a
# function of (pos, draft-age, pick) alone, so it cannot move when the par surface moves — which means
# the D14a/D14b gates and the national `v0_start` column are UNCHANGED BY CONSTRUCTION under the fix,
# not unchanged as a finding. Reporting that green as if it were evidence would be misleading.
#
# `_build_v0_curve` honours RL_V0SURF_REFIT=1 by re-fitting the surface from the live roster's `_v0_raw`
# (_merged_recover.py:1735). This run therefore measures what the gates and the national v0 column would
# do IF the fix were adopted AND the V0 surface were re-baked on top of it — the state the owner would
# actually be in after an adoption, rather than the state a stale freeze is currently hiding.
#
# NOTE ON THE LOAD: like ORDER 20's population_probe.py this is a dev-shell engine load (no
# RL_CONFIG_MODE), so config-manifest enforcement is a no-op. It reads the engine; it builds no board.
#
# Usage: bash run_probe_refit.sh <HEAD|FIX> <out.json>
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SP=/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad
T="$1"; OUTF="$2"; WT=$SP/tree_$T
export PATH=/root/rl_venv312/bin:$PATH
export PYTHONHASHSEED=0
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
export RL_V0SURF_REFIT=1
# The live V0 lens fits from the #279 structural basis, a DECLARED INPUT (_merged_recover.py:1460-1469;
# there is deliberately no fallback). stage_trees.sh excludes docs/evidence from the tree copies, so the
# artifact is supplied from the CHECKOUT, read-only, by its canonical path. Its md5 is recorded in the
# refit's own output via _V0CURVE_META['_lens_basis'].
export RL_LENS_BASIS="$(cd "$HERE/../../../.." && pwd)/docs/evidence/exec_306_zlaarm/basis/structural_basis_279.json"
export RL_REPO="$WT" RL_FV="$WT/engine/forward_valuation"
export PYTHONPATH="$WT/engine/rl_after:$WT:$WT/vendor"
export OUT="$OUTF"
S=$(date +%s); python3 "$HERE/engine_probe.py"; rc=$?; E=$(date +%s)
echo "  refit-probe($T) exit=$rc  $(( (E-S)/60 ))m $(( (E-S)%60 ))s -> $OUTF"
exit $rc
