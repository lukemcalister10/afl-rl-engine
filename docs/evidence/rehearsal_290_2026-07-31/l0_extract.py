#!/usr/bin/env python3
"""L0 act 2 — extract every inventory row from the three lane reports.

Reads the committed lane reports and emits one record per table row, lane-prefixed
(lane B and lane C both use A1/B1/C1-style ids, so bare ids collide across lanes).
No dedup here — extraction only, so the raw per-lane counts can be checked against
each report's own COUNTS block before anything is merged.
"""
import json, re, sys, pathlib

INV = pathlib.Path(sys.argv[1])
LANES = {"A": "A_engine_value_path.md", "B": "B_data_artifacts.md", "C": "C_ui_and_gates.md"}

# the classification tokens each lane uses, longest-first so STALE-ROOTED wins over its substring
TOKENS = ["STALE-ROOTED", "RULED-CURRENT", "HISTORICAL-SEALED", "EXPECTED-TO-MOVE-AT-ADOPTION",
          "NOT-LIVE", "UNCLEAR"]
SHORT = {"SR": "STALE-ROOTED", "RC": "RULED-CURRENT", "HS": "HISTORICAL-SEALED", "UN": "UNCLEAR"}


def split_row(line):
    """Split a markdown table row on unescaped pipes, ignoring pipes inside backticks."""
    cells, cur, tick = [], [], False
    for ch in line.strip().strip("|"):
        if ch == "`":
            tick = not tick
        if ch == "|" and not tick:
            cells.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    cells.append("".join(cur).strip())
    return cells


def classify(cell):
    """Return every classification token present in a class cell, in report order."""
    found = []
    up = cell.upper()
    for t in TOKENS:
        if t in up:
            found.append(t)
    if not found:
        # lane B uses two-letter shorthand in bold
        for s, full in SHORT.items():
            if re.search(r"\*\*%s\*\*|\b%s\b" % (s, s), cell):
                found.append(full)
    # STALE-ROOTED appears inside "STALE-ROOTED (residual)" etc; dedupe preserving order
    out = []
    for f in found:
        if f not in out:
            out.append(f)
    return out


rows = []
for lane, fn in LANES.items():
    text = (INV / fn).read_text()
    section = None
    for line in text.splitlines():
        m = re.match(r"^#{3,4}\s+(.*)$", line)
        if m:
            section = m.group(1).strip()
            continue
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) < 6:
            continue
        rid = cells[0]
        # a data row's first cell is an id: lane A "1".."62"; lanes B/C "A1","B7","E12"...
        if not re.fullmatch(r"\d{1,2}|[A-H]\d{1,2}", rid):
            continue
        # the class column is the second-from-last in every lane's table
        klass = classify(cells[-2])
        if not klass:
            continue
        rows.append({
            "lane": lane,
            "lane_id": rid,
            "canonical_id": "%s#%s" % (lane, rid),
            "section": section,
            "artifact": cells[1],
            "path": cells[2],
            "classes": klass,
            "evidence": cells[-1],
        })

# per-lane counts, to be checked against each report's own COUNTS block
summary = {}
for lane in LANES:
    lr = [r for r in rows if r["lane"] == lane]
    counts = {}
    for r in lr:
        for c in r["classes"]:
            counts[c] = counts.get(c, 0) + 1
    summary[lane] = {"rows": len(lr), "by_class": counts}

print(json.dumps({"summary": summary, "rows": rows}, indent=1))
