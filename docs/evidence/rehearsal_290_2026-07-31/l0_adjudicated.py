#!/usr/bin/env python3
"""L0 act 2c — THE ADJUDICATED CANONICAL ROW LIST.

Rehearsal finding: the dedup is NOT mechanizable. The three lanes use incompatible row
granularity (A = one dial per row; B = one file-block per row; C = one pin/field per row),
so a regex rule either collapses distinct dials that share a file (130 rows) or merges
nothing across lanes (207 rows). Both are wrong. The cross-lane duplicates are therefore
ADJUDICATED BY HAND below, from reading the rows, and the merge table is published so the
seam can argue with each call rather than audit a black box.

Denominator = 209 lane rows − the merges below.
"""
import json, sys
from collections import OrderedDict

raw = json.load(open(sys.argv[1]))
rows = {r["canonical_id"]: r for r in raw["rows"]}

# Each entry: canonical name -> the lane rows that are ONE work item.
# Every call is a judgement about whether two lanes are inventorying the same THING
# TO DO, not merely the same file.
MERGES = OrderedDict([
    ("pvc_curve_v2.json:curve",              ["A#1",  "B#A1"]),
    ("pvc_curve_L1b.json",                   ["A#4",  "B#A4"]),
    ("pvc_snapshot.json",                    ["A#10", "B#A6"]),
    ("pvc_fit_candidate.json",               ["A#11", "B#A5"]),
    ("rl_model_data.json (THE store)",       ["A#12", "B#B10"]),
    ("national_draft_last_pick.json",        ["A#13", "B#B6"]),
    ("rl_passmark.json",                     ["A#15", "B#B4"]),
    ("params.json",                          ["A#16", "B#B5"]),
    ("bust_prior_table.json",                ["A#24", "B#B2"]),
    ("ycred_table.json",                     ["A#41", "B#B1"]),
    ("lti_return_table.json",                ["A#42", "B#B3"]),
    ("season_state.json",                    ["A#44", "B#C11"]),
    ("sealed_entrant_structure.json:counts", ["A#47", "B#E3"]),
    ("collision_sentry.json",                ["A#62", "B#B9"]),
    ("release_pick_curve.json:curve_source_store_md5", ["B#A8", "C#B3"]),
    ("release_contract.json:pvc_provenance", ["B#C4", "C#F2"]),
    ("release_contract.json:identities",     ["B#C5", "C#F1"]),
    ("release_contract.json:held_checks.ceiling_pct (LIVE gate input)", ["B#C6", "C#F3"]),
    ("release_contract.json:f5_entrant_reconciliation", ["B#C7", "C#F5"]),
    ("release_contract.json:present_lens_baseline", ["B#C8", "C#F6"]),
    ("pick_redenomination.json:factor",      ["A#49", "B#A7", "C#E12"]),
])

# Deliberate NON-merges, recorded because they LOOK mergeable and are not.
NON_MERGES = [
    ("C#D6 vs B#C1", "extract_board_view.py's docstring MENTIONS rl_app_data.json; it is a "
                     "doc row in a different file. Hazard class 1 — right name, wrong file."),
    ("C#A9 vs release_pick_curve.json", "club_valuation.js's stamp CITES the contract path; "
                                        "the row is the bundle stamp, not the contract."),
    ("B#A2 pool_value vs B#A1 curve", "same file, different sibling set: the pool triplet is "
                                      "3 files, the curve payload a different 3. Two work items."),
    ("B#A3 gy0_offline vs B#A1", "fit-time diagnostics of the curve — HISTORICAL-SEALED "
                                 "measurements, not an input. Distinct disposition."),
    ("C#F4 vs C#F3", "F4 is the DATED declaration record (HS); F3 is the live ceiling the gate "
                     "READS (SR-executable). Different dispositions, so not one row."),
    ("B#E4 vs B#E3", "E3 is the consumed occupancy COUNTS; E4 the file's embedded price totals, "
                     "which are not consumed. Distinct."),
    ("B#C2 vs B#C1", ".srcmd5 is a separate file certifying the board; its store side is RC "
                     "while what it certifies is SR."),
]

merged_ids = {i for ids in MERGES.values() for i in ids}
missing = [i for i in merged_ids if i not in rows]
assert not missing, "merge table names rows that do not exist: %s" % missing

canon = []
for name, ids in MERGES.items():
    classes = OrderedDict()
    for i in ids:
        for c in rows[i]["classes"]:
            classes.setdefault(c, []).append(i)
    canon.append({"key": name, "lane_rows": ids, "merged": True,
                  "lanes": sorted({i.split("#")[0] for i in ids}),
                  "classes": classes, "conflict": len(classes) > 1})
for cid, r in rows.items():
    if cid not in merged_ids:
        canon.append({"key": "%s %s" % (cid, r["artifact"][:70]), "lane_rows": [cid],
                      "merged": False, "lanes": [r["lane"]],
                      "classes": {c: [cid] for c in r["classes"]},
                      "conflict": len(r["classes"]) > 1})

for n, c in enumerate(canon, 1):
    c["row"] = n

out = {
    "lane_rows_in": len(rows),
    "merge_sets": len(MERGES),
    "rows_merged_away": len(merged_ids) - len(MERGES),
    "CANONICAL_ROWS": len(canon),
    "cross_lane_merges": sum(1 for c in canon if c["merged"] and len(c["lanes"]) > 1),
    "conflicts_to_resolve": [c["key"] for c in canon if c["conflict"]],
    "deliberate_non_merges": NON_MERGES,
    "rows": canon,
}
print(json.dumps(out, indent=1))
