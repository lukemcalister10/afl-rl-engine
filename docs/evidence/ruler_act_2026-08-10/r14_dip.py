"""WORKED DIP EXAMPLES + age-unknown composition + explicit pooling ladder. READ-ONLY."""
import json
from collections import Counter
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
D = json.load(open(SP + "/r10_rows.json"))
ROWS = [r for r in D["rows"] if 2004 <= r["year"] <= 2015]
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
MX = {(r["key"], r["type"], r["year"]): r for r in
      json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]}

el = lambda r: r["reached5"] and r["g3"] >= 1 and r["g5"] >= 1
dipA = lambda r: el(r) and r["sp4"] < 0.80 * min(r["sp3"], r["sp5"])
dipB = lambda r: el(r) and r["sp4"] < 0.80 * max(r["sp3"], r["sp5"])
dipG = lambda r: el(r) and r["g4"] < 0.60 * min(r["g3"], r["g5"])

print("=" * 112)
print("WORKED EXAMPLE 1 — MICHAEL HURLEY (the shape the owner named)")
print("=" * 112)
h = next(r for r in ROWS if r["key"] == "michael-hurley")
rec = MX[("michael-hurley", "ND", 2008)]
print("  ND 2008 pick %s, %s, draft age %s. Career year k = calendar 2008+k; year 4 = 2012."
      % (h["pick"], h["pos"], h["age"]))
print("  engine as-of price path (vpath), career years 1..%d:" % len(rec["vpath"]))
for i, (y, val) in enumerate(zip(rec["yrs"], rec["vpath"]), start=1):
    s = next((s for s in rec["seasons"] if s["year"] == y), None)
    mark = "  <== PROXY (career year 4)" if i == 4 else ""
    print("     yr%-2d  %d   price %6s   season %s%s"
          % (i, y, val, ("%2d games @ %5.1f  bar %-4s" % (s["games"], s["avg"], s["bar"])) if s else "NO ROW (0 games)", mark))
print("  season prices (engine kernel): yr3 %.1f  yr4 %.1f  yr5 %.1f" % (h["sp3"], h["sp4"], h["sp5"]))
print("  dip classification: DIP-A(strict)=%s  DIP-B(broad)=%s  DIP-G(games)=%s"
      % (dipA(h), dipB(h), dipG(h)))
print("  PROXY (year-4 price)      = %8.1f" % h["proxy"])
print("  REALIZED (yr4 on, @1.0939)= %8.1f   (no stub: career completed)" % h["realized"])
print("  TILT = %.4f  -> the year-4 price was %.2fx the value his own remaining career delivered"
      % (h["realized"] / h["proxy"], h["proxy"] / h["realized"]))
print("  READ: the price DID fall through the dip (yr1 5284 -> yr4 3041 -> yr5 2341) and DID recover")
print("        (4876 by yr9) -- so the year-4 number is a MARKED-DOWN one, and the question is whether")
print("        it was marked down enough. Compare against his own no-dip peers below.")
print("  NOTE: his 2016 row is ABSENT from the store (the season Essendon's list did not play).")
print("        Under the store's no-row convention that season is priced at 0 in REALIZED.")

print()
print("=" * 112)
print("WORKED EXAMPLES 2-4 — the heaviest-weighted DIP-A rows (largest year-4 price in the dip cell)")
print("=" * 112)
cands = sorted([r for r in ROWS if dipA(r)], key=lambda r: -r["proxy"])[:6]
for r in cands:
    print("  %-24s %-4s %d pick %-3s %-4s age %-4s  yr4=%d" %
          (r["player"], r["typ"], r["year"], r["pick"], r["pos"], r["age"], r["year"] + 4))
    print("     games/avg  yr3 %2d@%5.1f   yr4 %2d@%5.1f   yr5 %2d@%5.1f"
          % (r["g3"], r["a3"], r["g4"], r["a4"], r["g5"], r["a5"]))
    print("     season price yr3 %7.1f  yr4 %7.1f  yr5 %7.1f" % (r["sp3"], r["sp4"], r["sp5"]))
    print("     PROXY %8.1f   REALIZED %8.1f   TILT %.3f   (stub %.0f)"
          % (r["proxy"], r["realized"], r["realized"] / r["proxy"] if r["proxy"] else float("nan"), r["stub"]))

print()
print("=" * 112)
print("DIP CELL COMPOSITION")
print("=" * 112)
base = [r for r in ROWS if el(r)]
for nm, f in (("DIP-A", dipA), ("DIP-B", dipB), ("DIP-G", dipG)):
    sub = [r for r in base if f(r)]
    print("  %-6s n=%3d  pos=%s" % (nm, len(sub), Counter(r["pos"] for r in sub).most_common()))
print("  eligible base n=%d (of %d rows in the window); ineligible = career did not reach yr5 with both"
      " yr3 and yr5 played" % (len(base), len(ROWS)))
print("  overlap: DIP-A subset of DIP-B ?", all(dipB(r) for r in base if dipA(r)))
print("  DIP-G n=%d of which also DIP-A: %d" % (sum(1 for r in base if dipG(r)),
                                                sum(1 for r in base if dipG(r) and dipA(r))))

print()
print("=" * 112)
print("AGE-UNKNOWN COMPOSITION (207 rows, tilt 0.4674, eff-n 47.5) — why the mature cells are starved")
print("=" * 112)
au = [r for r in ROWS if r["age"] is None]
print("  n=%d  by route: %s" % (len(au), Counter(r["typ"] for r in au).most_common()))
print("  by class : %s" % sorted(Counter(r["year"] for r in au).items()))
print("  by pos   : %s" % Counter(r["pos"] for r in au).most_common())
print("  share of each class's rows with NO draft age:")
for y in range(2004, 2016):
    tot = [r for r in ROWS if r["year"] == y]
    n = sum(1 for r in tot if r["age"] is None)
    print("     %d  %3d/%3d = %4.0f%%" % (y, n, len(tot), 100 * n / len(tot)))

print()
print("=" * 112)
print("POOLING LADDER — every below-bar cell and the named cell it pools into")
print("=" * 112)
M = json.load(open(SP + "/r13_map.json"))
fails = []
for axis, cells in M["axes"].items():
    for nm, c in cells.items():
        if c and not c["named"]:
            fails.append((axis, nm, c["effn"], c["tilt"]))
for axis, nm, e, t in sorted(fails, key=lambda x: -x[2]):
    print("  %-38s eff-n %6.1f  tilt %7.4f   (axis: %s)" % (nm, e, t, axis.split(" - ")[0]))
