"""Find the two REAL search rows: (3) 1 career game, sa nearest 7; (5) mid-pick ~6 games @ ~70."""
import engine_load, json
g = engine_load.load()
MA = g['MA']; cp = g['cp']
data = MA.data

def career(p):
    return sum(x['games'] for x in p['scoring'])

def wavg(p):
    tg = career(p)
    if tg == 0: return None
    return sum(x['games'] * x['avg'] for x in p['scoring']) / tg

print('=== ALL store players with EXACTLY 1 career game ===')
one = []
for p in data:
    if career(p) != 1: continue
    a = wavg(p)
    one.append((abs(a - 7.0), a, p['key'], p.get('type'), p.get('pick'), MA.effpk(p),
                MA.gfut(p), p.get('year'), cp.debutyr(p), p['scoring']))
one.sort()
for r in one[:25]:
    print('  |sa-7|=%6.2f sa=%6.2f  %-30s %-4s pick %-5s effpk %-3d %-5s draft %s debut %s' % r[:9])
print('  total 1-game rows:', len(one))

print()
print('=== mid-pick (effpk 15-45) rows: career games in [4,9], career avg in [60,80] ===')
mid = []
for p in data:
    cg = career(p)
    if not (4 <= cg <= 9): continue
    a = wavg(p)
    if a is None or not (55 <= a <= 85): continue
    ep = MA.effpk(p)
    if not (15 <= ep <= 45): continue
    d = ((cg - 6.0) / 6.0) ** 2 + ((a - 70.0) / 70.0) ** 2
    mid.append((d, cg, a, p['key'], p.get('type'), p.get('pick'), ep, MA.gfut(p),
                p.get('year'), cp.debutyr(p), p['scoring']))
mid.sort()
for r in mid[:20]:
    print('  d=%.5f  g=%d sa=%6.2f  %-30s %-4s pick %-5s effpk %-3d %-5s draft %s debut %s' % r[:10])
print('  total candidates:', len(mid))
