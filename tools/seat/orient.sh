#!/usr/bin/env bash
# orient.sh — SEAT TOOLS (P3) · Tier-3 READ-ONLY freshness check.
# One command: is my seat looking at the live tree, and does Project-Knowledge match the repo?
# Prints RAW SHAs and RAW version strings — never a bare verdict (house law #2).
# WRITES NOTHING. POSIX bash + python3 stdlib only. Network: canonical URL only (house law #4).
# Non-zero exit on ANY failure or missing input; the exit code propagates (house law #3 — SILENCE IS A RED).
set -euo pipefail

URL="https://github.com/lukemcalister10/afl-rl-engine.git"
HERE="$(cd "$(dirname "$0")" && cd ../.. && pwd)"   # repo root (tools/seat -> ../..)
die() { echo "orient: FAIL — $*" >&2; exit 1; }

[ -d "$HERE/docs" ] || die "docs/ not found under repo root $HERE (run from a checkout)"
[ -f "$HERE/LTI_REGISTER.md" ] || die "LTI_REGISTER.md missing (register is a pinned input)"

echo "== orient · $URL =="

# 1) LIVE remote refs — RAW SHAs (canonical URL only).
echo "-- ls-remote (RAW SHAs) --"
LS="$(git ls-remote "$URL" refs/heads/main refs/tags/v2.9 2>/dev/null)" \
  || die "ls-remote against canonical URL failed (network / URL)"
[ -n "$LS" ] || die "ls-remote returned nothing (no main / no v2.9 tag)"
printf '%s\n' "$LS" | while IFS=$'\t' read -r sha ref; do
  printf '  %-22s %s\n' "$ref" "$sha"
done
# checked-out HEAD, for the reader to compare against live main by eye.
HEAD_SHA="$(git -C "$HERE" rev-parse HEAD)" || die "rev-parse HEAD failed"
printf '  %-22s %s\n' "checkout HEAD" "$HEAD_SHA"

# 2) The register's OWN header line (raw).
echo "-- register header (raw line 1) --"
REG_HDR="$(head -n1 "$HERE/LTI_REGISTER.md")" || die "cannot read LTI_REGISTER.md"
[ -n "$REG_HDR" ] || die "LTI_REGISTER.md header line is empty"
echo "  $REG_HDR"

# 3) docs/ listing (raw).
echo "-- docs/ listing --"
ls -1 "$HERE/docs" | sed 's/^/  /'

# 4) Pack-doc HEADER VERSION table for PK comparison — raw version string per doc.
#    Glob by prefix so a version bump (new filename) is still found; print filename + header.
echo "-- pack doc HEADER VERSIONS (for PK compare) --"
emit() { # $1=label  $2=glob-or-file
  local label="$1" pat="$2" f hdr
  # shellcheck disable=SC2086
  f="$(ls -1 $pat 2>/dev/null | sort | tail -n1)" || true
  if [ -z "${f:-}" ] || [ ! -f "$f" ]; then
    die "pack doc missing: $label ($pat) — PK/repo compare cannot be made"
  fi
  if [ "${f##*.}" = "json" ]; then
    hdr="$(python3 -c 'import json,sys;d=json.load(open(sys.argv[1]));print("version",d.get("version"),"date",d.get("date"))' "$f")" \
      || die "cannot parse JSON header: $f"
  else
    hdr="$(head -n1 "$f")" || die "cannot read header: $f"
  fi
  printf '  %-11s %-34s %s\n' "$label" "$(basename "$f")" "$hdr"
}
emit MANIFEST    "$HERE/docs/00_MANIFEST_*.md"
emit CORE        "$HERE/docs/CORE_*.md"
emit HANDOVER    "$HERE/docs/HANDOVER_*.md"
emit DECISIONS   "$HERE/docs/DECISIONS_*.md"
emit CONSTRAINTS "$HERE/docs/CONSTRAINTS_*.md"
emit acceptance  "$HERE/docs/acceptance_*.json"
emit SSI         "$HERE/docs/SINGLE_SOURCE_INVARIANT.md"

echo "== orient OK =="
