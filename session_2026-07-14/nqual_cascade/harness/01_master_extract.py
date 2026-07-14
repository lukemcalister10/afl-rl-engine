"""Master extraction + repricing engine. READ-ONLY. store b0c39d78 / board 81e48293."""
import io,contextlib,json,copy,numpy as np,os
from collections import Counter,defaultdict
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; cp=g['cp']
_nqual=g['_nqual']; PROVEN_N=g['PROVEN_N']; _lvlcurr=g['_lvlcurr']; _par_prior=g['_par_prior']
delisted=g['delisted']; nseas=g['nseas']; nseas_pro=g['nseas_pro']
_coreM1=g['_coreM1']
SEASON_FE=g['SEASON_FE']; INPROG_Y=g['INPROG_Y']
F=1.0524; Y=2026
board=json.load(open('board_of_record.json'))
bv={p['key']:p for p in board['active']}

def regime(n): return '0' if n==0 else ('PROVEN' if n>=PROVEN_N else str(n))
def shipped_v(p): return int(round(ev(p,Y)/F))

def base_rec(p):
    n=_nqual(p,Y)
    gy={int(x['year']):int(x['games']) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y}
    # qualifying-relevant seasons (games>0, in career window, year<=Y)
    seasons=[(int(x['year']),int(x['games'])) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y]
    nine_completed=[yr for yr,gm in seasons if gm==9 and yr<INPROG_Y]
    nine_inprog=[yr for yr,gm in seasons if gm==9 and yr==INPROG_Y]
    return dict(
        key=p.get('key'), name=p.get('player'), pos=p.get('pos'), grp=MA.gfut(p),
        pick=MA.effpk(p), type=p.get('type'), age=cp._age_asof(p,Y),
        n=n, regime=regime(n), par=round(_par_prior(p,Y),3), lvlcurr=round(_lvlcurr(p,Y),3),
        lvl_ship=round(cp._lvl_eff(p,Y),3), ev_raw=round(ev(p,Y),2), v=shipped_v(p),
        delisted=bool(delisted(p)), retired=bool(p.get('_retired')), pickless=bool(p.get('_pickless')),
        nseas=nseas(p,Y), nseas_pro=round(nseas_pro(p,Y),3),
        games_by_year=gy, debutyr=cp.debutyr(p),
        nine_completed=nine_completed, nine_inprog=nine_inprog,
        on_board=(p.get('key') in bv),
        board_v=(bv[p['key']]['v'] if p.get('key') in bv else None),
    )

pool=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
key2p={p.get('key'):p for p in pool}
rows=[base_rec(p) for p in pool]
json.dump(rows, open('/tmp/nq_ws/master.json','w'))

board_rows=[r for r in rows if r['on_board']]
print('pool=%d  on_board=%d'%(len(rows),len(board_rows)))

# ---------- REPRICING: bump one season from g->g+1 (the "one game lands") ----------
def reprice_bump(p, target_year):
    """Return (n_before, n_after, v_before, v_after, lvl_before, lvl_after) after bumping target_year's games +1."""
    n0=_nqual(p,Y); v0=shipped_v(p); l0=cp._lvl_eff(p,Y)
    sav=None
    for x in p['scoring']:
        if int(x['year'])==target_year:
            sav=x['games']; x['games']=x['games']+1; break
    MA._pe_clear()
    try:
        n1=_nqual(p,Y); v1=shipped_v(p); l1=cp._lvl_eff(p,Y)
    finally:
        for x in p['scoring']:
            if int(x['year'])==target_year and sav is not None:
                x['games']=sav; break
        MA._pe_clear()
    return n0,n1,v0,v1,round(l0,3),round(l1,3)

# For every player within one game of a boundary: a season currently at games==9 whose flip to 10 increments n.
# We reprice by bumping the MOST RECENT 9-game season (in-progress preferred, else latest completed).
cliff=[]
for r in rows:
    nines = r['nine_inprog'] + r['nine_completed']
    if not nines: continue
    p=key2p[r['key']]
    ty = INPROG_Y if r['nine_inprog'] else max(r['nine_completed'])
    n0,n1,v0,v1,l0,l1=reprice_bump(p,ty)
    if n1==n0: continue  # bump didn't change n (already counted elsewhere) -> skip
    boundary = '0->1' if (n0==0 and n1==1) else ('3->4(PROVEN)' if (n0==3 and n1>=PROVEN_N) else '%d->%d'%(n0,n1))
    cliff.append(dict(key=r['key'],name=r['name'],grp=r['grp'],pick=r['pick'],age=r['age'],
        type=r['type'],on_board=r['on_board'],boundary=boundary,
        n0=n0,n1=n1,v0=v0,v1=v1,delta=v1-v0,lvl0=l0,lvl1=l1,
        bump_year=ty,bump_inprog=bool(r['nine_inprog']),
        par=r['par'],lvlcurr=r['lvlcurr'],
        delisted=r['delisted'],retired=r['retired']))
json.dump(cliff, open('/tmp/nq_ws/cliff.json','w'))
print('cliff crossers=%d  (on_board=%d)'%(len(cliff), sum(1 for c in cliff if c['on_board'])))
bc=Counter(c['boundary'] for c in cliff)
print('boundary counts:', dict(bc))
