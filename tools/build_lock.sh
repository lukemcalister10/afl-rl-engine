#!/usr/bin/env bash
# ==================================================================================================
# tools/build_lock.sh — THE BUILD LOCK. A real, flock-based, single-writer interlock.
# ==================================================================================================
#
#   source tools/build_lock.sh && build_lock_acquire <tag> [timeout_seconds]
#   tools/build_lock.sh run <tag> -- <command...>      # acquire, run, release
#   tools/build_lock.sh status                          # who holds it, since when
#
# WHY THIS EXISTS (AUDIT_CI.md gap G7, "no single-writer interlock in CI, though the tree owns one"):
#
#   /home/claude/rl_workspace is A SINGLE SHARED MUTABLE WORKSPACE. Both ci-guards.yml and
#   final-integration.yml run bootstrap.sh against it; guard_correction_canary.py rebuilds through it
#   with a DELIBERATELY EDITED store. Two engine acts that overlap produce results that look clean
#   and are void. That is not hypothetical — tools/preboot_assert.sh exists because IT HAPPENED, on
#   2026-07-31, and says so in its own header.
#
# WHY preboot_assert.sh WAS NOT ENOUGH, and this is an addition rather than a replacement:
#
#   preboot_assert.sh is a DETECTOR: it greps `ps` for a live engine process and refuses to start if
#   it finds one. Three limits the audit measured or that follow directly from its design —
#
#     1. IT IS CALLED BY NO WORKFLOW. "Both ci-guards.yml and final-integration.yml run bootstrap.sh
#        against the same shared /home/claude/rl_workspace; on a self-hosted runner they can race,
#        and the interlock the tree built for exactly that is not wired in."
#     2. IT MATCHES ON PROCESS NAME, NOT WORKSPACE PATH — "so an isolated engine run anywhere on the
#        box trips it." It fired twice during the audit itself, on runs that were not racing anyone.
#     3. IT IS A CHECK, NOT A LOCK. Two seats that check simultaneously both see a clear board and
#        both proceed. There is no atomic step anywhere in the sequence.
#
#   flock(2) has none of those properties. The kernel arbitrates, the grant is atomic, and the lock
#   is released when the LAST FD REFERRING TO IT CLOSES — which covers the holder being killed,
#   crashing, or its container being torn down. A lock that survives its holder's death is worse
#   than no lock, because the next seat's remedy is to delete it, and that is a habit which
#   eventually deletes a live one. There is nothing to delete here, ever.
#
#   ONE PRECISION, MEASURED RATHER THAN ASSUMED, because the obvious wording is wrong. "Released
#   when the holder dies" is NOT what flock does: the fd is inherited by children, so the lock is
#   held until the last process holding it exits. Measured on this box — SIGKILL the acquiring
#   script while its `sleep 45` child ran, and the lock stayed held for the remaining 45 seconds,
#   then released with no cleanup. That is the SAFE direction and it is what we want: an orphaned
#   child of a dead holder is still mutating the shared workspace, and releasing the lock the
#   instant its parent died would hand the workspace to a second writer while the first is still in
#   it — exactly the void-both-results failure the lock exists to prevent. `status` says so
#   explicitly when it sees a held lock whose recorded pid is gone, so nobody mistakes it for a
#   stale file to be removed.
#
# THE TWO ARE COMPLEMENTARY AND BOTH SHOULD RUN: this lock serialises the seats that cooperate;
# preboot_assert catches the process that never asked.
#
# --------------------------------------------------------------------------------------------------
# DESIGN NOTES, in the order someone debugging at 3am will want them:
#
#   * FAIL-CLOSED, LIKE EVERY OTHER GATE IN THIS TREE. If flock is missing, if the lock directory
#     cannot be created, if the fd cannot be opened — this HALTS. It never shrugs and proceeds. A
#     lock that silently degrades to no-lock is the worst outcome available: it is indistinguishable
#     from a working lock right up until it voids a build.
#
#   * THE HOLDER IS NAMED. The lock file records tag, pid, host, workspace and an ISO timestamp
#     BEFORE the work starts, so a waiter can print who it is waiting for rather than "resource
#     busy". The required message is exactly:
#
#         waiting for lock held by <tag> since <t>
#
#   * IT IS ADVISORY, AND DELIBERATELY SO. Nothing here can stop a process that does not take the
#     lock. The interlock is a protocol between cooperating callers, which is why the deliverable is
#     the helper PLUS its wiring into the entry points under version control.
#
#   * BUILD_LOCK=0 DISABLES IT, LOUDLY. Nested calls are the real reason (run_panel.sh invoked
#     from inside an already-locked bake would otherwise deadlock against itself), and a seat that
#     truly knows better should not have to comment out a line. Every skip prints why it skipped.
#     A reentrant grant is detected automatically via RL_BUILD_LOCK_HELD and never deadlocks.
#
#   * THE LOCK PATH FOLLOWS THE THING BEING PROTECTED, not the repo. The contended resource is the
#     shared workspace, and two checkouts building through the same workspace must contend. Default:
#     ${BUILD_LOCK_FILE:-/home/claude/.rl_build.lock}, overridable for tests.
#
#   * THIS TOOL'S OWN FLAGS ARE NOT `RL_*`, AND THAT IS THE FOURTH BURN OF THAT CLASS PAID FOR.
#     BUILD_LOCK / BUILD_LOCK_FILE / BUILD_LOCK_FD / BUILD_LOCK_TIMEOUT were RL_-prefixed until
#     2026-08-21. `config_manifest.enforce()` treats ANY ambient RL_/PAR_ variable that is not a
#     manifest var and not in INFRA_ALLOW as a divergent model override and HALTS the build — so a
#     seat isolating a sandbox with the old `RL_BUILD_LOCK_FILE` got, at the first armed advance,
#     `ConfigPolicyError: UNKNOWN inherited valuation flag RL_BUILD_LOCK_FILE` — a message about
#     valuation flags for what is a lock path. Measured on a real armed run: R24 dress rehearsal
#     2026-08-21 §3.3, RUN D. The legacy names are DETECTED AND HALTED below rather than silently
#     ignored: an isolation flag that stops being read is a sandbox quietly contending for the
#     shared lock, which is the very thing this file exists to prevent.
# ==================================================================================================

# THE LEGACY NAMES, REFUSED LOUDLY. Silently ignoring them would drop a caller's isolation or its
# deliberate skip on the floor; see the note above.
for _bl_legacy in RL_BUILD_LOCK RL_BUILD_LOCK_FILE RL_BUILD_LOCK_FD RL_BUILD_LOCK_TIMEOUT; do
    if [ -n "$(eval "printf '%s' \"\${${_bl_legacy}:-}\"")" ]; then
        echo "BUILD-LOCK HALT: ${_bl_legacy} is set. This tool's own flags are no longer RL_-prefixed" >&2
        echo "  (an RL_/PAR_ variable is a MODEL override to config_manifest.enforce() and halts any" >&2
        echo "  armed build that inherits it — R24 rehearsal §3.3). Use ${_bl_legacy#RL_} instead." >&2
        unset _bl_legacy
        return 1 2>/dev/null || exit 1
    fi
done
unset _bl_legacy

BUILD_LOCK_FILE="${BUILD_LOCK_FILE:-/home/claude/.rl_build.lock}"
BUILD_LOCK_FD="${BUILD_LOCK_FD:-9}"
BUILD_LOCK_TIMEOUT="${BUILD_LOCK_TIMEOUT:-3600}"

_bl_now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

_bl_halt() {
    echo "BUILD-LOCK HALT: $*" >&2
    echo "  The lock is fail-closed by design: a build that cannot prove it is the single writer" >&2
    echo "  does not start. (tools/build_lock.sh; AUDIT_CI.md gap G7.)" >&2
    return 1
}

# Read the holder record. Prints "<tag>|<pid>|<since>" or nothing.
_bl_holder() {
    [ -s "$BUILD_LOCK_FILE" ] || return 0
    awk -F'\t' 'NR==1{printf "%s|%s|%s", $1, $2, $3}' "$BUILD_LOCK_FILE" 2>/dev/null
}

# --------------------------------------------------------------------------------------------------
# build_lock_acquire <tag> [timeout_seconds]
#
# Blocks until the lock is held or the timeout expires. Returns 0 on success, 1 on halt.
# The lock is released automatically when the shell exits (the fd closes).
build_lock_acquire() {
    local tag="${1:-unnamed}" timeout="${2:-$BUILD_LOCK_TIMEOUT}"

    if [ "${BUILD_LOCK:-1}" = "0" ]; then
        echo "build-lock: SKIPPED by BUILD_LOCK=0 (tag=$tag). This build is NOT interlocked;" \
             "if another engine act is live against the shared workspace, both results are void."
        return 0
    fi

    # Reentrancy: a nested call inside an already-locked act must not deadlock against itself.
    if [ -n "${RL_BUILD_LOCK_HELD:-}" ]; then
        echo "build-lock: already held by this process tree as '$RL_BUILD_LOCK_HELD' (tag=$tag);" \
             "reentrant, not re-acquiring."
        return 0
    fi

    command -v flock >/dev/null 2>&1 || { _bl_halt "flock(1) not found; cannot interlock."; return 1; }

    local dir; dir=$(dirname "$BUILD_LOCK_FILE")
    mkdir -p "$dir" 2>/dev/null || { _bl_halt "cannot create lock dir $dir"; return 1; }

    eval "exec ${BUILD_LOCK_FD}>>\"\$BUILD_LOCK_FILE\"" \
        || { _bl_halt "cannot open $BUILD_LOCK_FILE on fd $BUILD_LOCK_FD"; return 1; }

    # Try once without blocking, so the common (uncontended) case prints nothing but the grant.
    if ! flock -n "$BUILD_LOCK_FD"; then
        local h tag_h since_h
        h=$(_bl_holder)
        tag_h=$(printf '%s' "$h" | cut -d'|' -f1)
        since_h=$(printf '%s' "$h" | cut -d'|' -f3)
        # THE REQUIRED LINE. Named holder, named time — never "resource temporarily unavailable".
        echo "waiting for lock held by ${tag_h:-<unknown>} since ${since_h:-<unknown>}"
        echo "  (lock $BUILD_LOCK_FILE; waiting up to ${timeout}s; this build will not start" \
             "until that act finishes — two engine acts through one workspace void both.)"
        if ! flock -w "$timeout" "$BUILD_LOCK_FD"; then
            h=$(_bl_holder)
            _bl_halt "timed out after ${timeout}s waiting for lock held by $(printf '%s' "$h" | cut -d'|' -f1) since $(printf '%s' "$h" | cut -d'|' -f3)"
            return 1
        fi
    fi

    # Held. Record who we are BEFORE any work starts, so a waiter always has someone to name.
    printf '%s\t%s\t%s\t%s\t%s\n' \
        "$tag" "$$" "$(_bl_now)" "$(hostname 2>/dev/null || echo '?')" "${PWD}" \
        > "$BUILD_LOCK_FILE"
    export RL_BUILD_LOCK_HELD="$tag"
    echo "build-lock: HELD by $tag (pid $$) since $(_bl_now) — single writer for the shared workspace."
    return 0
}

# Explicit release. Rarely needed: the fd closes on exit, which is the point of using flock.
build_lock_release() {
    [ -n "${RL_BUILD_LOCK_HELD:-}" ] || return 0
    eval "exec ${BUILD_LOCK_FD}>&-" 2>/dev/null || true
    echo "build-lock: released by $RL_BUILD_LOCK_HELD"
    unset RL_BUILD_LOCK_HELD
}

build_lock_status() {
    if [ ! -s "$BUILD_LOCK_FILE" ]; then
        echo "build-lock: no holder record at $BUILD_LOCK_FILE"
        return 0
    fi
    # A held lock cannot be flock'd non-blocking by us; that is the actual test, not the file's
    # existence. A stale record with no live holder must read as FREE, or seats learn to delete it.
    if command -v flock >/dev/null 2>&1 && \
       ( eval "exec ${BUILD_LOCK_FD}>>\"\$BUILD_LOCK_FILE\"" && flock -n "$BUILD_LOCK_FD" ) 2>/dev/null; then
        echo "build-lock: FREE (last holder record: $(_bl_holder | tr '|' ' '))"
    else
        echo "build-lock: HELD by $(_bl_holder | tr '|' ' ')"
        # The lock is genuinely held, but by a descendant of the recorded pid rather than by it.
        # Say so, or the next seat reads "held by pid 17477" + "17477 does not exist" and concludes
        # the lock file is stale garbage. It is not. Deleting it would release a live interlock.
        local pid; pid=$(_bl_holder | cut -d'|' -f2)
        if [ -n "$pid" ] && ! kill -0 "$pid" 2>/dev/null; then
            echo "  NOTE: recorded pid $pid is gone, but the lock is STILL HELD — an inherited fd," \
                 "i.e. a child of the dead holder is still running against the workspace."
            echo "  This is correct and the lock will free itself when that child exits." \
                 "DO NOT DELETE THE LOCK FILE; there is never a reason to."
        fi
    fi
}

# --------------------------------------------------------------------------------------------------
if [ "${BASH_SOURCE[0]}" = "${0}" ]; then
    case "${1:-status}" in
        status) build_lock_status ;;
        run)
            shift
            tag="${1:-unnamed}"; shift
            [ "${1:-}" = "--" ] && shift
            build_lock_acquire "$tag" || exit 1
            "$@"
            rc=$?
            build_lock_release
            exit $rc
            ;;
        *) echo "usage: $0 [status | run <tag> -- <command...>]" >&2; exit 2 ;;
    esac
fi
