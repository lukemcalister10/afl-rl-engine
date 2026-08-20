"""BAND-ONLY PREDICTION across the thin-evidence population.

Predicted price = price6(p_at_shipped_scoring, band(L(score)), Y): the player's own row is HELD at the
shipped state so v_at_peak's continuous inputs are frozen; ONLY the conditional-prior band moves.
If that reproduces the trough, the band model IS the site.
"""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']; price6 = G['price6']
F = 1.052329
Y = 2026
QK = sorted(cm.keys())
SP = os.path.dirname(os.path.dirname(OUTBASE))
_raw = json.load(open(os.path.join(SP, 'store_r22.json')))
R22 = {p.get('key') or p.get('player'): p for p in _raw}
print('R22 store rows=%d' % len(R22))


def band_at(feat, L):
    f = list(feat); f[9] = float(L)
    a = np.array([f])
    b = np.sort(np.array([float(cm[q].predict(a)[0]) for q in QK]))
    return list(b) + [max(float(q97m.predict(a)[0]), float(b[4]))]


def prior_row(p):
    q = R22.get(p['key'])
    if not q:
        return None
    r = [x for x in q['scoring'] if x['year'] == Y]
    if not r:
        return None
    return r[0]['games'], r[0]['avg']


SCORES = list(range(0, 151))
cands = []
for p in MA.data:
    r = [x for x in p['scoring'] if x['year'] == Y]
    if not r:
        continue
    g = r[0]['games']; a = r[0]['avg']
    if not (5 <= g <= 13) or G['delisted'](p):
        continue
    pr = prior_row(p)
    if pr is None or pr[0] != g - 1:
        continue            # must have played exactly round 23
    g0, a0 = pr
    cands.append((p, g0, a0, g, a, round(g * a - g0 * a0)))
print('POPULATION (5-13 games in 2026 AND played round 23): n=%d' % len(cands))

res = {}
for p, g0, a0, g, a, actual in cands:
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == Y)
    Ls = []
    for sc in SCORES:
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        Ls.append(float(cp._feat(p, Y)[9]))
    feat0 = [float(x) for x in cp._feat(p, Y)]
    p['scoring'] = saved                       # restore: v_at_peak inputs frozen at the SHIPPED row
    pv = []
    for L in Ls:
        pv.append(float(price6(p, band_at(feat0, L), Y)))
    # non-monotonicity of the BAND-ONLY predicted price
    worst = (0.0, None, None)
    run = pv[0]; runs = 0
    for i in range(len(pv)):
        for j in range(i + 1, len(pv)):
            pass
    # O(n) running-max drop
    mx = pv[0]; mxi = 0
    for j in range(1, len(pv)):
        if pv[j] > mx:
            mx = pv[j]; mxi = j
        d = (mx - pv[j]) / mx
        if d > worst[0]:
            worst = (d, SCORES[mxi], SCORES[j])
    res[p['player']] = {'key': p['key'], 'g': g, 'avg': a, 'a0': a0, 'actual_r23': actual,
                        'pos': MA.gfut(p), 'pk': MA.effpk(p), 'v': round(ev(p, Y) / F, 1),
                        'L': Ls, 'pv': pv, 'worst_drop': worst[0], 'worst_from': worst[1], 'worst_to': worst[2]}

rank = sorted(res.items(), key=lambda kv: -kv[1]['worst_drop'])
print()
print('BAND-ONLY PREDICTED NON-MONOTONICITY (max drop in predicted price as the round score RISES):')
print('%-26s %4s %7s %7s %6s %8s   %s' % ('player', 'g', 'prioravg', 'r23', 'v', 'maxdrop', 'from->to score'))
for nm, d in rank:
    print('%-26s %4d %7.2f %7d %6.0f %7.1f%%   %d -> %d' %
          (nm, d['g'], d['a0'], d['actual_r23'], d['v'], 100 * d['worst_drop'], d['worst_from'], d['worst_to']))

json.dump(res, open(OUTBASE + '.json', 'w'), indent=1, default=str)
print('WROTE', OUTBASE + '.json')
