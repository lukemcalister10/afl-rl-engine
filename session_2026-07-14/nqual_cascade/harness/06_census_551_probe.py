import io,contextlib,json,numpy as np,itertools,collections
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; _nqual=g['_nqual']; PROVEN_N=g['PROVEN_N']
SEASON_FE=g['SEASON_FE']; INPROG_Y=g['INPROG_Y']; Y=2026
pool=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
def seasons(p): return [(int(x['year']),int(x['games'])) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y]
# also seasons WITHOUT the debut-year exclusion / without >0 filter, to test census variants
def seasons_all(p): return [(int(x['year']),int(x['games'])) for x in p['scoring']]
def seasons_win(p): return [(int(x['year']),int(x['games'])) for x in p['scoring'] if (cp.debutyr(p)-1)<x['year']<=Y]

N=len(pool)
print('pool',N)
# distinct-player counts: has any season (with filter variant) at exactly g games
for tag,sf in [('win+pos>0',seasons),('win(any g)',seasons_win),('all-rows',seasons_all)]:
    dist=collections.Counter()
    for p in pool:
        gs=set(gm for _,gm in sf(p))
        for gm in gs: dist[gm]+=1
    print('--- variant',tag,'--- players with a season at exactly g:')
    print('   ', {k:dist[k] for k in range(5,14)})
# cumulative: players with any season with games <= 9 and >= X  (approaching)
# target 551. Try: players with any season in a set S
cand_sets=[{9},{9,10},{8,9},{9,11},{8,9,10},{9,10,11},{7,8,9},{9,10,11,12}]
for S in cand_sets:
    for tag,sf in [('win+pos>0',seasons),('win',seasons_win)]:
        c=sum(1 for p in pool if any(gm in S for _,gm in sf(p)))
        if abs(c-551)<=8 or abs(c-551)==0:
            print('MATCH-ish set=%s var=%s -> %d'%(S,tag,c))
        # print all anyway
print('--- brute distinct players with season games in [a,b] ---')
for a in range(6,11):
    for b in range(a,13):
        c=sum(1 for p in pool if any(a<=gm<=b for _,gm in seasons(p)))
        if abs(c-551)<=5: print('  range[%d,%d] win+pos>0 -> %d'%(a,b,c))
        c2=sum(1 for p in pool if any(a<=gm<=b for _,gm in seasons_win(p)))
        if abs(c2-551)<=5: print('  range[%d,%d] win -> %d'%(a,b,c2))
# season-instance counts (not distinct players)
si9=sum(1 for p in pool for _,gm in seasons(p) if gm==9)
si_all9=sum(1 for p in pool for _,gm in seasons_all(p) if gm==9)
print('season-instances at 9 (win+pos>0):',si9,'(all rows):',si_all9)
# players whose _nqual would change if bar dropped to 9 (a season at exactly 9 flips): distinct
flip=sum(1 for p in pool if any(gm==9 for _,gm in seasons(p)))
print('players with >=1 season at 9 (flip-up on -1 bar):',flip)
# players within one game EITHER direction: season at 9 (up) or at 10 (down)
either=sum(1 for p in pool if any(gm in (9,10) for _,gm in seasons(p)))
print('players with a season at 9 OR 10:',either)
