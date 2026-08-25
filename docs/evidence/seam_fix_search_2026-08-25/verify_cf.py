#!/usr/bin/env python3
"""Verify the 51-row census counterfactuals LIVE, in-process, read-only (main checkout).
Counterfactual method of record: p['scoring']=[] -> ev(p,2026)/1.0524 -> restore (exact on 48 sitters)."""
import contextlib, html, io, json, os, sys, unicodedata
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest
config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']
F=1.0524
def norm(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode()
    return s.lower().replace(' ','-').replace("'",'')
byname={}
probe=MA.data[0]
print('store row fields sample:', sorted(probe.keys())[:30])
for p in MA.data:
    for f in ('player','name','key','display'):
        v=p.get(f)
        if isinstance(v,str) and v:
            byname.setdefault(norm(v), p)
rows=json.load(open('/home/user/seam_fix/census51.json'))
ev=g.get('ev') or MA.ev if hasattr(MA,'ev') else None
# find the ev callable the census used
cand=[k for k,v in g.items() if callable(v) and k in ('ev','gated_ev','ev_gated')]
print('ev candidates:', cand)
evf=g[cand[0]] if cand else None
bad=0
out=[]
for r in rows:
    p=byname.get(norm(html.unescape(r['player'])))
    if p is None:
        print('MISS', r['player']); bad+=1; continue
    v_ev=evf(p,2026)/F
    sc=p['scoring']
    p['scoring']=[]
    try:
        v_cf=evf(p,2026)/F
    finally:
        p['scoring']=sc
    ok_ev = round(v_ev)==r['cur']
    ok_cf = round(v_cf)==r['cf']
    if not (ok_ev and ok_cf):
        bad+=1
        print('DIFF %-22s cur %d vs %d | cf %d vs %d' % (r['player'], r['cur'], round(v_ev), r['cf'], round(v_cf)))
    out.append(dict(r, v_ev=round(v_ev,2), v_cf=round(v_cf,2)))
json.dump(out, open('/home/user/seam_fix/census51_live_verified.json','w'), indent=1)
print('verified %d rows, %d mismatches' % (len(out), bad))
