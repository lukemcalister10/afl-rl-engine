# Base(800bf461, schedule fade) -> Rework(evidence fade) ablation.
# RAW board moves in numeraire SCAR (round(ev/1.0524)) — the list the owner rules from (item 114).
import json, sys
M=sys.argv[1] if len(sys.argv)>1 else '.'
base=json.load(open(f'{M}/rboard_base.json')); rew=json.load(open(f'{M}/rboard_rework.json'))
keys=[k for k in base if 'error' not in base[k] and k in rew and 'error' not in rew[k]]
def n(d,k): return d[k]['num']
def rev(d,k): return d[k]['ev']

# separability: every NON-gap player must be byte-identical (the change is in the absence path only)
movers=[(k, n(rew,k)-n(base,k)) for k in keys if n(rew,k)!=n(base,k)]
gap_movers=[(k,d) for k,d in movers if base[k].get('gap')]
nongap_movers=[(k,d) for k,d in movers if not base[k].get('gap')]

out=[]; w=out.append
w("# AFFECTED-ROW LIST — R100.11 rework (schedule fade -> evidence fade) · candidate")
w("Base board 800bf461 (schedule fade, the pinned base) -> Rework board 24159c49 (evidence fade pw(g)).")
w("RAW board moves, numeraire SCAR = round(ev/1.0524). Sorted by |Δ|. Single lever => one leg (path-additive trivially).\n")
w(f"## Separability / additivity")
w(f"- total priced rows compared: {len(keys)}")
w(f"- rows that MOVE base->rework: {len(movers)}   (all carry a gap: {len(nongap_movers)==0})")
w(f"- NON-gap movers (must be 0 — separability): {len(nongap_movers)}")
if nongap_movers:
    for k,d in nongap_movers[:20]: w(f"    !! {base[k]['player']} {d:+d}  (NO GAP — investigate)")
sd=sum(n(rew,k)-n(base,k) for k in keys)
sdr=sum(rev(rew,k)-rev(base,k) for k in keys)
w(f"- ΣΔ over all rows: {sd:+d} num-SCAR   (raw ev {sdr:+.0f})   — the board's net move\n")

w(f"## The complete affected list ({len(movers)} rows), sorted |Δ| desc")
w(f"{'player':26}{'pos':9}{'base':>6}{'rework':>7}{'Δ':>6}  gap(age_pre/ret/gpost) lvlB->lvlR")
for k,d in sorted(movers, key=lambda t:-abs(t[1])):
    g=base[k].get('gap') or {}
    gr=rew[k].get('gap') or {}
    gtxt=f"a{g.get('age_pre')}/ret{g.get('ret')}/g{gr.get('gpost')}"
    w(f"{base[k]['player'][:25]:26}{base[k]['pos']:9}{n(base,k):6d}{n(rew,k):7d}{d:+6d}  {gtxt:24} {base[k]['lvl']:.1f}->{rew[k]['lvl']:.1f}")

# named rows
w("\n## Named rows")
for nm in ['Bailey Smith','Jack Buller','Darcy Wilmot']:
    kk=[k for k in keys if base[k]['player']==nm]
    if not kk: w(f"- {nm}: NOT ON BOARD"); continue
    k=kk[0]; g=rew[k].get('gap') or base[k].get('gap')
    w(f"- {nm}: base {n(base,k)} -> rework {n(rew,k)}  (Δ {n(rew,k)-n(base,k):+d})  lvl {base[k]['lvl']:.2f}->{rew[k]['lvl']:.2f}  gap(rework)={g}")
print('\n'.join(out))
