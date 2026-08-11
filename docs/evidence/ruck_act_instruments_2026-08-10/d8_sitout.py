import json
from collections import defaultdict
SP = "/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/"
A = json.load(open(SP + "ruck_cf3_branch_allrows.json"))
s6 = json.load(open(SP + "s6_rows.json"))
nd = {(r['key'], r['C'], r['Y']): (r['nd'], r['pk']) for r in s6}
est = set((r['key'], r['C'], r['Y']) for r in s6 if r['pos'] == 'RUCK')
print("ALL priced RUCK (player, evaluation-year) rows, classes 2004-2022, years C+1..2026: n=%d" % len(A))
print("  established (ns>=1) = %d   SIT-OUT / not-yet-qualified (ns==0) = %d"
      % (sum(1 for r in A if r['ns'] >= 1), sum(1 for r in A if r['ns'] == 0)))
for lab, sel in (("ns>=1 (the measured established leg)", lambda r: r['ns'] >= 1),
                 ("ns==0 (sit-out / pre-qualification)", lambda r: r['ns'] == 0),
                 ("ALL ruck rows", lambda r: True)):
    c = [r for r in A if sel(r)]
    P = sum(r['price'] for r in c); PA = sum(r['price_A'] for r in c)
    PC = sum(r['price_C'] for r in c); PAC = sum(r['price_AC'] for r in c)
    nb = sum(1 for r in c if r['price_A'] > r['price'] + 0.5)
    print("  %-38s rows=%5d  Sprice=%10.1f  ceilOFF %+9.1f (rows cut %3d)  poleON %+9.1f  both %+9.1f"
          % (lab, len(c), P, PA - P, nb, PC - P, PAC - P))
print()
print("  the sit-out rows the ceiling actually moves:")
for r in sorted([x for x in A if x['ns'] == 0 and x['price_A'] > x['price'] + 0.5], key=lambda z: -(z['price_A'] - z['price']))[:25]:
    t = nd.get((r['key'], r['C'], r['Y']))
    print("    %-24s C=%d Y=%d N=%d pk=%3d  price=%8.1f -> ceilOFF %8.1f  (+%.1f)"
          % (r['key'], r['C'], r['Y'], r['N'], r['pk'], r['price'], r['price_A'], r['price_A'] - r['price']))
print()
byN = defaultdict(lambda: [0, 0, 0.0, 0.0])
for r in A:
    a = byN[r['N']]; a[0] += 1; a[3] += r['price']
    if r['price_A'] > r['price'] + 0.5: a[1] += 1; a[2] += r['price_A'] - r['price']
print("  bite by evaluation year (ALL ruck rows incl. sit-outs):")
for N in sorted(byN):
    n, nb, b, sp = byN[N]
    if nb: print("    N=%2d rows=%4d cut=%3d bite=%9.1f  (%.2f%% of Sprice %9.1f)" % (N, n, nb, b, 100*b/sp, sp))
