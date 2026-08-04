#!/usr/bin/env bash
# preboot_assert.sh — #290 Addendum C.6 / D condition 2.
#
# /home/claude/rl_workspace is a SINGLE SHARED MUTABLE WORKSPACE with no interlock, and
# guard_correction_canary.py rebuilds through it with a DELIBERATELY EDITED store. Two engine
# acts that overlap produce results that look clean and are void (it happened, 2026-07-31).
# Run this before seeding the workspace or starting any engine act.
#
# Exit 0 = clear to proceed. Exit 1 = an engine process is live; HALT.
#
# Why a script file and not an inline pgrep: `pgrep -f` matches against full command lines, so
# an inline pattern matches the very shell that is running it — the assert then fires with zero
# engine processes and is useless in the failing direction AND the passing one. Living in a file
# keeps the pattern out of the caller's command line; we additionally exclude our own pid, our
# parent, and any pgrep.
set -uo pipefail

ENGINE_PATTERN='(rl_export|s4_matrix_M1v7|one_source_selftest|guard_correction_canary|refit_v0surf|build_peak_model_v4|run_panel)'

self=$$
parent=$PPID

hits=""
while read -r pid cmd; do
    [ -z "${pid:-}" ] && continue
    [ "$pid" = "$self" ] && continue
    [ "$pid" = "$parent" ] && continue
    case "$cmd" in
        *preboot_assert*) continue ;;   # never match ourselves by name
        *pgrep*)          continue ;;
    esac
    hits="${hits}  pid ${pid}: ${cmd}
"
done < <(ps -eo pid=,args= | grep -E "$ENGINE_PATTERN" | grep -v -E 'grep -E')

if [ -n "$hits" ]; then
    echo "PREBOOT HALT: an engine process is live; /home/claude/rl_workspace is single-writer (N10)."
    printf '%s' "$hits"
    echo "  Wait for it to exit. Never run two engine acts against the shared workspace."
    exit 1
fi

echo "preboot assert PASS — no engine process live; clear to seed the workspace"
exit 0
