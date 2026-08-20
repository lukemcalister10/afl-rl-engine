"""Blast radius of ONE candidate fix, measured but NOT implemented in the engine.

CANDIDATE FIX B: re-apply the house isotonic instrument (already used three times in this engine) to the
conditional-prior band ALONG THE LEVEL AXIS — for each quantile model q, force cm[q].predict to be
non-decreasing in feature 9 at the row's own other features. Everything else untouched.
Measured here in scratch, on the shipped board population, with the engine unmodified.
"""
import copy, json, os, numpy as np
from sklearn.isotonic import IsotonicRegression

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']; price6 = G['price6']
F = 1.052329
Y = 2026
QK = sorted(cm.keys())
SP = os.path.dirname(os.path.dirname(OUTBASE))

board = json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))
if isinstance(board, dict):
    for k in ('players', 'rows', 'data'):
        if k in board and isinstance(board[k], list):
            board = board[k]; break
bkeys = set()
for r in board:
    if isinstance(r, dict):
        for k in ('key', 'id', 'player_key', 'slug'):
            if r.get(k):
                bkeys.add(r[k]); break
print('board rows=%d  keys=%d' % (len(board), len(bkeys)))

GRID = np.arange(40.0, 120.01, 0.5)


def bands_on_grid(feat):
    X = np.tile(np.array(feat, float), (len(GRID), 1))
    X[:, 9] = GRID
    raw = {q: cm[q].predict(X) for q in QK}
    raw97 = q97m.predict(X)
    iso = {q: IsotonicRegression(increasing=True, out_of_bounds='clip').fit_transform(GRID, raw[q]) for q in QK}
    iso97 = IsotonicRegression(increasing=True, out_of_bounds='clip').fit_transform(GRID, raw97)
    return raw, raw97, iso, iso97


def band_at_idx(raw, raw97, i):
    b = np.sort(np.array([raw[q][i] for q in QK]))
    return list(b) + [max(float(raw97[i]), float(b[4]))]


def band_iso_idx(iso, iso97, i):
    b = np.sort(np.array([iso[q][i] for q in QK]))
    return list(b) + [max(float(iso97[i]), float(b[4]))]


pop = [p for p in MA.data if p.get('key') in bkeys] if bkeys else \
      [p for p in MA.data if not G['delisted'](p)]
print('population priced here: n=%d' % len(pop))

res = []
for p in pop:
    try:
        feat = [float(x) for x in cp._feat(p, Y)]
        L = feat[9]
        if not (GRID[0] <= L <= GRID[-1]):
            res.append({'player': p['player'], 'key': p.get('key'), 'L': L, 'skip': 'L out of grid'})
            continue
        raw, raw97, iso, iso97 = bands_on_grid(feat)
        i = int(np.argmin(np.abs(GRID - L)))
        b0 = band_at_idx(raw, raw97, i)
        b1 = band_iso_idx(iso, iso97, i)
        v0 = float(price6(p, b0, Y)); v1 = float(price6(p, b1, Y))
        g26 = sum(x['games'] for x in p['scoring'] if x['year'] == Y)
        res.append({'player': p['player'], 'key': p.get('key'), 'L': L, 'g26': g26,
                    'pos': MA.gfut(p), 'pk': MA.effpk(p), 'v_ship': float(ev(p, Y) / F),
                    'price6_raw': v0, 'price6_iso': v1,
                    'dpct': (v1 - v0) / v0 * 100.0 if v0 else 0.0,
                    'band_raw': b0, 'band_iso': b1})
    except Exception as e:
        res.append({'player': p['player'], 'key': p.get('key'), 'err': str(e)})

ok = [r for r in res if 'dpct' in r]
print('measured n=%d  errors=%d' % (len(ok), len(res) - len(ok)))
d = np.array([r['dpct'] for r in ok])
print('price6 change under FIX B (isotonic-in-level band):')
print('  median %+.2f%%   mean %+.2f%%   p90 %+.2f%%   p99 %+.2f%%   max %+.2f%%'
      % (np.median(d), d.mean(), np.percentile(d, 90), np.percentile(d, 99), d.max()))
for bar in (0.5, 1, 2, 5, 10, 20):
    print('  rows moving >%4.1f%%: %4d of %d (%.1f%%)' % (bar, int((d > bar).sum()), len(d), 100 * (d > bar).mean()))
print('  rows unmoved (<0.05%%): %d' % int((d < 0.05).sum()))
print()
print('  by 2026 games:')
for lo, hi in [(0, 0), (1, 4), (5, 13), (14, 21), (22, 40)]:
    s = [r['dpct'] for r in ok if lo <= r['g26'] <= hi]
    if s:
        print('    g %2d-%2d n=%4d  median %+6.2f%%  p90 %+7.2f%%  max %+7.2f%%'
              % (lo, hi, len(s), np.median(s), np.percentile(s, 90), max(s)))
print('  by level feature:')
for lo, hi in [(40, 50), (50, 60), (60, 70), (70, 80), (80, 95), (95, 120)]:
    s = [r['dpct'] for r in ok if lo <= r['L'] < hi]
    if s:
        print('    L %3d-%3d n=%4d  median %+6.2f%%  p90 %+7.2f%%  max %+7.2f%%'
              % (lo, hi, len(s), np.median(s), np.percentile(s, 90), max(s)))
print()
print('  top 25 movers:')
for r in sorted(ok, key=lambda r: -r['dpct'])[:25]:
    print('    %-26s g26=%-3d L=%6.2f v=%8.1f  price6 %8.1f -> %8.1f  %+6.2f%%'
          % (r['player'], r['g26'], r['L'], r['v_ship'], r['price6_raw'], r['price6_iso'], r['dpct']))

# ---- does FIX B remove the trough? re-sweep the four rows with the isotonic band ----
print()
print('=== DOES FIX B REMOVE THE TROUGH? (band-only sweep, raw vs isotonic) ===')
R22 = {q.get('key'): q for q in json.load(open(os.path.join(SP, 'store_r22.json')))}
for nm in ['Max Kondogiannis', 'Josh Dolan', 'Charlie West', 'Will Hayes']:
    p = next(x for x in MA.data if x['player'] == nm)
    q = R22[p['key']]; rq = next(x for x in q['scoring'] if x['year'] == Y)
    g0, a0 = rq['games'], rq['avg']
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == Y)
    Ls = []
    for sc in range(0, 151):
        row['games'] = g0 + 1; row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        Ls.append(float(cp._feat(p, Y)[9]))
    p['scoring'] = saved
    feat = [float(x) for x in cp._feat(p, Y)]
    raw, raw97, iso, iso97 = bands_on_grid(feat)
    vr, vi = [], []
    for L in Ls:
        i = int(np.argmin(np.abs(GRID - L)))
        vr.append(float(price6(p, band_at_idx(raw, raw97, i), Y)))
        vi.append(float(price6(p, band_iso_idx(iso, iso97, i), Y)))

    def md(v):
        mx = v[0]; w = 0.0
        for x in v[1:]:
            mx = max(mx, x); w = max(w, (mx - x) / mx)
        return w
    print('  %-18s raw maxdrop %5.1f%%   isotonic maxdrop %5.1f%%   (shipped-score price6 %.1f -> %.1f)'
          % (nm, 100 * md(vr), 100 * md(vi), vr[0], vi[0]))
    print('     score  ' + ' '.join('%7d' % s for s in range(0, 151, 15)))
    print('     raw    ' + ' '.join('%7.1f' % vr[s] for s in range(0, 151, 15)))
    print('     iso    ' + ' '.join('%7.1f' % vi[s] for s in range(0, 151, 15)))

json.dump(res, open(OUTBASE + '.json', 'w'), indent=1, default=str)
print('WROTE', OUTBASE + '.json')
