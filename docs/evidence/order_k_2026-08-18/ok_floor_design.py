#!/usr/bin/env python3
"""ORDER K — the FADE FLOOR fix, designed on Order H's own fitted-sitter set."""
import json, math
SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
FM={'paddy-mccartin','thomas-boyd'}
GRP={'RUCK':'RUCK','KPD':'KPP','KPF':'KPP','MID':'SMALL','SD':'SMALL','SF':'SMALL'}
D2=0.5582775239783688
# Order D pooled
G0,G1,SN=0.1286221202379088,0.4535958546743124,1.7472066252064105
# Order H tall/small
TG0,TG1,HT=-0.8778138796894399,0.7100022285392401,-0.6921227120657417
SN2_WIRED=1.4284052406915069
A=json.load(open(SP+'/per_entrant_O32RFINAL.json'))
ROWS=[]
for r in A['recs']:
    if r['key'] in FM or not (r.get('teaches_curve') and r['type']=='ND'): continue
    if not (2005<=r['year']<=2020) or not r.get('pick') or not (1<=r['pick']<=64): continue
    ROWS.append(dict(key=r['key'],player=r['player'],pick=int(r['pick']),pos=r['pos'],
                     grp=GRP[r['pos']],g1=int(r.get('games_yr1') or 0)))
SAT=[r for r in ROWS if r['g1']==0]
print('population %d ; fitted sitters (g1==0) %d'%(len(ROWS),len(SAT)))
print('  sitters TALL %d  SMALL %d'%(sum(1 for r in SAT if r['grp'] in('KPP','RUCK')),
                                     sum(1 for r in SAT if r['grp']=='SMALL')))
def kpool(p):
    p=max(1.0,min(64.0,float(p)))
    return min(2.0,max(0.5,(G0+G1*math.log(p))/SN))
def s_t(p,tall):
    p=max(1.0,min(64.0,float(p)))
    return TG0+TG1*math.log(p)+(HT if tall else 0.0)
# ---- WIRED form (the defect) ----
def kap_wired(p,tall,sn):
    return min(2.0,max(0.5,s_t(p,tall)/sn))
# ---- FIX form: SMALL floor re-sited at the row's own pre-factor exponent ----
def kap_fix(p,tall,sn):
    k=s_t(p,tall)/sn
    if tall: return min(2.0,max(0.5,k))
    return min(2.0,max(kpool(p),k))
def solve(kfn):
    lo,hi=0.05,40.0
    def ident(sn):
        return sum(D2**kfn(r['pick'],r['grp'] in('KPP','RUCK'),sn) for r in SAT)/len(SAT)-D2
    for _ in range(300):
        mid=0.5*(lo+hi)
        if ident(mid)<0: lo=mid
        else: hi=mid
    sn=0.5*(lo+hi)
    return sn,ident(sn)
r_wired=sum(D2**kap_wired(r['pick'],r['grp'] in('KPP','RUCK'),SN2_WIRED) for r in SAT)/len(SAT)-D2
print('\nWIRED  s_norm-prime=%.16f  identity residual %.3e'%(SN2_WIRED,r_wired))
sn_re,res_re=solve(kap_wired)
print('  re-solve of the WIRED form reproduces  s_norm-prime=%.16f  residual %.3e'%(sn_re,res_re))
SN_FIX,RES_FIX=solve(kap_fix)
print('\nFIX    s_norm-prime=%.16f  identity residual %.3e'%(SN_FIX,RES_FIX))
print('       (wired %.10f -> fix %.10f ; delta %+.3e)'%(SN2_WIRED,SN_FIX,SN_FIX-SN2_WIRED))
print('\n pick | kpool  | WIRED small tall | FIX small tall | fade wired S/T | fade fix S/T | small chg wired/fix')
for p in list(range(1,25))+[25,30,40,50,64]:
    kp=kpool(p)
    ws_,wt=kap_wired(p,False,SN2_WIRED),kap_wired(p,True,SN2_WIRED)
    fs,ft=kap_fix(p,False,SN_FIX),kap_fix(p,True,SN_FIX)
    print('%5d | %.4f | %.4f %.4f | %.4f %.4f | %.4f %.4f | %.4f %.4f | %+7.2f%% %+7.2f%%'%(
        p,kp,ws_,wt,fs,ft,D2**ws_,D2**wt,D2**fs,D2**ft,
        100*(D2**ws_/D2**kp-1),100*(D2**fs/D2**kp-1)))
print('\nSMALLS MADE LIGHTER (fade multiplier UP vs pooled) — wired vs fix:')
lw=[p for p in range(1,65) if D2**kap_wired(p,False,SN2_WIRED)>D2**kpool(p)+1e-12]
lf=[p for p in range(1,65) if D2**kap_fix(p,False,SN_FIX)>D2**kpool(p)+1e-12]
print('  WIRED: picks',lw)
print('  FIX  : picks',lf if lf else 'NONE')
print('\nTALL relief retained (fade multiplier vs pooled):')
for p in [7,10,13,16,24,30,40,55,64]:
    print('  pick %2d  wired %+6.2f%%   fix %+6.2f%%'%(p,100*(D2**kap_wired(p,True,SN2_WIRED)/D2**kpool(p)-1),
                                                       100*(D2**kap_fix(p,True,SN_FIX)/D2**kpool(p)-1)))
print('\nFLOOR BINDING under the FIX:')
tb=[p for p in range(1,65) if abs(kap_fix(p,True,SN_FIX)-0.5)<1e-12]
sb=[p for p in range(1,65) if abs(kap_fix(p,False,SN_FIX)-kpool(p))<1e-12]
sb05=[p for p in sb if abs(kpool(p)-0.5)<1e-12]
print('  TALL on the 0.5 floor : picks %s (%d)'%((('%d-%d'%(min(tb),max(tb))) if tb else 'none'),len(tb)))
print('  SMALL on the re-sited floor (its own pooled exponent): picks %s (%d)'%(
    (('%d-%d'%(min(sb),max(sb))) if sb else 'none'),len(sb)))
print('  ...of which also on the 0.5 hard floor (pooled itself clipped): picks %s (%d)'%(
    (('%d-%d'%(min(sb05),max(sb05))) if sb05 else 'none'),len(sb05)))
print('\nCONTINUITY of the FIX small curve (max of two smooth curves): max |jump| over pick grid 1..64 step .01')
mx=0.0;at=0
pp=1.0
prev=kap_fix(pp,False,SN_FIX)
while pp<64.0:
    pp=round(pp+0.01,2)
    c=kap_fix(pp,False,SN_FIX)
    if abs(c-prev)>mx: mx=abs(c-prev); at=pp
    prev=c
print('  max step %.3e at pick %.2f  (a 0.01-pick step; smooth, no cliff)'%(mx,at))
json.dump(dict(s_norm_fix=SN_FIX,residual_fix=RES_FIX,s_norm_wired=SN2_WIRED,residual_wired=r_wired,
               n_sat=len(SAT),lighter_wired=lw,lighter_fix=lf,tall_floor_picks=tb,small_floor_picks=sb),
          open(SP+'/ok/FLOOR_DESIGN.json','w'),indent=1)
