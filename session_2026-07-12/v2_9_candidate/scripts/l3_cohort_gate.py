#!/usr/bin/env python3
"""L3 GATE — the walk-forward G-COHORT re-measure (CONSTRAINTS v1.7 G-COHORT).

Construction (owner-worded, BINDING): for each draft CLASS, SUM that class's players' values in
career year t (class-year SUM — NOT per-capita); average those sums across classes → one figure per
t; years 4,5,6 EACH must be ≤ 130% (hard; guide 120-125%) of the denominator = min(year-1, year-2).
Walk-forward, leak-free: value_asof(p,t) prices p at Yt=draft+t with scoring truncated ≤Yt (the
sanctioned _p3_cohort_v6 machinery; inactive→0). L3 (s(age)) applied via the same source patch as
l3_age_sim; base run for the delta. argv[1]=out json  argv[2]=base|age
"""
import io, contextlib, copy, os, sys, json
import numpy as np

WS = "/home/claude/rl_workspace/rl_after"; os.chdir(WS)
MODE = sys.argv[2] if len(sys.argv) > 2 else "base"
src = open("_merged_recover.py").read().split('print("=== AFTER')[0]
ORIG = "if Lc>=Lo: return (Lo+S_M1*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"
if MODE == "age":
    PATCH = "if Lc>=Lo: return (Lo+_S_AGE(cp._age_asof(p,Y))*(Lc-Lo)) if ((Lc-Lo)>=TOL_M1 and _radq(p,Y,Lo)) else Lo"
    assert ORIG in src
    src = src.replace(ORIG, PATCH)

g = {"__name__": "_mr_sim"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g["MA"]; cp = g["cp"]; ev = g["ev"]
_AX = [20,21,22,23,24,25,26,27,28,29,30,31]
_AY = [0.915376,0.860795,0.789170,0.700837,0.599107,0.489589,0.377802,0.265858,0.150620,0.026915,0.0,0.0]
g["_S_AGE"] = lambda a: float(np.clip(np.interp(a, _AX, _AY), 0.0, 1.0)) if a is not None else 0.46

def draft_year(p): return p.get("year")
def cum_games(p, Y): return sum(x.get("games", 0) for x in p["scoring"] if x["year"] <= Y)
def value_asof(p, t):
    D = draft_year(p); Yt = D + t; q = copy.deepcopy(p)
    q["scoring"] = [x for x in q["scoring"] if x["year"] <= Yt]; q["_pos_now"] = None; q["_fut"] = []
    MA.BASE_REF = MA.AGE_REF = Yt; MA._pe_clear()
    if cum_games(p, Yt) == 0 and t >= 3: return 0.0
    with contextlib.redirect_stdout(io.StringIO()): return float(ev(q, Yt))

# classes = ND-pick players by draft year; need t6 observed (draft+6 <= 2026) -> classes 2014..2020
CLASSES = list(range(2014, 2021))
by_class = {Y: [p for p in MA.data if p.get("type") == "ND" and p.get("pick") and draft_year(p) == Y]
            for Y in CLASSES}
# class-year SUMS, then average across classes (only classes with t observed <= 2026)
classyr_sum = {Y: {} for Y in CLASSES}
for Y in CLASSES:
    for t in range(1, 7):
        if Y + t <= 2026:
            classyr_sum[Y][t] = sum(value_asof(p, t) for p in by_class[Y])
avg = {}
for t in range(1, 7):
    sums = [classyr_sum[Y][t] for Y in CLASSES if t in classyr_sum[Y]]
    avg[t] = float(np.mean(sums))
denom = min(avg[1], avg[2])
ratios = {t: avg[t] / denom for t in (4, 5, 6)}
breach = {t: ratios[t] > 1.30 for t in (4, 5, 6)}
res = dict(mode=MODE, classes=CLASSES, class_sizes={Y: len(by_class[Y]) for Y in CLASSES},
           avg_by_t={t: round(avg[t], 1) for t in avg}, denom=round(denom, 1),
           denom_leg="year-1" if avg[1] <= avg[2] else "year-2",
           ratios={t: round(ratios[t], 4) for t in ratios},
           breach_130={t: breach[t] for t in breach}, any_breach=any(breach.values()))
json.dump(res, open(sys.argv[1], "w"), indent=1)
print("MODE %s | class sizes %s" % (MODE, res["class_sizes"]))
print("  avg class-sum by t:", res["avg_by_t"], "| denom=min(t1,t2)=%.0f (%s)" % (denom, res["denom_leg"]))
print("  ratios vs denom: t4=%.1f%% t5=%.1f%% t6=%.1f%% (hard 130%%; guide 120-125%%)"
      % (ratios[4]*100, ratios[5]*100, ratios[6]*100))
print("  GATE:", "BREACH" if res["any_breach"] else "PASS", res["breach_130"])
