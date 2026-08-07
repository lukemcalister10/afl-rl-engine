"""#334 stage B / STAGE 4 AMENDMENT 1 — THE NEAR-PROJECTION PROOF.

THE OWNER'S NO-REBALANCE CONDITION, verbatim from the directive: no broad hit to young players; players
performing NEAR PROJECTION keep today's reactivity. The amendment is supposed to shrink ONLY records that
claim a large re-rate off a thin sample. This file proves that on the BUILT BOARD, programmatically.

DEFINITIONS, stated before they are measured, so nothing is chosen after the fact.
  population  : every board player on the THIN-RECORD (sit-out) path, i.e. routed through sitout_ev by
                the ns==0 arm of ev(), who has live 2026 evidence (games > 0). A player with no games has
                lam == 0 and is byte-exact by construction; he is counted in the denominators and shown.
  projection  : anchor_full = R x entry_anchor(p) — the PRIOR-IMPLIED FULL PRICE, the same anchor leg the
                blend itself uses (the choice is argued in MEMO.md §2; it is the pairing that makes
                "zero surprise" and "this change is inert" the same statement).
  the band    : |log(e_full / anchor_full)| <= log(1.25), i.e. the demonstrated level sits within +/-25%
                of the projection. This is the directive's band, converted to the statistic's own units.
  moved       : the exported board value v changed at all (integer board points).

TWO RULERS ARE REPORTED, and the difference between them is the whole finding.
  (1) CONTINUOUS: the relative change in the engine's own real-valued price for that player, sitout_ev
      before vs after. This is the economics of the change.
  (2) INTEGER BOARD: the relative change in the exported integer board value v. This is what the owner
      reads, and on a small-valued row a single board point is already a large percentage.
"""
import os, sys, io, json, contextlib, math
import numpy as np
REPO=os.environ.get('RL_REPO','/home/claude/amend1_landing')
WORKDIR=os.environ.get('RL_WORKDIR','/home/claude/amend1_ws/rl_after')
OUT=os.path.dirname(os.path.abspath(__file__))
OLD=sys.argv[1]; NEW=sys.argv[2]
sys.path.insert(0,REPO+'/vendor'); os.chdir(WORKDIR); sys.path.insert(0,'.')
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
G={'__name__':'_s4a1_np'}
with contextlib.redirect_stdout(io.StringIO()): exec(src,G)
MA=G['MA']; cp=G['cp']; Y=2026
def rows(d):
    r=d['active'] if isinstance(d,dict) and 'active' in d else d
    return list(r.values()) if isinstance(r,dict) else r
A={p['key']:p for p in rows(json.load(open(OLD))) if p.get('v') is not None}
B={p['key']:p for p in rows(json.load(open(NEW)))  if p.get('v') is not None}
bykey={p.get('key'):p for p in MA.data if p.get('key')}
BAND=math.log(1.25)
def price_at(p,W):
    G['SUR_W']=float(W); MA._pe_clear(); G['_V0C'].clear(); G['_V0U'].clear()
    return G['sitout_ev'](p,Y,G['_prod_path'](p,Y))
SURW=G['SUR_W']
pop=[]
for k in sorted(set(A)&set(B)):
    p=bykey.get(k)
    if p is None or G['delisted'](p): continue
    try:
        if G['nseas_pro'](p,Y)!=0: continue
    except Exception: continue
    fe=G['_fEy'](Y,p); tau=max(0.0,Y-cp.debutyr(p))+((fe**1.5) if Y>=cp.debutyr(p) else 0.0)
    cls=G['_sitout_cls'](MA.gfut(p)); pk=MA.effpk(p); R=G['_R_surf'](cls,pk,tau)
    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y)
    ef=G['_prod_path'](p,Y); anch=R*G['entry_anchor'](p)
    s=abs(float(np.log(ef/anch))) if (ef>0 and anch>0) else 0.0
    pop.append(dict(key=k,name=p.get('player'),pos=MA.gfut(p),pk=pk,gy=gy,ef=ef,anch=anch,s=s,
                    ratio=ef/anch,old=A[k]['v'],new=B[k]['v'],p=p))
L=[]
def say(x=''): L.append(x); print(x)
say('='*116)
say('#334 STAGE B / STAGE 4 AMENDMENT 1 — THE NEAR-PROJECTION PROOF (the owner\'s no-rebalance condition)')
say('board b490ae8b (stage 4)  ->  b56bbddea15f (amendment 1)     RL_SUR_W = %.4g'%SURW)
say('='*116)
live=[x for x in pop if x['gy']>0]; dead=[x for x in pop if x['gy']<=0]
band=[x for x in live if x['s']<=BAND]
outb=[x for x in live if x['s']>BAND]
say('')
say('DENOMINATORS')
say('  board rows compared                                        : %d'%len(set(A)&set(B)))
say('  on the THIN-RECORD (sit-out) path                          : %d'%len(pop))
say('    ... with NO 2026 games (lam==0, byte-exact by construction): %d   moved: %d'%(len(dead),len([x for x in dead if x['old']!=x['new']])))
say('    ... with live 2026 evidence (the reactivity population)   : %d   moved: %d'%(len(live),len([x for x in live if x['old']!=x['new']])))
say('  WITHIN +/-25%% OF PROJECTION  (s <= log(1.25) = %.6f)       : %d   moved: %d'%(BAND,len(band),len([x for x in band if x['old']!=x['new']])))
say('  outside the band                                           : %d   moved: %d'%(len(outb),len([x for x in outb if x['old']!=x['new']])))
say('')
say('THE BAND, PLAYER BY PLAYER  (n=%d, NO CAP)'%len(band))
say('-'*116)
say('%-26s %-5s %-20s %4s %8s %8s %8s %8s %10s %10s'%('player','pos','entry','g26','ev/prior','s','old v','new v','board rel','cont rel'))
say('-'*116)
maxb=0.0; maxc=0.0
for x in sorted(band,key=lambda z:-z['s']):
    p0=price_at(x['p'],0.0); p1=price_at(x['p'],SURW)
    c=(p1-p0)/p0; b=(x['new']-x['old'])/x['old'] if x['old'] else 0.0
    maxb=max(maxb,abs(b)); maxc=max(maxc,abs(c))
    ent=('%s pick %s'%(x['p'].get('type') or '?', x['p'].get('pick'))) if not MA.is_pool(x['p']) else '%s (pool, effpk %d)'%(x['p'].get('type') or '?',x['pk'])
    say('%-26s %-5s %-20s %4d %7.3fx %8.4f %8d %8d %9.3f%% %9.3f%%'%(
        (x['name'] or '?')[:26],x['pos'],ent[:20],x['gy'],x['ratio'],x['s'],x['old'],x['new'],100*b,100*c))
say('-'*116)
say('  MAX |rel| in band — CONTINUOUS engine price : %.4f%%'%(100*maxc))
say('  MAX |rel| in band — INTEGER board value     : %.4f%%'%(100*maxb))
say('')
say('THE ASSERTION')
say('-'*116)
okc = maxc < 0.01
okb = maxb < 0.01
say('  (1) CONTINUOUS  every near-projection player moves < 1%%  :  %s   (max %.4f%%)'%('PASS' if okc else 'FAIL',100*maxc))
say('  (2) INTEGER     every near-projection player moves < 1%%  :  %s   (max %.4f%%)'%('PASS' if okb else 'FAIL',100*maxb))
say('')
if not okb:
    say('  THE INTEGER RULER FAILS, AND IT IS REPORTED RATHER THAN FORCED. The whole excess is one row:')
    for x in sorted(band,key=lambda z:-z['s']):
        b=abs((x['new']-x['old'])/x['old']) if x['old'] else 0.0
        if b>=0.01:
            p0=price_at(x['p'],0.0); p1=price_at(x['p'],SURW)
            say('    %s  %s  board v %d -> %d  (%+d POINTS)'%(x['name'],x['pos'],x['old'],x['new'],x['new']-x['old']))
            say('      his CONTINUOUS move is %.4f%% — i.e. %.2f board points — which is UNDER the 1%% bar.'%(100*(p1-p0)/p0,abs((p1-p0)/p0)*x['old']))
            say('      but his board value is %d, so ONE board point is already %.3f%%, and the 1%% bar on this'%(x['old'],100.0/x['old']))
            say('      row means "moves by less than %.2f board points". The integer grid cannot express it.'%(0.01*x['old']))
    say('')
    say('  This is a MEASUREMENT-GRANULARITY result, not a re-rate: the engine moved him by less than one and')
    say('  a quarter board points and the board had to round it to two. It is stated as a FAILURE of the')
    say('  criterion as literally written, because it is one, and the owner should rule on it rather than')
    say('  have it smoothed away here. See MEMO.md §5 (THE TENSION) and README.md.')
say('')
say('FOR CONTRAST — THE POPULATION OUTSIDE THE BAND (what the change is FOR)')
say('-'*116)
mv=[x for x in outb if x['old']!=x['new']]
say('  outside the band: %d players, %d moved, mean |board rel| %.3f%%, max |board rel| %.3f%%'%(
    len(outb),len(mv),100*float(np.mean([abs((x['new']-x['old'])/x['old']) for x in mv])) if mv else 0.0,
    100*max((abs((x['new']-x['old'])/x['old']) for x in mv),default=0.0)))
say('  in the band    : %d players, %d moved, max |board rel| %.3f%%'%(len(band),len([x for x in band if x['old']!=x['new']]),100*maxb))
say('')
say('  MONOTONE SANITY: the band and the movers are ordered by s, not by pedigree, position or value.')
say('  Sorted by s, the mean |continuous rel| by quartile of the live population:')
ls=sorted(live,key=lambda z:z['s']); n=len(ls)
for qi in range(4):
    seg=ls[qi*n//4:(qi+1)*n//4]
    vals=[]
    for x in seg:
        p0=price_at(x['p'],0.0); p1=price_at(x['p'],SURW); vals.append(abs((p1-p0)/p0))
    say('    quartile %d of s  [%.4f .. %.4f]  n=%2d   mean |cont rel| = %7.3f%%'%(qi+1,seg[0]['s'],seg[-1]['s'],len(seg),100*float(np.mean(vals))))
open(os.path.join(OUT,'NEAR_PROJECTION_PROOF.txt'),'w').write('\n'.join(L)+'\n')
json.dump(dict(n_band=len(band),n_band_moved=len([x for x in band if x['old']!=x['new']]),
               max_rel_continuous=maxc,max_rel_integer=maxb,
               pass_continuous=bool(okc),pass_integer=bool(okb),
               n_path=len(pop),n_live=len(live),n_zero_games=len(dead),band_edge=BAND,SUR_W=SURW),
          open(os.path.join(OUT,'near_projection_proof.json'),'w'),indent=1)
