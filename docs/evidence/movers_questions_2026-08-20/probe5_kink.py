"""Probe 5 — LOCALISE THE KINK. Dolan only, tight grid across the trough, minimal internals.

READ-ONLY, no board build. Trimmed from probe4_fine.py (which did 4 players x 71 points x 8
internals and did not finish under contention). Here: 1 player, 36 points, 3 cheap internals.
"""
import io, contextlib, copy, json, os, time

t0 = time.time()
g = {}
src = open('_merged_recover.py').read().split('print("=== AFTER')[0]
with contextlib.redirect_stdout(io.StringIO()):
    exec(src, g)
MA = g['MA']; ev = g['ev']
F = 1.052329
print("LOADED %.1fs fE=%r" % (time.time() - t0, g['SEASON_FE']), flush=True)

out = {'fE': g['SEASON_FE'], 'numeraire': F}

# Dolan: 2026 row is 9 games @ 50.09 before round 23; the 48 takes him to 10 @ 49.88.
# Sweep the RESULTING SEASON AVERAGE directly at fixed games=10, so the x-axis is the level itself.
p = next(x for x in MA.data if x['player'] == 'Josh Dolan')
saved = copy.deepcopy(p['scoring'])
row = next(x for x in p['scoring'] if x['year'] == 2026)

rows = []
avg = 46.0
while avg <= 53.5001:
    row['games'] = 10
    row['avg'] = round(avg, 3)
    rec = {'avg': row['avg'], 'v': ev(p) / F, 'score_implied': round(10 * avg - 9 * 50.09, 1)}
    for fn, key in (('_lvlcurr', 'lvlcurr'), ('bestlvl', 'bestlvl')):
        try:
            rec[key] = g[fn](p, 2026) if fn == '_lvlcurr' else g[fn](p)
        except Exception as e:
            rec[key] = 'ERR:%s' % e
    try:
        rec['radq'] = bool(g['_radq'](p, 2026, g['_lvlcurr'](p, 2026)))
    except Exception as e:
        rec['radq'] = 'ERR:%s' % e
    try:
        rec['delivered'] = bool(g['o32_delivered'](p, 2026, row))
    except Exception as e:
        rec['delivered'] = 'ERR:%s' % e
    rows.append(rec)
    avg += 0.2

p['scoring'] = saved
out['restored_v'] = ev(p) / F
out['rows'] = rows

print("avg      score   v        lvlcurr  bestlvl  radq   delivered")
prev = None
for r in rows:
    flag = ''
    if prev is not None and abs(r['v'] - prev) > 4:
        flag = '   <== STEP %+.1f' % (r['v'] - prev)
    print("%6.2f  %6.1f  %7.1f  %7.3f  %7.2f  %-5s  %-5s%s"
          % (r['avg'], r['score_implied'], r['v'], r['lvlcurr'] if isinstance(r['lvlcurr'], float) else -1,
             r['bestlvl'] if isinstance(r['bestlvl'], float) else -1, r['radq'], r['delivered'], flag), flush=True)
    prev = r['v']
print("restored v = %.1f (shipped board = 247)" % out['restored_v'], flush=True)

json.dump(out, open(os.environ['PROBE_OUT'], 'w'), indent=1, default=str)
print("WROTE", os.environ['PROBE_OUT'], "total %.1fs" % (time.time() - t0), flush=True)
