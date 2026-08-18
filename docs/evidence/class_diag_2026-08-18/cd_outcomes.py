#!/usr/bin/env python3
"""CLASS DIAGNOSTIC — PART A. REALISED year-1 outcomes for draft classes 2005-2015, measured off the
store rows the matrices carry. NO BOARD PRICE IS READ ANYWHERE IN THIS FILE except v0, which is only
used to define the same row population op_class.py scores, never as an outcome.

Year 1 of draft class C is season C+1 (the cohort year), the same year the class mark prices.
"""
import sys, os, json, math, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cd_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []
def P(s=''):
    print(s); OUT.append(str(s))

R = L.load('OKRULED')                     # the store rows are identical on both matrices
per, wend = L.rowset(R)

MEAS = {}
for y in L.ALLC:
    pop = [r for r in per.get(y, []) if L.year1_price(r, y, wend) is not None]
    n = len(pop)
    played = []
    G = 0.0; GA = 0.0; SURP = 0.0; ABOVE = 0; ABOVE_ND = 0
    for r in pop:
        s = L.season_of(r, y)
        if not s:
            continue
        g = float(s['games']); a = s.get('avg')
        if a is None or s.get('bar') not in L.BARS:
            continue
        played.append(r)
        b = L.age_bar(s['bar'], L.age_at(r, y))
        G += g; GA += g * float(a); SURP += g * (float(a) - b)
        if float(a) > b:
            ABOVE += 1
    # career-long realised strength, for the same rows
    cg = sum(float(s['games']) for r in pop for s in r['seasons'] if (s.get('games') or 0) > 0
             and s['year'] <= L.LAST_REAL_SEASON)
    c100 = sum(1 for r in pop if sum(float(s['games']) for s in r['seasons']
                                     if (s.get('games') or 0) > 0 and s['year'] <= L.LAST_REAL_SEASON) >= 100)
    MEAS[y] = dict(
        n=n,
        share_played=len(played) / n,
        games_tot=G, games_per_row=G / n, games_per_player=(G / len(played)) if played else float('nan'),
        ppg=(GA / G) if G else float('nan'),
        surp_ppg=(SURP / G) if G else float('nan'),
        share_above=(ABOVE / len(played)) if played else float('nan'),
        share_above_all=ABOVE / n,
        prod_tot=GA, prod_per_row=GA / n,
        surp_tot=SURP, surp_per_row=SURP / n,
        career_games_per_row=cg / n, share_100=c100 / n)

P('=' * 122)
P('A — REALISED YEAR-1 OUTCOMES, DRAFT CLASSES 2005-2015. Measured off the store, no board price used.')
P('=' * 122)
P('  year 1 of draft class C is season C+1.  "above the bar" = that season\'s average above the S1')
P('  age bar for the player\'s position and age.  ppg = games-weighted mean season average.')
P()
hdr = ('class', 'rows', 'played%', 'gms/row', 'gms/plyr', 'ppg', 'surp ppg', 'above%', 'prod/row', 'surp/row', 'car g/row', '100g%')
P('  %-6s %5s %8s %8s %9s %7s %9s %8s %9s %9s %10s %7s' % hdr)
for y in L.W2:
    m = MEAS[y]
    P('  %-6d %5d %7.1f%% %8.2f %9.2f %7.2f %+9.2f %7.1f%% %9.1f %+9.1f %10.1f %6.1f%%' %
      (y - 1, m['n'], 100 * m['share_played'], m['games_per_row'], m['games_per_player'], m['ppg'],
       m['surp_ppg'], 100 * m['share_above'], m['prod_per_row'], m['surp_per_row'],
       m['career_games_per_row'], 100 * m['share_100']))
P()

KEYS = [('games_per_row', 'year-1 games per row'),
        ('share_played', 'share of the class that played at all in year 1'),
        ('ppg', 'year-1 points per game (games-weighted)'),
        ('surp_ppg', 'year-1 points per game above the age bar'),
        ('share_above', 'share of year-1 players above their age bar'),
        ('prod_per_row', 'year-1 total production per row (games x ppg)'),
        ('surp_per_row', 'year-1 surplus points per row (games x (ppg - bar))'),
        ('career_games_per_row', 'career games per row, to 2025'),
        ('share_100', 'share of the class that reached 100 career games')]

P('  RANKS on the registered basis. 1 = strongest of the eleven classes.')
P('  %-6s' % 'class' + ''.join('%12s' % k[:12] for k, _ in KEYS))
RANK = {}
for k, _ in KEYS:
    order = sorted(L.W2, key=lambda y: -MEAS[y][k])
    for i, y in enumerate(order):
        RANK.setdefault(y, {})[k] = i + 1
for y in L.W2:
    P('  %-6d' % (y - 1) + ''.join('%12d' % RANK[y][k] for k, _ in KEYS))
P()
P('  mean rank across the nine measures:')
for y in sorted(L.W2, key=lambda z: sum(RANK[z].values())):
    P('    draft class %d   mean rank %.1f' % (y - 1, sum(RANK[y].values()) / len(KEYS)))

json.dump(dict(meas={str(k): v for k, v in MEAS.items()},
               rank={str(k): v for k, v in RANK.items()},
               keys=[k for k, _ in KEYS]),
          open(os.path.join(HERE, 'CD_OUTCOMES.json'), 'w'), indent=1, default=float)
open(os.path.join(HERE, 'CD_OUTCOMES_out.txt'), 'w').write('\n'.join(OUT) + '\n')
