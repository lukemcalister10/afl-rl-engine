"""Supplementary cells: the stage-7 cut cells (sitter-conditioned) re-run on the F8 bar,
plus mature x route x age fine cuts named in the no-blanket law."""
import json, math
import numpy as np
from statistics import NormalDist
exec(open("/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/grid.py").read().split("rng = np.random.default_rng")[0])

rng = np.random.default_rng(20260810)
route = np.array([x["route"] for x in ROWS]); pos = np.array([x["pos"] for x in ROWS])
ageb = np.array([x["ageb"] for x in ROWS]); age = np.array([-1 if x["age"] is None else x["age"] for x in ROWS])
gy1 = np.array([x["gy1"] for x in ROWS]); raw = np.array([x["raw_route"] for x in ROWS])

SIT = gy1 == 0; QUIET = (gy1 >= 1) & (gy1 <= 5); EST = gy1 >= 6
mat = age >= 21

CELLS = [
    ("STAGE-7 CUT: sitters age23+",              SIT & (age >= 23)),
    ("STAGE-7 CUT: sitters IRE",                 SIT & (route == "IRE")),
    ("STAGE-7 CUT: sitters MSD",                 SIT & (route == "MSD")),
    ("STAGE-7 CUT: NAMED UNION (23+|IRE|MSD)",   SIT & ((age >= 23) | (route == "IRE") | (route == "MSD"))),
    ("STAGE-7 LIFT: quiet starters, all pool",   QUIET),
    ("STAGE-7 LIFT: quiet starters RD",          QUIET & (route == "RD")),
    ("pool sitters, ALL",                        SIT),
    ("pool sitters <=20",                        SIT & (age >= 0) & (age <= 20)),
    ("pool sitters 21-22",                       SIT & (age >= 21) & (age <= 22)),
    ("pool sitters 23+",                         SIT & (age >= 23)),
    ("pool established 6+, all",                 EST),
    ("pool established 6+, mature 21+",          EST & mat),
    ("pool established 6+, young <=20",          EST & (age >= 0) & (age <= 20)),
    ("mature 21+ x RD x sitters",                mat & (route == "RD") & SIT),
    ("mature 21+ x RD x played yr1",             mat & (route == "RD") & (gy1 > 0)),
    ("mature 21+ x RD x quiet",                  mat & (route == "RD") & QUIET),
    ("mature 21+ x RD x est",                    mat & (route == "RD") & EST),
    ("mature 21+ x non-RD",                      mat & (route != "RD")),
    ("mature 21-22 x RD",                        (age >= 21) & (age <= 22) & (route == "RD")),
    ("mature 23+ x RD",                          (age >= 23) & (route == "RD")),
    ("mature 21+ x RD x RUNNING",                mat & (route == "RD") & np.isin(pos, ["MID", "SD", "SF"])),
    ("mature 21+ x RD x TALL",                   mat & (route == "RD") & np.isin(pos, ["KPF", "KPD", "RUCK"])),
    ("IRE x sitters+quiet",                      (route == "IRE") & (gy1 <= 5)),
    ("UNR all",                                  route == "UNR"),
    ("UNR x RUCK",                               (route == "UNR") & (pos == "RUCK")),
    ("MSD all",                                  route == "MSD"),
    ("age-unknown RD rows",                      (route == "RD") & (age < 0)),
]

print("%-42s %5s %7s %8s %-20s %-20s %7s %8s %-20s %-20s" % (
    "cell", "n", "effn0", "F0", "F0 CI (player)", "F0 CI (class)", "effn1", "F1", "F1 CI (player)", "F1 CI (class)"))
for lbl, m in CELLS:
    c = cell(m, lbl, rng)
    if c is None:
        print("%-42s  EMPTY" % lbl); continue
    f = lambda x: "[%7.3f,%7.3f]" % tuple(x) if not any(math.isnan(v) for v in x) else "       nan          "
    tag = []
    for w in (0, 1):
        e = c["effn%d" % w]; ci = c["ci%d" % w]
        ok = (e >= 35) and not any(math.isnan(v) for v in ci) and (ci[0] > 1 or ci[1] < 1)
        tag.append("NAMED%d" % w if ok else ("thin" if e < 35 else "strad"))
    print("%-42s %5d %7.1f %8.3f %s %s %7.1f %8.3f %s %s  %s" % (
        lbl, c["n"], c["effn0"], c["f0"], f(c["ci0"]), f(c["kci0"]),
        c["effn1"], c["f1"], f(c["ci1"]), f(c["kci1"]), "/".join(tag)))
