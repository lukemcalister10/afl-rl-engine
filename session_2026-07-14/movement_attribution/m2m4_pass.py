#!/usr/bin/env python3
"""Second engine pass: price M2 hypothetical would-have-been credits (denied risers) and
M4 thin-hot-sample counterfactuals. Writes m2m4_data.json. Same env/board as census.py."""
import io,contextlib,os,json,copy,numpy as np
NB=1.0524
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0],g)
MA=g['MA']; cp=g['cp']; ev=g['ev']
_inferM1=g['_inferM1']; _lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; _S_AGE=g['_S_AGE']
real_lvl=cp._lvl_eff; Y=2026; _lvl_orig=cp._lvl_eff_orig
def _ev_at(tp,L):
    def ov(pp,YY=Y): return L if (pp is tp and YY==Y) else real_lvl(pp,YY)
    cp._lvl_eff=ov; MA._pe_clear()
    try:
        with contextlib.redirect_stdout(io.StringIO()): return ev(tp)
    finally: cp._lvl_eff=real_lvl; MA._pe_clear()
def SN(tp,L): return _ev_at(tp,L)/NB

D=json.load(open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/census_data.json'))
rows=D['rows']
# index board objects by key (unique)
by_key={}
seen=set()
for p in MA.players:
    if id(p) in seen: continue
    seen.add(id(p)); by_key[p.get('key')]=p

# ---------- M2 hypothetical would-have-been credit for DENIED risers ----------
# credit level if BOTH gates passed = Lo + sage*(Lc-Lo).  Denied set = risers 0<imp with (not TOL) or (TOL & not radq).
m2={}
for r in rows:
    if r['n']<4 or r['branch']!='rising' or r['improvement']<=1e-9: continue
    denied = (not r['passes_tol']) or (r['passes_tol'] and not r['passes_radq'])
    if not denied: continue
    p=by_key[r['key']]
    Lo=r['Lo']; Lc=r['Lc']; sage=r['sage']
    credit_lvl=Lo+sage*(Lc-Lo)
    would=SN(p,credit_lvl)-SN(p,Lo)      # would-have-been credit SCAR (numeraire) if gate(s) removed
    m2[r['key']]=dict(would_credit_scar=would, credit_lvl_delta=sage*(Lc-Lo))
print('M2 hypothetical priced for %d denied risers'%len(m2))

# ---------- M4 thin-hot-sample lift ----------
# Candidate = board player with >=1 season games<GTHIN AND avg>Lo (a thin HOT sample above pre-machine level)
# that is inside the recency window (year within last WIN2 years so it drives _lvlcurr materially).
# Counterfactual: remove ALL such thin-hot seasons, recompute _inferM1 on the copy, price the LIFT.
GTHIN=8; WIN2=3
m4=[]
for r in rows:
    p=by_key[r['key']]
    Lo=r['Lo']
    debut=cp.debutyr(p)
    thin_hot=[x for x in p['scoring'] if 0<x['games']<GTHIN and x['avg']>Lo and (Y-WIN2)<x['year']<=Y and (debut-1)<x['year']]
    if not thin_hot: continue
    # counterfactual copy without the thin-hot seasons
    cf=copy.deepcopy(p)
    drop_years={x['year'] for x in thin_hot}
    cf['scoring']=[x for x in p['scoring'] if x['year'] not in drop_years]
    ship_cf=float(_inferM1(cf,Y)) if cf['scoring'] else Lo
    ship_actual=r['ship']
    lift_lvl=ship_actual-ship_cf
    lift_scar=SN(p,ship_actual)-SN(p,ship_cf)
    m4.append(dict(key=r['key'],player=r['player'],pos=r['pos'],n=r['n'],branch=r['branch'],
                   age=r['age'],Lo=Lo,Lc=r['Lc'],ship=ship_actual,ship_cf=ship_cf,
                   lift_lvl=lift_lvl,lift_scar=lift_scar,native_num=r['native_num'],
                   thin_hot=[(x['year'],x['games'],round(x['avg'],2)) for x in thin_hot]))
m4.sort(key=lambda z:-z['lift_scar'])
print('M4 thin-hot candidates:',len(m4),' with lift>10num:',sum(1 for x in m4 if x['lift_scar']>10))

json.dump(dict(m2=m2,m4=m4,GTHIN=GTHIN,WIN2=WIN2),
          open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/m2m4_data.json','w'))
print('M2M4 OK')
