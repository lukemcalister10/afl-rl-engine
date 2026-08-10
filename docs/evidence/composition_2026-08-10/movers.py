"""PER-ITEM MOVERS — one function, run over any pair of boards. READ-ONLY.

Usage: movers.py <before.json> <after.json> <label>
Prints the mover count, direction split, the board ratio, the position concentration and the
top movers both ways. This is the single instrument every per-item attribution column uses, so
no two items are measured by two code paths.
"""
import os, sys, json, collections

bef, aft, label = sys.argv[1], sys.argv[2], sys.argv[3]
B = {r['key']: r for r in json.load(open(bef))['active']}
A = {r['key']: r for r in json.load(open(aft))['active']}
keys = set(B) | set(A)
sb = sum(r['v'] for r in B.values()); sa = sum(r['v'] for r in A.values())

mv = []
for k in keys:
    b, a = B.get(k), A.get(k)
    if b is None or a is None:
        mv.append((0, k, (a or b).get('name'), (a or b).get('gf'), None if b is None else b['v'],
                   None if a is None else a['v'], 'ROSTER CHANGE'))
        continue
    d = a['v'] - b['v']
    if d: mv.append((d, k, a.get('name'), a.get('gf'), b['v'], a['v'], ''))

print("=" * 96)
print("MOVERS — %s" % label)
print("  before %s  (n=%d, sum %d)" % (os.path.basename(bef), len(B), sb))
print("  after  %s  (n=%d, sum %d)" % (os.path.basename(aft), len(A), sa))
print("=" * 96)
real = [m for m in mv if m[6] == '']
up = [m for m in real if m[0] > 0]; dn = [m for m in real if m[0] < 0]
print("  movers: %d   up: %d (+%d)   down: %d (%d)"
      % (len(real), len(up), sum(m[0] for m in up), len(dn), sum(m[0] for m in dn)))
print("  board sum %d -> %d   delta %+d   ratio %.6f" % (sb, sa, sa - sb, (sa / sb) if sb else 0))
byp = collections.Counter(m[3] for m in real)
print("  by position: %s" % (" · ".join("%s %d" % (p, n) for p, n in byp.most_common()) or "none"))
if real:
    print("\n  %-26s %-6s %9s %9s %8s" % ("player", "pos", "before", "after", "delta"))
    for m in sorted(real, key=lambda x: x[0])[:15]:
        print("  %-26s %-6s %9d %9d %+8d" % (m[2], m[3], m[4], m[5], m[0]))
    if len(real) > 15:
        print("  ... top rises:")
        for m in sorted(real, key=lambda x: -x[0])[:10]:
            if m[0] > 0: print("  %-26s %-6s %9d %9d %+8d" % (m[2], m[3], m[4], m[5], m[0]))
odd = [m for m in mv if m[6]]
if odd:
    print("\n  ROSTER CHANGES (should be none): %d" % len(odd))
    for m in odd[:5]: print("   ", m[2], m[4], "->", m[5])
