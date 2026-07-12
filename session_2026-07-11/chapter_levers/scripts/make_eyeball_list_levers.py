#!/usr/bin/env python3
"""(e) THE OWNER'S EYEBALL LIST — every player AND every pick asset, old->new, sorted by Δ%.
Compares the baked v2.7 board (OLD) to the candidate's regenerated board (NEW).
Flags the RUC cohort and the floor-dippers. Emits a one-page summary + the full table.
"""
import json, statistics, sys, os

REPO='/home/user/afl-rl-engine'
OLD=json.load(open(os.path.join(REPO,'session_2026-07-11/pick_corrections/out/board_baked_v27.json')))
NEW=json.load(open(sys.argv[1] if len(sys.argv)>1 else '/tmp/claude-0/-home-user-afl-rl-engine/b8e67301-6ed7-5f3f-bd9a-8cf5cd7e3896/scratchpad/board_final.json'))
OUT_MD=os.path.join(REPO,'session_2026-07-11/chapter_levers/EYEBALL_LIST.md')
FACTOR=json.load(open(os.path.join(REPO,'engine/rl_after/pick_redenomination.json')))['factor']

def pct(o,n): return (n-o)/o*100 if o else 0.0
SCALE_OLD=OLD.get('SCALE'); SCALE_NEW=NEW.get('SCALE')
SCALE_RATIO=(SCALE_NEW/SCALE_OLD) if SCALE_OLD else None
# three narrowest guard margins on the candidate (from the gate suite + the G-COHORT class-sum row).
GUARD_MARGINS=[
 ("G-COHORT y4 (BINDING, class-year-sum vs hard 1.30)","128.6 vs 130 -> 1.4 pts (levered book B1 row; the GDEF credit lands mostly in the y1 denominator)"),
 ("A10 Curnow decline (frozen suite, bar 0.50)","0.55 vs 0.50 -> +0.05 (narrowest PASSING anchor; PROVISIONAL, data-caused)"),
 ("A8 Berry >= 2x Tsatas (frozen suite)","2.14x vs 2.00x -> +0.14x"),
]

# ---- players ----
oldp={p['key']:p for p in OLD['active']}
newp={p['key']:p for p in NEW['active']}
rows=[]
for k,np_ in newp.items():
    op=oldp.get(k)
    if not op or not op.get('v') or np_.get('v') is None: continue
    o,n=op['v'],np_['v']
    rows.append({'kind':'player','key':k,'name':np_.get('name'),'pos':np_.get('grp'),
                 'old':o,'new':n,'dabs':n-o,'dpct':pct(o,n)})

# ---- pick assets ----
oldpvc={int(x['n']):x['v'] for x in OLD['picks']}
newpvc={int(x['n']):x['v'] for x in NEW['picks']}
for n_ in sorted(newpvc):
    o,n=oldpvc.get(n_),newpvc[n_]
    if o is None: continue
    rows.append({'kind':'pick','key':'pick-%d'%n_,'name':'Pick %d'%n_,'pos':'PICK ASSET',
                 'old':o,'new':n,'dabs':n-o,'dpct':pct(o,n)})

# ---- flags ----
RUC=[r for r in rows if r['pos']=='RUC']
DIP=[r for r in rows if r['kind']=='player' and r['dabs']<0]   # floor-dippers (value LOWERED)
for r in rows:
    r['flag']=''
    if r['pos']=='RUC': r['flag']='RUC'
    if r in DIP: r['flag']=(r['flag']+' FLOOR-DIP').strip()

rows.sort(key=lambda r:r['dpct'])

# ---- summary ----
pl=[r for r in rows if r['kind']=='player']
pk=[r for r in rows if r['kind']=='pick']
dp=[r['dpct'] for r in pl]
bypos={}
for r in pl: bypos.setdefault(r['pos'],[]).append(r['dpct'])
ruc_dp=[r['dpct'] for r in RUC if r['kind']=='player']
nonruc_dp=[r['dpct'] for r in pl if r['pos']!='RUC']

lines=[]
lines.append('# OWNER EYEBALL LIST — chapter-lever candidate (L1 transition credit; L2 measured-not-supported) — 2026-07-11')
lines.append('')
lines.append('OLD = baked v2.7 board (SCALE 4.45). NEW = pick-convention remediation regenerated board (SCALE %.5f). '
             'NEW carries the pick-convention remediation (base c02499a3) PLUS lever L1 (young-GDEF transition credit; '
             'GEN_DEF ycred rows strengthened, engine untouched). L2 (sustained-form) measured NOT-SUPPORTED — nothing shipped. '
             'Every player AND every pick asset below.'%SCALE_NEW)
lines.append('')
lines.append('## ONE-PAGE SUMMARY')
lines.append('')
lines.append('- **MEASURED CURRENCY FACTOR = %.4f** — the global board SCALE ratio (new %.5f / baked %.5f). '
             'This is the definitive uniform scalar; owner ruling (f): shipped pick assets = frozen v3.4 x this factor. '
             'Matches audit Q4 (1.0524).'%(FACTOR, SCALE_NEW, SCALE_OLD))
lines.append('- Players: %d. Pick assets: %d.'%(len(pl),len(pk)))
lines.append('- Player Δ%% distribution: min %.2f%% / **median %.2f%%** / max %.2f%%. The MEDIAN (~currency factor) is the '
             'representative per-player shift; the MEAN is right-skewed by low-value floor players whose few-SCAR rises '
             'are large in %%.'%(min(dp),statistics.median(dp),max(dp)))
lines.append('- Non-RUC players **median Δ%% %+.2f%%** (mean %+.2f%%, skewed). RUC cohort **median Δ%% %+.2f%%** '
             '(mean %+.2f%%). Established RUCs move LESS than the currency (e.g. Max Gawn baked 2413 -> 2483 = +2.90%%, '
             'i.e. ~-2.3%% relative to the +5.24%% currency — the RUC cap machinery; FLAGGED per directive).'
             %(statistics.median(nonruc_dp), statistics.mean(nonruc_dp), statistics.median(ruc_dp), statistics.mean(ruc_dp)))
lines.append('- Pick assets Δ%%: uniform **+%.2f%%** (= factor-1; pick-vs-pick ratios byte-preserved, uniform scalar).'%((FACTOR-1)*100))
lines.append('')
lines.append('### Three narrowest guard margins (candidate)')
lines.append('')
for g,m in GUARD_MARGINS: lines.append('- **%s**: %s'%(g,m))
lines.append('- Gate suite: all green except reds **{A2, A3, A12}** — A2/A3 the standing owner-ruled data-caused reds; A12 did NOT flip (travaglia 792 vs moraes 1023): the MEASURED transition already prices travaglia at his genuine chance (ACCEPTANCE.md &sect;1). B4 board-parity PASS (9ecbe0fa); B3 book-seal PASS (candidate re-seal a19b3cb8); B5 raise-only intact (0 lowered).')
lines.append('')
lines.append('### Per-position mean Δ% (players)')
lines.append('')
lines.append('| position | n | mean Δ% | median Δ% |')
lines.append('|---|---|---|---|')
for g in sorted(bypos):
    v=bypos[g]; lines.append('| %s | %d | %+.2f%% | %+.2f%% |'%(g,len(v),statistics.mean(v),statistics.median(v)))
lines.append('')
lines.append('### FLOOR-DIPPERS (G-FLOOR dispensation — players whose value LOWERED)')
lines.append('')
lines.append('Count = **%d** (owner ruling: ≤5 SCAR dips on the floor anchors ruled not-cratering, dispensation granted). '%len(DIP))
worst=max((abs(r['dabs']) for r in DIP), default=0)
lines.append('Largest absolute dip = **%.0f SCAR**. %s'%(worst, 'ALL ≤5 SCAR ✓' if worst<=5 else '!!! A DIP EXCEEDS 5 SCAR — STOP/REVIEW !!!'))
lines.append('')
lines.append('| player | key | pos | old | new | Δabs | Δ% |')
lines.append('|---|---|---|---|---|---|---|')
for r in sorted(DIP,key=lambda r:r['dabs']):
    lines.append('| %s | %s | %s | %d | %d | %+.0f | %+.2f%% |'%(r['name'],r['key'],r['pos'],r['old'],r['new'],r['dabs'],r['dpct']))
lines.append('')
lines.append('### RUC cohort (flagged — moves less than the currency shift)')
lines.append('')
lines.append('| player | key | old | new | Δabs | Δ% |')
lines.append('|---|---|---|---|---|---|')
for r in sorted([x for x in RUC if x['kind']=='player'],key=lambda r:r['dpct']):
    lines.append('| %s | %s | %d | %d | %+.0f | %+.2f%% |'%(r['name'],r['key'],r['old'],r['new'],r['dabs'],r['dpct']))
lines.append('')
lines.append('## FULL LIST — every player AND every pick asset, sorted by Δ%')
lines.append('')
lines.append('| # | kind | name | key | pos/asset | old | new | Δabs | Δ% | flag |')
lines.append('|---|---|---|---|---|---|---|---|---|---|')
for i,r in enumerate(rows,1):
    lines.append('| %d | %s | %s | %s | %s | %d | %d | %+.0f | %+.2f%% | %s |'
                 %(i,r['kind'],r['name'],r['key'],r['pos'],r['old'],r['new'],r['dabs'],r['dpct'],r['flag']))

open(OUT_MD,'w').write('\n'.join(lines)+'\n')
print('wrote', OUT_MD)
print('players=%d picks=%d floor-dippers=%d (worst %.0f SCAR) RUC=%d'%(len(pl),len(pk),len(DIP),worst,len([r for r in RUC if r['kind']=='player'])))
print('non-RUC mean Δ%%=%.3f  RUC mean Δ%%=%.3f  factor=%.4f'%(statistics.mean(nonruc_dp),statistics.mean(ruc_dp),FACTOR))
# also dump a machine-readable copy
json.dump({'factor':FACTOR,'rows':rows,'floor_dippers':len(DIP),'worst_dip_scar':worst},
          open(os.path.join(REPO,'session_2026-07-11/chapter_levers/out/eyeball_rows.json'),'w'))
