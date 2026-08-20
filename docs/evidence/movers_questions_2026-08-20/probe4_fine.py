"""Probe 4 — fine score sweep for the two young players, with the level/evidence internals at each point,
to locate the non-monotone steps exactly. READ-ONLY, no board build."""
import io, contextlib, copy, json, os, time

t0 = time.time()
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g['MA']; ev = g['ev']
print("LOADED %.1fs fE=%r" % (time.time() - t0, g['SEASON_FE']), flush=True)
F = 1.052329

get = lambda n: g.get(n)
out = {'fE': g['SEASON_FE']}

CASES = [('Max Kondogiannis', 9, 36.6), ('Josh Dolan', 9, 50.09), ('Lachlan Gulbin', 9, 45.0),
         ('Lachie Jaques', 9, 58.93)]

for nm, g0, a0 in CASES:
    p = next((x for x in MA.data if x['player'] == nm), None)
    if p is None:
        continue
    saved = copy.deepcopy(p['scoring'])
    row = next(x for x in p['scoring'] if x['year'] == 2026)
    rows = []
    for sc10 in range(0, 1401, 20):          # score 0 .. 140 in steps of 2
        sc = sc10 / 10.0
        row['games'] = g0 + 1
        row['avg'] = round((g0 * a0 + sc) / (g0 + 1), 4)
        rec = {'score': sc, 'avg': row['avg'], 'v': ev(p) / F}
        for fn, key in (('_lvlcurr', 'lvlcurr'), ('_par_prior', 'par')):
            try:
                rec[key] = get(fn)(p, 2026)
            except Exception:
                rec[key] = None
        for fn, key in (('bestlvl', 'bestlvl'), ('v0_start', 'v0')):
            try:
                rec[key] = get(fn)(p)
            except Exception:
                rec[key] = None
        try:
            rec['o31_cu'] = get('o31_cu')(p, 2026); rec['o31_D'] = get('o31_D')(p, 2026)
        except Exception:
            pass
        try:
            rec['delivered_2026'] = bool(get('o32_delivered')(p, 2026, row))
        except Exception as e:
            rec['delivered_2026'] = 'ERR:%s' % e
        try:
            rec['radq'] = bool(get('_radq')(p, 2026, get('_lvlcurr')(p, 2026)))
        except Exception:
            pass
        rows.append(rec)
    p['scoring'] = saved
    out[nm] = {'g0': g0, 'a0': a0, 'restored_v': ev(p) / F, 'rows': rows}
    # locate the biggest steps
    st = sorted(((rows[i + 1]['v'] - rows[i]['v'], rows[i]['score'], rows[i + 1]['score'],
                  rows[i]['avg'], rows[i + 1]['avg'], rows[i]['v'], rows[i + 1]['v'],
                  rows[i].get('delivered_2026'), rows[i + 1].get('delivered_2026'),
                  rows[i].get('o31_cu'), rows[i + 1].get('o31_cu'))
                 for i in range(len(rows) - 1)), key=lambda t: abs(t[0]), reverse=True)[:6]
    print("== %s  biggest single 2-point-score steps:" % nm, flush=True)
    for s in st:
        print("   score %5.1f->%5.1f  avg %6.2f->%6.2f   v %7.1f->%7.1f  (%+7.1f)  deliv %s->%s  cu %.4f->%.4f"
              % (s[1], s[2], s[3], s[4], s[5], s[6], s[0], s[7], s[8], s[9] or -1, s[10] or -1), flush=True)

json.dump(out, open(os.environ['PROBE_OUT'], 'w'), indent=1, default=str)
print("WROTE", os.environ['PROBE_OUT'], flush=True)
