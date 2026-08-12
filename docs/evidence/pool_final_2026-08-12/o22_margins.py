#!/usr/bin/env python3
"""ORDER 22 -- BOTH COHORT INSTRUMENTS, SHIP vs FINAL, WITH THE 14% CHARGE PRINTED BESIDE EVERY READING.

Sibling of docs/evidence/pool_retention_2026-08-12/noarb_margins.py, carried; the ONE change is that
the variant set is an argument. Reads only the JSON the two canonical instruments wrote.

    margin vs 14% = 14% - (year-0 -> year-1 appreciation).   A NEGATIVE margin is an ARBITRAGE.

  usage: o22_margins.py <out.json> <LABEL> [<LABEL> ...]
"""
import sys, json, os

N = '/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o22/noarb'
OUT = sys.argv[1]
LABELS = sys.argv[2:]
CHARGE = 0.14
P = print
RES = {'charge': CHARGE, 'readings': []}

P("=" * 116)
P("BOTH COHORT INSTRUMENTS -- margins against the %g%% annual charge. A NEGATIVE MARGIN IS AN ARBITRAGE."
  % (CHARGE * 100))
P("=" * 116)
P()
P("ALL-ARM DECIDING INSTRUMENT  (noarb_table_allarm.py)")
P("  %-12s %-10s %8s %8s %8s %8s %8s %8s | %10s %12s %8s" %
  ('window', 'variant', 'yr0', 'yr1', 'yr2', 'yr3', 'yr4', 'yr5', 'apprec 0-1', 'margin v14%', 'verdict'))
for lab in LABELS:
    p = os.path.join(N, 'allarm_%s.json' % lab)
    if not os.path.exists(p):
        P("  (no allarm json for %s)" % lab); continue
    D = json.load(open(p))
    for wname, W in D['groups'].items():
        if 'rows' not in W: continue
        yr = {int(r['N']): r['ratio_meanN_over_mean0'] for r in W['rows']}
        a = yr.get(1, float('nan')) / yr.get(0, 1.0) - 1.0
        m = CHARGE - a
        RES['readings'].append(dict(instrument='allarm', window=wname, variant=lab,
                                    yr={str(k): yr[k] for k in sorted(yr)}, apprec=a, margin=m,
                                    arb=bool(m < 0), n=W.get('n')))
        P("  %-12s %-10s %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f | %9.2f%% %11.2f%% %8s" %
          ("%s n=%s" % (wname, W.get('n')), lab, yr.get(0, float('nan')), yr.get(1, float('nan')),
           yr.get(2, float('nan')), yr.get(3, float('nan')), yr.get(4, float('nan')),
           yr.get(5, float('nan')), 100 * a, 100 * m, 'ARB' if m < 0 else 'no arb'))
P()
P("LEGACY RETAINED INSTRUMENT  (noarb_table_338.py, UNMODIFIED)")
P("  %-14s %-10s %8s %10s %12s %8s" % ('group', 'variant', 'yr1', 'apprec 0-1', 'margin v14%', 'verdict'))
for lab in LABELS:
    p = os.path.join(N, 'table_%s.json' % lab)
    if not os.path.exists(p):
        P("  (no table json for %s)" % lab); continue
    D = json.load(open(p))
    for g, G in D['groups'].items():
        if not isinstance(G, dict) or 'rows' not in G: continue
        y = {int(r['N']): r['ratio_meanN_over_mean0'] for r in G['rows']}
        if 1 not in y or 0 not in y: continue
        a = y[1] / y[0] - 1.0
        m = CHARGE - a
        RES['readings'].append(dict(instrument='legacy338', window=g, variant=lab,
                                    yr={str(k): y[k] for k in sorted(y)}, apprec=a, margin=m,
                                    arb=bool(m < 0), n=G.get('n')))
        P("  %-14s %-10s %8.4f %9.2f%% %11.2f%% %8s" % (g, lab, y[1], 100 * a, 100 * m,
                                                        'ARB' if m < 0 else 'no arb'))
P()
narb = sum(1 for r in RES['readings'] if r['arb'])
RES['n_readings'] = len(RES['readings']); RES['n_arbitrages'] = narb
P("  ARBITRAGES OPENED: %d of %d readings." % (narb, len(RES['readings'])))
json.dump(RES, open(OUT, 'w'), indent=1, default=float)
P("  wrote %s" % OUT)
