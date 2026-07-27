#!/usr/bin/env python3
# ===== BEGIN ITEM 411 D1 PROVENANCE HEADER — NOT PART OF THE PROVEN ARTIFACT =====
#
# ITEM 411 / D1 — STORE ATTRIBUTION, BOTH DIRECTIONS: SESSION-LOCAL VERIFICATION SCRIPT.
#
#   Reconstruction label : ITEM_411_D1_attribute.py — review instrument
#   Author               : d1-cold-review
#   Date                 : 2026-07-27
#
# ----------------------------------------------------------------------------------------
# READ THIS FIRST — WHAT THIS FILE IS NOT
# ----------------------------------------------------------------------------------------
# This is a SESSION-LOCAL VERIFICATION SCRIPT. IT IS NOT PRODUCTION CODE AND IT IS NOT THE
# ARTIFACT OF RECORD. It carries no proof of its own, and it DOES NOT INHERIT THE PROOF
# ATTACHED TO ITS SIBLING. ITEM_411_D1_transform.py has a byte-exact reproduction result
# against a committed input pair; THIS FILE HAS NO SUCH RESULT, and nothing in this header
# should be read as extending that one to cover this script. The two files were committed
# together and share nothing else.
#
# ----------------------------------------------------------------------------------------
# ITS STANDING, EXACTLY — AND NOTHING STRONGER
# ----------------------------------------------------------------------------------------
#
#   "Produces the reported verdict (FORWARD PASS / REVERSE PASS, exit 0)."
#
# That is the whole of its standing. THERE IS NO BYTE-EXACT REPRODUCTION PROOF ATTACHED TO
# THIS SCRIPT. It reports a verdict; it does not prove itself, and a verdict it prints is
# evidence about the stores and the manifest, never evidence about this instrument.
#
# DELETION RULE
#   This header is provenance, not code. To remove it, delete from the FIRST BYTE of the
#   BEGIN line above through and INCLUDING the newline that terminates the END line below.
#   Deleting exactly that span, no more and no less, restores the as-run file byte-for-byte
#   (as-run sha256 recorded at the foot of this header). Every line of this header is a `#`
#   comment and Python comments are not statements, so the module docstring below is still
#   __doc__ and no semantic of the script is altered by the header's presence.
#
# ----------------------------------------------------------------------------------------
# RE-RUNNING IT — HARDCODED SCRATCH PATH AT SP
# ----------------------------------------------------------------------------------------
# This script HARDCODES ITS SCRATCH PATH in the module-level constant SP, which points at
# the review session's own scratch directory and WILL NOT EXIST for anyone else. There is no
# argument parsing and no fallback: with SP pointing nowhere the script dies at import time
# on the first open(). A RE-RUNNER MUST EITHER REPOINT SP OR STAGE THESE THREE INPUTS UNDER
# IT:
#
#       {SP}/store_base.json
#       {SP}/store_cand.json
#       {SP}/prep/ITEM_411_CHANGE_MANIFEST.csv
#
# The two stores are `git cat-file -p` of engine/rl_after/rl_model_data.json — store_base
# from the base pin, store_cand from the branch tip. The manifest is the hash-verified
# change manifest. This instrument READS ONLY those three files and writes nothing.
#
# ----------------------------------------------------------------------------------------
# THIS IS THE CORRECTED VERSION
# ----------------------------------------------------------------------------------------
# The ORIGINAL instrument was WRONG. It MIS-COMPARED AN ABSENT KEY AGAINST AN EXPLICIT NULL
# and on that basis REPORTED 8,711 FALSE REVERSE FAILURES. Those 8,711 rows are not a
# coincidence: they are exactly the fields that are absent-or-null in the baseline store,
# the same population that takes the transform's type-inference branch.
#
# The two states are INDISTINGUISHABLE FOR ATTRIBUTION PURPOSES — the manifest declares such
# an old_value as an empty cell either way — so treating them as different was a defect in
# the instrument and never a finding about the stores. FIXED BY AN "<absent>" -> "<none>"
# NORMALISATION APPLIED AT THE REVERSE-COMPARISON SITE (the nb / nc normalisation inside the
# reverse loop, immediately before the comparison against mnorm). The forward pass never had
# the defect and is unchanged.
#
# IF YOU RUN THIS AND SEE 8,711 REVERSE FAILURES, YOU ARE RUNNING THE UNCORRECTED VERSION.
#
# ----------------------------------------------------------------------------------------
# THIS FILE IS THE SPECIFICATION OF WHAT "HARDENED" MEANS
# ----------------------------------------------------------------------------------------
# The routine store-maintenance lane's HARDENED SUCCESSOR is specified by what this script
# checks, because these are precisely the checks the transform does not perform:
#
#   FORWARD  — every player-level manifest row lands in the candidate store, with the
#              manifest's old_value agreeing against the base store, and every declared
#              __ROW__ removal actually realised.
#   REVERSE  — every base->candidate store delta is explained by a manifest row, with
#              removals and additions individually accounted for and none unexplained.
#   PLUS     — duplicate-key rejection on both stores, and a census of inert rows whose
#              old_value equals new_value.
#
# A successor that applies edits WITHOUT these is the applicator without its interlock, and
# is not hardened whatever else it does.
#
# ----------------------------------------------------------------------------------------
# LOAD-BEARING INVISIBLE CHARACTER — U+FEFF — DO NOT LET ANY TOOL TOUCH THIS FILE
# ----------------------------------------------------------------------------------------
# There is a literal U+FEFF (bytes EF BB BF) INSIDE A STRING LITERAL, in the line that reads
#
#       r["entity_type"] = r.pop("<U+FEFF HERE>entity_type")
#
# It is NOT a leading byte-order mark; it sits mid-source and is INVISIBLE in every editor.
# It is REQUIRED: the change manifest's first header cell is BOM-prefixed and csv.DictReader
# yields that key verbatim. STRIP IT OR NORMALISE IT AND THE SCRIPT DIES WITH KeyError. DO
# NOT lint, format, reflow, retype, re-encode, or round-trip this file through any tool that
# may alter encoding or line endings. There is exactly ONE occurrence in this file; if a
# tool reports zero, or two, the file is already damaged.
#
# COORDINATES — AS-RUN VERSUS COMMITTED. The AS-RUN coordinate is BYTE 677 (0-based) /
# LINE 17. THAT IS TRUE OF THE AS-RUN FILE AND IT BECOMES FALSE OF THIS COMMITTED FILE,
# because this header shifts every byte below it. In THIS COMMITTED FILE the same single
# character sits at BYTE 7949 (0-based) / LINE 135. Strip this header per the deletion rule
# above and the as-run coordinate is restored exactly.
#
# ----------------------------------------------------------------------------------------
# HASH
# ----------------------------------------------------------------------------------------
# AS-RUN sha256 — this file with this header stripped per the deletion rule:
#
#   b4edab35f46d3f6207f754d9e66223a38720ac4209116c593030b22501c962ab
#
# This file's OWN committed hash is deliberately NOT recorded here; a file cannot contain
# its own hash. It is in the commit message.
#
# ===== END ITEM 411 D1 PROVENANCE HEADER =====
"""ITEM 411 — store-level attribution, BOTH directions.

FORWARD  : every player-level manifest row lands in the candidate store.
REVERSE  : every base->candidate store delta is explained by a manifest row.

Cold-review instrument. Reads only: the two committed stores + the hash-verified manifest.
"""
import csv, json, sys, collections

SP = "/tmp/claude-0/-home-user-afl-rl-engine/75935eb9-16eb-55dc-ad47-8a353aa3a515/scratchpad"

base = json.load(open(f"{SP}/store_base.json"))
cand = json.load(open(f"{SP}/store_cand.json"))
rows = list(csv.DictReader(open(f"{SP}/prep/ITEM_411_CHANGE_MANIFEST.csv")))
for r in rows:
    r["entity_type"] = r.pop("﻿entity_type")

B = {r["key"]: r for r in base}
C = {r["key"]: r for r in cand}
assert len(B) == len(base) and len(C) == len(cand), "duplicate keys in a store"


def norm(v):
    """Canonical comparison form for a store value vs a manifest string cell."""
    if v is None:
        return "<none>"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def mnorm(s):
    """Manifest cell -> comparison form. Empty cell means absent/null."""
    if s is None:
        return "<none>"
    s = s.strip()
    if s == "" or s.lower() in ("none", "null", "nan"):
        return "<none>"
    return s


player_rows = [r for r in rows if r["entity_type"] == "player"]
ref_rows = [r for r in rows if r["entity_type"] != "player"]
removals = [r for r in player_rows if r["field"] == "__ROW__"]
edits = [r for r in player_rows if r["field"] != "__ROW__"]

print("=" * 78)
print("SCOPE")
print("=" * 78)
print(f"  manifest rows total        : {len(rows)}")
print(f"  player-level rows          : {len(player_rows)}")
print(f"    field edits              : {len(edits)}")
print(f"    row removals (__ROW__)   : {len(removals)}")
print(f"  year_reference rows        : {len(ref_rows)}  (no store field — out of store scope)")
print(f"  base store players         : {len(base)}")
print(f"  candidate store players    : {len(cand)}")

# ---------------------------------------------------------------- FORWARD
print()
print("=" * 78)
print("FORWARD — every player-level manifest row lands in the candidate store")
print("=" * 78)

f_ok = f_newbad = f_oldbad = f_missing = 0
f_fail = []
for r in edits:
    k, f = r["entity_id"], r["field"]
    if k not in C:
        f_missing += 1
        f_fail.append((k, f, "entity absent from candidate store"))
        continue
    got = norm(C[k].get(f))
    want = mnorm(r["new_value"])
    if got != want:
        f_newbad += 1
        f_fail.append((k, f, f"cand={got!r} != manifest new_value={want!r}"))
        continue
    # old_value must match the base store (entity may be new, but none are here)
    if k in B:
        gotb = norm(B[k].get(f))
        wantb = mnorm(r["old_value"])
        if gotb != wantb:
            f_oldbad += 1
            f_fail.append((k, f, f"base={gotb!r} != manifest old_value={wantb!r}"))
            continue
    f_ok += 1

print(f"  field edits attributed FORWARD : {f_ok} / {len(edits)}")
print(f"    new_value mismatch in cand   : {f_newbad}")
print(f"    old_value mismatch in base   : {f_oldbad}")
print(f"    entity missing from cand     : {f_missing}")

r_ok = 0
for r in removals:
    k = r["entity_id"]
    if k in B and k not in C:
        r_ok += 1
        print(f"  REMOVAL verified               : {k!r} present in base, absent from candidate")
    else:
        f_fail.append((k, "__ROW__", f"in_base={k in B} in_cand={k in C} — removal not realised"))

if f_fail:
    print(f"\n  FORWARD FAILURES ({len(f_fail)}) — first 25:")
    for k, f, why in f_fail[:25]:
        print(f"    {k:<32} {f:<22} {why}")

# ---------------------------------------------------------------- REVERSE
print()
print("=" * 78)
print("REVERSE — every base->candidate store delta is explained by a manifest row")
print("=" * 78)

# index the manifest by (entity, field)
midx = collections.defaultdict(list)
for r in edits:
    midx[(r["entity_id"], r["field"])].append(r)

deltas = []
all_fields = set()
for k in set(B) | set(C):
    all_fields |= set(B.get(k, {}).keys()) | set(C.get(k, {}).keys())

removed_keys = set(B) - set(C)
added_keys = set(C) - set(B)

for k in sorted(set(B) & set(C)):
    b, c = B[k], C[k]
    for f in sorted(set(b) | set(c)):
        ob, oc = b.get(f, "<absent>"), c.get(f, "<absent>")
        if json.dumps(ob, sort_keys=True) != json.dumps(oc, sort_keys=True):
            deltas.append((k, f, ob, oc))

print(f"  rows removed base->cand        : {len(removed_keys)}  {sorted(removed_keys)}")
print(f"  rows added   base->cand        : {len(added_keys)}  {sorted(added_keys)}")
print(f"  field-level deltas (common rows): {len(deltas)}")

unattributed = []
attributed = 0
for k, f, ob, oc in deltas:
    cands = midx.get((k, f))
    if not cands:
        unattributed.append((k, f, ob, oc, "NO manifest row for this (entity,field)"))
        continue
    m = cands[0]
    # an ABSENT key and an explicit null are the same state for attribution purposes:
    # the manifest declares such an old_value as an empty cell.
    nb = "<none>" if ob == "<absent>" else norm(ob)
    nc = "<none>" if oc == "<absent>" else norm(oc)
    if nc != mnorm(m["new_value"]) or nb != mnorm(m["old_value"]):
        unattributed.append((k, f, ob, oc,
                             f"manifest says {mnorm(m['old_value'])!r}->{mnorm(m['new_value'])!r}"))
        continue
    attributed += 1

print(f"  deltas ATTRIBUTED to manifest  : {attributed} / {len(deltas)}")
print(f"  deltas UNATTRIBUTED            : {len(unattributed)}")

# removals explained?
rem_manifest = {r["entity_id"] for r in removals}
rem_unexplained = removed_keys - rem_manifest
add_unexplained = added_keys
print(f"  removals unexplained           : {len(rem_unexplained)}  {sorted(rem_unexplained)}")
print(f"  additions unexplained          : {len(add_unexplained)}  {sorted(add_unexplained)}")

if unattributed:
    print(f"\n  UNATTRIBUTED DELTAS ({len(unattributed)}) — first 40:")
    for k, f, ob, oc, why in unattributed[:40]:
        print(f"    {k:<30} {f:<22} {str(ob)[:18]:<18} -> {str(oc)[:18]:<18} {why}")

# manifest rows that produced NO store delta (claimed but inert)
delta_pairs = {(k, f) for k, f, _, _ in deltas}
noop_rows = [r for r in edits if (r["entity_id"], r["field"]) not in delta_pairs]
print()
print(f"  manifest field-edit rows with NO store delta : {len(noop_rows)}")
if noop_rows:
    byf = collections.Counter(r["field"] for r in noop_rows)
    for f, n in byf.most_common(10):
        print(f"      {f:<24} {n}")
    print("    (these are rows whose old_value == new_value, i.e. declared but inert)")

print()
print("=" * 78)
verdict_fwd = (f_ok == len(edits)) and (r_ok == len(removals)) and not f_fail
verdict_rev = (not unattributed) and (not rem_unexplained) and (not add_unexplained)
print(f"FORWARD verdict : {'PASS' if verdict_fwd else 'FAIL'}")
print(f"REVERSE verdict : {'PASS' if verdict_rev else 'FAIL'}")
print("=" * 78)
sys.exit(0 if (verdict_fwd and verdict_rev) else 1)
