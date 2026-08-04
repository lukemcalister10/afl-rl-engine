#!/usr/bin/env python3
"""L0 act 2b — dedupe the extracted lane rows into THE CANONICAL ROW LIST.

Acceptance 2's denominator is this list's own count.

THE DEDUP RULE, stated so it can be argued with:
  A canonical row is an (artifact-file, field) pair. Two lane rows merge ONLY when both
  the file AND the field match exactly. Everything else stays its own row.

Why not merge on file alone: `rl_model.py` hosts ~20 independent dials (SCALE, ALPHA,
GAMMA, MA.REPL, the EXP_* floors …), each with its own basis and its own disposition.
Merging them on the filename would collapse the work list into the file list and lose
every disposition — the opposite of what acceptance 2 counts. Same for the ui/data
bundles: `board_view_working.js` carries one RULED-CURRENT stamp, five
EXPECTED-TO-MOVE fields and one STALE-ROOTED F5 block, which cannot share a token.

Why the field must match too: lane B rows `pvc_curve_v2.json → curve` and
`… → pool_value` separately, and they carry different downstream sibling sets (the pool
triplet is three files; the curve payload is a different three). Lane B's prose counts
them as one ARTIFACT; this list counts WORK ITEMS, so they stay two rows linked to one
act. That is a deliberate divergence from lane B's "20 distinct artifacts" and is
recorded as such.

Grouping is by KEY, never by substring of a prose cell (hazard class 13), and the PATH
cell is resolved before prose so a docstring that merely mentions a file does not merge
with it (hazard class 1).
"""
import json, re, sys
from collections import OrderedDict

raw = json.load(open(sys.argv[1]))
rows = raw["rows"]

FILE_RE = re.compile(r"[A-Za-z0-9_./-]+\.(?:json|pkl|py|js|mjs|sh|md|csv|yml)")
# a field reference: lane B/C write "→ `field`" or "`file` → `field`"; lane A writes paths with :line
FIELD_RE = re.compile(r"(?:→|->)\s*`([^`]+)`")
LINE_RE = re.compile(r"\.(?:py|sh|js|mjs|yml|json):(\d+)")

DATA_EXT = (".json", ".pkl")


def file_of(r):
    """The file the row's artifact LIVES in — path cell first, prose only as fallback."""
    for cell in (r["path"], r["artifact"] + " " + r["path"]):
        files = FILE_RE.findall(cell)
        if files:
            # inside the chosen cell prefer a data artifact over a consuming module
            for f in files:
                if f.lower().endswith(DATA_EXT):
                    return f.split("/")[-1]
            return files[0].split("/")[-1]
    return None


def field_of(r):
    """The field/block within the file, when the lane names one."""
    m = FIELD_RE.search(r["path"]) or FIELD_RE.search(r["artifact"])
    if m:
        return m.group(1).strip().split(",")[0].strip("` ")
    m = LINE_RE.search(r["path"])
    if m:
        return "L" + m.group(1)          # a code site: the line IS the field
    return None


def key_of(r):
    f = file_of(r)
    if not f:
        return "sym::%s::%s" % (r["lane"], r["lane_id"])
    fld = field_of(r)
    if fld is None:
        # no discernible field: the row is its own item, keyed by lane row so it never
        # silently merges with a sibling field of the same file
        return "%s::%s#%s" % (f, r["lane"], r["lane_id"])
    return "%s::%s" % (f, fld)


groups = OrderedDict()
for r in rows:
    groups.setdefault(key_of(r), []).append(r)

canon = []
for i, (k, members) in enumerate(groups.items(), 1):
    lanes = sorted({m["lane"] for m in members})
    classes = OrderedDict()
    for m in members:
        for c in m["classes"]:
            classes.setdefault(c, []).append(m["canonical_id"])
    canon.append({
        "row": i,
        "key": k,
        "file": file_of(members[0]),
        "lanes": lanes,
        "lane_rows": [m["canonical_id"] for m in members],
        "classes": {c: ids for c, ids in classes.items()},
        "cross_lane": len(lanes) > 1,
        "conflict": len(classes) > 1,
        "artifact": members[0]["artifact"][:140],
    })

print(json.dumps({
    "lane_rows_in": len(rows),
    "canonical_rows": len(canon),
    "merged_away": len(rows) - len(canon),
    "cross_lane": sum(1 for c in canon if c["cross_lane"]),
    "classification_conflicts": sum(1 for c in canon if c["conflict"]),
    "rows": canon,
}, indent=1))
