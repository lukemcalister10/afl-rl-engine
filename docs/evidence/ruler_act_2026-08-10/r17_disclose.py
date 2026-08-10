"""REMAINING DISCLOSURES: incomplete season records (interior zero-gaps), stub flags on NAMED cells,
and the self-reference arithmetic.  READ-ONLY."""
import json
from collections import Counter
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
E = SP + "/repoB/docs/evidence/act_334B_2026-08-07"
D = json.load(open(SP + "/r10_rows.json"))
ROWS = [r for r in D["rows"] if 2004 <= r["year"] <= 2015]
MX = {(r["key"], r["type"], r["year"]): r for r in
      json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]}

print("=" * 110)
print("A. INTERIOR ZERO-SEASONS FROM CAREER YEAR 4 ONWARD  (store convention: no row = 0 games)")
print("=" * 110)
gaps = []
for r in ROWS:
    rec = MX[(r["key"], r["typ"], r["year"])]
    ys = sorted(s["year"] for s in (rec.get("seasons") or []) if s["games"] >= 1)
    if len(ys) < 2: continue
    miss = [y for y in range(max(ys[0], r["year"] + 4), ys[-1]) if y not in ys]
    if miss: gaps.append((r, miss))
print("rows with >=1 interior season carrying NO row at or after career year 4 : %d of %d"
      % (len(gaps), len(ROWS)))
print("  total such seasons: %d" % sum(len(m) for _, m in gaps))
print("  by calendar year of the gap:", sorted(Counter(y for _, m in gaps for y in m).items()))
w = sum(r["proxy"] for r, _ in gaps); W = sum(r["proxy"] for r in ROWS)
print("  those rows carry %.1f%% of the population's year-4 price weight" % (100 * w / W))
y2016 = [(r, m) for r, m in gaps if 2016 in m]
print("  the 2016 spike (%d rows) is the single-season league event of that year; those seasons are"
      % len(y2016))
print("  priced at 0 in REALIZED under the store's own no-row convention -- named, not adjusted.")
print("  worst 6 by weight:")
for r, m in sorted(gaps, key=lambda t: -t[0]["proxy"])[:6]:
    print("     %-24s %s %d  missing %s  proxy %7.0f  tilt %.3f"
          % (r["player"], r["typ"], r["year"], m, r["proxy"],
             r["realized"] / r["proxy"] if r["proxy"] else float("nan")))

print()
print("=" * 110)
print("B. TERMINAL-STUB FLAGS -- every cell in the map whose stub share exceeds 15%")
print("=" * 110)
M = json.load(open(SP + "/r13_map.json"))
hits = []
for axis, cells in M["axes"].items():
    for nm, c in (cells or {}).items():
        if c and c["stub"] > 0.15: hits.append((nm, c["stub"], c["effn"], c["named"], axis))
for nm, s, e, named, axis in sorted(hits, key=lambda t: -t[1]):
    print("  %-34s stub %5.1f%%  eff-n %6.1f  %s" %
          (nm, 100 * s, e, "NAMED  <== FLAG" if named else "below bar (not named)"))
if not hits: print("  none")
print()
print("  named cells with stub between 10%% and 15%%:")
for axis, cells in M["axes"].items():
    for nm, c in (cells or {}).items():
        if c and c["named"] and 0.10 < c["stub"] <= 0.15:
            print("     %-34s stub %5.1f%%  eff-n %6.1f" % (nm, 100 * c["stub"], c["effn"]))

print()
print("=" * 110)
print("C. LIVE-CAREER (11+) SUB-POPULATION -- what the stub actually is")
print("=" * 110)
lv = [r for r in ROWS if not r["done"]]
print("  n=%d live 11+ rows; sum proxy %.0f (%.1f%% of population weight)"
      % (len(lv), sum(r["proxy"] for r in lv), 100 * sum(r["proxy"] for r in lv) / W))
print("  sum observed realized %.0f ; sum stub %.0f ; stub share of the LIVE rows' realized = %.1f%%"
      % (sum(r["real4"] for r in lv), sum(r["stub"] for r in lv),
         100 * sum(r["stub"] for r in lv) / sum(r["real4"] + r["stub"] for r in lv)))
print("  live-rows-only tilt = %.4f  vs completed-rows-only tilt = %.4f"
      % (sum(r["real4"] + r["stub"] for r in lv) / sum(r["proxy"] for r in lv),
         sum(r["real4"] for r in ROWS if r["done"]) / sum(r["proxy"] for r in ROWS if r["done"])))
print("  seasons of data:", sorted(Counter(r["nseas"] for r in lv).items()))

print()
print("=" * 110)
print("D. SELF-REFERENCE ARITHMETIC -- how much of REALIZED is engine judgement vs engine arithmetic")
print("=" * 110)
tot = sum(r["real4"] + r["stub"] for r in ROWS)
print("  REALIZED total                    %10.0f" % tot)
print("    from OBSERVED seasons priced     %10.0f  (%.1f%%)" % (sum(r["real4"] for r in ROWS),
                                                                 100 * sum(r["real4"] for r in ROWS) / tot))
print("    from the ENGINE'S CURRENT PRICE  %10.0f  (%.1f%%)" % (sum(r["stub"] for r in ROWS),
                                                                 100 * sum(r["stub"] for r in ROWS) / tot))
print("  i.e. 95.1%% of REALIZED is the engine's season kernel applied to games and averages that")
print("  actually happened; 4.9%% is a second engine forward price (the live tail).")
