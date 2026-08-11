"""The RELATIVE cell: ruck F1 divided by the leg's own F1, with a joint bootstrap.
   The leg is not at 1.00 on this instrument (N=1 leg F1 = 1.136), so the comparator for a ruck dial
   is the leg, not no-arb parity.  Both ratios are recomputed inside every bootstrap replicate."""
import json, numpy as np
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
s6 = json.load(open(SP + "s6_rows.json"))
CF = {(r['key'], r['Y']): r for r in json.load(open(SP + "ruck_cf2_branch.json"))}
B = 20000; RNG = np.random.default_rng(20260810)
ND = [r for r in s6 if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022]

def rel(cellname, legrows, pricef=lambda r: r['price']):
    ru = [r for r in legrows if r['pos'] == 'RUCK']
    lf = sum(r['F'] for r in legrows) / sum(pricef(r) for r in legrows)
    rf = sum(r['F'] for r in ru) / sum(pricef(r) for r in ru)
    for keyname, keyf in (('player', lambda r: r['key']), ('class', lambda r: r['C'])):
        g = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
        for r in legrows:
            a = g[keyf(r)]; a[0] += r['F']; a[1] += pricef(r)
            if r['pos'] == 'RUCK': a[2] += r['F']; a[3] += pricef(r)
        gs = list(g.values()); G = len(gs)
        M = np.array(gs)
        idx = RNG.integers(0, G, size=(B, G))
        lnum = M[:, 0][idx].sum(axis=1); lden = M[:, 1][idx].sum(axis=1)
        rnum = M[:, 2][idx].sum(axis=1); rden = M[:, 3][idx].sum(axis=1)
        ok = rden > 0
        est = (rnum[ok] / rden[ok]) / (lnum[ok] / lden[ok])
        print("  %-40s %-7s  ratio=%.3f  95%% [%.3f, %.3f]  90%% [%.3f, %.3f]  P(ratio<1)=%.3f"
              % (cellname, keyname, rf / lf, np.percentile(est, 2.5), np.percentile(est, 97.5),
                 np.percentile(est, 5.0), np.percentile(est, 95.0), (est < 1).mean()))

print("=" * 128)
print("RUCK F1 RELATIVE TO THE LEG'S OWN F1  (>1 = rucks under-priced RELATIVE to the leg)")
print("=" * 128)
rel("N=1 leg, shipped prices", [r for r in ND if r['N'] == 1])
rel("N=1..3 leg, shipped prices", [r for r in ND if 1 <= r['N'] <= 3])
rel("ALL N leg, shipped prices", ND)
print()
print("  the same, with the ruck ceiling neutralised on the ruck rows (leg prices unchanged elsewhere):")
def pf_A(r): return CF[(r['key'], r['Y'])]['price_A'] if (r['pos'] == 'RUCK' and (r['key'], r['Y']) in CF) else r['price']
def pf_AC(r): return CF[(r['key'], r['Y'])]['price_AC'] if (r['pos'] == 'RUCK' and (r['key'], r['Y']) in CF) else r['price']
rel("N=1 leg, ceiling OFF", [r for r in ND if r['N'] == 1], pf_A)
rel("N=1 leg, ceiling OFF + pole ON", [r for r in ND if r['N'] == 1], pf_AC)
rel("N=1..3 leg, ceiling OFF", [r for r in ND if 1 <= r['N'] <= 3], pf_A)
rel("N=1..3 leg, ceiling OFF + pole ON", [r for r in ND if 1 <= r['N'] <= 3], pf_AC)
print()
print("=" * 128)
print("PER-ENTRANT INSTRUMENT, same relative reading")
print("=" * 128)
PE = json.load(open(SP + "per_entrant_338_stage5.json"))['recs']
def ok(r): return r.get('vpath') and len(r['vpath']) >= 4 and r['vpath'][0] and r['vpath'][3] is not None
LEG = [r for r in PE if r.get('teaches_curve') and r.get('year') and 2004 <= r['year'] <= 2022 and ok(r)]
D = 1.0939
for keyname, keyf in (('player', lambda r: r['key']), ('class', lambda r: r['year'])):
    g = defaultdict(lambda: [0.0, 0.0, 0.0, 0.0])
    for r in LEG:
        a = g[keyf(r)]; a[0] += r['vpath'][3] / D ** 3; a[1] += r['vpath'][0]
        if r['pos'] == 'RUCK': a[2] += r['vpath'][3] / D ** 3; a[3] += r['vpath'][0]
    M = np.array(list(g.values())); G = len(M)
    idx = RNG.integers(0, G, size=(B, G))
    ln = M[:, 0][idx].sum(axis=1); ld = M[:, 1][idx].sum(axis=1)
    rn = M[:, 2][idx].sum(axis=1); rd = M[:, 3][idx].sum(axis=1)
    ok2 = rd > 0; est = (rn[ok2] / rd[ok2]) / (ln[ok2] / ld[ok2])
    lf = M[:, 0].sum() / M[:, 1].sum(); rf = M[:, 2].sum() / M[:, 3].sum()
    print("  %-40s %-7s  ratio=%.3f  95%% [%.3f, %.3f]  90%% [%.3f, %.3f]  P(<1)=%.3f"
          % ("per-entrant leg", keyname, rf / lf, np.percentile(est, 2.5), np.percentile(est, 97.5),
             np.percentile(est, 5.0), np.percentile(est, 95.0), (est < 1).mean()))
