#!/usr/bin/env python3
"""L2 EVIDENCE (one arm, correct method) — the dial is patched in rl_model.py BEFORE import (driver
does the sed), so SCALE re-anchors to the 99th pct at the new rate (the sweep's method). This script
just execs the engine at whatever LENS is on disk, optionally applies L1(b) _PVC0 adoption, and
reports emmett + anchors + the youth/old redistribution. argv[1]=out  argv[2]=base|adopt
"""
import json, io, os, sys, contextlib

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
SESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADOPT = len(sys.argv) > 2 and sys.argv[2] == "adopt"
smoothed = {int(k): int(v) for k, v in
            json.load(open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"))).items()}

_ens = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("_merged_recover.py").read().split('print("=== AFTER')[0], _ens)
ev = _ens["ev"]; MA = _ens["MA"]; players = MA.players; cp = _ens["cp"]
dial = MA.LENS["bal"]

if ADOPT:
    _ens["_PVC0"].clear(); _ens["_PVC0"].update(smoothed)
    _ens["_V0C"].clear(); _ens["_V0U"].clear(); _ens["_V0GUARD"].clear(); _ens["_RUCCEIL"].pop("grid", None)
    with contextlib.redirect_stdout(io.StringIO()):
        _ens["_build_v0_guard"](); _ens["_V0CURVE"].clear(); _ens["_build_v0_curve"]()
    MA._pe_clear()

with contextlib.redirect_stdout(io.StringIO()):
    val = {(p["key"] or p["player"]): ev(p, 2026) for p in players}
named = {k: val.get(k) for k in ["louis-emmett","max-gawn","kieren-briggs","marcus-bontempelli",
                                  "willem-duursma","dylan-patterson","kysaiah-pickett"]}
# youth vs old redistribution
def band(lo, hi):
    vs = [ev(p, 2026) for p in players if lo <= (cp._age_asof(p, 2026) or 99) <= hi]
    return round(sum(vs)/len(vs)) if vs else None
res = dict(dial=dial, adopt=ADOPT, named=named,
           mean_age_le21=band(0, 21), mean_age_30plus=band(30, 99), board_sum=sum(val.values()))
json.dump(res, open(sys.argv[1], "w"), indent=1)
print("dial=%.2f adopt=%s | emmett %s gawn %s bont %s | youth<=21 %s 30+ %s"
      % (dial, ADOPT, named["louis-emmett"], named["max-gawn"], named["marcus-bontempelli"],
         res["mean_age_le21"], res["mean_age_30plus"]))
