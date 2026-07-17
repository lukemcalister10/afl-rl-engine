#!/usr/bin/env bash
# first_commands.sh BRANCH_REF EXPECTED_SHA NEW_BRANCH [EXPECTED_STORE_MD5] [REQUIRED_SYMBOL[:FILE]]
# SEAT TOOLS (P3) · THE BASE GUARD — mechanizes a directive's EXECUTE-FIRST base block so the
# wrong-base failure (register items 264 · 270 · 298 · 299) fails LOUDLY instead of silently.
#
# It stands a build on the PINNED base by hand-proof, in order, EACH check printing an explicit
# PASS/FAIL verdict beside the raw SHAs/md5s that produced it (house law #2 — never a bare verdict):
#   0) refuse to run on a dirty working tree (a base guard must not run over uncommitted work)
#   1) ls-remote(BRANCH_REF) == EXPECTED_SHA        (the pin is live on the canonical remote)
#   2) fetch EXPECTED_SHA from the canonical URL     (bring the pinned object local)
#   3) checkout -B NEW_BRANCH EXPECTED_SHA           (branch FROM the pin, not "content moved to match")
#   4) merge-base --is-ancestor EXPECTED_SHA HEAD    (proof the checkout sits ON the pin)
#   5) [optional] store md5 == EXPECTED_STORE_MD5    (the pinned store travels with the tree, item 264)
#   6) [optional] git grep -c REQUIRED_SYMBOL >= 1   (a base-only tree lacks the candidate's symbol, item 298)
# On full success it writes the whole transcript to FIRST_COMMANDS_PROOF.txt in the CWD (the item-298
# SEAM NOTE: the ancestor proof must be the branch's FIRST COMMITTED ARTIFACT) and prints the one
# line the build must commit it with. prescreen.sh then verifies that committed proof.
#
# SILENCE IS A RED (house law #3): a check that cannot prove its claim routes through die() and exits
# non-zero — no green FIRST_COMMANDS_PROOF.txt is ever written on a failed base. set -euo pipefail;
# the exit code propagates. POSIX bash + coreutils only. Network: the canonical URL only (house law #4).
set -euo pipefail

URL="https://github.com/lukemcalister10/afl-rl-engine.git"
HERE="$(cd "$(dirname "$0")" && cd ../.. && pwd)"   # repo root (tools/seat -> ../..)
STORE_REL="engine/rl_after/rl_model_data.json"      # the Guard-5 canonical store (id_resolver _STORE_DEFAULT)
PROOF="FIRST_COMMANDS_PROOF.txt"                     # written to the CWD, committed as the branch's first artifact

TRANSCRIPT=""
say() { echo "$*"; TRANSCRIPT="${TRANSCRIPT}$*"$'\n'; }   # print live AND accumulate for the proof file
die() { echo "first_commands: FAIL — $*" >&2; exit 1; }

usage() {
  die "usage: first_commands.sh BRANCH_REF EXPECTED_SHA NEW_BRANCH [EXPECTED_STORE_MD5] [REQUIRED_SYMBOL[:FILE]]"
}

[ $# -ge 3 ] && [ $# -le 5 ] || usage
BRANCH_REF="$1"; EXPECTED_SHA="$2"; NEW_BRANCH="$3"
EXPECTED_STORE_MD5="${4:-}"; REQUIRED_SYMBOL="${5:-}"

# EXPECTED_SHA must be a full 40-hex commit id — a short/typo'd pin is itself a red.
case "$EXPECTED_SHA" in
  *[!0-9a-fA-F]*|"") die "EXPECTED_SHA '$EXPECTED_SHA' is not hex" ;;
esac
[ "${#EXPECTED_SHA}" -eq 40 ] || die "EXPECTED_SHA must be a full 40-char SHA (got ${#EXPECTED_SHA} chars: '$EXPECTED_SHA')"

cd "$HERE" || die "cannot cd to repo root $HERE"

say "== first_commands · THE BASE GUARD =="
say "url          : $URL"
say "branch_ref   : $BRANCH_REF"
say "base_sha     : $EXPECTED_SHA"          # <- machine field: prescreen.sh reads THIS as the recorded base
say "new_branch   : $NEW_BRANCH"
say "store_md5    : ${EXPECTED_STORE_MD5:-'(not asserted)'}"
say "symbol       : ${REQUIRED_SYMBOL:-'(not asserted)'}"

# --- 0) dirty-tree refusal — uncommitted changes to TRACKED files (the destructive case: checkout -B
#     would carry or clobber them). Untracked scratch (a session_*/ proof dir, the $PROOF file itself)
#     survives checkout -B untouched, so it does NOT block — else the guard could never run beside its
#     own output. --untracked-files=no keeps the check to tracked staged/unstaged changes. ---
DIRTY="$(git status --porcelain --untracked-files=no 2>/dev/null | grep -v -- " $PROOF\$" || true)"
if [ -n "$DIRTY" ]; then
  echo "$DIRTY" >&2
  die "working tree is DIRTY — uncommitted changes to TRACKED files; commit/stash before running the base guard (checkout -B must not run over uncommitted work)"
fi
say "[0] dirty-tree : PASS  no uncommitted changes to tracked files (untracked scratch tolerated)"

# --- 1) ls-remote(BRANCH_REF) == EXPECTED_SHA (the pin is live on the canonical remote) ---
LS_SHA="$(git ls-remote "$URL" "$BRANCH_REF" 2>/dev/null | awk 'NR==1{print $1}')" \
  || die "ls-remote of '$BRANCH_REF' against canonical URL failed (network / URL)"
[ -n "$LS_SHA" ] || die "ls-remote returned no SHA for '$BRANCH_REF' (ref does not exist on the remote)"
if [ "$LS_SHA" = "$EXPECTED_SHA" ]; then
  say "[1] ls-remote  : PASS  $BRANCH_REF -> $LS_SHA == expected"
else
  die "[1] ls-remote MISMATCH — $BRANCH_REF is $LS_SHA on the remote, expected $EXPECTED_SHA (the pin moved or the wrong ref was named)"
fi

# --- 2) fetch the pinned object from the canonical URL ---
git fetch --quiet "$URL" "$EXPECTED_SHA" 2>/dev/null \
  || git fetch --quiet "$URL" "$BRANCH_REF" 2>/dev/null \
  || die "fetch of $EXPECTED_SHA from canonical URL failed"
git cat-file -e "${EXPECTED_SHA}^{commit}" 2>/dev/null \
  || die "$EXPECTED_SHA is not a commit object after fetch"
say "[2] fetch      : PASS  $EXPECTED_SHA present locally (git cat-file -e ok)"

# --- 3) checkout -B NEW_BRANCH EXPECTED_SHA (branch FROM the pin) ---
git checkout -B "$NEW_BRANCH" "$EXPECTED_SHA" >/dev/null 2>&1 \
  || die "checkout -B $NEW_BRANCH $EXPECTED_SHA failed"
HEAD_SHA="$(git rev-parse HEAD)" || die "rev-parse HEAD failed after checkout"
[ "$HEAD_SHA" = "$EXPECTED_SHA" ] || die "post-checkout HEAD $HEAD_SHA != pin $EXPECTED_SHA"
say "[3] checkout   : PASS  $NEW_BRANCH @ HEAD $HEAD_SHA (== pin; branched FROM it, not copied ONTO it)"

# --- 4) merge-base --is-ancestor proof (the checkout sits ON the pin) ---
if git merge-base --is-ancestor "$EXPECTED_SHA" HEAD 2>/dev/null; then
  say "[4] ancestor   : PASS  $EXPECTED_SHA is-ancestor HEAD $HEAD_SHA (the pinned base is in this branch's history)"
else
  die "[4] ancestor MISMATCH — $EXPECTED_SHA is NOT an ancestor of HEAD $HEAD_SHA"
fi

# --- 5) [optional] store md5 assert (the pinned store travels with the tree — item 264) ---
if [ -n "$EXPECTED_STORE_MD5" ]; then
  [ -f "$STORE_REL" ] || die "[5] store MISSING — $STORE_REL absent at HEAD (cannot assert store md5)"
  STORE_MD5="$(md5sum "$STORE_REL" | cut -d' ' -f1)" || die "md5sum of $STORE_REL failed"
  # accept a short (prefix) or full expected md5 — compare on the shorter length
  n="${#EXPECTED_STORE_MD5}"
  if [ "${STORE_MD5:0:$n}" = "$EXPECTED_STORE_MD5" ]; then
    say "[5] store md5  : PASS  $STORE_REL = ${STORE_MD5:0:$n} == expected $EXPECTED_STORE_MD5"
  else
    die "[5] store md5 MISMATCH — $STORE_REL = $STORE_MD5, expected ${EXPECTED_STORE_MD5} (wrong store under the tree — item 264/298)"
  fi
else
  say "[5] store md5  : SKIP  (no EXPECTED_STORE_MD5 argument given)"
fi

# --- 6) [optional] required-symbol grep-count >= 1 (a base-only tree lacks the candidate's symbol — item 298) ---
if [ -n "$REQUIRED_SYMBOL" ]; then
  SYM="${REQUIRED_SYMBOL%%:*}"                                   # SYMBOL  (before the optional :FILE)
  SFILE=""; case "$REQUIRED_SYMBOL" in *:*) SFILE="${REQUIRED_SYMBOL#*:}";; esac
  [ -n "$SYM" ] || die "[6] symbol argument '$REQUIRED_SYMBOL' has an empty SYMBOL part"
  # NOTE: git grep exits 1 when there are NO matches — the very case [6] must catch. Under
  # `set -e -o pipefail` an unguarded `CNT=$(git grep ...)` would kill the script at the assignment
  # with NO [6] verdict printed (a SILENCE-IS-A-RED hole). The trailing `|| true` lets the zero count
  # flow to the explicit die() below, so the miss fails LOUDLY, not silently.
  if [ -n "$SFILE" ]; then
    [ -f "$SFILE" ] || die "[6] symbol FILE '$SFILE' absent at HEAD (cannot grep the required symbol)"
    CNT="$(git grep -c -F -e "$SYM" -- "$SFILE" 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')" || true
    SCOPE="$SFILE"
  else
    CNT="$(git grep -c -F -e "$SYM" 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')" || true
    SCOPE="(whole tree)"
  fi
  [ -n "${CNT:-}" ] || CNT=0
  if [ "${CNT:-0}" -ge 1 ]; then
    say "[6] symbol     : PASS  '$SYM' found $CNT time(s) in $SCOPE (>=1 — the candidate's code is present)"
  else
    die "[6] symbol MISSING — '$SYM' found 0 times in $SCOPE (base-only tree? the candidate's code is not here — item 298)"
  fi
else
  say "[6] symbol     : SKIP  (no REQUIRED_SYMBOL argument given)"
fi

say "== first_commands PASS — base proven; this transcript IS the branch's first committed artifact =="

# --- write the transcript to FIRST_COMMANDS_PROOF.txt (only on full success) ---
printf '%s' "$TRANSCRIPT" > "$PROOF" || die "could not write $PROOF to $(pwd)"
echo
echo "wrote $(pwd)/$PROOF — commit it as the branch's FIRST commit with:"
echo "  git add $PROOF && git commit -m 'base: FIRST_COMMANDS_PROOF ($EXPECTED_SHA on $NEW_BRANCH)'"
