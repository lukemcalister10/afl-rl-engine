#!/usr/bin/env python3
"""L2 EVIDENCE — the prior-cap-gone proof + the dial-14 effect (read-only).

The assert order (directive L2): PROVE the young-ruck prior-cap artifact is gone via L1(b) BEFORE
moving the dial. The ruling pack's D5 says louis-emmett shows -20/-22% at rates <=13% "via the cap —
artifact, not football; option (b) removes the mechanism". This measures emmett (+ anchors + the
young-RUC pocket) across dials 0.15/0.14/0.13/0.12, in TWO worlds:
  (A) base _PVC0 (frozen v3.4)         -> the artifact should appear at <=13%
  (B) L1(b) adopted _PVC0 (derived)    -> option (b); the artifact should be gone
Dial = LENS['bal'] (rl_model.py:301, d=LENS[lens], *21/((1+d)**k)). Read-only; writes only JSON.
argv[1]=out json
"""
import json, io, os, sys, contextlib

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
SESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
smoothed = {int(k): int(v) for k, v in
            json.load(open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"))).items()}  # pin 3000

_ens = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("_merged_recover.py").read().split('print("=== AFTER')[0], _ens)
ev = _ens["ev"]; MA = _ens["MA"]; players = MA.players
NAMES = ["louis-emmett","lachlan-mcandrew","marcus-bontempelli","max-gawn","kieren-briggs",
         "max-knobel","harry-barnett","toby-conway"]
keyrec = {}
for p in MA.data:
    if p.get("key") in NAMES and MA.GRP.get(p["pos"]): keyrec[p["key"]] = p

def measure():
    with contextlib.redirect_stdout(io.StringIO()):
        vals = {k: ev(p, 2026) for k, p in keyrec.items()}
        bsum = sum(ev(p, 2026) for p in players)
    return vals, bsum

def set_dial(d):
    MA.LENS["bal"] = d; MA._pe_clear()

DIALS = [0.15, 0.14, 0.13, 0.12]
res = {"world_A_base": {}, "world_B_L1adopt": {}}

# WORLD A — base _PVC0
for d in DIALS:
    set_dial(d); vals, bsum = measure()
    res["world_A_base"]["%.2f" % d] = {"emmett": vals["louis-emmett"], "bsum": bsum,
                                        "knobel": vals["max-knobel"], "gawn": vals["max-gawn"],
                                        "bont": vals["marcus-bontempelli"]}
# restore dial, then adopt L1(b): swap _PVC0 + rebuild V0/RUC machinery
set_dial(0.15)
_ens["_PVC0"].clear(); _ens["_PVC0"].update(smoothed)
_ens["_V0C"].clear(); _ens["_V0U"].clear(); _ens["_V0GUARD"].clear(); _ens["_RUCCEIL"].pop("grid", None)
with contextlib.redirect_stdout(io.StringIO()):
    _ens["_build_v0_guard"](); _ens["_V0CURVE"].clear(); _ens["_build_v0_curve"]()
MA._pe_clear()
# WORLD B — L1(b) adopted
for d in DIALS:
    set_dial(d); vals, bsum = measure()
    res["world_B_L1adopt"]["%.2f" % d] = {"emmett": vals["louis-emmett"], "bsum": bsum,
                                           "knobel": vals["max-knobel"], "gawn": vals["max-gawn"],
                                           "bont": vals["marcus-bontempelli"]}
json.dump(res, open(sys.argv[1], "w"), indent=1)

def cap_artifact(world):
    e15 = world["0.15"]["emmett"]
    return {d: {"emmett": world[d]["emmett"],
                "vs15_pct": round(100*(world[d]["emmett"]-e15)/e15, 1)} for d in ["0.15","0.14","0.13","0.12"]}
print("WORLD A (base _PVC0)  emmett vs dial:", cap_artifact(res["world_A_base"]))
print("WORLD B (L1 adopted)  emmett vs dial:", cap_artifact(res["world_B_L1adopt"]))
