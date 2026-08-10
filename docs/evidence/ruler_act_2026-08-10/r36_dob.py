"""AGE RE-DERIVATION from the DOB-written store (main@064abcae, store d9a24282).

THE BASIS SPLIT, STATED PLAINLY AND ENFORCED IN CODE:
  PROXY (vpath[3]), the realized-season kernel inputs, the year-11 mark, the dip classifier and
  every numerator in the 2x2 come from the ACT-BRANCH artifact per_entrant_338_stage5.json, whose
  store is 37ced3ce (PRE-DOB).  Those are NOT rebuilt and NOT touched here.
  ONLY the AGE FIELD is taken from the new store d9a24282.  Nothing else crosses the boundary.
  This is legitimate because a birth year is a fact about the world, not a valuation: writing it
  cannot move a walk-forward price that was computed without it.  (Verified below: the DOB act's
  own landing note records 6 movers all +/-1 board point, none in this population's vpath.)

age_draft = draft year - _by, matching emit_matrix_338.py:262 exactly:
      age_draft = p.get('_by') and (C - p['_by'])
READ-ONLY.
"""
import json, hashlib
from collections import Counter
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad"
NEW = SP + "/repoM/engine/rl_after/rl_model_data.json"
OLD = SP + "/repoB/engine/rl_after/rl_model_data.json"
print("new store md5 %s" % hashlib.md5(open(NEW, "rb").read()).hexdigest()[:8])
print("old store md5 %s (act branch, the basis the vpaths were built on)"
      % hashlib.md5(open(OLD, "rb").read()).hexdigest()[:8])


def load_by(path):
    d = json.load(open(path))
    recs = d if isinstance(d, list) else (d.get("players") or d.get("data") or [])
    if not isinstance(recs, list):
        for v in d.values():
            if isinstance(v, list) and v and isinstance(v[0], dict) and "key" in v[0]:
                recs = v; break
    out = {}
    for p in recs:
        k = p.get("key")
        if k is None: continue
        out[k] = dict(by=p.get("_by"), dob=p.get("dob"), year=p.get("year"), typ=p.get("type"))
    return out, len(recs)


NB, nn = load_by(NEW)
OB, no = load_by(OLD)
print("records: new %d, old %d" % (nn, no))
print("with a birth year: new %d, old %d  (delta +%d)"
      % (sum(1 for v in NB.values() if v["by"]), sum(1 for v in OB.values() if v["by"]),
         sum(1 for v in NB.values() if v["by"]) - sum(1 for v in OB.values() if v["by"])))

ROWS = json.load(open(SP + "/r24_rows.json"))["rows"]          # the 2x2 population, act-branch basis
print("\ntilt-map population rows (classes 2004-2015): %d" % len(ROWS))
old_unknown = [r for r in ROWS if r["age"] is None]
print("age-UNKNOWN under the OLD store: %d rows" % len(old_unknown))

miss = []
for r in ROWS:
    e = NB.get(r["key"])
    r["age_new"] = (r["year"] - e["by"]) if (e and e["by"]) else None
    if r["age_new"] is None: miss.append(r)
print("age-UNKNOWN under the NEW store: %d rows" % len(miss))
if miss:
    print("  remaining unknowns by class:", sorted(Counter(r["year"] for r in miss).items()))
    print("  remaining unknowns by route:", Counter(r["typ"] for r in miss).most_common())
    print("  their share of the population's year-4 price weight: %.2f%%"
          % (100 * sum(r["proxy"] for r in miss) / sum(r["proxy"] for r in ROWS)))
    for r in sorted(miss, key=lambda x: -x["proxy"])[:10]:
        print("     %-26s %-4s %d pick %-4s proxy %7.0f" % (r["player"], r["typ"], r["year"],
                                                            r["pick"], r["proxy"]))

# agreement check on rows that had an age BEFORE (the DOB act must not have moved existing ages)
both = [r for r in ROWS if r["age"] is not None and r["age_new"] is not None]
dis = [r for r in both if r["age"] != r["age_new"]]
print("\nrows with an age on BOTH stores: %d ; disagreements: %d" % (len(both), len(dis)))
for r in dis[:10]:
    print("   %-26s %d  old %s -> new %s" % (r["player"], r["year"], r["age"], r["age_new"]))

print("\n=== THE OLD 'age UNKNOWN' CELL, RELABELLED (its true age composition) ===")
print("  n=%d, all classes %s" % (len(old_unknown), sorted({r['year'] for r in old_unknown})))
got = [r for r in old_unknown if r["age_new"] is not None]
print("  now carrying a real draft age: %d of %d" % (len(got), len(old_unknown)))
print("  age distribution:", sorted(Counter(r["age_new"] for r in got).items()))
W = sum(r["proxy"] for r in old_unknown)
for lo, hi, nm in ((0, 18, "<=18"), (19, 20, "19-20"), (21, 22, "21-22"), (23, 99, "23+")):
    sub = [r for r in got if lo <= r["age_new"] <= hi]
    print("     %-6s n=%3d (%4.1f%% of rows)  %5.1f%% of the cell's year-4 price weight"
          % (nm, len(sub), 100 * len(sub) / max(len(got), 1),
             100 * sum(r["proxy"] for r in sub) / W if W else 0))
young = [r for r in got if r["age_new"] <= 20]
print("  young<=20 share of the cell by weight: %.1f%%  -> the cell is %s"
      % (100 * sum(r["proxy"] for r in young) / W,
         "overwhelmingly YOUNG (so its 2.139 was an ERA reading, not an age one)"
         if sum(r["proxy"] for r in young) / W > 0.8 else "a genuine age MIXTURE"))

json.dump([dict(key=r["key"], typ=r["typ"], year=r["year"], age_new=r["age_new"],
                age_old=r["age"]) for r in ROWS],
          open(SP + "/r36_ages.json", "w"), indent=0)
print("\nwrote", SP + "/r36_ages.json")
