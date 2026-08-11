"""Dovaston worked example: is v0 position-aware at the same pick, and what does year 1 read?"""
import engine_load
g = engine_load.load()
MA = g['MA']; cp = g['cp']; ev = g['ev']
entry_anchor = g['entry_anchor']; _ageR = g['_ageR']

dov = [p for p in MA.data if 'dovaston' in p.get('key','')]
for p in dov:
    print('DOVASTON:', p['key'], '| type', p.get('type'), '| pos', MA.gfut(p),
          '| pick', p.get('pick'), '| draft yr', p.get('year'),
          '| draft age', _ageR(p), '| games', sum(x['games'] for x in p['scoring']),
          '| v0 (fitted entry anchor) %.1f' % entry_anchor(p),
          '| ev2026 %.1f' % ev(p, 2026))

# every player drafted at picks 14-18, any year: fitted v0 by position at ~the same pick
print('\nfitted v0 at picks 14-18 (position-awareness of the year-0 surface):')
rows = [p for p in MA.data if p.get('type')=='ND' and p.get('pick') and 14 <= p['pick'] <= 18
        and _ageR(p) == 18 and p.get('year') in (2023, 2024, 2025)]
for p in sorted(rows, key=lambda x: (MA.gfut(x), x['pick'])):
    print('  pick %2d %-4s %-22s v0 %7.1f' % (p['pick'], MA.gfut(p), p['player'], entry_anchor(p)))
