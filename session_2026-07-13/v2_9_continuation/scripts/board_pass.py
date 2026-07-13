#!/usr/bin/env python3
"""Board pass on the CURRENT workspace engine (whatever is patched on disk). Prices every player at
2026 and records named anchors + full board (key->value). Mirrors the inherited sims' board_pass.
usage: board_pass.py <out.json> [label]
"""
import sys, io, os, contextlib, json

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
OUT = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else "board"

g = {"__name__": "_mr_board"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("_merged_recover.py").read().split('print("=== AFTER')[0], g)
ev = g["ev"]; MA = g["MA"]; players = MA.players

with contextlib.redirect_stdout(io.StringIO()):
    board = {(p.get("key") or p["player"]): ev(p, 2026) for p in players}

NAMED = ["louis-emmett", "lachlan-mcandrew", "flynn-perez", "mark-keane", "jai-newcombe",
         "marcus-bontempelli", "max-gawn", "kieren-briggs", "jeremy-cameron", "sam-darcy",
         "zak-butters", "max-holmes", "harley-reid", "nick-daicos", "knobel", "matt-knobel"]
named = {}
for key in NAMED:
    if key in board:
        named[key] = board[key]
# knobel by name fallback (validation target from L1)
for p in players:
    if "knobel" in p["player"].lower() and MA.GRP.get(p.get("pos")):
        named["knobel(%s)" % (p.get("key") or p["player"])] = board.get(p.get("key") or p["player"])

out = dict(label=LABEL, n=len(board), board_sum=sum(board.values()), named=named, board=board)
json.dump(out, open(OUT, "w"))
print("BOARD %s | n=%d sum=%d | emmett=%s bont=%s gawn=%s butters=%s"
      % (LABEL, len(board), out["board_sum"], named.get("louis-emmett"),
         named.get("marcus-bontempelli"), named.get("max-gawn"), named.get("zak-butters")))
