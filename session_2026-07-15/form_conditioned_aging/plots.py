#!/usr/bin/env python3
"""Figures for the form-conditioned aging return. Reads summary.json + re-runs panel for raw points."""
import json, os, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import measure as M

HERE=os.path.dirname(os.path.abspath(__file__))
s=json.load(open(os.path.join(HERE,'summary.json')))
ages=list(range(29,37))
ca=s['by_age']['conditioned']; ua=s['by_age']['unconditioned']; sm=s['smoothed']; eng=s['engine']

def g(d,a,k): return d[str(a)][k]

# ---------- FIG 1: decline hazard + Δ vs age ----------
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(13,5.2))
# hazard
cn=[g(ca,a,'n_played') for a in ages]; un=[g(ua,a,'n_played') for a in ages]
ch=[g(ca,a,'h_lower') for a in ages]; uh=[g(ua,a,'h_lower') for a in ages]
chu=[g(ca,a,'h_upper') for a in ages]
chs=[sm['cond_hlo'][str(a)] for a in ages]; uhs=[sm['unc_hlo'][str(a)] for a in ages]
ax1.plot(ages,chs,'-',color='#c0392b',lw=2.5,label='conditioned (flat/rising) — smoothed H_lower',zorder=3)
ax1.plot(ages,uhs,'-',color='#2980b9',lw=2.0,label='unconditioned cohort — smoothed H_lower',zorder=3)
ax1.plot(ages,[sm['cond_hup'][str(a)] for a in ages],'--',color='#c0392b',lw=1.4,alpha=.8,label='conditioned — smoothed H_upper (exit=decline)')
# raw points sized by n
for a,h,n in zip(ages,ch,cn):
    if h is not None: ax1.scatter([a],[h],s=max(18,n*1.4),color='#c0392b',alpha=.35,edgecolor='none',zorder=2)
for a,h,n in zip(ages,uh,un):
    if h is not None: ax1.scatter([a],[h],s=max(18,n*0.7),color='#2980b9',alpha=.30,edgecolor='none',zorder=2)
for a in ages:
    if g(ca,a,'n_played')>0: ax1.annotate(f"n={g(ca,a,'n_played')}",(a,g(ca,a,'h_lower') or 0),fontsize=6.5,color='#7b241c',ha='center',va='bottom')
ax1.axvspan(32.5,36.5,color='0.9',zorder=0); ax1.text(34.5,0.05,'33–36 pooled\n(thin: cond n≈12)',ha='center',fontsize=8,color='0.4')
ax1.axhline(0.5,color='0.7',ls=':',lw=1)
ax1.set_xlabel('age (season year − birth year)'); ax1.set_ylabel('P(material demonstrated-level decline next season)')
ax1.set_title('Decline hazard by age — conditioned vs cohort'); ax1.set_ylim(0,1); ax1.legend(fontsize=8,loc='upper left')
# delta
cd=[sm['cond_dl'][str(a)] for a in ages]; ud=[sm['unc_dl'][str(a)] for a in ages]
ax2.plot(ages,cd,'-',color='#c0392b',lw=2.5,label='conditioned — smoothed E[ΔLc]')
ax2.plot(ages,ud,'-',color='#2980b9',lw=2.0,label='unconditioned — smoothed E[ΔLc]')
for a in ages:
    r=ca[str(a)]
    if r['dL_p25'] is not None:
        ax2.plot([a,a],[r['dL_p25'],r['dL_p75']],color='#c0392b',alpha=.35,lw=6,solid_capstyle='butt')
ax2.axhline(0,color='0.5',lw=1)
ax2.axvspan(32.5,36.5,color='0.9',zorder=0)
ax2.set_xlabel('age'); ax2.set_ylabel('E[next-season demonstrated-level change] (SC pts)')
ax2.set_title('Next-season ΔLc — conditioned (IQR bars) vs cohort'); ax2.legend(fontsize=8,loc='lower left')
fig.suptitle('Form-conditioned aging (ages 29–36): flat-or-rising to date does NOT buy slower decline',fontsize=12,weight='bold')
fig.tight_layout(rect=[0,0,1,0.96]); fig.savefig(os.path.join(HERE,'fig_hazard_by_age.png'),dpi=130)
print('wrote fig_hazard_by_age.png')

# ---------- FIG 2: worked-example trajectories ----------
named=[('gawn','Max Gawn (35 in 2026)'),('bontempelli','Marcus Bontempelli (31)'),
       ('english','Tim English (29)'),('heeney','Isaac Heeney (30)'),('dale','Bailey Dale (29)')]
fig2,axes=plt.subplots(1,5,figsize=(19,4.2),sharey=True)
for ax,(short,title) in zip(axes,named):
    traj=s['worked'].get(short+'_traj')
    if not traj: ax.set_title(title+' — n/a'); continue
    yrs=[t['year'] for t in traj]; raw=[t['raw'] for t in traj]; lc=[t['Lc'] for t in traj]
    ax.plot(yrs,raw,'o-',color='0.6',ms=4,lw=1,label='season avg (raw)')
    ax.plot(yrs,lc,'-',color='#1a5276',lw=2.2,label='Lc demonstrated')
    for t in traj:
        if t['partial']: ax.scatter([t['year']],[t['raw']],marker='s',color='#e67e22',s=45,zorder=5,label='2026 partial')
    # conditional band at his 2026 age
    p=[x for x in M.players if x.get('key')==dict(gawn='max-gawn',bontempelli='marcus-bontempelli',english='timothy-english',heeney='isaac-heeney',dale='bailey-dale')[short]][0]
    a26=M.age_of(p,2026); lc25=M.lvlcurr(p,2025)
    if a26 is not None and 29<=a26<=36 and lc25 is not None:
        dl=sm['cond_dl'].get(str(min(a26,36)));
        if dl is not None:
            ax.errorbar([2026.15],[lc25+dl],yerr=[[abs(s['by_age']['conditioned'][str(min(a26,36))]['dL_p25'] or 6)],[abs(s['by_age']['conditioned'][str(min(a26,36))]['dL_p75'] or 6)]] if False else 4.0,
                        fmt='D',color='#c0392b',ms=7,capsize=4,label='data says 2026 lands ~here')
            ax.annotate(f"cond E[Δ]={dl:+.1f}\nHlo≈{sm['cond_hlo'].get(str(min(a26,36))):.2f}",(2026.2,lc25+dl),fontsize=7,color='#7b241c',va='center')
    ax.set_title(title,fontsize=9); ax.set_xlabel('season'); ax.grid(alpha=.25)
axes[0].set_ylabel('SuperCoach avg / Lc'); axes[0].legend(fontsize=6.5,loc='lower left')
fig2.suptitle('Worked examples — career trajectory vs the conditional estimate for his age (2026 = partial, right-censored)',fontsize=11,weight='bold')
fig2.tight_layout(rect=[0,0,1,0.94]); fig2.savefig(os.path.join(HERE,'fig_worked_examples.png'),dpi=130)
print('wrote fig_worked_examples.png')
