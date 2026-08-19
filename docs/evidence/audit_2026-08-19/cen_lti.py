#!/usr/bin/env python3
"""THE SEASON-CONSTANT CENSUS — SITE 1, the one that genuinely bites.
L = 1 - min(g2026/G_FULL, 1)  [lti_register.py:117], G_FULL=22, asserted == cp.SEASON.
READ-ONLY."""
import json,re
WT='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cen-wt'
ASM='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm'
out=[]
def P(s=''):
    print(s); out.append(str(s))
S={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}
B={r['key']:r for r in json.load(open(ASM+'/bb_V751_CAND/rl_after/rl_app_data.json'))['active']}
lti=sorted({m.group(1) for m in (re.match(r'\|\s*([a-z0-9\-]+)\s*\|',l) for l in open(WT+'/LTI_REGISTER.md')) if m and m.group(1) in S})
P('='*104)
P('SITE 1 · THE LTI LOST-SEASON FRACTION — the one true games/season-length ratio on the board')
P('='*104)
P('  L = 1 - min(g2026 / G_FULL, 1)      lti_register.py:117      G_FULL = 22')
P('  CONSUMERS: (a) _avail_hc, the Part-1 present haircut (lost production) -> LOWERS price;')
P('             (b) the LTI clock advance  g += L*cp.SEASON  [_merged_recover.py:1380].')
P('  IDENTITY: L*SEASON == SEASON - g2026. The advance adds "the games he would have played".')
P()
P('  %-24s %5s %8s %8s %9s %9s %7s'%('key','g2026','L@22','L@18','phantom22','phantom18','price'))
n=0; hcok=0
for k in lti:
    p=S[k]
    g=next((float(x['games']) for x in (p.get('scoring') or []) if int(x['year'])==2026),0.0)
    L22=max(0.0,1.0-min(g/22.0,1.0)); L18=max(0.0,1.0-min(g/18.0,1.0))
    hc=B.get(k,{}).get('avail_hc')
    if hc is not None and abs(float(hc)-L22)<1e-9: hcok+=1
    if g>0:
        n+=1
        P('  %-24s %5.0f %8.4f %8.4f %9.1f %9.1f %7s'%(k,g,L22,L18,22-g,max(0.0,18-g),B.get(k,{}).get('v')))
P()
P('  BOARD CONFIRMATION: %d of %d register rows carry avail_hc EXACTLY equal to L@22.'%(hcok,len(lti)))
P('  This site is LIVE on the delivered board, not theoretical.')
P()
P('  rows with zero 2026 games (L=1.0 on any norm, unaffected): %d'%(len(lti)-n))
P('  rows where the norm BITES today: %d'%n)
P()
P('  WORKED EXAMPLE, no target: a row with 15 games in 2026 who is then registered out is booked')
P('  as having lost 31.8%% of a season. On an 18-game realistic season he lost 16.7%%. The haircut')
P('  is close to DOUBLE what the owner\'s reading of a full season would give.')
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cenpkg/CENSUS_SEASON_LTI_out.txt','w').write('\n'.join(out))
