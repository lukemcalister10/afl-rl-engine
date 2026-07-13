#!/usr/bin/env python3
"""v2.9 export/display acceptance + EV-invariance proof.

Validates the wired board (default: data/rl_build/rl_app_data.json) against the certified 8a66b4ba
"before" EV reference. Exit 0 = all pass. The HARD ACCEPTANCE is (D): zero EV movers — every shipped
`v` / lens value is byte-identical before and after; only NEW fields differ.

usage: test_export_display.py [after_board.json]
"""
import json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
AFTER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "data", "rl_build", "rl_app_data.json")
REF = os.path.join(REPO, "session_2026-07-13", "v2_9_export_display", "out", "board_before_ev_8a66b4ba.json")

d = json.load(open(AFTER))
ref = json.load(open(REF))
fails = []


def check(name, cond, detail=""):
    print(("  PASS " if cond else "  FAIL ") + name + (("  — " + detail) if detail else ""))
    if not cond:
        fails.append(name)


active = d["active"]
back = d.get("back", [])
by_key = {r["key"]: r for r in active}
sum_v = sum(r["v"] for r in active)

print("== A. lti_reg consumer-wiring fix (barker/thredgold) ==")
for k in ("harley-barker", "blake-thredgold"):
    row = by_key.get(k, {})
    tag = row.get("lti_reg")
    check("%s lti_reg populated" % k, isinstance(tag, dict) and tag.get("section") in ("A", "B"),
          "lti_reg=%s v=%s" % (tag, row.get("v")))

print("== B. export fields present + typed ==")
missing_vp = [r["key"] for r in active if "vPrev" not in r]
missing_lev = [r["key"] for r in active if "levers" not in r]
check("every active row carries vPrev key", not missing_vp, "%d missing" % len(missing_vp))
check("every active row carries vRaw key", all("vRaw" in r for r in active))
check("every active row carries levers key", not missing_lev, "%d missing" % len(missing_lev))
# levers split closes: v - vPrev == sum(levers) for rows that have both
closed = bad = 0
for r in active:
    if r.get("vPrev") is not None and isinstance(r.get("levers"), dict):
        if r["v"] - r["vPrev"] == sum(r["levers"].values()):
            closed += 1
        else:
            bad += 1
check("per-lever split closes (v - vPrev == Σlevers)", bad == 0, "%d close, %d broken" % (closed, bad))
check("vRaw null where no owner override (0 today)", all(r.get("vRaw") is None for r in active if not r.get("ov")))

print("== C. phantom-pick lens entries (+1/+2 only) ==")
lp = d.get("lensPicks", [])
lenses = sorted({p["lens"] for p in lp})
check("lensPicks present", len(lp) > 0, "%d entries" % len(lp))
check("appear on +1/+2 ONLY (never current/-1/-2)", lenses == [1, 2], "lenses=%s" % lenses)
check("each lens carries the 30-pick class", sum(1 for p in lp if p["lens"] == 1) == 30 and
      sum(1 for p in lp if p["lens"] == 2) == 30)
check("phantom pick value == shipped PVC face value",
      all(p["v"] == d["PVC"][str(p["n"])] for p in lp), "PVC-scaled")
check("rolling labelYear (2027 on +1, 2028 on +2)",
      all(p["labelYear"] == 2026 + p["lens"] for p in lp))

print("== D. lens-conservation diagnostic (report-only) ==")
lc = d.get("lensConservation", {})
check("conservation covers -2..+2", all(k in lc for k in ("-2", "-1", "now", "+1", "+2")))
if lc:
    for k in ("-2", "-1", "now", "+1", "+2"):
        e = lc[k]
        print("     lens %-4s year %d | players=%d picks=%d total=%d (n=%d)"
              % (k, e["lensYear"], e["players"], e["picks"], e["total"], e["nPlayers"]))
    print("     spread vs now:", lc.get("_meta", {}).get("spread_vs_now"))

print("== E. HARD ACCEPTANCE — ZERO EV MOVERS vs certified 8a66b4ba ==")
check("n_active unchanged (804)", len(active) == ref["n_active"], "%d vs %d" % (len(active), ref["n_active"]))
check("sum_v unchanged (732725)", sum_v == ref["sum_v"], "%d vs %d" % (sum_v, ref["sum_v"]))
check("active key set unchanged", set(by_key) == set(ref["active"]),
      "sym-diff %d" % len(set(by_key) ^ set(ref["active"])))
movers = []
for k, before in ref["active"].items():
    r = by_key.get(k)
    if r is None:
        continue
    now = [r["v"], r.get("vM2"), r.get("vM1"), r.get("vP1"), r.get("vP2")]
    if now != before:
        movers.append((k, before, now))
check("ZERO EV movers on active (v + all lens years)", not movers,
      "%d movers, e.g. %s" % (len(movers), movers[:3]))
back_by = {r["key"]: [r["v"], r.get("vM2"), r.get("vM1"), r.get("vP1"), r.get("vP2")] for r in back}
back_movers = [k for k, b in ref["back"].items() if back_by.get(k) != b]
check("ZERO EV movers on back rows", not back_movers, "%d movers" % len(back_movers))

print("\nRESULT:", "PASS — all acceptance + zero-EV-mover proof GREEN" if not fails else "FAIL: " + ", ".join(fails))
sys.exit(1 if fails else 0)
