"""#334 s4a1 — THE COMPOSITION CHECK: is composing the surprise demand with stage 4's pedigree demand
DOUBLE-CHARGING, and does ADDITIVE or MULTIPLICATIVE composition charge the shared channel better?

The directive's instruction: compose with (do not delete) stage 4's machinery UNLESS composition is
genuinely double-charging -- in which case say so, show the measurement, and prefer the surprise form as
primary with the sit-out prior effect retained. This file is that measurement."""
import os,sys,io,json,contextlib,copy,math
import numpy as np
REPO=os.environ.get('RL_REPO','/home/claude/amend1_landing')
WORKDIR=os.environ.get('RL_WORKDIR','/home/claude/amend1_ws/rl_after')
OUT=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,REPO+'/vendor'); os.chdir(WORKDIR); sys.path.insert(0,'.')
G={'__name__':'_s4a1_comp'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0],G)
MA=G['MA']; cp=G['cp']; Y=2026
L=[]
def say(x=''): L.append(x); print(x)
MRAZ=next(x for x in MA.data if x.get('key')=='noah-mraz')
fe=G['_fEy'](Y,MRAZ); tau=max(0.0,Y-cp.debutyr(MRAZ))+fe**1.5
cls=G['_sitout_cls'](MA.gfut(MRAZ)); pk=MA.effpk(MRAZ); R=G['_R_surf'](cls,pk,tau)
V0=G['entry_anchor'](MRAZ); ef=G['_prod_path'](MRAZ,Y)
gp=min(4/fe,6.0); lam=float(np.interp(gp,[0,1,2,3,4,5,6],G['LAM_SIT']))
q=G['_ped_prior'](MRAZ,Y,fe,tau,cls,pk); e4=1.0+G['PED_BAR']*(1.0-q)
u=1.0-G['_rho_res'](gp)/G['_RHO_SIT_BAR']; W=G['SUR_W']
say('='*112)
say('#334 STAGE B / STAGE 4 AMENDMENT 1 — THE COMPOSITION CHECK (double-charging, and additive vs multiplicative)')
say('='*112)
say('')
say('(1) THE SHARED CHANNEL, MEASURED. Stage 4 and the amendment overlap in EXACTLY ONE place: the sit-out')
say('    depth. It enters stage 4 through `sit` (a ratio of the retention surface) and it enters the')
say('    amendment through R, which discounts the anchor that s is measured against. Pedigree (the pick')
say('    axis) is NOT shared: it enters stage 4 only, and s does not read the pick at all except through R.')
say('')
s_disc=abs(math.log(ef/(R*V0))); s_undisc=abs(math.log(ef/V0))
sit=G['_R_surf'](cls,pk,tau)/G['_R_surf'](cls,pk,fe**1.5)
say('    Mraz, the calibration case:')
say('      anchor UNDISCOUNTED (entry_anchor)          : %10.2f'%V0)
say('      retention R at his sit-out depth            : %10.5f'%R)
say('      anchor DISCOUNTED (R x entry_anchor)        : %10.2f'%(R*V0))
say('      e_full                                      : %10.2f'%ef)
say('      s against the DISCOUNTED anchor  (SHIPPED)  : %10.6f nats'%s_disc)
say('      s against the UNDISCOUNTED anchor           : %10.6f nats'%s_undisc)
say('      => the sit-out discount contributes          %10.6f nats = %.1f%% of s'%(s_disc-s_undisc,100*(s_disc-s_undisc)/s_disc))
say('      stage 4 separately charges the same sit-out through sit = %.6f (q = ped %.6f x sit = %.6f)'%(sit,q/sit if sit else float('nan'),q))
say('')
say('    VERDICT ON DOUBLE-CHARGING: the overlap is REAL but it is NOT a double charge, for two reasons,')
say('    and the second is the decisive one.')
say('      (a) The two terms answer different questions about the same fact. `sit` asks "how much prior')
say('          expectation survives the year he did not play"; R inside s asks "what is his prior price')
say('          TODAY, which is what the evidence is actually contradicting". A sit-out lowers both the')
say('          expectation AND the baseline the claim is measured from, and both are true.')
say('      (b) THE ANCHOR CHOICE IS FORCED, not preferred. The blend is (1-lam)*anchor + lam*e_full.')
say('          If s were measured against the UNDISCOUNTED V0, then s would be NON-ZERO at the exact point')
say('          where lam cannot move the price at all (e_full == R*V0), and ZERO at a point where it can.')
say('          The statistic would not be measuring the re-rate the mechanism performs. Measured against')
say('          the discounted anchor, "s == 0" and "this change is inert" are THE SAME STATEMENT.')
say('    So stage 4 is COMPOSED WITH, not replaced, and the sit-out prior effect is retained in both.')
say('')
say('(2) ADDITIVE vs MULTIPLICATIVE, measured on the same landing.')
say('    additive       : exponent = 1 + PED_BAR*(1-q) + W*s*u        [SHIPPED]')
say("    multiplicative : exponent = (1 + PED_BAR*(1-q)) * (1 + W*s*u)  [the directive's offered form]")
say('')
def blend(E): 
    l=lam**E; return (1.0-l)*R*V0+l*ef
say('    On Mraz (lam raw %.6f, stage-4 exponent %.6f, s %.6f, u %.6f):'%(lam,e4,s_disc,u))
say('    %8s | %14s %10s | %14s %10s'%('W','additive exp','price','multipl. exp','price'))
for w in (0,1,2,3,4,5,6,8):
    ea=e4+w*s_disc*u; em=e4*(1.0+w*s_disc*u)
    say('    %8.1f | %14.6f %10.1f | %14.6f %10.1f'%(w,ea,blend(ea),em,blend(em)))
say('')
say('    The multiplicative form reaches the same Mraz landing at a smaller W (it scales the surprise demand')
say('    BY the pedigree demand, %.4f on Mraz). The reason the ADDITIVE form ships is the shared channel in'%e4)
say('    (1): multiplication charges the sit-out once through `sit`, once through R inside s, AND a third')
say('    time through their PRODUCT. Addition charges it once per term and no more. The exponent is')
say('    denominated in "passes of the lam ramp this record must clear", and two independent demands on the')
say('    same evidence SUM -- a pick-1 player with a huge claim and a pick-60 player with no claim should')
say("    each be charged their own demand, not each other's.")
say('')
say('    THE CONSEQUENCE, and it is the honest cost of the choice: under the additive form a top-pick player')
say('    with a big claim is charged the SAME surprise demand as a deep-pick player with the same claim, and')
say("    only stage 4's own term separates them. The pedigree pair still separates (PROBES.md §(c)); it")
say("    separates by stage 4's margin, not by a compounded one.")
open(os.path.join(OUT,'COMPOSITION_CHECK.txt'),'w').write('\n'.join(L)+'\n')
