"""board_movers.py <boardA.json> <boardB.json> [labelA labelB] — name the active-row + pick movers
between two exported boards (A=before, B=after). Prints md5s, mover count, and every mover named with
its value class. Used for the per-consumer AFFECTED-ROW proofs (counts are not behaviours — rows named)."""
import json, sys, hashlib

def md5(p):
    h = hashlib.md5(open(p, 'rb').read()); return h.hexdigest()[:8]

def bykey(b): return {p['key']: p for p in b.get('active', []) if p.get('key')}
def picks(b): return {p['n']: p['v'] for p in b.get('picks', [])}

A = json.load(open(sys.argv[1])); B = json.load(open(sys.argv[2]))
la = sys.argv[3] if len(sys.argv) > 3 else 'A'
lb = sys.argv[4] if len(sys.argv) > 4 else 'B'
ka, kb = bykey(A), bykey(B)
common = set(ka) & set(kb)
movers = []
for k in common:
    va, vb = ka[k].get('v'), kb[k].get('v')
    if va != vb:
        movers.append((kb[k].get('name', k), va, vb, (vb - va) if (va is not None and vb is not None) else None,
                       kb[k].get('type'), kb[k].get('pos'), kb[k].get('age')))
pa, pb = picks(A), picks(B)
pmv = [(n, pa.get(n), pb.get(n)) for n in sorted(set(pa) | set(pb)) if pa.get(n) != pb.get(n)]

print("board md5: %s %s -> %s %s" % (la, md5(sys.argv[1]), lb, md5(sys.argv[2])))
print("active movers: %d / %d common (+%d added, -%d removed)"
      % (len(movers), len(common), len(set(kb) - set(ka)), len(set(ka) - set(kb))))
if movers:
    net = sum(m[3] for m in movers if m[3] is not None)
    print("net ΣΔ = %+d  gross = %d" % (net, sum(abs(m[3]) for m in movers if m[3] is not None)))
    for m in sorted(movers, key=lambda x: -abs(x[3] or 0)):
        print("  %-26s %5s -> %5s (%+5s)  %-4s %-8s age%s"
              % (m[0][:26], m[1], m[2], m[3], m[4], m[5], m[6]))
else:
    print("  (NULL — no active row moved; hash-equal on values)")
print("pick movers: %d" % len(pmv))
for n, a, b in pmv[:20]:
    print("  pick %2s: %s -> %s (%+s)" % (n, a, b, (b - a) if (a is not None and b is not None) else '?'))
