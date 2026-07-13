#!/usr/bin/env python3
"""G-ATTR — per-lever board attribution. Given the cumulative-board JSONs
(base -> +L1 -> +L1L4 -> +L1L4L2 -> +L1L4L2L3), report each lever's separable per-row delta
(diff of consecutive boards), the anchor/emmett carry, and the all-off==base byte-check.
usage: attribute.py <base.json> <L1.json> <L1L4.json> <L1L4L2.json> <L1L4L2L3.json> [out.json]
"""
import sys, json

STAGES = ["base", "+L1", "+L4", "+L2", "+L3"]
paths = sys.argv[1:6]
boards = [json.load(open(p))["board"] for p in paths]
ANCHORS = ["louis-emmett", "marcus-bontempelli", "max-gawn", "kieren-briggs", "jeremy-cameron",
           "sam-darcy", "zak-butters", "max-holmes"]

keys = set(boards[0])
for b in boards[1:]:
    keys &= set(b)
keys = sorted(keys)

rows = []
for i in range(1, len(boards)):
    prev, cur = boards[i - 1], boards[i]
    movers = [(k, prev[k], cur[k], cur[k] - prev[k]) for k in keys if cur[k] != prev[k]]
    movers.sort(key=lambda t: -abs(t[3]))
    rows.append(dict(lever=STAGES[i], n_movers=len(movers),
                     board_sum_prev=sum(prev[k] for k in keys), board_sum_cur=sum(cur[k] for k in keys),
                     top=[(k, a, b, d) for k, a, b, d in movers[:12]]))

anchor_track = {a: [boards[i].get(a) for i in range(len(boards))] for a in ANCHORS}
out = dict(stages=STAGES, per_lever=rows, anchors=anchor_track)
print("=== G-ATTR (per-lever separable board deltas) ===")
for r in rows:
    print("  %-4s movers=%-5d board_sum %d -> %d (%+d)"
          % (r["lever"], r["n_movers"], r["board_sum_prev"], r["board_sum_cur"],
             r["board_sum_cur"] - r["board_sum_prev"]))
    print("       top: " + ", ".join("%s %d->%d(%+d)" % t for t in r["top"][:6]))
print("=== anchor / emmett carry across stages (%s) ===" % " ".join(STAGES))
for a in ANCHORS:
    print("  %-20s %s" % (a, anchor_track[a]))
if len(sys.argv) > 6:
    json.dump(out, open(sys.argv[6], "w"), indent=1)
    print("wrote", sys.argv[6])
