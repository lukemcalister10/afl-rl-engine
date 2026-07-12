#!/usr/bin/env python3
"""L4 EVIDENCE — read-only reproduction of the MSD-pool-exclusion refit on the CURRENT store
(b0c39d78), mirroring #63 msd_pool_ripple_pass.py. Patches the training-pool filter line in the
engine SOURCE STRING in memory (adds `or type=='MSD'` to the continue), re-execs, re-evs, reports
movers + emmett + trio/pool membership. Writes only JSON. argv[1]=out  argv[2]=base|msdexcl
"""
import json, io, os, sys, contextlib

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
MODE = sys.argv[2] if len(sys.argv) > 2 else "base"
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]

FILTER = "if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')): continue"
if MODE == "msdexcl":
    patched = "if cp.debutyr(p)>2021 or not (p.get('pick') or p.get('_ft')) or p.get('type')=='MSD': continue"
    assert FILTER in src, "pool filter line not found — engine changed"
    src = src.replace(FILTER, patched)

_ens = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, _ens)
ev = _ens["ev"]; MA = _ens["MA"]; players = MA.players; cp = _ens["cp"]

# trained-pool census (recompute the same filter to report membership by type)
pool = []
for p in MA.data:
    if not MA.GRP.get(p["pos"]): continue
    if cp.debutyr(p) > 2021 or not (p.get("pick") or p.get("_ft")): continue
    if MODE == "msdexcl" and p.get("type") == "MSD": continue
    pool.append(p)
by_type = {}
for p in pool: by_type[p.get("type")] = by_type.get(p.get("type"), 0) + 1

board = {(p["key"] or p["player"]): ev(p, 2026) for p in players}
named = {}
for key in ["louis-emmett","lachlan-mcandrew","flynn-perez","jai-newcombe",
            "marcus-bontempelli","max-gawn","kieren-briggs"]:
    for p in MA.data:
        if p.get("key") == key and MA.GRP.get(p["pos"]):
            named[key] = ev(p, 2026); break
json.dump({"mode": MODE, "n": len(board), "trained_pool_by_type": by_type,
           "board": board, "named": named}, open(sys.argv[1], "w"))
print("MODE %s | board %d | pool %s | emmett %s mcandrew %s bont %s gawn %s"
      % (MODE, len(board), by_type, named.get("louis-emmett"), named.get("lachlan-mcandrew"),
         named.get("marcus-bontempelli"), named.get("max-gawn")))
