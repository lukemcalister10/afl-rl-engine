#!/usr/bin/env python3
# ORDER 30B -- board-vs-board mover reader. Usage:
#   o30b_movers.py OLD.json NEW.json [--label X] [--json OUT.json] [--top N]
# Prints the mover count, the sum of deltas, the composition by evidence class, and the largest moves.
import json, sys, collections

def load(p):
    B = json.load(open(p))
    return {r['key']: r for r in B['active']}

old_p, new_p = sys.argv[1], sys.argv[2]
LABEL = sys.argv[sys.argv.index('--label') + 1] if '--label' in sys.argv else ''
TOP = int(sys.argv[sys.argv.index('--top') + 1]) if '--top' in sys.argv else 25
O, N = load(old_p), load(new_p)
keys = sorted(set(O) | set(N))
rows = []
for k in keys:
    a, b = O.get(k), N.get(k)
    if a is None or b is None:
        print('POPULATION CHANGE: %s %s' % (k, 'added' if a is None else 'dropped'))
        continue
    if a['v'] != b['v']:
        rows.append(dict(key=k, old=a['v'], new=b['v'], d=b['v'] - a['v'],
                         cg=a.get('cg') or 0, yr=a.get('yr'), ty=a.get('ty'), pk=a.get('pk'),
                         gf=a.get('gf'), age=a.get('age')))
tot_o = sum(r['v'] for r in O.values()); tot_n = sum(r['v'] for r in N.values())
print('MOVERS %s' % LABEL)
print('  old %s  total %d' % (old_p.split("/")[-1], tot_o))
print('  new %s  total %d  (delta %+d, %+.4f%%)' % (new_p.split("/")[-1], tot_n, tot_n - tot_o,
                                                    100.0 * (tot_n - tot_o) / tot_o))
print('  movers %d of %d   sum delta %+d' % (len(rows), len(keys), sum(r['d'] for r in rows)))
cls = collections.Counter()
csum = collections.Counter()
for r in rows:
    c = '0' if r['cg'] == 0 else ('1-2' if r['cg'] <= 2 else ('3-5' if r['cg'] <= 5 else
        ('6-10' if r['cg'] <= 10 else ('11-15' if r['cg'] <= 15 else '16+'))))
    cls[c] += 1; csum[c] += r['d']
print('  by career-games class:')
for c in ('0', '1-2', '3-5', '6-10', '11-15', '16+'):
    if cls[c]:
        print('     cg %-6s movers %4d   sum %+9d' % (c, cls[c], csum[c]))
tc = collections.Counter(); ts = collections.Counter()
for r in rows:
    tc[r['ty']] += 1; ts[r['ty']] += r['d']
print('  by entry type: %s' % ', '.join('%s %d(%+d)' % (t, tc[t], ts[t]) for t in sorted(tc, key=str)))
print('  LARGEST %d MOVES' % TOP)
print('  %-26s %8s %8s %9s %5s %5s %5s %4s' % ('key', 'old', 'new', 'delta', 'cg', 'yr', 'ty', 'pk'))
for r in sorted(rows, key=lambda x: -abs(x['d']))[:TOP]:
    print('  %-26s %8d %8d %+9d %5d %5s %5s %4s' % (r['key'], r['old'], r['new'], r['d'], r['cg'],
                                                    r['yr'], r['ty'], r['pk']))
if '--json' in sys.argv:
    out = sys.argv[sys.argv.index('--json') + 1]
    json.dump(dict(label=LABEL, old=old_p, new=new_p, total_old=tot_o, total_new=tot_n,
                   n_movers=len(rows), sum_delta=sum(r['d'] for r in rows), rows=rows),
              open(out, 'w'), indent=1, sort_keys=True)
    print('  wrote %s' % out)
