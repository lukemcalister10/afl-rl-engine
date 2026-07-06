#!/usr/bin/env python3
"""Single-lever movers diff for the form-conditioned decline curve (2026-07-06).
Prices every real board player with the lever OFF (RL_FORMDECL=0) and ON (=1) in the SAME candidate
engine, and against the baked-v2.5 baseline matrix (data/s4_matrix_baked_efea88e5.json, field 'cur').
Asserts single-lever: OFF == v2.5 (byte-exact), and every ON-vs-OFF mover is a prime/older established
above-replacement player moving UP. Prints the owner movers table. READ-ONLY."""
import io, contextlib, os, json
import numpy as np

REPO='/home/user/afl-rl-engine'
base=json.load(open(REPO+'/data/s4_matrix_baked_efea88e5.json'))
CUR={v['key']:v['cur'] for v in base.values() if v.get('key') is not None}

def price(formdecl):
    os.environ['RL_FORMDECL']=formdecl
    g={}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
    MA=g['MA']; ev=g['ev']; cp=g['cp']
    _lvlcurr=g['_lvlcurr']; _nqual=g['_nqual']; DOWN_TOL=g['DOWN_TOL']; PROVEN_N=g['PROVEN_N']
    lvl_eff_orig=cp._lvl_eff_orig; REPL=MA.REPL
    out={}; meta={}
    for p in MA.data:
        if not MA.GRP.get(p.get('pos')): continue
        k=p.get('key')
        if k is None: continue
        out[k]=ev(p,2026)
        if formdecl=='1':
            n=_nqual(p,2026); Lo=lvl_eff_orig(p,2026); Lc=_lvlcurr(p,2026)
            br='UP-hold' if (n>=PROVEN_N and Lc>=Lo) else ('SHED' if (n>=PROVEN_N and (Lo-Lc)>DOWN_TOL) else ('hold' if n>=PROVEN_N else 'thin'))
            meta[k]=(p['player'],MA.gfut(p),round(cp._age_asof(p,2026)),n,round(Lc-REPL.get(MA.gfut(p),0.0),1),br)
    return out,meta

ev0,_=price('0'); ev1,meta=price('1')

# (A) candidate-OFF must reproduce baked v2.5 (byte-exact board value)
off_vs_v25=[(k,ev0[k],CUR[k]) for k in ev0 if k in CUR and ev0[k]!=CUR[k]]
print("="*90)
print("(A) SINGLE-LEVER CONTROL — candidate engine, lever OFF (RL_FORMDECL=0) vs baked v2.5 'cur'")
print("    players compared: %d | mismatches: %d" % (len(set(ev0)&set(CUR)), len(off_vs_v25)))
if off_vs_v25:
    for k,a,b in off_vs_v25[:20]: print("      MISMATCH %-24s off=%s v25=%s"%(k,a,b))
    print("    ==> NOT byte-exact — investigate before proceeding")
else:
    print("    ==> byte-exact: the candidate engine with the lever OFF == baked v2.5. Clean base.")

# (B) the lever's effect: ON vs OFF (same engine)
movers=sorted([(k,ev1[k]-ev0[k]) for k in ev1 if ev1[k]!=ev0.get(k)], key=lambda t:-t[1])
print("\n"+"="*90)
print("(B) LEVER EFFECT — RL_FORMDECL=1 vs =0 (same candidate engine)")
print("    N moved: %d of %d  | UP: %d  DOWN: %d" %
      (len(movers), len(ev1), sum(1 for _,d in movers if d>0), sum(1 for _,d in movers if d<0)))
# single-lever assertions
bad_branch=[k for k,_ in movers if meta.get(k,('','','',0,0,'?'))[5]!='SHED']
bad_lcr=[k for k,_ in movers if meta.get(k,('','','',0,0,0,'',))[4]<=0]
down=[k for k,d in movers if d<0]
print("    movers not on SHED branch: %d | movers with lcr<=0: %d | DOWN movers: %d" %
      (len(bad_branch),len(bad_lcr),len(down)))
print("    single-lever verdict:", "PASS (all movers = above-replacement established shed players, all UP)"
      if not bad_branch and not bad_lcr and not down else "SPILL — STOP")

print("\n  --- ALL MOVERS (before -> after, delta), sorted by delta ---")
print("  %-24s %-8s %3s %3s %6s  %6s %6s %6s"%('player','pos','age','nq','lcr','v2.5','after','delta'))
for k,d in movers:
    nm,pos,age,nq,lcr,br=meta[k]
    print("  %-24s %-8s %3d %3d %6.1f  %6d %6d %+6d"%(nm[:24],pos,age,nq,lcr,ev0[k],ev1[k],d))

# (C) named anchors + genuine-decliner contrast set (must be Δ=0 / still-low)
print("\n"+"="*90)
print("(C) NAMED ANCHORS + GENUINE-DECLINER CONTRAST SET (before -> after)")
print("="*90)
def show(keys,label):
    print("  ["+label+"]")
    for k in keys:
        if k not in ev1: print("    %-24s NOT FOUND"%k); continue
        nm,pos,age,nq,lcr,br=meta.get(k,(k,'?',0,0,0,'?'))
        d=ev1[k]-ev0[k]
        print("    %-24s %-8s age%3d lcr%6.1f %-8s  %6d -> %6d  (%+d)"%(nm[:24],pos,age,lcr,br,ev0[k],ev1[k],d))
show(['max-gawn','jeremy-cameron','marcus-bontempelli','kieren-briggs'],'named anchors')
show(['stephen-coniglio','taylor-adams','mark-blicavs','cameron-guthrie','patrick-dangerfield'],'genuine decliners (must still be low / Δ=0)')
show(['lachie-neale','andrew-brayshaw','rory-laird','touk-miller','jack-steele','patrick-cripps'],'flagship rescues (still-elite dippers, expect UP)')

json.dump({'n_moved':len(movers),'off_vs_v25_mismatch':len(off_vs_v25),
           'movers':[{'key':k,'player':meta[k][0],'pos':meta[k][1],'age':meta[k][2],'lcr':meta[k][4],
                      'before':ev0[k],'after':ev1[k],'delta':d} for k,d in movers]},
          open(REPO+'/session_2026-07-06/out/movers.json','w'),indent=1)
print("\n  wrote session_2026-07-06/out/movers.json")
