"""THE OWNER'S TABLE (issue #334 comment 5236508995) — one table, three rows, one column per age.

Each age cell = the RAW POINTS of that player's CURRENT live-board value attributable to the
projected season at that age.  Ages the player is already past are EMPTY.  Each row SUMS to the
current-value column; a check column proves the attribution is complete.

ATTRIBUTION BASIS, stated plainly.  The engine's forward integral (_proj_w4) is captured exactly,
term by term -- that gives the SHAPE of the per-age contribution and its raw point value.  The
board's CURRENT price is not always equal to that integral: value() takes
max(production, demonstrated floor, pedigree pedestal) and may gate by the establishment
probability P (rl_model.py:1160-1170).  Where the price exceeds the integral, the excess is
attributed across ages in the integral's own proportions -- the only assumption in the table, and it
is disclosed per player as the 'scale' factor in the reconciliation block below.  scale = 1.000
means the price IS the integral and the row is exact with no assumption at all.
READ-ONLY.
"""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
X = json.load(open(SP + "/r27_xsec.json"))
ORDER = ["willem-duursma", "zak-butters", "marcus-bontempelli"]
present = [k for k in ORDER if k in X]

per = {}
for key in present:
    d = X[key]; SC = float(d["SCALE"])
    tot = sum(r["pv"] for r in d["rows"])
    price = float(d["price"])
    scale = (price / (tot * SC)) if tot > 0 else 0.0
    cells = {}
    for r in d["rows"]:
        a = int(round(float(r["age"])))
        cells[a] = cells.get(a, 0.0) + float(r["pv"]) * SC * scale
    per[key] = dict(cells=cells, price=price, integral_points=tot * SC, scale=scale,
                    a_now=float(d["a_now"]), C=int(d["C"]), pos=d["pos"],
                    cy0=2026 - int(d["C"]),
                    rows=d["rows"], SC=SC,
                    prod_v=float(d["prod_v"]), pf=float(d["prod_floor"]) * SC,
                    unpl=float(d["unpl_eq"]), vfn=float(d["value_fn"]),
                    lvl=float(d["level_now"] or 0), pe=float(d["peak_est"]))

AGES = sorted({a for k in present for a in per[k]["cells"]})
print("=" * (26 + 9 * (len(AGES) + 2)))
print("THE OWNER'S TABLE — current live-board value attributed to the projected season at each age")
print("basis: origin/main @ ef7eff8 | store 0dd6b4a0 | currency: engine PLAYER board points, "
      "pick-1 = 3000")
print("empty cell = the player is already past that age; each row sums to its CURRENT column")
print("=" * (26 + 9 * (len(AGES) + 2)))
hdr = "  %-22s %9s |" % ("player", "CURRENT") + "".join("%8d" % a for a in AGES) + " |%10s%9s" % ("ROW SUM", "CHECK")
print(hdr)
print("  " + "-" * (len(hdr) - 2))
for key in present:
    p = per[key]
    line = "  %-22s %9.0f |" % (key, p["price"])
    for a in AGES:
        line += ("%8.0f" % p["cells"][a]) if a in p["cells"] else ("%8s" % "")
    s = sum(p["cells"].values())
    line += " |%10.0f%9.2f" % (s, s - p["price"])
    print(line)
print()
print("  CHECK column = row sum minus the current value; 0.00 means the attribution is complete.")

print()
print("=" * 100)
print("RECONCILIATION — how much of each price IS the forward integral (the table's only assumption)")
print("=" * 100)
print("  %-22s %9s %11s %8s | %9s %9s %9s" %
      ("player", "CURRENT", "integral", "scale", "prod_v", "floor", "pedigree"))
for key in present:
    p = per[key]
    print("  %-22s %9.0f %11.0f %8.4f | %9.0f %9.0f %9.0f" %
          (key, p["price"], p["integral_points"], p["scale"], p["prod_v"], p["pf"], p["unpl"]))
print("  scale 1.0000 => the row is the engine's integral exactly, no assumption.")
print("  scale != 1  => the price carries a floor/pedestal/gating component; the table spreads it")
print("                 across ages in the integral's own proportions.")

print()
print("=" * 118)
print("SUPPORTING DETAIL — the raw integral, term by term (level, certainty weight, discount)")
print("=" * 118)
for key in present:
    p = per[key]
    print()
    print("  %s  (draft %d, %s, age now %.1f, 2026 = career year %d; demonstrated level %.2f, "
          "projected peak %.2f)" % (key, p["C"], p["pos"], p["a_now"], p["cy0"], p["lvl"], p["pe"]))
    print("    %-3s %6s %7s %9s %9s %7s %8s %11s %8s" %
          ("k", "age", "carYr", "level", "base", "Wk", "disc", "pts(attr)", "share"))
    tot = sum(r["pv"] for r in p["rows"])
    for r in p["rows"]:
        cy = p["cy0"] + int(r["k"])
        print("    %-3d %6.1f %7d %9.2f %9.2f %7.3f %8.3f %11.0f %7.1f%%" %
              (int(r["k"]), float(r["age"]), cy, float(r["lev"]), float(r["base"]),
               float(r["Wk"]), float(r["disc"]),
               float(r["pv"]) * p["SC"] * p["scale"], 100 * float(r["pv"]) / tot))
    t7 = sum(r["pv"] for r in p["rows"] if p["cy0"] + int(r["k"]) > 7) / tot
    t11 = sum(r["pv"] for r in p["rows"] if p["cy0"] + int(r["k"]) > 11) / tot
    print("    TAIL beyond career year 7: %.1f%%   beyond career year 11: %.1f%%   "
          "(last priced age %.1f, %d seasons)"
          % (100 * t7, 100 * t11, float(p["rows"][-1]["age"]), len(p["rows"])))

json.dump({k: dict(cells=per[k]["cells"], price=per[k]["price"], scale=per[k]["scale"])
           for k in present}, open(SP + "/r30_owner_table.json", "w"), indent=1)
print()
print("wrote", SP + "/r30_owner_table.json")
