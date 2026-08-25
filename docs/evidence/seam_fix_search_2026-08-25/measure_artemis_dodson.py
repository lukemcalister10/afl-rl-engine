#!/usr/bin/env python3
"""Owner questions 2026-08-25: (1) does the model credit Artemis's LOW time-in-system, vs an
18-drafted twin with identical output? (2) Dodson's fade clock — how many sitting years is he
actually being charged, and what would one fewer cost? Read-only, in-process counterfactuals."""
import contextlib, copy, io, json, os, sys
os.environ.setdefault('RL_CONFIG_MODE','gate')
sys.path.insert(0, os.environ['RL_REPO'])
import config_manifest; config_manifest.enforce('gate')
g={}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open('_merged_recover.py').read().split('print("=== AFTER')[0], g)
MA=g['MA']; evf=g['ev']; F=1.0524; Y=2026
def price(p): return round(evf(p,Y)/F)
row={p['key']:p for p in MA.data}

# (1) ARTEMIS — the time-in-system axis, output held fixed
a=row['jaxon-artemis']
print('ARTEMIS live:', price(a), '| tenure', Y-a['year']+1, '| age', Y-a['_by'])
for yr in (2025, 2024):
    t=copy.deepcopy(a); t['year']=yr
    if 'stream_year' in t: t['stream_year']=yr
    MA.data.append(t); t['key']='artemis-twin'
    try:
        print('  twin entered %d (tenure %d, SAME age, SAME 6g@51.3): %d' % (yr, Y-yr+1, price(t)))
    finally:
        MA.data.remove(t)

# (2) DODSON — the sitting clock
d=row['alex-dodson']
print('DODSON live:', price(d), '| entered', d['year'], '| playable seasons 2025,2026 (=2 opportunities); tenure formula gives', Y-d['year']+1)
sc=d['scoring']
d['scoring']=[]
try:
    print('  never-played self as priced today:', price(d))
    for yr in (2025, 2023):
        t=copy.deepcopy(d); t['year']=yr
        if 'stream_year' in t: t['stream_year']=yr
        t['key']='dodson-twin'
        MA.data.append(t)
        try:
            print('  never-played twin entered %d (one %s sitting year): %d' % (yr, 'fewer' if yr==2025 else 'more', price(t)))
        finally:
            MA.data.remove(t)
finally:
    d['scoring']=sc
