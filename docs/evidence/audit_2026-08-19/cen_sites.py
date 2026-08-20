#!/usr/bin/env python3
"""THE SEASON-CONSTANT CENSUS — the two sites where cp.SEASON is genuinely LIVE, sized.
READ-ONLY. No engine run, no board written."""
import json, math, re, collections
WT='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cen-wt'
src=open(WT+'/engine/rl_after/_merged_recover.py').read()
out=[]
def P(s=''):
    print(s); out.append(str(s))

TAU=float(re.search(r'SIGMA30BP_TAU=([0-9.]+)',src).group(1))
BET=float(re.search(r'SIGMA30BP_BETA=([0-9.]+)',src).group(1))
TAU_RHO=float(re.search(r'O31_TAU_RHO=([0-9.]+)',src).group(1))
B_RHO=float(re.search(r'O31_B_RHO=([0-9.]+)',src).group(1))
KAPPA=float(re.search(r'O32_KAPPA=([0-9.]+)',src).group(1))
GAMMA=float(re.search(r'O32_GAMMA=([0-9.]+)',src).group(1))
def sigma(g): return 1.0 if g<=0 else math.exp(-((g/TAU)**BET))
def rho(g):
    r=0.0 if g<=0 else 1.0-math.exp(-((g/TAU_RHO)**B_RHO))
    if r>0: r=r+KAPPA*((g/GAMMA)*math.exp(1.0-g/GAMMA))*(1.0-r)
    return r

S={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}
ASM='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/asm'
B={r['key']:r for r in json.load(open(ASM+'/bb_V751_CAND/rl_after/rl_app_data.json'))['active']}

P('='*104)
P('THE SEASON-CONSTANT CENSUS — SIZING THE TWO GENUINELY LIVE SITES')
P('='*104)
P()
P('-'*104)
P('SITE A · pv_games MSD ENTRY-SEASON SCALER   _merged_recover.py:3359    _k = cp.SEASON/12')
P('-'*104)
P('   What it computes: the GAMES AXIS that sigma30bp (pedigree share) and rho31 (production')
P('   reliability) both read. Ruling 5 makes an MSD entry season "at most 12 games" and scales it')
P('   to a full-season equivalent. k = 22/12 = %.4f today; k = 18/12 = 1.5000 on an 18-rebase.'%(22/12))
P()
def pv_games(p,Y,k):
    msd=(p.get('type')=='MSD'); e=int(p.get('year') or 0); g=0.0
    for x in (p.get('scoring') or []):
        if x['year']>Y or not x['games']: continue
        g+=float(x['games'])*(k if (msd and x['year']==e) else 1.0)
    return g
msd=[k for k,p in S.items() if p.get('type')=='MSD' and k in B]
P('   MSD rows ON THE BOARD: %d of %d'%(len(msd),len(B)))
moved=[]
for k in msd:
    p=S[k]
    g22=pv_games(p,2026,22/12.0); g18=pv_games(p,2026,18/12.0)
    if abs(g22-g18)>1e-9:
        moved.append((k,g22,g18,sigma(g22),sigma(g18),rho(g22),rho(g18),B[k]['v']))
P('   MSD rows whose games axis would MOVE on an 18-rebase: %d'%len(moved))
P()
moved.sort(key=lambda r:-(r[7]))
P('   %-24s %7s %7s   %8s %8s   %8s %8s %7s'%('key','g@22','g@18','sig@22','sig@18','rho@22','rho@18','price'))
for k,a,b,sa,sb,ra,rb,v in moved[:14]:
    P('   %-24s %7.2f %7.2f   %8.4f %8.4f   %8.4f %8.4f %7d'%(k,a,b,sa,sb,ra,rb,v))
if moved:
    dsig=sum(sb-sa for _,_,_,sa,sb,_,_,_ in moved)/len(moved)
    drho=sum(rb-ra for _,_,_,_,_,ra,rb,_ in moved)/len(moved)
    P()
    P('   MEAN EFFECT of an 18-rebase on the %d moved MSD rows:'%len(moved))
    P('     pedigree share sigma  %+.4f  (18 gives FEWER effective games -> MORE pedigree weight)'%dsig)
    P('     production rho        %+.4f  (FEWER effective games -> LESS production weight)'%drho)
    P('   DIRECTION: an 18-rebase moves MSD rows TOWARD their draft pedigree and away from what')
    P('   they have shown. That is the OPPOSITE of the owner\'s intent (he wants a short season to')
    P('   count as MORE complete, not less). The scaler grosses UP, so a smaller season length')
    P('   grosses up LESS.')
P()

P('-'*104)
P('SITE B · THE LTI CLOCK ADVANCE   _merged_recover.py:1380    g += L * cp.SEASON')
P('-'*104)
P('   What it computes: for a row the availability register marks OUT, the young-credit clock is')
P('   AGED by the games he is expected to have LOST, so his young credit fades as if he had played.')
P('   Owner-ruled 2026-07-10 (advance, not pause).')
P()
lti={}
for line in open(WT+'/LTI_REGISTER.md'):
    m=re.match(r'\|\s*([a-z0-9\-]+)\s*\|([^|]+)\|\s*([AB])\s*\|\s*([0-9.]+)\s*\|',line)
    if m: lti[m.group(1)]=(m.group(3),float(m.group(4)))
P('   rows on LTI_REGISTER.md with an L value: %d'%len(lti))
Ls=collections.Counter(round(v[1],2) for v in lti.values())
P('   L values present: %s'%dict(Ls))
P('   phantom games added per row:  L*22 vs L*18')
for L in sorted(set(v[1] for v in lti.values())):
    P('     L=%.2f  ->  %5.2f games @22   %5.2f games @18   difference %+.2f games'%(L,L*22,L*18,L*18-L*22))
onb=[k for k in lti if k in B]
P('   of those, ON THE BOARD: %d'%len(onb))
P()
P('   The clock this feeds is _ycred_games, whose credit is COMPLETE at G0=46 games. So the site')
P('   only bites for rows still under 46 career+phantom games. Rows over it read 1.0 either way.')
u46=[]
for k in onb:
    p=S[k]
    d0=(p['year'] if p.get('type')=='MSD' else p['year']+1)-1
    g=sum(float(x.get('games') or 0) for x in (p.get('scoring') or []) if d0<x['year']<=2026)
    L=lti[k][1]
    if g+L*22<46 or g+L*18<46: u46.append((k,g,g+L*22,g+L*18,B[k]['v']))
P('   LTI rows still UNDER the G0=46 completion bar on either basis: %d'%len(u46))
P('   %-24s %7s %9s %9s %7s'%('key','raw g','g+L*22','g+L*18','price'))
for k,g,a,b,v in sorted(u46,key=lambda r:-r[4])[:12]:
    P('   %-24s %7.1f %9.1f %9.1f %7d'%(k,g,a,b,v))
P()
P('   DIRECTION: an 18-rebase adds FEWER phantom games, so the young credit fades LESS, so these')
P('   rows price HIGHER. Size is bounded by the young-credit multiplier on rows under 46 games.')
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cenpkg/CENSUS_SEASON_SITES_out.txt','w').write('\n'.join(out))
