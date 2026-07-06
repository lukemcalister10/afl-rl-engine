#!/usr/bin/env python3
# BATCH2 (2026-07-06) — RUC production-derived ceiling: single-lever proof + before->after $ table + sanity.
# Baseline (OLD 1.4xPVC cap engine) values are read from a frozen JSON dumped from the pre-change engine;
# CURRENT values come from the checked-out (candidate) engine. Non-ruck invariance is the single-lever claim.
import os, sys, io, json, contextlib
import numpy as np
RA = '/home/claude/rl_workspace/rl_after'
os.environ.update(PYTHONHASHSEED='0', RL_GAMMA='0.85', RL_PICK1='3000', RL_RUCK_TAX='0.25',
                  RL_RECENCY_DECAY='0.72', RL_PRIOR_TREES='400', PAR_RAMPS='22')
sys.path[:0] = [RA, '/home/claude/rl_workspace/forward_valuation', '/home/claude/rl_vendor']
os.chdir(RA)
BASE = sys.argv[1]                       # base_old.json (frozen OLD-engine board values, all real players)
OUT  = sys.argv[2]                       # output dir
G = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], G)
MA, ev, _isreal = G['MA'], G['ev'], G['_isreal']
bestlvl, delisted = G['bestlvl'], G['delisted']
def E(p):
    with contextlib.redirect_stdout(io.StringIO()): return ev(p)
def key(p): return f"{p['player']}|{p.get('year')}|{p.get('pick')}"
base = json.load(open(BASE))

# ---- single-lever: only rucks move; every non-ruck byte-identical ----
nonruc_moved = []; ruck_rows = []
for p in MA.data:
    if not _isreal(p): continue
    vN = E(p); k = key(p); vO = base[k]['v']; pos = MA.gfut(p)
    if pos != 'RUC':
        if vN != vO: nonruc_moved.append((k, pos, vO, vN))
    else:
        ruck_rows.append(dict(name=p['player'], key=k, pk=p.get('pick'), best=round(bestlvl(p),1),
                              old=vO, new=vN, d=vN-vO))
ruck_moved = [r for r in ruck_rows if r['d'] != 0]

# ---- ceiling curve (for the record) ----
G['_build_ruc_ceiling'](); xg, yg = G['_RUCCEIL']['grid']; meta = G['_RUCCEIL_META']

# ---- cross-position sanity (active players; ruck $ vs active non-ruck $ at bestlvl +-12) ----
def active(p): return _isreal(p) and not p.get('_retired') and not p.get('_pickless') and not delisted(p)
recs = []
for p in MA.data:
    if not active(p): continue
    recs.append((MA.gfut(p), bestlvl(p), E(p), p['player']))
nonruc = [(b,v) for pos,b,v,_ in recs if pos!='RUC' and b>0]
def band(b, w=12):
    xs = [v for bb,v in nonruc if abs(bb-b)<=w]
    if len(xs) < 8: xs = [v for bb,v in nonruc if abs(bb-b)<=2*w]
    return (np.percentile(xs,25), np.median(xs), np.percentile(xs,75), len(xs)) if xs else (0,0,0,0)
_moved_names = {r['name'] for r in ruck_moved}
flags = []
for pos,b,v,nm in recs:
    if pos!='RUC' or b<=0: continue
    q25,med,q75,n = band(b)
    if med>0 and (v>1.5*q75 or (q25>0 and v<0.5*q25)):
        flags.append(dict(name=nm, best=round(b,1), ruck=v, np_med=round(med), q75=round(q75),
                          ratio=round(v/max(q75,1),2), moved=(nm in _moved_names)))

# ---- write the report ----
os.makedirs(OUT, exist_ok=True)
md = []
md.append("# RUCK VALUES DERIVED OFF PRODUCTION — before→after (BATCH2, 2026-07-06)\n")
md.append(f"Engine (candidate) — production-derived ceiling replaces 1.4×PVC on the ruck production leg.\n")
md.append(f"Ceiling: HEAD={meta['head']} × synthprice_RUC(bestlvl) at refpk={meta['refpk']:.0f} "
          f"(grid ${meta['grid_lo']:.0f}..${meta['grid_hi']:.0f}). No-production rucks (bestlvl=0) → prior cap (byte-exact).\n")
md.append(f"\n## SINGLE-LEVER: non-ruck moved = **{len(nonruc_moved)}** (must be 0); rucks moved = **{len(ruck_moved)}**/{len(ruck_rows)}\n")
if nonruc_moved:
    md.append("!!! SPILL — STOP:\n")
    for k,pos,vO,vN in nonruc_moved[:30]: md.append(f"  - {pos} {k}: {vO} -> {vN}\n")

md.append("\n## Ruck $ — moved rucks + anchors + top rucks (before → after)\n")
md.append("| ruck | pick | bestlvl | OLD $ | NEW $ | Δ |\n|---|--:|--:|--:|--:|--:|\n")
anchors = {'Louis Emmett','Nicholas Naitanui'}
top = sorted(ruck_rows, key=lambda r:-r['old'])[:12]
show = {r['key'] for r in top} | {r['key'] for r in ruck_moved} | {r['key'] for r in ruck_rows if r['name'] in anchors}
for r in sorted([r for r in ruck_rows if r['key'] in show], key=lambda r:-r['new']):
    tag = ' **(anchor)**' if r['name'] in anchors else (' *moved*' if r['d'] else '')
    md.append(f"| {r['name']}{tag} | {r['pk']} | {r['best']:.1f} | {r['old']} | {r['new']} | {r['d']:+d} |\n")

md.append("\n## Cross-position SANITY (active players; ruck $ vs active non-ruck $ at bestlvl ±12) — FLAG only, NOT calibration\n")
if not flags:
    md.append("No flags.\n")
else:
    md.append("| ruck | bestlvl | ruck $ | non-ruck q75 | ratio | moved by this lever? |\n|---|--:|--:|--:|--:|:--:|\n")
    for f in sorted(flags, key=lambda x:-x['ratio']):
        md.append(f"| {f['name']} | {f['best']} | {f['ruck']} | {f['q75']} | {f['ratio']} | {'YES' if f['moved'] else 'no (byte-exact)'} |\n")

open(os.path.join(OUT,'ruck_deriv_before_after.md'),'w').write(''.join(md))
json.dump(dict(nonruc_moved=len(nonruc_moved), ruck_moved=[{k:r[k] for k in ('name','pk','best','old','new','d')} for r in ruck_moved],
               curve=dict(meta=meta, x=list(map(float,xg)), y=list(map(float,yg))),
               flags=flags), open(os.path.join(OUT,'ruck_deriv.json'),'w'), indent=1, default=float)
print("non-ruck moved:", len(nonruc_moved), "| rucks moved:", len(ruck_moved))
print("flags:", len(flags), "| moved-and-flagged:", sum(1 for f in flags if f['moved']))
print("wrote", os.path.join(OUT,'ruck_deriv_before_after.md'))
