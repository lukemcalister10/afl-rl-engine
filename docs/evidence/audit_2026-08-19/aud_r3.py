#!/usr/bin/env python3
"""INDEPENDENT AUDIT · B1 — THE R3 RULE AS RULED vs AS WIRED.
The ruled rule (register v752): CURRENT CONSECUTIVE absence walking back from Y; ANY played season
breaks the run; injured-annotated exempt; depth < 2 zero. This file re-derives the run length from
the STORE and tests it against the R3 lever's own board delta (V750_L5C -> V751_CAND). Nothing here
reads the packet. Fixes nothing."""
import json, os, csv, re, hashlib

SP='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad'
ASM=SP+'/asm'
WT=SP+'/audit-wt'
Y=2026
out=[]
def P(s=''):
    print(s); out.append(str(s))

def board(tag):
    p='%s/bb_%s/rl_after/rl_app_data.json'%(ASM,tag)
    return {r['key']:r for r in json.load(open(p))['active']}, hashlib.md5(open(p,'rb').read()).hexdigest()[:8]

PRE,mPRE=board('V750_L5C')       # everything except R3
CAND,mCAND=board('V751_CAND')    # + R3   = THE CANDIDATE
STORE={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}

# the owner's pinned annotation, read here directly
ib=open(WT+'/docs/owner_annotations/SITTER_2026_v1.csv','rb').read()
P('='*104)
P('INDEPENDENT AUDIT · B1 — THE R3 PRODUCTION FADE AS RULED vs AS WIRED')
P('='*104)
P('  board before R3 : %s   after R3 : %s'%(mPRE,mCAND))
P('  SITTER_2026_v1.csv md5 read here: %s'%hashlib.md5(ib).hexdigest())
rows=list(csv.DictReader(ib.decode('utf-8').splitlines()))
inj=[r for r in rows if (r.get('injured') or '').strip().upper()=='Y']
P('  annotation rows: %d   injured=Y: %d'%(len(rows),len(inj)))
def norm(n): return re.sub(r'[^a-z0-9]+','-',str(n).strip().lower().replace('’',"'")).strip('-')
INJ=set(norm(r['player']) for r in inj)
P()

def played_years(k):
    r=STORE.get(k) or {}
    return set(int(x['year']) for x in (r.get('scoring') or []) if x.get('games') and float(x['games'] or 0)>0)

def run_len(k):
    """CONSECUTIVE unplayed seasons walking back from Y. 0 if he played in Y."""
    pl=played_years(k)
    if Y in pl: return 0
    r=STORE.get(k) or {}
    floor=int(r['year']) if r.get('year') else None
    n=0; yy=Y-1
    while floor is None or yy>floor:
        if yy in pl: break
        n+=1; yy-=1
        if floor is None and Y-yy>40: break
    return n

# the R3 take, MEASURED: the board difference the lever made
TAKE={k:(PRE[k]['v']-CAND[k]['v']) for k in CAND if k in PRE}
charged={k:v for k,v in TAKE.items() if v!=0}
P('  rows the R3 lever moved: %d   (all downward: %s)'%(len(charged),all(v>0 for v in charged.values())))
P()

P('-'*104)
P('B1 TEST 1 — NO ROW THAT PLAYED IN %d MAY BE CHARGED (the v752 ruling; the Edwards defect)'%Y)
P('-'*104)
viol=[k for k in charged if Y in played_years(k)]
P('  rows charged that PLAYED in %d : %d      %s'%(Y,len(viol),'PASS' if not viol else '*** FAIL ***'))
if viol: P('    '+', '.join(viol[:20]))
P()

P('-'*104)
P('B1 TEST 2 — EVERY CHARGED ROW MUST HAVE A CURRENT CONSECUTIVE RUN GIVING DEPTH >= 2')
P('-'*104)
bad=[]
for k in charged:
    # depth = 1 + run (+ the in-progress fraction, which only ADDS); run>=1 is necessary for depth>=2
    if run_len(k)<1: bad.append(k)
P('  charged rows with NO consecutive absent season: %d   %s'%(len(bad),'PASS' if not bad else '*** FAIL ***'))
if bad: P('    '+', '.join(bad[:20]))
P()

P('-'*104)
P('B1 TEST 3 — NO INJURED-ANNOTATED ROW MAY BE CHARGED (the two-channel law)')
P('-'*104)
iv=[k for k in charged if k in INJ]
P('  injured-annotated rows charged: %d   %s'%(len(iv),'PASS' if not iv else '*** FAIL ***'))
if iv: P('    '+', '.join(iv[:20]))
P()

P('-'*104)
P('B1 TEST 4 — NAMED ROWS FROM THE STORE (no targets; these are the rows the ruling names as exhibits)')
P('-'*104)
P('  %-22s %-8s %-26s %5s %5s %8s'%('key','run','2026 scoring line','pre','cand','R3 take'))
def show(k):
    r=STORE.get(k)
    sc=[x for x in (r.get('scoring') or []) if int(x['year'])==Y]
    s=('%d games @ %.1f'%(sc[0]['games'],sc[0]['avg'])) if sc else 'NO 2026 SEASON'
    P('  %-22s %-8s %-26s %5s %5s %8s'%(k,run_len(k),s,PRE.get(k,{}).get('v'),CAND.get(k,{}).get('v'),
                                        '%+d'%(-TAKE.get(k,0)) if k in TAKE else '-'))
for k in ('mitchell-edwards','toby-conway','harry-barnett','will-brodie','sam-madden',
          'tom-nankervis','jedd-busslinger','oscar-mraz'):
    if k in STORE: show(k)
    else: P('  %-22s NOT IN STORE'%k)
P()

P('-'*104)
P('B1 TEST 5 — CONTINUOUS PLAYERS (played every season since draft) MUST BE UNCHARGED')
P('-'*104)
cont=[]
for k,r in STORE.items():
    if k not in CAND: continue
    yr=r.get('year')
    if not yr: continue
    pl=played_years(k)
    if not pl: continue
    span=set(range(int(yr)+1,Y+1))
    if span and span<=pl: cont.append(k)
cv=[k for k in cont if TAKE.get(k,0)!=0]
P('  continuous-since-draft rows: %d   of which charged: %d   %s'%(len(cont),len(cv),'PASS' if not cv else '*** FAIL ***'))
if cv: P('    '+', '.join(cv[:20]))
P()

P('-'*104)
P('B1 TEST 6 — THE SHIELD, MEASURED INDEPENDENTLY (the open defect v753 reports)')
P('-'*104)
sh=[]
for k in CAND:
    if k not in STORE: continue
    r=STORE[k]
    sc=[x for x in (r.get('scoring') or []) if int(x['year'])==Y and x.get('games')]
    if sc and 0<float(sc[0]['games'])<=2:
        sh.append((k,float(sc[0]['games']),CAND[k]['v']))
sh.sort(key=lambda x:-x[2])
P('  rows whose %d season is 1-2 games (run broken, R3 take forced to 0): %d'%(Y,len(sh)))
for k,g,v in sh[:10]:
    P('    %-24s %.0f game(s)   candidate price %5d'%(k,g,v))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/auditpkg/AUD_R3_out.txt','w').write('\n'.join(out))
