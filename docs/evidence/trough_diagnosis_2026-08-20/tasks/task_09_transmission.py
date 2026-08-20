"""(a) why 7 of 37 grid steps missed: the demonstrated-production floor inside v_at_peak absorbs some
   band legs; (b) the transmission coefficient rho31(g) that bounds which rows the band can bite."""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']
cm = G['cm']; q97m = G['q97m']; price6 = G['price6']
Y = 2026; F = 1.052329
QK = sorted(cm.keys())
SP = os.path.dirname(os.path.dirname(OUTBASE))

print('=== (a) v_at_peak legs at the two "predicted move, actually bit-identical" breakpoints ===')
p = next(x for x in MA.data if x['player'] == 'Josh Dolan')
saved = copy.deepcopy(p['scoring'])
row = next(x for x in p['scoring'] if x['year'] == Y)
row['games'] = 10; row['avg'] = 49.88
feat0 = [float(x) for x in cp._feat(p, Y)]
dp = G['dp']
pf = float(MA.prod_floor(p, 'bal'))
print('  MA.prod_floor(Dolan) = %.3f' % pf)


def band_at(L):
    f = list(feat0); f[9] = float(L)
    a = np.array([f])
    b = np.sort(np.array([float(cm[q].predict(a)[0]) for q in QK]))
    return list(b) + [max(float(q97m.predict(a)[0]), float(b[4]))]


def legs(bb):
    o = []
    for L in bb:
        raw = float(MA.val(MA.proj_from_peak(MA.gfut(p), float(L), MA.age(p), MA.level_now(p), 'bal',
                                             g0=MA.bnow(p), fut=MA.futblend(p),
                                             pre_hc=p.get('_avail_hc', 0.0), grace=MA.grace_years(p))))
        o.append((raw, pf, pf > raw))
    return o


for Lb, La, lab in [(47.23396694 + 0.398049 * (46.90 - 46.0), 47.23396694 + 0.398049 * (46.94 - 46.0),
                     'the avg 46.921 breakpoint (bb[1] +0.116)')]:
    b0, b1 = band_at(Lb), band_at(La)
    print('  %s' % lab)
    print('     band before %s' % ' '.join('%.3f' % x for x in b0))
    print('     band after  %s' % ' '.join('%.3f' % x for x in b1))
    for i, ((r0, f0, bd0), (r1, f1, bd1)) in enumerate(zip(legs(b0), legs(b1))):
        print('     leg %d  v_at_peak raw %9.3f -> %9.3f   prod_floor %9.3f   floor binds: %s -> %s'
              % (i, r0, r1, f0, bd0, bd1))
    print('     price6 %.6f -> %.6f' % (price6(p, b0, Y), price6(p, b1, Y)))
p['scoring'] = saved

print()
print('=== (b) the transmission coefficient: price = rho31(g)*e + o31_pi(...)*ped + age_credit ===')
rho31 = G['rho31']; pv_games = G['pv_games']; pv_pedigree = G['pv_pedigree']; o31_pi = G['o31_pi']
prev = json.load(open(os.path.join(SP, 'tasks', 'task_05_class.json')))
drops = {r['player']: r['drop'] for r in prev}

rows = []
for p in MA.data:
    if G['delisted'](p) or not G['_isreal'](p) or not MA.GRP.get(p.get('pos')):
        continue
    try:
        g = pv_games(p, Y); ped = pv_pedigree(p)
        e = G['_prod_path'](p, Y) * G['_h_cut'](p, Y)
        prod = rho31(g) * float(e)
        pedleg = o31_pi(p, Y, g) * ped
        ac = G['o32_age_credit'](p, Y, g)
        tot = prod + pedleg + ac
        rows.append({'player': p['player'], 'pv_games': float(g), 'rho31': float(rho31(g)),
                     'prod_share': float(prod / tot) if tot else 0.0, 'L': float(cp._feat(p, Y)[9]),
                     'v': float(ev(p, Y) / F), 'g26': sum(x['games'] for x in p['scoring'] if x['year'] == Y)})
    except Exception as e:
        pass
print('rows=%d' % len(rows))
print('  rho31 by career-games band:')
for lo, hi in [(0, 0), (1, 5), (6, 12), (13, 25), (26, 50), (51, 100), (101, 400)]:
    s = [r for r in rows if lo <= r['pv_games'] <= hi]
    if s:
        print('    pv_games %3d-%3d n=%4d  median rho31 %.4f  median production share %.3f'
              % (lo, hi, len(s), np.median([r['rho31'] for r in s]), np.median([r['prod_share'] for r in s])))

named = {r['player']: r for r in rows}
print()
print('  the anchored/probe rows:')
for nm in ['Billy Cootee', 'Josh Dolan', 'Max Kondogiannis', 'Will Hayes', 'Charlie West',
           'Marcus Herbert', 'Sam Lalor', 'Will Day', 'Mark Keane']:
    r = named.get(nm)
    if r:
        print('    %-20s pv_games=%6.2f  rho31=%.4f  production share=%.3f  L=%6.2f  v=%8.1f  '
              'true sweep max-drop=%s'
              % (nm, r['pv_games'], r['rho31'], r['prod_share'], r['L'], r['v'],
                 ('%.1f%%' % (100 * drops[nm])) if nm in drops else 'n/a'))

s = [(r['prod_share'], drops[r['player']]) for r in rows if r['player'] in drops]
if s:
    a = np.array(s)
    print()
    print('  corr(production share, true score->price max-drop) over the 86 = %+.3f' %
          float(np.corrcoef(a[:, 0], a[:, 1])[0, 1]))
    lo = [d for ps, d in s if ps < 0.5]; hi = [d for ps, d in s if ps >= 0.5]
    print('  production share <0.5: n=%d median drop %.1f%%   >=0.5: n=%d median drop %.1f%%'
          % (len(lo), 100 * np.median(lo) if lo else -1, len(hi), 100 * np.median(hi) if hi else -1))

json.dump(rows, open(OUTBASE + '.json', 'w'), indent=1, default=str)
