"""CONFIRMATION: true ev() sweeps for the three predicted rows + four negative controls."""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']; price6 = G['price6']
F = 1.052329
Y = 2026
QK = sorted(cm.keys())
SP = os.path.dirname(os.path.dirname(OUTBASE))
R22 = {p.get('key'): p for p in json.load(open(os.path.join(SP, 'store_r22.json')))}

TARGETS = ['Billy Cootee', 'Charlie West', 'Will Hayes',
           'Marcus Herbert', 'Mark Keane', 'Sam Lalor', 'Will Day',
           'Max Kondogiannis', 'Josh Dolan']
SCORES = list(range(0, 151))


def band_at(feat, L):
    f = list(feat); f[9] = float(L)
    a = np.array([f])
    b = np.sort(np.array([float(cm[q].predict(a)[0]) for q in QK]))
    return list(b) + [max(float(q97m.predict(a)[0]), float(b[4]))]


def maxdrop(v):
    mx = v[0]; mxi = 0; w = (0.0, 0, 0)
    for j in range(1, len(v)):
        if v[j] > mx:
            mx = v[j]; mxi = j
        d = (mx - v[j]) / mx
        if d > w[0]:
            w = (d, mxi, j)
    return w


out = {}
for nm in TARGETS:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        print('MISSING', nm); continue
    r = next(x for x in p['scoring'] if x['year'] == Y)
    q = R22.get(p['key'])
    rq = next(x for x in q['scoring'] if x['year'] == Y)
    g0, a0 = rq['games'], rq['avg']
    shipped = ev(p, Y) / F
    saved = copy.deepcopy(p['scoring'])
    # ---- band-only predictor (row frozen at shipped) ----
    Ls = []
    for sc in SCORES:
        r['games'] = g0 + 1
        r['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        Ls.append(float(cp._feat(p, Y)[9]))
    p['scoring'] = copy.deepcopy(saved)
    r = next(x for x in p['scoring'] if x['year'] == Y)
    feat0 = [float(x) for x in cp._feat(p, Y)]
    pred = [float(price6(p, band_at(feat0, L), Y)) for L in Ls]
    # ---- TRUE ev() sweep ----
    true = []
    for sc in SCORES:
        r['games'] = g0 + 1
        r['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        true.append(ev(p, Y) / F)
    p['scoring'] = saved
    back = ev(p, Y) / F
    dp_, dpi, dpj = maxdrop(pred)
    dt_, dti, dtj = maxdrop(true)
    out[nm] = {'g0': g0, 'a0': a0, 'shipped': shipped, 'restored': back, 'rt': abs(shipped - back) < 1e-9,
               'L': Ls, 'pred': pred, 'true': true,
               'pred_drop': dp_, 'pred_from': dpi, 'pred_to': dpj,
               'true_drop': dt_, 'true_from': dti, 'true_to': dtj,
               'corr': float(np.corrcoef(pred, true)[0, 1])}
    print('%-20s g0=%-3d a0=%-6.2f shipped=%8.1f rt=%s  |  BAND-ONLY maxdrop %5.1f%% (%d->%d)   '
          'TRUE maxdrop %5.1f%% (%d->%d)   corr(pred,true)=%.3f'
          % (nm, g0, a0, shipped, out[nm]['rt'], 100 * dp_, dpi, dpj, 100 * dt_, dti, dtj, out[nm]['corr']))

print()
print('NAMED PREDICTIONS vs OUTCOME')
for nm, s1, s2 in [('Billy Cootee', 7, 15), ('Charlie West', 59, 110), ('Will Hayes', 0, 35)]:
    d = out[nm]
    tp = 100 * (d['true'][s1] - d['true'][s2]) / d['true'][s1]
    pp = 100 * (d['pred'][s1] - d['pred'][s2]) / d['pred'][s1]
    print('  %-16s score %3d -> %3d :  band-only predicted %+6.1f%%   TRUE %+6.1f%%   '
          '(true v %.1f -> %.1f)' % (nm, s1, s2, pp, tp, d['true'][s1], d['true'][s2]))

print()
for nm in TARGETS:
    d = out[nm]
    print('== %s  (prior %d g @ %.2f)' % (nm, d['g0'], d['a0']))
    print('   score:  ' + ' '.join('%7d' % s for s in range(0, 151, 10)))
    print('   TRUE :  ' + ' '.join('%7.1f' % d['true'][s] for s in range(0, 151, 10)))
    print('   BAND :  ' + ' '.join('%7.1f' % d['pred'][s] for s in range(0, 151, 10)))

json.dump(out, open(OUTBASE + '.json', 'w'), indent=1, default=str)
print('WROTE', OUTBASE + '.json')
