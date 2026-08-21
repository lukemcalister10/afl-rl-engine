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

# 2) The OPEN-ITEMS register's freshest line — the durable freshness rung (raw, truncated).
#    Repointed by the 3b act (2026-08-21): the record continues at docs/register/, and LATEST.md
#    line 1 carries the newest version + summary. The old file is frozen (its line 1 is sealed at
#    v812 forever, so it can no longer answer "how fresh"). Missing/empty = a RED (house law #3).
echo "-- open-items register, newest entry (docs/register/LATEST.md line 1) --"
[ -f "$HERE/docs/register/LATEST.md" ] \
  || die "docs/register/LATEST.md missing (open-items register is the durable freshness input)"
OIR_HDR="$(head -n1 "$HERE/docs/register/LATEST.md")" || die "cannot read docs/register/LATEST.md"
[ -n "$OIR_HDR" ] || die "docs/register/LATEST.md header line is empty (SILENCE IS A RED)"
if [ "${#OIR_HDR}" -gt 200 ]; then
  printf '  %s …(truncated)\n' "${OIR_HDR:0:200}"
else
  printf '  %s\n' "$OIR_HDR"
fi

# 2b) The LTI/availability register header (pinned input, root) — kept, honestly relabelled.
#     This is the availability sidecar, NOT the open-items log printed above.
echo "-- LTI register header (pinned input, root) --"
REG_HDR="$(head -n1 "$HERE/LTI_REGISTER.md")" || die "cannot read LTI_REGISTER.md"
[ -n "$REG_HDR" ] || die "LTI_REGISTER.md header line is empty"
echo "  $REG_HDR"

# 3) docs/ listing (raw).
echo "-- docs/ listing --"
ls -1 "$HERE/docs" | sed 's/^/  /'

# 4) THE PACK-DOC PK COMPARE IS RETIRED (2026-08-21, the 3c act). Replaced by the live-doc headers
#    below. Why, named rather than quietly dropped:
#
#      * The pack it compared no longer exists at docs/. 00_MANIFEST_*, CORE_*, DECISIONS_* and
#        CONSTRAINTS_* were archived to docs/archive/ long before this act — the newest of them are
#        dated 2026-07-19 — and this script had been dying on the FIRST of them
#        ("pack doc missing: MANIFEST") ever since, taking the whole run to exit 1 and taking the
#        register freshness rung above it down with it. The section was checking a Project-Knowledge
#        pack that is not maintained any more, so a "repoint at the archive" would print the header
#        of a doc frozen in July and invite a seat to compare live work against it.
#      * docs/acceptance_*.json must NOT be resurrected here in any form. The derived laws twin
#        (docs/acceptance_v2_0.json) was REMOVED by the RULEBOOK v3 amendment on the owner's word,
#        and tools/rulebook_lint.py R5/R6 now red on a second laws file REAPPEARING (RULEBOOK PART 4,
#        process law P10). An orientation tool that went looking for one would be teaching the
#        retirement backwards.
#      * The historical pack is still in the tree, at docs/archive/, and is read as HISTORY when a
#        task reaches it. It is named here so nothing is hidden by the removal.
#
#    What a seat actually needs to compare now is the LIVE governing set, so that is what prints.
echo "-- pack doc PK compare: RETIRED 2026-08-21 (the pack is archived at docs/archive/) --"
echo "-- live governing docs, raw headers --"
emit() { # $1=label  $2=file
  local label="$1" f="$2" hdr
  [ -f "$f" ] || die "live governing doc missing: $label ($f)"
  hdr="$(head -n1 "$f")" || die "cannot read header: $f"
  [ -n "$hdr" ] || die "$label header line is empty (SILENCE IS A RED)"
  printf '  %-11s %-34s %s\n' "$label" "$(basename "$f")" "${hdr:0:150}"
}
emit RULEBOOK "$HERE/docs/RULEBOOK.md"
emit SSI      "$HERE/docs/SINGLE_SOURCE_INVARIANT.md"
emit PRIMER   "$HERE/docs/ENGINE_PRIMER.md"
emit STATE    "$HERE/docs/STATE.md"

echo "== orient OK =="
