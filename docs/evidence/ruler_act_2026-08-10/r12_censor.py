"""CENSORING DIAGNOSTIC — why the class window must close at 2015, shown as a number.
A class C can contribute a LIVE career only if it can reach 11 seasons by 2026: C+11 <= 2026 => C <= 2015.
For C >= 2016 the owner's population rule admits ONLY completed careers, i.e. only the failures.
READ-ONLY."""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json")); ROWS = D["rows"]
print("  %-6s %5s %5s %5s %8s %8s %8s   %s" %
      ("class", "n", "done", "live", "sumProxy", "sumReal", "TILT", "live-share of proxy"))
for y in range(2004, 2023):
    rs = [r for r in ROWS if r["year"] == y]
    if not rs: continue
    P = sum(r["proxy"] for r in rs); R = sum(r["realized"] for r in rs)
    lv = [r for r in rs if not r["done"]]
    lp = sum(r["proxy"] for r in lv)
    print("  %-6d %5d %5d %5d %8.0f %8.0f %8.4f   %5.1f%%" %
          (y, len(rs), sum(1 for r in rs if r["done"]), len(lv), P, R,
           (R / P if P else float('nan')), (100 * lp / P if P else 0)))
print()
for lo, hi, nm in ((2004, 2015, "PRIMARY  classes 2004-2015"), (2016, 2022, "CENSORED classes 2016-2022")):
    rs = [r for r in ROWS if lo <= r["year"] <= hi]
    P = sum(r["proxy"] for r in rs); R = sum(r["realized"] for r in rs)
    print("%s : n=%4d  done=%4d live=%3d  TILT=%.4f" %
          (nm, len(rs), sum(1 for r in rs if r["done"]), sum(1 for r in rs if not r["done"]),
           R / P if P else float('nan')))
