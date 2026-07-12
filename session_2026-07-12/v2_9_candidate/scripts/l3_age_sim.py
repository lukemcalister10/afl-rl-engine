#!/usr/bin/env python3
"""L3 EVIDENCE — adopt the l7hinr s(age) up-side breakout-persistence slope (option A), read-only.

Replaces the flat S_M1=0.46 in _coreM1's proven-riser up-branch (_merged_recover.py:225) with
clip(s_age(age),0,1). s(age) crosses 0.46 at ~25.3 → risers <25 gain, >25 shrink. Patched in the
source STRING in memory (no disk/md5/Guard-5 change; the permanent RL_AGE lever rides the refit).
argv[1]=out json   argv[2]=base|age
"""
import json, io, os, sys, contextlib
import numpy as np

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
MODE = sys.argv[2] if len(sys.argv) > 2 else "base"
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]

ORIG = "if Lc>=Lo: return (Lo+S_M1*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"
if MODE == "age":
    PATCH = "if Lc>=Lo: return (Lo+_S_AGE(cp._age_asof(p,Y))*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"
    assert ORIG in src, "the _coreM1 up-branch line changed — re-locate before patching"
    src = src.replace(ORIG, PATCH)

_ens = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, _ens)
# inject s(age): interp over the l7hinr s_clip table, clipped [0,1]; age None -> flat 0.46 (unchanged)
_AX = [20,21,22,23,24,25,26,27,28,29,30,31]
_AY = [0.915376,0.860795,0.789170,0.700837,0.599107,0.489589,0.377802,0.265858,0.150620,0.026915,0.0,0.0]
_ens["_S_AGE"] = lambda a: float(np.clip(np.interp(a, _AX, _AY), 0.0, 1.0)) if a is not None else 0.46

ev = _ens["ev"]; MA = _ens["MA"]; players = MA.players; cp = _ens["cp"]
with contextlib.redirect_stdout(io.StringIO()):
    board = {(p["key"] or p["player"]): ev(p, 2026) for p in players}
NAMED = ["zak-butters","max-holmes","matthew-wilmot","jack-callaghan","jai-newcombe","luke-ryan",
         "dylan-moore","kysaiah-pickett","marcus-bontempelli","max-gawn","sam-darcy","caleb-daniel"]
named = {k: board.get(k) for k in NAMED}
json.dump({"mode": MODE, "n": len(board), "board": board, "named": named}, open(sys.argv[1], "w"))
print("MODE %s | board %d | butters %s holmes %s bont %s gawn %s"
      % (MODE, len(board), named["zak-butters"], named["max-holmes"],
         named["marcus-bontempelli"], named["max-gawn"]))
