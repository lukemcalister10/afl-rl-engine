"""Definitive: does the BOARD's own pricing function ev() respond to the swapped curve
for the zero-game actives? Execs the full engine exactly as the matrix emitter does."""
import os,io,contextlib,json,sys,hashlib
src=open('_merged_recover.py').read().split('print("=== AFTER')[0]
G={'__name__':'_probe_ev'}
with contextlib.redirect_stdout(io.StringIO()):
    exec(src,G)
MA=G['MA']; ev=G['ev']
keys=json.load(open(sys.argv[1]))
out={'PVC2M_payload':hashlib.md5(json.dumps({str(k):int(MA._PVC2M[k]) for k in range(1,65)},sort_keys=True).encode()).hexdigest()[:8],
     'PVC0_payload':hashlib.md5(json.dumps({str(k):int(G['_PVC0'][k]) for k in range(1,65)},sort_keys=True).encode()).hexdigest()[:8],
     'v0surf_sig':G['_V0CURVE_META'].get('_v0surf_sig','')[:12],'players':{}}
byk={p.get('key'):p for p in MA.data if p.get('key')}
for k in keys:
    p=byk.get(k)
    if p is None: out['players'][k]={'error':'absent'}; continue
    rec={}
    for tag,yr in (('ev_2026',2026),):
        try:
            with contextlib.redirect_stdout(io.StringIO()): rec[tag]=ev(p,yr)
        except Exception as e: rec[tag]='ERR:'+str(e)
    try:
        with contextlib.redirect_stdout(io.StringIO()): rec['value_bal']=MA.value(p,'bal')
    except Exception as e: rec['value_bal']='ERR:'+str(e)
    rec['v0_start']=round(G['v0_start'](p),2) if 'v0_start' in G else None
    rec['ep']=int(MA.effpk(p))
    out['players'][k]=rec
print(json.dumps(out,indent=1))
