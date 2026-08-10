import json
E = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB/docs/evidence/act_334B_2026-08-07"
recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
S6 = json.load(open(E + "/stage6/s6_rows.json"))
s6keys = {x["key"] for x in S6}
want = ['alex-sexton', 'james-mcdonald', 'lachie-neale', 'orren-stephenson', 'tim-mohr', 'tory-dickson']
for r in recs:
    if r["key"] in want and r["year"] == 2011:
        s12 = [s for s in (r.get("seasons") or []) if s["year"] <= 2013]
        print("%-20s type=%-4s pos=%-5s epk=%-3s age=%s inS6anyyear=%s" %
              (r["key"], r["type"], r["pos"], r["epk"], r.get("age_draft"), r["key"] in s6keys))
        print("     seasons<=2013:", s12)
        print("     vpath[:4]=", (r.get("vpath") or [])[:4], " yrs[:4]=", (r.get("yrs") or [])[:4])
# what other 2011 ND records ARE in s6 at N=1
s6_2011 = sorted(x["key"] for x in S6 if x["C"] == 2011 and x["N"] == 1 and x["nd"])
print("\n2011 ND N=1 rows present in s6:", len(s6_2011))
print("2011 ND recs with yr1 games>=6:",
      len([r for r in recs if r["year"] == 2011 and r["type"] == "ND" and not r.get("pickless")
           and 1 <= (r.get("epk") or 0) <= 64
           and any(s["year"] == 2012 and s["games"] >= 6 for s in (r.get("seasons") or []))]))
# do these 6 appear in s6 at ANY N?
for w in want:
    ns = sorted(x["N"] for x in S6 if x["key"] == w)
    print("  %-20s s6 N-rows: %s" % (w, ns))
