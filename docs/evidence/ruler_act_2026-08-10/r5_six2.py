import json
E = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB/docs/evidence/act_334B_2026-08-07"
recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
S6 = json.load(open(E + "/stage6/s6_rows.json"))
want = {'alex-sexton', 'james-mcdonald', 'lachie-neale', 'orren-stephenson', 'tim-mohr', 'tory-dickson'}
for r in recs:
    if r["key"] in want and r["year"] == 2011:
        print("%-18s pick=%s pick_stored=%s raw=%s epk=%s pickless=%s is_pool=%s is_pool_eng=%s teaches=%s band=%s cat=%s" %
              (r["key"], r["pick"], r["pick_stored"], r["raw_pick"], r["epk"], r["pickless"],
               r["is_pool"], r["is_pool_engine"], r["teaches_curve"], r["band"], r["cat"]))
for x in S6:
    if x["key"] in want and x["N"] == 1:
        print("S6 %-18s C=%s pk=%s nd=%s is_pool=%s pos=%s price=%.1f F=%.1f" %
              (x["key"], x["C"], x["pk"], x["nd"], x["is_pool"], x["pos"], x["price"], x["F"]))
# how many matrix ND recs 2004-2022 have epk != pick
d = [r for r in recs if r["type"] == "ND" and not r.get("pickless") and 2004 <= r["year"] <= 2022
     and (r.get("epk") or 0) != (r.get("pick") or 0)]
print("\nND recs where epk != pick:", len(d))
print("  sample:", [(r["key"], r["pick"], r["epk"]) for r in d[:10]])
