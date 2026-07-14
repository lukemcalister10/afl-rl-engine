# DOUBLE-CHARGE SPLIT: per gap player, decay-charge vs new-term-charge vs total, in LEVEL and SCAR,
# against the measured D2 R2 curve. Boots BOTH levers ON (damp on, absence on). Reuses the engine's own
# _abs_gap / _abs_shift / _abs_frac / _lvl_eff_preabs (= level with damp, absence OFF).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['RL_DAMP']='1'; os.environ['RL_ABSENCE']='1'
import h
g=h.boot(); MA=g['MA']; cp=g['cp']; ev=g['ev']; F=1.0524
preabs=g['_lvl_eff_preabs']; abscur=cp._lvl_eff
_abs_gap=g['_abs_gap']; _abs_shift=g['_abs_shift']; _abs_frac=g['_abs_frac']
L_REF=float(os.environ.get('RL_ABS_LREF','75.0')); FADE_N=float(os.environ.get('RL_ABS_FADE_N','3.0'))
priced=[p for p in MA.data if MA.GRP.get(p.get('pos'))]

def ev_absoff(p):
    cp._lvl_eff=preabs
    try: return ev(p,2026)
    finally: cp._lvl_eff=abscur

rows=[]
for p in priced:
    gi=_abs_gap(p,2026)
    if gi is None or gi['age_pre'] is None: continue
    fade=float(np.clip(1.0-gi['npost']/FADE_N,0.0,1.0))
    frac=_abs_frac(gi['age_pre'])
    q=_abs_shift(p,gi['last'],gi['ret'])
    L_nogap=preabs(q,2026); L_dec=preabs(p,2026); L_fin=abscur(p,2026)
    ev_nogap=ev_absoff(q); ev_dec=ev_absoff(p); ev_fin=ev(p,2026)
    decay_lvl=L_dec-L_nogap; new_lvl=L_fin-L_dec; tot_lvl=L_fin-L_nogap
    truth_mult=-L_nogap*frac            # multiplicative truth (fade=1, return season)
    truth_add=-frac*L_REF               # additive-reading curve value (|eff| at this age)
    # seasons missed
    yrs=sorted(x['year'] for x in p['scoring'] if x['games']>0)
    missed=[y for y in range(gi['last']+1,gi['ret'])]
    rows.append(dict(player=p['player'], pos=MA.gfut(p), age_pre=gi['age_pre'], missed=missed,
        ret=gi['ret'], npost=gi['npost'], fade=round(fade,2), frac=round(frac,4),
        L_nogap=round(L_nogap,2), L_dec=round(L_dec,2), L_fin=round(L_fin,2),
        decay_lvl=round(decay_lvl,2), new_lvl=round(new_lvl,2), tot_lvl=round(tot_lvl,2),
        truth_mult=round(truth_mult,2), truth_add=round(truth_add,2),
        num_nogap=round(ev_nogap/F), num_dec=round(ev_dec/F), num_fin=round(ev_fin/F),
        decay_scar=round((ev_dec-ev_nogap)/F), new_scar=round((ev_fin-ev_dec)/F),
        tot_scar=round((ev_fin-ev_nogap)/F)))
json.dump(rows, open('gap_split.json','w'))

# report
rows.sort(key=lambda r: r['tot_lvl'])
print(f"=== DOUBLE-CHARGE SPLIT · {len(rows)} gap players (both levers ON) · LEVEL points ===")
print(f"  truth_mult = -L_nogap*frac(age) (multiplicative, fade=1);  a NEW-TERM overshoot = |tot|>|truth_mult|+0.3 AND new_lvl<0")
print(f"  {'player':22}{'pos':6}{'age':>4}{'missed':>10}{'npost':>6}{'fade':>5}{'Lng':>7}{'Ldec':>7}{'Lfin':>7}{'decay':>7}{'newT':>7}{'total':>7}{'truthM':>7}  flag")
over=0
for r in rows:
    flag=''
    if r['new_lvl']<-0.001 and abs(r['tot_lvl'])>abs(r['truth_mult'])+0.3: flag='OVERSHOOT'; over+=1
    if r['decay_lvl']<r['truth_mult']-0.3 and abs(r['new_lvl'])<0.01: flag='decay-only>curve(pre-existing)'
    print(f"  {r['player'][:21]:22}{r['pos']:6}{r['age_pre']:4.0f}{str(r['missed']):>10}{r['npost']:6d}{r['fade']:5.2f}"
          f"{r['L_nogap']:7.1f}{r['L_dec']:7.1f}{r['L_fin']:7.1f}{r['decay_lvl']:7.2f}{r['new_lvl']:7.2f}{r['tot_lvl']:7.2f}{r['truth_mult']:7.2f}  {flag}")
print(f"\n  NEW-TERM OVERSHOOTS (double-charge caused by the new term): {over}   (HALT condition if >0)")
# aggregate
import numpy as np
dl=np.array([r['decay_lvl'] for r in rows]); nl=np.array([r['new_lvl'] for r in rows]); tl=np.array([r['tot_lvl'] for r in rows])
print(f"  mean decay {dl.mean():+.2f}  mean new-term {nl.mean():+.2f}  mean total {tl.mean():+.2f} lvl-pts  (D2: decay -1.7, shortfall -3.2, truth -4.9)")
ds=np.array([r['decay_scar'] for r in rows]); ns=np.array([r['new_scar'] for r in rows]); ts=np.array([r['tot_scar'] for r in rows])
print(f"  SCAR: Σdecay {ds.sum():+d}  Σnew-term {ns.sum():+d}  Σtotal {ts.sum():+d} num-SCAR")
