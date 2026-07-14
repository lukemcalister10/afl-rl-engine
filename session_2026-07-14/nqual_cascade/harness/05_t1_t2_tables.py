import json,numpy as np
rows=json.load(open('/tmp/nq_ws/master.json'))
board=[r for r in rows if r['on_board']]
full=rows
def tbl(pop,tag):
    print('--- %s (N=%d) ---'%(tag,len(pop)))
    print('%-8s %5s | %6s %6s %6s | %8s %8s'%('regime','count','par','lvlcur','lvlshp','v_med','v_mean'))
    for rg in ['0','1','2','3','PROVEN']:
        z=[r for r in pop if r['regime']==rg]
        if not z: continue
        pw=1-int(rg)/4 if rg not in('0','PROVEN') else (0.0 if rg=='PROVEN' else None)
        print('%-8s %5d | %6.1f %6.1f %6.1f | %8.0f %8.0f   pedigree wt=%s'%(
            rg,len(z),np.mean([r['par'] for r in z]),np.mean([r['lvlcurr'] for r in z]),
            np.mean([r['lvl_ship'] for r in z]),np.median([r['v'] for r in z]),np.mean([r['v'] for r in z]),
            ('n/a(Lo)' if rg=='0' else ('%.2f'%pw if pw is not None else '0(VANISHED)') if rg!='PROVEN' else '0 (VANISHED)')))
print('====== T1: FOUR-REGIME POPULATION TABLE ======')
tbl(board,'BOARD population (shipped, store b0c39d78 / board 81e48293)')
print()
tbl(full,'FULL priced pool (incl. historical/non-shipped)')

print('\n====== T2: THE 551, SPLIT ======')
INPROG=2026; FE=0.58
def has_comp9(r): return len(r['nine_completed'])>0
def has_ip9(r): return len(r['nine_inprog'])>0
def ip_proj(r):  # 2026 games in [10*FE,10) -> currently sub-bar, projects to clear by R24
    g=r['games_by_year'].get(str(INPROG),0) or r['games_by_year'].get(INPROG,0)
    return 10*FE<=g<10
for tag,pop in [('BOARD',board),('FULL',full)]:
    c9=[r for r in pop if has_comp9(r)]
    i9=[r for r in pop if has_ip9(r)]
    any9=[r for r in pop if has_comp9(r) or has_ip9(r)]
    proj=[r for r in pop if ip_proj(r)]
    print('%s: completed-season==9: %d | in-progress(2026)==9: %d | union(any==9): %d | 2026 in [5.8,10) projecting-to-clear: %d'%(
        tag,len(c9),len(i9),len(any9),len(proj)))
# effective bar
print('\nEffective mid-season bar: need 10 games. SEASON_FE=0.58 => playable-so-far ~= 22*0.58 = 12.8 games.')
print('  mid-season bar = 10/12.8 = %.0f%% of playable-so-far  vs  end-season 10/22 = %.0f%%  (%.2fx harder)'%(
    100*10/12.8,100*10/22,(10/12.8)/(10/22)))
# who is disqualified now (2026<10) but will clear by R24 (2026 >= 5.8 -> projects >=10): regime-boundary ones
disq=[r for r in board if (r['games_by_year'].get(str(INPROG),0) or 0)<10 and (r['games_by_year'].get(str(INPROG),0) or 0)>=10*FE]
print('\nBoard players currently <10 games in 2026 but projecting to clear 10 by R24: %d'%len(disq))
from collections import Counter
print('  their current regime:',dict(Counter(r['regime'] for r in disq)))
print('  at a switch boundary (n=0 -> will gain pedigree, or n=3 -> will lose pedigree):')
b0=[r for r in disq if r['regime']=='0']; b3=[r for r in disq if r['regime']=='3']
print('    n=0 (pedigree switches ON at R24): %d'%len(b0))
print('    n=3 (pedigree VANISHES at R24):    %d  e.g. %s'%(len(b3),', '.join(r['name'] for r in b3[:8])))
