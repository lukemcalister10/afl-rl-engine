# R4 — THE FOUR PHANTOM BOARDS (owner-proposed mechanism; SIMULATE, DO NOT WIRE).
# Insert ONE phantom game-row (games=1) in each missed season, at four averages, re-price the whole
# AFFECTED board via ev(), and report movers/magnitudes + Jamarra + the A-anchors + the young cohort.
#   1. avg = 0
#   2. avg = replacement bar  MA.REPL[pos]
#   3. avg = pre-absence level + effect  (signed effect<0 => level-|penalty|; the DATA-IMPLIED candidate)
#   4. avg = pre-absence level           (the null: absence costs nothing)
# Board of record: store b0c39d78. Deep-copies only; the store is never written.
import harness as H, d2common as D, numpy as np, copy
MA=H.MA; cp=H.cp; ev=H.ev
np.random.seed(0)

# truth curve (R2 mean-reversion-adjusted) for the candidate avg
ev_=D.build_events(); ctrl=D.build_control(); exp=D.make_expected(ctrl)
cl=D.build_control_lvl(); pred=D.fit_ctrl_model(cl)
rows=D.effect_rows(ev_,exp,ctrl_predict=pred)
tage=np.array([r['age_pre'] for r in rows]); tadj=np.array([r['effect_adj'] for r in rows]); BW=2.5
def truth(age):
    if age is None: return -4.94
    w=np.exp(-0.5*((tage-age)/BW)**2); return float(np.sum(w*tadj)/w.sum())

gaps_pop=D.gap_players()
# baseline board values for the affected players
base={gp['player']: ev(gp['p'],2026) for gp in gaps_pop}

def phantom_avg(gp, opt):
    pos=gp['pos']; pre=gp['pre_avg']; age=gp['age_pre']
    if opt==1: return 0.0
    if opt==2: return MA.REPL.get(MA.gfut(gp['p']),0.0)
    if opt==3: return max(0.0, pre+truth(age))    # data-implied (candidate)
    if opt==4: return pre
def make_phantom(gp, av):
    q=copy.deepcopy(gp['p'])
    for y in gp['gaps']:
        q['scoring'].append({'year':y,'games':1,'avg':float(av)})
    q['scoring'].sort(key=lambda x:x['year'])
    return q

OPTS={1:'avg=0',2:'avg=REPL bar',3:'avg=pre+effect (candidate)',4:'avg=pre (null)'}
boards={}
for opt in OPTS:
    b={}
    for gp in gaps_pop:
        av=phantom_avg(gp,opt); q=make_phantom(gp,av)
        b[gp['player']]=ev(q,2026)
    boards[opt]=b

print("=== R4 · FOUR PHANTOM BOARDS · one 1-game row per missed season · board b0c39d78 ===")
print(f"affected population: {len(gaps_pop)} established-base absence players; rest of board (695) UNCHANGED (ev is per-player)\n")
names=[gp['player'] for gp in gaps_pop]
for opt in OPTS:
    d=np.array([boards[opt][nm]-base[nm] for nm in names])
    movers=np.sum(np.abs(d)>=1)
    up=np.sum(d>=1); dn=np.sum(d<=-1)
    tot=d.sum()
    print(f"[{opt}] {OPTS[opt]:28}  movers(|Δ|≥1 SCAR)={movers:3d} (↑{up} ↓{dn})  ΣΔ={tot:+7.0f}  meanΔ={d.mean():+6.1f}  medianΔ={np.median(d):+5.1f}  max|Δ|={np.abs(d).max():.0f}")

# Jamarra across the four
print("\n--- Jamarra Ugle-Hagan (KFWD, gap 2025; pre-absence ~63.8; NOT yet returned) ---")
jam=next(gp for gp in gaps_pop if 'ugle-hagan' in gp['player'].lower())
print(f"    baseline ev = {base[jam['player']]:.0f} SCAR")
for opt in OPTS:
    print(f"    [{opt}] {OPTS[opt]:28} phantom_avg={phantom_avg(jam,opt):5.1f} -> ev={boards[opt][jam['player']]:5.0f}  (Δ{boards[opt][jam['player']]-base[jam['player']]:+.0f})")

# A-anchors: must be inert (no gap) -> confirms the phantom is surgical
print("\n--- A-anchors (no absence -> expected INERT; confirms surgical) ---")
anchor_names=['Marcus Bontempelli','Max Gawn','Nick Daicos','Harry Sheezel','Harley Reid']
for an in anchor_names:
    p=next((x for x in MA.data if x['player']==an),None)
    if p is None: continue
    v0=ev(p,2026)
    # a phantom would only touch p if p had a gap; anchors have none -> value is baseline, unaffected by others
    inpop = an in base
    print(f"    {an:22} ev={v0:5.0f}  in-affected-population={inpop}  (unaffected: phantoms are inserted only into gap-players' own records)")

# G-COHORT proxy: young (age_pre<25) gap-players' aggregate board value under each option
print("\n--- G-COHORT (board-side proxy = young gap-players age_pre<25; the binding walk-forward gate recompute is OUT of Tier-3 scope, declared) ---")
young=[gp['player'] for gp in gaps_pop if gp['age_pre'] is not None and gp['age_pre']<25]
print(f"    young affected n={len(young)}   baseline Σev={sum(base[nm] for nm in young):.0f}")
for opt in OPTS:
    s=sum(boards[opt][nm] for nm in young); b0=sum(base[nm] for nm in young)
    print(f"    [{opt}] {OPTS[opt]:28} Σev={s:7.0f}  (Δ{s-b0:+.0f}, {100*(s-b0)/b0:+.1f}%)")

# GAMES-WEIGHT sensitivity: the candidate avg carried by 1 / 5 / 10 / 18 games. A 1-game phantom
# weighs ld^1 (~0.40 KEY / 0.35 GEN / 0.225 MR) against ~18 for a real season -> the AVERAGE barely
# registers; WEIGHT is the real knob (this is why options 2/3/4 above are a wash, and why the owner's
# own note reached for ~10 phantom games). SIMULATE ONLY.
print("\n--- games-weight sensitivity: candidate avg (pre+effect) carried by g games ---")
def make_phantom_g(gp,av,g):
    q=copy.deepcopy(gp['p'])
    for y in gp['gaps']: q['scoring'].append({'year':y,'games':int(g),'avg':float(av)})
    q['scoring'].sort(key=lambda x:x['year']); return q
for g in (1,5,10,18):
    d=[]
    for gp in gaps_pop:
        av=phantom_avg(gp,3); d.append(ev(make_phantom_g(gp,av,g),2026)-base[gp['player']])
    d=np.array(d)
    jd=ev(make_phantom_g(jam,phantom_avg(jam,3),g),2026)-base[jam['player']]
    print(f"    g={g:2d}  movers(|Δ|≥1)={np.sum(np.abs(d)>=1):3d}  ΣΔ={d.sum():+7.0f}  meanΔ={d.mean():+6.1f}  Jamarra Δ={jd:+.0f}")

# biggest individual movers under the candidate (option 3)
print("\n--- largest |Δ| under [3] candidate (avg=pre+effect, 1 game) ---")
d3=sorted(((boards[3][nm]-base[nm],nm) for nm in names),key=lambda t:-abs(t[0]))[:8]
for dv,nm in d3:
    gp=next(g for g in gaps_pop if g['player']==nm)
    print(f"    {nm:24} {gp['pos']:5} age {gp['age_pre'] if gp['age_pre'] else 0:.0f}  base {base[nm]:5.0f} -> {boards[3][nm]:5.0f}  (Δ{dv:+.0f})")
