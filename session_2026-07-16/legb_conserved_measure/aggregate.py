#!/usr/bin/env python3
"""LEG B UNFUNDED — aggregate the harvested per-point results into GRID.out (compact table) + feed MEASURE.md.
Reads out/gc_*.txt (GCJSON), out/beta_*.txt (s= line), out/POINT_s*.md (PTJSON). No engine load."""
import json, os, re, glob
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
GRID = ['0.15', '0.25', '0.35', '0.45', '0.55', '0.60', '0.65', '0.70']

def gcjson(label):
    p = os.path.join(OUT, 'gc_%s.txt' % label)
    if not os.path.exists(p): return None
    for ln in open(p):
        if ln.startswith('GCJSON '): return json.loads(ln[7:])
    return None

def beta(label):
    p = os.path.join(OUT, 'beta_%s.txt' % label)
    if not os.path.exists(p): return None
    for ln in open(p):
        if ln.startswith('s='):
            m = re.search(r's=(\S+)\s+beta=([\d.]+)\s+CI=\[([\d.]+),([\d.]+)\]\s+width=([\d.]+)\s+n=(\d+)', ln)
            if m:
                return dict(s=m.group(1), beta=float(m.group(2)), lo=float(m.group(3)), hi=float(m.group(4)),
                            width=float(m.group(5)), n=int(m.group(6)))
    return None

def ptjson(s):
    p = os.path.join(OUT, 'POINT_s%s.md' % s)  # PTJSON printed to stdout captured separately; try sidecar
    q = os.path.join(OUT, 'PT_%s.json' % s)
    if os.path.exists(q): return json.load(open(q))
    return None

lines = []
def w(s=''): lines.append(s); print(s)
w("# LEG B CONSERVED — MEASUREMENT GRID (shipped C applied; RL_UNCONSERVE UNSET)  ·  frozen instruments only")
w("# engine base b7a776c · store b1fd0bce · board OFF=8d90c9ac · toggle UNSET (no-op) · A/B byte-exact")
w()
# beta table
bc = beta('OFF')
w("## β (proven-27+, FROZEN beta_measure.py md5 14c59139; owner reference bar 0.80; rails width<=0.35, n>=120)")
w("  %-8s %8s  %-22s %8s %6s   %s" % ('point', 'β', 'CI', 'width', 'n', 'rails'))
if bc:
    w("  %-8s %8.4f  [%6.4f,%6.4f] %8.4f %6d   width%s n%s" % ('β_c(OFF)', bc['beta'], bc['lo'], bc['hi'],
      bc['width'], bc['n'], 'OK' if bc['width'] <= 0.35 else 'RAIL', 'OK' if bc['n'] >= 120 else '<120'))
for s in GRID:
    b = beta('s'+s)
    if b:
        w("  s=%-6s %8.4f  [%6.4f,%6.4f] %8.4f %6d   width%s n%s" % (s, b['beta'], b['lo'], b['hi'],
          b['width'], b['n'], 'OK' if b['width'] <= 0.35 else 'RAIL', 'OK' if b['n'] >= 120 else '<120'))
w()
# gcohort table
w("## G-COHORT y4/y5/y6 (FROZEN July-8 construction, ship_gates_check._b1_july8; hard <=1.30)")
w("  %-8s %9s %9s %9s   %s" % ('point', 'y4', 'y5', 'y6', 'verdict'))
for label in ['OFF'] + GRID:
    g = gcjson(label if label == 'OFF' else 's'+label)
    if g:
        br = g['breaches']
        w("  %-8s %9.4f %9.4f %9.4f   %s" % (label if label == 'OFF' else 's=' + label, g['y4'], g['y5'], g['y6'],
          'PASS x3 (<=1.30)' if not br else 'BREACH y%s' % br))
w()
# point summaries
w("## PER-POINT (E/B vs 1.75 · Bontempelli SCAR/rank · net board SigmaD · sincerity failures)")
w("  %-8s %9s %-28s %12s %10s" % ('point', 'E/B', 'Bontempelli', 'net ΣΔ', 'sinc-fail'))
for s in GRID:
    pt = ptjson(s)
    if pt:
        bo = pt.get('bont') or {}
        bont = 'SCAR%+d rank%+d %s' % (bo.get('dscar', 0), bo.get('drank', 0),
               'OK' if (bo.get('dscar', 0) > 0 and bo.get('drank', 0) < 0) else 'FAIL') if bo else 'n/a'
        eb = pt.get('eb_on')
        w("  s=%-6s %9s %-28s %+12d %10d" % (s, ('%.3f' % eb) if eb else 'n/a', bont, pt.get('sigmaD', 0), pt.get('sinc_fail', 0)))
w()
# pool re-rate
w("## POSITION-POOL Δ TOTALS per point (ΣΔnum by pos — which pools re-rate)")
POS = ['MID', 'GEN_FWD', 'KEY_FWD', 'GEN_DEF', 'KEY_DEF', 'RUC']
w("  %-8s " % 'point' + ' '.join('%9s' % p for p in POS))
for s in GRID:
    pt = ptjson(s)
    if pt and pt.get('pool'):
        w("  s=%-6s " % s + ' '.join('%+9d' % pt['pool'].get(p, 0) for p in POS))
open(os.path.join(OUT, 'GRID.out'), 'w').write('\n'.join(lines) + '\n')
