#!/usr/bin/env python3
"""
THE DOB COURIER STORE WRITE — 2026-08-10.

The write that #290's runbook section 5 ("THE DOB COURIER ACT") specified and never fired.
One atomic, exact-byte pass over the single source engine/rl_after/rl_model_data.json:
302 staged rows get their birth year (_by) and birth date (_bd), joined on the store key.

SINGLE SOURCE for this act:
  1. docs/evidence/dob_courier_2026-07-31/dob_courier_staging_302.csv  (302 rows, columns key,player,_by,_bd,provenance)
  2. the two owner overrides below, from his word of 2026-08-10 (issue #334 comment 5235574982),
     which SUPERSEDE the staging file for those two keys only.

Nothing else about any record is touched. No field is removed. No record is added or dropped.

FAIL-CLOSED. The script HALTS and writes nothing if:
  - the store md5 on entry is not the expected pin,
  - any staged key is missing from the store,
  - a staged key hits more than one store record,
  - a staged player name disagrees with the store's name for that key,
  - the row count is not exactly 302,
  - the modified store does not re-serialise byte-identically apart from the intended field edits.

FIELD PLACEMENT. All 302 target records already carry "_by" (explicit null) and carry no "_bd" at all.
"_by" is set in place, preserving key order. "_bd" is inserted immediately after "_pickless", which is
where the store's own dominant convention puts it (781 of the 848 records that already carry a birth
date are shaped exactly that way, and all 302 targets have "_pickless" followed by "future_position").

Usage:  python3 write_dob.py <repo_root>
"""
import csv
import hashlib
import json
import os
import sys

STORE_REL = "engine/rl_after/rl_model_data.json"
STAGING_REL = "docs/evidence/dob_courier_2026-07-31/dob_courier_staging_302.csv"

EXPECTED_STORE_MD5_BEFORE = "0dd6b4a01e16dabf8d3a388d8f8ac1f2"
EXPECTED_ROWS = 302

# ---------------------------------------------------------------------------
# THE TWO OWNER OVERRIDES — owner's word 2026-08-10, relayed at issue #334
# comment 5235574982:  "Ruory Kirkby - 4/2/86. Tim Looby - 2/9/87. Write the
# birthdates."  Read day/month/year per Australian convention, as the brief
# states.  These were the crosscheck's two DISCREPANT rows; the 2026-07-31
# staging file carries them YEAR-ONLY (_bd deliberately empty) under the
# then-standing seam ruling.  The owner's fresh word supersedes that ruling
# for these two keys, and his values rule.
# ---------------------------------------------------------------------------
OWNER_OVERRIDES = {
    "ruory-kirkby": {
        "_by": 1986,
        "_bd": "1986-02-04",
        "provenance": 'owner word 2026-08-10 (issue #334 comment 5235574982): "Ruory Kirkby - 4/2/86" — read day/month/year. Supersedes the 2026-07-31 year-only staging row.',
    },
    "tim-looby": {
        "_by": 1987,
        "_bd": "1987-09-02",
        "provenance": 'owner word 2026-08-10 (issue #334 comment 5235574982): "Tim Looby - 2/9/87" — read day/month/year. Supersedes the 2026-07-31 year-only staging row.',
    },
}


def halt(msg):
    print("HALT: " + msg, file=sys.stderr)
    sys.exit(1)


def main():
    root = os.path.abspath(sys.argv[1])
    store_path = os.path.join(root, STORE_REL)
    staging_path = os.path.join(root, STAGING_REL)
    out_dir = os.path.join(root, "docs/evidence/dob_write_2026-08-10")

    raw_before = open(store_path, "rb").read()
    md5_before = hashlib.md5(raw_before).hexdigest()
    print("store md5 before : %s" % md5_before)
    if md5_before != EXPECTED_STORE_MD5_BEFORE:
        halt("store md5 %s != expected %s" % (md5_before, EXPECTED_STORE_MD5_BEFORE))

    data = json.loads(raw_before)
    # PROOF THE WRITE IS EXACT-BYTE: the store round-trips through json byte-identically,
    # so any byte that moves in the output moved because this script moved it.
    if json.dumps(data).encode() != raw_before:
        halt("store does not round-trip byte-identically through json; an exact-byte write is not available by this route")

    index = {}
    for rec in data:
        k = rec.get("key")
        if k in index:
            halt("store carries duplicate key %r; the join is not one-to-one" % k)
        index[k] = rec

    staged = list(csv.DictReader(open(staging_path, newline="")))
    if len(staged) != EXPECTED_ROWS:
        halt("staging file has %d rows, expected %d" % (len(staged), EXPECTED_ROWS))

    # --- join validation, all of it, before a single byte is written ---
    missing, name_conflicts, dup_staged = [], [], []
    seen = set()
    for row in staged:
        k = row["key"]
        if k in seen:
            dup_staged.append(k)
        seen.add(k)
        if k not in index:
            missing.append(k)
            continue
        store_name = str(index[k].get("player", "")).strip()
        if row["player"].strip() != store_name:
            name_conflicts.append((k, row["player"], store_name))
    if missing:
        halt("%d staged keys do not exist in the store: %s" % (len(missing), missing))
    if dup_staged:
        halt("staging file repeats keys: %s" % dup_staged)
    if name_conflicts:
        halt("player name disagrees with the store on %d keys: %s" % (len(name_conflicts), name_conflicts))
    for k in OWNER_OVERRIDES:
        if k not in index:
            halt("owner-override key %r is not in the store" % k)
        if k not in seen:
            halt("owner-override key %r is not in the staging file" % k)

    # --- the write ---
    applied = []
    for row in staged:
        k = row["key"]
        rec = index[k]
        old_by = rec.get("_by", None)
        old_bd = rec.get("_bd", None)

        staged_by = int(row["_by"]) if row["_by"].strip() else None
        staged_bd = row["_bd"].strip() or None

        ov = OWNER_OVERRIDES.get(k)
        if ov is not None:
            new_by, new_bd = ov["_by"], ov["_bd"]
            source = "OWNER OVERRIDE 2026-08-10"
        else:
            new_by, new_bd = staged_by, staged_bd
            source = "staging 2026-07-31"

        if new_by is None or new_bd is None:
            halt("row %r would write a null birth year or birth date; every one of the 302 must land complete" % k)

        rec["_by"] = new_by
        if "_bd" in rec:
            rec["_bd"] = new_bd
        else:
            # insert immediately after "_pickless", the store's own convention
            keys = list(rec.keys())
            if "_pickless" not in keys:
                halt("record %r has no _pickless field; field placement convention does not apply" % k)
            pos = keys.index("_pickless") + 1
            rebuilt = {}
            for i, kk in enumerate(keys):
                rebuilt[kk] = rec[kk]
                if i + 1 == pos:
                    rebuilt["_bd"] = new_bd
            rec.clear()
            rec.update(rebuilt)

        applied.append({
            "key": k,
            "player": rec["player"],
            "draft_year": rec.get("year"),
            "type": rec.get("type"),
            "old__by": old_by,
            "old__bd": old_bd,
            "new__by": new_by,
            "new__bd": new_bd,
            "source": source,
            "staged__by": staged_by,
            "staged__bd": staged_bd,
            "provenance": ov["provenance"] if ov else row["provenance"],
        })

    if len(applied) != EXPECTED_ROWS:
        halt("applied %d rows, expected %d" % (len(applied), EXPECTED_ROWS))

    out = json.dumps(data).encode()

    # --- post-write structural proof: nothing but the intended fields moved ---
    before = json.loads(raw_before)
    after = json.loads(out)
    if len(before) != len(after):
        halt("record count changed %d -> %d" % (len(before), len(after)))
    target = {r["key"] for r in applied}
    for b, a in zip(before, after):
        if b.get("key") != a.get("key"):
            halt("record order changed at key %r" % b.get("key"))
        if b.get("key") in target:
            bb = {k: v for k, v in b.items() if k not in ("_by", "_bd")}
            aa = {k: v for k, v in a.items() if k not in ("_by", "_bd")}
            if bb != aa:
                halt("a field other than _by/_bd moved on key %r" % b.get("key"))
        elif b != a:
            halt("a record outside the 302 changed: key %r" % b.get("key"))

    open(store_path, "wb").write(out)
    md5_after = hashlib.md5(out).hexdigest()
    print("store md5 after  : %s" % md5_after)
    print("rows written     : %d" % len(applied))

    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "applied_302.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(applied[0].keys()))
        w.writeheader()
        for a in applied:
            w.writerow(a)
    with open(os.path.join(out_dir, "md5_before_after.txt"), "w") as fh:
        fh.write("artifact: %s\n" % STORE_REL)
        fh.write("md5 before: %s\n" % md5_before)
        fh.write("md5 after : %s\n" % md5_after)
        fh.write("rows written: %d\n" % len(applied))
    with open(os.path.join(out_dir, "owner_overrides.json"), "w") as fh:
        json.dump([a for a in applied if a["source"].startswith("OWNER")], fh, indent=2)
        fh.write("\n")
    print("evidence written to %s" % out_dir)


if __name__ == "__main__":
    main()
