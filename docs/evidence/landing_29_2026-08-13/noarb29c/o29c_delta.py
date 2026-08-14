"""ORDER 29C — the year-0 column delta, counted before the prereg is filed."""
import os, sys, json, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(sys.argv[1]))['recs']
V = json.load(open(sys.argv[2]))
moved = same = 0; up = down = 0
so = sn = 0.0
for r in R:
    o = float(r['v0']); n = float(V['%s|%s|%s' % (r['key'], r['type'], r['year'])])
    so += o; sn += n
    if o == n: same += 1
    else:
        moved += 1
        if n > o: up += 1
        else: down += 1
print("v0 cells: %d total | MOVED %d | unchanged %d | rose %d | fell %d" % (len(R), moved, same, up, down))
print("Sigma v0 over all records: OLD %.1f -> LANDED %.1f  (%.4fx)" % (so, sn, sn / so))
json.dump(dict(n=len(R), moved=moved, unchanged=same, rose=up, fell=down,
               sum_old=round(so, 1), sum_new=round(sn, 1), ratio=round(sn / so, 6)),
          open(os.path.join(HERE, 'V0DELTA_29C.json'), 'w'), indent=1)
