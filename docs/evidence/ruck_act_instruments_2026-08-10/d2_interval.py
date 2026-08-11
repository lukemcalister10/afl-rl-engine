"""D2 — THE INTERVAL.  Bootstrap CIs on the ruck delivery-vs-price ratio F1 = sum(F)/sum(price).

Basis: docs/evidence/act_334B_2026-08-07/stage6/s6_rows.json (branch tip 3820303), the artifact the
published anchors were measured on (leg 1.229 / 1.136, RUCK 0.833 / 1.696, all reproduced exactly).
F = v(career year 4) / 1.0939**(4-N), busts and out-of-window = 0; price = the frozen walk-forward
price at the evaluation year.  F1 > 1 = UNDER-priced (delivery exceeds price).

Two resampling schemes, both nonparametric percentile:
  PLAYER   — resample distinct players with replacement (a player carries ALL his rows in the cell)
  CLASS    — resample draft classes with replacement (a class carries all its players' rows)
Kish effective n is computed on the cell's OWN denominator weights w = price:  (sum w)^2 / sum(w^2).
"""
import json, numpy as np
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
rows = json.load(open(SP + "s6_rows.json"))
B = 20000
RNG = np.random.default_rng(20260810)

def kish(w):
    w = np.asarray(w, float); s = w.sum()
    return float(s * s / (w * w).sum()) if s > 0 else 0.0

def boot(cell, key, B=B):
    """key: callable row -> cluster id.  Returns percentile CI on sum(F)/sum(price)."""
    groups = defaultdict(list)
    for r in cell: groups[key(r)].append(r)
    gids = list(groups)
    gF = np.array([sum(x['F'] for x in groups[g]) for g in gids])
    gP = np.array([sum(x['price'] for x in groups[g]) for g in gids])
    G = len(gids)
    idx = RNG.integers(0, G, size=(B, G))
    num = gF[idx].sum(axis=1); den = gP[idx].sum(axis=1)
    ok = den > 0
    est = num[ok] / den[ok]
    return dict(G=G, lo95=float(np.percentile(est, 2.5)), hi95=float(np.percentile(est, 97.5)),
                lo90=float(np.percentile(est, 5.0)), hi90=float(np.percentile(est, 95.0)),
                lo80=float(np.percentile(est, 10.0)), hi80=float(np.percentile(est, 90.0)),
                p_below_1=float((est < 1.0).mean()), med=float(np.median(est)), B=int(ok.sum()))

def report(name, cell, extra=""):
    if not cell:
        print("%-46s  EMPTY" % name); return
    sp = sum(r['price'] for r in cell); sf = sum(r['F'] for r in cell)
    f1 = sf / sp
    en = kish([r['price'] for r in cell])
    npl = len(set(r['key'] for r in cell)); ncl = len(set(r['C'] for r in cell))
    bp = boot(cell, lambda r: r['key'])
    bc = boot(cell, lambda r: r['C'])
    print("%-46s rows=%4d players=%3d classes=%2d  F1=%6.3f  effn(Kish,price)=%6.2f" %
          (name, len(cell), npl, ncl, f1, en))
    print("      player-resampled  95%% [%6.3f, %6.3f]  90%% [%6.3f, %6.3f]  P(F1<1)=%.3f" %
          (bp['lo95'], bp['hi95'], bp['lo90'], bp['hi90'], bp['p_below_1']))
    print("      class-clustered   95%% [%6.3f, %6.3f]  90%% [%6.3f, %6.3f]  P(F1<1)=%.3f   clusters=%d %s" %
          (bc['lo95'], bc['hi95'], bc['lo90'], bc['hi90'], bc['p_below_1'], bc['G'], extra))
    return dict(name=name, n=len(cell), players=npl, classes=ncl, F1=f1, effn=en, player=bp, cls=bc)

OUT = []
ND = [r for r in rows if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022]
ALL = [r for r in rows if 2004 <= r['C'] <= 2022]

print("=" * 118)
print("A.  THE PUBLISHED CELL AND ITS NEIGHBOURS  (ND 1-64, classes 2004-2022)")
print("=" * 118)
OUT.append(report("[A1] RUCK, N=1  (THE PUBLISHED CELL, n=11)", [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK']))
OUT.append(report("[A2] whole leg, N=1  (the 414)", [r for r in ND if r['N'] == 1]))
for pz in ('MID', 'SF', 'SD', 'KPD', 'KPF'):
    OUT.append(report("[A2." + pz + "] " + pz + ", N=1", [r for r in ND if r['N'] == 1 and r['pos'] == pz]))

print()
print("=" * 118)
print("B.  WIDER LAWFUL RUCK POPULATIONS  (each disclosed)")
print("=" * 118)
OUT.append(report("[B1] RUCK N=1, ALL ROUTES (ND+pool)", [r for r in ALL if r['N'] == 1 and r['pos'] == 'RUCK']))
OUT.append(report("[B2] RUCK N=1, POOL ROUTES ONLY", [r for r in ALL if r['N'] == 1 and r['pos'] == 'RUCK' and not (r['nd'] and r['pk'] <= 64)]))
OUT.append(report("[B3] RUCK ND 1-64, N=1..3 pooled", [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK']))
OUT.append(report("[B4] RUCK ND 1-64, ALL N", [r for r in ND if r['pos'] == 'RUCK']))
OUT.append(report("[B5] RUCK ALL ROUTES, ALL N", [r for r in ALL if r['pos'] == 'RUCK']))

print()
print("=" * 118)
print("C.  LATER HORIZONS  (ND 1-64 RUCK, one evaluation year per cell)")
print("=" * 118)
for NN in range(1, 9):
    OUT.append(report("[C%d] RUCK ND 1-64, N=%d" % (NN, NN), [r for r in ND if r['N'] == NN and r['pos'] == 'RUCK']))
print()
print("   ... and the whole leg at the same horizons, for scale:")
for NN in range(1, 7):
    c = [r for r in ND if r['N'] == NN]
    sp = sum(r['price'] for r in c); sf = sum(r['F'] for r in c)
    print("        leg N=%d  rows=%4d  F1=%.4f  effn=%.1f" % (NN, len(c), sf / sp, kish([r['price'] for r in c])))

json.dump([o for o in OUT if o], open(SP + "d2_intervals.json", "w"), indent=1)
print("\nreps B=%d per scheme; percentile method; seed 20260810" % B)
