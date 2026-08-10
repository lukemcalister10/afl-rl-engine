"""Close the N=1 leg reconstruction: nseas_pro bar is games>=6 (_merged_recover.py:1127-1128)."""
import json
B = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB"
E = B + "/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026

S6 = json.load(open(E + "/stage6/s6_rows.json"))
s6y1 = {(x["key"], x["C"]) for x in S6 if x["N"] == 1}
s6nd = {(x["key"], x["C"]) for x in S6 if x["N"] == 1 and x["nd"] and 1 <= x["pk"] <= 64}


def load(p):
    d = json.load(open(p))
    return d["meta"], d["recs"]


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def g_in(r, y):
    for s in (r.get("seasons") or []):
        if s["year"] == y: return s["games"]
    return 0


for tag, path in (("stage4a1", E + "/stage4_amend1/noarb/per_entrant_338_stage4a1.json"),
                  ("stage5  ", E + "/stage5/noarb/per_entrant_338_stage5.json")):
    meta, recs = load(path)
    leg = []
    for r in recs:
        if not (r.get("type") == "ND" and not r.get("pickless")): continue
        pk = r.get("epk") or 0
        if not (1 <= pk <= 64): continue
        if not (2004 <= r["year"] <= 2022): continue
        if r["year"] + 4 > END: continue
        if g_in(r, r["year"] + 1) < 6: continue            # nseas_pro bar
        price = v(r, 1)
        if not price or price <= 0: continue
        y4 = v(r, 4)
        leg.append((r, y4 / DISC ** 3, price))
    n = len(leg); a = sum(x[1] for x in leg) / sum(x[2] for x in leg)
    print("%s  ND1-64 N=1 leg  n=%4d  F1=%.4f" % (tag, n, a))
    ks = {(x[0]["key"], x[0]["year"]) for x in leg}
    print("    set-vs-s6: mine-only=%d  s6-only=%d" % (len(ks - s6nd), len(s6nd - ks)))
    if ks - s6nd: print("      mine-only sample:", sorted(ks - s6nd)[:8])
    if s6nd - ks: print("      s6-only  sample:", sorted(s6nd - ks)[:8])
    for pz in ("MID", "SD", "SF", "KPF", "KPD", "RUCK"):
        sub = [x for x in leg if x[0]["pos"] == pz]
        if sub:
            print("      pos %-5s n=%4d  F1=%.4f" % (pz, len(sub), sum(x[1] for x in sub) / sum(x[2] for x in sub)))
