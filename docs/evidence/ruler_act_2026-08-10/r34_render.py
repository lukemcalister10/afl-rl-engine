"""RENDER THE OWNER'S TABLE from the TRUE-weight capture. READ-ONLY.
Rows sum to the board price by construction; the CHECK column asserts it to 1e-6."""
import json
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
X = json.load(open(SP + "/r33_owner_true.json"))
ORDER = ["willem-duursma", "zak-butters", "marcus-bontempelli"]
present = [k for k in ORDER if k in X]
AGES = sorted({int(a) for k in present for a in X[k]["cells"]})

print("=" * (30 + 7 * (len(AGES) + 2)))
print("CURRENT LIVE-BOARD VALUE ATTRIBUTED TO THE PROJECTED SEASON AT EACH AGE — TRUE NODE WEIGHTS")
print("basis origin/main @ ef7eff8 | store 0dd6b4a0 | engine PLAYER board points, pick-1 = 3000")
print("weights WQ6 = [0.18 x5, 0.10] over the 6-level band (_merged_recover.py:94, :381-387)")
print("empty cell = the player is already past that age")
print("=" * (30 + 7 * (len(AGES) + 2)))
hdr = "  %-20s %8s |" % ("player", "CURRENT") + "".join("%7d" % a for a in AGES) + " |%9s%8s" % ("ROW SUM", "CHECK")
print(hdr); print("  " + "-" * (len(hdr) - 2))
ok = True
for k in present:
    d = X[k]; c = {int(a): v for a, v in d["cells"].items()}
    line = "  %-20s %8.0f |" % (k, d["price"])
    for a in AGES:
        line += ("%7.0f" % c[a]) if a in c else ("%7s" % "")
    s = sum(c.values()); chk = s - d["price"]
    ok = ok and abs(chk) < 1e-6
    line += " |%9.0f%8.5f" % (s, chk)
    print(line)
print()
print("  CHECK = row sum - current value.  All rows tie to 1e-6: %s" % ok)
assert ok, "ROW SUMS DO NOT TIE"

print()
print("=" * 100)
print("PER-NODE CARRIER, BAND, AND THE price6 -> board-price SCALE")
print("=" * 100)
print("  %-20s %9s %10s %7s  %-28s %s" % ("player", "CURRENT", "price6", "scale", "band (peak levels)", "carried by"))
for k in present:
    d = X[k]
    print("  %-20s %9.0f %10.2f %7.4f  %-28s %s"
          % (k, d["price"], d["price6"], d["scale"],
             " ".join("%.0f" % b for b in d["band"]), " ".join(x[0] for x in d["carried"])))
print("  carried-by letters are the six band nodes in order: i=integral, F=FLOOR")
print("  scale = board price / price6: the captaincy add-back, the LEG-B un-compress map and the")
print("          pedigree/iso layers that sit ABOVE the production value.  The table's SHAPE is the")
print("          true-weighted production mixture; its LEVEL is the board price.")

print()
print("=" * 100)
print("SHARE OF CURRENT VALUE BY AGE REACHED, AND TAIL SHARES")
print("=" * 100)
print("  %-20s %6s %7s | %8s %8s %8s %8s | %10s %11s"
      % ("player", "age", "carYr", "by 23", "by 26", "by 29", "by 32", "tail >cy7", "tail >cy11"))
for k in present:
    d = X[k]; c = {int(a): v for a, v in d["cells"].items()}
    tot = sum(c.values()); a0 = int(round(float(d["a_now"]))); cy0 = 2026 - int(d["C"])
    by = lambda A: 100 * sum(v for a, v in c.items() if a <= A) / tot
    tail = lambda N: 100 * sum(v for a, v in c.items() if (cy0 + (a - a0)) > N) / tot
    print("  %-20s %6.1f %7d | %7.1f%% %7.1f%% %7.1f%% %7.1f%% | %9.1f%% %10.1f%%"
          % (k, float(d["a_now"]), cy0, by(23), by(26), by(29), by(32), tail(7), tail(11)))
print("  ('tail > career year N' is 100%% for a player already past year N — the age columns are")
print("   the comparable view.)")
