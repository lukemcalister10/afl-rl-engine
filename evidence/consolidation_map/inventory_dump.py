#!/usr/bin/env python3
"""
CONSOLIDATION STEP 1 — Tasks 2/3/4 raw inventory dumper (READ-ONLY).

Reproduces the machine-checkable facts behind the data-location, feature/credit and
position-field inventories: checksums, store field counts, categorical distributions,
credit magnitudes (PICKEQ/MECH), and the collapse map for positions.

Re-runnable:  python3 evidence/consolidation_map/inventory_dump.py
DATA_SOURCE for player figures = engine/rl_after/rl_model_data.json
DATA_SOURCE for board figures  = data/rl_build/rl_app_data.json
"""
import json, os, hashlib, collections, subprocess

ROOT  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STORE = os.path.join(ROOT, "engine/rl_after/rl_model_data.json")
BOARD = os.path.join(ROOT, "data/rl_build/rl_app_data.json")

def md5_8(p): return hashlib.md5(open(p, "rb").read()).hexdigest()[:8]

def line(c="-"): print(c * 66)

def main():
    line("=")
    print("STEP 0 — GROUND TRUTH")
    line("=")
    sha = subprocess.check_output(["git", "-C", ROOT, "rev-parse", "--short", "HEAD"]).decode().strip()
    print(f"git HEAD short          = {sha}  (expect 389ac39)")
    print(f"store md5(8)            = {md5_8(STORE)}  (expect 644d1254)  [rl_model_data.json = pre_stage0]")
    print(f"board md5(8)            = {md5_8(BOARD)}  [data/rl_build/rl_app_data.json = the app board]")
    print(f"baked matrix (filename) = data/s4_matrix_baked_c47cb43d.json  [engine md5 c47cb43d]")
    print(f"store byte-size        = {os.path.getsize(STORE):,}")

    d = json.load(open(STORE, encoding="utf-8"))
    print(f"store records          = {len(d)}")

    line("=")
    print("TASK 3/4 — STORE FIELD PRESENCE (source flags)")
    line("=")
    keys = collections.Counter(k for r in d for k in r)
    for k, c in keys.most_common():
        print(f"  {k:15s} present in {c:5d} / {len(d)}")

    line("=")
    print("TASK 3 — CREDIT / SPECIAL-CASE RECORDS (the confusing candidates)")
    line("=")
    for r in d:
        if r.get("_phantom") or r.get("_double_count") or r.get("_pvc_exclude"):
            flags = [f for f in ("_phantom", "_double_count", "_pvc_exclude") if r.get(f)]
            print(f"  {r['player']:34s} key={r['key']:26s} type={r.get('type'):4s} {'+'.join(flags)}")

    line("=")
    print("TASK 3 — CATEGORICAL DISTRIBUTIONS (draft type / category / channel)")
    line("=")
    for key in ("type", "_cat", "_draft"):
        c = collections.Counter(r.get(key) for r in d)
        print(f"  [{key}]")
        for v, n in c.most_common():
            print(f"      {str(v):32s} {n}")

    line("=")
    print("TASK 3 — CREDIT MAGNITUDES ON THE BOARD (PICKEQ / MECH)")
    line("=")
    b = json.load(open(BOARD, encoding="utf-8"))
    print("  PICKEQ (pathway -> pedigree pick-equivalent applied as _eff):")
    for k, v in sorted(b.get("PICKEQ", {}).items(), key=lambda x: x[1]):
        print(f"      {k:5s} -> pick_equiv {v}")
    print("  MECH pathway pools:")
    for m in b.get("MECH", []):
        print(f"      {m['name']:22s} n={m['n']:3d} played={m['played_n']:3d} "
              f"hit={m['hit_rate']:5}% pooled={m['pooled_value']:>3} pick_equiv={m['pick_equiv']}")
    ty = collections.Counter(r.get("ty") for r in b["active"])
    print("  active board (805) by draft type:", dict(ty))

    line("=")
    print("TASK 4 — POSITION FIELDS & COLLAPSE MAP")
    line("=")
    print("  SOURCE (rl_model_data.json):")
    print("    pos       drafted position   7 codes:", dict(collections.Counter(r["pos"] for r in d)))
    print("    _pos_now  present override  set in", sum(1 for r in d if r.get("_pos_now") is not None), "records")
    print("    _fut      raw multi-pos     set in", sum(1 for r in d if r.get("_fut")), "records")
    print("  ENGINE map GRP (rl_model.py:31): "
          "MID->MID RUC->RUC GFWD->GEN_FWD KFWD->KEY_FWD GDEF->GEN_DEF DEF->GEN_DEF KDEF->KEY_DEF")
    print("  ENGINE derived:")
    print("    bnow(p)   = GRP(_pos_now or pos)   -> PRESENT valuation group  (own active value)")
    print("    gfut(p)   = GRP(max-weight _fut)   -> FUTURE settled group     (curve/peak/runway)")
    print("    futblend  = normalised _fut blend  -> years-1+ replacement mix")
    print("    pm_pos    = 'band|group' key       -> peak-multiplier curve (params/rl_passmark)")
    print("  BOARD app record (rl_app_data active): grp=bnow  gf=gfut  fut=futblend   (no raw pos/_pos_now)")
    print("  BOOK s4_matrix record: pos=GRP(pos)  cpos=gfut  sw=(pos!=gfut) switch flag  (xlsx book only)")
    print()
    print("  COLLAPSE TARGET: two fields ->")
    print("    present_position = _pos_now or pos   (source: 131 overrides; board grp/bnow)")
    print("    drafted_position = pos               (source; board grp uses present, book pos uses drafted)")

if __name__ == "__main__":
    main()
