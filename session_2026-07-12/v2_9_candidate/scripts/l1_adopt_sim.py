#!/usr/bin/env python3
"""L1 option-(b) adoption EVIDENCE — faithful read-only reproduction of icbhpu sim_option_b.py's
in-memory recipe, but with (1) the L1b SMOOTHED derived curve and (2) the directive's pin=3000
(ev-channel-consistent), plus a 3157 (shipped-display) variant for the pin comparison.

READ-ONLY: swaps the frozen _PVC0 basis IN MEMORY and rebuilds the V0 guard / V0 curve / RUC ceiling
grid exactly as the sim does, re-evs the board, reports movers+anchors. Writes only JSON evidence.
It does NOT modify the engine on disk — the permanent lever is a separate, ladder-gated change.
argv[1]=out json   argv[2]=pin (3000|3157)
"""
import json, io, os, sys, contextlib

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
SESS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PIN = float(sys.argv[2]) if len(sys.argv) > 2 else 3000.0

smoothed = {int(k): int(v) for k, v in
            json.load(open(os.path.join(SESS, "out", "pvc_curve_smoothed.json"))).items()}
factor = PIN / 3000.0
new_curve = {k: int(round(smoothed[k]*factor)) for k in smoothed}

_ens = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("_merged_recover.py").read().split('print("=== AFTER')[0], _ens)
ev = _ens["ev"]; MA = _ens["MA"]; players = MA.players

def board_pass():
    with contextlib.redirect_stdout(io.StringIO()):
        return {(p["key"] or p["player"]): ev(p, 2026) for p in players}

base = board_pass()

# STAGE 1 — swap the ev-channel basis _PVC0 and rebuild the V0/RUC machinery (sim recipe, verbatim)
missing = [n for n in ("_PVC0","_V0C","_V0U","_V0GUARD","_RUCCEIL","_build_v0_guard","_V0CURVE","_build_v0_curve") if n not in _ens]
if missing:
    print("MISSING engine internals:", missing); raise SystemExit(1)
_ens["_PVC0"].clear(); _ens["_PVC0"].update(new_curve)
_ens["_V0C"].clear(); _ens["_V0U"].clear(); _ens["_V0GUARD"].clear()
_ens["_RUCCEIL"].pop("grid", None)
with contextlib.redirect_stdout(io.StringIO()):
    _ens["_build_v0_guard"]()
    _ens["_V0CURVE"].clear(); _ens["_build_v0_curve"]()
MA._pe_clear()
s1 = board_pass()

pl = {(p["key"] or p["player"]): p for p in players}
movers = []
for k, v0 in base.items():
    v1 = s1[k]
    if v1 != v0:
        p = pl[k]
        movers.append(dict(key=k, player=p["player"], pos=MA.gfut(p), type=p["type"],
                           effpk=MA.effpk(p), games=p["games"], before=v0, after=v1,
                           delta=v1-v0, delta_pct=round(100*(v1-v0)/v0, 1) if v0 else None))
movers.sort(key=lambda m: -abs(m["delta"]))
posmix = {}
for m in movers: posmix[m["pos"]] = posmix.get(m["pos"], 0) + 1
anchors = {}
for key in ["marcus-bontempelli","max-gawn","kieren-briggs","jeremy-cameron","sam-darcy",
            "zak-butters","max-holmes","louis-emmett"]:
    if key in base: anchors[key] = {"before": base[key], "after": s1[key], "same": base[key]==s1[key]}
tot0, tot1 = sum(base.values()), sum(s1.values())
res = dict(pin=PIN, parity_keys=len(base), movers_n=len(movers), mover_pos_mix=posmix,
           board_sum_before=tot0, board_sum_after=tot1,
           board_delta_pct=round(100*(tot1-tot0)/tot0, 3),
           anchors=anchors, top_movers=movers[:30])
json.dump(res, open(sys.argv[1], "w"), indent=1)
print("PIN %d | parity %d | movers %d %s | board %+.3f%% | anchors_all_same %s"
      % (PIN, len(base), len(movers), posmix,
         res["board_delta_pct"], all(a["same"] for a in anchors.values())))
print("anchors:", {k: (v["before"], v["after"]) for k, v in anchors.items()})
print("top 8 movers:", [(m["key"], m["before"], m["after"], m["delta_pct"]) for m in movers[:8]])
