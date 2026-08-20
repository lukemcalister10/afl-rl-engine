#!/usr/bin/env python3
"""THE SEASON-CONSTANT CENSUS — measurement half. READ-ONLY: no engine run, no dial, no board written.

Every constant below is READ OUT OF THE SOURCE at the line the census names, then the pure functions
are re-implemented here so the reading is independent of the engine's own reporting.
"""
import json, math, re, os, collections

WT='/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cen-wt'
MR=WT+'/engine/rl_after/_merged_recover.py'
CP=WT+'/engine/forward_valuation/conditional_prior.py'
out=[]
def P(s=''):
    print(s); out.append(str(s))

src=open(MR).read(); csrc=open(CP).read()
def con(pat,txt,cast=float):
    m=re.search(pat,txt)
    return cast(m.group(1)) if m else None

SEASON      = con(r'^SEASON=(\d+)',csrc,int) if re.search(r'^SEASON=(\d+)',csrc,re.M) else int(re.search(r'\nSEASON=(\d+)',csrc).group(1))
POLE_RAMP   = con(r'POLE_RAMP=([0-9.]+)',src)
LEVEL_RAMP  = con(r"LEVEL_RAMP=float\(os\.environ\.get\('RL_LEVEL_RAMP','([0-9.]+)'\)\)",csrc)
RECD        = con(r"RECENCY_DECAY=float\(os\.environ\.get\('RL_RECENCY_DECAY','([0-9.]+)'\)\)",csrc)
TAU_RHO     = con(r'O31_TAU_RHO=([0-9.]+)',src)
B_RHO       = con(r'O31_B_RHO=([0-9.]+)',src)
G0          = con(r'O37_G0=([0-9.]+)',src)
KAPPA       = con(r'O32_KAPPA=([0-9.]+)',src)
GAMMA       = con(r'O32_GAMMA=([0-9.]+)',src)
SEASON_FE   = con(r"SEASON_FE=_season_val\('calendar_progress',([0-9.]+)\)",src)
EXPO_F      = con(r"EXPO_F=_season_val\('exposure_pace',([0-9.]+)\)",csrc)
EXPO_DEN    = con(r'EXPO_DEN=([0-9.]+)',csrc)
G_FULL      = con(r'G_FULL = (\d+)',open(WT+'/engine/rl_after/lti_register.py').read(),int)

P('='*104)
P('THE SEASON-CONSTANT CENSUS — MEASUREMENT HALF')
P('='*104)
P('  constants read straight out of the source:')
P('    conditional_prior.SEASON      = %s   (the season-length constant itself)'%SEASON)
P('    lti_register.G_FULL           = %s   (asserted == cp.SEASON at wire time)'%G_FULL)
P('    POLE_RAMP                     = %s   (_merged_recover.py:103)'%POLE_RAMP)
P('    LEVEL_RAMP (RL_LEVEL_RAMP)    = %s   (conditional_prior.py:108)'%LEVEL_RAMP)
P('    RECENCY_DECAY                 = %s'%RECD)
P('    SEASON_FE / calendar_progress = %s   (the in-progress fraction at this cut)'%SEASON_FE)
P('    EXPO_F / EXPO_DEN             = %s / %s'%(EXPO_F,EXPO_DEN))
P('    MEASURED: rho31 tau/beta      = %.6f / %.6f'%(TAU_RHO,B_RHO))
P('    MEASURED: A(g) G0             = %.4f  -> half-conviction at %.2f games'%(G0,G0*math.log(2)))
P('    MEASURED: remix kappa/gamma   = %s / %s'%(KAPPA,GAMMA))
P()

# ---- the measured layers, re-implemented -------------------------------------------------------
def rho_base(g): return 0.0 if g<=0 else 1.0-math.exp(-((g/TAU_RHO)**B_RHO))
def rho31(g):
    r=rho_base(g)
    if r>0 and KAPPA>0: r=r+KAPPA*((g/GAMMA)*math.exp(1.0-g/GAMMA))*(1.0-r)
    return r
def A(g): return 1.0-math.exp(-g/G0)
# the F1 guarded credit curve, knots lifted from the source
kn=dict((int(a),float(b)) for a,b in re.findall(r'\((\d+),([0-9.]+)\)',
        re.search(r'O41_CREDIT=\((.*?)\)\n',src,re.S).group(1)))
def credit(g):
    g=float(g)
    if g<=0: return 0.0
    if g>=11: return 1.0
    n=int(math.floor(g)); f=g-n
    return kn[n] if f<=0 else (1-f)*kn[n]+f*kn[min(n+1,11)]

P('-'*104)
P('1 · WHAT THE MEASURED LAYERS ALREADY SAY ABOUT A 14-18 GAME SEASON')
P('-'*104)
P('   (these carry NO season norm — they are functions of RAW GAMES)')
P()
P('   %5s %10s %10s %10s   %s'%('games','credit(g)','A(g)','rho31(g)','share of the 22-game reading'))
for g in (1,2,5,8,10,11,12,14,15,16,18,20,22,23):
    P('   %5d %10.4f %10.4f %10.4f   credit %5.1f%%  A %5.1f%%  rho %5.1f%%'
      %(g,credit(g),A(g),rho31(g),
        100*credit(g)/credit(22),100*A(g)/A(22),100*rho31(g)/rho31(22)))
P()
P('   READ: the F1 credit curve is at FULL presence (1.0) from 11 games — a 14, 15 or 18-game')
P('   season already counts as a WHOLE season of presence, not 64%%/68%%/82%%. A(g) is at %.1f%% of its'%(100*A(15)/A(22)))
P('   22-game value by 15 games. rho31 is the only one still climbing, and it is a MEASURED')
P('   reliability curve fitted on raw games with no season length in it at all.')
P()

# ---- the algebraic cancellation ----------------------------------------------------------------
P('-'*104)
P('2 · THE CANCELLATION TEST — is cp.SEASON actually load-bearing where it appears?')
P('-'*104)
P('   _playable(p,Y)      = cp.SEASON * (seasons_elapsed + fE)          [_merged_recover.py:135]')
P('   _playable_fse(p,Y)  = SEASON    * (seasons_elapsed + fE)          [conditional_prior.py:111]')
P('   Both are consumed ONLY as  _playable(p,Y) / cp.SEASON  :')
P('       _merged_recover.py:302   POLE_RAMP * min(1, _playable(p,Y)/cp.SEASON)')
P('       conditional_prior.py:117 LEVEL_RAMP * min(1, _playable_fse(p,Y)/SEASON)')
P()
for S in (18,22,23,26):
    vals=[]
    for elapsed,fe in ((0,SEASON_FE),(1,SEASON_FE),(2,1.0),(5,1.0)):
        vals.append(S*(elapsed+fe)/S)
    P('   with SEASON=%2d  ->  playable/SEASON at (0,1,2,5) seasons elapsed = %s'%(S,['%.4f'%v for v in vals]))
P()
P('   VERDICT: the ratio is IDENTICALLY (seasons_elapsed + fE) for every value of SEASON.')
P('   cp.SEASON CANCELS EXACTLY at both sites. Changing 22 -> 18 there changes NOTHING.')
P('   The live bars at those two sites are POLE_RAMP=%s and LEVEL_RAMP=%s, which are GAMES bars,'%(POLE_RAMP,LEVEL_RAMP))
P('   not season-length constants — and LEVEL_RAMP is ALREADY 14.')
P()

# ---- exposure is a CAREER quantity, not a season quantity ---------------------------------------
S={x['key']:x for x in json.load(open(WT+'/engine/rl_after/rl_model_data.json'))}
def debutyr(p): return p['year'] if p.get('type')=='MSD' else p['year']+1
def exposure(p,Y):
    rows=[(x['year'],x['games']) for x in (p.get('scoring') or [])
          if x.get('games') and (debutyr(p)-1)<x['year']<=Y]
    return sum(g*(RECD**max(0,Y-yr)) for yr,g in rows)

P('-'*104)
P('3 · IS THE POLE_RAMP=22 BAR A "FULL SEASON" BAR? (it is fed by CAREER recency-weighted games)')
P('-'*104)
P('   A steady N-games-a-year player, recency decay %.2f, exposure after k seasons:'%RECD)
P('   %6s %9s %9s %9s %9s   %s'%('N/yr','after 1','after 2','after 3','after 4','reaches the 22 bar at'))
for N in (10,12,14,15,16,18,20,22):
    e=[]; tot=0.0
    for k in range(1,5):
        tot=N+RECD*tot; e.append(tot)
    hit=next((k+1 for k,v in enumerate(e) if v>=POLE_RAMP),None)
    P('   %6d %9.1f %9.1f %9.1f %9.1f   %s'%(N,e[0],e[1],e[2],e[3],
        ('season %d'%hit) if hit else 'never (steady-state %.1f)'%(N/(1-RECD))))
P()
P('   READ: the 22 bar is on RECENCY-WEIGHTED CAREER games, not one season. A 15-game-a-year')
P('   player clears it in season 2. It is not a "did he play a full season" test.')
P()

# ---- who is actually in the 14-18 band -----------------------------------------------------------
P('-'*104)
P('4 · WHO IS IN THE OWNER\'S 14-18 BAND, on the last COMPLETED season (2025)')
P('-'*104)
board=json.load(open(WT+'/docs/evidence/assembly_2026-08-19/../../..'
                    +'/engine/rl_after/rl_model_data.json')) if False else None
g25=collections.Counter()
band=[]
for k,p in S.items():
    r=[x for x in (p.get('scoring') or []) if int(x['year'])==2025 and x.get('games')]
    if not r: continue
    g=float(r[0]['games']); g25[int(g)]+=1
    if 14<=g<=18: band.append(k)
tot=sum(g25.values())
P('   store rows with a 2025 season: %d'%tot)
P('   in the 14-18 band: %d (%.1f%%)'%(len(band),100.0*len(band)/tot if tot else 0))
P('   19+ games        : %d (%.1f%%)'%(sum(v for kk,v in g25.items() if kk>=19),
                                       100.0*sum(v for kk,v in g25.items() if kk>=19)/tot if tot else 0))
P('   11-13 games      : %d'%sum(v for kk,v in g25.items() if 11<=kk<=13))
P('   1-10 games       : %d'%sum(v for kk,v in g25.items() if 1<=kk<=10))
P()
P('   what those 14-18 rows are worth under each layer, vs a 22-game season:')
for g in (14,15,16,17,18):
    P('     %2d games: credit %.3f (%.0f%% of 22)  A %.3f (%.0f%%)  rho31 %.3f (%.0f%%)'
      %(g,credit(g),100*credit(g)/credit(22),A(g),100*A(g)/A(22),rho31(g),100*rho31(g)/rho31(22)))
P()
open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/cenpkg/CENSUS_SEASON_MEASURE_out.txt','w').write('\n'.join(out))
