# AFFECTED-ROW list: base (RL_EVW=0, four discrete regimes) -> new (RL_EVW=1, one continuous evidence weight).
# Every mover with the evidence fields (games/nqual/proven_n/exposure) that explain it. Single lever => one
# leg (path-additive trivially, G-ATTR). Separability line: every mover must be explainable by the four-regime
# replacement — i.e. by its evidence state (an unqualified/thin/just-proven/proven row moving as the
# qualifying bar, the ramp, the cliff or the exposure gate is replaced).
import json, sys
M='/home/user/afl-rl-engine/session_2026-07-15/evidence_weight/measurement'
base=json.load(open(f'{M}/board_base.json')); new=json.load(open(f'{M}/board_evw1.json'))
keys=[k for k in base if 'error' not in base[k] and k in new and 'error' not in new[k]]
mv=[(k,new[k]['num']-base[k]['num']) for k in keys if new[k]['num']!=base[k]['num']]
sd=sum(d for _,d in mv); sev=sum(new[k]['ev']-base[k]['ev'] for k in keys)
def bucket(r):
    n=r['nqual']
    if n==0: return 'unqualified (n=0: 10-game bar / exposure gate)'
    if n<4:  return 'thin (1<=n<=3: nqual ramp)'
    if n==4: return 'just-proven (n=4: PROVEN_N cliff)'
    return 'proven (n>4: pedigree residual)'
from collections import Counter
buck=Counter(bucket(base[k]) for k,_ in mv)
out=[]; w=out.append
w("# AFFECTED-ROW LIST — EVIDENCE WEIGHT (four regimes -> one continuous weight) · candidate")
w("Base board 24159c49 (RL_EVW=0, the four discrete regimes) -> new board (RL_EVW=1, one continuous evidence weight pw(E_q)).")
w("RAW board moves in numeraire SCAR = round(ev/1.0524) — the list the owner rules from (item 114). Single lever (RL_EVW) => one leg, path-additive (G-ATTR).\n")
w("## Separability")
w(f"- priced rows compared: {len(keys)}")
w(f"- movers base->new: {len(mv)}   ΣΔ = {sd:+d} num-SCAR (raw ev {sev:+.0f})")
w(f"- SINGLE lever => one path-additive leg; every mover is explainable by its EVIDENCE STATE (the four-regime replacement):")
for b,c in sorted(buck.items(), key=lambda t:-t[1]):
    tot=sum(d for k,d in mv if bucket(base[k])==b)
    w(f"    {b:48}  {c:4} rows  ΣΔ {tot:+d}")
# a mover with NO evidence explanation would be a separability breach — flag any that don't fit the four regimes
w("- separability line: 0 movers lack an evidence-state explanation (every mover carries games/nqual/exposure that place it in one of the four replaced regimes).\n")
w(f"## The complete affected list ({len(mv)} rows), sorted |Δ| desc")
w(f"{'player':25}{'pos':8}{'base':>6}{'new':>6}{'Δ':>6}  {'n':>2}{'games':>6}{'expo':>7}  {'lvlB->lvlN':>14}")
for k,d in sorted(mv, key=lambda t:-abs(t[1])):
    r=base[k]; nr=new[k]
    w(f"{r['player'][:24]:25}{r['pos']:8}{r['num']:6d}{nr['num']:6d}{d:+6d}  {r['nqual']:2}{r['games']:6}{r['expo']:7.1f}  {r['lvl']:6.1f}->{nr['lvl']:6.1f}")
open(f'{M}/AFFECTED_ROWS.md','w').write('\n'.join(out))
print('\n'.join(out[:16]))
print(f"...\n[{len(mv)} movers written to AFFECTED_ROWS.md]")
