#!/bin/bash
# GUARD 5 — VERIFIED, NOT ASSERTED. Run the way the boot runs it (run_panel.sh / bootstrap.sh form),
# against THE BRANCH TREE, after the C3 six-pin re-key.
#
# THE BOOT FORM, taken verbatim from run_panel.sh:17 and bootstrap.sh:85 --
#     RL_REPO=<root> RL_FV=<root>/engine/forward_valuation \
#       python3 <root>/boot_guard.py <label> <store> <_merged_recover.py> <cm_400.pkl> <LTI_REGISTER.md>
# assert_boot runs EVERY leg on entry: (0) store checkout · (0r) register · (0b) config · (0c) board
# checkout · (0f) rl_model checkout · (0d) fitted-artifact checkout (q97m/v0surf/peak_model/
# pvc_snapshot/bust_prior) · (0e) fitted-artifact LOADED-PATH (q97m/v0surf/band) · the four _chk
# read-path assertions · (0g) forward-valuation provenance BOTH HALVES (checkout + loaded-path).
#
# WHY THE PATHS ARE RE-POINTED AT THE BRANCH TREE, and on whose word.
#   run_panel.sh hardcodes WS=/home/claude/rl_workspace/rl_after -- a SHARED, out-of-repo workspace
#   that this branch does not own and that bootstrap.sh (not this seat) is what re-seeds. Register
#   v770 already ruled on exactly this: "the runbook's Guard 5 recipe points at /home/claude/
#   rl_workspace ... producing an alarming-looking but artefactual store complaint -- re-point it at
#   the [candidate] tree; real complaints remain pure pin staleness = C3." RUN A below is that
#   re-pointing. RUN C below is the LITERAL run_panel.sh against the shared workspace, reported
#   unedited so the artefact is on the record rather than hidden.
#
# ARG1: bound | unbound | literal
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$HERE/../../.." && pwd)"
export PATH="/root/rl_venv312/bin:$PATH"
MODE="${1:-bound}"

echo "=============================================================================="
echo "GUARD 5  —  mode: $MODE"
echo "  branch tree : $ROOT"
echo "  HEAD        : $(git -C "$ROOT" rev-parse --short=7 HEAD)"
echo "=============================================================================="

case "$MODE" in
  bound)
    # THE BOOT FORM, every path re-pointed at the branch tree, RL_V0SURF_PKL bound explicitly.
    export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
    echo "  RL_V0SURF_PKL = $RL_V0SURF_PKL"
    RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" python3 "$ROOT/boot_guard.py" \
      run_panel_branchtree \
      "$ROOT/engine/rl_after/rl_model_data.json" \
      "$ROOT/engine/rl_after/_merged_recover.py" \
      "$ROOT/data/cm_400.pkl" \
      "$ROOT/LTI_REGISTER.md"
    ;;
  unbound)
    # IDENTICAL to `bound` except RL_V0SURF_PKL is NOT set. This is the footgun probe: the engine's
    # own precedence is $RL_V0SURF_PKL -> /home/claude/v0surf.pkl -> <repo>/data/v0surf.pkl, so with
    # the binding absent the out-of-repo copy WINS over the branch's own frozen surface.
    unset RL_V0SURF_PKL
    echo "  RL_V0SURF_PKL = <unset>"
    echo "  /home/claude/v0surf.pkl = $( [ -f /home/claude/v0surf.pkl ] && md5sum /home/claude/v0surf.pkl | cut -d' ' -f1 || echo ABSENT )"
    echo "  <repo>/data/v0surf.pkl  = $(md5sum "$ROOT/data/v0surf.pkl" | cut -d' ' -f1)"
    RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" python3 "$ROOT/boot_guard.py" \
      run_panel_branchtree_unbound \
      "$ROOT/engine/rl_after/rl_model_data.json" \
      "$ROOT/engine/rl_after/_merged_recover.py" \
      "$ROOT/data/cm_400.pkl" \
      "$ROOT/LTI_REGISTER.md"
    ;;
  literal)
    # run_panel.sh's own line, byte-for-byte, against the SHARED out-of-repo workspace.
    WS=/home/claude/rl_workspace/rl_after
    echo "  workspace   : $WS   (shared, out-of-repo, NOT owned by this branch)"
    echo "  ws _merged_recover.py : $(md5sum $WS/_merged_recover.py | cut -d' ' -f1)"
    echo "  branch _merged_recover.py : $(md5sum "$ROOT/engine/rl_after/_merged_recover.py" | cut -d' ' -f1)"
    export RL_V0SURF_PKL="$ROOT/data/v0surf.pkl"
    RL_REPO="$ROOT" RL_FV="$ROOT/engine/forward_valuation" python3 "$ROOT/boot_guard.py" \
      run_panel "$WS/rl_model_data.json" "$WS/_merged_recover.py" \
      "$ROOT/data/cm_400.pkl" "$WS/LTI_REGISTER.md"
    ;;
  *) echo "usage: guard5.sh bound|unbound|literal"; exit 2 ;;
esac
RC=$?
echo
echo "GUARD 5 [$MODE] EXIT=$RC  ->  $( [ $RC -eq 0 ] && echo PASS || echo FAIL )"
exit $RC
