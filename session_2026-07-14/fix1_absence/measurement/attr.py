import json, numpy as np
B=lambda f: json.load(open(f))
base=B('rboard_base.json'); fix1=B('rboard_fix1.json'); absb=B('rboard_abs.json'); both=B('rboard_both.json')
keys=[k for k in base if 'error' not in base[k]]
def num(d,k): return d[k]['num']
def ev(d,k): return d[k]['ev']

print("="*80)
print("P0 — ATTRIBUTION (3 ablated boards, path-additive; declared order Fix1 -> Absence)")
print("="*80)
# per-lever SCAR deltas (numeraire units)
def sumd(a,b): return sum(num(b,k)-num(a,k) for k in keys)
L1=sumd(base,fix1)          # Fix1 leg  (base -> +Fix1)
L2=sumd(fix1,both)          # Absence leg (+Fix1 -> +Fix1+Absence)
TOT=sumd(base,both)         # total
absAlone=sumd(base,absb)    # absence alone (for reporting)
def movers(a,b,th=1):
    m=[(k,num(b,k)-num(a,k)) for k in keys if abs(num(b,k)-num(a,k))>=th]
    up=sum(1 for _,d in m if d>0); dn=sum(1 for _,d in m if d<0)
    return len(m),up,dn
print(f"Fix1 leg   (base->fix1)      : ΣΔ = {L1:+d} num-SCAR   movers|Δ|>=1: {movers(base,fix1)}")
print(f"Absence leg(fix1->both)      : ΣΔ = {L2:+d} num-SCAR   movers|Δ|>=1: {movers(fix1,both)}")
print(f"  (absence ALONE base->abs   : ΣΔ = {absAlone:+d} num-SCAR   movers: {movers(base,absb)})")
print(f"BOTH total (base->both)      : ΣΔ = {TOT:+d} num-SCAR   movers|Δ|>=1: {movers(base,both)}")
print(f"PATH-ADDITIVITY: L1+L2 = {L1+L2:+d}  vs total {TOT:+d}   max|Σlegs-total| = {abs(L1+L2-TOT)}")
# raw (pre-numeraire) too
def sumdr(a,b): return sum(ev(b,k)-ev(a,k) for k in keys)
print(f"  (raw ev units: Fix1 {sumdr(base,fix1):+.0f}  Absence {sumdr(fix1,both):+.0f}  total {sumdr(base,both):+.0f})")

print()
print("="*80)
print("JAMARRA UGLE-HAGAN under (a) Fix1 alone, (b) Absence alone, (c) Both — numeraire SCAR")
print("="*80)
jk=[k for k in keys if 'ugle-hagan' in base[k]['player'].lower()][0]
print(f"  base                = {num(base,jk):5d}   (level {base[jk]['lvl']:.2f})")
print(f"  (a) Fix1 alone      = {num(fix1,jk):5d}   (level {fix1[jk]['lvl']:.2f})   Δ vs base {num(fix1,jk)-num(base,jk):+d}")
print(f"  (b) Absence alone   = {num(absb,jk):5d}   (level {absb[jk]['lvl']:.2f})   Δ vs base {num(absb,jk)-num(base,jk):+d}")
print(f"  (c) Both            = {num(both,jk):5d}   (level {both[jk]['lvl']:.2f})   Δ vs base {num(both,jk)-num(base,jk):+d}")
print(f"  gap info: {both[jk]['gap']}   scoring: {both[jk]['scoring']}")

print()
print("="*80)
print("P1a — FIX 1 MOVERS (|Δnum|>=1 base->fix1), sorted by |Δ|.  M4 list flagged.")
print("="*80)
M4={'peter-ladhams','aiden-o-driscoll','nathan-o-driscoll','deven-robertson','rhett-bazzo',
    'kane-mcauliffe','ned-moyle','sam-day','will-day','elijah-tsatas','josh-lindsay','xavier-lindsay',
    'campbell-chesser','jamarra-ugle-hagan'}
fm=sorted([(k,num(fix1,k)-num(base,k)) for k in keys if abs(num(fix1,k)-num(base,k))>=1],
          key=lambda t:-abs(t[1]))
print(f"  {len(fm)} Fix1 movers. Top 40 by |Δ|:")
print(f"  {'player':24}{'pos':8}{'base':>6}{'fix1':>6}{'Δ':>6}  {'lvlB->lvlF':>14}  M4")
for k,d in fm[:40]:
    tag='<<M4' if k in M4 else ''
    print(f"  {base[k]['player'][:23]:24}{base[k]['pos']:8}{num(base,k):6d}{num(fix1,k):6d}{d:+6d}  {base[k]['lvl']:6.1f}->{fix1[k]['lvl']:5.1f}  {tag}")
print("  --- M4 list explicit (even if |Δ|<1) ---")
for k in sorted(M4):
    if k in base:
        print(f"  {base[k]['player'][:23]:24}{base[k]['pos']:8}{num(base,k):6d}{num(fix1,k):6d}{num(fix1,k)-num(base,k):+6d}  {base[k]['lvl']:6.1f}->{fix1[k]['lvl']:5.1f}")
    else:
        print(f"  {k}: NOT ON BOARD")
