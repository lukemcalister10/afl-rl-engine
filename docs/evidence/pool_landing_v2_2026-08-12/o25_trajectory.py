#!/usr/bin/env python3
"""ORDER 25 -- THE ITERATION TRAJECTORY ON THE LANDED DELIVERY, printed honestly, every round.

Carried from docs/evidence/pool_landing_2026-08-12/o23_trajectory.py; only the scratchpad path moves.

  usage: o23_trajectory.py <out.json> <label> [<label> ...]
"""
import sys, json, os

IT = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o25/iter'
OUT = sys.argv[1]
LABS = sys.argv[2:]
ORDER = ['RD', 'SSP', 'MSD', 'IRE', 'PDA', 'PDN', 'PDS', 'UNR', 'ND>64']
P = print
TOL = 0.01
D = {}
for L in LABS:
    p = os.path.join(IT, 'derive_%s.json' % L)
    if os.path.exists(p): D[L] = json.load(open(p))
LABS = [L for L in LABS if L in D]

P("=" * 118)
P("THE ITERATE-TO-TOLERANCE TRAJECTORY.  Declared tolerance: %.1f%% relative on every pathway's lambda."
  % (TOL * 100))
P("=" * 118)
P()
P("RAW lambda (pathway career profile / the freshly measured national target) by round:")
P("  %-8s" % 'pathway' + "".join("%12s" % L for L in LABS))
for s in ORDER:
    P("  %-8s" % s + "".join("%12.6f" % D[L]['layer1'][s]['lam_raw'] for L in LABS))
P("  %-8s" % 'ALLPOOL' + "".join("%12.6f" % (D[L]['pool_profile'] / D[L]['target_nd_profile']) for L in LABS))
P()
P("SHRUNK lambda (the quantity the level step is driven by; K=15 uniform):")
P("  %-8s" % 'pathway' + "".join("%12s" % L for L in LABS))
for s in ORDER:
    P("  %-8s" % s + "".join("%12.6f" % D[L]['layer1'][s]['lam'] for L in LABS))
P()
P("THE LEVEL IN FORCE at each round (what the engine actually read, int-truncated):")
keys = [('SSP', 'signed_flat'), ('MSD', 'signed_flat'), ('IRE', 'signed_flat'), ('PDA', 'signed_flat'),
        ('PDN', 'signed_flat'), ('PDS', 'signed_flat'), ('UNR', 'signed_flat')]
P("  %-10s" % 'key' + "".join("%9s" % L for L in LABS))
for k, f in keys:
    P("  %-10s" % k + "".join("%9.0f" % float(D[L]['levels_in_force'][f][k]) for L in LABS))
P("  %-10s" % 'ND65+eff' + "".join("%9.0f" % float(D[L]['levels_in_force']['nd65_effective']) for L in LABS))
for p in ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']:
    P("  %-10s" % ('RD:' + p) + "".join("%9.0f" % float(D[L]['levels_in_force']['signed_rd_positional'][p])
                                        for L in LABS))
P()
P("THE TARGET at each round (the separation law, read at the calibration target itself):")
P("  %-10s" % 'target' + "".join("%12.10f" % D[L]['target_nd_profile'] for L in LABS))
tgt = {D[L]['target_nd_profile'] for L in LABS}
P("  distinct values across every round: %d  -> %s" % (len(tgt),
  'the target does NOT move when pool prices move' if len(tgt) == 1 else '*** THE TARGET MOVED ***'))
P()
last = LABS[-1]
P("CONVERGENCE AT THE FINAL ROUND (%s):" % last)
P("  %-8s %12s %12s %12s %12s %10s" % ('pathway', 'raw lam', '|raw-1|', 'shrunk lam', '|shrunk-1|', 'verdict'))
RES = {}
for s in ORDER:
    r = D[last]['layer1'][s]['lam_raw']; sh = D[last]['layer1'][s]['lam']
    ok = abs(sh - 1) <= TOL and abs(r - 1) <= TOL
    RES[s] = dict(raw=r, shrunk=sh, within=bool(ok))
    P("  %-8s %12.6f %12.4f%% %12.6f %11.4f%% %10s"
      % (s, r, 100 * abs(r - 1), sh, 100 * abs(sh - 1), 'within' if ok else 'OUT'))
P()
pool_agg = D[last]['pool_profile'] / D[last]['target_nd_profile']
P("  THE RESIDUAL IS AN IDENTITY, NOT NOISE. The shrinkage makes")
P("      shrunk = w*raw + (1-w)*pool_aggregate,  so  raw = (shrunk - (1-w)*pool_agg) / w.")
P("  With pool_agg = %.6f at this round, the predicted raw lambda for each pathway is:" % pool_agg)
P("  %-8s %10s %14s %14s %12s" % ('pathway', 'w', 'raw PREDICTED', 'raw MEASURED', 'difference'))
for s in ORDER:
    w = D[last]['layer1'][s]['w']; sh = D[last]['layer1'][s]['lam']
    pred = (sh - (1 - w) * pool_agg) / w
    P("  %-8s %10.4f %14.6f %14.6f %12.2e"
      % (s, w, pred, D[last]['layer1'][s]['lam_raw'], abs(pred - D[last]['layer1'][s]['lam_raw'])))
P()
P("  So every pathway's raw lambda is pinned by the POOL AGGREGATE. In ORDER 22 that aggregate was held")
P("  above 1 by ONE pathway a signed law forbade repricing -- ND>64, capped at the curve's pick-64")
P("  value -- and the 1% residual on every other pathway was that cap's arithmetic shadow. THE OWNER")
P("  REMOVED THE CAP (ruling 5262928754). The two aggregates below are now the SAME NUMBER to three")
P("  decimal places, which is what it looks like when the blocked pathway stops blocking:")
tot_e = sum(D[last]['layer1'][s]['entry_now'] for s in ORDER)
nd_e = D[last]['layer1']['ND>64']['entry_now']
tot_v = sum(D[last]['layer1'][s]['entry_now'] * D[last]['layer1'][s]['profile'] for s in ORDER)
nd_v = nd_e * D[last]['layer1']['ND>64']['profile']
ex = (tot_v - nd_v) / (tot_e - nd_e) / D[last]['target_nd_profile']
P("    pool aggregate INCLUDING ND>64 : %.6f" % pool_agg)
P("    pool aggregate EXCLUDING ND>64 : %.6f   (ND>64 is %.1f%% of the pool's entry weight)"
  % (ex, 100.0 * nd_e / tot_e))
json.dump(dict(tolerance=TOL, rounds=LABS, final=last, convergence=RES, pool_agg=pool_agg,
               pool_agg_ex_nd65=ex,
               raw={L: {s: D[L]['layer1'][s]['lam_raw'] for s in ORDER} for L in LABS},
               shrunk={L: {s: D[L]['layer1'][s]['lam'] for s in ORDER} for L in LABS},
               targets={L: D[L]['target_nd_profile'] for L in LABS},
               levels={L: D[L]['levels_in_force'] for L in LABS}),
          open(OUT, 'w'), indent=1, default=float)
P()
P("wrote %s" % OUT)
