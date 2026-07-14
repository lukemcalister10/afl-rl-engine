#!/usr/bin/env python3
"""MOVEMENT-MACHINE ATTRIBUTION CENSUS  (supervisor seat 6 · 2026-07-14 · READ-ONLY, Tier 3)
Five-leg per-player decomposition of _coreM1/_inferM1 (up credit / down penalty / _agemult2 / _eo),
priced through the convex price (SCAR). M2 denied-credit ledger, M3 English/eo test, M4 thin-hot-sample.

Measured on the LIVE pinned env: engine 2030e5df, store 340a7a32 -> board 3dc19fbb, config 69ead79b944d.
Board 3dc19fbb == tagged board-of-record 81e48293 EXCEPT bramble (+1 SCAR) [item-20 store-identity job].
SCAR reported in the NUMERAIRE (ev / F, F=1.0524, pick-1=3000) to match the shipped board.
Emits census_data.json (consumed by the report writer)."""
import io,contextlib,os,json,copy,numpy as np

NB=1.0524   # L7 numeraire divisor
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0],g)
MA=g['MA']; cp=g['cp']; ev=g['ev']
_coreM1=g['_coreM1']; _inferM1=g['_inferM1']; _eo=g['_eo']; _lvlcurr=g['_lvlcurr']
_S_AGE=g['_S_AGE']; _radq=g['_radq']; _agemult2=g['_agemult2']; _upS=g['_upS']; _nqual=g['_nqual']
PROVEN_N=g['PROVEN_N']; TOL_M1=g['TOL_M1']; DOWN_TOL=g['DOWN_TOL']; G_ADQ=g['G_ADQ']; WIN=g['WIN']
_L3_AGE=g['_L3_AGE']; S_M1=g['S_M1']
_lvl_orig=cp._lvl_eff_orig
real_lvl=cp._lvl_eff   # == _inferM1 (bound)
Y=2026

# ---- convex price at an overridden shipped level (path-additive SCAR pricing) ----
def _ev_at(tp,L):
    def ov(pp,YY=Y): return L if (pp is tp and YY==Y) else real_lvl(pp,YY)
    cp._lvl_eff=ov; MA._pe_clear()
    try:
        with contextlib.redirect_stdout(io.StringIO()): return ev(tp)
    finally: cp._lvl_eff=real_lvl; MA._pe_clear()
def _price_set(tp,levels):
    """price a set of distinct levels once each; returns {round(L,6):ev_raw}"""
    out={}
    for L in levels:
        k=round(float(L),6)
        if k not in out: out[k]=_ev_at(tp,L)
    return out
def _num(evraw): return evraw/NB

def debut(p): return cp.debutyr(p)
def age_of(p): return cp._age_asof(p,Y)

# dedupe board by object identity
seen=set(); board=[]
for p in MA.players:
    if id(p) in seen: continue
    seen.add(id(p)); board.append(p)

rows=[]
for p in board:
    pos=MA.gfut(p); repl=MA.REPL.get(pos,0.0)
    Lo=float(_lvl_orig(p,Y)); Lc=float(_lvlcurr(p,Y)); n=int(_nqual(p,Y)); a=age_of(p); eo=float(_eo(p,Y))
    core=float(_coreM1(p,Y)); ship=float(_inferM1(p,Y))
    with contextlib.redirect_stdout(io.StringIO()): native=ev(p)
    branch='?'; up_lvl=down_lvl=age_lvl=coreoth_lvl=0.0
    sw=None; am=None; L_raw=None
    if n==0:
        branch='cameo'; coreoth_lvl=core-Lo
    elif n<PROVEN_N:
        branch='thin'; coreoth_lvl=core-Lo
    else:
        if Lc>=Lo:
            branch='rising'; up_lvl=core-Lo
        else:
            drop=Lo-Lc
            if drop<=DOWN_TOL:
                branch='falling-hold'
            else:
                branch='falling-shed'
                sw=float(np.clip((drop-DOWN_TOL)/5.0,0.0,1.0))
                am=float(_agemult2(a,Lc-repl))
                L_raw=(1.0-sw)*Lo+sw*Lc
                down_lvl=L_raw-Lo
                age_lvl=core-L_raw
    eo_lvl=ship-core
    # price the levels we need: Lo, Lc, core, ship, (L_raw for shed)
    levels=[Lo,Lc,core,ship]
    if L_raw is not None: levels.append(L_raw)
    P=_price_set(p,levels)
    def SN(L): return _num(P[round(float(L),6)])   # numeraire SCAR at level L
    base=SN(Lo); ship_scar=SN(ship); native_num=_num(native)
    residual=native_num-ship_scar
    # SCAR legs (numeraire), path-additive from base
    up_scar=down_scar=age_scar=coreoth_scar=0.0
    if branch=='rising': up_scar=SN(core)-SN(Lo)
    elif branch=='falling-shed':
        down_scar=SN(L_raw)-SN(Lo); age_scar=SN(core)-SN(L_raw)
    elif branch in ('thin','cameo'): coreoth_scar=SN(core)-SN(Lo)
    eo_scar=SN(ship)-SN(core)
    total=native_num-base   # full machine effect vs pre-machine level Lo, incl residual
    # M2 riser diagnostics
    improvement=Lc-Lo
    passes_tol=improvement>=TOL_M1
    passes_radq=bool(_radq(p,Y,Lo))
    sage=float(_S_AGE(a)) if (_L3_AGE and a is not None) else (S_M1 if a is None else float(_S_AGE(a)))
    # full-improvement SCAR (un-discounted) and S_AGE shave, only meaningful for risers
    full_imp_scar=SN(Lc)-SN(Lo)           # value if the full rise were credited (level -> Lc)
    granted_scar=up_scar                  # what was actually granted
    # near-miss radq: best recent (last WIN yrs) season games/avg above Lo
    recent=[x for x in p['scoring'] if Y-WIN<x['year']<=Y and (debut(p)-1)<x['year']]
    recent_above=[(x['year'],x['games'],x['avg']) for x in recent if x['avg']>Lo]
    best_recent_games=max([x[1] for x in recent_above],default=0) if recent_above else 0
    rows.append(dict(
        player=p['player'],pos=pos,key=p.get('key'),n=n,age=(None if a is None else float(a)),
        debut=int(debut(p)),eo=eo,repl=float(repl),
        Lo=Lo,Lc=Lc,core=core,ship=ship,L_raw=(None if L_raw is None else float(L_raw)),
        sw=sw,agemult2=am,branch=branch,
        up_lvl=up_lvl,down_lvl=down_lvl,age_lvl=age_lvl,coreoth_lvl=coreoth_lvl,eo_lvl=eo_lvl,
        native=int(native),native_num=native_num,base_scar=base,ship_scar=ship_scar,residual=residual,
        up_scar=up_scar,down_scar=down_scar,age_scar=age_scar,coreoth_scar=coreoth_scar,eo_scar=eo_scar,
        total=total,
        improvement=improvement,passes_tol=passes_tol,passes_radq=passes_radq,sage=sage,
        full_imp_scar=full_imp_scar,granted_scar=granted_scar,
        best_recent_games=int(best_recent_games),
        n_recent_above=len(recent_above),
        recent_above=recent_above,
        scoring=[(x['year'],x['games'],round(x['avg'],2)) for x in p['scoring']],
    ))

json.dump(dict(board_md5='3dc19fbb',tag_board='81e48293',store='340a7a32',engine='2030e5df',
               NB=NB,n_board=len(rows),rows=rows),
          open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/census_data.json','w'))
print('CENSUS OK  board=%d  numeraire F=%.4f  board_md5=3dc19fbb (==81e48293 except bramble +1)'%(len(rows),NB))

# ---- quick sanity: legs sum to total (path-additive check) ----
maxerr=0.0
for r in rows:
    legsum=r['up_scar']+r['down_scar']+r['age_scar']+r['coreoth_scar']+r['eo_scar']+r['residual']
    maxerr=max(maxerr,abs(legsum-r['total']))
print('PATH-ADDITIVE CHECK: max|sum(legs)-total| = %.4f numeraire (G-ATTR)'%maxerr)
# native reconciliation: base + total == native_num
print('sample English:',[ (r['player'],round(r['base_scar']),round(r['eo_scar']),round(r['total']),round(r['residual'],2)) for r in rows if r['player']=='Timothy English'])
