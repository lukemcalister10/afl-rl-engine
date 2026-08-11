"""ANCHOR LOCK — final. Reconstruct every published F component from the matrix alone.
  F1 leg (ND 1-64, classes 2004-2022, evaluation year N=1, established = yr-1 games>=6):
      F1 = sum_i v_i(C+4)/1.0939^3  /  sum_i v_i(C+1)      target 1.136, n=414
      KPD 0.668 ; RUCK 1.696
  F0 (year-zero instrument): F0 = sum v(C+4)/1.0939^4 / sum v0
      RD age>=21 3.242 ; pool KPF age>=21 0.556 ; pool age 21-22 2.149
READ-ONLY.
"""
import json
E = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def games_in(r, y):
    for s in (r.get("seasons") or []):
        if s["year"] == y: return s["games"]
    return 0


def ros(rows):
    return len(rows), (sum(a for a, b in rows) / sum(b for a, b in rows) if rows else float("nan"))


for tag, path in (("stage4a1 TEACHING", E + "/stage4_amend1/noarb/per_entrant_338_stage4a1.json"),
                  ("stage5   LANDED  ", E + "/stage5/noarb/per_entrant_338_stage5.json")):
    recs = json.load(open(path))["recs"]
    print("=" * 92)
    print(tag)
    leg = []
    for r in recs:
        if r.get("type") != "ND" or r.get("pickless"): continue
        pk = r.get("pick") or 0
        if not (1 <= pk <= 64): continue
        if not (2004 <= r["year"] <= 2022): continue
        if r["year"] + 4 > END: continue
        if games_in(r, r["year"] + 1) < 6: continue
        price = v(r, 1)
        if not price or price <= 0: continue
        leg.append((r, v(r, 4) / DISC ** 3, price))
    n, a = ros([(x[1], x[2]) for x in leg])
    print("  F1 ND 1-64 N=1 leg           n=%4d  F1=%.4f   [1.136 / n=414]" % (n, a))
    for pz in ("MID", "SD", "SF", "KPF", "KPD", "RUCK"):
        sub = [(x[1], x[2]) for x in leg if x[0]["pos"] == pz]
        if sub:
            n2, a2 = ros(sub)
            tgt = {"KPD": " [0.668]", "RUCK": " [1.696]"}.get(pz, "")
            print("     pos %-5s                  n=%4d  F1=%.4f%s" % (pz, n2, a2, tgt))

    def f0(pred):
        rows = []
        for r in recs:
            if not (2004 <= r["year"] <= 2025): continue
            if r["year"] + 4 > END: continue
            v0 = v(r, 0)
            if v0 is None or v0 <= 0: continue
            if not pred(r): continue
            rows.append((v(r, 4) / DISC ** 4, v0))
        return ros(rows)

    age = lambda r: r.get("age_draft")
    print("  F0 RD age>=21                n=%4d  F0=%.4f   [3.242]"
          % f0(lambda r: r["type"] == "RD" and (age(r) or 0) >= 21))
    print("  F0 pool KPF age>=21          n=%4d  F0=%.4f   [0.556]"
          % f0(lambda r: r["is_pool"] and r["pos"] == "KPF" and (age(r) or 0) >= 21))
    print("  F0 pool age 21-22            n=%4d  F0=%.4f   [2.149]"
          % f0(lambda r: r["is_pool"] and (age(r) or 0) in (21, 22)))
