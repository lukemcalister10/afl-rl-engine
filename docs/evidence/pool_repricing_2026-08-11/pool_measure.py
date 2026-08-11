"""POOL REPRICING — the measurements behind the directive. READ-ONLY, no emits, no wiring.

Re-derivable by the seat: every number in DRAFT_POOL_REPRICING_DIRECTIVE_2026-08-11.md comes from here
or from the cited prior evidence file. Sources:
  - the SHIPPED matrix per_entrant_SHIP.json (the landed composition = the live baseline)
  - the main matrix per_entrant_main.json (the pre-act engine)
  - the ITEM B natural experiment: board at origin/main vs board at aa1693b (ITEM B alone)
"""
import json, statistics, math
SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
O3=SP+'/o3'
def cohort(r):
    y=r.get('year'); return None if y is None else (y if r.get('type')=='MSD' else y+1)
def stream(r):
    t=r.get('type')
    if t=='ND' and r.get('pick') and 1<=r['pick']<=64 and not r.get('is_pool'): return 'ND 1-64'
    if t=='ND': return 'ND>64'
    return t
def val(r,N,W):
    if N==0: return float(r['v0']),'v0'
    Y=cohort(r)+N-1; yrs=r.get('yrs') or []; vp=r.get('vpath') or []
    if not yrs: return 0.0,'ended'
    if Y<yrs[0]: return None,'pre'
    if Y>yrs[-1]: return 0.0,'ended'
    i=yrs.index(Y); return (0.0,'null') if vp[i] is None else (float(vp[i]),'path')

for base in ('SHIP','main'):
    R=json.load(open(f"{SP}/per_entrant_{base}.json"))['recs']
    W=max(y for r in R for y,v in zip(r.get('yrs') or [],r.get('vpath') or []) if v is not None)
    elig=[r for r in R if cohort(r) is not None and (r.get('v0') or 0)>0]
    print("="*104); print(f"### PER-STREAM OUTCOME CURVES — base {base} (window end {W})"); print("="*104)
    print(f"  {'stream':9} {'n':>5} " + "".join(f"{'yr%d'%N:>9}" for N in range(7)) + f" {'Sig v0':>12}")
    order=['ND 1-64','RD','SSP','MSD','IRE','PDA','PDN','PDS','UNR','ND>64']
    for s in order:
        sub=[r for r in elig if stream(r)==s]
        if not sub: continue
        cells=[]
        for N in range(7):
            reach=sub if N==0 else [r for r in sub if cohort(r)+N-1<=W]
            vv,zz=[],[]
            for r in reach:
                v,k=val(r,N,W)
                if k=='pre': continue
                vv.append(v); zz.append(float(r['v0']))
            cells.append(sum(vv)/sum(zz) if zz and sum(zz) else float('nan'))
        s0=sum(float(r['v0']) for r in sub)
        print(f"  {s:9} {len(sub):5} " + "".join(f"{c:9.4f}" for c in cells) + f" {round(s0):12,}")
    print()

# ---- the ITEM B natural experiment: measured pass-through from ENTRY ANCHOR to PRICE ----
L=lambda f: {r['key']:r for r in json.load(open(f))['active']}
MAIN=L(O3+'/wf_main.json'); AFTB=L(O3+'/wf_mraz.json')
MX={r['key']:r for r in json.load(open(f"{SP}/per_entrant_main.json"))['recs']}
K=0.726863
def bshape(a):
    if a is None: return 1.0
    return 0.6858757327896249 if a<=18 else (1.411187553120842 if a<=20 else 2.817253502223132)
print("="*104)
print("### THE PASS-THROUGH FROM ENTRY ANCHOR TO PRICE — measured on the ITEM B natural experiment")
print("="*104)
print("  ITEM B multiplied every pool entry anchor by k*shape(draft age), k=0.726863, and changed")
print("  NOTHING else (verified: the next commit altered only asserts). So for each pool board row the")
print("  ANCHOR ratio is known exactly and the PRICE ratio is measured. e = log(price)/log(anchor).")
print(f"  {'career games':>14} {'n':>5} {'median anchor x':>16} {'median price x':>15} {'PASS-THROUGH e':>15}")
rows=[]
for k,r in AFTB.items():
    if k not in MAIN or k not in MX: continue
    m=MX[k]
    if not m.get('is_pool'): continue
    a=m.get('age_draft'); fa=K*bshape(a)
    if abs(fa-1.0)<1e-6: continue
    p0,p1=MAIN[k]['v'],r['v']
    if p0<=0 or p1<=0: continue
    g=r.get('g') or 0
    rows.append((g, fa, p1/p0, math.log(p1/p0)/math.log(fa)))
for lab,lo,hi in [('0',0,0),('1-9',1,9),('10-29',10,29),('30-99',30,99),('100+',100,10**6)]:
    sub=[x for x in rows if lo<=x[0]<=hi]
    if not sub: continue
    print(f"  {lab:>14} {len(sub):5} {statistics.median(x[1] for x in sub):16.4f} "
          f"{statistics.median(x[2] for x in sub):15.4f} {statistics.median(x[3] for x in sub):15.3f}")
allr=rows
print(f"  {'ALL':>14} {len(allr):5} {statistics.median(x[1] for x in allr):16.4f} "
      f"{statistics.median(x[2] for x in allr):15.4f} {statistics.median(x[3] for x in allr):15.3f}")
print("  e ~ 1 means the price IS the anchor (no evidence to lead it); e ~ 0 means production leads and")
print("  the anchor is already faded out of the price. This is the curve a level change travels down.")

# ---- CANDIDATE LEVEL OPTIONS: what a level change does, using the MEASURED pass-through ----
print()
print("="*104)
print("### CANDIDATE ENTRY-LEVEL OPTIONS — consequences computed with the measured pass-through")
print("="*104)
R=json.load(open(f"{SP}/per_entrant_SHIP.json"))['recs']
W=max(y for r in R for y,v in zip(r.get('yrs') or [],r.get('vpath') or []) if v is not None)
elig=[r for r in R if cohort(r) is not None and (r.get('v0') or 0)>0]
POOLS=['RD','SSP','MSD','IRE','PDA','PDN','PDS','UNR','ND>64']
def e_of(r):
    g=sum(s.get('games',0) for s in (r.get('seasons') or []))
    return 1.0 if g==0 else (0.12 if g<=9 else 0.0)
def ratio(sub,N,lam=1.0):
    reach=sub if N==0 else [r for r in sub if cohort(r)+N-1<=W]
    num=den=0.0
    for r in reach:
        v,k=val(r,N,W)
        if k=='pre': continue
        num+=v*(lam**e_of(r) if N>0 else lam); den+=float(r['v0'])*lam
    return num/den if den else float('nan')
pool=[r for r in elig if stream(r) in POOLS]
print(f"  pooled POOL yr4 delivery on SHIP = {ratio(pool,4):.4f}   (n={len(pool)})")
print(f"  ND 1-64 yr4 = {ratio([r for r in elig if stream(r)=='ND 1-64'],4):.4f}")
print()
print("  OPTION A: no change (lambda = 1.00 everywhere)")
print("  OPTION B: ONE pool-wide lambda = the pooled pool yr4 delivery")
print("  OPTION C: PER-STREAM lambda = that stream's own yr4 delivery")
lamB=ratio(pool,4)
print(f"\n  {'stream':9} {'n':>5} {'yr4 now':>9} {'lam_B':>7} {'yr4 @B':>8} {'lam_C':>7} {'yr4 @C':>8} {'Sig v0 now':>12} {'Sig v0 @C':>11}")
tot0=totC=0.0
for s in POOLS:
    sub=[r for r in elig if stream(r)==s]
    r4=ratio(sub,4); lamC=r4 if r4==r4 and r4>0 else 1.0
    s0=sum(float(r['v0']) for r in sub); tot0+=s0; totC+=s0*lamC
    print(f"  {s:9} {len(sub):5} {r4:9.4f} {lamB:7.3f} {ratio(sub,4,lamB):8.4f} {lamC:7.3f} {ratio(sub,4,lamC):8.4f} {round(s0):12,} {round(s0*lamC):11,}")
print(f"  {'ALL POOL':9} {len(pool):5} {ratio(pool,4):9.4f} {lamB:7.3f} {ratio(pool,4,lamB):8.4f} {'per-arm':>7} {'':>8} {round(tot0):12,} {round(totC):11,}")
print()
print("### THE NAMED LINES under each option — board points (pass-through applied per row)")
BD={r['key']:r for r in json.load(open(O3+'/ship_board.json'))['active']}
MXS={r['key']:r for r in R}
NAMED=['john-noble','max-hall','james-peatling','mark-keane','marcus-herbert','zac-banch','flynn-perez',
       'paddy-cross','mitch-podhajski','harrison-coe','lachlan-mcandrew','tom-mccarthy']
print(f"  {'player':18} {'stream':7} {'career g':>9} {'e':>5} {'SHIP':>7} {'@B':>7} {'@C':>7}")
for k in NAMED:
    if k not in BD or k not in MXS: continue
    m=MXS[k]; s=stream(m); e=e_of(m); g=sum(x.get('games',0) for x in (m.get('seasons') or []))
    sub=[r for r in elig if stream(r)==s]; r4=ratio(sub,4); lamC=r4 if r4==r4 and r4>0 else 1.0
    print(f"  {BD[k]['name'][:18]:18} {s:7} {g:9} {e:5.2f} {BD[k]['v']:7} {round(BD[k]['v']*lamB**e):7} {round(BD[k]['v']*lamC**e):7}")
print()
print("### BOARD TOTAL and the ALL-ARM no-arb effect")
tb=sum(r['v'] for r in BD.values())
for lab,lam in (('B (one lambda)',lamB),):
    d=sum(BD[k]['v']*(lam**e_of(MXS[k])-1) for k in BD if k in MXS and stream(MXS[k]) in POOLS)
    print(f"  board total {tb:,} -> {round(tb+d):,} under option {lab}  ({100*d/tb:+.2f}%)")
allsub=[r for r in elig if 2005<=cohort(r)<=2023]
def allarm(lam):
    num=den=0.0
    for r in allsub:
        if cohort(r)+0<=W:
            v,k=val(r,1,W)
            if k=='pre': continue
            L=lam if stream(r) in POOLS else 1.0
            num+=v*(L**e_of(r)); den+=float(r['v0'])*L
    return num/den
print(f"  ALL-ARM yr1 ratio (cohorts 2005-2023): now {allarm(1.0):.4f} -> {allarm(lamB):.4f} under option B")
print("  (pool year-0 anchors falling RAISES the all-arm ratio: the denominator falls by lambda while a")
print("   produced player's price does not move at all, because his pass-through e is 0.)")

print()
print("="*104)
print("### HOW MANY LIVE BOARD ROWS A LEVEL CHANGE CAN REACH AT ALL")
print("="*104)
reach=[k for k in BD if k in MXS and stream(MXS[k]) in POOLS and e_of(MXS[k])>0]
val_reach=sum(BD[k]['v'] for k in reach)
print(f"  pool rows on the live board            : {sum(1 for k in BD if k in MXS and stream(MXS[k]) in POOLS)}")
print(f"  of those, rows a level change reaches  : {len(reach)}   (pass-through e > 0, i.e. under 10 career games)")
print(f"  their combined board value             : {val_reach:,} of {tb:,}  ({100*val_reach/tb:.2f}% of the board)")
print("  EVERY other pool player is production-priced and a level change cannot move him at all.")

print()
print("="*104)
print("### PLAY QUALITY vs PARTICIPATION, PER STREAM (the play-quality principle's own measure)")
print("="*104)
print("  quality  = career GAMES-WEIGHTED scoring average (how they play)")
print("  particip = career games total (whether/how much they play)")
print(f"  {'stream':9} {'n':>5} {'quality':>9} {'particip':>9} {'zero-game':>10} {'q by draft age <=18 / 19-20 / 21+':>34}")
for s in ['ND 1-64','RD','SSP','MSD','IRE','PDA','PDN','PDS','UNR','ND>64']:
    sub=[r for r in elig if stream(r)==s]
    if not sub: continue
    Q=[];G=[]
    for r in sub:
        ss=[x for x in (r.get('seasons') or []) if x.get('games',0)>0]
        gt=sum(x['games'] for x in ss); G.append(gt)
        if gt>0: Q.append(sum(x['games']*x['avg'] for x in ss)/gt)
    qb=[]
    for lo,hi in ((0,18),(19,20),(21,99)):
        g2=[r for r in sub if r.get('age_draft') is not None and lo<=r['age_draft']<=hi]
        qq=[]
        for r in g2:
            ss=[x for x in (r.get('seasons') or []) if x.get('games',0)>0]
            gt=sum(x['games'] for x in ss)
            if gt>0: qq.append(sum(x['games']*x['avg'] for x in ss)/gt)
        qb.append(statistics.mean(qq) if qq else float('nan'))
    print(f"  {s:9} {len(sub):5} {statistics.mean(Q) if Q else 0:9.2f} {statistics.mean(G):9.1f} "
          f"{sum(1 for x in G if x==0):10} {qb[0]:11.2f} {qb[1]:9.2f} {qb[2]:9.2f}")

print()
print("="*104)
print("### POSITIONAL LENSES — DO THE SAMPLES PERMIT? (owner amendment, 2026-08-11)")
print("="*104)
print("  Owner: 'it would be good to have positional lenses where possible for pool players, but samples")
print("  may make it hard.' This is the count, so the directive states what is possible rather than guesses.")
POSN=['MID','SD','SF','KPD','KPF','RUCK']
print(f"  {'stream':9} {'n':>5} " + "".join(f"{p:>7}" for p in POSN) + f" {'cells n>=20':>12}")
for s in ['ND 1-64','RD','SSP','MSD','IRE','PDA','PDN','PDS','UNR','ND>64']:
    sub=[r for r in elig if stream(r)==s]
    if not sub: continue
    cnt={p:sum(1 for r in sub if r.get('pos')==p) for p in POSN}
    ok=sum(1 for p in POSN if cnt[p]>=20)
    print(f"  {s:9} {len(sub):5} " + "".join(f"{cnt[p]:7}" for p in POSN) + f" {ok:12}")
print()
print("  yr4 delivery BY POSITION where the cell has n>=20 (blank = too thin, disclosed not forced):")
print(f"  {'stream':9} " + "".join(f"{p:>9}" for p in POSN))
for s in ['ND 1-64','RD','SSP','MSD','IRE','PDA','PDN','PDS','UNR','ND>64']:
    sub=[r for r in elig if stream(r)==s]
    if not sub: continue
    cells=[]
    for p in POSN:
        g=[r for r in sub if r.get('pos')==p]
        if len(g)<20: cells.append(f"{'  -':>9}"); continue
        cells.append(f"{ratio(g,4):9.4f}")
    print(f"  {s:9} " + "".join(cells))
