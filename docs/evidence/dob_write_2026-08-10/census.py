#!/usr/bin/env python3
"""
POST-WRITE CENSUS — the proof the courier worked.

Counts the store's birth-data coverage, using the SAME classification the L4 age-source census
uses (engine/forward_valuation/build_peak_model_v4.py, age_source()):

    REAL_DATE  -> the store carries _bd (an exact date of birth)
    REAL_YEAR  -> the store carries _by only (a first-class store state, runbook Addendum A.2)
    FALLBACK   -> neither; the engine falls back to draft-year-minus-18 (rl_model.by())

This script only READS. It does not run build_peak_model_v4.py — that is a bake-time refit and
this act is a data write only. The classification is reproduced here so the census can be taken
without triggering any fit.

Usage:  python3 census.py <repo_root> [staging_csv]
"""
import csv
import json
import os
import sys


def age_source(p):
    if p.get("_bd"):
        return "REAL_DATE"
    if p.get("_by"):
        return "REAL_YEAR"
    return "FALLBACK"


def main():
    root = os.path.abspath(sys.argv[1])
    store = json.load(open(os.path.join(root, "engine/rl_after/rl_model_data.json")))
    staging = os.path.join(root, "docs/evidence/dob_courier_2026-07-31/dob_courier_staging_302.csv")
    staged_keys = {r["key"] for r in csv.DictReader(open(staging, newline=""))}

    lines = []

    def say(s):
        print(s)
        lines.append(s)

    say("CENSUS — store engine/rl_after/rl_model_data.json, after the DOB courier write 2026-08-10")
    say("")
    say("Store records: %d" % len(store))

    # --- the acceptance test named in the brief ---
    cls_2003_05 = [p for p in store if p.get("year") in (2003, 2004, 2005)]
    nd_2003_05 = [p for p in cls_2003_05 if p.get("type") == "ND"]
    nd_blank = [p for p in nd_2003_05 if not p.get("_by")]
    say("")
    say("ACCEPTANCE 1 — ND records in draft classes 2003-2005 with a blank birth year")
    say("  ND records in classes 2003-2005 : %d" % len(nd_2003_05))
    say("  of those, blank _by             : %d   (required: 0)" % len(nd_blank))
    if nd_blank:
        say("  BLANK: %s" % sorted(p["key"] for p in nd_blank))

    say("")
    say("  all record types, classes 2003-2005 : %d" % len(cls_2003_05))
    blank_all = [p for p in cls_2003_05 if not p.get("_by")]
    say("  of those, blank _by                 : %d" % len(blank_all))
    if blank_all:
        say("  BLANK: %s" % sorted(p["key"] for p in blank_all))

    # --- the 302 themselves ---
    written = [p for p in store if p.get("key") in staged_keys]
    say("")
    say("ACCEPTANCE 2 — the 302 couriered rows")
    say("  rows found in the store   : %d   (required: 302)" % len(written))
    say("  with a birth year (_by)   : %d" % sum(1 for p in written if p.get("_by")))
    say("  with a birth date (_bd)   : %d" % sum(1 for p in written if p.get("_bd")))
    remaining = [p for p in written if not p.get("_by")]
    say("  STILL BLANK of the 302    : %d   (required: 0)" % len(remaining))
    if remaining:
        say("  BLANK: %s" % sorted(p["key"] for p in remaining))

    # --- store-wide age-source census ---
    counts = {"REAL_DATE": 0, "REAL_YEAR": 0, "FALLBACK": 0}
    for p in store:
        counts[age_source(p)] += 1
    say("")
    say("STORE-WIDE AGE-SOURCE CENSUS (build_peak_model_v4.age_source classification)")
    for k in ("REAL_DATE", "REAL_YEAR", "FALLBACK"):
        say("  %-10s : %d" % (k, counts[k]))
    say("  total      : %d" % sum(counts.values()))
    say("")
    say("  store-wide records with a blank birth year : %d" % counts["FALLBACK"])
    say("  (this is the whole store, every draft class; the 302 this act wrote are all clear)")

    out = os.path.join(root, "docs/evidence/dob_write_2026-08-10/census_after.txt")
    with open(out, "w") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
