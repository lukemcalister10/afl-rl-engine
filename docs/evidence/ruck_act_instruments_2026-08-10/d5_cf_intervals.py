"""Counterfactual delivery ratios + the era split of the ceiling bite, with bootstrap CIs."""
import json, numpy as np
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
s6 = json.load(open(SP + "s6_rows.json"))
CF = {(r['key'], r['Y']): r for r in json.load(open(SP + "ruck_cf2_branch.json"))}
B = 20000; RNG = np.random.default_rng(20260810)
def kish(w):
    w = np.asarray(w, float); s = w.sum()
    return float(s * s / (w * w).sum()) if s > 0 else 0.0
def boot_ratio(cell, num, den, key):
    g = defaultdict(lambda: [0.0, 0.0])
    for r in cell:
        g[key(r)][0] += num(r); g[key(r)][1] += den(r)
    gs = list(g.values()); gn = np.array([x[0] for x in gs]); gd = np.array([x[1] for x in gs])
    idx = RNG.integers(0, len(gs), size=(B, len(gs)))
    est = gn[idx].sum(axis=1) / gd[idx].sum(axis=1)
    return float(np.percentile(est, 2.5)), float(np.percentile(est, 97.5)), float((est < 1).mean())

ND = [r for r in s6 if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022]
cells = {
  "RUCK ND1-64 N=1 (11)":      [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK'],
  "RUCK ND1-64 N=1..3 (61)":   [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK'],
  "RUCK ND1-64 ALL N (379)":   [r for r in ND if r['pos'] == 'RUCK'],
}
print("=" * 132)
print("F1 = sum(F)/sum(price) UNDER THE COUNTERFACTUALS.  If the ceiling and the pole denial were the")
print("whole story the counterfactual F1 would fall to the leg's 1.136.  It does not.")
print("=" * 132)
print("%-26s %6s %9s %9s %9s %9s   %-22s" % ("cell", "rows", "F1 ship", "F1 ceilOFF", "F1 poleON", "F1 both", "95% CI on F1(both), player"))
for nm, c in cells.items():
    c = [r for r in c if (r['key'], r['Y']) in CF]
    sf = sum(r['F'] for r in c)
    p = lambda f: sum(CF[(r['key'], r['Y'])][f] for r in c)
    lo, hi, pb = boot_ratio(c, lambda r: r['F'], lambda r: CF[(r['key'], r['Y'])]['price_AC'], lambda r: r['key'])
    print("%-26s %6d %9.4f %9.4f %9.4f %9.4f   [%6.3f, %6.3f]  P(<1)=%.3f"
          % (nm, len(c), sf / p('price'), sf / p('price_A'), sf / p('price_C'), sf / p('price_AC'), lo, hi, pb))
print()
print("=" * 132)
print("THE CEILING'S BITE BY ERA (ND 1-64 ruck rows; bite = price(ceiling off) - price)")
print("=" * 132)
ERAS = [("pre-2012 (C<=2011)", lambda C: C <= 2011), ("2012-2017", lambda C: 2012 <= C <= 2017),
        ("2018-2022", lambda C: C >= 2018)]
for lab, f in ERAS:
    for tag, sel in (("N=1", lambda r: r['N'] == 1), ("N=1..3", lambda r: 1 <= r['N'] <= 3), ("ALL N", lambda r: True)):
        c = [r for r in ND if r['pos'] == 'RUCK' and f(r['C']) and sel(r) and (r['key'], r['Y']) in CF]
        if not c: continue
        P = sum(CF[(r['key'], r['Y'])]['price'] for r in c)
        A = sum(CF[(r['key'], r['Y'])]['price_A'] for r in c)
        C2 = sum(CF[(r['key'], r['Y'])]['price_C'] for r in c)
        nb = sum(1 for r in c if CF[(r['key'], r['Y'])]['price_A'] > CF[(r['key'], r['Y'])]['price'] + 0.5)
        print("  %-20s %-7s rows=%4d players=%3d  Sprice=%9.1f  bite=%8.1f (%5.2f%%)  n_cut=%2d  poleON=%+8.1f"
              % (lab, tag, len(c), len(set(r['key'] for r in c)), P, A - P, 100 * (A - P) / P, nb, C2 - P))
print()
print("=" * 132)
print("PRICE-SIDE vs DELIVERY-SIDE: is the ruck year-1 under-pricing a PRICE defect or a DELIVERY fact?")
print("  ratio of the ruck cell's F1 to the leg's F1, shipped and under the counterfactuals")
print("=" * 132)
legs = {"N=1": [r for r in ND if r['N'] == 1], "N=1..3": [r for r in ND if 1 <= r['N'] <= 3]}
for tag, lc in legs.items():
    lf = sum(r['F'] for r in lc) / sum(r['price'] for r in lc)
    rc = [r for r in lc if r['pos'] == 'RUCK' and (r['key'], r['Y']) in CF]
    sf = sum(r['F'] for r in rc)
    for f, nm in (('price', 'shipped'), ('price_A', 'ceilOFF'), ('price_AC', 'ceilOFF+pole')):
        d = sum(CF[(r['key'], r['Y'])][f] for r in rc)
        print("  leg %-7s F1=%.4f | RUCK %-13s F1=%.4f  ratio=%.3f" % (tag, lf, nm, sf / d, (sf / d) / lf))
