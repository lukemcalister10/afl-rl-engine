"""ALIGNMENT PROOF — the PROXY used by the tilt map is byte-identical to the object the published
F numbers discount.  One `v()` helper, used for both.  If this does not print PASS, nothing else
in the tilt map may be read.  READ-ONLY."""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
DISC = 1.0939; END = 2026


def v(r, n):                       # THE one helper (identical text in r10_tilt.py)
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


def ros(rows): return len(rows), sum(a for a, b in rows) / sum(b for a, b in rows)


ok = True
for tag, path, tgt in (("stage4a1 (teaching matrix)", E + "/stage4_amend1/noarb/per_entrant_338_stage4a1.json", None),
                       ("stage5   (tilt-map basis)", E + "/stage5/noarb/per_entrant_338_stage5.json", None)):
    recs = json.load(open(path))["recs"]
    leg = []
    for r in recs:
        if r.get("type") != "ND" or r.get("pickless"): continue
        if not (1 <= (r.get("pick") or 0) <= 64): continue
        if not (2004 <= r["year"] <= 2022): continue
        if r["year"] + 4 > END: continue
        if games_in(r, r["year"] + 1) < 6: continue
        price = v(r, 1)
        if not price or price <= 0: continue
        PROXY = v(r, 4)                        # <-- the identical call the tilt map makes
        leg.append((PROXY / DISC ** 3, price, r))
    n, F1 = ros([(a, b) for a, b, _ in leg])
    kpd = ros([(a, b) for a, b, r in leg if r["pos"] == "KPD"])
    ruck = ros([(a, b) for a, b, r in leg if r["pos"] == "RUCK"])
    p1 = abs(F1 - 1.136) < 5e-4 and n == 414
    p2 = abs(kpd[1] - 0.668) < 5e-4
    p3 = abs(ruck[1] - 1.696) < 5e-4
    ok = ok and p1 and p2 and p3
    print("%s  n=%d F1=%.4f [1.136] %s | KPD %.4f [0.668] %s | RUCK %.4f [1.696] %s"
          % (tag, n, F1, "OK" if p1 else "FAIL", kpd[1], "OK" if p2 else "FAIL",
             ruck[1], "OK" if p3 else "FAIL"))

    def f0(pred):
        rows = []
        for r in recs:
            if not (2004 <= r["year"] <= 2025) or r["year"] + 4 > END: continue
            v0 = v(r, 0)
            if not v0 or v0 <= 0 or not pred(r): continue
            rows.append((v(r, 4) / DISC ** 4, v0))     # <-- same PROXY object, year-0 instrument
        return ros(rows)
    age = lambda r: r.get("age_draft")
    a = f0(lambda r: r["type"] == "RD" and (age(r) or 0) >= 21)
    b = f0(lambda r: r["is_pool"] and r["pos"] == "KPF" and (age(r) or 0) >= 21)
    p4 = abs(a[1] - 3.242) < 6e-3; p5 = abs(b[1] - 0.556) < 5e-4
    ok = ok and p4 and p5
    print("      F0 RD-mature n=%d %.4f [3.242] %s | F0 mature KPF n=%d %.4f [0.556] %s"
          % (a[0], a[1], "OK" if p4 else "FAIL", b[0], b[1], "OK" if p5 else "FAIL"))

# and the same PROXY, read straight out of the tilt-map row file, for a spot player
D = json.load(open(SP + "/r10_rows.json"))
h = next(r for r in D["rows"] if r["key"] == "michael-hurley")
recs5 = {(r["key"], r["type"], r["year"]): r for r in
         json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]}
rec = recs5[("michael-hurley", "ND", 2008)]
same = abs(h["proxy"] - float(rec["vpath"][3])) < 1e-6 and rec["yrs"][3] == rec["year"] + 4
print("spot: michael-hurley tilt-map proxy=%.1f  vpath[3]=%s  yrs[3]=%s (=C+4=%d)  %s"
      % (h["proxy"], rec["vpath"][3], rec["yrs"][3], rec["year"] + 4, "OK" if same else "FAIL"))
ok = ok and same
print()
print("ALIGNMENT: %s" % ("PASS" if ok else "FAIL"))
