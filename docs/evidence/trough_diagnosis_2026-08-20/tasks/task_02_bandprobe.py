"""Isolate the band model as a 1-D step function of the level feature, and find candidate 3rd players."""
import copy, json, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']; PR = G['PR']
cm = G['cm']; q97m = G['q97m']
F = 1.052329
Y = 2026
Q = None
import sys
# Q keys of the band model
Qkeys = sorted(cm.keys()) if isinstance(cm, dict) else None
print('cm type=%r keys=%r' % (type(cm), Qkeys))
m0 = cm[Qkeys[0]] if Qkeys else None
print('member type=%r' % type(m0))
try:
    print('n_estimators=%r max_depth=%r' % (m0.n_estimators, m0.max_depth))
except Exception as e:
    print('meta err', e)

# ---- how many distinct split thresholds does the ensemble carry on feature 9 (the level)? ----
for qk in (Qkeys or []):
    mm = cm[qk]
    th = []
    for est in np.asarray(mm.estimators_).ravel():
        t = est.tree_
        th += [float(x) for f, x in zip(t.feature, t.threshold) if f == 9]
    th = sorted(set(round(x, 6) for x in th))
    print('q=%r  feature-9 split thresholds: n=%d  range=[%.3f,%.3f]' % (qk, len(th), th[0], th[-1]))
try:
    th = []
    for est in np.asarray(q97m.estimators_).ravel():
        t = est.tree_
        th += [float(x) for f, x in zip(t.feature, t.threshold) if f == 9]
    th = sorted(set(round(x, 6) for x in th))
    print('q97m  feature-9 split thresholds: n=%d  range=[%.3f,%.3f]' % (len(th), th[0], th[-1]))
except Exception as e:
    print('q97m meta err', e)


def band_at(feat, L):
    f = list(feat); f[9] = float(L)
    a = np.array([f])
    b = np.sort(np.array([float(cm[q].predict(a)[0]) for q in Qkeys]))
    return list(b) + [max(float(q97m.predict(a)[0]), float(b[4]))]


def breakpoints(feat, lo, hi, step=0.002):
    Ls = np.arange(lo, hi + step, step)
    prev = None; bps = []
    for L in Ls:
        b = band_at(feat, L)
        if prev is not None and any(abs(x - y) > 1e-9 for x, y in zip(b, prev)):
            bps.append((float(L), [float(x - y) for x, y in zip(b, prev)]))
        prev = b
    return bps


out = {}
for nm, g0, a0 in [('Max Kondogiannis', 9, 36.6), ('Josh Dolan', 9, 50.09)]:
    p = next(x for x in MA.data if x['player'] == nm)
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == Y)
    # score -> level map
    smap = []
    for sc in range(0, 151):
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        f = [float(x) for x in cp._feat(p, Y)]
        smap.append((sc, f[9], f))
    p['scoring'] = saved
    feat0 = smap[0][2]
    lo, hi = smap[0][1], smap[-1][1]
    bps = breakpoints(feat0, lo - 0.01, hi + 0.01)
    print('== %s  level window [%.4f, %.4f]  band breakpoints n=%d' % (nm, lo, hi, len(bps)))
    # map breakpoints back to score
    for L, d in bps:
        sc = (L - smap[0][1]) / ((smap[-1][1] - smap[0][1]) / 150.0)
        print('   L=%.4f  (score~%.2f)   dband=%s' % (L, sc, ' '.join('%+.2f' % x for x in d)))
    out[nm] = {'smap': [(s, l) for s, l, _ in smap], 'bps': bps, 'feat0': feat0}

json.dump(out, open(OUTBASE + '.json', 'w'), indent=1, default=str)

# ---- the thin-evidence population (5..13 games in 2026), for the 3rd-player prediction ----
pop = []
for p in MA.data:
    r = [x for x in p['scoring'] if x['year'] == Y]
    g = sum(x['games'] for x in r)
    if 5 <= g <= 13 and not G['delisted'](p):
        try:
            v = ev(p, Y) / F
        except Exception:
            continue
        pop.append((p['player'], p.get('key'), g, r[0]['avg'], MA.gfut(p), MA.effpk(p), round(v, 1),
                    round(float(cp._feat(p, Y)[9]), 4)))
print('THIN-EVIDENCE POPULATION n=%d' % len(pop))
for t in sorted(pop, key=lambda t: -t[6])[:120]:
    print('   %-26s g=%-3d avg=%-6.2f pos=%-5s pk=%-4s v=%-8.1f lvl=%.4f' % (t[0], t[2], t[3], t[4], t[5], t[6], t[7]))
