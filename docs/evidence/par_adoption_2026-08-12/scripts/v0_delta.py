"""ORDER 20B TASK 1 — v0 DELTAS UNDER THE ARM-SPLIT FIX.

Reads two engine_probe.py outputs (HEAD tree, FIX tree) and reports the delta in
`v0_start`, `_v0_uncapped` and `_v0_raw` for EVERY row the engine carries, BOTH arms,
cut by arm, position group and pick band. Also tests PREREG P2/P3 directly.

Population: all 1002 rows the board carries (active + back), which is exactly the population
BOARD_DELTA_par_armsplit.json scored (national 668 + pool 334).

Run: python3 v0_delta.py <probe_HEAD.json> <probe_FIX.json> <out_prefix>
"""
import json, sys, collections

H = json.load(open(sys.argv[1])); X = json.load(open(sys.argv[2]))
PRE = sys.argv[3]
hh = {(r['set'], r['key']): r for r in H['rows']}
xx = {(r['set'], r['key']): r for r in X['rows']}
KEYS = [k for k in hh if k in xx]

BANDS = ['1-3', '4-7', '8-12', '13-20', '21-27', '28-35', '36-48', '49-99', 'none']
GROUPS = ['MID', 'SD', 'SF', 'KPD', 'KPF', 'RUCK']
P = print
OUT = {}


def national(r): return r['ty'] == 'ND' and (r['ep'] or 99) <= 64


def arm(r): return 'NATIONAL' if national(r) else 'POOL'


FIELDS = ['v0_start', 'v0_uncapped', 'v0_raw']
P("=" * 116)
P("ORDER 20B TASK 1 — v0 UNDER THE PAR ARM-SPLIT FIX")
P("  HEAD probe %s   (arm_split=%s)" % (sys.argv[1], H['meta']['par_arm_split']))
P("  FIX  probe %s   (arm_split=%s)" % (sys.argv[2], X['meta']['par_arm_split']))
P("  population: %d rows carried by the board (active+back) = the BOARD_DELTA population" % len(KEYS))
P("=" * 116)


def stats(sub, fld):
    """movers / mean pct / total, over rows where both sides are finite and HEAD is non-zero."""
    n = mv = 0; tot_a = tot_b = 0.0; pcts = []
    for k in sub:
        a = hh[k].get(fld); b = xx[k].get(fld)
        if a is None or b is None: continue
        n += 1; tot_a += a; tot_b += b
        if abs(b - a) > 1e-9:
            mv += 1
            if abs(a) > 1e-9: pcts.append(100.0 * (b - a) / a)
    d = tot_b - tot_a
    return dict(n=n, movers=mv, tot_before=tot_a, tot_after=tot_b, delta=d,
                pct=(100.0 * d / tot_a if abs(tot_a) > 1e-9 else None),
                mean_abs_pct=(sum(abs(x) for x in pcts) / len(pcts) if pcts else 0.0),
                mean_pct=(sum(pcts) / len(pcts) if pcts else 0.0),
                max_up=(max(pcts) if pcts else 0.0), max_dn=(min(pcts) if pcts else 0.0))


# ---------------------------------------------------------------- 1. by arm
for fld in FIELDS:
    P()
    P("  ---- %s ----------------------------------------------------------------" % fld)
    P("    %-10s %5s %7s  %14s %14s %10s %8s %9s %8s %8s" %
      ('arm', 'n', 'movers', 'total before', 'total after', 'delta', 'pct', 'mean|%|', 'max+%', 'max-%'))
    for a in ('NATIONAL', 'POOL'):
        sub = [k for k in KEYS if arm(hh[k]) == a]
        s = stats(sub, fld)
        OUT['%s|arm|%s' % (fld, a)] = s
        P("    %-10s %5d %7d  %14.1f %14.1f %10.1f %7s%% %8.3f %8.2f %8.2f" %
          (a, s['n'], s['movers'], s['tot_before'], s['tot_after'], s['delta'],
           ('%.4f' % s['pct']) if s['pct'] is not None else 'n/a',
           s['mean_abs_pct'], s['max_up'], s['max_dn']))

# ---------------------------------------------------------------- 2. arm x position
P()
P("  ---- v0_start BY ARM x POSITION GROUP -----------------------------------------")
P("    %-9s %-6s %5s %7s %12s %12s %9s %8s" % ('arm', 'pos', 'n', 'movers', 'before', 'after', 'delta', 'pct'))
for a in ('NATIONAL', 'POOL'):
    for g in GROUPS:
        sub = [k for k in KEYS if arm(hh[k]) == a and hh[k]['pos'] == g]
        if not sub: continue
        s = stats(sub, 'v0_start'); OUT['v0_start|pos|%s|%s' % (a, g)] = s
        P("    %-9s %-6s %5d %7d %12.1f %12.1f %+9.1f %7s%%" %
          (a, g, s['n'], s['movers'], s['tot_before'], s['tot_after'], s['delta'],
           ('%.4f' % s['pct']) if s['pct'] is not None else 'n/a'))

# ---------------------------------------------------------------- 3. arm x pick band
P()
P("  ---- v0_start BY ARM x PICK BAND (the #338 bands) -----------------------------")
P("    %-9s %-7s %5s %7s %12s %12s %9s %8s" % ('arm', 'band', 'n', 'movers', 'before', 'after', 'delta', 'pct'))
for a in ('NATIONAL', 'POOL'):
    for b in BANDS:
        sub = [k for k in KEYS if arm(hh[k]) == a and hh[k]['band'] == b]
        if not sub: continue
        s = stats(sub, 'v0_start'); OUT['v0_start|band|%s|%s' % (a, b)] = s
        P("    %-9s %-7s %5d %7d %12.1f %12.1f %+9.1f %7s%%" %
          (a, b, s['n'], s['movers'], s['tot_before'], s['tot_after'], s['delta'],
           ('%.4f' % s['pct']) if s['pct'] is not None else 'n/a'))

# ---------------------------------------------------------------- 4. KPD, called out explicitly
P()
P("  ---- KPD: THE OWNER'S QUESTION ('does the v0 for KPDs go backwards too?') ------")
kpd = [k for k in KEYS if hh[k]['pos'] == 'KPD']
kn = [k for k in kpd if national(hh[k])]
s = stats(kn, 'v0_start'); OUT['KPD_national'] = s
P("    NATIONAL KPD  n=%d movers=%d  v0_start total %.1f -> %.1f  (%+.1f, %s%%)" %
  (s['n'], s['movers'], s['tot_before'], s['tot_after'], s['delta'],
   ('%.4f' % s['pct']) if s['pct'] is not None else 'n/a'))
up = [k for k in kn if (xx[k]['v0_start'] or 0) > (hh[k]['v0_start'] or 0) + 1e-9]
dn = [k for k in kn if (xx[k]['v0_start'] or 0) < (hh[k]['v0_start'] or 0) - 1e-9]
P("    of the national KPD movers: %d UP, %d DOWN, %d flat" % (len(up), len(dn), s['n'] - len(up) - len(dn)))
P("    every national KPD row, by pick:")
P("      %-24s %4s %8s %10s %10s %9s %8s" % ('name', 'ep', 'ageR', 'v0 HEAD', 'v0 FIX', 'delta', 'pct'))
for k in sorted(kn, key=lambda k: (hh[k]['ep'] or 99)):
    a = hh[k]['v0_start']; b = xx[k]['v0_start']
    if a is None or b is None: continue
    P("      %-24s %4s %8s %10.2f %10.2f %+9.2f %+7.2f%%" %
      (hh[k]['name'][:24], hh[k]['ep'], hh[k]['ageR'], a, b, b - a, 100.0 * (b - a) / a if a else 0))

# ---------------------------------------------------------------- 5. largest movers by name
P()
P("  ---- LARGEST v0_start MOVERS BY NAME (both arms, by |pct|) --------------------")
mv = [(k, hh[k]['v0_start'], xx[k]['v0_start']) for k in KEYS
      if hh[k]['v0_start'] and xx[k]['v0_start'] and abs(xx[k]['v0_start'] - hh[k]['v0_start']) > 1e-9]
P("      %-24s %-9s %-5s %4s %10s %10s %9s %8s" % ('name', 'arm', 'pos', 'ep', 'v0 HEAD', 'v0 FIX', 'delta', 'pct'))
for k, a, b in sorted(mv, key=lambda t: -abs((t[2] - t[1]) / t[1]))[:25]:
    P("      %-24s %-9s %-5s %4s %10.2f %10.2f %+9.2f %+7.2f%%" %
      (hh[k]['name'][:24], arm(hh[k]), hh[k]['pos'], hh[k]['ep'], a, b, b - a, 100.0 * (b - a) / a))
P()
P("      (by absolute size)")
for k, a, b in sorted(mv, key=lambda t: -abs(t[2] - t[1]))[:15]:
    P("      %-24s %-9s %-5s %4s %10.2f %10.2f %+9.2f %+7.2f%%" %
      (hh[k]['name'][:24], arm(hh[k]), hh[k]['pos'], hh[k]['ep'], a, b, b - a, 100.0 * (b - a) / a))

# ---------------------------------------------------------------- 6. PREREG P2 / P3
P()
P("  ---- PREREG P2: is the v0_uncapped RATIO a pure function of (pos, effpk)? ------")
cells = collections.defaultdict(list)
for k in KEYS:
    a = hh[k].get('v0_uncapped'); b = xx[k].get('v0_uncapped')
    if not a or b is None: continue
    cells[(hh[k]['pos'], hh[k]['ep'])].append((b / a, hh[k]['name']))
bad = [(c, v) for c, v in cells.items() if len(v) > 1 and (max(x[0] for x in v) - min(x[0] for x in v)) > 1e-9]
P("    (pos,effpk) cells with >1 row: %d | cells whose ratio is NOT constant: %d" %
  (sum(1 for v in cells.values() if len(v) > 1), len(bad)))
OUT['P2_cells_multi'] = sum(1 for v in cells.values() if len(v) > 1)
OUT['P2_cells_inconsistent'] = len(bad)
for c, v in sorted(bad, key=lambda t: -(max(x[0] for x in t[1]) - min(x[0] for x in t[1])))[:10]:
    P("      %-6s pk%-3s spread %.3e   %s" % (c[0], c[1], max(x[0] for x in v) - min(x[0] for x in v),
                                              ', '.join('%s=%.9f' % (n, r) for r, n in v[:4])))
P()
P("  ---- PREREG P3: does that ratio EQUAL iso_corr_FIX/iso_corr_HEAD? -------------")
worst = (0.0, None)
nchk = 0
for k in KEYS:
    a = hh[k].get('v0_uncapped'); b = xx[k].get('v0_uncapped')
    ia = hh[k].get('iso'); ib = xx[k].get('iso')
    if not a or b is None or not ia or ib is None: continue
    nchk += 1
    d = abs((b / a) - (ib / ia))
    if d > worst[0]: worst = (d, hh[k]['name'], hh[k]['pos'], hh[k]['ep'], b / a, ib / ia)
P("    rows checked %d | worst |v0ratio - isoratio| = %.3e  %s" % (nchk, worst[0], worst[1:] if worst[1] else ''))
OUT['P3_rows'] = nchk; OUT['P3_worst_abs_diff'] = worst[0]

# ---------------------------------------------------------------- 7. the ISO table itself
P()
P("  ---- THE ISO MULTIPLIER TABLE (:497 V0 pick-surface synthetics), HEAD vs FIX ---")
P("    the ONLY par-fed factor that reaches v0. pick 65-70 route to the POOL arm under the fix (KMAX=70).")
P("      %-6s %s" % ('pos', ' '.join('%7s' % ('pk%d' % pk) for pk in [1, 3, 5, 10, 20, 30, 40, 50, 60, 64, 65, 70])))
for g in GROUPS:
    row = []
    for pk in [1, 3, 5, 10, 20, 30, 40, 50, 60, 64, 65, 70]:
        a = H['iso'].get('%s|%d' % (g, pk)); b = X['iso'].get('%s|%d' % (g, pk))
        row.append('%+6.2f%%' % (100.0 * (b / a - 1.0)) if a and b else '     --')
    P("      %-6s %s" % (g, ' '.join('%7s' % x for x in row)))
P("      (cells are the PERCENT CHANGE in iso_corr, FIX vs HEAD)")

json.dump(OUT, open(PRE + '.json', 'w'), indent=1)
P()
P("  json -> %s.json" % PRE)
