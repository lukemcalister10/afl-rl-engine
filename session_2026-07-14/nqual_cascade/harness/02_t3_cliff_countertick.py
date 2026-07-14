"""T3 cliff ledger via PURE COUNTER-TICK repricing (hold all level inputs fixed; tick n->n+1).
Isolates the regime switch = the cliff height. READ-ONLY. board 81e48293 / store b0c39d78."""
import io,contextlib,json,numpy as np,collections
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; PROVEN_N=g['PROVEN_N']
_par_prior=g['_par_prior']; _lvlcurr=g['_lvlcurr']
SEASON_FE=g['SEASON_FE']; INPROG_Y=g['INPROG_Y']; F=1.0524; Y=2026
orig_nqual=g['_nqual']
FORCE={}  # key -> additive n bump for measurement
def nqual_patched(p,Y=2026):
    return orig_nqual(p,Y)+FORCE.get(p.get('key'),0)
g['_nqual']=nqual_patched   # all engine closures read _nqual from g -> picked up

board=json.load(open('board_of_record.json')); bset={p['key'] for p in board['active']}
pool=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
def sv(p):
    MA._pe_clear(); return int(round(ev(p,Y)/F))
def lvl(p):
    MA._pe_clear(); return round(cp._lvl_eff(p,Y),3)
def seas(p): return [(int(x['year']),int(x['games'])) for x in p['scoring'] if x['games']>0 and (cp.debutyr(p)-1)<x['year']<=Y]

def reprice_plus1(p):
    n0=orig_nqual(p,Y); v0=sv(p); l0=lvl(p)
    FORCE[p['key']]=1
    try: n1=orig_nqual(p,Y)+1; v1=sv(p); l1=lvl(p)
    finally: FORCE.pop(p['key'],None); MA._pe_clear()
    return n0,n1,v0,v1,l0,l1

def near_bar(p):
    """live proximity: a completed season at exactly 9 (settled knife-edge) OR 2026 season projecting to
    clear by R24 (current games>=10*SEASON_FE and <10)."""
    s=seas(p)
    comp9=any(gm==9 and yr<INPROG_Y for yr,gm in s)
    ip9  =any(gm==9 and yr==INPROG_Y for yr,gm in s)
    ip_proj=any(yr==INPROG_Y and 10*SEASON_FE<=gm<10 for yr,gm in s)
    return comp9,ip9,ip_proj

ledger=[]
for p in pool:
    n0=orig_nqual(p,Y)
    comp9,ip9,ip_proj=near_bar(p)
    live = comp9 or ip9 or ip_proj
    n0v,n1v,v0,v1,l0,l1=reprice_plus1(p)
    boundary='0->1' if n0==0 else ('3->4' if n0==3 else ('%d->%d'%(n0,n0+1)))
    regime_switch = (n0==0) or (n0==3)   # 0->1 switch ON, 3->4 switch OFF (pedigree vanishes)
    ledger.append(dict(
        key=p['key'],name=p.get('player'),grp=MA.gfut(p),pick=MA.effpk(p),age=cp._age_asof(p,Y),
        type=p.get('type'),on_board=(p['key'] in bset),n0=n0,boundary=boundary,
        v0=v0,v1=v1,delta=v1-v0,lvl0=l0,lvl1=l1,
        par=round(_par_prior(p,Y),2),lvlcurr=round(_lvlcurr(p,Y),2),
        comp9=comp9,ip9=ip9,ip_proj=ip_proj,live=live,
        g2026=next((gm for yr,gm in seas(p) if yr==INPROG_Y),0),
    ))
json.dump(ledger,open('/tmp/nq_ws/t3_ledger.json','w'))

def summ(rows,tag):
    if not rows: print(tag,'(none)'); return
    d=[r['delta'] for r in rows]
    print('%-38s n=%3d  |d| mean=%6.1f med=%6.1f max=%5d  netΣ=%+d'%(
        tag,len(rows),np.mean(np.abs(d)),np.median(np.abs(d)),max(abs(x) for x in d),sum(d)))

print('=== FULL cliff-height by starting regime (pure counter-tick, ALL pool) ===')
for nb,lab in [(0,'0->1 (pedigree switch ON)'),(1,'1->2'),(2,'2->3'),(3,'3->4 (pedigree VANISH)'),(4,'4->5 proven'),(5,'5->6 proven')]:
    summ([r for r in ledger if r['n0']==nb],lab)
print()
print('=== LIVE crossers only (near_bar) by regime ===')
for nb,lab in [(0,'0->1 live'),(3,'3->4 live')]:
    summ([r for r in ledger if r['n0']==nb and r['live']],lab)
print('   0->1 live on_board:',sum(1 for r in ledger if r['n0']==0 and r['live'] and r['on_board']))
print('   3->4 live on_board:',sum(1 for r in ledger if r['n0']==3 and r['live'] and r['on_board']))

def show(sub):
    for r in ledger:
        if sub.lower() in (r['name'] or '').lower():
            print('  %-20s n0=%d %s v0=%5d v1=%5d Δ=%+5d lvl %6.1f->%6.1f par=%5.1f lc=%5.1f live=%s(c9=%s ip9=%s ipj=%s) g26=%d'%(
                r['name'],r['n0'],r['boundary'],r['v0'],r['v1'],r['delta'],r['lvl0'],r['lvl1'],r['par'],r['lvlcurr'],r['live'],r['comp9'],r['ip9'],r['ip_proj'],r['g2026']))
print('\n=== known anchors ===')
for s in ['tsatas','nathan o','cadman']: show(s)
