import json
B = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB"
p = B + "/docs/evidence/act_334B_2026-08-07/stage5/noarb/per_entrant_338_stage5.json"
d = json.load(open(p))
print("top keys:", list(d.keys()))
print("META:")
print(json.dumps(d["meta"], indent=1)[:4000])
recs = d["recs"]
print("n recs:", len(recs))
print("rec keys:", list(recs[0].keys()))
for r in recs[:3]:
    print(json.dumps(r)[:900])
# distribution of vpath lengths
from collections import Counter
c = Counter(len(r.get("vpath") or []) for r in recs)
print("vpath len counts:", sorted(c.items()))
c2 = Counter(r.get("type") for r in recs)
print("types:", c2.most_common())
