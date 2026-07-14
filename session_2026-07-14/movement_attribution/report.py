#!/usr/bin/env python3
"""Compute all census figures for the RETURN. Reads census_data.json + m2m4_data.json; prints structured
blocks used to compose the markdown report. Pure arithmetic — no engine."""
import json,numpy as np
from collections import Counter
D=json.load(open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/census_data.json'))
M=json.load(open('/home/user/afl-rl-engine/session_2026-07-14/movement_attribution/m2m4_data.json'))
rows=D['rows']; m2=M['m2']; m4=M['m4']
def s(v): return 0.0 if v is None else v
def R(x): return int(round(x))

print('='*70); print('BOARD',D['board_md5'],'== tag',D['tag_board'],'(except bramble +1) | store',D['store'],'| engine',D['engine'],'| N=',D['n_board'],'| F=',D['NB'])
print('='*70)

# ===================== M1 — leg aggregates =====================
legs=['up_scar','down_scar','age_scar','eo_scar','coreoth_scar','residual']
print('\n### M1 BOARD-WIDE LEG TOTALS (numeraire SCAR)')
for L in legs:
    tot=sum(r[L] for r in rows)
    npos=sum(1 for r in rows if r[L]>0.5); nneg=sum(1 for r in rows if r[L]<-0.5)
    print('  %-12s  total=%+9d   (+:%3d  -:%3d)'%(L.replace('_scar',''),R(tot),npos,nneg))
print('  %-12s  total=%+9d'%('TOTAL(net)',R(sum(r['total'] for r in rows))))
print('  abs machine churn Σ|total| = %d'%R(sum(abs(r['total']) for r in rows)))

# ranked by |total|
print('\n### M1 TOP 30 BY |total|  (Lo->up->down->age->eo->ship)')
hdr='%-22s %-12s %3s %4s %5s | %6s | %6s %6s %6s %6s %6s %5s | %7s | %6s'%(
 'player','branch','n','age','eo','baseSC','up','down','age','EO','other','resid','total','native')
print(hdr)
for r in sorted(rows,key=lambda z:-abs(z['total']))[:30]:
    print('%-22s %-12s %3d %4s %5.2f | %6d | %+6d %+6d %+6d %+6d %+6d %5d | %+7d | %6d'%(
      r['player'][:22],r['branch'],r['n'],('%.0f'%r['age'] if r['age'] is not None else '  -'),r['eo'],
      R(r['base_scar']),R(r['up_scar']),R(r['down_scar']),R(r['age_scar']),R(r['eo_scar']),R(r['coreoth_scar']),
      R(r['residual']),R(r['total']),r['native']))

# ===================== M2 — denied credit ledger =====================
prov=[r for r in rows if r['n']>=4]
risers=[r for r in prov if r['branch']=='rising' and r['improvement']>1e-9]
full_all=sum(r['full_imp_scar'] for r in risers)
grant_all=sum(r['granted_scar'] for r in risers)
print('\n'+'='*70); print('### M2 DENIED-CREDIT LEDGER  (%d proven risers, improvement>0)'%len(risers))
print('  Σ full improvement value (level Lo->Lc, 100%%): %+d SCAR'%R(full_all))
print('  Σ actually credited (granted):                 %+d SCAR'%R(grant_all))
print('  Σ DENIED TO IMPROVERS (full - granted):        %+d SCAR'%R(full_all-grant_all))
tol_denied=[r for r in risers if not r['passes_tol']]
radq_denied=[r for r in risers if r['passes_tol'] and not r['passes_radq']]
passed=[r for r in risers if r['passes_tol'] and r['passes_radq']]
def wc(r): return m2.get(r['key'],{}).get('would_credit_scar',0.0)
print('\n  -- Denied by TOL_M1 (0<imp<5.0): %d players'%len(tol_denied))
print('     Σ would-have-been credit (if TOL removed, still sage-disc): %+d SCAR'%R(sum(wc(r) for r in tol_denied)))
print('     Σ full improvement value they generated:                    %+d SCAR'%R(sum(r['full_imp_scar'] for r in tol_denied)))
neartol=sorted([r for r in tol_denied if 4.0<=r['improvement']<5.0],key=lambda z:-z['improvement'])
print('     4.0-4.9 NEAR-MISS (%d) — a rounding error from credit:'%len(neartol))
for r in neartol:
    print('        %-22s %-9s imp=%.2f  would=%+d  full=%+d'%(r['player'][:22],r['pos'],r['improvement'],R(wc(r)),R(r['full_imp_scar'])))
print('\n  -- Denied by _radq (imp>=5.0, no 12g season above Lo in last 2y): %d players'%len(radq_denied))
print('     Σ would-have-been credit: %+d SCAR ; Σ full improvement: %+d SCAR'%(R(sum(wc(r) for r in radq_denied)),R(sum(r['full_imp_scar'] for r in radq_denied))))
for r in sorted(radq_denied,key=lambda z:-z['improvement']):
    print('        %-22s %-9s imp=%.2f  best_recent_games=%d  would=%+d'%(r['player'][:22],r['pos'],r['improvement'],r['best_recent_games'],R(wc(r))))
radq_1011=[r for r in radq_denied if r['best_recent_games'] in (10,11)]
print('     of these, ON 10 OR 11 GAMES (one game from qualifying): %d'%len(radq_1011))
for r in radq_1011: print('        %-22s %-9s %d games'%(r['player'][:22],r['pos'],r['best_recent_games']))
print('\n  -- Denied by S_AGE (age discount on the %d who PASSED both gates):'%len(passed))
shave=sum(r['full_imp_scar']-r['granted_scar'] for r in passed)
print('     Σ S_AGE shave (full - granted): %+d SCAR'%R(shave))
zero30=[r for r in passed if r['age'] is not None and r['age']>=30 and r['sage']<=1e-9]
print('     age30+ who improved and got EXACTLY ZERO credit (sage=0): %d'%len(zero30))
for r in sorted(zero30,key=lambda z:-z['full_imp_scar']):
    print('        %-22s %-9s age=%.0f imp=%.2f  shaved(=full)=%+d'%(r['player'][:22],r['pos'],r['age'],r['improvement'],R(r['full_imp_scar'])))
print('     per-player S_AGE shave, top 12 gate-passers:')
for r in sorted(passed,key=lambda z:-(z['full_imp_scar']-z['granted_scar']))[:12]:
    print('        %-22s %-9s age=%3s sage=%.2f imp=%.2f full=%+d granted=%+d shave=%+d'%(
      r['player'][:22],r['pos'],('%.0f'%r['age'] if r['age'] else '-'),r['sage'],r['improvement'],
      R(r['full_imp_scar']),R(r['granted_scar']),R(r['full_imp_scar']-r['granted_scar'])))

# ===================== M3 — eo / English test =====================
print('\n'+'='*70); print('### M3 THE ENGLISH TEST (_eo)')
eos=[r['eo'] for r in rows]
print('  eo distribution: N=%d  at1.0=%d  >=0.99=%d  >=0.90=%d  (0,0.9)=%d  ==0=%d  mean=%.3f'%(
  len(eos),sum(e>=0.999 for e in eos),sum(e>=0.99 for e in eos),sum(e>=0.90 for e in eos),
  sum(1 for e in eos if 0<e<0.90),sum(e<=1e-9 for e in eos),float(np.mean(eos))))
# override quantification among eo>=0.99
near1=[r for r in rows if r['eo']>=0.99]
overwritten=[r for r in near1 if r['ship']<r['core']-1e-6]   # eo dragged below coreM1
preserved=[r for r in near1 if abs(r['ship']-r['core'])<=1e-6]  # min() selected coreM1
print('  among eo>=0.99 (%d): shipped<coreM1 (OVERWRITTEN/dragged)=%d  shipped==coreM1 (PRESERVED)=%d'%(
  len(near1),len(overwritten),len(preserved)))
print('  Σ eo drag SCAR over eo>=0.99 dragged: %+d ; mean level drop %.2f'%(
  R(sum(r['eo_scar'] for r in overwritten)),float(np.mean([r['core']-r['ship'] for r in overwritten])) if overwritten else 0))
# HOLD BAND test
hold=[r for r in rows if r['branch']=='falling-hold']
hold_dragged=[r for r in hold if r['eo_lvl']<-1e-6]
print('\n  HOLD BAND: falling-hold (drop<=3, coreM1 forgives) = %d players'%len(hold))
print('     of those, _eo drags DOWN anyway = %d  (%.0f%%)'%(len(hold_dragged),100*len(hold_dragged)/max(1,len(hold))))
print('     Σ SCAR the "hold band" players lose to _eo: %+d'%R(sum(r['eo_scar'] for r in hold_dragged)))
print('     biggest hold-band eo victims:')
for r in sorted(hold_dragged,key=lambda z:z['eo_scar'])[:10]:
    cg=sum(x[1] for x in r['scoring'])
    print('        %-22s %-9s drop=%.2f eo=%.2f  eo_SCAR=%+d  (career games %d)'%(
      r['player'][:22],r['pos'],r['Lo']-r['Lc'],r['eo'],R(r['eo_scar']),cg))
# English
eng=[r for r in rows if r['player']=='Timothy English'][0]
print('\n  TIMOTHY ENGLISH: Lo=%.2f Lc=%.2f drop=%.2f coreM1=%.2f ship=%.2f eo=%.3f'%(
  eng['Lo'],eng['Lc'],eng['Lo']-eng['Lc'],eng['core'],eng['ship'],eng['eo']))
print('     base_SCAR(Lo)=%d  down/age legs=%d/%d (hold band -> 0)  eo_SCAR=%+d  total=%+d  native=%d'%(
  R(eng['base_scar']),R(eng['down_scar']),R(eng['age_scar']),R(eng['eo_scar']),R(eng['total']),eng['native']))
# durability correlation
drag=[r for r in rows if r['eo_lvl']<-1e-6]
cg=np.array([sum(x[1] for x in r['scoring']) for r in drag]); es=np.array([-r['eo_scar'] for r in drag])
r_gd=float(np.corrcoef(cg,es)[0,1])
print('\n  DURABILITY vs DRAG: over %d eo-dragged players, corr(career games, |eo drag SCAR|) = %.3f'%(len(drag),r_gd))
# also within hold band
cgh=np.array([sum(x[1] for x in r['scoring']) for r in hold_dragged]); esh=np.array([-r['eo_scar'] for r in hold_dragged])
print('     within hold-band victims (n=%d): corr = %.3f'%(len(hold_dragged),float(np.corrcoef(cgh,esh)[0,1]) if len(hold_dragged)>2 else float('nan')))

# ===================== M4 — thin hot sample =====================
print('\n'+'='*70); print('### M4 THIN-HOT-SAMPLE LIFT (games<%d, avg>Lo, last %dy; counterfactual removes them)'%(M['GTHIN'],M['WIN2']))
mat=[x for x in m4 if x['lift_scar']>10]
print('  candidates=%d  material(>10 SCAR)=%d  Σ lift handed by thin samples=%+d SCAR'%(len(m4),len(mat),R(sum(x['lift_scar'] for x in mat))))
print('  top 20 lifted:')
print('  %-22s %-9s %3s %-6s %6s %6s  %s'%('player','pos','n','branch','liftSC','native','thin-hot seasons (yr,g,avg)'))
for x in m4[:20]:
    print('  %-22s %-9s %3d %-6s %+6d %6d  %s'%(x['player'][:22],x['pos'],x['n'],x['branch'][:6],R(x['lift_scar']),R(x['native_num']),x['thin_hot']))
