import json
E = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB/docs/evidence/act_334B_2026-08-07"
recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
for r in recs:
    if "hurley" in (r["key"] or ""):
        print(r["key"], r["type"], r["year"], "pick", r["pick"], "pos", r["pos"],
              "age", r.get("age_draft"), "retired", r["retired_now"], "delisted", r["delisted"])
        print("  v0=%s  vpath=%s" % (r["v0"], r["vpath"]))
        print("  yrs=%s" % r["yrs"])
        for s in (r.get("seasons") or []):
            print("     ", s)
        print("  cur=", r["cur"], " peak=", r["peak"], " games_total=", r["games_total"])
