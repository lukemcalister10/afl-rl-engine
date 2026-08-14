"""ORDER 29C — score P29C-5 against the EMITTED matrices rather than against the pre-emit probe."""
import os, sys, json, statistics
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
A = json.load(open(sys.argv[1]))['recs']      # 29B
B = json.load(open(sys.argv[2]))['recs']      # 29C
PRE = json.load(open(os.path.join(HERE, 'LAWPROBE_29C.json')))['by_arm']
pre = {r['arm']: r for r in PRE}


def arm(r):
    if r['type'] == 'ND' and not r['is_pool_engine']: return 'ND 1-64'
    if r['type'] == 'ND': return 'ND>64'
    return r['type']


oa, na = defaultdict(list), defaultdict(list)
for r in A: oa[arm(r)].append(float(r['v0']))
for r in B: na[arm(r)].append(float(r['v0']))
print("  %-8s %6s %12s %12s %8s | %12s %12s %s"
      % ("arm", "n", "old mean", "new mean", "old/new", "PREREG old", "PREREG new", "match"))
allok = True
out = []
for a in sorted(oa, key=lambda x: -len(oa[x])):
    mo, mn = statistics.mean(oa[a]), statistics.mean(na[a])
    p = pre.get(a, {})
    ok = (round(mo, 2) == p.get('old_mean_v0') and round(mn, 2) == p.get('new_mean_v0'))
    allok &= ok
    print("  %-8s %6d %12.2f %12.2f %8.3f | %12s %12s %s"
          % (a, len(oa[a]), mo, mn, mo / mn if mn else float('nan'),
             p.get('old_mean_v0'), p.get('new_mean_v0'), "OK" if ok else "MISMATCH"))
    out.append(dict(arm=a, n=len(oa[a]), old_mean_v0=round(mo, 2), new_mean_v0=round(mn, 2),
                    ratio=round(mo / mn, 4) if mn else None, matches_prereg=bool(ok)))
print("P29C-5 vs the EMITTED matrices: %s" % ("HELD — every arm, both columns" if allok else "BREACHED"))
json.dump(dict(held=bool(allok), rows=out), open(os.path.join(HERE, 'ARMCHECK_29C.json'), 'w'), indent=1)
