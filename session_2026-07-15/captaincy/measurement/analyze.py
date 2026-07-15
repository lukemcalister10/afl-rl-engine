# L-CAPTAIN wire — base (RL_CAPT=0, retired saturating) vs cand (RL_CAPT=1, ruled curve).
# Writes AFFECTED_ROWS.md (every mover + the credit it earned) + VALUE_FLOW.md (item 130) + CREDITS.md
# (Gawn/Bont/Daicos achieved vs the fitted references). Currency = num-SCAR = round(ev/1.0524).
import json, sys
from collections import defaultdict
M=sys.argv[1] if len(sys.argv)>1 else '.'
def load(n): return json.load(open(f'{M}/board_{n}.json'))
base=load('base'); cand=load('cand')
keys=[k for k in base if 'error' not in base[k] and k in cand and 'error' not in cand[k]]
mv=[(k,cand[k]['num']-base[k]['num']) for k in keys if cand[k]['num']!=base[k]['num']]
sdall=sum(d for _,d in mv)
raw=sum(cand[k]['ev']-base[k]['ev'] for k in keys)

# ---- AFFECTED_ROWS ----
out=[]; w=out.append
w("# AFFECTED-ROW LIST — L-CAPTAIN RULED CURVE (base RL_CAPT=0 retired saturating -> cand RL_CAPT=1 ruled) · candidate")
w("num-SCAR = round(ev/1.0524), the currency the owner rules from (item 114). credit(L) = the captaincy credit")
w("at the current-year projected level L: RULED = G*integral[BAR->L]P; SAT = the retired saturating value. Δcr =")
w("RULED-SAT is the marginal captaincy repricing that drives Δnum through the level->value legs (current + every")
w(f"projected future year in the band).\n")
w(f"## Summary: **{len(mv)}** movers / {len(keys)} priced · ΣΔ **{sdall:+d}** num-SCAR (raw ev {raw:+.0f})\n")
w(f"{'player':26}{'pos':8}{'age':>4}{'lvl':>7}{'crSAT':>7}{'crRULE':>7}{'Δcr':>7}{'base':>7}{'new':>7}{'Δnum':>7}")
for k,d in sorted(mv,key=lambda t:-abs(t[1])):
    r=base[k]; nr=cand[k]
    w(f"{r['player'][:25]:26}{r['pos']:8}{r['age']:4.0f}{nr['lvl']:7.1f}{nr['cr_sat']:7.2f}{nr['cr_ruled']:7.2f}"
      f"{nr['cr_ruled']-nr['cr_sat']:+7.2f}{r['num']:7d}{nr['num']:7d}{d:+7d}")
open(f'{M}/AFFECTED_ROWS.md','w').write('\n'.join(out))

# ---- VALUE_FLOW (item 130) ----
vf=[]; v=vf.append
v("# VALUE-FLOW — L-CAPTAIN RULED CURVE (item 130, standing) · base 800d0399 (RL_CAPT=0) -> cand (RL_CAPT=1)")
v(f"- movers: **{len(mv)}** / {len(keys)} priced · **ΣΔ {sdall:+d} num-SCAR** (raw ev {raw:+.0f})")
def agb(a): return '<=22' if a<=22 else ('23-26' if a<=26 else '>=27')
bk=defaultdict(lambda:[0,0])
for k,d in mv:
    b=agb(base[k]['age']); bk[b][0]+=1; bk[b][1]+=d
v("- age-bucket delta distribution:")
for b in ['<=22','23-26','>=27']:
    c,s=bk[b]; v(f"    {b:6}  {c:4} movers  ΣΔ {s:+d}")
lifts=sorted([m for m in mv if m[1]>0],key=lambda t:-t[1])[:3]
cuts =sorted([m for m in mv if m[1]<0],key=lambda t:t[1])[:3]
v("- three largest LIFTS by name:")
for k,d in lifts: v(f"    {base[k]['player'][:26]:26} {base[k]['pos']:8} age {base[k]['age']:.0f}  lvl {cand[k]['lvl']:.1f}  {base[k]['num']}->{cand[k]['num']} ({d:+d})  credit {cand[k]['cr_sat']:.2f}->{cand[k]['cr_ruled']:.2f}")
v("- three largest CUTS by name:")
for k,d in cuts:  v(f"    {base[k]['player'][:26]:26} {base[k]['pos']:8} age {base[k]['age']:.0f}  lvl {cand[k]['lvl']:.1f}  {base[k]['num']}->{cand[k]['num']} ({d:+d})  credit {cand[k]['cr_sat']:.2f}->{cand[k]['cr_ruled']:.2f}")
# net direction: is this a young-strip? (the recorded caution: the curve lifts young upper tails)
v(f"- direction: net ΣΔ {sdall:+d}; the curve is a pure captaincy REPRICE (credit rises at high L, and the retired")
v(f"  saturating cap is removed at the very top). No store/config move. Young upper tails that clear the bar are")
v(f"  lifted (the recorded A-PAIRS pair-3 caution).")
open(f'{M}/VALUE_FLOW.md','w').write('\n'.join(vf))

# ---- CREDITS: Gawn/Bont/Daicos achieved vs fitted references ----
cr=[]; c=cr.append
c("# ACHIEVED CREDITS vs FITTED REFERENCES — L-CAPTAIN (CONSTRAINTS PART 5)")
c("Fitted references (curve fit to the realized armband record, held-out ranks reproduced): Gawn 16.34 · Bont 9.85 · Daicos 4.96.")
c("Achieved = the ruled credit at the engine's current-year projected level L for each player.\n")
c(f"{'player':22}{'lvl':>8}{'crRULED':>9}{'fitted':>8}{'Δ':>7}")
REF={'max gawn':16.34,'marcus bontempelli':9.85,'nick daicos':4.96}
def find(nmlow):
    for k in keys:
        if base[k]['player'].lower()==nmlow: return k
    for k in keys:
        if nmlow in base[k]['player'].lower(): return k
    return None
for nm,ref in REF.items():
    k=find(nm)
    if k: c(f"{cand[k]['player'][:21]:22}{cand[k]['lvl']:8.2f}{cand[k]['cr_ruled']:9.2f}{ref:8.2f}{cand[k]['cr_ruled']-ref:+7.2f}")
    else: c(f"{nm:22}   NOT FOUND")
open(f'{M}/CREDITS.md','w').write('\n'.join(cr))

# ---- A-PAIRS (acceptance_v1_15 id A-PAIRS; computed from the board, base->cand) ----
def byname(dump, key_lower, poshint=None):
    cand_hits=[k for k in dump if 'error' not in dump[k] and dump[k]['player'].lower()==key_lower]
    return cand_hits[0] if cand_hits else None
# resolve keys once on the base dump
def find_player(nmlow):
    for k in keys:
        if base[k]['player'].lower()==nmlow: return k
    return None
kg=find_player('max gawn'); kb=find_player('kieren briggs'); kr=find_player('harley reid')
kbo=find_player('marcus bontempelli'); ks=find_player('ryley sanders')
ap=[]; a=ap.append
a("# A-PAIRS — scored base (800d0399) -> cand (ruled curve). acceptance_v1_15 id A-PAIRS. num-SCAR.")
def num(d,k): return d[k]['num'] if k else None
def pct(l,r): return (l-r)/r*100.0 if (l is not None and r) else None
# pair_1 gawn/briggs (owner-on-sight ratio)
if kg and kb:
    a(f"- **pair_1 gawn/briggs** (owner-on-sight): base {num(base,kg)}/{num(base,kb)}={num(base,kg)/num(base,kb):.3f}x "
      f"-> cand {num(cand,kg)}/{num(cand,kb)}={num(cand,kg)/num(cand,kb):.3f}x")
# pair_2 reid/bont (PARITY +/-10%)
if kr and kbo:
    pb=pct(num(base,kr),num(base,kbo)); pcv=pct(num(cand,kr),num(cand,kbo))
    a(f"- **pair_2 reid/bont** (PARITY band +/-10%): base reid {num(base,kr)} vs bont {num(base,kbo)} = {pb:+.1f}% "
      f"[{'PASS' if abs(pb)<=10 else 'FAIL'}] -> cand {num(cand,kr)} vs {num(cand,kbo)} = {pcv:+.1f}% "
      f"[{'PASS' if abs(pcv)<=10 else 'FAIL'}]")
# pair_3 sanders/bont (read: bont ABOVE sanders; band [0,10]% below; sanders above bont = FAIL; EXPECTED TO WORSEN)
if ks and kbo:
    pb=pct(num(base,ks),num(base,kbo)); pcv=pct(num(cand,ks),num(cand,kbo))
    a(f"- **pair_3 sanders/bont** (read: bont above sanders; sanders should sit 0-10% BELOW bont): "
      f"base sanders {num(base,ks)} vs bont {num(base,kbo)} = {pb:+.1f}% [{'PASS' if -10<=pb<=0 else 'FAIL (sanders above bont)'}] "
      f"-> cand sanders {num(cand,ks)} vs bont {num(cand,kbo)} = {pcv:+.1f}% [{'PASS' if -10<=pcv<=0 else 'FAIL (sanders above bont)'}]")
    a(f"  EXPECTED-TO-WORSEN (recorded caution): the ruled curve lifts young upper tails that clear the bar; "
      f"pair_3 moves {pb:+.1f}% -> {pcv:+.1f}% ({'WORSENED' if pcv>pb else 'improved'} by {pcv-pb:+.1f}pp). "
      f"No hand-edit (an anchor is a diagnostic, not a target).")
open(f'{M}/A_PAIRS.md','w').write('\n'.join(ap))

print('\n'.join(vf)); print(); print('\n'.join(cr)); print(); print('\n'.join(ap))
print(f"\n[AFFECTED_ROWS.md + VALUE_FLOW.md + CREDITS.md written to {M}]  [{len(mv)} movers ΣΔ {sdall:+d}]")
