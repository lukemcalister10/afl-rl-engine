"""Broader search for the 6-games-at-70 row (any pick, non-RUCK preferred)."""
import engine_load
g = engine_load.load()
MA = g['MA']; cp = g['cp']
data = MA.data
def career(p): return sum(x['games'] for x in p['scoring'])
def wavg(p):
    tg = career(p)
    return None if tg == 0 else sum(x['games'] * x['avg'] for x in p['scoring']) / tg
out = []
for p in data:
    cg = career(p)
    if not (5 <= cg <= 7): continue
    a = wavg(p)
    if a is None or not (62 <= a <= 78): continue
    out.append((abs(cg - 6) + abs(a - 70) / 10.0, cg, a, p['key'], p.get('type'),
                p.get('pick'), MA.effpk(p), MA.gfut(p), p.get('year'), cp.debutyr(p)))
out.sort()
for r in out[:25]:
    print('  d=%.3f g=%d sa=%6.2f %-30s %-4s pick %-5s effpk %-3d %-5s draft %s debut %s' % r)
print('n=', len(out))
