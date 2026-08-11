"""D4 — THE DECOMPOSITION.  Branch (act) basis, teaching leg."""
import json
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
s6 = json.load(open(SP + "s6_rows.json"))
INSTR = json.load(open(SP + "ruck_instr_branch.json"))
V0 = INSTR['v0tab']
CF = {(r['key'], r['Y']): r for r in json.load(open(SP + "ruck_cf_branch.json"))}
IR = {(r['key'], r['Y']): r for r in INSTR['rows']}

leg = [r for r in s6 if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022 and r['N'] == 1]

print("=" * 120)
print("D4-B  THE DROPPED YEAR-0 SURFACE LIFT.   R = sum(v0_start)/sum(v0_uncapped) on the cell's own rows.")
print("      'honest mark-up' = shipped mark-up x R  (the mark-up trace's CF-B: carry the year-0 correction")
print("      into the year-1 price).  Delivered mark-up = sum(price)/sum(v0_start).")
print("=" * 120)
d = defaultdict(lambda: [0, 0.0, 0.0, 0.0, 0.0])
for r in leg:
    v = V0.get(r['key'])
    if v is None: continue
    a = d[r['pos']]; a[0] += 1; a[1] += r['price']; a[2] += v['v0s']; a[3] += v['v0u']; a[4] += r['F']
tot = [0, 0.0, 0.0, 0.0, 0.0]
print("%-6s %4s %10s %10s %10s %9s %9s %9s %9s" % ("pos", "n", "Sprice", "Sv0_start", "Sv0_unc",
                                                   "R", "mark-up", "honest", "F1"))
for pos in ('RUCK', 'KPD', 'KPF', 'MID', 'SF', 'SD'):
    n, sp, sv, su, sf = d[pos]
    for i, x in enumerate([n, sp, sv, su, sf]): tot[i] += x
    print("%-6s %4d %10.1f %10.1f %10.1f %9.4f %9.4f %9.4f %9.4f"
          % (pos, n, sp, sv, su, sv / su, sp / sv, (sp / sv) * (sv / su), sf / sp))
n, sp, sv, su, sf = tot
print("%-6s %4d %10.1f %10.1f %10.1f %9.4f %9.4f %9.4f %9.4f"
      % ("LEG", n, sp, sv, su, sv / su, sp / sv, (sp / sv) * (sv / su), sf / sp))
R_ruck = d['RUCK'][2] / d['RUCK'][3]; R_leg = sv / su

print()
print("=" * 120)
print("D4-AC  THE 2x2 COUNTERFACTUAL GRID on the 11 (ND 1-64, RUCK, N=1).")
print("       A = ruck ceiling neutralised.   C = pole granted (wage = the standard ramp).")
print("=" * 120)
ru = [r for r in leg if r['pos'] == 'RUCK']
S = lambda f: sum(f(r) for r in ru)
sv0 = sum(V0[r['key']]['v0s'] for r in ru)
sv0u = sum(V0[r['key']]['v0u'] for r in ru)
P   = S(lambda r: CF[(r['key'], r['Y'])]['price'])
PA  = S(lambda r: CF[(r['key'], r['Y'])]['price_A'])
PC  = S(lambda r: CF[(r['key'], r['Y'])]['price_C'])
PAC = S(lambda r: CF[(r['key'], r['Y'])]['price_AC'])
print("  shipped              Sprice=%9.1f  mark-up=%.4f" % (P, P / sv0))
print("  A  ceiling OFF       Sprice=%9.1f  mark-up=%.4f   delta=%+8.1f" % (PA, PA / sv0, PA - P))
print("  C  pole ON           Sprice=%9.1f  mark-up=%.4f   delta=%+8.1f" % (PC, PC / sv0, PC - P))
print("  AC ceiling OFF+pole  Sprice=%9.1f  mark-up=%.4f   delta=%+8.1f" % (PAC, PAC / sv0, PAC - P))
print("  pole increment WITH the ceiling live      = %+8.1f" % (PC - P))
print("  pole increment WITH the ceiling removed   = %+8.1f   (the ceiling absorbs %+.1f of it)"
      % (PAC - PA, (PC - P) - (PAC - PA)))
print()
print("  per player (N=1):")
print("  %-22s %9s %9s %9s %9s %9s %9s" % ("key", "price", "+A", "+C", "+AC", "v0_start", "v0_unc"))
for r in sorted(ru, key=lambda x: -x['price']):
    c = CF[(r['key'], r['Y'])]; v = V0[r['key']]
    print("  %-22s %9.1f %+9.1f %+9.1f %+9.1f %9.1f %9.1f"
          % (r['key'], c['price'], c['price_A'] - c['price'], c['price_C'] - c['price'],
             c['price_AC'] - c['price'], v['v0s'], v['v0u']))

print()
print("=" * 120)
print("D4  THE LADDER — closing the ruck mark-up gap to the leg, in mark-up units and in points.")
print("=" * 120)
m0 = P / sv0; mleg = sp / sv
gapU = mleg - m0; gapP = gapU * sv0
print("  shipped RUCK mark-up            %.4f" % m0)
print("  shipped LEG   mark-up            %.4f" % mleg)
print("  gap                              %.4f mark-up units = %.1f points on Sv0(ruck)=%.1f" % (gapU, gapP, sv0))
steps = [("(a) ceiling's direct bite", (PA - P) / sv0, PA - P),
         ("(c) pole denial, ceiling off", (PAC - PA) / sv0, PAC - PA)]
run = m0
for lab, du, dp in steps:
    run += du
    print("   + %-32s %+8.4f  (%+8.1f pts)  ->  %.4f" % (lab, du, dp, run))
mb = run * R_ruck
print("   x %-32s x%.4f              ->  %.4f   [(b) year-0 surface carry, R_ruck]" % ("(b) surface lift carried", R_ruck, mb))
print("     LEG comparator on the same footing: leg mark-up x R_leg = %.4f x %.4f = %.4f" % (mleg, R_leg, mleg * R_leg))
print("   residual (d) vs the leg comparator: %+.4f mark-up units = %+.1f points"
      % (mb - mleg * R_leg, (mb - mleg * R_leg) * sv0))

print()
print("=" * 120)
print("D4  SAME LADDER, ALL EVALUATION YEARS on the ND 1-64 ruck leg (n=379 rows / 49 players)")
print("=" * 120)
ruA = [r for r in s6 if r['nd'] and 1 <= r['pk'] <= 64 and 2004 <= r['C'] <= 2022 and r['pos'] == 'RUCK']
P   = sum(CF[(r['key'], r['Y'])]['price'] for r in ruA)
PA  = sum(CF[(r['key'], r['Y'])]['price_A'] for r in ruA)
PC  = sum(CF[(r['key'], r['Y'])]['price_C'] for r in ruA)
PAC = sum(CF[(r['key'], r['Y'])]['price_AC'] for r in ruA)
print("  shipped %9.1f | ceiling off %+8.1f | pole on %+8.1f | both %+8.1f"
      % (P, PA - P, PC - P, PAC - P))
print("  pole increment with ceiling live %+8.1f ; with ceiling removed %+8.1f" % (PC - P, PAC - PA))
byp = defaultdict(lambda: [0.0, 0.0, 0.0])
for r in ruA:
    c = CF[(r['key'], r['Y'])]
    byp[r['key']][0] += c['price_A'] - c['price']
    byp[r['key']][1] += c['price_C'] - c['price']
    byp[r['key']][2] += c['price']
print("  top movers (all years):  %-24s %10s %10s %10s" % ("key", "Sprice", "ceilingOFF", "poleON"))
for k in sorted(byp, key=lambda z: -(byp[z][0] + byp[z][1]))[:14]:
    a, c2, pp = byp[k]
    print("     %-24s %10.1f %+10.1f %+10.1f" % (k, pp, a, c2))
