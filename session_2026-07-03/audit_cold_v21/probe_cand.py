import io, contextlib, json, numpy as np
OUT=open('/tmp/claude-0/-home-user-afl-rl-engine/a62bb32e-b9ba-53aa-805e-a08c12f3bf5a/scratchpad/probe_cand_out.txt','w')
def P(*a): print(*a, file=OUT)
g={}
with contextlib.redirect_stdout(io.StringIO()):
    src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
    exec(src, g)
MA=g['MA']; ev=g['ev']; raw_ev=g['raw_ev']; v0=g['v0_start']; sitout_ev=g['sitout_ev']
iso=g['iso_corr']; nseas=g['nseas']; nseas_pro=g['nseas_pro']; delisted=g['delisted']
bestlvl=g['bestlvl']; PR=g['PR']; cp=g['cp']; synth=g['synth']; GRPPOS=g['GRPPOS']
floor_frac=g['floor_frac']; draftval=g['draftval']; R_SIT=g['R_SIT']; LAM_SIT=g['LAM_SIT']
_sitcls=g['_sitout_cls']; _fEy=g['_fEy']; SEASON_FE=g.get('SEASON_FE'); M3_FE=g.get('M3_FE')
ev_prefloor=g['ev_prefloor']; _prod_path=g['_prod_path']
P("== ENV/CONST ==  SEASON_FE=%r  M3_FE=%r  R_SIT.nonKPP=%s  LAM_SIT=%s"%(SEASON_FE,M3_FE,R_SIT['nonKPP'],LAM_SIT))

def mk(pos,pk,year,scoring,dob='2006-03-01'):
    d={'player':'synth','pos':GRPPOS.get(pos),'pick':float(pk),'year':year,'dob':dob,'type':'ND',
       '_pos_now':None,'_fut':[],'scoring':scoring}
    d['games']=sum(x['games'] for x in scoring); return d

def key(name,cohort,pick):
    c=[p for p in MA.data if p['player'].strip().lower()==name.strip().lower()
       and int(p.get('year') or -1)==cohort and abs(float(p.get('pick') or -9)-pick)<0.6 and MA.GRP.get(p.get('pos'))]
    return c[0] if c else None

# ---- PANEL at candidate ----
PANEL=[('Nick Daicos',7059),('Marcus Bontempelli',3101),('Harry Sheezel',7287),('Max Gawn',2126),
       ('Harley Reid',3523),('Josh Ward',1782),('Darcy Moore',177),('Taylor Goad',545),
       ('Josh Smillie',896),('Will Green',741)]
def findn(nm):
    c=[p for p in MA.data if nm.lower() in p['player'].lower() and MA.GRP.get(p.get('pos'))]; return c[0] if c else None
P("\n== PANEL @ candidate c8051893 =="); pok=0
for nm,exp in PANEL:
    p=findn(nm); v=ev(p) if p else None; ok=(v==exp); pok+=ok
    P("  %-22s cand=%-6s control_exp=%-6d %s"%(nm,v,exp,'OK' if ok else '<-- MOVED'))
P("  PANEL cand-vs-control-expected: %d/10 identical"%pok)

# ---- ANCHORS: name|cohort|pick ----
P("\n== V0 (live start value) + ev @ v2.1 ==")
ANCH=[('Harry Dean',2025,3),('Sullivan Robey',2025,9),('Daniel Annable',2025,6),
      ('Sam Cumming',2025,7),('Dylan Patterson',2025,5),('Jacob Farrow',2025,10),
      ('Xavier Taylor',2025,11),('Oskar Taylor',2025,15),('Louis Emmett',2025,27),
      ('Jack Ison',2025,47),('Cooper Lord',2024,9),('Tobie Travaglia',2024,8),
      ('Angus Clarke',2024,39)]
def g26(p): return sum(x['games'] for x in p['scoring'] if x['year']==2026)
def prod26(p):
    s=[x['avg'] for x in p['scoring'] if x['year']==2026 and x['games']>0]; return s[0] if s else None
for nm,co,pk in ANCH:
    p=key(nm,co,pk)
    if not p: P("  %-20s|%d|%d  NOT FOUND"%(nm,co,pk)); continue
    P("  %-18s|%d|pk%-3d pos=%-8s g26=%-3d prod=%-6s PVC=%-5.0f V0=%-6.0f ev=%-6d ns_pro=%d dlst=%s"%(
        nm,co,pk,MA.gfut(p),g26(p),str(prod26(p)),draftval(p),v0(p),ev(p),nseas_pro(p),delisted(p)))

# ---- PATTERSON full trajectory decomposition ----
P("\n== A4 PATTERSON TRAJECTORY (name|2025|pk5) ==")
pat=key('Dylan Patterson',2025,5)
if pat:
    Y=2026; fe=_fEy(Y); dby=cp.debutyr(pat)
    tau=max(0.0,Y-dby)+(fe if Y>=dby else 0.0)
    cls=_sitcls(MA.gfut(pat))
    R=float(np.interp(tau,[0,1,2,3,4,5,6],[1.0]+R_SIT[cls]))
    gy=sum(x['games'] for x in pat['scoring'] if x['year']==Y)
    lam=float(np.interp(min(gy/fe,6.0),[0,1,2,3,4,5,6],LAM_SIT))
    V0=v0(pat); efull=_prod_path(pat,Y)
    anchor=(1.0-lam)*R*V0+lam*efull
    yis=Y-int(pat.get('year') or 0); fl=floor_frac(yis)*draftval(pat)
    P("  debutyr=%d  fE(_fEy)=%.4f  tau=%.4f  class=%s"%(dby,fe,tau,cls))
    P("  V0=%.1f  R(tau)=%.4f  lam=%.4f (g26=%d)  e_full=%.1f"%(V0,R,lam,gy,efull))
    P("  sitout anchor = (1-lam)*R*V0 + lam*e_full = %.1f"%anchor)
    P("  B5 floor: yis=%d  floor_frac=%.3f  draftval=%.0f  floor=%.1f"%(yis,yis and floor_frac(yis),draftval(pat),fl))
    P("  ev_prefloor=%d  FINAL ev=%d"%(ev_prefloor(pat,Y),ev(pat)))
    P("  PRORATED? tau uses fE=%.4f not 1.0 -> decay accrued only %.1f%% of season1"%(fe,R and (1-R)/(1-R_SIT[cls][0])*100 if R<1 else 0))

# ---- B6 ramp: first-evidence MID pk10 avg85, games 0..14 ----
P("\n== A3b/B6 RAMP: first-evidence MID pk10 @avg85, games 0..14 ==")
def ramp(pos,pk,avg,grange):
    out=[]
    for gg in grange:
        sc=[{'year':2026,'games':gg,'avg':float(avg)}] if gg>0 else []
        out.append(ev(mk(pos,pk,2025,sc)))
    return out
r=ramp('MID',10,85,range(0,15))
P("  ramp(0..14)=%s"%r)
steps=[r[i+1]-r[i] for i in range(len(r)-1)]
P("  steps=%s"%steps)
T=r[6]-r[0]
P("  dips(<0)=%s  T(0->6)=%d  max|step|first6=%d (cap50%%T=%d)  rise-by-3g=%d (need25%%T=%d)"%(
    [s for s in steps if s<0], T, max(abs(s) for s in steps[:6]), int(0.5*T), r[3]-r[0], int(0.25*T)))
# low-rate ramp avg40
r40=ramp('MID',10,40,range(0,9))
P("  low-rate avg40 ramp(0..8)=%s dips=%s"%(r40,[r40[i+1]-r40[i] for i in range(len(r40)-1) if r40[i+1]-r40[i]<0]))
# output-monotone at fixed games g=2
P("\n== A3b OUTPUT-MONOTONE at fixed g=2, MID pk10, avg 20..110 ==")
om=[]
for av in range(20,111,10):
    om.append(ev(mk('MID',10,2025,[{'year':2026,'games':2,'avg':float(av)}])))
P("  avg20..110 -> %s  strictly-rising=%s"%(om, all(om[i+1]>=om[i] for i in range(len(om)-1))))

# ---- Position preservation: same-pick zero-evidence synths ----
P("\n== A3d POSITION PRESERVATION: same-pick(12) zero-evidence sit-out synths ==")
for pos in ['MID','KEY_DEF','GEN_DEF','RUC']:
    sp=mk(pos,12,2025,[])
    P("  %-8s V0=%.0f  ev(sit-out,0g)=%d"%(pos,v0(sp),ev(sp)))

# ---- Pre-season penalty exactly zero: ev(draft-year)==V0 ----
P("\n== A3a PRE-SEASON HOLD: ev(p, debutyr-1)==V0 for a not-yet-started synth ==")
sp=mk('MID',8,2026,[],dob='2007-03-01')
dby=cp.debutyr(sp)
P("  debutyr=%d  V0=%.2f  ev(debutyr-1=%d)=%.2f  equal=%s"%(dby,v0(sp),dby-1,ev(sp,dby-1),abs(v0(sp)-ev(sp,dby-1))<1))

# ---- 2025 cohort total (active, board group) ----
P("\n== A7 2025 COHORT TOTAL (live @ v2.1) ==")
coh=[p for p in MA.data if int(p.get('year') or -1)==2025 and MA.GRP.get(p.get('pos')) and not p.get('_double_count')
     and not delisted(p) and (p.get('pick') or p.get('_ft'))]
tot=sum(ev(p) for p in coh)
P("  n(active 2025, board grp, not delisted, picked)=%d  sum ev=%d"%(len(coh),tot))
# under-seam: never-qualified through 2026, 1-5 g26
useam=[p for p in coh if nseas_pro(p)==0 and 1<=g26(p)<=5]
P("  under-seam (ns_pro==0, 1<=g26<=5) n=%d sum=%d"%(len(useam),sum(ev(p) for p in useam)))
zg=[p for p in coh if g26(p)==0 and nseas_pro(p)==0]
P("  zero-game sit-outs (ns_pro==0,g26==0) n=%d sum=%d"%(len(zg),sum(ev(p) for p in zg)))
OUT.close()
print("done")
