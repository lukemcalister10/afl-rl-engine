"""Characterise the tilt-map population from the stage5 matrix. READ-ONLY, no engine."""
import json
from collections import Counter
E = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/repoB/docs/evidence/act_334B_2026-08-07"
recs = json.load(open(E + "/stage5/noarb/per_entrant_338_stage5.json"))["recs"]
END = 2026


def nseas_data(r):   # seasons with >=1 game
    return sum(1 for s in (r.get("seasons") or []) if s["games"] >= 1)


def v(r, n):
    if r["year"] + n > END: return None
    if n == 0: return float(r["v0"])
    vp = r.get("vpath") or []
    if n - 1 >= len(vp): return 0.0
    x = vp[n - 1]
    return 0.0 if x is None else float(x)


reach4 = [r for r in recs if r["year"] + 4 <= END]
print("records total            :", len(recs))
print("reached career year 4    :", len(reach4))
done = [r for r in reach4 if r["retired_now"] or r["delisted"]]
live = [r for r in reach4 if not (r["retired_now"] or r["delisted"])]
print("  completed (retired/del):", len(done))
print("  live                   :", len(live))
live11 = [r for r in live if nseas_data(r) >= 11]
print("  live with >=11 seasons :", len(live11))
POP = done + live11
print("POPULATION (done + live11):", len(POP))
print()
print("by type   :", Counter(r["type"] for r in POP).most_common())
print("by pos    :", Counter(r["pos"] for r in POP).most_common())
print("class span:", min(r["year"] for r in POP), "-", max(r["year"] for r in POP))
print("class hist:", sorted(Counter(r["year"] for r in POP).items()))
print()
# proxy = vpath[3]
z = sum(1 for r in POP if not v(r, 3))
print("POP with year-4 price == 0 (career already over / no price):", z)
print("POP with year-4 price  > 0                                :", len(POP) - z)
print()
nd = [r for r in POP if r["type"] == "ND" and not r["pickless"] and 1 <= (r["pick"] or 0) <= 64]
print("ND 1-64 in POP:", len(nd), " with y4 price>0:", sum(1 for r in nd if v(r, 3)))
pool = [r for r in POP if r["is_pool"]]
print("pool   in POP:", len(pool), " with y4 price>0:", sum(1 for r in pool if v(r, 3)))
print("pool by type:", Counter(r["type"] for r in pool).most_common())
print()
ages = Counter(("None" if r.get("age_draft") is None else ("<=20" if r["age_draft"] <= 20 else "21+"))
               for r in POP)
print("draft-age bands:", ages.most_common())
print()
# live11 seasons profile + 2026 games (partial season concern)
g26 = [sum(s["games"] for s in (r.get("seasons") or []) if s["year"] == 2026) for r in live11]
print("live11: n=%d ; 2026 games mean=%.1f max=%d ; zero-2026=%d"
      % (len(live11), (sum(g26) / len(g26) if g26 else 0), (max(g26) if g26 else 0),
         sum(1 for x in g26 if x == 0)))
print("live11 by class:", sorted(Counter(r["year"] for r in live11).items()))
print("live11 seasons-of-data:", sorted(Counter(nseas_data(r) for r in live11).items()))
# what does a completed career look like -- any with last game == 2025/2026?
print()
lg = Counter(r.get("last_game_year") for r in done)
print("completed careers, last game year (top):", sorted([x for x in lg.items() if x[0] and x[0] >= 2020]))
