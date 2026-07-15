# Generate the committed P1 affected-row list from the 4 ablated boards + the double-charge split.
import json, numpy as np
D=lambda f: json.load(open(f))
base=D('rboard_base.json'); fix1=D('rboard_fix1.json'); absb=D('rboard_abs.json'); both=D('rboard_both.json')
split={r['player']:r for r in D('bor_ws/gap_split.json')}
FADE_N=2.0
keys=[k for k in base if 'error' not in base[k]]
def n(d,k): return d[k]['num']
out=[]
w=out.append
w("# AFFECTED-ROW LIST — Fix 1 + the absence term (Option C) · candidate\n")
w("Numeraire SCAR (round(ev/1.0524)). base = both levers OFF (byte-exact, Jamarra=187).")
w("Legs path-additive, declared order Fix1->Absence: fix1 = base+Fix1; both = base+Fix1+Absence.\n")

# ---- P0 headline ----
def sd(a,b): return sum(n(b,k)-n(a,k) for k in keys)
w("## P0 — attribution (path-additive)")
w(f"- Fix 1 leg  (base->fix1): {sd(base,fix1):+d} num-SCAR")
w(f"- Absence leg(fix1->both): {sd(fix1,both):+d} num-SCAR   (absence alone base->abs: {sd(base,absb):+d})")
w(f"- BOTH total (base->both): {sd(base,both):+d} num-SCAR")
w(f"- path-additivity: L1+L2={sd(base,fix1)+sd(fix1,both):+d} == total {sd(base,both):+d}; max|Σlegs-total|={abs(sd(base,fix1)+sd(fix1,both)-sd(base,both))}\n")

# ---- Jamarra ----
jk='jamarra-ugle-hagan'
w("## JAMARRA UGLE-HAGAN — under (a) Fix1, (b) Absence, (c) Both")
w(f"- base {n(base,jk)} | (a) Fix1 {n(fix1,jk)} | (b) Absence {n(absb,jk)} | (c) Both {n(both,jk)}")
w(f"- levels: base {base[jk]['lvl']:.2f} -> Fix1 {fix1[jk]['lvl']:.2f} -> Both {both[jk]['lvl']:.2f}")
w(f"- scoring {base[jk]['scoring']}; gap 2025, age_pre 22")
sj=split.get('Jamarra Ugle-Hagan')
if sj: w(f"- double-charge split (both): decay {sj['decay_scar']:+d} · new-term {sj['new_scar']:+d} · total {sj['tot_scar']:+d} SCAR vs no-gap; level total {sj['tot_lvl']:+.2f} == mult-truth {sj['truth_mult']:+.2f} (NO overshoot)\n")

# ---- Absence term: every gap player that MOVES (new_scar!=0), + the double-charge split ----
w("## ABSENCE TERM — every gap player the term MOVES (sorted by |total ΔSCAR|)")
w("cols: player · pos · age_pre · missed · fade(N=2) · Lnogap · Lfin · decayΔlvl · newΔlvl · totΔlvl · mult-truth · | decayΔscar · newΔscar · totΔscar")
mv=[r for r in split.values() if r['new_scar']!=0]
def fade2(np_): return float(np.clip(1.0-np_/FADE_N,0.0,1.0))
mv.sort(key=lambda r:-abs(r['new_scar']))
for r in mv:
    fd=fade2(r['npost'])
    w(f"- {r['player']:22} {r['pos']:8} a{r['age_pre']:.0f} miss{r['missed']} fade{fd:.2f} | "
      f"Lng {r['L_nogap']:.1f} Lfin {r['L_fin']:.1f} | dcy {r['decay_lvl']:+.2f} new {r['new_lvl']:+.2f} tot {r['tot_lvl']:+.2f} truthM {r['truth_mult']:+.2f} | "
      f"dcyS {r['decay_scar']:+d} newS {r['new_scar']:+d} totS {r['tot_scar']:+d}")
over=sum(1 for r in split.values() if r['new_lvl']<-0.001 and abs(r['tot_lvl'])>abs(r['truth_mult'])+0.3)
w(f"\nNEW-TERM double-charge OVERSHOOTS: {over} (HALT if >0). Total gap players detected: {len(split)}; term moves {len(mv)}.")
w("Non-moving gap players (267): re-established (fade->0, >=2 post-return seasons) OR curve~0 (age<20 data-free) OR decay already >= curve.\n")

# ---- Fix 1: every mover, M4 flagged ----
w("## FIX 1 — every value mover (|Δ|>=1), sorted by |Δ|. M4 flagged.")
M4={'peter-ladhams':'Ladhams','nathan-o-driscoll':'O`Driscoll(N)','aiden-o-driscoll':'O`Driscoll(A)',
    'deven-robertson':'Robertson','rhett-bazzo':'Bazzo','kane-mcauliffe':'McAuliffe','ned-moyle':'Moyle',
    'sam-day':'Day(S)','will-day':'Day(W)','elijah-tsatas':'Tsatas','josh-lindsay':'Lindsay(J)',
    'xavier-lindsay':'Lindsay(X)','campbell-chesser':'Chesser','jamarra-ugle-hagan':'Jamarra'}
fm=sorted([(k,n(fix1,k)-n(base,k)) for k in keys if abs(n(fix1,k)-n(base,k))>=1], key=lambda t:-abs(t[1]))
w(f"{len(fm)} movers. cols: player · pos · base · fix1 · Δ · lvlB->lvlF")
for k,d in fm:
    tag=' <<M4:'+M4[k] if k in M4 else ''
    w(f"- {base[k]['player']:24}{base[k]['pos']:8} {n(base,k):5d} -> {n(fix1,k):5d}  Δ{d:+5d}  lvl {base[k]['lvl']:.1f}->{fix1[k]['lvl']:.1f}{tag}")
w("\n## M4 list explicit (owner-flagged overpriced)")
for k,nm in sorted(M4.items(), key=lambda x:x[1]):
    if k in base: w(f"- {nm:14} {base[k]['player']:22} base {n(base,k):5d} · Fix1 {n(fix1,k):5d} · Both {n(both,k):5d}  (Δboth {n(both,k)-n(base,k):+d})")
print('\n'.join(out))
