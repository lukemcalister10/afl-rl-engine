import sys, json
sys.path.insert(0,'/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
import engine_load
g=engine_load.load(); MA=g['MA']
hc=g['_h_cut']; ash=g['_a_share']; ea=g['entry_anchor']; bf=g['_b_factor']; bs=g['_b_shape']; ba=g['_b_age']
Y=2026
rows=[p for p in MA.data if g['_isreal'](p)]
print("=== ITEM H CENSUS over the live board population ===")
cells={'union sitters':0,'all-pool-sitters':0,'mature nonRD':0,'none':0}
mat=[]
for p in rows:
    f=hc(p,Y)
    pool=bool(p.get('_pool')); typ=p.get('type'); age=ba(p)
    sitter=(sum(x['games'] for x in p['scoring'] if x['year']==Y)<=0)
    if pool and typ!='RD' and age is not None and age>=21.0:
        cells['mature nonRD']+=1; mat.append(p)
    if pool and sitter: cells['all-pool-sitters']+=1
    if f==1.0: cells['none']+=1
print("  rows:", len(rows))
for k,v in cells.items(): print(f"    {k:20} {v}")
print(f"\n  MATURE-nonRD cell n = {len(mat)}  (the cell sized at n=99, eff-n 46.2 in item_h_derive_out.txt)")
gm=[sum(x['games'] for x in p['scoring']) for p in mat]
est=[p for p in mat if any(x['games']>=6 for x in p['scoring'])]
print(f"  of those, career games: median {sorted(gm)[len(gm)//2]}  max {max(gm)}  ZERO-game {sum(1 for x in gm if x==0)}")
print(f"  ESTABLISHED (>=1 season of >=6 games): {len(est)} of {len(mat)}  ({100*len(est)/len(mat):.1f}%)")
print(f"  100+ career games: {sum(1 for x in gm if x>=100)}   50+: {sum(1 for x in gm if x>=50)}")
print("\n=== THE NAMED PLAYERS — every entry-arm-dependent channel, measured ===")
print(f"  {'player':20} {'type':5} {'draft_age':>9} {'effpk':>6} {'games':>6} {'_h_cut':>8} {'_a_share':>9} {'_b_shape':>9} {'entry_anchor':>13}")
for s in ['john-noble','max-hall','tom-mccarthy','james-peatling','mark-keane','flynn-perez','zac-banch','noah-mraz']:
    p=next((q for q in rows if q.get('key')==s), None)
    if p is None: continue
    cg=sum(x['games'] for x in p['scoring'])
    print(f"  {p['player'][:20]:20} {str(p.get('type')):5} {ba(p) if ba(p) is not None else float('nan'):9.2f} "
          f"{MA.effpk(p):6} {cg:6} {hc(p,Y):8.4f} {ash(p,Y):9.6f} {bs(ba(p)):9.4f} {ea(p):13.1f}")
print("\n=== ITEM B CONSERVATION — over WHAT set? (read from the assert itself) ===")
POOL=[p for p in MA.data if g['_isreal'](p) and p.get('_pool')]
before=sum(float(MA.pool_level(p))*g['_PL_F'] for p in POOL)
after=sum(ea(p) for p in POOL)
print(f"  set = the LIVE POOL population, n = {len(POOL)}   (assert at _merged_recover.py:2402-2414)")
print(f"  quantity conserved = SUM of ENTRY ANCHORS (a YEAR-ZERO object), not board prices")
print(f"    before {before:.4f}   after {after:.4f}   relative move {abs(after-before)/before:.3e}")
subs=[('established (>=1 season >=6g)', [p for p in POOL if any(x['games']>=6 for x in p['scoring'])]),
      ('no-evidence (0 career games)',  [p for p in POOL if sum(x['games'] for x in p['scoring'])==0])]
for lab,S in subs:
    b=sum(float(MA.pool_level(p))*g['_PL_F'] for p in S); a=sum(ea(p) for p in S)
    print(f"  SUBSET {lab:32} n={len(S):4}  entry-anchor sum {b:12.1f} -> {a:12.1f}  ({100*(a/b-1):+7.2f}%)")
import sys, io, contextlib
sys.path.insert(0,'/home/user/afl-rl-engine/docs/evidence/composition_2026-08-10')
import engine_load
g=engine_load.load(); MA=g['MA']
k=g['_b_renorm'](); PLF=g['_PL_F']
print(f"ITEM B renormaliser k = {k:.6f}")
print(f"  effective entry-anchor factor by draft age:")
for a in (18,19,20,21,22,25):
    print(f"    draft age {a}: _b_shape {g['_b_shape'](float(a)):.4f}  x k = {k*g['_b_shape'](float(a)):.4f}"
          f"   ({100*(k*g['_b_shape'](float(a))-1):+.1f}% on the entry anchor)")
print()
rows=[p for p in MA.data if g['_isreal'](p)]
print(f"{'player':20} {'games':>6} {'scoring rows':>13} {'unpl?':>6} {'ev(H on)':>9} {'ev(H off)':>10} {'anchor pre-B':>13} {'anchor post-B':>14}")
import os
for s in ['flynn-perez','paddy-cross','zac-banch','mitch-podhajski','john-noble','max-hall']:
    p=next((q for q in rows if q.get('key')==s), None)
    if p is None: print(s,"NOT FOUND"); continue
    cg=sum(x['games'] for x in p['scoring'])
    with contextlib.redirect_stdout(io.StringIO()):
        von=g['ev'](p,2026)
    a_post=g['entry_anchor'](p); a_pre=float(MA.pool_level(p))*PLF
    print(f"{p['player'][:20]:20} {cg:6} {len(p['scoring']):13} {str(p.get('_unpl') or '')[:6]:>6} {von:9} "
          f"{'(see board)':>10} {a_pre:13.1f} {a_post:14.1f}")
    print(f"     scoring: {p['scoring'][:4]}")
