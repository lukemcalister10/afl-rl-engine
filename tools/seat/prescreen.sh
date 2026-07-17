#!/usr/bin/env bash
# prescreen.sh <branch> <base_sha> — SEAT TOOLS (P3) · Tier-3 READ-ONLY candidate prescreen.
# Reads a candidate branch straight off the canonical remote and lays its fence-relevant facts
# beside the base, each on its own evidence-bearing line. WRITES NOTHING to the working tree /
# store / board / docs (git fetch only populates the .git object cache, which the directive
# authorizes as the way to READ a remote branch). Output kept <=35 lines.
# Non-zero exit on ANY failure or missing input; the exit code propagates (house law #3).
# POSIX bash + python3 stdlib only. Network: canonical URL only (house law #4).
set -euo pipefail

URL="https://github.com/lukemcalister10/afl-rl-engine.git"
HERE="$(cd "$(dirname "$0")" && cd ../.. && pwd)"
die() { echo "prescreen: FAIL — $*" >&2; exit 1; }

[ $# -eq 2 ] || die "usage: prescreen.sh <branch> <base_sha>"
BRANCH="$1"; BASE="$2"
BOARD="data/rl_build/rl_app_data.json"; EB="data/expected_boot.json"

# --- read the remote candidate (fetch = read; canonical URL only) ---
git -C "$HERE" fetch --quiet "$URL" "$BRANCH" 2>/dev/null || die "fetch branch '$BRANCH' from canonical URL failed"
HEAD="$(git -C "$HERE" rev-parse FETCH_HEAD)" || die "rev-parse FETCH_HEAD failed"
git -C "$HERE" cat-file -e "${BASE}^{commit}" 2>/dev/null \
  || git -C "$HERE" fetch --quiet "$URL" "$BASE" 2>/dev/null \
  || die "base_sha '$BASE' not reachable from canonical URL"
git -C "$HERE" cat-file -e "${HEAD}^{commit}" 2>/dev/null || die "head object missing after fetch"

show() { git -C "$HERE" show "$1:$2" 2>/dev/null; }   # empty+nonzero if path absent at that rev

echo "== prescreen · $BRANCH =="
echo "branch     : $BRANCH"
echo "base       : $BASE"
echo "head       : $HEAD   (git rev-parse FETCH_HEAD)"

# --- FIRST CHECK (base guard, directive 2026-07-17 / register items 264·270·298·299): the branch's
#     FIRST commit above the base must carry FIRST_COMMANDS_PROOF.txt, and the SHA it recorded must
#     equal the branch's ACTUAL base (the parent of that first commit) AND the pinned base we were
#     handed. A content-copy branch (item 270/298) fails here: its first commit sits on main, not the
#     pin, so the recorded pin != the actual parent. This runs BEFORE anything else is read — the
#     item-298 SEAM NOTE: prescreen verifies the ancestor proof before reading the candidate. ---
echo "-- FIRST_COMMANDS_PROOF check (base guard, first artifact) --"
FIRST="$(git -C "$HERE" rev-list --reverse --ancestry-path "${BASE}..${HEAD}" 2>/dev/null | head -n1 || true)"
if [ -z "$FIRST" ]; then
  die "cannot locate the branch's first commit above base — ${BASE:0:8}..${HEAD:0:8} has no ancestry path (base NOT an ancestor of head: the wrong-base failure, items 270/298)"
fi
PROOF_TXT="$(show "$FIRST" "FIRST_COMMANDS_PROOF.txt")" \
  || die "branch's first commit ${FIRST:0:8} does NOT contain FIRST_COMMANDS_PROOF.txt (the base guard's first artifact is missing — items 298/299)"
[ -n "$PROOF_TXT" ] || die "FIRST_COMMANDS_PROOF.txt is empty at first commit ${FIRST:0:8} (SILENCE IS A RED)"
REC_SHA="$(printf '%s\n' "$PROOF_TXT" | grep -E '^base_sha' | head -n1 | grep -oE '[0-9a-fA-F]{40}' | head -n1 || true)"
[ -n "$REC_SHA" ] || die "FIRST_COMMANDS_PROOF.txt at ${FIRST:0:8} carries no 'base_sha' 40-hex line (cannot read the recorded base)"
ACTUAL_BASE="$(git -C "$HERE" rev-parse "${FIRST}^" 2>/dev/null || true)"
[ -n "$ACTUAL_BASE" ] || die "cannot resolve parent of first commit ${FIRST:0:8} (its actual base)"
if [ "$REC_SHA" = "$ACTUAL_BASE" ] && [ "$REC_SHA" = "$BASE" ]; then
  echo "  proof      : PASS  first commit ${FIRST:0:8} records base_sha ${REC_SHA:0:8} == actual parent ${ACTUAL_BASE:0:8} == pinned base ${BASE:0:8}"
elif [ "$REC_SHA" != "$ACTUAL_BASE" ]; then
  die "recorded base ${REC_SHA:0:8} != first commit's ACTUAL parent ${ACTUAL_BASE:0:8} — the proof claims a base the branch was not cut from (content-copied? items 270/298)"
else
  die "recorded base ${REC_SHA:0:8} != the pinned base ${BASE:0:8} we were handed — branch's first commit proves a different pin"
fi

# --- ancestry (raw SHAs, explicit verdict) ---
if git -C "$HERE" merge-base --is-ancestor "$BASE" "$HEAD" 2>/dev/null; then
  echo "ancestry   : YES  base $(echo "$BASE" | cut -c1-8) is-ancestor head $(echo "$HEAD" | cut -c1-8)"
else
  echo "ancestry   : NO   base $(echo "$BASE" | cut -c1-8) NOT ancestor of head $(echo "$HEAD" | cut -c1-8)"
fi

# --- changed files (name-status) — fence-relevant paths named individually; session_*/ scratch
#     rolled up per top-dir so the ≤35-line budget survives a big candidate without hiding a fence touch.
echo "-- diff --name-status base..head (session_*/ rolled up) --"
DIFF="$(git -C "$HERE" diff --name-status "$BASE" "$HEAD")" || die "diff base..head failed"
if [ -z "$DIFF" ]; then
  echo "  (no file changes base..head)"
else
  printf '%s\n' "$DIFF" | python3 -c '
import sys, collections
roll = collections.Counter()
for line in sys.stdin:
    line = line.rstrip("\n")
    if not line.strip():
        continue
    parts = line.split("\t", 1)
    path = parts[1] if len(parts) > 1 else line
    if path.startswith("session_"):
        roll[path.split("/", 1)[0]] += 1        # scratch/session dirs: count, dont enumerate
    else:
        print("  " + line)                        # fence-relevant: name it
for d in sorted(roll):
    print("  ~\t%s/ (%d files, session scratch)" % (d, roll[d]))
' || die "diff rollup failed"
fi

# --- board md5 recomputed at head, beside expected_boot's board pin at head ---
BMD5="$(show "$HEAD" "$BOARD" | md5sum | cut -d' ' -f1)"
[ -n "$BMD5" ] || die "board file $BOARD absent at head (cannot recompute board md5)"
PIN="$(show "$HEAD" "$EB" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("board",""))' 2>/dev/null)" \
  || die "expected_boot.json unreadable at head"
[ -n "$PIN" ] || die "expected_boot.json has no board pin at head"
if [ "${BMD5:0:${#PIN}}" = "$PIN" ] || [ "${PIN:0:8}" = "${BMD5:0:8}" ]; then V="MATCH"; else V="DRIFT"; fi
echo "board      : recomputed ${BMD5:0:8} vs pin ${PIN:0:8}  -> $V   (md5 of $BOARD @head)"

# --- expected_boot changed-field list (base vs head) ---
echo "-- expected_boot changed fields (base..head) --"
EB_BASE="$(show "$BASE" "$EB")" || true
EB_HEAD="$(show "$HEAD" "$EB")" || true
[ -n "$EB_HEAD" ] || die "expected_boot.json absent at head"
printf '%s\1%s' "$EB_BASE" "$EB_HEAD" | python3 -c '
import json,sys
raw=sys.stdin.read().split("\1",1)
b=json.loads(raw[0]) if raw[0].strip() else {}
h=json.loads(raw[1]) if len(raw)>1 and raw[1].strip() else {}
keys=[k for k in sorted(set(b)|set(h)) if not k.startswith("_")]
ch=[k for k in keys if b.get(k)!=h.get(k)]
if not ch: print("  (no expected_boot field changed)")
for k in ch:
    print("  %-12s %s -> %s" % (k, str(b.get(k))[:8], str(h.get(k))[:8]))
' || die "expected_boot field diff failed"

# --- book seal + any stamped __meta__ at head ---
echo "-- book seal (data/book_stable_seal.json @head) --"
show "$HEAD" "data/book_stable_seal.json" | python3 -c '
import json,sys
try: d=json.load(sys.stdin)
except Exception: print("  (no book_stable_seal.json at head)"); sys.exit(0)
print("  seal head=%s store=%s n=%s sha256=%s" % (
  str(d.get("head_md5"))[:8], str(d.get("store_md5"))[:8], d.get("n_players"), str(d.get("stable_sha256"))[:12]))
' || die "book seal parse failed"
META="$(git -C "$HERE" ls-tree -r --name-only "$HEAD" data 2>/dev/null | grep '^data/s4_matrix.*\.json$' || true)"
FOUND=""
for f in $META; do
  L="$(show "$HEAD" "$f" | python3 -c '
import json,sys
try: d=json.load(sys.stdin); m=d.get("__meta__")
except Exception: sys.exit(0)
if m: print("  __meta__ %s head=%s store=%s n=%s"%(__import__("sys").argv[1], str(m.get("engine_head_md5"))[:8], str(m.get("store_md5"))[:8], m.get("n_players")))
' "$(basename "$f")" 2>/dev/null || true)"
  [ -n "$L" ] && { echo "$L"; FOUND=1; }
done
[ -n "$FOUND" ] || echo "  __meta__ : none stamped in data/s4_matrix*.json @head (seal is the record)"

# --- run_panel.sh pin diff (base vs head) ---
echo "-- run_panel.sh pin diff (base..head) --"
RP_B="$(show "$BASE" "run_panel.sh" | grep -E 'RL_|PAR_RAMPS|PYTHONHASHSEED' || true)"
RP_H="$(show "$HEAD" "run_panel.sh" | grep -E 'RL_|PAR_RAMPS|PYTHONHASHSEED' || true)"
if [ "$RP_B" = "$RP_H" ]; then
  echo "  pins UNCHANGED base..head"
else
  echo "  PINS DIFFER — base then head:"
  diff <(printf '%s\n' "$RP_B") <(printf '%s\n' "$RP_H") | sed 's/^/  /' || true
fi

# --- NEW-ENV-READ CHECK (register item 114): ADDED os.environ.get/getenv in engine/ ---
echo "-- new env-read check in engine/ (register item 114) --"
ADDED="$(git -C "$HERE" diff "$BASE" "$HEAD" -- engine \
        | grep -E '^\+' | grep -vE '^\+\+\+' \
        | grep -E 'os\.environ\.get|os\.getenv|getenv\(' || true)"
if [ -z "$ADDED" ]; then
  echo "  none — no ADDED os.environ.get/getenv in engine/ (no unpinned board dial introduced)"
else
  echo "  FLAG — ADDED env reads in engine/ (must be pinned per item 114):"
  printf '%s\n' "$ADDED" | sed 's/^/  /'
fi

echo "== prescreen done =="
