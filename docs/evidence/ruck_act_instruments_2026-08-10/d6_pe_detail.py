"""The per-entrant ruck cell in full: both bootstrap schemes, eff-n, era split, ceiling exposure."""
import json, numpy as np
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
PE = json.load(open(SP + "per_entrant_338_stage5.json"))
recs = PE['recs']; DISC = 1.0939
B = 20000; RNG = np.random.default_rng(20260810)
def kish(w):
    w = np.asarray(w, float); s = w.sum()
    return float(s * s / (w * w).sum()) if s > 0 else 0.0
def boot(cell, keyf, num, den):
    g = defaultdict(lambda: [0.0, 0.0])
    for r in cell:
        g[keyf(r)][0] += num(r); g[keyf(r)][1] += den(r)
    gs = list(g.values()); gn = np.array([x[0] for x in gs]); gd = np.array([x[1] for x in gs])
    idx = RNG.integers(0, len(gs), size=(B, len(gs)))
    est = gn[idx].sum(axis=1) / gd[idx].sum(axis=1)
    return (float(np.percentile(est, 2.5)), float(np.percentile(est, 97.5)),
            float(np.percentile(est, 5.0)), float(np.percentile(est, 95.0)),
            float((est < 1).mean()), len(gs))
def ok(r): return r.get('vpath') and len(r['vpath']) >= 4 and r['vpath'][0] and r['vpath'][3] is not None
def show(name, cell):
    cell = [r for r in cell if ok(r)]
    if not cell: print("%-40s EMPTY" % name); return
    n = sum(r['vpath'][3] for r in cell); d = sum(r['vpath'][0] for r in cell)
    f1 = n / DISC ** 3 / d
    en = kish([r['vpath'][0] for r in cell])
    p = boot(cell, lambda r: r['key'], lambda r: r['vpath'][3] / DISC ** 3, lambda r: r['vpath'][0])
    c = boot(cell, lambda r: r['year'], lambda r: r['vpath'][3] / DISC ** 3, lambda r: r['vpath'][0])
    bar = "PASS" if (en >= 35 and p[0] > 1 and c[0] > 1) else "FAIL"
    print("%-40s n=%4d  F1=%6.3f  effn=%7.2f | player95 [%6.3f,%6.3f] 90%% [%6.3f,%6.3f] | "
          "class95 [%6.3f,%6.3f] 90%% [%6.3f,%6.3f] cl=%2d | F8 %s"
          % (name, len(cell), f1, en, p[0], p[1], p[2], p[3], c[0], c[1], c[2], c[3], c[5], bar))
LEG = [r for r in recs if r.get('teaches_curve') and r.get('year') and 2004 <= r['year'] <= 2022]
RU = [r for r in LEG if r['pos'] == 'RUCK']
print("=" * 160)
print("PER-ENTRANT INSTRUMENT (stage5 walk-forward, one row per entrant; F1 = sum(v_yr4)/1.0939^3 / sum(v_yr1))")
print("=" * 160)
show("LEG all positions", LEG)
show("LEG RUCK", RU)
show("LEG RUCK, played year 1", [r for r in RU if r.get('played_yr1')])
show("LEG RUCK, sat out year 1", [r for r in RU if r.get('sat_out_yr1')])
show("LEG RUCK pick 1-20", [r for r in RU if r['pick'] and r['pick'] <= 20])
show("LEG RUCK pick 21-64", [r for r in RU if r['pick'] and r['pick'] > 20])
NAMED = {'nicholas-naitanui', 'matthew-kreuzer', 'paddy-ryder', 'daniel-gorringe'}
show("LEG RUCK ex the 4 named", [r for r in RU if r['key'] not in NAMED])
print()
for lab, f in (("pre-2012 (2004-2011)", lambda y: y <= 2011), ("2012-2017", lambda y: 2012 <= y <= 2017),
               ("2018-2022", lambda y: y >= 2018)):
    show("LEG RUCK " + lab, [r for r in RU if f(r['year'])])
print()
print("  the ruck entrants, enumerated (F' = v_yr4/1.0939^3 / v_yr1):")
print("  %-24s %5s %5s %4s %9s %9s %9s %7s" % ("key", "year", "pick", "g1", "v0", "v_yr1", "v_yr4", "F'"))
for r in sorted([x for x in RU if ok(x)], key=lambda z: (z['year'], z['pick'] or 99)):
    print("  %-24s %5d %5s %4s %9.1f %9.1f %9.1f %7.3f" % (
        r['key'], r['year'], r['pick'], r.get('games_yr1'), r['v0'], r['vpath'][0], r['vpath'][3],
        r['vpath'][3] / DISC ** 3 / r['vpath'][0]))
