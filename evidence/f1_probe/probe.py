#!/usr/bin/env python3
# F1/F2 pipeline-divergence probe. READ-ONLY. Run from /home/claude/rl_workspace/rl_after
# (byte-identical mirror of repo engine/rl_after @ commit 389ac39, engine md5 c47cb43d).
import io,contextlib,json,os,statistics,sys

REPO="/home/user/afl-rl-engine"
SHIP=json.load(open(REPO+"/data/rl_build/rl_app_data.json"))
SHIP_ACT={r['key']:r for r in SHIP['active']}

# ---- GATED engine: exec _merged_recover, use ITS MA/ev (players ARE in _REAL) ----
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; ev=g['ev']; REAL=g['_REAL']
print("RUC_PRIOR_CAP (baked default) =", g.get('RUC_PRIOR_CAP'))

def gfind(pred):
    c=[p for p in MA.data if pred(p)]; return c[0] if c else None

# fingerprint locators keyed by ID/pick/cohort, NEVER surname alone
def is_louis(p):  return 'emmett' in p['player'].lower() and p.get('year')==2025 and p.get('pick')==27
def is_petracca(p): return 'petracca' in p['player'].lower() and p.get('year')==2014 and p.get('pick')==2

louis_g=gfind(is_louis); petr_g=gfind(is_petracca)

# ---- EXPORT-PATH replication: exec rl_model.py in a SEPARATE namespace like rl_export.py line 6 ----
ns={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("rl_model.py").read().split("print('PVC:'")[0], ns)
xplayers=ns['players']
def xfind(pred):
    c=[p for p in xplayers if pred(p)]; return c[0] if c else None
louis_x=xfind(is_louis); petr_x=xfind(is_petracca)

print("\n=== ID-MEMBERSHIP TEST (crux of F1) ===")
print("gated  Louis id in _REAL:", id(louis_g) in REAL if louis_g else "NOTFOUND")
print("export Louis id in _REAL:", id(louis_x) in REAL if louis_x else "NOTFOUND")
n_in=sum(1 for p in xplayers if id(p) in REAL)
print("export players total=%d,  how many of them have id in _REAL: %d"%(len(xplayers),n_in))

def row(tag,p):
    if not p: 
        print(tag,"NOTFOUND"); return None
    with contextlib.redirect_stdout(io.StringIO()):
        v=ev(p,2026)
    return v

print("\n=== FINGERPRINT 1: Louis Emmett (id? RUC pick27/2025, key louis-emmett) ===")
lg=row("gated  ",louis_g); lx=row("export ",louis_x); ls=SHIP_ACT['louis-emmett']['v']
print("  GATED ev(p,2026)   =",lg,"  (id in _REAL -> ruck cap 1.4x applies)")
print("  EXPORT ev(p,2026)  =",lx,"  (id NOT in _REAL -> cap stripped)")
print("  SHIPPED active.v   =",ls)
if louis_g:
    print("  gfut=",MA.gfut(louis_g)," draftval(PVC@ep)=",g['draftval'](louis_g)," cap=%.1fxPVC=%.0f"%(g['RUC_PRIOR_CAP'],g['RUC_PRIOR_CAP']*g['draftval'](louis_g)))

print("\n=== FINGERPRINT 2: Christian Petracca (id? MID pick2/2014, key christian-petracca) ===")
pg=row("gated  ",petr_g); px=row("export ",petr_x); ps=SHIP_ACT['christian-petracca']
print("  GATED ev(p,2026)=",pg,"  EXPORT ev(p,2026)=",px,"  SHIPPED.v=",ps['v'])
if petr_g:
    print("  engine pos (raw p['pos'])=",petr_g.get('pos'),"  bnow=",g['MA'].__dict__ and None)
    print("  gated  gfut=",MA.gfut(petr_g),"  bnow(grp)=",g['bnow'](petr_g) if 'bnow' in g else 'n/a')
print("  shipped: gf=",ps['gf']," grp=",ps['grp']," fut=",ps['fut'])

# save machine-readable
out={'louis':{'gated':lg,'export':lx,'shipped':ls},
     'petracca':{'gated':pg,'export':px,'shipped':ps['v'],'ship_gf':ps['gf'],'ship_grp':ps['grp'],'ship_fut':ps['fut']},
     'export_in_real':n_in,'export_total':len(xplayers)}
json.dump(out,open(REPO+"/evidence/f1_probe/fingerprints.json","w"),indent=2)
print("\nwrote fingerprints.json")
