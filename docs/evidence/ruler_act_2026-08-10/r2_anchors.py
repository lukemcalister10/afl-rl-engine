"""ANCHOR REPRODUCTION — step 1 of the ruler tilt map.
Must reproduce, before any new number:
  leg F1 = 1.136 (n=414) ND 1-64 teaching leg, classes 2004-2022, N=1
  KPD F1 = 0.668 ; RUCK F1 = 1.696
  F0 RD-mature = 3.242 ; mature KPF = 0.556
READ-ONLY.
"""
import json, os
B = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB"
E = B + "/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939
END = 2026

S6 = json.load(open(E + "/stage6/s6_rows.json"))
print("== (a) direct check against the published stage-6 rows (s6_rows.json) ==")


def agg(rows, fk="F", pk="price"):
    sp = sum(x[pk] for x in rows); sf = sum(x[fk] for x in rows)
    return len(rows), (sf / sp if sp else float("nan"))


ND = [x for x in S6 if x["nd"] and 1 <= x["pk"] <= 64]
y1 = [x for x in ND if x["N"] == 1]
print("  ND 1-64 N=1 leg           n=%4d  F1=%.4f   [target 1.136 / n=414]" % agg(y1))
for pz in ("MID", "SD", "SF", "KPF", "KPD", "RUCK"):
    n, a = agg([x for x in y1 if x["pos"] == pz])
    print("    yr1 pos %-5s            n=%4d  F1=%.4f" % (pz, n, a))

print()
print("== (b) independent re-derivation from the walk-forward matrix alone ==")


def load(p):
    d = json.load(open(p))
    return d["meta"], {(r["key"], r["type"], r["year"]): r for r in d["recs"]}


def v(r, n):
    """engine as-of price at career year n; n=0 -> v0. None = not yet reached."""
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0          # career ended -> bust, 0, kept in denominator
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


def F_num(r, N):
    """discounted career-year-4 value, discounted back to evaluation year N."""
    y4 = v(r, 4)
    if y4 is None: return None
    return y4 / (DISC ** (4 - N))


for tag, path in (("stage4a1 (teaching)", E + "/stage4_amend1/noarb/per_entrant_338_stage4a1.json"),
                  ("stage5    (landed)  ", E + "/stage5/noarb/per_entrant_338_stage5.json")):
    meta, M = load(path)
    recs = list(M.values())
    # ---- F1 teaching leg: ND, teaches_curve, pick 1-64, classes 2004-2022, played year 1 ----
    leg = []
    for r in recs:
        if not (r.get("type") == "ND" and not r.get("pickless")): continue
        pk = r.get("epk") or 0
        if not (1 <= pk <= 64): continue
        if not (2004 <= r["year"] <= 2022): continue
        if r["year"] + 4 > END: continue
        if not r.get("played_yr1"): continue
        price = v(r, 1)
        if not price or price <= 0: continue
        f = F_num(r, 1)
        if f is None: continue
        leg.append((r, f, price))
    n = len(leg); a = sum(x[1] for x in leg) / sum(x[2] for x in leg)
    print("  %s  ND1-64 N=1  n=%4d  F1=%.4f" % (tag, n, a))
    for pz in ("MID", "SD", "SF", "KPF", "KPD", "RUCK"):
        sub = [x for x in leg if x[0]["pos"] == pz]
        if not sub: continue
        print("      pos %-5s  n=%4d  F1=%.4f"
              % (pz, len(sub), sum(x[1] for x in sub) / sum(x[2] for x in sub)))

    # ---- F0 instrument: v(C+4)/DISC^4 over v0 ----
    def f0cell(pred):
        rows = []
        for r in recs:
            if not (2004 <= r["year"] <= 2025): continue
            if r["year"] + 4 > END: continue
            v0 = v(r, 0)
            if v0 is None or v0 <= 0: continue
            if not pred(r): continue
            rows.append((r, F_num(r, 0), v0))
        if not rows: return 0, float("nan")
        return len(rows), sum(x[1] for x in rows) / sum(x[2] for x in rows)

    age = lambda r: r.get("age_draft")
    print("      F0 RD age>=21          n=%4d  F0=%.4f   [target 3.242]"
          % f0cell(lambda r: r["type"] == "RD" and (age(r) or 0) >= 21))
    print("      F0 KPF age>=21 (pool)  n=%4d  F0=%.4f   [target 0.556]"
          % f0cell(lambda r: r.get("is_pool") and r["pos"] == "KPF" and (age(r) or 0) >= 21))
    print("      F0 KPF age>=21 (all)   n=%4d  F0=%.4f"
          % f0cell(lambda r: r["pos"] == "KPF" and (age(r) or 0) >= 21))
    print("      F0 pool age 21-22      n=%4d  F0=%.4f   [target 2.149]"
          % f0cell(lambda r: r.get("is_pool") and (age(r) or 0) in (21, 22)))
    print()
