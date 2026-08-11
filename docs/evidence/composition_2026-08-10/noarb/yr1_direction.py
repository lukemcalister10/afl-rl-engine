"""PRE-EMIT DIRECTION PROBE for the ramp de-couple (#334 ORDER 2).

Question the pre-registration must answer BEFORE the emit: with the de-couple ON, first-season
qualifiers gain a nonzero anchor share s. The sign of the year-1 book move is therefore the sign of
(anch - e_full) on those rows -- the anchor is a SUPPORT where anch > e_full and a DRAG where
anch < e_full. This walks the year-1 as-of exactly as emit_matrix_338.py does (same truncation, same
BASE_REF/AGE_REF, same _pe_clear), records (e_full, anch, s) at the A site for every admitted row,
and prints the direction. It PRICES NOTHING and writes nothing into the repo.
"""
import sys, os, io, json, contextlib, statistics
sys.path.insert(0,'/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
import engine_load
g = engine_load.load()
MA = g['MA']; cp = g['cp']; ev = g['ev']
LOG = []
_orig = g['_a_blend']
def _rec(p, Y, e_full):
    tau = max(0.0, Y-cp.debutyr(p)) + ((g['_fEy'](Y,p)**1.5) if Y >= cp.debutyr(p) else 0.0)
    R = g['_R_surf'](g['_sitout_cls'](MA.gfut(p)), MA.effpk(p), tau)
    ea = g['entry_anchor'](p); anch0 = R*ea
    w = g['_c_w'](p, Y, e_full, ea)
    anch = anch0*(1.0+w*(g['C_H']-1.0))
    LOG.append(dict(key=p.get('key'), Y=Y, pick=MA.effpk(p), pos=MA.gfut(p),
                    e_full=float(e_full), anch=float(anch), s=float(g['_a_share'](p,Y)),
                    gy=sum(x['games'] for x in p['scoring'] if x['year']==Y),
                    cg=sum(x['games'] for x in p['scoring'] if x['year']<=Y)))
    return _orig(p, Y, e_full)
g['_a_blend'] = _rec

def _min_tenure(p):
    if p.get('type')=='ND' and not p.get('_pickless'):
        pk=MA.effpk(p)
        if pk<=20: return 4
        if pk<=40: return 3
    return 2
def _debut_year(p):
    C=p.get('year'); return None if C is None else (C if p.get('type')=='MSD' else C+1)
def _listed_through(p,lastscore):
    LL=p.get('_last_listed')
    if LL is not None: return LL
    if not p.get('_retired'): return None
    d=_debut_year(p)
    return max((d+_min_tenure(p)-1) if d is not None else 0, lastscore)

def eligible(p): return MA.GRP.get(p.get('pos')) and not p.get('_pvc_exclude')
players=[p for p in MA.data if eligible(p)]
best={}
for p in players:
    k=(p.get('key') or MA.slug(p['player']), p.get('type'), p.get('year'))
    if k not in best or len(p['scoring'])>len(best[k]['scoring']): best[k]=p
players=list(best.values())
# the harness population: ND, picks 1-64, classes 2004-2022
POP=[p for p in players if p.get('type')=='ND' and p.get('pick') and 1<=p['pick']<=64
     and p.get('year') and 2004<=p['year']<=2022]
print("population n =", len(POP))

# walk each entrant's OWN year 1 (Y = draft year + 1), grouped by Y so the truncation is done once
byY={}
for p in POP: byY.setdefault(p['year']+1, []).append(p)
for Y in sorted(byY):
    saved={}
    for p in players:
        if (p.get('year') or 9999) > Y: continue
        LL=p.get('_last_listed'); RET=p.get('_retired')
        lastscore=max((r['year'] for r in p['scoring']), default=0)
        saved[id(p)]=(p['scoring'], RET, LL)
        p['scoring']=[r for r in p['scoring'] if r['year']<=Y]
        el=_listed_through(p,lastscore)
        p['_retired']=False
        p['_last_listed']= el if (el is not None and el<Y) else None
    MA.BASE_REF=Y; MA.AGE_REF=Y; MA._pe_clear()
    for p in byY[Y]:
        try:
            with contextlib.redirect_stdout(io.StringIO()): ev(p,Y)
        except Exception as e: pass
    for p in players:
        if id(p) in saved: p['scoring'],p['_retired'],p['_last_listed']=saved[id(p)]
    MA._pe_clear()
MA.BASE_REF=MA.AGE_REF=2026; MA._pe_clear()

print("A-site calls at cohort year 1 (admitted rows only):", len(LOG))
if LOG:
    sup=[r for r in LOG if r['anch']>r['e_full']]
    drg=[r for r in LOG if r['anch']<r['e_full']]
    print(f"  SUPPORT (anch > e_full): {len(sup)}  ({100*len(sup)/len(LOG):.1f}%)")
    print(f"  DRAG    (anch < e_full): {len(drg)}  ({100*len(drg)/len(LOG):.1f}%)")
    rat=[r['anch']/r['e_full'] for r in LOG if r['e_full']>0]
    print(f"  anch/e_full  median {statistics.median(rat):.4f}  mean {statistics.fmean(rat):.4f}")
    print(f"  built-A share s: max {max(r['s'] for r in LOG):.6f} (0 == the year-1 silence)")
    # POOLED: the book-weighted direction. Sum(anch) vs Sum(e_full) is what a pooled ratio moves on.
    se=sum(r['e_full'] for r in LOG); sa=sum(r['anch'] for r in LOG)
    print(f"  POOLED sum(anch)/sum(e_full) = {sa/se:.4f}   (>1 => a nonzero share LIFTS the pooled year-1 book)")
    cg=[r['cg'] for r in LOG]
    print(f"  career games at yr1: median {statistics.median(cg)}  <18: {sum(1 for x in cg if x<18)}  >=18: {sum(1 for x in cg if x>=18)}")
    LOG.sort(key=lambda r:(r['pick'], r['key'] or ''))
    print("\n  THE 20-ROW SAMPLE (evenly spaced through the pick order):")
    step=max(1,len(LOG)//20)
    print(f"    {'key':28} {'pk':>3} {'pos':5} {'gy':>3} {'cg':>3} {'e_full':>9} {'anch':>9} {'anch/e':>7}")
    for r in LOG[::step][:20]:
        print(f"    {str(r['key'])[:28]:28} {r['pick']:3} {str(r['pos'])[:5]:5} {r['gy']:3} {r['cg']:3} "
              f"{r['e_full']:9.1f} {r['anch']:9.1f} {r['anch']/r['e_full'] if r['e_full'] else 0:7.4f}")
json.dump(LOG, open('/tmp/claude-0/-home-user-afl-rl-engine/7ac96fea-1199-5b6a-9d77-ded9f53694f7/scratchpad/o3/yr1_direction.json','w'))
