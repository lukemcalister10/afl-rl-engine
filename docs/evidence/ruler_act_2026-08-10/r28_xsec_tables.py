"""PER-PLAYER AGE-SHARE CROSS-SECTIONS — presentation. Reads r27_xsec.json. READ-ONLY.
Currency: engine PLAYER board points, pick-1 anchored at 3000 (live board, origin/main @ ef7eff8).
Career year of a projected season = (2026 - draft year) + k, k=0 being the 2026 season.
"""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
X = json.load(open(SP + "/r27_xsec.json"))
ORDER = ["willem-duursma", "zak-butters", "marcus-bontempelli"]

comb = {}
for key in ORDER:
    if key not in X: print("MISSING:", key); continue
    d = X[key]
    rows = d["rows"]; SC = float(d["SCALE"])
    tot = sum(r["pv"] for r in rows)
    C = int(d["C"]); cy0 = 2026 - C          # career year of the k=0 season
    print()
    print("=" * 118)
    print("%s  —  draft %s pick %s, %s, age now %s, career games %s"
          % (d.get("player", key).upper() if isinstance(d.get("player", key), str) else key,
             C, d["pick_no"], d["pos"], d["a_now"], d["games"]))
    print("  2026 is CAREER YEAR %d.  demonstrated level_now = %.2f | projected peak_est = %.2f | "
          "peak age = %s" % (cy0, float(d["level_now"] or 0), float(d["peak_est"]), d["extra"]["pa"]))
    print("  price composition (board points): ENGINE CURRENT PRICE = %s" % d["price"])
    print("     production integral val(prod) = %.0f | demonstrated floor = %.0f | "
          "pedigree-only unpl_eq = %.0f | value() = %.0f"
          % (d["prod_v"], d["prod_floor"] * SC, d["unpl_eq"], d["value_fn"]))
    print("     integral multipliers: key-pos x%.2f  runway %.3f  elite %.3f  ->  kicker x%.4f  "
          "(discount d=%.2f/yr)" % (d["extra"]["keymul"], d["extra"]["runway"], d["extra"]["elite"],
                                    d["extra"]["kick"], d["extra"]["d"]))
    print("-" * 118)
    print("  %-3s %5s %7s %9s %9s %7s %8s %11s %9s %9s" %
          ("k", "age", "carYr", "level", "base", "Wk", "disc", "PV(points)", "share", "cum share"))
    cum = 0.0
    for r in rows:
        cy = cy0 + r["k"]
        cum += r["pv"]
        print("  %-3d %5.1f %7d %9.2f %9.2f %7.3f %8.3f %11.1f %8.1f%% %8.1f%%" %
              (r["k"], r["age"], cy, r["lev"], r["base"], r["Wk"], r["disc"],
               r["pv"] * SC, 100 * r["pv"] / tot, 100 * cum / tot))
    print("  %-3s %5s %7s %9s %9s %7s %8s %11.1f %8s %8s" %
          ("", "", "", "", "", "", "TOTAL", tot * SC, "100.0%", ""))
    # cumulative-by-age and tail shares
    def share_by_age(A):
        return sum(r["pv"] for r in rows if r["age"] <= A) / tot
    def tail_after_caryr(N):
        return sum(r["pv"] for r in rows if (cy0 + r["k"]) > N) / tot
    comb[key] = dict(cy0=cy0, a_now=d["a_now"], pos=d["pos"], price=d["price"],
                     tot_points=tot * SC,
                     by23=share_by_age(23), by26=share_by_age(26), by29=share_by_age(29),
                     by32=share_by_age(32),
                     t7=tail_after_caryr(7), t11=tail_after_caryr(11),
                     nyears=len(rows), lastage=rows[-1]["age"])
    print("  cumulative share of the forward integral delivered by age: 23 %.1f%% | 26 %.1f%% | "
          "29 %.1f%% | 32 %.1f%%" % (100 * comb[key]["by23"], 100 * comb[key]["by26"],
                                     100 * comb[key]["by29"], 100 * comb[key]["by32"]))
    print("  TAIL SHARE beyond career year 7 : %.1f%%   beyond career year 11 : %.1f%%"
          % (100 * comb[key]["t7"], 100 * comb[key]["t11"]))
    print("  projected seasons priced: %d (runs to age %.1f, then the frac<0.42 / age>38 break fires)"
          % (len(rows), rows[-1]["age"]))

print()
print("=" * 118)
print("COMBINED COMPARABLE VIEW — share of each player's forward integral delivered by age")
print("=" * 118)
print("  %-22s %5s %6s %7s | %8s %8s %8s %8s | %9s %9s | %6s" %
      ("player", "age", "carYr", "seasons", "by 23", "by 26", "by 29", "by 32",
       "tail >cy7", "tail >cy11", "price"))
for key in ORDER:
    if key not in comb: continue
    c = comb[key]
    print("  %-22s %5.1f %6d %7d | %7.1f%% %7.1f%% %7.1f%% %7.1f%% | %8.1f%% %9.1f%% | %6s" %
          (key, c["a_now"], c["cy0"], c["nyears"], 100 * c["by23"], 100 * c["by26"],
           100 * c["by29"], 100 * c["by32"], 100 * c["t7"], 100 * c["t11"], c["price"]))
print()
print("  NOTE ON READING 'tail > career year N': for a player already past career year N, the whole")
print("  remaining integral is tail by definition (100%). The age columns are the comparable view.")
json.dump(comb, open(SP + "/r28_combined.json", "w"), indent=1)
print()
print("wrote", SP + "/r28_combined.json")
