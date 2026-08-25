#!/usr/bin/env python3
"""Scope census: every ACTIVE row with >=1 career game and NO banked level (all seasons <6 games).
Compares against the 51-row census scope (1-8 games, tenure 1-4). Read-only."""
import contextlib, io, json, os, sys
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; evf=g['ev']; F=1.0524
Y=2026
census=json.load(open('/home/user/seam_fix/census51.json'))
import html
cnames={html.unescape(r['player']) for r in census}
rows=[]
for p in MA.data:
    if p.get('_retired'): continue
    sc=[x for x in (p.get('scoring') or []) if x.get('year',0)<=Y]
    gtot=sum(x.get('games',0) for x in sc)
    if gtot<1: continue
    if any(x.get('games',0)>=6 for x in sc): continue      # has a banked level -> out
    ten=Y-int(p.get('year') or Y)+1
    c=sum(x['avg']*x['games'] for x in sc if x.get('games',0)>0)/gtot
    v=evf(p,Y)/F
    s0=p['scoring']; p['scoring']=[]
    try: vcf=evf(p,Y)/F
    finally: p['scoring']=s0
    nm=p.get('player') or p.get('name') or ''
    rows.append({'player':nm,'games':int(gtot),'tenure':int(ten),'cameo':round(c,1),
                 'cur':round(v),'cf':round(vcf),'in_census':nm in cnames})
extra=[r for r in rows if not r['in_census']]
print('no-banked-level rows with >=1 game:', len(rows), '| in the 51-census:', sum(r['in_census'] for r in rows), '| OUTSIDE it:', len(extra))
for r in extra:
    print('  OUTSIDE %-24s g=%2d t=%d c=%5.1f cur=%5d cf=%5d %s'
          % (r['player'],r['games'],r['tenure'],r['cameo'],r['cur'],r['cf'],
             '<- BELOW CF' if r['cf']>r['cur'] else ''))
missed=[n for n in cnames if n not in {r['player'] for r in rows}]
print('census rows NOT captured by no-banked-level scope:', missed)
json.dump(rows, open('/home/user/seam_fix/scope_census.json','w'), indent=1)
