#!/usr/bin/env python3
"""Dump {key: ev} for every board player + the acceptance anchors. Run per env (RL_PVCFIT 0/1) in a
FRESH process; diff the two dumps for L1 attribution + verification. argv[1] = output path."""
import io, contextlib, os, sys, json

WS = "/home/claude/rl_workspace/rl_after"
os.chdir(WS)
g = {}
src = open(os.path.join(WS, "_merged_recover.py")).read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g["MA"]; ev = g["ev"]
board = {}
for p in MA.data:
    if MA.GRP.get(p.get("pos")):
        k = p.get("key") or p.get("player")
        board[k] = ev(p)
anchors = {}
for key in ["marcus-bontempelli", "max-gawn", "kieren-briggs", "jeremy-cameron", "sam-darcy",
            "zak-butters", "max-holmes", "louis-emmett"]:
    for p in MA.data:
        if p.get("key") == key and MA.GRP.get(p.get("pos")):
            anchors[key] = ev(p); break
json.dump({"pvcfit": os.environ.get("RL_PVCFIT", "0"), "n": len(board),
           "board": board, "anchors": anchors},
          open(sys.argv[1], "w"))
print("dumped", len(board), "rows; RL_PVCFIT=", os.environ.get("RL_PVCFIT", "0"), "->", sys.argv[1])
