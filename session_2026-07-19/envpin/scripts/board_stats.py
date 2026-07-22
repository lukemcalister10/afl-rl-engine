#!/usr/bin/env python3
# Board stats / keyed diff for rl_app_data.json (env-pin proofs).
#   board_stats.py <a.json>            -> md5, n, Sv, Sheezel, top-6 order
#   board_stats.py <a.json> <b.json>   -> keyed v-diff (row movers) + top-6 rank change
import sys, json, hashlib

def load(p):
    raw = open(p, "rb").read()
    d = json.loads(raw)
    rows = d["active"]
    return hashlib.md5(raw).hexdigest()[:8], rows

def key(p):
    return p.get("key") or p.get("id") or p.get("player") or p.get("name")

def stats(p):
    md5, rows = load(p)
    sv = sum(int(p["v"]) for p in rows)
    sh = next((int(r["v"]) for r in rows if "sheezel" in str(r.get("player", r.get("name",""))).lower()), None)
    top = sorted(rows, key=lambda r: -int(r["v"]))[:6]
    print(f"file      : {p}")
    print(f"md5       : {md5}")
    print(f"n / Sv    : {len(rows)} / {sv}")
    print(f"Sheezel v : {sh}")
    print(f"top-6     : " + " > ".join(f"{r.get('player',r.get('name'))}={r['v']}" for r in top))

def diff(a, b):
    _, ra = load(a); _, rb = load(b)
    ma = {key(r): int(r["v"]) for r in ra}
    mb = {key(r): int(r["v"]) for r in rb}
    movers = [(k, ma[k], mb[k]) for k in ma if k in mb and ma[k] != mb[k]]
    onlya = [k for k in ma if k not in mb]; onlyb = [k for k in mb if k not in ma]
    print(f"row v-movers (keyed): {len(movers)}")
    for k, x, y in movers[:20]:
        print(f"  {k}: {x} -> {y} ({y-x:+d})")
    if onlya or onlyb:
        print(f"  key mismatch: only-a={len(onlya)} only-b={len(onlyb)}")
    ta = [key(r) for r in sorted(ra, key=lambda r: -int(r["v"]))[:6]]
    tb = [key(r) for r in sorted(rb, key=lambda r: -int(r["v"]))[:6]]
    print(f"top-6 rank change: {'NONE' if ta==tb else 'RANK MOVED'}")
    if ta != tb:
        print(f"  a: {ta}")
        print(f"  b: {tb}")

if __name__ == "__main__":
    if len(sys.argv) == 2: stats(sys.argv[1])
    else: diff(sys.argv[1], sys.argv[2])
