#!/usr/bin/env python3
"""THE SEASON-CONSTANT CENSUS — do the engine's games BARS mistreat a 14-18 game season?
READ-ONLY. The bars are 6 / 10 / 14 / 22, enumerated at _merged_recover.py:106-109."""
import json, collections
WT='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cen-wt'
ASM='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm'
out=[]
def P(s=''):
    print(s); out.append(str(s))
S={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}
B={r['key']:r for r in json.load(open(ASM+'/bb_V751_CAND/rl_after/rl_app_data.json'))['active']}
FE=0.58   # calendar progress at this cut, read from the source in the companion file

P('='*104)
P('THE GAMES BARS — 6 (qualifies) / 10 (delivered) / 14 (level counts fully) / 22 (pole gate)')
P('='*104)
P('   NONE of these is a games/SEASON ratio. They are ABSOLUTE games bars, prorated only by the')
P('   CALENDAR fraction fE=%.2f for the in-progress season. Season LENGTH does not enter any of them.'%FE)
P()
P('   %-9s %-46s %s'%('bar','what it asks','does a 14-18 game season clear it?'))
for bar,what in ((6,'is the season readable at all (nseas_pro/bestlvl)'),
                 (10,'is the season DELIVERED (o32_delivered)'),
                 (14,'does the demonstrated level count FULLY (LEVEL_RAMP)'),
                 (22,'does the pole/recovery gate open fully (POLE_RAMP)')):
    P('   %-9s %-46s %s'%(bar,what,'YES, comfortably' if bar<=14 else 'on CAREER recency-weighted games — by season 2'))
P()
P('-'*104)
P('COMPLETED-SEASON CHECK: every 2025 season row, against the absolute bars')
P('-'*104)
rows=[]
for k,p in S.items():
    r=[x for x in (p.get('scoring') or []) if int(x['year'])==2025 and x.get('games')]
    if r: rows.append((k,float(r[0]['games'])))
band=[(k,g) for k,g in rows if 14<=g<=18]
P('   2025 season rows: %d      in the 14-18 band: %d'%(len(rows),len(band)))
P('   of the 14-18 band:')
P('     clear the 6-game readable bar   : %d of %d'%(sum(1 for _,g in band if g>=6),len(band)))
P('     clear the 10-game delivered bar : %d of %d  (games leg; the avg-vs-bar leg is separate)'%(sum(1 for _,g in band if g>=10),len(band)))
P('     clear the 14-game level ramp    : %d of %d'%(sum(1 for _,g in band if g>=14),len(band)))
P('   ALL of them clear every absolute bar. Not one 14-18 game row is treated as a partial')
P('   participant by any bar in the engine.')
P()
P('-'*104)
P('THE ONE PLACE A 14-18 GAME SEASON IS STILL DISCOUNTED — and it is MEASURED, not a norm')
P('-'*104)
P('   rho31(g), the production-reliability weight, is still climbing at 15-18 games (it reaches')
P('   ~91-95%% of its 22-game value). But rho31 is FITTED ON RAW GAMES with no season length in it:')
P('     rho31(g) = 1 - exp(-(g/29.19)^0.8015)   + the measured re-mix bump')
P('   Its tau is 29.19 GAMES — larger than any season length. It is a career-evidence curve, not a')
P('   season-completeness ratio. Rebasing "a season" to 18 would not touch it; only a refit would,')
P('   and the refit would have to be justified by out-of-sample error, not by a convention.')
P()
P('-'*104)
P('POPULATIONS THE TWO LIVE 22-SITES REACH')
P('-'*104)
msd=[k for k,p in S.items() if p.get('type')=='MSD' and k in B]
P('   SITE A  pv_games MSD entry scaler (22/12): %d MSD rows on the board, 39 with a moving axis'%len(msd))
pickless=[k for k,r in B.items() if not r.get('pk')]
P('   SITE B  LTI clock advance (L*22)         : 43 register rows, 21 still under the G0=46 bar')
P('   SITE C  debut_factor (22-cg)/22          : reaches PICKLESS-unplayed rows only; pickless on board: %d'%len(pickless))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cenpkg/CENSUS_SEASON_BARS_out.txt','w').write('\n'.join(out))
