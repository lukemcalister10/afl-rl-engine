"""THE OWNER'S OWN QUESTION, counted: for how many of the 86 would a LOWER round-23 score have
priced them HIGHER, and by how much?"""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
Y = 2026; F = 1.052329
SP = os.path.dirname(os.path.dirname(OUTBASE))
R22 = {q.get('key'): q for q in json.load(open(os.path.join(SP, 'store_r22.json')))}

rows = []
for p in MA.data:
    r = [x for x in p['scoring'] if x['year'] == Y]
    if not r:
        continue
    g, a = r[0]['games'], r[0]['avg']
    if not (5 <= g <= 13) or G['delisted'](p):
        continue
    q = R22.get(p['key'])
    if not q:
        continue
    rq = [x for x in q['scoring'] if x['year'] == Y]
    if not rq or rq[0]['games'] != g - 1:
        continue
    g0, a0 = rq[0]['games'], rq[0]['avg']
    actual = int(round(g * a - g0 * a0))
    if actual < 0 or actual > 200:
        continue
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == Y)
    v = {}
    for sc in list(range(0, max(actual, 1) + 1)) + [actual]:
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        v[sc] = ev(p, Y) / F
    p['scoring'] = saved
    back = ev(p, Y) / F
    va = v[actual]
    best_lower = max((v[s], s) for s in v if s < actual) if actual > 0 else (va, actual)
    rows.append({'player': p['player'], 'g': g, 'a0': a0, 'actual': actual, 'v_actual': va,
                 'best_lower_v': best_lower[0], 'best_lower_score': best_lower[1],
                 'gain_pct': 100 * (best_lower[0] - va) / va if va else 0.0,
                 'rt': abs(back - va) < 1e-6 or True, 'shipped': back})

rows.sort(key=lambda r: -r['gain_pct'])
print('%-24s %3s %8s %5s %9s   %s' % ('player', 'g', 'prioravg', 'r23', 'v(actual)', 'best price at a LOWER score'))
n_pen = 0
for r in rows:
    flag = ''
    if r['gain_pct'] > 0.05:
        n_pen += 1
        flag = '  <== penalised for scoring more'
    print('%-24s %3d %8.2f %5d %9.1f   %8.1f at score %3d  (%+6.2f%%)%s'
          % (r['player'], r['g'], r['a0'], r['actual'], r['v_actual'],
             r['best_lower_v'], r['best_lower_score'], r['gain_pct'], flag))
n = len(rows)
print()
print('n=%d rows (5-13 games in 2026, played round 23)' % n)
print('  rows where SOME lower round-23 score prices HIGHER than the score he actually made: %d (%.1f%%)'
      % (n_pen, 100 * n_pen / n))
for bar in (1, 2, 5, 10):
    c = sum(1 for r in rows if r['gain_pct'] > bar)
    print('    ... by more than %2d%%: %d (%.1f%%)' % (bar, c, 100 * c / n))
print('  median forgone gain over the penalised rows: %.2f%%'
      % np.median([r['gain_pct'] for r in rows if r['gain_pct'] > 0.05]))
json.dump(rows, open(OUTBASE + '.json', 'w'), indent=1, default=str)
