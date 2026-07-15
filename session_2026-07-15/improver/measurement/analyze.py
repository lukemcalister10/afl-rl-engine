# Improver build — per-leg ablation, additivity, value-flow (item 130), named beneficiaries.
# Reads dumps: board_base (all off), board_eo2 / board_lsym / board_sage29 (single leg on), board_allon.
# Writes AFFECTED_ROWS.md + VALUE_FLOW.md.
import json, sys
M=sys.argv[1] if len(sys.argv)>1 else '.'
def load(n): return json.load(open(f'{M}/board_{n}.json'))
base=load('base'); allon=load('allon')
eo2=load('eo2'); lsym=load('lsym'); sage29=load('sage29')
keys=[k for k in base if 'error' not in base[k] and k in allon and 'error' not in allon[k]]
def movers(a,b): return [(k,b[k]['num']-a[k]['num']) for k in keys if b[k]['num']!=a[k]['num']]
def sd(mv): return sum(d for _,d in mv)
legs={'RL_EO2 (kill the _eo min())':eo2,'RL_LSYM (L-SYMMETRY)':lsym,'RL_SAGE29 (S_AGE 29-tail)':sage29}
out=[]; w=out.append
w("# AFFECTED-ROW LIST — THE IMPROVER BUILD (per-leg ablation + additivity) · candidate")
w("Base board 9a9889f8 (all three switches OFF) -> per-leg (one switch ON) -> all-on. num-SCAR = round(ev/1.0524),")
w("the currency the owner rules from (item 114). Three declared kill-switches => three separable legs.\n")
w("## Per-leg ablation (base -> single leg ON)")
per_leg_delta={}   # k -> sum of per-leg deltas
for name,brd in legs.items():
    mv=movers(base,brd)
    for k,d in mv: per_leg_delta[k]=per_leg_delta.get(k,0)+d
    w(f"- **{name}**: {len(mv)} movers · ΣΔ {sd(mv):+d} num-SCAR")
mv_all=movers(base,allon)
w(f"- **ALL THREE (combined)**: {len(mv_all)} movers · ΣΔ {sd(mv_all):+d} num-SCAR\n")
# additivity: max |Σ(per-leg Δ) - combined Δ| over players
allon_delta={k:allon[k]['num']-base[k]['num'] for k in keys}
allk=set(per_leg_delta)|set(allon_delta)
resid={k:abs(per_leg_delta.get(k,0)-allon_delta.get(k,0)) for k in allk}
maxres=max(resid.values()) if resid else 0
nz=sum(1 for k in allk if resid[k]!=0)
w("## Additivity")
w(f"- max|Σlegs − total| over all priced rows = **{maxres}** num-SCAR ({nz} rows with a nonzero leg-interaction residual)")
w(f"- Σ(Σ per-leg ΣΔ) = {sd(movers(base,eo2))+sd(movers(base,lsym))+sd(movers(base,sage29)):+d} vs combined ΣΔ {sd(mv_all):+d} "
  f"(legs 2 and 3 share the s=_S_AGE fraction, so a small interaction residual is expected & measured above)\n")
# complete combined affected list
w(f"## Complete affected list (combined base->all-on, {len(mv_all)} rows), sorted |Δ| desc")
w(f"{'player':26}{'pos':8}{'age':>4}{'base':>7}{'new':>7}{'Δ':>7}   {'lvlB->lvlN':>16}")
for k,d in sorted(mv_all,key=lambda t:-abs(t[1])):
    r=base[k]; nr=allon[k]
    w(f"{r['player'][:25]:26}{r['pos']:8}{r['age']:4.0f}{r['num']:7d}{nr['num']:7d}{d:+7d}   {r['lvl']:6.1f}->{nr['lvl']:6.1f}")
open(f'{M}/AFFECTED_ROWS.md','w').write('\n'.join(out))

# ---- VALUE-FLOW (item 130) ----
vf=[]; v=vf.append
sdall=sd(mv_all)
v("# VALUE-FLOW — THE IMPROVER BUILD (item 130, standing) · base 9a9889f8 -> all-on candidate")
v(f"- movers: **{len(mv_all)}** / {len(keys)} priced · **ΣΔ {sdall:+d} num-SCAR** (raw ev {sum(allon[k]['ev']-base[k]['ev'] for k in keys):+.0f})")
# age buckets
def agb(a):
    return '<=22' if a<=22 else ('23-26' if a<=26 else '>=27')
from collections import defaultdict
bk=defaultdict(lambda:[0,0])
for k,d in mv_all:
    b=agb(base[k]['age']); bk[b][0]+=1; bk[b][1]+=d
v("- age-bucket delta distribution:")
for b in ['<=22','23-26','>=27']:
    c,s=bk[b]; v(f"    {b:6}  {c:4} movers  ΣΔ {s:+d}")
lifts=sorted([m for m in mv_all if m[1]>0],key=lambda t:-t[1])[:3]
cuts =sorted([m for m in mv_all if m[1]<0],key=lambda t:t[1])[:3]
v("- three largest LIFTS by name:")
for k,d in lifts: v(f"    {base[k]['player'][:26]:26} {base[k]['pos']:8} age {base[k]['age']:.0f}  {base[k]['num']}->{allon[k]['num']} ({d:+d})")
v("- three largest CUTS by name:")
for k,d in cuts:  v(f"    {base[k]['player'][:26]:26} {base[k]['pos']:8} age {base[k]['age']:.0f}  {base[k]['num']}->{allon[k]['num']} ({d:+d})")
# named beneficiaries of the 29-tail study (item 127): Isaac Heeney, Bailey Dale — both AGE 30 in 2026, so
# the age-29 knot (leg 3) gives them ZERO; their all-on lift is leg 1 (RL_EO2) pulling L0 up to demonstrated
# production. The 30+ zero STANDS for them by design. Per-leg attribution shown.
def attr(k):
    return (f"eo2 {eo2[k]['num']-base[k]['num']:+d} / lsym {lsym[k]['num']-base[k]['num']:+d} / "
            f"sage29 {sage29[k]['num']-base[k]['num']:+d}")
v("- item-127 named names (Isaac Heeney, Bailey Dale) base->new [both AGE 30 => 29-tail=0; lift is RL_EO2]:")
for full in ['isaac heeney','bailey dale']:
    for k in [k for k in keys if base[k]['player'].lower()==full]:
        v(f"    {base[k]['player'][:26]:26} age {base[k]['age']:.0f}  num {base[k]['num']}->{allon[k]['num']} "
          f"({allon[k]['num']-base[k]['num']:+d})  lvl {base[k]['lvl']:.2f}->{allon[k]['lvl']:.2f}  [per-leg: {attr(k)}]")
# the ACTUAL 29-tail (leg-3) movers — as-of-age-29 rows only
s29=[(k,sage29[k]['num']-base[k]['num']) for k in keys if sage29[k]['num']!=base[k]['num']]
v(f"- the ACTUAL leg-3 (RL_SAGE29) footprint — {len(s29)} movers, ALL as-of-age 29 (30+ untouched), ΣΔ {sum(d for _,d in s29):+d}:")
for k,d in sorted(s29,key=lambda t:-abs(t[1])):
    v(f"    {base[k]['player'][:26]:26} age {base[k]['age']:.0f}  {base[k]['num']}->{sage29[k]['num']} ({d:+d})")
open(f'{M}/VALUE_FLOW.md','w').write('\n'.join(vf))
print('\n'.join(vf))
print(f"\n[additivity max|Σlegs-total| = {maxres}]  [combined {len(mv_all)} movers ΣΔ {sdall:+d}]")
print(f"[AFFECTED_ROWS.md + VALUE_FLOW.md written to {M}]")
