"""T4: what the pedigree (par term) is worth per blend player (n=1..3), in level and in SCAR value.
Counterfactual: collapse the blend to pure current level (par->Lc) and reprice. READ-ONLY. board 81e48293."""
import io,contextlib,json,numpy as np
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; cp=g['cp']; ev=g['ev']; PROVEN_N=g['PROVEN_N']
_lvlcurr=g['_lvlcurr']; orig_par=g['_par_prior']; orig_nqual=g['_nqual']
INPROG_Y=g['INPROG_Y']; F=1.0524; Y=2026
board=json.load(open('board_of_record.json')); bset={p['key'] for p in board['active']}

PAR_OVR={}   # key -> forced par value (for the counterfactual)
def par_patched(p,Y=2026):
    k=p.get('key')
    if k in PAR_OVR: return PAR_OVR[k]
    return orig_par(p,Y)
g['_par_prior']=par_patched
def sv(p): MA._pe_clear(); return int(round(ev(p,Y)/F))
def lvl(p): MA._pe_clear(); return round(cp._lvl_eff(p,Y),3)

pool=[p for p in MA.data if MA.GRP.get(p.get('pos'))]
rows=[]
for p in pool:
    n=orig_nqual(p,Y)
    if not (1<=n<=3): continue
    Lc=_lvlcurr(p,Y); par=orig_par(p,Y); c=n/PROVEN_N
    v0=sv(p); l0=lvl(p)
    PAR_OVR[p['key']]=Lc          # collapse blend -> pure current
    try: v_np=sv(p); l_np=lvl(p)
    finally: PAR_OVR.pop(p['key'],None); MA._pe_clear()
    rows.append(dict(key=p['key'],name=p.get('player'),grp=MA.gfut(p),pick=MA.effpk(p),age=cp._age_asof(p,Y),
        n=n,c=round(c,2),ped_wt=round(1-c,2),Lc=round(Lc,2),par=round(par,2),
        dlevel=round((1-c)*(par-Lc),2),         # pedigree's effect on level (>0 held up)
        lvl_ship=l0,lvl_nopedigree=l_np,
        v_ship=v0,v_nopedigree=v_np,ped_worth=v0-v_np,  # >0 pedigree HOLDS UP value; <0 holds DOWN
        on_board=(p['key'] in bset)))
json.dump(rows,open('/tmp/nq_ws/t4_pedigree.json','w'))
bd=[r for r in rows if r['on_board']]
print('blend players n=1..3: total=%d on_board=%d'%(len(rows),len(bd)))
held_up=[r for r in bd if r['ped_worth']>0]; held_dn=[r for r in bd if r['ped_worth']<0]
print('on_board HELD UP by pedigree: %d (ΣSCAR=+%d)  HELD DOWN: %d (ΣSCAR=%d)  net=%+d'%(
    len(held_up),sum(r['ped_worth'] for r in held_up),len(held_dn),sum(r['ped_worth'] for r in held_dn),
    sum(r['ped_worth'] for r in bd)))
def line(r):
    return '%-22s%-8s n=%d wt=%.2f  Lc=%6.1f par=%6.1f  lvl %6.1f->%6.1f  v %5d->%5d  ped_worth=%+5d'%(
        (r['name'] or '')[:22],r['grp'],r['n'],r['ped_wt'],r['Lc'],r['par'],r['lvl_ship'],r['lvl_nopedigree'],
        r['v_ship'],r['v_nopedigree'],r['ped_worth'])
print('\n== TOP 20 HELD UP by pedigree (production BELOW par; pedigree props value up) ==')
for r in sorted(bd,key=lambda r:-r['ped_worth'])[:20]: print(line(r))
print('\n== TOP 20 HELD DOWN by pedigree (production ABOVE par; pedigree suppresses value) ==')
for r in sorted(bd,key=lambda r:r['ped_worth'])[:20]: print(line(r))
# per-n summary
for nn in (1,2,3):
    z=[r for r in bd if r['n']==nn]
    if z: print('\nn=%d (ped wt %.2f): %d players, ped_worth mean=%+.1f med=%+.1f  |worth| mean=%.1f max=%d'%(
        nn,1-nn/4.,len(z),np.mean([r['ped_worth'] for r in z]),np.median([r['ped_worth'] for r in z]),
        np.mean([abs(r['ped_worth']) for r in z]),max(abs(r['ped_worth']) for r in z)))
