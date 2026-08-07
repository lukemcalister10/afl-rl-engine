import json, sys, collections
import numpy as np

A = json.load(open(sys.argv[1]))   # old board
B = json.load(open(sys.argv[2]))   # new board


def rows(d):
    r = d['active'] if isinstance(d, dict) and 'active' in d else d
    if isinstance(r, dict):
        r = list(r.values())
    return r


ra = {p['key']: p for p in rows(A) if p.get('v') is not None}
rb = {p['key']: p for p in rows(B) if p.get('v') is not None}
ks = sorted(set(ra) & set(rb))
print('keys old=%d new=%d shared=%d  only_old=%s only_new=%s'
      % (len(ra), len(rb), len(ks), sorted(set(ra) - set(rb))[:5], sorted(set(rb) - set(ra))[:5]))

mv = [(k, ra[k]['v'], rb[k]['v']) for k in ks if ra[k]['v'] != rb[k]['v']]
ta, tb = sum(ra[k]['v'] for k in ks), sum(rb[k]['v'] for k in ks)
print('MOVERS %d of %d (%.2f%%)  cuts %d  lifts %d'
      % (len(mv), len(ks), 100.0 * len(mv) / len(ks),
         sum(1 for _, a, b in mv if b < a), sum(1 for _, a, b in mv if b > a)))
print('TOTAL %d -> %d  ratio %.6f  delta %d' % (ta, tb, tb / ta, tb - ta))
rel = [abs(b - a) / a for k, a, b in [(k, ra[k]['v'], rb[k]['v']) for k in ks] if a > 0]
print('mean |relative move| board-wide %.4f%%' % (100 * float(np.mean(rel))))
relm = [abs(b - a) / a for _, a, b in mv if a > 0]
if relm:
    print('mean |relative move| movers   %.4f%%' % (100 * float(np.mean(relm))))

mv.sort(key=lambda t: t[2] - t[1])
print('\nTOP 10 CUTS')
for k, a, b in mv[:10]:
    print('  %-28s %6d -> %6d  %+6d  %+7.2f%%' % (k, a, b, b - a, 100.0 * (b - a) / a))
print('TOP 10 LIFTS')
for k, a, b in list(reversed(mv))[:10]:
    print('  %-28s %6d -> %6d  %+6d  %+7.2f%%' % (k, a, b, b - a, 100.0 * (b - a) / a))


def agebucket(p):
    a = p.get('age')
    if a is None:
        return 'unknown'
    a = float(a)
    return '<=22' if a <= 22 else ('23-26' if a <= 26 else '>=27')


print('\nAGE BUCKETS')
g = collections.defaultdict(lambda: [0, 0, 0, 0])
for k in ks:
    b = agebucket(rb[k]); g[b][0] += ra[k]['v']; g[b][1] += rb[k]['v']; g[b][2] += 1
    if ra[k]['v'] != rb[k]['v']:
        g[b][3] += 1
for b in ('<=22', '23-26', '>=27', 'unknown'):
    if b in g:
        o, n, c, m = g[b]
        print('  %-8s n=%4d movers=%4d  total %7d -> %7d  ratio %.6f' % (b, c, m, o, n, n / o))
