"""NODE-STABILITY TEST — is the per-age share of the forward integral well-defined?

THE PROBLEM THE CAPTURE REVEALED.  The shipped board does NOT price a player off one forward
integral.  For each player ev() evaluates the integral at SEVERAL peak-level nodes (a distribution
over outcomes), and the price is some positive combination of them.  The node WEIGHTS live in the
distribution layer and are not visible at the proj_from_peak boundary, so a single node must never
be presented as "the player's decomposition" -- the first cut of this script picked one and would
have been wrong.

THE RESOLUTION.  The price's per-age vector is that same positive combination of the nodes' per-age
vectors.  If every node's per-age SHARE vector is (near-)identical, then the price's per-age share
equals that common share FOR ANY weights -- the unknown weighting drops out.  This script tests
exactly that: it reports, per age, the min/max/spread of the share across all nodes.  If the spread
is small the age table is well-defined; if not, it is not, and the table must wait for the weights.
READ-ONLY.
"""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
X = json.load(open(SP + "/r27_xsec.json"))
ORDER = ["willem-duursma", "zak-butters", "marcus-bontempelli"]

SUM = {}
for key in ORDER:
    if key not in X: continue
    d = X[key]
    nodes = d["nodes"]
    print()
    print("=" * 112)
    print("%s — %d distribution nodes captured (lp ranges %.2f .. %.2f); peak_est point = %.4f"
          % (key, len(nodes), min(n["lp"] for n in nodes), max(n["lp"] for n in nodes),
             float(d["peak_est"])))
    print("=" * 112)
    ages = sorted({int(round(r["age"])) for n in nodes for r in n["rows"]})
    shares = {}
    for n in nodes:
        tot = sum(r["pv"] for r in n["rows"])
        if tot <= 0: continue
        s = {}
        for r in n["rows"]:
            a = int(round(r["age"])); s[a] = s.get(a, 0.0) + r["pv"] / tot
        for a in ages: shares.setdefault(a, []).append(s.get(a, 0.0))
    print("  %-5s %9s %9s %9s %9s   %s" % ("age", "min%", "max%", "mean%", "spread", "verdict"))
    worst = 0.0
    for a in ages:
        v = shares[a]
        lo, hi = min(v), max(v); mn = sum(v) / len(v)
        sp = hi - lo; worst = max(worst, sp)
        print("  %-5d %8.2f%% %8.2f%% %8.2f%% %8.2f pp   %s"
              % (a, 100 * lo, 100 * hi, 100 * mn, 100 * sp,
                 "stable" if sp < 0.02 else ("WIDE" if sp > 0.05 else "moderate")))
    print("  worst per-age spread across nodes: %.2f percentage points" % (100 * worst))
    print("  -> the age-share table is %s"
          % ("WELL-DEFINED regardless of the unknown node weights (max spread < 2pp)"
             if worst < 0.02 else
             "NOT well-defined without the node weights -- do not publish the age table"))
    # the equal-weight mean share, for reference only
    SUM[key] = dict(ages=ages, mean={a: sum(shares[a]) / len(shares[a]) for a in ages},
                    worst=worst, price=d["price"], nnodes=len(nodes),
                    C=int(d["C"]), a_now=float(d["a_now"]), pos=d["pos"],
                    prod_floor=float(d["prod_floor"]) * float(d["SCALE"]),
                    unpl=float(d["unpl_eq"]), vfn=float(d["value_fn"]))

print()
print("=" * 112)
print("SUMMARY")
print("=" * 112)
for key in ORDER:
    if key not in SUM: continue
    s = SUM[key]
    cy0 = 2026 - s["C"]
    t11 = sum(v for a, v in s["mean"].items() if (cy0 + (a - int(round(s["a_now"])))) > 11)
    t7 = sum(v for a, v in s["mean"].items() if (cy0 + (a - int(round(s["a_now"])))) > 7)
    print("  %-22s price %6s  age now %4.1f  career yr %2d  nodes %2d  worst spread %5.2fpp  "
          "tail>cy7 %5.1f%%  tail>cy11 %5.1f%%"
          % (key, s["price"], s["a_now"], cy0, s["nnodes"], 100 * s["worst"], 100 * t7, 100 * t11))
json.dump(SUM, open(SP + "/r31_nodes.json", "w"), indent=1, default=str)
print()
print("wrote", SP + "/r31_nodes.json")
