# THE ANCHOR HEAD, MEASURED HONESTLY.
# build_pvc_v34() reads SCALE (step 5 anchors to build_pvc(ALPHA), which is SCALE-dependent), and the
# module MUTATES SCALE at the anchor line (SCALE = SCALE * BOARD_FACTOR). So re-calling it after import
# gives a DIFFERENT number from the one the anchor actually used. Restore SCALE first, then measure.
import io,contextlib,json,config_manifest
config_manifest.enforce()
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open('rl_model.py').read(),'rl_model.py','exec'), g)
BF=g['BOARD_FACTOR']; s=g['_NUM']['s']; H=g['_NUM']['H']
print('MEASURED FROM THE MODULE ITSELF')
print('  BOARD_FACTOR                 = %.10f'%BF)
print('  numeraire s                  = %.10f   (= 3000 / %.6f)'%(s,H))
print('  => the head the anchor used  = 3000 * s / BOARD_FACTOR = %.4f'%(3000.0*s/BF))
print()
# restore the pre-anchor SCALE and re-measure for real
import builtins
g['SCALE']=g['SCALE']/BF
raw=g['build_pvc_v34']()
print('RE-MEASURED WITH THE PRE-ANCHOR SCALE RESTORED')
print('  v3.4 pre-anchor head PVC[1]  =', raw[1])
print('  picks 1-6                    =', [raw[k] for k in range(1,7)])
print()
hist=g['hist']; effpk=g['effpk']
n=0
for p in hist:
    if p.get('key') in ('paddy-mccartin','thomas-boyd'): p['_pvc_exclude']=True; n+=1
from collections import defaultdict
eff=defaultdict(list)
for p in hist:
    if p.get('_pvc_exclude'): eff[p['year']].append(effpk(p))
slid=0
for p in hist:
    if not p.get('_pvc_exclude') and p['year'] in eff:
        e=effpk(p); up=sum(1 for x in eff[p['year']] if x<e)
        if up: p['_pvc_eff']=e-up; slid+=1
raw2=g['build_pvc_v34']()
print('WITH THE TWO EXCLUDED (flagged %d, slid %d in the cohort)'%(n,slid))
print('  v3.4 pre-anchor head PVC[1]  =', raw2[1], '  (%+.3f%%)'%(100*(raw2[1]/raw[1]-1)))
print('  picks 1-6                    =', [raw2[k] for k in range(1,7)])
print()
bf1=(3000.0/raw[1])*s; bf2=(3000.0/raw2[1])*s
print('  BOARD_FACTOR  %.9f -> %.9f  (%+.3f%%)'%(bf1,bf2,100*(bf2/bf1-1)))
print('  (module BOARD_FACTOR %.9f — agrees with bf1 to %.2e)'%(BF,abs(BF-bf1)))
print()
print('THE ADOPTED CURVE, for comparison')
print('  its own measured head        = %.4f  published at 3000  (s = %.6f)'%(H,s))
print('  shipped picks 1-6            =', [g['PVC'][k] for k in range(1,7)])
