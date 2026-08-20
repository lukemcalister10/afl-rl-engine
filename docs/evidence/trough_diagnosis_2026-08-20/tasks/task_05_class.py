"""(a) why Billy Cootee is immune; (b) TRUE ev() max-drop for all 86; (c) what predicts susceptibility."""
import copy, json, os, numpy as np

MA = G['MA']; ev = G['ev']; cp = G['cp']; PR = G['PR']
price6 = G['price6']
F = 1.052329
Y = 2026
SP = os.path.dirname(os.path.dirname(OUTBASE))
R22 = {p.get('key'): p for p in json.load(open(os.path.join(SP, 'store_r22.json')))}


def terms(p):
    d = {}

    def t(k, fn):
        try:
            d[k] = float(fn())
        except Exception as e:
            d[k] = 'ERR:%s' % e
    t('ev', lambda: ev(p, Y))
    t('ev_prefloor', lambda: G['ev_prefloor'](p, Y))
    t('ev_click', lambda: G['_ev_click'](p, Y))
    t('prod_path', lambda: G['_prod_path'](p, Y))
    t('raw_ev', lambda: G['raw_ev'](p, Y))
    t('price6', lambda: G['price6'](p, G['b6'](p, Y), Y))
    t('iso_eff', lambda: G['iso_eff'](p, Y))
    t('v0_start', lambda: G['v0_start'](p))
    t('entry_anchor', lambda: G['entry_anchor'](p))
    t('h_cut', lambda: G['_h_cut'](p, Y))
    d['nseas_pro'] = G['nseas_pro'](p, Y)
    d['tenure'] = PR.tenure(p, Y)
    d['type'] = p.get('type'); d['pool'] = bool(p.get('_pool')); d['pickless'] = bool(p.get('_pickless'))
    yis = Y - int(p.get('year') or 0)
    d['yis'] = yis
    try:
        d['floor'] = float(G['floor_frac'](yis) * G['entry_anchor'](p))
    except Exception as e:
        d['floor'] = 'ERR:%s' % e
    # the D8 / mediocre staleness caps
    try:
        pos = MA.gfut(p); el = d['tenure']; ns = d['nseas_pro']
        keyruc = pos in ('KPF', 'KPD', 'RUCK'); onset = (4 if keyruc else 3)
        d['stale_branch'] = ('D8' if (el >= onset and ns <= 1) else
                             ('MEDIOCRE' if (el >= onset + 2) else 'none'))
        if el >= onset and ns <= 1:
            frac = 0.25 * max(0.4, 1 - 0.10 * (el - onset)) * (1.6 if keyruc else 1.0)
            d['stale_cap'] = float(G['v0_start'](p) * frac)
            d['stale_grade'] = float(G['_staleness_grade'](p, Y, pos))
    except Exception as e:
        d['stale_err'] = str(e)
    # does MA.prod_floor bind inside v_at_peak?
    try:
        dp = G['dp']; bb = G['b6'](p, Y)
        binds = []
        for L in bb:
            pf = float(MA.prod_floor(p, 'bal'))
            raw = float(MA.val(MA.proj_from_peak(MA.gfut(p), float(L), MA.age(p), MA.level_now(p), 'bal',
                                                 g0=MA.bnow(p), fut=MA.futblend(p),
                                                 pre_hc=p.get('_avail_hc', 0.0), grace=MA.grace_years(p))))
            binds.append(pf > raw)
        d['prodfloor_binds'] = binds
    except Exception as e:
        d['prodfloor_err'] = str(e)
    return d


print('=== (a) TERM CENSUS at the shipped row ===')
for nm in ['Billy Cootee', 'Charlie West', 'Will Hayes', 'Max Kondogiannis', 'Josh Dolan',
           'Harvey Harrison', 'Conor Stone', 'Marcus Herbert']:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        continue
    d = terms(p)
    print('%-20s ev=%8.1f prefloor=%8.1f click=%8.1f prod=%8.1f raw=%8.1f price6=%8.1f  '
          'floor=%8.1f (%s) v0=%7.1f anchor=%7.1f ten=%s ns=%s stale=%s%s  pfbinds=%s'
          % (nm, d['ev'], d['ev_prefloor'], d['ev_click'], d['prod_path'], d['raw_ev'], d['price6'],
             d['floor'] if isinstance(d['floor'], float) else -1,
             'BINDS' if (isinstance(d['floor'], float) and d['floor'] > d['ev_prefloor']) else 'inert',
             d['v0_start'], d['entry_anchor'], d['tenure'], d['nseas_pro'], d.get('stale_branch'),
             (' cap=%.1f grade=%.2f' % (d.get('stale_cap', -1), d.get('stale_grade', -1))
              if 'stale_cap' in d else ''),
             d.get('prodfloor_binds')))

print()
print('=== (b) TRUE ev() sweep, all 86 ===')
SCORES = list(range(0, 151, 2))
rows = []
for p in MA.data:
    r = [x for x in p['scoring'] if x['year'] == Y]
    if not r:
        continue
    g = r[0]['games']
    if not (5 <= g <= 13) or G['delisted'](p):
        continue
    q = R22.get(p['key'])
    if not q:
        continue
    rq = [x for x in q['scoring'] if x['year'] == Y]
    if not rq or rq[0]['games'] != g - 1:
        continue
    g0, a0 = rq[0]['games'], rq[0]['avg']
    shipped = ev(p, Y) / F
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == Y)
    v = []
    for sc in SCORES:
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        v.append(ev(p, Y) / F)
    p['scoring'] = saved
    back = ev(p, Y) / F
    mx = v[0]; mxi = 0; w = (0.0, 0, 0)
    for j in range(1, len(v)):
        if v[j] > mx:
            mx = v[j]; mxi = j
        dd = (mx - v[j]) / mx
        if dd > w[0]:
            w = (dd, SCORES[mxi], SCORES[j])
    d = terms(p)
    actual = round(g * r[0]['avg'] - g0 * a0)
    fl = d['floor'] if isinstance(d['floor'], float) else -1
    rows.append({'player': p['player'], 'g': g, 'a0': a0, 'actual': actual, 'pos': MA.gfut(p),
                 'pk': MA.effpk(p), 'v': shipped, 'rt': abs(shipped - back) < 1e-9,
                 'lvl': float(cp._feat(p, Y)[9]), 'drop': w[0], 'from': w[1], 'to': w[2],
                 'floor_binds': fl > d['ev_prefloor'], 'stale': d.get('stale_branch'),
                 'price6': d['price6'], 'ev_eng': d['ev'], 'sweep': v})

rows.sort(key=lambda r: -r['drop'])
print('%-24s %3s %7s %5s %6s %8s %8s %8s %s' %
      ('player', 'g', 'prioravg', 'r23', 'lvl', 'v', 'MAXDROP', 'from->to', 'floor/stale'))
for r in rows:
    print('%-24s %3d %7.2f %5d %6.2f %8.1f %7.1f%%  %3d->%-3d  %s%s' %
          (r['player'], r['g'], r['a0'], r['actual'], r['lvl'], r['v'], 100 * r['drop'],
           r['from'], r['to'], 'FLOORED ' if r['floor_binds'] else '', r['stale'] or ''))
print('rt all True: %s' % all(r['rt'] for r in rows))
n = len(rows)
for bar in (0.05, 0.10, 0.20, 0.30):
    print('  rows with a >%.0f%% true score->price drop: %d of %d (%.1f%%)'
          % (100 * bar, sum(1 for r in rows if r['drop'] > bar), n, 100 * sum(1 for r in rows if r['drop'] > bar) / n))
print('  median max-drop %.1f%%' % (100 * np.median([r['drop'] for r in rows])))
# susceptibility drivers
import math
print()
print('=== (c) drivers ===')
for key, lab in [('g', 'games'), ('a0', 'prior avg'), ('lvl', 'level feature'), ('v', 'board value')]:
    xs = np.array([r[key] for r in rows], float); ys = np.array([r['drop'] for r in rows], float)
    print('  corr(drop, %-14s) = %+.3f' % (lab, float(np.corrcoef(xs, ys)[0, 1])))
    print('  corr(drop, log %-10s) = %+.3f' % (lab, float(np.corrcoef(np.log(np.maximum(xs, 1e-6)), ys)[0, 1])))
fl = [r for r in rows if r['floor_binds']]
print('  floored rows: n=%d  median drop %.1f%%' % (len(fl), 100 * np.median([r['drop'] for r in fl]) if fl else -1))
nf = [r for r in rows if not r['floor_binds']]
print('  unfloored   : n=%d  median drop %.1f%%' % (len(nf), 100 * np.median([r['drop'] for r in nf])))

json.dump(rows, open(OUTBASE + '.json', 'w'), indent=1, default=str)
print('WROTE', OUTBASE + '.json')
