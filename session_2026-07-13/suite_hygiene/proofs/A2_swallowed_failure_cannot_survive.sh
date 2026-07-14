#!/usr/bin/env bash
# =============================================================================
# ACCEPTANCE A2 — a SWALLOWED FAILURE CANNOT SURVIVE.
# For the three worst LIVE-HARNESS propagation sites, induce a failure and show
# the exit code is NON-ZERO now, where the pre-hardening script returned 0.
# (D3's literal enumeration was not in main — PR #71 was report-only — so these
# are the three worst in-fence sites found by direct sweep.)
#
# For each site: BEFORE = the script as it stood PRE-HARDENING (commit c3b0337^,
# the merge of PR #70); AFTER = the committed hardened script. Same induced break,
# compare rc. (The hardening is committed, so HEAD is the *after* — see PRE below.)
# All breaks are applied to SCRATCH copies; no real file is modified.
# =============================================================================
set -uo pipefail
REPO=/home/user/afl-rl-engine
SCR="$REPO/session_2026-07-13/suite_hygiene/proofs"
LOG="$SCR/A2_run.log"
# BEFORE = the PRE-HARDENING tree. The hardening is now COMMITTED (commit c3b0337),
# so `HEAD` is the *after*; the pre-hardening baseline is that commit's parent
# (= 2bc5151, the merge of PR #70). Pinning to c3b0337^ keeps this correct even as
# the branch grows. (This is why a first resume-run showed BEFORE==AFTER on the two
# git-sourced sites — the baseline had drifted onto the hardened HEAD.)
PRE=$(git -C "$REPO" rev-parse c3b0337^)
: > "$LOG"
say(){ echo "$@" | tee -a "$LOG"; }

overall=0
verdict(){ # name  before_rc  after_rc
  if [ "$2" = "0" ] && [ "$3" != "0" ]; then say "  => $1: PASS  (BEFORE swallowed: rc=$2 ; AFTER propagates: rc=$3)";
  else say "  => $1: FAIL  (BEFORE rc=$2 AFTER rc=$3 — expected before=0, after!=0)"; overall=1; fi
}

# ---------------------------------------------------------------------------
# SITE 1 — run_panel.sh : the panel gate computes a FAIL (a player mismatches).
#   This is the TRUE swallow: the panel prints "RESULT: FAIL" but the pre-hardening
#   heredoc has NO sys.exit, so python exits 0 and the FAIL verdict is thrown away.
#   (An unhandled *raise* was never swallowed — python's non-zero exit is the last
#   command's status regardless; 2>/dev/null only hid the traceback TEXT.)
#   BEFORE: prints RESULT: FAIL, exits 0 (swallowed).
#   AFTER : `sys.exit(0 if ok else 1)` -> exits 1 on the same computed FAIL.
# Induce by corrupting ONE panel expected value in a scratch copy (7667 -> 9999).
# ---------------------------------------------------------------------------
say "### SITE 1: run_panel.sh (panel computes a FAIL) ###"
mk_panel(){ # $1 = source file, $2 = dest ; force a mismatch on the first panel row,
            # and pin HERE to the real repo so boot_guard/WS/data resolve (the scratch
            # copy lives in proofs/, so its own dirname would break line-8 boot_guard).
  sed -e "s|^HERE=\$(cd .*|HERE=$REPO|" \
      -e "s/('Nick Daicos',7667)/('Nick Daicos',9999)/" "$1" > "$2"; }
git show "$PRE:run_panel.sh" > "$SCR/_panel_before_src.sh"
mk_panel "$SCR/_panel_before_src.sh" "$SCR/_panel_before.sh"
mk_panel "$REPO/run_panel.sh"        "$SCR/_panel_after.sh"
bash "$SCR/_panel_before.sh" >>"$LOG" 2>&1; b1=$?
bash "$SCR/_panel_after.sh"  >>"$LOG" 2>&1; a1=$?
verdict "run_panel.sh" "$b1" "$a1"

# ---------------------------------------------------------------------------
# SITE 2 — bootstrap.sh : the `md5sum <seed> | cut` pipe on a MISSING seed file.
#   BEFORE: `set -e` (no pipefail) -> the pipe's status is cut's success -> 0/continues
#   AFTER : `set -euo pipefail`    -> the pipe fails on md5sum -> HALT
# Demonstrated on the exact pipe pattern from bootstrap.sh:38-40 under each regime.
# ---------------------------------------------------------------------------
say "### SITE 2: bootstrap.sh md5-pipe on a missing seed (lines 38-40 pattern) ###"
cat > "$SCR/_boot_before.sh" <<'EOF'
set -e                                   # bootstrap.sh header BEFORE
M=$(md5sum /home/claude/__NO_SUCH_STORE__ | cut -c1-8)
echo "REACHED-PAST-PIPE M=[$M]"
EOF
cat > "$SCR/_boot_after.sh" <<'EOF'
set -euo pipefail                        # bootstrap.sh header AFTER
M=$(md5sum /home/claude/__NO_SUCH_STORE__ | cut -c1-8)
echo "REACHED-PAST-PIPE M=[$M]"
EOF
bash "$SCR/_boot_before.sh" >>"$LOG" 2>&1; b2=$?
bash "$SCR/_boot_after.sh"  >>"$LOG" 2>&1; a2=$?
verdict "bootstrap.sh md5-pipe" "$b2" "$a2"

# ---------------------------------------------------------------------------
# SITE 3 — verify_restore.sh : a failing chk() (restore-verify FAIL).
#   BEFORE: prints RESTORE-VERIFY FAIL but always `exit 0`  (the disease)
#   AFTER : authoritative `exit $((fail>0?1:0))` -> exit 1 on any FAIL
# Run both against the live tree (it already has 2 real FAILs), compare rc.
# ---------------------------------------------------------------------------
say "### SITE 3: verify_restore.sh (a chk FAILs) ###"
git show "$PRE:verify_restore.sh" > "$SCR/_vr_before.sh"
( cd "$REPO" && bash "$SCR/_vr_before.sh" "$REPO" >>"$LOG" 2>&1 ); b3=$?
( cd "$REPO" && bash "$REPO/verify_restore.sh" "$REPO" >>"$LOG" 2>&1 ); a3=$?
verdict "verify_restore.sh" "$b3" "$a3"

say "----------------------------------------------------"
[ "$overall" = 0 ] && say "A2 RESULT: PASS  (all three sites: swallowed before, propagate now)" || say "A2 RESULT: FAIL"
exit "$overall"
