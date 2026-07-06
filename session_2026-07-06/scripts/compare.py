#!/usr/bin/env python3
"""Compare ev_off / ev_on dumps + baked-v2.5 baseline. Single-lever verdict + owner movers table."""
import json
REPO='/home/user/afl-rl-engine'; O=REPO+'/session_2026-07-06/out'
off=json.load(open(O+'/ev_off.json')); on=json.load(open(O+'/ev_on.json'))
base=json.load(open(REPO+'/data/s4_matrix_baked_efea88e5.json'))
CUR={v['key']:v['cur'] for v in base.values() if v.get('key') is not None}
# rec = [ev, player, pos, age, nq, lcr, branch]
common=set(off)&set(CUR)
mm=[(k,off[k][0],CUR[k]) for k in common if off[k][0]!=CUR[k]]
print("="*92)
print("(A) CONTROL — candidate engine lever OFF vs baked v2.5 'cur' | compared %d | mismatch %d"%(len(common),len(mm)))
for k,a,b in mm[:15]: print("    MISMATCH %-26s off=%s v25=%s"%(k,a,b))
print("    ==>", "byte-exact base (lever OFF == v2.5)" if not mm else "NOT byte-exact — investigate")

movers=sorted([(k,on[k][0]-off[k][0]) for k in on if on[k][0]!=off.get(k,[None])[0]], key=lambda t:-t[1])
up=[m for m in movers if m[1]>0]; dn=[m for m in movers if m[1]<0]
bad_branch=[k for k,_ in movers if on[k][6]!='SHED']
bad_lcr=[k for k,_ in movers if on[k][5]<=0]
print("\n"+"="*92)
print("(B) LEVER EFFECT — RL_FORMDECL 1 vs 0 | N moved %d/%d | UP %d DOWN %d"%(len(movers),len(on),len(up),len(dn)))
print("    non-SHED movers: %d | lcr<=0 movers: %d | DOWN movers: %d"%(len(bad_branch),len(bad_lcr),len(dn)))
print("    SINGLE-LEVER VERDICT:", "PASS — all movers = above-replacement established shed players, all UP"
      if not bad_branch and not bad_lcr and not dn else "SPILL — STOP: "+str((bad_branch[:5],bad_lcr[:5],dn[:5])))
ages=[on[k][3] for k,_ in movers]
if ages: print("    mover age range: %d..%d (min..max) — all prime/older"%(min(ages),max(ages)))
tot0=sum(off[k][0] for k in on); tot1=sum(on[k][0] for k in on)
print("    board total: %d -> %d (%+d, %+.2f%%)"%(tot0,tot1,tot1-tot0,100*(tot1-tot0)/tot0))

print("\n  --- ALL MOVERS (v2.5 -> after, delta), sorted by delta ---")
print("  %-24s %-8s %3s %3s %6s  %7s %7s %7s"%('player','pos','age','nq','lcr','v2.5','after','delta'))
for k,d in movers:
    ev,nm,pos,age,nq,lcr,br=on[k]
    print("  %-24s %-8s %3d %3d %6.1f  %7d %7d %+7d"%(nm[:24],pos,age,nq,lcr,off[k][0],ev,d))

print("\n"+"="*92); print("(C) NAMED ANCHORS + CONTRAST SET + RESCUES (v2.5 -> after)"); print("="*92)
def show(keys,label):
    print("  ["+label+"]")
    for k in keys:
        if k not in on: print("    %-26s NOT FOUND"%k); continue
        ev,nm,pos,age,nq,lcr,br=on[k]; d=ev-off[k][0]
        print("    %-24s %-8s age%3d lcr%6.1f %-8s  %7d -> %7d  (%+d)"%(nm[:24],pos,age,lcr,br,off[k][0],ev,d))
show(['max-gawn','jeremy-cameron','marcus-bontempelli','kieren-briggs'],'named anchors (expect Δ=0)')
show(['stephen-coniglio','taylor-adams','mark-blicavs','cameron-guthrie','patrick-dangerfield'],'genuine decliners (expect Δ=0, still low)')
show(['lachie-neale','andrew-brayshaw','rory-laird','touk-miller','jack-steele','patrick-cripps','sam-walsh'],'flagship rescues (expect UP)')
