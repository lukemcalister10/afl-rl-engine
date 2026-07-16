# LEG A value-flow (item 130 standing check) + faces + watch rows. Reads board_off/on.json (RL_ISOFADE A/B).
# num = round(ev/1.0524) is the owner currency. "above projection" = Lc (demonstrated recency level) > par
# (pedigree par projection). HALT conditions: young (<=26) net-strip; any above-projection young cut.
import json, sys
from collections import defaultdict
M='/home/user/afl-rl-engine/session_2026-07-16/isofade/measurement'
off=json.load(open(f'{M}/board_off.json')); on=json.load(open(f'{M}/board_on.json'))
# active 804 board of record
act=json.load(open('/home/user/afl-rl-engine/data/rl_build/rl_app_data.json'))['active']
ACT={r['key'] for r in act}
def good(d): return isinstance(d,dict) and 'error' not in d
keys=[k for k in off if good(off[k]) and good(on.get(k,{}))]
akeys=[k for k in keys if k in ACT]
def dnum(k): return on[k]['num']-off[k]['num']
out=[]; w=out.append
w("# LEG A — VALUE-FLOW (item 130 standing check) · board_off (RL_ISOFADE=0 == v2.10 790136a3) -> board_on")
w(f"priced universe {len(keys)} · ACTIVE board {len(akeys)}/804. num-SCAR = round(ev/1.0524).\n")
for label,ks in [('ACTIVE-804 board',akeys),('full priced universe',keys)]:
    mv=[(k,dnum(k)) for k in ks if dnum(k)!=0]
    sd=sum(d for _,d in mv)
    lift=sum(1 for _,d in mv if d>0); cut=sum(1 for _,d in mv if d<0)
    w(f"## {label}: {len(mv)} movers · SigmaD {sd:+d} num-SCAR · {lift} lifted / {cut} cut")
# ---- cohort distribution (ACTIVE) ----
def agb(a): return '<=22' if a<=22 else ('23-26' if a<=26 else '>=27')
bk=defaultdict(lambda:[0,0,0])  # count, sumD, sum|D|
for k in akeys:
    d=dnum(k); b=agb(off[k]['age']); bk[b][0]+= (d!=0); bk[b][1]+=d; bk[b][2]+=abs(d)
w("\n## AGE-COHORT distribution (ACTIVE board) — item-130 no-young-net-strip check")
for b in ['<=22','23-26','>=27']:
    c,s,a=bk[b]; w(f"    {b:6}  {c:4} movers   netSigmaD {s:+7d}   grossSum|D| {a:7d}")
young_net = bk['<=22'][1]+bk['23-26'][1]
w(f"    YOUNG (<=26) net SigmaD = {young_net:+d}  => {'PASS (>=0, no net-strip)' if young_net>=0 else 'HALT (young net-strip!)'}")
# ---- over-performer scan (ACTIVE, young, above projection, CUT) ----
w("\n## OVER-PERFORMER SCAN (item-130 HALT) — young (<=26) ABOVE projection (Lc>par) that are CUT")
op=[]
for k in akeys:
    o=off[k]; d=dnum(k)
    if o['age']<=26 and o.get('pormargin',0)>0 and d<0:
        op.append((k,o['player'],o['pos'],o['age'],o['effpk'],o['pormargin'],o['Eq'],o['num'],on[k]['num'],d))
op.sort(key=lambda t:t[-1])
if not op:
    w("    NONE — no above-projection young player is cut. PASS.")
else:
    w(f"    {len(op)} above-projection young players CUT (candidate HALTs — inspect):")
    w(f"    {'player':24}{'pos':8}{'age':>4}{'pk':>4}{'Lc-par':>8}{'Eq':>5}{'off':>7}{'on':>7}{'d':>7}")
    for k,pl,po,ag,pk,pm,eq,o_,n_,d in op[:40]:
        w(f"    {pl[:23]:24}{po:8}{ag:>4.0f}{pk:>4}{pm:>8.1f}{eq:>5.1f}{o_:>7}{n_:>7}{d:>+7}")
# also: all young cuts (regardless of projection) for context
yc=sorted([(k,dnum(k)) for k in akeys if off[k]['age']<=26 and dnum(k)<0], key=lambda t:t[1])[:15]
w("\n## Largest YOUNG (<=26) cuts (context — below-projection cuts are two-directional, allowed):")
w(f"    {'player':24}{'pos':8}{'age':>4}{'pk':>4}{'Lc-par':>8}{'off':>7}{'on':>7}{'d':>7}")
for k,d in yc:
    o=off[k]; w(f"    {o['player'][:23]:24}{o['pos']:8}{o['age']:>4.0f}{o['effpk']:>4}{o.get('pormargin',0):>8.1f}{o['num']:>7}{on[k]['num']:>7}{d:>+7}")
# ---- faces + top lifts ----
w("\n## THE FACES (expected pure lifts) + top-15 lifts (ACTIVE)")
for nm in ['timothy-english','tristan-xerri','max-gawn','brodie-grundy','tom-de-koning','reilly-o-brien']:
    if nm in on:
        o=off[nm]; w(f"    {o['player'][:24]:25} {o['pos']:6} pk{o['effpk']:<3} Eq{o['Eq']:>4.1f} iso {o['iso']:.3f}->{on[nm]['iso']:.3f}  num {o['num']}->{on[nm]['num']} ({dnum(nm):+d})")
tl=sorted([(k,dnum(k)) for k in akeys],key=lambda t:-t[1])[:15]
w("  top-15 lifts:")
for k,d in tl:
    o=off[k]; w(f"    {o['player'][:24]:25} {o['pos']:6} pk{o['effpk']:<3} age{o['age']:.0f} Eq{o['Eq']:>4.1f}  {o['num']}->{on[k]['num']} ({d:+d})")
# ---- English/Briggs ratio + watch rows ----
w("\n## English/Briggs priced ratio (R104.3 floor 1.75 is a CHAPTER acceptance; print where Leg A lands)")
for pair in [('timothy-english','kieren-briggs')]:
    a,b=pair
    if a in on and b in on:
        w(f"    OFF: English {off[a]['num']} / Briggs {off[b]['num']} = {off[a]['num']/off[b]['num']:.3f}x")
        w(f"    ON : English {on[a]['num']} / Briggs {on[b]['num']} = {on[a]['num']/on[b]['num']:.3f}x")
w("## WATCH ROWS (R103.5): Gawn ↑ · Bontempelli ↑ · Harley Reid (band)")
for nm in ['max-gawn','marcus-bontempelli','harley-reid']:
    if nm in on:
        d=dnum(nm); w(f"    {off[nm]['player'][:22]:23} {off[nm]['num']}->{on[nm]['num']} ({d:+d})  {'UP' if d>0 else ('flat' if d==0 else 'DOWN')}")
txt='\n'.join(out); open(f'{M}/VALUE_FLOW.md','w').write(txt); print(txt)
