"""D2b + D3 — eff-n at three levels, the era split, and the independent per-entrant instrument."""
import json, numpy as np
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
rows = json.load(open(SP + "s6_rows.json"))
B = 20000
RNG = np.random.default_rng(20260810)

def kish(w):
    w = np.asarray(w, float); s = w.sum()
    return float(s * s / (w * w).sum()) if s > 0 else 0.0
def kish_by(cell, key):
    g = defaultdict(float)
    for r in cell: g[key(r)] += r['price']
    return kish(list(g.values())), len(g)
def boot(cell, key, B=B):
    groups = defaultdict(list)
    for r in cell: groups[key(r)].append(r)
    gids = list(groups)
    gF = np.array([sum(x['F'] for x in groups[g]) for g in gids])
    gP = np.array([sum(x['price'] for x in groups[g]) for g in gids])
    G = len(gids)
    idx = RNG.integers(0, G, size=(B, G))
    num = gF[idx].sum(axis=1); den = gP[idx].sum(axis=1)
    ok = den > 0; est = num[ok] / den[ok]
    return (float(np.percentile(est, 2.5)), float(np.percentile(est, 97.5)),
            float(np.percentile(est, 5.0)), float(np.percentile(est, 95.0)),
            float((est < 1.0).mean()), G)

def line(name, cell):
    if not cell:
        print("%-44s  EMPTY" % name); return
    sp = sum(r['price'] for r in cell); f1 = sum(r['F'] for r in cell) / sp
    en_row = kish([r['price'] for r in cell])
    en_pl, npl = kish_by(cell, lambda r: r['key'])
    en_cl, ncl = kish_by(cell, lambda r: r['C'])
    p = boot(cell, lambda r: r['key']); c = boot(cell, lambda r: r['C'])
    bar = "PASS" if (en_pl >= 35 and p[0] > 1.0 and c[0] > 1.0) else "FAIL"
    print("%-44s rows=%4d  F1=%6.3f | effn row=%7.2f  player=%6.2f (n=%3d)  class=%5.2f (n=%2d) | "
          "player95 [%6.3f,%6.3f]  class95 [%6.3f,%6.3f] | F8 %s"
          % (name, len(cell), f1, en_row, en_pl, npl, en_cl, ncl, p[0], p[1], c[0], c[1], bar))
    return dict(name=name, rows=len(cell), F1=f1, effn_row=en_row, effn_player=en_pl,
                n_players=npl, effn_class=en_cl, n_classes=ncl,
                player95=[p[0], p[1]], player90=[p[2], p[3]], class95=[c[0], c[1]],
                class90=[c[2], c[3]], p_below1_player=p[4], p_below1_class=c[4], f8=bar)

ND = [r for r in rows if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022]
ALL = [r for r in rows if 2004 <= r['C'] <= 2022]
RES = []
print("=" * 175)
print("D2b  EFF-N AT THREE LEVELS.  The F8 bar is read at the INDEPENDENT unit (player): a player's F")
print("     is ONE career-year-4 point re-discounted into every evaluation row, so rows are not")
print("     independent draws.  Row-level Kish is printed because the bar is written on the cell's own")
print("     denominator weights; the player-level column is the honest one.")
print("=" * 175)
RES.append(line("RUCK ND 1-64 N=1  (PUBLISHED CELL)", [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ND 1-64 N=2", [r for r in ND if r['N'] == 2 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ND 1-64 N=3", [r for r in ND if r['N'] == 3 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ND 1-64 N=1..3 pooled", [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ND 1-64 ALL N", [r for r in ND if r['pos'] == 'RUCK']))
RES.append(line("RUCK ALL ROUTES N=1", [r for r in ALL if r['N'] == 1 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ALL ROUTES N=1..3 pooled", [r for r in ALL if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK']))
RES.append(line("RUCK ALL ROUTES ALL N", [r for r in ALL if r['pos'] == 'RUCK']))
RES.append(line("LEG (all pos) ND 1-64 N=1", [r for r in ND if r['N'] == 1]))
RES.append(line("LEG (all pos) ND 1-64 N=1..3", [r for r in ND if 1 <= r['N'] <= 3]))

print()
print("=" * 175)
print("D3  THE ERA SPLIT — draft classes pre-2012 / 2012-2017 / 2018-2022.")
print("    Maturity: a class only enters when it has reached career year 4 (C<=2022), so 2018+ is")
print("    structurally 2018-2022 and its year-4 points land 2022-2026.")
print("=" * 175)
ERAS = [("pre-2012 (C 2004-2011)", lambda C: C <= 2011),
        ("2012-2017", lambda C: 2012 <= C <= 2017),
        ("2018+ (C 2018-2022)", lambda C: C >= 2018)]
for lab, f in ERAS:
    RES.append(line("[N=1  ND 1-64 RUCK] " + lab, [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK' and f(r['C'])]))
print()
for lab, f in ERAS:
    RES.append(line("[N=1..3 ND 1-64 RUCK] " + lab, [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK' and f(r['C'])]))
print()
for lab, f in ERAS:
    RES.append(line("[ALL N ND 1-64 RUCK] " + lab, [r for r in ND if r['pos'] == 'RUCK' and f(r['C'])]))
print()
for lab, f in ERAS:
    RES.append(line("[N=1..3 ALL ROUTES RUCK] " + lab, [r for r in ALL if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK' and f(r['C'])]))
print()
print("    the four named pre-2012 top picks REMOVED (Naitanui 2008, Kreuzer 2007, Ryder 2005, Gorringe 2010):")
NAMED = {'nicholas-naitanui', 'matthew-kreuzer', 'paddy-ryder', 'daniel-gorringe'}
RES.append(line("[N=1  ND 1-64 RUCK] ex-4-named", [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK' and r['key'] not in NAMED]))
RES.append(line("[N=1..3 ND1-64 RUCK] ex-4-named", [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK' and r['key'] not in NAMED]))
RES.append(line("[ALL N ND 1-64 RUCK] ex-4-named", [r for r in ND if r['pos'] == 'RUCK' and r['key'] not in NAMED]))
print()
print("    the CEILING-BOUND rows removed (the 8 rows / 5 players the cap actually cut):")
BOUND = {('nicholas-naitanui', 2009), ('nicholas-naitanui', 2010), ('matthew-kreuzer', 2008),
         ('matthew-kreuzer', 2011), ('matthew-leuenberger', 2009), ('paddy-ryder', 2006),
         ('daniel-gorringe', 2011), ('daniel-gorringe', 2012)}
RES.append(line("[N=1  ND1-64 RUCK] ex-ceiling-bound rows", [r for r in ND if r['N'] == 1 and r['pos'] == 'RUCK' and (r['key'], r['Y']) not in BOUND]))
RES.append(line("[N=1..3 ND1-64 RUCK] ex-bound rows", [r for r in ND if 1 <= r['N'] <= 3 and r['pos'] == 'RUCK' and (r['key'], r['Y']) not in BOUND]))

print()
print("=" * 175)
print("D2c  INDEPENDENT INSTRUMENT — the per-entrant walk-forward artifact (stage5), one row per player")
print("     F1 = sum(vpath[3])/1.0939**3 / sum(vpath[0]) ;  F0 = sum(vpath[3])/1.0939**4 / sum(v0)")
print("=" * 175)
PE = json.load(open(SP + "per_entrant_338_stage5.json"))
recs = PE['recs']
def pe_cell(name, sel):
    c = [r for r in sel if r.get('vpath') and len(r['vpath']) >= 4
         and r['vpath'][0] and r['vpath'][3] is not None and r.get('v0')]
    if not c: print("%-44s EMPTY" % name); return
    n = sum(r['vpath'][3] for r in c); d1 = sum(r['vpath'][0] for r in c); d0 = sum(r['v0'] for r in c)
    f1 = n / 1.0939 ** 3 / d1; f0 = n / 1.0939 ** 4 / d0
    en = kish([r['vpath'][0] for r in c])
    gF = np.array([r['vpath'][3] for r in c]); gP = np.array([r['vpath'][0] for r in c])
    idx = RNG.integers(0, len(c), size=(B, len(c)))
    est = (gF[idx].sum(axis=1) / 1.0939 ** 3) / gP[idx].sum(axis=1)
    print("%-44s n=%4d  F1=%6.3f  F0=%6.3f  effn=%7.2f  player95 [%6.3f,%6.3f]  P(<1)=%.3f"
          % (name, len(c), f1, f0, en, np.percentile(est, 2.5), np.percentile(est, 97.5), (est < 1).mean()))
LEGPE = [r for r in recs if r.get('teaches_curve') and r.get('year') and 2004 <= r['year'] <= 2022]
pe_cell("per-entrant LEG (teaches_curve, 2004-22)", LEGPE)
pe_cell("per-entrant LEG RUCK", [r for r in LEGPE if r['pos'] == 'RUCK'])
for pz in ('MID', 'SF', 'SD', 'KPD', 'KPF'):
    pe_cell("per-entrant LEG " + pz, [r for r in LEGPE if r['pos'] == pz])
POOLPE = [r for r in recs if r.get('is_pool') and r.get('year') and 2004 <= r['year'] <= 2022]
pe_cell("per-entrant POOL RUCK", [r for r in POOLPE if r['pos'] == 'RUCK'])

json.dump([r for r in RES if r], open(SP + "d2b_cells.json", "w"), indent=1)
print("\nB=%d, percentile, seed 20260810" % B)
